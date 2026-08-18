const slides = [...document.querySelectorAll('.slide')];
    const prog = document.getElementById('prog');
    const count = document.getElementById('count');
    const notes = document.getElementById('notes');
    const notesP = notes.querySelector('p');
    const toc = document.getElementById('toc');
    const tocGrid = document.getElementById('tocGrid');
    let i = Number(location.hash.replace('#','')) || 1; i = Math.max(1, Math.min(slides.length, i)) - 1;
    function titleOf(s){ const h=s.querySelector('h1,h2'); return h ? h.textContent.replace(/\s+/g,' ').trim() : 'Slide'; }
    slides.forEach((s, idx)=>{ const b=document.createElement('button'); b.textContent=(idx+1)+'. '+titleOf(s); b.onclick=()=>{go(idx); toc.classList.remove('show')}; tocGrid.appendChild(b); });
    function go(n){ slides[i].classList.remove('active'); i=(n+slides.length)%slides.length; slides[i].classList.add('active'); prog.style.width=((i+1)/slides.length*100)+'%'; count.textContent=(i+1)+' / '+slides.length; notesP.textContent=slides[i].dataset.notes || ''; history.replaceState(null,'','#'+(i+1)); }
    document.getElementById('prev').onclick=()=>go(i-1); document.getElementById('next').onclick=()=>go(i+1); document.getElementById('notesBtn').onclick=()=>notes.classList.toggle('show'); document.getElementById('tocBtn').onclick=()=>toc.classList.toggle('show');
    document.addEventListener('keydown', e=>{ if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)} if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(i-1)} if(e.key.toLowerCase()==='n') notes.classList.toggle('show'); if(e.key.toLowerCase()==='t') toc.classList.toggle('show'); if(e.key.toLowerCase()==='p') window.print(); if(e.key==='Escape'){notes.classList.remove('show');toc.classList.remove('show')} });
    go(i);
