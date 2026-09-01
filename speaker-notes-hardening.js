Object.assign(window.SPEAKER_NOTES, {
  "m1": "ЗАЧЕМ: дать аудитории одну простую mental model на весь доклад.\n\nСКАЗАТЬ: язык может быть расширяемым, пока мы его собираем, но перед исполнением глобальные choices превращаются в конкретный LanguagePlan. Runtime исполняет уже выбранную конфигурацию, а не заново решает composition на каждом Run.\n\nПЕРЕХОД: сначала покажу сильнейший baseline — обычный pipeline руками.\n\nНЕ ПЕРЕОБЕЩАТЬ: это не zero-cost claim и не обещание, что interfaces, objects или dispatch исчезнут.",

  "m2": "ЗАЧЕМ: сразу признать, что planner нужен далеко не всегда.\n\nСКАЗАТЬ: если один владелец заранее знает parser, lowering, optimizations и backend, явный pipeline проще и прозрачнее. Я бы начинал именно с него.\n\nПЕРЕХОД: проблема появляется, когда продукт — уже не один фиксированный язык.\n\nНЕ ПЕРЕОБЕЩАТЬ: не называть ручную композицию примитивной или устаревшей.",

  "m3": "ЗАЧЕМ: объяснить, зачем вообще нужна language extensibility.\n\nСКАЗАТЬ: иногда один codebase должен собирать семейство связанных языков. В Wist есть, например, minimal arithmetic, restricted pricing и full default — они переиспользуют общую инфраструктуру, но дают разные concrete languages.\n\nПЕРЕХОД: сначала это всё ещё выглядит как обычная конфигурация.\n\nНЕ ПЕРЕОБЕЩАТЬ: не говорить про inheritance диалектов — здесь речь о разных definitions/presets.",

  "m4": "ЗАЧЕМ: показать, что flags и builder — нормальная первая архитектура.\n\nСКАЗАТЬ: пока features, backend, optimizers и policies выбираются независимо, planner не нужен. Обычные options или builder полностью достаточны.\n\nПЕРЕХОД: перелом происходит тогда, когда эти choices начинают зависеть друг от друга.\n\nНЕ ПЕРЕОБЕЩАТЬ: не изображать DI или builder как плохие решения сами по себе.",

  "m5": "ЗАЧЕМ: сформулировать центральный reasoning step доклада.\n\nСКАЗАТЬ: configuration становится planning, когда options перестают быть независимыми: feature требует feature, capability имеет несколько providers, contributions конфликтуют или требуют ordering, backend требует route, runtime должен поддержать выбранный plan. Теперь ответ зависит от языка целиком.\n\nПЕРЕХОД: возникает вопрос — кто вообще имеет право принять это whole-language решение?\n\nНЕ ПЕРЕОБЕЩАТЬ: planner решает только явно выраженные constraints.",

  "m6": "ЗАЧЕМ: разделить ownership локальных компонентов и глобального решения.\n\nСКАЗАТЬ: package author знает локальные facts своего extension. Language integrator выбирает конкретный набор. LanguageCompiler видит всю LanguageDefinition и разрешает global composition choices.\n\nПЕРЕХОД: покажу простой failure case, который локально решить нельзя.\n\nНЕ ПЕРЕОБЕЩАТЬ: эти роли conceptual — они не обязаны быть разными компаниями или людьми.",

  "m7": "ЗАЧЕМ: показать реальную неоднозначность вместо абстрактных A/B.\n\nСКАЗАТЬ: consumer требует capability, а два providers подходят одинаково. Порядок регистрации не должен молча решать policy, поэтому compiler выдаёт UTL2002. Integrator явно выбирает provider через PreferCapabilityProvider.\n\nПЕРЕХОД: provider ambiguity — только один тип глобального решения; второй важный тип — artifact routing.\n\nНЕ ПЕРЕОБЕЩАТЬ: explicit preference не означает, что planner знает семантически лучший provider.",

  "m8": "ЗАЧЕМ: показать, что backend selection тоже требует whole-language view.\n\nСКАЗАТЬ: backend usable только если от текущего artifact существует type-compatible цепочка transformations до его input contract. Planner выбирает route, а LanguagePlan сохраняет ordered steps и route cost.\n\nПЕРЕХОД: теперь можно посмотреть на результат planning как на конкретные данные.\n\nНЕ ПЕРЕОБЕЩАТЬ: route cost — planning metric, а не измеренная runtime latency.",

  "m9": "ЗАЧЕМ: сделать LanguagePlan конкретным и понятным.\n\nСКАЗАТЬ: после planning в plan уже записаны resolved features, contributions, runtime provider, routes, PlanHash и summary. То есть глобальные composition choices уже разрешены; runtime не получает мешок будущих вариантов.\n\nПЕРЕХОД: если plan уже concrete, можно провести точную границу между composition и execution.\n\nНЕ ПЕРЕОБЕЩАТЬ: PlanHash — identity/canonical representation конфигурации, не semantic equivalence и не security proof.",

  "m10": "ЗАЧЕМ: показать staging boundary во времени.\n\nСКАЗАТЬ: authoring оставляет possibilities открытыми; composition создаёт LanguagePlan; runtime creation проверяет exact binding и materializes planned components; затем идут request #1, #2, ... #N. Runtime validation есть, но она не открывает global choices заново.\n\nПЕРЕХОД: это можно увидеть на одном маленьком source-backed demo.\n\nНЕ ПЕРЕОБЕЩАТЬ: runtime всё ещё выполняет verification и другую работу.",

  "m11": "ЗАЧЕМ: показать архитектуру на реальном Wist path, а не только схемами.\n\nСКАЗАТЬ: берём настоящий MinimalArithmetic definition, один раз строим LanguagePlan, создаём LanguageRuntime и запускаем два выражения. Получаем 42 и 42, используя тот же plan/runtime.\n\nПЕРЕХОД: из этого примера можно обобщить главный architectural pattern.\n\nНЕ ПЕРЕОБЕЩАТЬ: demo доказывает staging и reuse, но это не benchmark.",

  "m12": "ЗАЧЕМ: сформулировать takeaway после concrete example.\n\nСКАЗАТЬ: Extensible at composition time. Concrete at execution time. Гибкость построения языка не требует, чтобы repeated execution оставалось global dynamic composition problem.\n\nПЕРЕХОД: важно точно сказать, что именно стало concrete, а что осталось runtime abstraction.\n\nНЕ ПЕРЕОБЕЩАТЬ: concrete execution не означает zero runtime overhead.",

  "m13": "ЗАЧЕМ: не дать слову deabstraction превратиться в performance marketing.\n\nСКАЗАТЬ: исчезнуть из hot path может нерешённый вопрос — какой provider, route, ordering или runtime выбрать. Но interfaces, objects, indirect calls, validation и allocations вполне могут остаться.\n\nПЕРЕХОД: поэтому performance нужно обсуждать как четыре разные стадии.\n\nНЕ ПЕРЕОБЕЩАТЬ: planning не гарантирует JIT devirtualization или specialization.",

  "m14": "ЗАЧЕМ: честно разложить стоимость extensibility.\n\nСКАЗАТЬ: отдельно есть planning, runtime creation, first execution и steady state. Наш архитектурный тезис только в том, что steady state не обязан повторять global re-planning. Численных claims без exact-current benchmark artifact я не делаю.\n\nПЕРЕХОД: кроме performance есть ещё более важная граница — что planner способен доказать по correctness.\n\nНЕ ПЕРЕОБЕЩАТЬ: no re-planning не равно zero overhead и не означает, что UniversalToolchain быстрее handwritten pipeline.",

  "m15": "ЗАЧЕМ: поставить жёсткую correctness/security boundary.\n\nСКАЗАТЬ: planner может проверить expressed structure: dependencies, conflicts, capabilities, ordering, artifact contracts и runtime/backend coverage. Но valid plan не доказывает semantic interchangeability, behavioral correctness, security, sandboxing или performance optimality.\n\nПЕРЕХОД: остаётся один практический вопрос — когда вообще стоит брать такую архитектуру.\n\nНЕ ПЕРЕОБЕЩАТЬ: structural compatibility не превращать в semantic proof.",

  "m16": "ЗАЧЕМ: закончить decision rule, а не лозунгом про сложность framework.\n\nСКАЗАТЬ: используйте самого простого owner, который способен корректно принять whole-system decision. Если один owner знает всё — wire by hand. Если независимые pieces создают global choices — resolve them once into a concrete plan.\n\nПЕРЕХОД: дальше Q&A и appendix с evidence.\n\nНЕ ПЕРЕОБЕЩАТЬ: UniversalToolchain — один design point, а не универсальная замена builder, DI и ручному pipeline."
});

function formatSpeakerNote(note) {
  return String(note || '')
    .replace(/\s+(?=(?:ЗАЧЕМ|СКАЗАТЬ|ПЕРЕХОД|ДЕТАЛЬ|НЕ ПЕРЕОБЕЩАТЬ):)/g, '\n\n')
    .trim();
}

for (const key of Object.keys(window.SPEAKER_NOTES)) {
  window.SPEAKER_NOTES[key] = formatSpeakerNote(window.SPEAKER_NOTES[key]);
}

for (const slide of document.querySelectorAll('.slide[data-note-key]')) {
  slide.dataset.notes = window.SPEAKER_NOTES[slide.dataset.noteKey] || '';
}
