# Demo runbook — one language, two backends, one meaning

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Target: **90–120 seconds**. No live coding. Audience-visible state changes: **3 maximum**.

## Main proof

The conference demo now matches the talk and accepted LangDev abstract more closely than the former synthetic route-cost fixture.

### 1. Inspect the shipped restricted pricing dialect

```bash
./demo/run-demo.sh /path/to/UniversalToolchain
```

The script first runs `wistc dialect-inspect` for:

```text
UniversalToolchain/Dialects/examples/wist/pricing-restricted/dialect.wistdialect
```

The point is not to read the whole manifest. Show that the language surface is composed deliberately and that both `interpreter` and `cil` are available.

### 2. Execute the same pricing program through both backends

The shipped program is:

```text
100.0 * 0.9 + 5.0
```

Expected semantic result:

```text
interpreter → 95
cil         → 95
```

This demonstrates a concrete language, a concrete composition, and two execution implementations that agree on the same program.

### 3. Run the targeted shadowing parity regression test

The script runs only:

```text
InterpreterBindingsParityTests.
ShadowingAndNestedScope_WithLocalNamesOverlappingExternals_ShouldBeDeterministicAndParityStable
```

The covered source patterns include local names overlapping external `price` / `fee` bindings and nested scopes. The test executes both the CIL and interpreter paths and requires semantic parity.

## What the demo proves

- the repository contains a real restricted pricing dialect;
- the same current source program executes through `interpreter` and `cil`;
- both backends produce the expected pricing result for the shipped example;
- current regression tests explicitly guard local/external binding shadowing across the two backends;
- the talk's correctness problem is compiler-shaped, not a generic plugin-selection toy.

It does **not** prove:

- semantic equivalence for every possible Wist program;
- that current UniversalToolchain already implements the proposed obligation-first whole-language planner;
- that a lower route `Cost` means faster execution;
- zero-overhead extensibility;
- hardened sandboxing;
- production maturity of an arbitrary extension ecosystem.

## Why the old route-cost demo is no longer central

The previous conference fixture showed:

```text
route Cost 7 → route Cost 2
```

when an independently authored feature added another conversion edge. That is valid evidence about current structural route selection, but it proves **preference**, not whole-language correctness. It therefore remains useful for appendix/Q&A and repository history, not as the main on-stage proof.

## Preflight

Use the exact pinned UniversalToolchain checkout and run one full build/restore-backed pass:

```bash
git -C /path/to/UniversalToolchain checkout 7005371d6c30175dff4b0e9f906a26218b0ee54d
./demo/run-demo.sh /path/to/UniversalToolchain | tee demo-last-good.txt
```

The script verifies the UniversalToolchain commit before execution and fails closed on source drift. Set `DEMO_ALLOW_SOURCE_DRIFT=1` only for deliberate local investigation, never for conference evidence.

After a successful preflight, keep the checkout and .NET build outputs locally available.

## Conference command — no build / no restore

For the actual stage run, use the already-built outputs:

```bash
DEMO_NO_BUILD=1 ./demo/run-demo.sh /path/to/UniversalToolchain
```

In this mode every `dotnet run` / targeted `dotnet test` invocation uses `--no-build --no-restore`. That keeps the live proof independent of package feeds and network availability after the preflight has succeeded.

## Live sequence

Show only these three beats:

1. **Language:** the restricted pricing dialect and its selected surface.
2. **Execution:** `100.0 * 0.9 + 5.0` produces `95` through interpreter and CIL.
3. **Correctness boundary:** the targeted local/external shadowing parity test passes.

Say explicitly:

> “The interesting invariant is not that both backends are reachable. It is that both still implement the same language semantics.”

Then transition to the planner limitation:

> “Current UT can freeze a structural route, but its route layer does not generally encode every semantic obligation that makes that route admissible.”

## Fallback ladder

1. **Cached stdout:** keep `demo-last-good.txt` from the exact pinned checkout.
2. **CI artifact:** keep `demo-source-output.txt` from the last green presentation run.
3. **Screenshot / recording:** keep the exact same three-beat proof captured from the pinned revision.

If the live environment fails, say:

> “The live environment failed; I’ll use the last CI-validated output. The claim is cross-backend language parity, not terminal theatre.”

Never invent a successful test, output, benchmark number, route cost, or performance result.

## Performance boundary

The accepted abstract mentions selected hot-execution measurements. The current repository has a dedicated BenchmarkDotNet suite, but this presentation does not put numerical performance results on stage without an exact raw benchmark artifact bound to the same revision/environment.

The architecture claim does not require a speedup claim.