# Research update: runtime render validation

## Finding

Runtime-mutated HTML decks cannot be validated safely by counting source fragments. The final slide set is produced by executing the deck scripts in order, including reorders, replacements, demotions to appendix, and speaker-script overlays.

## Strongest alternative considered

The brute-force checker is conceptually simple: test every runtime slide at every geometry and emit every screenshot variant. It is stronger as an exhaustive layout sweep, but it is too expensive for a CI loop when each state starts a fresh headless browser process.

## Chosen validation model

Use two layers:

1. **Complete runtime identity layer** — derive all main/appendix keys from the executed DOM, reject duplicates/overlap/missing speech, validate navigation and every slide in audience + presenter mode at canonical conference geometry.
2. **Risk-sampled geometry layer** — test additional viewport sizes for semantic milestone slides and the late architecture cluster, where previous visual review found the highest density risk.

## Remaining limitation

This is not a substitute for a human visual pass. It is a CI regression guard for runtime identity, canonical slide visibility, presenter-note ownership, navigation, and representative responsive layout.
