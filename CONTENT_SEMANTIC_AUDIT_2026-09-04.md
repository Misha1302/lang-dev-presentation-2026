# Content / semantic audit — 2026-09-04

Baseline presentation: `Misha1302/lang-dev-presentation-2026@ed65ecc94970aa9902e53d034dacb93156d6c866`

Primary implementation evidence: `Misha1302/UniversalToolchain@1078ddb5b9fd83b569a8ef0e590c4bec9594e1c5`

## Verdict

The foundation-first rebuild is a clear improvement in causal order, but the deck is not yet fully correct as a technical talk. The highest-impact defect is evidential: the title payoff is currently explained mostly as an architectural/design objective, while the repository contains a concrete current deabstraction example and a concrete backend-parity boundary that are absent from the main deck. The speculative semantic-composition layer is therefore better represented than the shipped evidence that should earn the title.

The repair should preserve the new semantic-composition research layer, not roll back to the old 14-slide talk. It should insert a short repository-backed implementation bridge before the research layer, then correct the factual/semantic imprecisions below.

## Material findings and decisions

### F1 — Title payoff lacks a current implementation witness (MAJOR)

**Current deck:** slides 27–37 argue that composition can freeze and global optimization can remain possible, but no current UT transformation is shown where an abstraction actually disappears.

**Evidence:** `NativeMathModule/NativeCILOptimizerModule.cs` currently recognizes an exact `LoadEnvironment` + `Push(slot)` + generic `LoadExternal<T>` sequence and replaces it with one typed `LoadExternal<T>(slot)` intrinsic only when the backend capability supports the exact type. Tests assert the three-to-one rewrite.

**Decision:** add a short `CURRENT UT` deabstraction block before the research layer: before → known facts/legality → after; then explicitly state what disappeared and what did not. No zero-cost claim.

### F2 — Demo / narrative evidence is under-connected (MAJOR)

**Current deck:** the real demo exercises a restricted pricing profile through interpreter and CIL plus a local/external-shadowing parity regression, but the main deck does not explain backend semantic ownership/parity as a first-class current implementation boundary.

**Evidence:** `Tests/Backends/InterpreterBindingsParityTests.cs` contains the focused shadowing/nested-scope regression. The presentation demo/CI already runs that test.

**Decision:** add one concise `CURRENT UT` parity slide after deabstraction: different backend representations are allowed; re-deciding binding/storage semantics is not. Make clear that parity tests are relational evidence, not proof of equivalence.

### F3 — `exclude` is incorrectly described as subtraction (FACTUAL)

**Current slide 15:** “Extensibility includes subtraction and policy.”

**Evidence:** current dialect reference explicitly says `exclude` is a fail-closed constraint on the current definition/dependency closure and is **not** an inheritance/subtraction mechanism because the current Wist facade has no base-dialect inheritance.

**Decision:** replace “subtraction” with “constraints / negative surface / policy”. Keep the important point that selected contributions can be explicitly unavailable.

### F4 — A `LanguagePlan` is incorrectly collapsed to one backend route (FACTUAL)

**Current slide 26:** execution-time side says “one resolved graph · one concrete backend route”.

**Evidence:** `LanguagePlan.Routes` is a dictionary keyed by backend; `LanguageRuntime` verifies a route for every enabled backend, and each execution request selects one enabled backend.

**Decision:** say “one resolved graph · preplanned route for each enabled backend; each execution chooses one requested route”.

### F5 — Current UT feasibility is described too semantically (BOUNDARY)

**Current slide 34:** hard constraints include “semantic feasibility”.

**Problem:** this can be heard as “UT proves semantic preservation”. Current planner evidence is narrower: declared artifact-contract compatibility, mandatory-pass feasibility, ordering/provider constraints and ambiguity policy. The planner does not prove that two independently authored artifact contracts with matching declared identities mean the same semantics.

**Decision:** rename to “declared contract / route feasibility” or “planner-level feasibility”; add the author-declared semantic-equivalence limitation explicitly near slide 35.

### F6 — `module`, `feature`, `contribution` are not cleanly separated (SEMANTIC MODEL)

**Current slides 9/11/13:** module language mixes Wist module aliases, generic `Feature`/`Contribution`, optimizers and backends. Slide 13 says the tiny language “is four selected modules”, while the planner may close transitive dependencies and add required contributions.

**Decision:** make the taxonomy explicit:
- Wist module/profile alias = Wist-facing selectable extension unit;
- `Feature` = generic requested capability;
- `Contribution` = implementation participant;
- backend/optimizer = ecosystem component categories, not all “modules”.

Change slide 13 to “the profile requests four Wist module aliases” and note that dependency closure may add required contributions.

### F7 — The Range/Shape example assigns the wrong fact to the wrong producer (SEMANTIC)

**Current slide 43:** `RangeAnalysis` gives `0 ≤ i?`; `ShapeAnalysis` gives `i < n?`.

**Problem:** shape analysis naturally provides an extent/shape fact such as `length(a)=n`; the relation between `i` and `n` needs a join rule/query engine using both producers. The current picture hides the actual composition step.

**Decision:** use independent facts, e.g. `RangeAnalysis: 0 ≤ i ≤ 7` and `ShapeAnalysis: length(a)=10`, then an explicit contract rule/solver discharges `0 ≤ i < length(a)`. Mark the entire example `HYPOTHETICAL / PROPOSED`.

### F8 — Several research diagrams look implemented because visual boundary markers are missing (BOUNDARY)

**Affected:** the semantic-composition example, obligation→representation→route slide, and lowering/projection example.

**Decision:** add visible `PROPOSED MODEL`, `DESIGN TARGET`, or `ILLUSTRATIVE LOWERING` badges where the diagram can otherwise be mistaken for current UT behavior. Speaker-note-only disclaimers are insufficient for these slides.

### F9 — “Independent semantic dimensions” is too strong (SEMANTIC PRECISION)

**Current slide 47:** volatility, atomicity, ordering, visibility, GC barriers and transactions are presented as independent dimensions.

**Problem:** these concerns are not mutually independent; some constrain or imply others, and GC barriers are often lowering/runtime obligations rather than an object property.

**Decision:** describe them as “distinct, partially orthogonal write-semantics axes” that do not form a useful single inheritance hierarchy. Keep the operation-centric conclusion.

### F10 — Obligation→representation example mixes unlike concepts (SEMANTIC PRECISION)

**Current slide 51:** `SafeIndex / legality / capability` is used as one obligation family and then directly mapped to a representation requirement.

**Problem:** a proved `SafeIndex` often enables deleting a check; it does not inherently require a representation property. Target legality or memory-order/barrier semantics are cleaner examples of obligations that constrain lowering/representation.

**Decision:** use a stronger example such as `release-write semantics / GC reference-store barrier / target legality` → required IR/lowering capability → feasible lowerings → preference. Label as proposed planner model.

### F11 — The lowering chain is presented too literally (SEMANTIC PRECISION)

**Current slide 54:** `Write → volatile store → helper call → machine ops` reads like a mandatory linear lowering sequence.

**Decision:** make it explicitly illustrative and branch-aware: high-level write may lower to a target store, barrier sequence, helper call, or several machine operations; the semantic question may outlive the original node.

### F12 — The falsifiable experiment omits the first-order correctness metric (RESEARCH DESIGN)

**Current slide 62 metrics:** integration edges, consumer LOC, precision, invalidation cost, projection overhead, explainability.

**Problem:** an unsound system can “improve precision” by proving false things. The slide notes mention soundness, but the public experiment does not measure it.

**Decision:** add `soundness / false discharge` as a primary metric and a negative control: stale/contradictory producer evidence must not discharge an obligation.

### F13 — “one open semantic contract” risks implying one monolithic schema (ARCHITECTURE)

**Current slide 61:** “share one open semantic contract”.

**Decision:** use “shared extensible semantic-contract layer” with typed/versioned schemas. This remains compatible with slide 52: one shared boundary does not imply one solver or one universal ontology.

### F14 — Plugin comparison is a strawman in appendix Q&A (PRECISION)

**Current appendix:** “Plugins solve loading”.

**Problem:** plugin systems can also define APIs, lifecycle and extension points. The narrower defensible claim is that plugin loading alone does not define semantic composition, route legality, or cross-component knowledge reuse.

**Decision:** rewrite the answer narrowly; do not argue against plugin architectures in general.

### F15 — Final wording can still sound like a runtime zero-cost claim (BOUNDARY)

**Current final memory:** “Make abstractions disappear from execution…”

**Decision:** say “Resolve composition abstractions before execution; keep semantics available through transformation.” Preserve the accepted title, but keep the final explanatory sentence narrower than the title.

## Verified prior-art claims

No correction is required for the current LLVM / MLIR / CMake analogy slides:

- LLVM `PassBuilder` builds default pipelines from optimization levels and exposes extension-point callbacks.
- MLIR Interfaces exist specifically to let generic transformations/analyses query dialect-defined semantics without hard-coding operation types; Dialect Conversion uses conversion targets, rewrite patterns and optional type conversion.
- CMake specifies build structure abstractly and a generator writes the native buildsystem inputs.

These remain analogies, not novelty claims.

## Deliberately deferred: talk length

LangDev's published format is 25 minutes + 5 minutes Q&A, but the latest rebuild request explicitly removed the timing/slide-count cap for the intellectual-deck pass. Therefore this audit does **not** shorten the deck. Timing reduction remains a separate editorial pass after semantic correction.

## Repair order

1. Preserve the current foundation-first causal structure.
2. Insert a short repository-backed deabstraction + parity bridge before the research layer.
3. Correct factual UT boundaries (`exclude`, backend routes, planner-level feasibility, module/feature/contribution taxonomy).
4. Repair hypothetical semantic examples and add visible current/proposed labels.
5. Strengthen the research experiment with soundness and negative controls.
6. Tighten final/appendix wording to avoid zero-cost/plugin strawmen.
7. Extend deterministic deck checks so these specific semantic boundaries cannot silently regress.
8. Run structural, JS, timing and exhaustive render checks; then push and verify CI/Pages.
