# Claim boundaries and hostile Q&A — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

This file is the rehearsal/Q&A owner. Implementation maturity is owned by [`claims.md`](claims.md); operational demo details are owned by [`DEMO.md`](DEMO.md).

## Core wording

Use:

> **Resolve globally. Justify locally. Execute concretely.**

> Global planning selects one concrete execution environment; local compiler passes justify rewrites from explicit semantic contracts and from the capabilities that this selected environment actually exposes.

Do **not** turn this into:

- the planner proves semantics;
- the planner produces all optimizer guarantees;
- extensibility is free;
- all abstractions/dispatch disappear;
- capability availability implies a performance win;
- valid plan implies sandbox/security;
- current e-graph module is general equality saturation.

## 1. Why not just DI or a builder?

If the host already knows the exact graph, use them. The planner addresses an earlier ownership problem: independent packages declare dependencies/providers/conflicts/routes, and one whole-language phase resolves those choices before materialization. DI may still build objects afterward.

## 2. Why not LLVM or MLIR?

They solve different layers. LLVM is compiler infrastructure around established IR/toolchain contracts; MLIR provides extensible multi-level IR and dialect/conversion infrastructure. This talk focuses on whole runnable-language composition in .NET and then on local rewrite evidence. They can be complementary; no superiority claim.

## 3. Does `LanguagePlan` prove semantic compatibility?

No. It proves only what the expressed structural/configuration protocol can check: selected identities, dependencies, conflicts, routes, runtime/backend coverage, and related invariants.

## 4. What if `CallableDescriptor` metadata lies?

Then an optimizer may be given false evidence. Current local CSE/folding require trusted descriptor levels in addition to purity/determinism, but that is still a trust/specification boundary. Typed metadata makes assumptions explicit and testable; it does not make them automatically true.

## 5. Why is `pure + deterministic + trusted` interesting?

Because the legality rule is attached to semantic properties rather than hard-coded operation names. The same optimizer mechanism can conservatively preserve unknown/effectful/untrusted calls and reuse a trusted deterministic pure call without language-specific name knowledge.

## 6. What if the selected backend cannot execute the specialization?

The current Wist path combines selected backend capabilities with plan intrinsic policy before the optimizer sees `Supports(...)`. If support/policy rejects an intrinsic, the optimizer sees it as unavailable. Backend boundaries also validate emitted AIR and fail closed for forbidden intrinsics.

## 7. Is capability-gated specialization universal in UniversalToolchain?

No. The talk claims the exact current Wist typed-intrinsic path. Generalizing it to every optimizer/backend is outside current evidence.

## 8. Does extensibility hurt performance?

It can. The source-backed architectural claim is only that global composition does not have to be rediscovered on every execution. Planning, materialization, validation, dispatch, allocations, JIT/backend startup and generated-code quality still cost something.

## 9. Have you measured it?

Not with a presentation-bound exact-current raw benchmark artifact. Therefore the deck has no numerical performance claim. Planning/runtime creation/first execution/steady state are all `NEEDS MEASUREMENT` for this talk.

## 10. Does “concrete execution” mean no dynamic dispatch?

No. “Concrete” refers to resolved whole-language choices. Interfaces, objects, indirect calls and validation may remain.

## 11. Does `PlanHash` prove correctness?

No. It is canonical identity of the expressed resolved plan, useful for reproducibility/drift/testing. It is not semantic equivalence, a security attestation, or a performance identity.

## 12. Is restricted composition a sandbox?

No. Policies can restrict selected features/interop/runtime choices, but they do not create process isolation or malicious-code containment.

## 13. Do `IrStageContract`s automatically schedule passes?

No. Current `SsaOptimizerPipeline` iterates a supplied pass list. Contracts decide whether running the next supplied pass is legal (`RequiresFacts`, `RequiresCapabilities`) and update facts afterward (`Produces`, `Preserves`, `Invalidates`).

## 14. Is `EGraphOptimizerModule` a production e-graph/equality-saturation engine?

No. Current implementation is a bounded straight-line symbolic simplifier/canonicalizer over a restricted arithmetic subset, guarded by intrinsic capabilities. Keep `e-graph` out of the main narrative.

## 15. Why a synthetic demo instead of real Wist?

Because the demo's job is to isolate the planner/runtime boundary in 90–120 seconds. `Demo.Ambiguity` exposes UTL2002 deterministically, and `Demo.Runtime` exposes plan→route→runtime→execution without language-syntax noise. Wist remains source evidence elsewhere, but the executable slide must match the executable source.

## 16. How is this testable?

Planning can be tested as definition/registry → plan/diagnostics. Runtime can be tested as exact plan → materialization/execution. Compiler legality can be tested with positive and negative semantic descriptors. Capability gating can be tested both at optimizer `Supports(...)` and backend validation.

## 17. What happens with unknown semantic information?

Fail conservatively: do not justify the rewrite. Current local CSE requires a descriptor and known instruction/terminator shapes; constant folding requires descriptor + safe semantics + constant operands + successful evaluator.

## 18. Is deterministic selection the same as correct selection?

No. Reproducibility can be reproducibly wrong. Deterministic planning is a protocol property; semantic correctness still needs specifications/tests/oracles.

## 19. When should I not use this architecture?

When one owner can clearly wire the stable pipeline; when variants should be independent implementations; when the composition protocol cannot express the constraints that matter; or when the ownership problem is smaller than the planner infrastructure.

## 20. One-sentence answer if time is gone

> Independent components create global choices, so resolve those once; then let each compiler rewrite proceed only when explicit local semantics and the selected environment justify it.
