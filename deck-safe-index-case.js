const safeIndexDeck = document.getElementById('deck');
safeIndexDeck.insertAdjacentHTML('beforeend', String.raw`
<section class="slide stack" data-kind="main" data-note-key="safe1"><div class="slidehead"><div class="eyebrow">Running example · semantic exchange</div><h2>Independent checkers publish facts about expressions</h2></div><div class="ownerflow"><div class="role"><b>Lower-bound checker</b><span><code>i ≥ 0</code></span></div><i>+</i><div class="role"><b>Loop-condition checker</b><span><code>i &lt; a.Length</code></span></div><i>+</i><div class="role"><b>Extent checker</b><span><code>Length(a)</code> is stable here</span></div></div><div class="mapflow horizontal"><div>producers know only the contract</div><i>→</i><div class="good">semantic expression knowledge</div><i>→</i><div>consumers ask propositions</div></div><p class="caption centertext"><span class="boundary hypothesis">DESIGN SKETCH</span> The checkers do not call each other and do not know the future optimizer. They publish current-valid evidence about expression identities.</p></section>
<section class="slide two" data-kind="main" data-note-key="safe2"><div class="slidehead"><div class="eyebrow">Specialization · global optimization</div><h2>A bounds check can disappear only after the obligation is discharged</h2></div><div class="panel code bigcode">for (int i = 0; i &lt; a.Length; i++)
{
    sum += a[i];
}

query: SafeIndex(a, i)</div><div class="panel good"><h3>Specializer rule</h3><p><code>BoundsCheckedLoad(a, i)</code><br/>→ <code>UncheckedLoad(a, i)</code></p><p class="caption">only if evidence establishes <code>0 ≤ i &lt; Length(a)</code> for the same subject, path and revision</p></div><p class="memory span2">No direct producer dependency. No valid proof — no specialization.</p></section>
`);

function moveSafeIndexSlideAfter(noteKey, anchorKey) {
  const slide = document.querySelector(`.slide[data-note-key="${noteKey}"]`);
  const anchor = document.querySelector(`.slide[data-note-key="${anchorKey}"]`);
  if (!slide || !anchor) throw new Error(`SafeIndex deck reorder failed: ${noteKey} after ${anchorKey}`);
  anchor.insertAdjacentElement('afterend', slide);
}

moveSafeIndexSlideAfter('safe1', 'm30');
moveSafeIndexSlideAfter('safe2', 'safe1');
