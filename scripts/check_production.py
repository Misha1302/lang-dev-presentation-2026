#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib
import os
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'production-artifacts'
PRODUCTION = 'https://misha1302.github.io/lang-dev-presentation-2026/'
TARGET_REL = 'rebuild-2026-09-17/delegates-rebuild-deck.html'
TARGET = ROOT / TARGET_REL
sha = os.environ.get('GITHUB_SHA', 'unknown')

if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

assets = ['index.html', TARGET_REL]
missing = [name for name in assets if not (ROOT / name).is_file()]
if missing:
    raise RuntimeError(f'local production assets missing: {missing}')

raw = TARGET.read_text(encoding='utf-8')
keys = re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*(?:data-note-key|data-note)="([^"]+)"', raw)
if len(keys) < 21 or len(keys) != len(set(keys)):
    raise RuntimeError('invalid local slide identity')

browser = next((name for name in [
    'google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'
] if shutil.which(name)), None)
if browser is None:
    raise RuntimeError('Chrome/Chromium was not found')
common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']

class ActiveSlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.active: list[str] = []
        self.slide_count = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != 'section':
            return
        attr = dict(attrs)
        classes = attr.get('class', '').split()
        if 'slide' not in classes:
            return
        self.slide_count += 1
        if 'active' in classes:
            self.active.append(attr.get('data-note', attr.get('data-note-key', '')))


def dump(url: str) -> str:
    result = subprocess.run(common + ['--window-size=1366,768', '--dump-dom', url], capture_output=True, text=True, timeout=40)
    if result.returncode != 0:
        raise RuntimeError(f'browser exit {result.returncode}: {result.stderr[-300:]}')
    return result.stdout

local_hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in assets}
deadline = time.time() + 360
last = ''
while time.time() < deadline:
    stale: list[str] = []
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
    raise RuntimeError(f'Pages did not reach exact final assets: {last}')

for index, key in enumerate(keys, 1):
    dom = dump(f'{PRODUCTION}{TARGET_REL}?qa={quote(sha)}#{index}')
    parser = ActiveSlideParser()
    parser.feed(dom)
    if parser.slide_count != len(keys) or parser.active != [key]:
        raise RuntimeError(f'production #{index}: identity mismatch count={parser.slide_count} active={parser.active!r}')

sample_indexes = sorted({1, 2, len(keys)//2 + 1, len(keys)})
for index in sample_indexes:
    output = ARTIFACTS / f'production-1366x768-{index:02d}-{keys[index-1]}.png'
    result = subprocess.run(
        common + ['--window-size=1366,768', '--hide-scrollbars', f'--screenshot={output}', f'{PRODUCTION}{TARGET_REL}?qa={quote(sha)}#{index}'],
        capture_output=True,
        text=True,
        timeout=40,
    )
    if result.returncode != 0 or not output.exists() or output.stat().st_size < 1024:
        raise RuntimeError(f'production screenshot #{index} failed')

print(f'Production check PASS: exact index/deck hashes match Pages; {len(keys)} slide identities/navigation states replayed; {len(sample_indexes)} screenshots captured')
