using UniversalToolchain.FeatureSdk;
using UniversalToolchain.Language.Abstractions;
using UniversalToolchain.LanguageAuthoring;
using UniversalToolchain.LanguageSdk;
using UniversalToolchain.Runtime;

Console.WriteLine("== small provider ambiguity proof ==");
var capability = new LanguageCapabilityId("demo.capability");
var ambiguityFeature = new LanguageFeatureId("demo.ambiguity");
var providerA = new LanguageContributionId("demo.provider.a");
var providerB = new LanguageContributionId("demo.provider.b");
var consumer = new LanguageContributionId("demo.consumer");

var ambiguityPackage = new LanguagePackageDescriptor(
    new LanguagePackageId("Demo.Ambiguity"),
    new LanguageVersion("1"),
    ToolchainApi.Current,
    [new LanguageFeatureDescriptor(ambiguityFeature, contributions: [consumer])],
    contributions:
    [
        new LanguageContributionDescriptor(
            providerA,
            LanguageSlots.Tooling,
            providesCapabilities: [capability]),
        new LanguageContributionDescriptor(
            providerB,
            LanguageSlots.Tooling,
            providesCapabilities: [capability]),
        new LanguageContributionDescriptor(
            consumer,
            LanguageSlots.Tooling,
            requiresCapabilities: [capability])
    ]);

var ambiguityCompiler =
    new LanguageCompiler(new LanguagePackageRegistry().AddPackage(ambiguityPackage));
var ambiguous = ambiguityCompiler.Compile(
    LanguageDefinitionBuilder.Create("Demo.Ambiguity.Language", "1")
        .UseFeature(ambiguityFeature)
        .Build());
var ambiguityDiagnostic = ambiguous.Diagnostics.Single(d => d.Code == "UTL2002");
Console.WriteLine(
    $"[planning] {ambiguityDiagnostic.Code}: {ambiguityDiagnostic.Message}");

var resolved = ambiguityCompiler.Compile(
        LanguageDefinitionBuilder.Create("Demo.Ambiguity.Language", "1")
            .UseFeature(ambiguityFeature)
            .PreferCapabilityProvider(capability, providerA)
            .Build())
    .GetRequiredPlan();
Console.WriteLine($"[planning] preferred provider: {providerA.Value}");
Console.WriteLine(
    $"[planning] contributions: {string.Join(", ", resolved.Contributions.Select(
        x => x.Contribution.Id.Value))}");

Console.WriteLine();
Console.WriteLine("== route-changing language composition ==");

var syntax = new LanguageArtifactKind<int>("demo.syntax");
var air = new LanguageArtifactKind<int>("demo.air");
var backend = new BackendId("demo");

var package = LanguagePackageBuilder.Create("Demo.Route", "1")
    .AddFeature("demo.core", feature => feature
        .AddTransformer(
            "demo.parse",
            LanguageSlots.FrontendParser,
            StandardLanguageArtifactKinds.SourceText,
            syntax,
            static (source, _) => int.Parse(source),
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop,
            cost: 1)
        .AddTransformer(
            "demo.lower.safe",
            LanguageSlots.Lowering,
            syntax,
            air,
            static (value, _) => value,
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop,
            cost: 6)
        .AddBackend(
            backend,
            new LanguageContributionId("demo.backend"),
            air,
            static (value, _) => value + 1,
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop))
    .AddFeature("demo.fast-path", feature => feature
        .AddTransformer(
            "demo.lower.fast",
            LanguageSlots.Lowering,
            syntax,
            air,
            static (value, _) => value,
            LanguageRuntimeComponentTraits.DeterministicNoHostInterop,
            cost: 1))
    .UseRouteRuntime("demo.runtime", "1")
    .Build();

var registry = new LanguagePackageRegistry().AddPackage(package);
var compiler = new LanguageCompiler(registry);

var basePlan = compiler
    .Compile(LanguageDefinitionBuilder.Create("Demo.Route.Language", "1")
        .UseFeature("demo.core")
        .EnableBackend(backend)
        .UseRuntimeProvider("demo.runtime", "1")
        .Build())
    .GetRequiredPlan();

var extendedPlan = compiler
    .Compile(LanguageDefinitionBuilder.Create("Demo.Route.Language", "1")
        .UseFeature("demo.core")
        .UseFeature("demo.fast-path")
        .EnableBackend(backend)
        .UseRuntimeProvider("demo.runtime", "1")
        .Build())
    .GetRequiredPlan();

var baseRoute = basePlan.Routes[backend];
var extendedRoute = extendedPlan.Routes[backend];

Console.WriteLine(
    $"[route:base] cost={baseRoute.TotalCost} | {RouteSignature(baseRoute)}");
Console.WriteLine(
    $"[route:+fast-path] cost={extendedRoute.TotalCost} | " +
    RouteSignature(extendedRoute));
Console.WriteLine(
    "[route] Cost is declared planning weight, not measured runtime latency.");

RequireRoute(baseRoute, expectedLowering: "demo.lower.safe", expectedCost: 7);
RequireRoute(extendedRoute, expectedLowering: "demo.lower.fast", expectedCost: 2);

using var runtime = LanguageRuntime.Create(
    extendedPlan,
    new ILanguageRouteComponentSource[] { package });
var result = runtime.Run(new LanguageExecutionRequest("41", backend));
Console.WriteLine($"[runtime] input=41 output={result.Value}");

if (!Equals(result.Value, 42))
    throw new InvalidOperationException($"Expected 42, got {result.Value}.");

static string RouteSignature(LanguageArtifactRoute route) =>
    string.Join(" -> ", route.Steps.Select(step => step.ContributionId.Value));

static void RequireRoute(
    LanguageArtifactRoute route,
    string expectedLowering,
    int expectedCost)
{
    if (route.TotalCost != expectedCost)
    {
        throw new InvalidOperationException(
            $"Expected route cost {expectedCost}, got {route.TotalCost}.");
    }

    if (!route.Steps.Any(step => step.ContributionId.Value == expectedLowering))
    {
        throw new InvalidOperationException(
            $"Expected route to contain '{expectedLowering}'.");
    }
}
