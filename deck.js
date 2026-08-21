(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const counter = document.getElementById('counter');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const fullscreen = document.getElementById('fullscreen');
  const notesToggle = document.getElementById('notesToggle');
  const notesPanel = document.getElementById('notesPanel');
  const notesText = document.getElementById('notesText');

  // Keep the slide source faithful to the shipped example while allowing visual line breaks at commas.
  const dialectCode = document.querySelector('.dialect-layout .code-block code');
  if (dialectCode) {
    dialectCode.innerHTML = `dialect CompositionRestricted
use Arithmetic,<wbr>BooleanConditions,<wbr>Comments,<wbr>ComparisonConditions,<wbr>Conditions,<wbr>Equality,<wbr>Numbers,<wbr>Scopes,<wbr>Whitespaces
exclude CSharpInterop,<wbr>Identifier,<wbr>InternalPreprocessorLexemes,<wbr>Labels,<wbr>Loops,<wbr>NativeTypes,<wbr>ParametersSetter,<wbr>SemicolonAsNewLine,<wbr>Variables
backend interpreter
security restricted
capability composition-restricted`;
  }

  const previousTransitions = [
    '',
    'From previous: the opening question asks for composability without carrying dynamic machinery into every execution; now establish the tool spectrum developers already have. ',
    'From previous: after showing the two extremes, zoom into the engineering work that remains between them. ',
    'From previous: having named the engineering gap, acknowledge prior art before proposing our design point. ',
    'From previous: after separating our .NET design point from Racket and language workbenches, state the objective precisely. ',
    'From previous: the first design question from the goal slide is what the generic framework itself must know. ',
    'From previous: once the core surface is small, show how independent stages can connect without shared compiler internals. ',
    'From previous: typed routes are abstract until we show how a real Wist language requests one composition. ',
    'From previous: after showing the dialect declaration, answer what each concrete kind of extension maps to. ',
    'From previous: after demonstrating the open extension choices, ask where those choices become closed. ',
    'From previous: after the generic planner freezes a route, instantiate the idea with Wist\'s concrete compilation path. ',
    'From previous: once the route is concrete, separate planning-time staging from program-level IR specialization. ',
    'From previous: now substantiate the IR-specialization half with one rewrite that exists in the current code. ',
    'From previous: after one successful specialization, define exactly what that example proves and where performance is measured. ',
    'From previous: specialization is useful only if different execution strategies still preserve one language meaning. ',
    'From previous: an ownership rule needs executable checks, so show parity testing and the current maturity boundary. ',
    'From previous: after verification and the alpha boundary, compress the whole architecture into the final formula. '
  ];
  slides.forEach((slide, i) => {
    const prefix = previousTransitions[i];
    if (prefix && slide.dataset.notes && !slide.dataset.notes.startsWith('From previous:')) {
      slide.dataset.notes = prefix + slide.dataset.notes;
    }
  });

  const clamp = n => Math.max(0, Math.min(slides.length - 1, n));
  const fromHash = () => {
    const raw = location.hash.replace(/^#(?:slide-?)?/, '');
    const parsed = Number.parseInt(raw, 10);
    return Number.isFinite(parsed) ? clamp(parsed - 1) : 0;
  };

  let index = fromHash();

  function render(updateHash = true) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
      slide.setAttribute('aria-hidden', i === index ? 'false' : 'true');
    });
    counter.textContent = `${index + 1} / ${slides.length}`;
    prev.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    notesText.textContent = slides[index].dataset.notes || 'No notes for this slide.';
    document.title = `Slide ${index + 1}/${slides.length} — Build the Language, Then Make the Abstractions Disappear`;
    if (updateHash && location.hash !== `#${index + 1}`) history.replaceState(null, '', `#${index + 1}`);
  }

  function go(delta) {
    const target = clamp(index + delta);
    if (target === index) return;
    index = target;
    render();
  }

  prev.addEventListener('click', () => go(-1));
  next.addEventListener('click', () => go(1));
  fullscreen.addEventListener('click', async () => {
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
      else await document.exitFullscreen();
    } catch (_) { /* browser may deny fullscreen without user activation */ }
  });
  notesToggle.addEventListener('click', () => {
    notesPanel.hidden = !notesPanel.hidden;
    if (!notesPanel.hidden) notesPanel.scrollTop = 0;
  });

  window.addEventListener('hashchange', () => {
    index = fromHash();
    render(false);
  });

  window.addEventListener('keydown', event => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    const key = event.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(key)) {
      event.preventDefault(); go(1);
    } else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(key)) {
      event.preventDefault(); go(-1);
    } else if (key === 'Home') {
      event.preventDefault(); index = 0; render();
    } else if (key === 'End') {
      event.preventDefault(); index = slides.length - 1; render();
    } else if (key.toLowerCase() === 'f') {
      event.preventDefault(); fullscreen.click();
    } else if (key.toLowerCase() === 'n') {
      event.preventDefault(); notesToggle.click();
    }
  });

  let touchStartX = null;
  window.addEventListener('touchstart', e => {
    if (e.touches.length === 1) touchStartX = e.touches[0].clientX;
  }, {passive:true});
  window.addEventListener('touchend', e => {
    if (touchStartX == null || e.changedTouches.length !== 1) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    touchStartX = null;
    if (Math.abs(dx) > 55) go(dx < 0 ? 1 : -1);
  }, {passive:true});

  render(false);
})();
