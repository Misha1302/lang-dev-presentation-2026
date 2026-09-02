const DECK_QA_CONTRACT = 'planning-core-v3';
document.documentElement.dataset.deckQaContract = DECK_QA_CONTRACT;

const presenterStyles = document.createElement('link');
presenterStyles.rel = 'stylesheet';
presenterStyles.href = 'presenter.css';
presenterStyles.dataset.presenterStyles = 'true';
document.head.appendChild(presenterStyles);

const allSlides = [...document.querySelectorAll('.slide')];
const mainSlides = allSlides.filter(s => s.dataset.kind !== 'appendix');
const appendixSlides = allSlides.filter(s => s.dataset.kind === 'appendix');
const prog = document.getElementById('prog');
const count = document.getElementById('count');
const notes = document.getElementById('notes');
const toc = document.getElementById('toc');
const tocGrid = document.getElementById('tocGrid');
const notesBtn = document.getElementById('notesBtn');
const tocBtn = document.getElementById('tocBtn');
const appendixBtn = document.getElementById('appendixBtn');
const NOTE_MARKERS = ['ЗАЧЕМ', 'СКАЗАТЬ', 'ПЕРЕХОД', 'ДЕТАЛЬ', 'НЕ ПЕРЕОБЕЩАТЬ'];
const PRESENTER_QUERY = 'presenter';
let showAppendix = false;
let presenterMode = false;
let slides = [];
let i = 0;

function titleOf(s){
  const h = s.querySelector('h1,h2');
  return h ? h.textContent.replace(/\s+/g, ' ').trim() : 'Slide';
}
function rectsOverlap(a,b){
  return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
}
function presenterRequested(){
  return new URLSearchParams(location.search).get(PRESENTER_QUERY) === '1';
}
function visibleSlides(){
  return allSlides.filter(s => showAppendix ? s.dataset.kind === 'appendix' : s.dataset.kind !== 'appendix');
}
function writeCurrentUrl(hash){
  const url = new URL(location.href);
  url.hash = hash;
  history.replaceState(null, '', url.pathname + url.search + url.hash);
}
function syncPresenterUrl(){
  const url = new URL(location.href);
  if(presenterMode) url.searchParams.set(PRESENTER_QUERY, '1');
  else url.searchParams.delete(PRESENTER_QUERY);
  history.replaceState(null, '', url.pathname + url.search + url.hash);
}
function parseNoteSections(note){
  const text = String(note || '').trim();
  if(!text) return [];
  const pattern = /(ЗАЧЕМ|СКАЗАТЬ|ПЕРЕХОД|ДЕТАЛЬ|НЕ ПЕРЕОБЕЩАТЬ):\s*/g;
  const matches = [...text.matchAll(pattern)];
  if(!matches.length) return [{label:'NOTES', body:text}];
  const sections = [];
  if(matches[0].index > 0){
    const preface = text.slice(0, matches[0].index).trim();
    if(preface) sections.push({label:'NOTES', body:preface});
  }
  matches.forEach((match, index) => {
    const start = match.index + match[0].length;
    const end = index + 1 < matches.length ? matches[index + 1].index : text.length;
    sections.push({label:match[1], body:text.slice(start, end).trim()});
  });
  return sections.filter(section => section.body);
}
function ensurePresenterPanel(){
  if(notes.dataset.presenterReady === 'true') return;
  notes.replaceChildren();
  const header = document.createElement('header');
  header.className = 'presenter-note-header';
  const slideCount = document.createElement('div');
  slideCount.className = 'presenter-slide-count';
  slideCount.id = 'presenterSlideCount';
  const title = document.createElement('h2');
  title.className = 'presenter-slide-title';
  title.id = 'presenterSlideTitle';
  header.append(slideCount, title);
  const body = document.createElement('div');
  body.className = 'presenter-note-sections';
  body.id = 'presenterNoteSections';
  notes.append(header, body);
  notes.dataset.presenterReady = 'true';
  notes.setAttribute('aria-label', 'Speaker notes for current slide');
}
function renderPresenterNotes(){
  ensurePresenterPanel();
  const slide = slides[i];
  if(!slide) return;
  const slideCount = document.getElementById('presenterSlideCount');
  const title = document.getElementById('presenterSlideTitle');
  const body = document.getElementById('presenterNoteSections');
  const suffix = showAppendix ? ' · APPENDIX' : '';
  slideCount.textContent = `SLIDE ${i + 1} / ${slides.length}${suffix}`;
  title.textContent = titleOf(slide);
  body.replaceChildren();
  const canonicalNote = slide.dataset.notes || window.SPEAKER_NOTES?.[slide.dataset.noteKey] || '';
  for(const section of parseNoteSections(canonicalNote)){
    const wrapper = document.createElement('section');
    wrapper.className = 'presenter-note-section';
    wrapper.dataset.noteSection = section.label;
    const heading = document.createElement('h3');
    heading.textContent = section.label;
    const paragraph = document.createElement('p');
    paragraph.textContent = section.body;
    wrapper.append(heading, paragraph);
    body.appendChild(wrapper);
  }
  notes.scrollTop = 0;
  notes.dataset.noteKey = slide.dataset.noteKey || '';
}
function updatePresenterLayout(){
  if(!presenterMode || window.innerWidth < 1100){
    document.documentElement.style.removeProperty('--presenter-scale');
    document.documentElement.style.removeProperty('--presenter-deck-left');
    document.documentElement.style.removeProperty('--presenter-deck-top');
    document.documentElement.style.removeProperty('--presenter-panel-px');
    document.documentElement.style.removeProperty('--presenter-left-px');
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
  const rootStyle = document.documentElement.style;
  rootStyle.setProperty('--presenter-scale', String(scale));
  rootStyle.setProperty('--presenter-deck-left', `${left}px`);
  rootStyle.setProperty('--presenter-deck-top', `${top}px`);
  rootStyle.setProperty('--presenter-panel-px', `${panelWidth}px`);
  rootStyle.setProperty('--presenter-left-px', `${leftWidth}px`);
}
function setPresenterMode(enabled, {syncUrl = true} = {}){
  presenterMode = Boolean(enabled);
  document.body.classList.toggle('presenter-mode', presenterMode);
  notes.classList.toggle('show', presenterMode);
  notesBtn.setAttribute('aria-pressed', String(presenterMode));
  notesBtn.textContent = presenterMode ? 'Audience' : 'Notes';
  if(syncUrl) syncPresenterUrl();
  updatePresenterLayout();
  renderPresenterNotes();
  requestAnimationFrame(runLayoutDiagnostics);
}
function togglePresenterMode(){
  setPresenterMode(!presenterMode);
}
function runLayoutDiagnostics(){
  if(new URLSearchParams(location.search).get('visual-check') !== '1') return;
  const active = document.querySelector('.slide.active');
  const errors = [];
  if(!active) errors.push('no-active-slide');
  if(active){
    const w = document.documentElement.clientWidth;
    const h = document.documentElement.clientHeight;
    for(const el of [active, ...active.querySelectorAll('*')]){
      const style = getComputedStyle(el);
      if(style.display === 'none' || style.visibility === 'hidden') continue;
      const r = el.getBoundingClientRect();
      if(r.width < 1 || r.height < 1) continue;
      if(r.left < -2 || r.top < -2 || r.right > w + 2 || r.bottom > h + 2){
        errors.push(`overflow:${el.tagName.toLowerCase()}.${String(el.className || '-').replace(/\s+/g,'.')}`);
        break;
      }
    }
    const nav = document.querySelector('nav');
    if(nav){
      const navRect = nav.getBoundingClientRect();
      for(const el of active.querySelectorAll('.sourcebar a,.sourcebar span')){
        if(rectsOverlap(el.getBoundingClientRect(), navRect)){
          errors.push('overlap:sourcebar-navigation');
          break;
        }
      }
    }
    if(presenterMode && window.innerWidth >= 1100){
      const slideRect = document.getElementById('deck').getBoundingClientRect();
      const notesRect = notes.getBoundingClientRect();
      if(slideRect.right > notesRect.left - 8) errors.push('collision:presentation-speaker-panel');
      if(slideRect.left < -2 || slideRect.top < -2 || slideRect.bottom > h + 2) errors.push('clipping:presentation-surface');
      const navRect = document.querySelector('nav')?.getBoundingClientRect();
      if(navRect && rectsOverlap(navRect, notesRect)) errors.push('collision:navigation-speaker-panel');
      if(notes.scrollWidth > notes.clientWidth + 2) errors.push('overflow:speaker-panel-x');
    }
  }
  document.documentElement.dataset.visualCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.visualErrors = errors.join('|');
}
function rebuildToc(){
  tocGrid.innerHTML='';
  slides.forEach((s, idx)=>{
    const b=document.createElement('button');
    b.textContent=(idx+1)+'. '+titleOf(s);
    if(s.dataset.kind === 'appendix') b.dataset.appendix = 'true';
    b.onclick=()=>{go(idx); toc.classList.remove('show')};
    tocGrid.appendChild(b);
  });
}
function readHash(){
  const raw = location.hash.replace('#','');
  if(!raw){ showAppendix = false; return 0; }
  if(raw.startsWith('a')){
    showAppendix = true;
    const n = Number(raw.slice(1)) || 1;
    const target = appendixSlides[Math.max(0, Math.min(appendixSlides.length - 1, n - 1))];
    slides = visibleSlides();
    return Math.max(0, slides.indexOf(target));
  }
  showAppendix = false;
  return Math.max(0, Math.min((Number(raw) || 1) - 1, visibleSlides().length - 1));
}
function refresh(targetIndex){
  slides = visibleSlides();
  if(appendixBtn) appendixBtn.textContent = showAppendix ? 'Main' : 'Appendix';
  allSlides.forEach(s => s.classList.remove('active'));
  i = Math.max(0, Math.min(targetIndex ?? i, slides.length - 1));
  rebuildToc();
  go(i, true);
}
function go(n, replaceHash=false){
  allSlides.forEach(s => s.classList.remove('active'));
  i=(n+slides.length)%slides.length;
  slides[i].classList.add('active');
  prog.style.width=((i+1)/slides.length*100)+'%';
  count.textContent=(i+1)+' / '+slides.length + (showAppendix ? ' · appendix' : '');
  renderPresenterNotes();
  const appIndex = appendixSlides.indexOf(slides[i]);
  const hash = appIndex >= 0 ? '#a'+(appIndex+1) : '#'+(mainSlides.indexOf(slides[i])+1);
  writeCurrentUrl(hash);
  runLayoutDiagnostics();
}

document.getElementById('prev').onclick=()=>go(i-1);
document.getElementById('next').onclick=()=>go(i+1);
notesBtn.setAttribute('aria-label', 'Toggle presenter mode');
notesBtn.setAttribute('aria-pressed', 'false');
notesBtn.onclick=togglePresenterMode;
tocBtn.setAttribute('aria-label', 'Toggle table of contents');
tocBtn.onclick=()=>toc.classList.toggle('show');
appendixBtn.onclick=()=>{showAppendix=!showAppendix;refresh(0)};
document.addEventListener('keydown', e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}
  if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}
  if(e.key.toLowerCase()==='n') togglePresenterMode();
  if(e.key.toLowerCase()==='t') toc.classList.toggle('show');
  if(e.key.toLowerCase()==='a'){showAppendix=!showAppendix;refresh(0)}
  if(e.key.toLowerCase()==='f'){
    if(document.fullscreenElement) document.exitFullscreen?.();
    else document.documentElement.requestFullscreen?.();
  }
  if(e.key.toLowerCase()==='p') window.print();
  if(e.key==='Escape') toc.classList.remove('show');
});
window.addEventListener('hashchange',()=>refresh(readHash()));
window.addEventListener('resize',()=>{updatePresenterLayout(); requestAnimationFrame(runLayoutDiagnostics)});

function runNavigationDiagnostics(){
  if(new URLSearchParams(location.search).get('nav-check') !== '1') return;
  const errors = [];
  const expect = (condition, message)=>{ if(!condition) errors.push(message); };
  const activeKey = ()=>document.querySelector('.slide.active')?.dataset.noteKey;
  const setHash = hash=>{ writeCurrentUrl(hash); window.dispatchEvent(new HashChangeEvent('hashchange')); };
  const key = value=>document.dispatchEvent(new KeyboardEvent('keydown',{key:value,bubbles:true,cancelable:true}));
  const firstMain = mainSlides[0]?.dataset.noteKey;
  const secondMain = mainSlides[1]?.dataset.noteKey;
  const lastMainHash = '#'+mainSlides.length;
  const lastMainKey = mainSlides.at(-1)?.dataset.noteKey;
  const firstAppendix = appendixSlides[0]?.dataset.noteKey;
  const lastAppendixHash = '#a'+appendixSlides.length;
  const lastAppendixKey = appendixSlides.at(-1)?.dataset.noteKey;

  setHash('#1'); expect(activeKey()===firstMain && count.textContent.startsWith(`1 / ${mainSlides.length}`),'deep-first-main');
  key('n');
  expect(presenterMode && document.body.classList.contains('presenter-mode'),'Presenter-N-on');
  expect(activeKey()===firstMain,'Presenter-toggle-keeps-slide');
  expect(notes.dataset.noteKey===firstMain && document.getElementById('presenterNoteSections')?.textContent.trim().length>0,'Presenter-notes-current');
  key('ArrowRight');
  expect(activeKey()===secondMain && notes.dataset.noteKey===secondMain,'Presenter-next-sync');
  key('n');
  expect(!presenterMode && activeKey()===secondMain,'Presenter-N-off');
  key('ArrowLeft'); expect(activeKey()===firstMain && location.hash==='#1','ArrowLeft');
  key('PageDown'); expect(activeKey()===secondMain,'PageDown');
  key('PageUp'); expect(activeKey()===firstMain,'PageUp');
  key(' '); expect(activeKey()===secondMain,'Space');
  setHash(lastMainHash); expect(activeKey()===lastMainKey && count.textContent.startsWith(`${mainSlides.length} / ${mainSlides.length}`),'deep-last-main');
  setHash('#a1'); expect(activeKey()===firstAppendix && count.textContent.startsWith(`1 / ${appendixSlides.length} · appendix`),'deep-first-appendix');
  setPresenterMode(true);
  expect(notes.dataset.noteKey===firstAppendix,'Presenter-appendix-notes');
  setHash(lastAppendixHash); expect(activeKey()===lastAppendixKey && notes.dataset.noteKey===lastAppendixKey,'Presenter-appendix-sync');
  setPresenterMode(false);
  setHash('#1'); appendixBtn.click(); expect(activeKey()===firstAppendix && location.hash==='#a1' && appendixBtn.textContent==='Main','Appendix-button');
  appendixBtn.click(); expect(activeKey()===firstMain && location.hash==='#1' && appendixBtn.textContent==='Appendix','Main-button');
  tocBtn.click();
  expect(toc.classList.contains('show') && tocGrid.querySelectorAll('button').length===mainSlides.length,'TOC-open');
  tocGrid.querySelectorAll('button')[Math.min(2, mainSlides.length - 1)]?.click();
  expect(activeKey()===mainSlides[Math.min(2, mainSlides.length - 1)]?.dataset.noteKey && !toc.classList.contains('show'),'TOC-navigate');
  notesBtn.click();
  expect(presenterMode && notes.classList.contains('show') && notes.dataset.noteKey===activeKey(),'Notes-button-on');
  tocBtn.click();
  key('Escape');
  expect(presenterMode && notes.classList.contains('show') && !toc.classList.contains('show'),'Escape-keeps-presenter');
  key('n');
  expect(!presenterMode && !notes.classList.contains('show'),'Presenter-cleanup');
  setHash('#1');
  document.documentElement.dataset.navCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.navErrors = errors.join('|');
}

refresh(readHash());
setPresenterMode(presenterRequested(), {syncUrl:false});
runNavigationDiagnostics();
presenterStyles.addEventListener('load', ()=>{
  document.documentElement.dataset.presenterStyles = 'ready';
  updatePresenterLayout();
  requestAnimationFrame(runLayoutDiagnostics);
});
presenterStyles.addEventListener('error', ()=>{
  document.documentElement.dataset.presenterStyles = 'error';
  requestAnimationFrame(runLayoutDiagnostics);
});
