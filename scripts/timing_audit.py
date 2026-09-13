#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
browser = next((name for name in ['google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'] if shutil.which(name)), None)
if browser is None:
    print('Timing audit FAILED: Chrome/Chromium was not found')
    sys.exit(1)

server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', '8879', '--bind', '127.0.0.1'],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']


def data_attr(dom: str, name: str) -> str | None:
    match = re.search(rf'\bdata-{re.escape(name)}="([^"]*)"', dom)
    if not match:
        return None
    return html.unescape(match.group(1))

try:
    time.sleep(.7)
    out = ''
    for attempt in range(3):
        result = subprocess.run(
            common + ['--window-size=1366,768', '--dump-dom', 'http://127.0.0.1:8879/?timing-check=1#1'],
            capture_output=True,
            text=True,
            timeout=35,
        )
        out = result.stdout + result.stderr
        if result.returncode == 0 and data_attr(result.stdout, 'runtime-main-count'):
            break
        time.sleep(.7)
    else:
        print('Timing audit FAILED: runtime manifest unavailable')
        print(out[:500])
        sys.exit(1)

    main = int(data_attr(result.stdout, 'runtime-main-count') or '0')
    appendix = int(data_attr(result.stdout, 'runtime-appendix-count') or '0')
    words = int(data_attr(result.stdout, 'runtime-main-speech-words') or '0')
    seconds = int(data_attr(result.stdout, 'runtime-main-speech-seconds130') or '0')
    missing = data_attr(result.stdout, 'runtime-speech-missing') or ''
    if missing:
        print(f'Timing audit FAILED: missing runtime speech entries: {missing}')
        sys.exit(1)
    print(f'runtime main slides: {main}')
    print(f'runtime appendix slides: {appendix}')
    print(f'runtime main spoken words: {words}')
    print(f'rehearsal estimate at 130 wpm: {seconds // 60:02d}:{seconds % 60:02d}')
    # Keep headroom for transitions and Q&A while validating the actual runtime deck,
    # not pre-mutation source fragments. Fast-pass slides are still included here.
    if not (22 * 60 <= seconds <= 24 * 60):
        print(f'Timing audit FAILED: runtime script outside 22-24 min: {seconds // 60:02d}:{seconds % 60:02d}')
        sys.exit(1)
    print('Timing audit PASS: final runtime main script stays inside the 22-24 minute rehearsal envelope for a 25-minute talk')
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
