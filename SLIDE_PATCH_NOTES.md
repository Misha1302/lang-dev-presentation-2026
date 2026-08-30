# Slide patch notes

These are safe presentation-only changes to apply manually to `index.html`, speaker notes and/or appendix. They do not require production code changes.

## Main-deck wording changes

### Title / thesis

Current style is already close. Prefer:

> Modules keep local knowledge. The planner owns global composition decisions.

Speaker note addition:

> The planner does not remove complexity. It changes where complexity lives and how it is represented.

### Handwritten baseline slide

Keep this early. Add speaker note:

> For one fixed language with known parser, lowering, optimizer and backend, this is often the better architecture. UniversalToolchain starts to pay for itself only when components are contributed independently and create global choices.

### Provider ambiguity slide

Change title from broad “planner refuses to guess” to scoped wording:

> Provider ambiguity fails before execution

Speaker note:

> I am deliberately saying provider ambiguity here. Equal-cost route selection is a separate policy question; determinism alone does not prove semantic equivalence.

### LanguagePlan slide

Add bottom caption:

> Resolved composition data, not a service container and not a semantic proof.

### Runtime boundary slide

Add note:

> Runtime validates/materializes the selected graph. It should reject mismatches; it should not rediscover global provider or route choices.

### Payoff slide

Keep “open composition decisions disappear”. Avoid “abstractions disappear” as zero-overhead claim. Add:

> The abstraction disappears as an open decision, not necessarily as an allocated object or runtime cost.

### Costs slide

Ensure explicit costs:

- planning time;
- framework concepts;
- configuration state space;
- need for evidence/benchmarks;
- structural guarantees are weaker than semantic guarantees.

## Appendix slides to add or strengthen

1. What planning does not prove.
2. Equal-cost route ambiguity.
3. PlanHash is representation identity.
4. Valid plan is not a sandbox.
5. PlanFuzz as research/testing layer, not production proof.
6. NativeAOT/trimming: measured scope only.
7. Thread-safety: lifecycle coordination is not arbitrary provider thread-safety.
8. Future work: cache/version solver/PlanningReport/SAT/repo split decisions.

## Demo fallback

If live demo fails, switch to evidence story:

1. show claim/evidence map;
2. show `LanguageCompiler.Compile` -> `LanguagePlan` -> `LanguageRuntime.Create` boundary;
3. show ambiguity diagnostic and explicit preference;
4. say exact runtime/build validation is CI-bound to a pinned truth snapshot.

Do not improvise unmeasured performance claims.
