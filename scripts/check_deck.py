#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text(encoding="utf-8")

class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self._in_section = False
        self._depth = 0
        self._buf = []
        self._attrs = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and "slide" in attrs.get("class", ""):
            self._in_section = True
            self._depth = 1
            self._buf = []
            self._attrs = attrs
            return
        if self._in_section:
            self._depth += 1
    def handle_endtag(self, tag):
        if self._in_section:
            self._depth -= 1
            if self._depth == 0 and tag == "section":
                text = " ".join("".join(self._buf).split())
                self.slides.append((self._attrs, text))
                self._in_section = False
    def handle_data(self, data):
        if self._in_section:
            self._buf.append(data)

p = SlideParser(); p.feed(html)
slides = p.slides
main = [s for s in slides if s[0].get("data-kind") != "appendix"]
appendix = [s for s in slides if s[0].get("data-kind") == "appendix"]
assert len(main) >= 14, f"expected at least 14 main slides, got {len(main)}"
assert len(appendix) >= 3, f"expected appendix slides, got {len(appendix)}"
for n, (attrs, text) in enumerate(main, 1):
    assert "data-notes" in attrs and len(attrs["data-notes"]) > 80, f"main slide {n} missing detailed notes"
    for marker in ["ЗАЧЕМ", "СКАЗАТЬ", "ПЕРЕХОД"]:
        assert marker in attrs["data-notes"], f"main slide {n} notes missing {marker}"
required = [
    "For one language", "Local extensibility creates", "Two providers", "type-compatible route",
    "LanguagePlan", "Runtime executes", "stable facts", "Demo", "Prior art", "When does a planner pay",
    "Composition protocol", "Structural compatibility", "Keep local knowledge local"
]
full = re.sub(r"\s+", " ", html)
missing = [r for r in required if r not in full]
assert not missing, f"missing narrative elements: {missing}"
assert "all extensibility is free" not in full.lower(), "avoid universal free-extensibility wording"
assert "appendixBtn" in html, "appendix toggle missing"
print(f"OK: {len(main)} main slides, {len(appendix)} appendix slides")
