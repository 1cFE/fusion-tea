# WI-099 independent oracle and offer policy: notes

Author: independent oracle author (T-005), brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t005-oracle-policy.md`. Written from the released contract (`evidence/comparison-contract.md` r3) and the reviewed design (`work/active/WI-099_magnet-conductor-alternatives/design.md` §§ 2, 5, 6) only. I did not read the implementer's SysML, bodies or package. The coordinator's `reference-case.json` was used only as a layout cross-check after my own offers were generated.

## What exists

- `exploration/magnet_materials/oracle.py`: one function per design § 2 calc, keyed by the § 2 input names and returning every § 2 output under the same names. `evaluate_case(case)` takes a § 6-keyed case and returns per-material outputs plus the pair comparison. Standard library only.
- `exploration/magnet_materials/studies/offer_policy.py`: the declared offer policy (contract § 5), the anchors, conductors, constructions and the variant table, all cited.
- `exploration/magnet_materials/studies/declare_cases.py` writes `cases.json` (2832 cases, 12.3 MB, one case per line). Run: `.codex-test/run python exploration/magnet_materials/studies/declare_cases.py`.
- `tests/models/test_magnet_oracle.py`: 58 pure-oracle tests (source points, anchors, Tcs root, MR-7 behaviour, D1 and D5, case-set policy checks). Run: `.codex-test/run python -m pytest tests/models/test_magnet_oracle.py -q` (58 passed, about 23 s).

## Methods that differ from the implementer's (by design)

- **Tcs root (Nb₃Sn).** Brent–Dekker on [0, T_zero], absolute tolerance 1e−13 K (`oracle.py` `brent_root`). The design's implementer uses bisection. A test checks Brent against a 200-step bisection to 1e−9 K and checks n·Ic(Tcs) = I to 1e−9 relative.
- **NIST 316 integral.** Composite 10-point Gauss–Legendre on 64 equal panels in ln T (nodes computed by Newton iteration). The design's implementer uses Simpson in log T. A test checks 16 and 256 panels agree to 1e−13 and a 20,000-panel Simpson in T agrees to 1e−10. K(4.5 K) = 325.98282084 W/m, K(20 K) = 307.43674001 W/m, K(4 K) = 326.13051739 W/m.

## Equations as implemented

Units: A, T, K, mm² for areas, m, kg, W unless named, USD2021.

- **Nb₃Sn (§ 2.1).** ε_sh = Ca2·ε0a/√(Ca1² − Ca2²), or 0 when Ca2 = 0. s(ε) = 1 + [Ca1(√(ε_sh² + ε0a²) − √((ε − ε_sh)² + ε0a²)) − Ca2·ε]/(1 − Ca1·ε0a). Tc* = Tc0·s^(1/3), t = T/Tc*, Bc2* = Bc20·s·(1 − t^1.52), b = B/Bc2*. Ic_strand = (C1/B)·s·(1 − t^1.52)(1 − t²)·b^p(1 − b)^q for 0 ≤ t < 1 and 0 < b < 1, else 0 (see A1). T_conductor = T_supply + nuclear_rise. T_zero = Tc*·(1 − B/(Bc20·s))^(1/1.52), or 0 when B ≥ Bc20·s. If n·Ic(B, 0) < I then T_cs = 0 and tcs_defined = 0, else T_cs is the Brent root of n·Ic(B, T) = I on [0, T_zero]. Rule margins: temp_rule_margin = T_cs − (T_supply + nuclear_rise + margin_rise); fraction_rule_margin = fraction_rule − I/(n·Ic(T_conductor)). acceptance_rule 0 selects the temperature margin, 1 the fraction margin. Status: 0 unless 8 ≤ B ≤ 14.5 T, 4.2 ≤ T_conductor ≤ 12 K and −0.010 ≤ ε ≤ 0.002; then 1 for B ≤ 12.2, 2 for B ≤ 13.5, else 3. acceptance_pass = supported and margin ≥ 0. element_area_total = n·(π/4)d²·1e6; element_copper_area = strand_copper_fraction × that.
- **REBCO (§ 2.2).** g(B): shape_mode 0 interpolates the five knots linearly in (ln B, ln g); outside [8, 20] T the end segment is extended (status is 0 there and the value carries no claim). shape_mode 1 is (B/20)^−α. Ic_tape = anchor_ic·g·exp(−(T − 20)/T*). ic_cable_op = n·degradation·Ic_tape(T_conductor). T_cs = 20 + T*·ln(n·degradation·anchor_ic·g/I). Status 1 only inside the active shape's field domain and 4.2 ≤ T_conductor ≤ 50 K. tcs_defined = 1 whenever the log argument is positive (see A20).
- **Area screen (§ 2.3).** cable = element_area/cabling_factor/(1 − cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 − ins_fraction); fit_margin = available_area − gross; required_envelope_J = I/gross. cu_required = max(0, I/J_cu_rule − element_copper_area)/(1 − cu_void) when J_cu_rule > 0, else cu_per_kA_rule·I/1000. steel_required = steel_per_kA_rule·(I/1000)·(B/B_steel_ref if steel_B_scaling ≠ 0 else 1). Pass flags are margin ≥ 0.
- **Inventory and cost (§ 2.4).** L = turns·coils·turn_length; element_length = n·L; element_mass = element_area_total·1e−6·L·element_density; cu_mass = cu_space·(1 − cu_void)·1e−6·L·rho_cu; steel_mass = steel_area·1e−6·L·rho_steel; solder_mass = solder_area·1e−6·L·rho_solder (A4); sc_cost = element_length·element_price_per_m; materials_cost = Σ mass·price; manufacturing_cost = L·manufacturing_per_m; ampere_metres = I·L.
- **Cold stage (§ 2.5).** q_cond = conduction_ref·K(T_supply)/K(T_conduction_ref) with K(T) = ∫_T^77 k316; q_rad = radiation_ref; q_nuc = nuclear_density·cold_volume; q_lead = f_lead·n_leads·|I|·√(L0(77² − T_supply²)); q_joint = p_joint_ref·(I/I_joint_ref)²; q_cold = load_multiplier × the sum; q_shield = shield_static + f_lead·n_leads·|I|·√(L0(300² − 77²)); k_integral = K(T_supply).
- **Refrigeration (§ 2.6).** carnot = (300 − T_supply)/T_supply; equiv = carnot/((300 − T_green)/T_green); R_equiv_kW = rating/1000 × (equiv if capital_mode 0 else 1); η = green_a·(rating/1000)^green_b (mode 0), eta_const (mode 1), green_a·(rating/1000·equiv)^green_b (mode 2); p_in_cold = q_cold·carnot/η; p_in_shield = q_shield·(300 − 77)/77/f_carnot_shield; capital = green_c·R_equiv^green_d·usd2015_to_2021; green_extrapolated = 1 if R_equiv or the efficiency argument lies outside [0.01, 35] kW (A11).
- **Annualized (§ 2.7).** capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW·hours·availability·electricity_price; annualized_cost = crf·capital_total + annual_electricity.
- **Pair (§ 2.8).** all_pass = acceptance·fit·cu·steel·capacity passes. rankable = product of both all_pass. pair_status = Nb₃Sn status when both statuses are nonzero, else 0. cost_difference = annualized_rebco − annualized_nb3sn. breakeven_per_m = rebco_price − cost_difference/(crf·rebco_element_length); breakeven_per_kAm = breakeven_per_m/(ic_tape_op/1000).

## Constants and their sources

| Quantity | Value | Source |
|---|---|---|
| NIST 316 k(T) coefficients a–i | −1.4087, 1.3982, 0.2543, −0.6260, 0.2334, 0.4256, −0.4658, 0.1650, −0.0199 | `knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md:24-32` |
| Breschi Table III, ten TF production sets | p, q, Ca1, Ca2, ε0a (fraction), Bc20, Tc0, C1 as in `offer_policy.py` | `knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf` p.24, rendered and read by me; matches check A r3 to 0.01 A |
| Reference strand | WST TFCN5-6 | contract § 3 |
| Tsui BEAS II and OST (Table 5c, 5a) | C converted as C1 = C·(π/4)(0.82 mm)² | `evidence/sources/nb3sn-law.md:22-24`; check A § 1 |
| Strand diameter, Cu fraction | 0.82 mm, 0.5 | contract § 3 |
| REBCO knots 8/10/12/15/20 T | 2.11, 1.85, 1.61, 1.33, 1.00 | contract § 3 (Molodyk Fig. 1a) |
| REBCO anchor, T*, degradation, α | 198 A, 22 K, 0.90, 0.6 | contract § 3 |
| Tape | 4 mm × 56 µm, Cu 10/56 | contract § 3–4 |
| Temperatures | Nb₃Sn 4.5 K supply, REBCO 20 K, rise 0.7 K, margin 1.5 K, fraction 0.8 | contract § 3 |
| Construction P | cabling 0.97, void 0.20, J_Cu 93.4 A/mm², Cu void 0.10, steel 12.66 mm²/kA × B/12.04 T, misc 1.1077 mm²/kA, insulation 0.237 | contract § 4 |
| Construction C | Cu 2.945455, solder 1.009870, He 0.673247, steel 3.029610 mm²/kA × B/24.9 T; cabling 1, void 0, insulation 0 | Table 7 fractions × (0.36² m²/308)/50 kA, contract § 4 (A2) |
| Anchor D geometry | 16 × 142, 104.95 kA at 12.04 T, 1296 × 411 mm / 142 = 3751.099 mm², 55.6 m | contract § 2 |
| Anchor D cold | nuclear 35.5 W/m³ × 473.851 m³; radiation 1.3 kW; conduction 4.6 kW at 4 K; 4 leads, f 1.25; joints 256 nΩ × I² = 2819.71 W at 104.95 kA; shield static 1102.0 kW | contract § 6; Končar Table 1 (`knowledge/raw/koncar17578.pdf` pp.4–5, rendered) (A6, A19) |
| Anchor S geometry | 48 × 308, 50 kA at 24.9 T, 420.779 mm², 21.753247 m | contract § 2; replay conductor_length 321,600.0 m (A7) |
| Anchor S cold | nuclear 35.5 × 136.56 m³; radiation 266.681 W; conduction 590.279 W at 20 K; 12 leads, f 1.25; joints 7.5 kW at 50 kA; shield static 7561.689 W | recomputed from `models/library/analyses/mfe_cryo_inventory.sysml:10-17` with `models/designs/stellarator_09/stellarator_plant.sysml` cryoplant values (c_coil 25.0 m, wp_side 0.36, t_case 0.10, ε 0.05, σ, q_MLI 1.0, area ratio 1.2, g 0.04, k_c 5.39362701769, k_s 12.12875814211) |
| L0 | 2.45e−8 W Ω K⁻² | model cryoplant.L0; Ballarino |
| Green laws | η = 0.155·R^0.23; C = 3.1·R^0.65 M$2015; fit data 0.01–35 kW | contract § 6; check B § 4 |
| 77 K stage | fraction of Carnot 0.20 | contract § 6; model f_carnot_shield |
| CPI | 2015 237.0, 2021 271.0 (×1.14346) | `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md:731, :773` |
| Densities, prices | Cu 8940, steel 8000, solder 8390 kg/m³; Cu 11, steel 6, solder 64.4411 USD/kg | `stellarator_plant.sysml:380-396` (A16) |
| Element density | 8900 kg/m³ both | [AGENT] (A5) |
| Conductor prices | Nb₃Sn 8 (5.4, 13.5); REBCO 80 (30, 10) USD/m | contract § 7 (A18) |
| Economics | crf 0.08, availability 0.8, 60 USD/MWh, 8760 h | contract § 7 |

The anchor S inventory reconstructs the model's 21,933.902368719853 W rating to the last digit, and the intercept terms reconstruct 41,599.953939961626 W exactly.

## Offer policy as implemented

- **Element count.** The smallest integer n whose oracle acceptance margin is ≥ 0, found by stepping from ⌊I/Ic_rule⌋ − 2 and confirming that n − 1 fails. Support status is ignored here so that unsupported points still get an offer to evaluate (A12).
- **Areas.** Each construction-rule area at the offer's own duty, computed in double precision and rounded up to the next 1e−6 mm² with a float guard (design D1). Reference copper and steel margins lie in [0, 1e−6] mm² ("at allowance"). The margin is exactly 0 where the rule copper is 0 (very large Nb₃Sn counts whose strand copper already exceeds I/J).
- **Rating.** The smallest listed rating ≥ q_cold of the offer; the next lower one is the insufficient refrigerator.
- **Insufficient and generous.** ⌊0.9 n⌋ = (9n)//10 and ⌈1.2 n⌉ = (12n + 9)//10 in integers. Both keep the reference areas and rating (A9).
- **Variants.** Re-evaluated reference: the offer quantities (n, cabling factor, void, the four areas, insulation fraction, rating) are copied from the base reference offer, and every assumption input takes the variant's value. Variant offer: the policy reruns under the variant's assumptions.

## Case set

2832 cases, all carrying every § 6 input plus `labels` (anchor, B_peak, point_class, pairing, rule_family, variant, offer_kind, refrigerator_kind) and a `policy` trace block that is not a model input.

- **Base grid, 576 cases.** 16 anchor-field points (D: 8–13, 14, 16, 18, 20 T; S: 8–13 T) × 3 pairings × 3 rule families × 4 kinds (reference; insufficient elements; generous elements; reference elements with the insufficient refrigerator).
- **Variants, 2256 cases.** 36 one-at-a-time variants at the reference rule family and the common-P and native pairings only, each as a re-evaluated reference and a variant offer. The two anchor D turn-length variants run on anchor D only.
- **By offer kind.** reference 1416 (144 base, 144 base with the insufficient refrigerator, 1128 re-evaluated under variants), insufficient 144, generous 144, variant-offer 1128. By refrigerator kind: reference 2688, insufficient 144.
- **By pairing and family.** common-P 1320, native 1320, common-C 192; reference family 2448, both-temperature 192, both-fraction 192. By point class: matched 1760, edge 352, extension 720.
- **Duplicates.** 506 variant offers equal their reference offer (economics-only variants such as prices, electricity, crf, manufacturing and η or capital basis). They are kept and flagged `identical_to_reference_offer`.
- **Carried offers.** 6 Nb₃Sn variant offers carry the reference offer: −0.6 % strain at 20 T for WST, OST TFEU9 and BEAS TFEU10-12, in both pairings. Bc2(6.7 K) is below 20 T there, so no element count meets the rule (A12).
- **Exhausted rating list.** 8 material offers exceed the list: cold-load ×2 at anchor D 18 and 20 T, demand 75.8–82.0 kW. They are offered 75 kW and fail capacity (A13).
- **Knife edges.** The smallest generated acceptance margin among supported offers is 1.0e−5 (REBCO fraction) and 2.7e−5 K (Nb₃Sn temperature). Among unsupported offers it is 4.8e−7 K. The smallest area round-up is 0. No verdict sits within the 1e−9 agreement tolerance.

**Coordinator cross-check.** At anchor D, 10 T, common-P, my reference offers equal `reference-case.json` field for field: n 438 and 342, all areas to 1e−6 mm², 30 kW ratings. The one difference is anchor D `shield_static`: 1,102.0 kW here against 1,107.9 kW there (A6). The coordinator's q_cold agrees to 3e−11 relative; the gap comes from its trapezoid K integral.

## Contract and design ambiguities (flagged, resolved as stated)

- **A1. Ic zero condition.** Design § 2.1 says Ic_strand is zero unless 0 < t < 1. Read literally, that makes Ic(B, 0) = 0, so the Tcs guard "n·Ic(B, 0) < I" fires in every case and Tcs is never defined. The oracle uses 0 ≤ t < 1. The implementer must do the same, or every case differs.
- **A2. Construction C precision.** The contract prints C per kA to 4 significant figures (2.945, 1.010, 0.673, 3.030). Those values miss Table 7 by 1.3–3.7e−4 relative, so the 1e−6 anchor test cannot pass with them. The oracle uses the unrounded calibration (fractions × 420.779 mm²/50 kA), which rounds to the printed values. The contract also does not state C's cabling factor, cable void, copper void or insulation. The oracle uses 1, 0, 0 and 0 because Table 7 lists tape and helium areas directly. Helium goes into `misc_area`. For Nb₃Sn on C (common-C) round strands get the same treatment, with no packing factor; the common-C pairing is hypothetical anyway.
- **A3. Which temperature is checked against the law domain.** The design does not say. The oracle checks T_conductor. No case in the set depends on the choice.
- **A4. Steel and solder mass.** "Steel_mass and solder_mass likewise" is read as area × length × density without the copper void, since neither has a void input.
- **A5. Element density.** No source is given for strand or tape density. 8900 kg/m³ is used for both [AGENT]. It affects only the reported superconductor mass, never cost.
- **A6. Anchor D intercept static load (contract silent).** The oracle uses Končar Table 1 shields only: VVTS 912.6 + CTS 189.4 = 1,102.0 kW. The 1,107.9 kW used by `reference-case.json`, and labelled the shield total in `evidence/sources/cryo-loads.md:27`, is the table's all-component total. It includes the 5.9 kW magnet load that the cold stage already counts as 1.3 + 4.6 kW, so it double-counts. The load is equal for both materials, so no verdict, difference or break-even changes. Each material's p_in_shield and annualized cost fall by the same amount.
- **A7. Anchor S turn length.** The brief says 21.75 m. The oracle uses the model quotient 321,600.0/(48 × 308) = 21.753247 m, since the replay record gives conductor_length as exactly 321,600.0. The two differ by 0.015 %. The brief's 266.6 W radiation is my 266.681 W truncated.
- **A8. Turn-length variant.** Anchor D cold volume is defined as coils × pack area × turn length (contract § 6), so the 45 and 60 m variants also scale the nuclear load. Re-evaluated reference offers therefore see a changed cold demand.
- **A9. Generous offer areas.** The contract says "same component areas" only for the insufficient offer. The policy uses the reference areas for the generous offer too, so only n differs.
- **A10. Green η(18 kW).** The contract states 30.2 %, but 15.5 × 18^0.23 = 30.13 %. The test checks the formula to 1e−9, as the contract's bracket says.
- **A11. green_extrapolated with constant η.** eta_mode 1 has no efficiency argument, so only the capital argument is checked.
- **A12. Offers at unsupported points.** Acceptance requires support, so "smallest n meeting the acceptance rule" does not exist there. The policy uses the rule margin alone. Where even that is impossible (zero Ic at the rule point), the reference offer is carried and labelled `carried-reference`.
- **A13. Rating list exhausted.** The fixed list stops at 75 kW. Where demand exceeds it, the policy offers 75 kW and flags `rating_list_exhausted`; the offer fails capacity.
- **A14. Layer-1 steel variant.** The contract text says 9.36 mm²/kA. The oracle uses the exact layer-1 value 982.7/104.95 = 9.3635, which is the value the contract's own anchor test uses.
- **A15. Variant scope.** The steel-base variants apply to construction P only. The no-field-scaling variant applies to both P and C, since both scale steel with B. The copper-density variants act only on P, because C sets copper per kA.
- **A16. Price year.** The contract says to use the model's existing material prices. The model documents them as 2026-era (price_solder explicitly 2026 USD), while the comparison currency is 2021 USD. They are used unconverted, as instructed.
- **A17. REBCO anchor.** 1.13 × 175 = 197.75 A; the contract's 198 A is used.
- **A18. Printed sensitivity levels used as declared.** Nb₃Sn 5.4 USD/m against the law-derived 8.0 × 0.68048 = 5.44; manufacturing 1128 USD/m against 985 × 271.0/236.7 = 1127.75.
- **A19. Anchor D conduction reference temperature.** 4 K, from Končar's 4 K magnets (not 4.5 K). K(4)/K(4.5) = 1.00045.
- **A20. REBCO tcs_defined.** The design lists the REBCO outputs "as § 2.1". The oracle returns tcs_defined = 1 whenever the closed-form log argument is positive, which holds in every case.
- **A21. Strain sensitivity carries a grade effect.** At −0.6 % the WST strand ranks 3rd of 10, not at the median (61.2 A against a median of 73.1 A). The upper and lower production sets are therefore also run at −0.6 %, as contract § 3 asks.
