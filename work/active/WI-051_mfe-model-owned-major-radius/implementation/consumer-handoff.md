# WI-051 consumer handoff

**Current-study compatibility remains incomplete and is not certified by WI-051.**

[AGENT] All four implementation phases are executed. This handoff covers the model and two direct callers only. A fresh independent native audit remains required; SV-089 is pending and item completion is not certified. Original F07 remains open. No integration, pin, study, archive, commit or goal-state write was performed by this stage.

## Final production identity

[AGENT] These identities were measured from the revised production bytes after fresh source and independent fresh-snapshot generation. Original prototype identities in the design are historical and do not identify this package. The source change is two logical files, applied identically to canonical and MFE twins.

- Semantic fingerprint: `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e`.
- Executable fingerprint (strict native load): `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c`.
- Package seal SHA256 (`contracts/package_contract.json`): `7afe83954c8b591c7b30c94b64940f9904d9f25ea9cf4fc6da5bbb87f171c9f7`.
- Model contract SHA256: `d2ee3c18e6d087149f55699dd7cdce59f074abcbd861b7824b9310e770b07bc2`.
- Current snapshot SHA256: `5de752af13561c6e8c7f3e5f5abd2cad08a082564039afd32bf622a1c6d24ce6`.
- Complete 23-file source, manual and package SHA256 manifests: [final-identities.json](final-identities.json). Complete entering manifests: [entering.json](entering.json), [entering-package/](entering-package/) and [entering-models/](entering-models/).

| Changed logical source | Final SHA256 |
|---|---|
| `designs/generic_mfe/mfe_plant.sysml` | `266c39d3f069620a22a62879b6b8d8f04527953cf3a439fef222fca89868cad7` |
| `designs/stellarator_09/stellarator_plant.sysml` | `4a98b5a4139992a539c482e3283e9749b34b1b54ef116b74255607fd87aac82a` |

The freshly measured semantic fingerprint equals the original prototype’s semantic fingerprint; the documentation revision preserves semantic meaning. The freshly measured executable fingerprint differs because generated documentation and source metadata are part of the sealed package. Neither value was supplied as an expected identity.

Exactly four normative manual bodies were copied, each verified before and after both generations. The other 65 bodies were generated fresh. Both guarded destinations were absent and created exclusively; [source-attempt-1-freshness.json](source-attempt-1-freshness.json) and [snapshot-attempt-1-freshness.json](snapshot-attempt-1-freshness.json) retain that evidence. Full source/snapshot/production byte equality excludes only runtime caches. [generation.json](generation.json) enumerates every fresh nonmanual body. [generated-body-delta.json](generated-body-delta.json) shows 28 regenerated bodies changed documentation/source locations and all 69 preserve executable Python AST after excluding only docstrings.

| Normative manual path | SHA256 |
|---|---|
| `handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` | `cbb20033c1e30d640b0f46e6dccbef2fd00633572e21aaff5fb64c761c07237f` |
| `handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py` | `30aee9ecd9820a24929de992e70a8c47d65bcd07895633930946d11b86527308` |
| `handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py` | `4f86ff9c90f465893c6684b2d336056ffa0fa2b0671df73ab8ba15c53fa9da37` |
| `handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py` | `ed5872f52003434c873cbd60e17b580427c861f97a088e5dd6c14bcebca5db11` |

## Public input contract and direct edges

[AGENT] Complete public census is 247 → 246. Sole removed pair: `(stellarator_plant_params, stellarator_09__stellaris__magnet__R0)`. No additions. All 246 surviving complete parameter records and input defaults are exact. [contract-delta.json](contract-delta.json) lists every old/new pair; [contract-checks.json](contract-checks.json) lists all five changed operands and six unchanged fixed-anchor edges. Current classifier output is [mfe_census.json](../../../../tests/models/data/mfe_census.json).

All nine edges below originate at `(stellarator_plant_params, stellarator_09__stellaris__R)`. The module prefix is `stellarator_09__stellaris__`. Exactly five former magnet operands changed; the complete remaining binding map is unchanged.

| Consumer module suffix | Formal |
|---|---|
| `coil_length` | `R0` |
| `rb` | `R_in` |
| `field_calc` | `R0` |
| `peak_field_calc` | `R_in` |
| `magnet_cost` | `R0` |
| `geom` | `R_in` |
| `sustain` | `R_in` |
| `divheat` | `R_in` |
| `stored_energy` | `R0` |

Reusable winding, axis-field, stored-energy and conductor functions still accept explicit `R0`; the peak component retains `R_in`. At fixed other component inputs, winding/procurement scale as `14/12.7`, field/energy as `12.7/14`. [standalone.json](acceptance-attempt-2/standalone.json) retains typed inputs and actual results.

Fixed anchors remain `magnet.R_ref=12.7`, `magnet.a_coil_ref=3.1500000000000004`, `wall_peak_R_ref=12.7`, `R_ref_divertor=12.7`. They do not track plant R. Coil bore is `3.0000000000000004`, coil centre is `3.1500000000000004`, and outer build is `3.5500000000000003`. The first two are emitted radial-build outputs; outer build is the retained bore + coil thickness + gap2 + low-temperature shield sum. [checks.json](acceptance-attempt-2/checks.json) and the kept geometry test verify these alongside unchanged source/bindings.

## Complete controls and execution evidence

[INHERITED, REFERENT] The 158 numeric channel expectations were frozen at `2026-09-11T23:28:01.937500+00:00` from T-021 git objects at `2f8856b7`, before prototype generation. The extra raw representation (177 channels) was captured by the original working single runner after prototype generation but before repaired execution. The frozen expectations file incorrectly says that extra capture preceded generation; its bytes and hash remain unchanged. The original helper failed with `PipelineValidationError` from missing constraint-schema routing and has no successful entering helper baseline. Production helper scalars compare against frozen native/single-runner controls, not a claimed old helper success.

| Frozen comparator | SHA256 |
|---|---|
| [prototype/frozen-results.json](../prototype/frozen-results.json) | `65d5e9bb596daca23323c35ffe122e642277767f819a877275e5ff4b8281e589` |
| [prototype/frozen-inventory.json](../prototype/frozen-inventory.json) | `aaf3e6c479f65ee9a27d3ad0ea5b780a2c7086d1174cef54ec7e6b8daeb41dbe` |
| [prototype/frozen-checks.json](../prototype/frozen-checks.json) | `e65359009445997b5a098d1671ef15ab089943a69b25615fc649fb1c51965f4f` |
| [prototype/frozen-source-meaning.md](../prototype/frozen-source-meaning.md) | `92110f6a826da0ed3031db2c361565209271fd43bd20c18798d5bb8a297c1c36` |
| [prototype/expectations.json](../prototype/expectations.json) | `a16c0731e81230060d6c74d0cc93189445ba7f4c06bb002ab2338fe07b25648a` |
| [prototype/direct-entering.json](../prototype/direct-entering.json) | `e571edb45b557e454b10e0a3dea821f71b4699693dac266eeaa863c110b8885d` |

[AGENT] Baseline channel sets and all values are exact: 158 scalars, 177 single-runner raw outputs, 18 authored evaluations plus aggregate, normalized serialized reports, observed operands and margins. Ordinary R14 changes only plant R in a complete JSON group and matches the pre-repair coordinated control across all outputs, including every cost/finance channel and both LCOEs. R14 numeric tolerance is relative and absolute `1e-9` in existing channel units; channel sets and verdicts are exact. Direct structured outputs also matched exactly.

- [numerical-report.md](acceptance-attempt-2/numerical-report.md): every scalar expected/actual baseline and R14 value and all named verdicts.
- [results.json](acceptance-attempt-2/results.json): strict native actual outputs/responses/reports and all invalid/refused proposals.
- [direct-production.json](acceptance-attempt-2/direct-production.json): complete actual outputs/errors for both actual production functions.
- [direct-production/](acceptance-attempt-2/direct-production/): complete per-case JSON input groups and byte-identical generated pipeline copies. R14 changes only `stellarator_09__stellaris__R=14.0`; all other public inputs stay at baseline.
- [checks.json](acceptance-attempt-2/checks.json): independent volume/winding `14/12.7`, field/energy `12.7/14`, peak `(12.7-c)/(14-c)` with `c=3.1500000000000004`, and plant conductor-procurement invariance. Computed B×R cancels at fixed current. Decomposed magnet capital follows full frozen winding/casing controls; no total-cost ratio is asserted.

Baseline violates divertor heat. R14 additionally violates wall load, sustainment and loop capacity. Both aggregate responses are violated; neither diagnostic represents a feasible plant.

## Refusal and adverse cases

[AGENT] Both direct functions expose keyword-only `pipeline_path` and `output_dir`, retain baseline defaults, and load complete typed JSON groups. The supported input graph is an unchanged generated pipeline; no flat-key alias, filtering, external tie, model-copy bypass or alternate graph is certified. The helper registers output schemas once and filters only its returned scalar outputs; input validation remains intact.

The old key alone, equal alongside plant R, conflicting alongside R and magnet-zero are all explicitly refused by the strict evaluator, generated extra-forbidden schema and both direct functions, naming the exact old key. “Alone” is the old-key-only proposal applied to a complete baseline group. The actual baseline CLI retains all existing gates; its old-key alone/equal/conflicting/zero arguments are rejected with the exact submitted text. CLI tests isolate only output placement via [cli_entry.py](cli_entry.py) and execute the production script as `__main__`. Evidence: [schema-refusals.json](acceptance-attempt-2/schema-refusals.json), [cli-checks.json](acceptance-attempt-2/cli-checks.json), direct/native records above.

| Unified plant R | Direct failure | Strict evaluator |
|---|---|
| 4, 3 | SustainmentError | EvaluationFailed |
| Exact coil centre, 0 | ZeroDivisionError | EvaluationFailed |
| −1 | TypeError from complex arithmetic | EvaluationFailed |

Original `plant_zero` and `magnet_zero` records remain in frozen-results.json. Unified zero need not reproduce the old scheduler/message ordering. The now-retired magnet-zero proposal fails input validation. There is no clipping or fallback.

**F07 stays open.** Typed peak-component controls reproduce `original_negative=-792.6499999999979 T` and `reference_inverted=-0.7821989528795832 T`, both still satisfying the upper-bound comparison. Live/reference equality fail with ZeroDivisionError; the retained baseline component is named `valid`. Full inputs and original outcomes remain frozen; actual component results are in checks.json. These finite probes establish no general domain.

## Separate coding migration contract

**Current-study compatibility remains incomplete and is not certified by WI-051.** The following current surfaces remain unchanged and need a separately certified coding migration:

| Surface | Required later change |
|---|---|
| `exploration/stellarator_e2e/verify_stellaris.py` | Use plant R consistently for magnet operation and sustainment. Its sustainment radius operand is currently incorrect. Preserve fixed reference anchors, finance/cost formulas and adverse component evidence. |
| `studies/oracle_entry.py` | Remove the retired mapping; reject old flat keys before filtering or conversion, including equal/conflicting proposals. Match the exact 246-entry contract and nine edges. |
| Current `studies/manifest.json`, `study_route.py`, `ANNEX.md` | Remove radius tie/injection, describe model-owned R and refresh contract/package identities. Preserve native failure/constraint behavior versus study validity-mask distinctions. |
| `tests/study/` | Migrate current mappings, fixtures, census, graph and independent-axis expectations to no-tie R-only14 controls at the stated tolerance. Preserve generic tie-mechanism tests and historical studies/packages/snapshots/pins. |

## Validation, reproduction and audit boundary

[AGENT] [validation.md](validation.md) maps every MR-051 requirement to exact kept test nodes and production evidence. Final model regression: 428 passed / 13 inherited skips; all 364 entering passes remain and 64 new tests execute. [regression-diff.json](regression-diff.json) retains every node/outcome/reason and the exact delta. L1/L3/L4/L5 pass; L2 fails with ten inherited findings and L6 with 229. [full-validation-diff.json](full-validation-diff.json) retains raw and normalized messages, multiplicities and affected locations with no added/removed finding. This is not an all-level-pass claim.

[AGENT] [citation-attachments.json](citation-attachments.json) resolves the source/basis chain against T-021. Native PM recorded two trace rows and SV-083–088 passing; SV-089 remains pending. Native trace rows use CRLF, so git diff --check reports their line endings. Original evidence and excluded study surfaces remain exact. [protection-diff.json](protection-diff.json) separately records the bounded current-model count correction and concurrent parent commits, verified against git objects; none of the parent research/goal changes was a WI-051 write.

Run the shared acceptance path into a new destination, using the retained launcher (it sets the required TEAx environment for every child). Required tests fail rather than skip without native capability:

```bash
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/run_acceptance.py /tmp/wi051-new-acceptance
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/test_mfe_major_radius.py tests/models/test_model_family_spines.py -v -ra'
```

Use a destination that does not yet exist. The original implementation generation destinations are retained and intentionally refuse reuse. Kept family tests independently generate source/snapshot packages in fresh temporary directories with the same four-seed guard. [commands.md](commands.md) records executed commands/exits and all failed attempts; production acceptance child commands are in [commands.jsonl](acceptance-attempt-2/commands.jsonl).

[AGENT] Parent should open a fresh independent native audit against the accepted spec, revised design, approved plan and this production evidence. The auditor must assess MR-051-07/08/09 and SV-089, verify the requirement/evidence coverage and scope preservation, and independently decide whether the item meets its contract. This author supplies implementation evidence only.
