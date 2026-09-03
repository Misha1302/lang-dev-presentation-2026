#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "speaker-notes-hardening.js"
text = path.read_text(encoding="utf-8")
old = "durable program и reusable delegate.\n\nПЕРЕХОД: теперь можно обсуждать стоимость extensibility без магического «zero cost»."
new = r"durable program и reusable delegate.\n\nПЕРЕХОД: теперь можно обсуждать стоимость extensibility без магического «zero cost»."
if text.count(old) != 1:
    raise SystemExit(f"expected one literal-newline note fragment, got {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("speaker-note JSON escaping fixed")
