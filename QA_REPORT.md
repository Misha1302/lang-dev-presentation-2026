# QA report — slide-by-slide paging revision

## Scope

This revision changes navigation mechanics only. Talk content, narrative order, claim boundaries and diagrams were protected; the only audience-copy change is the opening navigation cue (`scroll · swipe · ↓ advance`).

## Implemented paging model

The narrative sections remain a continuous vertical document, but navigation now advances through deterministic page stops. A scene taller than the usable viewport receives extra stops, so paging cannot make lower content unreachable. Scene starts stay exact anchor targets. The Appendix/FAQ is deliberately outside scripted paging and keeps native continuous scrolling.

The implementation removes the old CSS `scroll-behavior: smooth` from the document. Animation is owned only by the JavaScript pager, preventing CSS smooth scrolling and the requestAnimationFrame animation from competing with each other.

## Browser verification

Chromium-class browser checks were run against the exact standalone build.

### Desktop — 1440 × 1000

- horizontal overflow: none (`scrollWidth == innerWidth == 1440`);
- paging stops: 28 at this viewport;
- one wheel gesture lands exactly on the next stop;
- a rapid momentum-like wheel burst lands on only one stop, with no overshoot;
- a second distinct gesture advances exactly one additional stop;
- reverse wheel returns exactly one stop;
- `ArrowDown`, `PageDown`, `Space`, and `J` advance exactly one stop;
- `ArrowUp`, `PageUp`, `Shift+Space`, and `K` move exactly one stop backward;
- repeated `keydown` events do not skip multiple pages;
- the complete ArrowDown traversal visited every stop in order; the complete ArrowUp traversal returned through every stop to `0`;
- chapter anchor test (`#proof`) landed at the exact calculated scene-start offset;
- no JavaScript page errors were observed.

### Mobile — 390 × 844

- horizontal overflow: none (`scrollWidth == innerWidth == 390`);
- one upward swipe advanced exactly one page stop;
- a second distinct swipe advanced exactly one further stop;
- one downward swipe returned exactly one stop;
- no JavaScript page errors were observed.

### Tablet / responsive checks

A 768 × 1024 touch viewport was also checked during implementation: no horizontal overflow and touch paging landed exactly on the computed stop.

### Reduced motion

With `prefers-reduced-motion: reduce`, paging still lands on the same deterministic stops, but motion is immediate rather than animated.

## Regression protection

A source diff confirmed that `index.html` content is unchanged except for the opening navigation cue. CSS changes are limited to removing global smooth scrolling and adding the paging foundation. Navigation behavior is isolated in `script.js`.

`node --check script.js` passes.