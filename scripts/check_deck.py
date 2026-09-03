#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
notes = (ROOT / "speaker-notes-hardening.js").read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
deck_js = (ROOT / "deck.js").read_text(encoding="utf-8")
qa = (ROOT / "CLAIM_BOUNDARIES_40_QA.md").read_text(encoding="utf-8")

class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self._in = False
        self._depth = 0
        self._buf = []
        self._attrs = {}

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if self._in and tag == "br":
            self._buf.append(" ")
        if tag == "section" and "slide" in values.get("class", "").split():
            self._in = True
            self._depth = 1
            self._buf = []
            self._attrs = values
            return
        if self._in and tag not in {"br", "meta", "link", "img", "input"}:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._in:
            self._depth -= 1
            if self._depth == 0 and tag == "section":
                self.slides.append((self._attrs, " ".join("".join(self._buf).split())))
                self._in = False

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

parser = SlideParser()
parser.feed(html)
main = [s for s in parser.slides if s[0].get("data-kind") != "appendix"]
appendix = [s for s in parser.slides if s[0].get("data-kind") == "appendix"]
assert len(main) == 14, f"expected 14 main slides, got {len(main)}"
assert len(appendix) == 8, f"expected 8 appendix slides, got {len(appendix)}"
assert [s[0].get("data-note-key") for s in main] == [f"m{i}" for i in range(1, 15)]
assert [s[0].get("data-note-key") for s in appendix] == [f"a{i}" for i in range(1, 9)]

expected_titles = [
    "When Extensibility Becomes Planning",
    "If one owner knows the compiler, wire it explicitly",
    "Independent extensions create requirements across compiler stages",
    "Planning begins when no local owner can guarantee a valid whole compiler",
    "Language authors define requirements; implementations declare what they satisfy",
    "A reachable pipeline is not necessarily an admissible compiler",
    "Feasibility before preference",
    "Planning materializes one inspectable concrete compiler plan",
    "Open during composition; concrete during execution",
    "A type-compatible shortcut can still be illegal",
    "UniversalToolchain proves the staging — and exposes the current limits",
    "Extensibility still has a price",
    "Sometimes the planner is the bigger problem",
    "Resolve globally only what correctness cannot own locally",
]
for i, title in enumerate(expected_titles):
    assert title in main[i][1], f"slide {i + 1} missing expected title: {title}"

assert 'data-deck-qa-contract="obligations-core-v1"' in html
assert "obligations-core-v1" in deck_js

required = [
    "Declare requirements locally. Resolve feasibility globally. Execute one concrete plan.",
    "Hard obligations define admissibility. Preference only chooses among admissible compiler plans.",
    "Planner owns global implementation resolution — not the meaning of the language.",
    "Artifact identity and semantic state are orthogonal dimensions.",
    "Green means feasible — not cheaper.",
    "CURRENT UT",
    "CURRENT LIMITATION",
    "PROPOSED GENERAL MODEL",
    "UT is a useful prototype of staged composition, not the reference architecture.",
    "Performance impact: NEEDS MEASUREMENT.",
    "whole-language planner → cross-owner hard constraints",
    "7005371d6c30175dff4b0e9f906a26218b0ee54d",
]
combined = html + "\n" + notes + "\n" + qa
missing = [item for item in required if item not in combined]
assert not missing, f"missing architecture/narrative anchors: {missing}"

for forbidden in [
    "Planning chooses the language",
    "Changing language composition changes the resolved route",
    "route Cost = 2",
    "route Cost = 7",
    "Lower Cost means planner preference",
    "Extensibility becomes planning when choices stop being independent.",
]:
    assert forbidden not in combined, f"stale mental model remains: {forbidden}"

# The central case-study slide must not visually/textually teach Cost ranking.
assert "Cost" not in main[9][1], "slide 10 must not use Cost as its proof"
for anchor in ["NoHighLevelOps", "CilLegal", "reject candidate", "rank only after feasible"]:
    assert anchor in main[9][1], f"slide 10 missing legalization anchor: {anchor}"

for label in ["CURRENT UT", "CURRENT LIMITATION", "PROPOSED GENERAL MODEL"]:
    assert label in main[10][1], f"slide 11 missing boundary label: {label}"

# Every live main note must preserve the causal presenter structure.
for n in range(1, 15):
    assert re.search(rf"\bm{n}\s*:\s*`", notes), f"speaker note m{n} missing"
for marker in ["ЗАЧЕМ:", "СКАЗАТЬ:", "ПЕРЕХОД:", "НЕ ПЕРЕОБЕЩАТЬ:"]:
    assert notes.count(marker) >= 14, f"main notes missing enough {marker} sections"

for primitive in [".broken", ".good", ".architecture", ".casegrid", ".decisionrule"]:
    assert primitive in css, f"missing visual primitive: {primitive}"

assert qa.count("\n## ") == 40, f"expected 40 hostile Q&A items, got {qa.count(chr(10) + '## ')}"
for q in [
    "Why isn't this just a pass manager?",
    "Why isn't this MLIR legalization?",
    "Who owns Cost?",
    "When not to use a planner?",
]:
    assert q in qa, f"hostile Q&A missing: {q}"

print(
    "Deck contract PASS: 14 main + 8 appendix; obligation-first narrative; "
    "legalization case; CURRENT/LIMITATION/PROPOSED boundary; 40 hostile Q&A"
)
