# LangDev 2026 — UniversalToolchain presentation

Conference deck:

> **When Extensibility Becomes Planning**
>
> *Building a concrete compiler from independent language extensions*

Memory anchor:

> **Declare locally. Resolve globally. Execute concretely.**

## Audience memory target

One question:

> When does language extensibility stop being configuration and become a planning problem?

One answer:

> When independently authored choices start interacting across compiler stages, local declarations are no
> longer enough: resolve the whole-language choices globally into one inspectable plan, then materialize and
> execute that concrete answer.

One picture:

```text
local extension facts + integrator choices
                ↓
         LanguageDefinition
                ↓
         LanguageCompiler
                ↓
      immutable LanguagePlan
                ↓
      one concrete backend route
                ↓
         LanguageRuntime
```

## Redesign snapshot

This redesign started from presentation HEAD:

- `Misha1302/lang-dev-presentation-2026@59514e86d2708cc7b70d87e3f7b93d872ac78b6c`.

All load-bearing implementation claims were revalidated against:

- `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Implementation claims follow this evidence order:

```text
implementation -> tests -> executable behavior -> architecture docs -> README/comments
```

## Chosen narrative

Four candidate framings were reconsidered:

- problem -> extensibility cost -> planner;
- progressively build a compiler until manual composition breaks;
- fixed pipeline -> configurable pipeline -> transformation graph -> planner;
- extensibility is a coordination problem.

The final deck is a hybrid of the strongest two:

> **Fixed pipeline -> choices -> transformation graph -> global planning**, framed by
> **extensibility is a coordination problem**.

UniversalToolchain remains the case study, not the premise of the talk.

## Main narrative

```text
one stable pipeline
    ↓
wire it by hand

shared infrastructure serves a family of languages
    ↓
independently authored choices appear
    ↓
dependencies / conflicts / providers / ordering / routes
    ↓
local decisions are no longer sufficient
    ↓
one canonical LanguageDefinition
    ↓
LanguageCompiler resolves whole-language choices
    ↓
LanguagePlan records the concrete answer and route
    ↓
LanguageRuntime materializes exactly that plan
    ↓
source requests follow the selected route
```

The main deck remains **15 slides**. CSE, semantic descriptors, SSA contracts, e-graph details and related
compiler mechanisms stay in appendix/Q&A rather than becoming a second narrative.

## Ownership model

The talk now makes five conceptual roles explicit:

- **framework author** — defines contracts and composition protocol;
- **package / extension author** — contributes local compiler/runtime pieces and capability requirements;
- **language integrator** — chooses desired features, backend and policy for one concrete language;
- **planner** — sees the whole selected language and resolves global choices;
- **runtime** — materializes and executes the resolved plan.

These are conceptual roles; one person/team may perform several.

## Configuration boundary

Wist configuration frontends converge on one semantic model:

```text
.wistdialect ─┐
C# builder ───┴→ LanguageDefinition → LanguageCompiler → LanguagePlan
```

`.wistdialect` is not the planner, and textual configuration order is not the compiler route.

## Route truth

Current `LanguageArtifactRoutePhase`:

1. starts from transformations belonging to selected contributions for a backend;
2. searches the type-compatible conversion graph;
3. chooses minimum sum of declared transformation `Cost`;
4. resolves equal-cost alternatives deterministically;
5. inserts selected passes where their artifact contracts fit;
6. stores the ordered route in `LanguagePlan`.

Truth boundaries:

- deterministic route selection **≠** semantic correctness;
- structural/type compatibility **≠** semantic equivalence;
- route `Cost` **≠** runtime latency;
- `PlanHash` **≠** correctness/security proof.

## Demo

See [`DEMO.md`](DEMO.md).

The primary executable story is now route-specific:

```text
demo.core
-> demo.parse -> demo.lower.safe
-> route Cost 7

+ demo.fast-path
-> demo.parse -> demo.lower.fast
-> route Cost 2

LanguageRuntime.Create(enhancedPlan, ...)
-> input=41 output=42
```

This proves that changing language composition can change the concrete resolved compiler route. It does
**not** prove that lower `Cost` means faster execution or that arbitrary alternative routes are semantically
equivalent.

The prior `UTL2002 -> PreferCapabilityProvider` case remains as a small secondary proof, not the central example.

## Two different “once” boundaries

### A — language environment

```text
WistEngine.Create(...)
-> LanguageDefinition
-> LanguageCompiler
-> LanguagePlan
-> LanguageRuntime
```

Whole-language planning happens during engine creation and the environment can be reused.

### B — compiled program

```text
Compile<TDelegate>(code)
-> Runtime.Build(...)
-> durable program
-> reusable delegate
```

`Evaluate(code)` reuses the environment but still processes that source request.

## Extensibility cost model

Planning can move repeated global coordination out of the repeated execution path, but extensibility still costs:

- contracts and versioning;
- global coordination and planner complexity;
- diagnostics and observability;
- larger testing state space;
- startup/materialization;
- maintenance of expressed and hidden invariants;
- all actual compiler work that remains: parsing, lowering, optimization, code generation and execution.

Numerical performance impact remains **NEEDS MEASUREMENT** because no exact-current raw benchmark-result
artifact is bound into this deck.

## Talk timing budget

`scripts/timing_audit.py` targets:

- main talk: about **20:00**;
- source-backed demo: **1:50** inside that budget;
- interaction allowance: **0:20** inside that budget;
- at least **3:00** buffer before the 25:00 content hard stop;
- Q&A: **5:00** separate window.

If behind schedule, shorten examples on slides 3, 5 and 14. Do not cut the graph/route proof (6–7),
plan/runtime boundary (8–9), route-changing demo (10), staging boundaries (11–12), or final anchor (15).

## Run the deck locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard: `←` / `→` / space navigate, `N` notes, `T` TOC, `A` appendix, `F` fullscreen, `P` print.

## Validate

```bash
python3 scripts/check_deck.py
node --check deck.js
node --check speaker-notes-1.js
node --check speaker-notes-2.js
node --check speaker-notes-hardening.js
python3 scripts/timing_audit.py
python3 scripts/check_render.py
```

GitHub Actions additionally:

- checks out exact UniversalToolchain truth snapshot;
- compiles/runs the canonical route-changing demo;
- asserts route and runtime output anchors;
- render-checks all main/appendix slides and presenter mode;
- reopens deployed GitHub Pages after pushes to `main`.

## Rehearsal / hostile review

- [`claims.md`](claims.md) — implementation status and evidence debt;
- [`CLAIM_BOUNDARIES_40_QA.md`](CLAIM_BOUNDARIES_40_QA.md) — 40 hostile/rehearsal questions;
- [`ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md) — independent attack on the final narrative.
