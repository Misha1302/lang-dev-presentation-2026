# LangDev 2026 — final QA, 2026-10-09

Canonical deck: `index.html`, 18 slides, 1290 seconds (**21:30**). Baseline: clean `main` at `e7256fd`. Current change/technical-integrity/outline report: IMPROVEMENT_REPORT.md. Historical QA remains in Git history and REBUILD_EVIDENCE.md; this report describes the current stable candidate.

Final executed command:

```bash
python scripts/validate_deck.py --output qa/verified-2026-10-09
```

## Browser and visual results

Chromium, Playwright 1.57.0. The final run asserts that HTML, runbook and validator hashes stay unchanged during capture; those hashes also match the final files after the run. Earlier candidate captures informed repairs but are not the final evidence.

| Check | Actual result |
|---|---|
| Slides / timing / research outlook | 18 / 1290 s / 415 s |
| Every fully shown slide at 1920×1080 | 18 captured; inspected; zero geometry issues |
| Every fully shown slide at 1536×864 | 18 captured; inspected; zero geometry issues |
| Every fully shown slide at 1366×768 | 18 captured; inspected; zero geometry issues |
| Additional design viewport 1600×900 | 18 captured; zero geometry issues |
| All logical reveal states | 55 states × 4 sizes = 220 captures; zero geometry issues |
| JavaScript errors | 0 |
| Previous/next and keyboard | Arrows, PageUp/Down, Space/Shift+Space, J/K, Home/End passed |
| Buttons, dots, hashes | Passed; all 18 slides reachable |
| Counter / progress | Explicitly checked on every slide at all four design/projector sizes |
| R / A reveals | Passed; contiguous steps; final content visible |
| Presenter notes / help | Actual visible SAY/NEXT/END cues and P dismissal checked on every slide; H dismissal passed |
| Wheel / touch | Passed |
| Embedded fonts / QR images | Seven font faces and all four images load offline |
| Local file / offline | All 18 slides opened offline |
| Non-16:9 and smaller windows | All slides checked at 1280×720, 1024×768, 1280×900 and 390×844; 72 captures; zero geometry issues |
| Print | PDF generated; `pdfinfo` confirms 18 pages |
| Notes consistency | All runbook SAY cues match actual P cues; detailed ANCHOR/FLOW/TRANSITION notes retained |
| Diff whitespace | `git diff --check` passed |

Visual inspection covered all **54 requested full-slide combinations**, including fully revealed states. Parent reviewed all five 1920 contact sheets and individual 1366 proof/extension slides. Independent designer/audience review covered all ten 1536/1366 contact sheets and all **21 research reveal states at 1920** (slides 9–15). Parent also inspected the proof/extension reveal montage. No clipping, collisions, unreadable node labels, detached revealed arrows or premature proof-success state was observed. Automated geometry covers every intermediate reveal at every size; additional manual inspection of all intermediate states at the smaller sizes was not performed.

These are rendered technical/designer reviews, not measured human comprehension or projector-room usability tests. No delivery duration was measured. Rehearse the 8→9 reset, 10–12 derivation/bridge sequence and 15→16 return to implemented code.

Source hashes:

| File | SHA-256 |
|---|---|
| index.html | `faf1a10bc8443e403079b5b0f473b3716f282354e357a9f3b1542718bec760a9` |
| speaker-runbook.html | `340dc709499472739739a599240cfa3a72978d3e91823d69c4de4aa8f8f08a70` |
| scripts/validate_deck.py | `500350a4692ed7fee7c0dcfaa9dcf2d2ce6a4a49e936c1b6fc0a97cea24c1539` |

Artifacts (ignored by Git): `qa/verified-2026-10-09/validation.json`, screenshots, contact sheets, reveal captures and `LangDev-2026.pdf`.

## Fresh compiler validation

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

## Links, integrity and remaining limits

All **26 unique external hyperlinks** returned HTTP 200 in the network check, including pinned compiler/research links, primary prior-art pages and contact destinations. Result: `qa/link-check-2026-10-09.json`. All **27 data-source references** resolve to existing files in the pinned checkout. Fonts and QR assets are embedded; no external runtime asset is required.

Independent compiler/PL review repaired overlapping dependency premises, hidden lane-equivalence assumptions, rule ownership and the parity/proposal causal conflation. Audience/designer review repaired producer naming and the unchanged top-level query. Final reviewed candidate has no unresolved technical contradiction under its explicit bounds.

Remaining limits are intentional: SIMD and general relation inference/provenance are proposed and illustrative; provider authority, bridge soundness and complete invalidation need research implementation/evaluation. Existing compiler facts/lifecycle contracts are implemented. No performance benchmark, production SIMD engine, universal zero-cost result or human delivery/comprehension claim is asserted. This report records local validation before publication. Release status must be checked against the subsequent GitHub CI/deployment runs and live artifact.
