---
Status: proposed
Created: 2026-09-30
Updated: 2026-09-30
Related Artifacts:
  - spec.md
  - ../../orchestration/goals/magnet-material-comparison/evidence/plant-contract.md
  - ../../orchestration/goals/magnet-material-comparison/evidence/plant-chain-audit.md
---

# WI-100 design: plant-level conductor material variants on the Stellaris plant

Author: T-013 fresh modeler, brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t013-design.md`. Governing contract: `evidence/plant-contract.md` **r4** (released 2026-09-30; cited "contract § n"). Spec: `spec.md` R1–R7. Evidence: `evidence/plant-chain-audit.md` §§ 2, 4, 6 (cited "audit"). Nothing is implemented by this document; a fresh reviewer checks it before implementation. Every choice here is `[AGENT]` unless marked otherwise.

## 0. The design in one screen

- Two magnet variants, `'Nb3Sn Magnet System'` and `'Round1 REBCO Magnet System'`, each specialize `'Magnet System'` directly. Each runs Round 1's conductor law, turn-area screen and inventory calcs at its own supply temperature, prices the winding through the existing `winding_cost` seam, and asserts five checks (`acceptance_ok`, `copper_ok`, `steel_ok`, `pack_area_ok`, `ampere_floor_ok`).
- One cryoplant variant, `'Staged Cryoplant' :> 'Cryoplant'`, runs Round 1's cold-stage load and staged refrigeration and feeds four seams: the cold-stage demand, the intercept demand, the refrigeration electricity that reaches `p_cryo`, and the lead/joint drive. Its capital comes from the Green law at the supplied rating.
- Five plant library files need value-neutral edits: a gate on the plant REBCO law, a pack-arm slot on the peak-field calc, and four `default` seams on the cryoplant. **These edits live only in the derived package's staged source copies, not in the canonical library** (§ 1.1 explains why: the repository's twin rule makes any canonical edit a change under `exploration/stellarator_e2e/**`).
- The package `exploration/stellarator_materials/` has three instances. The reference instance is the unchanged Stellaris design file, staged byte-for-byte, so its keys equal the pin's and the WI-098 parity comparison applies with no key map. The two material instances sit in one new design file, generated from the Stellaris file by a declared edit list.
- Regression: the reference instance must reproduce the pin's 1,352 outputs and 67 verdicts bit-for-bit, with a declared delta of three new neutral entry keys and one new output. Protected paths are hash-checked before and after every build and test.

## 1. Placement and isolation

### 1.1 Premise conflict: shared-library edits versus byte-identical `exploration/stellarator_e2e/**` (surfaced, not resolved silently)

The contract (§ 9) and the audit (§ 6 steps 1–4) put the gate, the slot and the seams in the canonical `models/library/` files. Spec R5 also requires `exploration/stellarator_e2e/**` to stay byte-identical. Both cannot hold, for three reasons found in the repository:

- **Twin rule.** Every MFE-owned canonical file must equal its twin under `exploration/stellarator_e2e/models/` byte for byte (`tests/models/test_model_family_spines.py:291-304`; ownership list `tests/model_families.py:57-103`; convention stated in `exploration/stellarator_e2e/STAGED_MODELS.md:3`). A canonical edit therefore forces a twin edit inside the protected tree.
- **Census pin.** The MFE family generated from the canonical subset must match the WI-080 census receipt's semantic fingerprint and parameter set (`tests/models/test_model_family_spines.py:381-392`; `tests/models/current_mfe_regressions.py:13, 688`; `tests/study/test_known_answers.py:161, 174`). The gate and slot add entry points, so the canonical MFE contract would move and those receipts would need re-deriving.
- **Sealed package.** After such a re-derivation the sealed `exploration/stellarator_e2e/generated/` (fingerprint `83ea3b6c…`) would no longer match its sources. The only repair is regenerating it, which R5 and the goal invariant "Package" forbid.

**Resolution proposed `[AGENT]` (option Y, used in the rest of this design).** Canonical files and the twin stay untouched. The derived build stages copies of the stellarator_e2e twin sources and applies a declared, reversible hunk list to five of them (§ 1.3). Two handwritten bodies get modified copies. The new variants library and the materials design file live in the derived package's own model tree, not in canonical `models/`. As a result, zero canonical or protected files change, `tests/model_families.py` needs no new registration, and every existing test keeps its inputs. The cost: the gate, the slot and the seams do not reach the canonical library in this item. Promoting them later needs a canonical edit, a twin edit, a census re-derivation and a stellarator_e2e regeneration, all under the MR-7 review of `modeling_project/REQUIREMENTS.md:103`, and it is outside this goal round.

**Alternative (option X, not used).** Edit canonical and twin together and re-derive the WI-080 census receipts. This follows the audit literally but breaks R5 as written and cascades into test re-pins. It needs an owner ruling on R5.

The SysML text of every hunk is the same under X and Y. Only its location and the build's staging step differ, so a reviewer who prefers X changes § 1.2 and § 1.6 only. **Dependency flagged:** R5's wording and contract § 9's phrase "per the audit's seam proposal" both need the reviewer's or owner's confirmation of Y.

### 1.2 Files

| Path | Kind | Content |
|---|---|---|
| `exploration/stellarator_materials/models/library/analyses/magnet_material_variants.sysml` | new SysML, package `magnet_material_variants` | the three variant part defs, six glue calc defs, one constraint def (§ 2.4–2.9); library defaults neutral (MR-3) |
| `exploration/stellarator_materials/models/designs/stellarator_09_materials/materials_plant.sysml` | new SysML, package `stellarator_09_materials` | parts `rebco_material` and `nb3sn_material`, each a copy of `part stellaris` with declared edits (§ 2.10) |
| `exploration/stellarator_materials/author_materials_design.py` | new script | derives `materials_plant.sysml` from the staged Stellaris file plus the edit list and the default-design values; the build refuses if the committed file differs from its output (drift check, `exploration/component_alternatives/author_model.py` precedent) |
| `exploration/stellarator_materials/reference_designs.json` + `make_reference_designs.py` | new data + script | the two material instances' default supplied designs, generated by the contract § 5 rules (WI-099 `reference-case.json` precedent); design-file defaults must equal it |
| `exploration/stellarator_materials/seams/seam_hunks.json` | new data | the exact `(file, old, new)` hunk list of § 1.3 |
| `exploration/stellarator_materials/bodies/mfe_conductor_current/rebco_conductor_current_impl.py`, `bodies/mfe_plasma_scaling/conductor_peak_field_impl.py` | modified body copies | gate and arm slot (§ 2.1, 2.2); each with a whole-body diff receipt against the stellarator_e2e original (WI-096 design § 4 item 4 rule) |
| `exploration/stellarator_materials/build.py` | new script | staging, hunks, generation, body installation, fixed point, snapshot, census, regression (§ 1.6) |
| `exploration/stellarator_materials/input_models/` | staged copy (committed, WI-096 precedent) | 42 twin files (5 patched) + Round 1 library + the two new files, twin layout |
| `exploration/stellarator_materials/stellarator_materials_tea/` | generated package | `sysml-codegen` output with installed bodies |
| `exploration/stellarator_materials/studies/{study_route.py, prepare_interface.py, interface_data.py, oracle_entry.py, manifest.json, baseline/}` | new route | § 5 |
| `exploration/stellarator_materials/oracle_glue.py`, `oracle-reuse.json` | new oracle (separate author) | § 6.3 |
| `tests/models/test_stellarator_materials.py` | new tests | § 6 |
| `work/active/WI-100_stellarator-material-variants/build/` | evidence (force-added; `.gitignore:4`) | logs, `build-hashes.json`, `regression/baseline-parity.json`, `regression/preservation.json`, body diffs, probe results |

Bodies reused: the 51 manual stellarator_e2e bodies whose stubs the derived generation emits, copied from `exploration/stellarator_e2e/generated/handwritten/` with the WI-093 prefix rewrite `stellarator_tea.` → `stellarator_materials_tea.` (`exploration/component_alternatives/build.py:78-120`, reversibility asserted). The two bodies of § 1.3 replace their originals. Six Round 1 bodies from `exploration/magnet_materials/bodies/magnet_conductor_alternatives/` (Nb₃Sn surface, REBCO surface, area screen, inventory, cold-stage load, refrigeration screen) get the WI-099 typed adapter (`exploration/magnet_materials/build.py:79-107`). The two unused Round 1 bodies (annualized cost, pair comparison) are not installed; contract § 6 adds nothing from Round 1's annualization. The glue calcs are expression calcs that codegen auto-implements, so they need no body (probe P4 confirms this for the conditional one).

### 1.3 Staged-copy hunks (value-neutral), with the reason each is neutral

| # | Staged file (canonical anchor) | Exact edit | Why neutral at the reference |
|---|---|---|---|
| H1 | `analyses/mfe_conductor_current.sysml` ('REBCO Conductor Current', `:3-38`) | append `in attribute enabled : Real default 1.0;` after `:26`; append `out attribute evaluation_defined : Real;` after `:37`; one doc sentence on the gate | appended last, so positional bindings keep their prefix (`work/active/WI-099_magnet-conductor-alternatives/implementation-notes.md:26`); at `enabled = 1` body B1 runs the unchanged arithmetic |
| H2 | `cost_structure/mfe_power_core.sysml` ('Magnet System') | add `attribute rebco_law_enabled : Real default 1.0;` after `:108`; append `in enabled = rebco_law_enabled;` to the `conductor_current` usage after `:209`; append `in wp_side_in = winding_pack.wp_side; in arm_slope_in = coil.arm_slope; in arm_x_ref_in = coil.arm_x_ref;` to `peak_field_calc` after `:173` | new values reach only the gate and the slot, both identity at their defaults |
| H3 | `structure/mfe_magnet_parts.sysml` ('Modular Coil', `:4-54`) | add `attribute arm_slope : Real default 0.0;` and `attribute arm_x_ref : Real default 35.278;` after `:50` | slope 0 disables the arm |
| H4 | `analyses/mfe_plasma_scaling.sysml` ('Conductor Peak Field', `:420-494`) | append `in attribute wp_side_in : Real default 1.0; in attribute arm_slope_in : Real default 0.0; in attribute arm_x_ref_in : Real default 0.0;` after `:486`; amend the doc at `:440-442` ("not carried" → "carried only through the optional arm slot, off by default") and add the arm equation and its domain | `ratio_eff = peak_ratio + 0.0·(x − x0)` equals `peak_ratio` exactly in IEEE-754 for finite x, so `(B_axis·ratio_eff)·bore_norm` keeps its bits (`:449-454` order preserved) |
| H5 | `structure/mfe_plant_systems.sysml` ('Cryoplant', `:463-652`) | `:485` `cold_load_W_required` `=` → `default`; add `attribute intercept_load_W_required : Real default inventory.q_inventory_shield;` and `attribute intercept_demand_available : Boolean default inventory_enabled;`; re-point `:500` to `intercept_load_W_required` and `:503` to `intercept_demand_available`; `:586` `p_elec` and `:587` `p_drive` `=` → `default` | `=` → `default` has no numeric effect (WI-057 D5, `work/active/WI-057_stellaris-structural-decomposition/design.md:55`); the re-pointed reads resolve to the same channels (`exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:1792-1793`) |
| B1 | `handwritten/mfe_conductor_current/rebco_conductor_current_impl.py` | first statement: refuse `enabled ∉ {0, 1}`; if `enabled == 0`, return every output 0.0 (including `evaluation_defined`) before any domain check; else run the existing body unchanged and add `evaluation_defined = 1.0` | WI-080 pattern (`models/library/analyses/mfe_viability.sysml:106-118`); arithmetic at 1 unchanged |
| B2 | `handwritten/mfe_plasma_scaling/conductor_peak_field_impl.py` | after the two existing clearance guards, refuse nonfinite arm inputs and `wp_side_in ≤ 0`; `ratio = peak_ratio_in + arm_slope_in·(R_in/wp_side_in − arm_x_ref_in)`; refuse `ratio ≤ 0`; return `(B_axis_in·ratio)·bore_norm` | the new guards are satisfied at every evaluable reference design; return order kept |

This is 15 textual edits in 5 staged files plus 2 body copies. The audit's step 2 promoted all eleven `conductor_*` EXPOSEs (`mfe_power_core.sysml:136-146`) to `default`. This design promotes none of them, because their only asserted consumer, `reference_conductor_current_ok` (`models/designs/stellarator_09/stellarator_plant.sysml:2200-2202`), is an instance-level constraint, and the material copies re-point it (§ 2.10 E6). This also avoids the unproven "`default` on an asserted EXPOSE" path. The audit's step 4 re-pointed the thermal-inventory outputs into the cold-load sum. This design instead puts the seams at the demand side (`:485`, `:500`, `:503`) and at the exports (`:586`, `:587`), because Round 1's cold load already includes nuclear and joint heat, and feeding it into `'Cold Load Sum'` (`models/library/analyses/mfe_cryo_inventory.sysml:79`) would count those twice.

### 1.4 Protected paths and how the protection is proven

Protected: `models/**` (all canonical, including `models/designs/stellarator_09/stellarator_plant.sysml`), `exploration/stellarator_e2e/**`, `exploration/magnet_materials/**`, `tests/model_families.py`. `build.py`, the regression script and the test module each hash these trees before and after they run, excluding `__pycache__` (the pattern of `work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/probe.py:18-19, 37-39`). They write `preservation.json` and fail on any change. At close, `git diff --stat` on the protected paths must be empty (R5). Staging reads the stellarator_e2e twin, which I9 keeps equal to canonical, and asserts that equality before patching (the pattern of `work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/regenerate.py:63-65`).

### 1.5 Regression: reuse of the WI-098 magnet-probe comparison

- **Pin.** The pin is `work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json`: 1,352 outputs and 67 verdicts plus the headline, at executable fingerprint `83ea3b6c…` (`exploration/stellarator_e2e/studies/manifest.json`, `recorded_provenance`). The magnet probe already reproduced it exactly (`…/magnet-probe/report.md:12`; `baseline-parity.json`).
- **Inputs.** The pin's full input map is `…/magnet-probe/baseline-inputs.json` (704 keys, `stellarator_09__stellaris__` prefix). The reference instance is the staged, unchanged `part stellaris`, so its keys and prefix are identical and no key map is needed.
- **Comparison.** The regression script adapts `…/magnet-probe/summarize.py:6`'s `parity` dictionary. It runs one evaluation of the derived manifest's baseline point: the reference at pin inputs plus the three new keys at their neutral defaults, and the material instances at their design defaults. It then compares reference-prefix outputs and verdicts with the pin.
- **Acceptance.** `missing = []`, `unequal = {}`, `verdict_unequal = {}`. `added` equals the declared delta exactly: output `stellarator_09__stellaris__magnet__conductor_current__evaluation_defined = 1.0`. Any surfaced alias channel for the H5 seams must equal its source channel and be added to the declaration. The entry-key delta must equal `{magnet__rebco_law_enabled: 1.0, magnet__coil__arm_slope: 0.0, magnet__coil__arm_x_ref: 35.278}`. The reference headline is recomputed from its 67 verdicts, because the package headline covers 213.
- **Constraint ids.** They carry a 16-hex suffix. They are expected to be identical because no constraint or bound operand in the reference changes. If the suffix recipe moves anyway, compare by the suffix-stripped name, require it unique, and record the id map.
- **Continuous check.** The reference instance runs in every case, so the derived route also asserts on every completed case that reference-prefix outputs equal the pin. The comparison is cheap, and it turns every study case into a regression witness.

### 1.6 Build steps (`exploration/stellarator_materials/build.py`)

1. Hash the protected trees. Assert twin == canonical for the 42 MFE files.
2. Stage, in twin layout, into `input_models/`: the 42 twin files, `models/library/analyses/magnet_conductor_alternatives.sysml`, and the two new SysML files. Apply `seam_hunks.json`: each `old` must occur exactly once, and reversing each hunk must reproduce the source bytes. Record source, patched and hunk digests. Refuse if `author_materials_design.py` output differs from the committed design file.
3. Check positional bindings for every usage of a hunked or new definition (extending `exploration/magnet_materials/build.py:54-72` to the staged tree).
4. Run `sysml-codegen generate --package-name stellarator_materials_tea`. Install bodies (§ 1.2) and assert that the installed set equals the emitted manual-stub set. Regenerate with `--smart-regen --preserve-handwritten`, prove a fixed point, write the snapshot and the census (`scripts.integrate.rederived_census`), and write `build-hashes.json`.
5. Run the regression (§ 1.5) and write `preservation.json`. Run `execute_baseline` on the manifest point to prove that all three instances evaluate without refusal at their defaults.

## 2. Definitions

Units: A, T, K, m, kg, W unless named. Round 1 areas are mm², Round 1 money is USD2021, plant money is mixed-year dollars (§ 7 K14). Round 1 calcs are reused unchanged by name (`models/library/analyses/magnet_conductor_alternatives.sysml`; equations `work/active/WI-099_magnet-conductor-alternatives/design.md` § 2). Every new definition doc carries Source (this design and contract r4), Reference (section and file:line below) and Basis (`[AGENT]` or `[U]` as marked).

### 2.1 Gated `'REBCO Conductor Current'` (H1, H2, B1)

- New inputs: `enabled` [0/1], default 1.0, bound in 'Magnet System' to `rebco_law_enabled` (`default 1.0`).
- New output: `evaluation_defined` [0/1].
- At 1: equations, domain refusals and outputs are exactly today's (`mfe_conductor_current.sysml:4-6`; body `exploration/stellarator_e2e/generated/handwritten/mfe_conductor_current/rebco_conductor_current_impl.py:9-57`).
- At 0: all 11 existing outputs and `evaluation_defined` are 0.0, returned before any domain check, and no exception is raised. Any other value raises.
- Only the material variants set 0, by redefinition. The plant's REBCO law channels then read zeros, flagged by `evaluation_defined = 0`.
- Citation: WI-080 gating pattern `models/library/analyses/mfe_viability.sysml:106-118`; audit § 6 step 1.

### 2.2 Pack-arm slot on `'Conductor Peak Field'` (H2–H4, B2)

- New inputs: `wp_side_in` [m], default 1.0; `arm_slope_in` [1], default 0.0; `arm_x_ref_in` [1], default 0.0.
- Bindings: `winding_pack.wp_side`, `coil.arm_slope` (`default 0.0`), `coil.arm_x_ref` (`default 35.278`).
- Equations: `x = R/wp_side` (square pack, so `√A_wp = wp_side`); `ratio_eff = peak_ratio + arm_slope·(x − arm_x_ref)`; `B_peak = (B_axis·ratio_eff)·bore_norm`, with `bore_norm` unchanged (`mfe_plasma_scaling.sysml:426-428`).
- Domain refusals: nonfinite arm inputs, `wp_side ≤ 0`, `ratio_eff ≤ 0`, plus today's two clearances (`:465`).
- At `arm_slope = 0` the result is bit-identical to today's for any finite `arm_x_ref`. On the arm cells the instance supplies `arm_slope = 0.0641`, `arm_x_ref = 35.278` (contract § 3.2 r4, marked C).
- Stress (`mfe_power_core.sysml:264-269`), the ceiling (`models/designs/generic_mfe/mfe_plant.sysml:856-859`) and both conductor laws read this `B_peak`, so the arm reaches every field consumer together.
- Citation: contract § 3.2 r4 (C); `evidence/check-field-relations.md` § Relation 2; label [D] on Helias 5, [U] on transfer.
- **r4 dependency.** Spec R3 and audit step 3 name the slot `(a1_ratio, A_wp, A_wp_ref)` in a multiplicative form. r4 prints the additive form with constants (35.278, 0.0641), so the entry keys are `arm_slope` and `arm_x_ref`, and spec R3's wording should follow.

### 2.3 Cryoplant seams (H5)

| Seam (default) | Default producer | Consumer | Rebound in 'Staged Cryoplant' to |
|---|---|---|---|
| `cold_load_W_required` | `cold_load_W_demand_conversion.demand` (`mfe_plant_systems.sysml:482-485`) | `cold_stage_capability.demand_in` (`:488`) | `cold_stage.q_cold` |
| `intercept_load_W_required` (new) | `inventory.q_inventory_shield` | `intercept_stage_capability.demand_in` (`:500`) | `cold_stage.q_shield` |
| `intercept_demand_available` (new, Boolean) | `inventory_enabled` (`:538`) | `intercept_stage_capability.demand_available_in` (`:503`) | `true` |
| `p_elec` | `refrigeration_sum.total` (`:586`) | `pb.p_cryo` (`mfe_plant.sysml:395`) | `refrigeration.p_in_total_MW` |
| `p_drive` | `inventory.p_drive` (`:587`) | `power_supplies.p_tf_extra` (`mfe_plant.sysml:192`) | `staged_drive.p_drive` |

### 2.4 Glue calc defs (new, `magnet_material_variants`; all expression calcs, auto-implemented; defaults neutral)

| Calc def | Inputs [unit] (default) | Equations → outputs | Domain / refusal | Citation |
|---|---|---|---|---|
| `'Material Winding Adapter'` | `reference_turns_in` [1] (1.0), `f_set_in` [1] (0), `c_coil_in` [m] (0), `wp_side_in` [m] (0) | `turn_length = f_set·c_coil` [m]; `pack_area_per_turn = wp_side·wp_side·1e6/reference_turns` [mm²] | positivity is enforced upstream by `'Winding Operating State'` (`mfe_power_core.sysml:187-191`) and downstream by the area screen (`available_area > 0`) | plant conductor-length identity `models/library/analyses/mfe_winding_pack_cost.sysml:44`; contract § 5 pack-side rule; `[AGENT]` |
| `'Material Winding Cost'` | `superconductor_cost_in`, `materials_cost_in`, `helium_cost_in`, `winding_operations_cost_in` [$] (0) | `cost = sum` [$] | none | contract § 6 (one basis; plant helium and winding operations kept, N3, N4); `[AGENT]` |
| `'Pack Field Checks'` | `B_peak_in` [T], `I_coil_in` [A·turn], `R_in` [m] (0), `wp_side_in` [m] (1.0), `mu0_in` (1.25663706212e-6) | `R_over_sqrt_A_wp = R/wp_side`; `ampere_floor = mu0·I_coil/(4·wp_side)` [T]; `ampere_floor_margin = B_peak − ampere_floor` [T] | none (inputs positive upstream) | contract § 3.2 and § 7 r4 (C); `check-field-relations.md` § Relation 1 (13.44 T against 24.6 T at coil 0); μ0 as `mfe_magnet_field.sysml:52-53` |
| `'REBCO Shape Branch'` | `B_peak_in` [T], `B_knot_max_in` [T] (0) | `shape_mode = if B_peak > B_knot_max? 1.0 else 0.0` | none | contract § 4 (measured shape to 20 T, power-law continuation above, continuous at 20 T because g20 = 1 = (20/20)^−α); `[AGENT]` |
| `'Staged Static Loads'` | `n_coils_in`, `c_coil_in` [m], `wp_side_in` [m], `t_case_in` [m], `shield_area_ratio_in` (1.0), `eps_eff_in`, `sigma_SB_in`, `q_MLI_in` [W/m²], `g_per_coil_in`, `k_c_in`, `k_s_in`, `T_cold_in`, `T_shield_in` (77), `T_amb_in` (300), `T_conduction_ref_in` [K], `p_fixed_MW_in` [MW] | `area_cold = n_coils·c_coil·4·(wp_side + 2·t_case)`; `q_radiation = area_cold·eps_eff·sigma_SB·(T_shield⁴ − T_cold⁴)`; `conduction_ref = n_coils·g_per_coil·k_c·(T_shield − T_conduction_ref)`; `shield_static = shield_area_ratio·area_cold·q_MLI − q_radiation + n_coils·g_per_coil·k_s·(T_amb − T_shield) − conduction_ref`; `p_joint_ref = p_fixed_MW·1e6` [W] | none; these are the plant's own static-term equations evaluated without the 10–30 K guard of its thermal-inventory body | plant equations `mfe_cryo_inventory.sysml:11-16` (WI-059 D3–D4); at 20 K they reproduce the pin's 266.68 W, 590.28 W and 7,561.69 W; `[AGENT]` |
| `'Staged Drive Power'` | `q_leads_in`, `q_shield_in`, `shield_static_in`, `q_joints_in` [W], `joint_drive_fraction_in` [1] (0) | `p_drive = (q_leads + (q_shield − shield_static) + joint_drive_fraction·q_joints)·1e-6` [MW] | none | plant drive definition `mfe_cryo_inventory.sysml:17`; reproduces the pin's 0.0502673 MW at 20 K |

New constraint def `'Ampere Floor'`: `in attribute margin_in : Real; margin_in >= 0.0`. A violation files the design as failed (contract § 7 r4, marked C). Bindings form, so the executable profile admits it (`.agentic-mbse/patterns/constraints.md:13-45`).

### 2.5 `'Nb3Sn Magnet System' :> 'Magnet System'`

- **Attributes** (declared without values; the instance binds them with MR-4 docs):
  - Round 1 § 6 conductor names: `n_elements`, `strand_diameter` [m], `strand_copper_fraction`, `p`, `q`, `C1` [A·T/strand], `Ca1`, `Ca2`, `eps0a`, `Bc20` [T], `Tc0` [K], `nuclear_rise` [K], `margin_rise` [K], `fraction_rule`, `acceptance_rule`.
  - Law bounds: `B_law_min`, `B_law_max`, `B_design_max`, `B_edge_max` [T]; `T_law_min`, `T_law_max` [K]; `eps_min`, `eps_max`.
  - Construction names: `cabling_factor`, `cable_void`, `cu_space`, `steel_area`, `misc_area`, `solder_area` [mm²], `ins_fraction`, `J_cu_rule` [A/mm²], `cu_void`, `cu_per_kA_rule` [mm²/kA], `steel_per_kA_rule` [mm²/kA], `B_steel_ref` [T], `steel_B_scaling`.
  - Inventory names: `element_density` [kg/m³], `element_price_per_m` [USD2021/m].
  - Round 1's `T_supply` is not redeclared. It is the plant's `winding_pack.T_inventory = cryoplant.T_cold_cryo` (`mfe_plant.sysml:126`), so the plant has one temperature. Round 1's `rho_*`/`price_*` bind to the plant's `winding_pack` densities and prices (`stellarator_plant.sysml:380-400`), per contract § 6. Round 1's `manufacturing_per_m` is bound to the literal 0.0, because the plant's winding operations are added separately.
- **Redefinitions:** `:>> rebco_law_enabled = 0.0;` and `:>> winding_cost = winding_sum.cost;` (the WI-057 seam, `mfe_power_core.sysml:129`).
- **Calc usages.** Bindings are in definition order. Calc inputs read producing calc outputs directly (WI-057 D4); EXPOSEs are only for outside readers.
  - `conductor : 'Nb3Sn Cable Critical Surface'` binds formals 1–26: `n_strands_in = n_elements`, `turn_current_in = coil.turn_current`, `B_peak_in = B_peak`, `T_supply_in = winding_pack.T_inventory`, the rest to the attributes above. `eps_intrinsic_in` stays unbound (§ 7 K6).
  - `adapter : 'Material Winding Adapter'`: `coil.reference_turns`, `coil.f_set`, `coil.c_coil`, `winding_pack.wp_side`.
  - `area : 'Winding Turn Area Screen'`: `turn_current_in = coil.turn_current`, `B_peak_in = B_peak`, `available_area_in = adapter.pack_area_per_turn`, `element_area_in = conductor.element_area_total`, `element_copper_area_in = conductor.element_copper_area`, construction attributes.
  - `inventory : 'Winding Inventory and Cost'`: `n_elements_in = n_elements`, `element_area_in = conductor.element_area_total`, `turns_in = coil.reference_turns`, `coils_in = coil.n_coils`, `turn_length_in = adapter.turn_length`, `turn_current_in = coil.turn_current`, areas, plant densities and prices, `element_price_per_m_in = element_price_per_m`, `manufacturing_per_m_in = 0.0`.
  - `pack_field : 'Pack Field Checks'`: `B_peak`, `coil.I_coil`, `coil.R0`, `winding_pack.wp_side`.
  - `winding_sum : 'Material Winding Cost'`: `inventory.sc_cost`, `inventory.materials_cost`, `material_inventory.cost_helium` (`mfe_power_core.sysml:307-323`), `winding_procurement.winding_fabrication_cost` (`:324-337`).
- **EXPOSEs (outside readers):** `conductor_supported = conductor.supported`, `conductor_status_code = conductor.status_code`, `conductor_acceptance_margin = conductor.acceptance_margin`, `conductor_T_cs = conductor.T_cs`, `conductor_operating_fraction = conductor.operating_fraction`, `superconductor_cost = inventory.sc_cost`, `element_length = inventory.element_length`, `ampere_floor_margin = pack_field.ampere_floor_margin`, `R_over_sqrt_A_wp = pack_field.R_over_sqrt_A_wp`.
- **Asserted:**
  - `acceptance_ok : 'Conductor Acceptance'` (`supported_in = conductor.supported`, `margin_in = conductor.acceptance_margin`).
  - `copper_ok : 'Protection Copper Allowance'` (`area.cu_margin`).
  - `steel_ok : 'Structural Steel Allowance'` (`area.steel_margin`).
  - `pack_area_ok : 'Winding Fit'` (`area.fit_margin`). With `available_area` = the pack's share per turn, this is exactly contract § 5's `turns × gross ≤ wp_side²·1e6`, divided by turns. Round 1's `fit_ok` is not asserted separately because it is the same inequality.
  - `ampere_floor_ok : 'Ampere Floor'` (`pack_field.ampere_floor_margin`).
- **Unsupported behaviour.** Outside its bands the Round 1 law returns `status_code 0`, `supported 0` and `acceptance_pass 0` without an exception (`magnet_conductor_alternatives.sysml:6`). `acceptance_ok` is then violated and the separate status output lets the study file the design as `unsupported`, never as pass or fail.
- Citation: Round 1 design § 2.1–2.4, § 6; contract §§ 4–7 r4; audit § 6 step 5.
- **Direct specialization only.** An intermediate common def is avoided because syside does not surface a grandparent through an intermediate def and drops its template calcs (`stellarator_plant.sysml:22-31`). The common usages are therefore written in both leaves.

### 2.6 `'Round1 REBCO Magnet System' :> 'Magnet System'`

Same structure as § 2.5, with these differences:

- The REBCO attributes (Round 1 § 6 names) are `tape_width` [m], `tape_thickness` [m], `tape_copper_fraction`, `anchor_ic` [A/tape at 20 T, 20 K], `g8`, `g10`, `g12`, `g15`, `g20`, `alpha`, `T_star` [K], `degradation`, and the bounds `B_knot_min`, `B_knot_max`, `B_law_min`, `B_law_max` [T], `T_law_min`, `T_law_max` [K]. Top-level `tape_width` and `tape_thickness` are distinct from the dormant plant `winding_pack.tape_width` (6 mm).
- A `shape_branch : 'REBCO Shape Branch'` usage (`B_peak`, `B_knot_max`) feeds `shape_mode_in` of `conductor : 'REBCO Cable Critical Surface'`. `shape_mode` is therefore calculated, not supplied (MR-7 call-out, § 4).
- REBCO status is 1 on 8–20 T (knots) and on 20–25 T (power law, `B_law_max` 25 T per contract § 4 F10). It is 0 above 25 T. Below 8 T the knot branch returns NaN outputs with status 0 (`work/active/WI-099_magnet-conductor-alternatives/implementation-notes.md:29`); the contract grid does not go there.
- The flags `extrapolated` (20–24 T), `beyond_law_extents` (24–25 T) and `above_stellaris_envelope` (> 24.9 T) are study-side labels computed from `B_peak`.

### 2.7 `'Staged Cryoplant' :> 'Cryoplant'`

- **Attributes** (no values; instance-bound):
  - Round 1 § 6 names: `load_multiplier`; NIST `k_a` … `k_i`; `eta_mode`, `eta_const`, `green_a`, `green_b`, `capital_mode`, `green_c` [USD2015], `green_d`, `T_green` [K], `usd2015_to_2021`.
  - New: `T_conduction_ref` [K] (20.0, the plant's `k_c` segment basis) and `I_joint_ref` [A] (50,000).
  - Round 1's `n_leads`, `f_lead`, `L0`, `T_shield`, `T_amb`, `f_carnot_shield` and `rating_cold` are the plant's own `n_leads`, `f_lead`, `L0`, `T_shield`, `T_amb_cryo`, `f_carnot_shield` and `rated_cold_W` (`mfe_plant_systems.sysml:467, 543-547, 564`). Round 1's `nuclear_density` and `cold_volume` are the plant-wired `q_nuc_cryo` and `vol_cold_total` (`mfe_plant.sysml:100-101`), which is the pack-volume basis of audit § 4 item 5.
- **Redefinitions:**
  - `:>> inventory_enabled = false;`, so `'Coil Thermal Inventory'` returns zeros and never evaluates outside its 10–30 K domain (`mfe_cryo_inventory.sysml:5-6`).
  - `:>> purchase_cost_per_module = refrigeration.refrigerator_capital;`, so the cryo capital is calculated from the supplied rating (MR-7 call-out). It reaches `cryo_cost` (`mfe_plant_systems.sysml:585, 646-651`) and `aux_cooling_capital` (`mfe_plant.sysml:551`).
  - The five seams of § 2.3.
- **Calc usages:**
  - `static_loads : 'Staged Static Loads'` binds `n_coils`, `c_coil`, `wp_side`, `t_case`, `shield_area_ratio`, `eps_eff`, `sigma_SB`, `q_MLI`, `g_per_coil`, `k_c`, `k_s`, `T_cold_cryo`, `T_shield`, `T_amb_cryo`, `T_conduction_ref`, `p_fixed_cryo`.
  - `cold_stage : 'Magnet Cold Stage Load'` binds `T_supply_in = T_cold_cryo`, `T_shield_in = T_shield`, `T_amb_in = T_amb_cryo`, `turn_current_in = I_turn`, `nuclear_density_in = q_nuc_cryo`, `cold_volume_in = vol_cold_total`, `radiation_ref_in = static_loads.q_radiation`, `conduction_ref_in = static_loads.conduction_ref`, `T_conduction_ref_in = T_conduction_ref`, NIST coefficients, `n_leads_in = n_leads`, `f_lead_in = f_lead`, `L0_in = L0`, `p_joint_ref_in = static_loads.p_joint_ref`, `I_joint_ref_in = I_joint_ref`, `shield_static_in = static_loads.shield_static`, `load_multiplier_in = load_multiplier`.
  - `refrigeration : 'Staged Refrigeration Screen'` binds `cold_stage.q_cold`, `T_cold_cryo`, `cold_stage.q_shield`, `T_shield`, `T_amb_cryo`, `rated_cold_W`, `eta_mode` … `usd2015_to_2021`, with `f_carnot_shield_in = f_carnot_shield`.
  - `staged_drive : 'Staged Drive Power'` binds `cold_stage.q_leads`, `cold_stage.q_shield`, `static_loads.shield_static`, `cold_stage.q_joints`, `joint_drive_fraction`.
- **EXPOSEs:** `staged_q_cold`, `staged_q_shield`, `refrigeration_eta_cold`, `refrigeration_green_extrapolated`.
- **Asserted:** `capacity_ok : 'Refrigerator Capacity'` (`refrigeration.capacity_margin`). This duplicates `cold_stage_capacity_ok` by construction (§ 7 K17).
- **Physics at the reference (20 K, 50 kA).** `q_cold` = 4,847.9 (nuclear) + 266.68 (radiation) + 590.28 (conduction) + 8,729.06 (leads) + 7,500 (joints) = 21,933.9 W, the pin's `cold_load_W_demand_conversion__demand` to rounding. `q_shield` = 41,599.95 W, the pin's intercept demand. At 4.5 K, conduction scales by the NIST integral ratio (≈ 326/307). Radiation follows the plant's area law. Joints scale with I² (Round 1 anchor D form).
- Citation: Round 1 design § 2.5–2.6; contract § 6; audit § 6 step 6.

### 2.8 How the cryo electricity reaches the power balance

`refrigeration.p_in_total_MW = (q_cold·carnot/η + q_shield·(T_amb − T_shield)/T_shield/f_carnot_shield)/1e6` feeds the `p_elec` seam. `pb.p_cryo` reads `cryoplant.p_elec` (`mfe_plant.sysml:395`; pipeline `:2119`), which enters the recirculating sum (`models/library/analyses/mfe_power_balance.sysml:159-172`), then `p_net` and the LCOE denominator. The cold stage uses Green η at the installed rating; the 77 K stage keeps the plant's 0.20 of Carnot for both materials (contract § 6). The drive follows the same path: `staged_drive.p_drive` feeds the `p_drive` seam, then `power_supplies.p_tf_extra` (`mfe_plant.sysml:192`), then `tf_power` (pipeline `:2074-2080`), then the recirculating power and `magnet_tf_electric_capacity_ok` (`stellarator_plant.sysml:2327`). The plant's own 0.20-Carnot cold chain (`cryo_elec`, `mfe_plant_systems.sysml:636-645`) and `shield_elec` (`:623-629`) still execute but are dormant: they reach no priced or checked channel.

### 2.9 Supplied count to inventory and acceptance

`n_elements` feeds `conductor.n_*_in`, which gives the cable Ic, `acceptance_margin`, `acceptance_ok`, and `reference_conductor_current_ok` (re-pointed, § 2.10 E6). It also sets `element_area_total`, which feeds `area.gross_area` and `pack_area_ok`. Separately, `n_elements` feeds `inventory.n_elements_in`, which gives `element_length` and `sc_cost`, then `winding_sum.cost`, the `winding_cost` seam, `magnet_capital_rollup` (`mfe_power_core.sysml:360-364`), `powercore_capital` (`mfe_plant.sysml:461-464`), and finally overnight capital and LCOE. The count is never resized. The plant's composition-implied count (`conductor_current.parallel_tapes_*`) reads zero in the material instances.

### 2.10 The materials design file (`stellarator_09_materials`)

`author_materials_design.py` copies `part stellaris : 'MFE Power Plant' { … }` from the staged `stellarator_plant.sysml` (`:35` to its closing brace) twice and applies:

| # | Edit | Anchor |
|---|---|---|
| E1 | rename to `part rebco_material` / `part nb3sn_material` | `:35` |
| E2 | rewrite the seven self-references `stellaris.` → `<name>.`, count asserted equal to 7, no doc text touched | `:562-568` |
| E3 | retype `part :>> magnet : 'Round1 REBCO Magnet System' {` / `'Nb3Sn Magnet System'` | `:115` |
| E4 | retype `part :>> cryoplant : 'Staged Cryoplant' {` | `:1342` |
| E5 | delete the cryoplant `purchase_cost_per_module` and `inventory_enabled` bindings, now final in the variant | `:1350-1353` |
| E6 | re-point `reference_conductor_current_ok` to `in margin_fraction_in = magnet.conductor_acceptance_margin;`, keeping 67 plant verdicts meaningful | `:2200-2202` |
| E7 | add the variant attribute bindings, citing the Round 1 values by path, e.g. Nb₃Sn law `models/designs/magnet_materials/magnet_subsystem.sysml:71-100`, bounds `:238-261`, Green and NIST `:210-235, 268-293`, REBCO `:484-521, 660-677` with `B_law_max = 25.0` per contract § 4 F10; add `T_conduction_ref = 20.0` [INHERITED: plant `k_c` basis, `stellarator_plant.sysml:1387`] and `I_joint_ref = 50000.0` [INHERITED: `:1416` with `:202`] | magnet and cryoplant blocks |
| E8 | material values: `T_cold_cryo` 20.0 / 4.5 and `rated_cryogenic_cold_K` to match; `B_max` 25.0 / 13.0; `eps_cond_allow` 0.004 / 0.003 [U]; default-design supplied quantities from `reference_designs.json` | `:1422, :1343, :436, :428` |
| E9 | package header: the nine stellarator imports (`:2-10`) plus `private import magnet_material_variants::*;` and a doc saying these are material-variant copies | file header |

Default designs `[AGENT]`:

- **REBCO.** The contract § 6 basis-bridge design: the Stellaris supplied design, construction C at 50 kA and 24.9 T, and `n_elements` equal to the composition-implied count in 4 mm units (169.06). It is expected to fail acceptance; it is a reconciliation point, not a ranked design.
- **Nb₃Sn.** The anchored-cell equal-duty 12 T design at R 12.7 m: 149 turns at 50 kA, construction P, strand count from the Round 1 offer rule, ratings from the fixed list. Its default must evaluate without refusal (§ 1.6 step 5; § 7 K22).
- `eps_intrinsic_in` is supplied by the manifest point, not by the file (K6).

## 3. Binding table (plant-side anchors)

| Quantity | Producer / supplied at | Into the WI-099 calc (material instances) | Plant-side anchor |
|---|---|---|---|
| `reference_turns` | supplied, `stellarator_plant.sysml:254` (`'Modular Coil'` `mfe_magnet_parts.sysml:22`) | `inventory.turns_in`, `adapter.reference_turns_in`; `I_coil` via `winding_state` | `mfe_power_core.sysml:187-191`; axis field `:157-162` |
| `turn_current` | supplied, `stellarator_plant.sysml:202` | `conductor.turn_current_in`, `area.turn_current_in`, `inventory.turn_current_in`; `cold_stage.turn_current_in` via `cryoplant.I_turn` | `mfe_plant.sysml:105` |
| `wp_side` | supplied, `stellarator_plant.sysml:447` | `adapter` (pack share, so `pack_area_ok`), `pack_field` (Ampère floor, R/√A_wp), peak-field slot; `static_loads` via `cryoplant.wp_side` | `mfe_plant.sysml:104`; `mfe_power_core.sysml:252-269`; fit `:211-221` |
| `coil_t` | supplied, `stellarator_plant.sysml:305` | through the radial build to `r_coil_centre`, which sets `bore_norm` and `c_coil`, which sets `adapter.turn_length` and `static_loads` | `mfe_plant.sysml:325, 134`; `mfe_power_core.sysml:245-249`; fit `:217` |
| `c_coil`, `f_set` | calculated (`mfe_power_core.sysml:113`) / supplied `stellarator_plant.sysml:231` | `adapter.turn_length = f_set·c_coil`, the plant's conductor length per turn (321,600 m total at the reference, audit § 4) | `mfe_winding_pack_cost.sysml:44` |
| `B_peak` | calculated, `mfe_power_core.sysml:123`, `:167-174` + slot | `conductor.B_peak_in`, `area.B_peak_in` (steel rule), `pack_field`, `shape_branch` | pipeline `:1961-1991, 2056` |
| `T_cold_cryo` | supplied per material, `stellarator_plant.sysml:1422` | `winding_pack.T_inventory` feeds `conductor.T_supply_in` and the plant helium (`mfe_power_core.sysml:321`); `cold_stage` and `refrigeration` `T_supply_in`; `static_loads.T_cold_in` | `mfe_plant.sysml:126` |
| `winding_cost` | seam `mfe_power_core.sysml:129` | rebound to `winding_sum.cost` | rollup `:360-364` |
| `structure_cost` | seam `:149`, unchanged, prices supplied `m_support` | — | `stellarator_plant.sysml:116`; `mfe_magnet_cost.sysml:157-178` |
| plant REBCO law | usage `mfe_power_core.sysml:192-210` | gated off (`rebco_law_enabled = 0`) | pipeline `:1974-2001` |
| `conductor_margin_fraction` | EXPOSE `:144`, unchanged | not read in material instances; E6 re-points the constraint | `stellarator_plant.sysml:2200-2202`; pipeline `:4644-4650` |
| `conductor_supported`, `conductor_status_code` | new EXPOSEs on the leaves | — | study status rule, contract § 7 |
| cold-stage demand | seam `mfe_plant_systems.sysml:485` | `cold_stage.q_cold`, screened against `rated_cold_W` (`:467`, `stellarator_plant.sysml:1346`) | pipeline `:1855-1870` |
| intercept demand and availability | seams at `:500`, `:503` | `cold_stage.q_shield`, `true`, screened against `rated_intercept_W` (`stellarator_plant.sysml:1347`) | pipeline `:1786-1793` |
| `p_elec` | seam `:586` | `refrigeration.p_in_total_MW` | `mfe_plant.sysml:395`; pipeline `:2119` |
| `p_drive` | seam `:587` | `staged_drive.p_drive` | `mfe_plant.sysml:192`; pipeline `:2074-2080` |
| cryo capital | `purchase_cost_per_module` (`mfe_plant_systems.sysml:571`) | `refrigeration.refrigerator_capital` (Green, USD2021) | `:646-651`; `mfe_plant.sysml:551, 926` |
| `q_nuc_cryo`, `vol_cold_total` | supplied `stellarator_plant.sysml:492`; calculated `mfe_power_core.sysml:127` | `cold_stage.nuclear_density_in`, `cold_volume_in` | `mfe_plant.sysml:100-101` |
| lead, radiation and support facts | supplied `stellarator_plant.sysml:1354-1416` | `static_loads`, `cold_stage`, `staged_drive` | `mfe_plant_systems.sysml:538-561` |
| densities and prices | supplied `stellarator_plant.sysml:380-400` | `inventory.rho_*`, `price_*` | contract § 6 |
| `B_max`, `eps_cond_allow` | supplied per material `stellarator_plant.sysml:436, 428` | — (plant ceiling and strain checks) | `mfe_plant.sysml:856-859, 874-875` |

## 4. MR-7 role table (material instances)

| Quantity | Role | Where | Change against the reference |
|---|---|---|---|
| turns, turn current, `wp_side`, `coil_t`, `interior_y`, R, a, `n_e0`, `T_i0` | chosen (policy) | instance | none |
| `n_elements`, construction areas, `element_price_per_m` | chosen | leaf attrs | new; replaces the composition-implied count |
| construction rule inputs, law constants and bounds, acceptance rules | held material facts / requirement rules | leaf attrs | new |
| `T_cold_cryo` (supply temperature) | chosen per material | cryoplant | value changes |
| `B_axis`, `B_peak`, `I_coil`, `R/√A_wp`, Ampère floor | calculated | plant calcs + `pack_field` | arm slot (off at 0) |
| `shape_mode` (REBCO) | **calculated** branch selector | `shape_branch` | **role change**: a Round 1 case input becomes calculated (contract § 4 piecewise law) |
| Ic, T_cs, margins, status | calculated | `conductor` | new |
| gross area, pack share, cu/steel requirements | calculated / requirement | `area`, `adapter` | new; checked by `pack_area_ok`, `copper_ok`, `steel_ok` |
| `m_support` | chosen (policy rule [U]) | `magnet` | none |
| `p_wallplug_heat` | chosen (policy rule [U]) | heating | none |
| `rated_cold_W`, `rated_intercept_W`, rated temperatures | installed capacity (chosen) | cryoplant | none |
| `q_cold`, `q_shield`, drive | calculated demand | `cold_stage`, `staged_drive` | new basis; checked by `cold_stage_capacity_ok`, `intercept_stage_capacity_ok`, `capacity_ok`, `magnet_tf_electric_capacity_ok` |
| cryo electricity | calculated (Green η at the installed rating) | `refrigeration` | new basis |
| cryo `purchase_cost_per_module` | **calculated** from the chosen rating (Green law) | variant | **call-out**: a supplied price becomes a calculated binding (contract § 6) |
| `inventory_enabled`, `rebco_law_enabled` | **final** in the variants (false, 0) | variants | **call-out**: the entry points disappear or are refused (K11) |
| plant REBCO law inputs, `tape_width` 6 mm, `tape_price_per_m`, `f_copper`/`f_solder`/`f_steel`, `f_carnot_cryo`, `p_cryo` | **dormant** | plant | **call-out**: still executed and reported, but they reach no priced or checked channel |
| `f_helium` | chosen (held 0.08 [AGENT]) | winding pack | prices plant helium only |
| package ratings, building dimensions, turbine/heat-rejection/power-supply/divertor purchase costs, 22 `*_class_MW(e)` | chosen (policy: demand × 1.05, scaling [U]) | instance | none in the model |
| `f_ren`, `beta_limit`, `peak_ratio`, `k_link`, `arm_slope`, `arm_x_ref` | held assumption axes | instance | arm new |
| `B_max` | supplied envelope, a flag not a limit | winding pack | per material |

Nothing calculated is bound back as an input. The only model-side value derived from demand is the Green capital, and it prices the chosen rating rather than sizing it. Every demand-to-capacity rule (ratings × 1.05, heating, structure mass, classes, pack side, turns) lives in the external policy script. The recorded supplied design is evaluated without the policy. MR-7 status for this scope: compliant by construction, to be confirmed by the § 6 tests.

## 5. Interface

### 5.1 Entry keys (material prefix `M = stellarator_09_materials__<rebco_material|nb3sn_material>__`)

| Contract item | Key suffix(es) after `M` |
|---|---|
| § 3.1 `f_ren`, `beta_limit` | `plasma__f_ren`, `beta_limit` |
| § 3.2 geometry | `magnet__coil__peak_ratio`, `magnet__coil__arm_slope`, `magnet__coil__arm_x_ref`, `magnet__coil__k_link` |
| § 3.2 envelope | `magnet__winding_pack__B_max` |
| § 5 turns, current | `magnet__coil__reference_turns`, `magnet__coil__turn_current` |
| § 5 size, operating point | `plasma__R`, `plasma__a`, `plasma__T_i0`, `plasma__n_e0` |
| § 5 element count, construction | `magnet__n_elements`, `magnet__{cu_space, steel_area, misc_area, solder_area, ins_fraction, cabling_factor, cable_void, J_cu_rule, cu_void, cu_per_kA_rule, steel_per_kA_rule, B_steel_ref, steel_B_scaling}` |
| § 5 pack, allocation, casing | `magnet__winding_pack__wp_side`, `magnet__coil__coil_t`, `magnet__casing__interior_y` |
| § 5 structure, heating | `magnet__m_support`, `heating__p_wallplug_heat` |
| § 5 cryo ratings | `cryoplant__rated_cold_W`, `cryoplant__rated_intercept_W`, `cryoplant__rated_cryogenic_{cold,intercept,ambient}_K`, `cryoplant__T_cold_cryo` |
| § 5 packages and occupancy | every `*__rated_*`, `*__installed_*`, `turbine__selected_gross_MWe`, `turbine__{hp,lp}_turbine__rated_*`, `turbine__{condenser,condensate_pump,feedwater_pump}__rated_*`, `turbine__{main_steam_generator,reheater}__installed_UA_MW_K`, `heat_transport__{rated_*,helium_rated_*,equipment_*_design_*,equipment_*_purchased_mass_kg,mdot_loop_rated}`, `electric_plant__installed_gross_rating_MWe`, `power_supplies__rated_{tf,pf}_MWe`, and the 82 `buildings__selected_*` keys (the families in `…/magnet-probe/baseline-inputs.json`) |
| § 5 purchase costs | `{turbine, heat_rejection, power_supplies, divertor}__purchase_cost_per_module` (the cryoplant's is calculated) |
| § 5 power classes | the 22 `*_class_MW` / `*_class_MWe` keys listed in the pin inputs |
| § 4 prices, strain | `magnet__element_price_per_m`; Nb₃Sn `magnet__conductor__eps_intrinsic_in` (**required**, K6) |
| material and cryo facts | leaf and 'Staged Cryoplant' attributes of § 2.5–2.7 (held; variants per contract § 5) |

`prepare_interface.py` derives the exact list from `stellarator_materials_tea/contracts/model_contract.json`, matches every family above, and fails closed on a key matching no family (WI-099 `prepare_interface.py` precedent).

### 5.2 Output channels the study reads (after `M`)

- **Headline:** `lcoe_calc__lcoe`.
- **Decomposition** (contract § 8 groups):
  - Conductor purchase: `magnet__inventory__sc_cost`.
  - Other winding materials and operations: `magnet__inventory__materials_cost`, `magnet__material_inventory__cost_helium`, `magnet__winding_procurement__winding_fabrication_cost`, `magnet__insulation_inventory__stock_cost`.
  - Structure: `magnet__magnet_structure_cost__cost`.
  - Refrigeration capital: `cryoplant__refrigeration__refrigerator_capital` (= `cryoplant__aux_cooling__cryo_cost`). Refrigeration electricity: `cryoplant__refrigeration__p_in_total_MW`.
  - Heating: `heating__heating_cost__cost`, `operating_heat__p_wallplug`.
  - Radial build: `{blanket,shield,structure,vessel}__*_cost__cost`.
  - Packages: `turbine__turbine_cost__cost`, `electric_plant__electric_cost__cost`, `heat_rejection__heat_rejection_cost__cost`, `power_supplies__power_supplies_cost__cost`, `divertor__divertor_cost__cost`, `cryoplant__aux_cooling__cost`.
  - Buildings: `buildings__facility_accounts__cost`.
  - Fuel and O&M: `cas71_calc__levelized`, `calendar__cas72_annual`, `cas80_calc__levelized`, `fuel_cycle__fuel_calc__annual_fuel`.
  - Capital: `magnet__magnet_capital_rollup__capital_cost`, `overnight_capital__overnight_capital`, `total_capital__total_capital`.
  - Energy: `pb__p_net`, `pb__p_et`, `pb__p_th`.
- **Plasma and field:** `plasma__fusion__p_fus`, `plasma__sustain__p_aux_required`, `plasma__beta_calc__beta`, `magnet__field_calc__B_axis`, `magnet__peak_field_calc__B_peak`, `magnet__stored_energy__W_mag` (the policy's structure-mass input), `magnet__wp_stress__sigma_wp`, `magnet__cond_strain__eps_cond`, `magnet__wp_fit__minimum_margin`.
- **Magnet:** `magnet__conductor__{T_conductor, ic_cable_op, operating_fraction, T_cs, tcs_defined, acceptance_margin, status_code, supported, acceptance_pass}`, `magnet__area__{gross_area, fit_margin, fit_margin_fraction, cu_margin, steel_margin}`, `magnet__inventory__{conductor_length, element_length}`, `magnet__pack_field__{R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin}`, `magnet__conductor_current__evaluation_defined` (0 by design).
- **Cryo:** `cryoplant__cold_stage__{q_nuclear, q_radiation, q_conduction, q_leads, q_joints, q_cold, q_shield}`, `cryoplant__refrigeration__{eta_cold, p_in_cold, p_in_shield, R_equiv_kW, capacity_margin, green_extrapolated}`, `cryoplant__{cold,intercept}_stage_capability__margin`, `cryoplant__staged_drive__p_drive`.
- **Verdicts.** Each material instance has 73: the 67 plant names of the pin (e.g. `beta_ok`, `sustainment_ok`, `burn_hold_ok`, `peak_field_ok`, `wp_fit_ok`, `tbr_ok`, `reference_conductor_current_ok`, …) plus `magnet__{acceptance_ok, copper_ok, steel_ok, pack_area_ok, ampere_floor_ok}` and `cryoplant__capacity_ok`, each with its hash suffix. The package total is 67 + 73 + 73 = 213. Statuses (contract § 7) and flags are study-side, from these channels. `peak_field_ok` is read as `envelope_flag`.

### 5.3 Route (`exploration/stellarator_materials/studies/study_route.py`)

Carried over from `exploration/stellarator_e2e/studies/study_route.py`, applied to all three prefixes:

- the retired-key refusals (`:184-189`);
- `validate_proposal`'s numeric and Boolean typing (`:181-204`);
- the stock strict loader and runner (`:207-335`).

Changed or added:

- `PACKAGE_NAME = "stellarator_materials_tea"`, a new `PACKAGE_DIR`, `MANIFEST_PATH` and three prefixes (in place of `:66-69`).
- `EXPECTED_CONSTRAINT_COUNT = 213`, with per-prefix counts 67/73/73 asserted in `_export_catalog` (in place of `:71, 348-352`).
- `BOOLEAN_KEYS` recomputed per prefix from the new contract. The material prefixes drop `cryoplant__inventory_enabled` and may gain `cryoplant__intercept_demand_available` (K10) (in place of `:124-179`).
- New refusals: any reference-prefix key (the reference is pinned); keys from both material prefixes in one proposal (one material per case); `magnet__rebco_law_enabled` or `cryoplant__inventory_enabled` under a material prefix if codegen emits them (K11); a Nb₃Sn proposal without `magnet__conductor__eps_intrinsic_in` (K6).
- The per-case reference-parity assertion (§ 1.5).
- A new `manifest.json` (package identity; per-material `lcoe` objectives; baseline point = material defaults plus `eps_intrinsic_in = -0.003`) and a new `oracle_entry.py` (§ 6.3).

## 6. Verification

### 6.1 Build- and model-level tests (`tests/models/test_stellarator_materials.py`, through the generated package via the route)

1. **Reference bit-for-bit** (§ 1.5) and protected paths unchanged (§ 1.4).
2. **Gating.** In the reference, `rebco_law_enabled = 1` is identity (covered by test 1). With `rebco_law_enabled = 0` on the reference, all 11 law outputs are 0 and `evaluation_defined` is 0, with no exception. `reference_conductor_current_ok` then reads 0 ≥ 0 and is satisfied, which documents why E6 re-points it. `enabled = 0.5` refuses.
3. **Pack-arm slot.** At `arm_slope = 0`, `B_peak` is bitwise equal to `(B_axis·peak_ratio)·bore_norm` for randomized R, `wp_side` and `arm_x_ref` ∈ {0, 35.278, 1e3}. At (0.0641, 35.278) and the reference pack, B_peak = 24.9·(1 + 0.0641·(35.2777… − 35.278)/2.7667) ≈ 24.89987 T. A larger pack (x = 30) lowers the peak, which is the sign check.
4. **Staged cryo insertion.**
   - (a) In a material instance, `pb`'s `p_cryo` operand equals `cryoplant__refrigeration__p_in_total_MW` and `tf_power` equals `p_tf + staged_drive.p_drive`, checked on both pipeline wiring and values.
   - (b) Identity under the reference selection: the REBCO-material instance at the bridge design with `eta_mode = 1`, `eta_const = 0.20` reproduces the pin's `cryo_elec__p_elec` 1.5353731658, `shield_elec__p_elec` 0.6023889434, `refrigeration_sum__total` 2.1377621092 MW, cold demand 21,933.9024 W, intercept demand 41,599.9539 W and drive 0.0502673272 MW, each to relative 1e-9.
   - (c) With the default Green η, only `p_in_cold`, `p_net` and their downstream channels move against (b).
5. **MR-7 pairs.** Each pair is one insufficient and one sufficient supplied design, with the design unchanged by evaluation:
   - acceptance: `n_elements` ⌊0.9 n⌋ against n, for Nb₃Sn at 12 T and REBCO at 24.9 T;
   - `pack_area_ok`: `wp_side` 0.999·√(turns·gross) against the policy value;
   - fit: `coil_t` and `interior_y` below and above;
   - capacity: `rated_cold_W` one list step below against at; `rated_intercept_W`; `power_supplies__rated_tf_MWe`;
   - `ampere_floor_ok`: `peak_ratio` 2.12 with R 22 m and a small pack against the reference.
   In each pair, inventory and cost must follow the supplied design only.
6. **Hardware fixed, demand varied.** `turn_current` ±10 % moves B_peak, the margins, leads and joints, but leaves `element_length`, `sc_cost`, `materials_cost`, the pack volume and the ratings unchanged.
7. **Unsupported, one per conductor, status only.** Nb₃Sn at 15 T gives `status_code 0` and `supported 0`, with `acceptance_ok` violated and no exception. REBCO at 26 T gives the same, with finite outputs. A domain refusal (`R − a_coil ≤ 0`) is recorded as a failed evaluation with its refusal text, filed `unsupported`.
8. **Anchors through the plant instances.**
   - Stellaris Table 7: the REBCO-material instance with construction C at 50 kA and 24.9 T gives `area__gross_area` = 420.779220779 mm² to relative 1e-6, equal to the pack share 0.1296e6/308.
   - EU DEMO layer 1: the Nb₃Sn-material instance with `turn_current` 104,950 A, 147 turns (so the field stays moderate), 399 strands of 1 mm, J_Cu 93.4, steel 9.3635 mm²/kA and `steel_B_scaling = 0` gives 2,577.2011 mm² to relative 1e-6 (WI-099 implementation-notes.md:21).
9. **Pack share.** `pack_area_ok`'s margin equals `(wp_side²·1e6 − turns·gross)/turns` to 1e-12 relative.
10. **Build.** Positional-binding report; fixed point; body set equals stub set; B1 and B2 whole-body diffs show only the declared statements.

### 6.2 Policy acceptance (study-owned, listed for completeness)

Contract § 5 tolerances on every recorded design: `p_fus` ± 0.5 %, `B_peak` ± 0.1 T, `p_aux_required` reproduced without the policy.

### 6.3 Oracle partition (relative 1e−9, every recorded channel of every case)

| Oracle | Author | Channels |
|---|---|---|
| Plant oracles: `exploration/stellarator_e2e/studies/oracle_entry.py` over `verify_stellaris.py` and the `oracle_*.py` family | existing | all reference-prefix channels; in material instances, every channel whose producer is an unchanged plant calc: plasma, sustainment, beta, wall, divertor, radial build, field and bore, stress and strain, fit, stored energy, conversion and heat transport, buildings, fuel cycle, the plant's own magnet sub-accounts (helium, winding operations, insulation, structure), and the dormant plant REBCO law, inventory and cold chain |
| Round 1 oracle `exploration/magnet_materials/oracle.py` | existing (WI-099) | `magnet__conductor__*`, `magnet__area__*`, `magnet__inventory__*`, `cryoplant__cold_stage__*`, `cryoplant__refrigeration__*` from the recorded calc inputs |
| New glue oracle `exploration/stellarator_materials/oracle_glue.py` | separate author, from this design and contract r4 only | `adapter`, `winding_sum`, `pack_field`, `shape_branch`, `static_loads`, `staged_drive`; the seam insertions (`p_cryo`, `p_tf_extra`, cold and intercept demands, cryo capital, `winding_cost`); `pack_area_ok`, `ampere_floor_ok`, `capacity_ok`; the peak-ratio arm; the re-pointed `reference_conductor_current_ok` operand; the structure-mass rule as a recorded-design check (`m_support = 11,615.6 t × W_mag/111 GJ` × variant) |
| Downstream aggregation in material instances (power balance, capital rollups, DCF, LCOE) | new oracle author, composing the plant oracle's function-level pieces by import with the rebound legs taken from the Round 1 and glue oracles | `pb__*`, `*_capital__*`, `cas7x/8x`, `lcoe_calc__lcoe`. The reuse boundary is recorded in `oracle-reuse.json` (WI-096 precedent). Protected oracle files are not edited, and any piece reachable only through `_compute` is re-derived and listed |

## 7. Clarifications and risks (each resolution `[AGENT]`)

- **K1, placement conflict** (§ 1.1). Option Y is proposed; the reviewer or owner confirms, or rules X. **Contract/spec dependency.**
- **K2, r4 arm parameterization.** The r4 additive form differs from spec R3 and audit step 3; the keys are `arm_slope` and `arm_x_ref`. Default `arm_x_ref` 35.278 reproduces 24.9 T to 5e-6 relative. Supplying the exact 12.7/0.35999999999999993 needs no model change. **r3→r4 dependency.**
- **K3, `ampere_floor_ok` (r4 C) only in material instances.** Adding it to the reference would change the pinned 67. **r3→r4 dependency.**
- **K4, three instances, but the reference is the staged, unchanged Stellaris file** rather than a copy inside the new file. This gives exact key identity with the pin and zero transcription. It deviates from contract § 9's wording.
- **K5, one-level specialization.** Grandparent template calcs are dropped through an intermediate def (`stellarator_plant.sysml:22-31`), so the common usages are duplicated in both leaves.
- **K6, negative literals are not entry points** (`…/WI-099…/implementation-notes.md:25`). Nb₃Sn `eps_intrinsic_in` is left unbound as the last formal. The manifest point supplies −0.003, and the route refuses a Nb₃Sn proposal without it. The fixed negative values (`eps_min`, NIST `k_a`, `k_d`, `k_g`, `k_i`) are constant channels, as intended.
- **K7, retyping a `part` instance.** The Stellaris instance is a usage, so the material instances are copies. Each copy retypes two sub-parts (magnet and cryoplant), while WI-057 Stage E proved one. **Probe P2** on a scratch tree comes before implementation.
- **K8, riskiest step: cross-part consumers of rebound seams.** `p_elec` feeds `pb.p_cryo` (`mfe_plant.sysml:395`) and `p_drive` feeds `power_supplies.p_tf_extra` (`:192`). Stage E proved only an in-definition consumer of a rebound seam. **Probe P1** checks the pipeline wiring. Fallback: route the staged electricity through the direct term `p_cryo` (`mfe_plant_systems.sysml:560, 644`) with the plant cold-chain inputs zeroed in the copy. The cost is that `direct_electric_capability` (`:510-516`) then screens the staged electricity, so its rating must be supplied.
- **K9, `default` on asserted EXPOSEs.** Avoided: E6 re-points the only asserted reader, and the `conductor_*` EXPOSEs stay `=`.
- **K10, Boolean seam** (`intercept_demand_available default inventory_enabled`, an attribute-to-attribute default). Covered by probe P1. The literal `true` rebinding may surface as a Boolean entry key, like `cold_stage_capability__demand_available_in` (`study_route.py:132`); the route then lists it.
- **K11, def-level literals in specializations** (`rebco_law_enabled = 0.0`, `inventory_enabled = false`). They may or may not be emitted as entry keys (**probe P3**). The route refuses them under material prefixes either way.
- **K12, body installation.** Six Round 1 bodies get the WI-099 typed adapter. The 51 stellarator bodies are prefix-rewritten, and the build asserts the body set equals the stub set. B1 and B2 carry whole-body diffs. The conditional glue calc is assumed auto-implemented (**probe P4**; fallback: a three-line handwritten body).
- **K13, cold-stage basis.**
  - Radiation and support conduction use the plant's formulas, and the NIST integral scales conduction to 4.5 K. Round 1's fixed anchor constants are not used, so the terms keep the geometry response.
  - `shield_static` subtracts conduction on the 20 K basis, which differs by ≤ 0.1 % of the intercept load at 4.5 K.
  - Joints scale with I² (Round 1 form). At 20 K the whole set reproduces the pin's inventory to rounding.
- **K14, money year.** Refrigerator capital is USD2021 inside the mixed-year plant, like the conductor prices. **Contract dependency:** contract § 6's CPI post-processing variant should cover it too.
- **K15, `pack_area_ok` at the Stellaris pack.** Under construction C it sits at its boundary by calibration, so the basis bridge reports the margin, not the verdict. When √(turns·gross) lands exactly on a 5 mm step, the policy takes the next step.
- **K16, cold capacity at the bridge.** The plant rating was captured at zero margin, and the staged `q_cold` equals it only to rounding, so the verdict is ulp-sensitive. The bridge reports the margin. Ranked designs use list ratings.
- **K17, `capacity_ok` duplicates `cold_stage_capacity_ok`.** Both are kept for contract § 7 fidelity, and the failure reasons name both.
- **K18, Round 1 `fit_ok` not asserted.** `pack_area_ok` is the same inequality at the pack share.
- **K19, REBCO `shape_mode` calculated** (§ 4 call-out). Below 8 T the knot branch returns NaN with status 0, and the grid avoids it. **K20:** NaN operands can make `reference_conductor_current_ok` indeterminate; those cases are already `unsupported`.
- **K21, cost and coupling of three instances per evaluation.** Every case evaluates three plants, and any instance's refusal fails the case (defaults must evaluate, § 1.6). **Probe P5** measures the per-case time. Fallback: split into per-instance packages from the same staged tree, which changes only the build and route, not the model.
- **K22, Nb₃Sn default design.** It sits at about 4.3 T axis with the Stellaris plasma, where sustainment convergence is not established. The build executes the defaults. If they refuse, the defaults become the first policy-recorded Nb₃Sn design that evaluates.
- **K23, dormant plant channels stay in the outputs** (plant REBCO law zeros, composition-implied tape metres and tape cost, plant cold chain, inventory zeros). The study reads the variant channels, and the dormant set is listed in the route.
- **K24, helium.** The plant keeps its ideal-gas basis at 4.5 K, roughly 15 % high (contract § 6 N3), and `f_helium` is held at 0.08 for both materials. It is a sub-M$ account and is disclosed.
- **K25, refusals are not status outputs.** `R − a_coil ≤ 0` and sustainment non-convergence raise, so the route records them as `unsupported (domain refusal)` with the text (contract § 7 item 1).
- **K26, spec wording.** Spec R3 (names) and R5 (the phrase "shared-library edits") should be amended to r4 and to option Y once ruled; the spec is not edited here.

Probes P1–P5 run on scratch copies with results deposited under `work/active/WI-100_stellarator-material-variants/prototype/` before implementation (WI-057 prototype discipline). A probe refusal that the stated fallback cannot absorb stops implementation and returns to the reviewer.
