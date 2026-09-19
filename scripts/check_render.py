#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = 'rebuild-2026-09-17/delegates-rebuild-deck.html'
TARGET = ROOT / TARGET_REL
ARTIFACTS = ROOT / 'render-artifacts'

raw = TARGET.read_text(encoding='utf-8')
keys = re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*(?:data-note-key|data-note)="([^"]+)"', raw)
if len(keys) < 21 or len(keys) != len(set(keys)):
    raise SystemExit('Render check FAILED: invalid slide key set')

browser = next((name for name in [
    'google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'
] if shutil.which(name)), None)
if browser is None:
    raise SystemExit('Render check FAILED: Chrome/Chromium was not found')

if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']

class ActiveSlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.active: list[str] = []
        self.slide_count = 0
        self.notes_has_text = False
        self._in_notes = False

    def handle_starttag(self, tag: str, attrs) -> None:
        attr = dict(attrs)
        if tag == 'section' and 'slide' in attr.get('class', '').split():
            self.slide_count += 1
            if 'active' in attr.get('class', '').split():
                self.active.append(attr.get('data-note', attr.get('data-note-key', '')))
        if tag == 'aside' and attr.get('id') == 'notes':
            self._in_notes = True

    def handle_endtag(self, tag: str) -> None:
        if tag == 'aside' and self._in_notes:
            self._in_notes = False

    def handle_data(self, data: str) -> None:
        if self._in_notes and data.strip():
            self.notes_has_text = True


def dump_dom(url: str) -> str:
    result = subprocess.run(
        common + ['--window-size=1366,768', '--dump-dom', url],
        capture_output=True,
        text=True,
        timeout=35,
    )
    if result.returncode != 0:
        raise RuntimeError(f'browser exit={result.returncode}: {result.stderr[-300:]}')
    return result.stdout


def screenshot(url: str, output: Path, width: int, height: int) -> None:
    result = subprocess.run(
        common + [f'--window-size={width},{height}', '--hide-scrollbars', f'--screenshot={output}', url],
        capture_output=True,
        text=True,
        timeout=35,
    )
    if result.returncode != 0 or not output.exists() or output.stat().st_size < 1024:
        raise RuntimeError(f'screenshot failed: {result.stderr[-300:]}')

server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', '8878', '--bind', '127.0.0.1'],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

try:
    time.sleep(.6)
    base = f'http://127.0.0.1:8878/{TARGET_REL}'
    for index, key in enumerate(keys, 1):
        url = f'{base}#{index}'
        dom = dump_dom(url)
        parser = ActiveSlideParser()
        parser.feed(dom)
        if parser.slide_count != len(keys):
            raise RuntimeError(f'#{index}: slide count {parser.slide_count}!={len(keys)}')
        if parser.active != [key]:
            raise RuntimeError(f'#{index}: active slide mismatch {parser.active!r}!={[key]!r}')
        if not parser.notes_has_text:
            raise RuntimeError(f'#{index}: notes panel was not synchronized')
        screenshot(url, ARTIFACTS / f'1366x768-{index:02d}-{key}.png', 1366, 768)

    sample_indexes = sorted({1, 2, len(keys)//2 + 1, len(keys)})
    for width, height in [(1280, 720), (1920, 1080)]:
        for index in sample_indexes:
            key = keys[index - 1]
            screenshot(
                f'{base}#{index}',
                ARTIFACTS / f'{width}x{height}-{index:02d}-{key}.png',
                width,
                height,
            )

    expected = len(keys) + 2 * len(sample_indexes)
    actual = len(list(ARTIFACTS.glob('*.png')))
    if actual != expected:
        raise RuntimeError(f'screenshot coverage {actual}!={expected}')
    print(f'Render check PASS: {len(keys)} slides; active-slide/notes sync for every slide; {actual} screenshots across 3 geometries')
except Exception as exc:
    print(f'Render check FAILED: {exc}')
    sys.exit(1)
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
