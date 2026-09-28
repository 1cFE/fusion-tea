# Native IHX screen implementation

[AGENT] Implemented only the T-007 partial review release and T-008 scope on 2026-09-20. The entering WI-078 seed remains unchanged. The successor seed is `seeds/cooling_equipment_impl.py` in this item. Existing geometry, required-area formula, Boolean, price, inventory, thermal-state guards and qualification outputs are unchanged.

## Exact output and formal mapping

| Surface | Name | Meaning/binding |
|---|---|---|
| `Cooling Equipment` Real output | `ihx_capacity_margin_m2` | Raw per-exchanger installed area minus required area, square metres |
| `Cooling Equipment` Real output | `ihx_capacity_defined` | Active valid calculation returns 1; dormant returns 0 before arithmetic |
| `Primary Heat Transport` EXPOSE | `ihx_capacity_margin_m2` | `equipment.ihx_capacity_margin_m2` |
| `Primary Heat Transport` EXPOSE | `ihx_capacity_defined` | `equipment.ihx_capacity_defined` |
| `Intermediate Exchanger Capacity` formal | `defined_in` | `heat_transport.ihx_capacity_defined` |
| `Intermediate Exchanger Capacity` formal | `margin_m2_in` | `heat_transport.ihx_capacity_margin_m2` |
| Stellarator assertion | `ihx_capacity_ok` | `defined_in >= 1.0 and margin_m2_in >= 0.0` |

Expected named output aliases after regeneration are `stellarator_09__stellaris__heat_transport__ihx_capacity_margin_m2` and `stellarator_09__stellaris__heat_transport__ihx_capacity_defined`; corresponding calculation outputs use the additional `equipment__` segment. These are output additions, not new public input choices. Coordinator must confirm generated spelling and native inventory identity; generation was intentionally not performed by this worker.

The existing `equipment.ihx_capacity_ok` Boolean is unchanged. The new asserted constraint is a distinct native verdict fed by numeric formals. A dormant calculation has zero area carriers and definedness zero, so the assertion fails for undefinedness rather than receiving physical adequacy credit. Reports can distinguish this from an active negative margin using the separate output. Invalid active thermodynamic states still raise; no rating or area is automatically enlarged.

## Verification

- `.codex-test/run python -m pytest tests/models/test_supplied_thermal_capability.py -q`: 8 passed. Covers insufficient/sufficient area at fixed installed hardware, fixed price under changed heat, supplied circuit-count changes with inventory/cost response, dormant definedness, three invalid-domain cases, preservation of all old outputs and tiny positive/negative margins around the actual floating-point boundary without snapping.
- `.codex-test/run agentic-mbse validate --level=1 models/`: 48 files, zero errors and zero warnings.
- All four edited production/twin pairs were checked byte-identical after edits.

Native package execution, assertion lowering/aggregate inclusion, oracle extension, schema/read-set migration, regression fixtures and registry updates remain coordinator-owned and unverified here. No full-suite tests or package generation were run. Conditional area comparison does not qualify pressure design, heat-transfer coefficients outside their existing assumptions or complete installed equipment.
