#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'production-artifacts'
PRODUCTION = 'https://misha1302.github.io/lang-dev-presentation-2026/'
PORT = '8880'
sha = os.environ.get('GITHUB_SHA', 'unknown')
contract = json.loads((ROOT / 'CONTENT_NARRATIVE_CONTRACT.json').read_text(encoding='utf-8'))
index = (ROOT / 'index.html').read_text(encoding='utf-8')

if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


script_assets = re.findall(r'<script\s+src="([^"]+)"', index)
style_assets = re.findall(r'<link\b[^>]*\bhref="([^"]+)"', index)
# presenter.css is injected dynamically by deck.js, so it is part of production
# even though it is intentionally absent from index.html.
assets = unique([
    'index.html',
    'CONTENT_NARRATIVE_CONTRACT.json',
    *style_assets,
    *script_assets,
    'presenter.css',
])
missing_assets = [name for name in assets if not (ROOT / name).is_file()]
if missing_assets:
    raise RuntimeError(f'local production assets missing: {missing_assets}')

browser = next((name for name in [
    'google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'
] if shutil.which(name)), None)
if browser is None:
    print('Production check FAILED: Chrome/Chromium was not found')
    sys.exit(1)
common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']


class SlideMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != 'section':
            return
        attr = dict(attrs)
        if 'slide' in attr.get('class', '').split():
            self.slides.append(attr)


def parse_slide_meta(raw: str) -> list[dict[str, str]]:
    parser = SlideMetaParser()
    parser.feed(raw)
    return parser.slides


def normalized_kind(slide: dict[str, str]) -> str:
    return 'appendix' if slide.get('data-kind') == 'appendix' else 'main'


def validate_semantic_owners(slides: list[dict[str, str]]) -> tuple[list[str], list[str], list[str]]:
    note_keys = [slide.get('data-note-key', '').strip() for slide in slides]
    if not note_keys or not all(note_keys) or len(note_keys) != len(set(note_keys)):
        raise RuntimeError('runtime slide identity is missing or duplicated')
    by_key = {slide['data-note-key']: slide for slide in slides}
    main_keys = [slide['data-note-key'] for slide in slides if normalized_kind(slide) == 'main']
    appendix_keys = [slide['data-note-key'] for slide in slides if normalized_kind(slide) == 'appendix']
    main_position = {key: idx for idx, key in enumerate(main_keys)}
    milestones = contract['milestones']
    for milestone_id, spec in milestones.items():
        owner = spec['owner']
        if owner not in by_key:
            raise RuntimeError(f'semantic owner missing: {milestone_id}:{owner}')
        if normalized_kind(by_key[owner]) != spec['kind']:
            raise RuntimeError(f'semantic owner kind mismatch: {milestone_id}')
    for before, after in contract['causal_edges']:
        a = milestones[before]
        b = milestones[after]
        if a['kind'] == b['kind'] == 'main' and main_position[a['owner']] > main_position[b['owner']]:
            raise RuntimeError(f'causal order violated: {before}>{after}')
    return note_keys, main_keys, appendix_keys


def dataset_value(dom: str, name: str) -> str | None:
    match = re.search(rf'\bdata-{re.escape(name)}="([^"]*)"', dom)
    return None if match is None else match.group(1)


def run_dom(url: str, width: int = 1366, height: int = 768, timeout: int = 45) -> subprocess.CompletedProcess[str] | None:
    result: subprocess.CompletedProcess[str] | None = None
    for attempt in range(2):
        try:
            result = subprocess.run(
                common + [f'--window-size={width},{height}', '--dump-dom', url],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            if attempt == 0:
                time.sleep(.5)
                continue
            return None
        if result.returncode == 0:
            return result
        if attempt == 0:
            time.sleep(.5)
    return result


def require_runtime_dom(result: subprocess.CompletedProcess[str] | None, label: str) -> tuple[list[str], list[str], list[str]]:
    if result is None:
        raise RuntimeError(f'{label}: browser timeout')
    if result.returncode != 0:
        raise RuntimeError(f'{label}: browser exit {result.returncode}: {result.stderr[-400:]}')
    if 'data-nav-check="ok"' not in result.stdout:
        raise RuntimeError(f'{label}: navigation QA did not pass: {dataset_value(result.stdout, "nav-errors") or "no detail"}')
    expected_qa = contract['runtime_qa_contract']
    if f'data-deck-qa-contract="{expected_qa}"' not in result.stdout:
        raise RuntimeError(f'{label}: runtime QA contract marker mismatch')
    note_keys, main_keys, appendix_keys = validate_semantic_owners(parse_slide_meta(result.stdout))
    declared_main = dataset_value(result.stdout, 'runtime-main-count')
    declared_appendix = dataset_value(result.stdout, 'runtime-appendix-count')
    missing_speech = dataset_value(result.stdout, 'runtime-speech-missing')
    if declared_main is not None and int(declared_main) != len(main_keys):
        raise RuntimeError(f'{label}: runtime main count mismatch {declared_main}!={len(main_keys)}')
    if declared_appendix is not None and int(declared_appendix) != len(appendix_keys):
        raise RuntimeError(f'{label}: runtime appendix count mismatch {declared_appendix}!={len(appendix_keys)}')
    if missing_speech:
        raise RuntimeError(f'{label}: missing canonical speech for {missing_speech}')
    return note_keys, main_keys, appendix_keys


def visual_failure(prefix: str, result: subprocess.CompletedProcess[str] | None) -> str:
    if result is None:
        return f'{prefix}: browser timeout after retry'
    if result.returncode != 0:
        stderr = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'no stderr'
        return f'{prefix}: browser exit {result.returncode}: {stderr}'
    status = dataset_value(result.stdout, 'visual-check')
    detail = dataset_value(result.stdout, 'visual-errors')
    if status is None:
        return f'{prefix}: visual status missing'
    return f'{prefix}: visual-check failed: {detail or "no data-visual-errors"}'


server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', PORT, '--bind', '127.0.0.1'],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

try:
    time.sleep(.8)
    local_nav = run_dom(f'http://127.0.0.1:{PORT}/?nav-check=1#1')
    local_note_keys, main_keys, appendix_keys = require_runtime_dom(local_nav, 'local runtime')
    note_target = {key: f'#{i + 1}' for i, key in enumerate(main_keys)}
    note_target.update({key: f'#a{i + 1}' for i, key in enumerate(appendix_keys)})

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
        print(f'Production check FAILED: Pages did not reach exact final assets: {last}')
        sys.exit(1)

    failures: list[str] = []
    deployed_nav = run_dom(f'{PRODUCTION}?nav-check=1&qa={quote(sha)}#1')
    try:
        deployed_note_keys, deployed_main, deployed_appendix = require_runtime_dom(deployed_nav, 'production runtime')
        if deployed_note_keys != local_note_keys:
            failures.append('production final DOM slide identity/order differs from local candidate')
        if deployed_main != main_keys or deployed_appendix != appendix_keys:
            failures.append('production main/appendix runtime partition differs from local candidate')
    except Exception as exc:
        failures.append(str(exc))

    milestone_owner_keys: list[str] = []
    for milestone_id in contract['milestones']:
        key = contract['milestones'][milestone_id]['owner']
        if key not in milestone_owner_keys:
            milestone_owner_keys.append(key)
    representative = [note_target[key] for key in milestone_owner_keys if key in note_target]
    for key in [main_keys[0], main_keys[-1], appendix_keys[0], appendix_keys[-1]]:
        target = note_target[key]
        if target not in representative:
            representative.append(target)

    for target in representative:
        result = run_dom(f'{PRODUCTION}?visual-check=1&qa={quote(sha)}{target}')
        if result is None or result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
            failures.append(visual_failure(f'production {target}', result))
            continue
        output = ARTIFACTS / f'1366x768-{target[1:]}.png'
        try:
            shot = subprocess.run(
                common + ['--window-size=1366,768', '--hide-scrollbars', f'--screenshot={output}', f'{PRODUCTION}?qa={quote(sha)}{target}'],
                capture_output=True,
                text=True,
                timeout=35,
            )
        except subprocess.TimeoutExpired:
            failures.append(f'production screenshot {target}: timeout')
            continue
        if shot.returncode != 0 or not output.exists():
            failures.append(f'production screenshot {target}: failed')

    # Presenter-state validation follows the active causal contract instead of
    # hard-coding legacy milestone identifiers from an older narrative order.
    presenter_representative: list[str] = []
    for spec in contract['milestones'].values():
        owner = spec['owner']
        if owner in note_target:
            target = note_target[owner]
            if target not in presenter_representative:
                presenter_representative.append(target)
    for target in presenter_representative:
        result = run_dom(f'{PRODUCTION}?presenter=1&visual-check=1&qa={quote(sha)}{target}')
        if result is None or result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
            failures.append(visual_failure(f'production presenter {target}', result))
            continue
        if f'data-canonical-owner="{contract["speaker_owner"]}"' not in result.stdout:
            failures.append(f'production presenter {target}: canonical owner marker missing')

    if failures:
        print('Production check FAILED:')
        for failure in failures:
            print(' - ' + failure)
        sys.exit(1)

    print(
        'Production check OK: exact runtime asset hashes match Pages; '
        f'{len(main_keys)} main + {len(appendix_keys)} appendix; '
        'final DOM identity/order, navigation, audience and presenter states PASS'
    )
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
