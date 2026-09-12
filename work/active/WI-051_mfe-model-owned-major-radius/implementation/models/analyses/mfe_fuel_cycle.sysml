package mfe_fuel_cycle {
    private import ScalarValues::*;

    calc def 'Fuel Cycle Flows' {
        doc /*
        Tritium flows of a D-T plant, reduced to conservation (WI-047):

          E_fus_J         = q_eff * mev_to_joules                        [J]
          burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
          inject_rate     = burn_rate / burn_fraction                    [atoms/s]
          exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
          loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
          tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                            / (eta_extract * burn_rate)                  [1]
          tbr_margin      = tbr_available - tbr_required                 [1]
          burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

        One D-T reaction burns one tritium atom; the fusion power fixes the burn,
        the single-pass burn fraction fixes the circulating stream, and the recovery
        of the unburned stream fixes the permanent loss. The required breeding ratio
        is the tritium that must be bred per atom burned to replace burn, permanent
        loss, decay of the held inventory and any stock growth, divided by the
        extraction efficiency from breeder to usable supply. The margin against the
        ACHIEVED ratio a concept binds is a REPORTED adequacy quantity: no fence reads
        it (the achieved ratio is a source-conditioned input at the source's own
        geometry, and the recovery semantics are an open owner decision -- see the
        instance binding of t_recycle).

        Inventory and startup stock are NOT computed here: I_total, G_stock and
        eta_extract are dormant (0, 0, 1) until residence times, extraction
        efficiency and a reserve policy have an admissible source (retrieval target:
        Lord et al., UKAEA-STEP-PR(24)12). A duty factor multiplies operating burns
        and flows in the plant (the calendar's productive time); stock decays through
        calendar time too -- the two clocks are the lifecycle calc's, not this one's.

        This calc computes REQUIRED breeding, never achieved neutronics: rubric Row
        2c stays bounded at the source geometry. 'DT Fuel Cost' (mfe_account_costs)
        keeps its own burn correction on the same burn_fraction and the same
        recovery number read as a feedstock cost factor; the two calcs read the
        same inputs and mean different things, and say so.

        Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

        **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
        **Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
            half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
            58 (startup as a residence-time balance, not computed here), 60 (the
            conditional 1.19 finding)
        **Basis**: Tritium conservation on the burned, circulating and bred streams
        */

        // fusion power [MW]
        in attribute p_fus_in : Real;
        // per-reaction energy [MeV] and the MeV -> J conversion -- the same two
        // formals 'DT Fuel Cost' takes, so the burn and the fuel cost count the same
        // reactions (the product is formed here; a product on a calc-input binding
        // is not a resolvable reference on the exact route -- WI-047 phase 1)
        in attribute q_eff_in : Real;
        in attribute mev_to_joules_in : Real;
        // single-pass burn fraction [1], 0 < burn_fraction_in <= 1
        in attribute burn_fraction_in : Real;
        // recovery fraction of the unburned tritium stream [1], 0 <= t_recycle_in <= 1
        in attribute t_recycle_in : Real;
        // achieved tritium breeding ratio [1] (a concept's source-conditioned value)
        in attribute tbr_available_in : Real;
        // breeder-to-supply extraction efficiency [1], 0 < eta_extract_in <= 1 (dormant 1.0)
        in attribute eta_extract_in : Real;
        // tritium decay constant [1/s] (an instance input derived from the half-life)
        in attribute lambda_T_in : Real;
        // total held tritium inventory [atoms] (dormant 0.0: residence times unsourced)
        in attribute I_total_in : Real;
        // required stock growth [atoms/s] (dormant 0.0: a single mature plant)
        in attribute G_stock_in : Real;
        // tritium atomic mass [kg] (an instance input with its derivation)
        in attribute m_T_kg_in : Real;
        // seconds per full-power year [s]: 8760 h x 3600 s, the model's own year
        // ('LCOE DCF' 8760.0; 'DT Fuel Cost' 3600.0 * 8760.0)
        in attribute s_per_fpy_in : Real default 31536000.0;

        // energy per D-T reaction [J]
        attribute E_fus_J : Real = q_eff_in * mev_to_joules_in;

        out attribute burn_rate : Real = p_fus_in * 1.0e6 / E_fus_J;
        out attribute inject_rate : Real = burn_rate / burn_fraction_in;
        out attribute exhaust_rate : Real = inject_rate - burn_rate;
        out attribute loss_rate : Real = (1.0 - t_recycle_in) * exhaust_rate;
        out attribute tbr_required : Real =
            (burn_rate + loss_rate + lambda_T_in * I_total_in + G_stock_in) / (eta_extract_in * burn_rate);
        out attribute tbr_margin : Real = tbr_available_in - tbr_required;
        out attribute burn_kg_per_fpy : Real = burn_rate * m_T_kg_in * s_per_fpy_in;
    }
}
