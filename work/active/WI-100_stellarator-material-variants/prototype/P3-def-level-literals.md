# Probe P3 — are def-level literals in the specializations entry keys?

Design § 7 P3 (K11). Run 2026-09-30 on the P1/P2 scratch probe package (single material instance `probe_a`).

## What was run

`'Probe Magnet System'` writes `:>> rebco_law_enabled = 0.0;` and `'Probe Cryoplant'` writes `:>> inventory_enabled = false;` and `:>> intercept_demand_available = true;` at definition level (the shape design §§ 2.5–2.7 use). The generated `contracts/model_contract.json` was read with `sources/inspect_wiring.py`.

## Generated evidence (`evidence/p1_material_wiring.json`, `entry_keys_matching`)

| Entry key after `stellarator_09_probe__probe_a__` | entry_type | python_type | default |
|---|---|---|---|
| `magnet__rebco_law_enabled` | design_attribute | float | 0.0 |
| `cryoplant__inventory_enabled` | design_attribute | bool | 0.0 (false) |
| `cryoplant__intercept_demand_available` | design_attribute | bool | 1.0 (true) |
| `magnet__coil__arm_slope`, `magnet__coil__arm_x_ref` | design_attribute | float | 0.0 |

`cryoplant__purchase_cost_per_module` is not an entry key in the material copy: its rebinding to a calc output removes it (the aux-cooling module reads `…cryoplant__staged_capital__total`).

## Result

**Emitted.** The def-level literals are overridable entry keys, so "final" holds only by the route. Per K11 the route refuses `magnet__rebco_law_enabled` and `cryoplant__inventory_enabled` under a material prefix, and the key partition names them in the Removed class (review R5). `cryoplant__purchase_cost_per_module` is absent, as K11 allows. No fallback is needed.
