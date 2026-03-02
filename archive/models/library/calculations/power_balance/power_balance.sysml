package PowerBalanceLibrary {
    doc /*
    Generic power balance calculations for fusion power plants.

    Contains concept-agnostic calculations that apply to any fusion approach:
    - Alpha power calculation (fuel-type dependent)
    - Generic power balance (p_alpha, p_neutron, q_sci)

    MFE-specific and IFE-specific calculations are in separate files.

    **Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py
    **Last Updated**: 2026-01-26
    */

    private import ScalarValues::Real;
    private import FoundationTypes::FuelType;

    // ============================================================
    // ALPHA POWER CALCULATION
    // ============================================================

    calc def 'Alpha Power Calc' {
        doc /*
        Compute charged particle (alpha) power from fusion reaction.

        The alpha fraction depends on fuel type and reaction kinematics:
        - DT: 3.52 MeV alpha / 17.58 MeV total = 20.02%
        - DD: Weighted average of two branches = ~50%
        - DHe3: 14.7 MeV / 18.3 MeV = 80.33%
        - PB11: 100% (aneutronic - all charged particles)

        **Source**: PyFECONS PowerBalance.py:94-104
        **Reference**: https://en.wikipedia.org/wiki/Nuclear_fusion
        **Last Updated**: 2026-01-26
        */

        in attribute p_nrl : Real;          // Fusion power [MW]
        in attribute fuel_type : FuelType;  // Fuel type enum

        return attribute p_alpha : Real;    // Alpha particle power [MW]

        // Fuel-type conditional calculation
        // DT: 3.52/17.58 = 0.2002
        // DD: (0.5 * 3.02/4.03 + 0.5 * 0.82/3.27) = 0.5001
        // DHE3: 14.7/18.3 = 0.8033
        // PB11: 8.7/8.7 = 1.0
        if fuel_type == FuelType::DT? p_nrl * 3.52 / 17.58
        else if fuel_type == FuelType::DD? p_nrl * (0.5 * 3.02 / 4.03 + 0.5 * 0.82 / 3.27)
        else if fuel_type == FuelType::DHE3? p_nrl * 14.7 / 18.3
        else p_nrl * 1.0
    }

    // ============================================================
    // GENERIC POWER BALANCE CALCULATION
    // ============================================================

    calc def 'Power Balance Calc' {
        doc /*
        Generic power balance calculation for any fusion concept.

        Computes:
        - p_alpha: Charged particle power (from fuel type)
        - p_neutron: Neutron power (remainder after alpha)
        - q_sci: Scientific Q (fusion power / input power)

        These outputs are concept-agnostic and used by both MFE and IFE.
        Specialized calculations (MFE, IFE) extend this with concept-specific
        recirculating power flows.

        **Source**: PyFECONS PowerBalance.py:10-11, 28
        **Reference**: Standard fusion physics
        **Last Updated**: 2026-01-26
        */

        // === PRIMARY INPUTS ===
        in attribute p_nrl : Real;          // Fusion power [MW]
        in attribute fuel_type : FuelType;  // Fuel type enum
        in attribute p_input : Real;        // Input/heating power [MW]

        // === PRIMARY OUTPUT ===
        return attribute q_sci : Real;      // Scientific Q (dimensionless)

        // === CALCULATIONS ===

        // Alpha power from helper calc
        // Source: PowerBalance.py:10
        calc alpha_calc : 'Alpha Power Calc' {
            in p_nrl = p_nrl;
            in fuel_type = fuel_type;
        }

        // Expose alpha power for downstream access
        // Source: PowerBalance.py:10
        attribute p_alpha : Real = alpha_calc.p_alpha;

        // Neutron power: remainder of fusion power
        // Source: PowerBalance.py:11
        attribute p_neutron : Real = p_nrl - p_alpha;

        // Scientific Q: fusion power gain over input
        // Source: PowerBalance.py:28
        p_nrl / p_input
    }
}
