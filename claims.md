# Claim ledger — LangDev 2026

Current presentation truth snapshot: `Misha1302/UniversalToolchain@1078ddb5b9fd83b569a8ef0e590c4bec9594e1c5`.

Historical demo material may still reference `7005371d6c30175dff4b0e9f906a26218b0ee54d`, but that older snapshot must not be used to describe the current planner.

Claims are classified as **CURRENT IMPLEMENTATION**, **PROPOSED / INTENDED DESIGN**, **OPEN ARCHITECTURE QUESTION**, or **NEEDS MEASUREMENT**.

## CURRENT IMPLEMENTATION — restricted pricing language

The repository contains the Wist pricing-restricted dialect. Its role in the talk is a composition-constrained language profile, not a hardened sandbox guarantee.

## CURRENT IMPLEMENTATION — Wist compiler path

The current Wist implementation uses a concrete path conceptually described as:

```text
source text
→ lexer / parser AST
→ module-oriented Bytecode
→ AIR
→ backend-neutral optimization / specialization
→ interpreter or CIL backend
```

Boundary:

- Bytecode and AIR are current Wist implementation artifacts;
- the generic language-authoring architecture does not require every language to use Wist Bytecode/AIR.

## CURRENT IMPLEMENTATION — cross-backend semantic parity

`UniversalToolchain/Tests/Backends/InterpreterBindingsParityTests.cs` exercises Interpreter/CIL parity for covered binding and shadowing scenarios.

Allowed claim:

> Backend diversity is allowed; accidental semantic diversity is not.

The regression is relational evidence for covered programs, not a proof of equivalence for every Wist program.

## CURRENT IMPLEMENTATION — staged whole-language planning

`LanguageCompiler.Compile(...)` is staged:

1. feature resolution / dependency closure;
2. contribution and provider resolution;
3. artifact-route planning for each enabled backend;
4. immutable `LanguagePlan` construction and verification.

Provider ambiguity is fail-closed. Route reachability is not used as an implicit provider-selection policy.

`LanguageRuntime.Create(...)` materializes the already-resolved plan. Runtime execution does not reopen feature/provider/route planning.

## CURRENT IMPLEMENTATION — third-party package path

The generic authoring path supports explicit typed package registration. A third-party package can provide Feature/Contribution descriptors plus implementations, be registered with `LanguagePackageRegistry.AddPackage(...)`, and enter the same `LanguageCompiler` flow without the planner hard-coding that package.

Source-backed sample: `samples/Acme.PricingLanguage/Program.cs`.

This is the preferred example for “independent extension author joins the ecosystem”.

## CURRENT IMPLEMENTATION — LanguagePlan data

Current `LanguagePlan` contains the requested definition, resolved features/contributions, selected runtime provider, per-backend routes, `PlanHash`, and summary data.

`PlanHash` identifies the resolved snapshot. It is not semantic proof, security attestation, or a performance certificate.

## CURRENT IMPLEMENTATION — route planning at 1078ddb

Current `LanguageArtifactRoutePhase` separates selected contract-changing conversions from selected same-contract passes.

For each enabled backend it:

1. requires exactly one selected backend capability owner;
2. determines the backend/runtime input artifact contract;
3. collects already-selected transformation contributions compatible with that backend;
4. searches conversion routes with state `(artifact contract, mandatory-pass coverage)`;
5. minimizes declared route `Cost` only among states that cover all mandatory pass contracts;
6. fails closed on distinct equal-best routes (`UTL2207`);
7. inserts same-contract passes with explicit ordering/ambiguity checks;
8. validates descriptor-level and definition-level executable ordering on the produced route;
9. constructs the route only after those validations succeed.

Confirmed current repair relative to the old `7005371...` snapshot:

> Mandatory-pass coverage participates in route search before route Cost chooses a candidate.

Therefore the old claim “current routing chooses the cheapest conversion skeleton first and only afterward discovers whether mandatory passes fit” is stale and must not appear as current truth.

## CURRENT IMPLEMENTATION — remaining route-order boundary

At `1078ddb`, conversion-route search still chooses its minimum-cost route before `ValidateDescriptorRouteOrder(...)` / `ValidateDefinitionRouteOrder(...)` run on the executable steps.

This creates a focused open implementation question:

> If the cheapest conversion route violates an executable Before/After constraint, but a more expensive route is valid, does the planner search the more expensive route or fail after validating only the cheapest candidate?

Source control flow strongly suggests the latter, but the presentation must treat this as **NEEDS FOCUSED REGRESSION** until the counterexample test is executed.

Until that regression passes, current on-stage wording is deliberately narrower:

- **verified current scope:** artifact reachability + mandatory-pass coverage + equal-best ambiguity before Cost;
- **architectural target:** all correctness constraints participate in feasibility before preferences rank alternatives.

## CURRENT IMPLEMENTATION — artifact identity and Cost boundary

Artifact route connectivity compares declared contract identity. Matching identities do not prove that independently authored transformations preserve identical semantics.

Route `Cost` is a planner preference weight. It does not prove semantic preservation, trust, runtime latency, or optimization quality.

## CURRENT IMPLEMENTATION — language-time vs program-time lifecycle

Planning freezes language composition once into `LanguagePlan`.

Per program, the runtime/build pipeline still:

```text
select the already-planned backend route
→ apply concrete route transformations
→ verify each produced artifact contract
→ run the selected passes/optimizers represented by that route
→ execute/materialize the backend
```

Therefore “freeze” means composition uncertainty is removed. It does **not** mean program optimization happened when the plan was built.

## CURRENT IMPLEMENTATION — bounded reflection

Current capability projection uses reflection only over exact implementation types already selected by `LanguagePlan`.

`SelectedCapabilityCatalogBuilder` performs no feature/package/backend/route selection. Reflection removes wiring; planning remains the semantic authority.

## CURRENT IMPLEMENTATION — local deabstraction witness

The AIR rewrite demonstrated in the deck turns the exact pattern:

```text
LoadEnvironment()
Push(slot)
LoadExternal<T>()
```

into a typed direct external-load intrinsic when the required slot/type/backend conditions hold.

Three representation operations become one. Representation machinery disappears; external-load semantics do not.

## NEEDS MEASUREMENT — performance

No raw BenchmarkDotNet artifact is bound into this presentation revision. Therefore the deck makes no numerical claim for CIL-vs-C# speed, planner latency, materialization cost, allocation count, or amortization break-even.

Allowed wording:

> Composition can be resolved before repeated execution. That changes the lifecycle; it does not make extensibility free.

## PROPOSED / INTENDED DESIGN — semantic contracts

The research layer proposes typed/versioned shared semantic query schemas so independently authored producers and consumers do not require pairwise adapters.

Falsifiable target:

> Add a semantic producer. Change zero existing consumers.

The proposal does not require one universal ontology, one solver, or one global semantic service.

## OPEN ARCHITECTURE QUESTION — who owns semantic query composition?

The contract schema boundary does not yet answer:

- who combines multiple producer answers;
- how contradictory evidence is handled;
- where caching lives;
- who invalidates stale evidence after transformations;
- whether different semantic domains use different engines;
- how engine selection is exposed without creating a mega-solver.

The deck must present these as open design questions, not current implementation facts.

## PROPOSED / INTENDED DESIGN — obligations and validity

The research model distinguishes:

- contextual `Judgement` — what is known, with subject/context/revision/evidence/assumptions;
- semantic `Obligation` — what must hold before a transformation or check elimination is legal.

Negative control requirement:

> stale or contradictory producer evidence must not discharge an obligation.

## STRONGEST ALTERNATIVE

Before introducing a shared semantic substrate, prefer the smallest mechanism that already owns the decision:

- explicit compiler pipeline for one stable sequence;
- builder/DI for configuration and object wiring;
- pass manager for a known pass set and invalidation model;
- MLIR-style interfaces/legalization for local IR semantics;
- domain-specific analysis APIs and adapters where cross-domain reuse is limited.

A shared semantic-contract layer earns its complexity only if it measurably improves producer independence, correctness, or coupling relative to those local mechanisms.

## Core wording

> **Feasibility before preference.**

Current implementation evidence supports this fully for mandatory-pass route coverage; broader correctness-before-preference remains the architectural target until each interaction has regression evidence.

> **Resolve globally only what correctness cannot own locally.**

> **Declare requirements locally. Resolve feasibility globally. Execute one concrete plan.**

Anti-takeaway:

> If one owner already knows the stable compiler, wire it explicitly.
