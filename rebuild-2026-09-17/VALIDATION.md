# VALIDATION — LangDev presentation rebuild 2026-09-18 fix

## What is now production

- `index.html` now routes the default presentation entrypoint to `rebuild-2026-09-17/delegates-rebuild-deck.html`.
- The validation record now describes only files that exist in this PR and checks that are actually wired into repository CI.
- The self-contained deck remains the Delegates × multiple type-semantics rebuild with a complete `speaker-script-conference.md` and explicit TARGET / RESEARCH HYPOTHESIS boundaries.

## Repository checks on this branch

- `python3 scripts/check_deck.py` — validates the production route, required narrative moments, slide/script coverage, evidence boundaries, and this validation record.
- `node --check deck.js` and `node --check deck-*.js speaker-script-*.js` — verifies retained JS assets remain syntactically valid.
- `python3 scripts/timing_audit.py` — verifies the complete speaker script is present and within a concise conference range.
- `python3 scripts/check_render.py` — parses the deck and captures Chrome smoke screenshots when Chromium is available.

## Narrative gate

- Concrete programmer code appears on slide 2.
- `Delegates` is treated as a source-language feature, not a compiler plugin.
- Scenario A and Scenario B are separated.
- Pairwise hardcoding and a giant `ITypeSystem` are both attacked before introducing semantic capabilities.
- Global/profile-time resolution is separated from local/per-program proof obligations.
- Structural composition is not claimed to imply semantic correctness.
- Unsupported, unknown, refuted and contradictory evidence fail closed.
- The before/after slide shows generic delegate machinery becoming a direct call only under explicit obligations.
- Prior art is framed as a serious threat; UT is an implementation witness, not the thesis.

## Remaining limitation

- `Delegates × multiple independently authored type semantics` remains TARGET / RESEARCH HYPOTHESIS, not an implemented UniversalToolchain claim.
