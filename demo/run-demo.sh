#!/usr/bin/env bash
set -euo pipefail

EXPECTED_UT_SHA="7005371d6c30175dff4b0e9f906a26218b0ee54d"
ROOT="${1:-${UNIVERSAL_TOOLCHAIN_ROOT:-}}"
PROJECT="$(cd "$(dirname "$0")" && pwd)/UniversalToolchainDemo.csproj"

if [[ -z "$ROOT" || ! -d "$ROOT/UniversalToolchain/UniversalToolchain.LanguageSdk" ]]; then
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

ARGS=(run --project "$PROJECT" -p:UniversalToolchainRoot="$ROOT")
if [[ "${DEMO_NO_BUILD:-0}" == "1" ]]; then
  ARGS=(run --no-build --no-restore --project "$PROJECT" -p:UniversalToolchainRoot="$ROOT")
fi

dotnet "${ARGS[@]}"
