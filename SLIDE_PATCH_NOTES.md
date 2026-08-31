# Slide patch notes — 2026-09-01

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

This patch is presentation-only. UniversalToolchain production code/API/behavior is intentionally unchanged.

## Material main-deck changes

### Slide 1 — title / thesis

Changed to:

> **Build an Extensible Language, Run a Concrete One**

Opening thesis:

> **Resolve composition before execution — keep open choices out of the hot path.**

This title keeps extensibility explicit, communicates open → concrete execution, carries a performance consequence without promising zero cost, and is understandable without knowing UniversalToolchain APIs.

### Slide 5 — provider ambiguity wording

Scoped the heading to the actual guarantee:

> **Provider ambiguity fails before execution**

This avoids implying that every possible ambiguity class is rejected identically.

### Slide 7 — composition deabstraction

Rewritten as a literal before/after:

```text
provider = A | B          provider = A
route = R1 | R2 | R3  →  route = R2
runtime = X | Y           runtime = X
order = partial           order = deterministic
```

Payoff: **open composition choices become concrete plan data**.

### Slide 8 — exact planner/runtime boundary

Kept the strong planner/runtime split and made the payoff explicit:

> **No second global composition pass.**

Runtime verification/materialization remains visible and is not mislabeled as zero-cost execution.

### Slide 9 — staging payoff

Replaced the older generic deabstraction framing with the core mental model:

> **Extensible at composition time. Concrete at execution time.**

The slide shows an extensible world (`packages/providers/routes/ordering/conflicts`) → `LanguagePlan` → concrete provider/route/runtime/order.

### Slide 10 — two deabstraction layers

Made the distinction explicit:

1. composition deabstraction — current guarantee;
2. representation/code specialization — separate optional optimization.

The slide explicitly allows interfaces, objects, validation and indirect dispatch to remain.

### Slide 14 — four cost boundaries

Rebuilt around:

> **Extensibility changes where we pay — not whether cost exists.**

Visible boundaries are now:

1. Planning;
2. Runtime creation;
3. First execution;
4. Steady state.

Bottom line:

> **Don't repeatedly pay for decisions already made.**

And the guardrail is visible:

> **No re-planning ≠ zero overhead.**

### Slide 16 — takeaway

Changed final memory hook to:

> **Be extensible when composing. Be concrete when executing.**

The final three-step story is extensions → planning → resolved runtime.

## Appendix performance change

All four numerical boundaries are now `NEEDS MEASUREMENT` for the exact current truth snapshot. The appendix names the current benchmark surfaces but does not invent or reuse numbers from unrelated workloads/revisions.

Added conceptual amortization only:

```text
N × (Ccomposition + Cexecution)
vs
Ccomposition + N × Cexecution
```

`Ccomposition / N` is explicitly labeled a cost model, not benchmark evidence.

## Speaker-note hardening

The live override notes now contain prepared answers for:

- “Is extensibility free?” — no;
- “Are you claiming zero-cost abstractions?” — no;
- “Then why should this be faster?” — architecture does not guarantee faster final code;
- runtime validation vs second planning pass;
- current architecture guarantee vs optional JIT/AOT specialization;
- four cost boundaries and amortization;
- exact-current-revision benchmark evidence boundary.

The existing slide-12 note already contains the DI distinction: DI materializes known bindings; the planner resolves a domain-specific whole-language composition before materialization.

## Preserved material

Unchanged in role/narrative:

- handwritten pipeline as strongest baseline;
- planner is not always needed;
- UTL2002 case;
- route construction;
- `LanguagePlan`;
- exact planner/runtime boundary;
- structural ≠ semantic compatibility;
- prior-art positioning;
- source-backed `41 → 42` demo;
- 16 main slides + 4 appendix slides;
- existing visual language.
