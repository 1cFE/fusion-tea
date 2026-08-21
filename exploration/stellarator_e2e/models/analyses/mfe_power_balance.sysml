package mfe_power_balance {
    private import ScalarValues::*;

    calc def 'MFE Power Balance Calc' {
        doc /*
        MFE (Magnetic Fusion Energy) power balance for tokamaks and
        stellarators: fusion power -> net electric power, engineering Q, and
        recirculating power fraction. Faithful to 1costingFE
        mfe_forward_power_balance in the DEC-free, non-radiation-limited
        regime (validity conditions below).

        Power flow:
          - Alpha / neutron split of fusion power (D-T, inlined)
          - Thermal power = blanket neutron heating + charged-particle (alpha)
            power reaching the wall + heating power + recovered pumping heat
          - Thermal electric via the conversion efficiency eta_th
          - Recirculating power: coils + pumping + subsystems + auxiliary
            + cooling + cryo + wall-plug heating
          - Engineering Q = gross electric / recirculating

        Thermal power derivation (WI-019): 1costingFE step 7 is
          p_th = mn*p_neutron + p_rad + p_wall + eta_p*p_pump   (physics.py:303)
        with p_wall = p_ash + p_input_eff - p_rad at f_dec = 0
        (physics.py:290-299), so p_rad cancels and
          p_th = mn*p_neutron + p_alpha + p_input + eta_p*p_pump.
        Charged-particle power reaches the wall as radiation or as transport;
        both are recovered thermally, so no radiation model is needed here.

        Validity conditions (documented regime, WI-019 MR-WI019-4):
          1. f_dec = 0 -- no direct energy conversion (standing WI-009
             deviation, out of scope).
          2. p_rad - p_alpha <= p_input -- non-radiation-limited, so
             p_input_eff = p_input (physics.py:290). Deep margin for D-T
             (Anchor A point: p_rad 25.7 vs p_alpha 517 MW). Enforcement as
             a viability constraint is deferred to the predictive-physics
             item, which introduces p_rad to the model.

        One further documented deviation from 1costingFE: the fuel-type
        ash/neutron split (physics.py:160-181) is replaced by the inlined
        D-T ratio 3.52/17.58 (p_alpha below; 1costingFE calls it p_ash) so
        this calc stays flat and codegen-safe (no nested calc invocation).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
        **Ref**: physics.py:290-328 (steps 4-14, mfe_forward_power_balance)
        **Basis**: Steady-state MFE power flow; tokamak/stellarator-generic
        */

        // === PRIMARY INPUTS ===
        // Fusion power [MW]
        in attribute p_nrl : Real;
        // Plasma heating power [MW]
        in attribute p_input_in : Real;

        // === EFFICIENCIES ===
        // Neutron energy multiplier (blanket)
        in attribute mn_in : Real;
        // Thermal-to-electric efficiency
        in attribute eta_th_in : Real;
        // Pumping power capture efficiency
        in attribute eta_p_in : Real;
        // Input power wall-plug efficiency
        in attribute eta_pin_in : Real;

        // === PUMPING / SUBSYSTEM POWER ===
        // Primary coolant pumping power [MW]
        in attribute p_pump_in : Real;
        // Subsystem and control fraction
        in attribute f_sub_in : Real;

        // === COIL POWER ===
        // TF coil power [MW]
        in attribute p_tf_in : Real;
        // PF coil power [MW]
        in attribute p_pf_in : Real;

        // === COOLING POWER ===
        // TF coil cooling [MW]
        in attribute p_tfcool_in : Real;
        // PF coil cooling [MW]
        in attribute p_pfcool_in : Real;

        // === AUXILIARY POWER ===
        // Tritium systems [MW]
        in attribute p_trit_in : Real;
        // Housekeeping [MW]
        in attribute p_house_in : Real;
        // Cryogenic pumping [MW]
        in attribute p_cryo : Real;

        // === CALCULATIONS ===

        // D-T alpha (ash) power at full precision: E_alpha / Q = 3.52 / 17.58,
        // the charged-particle fraction of D-T fusion energy, written as the
        // ratio (not a rounded literal) so p_th matches 1costingFE to float
        // precision. Replaces the fuel-type 'Alpha Power Calc'.
        // Source: physics.py:32 (E_ALPHA_DT=3.52), physics.py:34 (Q_DT=17.58),
        //         physics.py:177 (ash_frac = (E_total - E_neutron)/E_total)
        attribute p_alpha : Real = (3.52 / 17.58) * p_nrl;

        // Neutron power. Source: physics.py:179 (p_neutron = p_fus*(1-ash_frac))
        attribute p_neutron : Real = p_nrl - p_alpha;

        // Cooling aggregation.
        attribute p_cool : Real = p_tfcool_in + p_pfcool_in;

        // Auxiliary aggregation. Source: physics.py:294 (p_aux = p_trit+p_house)
        attribute p_aux : Real = p_trit_in + p_house_in;

        // Coil power aggregation (TF + PF).
        attribute p_coils : Real = p_tf_in + p_pf_in;

        // Thermal power: blanket neutron heating + alpha power reaching the
        // wall + heating power + recovered pumping heat. Collapsed form of
        // 1costingFE steps 4-7 (derivation in the header doc). Exposed as an
        // output so the plant cost spine scales with the forward-computed
        // thermal power (WI-010).
        // Source: physics.py:290-303 (p_input_eff, p_transport, p_wall, p_th)
        out attribute p_th : Real =
            mn_in * p_neutron + p_alpha + p_input_in + eta_p_in * p_pump_in;

        // Thermal electric power. Exposed for the plant cost spine (WI-010).
        // Source: physics.py:306 (p_the = eta_th*p_th)
        out attribute p_the : Real = eta_th_in * p_th;

        // Gross electric (no direct conversion). Exposed for the plant cost
        // spine (WI-010). Source: physics.py:309 (p_et, p_dee=0 here)
        out attribute p_et : Real = p_the;

        // Subsystem power. Source: physics.py:315 (p_sub = f_sub * p_et)
        attribute p_sub : Real = f_sub_in * p_et;

        // Recirculating power.
        // Source: physics.py:321-323
        attribute recirculating : Real =
            p_coils + p_pump_in + p_sub + p_aux + p_cool + p_cryo
            + p_input_in / eta_pin_in;

        // === OUTPUTS ===

        // Engineering Q. Source: physics.py:324 (q_eng = p_et / recirculating)
        out attribute q_eng : Real = p_et / recirculating;

        // Recirculating fraction. Source: physics.py:327 (rec_frac = 1/q_eng)
        out attribute rec_frac : Real = 1.0 / q_eng;

        // Net electric power [MW]. Source: physics.py:328 (p_net=(1-rec_frac)*p_et)
        out attribute p_net : Real = (1.0 - rec_frac) * p_et;
    }
}
