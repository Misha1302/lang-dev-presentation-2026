#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text(encoding="utf-8")
css = (root / "styles.css").read_text(encoding="utf-8")
js1 = (root / "speaker-notes-1.js").read_text(encoding="utf-8")
js2 = (root / "speaker-notes-2.js").read_text(encoding="utf-8")
js3 = (root / "speaker-notes-hardening.js").read_text(encoding="utf-8")
demo_source = (root / "demo" / "Program.cs").read_text(encoding="utf-8")
demo_run = (root / "demo" / "run-demo.sh").read_text(encoding="utf-8")
demo_doc = (root / "DEMO.md").read_text(encoding="utf-8")
claims = (root / "claims.md").read_text(encoding="utf-8")
readme = (root / "README.md").read_text(encoding="utf-8")
adversarial = (root / "ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
audit = (root / "REDESIGN_AUDIT_2026-09-03.md").read_text(encoding="utf-8")
qa = (root / "CLAIM_BOUNDARIES_40_QA.md").read_text(encoding="utf-8")

m1 = re.search(r"window\.SPEAKER_NOTES=(\{.*?\});\n", js1, re.S)
m2 = re.search(r"Object\.assign\(window\.SPEAKER_NOTES,(\{.*?\})\);", js2, re.S)
m3 = re.search(r"Object\.assign\(window\.SPEAKER_NOTES,\s*(\{.*?\})\s*\);", js3, re.S)
assert m1 and m2 and m3, "speaker notes objects missing"
notes_by_key = json.loads(m1.group(1))
notes_by_key.update(json.loads(m2.group(1)))
notes_by_key.update(json.loads(m3.group(1)))


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
        if tag == "section" and "slide" in values.get("class", "").split():
            self._in = True
            self._depth = 1
            self._buf = []
            self._attrs = values
            return
        if self._in:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._in:
            self._depth -= 1
            if self._depth == 0 and tag == "section":
                text = " ".join("".join(self._buf).split())
                self.slides.append((self._attrs, text))
                self._in = False

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)


parser = SlideParser()
parser.feed(html)
main = [slide for slide in parser.slides if slide[0].get("data-kind") != "appendix"]
appendix = [slide for slide in parser.slides if slide[0].get("data-kind") == "appendix"]
assert len(main) == 14, f"expected 14 main slides, got {len(main)}"
assert len(appendix) == 10, f"expected 10 appendix slides, got {len(appendix)}"

all_keys = []
for n, (attrs, _) in enumerate(parser.slides, 1):
    key = attrs.get("data-note-key")
    assert key, f"slide {n} has no data-note-key"
    assert key not in all_keys, f"duplicate speaker note key: {key}"
    all_keys.append(key)
    assert key in notes_by_key, f"slide {n} missing speaker note content for {key}"
    assert len(notes_by_key[key]) > 120, f"speaker note {key} looks truncated"

assert [slide[0].get("data-note-key") for slide in main] == [
    f"m{i}" for i in range(1, 15)
]
assert [slide[0].get("data-note-key") for slide in appendix] == [
    f"a{i}" for i in range(1, 11)
]

main_notes = []
for n, (attrs, _) in enumerate(main, 1):
    note = notes_by_key[attrs["data-note-key"]]
    main_notes.append(note)
    assert len(note) > 300, f"main speaker note m{n} is too short"
    for marker in ["ЗАЧЕМ", "СКАЗАТЬ", "ПЕРЕХОД", "НЕ ПЕРЕОБЕЩАТЬ"]:
        assert marker in note, f"main slide {n} notes missing {marker}"

words = sum(
    len(re.findall(r"\b[\wА-Яа-яЁё.-]+\b", note))
    for note in main_notes
)
assert words >= 1500, f"live speaker cues look truncated: {words} words"

full = re.sub(
    r"\s+",
    " ",
    " ".join([html, js2, js3, claims, readme, adversarial, audit, qa]),
)

required = [
    "When Extensibility",
    "Declare locally. Resolve globally. Execute concretely.",
    "If one owner knows the pipeline",
    "Configuration becomes",
    "Framework author",
    "Package / extension author",
    "Language integrator",
    "LanguageDefinition",
    "One canonical semantic configuration model. One planning authority.",
    "Local transformations turn one pipeline into a",
    "automatic route search over already-selected conversion edges",
    "artifact-contract-compatible conversion graph",
    "global optimum across conversions + passes",
    "conversion skeleton first",
    "Cost is a planning weight, not measured runtime latency",
    "not source code",
    "AUTHORING",
    "MATERIALIZATION",
    "SOURCE BUILD",
    "Changing language composition changes the resolved route",
    "demo.lower.safe",
    "demo.lower.fast",
    "There are two different",
    "Evaluate(code)",
    "testing state space",
    "NEEDS MEASUREMENT",
    "planner complexity + hidden semantic coupling",
    "Extensibility becomes planning when choices stop being independent.",
    "7005371d6c30175dff4b0e9f906a26218b0ee54d",
]
missing = [value for value in required if value not in full]
assert not missing, f"missing narrative/evidence elements: {missing}"

layout_primitives = [
    ".phase{", ".family-grid{", ".interaction{", ".route-story{", ".routebox{",
    ".routecallout{", ".plan-card{", ".comparecards{", ".costs{", ".decisionrule{",
]
missing_layout = [value for value in layout_primitives if value not in css]
assert not missing_layout, f"missing current-deck layout primitives: {missing_layout}"

# Demo/source consistency: route change is the primary compiler-specific proof.
demo_contract = demo_source + "\n" + demo_run + "\n" + demo_doc
for anchor in [
    'new LanguagePackageId("Demo.Ambiguity")',
    'PreferCapabilityProvider(capability, providerA)',
    'LanguagePackageBuilder.Create("Demo.Route", "1")',
    '"demo.lower.safe"',
    '"demo.fast-path"',
    '"demo.lower.fast"',
    '.UseFeature("demo.fast-path")',
    '[route:base]',
    '[route:+fast-path]',
    'expectedLowering: "demo.lower.safe", expectedCost: 7',
    'expectedLowering: "demo.lower.fast", expectedCost: 2',
    'new LanguageExecutionRequest("41", backend)',
    'Expected 42',
    'UTL2002',
]:
    assert anchor in demo_contract, f"demo contract anchor missing: {anchor}"

slide10 = main[9][1]
for anchor in [
    "Changing language composition changes the resolved route",
    "demo.fast-path",
    "demo.lower.safe",
    "demo.lower.fast",
    "Cost = 7",
    "Cost = 2",
    "41",
    "42",
]:
    assert anchor in slide10, f"slide 10 no longer matches route-changing demo: {anchor}"

for stale in [
    "Resolve one ambiguity; run one resolved language",
    "real Wist dialect",
    "40 + 2",
    "6 * 7",
]:
    assert stale not in slide10, f"stale demo claim remains on slide 10: {stale}"

assert "route-changing demo is a future design" not in readme.lower()
assert "route-changing conference demo until" not in claims.lower()
assert "Resolve globally. Justify locally. Execute concretely." not in adversarial
assert "Resolve globally. Justify locally. Execute concretely." not in qa
assert qa.count("\n## ") == 40, "hostile Q&A must retain exactly 40 numbered questions"

# Current truth boundaries must remain explicit.
main_text = " ".join(text for _, text in main)
for forbidden in [
    "zero-cost extensibility",
    "all abstractions disappear",
    "semantically best compiler pipeline",
    "execution-time optimal route",
]:
    assert forbidden.lower() not in main_text.lower(), f"forbidden live claim: {forbidden}"

for removed_main_topic in [
    "foo(x)",
    "Supports(...)?",
    "EGraph",
    "automatic pass scheduling",
]:
    assert removed_main_topic not in main_text, (
        f"removed compiler mini-talk leaked back into main: {removed_main_topic}"
    )

# Source links should be pinned where the current implementation is load-bearing.
assert "UniversalToolchain/search?q=LanguageArtifactRoutePhase" not in html
assert "UniversalToolchain/search?q=WistEngine.Create" not in html
assert "UniversalToolchain/search?q=CompileCore" not in html

old_sha = "36206b66548fec365be6e03381ba44d50c2cafe5"
for name, text in [
    ("index.html", html),
    ("run-demo.sh", demo_run),
    ("DEMO.md", demo_doc),
    ("claims.md", claims),
    ("README.md", readme),
]:
    assert old_sha not in text, f"stale source pin remains in {name}"

expected_sha = "7005371d6c30175dff4b0e9f906a26218b0ee54d"
assert expected_sha in demo_run, "run-demo.sh is not pinned to current truth snapshot"
assert "59514e86d2708cc7b70d87e3f7b93d872ac78b6c" in readme
assert "planning-core-v3" in (root / "deck.js").read_text(encoding="utf-8")
assert (
    "speaker-notes-1.js" in html
    and "speaker-notes-2.js" in html
    and "speaker-notes-hardening.js" in html
)

print(
    f"OK: {len(main)} main, {len(appendix)} appendix, {len(all_keys)} note keys, "
    f"{words} live cue words; ownership + route-changing planning narrative PASS"
)
