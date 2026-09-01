# Claim ledger — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`. Re-audited: `2026-09-01`.

## IMPLEMENTED — current source-backed

### Global composition

- `LanguageCompiler` is the public semantic planner for the current path; it resolves features, contributions/provider ambiguity and artifact routes into `LanguagePlan` or diagnostics.
- Provider ambiguity can fail as `UTL2002`; `PreferCapabilityProvider(...)` makes the integrator's choice explicit.
- `LanguagePlan` contains resolved Features, Contributions, RuntimeProvider, Routes, PlanHash and Summary.
- Runtime creation verifies/materializes the selected plan. `LanguageRuntime.Run` does not invoke a second global feature/provider/route planning pass.
- Artifact route compatibility is structural; route `TotalCost` is a planning quantity, not runtime latency.

### Local semantic legality

- `CallableDescriptor` carries optimizer-visible semantic properties including effects, determinism, algebraic traits and trust.
- `SsaConstantFoldingPass` folds a call only when its descriptor is pure, deterministic, trusted, operands are known constants and the evaluator succeeds.
- `SsaLocalCommonSubexpressionEliminationPass` eliminates repeated calls only when the descriptor is pure, deterministic and trusted; unknown/unsupported shapes fail conservatively.

### Selected-environment capability legality

- `WistIntrinsicPlanPolicy` derives allow/forbid policy from `LanguagePlan` for the selected backend.
- `WistDirectRuntimeComponents` combines actual selected-backend intrinsic support with that plan policy before initializing optimizers.
- Optimizers observe this through `IOptimizerIntrinsicCapabilityContext.Supports(...)`.
- Wist backend boundaries validate emitted AIR against the selected plan and fail closed for forbidden typed intrinsics.
- `WistIntrinsicPlanPolicyTests` exercises both optimizer-visible rejection and backend rejection.

### IR stage contracts

- `SsaOptimizerPipeline` runs the supplied pass list in order.
- Before each pass it validates `RequiresFacts` and `RequiresCapabilities`.
- After each pass it applies `Produces`, `Preserves`, and `Invalidates`.
- This is contract-checked pass execution, not an automatic pass scheduler.

## DEMO-ONLY

`demo/Program.cs` intentionally uses synthetic `Demo.Ambiguity` and `Demo.Runtime` packages:

```text
UTL2002
→ PreferCapabilityProvider(...provider.a...)
→ LanguagePlan
→ LanguageRuntime.Create
→ input=41 output=42
```

The synthetic demo isolates the architecture. It does **not** claim to execute Wist `MinimalArithmetic`.

## PARTIALLY IMPLEMENTED / BOUNDED

- Capability-gated specialization is demonstrated by the current Wist typed-intrinsic path. Do not generalize it into a guarantee that every optimizer/backend in UniversalToolchain is capability-gated.
- `EGraphOptimizerModule` is a bounded straight-line symbolic simplifier/canonicalizer over a restricted arithmetic subset with capability guards. Do not call it a general equality-saturation engine or production e-graph framework.
- Semantic descriptors are consumed as explicit evidence. Their truthfulness remains a trust/specification boundary; typed metadata is not automatic semantic proof.

## NEEDS MEASUREMENT

- planning latency/allocation cost;
- runtime creation cost;
- first-execution/cold-start cost;
- steady-state overhead vs a handwritten equivalent;
- JIT/AOT specialization effects;
- workload-specific amortization/break-even.

No exact-current raw benchmark-result artifact is bound into this deck, so there is no numerical performance comparison.

## NOT CURRENTLY SUPPORTED / NOT CLAIMED

- automatic semantic compatibility proof for extensions;
- proof that descriptor metadata is behaviorally truthful;
- automatic pass scheduling from `IrStageContract`;
- general equality saturation;
- planner-driven universal devirtualization/specialization;
- sandboxing arbitrary in-process extensions;
- proof that a selected route is execution-time optimal;
- zero-cost extensibility;
- all runtime interfaces/dispatch disappear;
- UniversalToolchain is universally better than handwritten pipelines, DI, builders, LLVM/MLIR, Racket or language workbenches.

## Core wording

Use:

> **Resolve globally. Justify locally. Execute concretely.**

Expanded:

> Global planning selects one concrete execution environment; local compiler passes then justify rewrites from explicit semantic contracts and from the capabilities that this selected environment actually exposes.

Do not replace it with “the planner proves semantics” or “the planner produces all optimizer guarantees”.
