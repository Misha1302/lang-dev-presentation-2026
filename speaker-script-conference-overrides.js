// Non-destructive runtime overrides for rehearsal pacing.
// Original speaker-script-canonical.js and speaker-script-research-update.js stay intact.
// These overrides shorten bridge/detail slides and keep long sequences on one causal line
// without deleting slides or moving them to appendix.
window.SPEAKER_SCRIPT = Object.freeze({
  ...window.SPEAKER_SCRIPT,

  m1: `Hi everyone. The title of this talk is: Build the Language, Then Make the Abstractions Disappear. The question is: can independently developed language capabilities become one concrete language and still optimize well? I will use three words. AUTHOR: build reusable language pieces. RESOLVE: turn one selected language profile into one concrete compiler plan. OPTIMIZE: erase machinery when it has done its job, while keeping only the semantic facts later compiler decisions still need.`,

  m3: `Why is reuse hard in a compiler?

A feature such as arrays is not just syntax. It can touch types, analysis, IR, lowering, optimization, backend behavior and tooling. If every related language copies a whole compiler, it copies this vertical slice again and again.

So the reusable unit has to be able to span layers, not just attach to one small hook.`,

  r1: `First, why pay for any of this? Languages evolve in practice, so variation is real. But that does not prove a reusable architecture is worth its ceremony. It only gives us a reason to measure the trade-off.`,

  r2: `Clone-and-own is the strongest simple baseline. It is cheap at the beginning and easy to explain. A reusable platform only wins if later variants become cheaper enough to repay the upfront cost.`,

  r3: `So we froze one pricing-language workload and implemented related variants both ways: clone-and-own and UniversalToolchain composition. The important part is that a negative result was allowed. If composition did not pay back, the architecture should not pretend that it did.`,

  m26: `The local example worked because all required facts were nearby. Many useful optimizations are not like that. The code pattern may be local, but the proof that the transformation is legal may live in a loop, another block, alias facts or another analysis.

That is the bridge: disappearing machinery is easy locally; preserving useful meaning becomes hard when legality is non-local.`,

  m30: `Keep the bounds-check example in mind. The consumer question is SafeIndex(a, i). I do not want true and false to be the only states, because unsupported, unknown, established, refuted and contradictory lead to different compiler behavior.

The safety rule is simple: uncertainty is not permission to optimize.`,

  m31: `Still on the same example: range and extent are useful only if their assumptions line up. They must refer to the same subject, context and program revision, and no later mutation may invalidate the fact.

So the issue is not just evidence. It is current-valid evidence here and now.`,

  m32: `This is the same independence problem we had for language capabilities. A consumer should not learn every producer's private API. It should ask a published semantic question and receive evidence through that contract.`,

  m33: `Now the strongest baseline is not a naive compiler. LLVM and MLIR already have serious local mechanisms: analysis managers, invalidation, interfaces, effects, data-flow and conversion legality.

Any shared evidence lifecycle has to beat those plus explicit local adapters.`,

  m34: `So the hypothesis is narrower than “make a universal semantic layer”. The possible reusable boundary is the lifecycle of evidence: typed result, identity, context, revision, assumptions and provenance.

This is still a hypothesis, not a result.`,

  m35: `A useful modularity test is: add a new producer and change zero existing consumers.

But that is not a soundness theorem. Unknown is not yes. Unsupported is not yes. Refuted is no. Contradictory current evidence must fail closed unless there is an explicit trusted reconciliation rule.`,

  m36: `This write example is a quick supporting detail, not a new chapter. The point is that the same split appears outside bounds checks: source-level write meaning and later runtime lowering obligations are different things and must not be mixed.`,

  m39: `Here is the same validity problem from another angle. A typed fact can still become stale after the program changes.

The question is not only what the fact says. The question is whether it still describes the same value, operation, control-flow point, revision and assumptions.`,

  m40: `I call that packaged answer a Judgement, but the name is not the important part.

The important part is: proposition, result, subject, context, revision, assumptions and evidence travel together. Freshness and provenance are part of the answer instead of private bookkeeping in each consumer.`,

  m41: `The matching concept is the transformation obligation: the proposition that must be established before this transformation is legal.

A producer can provide evidence, but it cannot quietly weaken the transformation's precondition. If the obligation is not discharged, we keep the safe program.`,

  m48: `This is the falsification test. Compare the shared lifecycle against the best local baseline: explicit adapters, existing invalidation, existing interfaces and local proof obligations.

If the shared layer does not reduce coupling or verification burden at equal precision and safety, we should not keep it.`,

  m52: `Let me finish with the three words from the beginning.

AUTHOR: build reusable language capabilities against shared contracts. RESOLVE: turn one profile into one concrete, structurally feasible compiler plan. OPTIMIZE: erase machinery when it is no longer needed.

But not all meaning should disappear with the machinery. Some current-valid semantic knowledge may still be needed by later decisions. The open research question is whether a shared evidence lifecycle earns its complexity against strong LLVM, MLIR and local-adapter baselines.

Thank you.`
});
