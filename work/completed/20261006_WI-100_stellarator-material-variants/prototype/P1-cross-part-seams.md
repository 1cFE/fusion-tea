# Probe P1 — cross-part reads of rebound seams, and the Boolean seam

Design § 7 P1 (K8, K10, D1). Run 2026-09-30 on scratch copies only; nothing in the repository's model trees or packages was touched.

## What was run

- Staged a scratch copy of the 42 `exploration/stellarator_e2e/models` twin files and applied the 15 hunks of `seams/seam_hunks.json` with `sources/stage.py` (each `old` found exactly once; the reversed set reproduced the twin bytes).
- Added `sources/probe_variants.sysml`: `'Probe Magnet System' :> 'Magnet System'` rebinding `winding_cost` to a new calc output and `rebco_law_enabled = 0.0`, and `'Probe Cryoplant' :> 'Cryoplant'` rebinding `purchase_cost_per_module`, `cold_load_W_required`, `intercept_load_W_required`, `intercept_demand_available = true`, `p_elec` and `p_drive` to new calc outputs (each a stock `'Electrical Power Sum'` so the producer is identifiable).
- `sources/make_probe_design.py` wrote a copy of `part stellaris` as `part probe_a` (E1, E2 word-boundary rename with count 7, E3/E4 retypes, E5 deletions scoped to the cryoplant block).
- Generated with `sysml-codegen generate --package-name stellarator_materials_tea` from a tree holding only the probe instance (see P2 for why), then read the wiring with `sources/inspect_wiring.py`.
- The same reader ran on the hunked reference alone (`stellarator_materials_reference_tea`).

## Generated pipeline evidence

| Read | Material copy `probe_a` reads | Hunked reference reads |
|---|---|---|
| `pb.p_cryo` (`mfe_plant.sysml:395`) | `…cryoplant__staged_elec__total` | `…cryoplant__refrigeration_sum__total` |
| `power_supplies.tf_power.p_b` (`p_tf_extra`, `mfe_plant.sysml:192`) | `…cryoplant__staged_drive__total` | `…cryoplant__inventory__p_drive` |
| `magnet_capital_rollup.winding_cost` (owner-qualified, `mfe_power_core.sysml:361`) | `…magnet__winding_sum__total` | `…magnet__winding_procurement__cost` |
| `cold_stage_capability.demand_in` | `…cryoplant__staged_cold__total` | `…cryoplant__cold_load_W_demand_conversion__demand` |
| `intercept_stage_capability.demand_in` | `…cryoplant__staged_shield__total` | `…cryoplant__inventory__q_inventory_shield` |
| `intercept_stage_capability.demand_available_in` | entry key `…cryoplant__intercept_demand_available` (bool, default 1.0) | entry key `…cryoplant__inventory_enabled` |
| `aux_cooling.purchase_cost_in` | `…cryoplant__staged_capital__total` | entry key `…cryoplant__purchase_cost_per_module` |

Full maps: `evidence/p1_material_wiring.json`, `evidence/p1_reference_wiring.json`. The reference's `tf_power` wiring equals the pinned package's (`exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:2074-2080`).

## Result

**PASS.** Every cross-part consumer in the plant definition follows the variant's rebinding, including the owner-qualified rollup read. No fallback is needed: contingent hunk H6 is not applied, the copy's `p_tf = 0.0` and `p_cryo = 0.0` stay as they are (review R1/R2 fallbacks unused).

K10: the literal `true` rebinding of the Boolean seam surfaces as an entry key under the material prefix (`cryoplant__intercept_demand_available`, bool). In the reference the seam resolves to `inventory_enabled` and adds no key. As K10 says, the route lists it among the Boolean keys; like the other WI-080 `demand_available` flags it can only remove capability credit.
