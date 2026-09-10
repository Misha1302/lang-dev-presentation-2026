(() => {
  const byKey = key => document.querySelector(`.slide[data-note-key="${key}"]`);

  function patchTitleSlide() {
    const slide = byKey('m1');
    if (!slide) return;

    const h2 = slide.querySelector('h2');
    if (h2) {
      h2.innerHTML = 'Build the Language,<br/><span class="accent">Then Make the Abstractions Disappear.</span>';
    }

    const hero = slide.querySelector('.hero');
    const bigq = hero?.querySelector('.bigq');
    if (bigq) {
      bigq.textContent = 'How can independently developed language capabilities compose into concrete languages without giving up serious optimization?';
    }

    if (hero && !hero.querySelector('.talk-thesis')) {
      const thesis = document.createElement('p');
      thesis.className = 'talk-thesis';
      thesis.textContent = 'Author reusable pieces. Resolve one concrete compiler plan. Erase machinery where it is no longer needed, while preserving the semantic facts later decisions still need.';
      hero.insertBefore(thesis, hero.querySelector('.memory'));
    }
  }

  function patchVerticalSliceSlide() {
    const slide = byKey('m3');
    if (!slide || slide.querySelector('.slice-demo')) return;
    slide.classList.add('vertical-slice-enhanced');

    const layers = slide.querySelector('.layers');
    const demo = document.createElement('div');
    demo.className = 'slice-demo';
    demo.innerHTML = `
      <div class="slice-feature">arrays</div>
      <div class="slice-track" aria-label="Array capability crosses compiler layers">
        <span>syntax<br/><small>a[i]</small></span>
        <span>types<br/><small>T[]</small></span>
        <span>analysis<br/><small>range facts</small></span>
        <span>IR<br/><small>load element</small></span>
        <span>lowering<br/><small>address + check</small></span>
        <span>optimizer / backend<br/><small>remove or emit</small></span>
      </div>
      <p class="slice-caption">One reusable capability may own a vertical slice, not just one parser hook.</p>
    `;
    layers?.insertAdjacentElement('afterend', demo);
  }

  function markFastPassSlides() {
    // No slides are deleted, hidden, or moved to appendix. These markers tell the
    // speaker which existing slides should be treated as continuation/details
    // during rehearsal and allow CSS to label them without altering navigation.
    const fast = ['r1', 'r2', 'r3', 'm26', 'm30', 'm31', 'm39', 'm40', 'm41'];
    const detail = ['r6', 'r7', 'm33', 'm36', 'm48'];
    for (const key of fast) byKey(key)?.setAttribute('data-pace', 'fast-pass');
    for (const key of detail) byKey(key)?.setAttribute('data-pace', 'supporting-detail');
  }

  function patchFinalSlide() {
    const slide = byKey('m52');
    if (!slide) return;

    const h2 = slide.querySelector('h2');
    if (h2) {
      h2.innerHTML = 'Erase the <span class="accent">machinery</span>.<br/>Preserve only valid semantic <span class="accent">knowledge</span>.';
    }

    const caption = slide.querySelector('.caption');
    if (caption) {
      caption.textContent = 'Meaning is narrow here: current-valid semantic knowledge needed by later compiler decisions, not permanent preservation of every source representation.';
    }

    if (!slide.querySelector('.final-precision-note')) {
      const note = document.createElement('p');
      note.className = 'final-precision-note centertext';
      note.textContent = 'AUTHOR reusable pieces → RESOLVE one compiler → OPTIMIZE by removing machinery without losing usable meaning.';
      caption?.insertAdjacentElement('beforebegin', note);
    }
  }

  patchTitleSlide();
  patchVerticalSliceSlide();
  markFastPassSlides();
  patchFinalSlide();
})();
