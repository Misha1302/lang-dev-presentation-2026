# Demo runbook — planner/runtime boundary

Truth snapshot: `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`. Target: 90–120 seconds; no live coding.

## What the demo proves

The first half creates a real `LanguagePackageDescriptor` whose consumer requires a capability with two eligible providers. `LanguageCompiler.Compile(...)` must return diagnostic `UTL2002`. The minimal correction is `LanguageDefinitionBuilder.PreferCapabilityProvider(...)`; the corrected plan then exposes the selected contributions.

The second half uses `LanguagePackageBuilder` to author a tiny executable language: `SourceText` is parsed to an `int`, the selected backend returns `value + 1`, and `UseRouteRuntime` supplies the runtime provider. The program prints actual `LanguagePlan` fields, calls `LanguageRuntime.Create(plan, componentSources)`, and runs `"41"`, expecting `42`.

This demo proves the composition boundary only: possibilities are resolved into a concrete plan and the runtime materializes/executes that exact selection. It is not a performance benchmark and does not prove semantic compatibility for arbitrary extensions.

## Run against a current checkout

```bash
./demo/run-demo.sh /path/to/UniversalToolchain
```

`run-demo.sh` refuses a missing checkout and prints the source commit when Git metadata is available. The project uses direct `ProjectReference`s into the supplied checkout; it does not substitute a stub planner or an older NuGet package.

## Conference path

Run once before the talk and keep the stdout. During the talk, show only: `UTL2002`; the one-line provider policy; `PlanHash` + runtime/route summary; and final `input=41 output=42`.

If source checkout/build fails, say that the live environment is blocked and use the CI artifact from the last validated presentation commit. Do not invent a hash, route cost, successful runtime output, or performance number.
