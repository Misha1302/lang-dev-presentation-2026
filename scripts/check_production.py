#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib
import html
import json
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
contract = json.loads((ROOT / 'CONTENT_NARRATIVE_CONTRACT.json').read_text(encoding='utf-8'))
index = (ROOT / 'index.html').read_text(encoding='utf-8')


class IndexAssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attr = dict(attrs)
        if tag == 'script' and attr.get('src'):
            self.assets.append(attr['src'])
        if tag == 'link' and attr.get('rel') == 'stylesheet' and attr.get('href'):
            self.assets.append(attr['href'])


class SlideMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != 'section':
            return
        attr = {k: v or '' for k, v in attrs}
        if 'slide' in attr.get('class', '').split():
            self.slides.append(attr)


def parse_slide_meta(raw: str) -> list[dict[str, str]]:
    parser = SlideMetaParser()
    parser.feed(raw)
    return parser.slides


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def data_attr(dom: str, name: str) -> str | None:
    match = re.search(rf'\bdata-{re.escape(name)}="([^"]*)"', dom)
    if not match:
        return None
    return html.unescape(match.group(1))


asset_parser = IndexAssetParser()
asset_parser.feed(index)
dynamic_assets = ['presenter.css']
assets = unique_preserving_order(
    ['index.html', 'CONTENT_NARRATIVE_CONTRACT.json']
    + asset_parser.assets
    + [name for name in dynamic_assets if (ROOT / name).is_file()]
)
missing_assets = [name for name in assets if not (ROOT / name).is_file()]
if missing_assets:
    raise RuntimeError(f'local production assets missing: {missing_assets}')

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

browser = next((name for name in ['google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'] if shutil.which(name)), None)
if browser is None:
    print('Production check FAILED: Chrome/Chromium was not found')
    sys.exit(1)
common = [browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox', '--no-first-run']


def run_dom(url: str, width: int = 1366, height: int = 768, timeout: int = 35) -> subprocess.CompletedProcess[str] | None:
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


def visual_failure(prefix: str, result: subprocess.CompletedProcess[str] | None) -> str:
    if result is None:
        return f'{prefix}: browser timeout after retry'
    if result.returncode != 0:
        stderr = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'no stderr'
        return f'{prefix}: browser exit {result.returncode}: {stderr}'
    status = data_attr(result.stdout, 'visual-check')
    detail = data_attr(result.stdout, 'visual-errors')
    if status is None:
        return f'{prefix}: visual status missing'
    if status != 'ok':
        return f'{prefix}: visual-check failed: {detail or "no data-visual-errors"}'
    return f'{prefix}: visual-check unexpectedly reported ok'


def runtime_manifest(dom: str) -> tuple[list[str], list[str]]:
    main_keys_raw = data_attr(dom, 'runtime-main-keys')
    appendix_keys_raw = data_attr(dom, 'runtime-appendix-keys')
    missing = data_attr(dom, 'runtime-speech-missing')
    if main_keys_raw is None or appendix_keys_raw is None or missing is None:
        raise RuntimeError('runtime manifest attributes missing')
    if missing:
        raise RuntimeError(f'missing canonical speech for runtime keys: {missing}')
    main = [key for key in main_keys_raw.split(',') if key]
    appendix = [key for key in appendix_keys_raw.split(',') if key]
    if len(main) != len(set(main)) or len(appendix) != len(set(appendix)):
        raise RuntimeError('runtime slide keys are not unique')
    if len(main) < 1 or len(appendix) < 1:
        raise RuntimeError(f'invalid runtime counts: {len(main)} main + {len(appendix)} appendix')
    return main, appendix


def validate_semantic_owners(slides: list[dict[str, str]]) -> None:
    note_keys = [slide.get('data-note-key', '').strip() for slide in slides]
    if not all(note_keys) or len(note_keys) != len(set(note_keys)):
        raise RuntimeError('production DOM slide identity is missing or duplicated')
    by_key = {slide['data-note-key']: slide for slide in slides}
    main_keys = [slide['data-note-key'] for slide in slides if slide.get('data-kind') != 'appendix']
    main_position = {key: idx for idx, key in enumerate(main_keys)}
    milestones = contract['milestones']
    for milestone_id, spec in milestones.items():
        owner = spec['owner']
        if owner not in by_key:
            raise RuntimeError(f'production semantic owner missing: {milestone_id}:{owner}')
        expected_kind = spec['kind']
        actual_kind = 'appendix' if by_key[owner].get('data-kind') == 'appendix' else 'main'
        if actual_kind != expected_kind:
            raise RuntimeError(f'production semantic owner kind mismatch: {milestone_id}')
    for before, after in contract['causal_edges']:
        a = milestones[before]
        b = milestones[after]
        if a['kind'] == b['kind'] == 'main' and main_position[a['owner']] > main_position[b['owner']]:
            raise RuntimeError(f'production causal order violated: {before}>{after}')


failures: list[str] = []
nav_url = f'{PRODUCTION}?nav-check=1&qa={quote(sha)}#1'
nav = run_dom(nav_url)
if nav is None:
    failures.append('production navigation: browser timeout after retry')
elif nav.returncode != 0 or 'data-nav-check="ok"' not in nav.stdout:
    detail = data_attr(nav.stdout, 'nav-errors') if nav.returncode == 0 else nav.stderr.strip()
    failures.append(f'production navigation: nav-check did not pass: {detail or "no detail"}')
else:
    expected_contract = contract['runtime_qa_contract']
    if f'data-deck-qa-contract="{expected_contract}"' not in nav.stdout:
        failures.append('production DOM runtime QA contract marker mismatch')
    try:
        main_keys, appendix_keys = runtime_manifest(nav.stdout)
        validate_semantic_owners(parse_slide_meta(nav.stdout))
    except Exception as exc:
        failures.append(f'production semantic/runtime contract: {exc}')
        main_keys, appendix_keys = [], []

if not failures:
    note_target = {key: f'#{i + 1}' for i, key in enumerate(main_keys)}
    note_target.update({key: f'#a{i + 1}' for i, key in enumerate(appendix_keys)})

    milestone_owner_keys: list[str] = []
    for milestone_id in contract['milestones']:
        key = contract['milestones'][milestone_id]['owner']
        if key in note_target and key not in milestone_owner_keys:
            milestone_owner_keys.append(key)
    representative = [note_target[key] for key in milestone_owner_keys]
    for key in [main_keys[0], main_keys[-1], appendix_keys[0], appendix_keys[-1]]:
        target = note_target[key]
        if target not in representative:
            representative.append(target)

    for target in representative:
        url = f'{PRODUCTION}?visual-check=1&qa={quote(sha)}{target}'
        result = run_dom(url)
        if result is None or result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
            failures.append(visual_failure(f'production {target}', result))
            continue
        output = ARTIFACTS / f'1366x768-{target[1:]}.png'
        shot_url = f'{PRODUCTION}?qa={quote(sha)}{target}'
        try:
            shot = subprocess.run(
                common + ['--window-size=1366,768', '--hide-scrollbars', f'--screenshot={output}', shot_url],
                capture_output=True,
                text=True,
                timeout=35,
            )
        except subprocess.TimeoutExpired:
            failures.append(f'production screenshot {target}: timeout')
            continue
        if shot.returncode != 0 or not output.exists():
            failures.append(f'production screenshot {target}: failed')

    presenter_ids = [
        'monolith-baseline',
        'independent-authorship',
        'what-how',
        'feasibility-before-preference',
        'local-deabstraction',
        'safeindex',
        'semantic-producer-independence',
        'validity',
        'obligation',
        'cross-representation-correspondence',
        'strongest-alternative',
        'author-resolve-optimize-conclusion',
    ]
    presenter_representative: list[str] = []
    for milestone_id in presenter_ids:
        owner = contract['milestones'][milestone_id]['owner']
        if owner in note_target:
            target = note_target[owner]
            if target not in presenter_representative:
                presenter_representative.append(target)

    for target in presenter_representative:
        url = f'{PRODUCTION}?presenter=1&visual-check=1&qa={quote(sha)}{target}'
        result = run_dom(url)
        if result is None or result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
            failures.append(visual_failure(f'production presenter {target}', result))
            continue
        expected_owner = contract['speaker_owner']
        if f'data-canonical-owner="{expected_owner}"' not in result.stdout:
            failures.append(f'production presenter {target}: canonical owner marker missing')

if failures:
    print('Production check FAILED:')
    for failure in failures:
        print(' - ' + failure)
    sys.exit(1)

print(
    'Production check OK: exact asset hashes from index and dynamic presenter CSS match Pages; '
    f'{len(main_keys)} runtime main + {len(appendix_keys)} runtime appendix; '
    'semantic owner/order, navigation, audience and presenter states PASS'
)
