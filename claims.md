# Claim ledger — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Claims are classified as **CURRENT IMPLEMENTATION**, **PROPOSED / INTENDED DESIGN**, or
**NEEDS MEASUREMENT**. The main deck uses only current claims unless a boundary is explicitly labeled.

## CURRENT IMPLEMENTATION — whole-language planning

- `LanguageCompiler` is the single public semantic planner for `LanguageDefinition` on this path.
  Despite the name, it does **not** compile a user's source program.
- `LanguageDefinitionBuilder` is a C# authoring frontend for the canonical semantic configuration model.
- Wist `.wistdialect` parsing/translation is another frontend that produces `LanguageDefinition`; it is not
  a second planner.
- `LanguageCompiler.Compile(...)` performs toolchain API validation, feature resolution, contribution/provider
  resolution and backend artifact-route planning, returning diagnostics or an immutable `LanguagePlan`.
- Provider ambiguity can fail as `UTL2002`; `PreferCapabilityProvider(...)` makes integrator policy explicit.

## CURRENT IMPLEMENTATION — route planning

- Route planning works over transformations from **already selected contributions** for the selected backend.
- Non-pass transformations form the candidate conversion graph.
- `LanguageArtifactRoutePhase.FindBestRoute(...)` chooses minimum sum of declared transformation `Cost`.
- Equal-cost choices are deterministic through contribution-signature ordering.
- Selected passes are inserted where their artifact contracts fit; `Before` / `After` constraints order
  passes sharing a compatible contract.
- The resulting ordered `LanguageArtifactRoute` is stored in `LanguagePlan.Routes`.

Truth boundaries:

- structural/type compatibility **does not imply** semantic equivalence;
- deterministic selection **does not imply** semantic correctness;
- route `Cost` is a planning weight **not** measured execution latency;
- the planner does not search unselected packages/features as if every registered transformation were active.

## CURRENT IMPLEMENTATION — concrete decision record

`LanguagePlan` contains:

- original `Definition`;
- resolved `Features`;
- resolved `Contributions`;
- exact `RuntimeProviderContribution` / `RuntimeProvider`;
- backend `Routes`;
- `PlanHash`;
- `Summary`.

`PlanHash` is canonical identity of the expressed resolved plan. It is **not** a semantic proof,
security attestation, program identity, or performance certificate.

## CURRENT IMPLEMENTATION — runtime ownership

- `LanguageRuntime.Create` verifies the plan and exact runtime-provider/backend/route binding before creating
  a runtime session.
- `LanguageRuntime.Run` executes a request through that already-selected environment.
- Runtime creation does not call a second whole-language feature/provider/route planner.
- Therefore global composition can be resolved before repeated source requests.

This does **not** mean no runtime validation, no interfaces, no allocations, no parsing/lowering, or zero overhead.

## CURRENT IMPLEMENTATION — two reuse boundaries

- `WistEngine.Create` resolves one language environment:
  `LanguageDefinition -> LanguageCompiler -> LanguagePlan -> LanguageRuntime`.
- `Evaluate(code)` reuses that environment but still sends a source request through `Runtime.Run`.
- `Compile<TDelegate>` is a separate compiled-program boundary:
  `Runtime.Build -> durable program -> reusable delegate`.

Environment reuse **does not equal** compiled-program reuse.

## CURRENT IMPLEMENTATION — source-backed conference demo

`demo/Program.cs` now contains a compiler-specific route-changing proof:

```text
demo.core
-> route: demo.parse -> demo.lower.safe
-> Cost 7

+ demo.fast-path
-> route: demo.parse -> demo.lower.fast
-> Cost 2

LanguageRuntime.Create(enhancedPlan, ...)
-> input=41 output=42
```

The same source also retains a small `UTL2002 -> PreferCapabilityProvider` proof, but provider ambiguity is
not the main architectural example.

The two lowering functions are intentionally equivalent identity transforms in the synthetic fixture.
That equivalence comes from the fixture implementation, **not** from the route planner.

## CURRENT BUT APPENDIX / Q&A ONLY

The repository also contains current compiler mechanisms that are intentionally outside the main narrative,
including descriptor-gated optimization helpers, Wist intrinsic capability policy, IR-stage contract checks,
and bounded symbolic simplification. They remain supporting evidence, not a second talk.

PlanFuzz-related projects also exist in current UniversalToolchain; do not describe PlanFuzz as nonexistent.
Its scope is auxiliary testing evidence, not a main-talk guarantee.

## NEEDS MEASUREMENT

No exact-current raw benchmark-result artifact is bound into this presentation. Therefore all numerical
performance claims remain evidence debt:

- planning latency and allocations;
- runtime creation / materialization cost;
- first-execution / cold-start cost;
- steady-state overhead versus handwritten equivalents;
- cost of diagnostics/observability;
- scaling with numbers of features/contributions/routes;
- JIT/AOT specialization effects;
- workload-specific amortization and break-even.

Allowed wording:

> Planning moves some coordination work earlier. It does not make extensibility free.

## PROPOSED / NOT CLAIMED AS CURRENT GUARANTEE

The deck does not claim:

- automatic semantic compatibility proof for alternative routes;
- execution-time optimality from planning `Cost`;
- a general solver for hidden semantic assumptions;
- automatic pass scheduling from all compiler contracts;
- general equality saturation;
- sandboxing arbitrary in-process extensions;
- zero-cost extensibility;
- universal superiority over handwritten pipelines, DI, pass managers, LLVM, MLIR, Racket or MPS.

## Core wording

> **Extensibility becomes planning when choices stop being independent.**

> **Declare locally. Resolve globally. Execute concretely.**

Anti-takeaway:

> If one owner already knows the stable pipeline, wire it by hand.
