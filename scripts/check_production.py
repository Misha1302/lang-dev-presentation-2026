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
if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()
PRODUCTION = 'https://misha1302.github.io/lang-dev-presentation-2026/'
sha = os.environ.get('GITHUB_SHA', 'unknown')
contract = json.loads((ROOT / 'CONTENT_NARRATIVE_CONTRACT.json').read_text(encoding='utf-8'))
index = (ROOT / 'index.html').read_text(encoding='utf-8')
load_order = re.findall(r'<script\s+src="([^"]+)"', index)
DECK_FRAGMENT_ASSETS = ['deck-main.js', 'deck-research-update.js', 'deck-appendix.js']
DECK_RUNTIME_PATCHES = ['deck-non-destructive-patches.js']
expected_deck_load_order = DECK_FRAGMENT_ASSETS + DECK_RUNTIME_PATCHES
deck_assets = [name for name in load_order if name.startswith('deck-') and name != 'deck.js']
if deck_assets != expected_deck_load_order:
    raise RuntimeError(f'unexpected production deck load order: {deck_assets}')
RESEARCH_KEYS = [f'r{i}' for i in range(1, 8)]
RESEARCH_EDGES = [
    ('r1', 'm3'),
    ('r2', 'r1'),
    ('r3', 'r2'),
    ('r4', 'r3'),
    ('r5', 'r4'),
    ('r6', 'm12'),
    ('r7', 'm25'),
]


def fragment_text(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    match = re.search(r'String\.raw`(.*?)`\);', raw, re.S)
    if not match:
        raise RuntimeError(f'cannot parse {path.name}')
    return match.group(1)


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


def apply_runtime_research_order(slides: list[dict[str, str]]) -> list[dict[str, str]]:
    main = [slide for slide in slides if slide.get('data-kind') == 'main']
    appendix = [slide for slide in slides if slide.get('data-kind') == 'appendix']
    by_key = {slide.get('data-note-key', ''): slide for slide in main}
    if not all(key in by_key for key in RESEARCH_KEYS):
        return slides
    main = [slide for slide in main if slide.get('data-note-key') not in RESEARCH_KEYS]
    for child, anchor in RESEARCH_EDGES:
        anchor_index = next(i for i, slide in enumerate(main) if slide.get('data-note-key') == anchor)
        main.insert(anchor_index + 1, by_key[child])
    return main + appendix


def validate_semantic_owners(slides: list[dict[str, str]]) -> list[str]:
    note_keys = [slide.get('data-note-key', '').strip() for slide in slides]
    if not all(note_keys) or len(note_keys) != len(set(note_keys)):
        raise RuntimeError('production DOM slide identity is missing or duplicated')
    by_key = {slide['data-note-key']: slide for slide in slides}
    main_keys = [slide['data-note-key'] for slide in slides if slide.get('data-kind') == 'main']
    main_position = {key: idx for idx, key in enumerate(main_keys)}
    milestones = contract['milestones']
    for milestone_id, spec in milestones.items():
        owner = spec['owner']
        if owner not in by_key:
            raise RuntimeError(f'production semantic owner missing: {milestone_id}:{owner}')
        if by_key[owner].get('data-kind') != spec['kind']:
            raise RuntimeError(f'production semantic owner kind mismatch: {milestone_id}')
    for before, after in contract['causal_edges']:
        a = milestones[before]
        b = milestones[after]
        if a['kind'] == b['kind'] == 'main' and main_position[a['owner']] > main_position[b['owner']]:
            raise RuntimeError(f'production causal order violated: {before}>{after}')
    return note_keys


# Only authored String.raw fragments own slide identity. Runtime patch scripts may
# mutate presentation copy/markup but are deliberately not reparsed as fragments.
local_slides = parse_slide_meta('\n'.join(fragment_text(ROOT / name) for name in DECK_FRAGMENT_ASSETS))
local_slides = apply_runtime_research_order(local_slides)
local_note_keys = validate_semantic_owners(local_slides)
main_keys = [slide['data-note-key'] for slide in local_slides if slide.get('data-kind') == 'main']
appendix_keys = [slide['data-note-key'] for slide in local_slides if slide.get('data-kind') == 'appendix']
note_target = {key: f'#{i + 1}' for i, key in enumerate(main_keys)}
note_target.update({key: f'#a{i + 1}' for i, key in enumerate(appendix_keys)})

browser = next((name for name in ['google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium'] if shutil.which(name)), None)
if browser is None:
    print('Production check FAILED: Chrome/Chromium was not found')
    sys.exit(1)

assets = [
    'index.html',
    'CONTENT_NARRATIVE_CONTRACT.json',
    'deck-main.js',
    'deck-research-update.js',
    'deck-appendix.js',
    'deck-non-destructive-patches.js',
    contract['speaker_owner'],
    'speaker-script-research-update.js',
    'speaker-script-conference-overrides.js',
    'deck.js',
    'presenter-cues.js',
    'presenter.css',
    'presenter-cues.css',
    'speaker-script.css',
    'foundation.css',
    'styles.css',
    'visual-balance.css',
    'conference-polish.css',
]
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
    if f'data-deck-qa-contract="{contract["runtime_qa_contract"]}"' not in nav.stdout:
        failures.append('production DOM runtime QA contract marker mismatch')
    try:
        deployed_note_keys = validate_semantic_owners(parse_slide_meta(nav.stdout))
        if deployed_note_keys != local_note_keys:
            failures.append('production semantic slide identity/order differs from local candidate')
    except Exception as exc:
        failures.append(f'production semantic contract: {exc}')

milestone_owner_keys = []
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
presenter_representative = []
for milestone_id in presenter_ids:
    owner = contract['milestones'][milestone_id]['owner']
    target = note_target[owner]
    if target not in presenter_representative:
        presenter_representative.append(target)
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
    if f'data-canonical-owner="{contract["speaker_owner"]}"' not in result.stdout:
        failures.append(f'production presenter {target}: canonical owner marker missing')

if failures:
    print('Production check FAILED:')
    for failure in failures:
        print(' - ' + failure)
    sys.exit(1)
print(
    'Production check OK: exact asset hashes including additive research and conference runtime overlays match Pages; '
    f'{len(main_keys)} main + {len(appendix_keys)} appendix; semantic owner/order, navigation, audience and presenter states PASS'
)
