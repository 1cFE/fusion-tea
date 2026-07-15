package mfe_power_balance {
    private import ScalarValues::*;

    calc def 'MFE Power Balance Calc' {
        doc /*
        MFE (Magnetic Fusion Energy) power balance for tokamaks and
        stellarators: fusion power -> net electric power, engineering Q, and
        recirculating power fraction.

        Power flow:
          - Alpha / neutron split of fusion power (D-T, inlined)
          - Thermal power = neutron heating + input + recovered pumping heat
          - Thermal electric via the conversion efficiency eta_th
          - Recirculating power: coils + pumping + subsystems + auxiliary
            + cooling + cryo + wall-plug heating
          - Engineering Q = gross electric / recirculating

        Two documented deviations from the base PyFECONS balance:
          1. Direct energy conversion (p_dee, eta_de) is dropped, as in the
             archived revival base and the WI-009 spec (out of scope).
          2. The fuel-type-dependent 'Alpha Power Calc' is replaced by an
             inlined D-T alpha fraction (see p_alpha below) so this calc stays
             flat and codegen-safe (no nested calc invocation).
        The top-level q_eng / rec_frac / p_net relations follow current
        1costingFE (physics.py:324-328), not the older archived q_eng
        numerator.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
        **Ref**: physics.py:183-328 (mfe_forward_power_balance)
        **Basis**: Steady-state MFE power flow; tokamak/stellarator-generic
        */

        // === PRIMARY INPUTS ===
        in attribute p_nrl : Real;      // Fusion power [MW]
        in attribute p_input : Real;    // Plasma heating power [MW]

        // === EFFICIENCIES ===
        in attribute mn : Real;         // Neutron energy multiplier (blanket)
        in attribute eta_th : Real;     // Thermal-to-electric efficiency
        in attribute eta_p : Real;      // Pumping power capture efficiency
        in attribute eta_pin : Real;    // Input power wall-plug efficiency

        // === POWER FRACTIONS ===
        in attribute fpcppf : Real;     // Primary coolant pumping power fraction
        in attribute f_sub : Real;      // Subsystem and control fraction

        // === COIL POWER ===
        in attribute p_tf : Real;       // TF coil power [MW]
        in attribute p_pf : Real;       // PF coil power [MW]

        // === COOLING POWER ===
        in attribute p_tfcool : Real;   // TF coil cooling [MW]
        in attribute p_pfcool : Real;   // PF coil cooling [MW]

        // === AUXILIARY POWER ===
        in attribute p_trit : Real;     // Tritium systems [MW]
        in attribute p_house : Real;    // Housekeeping [MW]
        in attribute p_cryo : Real;     // Cryogenic pumping [MW]

        // === CALCULATIONS ===

        // D-T alpha power: 0.2002 = E_alpha / Q = 3.52 MeV / 17.58 MeV, the
        // charged-particle (ash) fraction of D-T fusion energy. Replaces the
        // fuel-type 'Alpha Power Calc' with an inlined D-T constant.
        // Source: physics.py:32 (E_ALPHA_DT=3.52), physics.py:34 (Q_DT=17.58),
        //         physics.py:177 (ash_frac = (E_total - E_neutron)/E_total)
        attribute p_alpha : Real = 0.2002 * p_nrl;

        // Neutron power. Source: physics.py:179 (p_neutron = p_fus*(1-ash_frac))
        attribute p_neutron : Real = p_nrl - p_alpha;

        // Cooling aggregation.
        attribute p_cool : Real = p_tfcool + p_pfcool;

        // Auxiliary aggregation. Source: physics.py:294 (p_aux = p_trit+p_house)
        attribute p_aux : Real = p_trit + p_house;

        // Coil power aggregation (TF + PF).
        attribute p_coils : Real = p_tf + p_pf;

        // Thermal power (neutron heating + input + recovered pumping heat).
        // Exposed as an output so the plant cost spine scales with the
        // forward-computed thermal power (WI-010).
        // Source: archived PyFECONS PowerBalance.py:15-21 (DEC-free form)
        out attribute p_th : Real =
            mn * p_neutron + p_input
            + eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron);

        // Thermal electric power. Exposed for the plant cost spine (WI-010).
        // Source: physics.py:306 (p_the = eta_th*p_th)
        out attribute p_the : Real = eta_th * p_th;

        // Gross electric (no direct conversion). Exposed for the plant cost
        // spine (WI-010). Source: physics.py:309 (p_et, p_dee=0 here)
        out attribute p_et : Real = p_the;

        // Pumping power. Source: archived PowerBalance.py:26 (p_pump=fpcppf*p_the)
        attribute p_pump : Real = fpcppf * p_the;

        // Subsystem power. Source: physics.py:315 (p_sub = f_sub * p_et)
        attribute p_sub : Real = f_sub * p_the;

        // Recirculating power.
        // Source: physics.py:321-323
        attribute recirculating : Real =
            p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo
            + p_input / eta_pin;

        // === OUTPUTS ===

        // Engineering Q. Source: physics.py:324 (q_eng = p_et / recirculating)
        out attribute q_eng : Real = p_et / recirculating;

        // Recirculating fraction. Source: physics.py:327 (rec_frac = 1/q_eng)
        out attribute rec_frac : Real = 1.0 / q_eng;

        // Net electric power [MW]. Source: physics.py:328 (p_net=(1-rec_frac)*p_et)
        out attribute p_net : Real = (1.0 - rec_frac) * p_et;
    }
}
