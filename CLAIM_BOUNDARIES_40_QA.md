# Claim boundaries and hostile Q&A for LangDev 2026

This is a documentation/presentation-only hardening file. It is intended to be copied into the presentation repository or used as speaker prep. It adds no UniversalToolchain production API, features or abstractions.

## Claim boundaries

Use these claims:

- Keep local knowledge local. Make global decisions explicit.
- The planner does not eliminate complexity; it gives composition complexity one owner.
- Planning moves composition decisions out of repeated execution.
- LanguagePlan is resolved composition data.
- Runtime materializes a selected plan; it does not rediscover global composition.

Do not use these claims without exact evidence:

- zero-cost extensibility;
- free abstraction;
- automatic semantic compatibility;
- universal plugin safety;
- dependency hell solved;
- all ambiguity rejected;
- NativeAOT support;
- thread-safe runtime;
- PlanFuzz proves the architecture;
- PlanFuzz beats normal fuzzing.

## Required narrative sequence

1. Simple case: handwritten pipeline.
2. Scaling problem: independent components create global decisions.
3. Planner: local declarations → global plan.
4. LanguagePlan: choices become data.
5. Runtime: executes selected plan instead of rediscovering composition.
6. Benefits: determinism, inspectability, centralized conflicts, reproducibility, testability.
7. Costs: planning, framework concepts, configuration state space.
8. Limitations: planning does not prove semantic correctness, sandboxing, performance or thread safety.

## Appendix slide candidates

### What planning does not prove

- semantic equivalence between arbitrary extensions;
- optimizer correctness;
- absence of semantic interference;
- security/sandboxing;
- malicious-code safety;
- performance;
- thread safety;
- general dependency solving.

### Equal-cost route ambiguity

- Provider ambiguity fails closed when current source emits explicit ambiguity diagnostics.
- Route selection may be deterministic without proving semantic equivalence.
- Equal-cost structural routes require explicit policy if semantic preference matters.

### PlanHash

- Identity of canonical resolved plan representation.
- Useful for reproducibility and evidence binding.
- Not a proof of semantic compatibility, safety or optimality.

## 40+ hostile questions

Use the hostile Q&A table in `UniversalToolchain/docs/talks/langdev-2026/adversarial-defense-pack.md` as the canonical extended version. For live rehearsal, compress to the following highest-risk set:

1. Planner hides complexity? — No, it changes representation and ownership.
2. Why not handwritten? — Handwritten is better for fixed known pipelines.
3. Why not DI? — DI wires services; UT resolves language composition and routes into plan data.
4. Dependency manager? — No; rich version solving is not claimed.
5. Two providers? — Provider ambiguity fails before execution when no explicit preference exists.
6. Two equal-cost routes? — Determinism is not semantic equivalence; explicit policy is future work.
7. Does LanguagePlan prove correctness? — No, structural composition only.
8. PlanHash proof? — No, representation identity.
9. Safe plugins? — No, valid plan is not sandbox.
10. Runtime second planner? — No, exact materialization/validation only.
11. Performance? — Measure planning/runtime/steady-state separately.
12. 1000 contributions? — Needs measurement; no speculative cache.
13. 2^N tests? — Explicit plans enable sampling, not exhaustive proof.
14. PlanFuzz proves UT? — No, it consumes explicit plan data.
15. PlanFuzz better? — Needs equal-budget experiment.
16. Wist leakage? — Boundary risk; keep Wist semantics outside generic core.
17. Why not MLIR/LLVM? — Different ownership problem; use them when they are the right owner.
18. Semantic compatibility? — Not automatic; needs specs/tests/oracles.
19. Optimizer correctness? — Separate verifier/parity/property tests.
20. Lying metadata? — Supply-chain/trust issue outside planner proof.
21. NativeAOT? — Only exact measured scope.
22. Thread safe? — Lifecycle coordination is not provider thread-safety.
23. Deterministic = correct? — No; reproducible can be reproducibly wrong.
24. Hash drift? — Bind to canonicalization version.
25. Bad-plan debug? — inspect diagnostics, plan, routes, lock; report projection can be future.
26. PlanningReport now? — No unless existing observability is insufficient.
27. SAT solver? — Reject before evidence of need.
28. Authoring ergonomics? — Low-level alpha; high-level DSL future.
29. Backend-neutral done? — Some contracts implemented; third backend validation still limited.
30. Structural route but semantic mismatch? — Tests/oracles, not planning, catch it.
31. Beats handwritten? — Not claimed.
32. Break-even point? — Independent packages + global reproducible decisions.
33. Lock freezes semantics? — It freezes representation/provenance, not semantic truth.
34. Package version conflict? — Future ecosystem-triggered work.
35. Runtime fallback? — Must be explicit, not invisible semantics.
36. Claims drift? — Maintain claim/evidence map pinned to commits.
37. Old truth snapshot? — Update snapshot or explicitly pin claims.
38. Split repos now? — Not before LangDev; document/check boundaries.
39. What can planner reject? — Declared structural failures, not unknown semantics.
40. One-sentence claim? — Keep local knowledge local; make global decisions explicit.
41. Independent authors? — Declarations compose; semantics still require compatibility work.
42. If benchmarks are bad? — Admit cost; use UT where explicit composition ownership is worth it.
