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
  }
  document.documentElement.dataset.visualCheck = errors.length ? 'fail' : 'ok';
  document.documentElement.dataset.visualErrors = errors.join('|');
}
function visibleSlides(){ return allSlides.filter(s => showAppendix || s.dataset.kind !== 'appendix'); }
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
  if(!raw) return 0;
  if(raw.startsWith('a')){
    showAppendix = true;
    const n = Number(raw.slice(1)) || 1;
    const app = allSlides.filter(s => s.dataset.kind === 'appendix');
    const target = app[Math.max(0, Math.min(app.length - 1, n - 1))];
    slides = visibleSlides();
    return Math.max(0, slides.indexOf(target));
  }
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
  count.textContent=(i+1)+' / '+slides.length + (showAppendix ? ' · appendix on' : '');
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
refresh(readHash());
