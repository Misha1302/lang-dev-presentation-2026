# LangDev 2026 — Extensible Programming on .NET

Conference talk:

> **Author many language pieces. Resolve one compiler. Keep the meaning.**

The presentation is about a general compiler-architecture question, not about UniversalToolchain internals:

> How can independently authored language capabilities be reused and recombined into several concrete language profiles, resolved into one feasible compiler, optimized after composition machinery disappears, and still share the semantic knowledge required by later non-local optimizations?

UniversalToolchain/Wist is used only as an **implementation witness** for bounded mechanisms that exist today.

## Main narrative

The main deck is **52 slides**. The story is deliberately one causal chain rather than separate “dialect”, “planner”, and “optimization” sections:

1. A monolithic compiler remains the baseline; extensibility earns its cost only when reuse, variation or independent authorship matters.
2. A **capability / extension** is a reusable authored compiler slice. A **dialect / language profile** is a concrete declarative composition of many such pieces. They are different entities.
3. One ecosystem can produce multiple dialects. Extensibility therefore means both **adding new capabilities** and **recombining existing capabilities**.
4. Independent authors should not need a private handshake. A dialect declares **WHAT** language is wanted; composition/planning resolves **HOW** to assemble it.
5. MLIR is introduced here as strong prior art: IR dialects, interfaces, legality/conversion, pass infrastructure and the Transform dialect already make representations and transformations highly extensible. That success exposes, rather than erases, the next research question: who resolves one coherent compiler from the requested capabilities, providers, conflicts, representation routes, ordering and backend?
6. The resulting compiler plan must be feasible before preferences rank alternatives. Optimization requirements can constrain representation routes, and the historical UT planner failure makes **FEASIBILITY FIRST. PREFERENCE SECOND.** an evidence-backed rule.
7. Freeze open-world composition into one concrete plan so extensibility machinery can stay off the repeated runtime path.
8. Local optimization can erase modular representation machinery; Wist AIR supplies a concrete 3→1 deabstraction witness.
9. Global/non-local optimization needs shared facts. Range + extent knowledge motivates `SafeIndex(a,i)` and possible bounds-check elimination.
10. The private-handshake problem returns at the semantic level: independently authored analyses and consumers need a stable way to exchange semantic knowledge without private producer-consumer APIs.
11. `Write(place, value)` supplies a second semantic domain with volatility, atomicity, ordering, visibility, GC-barrier and transaction concerns. Operation-centric queries avoid encoding their cross-product as one inheritance lattice.
12. Typed facts can become stale. `Judgement` models contextual valid knowledge; `Obligation` models what must hold before a transformation is legal.
13. Representation and knowledge are separate axes. There is no universal inverse lowering, so later passes may need meaning preserved, exposed on the current representation, or re-analysed.
14. LLVM and MLIR are prior art; local interfaces/adapters are the strongest alternative; the shared semantic-contract hypothesis must earn its complexity in a falsifiable producer experiment.
15. The final synthesis separates **IMPLEMENTED WITNESS**, **GENERAL DESIGN**, and **RESEARCH HYPOTHESIS**, then reconnects the three themes as **AUTHOR → RESOLVE → OPTIMIZE**.

The appendix remains **8 slides** for UT-specific terminology/configuration/planner staging, bounded reflection, parity evidence, validity/trust, a falsifiable “Why not just MLIR?” Q&A, and numerical benchmark publication requirements.

## MLIR boundary

MLIR is treated as **VERIFIED PRIOR ART**, not as a competitor or strawman. The deck explicitly distinguishes this talk's `dialect` (language profile) from an MLIR IR dialect.

The core scope distinction is:

> **MLIR makes compiler representations extensible. We are asking how compiler composition itself becomes resolvable.**

That does not mean MLIR cannot host such policy in user code. The research move is to make whole-composition resolution a first-class architectural object. A future `LanguagePlan` could select an MLIR-based subsystem and lower onward to LLVM or a specialized backend; current UT does not implement that provider integration. If MLIR plus local adapters solves the same problem with less machinery, the extra layer is not justified.

## Central synthesis

> **Extensibility should disappear where it is machinery — and survive where it is meaning.**

- **AUTHOR** — independent capabilities can be added and recombined into multiple dialects.
- **RESOLVE** — a declarative WHAT becomes one feasible concrete compiler HOW.
- **OPTIMIZE** — composition and representation machinery can be erased while useful semantic knowledge is preserved, re-exposed or re-derived.

This is not a zero-overhead claim. Composition, compiler construction and compilation may cost more. Equal-or-better-than-C# performance is not guaranteed.

## Claim-status boundary

The deck uses four interpretation categories:

- **VERIFIED PRIOR ART** — externally verified mechanisms from primary/upstream sources;
- **IMPLEMENTED WITNESS** — current UT/Wist demonstrates the bounded mechanism/example;
- **GENERAL DESIGN** — architecture argued by the talk;
- **RESEARCH HYPOTHESIS** — falsifiable architecture not yet established by the implementation.

UniversalToolchain remains evidence for the general argument, not its ontology. Wist-specific `module / Feature / Contribution` terminology and bounded-reflection details stay in the appendix.

## Performance evidence

The main deck contains no numerical C#↔Wist performance ratio. Current UT has a BenchmarkDotNet hot-path suite with a prepared C# delegate baseline and a Wist compiled delegate, and it keeps composition/compilation/setup in separate suites. A numerical conference claim remains withheld until a current reviewed raw Release BenchmarkDotNet artifact, environment metadata, source identity and correctness/parity precheck are preserved and reviewed.

See `claims.md` for the exact publication boundary.

## Runtime assets

- `deck-main.js` — 52-slide main story;
- `deck-appendix.js` — 8-slide appendix;
- `speaker-script-canonical.js` — the single canonical stage-ready English speaker script for every slide;
- `deck.js` — navigation, presenter mode and geometry/runtime diagnostics;
- `presenter.css` — speech-only presenter teleprompter layout;
- `styles.css`, `foundation.css`, `visual-balance.css` — visual system.

Presenter mode does not load or merge legacy structured notes. The panel renders only text from `speaker-script-canonical.js`.

## UniversalToolchain evidence policy

Conference-facing UT source links use moving `master` paths. The presentation architecture is not tied to a UT commit hash.

Normal CI checks current `master` intentionally and runs focused witness checks. Exact source/environment identity belongs in raw benchmark evidence when numerical reproducibility requires it; it is not a deck-wide truth snapshot.

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

`check_deck.py` reconstructs the actual script load order, verifies 52 main + 8 appendix keys, enforces the causal dialect/extensibility → MLIR scope bridge → planner → local/global → semantic-contract → lowering → synthesis story, keeps planner/Write blocks in main, rejects conference-facing UT commit pins, and proves that exactly one canonical speaker-script owner supplies complete spoken text.

`timing_audit.py` verifies the main canonical script remains inside the 25–27 minute rehearsal envelope at 130 wpm.

`check_render.py` geometry-checks every audience and presenter slide at conference/stress viewports, captures every audience slide at three viewports plus every presenter slide at 1366×768, and keeps navigation/presenter synchronization checks.

On `main`, `check_production.py` waits for GitHub Pages, compares exact hashes for the built deck including `speaker-script-canonical.js`, and exercises representative audience and presenter states. A stale deployed speaker script therefore fails production validation.

Presentation CI also checks the current UT `master` witness: pricing/parity demo, typed-intrinsic local rewrite tests, route-order feasibility, and benchmark-methodology boundary. It does not turn a smoke benchmark or remembered number into performance evidence.
