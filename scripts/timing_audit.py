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

def count(text: str) -> int:
    return len(re.findall(r"[A-Za-zА-Яа-я0-9]+(?:[-'][A-Za-zА-Яа-я0-9]+)?", text))

per_slide = {k: count(blocks[k]) for k in main_keys}
words = sum(per_slide.values())
seconds = round(words * 60 / 130)
opening_seconds = round(per_slide['m1'] * 60 / 130)
delegate_intro_seconds = round((per_slide['m1'] + per_slide['m2']) * 60 / 130)
final_seconds = round(per_slide['m21'] * 60 / 130)
print(f'runtime main slides: {len(main_keys)}')
print(f'runtime main spoken words: {words}')
print(f'rehearsal estimate at 130 wpm: {seconds//60:02d}:{seconds%60:02d}')
print(f'slide 2 starts at approximately {opening_seconds}s')
print(f'delegate example setup completes at approximately {delegate_intro_seconds}s')
print(f'final synthesis: approximately {final_seconds}s')
if not (22*60 <= seconds <= 25*60):
    raise SystemExit('Timing audit FAILED: script outside 22-25 minute conference range')
if opening_seconds > 90:
    raise SystemExit('Timing audit FAILED: programmer-visible example does not appear inside first 90 seconds')
if delegate_intro_seconds > 120:
    raise SystemExit('Timing audit FAILED: central delegate example is not established within about 2 minutes')
if not (45 <= final_seconds <= 80):
    raise SystemExit('Timing audit FAILED: final synthesis is not approximately one minute')
print('Timing audit PASS: 22-25 minute talk, first-90s code, ~2-minute delegate setup, and ~1-minute final synthesis')
