# Runtime / research self-review — 2026-09-13

## Result

The substantive deck revision is already on `main` at `6877be0`: the research claim is narrowed to cross-representation evidence, MLIR/LLVM/MPS are treated as strong prior art, and the late architecture section is simplified.

## Validation evidence

The `main` CI run validated the semantic contract, JavaScript syntax, 52 runtime main slides, 16 runtime appendix slides, 2873 spoken words (22:06 at 130 wpm), UniversalToolchain witnesses, and the full runtime render matrix: 272 screenshots over 476 audience/presenter geometry states.

The only failure was not a slide/render defect. `scripts/check_production.py` still hard-coded the older pre-runtime-mutator asset stack, so it rejected the current `index.html` before checking the deployed deck.

## Fix in this branch

Production validation now treats the executed final DOM as source of truth, matching the render/timing validators:

- production assets come from the actual stylesheet/script load list plus dynamically injected `presenter.css`;
- a local browser executes the complete deck and provides final main/appendix identities and order;
- semantic owners and causal order are validated on that runtime DOM;
- deployed Pages assets must match exact local hashes;
- deployed final DOM identity/order must equal the locally executed final DOM;
- representative audience and presenter states are then checked and captured.

This removes the same class of false ownership drift that previously affected render/timing checks: no validator should reconstruct the final presentation from stale source-fragment assumptions once runtime mutations own the final deck.

## Research boundary retained

The deck still does **not** claim that shared semantic evidence is already proven superior. The falsifiable target remains: compare a shared evidence lifecycle against MLIR/LLVM-style analyses plus explicit adapters across heterogeneous representations, and delete the extra layer if adapters win on cost, precision, safety, compile time, memory, or schema burden.
