# Claim ledger — LangDev 2026

UniversalToolchain is an **implementation witness**, not the source of truth for the general architecture. Conference-facing links use the repository's current `master` paths; the talk is not pinned to a UT commit.

The deck uses four status categories when interpretation depends on them:

- **VERIFIED PRIOR ART** — externally verified mechanisms from primary/upstream sources;
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

## VERIFIED PRIOR ART — MLIR extensibility and conversion

MLIR is strong prior art for extensible compiler infrastructure. Official MLIR documentation supports the following bounded claims:

- dialects provide extensible IR namespaces with custom operations, types and attributes;
- `OpInterface` / dialect interfaces let generic infrastructure query dialect-defined behavior;
- Dialect Conversion uses a `ConversionTarget`, legalization rules and rewrite patterns, and can backtrack/rollback along legalization paths;
- pass infrastructure supports registered, textual and dynamically constructed pipelines;
- the Transform dialect provides an IR for expressing and controlling transformations.

Allowed claim: MLIR already provides substantial machinery for representation extensibility, semantic interfaces, legality/conversion and programmable transformations. The talk must not imply that MLIR cannot compose IR dialects, build legalization paths, target unusual hardware, or express custom compiler policy in user code.

Primary sources:

- https://mlir.llvm.org/docs/Dialects/
- https://mlir.llvm.org/docs/Interfaces/
- https://mlir.llvm.org/docs/DialectConversion/
- https://mlir.llvm.org/docs/PassManagement/
- https://mlir.llvm.org/docs/Dialects/Transform/
- Alex Zinenko, LLVM Developer Meeting 2023, *MLIR Is Not an ML Compiler, and Other Common Misconceptions*.

The Zinenko talk explicitly frames MLIR as a collection of abstractions and transforms for assembling a compiler rather than one compiler with a single established pass pipeline, target selection, heuristics and benchmark policy.

## GENERAL DESIGN — the MLIR / LanguagePlan scope boundary

The early MLIR bridge asks a narrower architectural question than “is MLIR extensible?”:

> Once independently authored language capabilities, alternative providers, conflicts, mandatory transformations, representation requirements, routes and backends coexist, which coherent compiler are we building for this language profile and target?

Allowed claim: UT treats this whole-language/compiler resolution as a first-class planning object and research subject. This is a scope/ownership distinction, not a claim that MLIR user code is incapable of implementing such policy.

Memorable distinction:

> **MLIR makes compiler representations extensible. We are asking how compiler composition itself becomes resolvable.**

Terminology remains explicit: this talk's `dialect` means declarative language profile; an MLIR dialect is an IR namespace / semantic extension.

## GENERAL DESIGN — MLIR may be a provider, not a competitor

A future compiler plan could select an MLIR-based representation/transformation subsystem for the stages where MLIR is appropriate and then lower to LLVM or to a specialized backend.

This is conceptual architecture only. Current UT does **not** implement MLIR, Roslyn, NIR or other third-party compiler subsystems as selectable `LanguagePlan` providers.

## RESEARCH HYPOTHESIS — whole-compiler subsystem composition must earn its layer

Broad third-party compiler-subsystem composition, including MLIR/Roslyn/NIR provider integration and universal cross-subsystem semantic contracts, is not implemented evidence. It remains a research hypothesis.

Falsifiability condition:

> If MLIR plus local interfaces, pass pipelines and adapters resolves the same composition problem with less machinery, the additional UT abstraction layer is not justified.

## VERIFIED PRIOR ART — hardware/toolchain diversity

Hardware evidence is validation, not the main causal story. Primary/upstream examples show both patterns:

- Google Coral documents an MLIR/IREE compiler path for the RISC-V-based Coral NPU, including target-specific plugins and dialects;
- AMD/Xilinx MLIR-AIE is an MLIR-based toolchain for AI Engine devices and uses representations at multiple abstraction levels;
- Tenstorrent `tt-mlir` is an MLIR-based compiler infrastructure with several target-specific dialects;
- Buddy-MLIR's DynamicVector proposal uses RVV as an end-to-end example and explicitly warns that an architecture-specific RVV dialect without a generic vector abstraction risks becoming a silo;
- Mesa RADV deliberately uses its own shader stack: SPIR-V is translated to NIR, optimized/lowered in NIR, then the lowered NIR is passed to the ACO backend for GPU-specific ISA generation.

Allowed conclusion only:

> New hardware does not imply MLIR failure. Real compiler ecosystems use both MLIR-based multi-level stacks and deliberately specialized IR/backend stacks.

The deck does not turn these examples into an adoption trend, commercial-market-share claim, or a claim that one architecture is universally preferable.

Primary sources:

- https://developers.google.com/coral/guides/software/mlir-iree-compilers
- https://xilinx.github.io/mlir-aie/latest/getting-started/
- https://docs.tenstorrent.com/tt-mlir/overview.html
- https://github.com/buddy-compiler/buddy-mlir/blob/main/docs/DynamicVector.md
- https://docs.mesa3d.org/drivers/radv.html

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

LLVM demonstrates extensible pass infrastructure that resolves to concrete optimization pipelines. MLIR demonstrates extensible IR dialects, interfaces, explicit legality/conversion, configurable pass infrastructure and programmable transformations.

The talk uses them as prior art, not as novelty foils. In particular, MLIR Dialect Conversion already has legalization paths with rollback/backtracking, and the Transform dialect / PassManager already provide programmable transformation policy. Their existence strengthens the burden of proof for any additional planning or shared semantic layer.

Hardware evidence is deliberately secondary. New or unusual hardware is not evidence that MLIR “failed”; architecture-specific validation belongs in appendix/research discussion rather than the main causal chain.

## STRONGEST ALTERNATIVE

A shared semantic layer may be unnecessary. Local pass managers, IR interfaces, domain-specific analyses, explicit adapters and local invalidation rules may solve the real coupling problem with less machinery.

The research hypothesis earns its complexity only if experiments show lower pairwise coupling without sacrificing soundness or hiding domain semantics.

The same falsifiability standard applies to the planning layer: if MLIR plus local policy/adapters expresses the required whole-composition resolution with less machinery and equal inspectability, the additional UT layer should be removed rather than defended rhetorically.

Open research questions retained in the main narrative: semantic identity across transforms, trust in evidence, invalidation granularity, and ownership of obligations across specialized engines.

## Final conference boundary

**VERIFIED PRIOR ART:** MLIR provides extensible IR dialects, semantic interfaces, Dialect Conversion legality/legalization, configurable pass pipelines and the Transform dialect.

**IMPLEMENTED WITNESS:** declarative language profiles, staged resolution into frozen plans, route feasibility before preference, local deabstraction, selected backend parity regressions, and a disciplined benchmark boundary.

**GENERAL DESIGN:** independent capabilities can be added and recombined into multiple dialects; dialects declare WHAT, planning resolves one feasible HOW; open-world composition can freeze before repeated execution; an MLIR-based subsystem could conceptually participate as a provider.

**RESEARCH HYPOTHESIS:** broad third-party compiler-subsystem composition and shared semantic queries plus validity discipline can preserve optimization-quality meaning across independently authored components and changing representations, while semantic obligations constrain legal lowering without pairwise wiring.

Final synthesis:

> **Extensibility should disappear where it is machinery — and survive where it is meaning.**
