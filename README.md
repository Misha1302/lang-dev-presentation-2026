# LangDev 2026 — UniversalToolchain presentation

Reworked conference deck for the accepted talk title:

> Build the Language, Then Make the Abstractions Disappear

Central thesis:

> Modules keep local knowledge; the planner owns global composition decisions.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard:

- `←` / `→` / space — navigate
- `N` — speaker notes
- `T` — table of contents
- `A` — include appendix slides
- `F` — fullscreen
- `P` — print

## Validate

```bash
python3 scripts/check_deck.py
node --check deck.js
python3 scripts/check_render.py
```

## Narrative contract

The deck deliberately starts with the strongest baseline: a single known language can often use an explicit host pipeline. The planner appears only after independent extensions introduce global composition decisions: provider ambiguity, artifact routing, ordering, conflicts, backend/runtime selection and early diagnostics.

The accepted title is preserved. The “abstractions disappear” payoff is scoped: planning collapses local possibilities into stable facts, and some generic execution/IR machinery can leave the hot path when those facts are static. The deck does not claim universal zero-cost extensibility or performance wins without measurements.
