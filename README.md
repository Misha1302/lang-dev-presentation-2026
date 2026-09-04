# LangDev 2026 — UniversalToolchain presentation

Conference talk:

> **Build the Language, Then Make the Abstractions Disappear: Extensible Programming on .NET**

## Narrative contract

This rebuild is intentionally **foundation-first**. A viewer who has never seen UniversalToolchain should understand the first half before encountering `Judgement`, obligations or upward semantic projection:

```text
monolithic evolution pressure
→ reusable language/compiler modules
→ language profiles / Wist dialect configuration
→ declarative WHAT, planner-resolved HOW
→ concrete compiler pipeline
→ routing / providers / ordering / policy
→ immutable LanguagePlan
→ one concrete compiler
→ whole-IR / global optimization remains possible
```

Only then does the talk enter the deeper research layer:

```text
independently authored modules also know things
→ producer × consumer coupling
→ stable semantic contracts
→ contextual Judgement + validity + evidence
→ obligations
→ representation requirements
→ multi-level lowering
→ upward semantic projection
```

The main falsifiable experiment remains:

> **add a semantic producer; change zero existing consumers**

## Claim boundaries

The deck explicitly distinguishes:

- **CURRENT UT** — repository-backed implementation evidence;
- **DESIGN SKETCH / HYPOTHETICAL EXAMPLE** — desired architecture, not shipped syntax/behavior;
- **RESEARCH HYPOTHESIS** — claims that need experiments;
- **PRIOR-ART ANALOGY** — LLVM / MLIR / build-system ideas used to explain one point, not novelty claims.

Current UniversalToolchain implementation evidence is sourced from `master@1078ddb5b9fd83b569a8ef0e590c4bec9594e1c5` where cited on slides. The conference executable demo remains fail-closed on the separately pinned snapshot `7005371d6c30175dff4b0e9f906a26218b0ee54d` used by `demo/run-demo.sh` and CI.

Important planner correction: the old failure mode “choose the cheapest conversion skeleton before mandatory pass placement” is presented as an **already repaired implementation lesson**, not as a current bug. Current UT's adopted structural planner contract applies hard feasibility/mandatory constraints before `Cost`/`Order` preference. General semantic obligations, evidence/validity and cross-level meaning remain broader design/research work.

## Deck size

The intellectual deck contains **65 main slides + 6 appendix slides**. There is intentionally no upper slide-count or timing gate in this pass; shortening is a later editorial task after the causal structure is stable.

## Runtime assets

The deck is split into small authored fragments so the HTML shell stays readable and validators remain dynamic:

- `deck-act-1.js` … `deck-act-9.js` — ordered slide HTML fragments;
- `speaker-notes-hardening.js` + `speaker-notes-research.js` — Russian presenter notes;
- `styles.css` — existing visual identity;
- `foundation.css` — primitives needed by module/dialect/pipeline/routing diagrams;
- `deck.js` / `presenter.css` — navigation, presenter mode and geometry diagnostics.

## Presenter mode

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard: `←` / `→` / space navigate, `N` presenter mode, `T` TOC, `A` appendix, `F` fullscreen, `P` print.

## Validate

```bash
python3 scripts/check_deck.py
for file in deck.js deck-act-*.js speaker-notes-*.js; do node --check "$file"; done
python3 scripts/timing_audit.py
python3 scripts/check_render.py
```

`check_render.py` discovers the split deck dynamically, geometry-checks **every main and appendix slide** at conference/stress viewports, exercises presenter mode and navigation, and captures every audience slide at both conference viewports plus representative presenter screenshots. It does not weaken overflow/collision checks.

On `main`, CI also executes the pinned UniversalToolchain pricing/parity demo and re-opens the deployed GitHub Pages build in Chromium, capturing representative production screenshots.
