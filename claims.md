# Conference claim contract — LangDev 2026

`CONTENT_EVIDENCE_LEDGER.md` is the authoritative evidence boundary for this content-finalization campaign. UniversalToolchain/Wist is an **implementation witness** for bounded mechanisms that exist today; it is not evidence that the general architecture is novel or universally correct.

The talk keeps four interpretation classes separate:

- **PRIOR ART / VERIFIED PRIOR ART** — mechanisms established by primary/upstream or peer-reviewed sources;
- **IMPLEMENTED WITNESS** — current UT/Wist code or tests demonstrate the bounded mechanism stated;
- **GENERAL DESIGN** — an architectural responsibility or distinction argued by the talk;
- **RESEARCH HYPOTHESIS** — a falsifiable proposal that still has to beat credible alternatives experimentally.

## Vocabulary and independent development

A **language capability** is a reusable authored compiler contribution. Depending on the system, it may participate in syntax, typing, analysis, lowering, optimization, backend behavior or tooling.

A **language profile** is one concrete request/configuration that selects and constrains reusable capabilities, policies and targets.

The unqualified word **dialect** is not the general term in this talk. It is reserved for an ecosystem's own terminology: Wist's `.wistdialect` file is one implementation syntax, while an MLIR dialect is an IR namespace/semantic extension.

Independent development means that producers can implement against **published ecosystem contracts** rather than requiring private pairwise integration APIs with every other author. It does **not** mean zero coordination, arbitrary compatibility or automatic semantic non-interference. Shared schema/version rules, declared dependencies, conflicts, ordering constraints and trust policy are all legitimate ecosystem contracts.

## Prior-art / novelty boundary

The following broad ideas are not novelty claims for this talk:

- independently developed or modular language extensions and automatic/reusable composition — Silver/ableC, Neverlang and MontiCore are direct prior art;
- relative cross-extension ordering and explicit/global generation plans — JetBrains MPS is direct prior art;
- extensible pass pipelines, generic cached analysis lookup and explicit preservation/invalidation — LLVM New Pass Manager is direct prior art;
- decoupled semantic interfaces/external models, effect queries, legality/conversion and reusable data-flow infrastructure — MLIR is direct prior art;
- semantic preservation and per-translation/refinement validation — CompCert, translation validation and Alive2 establish much stronger correctness baselines than structural route planning.

Safe framing:

> Independent language extension is the starting problem, not the invention. The research question is whether a narrower cross-component **semantic-evidence lifecycle** buys something useful beyond these mature mechanisms.

Composition also must not be equated with soundness:

> Composition answers whether pieces can be assembled under declared rules. Semantic preservation/non-interference is a separate property that needs its own proof, validator, trusted contract or fail-closed obligation mechanism.

## IMPLEMENTED WITNESS — Wist profile selection

Current Wist ships multiple `.wistdialect` examples. The dialect frontend parses that syntax and translates the requested modules/policy/backend into a `LanguageDefinition`; `LanguageCompiler` subsequently resolves the concrete plan.

Allowed wording: Wist has a declarative language-profile syntax today.

Not allowed: the syntax proves arbitrary third-party compatibility, or represents the general architecture by itself.

## IMPLEMENTED WITNESS — staged plan lifecycle

Current UT separates requested language definition, semantic planning, a read-only snapshotted `LanguagePlan`, and runtime/build-session materialization.

Allowed wording:

> Composition decisions can be resolved into an inspectable plan before runtime execution; runtime materializes that plan rather than rediscovering language features.

Do not say the whole compiler or all third-party state is immutable/stateless, or that freezing the plan proves semantic correctness.

## GENERAL DESIGN — profile WHAT / planner HOW

The language profile owns requested capabilities, exclusions/restrictions, policy and targets. Planning owns dependency/provider resolution, declared conflicts/order and executable representation routes.

A whole-language planning object is a responsibility boundary, not a novelty claim that global plans do not exist elsewhere. MPS generation plans and ordinary compiler pipeline builders are explicit prior art.

A future plan could select an MLIR-based subsystem where useful. Current UT does not implement an MLIR provider.

## IMPLEMENTED WITNESS — structural feasibility before preference

Current UT has a focused route-search regression in which a cost-2 route is rejected because artifact flow and a hard contribution-order constraint cannot both hold; a direct cost-10 route remains feasible and is selected.

Allowed wording:

> Hard declared requirements participate before route-cost preference. Cost ranks surviving structurally feasible candidates.

Mandatory boundary:

> **Structural feasibility is not semantic preservation.** The regression checks artifact connectivity, declared ordering and selected route identity; it does not define or prove a source-target semantic relation.

Semantic preservation must come from separate proofs, validators, trusted transformation contracts or explicit obligations/evidence.

## GENERAL DESIGN — precise freeze boundary

Open-world authoring/composition may terminate in one resolved plan, so ecosystem discovery and global composition need not repeat on an already-resolved per-program path.

This says nothing universal about mutable runtime/provider state, program-specific optimization cost, code size, dispatch cost or semantic non-interference. Per-program compilation and optimization still happen after the composition decision is frozen.

## IMPLEMENTED WITNESS — local deabstraction

Current UT contains bounded local rewrites, including:

- a recognized managed comparison call becoming a typed comparison intrinsic under the tested capability gate;
- `LoadEnvironment + Push(slot) + LoadExternal<T>` becoming one typed `LoadExternal<T>(slot)` intrinsic when the exact requested type/capability is supported.

Unsupported cases fail closed to the original IR in the tested paths.

Instruction-count reduction is not a numerical performance claim or a proof of whole-program equivalence.

## IMPLEMENTED WITNESS — backend parity and benchmark boundaries

Selected CIL/interpreter behavior is protected by differential regressions, including external-binding and shadowing cases. This is relational test evidence for covered cases, not a formal equivalence theorem.

The presentation publishes no C#↔Wist numerical performance ratio until a current reviewed raw Release BenchmarkDotNet artifact with environment/source identity and correctness/parity precheck exists. Setup and prepared execution remain separate measurement boundaries.

## RESEARCH HYPOTHESIS — semantic evidence contract

Generic semantic queries and invalidation are already prior art in LLVM/MLIR. The narrower proposal to test is a minimal cross-component **semantic-evidence lifecycle** with explicit identity, validity, contradiction and obligation rules.

For a proposition `P`, a query result must distinguish at least:

1. **unsupported** — this provider/contract does not answer this proposition;
2. **unknown** — the proposition is supported but current evidence cannot establish either side;
3. **established(P)** — current-valid suitable evidence supports `P`;
4. **refuted(P)** — current-valid suitable evidence supports `¬P`;
5. **contradictory** — current-valid suitable evidence supports both `P` and `¬P`, or otherwise conflicts under the contract.

Only current-valid evidence suitable for the proposition may discharge a legality obligation. **Unknown, unsupported and contradictory do not discharge it.** Contradictory current-valid evidence fails closed unless the published contract defines an explicit trusted reconciliation rule.

A shared query/evidence contract also needs explicit ownership and versioning. The contract owner defines proposition identity, evidence compatibility and result semantics; a producer cannot privately redefine what `P` means for existing consumers.

## RESEARCH HYPOTHESIS — obligations belong to transformations

A transformation/lowering owns the legal precondition it must satisfy. Producers contribute evidence; they do not get to weaken or redefine that precondition.

Example:

> “May omit this bounds check?” is a transformation obligation. Range/shape producers can contribute evidence toward `SafeIndex(a,i)`, but the consumer/transform defines the exact safety proposition and which side conditions matter.

## RESEARCH HYPOTHESIS — `SafeIndex` side conditions

The mnemonic equation

```text
0 <= i < N
N = Length(a)
=> SafeIndex(a, i)
```

is intentionally incomplete unless its evidence is scoped. A defensible obligation must account for at least:

- facts describing the same semantic array/index and the same relevant context/revision;
- no intervening invalidating mutation/reallocation/extent change for the modeled object;
- the actual integer/signedness/overflow semantics used by the access and comparison;
- path/control-flow/dominance conditions under which the range and extent facts hold;
- assumptions attached to the analyses/evidence.

If those conditions cannot be established, the transformation keeps the check.

## RESEARCH HYPOTHESIS — operation semantics vs lowering obligations for writes

`Write(place, value)` spans two distinct layers that must not be collapsed.

**Operation/source semantic questions** may include writability, abstract effects/resources, alias/resource identity, visibility, volatility and language-level ordering/atomicity requirements.

**Lowering/runtime obligations** may include a CoreCLR GC write barrier for a managed-reference heap store, a target-specific atomic/fence sequence, or a runtime/transaction protocol.

MLIR effect interfaces are direct prior art for operation/effect queries. A CoreCLR GC barrier is a concrete JIT/runtime lowering obligation whose legal normal/checked/no-barrier choice depends on runtime/JIT facts; it is not simply a source-language `IWritable` trait.

## RESEARCH HYPOTHESIS — validity and cross-representation correspondence

A typed value alone is insufficient because evidence can become stale after transformation. The proposed `Judgement` name means a proposition/result together with subject, context/revision/validity, assumptions and evidence. It is modeling terminology, not a claimed universal ontology.

Stable IDs/provenance can help, but they are not sufficient for transformations such as cloning, fusion, CSE, inlining, unrolling, code motion or many-to-one lowering. The meaningful question is a **semantic correspondence**: refinement, simulation, projection/property transport or another explicitly defined relation.

For a transformation `T : r -> r'`, each affected fact that a later decision still uses must be handled explicitly:

1. **transport/project** it through a justified correspondence relation;
2. **re-analyse/recompute** it on `r'`; or
3. **invalidate** it so it cannot discharge a later obligation.

“There is no universal inverse lowering” motivates this rule but is not itself a correctness proof. CompCert, translation validation and Alive2 are important stronger baselines for cross-representation correctness claims.

## STRONGEST ALTERNATIVE

The strongest practical alternative is deliberately ordinary:

> local IR interfaces + domain-specific analyses + a pass/analysis manager + explicit adapters + local invalidation.

LLVM AnalysisManager/`PreservedAnalyses` and MLIR interfaces/external models/effects/data-flow make this alternative substantial, not a strawman.

The shared evidence layer should be rejected if it cannot demonstrate a better engineering/correctness tradeoff. A fair comparator experiment must measure at least:

- edits required in existing consumers when a new producer is added;
- number of integration edges/adapters;
- **false obligation discharges** / unsafe transformations (must remain zero in the test model);
- analysis/optimization precision;
- invalidation and re-analysis cost;
- schema/versioning/infrastructure burden.

Negative controls include stale evidence, contradictory evidence and representation changes. If the shared layer merely renames MLIR/LLVM-style local mechanisms or adds schema burden without reducing coupling, remove it.

## Final conference boundary

**PRIOR ART:** independent/modular language extension and composition; global/ordered generation plans; generic semantic interfaces/effect queries; analysis caching/preservation/invalidation; semantic-preservation/translation-validation approaches.

**IMPLEMENTED WITNESS:** Wist profiles; staged UT planning; focused structural feasibility-before-preference regression; bounded local deabstraction; selected CIL/interpreter parity regressions; benchmark methodology boundary.

**GENERAL DESIGN:** language capability/profile distinction; profile WHAT vs planner HOW; one resolved structural plan can terminate open-world composition before an already-resolved per-program path; composition is not soundness.

**RESEARCH HYPOTHESIS:** whether a versioned cross-component semantic-evidence lifecycle with five-state results, fail-closed contradictions, transformation-owned obligations and explicit transport/reanalyse/invalidate rules measurably reduces coupling versus LLVM/MLIR/local-adapter baselines without weakening correctness.

Final synthesis:

> **AUTHOR against published contracts. RESOLVE one declared-feasible plan. OPTIMIZE only when current-valid evidence justifies the transformation.**
