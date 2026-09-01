# Demo runbook — planner/runtime boundary

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Target: **90–120 seconds**. No live coding. Audience-visible state changes: **3 maximum**.

## What the demo proves

`demo/Program.cs` has two source-backed phases.

1. **Negative planning case.** A synthetic consumer requires `demo.capability`; two providers are eligible. `LanguageCompiler.Compile(...)` must return `UTL2002`. Adding `PreferCapabilityProvider(...provider.a...)` resolves exactly that whole-language ambiguity.
2. **Resolved execution case.** A tiny synthetic language parses `SourceText` to `int`, has one selected backend that returns `value + 1`, and uses a route runtime. The program prints `LanguagePlan` data, calls `LanguageRuntime.Create(...)`, runs `"41"`, and requires output `42`.

This is intentionally **not** the Wist `MinimalArithmetic` path. A synthetic package isolates the planner/runtime architecture and keeps the conference demo deterministic.

The demo proves:

- real planner diagnostics;
- explicit provider policy;
- a real immutable `LanguagePlan`;
- a real route/runtime-provider summary;
- exact runtime materialization;
- real execution through the planned environment.

It does **not** prove:

- Wist language semantics;
- arbitrary extension semantic compatibility;
- optimizer correctness;
- sandboxing;
- performance or zero overhead.

## Preflight

Use the exact pinned UniversalToolchain checkout:

```bash
git -C /path/to/UniversalToolchain checkout 7005371d6c30175dff4b0e9f906a26218b0ee54d
dotnet build demo/UniversalToolchainDemo.csproj \
  -p:UniversalToolchainRoot=/path/to/UniversalToolchain
./demo/run-demo.sh /path/to/UniversalToolchain | tee demo-last-good.txt
```

Expected semantic anchors:

```text
[planning] UTL2002:
[planning] preferred provider: demo.provider.a
[plan] runtime: demo.runtime@1
[plan] route: demo
[runtime] input=41 output=42
```

`PlanHash` is intentionally not hard-coded.

## Conference command

After a successful prebuild:

```bash
DEMO_NO_BUILD=1 ./demo/run-demo.sh /path/to/UniversalToolchain
```

The script verifies the UniversalToolchain commit before execution and fails closed on source drift. Set `DEMO_ALLOW_SOURCE_DRIFT=1` only for deliberate local investigation, never for the conference evidence path.

After prebuild, the conference path is expected to require **no network access**. Keep the checkout, .NET SDK, build outputs and terminal locally available.

Recommended terminal setup: 16–18 pt monospace, ~100–110% zoom, dark/light choice tested on the projector, and enough width that diagnostic lines do not wrap.

## Live sequence

Show only these three changes:

1. `UTL2002` — ask “Two providers are valid. Who wins?”;
2. the one explicit provider preference + plan/runtime/route summary;
3. final `input=41 output=42`.

Do not scroll through project files or live-edit code.

## Reset

The demo is read-only with respect to both repositories; reset is simply rerun the command. No generated source state is required.

## Fallback ladder

1. **Cached stdout:** keep `demo-last-good.txt` from the same pinned checkout and last successful preflight.
2. **Screenshot:** use the `presentation-validation-evidence` CI artifact from the last green presentation commit.
3. **Recorded fallback:** if venue reliability warrants it, keep a short screen recording of the same exact command/output.

If the live demo fails, say:

> “The live environment failed; I’ll use the last CI-validated output. The claim is the planner/runtime boundary, not terminal theatre.”

Never invent a hash, route cost, successful output, or performance number.

## CI contract

Presentation CI runs this canonical script against exact UniversalToolchain `7005371d6c30175dff4b0e9f906a26218b0ee54d` and asserts both the negative and positive anchors. `scripts/check_deck.py` also cross-checks slide text, demo source, runbook and truth pin so the deck cannot silently drift back to a different executable story.
