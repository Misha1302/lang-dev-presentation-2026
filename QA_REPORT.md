# LangDev 2026 — range-check follow-up QA, 2026-10-09

Current artifact: `index.html`, **19 slides / 1305 seconds (21:45)**. Follow-up baseline: clean `main` at `3c43420`. The requested prior-art row and its speaker references were removed. Proposed global semantic optimization is demonstrated on slide 15 through an existing guard, a path-scoped SSA range invariant and two dominated in-bounds uses.

Executed final command:

```bash
python scripts/validate_deck.py --output qa/range-final
```

| Check | Observed result |
|---|---|
| Slides / total / research | 19 / 1305 s / 480 s |
| Full slides at 1920×1080 | 19 captured and visually reviewed; no geometry errors |
| Full slides at 1536×864 | 19 captured and visually reviewed; no geometry errors |
| Full slides at 1366×768 | 19 captured and visually reviewed; no geometry errors |
| Full slides at 1600×900 | 19 captured; no geometry errors |
| All intermediate/final reveals | 58 logical states × 4 sizes = 232 captures; no geometry errors |
| JavaScript errors | 0 |
| Navigation / counter / progress | All 19 reachable; keyboard, buttons, dots, hashes, wheel and touch passed; every counter/progress value checked |
| P / H / R / A | Presenter/help visibility/dismissal and reveal navigation passed; complete content reachable |
| Local file / offline | All 19 opened; seven embedded fonts and four QR images loaded |
| Smaller/non-16:9 windows | All slides checked at 1280×720, 1024×768, 1280×900, 390×844; 76 captures; no geometry errors |
| Runbook | All 19 actual P cues synchronized; timing and transitions updated |
| Print | PDF generated; 19 pages confirmed |
| Links | 26 unique external links returned HTTP 200; all 29 pinned source references exist locally |
| Diff | `git diff --check` passed |

The initial range candidate failed the caption-to-claim spacing check on slide 15. Reduced body spacing repaired it without smaller fonts or weaker validation. The final stable run passed all existing checks. The validator now uses exact 19-slide/1305-second/480-second contracts and checks the contact slide at its new number 19.

Parent inspected all five final 1920 contact sheets and the new range slide at 1366. Independent technical review verified both code/notes and the 1366 range rendering. Additional audience/designer review covered the final smaller-size sheets and the new reveals. No clipping, collisions, disconnected revealed arrows or unreadable important labels were observed. Automated coverage includes every intermediate state at all sizes; manual inspection does not claim every intermediate state at every size.

Range correctness boundaries: successful normal guard continuation dominates each use; half-open range; same immutable SSA identities and ordinary fixed-length non-null arrays. Keep the existing guard at its original position and preserve exception behavior. A caught-failure path cannot inherit success evidence; a new value or unguarded incoming path requires its own evidence. This is a path-scoped invariant, not a loop-induction proof. General range analysis/elimination is proposed; implemented SSA SCCP and dominance verification are the foundation. No new compiler implementation or speedup claim is made.

Source hashes of the stable final run:

| File | SHA-256 |
|---|---|
| index.html | `e1476ccb1e6453dae5e999ff686a1c79d9b0e9818ceee03a789754c9e09ac517` |
| speaker-runbook.html | `caca735e5ce3443644ad70dbdac192d9496785358e55a40c926130b326a3beae` |
| scripts/validate_deck.py | `66c6b240a59c3302aa3098ee2d8fa1349285863d1a98feb3bc33684d3f4c9c7b` |

Artifacts: `qa/range-final/validation.json`, all screenshots/contact sheets/reveals and `LangDev-2026.pdf`; link results: `qa/link-check-2026-10-09.json`. Artifacts are ignored by Git. No delivery-time or human-comprehension measurement was made. Rehearse the new 14→15→16 sequence and 16→17 return to implemented execution.

## Previous pinned-source compiler validation

The following 28-test/probe evidence was executed during the preceding narrative revision against the same unchanged pinned compiler source. It was not rerun for this presentation-only follow-up.


Source: clean pinned `../Wist2` at `1d46f17c8dc28f434fa58bdf92f9f8278fa5aaee`; SDK 10.0.111. Existing binary timestamps had uncertain provenance, so these commands **built the projects**, reusing available restored dependencies. No compiler source was edited. Commands ran from `../Wist2/UniversalToolchain`:

```bash
dotnet test UniversalToolchain.LanguageSdk.Tests/UniversalToolchain.LanguageSdk.Tests.csproj --no-restore --filter 'FullyQualifiedName~WistCanonicalArtifactGraphTests|FullyQualifiedName~PlanHash_IsIndependentOfFeatureAndBackendInsertionOrder' --logger 'console;verbosity=minimal' --verbosity quiet
dotnet test Tests/Tests.csproj --no-restore --filter 'FullyQualifiedName~InterpreterBindingsParityTests' --logger 'console;verbosity=minimal' --verbosity quiet
dotnet test UniversalToolchain.Dialects.Tests/UniversalToolchain.Dialects.Tests.csproj --no-restore --filter 'FullyQualifiedName~WistDialectProfileContractTests' --logger 'console;verbosity=minimal' --verbosity quiet
dotnet test UniversalToolchain.Modules.Tests/UniversalToolchain.Modules.Tests.csproj --no-restore --filter 'FullyQualifiedName~TypedIntrinsicEmitterOptimizerTests.NativeCilOptimizer_' --logger 'console;verbosity=minimal' --verbosity quiet
```

| Suite | Passed | Failed / skipped |
|---|---:|---:|
| Canonical artifact route + hash canonicalization | 6 | 0 / 0 |
| Interpreter bindings parity | 10 | 0 / 0 |
| Shipped dialect profile contracts | 7 | 0 / 0 |
| Native CIL typed-intrinsic optimizer | 5 | 0 / 0 |
| **Total** | **28** | **0 / 0** |

The independent existing probe `/tmp/langdev-evidence-TjuzUP/Probe.csproj` was inspected, rebuilt and rerun with:

```bash
dotnet run --project /tmp/langdev-evidence-TjuzUP/Probe.csproj --no-restore --verbosity quiet
```

It uses full-default-native, `let price = fee` / `price + fee`, and host `price=10.0`, `fee=1.0`. Actual output: **interpreter: shadowing = 2; cil: shadowing = 2**. This independently supports the numeric slide result; the parity suite alone also allows matching deterministic failures.

The pinned compiler checkout remained Git-clean after tests and probe. The broader compiler suite was not run because focused contracts cover the claims affected by this presentation edit.


## Publication

This report describes local validation before publication. Release status must be checked against the subsequent PR/main CI, GitHub Pages deployment and live HTML/runbook hashes.
