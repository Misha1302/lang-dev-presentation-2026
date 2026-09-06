# LangDev 2026 — Extensible Programming on .NET

Conference talk:

> **Author many language pieces. Resolve one compiler. Keep the meaning.**

The talk is a compiler-architecture argument grounded by current UniversalToolchain/Wist evidence and constrained by `CONTENT_EVIDENCE_LEDGER.md`.

Its central question is narrower than “can languages be extended?” — mature prior art already answers that in several ways:

> Can an ecosystem resolve a requested language into one declared-feasible compiler plan, then let independently authored semantic producers/consumers exchange **current-valid evidence** across changing representations without recreating pairwise coupling or pretending structural composition proves semantic correctness?

UniversalToolchain/Wist remains an **implementation witness**, not the ontology or a novelty certificate.

## Vocabulary

The main audience-facing reusable unit is a **language capability**. A concrete requested configuration is a **language profile**.

The unqualified word `dialect` is not the general abstraction. Wist `.wistdialect` is an implementation syntax; an MLIR dialect is MLIR's IR namespace/semantic-extension concept.

“Independent development” means implementing against published ecosystem contracts instead of private pairwise integration APIs. It does not promise zero coordination, arbitrary compatibility or semantic non-interference.

## Main narrative

The current main deck has 52 slides and preserves the existing slide identities/order. Phase 03 repairs the truth model rather than globally reordering the story:

1. A monolithic compiler remains the baseline. Extensibility earns its cost only when reuse, variation or independent authorship matters.
2. Language capabilities are reusable authored pieces; language profiles are concrete selections/restrictions/policies/targets. Wist `.wistdialect` is one implementation surface, not the general term.
3. Independent language-extension composition is established prior art: Silver/ableC, Neverlang, MontiCore and MPS sharply limit any novelty claim based on independent pieces or a global plan.
4. A profile declares **WHAT** is requested; planning resolves **HOW** to assemble it under published contracts. MPS generation plans and ordinary compiler pipeline builders are acknowledged prior art for global/ordered planning.
5. MLIR is a strongest baseline, not a foil: dialects, interfaces/external models, legality/conversion, effects, data-flow and programmable transformation infrastructure already cover substantial representation/semantic extensibility.
6. Current UT contributes bounded implementation evidence for a staged plan lifecycle and one route-search lesson: hard declared requirements participate before cost preference. **Structural feasibility is not semantic preservation.**
7. The freeze boundary is precise: open-world discovery/composition can terminate in one resolved plan, so it need not repeat on an already-resolved per-program path. Runtime/provider state and per-program compilation can still be mutable/costly.
8. Local deabstraction is concrete evidence: current UT has capability-gated typed-intrinsic rewrites, including the tested 3→1 external-load pattern, without turning instruction count into a performance theorem.
9. Non-local optimization motivates a semantic question such as `SafeIndex(a,i)`, but a real proof needs context/revision, mutation/extent, integer semantics, control-flow/path and assumption side conditions.
10. Generic semantic queries and invalidation are already LLVM/MLIR prior art. The research hypothesis is narrower: a versioned cross-component **semantic-evidence lifecycle** with results `unsupported`, `unknown`, `established(P)`, `refuted(P)` and `contradictory`.
11. Modularity is not soundness. Stale/unknown/unsupported/contradictory evidence cannot discharge an unsafe transformation; contradictory current-valid evidence fails closed unless a published trusted reconciliation rule exists.
12. Transformations own their legality obligations. Producers only contribute evidence; they cannot privately redefine what makes an existing transformation legal.
13. `Write(place,value)` is split into operation/source semantics (effects/resources, writability, alias/identity, visibility/order/volatility) and lowering/runtime obligations (for example CoreCLR GC barriers, target atomic/fence sequences or runtime protocols). MLIR effect interfaces are explicit prior art.
14. Across transformations, stable IDs/provenance are only helpers. For every affected later-used fact, the compiler must **transport/project**, **re-analyse**, or **invalidate** it under an explicit correspondence/refinement story. CompCert, translation validation and Alive2 are stronger correctness baselines.
15. The strongest alternative is local IR interfaces + domain analyses + pass/analysis manager + explicit adapters + local invalidation. The shared layer survives only if a comparator experiment shows fewer existing-consumer edits/integration edges without false obligation discharges and with acceptable precision, invalidation/re-analysis cost and schema/version burden.

The appendix remains 8 slides for implementation terminology/configuration, planner staging, bounded reflection, parity evidence, the evidence-validity contract, “Why not just MLIR?” Q&A and numerical benchmark publication requirements.

## Prior-art / novelty boundary

The talk does **not** claim novelty for:

- independently authored/modular language extensions or their composition;
- global/ordered generation plans;
- generic semantic interfaces/effect queries;
- cached analysis lookup and preservation/invalidation;
- semantic preservation, translation validation or refinement checking.

`CONTENT_EVIDENCE_LEDGER.md` records the reviewed primary/prior-art sources and the safe/unsafe wording boundary for Silver/ableC, Neverlang, MPS, MontiCore, LLVM, MLIR, CompCert, classic translation validation, Alive2 and CoreCLR GC barriers.

The remaining research hypothesis is deliberately narrower and is **not** presented as proven novelty.

## Structural plan vs semantic correctness

The talk uses two different notions of “legal” and keeps them distinct.

**Declared structural feasibility** means the planner found a route that satisfies the currently modeled artifact contracts, hard order/mandatory requirements and executable reachability constraints.

**Semantic preservation/correctness** means a transformation preserves or refines a defined program property/semantics. Current UT's route-order regression does not prove this stronger relation.

The callback “FEASIBILITY FIRST. PREFERENCE SECOND.” therefore means:

- cost/policy never rescue a candidate that violates a declared hard requirement;
- semantic obligations, when modeled, need separate evidence/proof/validation before they may enter the feasible set.

## Semantic evidence contract under test

For a proposition `P`, the research model distinguishes:

- `unsupported`;
- `unknown`;
- `established(P)`;
- `refuted(P)`;
- `contradictory`.

Only current-valid suitable evidence can discharge an obligation. Contradictions fail closed unless the published contract defines a trusted reconciliation rule.

The proposition/query schema itself needs ownership/versioning. Transformations own legal preconditions; producers contribute evidence under that contract.

## Cross-representation rule

For a transformation `T : r -> r'`, each affected fact that a later decision still consumes must be one of:

1. transported/projected through an explicitly justified semantic correspondence;
2. recomputed by analysis on `r'`; or
3. invalidated.

This is stronger and more operational than merely observing that inverse lowering does not generally exist. Stable identity can help map entities, but cloning, fusion, CSE, inlining, unrolling, code motion and many-to-one lowering require a semantic relation, not just an ID.

## Central synthesis

> **Extensibility should disappear where it is machinery — and survive where it is meaning.**

- **AUTHOR** — capabilities are independently developed against published ecosystem contracts; broad independent composition is prior art, not the novelty claim.
- **RESOLVE** — one language profile becomes one declared-feasible concrete plan; structural feasibility is not semantic preservation.
- **OPTIMIZE** — erase local machinery aggressively, but let transformations act only when current-valid evidence establishes the obligation; across lowering, transport, re-analyse or invalidate the facts later decisions still need.

Composition, compiler construction and compilation may still cost more. C# parity is not guaranteed.

## Evidence classes

The deck uses interpretation labels when needed:

- **PRIOR ART / VERIFIED PRIOR ART** — externally established mechanisms;
- **IMPLEMENTED WITNESS** — bounded current UT/Wist code/test evidence;
- **GENERAL DESIGN** — architectural distinctions argued by the talk;
- **RESEARCH HYPOTHESIS** — falsifiable architecture not established by current UT.

See `CONTENT_EVIDENCE_LEDGER.md` for source identity, validity boundaries, strongest alternatives and prohibited wording. See `claims.md` for the conference-facing claim contract.

## Performance evidence

The main deck contains no numerical C#↔Wist performance ratio. Current UT has a BenchmarkDotNet boundary that separates prepared execution from setup/compilation. A numerical conference claim remains withheld until a current reviewed raw Release artifact, environment metadata, source identity and correctness/parity precheck are preserved.

Instruction-count deabstraction examples are not performance ratios.

## Runtime assets

- `deck-main.js` — current 52-slide main story;
- `deck-appendix.js` — current 8-slide appendix;
- `speaker-script-canonical.js` — the single canonical stage-ready English speaker script;
- `CONTENT_NARRATIVE_CONTRACT.json` — stable semantic milestone ownership and causal DAG used by validation;
- `CONTENT_EVIDENCE_LEDGER.md` — implementation/prior-art evidence boundary;
- `deck.js` — navigation, presenter mode and runtime diagnostics;
- `presenter.css`, `styles.css`, `foundation.css`, `visual-balance.css` — presentation visual system.

Presenter mode renders only text owned by `speaker-script-canonical.js`.

## UniversalToolchain evidence policy

Conference-facing UT links intentionally point to current `master`; GitHub CI resolves and records the actual UT SHA used for each validation run. Evidence-sensitive claims remain bounded to the implementation/test identities recorded in `CONTENT_EVIDENCE_LEDGER.md`.

The deck must never turn a smoke benchmark, an instruction-count change or a remembered number into a performance result.

## Validate

```bash
python3 scripts/check_deck.py
for file in deck.js deck-*.js speaker-script-*.js; do node --check "$file"; done
python3 scripts/timing_audit.py
python3 scripts/check_render.py
```

`check_deck.py` reconstructs actual deck script load order, verifies unique slide/note identity, the stable semantic milestone DAG/evidence categories, canonical speaker ownership/coverage and the runtime QA contract. Visible English wording and an arbitrary fixed slide count are not the semantic source of truth.

`timing_audit.py` remains a separate rehearsal measurement. Content truth must not be weakened merely to satisfy a timing target.

`check_render.py` geometry-checks every discovered audience/presenter slide and captures the full rendered deck at supported viewports.

On `main`, `check_production.py` verifies exact deployed asset hashes, Pages freshness, navigation/runtime sanity and semantic milestone ownership against production assets.

Presentation CI also checks the current UT `master` witness: pricing/parity demo, typed-intrinsic local rewrite tests, route-order feasibility and benchmark-methodology boundary. It records the resolved UT witness SHA as validation evidence.
