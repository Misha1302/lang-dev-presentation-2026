# LangDev 2026 presentation

Current conference presentation website for **Build the Language, Then Make the Abstractions Disappear**.

The repository was intentionally flattened on 2026-09-20: the previous slide-deck implementation, legacy deck scripts/styles, old speaker-script overlays, demo subtree, and superseded rebuild files were removed and replaced by the current vertical narrative site.

## Run

Serve the repository root with any static HTTP server and open `index.html`.

For a portable single-file copy, open `langdev-talk-standalone.html`.

## Navigation

The main narrative uses slide-by-slide vertical paging:

- wheel / trackpad: one page per gesture;
- `ArrowDown`, `PageDown`, `Space`, `J`: next page;
- `ArrowUp`, `PageUp`, `Shift+Space`, `K`: previous page;
- touch swipe: one page;
- chapter links: exact scene starts.

Long semantic scenes get additional viewport-sized page stops so content is not skipped. The appendix returns to ordinary continuous scrolling. `prefers-reduced-motion` disables animated transitions while preserving paging.

## Files

- `index.html` — canonical GitHub Pages entry point.
- `styles.css` — visual system.
- `script.js` — interactions, paging, progressive states.
- `langdev-talk-standalone.html` — exact single-file build.
- `QA_REPORT.md` — browser verification for the current paging revision.
