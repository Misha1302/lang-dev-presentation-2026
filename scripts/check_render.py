#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, shutil, subprocess, sys, time
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'rebuild-2026-09-17' / 'delegates-rebuild-deck.html'
ARTIFACTS = ROOT / 'render-artifacts'
if ARTIFACTS.exists(): shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()
raw = TARGET.read_text(encoding='utf-8')
keys = re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*(?:data-note-key|data-note)="([^"]+)"', raw)
if len(keys) < 21 or len(keys) != len(set(keys)):
    raise SystemExit('Render check FAILED: invalid slide key set')
browser = next((n for n in ['google-chrome-stable','google-chrome','chromium-browser','chromium','chrome'] if shutil.which(n)), None)
if browser:
    server = subprocess.Popen([sys.executable,'-m','http.server','8878','--bind','127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(.5)
        main_count = len([k for k in keys if k.startswith('m')])
        samples = ['#1', '#2', '#7', '#13', '#17', f'#{main_count}']
        for i, target in enumerate(samples, 1):
            out = ARTIFACTS / f'delegates-smoke-{i:02d}.png'
            url = f'http://127.0.0.1:8878/rebuild-2026-09-17/delegates-rebuild-deck.html{target}'
            r = subprocess.run([browser,'--headless=new','--disable-gpu','--disable-dev-shm-usage','--no-sandbox','--window-size=1366,768','--hide-scrollbars',f'--screenshot={out}',url], capture_output=True, text=True, timeout=35)
            if r.returncode != 0 or not out.exists():
                raise SystemExit('Render check FAILED: screenshot failed for '+target+' '+r.stderr[:300])
        print(f'Render check PASS: {len(keys)} slides parsed; {len(samples)} Chrome smoke screenshots captured')
    finally:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired: server.kill()
else:
    print(f'Render check PASS (parser-only): {len(keys)} slides parsed; Chrome unavailable in this environment')
