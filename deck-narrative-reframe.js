(() => {
  const deck = document.getElementById('deck');
  if (!deck) return;

  const byKey = key => deck.querySelector(`.slide[data-note-key="${key}"]`);

  const replaceSlide = (key, html) => {
    const slide = byKey(key);
    if (!slide) throw new Error(`Final narrative: missing slide ${key}`);
    slide.outerHTML = html.trim();
  };

  const addSlide = (key, html) => {
    if (byKey(key)) throw new Error(`Final narrative: duplicate slide ${key}`);
    deck.insertAdjacentHTML('beforeend', html.trim());
  };

  replaceSlide('m1', `
<section class="slide center fn-title" data-kind="main" data-note-key="m1">
  <div class="slidehead">
    <div class="eyebrow">LangDev 2026 · UniversalToolchain</div>
    <h2>Build the Language.<br/><span class="accent">Then Make the Abstractions Disappear.</span></h2>
  </div>
  <div class="hero">
    <p class="bigq">How can independently developed language pieces become one concrete compiler without giving up serious optimization?</p>
    <p class="talk-thesis">Author reusable pieces. Resolve one compiler. Reuse only semantic knowledge that is still valid.</p>
    <p class="memory">AUTHOR → RESOLVE → OPTIMIZE</p>
  </div>
</section>`);

  replaceSlide('m2', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="m2">
  <div class="slidehead">
    <div class="eyebrow">Motivation</div>
    <h2>Extensibility is worth paying for only when the language keeps diverging.</h2>
  </div>
  <div class="panel fn-equal-card good">
    <h3>Prefer the monolith</h3>
    <p class="fn-card-lead">one language · one owner</p>
    <p>Stable targets and roadmap. Direct code is simpler and cheaper.</p>
  </div>
  <div class="panel fn-equal-card">
    <h3>Extensibility starts to matter</h3>
    <p class="fn-card-lead">related languages · independent extensions</p>
    <p>The same feature keeps cutting across parser, analysis, lowering, optimization and tooling.</p>
  </div>
  <p class="caption span2 centertext">The default is not “use UT”. The question is when repeated variation earns the extra infrastructure.</p>
</section>`);

  addSlide('nProblem', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="nProblem">
  <div class="slidehead">
    <div class="eyebrow">Problem</div>
    <h2>Two things stop scaling together: implementation and knowledge.</h2>
  </div>
  <div class="panel fn-equal-card">
    <h3>Implementation coupling</h3>
    <p class="fn-card-lead">One feature crosses many compiler stages.</p>
    <p>Forking a language duplicates a vertical slice; a local plugin hook is often too small.</p>
  </div>
  <div class="panel fn-equal-card">
    <h3>Semantic coupling</h3>
    <p class="fn-card-lead">One optimizer needs facts produced somewhere else.</p>
    <p>Private producer APIs turn each new analysis × consumer pair into another integration.</p>
  </div>
  <p class="memory span2">We need to compose both what extensions <b>do</b> and what they <b>know</b>.</p>
</section>`);

  addSlide('nSolutions', `
<section class="slide stack" data-kind="main" data-note-key="nSolutions">
  <div class="slidehead">
    <div class="eyebrow">Existing solutions</div>
    <h2>Most of the ingredients already exist — in different architecture boundaries.</h2>
  </div>
  <div class="fn-solution-grid">
    <div class="panel fn-solution-card"><span class="boundary analogy">MLIR</span><h3>Extensible IR world</h3><p>dialects · interfaces · data-flow · effects · conversion legality</p></div>
    <div class="panel fn-solution-card"><span class="boundary analogy">MPS / Neverlang</span><h3>Language composition</h3><p>language modules · generators · global ordering / products</p></div>
    <div class="panel fn-solution-card"><span class="boundary analogy">LLVM New PM</span><h3>Analysis lifecycle</h3><p>cached analyses · preservation · invalidation · pass pipelines</p></div>
    <div class="panel fn-solution-card"><span class="boundary analogy">Graal / Truffle</span><h3>Interop + specialization</h3><p>common runtime protocol · self-specializing language implementations</p></div>
  </div>
  <p class="caption centertext">UT must justify the gap between these boundaries — not rename mechanisms that already exist.</p>
</section>`);

  addSlide('nMatrix', `
<section class="slide stack fn-matrix-slide" data-kind="main" data-note-key="nMatrix">
  <div class="slidehead">
    <div class="eyebrow">Comparison matrix</div>
    <h2>Compare systems by the boundary they make first-class.</h2>
  </div>
  <div class="fn-matrix" role="table" aria-label="Comparison of related compiler and language systems">
    <div class="fn-matrix-cell fn-head">System</div>
    <div class="fn-matrix-cell fn-head">Solves well</div>
    <div class="fn-matrix-cell fn-head">Boundary / limitation for this problem</div>
    <div class="fn-matrix-cell fn-head">Role in this talk</div>

    <div class="fn-matrix-cell fn-system">MLIR</div>
    <div class="fn-matrix-cell">extensible IR, interfaces, transformations</div>
    <div class="fn-matrix-cell">all participating program IR lives in the MLIR object model</div>
    <div class="fn-matrix-cell fn-strong">strongest in-IR baseline</div>

    <div class="fn-matrix-cell fn-system">MPS / Neverlang</div>
    <div class="fn-matrix-cell">language modules, products, generator planning</div>
    <div class="fn-matrix-cell">framework-specific language / model substrate</div>
    <div class="fn-matrix-cell fn-strong">strongest language-composition baseline</div>

    <div class="fn-matrix-cell fn-system">LLVM New PM</div>
    <div class="fn-matrix-cell">analysis lookup, preservation, invalidation</div>
    <div class="fn-matrix-cell">analysis lifecycle inside one LLVM-IR ecosystem</div>
    <div class="fn-matrix-cell fn-strong">strongest local evidence baseline</div>

    <div class="fn-matrix-cell fn-system">Graal / Truffle</div>
    <div class="fn-matrix-cell">common runtime interop + specialization</div>
    <div class="fn-matrix-cell">runtime values and execution, not compile-time proof evidence</div>
    <div class="fn-matrix-cell">useful common-protocol analogy</div>

    <div class="fn-matrix-cell fn-system fn-ut">Ideal UT</div>
    <div class="fn-matrix-cell fn-ut">whole compiler plan + cross-representation evidence</div>
    <div class="fn-matrix-cell fn-ut">research hypothesis; no result yet</div>
    <div class="fn-matrix-cell fn-ut"><b>must beat explicit adapters without weakening correctness</b></div>
  </div>
</section>`);

  addSlide('nExternalBench', `
<section class="slide stack fn-external-bench" data-kind="main" data-note-key="nExternalBench">
  <div class="slidehead">
    <div class="eyebrow">External benchmark · EuroLLVM 2024</div>
    <h2>Extensibility has measurable compiler-side overhead — so “zero cost” must be measured, not assumed.</h2>
  </div>
  <div class="fn-benchmark-grid">
    <div class="panel fn-benchmark-card"><h3>IR traversal</h3><p class="fn-bench-number">0.35 ns/op</p><p>flat <code>std::vector</code></p><p class="fn-vs">vs</p><p class="fn-bench-number">6.11 ns/op</p><p>MLIR <code>walk</code>, no regions</p></div>
    <div class="panel fn-benchmark-card"><h3>Interface lookup</h3><p class="fn-bench-number">2.16 ns/op</p><p>operation <code>dyn_cast</code></p><p class="fn-vs">vs</p><p class="fn-bench-number">9.68 ns/op</p><p>successful interface <code>dyn_cast</code></p></div>
    <div class="panel fn-benchmark-card good"><h3>What this tells us</h3><p class="fn-card-lead">Abstraction cost is real.</p><p>UT must measure compile-time and memory overhead as well as engineering reuse.</p></div>
  </div>
  <p class="caption centertext"><b>Amini &amp; Niu, “How Slow is MLIR?”, EuroLLVM 2024.</b> Their slides explicitly frame these as microbenchmarks for intuition; this is not a UT-vs-MLIR performance comparison.</p>
  <div class="sourcebar"><a href="https://llvm.org/devmtg/2024-04/slides/Keynote/Amini-Niu-HowSlowIsMLIR.pdf" rel="noreferrer" target="_blank">LLVM Foundation / EuroLLVM slides</a></div>
</section>`);

  addSlide('nOverview', `
<section class="slide stack fn-overview" data-kind="main" data-note-key="nOverview">
  <div class="slidehead">
    <div class="eyebrow">Solution overview · high level</div>
    <h2>UT separates three questions that ordinary plugin APIs often mix together.</h2>
  </div>
  <div class="cards3 fn-overview-cards">
    <div class="panel"><span class="fn-status fn-design">DESIGN</span><h3>AUTHOR</h3><p>Publish reusable language / compiler pieces against stable ecosystem contracts.</p></div>
    <div class="panel good"><span class="fn-status fn-current">CURRENT UT</span><h3>RESOLVE</h3><p>Turn one language request into selected providers, routes, constraints and one inspectable compiler plan.</p></div>
    <div class="panel"><span class="fn-status fn-hypothesis">HYPOTHESIS</span><h3>OPTIMIZE</h3><p>Let independent modules exchange validity-scoped semantic evidence so later transformations can specialize safely.</p></div>
  </div>
  <p class="memory">Author locally → resolve globally → prove before specializing.</p>
</section>`);

  replaceSlide('m7', `
<section class="slide stack fn-status-slide" data-kind="main" data-note-key="m7">
  <div class="slidehead">
    <div class="eyebrow">Research status</div>
    <h2>This is a research program, not a finished theorem.</h2>
  </div>
  <div class="cards3 fn-overview-cards">
    <div class="panel good"><span class="fn-status fn-current">CURRENT UT</span><h3>Implemented witnesses</h3><p>artifact routes · LanguagePlan · planner regression · bounded local deabstraction</p></div>
    <div class="panel"><span class="fn-status fn-measured">MEASURED</span><h3>Small DSL-evolution study</h3><p>mixed engineering-work result · negative propagation result · shared-pipeline control</p></div>
    <div class="panel"><span class="fn-status fn-hypothesis">OPEN</span><h3>Main research question</h3><p>cross-component semantic evidence across heterogeneous representations, including cost and correctness</p></div>
  </div>
  <p class="caption centertext">Every later claim is marked by one of these boundaries.</p>
</section>`);

  replaceSlide('r2', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="r2">
  <div class="slidehead">
    <div class="eyebrow">Engineering-work trade-off</div>
    <h2>Reusable infrastructure costs more work up front.</h2>
  </div>
  <div class="panel fn-equal-card">
    <h3>Clone-and-own</h3>
    <p class="fn-card-lead">less setup work</p>
    <p>Each variant owns its implementation directly. Cheap for the first language; duplication may grow later.</p>
  </div>
  <div class="panel fn-equal-card good">
    <h3>Shared platform</h3>
    <p class="fn-card-lead">more setup work</p>
    <p>Later extensions can reuse contracts, planning and shared infrastructure.</p>
  </div>
  <p class="caption span2 centertext">The question is not whether the API “feels complicated”. It is whether later extension work repays the extra initial implementation work.</p>
</section>`);

  replaceSlide('r3', `
<section class="slide stack" data-kind="main" data-note-key="r3">
  <div class="slidehead">
    <div class="eyebrow">Experiment 1 · frozen before implementation</div>
    <h2>We measured implementation work on the same language changes.</h2>
  </div>
  <div class="ownerflow"><div class="role"><b>CONTROL</b><span>one fixed pricing language</span></div><i>→</i><div class="role"><b>CLONE &amp; OWN</b><span>discount · surcharge · combined</span></div><i>↔</i><div class="role good"><b>UT COMPOSITION</b><span>same behavior oracle · current SDK</span></div></div>
  <div class="panel"><p><b>Frozen changes:</b> E1 discount → E2 surcharge / combined variant → E3 shared percentage-range rule.</p><p class="caption">Same parser/model and treatment-neutral behavior oracle. Negative or mixed outcomes were accepted before implementation.</p></div>
  <div class="sourcebar"><a href="https://github.com/Misha1302/UniversalToolchain/tree/research/dsl-evolution-experiment-2026-09-08/experiments/dsl-evolution-study" rel="noreferrer" target="_blank">Reproducible experiment, raw results and scripts</a></div>
</section>`);

  replaceSlide('r4', `
<section class="slide two fn-balanced-pair fn-economics-slide" data-kind="main" data-note-key="r4">
  <div class="slidehead">
    <div class="eyebrow">Measured result · E2</div>
    <h2>UT needed less work for the second extension — but more work overall.</h2>
  </div>
  <div class="panel fn-equal-card good">
    <h3>Work to add the second extension</h3>
    <p class="fn-number-line"><b>UT</b> 19 SLOC</p>
    <p class="fn-number-line"><b>clone-and-own</b> 35 SLOC</p>
  </div>
  <div class="panel fn-equal-card broken">
    <h3>Total implementation so far</h3>
    <p class="fn-number-line"><b>UT</b> 105 SLOC</p>
    <p class="fn-number-line"><b>clone-and-own</b> 61 SLOC</p>
  </div>
  <p class="memory span2">MORE INITIAL WORK ↔ LESS WORK FOR THIS EXTENSION</p>
  <p class="caption span2 centertext"><span class="fn-status fn-measured">MEASURED</span> Break-even was <b>not</b> reached in this experiment.</p>
  <div class="sourcebar span2"><a href="https://github.com/Misha1302/UniversalToolchain/blob/research/dsl-evolution-experiment-2026-09-08/internal-docs/research/dsl-evolution-study/RESULTS.md" rel="noreferrer" target="_blank">Measured study results</a></div>
</section>`);

  replaceSlide('r5', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="r5">
  <div class="slidehead">
    <div class="eyebrow">Measured result · E3</div>
    <h2>The expected maintenance advantage did not appear.</h2>
  </div>
  <div class="panel fn-equal-card">
    <h3>Clone-and-own</h3><p class="fn-number-line">1 logical site</p><p>1 file · 7 changed LOC</p>
  </div>
  <div class="panel fn-equal-card good">
    <h3>UT composition</h3><p class="fn-number-line">1 logical site</p><p>1 file · 7 changed LOC</p>
  </div>
  <p class="memory span2">A fair shared utility erased the expected propagation advantage.</p>
  <div class="sourcebar span2"><a href="https://github.com/Misha1302/UniversalToolchain/blob/research/dsl-evolution-experiment-2026-09-08/internal-docs/research/dsl-evolution-study/RESULTS.md" rel="noreferrer" target="_blank">H2: not supported in this workload</a></div>
</section>`);

  replaceSlide('r6', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="r6">
  <div class="slidehead">
    <div class="eyebrow">Strong control</div>
    <h2>Some reuse comes from an ordinary shared pipeline — not from UT.</h2>
  </div>
  <div class="panel fn-equal-card good"><h3>Ordinary shared pipeline</h3><p class="fn-number-line">1 site · 3 LOC</p><p>0 variant-semantic files touched</p></div>
  <div class="panel fn-equal-card"><h3>UT</h3><p class="fn-number-line">1 site · 5 LOC</p><p>0 variant-semantic files touched</p></div>
  <p class="caption span2 centertext">Both preserved the same results. Shared downstream representation is valuable, but it is not evidence that source-language composition uniquely needs UT.</p>
  <div class="sourcebar span2"><a href="https://github.com/Misha1302/UniversalToolchain/blob/research/dsl-evolution-experiment-2026-09-08/internal-docs/research/dsl-evolution-study/RQ3_RESULTS.md" rel="noreferrer" target="_blank">RQ3 control</a></div>
</section>`);

  replaceSlide('m3', `
<section class="slide stack fn-vertical-slice" data-kind="main" data-note-key="m3">
  <div class="slidehead">
    <div class="eyebrow">Concrete example · language evolution</div>
    <h2>One extension is a vertical compiler slice, not one parser hook.</h2>
  </div>
  <div class="fn-slice-track">
    <div><b>syntax</b><span><code>discount 10%</code></span></div>
    <i>→</i><div><b>validation</b><span><code>0..100%</code></span></div>
    <i>→</i><div><b>semantic model</b><span>percentage adjustment</span></div>
    <i>→</i><div><b>lowering</b><span>shared pricing IR</span></div>
    <i>→</i><div><b>execution / tooling</b><span>backend + diagnostics</span></div>
  </div>
  <p class="memory">The reusable unit must be able to own the slice.</p>
</section>`);

  replaceSlide('m5', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="m5">
  <div class="slidehead">
    <div class="eyebrow">Name the abstraction only now</div>
    <h2>A <span class="accent">Capability</span> is one reusable vertical slice.</h2>
  </div>
  <div class="panel fn-equal-card good"><h3>Capability</h3><p class="fn-card-lead">discount feature</p><p>May contribute syntax, validation, analysis, lowering, optimization, backend behavior or tooling.</p></div>
  <div class="panel fn-equal-card"><h3>Not a language</h3><p class="fn-card-lead">one reusable piece</p><p>The same capability can participate in several concrete language configurations.</p></div>
  <p class="caption span2 centertext"><span class="fn-status fn-design">GENERAL DESIGN</span> Current Wist packages are an implementation witness, not the universal definition.</p>
</section>`);

  replaceSlide('m11', `
<section class="slide two fn-balanced-pair" data-kind="main" data-note-key="m11">
  <div class="slidehead">
    <div class="eyebrow">Concrete language</div>
    <h2>A <span class="accent">Language Profile</span> chooses which capabilities become one language.</h2>
  </div>
  <div class="panel fn-equal-card"><h3>Reusable inventory</h3><p>base pricing · discount · surcharge · diagnostics · backend choices</p></div>
  <div class="panel fn-equal-card good"><h3>One profile</h3><p>selects capabilities · restrictions · policy · targets for one concrete language</p></div>
  <p class="caption span2 centertext">The profile says <b>what</b> is wanted. It does not know the globally valid route for building it.</p>
</section>`);

  replaceSlide('m12', `
<section class="slide center" data-kind="main" data-note-key="m12">
  <div class="slidehead"><div class="eyebrow">Request vs resolution</div><h2>The profile says <span class="accent">WHAT</span>.<br/>Resolution decides <span class="accent">HOW</span>.</h2></div>
  <div class="decisionrule"><div><b>PROFILE</b><span>capabilities · exclusions · policy · targets</span></div><div class="good"><b>GLOBAL RESOLUTION</b><span>providers · conflicts · ordering · representation routes · backend</span></div></div>
  <p class="caption centertext">A local extension should not have to predict every other extension that may later join the same language.</p>
</section>`);

  replaceSlide('m40', `
<section class="slide stack fn-evidence-record" data-kind="main" data-note-key="m40">
  <div class="slidehead">
    <div class="eyebrow">What must travel with a reusable fact?</div>
    <h2>Keep what the fact means — and where it is still valid.</h2>
  </div>
  <div class="fn-record-grid">
    <div class="panel"><h3>WHAT?</h3><p><code>SafeIndex(a, i)</code></p><small>the proposition</small></div>
    <div class="panel"><h3>ABOUT WHAT?</h3><p>array <code>a</code> · index <code>i</code></p><small>subject identity</small></div>
    <div class="panel"><h3>WHERE / WHEN?</h3><p>path · scope · revision</p><small>validity</small></div>
    <div class="panel"><h3>WHY?</h3><p>assumptions · producer · evidence</p><small>provenance</small></div>
  </div>
  <p class="caption centertext"><span class="fn-status fn-hypothesis">RESEARCH MODEL</span> The formal model may call this complete evidence record a <code>Judgement</code>; the noun is not needed to understand the mechanism.</p>
</section>`);

  replaceSlide('m50', `
<section class="slide stack fn-research-plan" data-kind="main" data-note-key="m50">
  <div class="slidehead">
    <div class="eyebrow">Planned study · before making stronger claims</div>
    <h2>Compare the shared evidence layer against the strongest ordinary baseline.</h2>
  </div>
  <div class="fn-study-grid">
    <div class="panel"><h3>Baseline</h3><p>MLIR / LLVM-style interfaces + domain analyses + explicit adapters + local invalidation</p></div>
    <div class="panel good"><h3>Intervention</h3><p>independent producers publish evidence through the shared lifecycle; existing consumers stay unchanged</p></div>
    <div class="panel"><h3>Correctness controls</h3><p>stale evidence · contradiction · mutation · representation change must never discharge an obligation</p></div>
    <div class="panel"><h3>Measure</h3><p>consumer edits · adapters · precision · false discharges · compile time · memory · invalidation / re-analysis · schema burden</p></div>
  </div>
  <p class="memory">If explicit adapters win on cost, precision and safety, remove the meta-layer.</p>
</section>`);

  addSlide('nRQ', `
<section class="slide stack fn-rq-slide" data-kind="main" data-note-key="nRQ">
  <div class="slidehead">
    <div class="eyebrow">What did this work actually answer?</div>
    <h2>Three research questions — three different answer states.</h2>
  </div>
  <div class="fn-rq-grid">
    <div class="panel"><span class="fn-status fn-measured">PARTIAL</span><h3>RQ1 · Does composition reduce extension work?</h3><p><b>Sometimes in the micro-study.</b> The second extension was smaller, but total implementation stayed larger and the maintenance win did not appear.</p></div>
    <div class="panel good"><span class="fn-status fn-current">BOUNDED YES</span><h3>RQ2 · Can one resolver choose a structurally valid compiler plan?</h3><p><b>Yes for the tested route/order case.</b> Hard feasibility beats cheaper invalid routes. This is not a semantic-correctness theorem.</p></div>
    <div class="panel"><span class="fn-status fn-hypothesis">OPEN</span><h3>RQ3 · Can independent modules share semantic evidence safely and profitably?</h3><p><b>Not answered yet.</b> The mechanism and falsification experiment are defined; the comparative study still has to be run.</p></div>
  </div>
</section>`);

  replaceSlide('m52', `
<section class="slide center fn-final" data-kind="main" data-note-key="m52">
  <div class="slidehead"><div class="eyebrow">Conclusion</div><h2>Author locally. Resolve globally.<br/><span class="accent">Prove before specializing.</span></h2></div>
  <div class="cards3 fn-overview-cards">
    <div class="panel"><h3>AUTHOR</h3><p>Reusable pieces only pay when language variation justifies the infrastructure.</p></div>
    <div class="panel good"><h3>RESOLVE</h3><p>Global feasibility comes before local preference; freeze one inspectable compiler plan.</p></div>
    <div class="panel"><h3>OPTIMIZE</h3><p>Semantic facts are useful only while their evidence is valid. No proof → no specialization.</p></div>
  </div>
  <p class="memory">And if the shared layer does not beat explicit adapters — delete it.</p>
</section>`);

  const FINAL_APPENDIX_KEYS = Object.freeze(['pa1', 'pa3', 'pa6']);
  for (const key of FINAL_APPENDIX_KEYS) {
    const slide = byKey(key);
    if (!slide) throw new Error(`Final narrative: missing appendix-demotion slide ${key}`);
    slide.dataset.kind = 'appendix';
  }

  const FINAL_MAIN_ORDER = Object.freeze([
    'm1', 'm2', 'nProblem', 'nSolutions', 'nMatrix', 'nExternalBench', 'nOverview', 'm7',
    'r1', 'r2', 'r3', 'r4', 'r5', 'r6',
    'm3', 'm5', 'm11', 'm12', 'm13', 'm15', 'm19', 'm20', 'm21', 'm25',
    'r7', 'm26', 'm28', 'm29', 'm32', 'safe1', 'm30', 'm41', 'safe2', 'm31',
    'm39', 'm40', 'm33', 'm34', 'm35', 'm36', 'm43', 'm45', 'm48', 'm49',
    'pa4', 'pa5', 'pa7', 'pa2', 'pa8', 'm50', 'nRQ', 'm52'
  ]);

  const actualMain = [...deck.querySelectorAll('.slide[data-kind="main"]')]
    .map(slide => slide.dataset.noteKey);
  const expected = new Set(FINAL_MAIN_ORDER);
  const missing = FINAL_MAIN_ORDER.filter(key => !actualMain.includes(key));
  const extra = actualMain.filter(key => !expected.has(key));
  if (missing.length || extra.length) {
    throw new Error(`Final narrative main-set mismatch; missing=${missing.join(',')} extra=${extra.join(',')}`);
  }

  for (const key of FINAL_MAIN_ORDER) deck.appendChild(byKey(key));
  for (const key of FINAL_APPENDIX_KEYS) deck.appendChild(byKey(key));

  window.FINAL_MAIN_ORDER = FINAL_MAIN_ORDER;
  window.FINAL_APPENDIX_KEYS = FINAL_APPENDIX_KEYS;
  deck.dataset.finalNarrative = 'two-anchor-v1';
})();
