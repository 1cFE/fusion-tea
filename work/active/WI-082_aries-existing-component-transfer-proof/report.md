# Conditioned fuel reuse result

[AGENT] Five isolated native TEAx cases execute the unchanged fuel-flow balance and offered-capacity screen. This establishes transfer of those relations to a new component assembly. It does not qualify ARIES fuel equipment, breeding or plant performance. Independent review accepted this bounded result; see [implementation review](../../orchestration/aries-transfer-experiment/evidence/implementation-review.md).

## Measured result

| Case | Supplied fusion MW | Supplied rating, T atoms/s | Calculated exhaust, T atoms/s | Scalar capacity result |
|---|---:|---:|---:|---|
| Reference load | 2436 | 2e22 | 1.6432423549621273e22 | Satisfied |
| Smaller supplied hardware | 2436 | 1e22 | 1.6432423549621273e22 | Violated |
| Twice the load, same hardware | 4872 | 2e22 | 3.2864847099242546e22 | Violated |
| Half the load, same hardware | 1218 | 2e22 | 8.216211774810637e21 | Satisfied |
| Unsupported offered conditions | 2436 | 2e22 | 1.6432423549621273e22 | Undefined capability; no adequacy credit |

[AGENT] Under the explicit 5% burn and 99% recovery scenario, the reference burn is 8.648643973484881e20 T atoms/s, or 136.59731342720096 kg per 8760-hour full-power year. Those scenario fractions are not source-validated ARIES operating data. The last case's native conjunction reports `violated` because `evaluation_defined=0`; it must be read with `supported=false`, not as a physical equipment shortage. All raw outputs and effective inputs are retained in [results.json](evidence/results.json).

## Reuse and change count

[AGENT] Two existing calculation definitions are reused unchanged: `Fuel Cycle Flows` and `Offered Capacity Screen`. One existing constraint definition is reused unchanged: `Offered Equipment Capacity`. The new design has two component occurrences, two calculation usages, their bindings and three exposed outputs. There are zero new physical equations, zero changed shared library files and zero modified baseline runtime files. The capacity native completion is carried exactly except its package import prefix. The fuel-flow body is generated from the unchanged definition. [Reuse hashes](evidence/reuse-hashes.json) compare the whole source files to the isolated generation copies; [reference hashes](evidence/reference-hashes.txt) identify the existing implementations and inspected source image.

[AGENT] This is functional reuse, not a declaration count: generated `pipelines/pipeline.yaml` binds computed `flows.exhaust_rate` directly to `capacity.demand_in`; that result's margin and definedness drive the executable constraint. Required flow responds to supplied fusion load while the independently supplied rating stays unchanged. Inventory and cost are outside this assembly, so no inventory/cost preservation claim is made.

## Verification and limitations

[AGENT] All seven fuel outputs in each of five cases agree exactly with the existing baseline function, giving 35 comparisons. That baseline function receives only an import-prefix remap for the comparison; it supplies none of the executed case outputs. Independent 50-digit decimal energy-to-reaction arithmetic and tritium conservation checks pass, as do exact doubling/halving response and supplied-rating preservation. The executable constraint is assessed once in each native run and agrees with the expected satisfied/violated status. Positive undefined-case margins cannot manufacture supported success.

[AGENT] `agentic-mbse validate --complete` returns exit 1: L1–L5 pass, and L6 rejects the three plain EXPOSE expressions with unsupported `.` diagnostics. This is an independently accepted scoped static-tool exception, supported by the generated dependency graph and successful five-case TEAx execution of those exact edges. It is not a claim that all six validation levels pass. The review independently replayed a fresh 3000 MW case and the unsupported case. No broad regression was run because this assembly does not edit shared definitions or baseline packages.

[AGENT] Failure history is retained: `execution-attempt-01.log` records the initial absent baseline package alias; `validation-attempt-01.log` records literal-binding warnings plus the same EXPOSE diagnostics; `results-attempt-02.json` preserves the successful result before the scenario literals became named attributes. Final generation/completion logs, final validation log and final results describe the current design.

[AGENT] The source Table VII fusion load was visually checked. Its use here is a supplied subsystem boundary, not fusion-power validation. The definition necessarily emits breeding arithmetic; zero is supplied to its unused achieved-TBR formal and every breeding channel is excluded from the accepted result. A raw 1.19 required ratio under these assumptions is not a predicted ARIES breeding outcome. Independent ARIES fuel qualification still needs burnup, recovery, extraction, inventory/residence times, actual equipment rating and supported operating conditions.

## Reproduce

```bash
.codex-test/run python exploration/aries_transfer/fuel_reuse/build.py
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/fuel_reuse/run.py
.codex-test/run agentic-mbse validate --complete exploration/aries_transfer/fuel_reuse/input_models
```

[AGENT] `build.py` stages byte-identical shared source files, generates the isolated package, carries the one guarded native completion, then regenerates with `--preserve-handwritten` so the package contracts match. `run.py` loads the resulting package with the real provisional loader and executes five case pipelines with supplied input overrides. Runtime stores and staging copies are ignored; the generated package, contracts, repeatable scripts and compact evidence are retained.
