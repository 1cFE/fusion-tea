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
        in attribute gain : Real;
        in attribute blanket_multiplier : Real;
        in attribute thermal_efficiency : Real;

        attribute fusion_cycle_gain : Real = eta * gain * blanket_multiplier * thermal_efficiency;

        out attribute f_recirc : Real = 1.0 / fusion_cycle_gain;
    }

    constraint def 'Viability Threshold' {
        doc /*
        The product of driver efficiency (eta) and target gain (G)
        must exceed ~10 for economically viable IFE. This threshold
        ensures the recirculating power fraction remains manageable
        (<25%) and creates fundamentally different gain requirements
        by driver type:
        - Heavy-ion (eta=0.25): G > 40
        - Laser (eta=0.07): G > 143
        - Pulser (eta=0.10): G > 100

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md,
            knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
        **Ref**: EIF-1992 Components section; Accel-2013 Section 3
        **Basis**: DI-001 — physics-derived minimum for economic viability
        */

        in attribute eta : Real;
        in attribute gain : Real;
        in attribute threshold : Real default 10.0;

        eta * gain >= threshold
    }
}
