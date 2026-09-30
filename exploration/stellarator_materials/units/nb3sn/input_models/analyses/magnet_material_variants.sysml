package magnet_material_variants {
    doc /* Plant-level conductor material variants for the MFE plant (WI-100): two magnet-system variants that evaluate a supplied Nb3Sn strand winding or a supplied REBCO tape winding with Round 1's conductor law, turn-area screen and inventory calcs at the plant's own supply temperature, and one cryoplant variant that carries Round 1's cold-stage load and staged refrigeration into the plant's recirculating power and capital. Every calculation evaluates a supplied design: no calculation writes a supplied quantity, no output is bound back as an input, and nothing sets an offer, area, count or rating from demand (MR-7). Library defaults are neutral (zero or unit); concept values are bound in the materials design files. The variants rebind only the plant's swap seams (declared default); every other plant calculation is inherited unchanged. Units: currents A, fields T, temperatures K, lengths m, areas mm2 per turn unless named, powers W unless named, money in the plant's mixed-year dollars except Round 1 conductor prices and the refrigerator capital (USD2021). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: sections 2.1-2.9; governing contract work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md (r4) sections 3-7. **Basis**: [AGENT] reviewed design (evidence/design-review-wi100.md, PASS WITH CORRECTIONS and Recheck). **Last Updated**: 2026-09-30 */
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_plant_systems::*;
    private import magnet_conductor_alternatives::*;

    // ------------------------------------------------------------------ glue calcs (design section 2.4)

    calc def 'Material Winding Adapter' {
        doc /* Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        in attribute reference_turns_in : Real default 1.0;
        in attribute f_set_in : Real default 0.0;
        in attribute c_coil_in : Real default 0.0;
        in attribute wp_side_in : Real default 0.0;
        out attribute turn_length : Real = f_set_in * c_coil_in;
        out attribute pack_area_per_turn : Real = wp_side_in * wp_side_in * 1e6 / reference_turns_in;
    }

    calc def 'Material Winding Cost' {
        doc /* One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        in attribute superconductor_cost_in : Real default 0.0;
        in attribute materials_cost_in : Real default 0.0;
        in attribute helium_cost_in : Real default 0.0;
        in attribute winding_operations_cost_in : Real default 0.0;
        out attribute cost : Real = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in;
    }

    calc def 'Pack Field Checks' {
        doc /* Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30 */
        in attribute B_peak_in : Real default 0.0;
        in attribute I_coil_in : Real default 0.0;
        in attribute R_in : Real default 0.0;
        in attribute wp_side_in : Real default 1.0;
        in attribute mu0_in : Real default 1.25663706212e-6;
        out attribute R_over_sqrt_A_wp : Real = R_in / wp_side_in;
        out attribute ampere_floor : Real = mu0_in * I_coil_in / (4.0 * wp_side_in);
        out attribute ampere_floor_margin : Real = B_peak_in - ampere_floor;
    }

    calc def 'REBCO Shape Branch' {
        doc /* Selects the REBCO field shape from the calculated peak field: shape_mode = 1.0 if B_peak_in > B_knot_max_in, else 0.0. Below and at the last knot the measured 20 K shape is used (knots 8-20 T), above it the power-law continuation, which is continuous at 20 T because g20 = 1 = (20/20)^-alpha. The conditional is completed by the handwritten body exploration/stellarator_materials/bodies/magnet_material_variants/rebco_shape_branch_impl.py: the codegen exact route refuses an if expression (probe P4, work/active/WI-100_stellarator-material-variants/prototype/P4-conditional-calc.md). **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md **Reference**: contract r4 section 4 (REBCO status bands); WI-100 design section 2.4 and D15. **Basis**: [AGENT] reviewed design; shape_mode becomes calculated, not supplied (design section 4 call-out). **Last Updated**: 2026-09-30 */
        in attribute B_peak_in : Real default 0.0;
        in attribute B_knot_max_in : Real default 0.0;
        out attribute shape_mode : Real;
    }

    calc def 'Staged Static Loads' {
        doc /* The plant's own static cold and intercept terms, evaluated for Round 1's cold-stage load without the 10-30 K guard of the plant's thermal-inventory body. area_cold = n_coils_in * c_coil_in * 4 * (wp_side_in + 2 * t_case_in) (m2); q_radiation = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in^4 - T_cold_in^4) (W, at the design's cold temperature); conduction_ref = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in) (W, support conduction on the k_c segment basis, which the cold-stage load scales by the NIST 316 integral ratio); shield_static = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref (W, the intercept's static load); p_joint_ref = p_fixed_MW_in * 1e6 (W, joint losses at the reference current). Nuclear heating of the cold mass (coordinator amendment A2): q_structure_nuclear = q_nuc_structure_in * m_support_in / rho_structure_in (W, the plant's structure-nuclear term, models/library/analyses/mfe_cryo_inventory.sysml 'Cold Load Sum'); nuclear_density_eff = q_nuc_in + q_structure_nuclear / vol_cold_in (W/m3 over the winding-pack cold volume), so the cold-stage load's nuclear term nuclear_density_eff * vol_cold equals the winding-pack term plus the structure term, and equals q_nuc * vol_cold exactly when q_nuc_structure is zero. At 20 K and the Stellaris design these reproduce the pinned inventory's 266.68 W radiation, 590.28 W conduction and 7,561.69 W intercept static load. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' equations, lines 11-16 (WI-059 D3-D4); WI-100 design section 2.4. **Basis**: [AGENT] reviewed design; plant equations reused unchanged. **Last Updated**: 2026-09-30 */
        in attribute n_coils_in : Real default 0.0;
        in attribute c_coil_in : Real default 0.0;
        in attribute wp_side_in : Real default 0.0;
        in attribute t_case_in : Real default 0.0;
        in attribute shield_area_ratio_in : Real default 1.0;
        in attribute eps_eff_in : Real default 0.0;
        in attribute sigma_SB_in : Real default 0.0;
        in attribute q_MLI_in : Real default 0.0;
        in attribute g_per_coil_in : Real default 0.0;
        in attribute k_c_in : Real default 0.0;
        in attribute k_s_in : Real default 0.0;
        in attribute T_cold_in : Real default 0.0;
        in attribute T_shield_in : Real default 77.0;
        in attribute T_amb_in : Real default 300.0;
        in attribute T_conduction_ref_in : Real default 0.0;
        in attribute p_fixed_MW_in : Real default 0.0;
        in attribute q_nuc_in : Real default 0.0;
        in attribute vol_cold_in : Real default 1.0;
        in attribute q_nuc_structure_in : Real default 0.0;
        in attribute m_support_in : Real default 0.0;
        in attribute rho_structure_in : Real default 1.0;
        out attribute area_cold : Real = n_coils_in * c_coil_in * 4.0 * (wp_side_in + 2.0 * t_case_in);
        out attribute q_radiation : Real = area_cold * eps_eff_in * sigma_SB_in * (T_shield_in ** 4 - T_cold_in ** 4);
        out attribute conduction_ref : Real = n_coils_in * g_per_coil_in * k_c_in * (T_shield_in - T_conduction_ref_in);
        out attribute shield_static : Real = shield_area_ratio_in * area_cold * q_MLI_in - q_radiation + n_coils_in * g_per_coil_in * k_s_in * (T_amb_in - T_shield_in) - conduction_ref;
        out attribute p_joint_ref : Real = p_fixed_MW_in * 1e6;
        out attribute q_structure_nuclear : Real = q_nuc_structure_in * m_support_in / rho_structure_in;
        out attribute nuclear_density_eff : Real = q_nuc_in + q_structure_nuclear / vol_cold_in;
    }

    calc def 'Staged Drive Power' {
        doc /* Lead and joint drive power of the staged cold load, in MW: p_drive = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6, with the cold-segment lead heat, the warm-segment lead heat (the intercept load less its static part) and the joint losses in W. It is the plant's drive definition on the staged loads and reproduces the pinned 0.0502673 MW at 20 K. **Source**: models/library/analyses/mfe_cryo_inventory.sysml **Reference**: 'Coil Thermal Inventory' p_drive, line 17; WI-100 design section 2.4. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        in attribute q_leads_in : Real default 0.0;
        in attribute q_shield_in : Real default 0.0;
        in attribute shield_static_in : Real default 0.0;
        in attribute q_joints_in : Real default 0.0;
        in attribute joint_drive_fraction_in : Real default 0.0;
        out attribute p_drive : Real = (q_leads_in + (q_shield_in - shield_static_in) + joint_drive_fraction_in * q_joints_in) * 1e-6;
    }

    constraint def 'Ampere Floor' {
        doc /* The modeled peak field is not below the exact Ampere floor of the pack: ampere_floor_margin >= 0. A violation is an impossible peak field and files the design as failed (contract section 7). **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md **Reference**: r4 sections 3.2 and 7 (correction C); evidence/check-field-relations.md Relation 1. **Basis**: [AGENT] reviewed design (WI-100 design section 2.4). **Last Updated**: 2026-09-30 */
        in attribute margin_in : Real;
        margin_in >= 0.0
    }

    // ------------------------------------------------------------------ magnet variants (design sections 2.5, 2.6)

    part def 'Nb3Sn Magnet System' :> 'Magnet System' {
        doc /* A supplied Nb3Sn strand-cable winding on the plant's coil set, evaluated with Round 1's ITER-form critical surface, turn-area screen and inventory at the plant's supply temperature (winding_pack.T_inventory, the cryoplant's T_cold_cryo). The plant REBCO law is gated off (rebco_law_enabled = 0) and the winding account seam is rebound to the one-basis winding cost; every other magnet calculation is the plant's. Asserts the conductor acceptance, the copper and steel allowances, the pack-area fit and the Ampere floor. Outside its bands the law reports status 0 with acceptance violated, never an exception; the study files such a design unsupported. Direct specialization only (a grandparent is not surfaced through an intermediate def, models/designs/stellarator_09/stellarator_plant.sysml:22-31). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.5; contract r4 sections 4-7; plant-chain-audit.md section 6 step 5. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        // Round 1 conductor definition (design section 6 names); bound by the instance with MR-4 docs.
        attribute n_elements : Real;
        attribute strand_diameter : Real;
        attribute strand_copper_fraction : Real;
        attribute p : Real;
        attribute q : Real;
        attribute C1 : Real;
        attribute Ca1 : Real;
        attribute Ca2 : Real;
        attribute eps0a : Real;
        attribute Bc20 : Real;
        attribute Tc0 : Real;
        attribute nuclear_rise : Real;
        attribute margin_rise : Real;
        attribute fraction_rule : Real;
        attribute acceptance_rule : Real;
        // law bounds
        attribute B_law_min : Real;
        attribute B_law_max : Real;
        attribute B_design_max : Real;
        attribute B_edge_max : Real;
        attribute T_law_min : Real;
        attribute T_law_max : Real;
        attribute eps_min : Real;
        attribute eps_max : Real;
        // supplied construction and allowance-rule inputs
        attribute cabling_factor : Real;
        attribute cable_void : Real;
        attribute cu_space : Real;
        attribute steel_area : Real;
        attribute misc_area : Real;
        attribute solder_area : Real;
        attribute ins_fraction : Real;
        attribute J_cu_rule : Real;
        attribute cu_void : Real;
        attribute cu_per_kA_rule : Real;
        attribute steel_per_kA_rule : Real;
        attribute B_steel_ref : Real;
        attribute steel_B_scaling : Real;
        // inventory and price
        attribute element_density : Real;
        attribute element_price_per_m : Real;
        :>> rebco_law_enabled = 0.0;
        :>> winding_cost = winding_sum.cost;
        calc conductor : 'Nb3Sn Cable Critical Surface' {
            in n_strands_in = n_elements;
            in strand_diameter_in = strand_diameter;
            in strand_copper_fraction_in = strand_copper_fraction;
            in turn_current_in = coil.turn_current;
            in B_peak_in = peak_field_calc.B_peak;
            in T_supply_in = winding_pack.T_inventory;
            in nuclear_rise_in = nuclear_rise;
            in margin_rise_in = margin_rise;
            in p_in = p;
            in q_in = q;
            in C1_in = C1;
            in Ca1_in = Ca1;
            in Ca2_in = Ca2;
            in eps0a_in = eps0a;
            in Bc20_in = Bc20;
            in Tc0_in = Tc0;
            in fraction_rule_in = fraction_rule;
            in acceptance_rule_in = acceptance_rule;
            in B_law_min_in = B_law_min;
            in B_law_max_in = B_law_max;
            in B_design_max_in = B_design_max;
            in B_edge_max_in = B_edge_max;
            in T_law_min_in = T_law_min;
            in T_law_max_in = T_law_max;
            in eps_min_in = eps_min;
            in eps_max_in = eps_max;
            // eps_intrinsic_in is deliberately left unbound (design K6): a negative design literal generates as a
            // constant formula, so the case point supplies it and the route refuses an Nb3Sn proposal without it.
        }
        calc adapter : 'Material Winding Adapter' {
            in reference_turns_in = coil.reference_turns;
            in f_set_in = coil.f_set;
            in c_coil_in = coil.c_coil;
            in wp_side_in = winding_pack.wp_side;
        }
        calc area : 'Winding Turn Area Screen' {
            in turn_current_in = coil.turn_current;
            in B_peak_in = peak_field_calc.B_peak;
            in available_area_in = adapter.pack_area_per_turn;
            in element_area_in = conductor.element_area_total;
            in element_copper_area_in = conductor.element_copper_area;
            in cabling_factor_in = cabling_factor;
            in cable_void_in = cable_void;
            in cu_space_in = cu_space;
            in steel_area_in = steel_area;
            in misc_area_in = misc_area;
            in solder_area_in = solder_area;
            in ins_fraction_in = ins_fraction;
            in J_cu_rule_in = J_cu_rule;
            in cu_void_in = cu_void;
            in cu_per_kA_rule_in = cu_per_kA_rule;
            in steel_per_kA_rule_in = steel_per_kA_rule;
            in B_steel_ref_in = B_steel_ref;
            in steel_B_scaling_in = steel_B_scaling;
        }
        calc inventory : 'Winding Inventory and Cost' {
            in n_elements_in = n_elements;
            in element_area_in = conductor.element_area_total;
            in element_density_in = element_density;
            in turns_in = coil.reference_turns;
            in coils_in = coil.n_coils;
            in turn_length_in = adapter.turn_length;
            in turn_current_in = coil.turn_current;
            in cu_space_in = cu_space;
            in cu_void_in = cu_void;
            in steel_area_in = steel_area;
            in solder_area_in = solder_area;
            in rho_cu_in = winding_pack.rho_copper;
            in rho_steel_in = winding_pack.rho_steel;
            in rho_solder_in = winding_pack.rho_solder;
            in price_cu_in = winding_pack.price_copper;
            in price_steel_in = winding_pack.price_steel;
            in price_solder_in = winding_pack.price_solder;
            in element_price_per_m_in = element_price_per_m;
            // Round 1's manufacturing rate is zero: the plant's winding operations are added separately (contract N4).
            in manufacturing_per_m_in = 0.0;
        }
        calc pack_field : 'Pack Field Checks' {
            in B_peak_in = peak_field_calc.B_peak;
            in I_coil_in = coil.I_coil;
            in R_in = coil.R0;
            in wp_side_in = winding_pack.wp_side;
            // mu0_in is left unbound: held calc-usage entry key (design section 2.4, D5).
        }
        calc winding_sum : 'Material Winding Cost' {
            in superconductor_cost_in = inventory.sc_cost;
            in materials_cost_in = inventory.materials_cost;
            in helium_cost_in = material_inventory.cost_helium;
            in winding_operations_cost_in = winding_procurement.winding_fabrication_cost;
        }
        // ---- EXPOSEs for outside readers ----
        attribute conductor_supported : Real = conductor.supported;
        attribute conductor_status_code : Real = conductor.status_code;
        attribute conductor_acceptance_margin : Real = conductor.acceptance_margin;
        attribute conductor_T_cs : Real = conductor.T_cs;
        attribute conductor_operating_fraction : Real = conductor.operating_fraction;
        attribute superconductor_cost : Real = inventory.sc_cost;
        attribute element_length : Real = inventory.element_length;
        attribute ampere_floor_margin : Real = pack_field.ampere_floor_margin;
        attribute R_over_sqrt_A_wp : Real = pack_field.R_over_sqrt_A_wp;
        assert constraint acceptance_ok : 'Conductor Acceptance' {
            in supported_in = conductor.supported;
            in margin_in = conductor.acceptance_margin;
        }
        assert constraint copper_ok : 'Protection Copper Allowance' {
            in cu_margin_in = area.cu_margin;
        }
        assert constraint steel_ok : 'Structural Steel Allowance' {
            in steel_margin_in = area.steel_margin;
        }
        assert constraint pack_area_ok : 'Winding Fit' {
            in fit_margin_in = area.fit_margin;
        }
        assert constraint ampere_floor_ok : 'Ampere Floor' {
            in margin_in = pack_field.ampere_floor_margin;
        }
    }

    part def 'Round1 REBCO Magnet System' :> 'Magnet System' {
        doc /* A supplied REBCO tape-cable winding on the plant's coil set, evaluated with Round 1's REBCO critical surface (measured 20 K shape on the 8-20 T knots, power-law continuation above, selected by the calculated peak field), turn-area screen and inventory at the plant's supply temperature. Same structure as 'Nb3Sn Magnet System'. The top-level tape_width and tape_thickness are Round 1's tape, distinct from the dormant plant winding_pack.tape_width. Status is 1 on 8-20 T (knots) and 20 T to B_law_max (power law); below 8 T the knot branch returns NaN outputs with status 0. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.6; contract r4 section 4 (F10: B_law_max 25 T). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        attribute n_elements : Real;
        attribute tape_width : Real;
        attribute tape_thickness : Real;
        attribute tape_copper_fraction : Real;
        attribute nuclear_rise : Real;
        attribute margin_rise : Real;
        attribute anchor_ic : Real;
        attribute g8 : Real;
        attribute g10 : Real;
        attribute g12 : Real;
        attribute g15 : Real;
        attribute g20 : Real;
        attribute alpha : Real;
        attribute T_star : Real;
        attribute degradation : Real;
        attribute fraction_rule : Real;
        attribute acceptance_rule : Real;
        attribute B_knot_min : Real;
        attribute B_knot_max : Real;
        attribute B_law_min : Real;
        attribute B_law_max : Real;
        attribute T_law_min : Real;
        attribute T_law_max : Real;
        attribute cabling_factor : Real;
        attribute cable_void : Real;
        attribute cu_space : Real;
        attribute steel_area : Real;
        attribute misc_area : Real;
        attribute solder_area : Real;
        attribute ins_fraction : Real;
        attribute J_cu_rule : Real;
        attribute cu_void : Real;
        attribute cu_per_kA_rule : Real;
        attribute steel_per_kA_rule : Real;
        attribute B_steel_ref : Real;
        attribute steel_B_scaling : Real;
        attribute element_density : Real;
        attribute element_price_per_m : Real;
        :>> rebco_law_enabled = 0.0;
        :>> winding_cost = winding_sum.cost;
        calc shape_branch : 'REBCO Shape Branch' {
            in B_peak_in = peak_field_calc.B_peak;
            in B_knot_max_in = B_knot_max;
        }
        calc conductor : 'REBCO Cable Critical Surface' {
            in n_tapes_in = n_elements;
            in tape_width_in = tape_width;
            in tape_thickness_in = tape_thickness;
            in tape_copper_fraction_in = tape_copper_fraction;
            in turn_current_in = coil.turn_current;
            in B_peak_in = peak_field_calc.B_peak;
            in T_supply_in = winding_pack.T_inventory;
            in nuclear_rise_in = nuclear_rise;
            in margin_rise_in = margin_rise;
            in anchor_ic_in = anchor_ic;
            in shape_mode_in = shape_branch.shape_mode;
            in g8_in = g8;
            in g10_in = g10;
            in g12_in = g12;
            in g15_in = g15;
            in g20_in = g20;
            in alpha_in = alpha;
            in T_star_in = T_star;
            in degradation_in = degradation;
            in fraction_rule_in = fraction_rule;
            in acceptance_rule_in = acceptance_rule;
            in B_knot_min_in = B_knot_min;
            in B_knot_max_in = B_knot_max;
            in B_law_min_in = B_law_min;
            in B_law_max_in = B_law_max;
            in T_law_min_in = T_law_min;
            in T_law_max_in = T_law_max;
        }
        calc adapter : 'Material Winding Adapter' {
            in reference_turns_in = coil.reference_turns;
            in f_set_in = coil.f_set;
            in c_coil_in = coil.c_coil;
            in wp_side_in = winding_pack.wp_side;
        }
        calc area : 'Winding Turn Area Screen' {
            in turn_current_in = coil.turn_current;
            in B_peak_in = peak_field_calc.B_peak;
            in available_area_in = adapter.pack_area_per_turn;
            in element_area_in = conductor.element_area_total;
            in element_copper_area_in = conductor.element_copper_area;
            in cabling_factor_in = cabling_factor;
            in cable_void_in = cable_void;
            in cu_space_in = cu_space;
            in steel_area_in = steel_area;
            in misc_area_in = misc_area;
            in solder_area_in = solder_area;
            in ins_fraction_in = ins_fraction;
            in J_cu_rule_in = J_cu_rule;
            in cu_void_in = cu_void;
            in cu_per_kA_rule_in = cu_per_kA_rule;
            in steel_per_kA_rule_in = steel_per_kA_rule;
            in B_steel_ref_in = B_steel_ref;
            in steel_B_scaling_in = steel_B_scaling;
        }
        calc inventory : 'Winding Inventory and Cost' {
            in n_elements_in = n_elements;
            in element_area_in = conductor.element_area_total;
            in element_density_in = element_density;
            in turns_in = coil.reference_turns;
            in coils_in = coil.n_coils;
            in turn_length_in = adapter.turn_length;
            in turn_current_in = coil.turn_current;
            in cu_space_in = cu_space;
            in cu_void_in = cu_void;
            in steel_area_in = steel_area;
            in solder_area_in = solder_area;
            in rho_cu_in = winding_pack.rho_copper;
            in rho_steel_in = winding_pack.rho_steel;
            in rho_solder_in = winding_pack.rho_solder;
            in price_cu_in = winding_pack.price_copper;
            in price_steel_in = winding_pack.price_steel;
            in price_solder_in = winding_pack.price_solder;
            in element_price_per_m_in = element_price_per_m;
            // Round 1's manufacturing rate is zero: the plant's winding operations are added separately (contract N4).
            in manufacturing_per_m_in = 0.0;
        }
        calc pack_field : 'Pack Field Checks' {
            in B_peak_in = peak_field_calc.B_peak;
            in I_coil_in = coil.I_coil;
            in R_in = coil.R0;
            in wp_side_in = winding_pack.wp_side;
            // mu0_in is left unbound: held calc-usage entry key (design section 2.4, D5).
        }
        calc winding_sum : 'Material Winding Cost' {
            in superconductor_cost_in = inventory.sc_cost;
            in materials_cost_in = inventory.materials_cost;
            in helium_cost_in = material_inventory.cost_helium;
            in winding_operations_cost_in = winding_procurement.winding_fabrication_cost;
        }
        // ---- EXPOSEs for outside readers ----
        attribute conductor_supported : Real = conductor.supported;
        attribute conductor_status_code : Real = conductor.status_code;
        attribute conductor_acceptance_margin : Real = conductor.acceptance_margin;
        attribute conductor_T_cs : Real = conductor.T_cs;
        attribute conductor_operating_fraction : Real = conductor.operating_fraction;
        attribute superconductor_cost : Real = inventory.sc_cost;
        attribute element_length : Real = inventory.element_length;
        attribute ampere_floor_margin : Real = pack_field.ampere_floor_margin;
        attribute R_over_sqrt_A_wp : Real = pack_field.R_over_sqrt_A_wp;
        attribute shape_mode : Real = shape_branch.shape_mode;
        assert constraint acceptance_ok : 'Conductor Acceptance' {
            in supported_in = conductor.supported;
            in margin_in = conductor.acceptance_margin;
        }
        assert constraint copper_ok : 'Protection Copper Allowance' {
            in cu_margin_in = area.cu_margin;
        }
        assert constraint steel_ok : 'Structural Steel Allowance' {
            in steel_margin_in = area.steel_margin;
        }
        assert constraint pack_area_ok : 'Winding Fit' {
            in fit_margin_in = area.fit_margin;
        }
        assert constraint ampere_floor_ok : 'Ampere Floor' {
            in margin_in = pack_field.ampere_floor_margin;
        }
    }

    // ------------------------------------------------------------------ cryoplant variant (design section 2.7)

    part def 'Staged Cryoplant' :> 'Cryoplant' {
        doc /* The plant's cryoplant with Round 1's cold-stage load and staged refrigeration: the cold-stage and intercept demands, the refrigeration electricity that reaches the power balance's p_cryo, and the lead and joint drive that reaches the TF power supply are rebound to the staged calcs through the plant's default seams; the refrigerator capital is Round 1's Green law at the supplied cold rating. The plant's thermal inventory is disabled (inventory_enabled = false), so it returns zeros and never evaluates outside its 10-30 K domain; the plant's 0.20-Carnot cold chain and intercept electricity still execute but reach no priced or checked channel. The Green law prices only the cold rating, so rated_intercept_W has no cost response here (free_capacity, design D17). The Round 1 NIST 316 coefficients are named nist_k_a to nist_k_i because the plant cryoplant already owns k_c (support conductance). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: sections 2.3, 2.7, 2.8; contract r4 section 6; plant-chain-audit.md section 6 step 6. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30 */
        attribute load_multiplier : Real;
        attribute nist_k_a : Real;
        attribute nist_k_b : Real;
        attribute nist_k_c : Real;
        attribute nist_k_d : Real;
        attribute nist_k_e : Real;
        attribute nist_k_f : Real;
        attribute nist_k_g : Real;
        attribute nist_k_h : Real;
        attribute nist_k_i : Real;
        attribute eta_mode : Real;
        attribute eta_const : Real;
        attribute green_a : Real;
        attribute green_b : Real;
        attribute capital_mode : Real;
        attribute green_c : Real;
        attribute green_d : Real;
        attribute T_green : Real;
        attribute usd2015_to_2021 : Real;
        attribute T_conduction_ref : Real;
        attribute I_joint_ref : Real;
        :>> inventory_enabled = false;
        :>> purchase_cost_per_module = refrigeration.refrigerator_capital;
        :>> cold_load_W_required = cold_stage.q_cold;
        :>> intercept_load_W_required = cold_stage.q_shield;
        :>> intercept_demand_available = true;
        :>> p_elec = refrigeration.p_in_total_MW;
        :>> p_drive = staged_drive.p_drive;
        calc static_loads : 'Staged Static Loads' {
            in n_coils_in = n_coils;
            in c_coil_in = c_coil;
            in wp_side_in = wp_side;
            in t_case_in = t_case;
            in shield_area_ratio_in = shield_area_ratio;
            in eps_eff_in = eps_eff;
            in sigma_SB_in = sigma_SB;
            in q_MLI_in = q_MLI;
            in g_per_coil_in = g_per_coil;
            in k_c_in = k_c;
            in k_s_in = k_s;
            in T_cold_in = T_cold_cryo;
            in T_shield_in = T_shield;
            in T_amb_in = T_amb_cryo;
            in T_conduction_ref_in = T_conduction_ref;
            in p_fixed_MW_in = p_fixed_cryo;
            in q_nuc_in = q_nuc_cryo;
            in vol_cold_in = vol_cold_total;
            in q_nuc_structure_in = q_nuc_structure;
            in m_support_in = m_support;
            in rho_structure_in = rho_structure;
        }
        calc cold_stage : 'Magnet Cold Stage Load' {
            in T_supply_in = T_cold_cryo;
            in T_shield_in = T_shield;
            in T_amb_in = T_amb_cryo;
            in turn_current_in = I_turn;
            in nuclear_density_in = static_loads.nuclear_density_eff;
            in cold_volume_in = vol_cold_total;
            in radiation_ref_in = static_loads.q_radiation;
            in conduction_ref_in = static_loads.conduction_ref;
            in T_conduction_ref_in = T_conduction_ref;
            in k_a_in = nist_k_a;
            in k_b_in = nist_k_b;
            in k_c_in = nist_k_c;
            in k_d_in = nist_k_d;
            in k_e_in = nist_k_e;
            in k_f_in = nist_k_f;
            in k_g_in = nist_k_g;
            in k_h_in = nist_k_h;
            in k_i_in = nist_k_i;
            in n_leads_in = n_leads;
            in f_lead_in = f_lead;
            in L0_in = L0;
            in p_joint_ref_in = static_loads.p_joint_ref;
            in I_joint_ref_in = I_joint_ref;
            in shield_static_in = static_loads.shield_static;
            in load_multiplier_in = load_multiplier;
        }
        calc refrigeration : 'Staged Refrigeration Screen' {
            in q_cold_in = cold_stage.q_cold;
            in T_supply_in = T_cold_cryo;
            in q_shield_in = cold_stage.q_shield;
            in T_shield_in = T_shield;
            in T_amb_in = T_amb_cryo;
            in rating_cold_in = rated_cold_W;
            in eta_mode_in = eta_mode;
            in eta_const_in = eta_const;
            in green_a_in = green_a;
            in green_b_in = green_b;
            in f_carnot_shield_in = f_carnot_shield;
            in capital_mode_in = capital_mode;
            in green_c_in = green_c;
            in green_d_in = green_d;
            in T_green_in = T_green;
            in usd2015_to_2021_in = usd2015_to_2021;
        }
        calc staged_drive : 'Staged Drive Power' {
            in q_leads_in = cold_stage.q_leads;
            in q_shield_in = cold_stage.q_shield;
            in shield_static_in = static_loads.shield_static;
            in q_joints_in = cold_stage.q_joints;
            in joint_drive_fraction_in = joint_drive_fraction;
        }
        // ---- EXPOSEs for outside readers ----
        attribute staged_q_cold : Real = cold_stage.q_cold;
        attribute staged_q_shield : Real = cold_stage.q_shield;
        attribute refrigeration_eta_cold : Real = refrigeration.eta_cold;
        attribute refrigeration_green_extrapolated : Real = refrigeration.green_extrapolated;
        assert constraint capacity_ok : 'Refrigerator Capacity' {
            in capacity_margin_in = refrigeration.capacity_margin;
        }
    }
}
