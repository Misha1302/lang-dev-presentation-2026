# LangDev 2026 — UniversalToolchain talk

Conference HTML deck for **Build the Language, Then Make the Abstractions Disappear**.

Published deck: https://misha1302.github.io/lang-dev-presentation-2026/

Main project: https://github.com/Misha1302/UniversalToolchain

## Controls

- `←` / `→`, `PageUp` / `PageDown`, `Space`: navigate the current section.
- `Home` / `End`: jump to the first / last slide of the current section.
- `F`: fullscreen.
- `N`: speaker notes.
- `A`: toggle the Q&A appendix. The main talk remains 15 slides; the appendix is separate.
- Direct links: `#1` … `#15`, and `#A1` … `#A4` for appendix slides.

## Live demo

Use the rehearsed commands in [`DEMO.md`](DEMO.md). They are sourced from shipped UniversalToolchain example READMEs; the main talk has a demo checkpoint on slide 11.

## Validation

`python3 scripts/check_deck.py` validates the authored slide contract and source-of-truth invariants. `node --check deck.js` validates JavaScript syntax. `python3 scripts/check_render.py` opens every main and appendix slide in headless Chrome at **1920×1080** and **1366×768**, rejects viewport overflow or source/control overlap, and captures representative screenshots.

All three checks run in GitHub Actions on pushes and pull requests; render screenshots are uploaded as a workflow artifact.

The talk deliberately avoids historical performance percentages unless they are re-established with a current reproducible benchmark and semantic-parity precheck.
