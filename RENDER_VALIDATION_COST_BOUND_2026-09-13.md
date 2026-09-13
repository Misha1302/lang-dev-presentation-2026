# Runtime render validation cost bound

Commit branch: `fix/runtime-render-check-budget-2026-09-13`.

## Problem

The previous runtime-aware render checker correctly stopped trusting source-fragment slide counts, but it launched a fresh browser process for every slide across every geometry and screenshot variant. On the current runtime deck this made the GitHub Actions render step too slow for practical CI feedback.

## Fix

The checker still discovers the final executed runtime manifest from the browser DOM and still validates every runtime main and appendix slide in both audience and presenter modes at the canonical conference geometry (`1366x768`). It also captures one audience and one presenter screenshot for every runtime slide.

Additional geometries are now sampled by semantic risk rather than brute force: first/last slides, appendix edges, milestone owners from `CONTENT_NARRATIVE_CONTRACT.json`, and the late dense architecture cluster (`m33..m50`, `pa2`, `pa4`, `pa5`, `pa7`, `pa8`).

## Guardrail preserved

This preserves the important regression guard: coverage is driven by final runtime DOM keys, not by regex counts over source JavaScript fragments. Nonexistent `#53...` hashes can no longer fake coverage by clamping to the last slide, and runtime-demoted appendix slides remain visible to the checker.
