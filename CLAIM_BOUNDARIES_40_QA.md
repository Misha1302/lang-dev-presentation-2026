# Claim boundaries and hostile Q&A for LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

This is presentation/speaker-prep material. It adds no UniversalToolchain production API, feature or abstraction.

## Core wording

Use:

> **Build an Extensible Language, Run a Concrete One**

> Extensions describe possibilities. Planning resolves global composition choices into one concrete `LanguagePlan`. Runtime executes that resolved plan instead of reopening those decisions.

> **Extensible at composition time. Concrete at execution time.**

> Extensibility does not inherently require global composition decisions to remain dynamic during repeated execution.

> **The runtime should not repeatedly pay for decisions that were already made.**

> Planning does not remove cost. It makes where we pay explicit.

Do not turn these into:

- zero-cost extensibility;
- extensibility is free;
- same speed as handwritten C#;
- all abstractions disappear;
- all dispatch disappears;
- planning guarantees devirtualization;
- UniversalToolchain always produces the fastest pipeline;
- “minimum-cost language” or global configuration optimality;
- an unconditional claim that extensibility does not sacrifice performance.

## Two meanings of deabstraction

### Composition deabstraction — current architecture

Before planning, provider/route/runtime/order can be alternatives or constraints. After planning they are concrete `LanguagePlan` data. The abstraction disappears **as an open decision**, not necessarily as an allocated object.

### Representation/code specialization — separate optimization

Interfaces, objects, validation and indirect calls may remain. JIT/AOT may specialize some of them, but that is an implementation- and workload-specific optimization problem with its own evidence requirement.

## Performance answer in 30 seconds

**Won't extensibility hurt performance?**

The architectural result and empirical result are different. Current source stages global composition before execution: `LanguageCompiler` resolves providers, ordering and artifact routes into `LanguagePlan`; `LanguageRuntime.Run` executes through the already-created plan/session rather than invoking the semantic planner again. That removes repeated global composition from the execution boundary, not every runtime abstraction. Planning, runtime creation, first-use work, validation, dispatch and generated-code quality still cost something, so their size must be benchmarked separately.

**So is extensibility free?**

No. Planning, materialization and remaining runtime abstractions all have costs. The narrower claim is that provider, route, ordering and runtime selection do not need to be rediscovered during every execution.

**Are you claiming zero-cost abstractions?**

No. Composition choices become concrete before execution. Interfaces, objects, validation and dispatch may remain. Eliminating some of them is a separate specialization problem.

**Then why should this be faster?**

The architecture does not guarantee that the final program is faster than handwritten code. It guarantees that repeated execution does not need to reopen the global composition problem. Whether the remaining steady-state overhead is negligible is workload-dependent and measurable.

**Why not just use DI?**

DI is good at materializing known bindings. Here the missing step is earlier: resolve a domain-specific whole-language composition graph — capability providers, conflicts, ordering, artifact routes and runtime provider — into validated plan data before materialization. If those choices are already known, use the simpler host pipeline/DI solution.

## Cost boundaries

1. **Planning:** feature/contribution resolution, provider selection, conflicts, ordering, route search, canonicalization, diagnostics, allocations.
2. **Runtime creation:** plan verification, component materialization, route/session assembly.
3. **First execution:** parsing/lowering/codegen where applicable, initialization, JIT, cold caches.
4. **Steady state:** concrete selected path; no global re-planning by architecture, but validation, provider/session calls, dispatch, allocations and generated-code quality may remain.

`No re-planning ≠ zero overhead.`

Conceptual amortization only:

```text
naive dynamic composition: N × (Ccomposition + Cexecution)
staged composition:        Ccomposition + N × Cexecution
per-run composition share: Ccomposition / N
```

This decomposition is not benchmark evidence and does not prove total UniversalToolchain performance beats an alternative.

## Benchmark evidence boundary

Current source has separate BenchmarkDotNet surfaces for:

- `MigrationArchitectureBoundaryBenchmarks` — `LanguagePlan_Compile`, `WistEngine_CreateAndDispose`;
- `FormulaHotPathBenchmarks` — prepared C# / NCalc / Wist delegates, with parity checks;
- `FormulaCompilationBenchmarks` — existing-engine compilation and create-engine+compile;
- `FormulaConvenienceBenchmarks` — `Evaluate` convenience paths.

Do not compare `Evaluate` with a prepared C# delegate and label the difference “runtime execution overhead”: those workloads include different work. Do not publish Dry/Smoke results as precise performance evidence.

For the current truth snapshot, a presentation-bound raw exact-environment result set is not available, so numerical planning/runtime/first/steady-state claims are `NEEDS MEASUREMENT`.

## Required narrative sequence

1. Handwritten pipeline works and is often best.
2. Independent extensions create global composition decisions.
3. Planner owns those decisions.
4. `LanguagePlan` collapses the open choice space into concrete data.
5. Runtime validates/materializes and executes that plan; it does not perform a second global planning pass.
6. Therefore extensibility does not inherently require dynamic global composition in repeated execution.
7. Remaining performance cost is split into four measured boundaries.
8. Structural compatibility still does not prove semantic compatibility.

## Hostile rehearsal set

1. Planner hides complexity? — No; it changes ownership and representation.
2. Why not handwritten? — For fixed known pipelines, handwritten is often better.
3. Why not DI? — DI materializes known bindings; the planner resolves whole-language choices before materialization.
4. Dependency manager? — No; general ecosystem version solving is not claimed.
5. Two providers? — `UTL2002` fails before execution unless preference is explicit.
6. Two equal-cost routes? — Deterministic tie-break gives reproducibility, not semantic equivalence.
7. Does `LanguagePlan` prove correctness? — No; it proves selected declared structure.
8. `PlanHash` proof? — No; canonical representation identity.
9. Safe plugins? — No; a valid plan is not a sandbox.
10. Runtime second planner? — No on the current public path; it validates/materializes exact selected bindings.
11. Performance? — Separate planning, runtime creation, first execution and steady state.
12. 1000 contributions? — Needs synthetic measurement before scale claims or caching work.
13. 2^N tests? — Explicit plans enable configuration-aware sampling, not exhaustive proof.
14. PlanFuzz proves UT? — No; it is a possible consumer of plan data.
15. PlanFuzz better than ordinary fuzzing? — Needs equal-budget experiment.
16. Wist leakage into generic core? — Real boundary risk; keep language semantics outside generic core.
17. Why not MLIR/LLVM? — Different ownership problem; use them when they own the relevant IR/pass composition.
18. Semantic compatibility? — Not automatic; requires specs/tests/oracles.
19. Optimizer correctness? — Separate verifier/parity/property testing problem.
20. Lying metadata? — Supply-chain/trust problem outside structural planning guarantees.
21. NativeAOT? — Claim only exact measured consumers.
22. Thread-safe? — Lifecycle coordination is not arbitrary provider thread safety.
23. Deterministic = correct? — No; reproducible can be reproducibly wrong.
24. Hash drift? — Bind evidence to canonicalization/version/source identity.
25. Debug bad plan? — Inspect diagnostics, selected contributions, routes, runtime and hash/lock representation.
26. PlanningReport now? — Only if current typed plan/diagnostics repeatedly prove insufficient.
27. Why no SAT solver? — No need until the domain constraints require one.
28. Authoring ergonomics? — Alpha-level concern; do not confuse convenience DSLs with architecture proof.
29. Backend-neutral complete? — Claim only current tested contracts, not universal backend portability.
30. Structural route but semantic mismatch? — Tests/oracles catch what the protocol does not express.
31. Beats handwritten? — Not claimed.
32. Break-even point? — Workload/organization dependent; independent global choices justify the architecture, not a universal numeric threshold.
33. Lock freezes semantics? — It freezes representation/provenance, not semantic truth.
34. Package version conflict solved? — General ecosystem solving is outside current claim.
35. Runtime fallback? — It must be explicit; invisible semantic fallback would violate the ownership story.
36. Claims drift? — Pin the presentation to exact source and re-audit on source movement.
37. Old truth snapshot? — Update the source pin only after code/tests/docs/demo review.
38. Split repos now? — Not required for this talk; architecture boundary matters more than repository topology.
39. What can planner reject? — Expressed structural/configuration failures, not unknown semantics.
40. One-sentence architecture claim? — Extensions describe possibilities; planning resolves one plan; runtime executes it.
41. Is extensibility free? — No; only repeated global composition is staged out.
42. Does planning remove dispatch? — No guarantee.
43. Does planning guarantee devirtualization? — No.
44. Does planning always pay off? — No; slide 2 deliberately keeps the simpler baseline.
45. Is amortization a benchmark? — No; it is a cost decomposition.
46. Could `Run` secretly route again? — Current `LanguageRuntime.Run` does not invoke semantic planning/route search; it validates plan-bound inputs and calls the created session.
47. Is route `Cost` runtime cost? — No; it is the declared planning weight used by route construction.
48. If benchmarks are bad? — Admit the cost and use the planner only where explicit composition ownership is worth it.
