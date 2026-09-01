# LangDev 2026 — UniversalToolchain presentation

Conference deck:

> **Build an Extensible Language, Run a Concrete One**

Final causal thesis:

> **Global planning selects one concrete execution environment; local compiler passes justify rewrites from explicit semantic contracts and from the capabilities that selected environment actually exposes.**

Memory anchor:

> **Resolve globally. Justify locally. Execute concretely.**

## Audience memory target

One sentence: the anchor above.

One picture: whole-language choices collapse into `LanguagePlan`; local passes then consume semantic + capability evidence.

One example: the same `foo(x)` call may or may not be reusable depending on `pure + deterministic + trusted`.

## Source-of-truth contract

Redesign audit base:

- presentation: `6cafa311480f454e6aec0634bf0e3f8478e1c4ac`;
- UniversalToolchain implementation truth: `7005371d6c30175dff4b0e9f906a26218b0ee54d`;
- research date: `2026-09-01`.

Implementation claims follow this evidence order: implementation → tests → executable behavior → architecture docs → README/comments.

The global path is:

```text
packages + LanguageDefinition
        ↓
LanguageCompiler.Compile
        ↓
immutable LanguagePlan
        ↓
LanguageRuntime.Create
        ↓
repeated execution on the selected environment
```

The local compiler path highlighted in the talk is deliberately separate:

```text
explicit semantic descriptor
+ selected-environment capabilities
        ↓
rewrite legality / specialization gate
        ↓
optimized representation
        ↓
backend validates what it receives
```

`LanguagePlan` resolves composition structure. It does **not** manufacture every semantic guarantee used by optimizers.

## LangDev 2026 conference contract

Last verified: **2026-09-01** from the official LangDev site: <https://langdevcon.org/>.

- conference: LangDev 2026;
- dates: **8–9 October 2026**;
- venue: **Meliá Costa del Sol, Torremolinos, Málaga, Spain**;
- speaker slot: **25 min talk + 5 min Q&A**;
- language: English;
- applied/tool demonstrations are encouraged;
- a public companion repository is encouraged when possible;
- preliminary/unfinished work is welcome when its status is clear.

This repository therefore optimizes for a source-backed demo, explicit maturity labels, reproducibility, and a talk target below the 25-minute hard content limit.

## Main narrative

```text
one fixed language
        ↓
a family introduces choices
        ↓
choices stop being independent
        ↓
global composition needs one owner
        ↓
LanguageCompiler resolves ambiguity / routes / runtime
        ↓
LanguagePlan describes one concrete environment
        ↓
LanguageRuntime materializes and executes it

BUT

knowing what exists
        ≠
knowing which compiler rewrite is legal

        ↓
local passes consume explicit semantic evidence
+ capabilities exposed by the selected environment
        ↓
legal rewrite / legal specialization
        ↓
concrete execution
```

Main-deck compiler concept budget: **two** concepts only:

1. semantic-contract-driven transformation legality;
2. capability-gated specialization.

SSA is notation, not a separate lesson. IR fact contracts and the bounded e-graph-style simplifier stay in appendix/Q&A.

## Truth boundaries

- planning removes unresolved composition decisions from repeated execution **≠** all runtime objects/dispatch disappear;
- structural compatibility **≠** semantic correctness proof;
- a semantic descriptor **≠** proof that its metadata is truthful;
- a declared/selected capability **≠** a performance claim;
- restricted composition **≠** sandboxing;
- no repeated global planning **≠** zero runtime overhead;
- the current `EGraphOptimizerModule` is a bounded straight-line symbolic simplifier, **not** a general equality-saturation framework;
- current IR stage contracts validate a supplied pass sequence; they do **not** automatically schedule passes.

Numerical performance claims remain **NEEDS MEASUREMENT** because this deck is not bound to an exact-current raw benchmark-result artifact.

## Talk timing budget

The canonical timing audit in `scripts/timing_audit.py` targets:

- main talk: **21:05**;
- source-backed demo: **2:00** inside that budget;
- prediction/reveal interaction allowance: **~0:50** inside that budget;
- buffer before the 25:00 hard content limit: **3:55**;
- Q&A: **5:00** official separate window.

If behind schedule, cut explanatory detail from slides 3, 8, and appendix references; do not cut the causal bridge (12), semantic prediction (13), capability path (14), or final anchor (16).

## Demo

See [`DEMO.md`](DEMO.md).

The primary demo intentionally uses a tiny synthetic package so the architecture is observable without depending on Wist syntax/semantics:

```text
UTL2002 ambiguity
→ explicit PreferCapabilityProvider
→ concrete LanguagePlan
→ LanguageRuntime.Create
→ input=41 output=42
```

The demo proves composition/runtime staging, not Wist semantics and not performance.

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

- checks out exact UniversalToolchain `7005371d6c30175dff4b0e9f906a26218b0ee54d`;
- exercises the canonical `demo/run-demo.sh`;
- asserts the UTL2002 negative case and `41 → 42` result;
- renders every main/appendix slide at required and stress viewports;
- reopens deployed GitHub Pages after pushes to `main` and checks the release marker, navigation, final thesis, and representative screenshots.
