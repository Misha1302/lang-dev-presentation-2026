# Demo runbook — composition changes the concrete route

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

Target: **90–120 seconds**. No live coding. Audience-visible state changes: **3 maximum**.

## Main proof

The visible conference story is compiler-specific:

```text
base language: demo.core
    Source --demo.parse(1)--> Syntax --demo.lower.safe(6)--> AIR
    resolved route Cost = 7

enable one independently authored feature: demo.fast-path
    Source --demo.parse(1)--> Syntax --demo.lower.fast(1)--> AIR
    resolved route Cost = 2

same backend
same source input
Run("41") -> 42
```

The new feature contributes an alternative typed `Syntax -> AIR` edge. `LanguageCompiler`
automatically searches the conversion graph formed by **selected contributions** and chooses the
deterministic minimum declared planning cost. The route is stored in `LanguagePlan`.

`Cost` is a planner weight. It is **not** measured execution latency.

Both lowering functions in this deliberately synthetic fixture are identity transforms. That makes the
route change observable without making semantic behavior the point of the demo. The planner does not
prove that arbitrary alternative routes are semantically equivalent.

## Small secondary proof

`demo/Program.cs` still begins with the previous compact provider-ambiguity case:

```text
UTL2002
-> PreferCapabilityProvider(...provider.a...)
-> successful LanguagePlan
```

Keep this as a small supporting proof that whole-language policy resolves provider ambiguity. Do **not**
make it the central architectural example; the route-changing section is the live focus.

## What the demo proves

- independently selected features change the candidate transformation graph;
- route search happens inside the current whole-language planner;
- the selected route changes from `demo.lower.safe` to `demo.lower.fast`;
- the result is visible through `LanguagePlan.Routes`;
- exact runtime materialization can execute the resolved plan;
- real execution through the enhanced plan produces `41 -> 42`.

It does **not** prove:

- semantic equivalence of arbitrary routes;
- optimizer correctness in Wist;
- runtime speedup from the lower `Cost`;
- zero-overhead extensibility;
- sandboxing;
- production maturity of an extension ecosystem.

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
[route:base] cost=7 | demo.parse -> demo.lower.safe
[route:+fast-path] cost=2 | demo.parse -> demo.lower.fast
[route] Cost is declared planning weight, not measured runtime latency.
[runtime] input=41 output=42
```

`PlanHash` is intentionally not hard-coded.

## Conference command

After a successful prebuild:

```bash
DEMO_NO_BUILD=1 ./demo/run-demo.sh /path/to/UniversalToolchain
```

The script verifies the UniversalToolchain commit before execution and fails closed on source drift.
Set `DEMO_ALLOW_SOURCE_DRIFT=1` only for deliberate local investigation, never for conference evidence.

After prebuild, the conference path is expected to require **no network access**. Keep the exact checkout,
.NET SDK, build outputs and terminal locally available.

## Live sequence

Show only these three changes:

1. base plan: `demo.parse -> demo.lower.safe`, Cost `7`;
2. enable `demo.fast-path`: route becomes `demo.parse -> demo.lower.fast`, Cost `2`;
3. execute the enhanced plan: `input=41 output=42`.

Say explicitly:

> “The smaller Cost changed the planner's choice. I have not measured it as a faster runtime route.”

Do not scroll through implementation files or live-edit code. The UTL2002 section is fallback/Q&A evidence,
not a fourth live beat.

## Fallback ladder

1. **Cached stdout:** keep `demo-last-good.txt` from the same pinned checkout and last successful preflight.
2. **Screenshot:** use `presentation-validation-evidence` from the last green presentation CI run.
3. **Recorded fallback:** keep a short recording of the exact same command/output if venue reliability warrants it.

If the live environment fails, say:

> “The live environment failed; I’ll use the last CI-validated output. The claim is the resolved route change, not terminal theatre.”

Never invent a hash, route cost, successful output or performance number.

## CI contract

Presentation CI checks out exact UniversalToolchain
`7005371d6c30175dff4b0e9f906a26218b0ee54d`, runs the canonical script and asserts:

- `UTL2002` still exists as the small ambiguity proof;
- base route contains `demo.lower.safe` with Cost `7`;
- enabling `demo.fast-path` changes the route to `demo.lower.fast` with Cost `2`;
- runtime still produces `41 -> 42`.

`scripts/check_deck.py` cross-checks slide text, demo source, runbook and truth pin so the visible talk
cannot silently drift from the executable story.
