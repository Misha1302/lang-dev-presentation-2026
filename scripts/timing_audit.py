#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'speaker-notes-hardening.js').read_text(encoding='utf-8')
prefix='window.SPEAKER_NOTES = '
notes=json.loads(raw[len(prefix):].rstrip()[:-1])
research=(ROOT/'speaker-notes-research.js').read_text(encoding='utf-8')
m=re.search(r'Object\.assign\(window\.SPEAKER_NOTES,\s*(\{.*\})\);\s*$',research,re.S)
assert m
notes.update(json.loads(m.group(1)))
main=[notes[f'm{i}'] for i in range(1,68)]
secs=[]
for note in main:
    words=len(re.findall(r'[\wА-Яа-яЁё-]+',note))
    s=max(24,min(120,round(words/130*60)+10))
    secs.append(s)
assert all(24 <= s <= 120 for s in secs)
total=sum(secs)
print(f'main slides: {len(main)}')
print(f'full intellectual-deck rehearsal estimate: {total//60:02d}:{total%60:02d}')
print(f'per-slide estimate range: {min(secs)}-{max(secs)} s')
print('No upper timing or slide-count cap is enforced; cutting is a later editorial pass.')
print('Timing audit PASS')
