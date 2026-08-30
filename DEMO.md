# Demo script

Goal: prove the planning claim, not merely that a program runs.

## Happy path

1. Show local declarations from two or three packages.
2. Run the planner.
3. Inspect the resulting `LanguagePlan`:
   - selected provider: `X -> ProviderA`
   - route: `SourceText -> AST -> AIR -> SSA -> Backend`
   - pass order: `Parse -> Lower -> Optimize -> Cleanup`
   - exact backend executor / runtime package
4. Execute the valid configuration.

Expected fallback output:

```text
$ dotnet run --project demo/PlanInspection
✓ loaded language packages
✓ built LanguagePlan
  provider: X -> ProviderA
  route: SourceText -> AST -> AIR -> SSA -> Backend
  order: Parse -> Lower -> Optimize -> Cleanup
✓ executed selected backend route
```

## Controlled failure

Change only one thing: add a second provider for capability `X`, or remove the AIR-to-SSA conversion.

Expected fallback output:

```text
$ dotnet run --project demo/AmbiguousProvider
✗ planning failed: capability X has multiple matching providers
```

The audience should see that the failure belongs to planning time, not to a later accidental runtime crash.

## Talk boundary

Do not live-code. Use prepared commands and keep screenshot/output fallback available.
