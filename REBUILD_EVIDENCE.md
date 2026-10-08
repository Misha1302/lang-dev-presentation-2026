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

## Original 17-slide spoken allocation (superseded by the 2026-10-08 audit)

Each row supplies an anchor, 3–5 visible reasoning steps, and a causal transition. Notes in the HTML mirror this outline, not a full script.

| Slide | Seconds | Visible reasoning / transition |
|---|---:|---|
| 1 | 60 | Real Wist expression → reusable framework → open composition → concrete .NET execution. Why can one feature be reused? |
| 2 | 80 | NativeTypes contributes tokens → AST → lowering → numeric operations. A feature crosses stages, so one plugin hook is insufficient. |
| 3 | 80 | Monolithic edits → module-owned contributions → dialect selection. Published extension contracts move ownership out of the core. What language does this build? |
| 4 | 90 | Exact PricingRestricted selection → native arithmetic works → loops/conditions/interop excluded. Selection defines the language; global compatibility still needs resolution. |
| 5 | 110 | Definition + registered packages → unresolved choices → Compile → immutable plan fields. Runtime materializes that answer. Now compile a program. |
| 6 | 120 | Same Wist expression → syntax tree → semantic binding → module Bytecode → AIR → interpreter/CIL → 95.0. Representation becomes executable. |
| 7 | 90 | Generic environment load → exact local match + capability → typed intrinsic → CIL argument load. Removal is a concrete conditional rewrite. What must remain invariant? |
| 8 | 115 | Host price/fee → local price declaration → binding/storage identities → deterministic interpreter/CIL parity. Test-backed regression guard, no invented wrong output. Structure alone does not settle all future semantic questions. |
| 9 | 45 | Current plan/representations/parity → multiple components need meaning → proposed evidence/rule boundary. Binding stays binder-owned. Ask about a future optimizer. |
| 10 | 55 | One conceptual SIMD loop → direct dependencies and combination logic → one obligation query → unchanged scalar fallback unless proven. How is an answer derived? |
| 11 | 65 | Two dependency facts → IndependentIterations; purity + target support → legality under fixed type/bounds/lane assumptions. Cost is separate. What if a premise is missing? |
| 12 | 50 | Same consumer UNKNOWN → new DependencyAnalysis evidence/rule → same query PROVED. Consumer unchanged, knowledge changes; monotonicity only for current valid evidence. |
| 13 | 45 | Providers publish typed scoped evidence → rules derive → consumer queries. Subject, scope, revision remain aligned; no runtime activation by projection. How do we explain and invalidate the answer? |
| 14 | 50 | Derivation names producer/rule → changed loop invalidates premise → obligation returns UNKNOWN → scalar fallback/recompute. Unknown differs from disproven; conflicts fail closed. |
| 15 | 50 | Serious precedents already exist → distinguish their integration boundaries → evaluate shared boundary against strongest local baseline. Contribution remains a question, not a novelty claim. |
| 16 | 100 | Revisit module choices → plan → program representations → specialized CIL → DynamicMethod → .NET JIT. Decisions and local machinery disappear at different gates; no universal cost claim. |
| 17 | 55 | Compose structure → agree on meaning → specialize representation. Show code/research links; invite questions. |

Total: **1260 seconds = 21:00**, excluding audience Q&A. Slides 1–8 and 16–17 receive **900 seconds = 15:00**; slides 9–15 are a bounded **360 seconds = 6:00 research outlook**. This is a rehearsal allocation, not a measured delivery duration.

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

## 2026-10-08 narrative and cognitive investigation

### Authority and method

Baseline: current remote main `128d6f910d35f2aebedd95a3efd432be9a019ea9`, freshly cloned into an isolated checkout. Production HTML fetched on 2026-10-08 was byte-identical to that checkout: SHA-256 `4ce2c872727fdb574508aeb33d618ae1d06e7e4181332d513b71e76220e347d5`. Production was also opened in Chromium. No AGENTS.md exists in this checkout or its parent directories. The entire HTML was read, including styles, reveal/navigation logic, all detailed notes and the separate `shortNotes` map actually displayed by P. README, runbook, this evidence record, QA report, all four workflows and the complete validator were inspected.

The existing compiler checkout is clean and exactly matches the deck's pinned `1d46f17c8dc28f434fa58bdf92f9f8278fa5aaee`. Read-only verification covered current architecture status; LanguageCompiler/LanguagePlan; selected dialect; native lexer/parser/visitors; exact optimizer match and capability gate; intrinsic CIL emission; binding parity test; DynamicMethod/typed facade; and the full semantic-fact-proof research note. Compiler files were not changed. Previously recorded execution results remain historical evidence, not newly executed tests.

Recent history matters: `5dab7a2` intentionally introduced short SAY/NEXT notes and retained long notes hidden for validation. Thus a definition present only in the long notes is not a reliable delivery cue. `426b36c` moved the overlay; `ad114ab` made QRs offline-safe; `b970ffb` repaired contact navigation. The older `92a0e1d` DAG and explanation were inspected as historical design evidence, not restored: older material must not supersede the current binding/plan/proposal boundaries.

Analytical audience perspectives: compiler engineer; language-tooling researcher; systems/.NET developer; attentive first-time listener. These are author-side reasoning checks, not measured human comprehension. Browser observations and test results are identified separately below.

### Complete argument and dependency reconstruction

Question / claim / next dependency are listed for every slide. Timing is the actual baseline, not the stale 17-slide table above. Oral load estimates are analytical; no delivery duration was measured.

| Slide / seconds | Inherited question → principal claim → retained conclusion / next question | Required → new concepts; supporting evidence and oral load |
|---|---|---|
| 1 / 60 | What is the talk about? → open language composition, concrete execution → why is a feature hard to extend? | Compiler familiarity → UniversalToolchain framework vs Wist reference language. Real pricing formula. Four short beats; realistic. |
| 2 / 80 | Why one plugin hook is insufficient → a feature crosses stages → who owns the contributions? | Formula, pipeline → NativeTypes contributions. Source-linked lexer, parser and lowering methods; explain lanes as ownership, not dataflow. Realistic. |
| 3 / 80 | How to avoid central edits → modules own, dialect selects → what language results? | Crosscutting owner → dialect DSL, contribution contracts. Real excerpt vs explicitly conceptual monolith. Selection/resolution distinction spoken; realistic. |
| 4 / 90 | What does selection change? → actual restricted surface → who checks global compatibility? | Dialect/modules → exact five selected identities and excluded stack. Program/profile tests; NativeTypes vs Arithmetic explicitly resolved. Realistic. |
| 5 / 110 | How do local choices close? → one immutable LanguagePlan → how is a program compiled? | Selection → dependencies, provider/order/routes, PlanHash. Exact public API/snapshot fields. Clearly distinguish language planning from per-program binding. Enough time. |
| 6 / 120 | What consumes the plan? → source/binding/Bytecode/AIR/backend routes → what machinery can specialize? | Plan, arithmetic → project-specific method Bytecode and AIR. Explanatory unoptimized fragments, actual lowerers/emitter. Highest implementation explanation load, justified two minutes. AIR's local name needs expansion. |
| 7 / 90 | What exactly disappears? → capability-gated 3→1 external load → what meaning must survive? | AIR, backend → external slot/type/intrinsic. Exact match, unsupported-type preservation and ldarg source. Need brief oral host-slot context; sufficient time. |
| 8 / 115 | How do routes keep meaning? → binding identities, parity → who assembles answers spanning owners? | Binding/backend → shadowing/storage identity. Existing tests plus historical facade probe; no fabricated wrong output. A test is not a proof of universal parity. Sufficient time. |
| 9 / 45 | Does structural composition solve semantic cooperation? → proposed shared boundary → ask one concrete optimizer question | Current plan/binder/parity → evidence/rule/query preview. Explicit proposed marker protects epistemic boundary. Avoid treating unintroduced 'premises' as settled vocabulary. |
| 10 / 55 | What question spans owners? → legality query decouples vectorizer → how is an answer derived? | Compiler analyses → obligation and bounded illustrative SIMD loop. Goal/fallback already visible. Cost is separate; lane/type/bounds/traps assumptions exist, tail handling should be explicit. Realistic if vocabulary is contextual. |
| 11 / 65 | Why can the query succeed? → derivation combines owned facts → what if one input is unavailable? | Query/loop → premise, rule, base vs derived fact, proof. DAG distinguishes colors but not actual producers or AND-rule junctions. Missing authority boundary; highest research conceptual load, allocate more time here. |
| 12 / 50 | What does extensibility buy? → missing evidence can satisfy existing query → generalize this contract | Derivation → Unknown→Proved with unchanged consumer. Existing rule vs new provider ambiguous; same facts renamed later. Before/after visually strong; retain it and make fixed-rule assumption explicit. |
| 13 / 45 | What stays shared? → providers/rules/consumer contract → what expires? | Running example → predicate naming, scoped identity/revision. Three synonyms for dependency facts and 'relation' add avoidable debt. Rules belong to the shared semantic contract; no need for a separate ontology lesson. |
| 14 / 50 | Why and until when is a proof valid? → dependency provenance + invalidation → compare prior art | Rules, facts, identity → proof provenance, revision validity, conflict. Trace needs to be identified as an excerpt; invalidating one path does not always destroy every proof. Explicit negative evidence/Disproven absent from actual SAY notes. |
| 15 / 50 | Is this mechanism new or necessary? → prior art plus falsifiable integration experiment → return to execution | Evidence contract → four established approaches/baseline. Primary docs checked. Fair strengths and modest proposal; no competitive superiority claim. Dense but readable table; time sufficient for comparison at integration level, not four tutorials. |
| 16 / 100 | How does outlook connect to title? → two implemented narrowing gates → synthesize responsibilities | Plan and local rewrite → DynamicMethod/typed artifact return. Clearly re-enters implemented story; proposed evidence is not shown as a shipped stage. Sufficient time. |
| 17 / 55 | What should remain? → compose / agree / execute → contacts and Q&A | Entire argument → no new machinery. Correct summary and separate code/research links. Keep content. |
| 18 / 30 | How to continue? → persistent links/QRs → Q&A | No conceptual prerequisite beyond project identity. Four embedded QRs; browser-width media queries conflict with uniformly scaled fixed stage. Runbook omits this slide. |

Directed dependencies (edge roles explicitly separated):

```text
Conceptual prerequisites:
1 → 2 → 3 → 4 → 5 → 6 → 7
                    5 → 9; 6/7 → 8; 8 → 9
9 → 10 [motivation]; 10 → 11 [query and fixed loop assumptions]
11 → 12 [rule premises]; 11/12 → 13 [generalize example]
11/13 → 14 [proof dependencies and scoped revision]
9/13/14 → 15 [evaluate integration hypothesis]
5/7/8 → 16 → 17 → 18 [return, synthesis, handoff]

Implementation demonstrations: 2, 4, 5, 6, 7, 8, 16.
Evidence-supported engineering conclusions: 4, 5, 7, 8.
Research boundary: 9. Illustrative proposed scenario: 10–14.
Prior-art evidence + speculative evaluation: 15.
Causal reasoning: crosscutting feature → ownership → selection → resolution;
exact match + support → rewrite; valid premises + scoped rules → permission;
changed artifact → invalidate dependent proof path → re-query.
```

No necessary reorder found. The significant cognitive debt begins at the research example, not in the implemented compiler story. The two successful specialization/parity examples are complementary, not redundant.

### First-use terminology map (actual baseline)

V = visible; S = actually displayed SAY/NEXT; L = hidden long notes. An early word alone is not counted as an explanation.

| Class / term | First appearance | Explanation / concrete example / first essential reasoning | Diagnosis |
|---|---|---|---|
| A: lexer, AST, lowering, CIL, interpreter, JIT | 2 (CIL/interpreter 3; JIT 6) | Familiar compiler terms; 2 stage witness and 6 executable example | No general glossary warranted. |
| A/B: semantic binding | 6 V/L | 6 type binding, concrete name/storage example 8; reasoning 8 | Sound sequence; short note 6 should preserve binding step. |
| B: UniversalToolchain vs Wist | 1 V | 1 explicitly framework/reference language; examples 1 onward | Stable; keep. |
| B: contribution / dialect | 2 V, 3 V | 2 methods + 3 DSL; concrete selection 4; resolution 5 | Explained before essential use. |
| B: LanguagePlan / PlanHash | 5 V | Exact fields/API 5; runtime/program split 5–6; reused 9/16 | Actual snapshots, not whole-program proof. Keep. |
| B: Bytecode / AIR | Bytecode 2, AIR 6 | 6 method representations/push-call sketch; specialization 7 | Project Bytecode meaning is explicit; expand AIR as Abstract IR. |
| B: external slot / typed intrinsic | 7 V | 7 three-instruction witness and CIL argument; binding example 8 | Short host-slot cue supplies motivation without moving slide 8. |
| C: evidence / fact | 9 V/S, fact 11 V | Named but not locally defined; example 11; essential derivation 11 | Evidence is a scoped assertion of a fact with origin/authority. Base and derived are roles, not unrelated logical species. Define in example. |
| C: premise | 8 S transition, 9 V | First dependency inputs 11, but no explicit definition | Replace early word with 'parts of the answer'; label rule inputs as premises when demonstrated. |
| C: rule | 9 V/L | Graph 11, symbolic rule 13; essential reasoning 11 | Arrows could mean dataflow, inference OR, or execution. Label R1/R2 and all-input requirement at first derivation. |
| C: obligation / query | 10 V/L | LegallyVectorizable(loop), isProven and fallback 10; graph 11 | Goal exists already. Define obligation as required property; query asks its proof status. |
| C: predicate / relation | 13 V ('relation'), 15 V | Typed syntax in 13; no needed independent relational example | Use one 'property' term. S13 may identify Pure(compute) as property applied to an entity; no ontology slide. |
| C: derived fact | 11 V | Cyan IndependentIterations; derivation essential 11 | Contextual legend and R1 establish it. |
| C: proof | 10 S, 11 L | Derivation 11; explanation 14 | Proof checks registered rules/premises, not arbitrary provider correctness. This omitted boundary matters technically. |
| C: Unknown / Disproven / conflict | Unknown 10 S, 12 V; conflict 14 V; Disproven not explained | Missing premise 12; invalidation 14; negative evidence absent | Unknown is already conservative, not falsely treated as false. Add explicit negative-evidence distinction at 14. |
| C: provenance / invalidation | 14 V | Producer/revision trace and r7→r8 scenario | Need not teach caches; name trace as partial and state no alternative valid path in this example. |

Source-supported distinctions: published evidence retains owner/verifier/rule origin; a fact is a typed proposition in context; a derived fact follows registered rules. A premise is a fact required by a rule. Predicate/schema versus instance is needed only to understand `Pure(compute)` and `LegallyVectorizable(L)`; use existing syntax as example. An obligation is a required proposition before an action, queried through the ordinary proof-status API. Provenance records the derivation and dependencies; it is not a second correctness proof. Missing evidence is Unknown, explicit negative evidence is Disproven, both polarities conflict, invalidation withdraws a stale path and requires another current proof. The source explicitly assigns reusable inference families to shared contract/framework maintainers, with ordinary providers publishing owned facts.

### Confirmed issues and selected repairs (diagnosis before slide edits)

| Priority / slides | Symptom, cause, evidence and audience consequence | Candidates → smallest selected repair / validation |
|---|---|---|
| P1 / 9–13 | Evidence/rule/premise roles reused before local explanation. DAG has unlabeled junctions and no producers; S11 merely repeats evidence/rules. Compiler engineer can infer logic, systems listener must guess; an attentive listener cannot tell why all inputs are necessary. Actual source + staged screenshots + displayed notes substantiate diagnosis. | No change leaves dependency unresolved; notes-only fragile; glossary adds isolated theory; reordering duplicates query slide 10. Combine A+C: introduce terms in existing example, producer labels and R1/R2 AND labels inside DAG, scoped fact/authority caption, short matching delivery cues. Test reveals and explain using only slides ≤11. |
| P1 / 11–14 | 'Proof' can imply provider truth is verified. Research note's Evidence authority section explicitly rejects that stronger interpretation; visible/short notes omit it. | Full authority taxonomy unnecessary. One visible sentence and one spoken cue bound proof to trusted/verified premises and registered rules. Preserve illustrative SIMD boundary and legality/cost separation. |
| P2 / 10–13 | The same dependency/target facts change names across slides; slide 12 says new evidence **and rule**, obscuring unchanged contract experiment. 'relation' adds a new label unnecessarily. | Define every synonym vs consistent short property names. Select consistent identifiers, explicit fixed rules/query and valid new facts; shared contract owns reusable rules. Re-read 11→12→13 with no imported terminology. |
| P2 / 10–11 | Existing type/lane/bounds/trap assumptions are sound but tail handling and exact supported operation are only implicit in illustrative support. | A real vectorizer tutorial unwarranted. Retain bounded example, name tail handling in assumptions and operation/lane support in note; no full legality or profitability guarantee. |
| P2 / 14 | Three outcomes omit Disproven; invalidation sounds unconditional, and trace omits other premises without saying it is an excerpt. Potential confusion between false, missing and stale evidence; one withdrawn proof need not remove an alternative. | Add four compact status labels, explicit-negative cue, excerpt label and no-other-proof assumption. Check against source's four-state model, reveal hierarchy and revision scope. |
| P1 / 18 | At 1024×768 and 390×844 contact media queries produce two/one-column content on a 1600×900 fixed stage; lower QR cards physically clipped. Existing fit test renders only slide 11, so misses it. Browser screenshots + geometry groups confirm. | Responsive redesign unnecessary. Remove two internal viewport queries; the existing uniform scaling owns responsiveness. Run all-slide geometry at required and non-16:9 sizes, inspect all four QRs. |
| P2 / 6–7 | AIR acronym has no expansion; active short note omits binding and host-slot setup although L notes include them. Recoverable project-specific term debt. | Expand local AIR label and keep binding/host input in existing short cues; no slide rearrangement. |
| P2 / docs/validator | Runbook says 21:00 and lacks slide 18; README claims displayed ANCHOR/FLOW/TRANSITION though actual UI is SAY/NEXT. Validator's ANCHOR check passes through a hidden legacy clone, not rendered notes. | Synchronize actual runbook/README/evidence timing. Check visible SAY/tail and note availability on every slide; keep detailed-note contract too. Expand geometry viewports, no weakened checks. |

No P0 technical contradiction found in source-backed slides 1–8/16. A successful parity regression is not universal formal semantic equivalence; existing slides correctly scope it. UNKNOWN already has safe fallback, contradicting the stronger initial suspicion that it might be treated as false. Research markers already clearly separate proposal from implementation. Prior-art table fairly credits [MLIR decoupled interfaces/external models](https://mlir.llvm.org/docs/Interfaces/), [LLVM cached analysis/invalidation](https://llvm.org/docs/NewPassManager.html), [ableC extension composition](https://melt.cs.umn.edu/ableC/), and [Soufflé derivation provenance](https://souffle-lang.github.io/provenance); primary documents checked on 2026-10-08. No novelty or superiority claim needs removal.

### Repair alternatives and pacing decision

A (no new slide) is sufficient **with** C (contextual DAG definitions): slide 10 already motivates the query, and the existing graph can teach evidence/premises/rules with its real inputs. B adds at least 30–45 seconds or steals core engineering time, then duplicates slide 13. D's concrete-before-abstraction goal is already substantially met by 10→11; moving 13 before 11 makes the first-time explanation more abstract. Pure C without spoken synchronization leaves the actual presenter cues underspecified. No change is appropriate for 1–5, 8, 15–17 and the dark technical visual system.

Selected mutation scope: local labels/notes on 6–7 and 9–14; producer/rule annotation and existing title on 11; fixed-stage media repair on 18; affected runbook, README, validator and existing reports. No new slide, framework, font, image dependency or compiler modification. Preserve 18 slides, 1290 seconds = 21:30. Research stays 360 seconds: 9=40, 10=55, 11=80, 12=45, 13=40, 14=50, 15=50. Move 15 seconds to the first derivation by shortening already-repeated preview/generalization/before-after narration. This is an editorial allocation, not a stopwatch result.

### Baseline browser evidence

`python scripts/validate_deck.py --output qa/baseline`: 18 slides, 1290 seconds, 36 default screenshots, 56 reveal states, seven font faces, zero JS errors, zero geometry groups; navigation/wheel/touch/local-file/offline contacts passed. Additional browser audit captured 108 full slides at 1920×1080, 1536×864, 1366×768, 1024×768, 1280×900 and 390×844; 26 research/adjacent reveal states at 1920; actual P overlay; all 18 offline slides; live production slide 11. Only slide 18 failed geometry at 1024 and 390 (3 and 9 issues respectively). Artifacts are ignored under `qa/baseline` and `qa/baseline-extra`; historical QA was not treated as current evidence.

### Final repair and regression evidence

Final HTML SHA-256: `ee97af4e975e71b2cb939a1f214428b58ff2ee7724f110941f21cac11afdd6cc`. Final validator (`qa/final/validation.json`) passed: 18 slides, 1290 seconds, research 360 seconds, 72 defaults, 72 responsive captures, 56 logical reveals / 176 reveal captures, seven embedded fonts, zero JavaScript errors and geometry issue groups. All-slide offline opening and actual visible presenter cues/dismissal passed. Required 54 projector combinations were captured and visually reviewed. The added compute label resolves a concrete first-use omission without adding another term or slide.

The final explanation through slide 11 can be reconstructed without later definitions: slide 9 proposes cross-owner cooperation; slide 10 states the optimizer's required property and fixed assumptions; slide 11 identifies provider assertions, two all-input rules, the derived independence fact and the legality answer. The same slide bounds proof to derivation and separates cost. Slide 12 adds compatible valid evidence under fixed rules, 13 generalizes its identity contract, and 14 explains missing/negative/stale/conflicting knowledge. The 15→16 return still consumes decisions at compile boundaries; no proposed engine is inserted into production execution.

Before publication, the user explicitly instructed “скипни проверки”. Remaining additional checks, including exhaustive manual review of every final changed reveal and an additional standalone adversarial pass, were skipped. Executed automatic checks and reviewed full-slide evidence are retained; omitted manual coverage is disclosed in QA_REPORT.md. CI remains enabled and will run normally for the release commit. No checks were disabled or weakened.
