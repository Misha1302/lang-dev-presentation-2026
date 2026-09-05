# LangDev 2026 — Extensible Programming on .NET

Conference talk:

> **Build an extensible language. Resolve it into one compiler.**

The presentation is about a general compiler architecture question, not about UniversalToolchain internals:

> How can independently authored language/compiler components compose into one concrete compiler, keep extensibility off the runtime hot path, retain local and non-local optimization opportunities, and preserve the semantic information later optimizers still need as representations are lowered?

UniversalToolchain/Wist is used only as an **implementation witness** for mechanisms that exist today.

## Main narrative

The rebuilt main deck is **40 slides** in ten causal acts:

1. Why extensibility — and when a monolith is better.
2. Reusable capabilities + declarative configuration → one resolved compiler plan.
3. Extensibility is primarily authoring-time; it does not have to remain on the hot path.
4. Local/peephole optimization and the concrete Wist AIR 3→1 rewrite.
5. The correct performance-evidence boundary: setup vs prepared steady-state execution.
6. Why local optimization is insufficient: one running array-bounds example.
7. Independent semantic producers and stable typed query contracts.
8. Lowering as a semantic-information problem: preserve, expose or re-derive useful facts.
9. LLVM/MLIR prior art, strongest alternative and a falsifiable experiment.
10. What is demonstrated vs what remains the research bet.

The appendix contains **8 slides** for UT-specific terminology/configuration/planner details, bounded reflection, parity evidence, validity/trust, the historical planner lesson and numerical benchmark publication requirements.

## Central claims

The deck distinguishes only the status categories needed to interpret a claim:

- **IMPLEMENTED WITNESS** — current UT/Wist demonstrates the bounded mechanism/example;
- **GENERAL DESIGN** — architecture argued by the talk;
- **RESEARCH HYPOTHESIS** — not yet established and intended to be falsified or supported experimentally.

A central phrase is:

> **Extensibility does not have to cost runtime performance.**

That is deliberately not a claim that extensibility is free. Composition and compilation may cost more, and equal-or-better-than-C# performance is not guaranteed.

## Performance evidence

The main deck contains no numerical C#↔Wist performance ratio. Current UT has a BenchmarkDotNet hot-path suite with a prepared C# delegate baseline and a Wist compiled delegate, and it keeps composition/compilation/setup in separate suites. But a current reviewed raw Release artifact is not checked into this presentation repository, so numbers are withheld rather than reconstructed from memory or smoke jobs.

See `claims.md` for the exact publication boundary.

## Runtime assets

- `deck-main.js` — 40-slide main story;
- `deck-appendix.js` — 8-slide appendix;
- `speaker-script-canonical.js` — the single canonical stage-ready English speaker script for every slide;
- `deck.js` — navigation, presenter mode and geometry/runtime diagnostics;
- `presenter.css` — speech-only presenter teleprompter layout;
- `styles.css`, `foundation.css`, `visual-balance.css` — visual system.

Presenter mode does not load or merge legacy structured notes. The panel renders only text from `speaker-script-canonical.js`.

## UniversalToolchain evidence policy

Conference-facing UT source links use moving `master` paths. The presentation architecture is not tied to a UT commit hash.

Normal CI checks out current `master` intentionally and runs focused witness checks. Exact source/environment identity belongs in raw benchmark evidence when numerical reproducibility requires it; it is not a deck-wide truth snapshot.

## Presenter mode

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard: `←` / `→` / space navigate, `N` presenter mode, `T` TOC, `A` appendix, `F` fullscreen, `P` print.

## Validate

```bash
python3 scripts/check_deck.py
for file in deck.js deck-*.js speaker-script-*.js; do node --check "$file"; done
python3 scripts/timing_audit.py
python3 scripts/check_render.py
```

`check_deck.py` reconstructs the actual script load order from `index.html`, verifies 40 main + 8 appendix keys, enforces the causal narrative anchors, rejects conference-facing UT commit pins, and proves that exactly one `speaker-script-*.js` owner supplies complete spoken text.

`check_render.py` geometry-checks every audience and presenter slide at conference/stress viewports, captures every audience slide at three viewports plus every presenter slide at 1366×768, and keeps navigation/presenter synchronization checks.

On `main`, `check_production.py` waits for GitHub Pages, compares exact hashes for the built deck **including `speaker-script-canonical.js`**, and exercises both audience and presenter states. A stale deployed speaker script therefore fails production validation.

Presentation CI also checks the current UT `master` witness: pricing/parity demo, the typed-intrinsic local rewrite tests, the route-order regression retained in the appendix, and the benchmark-methodology boundary. It does not run a smoke benchmark and call it performance evidence.
