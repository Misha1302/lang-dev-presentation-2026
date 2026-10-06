# LangDev 2026 — Open to extension. Concrete at execution.

The production presentation is **index.html**: a self-contained, offline-capable 16:9 HTML deck with 17 slides and a **21:00 rehearsal allocation**, excluding audience Q&A. Open it directly in a browser; no installation, installed fonts, CDN or server is required. Inter and renamed Liberation Mono subsets are embedded as WOFF2 data URLs, with SIL OFL licenses included in the HTML. The live production entrypoint is https://misha1302.github.io/lang-dev-presentation-2026/.

The accepted talk title is **“Build the Language, Then Make the Abstractions Disappear: Extensible Programming on .NET.”** The shorter on-slide thesis is **“Open to extension. Concrete at execution.”**

The narrative follows real Wist source through modular composition, one immutable LanguagePlan, Bytecode/AIR and interpreter/CIL execution. A tested external-binding regression motivates a clearly separated **6:00 research outlook** on typed semantic evidence, illustrated with one conceptual SIMD scenario. No production SIMD, formal completeness, measured speedup or novelty claim is made.

For last-mile rehearsal, use the deployed companion runbook: https://misha1302.github.io/lang-dev-presentation-2026/speaker-runbook.html. It keeps slides 9–15 framed as a short research outlook rather than a second full talk.

## Navigation

- `→`, `↓`, `PageDown`, `Space`, `J`: next slide, or next reasoning step in reveal mode.
- `←`, `↑`, `PageUp`, `Shift+Space`, `K`: previous slide.
- `R`: toggle staged reveals; `A`: reveal the complete current slide.
- `P`: presenter notes in ANCHOR / FLOW / TRANSITION form; `H`: help; `F`: fullscreen.
- `Home` / `End`: first / last slide. Buttons and left-side dots also navigate.
- Wheel/trackpad and touch swipe advance one step per gesture.
- Canonical hashes: `#slide-1` … `#slide-17`; numeric `#1` … `#17` links also work.

The deck scales uniformly and letterboxes non-16:9 viewports. Browser printing produces one slide per page. All meaningful type is at least 16px in the 1600×900 design coordinates; code is 23–40px.

## Reproducible QA

```bash
python -m pip install -r scripts/requirements.txt
python -m playwright install chromium
python scripts/validate_deck.py --output qa/final
```

The validator exercises the actual production DOM, captures every slide at 1600×900 and 1920×1080, captures every reveal state, checks typography/geometry and navigation, tests direct local-file loading, and creates a PDF and contact sheets. Human screenshot inspection is still required; see QA_REPORT.md for the completed review.

REBUILD_EVIDENCE.md records pinned compiler sources, implementation/proposal boundaries, the git-history investigation and each slide's causal narrative. Generated QA artifacts live in `qa/` and are ignored by Git. Compiler sources are unchanged.
