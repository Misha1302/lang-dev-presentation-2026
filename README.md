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

> When independently owned choices start interacting across compiler stages, resolve the global choices before execution, freeze the result as data, and make runtime materialize exactly that decision.

One picture:

```text
local extension facts + integrator choices
                ↓
         LanguageCompiler
                ↓
      immutable LanguagePlan
                ↓
      one concrete backend route
                ↓
         LanguageRuntime
                ↓
      repeated concrete execution
```

## Source-of-truth contract

Current presentation baseline for this redesign: `cf7e5cd26dec61cd7818006795502d995ffac617`.

UniversalToolchain implementation truth remains pinned to:

- `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Implementation claims follow this evidence order: implementation → tests → executable behavior → architecture docs → README/comments.

Load-bearing current claims:

- `LanguageCompiler` owns whole-language resolution;
- artifact transformations form structurally typed candidate routes;
- route selection is deterministic by expressed planning protocol/cost;
- `LanguagePlan` records resolved features, contributions, runtime provider and routes;
- `LanguageRuntime.Create` verifies/materializes the selected plan rather than running a second global planner;
- `WistEngine.Create` and `Compile<TDelegate>` are different staging/reuse boundaries.

## Main narrative

```text
one stable pipeline
    ↓
wire it by hand

language family
    ↓
independent choices
    ↓
configuration is still enough

choices become coupled across stages
    ↓
local transformations form a graph
    ↓
no local extension owns the whole route
    ↓
LanguageCompiler resolves one concrete language
    ↓
LanguagePlan records one concrete route/environment
    ↓
LanguageRuntime materializes exactly that plan
    ↓
repeated execution does not rediscover global composition
```

The main deck is intentionally **15 slides**. CSE, semantic descriptors, capability-gated intrinsics, SSA contracts, the bounded EGraph module, PlanFuzz, security details and deeper performance discussion stay in appendix/Q&A.

## Truth boundaries

- deterministic route selection **≠** semantic correctness;
- structural/type compatibility **≠** semantic equivalence;
- route `Cost` **≠** runtime latency;
- `PlanHash` **≠** correctness/security proof;
- no repeated global planning **≠** zero runtime overhead;
- reusing a language environment **≠** reusing a compiled program;
- `Evaluate(code)` **≠** an already compiled reusable delegate;
- restricted composition **≠** sandboxing.

Numerical performance claims remain **NEEDS MEASUREMENT** because no exact-current raw benchmark-result artifact is bound into this deck.

## Demo

See [`DEMO.md`](DEMO.md).

The current safe, source-backed demo remains:

```text
UTL2002 ambiguity
→ explicit PreferCapabilityProvider
→ concrete LanguagePlan + route
→ LanguageRuntime.Create
→ input=41 output=42
```

It proves planner diagnostics, an explicit whole-language policy, concrete plan/runtime materialization and actual execution. It does **not** prove Wist semantics, arbitrary route semantic equivalence or performance.

A stronger route-changing demo is a future design until it is implemented and CI-backed; it is not presented as current behavior.

## Talk timing budget

`scripts/timing_audit.py` targets:

- main talk: **20:00**;
- source-backed demo: **1:50** inside that budget;
- interaction allowance: **0:20** inside that budget;
- buffer before the 25:00 content limit: **5:00**;
- Q&A: **5:00** separate window.

If behind schedule, shorten examples on slides 3, 5 and 14. Do not cut the graph/route proof (6–7), plan/runtime boundary (8–9), demo (10) or final anchor (15).

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

GitHub Actions additionally checks out the exact UniversalToolchain pin, runs the canonical demo, render-checks all main/appendix slides and reopens the deployed GitHub Pages after pushes to `main`.
