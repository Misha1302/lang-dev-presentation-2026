# LangDev 2026 live demo

Target: **90–120 seconds**. Run these from the root of a current `UniversalToolchain` checkout before the talk and keep the terminal ready.

The commands below are copied from the shipped example READMEs in `UniversalToolchain/Dialects/examples/wist` and were rechecked against commit `fde7d0b5b88347ca07687cb6b0870f6b59c30f0b` on 2026-08-22.

## 1. Show the resolved restricted composition

```bash
dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  dialect-inspect \
  --file UniversalToolchain/Dialects/examples/wist/composition-restricted/dialect.wistdialect
```

Then run the allowed program:

```bash
dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  run \
  --dialect-file UniversalToolchain/Dialects/examples/wist/composition-restricted/dialect.wistdialect \
  --file UniversalToolchain/Dialects/examples/wist/composition-restricted/program.wist \
  --backend interpreter
```

Expected result: `true`.

## 2. Show that absence is observable

```bash
dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  run \
  --dialect-file UniversalToolchain/Dialects/examples/wist/composition-restricted/dialect.wistdialect \
  --file UniversalToolchain/Dialects/examples/wist/composition-restricted/forbidden-program.wist \
  --backend interpreter
```

Expected: non-zero exit because variable declarations are excluded.

Optional second rejection:

```bash
dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  run \
  --dialect-file UniversalToolchain/Dialects/examples/wist/composition-restricted/dialect.wistdialect \
  --file UniversalToolchain/Dialects/examples/wist/composition-restricted/forbidden-interop.wist \
  --backend interpreter
```

Expected: non-zero exit because C# interop is excluded.

## 3. Show backend parity on one shipped program

```bash
dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  run \
  --dialect-file UniversalToolchain/Dialects/examples/wist/full-default/dialect.wistdialect \
  --file UniversalToolchain/Dialects/examples/wist/full-default/program.wist \
  --backend interpreter

dotnet run --project UniversalToolchain/Wistc/Wistc.csproj -- \
  run \
  --dialect-file UniversalToolchain/Dialects/examples/wist/full-default/dialect.wistdialect \
  --file UniversalToolchain/Dialects/examples/wist/full-default/program.wist \
  --backend cil
```

Expected result from both: `15`.

## Delivery

Narrate only three ideas: **the dialect selects a composition → excluded features really disappear from the accepted language surface → two backend routes preserve the same observable result**. Do not use the demo to claim process isolation, formal equivalence, or universal performance.
