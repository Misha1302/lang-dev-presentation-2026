const priorArtMatrixDeck = document.getElementById('deck');
priorArtMatrixDeck.insertAdjacentHTML('beforeend', String.raw`
<section class="slide stack" data-kind="main" data-note-key="pa1"><div class="slidehead"><div class="eyebrow">Prior art · strongest alternatives</div><h2>Existing systems solve different parts of the language-extension problem</h2></div><div class="matrix compactmatrix"><div class="mhead">System</div><div class="mhead">What it is good at</div><div class="mhead">Boundary for this talk</div><div><b>LLVM</b></div><div>optimizer, IR, codegen, pass pipeline, reusable compiler infrastructure</div><div>does not make whole source-language/profile composition the first-class object</div><div><b>MLIR</b></div><div>extensible IR dialects, interfaces, legality, lowering, transform infrastructure</div><div>closest prior art; UT asks who resolves capabilities, providers, routes and backend into one compiler plan</div><div><b>Racket</b></div><div>language-oriented programming, macros, <code>#lang</code>, custom surfaces</div><div>different ecosystem model: language creation inside Racket's macro/expander world, not .NET pipeline planning</div><div><b>Lua / embedded scripting</b></div><div>small embeddable language and extension point for host applications</div><div>excellent embedding story, but not a typed compiler-composition architecture</div><div><b>Parser tools</b></div><div>ANTLR/Sprache/Irony-style frontend construction</div><div>help build syntax/frontends; semantic contracts, IR, optimization and backend composition remain on the author</div></div><p class="caption centertext">This is a responsibility boundary, not a “why existing tools are bad” slide.</p></section>
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
