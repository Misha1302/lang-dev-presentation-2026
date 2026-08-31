# LangDev 2026 — UniversalToolchain presentation

Conference deck:

> **Build an Extensible Language, Run a Concrete One**

Opening thesis:

> **Resolve composition before execution — keep open choices out of the hot path.**

Central architecture claim:

> Extensions describe possibilities. Planning resolves global composition choices into one concrete `LanguagePlan`. Runtime executes that resolved plan instead of reopening those decisions.

Performance consequence, deliberately scoped:

> Extensibility does not inherently require global composition decisions to remain dynamic during repeated execution.

The deck does **not** claim that extensibility is free, that all runtime abstractions/dispatch disappear, that planning guarantees JIT/AOT devirtualization, or that UniversalToolchain/Wist is generally as fast as or faster than handwritten C#.

## Source-of-truth contract

Implementation claims are pinned to `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

The current public path is:

```text
packages + definition
        ↓
LanguageCompiler.Compile
        ↓
immutable LanguagePlan
        ↓
LanguageRuntime.Create
        ↓
repeated execution on the selected plan/session
```

`LanguageRuntime.Create` performs exact validation/materialization. That is not a second global provider/route planning pass. `LanguageRuntime.Run` validates the request against the already-selected plan and dispatches to the created session.

## Performance evidence boundary

The talk separates four cost boundaries:

1. planning;
2. runtime creation;
3. first execution;
4. steady-state execution.

Current UniversalToolchain source has separate benchmark surfaces for architecture-boundary setup/planning, formula compilation, convenience `Evaluate`, and prepared hot invocation. The benchmark methodology explicitly forbids mixing those workloads.

No raw exact-current-revision result bundle with commit/environment/config/raw BenchmarkDotNet artifacts is bound into this presentation, so numerical values remain **NEEDS MEASUREMENT**. The amortization equation in the appendix is a conceptual cost model, not benchmark evidence.

## Run locally

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

GitHub Actions additionally checks out the exact UniversalToolchain truth snapshot and runs `demo/UniversalToolchainDemo.csproj` through project references.

## Demo

See [`DEMO.md`](DEMO.md). The live path proves two source-backed boundaries: a real planning ambiguity (`UTL2002`) resolved by `PreferCapabilityProvider`, then a real authored package compiled to `LanguagePlan`, materialized by `LanguageRuntime.Create`, and executed as `41 → 42`.

## Narrative map

```text
handwritten pipeline works
        ↓
independent extensions create global composition decisions
        ↓
planner owns those decisions
        ↓
LanguagePlan collapses open choices into concrete data
        ↓
runtime validates/materializes and executes the resolved language
        ↓
extensibility need not mean dynamic global composition in the hot path
```
