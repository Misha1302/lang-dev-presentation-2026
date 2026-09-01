const DECK_QA_CONTRACT = 'split-main-appendix-v1';
document.documentElement.dataset.deckQaContract = DECK_QA_CONTRACT;
const allSlides = [...document.querySelectorAll('.slide')];
const prog = document.getElementById('prog');
const count = document.getElementById('count');
const notes = document.getElementById('notes');
const notesP = notes.querySelector('p');
const toc = document.getElementById('toc');
const tocGrid = document.getElementById('tocGrid');
const appendixBtn = document.getElementById('appendixBtn');
let showAppendix = false;
let slides = [];
let i = 0;
function titleOf(s){ const h=s.querySelector('h1,h2'); return h ? h.textContent.replace(/\s+/g,' ').trim() : 'Slide'; }
function rectsOverlap(a,b){ return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top; }
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
  }
  document.documentElement.dataset.visualCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.visualErrors = errors.join('|');
}
function visibleSlides(){ return allSlides.filter(s => showAppendix ? s.dataset.kind === 'appendix' : s.dataset.kind !== 'appendix'); }
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
    const app = allSlides.filter(s => s.dataset.kind === 'appendix');
    const target = app[Math.max(0, Math.min(app.length - 1, n - 1))];
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
  notesP.textContent=slides[i].dataset.notes || '';
  const appIndex = allSlides.filter(s => s.dataset.kind === 'appendix').indexOf(slides[i]);
  const hash = appIndex >= 0 ? '#a'+(appIndex+1) : '#'+(allSlides.filter(s => s.dataset.kind !== 'appendix').indexOf(slides[i])+1);
  history.replaceState(null,'',hash);
  runLayoutDiagnostics();
}
document.getElementById('prev').onclick=()=>go(i-1);
document.getElementById('next').onclick=()=>go(i+1);
document.getElementById('notesBtn').onclick=()=>notes.classList.toggle('show');
document.getElementById('tocBtn').onclick=()=>toc.classList.toggle('show');
appendixBtn.onclick=()=>{showAppendix=!showAppendix;refresh(0)};
document.addEventListener('keydown', e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}
  if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}
  if(e.key.toLowerCase()==='n') notes.classList.toggle('show');
  if(e.key.toLowerCase()==='t') toc.classList.toggle('show');
  if(e.key.toLowerCase()==='a'){showAppendix=!showAppendix;refresh(0)}
  if(e.key.toLowerCase()==='f') document.documentElement.requestFullscreen?.();
  if(e.key.toLowerCase()==='p') window.print();
  if(e.key==='Escape'){notes.classList.remove('show');toc.classList.remove('show')}
});
window.addEventListener('hashchange',()=>refresh(readHash()));
function runNavigationDiagnostics(){
  if(new URLSearchParams(location.search).get('nav-check') !== '1') return;
  const errors = [];
  const expect = (condition, message)=>{ if(!condition) errors.push(message); };
  const activeKey = ()=>document.querySelector('.slide.active')?.dataset.noteKey;
  const setHash = hash=>{ history.replaceState(null,'',hash); window.dispatchEvent(new HashChangeEvent('hashchange')); };
  const key = value=>document.dispatchEvent(new KeyboardEvent('keydown',{key:value,bubbles:true,cancelable:true}));
  setHash('#1'); expect(activeKey()==='m1' && count.textContent.startsWith('1 / 16'),'deep-1');
  key('ArrowRight'); expect(activeKey()==='m2' && location.hash==='#2','ArrowRight');
  key('ArrowLeft'); expect(activeKey()==='m1' && location.hash==='#1','ArrowLeft');
  key('PageDown'); expect(activeKey()==='m2','PageDown');
  key('PageUp'); expect(activeKey()==='m1','PageUp');
  key(' '); expect(activeKey()==='m2','Space');
  setHash('#16'); expect(activeKey()==='m16' && count.textContent.startsWith('16 / 16'),'deep-16');
  setHash('#a1'); expect(activeKey()==='a1' && count.textContent.startsWith('1 / 8 · appendix'),'deep-a1');
  setHash('#a8'); expect(activeKey()==='a8' && count.textContent.startsWith('8 / 8 · appendix'),'deep-a8');
  setHash('#1'); appendixBtn.click(); expect(activeKey()==='a1' && location.hash==='#a1' && appendixBtn.textContent==='Main','Appendix-button');
  appendixBtn.click(); expect(activeKey()==='m1' && location.hash==='#1' && appendixBtn.textContent==='Appendix','Main-button');
  document.getElementById('tocBtn').click();
  expect(toc.classList.contains('show') && tocGrid.querySelectorAll('button').length===16,'TOC-open');
  tocGrid.querySelectorAll('button')[2]?.click();
  expect(activeKey()==='m3' && location.hash==='#3' && !toc.classList.contains('show'),'TOC-navigate');
  document.getElementById('notesBtn').click();
  expect(notes.classList.contains('show') && notesP.textContent.trim().length>0,'Notes-open');
  document.getElementById('tocBtn').click();
  key('Escape');
  expect(!notes.classList.contains('show') && !toc.classList.contains('show'),'Escape');
  setHash('#1');
  document.documentElement.dataset.navCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.navErrors = errors.join('|');
}
refresh(readHash());
runNavigationDiagnostics();
