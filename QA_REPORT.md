# LangDev 2026 — production narrative and browser QA

Reviewed 2026-10-08 against baseline main `128d6f910d35f2aebedd95a3efd432be9a019ea9`.
Production artifact: `index.html`, SHA-256 `ee97af4e975e71b2cb939a1f214428b58ff2ee7724f110941f21cac11afdd6cc`.

## Result and scope

Targeted repairs preserve 18 slides, 1290 seconds (21:30) and the six-minute proposed research outlook. No compiler source, dependency, visual framework or deployment workflow was changed. The complete causal diagnosis, first-use terminology map, alternative repairs and per-slide argument are in REBUILD_EVIDENCE.md, section “2026-10-08 narrative and cognitive investigation”.

The suspected vocabulary gap was real at the first derivation, but a new glossary slide was unnecessary: the optimizer question and conservative fallback were already visible on slide 10. The repaired DAG teaches its roles in that same running example. Source-backed implementation claims, prior-art comparison and the return to the main thesis were retained.

## Repairs

- Slides 6–7: expand AIR locally and synchronize actual SAY cues with semantic binding and host binding-slot motivation.
- Slide 9: avoid assuming listeners already understand premises; preserve explicit proposal boundary.
- Slide 10: name the obligation as required legality and make type/lane/bounds/trap/tail assumptions explicit.
- Slide 11: annotate producers and R1/R2, require all incoming premises, define evidence contextually, identify the arithmetic computation, and bound proof to derivation rather than provider correctness. Its existing title is shortened to make space; original graph topology and colors remain.
- Slides 12–13: keep query/rules fixed, identify new valid facts as the change, use consistent property names and identify shared rule ownership. No unconditional truth from adding a module.
- Slide 14: distinguish explicit negative evidence from missing proof, identify a provenance excerpt, and make loss of the answer conditional on no alternative valid proof.
- Slide 18: remove browser-width media queries inside the uniformly scaled fixed stage. All four QRs now remain visible at 1024×768 and portrait widths.
- README/runbook: synchronize actual SAY/NEXT interface, 18-slide handoff and timing. Detailed hidden notes remain available in source.
- Validator: test visible notes rather than a hidden legacy clone, enforce unchanged timing, cover every projector size, all changed reveals at smaller sizes, all-slide non-16:9 geometry and all slides offline.

## Executed final validation

Command: `python scripts/validate_deck.py --output qa/final`.

| Check | Observed result |
|---|---|
| Slides / total timing / research timing | 18 / 1290 s / 360 s |
| Default screenshots | 72: every slide at 1600×900, 1920×1080, 1536×864, 1366×768 |
| Required projector combinations | 54 / 54 captured and visually reviewed |
| Responsive screenshots | 72: all slides at 1280×720, 1024×768, 1280×900, 390×844 |
| Logical reveal states / captures | 56 / 176 |
| Reveal coverage | All states at 1600 and 1920; changed slides at 1536 and 1366 |
| JavaScript errors / geometry groups | 0 / 0 |
| Embedded fonts | Seven faces loaded, also explicitly loaded offline |
| Navigation | Keyboard, buttons, dots, canonical/numeric hashes, wheel, touch passed |
| Presenter/help | Visible SAY/tail and P dismissal on all 18; H dismissal passed |
| Local/offline | All 18 slides opened offline; four embedded QR images loaded |
| Printing | PDF generated |

An additional final browser capture under `qa/final-visual` covers 108 viewport/slide combinations and 26 research/adjacent reveal states, plus the actual slide 11 presenter overlay. It also observed zero geometry and JavaScript errors. Final source hashes are recorded in `qa/final/validation.json` for HTML, runbook and validator, so these results identify the release candidate rather than an earlier revision.

Final full-slide contact sheets at all three required projector sizes were visually reviewed. Titles, code, proof labels, contrast and layout remain coherent; no clipping or overlap was observed. Intermediate candidate and baseline research reveals were reviewed during the investigation. The user then explicitly requested skipping further checks: the remaining manual review of **every final changed reveal screenshot** and additional standalone adversarial pass were therefore not completed. Automated final reveal geometry did pass. This is a review limitation, not a claim of complete manual reveal QA or human usability testing.

No comprehension score or measured delivery-time claim is made. The allocation gives the first derivation 80 seconds by moving 15 seconds from repeated research narration, without changing total duration.

## Before/after and remaining boundaries

The optimizer question now precedes contextual definitions; producers, required premises and derived conclusion are visible together. Evidence authority, fixed rules, negative evidence and alternative-proof invalidation are explicit. The non-16:9 contact clipping reproduced in baseline is absent in final automated geometry.

Slides 1–5, 8, 15–17 retain their audience-facing content. Slide 8 has only an updated transition cue. The research layer and SIMD remain proposed/illustrative; legality is bounded by fixed assumptions and separate from profitability. No speedup, formal completeness or shipped vectorizer is asserted. Compiler execution results in the older evidence record were not rerun; pinned source contracts were inspected read-only.

CI/deployment conclusions must be taken from the runs for the published commit, not inferred from this local report.
