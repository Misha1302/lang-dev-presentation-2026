#!/usr/bin/env bash
set -euo pipefail

EXPECTED_UT_SHA="7005371d6c30175dff4b0e9f906a26218b0ee54d"
ROOT="${1:-${UNIVERSAL_TOOLCHAIN_ROOT:-}}"

if [[ -z "$ROOT" || ! -d "$ROOT/UniversalToolchain/Wistc" ]]; then
  echo "ERROR: pass the UniversalToolchain checkout root as argv[1] or UNIVERSAL_TOOLCHAIN_ROOT." >&2
  exit 2
fi

if git -C "$ROOT" rev-parse HEAD >/dev/null 2>&1; then
  ACTUAL="$(git -C "$ROOT" rev-parse HEAD)"
  echo "UniversalToolchain source: $ACTUAL"
  if [[ "$ACTUAL" != "$EXPECTED_UT_SHA" ]]; then
    echo "ERROR: talk truth snapshot is $EXPECTED_UT_SHA, got $ACTUAL." >&2
    if [[ "${DEMO_ALLOW_SOURCE_DRIFT:-0}" != "1" ]]; then
      exit 3
    fi
    echo "WARNING: DEMO_ALLOW_SOURCE_DRIFT=1; result is not conference evidence." >&2
  fi
else
  echo "WARNING: supplied checkout has no readable Git HEAD; source identity cannot be verified." >&2
  if [[ "${DEMO_ALLOW_SOURCE_DRIFT:-0}" != "1" ]]; then
    exit 3
  fi
fi

# UniversalToolchain/NuGet.config declares a repository-local packages feed.
# The upstream CI provisions the directory even when the feed is empty.
mkdir -p "$ROOT/UniversalToolchain/packages"

WISTC="$ROOT/UniversalToolchain/Wistc/Wistc.csproj"
DIALECT="$ROOT/UniversalToolchain/Dialects/examples/wist/pricing-restricted/dialect.wistdialect"
PROGRAM="$ROOT/UniversalToolchain/Dialects/examples/wist/pricing-restricted/program.wist"
TESTS="$ROOT/UniversalToolchain/Tests/Tests.csproj"
TEST_FILTER='FullyQualifiedName~Tests.Backends.InterpreterBindingsParityTests.ShadowingAndNestedScope_WithLocalNamesOverlappingExternals_ShouldBeDeterministicAndParityStable'

printf '%s\n' '[language] pricing-restricted dialect'
dotnet run --project "$WISTC" -- dialect-inspect --file "$DIALECT"

run_backend() {
  local backend="$1"
  local output
  output="$(dotnet run --project "$WISTC" -- run --dialect-file "$DIALECT" --file "$PROGRAM" --backend "$backend")"
  printf '%s\n' "$output"
  if ! grep -Eq '(^|[^0-9])95([.]0+)?([^0-9]|$)' <<<"$output"; then
    echo "ERROR: backend '$backend' did not expose expected pricing result 95." >&2
    exit 4
  fi
  printf '[pricing:%s] result=95\n' "$backend"
}

run_backend interpreter
run_backend cil

printf '%s\n' '[parity] external bindings + local shadowing'
dotnet test "$TESTS" --filter "$TEST_FILTER" --verbosity minimal
printf '%s\n' '[parity] shadowing regression PASS'
