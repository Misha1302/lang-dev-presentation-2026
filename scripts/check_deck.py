#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text(encoding='utf-8')

script_load_order = re.findall(r'<script\s+src="([^"]+)"', INDEX)
deck_assets = [name for name in script_load_order if name.startswith('deck-') and name != 'deck.js']
speaker_assets = [name for name in script_load_order if re.fullmatch(r'speaker-script-.*\.js', name)]
assert deck_assets == ['deck-main.js', 'deck-appendix.js'], f'unexpected deck load order: {deck_assets}'
assert speaker_assets == ['speaker-script-canonical.js'], f'canonical speaker owner mismatch: {speaker_assets}'
assert script_load_order.index('speaker-script-canonical.js') < script_load_order.index('deck.js')
assert not any(name.startswith('speaker-notes-') for name in script_load_order), 'legacy notes still participate in runtime ownership'
assert 'data-deck-qa-contract="architecture-story-v3"' in INDEX


def fragment_text(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    match = re.search(r'String\.raw`(.*)`\);\s*$', raw, re.S)
    assert match, f'cannot parse {path.name}'
    return match.group(1)


fragments = '\n'.join(fragment_text(ROOT / name) for name in deck_assets)


class SlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[tuple[dict[str, str], str]] = []
        self.current: dict[str, str] | None = None
        self.depth = 0
        self.buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attr = dict(attrs)
        if self.current is None and tag == 'section' and 'slide' in attr.get('class', '').split():
            self.current = attr
            self.depth = 1
            self.buffer = []
            return
        if self.current is not None and tag not in {'br', 'meta', 'link', 'img', 'input'}:
            self.depth += 1

    def handle_startendtag(self, tag: str, attrs) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        self.depth -= 1
        if self.depth == 0 and tag == 'section':
            text = ' '.join(' '.join(self.buffer).split())
            self.slides.append((self.current, text))
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.buffer.append(data)


parser = SlideParser()
parser.feed(fragments)
main = [slide for slide in parser.slides if slide[0].get('data-kind') == 'main']
appendix = [slide for slide in parser.slides if slide[0].get('data-kind') == 'appendix']
expected_main_keys = [f'm{i}' for i in range(1, 53)]
expected_appendix_keys = [f'a{i}' for i in range(1, 9)]
assert len(main) == 52, f'expected 52 main slides, got {len(main)}'
assert len(appendix) == 8, f'expected 8 appendix slides, got {len(appendix)}'
assert [slide[0].get('data-note-key') for slide in main] == expected_main_keys
assert [slide[0].get('data-note-key') for slide in appendix] == expected_appendix_keys
assert len({slide[0].get('data-note-key') for slide in parser.slides}) == 60, 'duplicate slide note key'

main_text = '\n'.join(slide[1] for slide in main)
appendix_text = '\n'.join(slide[1] for slide in appendix)
all_text = main_text + '\n' + appendix_text

# This is a causal-story contract, not just a slide-count contract. If any of
# these load-bearing concepts disappears or moves behind its consequence, CI
# must fail.
anchors = [
    'A monolithic compiler is often the right answer',
    'A capability / extension is something authored once and reusable across languages',
    'A dialect is one declarative language profile built from that ecosystem',
    'Capability ≠ dialect',
    'One ecosystem → multiple dialects',
    'There are two independent moves',
    'Two extension authors should not need a private handshake',
    'The dialect declares WHAT language we want.',
    'A configuration is not yet a compiler',
    'Composition should end in one concrete compiler plan',
    'Requested behavior can require a representation property',
    'Choosing a conversion skeleton too early actually missed feasible routes',
    'FEASIBILITY FIRST.',
    'Resolve the open world once.',
    'Extensibility machinery can stay off the runtime hot path',
    'Peephole optimization looks at a small window',
    'Local rewrites are easy. Global optimization needs shared facts.',
    'A bounds check is a non-local proof problem',
    'Two authors should not need a private handshake for semantic knowledge either.',
    'Stable typed semantic queries decouple producers from consumers',
    'A write is not just “writable”',
    'A typed fact can become stale after a transformation',
    'A Judgement says what is known',
    'An Obligation is what must hold before a transformation is legal',
    'Representation axis ≠ knowledge axis',
    'There is no universal inverse lowering',
    'Preserve, expose or re-analyse the facts a later pass still needs',
    'Maybe a shared semantic layer is unnecessary',
    'Add a producer. Change zero consumers. Measure soundness and coupling.',
    'Keep implementation witness, general design and research hypothesis separate',
    'Extensibility should disappear where it is machinery',
]
for anchor in anchors:
    assert anchor in main_text, f'missing narrative anchor: {anchor}'
positions = [main_text.index(anchor) for anchor in anchors]
assert positions == sorted(positions), 'causal narrative anchors are out of order'

# Dialect/extensibility story must remain explicit rather than implied.
for marker in [
    'It is not a language by itself.',
    'One capability can appear in many language profiles.',
    'One dialect selects and constrains many reusable things.',
    'add new pieces + recombine existing pieces',
    'First goal: both can enter the same ecosystem and participate in one dialect without pairwise coordination.',
    'The composer / planner resolves HOW to assemble it.',
    'structural extensibility → semantic extensibility',
]:
    assert marker in main_text, f'missing extensibility marker: {marker}'

# Planner, optimization, semantic and lowering blocks are all load-bearing.
assert 'Three AIR instructions become one typed intrinsic' in main_text
assert 'SafeIndex(a,i)' in main_text
assert 'GC-barrier semantics' in main_text
assert 'IAtomicVolatileOrderedWritable' in main_text
assert 'Historical failure mode' in main_text
assert 'Cost is not a proof of semantic preservation' in main_text
assert 'RangeAnalysis' in main_text and 'ShapeAnalysis' in main_text
assert 'meaning stays queryable / re-derivable' in main_text
assert 'No numerical ratio is published' in main_text
assert 'prepared C# delegate' in main_text and 'Wist compiled delegate' in main_text
assert 'volatility' in main_text and 'atomicity' in main_text and 'ordering' in main_text
assert 'visibility' in main_text and 'transaction context' in main_text
assert 'Only valid evidence may discharge an Obligation' in main_text
assert 'representation axis' in main_text and 'knowledge axis' in main_text
assert 'Wist module, Feature and Contribution' not in main_text
assert 'bounded reflection' not in main_text.lower()
assert 'CMake' not in main_text
assert 'Wist module, Feature and Contribution' in appendix_text
assert 'Historical failure mode' in appendix_text

for required_status in ['IMPLEMENTED WITNESS', 'GENERAL DESIGN', 'RESEARCH HYPOTHESIS']:
    assert required_status in all_text, f'missing status category {required_status}'
for stale_status in ['CURRENT UT', 'DESIGN SKETCH', 'PROPOSED / RESEARCH', 'OPEN ARCHITECTURE QUESTION']:
    assert stale_status not in all_text, f'stale status remains: {stale_status}'

conference_files = [
    ROOT / 'deck-main.js',
    ROOT / 'deck-appendix.js',
    ROOT / 'speaker-script-canonical.js',
    ROOT / 'claims.md',
    ROOT / 'README.md',
    ROOT / 'index.html',
]
pin_pattern = re.compile(r'UniversalToolchain/(?:blob|tree)/[0-9a-f]{7,40}/', re.I)
for path in conference_files:
    if path.exists():
        assert not pin_pattern.search(path.read_text(encoding='utf-8')), f'presentation-level UT revision pin remains in {path.name}'

script_raw = (ROOT / 'speaker-script-canonical.js').read_text(encoding='utf-8')
match = re.search(r'window\.SPEAKER_SCRIPT\s*=\s*Object\.freeze\((\{.*\})\);\s*$', script_raw, re.S)
assert match, 'cannot parse canonical speaker script'
speech = json.loads(match.group(1))
expected_keys = expected_main_keys + expected_appendix_keys
assert list(speech.keys()) == expected_keys, 'speaker-script key order/coverage differs from slide order'
assert set(speech) == set(expected_keys)
for key in expected_keys:
    value = speech[key].strip()
    assert len(value) >= 80, f'{key} speaker text is too short to be useful speech'
    assert not re.search(r'(ЗАЧЕМ|СКАЗАТЬ|ПЕРЕХОД|ДЕТАЛЬ|НЕ ПЕРЕОБЕЩАТЬ):', value), f'internal note label leaked into {key}'
    assert 'http://' not in value and 'https://' not in value, f'URL leaked into spoken text {key}'
    assert 'remember to' not in value.lower(), f'instruction leaked into spoken text {key}'
    assert not re.search(r'\b[0-9a-f]{12,40}\b', value, re.I), f'commit-like identifier leaked into spoken text {key}'

# The private-handshake motif must be planted structurally and called back
# semantically in the canonical stage script, not only on slide furniture.
assert 'private handshake' in speech['m11'].lower()
assert 'private handshake' in speech['m32'].lower()
assert 'structural' in speech['m32'].lower() and 'semantic' in speech['m32'].lower()
assert 'same extensibility problem' in speech['m32'].lower()
assert 'what' in speech['m12'].lower() and 'how' in speech['m12'].lower()
assert 'feasibility first' in speech['m20'].lower()
assert 'judgement' in speech['m40'].lower() and 'obligation' in speech['m41'].lower()
assert 'author' in speech['m52'].lower() and 'resolve' in speech['m52'].lower() and 'optimize' in speech['m52'].lower()

repo_speaker_assets = sorted(path.name for path in ROOT.glob('speaker-script-*.js'))
assert repo_speaker_assets == ['speaker-script-canonical.js'], f'competing speaker-script assets remain: {repo_speaker_assets}'
assert not list(ROOT.glob('speaker-notes-*.js')), 'legacy speaker-note owners must be removed'

print('Deck contract PASS: 52 main + 8 appendix; dialect/extensibility causality, planner feasibility, local/global optimization, semantic callback, Write/Judgement/Obligation, lowering story and one canonical spoken-script owner verified')
