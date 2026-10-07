# LangDev 2026 — final production visual QA

Reviewed 2026-10-07. Production artifact: `index.html`. Final deck revision under visual QA: `ad114ab509e23386728d3e484401d9ae64cd4ee5`.

## Verdict

**PRESENTATION READY**

The production deck has **18 slides**, a **21:30 editorial rehearsal allocation** excluding audience Q&A, and a fixed 16:9 design surface. The visual language remains unchanged: dark technical background, cyan/violet/green semantic accents, code-first engineering diagrams and restrained card use.

This report is based on rendered browser output, not source inspection alone.

## Required rendered QA completed

After the final repairs, every slide was rendered again at all required viewports:

| Viewport | Slides rendered and visually inspected |
|---|---:|
| 1920×1080 | 18 / 18 |
| 1536×864 | 18 / 18 |
| 1366×768 | 18 / 18 |
| **Required viewport × slide combinations** | **54** |

Staged reveals were captured again at 1920×1080. There are **56 rendered reveal states** including initial states, every intermediate reveal and final states. Slide 17 has no staged reveal.

The checked contact sheets are in the ignored local QA workspace under `qa-final-visual/`:
- `before-contact-sheet.png` — historical baseline at `4fdca2d`;
- `after-contact-sheet.png` — accepted 1920×1080 revision;
- `after-1536x864-contact-sheet.png`;
- `after-1366x768-contact-sheet.png`;
- `reveal-sheets/reveal-01-12.png` … `reveal-49-56.png`.

## Findings and repairs

### Slide 18 — P0 — presenter/navigation state could fail on the new contact slide

**Problem:** after slide 18 was added, the short-notes map still ended at slide 17. Navigation to slide 18 could reach `updateNotes()` with no note entry.

**Why it mattered:** the final slide could render but navigation/presenter state was not reliable.

**Fix:** slide 18 now owns a complete short-note record and the deck validator expects all 18 slides and `End → 18`.

### Slide 18 — P0 — QR codes depended on an external image service

**Problem:** all four QR images were loaded from `api.qrserver.com`. With browser networking disabled, the rendered QR areas became blank broken images.

**Why it mattered:** the deck is intended to be usable locally/on a projector. The final slide's primary interaction must not fail because venue Wi-Fi or an external service is unavailable.

**Fix:** the four QR codes are now embedded directly in `index.html` as PNG data URIs. The validator switches the browser offline, opens `file://...#slide-18`, asserts four loaded QR images with non-zero natural dimensions, and captures `offline-contact-slide.png`.

The four embedded QRs were also decoded from their final PNG bytes and resolve to:
- live deck: `https://misha1302.github.io/lang-dev-presentation-2026/`;
- project: `https://github.com/Misha1302/Wist2`;
- Telegram: `https://t.me/Micodiy`;
- email: `mailto:razakov.mikhail@outlook.com`.

### Slide 18 — P1 — contact grid looked like a five-card layout with one card removed

**Problem:** after removing the GitHub-profile card, the grid still used the previous five-column geometry; secondary text was undersized and the QR cards did not feel intentionally recomposed.

**Fix:** the contact slide uses four equal columns, larger secondary text, equal centered QR geometry, safe wrapping for the email card and deliberate footer spacing.

### Slide 18 — P2 — duplicate slide count

**Problem:** the contact slide had a local `18 / 18` marker in addition to the deck-wide navigation counter.

**Fix:** the local duplicate was removed so navigation chrome has a single owner.

No additional P0/P1 issue was found on slides 1–17 in the final rendered pass.

## Final automated browser run

Command:

```bash
python scripts/validate_deck.py --output qa-final-candidate
```

Observed result:

| Check | Result |
|---|---|
| Slides | 18 |
| Timing metadata | 1290 s |
| Validator full-slide screenshots | 36: 18 at 1600×900 + 18 at 1920×1080 |
| Required final visual screenshots | 54: 18 each at 1920×1080, 1536×864, 1366×768 |
| Reveal captures | 56 |
| Embedded font faces | 7 |
| JavaScript errors | 0 |
| Geometry issue groups | 0 |
| Keyboard/arrows/dots/hash navigation | passed |
| Wheel/touch navigation | passed |
| Local-file opening | passed |
| Responsive fit / letterboxing | passed |
| Offline contact slide | passed |
| Embedded QR decode | 4 / 4 |

## Visual review notes

- No visible overflow, clipping or panel collisions remain at the three required 16:9 viewports.
- Header, kicker, claims, sources and navigation chrome remain aligned across the deck.
- Slides 6–8 remain the densest engineering slides, but code and route diagrams stay readable and preserve hierarchy.
- Slides 11–14 preserve the intended proof/provenance progression; reveal steps expose evidence before conclusions without layout shifts.
- Slide 15 is dense by design but remains legible at 1366×768 and does not cross safe margins.
- Slide 18 now remains functional with networking disabled; QR cards keep equal visual mass and quiet zones.
- Reveal states use opacity only, so neighboring geometry does not jump when staged content appears.

## Intentional non-changes

- The deck was not redesigned: color system, typography hierarchy, technical semantics and narrative structure were preserved.
- Presenter notes/help remain explicit on-demand overlays; they are not part of the audience-facing slide state and were not converted into a separate presenter-console redesign.
- Source links remain clickable external evidence. They are optional follow-up links, not rendering dependencies.

## Evidence boundary

The proposed semantic proof layer and SIMD example remain explicitly proposals. The deck does not claim production SIMD, formal completeness, measured speedup or novelty. Existing compiler/runtime claims and evidence boundaries remain unchanged by this visual QA pass.
