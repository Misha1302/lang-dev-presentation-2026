# Runtime-validated LangDev deck research update — 2026-09-13

## Source of truth

Remote `main` reviewed at `a4ba28ef1b911aa86b163710c89694514ee48217`.
The local clone had a newer unpushed commit, but `git ls-remote origin refs/heads/main` showed that remote `main` remained at `a4ba28e`; the newer local commit was therefore excluded as a source of truth.

## Prior-art update

The strongest baseline is not plain “MLIR dialects”. It is MLIR with dialect interfaces, op/type interfaces, external models, data-flow analysis, effects, conversion legality, Transform dialect, and ordinary explicit adapters.

Consequence: “a producer can strengthen an existing consumer through a common contract” is not a sufficient novelty claim. MLIR already supports decoupling transformations/analyses from concrete operations through interfaces and external models, and its data-flow utilities support analysis facts over rich IR/control-flow structures.

The defendable UT claim is narrower:

> Can a framework-level lifecycle for evidence pay for itself across heterogeneous compiler representations and engines that do not all live inside one shared MLIR object model?

## Presentation changes applied

- Moved the external MLIR overhead benchmark out of the opening sequence and next to the adapter/cost discussion.
- Simplified the architecture cluster that previously overloaded slides 45–49.
- Replaced dense “current vs target / meta-kernel / packages / MLIR comparison / falsification” slides with fewer large claims and equal visual treatment.
- Shortened long presenter notes for architecture and prior-art slides.
- Preserved the scientific boundary: current planning witness, measured small DSL-evolution study, and open semantic-evidence hypothesis remain separate.

## CI/runtime fixes

### Render coverage

Old `check_render.py` counted `data-kind="main"` with regex over source fragments before runtime mutation. That produced a static count that did not match the final DOM after `deck-narrative-reframe.js` demoted/reordered slides.

New `check_render.py` discovers the final slide order from the executed browser DOM and verifies that each visited hash activates the expected unique `data-note-key`. This closes the “#53 clamps to last slide” false-pass gap.

### Timing coverage

Old `timing_audit.py` reconstructed only 32 authored slides plus 7 research slides. The final runtime deck has 52 main slides.

New `timing_audit.py` parses `FINAL_MAIN_ORDER`, evaluates the runtime speaker-script overlay stack, checks every runtime main key, and times the actual final script.

## Local validation

- `python3 scripts/check_deck.py` — PASS.
- `python3 scripts/timing_audit.py` — PASS: 52 runtime main slides, 3029 spoken words, 23:17 at 130 wpm, per-slide range 18–43 seconds.
- Browser visual audit rendered all 52 final main slides at 1366×768 with Playwright/Chromium and checked each hash activates the expected unique slide key.

The committed CI render check still runs the fuller audience/presenter geometry and screenshot matrix on GitHub runners where Chrome/Chromium is available.

## Remaining risk

The central research claim is still open. The next decisive experiment should compare shared evidence lifecycle against MLIR/LLVM-style local analyses plus explicit adapters, measuring consumer edits, producer-specific adapters, precision, false discharges, compile time, memory, invalidation/re-analysis cost, and schema/version burden.
