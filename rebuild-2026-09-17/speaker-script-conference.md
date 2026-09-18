## m1

I am going to argue for a narrow version of Extensible Programming. The claim is not that a framework makes every language feature free. The claim is that a feature can be authored against explicit semantic requirements, resolved into one concrete language, and later specialized when the program proves the right obligations. The talk title is literal: build the language, then make some authoring abstractions disappear.

## m2

Start with the programmer. After adding an independently authored Delegates extension, the programmer can declare a callable shape, assign a lambda to it, and invoke it. This is not a pass hidden in the compiler. It changes the source language: callable values, lambda creation, invocation, and possibly captured environments become expressible. Only after this is concrete do planner objects matter.

## m3

A compiler plugin usually assumes a known language and representation. A language feature extension is more invasive: it touches syntax, typing, lowering, tooling and optimization. That is why the delegates example is better than an optimizer-only example. It creates the next problem: what happens when the same feature is reused with different type semantics?

## m4

The same source feature can meet several type models. In a nominal language, Mapper may be a named delegate type. In a structural language, the callable may just be a function type from Int to String. In a gradual language, the static type may be accompanied by a runtime contract. None of these is obviously wrong, but a reusable Delegates feature must not hardcode one of them as the only universe.

## m5

One answer is to write DelegatesForNominalTypes, DelegatesForStructuralTypes, DelegatesForGradualTypes, and so on. That is easy once, but it turns language reuse into a matrix of private integrations. Every new typing discipline or target multiplies the surface area. The next tempting answer is a single universal type-system interface.

## m6

A giant ITypeSystem is not a satisfying boundary. If it contains every future semantic operation, it becomes a universal type system. If it keeps only common operations, the interesting parts leak into side channels. So the question changes: what does Delegates actually need to ask, and who is allowed to answer?

## m7

For this example, the feature needs a small set of semantic capabilities: construct a callable for a signature, decide assignability, decide applicability at invocation, compute the invocation result, check capture legality, and sometimes request a runtime check. This list is not a universal ontology. It is the minimum contract that makes this delegates example precise enough to attack.

## m8

There are two scenarios. First, the same feature may be reused across alternative type-system profiles. Second, one concrete profile may combine several typing disciplines. Delegates may rely on nominal types for representation and invocation, effects for call compatibility, and ownership for capture legality. Now the question is no longer 'call the type system'. The question is who composes these independently authored components into one coherent language.

## m9

The ownership boundary matters. Delegates owns the feature-level meaning: there is a callable construct, it has a signature, it can be created and invoked, and it may capture an environment. Typing components own or constrain representation, assignability, variance, runtime checks, effects and lifetimes. No producer should silently weaken the consumer's legality condition.

## m10

Now separate global decisions from local facts. At profile time we choose providers, representations, contract versions, conflicts and routes. At program time we learn exact targets, captures, escape behavior, effects and lifetimes. A resolved profile says the language is coherent. It does not prove that every delegate invocation can be replaced by a direct call.

## m11

A resolver closes the open world. The requested profile asks for Delegates with nominal types, effects and ownership. The resolver chooses providers, checks contracts, and rejects conflicts. If the ownership component cannot answer capture legality for escaping closures, the composition must fail closed or the construct must be rejected. 'Works with everything' is not the claim.

## m12

Structural composition is still not semantic correctness. We may have a parser, type provider, lowering route and backend that assemble successfully. That does not prove a direct-call rewrite preserves the semantics of a delegate invocation. The transformation owns its precondition; evidence producers only help discharge it.

## m13

Here is a concrete obligation. For a direct-call rewrite, we need to know that the delegate has exact target Foo, that conversions match Mapper, that captures are legal or absent, that effects are compatible, that lifetime obligations hold, and that the value does not escape when that is required. If any of these is missing, the safe generic path remains.

## m14

This slide is the rule for avoiding hand waving. NominalTypes contributes a specific assignability fact. EffectSystem contributes a specific effect-compatibility fact. Escape and capture analysis contributes exact-target and environment facts. Delegate lowering consumes those facts for one obligation. The consumer does not depend on every producer's private API.

## m15

Different non-success states matter. Established evidence can discharge the obligation. Unknown evidence keeps the generic path. Unsupported means the profile lacks a required capability. Refuted means the rewrite is illegal. Contradictory current evidence must fail closed unless the language has an explicit trusted reconciliation rule. Extensibility cannot mean optimistic unsoundness.

## m16

Facts also have a lifecycle. A fact is derived with scope and assumptions. It may be transported across representation changes only when a mapping exists. It must be preserved or invalidated after transformations. Only current evidence may be consumed. This lifecycle is where the language-composition story meets the deabstraction story.

## m17

Now the title pays off. The authoring form contains a generic delegate value, generic invocation, capture adapter and maybe a runtime check. After a concrete profile is selected and the program establishes the required facts, this specific program point can become a direct call to Foo. What disappears is the generic delegate machinery. What remains is the concrete operation and the obligation to preserve its semantics. If the proof fails, nothing is erased.

## m18

The idea has serious competition. Workbenches and extensible typing frameworks already compose languages and typing rules. MLIR and LLVM already provide interfaces, effects, legality, analyses and invalidation. In many engineering contexts, a small local adapter per type system is simply the right answer. The proposal only matters if a shared semantic-capability boundary reduces coupling without reducing precision or correctness.

## m19

So the hypothesis is narrow. Can a language feature depend on semantic capabilities rather than one concrete type-system implementation, be globally resolved with independently authored typing components, and then be specialized when the concrete program proves the required legality conditions? None of the ingredients is novel alone. The possible contribution is the disciplined connection between feature authoring, semantic capability resolution, evidence lifecycle and deabstraction.

## m20

UniversalToolchain is not the thesis. It is evidence for selected parts: declarative profiles, staged planning, snapshotted plans, selected backend parity, feasibility before preference, and bounded local deabstraction. Delegates across multiple independently authored type semantics is a target and research hypothesis, not an implemented UT claim. If UT disappeared tomorrow, the research question would still make sense.

## m21

The whole talk is this loop: extend, resolve, prove, erase. Extend the language against semantic requirements. Resolve the concrete semantics for one profile. Prove the local obligations for a program point. Erase only the abstraction whose obligations were established. What disappears may be generic delegate machinery. What remains is the concrete call and preserved semantics. What is implemented today is a set of witnesses; what remains research is the full capability-contract boundary across independent type semantics.

## a1

This appendix records why the delegates example stayed as the main path after comparing alternatives.

## a2

This appendix is the overclaim guard: prior art is a threat, not decoration.

## a3

SafeIndex remains a backup example for semantic evidence but is no longer the main running example.

## a4

These labels keep implementation evidence separate from target architecture and research hypotheses.
