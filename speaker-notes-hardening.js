Object.assign(window.SPEAKER_NOTES, {
  m1: `ЗАЧЕМ: сразу совместить официальный LangDev title с новым архитектурным тезисом.

СКАЗАТЬ: доклад начинается с конкретной extensible .NET language, а не с planner abstraction. Но главный transferable вывод будет архитектурным: когда корректность whole compiler пересекает ownership boundaries, сначала нужно определить feasible implementations, и только потом применять preference. Feasibility before preference.

ПЕРЕХОД: сначала покажем baseline, где planner вообще не нужен.

НЕ ПЕРЕОБЕЩАТЬ: UniversalToolchain — current case study, а не reference architecture.` ,
  m2: `ЗАЧЕМ: убрать strawman против обычного compiler pipeline.

СКАЗАТЬ: если parser, lowering, passes и backend знает один owner, явная цепочка обычно лучше. Builder, DI или pass manager могут помогать локально. Whole-language planner здесь только увеличивает complexity.

ПЕРЕХОД: теперь возьмём реальный язык, для которого extensibility уже полезна.

НЕ ПЕРЕОБЕЩАТЬ: declarative composition не является самоцелью.` ,
  m3: `ЗАЧЕМ: выполнить practical promise accepted abstract до введения терминов planner architecture.

СКАЗАТЬ: pricing-restricted — реальный shipped Wist dialect. Он оставляет variables, scopes и native numeric types, исключает ненужные capabilities и поддерживает interpreter и CIL. Пример 100 * 0.9 + 5 даёт 95. Это не sandbox claim; это composition-constrained language surface.

ПЕРЕХОД: посмотрим, куда исчезают выбранные modules после composition.

НЕ ПЕРЕОБЕЩАТЬ: restricted dialect не означает hardened sandbox.` ,
  m4: `ЗАЧЕМ: вернуть promised Bytecode → AIR → CIL story и показать compiler-native context.

СКАЗАТЬ: Wist frontend modules emit Bytecode; Bytecode-to-AIR lowering creates backend-neutral AIR; further lowering/specialization feeds interpreter or CIL. Extension machinery не должна оставаться набором dynamic choices на каждом execution step — в итоге нужен concrete pipeline.

ПЕРЕХОД: но два backends создают более серьёзную обязанность, чем reachability.

НЕ ПЕРЕОБЕЩАТЬ: generic UniversalToolchain SDK не требует Bytecode или AIR; это current Wist pipeline.` ,
  m5: `ЗАЧЕМ: дать реальный correctness failure class раньше архитектурной абстракции.

СКАЗАТЬ: external bindings и local shadowing — ровно тот случай, где один language может незаметно стать двумя. Local price должен shadow external price одинаково в interpreter и CIL. Current parity tests защищают shadowing, nested scopes, reordered bindings и local/external arithmetic.

ПЕРЕХОД: теперь задаём главный ownership question — кто отвечает за эту parity целиком?

НЕ ПЕРЕОБЕЩАТЬ: тесты доказывают покрытые cases, а не semantic equivalence всех программ.` ,
  m6: `ЗАЧЕМ: вывести необходимость planning из конкретной compiler correctness проблемы.

СКАЗАТЬ: frontend owns binding declarations, lowering owns representation/storage operations, backend owns execution. Ни один local owner не может сам гарантировать whole-language parity. Planner нужен только если такие hard cross-owner obligations можно выразить и проверить на уровне composition.

ПЕРЕХОД: current UT уже содержит полезную staging boundary.

НЕ ПЕРЕОБЕЩАТЬ: planner не угадывает hidden invariants; неизвестное требование остаётся неизвестным.` ,
  m7: `ЗАЧЕМ: отделить сильную current implementation idea от proposed model.

СКАЗАТЬ: current UT already has LanguageDefinition, LanguageCompiler, immutable LanguagePlan and exact LanguageRuntime materialization. Это хорошая staging architecture: global composition происходит до source execution, а runtime следует сохранённому route/provider answer.

ПЕРЕХОД: но current route planner знает меньше о correctness, чем эта story требует.

НЕ ПЕРЕОБЕЩАТЬ: current LanguageCompiler performs structural whole-language resolution, not general semantic proof.` ,
  m8: `ЗАЧЕМ: показать подтверждённый implementation defect в mental model route-first planning.

СКАЗАТЬ: current LanguageArtifactRoutePhase first calls FindBestRoute over conversion edges using sum of int Cost, then inserts selected same-contract passes. If a pass cannot be placed, UTL2204 is reported; planner does not backtrack to a different conversion skeleton. Поэтому Cost and reachability are preference/structure, not feasibility evidence.

ПЕРЕХОД: отсюда возникает более общий architecture rule.

НЕ ПЕРЕОБЕЩАТЬ: не утверждать, что current UT уже реализует obligation-first search.` ,
  m9: `ЗАЧЕМ: дать главный architecture slide только после concrete evidence.

СКАЗАТЬ: requested language derives hard obligations. Candidate implementations declare what they require and ensure. First reject candidates that cannot satisfy obligations. Only among feasible plans may policy compare cost, providers or deterministic tie-breaks. This is the whole point: feasibility before preference.

ПЕРЕХОД: теперь чётко разведём текущий LanguagePlan и то, что stronger planner должен был бы объяснять.

НЕ ПЕРЕОБЕЩАТЬ: это general proposed model, не описание current UT API.` ,
  m10: `ЗАЧЕМ: устранить прежнюю ошибку, где proposed provenance/diagnostics визуально выглядели current LanguagePlan fields.

СКАЗАТЬ: current plan реально содержит Definition, Features, Contributions, RuntimeProvider, Routes, PlanHash и Summary. Stronger target model дополнительно должен сделать obligations/effects and selection reasons inspectable. Diagnostics о failure принадлежат planning result, а не current LanguagePlan object.

ПЕРЕХОД: независимо от силы planner, global reasoning должен закончиться freeze boundary.

НЕ ПЕРЕОБЕЩАТЬ: PlanHash не является semantic proof или security attestation.` ,
  m11: `ЗАЧЕМ: связать accepted title “make abstractions disappear” с реальной lifecycle boundary.

СКАЗАТЬ: during authoring architecture is open; LanguageCompiler resolves whole-language choices; runtime materializes exact components; Run/Build processes source using that frozen environment. “Disappear” means no second whole-language composition decision during repeated execution — не отсутствие compiler work or validation.

ПЕРЕХОД: staging itself does not prove zero overhead.

НЕ ПЕРЕОБЕЩАТЬ: не обещать zero-cost extensibility.` ,
  m12: `ЗАЧЕМ: честно закрыть accepted abstract performance angle без неподкреплённого marketing claim.

СКАЗАТЬ: repository has a dedicated BenchmarkDotNet hot-path suite that measures prepared artifacts separately from parsing/compilation. Но presentation не публикует число без exact raw artifact bound to this revision. Extensibility still costs contracts, diagnostics, tests, startup/materialization and all normal compiler work.

ПЕРЕХОД: strongest counterargument определяет, где planner вообще применять нельзя.

НЕ ПЕРЕОБЕЩАТЬ: не повторять “within 10%” или “0 B” на сцене без raw current evidence artifact.` ,
  m13: `ЗАЧЕМ: защитить applicability boundary против LLVM/MLIR/DI вопросов.

СКАЗАТЬ: local IR legality belongs to MLIR-style legalization; known pass order belongs to pass manager; provider wiring belongs to DI. Whole-language planner оправдан только для expressed hard constraints across independently owned language/compiler components.

ПЕРЕХОД: финал сжимает весь talk в одну decision rule.

НЕ ПЕРЕОБЕЩАТЬ: planner не заменяет LLVM, MLIR, DI или handwritten compiler pipeline.` ,
  m14: `ЗАЧЕМ: оставить один переносимый вывод.

СКАЗАТЬ: resolve globally only what correctness cannot own locally. Fixed compiler — wire explicitly. Hard cross-owner obligation — make it part of feasibility. Several feasible implementations — only then apply preference. Execution — follow one frozen concrete plan.

ПЕРЕХОД: Q&A can go into current UT limitations, parity tests, route Cost or prior-art boundary.

НЕ ПЕРЕОБЕЩАТЬ: не расширять thesis до universal architecture.` ,
  a1: `Technical appendix: current UT structural route and proposed obligation-first planner boundary.`,
  a2: `Technical appendix: mandatory vs optional is not source-target equality.`,
  a3: `Technical appendix: selected contribution is not necessarily executed.`,
  a4: `Technical appendix: nominal artifact identity is not enough semantic state.`,
  a5: `Technical appendix: IR stage contracts already demonstrate requires/produces/preserves/invalidates locally.`,
  a6: `Technical appendix: deterministic tie-break supports reproducibility, not semantic equivalence.`,
  a7: `Technical appendix: planning and runtime performance claims need bound measurements.`,
  a8: `Technical appendix: strongest objection and narrow justification for planner.`
});