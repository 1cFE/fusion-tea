---
Status: complete
Updated: '2026-10-06'
---

# WI design: matched-duty magnet conductor alternatives

Status: reviewed (contract-review.md § Recheck r3 and design review), amended for D1–D7; D1–D7 recheck PASS (contract-review.md § Recheck D1–D7). Released for implementation 2026-09-29. Governing contract: `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (released revision; cited as “contract § n”). This design fixes the model structure, equations, interface names and bindings. Numbers and their sources come from the contract and evidence notes; every attribute in SysML carries an MR-4 citation to those sources.

## 1. Placement and isolation

- **Library (concept-agnostic, MR-3):** new file `models/library/analyses/magnet_conductor_alternatives.sysml`, package `magnet_conductor_alternatives`. It holds conductor, construction, inventory, cryogenic, cost and pair-comparison calculation definitions and five constraint definitions. Defaults are neutral (zero or unit); no concept values in the library.
- **Design:** new file `models/designs/magnet_materials/magnet_subsystem.sysml`, package `magnet_subsystem`, one part `subsystem` whose default values are the anchor D reference case at 10 T with policy-generated reference offers (contract § 5). All anchor and case values are overridable inputs.
- **Package:** `exploration/magnet_materials/` with `build.py` (pattern of `exploration/component_alternatives/build.py`), `bodies/magnet_conductor_alternatives/*_impl.py` handwritten bodies (each `AUTO_IMPLEMENTED = False`, `calculate(dict) -> dict`), generated package `magnet_materials_tea`, snapshot, census and `studies/` (route, interface, manifest).
- **Nothing existing is modified.** No Stellaris or ARIES library, design, package or study file changes. Only the two SysML files above are staged with no other library imports except `ScalarValues`.

## 2. Calculation definitions

All currents A, fields T, temperatures K, areas mm² unless named, lengths m, masses kg, power W unless named, money USD2021. Each calc's numerical semantics are the complete `calculate` function in its body; the SysML doc states that and the equations below.

### 2.1 `'Nb3Sn Cable Critical Surface'`

Inputs: `n_strands`, `strand_diameter` (m), `strand_copper_fraction` (0.5), `turn_current`, `B_peak`, `T_supply`, `nuclear_rise` (0.7 K), `margin_rise` (1.5 K), `eps_intrinsic` (fraction), `p`, `q`, `C1` (A·T per strand), `Ca1`, `Ca2`, `eps0a` (fraction), `Bc20`, `Tc0`, `fraction_rule` (0.8), `acceptance_rule` (0 temperature, 1 fraction), domain bounds `B_law_min` 8, `B_law_max` 14.5, `B_design_max` 12.2, `B_edge_max` 13.5, `T_law_min` 4.2, `T_law_max` 12, `eps_min` −0.010, `eps_max` 0.002.

Equations (Tsui & Hampshire 2012 eq. 6–7): ε_sh = Ca2·ε0a/√(Ca1² − Ca2²); s(ε) = 1 + [Ca1(√(ε_sh² + ε0a²) − √((ε − ε_sh)² + ε0a²)) − Ca2·ε]/(1 − Ca1·ε0a); Tc*(ε) = Tc0·s^(1/3); t = T/Tc*; Bc2*(T, ε) = Bc20·s·(1 − t^1.52); b = B/Bc2*; Ic_strand = (C1/B)·s·(1 − t^1.52)(1 − t²)·b^p(1 − b)^q for 0 ≤ t < 1 and 0 < b < 1, else 0 (A1: T = 0 allowed so the Tcs bracket starts at a finite Ic) (Breschi Table III form; Tsui's C in A T m⁻² converts as C1 = C × (π/4)d²). Ic_cable(T) = n·Ic_strand(B, T, ε). If Ca2 = 0 the strain shift ε_sh is 0.

Derived: T_conductor = T_supply + nuclear_rise (D4). Outputs: `T_conductor`, `ic_strand_op`, `ic_cable_op` (at T_conductor), `operating_fraction` = I/ic_cable_op, `T_cs` (bisection on [0, T_zero] where T_zero is the temperature at which b = 1, tolerance 1e−10 K; if n·Ic(B, 0) < I then `T_cs` = 0 and `tcs_defined` = 0), `tcs_defined`, `temperature_margin` = T_cs − T_conductor, `temp_rule_margin` = T_cs − (T_supply + nuclear_rise + margin_rise), `fraction_rule_margin` = fraction_rule − operating_fraction, `acceptance_margin` (the selected rule's margin), `status_code` (0 unsupported, 1 supported, 2 edge, 3 law-only; contract § 2), `supported` (1 if status ≠ 0), `acceptance_pass` (1 if supported and acceptance_margin ≥ 0), `element_area_total` = n·(π/4)d²·1e6, `element_copper_area` = strand_copper_fraction × element_area_total.

### 2.2 `'REBCO Cable Critical Surface'`

Inputs: `n_tapes`, `tape_width` (m), `tape_thickness` (m), `tape_copper_fraction` (10/56), `turn_current`, `B_peak`, `T_supply`, `nuclear_rise`, `margin_rise`, `anchor_ic` (A per tape at 20 T, 20 K), `shape_mode` (0 measured knots, 1 power law), knots `g8`, `g10`, `g12`, `g15`, `g20`, `alpha`, `T_star`, `degradation`, `fraction_rule`, `acceptance_rule`, bounds `B_knot_min` 8, `B_knot_max` 20, `B_law_min` 5, `B_law_max` 24, `T_law_min` 4.2, `T_law_max` 50.

Equations: g(B) = log-log linear interpolation between knots (shape_mode 0; supported only on [8, 20] T) or (B/20)^−α (shape_mode 1; supported on [5, 24] T). Ic_tape(B, T) = anchor_ic·g(B)·exp(−(T − 20)/T*). Ic_cable(T) = n·degradation·Ic_tape(B, T). T_cs = 20 + T*·ln(n·degradation·anchor_ic·g(B)/I) (closed form).

Outputs: as § 2.1 with `ic_tape_op`, `ic_cable_op`, and `element_area_total` = n·w·t·1e6, `element_copper_area` = tape_copper_fraction × element_area_total. Status: 1 supported inside the active shape's domain and the temperature domain, else 0 (REBCO has no edge or law-only band); `extension` is a study label, not a model status.

### 2.3 `'Winding Turn Area Screen'`

Inputs: `turn_current`, `B_peak`, `available_area`, `element_area`, `element_copper_area`, `cabling_factor`, `cable_void`, supplied areas `cu_space`, `steel_area`, `misc_area`, `solder_area`, `ins_fraction`; rule inputs `J_cu_rule` (0 disables the current-density rule), `cu_void`, `cu_per_kA_rule`, `steel_per_kA_rule`, `B_steel_ref`, `steel_B_scaling` (1 or 0).

Equations: cable = element_area/cabling_factor/(1 − cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 − ins_fraction); fit_margin = available_area − gross; required_envelope_J = I/gross. Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule − element_copper_area)/(1 − cu_void), else cu_required = cu_per_kA_rule·I/1000. Steel rule: steel_required = steel_per_kA_rule·(I/1000)·(B/B_steel_ref if steel_B_scaling else 1).

Outputs: `cable_area`, `net_area`, `gross_area`, `fit_margin`, `fit_margin_fraction` = fit_margin/available_area, `required_envelope_J`, `cu_required`, `cu_margin` = cu_space − cu_required, `steel_required`, `steel_margin` = steel_area − steel_required, `fit_pass`, `cu_pass`, `steel_pass`.

### 2.4 `'Winding Inventory and Cost'`

Inputs: `n_elements`, `element_area`, `element_density` (kg/m³), `turns`, `coils`, `turn_length`, `cu_space`, `cu_void`, `steel_area`, `solder_area`, densities `rho_cu`, `rho_steel`, `rho_solder`, prices `price_cu`, `price_steel`, `price_solder` (USD/kg), `element_price_per_m`, `manufacturing_per_m` (USD per conductor metre; default 0, nonzero only in the manufacturing-allowance variant, D7).

Equations: conductor_length = turns·coils·turn_length; element_length = n_elements·conductor_length; element_mass = element_area·1e−6/n·… (per-element area × length × density; equivalently element_area_total·1e−6·conductor_length·density); cu_mass = cu_space·(1 − cu_void)·1e−6·conductor_length·rho_cu; steel_mass and solder_mass likewise; sc_cost = element_length·element_price_per_m; materials_cost = Σ mass·price; manufacturing_cost = conductor_length·manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost.

Outputs: `conductor_length`, `element_length`, `element_mass`, `cu_mass`, `steel_mass`, `solder_mass`, `sc_cost`, `materials_cost`, `manufacturing_cost`, `winding_capital`, `ampere_metres` = turn_current·conductor_length.

### 2.5 `'Magnet Cold Stage Load'`

Inputs: `T_supply`, `T_shield` (77), `T_amb` (300), `turn_current`, `nuclear_density` (W/m³), `cold_volume` (m³), `radiation_ref` (W, temperature-independent), `conduction_ref` (W) at `T_conduction_ref`, NIST 316 fit coefficients `k_a` … `k_i`, `n_leads`, `f_lead`, `L0`, `p_joint_ref` (W at `I_joint_ref`), `I_joint_ref`, `shield_static` (W), `load_multiplier`.

Equations: K(T) = ∫_T^{T_shield} k_316(T′) dT′ with log10 k = Σ coefficients·(log10 T)^i (NIST form), integrated numerically (composite Simpson, 2000 panels in log T, tolerance checked by the oracle); q_cond = conduction_ref·K(T_supply)/K(T_conduction_ref); q_rad = radiation_ref; q_nuc = nuclear_density·cold_volume; q_lead = f_lead·n_leads·|I|·√(L0(T_shield² − T_supply²)); q_joint = p_joint_ref·(I/I_joint_ref)²; q_cold = load_multiplier·(q_nuc + q_rad + q_cond + q_lead + q_joint); q_shield = shield_static + f_lead·n_leads·|I|·√(L0(T_amb² − T_shield²)).

Outputs: `q_nuclear`, `q_radiation`, `q_conduction`, `q_leads`, `q_joints`, `q_cold`, `q_shield`, `k_integral`.

### 2.6 `'Staged Refrigeration Screen'`

Inputs: `q_cold`, `T_supply`, `q_shield`, `T_shield`, `T_amb`, `rating_cold` (W, installed offer), `eta_mode` (0 Green at installed capacity, 1 constant, 2 Green at input-power-equivalent capacity), `eta_const`, `green_a` (0.155), `green_b` (0.23), `f_carnot_shield` (0.20), `capital_mode` (0 input-power equivalence, 1 capacity basis), `green_c` (3.1e6 USD2015), `green_d` (0.65), `T_green` (4.5), `usd2015_to_2021`.

Equations: carnot = (T_amb − T_supply)/T_supply; carnot_ref = (T_amb − T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv (kW) = rating_cold/1000 × (equiv_factor if capital_mode = 0 else 1); η = green_a·(R_eta)^green_b with R_eta = rating_cold/1000 (mode 0) or rating_cold/1000·equiv_factor (mode 2), or eta_const (mode 1); p_in_cold = q_cold·carnot/η; p_in_shield = q_shield·(T_amb − T_shield)/T_shield/f_carnot_shield; capital = green_c·R_equiv^green_d·usd2015_to_2021. Efficiency is a property of the installed plant, evaluated at its rating and applied to the operating load (part-load penalty not modeled; stated).

Outputs: `carnot_specific_power`, `eta_cold`, `p_in_cold`, `p_in_shield`, `p_in_total_MW`, `R_equiv_kW`, `refrigerator_capital`, `capacity_margin` = rating_cold − q_cold, `capacity_pass`, `green_extrapolated` = 1 if the efficiency or capital argument (kW) lies outside Green's fitted data [0.01, 35] kW, else 0 (D6).

### 2.7 `'Subsystem Annualized Cost'`

Inputs: `winding_capital`, `refrigerator_capital`, `p_in_total_MW`, `crf`, `hours` (8760), `availability`, `electricity_price` (USD/MWh). Outputs: `capital_total`, `annual_electricity` = p_in·hours·availability·price, `annualized_cost` = crf·capital_total + annual_electricity.

### 2.8 `'Matched Pair Comparison'`

Inputs: `annualized_nb3sn`, `annualized_rebco`, `all_pass_nb3sn`, `all_pass_rebco`, `status_nb3sn`, `status_rebco`, `rebco_element_length`, `rebco_price_per_m`, `rebco_ic_tape_op`, `crf`. Outputs: `rankable` = all_pass_nb3sn·all_pass_rebco (all_pass already requires supported status); `pair_status` = the Nb₃Sn status code when both are supported (1 supported, 2 edge, 3 law-only), else 0 (D2); `cost_difference` = annualized_rebco − annualized_nb3sn; `breakeven_rebco_price_per_m` = rebco_price_per_m − cost_difference/(crf·rebco_element_length) (meaningful only when rankable = 1; reported otherwise but excluded from claims); `breakeven_rebco_price_per_kAm` = breakeven_per_m / (rebco_ic_tape_op/1000), per kA·m of tape critical current at the operating field and conductor temperature (D7). `all_pass_*` = acceptance_pass·fit_pass·cu_pass·steel_pass·capacity_pass.

### 2.9 Constraint definitions

`'Conductor Acceptance'` (supported ≥ 1 and acceptance_margin ≥ 0), `'Winding Fit'` (fit_margin ≥ 0), `'Protection Copper Allowance'` (cu_margin ≥ 0), `'Structural Steel Allowance'` (steel_margin ≥ 0), `'Refrigerator Capacity'` (capacity_margin ≥ 0). One asserted usage of each per material in the design. An unsupported conductor makes `'Conductor Acceptance'` violated; the separate `supported`/`status_code` outputs distinguish unsupported from failed, as in the existing `'Offered Equipment Capacity'` pattern.

## 3. Design binding (`magnet_subsystem.sysml`)

`part subsystem` owns `duty` (anchor: coils, turns, turn_length, available_area, I_ref, B_ref, B_peak; derived `turn_current` = I_ref·B_peak/B_ref as simple same-part arithmetic), economic inputs (crf, availability, electricity_price, usd factors), and two parts `nb3sn` and `rebco`. Each material part owns its supplied offer (element count, areas, temperatures, rating, prices), its conductor calc, area screen, inventory/cost, cold load, refrigeration and annualized cost usages, and asserts its five constraints. `subsystem.pair` binds the two annualized costs and pass flags into `'Matched Pair Comparison'`. Consumers bind producer attributes, never calc internals (EXPOSE pattern).

## 4. MR-7 role record

| Quantity | Role | Where bound |
|---|---|---|
| n_strands / n_tapes | chosen offer | material part input |
| cu_space, steel_area, misc_area, solder_area, ins_fraction | chosen offer (policy-generated from the construction rule at the offer's reference duty) | material part input |
| T_supply, nuclear_rise, margin_rise | chosen | material part input |
| T_conductor | derived: T_supply + nuclear_rise | conductor calc |
| rating_cold | installed capacity offer | material part input |
| turn_current, B_peak | duty (turn_current derived from B_peak at fixed geometry) | duty part |
| critical currents, Tcs, fractions | calculated | conductor calc |
| cu_required, steel_required | requirement (allowance rule) | area screen, compared with supplied areas |
| gross_area | calculated from supplied areas | area screen, compared with available_area |
| q_cold, p_in | calculated demand | cold load, refrigeration; compared with rating_cold |
| inventory, costs | calculated from supplied design | inventory/cost, refrigeration capital from rating |

No calculation writes a supplied quantity; no output is bound back as an input; nothing sets an offer from demand. The offer policy lives only in study scripts.

## 5. Verification plan

- **D1 (supplied-area precision).** The offer policy computes each rule-generated area at full double precision and then rounds it **up** to the next 1e−6 mm², so every reference offer's copper and steel margins are ≥ 0 at its reference duty. A margin in [0, 1e−6] mm² is reported as `at allowance`, not near-threshold. Test: every reference offer in the case set has cu_margin ≥ 0 and steel_margin ≥ 0 in the package.
- **D5 (hardware isolation).** Tests: varying element count changes only conductor-dependent outputs (critical current, margins, element inventory and conductor cost), not cold load, refrigeration or other materials; varying rating_cold changes only refrigerator capital, capacity margin and efficiency, not conductor or winding outputs.

- Independent oracle (separate author, from the contract and this design only) mirrors every calc; package versus oracle relative 1e−9 over all study cases.
- Source-data and anchor-reproduction tests listed in contract § 5.
- MR-7 tests: insufficient/sufficient pairs for acceptance, fit, copper, steel, capacity; field varied with hardware fixed (inventory and conductor cost unchanged); unsupported case per conductor (status 0, acceptance violated, rankable 0).
- Preservation: Stellaris and component-alternatives package fingerprints unchanged; `git diff` shows only new paths.

## 6. Case-input interface (shared by the implementation, the oracle and the offer policy)

Every case supplies all of the following design attributes; the package route maps each to its generated entry key(s). Names are exact.

- `duty`: `coils`, `turns`, `turn_length`, `available_area`, `I_ref`, `B_ref`, `B_peak` (derived in the design: `turn_current` = `I_ref`·`B_peak`/`B_ref`).
- `economics`: `crf`, `availability`, `electricity_price`, `hours`, `usd2015_to_2021`.
- For each material part `nb3sn` and `rebco`:
  - conductor: `n_elements`, `T_supply`, `nuclear_rise`, `margin_rise`, `fraction_rule`, `acceptance_rule` (T_conductor is derived: T_supply + nuclear_rise); Nb₃Sn only `strand_diameter`, `strand_copper_fraction`, `p`, `q`, `C1`, `Ca1`, `Ca2`, `eps0a`, `Bc20`, `Tc0`, `eps_intrinsic`; REBCO only `tape_width`, `tape_thickness`, `tape_copper_fraction`, `anchor_ic`, `shape_mode`, `g8`, `g10`, `g12`, `g15`, `g20`, `alpha`, `T_star`, `degradation`.
  - construction (supplied areas and rule inputs): `cabling_factor`, `cable_void`, `cu_space`, `steel_area`, `misc_area`, `solder_area`, `ins_fraction`, `J_cu_rule`, `cu_void`, `cu_per_kA_rule`, `steel_per_kA_rule`, `B_steel_ref`, `steel_B_scaling`.
  - inventory and cost: `element_density`, `rho_cu`, `rho_steel`, `rho_solder`, `price_cu`, `price_steel`, `price_solder`, `element_price_per_m`, `manufacturing_per_m`.
  - cold load: `nuclear_density`, `cold_volume`, `radiation_ref`, `conduction_ref`, `T_conduction_ref`, `n_leads`, `f_lead`, `L0`, `p_joint_ref`, `I_joint_ref`, `shield_static`, `load_multiplier` (NIST 316 coefficients are fixed design values).
  - refrigeration: `rating_cold`, `eta_mode`, `eta_const`, `green_a`, `green_b`, `f_carnot_shield`, `capital_mode`, `green_c`, `green_d`, `T_green`.

Domain bounds, T_shield (77 K), T_amb (300 K) and the NIST coefficients are fixed design values, not case inputs. Each case record also carries non-model labels (anchor, pairing, rule family, variant, offer kind) for the study.


## 7. Post-review clarifications (2026-09-29, coordinator; from the independent oracle author's notes A1, A2, A6, A7)

- A1: the Nb₃Sn validity guard is 0 ≤ t < 1 (see § 2.1).
- A2: construction C uses the unrounded Stellaris Table 7 calibration, per_kA = fraction × (0.36² m² × 1e6 / 308 mm²)/50 kA (copper 0.35, solder 0.12, helium 0.08, steel 0.36), with cabling_factor 1, cable_void 0 and ins_fraction 0; its anchor test is relative 1e−6 against 420.779220779 mm² at 50 kA and 24.9 T.
- A6: anchor D shield_static is the EU DEMO shields' own load, 912.6 + 189.4 = 1102.0 kW (Končar Table 1); the 1107.9 kW total includes the 5.9 kW that reaches the 4 K magnets, already counted in the cold stage.
- A7: anchor S turn length is 321600/(48 × 308) = 21.753246753 m exactly.
