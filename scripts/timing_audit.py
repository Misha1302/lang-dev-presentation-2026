#!/usr/bin/env python3
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
js1=(root/'speaker-notes-1.js').read_text(); js2=(root/'speaker-notes-2.js').read_text(); js3=(root/'speaker-notes-hardening.js').read_text()
o=json.loads(re.search(r'window\.SPEAKER_NOTES=(\{.*?\});\n',js1,re.S).group(1)); o.update(json.loads(re.search(r'Object\.assign\(window\.SPEAKER_NOTES,(\{.*?\})\);\n',js2,re.S).group(1))); o.update(json.loads(re.search(r'Object\.assign\(window\.SPEAKER_NOTES,\s*(\{.*?\})\s*\);',js3,re.S).group(1)))
words=sum(len(re.findall(r'\b[\wА-Яа-яЁё.-]+\b',o[f'm{i}'])) for i in range(1,17)); print(f'speaker notes: {words} words')
for wpm in (125,135,145):
    minutes=words/wpm; print(f'@ {wpm} wpm: {int(minutes):02d}:{int(round((minutes%1)*60)):02d}')
