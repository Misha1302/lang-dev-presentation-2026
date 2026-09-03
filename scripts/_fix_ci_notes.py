#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]

notes_path = root / "speaker-notes-hardening.js"
text = notes_path.read_text(encoding="utf-8")
old = "durable program и reusable delegate.\n\nПЕРЕХОД: теперь можно обсуждать стоимость extensibility без магического «zero cost»."
new = r"durable program и reusable delegate.\n\nПЕРЕХОД: теперь можно обсуждать стоимость extensibility без магического «zero cost»."
if text.count(old) != 1:
    raise SystemExit(f"expected one literal-newline note fragment, got {text.count(old)}")
notes_path.write_text(text.replace(old, new, 1), encoding="utf-8")

check_path = root / "scripts" / "check_deck.py"
check = check_path.read_text(encoding="utf-8")
old_check = '    "Cost is a planning weight, not measured runtime latency",'
new_check = '    "Current order: conversion skeleton first → selected passes second. Cost ≠ runtime latency.",'
if check.count(old_check) != 1:
    raise SystemExit(f"expected one stale cost assertion, got {check.count(old_check)}")
check_path.write_text(check.replace(old_check, new_check, 1), encoding="utf-8")

print("speaker-note JSON escaping and hardened cost assertion fixed")
