# Adversarial review — When Extensibility Becomes Planning

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Presentation baseline attacked: `Misha1302/lang-dev-presentation-2026@59514e86d2708cc7b70d87e3f7b93d872ac78b6c`.

Review date: `2026-09-03`.

## Narrative candidates reconsidered

### A — Problem -> extensibility cost -> planner

Strong causal logic, but too abstract before the audience has a compiler-shaped failure case.

### B — Build a compiler progressively until manual composition breaks

Intuitive, but spends too much conference time constructing an example before reaching the architecture.

### C — Fixed pipeline -> configurable pipeline -> transformation graph -> planner

Strongest visual progression. It makes route planning compiler-specific instead of looking like generic DI.

### D — Extensibility is a coordination problem

Strongest thesis and most transferable takeaway, but needs C's concrete graph to avoid sounding generic.

## Decision

Use **C as the visual spine** and **D as the thesis** under:

> **When Extensibility Becomes Planning**

Memory line:

> **Declare locally. Resolve globally. Execute concretely.**

## Null hypothesis

The null hypothesis is:

> “A builder, DI container and explicit pass list are enough; a whole-language planner is unnecessary
> architecture.”

The talk only defeats that null hypothesis if it demonstrates a decision that:

1. depends on multiple independently authored choices;
2. is not owned by one local extension;
3. is compiler-specific rather than merely object construction;
4. produces a concrete, inspectable result used by runtime.

The transformation-route example now satisfies all four better than the previous central UTL2002 example.

## Hostile review

### 1. “The planner is not needed; just wire the pipeline.”

**Attack:** if one owner knows all stages, the planner adds indirection and failure modes.

**Finding:** valid.

**Correction in deck:** slide 2 opens with the handwritten baseline and slide 14 repeats the decision rule.
The talk no longer treats direct wiring as primitive architecture that needs replacement.

**Status:** PASS.

### 2. “A builder is sufficient.”

**Attack:** `LanguageDefinitionBuilder` already describes the language. Why compile configuration again?

**Finding:** a builder can construct the requested semantic model, but it does not by itself own dependency
closure, provider ambiguity, cross-contribution ordering or artifact-route search.

**Correction in deck:** slide 5 now makes `.wistdialect` and C# builder explicit frontends into the same
`LanguageDefinition`, followed by one planning authority.

**Status:** PASS.

### 3. “DI is sufficient.”

**Attack:** capabilities/providers sound exactly like dependency injection.

**Finding:** provider ambiguity alone was too DI-shaped for the main example.

**Correction in deck:** provider ambiguity is demoted to secondary demo evidence. Slides 6–7 and the primary
demo use typed artifact transformation routes, which are compiler composition decisions. Appendix retains
the DI boundary.

**Status:** PASS.

### 4. “The route graph is unnecessarily clever.”

**Attack:** alternatives can be expressed with conditionals or a manually ordered list.

**Finding:** true when one integration owner controls the alternatives. The graph earns its cost only when
extensions independently contribute edges and the final backend path depends on the selected language.

**Correction in deck:** slide 6 begins from the fixed line and introduces one alternative edge only after
independent ownership exists. Slide 14 explicitly says to choose a smaller mechanism otherwise.

**Status:** PASS.

### 5. “`LanguageCompiler` is a confusing name.”

**Attack:** audience will assume it compiles source programs.

**Finding:** material confusion risk.

**Correction in deck:** slide 8 now states in the title that `LanguageCompiler` compiles a
`LanguageDefinition` into a `LanguagePlan`, **not source code**. Notes repeat the current source comment:
single public semantic planner for language definitions.

**Status:** PASS.

### 6. “The performance thesis is unproved.”

**Attack:** moving planning earlier might still be slower overall; route Cost could mislead people into
thinking it predicts speed.

**Finding:** valid.

**Correction in deck:** slide 7 says Cost is a declared planning weight, slide 10 repeats that lower demo
Cost is not measured speed, and slide 13 keeps all performance impact under `NEEDS MEASUREMENT`.
No numerical benchmark claim exists.

**Status:** PASS.

### 7. “Route Cost is misleading.”

**Attack:** “minimum cost route” sounds like runtime optimization.

**Finding:** high risk.

**Correction in deck:** every main location using route Cost qualifies it as planner policy. The demo says
“Lower Cost means planner preference here — not measured speed.” `claims.md` and Q&A own the same boundary.

**Status:** PASS.

### 8. “The example still is not compiler-specific.”

**Attack:** UTL2002 plus provider preference could be shown with any plugin container.

**Finding:** true of the previous main demo.

**Correction in deck:** the executable proof now changes `Syntax -> AIR` route selection when an extension
feature contributes an alternative transformation edge. UTL2002 remains only secondary evidence.

**Status:** PASS.

### 9. “The talk still requires prior UniversalToolchain knowledge.”

**Attack:** terms such as feature, contribution, capability, provider, route and LanguagePlan can become an API tour.

**Finding:** partially valid in the previous slide 5.

**Correction in deck:** terms are introduced by ownership and cause:
- feature = what the language integrator wants enabled;
- contribution = concrete package piece;
- capability = abstract requirement;
- provider = contribution satisfying it;
- route = resolved ordered artifact path;
- LanguageDefinition = requested concrete language;
- LanguagePlan = resolved answer;
- runtime = materializer/executor.

Slide 5 also shows the canonical configuration flow instead of a glossary dump.

**Status:** PASS.

### 10. “The narrative is two talks again.”

**Attack:** planner architecture plus CSE/SSA/intrinsics becomes two unrelated presentations.

**Finding:** previous repository documents still contained stale “Resolve globally. Justify locally” framing,
even though the main 15-slide deck had already removed most of that material.

**Correction in deck/docs:** main narrative remains planning-only. CSE, semantic descriptors, IR-stage
contracts and e-graph material remain appendix/Q&A. `CLAIM_BOUNDARIES_40_QA.md` and this review are rewritten
around the planning thesis instead of the old two-talk narrative.

**Status:** PASS.

## Additional hostile checks

### Hidden semantic coupling

A structurally compatible edge can still be semantically wrong.

**Mitigation:** slide 7 visibly separates structural guarantee from semantic non-guarantees. No claim that
planner proves route equivalence.

### Distributed contract-system failure mode

A planner can make the system harder to understand if contracts fail to encode the assumptions that matter.

**Mitigation:** slide 14 states this as the main counterargument, not a footnote.

### Lifecycle ambiguity

“Planning once” can accidentally imply “source compiled once.”

**Mitigation:** slide 9 separates planning/materialization/source build/execution; slides 11–12 separately
show environment reuse and compiled-program reuse.

### Configuration authority split

A textual DSL could accidentally look like a second planner or textual order could look executable.

**Mitigation:** slide 5 shows `.wistdialect` and C# builder converging on one `LanguageDefinition` and one
`LanguageCompiler`.

### Observability

A global planner that cannot explain its result would be difficult to debug.

**Mitigation:** main slide 8 exposes `Features`, `Contributions`, `RuntimeProvider`, `Routes`, `PlanHash`,
and `Summary`; demo prints exact route choices. No invented ExplainPlan subsystem is claimed.

## 5-second test for every main slide

1. **Title:** extensibility can become planning.
2. **Baseline:** fixed pipeline -> wire it explicitly.
3. **Motivation:** one infrastructure can serve a family of languages.
4. **Threshold:** coupling, not option count, creates planning.
5. **Ownership:** local facts, one global planner, one semantic config model.
6. **Compiler failure case:** transformations form a graph.
7. **Selection:** planner searches selected typed edges by declared cost.
8. **Answer:** LanguageDefinition -> LanguagePlan; LanguageCompiler is not source compilation.
9. **Lifecycle:** planning/materialization happen before source build/execution.
10. **Proof:** enabling an extension changes the resolved route.
11. **Boundary A/B:** environment reuse is not program reuse.
12. **Evaluate:** source request still does work; Compile creates durable program reuse.
13. **Price:** extensibility costs contracts, coordination, testing and runtime work.
14. **Counterargument:** use the smallest mechanism; planner can be the bigger problem.
15. **Rule:** Declare locally. Resolve globally. Execute concretely.

## Remaining evidence debt

The architecture claim is source-backed. The following remain **NEEDS MEASUREMENT**:

- planning latency / allocations;
- runtime materialization cost;
- first execution;
- steady-state overhead;
- route-graph scaling;
- diagnostics/observability cost;
- amortization break-even.

These are not blockers for the architectural talk as long as no speed claim is made.
