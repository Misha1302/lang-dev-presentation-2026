# Claim Boundaries / Hostile Q&A

## 1. Why isn't this just a pass manager?
A pass manager is enough when the compiler owner already owns the sequence and analysis invalidation. The proposed planner is only for cross-owner hard constraints.

## 2. Why isn't this MLIR legalization?
If the problem is local IR legalization, MLIR-style legalization is the smaller mechanism. Whole-language planning is for requirements spanning language features, frontends, transformations, backends and policy.

## 3. Why isn't this DI?
DI wires objects/providers. It does not normally prove a compiler transformation sequence establishes target legality properties.

## 4. Why isn't a builder enough?
A builder is enough for configuration. It is not enough when independent implementations create feasibility constraints the builder owner cannot locally guarantee.

## 5. Why doesn't structural route imply correctness?
Because artifact identity is not semantic state. AIR may or may not be typed, lowered, verified, or target legal.

## 6. Who decides whether an optimization is mandatory?
Usually nobody: it is optional. It becomes mandatory only through language semantics, build policy, validation, instrumentation, or backend legality.

## 7. What prevents mandatory legalization from being skipped?
In the target architecture, explicit hard obligations and requires/ensures. In current UT, the whole-language route layer does not generally model this.

## 8. How are IR invariants represented?
Only composition-relevant properties should be modeled. This is not a theorem prover.

## 9. Why isn't deterministic tie-break correctness?
Determinism gives reproducibility. Correctness requires admissibility.

## 10. Who owns Cost?
Cost is preference policy. It should only apply after hard constraints are satisfied.

## 11. What exactly is limited in current UT?
It has deterministic structural routes, selected same-contract passes and exact materialization, but no general whole-language semantic-obligation model.

## 12. What does planner buy without proving full semantic equivalence?
It makes expressed composition constraints explicit, rejects impossible combinations, produces one inspectable plan and improves diagnostics.

## 13. When not to use a planner?
When explicit pipeline, builder, DI, pass manager or MLIR-style legalization already owns the decision.

## 14. Does pre-planning improve performance?
Needs measurement. Staging is confirmed; speed is not.

## 15. Is UniversalToolchain the reference architecture?
No. It is a current case study and prototype of staged composition.

## 16. Why keep route vocabulary?
For current UT materialization. It should not be the general semantic planning abstraction.

## 17. Can selection imply execution?
No. Availability/selection and mandatory execution obligation are separate.

## 18. Why not encode every state as a new artifact kind?
Orthogonal properties create nominal-state explosion.

## 19. Does a plan hash prove correctness?
No. It identifies a resolved plan; it is not semantic proof.

## 20. Does metadata lying break this?
Yes. The planner can only reason about expressed and trusted facts.

## 21. Is this a solver talk?
No. The point is responsibility, not SAT/SMT branding.

## 22. Is this proof-carrying compilation?
No. It is expressed composition feasibility.

## 23. Are all optimizations hard obligations?
No. Most are optional preference.

## 24. What is the strongest rule?
Feasibility before preference.

## 25. What is the final memory line?
Declare requirements locally. Resolve feasibility globally. Execute one concrete plan.

## 26. What is hard?
Semantics, legality, required properties, conflicts, required providers, validation/instrumentation when policy makes them mandatory.

## 27. What is preference?
Provider preference, optimization level, measured cost, code-size vs compile-time, deterministic tie-break among feasible alternatives.

## 28. What if constraints are hidden?
Then the planner cannot save correctness; use simpler architecture or add evidence.

## 29. Does green mean cheap?
No. Green means feasible.

## 30. Does red mean impossible forever?
No. It means inadmissible under current obligations and candidates.

## 31. Why mention current UT limitation publicly?
It makes the architecture honest and prevents false claims.

## 32. What current UT part is strongest?
Staging: planning creates LanguagePlan; runtime materializes and executes the plan.

## 33. What current UT part is weakest for this thesis?
Whole-language route layer lacks general semantic obligations.

## 34. What about backend special cases?
They show missing generic mandatory-operation abstraction.

## 35. What about ordering constraints?
Ordering is not execution requirement.

## 36. What about ReplaceSlot provenance?
It is a targeted countertest/backlog item, not main talk.

## 37. Is artifact contract useless?
No. It is good for representation compatibility, not enough for semantic state.

## 38. What is the minimal proposed addition?
Hard obligations and implementation effects sufficient for feasibility before preference.

## 39. What is not being claimed?
No performance win, no semantic equivalence proof, no universal replacement for existing compiler infrastructure.

## 40. Why is this worth discussing at LangDev?
Because extensible languages need clear ownership boundaries when independent pieces must form one valid runnable compiler.
