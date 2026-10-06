# LangDev 2026 — final production review

Reviewed 2026-10-06. Artifact: the actual production `index.html`, not a mockup.

## Result

PASS for the reviewed Chromium/local-file presentation. **17 slides, 16:9, 21:25 rehearsal allocation**, excluding audience Q&A. Duration is an editorial allocation, not a measured speaker rehearsal.

The deck is self-contained: no font, CDN, network or server dependency is needed to present it. External evidence links are optional. The exported PDF has 17 pages.

## Completed passes

1. **Narrative / technical content:** inspected production source and full git history, pinned current compiler source, read architecture contracts, inspected implementations and tests, executed compiler evidence checks, then wrote the claim map and each slide's visible reasoning. Rebuilt the story around one real Wist program and one bounded proposed SIMD scenario.
2. **Visual composition:** restored connected module lanes, unresolved-to-resolved planning, an exact capability-gated AIR rewrite and narrowing abstraction layers. Different layouts show syntax, configuration, representations, binding identity, evidence derivation and provenance. Notes contain ANCHOR / FLOW / TRANSITION rather than a memorized script.
3. **Rendered QA / repairs:** opened the production file in Chromium; rendered and visually inspected all 17 slides at 1600×900, all staged-reveal contact sheets and the full-deck montage. Rendered all 17 slides again at 1920×1080. Automated geometry checks complement, rather than replace, screenshot inspection.

Screenshot-driven repairs included a long module label touching a connector, a compressed evidence-identity strip, a query node extending past the safe margin, a prior-art title pushing content downward, an unnecessary DAG label touching a node, and a crowded final narrowing diagram. The interpreter/CIL route changed from an ambiguous sequence into a genuine fork/join. Content and spacing were reduced without shrinking meaningful text below 16px.

The montage was checked for density, neighboring layout repetition, color balance and continuity. Code, lanes, comparisons, DAG, provenance path, narrowing pipeline and hero statements provide visual rhythm. Final reveal inspection confirmed reasoning appears in order without changing the underlying layout.

## Final automated browser run

```bash
python scripts/validate_deck.py --output qa/final
```

| Check | Observed result |
|---|---|
| Full-slide captures | 34: 17 at 1600×900 and 17 at 1920×1080 |
| Reveal captures | 53 states, including initial and completed states |
| Geometry issue groups | 0 |
| JavaScript errors | 0 |
| Embedded fonts | Seven bundled WOFF2 faces; loading checked explicitly |
| Meaningful text / panel bounds | Passed at both desktop sizes and every reveal state |
| Slide IDs, counters, notes, step continuity | Passed |
| Keyboard, arrows, dots, hashes, wheel debounce | Passed |
| Notes/help visibility and reveal completion | Passed |
| Touch swipe handler | Passed with synthetic touch events; not a physical-device test |
| Direct local-file opening and navigation | Passed |
| Uniform fitting / letterboxing | Passed at 1280×720, 1024×768 and 390×844 |
| Printable slide count | 17 pages, checked with pdfinfo |
| JavaScript syntax / whitespace | Node syntax check and git diff --check |

Artifacts: `qa/final/validation.json`, `montage.png`, full-resolution slides, reveal contact sheets and `LangDev-2026.pdf`. They are ignored by Git; the validator and CI workflow are checked-in source. Fullscreen uses the browser API and was not validated as a real projector/OS session. Other browser engines were not tested in this final run.

## Narrative and audience review

Transitions were checked as consequences of preceding slides, not simply topic changes:

- A formula needs several stages → a feature owns several contributions → selecting them changes the language (1–4).
- Selection leaves global choices unresolved → LanguagePlan resolves them → the program becomes concrete Bytecode/AIR/backend operations (4–7).
- Representations differ while meaning must agree → binding parity makes that observable → future transformations need premises with several owners (7–9).
- Producer-specific coupling → semantic obligation → visible proof → a new producer helps the unchanged consumer (10–12).
- Evidence needs identity → provenance also defines when an answer becomes stale → compare that integration boundary with serious precedents (13–15).
- Execution consumes resolved decisions → return to the original expression and two disappearance gates (16–17).

Audience questions are answered on the slide itself: UniversalToolchain versus Wist (1), feature composition (2–3), exact dialect selection (4), plan purpose and contents (5), representations and .NET execution (6–7), engineering regression and current result (8), current/proposed boundary (9), semantic query (10), derivation and unchanged consumer (11–12), contracts and provenance (13–14), responsible prior-art boundary (15), disappearing abstractions (16).

## Adversarial technical review

- **Compiler researcher:** no novelty, formal completeness or measured advantage is asserted. Slide 15 states an integration experiment against an interface/analysis-manager baseline.
- **Compiler engineer:** the plan and exact 3→1 AIR rewrite are implemented mechanisms. The proposed layer must justify itself through unchanged-consumer integration and correct invalidation; more framework is not an automatic benefit.
- **Language designer:** MLIR interfaces, LLVM analysis management, Silver/ableC and Soufflé provenance link to primary sources. The comparison describes boundaries without misleading capability checkmarks.
- **.NET engineer:** AIR execution and CIL compilation are separate routes. DynamicMethod, typed delegate, argument-slot lowering and the .NET JIT are visible. CIL is not mislabeled as machine code.
- **First-time attendee / speaker:** the pricing expression, actual module selection and trace recur. Every slide has a causal outline; notes are backup rather than the only source of meaning.
- **SIMD safety:** the example fixes lane-wise arithmetic, types, valid bounds and non-trapping evaluation. Computation purity does not erase output writes; dependency facts account for iteration interactions. Legality differs from profitability. Missing, invalidated or conflicting evidence cannot grant permission.

## Evidence boundaries

Executed source-baseline checks: 10 interpreter-binding parity tests, 7 dialect-profile contract tests, 5 focused NativeCilOptimizer tests, shipped pricing returning 95 in both routes, and a successful public-facade shadowing probe returning 2 in both routes. Full source/status details are in `REBUILD_EVIDENCE.md`.

The semantic proof layer and SIMD example remain proposals, not implemented functionality. No historical incorrect numeric result was recovered or invented. Bytecode/AIR fragments are explicitly unoptimized explanatory sketches; constant folding may change the production artifact. No performance numbers or advantage over prior art are claimed. A timed human rehearsal and projector check remain speaker-side checks, not completed browser evidence.

## Cleanup

Removed obsolete duplicate `langdev_presentation_dag_pseudocode.html`; Git history retains it. Replaced stale 24-slide/delegate documentation and CI contracts with checks for the actual production deck. Removed obsolete slide CSS/IDs/navigation references during the rebuild. Compiler source and architecture are unchanged. The rebuild was verified locally before the owner's follow-up publication request; publishing uses the existing GitHub Pages deployment from `main` at the repository root.

The first publication's GitHub-hosted browser exposed a portability defect: local Inter was not installed on the runner, so fallback-font metrics wrapped titles and crowded slides 6, 13 and 15. The deployed source and controls were correct, but the independent geometry check appropriately failed. The repair embeds Inter and renamed Liberation Mono subsets directly in the HTML, including their original OFL licenses. Every CSS text stack now prefers these bundled families. No geometry assertion was removed or relaxed; font loading is now an additional assertion. This also removes dependence on the speaker's installed fonts.
