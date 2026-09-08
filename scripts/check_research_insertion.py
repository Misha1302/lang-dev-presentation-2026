#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTECTED = [
    "deck-main.js",
    "deck-appendix.js",
    "speaker-script-canonical.js",
]
EXPECTED_RESEARCH_KEYS = [f"r{i}" for i in range(1, 8)]
EXPECTED_ORDER_EDGES = [
    ("r1", "m3"),
    ("r2", "r1"),
    ("r3", "r2"),
    ("r4", "r3"),
    ("r5", "r4"),
    ("r6", "m12"),
    ("r7", "m25"),
]


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RESEARCH_INSERTION=FAIL: {message}")


def main() -> int:
    base = run("git", "merge-base", "HEAD", "origin/main")
    for path in PROTECTED:
        before = run("git", "rev-parse", f"{base}:{path}")
        after = run("git", "rev-parse", f"HEAD:{path}")
        require(before == after, f"protected authored content changed: {path}")

    deck = (ROOT / "deck-research-update.js").read_text(encoding="utf-8")
    speech = (ROOT / "speaker-script-research-update.js").read_text(encoding="utf-8")
    index = (ROOT / "index.html").read_text(encoding="utf-8")

    deck_keys = re.findall(r'data-note-key="(r\d+)"', deck)
    require(deck_keys == EXPECTED_RESEARCH_KEYS, f"research slide keys/order mismatch: {deck_keys}")
    for child, anchor in EXPECTED_ORDER_EDGES:
        needle = f"moveResearchSlideAfter('{child}', '{anchor}')"
        require(needle in deck, f"missing reorder edge {child} after {anchor}")

    speech_keys = re.findall(r'^\s*"(r\d+)":', speech, re.MULTILINE)
    require(speech_keys == EXPECTED_RESEARCH_KEYS, f"research speech keys/order mismatch: {speech_keys}")
    spoken = re.findall(r'^\s*"r\d+":\s*"([^"]+)"', speech, re.MULTILINE)
    word_count = sum(len(text.split()) for text in spoken)
    require(word_count <= 95, f"additive speech budget exceeded: {word_count} words")

    require('<script src="deck-research-update.js"></script>' in index, "deck research layer not loaded")
    require('<script src="speaker-script-research-update.js"></script>' in index, "speaker research layer not loaded")
    require(index.index('deck-main.js') < index.index('deck-research-update.js') < index.index('deck-appendix.js'),
            "deck research layer load order is wrong")
    require(index.index('speaker-script-canonical.js') < index.index('speaker-script-research-update.js') < index.index('deck.js'),
            "speaker research layer load order is wrong")

    print(f"RESEARCH_INSERTION=PASS protected=3 added_slides=7 added_speech_words={word_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
