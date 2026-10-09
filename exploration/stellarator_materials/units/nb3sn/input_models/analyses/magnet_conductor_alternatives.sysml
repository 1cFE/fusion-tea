package magnet_conductor_alternatives {
    doc /* Concept-agnostic calculation and constraint definitions for comparing two supplied superconducting windings (an Nb3Sn strand cable and a REBCO tape cable) at one supplied magnetic duty. Every calculation evaluates a supplied design: no calculation writes a supplied quantity, no output is bound back as an input, and nothing sets an offer, area or rating from demand (MR-7). Library defaults are neutral (zero or unit); concept values live in models/designs/. Units: currents A, fields T, temperatures K, areas mm2 unless named, lengths m, masses kg, powers W unless named, money USD2021. Numerical semantics of every calc def are the complete calculate function in its handwritten body under exploration/magnet_materials/bodies/magnet_conductor_alternatives/. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: sections 2 and 4 (equations, MR-7 role record); governing contract work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md (r3) sections 2-7. **Basis**: [AGENT] reviewed design (contract-review.md, Recheck r3 and design review; D1-D7 recheck PASS). **Last Updated**: 2026-09-29 */
    private import ScalarValues::*;

    calc def 'Nb3Sn Cable Critical Surface' {
        doc /* ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi 2017 Table III form with C1 in A*T per whole strand), evaluated at the supplied strand count, turn current, peak field and conductor temperature. eps_sh = Ca2*eps0a/sqrt(Ca1^2 - Ca2^2); s(eps) = 1 + [Ca1(sqrt(eps_sh^2 + eps0a^2) - sqrt((eps - eps_sh)^2 + eps0a^2)) - Ca2*eps]/(1 - Ca1*eps0a); Tc* = Tc0*s^(1/3); t = T/Tc*; Bc2* = Bc20*s*(1 - t^1.52); b = B/Bc2*; Ic_strand = (C1/B)*s*(1 - t^1.52)*(1 - t^2)*b^p*(1 - b)^q for t < 1 and 0 < b < 1, else 0; Ic_cable = n*Ic_strand. T_conductor = T_supply + nuclear_rise. T_cs solves n*Ic_strand(B, T_cs) = I by bisection on [0, T_zero] (b = 1 at T_zero) to 1e-10 K; if n*Ic_strand(B, 0) < I then T_cs = 0 and tcs_defined = 0. Temperature rule margin = T_cs - (T_supply + nuclear_rise + margin_rise); fraction rule margin = fraction_rule - I/Ic_cable; acceptance_rule selects 0 temperature or 1 fraction. status_code: 1 supported (B <= B_design_max), 2 edge (B <= B_edge_max), 3 law-only (B <= B_law_max), 0 unsupported (B outside [B_law_min, B_law_max], T_conductor outside [T_law_min, T_law_max] or eps_intrinsic outside [eps_min, eps_max]). Unsupported evaluations are reported with status 0 and acceptance_pass 0, never as a pass. Strain enters as a fraction. eps_intrinsic_in is the last input so that a design may leave it unbound (usage parameters redefine definition parameters by position); a negative design literal would otherwise generate as a non-overridable constant. Areas: element_area_total = n*(pi/4)*d^2*1e6 mm2; element_copper_area = strand_copper_fraction*element_area_total. **Source**: knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/raw.pdf; knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf **Reference**: Tsui & Hampshire 2012 eq. (6)-(7), printed p.7 (PDF p.8); Breschi et al. 2017 Table III, PDF p.24 (images/tmpniti0z1h.pdf-0024-01.png); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.1; contract section 3. **Basis**: law form directly supported; evaluation at 5.2-6.7 K is temperature interpolation of a fitted law (contract section 2 support wording). The T >= 0 bound: the design's T_cs bracket evaluates Ic at T = 0, so the law is applied on 0 <= t < 1 (see implementation-notes.md). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29 */
        in attribute n_strands_in : Real default := 0.0;
        in attribute strand_diameter_in : Real default := 0.0;
        in attribute strand_copper_fraction_in : Real default := 0.0;
        in attribute turn_current_in : Real default := 0.0;
        in attribute B_peak_in : Real default := 0.0;
        in attribute T_supply_in : Real default := 0.0;
        in attribute nuclear_rise_in : Real default := 0.0;
        in attribute margin_rise_in : Real default := 0.0;
        in attribute p_in : Real default := 0.0;
        in attribute q_in : Real default := 0.0;
        in attribute C1_in : Real default := 0.0;
        in attribute Ca1_in : Real default := 0.0;
        in attribute Ca2_in : Real default := 0.0;
        in attribute eps0a_in : Real default := 0.0;
        in attribute Bc20_in : Real default := 0.0;
        in attribute Tc0_in : Real default := 0.0;
        in attribute fraction_rule_in : Real default := 0.0;
        in attribute acceptance_rule_in : Real default := 0.0;
        in attribute B_law_min_in : Real default := 0.0;
        in attribute B_law_max_in : Real default := 0.0;
        in attribute B_design_max_in : Real default := 0.0;
        in attribute B_edge_max_in : Real default := 0.0;
        in attribute T_law_min_in : Real default := 0.0;
        in attribute T_law_max_in : Real default := 0.0;
        in attribute eps_min_in : Real default := 0.0;
        in attribute eps_max_in : Real default := 0.0;
        in attribute eps_intrinsic_in : Real default := 0.0;
        out attribute T_conductor : Real;
        out attribute ic_strand_op : Real;
        out attribute ic_cable_op : Real;
        out attribute operating_fraction : Real;
        out attribute T_cs : Real;
        out attribute tcs_defined : Real;
        out attribute temperature_margin : Real;
        out attribute temp_rule_margin : Real;
        out attribute fraction_rule_margin : Real;
        out attribute acceptance_margin : Real;
        out attribute status_code : Real;
        out attribute supported : Real;
        out attribute acceptance_pass : Real;
        out attribute element_area_total : Real;
        out attribute element_copper_area : Real;
    }

    calc def 'REBCO Cable Critical Surface' {
        doc /* REBCO tape critical current at the supplied tape count, turn current, peak field and conductor temperature. Field shape g(B): shape_mode 0 interpolates log-log between the measured 20 K, B||c knots g8, g10, g12, g15, g20 at 8, 10, 12, 15, 20 T (defined only on [8, 20] T; NaN outside, since no knot interval exists there); shape_mode 1 is the power law (B/20)^-alpha. Ic_tape(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star); Ic_cable = n*degradation*Ic_tape; T_cs = 20 + T_star*ln(n*degradation*anchor_ic*g(B)/I) (closed form). Rule margins, acceptance selection and area outputs as in 'Nb3Sn Cable Critical Surface'; element_area_total = n*w*t*1e6 mm2 and element_copper_area = tape_copper_fraction*element_area_total. status_code 1 when B lies in the active shape's supported range ([B_knot_min, B_knot_max] for shape 0, [B_law_min, B_law_max] for shape 1) and T_conductor lies in [T_law_min, T_law_max]; otherwise 0 (unsupported). REBCO has no edge or law-only band. **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf; knowledge/sources/field_and_temperature_scaling_of_the_critical_current/raw.pdf **Reference**: Molodyk et al. 2021 Fig. 1a (raw.pdf p.3), output.md:77, :93, :137; Senatore et al. 2016 eq. (1), raw.pdf p.6, validity output.md:94; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.2; contract section 3. **Basis**: measured 20 K shape digitized twice (check-rebco-cryo-cost.md section 1); Senatore exponential temperature form; field perpendicular to the tape face assumed everywhere. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29 */
        in attribute n_tapes_in : Real default := 0.0;
        in attribute tape_width_in : Real default := 0.0;
        in attribute tape_thickness_in : Real default := 0.0;
        in attribute tape_copper_fraction_in : Real default := 0.0;
        in attribute turn_current_in : Real default := 0.0;
        in attribute B_peak_in : Real default := 0.0;
        in attribute T_supply_in : Real default := 0.0;
        in attribute nuclear_rise_in : Real default := 0.0;
        in attribute margin_rise_in : Real default := 0.0;
        in attribute anchor_ic_in : Real default := 0.0;
        in attribute shape_mode_in : Real default := 0.0;
        in attribute g8_in : Real default := 1.0;
        in attribute g10_in : Real default := 1.0;
        in attribute g12_in : Real default := 1.0;
        in attribute g15_in : Real default := 1.0;
        in attribute g20_in : Real default := 1.0;
        in attribute alpha_in : Real default := 0.0;
        in attribute T_star_in : Real default := 1.0;
        in attribute degradation_in : Real default := 1.0;
        in attribute fraction_rule_in : Real default := 0.0;
        in attribute acceptance_rule_in : Real default := 0.0;
        in attribute B_knot_min_in : Real default := 0.0;
        in attribute B_knot_max_in : Real default := 0.0;
        in attribute B_law_min_in : Real default := 0.0;
        in attribute B_law_max_in : Real default := 0.0;
        in attribute T_law_min_in : Real default := 0.0;
        in attribute T_law_max_in : Real default := 0.0;
        out attribute T_conductor : Real;
        out attribute ic_tape_op : Real;
        out attribute ic_cable_op : Real;
        out attribute operating_fraction : Real;
        out attribute T_cs : Real;
        out attribute tcs_defined : Real;
        out attribute temperature_margin : Real;
        out attribute temp_rule_margin : Real;
        out attribute fraction_rule_margin : Real;
        out attribute acceptance_margin : Real;
        out attribute status_code : Real;
        out attribute supported : Real;
        out attribute acceptance_pass : Real;
        out attribute element_area_total : Real;
        out attribute element_copper_area : Real;
    }

    calc def 'Winding Turn Area Screen' {
        doc /* Sums the supplied per-turn component areas and compares the gross area with the envelope; separately computes the allowance-rule requirements at the evaluated duty and compares them with the supplied areas. It never resizes an area. cable = element_area/cabling_factor/(1 - cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 - ins_fraction); fit_margin = available_area - gross; fit_margin_fraction = fit_margin/available_area; required_envelope_J = I/gross (A/mm2). Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule - element_copper_area)/(1 - cu_void), else cu_required = cu_per_kA_rule*I/1000. Steel rule: steel_required = steel_per_kA_rule*(I/1000)*(B/B_steel_ref if steel_B_scaling = 1, else 1). Margins are supplied minus required; pass flags are 1 when the margin is >= 0. Protection and structural adequacy are allowance rules, not evaluated physics. **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf; knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png **Reference**: Demattè & Bruzzone Table I and pp.2-4 (output.md:106, :139); Stellaris Table 7; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.3; contract section 4 (constructions P and C). **Basis**: [AGENT] allowance-rule construction calibrated to reproduce EU DEMO layer 1 and Stellaris Table 7; scaling steel with B at fixed geometry is a bounded assumption. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_turn_area_screen_impl.py. **Last Updated**: 2026-09-29 */
        in attribute turn_current_in : Real default := 0.0;
        in attribute B_peak_in : Real default := 0.0;
        in attribute available_area_in : Real default := 0.0;
        in attribute element_area_in : Real default := 0.0;
        in attribute element_copper_area_in : Real default := 0.0;
        in attribute cabling_factor_in : Real default := 1.0;
        in attribute cable_void_in : Real default := 0.0;
        in attribute cu_space_in : Real default := 0.0;
        in attribute steel_area_in : Real default := 0.0;
        in attribute misc_area_in : Real default := 0.0;
        in attribute solder_area_in : Real default := 0.0;
        in attribute ins_fraction_in : Real default := 0.0;
        in attribute J_cu_rule_in : Real default := 0.0;
        in attribute cu_void_in : Real default := 0.0;
        in attribute cu_per_kA_rule_in : Real default := 0.0;
        in attribute steel_per_kA_rule_in : Real default := 0.0;
        in attribute B_steel_ref_in : Real default := 1.0;
        in attribute steel_B_scaling_in : Real default := 0.0;
        out attribute cable_area : Real;
        out attribute net_area : Real;
        out attribute gross_area : Real;
        out attribute fit_margin : Real;
        out attribute fit_margin_fraction : Real;
        out attribute required_envelope_J : Real;
        out attribute cu_required : Real;
        out attribute cu_margin : Real;
        out attribute steel_required : Real;
        out attribute steel_margin : Real;
        out attribute fit_pass : Real;
        out attribute cu_pass : Real;
        out attribute steel_pass : Real;
    }

    calc def 'Winding Inventory and Cost' {
        doc /* Inventory and cost of the supplied winding; never from demand. conductor_length = turns*coils*turn_length; element_length = n_elements*conductor_length; element_mass = element_area*1e-6*conductor_length*element_density (element_area is the total element area per turn, mm2); cu_mass = cu_space*(1 - cu_void)*1e-6*conductor_length*rho_cu; steel_mass = steel_area*1e-6*conductor_length*rho_steel; solder_mass = solder_area*1e-6*conductor_length*rho_solder; sc_cost = element_length*element_price_per_m; materials_cost = cu_mass*price_cu + steel_mass*price_steel + solder_mass*price_solder; manufacturing_cost = conductor_length*manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost; ampere_metres = turn_current*conductor_length. Cabling twist is ignored (contract section 7). **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.4; contract section 7 (cost accounting and boundary). **Basis**: [AGENT] partial accounting within the evaluated categories; winding labour, heat treatment, stacking, case and structure excluded (contract section 7). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py. **Last Updated**: 2026-09-29 */
        in attribute n_elements_in : Real default := 0.0;
        in attribute element_area_in : Real default := 0.0;
        in attribute element_density_in : Real default := 0.0;
        in attribute turns_in : Real default := 0.0;
        in attribute coils_in : Real default := 0.0;
        in attribute turn_length_in : Real default := 0.0;
        in attribute turn_current_in : Real default := 0.0;
        in attribute cu_space_in : Real default := 0.0;
        in attribute cu_void_in : Real default := 0.0;
        in attribute steel_area_in : Real default := 0.0;
        in attribute solder_area_in : Real default := 0.0;
        in attribute rho_cu_in : Real default := 0.0;
        in attribute rho_steel_in : Real default := 0.0;
        in attribute rho_solder_in : Real default := 0.0;
        in attribute price_cu_in : Real default := 0.0;
        in attribute price_steel_in : Real default := 0.0;
        in attribute price_solder_in : Real default := 0.0;
        in attribute element_price_per_m_in : Real default := 0.0;
        in attribute manufacturing_per_m_in : Real default := 0.0;
        out attribute conductor_length : Real;
        out attribute element_length : Real;
        out attribute element_mass : Real;
        out attribute cu_mass : Real;
        out attribute steel_mass : Real;
        out attribute solder_mass : Real;
        out attribute sc_cost : Real;
        out attribute materials_cost : Real;
        out attribute manufacturing_cost : Real;
        out attribute winding_capital : Real;
        out attribute ampere_metres : Real;
    }

    calc def 'Magnet Cold Stage Load' {
        doc /* Cold-stage and 77 K intercept loads at the supply temperature. K(T) = integral from T to T_shield of k_316 dT, with log10 k = sum_i c_i*(log10 T)^i over the NIST coefficients k_a..k_i (i = 0..8), integrated by composite Simpson over 2000 intervals in ln T. q_conduction = conduction_ref*K(T_supply)/K(T_conduction_ref); q_radiation = radiation_ref (temperature-independent from the 77 K shield); q_nuclear = nuclear_density*cold_volume; q_leads = f_lead*n_leads*|I|*sqrt(L0*(T_shield^2 - T_supply^2)); q_joints = p_joint_ref*(I/I_joint_ref)^2; q_cold = load_multiplier*(q_nuclear + q_radiation + q_conduction + q_leads + q_joints); q_shield = shield_static + f_lead*n_leads*|I|*sqrt(L0*(T_amb^2 - T_shield^2)); k_integral = K(T_supply) in W/m. Circulator work, helium inventory and AC losses are excluded (contract section 6). **Source**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md; knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/; knowledge/sources/koncar_et_al_2017_heat_loads_and_design_temperature/ **Reference**: NIST 316 conductivity fit coefficients a-i (output.md:24-32, data range 4-300 K); Ballarino slide 14 minimum-heat-leak form; Končar Eq. 1 and Table 1 (PDF pp.3-5); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.5; contract section 6. **Basis**: [AGENT] staged static and nuclear cold-load inventory; resistive-lead optimum applied equally to both materials. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/magnet_cold_stage_load_impl.py. **Last Updated**: 2026-09-29 */
        in attribute T_supply_in : Real default := 0.0;
        in attribute T_shield_in : Real default := 0.0;
        in attribute T_amb_in : Real default := 0.0;
        in attribute turn_current_in : Real default := 0.0;
        in attribute nuclear_density_in : Real default := 0.0;
        in attribute cold_volume_in : Real default := 0.0;
        in attribute radiation_ref_in : Real default := 0.0;
        in attribute conduction_ref_in : Real default := 0.0;
        in attribute T_conduction_ref_in : Real default := 0.0;
        in attribute k_a_in : Real default := 0.0;
        in attribute k_b_in : Real default := 0.0;
        in attribute k_c_in : Real default := 0.0;
        in attribute k_d_in : Real default := 0.0;
        in attribute k_e_in : Real default := 0.0;
        in attribute k_f_in : Real default := 0.0;
        in attribute k_g_in : Real default := 0.0;
        in attribute k_h_in : Real default := 0.0;
        in attribute k_i_in : Real default := 0.0;
        in attribute n_leads_in : Real default := 0.0;
        in attribute f_lead_in : Real default := 1.0;
        in attribute L0_in : Real default := 0.0;
        in attribute p_joint_ref_in : Real default := 0.0;
        in attribute I_joint_ref_in : Real default := 1.0;
        in attribute shield_static_in : Real default := 0.0;
        in attribute load_multiplier_in : Real default := 1.0;
        out attribute q_nuclear : Real;
        out attribute q_radiation : Real;
        out attribute q_conduction : Real;
        out attribute q_leads : Real;
        out attribute q_joints : Real;
        out attribute q_cold : Real;
        out attribute q_shield : Real;
        out attribute k_integral : Real;
    }

    calc def 'Staged Refrigeration Screen' {
        doc /* Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage rating compared with the calculated cold load. carnot = (T_amb - T_supply)/T_supply; carnot_ref = (T_amb - T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv_kW = rating_cold/1000*(equiv_factor if capital_mode = 0, else 1); eta_cold = green_a*R_eta^green_b with R_eta = rating_cold/1000 (eta_mode 0) or rating_cold/1000*equiv_factor (eta_mode 2), or eta_const (eta_mode 1); p_in_cold = q_cold*carnot/eta_cold; p_in_shield = q_shield*(T_amb - T_shield)/T_shield/f_carnot_shield; p_in_total_MW = (p_in_cold + p_in_shield)/1e6; refrigerator_capital = green_c*R_equiv_kW^green_d*usd2015_to_2021. Efficiency is a property of the installed plant evaluated at its rating and applied to the operating load (part-load penalty not modeled). capacity_margin = rating_cold - q_cold; capacity_pass = 1 when >= 0. green_extrapolated = 1 when R_equiv_kW, or R_eta when a Green efficiency mode is active, lies outside Green's fitted data [0.01, 35] kW. **Source**: knowledge/sources/green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher/; knowledge/sources/strobridge_1974_cryogenic_refrigerators_an_updated_survey/ **Reference**: Green 2015 Eq. 1 and Eq. 2, printed p.2 (PDF p.3); Strobridge 1974 Eq. 1 (printed p.2), Fig. 1 and pp.4-6 (percent of Carnot independent of temperature band); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.6; contract section 6. **Basis**: [AGENT] one efficiency law for both temperatures at the installed capacity; 20 K capital by input-power equivalence (factor (300-20)/20 / ((300-4.5)/4.5) = 0.2132) per check-rebco-cryo-cost.md Recheck r2. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py. **Last Updated**: 2026-09-29 */
        in attribute q_cold_in : Real default := 0.0;
        in attribute T_supply_in : Real default := 0.0;
        in attribute q_shield_in : Real default := 0.0;
        in attribute T_shield_in : Real default := 0.0;
        in attribute T_amb_in : Real default := 0.0;
        in attribute rating_cold_in : Real default := 0.0;
        in attribute eta_mode_in : Real default := 0.0;
        in attribute eta_const_in : Real default := 0.0;
        in attribute green_a_in : Real default := 0.0;
        in attribute green_b_in : Real default := 0.0;
        in attribute f_carnot_shield_in : Real default := 1.0;
        in attribute capital_mode_in : Real default := 0.0;
        in attribute green_c_in : Real default := 0.0;
        in attribute green_d_in : Real default := 0.0;
        in attribute T_green_in : Real default := 0.0;
        in attribute usd2015_to_2021_in : Real default := 1.0;
        out attribute carnot_specific_power : Real;
        out attribute eta_cold : Real;
        out attribute p_in_cold : Real;
        out attribute p_in_shield : Real;
        out attribute p_in_total_MW : Real;
        out attribute R_equiv_kW : Real;
        out attribute refrigerator_capital : Real;
        out attribute capacity_margin : Real;
        out attribute capacity_pass : Real;
        out attribute green_extrapolated : Real;
    }

    calc def 'Subsystem Annualized Cost' {
        doc /* capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW*hours*availability*electricity_price (USD/MWh); annualized_cost = crf*capital_total + annual_electricity. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.7; contract section 7. **Basis**: [AGENT] capital recovery factor and electricity price are case inputs; partial accounting within the evaluated categories. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py. **Last Updated**: 2026-09-29 */
        in attribute winding_capital_in : Real default := 0.0;
        in attribute refrigerator_capital_in : Real default := 0.0;
        in attribute p_in_total_MW_in : Real default := 0.0;
        in attribute crf_in : Real default := 0.0;
        in attribute hours_in : Real default := 0.0;
        in attribute availability_in : Real default := 0.0;
        in attribute electricity_price_in : Real default := 0.0;
        out attribute capital_total : Real;
        out attribute annual_electricity : Real;
        out attribute annualized_cost : Real;
    }

    calc def 'Matched Pair Comparison' {
        doc /* Compares the two supplied windings at one duty. rankable = all_pass_nb3sn*all_pass_rebco, where each all_pass = acceptance_pass*fit_pass*cu_pass*steel_pass*capacity_pass (acceptance_pass already requires a supported status); pair_status = status_nb3sn when both statuses are supported (non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; breakeven_rebco_price_per_m = rebco_price_per_m - cost_difference/(crf*rebco_element_length); breakeven_rebco_price_per_kAm = breakeven_rebco_price_per_m/(rebco_ic_tape_op/1000), per kA*m of tape critical current at the operating field and conductor temperature. Break-even prices are reported for every pair but are meaningful only when rankable = 1. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.8 (D2, D7); contract sections 7-8. **Basis**: [AGENT] cost is linear in the REBCO price per metre, so the break-even price follows from recorded outputs. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/matched_pair_comparison_impl.py. **Last Updated**: 2026-09-29 */
        in attribute annualized_nb3sn_in : Real default := 0.0;
        in attribute annualized_rebco_in : Real default := 0.0;
        in attribute all_pass_nb3sn_in : Real default := 0.0;
        in attribute all_pass_rebco_in : Real default := 0.0;
        in attribute status_nb3sn_in : Real default := 0.0;
        in attribute status_rebco_in : Real default := 0.0;
        in attribute rebco_element_length_in : Real default := 1.0;
        in attribute rebco_price_per_m_in : Real default := 0.0;
        in attribute rebco_ic_tape_op_in : Real default := 1.0;
        in attribute crf_in : Real default := 1.0;
        out attribute rankable : Real;
        out attribute pair_status : Real;
        out attribute cost_difference : Real;
        out attribute breakeven_rebco_price_per_m : Real;
        out attribute breakeven_rebco_price_per_kAm : Real;
    }

    constraint def 'Conductor Acceptance' {
        doc /* The conductor evaluation is supported (supported >= 1) and the selected margin rule holds (acceptance_margin >= 0). An unsupported evaluation makes this constraint violated; the separate supported and status_code outputs distinguish unsupported from failed, as in the 'Offered Equipment Capacity' pattern (models/library/analyses/mfe_viability.sysml:119). No physical tolerance. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.9. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-29 */
        in attribute supported_in : Real;
        in attribute margin_in : Real;
        supported_in >= 1.0 and margin_in >= 0.0
    }

    constraint def 'Winding Fit' {
        doc /* Envelope area per turn minus the gross area of the supplied components is nonnegative. A design that does not fit is not a winding at this duty and receives no ranking. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.9; contract section 2. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-29 */
        in attribute fit_margin_in : Real;
        fit_margin_in >= 0.0
    }

    constraint def 'Protection Copper Allowance' {
        doc /* Supplied stabilizer copper space minus the allowance-rule requirement at the evaluated duty is nonnegative. An allowance rule, not an evaluated quench analysis. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.9; contract section 4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-29 */
        in attribute cu_margin_in : Real;
        cu_margin_in >= 0.0
    }

    constraint def 'Structural Steel Allowance' {
        doc /* Supplied structural steel area minus the allowance-rule requirement at the evaluated duty is nonnegative. An allowance rule, not an evaluated stress analysis. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.9; contract section 4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-29 */
        in attribute steel_margin_in : Real;
        steel_margin_in >= 0.0
    }

    constraint def 'Refrigerator Capacity' {
        doc /* Installed cold-stage rating minus the calculated cold-stage load is nonnegative. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.9; contract section 6. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-29 */
        in attribute capacity_margin_in : Real;
        capacity_margin_in >= 0.0
    }
}
