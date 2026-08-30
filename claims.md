# Claim / evidence map

Truth snapshot: `36206b66548fec365be6e03381ba44d50c2cafe5`.

| Talk claim | Current-source evidence | Classification |
| --- | --- | --- |
| There is one public semantic planning entrypoint | `UniversalToolchain.LanguageSdk/LanguageCompiler.cs` (`Compile(LanguageDefinition)`) | implemented |
| Planning produces a concrete immutable composition result | `LanguagePlan.cs`: Features, Contributions, RuntimeProvider, Routes, PlanHash, Summary | implemented |
| Multiple capability providers fail before execution | `LanguageContributionResolutionPhase.cs`, diagnostic `UTL2002`, hint `PreferCapabilityProvider` | implemented |
| Artifact routes are planning output | `LanguageArtifactRoutePhase.cs` + `LanguagePlan.Routes` | implemented |
| Runtime consumes and validates the selected plan | `Runtime/LanguageRuntime.cs` | implemented |
| Runtime materializes exact planned components | `LanguageRouteRuntimeAssembler.cs` + `ExactRuntimeBindingTests.cs` | implemented / regression-tested |
| A full tiny source-backed language can run through the boundary | `ExactRuntimeBindingTests.RuntimeAssembler_MaterializesOnlyPlannedComponents` and `demo/Program.cs` | implemented; presentation CI executes exact snapshot |
| Generic IR/runtime machinery can always be optimized away | no general proof or benchmark in cited source | **not claimed** |
| Extensibility is universally zero-cost | no evidence | **not claimed** |
