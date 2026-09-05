# Claim ledger — LangDev 2026

UniversalToolchain is an **implementation witness**, not the source of truth for the general architecture. Conference-facing links use the repository's current `master` paths; the talk is not pinned to a UT commit.

The deck uses three status categories when interpretation depends on them:

- **IMPLEMENTED WITNESS** — current UT/Wist demonstrates the bounded mechanism or example;
- **GENERAL DESIGN** — architecture argued by the talk without claiming it is already UT behavior;
- **RESEARCH HYPOTHESIS** — a falsifiable proposal that still needs experiments.

## IMPLEMENTED WITNESS — declarative language selection

Current Wist profiles select language capabilities, policy, optimizers and backends through `.wistdialect` configuration. Dependency closure and implementation selection are resolved after the declaration.

Allowed claim: configuration says what language is wanted; composition resolves how an admissible compiler is assembled.

## IMPLEMENTED WITNESS — resolved compiler staging

Current UT separates `LanguageDefinition`, `LanguageCompiler`, immutable `LanguagePlan` and `LanguageRuntime`. Explicitly registered third-party packages enter the same typed planning path.

Allowed claim: language composition can be resolved before repeated execution. Per-program compilation and optimization still happen later; freezing composition does not pre-optimize future programs.

## IMPLEMENTED WITNESS — Wist representation stack

Current Wist uses a concrete AST → Bytecode → AIR → optimization → Interpreter/CIL path.

Boundary: Bytecode and AIR are Wist implementation choices. The general architecture does not require other languages to copy them.

## IMPLEMENTED WITNESS — planner feasibility before preference

Current `master` includes focused regressions showing route search can reject a cheaper route that violates mandatory descriptor ordering and select a more expensive feasible route.

Historical lesson: choosing a preferred conversion skeleton before all mandatory-pass/order requirements participate can miss a feasible compiler plan.

Allowed claim: requirements such as reachability, mandatory-pass coverage and ordering participate in admissibility before `Cost`/`Order` preference ranks surviving routes.

Boundary: route cost is a preference signal. It is not evidence of semantic equivalence, trust or preservation by itself.

## IMPLEMENTED WITNESS — local AIR deabstraction

The current optimizer contains a focused rewrite from:

```text
LoadEnvironment()
Push(slot)
LoadExternal<T>()
```

to one typed external-load intrinsic when the exact slot/type/backend conditions hold.

Allowed claim: three representation operations become one; local representation machinery disappears while the external-load meaning remains.

## IMPLEMENTED WITNESS — backend parity regression

Interpreter/CIL tests cover selected binding and shadowing scenarios. They are relational evidence for those cases, not a proof of equivalence for every Wist program.

## IMPLEMENTED WITNESS — benchmark boundary

UT keeps steady-state prepared execution, convenience `Evaluate` overhead and compilation/setup in separate BenchmarkDotNet suites. The hot-path suite excludes parsing, language composition, compiler construction and compilation.

Allowed claim: the architecture permits hot execution to be measured separately from authoring/composition/setup work.

## NEEDS-VERIFICATION — numerical performance

No current reviewed raw Release BenchmarkDotNet artifact is checked into this presentation repository. Therefore the conference deck publishes no C#↔Wist ratio, slowdown percentage, speedup percentage or amortization figure.

A numerical slide becomes publishable only after preserving raw BenchmarkDotNet output, source identity, environment metadata and correctness/parity precheck for comparable prepared call boundaries.

## GENERAL DESIGN — extensible authoring, concrete execution

The talk argues for this lifecycle:

```text
independently authored capabilities
→ declarative language configuration
→ composition / planning
→ one feasible concrete compiler plan
→ per-program compilation / optimization / execution
```

Core wording:

> Extensibility is an authoring-time property. It does not have to become a runtime tax.

This is not a zero-overhead guarantee. Composition, compiler construction and compilation may still cost more.

## GENERAL DESIGN — planning is a correctness boundary

A requested optimization, mandatory pass or lowering obligation may require a representation property before a backend is reached.

Therefore:

```text
requirements / obligations
→ admissible representation routes
→ preference among admissible routes
```

Core wording:

> Feasibility first. Preference second.

A cheaper route that reaches the backend is not sufficient if it cannot establish required properties.

## GENERAL DESIGN — local vs non-local optimization

Local/peephole optimization uses a small IR window and exact local facts. Non-local optimization uses facts outside that window, potentially across blocks, loop iterations or independently authored components.

The first running example is bounds-check elimination:

```text
Range: 0 <= i < N
Extent: N = Length(a)
→ SafeIndex(a, i)
→ repeated bounds check may be omitted
```

This example motivates the semantic architecture; it is not presented as an already implemented UT optimization.

## RESEARCH HYPOTHESIS — operation-centric write semantics

The second semantic domain is a write:

```text
Write(place, value)
```

Correctness may depend on partially independent dimensions such as writability, effects, volatility, atomicity, ordering, visibility, GC-barrier obligations and transaction context.

Hypothesis: consumers should query the dimensions relevant to an operation rather than require one inheritance hierarchy encoding the cross-product of semantic traits.

A write obligation can also constrain legal lowering. For example, a reference store may require GC-barrier behavior to be preserved or emitted before target/cost preference ranks feasible lowerings.

This is a general architecture example, not a claim about a currently implemented UT write-semantics subsystem.

## RESEARCH HYPOTHESIS — shared semantic query contracts

Producers should expose knowledge through stable typed semantic questions so consumers do not depend on concrete producer implementations.

Primary falsifiable criterion:

> Add a semantic producer. Change zero existing consumers.

Positive control: fresh consistent evidence may strengthen an answer.

Negative control: stale or contradictory evidence must never discharge an unsafe obligation.

## RESEARCH HYPOTHESIS — meaning and validity across lowering

Representation lowering and semantic knowledge are separate axes. When high-level nodes disappear, later passes may still need selected higher-level semantic questions answered.

Candidate mechanisms:

- provenance / stable semantic identity;
- typed semantic views or query contracts on the current representation;
- re-analysis on lowered IR;
- explicit validity / revision discipline.

A naked typed fact can become stale after a transformation. `Judgement` therefore names what is known together with subject, context, validity/revision and evidence. `Obligation` names what must be true before a transformation is legal.

These are proposed modeling terms, not a finished universal ontology.

## STRONGEST ALTERNATIVE

A shared semantic layer may be unnecessary. Local pass managers, IR interfaces, domain-specific analyses, explicit adapters and local invalidation rules may solve the real coupling problem with less machinery.

The research hypothesis earns its complexity only if experiments show lower pairwise coupling without sacrificing soundness or hiding domain semantics.

Open research questions retained in the main narrative: semantic identity across transforms, trust in evidence, invalidation granularity, and ownership of obligations across specialized engines.

## Final conference boundary

Already demonstrated: declarative selection, staged resolution into frozen plans, route feasibility before preference, preplanned backend routes, local deabstraction, selected backend parity regressions, and a disciplined benchmark boundary.

Research bet: shared semantic queries and validity discipline can preserve useful non-local optimization knowledge across independently authored components and changing representations, while semantic obligations can constrain legal lowering without pairwise wiring.
