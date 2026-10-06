# LangDev final rebuild: evidence and narrative

Authority: presentation working record, not a compiler architecture contract.
Investigated 2026-10-06 before editing the production presentation.

## Source baseline

- Production deck: `Misha1302/lang-dev-presentation-2026`, `92a0e1d` (13-slide self-contained HTML).
- `Misha1302/Wist2` redirects to `Misha1302/UniversalToolchain`.
- Current compiler source inspected in `/home/micodiy/razakov/sharp/Wist2`, commit `1d46f17c8dc28f434fa58bdf92f9f8278fa5aaee`.
- Governing documents: AGENTS.md, documentation authority index, current architecture status, syntax ownership rules, documentation rules and project rules. Public current contracts take precedence over historical talk material.

All compiler links in the deck pin this source commit. Pseudocode is explicitly identified at the fragment/section level. No measured speedup, formal completeness or production SIMD claim is made.

## Evidence map

Paths below are relative to the pinned compiler repository.

| Claim | Source | Status | Usable in talk? |
|---|---|---|---|
| Wist accepts `100.0 * 0.9 + 5.0` | `UniversalToolchain/Dialects/examples/wist/pricing-restricted/program.wist`, adjacent README | IMPLEMENTED | Yes, real running example |
| NativeTypes owns number lexing, arithmetic node creators and lowerers | `UniversalToolchain/NativeMathModule/NativeTypesModuleImpl.cs`, `NativeArithmeticAstVisitor.cs`, `NativeNumberAstVisitor.cs` | IMPLEMENTED | Yes, feature crosscut witness |
| PricingRestricted selects Identifier, NativeTypes, Scopes, Variables, Whitespaces; excludes Arithmetic and general control/interop modules | shipped `dialect.wistdialect`; `UniversalToolchain/UniversalToolchain.Dialects.Tests/WistDialectProfileContractTests.cs` | TESTED / OBSERVED | Yes; do not list Arithmetic as selected |
| Exclusions are contribution constraints, not runtime feature toggles | `docs/CURRENT_ARCHITECTURE_STATUS.md`; `WistFacadeLanguageDefinitionFactory`; planner resolution phases | IMPLEMENTED | Yes |
| LanguageCompiler.Compile resolves features, contributions, runtime provider and routes | `UniversalToolchain/UniversalToolchain.LanguageSdk/LanguageCompiler.cs` | IMPLEMENTED | Yes, actual API |
| LanguagePlan snapshots Definition, Features, Contributions, RuntimeProvider, Routes, PlanHash | adjacent `LanguagePlan.cs` | IMPLEMENTED | Yes; not a whole-program semantic proof |
| Runtime follows one selected plan, without a second composition decision | `docs/CURRENT_ARCHITECTURE_STATUS.md`; `UniversalToolchain/UniversalToolchain.Runtime/LanguageRuntime.cs` | IMPLEMENTED | Yes |
| Wist syntax → semantic binding → Bytecode → AIR → selected backend | current architecture status; `docs/architecture/lowering-walkthrough.md`; native visitors; `AbstractIrConverters/BytecodeToAbstractIrConverterImpl.cs` | IMPLEMENTED | Yes; binding must be visible, unlike stale walkthrough wording |
| Bytecode carries method representations, not conventional VM `mul`/`add` opcodes | `UniversalToolchain/UniversalToolchain.Wist.LanguagePack/WistSemanticBytecodeLowerer.Operations.Values.cs`, `.Operations.Arithmetic.cs`; native module visitors | IMPLEMENTED | Yes, simplified method labels, no invented bytecode dump |
| AIR uses Push and represented managed calls for native arithmetic | bound Wist semantic lowerer above, `NativeArithmetic.cs`, Bytecode converter | IMPLEMENTED | Yes, semantic sketch; optimizers may fold literals |
| CIL backend produces DynamicMethod; typed external intrinsic emits Ldarg(slot + offset) | `BytecodeDynamicMethodsCompiler/Compilers/AbstractMethodsCompilerImpl.cs`, `AbstractMethodsIntrinsicCompiler.cs`; `BasicCilCompiler/Execution/DynamicMethodExecutor.cs` | IMPLEMENTED | Yes |
| Exact environment/slot/external-load sequence becomes typed LoadExternal intrinsic only with capability support | `NativeMathModule/NativeCILOptimizerModule.cs`; `UniversalToolchain.Modules.Tests/ModuleCoverage/TypedIntrinsicEmitterOptimizerTests.cs` | TESTED / OBSERVED | Yes, exact 3→1 witness; no zero-cost claim |
| External/local binding overlap is protected by deterministic interpreter/CIL parity checks | `Tests/Backends/InterpreterBindingsParityTests.cs`, `ShadowingAndNestedScope_WithLocalNamesOverlappingExternals_ShouldBeDeterministicAndParityStable` | TESTED / OBSERVED | Yes; test asserts equality/determinism, not a recorded historical wrong output |
| Current shadowing example returns 2 in both backends | direct `WistEngine.Evaluate<double>` probe, full-default-native, host price=10.0/fee=1.0; performed 2026-10-06 | TESTED / OBSERVED | Yes; current observed result, not historical bug output |
| External reads previously shared local storage lowering; fix separates slot-based external loads | commit `bc104d04cadfd4522ae5abf4b5f426952c6e9d2b`, VariablesVisitor diff and added ExternalBindings_ReadsMustWorkWithoutLocalContainerStorage test | IMPLEMENTED (historical fix) | Yes; do not invent an old incorrect result |
| Semantic evidence, typed predicates, rules, provenance and fail-closed queries | `docs/research/semantic-fact-proof-layer-2026-09-20.md` | DESIGN DIRECTION | Yes, section explicitly proposed |
| Adding dependency evidence can discharge an existing SIMD obligation | adapted bounded example, not production API | HYPOTHESIS | Yes, conceptual loop; retain lane/type/bounds assumptions and separate profitability |
| Actual production SIMD vectorizer/proof engine | no supporting implementation found | UNKNOWN | No |
| MLIR interfaces/external models provide decoupled semantic hooks | https://mlir.llvm.org/docs/Interfaces/ | IMPLEMENTED (prior art) | Yes |
| LLVM AnalysisManager/PreservedAnalyses cache and invalidate analyses | https://llvm.org/docs/NewPassManager.html | IMPLEMENTED (prior art) | Yes |
| Silver/ableC compose syntax and semantics through attribute grammars | https://melt.cs.umn.edu/ableC/ | IMPLEMENTED (prior art) | Yes |
| Soufflé provenance explains derived tuples via proof trees | https://souffle-lang.github.io/provenance | IMPLEMENTED (prior art) | Yes |
| Shared layer beats interfaces/analysis managers | no comparative evaluation | UNKNOWN | No; formulate a falsifiable experiment instead |

## History investigation

| Old visual detail | Why it worked | Reuse / adaptation |
|---|---|---|
| `7094974`: compact pipeline, two kinds of disappearance | Connects configuration staging to local IR specialization | Two narrowing gates recur on slides 5, 7, 16 |
| `9b101b9`: before/after alternatives, fixed LanguagePlan fields | Makes a plan a resolved decision rather than a named box | Slide 5 shows unresolved choices → exact public plan fields |
| `216eddd`: exact 3→1 external-load rewrite and central capability gate | Makes disappearing abstraction falsifiable and concrete | Slide 7 retains mechanism and adds actual CIL argument lowering |
| `92a0e1d`: colored module lanes and proof DAG | Encodes crosscutting ownership and derivation | Slides 2, 11 use connected paths and consistent colors; enlarge all labels |
| Earlier core-orbit/cloud and repeated cards | Relations are weak; claims are largely oral | Do not reuse |

## Spoken narrative / WHAT I SAY

Each row supplies an anchor, 3–5 visible reasoning steps, and a causal transition. Notes in the HTML mirror this outline, not a full script.

| Slide | Seconds | Visible reasoning / transition |
|---|---:|---|
| 1 | 45 | Real Wist expression → reusable framework → open composition → concrete .NET execution. Why can one feature be reused? |
| 2 | 65 | NativeTypes contributes tokens → AST → lowering → numeric operations. A feature crosses stages, so one plugin hook is insufficient. |
| 3 | 65 | Monolithic edits → module-owned contributions → dialect selection. Published extension contracts move ownership out of the core. What language does this build? |
| 4 | 75 | Exact PricingRestricted selection → native arithmetic works → loops/conditions/interop excluded. Selection defines the language; global compatibility still needs resolution. |
| 5 | 90 | Definition + registered packages → unresolved choices → Compile → immutable plan fields. Runtime materializes that answer. Now compile a program. |
| 6 | 95 | Same Wist expression → syntax tree → semantic binding → module Bytecode → AIR → interpreter/CIL → 95.0. Representation becomes executable. |
| 7 | 75 | Generic environment load → exact local match + capability → typed intrinsic → CIL argument load. Removal is a concrete conditional rewrite. What must remain invariant? |
| 8 | 90 | Host price/fee → local price declaration → binding/storage identities → deterministic interpreter/CIL parity. Test-backed regression guard, no invented wrong output. Structure alone does not settle all future semantic questions. |
| 9 | 65 | Current plan/representations/parity → multiple components need meaning → proposed evidence/rule boundary. Binding stays binder-owned. Ask about a future optimizer. |
| 10 | 85 | One conceptual SIMD loop → direct dependencies and combination logic → one obligation query → unchanged scalar fallback unless proven. How is an answer derived? |
| 11 | 100 | Two dependency facts → IndependentIterations; purity + target support → legality under fixed type/bounds/lane assumptions. Cost is separate. What if a premise is missing? |
| 12 | 95 | Same consumer UNKNOWN → new DependencyAnalysis evidence/rule → same query PROVED. Consumer unchanged, knowledge changes; monotonicity only for current valid evidence. |
| 13 | 75 | Providers publish typed scoped evidence → rules derive → consumer queries. Subject, scope, revision remain aligned; no runtime activation by projection. How do we explain and invalidate the answer? |
| 14 | 85 | Derivation names producer/rule → changed loop invalidates premise → obligation returns UNKNOWN → scalar fallback/recompute. Unknown differs from disproven; conflicts fail closed. |
| 15 | 75 | Serious precedents already exist → distinguish their integration boundaries → evaluate shared boundary against strongest local baseline. Contribution remains a question, not a novelty claim. |
| 16 | 75 | Revisit module choices → plan → program representations → specialized CIL → DynamicMethod → .NET JIT. Decisions and local machinery disappear at different gates; no universal cost claim. |
| 17 | 30 | Compose structure → agree on meaning → specialize representation. Show code/research links; invite questions. |

Total: **1285 seconds = 21:25**, excluding audience Q&A. This is a rehearsal allocation, not a measured delivery duration.

## Evidence gaps deliberately left out

- No captured historical incorrect shadowing result; only the real regression guard and its asserted contract are shown.
- No production SIMD/proof engine or measured advantage over LLVM/MLIR-style integration.
- IR fragments are explanatory unoptimized sketches, not a captured dump of the constant-folded production preset.

## Executed compiler evidence

- Shipped PricingRestricted program, `Wistc run`: interpreter **95**, CIL **95**.
- `InterpreterBindingsParityTests`: **10 passed** (built and executed at the source baseline).
- `WistDialectProfileContractTests`: **7 passed**.
- Focused `NativeCilOptimizer` module tests: **5 passed**.
- Public-facade probe at the same source baseline: full-default-native; `let price = fee\nprice + fee`; arguments `{ price = 10.0, fee = 1.0 }`; interpreter **2**, CIL **2**.
- The shadowing parity helper intentionally compares both success and deterministic failure outcomes. The slide's numeric result is supported by the separate successful probe, not inferred solely from a passing equality assertion.
- Source worktrees were not edited. Test builds and the disposable external probe generated only build artifacts.

## Existing documentation drift

The production deck had 13 slides, while its README and CI still described/required 24 delegate-focused slides. The rebuild updates those stale presentation contracts together with the deck. Compiler implementation is unchanged.
