# LangDev 2026 — Extensible Programming on .NET

Conference talk:

> **Build an extensible language. Resolve it into one compiler.**

The presentation is about a general compiler architecture question, not about UniversalToolchain internals:

> How can independently authored language/compiler components compose into one concrete compiler, keep extensibility off the runtime hot path, retain local and non-local optimization opportunities, and preserve the semantic information later optimizers still need as representations are lowered?

UniversalToolchain/Wist is used only as an **implementation witness** for mechanisms that exist today.

## Main narrative

The rebuilt main deck is **48 slides** in eleven causal acts:

1. Why extensibility — and when a monolith is better.
2. Reusable capabilities + declarative configuration → one resolved compiler plan.
3. Planning as a correctness problem: representation requirements, route feasibility and the current UT planner regression.
4. Extensibility is primarily authoring-time; it does not have to remain on the hot path.
5. Local/peephole optimization and the concrete Wist AIR 3→1 rewrite.
6. The correct performance-evidence boundary: setup vs prepared steady-state execution.
7. Why local optimization is insufficient: the array-bounds proof example.
8. A second semantic domain: write semantics, orthogonal effects and operation-centric queries.
9. Independent semantic producers plus meaning/validity across lowering.
10. LLVM/MLIR prior art, the strongest local-mechanism alternative and a falsifiable experiment.
11. What is demonstrated vs what remains the research bet.

The appendix contains **8 slides** for UT-specific terminology/configuration/planner staging, bounded reflection, parity evidence, validity/trust, the lower-level planner lesson and numerical benchmark publication requirements.

## Why the 48-slide version

The 40-slide reduction was too aggressive in two places. This version restores both load-bearing arguments:

- planner causality is back in the main story: optimization/mandatory-pass requirements can constrain representation routes, a cheaper reachable route may be inadmissible, and the historical UT failure makes **feasibility before preference** an evidence-backed lesson rather than a slogan;
- one bounds-check example is no longer carrying the entire semantic thesis: `Write(place, value)` supplies a second independent domain and shows why volatility, atomicity, ordering, visibility, GC-barrier and transaction concerns do not fit one inheritance lattice.

Validity is also reintroduced through a concrete failure mode — typed facts can become stale after transformations — while broader research questions remain compact rather than expanding back into a UT tutorial.

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

- `deck-main.js` — 48-slide main story;
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

`check_deck.py` reconstructs the actual script load order from `index.html`, verifies 48 main + 8 appendix keys, enforces planner/semantic/lowering causal anchors, rejects conference-facing UT commit pins, and proves that exactly one `speaker-script-*.js` owner supplies complete spoken text.

`check_render.py` geometry-checks every audience and presenter slide at conference/stress viewports, captures every audience slide at three viewports plus every presenter slide at 1366×768, and keeps navigation/presenter synchronization checks.

On `main`, `check_production.py` waits for GitHub Pages, compares exact hashes for the built deck **including `speaker-script-canonical.js`**, and exercises both audience and presenter states. A stale deployed speaker script therefore fails production validation.

Presentation CI also checks the current UT `master` witness: pricing/parity demo, the typed-intrinsic local rewrite tests, route-order feasibility, and the benchmark-methodology boundary. It does not run a smoke benchmark and call it performance evidence.
