Object.assign(window.SPEAKER_NOTES, {
  m1: `ЗАЧЕМ: сразу заменить старую память «route search» на новую центральную формулу.

СКАЗАТЬ: доклад не про то, что UniversalToolchain умеет искать дешёвый путь. Он про более общую границу: когда расширяемость языка создаёт обязанность построить корректный concrete compiler из независимых pieces. Главный тезис: feasibility before preference. Сначала hard obligations, потом выбор между уже допустимыми реализациями.

ПЕРЕХОД: начинаем с baseline, где planner не нужен.

НЕ ПЕРЕОБЕЩАТЬ: UT — case study, не эталон всей архитектуры.` ,
  m2: `ЗАЧЕМ: убрать strawman и показать уважение к explicit pipeline.

СКАЗАТЬ: если один owner знает parser, lowering, optimizer и backend, лучший design — явная цепочка. Builder или DI могут помочь собрать объекты, pass manager может выполнить известную последовательность. Отдельный planner здесь только добавит complexity.

ПЕРЕХОД: проблема возникает, когда появляется не один compiler, а семейство вариантов.

НЕ ПЕРЕОБЕЩАТЬ: не утверждать, что декларативность всегда лучше ручного wiring.` ,
  m3: `ЗАЧЕМ: объяснить, зачем нужна extensibility, без API-tour vocabulary.

СКАЗАТЬ: независимые авторы могут добавлять syntax, lowering, optimizers, backends and policies. Важно не количество plugins, а то, что их требования пересекают compiler stages и ownership boundaries.

ПЕРЕХОД: но даже это ещё не автоматически planner.

НЕ ПЕРЕОБЕЩАТЬ: language family здесь practical architecture term, не доказательство совместимости всех языков.` ,
  m4: `ЗАЧЕМ: дать точный threshold.

СКАЗАТЬ: choices interacting is too broad. DI, builder, pass manager or legalization may already own the local decision. Planner начинается только когда independently owned choices create whole-compiler hard constraints that no local mechanism can guarantee.

ПЕРЕХОД: поэтому нужно развести ownership: кто задаёт semantics и кто выбирает implementation.

НЕ ПЕРЕОБЕЩАТЬ: planner не угадывает скрытые invariants.` ,
  m5: `ЗАЧЕМ: исправить опасную фразу «planner chooses the language».

СКАЗАТЬ: language author или integrator определяет semantics, target и policy. Из этого возникают obligations. Extension implementations declare what they require and satisfy. Planner выбирает implementation, satisfying those obligations. Runtime materializes one frozen answer.

ПЕРЕХОД: теперь покажем, почему structural reachability недостаточна.

НЕ ПЕРЕОБЕЩАТЬ: planner owns global implementation resolution, not language meaning.` ,
  m6: `ЗАЧЕМ: разрушить mental model structural path equals feasible compiler.

СКАЗАТЬ: same nominal AIR type не доказывает, что IR typed, lowered or target legal. Shortcut may connect Semantic IR to AIR and reach CIL structurally, but it can still violate backend obligations.

ПЕРЕХОД: значит architecture должна ставить admissibility before ranking.

НЕ ПЕРЕОБЕЩАТЬ: не предлагать full dependent type system; нужны только composition-relevant properties.` ,
  m7: `ЗАЧЕМ: главный architecture slide.

СКАЗАТЬ: language selection derives hard obligations. Candidate implementations publish requires, ensures and conflicts. Feasibility rejects plans that fail hard constraints. Preference applies only after that. Cost, provider preference and deterministic tie-break are preference, not correctness.

ПЕРЕХОД: результат global reasoning должен стать concrete data.

НЕ ПЕРЕОБЕЩАТЬ: не говорить SAT/SMT, theorem prover or global optimizer.` ,
  m8: `ЗАЧЕМ: сохранить сильную идею inspectable LanguagePlan без API tour.

СКАЗАТЬ: concrete plan records selected implementations, ordering, backend, provenance and diagnostics. Current UT has LanguagePlan as data before source execution. This is good. But the target model is stronger about what makes a plan admissible.

ПЕРЕХОД: когда plan materialized, можно показать freeze boundary.

НЕ ПЕРЕОБЕЩАТЬ: PlanHash is not semantic proof or security attestation.` ,
  m9: `ЗАЧЕМ: сохранить lifecycle story and remove semantic ownership bug.

СКАЗАТЬ: during composition, architecture is still open. Planning produces a feasible concrete plan. Materialization binds exact runtime components. Run or Build then follows that plan; runtime does not redesign the whole language.

ПЕРЕХОД: central case study shows why type-compatible shortcut is rejected.

НЕ ПЕРЕОБЕЩАТЬ: no second whole-language planner does not mean no validation or no compile work.` ,
  m10: `ЗАЧЕМ: заменить misleading Cost 7 to Cost 2 demo.

СКАЗАТЬ: backend requires AIR plus NoHighLevelOps and CilLegal. Shortcut reaches AIR, so route-first thinking would call it candidate. But it fails hard obligation; reject it before preference. LegalizeForCIL establishes required properties; only then, if two legalizers are feasible, preference may choose.

ПЕРЕХОД: now we can honestly explain current UT as prototype with limits.

НЕ ПЕРЕОБЕЩАТЬ: do not claim current UT already has this whole-language property model.` ,
  m11: `ЗАЧЕМ: explicitly separate current implementation, limitation and proposed model.

СКАЗАТЬ: current UT proves staging: LanguageCompiler, LanguagePlan, deterministic structural route, selected passes, exact runtime materialization. Current limitation: route layer uses nominal artifact contracts and does not generally express semantic obligations like target legality. Proposed model: hard obligations then feasibility then preference.

ПЕРЕХОД: this honesty leads to the price of extensibility.

НЕ ПЕРЕОБЕЩАТЬ: do not sell UT as finished reference architecture.` ,
  m12: `ЗАЧЕМ: сохранить честность про costs and evidence debt.

СКАЗАТЬ: contracts, diagnostics, tests and startup/materialization are real costs. The important criterion: if invariant affects composition correctness, hiding it defeats the planner's purpose. Performance impact needs measurement.

ПЕРЕХОД: strongest counterargument decides when not to use this architecture.

НЕ ПЕРЕОБЕЩАТЬ: no numerical speed claim, no hot path claim without data.` ,
  m13: `ЗАЧЕМ: make the talk defensible against LLVM/MLIR/DI questions.

СКАЗАТЬ: explicit pipeline, builder, DI, pass manager and MLIR-style legalization are better when they already own the decision. Whole-language planner earns its cost only for expressed cross-owner hard constraints.

ПЕРЕХОД: final rule compresses the boundary.

НЕ ПЕРЕОБЕЩАТЬ: not a replacement for MLIR or LLVM.` ,
  m14: `ЗАЧЕМ: leave one precise memory.

СКАЗАТЬ: resolve globally only what correctness cannot own locally. Hard obligations cannot be traded away. Preference is allowed only among feasible plans. Final memory: Declare requirements locally. Resolve feasibility globally. Execute one concrete plan.

ПЕРЕХОД: Q&A can go to current UT limitations and prior-art boundary.

НЕ ПЕРЕОБЕЩАТЬ: do not broaden planner into universal architecture.` ,
  a1: `Technical appendix: current UT structural route and proposed obligation-first planner boundary.`,
  a2: `Technical appendix: mandatory vs optional is not source-target equality.`,
  a3: `Technical appendix: selected contribution is not necessarily executed.`,
  a4: `Technical appendix: nominal artifact identity is not enough semantic state.`,
  a5: `Technical appendix: IR stage contracts already demonstrate requires/produces/preserves/invalidates locally.`,
  a6: `Technical appendix: deterministic tie-break supports reproducibility, not semantic equivalence.`,
  a7: `Technical appendix: planning and runtime performance claims need measurements.`,
  a8: `Technical appendix: strongest objection and narrow justification for planner.`
});
