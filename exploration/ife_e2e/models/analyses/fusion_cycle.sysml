package fusion_cycle {
    private import ScalarValues::*;

    calc def 'Recirculating Power Fraction' {
        doc /*
        Computes the recirculating power fraction for an IFE plant.
        f_recirc = 1 / (eta * G * M * epsilon)

        The recirculating power fraction determines what fraction of
        gross electric output must be fed back to the driver. Values
        above ~0.25 (fusion cycle gain below ~4) create a sharp knee
        in the cost curve.

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Components section (fusion cycle gain discussion)
        **Basis**: DI-001 — eta*G must exceed ~10 for viability
        */

        in attribute eta : Real;
        in attribute gain_in : Real;
        in attribute blanket_multiplier : Real;
        in attribute thermal_efficiency_in : Real;

        attribute fusion_cycle_gain : Real = eta * gain_in * blanket_multiplier * thermal_efficiency_in;

        out attribute f_recirc : Real = 1.0 / fusion_cycle_gain;
    }

    constraint def 'Viability Threshold' {
        doc /*
        Eta-times-gain economic heuristic, retained for compatibility.
        Passing this threshold does not establish positive net generation:
        blanket and conversion efficiency and other parasitic loads also matter.
        Use Positive Net Generation on the actual priced power balance.

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md,
            knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
        **Ref**: EIF-1992 Components section; Accel-2013 Section 3
        **Basis**: DI-001 — approximate economic heuristic
        **Reference**: EIF-1992 Components section; Accel-2013 Section 3
        **Last Updated**: 2026-09-10
        */

        in attribute eta : Real;
        in attribute gain_in : Real;
        in attribute threshold : Real default 10.0;

        eta * gain_in >= threshold
    }
    constraint def 'Positive Net Generation' {
        doc /*
        A generating operating point must export strictly positive net electricity.
        net_power is the actual priced balance in W. Exact zero fails.
        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Reference**: Eqs. 2.12-2.16
        **Basis**: [DERIVED] Positive net electricity is required for generation.
        **Last Updated**: 2026-09-10
        */
        in attribute net_power : Real;
        net_power > 0.0
    }
}
