# T-001 binding audit: magnet conductor, field, fit, cryogenics and cost

Read-only audit for goal `magnet-material-comparison`, brief `evidence/briefs/t001-binding-audit.md`. Every claim cites the code. Line numbers are for the working tree on branch `goal/magnet-material-comparison` as of 2026-09-29. Numbers quoted for the published design come from the existing write-up replay record (`.project/active/write-up/magnet-study-evaluation/replay/summary.json`, case `s0-published`), which ran on the sealed package whose fingerprint `83ea3b6cf99f…3d23` matches `exploration/stellarator_e2e/generated/contracts/package_contract.json:458`. I did not rerun the model, and I did not check that the generated package was regenerated from the current `models/` tree.

## Mental model in five lines

- The designer supplies the winding: turns, turn current, pack side, composition, tape size, allocations, casing, masses, cryoplant ratings and price.
- The model calculates the demand those choices imply: ampere-turns, fields, tape and conductor length, cold volume, cold and intercept heat loads, cryo electricity, costs, LCOE.
- A handful of checks compare demand with a supplied limit: conductor current margin, peak-field ceiling, fit, stress, strain, cold and intercept capacity. Nothing is resized to pass.
- The REBCO current law is a check only. Its outputs feed one constraint and nothing else, so it never moves cost or LCOE.
- One temperature, `cryoplant.T_cold_cryo = 20 K`, drives the conductor law, the helium inventory, the Carnot term and the thermal inventory. Three of those refuse temperatures far from 20 K.

## 1. Conductor law

**Equations (evaluated path).** `'REBCO Conductor Current'` is declared at `models/library/analyses/mfe_conductor_current.sysml:3-38` with no SysML body. Its equations live in the doc (`:4`) and in the typed manual completion `exploration/stellarator_e2e/generated/handwritten/mfe_conductor_current/rebco_conductor_current_impl.py`:

- Parallel tapes over the coil set: `N_set = tape_length / conductor_length` (impl `:37`). Reference-coil count: `N_ref = N_set * f_set / f_wp_vol` (impl `:38-39`).
- Tape critical current: `Ic_tape = reference_tape_current * (tape_width/0.004) * (B_peak/20)^-0.6 * material_factor * orientation_factor` (impl `:40-43`).
- Conductor critical current per scope: `N * Ic_tape * cabling * degradation * sharing` (impl `:44-48`). Operating fraction: `turn_current / critical_current` (impl `:49`).
- `allowable_current = allowable_fraction * critical_current_reference`; `margin_fraction = allowable_fraction - operating_fraction_reference`; `margin_current = allowable_current - turn_current` (impl `:50-52`).

**Constants hard-coded in the library completion, not design inputs:** 4 mm reference width and linear width transfer (impl `:29-30, :41`), 20 T reference field and exponent 0.6 (impl `:41`), 20 K (impl `:25-28`), 56 µm composite thickness (impl `:25-28`), 20–32 T field domain (impl `:31-32`), extrapolation above 24 T (impl `:33-35`).

**Citations.** The doc cites `work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md` and Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp. 4, 5, 7, Fig. 4 (`mfe_conductor_current.sysml:7-8`). It states that the nominal 200 A is a rounded manufacturing inference (175 A × 1.13), not a measured guarantee, and that no temperature law is implied (`:6`).

**Domain guards.** Temperature must equal exactly 20.0 K and thickness exactly 56e-6 m, otherwise the completion raises `ValueError("unsupported temperature…")` (impl `:25-28`). Width outside 4–6 mm raises (impl `:29-30`). `B_peak` outside 20–32 T raises (impl `:31-32`). Above 24 T it raises unless `allow_field_extrapolation = 1`, and then it emits `field_extrapolated = 1` (impl `:33-35`). Retention factors and the allowance must be ≤ 1 (impl `:22-24`). An unsupported input therefore aborts the evaluation. It does not return an "unsupported" status the way the WI-080 capacity screens do (`models/library/analyses/mfe_viability.sysml:106-118`).

**What is bound with `=`.** In `'Magnet System'` (`models/library/cost_structure/mfe_power_core.sysml`):

- All eleven conductor outputs are exposed with `=`, for example `conductor_margin_fraction` (`:144`) and `conductor_field_extrapolated` (`:146`). They are not swap seams.
- The calc's inputs are bound inside the definition (`:192-210`). That includes `temperature = winding_pack.T_inventory` (`:194`), which the generic plant binds to `cryoplant.T_cold_cryo` (`models/designs/generic_mfe/mfe_plant.sysml:126`).
- `tape_length` and `conductor_length` come from the procurement calc (`mfe_power_core.sysml:134-135`).

**Consumers.** In the generated pipeline the conductor module (`exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:1974-2005`) has one downstream consumer: `margin_fraction → reference_conductor_current_ok` (`pipeline.yaml:4645-4650`, asserted at `models/designs/stellarator_09/stellarator_plant.sysml:2200-2202`). Every other output is export-only (`pipeline.yaml:5469-5479`). No fit, cryo, stress, cost or LCOE module reads a conductor-law output.

**Dormant sizing and grade calcs.** `'Current Driven Pack Sizing'` (`mfe_conductor_current.sysml:39-71`) and `'Conductor Field Capability'` (`models/library/analyses/mfe_conductor_grade.sysml:4-20`) are library definitions only. Neither appears in the pipeline (zero matches for their module names in `pipeline.yaml`). The route refuses their retired entry keys (`exploration/stellarator_e2e/studies/study_route.py:184-187`).

**Where the REBCO-specific content lives.**

| content | where | kind |
|---|---|---|
| Law form, 0.6 exponent, 20 T / 4 mm reference, 20 K, 56 µm, 20–32 T domain | `rebco_conductor_current_impl.py:25-43` (library completion) | library, hard-coded |
| Calc usage is typed `'REBCO Conductor Current'` | `mfe_power_core.sysml:192` | library, fixed binding |
| Reference current 200 A per 4 mm at 20 T | default `models/library/structure/mfe_magnet_parts.sysml:93`; instance `stellarator_plant.sysml:321` | library default + design |
| Retention factors, allowance 0.8, extrapolation switch | defaults `mfe_magnet_parts.sysml:94-100`; instance `stellarator_plant.sysml:324-344` | library default + design |
| Tape width 6 mm, thickness 56 µm, price 20 $/m | `stellarator_plant.sysml:358-366` | design |
| Composition Cu 0.35 / solder 0.12 / steel 0.36 / He 0.08 (tape = residual 0.09) | `stellarator_plant.sysml:368-379`; residual rule `models/library/analyses/mfe_winding_pack_cost.sysml:7` | design + library rule |
| Strain allowable 0.4 % (REBCO tape measurements) | `stellarator_plant.sysml:428` | design |
| Field ceiling 24.9 T (Stellaris design field, owner ruling 2026-08-21) | `stellarator_plant.sysml:431-436` | design |
| Legacy REBCO $/kA·m 50 | `stellarator_plant.sysml:302` | design (comparison-only) |
| Operating temperature 20 K | `stellarator_plant.sysml:1422` | design |

## 2. Field

- **Axis field** is calculated, not supplied: `B_axis = mu0 * k_link * n_coils * I_coil / (2π R0)` (`models/library/analyses/mfe_magnet_field.sysml:57`). It is exposed as `magnet.B` with `=` (`mfe_power_core.sysml:104`).
- **Ampere-turns** are calculated: `I_coil = reference_turns * turn_current` (`mfe_magnet_field.sysml:4-13`, completion `handwritten/mfe_magnet_field/winding_operating_state_impl.py:21`). This is bound onto `coil.I_coil` (`mfe_power_core.sysml:114, 187-191`).
- **Peak field** is `B_peak = B_axis * peak_ratio * (R/(R − a_coil)) / (R_ref/(R_ref − a_coil_ref))` (`models/library/analyses/mfe_plasma_scaling.sysml:420-428`). `a_coil` is the radial-build coil-centre radius `vessel_or + coil_t/2` (`mfe_plasma_scaling.sysml:145`, fed `coil_t_in = magnet.coil.coil_t` at `mfe_plant.sysml:325`).
- The winding-pack term `R a1(C)/sqrt(A_wp)` is not carried (`mfe_plasma_scaling.sysml:441`). Pack side therefore does not change `B_peak`, but the radial allocation `coil_t` does. In the replay, raising `coil_t` from 0.30 to 0.60 m moved `r_coil_centre` from 3.15 to 3.30 m and `B_peak` from 24.90 to 25.30 T, which violated `peak_field_ok` (`replay/summary.json`, cases s0 and s2).
- **Held quantities:** `peak_ratio = 2.7667` (`stellarator_plant.sysml:246`), `R_ref`, `a_coil_ref`, `k_link` (`:250-289`). The domain is `R − a_coil > 0` (`mfe_plasma_scaling.sysml:465`).
- **A supplied peak field cannot be substituted.** `B_peak` is bound with `=` (`mfe_power_core.sysml:123`). It feeds the conductor law, stress and the ceiling check (`pipeline.yaml:1991, 2056, 4604`). The ceiling `peak_field_ok` compares it with `winding_pack.B_max` (`mfe_plant.sysml:856-859`). Matched peak field is achieved only by holding ampere-turns, R and `coil_t`.
- **Axis-field consumers outside the magnet:** `B_axis` also feeds plasma sustainment and beta (`pipeline` consumers `plasma__sustain.B_in`, `plasma__beta_calc.B_in`). Changing ampere-turns changes the plasma, and holding them keeps it fixed.

## 3. Fit

- **Equations** (`models/library/analyses/mfe_winding_pack_fit.sysml:5`):
  - Nominal: `nominal_x = wp_side*sqrt(AR)`, `nominal_y = wp_side/sqrt(AR)`.
  - Required: `required = nominal*(1+internal_fraction) + 2*ground + 2*clearance`.
  - Allocated: `cavity_x = radial_allocation − 2*wall`, `cavity_y = interior_y`.
  - Margin: `margin = cavity − required`, with `minimum_margin = min(x, y)`.
- **Bindings** (`mfe_power_core.sysml:211-221`): `radial_allocation = coil.coil_t` (`:217`), with casing `interior_y`, `wall_thickness` and `assembly_clearance`. The design supplies `wp_side = 0.36 m` (`stellarator_plant.sysml:447`), `coil_t = 0.30` (`:305`), `interior_y = 0.40`, `wall = 0.025`, `clearance = 0.002` (`:497-505`), `internal_build_y = 0.025` and `ground = 0.003` (`:351-356`).
- **Check:** `wp_fit_ok` requires `minimum_margin >= 0` (`mfe_winding_pack_fit.sysml:38-42`; asserted `stellarator_plant.sysml:2344`). The published design reads `margin_x = −0.12 m` and is violated (replay s0).
- **Turns do not enter the fit.** Nothing checks that turns × conductor cross-section fits `wp_side²`. The composition fractions make the tape volume a fixed share of the pack (`mfe_winding_pack_cost.sysml:7`), so the tape count follows from the pack. It is not an independent choice checked against the pack (see §6, parallel tapes).
- **Pack side does feed** stress (`mfe_power_core.sysml:264-269`), cold volume (`:252-262`), insulation (`:290-302`), ampere-turn density (`:187-191`), and the cryoplant surface area through `cryoplant.wp_side` (`mfe_plant.sysml:104`).

## 4. Cryogenics

**Cold load categories.** `'Cold Load Sum'` (`models/library/analyses/mfe_cryo_inventory.sysml:62-80`) computes `p_cold = f_uplift*(q_nuc*vol_cold*1e-6 + p_fixed + q_structure_nuclear*1e-6) + q_inventory_cold*1e-6` (`:79`), in MW. The terms are:

- Pack nuclear heating: `q_nuc_cryo = 35.5 W/m³` (`stellarator_plant.sysml:492`).
- Joints: `p_fixed_cryo = 7.5 kW` (`:1416`).
- Structure nuclear heating, currently zero (`:1393`).
- The enumerated thermal inventory: cold lead segment, radiation, and support conduction (`mfe_cryo_inventory.sysml:3-61`).

**Cold volume basis.** Volume, not mass: `vol_cold_total = f_wp_vol * n_coils * wp_side² * c_coil + vol_extra` (`mfe_magnet_field.sysml:258`). `vol_cold_cryo = 0` (`stellarator_plant.sysml:165`). The published volume is 136.56 m³ (replay s0).

**Staging.** There are two stages:

- **Cold stage** at `T_cold_cryo`. Electricity is `p_elec = p_cold / (f_carnot * T_cold/(T_amb − T_cold))` (`models/library/analyses/mfe_cryo_plant.sysml:8-10`, usage `models/library/structure/mfe_plant_systems.sysml:636-645`).
- **Intercept stage** at 77 K: `q_shield*(T_amb − T_shield)/(f_carnot_shield*T_shield)` (`mfe_cryo_inventory.sysml:89-101`, usage `mfe_plant_systems.sysml:623-629`).
- The two are summed (`mfe_plant_systems.sysml:630-633, 586`) and sent to the power balance `pb.p_cryo` (`pipeline.yaml:2119`; `mfe_plant.sysml:395`). Lead and joint drive power goes separately to `p_tf_extra` (`mfe_plant.sysml:192`).
- Both Carnot fractions are 0.20 (`stellarator_plant.sysml:1366, 1428`).
- At fixed `f_carnot`, the specific power ratio `(300−T)/T` is 14.0 W/W at 20 K and 65.7 W/W at 4.5 K. That is 4.7 times higher per watt of cold load.

**Temperature domains.**

- `'Coil Thermal Inventory'` requires `10 <= T_cold <= 30 K`, `T_shield = 77` and `T_amb = 300`, or it raises (`handwritten/mfe_cryo_inventory/coil_thermal_inventory_impl.py:20-21`; doc `mfe_cryo_inventory.sysml:7`).
- Its support conductances `k_c` (cold→77 K) and `k_s` (77→300 K) are fixed segment means for a 316 proxy, valid under a stated 10–30 K cold-end approximation (`mfe_cryo_inventory.sysml:23-24`; values `stellarator_plant.sysml:1387-1391`).
- `'Cryoplant Electrical Power'` requires only `0 < T_cold < T_amb` (`handwritten/mfe_cryo_plant/cryoplant_electrical_power_impl.py:14-15`).
- The winding helium inventory uses ideal-gas density at `T_inventory` (`mfe_winding_pack_cost.sysml:7`, impl `winding_pack_material_inventory_impl.py:45`). Its registered sources are the NIST 20 K isotherm and the 10–50 K isobar (`mfe_winding_pack_cost.sysml:10-11`).

**Installed capacity versus demand.**

- The supplied ratings are `rated_cold_W = 21933.902368719853`, `rated_intercept_W = 41599.953939961626`, and rated conditions 20 / 77 / 300 K (`stellarator_plant.sysml:1343-1348`).
- `'Offered Capacity Screen'` computes rating minus demand (`mfe_viability.sysml:106-118`; usages `mfe_plant_systems.sysml:486-509`).
- Both margins read exactly 0.0 at the published design (replay s0). The captured ratings equal the entering demand to the last digit, so any added cold or intercept load reads as a shortage. Replay s1–s3 violate both stage checks only because the pack grew.
- Applicability is a point match of actual against rated temperatures within 8 ulp (`mfe_viability.sysml:74-75`; usage `mfe_plant_systems.sysml:470-481`). A 4.5 K operating point against a 20 K rating is "unsupported". The asserted `'Offered Equipment Capacity'` constraint needs `defined >= 1` (`mfe_viability.sysml:119-123`), so the verdict alone shows unsupported as violated. The separate `supported` and `applicable` outputs distinguish the two cases.

**Cryo capital** is the supplied package price `purchase_cost_per_module = 31.48 M$` (`stellarator_plant.sysml:1350`). It passes through `cryo_cost = purchase_cost_in` (`models/library/analyses/mfe_account_costs.sysml:33-39`) into `cas22_capital.aux_cooling_capital` (`pipeline.yaml:4030`). It does not follow demand or temperature.

## 5. Cost

- **Conductor purchase basis is individual tape metres derived from pack volume.** `tape_volume = vol_winding_pack * (1 − f_Cu − f_solder − f_steel − f_He)` (`mfe_winding_pack_cost.sysml:7`). `tape_length = tape_volume/(tape_width*tape_thickness)` and `tape_cost = tape_length * tape_price_per_m` (`mfe_winding_pack_cost.sysml:44`). The price is 20 $/m of 6 mm × 56 µm tape, an [AGENT] illustrative value (`stellarator_plant.sysml:364-366`). The published quantity is 36.58 million tape-metres (replay s0).
- **Conductor length** (composite-conductor metres) is `n_coils * reference_turns * f_set * c_coil` (`mfe_winding_pack_cost.sysml:44`). Published value: 321,600 m (replay s0).
- **Winding operations:** `conductor_length * 480 $1990/m * 2.5585 (CPI) * 1.9 (non-planar)` (`mfe_winding_pack_cost.sysml:44`; values `stellarator_plant.sysml:409-418`; UKAEA PROCESS `ucwindtf`).
- **Non-tape materials:** mass = volume × fraction × density × $/kg for copper, solder, steel and helium (`mfe_winding_pack_cost.sysml:7`). Prices: Cu 11 and steel 6 (1costingFE, year unstated), solder 64.44 (2026 $), helium 88.16 (estimated 2026 $) (`stellarator_plant.sysml:385-402`).
- **Insulation sheet stock:** `mfe_winding_pack_cost.sysml:72` (61.68 $/m², `stellarator_plant.sysml:462`).
- **Structure:** `(legacy_casing_fraction * n_coils * m_casing + m_support) * steel_price * f_steel_fab` (`models/library/analyses/mfe_magnet_cost.sysml:178`). The supplied masses are `m_support = 11.6 kt` and `legacy_casing_fraction = 0` (`stellarator_plant.sysml:116-120`).
- **Rollup:** `capital = winding_cost + structure_cost + insulation_stock_cost` (`mfe_magnet_cost.sysml:203`; `mfe_power_core.sysml:360-364`), where `winding_cost default winding_procurement.cost` (`:129`). Magnet capital feeds `powercore_capital` (`pipeline.yaml:2240-2243`) and LCOE. In the replay, the s0→s1 pack growth raised magnet capital from 1.71 to 2.55 G$ and LCOE from 318.7 to 340.7 $/MWh.
- **Comparison-only $/kA·m channels:** `'Magnet Coil Cost'` (`mfe_magnet_cost.sysml:9-10, 50-53`) and legacy `'Winding Pack Cost'` (`:60-61, 98-100`) use `cost_per_kAm = 50` (`stellarator_plant.sysml:302`). The legacy account scales with operating ampere-turns `I_coil`, which is demand-scaled. Neither is in the rollup.
- **Supplied versus calculated:** prices, rates, fractions, densities, tape dimensions, masses and turns are supplied. Tape volume, tape length, conductor length, masses of pack materials and all costs are calculated.

## 6. Design instance and pipeline

**Supplied winding** (`models/designs/stellarator_09/stellarator_plant.sysml`): 48 coils (`:223`), 308 reference turns (`:254`), 50 kA per turn (`:202`), pack side 0.36 m (`:447`), radial allocation 0.30 m (`:305`), casing interior 0.40 m, wall 0.025 m, clearance 0.002 m (`:497-505`), `f_set = 0.870` (`:231`), `f_wp_vol = 0.878` (`:465`), cryo ratings 21.93 kW cold / 41.60 kW intercept at 20 / 77 / 300 K (`:1343-1348`), cryo package price 31.48 M$ (`:1350`), `T_cold_cryo = 20 K` (`:1422`).

**Parallel tapes are calculated, not supplied.** Combining impl `:37-39` with `mfe_winding_pack_cost.sysml:7, 44` gives `N_ref = wp_side² * f_tape / (tape_width * tape_thickness * reference_turns)`. At the published design that is 0.1296 × 0.09 / (3.36e-7 × 308) = 112.7 tapes (replay s0 `parallel_tapes_reference = 112.709`).

**Published result:** `Ic_tape = 263.0 A`, operating fraction 1.687, `margin_current = −26.3 kA`, and `reference_conductor_current_ok` is violated (replay s0). The published REBCO winding fails its own current check at 24.9 T.

**Generated pipeline:** `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml` (6297 lines). `T_cold_cryo` is read directly by five modules: offered conditions (`:190`), thermal inventory (`:1745`), cold-stage electricity (`:1836`), helium inventory (`:1892`) and the REBCO law (`:1989`).

### Role table (MR-7 classes)

| quantity | units | current role | binding location | consumers |
|---|---|---|---|---|
| `reference_turns` | 1 | chosen | `stellarator_plant.sysml:254` | winding_state (`I_coil`), winding_procurement (`conductor_length`) |
| `turn_current` | A | chosen (operating) | `stellarator_plant.sysml:202` | winding_state, conductor law, cryo lead heat via `I_turn` (`mfe_plant.sysml:105`) |
| `I_coil` | A-turn | calculated | `mfe_power_core.sysml:114, 187-191` | axis field, stored energy, stress, legacy kA·m cost |
| `j_wp_effective` | A/mm² | calculated | `mfe_power_core.sysml:117` | export only |
| `B_axis` (`magnet.B`) | T | calculated | `mfe_power_core.sysml:104, 157-162` | plasma sustain and beta, peak field, 1cfe comparison cost |
| `B_peak` | T | calculated (not suppliable) | `mfe_power_core.sysml:123, 167-174` | conductor law, stress, `peak_field_ok` |
| `B_max` | T | requirement/limit | `stellarator_plant.sysml:436` | `peak_field_ok` (`mfe_plant.sysml:856`) |
| `wp_side` | m | chosen | `stellarator_plant.sysml:447` | fit, cold volume, stress, insulation, `j_wp`, cryo surface area |
| `coil_t` (radial allocation) | m | chosen | `stellarator_plant.sysml:305` | fit cavity, radial build `r_coil_centre` → `B_peak`, `c_coil` |
| `interior_y`, `wall_thickness`, `assembly_clearance` | m | chosen | `stellarator_plant.sysml:497-505` | fit |
| `f_Cu`, `f_solder`, `f_steel`, `f_He` | 1 | chosen (construction) | `stellarator_plant.sysml:368-379` | material inventory → tape volume |
| tape fraction (residual) | 1 | calculated | `mfe_winding_pack_cost.sysml:7` | tape volume |
| `tape_width`, `tape_thickness` | m | chosen (construction; thickness domain-locked to 56 µm) | `stellarator_plant.sysml:358-363` | procurement, conductor law |
| `tape_length` | m | calculated | `mfe_winding_pack_cost.sysml:44`; `mfe_power_core.sysml:134` | tape cost, conductor law |
| `conductor_length` | m | calculated | `mfe_winding_pack_cost.sysml:44`; `mfe_power_core.sysml:135` | winding operations cost, conductor law |
| `parallel_tapes_set` / `_reference` | 1 | calculated (implicit, not supplied) | `rebco_conductor_current_impl.py:37-39` | export only |
| `reference_tape_current` | A per 4 mm at 20 T, 20 K | policy-selected performance assumption | `stellarator_plant.sysml:321` | conductor law |
| material/orientation/cabling/degradation/sharing factors | 1 | policy-selected assumption | `stellarator_plant.sysml:324-338` | conductor law |
| `allowable_fraction` | 1 | requirement/limit | `stellarator_plant.sysml:339` | conductor law margin |
| `allow_field_extrapolation` | 0/1 | policy-selected switch | `stellarator_plant.sysml:342` | conductor law domain |
| `margin_fraction` | 1 | calculated check operand | `rebco_conductor_current_impl.py:51` | `reference_conductor_current_ok` (`stellarator_plant.sysml:2200`) |
| critical currents, operating fractions, `margin_current` | A, 1 | calculated | `rebco_conductor_current_impl.py:44-52` | export only |
| fit margins | m | calculated check operand | `mfe_winding_pack_fit.sysml:5` | `wp_fit_ok` (`stellarator_plant.sysml:2344`) |
| `sigma_wp` / `sigma_allow` | Pa | calculated / limit | `mfe_power_core.sysml:264-269`; `stellarator_plant.sysml:549` | `wp_stress_ok`, conductor strain |
| `eps_cond` / `eps_cond_allow` | 1 | calculated / limit | `mfe_power_core.sysml:273-277`; `stellarator_plant.sysml:428` | `cond_strain_ok` |
| `vol_cold_total` | m³ | calculated | `mfe_magnet_field.sysml:258`; `mfe_power_core.sysml:252-262` | cold load |
| `T_cold_cryo` | K | chosen (operating temperature) | `stellarator_plant.sysml:1422` | conductor law, helium inventory, Carnot, thermal inventory, offered conditions |
| `f_carnot_cryo`, `f_carnot_shield` | 1 | policy-selected assumption | `stellarator_plant.sysml:1428, 1366` | cold and intercept electricity, thermal inventory |
| `p_cold`, `q_inventory_shield` | MW, W | calculated demand | `mfe_cryo_inventory.sysml:79`; `mfe_plant_systems.sysml:588-622` | cryo electricity, stage screens |
| `rated_cold_W`, `rated_intercept_W` | W | installed capacity (captured equal to entering demand) | `stellarator_plant.sysml:1346-1347` | cold and intercept capacity checks |
| `rated_cryogenic_*_K` | K | installed rating conditions | `stellarator_plant.sysml:1343-1345` | applicability of both stage screens |
| cryo `p_elec` | MW | calculated demand | `mfe_plant_systems.sysml:586` | `pb.p_cryo` → net power → LCOE |
| cryo `purchase_cost_per_module` | $ | chosen (supplied price) | `stellarator_plant.sysml:1350` | CAS22 aux cooling → LCOE |
| `tape_price_per_m` | $/m | chosen price assumption | `stellarator_plant.sysml:364` | tape cost |
| winding rate × escalation × non-planar | $1990/m, 1, 1 | inherited price assumption | `stellarator_plant.sysml:409-418` | winding operations cost |
| `price_*`, `rho_*`, helium pressure | $/kg, kg/m³, Pa | chosen assumptions | `stellarator_plant.sysml:380-405` | material inventory cost |
| `cost_per_kAm` | $/kA·m | inherited, comparison-only | `stellarator_plant.sysml:302` | 1cfe comparison and legacy accounts (not in rollup) |
| `m_support`, `m_casing` | kg | chosen | `stellarator_plant.sysml:116, 518` | structure cost; `cryoplant.m_support` |
| magnet capital | $ | calculated | `mfe_magnet_cost.sysml:203` | `powercore_capital` → LCOE |

## 7. Existing evaluation route

`.project/active/write-up/magnet-study-evaluation/replay_supplied_windings.py` (read only):

- **Runner.** It imports the package-owned `exploration/stellarator_e2e/studies/study_route.py` (`replay:33-34`). It calls `route.run_points(study_id, proposals, out_dir)` (`replay:80`), which runs stock teax `simkit.study.runner.StudyRunner` over a `PreparedEvaluator` on the sealed package `exploration/stellarator_e2e/generated` (`study_route.py:230-248, 290-335`).
- **Environment.** Teax comes from `STOP_PARSER_TEAX_ROOT` (`replay:32`), and the script is invoked through `.codex-test/run python …` (`replay:15-17`). It records the package identity (`replay:77`).
- **Overrides.** Proposals are flat entry-key → float maps with prefix `stellarator_09__stellaris__` (`study_route.py:69`). The replay overrode only `magnet__winding_pack__wp_side`, `magnet__coil__coil_t` and `magnet__casing__interior_y` (`replay:39-52`). All other inputs stayed at package defaults.
- **Refused keys.** `validate_proposal` refuses the retired sizing keys (`I_coil`, `j_wp`, grade and sizing-mode keys; `study_route.py:181-187`) and requires finite floats or declared Booleans (`:190-199`).
- **Outputs read.** Each case's `inputs`, `outputs` and `verdicts` (`replay:84-96`), filtered to substrings for field, conductor law, fit, tape and conductor length, magnet capital, cold volume, the cryo stages, stress, strain and LCOE (`replay:53-59`). Magnet verdicts are summarized per constraint (`replay:95`). The script also hashes `generated/` and `models/` before and after to prove nothing changed (`replay:62-67, 99-105`).
- **Implication.** Any plant input, including `cryoplant__T_cold_cryo`, the composition, tape size and price, turns and cryo ratings, can be overridden the same way. A 4.5 K override would reach the REBCO law and the thermal inventory, and both raise (§1, §4). I did not run this case, so how the runner records the refusal is unverified.

## 8. Seams for an additive alternative

**Existing mechanism (WI-057 D5/D9).** A variant is a `part def` specializing `'Magnet System'`. It adds its own template calc and rebinds a swap seam declared `default`, and the instance swaps by retyping (`work/active/WI-057_stellaris-structural-decomposition/design.md:55, 63`; demonstration in `prototype/swap/`).

- Only two seams exist today: `winding_cost default winding_procurement.cost` (`mfe_power_core.sysml:129`) and `structure_cost default magnet_structure_cost.cost` (`:149`).
- The rules from that design: `=` bindings on a definition are final. A variant cannot rebind a template calc's formals or redefine a calc by name. The base template calc still executes in a retyped instance (`design.md:63`).
- Fact variants need no retype: rebinding in the instance is the swap (`design.md:63`).

**Component-alternatives pattern (WI-096).** It builds additive copied definitions and an isolated design and package, and leaves the original source, packages and studies unchanged (`work/active/WI-096_matched-conversion-subsystems/design.md:73, 164`; `models/designs/component_alternatives/plant.sysml`, `models/library/analyses/component_alternatives_thermal.sysml`, `exploration/component_alternatives/`).

**Why a 4.5 K Nb₃Sn case cannot run by retyping or overriding alone.** In the retyped instance, the base `'REBCO Conductor Current'` usage still executes. Its temperature is bound through `winding_pack.T_inventory = cryoplant.T_cold_cryo` (`mfe_power_core.sysml:194`; `mfe_plant.sysml:126`), and it raises at any temperature other than 20 K (impl `:25-28`). `'Coil Thermal Inventory'` raises below 10 K (`coil_thermal_inventory_impl.py:20-21`) and is bound inside `'Cryoplant'` with `=` (`mfe_plant_systems.sysml:588-612`).

**Smallest change set I see (not implemented; REBCO behavior unchanged at every valid REBCO input):**

1. **New conductor law, additive.** New `models/library/analyses/mfe_conductor_nb3sn.sysml` holding `'Nb3Sn Conductor Current'`, with its own law, sourced constants, explicit temperature/field/strain domain and supported/unsupported outputs, plus its handwritten completion.
2. **Promote the conductor exposes to seams, value-neutral.** In `mfe_power_core.sysml:136-146`, change the eleven `conductor_* : Real = conductor_current.*` exposes to `default` (D5 says this has no numeric effect). The minimum is `conductor_margin_fraction` (`:144`), which is the only one asserted.
3. **Make the REBCO law skippable, behavior-neutral for REBCO.** Add an applicability input to `'REBCO Conductor Current'` (`mfe_conductor_current.sysml:10-26`), bound from a new `default true` attribute on `'Winding Pack'` (`mfe_magnet_parts.sysml:56-134`). When the input is false, the completion returns undefined outputs instead of raising. This follows the WI-080 `enabled` / `evaluation_defined` pattern (`mfe_viability.sysml:74-118`). Without this step, or without decoupling `:194` from `T_cold_cryo`, the base calc aborts every non-20 K case.
4. **Variant magnet definition.** Add `'Nb3Sn Magnet System' :> 'Magnet System'` in a variant file outside the canonical library tree, as WI-057 N4 requires (`design.md:63`). It adds the Nb₃Sn calc, rebinds the conductor seams and sets the REBCO-applicability attribute false. If strand or cable pricing differs from $/tape-metre, it also rebinds `winding_cost` (`mfe_power_core.sysml:129`) to an Nb₃Sn procurement calc that includes reaction heat treatment.
5. **4 K thermal inventory.** Either extend `'Coil Thermal Inventory'` to 4–5 K with sourced 4.5→77 K conductivity integrals (`mfe_cryo_inventory.sysml:7, 23-24`; `coil_thermal_inventory_impl.py:20`), or add a 4 K calc and promote `cryoplant.inventory` outputs to seams (`mfe_plant_systems.sysml:587-625`). Also supply a real-gas helium density or a supplied density for the 4.5 K inventory (`mfe_winding_pack_cost.sysml:7`).
6. **Isolated Nb₃Sn instance.** Add a new design file and package, following the WI-096 isolation pattern, that retypes `magnet` and supplies:
   - Nb₃Sn construction and composition, and `B_max`;
   - `eps_cond_allow` for Nb₃Sn;
   - `T_cold_cryo ≈ 4.5 K`;
   - new 4.5 K rated conditions and ratings (`stellarator_plant.sysml:1343-1347` analogs), a cryo package price (`:1350` analog), and the Carnot fraction at 4.5 K.
   
   `models/designs/stellarator_09/stellarator_plant.sysml` and its package stay untouched.

Steps 2 and 3 edit shared library bindings. They are value-neutral for REBCO, but they change the generated package bytes and fingerprint. MR-7 review applies to both (`modeling_project/REQUIREMENTS.md:103`).

## Implications for a material comparison

**What the current model can already evaluate at a supplied duty.** Any supplied REBCO winding at exactly 20 K with 20 T ≤ `B_peak` ≤ 32 T can be evaluated by input overrides through `study_route.run_points` (§7). The outputs are:

- current margin;
- fit, stress and strain;
- the peak-field ceiling;
- cold volume and cold/intercept demand against the supplied ratings;
- tape, material, winding and insulation cost;
- structure cost, cryo electricity and LCOE.

Matched duty is easy to hold. Keeping `reference_turns × turn_current`, R and `coil_t` fixed fixes `B_axis`, `B_peak` and the plasma (§2). Keeping `reference_turns` fixed fixes conductor length (`mfe_winding_pack_cost.sysml:44`). Together, same ampere-turns and same conductor length force the same 308 turns at 50 kA. The only free conductor choices are construction, pack side within the allocation, temperature, and price.

**What is REBCO-specific.**

- The law and its whole domain are hard-coded in the library completion (§1 table).
- The procurement basis assumes a rectangular tape priced per metre, with count implied by the pack composition (`mfe_winding_pack_cost.sysml:44`).
- Design facts: the 0.4 % strain allowable, the 24.9 T ceiling, the 200 A reference current, and the 20 K temperature.
- The 20 K cryo ratings, point conditions and captured price.

**What is missing for Nb₃Sn.**

- **Law:** no Nb₃Sn critical-current law, with its field, temperature and strain dependence and sourced constants.
- **Construction:** no strand or cable definition (non-Cu fraction, Cu:non-Cu, void, jacket). Parallel count is implicit, not supplied.
- **Temperature:** three calcs refuse or are unsourced near 4.5 K (§4, §8).
- **Cryo staging:** no 4.5 K rating, price or Carnot basis. The ratings are point-matched at 20 K and captured at zero margin, and the conductivity integrals are for the 20 K span.
- **Cost:** no Nb₃Sn price basis ($/m, $/kg or $/kA·m and its year), and no wind-and-react heat-treatment account.

**Premise conflicts to surface to the owner before design.**

1. **The published REBCO reference already fails at the stated duty.** Its current check reads operating fraction 1.687 and margin −26.3 kA, and its fit check reads −0.12 m (replay s0). No supplied winding in the existing replay passes every magnet check at 24.9 T: s1 fails fit and both cryo stages, and s2/s3 fail the peak-field ceiling and both cryo stages. A "matched duty" comparison against this reference compares an Nb₃Sn candidate with a failing REBCO design, unless the goal first supplies a passing REBCO winding.
2. **The two conductors have no overlapping supported field domain.** The REBCO law refuses below 20 T. Nb₃Sn at 4.2–4.5 K is normally operated well below about 16 T peak, and its upper critical field at 4.2 K is roughly 25–30 T. That second statement is [AGENT] domain knowledge and is not yet checked against a registered source. At the Stellaris 24.9 T duty, Nb₃Sn is at or beyond its usable limit. At a field Nb₃Sn can carry, the REBCO law has no supported domain. The plan's "same peak field" therefore needs an owner decision:
   - accept "Nb₃Sn unsupported or failed at 24.9 T" as the result;
   - pick a lower-field duty and extend the REBCO law below 20 T with new evidence; or
   - drop peak field from the match.
3. **Matched duty constrains pack growth.** `B_peak` and `c_coil` depend on the radial allocation `coil_t` (§2). A lower-current-density Nb₃Sn pack that needs more allocation raises the peak field and the conductor length. Duty is matched only if allocation is held fixed, in which case the fit check decides feasibility.
4. **The conductor law never reaches cost.** The law feeds one constraint only (`pipeline.yaml:4645-4650`). Cost and LCOE differences between materials will come from supplied construction, prices, temperature (4.7× Carnot penalty at fixed fraction), cryo ratings and cryo price, not from the law. The law only decides the verdict. This is MR-7-consistent, but it means an Nb₃Sn winding must be designed and priced by someone. It also means the cryo capital difference exists only if a 4.5 K package price is supplied.
5. **"REBCO byte-identical" versus a shared package.** A 4.5 K variant cannot run inside the current package without editing shared bindings (§8 steps 2–3), because the base REBCO calc and the thermal inventory raise at 4.5 K. Byte identity holds only with an isolated package. Behavioral identity holds with the gated edits.
