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
ARTIFACTS = ROOT / 'render-artifacts'
PORT = '8878'

if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

index = (ROOT / 'index.html').read_text(encoding='utf-8')
load_order = re.findall(r'<script\s+src="([^"]+)"', index)
for required in ['deck-narrative-reframe.js', 'deck.js']:
    if required not in load_order:
        print(f'Render check FAILED: {required} is not loaded by index.html')
        sys.exit(1)

browser = next((name for name in ['google-chrome-stable','google-chrome','chromium-browser','chromium'] if shutil.which(name)), None)
if browser is None:
    print('Render check FAILED: Chrome/Chromium was not found')
    sys.exit(1)

common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']

server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', PORT, '--bind', '127.0.0.1'],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

class SlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[tuple[str, str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != 'section':
            return
        data = {k: v or '' for k, v in attrs}
        classes = data.get('class', '').split()
        if 'slide' not in classes:
            return
        self.slides.append((data.get('data-note-key', ''), data.get('data-kind', 'main'), 'active' in classes))

def run_browser(width: int, height: int, url: str, *, timeout: int = 35) -> subprocess.CompletedProcess[str]:
    return subprocess.run(common + [f'--window-size={width},{height}', '--dump-dom', url], capture_output=True, text=True, timeout=timeout)

def parse_slides(html: str) -> list[tuple[str, str, bool]]:
    parser = SlideParser()
    parser.feed(html)
    return parser.slides

def discover_runtime_targets() -> tuple[list[str], list[str], str | None]:
    result = run_browser(1366, 768, f'http://127.0.0.1:{PORT}/?visual-check=1#1', timeout=45)
    if result.returncode != 0:
        raise RuntimeError(f'browser discovery exit {result.returncode}: {result.stderr[:500]}')
    slides = parse_slides(result.stdout)
    if not slides:
        raise RuntimeError('no runtime slides found in browser DOM')
    main = [key for key, kind, _ in slides if kind != 'appendix']
    appendix = [key for key, kind, _ in slides if kind == 'appendix']
    if len(main) != len(set(main)):
        raise RuntimeError('duplicate runtime main slide keys')
    if len(appendix) != len(set(appendix)):
        raise RuntimeError('duplicate runtime appendix slide keys')
    marker = None
    token = 'data-final-narrative="'
    start = result.stdout.find(token)
    if start >= 0:
        start += len(token)
        marker = result.stdout[start:result.stdout.find('"', start)]
    return main, appendix, marker

def visible_key_for(target: str) -> str | None:
    if target.startswith('#a'):
        idx = int(target[2:]) - 1
        return appendix_keys[idx] if 0 <= idx < len(appendix_keys) else None
    idx = int(target[1:]) - 1
    return main_keys[idx] if 0 <= idx < len(main_keys) else None

def inspect(width: int, height: int, target: str, presenter: bool = False) -> str | None:
    mode = 'presenter=1&' if presenter else ''
    url = f'http://127.0.0.1:{PORT}/?{mode}visual-check=1{target}'
    result = None
    for attempt in range(2):
        try:
            result = run_browser(width, height, url, timeout=30)
        except subprocess.TimeoutExpired:
            if attempt == 0:
                time.sleep(.5)
                continue
            return 'browser timeout after retry'
        if result.returncode != 0:
            if attempt == 0:
                time.sleep(.5)
                continue
            return f'browser exit {result.returncode} after retry'
        break
    assert result is not None
    expected = visible_key_for(target)
    active = [key for key, _, is_active in parse_slides(result.stdout) if is_active]
    if active != [expected]:
        return f'active slide mismatch: expected {expected}, got {active}'
    if 'data-visual-check="ok"' in result.stdout:
        return None
    marker = 'data-visual-errors="'
    start = result.stdout.find(marker)
    if start < 0:
        return 'visual status missing'
    start += len(marker)
    return result.stdout[start:result.stdout.find('"', start)]

try:
    time.sleep(.8)
    try:
        main_keys, appendix_keys, final_marker = discover_runtime_targets()
    except Exception as exc:
        print(f'Render check FAILED: runtime discovery failed: {exc}')
        sys.exit(1)

    targets = [f'#{i}' for i in range(1, len(main_keys) + 1)] + [f'#a{i}' for i in range(1, len(appendix_keys) + 1)]
    audience_geometry = [(1920, 1080), (1536, 864), (1366, 768), (1280, 720)]
    audience_screenshots = [(1920, 1080), (1366, 768), (1280, 720)]
    presenter_geometry = [(1920, 1080), (1366, 768), (1280, 720)]
    presenter_screenshot = (1366, 768)

    failures: list[str] = []
    for width, height in audience_geometry:
        for target in targets:
            if detail := inspect(width, height, target):
                failures.append(f'audience {width}x{height} {target}: {detail}')
    for width, height in presenter_geometry:
        for target in targets:
            if detail := inspect(width, height, target, True):
                failures.append(f'presenter {width}x{height} {target}: {detail}')

    try:
        nav = run_browser(1366, 768, f'http://127.0.0.1:{PORT}/?nav-check=1#1', timeout=45)
    except subprocess.TimeoutExpired:
        failures.append('navigation: browser timeout')
    else:
        if nav.returncode != 0 or 'data-nav-check="ok"' not in nav.stdout:
            marker = 'data-nav-errors="'
            start = nav.stdout.find(marker)
            detail = 'navigation status missing'
            if start >= 0:
                start += len(marker)
                detail = nav.stdout[start:nav.stdout.find('"', start)]
            failures.append(f'navigation: {detail}')

    for width, height in audience_screenshots:
        for target in targets:
            output = ARTIFACTS / f'{width}x{height}-{target[1:]}.png'
            url = f'http://127.0.0.1:{PORT}/{target}'
            try:
                shot = subprocess.run(common + [f'--window-size={width},{height}', '--hide-scrollbars', f'--screenshot={output}', url], capture_output=True, text=True, timeout=30)
            except subprocess.TimeoutExpired:
                failures.append(f'screenshot {width}x{height} {target}: timeout')
                continue
            if shot.returncode != 0 or not output.exists():
                failures.append(f'screenshot {width}x{height} {target}: failed')

    width, height = presenter_screenshot
    for target in targets:
        output = ARTIFACTS / f'presenter-{width}x{height}-{target[1:]}.png'
        url = f'http://127.0.0.1:{PORT}/?presenter=1{target}'
        try:
            shot = subprocess.run(common + [f'--window-size={width},{height}', '--hide-scrollbars', f'--screenshot={output}', url], capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            failures.append(f'presenter screenshot {target}: timeout')
            continue
        if shot.returncode != 0 or not output.exists():
            failures.append(f'presenter screenshot {target}: failed')

    expected = len(targets) * (len(audience_screenshots) + 1)
    actual = len(list(ARTIFACTS.glob('*.png')))
    if actual != expected:
        failures.append(f'screenshot coverage: expected {expected}, got {actual}')
    if failures:
        print('Render check FAILED:')
        for failure in failures:
            print(' - ' + failure)
        sys.exit(1)
    geometry = len(targets) * (len(audience_geometry) + len(presenter_geometry))
    marker = f'; final narrative={final_marker}' if final_marker else ''
    print(f'Render check OK: {len(main_keys)} runtime main + {len(appendix_keys)} runtime appendix{marker}; {expected} unique screenshots; {geometry} audience/presenter geometry states; navigation + presenter sync PASS')
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
