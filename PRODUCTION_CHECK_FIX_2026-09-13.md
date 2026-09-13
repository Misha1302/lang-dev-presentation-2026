# Production check fix — 2026-09-13

This change fixes the post-merge Pages validation guard after the final LangDev runtime deck rebuild.

## Root cause

`scripts/check_production.py` still expected the old static deck asset list:

- `deck-main.js`
- `deck-research-update.js`
- `deck-appendix.js`
- `deck-non-destructive-patches.js`

The actual production deck now loads the full runtime stack from `index.html`:

- `deck-main.js`
- `deck-research-update.js`
- `deck-prior-art-matrix.js`
- `deck-safe-index-case.js`
- `deck-appendix.js`
- `deck-non-destructive-patches.js`
- `deck-narrative-reframe.js`

The deck itself, timing audit and full render audit were already passing on CI for commit `6877be0f01111ada930934505af3d4fa978c617f`; only the production asset-order guard was stale.

## Fix

The production checker now derives local production assets from `index.html`, adds the dynamically loaded presenter CSS, waits for exact deployed hashes, and validates the deployed runtime DOM rather than reconstructing slide identity from stale static fragments.

## Validation expectation

The next main CI run should keep the existing passing checks and make the production Pages comparison pass after deployment catches up.
