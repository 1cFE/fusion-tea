# Isolated native execution route

[AGENT] The smallest demonstrated route is a new model tree containing an unchanged library calculation file and a new design instance, generated into a separate Python package, then loaded and executed by real TEAx. The demonstrated numbers are synthetic tooling inputs. They establish no ARIES engineering result.

## Proven command sequence

Run from the repository root. The scratch model tree contains a byte copy of `models/library/analyses/mfe_heating_chain.sysml` and the retained `evidence/route-probe.sysml`. The source calculation is `mfe_heating_chain::'Heating Power Chain'`; its implementation is generated automatically.

```bash
mkdir -p /tmp/aries-native-route/models
cp models/library/analyses/mfe_heating_chain.sysml /tmp/aries-native-route/models/
cp work/orchestration/aries-transfer-experiment/evidence/route-probe.sysml /tmp/aries-native-route/models/route.sysml
.codex-test/run sysml-codegen generate --models /tmp/aries-native-route/models --output /tmp/aries-native-route/route_tea --package-name route_tea
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python work/orchestration/aries-transfer-experiment/evidence/route-execute.py
```

`--models` accepts a directory or file; a directory is convenient when imports need several library files. `--output` is the package root itself. The package name controls generated imports and registry name. The real `ProvisionalPackageLoader` accepts this root plus package name and creates an import link under its separate link root. `execute_pipeline` consumes the generated `pipelines/pipeline.yaml`, registry, and `CUSTOM_SCHEMA_TYPES` from that loaded module. This follows the existing public execution route in `tests/test_codegen_teax_acceptance.py`.

The launcher alone does not expose `simkit`; the extra TEAx source path is documented in `docs/integration_seam_operator_guide.md`. The first execution attempt established that absence; the second used the documented path and passed all four explicit output assertions. Generation emitted one calculation module. Inputs were wall-plug power 10 MW, source efficiency 0.5, and coupling efficiency 0.8. Outputs were wall-plug capacity 10 MW, delivered capacity 5 MW, coupled capacity 4 MW, and combined efficiency 0.4. See `evidence/route-generation.log`, `evidence/route-execution.log`, and the executable `evidence/route-execute.py`.

## Existing manual implementations

[INHERITED: tests/ife_execution.py] For calculations that generate stubs, the established native completion route is: generate the new package; copy only needed existing typed manual implementations into their same relative `handwritten/<sysml_package>/<calculation>_impl.py` homes; replace absolute `from stellarator_tea.` imports with the new package prefix where present; regenerate with `--overwrite --preserve-handwritten`. That second generation refreshes the package contracts and seal around the completed bodies. Do not copy baseline contracts into a newly generated package.

The current MFE seed inventory is `work/analysis/model-evaluation-diagnostics/candidate-seeds.json`, selected by `tests/models/current_mfe_regressions.py:425`. It identifies normative manual files and hashes, including support files such as `financial_factors.py`. The retained family recipe ultimately reads these from the baseline package, but its whole-family entry point should not be called against the baseline for this isolated task. Select the bodies needed by the isolated generated wrappers and include their imported helpers. Auto-generated bodies need no copying.

The contract is the generated schema and wrapper: the manual function consumes the generated typed input object and returns the scalar or tuple in the generated wrapper's output order. For example, Heating Power Chain returns `(p_wallplug_total, p_delivered, p_coupled, eta_pin_eff)`. Its four output names and order are already mapped by the native generator; independent code must not infer order from prose or SysML declaration order. A manual body copied for a different library version requires an input/output contract comparison before execution.

The manual completion recipe above is grounded in existing accepted tests; this probe exercised the simpler all-generated path only. The new ARIES model may require a separate completion and execution check after its selected calculations are known.

## Scope of evidence

[AGENT] The probe wrote generated files, TEAx links, and runtime output only under `/tmp/aries-native-route`, with durable evidence under this experiment. It did not invoke baseline regeneration, a study registry, the integration seam, or a full regression run. `exploration/stellarator_e2e/generated` was read solely as an existing implementation reference. The probe is execution evidence, not full six-level model validation or source validation.
