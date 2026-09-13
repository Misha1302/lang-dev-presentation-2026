#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def extract_js_string_array(source: str, const_name: str) -> list[str]:
    pattern = rf'const\s+{re.escape(const_name)}\s*=\s*Object\.freeze\(\[(.*?)\]\);'
    match = re.search(pattern, source, re.S)
    if not match:
        raise AssertionError(f'cannot parse {const_name}')
    return re.findall(r"'([^']+)'", match.group(1))

def load_speaker_script() -> dict[str, str]:
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    scripts = [name for name in re.findall(r'<script\s+src="([^"]+)"', index) if name.startswith('speaker-script')]
    if not scripts:
        raise AssertionError('no speaker-script files in index.html')
    node = r'''
const fs = require('fs');
const vm = require('vm');
const ctx = { window: {}, console };
vm.createContext(ctx);
for (const file of process.argv.slice(1)) {
  vm.runInContext(fs.readFileSync(file, 'utf8'), ctx, { filename: file });
}
console.log(JSON.stringify(ctx.window.SPEAKER_SCRIPT || {}));
'''
    result = subprocess.run(['node', '-e', node, *scripts], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError('speaker script evaluation failed: ' + result.stderr)
    return json.loads(result.stdout)

def count_words(text: str) -> int:
    return len(re.findall(r"[\w'-]+", text))

narrative = (ROOT / 'deck-narrative-reframe.js').read_text(encoding='utf-8')
main_order = extract_js_string_array(narrative, 'FINAL_MAIN_ORDER')
appendix_demotions = extract_js_string_array(narrative, 'FINAL_APPENDIX_KEYS')
speech = load_speaker_script()
missing = [key for key in main_order if not str(speech.get(key, '')).strip()]
if missing:
    raise AssertionError('missing runtime speaker entries: ' + ', '.join(missing))
words = [(key, count_words(str(speech[key]))) for key in main_order]
seconds = [(key, round(word_count / 130 * 60)) for key, word_count in words]
total_words = sum(word_count for _, word_count in words)
total = sum(sec for _, sec in seconds)
long = [(key, word_count) for key, word_count in words if word_count > 95]
print(f'runtime main slides: {len(main_order)}')
print(f'tracked runtime appendix demotions: {len(appendix_demotions)}')
print(f'main spoken words: {total_words}')
print(f'rehearsal estimate at 130 wpm: {total // 60:02d}:{total % 60:02d}')
print(f'per-slide spoken range: {min(sec for _, sec in seconds)}-{max(sec for _, sec in seconds)} s')
if long:
    print('long runtime notes (>95 words): ' + ', '.join(f'{key}={count}' for key, count in long))
if not (22 * 60 <= total <= 26 * 60):
    raise AssertionError(f'timing contract outside 22-26 min for runtime deck: {total // 60:02d}:{total % 60:02d}')
print('Timing audit PASS: final runtime main script stays inside the 22-26 minute rehearsal envelope')
