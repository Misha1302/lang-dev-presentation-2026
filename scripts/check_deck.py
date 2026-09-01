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
        a = dict(attrs)
        if tag == "section" and "slide" in a.get("class", "").split():
            self._in = True
            self._depth = 1
            self._buf = []
            self._attrs = a
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

p = SlideParser()
p.feed(html)
main = [s for s in p.slides if s[0].get("data-kind") != "appendix"]
appendix = [s for s in p.slides if s[0].get("data-kind") == "appendix"]
assert len(main) == 16, f"expected 16 main slides, got {len(main)}"
assert len(appendix) == 10, f"expected 10 appendix slides, got {len(appendix)}"

all_keys = []
for n, (attrs, _) in enumerate(p.slides, 1):
    key = attrs.get("data-note-key")
    assert key, f"slide {n} has no data-note-key"
    assert key not in all_keys, f"duplicate speaker note key: {key}"
    all_keys.append(key)
    assert key in notes_by_key, f"slide {n} missing speaker note content for {key}"
    assert len(notes_by_key[key]) > 120, f"speaker note {key} looks truncated"

assert [s[0].get("data-note-key") for s in main] == [f"m{i}" for i in range(1, 17)]
assert [s[0].get("data-note-key") for s in appendix] == [f"a{i}" for i in range(1, 11)]

main_notes = []
for n, (attrs, _) in enumerate(main, 1):
    note = notes_by_key[attrs["data-note-key"]]
    main_notes.append(note)
    assert len(note) > 300, f"main speaker note m{n} is too short"
    for marker in ["ЗАЧЕМ", "СКАЗАТЬ", "ПЕРЕХОД", "НЕ ПЕРЕОБЕЩАТЬ"]:
        assert marker in note, f"main slide {n} notes missing {marker}"

words = sum(len(re.findall(r"\b[\wА-Яа-яЁё.-]+\b", n)) for n in main_notes)
assert words >= 1000, f"live speaker cues look truncated: {words} words"

required = [
    "Build an Extensible Language,",
    "Resolve globally. Justify locally. Execute concretely.",
    "One fixed language is easy",
    "Configuration becomes",
    "UTL2002",
    "PreferCapabilityProvider",
    "LanguageArtifactRoute",
    "LanguagePlan",
    "LanguageRuntime.Create",
    "Resolve one ambiguity; run one resolved language",
    "Planning answers",
    "Optimization asks",
    "Can the compiler evaluate",
    "pure",
    "deterministic",
    "trusted",
    "The selected environment can",
    "Supports(...)?",
    "One architecture",
    "automatic pass scheduling",
    "bounded straight-line symbolic simplifier",
    "NEEDS MEASUREMENT",
    "7005371d6c30175dff4b0e9f906a26218b0ee54d",
]
full = re.sub(r"\s+", " ", html + " " + js2 + " " + js3 + " " + claims + " " + readme)
missing = [x for x in required if x not in full]
assert not missing, f"missing narrative/evidence elements: {missing}"

layout_primitives = [
    ".phase{", ".family-grid{", ".pillgrid{", ".interaction{", ".roles{",
    ".route-story{", ".plan-card{", ".timeline{", ".comparecards{", ".costs{",
    ".decisionrule{",
]
missing_layout = [x for x in layout_primitives if x not in css]
assert not missing_layout, f"missing current-deck layout primitives: {missing_layout}"

# Demo/source consistency: semantic anchors, not brittle full-stdout matching.
demo_contract = demo_source + "\n" + demo_run + "\n" + demo_doc
for anchor in [
    'new LanguagePackageId("Demo.Ambiguity")',
    'PreferCapabilityProvider(capability, providerA)',
    'new LanguagePackageId("Demo.Runtime")',
    'new LanguageExecutionRequest("41", backend)',
    'Expected 42',
    'UTL2002',
]:
    assert anchor in demo_contract, f"demo contract anchor missing: {anchor}"

slide11 = main[10][1]
for anchor in ["UTL2002", "PreferCapabilityProvider", "LanguagePlan", "LanguageRuntime.Create", "41", "42"]:
    assert anchor in slide11, f"slide 11 no longer matches demo: {anchor}"
for stale in ["MinimalArithmeticId", "40 + 2", "6 * 7", "real Wist dialect"]:
    assert stale not in slide11, f"stale Wist demo claim remains on slide 11: {stale}"

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

for forbidden in [
    "zero-cost extensibility",
    "all abstractions disappear",
    "general equality saturation engine",
]:
    assert forbidden.lower() not in " ".join(text for _, text in main).lower(), f"forbidden live claim: {forbidden}"

assert "Build the Language, Then Make the Abstractions Disappear" not in html
assert "balanced-causal-v2" in (root / "deck.js").read_text(encoding="utf-8")
assert "speaker-notes-1.js" in html and "speaker-notes-2.js" in html and "speaker-notes-hardening.js" in html

print(
    f"OK: {len(main)} main, {len(appendix)} appendix, {len(all_keys)} note keys, "
    f"{words} live cue words; demo/source consistency PASS"
)
