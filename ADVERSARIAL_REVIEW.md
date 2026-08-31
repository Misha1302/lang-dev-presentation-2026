# Independent adversarial review

Truth snapshot reviewed against `Misha1302/UniversalToolchain@7005371d6c30175dff4b0e9f906a26218b0ee54d`.

## Verdict

The revised narrative is defensible if the performance statement remains a staging claim:

> Extensions describe possibilities. Planning resolves global composition choices into one concrete `LanguagePlan`. Runtime executes that resolved plan instead of reopening those decisions.

The implementation supports that boundary. It does not support a universal zero-overhead or speedup claim.

## Hostile review

| Hostile question | Result | Evidence / correction |
| --- | --- | --- |
| Does the title imply zero-cost extensibility? | PASS | New title says extensible → concrete; slide 10 explicitly says interfaces/validation/dispatch may remain. |
| Does this imply all dispatch disappears? | PASS | Explicitly rejected on slides 9–10 and in speaker notes. |
| Does planning imply JIT/AOT devirtualization? | PASS | Representation/code specialization is labeled a separate optional optimization problem. |
| Does planning always pay off? | PASS | Handwritten pipeline remains the strongest baseline; slide 12 gives the decision criterion. |
| Does route `Cost` imply a globally minimum-cost language? | PASS | Route cost is treated as a protocol routing metric, not execution performance or global configuration optimality. |
| Does this imply Wist equals handwritten C# performance? | PASS | No speedup claim; appendix requires comparable-boundary measurements. |
| Are setup and steady-state costs mixed? | PASS | Slide 14 separates planning, runtime creation, first execution and steady state. |
| Is amortization presented as a benchmark? | PASS | Appendix labels `Ccomposition / N` a conceptual cost model only. |
| Is the hot-path claim actually enforced by current architecture? | PASS, scoped | `LanguageCompiler` performs global planning; `LanguageRuntime.Run` uses the already-created session and does not call the compiler or route search. Remaining validation/dispatch are not excluded. |
| Could runtime secretly perform a second composition pass? | PASS for current public path | `LanguageRuntime.Create` verifies exact plan/provider/route bindings and materializes selected components; this is validation/materialization, not global provider/route resolution. |
| Does a concrete plan prove semantic compatibility? | PASS | Dedicated slide keeps structural ≠ semantic compatibility. |
| Does deterministic routing prove equivalent semantics among tied routes? | PASS | Not claimed; determinism is reproducibility, not semantic proof. |

## Performance evidence disposition

Current source contains correctly separated benchmark surfaces:

- `MigrationArchitectureBoundaryBenchmarks` for `LanguagePlan_Compile` and `WistEngine_CreateAndDispose`;
- `FormulaHotPathBenchmarks` for prepared steady-state delegates with parity checking and a prepared C# baseline;
- `FormulaCompilationBenchmarks` for compilation/engine-creation boundaries;
- `FormulaConvenienceBenchmarks` for `Evaluate` convenience cost.

The benchmark methodology explicitly forbids comparing convenience `Evaluate` with prepared delegates as if they measured the same execution boundary, and treats Dry runs as smoke rather than performance evidence.

No exact-current-revision raw result bundle with commit, environment, BenchmarkDotNet configuration and raw artifacts is bound into this presentation. Therefore numerical claims remain `NEEDS MEASUREMENT`.

## Remaining risks

1. `LanguageRuntime.Create` and `Run` still perform real validation/materialization/session work; the talk must never compress “no re-planning” into “no overhead”.
2. Transformation route `Cost` is a domain planning weight. Calling the result “minimum-cost language” would overstate the algorithm.
3. Optional JIT/AOT specialization remains future empirical work.
4. The presentation pins source truth to an exact commit; any future UniversalToolchain change requires re-running the evidence and demo contract before moving the pin.
