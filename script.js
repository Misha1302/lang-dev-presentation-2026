document.documentElement.classList.add('js', 'slide-paging');

const progressBar = document.getElementById('progressBar');
const sections = [...document.querySelectorAll('main section[id]')];
const narrativeSections = [...document.querySelectorAll('main > section.scene[id]')];
const navLinks = [...document.querySelectorAll('.chapter-nav a')];
const revealItems = [...document.querySelectorAll('.reveal')];
const climax = document.querySelector('[data-climax]');
const toggle = document.getElementById('chapterToggle');
const nav = document.getElementById('chapterNav');
const topbar = document.querySelector('.topbar');
const appendix = document.getElementById('appendix');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const getHeaderOffset = () => Math.max(76, Math.ceil((topbar?.offsetHeight || 58) + 18));
const targetY = (el) => Math.max(0, Math.round(window.scrollY + el.getBoundingClientRect().top - getHeaderOffset()));

let sectionScrollFrame = 0;
let animationEpoch = 0;
let pagingInFlight = false;

const cancelSectionScroll = () => {
  animationEpoch += 1;
  if (sectionScrollFrame) cancelAnimationFrame(sectionScrollFrame);
  sectionScrollFrame = 0;
  pagingInFlight = false;
};

const goToY = (rawTarget) => {
  const maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
  const target = Math.max(0, Math.min(maxScroll, Math.round(rawTarget)));
  const start = window.scrollY;
  const distance = target - start;

  cancelSectionScroll();
  const epoch = animationEpoch;

  if (reduceMotion || Math.abs(distance) < 2) {
    window.scrollTo(0, target);
    updateProgress();
    return;
  }

  pagingInFlight = true;
  const duration = Math.min(500, Math.max(320, 300 + (Math.abs(distance) / Math.max(1, window.innerHeight)) * 95));
  const startedAt = performance.now();
  const ease = (t) => 1 - Math.pow(1 - t, 4);

  const step = (now) => {
    if (epoch !== animationEpoch) return;
    const t = Math.min(1, (now - startedAt) / duration);
    window.scrollTo(0, start + distance * ease(t));
    if (t < 1) {
      sectionScrollFrame = requestAnimationFrame(step);
      return;
    }

    sectionScrollFrame = 0;
    pagingInFlight = false;
    window.scrollTo(0, target);
    updateProgress();
  };

  sectionScrollFrame = requestAnimationFrame(step);
};

const goToSection = (el) => {
  if (el) goToY(targetY(el));
};

/*
  The talk is longer than one viewport in several places. Treating every section
  as a single slide would make lower content unreachable. Instead, each semantic
  scene gets one or more viewport-sized paging stops, while section boundaries
  remain exact anchor points. The appendix deliberately returns to ordinary
  continuous scrolling.
*/
let slideStops = [];
let appendixEntryY = Infinity;

const buildSlideStops = () => {
  const viewport = Math.max(1, window.innerHeight);
  const header = getHeaderOffset();
  const usable = Math.max(360, viewport - header - 20);
  const stride = Math.max(340, Math.round(usable * 0.92));
  const nextStops = [];

  const addStop = (y, sectionId, kind) => {
    const maxScroll = Math.max(0, document.documentElement.scrollHeight - viewport);
    const clamped = Math.max(0, Math.min(maxScroll, Math.round(y)));
    const previous = nextStops[nextStops.length - 1];
    if (previous && Math.abs(previous.y - clamped) < 44) return;
    nextStops.push({ y: clamped, sectionId, kind });
  };

  narrativeSections.forEach((section) => {
    const start = Math.max(0, section.offsetTop - header);
    const lastUseful = Math.max(start, section.offsetTop + section.offsetHeight - viewport);

    addStop(start, section.id, 'scene-start');

    let cursor = start + stride;
    while (cursor < lastUseful - 100) {
      addStop(cursor, section.id, 'scene-page');
      cursor += stride;
    }

    if (lastUseful > start + 120) addStop(lastUseful, section.id, 'scene-end');
  });

  if (appendix) {
    appendixEntryY = Math.max(0, appendix.offsetTop - header);
    addStop(appendixEntryY, 'appendix', 'appendix-entry');
  } else {
    appendixEntryY = Infinity;
  }

  slideStops = nextStops.sort((a, b) => a.y - b.y);
};

const pagingTarget = (direction) => {
  const y = window.scrollY;
  const tolerance = 28;

  if (direction > 0) {
    if (y >= appendixEntryY - tolerance) return null;
    return slideStops.find((stop) => stop.y > y + tolerance) || null;
  }

  /* Deep inside the appendix, keep native scrolling until its top is reached. */
  if (y > appendixEntryY + 96) return null;

  for (let i = slideStops.length - 1; i >= 0; i -= 1) {
    if (slideStops[i].y < y - tolerance) return slideStops[i];
  }
  return null;
};

const pageByDirection = (direction) => {
  const target = pagingTarget(direction);
  if (!target) return false;
  goToY(target.y);
  return true;
};

const navGroupForSection = (id) => {
  if (['opening','problem','semantics','baselines'].includes(id)) return 'problem';
  if (['capabilities','ownership','times'].includes(id)) return 'capabilities';
  if (['proof','evidence','lifecycle'].includes(id)) return 'proof';
  if (['erase','model'].includes(id)) return 'erase';
  return 'research';
};

const updateActiveChapter = () => {
  const cursor = window.scrollY + getHeaderOffset() + Math.min(220, window.innerHeight * 0.28);
  let current = sections[0]?.id;
  for (const section of sections) {
    if (section.offsetTop <= cursor) current = section.id;
    else break;
  }
  const activeGroup = navGroupForSection(current);
  navLinks.forEach((link) => link.classList.toggle('is-active', link.getAttribute('href') === `#${activeGroup}`));
};

const updateProgress = () => {
  const doc = document.documentElement;
  const max = Math.max(1, doc.scrollHeight - doc.clientHeight);
  const p = Math.min(1, Math.max(0, window.scrollY / max));
  progressBar.style.width = `${p * 100}%`;

  if (climax && !reduceMotion) {
    const stage = climax.querySelector('.climax-stage');
    const r = stage.getBoundingClientRect();
    const header = getHeaderOffset();
    const onScreen = r.bottom > header && r.top < window.innerHeight;
    climax.classList.toggle('is-mid', onScreen && r.top < window.innerHeight * 0.66);
    climax.classList.toggle('is-done', onScreen && r.top < window.innerHeight * 0.36);
  }

  updateActiveChapter();
};

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  revealItems.forEach((el) => revealObserver.observe(el));
} else {
  revealItems.forEach((el) => el.classList.add('is-visible'));
}

let scrollRaf = false;
window.addEventListener('scroll', () => {
  if (scrollRaf) return;
  scrollRaf = true;
  requestAnimationFrame(() => {
    updateProgress();
    scrollRaf = false;
  });
}, { passive: true });

let resizeTimer = 0;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(() => {
    cancelSectionScroll();
    buildSlideStops();
    updateProgress();
  }, 100);
}, { passive: true });

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
}

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const id = link.getAttribute('href')?.slice(1);
    const target = id ? document.getElementById(id) : null;
    if (!target) return;
    event.preventDefault();
    goToSection(target);
    if (nav) nav.classList.remove('is-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    history.replaceState(null, '', `#${id}`);
  });
});

/* One physical wheel / trackpad gesture advances one paging stop. Momentum from
   the same gesture is suppressed until the gesture has gone quiet. */
let wheelAccumulator = 0;
let wheelGestureLocked = false;
let lastWheelAt = 0;
let wheelUnlockTimer = 0;

const scheduleWheelUnlock = () => {
  clearTimeout(wheelUnlockTimer);
  wheelUnlockTimer = window.setTimeout(() => {
    const quietFor = performance.now() - lastWheelAt;
    if (quietFor >= 170 && !pagingInFlight) {
      wheelGestureLocked = false;
      wheelAccumulator = 0;
      return;
    }
    scheduleWheelUnlock();
  }, 90);
};

window.addEventListener('wheel', (event) => {
  if (event.ctrlKey || event.metaKey) return;
  if (Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
  if (!event.deltaY) return;

  const direction = Math.sign(event.deltaY);
  const target = pagingTarget(direction);
  if (!target) return;

  event.preventDefault();
  lastWheelAt = performance.now();
  scheduleWheelUnlock();

  if (wheelGestureLocked || pagingInFlight) return;

  wheelAccumulator += event.deltaY;
  const threshold = event.deltaMode === 1 ? 3 : event.deltaMode === 2 ? 1 : 46;
  if (Math.abs(wheelAccumulator) < threshold) return;

  wheelGestureLocked = true;
  wheelAccumulator = 0;
  goToY(target.y);
}, { passive: false });

/* Slide-style keyboard controls. Repeated keydown is intentionally ignored so
   holding a key cannot overshoot multiple pages. */
window.addEventListener('keydown', (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;

  const activeTag = document.activeElement?.tagName;
  if (['INPUT','TEXTAREA','SELECT','SUMMARY','BUTTON','A'].includes(activeTag)) return;

  let direction = 0;
  if (event.key === ' ' && event.shiftKey) direction = -1;
  else if (['ArrowDown','PageDown',' ','j','J'].includes(event.key) && !event.shiftKey) direction = 1;
  else if (['ArrowUp','PageUp','k','K'].includes(event.key) && !event.shiftKey) direction = -1;
  else return;

  const target = pagingTarget(direction);
  if (!target) return;

  event.preventDefault();
  if (event.repeat || pagingInFlight) return;
  goToY(target.y);
});

/* On touch screens the narrative behaves like a vertical presentation: one
   deliberate swipe = one paging stop. The appendix keeps native touch scroll. */
let touchStartX = 0;
let touchStartY = 0;
let touchControlsNarrative = false;

window.addEventListener('touchstart', (event) => {
  if (event.touches.length !== 1) return;
  const touch = event.touches[0];
  touchStartX = touch.clientX;
  touchStartY = touch.clientY;
  touchControlsNarrative = window.scrollY < appendixEntryY - 28;
}, { passive: true });

window.addEventListener('touchmove', (event) => {
  if (!touchControlsNarrative || event.touches.length !== 1) return;
  const touch = event.touches[0];
  const dx = touch.clientX - touchStartX;
  const dy = touch.clientY - touchStartY;
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 8) event.preventDefault();
}, { passive: false });

window.addEventListener('touchend', (event) => {
  if (!touchControlsNarrative || event.changedTouches.length !== 1 || pagingInFlight) {
    touchControlsNarrative = false;
    return;
  }

  const touch = event.changedTouches[0];
  const dx = touch.clientX - touchStartX;
  const dy = touch.clientY - touchStartY;
  touchControlsNarrative = false;

  if (Math.abs(dy) < 54 || Math.abs(dy) <= Math.abs(dx) * 1.15) return;
  pageByDirection(dy < 0 ? 1 : -1);
}, { passive: true });

buildSlideStops();
updateProgress();

