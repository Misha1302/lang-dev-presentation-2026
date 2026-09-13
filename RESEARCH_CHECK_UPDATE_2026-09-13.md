# Research check update — production validation

The substantive research/narrative change is already in the merged deck commit. This follow-up does not introduce a new research claim.

## Confirmed from prior CI on `6877be0f01111ada930934505af3d4fa978c617f`

- runtime main deck: 52 slides;
- runtime appendix deck: 16 slides;
- spoken timing: 2873 words, about 22:06 at 130 wpm;
- render validation: 272 screenshots and 476 audience/presenter geometry states;
- UniversalToolchain witness: `40117eb68c630f7129c120aaaadc69be8f4ecbfb`;
- pricing restricted interpreter/CIL parity: result 95 on both backends;
- typed intrinsic witness: 14 focused tests passed;
- route-order feasibility witness: 1 focused test passed.

## Production blocker

The only failing CI step was not a research/content failure. It was a stale production checker assumption about the deck asset load order.

## Updated evidence boundary

Production validation now checks the deployed runtime DOM and exact deployed asset hashes instead of static pre-mutation fragment reconstruction. This aligns the production guard with the final runtime deck architecture.
