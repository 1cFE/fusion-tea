# The swap demonstration (design D9) — materials

Deposited from prototype Stage E (`../README.md`, `../scripts/proto_transform_E.py`, `../model_diff_stage_E.patch`). Nothing here is in the canonical model tree: an uninstantiated calc-bearing definition would be a Level 6 finding there, so the variant lives with the demonstration.

- `mfe_magnet_cost_variants.sysml` — the prototype-only calc def `'Magnet Structure Cost NI'` (`cost = n_coils × m_casing × steel_price × f_steel_fab × (1 + f_ins)`), a formula stand-in, not a sourced model.
- `ni_hts_magnet_system_variant.sysml` — the variant definition: `'NI HTS Magnet System' :> 'Magnet System'` adding `t_charge_h` and `f_ins_markup`, its own template calc `magnet_structure_cost_ni`, and the seam rebind `:>> structure_cost = magnet_structure_cost_ni.cost;`.
- `instance_retype_excerpt.sysml` — the instance's swap: `part :>> magnet : 'NI HTS Magnet System' { :>> t_charge_h = 600.0; :>> f_ins_markup = 0.1; … }`, every existing binding unchanged.
- Executed results: `../results/after_E_result.json` (markup 0.0 — every channel equal to the pin), `../results/after_E2_result.json` (markup 0.1 — `magnet__magnet_structure_cost_ni__cost` 54 432 000 → 59 875 200, the magnet rollup ×1.001008, LCOE 224.60952472804465 → 224.72756193786321, 17 of 156 channels move; the base template calc's channel stays at 54 432 000, dormant).

To re-run: copy `exploration/stellarator_e2e/models` and `exploration/stellarator_e2e/generated` to a scratch folder with no symlink on the path, apply `proto_transform.py`, `proto_transform_B.py`, then `proto_transform_E.py <models> <markup>` in that order (Stage E expects the Stage B/D tree), regenerate with `sysml-codegen generate --overwrite --smart-regen --preserve-handwritten`, and execute with `proto_baseline.py` against `results/point_A.json` and `results/channels_B.json`.
