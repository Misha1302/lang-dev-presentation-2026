# REBUILD_DECISIONS — LangDev presentation rebuild 2026-09-17

## Chosen killer example

Main example: one independently authored `Delegates` module reused across multiple type-semantics models and constrained by several typing disciplines in one profile.

Reason: it begins with a programmer-visible language construct, exposes cross-extension semantic obligations, avoids turning the talk into optimizer-only infrastructure, and gives a concrete deabstraction payoff: generic delegate machinery can remain safe or become a direct call when obligations are established.

## Falsification summary

Delegates was compared against SafeIndex, ownership+FFI, tensors/GPU, units, automatic differentiation, query/reactive, serialization/layout, DSL routing and backend-only examples. SafeIndex remains a strong appendix example for semantic evidence but is not main because the programmer does not first gain a new language construct. Delegates stayed main because it forces both language-composition and specialization questions in one compact example.

## Scope narrowed after prior-art attack

The deck does not claim novelty for language workbenches, modular typing rules, global plans, MLIR-style interfaces/effects/conversion, LLVM-style analysis invalidation, proof obligations or translation validation. The remaining research hypothesis is the disciplined boundary between feature authoring, semantic capability resolution, evidence lifecycle and deabstraction.

## Implementation boundary

UniversalToolchain is presented only as an implementation witness for selected planning/deabstraction ideas. Delegates × multiple independently authored type systems is labeled as TARGET / RESEARCH HYPOTHESIS, not as an implemented UT feature.
