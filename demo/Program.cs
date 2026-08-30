using UniversalToolchain.FeatureSdk;
using UniversalToolchain.Language.Abstractions;
using UniversalToolchain.LanguageAuthoring;
using UniversalToolchain.LanguageSdk;
using UniversalToolchain.Runtime;

Console.WriteLine("== planning ambiguity ==");
var capability = new LanguageCapabilityId("demo.capability");
var feature = new LanguageFeatureId("demo.ambiguity");
var providerA = new LanguageContributionId("demo.provider.a");
var providerB = new LanguageContributionId("demo.provider.b");
var consumer = new LanguageContributionId("demo.consumer");

var ambiguityPackage = new LanguagePackageDescriptor(
    new LanguagePackageId("Demo.Ambiguity"),
    new LanguageVersion("1"),
    ToolchainApi.Current,
    [new LanguageFeatureDescriptor(feature, contributions: [consumer])],
    contributions:
    [
        new LanguageContributionDescriptor(providerA, LanguageSlots.Tooling, providesCapabilities: [capability]),
        new LanguageContributionDescriptor(providerB, LanguageSlots.Tooling, providesCapabilities: [capability]),
        new LanguageContributionDescriptor(consumer, LanguageSlots.Tooling, requiresCapabilities: [capability])
    ]);
var ambiguityCompiler = new LanguageCompiler(new LanguagePackageRegistry().AddPackage(ambiguityPackage));
var ambiguous = ambiguityCompiler.Compile(
    LanguageDefinitionBuilder.Create("Demo.Ambiguity.Language", "1")
        .UseFeature(feature)
        .Build());
var ambiguityDiagnostic = ambiguous.Diagnostics.Single(d => d.Code == "UTL2002");
Console.WriteLine($"[planning] {ambiguityDiagnostic.Code}: {ambiguityDiagnostic.Message}");

var resolved = ambiguityCompiler.Compile(
        LanguageDefinitionBuilder.Create("Demo.Ambiguity.Language", "1")
            .UseFeature(feature)
            .PreferCapabilityProvider(capability, providerA)
            .Build())
    .GetRequiredPlan();
Console.WriteLine($"[planning] preferred provider: {providerA.Value}");
Console.WriteLine($"[planning] contributions: {string.Join(", ", resolved.Contributions.Select(x => x.Contribution.Id.Value))}");

Console.WriteLine();
Console.WriteLine("== planner/runtime boundary ==");
var syntax = new LanguageArtifactKind<int>("demo.syntax");
var backend = new BackendId("demo");
var package = LanguagePackageBuilder.Create("Demo.Runtime", "1")
    .AddFeature("demo.core", f => f
        .AddTransformer(
            "demo.parse",
            LanguageSlots.FrontendParser,
            StandardLanguageArtifactKinds.SourceText,
            syntax,
            static (source, _) => int.Parse(source),
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop,
            cost: 1)
        .AddBackend(
            backend,
            new LanguageContributionId("demo.backend"),
            syntax,
            static (value, _) => value + 1,
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop))
    .UseRouteRuntime("demo.runtime", "1")
    .Build();

var registry = new LanguagePackageRegistry().AddPackage(package);
var plan = new LanguageCompiler(registry)
    .Compile(LanguageDefinitionBuilder.Create("Demo.Language", "1")
        .UseFeature("demo.core")
        .EnableBackend(backend)
        .UseRuntimeProvider("demo.runtime", "1")
        .Build())
    .GetRequiredPlan();

Console.WriteLine($"[plan] hash: {plan.PlanHash}");
Console.WriteLine($"[plan] runtime: {plan.RuntimeProvider!.ProviderId.Value}@{plan.RuntimeProvider.Version.Value}");
foreach (var route in plan.Routes.Values.OrderBy(r => r.Backend.Value, StringComparer.Ordinal))
{
    Console.WriteLine($"[plan] route: {route.Backend.Value} | cost={route.TotalCost} | steps={route.Steps.Count}");
    foreach (var step in route.Steps)
        Console.WriteLine($"       {step.ContributionId.Value}: {step.Source.Value} -> {step.Target.Value}");
}

using var runtime = LanguageRuntime.Create(plan, new ILanguageRouteComponentSource[] { package });
var result = runtime.Run(new LanguageExecutionRequest("41", backend));
Console.WriteLine($"[runtime] input=41 output={result.Value}");
if (!Equals(result.Value, 42))
    throw new InvalidOperationException($"Expected 42, got {result.Value}.");
