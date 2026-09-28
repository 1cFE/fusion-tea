# WI-069 implementation readiness

Preparation complete on entering revision `e36fe456805655fe404d49a5fd4d83f9f8c814a4`. Scientific implementation remains gated on the coordinator's reviewed-design release. This preparation changed only WI-069 evidence files. Existing model, executable, tests, frozen r2 and historical study content were preserved.

## Consumers and implementation boundary

- `models/library/analyses/mfe_fuel_cycle.sysml` owns required-breeding arithmetic and the burn/injection/exhaust/loss rates. Its inventory formal is atoms; kg stock must be converted explicitly before binding it.
- `models/library/structure/mfe_plant_systems.sysml:385` owns the generic Fuel Cycle, dormant inventory defaults, flow calculation and fuel-cost calculation. `models/designs/generic_mfe/mfe_plant.sysml:101` supplies fusion power, calendar availability, blanket TBR and electrical power. A new active inventory calculation must derive its burn rate independently of the existing fuel calculation to avoid an inventory → fuel → inventory cycle.
- `models/designs/stellarator_09/stellarator_plant.sysml:1352` configures the stellarator fuel cycle. Its `breeding_adequacy` reads exposed `I_total`, `lambda_T`, requirement, burn and loss at lines 1941–1949. The blanket continues to own achieved breeding. The vacuum consumer reads fuel-cycle burn/exhaust rates through the generic plant; DT Fuel Cost reads its existing independent feedstock inputs.
- Canonical edits require identical counterparts under `exploration/stellarator_e2e/models/`. A new analysis file also requires MFE ownership in `tests/model_families.py`; reuse of the existing analysis file avoids that addition. Final file placement follows the released design.
- Coordinator owns the independent oracle, study mappings, manifest/snapshot/census and integration/study state. Generated public keys, inventory-input retirement and changed breeding outputs must be handed over before repinning. Existing family tests consume `tests/models/current_mfe_regressions.py`, whose generation receipt currently points at WI-068.

## Generation and strict seed conventions

The current recipe is `work/active/WI-068_layout-based-facilities/evidence/regenerate.py`. It delegates the checked fresh-generation routine to `work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py`. Its native call is `run_codegen(GenerationConfig(output_path=fresh_path, package_name='stellarator_tea', overwrite=True, preserve_handwritten=True, smart_regen=True, models_path=ROOT / 'exploration/stellarator_e2e/models'))`. Invoke any WI-069 reproduction through `.codex-test/run python <recipe.py>` after coordinating shared generation.

The recipe refuses a nonfresh destination; detects every `AUTO_IMPLEMENTED = False` body plus `financial_factors.py`; requires the exact registered filename set and SHA256 values; rejects symlink seeds; copies only checked bodies; verifies they survive generation; and compares two fresh generated inventories exactly before accepting production equality. WI-068 has 34 normative seeds. Both the entering exact filename set and all 34 hashes passed. New manual calculations need a reviewed WI-069 seed manifest extending this inventory without changing unrelated bodies. Manual outputs use the order of generated output-schema fields, not SysML declaration order; compare direct execution and the typed generated wrapper.

## Entering evidence

Command: `.codex-test/run python -m pytest tests/models/test_computed_tritium_breeding.py tests/models/test_lifecycle_calendar.py tests/models/test_model_family_spines.py -q`. Result: **145 passed**, two serialization warnings, exit 0, 77.16 seconds. Receipt: `entering-regressions.log`. This covers existing breeding and invalid-account behavior, calendar boundaries, canonical/twin ownership, family generation, snapshot reproduction, census and mutation checks. No unrelated full suite ran.

Command: `.codex-test/run python work/active/WI-069_fuel-inventory-and-startup/evidence/capture_entering.py`. The script records native validator results without treating its own successful capture as validator success. **L2: success false, 10 issues. L6: success false, 1,076 issues.** Complete issue strings, metrics, entering revision, model/package SHA256 identities and seed checks are in `entering-static-identities.json`; raw output is in `entering-static.log`. Compare issue identities after implementation, not just counts. This capture does not establish engineering validity or classify future added diagnostics.

## Remaining gate

Wait for the source/math/interface design release, then load the exact released design and applicable calculation/binding/operator pattern references before scientific edits. The initial diagram and startup-decay bound in the goal's `current-trace.md` are agent proposals awaiting that release; this readiness record does not approve them.
