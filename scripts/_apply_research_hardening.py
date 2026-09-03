#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one regex match, got {count}")
    return result


# ---------------------------------------------------------------------------
# index.html — keep the winning narrative, reduce one API-ish slide, and make
# the current routing boundary explicit without turning the main talk into a
# bug report.
# ---------------------------------------------------------------------------
html = read("index.html")
html = replace_once(
    html,
    "defines typed contracts and the composition protocol",
    "defines explicit artifact contracts and the composition protocol",
    "slide 5 contract wording",
)
html = replace_once(
    html,
    "type-compatible conversion graph",
    "artifact-contract-compatible conversion graph",
    "slide 7 graph wording",
)
html = replace_once(
    html,
    "automatic route search over the already-selected contribution graph; equal cost is resolved deterministically",
    "automatic route search over already-selected conversion edges; equal declared cost is resolved deterministically",
    "slide 7 current guarantee",
)
html = replace_once(
    html,
    "semantic equivalence<br/>execution-time optimality<br/>correctness merely because selection is deterministic",
    "semantic equivalence<br/>runtime optimality<br/>global optimum across conversions + passes",
    "slide 7 non-guarantees",
)
html = replace_once(
    html,
    "<span>Cost is a planning weight, not measured runtime latency.</span>",
    "<span>Current order: conversion skeleton first → selected passes second. Cost ≠ runtime latency.</span>",
    "slide 7 staged routing boundary",
)
html = replace_once(
    html,
    "<p>Whole-language planning happens once for that engine.</p>",
    "<p>Whole-language planning happens once for that engine.<br/><br/><b>Evaluate(code)</b> reuses it, but still processes each source request.</p>",
    "slide 11 Evaluate merge",
)

# Remove the redundant API-boundary slide; slide 11 now carries both reuse
# boundaries. This makes the conceptual deck smaller without losing the fact.
html = regex_once(
    html,
    r'\n<section class="slide two" data-kind="main" data-note-key="m12">.*?</section>\n',
    "\n",
    "remove former slide 12",
)

# Keep contiguous main note keys after the merge.
for old, temp in [("m13", "__M13__"), ("m14", "__M14__"), ("m15", "__M15__")]:
    html = html.replace(f'data-note-key="{old}"', f'data-note-key="{temp}"')
for temp, new in [("__M13__", "m12"), ("__M14__", "m13"), ("__M15__", "m14")]:
    html = html.replace(f'data-note-key="{temp}"', f'data-note-key="{new}"')

html = replace_once(
    html,
    "<b>Contracts</b><p>typed boundaries<br/>versioning<br/>hidden invariants</p>",
    "<b>Contracts</b><p>artifact identities<br/>versioning<br/>hidden invariants</p>",
    "cost slide contract wording",
)
html = replace_once(
    html,
    "<p>Equal-cost/tie behavior and provider preferences belong to the planning protocol and should be tested as such. Route <code>Cost</code> is not execution-time performance.</p>",
    "<p><b>Current boundary:</b> the route phase chooses the cheapest conversion skeleton first, then inserts selected same-contract passes. If a selected pass cannot fit, it reports <code>UTL2204</code>; it does not retry a more expensive pass-feasible skeleton. Route <code>Cost</code> is planner policy, not execution-time performance.</p>",
    "appendix staged-routing boundary",
)
html = replace_once(
    html,
    "semantic equivalence proof: not current<br/>automatic pass scheduling: not current<br/>general equality saturation: not current<br/>sandboxing: not current<br/>performance wins: <strong>NEEDS MEASUREMENT</strong>",
    "semantic equivalence proof: not current<br/>global conversion + pass optimization: not current<br/>all invalid compositions as planner diagnostics: not current<br/>CLR-type proof from custom contract identity: not current<br/>performance wins: <strong>NEEDS MEASUREMENT</strong>",
    "appendix claim-boundary card",
)
write("index.html", html)


# ---------------------------------------------------------------------------
# Speaker notes — preserve the architecture-first story, but make the exact
# current algorithm and verifier/error boundaries defensible in Q&A.
# ---------------------------------------------------------------------------
notes = read("speaker-notes-hardening.js")
notes = replace_once(
    notes,
    "типизированные artifact contracts",
    "explicit artifact contracts",
    "m5 contract terminology",
)
notes = replace_once(
    notes,
    "typed transformation edges",
    "artifact-contract transformation edges",
    "m6 edge terminology",
)
notes = replace_once(
    notes,
    "два structural paths не становятся семантически эквивалентными только потому, что их типы соединяются",
    "два structural paths не становятся семантически эквивалентными только потому, что их declared artifact contracts соединяются",
    "m6 semantic boundary",
)
notes = replace_once(
    notes,
    "ищет type-compatible путь от entry artifact к backend input",
    "ищет artifact-contract-compatible путь от entry artifact к backend input",
    "m7 connectivity wording",
)
notes = replace_once(
    notes,
    "После base route selected passes вставляются там, где их source/target contract совместим с текущим artifact, с учётом Before/After ordering.",
    "После base route selected same-contract passes вставляются там, где их source/target contract совместим с текущим artifact, с учётом Before/After ordering. Важная current boundary: conversion skeleton выбирается ДО вставки passes. Если выбранный pass помещается только на более дорогом conversion skeleton, текущая phase может завершиться UTL2204 и не возвращаться к route search. Поэтому это staged deterministic algorithm, а не global constraint optimizer.",
    "m7 feasibility boundary",
)
notes = replace_once(
    notes,
    "Cost — protocol planning weight. Это не profiler result, не milliseconds, не prediction of generated-code quality. Поэтому слово minimum означает только минимум по выраженной planning metric.",
    "Cost — protocol planning weight; current implementation хранит его как `int` и суммирует по route edges. Это не profiler result, не milliseconds и не prediction of generated-code quality. Поэтому слово minimum означает только минимум по этой локальной planning metric; не надо превращать Cost в центральный objective архитектуры.",
    "m7 cost boundary",
)
notes = replace_once(
    notes,
    "НЕ ПЕРЕОБЕЩАТЬ: не говорить «семантически лучший pipeline», «самый быстрый route» или «correct route» без отдельного evidence.",
    "НЕ ПЕРЕОБЕЩАТЬ: не говорить «семантически лучший pipeline», «самый быстрый route», «global optimum» или «correct route» без отдельного evidence. `ContractsConnect` сравнивает Kind + stable ValueTypeIdentity; default identity выводится из CLR type, но custom identity может быть задан явно, поэтому это не runtime proof совпадения CLR types.",
    "m7 anti-overclaim",
)
notes = replace_once(
    notes,
    "НЕ ПЕРЕОБЕЩАТЬ: immutable LanguagePlan не означает, что все runtime objects immutable или что runtime ничего не проверяет при materialization.",
    "НЕ ПЕРЕОБЕЩАТЬ: immutable LanguagePlan не означает, что все runtime objects immutable или что runtime ничего не проверяет при materialization. И не обещать, что любой invalid composition всегда превращается в обычный `LanguageBuildResult` diagnostic: часть plan invariants, включая backend/runtime input mismatch, проверяет `LanguagePlanVerifier`, который бросает `LanguagePlanVerificationException`.",
    "m8 verifier boundary",
)
notes = replace_once(
    notes,
    "ПЕРЕХОД: поэтому `Evaluate(code)` нельзя рекламировать как compile-once execute-many.",
    "СКАЗАТЬ: отсюда важная API boundary: `Evaluate(code)` reuse'ит уже выбранный environment, но каждый source request всё равно идёт через `Runtime.Run`. Для reuse конкретной построенной программы public boundary — `Compile<TDelegate>`: `Runtime.Build` создаёт durable program и reusable delegate.\n\nПЕРЕХОД: теперь можно обсуждать стоимость extensibility без магического «zero cost».",
    "m11 merge former m12 explanation",
)
notes = replace_once(
    notes,
    "НЕ ПЕРЕОБЕЩАТЬ: environment lifetime не обязательно равен process lifetime; current WistEngine также intentionally rejects overlapping public operations, поэтому не делать здесь thread-safety claim.",
    "НЕ ПЕРЕОБЕЩАТЬ: environment lifetime не обязательно равен process lifetime; current WistEngine также intentionally rejects overlapping public operations, поэтому не делать здесь thread-safety claim. Без benchmark artifact нельзя делать сравнительный вывод, насколько Evaluate или Compile быстрее handwritten implementation.",
    "m11 merged measurement boundary",
)
notes = replace_once(
    notes,
    "Нужны typed contracts и versioning",
    "Нужны explicit artifact contracts и versioning",
    "cost-note terminology",
)

# Remove the now-merged m12 note line, then renumber the remaining main notes.
notes = regex_once(
    notes,
    r'\n  "m12": ".*?",\n',
    "\n",
    "remove former m12 note",
)
for old, temp in [("m13", "__M13__"), ("m14", "__M14__"), ("m15", "__M15__")]:
    notes = notes.replace(f'  "{old}":', f'  "{temp}":')
for temp, new in [("__M13__", "m12"), ("__M14__", "m13"), ("__M15__", "m14")]:
    notes = notes.replace(f'  "{temp}":', f'  "{new}":')
write("speaker-notes-hardening.js", notes)


# ---------------------------------------------------------------------------
# Claim ledger — make all six research findings explicit and classified.
# ---------------------------------------------------------------------------
claims = read("claims.md")
claims = claims.replace("type compatibility", "artifact-contract compatibility")
claims = claims.replace("structural/type compatibility", "artifact-contract compatibility")
claims = replace_once(
    claims,
    "## NEEDS MEASUREMENT\n",
    """## CURRENT IMPLEMENTATION — bounded planner mechanics\n\nThe research findings that matter for talk truthfulness are re-checked against the pinned source:\n\n| Finding | Status | Current truth |\n| --- | --- | --- |\n| F-01 · route/pass feasibility | `CONFIRMED_CURRENT_IMPLEMENTATION` | `FindBestRoute(...)` chooses the minimum declared-cost conversion skeleton first; `InsertPasses(...)` runs afterwards. An unplaceable selected pass produces `UTL2204`; the phase does not retry a more expensive pass-feasible conversion skeleton. |\n| F-02 · `ReplaceSlot` vs dependency closure | `CONFIRMED_CURRENT_IMPLEMENTATION` | contribution/capability dependency traversal happens before `ApplySlotPolicies(...)`; current composition is staged, not a provenance-aware global solve. |\n| F-03 · mandatory contract-changing semantics | `CONFIRMED_CURRENT_IMPLEMENTATION` model boundary | contract-changing transformations are candidate conversions; the explicit mandatory mechanism in this route phase is selected same-contract passes. There is no separate “mandatory contract-changing transformation” planner primitive. |\n| F-04 · artifact identity vs CLR type | `CONFIRMED_CURRENT_IMPLEMENTATION` model boundary | connectivity compares artifact `Kind` + stable `ValueTypeIdentity`. Default `LanguageArtifactKind<T>` derives that identity from `T`, but an explicit identity can be supplied; the string identity is not itself a runtime CLR-type proof. |\n| F-05 · backend/runtime input mismatch | `CONFIRMED_CURRENT_IMPLEMENTATION` error-surface boundary | `LanguagePlanVerifier` checks a backend input against the runtime-provider input and can throw `LanguagePlanVerificationException`; not every invalid composition is normalized into a `LanguageBuildResult` diagnostic. |\n| F-06 · route cost model | `CONFIRMED_CURRENT_IMPLEMENTATION` heuristic | edge and route cost use `int`; candidate sums are ordinary integer addition and equal sums use contribution-signature tie breaking. This is planner policy, not a benchmark metric or general optimization objective. |\n\nA future planner that jointly searches conversion feasibility, mandatory transformations and broader constraints is `FUTURE_DESIGN`, not a current guarantee. No such future solver is required for the thesis of this talk.\n\n## NEEDS MEASUREMENT\n""",
    "insert bounded planner findings",
)
write("claims.md", claims)


# ---------------------------------------------------------------------------
# README — record narrative comparison, 14-slide reduction, timing and cut test.
# ---------------------------------------------------------------------------
readme = read("README.md")
readme = regex_once(
    readme,
    r"## Chosen narrative\n.*?\n## Main narrative\n",
    """## Chosen narrative\n\nFour materially different framings were re-evaluated against the current implementation:\n\n| Narrative | Strength | Failure mode | Decision |\n| --- | --- | --- | --- |\n| **Extensibility without runtime chaos** | memorable staging / hot-path question | easily turns a design principle into an unmeasured performance claim | reject as the spine |\n| **From fixed pipelines to composable languages** | compiler-native and visual | can become a taxonomy of pipeline mechanisms | keep as visual progression |\n| **Local declarations -> one executable plan** | closest to the actual ownership model | introduces `LanguagePlan` too early and feels framework-first | use as the mental model after motivation |\n| **When choices stop being independent, extensibility becomes planning** | gives a precise causal threshold and a strong handwritten baseline | needs a concrete compiler-shaped graph to avoid sounding generic | **chosen thesis** |\n\nThe final story therefore uses the fixed-pipeline -> choices -> transformation-graph progression as its visual spine, while the transferable thesis is **choices stop being independent -> global planning becomes a real responsibility**. UniversalToolchain remains the case study, not the premise.\n\n## Main narrative\n""",
    "README narrative comparison",
)
readme = replace_once(
    readme,
    "The main deck remains **15 slides**. CSE, semantic descriptors, SSA contracts, e-graph details and related\ncompiler mechanisms stay in appendix/Q&A rather than becoming a second narrative.",
    "The main deck is now **14 slides**. The former standalone `Evaluate(code)` API-boundary slide was merged into the two-reuse-boundaries slide: the distinction is still explicit, but no longer costs a separate mental model. CSE, semantic descriptors, SSA contracts, e-graph details and related compiler mechanisms stay in appendix/Q&A rather than becoming a second narrative.",
    "README slide-count reduction",
)
readme = replace_once(
    readme,
    "searches the type-compatible conversion graph;",
    "searches the artifact-contract-compatible conversion graph;",
    "README route terminology",
)
readme = replace_once(
    readme,
    "- `PlanHash` **≠** correctness/security proof.\n",
    "- `PlanHash` **≠** correctness/security proof.\n\nCurrent route planning is deliberately narrower than a general constraint optimizer: it first chooses the minimum declared-cost conversion skeleton and only then inserts selected same-contract passes. If a selected pass cannot be placed, current planning reports `UTL2204`; it does not backtrack to a more expensive conversion skeleton that might make that pass feasible. Route compatibility is based on explicit artifact contract identity, not a proof of arbitrary semantic or CLR-type equivalence.\n",
    "README current route boundary",
)
readme = replace_once(
    readme,
    "- main talk: about **20:00**;",
    "- main talk: about **19:05**;",
    "README timing total",
)
readme = replace_once(
    readme,
    "- at least **3:00** buffer before the 25:00 content hard stop;",
    "- about **5:55** buffer before the 25:00 content hard stop;",
    "README timing buffer",
)
readme = regex_once(
    readme,
    r"If behind schedule, shorten examples on slides 3, 5 and 14\. Do not cut the graph/route proof \(6–7\),\nplan/runtime boundary \(8–9\), route-changing demo \(10\), staging boundaries \(11–12\), or final anchor \(15\)\.",
    "For a ~20% shorter slot, skip the detailed reuse-boundary slide 11 and the standalone cost slide 12 (their essential caveats are already present in slides 9 and 13), and run the demo in its ~65 s fallback form. Keep the graph/route proof (6–7), plan/runtime boundary (8–9), route-changing demo (10) and final anchor (14).",
    "README cut test",
)
write("README.md", readme)


# ---------------------------------------------------------------------------
# Adversarial review — attack the newly exposed algorithmic boundary and keep
# slide numbering in sync with the smaller main deck.
# ---------------------------------------------------------------------------
adv = read("ADVERSARIAL_REVIEW.md")
adv = adv.replace("typed artifact transformation routes", "artifact-contract transformation routes")
adv = adv.replace("selected typed edges", "selected artifact-contract edges")
adv = adv.replace("main 15-slide deck", "main 14-slide deck")
adv = replace_once(
    adv,
    "slide 14 repeats the decision rule.",
    "slide 13 repeats the decision rule.",
    "adversarial counterargument slide number",
)
adv = replace_once(
    adv,
    "slide 13 keeps all performance impact under `NEEDS MEASUREMENT`.",
    "slide 12 keeps all performance impact under `NEEDS MEASUREMENT`.",
    "adversarial performance slide number",
)
adv = replace_once(
    adv,
    "Slide 14 explicitly says to choose a smaller mechanism otherwise.",
    "Slide 13 explicitly says to choose a smaller mechanism otherwise.",
    "adversarial mechanism slide number",
)
adv = replace_once(
    adv,
    "slides 11–12 separately\nshow environment reuse and compiled-program reuse.",
    "slide 11 shows both environment reuse and compiled-program reuse, including the `Evaluate` boundary, without a separate API-tour slide.",
    "adversarial lifecycle merge",
)
adv = replace_once(
    adv,
    "### Distributed contract-system failure mode\n",
    """### Staged route feasibility\n\nThe current route phase is not a global conversion+pass optimizer: it chooses a minimum-cost conversion skeleton first and inserts selected passes afterwards. A pass that fits only a more expensive skeleton can therefore cause `UTL2204` rather than route backtracking.\n\n**Mitigation:** slide 7 exposes the staged order, appendix A5 names the limitation, and the talk never claims SAT/SMT-style or globally optimal planning.\n\n### Distributed contract-system failure mode\n""",
    "adversarial staged routing check",
)
adv = regex_once(
    adv,
    r"## 5-second test for every main slide\n.*?\n## Remaining evidence debt\n",
    """## 5-second test for every main slide\n\n1. **Title:** extensibility can become planning.\n2. **Baseline:** fixed pipeline -> wire it explicitly.\n3. **Motivation:** one infrastructure can serve a family of languages.\n4. **Threshold:** coupling, not option count, creates planning.\n5. **Ownership:** local facts, one global planner, one semantic config model.\n6. **Compiler failure case:** transformations form a graph.\n7. **Selection:** route search is automatic but staged and contract-based, not a global semantic optimizer.\n8. **Answer:** LanguageDefinition -> LanguagePlan; LanguageCompiler is not source compilation.\n9. **Lifecycle:** planning/materialization happen before source build/execution.\n10. **Proof:** enabling an extension changes the resolved route.\n11. **Reuse boundaries:** environment reuse is not program reuse; Evaluate is not compile-once/execute-many.\n12. **Price:** extensibility costs contracts, coordination, testing and runtime work.\n13. **Counterargument:** use the smallest mechanism; planner can be the bigger problem.\n14. **Rule:** Declare locally. Resolve globally. Execute concretely.\n\n## Remaining evidence debt\n""",
    "adversarial 5-second test",
)
write("ADVERSARIAL_REVIEW.md", adv)


# ---------------------------------------------------------------------------
# Hostile Q&A — answer the exact implementation questions a strong reviewer
# will ask about F-01/F-04/F-05/F-06 without increasing question count.
# ---------------------------------------------------------------------------
qa = read("CLAIM_BOUNDARIES_40_QA.md")
qa = replace_once(
    qa,
    "Conceptually, the owner of the composition protocol: typed artifact contracts, IDs, feature/contribution",
    "Conceptually, the owner of the composition protocol: explicit artifact contracts, IDs, feature/contribution",
    "Q&A contract wording",
)
qa = replace_once(
    qa,
    "returns diagnostics or a `LanguagePlan`. It does not compile the user's source program.",
    "returns diagnostics or a `LanguagePlan`. It does not compile the user's source program. Most planning failures are diagnostics, but not every invalid composition is normalized that way: `LanguagePlanVerifier` can throw `LanguagePlanVerificationException` for violated plan invariants such as a backend/runtime input-contract mismatch.",
    "Q&A verifier surface",
)
qa = replace_once(
    qa,
    "Current algorithm accumulates transformation `Cost`, chooses the minimum-cost reachable structural path, and\nuses deterministic contribution-signature ordering for equal-cost alternatives.",
    "Current algorithm accumulates transformation `Cost`, chooses the minimum-cost reachable artifact-contract-compatible **conversion skeleton**, and uses deterministic contribution-signature ordering for equal-cost alternatives. It then inserts selected passes; this is staged selection, not one global optimization over conversion and pass feasibility.",
    "Q&A route algorithm",
)
qa = replace_once(
    qa,
    "A **declared planning weight** in the protocol. It lets the planner prefer one structurally valid candidate\nover another according to authored policy.",
    "A **declared integer planning weight** in the protocol. It lets the planner prefer one contract-compatible conversion candidate over another according to authored policy. Current code uses `int` costs and ordinary addition; treat this as a local heuristic/protocol value, not a durable general objective function.",
    "Q&A cost representation",
)
qa = replace_once(
    qa,
    "After the base conversion route is found, current planner inserts selected pass transformations where their\nsource/target contract connects to the current artifact. Ordering uses pass `Order` plus `Before`/`After`\nconstraints; cycles can fail planning.",
    "After the base conversion route is found, current planner inserts selected same-contract pass transformations where their source/target contract connects to the current artifact. Ordering uses pass `Order` plus `Before`/`After` constraints; cycles can fail planning. If a selected pass cannot be placed, current code reports `UTL2204`; it does **not** retry a more expensive conversion skeleton that might make the pass feasible.",
    "Q&A pass feasibility",
)
qa = replace_once(
    qa,
    "No. Matching artifact kind/value-type contracts prove only structural connectivity expressed by the protocol.\nTwo structurally compatible routes can still implement different semantics.",
    "No. Current connectivity compares artifact `Kind` plus stable `ValueTypeIdentity`. Default `LanguageArtifactKind<T>` identities are derived from `T`, but authors can provide an explicit contract identity, so connectivity is a protocol-level identity check rather than a runtime proof that arbitrary CLR types or semantics are equivalent. Two connected routes can still implement different semantics.",
    "Q&A artifact identity boundary",
)
write("CLAIM_BOUNDARIES_40_QA.md", qa)


# ---------------------------------------------------------------------------
# Timing audit — 14 slides, 19:05 target, 5:55 content buffer.
# ---------------------------------------------------------------------------
timing = read("scripts/timing_audit.py")
timing = regex_once(
    timing,
    r"SLIDE_SECONDS = \[.*?\]\n",
    """SLIDE_SECONDS = [\n    45,  # 1 title / question / anchor\n    75,  # 2 handwritten baseline\n    75,  # 3 language family / why extensibility\n    80,  # 4 coupling threshold\n    75,  # 5 ownership + canonical configuration model\n    85,  # 6 pipeline becomes a transformation graph\n    110, # 7 automatic route search + staged-algorithm truth boundaries\n    75,  # 8 LanguageCompiler naming + immutable LanguagePlan\n    75,  # 9 authoring/planning/materialization/source-build lifecycle\n    110, # 10 source-backed route-changing demo\n    100, # 11 environment reuse vs compiled-program reuse + Evaluate boundary\n    85,  # 12 full extensibility cost / measurement boundary\n    95,  # 13 strongest counterargument / when not to use planner\n    60,  # 14 final anchor\n]\n""",
    "timing slide list",
)
timing = replace_once(timing, "assert len(SLIDE_SECONDS) == 15", "assert len(SLIDE_SECONDS) == 14", "timing slide count")
timing = replace_once(timing, "19 * 60 <= total <= 21 * 60", "18 * 60 <= total <= 20 * 60", "timing target range")
timing = replace_once(timing, "assert buffer >= 3 * 60", "assert buffer >= 5 * 60", "timing buffer gate")
write("scripts/timing_audit.py", timing)


# ---------------------------------------------------------------------------
# CI contract — lock in the smaller deck and the exact architecture boundaries
# so later edits cannot silently re-introduce stronger claims.
# ---------------------------------------------------------------------------
check = read("scripts/check_deck.py")
check = replace_once(
    check,
    'adversarial = (root / "ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")\nqa =',
    'adversarial = (root / "ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")\naudit = (root / "REDESIGN_AUDIT_2026-09-03.md").read_text(encoding="utf-8")\nqa =',
    "check reads audit",
)
check = replace_once(check, 'assert len(main) == 15, f"expected 15 main slides, got {len(main)}"', 'assert len(main) == 14, f"expected 14 main slides, got {len(main)}"', "check main count")
check = replace_once(check, 'f"m{i}" for i in range(1, 16)', 'f"m{i}" for i in range(1, 15)', "check note-key range")
check = replace_once(
    check,
    '" ".join([html, js2, js3, claims, readme, adversarial, qa]),',
    '" ".join([html, js2, js3, claims, readme, adversarial, audit, qa]),',
    "check full evidence set",
)
check = replace_once(
    check,
    '"automatic route search over the already-selected contribution graph",',
    '"automatic route search over already-selected conversion edges",\n    "artifact-contract-compatible conversion graph",\n    "global optimum across conversions + passes",\n    "conversion skeleton first",',
    "check routing boundaries",
)
check = replace_once(
    check,
    'f"OK: {len(main)} main, {len(appendix)} appendix, {len(all_keys)} note keys, "',
    'f"OK: {len(main)} main, {len(appendix)} appendix, {len(all_keys)} note keys, "',
    "check final print anchor",
)
write("scripts/check_deck.py", check)


# ---------------------------------------------------------------------------
# Research/redesign record — decision-useful audit, not a second slide deck.
# ---------------------------------------------------------------------------
audit = """# LangDev 2026 redesign audit — 2026-09-03\n\nPresentation baseline: `Misha1302/lang-dev-presentation-2026@867485139ceb80fd23a38e59367f889db4ea38a1`.\n\nImplementation truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.\n\n## Final thesis\n\nA fixed compiler pipeline is often the best design when one owner knows all stages. The harder problem begins when independently authored language choices interact across dependencies, providers, ordering and artifact routes: then local declarations need one global planning authority that produces an inspectable concrete plan before runtime materialization.\n\nMemory line: **Declare locally. Resolve globally. Execute concretely.**\n\n## Narrative decision\n\n| Candidate | Clarity | Implementation fit | Main risk | Decision |\n| --- | --- | --- | --- | --- |\n| Extensibility without runtime chaos | high | medium | sounds like a performance claim before measurement | reject as spine |\n| Fixed pipeline -> composable languages | high | high | can become pipeline taxonomy | visual spine |\n| Local declarations -> executable plan | medium | very high | too abstract / plan-first | central mental model after motivation |\n| Choices stop being independent -> planning | very high | very high | needs compiler-specific proof | **chosen thesis** |\n\n## Slide-by-slide audit of the 15-slide baseline\n\n| Baseline | Intended job | Actual issue found on this audit | Decision |\n| --- | --- | --- | --- |\n| 1 | thesis / memory anchor | already sharp | KEEP |\n| 2 | strongest conventional baseline | prevents strawman | KEEP |\n| 3 | motivate language-family variability | motivation is necessary before UT terms | KEEP |\n| 4 | define configuration -> planning threshold | strongest causal slide | KEEP |\n| 5 | ownership + semantic configuration model | “typed contracts” was stronger than current identity semantics | REWRITE wording |\n| 6 | turn pipeline into compiler transformation graph | “typed edges” could imply stronger CLR guarantees | REWRITE wording |\n| 7 | explain automatic route selection | omitted the key conversion-first/pass-second feasibility boundary | REWRITE materially |\n| 8 | define LanguagePlan and naming boundary | accurate; add verifier caveat to notes | KEEP + NOTES |\n| 9 | planning/runtime/source lifecycle | accurate current boundary | KEEP |\n| 10 | executable route-changing proof | demonstrates architecture, not just DSL syntax | KEEP |\n| 11 | two amortization/reuse boundaries | already contains the durable-program distinction | MERGE with 12 |\n| 12 | Evaluate vs Compile API boundary | correct but redundant and API-tour-like as a standalone slide | DELETE / MERGE into 11 |\n| 13 | cost of extensibility | good; replace “typed boundaries” terminology | KEEP + WORDING |\n| 14 | strongest counterargument | essential applicability boundary | KEEP |\n| 15 | final decision rule | strongest transferable close | KEEP |\n\nFinal main deck: **14 slides**.\n\n## Current implementation boundaries that changed the deck\n\n- **F-01 — confirmed:** route phase chooses the minimum declared-cost conversion skeleton first, then inserts selected same-contract passes. It does not backtrack to a more expensive pass-feasible skeleton after `UTL2204`.\n- **F-02 — confirmed:** contribution/capability dependency traversal precedes slot-policy replacement. Current planner is staged, not a provenance-aware global solver.\n- **F-03 — confirmed model boundary:** current route model has candidate contract-changing conversions and selected same-contract passes; there is no separate mandatory contract-changing semantic transformation primitive.\n- **F-04 — confirmed model boundary:** artifact connectivity is `Kind + ValueTypeIdentity`; explicit identities can be supplied, so connectivity is not itself a CLR runtime-type proof.\n- **F-05 — confirmed error-surface boundary:** `LanguagePlanVerifier` can throw for plan invariant violations including backend/runtime input mismatch; not every invalid composition is a normal planning diagnostic.\n- **F-06 — confirmed heuristic:** route `Cost` is an `int` planning value with deterministic signature tie-break, not runtime latency and not a general optimization objective.\n\n## Central mental model\n\n```text\nindependent package facts + integrator choices\n                    |\n                    v\n             LanguageDefinition\n                    |\n                    v\n LanguageCompiler: staged whole-language resolution\n                    |\n                    v\n             LanguagePlan\n   selected contributions + routes + exact runtime provider\n                    |\n                    v\n        LanguageRuntime materialization\n                    |\n                    v\n      source requests follow the stored route\n```\n\nThe audience-facing compression remains: **Declare locally. Resolve globally. Execute concretely.**\n\n## Final title-only sequence and authored timing\n\n1. When Extensibility Becomes Planning — 0:45\n2. If one owner knows the pipeline, wire it by hand — 1:15\n3. A language family creates choices across compiler stages — 1:15\n4. Configuration becomes planning when choices stop being independent — 1:20\n5. Local authors declare facts; one planner owns the global decision — 1:15\n6. Local transformations turn one pipeline into a graph — 1:25\n7. The planner selects one backend route — structurally, not semantically — 1:50\n8. LanguageCompiler compiles a language definition — not source code — 1:15\n9. Planning chooses the language; later stages process actual source — 1:15\n10. Changing language composition changes the resolved route — 1:50\n11. There are two different once boundaries — 1:40\n12. Extensibility still has a price — 1:25\n13. Sometimes the planner is the bigger problem — 1:35\n14. Declare locally. Resolve globally. Execute concretely. — 1:00\n\nTotal authored main-talk budget: **19:05**. Official 25-minute content hard stop remains separate from the 5-minute Q&A window.\n\n## 20% cut test\n\nFor a ~15:15 emergency version, skip slides 11 and 12: slide 9 already establishes the runtime boundary, and slide 13 already carries the “planner has a price” counterargument. Run the route-changing demo in ~65 seconds. The causal thesis remains intact.\n\n## Remaining uncertainty\n\n### NEEDS_MEASUREMENT\n\nPlanning latency/allocations, runtime creation cost, cold execution, steady-state overhead, graph-scaling behavior and amortization break-even. No numerical performance claim is allowed without an exact-current benchmark artifact.\n\n### FUTURE_DESIGN\n\nA planner that jointly optimizes conversion choice, mandatory transformations and broader constraints could remove some staged-feasibility limitations. That is a possible architectural direction, not current behavior and not required for the talk thesis.\n\n### NEEDS_VERIFICATION\n\nNo additional load-bearing claim is intentionally left unverified at the pinned source snapshot. Conference/project logistics can still change independently of the source code.\n"""
write("REDESIGN_AUDIT_2026-09-03.md", audit)

print("Applied LangDev presentation research hardening: 14-slide main deck + current-planner truth boundaries.")
