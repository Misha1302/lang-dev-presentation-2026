# LangDev 2026 presentation improvement — 2026-10-09

Canonical artifact: `index.html`. Baseline: clean `main`, commit `e7256fd`, **18 slides**. No 16-slide draft was edited. Self-contained HTML, embedded fonts/QRs, fixed 1600×900 stage, navigation and reveal architecture are retained. Implementation and local QA were completed before publication; compiler sources were not edited. `contact-slide.html`, unrelated assets and deployment workflows remain untouched.

## Material changes

| Slide | Original problem | Action | Architectural / narrative improvement |
|---|---|---|---|
| 1 | Thesis precedes the engineering tension | Introduce independent feature owners and the need for exact operations | Opening asks the question answered by planning and lowering |
| 5 | Plan fields underdemonstrate resolved choices | Show the test-backed interpreter route and ground hash identity in registered inputs | Audience can inspect an actual decision; hash is not semantic equivalence |
| 7 | Host slot appears without source context | Introduce `fee: double` as a host input | Exact 3→1 rewrite now connects to the running binding example |
| 8 | Familiar shadowing case consumes 1:55; transition risks motivating general inference | Retain a compact code/result example, reduce to 1:00, state its causal limit | Preserves tested backend architecture and gives binding ownership its own purpose |
| 9 | Abstract architectural question arrives before concrete coupling | Show Vectorizer→DependencyAnalysis call and arrival of a different analysis | Separate producer interoperability problem; stable typed interfaces remain a legitimate solution |
| 10 | Query demonstration repeats the specific API list; SIMD assumptions are implicit | Show producer→relations→consumer boundary with bounded uint32 loop | Consumer names legality; capability, evidence availability and cost stay distinct |
| 11 | Rules only annotate edges; dependency premises overlap; exact lowering implicit | Explicit amber B1/R rule nodes, independent evidence branches, equivalent lane lowering and missing-premise behavior | Genuine derivation DAG; target capability alone cannot prove legality |
| 12 | Adds facts without displaying bridge; only 45 seconds | Show new B1 concretely; same before/after query; allocate 75 seconds | New producer supplies evidence + bridge; existing consumer and existing R stay unchanged |
| 13 | Another publish/derive/query diagram | Replace with scoped evidence record and incompatible revisions/targets | Distinct requirement: evidence must describe the right subject and context |
| 14 | Provenance uses stale predicate/rule vocabulary | Align trace with B1, R and target T | Explanation and invalidation refer to the same derivation as slides 11–12 |
| 16 | Title payoff is another pipeline | Show construction→plan and generic load→concrete `ldarg` comparisons | Exactly identifies removed decisions/representation and remaining host/plan/JIT machinery |
| 17 | Generic synthesis path and weak status visibility | Name independent modules, one plan, concrete .NET operations; split working/research link captions | Returns to the opening problem and preserves status boundary |
| All notes | Some caveats exist only in hidden notes; changed narrative/timing needs synchronization | Update actual P cues, detailed notes and runbook | Speaker can reconstruct explanation without a memorized script |

Slides 2–4, 6, 15 and 18 retain their successful argument and visual design. No slide was added or removed: repurposing 9/13/16 removes repeated claims without losing evidence. Reveal steps remain contiguous; the strengthened validator captures every reveal at all requested projector sizes and checks every counter/progress value.

Shadowing alternatives considered: removing it would lose an observable preservation contract following the exact rewrite; retaining the original diagram would overallocate time; **a short engineering example** preserves that evidence with a clear limit. It is not the justification for the research layer.

## Technical integrity

All compiler links pin `1d46f17c8dc28f434fa58bdf92f9f8278fa5aaee`, the clean local `../Wist2` checkout. The later `../UniversalToolchain` checkout is supporting context, not silently substituted for pinned evidence.

| Claim | Evidence / boundary |
|---|---|
| Modules own syntax and lowering contributions | `NativeTypesModuleImpl.cs`, numeric/arithmetic visitors; implemented |
| PricingRestricted selects a numeric surface without loops/interop | Actual dialect file and profile tests. These tests check contribution selection; no fresh rejected-program execution is implied |
| One immutable plan selects contributions, provider and typed routes | `LanguageCompiler.cs`, `LanguagePlan.cs`, `LanguageRuntime.cs`; canonical artifact-route and insertion-order hash tests |
| Bytecode/AIR support interpreter and CIL routes | Lowerer, converter and emitter sources. Slide 6 is an unoptimized explanatory sketch, not a captured optimized dump |
| Supported external-load pattern becomes typed intrinsic and CIL argument load | Exact `NativeCILOptimizerModule` match, requested-type capability gate, intrinsic emitter and focused tests |
| Binding parity is protected | Regression source matches shown program. Numeric 2/2 was independently reconfirmed by a rebuilt public-facade probe on 2026-10-09; parity tests alone can also accept matching deterministic failures |
| General relation inference, B1/R derivation and provenance | Research proposal; no shipped general proof engine or production SIMD demonstration is claimed. Existing compiler facts and requires/produces/preserves/invalidates contracts already exist |

The SIMD illustration uses invariant `scale`, ordinary nonvolatile uint32 arrays and modulo arithmetic, no concurrent mutation, valid bounds and scalar tails. `ReadWriteDisjoint(L)` includes aliasing and `DistinctWrites(L)` requires different iterations to write different locations. Their B1 bridge establishes independence for this specific loop. `EquivalentLaneLowering(L,T)` covers lane arithmetic, per-lane effects/exceptions and boundary/tail behavior; cross-iteration reordering remains a separate independence obligation. `SupportsSIMD(op,T)` includes the operation and lane type. R is explicitly illustrative, not a complete general legality theorem. Cost is checked separately.

Additive extension is relational derivation through a newly registered bridge, not selecting a replacement vectorizer. Installation establishes no fact by itself: compatible evidence, provider authority and checked scope/revision remain required. The old legality rule and consumer query are unchanged; the new module adds B1 rather than editing R.

Prior-art claims were verified from [MLIR interfaces](https://mlir.llvm.org/docs/Interfaces/), [LLVM analysis management](https://llvm.org/docs/NewPassManager.html), [ableC](https://melt.cs.umn.edu/ableC/) and [Soufflé provenance](https://souffle-lang.github.io/provenance). These systems already support substantial decoupling, analysis lifecycle, modular semantics or inference. The experiment compares integration work and invalidation correctness against interfaces + analysis management, including adapters/external models; no novelty or superiority claim is made.

Remaining research risks: provider correctness/authority, bridge-rule review, inference termination, contradiction policy, revision/target identity and complete invalidation. None is solved by checking a proof DAG alone. No measured speedup, universal zero overhead or near-C# performance claim is made.

## Final talk outline

**21:30 allocation**, not a measured delivery: implemented story / synthesis 14:05, proposed research outlook 6:55, contacts 0:30 within the 25-minute slot. Rehearse slides 10–12 together, especially lane equivalence vs independence and the new B1 vs unchanged R. Also rehearse the 8→9 reset and the 15→16 return to implemented code.

| Slide | Title | Narrative role | Speaker anchor | Allocation |
|---|---|---|---|---|
| 01 | Open to extension. Concrete at execution. | Engineering tension: independent owners, concrete execution | Independent feature owners want to extend a language; execution needs exact operations. | 1:00 |
| 02 | A feature cuts across the whole compiler | Why features require contributions across compiler stages | A language feature is a vertical slice: syntax, AST, lowering and execution all participate. | 1:20 |
| 03 | Make the extension points module-owned | Ownership moves from central edits to selected modules | Each module owns its contributions. A dialect only selects which modules form the language. | 1:20 |
| 04 | The selected modules are the language | A real selection defines the allowed language surface | These selected modules literally define the language surface: arithmetic is present; loops and interop are not. | 1:30 |
| 05 | Composition closes into one LanguagePlan | Global composition choices close into a resolved plan | Features, contribution order, runtime provider and typed routes become one immutable plan. | 1:50 |
| 06 | One Wist program becomes executable operations | That plan compiles an authentic Wist expression | The same expression becomes more concrete: AST → semantic binding → module Bytecode → Abstract IR → interpreter or CIL. | 2:00 |
| 07 | Known slot + known type can erase a load sequence | One exact supported rewrite removes representation work | A host input has a binding slot and type. With the exact pattern and backend support, three AIR operations become one typed intrinsic. | 1:30 |
| 08 | One source must not acquire two meanings | Correctness guard: preserve binder-owned meaning | Local price reads host fee = 1; both backends return 2 in the freshly rerun pinned-source probe. | 1:00 |
| 09 | Who owns the answer an optimizer needs? | Separate research problem: consumer–producer coupling | Vectorizer calls BuiltinDependencyAnalysis.Check: its dependency names an implementation. | 1:05 |
| 10 | Ask a semantic question without naming its producer | Consumer requests a property under explicit assumptions | This conceptual loop uses uint32 modulo arithmetic, invariant scale, ordinary memory, checked bounds and scalar tails. | 0:55 |
| 11 | A proof joins independent premises | Independent premises join through bridge and legality rules | Dependency evidence joins through producer bridge B1 into independence. | 1:20 |
| 12 | New knowledge completes an existing decision | New evidence and bridge enable an unchanged consumer | Before, independence is unknown: scalar execution. The final query and R already exist. | 1:15 |
| 13 | An answer belongs to a subject and a context | Subject and context bound reusable evidence | Evidence names its relation, subject, revision, scope, producer and assumptions. | 0:40 |
| 14 | Provenance explains both success and a safe stop | Invalidation explains why a previously proved answer stops | Provenance records facts, producers and rules. This trace shows only the dependency branch. | 0:50 |
| 15 | Prior art supplies the pieces. Open composition sets the integration question. | Evaluate the hypothesis against strong existing mechanisms | MLIR, LLVM, extensible grammars and Datalog already provide important pieces. | 0:50 |
| 16 | What disappears — and what the backend receives | Title payoff: fixed composition and concrete backend input | Planning fixes Features, Contributions, RuntimeProvider and Routes; runtime materializes that selected graph. | 1:40 |
| 17 | Compose the language. Agree on meaning. Execute concrete operations. | Return to the opening division of responsibilities | Independent modules form one language plan; tested lowering produces concrete .NET operations. | 0:55 |
| 18 | Continue the discussion | Contact handoff and Q&A frame | The live deck, project, Telegram and email are all here for follow-up. | 0:30 |

## Causal review of every slide

Evidence supports each slide's claim. Its payoff creates the next slide's question (the last slide is the contact handoff). This table records why the preserved slides remain necessary as well as why replacements differ.

| Slide | Evidence | Payoff / next question |
|---|---|---|
| 01 | Shipped pricing program | Why does a feature need extension points across several stages? |
| 02 | NativeTypes lexer/parser/visitor registrations | So ownership should move from the central compiler into feature modules. |
| 03 | Actual dialect excerpt; conceptual monolith labelled | Now we can build a genuinely restricted language from the same compiler. |
| 04 | Exact PricingRestricted file and profile tests | But selecting modules is not enough — global choices still have to be resolved. |
| 05 | Public plan fields; canonical route and hash tests | Follow a program through this resolved compiler. |
| 06 | Actual lowering source; unoptimized IR sketches labelled | Once enough is known, some representation machinery can disappear. |
| 07 | Exact optimizer, capability gate and intrinsic tests | Representation may change, but meaning must not. |
| 08 | Binding regression and freshly rerun successful probe; no old wrong result | A separate problem: what if a consumer names one specific analysis producer? |
| 09 | Conceptual specific producer call; typed interface alternative | Let the consumer ask a question without selecting the producer. |
| 10 | Illustrative loop and proposed query, not shipped APIs | Where does that answer come from? |
| 11 | Illustrative DAG with distinct premises and provider/rule provenance | Install the missing provider and bridge, leaving R and the consumer unchanged. |
| 12 | Conceptual before/after: new B1, old R and query unchanged | Which loop revision and target does that evidence describe? |
| 13 | Proposed scoped evidence record | Change the memory accesses and this proof path must expire. |
| 14 | Proposed dependency-branch trace and r7→r8 invalidation | These ideas already have strong precedents. |
| 15 | Primary MLIR/LLVM/ableC/Soufflé references | Whatever mechanism wins, execution should consume resolved decisions. |
| 16 | Selected-plan runtime and actual external-load CIL emitter | Return to the opening problem: independent contributions, exact decisions, concrete execution. |
| 17 | Implementation/research links visibly separated | Leave the links visible for questions. |
| 18 | Embedded offline QR assets and actual hrefs | Thank you. Questions? |

## Adversarial review

Read-only independent technical and narrative reviews were requested as part of the user’s coordinated-team task. Compiler review led to distinct read/write-vs-write/write premises, explicit lane equivalence and the successful-probe distinction. PL/audience review led to a legitimate interface baseline, actual bridge attribution, concrete plan route and additional time for the extension example. Designer review uses rendered output, not CSS alone. Findings and executed checks are recorded in QA_REPORT.md; proof interpretation and producer trust remain explicit limits.

Baseline ordering/timing is preserved in REBUILD_EVIDENCE.md. Visual/functional results are recorded separately in QA_REPORT.md, linked to the actual validated source hashes. Focused compiler tests and an independent numeric probe were freshly executed; commands and results are recorded in QA_REPORT.md.
