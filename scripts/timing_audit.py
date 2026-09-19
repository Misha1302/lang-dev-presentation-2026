#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'rebuild-2026-09-17' / 'delegates-rebuild-deck.html'
SCRIPT = ROOT / 'rebuild-2026-09-17' / 'speaker-script-conference.md'
raw = DECK.read_text(encoding='utf-8')
script = SCRIPT.read_text(encoding='utf-8')
main_keys = re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*(?:data-note-key|data-note)="(m\d+)"', raw)
blocks = dict(re.findall(r'^##\s+(m\d+|a\d+)\s*\n\n(.*?)(?=\n##\s+|\Z)', script, re.S | re.M))
missing = [k for k in main_keys if not blocks.get(k, '').strip()]
if missing:
    raise SystemExit('Timing audit FAILED: missing script entries: ' + ','.join(missing))
words = sum(len(re.findall(r"[A-Za-zА-Яа-я0-9]+(?:[-'][A-Za-zА-Яа-я0-9]+)?", blocks[k])) for k in main_keys)
seconds = round(words * 60 / 130)
print(f'runtime main slides: {len(main_keys)}')
print(f'runtime main spoken words: {words}')
print(f'rehearsal estimate at 130 wpm: {seconds//60:02d}:{seconds%60:02d}')
if not (22*60 <= seconds <= 25*60):
    raise SystemExit('Timing audit FAILED: script outside 22-25 minute conference range')
print('Timing audit PASS: complete speaker script is inside the 22-25 minute conference range')
