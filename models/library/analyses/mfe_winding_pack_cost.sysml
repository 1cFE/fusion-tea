package mfe_winding_pack_cost {
    private import ScalarValues::*;

    calc def 'Winding Pack Material Inventory' {
        doc /*
        Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
        Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
        Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; additional inter-pancake insulation is accounted separately by the conditional insulation inventory.
        Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
        **Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
        **Last Updated**: 2026-09-15
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
        Additive full-composite tape procurement, external pack materials and winding operations. Casing and primary support remain separate accounts. Normative manual equations: tape_area = tape_width * tape_thickness; tape_length = tape_volume_in / tape_area; tape_cost = tape_length * tape_price_per_m; conductor_length = n_coils * I_coil * f_set * c_coil / turn_current; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
        Units: tape_volume_in m^3; width and full composite thickness m; tape_price_per_m dollars per metre of that complete purchased tape; tape_length individual tape metres. I_coil ampere-turns; turn_current A; conductor_length composite-conductor metres; winding_rate_1990 dollars1990/conductor-m; other costs dollars. The existing volume input already includes field-envelope quantity scaling. Never apply another envelope factor to tape price. Tape substrate/stabilizer are included in the complete tape purchase; external copper jacket, solder, steel and helium are separate. Winding operations are an inherited transfer assumption, not a complete factory quote. Detailed insulation inclusion in the inherited winding rate is uncertain; a conditional separate sheet-stock scenario is exposed. Spares, yield and integer tape counts remain unquantified.
        Domain: all inputs and outputs finite; n_coils, c_coil, turn_current, tape_width, tape_thickness, cost_escalation and nonplanar_factor > 0; I_coil, tape_volume_in, tape_price_per_m, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Computed tape_area finite and positive; positive volume requires positive tape_length; positive length and price require positive tape_cost. Typed manual completion raises calculation- and quantity-named ValueError before invalid arithmetic and refuses nonfinite results.
        **Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
        **Reference**: work/active/WI-060_tape-procurement-quantity-basis/design.md (volume/cross-section identity and conditional construction); knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
        **Last Updated**: 2026-09-15
        */
        in attribute n_coils : Real;
        in attribute I_coil : Real;
        in attribute f_set : Real;
        in attribute c_coil : Real;
        in attribute tape_volume_in : Real;
        in attribute tape_width : Real;
        in attribute tape_thickness : Real;
        in attribute tape_price_per_m : Real;
        in attribute turn_current : Real;
        in attribute winding_rate_1990 : Real;
        in attribute cost_escalation : Real;
        in attribute nonplanar_factor : Real;
        in attribute material_cost_in : Real;
        out attribute tape_length : Real;
        out attribute tape_cost : Real;
        out attribute conductor_length : Real;
        out attribute winding_fabrication_cost : Real;
        out attribute cost : Real;
    }

    calc def 'Winding Pack Insulation Inventory' {
        doc /* Conditional additional internal solid-sheet inventory and unpriced ground-layer envelope, excluding assembly clearance and extra cold equipment.
        Normative manual equations: internal_volume = volume_in*(internal_fraction_x+internal_fraction_y+internal_fraction_x*internal_fraction_y); perimeter = 2*n_coils*c_coil*wp_side*f_perimeter*(sqrt(aspect_ratio)*(1+internal_fraction_x)+(1+internal_fraction_y)/sqrt(aspect_ratio)); ground_volume = ground_thickness*perimeter+4*ground_thickness*ground_thickness*n_coils*c_coil; sheet_area = internal_volume/sheet_thickness; stock_cost = sheet_area*sheet_price.
        Units: volumes m^3, wp_side/c_coil/thicknesses m, sheet_area m^2, sheet_price dollars/m^2, stock_cost dollars; other inputs dimensionless. Current wp_side and geometric volume scale the frozen relative coil-section distribution with equal circumference and common aspect ratio. Area and perimeter distribution factors are distinct. Closed coils have no end layer. Internal solid-sheet occupancy and exclusion from the winding charge are assumptions; this is not a demonstrated missing charge. Ground wrapping, impregnation, installation, waste and qualification remain unresolved. The laminate stock already includes cured resin.
        Domain: every input and intermediate/output finite; volume_in, ground_thickness and sheet_price >= 0; wp_side, aspect_ratio, n_coils, c_coil, sheet_thickness > 0; internal fractions >= 0; 0 < f_perimeter <= 1. Positive products/divisions must not underflow to zero. Fractions are added build relative to the underlying section, not material occupancy fractions. No independently inconsistent volume/distribution interpretation is certified by this arithmetic.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/; work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/manufacturing-research.md.
        **Reference**: Stellaris Tables 7-8 and Figure 40; work/active/WI-063_magnet-manufacturing-account-completeness/design.md; goal evidence/source-design-review.md.
        **Last Updated**: 2026-09-15 */
        in attribute volume_in : Real;
        in attribute wp_side : Real;
        in attribute aspect_ratio : Real;
        in attribute internal_fraction_x : Real;
        in attribute internal_fraction_y : Real;
        in attribute ground_thickness : Real;
        in attribute n_coils : Real;
        in attribute c_coil : Real;
        in attribute f_perimeter : Real;
        in attribute sheet_thickness : Real;
        in attribute sheet_price : Real;
        out attribute internal_volume : Real;
        out attribute ground_volume : Real;
        out attribute sheet_area : Real;
        out attribute stock_cost : Real;
    }
}
