# Research evidence update — 2026-09-08

This update is intentionally **additive-only** for authored presentation content.

## User constraint

- Do not delete an existing slide.
- Do not delete or shorten existing canonical speaker text.
- New slides may be added.
- Existing slides may be reordered.

The implementation therefore leaves `deck-main.js`, `deck-appendix.js`, and `speaker-script-canonical.js` unchanged. `deck-research-update.js` adds seven slides and moves them into the runtime main-deck order before `deck.js` snapshots the slide list. `speaker-script-research-update.js` extends the existing `window.SPEAKER_SCRIPT` object without editing old entries.

## Added evidence arc

1. `r1` after `m3`: DSL evolution is an observed problem, not a hypothetical premise.
2. `r2` after `r1`: strongest literature baseline — clone-and-own versus explicit/platform reuse is an upfront-versus-repeat-cost trade-off.
3. `r3` after `r2`: frozen experiment design using fixed control, fair clone-and-own, and current UT composition.
4. `r4` after `r3`: measured E2 result — UT has lower marginal feature SLOC (19 vs 35), while cumulative footprint is still larger (105 vs 61).
5. `r5` after `r4`: measured E3 negative result — both strengthened treatments change one logical site / one file / seven LOC.
6. `r6` after `m12`: RQ3 downstream control — ordinary shared pipeline and UT both reuse downstream logic locally; shared pipeline changed 3 LOC, UT 5 LOC, with zero variant-semantic files touched.
7. `r7` after `m25`: explicit boundary between completed reuse-economics experiment and the existing proposed semantic-evidence experiment.

## Why this reorder

The audience now sees measured economics **before** the architecture is asked to justify itself. `m5/m7/m11/m12` become an architectural response to an observed reuse problem rather than an assumed need. `r6` makes the MLIR comparison stronger by first conceding experimentally that shared downstream infrastructure is not unique to source-language extensibility. `r7` prevents the completed DSL-evolution experiment from being misread as evidence for the later semantic-evidence lifecycle hypothesis.

## Timing discipline

The seven new speaker entries are deliberately short. `scripts/check_research_insertion.py` caps the additive speech at 95 words so the prior 26:18 / 3415-word main-script baseline can remain near the existing 27-minute ceiling without editing old speech.

## Evidence

- Zhang, Strüber & Hebig, *Empirical Software Engineering* (2026), DOI `10.1007/s10664-025-10775-2`.
- Krüger & Berger, ESEC/FSE 2020, DOI `10.1145/3368089.3409684`.
- Bertolotti, Cazzola & Favalli, *Journal of Systems and Software* 202 (2023), DOI `10.1016/j.jss.2023.111704`.
- UniversalToolchain DSL evolution study: branch `research/dsl-evolution-experiment-2026-09-08`.
- Primary results: `internal-docs/research/dsl-evolution-study/RESULTS.md`.
- RQ3 results: `internal-docs/research/dsl-evolution-study/RQ3_RESULTS.md`.

## Protected-content validation

`python3 scripts/check_research_insertion.py` compares the protected authored files against the PR merge-base with `origin/main`, validates all seven new slide/speech keys, validates runtime reorder edges and load order, and enforces the additive speech budget.
