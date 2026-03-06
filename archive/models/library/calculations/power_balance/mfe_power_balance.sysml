package MFEPowerBalanceLibrary {
    doc /*
    MFE (Magnetic Fusion Energy) specific power balance calculations.

    Computes full power flow for tokamaks and stellarators:
    - Thermal power from neutron heating + input + recovered pumping
    - Thermal electric power via Rankine/Brayton cycle
    - Recirculating power: coils, cooling, pumping, auxiliary
    - Engineering Q and net electric power

    Uses 'Alpha Power Calc' from PowerBalanceLibrary for fuel-type
    dependent alpha power.

    Note: Direct energy conversion (p_dee, eta_de) is deferred per spec.

    **Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py
    **Last Updated**: 2026-01-26
    */

    private import ScalarValues::Real;
    private import FoundationTypes::FuelType;
    private import PowerBalanceLibrary::'Alpha Power Calc';

    // ============================================================
    // MFE POWER BALANCE CALCULATION
    // ============================================================

    calc def 'MFE Power Balance Calc' {
        doc /*
        MFE (Magnetic Fusion Energy) specific power balance.

        Computes full power flow for tokamaks and stellarators:
        - Thermal power from neutron heating + input + recovered pumping
        - Thermal electric power via Rankine/Brayton cycle
        - Recirculating power: coils, cooling, pumping, auxiliary
        - Engineering Q and net electric power

        Inputs: 16 parameters (3 generic + 13 MFE-specific)
        Outputs: 15 power values and metrics

        **Source**: PyFECONS PowerBalance.py:8-50
        **Reference**: MFE power plant design standards
        **Last Updated**: 2026-01-26
        */

        // === PRIMARY INPUTS (from generic) ===
        in attribute p_nrl : Real;          // Fusion power [MW]
        in attribute fuel_type : FuelType;  // Fuel type enum
        in attribute p_input : Real;        // Plasma heating power [MW]

        // === MFE-SPECIFIC INPUTS: Efficiencies ===
        in attribute mn : Real;             // Neutron energy multiplier (blanket breeding)
        in attribute eta_th : Real;         // Thermal-to-electric efficiency
        in attribute eta_p : Real;          // Pumping power capture efficiency
        in attribute eta_pin : Real;        // Input power wall plug efficiency

        // === MFE-SPECIFIC INPUTS: Power fractions ===
        in attribute fpcppf : Real;         // Primary coolant pumping power fraction
        in attribute f_sub : Real;          // Subsystem and control fraction

        // === MFE-SPECIFIC INPUTS: Coil power ===
        in attribute p_tf : Real;           // TF coil power [MW]
        in attribute p_pf : Real;           // PF coil power [MW]

        // === MFE-SPECIFIC INPUTS: Cooling power ===
        in attribute p_tfcool : Real;       // TF coil cooling [MW]
        in attribute p_pfcool : Real;       // PF coil cooling [MW]

        // === MFE-SPECIFIC INPUTS: Auxiliary power ===
        in attribute p_trit : Real;         // Tritium systems [MW]
        in attribute p_house : Real;        // Housekeeping [MW]
        in attribute p_cryo : Real;         // Cryogenic pumping [MW]

        // === PRIMARY OUTPUT ===
        return attribute p_net : Real;      // Net electric power [MW]

        // === CALCULATIONS ===

        // Step 1: Alpha power (fuel-dependent)
        // Source: PowerBalance.py:10
        calc alpha_calc : 'Alpha Power Calc' {
            in p_nrl = p_nrl;
            in fuel_type = fuel_type;
        }
        attribute p_alpha : Real = alpha_calc.p_alpha;

        // Step 2: Neutron power
        // Source: PowerBalance.py:11
        attribute p_neutron : Real = p_nrl - p_alpha;

        // Step 3: Cooling power aggregation
        // Source: PowerBalance.py:12
        attribute p_cool : Real = p_tfcool + p_pfcool;

        // Step 4: Auxiliary power aggregation
        // Source: PowerBalance.py:13
        attribute p_aux : Real = p_trit + p_house;

        // Step 5: Coil power aggregation
        // Source: PowerBalance.py:14
        attribute p_coils : Real = p_tf + p_pf;

        // Step 6: Thermal power
        // Source: PowerBalance.py:15-21
        // p_th = mn*p_neutron + p_input + eta_th*(fpcppf*eta_p + f_sub)*(mn*p_neutron)
        attribute p_th : Real = mn * p_neutron + p_input +
                                eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron);

        // Step 7: Thermal electric power
        // Source: PowerBalance.py:22
        attribute p_the : Real = eta_th * p_th;

        // Step 8: Gross electric power (no direct conversion - deferred)
        // Source: PowerBalance.py:24 (simplified - p_dee deferred)
        attribute p_et : Real = p_the;

        // Step 9: Lost power (thermal minus electric conversion)
        // Source: PowerBalance.py:25 (simplified - p_dee deferred)
        // Note: Full formula is p_th - p_the - p_dee
        attribute p_loss : Real = p_th - p_the;

        // Step 10: Pumping power
        // Source: PowerBalance.py:26
        attribute p_pump : Real = fpcppf * p_the;

        // Step 11: Subsystem power
        // Source: PowerBalance.py:27
        attribute p_sub : Real = f_sub * p_the;

        // Step 12: Scientific Q
        // Source: PowerBalance.py:28
        attribute q_sci : Real = p_nrl / p_input;

        // Step 13: Engineering Q
        // Source: PowerBalance.py:29-48
        // Numerator: eta_th*(mn*p_neutron + p_pump + p_input)
        // Denominator: p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input/eta_pin
        //
        // Note: Original PyFECONS includes eta_de*p_alpha in numerator,
        // but we defer direct conversion per spec.
        attribute q_eng_numerator : Real = eta_th * (mn * p_neutron + p_pump + p_input);
        attribute q_eng_denominator : Real = p_coils + p_pump + p_sub + p_aux +
                                              p_cool + p_cryo + p_input / eta_pin;
        attribute q_eng : Real = q_eng_numerator / q_eng_denominator;

        // Step 14: Recirculating fraction
        // Source: PowerBalance.py:49
        attribute rec_frac : Real = 1.0 / q_eng;

        // Step 15: Net electric power
        // Source: PowerBalance.py:50
        (1.0 - rec_frac) * p_et
    }
}
