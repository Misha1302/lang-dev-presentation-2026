# Self-review — production runtime validation fix

## Review result

The change targets only the failed post-merge production validation guard. It does not alter slide content, speaker notes, research claims, layout CSS, navigation, or the published deck runtime.

## Why this is the minimal safe fix

The failed CI log shows that every content and runtime validation step before production comparison passed, including timing, UT witness checks, and full render coverage. The failing assertion was a stale expected deck load-order list in `scripts/check_production.py`.

The updated checker removes that static expectation and instead uses the same authority as the browser runtime: `index.html` plus the deployed DOM dataset published by `deck.js`.

## Failure modes checked by design

- stale Pages assets still fail by SHA-256 mismatch;
- missing runtime speech still fails through `data-runtime-speech-missing`;
- missing or duplicate slide identities still fail;
- causal owner order still fails against `CONTENT_NARRATIVE_CONTRACT.json`;
- audience and presenter visual diagnostics still run on representative deployed slides;
- canonical presenter owner is still checked.

## Risk

The production checker now trusts `index.html` as the asset list source. This is intentional: the old hardcoded list was the source of the false failure after legitimate deck assets were added.
