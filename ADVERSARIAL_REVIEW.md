# Independent adversarial review

## Issue 1 — “abstractions disappear” could be read as a zero-overhead claim

Fix: the main payoff slide now says open **composition decisions** disappear; the following slide explicitly lists specialization as future/illustrative and the appendix rejects zero-overhead claims.

## Issue 2 — a conceptual demo would not prove the architecture

Fix: replaced simulated output with a source-backed program using current `LanguagePackageBuilder`, `LanguageCompiler`, `LanguagePlan` and `LanguageRuntime`. CI checks out the exact truth commit and executes it.

## Issue 3 — runtime validation might look like a second planner

Fix: the boundary slide distinguishes exact plan/provider/route validation from global provider/route resolution and points to `ExactRuntimeBindingTests`.

## Issue 4 — structural route compatibility could be oversold as semantic compatibility

Fix: dedicated claim-boundary slide states exactly what `ContractsConnect`/declared protocol checks and what remains outside it.

## Issue 5 — planner could be framed as the default even when a handwritten pipeline is simpler

Fix: retained the explicit-pipeline slide as the strongest baseline and added a decision-criterion slide that recommends the simplest owner able to make whole-system decisions.
