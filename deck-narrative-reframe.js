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
<section class="slide stack fn-solutions-compact" data-kind="main" data-note-key="nSolutions"><div class="slidehead"><div class="eyebrow">External baseline / prior art</div><h2>The ingredients already exist at strong but different boundaries.</h2></div><div class="cards3 fn-overview-cards"><div class="panel"><span class="boundary analogy">MPS / Neverlang</span><h3>Language composition</h3><p>global generation planning / ordering · modular vertical slices · language products</p></div><div class="panel good"><span class="boundary analogy">LLVM / MLIR</span><h3>Analysis knowledge and IR semantics</h3><p>analysis preservation / invalidation · dialects · interfaces · external models · effects · data-flow · conversion</p></div><div class="panel"><span class="boundary analogy">Graal / Truffle</span><h3>Specialization / deabstraction</h3><p>runtime specialization is a strong precedent for making abstractions disappear under evidence.</p></div></div><p class="caption centertext">The research question is where these boundaries stop composing cleanly—not whether these mechanisms exist.</p></section>`);

  addSlide('nMatrix', `
<section class="slide stack fn-matrix-slide" data-kind="main" data-note-key="nMatrix"><div class="slidehead"><div class="eyebrow">Prior-art boundary map</div><h2>Different systems answer different parts of the three research questions.</h2></div><div class="fn-matrix" role="table" aria-label="Boundary comparison for the UT research target"><div class="fn-matrix-cell fn-head">System</div><div class="fn-matrix-cell fn-head">Language pieces</div><div class="fn-matrix-cell fn-head">Analysis knowledge</div><div class="fn-matrix-cell fn-head">Non-shared representations</div><div class="fn-matrix-cell fn-system">MPS / Neverlang</div><div class="fn-matrix-cell fn-strong">strong</div><div class="fn-matrix-cell">framework-specific</div><div class="fn-matrix-cell">through their substrate</div><div class="fn-matrix-cell fn-system">LLVM</div><div class="fn-matrix-cell">not its goal</div><div class="fn-matrix-cell fn-strong">cache · preservation · invalidation</div><div class="fn-matrix-cell">LLVM IR boundary</div><div class="fn-matrix-cell fn-system">MLIR</div><div class="fn-matrix-cell">dialects</div><div class="fn-matrix-cell fn-strong">interfaces · effects · data-flow · conversion</div><div class="fn-matrix-cell">MLIR model or explicit adapters</div><div class="fn-matrix-cell fn-system fn-ut">RESEARCH TARGET</div><div class="fn-matrix-cell fn-ut">whole-language plan</div><div class="fn-matrix-cell fn-ut">open lifecycle hypothesis</div><div class="fn-matrix-cell fn-ut"><b>must beat explicit adapters</b></div></div></section>`);

  addSlide('nExternalBench', `
<section class="slide stack fn-external-bench" data-kind="main" data-note-key="nExternalBench">
  <div class="slidehead">
    <div class="eyebrow">Cost baseline · EuroLLVM 2024</div>
    <h2>Abstraction overhead must be measured, not assumed away.</h2>
  </div>
  <div class="cards3 fn-overview-cards">
    <div class="panel"><h3>Compiler-side cost exists</h3><p>Amini &amp; Niu measured MLIR traversal and interface-dispatch costs as microbenchmarks.</p></div>
    <div class="panel good"><h3>Use the lesson narrowly</h3><p>This is not a UT-vs-MLIR benchmark. It is a warning against unmeasured “zero-cost” claims.</p></div>
    <div class="panel"><h3>What UT must report</h3><p>compile time · memory · adapters · precision · false discharges · schema burden</p></div>
  </div>
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
<section class="slide stack fn-rq-slide" data-kind="main" data-note-key="m7"><div class="slidehead"><div class="eyebrow">Research contract</div><h2>Three questions organize the rest of the talk.</h2></div><div class="fn-rq-grid"><div class="panel"><span class="fn-status fn-measured">MEASURED / MIXED</span><h3>RQ1 · Does reusable composition reduce engineering work enough to justify its infrastructure?</h3><p>The small DSL-evolution study measures this directly; a win is not assumed.</p></div><div class="panel good"><span class="fn-status fn-current">CURRENT / BOUNDED WITNESS</span><h3>RQ2 · Can independently authored language pieces resolve into one structurally valid compiler plan?</h3><p>Current UT has an inspectable LanguagePlan and a bounded planner witness.</p></div><div class="panel"><span class="fn-status fn-hypothesis">OPEN</span><h3>RQ3 · Can independent compiler components exchange semantic knowledge safely across representation boundaries?</h3><p>This is the open research target, not a solved feature.</p></div></div><p class="memory">AUTHOR → RESOLVE → PROVE / OPTIMIZE</p></section>`);

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

  replaceSlide('m13', `
<section class="slide two" data-kind="main" data-note-key="m13"><div class="slidehead"><div class="eyebrow">External baseline / prior art · MLIR</div><h2>Why not just MLIR?</h2></div><div class="panel"><span class="boundary analogy">MLIR ALREADY DOES</span><p><b>dialects · interfaces · external models</b><br/>effects · data-flow · legality / conversion · pass pipelines</p></div><div class="panel good"><span class="boundary target">CURRENT UT QUESTION</span><p class="bigq">Whole-language resolution.</p><p>Which capabilities, providers, conflicts, routes, ordering constraints and backends become one inspectable LanguagePlan?</p></div><p class="caption span2 centertext">MLIR can be inside that plan. This is a responsibility boundary, not an incapability claim.</p></section>`);

  replaceSlide('r7', `
<section class="slide two" data-kind="main" data-note-key="r7"><div class="slidehead"><div class="eyebrow">Evidence boundary</div><h2>RQ1 is measured and mixed. RQ2 has a bounded witness. RQ3 starts here.</h2></div><div class="panel good"><span class="boundary current">MEASURED RESULT</span><h3>Composition economics</h3><p>small study · lower E2 marginal work · higher cumulative work · no E3 maintenance win</p></div><div class="panel"><span class="boundary hypothesis">RESEARCH TARGET / OPEN</span><h3>Semantic evidence lifecycle</h3><p>independent producers · current-valid evidence · cross-representation reuse · conservative invalidation</p></div><p class="memory span2">LOCAL PROOF WAS EASY; THE HARD CASE STARTS WHEN THE PROOF LIVES ELSEWHERE.</p></section>`);

  replaceSlide('m30', `
<section class="slide two" data-kind="main" data-note-key="m30"><div class="slidehead"><div class="eyebrow">Semantic query</div><h2>Why can’t a semantic query simply return bool?</h2></div><div class="panel code bigcode">SafeIndex(a, i)

unsupported
unknown
established(P)
refuted(P)
contradictory</div><div class="panel"><p class="bigq">Different failures mean different things.</p><p>The transformation owns proposition <code>P</code>; independent producers contribute evidence through the published query contract.</p></div></section>`);

  replaceSlide('m41', `
<section class="slide stack" data-kind="main" data-note-key="m41"><div class="slidehead"><div class="eyebrow">Legality requirement</div><h2>The transformation owns the condition that must hold before its rewrite is legal.</h2></div><div class="timeline"><div><b>TRANSFORMATION</b><span>states proposition <code>P</code></span></div><i>→</i><div class="good"><b>LEGALITY REQUIREMENT</b><span>current-valid suitable evidence must establish <code>P</code></span></div><i>→</i><div><b>DISCHARGE / FAIL CLOSED</b><span>producers cannot redefine the precondition</span></div><i>→</i><div><b>LEGAL CANDIDATE</b><span>only then may preference rank it</span></div></div><p class="caption centertext">A formal model may call this requirement an <b>Obligation</b>; the talk keeps the plain-language term primary.</p></section>`);

  replaceSlide('m33', `
<section class="slide two" data-kind="main" data-note-key="m33"><div class="slidehead"><div class="eyebrow">Strongest existing baseline</div><h2>LLVM and MLIR already manage analysis knowledge seriously.</h2></div><div class="panel"><span class="boundary analogy">LLVM</span><p><code>AnalysisManager</code><br/><code>PreservedAnalyses</code><br/>cache · preservation · invalidation · pass/plugin extension points</p></div><div class="panel good"><span class="boundary analogy">MLIR</span><p>dialects · interfaces / external models<br/>effects/resources · data-flow · conversion legality</p></div><p class="caption span2 centertext">Any shared lifecycle must beat these mechanisms plus explicit adapters; generic queries and invalidation are not the novelty.</p></section>`);

  replaceSlide('m34', `
<section class="slide stack" data-kind="main" data-note-key="m34"><div class="slidehead"><div class="eyebrow">Research hypothesis</div><h2>The candidate reusable boundary is the lifecycle of semantic evidence.</h2></div><div class="ownerflow"><div class="role"><b>producer</b><span>derives evidence</span></div><i>→</i><div class="role good"><b>published lifecycle</b><span>typed state · semantic identity · validity scope · assumptions · provenance</span></div><i>→</i><div class="role"><b>consumer</b><span>asks its own semantic query</span></div></div><p class="caption centertext"><span class="boundary hypothesis">RESEARCH TARGET / OPEN</span> The claim to test is whether this lifecycle reduces cross-component integration cost without weakening correctness across non-shared representations.</p></section>`);

  replaceSlide('m49', `
<section class="slide two" data-kind="main" data-note-key="m49"><div class="slidehead"><div class="eyebrow">Strongest alternative</div><h2>Maybe the shared evidence lifecycle should not exist.</h2></div><div class="panel"><span class="boundary analogy">EXPLICIT-ADAPTER BASELINE</span><p>LLVM-style analysis manager<br/>MLIR interfaces + external models<br/>domain-specific analyses<br/>explicit local adapters<br/>local invalidation / re-analysis</p></div><div class="panel good"><p class="bigq">If this solves the same coupling problem with less machinery, use it.</p><p>The shared lifecycle earns its complexity only through measurable integration or verification benefit.</p></div></section>`);

  replaceSlide('m50', `
<section class="slide stack fn-research-plan" data-kind="main" data-note-key="m50"><div class="slidehead"><div class="eyebrow">Planned study · before stronger claims</div><h2>Compare the shared evidence lifecycle against the strongest ordinary baseline.</h2></div><div class="fn-study-grid"><div class="panel"><h3>Baseline</h3><p>MLIR / LLVM-style interfaces + domain analyses + explicit adapters + local invalidation</p></div><div class="panel good"><h3>Intervention</h3><p>Independent producers publish evidence through the shared lifecycle; existing consumers stay unchanged.</p></div><div class="panel"><h3>Correctness controls</h3><p>Stale evidence, contradiction, mutation or representation change must never satisfy a legality requirement.</p></div><div class="panel"><h3>Measure</h3><p>consumer edits · adapters · precision · false discharges · compile time · memory · invalidation / re-analysis · schema burden</p></div></div><p class="memory">If explicit adapters win on cost, precision and safety, remove the meta-layer.</p></section>`);

  addSlide('nRQ', `
<section class="slide stack fn-rq-slide" data-kind="main" data-note-key="nRQ"><div class="slidehead"><div class="eyebrow">Answers</div><h2>Return to the same three research questions.</h2></div><div class="fn-rq-grid"><div class="panel"><span class="fn-status fn-measured">PARTIAL / MIXED</span><h3>RQ1 · Does reusable composition reduce engineering work?</h3><p><b>Mixed in the small measured study.</b> E2 marginal work was lower for UT, cumulative work remained higher, and the E3 maintenance advantage did not appear.</p></div><div class="panel good"><span class="fn-status fn-current">BOUNDED YES</span><h3>RQ2 · Can independent pieces resolve into one structurally valid compiler plan?</h3><p><b>Yes for the tested route/order case.</b> LanguagePlan is implemented and inspectable; this is not a semantic-correctness theorem.</p></div><div class="panel"><span class="fn-status fn-hypothesis">OPEN</span><h3>RQ3 · Can independent components share semantic knowledge safely across representation boundaries?</h3><p><b>Not answered yet.</b> The hypothesis and falsification experiment are defined; the comparative study remains to be run.</p></div></div></section>`);

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



  replaceSlide('pa4', `
<section class="slide two fn-balanced-pair ut-current-target-slide" data-kind="main" data-note-key="pa4"><div class="slidehead"><div class="eyebrow">Identity boundary</div><h2>Current Wist/UT witness is not the required universal architecture.</h2></div><div class="panel fn-equal-card"><span class="boundary current">CURRENT WIST/UT WITNESS</span><h3>Stack-oriented AIR exists</h3><p>Bytecode → AIR → verifier / interpreter / CIL is a useful implementation witness.</p></div><div class="panel fn-equal-card good"><span class="boundary target">RESEARCH TARGET / OPEN</span><h3>No mandatory program IR</h3><p>StackIR, SSA, MLIR or a domain graph should remain selectable providers inside one LanguagePlan.</p></div><p class="caption span2 centertext">If the framework core requires Push, Drop, Block or Value semantics, the representation-neutral target has failed.</p></section>`);

  replaceSlide('pa5', `
<section class="slide stack ut-meta-kernel-slide" data-kind="main" data-note-key="pa5">
  <div class="slidehead"><div class="eyebrow">Representation-neutral target</div><h2>UT should coordinate routes and evidence, not define a universal IR.</h2></div>
  <div class="cards3 fn-overview-cards">
    <div class="panel"><h3>Packages define semantics</h3><p>syntax · types · effects · domain concepts · representation-specific invariants</p></div>
    <div class="panel good"><h3>UT coordinates</h3><p>identity · artifact contracts · providers · constraints · obligations · validity-scoped evidence</p></div>
    <div class="panel"><h3>Plans select engines</h3><p>AST interpreter · StackIR · SSA · MLIR / LLVM · custom domain graph</p></div>
  </div>
  <p class="memory">No required Operation/Value model. No required AST shape. No required VM opcode set.</p>
</section>`);

  replaceSlide('pa7', `
<section class="slide stack representation-packs-slide" data-kind="main" data-note-key="pa7">
  <div class="slidehead"><div class="eyebrow">Consequence</div><h2>Representation packs own their own semantics.</h2></div>
  <div class="cards3 fn-overview-cards">
    <div class="panel"><h3>StackIR pack</h3><p>owns stack typing, Push/Drop and stack-specific lowering.</p></div>
    <div class="panel"><h3>SSA / MLIR pack</h3><p>owns values, blocks, dominance, dialect legality and pass integration.</p></div>
    <div class="panel good"><h3>UT core</h3><p>owns only the contract boundary: how this pack participates in a compiler plan.</p></div>
  </div>
  <p class="caption centertext">The same concept may lower to stack ops, SSA ops, MLIR ops, CIL instructions, runtime calls or GPU operations.</p>
</section>`);

  replaceSlide('pa2', `
<section class="slide two fn-balanced-pair mlir-ut-slide" data-kind="main" data-note-key="pa2"><div class="slidehead"><div class="eyebrow">External baseline / prior art · MLIR</div><h2>MLIR already composes extensible semantics inside one program model.</h2></div><div class="panel fn-equal-card"><span class="boundary analogy">MLIR</span><h3>Strong baseline</h3><p>dialects · interfaces · external models · effects · conversion legality · composable data-flow analyses</p></div><div class="panel fn-equal-card good"><span class="boundary target">RESEARCH TARGET / OPEN</span><h3>Remaining question</h3><p>Does a useful evidence lifecycle survive when participants do not all share MLIR's Operation / Region / Value model?</p></div><p class="caption span2 centertext">Novelty is not queries, interfaces or invalidation. The comparison is a shared lifecycle across heterogeneous representations versus explicit adapters.</p></section>`);

  replaceSlide('pa8', `
<section class="slide stack ut-falsification-slide" data-kind="main" data-note-key="pa8"><div class="slidehead"><div class="eyebrow">Falsifier</div><h2>The shared layer should be deleted if explicit adapters are simpler and equally safe.</h2></div><div class="cards3 fn-overview-cards"><div class="panel"><h3>Positive case</h3><p>A new producer strengthens an unchanged consumer across a representation boundary.</p></div><div class="panel broken"><h3>Negative controls</h3><p>Stale, contradictory, wrong-path or unmapped evidence never satisfies a legality requirement.</p></div><div class="panel good"><h3>Decision rule</h3><p>Compare adapters, consumer edits, precision, false discharges, compile time, memory and schema burden.</p></div></div><p class="memory">If explicit adapters win on cost, precision and safety, delete the meta-layer.</p></section>`);

  const FINAL_APPENDIX_KEYS = Object.freeze(['pa1', 'pa3', 'pa6', 'nOverview', 'm36', 'pa5', 'pa7', 'nExternalBench']);
  for (const key of FINAL_APPENDIX_KEYS) {
    const slide = byKey(key);
    if (!slide) throw new Error(`Final narrative: missing appendix-demotion slide ${key}`);
    slide.dataset.kind = 'appendix';
  }

  const FINAL_MAIN_ORDER = Object.freeze([
    'm1', 'm2', 'm3', 'm5', 'nProblem',
    'm7', 'nSolutions', 'nMatrix', 'pa4',
    'm11', 'm12', 'm13', 'm15', 'm19', 'm20', 'm21',
    'r1', 'r2', 'r3', 'r4', 'r5', 'r6',
    'm25', 'r7',
    'm26', 'm28', 'm29', 'm32', 'safe1', 'm30', 'm41', 'safe2', 'm31', 'm39', 'm40',
    'm33', 'pa2', 'm34', 'm35', 'm43', 'm45',
    'm48', 'm49', 'pa8', 'm50',
    'nRQ', 'm52'
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
  deck.dataset.finalNarrative = 'causal-rq-spine-v1';
})();
