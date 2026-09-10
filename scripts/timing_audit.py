#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / 'speaker-script-canonical.js').read_text(encoding='utf-8')
match = re.search(r'window\.SPEAKER_SCRIPT\s*=\s*Object\.freeze\((\{.*\})\);\s*$', raw, re.S)
assert match, 'cannot parse canonical speaker script'
speech = json.loads(match.group(1))

deck_raw = (ROOT / 'deck-main.js').read_text(encoding='utf-8')
main_keys = re.findall(
    r'<section\b[^>]*data-kind="main"[^>]*data-note-key="([^"]+)"',
    deck_raw,
)
assert main_keys, 'cannot discover main slide keys from deck-main.js'
assert list(speech)[:len(main_keys)] == main_keys, 'main script order mismatch'

research_raw = (ROOT / 'speaker-script-research-update.js').read_text(encoding='utf-8')
research_pairs = re.findall(r'^\s*"(r\d+)":\s*"([^"]+)"', research_raw, re.MULTILINE)
research_speech = dict(research_pairs)
assert list(research_speech) == [f'r{i}' for i in range(1, 8)], 'research speaker extension mismatch'
speech.update(research_speech)

runtime_main_keys = list(main_keys)
for child, anchor in [
    ('r1', 'm3'),
    ('r2', 'r1'),
    ('r3', 'r2'),
    ('r4', 'r3'),
    ('r5', 'r4'),
    ('r6', 'm12'),
    ('r7', 'm25'),
]:
    runtime_main_keys.insert(runtime_main_keys.index(anchor) + 1, child)

override_raw = (ROOT / 'speaker-script-conference-overrides.js').read_text(encoding='utf-8')
override_pairs = re.findall(
    r'^\s*([mr]\d+):\s*`(.*?)`\s*,?\s*$',
    override_raw,
    re.MULTILINE | re.DOTALL,
)
override_speech = dict(override_pairs)
assert override_speech, 'conference speaker override layer is empty or unparsable'
unknown_overrides = set(override_speech) - set(runtime_main_keys)
assert not unknown_overrides, f'conference speaker overrides unknown runtime keys: {sorted(unknown_overrides)}'
speech.update(override_speech)

word_counts = [len(re.findall(r"[\w'-]+", speech[key])) for key in runtime_main_keys]
seconds = [round(words / 130 * 60) for words in word_counts]
total = sum(seconds)
print(f'main slides: {len(runtime_main_keys)} (32 authored + 7 additive research)')
print(f'conference speaker overrides: {len(override_speech)}')
print(f'main spoken words: {sum(word_counts)}')
print(f'rehearsal estimate at 130 wpm: {total // 60:02d}:{total % 60:02d}')
print(f'per-slide spoken range: {min(seconds)}-{max(seconds)} s')
# LangDev gives 25 minutes for the talk. Keep roughly 1-3 minutes of real-stage
# headroom for pauses, transitions and audience reaction instead of filling the
# entire slot with uninterrupted 130-wpm speech.
assert 22 * 60 <= total <= 24 * 60, f'timing contract outside 22-24 min: {total // 60:02d}:{total % 60:02d}'
print('Timing audit PASS: effective runtime main script stays inside the 22-24 minute rehearsal envelope for a 25-minute talk')
