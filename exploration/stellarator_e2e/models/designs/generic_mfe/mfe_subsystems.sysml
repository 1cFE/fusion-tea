package mfe_subsystems {
    private import ScalarValues::*;
    private import cas_hierarchy::*;
    private import economic_parameter::'CAS Scope';

    // =========================================================================
    // Shared power-core and balance-of-plant costed components for the generic
    // MFE plant. These are the concept-agnostic accounts NOT already defined by
    // WI-009's mfe_power_core (which owns the mfe-divergent 'Magnet System',
    // 'Heating and CD', 'Divertor'). Each specializes a cas_hierarchy account
    // type and carries its cost-driver attributes, mirroring the WI-009 magnet
    // pattern and the ife_subsystems costed-component idiom. All attributes are
    // concept inputs (WI-011); `capital_cost` (inherited from 'Costed
    // Component') is populated by the matching mfe_account_costs calc, bound in
    // the plant. No concept-specific values here (MR-3).
    //
    // CAS numbering note: this file follows the project cas_hierarchy
    // (CAS23 turbine, CAS24 electric, CAS25 heat rejection, CAS26 misc). The
    // 1costingFE source swaps 25/26 (CAS25 misc, CAS26 heat rejection); the
    // account_name and cost basis are preserved, only the CAS integer follows
    // the project convention.
    // =========================================================================

    // --- Shared power-core sub-accounts (CAS22.1.x, scope = shared) ---

    part def 'Blanket' :> 'CAS22 Power Core' {
        doc /*
        CAS22.1.1 First wall + breeding blanket + neutron multiplier.
        Concept-agnostic shared power-core account. Cost drivers below feed
        'Blanket Cost' (mfe_account_costs); WI-011 sets the values.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:252-254 (c220101)
        **Basis**: DI-002 — blanket is a shared (concept-agnostic) CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute structure_factor : Real;
        attribute blanket_vol : Real;
    }

    part def 'Shield' :> 'CAS22 Power Core' {
        doc /*
        CAS22.1.2 Shield (high-temperature + low-temperature + bioshield).
        Concept-agnostic shared power-core account. Cost drivers feed
        'Shield Cost'.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:267-269 (c220102)
        **Basis**: DI-002 — shield is a shared (concept-agnostic) CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute shield_scale : Real;
        attribute shield_vol : Real;
    }

    part def 'Primary Structure' :> 'CAS22 Power Core' {
        doc /*
        CAS22.1.5 Primary structure and support (gravity supports, thermal
        shields, inter-coil structure, machine base). Cost drivers feed
        'Structure Cost'.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:501 (c220105)
        **Basis**: DI-002 — primary structure is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute structure_vol : Real;
    }

    part def 'Vacuum Vessel' :> 'CAS22 Power Core' {
        doc /*
        CAS22.1.6 Vacuum vessel (double-walled SS chamber, ports, gauges).
        Cost drivers feed 'Vessel Cost' (vessel-shell term only; the gas-load
        pumping term is a Stage-3 deepening item).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:515 (c220106_vessel)
        **Basis**: DI-002 — vacuum vessel is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute vessel_vol : Real;
    }

    part def 'Power Supplies' :> 'CAS22 Power Core' {
        doc /*
        CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
        switchgear). Cost driver feeds 'Power Supplies Cost'.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:554 (c220107 steady-state)
        **Basis**: DI-002 — power supplies is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute base : Real;
    }

    // --- Balance-of-plant accounts (CAS23-26, scope = shared) ---

    part def 'Turbine Plant' :> 'CAS23 Turbine Plant' {
        doc /*
        CAS23 Turbine plant equipment (steam TG, condenser, feedwater). Linear
        in thermal-electric power; cost driver feeds 'Linear Power Cost' with
        power = p_the.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:154 (cas23_turbine)
        **Basis**: Concept-agnostic thermal conversion, power-cycle-set $/MW
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
    }

    part def 'Electric Plant' :> 'CAS24 Electric Plant' {
        doc /*
        CAS24 Electric plant equipment (switchyard, transformers, cabling).
        Linear in gross electric; feeds 'Linear Power Cost' with power = p_et.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:162 (cas24_electrical)
        **Basis**: Concept-agnostic electric plant, scales with gross electric
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
    }

    part def 'Heat Rejection' :> 'CAS25 Heat Rejection' {
        doc /*
        CAS25 Heat rejection (cooling towers, circulating water). Linear in
        total thermal power; feeds 'Linear Power Cost' with power = p_th.
        (1costingFE numbers this account CAS26 — see file header note.)

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:179 (cas26_heat_rejection)
        **Basis**: Concept-agnostic heat rejection, scales with thermal power
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
    }

    part def 'Miscellaneous Plant' :> 'CAS26 Miscellaneous' {
        doc /*
        CAS26 Miscellaneous plant equipment (fire protection, compressed air,
        HVAC). Linear in gross electric; feeds 'Linear Power Cost' with
        power = p_et. (1costingFE numbers this account CAS25 — see header note.)

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:170 (cas25_misc)
        **Basis**: Concept-agnostic miscellaneous plant, scales with gross electric
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
    }

    // --- Buildings (CAS21, pass-through) ---

    part def 'Buildings' :> 'CAS21 Structures' {
        doc /*
        CAS21 Buildings and site facilities. The 1costingFE building model is a
        per-building dictionary loop with fuel-keyed base costs and per-building
        scaling bases (out of the codegen envelope: needs sum/lookup). Its cost
        is therefore a plant INPUT (`capital_cost` set directly), a documented
        initial-model pass-through for Stage-3 deepening.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:97-152 (cas21_buildings — dict loop, out of envelope)
        **Basis**: Pass-through; buildings model needs sum/lookup constructs
        */
        :>> scope = 'CAS Scope'::shared;
    }
}
