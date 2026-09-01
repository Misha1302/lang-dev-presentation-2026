# Adversarial review — balanced causal narrative

Truth snapshot: `UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`. Review date: `2026-09-01`.

## Null-hypothesis verdict

**Baseline:** keep the 16-slide planner/runtime deck.

That baseline already had a strong first ten slides, but after the staging thesis was demonstrated it spent five slides repeating boundaries:

```text
takeaway
→ what disappears
→ performance decomposition
→ correctness boundary
→ decision rule
```

The tail was safe but increasingly defensive. It also left a source mismatch: main slide 11 described a real Wist `MinimalArithmetic` demo while `demo/Program.cs` executed synthetic `Demo.Ambiguity` + `Demo.Runtime`.

**Verdict:** keep the strongest planner/runtime spine, fix the demo truth, and spend the recovered conceptual budget on exactly two compiler ideas that are connected to the selected environment.

## One-sentence causal test

The talk can be described without “Part 1 / Part 2”:

> Whole-language planning selects one concrete environment; local compiler passes then use explicit semantic and selected-capability evidence to decide which rewrites are legal before that environment executes.

If rehearsal cannot preserve this sentence, cut compiler detail rather than adding more mechanisms.

## Why the redesign is stronger

- keeps 16 main slides;
- keeps the source-backed UTL2002 / plan / runtime demonstration;
- replaces a boundary-heavy tail instead of growing the deck;
- introduces only **semantic-contract legality** and **capability-gated specialization**;
- makes the compiler section causal: selected environment → actual capability context → legal specialization;
- moves performance, IR stage contracts, semantic trust, and maturity details into Q&A appendix;
- removes the false impression that the planner itself produces all semantic guarantees.

## Hostile pass

### Narrative overload

New main nouns after slide 11: `semantic descriptor` and `capability context`. `SSA`, SCCP, e-graphs and IR facts are not new main-deck topics.

**Pass condition:** the audience can follow slides 12–16 without knowing SSA theory.

### Two-talk problem

Slide 12 explicitly states:

```text
Planning: What exists?
Compiler pass: What may I change?
```

Slide 14 reconnects both sides through `LanguagePlan + selected backend → capability context`.

**Result:** PASS, provided the speaker does not turn slide 13 into a CSE tutorial.

### Compiler vanity

CSE and constant folding appear only as consequences of the same semantic safety predicate. The point is not “the project has optimizations”; the point is “legality consumes explicit properties.”

**Result:** PASS.

### Demo theatre

The visible slide now matches the exact executable path: synthetic ambiguity → explicit preference → plan → runtime → `41 → 42`. The synthetic package is labeled, and the slide no longer claims Wist semantics.

**Result:** PASS after CI exercises `demo/run-demo.sh`.

### Implementation maturity

- semantic-gated CSE/folding: implemented;
- Wist plan/backend capability gating + backend validation: implemented;
- IR fact/capability checks: implemented, appendix only;
- e-graph: bounded symbolic simplifier, appendix/Q&A only;
- performance: needs measurement.

**Result:** PASS.

### Timing

Canonical authored budget: 21:05 inside a 25:00 content slot. Demo is 2:00, interactions are short prediction/reveals, leaving 3:55 hard buffer before Q&A.

**Result:** PASS if rehearsal stays under 22:00.

### Audience prerequisites

No SSA lesson is required. Slide 13 uses three-address-like notation only. `pure`, `deterministic`, `trusted`, and `capability` are explained by consequence.

**Result:** PASS.

### Memorability

One phrase:

> Resolve globally. Justify locally. Execute concretely.

One picture: global plan on the left, local rewrite evidence on the right.

One example: two `foo(x)` calls.

**Result:** PASS.

## Main attack surfaces for Q&A

1. Why not DI/builder?
2. Why not LLVM/MLIR?
3. Does `LanguagePlan` prove semantic compatibility?
4. What if semantic metadata lies?
5. What if selected backend cannot consume optimized IR?
6. Does extensibility hurt performance?
7. How is the planner/runtime boundary testable?
8. What is experimental vs implemented?
9. Is restricted composition a sandbox?
10. Is the “e-graph” actually an e-graph/equality-saturation framework?
11. Do IR contracts schedule passes?
12. Why use a synthetic demo rather than Wist?

Canonical answers live in `CLAIM_BOUNDARIES_40_QA.md` and exact maturity statuses live in `claims.md`.
