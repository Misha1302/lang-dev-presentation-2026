# LangDev 2026 redesign audit — 2026-09-03

Presentation baseline: `Misha1302/lang-dev-presentation-2026@867485139ceb80fd23a38e59367f889db4ea38a1`.

Implementation truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Final thesis

A fixed compiler pipeline is often the best design when one owner knows all stages. The harder problem begins when independently authored language choices interact across dependencies, providers, ordering and artifact routes: then local declarations need one global planning authority that produces an inspectable concrete plan before runtime materialization.

Memory line: **Declare locally. Resolve globally. Execute concretely.**

## Narrative decision

| Candidate | Clarity | Implementation fit | Main risk | Decision |
| --- | --- | --- | --- | --- |
| Extensibility without runtime chaos | high | medium | sounds like a performance claim before measurement | reject as spine |
| Fixed pipeline -> composable languages | high | high | can become pipeline taxonomy | visual spine |
| Local declarations -> executable plan | medium | very high | too abstract / plan-first | central mental model after motivation |
| Choices stop being independent -> planning | very high | very high | needs compiler-specific proof | **chosen thesis** |

## Slide-by-slide audit of the 15-slide baseline

| Baseline | Intended job | Actual issue found on this audit | Decision |
| --- | --- | --- | --- |
| 1 | thesis / memory anchor | already sharp | KEEP |
| 2 | strongest conventional baseline | prevents strawman | KEEP |
| 3 | motivate language-family variability | motivation is necessary before UT terms | KEEP |
| 4 | define configuration -> planning threshold | strongest causal slide | KEEP |
| 5 | ownership + semantic configuration model | “typed contracts” was stronger than current identity semantics | REWRITE wording |
| 6 | turn pipeline into compiler transformation graph | “typed edges” could imply stronger CLR guarantees | REWRITE wording |
| 7 | explain automatic route selection | omitted the key conversion-first/pass-second feasibility boundary | REWRITE materially |
| 8 | define LanguagePlan and naming boundary | accurate; add verifier caveat to notes | KEEP + NOTES |
| 9 | planning/runtime/source lifecycle | accurate current boundary | KEEP |
| 10 | executable route-changing proof | demonstrates architecture, not just DSL syntax | KEEP |
| 11 | two amortization/reuse boundaries | already contains the durable-program distinction | MERGE with 12 |
| 12 | Evaluate vs Compile API boundary | correct but redundant and API-tour-like as a standalone slide | DELETE / MERGE into 11 |
| 13 | cost of extensibility | good; replace “typed boundaries” terminology | KEEP + WORDING |
| 14 | strongest counterargument | essential applicability boundary | KEEP |
| 15 | final decision rule | strongest transferable close | KEEP |

Final main deck: **14 slides**.

## Current implementation boundaries that changed the deck

- **F-01 — confirmed:** route phase chooses the minimum declared-cost conversion skeleton first, then inserts selected same-contract passes. It does not backtrack to a more expensive pass-feasible skeleton after `UTL2204`.
- **F-02 — confirmed:** contribution/capability dependency traversal precedes slot-policy replacement. Current planner is staged, not a provenance-aware global solver.
- **F-03 — confirmed model boundary:** current route model has candidate contract-changing conversions and selected same-contract passes; there is no separate mandatory contract-changing semantic transformation primitive.
- **F-04 — confirmed model boundary:** artifact connectivity is `Kind + ValueTypeIdentity`; explicit identities can be supplied, so connectivity is not itself a CLR runtime-type proof.
- **F-05 — confirmed error-surface boundary:** `LanguagePlanVerifier` can throw for plan invariant violations including backend/runtime input mismatch; not every invalid composition is a normal planning diagnostic.
- **F-06 — confirmed heuristic:** route `Cost` is an `int` planning value with deterministic signature tie-break, not runtime latency and not a general optimization objective.

## Central mental model

```text
independent package facts + integrator choices
                    |
                    v
             LanguageDefinition
                    |
                    v
 LanguageCompiler: staged whole-language resolution
                    |
                    v
             LanguagePlan
   selected contributions + routes + exact runtime provider
                    |
                    v
        LanguageRuntime materialization
                    |
                    v
      source requests follow the stored route
```

The audience-facing compression remains: **Declare locally. Resolve globally. Execute concretely.**

## Final title-only sequence and authored timing

1. When Extensibility Becomes Planning — 0:45
2. If one owner knows the pipeline, wire it by hand — 1:15
3. A language family creates choices across compiler stages — 1:15
4. Configuration becomes planning when choices stop being independent — 1:20
5. Local authors declare facts; one planner owns the global decision — 1:15
6. Local transformations turn one pipeline into a graph — 1:25
7. The planner selects one backend route — structurally, not semantically — 1:50
8. LanguageCompiler compiles a language definition — not source code — 1:15
9. Planning chooses the language; later stages process actual source — 1:15
10. Changing language composition changes the resolved route — 1:50
11. There are two different once boundaries — 1:40
12. Extensibility still has a price — 1:25
13. Sometimes the planner is the bigger problem — 1:35
14. Declare locally. Resolve globally. Execute concretely. — 1:00

Total authored main-talk budget: **19:05**. Official 25-minute content hard stop remains separate from the 5-minute Q&A window.

## 20% cut test

For a ~15:15 emergency version, skip slides 11 and 12: slide 9 already establishes the runtime boundary, and slide 13 already carries the “planner has a price” counterargument. Run the route-changing demo in ~65 seconds. The causal thesis remains intact.

## Remaining uncertainty

### NEEDS_MEASUREMENT

Planning latency/allocations, runtime creation cost, cold execution, steady-state overhead, graph-scaling behavior and amortization break-even. No numerical performance claim is allowed without an exact-current benchmark artifact.

### FUTURE_DESIGN

A planner that jointly optimizes conversion choice, mandatory transformations and broader constraints could remove some staged-feasibility limitations. That is a possible architectural direction, not current behavior and not required for the talk thesis.

### NEEDS_VERIFICATION

No additional load-bearing claim is intentionally left unverified at the pinned source snapshot. Conference/project logistics can still change independently of the source code.
