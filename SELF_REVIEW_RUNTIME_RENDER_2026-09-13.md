# Self-review: runtime render validation cost fix

## What changed

- `scripts/check_render.py` still reads the final runtime manifest from browser-executed DOM.
- Every runtime slide is still checked in audience and presenter mode at `1366x768`.
- Every runtime slide still gets canonical audience and presenter screenshots.
- Extra screen sizes are sampled by semantic risk instead of brute-forcing all slides at all geometries.

## Why this is safe

The original defect was not lack of brute force; it was the wrong source of truth. The old static approach counted literal `data-kind` strings before runtime mutations and could check nonexistent hashes while missing runtime-demoted appendix slides. The corrected source of truth remains the executed DOM manifest.

## Strongest objection

Sampling extra geometries can miss a responsive-only issue on a low-risk slide. That is accepted because canonical visibility is still complete, and the extra geometry sample includes semantic milestones and the previously risky late architecture cluster.

## Validation target

Expected CI output should report runtime main/appendix counts, canonical screenshots for every runtime slide, full canonical audience/presenter states, sampled extra geometry states, and navigation/presenter sync PASS.
