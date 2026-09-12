(() => {
  const deck = document.getElementById('deck');
  if (!deck) return;

  const byKey = (key) => deck.querySelector(`[data-note-key="${key}"]`);
  const replaceSlide = (key, html) => {
    const slide = byKey(key);
    if (!slide) return false;
    slide.outerHTML = html.trim();
    return true;
  };

  const moveBefore = (keys, beforeKey) => {
    const anchor = byKey(beforeKey);
    if (!anchor) return;
    for (const key of keys) {
      const slide = byKey(key);
      if (slide) deck.insertBefore(slide, anchor);
    }
  };

  replaceSlide('m1', `
<section class="slide center" data-kind="main" data-note-key="m1">
  <div class="slidehead">
    <div class="eyebrow">LangDev 2026 · research test first</div>
    <h2>Can one new plugin make an old optimizer smarter?</h2>
  </div>
  <div class="hero">
    <p class="bigq">Add a producer. Change zero consumers. Make an existing optimizer stronger.</p>
    <p class="memory">Can an extensible compiler do this safely?</p>
  </div>
</section>`);

  replaceSlide('m2', `
<section class="slide two" data-kind="main" data-note-key="m2">
  <div class="slidehead">
    <div class="eyebrow">The real scaling problem</div>
    <h2>The hard dependency is not a call. It is pairwise knowledge.</h2>
  </div>
  <div class="panel broken">
    <h3>Consumer-specific integration</h3>
    <p class="bigq">worst case Θ(N × M)</p>
    <p>Every consumer learns every producer's private API or adapter shape.</p>
  </div>
  <div class="panel good">
    <h3>Contract-bound integration</h3>
    <p class="bigq">fixed-contract Θ(N + M)</p>
    <p>A conforming producer should require no work proportional to existing consumers.</p>
  </div>
  <p class="caption span2 centertext">This is not “O(1) plugin development”: schema evolution, adapters, tests and governance still cost real work.</p>
</section>`);

  moveBefore(['m28', 'm29', 'm30', 'm31', 'm32', 'm33', 'm34', 'm35'], 'm3');

  replaceSlide('m3', `
<section class="slide stack" data-kind="main" data-note-key="m3">
  <div class="slidehead">
    <div class="eyebrow">Prior art is already strong</div>
    <h2>Most pieces exist. The intersection still has to earn its complexity.</h2>
  </div>
  <div class="ownerflow">
    <div class="role"><b>MLIR / LLVM</b><span>interfaces · dataflow · legality · invalidation</span></div>
    <i>+</i>
    <div class="role"><b>JastAdd / Neverlang</b><span>modular language semantics and feature composition</span></div>
    <i>+</i>
    <div class="role"><b>Abstract interpretation</b><span>analysis combination / reduced products</span></div>
  </div>
  <p class="memory">The target is not “plugins” or “queries”. The target is open semantic evidence under transformation.</p>
</section>`);

  replaceSlide('m5', `
<section class="slide two" data-kind="main" data-note-key="m5">
  <div class="slidehead">
    <div class="eyebrow">What ideal UT may actually contribute</div>
    <h2>Local extension. Global semantic reasoning. Concrete compiler.</h2>
  </div>
  <div class="panel good">
    <h3>Current UT witness</h3>
    <p>LanguageDefinition → LanguageCompiler → immutable LanguagePlan → LanguageRuntime</p>
    <p>Coarse facts/effects already use requires · produces · preserves · invalidates.</p>
  </div>
  <div class="panel">
    <h3>Ideal UT target</h3>
    <p>Validity-scoped semantic evidence with subject identity, provenance, assumptions, correspondence and invalidation across representations.</p>
  </div>
</section>`);

  replaceSlide('m7', `
<section class="slide two" data-kind="main" data-note-key="m7">
  <div class="slidehead">
    <div class="eyebrow">Do not sell the wrong thing</div>
    <h2>Three mechanisms, not three marketing promises</h2>
  </div>
  <div class="panel">
    <h3>Mechanisms</h3>
    <p>1. contract-bound composition<br/>2. semantic evidence lifecycle<br/>3. resolve / freeze / specialize</p>
  </div>
  <div class="panel good">
    <h3>Payoffs</h3>
    <p>fewer pairwise integrations<br/>cross-plugin optimization opportunities<br/>rapid profiles without permanent runtime tax</p>
  </div>
  <p class="caption span2 centertext">Main-stage claims must stay weaker than the evidence: no “zero overhead”, no “universal semantics”, no unqualified “O(1)”.</p>
</section>`);

  replaceSlide('m11', `
<section class="slide center" data-kind="main" data-note-key="m11">
  <div class="slidehead">
    <div class="eyebrow">The defensible central question</div>
    <h2>Can independently authored compiler components compose what they know — not just what they execute?</h2>
  </div>
  <div class="mapflow horizontal">
    <div>INDEPENDENT PRODUCERS</div><i>→</i><div class="good">VALIDITY-SCOPED EVIDENCE</div><i>→</i><div>INDEPENDENT CONSUMERS</div>
  </div>
  <p class="caption centertext">Open-world implementations still need shared propositions, adapters or inference rules. Unknown semantics do not compose magically.</p>
</section>`);

  replaceSlide('m12', `
<section class="slide center" data-kind="main" data-note-key="m12">
  <div class="slidehead">
    <div class="eyebrow">Then close the world deliberately</div>
    <h2>Resolve the open ecosystem into one inspectable compiler answer.</h2>
  </div>
  <div class="decisionrule">
    <div><b>OPEN INPUT</b><span>capabilities · providers · routes · evidence · policy · targets</span></div>
    <div class="good"><b>FROZEN OUTPUT</b><span>LanguagePlan · obligations · selected components · executable path</span></div>
  </div>
  <p class="caption centertext">Pay orchestration before repeated execution where the decision is static; program-specific compiler work still remains.</p>
</section>`);

  replaceSlide('m13', `
<section class="slide two" data-kind="main" data-note-key="m13">
  <div class="slidehead">
    <div class="eyebrow">The strongest comparison</div>
    <h2>Why not just MLIR plus local adapters?</h2>
  </div>
  <div class="panel good">
    <span class="boundary analogy">MLIR already gives us</span>
    <p>dialects · interfaces / external models · effects · dataflow · conversion legality · Transform dialect</p>
  </div>
  <div class="panel">
    <span class="boundary target">UT must earn this delta</span>
    <p class="bigq">Evidence across heterogeneous representations and engines that are not required to share one program-IR meta-model.</p>
  </div>
  <p class="caption span2 centertext">MLIR can be a provider inside the plan. The claim is a responsibility boundary, not an incapability claim.</p>
</section>`);

  replaceSlide('m35', `
<section class="slide two" data-kind="main" data-note-key="m35">
  <div class="slidehead">
    <div class="eyebrow">Make the architecture able to lose</div>
    <h2>Add a producer. Change zero consumers. That is a test, not a theorem.</h2>
  </div>
  <div class="panel good">
    <h3>Success signal</h3>
    <p>new semantic producer<br/>existing optimizer unchanged<br/>more valid optimizations found</p>
  </div>
  <div class="panel broken">
    <h3>Failure signal</h3>
    <p>consumer-specific adapter required<br/>stale evidence used<br/>semantic layer costs more than coupling removed</p>
  </div>
  <p class="caption span2 centertext">If MLIR + explicit adapters or reduced products win on safety, precision and cost, the UT meta-layer loses this scenario.</p>
</section>`);
})();
