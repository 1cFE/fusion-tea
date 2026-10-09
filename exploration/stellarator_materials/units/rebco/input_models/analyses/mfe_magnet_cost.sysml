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

    calc def 'Magnet Casing Mass' {
        doc /*
        Casing steel mass per coil [kg] from the coil set's stored magnetic
        energy, anchored at a reference (WI-044):

          m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

        Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
        law from existing machines" (L607) that Stellarator-PROCESS uses for
        the total coil support-structure mass because "the total mass is a
        good proxy, both for the cost and the support structure complexity".
        The source prints no units for the constant, so the constant is
        absorbed by the anchor: m_casing_ref is the instance's casing mass at
        its reference stored energy and only the exponent is carried. The
        anchor keeps whatever seam the instance's reference carries (for
        Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
        design D5); the scale responds to the bore through W_mag and the seam
        stays named at the binding. Disclosed limit (the source's own): the
        law "does not show whether the design point has local unsupportable
        forces" (L609).

        **Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
        **Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
            output.md L607 (the empirical law and its role), L609 (its limit)
        **Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
            concept-agnostic (MR-3) -- all values bound by instances
        */

        // coil-set stored magnetic energy [J]
        in attribute W_mag : Real;
        // reference stored magnetic energy [J]
        in attribute W_mag_ref : Real;
        // reference casing steel mass per coil [kg] at W_mag_ref
        in attribute m_casing_ref : Real;

        out attribute m_casing : Real = m_casing_ref * (W_mag / W_mag_ref) ** 0.78;
    }

    calc def 'Magnet Support Mass' {
        doc /* Total electromagnetic coil-support mass [kg], not a casing split.
        **Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
        knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
        **Reference**: Lion2021 Eq56; Lion2023 Eq2.89 and following MJ/tonne text.
        **Basis**: [AGENT] adopts later source unit convention for earlier fit;
        later fit has different coefficient/exponent. No local stress qualification.
        Native domain: finite c_support>=0; zero coefficient returns dormant0;
        otherwise finite W_mag>=0, e_support>0 and finite output.
        **Last Updated**: 2026-09-15 */
        in attribute W_mag : Real;
        in attribute c_support : Real default 0.0;
        in attribute e_support : Real default 0.78;
        out attribute m_support : Real = 1000.0*c_support*(W_mag/1e6)**e_support;
    }

    calc def 'Magnet Structure Cost'  {
        doc /* Electromagnetic support cost, exclusive total or legacy casing basis.
        cost=(legacy_casing_fraction*n_coils*m_casing+m_support)*steel_price*f_steel_fab.
        The casing output remains an inherited floor diagnostic in total-support mode.
        Native domain: every input finite and nonnegative; legacy_casing_fraction in [0,1]; finite nonnegative outputs with no positive product underflow. Historical multiplication order is preserved. effective_all_in_rate=steel_price*f_steel_fab exposes one assumed all-in rate; the factors do not establish measured material/fabrication subtotals.
        **Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
        **Reference**: D1-D2; T-005_structure_basis.md.
        **Basis**: inherited 6 dollars/kg times 3 = 18 dollars/kg all-in assumption; unknown price year and manufacturing qualification, no demonstrated duplicate removed or sourced casing/intercoil split.
        **Last Updated**: 2026-09-15 */
        in attribute m_support : Real default 0.0;
        in attribute legacy_casing_fraction : Real default 1.0;
        // number of field coils [1]
        in attribute n_coils : Real;
        // casing steel mass per coil [kg] (computed, 'Magnet Casing Mass')
        in attribute m_casing : Real;
        // Historical all-in rate component [$/kg]; no measured stock/fabrication split.
        in attribute steel_price : Real;
        // Historical rate-composition factor [1], not an additional measured fabrication charge.
        in attribute f_steel_fab : Real;

        out attribute effective_all_in_rate : Real = steel_price * f_steel_fab;
        out attribute cost : Real = (legacy_casing_fraction * n_coils * m_casing + m_support) * steel_price * f_steel_fab;
    }

    calc def 'Magnet Capital' {
        doc /*
        CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
        capital is the sum of the separately sized sub-accounts. Kept as a
        calc def so the plant's magnet.capital_cost redefinition stays a
        reference binding (the codegen-proven WI-021 pattern), not an
        arithmetic redefinition expression (dropped by the pinned codegen,
        WI-030).

        **Source**: work/completed/20260901_WI-035_magnet-closure/design.md
        **Ref**: design D6 (rollup + comparison channel); design Risk 1
            (redefinition envelope)
        **Basis**: sum of winding-pack, all-in magnet structure and conditional additional sheet-stock sub-accounts; sheet inclusion in winding remains uncertain (WI-063 design).
        */

        // winding-pack account [$]
        in attribute winding_cost : Real;
        // magnet structure (casing) account [$]
        in attribute structure_cost_in : Real;

        // Conditional incremental sheet stock; zero disables this charge, not manufacturing.
        in attribute insulation_stock_cost : Real default 0.0;
        out attribute capital_cost : Real = winding_cost + structure_cost_in + insulation_stock_cost;
    }
}
