package mfe_magnet_cost {
    private import ScalarValues::*;

    calc def 'Magnet Coil Cost' {
        doc /*
        Superconducting magnet/coil capital cost from the bilinear toroidal
        conductor-quantity model, concept-agnostic across MFE approaches.

          total_kAm = G * B * R0 * r_coil / (mu0 * 1000)
          capital_cost = total_kAm * cost_per_kAm * coil_markup

        The ampere-meter quantity follows Ampere's law around the torus
        (ampere-turns ~ B*R0) times the conductor length per turn (~ coil-bore
        radius r_coil). The expensive superconductor dominates SC coil cost, so
        cost = conductor quantity * $/kA-m * a manufacturing markup (winding,
        quench protection, cryostat, testing).

        Fully parameterized (MR-WI009-8): G, B, R0, r_coil, cost_per_kAm, and
        coil_markup are all inputs — the concept sets them in WI-011. See the
        reconciliation note below for the current 1costingFE values.

        Note on units: the 1costingFE source divides the conductor cost by 1e6
        to express M$ (cas22.py:442). This calc omits that conversion, so
        capital_cost inherits the units of cost_per_kAm (i.e. $ when
        cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
        **Basis**: MFE coil conductor-quantity cost model; magnet cost rises
            with B, R0, r_coil (SV-018)
        */

        in attribute G : Real;
        in attribute B : Real;
        in attribute R0 : Real;
        in attribute r_coil : Real;
        in attribute cost_per_kAm : Real;
        in attribute coil_markup : Real;

        // Vacuum permeability [T*m/A]. Source: cas22.py:92 (_MU0 = 4*pi*1e-7).
        in attribute mu0 : Real default 1.25663706212e-6;

        // Conductor quantity [kA*m]. 1000.0 = A -> kA. Source: cas22.py:427.
        attribute total_kAm : Real = G * B * R0 * r_coil / (mu0 * 1000.0);

        // Coil capital cost. Source: cas22.py:441-444.
        out attribute capital_cost : Real = total_kAm * cost_per_kAm * coil_markup;
    }
}
