# Claim ledger — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## CURRENT SOURCE-BACKED

- `LanguageCompiler` is the single public semantic planner; it resolves features, contributions and artifact routes and returns a `LanguagePlan` or diagnostics.
- Wist ships multiple preset definitions including `minimal-arithmetic`, `pricing-restricted`, `full-default`, `full-default-native`, `ssa`, and `composition-restricted`.
- The public `.wistdialect` path translates configuration to a `LanguageDefinition`; dependency/contribution/provider/route resolution remains owned by `LanguageCompiler`.
- Current Wist does **not** implement base-dialect inheritance.
- `LanguagePlan` contains resolved Features, Contributions, RuntimeProvider, Routes, PlanHash and Summary.
- Runtime creation verifies the plan and exact provider/binding requirements and materializes planned components; `Run` does not invoke a second global feature/provider/route planning pass.
- Artifact route compatibility is structural: kind and value-type identity are checked by `LanguageArtifactRoute.ContractsConnect`.
- Route `TotalCost` is a planning quantity computed from step costs.
- Restricted Wist composition/interop policy is not process isolation or a sandbox.

## EVIDENCE-BACKED

- Presentation CI executes `demo/Program.cs` against the exact source revision above.
- The demo plans the shipped Wist `minimal-arithmetic` definition, constructs a real `LanguageRuntime`, and executes two expressions on that runtime.
- Render validation captures every main and appendix slide at 1920×1080 and 1366×768 and fails on browser-reported overflow.

## CONCEPTUAL MODEL

- “Configuration becomes planning when choices stop being independent.” This is an explanatory abstraction over the dependency/provider/conflict/order/route/runtime constraints supported by current source.
- “Open while composing. Concrete while executing.” means global composition choices are resolved before repeated execution; it does not mean runtime objects or dynamic dispatch vanish.
- Framework author / package author / language integrator / runtime user are explanatory roles, not claims about mandatory organizational boundaries.
- Planning can be viewed as moving a class of whole-language decisions to a deliberate composition boundary.

## NEEDS MEASUREMENT

- planning latency and allocation cost;
- runtime creation latency and allocation cost;
- first-execution/cold-start cost;
- steady-state overhead compared with a handwritten equivalent pipeline;
- JIT/AOT specialization or devirtualization effects;
- workload-specific break-even point for amortizing planning.

No exact-current raw benchmark-result artifact is used by this presentation, so the deck contains no numerical performance comparison.

## FUTURE / NOT CURRENT

- automatic semantic compatibility checking;
- sandboxing untrusted extensions;
- planner-driven code specialization/devirtualization;
- proof that a selected route is execution-time optimal.

## NOT CLAIMED

- zero-cost extensibility;
- extensibility is free;
- same performance as handwritten C#;
- all abstractions or dispatch disappear;
- planning guarantees JIT devirtualization/specialization;
- planner finds a globally optimal language;
- route cost equals runtime latency;
- valid plan implies semantic correctness or security;
- restricted dialect means sandbox;
- PlanHash is semantic equivalence or security attestation;
- deterministic selection implies semantic equivalence;
- UniversalToolchain is universally better than manual composition, DI, builders, Racket, MLIR, MPS or MontiCore.
