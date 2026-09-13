# WI-049 executable migration

[AGENT] Production execution retains 19 entries. Two Real duration entries move from `lcoe_calc__construction_years` and `lcoe_calc__operational_years` to `construction_duration` and `operational_duration`. Defaults remain 5.0 and 40.0 years. Eighteen entries are now design attributes and one is a library default. The 30 previous numerical outputs remain; `pv_factors__construction_factor` and `pv_factors__operation_factor` are added. All public names retain `hif_plant_pkg__hif_plant__`.

The native generated package was regenerated with `GenerationConfig` and `run_codegen`. Both typed manual completions are shipped and copied into temporary packages by `tests/ife_execution.py`. The factor tuple order remains operation then construction. The direct supported caller `exploration/ife_e2e/eligibility.py:46` invokes the factor module before the cost module and binds named outputs. `run_anchors.py` consumes that caller. No current caller contains a duplicate stable-factor formula.

The actual migrated test surfaces are `tests/ife_oracle.py`, `tests/models/test_model_family_spines.py`, `tests/models/test_ife_operating_point_repair.py`, `tests/models/test_ife_zero_discount_repair.py`, and `tests/test_ife_consumer_eligibility.py`. The WI-048 structural assertion now counts the 16 required core inputs before the separate factor definition. The retained caller census is `caller-census.txt`; old direct calls and keys outside generated files remain only in immutable historical study context.

## Deferred study refresh

[INHERITED: plan.md Phase 2] `exploration/ife_e2e/studies/study_route.py` and its manifest still describe the previous channel set and package identity. `tests/study/test_ife_native_route.py` consequently fails closed after package regeneration; the separate run is retained in `deferred-study-tests.txt`. This is expected interface staleness assigned to the following package task, not a waived production numerical regression. No study execution or pin promotion occurred here.

The study adapter `exploration/ife_e2e/studies/oracle_entry.py` imports the current `tests.ife_oracle.BASE`, so its baseline keys migrate transitively. Its duration validation still tests suffixes `construction_years` and `operational_years`; it no longer catches the new duration names. This stale study validation contract requires explicit refresh alongside the 32-channel metadata. It does not establish an integer-only policy for the Real-valued production model.

`exploration/ife_e2e/studies/20260910-ife-operating-point/results/context/` retains its prior entry snapshots, eligibility implementation, oracle, manifests and package pins as immutable historical evidence. Those files were not rewritten to pretend the previous study executed the new model.

## Native PM limitation

`pm trace-element` accepts project requirement IDs only and rejects `MR-WI049-1`; no project requirement was invented or promoted. New rows carry existing DI-005 and explicit local MR references in Source_Location. Native duplicate detection prevents updating an existing element row, so the affected LCOE row was refined directly in the existing CSV schema. The new factor and both duration rows were created through native trace operations. Source interpretation is unchanged.
