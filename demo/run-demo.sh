#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-${UNIVERSAL_TOOLCHAIN_ROOT:-}}"
if [[ -z "$ROOT" || ! -d "$ROOT/UniversalToolchain/UniversalToolchain.LanguageSdk" ]]; then
  echo "ERROR: pass the UniversalToolchain checkout root as argv[1] or UNIVERSAL_TOOLCHAIN_ROOT." >&2
  exit 2
fi
if git -C "$ROOT" rev-parse HEAD >/dev/null 2>&1; then
  ACTUAL=$(git -C "$ROOT" rev-parse HEAD)
  echo "UniversalToolchain source: $ACTUAL"
  if [[ "$ACTUAL" != "36206b66548fec365be6e03381ba44d50c2cafe5" ]]; then
    echo "WARNING: talk truth snapshot is 36206b66548fec365be6e03381ba44d50c2cafe5" >&2
  fi
fi
dotnet run --project "$(dirname "$0")/UniversalToolchainDemo.csproj" -p:UniversalToolchainRoot="$ROOT"
