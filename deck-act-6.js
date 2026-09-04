document.getElementById('deck').insertAdjacentHTML('beforeend', String.raw`
<section class="slide two" data-kind="main" data-note-key="m45"><div class="slidehead"><div class="eyebrow">Act 6 · Semantic substrate</div><h2>A raw fact can become false after a transformation</h2></div><div class="panel"><h3>before</h3><p><code>range(i) = [0,n)</code></p></div><div class="panel broken"><h3>after transform</h3><p>what changed?<br/>same entity?<br/>same context?<br/>still valid?</p></div></section>
<section class="slide two" data-kind="main" data-note-key="m46"><div class="slidehead"><div class="eyebrow">Concept name · after the failure</div><h2>Use a contextual <span class="accent">Judgement</span>, not a naked value</h2></div><div class="panel code bigcode">Judgement =
  subject
+ value
+ context
+ revision / validity
+ evidence
+ assumptions</div><div class="panel"><span class="boundary hypothesis">PROPOSED MODEL</span><p>A claim is useful only if a consumer can know when and why it is valid.</p></div></section>
<section class="slide stack" data-kind="main" data-note-key="m47"><div class="slidehead"><div class="eyebrow">Why one interface hierarchy is not enough</div><h2>“Writable” becomes a cross-product of independent semantic dimensions</h2></div><div class="cards3"><div class="panel"><h3>seems simple</h3><p><code>IWritable</code></p></div><div class="panel broken"><h3>real dimensions</h3><p>volatile<br/>atomic<br/>ordering<br/>visibility<br/>GC barriers<br/>transactions</p></div><div class="panel"><h3>bad end state</h3><p><code>IAtomicVolatileWritable...</code></p></div></div></section>
<section class="slide stack" data-kind="main" data-note-key="m48"><div class="slidehead"><div class="eyebrow">Small stable anchors</div><h2>Keep identity small; let semantics stay orthogonal</h2></div><div class="architecture"><div class="archnode">Value</div><i>·</i><div class="archnode">Place</div><i>·</i><div class="archnode">Operation</div><i>·</i><div class="archnode">Region</div><i>·</i><div class="archnode">Type</div><i>·</i><div class="archnode">Symbol</div></div></section>
<section class="slide two" data-kind="main" data-note-key="m49"><div class="slidehead"><div class="eyebrow">Operation-centric semantics</div><h2>Ask about the operation, not the object’s inheritance chain</h2></div><div class="panel code bigcode">Write(place, value)
  ↓
CanWrite?
Effects?
Atomicity?
Ordering?
Visibility?</div><div class="panel"><p class="bigq">One operation can expose several orthogonal semantic views.</p></div></section>
<section class="slide stack" data-kind="main" data-note-key="m50"><div class="slidehead"><div class="eyebrow">From knowledge to correctness</div><h2>Judgements matter when they discharge obligations</h2></div><div class="timeline"><div><b>JUDGEMENTS</b><span>what we know</span></div><i>→</i><div class="good"><b>OBLIGATIONS</b><span>what must hold</span></div><i>→</i><div><b>DECISION</b><span>transform / reject / preserve check</span></div></div></section>
<section class="slide stack" data-kind="main" data-note-key="m51"><div class="slidehead"><div class="eyebrow">Obligations constrain representation</div><h2>Correctness requirements can force route structure</h2></div><div class="timeline"><div><b>OBLIGATION</b><span>SafeIndex / legality / capability</span></div><i>→</i><div><b>REPRESENTATION REQUIREMENT</b><span>property P / preserved mapping</span></div><i>→</i><div><b>FEASIBLE ROUTES</b><span>only candidates that can satisfy it</span></div><i>→</i><div><b>PREFERENCE</b><span>cost / policy</span></div></div></section>
<section class="slide two" data-kind="main" data-note-key="m52"><div class="slidehead"><div class="eyebrow">Why not one mega-solver?</div><h2>One contract does not imply one algorithm</h2></div><div class="panel"><p>abstract domains · fixed points · graph search · legalization · dependency resolution · cost selection · validation</p></div><div class="panel good"><p class="bigq">Share the semantic boundary, keep task-native engines.</p></div></section>
`);
