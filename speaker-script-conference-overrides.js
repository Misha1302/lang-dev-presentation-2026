// Non-destructive runtime overrides for rehearsal pacing.
// Original speaker-script-canonical.js and speaker-script-research-update.js stay intact.
// These overrides shorten bridge/detail slides and make the main causal line
// explicit without deleting slides or moving them to appendix.
window.SPEAKER_SCRIPT = Object.freeze({
  ...window.SPEAKER_SCRIPT,

  m1: `Hi everyone.

The title of this talk is: Build the Language, Then Make the Abstractions Disappear.

The question is: can independently developed language capabilities become one concrete language and still optimize well?

I will use three words. AUTHOR: build reusable language pieces. RESOLVE: turn one selected language profile into one concrete compiler plan. OPTIMIZE: erase machinery when it has done its job, while keeping only the semantic facts later compiler decisions still need.`,

  m3: `Why is reuse hard in a compiler?

A feature such as arrays is not just syntax. It can touch types, analysis, IR, lowering, optimization, backend behavior and tooling. If every related language copies a whole compiler, it copies this vertical slice again and again.

So the reusable unit has to be able to span layers, not just attach to one small hook.`,

  r1: `Before building architecture, we should check that the problem is real. A large empirical study of Xtext projects found many developed languages and studied grammar evolution. So languages do change; the real question is when that variation justifies paying for explicit reuse.`,

  r2: `And reuse is not free. Clone-and-own is cheap now. A reusable platform costs more first and only pays back if repeated variants become cheaper later. So we treated composition as a trade-off to test, not as an automatic win.`,

  r3: `This is the experiment setup. We froze one pricing-language workload, implemented related variants with clone-and-own and with UniversalToolchain composition, and accepted a negative result in advance. The next slide is the important result.`,

  m26: `The local example worked because all required facts were nearby. Many useful optimizations are not like that. The code pattern may be local, but the proof that the transformation is legal may live in a loop, another block, alias facts or another analysis.

That is the bridge: disappearing machinery is easy locally; preserving useful meaning becomes hard when legality is non-local.`,

  m30: `Let us make the consumer question explicit: SafeIndex(a, i). I do not want true and false to be the only states. Unsupported, unknown, established, refuted and contradictory mean different things.

The safety rule is simple: uncertainty is not permission to optimize.`,

  m31: `Even useful facts are not automatically safe to combine. Range and extent must refer to the same subject, context and program revision, and their assumptions must still hold.

So the central issue is freshness and applicability: is this evidence still true here, now?`,

  m35: `A useful modularity test is: add a new producer and change zero existing consumers.

But that is not a soundness theorem. Unknown is not yes. Unsupported is not yes. Refuted is no. Contradictory current evidence must fail closed unless there is an explicit trusted reconciliation rule.`,

  m39: `Here is the same problem from another angle. A typed fact can still become stale after the program changes.

The question is not only what the fact says. The question is whether it still describes the same value, operation, control-flow point, revision and assumptions.`,

  m40: `I call that packaged answer a Judgement, but the name is not the important part.

The important part is: proposition, result, subject, context, revision, assumptions and evidence travel together. Freshness and provenance are part of the answer instead of private bookkeeping in each consumer.`,

  m41: `The matching concept is the transformation obligation: the proposition that must be established before this transformation is legal.

A producer can provide evidence, but it cannot quietly weaken the transformation's precondition. If the obligation is not discharged, we keep the safe program.`,

  m52: `Let me finish with the three words from the beginning.

AUTHOR: build reusable language capabilities against shared contracts. RESOLVE: turn one profile into one concrete, structurally feasible compiler plan. OPTIMIZE: erase machinery when it is no longer needed.

But not all meaning should disappear with the machinery. Some current-valid semantic knowledge may still be needed by later decisions. The open research question is whether a shared evidence lifecycle earns its complexity against strong LLVM, MLIR and local-adapter baselines.

Thank you.`
});
