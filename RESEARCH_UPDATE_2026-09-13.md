# Research update — 2026-09-13

## Decision

The deck now treats MLIR as the strongest technical baseline, not as a weak foil. The central open claim is narrowed to cross-representation semantic-evidence lifecycle, compared against explicit adapters.

## Current evidence

- MLIR already supports dialects, interfaces, external models, effects, conversion legality and a composable data-flow framework. Therefore, "independent producer strengthens consumer" is not a sufficient novelty claim.
- LLVM New Pass Manager already provides mature analysis preservation/invalidation. Therefore, UT must not claim invalidation itself as novel.
- MPS generation plans already centralize generator ordering and checkpoints. Therefore, whole-language planning has strong prior art.
- Neverlang already composes language modules/slices. Therefore, capability composition must be framed as current-language-engineering context, not invention.
- EuroLLVM 2024 MLIR performance microbenchmarks support only the narrow lesson that abstraction overhead must be measured; they are not a UT-vs-MLIR benchmark.

## Slide changes made

- Strengthened the prior-art matrix around responsibility boundaries.
- Moved the external performance benchmark from the opening into the cost/falsification section.
- Rewrote late architecture slides so Wist AIR is only a current provider witness, not the universal architecture.
- Reframed the MLIR comparison around composable data-flow and external models.
- Made the falsification slide explicit: delete the shared layer if explicit adapters win on cost, precision and safety.
- Replaced the speaker overlay with concise runtime-complete notes for all 52 final main slides.

## New validation requirements

The old render and timing checks counted source fragments rather than the final runtime DOM. They now read runtime counts/keys from the executed deck, so runtime-demoted appendix slides and final ordering are validated directly.

## Sources checked

- MLIR Interfaces / External Models: https://mlir.llvm.org/docs/Interfaces/
- MLIR DataFlowSolver API: https://mlir.llvm.org/doxygen/classmlir_1_1DataFlowSolver.html
- EuroLLVM 2023: Extensible and Composable Dataflow Analysis in MLIR: https://www.llvm.org/devmtg/2023-05/
- LLVM New Pass Manager: https://releases.llvm.org/14.0.0/docs/NewPassManager.html
- MPS Generation Plan: https://www.jetbrains.com/help/mps/generation-plan.html
- Neverlang language composition: https://neverlang.di.unimi.it/
- EuroLLVM 2024: How Slow is MLIR?: https://llvm.org/devmtg/2024-04/
