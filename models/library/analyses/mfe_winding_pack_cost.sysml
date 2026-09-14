package mfe_winding_pack_cost {
    private import ScalarValues::*;

    calc def 'Winding Pack Material Inventory' {
        doc /*
        Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
        Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
        Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; inter-pancake insulation is unquantified and omitted.
        Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
        **Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
        **Last Updated**: 2026-09-13
        */
        in attribute volume_in : Real;
        in attribute f_copper : Real;
        in attribute f_solder : Real;
        in attribute f_steel : Real;
        in attribute f_helium : Real;
        in attribute rho_copper : Real;
        in attribute rho_solder : Real;
        in attribute rho_steel : Real;
        in attribute price_copper : Real;
        in attribute price_solder : Real;
        in attribute price_steel : Real;
        in attribute price_helium : Real;
        in attribute helium_pressure : Real;
        in attribute temperature : Real;
        in attribute helium_gas_constant : Real;
        out attribute mass_copper : Real;
        out attribute mass_solder : Real;
        out attribute mass_steel : Real;
        out attribute mass_helium : Real;
        out attribute cost_copper : Real;
        out attribute cost_solder : Real;
        out attribute cost_steel : Real;
        out attribute cost_helium : Real;
        out attribute material_cost : Real;
        out attribute helium_density : Real;
        out attribute tape_volume : Real;
    }

    calc def 'Winding Pack Procurement Cost' {
        doc /*
        Additive composite-tape procurement, non-tape material procurement and winding operations. Casing and primary structure remain separate accounts. Normative manual-completion equations: K = n_coils * I_coil * f_set * c_coil / 1000 [kA m]; tape_cost = K * cost_per_kAm; conductor_length = 1000 * K / turn_current [m]; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
        Inputs: n_coils and f_set dimensionless; I_coil ampere-turns; c_coil m; cost_per_kAm dollars/(kA m); turn_current A; winding_rate_1990 dollars1990/m; escalation and nonplanar factor dimensionless; material_cost_in dollars. Outputs: costs dollars, conductor_length m of composite conductor (not tape metres). Winding operations are not a complete factory quote or a labor-only rate. Steel sheath charges would overlap explicit pack steel; unresolved fixed cable and insulation quantities are omitted. Rate transfer to REBCO is an assumption.
        Domain: every input and output finite; n_coils, c_coil, turn_current, cost_escalation and nonplanar_factor > 0; I_coil, cost_per_kAm, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic and refuses non-finite results.
        **Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
        **Reference**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
        **Last Updated**: 2026-09-13
        */
        in attribute n_coils : Real;
        in attribute I_coil : Real;
        in attribute f_set : Real;
        in attribute c_coil : Real;
        in attribute cost_per_kAm : Real;
        in attribute turn_current : Real;
        in attribute winding_rate_1990 : Real;
        in attribute cost_escalation : Real;
        in attribute nonplanar_factor : Real;
        in attribute material_cost_in : Real;
        out attribute tape_cost : Real;
        out attribute conductor_length : Real;
        out attribute winding_fabrication_cost : Real;
        out attribute cost : Real;
    }
}
