# Adversarial review — post-redesign

Truth snapshot: `UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Narrative verdict

The baseline deck had a causal gap: after admitting that a handwritten pipeline is usually best, it jumped directly into providers/conflicts/routes before establishing why anyone needs multiple language configurations. The redesign closes that gap with a current Wist language-family story before planner vocabulary.

## Hostile pass

### “Why extensibility?”
Answered on main slide 3 with real shipped Wist presets. Practical value is reuse of one language infrastructure across different feature/backend/policy configurations rather than maintaining a compiler fork per profile.

### “Why not flags / CompilerOptions?”
Main slides 4–5 concede flags while options are independent. Planner appears only after dependencies, provider alternatives, conflicts/order, artifact routes and runtime/backend compatibility make choices whole-language decisions.

### “Why not a builder?”
A builder is sufficient when the integrator already knows the exact graph. It does not by itself define the policy for resolving independently declared global constraints. Appendix A3 makes this distinction explicit.

### “Why not DI?”
DI is strong at materializing a chosen object graph. UniversalToolchain's planning phase addresses the earlier question: which provider, route, ordering and runtime should constitute the graph under the expressed language protocol? DI may still be used after resolution. No claim that DI cannot be extended with custom policy logic.

### “Is this overengineering?”
Yes, if one owner knows a stable pipeline. Main slides 2 and 16 explicitly recommend handwritten composition in that case.

### “Why multiple dialects instead of forks?”
If variants intentionally share most language infrastructure, presets/definitions let the common implementation evolve once while integrators select different surfaces/backends/policies. Forks remain valid when variants truly need independent evolution or semantics.

### “Who extends the language?”
Main slide 6 separates conceptual framework author, package authors, language integrator and runtime user. They may be the same person/team; the architecture matters when they are not.

### “What if two extensions disagree?”
Expressed conflicts/order/provider ambiguity can fail planning. Semantic disagreements that are not encoded in the protocol are outside the planner's proof boundary.

### “Who guarantees semantic compatibility?”
Not `LanguagePlan`. Main slide 15 explicitly separates structural from semantic compatibility.

### “Is LanguagePlan just a dependency graph / DTO?”
No in the current API: it contains resolved package identities/contributions, runtime provider, concrete artifact routes, canonical hash and summary. It is still data; the point is that those data bind later materialization and are inspectable/testable.

### “What does PlanHash prove?”
Canonical identity of the expressed resolved plan for reproducibility/debugging/testing. It does not prove semantic equivalence, security, program identity or performance equivalence.

### “Is runtime really static?”
The deck does not call it static. Runtime still validates exact plan/provider constraints and request inputs, owns objects/sessions and may dispatch dynamically.

### “Is runtime validation planning again?”
No current `LanguageRuntime.Create` re-runs the feature/contribution/route phases. It verifies and materializes the already selected plan. This is an exact-binding boundary, not a second global composition search.

### “Does extensibility hurt performance?”
It can. The deck separates planning, runtime creation, first execution and steady-state costs. Only the staging fact is source-backed; magnitude requires measurement.

### “Is it zero-cost?”
No. Explicitly not claimed.

### “Does JIT remove the abstractions?”
Not guaranteed by planning. JIT/AOT specialization is a separate optimization question and remains `NEEDS MEASUREMENT`.

### “Have you measured it?”
Not with an exact-current raw result artifact used by this deck. Therefore no numerical performance claim appears.

### “When does planning pay off?”
Workload-specific. It can amortize only when a plan/runtime is reused enough that avoided repeated global decisions are meaningful relative to planning/runtime-creation cost. This needs measurement for a concrete workload.

### “Is route Cost a performance metric?”
No. It is summed planning metadata used by route selection; the deck explicitly says it is not measured runtime latency.

### “What if equal-cost routes exist?”
That is a deterministic planning-protocol question. Selection/tie behavior must be tested; equal planning cost does not imply semantic equivalence.

### “Is route selection deterministic?”
The architecture intends deterministic resolved plans under the expressed protocol; this is reproducibility of resolution, not semantic equivalence. Do not generalize beyond tested/current rules.

### “Is it thread-safe?”
Not a central claim. The Wist facade documents that one `WistEngine` rejects overlapping public operations and recommends separate engines for concurrency. Do not advertise universal thread safety.

### “Is it secure / a sandbox?”
No. Restricted policy can constrain composition and host interop but is not process isolation. Third-party extension trust/isolation is a separate security problem.

### “Can a malicious plugin hurt me?”
Yes, in-process extension code must be treated according to the host's trust model. Planning validation does not sandbox arbitrary code.

### “Why not MLIR?”
MLIR is an extensible multi-dialect IR ecosystem with operations/types/attributes and conversion infrastructure. UniversalToolchain addresses a different design point: composing a whole runnable language configuration into an explicit plan/runtime boundary in .NET. They can be complementary.

### “Why not Racket?”
Racket's `#lang` ecosystem makes language choice/creation a first-class module protocol. UniversalToolchain focuses on typed package contributions, global resolution and exact runtime binding. No superiority or novelty claim.

### “Why not MPS?”
MPS is a full language workbench with language modules, extension and projectional tooling. UniversalToolchain is not a replacement IDE/workbench; its narrow focus here is runtime/compiler composition staging.

### “Why not MontiCore?”
MontiCore provides reusable language components and composition through grammar inheritance, embedding and aggregation. UniversalToolchain does not claim the same composition model; it demonstrates a different typed planning/runtime design point.

### “What's novel?”
The talk does not make a novelty claim. It presents a concrete architecture and the staging reasoning behind it.

### “When should I not use it?”
When one owner can correctly and clearly wire a stable pipeline; when variants should truly be independent forks; when the composition protocol cannot express the semantic constraints you need; or when planner infrastructure costs more than the extensibility problem warrants.

## Newcomer noun audit

- slides 1–2: no UT nouns required;
- slide 3: only Wist + three variant names;
- slide 4: `.wistdialect` only;
- slide 5: generic feature/capability/contribution/backend vocabulary;
- slide 6: first `LanguageDefinition` / `LanguageCompiler`;
- slide 9: first full `LanguagePlan` field view;
- slide 10: `LanguageRuntime`;
- after slide 10 no new core UT noun is needed.

This is materially lower simultaneous jargon than the planner-first baseline.
