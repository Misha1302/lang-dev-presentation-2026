(() => {
  const TOPICS = Object.freeze({
    why: '1/5 · WHY EXTENSIBILITY?',
    compose: '2/5 · COMPOSE ONE LANGUAGE',
    disappear: '3/5 · MAKE ABSTRACTIONS DISAPPEAR',
    knowledge: '4/5 · KEEP SEMANTIC KNOWLEDGE',
    justify: '5/5 · DOES THE NEW LAYER EARN ITS COST?'
  });

  const CUES = Object.freeze({
    m1: [TOPICS.why, ['different people build language pieces', 'one concrete compiler, still optimized', 'AUTHOR → RESOLVE → OPTIMIZE']],
    m2: [TOPICS.why, ['monolith is often the better default', 'extensibility adds real complexity', 'pay for it only when reuse matters']],
    m3: [TOPICS.why, ['one feature crosses many compiler layers', 'arrays are the simple example', 'copying duplicates vertical slices']],
    r1: [TOPICS.why, ['languages really do evolve', '1,002 repos · 226 developed languages', 'question: when is reuse worth its cost?']],
    r2: [TOPICS.why, ['clone-and-own is cheap at first', 'a reusable platform costs more up front', 'later savings are not guaranteed']],
    r3: [TOPICS.why, ['pricing language + several variants', 'clone-and-own vs UniversalToolchain', 'workload and oracle frozen first']],
    r4: [TOPICS.why, ['marginal: UT 19 vs clone 35 SLOC', 'total: UT 105 vs clone 61 SLOC', 'marginal crossover ≠ total crossover']],
    r5: [TOPICS.why, ['expected composition win disappeared', 'both changed 1 site · 7 LOC', 'a normal shared utility was enough']],

    m5: [TOPICS.compose, ['capability = reusable language piece', 'it may span several compiler stages', 'authored against shared public contracts']],
    m7: [TOPICS.compose, ['capability = ingredient', 'profile = one concrete recipe', '.wistdialect is not an MLIR dialect']],
    m11: [TOPICS.compose, ['authors share ecosystem contracts', 'no private A ↔ B integration API', 'conflicts may still reject composition']],
    m12: [TOPICS.compose, ['profile says WHAT', 'planner decides HOW', 'dependencies · providers · conflicts · routes']],
    r6: [TOPICS.compose, ['shared downstream reuse helps both designs', 'common IR is not language extensibility', 'keep the responsibility boundary clear']],
    m13: [TOPICS.compose, ['MLIR already provides strong mechanisms', 'I am not trying to replace MLIR', 'my scope is whole-language resolution']],
    m15: [TOPICS.compose, ['request → resolve → plan → execute', 'UT already implements this boundary', 'one profile gets one inspectable answer']],
    m19: [TOPICS.compose, ['cost 2 route looks attractive', 'hard ordering makes it impossible', 'cost 10 wins because it is valid']],
    m20: [TOPICS.compose, ['FEASIBILITY FIRST', 'PREFERENCE SECOND', 'structural validity ≠ semantic correctness']],
    m21: [TOPICS.compose, ['resolve the language once', 'freeze this composition answer', 'repeat only per-program compiler work']],

    m25: [TOPICS.disappear, ['local legality is enough here', 'three AIR operations become one', 'erase machinery when enough is known']],
    r7: [TOPICS.disappear, ['reuse economics is measured', 'semantic evidence is a different question', 'experiment 1 does not prove experiment 2']],
    m26: [TOPICS.disappear, ['the pattern can stay local', 'the proof may live somewhere else', 'now we need reusable semantic evidence']],

    m28: [TOPICS.knowledge, ['bounds check is the running example', 'the array access is local', 'the proof of safety is not']],
    m29: [TOPICS.knowledge, ['range gives 0 ≤ i < N', 'extent gives N = Length(a)', 'consumer really asks: SafeIndex?']],
    m30: [TOPICS.knowledge, ['make SafeIndex(a, i) an explicit query', 'five result states, not just yes/no', 'uncertainty must not become permission']],
    m31: [TOPICS.knowledge, ['facts must describe the same situation', 'subject · context · revision · assumptions', 'stale evidence is dangerous']],
    m32: [TOPICS.knowledge, ['independence problem returns at knowledge level', 'producer and consumer meet through a contract', 'avoid private analysis APIs']],
    m33: [TOPICS.knowledge, ['LLVM and MLIR are strong baselines', 'queries and invalidation are not new', 'a shared layer must beat local mechanisms']],
    m34: [TOPICS.knowledge, ['hypothesis: share the evidence lifecycle', 'analyses can remain specialized', 'test coupling reduction without losing safety']],
    m35: [TOPICS.knowledge, ['modularity is not soundness', 'zero consumer edits is only a metric', 'unknown or conflicting evidence fails closed']],
    m36: [TOPICS.knowledge, ['test a second semantic domain: writes', 'operation semantics ≠ lowering obligations', 'GC write barrier is not just “writable”']],
    m39: [TOPICS.knowledge, ['a typed fact can still become stale', 'transformations change what the fact refers to', 'identity and context are required']],
    m40: [TOPICS.knowledge, ['Judgement = proposition + usable context', 'revision · assumptions · supporting evidence', 'freshness and provenance are part of the answer']],
    m41: [TOPICS.knowledge, ['Obligation belongs to the transformation', 'producers may supply evidence', 'no sufficient proof → no transformation']],
    m43: [TOPICS.knowledge, ['representation can change completely', 'the original node may disappear', 'representation and knowledge are separate axes']],
    m45: [TOPICS.knowledge, ['transport it', 're-analyse it', 'or invalidate it — never silently carry it']],

    m48: [TOPICS.justify, ['prior art sets a very high bar', 'CompCert · validation · Alive2', 'the remaining claim must be narrow and empirical']],
    m49: [TOPICS.justify, ['strongest alternative: build no new layer', 'use LLVM · MLIR · local adapters', 'negative result is a useful result']],
    m50: [TOPICS.justify, ['compare both architectures directly', 'add a producer without consumer edits', 'measure safety, precision, and integration cost']],
    m52: [TOPICS.justify, ['AUTHOR → RESOLVE → OPTIMIZE', 'remove machinery, keep useful meaning', 'open question: does the lifecycle earn its complexity?']]
  });

  const topic = document.createElement('div');
  topic.className = 'presenter-topic-memory';
  topic.hidden = true;
  topic.setAttribute('aria-live', 'polite');

  const cues = document.createElement('aside');
  cues.className = 'presenter-slide-memory';
  cues.hidden = true;
  cues.setAttribute('aria-label', 'Memory cues for the current slide');

  document.body.append(topic, cues);

  let scheduled = false;
  function scheduleUpdate() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      update();
    });
  }

  function update() {
    const slide = document.querySelector('.slide.active');
    const data = CUES[slide?.dataset.noteKey || ''];
    const visible = Boolean(data);

    topic.hidden = !visible;
    cues.hidden = !visible;
    if (!visible) return;

    topic.textContent = data[0];
    cues.replaceChildren();
    const list = document.createElement('ul');
    for (const text of data[1]) {
      const item = document.createElement('li');
      item.textContent = text;
      list.appendChild(item);
    }
    cues.appendChild(list);
  }

  const observer = new MutationObserver(scheduleUpdate);
  observer.observe(document.body, {
    subtree: true,
    attributes: true,
    attributeFilter: ['class']
  });

  window.addEventListener('hashchange', scheduleUpdate);
  window.addEventListener('resize', scheduleUpdate);
  document.addEventListener('keydown', scheduleUpdate);
  document.addEventListener('click', scheduleUpdate);
  scheduleUpdate();
})();
