# WI-100 design review (T-013)

Reviewer: fresh T-013 design reviewer (Opus 5.5), brief `evidence/briefs/t013-design-review.md`. Date 2026-09-30. Subject: `work/active/WI-100_stellarator-material-variants/design.md` against contract `evidence/plant-contract.md` **r4** (released), spec `spec.md` R1–R7 (R3 and R5 as amended), audit `evidence/plant-chain-audit.md` §§ 2, 4, 6, Round 1's library and WI-099 design. Placement is reviewed against the coordinator's ruling (trail.md § T-013 design draft; spec R5): every seam edit lives in the derived package's staged copies as a recorded hunk set, and canonical, twin and Stellaris design file stay byte-identical. Nothing but this file was written. Python ran only as `.codex-test/run python`.

## Verdict: PASS WITH CORRECTIONS

0 blocking, 9 corrections, 10 notes.

The architecture holds. The staged-hunk placement is sound, every hunk is value-neutral at the reference, and the regression is specified exactly. The retype mechanism already has a working precedent inside the pinned Stellaris instance. The physics matches contract §§ 3–6. Every cited plant binding exists as described. No binding creates a cycle, binds an output back as an input, or sizes a supplied quantity from demand.

The corrections are about four things:

- one unproven seam read (D1);
- a cost decomposition that double-counts and does not close (D2);
- gaps in the oracle and interface partitions (D3–D5);
- test-plan defects: one wrong anchor, a route conflict, and a missing copy-fidelity test (D7–D9).

None needs a contract change. Each can be fixed in the design text before implementation. The coordinator may apply them without a re-review. The one exception is D1: if probe P1 refuses and no fallback works, implementation stops, as the design already provides at `design.md:410`.

## What I verified directly

- **Twin equality.** The twin equals canonical for all 42 files under `exploration/stellarator_e2e/models/`, 40 SysML and 2 data (byte compare). The twin rule and census pins are as § 1.1 states (`tests/models/test_model_family_spines.py:292-304, 381-392`; `tests/model_families.py:57-103`).
- **Pin reproduces the design's numbers.** From `WI-080 …/integration/baseline.json`:
  - cold demand 21,933.902 W, intercept demand 41,599.954 W, drive 0.0502673 MW;
  - cold-stage terms: radiation 266.681 W, support 590.279 W, leads 8,729.062 W;
  - `cryo_elec` 1.5353732 MW, `shield_elec` 0.6023889 MW, sum 2.1377621 MW;
  - `B_peak` 24.899999999999995 T, `I_coil` 15.4 MA, `vol_cold_total` 136.56 m³.
  - My hand evaluation of `'Staged Static Loads'` reproduces 266.68 W, 590.28 W and 7,561.7 W.
- **Pin interface counts.** 1,352 outputs are all 1,213 float plus 139 Boolean channels of `model_contract.json`. There are 67 verdicts (42 in `stellarator_plant.sysml` plus 25 in `mfe_plant.sysml`). The 704 entry keys contain 82 `buildings__selected_*`, 22 `*_class_MW(e)` and 5 `purchase_cost_per_module` keys.
- **Default seams are not entry keys.** `winding_cost` and `p_elec` are absent from `model_contract.json` parameters. So the H5 promotions add no entry key. The declared delta (three keys, one output) is consistent.
- **Cited pipeline wiring.** Every cited pipeline line holds: `:1786-1793`, `:1855-1870`, `:1961-1995`, `:2056`, `:2074-2080`, `:2119`, `:4644-4650`. `B_peak` has exactly three consumers: the conductor law, stress, and `peak_field_ok` (`:1991, 2056, 4604`).
- **Hunk anchors.** Every anchor in the hunk table (H1–H5) and edit table (E1–E9) matches the current line. Examples: `mfe_power_core.sysml:108, 129, 173, 209, 361`; `mfe_plant_systems.sysml:485, 500, 503, 538, 571, 586, 587`; `mfe_plasma_scaling.sysml:486`; `mfe_magnet_parts.sysml:50`; `stellarator_plant.sysml:115, 1342, 1350-1353, 1387, 1416, 1422, 2200-2202`.
- **H4 is bit-neutral.** `peak_ratio + 0.0·(x − x0)` equals `peak_ratio` for finite x, whatever the sign of zero, and the `(B_axis·ratio)·bore_norm` order is kept.
- **B1 is safe at `enabled = 1`.** The existing positivity loop (`rebco_conductor_current_impl.py:15-21`) accepts `enabled = 1`.
- **H5 follows an existing pattern.** An EXPOSE read inside its own definition (`mfe_plant_systems.sysml:485, 488`) already works in the pin.
- **Coil Thermal Inventory disables cleanly.** With `inventory_enabled = false` it returns zeros before its 10–30 K guard (`coil_thermal_inventory_impl.py:10-11, 20-21`).
- **Other readers of `T_cold_cryo` are safe at 4.5 K.** They are the conditions screen, the 0.20-Carnot chain and the helium inventory (pipeline `:190, 1836, 1892`).
- **Positional binding counts.** The binding lists match their definitions: Nb₃Sn law 26 of 27 formals (last left unbound), area screen 18, cold-stage load 25, refrigeration screen 16.

## Findings

### D1 — correction — the variant rebinding of `winding_cost` is unproven (checks C, E)

- **Design text.** § 2.5: "`:>> winding_cost = winding_sum.cost;` (the WI-057 seam, `mfe_power_core.sysml:129`)". K8 and probe P1 cover only `p_elec` and `p_drive`.
- **Conflict.** The rollup reads this seam owner-qualified: `in winding_cost = 'Magnet System'::winding_cost;` (`mfe_power_core.sysml:361`). WI-057 introduced that form at implementation (`WI-057 …/design.md:106` item 2). WI-057's only executed swap rebound `structure_cost`, which the rollup reads bare (`WI-057 …/prototype/swap/ni_hts_magnet_system_variant.sysml:12`). No variant in the repository has ever rebound `winding_cost`.
- **Risk.** If codegen resolves the qualified name to the base default, magnet capital would silently keep the plant's 6 mm tape cost. The glue oracle would catch this only after implementation.
- **Fix.**
  - Add this read to probe P1 and to test 4(a): the pipeline input `magnet_capital_rollup.winding_cost` must read `winding_sum` in material instances and `winding_procurement__cost` in the reference.
  - State a fallback: a staged hunk that re-points `:361` to a new neutral `default` attribute with a name different from the formal, so it can be read bare.
  - The owner-qualified `'Cryoplant'::inventory_enabled` reads (`mfe_plant_systems.sysml:589, 624`) give false under either resolution. Record that they need no fallback.

### D2 — correction — the § 5.2 decomposition double-counts cryo capital and does not close (check A, contract § 8)

- **Design text.** "Refrigeration capital: `cryoplant__refrigeration__refrigerator_capital` (= `cryoplant__aux_cooling__cryo_cost`)" and, separately under Packages, "`cryoplant__aux_cooling__cost`".
- **Conflict 1: double count.** `cost = aux_cost + cryo_cost` (`mfe_account_costs.sysml:35-36`). In the pin, 35.116 M$ = 3.638 + 31.479. The cryo capital is counted twice.
- **Conflict 2: the groups do not close.** They omit capital, tail and annual accounts that the LCOE contains (all exist in `model_contract.json` outputs):
  - heat transport and plant: `heat_transport__coolant__cost`, `heat_transport__cooling_selection__cost`, `misc_plant__misc_cost__cost`;
  - fuel cycle: `fuel_cycle__fuel_handling__cost`, `fuel_cycle__processing_cost__cost`;
  - CAS22 tail: `remote_handling__cost`, `waste__cost`, `other_rpe__cost`, `inc_cost__cost`;
  - multipliers and owner accounts: `installation__cost`, `contingency__cost`, `indirect__cost`, `supplementary__cost`, `owner__cost`, `precon_cost__cost`, `facility_preconstruction__cost`, `idc__cost`, `special_materials_capital__special_materials_capital`;
  - annual: `cooling_annual__cas72_total`, `cas70_calc__annual_total`.
  - The LCOE denominator factor `calendar__availability` is also missing. It moves with wall load, so with R and `p_fus`.
- **Fix.**
  - Put `cryoplant__aux_cooling__aux_cost` in Packages.
  - Add the missing channels.
  - Add a closure test: the groups plus the multiplier accounts reproduce `overnight_capital`, `total_capital` and `lcoe_calc__lcoe` at 1e−9.

### D3 — correction — the oracle partition double-assigns the armed peak field and cannot reproduce the gated law (check F, R7)

- **Design text.** § 6.3 gives the plant oracle "every channel whose producer is an unchanged plant calc: … field and bore, stress and strain … and the dormant plant REBCO law". It gives the glue oracle "the peak-ratio arm".
- **Conflict: the peak field.** `'Conductor Peak Field'` is changed (H4, B2), so it is not an unchanged plant calc. Stress, the conductor laws and `peak_field_ok` all read its output (pipeline `:1991, 2056, 4604`). On arm cells, a plant oracle computing its own `B_peak` disagrees with the package.
- **Conflict: the gated law.** In material instances the plant REBCO law outputs gated zeros with `evaluation_defined = 0`. The plant oracle computes the ungated law, which refuses at 4.5 K (`rebco_conductor_current_impl.py:25-28`).
- **Fix.**
  - Assign `magnet__peak_field_calc__B_peak` to the glue oracle in material instances.
  - Every consumer of `B_peak` (stress, strain, both Round 1 laws, the area steel rule, `pack_field`, `peak_field_ok`) takes the glue's `B_peak` leg.
  - Assign the gated `conductor_current__*` channels (zeros, `evaluation_defined = 0`) to the glue oracle.
  - Write the explicit channel-to-oracle list into `oracle-reuse.json`. That includes the non-selected instance of D4.

### D4 — correction — the non-selected material instance has no defined inputs (checks E, F)

- **Design text.** § 1.5: "The reference instance runs in every case". K21: "Every case evaluates three plants, and any instance's refusal fails the case". § 5.3 refuses "keys from both material prefixes in one proposal".
- **Conflict.** Nothing fixes what the non-selected material instance receives. At package defaults, the Nb₃Sn instance evaluates with `eps_intrinsic_in = 0.0` (WI-099 `implementation-notes.md:25`: "Do not evaluate the package on its generated default inputs"). So every REBCO record carries a mis-strained Nb₃Sn plant. A refusal of the Nb₃Sn default (K22) would also fail every REBCO case.
- **Fix.** On every case the route fills the non-selected prefix from the manifest baseline point, including `eps_intrinsic_in = −0.003`. It asserts that prefix's outputs equal the recorded baseline, as a second witness. The oracle partition covers or explicitly excludes those channels.

### D5 — correction — the interface's fail-closed rule cannot pass as written (checks A, E)

- **Design text.** § 5.1: "`prepare_interface.py` … matches every family above, and fails closed on a key matching no family".
- **Conflict 1.** Each material prefix carries the copied instance's full set of pin keys. Of the 704, 47 are `library_default` and 55 are `usage_literal` (`model_contract.json`). Most are held keys that no family in the table matches, for example `plasma__kappa`.
- **Conflict 2.** `pack_field` binds 4 of the 5 formals of `'Pack Field Checks'` (§ 2.5). The unbound trailing `mu0_in` becomes a calc-usage entry key (`exploration/magnet_materials/build.py:58-59`).
- **Fix.** Define the complete key partition:
  - the varied families of the table;
  - the held pin suffixes (704 minus the varied);
  - the new variant and Staged Cryoplant attributes;
  - the named calc-usage keys (`conductor__eps_intrinsic_in`, and `pack_field__mu0_in` unless μ0 is bound).
  - The route fails closed on any key outside that partition.

### D6 — correction — H3 puts a Stellaris anchor into a library default (check D; MR-3, R6)

- **Design text.** H3: "`attribute arm_x_ref : Real default 35.278;`" on `'Modular Coil'`.
- **Conflict.** `'Modular Coil'` is library structure (`mfe_magnet_parts.sysml`). 35.278 is the Stellaris re-anchoring point (contract § 3.2). § 1.2 itself promises "library defaults neutral (MR-3)". These hunks are meant to be ported to canonical later (spec R5).
- **Fix.** Use `default 0.0`. At slope 0 any finite value is an identity (§ 2.2). Bind 35.278 in both material instances (E7), citing contract § 3.2 r4 and `check-field-relations.md` § Relation 2. The reference entry-key delta becomes `arm_x_ref: 0.0`.

### D7 — correction — the test 8 Nb₃Sn anchor runs at about 24.9 T, not a moderate field (check F)

- **Design text.** Test 8: "turn_current 104,950 A, 147 turns (so the field stays moderate)".
- **Conflict.** 147 × 104,950 A = 15.43 MA, which is the reference's 15.4 MA. So `B_peak` ≈ 24.9 T at the reference geometry.
  - That is above the Nb₃Sn law's `B_law_max` of 14.5 T (`magnet_subsystem.sysml:241`).
  - It is also above Bc2* at 5.2 K. Round 1's body then returns Ic = 0 and `operating_fraction` = +inf (WI-099 `implementation-notes.md:31`). The case records nonfinite channels.
- **Fix.** Use about 70 turns (about 11.9 T). Otherwise, state the field and assert that all recorded outputs are finite. The area result does not depend on B, because `steel_B_scaling` is 0.

### D8 — correction — tests 2 and 3 cannot run through the route (check F)

- **Design text.** § 6.1 says the tests run "through the generated package via the route". Test 2 sets "`rebco_law_enabled = 0` on the reference".
- **Conflict.** § 5.3 refuses "any reference-prefix key". Material instances fix `rebco_law_enabled` at 0 as final, so they cannot host test 2 either.
- **Fix.** Name the evaluator for tests 2 and 3. Either use the package's prepared evaluator directly (the route's strict loader without `validate_proposal`), or add a test-only flag that the route refuses in production.

### D9 — correction — no test proves the two copied instances are faithful (checks B, F)

- **Design text.** E1–E9 derive two copies of about 2,400 lines each. The drift check (§ 1.2) proves only reproducibility. Test 4(b) says the bridge instance "reproduces the pin's `cryo_elec__p_elec` …, `shield_elec__p_elec` …, `refrigeration_sum__total`".
- **Conflict 1.** A copy defect outside the edited rows would pass every listed test.
- **Conflict 2.** In material instances the named pin channels are the dormant plant chain. With inventory disabled, those channels differ from the pin.
- **Fix.**
  - Add a bridge-parity test. At the bridge design with `eta_mode = 1` and `eta_const = 0.20`, every REBCO-material channel outside a declared changed set must equal the reference channel with the same suffix, bit for bit. The changed set is: conductor, inventory and winding cost; cryo loads, electricity and capital; their rollups, `p_net` and LCOE.
  - Write test 4(b)'s channel map explicitly:

| Material-instance channel | Pin channel |
|---|---|
| `refrigeration__p_in_cold` | `cryo_elec__p_elec` |
| `refrigeration__p_in_shield` | `shield_elec__p_elec` |
| `refrigeration__p_in_total_MW` | `refrigeration_sum__total` |
| `cold_stage__q_cold` | `cold_load_W_demand_conversion__demand` |
| `cold_stage__q_shield` | `inventory__q_inventory_shield` |
| `staged_drive__p_drive` | `inventory__p_drive` |

### D10 — note — the retype has a stronger precedent than K7 and K8 state (check E)

- **Design text.** K7: "WI-057 Stage E proved one". K8: "Stage E proved only an in-definition consumer of a rebound seam".
- **Evidence.**
  - The pinned instance already retypes a sub-part: `part :>> blanket : 'Transport Calculated Blanket'` (`stellarator_plant.sysml:560`).
  - That variant rebinds `tbr` (`mfe_subsystems.sysml:131`).
  - A consumer in the plant definition (`fuel_cycle.tbr = blanket.tbr`, `mfe_plant.sysml:114`) resolves to the variant's producer (`pipeline.yaml:2341`).
- **What stays open.** The base default there is a literal, not an expression, so P1 and P2 still run.
- **The K8 fallback is under-specified.**
  - "Plant cold-chain inputs zeroed" would zero `q_nuc_cryo`, which the staged load also reads. `f_uplift_cryo = 0` zeros the dormant chain without touching the staged load.
  - No fallback is given for `p_drive`.

### D11 — note — E2's pattern must use a word boundary

The copied range contains "run_stellaris.py" (`stellarator_plant.sysml:75`). A plain replace of `stellaris.` finds 8 matches, not 7. Specify `(?<![\w])stellaris\.` so that "count asserted equal to 7" holds.

### D12 — note — the bridge count uses the reference-coil tape count, not the purchased count

- 169.06 = 1.5 × `parallel_tapes_reference` (112.709).
- The plant's tape metres correspond to `parallel_tapes_set` (113.739, or 170.61 in 4 mm units).
- So the bridge's conductor metres are f_set/f_wp_vol = 0.991 of the plant's.
- The bridge (contract § 6) should report that 0.9 % as a quantity-basis difference, not as a price effect.

### D13 — note — the stated binding rule and the bindings disagree

- **Design text.** § 2.5 says "Calc inputs read producing calc outputs directly (WI-057 D4); EXPOSEs are only for outside readers". Yet `conductor`, `area`, `pack_field` and `shape_branch` bind `B_peak_in = B_peak`, which is the EXPOSE (`mfe_power_core.sysml:123`).
- **Precedent.** The existing law reads it owner-qualified (`:193`). Stress reads the calc output (`:266`).
- **Fix.** Use `peak_field_calc.B_peak` throughout, per the stated rule.

### D14 — note — keep brackets out of docs on glue-calc operands

- **Evidence.** A bracketed token in a formula operand's doc caused `SI_RENDERING_COLLISION` (WI-099 `implementation-notes.md:27`).
- **Where it applies.** E7 and E8 plan `[INHERITED: …]` and `[U]` in the docs of `T_conduction_ref`, `I_joint_ref` and `eps_cond_allow`. The first two feed auto-implemented glue calcs.
- **Fix.** Write the basis in words on those docs.

### D15 — note — expect P4's handwritten fallback

- The library's codegen-envelope comment lists "no exp/if/lookup" (`mfe_account_costs.sysml:58-59`).
- No SysML file under `models/` or any staged `input_models/` uses an `if` expression.
- So `'REBCO Shape Branch'` will probably need the three-line body. Include it in the body-set assertion (§ 1.6 step 4).

### D16 — note — cheap tests to add

- REBCO band edges:
  - shape switch continuity at 20.0 T and 20.01 T;
  - status 1 at 25.0 T and status 0 at 25.01 T.
- Copper and steel insufficient/sufficient pairs. Both constraints are asserted (§ 2.5).
- Nb₃Sn strain separation. `eps_cond_allow` moves only `cond_strain_ok`. `eps_intrinsic_in` moves only the law.
- `peak_field_ok` read as `envelope_flag` on a 13.08 T Nb₃Sn case.
- The Ampère-floor pair should vary `wp_side` on one design rather than compare against the reference. At `peak_ratio` 2.12 and R 22 m, the floor binds below roughly 0.48 m.

### D17 — note — the intercept rating is uncosted in material instances

The Green law prices only the cold rating (`magnet_conductor_alternatives.sysml:204`). So `rated_intercept_W` carries no cost response. Contract § 5 requires a `free_capacity` flag naming such a quantity. Add it to § 4 and § 5.2 so the policy sets it.

### D18 — note — name the channels the policy reads back

§ 5.2 omits the demand operands the § 5 re-supply rules read:

- each WI-080 screen's demand and margin;
- the facility geometry, occupancy and parcel operands;
- installed coupled heating, `heating__heat__p_coupled`.

All outputs are recorded anyway. Naming them lets the policy acceptance test check them.

### D19 — note — records for the coordinator

- `spec.md:14` still reads "Governing contract … (r2, under recheck)".
- Contract § 9 still says "per the audit's seam proposal" and "a design file with three instances". Under the ruling, the reference is the staged Stellaris file and the hunks live in staged copies (K1, K4).
- One line in each document closes this.

## Check-by-check summary

- **A. Contract fidelity.**
  - Complete for entry keys, apart from D5:
    - every § 5 policy input has an entry-key family;
    - every § 3 axis has a key (`plasma__f_ren`, `beta_limit`, `magnet__coil__peak_ratio`, `magnet__coil__k_link`, `magnet__coil__arm_slope`, `magnet__coil__arm_x_ref`, `magnet__winding_pack__B_max` per material);
    - the cryoplant purchase cost is correctly calculated rather than keyed.
  - Every § 7 status and flag can be derived from exposed channels (`status_code`, `supported`, `B_peak`, `R_over_sqrt_A_wp`, `ampere_floor_margin`, `green_extrapolated`, `beta`, `p_aux_required`) or set by the policy.
  - The § 8 decomposition needs D2. D17 and D18 are policy-facing.
- **B. Preservation.**
  - H1–H5, B1 and B2 are value-neutral as argued.
  - The regression is exact: the WI-080 pin at 83ea3b6c, 1,352 outputs, 67 verdicts, a declared delta, and the headline recomputed from 67.
  - It reuses the WI-098 `parity` dictionary correctly.
  - The protected paths are hash-checked.
  - See D6, D8 and D9.
- **C. Bindings.** Every cited binding holds (see "What I verified"). Every flow exists as the design states:
  - `cryoplant.p_elec → pb.p_cryo` (`mfe_plant.sysml:395`) → the recirculating sum (`mfe_power_balance.sysml:159-161`);
  - `cryoplant.p_drive → power_supplies.p_tf_extra` (`mfe_plant.sysml:192`);
  - `T_inventory = T_cold_cryo` (`mfe_plant.sysml:126`);
  - `coil_t → rb → r_coil_centre → c_coil` (`mfe_plant.sysml:325, 134`; `mfe_power_core.sysml:245-249`).
  - There is no cycle, no output-to-input binding and no demand sizing. `purchase_cost_per_module` prices the supplied rating and is called out.
  - See D1 and D13.
- **D. Semantics.**
  - The definitions are consistent with contract § 4 and Round 1.
  - REBCO carries the 20–24 T `extrapolated` band and the 24–25 T `beyond_law_extents` band as study labels over status 1. This comes from `B_law_max` 25 and the calculated `shape_mode`, which is continuous at 20 T because g20 = 1.0 (`magnet_subsystem.sysml:511`).
  - Nb₃Sn keeps the strain screen (`eps_cond_allow` 0.003, `cond_strain_ok`) separate from `eps_intrinsic_in`.
  - See D6, D7, D14 and D15.
- **E. Toolchain.**
  - Retyping in a copied instance is expressible (D10).
  - No asserted EXPOSE is promoted (K9).
  - The design states the new manifest, the constraint count 213 and the per-prefix 67/73/73 counts.
  - Negative literals are handled (K6).
  - See D1, D4, D5 and D15.
- **F. Verification.**
  - Tests exist for: reference bit-for-bit, gating, the arm, staged-cryo identity, MR-7 pairs, hardware held with demand varied, unsupported per conductor, the two anchors, pack share, and the build checks.
  - See D3, D7, D8, D9 and D16.

## Rulings on the design's clarifications (check G)

| # | Ruling |
|---|---|
| K1 | Accept option Y. It is settled by the coordinator's ruling and spec R5. Record it in contract § 9 (D19). |
| K2 | Accept. Change the `arm_x_ref` library default per D6. |
| K3 | Accept. `ampere_floor_ok` appears only in material instances, so the pinned 67 are kept. |
| K4 | Accept. Coordinator records the § 9 wording deviation (D19). |
| K5 | Accept. The Transport Calculated Blanket (TCB) is the same one-level pattern and keeps its base calcs (`blanket__blanket_cost__cost` is in the pin). |
| K6 | Accept. Also apply D4. |
| K7 | Accept with the precedent in D10. P2 still runs. |
| K8 | Accept P1, extended by D1. Specify the fallback per D10. |
| K9 | Accept. |
| K10 | Accept. Covered by P1. |
| K11 | Accept. |
| K12 | Accept. See D15. |
| K13 | Accept. I checked the ≤ 0.1 % intercept effect: about 36 W of 41.6 kW. |
| K14 | Accept. Already applied as the contract § 6 r4a note. |
| K15 | Accept. |
| K16 | Accept. |
| K17 | Accept. |
| K18 | Accept. |
| K19 | Accept. |
| K20 | Accept. |
| K21 | Accept with D4. Probe P5 stands. |
| K22 | Accept. If the default refuses, record the sequencing: build with the policy supplying every Nb₃Sn key, then regenerate the defaults. |
| K23 | Accept. |
| K24 | Accept. |
| K25 | Accept. |
| K26 | Resolved. Spec R3 and R5 are already amended. D19 covers the stale header. |

## MR-7

Compliant as designed for this scope:

- supplied quantities stay supplied;
- demand, requirements and the Green capital are calculated from the supplied design and ratings;
- role changes are called out: the cryo price becomes calculated, `shape_mode` becomes calculated, two switches become final, and the dormant channels are listed;
- unsupported conductor status stays a status output.

Execution is unverified until tests 5–7, D1's wiring check and D9's parity test pass.

## Recheck — 2026-09-30

Scope: only the text the design author changed for D1–D18 (tagged in place, listed in design § 8), plus the D19 records. D19 is closed: `spec.md:14` reads r4, and contract § 9 records the staged-hunk placement. Nothing but this section was written.

### Verdict: PASS WITH CORRECTIONS

All 18 findings are resolved, and the new text is correct with one exception: the K8 fallbacks that D10 rewrote. Neither fallback can be expressed as written (R1, R2). They apply only if probe P1 fails, and a precedent makes that unlikely (R3). The coordinator can fix both lines without a further review. Implementation may start.

### Finding by finding

| # | Status | Is the new text correct? |
|---|---|---|
| D1 | Resolved | Yes. H6 edits the staged definition itself, not a variant override, so it breaks no finality rule. It adds `winding_account default winding_procurement.cost` and re-points `:361` to a bare read. A bare read of a `default` seam is the form Stage E proved for `structure_cost` (`mfe_power_core.sysml:362`). Both `winding_account` and `winding_cost` are `default`, so the variants may rebind both. H6 is neutral at the reference because it reads the same producer. The note on `'Cryoplant'::inventory_enabled` is right: false under either resolution. |
| D2 | Resolved | Yes, and it closes. `aux_cost` replaces `aux_cooling__cost`, which removes the double count (`mfe_account_costs.sysml:35-36`). See the anchor list below. |
| D3 | Resolved | Yes. Ownership of the arm-modified `B_peak`, its non-Round-1 readers and the gated law moves to the glue oracle, and the Round 1 oracle takes the glue's `B_peak` leg. Two owners are still unnamed (R4). |
| D4 | Resolved | Yes. The route fills the unselected prefix from the manifest baseline point, including `eps_intrinsic_in = −0.003`. It checks that prefix bit for bit against the record written by build step 5 (test 12), and the oracle table has an exclusion row for it. K22's sequencing is sound. |
| D5 | Resolved | Yes. The complete partition has these classes: varied; held pin suffixes; removed; new variant attributes; named calc-usage keys including `mu0_in`; reference. Small gaps remain (R5). |
| D6 | Resolved | Yes. H3 defaults `arm_x_ref` to 0.0, E7 binds 35.278 on the coil, and the delta is `{…, arm_x_ref: 0.0}`. |
| D7 | Resolved | Yes. 70 × 104,950 A = 7.35 MA, which gives about 11.9 T, inside the law. The test now asserts finite outputs. |
| D8 | Resolved | Yes. Tests 2 and 3 run on the direct evaluator, and the route has no bypass. |
| D9 | Resolved | Yes. The channel map is right, and test 4(b) excludes the dormant channels. Test 4(d)'s changed set is a hand list (R6). |
| D10 | Partly resolved | The precedent and the `f_uplift_cryo = 0` fix are right. Both fallbacks are wrong as written (R1, R2). |
| D11 | Resolved | Yes. |
| D12 | Resolved | Yes. |
| D13 | Resolved | Yes. Every `B_peak_in` binds `peak_field_calc.B_peak` (§§ 2.5, 2.6, 3). |
| D14 | Resolved | Yes. |
| D15 | Resolved | Yes. |
| D16 | Resolved | Yes. The step from 20.0 to 20.01 T changes `ic_cable_op` by about 3e−4, under the 1e−3 bound. |
| D17 | Resolved | Yes. |
| D18 | Resolved | Yes. All named channels exist, and there are exactly 32 `*_capability__margin` channels. |

**D2 anchors, verified against `mfe_plant.sysml` unless named.** The breakdown's listed accounts, with the rollup identities, reproduce `total_capital` with each account counted once:

- `bop_capital`: `:467`.
- `coolant_capital`: `:550`. It equals `cooling_selection.cost` (`mfe_plant_systems.sysml:302`).
- `fuel_handling_cost`: equals `processing_cost.cost` (`mfe_plant_systems.sysml:728`).
- `cas22_capital`: `:561`.
- `cas2x_pre_contingency`: `:572-574`, including `cas28_capital`.
- `cas20_capital`: `:586`.
- `overnight_capital`: `:669`.
- `idc_capital`: `:681`. Reported only; it is not part of `total_capital`.
- `total_capital`: `:688`.
- `annual_om`: equals `cas70_calc.annual_total` (`:789`).
- `lcoe_calc`: `:799-807`.
- `buildings.capital_cost`: equals `facility_accounts.cost` (`mfe_subsystems.sysml:2670`).
- Every channel named in the breakdown exists in `model_contract.json`.
- Test 13 fails on any residual or on an unlisted account.

### New findings

- **R1 — correction — the K8 `p_drive` fallback cannot be expressed.**
  - **Design text.** "in the copy, redefine `power_supplies.p_tf_extra` to read the staged calc output `cryoplant.staged_drive.p_drive` directly".
  - **Why it fails.** The `'MFE Power Plant'` definition binds `p_tf_extra` with `=` (`mfe_plant.sysml:192`). A binding feature value cannot be overridden (`WI-057 …/prototype/redefinition_probe/README.md`, variants a, c and d: "feature-value-overriding").
  - **Fix.** In the copy, replace the instance's literal `:>> p_tf = 0.0` (`stellarator_plant.sysml:732`) with `:>> p_tf = cryoplant.staged_drive.p_drive;`. The definition declares `p_tf` with no default (`mfe_subsystems.sysml:280`). `tf_power` sums `p_tf + p_tf_extra` (pipeline `:2074-2080`), and `p_tf_extra` then reads the disabled inventory's 0.
  - Record in § 4 that `p_tf` becomes a calculated binding in material instances.
- **R2 — correction — the K8 `p_elec` fallback must remove the copy's `p_cryo` literal.**
  - **Why.** The copy keeps `:>> p_cryo = 0.0` (`stellarator_plant.sysml:1403`). A final rebinding of `p_cryo` in the variant would conflict with that instance binding.
  - **Fix.** Either delete the literal in the copy, as E5 does for two other bindings, or bind `p_cryo` to the staged electricity inside the copy's cryoplant block rather than in the variant.
- **R3 — note — P1 has a closer precedent.** The redefinition probe's variant e shows a plant-definition consumer reading `magnet.cost` that follows a variant's rebinding of a `default <calc output>` seam (`…/redefinition_probe/README.md` row e; `variant_e_wiring.txt`). That is exactly the shape of the `p_elec` and `p_drive` reads, so P1 is expected to pass without the fallbacks.
- **R4 — note — two more owners to name (D3).**
  - The verdicts `wp_stress_ok` and `cond_strain_ok` read the glue's `B_peak` leg through `sigma_wp` and `eps_cond`. Name them in the glue oracle's list.
  - Assign the reference prefix's new output `magnet__conductor_current__evaluation_defined` (1.0) explicitly. The plant oracle, which owns "all reference-prefix channels", does not produce it.
  - The build's completeness check would catch both; naming them avoids a failed first build.
- **R5 — note — keep the partition closed (D5).**
  - Name `magnet__rebco_law_enabled` in the Removed class, next to `inventory_enabled` (K11).
  - Name `cryoplant__intercept_demand_available` (K10) in a class.
  - Replace "plus any other unbound trailing formal that the … report lists" with an equality: the report must list exactly the two named keys, or the build fails.
- **R6 — note — define test 4(d)'s changed set from the pipeline (D9).** Take it as the descendants, in the generated pipeline graph, of the edited producers: the seams, the variant calcs, the gated law and the cryo capital. Everything outside that set must be bit-identical. A hand list misses ulp-level dependents such as `pb__q_eng`, `pb__rec_frac`, `lcoe_1cfe_calc__lcoe` and the `net_positive` verdict.

MR-7 is unchanged from the first review: compliant as designed, and unverified until tests 4(a), 4(d), 5–7 and 12 pass. R1 adds one call-out, `p_tf` becoming calculated, and only if that fallback is used.
