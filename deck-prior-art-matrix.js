const priorArtMatrixDeck = document.getElementById('deck');
priorArtMatrixDeck.insertAdjacentHTML('beforeend', String.raw`
<section class="slide stack prior-art-matrix-slide" data-kind="main" data-note-key="pa1"><div class="slidehead"><div class="eyebrow">Prior art · compare the first-class object</div><h2>The nearest systems are close for <span class="accent">different reasons</span></h2></div><div class="pa-system-matrix" role="table" aria-label="Prior-art comparison for UniversalToolchain">
  <div class="pa-cell pa-head" role="columnheader">System</div>
  <div class="pa-cell pa-head" role="columnheader">First-class extensible thing</div>
  <div class="pa-cell pa-head" role="columnheader">How composition happens</div>
  <div class="pa-cell pa-head" role="columnheader">Result</div>
  <div class="pa-cell pa-head pa-ut" role="columnheader">Why it is not the same question as UT</div>

  <div class="pa-cell pa-system" data-system="llvm"><strong>LLVM</strong><small>downstream anchor</small></div>
  <div class="pa-cell">IR analyses, passes, target codegen</div>
  <div class="pa-cell">pass pipelines + analyses + plugins</div>
  <div class="pa-cell">optimized / lowered program IR</div>
  <div class="pa-cell" data-fit="outside">source-language family and compiler selection stay upstream</div>

  <div class="pa-cell pa-system" data-system="mlir"><strong>MLIR</strong><small>strongest IR neighbor</small></div>
  <div class="pa-cell" data-fit="core">dialect operations, types, attributes, interfaces</div>
  <div class="pa-cell" data-fit="core">pass pipelines + Transform dialect + dialect conversion / legality</div>
  <div class="pa-cell" data-fit="core">program IR transformed across abstraction levels</div>
  <div class="pa-cell" data-fit="target"><b>UT resolves a compiler configuration;</b> MLIR primarily represents and transforms programs. MLIR can be one UT provider.</div>

  <div class="pa-cell pa-system" data-system="neverlang"><strong>Neverlang</strong><small>closest language-product neighbor</small></div>
  <div class="pa-cell" data-fit="core">language features implemented by modules / roles / slices</div>
  <div class="pa-cell" data-fit="core">language descriptors + feature-model variability compose slices</div>
  <div class="pa-cell" data-fit="core">configured compiler / interpreter + tooling</div>
  <div class="pa-cell" data-fit="research">very close to UT's whole-language goal; the open question is whether UT's typed provider / route planning and cross-representation semantics add value</div>

  <div class="pa-cell pa-system" data-system="ablec"><strong>ableC / Silver</strong><small>independent extensions</small></div>
  <div class="pa-cell" data-fit="core">independently developed C language extensions</div>
  <div class="pa-cell" data-fit="core">attribute-grammar composition + modular parser / well-definedness analyses</div>
  <div class="pa-cell" data-fit="core">extended C compiler with composition guarantees</div>
  <div class="pa-cell" data-fit="research">stronger precedent for safe independent extension composition; UT targets a broader compiler/provider graph, not only extensions to one host language</div>

  <div class="pa-cell pa-system" data-system="racket"><strong>Racket</strong><small>language-oriented programming</small></div>
  <div class="pa-cell" data-fit="core">reader, expander, macros, module language</div>
  <div class="pa-cell" data-fit="core"><code>#lang</code> selects a reader + expander; language code defines semantics</div>
  <div class="pa-cell" data-fit="core">a new language surface and expansion model</div>
  <div class="pa-cell" data-fit="outside">language creation is first-class, but not a resolver over compiler providers, representation routes and backends</div>

  <div class="pa-cell pa-system" data-system="mps"><strong>JetBrains MPS</strong><small>full language workbench</small></div>
  <div class="pa-cell" data-fit="core">language concepts + editor + type system + generators</div>
  <div class="pa-cell" data-fit="core">language extension / composition inside a projectional environment</div>
  <div class="pa-cell" data-fit="core">integrated language + IDE + generator pipeline</div>
  <div class="pa-cell" data-fit="outside">much broader authoring/tooling platform; UT is a lighter library/planning architecture, not a workbench replacement</div>

  <div class="pa-cell pa-system pa-ut-row" data-system="ut"><strong>UniversalToolchain</strong><small>current + research target</small></div>
  <div class="pa-cell pa-ut-row" data-fit="target">language/compiler capabilities + provider choices</div>
  <div class="pa-cell pa-ut-row" data-fit="target">profile → constraints / providers / routes / ordering → immutable <code>LanguagePlan</code></div>
  <div class="pa-cell pa-ut-row" data-fit="target">one concrete compiler/runtime reused for programs</div>
  <div class="pa-cell pa-ut-row" data-fit="research"><b>research boundary:</b> whether one planning + semantic-evidence layer can reduce coupling across independently authored components and changing representations</div>
</div><div class="sourcebar"><a href="https://mlir.llvm.org/docs/Interfaces/" rel="noreferrer" target="_blank">MLIR interfaces</a><a href="https://neverlang.di.unimi.it/" rel="noreferrer" target="_blank">Neverlang</a><a href="https://melt.cs.umn.edu/ableC/" rel="noreferrer" target="_blank">ableC / Silver</a><a href="https://docs.racket-lang.org/guide/languages.html" rel="noreferrer" target="_blank">Racket languages</a><a href="https://www.jetbrains.com/help/mps/basic-notions.html" rel="noreferrer" target="_blank">MPS language model</a></div></section>

<section class="slide stack mlir-ut-slide" data-kind="main" data-note-key="pa2"><div class="slidehead"><div class="eyebrow">The hard comparison · MLIR vs UT</div><h2>Both compose compiler pieces — but the <span class="accent">thing being resolved</span> is different</h2></div><div class="mlir-ut-grid"><div class="mlir-ut-lane"><span class="boundary analogy">MLIR</span><h3>Resolve transformations of a program representation</h3><div class="mini-flow"><b>program IR</b><i>→</i><b>dialects + interfaces</b><i>→</i><b>passes / Transform IR</b><i>→</i><b>conversion legality</b><i>→</i><b>lowered program IR</b></div><p><strong>First-class object:</strong> the program representation and transformations over it.</p><p class="caption">MLIR already supports textual pass pipelines, extensible Transform dialect operations, interfaces and conversion targets. UT cannot claim “pipeline orchestration” as the distinction.</p></div><div class="mlir-ut-lane ut-lane"><span class="boundary target">UT</span><h3>Resolve which compiler will exist for a language profile</h3><div class="mini-flow"><b>language profile</b><i>→</i><b>capabilities + providers</b><i>→</i><b>conflicts / routes / ordering</b><i>→</i><b>LanguagePlan</b><i>→</i><b>compile many programs</b></div><p><strong>First-class object:</strong> the compiler configuration before per-program compilation.</p><p class="caption"><span class="boundary current">IMPLEMENTED WITNESS</span> Current UT has the <code>LanguageDefinition → LanguageCompiler → LanguagePlan → LanguageRuntime</code> ownership chain; broad third-party subsystem solving remains a design/research target.</p></div></div><div class="overlap-strip"><b>Overlap:</b> extensibility · interfaces · staged lowering · legality / constraints · multiple representations <span>→</span> <b>Relationship:</b> MLIR can sit <em>inside</em> a UT plan as the IR / transformation subsystem.</div><div class="sourcebar"><a href="https://mlir.llvm.org/docs/PassManagement/" rel="noreferrer" target="_blank">MLIR pass infrastructure</a><a href="https://mlir.llvm.org/docs/Dialects/Transform/" rel="noreferrer" target="_blank">Transform dialect</a><a href="https://mlir.llvm.org/docs/DialectConversion/" rel="noreferrer" target="_blank">Dialect conversion</a><a href="https://github.com/Misha1302/UniversalToolchain/blob/master/docs/start/mental-model.md" rel="noreferrer" target="_blank">UT ownership chain</a></div></section>

<section class="slide two close-precedents-slide" data-kind="main" data-note-key="pa3"><div class="slidehead"><div class="eyebrow">Closest precedents on the source-language axis</div><h2>Neverlang and ableC are the comparisons we cannot skip</h2></div><div class="panel good"><h3>Neverlang · language products</h3><p><b>modules → roles → slices → language</b></p><p>Features are independently compiled, tested and distributed; configurations compose them into compiler/interpreter variants and tooling.</p><p class="caption">This is closer to UT's whole-language composition than Lua or a parser generator.</p></div><div class="panel"><h3>ableC / Silver · safe independent extensions</h3><p><b>host C + certified extensions</b></p><p>Silver/Copper provide modular analyses so independently developed extensions that pass the checks can compose into a well-defined grammar / attribute grammar.</p><p class="caption">This is a stronger prior-art challenge to UT's “independent modules should compose safely” story.</p></div><p class="memory span2">UT must beat the strongest precedent on each axis — not one straw-man competitor.</p><div class="sourcebar span2"><a href="https://neverlang.di.unimi.it/neverlang.html" rel="noreferrer" target="_blank">Neverlang modules / slices</a><a href="https://link.springer.com/article/10.1007/s10664-021-10074-6" rel="noreferrer" target="_blank">Neverlang language product lines</a><a href="https://melt.cs.umn.edu/" rel="noreferrer" target="_blank">Silver modular composition analyses</a></div></section>

<section class="slide stack adjacent-prior-art-slide" data-kind="appendix" data-note-key="paa1"><div class="slidehead"><div class="eyebrow">Appendix · adjacent systems</div><h2>Useful comparisons — but weaker main-deck candidates</h2></div><div class="cards3"><div class="panel"><h3>MontiCore</h3><p>Textual language components composed by inheritance, embedding and aggregation; strong if the Q&amp;A turns to language composition mechanisms.</p></div><div class="panel"><h3>Spoofax / Rascal</h3><p>Full language-engineering environments for syntax, static semantics, transformations, compilers and IDE services. Compare when the question is “why not a workbench?”</p></div><div class="panel"><h3>Truffle / Graal</h3><p>Language implementation through self-optimizing AST interpreters and partial evaluation. Relevant to the performance/specialization story, not the primary composition story.</p></div></div><p class="caption centertext">Also keep Xtext / parser generators as baseline tooling, not as headline architectural competitors. Lua is useful as an embedding example, but too far from the central research question for the main matrix.</p><div class="sourcebar"><a href="https://monticore.github.io/monticore/docs/Languages/" rel="noreferrer" target="_blank">MontiCore</a><a href="https://spoofax.dev/" rel="noreferrer" target="_blank">Spoofax</a><a href="https://www.rascal-mpl.org/docs/Rascalopedia/LanguageDefinition/" rel="noreferrer" target="_blank">Rascal</a><a href="https://www.graalvm.org/jdk22/graalvm-as-a-platform/language-implementation-framework/" rel="noreferrer" target="_blank">Truffle</a></div></section>
`);

function movePriorArtSlideAfter(noteKey, anchorKey) {
  const slide = document.querySelector(`.slide[data-note-key="${noteKey}"]`);
  const anchor = document.querySelector(`.slide[data-note-key="${anchorKey}"]`);
  if (!slide || !anchor) throw new Error(`Prior-art matrix reorder failed: ${noteKey} after ${anchorKey}`);
  anchor.insertAdjacentElement('afterend', slide);
}

movePriorArtSlideAfter('pa1', 'r2');
movePriorArtSlideAfter('pa2', 'pa1');
movePriorArtSlideAfter('pa3', 'pa2');
