package mfe_cryo_plant {
    private import ScalarValues::*;

    calc def 'Cryoplant Electrical Power' {
        doc /*
        Cryoplant wall-plug electrical power [MW] from the cold-mass heat
        load (WI-024). Steady-state refrigeration power balance:
            p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift
            COP    = f_carnot * T_cold / (T_amb - T_cold)   (Carnot x fraction)
            p_elec = p_cold / COP + p_direct
        p_direct is an additive direct term for concepts that specify the
        cryoplant electrical outright (no chain); with zero heat inputs the
        calc passes p_direct through exactly. f_uplift names the seam for
        heat loads missing from the inventory (>= 1). Dormant-safe defaults:
        an unbound concept computes p_elec = 0; f_carnot defaults 1.0 (not 0)
        so the dormant COP stays defined — the mode is selected by the heat
        inputs, never by the efficiency (WI-022 T_i0 precedent).
        Output feeds the power-balance p_cryo slot ("cryogenic system
        power"), which 1costingFE's own defaults document as the cryoplant
        wall-plug electrical.
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
        **Ref**: physics.py:321-323 (p_cryo in the recirculating sum);
            steady_state_dipole.yaml:52-53 (slot semantics: "Cryogenic
            wall-plug power" = heat load x plant efficiency — semantics
            witness only, value inadmissible)
        **Basis**: reversed-Carnot reference cycle x fraction-of-Carnot;
            concept-agnostic (MR-3) — all values bound by instances
        */

        in attribute q_nuc : Real default 0.0;     // volumetric nuclear heating at the cold mass [W/m^3]
        in attribute vol_cold : Real default 0.0;  // heated cold-mass volume [m^3]
        in attribute p_fixed : Real default 0.0;   // fixed cold-mass heat loads [MW] (joints, leads)
        in attribute f_uplift : Real default 1.0;  // unprinted-loads multiplier [1] (>= 1)
        in attribute T_cold : Real default 20.0;   // cold-mass operating temperature [K]
        in attribute T_amb : Real default 300.0;   // heat-rejection (ambient) temperature [K]
        in attribute f_carnot : Real default 1.0;  // fraction-of-Carnot plant efficiency [1] (dormant-safe 1.0)
        in attribute p_direct : Real default 0.0;  // directly-specified cryoplant electrical [MW] (additive)

        attribute p_cold : Real = (q_nuc * vol_cold * 1.0e-6 + p_fixed) * f_uplift;
        attribute cop_carnot : Real = T_cold / (T_amb - T_cold);
        attribute cop : Real = f_carnot * cop_carnot;

        out attribute p_elec : Real = p_cold / cop + p_direct;
    }
}
