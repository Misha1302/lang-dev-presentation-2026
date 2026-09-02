# Claim boundaries and hostile Q&A — LangDev 2026

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

This is the rehearsal/Q&A owner. Implementation status lives in [`claims.md`](claims.md); executable demo
details live in [`DEMO.md`](DEMO.md).

Core wording:

> **Extensibility becomes planning when choices stop being independent.**

> **Declare locally. Resolve globally. Execute concretely.**

The answers below intentionally distinguish:

- **CURRENT IMPLEMENTATION** — source/test-backed at the pinned revision;
- **NEEDS MEASUREMENT** — performance/scaling without presentation-bound raw benchmark evidence;
- **DESIGN POSITIONING** — when this architecture is or is not appropriate.

## 1. Why does a compiler need a pipeline at all?

A compiler progressively transforms one representation into another: source text, syntax/semantic forms,
IRs, machine/runtime artifacts, or direct execution inputs. “Pipeline” is the ownership/order model for those
transformations; it need not always be a literal linear list.

## 2. Why do we need extensibility?

When one infrastructure must support a family of concrete languages, different integrators may want different
syntax/features, transformations, optimizers, backends, runtime policies, or packages without forking the
entire toolchain.

## 3. When is a handwritten pipeline better?

When one owner knows the stable stages and variability is small. Explicit wiring is simpler, easier to debug,
and should be preferred over a planner in that case.

## 4. What other ways can build a pipeline?

Depending on the decision: handwritten wiring, builder/configuration, DI for object binding/lifetime, a pass
manager for an already-known pass sequence, dialect/conversion machinery for IR legalization, or a graph/planner
when independent choices create global constraints.

## 5. When does configuration become planning?

Not when there are “many options,” but when options interact: dependencies, conflicts, provider ambiguity,
ordering constraints, backend reachability, or alternative artifact routes make the correct decision depend
on the whole selected language.

## 6. What concrete problem does UniversalToolchain solve in this talk?

It lets independently authored packages declare local language/compiler facts while one whole-language phase
resolves interacting choices into one inspectable `LanguagePlan` that a runtime materializes exactly.

## 7. Who is the framework author?

Conceptually, the owner of the composition protocol: typed artifact contracts, IDs, feature/contribution
descriptors, planning rules, diagnostics and runtime/materialization contracts.

## 8. Who is the package / extension author?

The author of independently contributed compiler/runtime pieces. They declare local facts and transformations;
they do **not** own the final whole-language pipeline.

## 9. Who is the language integrator?

The person/team choosing one concrete language: desired features, backends, provider preferences, overrides
and runtime policy. In Wist this choice can come from `.wistdialect`/options; in generic authoring it can come
from `LanguageDefinitionBuilder`.

## 10. Can one person be several of these roles?

Yes. These are conceptual authority boundaries, not job titles. One team can author framework, packages and
language definitions; the model still asks which decisions are local versus whole-language.

## 11. What is a feature?

For the talk: **what the language integrator wants to enable**. Current feature descriptors can own
contributions and express feature dependencies/conflicts/backend support.

## 12. What is a contribution?

A concrete package-provided piece participating in compiler/runtime architecture: for example a transformer,
backend, provider or other registered contribution with slot/capability/order metadata.

## 13. What is a capability?

An abstract requirement/ability identified independently of a concrete provider. Contributions may require or
provide capabilities.

## 14. What is a provider?

A contribution that satisfies a required capability. If several eligible contributions provide the same
required capability and policy does not choose one, current planning can fail with `UTL2002`.

## 15. What is a route?

The resolved ordered artifact path for a selected backend: `LanguageArtifactRoute` records source/target
contracts and the chosen transformation steps.

## 16. What is LanguageDefinition?

The canonical semantic model of **what concrete language is requested**: features, backends, runtime provider,
entry artifact, overrides, exclusions, policy and related configuration.

## 17. Is `.wistdialect` the planner?

No. It is a Wist configuration frontend. Current Wist code translates dialect/preset/text/file input into a
`LanguageDefinition`; `LanguageCompiler` remains the planning authority.

## 18. What role does LanguageDefinitionBuilder play?

It is another authoring frontend for `LanguageDefinition`. It collects the requested configuration. Building
the model is not the same thing as resolving global feature/contribution/provider/route choices.

## 19. Why insist on one canonical semantic configuration model?

So every frontend feeds the same semantic planning authority. Otherwise different DSLs/builders could encode
different hidden resolution rules and split ownership of global composition.

## 20. What is LanguageCompiler, despite its name?

**CURRENT:** the single public semantic planner for language definitions. `Compile(LanguageDefinition)`
returns diagnostics or a `LanguagePlan`. It does not compile the user's source program.

## 21. What is LanguagePlan?

The resolved answer: current plan data includes original definition, resolved features/contributions, exact
runtime provider, backend routes, `PlanHash` and `Summary`.

## 22. What is LanguageRuntime?

A materializer/executor for one immutable plan. `LanguageRuntime.Create` verifies exact provider/backend/route
binding and creates the runtime session; `Run` executes requests in that selected environment.

## 23. Who chooses the concrete compilation route?

`LanguageArtifactRoutePhase` inside `LanguageCompiler` after feature and contribution resolution.

## 24. Does UniversalToolchain search for a route automatically?

Yes, **within the graph of transformations from already-selected contributions** that support the backend.
It does not treat every registered/unselected package transformation as active.

## 25. What set of routes does it search?

Conversion edges are selected contributions whose `Transformation` is non-null and not a pass, filtered by
backend support. Search starts at `LanguageDefinition.EntryArtifact` and targets the selected backend input
contract (or compatible runtime-provider input when needed).

## 26. How is a route chosen?

Current algorithm accumulates transformation `Cost`, chooses the minimum-cost reachable structural path, and
uses deterministic contribution-signature ordering for equal-cost alternatives.

## 27. What does route Cost mean?

A **declared planning weight** in the protocol. It lets the planner prefer one structurally valid candidate
over another according to authored policy.

## 28. What does route Cost not mean?

It is not milliseconds, CPU cycles, throughput, allocation count, generated-code quality or a benchmark-derived
prediction. “Lower Cost” does not justify “faster runtime.”

## 29. What happens with selected passes?

After the base conversion route is found, current planner inserts selected pass transformations where their
source/target contract connects to the current artifact. Ordering uses pass `Order` plus `Before`/`After`
constraints; cycles can fail planning.

## 30. Does structural route compatibility prove semantic equivalence?

No. Matching artifact kind/value-type contracts prove only structural connectivity expressed by the protocol.
Two structurally compatible routes can still implement different semantics.

## 31. Does deterministic route selection prove correctness?

No. Reproducibility can be reproducibly wrong. Semantic correctness still requires specifications, tests,
oracles, review and truthful extension contracts.

## 32. Where is the authoring/planning/materialization/build/execution boundary?

Conceptually:

```text
authoring
-> LanguageDefinition
-> LanguageCompiler planning
-> LanguagePlan
-> LanguageRuntime.Create materialization
-> Run / Build source request
-> execution result or durable program
```

Planning chooses the language; source build/execution is later work.

## 33. What happens once per language environment?

In current Wist facade, `WistEngine.Create` resolves the `LanguageDefinition`, runs `LanguageCompiler`, obtains
one `LanguagePlan` and creates one runtime for that engine instance.

## 34. What happens once per compiled program?

`Compile<TDelegate>` performs `Runtime.Build`, materializes a durable program and creates a reusable delegate.
That is separate from language-environment planning.

## 35. Is Evaluate(code) compile-once/execute-many?

No. It reuses the already-planned environment, but every `Evaluate(code)` still sends the supplied source
through `Runtime.Run`.

## 36. Does moving planning earlier make extensibility free?

No. It can avoid repeated **global rediscovery** of language composition, but contracts, diagnostics, runtime
materialization, interfaces, parsing, lowering, optimization, code generation and execution still cost work.

## 37. What are the major costs of extensibility beyond runtime dispatch?

Contracts, versioning, global coordination, planner complexity, diagnostics, larger testing state space,
observability/debugging, hidden invariants, startup/materialization, and maintenance of extension interactions.

Performance magnitude and break-even remain **NEEDS MEASUREMENT**.

## 38. Why isn't this just DI / a pass manager / MLIR conversion?

Those mechanisms own different decisions. DI is strong when bindings are already known; pass managers execute
a known ordered pass set; conversion infrastructure handles IR legalization/conversion. Whole-language planning
is justified only when independently owned language choices create cross-stage decisions no local owner can make.

## 39. What is the strongest argument against this architecture?

You can replace straightforward compiler code with a distributed contract system whose correctness still
depends on extension authors expressing enough assumptions. The bad outcome is:

```text
planner complexity + hidden semantic coupling
```

If the variability is not real, do not build the planner.

## 40. What should the audience remember if there is only ten seconds?

> One fixed compiler? Wire it explicitly.
>
> Independent extensions whose choices interact? Let them declare local facts, resolve the cross-extension
> decisions globally into one inspectable plan, then execute that concrete answer.
>
> **Declare locally. Resolve globally. Execute concretely.**
