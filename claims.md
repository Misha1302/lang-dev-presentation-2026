# Claim ledger — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Main-talk load-bearing claims — CURRENT

### Whole-language planning

- `LanguageCompiler` is the current public whole-language planner for this path: it resolves feature closure, contributions/provider choices and artifact routes into `LanguagePlan` or diagnostics.
- Provider ambiguity can fail as `UTL2002`; `PreferCapabilityProvider(...)` makes the language integrator's policy explicit.
- Artifact transformations expose source/target contracts and planning cost; the route phase chooses a deterministic type-compatible path under the expressed protocol and stores it as `LanguageArtifactRoute`.
- Deterministic route selection is a protocol property. It is **not** semantic equivalence or correctness proof.
- Route `TotalCost` is a planning quantity. It is **not** execution-time latency.

### Concrete decision record

- `LanguagePlan` contains resolved Features, Contributions, RuntimeProvider, Routes, PlanHash and Summary.
- `PlanHash` is useful canonical identity for the expressed plan; it is **not** semantic/security proof.

### Runtime ownership

- `LanguageRuntime.Create` verifies exact binding and materializes the selected plan.
- `LanguageRuntime.Run` does not invoke a second global feature/provider/route planning pass.
- This supports the architectural claim that whole-language composition need not be rediscovered for every repeated execution.
- It does **not** support “zero overhead”, “all abstractions disappear” or a numerical speed claim.

### Two staging boundaries

- `WistEngine.Create` constructs the selected language environment: definition → compiler → plan → runtime.
- `Compile<TDelegate>` is a separate compiled-program reuse boundary.
- `Evaluate(code)` reuses the environment but is not equivalent to invoking an already materialized reusable compiled delegate.

## DEMO-ONLY

`demo/Program.cs` intentionally uses synthetic `Demo.Ambiguity` and `Demo.Runtime` packages:

```text
UTL2002
→ PreferCapabilityProvider(...provider.a...)
→ LanguagePlan + route
→ LanguageRuntime.Create
→ input=41 output=42
```

The current synthetic demo isolates planner/runtime ownership. It does **not** claim Wist `MinimalArithmetic` semantics, arbitrary semantic route equivalence or benchmark performance.

## APPENDIX / Q&A — CURRENT BUT NOT CENTRAL NARRATIVE

- semantic-descriptor-gated local CSE / constant folding;
- selected-environment capability gating for current Wist typed intrinsics;
- IR stage fact/capability contract checks on a supplied pass sequence;
- bounded straight-line `EGraphOptimizerModule` behavior.

These mechanisms remain useful evidence/Q&A material, but they are deliberately removed from the 15-slide main causal chain so the talk does not become an optimizer/API tour.

## NEEDS MEASUREMENT

- planning latency/allocation cost;
- runtime creation cost;
- first-execution/cold-start cost;
- steady-state overhead vs a handwritten equivalent;
- JIT/AOT specialization effects;
- workload-specific amortization/break-even.

No exact-current raw benchmark-result artifact is bound into this deck, so there is no numerical performance comparison.

## NOT CURRENTLY SUPPORTED / NOT CLAIMED

- automatic semantic compatibility proof for alternative routes;
- proof that deterministic routing implies correct program semantics;
- execution-time optimality from route planning `Cost`;
- automatic pass scheduling from `IrStageContract`;
- general equality saturation;
- sandboxing arbitrary in-process extensions;
- zero-cost extensibility;
- all runtime interfaces/dispatch disappear;
- UniversalToolchain is universally better than handwritten pipelines, DI, builders, LLVM/MLIR, Racket or language workbenches;
- a route-changing conference demo until such a demo is implemented and CI-backed.

## Core wording

Use:

> **Declare locally. Resolve globally. Execute concretely.**

Expanded:

> Independent extensions declare local facts and transformations; whole-language planning resolves interacting choices into one inspectable `LanguagePlan`; runtime materializes exactly that resolved environment.

Anti-takeaway:

> If one owner already knows the stable pipeline, wire it by hand.
