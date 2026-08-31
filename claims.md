# Claim / evidence map

Truth snapshot: `7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Central claims

> Extensions describe possibilities. Planning resolves global composition choices into one concrete `LanguagePlan`. Runtime executes that resolved plan instead of reopening those decisions.

> Extensibility does not inherently require global composition decisions to remain dynamic during repeated execution.

> The runtime should not repeatedly pay for decisions that were already made.

These are architecture/staging claims. They are not universal performance claims.

| Talk claim | Current-source evidence | Classification |
| --- | --- | --- |
| There is one public semantic planning entrypoint | `UniversalToolchain.LanguageSdk/LanguageCompiler.cs` (`Compile(LanguageDefinition)`) | implemented |
| Planning produces concrete resolved composition data | `LanguagePlan.cs`: resolved Features, Contributions, RuntimeProvider, Routes, PlanHash, Summary | implemented |
| Multiple capability providers fail before execution | `LanguageContributionResolutionPhase.cs`, diagnostic `UTL2002`, hint `PreferCapabilityProvider` | implemented |
| Artifact routes are planning output | `LanguageArtifactRoutePhase.cs` + `LanguagePlan.Routes` | implemented |
| Route `Cost` is a planning metric, not measured runtime latency | `LanguageArtifactRoutePhase.FindBestRoute(...)` | implemented boundary; not a benchmark claim |
| Runtime consumes and validates the selected plan | `Runtime/LanguageRuntime.cs` | implemented |
| Repeated `LanguageRuntime.Run(...)` does not invoke the global semantic planner | `LanguageRuntime.Run(...)` delegates to the already-created session after plan-bound validation; no `LanguageCompiler`/route search/provider resolution | implemented architectural boundary |
| Runtime materializes exact planned components | `LanguageRouteRuntimeAssembler.cs` + `ExactRuntimeBindingTests.cs` | implemented / regression-tested |
| A full tiny source-backed language can run through the boundary | `ExactRuntimeBindingTests.RuntimeAssembler_MaterializesOnlyPlannedComponents` and `demo/Program.cs` | implemented; presentation CI executes exact snapshot |
| Prepared hot invocation, formula compilation and convenience evaluation are distinct workloads | `docs/reference/performance-model.md`, `docs/reference/benchmark-methodology.md`, benchmark classes | documented / benchmark harness exists |
| Planning/engine setup has a dedicated architecture-boundary benchmark surface | `MigrationArchitectureBoundaryBenchmarks.LanguagePlan_Compile` and `WistEngine_CreateAndDispose` | benchmark harness exists |
| Current exact-revision talk-ready planning/runtime/first/steady-state numbers | no raw exact-environment result set committed to this presentation | **NEEDS MEASUREMENT** |
| Planning guarantees devirtualization or removal of interfaces/dispatch | no such guarantee in current source | **not claimed** |
| Extensibility is free or universally zero-overhead | no evidence and not an architectural consequence | **not claimed** |
| Wist/UniversalToolchain matches or beats handwritten C# in general | benchmark methodology explicitly forbids this inference | **not claimed** |
| The selected route is a globally minimum-cost language configuration | route search minimizes declared transformation cost only within its expressed routing problem | **not claimed** |

## Cost-model boundary

Conceptually, repeated dynamic composition can be written as `N × (Ccomposition + Cexecution)`, while staged composition is `Ccomposition + N × Cexecution`. The `Ccomposition / N` term is an amortization model only. It does **not** prove that the whole UniversalToolchain workload is faster than an alternative.
