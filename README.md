# LangDev 2026 — UniversalToolchain presentation

Conference talk:

> **Build the Language, Then Make the Abstractions Disappear: Extensible Programming on .NET**

Architecture memory:

> **Feasibility before preference.**
>
> **Resolve globally only what correctness cannot own locally.**

## Audience memory target

The talk now starts from a real language/compiler story rather than from planner terminology:

```text
restricted pricing language
        ↓
Wist source → Bytecode → AIR → interpreter / CIL
        ↓
real parity boundary: external bindings + local shadowing
        ↓
who owns whole-compiler correctness?
        ↓
current UT staging: LanguageDefinition → LanguageCompiler → LanguagePlan → LanguageRuntime
        ↓
current limitation: structural route preference can precede semantic feasibility
        ↓
proposed rule: hard obligations → feasible implementations → preference → concrete plan
```

UniversalToolchain is the current implementation case study, not the reference architecture.

## Truth snapshot

All current implementation claims in the deck are pinned to:

- `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Evidence order for current implementation claims:

```text
implementation → tests → executable behavior → architecture docs → README/comments
```

## Why the narrative changed

The previous version had a strong architecture thesis but introduced the proposed model before the audience had seen the concrete `.NET` language/compiler failure it was meant to solve. It also drifted away from the accepted LangDev abstract.

The repaired story keeps **Feasibility before preference**, but makes the evidence order concrete-first:

1. explicit pipeline is the baseline;
2. show the shipped `pricing-restricted` Wist dialect;
3. show the Wist `Bytecode → AIR → interpreter/CIL` execution path;
4. show the tested external-binding/local-shadowing parity boundary;
5. derive the cross-owner correctness problem;
6. show what current UT already gets right: staging and a concrete `LanguagePlan`;
7. expose the current structural-route limitation;
8. only then introduce the stronger obligation-first model;
9. close with applicability boundaries and the freeze-at-runtime principle.

## Concrete source-backed evidence

### Restricted pricing dialect

Current Wist ships `UniversalToolchain/Dialects/examples/wist/pricing-restricted`.

Its documented example evaluates:

```text
100.0 * 0.9 + 5.0
```

as `95` and supports both `interpreter` and `cil` backends while intentionally excluding unrelated language capabilities.

### Wist lowering path

The current architecture walkthrough documents:

```text
source text
→ AST
→ module-oriented Bytecode
→ AIR
→ backend-neutral optimization / specialization
→ interpreter or CIL backend
```

Bytecode/AIR are Wist implementation artifacts; the generic language SDK does not require them.

### Cross-backend parity boundary

`InterpreterBindingsParityTests` covers:

- external bindings;
- local variables mixed with externals;
- reordered declared bindings;
- local shadowing of external names;
- nested scopes;
- deterministic interpreter/CIL parity.

This is the concrete correctness problem behind the architecture: a structurally reachable backend is not enough if different implementations change language meaning.

## Current UT staging

Current UT already separates:

```text
LanguageDefinition
→ LanguageCompiler
→ LanguagePlan
→ LanguageRuntime.Create
→ Run / Build
```

`LanguagePlan` currently contains the original definition, resolved features/contributions, runtime provider, backend routes, `PlanHash` and `Summary`.

The deck does **not** claim that current `LanguagePlan` already stores explicit semantic obligations, selection provenance, or rejected-candidate explanations.

## Current route-planner limitation

Current `LanguageArtifactRoutePhase`:

1. collects contract-changing conversion edges from selected contributions;
2. calls `FindBestRoute(...)` and chooses minimum sum of declared integer `Cost`;
3. only after that calls `InsertPasses(...)` for selected same-contract passes;
4. reports `UTL2204` if a selected pass cannot be placed;
5. does not backtrack to a different conversion skeleton that could satisfy that pass.

Therefore:

- artifact-contract reachability is not semantic admissibility;
- route `Cost` is preference policy, not latency or correctness;
- deterministic tie-break gives reproducibility, not semantic equivalence;
- current whole-language routing does not generally model properties such as target legality or SSA state.

## Proposed general model

The proposed model is intentionally stronger than current UT:

```text
requested language
→ hard obligations
→ candidate implementation requires / ensures
→ feasible compiler plans
→ explicit preference among feasible plans
→ one concrete plan
```

The planner owns global implementation resolution, not the meaning of the language.

Local mechanisms remain preferable where they already own the decision:

- explicit wiring for one known compiler;
- builders for configuration;
- DI for provider/object wiring;
- pass managers for a known pass set and invalidation model;
- MLIR-style legalization for local IR legality;
- whole-language planning only for expressed cross-owner hard constraints.

## Performance claim boundary

The repository contains a dedicated BenchmarkDotNet measurement project with separate suites for prepared hot-path execution, convenience `Evaluate`, and compilation.

This deck intentionally publishes **no numerical performance result** unless an exact raw benchmark artifact is bound to the pinned source/environment. In particular, the architecture argument does not depend on a speedup claim.

Allowed on-stage wording:

> Moving whole-language composition before repeated execution changes the lifecycle. It does not make extensibility free.

## Demo

See [`DEMO.md`](DEMO.md).

The canonical conference proof is now the same concrete story as the deck:

1. inspect the shipped `pricing-restricted` dialect;
2. execute the same program through `interpreter` and `cil` and observe `95`;
3. run the targeted interpreter/CIL shadowing parity regression test.

The old synthetic `Cost 7 → Cost 2` route demo remains implementation evidence in repository history, but is no longer the main conference proof because it demonstrates route preference rather than language correctness.

## Talk timing budget

`scripts/timing_audit.py` targets roughly 19–20 minutes of authored content plus room before the 25-minute LangDev hard content limit and the separate 5-minute Q&A.

The highest-value sequence is slides 3–9: concrete dialect, actual Wist pipeline, parity boundary, ownership, current staging, current hole, then the general architecture rule.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Keyboard: `←` / `→` / space navigate, `N` presenter notes, `T` TOC, `A` appendix, `F` fullscreen, `P` print.

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

Presentation CI additionally checks out the exact UniversalToolchain truth snapshot and runs the source-backed pricing/parity demo.