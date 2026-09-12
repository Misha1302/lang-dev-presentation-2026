# Prior-art matrix research update — 2026-09-12

## Scope

This note records the evidence boundary for the revised comparison of the **research target / ideal UniversalToolchain**, not the current implementation depth of Wist or UT.

The target being compared is:

> Resolve independently authored representations, analyses, transformations and execution engines into one compiler plan, while allowing typed, validity-scoped semantic evidence and transformation-owned obligations to cross representation boundaries without requiring one universal program representation.

This is a research hypothesis and synthesis target, not a novelty certificate.

## Main-deck comparators

### MLIR

Primary sources:

- https://mlir.llvm.org/docs/Interfaces/
- https://mlir.llvm.org/docs/DialectConversion/
- https://mlir.llvm.org/docs/Dialects/Transform/
- https://mlir.llvm.org/doxygen/classmlir_1_1DataFlowSolver.html

Strongest overlap: extensible multi-level IR, generic interfaces and external models, reusable data-flow infrastructure, explicit conversion legality and extensible transformation control.

Boundary used by the deck: MLIR does **not** have one universal opcode set, but its program representations share the MLIR structural meta-model. The research target asks whether independent representation/engine providers can sit outside one mandatory program-IR model and still participate in one evidence/obligation lifecycle.

### Spoofax 3 / PIE

Primary sources:

- https://spoofax.dev/spoofax-pie/background/key_ideas/
- https://spoofax.dev/references/pie/

Strongest overlap: flexible, modular and incremental language pipelines expressed as typed PIE tasks; Spoofax Core is intentionally decoupled from concrete meta-components.

Consequence: “no universal program IR” is not sufficient differentiation by itself. The remaining target must include profile-driven provider/route resolution and semantic obligations/evidence across independently authored components.

### JetBrains MPS

Primary sources:

- https://www.jetbrains.com/help/mps/generation-plan.html
- https://www.jetbrains.com/help/mps/generator-cookbook.html

Strongest overlap: global generator planning and cross-language ordering; explicit Generation Plans centralize ordering; checkpoints preserve transient models and mapping labels for later cross-model/cross-phase reference resolution.

Consequence: a global resolved plan and cross-phase mappings are prior art ingredients, not novelty claims.

### Neverlang

Primary sources:

- https://neverlang.di.unimi.it/neverlang.html
- https://link.springer.com/article/10.1007/s10664-021-10074-6

Strongest overlap: independently developed language features organized into modules/roles/slices and composed into configurable compiler/interpreter products.

Consequence: whole-language feature composition is established prior art.

### ableC / Silver / Copper

Primary sources:

- https://melt.cs.umn.edu/ableC/
- https://melt.cs.umn.edu/

Strongest overlap: independently developed language extensions plus modular parser and attribute-grammar analyses that provide concrete composition guarantees within a narrower host-language setting.

Consequence: the broader UT target must not imply broader scope automatically means stronger guarantees.

### GEMOC / BCOoL

Primary sources:

- https://gemoc.org/BCOoL/
- https://gemoc.org/studio.html

Strongest overlap: explicit coordination patterns between heterogeneous executable modeling languages and configuration of heterogeneous execution engines.

Consequence: heterogeneous language/engine coordination is also prior art; the remaining target concerns compiler representation/analysis/lowering resolution and optimizer evidence across arbitrary representations.

## Appendix comparators

- LLVM New Pass Manager — cached analyses, plugins, preservation/invalidation: https://llvm.org/docs/NewPassManager.html
- MontiCore — reusable textual language components, inheritance/embedding/aggregation and language-component tooling: https://monticore.github.io/monticore/docs/Languages/
- Racket — first-class language creation via readers/expanders/#lang: https://docs.racket-lang.org/guide/languages.html
- Graal/Truffle — polyglot language implementation/interoperability baseline: https://www.graalvm.org/latest/reference-manual/polyglot-programming/

## Falsification boundary

The research meta-layer should be rejected if a composition of mature mechanisms — for example PIE-style typed pipeline tasks, MLIR-style semantic interfaces/dataflow where applicable, and explicit adapters/checkpoints — provides equivalent safety, precision and producer/consumer decoupling with less schema, governance and runtime/planning infrastructure.

Required comparison metrics remain:

- false obligation discharges / unsafe transformations: zero in the test model;
- edits required in existing consumers when adding a new producer;
- number of pairwise integration edges/adapters;
- optimization/analysis precision;
- invalidation/re-analysis/transport cost;
- schema/versioning/governance burden;
- planner/runtime overhead where material.
