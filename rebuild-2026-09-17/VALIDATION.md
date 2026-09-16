# VALIDATION — LangDev presentation rebuild 2026-09-17

## Checks run locally

- `node --check rebuild-2026-09-17/rebuild-deck.js` — PASS.
- `node --check rebuild-2026-09-17/speaker-script-canonical.js` — PASS.
- `node --check deck.js` — PASS.
- `node scripts/validate-rebuild.mjs` — PASS: 21 main slides, 4 appendix slides, 25 speaker-script entries.
- Rendered `render/langdev-delegates-rebuild-2026-09-17.pdf` with WeasyPrint from the same deck HTML source — PASS.
- Exported visual smoke PNGs for slides 1, 2, 7, 13, 17, 21 with `pdftoppm` — PASS; representative slides visually inspected.

## Narrative gate

- Concrete programmer code appears on slide 2, inside the first 90 seconds of the script.
- `Delegates` is treated as a source-language feature, not a compiler plugin.
- Scenario A and Scenario B are separated.
- Pairwise hardcoding and a giant `ITypeSystem` are both attacked before introducing semantic capabilities.
- Global/profile-time resolution is separated from local/per-program proof obligations.
- Structural composition is not claimed to imply semantic correctness.
- Unsupported, unknown, refuted and contradictory evidence fail closed.
- The before/after slide shows generic delegate machinery becoming a direct call only under explicit obligations.
- Prior art is framed as a serious threat; UT is an implementation witness, not the thesis.

## Exact blockers / limitations

- Existing repository validators from `scripts/check_deck.py`, `scripts/timing_audit.py`, and `scripts/check_render.py` were not run against a full local clone because this execution container could not resolve/clone GitHub. The connected GitHub API was used for repository read/write instead.
- Chromium/Playwright navigation to local files/localhost was blocked in this environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), so the rendered PDF was produced via WeasyPrint and visual PNG smoke checks via `pdftoppm`.
- Delegates × multiple independently authored type semantics remains labeled TARGET / RESEARCH HYPOTHESIS, not an implemented UT claim.
