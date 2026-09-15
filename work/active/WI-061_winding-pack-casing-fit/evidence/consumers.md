# WI-061 dependency and consumer inventory

## Physical dependencies

- `models/library/analyses/mfe_magnet_field.sysml`: pack sizing s, s² volume and stress proxy; current follows demand and reference density/purchased-envelope grade. Preserve these equations.
- `models/library/analyses/mfe_plasma_scaling.sysml`: radial build sets coil outer radius to vessel outer radius plus `coil_t_in`, and centre to vessel outer radius plus half that allocation. `coil.coil_t` is independently held at 0.30 m in the design. It can bound the exterior radial envelope under an explicit local radial-alignment assumption.
- `models/library/cost_structure/mfe_power_core.sysml`: magnet owns sizing, grade, inventory, procurement and support calculations. Add fit here with public pack/casing inputs and expose margin outputs.
- `models/library/structure/mfe_magnet_parts.sysml`: pack and casing quantity owners. Amend the stale casing doc that still describes exclusive casing pricing predating WI-059; current nominal prices total support exclusively.
- `models/library/structure/mfe_plant_systems.sysml` and `models/library/analyses/mfe_cryo_inventory.sysml`: thermal area is n×circumference×4×(s+2t_case). Retain its explicit equivalent-square proxy; thermal t_case does not establish physical cavity wall thickness.

## Executable and current consumer surfaces

| Surface | Required work |
|---|---|
| `exploration/stellarator_e2e/models/` | Byte-identical twins of all changed canonical files and new library file |
| `tests/model_families.py` | Add fit library ownership to MFE |
| `exploration/stellarator_e2e/generated/` | New fit schema/wrapper/manual completion and constraint; preserve twenty-two existing manual bodies |
| `exploration/stellarator_e2e/verify_stellaris.py` | Independent area/geometry calculation and explicit defaults; no cavity inferred from the demand |
| `exploration/stellarator_e2e/studies/oracle_entry.py` | New input/output maps and generated-ID-specific fit operand mapping; add existing public magnet__coil__coil_t → coil_t mapping, absent in entering adapter despite oracle equation support |
| `exploration/stellarator_e2e/studies/manifest.json`, `stellarator.snapshot.json`, `tests/models/data/mfe_census.json` | Refresh through native producers after generation, including instance snapshot omitted in initial WI-060 pass |
| `tests/models/current_mfe_regressions.py` | New current recipe pointer and explicit added parameters/channels; preserve historical fixture bytes |
| `tests/models/test_tape_procurement.py`, `test_winding_pack_cost.py`, `test_conductor_grade.py`, `test_mfe_operating_heating.py` | Existing eighteen-count assumptions must distinguish retained predicates from nineteen total |
| `tests/study/test_operand_bindings.py`, `test_domain_consumers.py`, `test_major_radius.py` | Expanded current native/oracle map and catalog expectations |
| `tests/study/test_verify.py`, `test_valid_empty.py`, `test_known_answers.py`, `financial_radius_controls.py` | Current catalog/indicator counts and feasibility coverage; inspect lineage before changing historical expectations |
| `exploration/stellarator_e2e/run_stellaris.py` | Verify headline neutrality and current contract assumptions |

## Generation and verification route

Follow `work/active/WI-060_tape-procurement-quantity-basis/evidence/regenerate.py`, importing the established WI-040 recipe with a WI-061 seed inventory. Record twenty-two identical inherited hashes plus exactly one new reviewed seed; generate two fresh directories and compare complete inventories to production. Generated field order determines completion tuple order. Add new parameters as source literals with citations; avoid static arithmetic turning them into calculation outputs accidentally.

Adapt the native `repin.py` route to evaluate the generated package through study_route/CandidateBridge, compare mapped oracle channels, refresh manifest fingerprint and census, then call `capture_instance_graph_snapshot`. The coordinator owns entering evidence, final integration and study; do not regenerate concurrently with that integration.

The current package has eighteen predicates. Changes must append one predicate, not replace an existing check. Keep an explicit old-predicate set from the entering catalog so nineteen-predicate failure never erases the old-feasibility result. Frozen study records and their old cardinalities remain historical evidence. All new native outputs should be independently mapped, including dimensions, not only the minimum margin.
