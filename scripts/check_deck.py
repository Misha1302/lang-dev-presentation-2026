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
readme = (ROOT / "README.md").read_text(encoding="utf-8")
demo = (ROOT / "DEMO.md").read_text(encoding="utf-8")
demo_script = (ROOT / "demo" / "run-demo.sh").read_text(encoding="utf-8")


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
    "Build the Language, Then Make the Abstractions Disappear",
    "If one owner knows the compiler, wire it explicitly",
    "Start with a restricted pricing language",
    "The extensions disappear into one execution pipeline",
    "One language must not silently become two",
    "Who owns the fact that the whole compiler still implements one language?",
    "UniversalToolchain already separates composition from execution",
    "Structural routing can make a preference decision before semantic feasibility is known",
    "Feasibility before preference",
    "Keep current evidence separate from the stronger target model",
    "Open during composition; concrete during execution",
    "Making composition disappear before execution does not make extensibility free",
    "Sometimes the planner is the bigger problem",
    "Resolve globally only what correctness cannot own locally",
]
for i, title in enumerate(expected_titles):
    assert title in main[i][1], f"slide {i + 1} missing expected title: {title}"

assert 'data-deck-qa-contract="concrete-first-obligations-v2"' in html
assert "concrete-first-obligations-v2" in deck_js, "deck.js QA contract must match index.html"

combined = "\n".join([html, notes, readme, demo, qa])
required = [
    "pricing-restricted",
    "Bytecode",
    "AIR",
    "InterpreterBindingsParityTests",
    "external bindings",
    "local shadowing",
    "CURRENT UT",
    "PROPOSED MODEL",
    "FindBestRoute",
    "InsertPasses",
    "UTL2204",
    "Feasibility before preference",
    "Resolve globally only what correctness cannot own locally",
    "7005371d6c30175dff4b0e9f906a26218b0ee54d",
]
missing = [item for item in required if item not in combined]
assert not missing, f"missing narrative/evidence anchors: {missing}"

# The main deck must not teach the old synthetic route-cost demo as the proof.
main_text = "\n".join(text for _, text in main)
for forbidden in [
    "route Cost = 2",
    "route Cost = 7",
    "demo.lower.fast",
    "demo.lower.safe",
    "Changing language composition changes the resolved route",
]:
    assert forbidden not in main_text, f"stale central proof remains: {forbidden}"

# Current/proposed boundaries must be explicit before the general model can be mistaken for current UT.
assert "CURRENT UT" in main[7][1], "slide 8 must label current UT limitation"
assert "PROPOSED MODEL" in main[8][1], "slide 9 must label proposed general model"
assert "CURRENT LanguagePlan" in main[9][1]
assert "PROPOSED planner evidence" in main[9][1]

# Practical abstract-alignment anchors must appear before the architecture generalization.
for anchor in ["pricing-restricted", "interpreter", "cil"]:
    assert anchor in main[2][1], f"slide 3 missing concrete language anchor: {anchor}"
for anchor in ["BYTECODE", "AIR", "INTERPRETER / CIL"]:
    assert anchor in main[3][1], f"slide 4 missing Wist pipeline anchor: {anchor}"
for anchor in ["external", "shadows", "cross-backend parity"]:
    assert anchor in main[4][1], f"slide 5 missing parity anchor: {anchor}"

# Demo/runbook must prove pricing + parity rather than synthetic route preference.
for anchor in [
    "pricing-restricted",
    "[pricing:interpreter] result=95",
    "[pricing:cil] result=95",
    "ShadowingAndNestedScope_WithLocalNamesOverlappingExternals_ShouldBeDeterministicAndParityStable",
    "[parity] shadowing regression PASS",
]:
    assert anchor in demo_script, f"demo script missing source-backed anchor: {anchor}"
assert "route Cost 7 → route Cost 2" in demo, "runbook should explain why old proof was demoted"

# Every live main note preserves the causal presenter structure.
for n in range(1, 15):
    assert re.search(rf"\bm{n}\s*:\s*`", notes), f"speaker note m{n} missing"
for marker in ["ЗАЧЕМ:", "СКАЗАТЬ:", "ПЕРЕХОД:", "НЕ ПЕРЕОБЕЩАТЬ:"]:
    assert notes.count(marker) >= 14, f"main notes missing enough {marker} sections"

for primitive in [".broken", ".good", ".timeline", ".comparecards", ".decisionrule"]:
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
    "Deck contract PASS: 14 main + 8 appendix; concrete pricing/Wist/parity proof precedes "
    "current-UT limitation and proposed obligation-first architecture"
)
