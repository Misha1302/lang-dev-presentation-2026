# CONTENT_EVIDENCE_LEDGER.md — LangDev 2026

Authoritative evidence layer for the content-finalization campaign.

- External-source review date: **2026-09-06**
- Presentation baseline reviewed: `Misha1302/lang-dev-presentation-2026@e69cab6adf38286945e191dee1fc95b278730ee4`
- Campaign baseline reviewed: `content/langdev-finalization-2026-09@638f1b085f09a7ef4aa51d4c1f29c4c45cd40598`
- UniversalToolchain implementation witness reviewed: `Misha1302/UniversalToolchain@40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- Evidence authority used here: current code/tests first; then current official/primary/peer-reviewed sources; then campaign contracts and repository documentation.
- This ledger is an evidence boundary, **not** a novelty certificate. Failure to find a closer system in this bounded review must not be stated as proof of novelty.

## Executive conclusions

1. **Independent and composable language extensions are established prior art.** Silver/ableC, Neverlang, JetBrains MPS and MontiCore cover materially different versions of independent feature/component authoring and language composition. The talk must not claim this idea as novel.
2. **Composition is not automatically soundness or semantic non-interference.** ableC/Silver provide specific modular well-definedness/determinism conditions; Neverlang's 2026 soundness work exists precisely because loose composition can leave undefined-attribute failures; MPS ordering and MontiCore syntax/tool composition do not amount to a universal semantic-preservation theorem.
3. **Generic semantic interfaces, effect queries, analysis caches and invalidation are established prior art.** LLVM New PM and MLIR are strong baselines. The talk must not present “generic semantic queries” or “validity/invalidation exists” as novelty by themselves.
4. **UT planner feasibility is structural/executable-plan feasibility, not semantic preservation.** The current regression proves that a hard ordering constraint participates before route-cost preference. It does not prove that a surviving route preserves source semantics.
5. **The defensible research hypothesis is narrower.** A candidate research question is whether independently authored producers/consumers can share a *minimal typed lifecycle* for semantic evidence identity, context/revision validity, contradiction handling, and obligation discharge across changing representations without centralizing every domain analysis. This review does **not** establish that this lifecycle is novel; Phase 03 must present it as a falsifiable research hypothesis and compare it explicitly with LLVM/MLIR/local-adapter alternatives.

## Prior-art comparison summary

| System | Problem solved | Extensibility unit / authorship boundary | Composition mechanism | Actual guarantee / evidence | Important limitation | Consequence for this talk |
|---|---|---|---|---|---|---|
| Silver / ableC | Extensible C and reliable composition of extensions | Independently developed language extensions / attribute-grammar fragments | Silver forwarding + modular well-definedness; Copper modular determinism; ableC extension imports | Certified extensions can compose into a well-defined AG; Copper addresses deterministic grammar composition | Specific formal conditions; not a theorem of arbitrary behavioral non-interference between all extension semantics | Independent extension composition is not novel; any claim must be narrower than reliable syntactic/AG composition |
| Neverlang | Feature-oriented modular language development | Modules, roles, slices, separately compiled feature artifacts | Language composes slices; roles form ordered semantic phases | Composition/restriction, separate compilation, dynamic extension are documented and evaluated | Loose dynamic attributes historically permit undefined-attribute failures; 2026 `nlgcheck` targets this gap | Feature/slice composition and ordered phases are prior art; composability and soundness must be separated |
| JetBrains MPS | Language extension and ordered model-to-model generation | Languages/generators and their mappings; extensions can contribute generation rules | Relative mapping priorities and explicit generation plans | Global generation plan is constructed from involved generators; explicit plan centralizes ordering | Mutual priorities can create dependencies; generation-plan correctness is not a general semantic-preservation proof | “One global/resolved generation plan” and cross-extension ordering are not novelty claims |
| MontiCore | Reusable textual DSL/language components | Independently developed grammar/language components | Grammar inheritance, extension, embedding, aggregation; composable generated infrastructure | Syntax-oriented reusable composition and associated tooling composition | Strongest published claims are primarily syntax/tooling composition, not universal semantic non-interference | Language-component composition is established prior art |
| LLVM New PM | Extensible transformation/analysis pipelines with cached analyses | Passes, analyses, plugins, target/frontend callbacks | PassBuilder pipelines; pass plugins; AnalysisManagers and proxies | Cached analysis queries plus explicit `PreservedAnalyses`/invalidation discipline | Scoped to LLVM IR units and pass-manager lifecycle; domain analyses still define their own semantics | Generic analysis query + preservation/invalidation is prior art |
| MLIR | Extensible multi-level IR, legality/conversion, generic semantics and analyses | Dialects, ops/types/attrs, interfaces and external interface models | Interfaces, external models, conversion targets/patterns/type conversion, data-flow solver, effect interfaces | Generic transforms can query semantics without exact op knowledge; explicit conversion legality; effect and data-flow infrastructure | No single interface is a universal semantic ontology; data-flow state is invalid after IR changes and must be rebuilt; some semantics remain out of model | Generic semantic interfaces/effects/legality/dataflow are prior art; surviving claim must be about a narrower cross-component lifecycle |
| CompCert | Compiler correctness across transformations | Verified compiler passes / source-target semantics | Pass-by-pass simulations composed into whole-compiler theorem | Semantic preservation theorem; forward/backward simulations, including separate compilation theorem | Requires formal semantics/proofs for its supported language/compiler | Planner reachability/order is far weaker than semantic preservation |
| Translation validation | Per-translation compiler correctness checking | One source→target translation instance | Validator checks each compiler run rather than proving compiler globally | Classic correctness approach for individual translations | Validator relation/coverage must itself be justified | Cross-representation correctness already has a mature validation framing |
| Alive2 | Bounded LLVM IR transformation validation | LLVM source/target IR pair | SMT-based refinement checking / bounded translation validation | Automatically detects refinement violations within supported/bounded model | Bounded loops/resource limits can miss bugs; LLVM-specific semantics | “Correspondence across lowering” must say what relation is checked; generic validation is not novel |
| CoreCLR/JIT GC barrier | Correct generational-GC bookkeeping for managed-reference stores | JIT/runtime lowering of reference stores | Normal/checked write-barrier helpers and GC/JIT state | Heap reference updates require appropriate bookkeeping; JIT may select normal, checked or no barrier based on destination facts | This is a concrete runtime/codegen obligation, not a universal source-level write ontology | GC-barrier example is valid as a lowering obligation, but must be located at runtime/JIT semantic boundary |

---

## CLAIM_ID: UT-DIALECT-PROFILES

**Proposed claim**

Current Wist ships declarative `.wistdialect` profiles that select and restrict reusable language pieces rather than hardcoding one compiler configuration.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`, reviewed 2026-09-06
- path/paper: `UniversalToolchain/Dialects/examples/wist/`
- test/function/section: shipped directories `composition-restricted`, `full-default-native`, `full-default`, `function-calls-safe-math`, `minimal-arithmetic-grouped`, `minimal-arithmetic-native`, `minimal-arithmetic`, `pricing-restricted`, `ssa`; `UniversalToolchain.Dialects.Frontend/DialectDslCompiler.cs`; `UniversalToolchain.Wist.LanguagePack/WistFacadeLanguageDefinitionFactory.cs`
- external source type: repository code/examples

**Observed support**

The repository contains multiple `.wistdialect` examples. `DialectDslCompiler` parses dialect source, and `WistFacadeLanguageDefinitionFactory` translates the resulting slice into a `LanguageDefinition`. Current docs and code place `LanguageCompiler` after this translation.

**Safe conference wording**

“Wist has a declarative profile syntax today: profiles request modules/capabilities, policy and a backend, then the generic planner resolves the concrete plan.”

**Unsafe / prohibited wording**

“Any arbitrary compiler feature can already be composed safely,” “`.wistdialect` proves language-extension non-interference,” or “the DSL syntax itself is the general architecture.”

**Assumptions / validity boundary**

Bounded to shipped Wist profiles and the current Wist frontend. The existence of profile examples does not establish compatibility of arbitrary third-party extensions.

**Strongest prior art / alternative**

Neverlang language/slice composition, MPS generation plans, MontiCore language components, Silver/ableC extension composition.

**Open question**

How much of the current profile surface remains convenient and stable when independently versioned third-party feature packages become common?

**Deck consequence**

Keep as an implementation witness; explicitly separate profile syntax from the general architecture and from novelty.

---

## CLAIM_ID: UT-DIALECT-FRONTEND-PARITY

**Proposed claim**

The current dialect frontend has tests that require standalone and dependency-injection-composed compiler frontends to produce equivalent parsed dialect slices for representative built-in inputs.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain/UniversalToolchain.Dialects.Tests/DialectDslCompositionParityTests.cs`
- test/function/section: `StandaloneCompiler_ShouldMatchDiComposedCompiler_ForRepresentativeBuiltInInputs`; `StandaloneCompiler_ShouldMatchExplicitFrontendPipeline_ForRepresentativeBuiltInInputs`; equivalent rejection tests
- external source type: current test source

**Observed support**

Representative built-in dialect inputs are compiled through standalone, DI-composed and explicit frontend paths and compared for equivalent dialect slices. Conflict/singleton error paths are also compared.

**Safe conference wording**

“The current dialect DSL has parity tests across its standalone and composed frontend entry paths.”

**Unsafe / prohibited wording**

“All textual permutations are equivalent,” “translation parity proves semantic equivalence of generated programs,” or “all third-party frontend extensions are order-independent.”

**Assumptions / validity boundary**

Only the representative inputs and error cases covered by the test source are established.

**Strongest prior art / alternative**

Ordinary frontend conformance/differential tests; no novelty claim.

**Open question**

Which additional extension permutations need property-based or fuzz testing before stronger independence claims are justified?

**Deck consequence**

Use only if frontend implementation evidence is needed; do not promote it into a semantic-composition theorem.

---

## CLAIM_ID: UT-STAGED-PLAN-LIFECYCLE

**Proposed claim**

Current UT separates requested language definition, semantic planning, a read-only snapshotted `LanguagePlan`, and runtime/build-session materialization.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain.Language.Abstractions/LanguageContracts.cs`; `UniversalToolchain.LanguageSdk/LanguageCompiler.cs`; `UniversalToolchain.LanguageSdk/LanguagePlan.cs`; `UniversalToolchain.Runtime/LanguageRuntime.cs`; `UniversalToolchain.Runtime/LanguageBuildRuntime.cs`
- test/function/section: `RuntimeLifecycleAndCanonicalizationTests.LanguagePlan_HasNoPublicConstructor_AndVerifierDetectsHashTampering`; runtime lifecycle tests
- external source type: current code/tests

**Observed support**

`LanguageDefinition` snapshots selected collections into read-only structures. `LanguageCompiler.Compile` is the public planner that resolves features, contributions and artifact routes before constructing `LanguagePlan`. `LanguagePlan` has no public constructor, stores read-only feature/contribution/route collections, computes `PlanHash`, and is verified. `LanguageRuntime` materializes and executes one plan; `LanguageBuildRuntime` adds exact planned artifact construction.

**Safe conference wording**

“Composition decisions are resolved into an inspectable plan before runtime execution; runtime materializes that plan rather than rediscovering language features.”

**Unsafe / prohibited wording**

“The entire compiler is immutable,” “no program-specific compilation happens after planning,” “all runtime state is pure/stateless,” or “freezing the plan proves semantic correctness.”

**Assumptions / validity boundary**

Read-only/snapshotted applies to the exposed plan/definition structures described above, not every object reachable through all descriptors or runtime providers. Runtime sessions can contain mutable execution state and have explicit lifetimes.

**Strongest prior art / alternative**

MPS generation plans; LLVM PassBuilder pipelines; conventional compiler configuration objects.

**Open question**

Whether the plan boundary remains sufficient when semantic evidence and third-party subsystem providers must also carry validity/ownership information.

**Deck consequence**

Keep the staged architecture; avoid “zero overhead” or global immutability language.

---

## CLAIM_ID: UT-PLAN-CANONICALIZATION-CONTROLS

**Proposed claim**

Current UT has focused controls showing plan identity is stable under tested irrelevant-package and authoring-order permutations.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain.LanguageSdk.Tests/PlannerPolicyControlTests.cs`; `RuntimeLifecycleAndCanonicalizationTests.cs`
- test/function/section: `Planner_ShouldPreservePlanAndExecution_WhenIrrelevantPackageIsAdded`; `Planner_ShouldPreservePlanAndExecution_WhenAuthoredInputOrderChanges`; `PlanHash_IsIndependentOfFeatureAndBackendInsertionOrder`
- external source type: current tests

**Observed support**

The tests compare `PlanHash`, selected route contribution IDs and/or runtime result under specific unused-package, contribution-order, feature-order and backend-order perturbations.

**Safe conference wording**

“Plan canonicalization has regression tests against several irrelevant input-order changes.”

**Unsafe / prohibited wording**

“Planning is invariant under every permutation,” “adding any extension cannot affect a plan,” or “this proves non-interference among arbitrary extensions.”

**Assumptions / validity boundary**

Only perturbations explicitly covered by the tests are established; a semantically relevant new package/provider is expected to be able to change planning.

**Strongest prior art / alternative**

Deterministic build systems, canonical lockfiles and reproducible pipeline planning.

**Open question**

Which metamorphic properties should define the complete plan-stability contract?

**Deck consequence**

Useful implementation evidence; phrase as tested controls, never universal non-interference.

---

## CLAIM_ID: UT-FEASIBILITY-BEFORE-PREFERENCE

**Proposed claim**

The current planner rejects a lower-cost artifact route when it violates a declared hard contribution order and selects a higher-cost feasible route.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain/UniversalToolchain.LanguageSdk.Tests/PlannerPolicyControlTests.cs`
- test/function/section: `RouteSearch_ShouldChooseMoreExpensiveRoute_WhenCheaperRouteViolatesDescriptorOrder`
- external source type: current regression test

**Observed support**

The cheap route consists of `cheapParse` (`SourceText → middle`, cost 1) then `cheapLower` (`middle → executable`, cost 1), but `cheapParse` declares `afterContributions: [cheapLower]`. Artifact flow requires parse before lower, while the hard descriptor order requires parse after lower, so that cost-2 route is inadmissible. A direct `SourceText → executable` transformation with cost 10 remains feasible and is the selected route.

**Safe conference wording**

“Hard feasibility/order constraints participate before route-cost preference: the test rejects an impossible cost-2 route and selects the feasible cost-10 route.”

**Unsafe / prohibited wording**

“The planner proves the chosen route is semantically equivalent,” “cost measures correctness/trust,” or “any feasible route preserves program meaning.”

**Assumptions / validity boundary**

The hard condition here is contribution ordering plus artifact-contract reachability. Semantic preservation is outside the tested assertion.

**Strongest prior art / alternative**

MLIR conversion legality, build/planning constraint solvers, MPS generation ordering; semantic correctness baselines are CompCert/translation validation/Alive2, which are stronger and different.

**Open question**

How should semantic obligations participate in feasibility without falsely equating structural feasibility with preservation?

**Deck consequence**

Keep the regression as the concrete planner witness; immediately state that structural feasibility is not semantic preservation.

---

## CLAIM_ID: UT-DEABSTRACTION-COMPARISON

**Proposed claim**

Current UT can replace a recognized managed comparison call with a typed comparison intrinsic when the optimizer's declared comparison capability family is complete, and fails closed when that family is incomplete.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain/UniversalToolchain.Modules.Tests/ModuleCoverage/TypedIntrinsicEmitterOptimizerTests.cs`
- test/function/section: `ComparisonOptimizer_WhenCapabilitySupportsFamily_RewritesToTypedIntrinsic`; `ComparisonOptimizer_WhenCapabilityIncomplete_ReturnsInputUnchanged`
- external source type: current optimizer tests

**Observed support**

With the tested comparison capability family available, a managed `Comparisons.Less<int>` call is rewritten to typed intrinsic `BuiltinIntrinsicSymbols.Comparison.Less<int>`. Removing required family capability support (the negative test removes `Less<double>`) causes the optimizer to return the original IR unchanged.

**Safe conference wording**

“A local optimizer recognizes this managed comparison pattern and deabstracts it to a typed intrinsic under an explicit capability gate; otherwise it leaves the IR unchanged.”

**Unsafe / prohibited wording**

“All managed calls are eliminated,” “typed intrinsics are always faster,” or “the rewrite proves whole-program equivalence.”

**Assumptions / validity boundary**

Bounded to the exact recognized patterns, supported type/capability family, and tested optimizer behavior.

**Strongest prior art / alternative**

Conventional peephole/intrinsic recognition in optimizing compilers.

**Open question**

How should non-local semantic evidence safely enable additional deabstraction beyond exact local patterns?

**Deck consequence**

Keep as local deabstraction witness; do not attach numerical performance claims.

---

## CLAIM_ID: UT-DEABSTRACTION-EXTERNAL-LOAD

**Proposed claim**

Current UT has a tested 3→1 AIR rewrite from managed external-load machinery to one typed `LoadExternal<T>` intrinsic when the exact requested external type is supported.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain/UniversalToolchain.Modules.Tests/ModuleCoverage/TypedIntrinsicEmitterOptimizerTests.cs`
- test/function/section: `NativeCilOptimizer_WhenCapabilitySupportsRequestedExternalType_RewritesManagedCallSequence`; `...DoesNotSupportRequestedExternalType_KeepsManagedCallSequence`; `...OnlyRequestedExternalTypeIsSupported_DoesNotRequireOtherExternalTypes`
- external source type: current optimizer tests

**Observed support**

For `double`, the tested input sequence `LoadEnvironment` managed call + `Push(2)` + managed `LoadExternal<double>` call becomes one typed `Core.LoadExternal<double>` intrinsic carrying operand `2`. If `double` is not supported, the original IR object is returned unchanged. Support for only the requested external type is sufficient.

**Safe conference wording**

“In this exact local case, three AIR operations become one typed external-load intrinsic; unsupported types fail closed to the original sequence.”

**Unsafe / prohibited wording**

“3→1 means 3× faster,” “all abstraction overhead disappears,” or “the optimization works for arbitrary external access patterns.”

**Assumptions / validity boundary**

Exact pattern, exact type capability and current optimizer implementation only. No performance result follows from instruction-count reduction.

**Strongest prior art / alternative**

Ordinary intrinsic recognition/peephole lowering.

**Open question**

Whether shared non-local semantic contracts can unlock equally safe rewrites where the required facts are not present in the local IR window.

**Deck consequence**

Keep as the concrete local witness and bridge to the research section.

---

## CLAIM_ID: UT-BACKEND-PARITY

**Proposed claim**

Current UT contains differential parity infrastructure and concrete regressions comparing selected Wist behavior across CIL and interpreter backends.

**Class**

`IMPLEMENTED WITNESS`

**Evidence identity**

- repository/source: `Misha1302/UniversalToolchain`
- revision/date: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`
- path/paper: `UniversalToolchain.Testing.Infrastructure/BackendParityInfrastructure.cs`; `Tests/Backends/InterpreterBindingsParityTests.cs`
- test/function/section: `RunBoth`; `AssertSemanticParity`; tests for external bindings, repeated local writes, reordered declarations, shadowing/nested scope, unknown identifiers
- external source type: current infrastructure/tests

**Observed support**

The parity helper builds one dual-backend definition, asserts backend-specific dialect translation agrees on selected features/policy/order/intrinsic policy, plans it, then compares CIL and interpreter outcomes. Binding tests cover concrete arithmetic, external binding, declaration-order, local/external shadowing, nested scope, failure and determinism cases.

**Safe conference wording**

“Selected CIL/interpreter semantics are protected by differential regressions, including external-binding and shadowing cases.”

**Unsafe / prohibited wording**

“The backends are formally equivalent for all Wist programs,” “parity tests prove compiler correctness,” or “every semantic domain is covered.”

**Assumptions / validity boundary**

Only tested programs, value normalization and failure comparisons are supported. This is relational test evidence, not a proof.

**Strongest prior art / alternative**

Differential testing and translation validation; formal proof systems such as CompCert are stronger.

**Open question**

Which semantic partitions need generated differential tests or formal refinement checks to raise confidence beyond handpicked regressions?

**Deck consequence**

Keep as bounded evidence; explicitly say “selected regressions,” not “equivalence.”

---

## CLAIM_ID: PA-SILVER-ABLEC

**Proposed claim**

Independently developed language extensions that compose under explicit modular checks are established prior art in Silver/ableC.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: Minnesota Extensible Language Tools (MELT)
- revision/date: official pages reviewed 2026-09-06; core publications 2012/2017
- path/paper: `https://melt.cs.umn.edu/`; `https://melt.cs.umn.edu/silver/concepts/modular-well-definedness/`; `https://melt.cs.umn.edu/ableC/`; OOPSLA 2017 *Reliable and Automatic Composition of Language Extensions to C: The ableC Extensible Language Framework*
- test/function/section: Silver modular well-definedness; Copper modular determinism; ableC extension ecosystem
- external source type: official project documentation + peer-reviewed prior art

**Observed support**

MELT explicitly targets extensions that need not know one another and automatic composition without glue code. Silver provides modular well-definedness analysis for independently developed certified extensions; Copper provides a modular determinism analysis; ableC demonstrates multiple extensions and compositions.

**Safe conference wording**

“Independent, automatically composable language extensions already have strong prior art; Silver/ableC even provides modular checks for specific composition properties.”

**Unsafe / prohibited wording**

“UT invented independent language extensions,” or “Silver proves arbitrary extensions cannot interfere semantically.”

**Assumptions / validity boundary**

The established guarantee is tied to the Silver/Copper analyses and their formal conditions, not arbitrary behavioral non-interference.

**Strongest prior art / alternative**

This is itself one of the strongest direct alternatives to a broad extensibility novelty claim.

**Open question**

What remaining coupling problem is not covered by Silver/ableC's grammar/attribute-grammar composition model?

**Deck consequence**

Use as a novelty boundary. Broad “independent extension composition” claims must be removed or reframed as prior art.

---

## CLAIM_ID: PA-NEVERLANG

**Proposed claim**

Neverlang establishes feature/slice-based modular language composition, ordered semantic roles, separate compilation and dynamic extension as prior art.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: Neverlang project / Vacchi & Cazzola
- revision/date: official docs reviewed 2026-09-06; 2015 journal paper; 2026 soundness preprint reviewed
- path/paper: `https://neverlang.di.unimi.it/neverlang.html`; Vacchi & Cazzola, *Neverlang: A framework for feature-oriented language development*, DOI `10.1016/j.cl.2015.02.001`; Bruzzone, Cazzola, Favalli, *From Separate Compilation to Sound Language Composition*, arXiv `2602.03777`
- test/function/section: modules/roles/slices/language composition; 2026 `nlgcheck` motivation
- external source type: official documentation + peer-reviewed paper + current preprint

**Observed support**

Neverlang composes modules into slices and slices into languages; roles form ordered compilation/interpretation phases. The 2015 work reports composition/restriction, separate compilation and dynamic extension. The 2026 work documents that loose dynamic attribute handling can allow undefined-attribute runtime errors and introduces static analysis to improve composition correctness.

**Safe conference wording**

“Feature slices, ordered semantic phases and separately compiled language components are established prior art; Neverlang also illustrates why composability alone does not imply static correctness.”

**Unsafe / prohibited wording**

“No earlier system composes semantic language features,” or “Neverlang composition is inherently sound.”

**Assumptions / validity boundary**

The 2026 soundness work is a preprint/current research artifact and should be labeled as such; it is used here primarily to show a documented limitation of prior composition machinery.

**Strongest prior art / alternative**

Direct prior art for feature-oriented language composition and separate compilation.

**Open question**

Can a generic evidence lifecycle help independent components without recreating whole-language global analysis or dynamic-map failure modes?

**Deck consequence**

Use as both prior art and a cautionary counterexample to “composition = soundness.”

---

## CLAIM_ID: PA-MPS

**Proposed claim**

JetBrains MPS already constructs global generation ordering from extensible generators and offers explicit generation plans that centralize cross-language ordering.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: JetBrains MPS official documentation
- revision/date: MPS 2025.3/2026.1 docs reviewed 2026-09-06
- path/paper: `https://www.jetbrains.com/help/mps/generation-plan.html`; `https://www.jetbrains.com/help/mps/mapping-priorities.html`; `https://www.jetbrains.com/help/mps/generator-cookbook.html`; `https://www.jetbrains.com/help/mps/the-generator-algorithm.html`
- test/function/section: generation plans, mapping priorities, extensible generator
- external source type: current official product documentation

**Observed support**

MPS mapping priorities impose relative ordering among generator mappings. Its generator can resolve involved rules into a global generation plan. Explicit generation plans were introduced partly because mutual generator priorities can force languages to know each other and thereby break desired independence; plans centralize ordering and can include transforms, checkpoints, extensions and forks.

**Safe conference wording**

“Explicit global generation planning and relative cross-extension ordering are established in MPS.”

**Unsafe / prohibited wording**

“No language workbench resolves a global plan,” or “MPS generation plans provide a universal semantic-preservation guarantee.”

**Assumptions / validity boundary**

MPS mechanisms are generation-oriented and tied to its model/generator architecture.

**Strongest prior art / alternative**

A strong alternative to any novelty claim based solely on a resolved global plan or relative ordering.

**Open question**

What additional semantics, feasibility or evidence-validity responsibilities justify a distinct whole-compiler planning abstraction?

**Deck consequence**

Mention when positioning `LanguagePlan`; novelty must be narrower than “global plan exists.”

---

## CLAIM_ID: PA-MONTICORE

**Proposed claim**

MontiCore establishes independently developed, reusable language-component composition through inheritance, embedding and aggregation as prior art.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: MontiCore / RWTH Aachen
- revision/date: official docs reviewed 2026-09-06; published prior art 2008–2015
- path/paper: `https://monticore.github.io/monticore/docs/Languages/`; `https://monticore.github.io/monticore/docs/GettingStarted/`; Haber et al., *Integration of Heterogeneous Modeling Languages via Extensible and Composable Language Components*, arXiv `1509.04502`; Krahn, Rumpe, Völkel, *MontiCore: Modular Development of Textual Domain Specific Languages*, DOI `10.1007/978-3-540-69824-1_17`
- test/function/section: language components; inheritance/embedding/aggregation
- external source type: official docs + peer-reviewed/archived publications

**Observed support**

MontiCore has an explicit notion of language components and composes grammars via inheritance, extension, embedding and aggregation; associated generated infrastructure and handwritten extensions are designed for reuse/composition. Research literature explicitly discusses independently developed syntactically composable components.

**Safe conference wording**

“Reusable, independently developed language components and multiple composition operators are established prior art.”

**Unsafe / prohibited wording**

“Composable language components are new,” or “MontiCore proves semantic non-interference of all combined components.”

**Assumptions / validity boundary**

The strongest direct claims are about grammar/language-component and tooling composition; behavioral semantics require separate analysis.

**Strongest prior art / alternative**

Direct prior art against broad language-component composition novelty.

**Open question**

How should semantic optimization knowledge compose once syntax/tooling composition is no longer the hard part?

**Deck consequence**

Use to narrow the extensibility novelty claim; do not use as an MLIR-style IR comparison.

---

## CLAIM_ID: PA-LLVM-ANALYSIS-INVALIDATION

**Proposed claim**

LLVM New Pass Manager establishes generic cached analysis queries, pass/plugin extensibility and explicit preservation/invalidation as prior art.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: LLVM Project official documentation
- revision/date: current docs reviewed 2026-09-06
- path/paper: `https://llvm.org/docs/NewPassManager.html`; `https://llvm.org/docs/WritingAnLLVMNewPMPass.html`; `https://llvm.org/doxygen/classllvm_1_1AnalysisManager.html`
- test/function/section: `AnalysisManager`, `PreservedAnalyses`, `PassBuilder`, pass-plugin callbacks, invalidation
- external source type: current upstream documentation/API reference

**Observed support**

Passes query `AnalysisManager` for cached analysis results. Transformations return `PreservedAnalyses` to say what remains valid, and managers invalidate non-preserved results; explicit clearing/manual invalidation and dependencies/proxies exist. Frontends/backends/plugins can inject passes into pipelines.

**Safe conference wording**

“Generic analysis lookup, cached results and explicit preservation/invalidation are mature prior art in LLVM.”

**Unsafe / prohibited wording**

“Compilers lack a shared analysis query mechanism,” “UT is novel because facts have validity,” or “LLVM invalidation solves all cross-representation semantic identity problems.”

**Assumptions / validity boundary**

LLVM analyses are scoped to LLVM IR units/pass-manager lifecycles; individual analyses define their own semantics and update rules.

**Strongest prior art / alternative**

The strongest baseline for a local pass-manager/analysis-manager alternative to a new semantic evidence layer.

**Open question**

Can the target research problem be solved with LLVM-style managers plus adapters, or does independently authored cross-representation evidence require an additional minimal contract?

**Deck consequence**

Mandatory strongest alternative. Any generic query/invalidation novelty wording must be removed.

---

## CLAIM_ID: PA-MLIR-SEMANTIC-INTERFACES

**Proposed claim**

MLIR establishes decoupled semantic interfaces/external models, explicit conversion legality, effect queries and reusable data-flow infrastructure as prior art.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: MLIR official documentation
- revision/date: current docs/API reviewed 2026-09-06
- path/paper: `https://mlir.llvm.org/docs/Interfaces/`; `https://mlir.llvm.org/docs/DialectConversion/`; `https://mlir.llvm.org/docs/Rationale/SideEffectsAndSpeculation/`; `https://mlir.llvm.org/doxygen/classmlir_1_1DataFlowSolver.html`
- test/function/section: op/type/attribute/dialect interfaces, external models, `ConversionTarget`, `MemoryEffectsOpInterface`, `ConditionallySpeculatable`, `DataFlowSolver`
- external source type: current upstream docs/API reference

**Observed support**

Interfaces let transformations and analyses query semantics without exact dialect/op knowledge. External models attach interface implementations without modifying the original IR definition. Dialect Conversion models legality and rewrite/type conversion. Memory effects/resources model read/write and implicit effects. The data-flow solver coordinates multiple analyses and explicitly states analysis states must be erased/rebuilt after IR changes.

**Safe conference wording**

“Decoupled semantic interfaces, external models, effect queries, legality and generic data-flow infrastructure are already present in MLIR.”

**Unsafe / prohibited wording**

“MLIR has no semantic extensibility,” “generic semantic questions are new,” or “MLIR has no validity discipline.”

**Assumptions / validity boundary**

These mechanisms do not form one universal semantic ontology, and MLIR itself documents boundaries such as incomplete non-local-control-flow modeling and data-flow-state invalidation after IR mutation.

**Strongest prior art / alternative**

MLIR interfaces + local analyses/adapters is the strongest practical alternative the research layer must beat.

**Open question**

Is there a demonstrable class of independent producer/consumer integrations across representation changes where a small evidence lifecycle reduces pairwise coupling relative to MLIR interfaces/local analyses without hiding domain semantics?

**Deck consequence**

Must be treated as strongest alternative and novelty boundary, not a foil.

---

## CLAIM_ID: PA-COMPCERT-PRESERVATION

**Proposed claim**

Semantic preservation across a compiler pipeline has a substantially stronger formal baseline in CompCert than UT's current structural planning evidence.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: CompCert official documentation
- revision/date: CompCert 3.18 docs, reviewed 2026-09-06
- path/paper: `https://compcert.org/doc/html/compcert.driver.Compiler.html`; `https://compcert.org/man/manual001.html`
- test/function/section: whole-compiler semantic-preservation theorems, forward/backward simulations, separate compilation theorem
- external source type: official formal proof documentation

**Observed support**

CompCert composes pass-level simulation results and proves whole-compiler semantic preservation, including a theorem for separate compilation/linking under its assumptions.

**Safe conference wording**

“Structural plan feasibility is not compiler correctness; formal semantic preservation systems such as CompCert establish a much stronger relation through simulations.”

**Unsafe / prohibited wording**

“A route that type-checks and satisfies ordering is semantically valid,” or “UT already provides semantic-preservation guarantees comparable to CompCert.”

**Assumptions / validity boundary**

CompCert's theorem applies to its formally modeled source/target languages, passes and stated conditions.

**Strongest prior art / alternative**

Formal proof of simulation/preservation.

**Open question**

What lighter-weight evidence is sufficient for extensible systems where full mechanized proof is impractical?

**Deck consequence**

Use as the correctness boundary when introducing `Obligation` or cross-representation correspondence.

---

## CLAIM_ID: PA-TRANSLATION-VALIDATION

**Proposed claim**

Checking each generated source→target translation for correctness is established compiler-verification prior art.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: Pnueli, Siegel, Singerman
- revision/date: TACAS 1998; bibliographic/source review 2026-09-06
- path/paper: *Translation Validation*, DOI `10.1007/BFb0054170`
- test/function/section: per-run validation concept
- external source type: peer-reviewed conference paper / Springer bibliographic record

**Observed support**

The classic approach validates each individual compiler translation after the run instead of proving once that the entire compiler always translates correctly.

**Safe conference wording**

“Per-translation correctness checking is established prior art; any proposed cross-representation evidence must specify the relation it validates.”

**Unsafe / prohibited wording**

“Checking correspondence after lowering is a new idea.”

**Assumptions / validity boundary**

Strength depends on the validator, source/target semantics and relation being checked.

**Strongest prior art / alternative**

CompCert for proof-oriented verification; Alive2 for an automated LLVM refinement validator.

**Open question**

Could translation validation at selected extensible boundaries replace a persistent shared evidence layer?

**Deck consequence**

Include in strongest-alternative reasoning; avoid generic “correspondence” novelty claims.

---

## CLAIM_ID: PA-ALIVE2-REFINEMENT

**Proposed claim**

Alive2 is a concrete automated baseline for bounded refinement/translation validation of LLVM IR transformations.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: Lopes, Lee, Hur, Liu, Regehr
- revision/date: PLDI 2021; source reviewed 2026-09-06
- path/paper: *Alive2: Bounded Translation Validation for LLVM*, DOI `10.1145/3453483.3454030`, `https://web.ist.utl.pt/nuno.lopes/pubs.php?id=alive2-pldi21`
- test/function/section: SMT-based bounded translation validation
- external source type: peer-reviewed paper + author publication page

**Observed support**

Alive2 checks LLVM IR transformations automatically with SMT-based refinement reasoning, intentionally bounding some resources/loops; the authors report that bounds can cause missed bugs while designing the tool to avoid false alarms.

**Safe conference wording**

“Alive2 shows that concrete IR transformations can be checked against a formal refinement relation, though with explicit boundedness limitations.”

**Unsafe / prohibited wording**

“No practical compiler checks transformations across IR states,” or “Alive2 proves arbitrary cross-language lowering.”

**Assumptions / validity boundary**

LLVM IR semantics and Alive2's supported/bounded model.

**Strongest prior art / alternative**

A concrete validation alternative to carrying persistent semantic evidence.

**Open question**

Which transformations need persistent evidence identity versus post-hoc refinement validation?

**Deck consequence**

Use to sharpen the meaning of “correspondence” and falsification criteria.

---

## CLAIM_ID: PA-CORECLR-GC-WRITE-BARRIER

**Proposed claim**

For CoreCLR, preserving the appropriate GC write-barrier behavior is a concrete runtime/JIT lowering obligation for managed-reference stores whose destination may be on the GC heap.

**Class**

`PRIOR ART`

**Evidence identity**

- repository/source: `dotnet/runtime` official design/source documentation
- revision/date: current `main` docs reviewed 2026-09-06
- path/paper: `https://github.com/dotnet/runtime/blob/main/docs/design/coreclr/jit/GC-write-barriers.md`; `https://github.com/dotnet/runtime/blob/main/docs/design/coreclr/botr/readytorun-overview.md`; `https://github.com/dotnet/runtime/blob/main/docs/design/coreclr/jit/object-stack-allocation.md`
- test/function/section: `JIT_WriteBarrier` / checked barrier description; reference-field update bookkeeping; stack-vs-heap barrier selection
- external source type: current upstream runtime/JIT design docs

**Observed support**

CoreCLR's generational GC needs bookkeeping when a heap object reference field is updated. JIT/runtime documentation distinguishes normal, checked and no-barrier cases depending on whether the destination is known heap, known stack, or may be either. The barrier performs the store plus GC bookkeeping.

**Safe conference wording**

“A managed reference store may carry a GC-barrier obligation at lowering/codegen time; whether a normal, checked or no barrier is legal depends on runtime/JIT facts.”

**Unsafe / prohibited wording**

“Every write needs a GC barrier,” “GC barrier is a source-language writability property,” or “one abstract `Write` interface automatically captures all GC/runtime semantics.”

**Assumptions / validity boundary**

CoreCLR generational-GC/JIT behavior; the exact helper and optimization vary by architecture/runtime state.

**Strongest prior art / alternative**

Existing JIT/runtime-specific store lowering and GC contracts.

**Open question**

Can a higher-level obligation abstraction preserve this requirement without obscuring the runtime-specific proof/discharge mechanism?

**Deck consequence**

Keep GC barrier as a concrete example of a lowering obligation, but place it at the runtime/codegen boundary and avoid turning it into proof of a universal semantic model.

---

## CLAIM_ID: CONCLUSION-INDEPENDENT-COMPOSITION-NOVELTY

**Proposed claim**

“Independently authored language extensions can compose into one language” is not a defensible novelty claim for this talk.

**Class**

`REJECTED`

**Evidence identity**

- repository/source: Silver/ableC, Neverlang, JetBrains MPS, MontiCore
- revision/date: sources reviewed 2026-09-06
- path/paper: see `PA-SILVER-ABLEC`, `PA-NEVERLANG`, `PA-MPS`, `PA-MONTICORE`
- test/function/section: cross-system prior-art comparison
- external source type: official docs + peer-reviewed research

**Observed support**

Multiple mature systems explicitly support independently developed or modular language features/components, composition, ordering and reuse.

**Safe conference wording**

“Independent language extension is our starting problem, not our claimed invention.”

**Unsafe / prohibited wording**

“Existing systems require all extension authors to coordinate pairwise,” or “no system composes independently authored language pieces.”

**Assumptions / validity boundary**

Different systems guarantee different properties; prior art refutes only the broad novelty claim, not every narrower research question.

**Strongest prior art / alternative**

Silver/ableC is particularly strong because it combines independent development with modular composition analyses.

**Open question**

Which narrower coupling/validity problem remains after acknowledging this prior art?

**Deck consequence**

Rewrite any broad novelty framing in Phase 03.

---

## CLAIM_ID: CONCLUSION-COMPOSABILITY-NOT-SOUNDNESS

**Proposed claim**

Language-component composability must not be equated with semantic non-interference, soundness or preservation.

**Class**

`GENERAL DESIGN`

**Evidence identity**

- repository/source: cross-system evidence review
- revision/date: reviewed 2026-09-06
- path/paper: Silver modular well-definedness; Neverlang 2026 `nlgcheck` preprint; MPS generation ordering; MontiCore composition; CompCert preservation
- test/function/section: comparative evidence boundary
- external source type: official docs + research literature

**Observed support**

Prior-art systems attach different guarantees to composition. Silver requires specific modular analyses; Neverlang documents correctness gaps under loose dynamic attributes; MPS/MontiCore composition mechanisms do not claim a universal behavioral preservation theorem; CompCert shows how much stronger a semantic-preservation statement is.

**Safe conference wording**

“Composition answers ‘can these pieces be assembled under these rules?’ Soundness/preservation is a separate claim that requires its own evidence.”

**Unsafe / prohibited wording**

“If the planner found a plan, the composed language is semantically sound.”

**Assumptions / validity boundary**

“Soundness” must always be defined relative to a particular semantic property/relation.

**Strongest prior art / alternative**

Formal preservation and translation-validation approaches.

**Open question**

Which obligations can be checked modularly at composition time, and which require representation-specific validation or proof?

**Deck consequence**

Make this distinction explicit before the semantic-research section.

---

## CLAIM_ID: CONCLUSION-GENERIC-SEMANTIC-QUERY-NOVELTY

**Proposed claim**

“Generic semantic queries plus validity/invalidation” is not a defensible novelty claim by itself.

**Class**

`REJECTED`

**Evidence identity**

- repository/source: LLVM and MLIR official documentation
- revision/date: current docs reviewed 2026-09-06
- path/paper: see `PA-LLVM-ANALYSIS-INVALIDATION`, `PA-MLIR-SEMANTIC-INTERFACES`
- test/function/section: AnalysisManager/PreservedAnalyses; interfaces/external models/effects/data-flow
- external source type: upstream compiler documentation

**Observed support**

LLVM and MLIR already let consumers query generic analysis/semantic interfaces and explicitly reason about preservation or invalidation. MLIR also supports external interface models and generic effect queries.

**Safe conference wording**

“The research question is not whether generic queries or invalidation exist; it is whether a smaller cross-component evidence lifecycle solves a coupling problem those local mechanisms leave awkward.”

**Unsafe / prohibited wording**

“Existing compilers wire every producer directly to every consumer,” or “validity metadata is new.”

**Assumptions / validity boundary**

A new combination may still be useful, but usefulness/novelty requires comparison and experiments rather than terminology differences.

**Strongest prior art / alternative**

LLVM AnalysisManager + MLIR interfaces/external models + local adapters.

**Open question**

Can a benchmark demonstrate fewer pairwise changes when adding a producer while maintaining fail-closed correctness and comparable analysis precision?

**Deck consequence**

Phase 03 must make LLVM/MLIR the baseline, not a strawman.

---

## CLAIM_ID: CONCLUSION-PLANNER-NOT-PRESERVATION

**Proposed claim**

UT's current planner establishes structural admissibility/executable-route selection, not semantic preservation across transformations.

**Class**

`GENERAL DESIGN`

**Evidence identity**

- repository/source: UT planner regression + CompCert/translation-validation/Alive2 prior art
- revision/date: UT `40117eb68c630f7129c120aaaadc69be8f4ecbfb`; external sources reviewed 2026-09-06
- path/paper: `PlannerPolicyControlTests.cs`; CompCert compiler theorem; Pnueli/Siegel/Singerman; Alive2
- test/function/section: `RouteSearch_ShouldChooseMoreExpensiveRoute_WhenCheaperRouteViolatesDescriptorOrder`
- external source type: current code/test + formal/peer-reviewed correctness baselines

**Observed support**

The UT test checks artifact connectivity, hard contribution ordering and selected route identity. It contains no source-target semantic relation. Prior-art correctness systems explicitly define and prove/validate such relations.

**Safe conference wording**

“The planner decides which route is structurally feasible under declared contracts; semantic preservation must come from separate proofs, validators, obligations or trusted transformation contracts.”

**Unsafe / prohibited wording**

“Feasible means semantics-preserving.”

**Assumptions / validity boundary**

Some artifact contracts may encode semantic intent, but the reviewed route test does not prove that intent is preserved.

**Strongest prior art / alternative**

CompCert simulations; per-translation validation; Alive2 refinement.

**Open question**

What is the minimum semantic contract a route step must expose so that a plan can compose preservation evidence without pretending to prove more than it knows?

**Deck consequence**

Mandatory wording boundary in Phase 03.

---

## CLAIM_ID: RESEARCH-SHARED-EVIDENCE-LIFECYCLE

**Proposed claim**

A falsifiable remaining research question is whether a minimal typed lifecycle for semantic evidence identity, context/revision validity, contradiction and obligation discharge can reduce coupling across independently authored producers/consumers and changing representations without centralizing domain analyses.

**Class**

`RESEARCH HYPOTHESIS`

**Evidence identity**

- repository/source: this evidence review + current presentation architecture hypothesis
- revision/date: reviewed 2026-09-06
- path/paper: strongest alternatives `PA-LLVM-ANALYSIS-INVALIDATION`, `PA-MLIR-SEMANTIC-INTERFACES`, `PA-TRANSLATION-VALIDATION`, `PA-ALIVE2-REFINEMENT`
- test/function/section: not implemented in current UT
- external source type: research framing derived from gap analysis, not implementation evidence

**Observed support**

The review establishes that the broad ingredients—independent composition, interfaces, effect queries, analysis managers, invalidation, legality and translation validation—already exist. It did not identify, within this bounded source set, one mechanism whose explicit abstraction boundary is exactly “typed cross-component evidence object with stable semantic identity + context/revision validity + contradiction policy + obligation discharge across multiple changing representations.” That absence is **not** proof of novelty.

**Safe conference wording**

“Our hypothesis is narrower: perhaps the missing reusable boundary is the lifecycle of semantic evidence across independent producers, consumers and representations. We need to test whether that boundary reduces coupling without weakening soundness.”

**Unsafe / prohibited wording**

“No prior compiler has semantic evidence validity,” “we invented semantic interfaces,” “this layer is necessary,” or “the architecture is novel because we did not find an identical class name.”

**Assumptions / validity boundary**

Research-only. Current UT does not implement the proposed universal/shared semantic evidence lifecycle. Novelty remains unproven until a broader literature review and direct experimental comparison against LLVM/MLIR/local-adapter designs.

**Strongest prior art / alternative**

LLVM AnalysisManager/PreservedAnalyses; MLIR interfaces/external models/effects/data-flow; local domain-specific analyses with explicit adapters; translation validation; Alive2 refinement.

**Open question**

Primary falsification tests:
1. add a new producer and change zero existing consumers while preserving fail-closed behavior;
2. mutate/lower the representation and demonstrate stale evidence cannot discharge an obligation;
3. introduce contradictory evidence and demonstrate deterministic conservative resolution;
4. compare implementation coupling and precision against an MLIR-interface/local-analysis baseline;
5. if the shared layer adds machinery without measurable coupling/verification benefit, remove it.

**Deck consequence**

Keep only as the central **research hypothesis**, not as implemented UT behavior or proven novelty. Phase 03 should organize the semantic half of the talk around these falsification conditions.

---

## Source-fidelity disposition for Phase 02

No narrow correction to `claims.md`, deck source or speaker script was required during this phase. The implementation-facing statements inspected for this ledger are supportable at the bounded strengths recorded above. The broad novelty implications are the problem, and those belong to Phase 03 content repair rather than a Phase 02 source hotfix.

## Phase 03 handoff constraints derived from this ledger

- Treat independent language-extension composition as prior art, not novelty.
- Treat global/resolved planning and cross-extension ordering as prior art-adjacent; distinguish UT only by the exact responsibility it adds.
- Preserve the concrete UT witnesses: declarative profiles, staged planning, feasibility-before-preference regression, local typed-intrinsic deabstraction, bounded backend parity.
- Never infer semantic preservation from structural plan feasibility.
- Introduce LLVM and MLIR as strongest alternatives before proposing the shared semantic-evidence lifecycle.
- Locate the CoreCLR GC write-barrier example at the runtime/JIT lowering-obligation boundary.
- Present `Judgement` / `Obligation` / evidence validity terminology as proposed modeling, not established implementation or novelty.
- Make falsification operational: producer addition, stale evidence, contradiction, representation change, and comparison against local-interface/adaptor baselines.
