(() => {
  const mainSlides = [...document.querySelectorAll('.slide[data-kind="main"]')];
  const appendixSlides = [...document.querySelectorAll('.slide[data-kind="appendix"]')];
  const allSlides = [...mainSlides, ...appendixSlides];
  const counter = document.getElementById('counter');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const appendixToggle = document.getElementById('appendixToggle');
  const fullscreen = document.getElementById('fullscreen');
  const notesToggle = document.getElementById('notesToggle');
  const notesPanel = document.getElementById('notesPanel');
  const notesText = document.getElementById('notesText');

  let appendixMode = false;
  let index = 0;

  const visibleSlides = () => appendixMode ? appendixSlides : mainSlides;
  const clamp = value => Math.max(0, Math.min(visibleSlides().length - 1, value));
  const activeSlide = () => visibleSlides()[index];

  function parseHash() {
    const raw = location.hash.replace(/^#/, '');
    const appendixMatch = raw.match(/^a(?:ppendix-?)?(\d+)$/i);
    if (appendixMatch) {
      appendixMode = true;
      index = Math.max(0, Math.min(appendixSlides.length - 1, Number.parseInt(appendixMatch[1], 10) - 1));
      return;
    }
    const mainMatch = raw.match(/^(?:slide-?)?(\d+)$/i);
    if (!mainMatch) return;
    const number = Number.parseInt(mainMatch[1], 10);
    if (number > mainSlides.length && number <= mainSlides.length + appendixSlides.length) {
      appendixMode = true;
      index = number - mainSlides.length - 1;
    } else {
      appendixMode = false;
      index = Math.max(0, Math.min(mainSlides.length - 1, number - 1));
    }
  }

  function syncHash() {
    const desired = appendixMode ? `#A${index + 1}` : `#${index + 1}`;
    if (location.hash !== desired) history.replaceState(null, '', desired);
  }

  function intersects(a, b) {
    return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
  }

  function runLayoutDiagnostics() {
    if (new URLSearchParams(location.search).get('visual-check') !== '1') return;
    const current = activeSlide();
    const errors = [];
    if (!current) errors.push('no-active-slide');

    if (current) {
      const viewportWidth = document.documentElement.clientWidth;
      const viewportHeight = document.documentElement.clientHeight;
      const elements = [current, ...current.querySelectorAll('*')];
      for (const element of elements) {
        const style = getComputedStyle(element);
        if (style.display === 'none' || style.visibility === 'hidden') continue;
        const rect = element.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;
        if (rect.left < -1 || rect.top < -1 || rect.right > viewportWidth + 1 || rect.bottom > viewportHeight + 1) {
          errors.push(`overflow:${element.tagName.toLowerCase()}.${element.className || '-'}`);
          break;
        }
      }
      const source = current.querySelector('.sources');
      const chrome = document.querySelector('.chrome');
      if (source && chrome && intersects(source.getBoundingClientRect(), chrome.getBoundingClientRect())) {
        errors.push('sources-overlap-controls');
      }
    }

    document.documentElement.dataset.visualCheck = errors.length ? 'fail' : 'ok';
    document.documentElement.dataset.visualErrors = errors.join('|');
  }

  function render({syncLocation = true} = {}) {
    const current = activeSlide();
    allSlides.forEach(slide => {
      const isActive = slide === current;
      slide.classList.toggle('active', isActive);
      slide.setAttribute('aria-hidden', isActive ? 'false' : 'true');
    });
    counter.textContent = appendixMode
      ? `A${index + 1} / A${appendixSlides.length}`
      : `${index + 1} / ${mainSlides.length}`;
    prev.disabled = index === 0;
    next.disabled = index === visibleSlides().length - 1;
    appendixToggle.classList.toggle('appendix-on', appendixMode);
    appendixToggle.setAttribute('aria-pressed', appendixMode ? 'true' : 'false');
    notesText.textContent = (current?.dataset.notes || 'No notes for this slide.').replace(/\\n/g, '\n');
    document.title = appendixMode
      ? `Appendix A${index + 1}/${appendixSlides.length} — LangDev 2026`
      : `Slide ${index + 1}/${mainSlides.length} — Build the Language, Then Make the Abstractions Disappear`;
    if (syncLocation) syncHash();
    runLayoutDiagnostics();
  }

  function go(delta) {
    const target = clamp(index + delta);
    if (target === index) return;
    index = target;
    render();
  }

  function toggleAppendix() {
    appendixMode = !appendixMode;
    index = appendixMode ? 0 : mainSlides.length - 1;
    render();
  }

  function isInteractiveTarget(target) {
    if (!(target instanceof Element)) return false;
    return Boolean(target.closest('button, a, input, textarea, select, summary, [contenteditable="true"], [role="button"]'));
  }

  prev.addEventListener('click', () => go(-1));
  next.addEventListener('click', () => go(1));
  appendixToggle.addEventListener('click', toggleAppendix);

  fullscreen.addEventListener('click', async () => {
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
      else await document.exitFullscreen();
    } catch (_) {
      // Browsers may deny fullscreen without direct user activation.
    }
  });

  notesToggle.addEventListener('click', () => {
    notesPanel.hidden = !notesPanel.hidden;
    notesToggle.setAttribute('aria-pressed', notesPanel.hidden ? 'false' : 'true');
    if (!notesPanel.hidden) notesPanel.scrollTop = 0;
  });

  window.addEventListener('hashchange', () => {
    parseHash();
    render({syncLocation: false});
  });

  window.addEventListener('keydown', event => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === 'Escape' && !notesPanel.hidden) {
      notesPanel.hidden = true;
      notesToggle.setAttribute('aria-pressed', 'false');
      return;
    }
    if (isInteractiveTarget(event.target)) return;

    const key = event.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(key)) {
      event.preventDefault();
      go(1);
    } else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(key)) {
      event.preventDefault();
      go(-1);
    } else if (key === 'Home') {
      event.preventDefault();
      index = 0;
      render();
    } else if (key === 'End') {
      event.preventDefault();
      index = visibleSlides().length - 1;
      render();
    } else if (key.toLowerCase() === 'a') {
      event.preventDefault();
      toggleAppendix();
    } else if (key.toLowerCase() === 'f') {
      event.preventDefault();
      fullscreen.click();
    } else if (key.toLowerCase() === 'n') {
      event.preventDefault();
      notesToggle.click();
    }
  });

  let touchStartX = null;
  window.addEventListener('touchstart', event => {
    if (event.touches.length === 1) touchStartX = event.touches[0].clientX;
  }, {passive: true});
  window.addEventListener('touchend', event => {
    if (touchStartX == null || event.changedTouches.length !== 1) return;
    const delta = event.changedTouches[0].clientX - touchStartX;
    touchStartX = null;
    if (Math.abs(delta) > 55) go(delta < 0 ? 1 : -1);
  }, {passive: true});

  parseHash();
  render({syncLocation: false});
})();
