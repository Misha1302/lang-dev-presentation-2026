(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const counter = document.getElementById('counter');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const fullscreen = document.getElementById('fullscreen');
  const notesToggle = document.getElementById('notesToggle');
  const notesPanel = document.getElementById('notesPanel');
  const notesText = document.getElementById('notesText');

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
