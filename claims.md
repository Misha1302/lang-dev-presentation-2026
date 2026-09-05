# Claim ledger — LangDev 2026

UniversalToolchain is an **implementation witness**, not the source of truth for the general architecture. Conference-facing links use the repository's current `master` paths; the talk is not pinned to a UT commit.

The deck uses three status categories when interpretation depends on them:

- **IMPLEMENTED WITNESS** — current UT/Wist demonstrates the bounded mechanism or example;
- **GENERAL DESIGN** — architecture argued by the talk without claiming it is already UT behavior;
- **RESEARCH HYPOTHESIS** — a falsifiable proposal that still needs experiments.

## GENERAL DESIGN — capability / extension vs dialect / language profile

A **capability / extension** is an independently authored reusable compiler slice. Depending on the domain it may contribute syntax, typing, analysis, lowering, optimization, backend behavior or tooling.

A **dialect / language profile** is a concrete declarative language configuration assembled from many reusable ecosystem pieces plus restrictions, policy and targets.

Allowed claim: capability and dialect are different entities. One capability can participate in multiple profiles; one profile selects and constrains multiple reusable pieces.

Terminology boundary: in this talk, “dialect” means language profile/configuration. It does not mean an MLIR IR dialect.

## GENERAL DESIGN — extensibility has two moves

The talk uses “extensible” in two independent senses that reinforce each other:

1. **extend the ecosystem** — add a new capability, optimizer, backend, type-system component or tooling contribution;
2. **compose a language** — select, restrict and recombine existing pieces into a different dialect/profile.

One ecosystem may therefore produce multiple materially different languages without duplicating the whole compiler.

Independent-authorship criterion:

> Two extension authors should not need a private handshake merely to enter the same ecosystem and participate in one dialect.

This is a design goal, not a claim that every arbitrary pair of extensions is semantically compatible. Conflicts and requirements still need explicit composition rules.

## IMPLEMENTED WITNESS — declarative language selection

Current Wist profiles select language capabilities, policy, optimizers and backends through `.wistdialect` configuration. Existing examples include a minimal arithmetic profile and richer/restricted profiles that reuse overlapping ecosystem pieces.

Allowed claim: configuration says **WHAT** language is wanted; dependency closure and implementation selection are resolved after the declaration.

Boundary: `.wistdialect` syntax is one implementation witness for the declarative boundary, not the general architecture itself.

## GENERAL DESIGN — dialect WHAT / planner HOW

The declarative profile owns the requested language surface, exclusions/restrictions, optimizer intent, policy and targets. Composition/planning owns dependency closure, provider selection, conflicts, ordering and executable representation routes.

Allowed claim:

> The dialect declares WHAT language we want. The composer / planner resolves HOW to assemble it.

A configuration is not yet a compiler. The output of composition should be one inspectable concrete compiler plan.

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

## GENERAL DESIGN — freeze the open world before repeated execution

The talk argues for this lifecycle:

```text
independently authored capabilities
→ declarative dialect / language profile
→ composition / planning
→ one feasible concrete compiler plan
→ per-program compilation / optimization / execution
```

Core wording: open-world authoring can terminate in a closed, inspectable plan. Extensibility machinery therefore does not have to remain in the repeated runtime path.

This is not a zero-overhead guarantee. Composition, compiler construction, parsing, compilation, code-size choices and target dispatch may still cost more.

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

## RESEARCH HYPOTHESIS — semantic extensibility is the same independence problem at a second level

The structural story says independently authored language extensions should not need private pairwise coordination merely to compose into one ecosystem/profile.

The semantic story asks the analogous question after optimization becomes non-local:

> Can independently authored semantic producers and consumers exchange useful knowledge without private producer-consumer APIs?

This callback is intentional. Semantic contracts are not a separate topic appended to the talk; they are the second level of the same extensibility problem.

## RESEARCH HYPOTHESIS — shared semantic query contracts

Producers should expose knowledge through stable typed semantic questions so consumers do not depend on concrete producer implementations.

Primary falsifiable criterion:

> Add a semantic producer. Change zero existing consumers.

Positive control: fresh consistent evidence may strengthen an answer.

Negative control: stale or contradictory evidence must never discharge an unsafe obligation.

A shared query schema does not imply one universal solver or one mega-service. Domain-specific analyses may remain specialized.

## RESEARCH HYPOTHESIS — operation-centric write semantics

The second semantic domain is a write:

```text
Write(place, value)
```

Correctness may depend on partially independent dimensions such as writability, effects, volatility, atomicity, ordering, visibility, GC-barrier obligations and transaction context.

Hypothesis: consumers should query the dimensions relevant to an operation rather than require one inheritance hierarchy encoding the cross-product of semantic traits.

This is a general architecture example, not a claim about a currently implemented UT write-semantics subsystem.

## RESEARCH HYPOTHESIS — Judgement, Obligation and validity

A naked typed fact can become stale after a transformation. `Judgement` therefore names what is known together with subject, value, context, revision/validity, evidence and assumptions.

`Obligation` names what must be true before a transformation or lowering is legal. Only valid Judgements may discharge an Obligation.

Example: a reference store may require GC-barrier behavior to be preserved or emitted. That semantic requirement constrains the feasible lowering set before target/cost preference ranks candidates.

This reconnects semantic legality to the earlier planner rule:

> Feasibility first. Preference second.

`Judgement` and `Obligation` are proposed modeling terms, not a finished universal ontology.

## RESEARCH HYPOTHESIS — meaning and validity across lowering

Representation lowering and semantic knowledge are separate axes. A more concrete representation does not automatically carry less semantic responsibility.

There is no universal inverse lowering: real transformations split, merge, fuse, delete and many-to-one lower operations. Rebuilding every previous IR is therefore not a general solution.

Candidate mechanisms for keeping selected questions answerable:

- preserve provenance / stable semantic identity;
- expose typed semantic views on the current representation;
- re-analyse the property on the lowered IR;
- maintain explicit validity / revision discipline.

## PRIOR ART BOUNDARY

LLVM demonstrates extensible pass infrastructure that resolves to concrete optimization pipelines. MLIR demonstrates semantic interfaces plus explicit legality/conversion across abstraction levels.

The talk uses them as prior art, not as novelty foils. Their existence strengthens the burden of proof for any additional shared semantic layer.

## STRONGEST ALTERNATIVE

A shared semantic layer may be unnecessary. Local pass managers, IR interfaces, domain-specific analyses, explicit adapters and local invalidation rules may solve the real coupling problem with less machinery.

The research hypothesis earns its complexity only if experiments show lower pairwise coupling without sacrificing soundness or hiding domain semantics.

Open research questions retained in the main narrative: semantic identity across transforms, trust in evidence, invalidation granularity, and ownership of obligations across specialized engines.

## Final conference boundary

**IMPLEMENTED WITNESS:** declarative language profiles, staged resolution into frozen plans, route feasibility before preference, local deabstraction, selected backend parity regressions, and a disciplined benchmark boundary.

**GENERAL DESIGN:** independent capabilities can be added and recombined into multiple dialects; dialects declare WHAT, planning resolves one feasible HOW; open-world composition can freeze before repeated execution.

**RESEARCH HYPOTHESIS:** shared semantic queries plus validity discipline can preserve optimization-quality meaning across independently authored components and changing representations, while semantic obligations constrain legal lowering without pairwise wiring.

Final synthesis:

> **Extensibility should disappear where it is machinery — and survive where it is meaning.**
