#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'production-artifacts'
if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()
PRODUCTION = 'https://misha1302.github.io/lang-dev-presentation-2026/'
sha = os.environ.get('GITHUB_SHA', 'unknown')
index = (ROOT / 'index.html').read_text(encoding='utf-8')
load_order = re.findall(r'<script\s+src="([^"]+)"', index)
deck_assets = [name for name in load_order if name.startswith('deck-') and name != 'deck.js']
raw = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in deck_assets)
main_count = len(re.findall(r'data-kind="main"', raw))
appendix_count = len(re.findall(r'data-kind="appendix"', raw))
if (main_count, appendix_count) != (40, 8):
    print('Production check FAILED: local deck count contract mismatch')
    sys.exit(1)

browser = next((name for name in ['google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium'] if shutil.which(name)), None)
if browser is None:
    print('Production check FAILED: Chrome/Chromium was not found')
    sys.exit(1)

assets = [
    'index.html',
    'deck-main.js',
    'deck-appendix.js',
    'speaker-script-canonical.js',
    'deck.js',
    'presenter.css',
    'speaker-script.css',
    'foundation.css',
    'styles.css',
    'visual-balance.css',
]
local_hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in assets}
deadline = time.time() + 360
last = ''
while time.time() < deadline:
    stale = []
    for name, expected in local_hashes.items():
        try:
            body = urlopen(f'{PRODUCTION}{name}?qa={quote(sha)}', timeout=15).read()
            actual = hashlib.sha256(body).hexdigest()
            if actual != expected:
                stale.append(f'{name}:{actual[:12]}!=local:{expected[:12]}')
        except Exception as exc:
            stale.append(f'{name}:{exc}')
    if not stale:
        break
    last = '; '.join(stale)
    time.sleep(5)
else:
    print(f'Production check FAILED: Pages did not reach exact final assets: {last}')
    sys.exit(1)

common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']
failures: list[str] = []
nav_url = f'{PRODUCTION}?nav-check=1&qa={quote(sha)}#1'
try:
    nav = subprocess.run(common + ['--window-size=1366,768', '--dump-dom', nav_url], capture_output=True, text=True, timeout=35)
except subprocess.TimeoutExpired:
    failures.append('production navigation: browser timeout')
    nav = None
if nav:
    if nav.returncode != 0 or 'data-nav-check="ok"' not in nav.stdout:
        failures.append('production navigation: nav-check did not pass')
    for marker in [
        'Extensibility is an authoring-time property',
        'Peephole optimization looks at a small window',
        'Local rewrites are easy. Global optimization needs shared facts.',
        'A bounds check is a non-local proof problem',
        'Stable typed semantic queries decouple producers from consumers',
        'Global optimization makes semantic preservation a lowering problem',
        'Extensibility does not have to cost runtime performance.'
    ]:
        if marker not in nav.stdout:
            failures.append(f'production narrative marker missing: {marker}')
    if 'data-deck-qa-contract="architecture-story-v2"' not in nav.stdout:
        failures.append('production DOM contract marker mismatch')

representative = ['#1', '#2', '#7', '#10', '#13', '#17', '#18', '#20', '#21', '#24', '#26', '#29', '#32', '#34', '#38', '#39', '#40', '#a3', '#a5', '#a8']
for target in representative:
    url = f'{PRODUCTION}?visual-check=1&qa={quote(sha)}{target}'
    try:
        result = subprocess.run(common + ['--window-size=1366,768', '--dump-dom', url], capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        failures.append(f'production {target}: browser timeout')
        continue
    if result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
        failures.append(f'production {target}: visual-check failed')
        continue
    output = ARTIFACTS / f'1366x768-{target[1:]}.png'
    shot_url = f'{PRODUCTION}?qa={quote(sha)}{target}'
    try:
        shot = subprocess.run(common + ['--window-size=1366,768', '--hide-scrollbars', f'--screenshot={output}', shot_url], capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        failures.append(f'production screenshot {target}: timeout')
        continue
    if shot.returncode != 0 or not output.exists():
        failures.append(f'production screenshot {target}: failed')

presenter_representative = ['#1', '#13', '#17', '#20', '#21', '#26', '#32', '#38', '#40', '#a8']
for target in presenter_representative:
    url = f'{PRODUCTION}?presenter=1&visual-check=1&qa={quote(sha)}{target}'
    try:
        result = subprocess.run(common + ['--window-size=1366,768', '--dump-dom', url], capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        failures.append(f'production presenter {target}: browser timeout')
        continue
    if result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
        failures.append(f'production presenter {target}: visual/canonical-script check failed')
        continue
    if 'data-canonical-owner="speaker-script-canonical.js"' not in result.stdout:
        failures.append(f'production presenter {target}: canonical owner marker missing')

if failures:
    print('Production check FAILED:')
    for failure in failures:
        print(' - ' + failure)
    sys.exit(1)
print(f'Production check OK: exact asset hashes including canonical speaker script match Pages; {main_count} main + {appendix_count} appendix; navigation, audience and presenter states PASS')
