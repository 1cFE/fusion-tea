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
        coil_markup are all inputs -- the concept sets them in WI-011. See the
        reconciliation note below for the current 1costingFE values.

        Note on units: the 1costingFE source divides the conductor cost by 1e6
        to express M$ (cas22.py:442). This calc omits that conversion, so
        capital_cost inherits the units of cost_per_kAm (i.e. $ when
        cost_per_kAm is $/kA-m). Apply the M$ scaling downstream if desired.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:427 (total_kAm), cas22.py:441-444 (SC coil cost)
        **Basis**: MFE coil conductor-quantity cost model; magnet cost rises
            with B, R0, r_coil (SV-018)

        WI-035: retained as the live 1cfe-form COMPARISON channel (exposed as
        magnet_capital_1cfe); the CAS22.1.3 rollup is now 'Magnet Capital'
        (winding pack + structure below), and B is computed by
        'Coil Set Axis Field' (mfe_magnet_field), so this channel responds
        to the coil-current lever too.
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

    calc def 'Winding Pack Cost' {
        doc /*
        Winding-pack capital [$] over the REAL winding length (WI-035 D4):

          kAm_wind = n_coils * I_coil * f_set * c_coil / 1000
          cost     = kAm_wind * cost_per_kAm * f_wp_fab

        Replaces the proxy length 4*pi*r_coil (a bore-radius stand-in,
        WI-032) with the coil count x set-mean current x printed typical
        circumference. f_wp_fab is the winding fabrication markup
        (content: winding, insulation, cooling, jointing, test --
        costing_constants.yaml:50 -- times the documented NCSX non-planar
        production penalty, yaml:60-66). Quench protection carries no
        separate account: the NI coils are passively protected (printed,
        sec. 2.9).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: costing_constants.yaml:50 (fab content), :60-72 (5.87 =
            3.09 x 1.9 NCSX penalty; path factor separate); cas22.py:34
            ("conductor is ~10-15% of finished magnet cost" -- cross-check);
            images/page_022_table_0.png (Table 8 per-coil currents);
            raw.pdf sec. 2.9 (25 m typical circumference; NI passive quench
            protection)
        **Basis**: conductor quantity over real winding length x $/kA-m x
            content-mapped fabrication markup; concept-agnostic (MR-3)
        */

        // number of field coils [1]
        in attribute n_coils : Real;
        // peak single-coil current [A]
        in attribute I_coil : Real;
        // set-mean over peak coil current ratio [1]
        in attribute f_set : Real;
        // typical winding circumference [m]
        in attribute c_coil : Real;
        // conductor cost [$/kA-m]
        in attribute cost_per_kAm : Real;
        // winding fabrication markup [1]
        in attribute f_wp_fab : Real;

        // conductor quantity over the real winding length [kA*m]
        attribute kAm_wind : Real = n_coils * I_coil * f_set * c_coil / 1000.0;

        out attribute cost : Real = kAm_wind * cost_per_kAm * f_wp_fab;
    }

    calc def 'Magnet Structure Cost' {
        doc /*
        Magnet casing-structure capital [$] on a steel-mass basis (WI-035 D5):

          cost = n_coils * m_casing * steel_price * f_steel_fab

        Covers the COIL CASINGS only; inter-coil plates, support rings, and
        legs remain CAS22.1.5 primary structure ('Structure Cost') -- the
        boundary that prevents double counting. m_casing is bound per
        instance; for Stellaris the printed cast-part floor is used as a
        knowing lower bound with the seam named in the binding doc.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml (pin 0254385);
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: costing_constants.yaml:52-53 (coil_steel_price_per_kg 6.0,
            coil_steel_fab_markup 3.0 "coil-case / inter-coil support
            fabrication"); raw.pdf sec. 2.10 (casing cast parts 63-200 t;
            AISI 316LN)
        **Basis**: casing steel mass x fabricated-steel rate x fabrication
            markup; concept-agnostic (MR-3)
        */

        // number of field coils [1]
        in attribute n_coils : Real;
        // casing steel mass per coil [kg]
        in attribute m_casing : Real;
        // fabricated structural steel price [$/kg]
        in attribute steel_price : Real;
        // casing fabrication markup [1]
        in attribute f_steel_fab : Real;

        out attribute cost : Real = n_coils * m_casing * steel_price * f_steel_fab;
    }

    calc def 'Magnet Capital' {
        doc /*
        CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
        capital is the sum of the separately sized sub-accounts. Kept as a
        calc def so the plant's magnet.capital_cost redefinition stays a
        reference binding (the codegen-proven WI-021 pattern), not an
        arithmetic redefinition expression (dropped by the pinned codegen,
        WI-030).

        **Source**: work/active/WI-035_magnet-closure/design.md
        **Ref**: design D6 (rollup + comparison channel); design Risk 1
            (redefinition envelope)
        **Basis**: sum of winding-pack and magnet-structure sub-accounts
        */

        // winding-pack account [$]
        in attribute winding_cost : Real;
        // magnet structure (casing) account [$]
        in attribute structure_cost_in : Real;

        out attribute capital_cost : Real = winding_cost + structure_cost_in;
    }
}
