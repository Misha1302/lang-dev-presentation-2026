# VALIDATION — LangDev presentation rebuild merge gate

## Production candidate

- `index.html` routes the default presentation entrypoint to `rebuild-2026-09-17/delegates-rebuild-deck.html`.
- The rebuilt deck is the Delegates × multiple type-semantics conference story.
- `speaker-script-conference.md` is the complete synchronized main-talk script; timing is checked at 130 wpm against a 22–25 minute contract.
- `Delegates × multiple independently authored type semantics` remains TARGET / RESEARCH HYPOTHESIS, while UniversalToolchain is used only as a bounded implementation witness.

## Required repository checks

- `python3 scripts/check_deck.py` — production route, required narrative moments, slide/script coverage and overclaim guards.
- `node --check deck.js` and `node --check deck-*.js speaker-script-*.js` — retained JavaScript syntax.
- `python3 scripts/timing_audit.py` — complete script and 22–25 minute conference range.
- current UniversalToolchain checkout + benchmark-boundary assertions.
- current pricing demo and interpreter/CIL parity witness, including no-build rerun.
- targeted UT tests for local deabstraction and route-order feasibility.
- `python3 scripts/check_render.py` — every rebuilt slide must navigate to the expected active slide, synchronize notes, and render at the canonical aspect ratio; representative slides are also rendered at 1280×720 and 1920×1080.
- `python3 scripts/check_production.py` on `main` pushes — exact deployed `index.html` and rebuilt deck hashes must match the merged revision, every slide hash-navigation state is replayed, and representative production screenshots are captured.
- `Research Insertion Guard` must pass in rebuild mode.

## Narrative gate

- Concrete programmer code appears on slide 2, inside the first 90 seconds of the script.
- `Delegates` is treated as a source-language feature, not a compiler plugin.
- Scenario A and Scenario B are separated.
- Pairwise hardcoding and a giant `ITypeSystem` are both attacked before semantic capabilities are introduced.
- Global/profile-time resolution is separated from local/per-program proof obligations.
- Structural composition is not claimed to imply semantic correctness.
- Unsupported, unknown, refuted and contradictory evidence fail closed.
- The before/after slide shows generic delegate machinery becoming a direct call only under explicit obligations.
- Prior art is framed as a serious threat; ordinary adapters/workbenches/MLIR-style mechanisms are conceded where sufficient.
- UT is an implementation witness, not the thesis.

## Remaining research boundary

The cross-type-system Delegates capability contract and full evidence lifecycle are not claimed as implemented UT functionality. They remain the research target to validate or falsify.
