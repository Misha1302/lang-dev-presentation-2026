# Claim ledger — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Claims are classified as **CURRENT IMPLEMENTATION**, **PROPOSED / INTENDED DESIGN**, or **NEEDS MEASUREMENT**.

The main deck deliberately starts with current executable/compiler evidence, then separates the stronger proposed architecture.

## CURRENT IMPLEMENTATION — restricted pricing language

The pinned repository contains the shipped Wist dialect:

```text
UniversalToolchain/Dialects/examples/wist/pricing-restricted
```

Its documented composition:

- enables `Identifier`, `NativeTypes`, `Scopes`, `Variables`, `Whitespaces`;
- supports `interpreter` and `cil` backends;
- intentionally excludes unrelated conditions/loops/labels/C# interop capabilities;
- evaluates the shipped program `100.0 * 0.9 + 5.0` as `95`;
- is a composition-constrained runtime surface, **not** a hardened sandbox guarantee.

## CURRENT IMPLEMENTATION — Wist compiler path

The current Wist architecture has a compiler-specific path conceptually described as:

```text
source text
→ lexer / parser AST
→ module-oriented Bytecode
→ BytecodeToAbstractIrConverterImpl
→ AIR
→ backend-neutral optimization / specialization
→ interpreter or CIL backend
```

Important boundary:

- Bytecode and AIR are current Wist implementation artifacts;
- the generic UniversalToolchain language-authoring SDK does not require every language to use Wist Bytecode/AIR.

## CURRENT IMPLEMENTATION — cross-backend semantic parity

`UniversalToolchain/Tests/Backends/InterpreterBindingsParityTests.cs` currently exercises both the CIL and interpreter execution paths for:

- external named bindings;
- local variables combined with external arithmetic;
- reordered declared bindings;
- nested scopes;
- local names overlapping external `price` / `fee` names;
- deterministic shadowing behavior;
- stable local storage keys;
- fail-closed unknown-identifier behavior.

The main deck uses this as the concrete correctness boundary:

> a backend being reachable is not enough; both execution implementations must still implement the same language semantics for the covered cases.

The tests prove only the covered cases, not universal semantic equivalence.

## CURRENT IMPLEMENTATION — whole-language staging

- `LanguageDefinitionBuilder` and Wist configuration frontends produce the requested language definition.
- `LanguageCompiler.Compile(...)` performs whole-language resolution and returns diagnostics or `LanguagePlan`.
- `LanguageRuntime.Create(...)` materializes exact providers/backends/routes from the already-resolved plan.
- `Run` / `Build` process source after that whole-language resolution boundary.

This staging is a current strength that the proposed architecture keeps.

## CURRENT IMPLEMENTATION — LanguagePlan data

Current `LanguagePlan` contains:

- original `Definition`;
- resolved `Features`;
- resolved `Contributions`;
- exact `RuntimeProviderContribution` / `RuntimeProvider`;
- backend `Routes`;
- `PlanHash`;
- `Summary`.

The deck does **not** claim that current `LanguagePlan` stores:

- explicit semantic hard obligations;
- general requires/ensures effects for whole-language feasibility;
- rejected-candidate explanations;
- general selection provenance such as “why this implementation was chosen”.

Planning diagnostics live in the build/planning result; they are not fields of the successful current `LanguagePlan` object.

`PlanHash` identifies the expressed resolved plan. It is not semantic proof, security attestation or a performance certificate.

## CURRENT IMPLEMENTATION — route planning

Current `LanguageArtifactRoutePhase`:

1. derives contract-changing conversion edges from already-selected contributions for the selected backend;
2. calls `FindBestRoute(...)` over that conversion graph;
3. minimizes ordinary integer sum of declared transformation `Cost`;
4. uses deterministic contribution-signature ordering for equal-cost alternatives;
5. then calls `InsertPasses(...)` for selected same-contract passes;
6. reports `UTL2204` if a selected pass cannot be placed;
7. does not backtrack to a different conversion skeleton that could make that pass placeable.

Consequences:

- structural artifact-contract reachability **does not imply** semantic admissibility;
- deterministic selection **does not imply** semantic correctness;
- route `Cost` is preference/planning policy **not** execution latency;
- current routing is staged conversion-first/pass-second, not one global feasibility solve;
- the route layer does not generally model semantic state such as target legality or SSA properties.

## CURRENT IMPLEMENTATION — other confirmed planner boundaries

| Finding | Status | Current truth |
| --- | --- | --- |
| F-01 · route/pass feasibility | `CONFIRMED_CURRENT_IMPLEMENTATION` | minimum-cost conversion skeleton is chosen before selected passes are inserted; no pass-feasibility backtracking after `UTL2204` |
| F-02 · dependency/slot staging | `CONFIRMED_CURRENT_IMPLEMENTATION` | contribution/capability dependency traversal precedes slot policy replacement; composition is staged, not provenance-aware global solving |
| F-03 · mandatory contract-changing semantics | `CONFIRMED_MODEL_BOUNDARY` | route phase has candidate contract-changing conversions and selected same-contract passes, but no separate generic mandatory contract-changing transformation primitive |
| F-04 · artifact identity | `CONFIRMED_MODEL_BOUNDARY` | connectivity compares artifact Kind + stable ValueTypeIdentity; this is protocol identity, not arbitrary semantic or CLR-type proof |
| F-05 · verifier error surface | `CONFIRMED_CURRENT_IMPLEMENTATION` | `LanguagePlanVerifier` can throw for invariant violations; not every invalid composition is normalized into a planning diagnostic |
| F-06 · Cost | `CONFIRMED_CURRENT_IMPLEMENTATION` | cost uses `int` and ordinary addition; it is a local planner heuristic/policy value, not a benchmark objective |

## CURRENT IMPLEMENTATION — source-backed conference demo

The canonical presentation demo now uses current UniversalToolchain directly:

1. inspect `pricing-restricted`;
2. execute the shipped pricing program through `interpreter`;
3. execute the same program through `cil`;
4. assert both expose result `95`;
5. run the targeted `ShadowingAndNestedScope_WithLocalNamesOverlappingExternals_ShouldBeDeterministicAndParityStable` test.

This is stronger conference evidence than the former synthetic route-cost fixture because it demonstrates a real language surface and a real semantic parity boundary.

The historical/synthetic `Cost 7 → Cost 2` fixture remains useful evidence about current route preference, but it is no longer the main talk proof.

## NEEDS MEASUREMENT — performance

The repository contains `UniversalToolchain.Benchmarks`, including separate benchmark suites for:

- already-prepared hot-path formula invocation;
- public convenience `Evaluate` overhead;
- engine creation / formula compilation.

The benchmark README explicitly separates these workloads and requires raw BenchmarkDotNet artifacts with source/environment identity before publishing numerical claims.

No exact raw result artifact is bound into this presentation revision. Therefore the on-stage deck makes no numerical claim for:

- CIL versus C# speed;
- allocation counts;
- planner latency;
- materialization cost;
- steady-state extensibility overhead;
- graph scaling;
- amortization break-even.

Allowed wording:

> Composition can be resolved before repeated execution. That changes the lifecycle; it does not make extensibility free.

## PROPOSED / INTENDED DESIGN

The proposed general model is deliberately stronger than current UT:

```text
requested language semantics / target / policy
→ explicit hard obligations
→ candidate implementation requires / ensures / conflicts
→ feasible compiler plans
→ preference only among feasible plans
→ one inspectable concrete plan
```

Examples of hard obligations may include:

- required language semantics;
- backend legality;
- required validation/instrumentation under explicit policy;
- composition-relevant IR properties;
- required providers;
- conflicts that make a language combination inadmissible.

Most optimizations remain optional preference unless an explicit language/build/backend policy makes one mandatory.

The proposed model does not require SAT/SMT branding, proof-carrying compilation or a theorem prover.

## APPLICABILITY BOUNDARY

Prefer the smallest mechanism that already owns the decision:

- fixed explicit compiler pipeline for one known sequence;
- builder for configuration;
- DI for provider/object wiring;
- pass manager for a known pass set and invalidation model;
- MLIR-style legalization for local IR legality;
- whole-language planning only for expressed hard constraints crossing independently owned language/compiler components.

The planner is a bad architecture when hidden semantic assumptions still decide correctness.

## Core wording

> **Feasibility before preference.**

> **Resolve globally only what correctness cannot own locally.**

> **Declare requirements locally. Resolve feasibility globally. Execute one concrete plan.**

Anti-takeaway:

> If one owner already knows the stable compiler, wire it explicitly.
