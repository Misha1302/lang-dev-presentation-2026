from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")
JS = (ROOT / "deck.js").read_text(encoding="utf-8")

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.main = 0
        self.appendix = 0
        self.slides_without_notes = 0
        self.imgs_without_alt = 0
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        element_id = data.get("id")
        if element_id:
            self.ids.add(element_id)
        classes = set((data.get("class") or "").split())
        if tag == "section" and "slide" in classes:
            if not (data.get("data-notes") or "").strip():
                self.slides_without_notes += 1
            kind = data.get("data-kind")
            if kind == "main":
                self.main += 1
            elif kind == "appendix":
                self.appendix += 1
            else:
                errors.append("slide without explicit data-kind")
        if tag == "img" and not (data.get("alt") or "").strip():
            self.imgs_without_alt += 1


parser = DeckParser()
parser.feed(HTML)

require(parser.main == 15, f"expected 15 main slides, found {parser.main}")
require(parser.appendix == 4, f"expected 4 appendix slides, found {parser.appendix}")
require(parser.slides_without_notes == 0, f"{parser.slides_without_notes} slides are missing speaker notes")
require(parser.imgs_without_alt == 0, f"{parser.imgs_without_alt} images are missing alt text")

for required_id in {"deck", "prev", "next", "counter", "appendixToggle", "fullscreen", "notesToggle", "notesPanel", "notesText"}:
    require(required_id in parser.ids, f"missing required id: {required_id}")

for token in [
    "Mikhail Razakov",
    "Variables",
    "CSharpInterop",
    "MPS",
    "MontiCore",
    "LIVE DEMO",
    "qr-universaltoolchain.svg",
]:
    require(token in HTML, f"missing required content token: {token}")

for forbidden in ["innerHTML", "outerHTML", "previousTransitions"]:
    require(forbidden not in JS, f"deck.js must not mutate authored slide content via {forbidden}")

require("isInteractiveTarget" in JS, "keyboard handler must guard interactive elements")
require("data-kind=\"appendix\"" in HTML, "appendix slides missing")
require(re.search(r"\.sources\{[^}]*font-size:clamp\(12px", CSS) is not None, "source footer minimum font size regressed below 12px")
require("overflow:hidden" in CSS, "viewport overflow contract missing")

try:
    ET.parse(ROOT / "qr-universaltoolchain.svg")
except Exception as exc:  # noqa: BLE001
    errors.append(f"QR SVG is not valid XML: {exc}")

if errors:
    print("Deck contract FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"Deck contract OK: {parser.main} main slides + {parser.appendix} appendix slides")
