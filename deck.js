const DECK_QA_CONTRACT = 'architecture-story-v2';
document.documentElement.dataset.deckQaContract = DECK_QA_CONTRACT;
const VISUAL_CHECK_MODE = new URLSearchParams(location.search).get('visual-check') === '1';
if (VISUAL_CHECK_MODE) document.documentElement.classList.add('visual-check-mode');

const presenterStyles = document.createElement('link');
presenterStyles.rel = 'stylesheet';
presenterStyles.href = 'presenter.css';
presenterStyles.dataset.presenterStyles = 'true';
document.head.appendChild(presenterStyles);

const allSlides = [...document.querySelectorAll('.slide')];
const mainSlides = allSlides.filter(slide => slide.dataset.kind !== 'appendix');
const appendixSlides = allSlides.filter(slide => slide.dataset.kind === 'appendix');
const prog = document.getElementById('prog');
const count = document.getElementById('count');
const notes = document.getElementById('notes');
const toc = document.getElementById('toc');
const tocGrid = document.getElementById('tocGrid');
const notesBtn = document.getElementById('notesBtn');
const tocBtn = document.getElementById('tocBtn');
const appendixBtn = document.getElementById('appendixBtn');
const PRESENTER_QUERY = 'presenter';
let showAppendix = false;
let presenterMode = false;
let slides = [];
let i = 0;

function titleOf(slide) {
  const heading = slide.querySelector('h1,h2');
  if (!heading) return 'Slide';
  const copy = heading.cloneNode(true);
  copy.querySelectorAll('br').forEach(br => br.replaceWith(' '));
  return copy.textContent.replace(/\s+/g, ' ').trim();
}
function rectsOverlap(a, b) {
  return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
}
function presenterRequested() {
  return new URLSearchParams(location.search).get(PRESENTER_QUERY) === '1';
}
function visibleSlides() {
  return allSlides.filter(slide => showAppendix ? slide.dataset.kind === 'appendix' : slide.dataset.kind !== 'appendix');
}
function writeCurrentUrl(hash) {
  const url = new URL(location.href);
  url.hash = hash;
  history.replaceState(null, '', url.pathname + url.search + url.hash);
}
function syncPresenterUrl() {
  const url = new URL(location.href);
  if (presenterMode) url.searchParams.set(PRESENTER_QUERY, '1');
  else url.searchParams.delete(PRESENTER_QUERY);
  history.replaceState(null, '', url.pathname + url.search + url.hash);
}
function canonicalSpeech(slide) {
  const key = slide?.dataset.noteKey || '';
  return String(window.SPEAKER_SCRIPT?.[key] || '').trim();
}
function renderPresenterSpeech() {
  const slide = slides[i];
  if (!slide) return;
  const speech = canonicalSpeech(slide);
  notes.replaceChildren();
  for (const block of speech.split(/\n\s*\n/).map(text => text.trim()).filter(Boolean)) {
    const paragraph = document.createElement('p');
    paragraph.textContent = block;
    notes.appendChild(paragraph);
  }
  notes.scrollTop = 0;
  notes.dataset.noteKey = slide.dataset.noteKey || '';
  notes.dataset.canonicalOwner = 'speaker-script-canonical.js';
  notes.setAttribute('aria-label', 'Canonical spoken script for the current slide');
}
function updatePresenterLayout() {
  if (!presenterMode || window.innerWidth < 1100) {
    for (const property of ['--presenter-scale', '--presenter-deck-left', '--presenter-deck-top', '--presenter-panel-px', '--presenter-left-px']) {
      document.documentElement.style.removeProperty(property);
    }
    return;
  }
  const panelWidth = window.innerWidth * 0.32;
  const gap = window.innerWidth * 0.015;
  const leftWidth = window.innerWidth - panelWidth - gap;
  const horizontalPadding = Math.max(18, window.innerWidth * 0.012);
  const navReserve = Math.max(68, window.innerHeight * 0.075);
  const verticalPadding = Math.max(14, window.innerHeight * 0.018);
  const availableWidth = Math.max(1, leftWidth - 2 * horizontalPadding);
  const availableHeight = Math.max(1, window.innerHeight - navReserve - 2 * verticalPadding);
  const scale = Math.min(availableWidth / window.innerWidth, availableHeight / window.innerHeight);
  const scaledWidth = window.innerWidth * scale;
  const scaledHeight = window.innerHeight * scale;
  const left = Math.max(horizontalPadding, (leftWidth - scaledWidth) / 2);
  const top = Math.max(verticalPadding, (window.innerHeight - navReserve - scaledHeight) / 2);
  const style = document.documentElement.style;
  style.setProperty('--presenter-scale', String(scale));
  style.setProperty('--presenter-deck-left', `${left}px`);
  style.setProperty('--presenter-deck-top', `${top}px`);
  style.setProperty('--presenter-panel-px', `${panelWidth}px`);
  style.setProperty('--presenter-left-px', `${leftWidth}px`);
}
function setPresenterMode(enabled, {syncUrl = true} = {}) {
  presenterMode = Boolean(enabled);
  document.body.classList.toggle('presenter-mode', presenterMode);
  notes.classList.toggle('show', presenterMode);
  notesBtn.setAttribute('aria-pressed', String(presenterMode));
  notesBtn.textContent = presenterMode ? 'Audience' : 'Notes';
  if (syncUrl) syncPresenterUrl();
  updatePresenterLayout();
  renderPresenterSpeech();
  requestAnimationFrame(runLayoutDiagnostics);
}
function togglePresenterMode() {
  setPresenterMode(!presenterMode);
}
function runLayoutDiagnostics() {
  if (!VISUAL_CHECK_MODE) return;
  const active = document.querySelector('.slide.active');
  const errors = [];
  if (!active) errors.push('no-active-slide');
  if (active) {
    const width = document.documentElement.clientWidth;
    const height = document.documentElement.clientHeight;
    for (const element of [active, ...active.querySelectorAll('*')]) {
      const style = getComputedStyle(element);
      if (style.display === 'none' || style.visibility === 'hidden') continue;
      const rect = element.getBoundingClientRect();
      if (rect.width < 1 || rect.height < 1) continue;
      if (rect.left < -2 || rect.top < -2 || rect.right > width + 2 || rect.bottom > height + 2) {
        errors.push(`overflow:${element.tagName.toLowerCase()}.${String(element.className || '-').replace(/\s+/g, '.')}`);
        break;
      }
    }
    const nav = document.querySelector('nav');
    if (nav) {
      const navRect = nav.getBoundingClientRect();
      for (const element of active.querySelectorAll('.sourcebar a,.sourcebar span')) {
        if (rectsOverlap(element.getBoundingClientRect(), navRect)) {
          errors.push('overlap:sourcebar-navigation');
          break;
        }
      }
    }
    if (presenterMode) {
      const speech = canonicalSpeech(active);
      if (!speech) errors.push('presenter:missing-canonical-speech');
      if (notes.dataset.canonicalOwner !== 'speaker-script-canonical.js') errors.push('presenter:wrong-owner');
      if (notes.querySelector('h1,h2,h3,label')) errors.push('presenter:non-speech-label');
      const rendered = [...notes.querySelectorAll('p')].map(p => p.textContent.trim()).join('\n\n');
      if (rendered !== speech) errors.push('presenter:runtime-speech-mismatch');
    }
    if (presenterMode && window.innerWidth >= 1100) {
      const slideRect = document.getElementById('deck').getBoundingClientRect();
      const notesRect = notes.getBoundingClientRect();
      if (slideRect.right > notesRect.left - 8) errors.push('collision:presentation-speaker-panel');
      if (slideRect.left < -2 || slideRect.top < -2 || slideRect.bottom > height + 2) errors.push('clipping:presentation-surface');
      const navRect = document.querySelector('nav')?.getBoundingClientRect();
      if (navRect && rectsOverlap(navRect, notesRect)) errors.push('collision:navigation-speaker-panel');
      if (notes.scrollWidth > notes.clientWidth + 2) errors.push('overflow:speaker-panel-x');
    }
  }
  document.documentElement.dataset.visualCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.visualErrors = errors.join('|');
}
function rebuildToc() {
  tocGrid.innerHTML = '';
  slides.forEach((slide, index) => {
    const button = document.createElement('button');
    button.textContent = `${index + 1}. ${titleOf(slide)}`;
    if (slide.dataset.kind === 'appendix') button.dataset.appendix = 'true';
    button.onclick = () => { go(index); toc.classList.remove('show'); };
    tocGrid.appendChild(button);
  });
}
function readHash() {
  const raw = location.hash.replace('#', '');
  if (!raw) { showAppendix = false; return 0; }
  if (raw.startsWith('a')) {
    showAppendix = true;
    const number = Number(raw.slice(1)) || 1;
    const target = appendixSlides[Math.max(0, Math.min(appendixSlides.length - 1, number - 1))];
    slides = visibleSlides();
    return Math.max(0, slides.indexOf(target));
  }
  showAppendix = false;
  return Math.max(0, Math.min((Number(raw) || 1) - 1, visibleSlides().length - 1));
}
function refresh(targetIndex) {
  slides = visibleSlides();
  appendixBtn.textContent = showAppendix ? 'Main' : 'Appendix';
  allSlides.forEach(slide => slide.classList.remove('active'));
  i = Math.max(0, Math.min(targetIndex ?? i, slides.length - 1));
  rebuildToc();
  go(i, true);
}
function go(index) {
  allSlides.forEach(slide => slide.classList.remove('active'));
  i = (index + slides.length) % slides.length;
  slides[i].classList.add('active');
  prog.style.width = `${(i + 1) / slides.length * 100}%`;
  count.textContent = `${i + 1} / ${slides.length}${showAppendix ? ' · appendix' : ''}`;
  renderPresenterSpeech();
  const appendixIndex = appendixSlides.indexOf(slides[i]);
  const hash = appendixIndex >= 0 ? `#a${appendixIndex + 1}` : `#${mainSlides.indexOf(slides[i]) + 1}`;
  writeCurrentUrl(hash);
  runLayoutDiagnostics();
}

document.getElementById('prev').onclick = () => go(i - 1);
document.getElementById('next').onclick = () => go(i + 1);
notesBtn.setAttribute('aria-label', 'Toggle presenter mode');
notesBtn.setAttribute('aria-pressed', 'false');
notesBtn.onclick = togglePresenterMode;
tocBtn.setAttribute('aria-label', 'Toggle table of contents');
tocBtn.onclick = () => toc.classList.toggle('show');
appendixBtn.onclick = () => { showAppendix = !showAppendix; refresh(0); };
document.addEventListener('keydown', event => {
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); go(i + 1); }
  if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); go(i - 1); }
  if (event.key.toLowerCase() === 'n') togglePresenterMode();
  if (event.key.toLowerCase() === 't') toc.classList.toggle('show');
  if (event.key.toLowerCase() === 'a') { showAppendix = !showAppendix; refresh(0); }
  if (event.key.toLowerCase() === 'f') {
    if (document.fullscreenElement) document.exitFullscreen?.();
    else document.documentElement.requestFullscreen?.();
  }
  if (event.key.toLowerCase() === 'p') window.print();
  if (event.key === 'Escape') toc.classList.remove('show');
});
window.addEventListener('hashchange', () => refresh(readHash()));
window.addEventListener('resize', () => { updatePresenterLayout(); requestAnimationFrame(runLayoutDiagnostics); });

function runNavigationDiagnostics() {
  if (new URLSearchParams(location.search).get('nav-check') !== '1') return;
  const errors = [];
  const expect = (condition, message) => { if (!condition) errors.push(message); };
  const activeKey = () => document.querySelector('.slide.active')?.dataset.noteKey;
  const setHash = hash => { writeCurrentUrl(hash); window.dispatchEvent(new HashChangeEvent('hashchange')); };
  const key = value => document.dispatchEvent(new KeyboardEvent('keydown', {key: value, bubbles: true, cancelable: true}));
  const firstMain = mainSlides[0]?.dataset.noteKey;
  const secondMain = mainSlides[1]?.dataset.noteKey;
  const lastMainHash = `#${mainSlides.length}`;
  const lastMainKey = mainSlides.at(-1)?.dataset.noteKey;
  const firstAppendix = appendixSlides[0]?.dataset.noteKey;
  const lastAppendixHash = `#a${appendixSlides.length}`;
  const lastAppendixKey = appendixSlides.at(-1)?.dataset.noteKey;

  setHash('#1');
  expect(activeKey() === firstMain && count.textContent.startsWith(`1 / ${mainSlides.length}`), 'deep-first-main');
  key('n');
  expect(presenterMode && document.body.classList.contains('presenter-mode'), 'Presenter-N-on');
  expect(notes.dataset.noteKey === firstMain, 'Presenter-notes-current');
  expect(notes.textContent.trim() === window.SPEAKER_SCRIPT[firstMain].trim(), 'Presenter-canonical-runtime');
  key('ArrowRight');
  expect(activeKey() === secondMain && notes.dataset.noteKey === secondMain, 'Presenter-next-sync');
  key('n');
  expect(!presenterMode && activeKey() === secondMain, 'Presenter-N-off');
  key('ArrowLeft'); expect(activeKey() === firstMain && location.hash === '#1', 'ArrowLeft');
  key('PageDown'); expect(activeKey() === secondMain, 'PageDown');
  key('PageUp'); expect(activeKey() === firstMain, 'PageUp');
  key(' '); expect(activeKey() === secondMain, 'Space');
  setHash(lastMainHash); expect(activeKey() === lastMainKey, 'deep-last-main');
  setHash('#a1'); expect(activeKey() === firstAppendix, 'deep-first-appendix');
  setPresenterMode(true);
  expect(notes.dataset.noteKey === firstAppendix, 'Presenter-appendix-notes');
  setHash(lastAppendixHash); expect(activeKey() === lastAppendixKey && notes.dataset.noteKey === lastAppendixKey, 'Presenter-appendix-sync');
  setPresenterMode(false);
  setHash('#1'); appendixBtn.click(); expect(activeKey() === firstAppendix && location.hash === '#a1', 'Appendix-button');
  appendixBtn.click(); expect(activeKey() === firstMain && location.hash === '#1', 'Main-button');
  tocBtn.click();
  expect(toc.classList.contains('show') && tocGrid.querySelectorAll('button').length === mainSlides.length, 'TOC-open');
  tocGrid.querySelectorAll('button')[Math.min(2, mainSlides.length - 1)]?.click();
  expect(activeKey() === mainSlides[Math.min(2, mainSlides.length - 1)]?.dataset.noteKey && !toc.classList.contains('show'), 'TOC-navigate');
  notesBtn.click();
  expect(presenterMode && notes.classList.contains('show') && notes.dataset.noteKey === activeKey(), 'Notes-button-on');
  tocBtn.click(); key('Escape');
  expect(presenterMode && !toc.classList.contains('show'), 'Escape-keeps-presenter');
  key('n'); expect(!presenterMode && !notes.classList.contains('show'), 'Presenter-cleanup');
  setHash('#1');
  document.documentElement.dataset.navCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.navErrors = errors.join('|');
}

refresh(readHash());
setPresenterMode(presenterRequested(), {syncUrl: false});
runNavigationDiagnostics();
presenterStyles.addEventListener('load', () => {
  document.documentElement.dataset.presenterStyles = 'ready';
  updatePresenterLayout();
  requestAnimationFrame(runLayoutDiagnostics);
});
presenterStyles.addEventListener('error', () => {
  document.documentElement.dataset.presenterStyles = 'error';
  requestAnimationFrame(runLayoutDiagnostics);
});
