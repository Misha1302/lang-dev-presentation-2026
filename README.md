# LangDev 2026 — UniversalToolchain presentation

Conference deck for the accepted talk title:

> Build the Language, Then Make the Abstractions Disappear

Central thesis:

> Modules keep local knowledge; the planner owns global composition decisions. Runtime materializes and executes the resolved plan rather than re-solving global composition.

## Source-of-truth contract

The implementation claims in the deck are pinned to `Misha1302/UniversalToolchain@36206b66548fec365be6e03381ba44d50c2cafe5`. The evidence path is the current public API: `LanguageCompiler.Compile(...)` produces an immutable `LanguagePlan`; `LanguageRuntime.Create(...)` / `LanguageBuildRuntime` materialize and execute that plan. The talk does **not** claim universal zero-cost extensibility or a measured speedup.

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
python3 scripts/check_render.py
python3 scripts/timing_audit.py
```

GitHub Actions additionally checks out the exact UniversalToolchain truth snapshot and runs `demo/UniversalToolchainDemo.csproj` through project references.

## Demo

See [`DEMO.md`](DEMO.md). The live path deliberately proves two boundaries: a real planning ambiguity (`UTL2002`) resolved by `PreferCapabilityProvider`, then a real authored package compiled to `LanguagePlan`, materialized by `LanguageRuntime.Create`, and executed as `41 → 42`.
