#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / 'speaker-script-canonical.js').read_text(encoding='utf-8')
match = re.search(r'window\.SPEAKER_SCRIPT\s*=\s*Object\.freeze\((\{.*\})\);\s*$', raw, re.S)
assert match, 'cannot parse canonical speaker script'
speech = json.loads(match.group(1))
main_keys = [f'm{i}' for i in range(1, 41)]
assert list(speech)[:40] == main_keys, 'main script order mismatch'

word_counts = [len(re.findall(r"[\w'-]+", speech[key])) for key in main_keys]
seconds = [round(words / 130 * 60) for words in word_counts]
total = sum(seconds)
print(f'main slides: {len(main_keys)}')
print(f'main spoken words: {sum(word_counts)}')
print(f'rehearsal estimate at 130 wpm: {total // 60:02d}:{total % 60:02d}')
print(f'per-slide spoken range: {min(seconds)}-{max(seconds)} s')
print('Timing audit PASS: estimate is informational; no artificial slide-count cap is enforced')
