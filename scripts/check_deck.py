#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / 'CONTENT_NARRATIVE_CONTRACT.json'
REQUIRED_MILESTONE_IDS = {
    'monolith-baseline',
    'extensibility-motivation',
    'capability-profile-distinction',
    'independent-authorship',
    'what-how',
    'feasibility-before-preference',
    'resolved-plan-freeze',
    'local-deabstraction',
    'local-nonlocal-bridge',
    'safeindex',
    'semantic-producer-independence',
    'modularity-vs-soundness',
    'second-semantic-domain',
    'validity',
    'obligation',
    'cross-representation-correspondence',
    'prior-art',
    'strongest-alternative',
    'falsification',
    'author-resolve-optimize-conclusion',
}


def fragment_text(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    match = re.search(r'String\.raw`(.*)`\);\s*$', raw, re.S)
    assert match, f'cannot parse {path.name}'
    return match.group(1)


class SlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != 'section':
            return
        attr = dict(attrs)
        if 'slide' in attr.get('class', '').split():
            self.slides.append(attr)


def parse_slides(deck_assets: list[str]) -> list[dict[str, str]]:
    parser = SlideParser()
    parser.feed('\n'.join(fragment_text(ROOT / name) for name in deck_assets))
    return parser.slides


def validate_contract(contract: dict, slides: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    assert contract.get('schema_version') == 1, 'unsupported narrative contract schema'
    assert isinstance(contract.get('contract_id'), str) and contract['contract_id'], 'missing contract id'
    milestones = contract.get('milestones')
    assert isinstance(milestones, dict), 'milestones must be an object'
    missing = REQUIRED_MILESTONE_IDS - set(milestones)
    assert not missing, f'missing required semantic milestone ids: {sorted(missing)}'

    note_keys = [slide.get('data-note-key', '').strip() for slide in slides]
    assert all(note_keys), 'every slide must have data-note-key'
    assert len(note_keys) == len(set(note_keys)), 'duplicate slide note key'
    by_key = {slide['data-note-key']: slide for slide in slides}
    main_keys = [slide['data-note-key'] for slide in slides if slide.get('data-kind') == 'main']
    appendix_keys = [slide['data-note-key'] for slide in slides if slide.get('data-kind') == 'appendix']
    assert main_keys, 'deck must contain at least one main slide'
    assert appendix_keys, 'deck must contain at least one appendix slide'

    allowed = set(contract.get('allowed_evidence_categories', []))
    required_categories = set(contract.get('required_evidence_categories', []))
    assert allowed, 'allowed evidence categories must be declared'
    seen_categories: set[str] = set()
    owner_index: dict[str, int] = {}
    main_position = {key: idx for idx, key in enumerate(main_keys)}

    for milestone_id, spec in milestones.items():
        assert isinstance(spec, dict), f'{milestone_id}: milestone spec must be an object'
        owner = spec.get('owner')
        kind = spec.get('kind')
        category = spec.get('evidence_category')
        assert owner in by_key, f'{milestone_id}: owner {owner!r} does not exist'
        assert kind in {'main', 'appendix'}, f'{milestone_id}: invalid owner kind {kind!r}'
        assert by_key[owner].get('data-kind') == kind, f'{milestone_id}: owner kind mismatch'
        assert category in allowed, f'{milestone_id}: invalid evidence category {category!r}'
        seen_categories.add(category)
        if kind == 'main':
            owner_index[milestone_id] = main_position[owner]

    assert required_categories <= seen_categories, (
        'missing required evidence categories: '
        + ', '.join(sorted(required_categories - seen_categories))
    )

    edges = contract.get('causal_edges')
    assert isinstance(edges, list) and edges, 'causal_edges must be a non-empty list'
    graph: dict[str, list[str]] = defaultdict(list)
    indegree = {milestone_id: 0 for milestone_id in milestones}
    seen_edges: set[tuple[str, str]] = set()
    for row in edges:
        assert isinstance(row, list) and len(row) == 2, f'invalid causal edge: {row!r}'
        before, after = row
        assert before in milestones and after in milestones, f'unknown milestone in edge {row!r}'
        assert before != after, f'self-edge is not allowed: {before}'
        edge = (before, after)
        assert edge not in seen_edges, f'duplicate causal edge: {edge}'
        seen_edges.add(edge)
        graph[before].append(after)
        indegree[after] += 1
        if before in owner_index and after in owner_index:
            assert owner_index[before] <= owner_index[after], (
                f'causal order violated: {before} must not appear after {after}'
            )

    queue = deque(node for node, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    assert visited == len(milestones), 'narrative causal graph contains a cycle'
    return main_keys, appendix_keys


def main() -> None:
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    script_load_order = re.findall(r'<script\s+src="([^"]+)"', index)
    deck_assets = [name for name in script_load_order if name.startswith('deck-') and name != 'deck.js']
    speaker_assets = [name for name in script_load_order if re.fullmatch(r'speaker-script-.*\.js', name)]
    assert deck_assets == ['deck-main.js', 'deck-appendix.js'], f'unexpected deck load order: {deck_assets}'
    assert speaker_assets == [contract['speaker_owner']], f'canonical speaker owner mismatch: {speaker_assets}'
    assert script_load_order.index(contract['speaker_owner']) < script_load_order.index('deck.js')
    assert not any(name.startswith('speaker-notes-') for name in script_load_order), 'legacy notes still participate in runtime ownership'

    expected_qa = contract['runtime_qa_contract']
    match = re.search(r'data-deck-qa-contract="([^"]+)"', index)
    assert match and match.group(1) == expected_qa, 'index runtime QA contract mismatch'
    deck_runtime = (ROOT / 'deck.js').read_text(encoding='utf-8')
    assert f"const DECK_QA_CONTRACT = '{expected_qa}';" in deck_runtime, 'deck.js runtime QA contract mismatch'

    slides = parse_slides(deck_assets)
    main_keys, appendix_keys = validate_contract(contract, slides)
    expected_keys = main_keys + appendix_keys

    script_raw = (ROOT / contract['speaker_owner']).read_text(encoding='utf-8')
    speech_match = re.search(r'window\.SPEAKER_SCRIPT\s*=\s*Object\.freeze\((\{.*\})\);\s*$', script_raw, re.S)
    assert speech_match, 'cannot parse canonical speaker script'
    speech = json.loads(speech_match.group(1))
    assert list(speech.keys()) == expected_keys, 'speaker-script key order/coverage differs from slide order'
    assert set(speech) == set(expected_keys), 'speaker-script has orphan or missing entries'
    for key in expected_keys:
        value = speech[key].strip()
        assert len(value) >= 80, f'{key} speaker text is too short to be useful speech'
        assert not re.search(r'(ЗАЧЕМ|СКАЗАТЬ|ПЕРЕХОД|ДЕТАЛЬ|НЕ ПЕРЕОБЕЩАТЬ):', value), f'internal note label leaked into {key}'
        assert 'http://' not in value and 'https://' not in value, f'URL leaked into spoken text {key}'
        assert 'remember to' not in value.lower(), f'instruction leaked into spoken text {key}'
        assert not re.search(r'\b[0-9a-f]{12,40}\b', value, re.I), f'commit-like identifier leaked into spoken text {key}'

    conference_files = [
        ROOT / 'deck-main.js',
        ROOT / 'deck-appendix.js',
        ROOT / contract['speaker_owner'],
        ROOT / 'claims.md',
        ROOT / 'README.md',
        ROOT / 'index.html',
    ]
    pin_pattern = re.compile(r'UniversalToolchain/(?:blob|tree)/[0-9a-f]{7,40}/', re.I)
    for path in conference_files:
        if path.exists():
            assert not pin_pattern.search(path.read_text(encoding='utf-8')), f'presentation-level UT revision pin remains in {path.name}'

    repo_speaker_assets = sorted(path.name for path in ROOT.glob('speaker-script-*.js'))
    assert repo_speaker_assets == [contract['speaker_owner']], f'competing speaker-script assets remain: {repo_speaker_assets}'
    assert not list(ROOT.glob('speaker-notes-*.js')), 'legacy speaker-note owners must be removed'

    print(
        'Deck semantic contract PASS: '
        f"{len(main_keys)} main + {len(appendix_keys)} appendix; "
        f"{len(REQUIRED_MILESTONE_IDS)} stable milestones; causal DAG, evidence categories, "
        f"semantic ownership and canonical speaker coverage verified ({contract['contract_id']})"
    )


if __name__ == '__main__':
    main()
