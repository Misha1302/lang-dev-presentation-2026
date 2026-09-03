# LangDev 2026 — UniversalToolchain presentation

Conference talk:

> **Build the Language, Then Make the Abstractions Disappear: Extensible Programming on .NET**

Architecture memory:

> **Compose knowledge. Discharge obligations. Lower safely. Keep semantics queryable.**

## Current narrative

The deck is organized around **open-world semantic composition under transformation**.
`LanguagePlan` is deliberately not presented as the central invention; it is a useful staged/frozen output of a stronger composition model.

```text
independently authored producers / consumers
        ↓
typed contextual judgements + evidence
        ↓
obligations
        ↓
representation requirements
        ↓
lowering / legalization / backend capabilities
        ↓
correctness-first planning
        ↓
one concrete execution plan
```

The central falsifiable experiment is:

> **add a semantic producer; change zero existing consumers**

The deck separates lowering from semantic refinement and introduces **upward semantic projection**: lower-level IR may keep selected higher-level meaning queryable without reconstructing an older representation.

## Story arc

1. explicit wiring is the strongest baseline for a closed compiler;
2. open ecosystems create producer × consumer integration pressure;
3. a stable semantic contract lets independently authored producers discharge obligations used by unchanged consumers;
4. raw facts are insufficient without context, revision/validity and evidence;
5. `Writable`/volatile/atomicity shows why semantics should not be frozen into inheritance hierarchies;
6. small anchors (`Value`, `Place`, `Operation`, `Region`, `Type`, `Symbol`) carry identity while orthogonal schemas carry semantics;
7. judgements produce obligations, obligations constrain representation and lowering;
8. lowering makes representations more concrete but need not erase higher-level meaning;
9. upward semantic projection answers higher-level queries without universal inverse lowering;
10. different subproblems keep different engines; one contract does not imply one mega-solver;
11. correctness/feasibility precedes preference and `LanguagePlan` becomes a staging artifact;
12. prior art supplies the pieces; the integration question remains a research hypothesis;
13. the hypothesis is tested by producer independence, precision, invalidation/projection cost and explainability.

## Claim boundary

The presentation does **not** claim that `Fact<T>`, semantic queries, interfaces, fixed points, legalization, cost-based planning, proof certificates, or composable language extensions are individually novel.

The defensible research question is whether typed, evidence-bearing, revision-aware semantic contracts can span independently authored analyses, transformations, representation levels and backends while reducing pairwise coupling.

UniversalToolchain is the implementation case study and staging prototype, not proof that the full proposed semantic substrate already exists.

Current implementation claims remain pinned to:

- `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Deck size and timing

The intellectual deck contains **27 main slides + 5 appendix slides**.
The rebuild intentionally does **not** enforce the earlier 25-minute/small-deck constraint. The current authored rehearsal estimate is about **31:45**; cutting is a later editorial pass, after the intellectual structure is stable.

## Presenter mode

Run locally:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard: `←` / `→` / space navigate, `N` presenter mode, `T` TOC, `A` appendix, `F` fullscreen, `P` print.

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

`check_render.py` exercises every main/appendix slide at conference and stress viewports, captures audience screenshots, checks presenter mode and navigation, and fails on detected overflow/collision.

The push CI also keeps the existing source-backed UniversalToolchain demo and re-opens the deployed GitHub Pages build in Chromium.
