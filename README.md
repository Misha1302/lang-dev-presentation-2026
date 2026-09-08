# LangDev 2026 — Extensible Programming on .NET

Conference talk:

> **Author language pieces. Resolve one compiler. Keep useful meaning.**

The talk asks one compiler-architecture question:

> How can independently developed language capabilities form concrete language profiles, resolve into one compiler plan, and still expose current-valid semantic knowledge when later optimizations need non-local facts?

UniversalToolchain/Wist is a bounded **implementation witness**. It is not the ontology of the general architecture.

## Main narrative

The Phase-04 main deck is **32 slides**. It is one causal argument:

1. A monolithic compiler is the baseline; extensibility earns its cost only when reuse, variation or independent ownership matters.
2. A language capability can span several compiler layers. A **language capability** is reusable authored inventory; a **language profile** is one concrete configuration selecting capabilities, policy and targets.
3. Independent development means targeting published ecosystem contracts rather than private pairwise APIs. Broad modular language composition is prior art, not the novelty claim.
4. A profile declares **WHAT** language is wanted; composition/planning resolves **HOW** to assemble it. MLIR is strong prior art and may be a subsystem inside that answer.
5. UT witnesses request → resolution → snapshotted plan → runtime staging. The current route-order regression establishes **structural feasibility before preference**, not semantic preservation.
6. Freezing one composition answer removes global discovery/replanning from the already-resolved repeated path while leaving per-program compiler work intact.
7. Current UT supplies one strong local deabstraction witness: an exact three-operation AIR external-load sequence becomes one typed intrinsic when its local capability gate holds.
8. The causal question then changes: what if optimization legality needs non-local facts? Bounds-check elimination motivates `SafeIndex(a,i)` from independently produced range and extent evidence.
9. A semantic query is a typed proposition with distinct `unsupported`, `unknown`, `established(P)`, `refuted(P)` and `contradictory` outcomes. Side conditions and validity determine whether evidence may discharge the proposition.
10. LLVM AnalysisManager/PreservedAnalyses and MLIR interfaces/external models/effects/data-flow are the serious baseline. The narrower hypothesis is a minimal cross-component, cross-representation lifecycle for semantic evidence identity, validity, assumptions and evidence.
11. Modularity is not soundness: contradictory or stale evidence fails closed. `Write(place,value)` supplies a second domain and keeps source/operation semantics separate from runtime/JIT obligations such as a CoreCLR GC write barrier.
12. `Judgement` names a proposition plus the context that makes its evidence usable. `Obligation` names the proposition a transformation owns and must establish before it is legal.
13. Representation and knowledge are separate axes. A later-used fact must be transported under a justified semantic correspondence, re-analysed, or invalidated.
14. LLVM/MLIR, CompCert, translation validation and Alive2 set the prior-art/correctness bar. The strongest alternative is to keep local interfaces, analyses and adapters and reject the shared layer if it adds no measurable benefit.
15. The primary experiment measures false obligation discharges, existing-consumer edits, integration edges, precision, invalidation/re-analysis cost and schema/version burden.
16. Final synthesis: **AUTHOR → RESOLVE → OPTIMIZE**. “Meaning” means selected current-valid semantic knowledge needed by later compiler decisions, not permanent preservation of every source representation.

The appendix is **12 slides** containing UT-specific vocabulary/configuration/planner details, bounded reflection, backend parity, evidence-contract detail, MLIR/LLVM Q&A, benchmark publication requirements, the concrete minimal profile, the second local rewrite, the inheritance cross-product warning and formal correctness baselines.

## Stable vocabulary

- **language capability** — reusable authored compiler contribution developed against published ecosystem contracts;
- **language profile** — one concrete language configuration selecting capabilities, restrictions, policy and targets;
- **feasible plan** — a plan whose declared structural requirements hold; this does not imply semantic preservation;
- **semantic query** — a typed proposition asked by a consumer about the current program state;
- **Judgement** — proposed evidence object: subject/proposition + result state + context/revision + assumptions + evidence;
- **Obligation** — proposition owned by a transformation that must be established before that transformation is legal;
- **semantic correspondence** — a justified relation describing which property of an old program state remains true of the transformed state; refinement is a stronger directional relation.

## Evidence boundaries

**IMPLEMENTED WITNESS:** declarative Wist profiles; staged UT planning; the tested cost-2-vs-cost-10 structural route regression; local typed-intrinsic deabstraction; selected backend parity; benchmark methodology boundary.

**GENERAL DESIGN:** language capability/profile split; WHAT/HOW ownership; one inspectable compiler plan; open-world composition vs repeated per-program work; structural feasibility distinct from semantic preservation.

**RESEARCH HYPOTHESIS:** the shared semantic-evidence lifecycle, conservative contradiction handling, transformation-owned obligations, and cross-representation transport/re-analysis/invalidation. Generic queries, invalidation, effect interfaces and semantic correspondence are prior art ingredients rather than novelty claims.

## Files

- `deck-main.js` — 32-slide main causal argument;
- `deck-appendix.js` — 12-slide evidence/Q&A appendix;
- `speaker-script-canonical.js` — single canonical spoken owner for all main and appendix slides;
- `CONTENT_NARRATIVE_CONTRACT.json` — semantic milestones and causal DAG;
- `claims.md` — scientific/claim boundary owner from Phase 03;
- `CONTENT_EVIDENCE_LEDGER.md` — implementation/prior-art evidence owner from Phase 02.

## Deferred work

Phase 04 does **not** optimize stage timing or redesign visuals. Numerical C#↔Wist performance claims remain withheld until current raw Release evidence is archived and reviewed. Visual/layout work and any separate timing campaign begin only after content finalization.

## Validate

```bash
python3 scripts/check_deck.py
for file in deck.js deck-*.js speaker-script-*.js; do node --check "$file"; done
python3 scripts/timing_audit.py
python3 scripts/check_render.py
```

Normal CI also checks the current UniversalToolchain `master` witness for pricing/backend parity, the local typed-intrinsic rewrite, the route-order regression and the benchmark evidence boundary.

## 2026-09-08 additive measured-evidence layer

The Phase-04 authored files above remain intact. `deck-research-update.js` adds **7 runtime main slides** and reorders those additions around the existing slides before `deck.js` snapshots navigation. The visible main deck is therefore **39 slides** while `deck-main.js` itself remains the original 32-slide authored causal argument.

The new slides insert measured evidence from the reproducible UniversalToolchain DSL-evolution study: observed DSL evolution, the clone/platform trade-off, the frozen experiment design, the E2 marginal-vs-total crossover, the failed E3 propagation hypothesis, the separate RQ3 shared-pipeline control, and an explicit boundary between the completed reuse-economics experiment and the still-proposed semantic-evidence experiment.

`speaker-script-research-update.js` extends `window.SPEAKER_SCRIPT` only for the seven new `r1..r7` slides. Existing entries in `speaker-script-canonical.js` are not edited or shortened. The additive speech is capped at 95 words by `scripts/check_research_insertion.py` so the prior 26:18 baseline remains close to the existing 27-minute ceiling without modifying old speech.

See `RESEARCH_EVIDENCE_UPDATE_2026-09-08.md` for the insertion order, evidence sources and protected-content contract.
