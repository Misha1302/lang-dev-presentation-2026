const priorArtMatrixDeck = document.getElementById('deck');
priorArtMatrixDeck.insertAdjacentHTML('beforeend', String.raw`
<section class="slide stack prior-art-matrix-slide" data-kind="main" data-note-key="pa1"><div class="slidehead"><div class="eyebrow">Prior art · responsibility matrix</div><h2>Where does each system own the extensibility problem?</h2></div><div class="pa-matrix" role="table" aria-label="Comparison of LLVM, MLIR, Racket, Lua and UniversalToolchain">
  <div class="pa-cell pa-head pa-row-label" role="columnheader">Responsibility</div>
  <div class="pa-cell pa-head" role="columnheader"><strong>LLVM</strong><small>optimizer + codegen</small></div>
  <div class="pa-cell pa-head" role="columnheader"><strong>MLIR</strong><small>extensible compiler IR</small></div>
  <div class="pa-cell pa-head" role="columnheader"><strong>Racket</strong><small>language-oriented programming</small></div>
  <div class="pa-cell pa-head" role="columnheader"><strong>Lua</strong><small>embedded extension language</small></div>
  <div class="pa-cell pa-head pa-ut" role="columnheader"><strong>UniversalToolchain</strong><small>language/compiler composition</small></div>

  <div class="pa-cell pa-row-label" role="rowheader">Create / vary the language surface</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">outside</span>frontend owns source language</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>custom dialect syntax / custom frontend</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span><code>#lang</code> + reader / expander</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>host extends one Lua language</div>
  <div class="pa-cell" data-fit="target"><span class="pa-tag">target</span>profiles assemble reusable capabilities</div>

  <div class="pa-cell pa-row-label" role="rowheader">Extensible IR semantics</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>stable LLVM IR + intrinsics / metadata</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span>dialect ops, types, attributes, interfaces</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">not central</span>expansion model, not an IR framework</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">not central</span>bytecode VM, not an extensible IR stack</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">provider choice</span>can use custom IR, MLIR, LLVM, …</div>

  <div class="pa-cell pa-row-label" role="rowheader">Resolve one compiler from a language profile</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">client work</span>tool authors assemble the pipeline</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">client-defined</span>passes / transforms / conversions compose</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">different model</span><code>#lang</code> selects a language implementation</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">host work</span>host chooses runtime and libraries</div>
  <div class="pa-cell" data-fit="target"><span class="pa-tag">first-class target</span>profile → resolved <code>LanguagePlan</code></div>

  <div class="pa-cell pa-row-label" role="rowheader">Independent component composition</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>passes, analyses, plugins</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span>interfaces + external models + dialects</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span>macros, modules, language layers</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>C API, libraries, host callbacks</div>
  <div class="pa-cell" data-fit="target"><span class="pa-tag">target</span>capabilities + providers + contracts</div>

  <div class="pa-cell pa-row-label" role="rowheader">Cross-module semantic evidence for optimization</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">supported</span>analysis manager + preserved analyses</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">strong prior art</span>interfaces, effects, data-flow analyses</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">not central</span>not the compiler-analysis focus</div>
  <div class="pa-cell" data-fit="outside"><span class="pa-tag">not central</span>not the compiler-analysis focus</div>
  <div class="pa-cell" data-fit="research"><span class="pa-tag">research</span>shared evidence across independent modules</div>

  <div class="pa-cell pa-row-label" role="rowheader">Lowering / backend choice</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span>mature target code generation</div>
  <div class="pa-cell" data-fit="core"><span class="pa-tag">core strength</span>staged lowering; LLVM / target dialects</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">ecosystem</span>runtime / compiler choices</div>
  <div class="pa-cell" data-fit="supported"><span class="pa-tag">runtime</span>register VM / interpreter</div>
  <div class="pa-cell" data-fit="target"><span class="pa-tag">target</span>planner selects legal provider/backend route</div>
</div><div class="pa-legend" aria-label="Matrix legend"><span><i class="core"></i>core strength</span><span><i class="supported"></i>supported / adjacent</span><span><i class="outside"></i>client / outside scope</span><span><i class="research"></i>research hypothesis</span><span><i class="target"></i>UT architectural target</span></div><div class="sourcebar"><a href="https://llvm.org/docs/WritingAnLLVMNewPMPass.html" rel="noreferrer" target="_blank">LLVM pass infrastructure</a><a href="https://mlir.llvm.org/docs/Interfaces/" rel="noreferrer" target="_blank">MLIR interfaces</a><a href="https://docs.racket-lang.org/guide/languages.html" rel="noreferrer" target="_blank">Racket: Creating Languages</a><a href="https://www.lua.org/manual/5.4/manual.html" rel="noreferrer" target="_blank">Lua embedding model</a></div></section>
<section class="slide two" data-kind="main" data-note-key="pa2"><div class="slidehead"><div class="eyebrow">Positioning</div><h2>MLIR can be a provider, not only a comparison point</h2></div><div class="panel good"><h3>MLIR gives</h3><p>dialects · interfaces · conversion legality · pass infrastructure · staged lowering</p></div><div class="panel"><h3>UT question</h3><p class="bigq">Who resolves one concrete compiler for this language profile?</p><p>capabilities · providers · conflicts · representation routes · backend · mandatory ordering</p></div><p class="memory span2">Representation extensibility creates a composition question.</p></section>
`);

function movePriorArtSlideAfter(noteKey, anchorKey) {
  const slide = document.querySelector(`.slide[data-note-key="${noteKey}"]`);
  const anchor = document.querySelector(`.slide[data-note-key="${anchorKey}"]`);
  if (!slide || !anchor) throw new Error(`Prior-art matrix reorder failed: ${noteKey} after ${anchorKey}`);
  anchor.insertAdjacentElement('afterend', slide);
}

movePriorArtSlideAfter('pa1', 'r2');
movePriorArtSlideAfter('pa2', 'pa1');
