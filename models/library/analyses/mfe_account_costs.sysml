package mfe_account_costs {
    private import ScalarValues::*;

    // =========================================================================
    // Concept-agnostic steady-state CAS account cost scalings (MFE)
    //
    // Each calc reproduces (does not call) a 1costingFE steady-state per-account
    // cost function that fits the codegen envelope: flat all-Real arithmetic,
    // operators + - * / **, no exp/if/lookup/sum/nested-calc. Concept-varying
    // unit costs, volumes, and powers are plain inputs (WI-011 binds them);
    // calibration constants (reference powers, scaling exponents, unit
    // conversions) are defaulted inputs carrying their 1costingFE citation.
    //
    // MONEY UNIT: these formulas are unit-transparent — the output money unit
    // equals the money unit of the supplied unit-cost input. The generic_mfe
    // plant rolls up in DOLLARS ($), so WI-011 supplies unit costs in $ (the
    // 1costingFE constants are M$; multiply by 1e6). This matches WI-009's
    // 'Magnet Coil Cost', which omits the 1costingFE /1e6 M$ conversion and so
    // already yields $. See the plant doc for the unit handshake note.
    // =========================================================================

    calc def 'Blanket Cost' {
        doc /*
        CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
        volume x thermal-power scaling:

          cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

        `unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
        (fuel-keyed table with a Li2O override in the source); `structure_factor`
        is the blanket-form multiplier. Both are concept inputs (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
        **Basis**: Volume-based blanket cost with thermal-intensity power law
        */

        in attribute unit_cost : Real;
        in attribute structure_factor : Real;
        in attribute blanket_vol : Real;
        in attribute p_th : Real;

        // Thermal-power calibration point. Source: cas22.py:223 (P_TH_REF=2500.0).
        in attribute p_th_ref : Real default 2500.0;
        // Thermal-intensity exponent. Source: cas22.py:254 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * structure_factor * blanket_vol * (p_th / p_th_ref) ** alpha;
    }

    calc def 'Shield Cost' {
        doc /*
        CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
        scaling with a fuel-dependent shield-mass scale factor:

          cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

        `shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
        pB11 0.1 in the source) — a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
        **Basis**: Volume-based shield cost with fuel neutron-load scale
        */

        in attribute unit_cost : Real;
        in attribute shield_vol : Real;
        in attribute shield_scale : Real;
        in attribute p_th : Real;

        // Thermal-power calibration point. Source: cas22.py:223 (P_TH_REF=2500.0).
        in attribute p_th_ref : Real default 2500.0;
        // Thermal-intensity exponent. Source: cas22.py:269 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * shield_vol * shield_scale * (p_th / p_th_ref) ** alpha;
    }

    calc def 'Structure Cost' {
        doc /*
        CAS22.1.5 Primary structure (gravity supports, thermal shields,
        inter-coil structure, machine base) cost. Volume x gross-electric
        scaling:

          cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
        **Basis**: Volume-based structure cost with gross-electric power law
        */

        in attribute unit_cost : Real;
        in attribute structure_vol : Real;
        in attribute p_et : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224
        // (P_ET_REF = ref_gross_power_mwe), costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:501 (** 0.5).
        in attribute alpha : Real default 0.5;

        out attribute cost : Real =
            unit_cost * structure_vol * (p_et / p_et_ref) ** alpha;
    }

    calc def 'Vessel Cost' {
        doc /*
        CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
        extensions, gauges, leak detection). Volume x gross-electric scaling:

          cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

        Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
        The gas-load pumping sub-term (c220106_pump) is a within-envelope but
        input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
        NBI/fueling throughput); it is omitted here and left for Stage-3
        deepening. See the plant doc's initial-model-limitations note.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
        **Basis**: Volume-based vessel-shell cost with gross-electric power law
        */

        in attribute unit_cost : Real;
        in attribute vessel_vol : Real;
        in attribute p_et : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224,
        // costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:515 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * vessel_vol * (p_et / p_et_ref) ** alpha;
    }

    calc def 'Power Supplies Cost' {
        doc /*
        CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
        switchgear). Power-law in gross electric:

          cost = base * (p_et/p_et_ref)^alpha

        `base` is the account cost at the calibration power (power_supplies_base,
        M$ at 1 GWe in the source) — a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
        **Basis**: Power-scaled power-supply cost
        */

        in attribute base : Real;
        in attribute p_et : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224,
        // costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:554 (** 0.7).
        in attribute alpha : Real default 0.7;

        out attribute cost : Real =
            base * (p_et / p_et_ref) ** alpha;
    }

    calc def 'Divertor Cost' {
        doc /*
        CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
        steady-state MFE. Power-law in thermal power:

          cost = base * (p_th/p_th_ref)^alpha

        `base` is the account cost at the 1 GWth calibration point
        (divertor_base) — a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
        **Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory
        */

        in attribute base : Real;
        in attribute p_th : Real;

        // Thermal-power calibration point [MWth]. Source: cas22.py:570 (/1000.0
        // = 1 GWth).
        in attribute p_th_ref : Real default 1000.0;
        // Exponent. Source: cas22.py:570 (** 0.5).
        in attribute alpha : Real default 0.5;

        out attribute cost : Real =
            base * (p_th / p_th_ref) ** alpha;
    }

    calc def 'Heating Cost' {
        doc /*
        CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
        Sum of per-method installed power times per-MW cost:

          cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
               + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

        All per-MW rates and delivered powers are the concept heating mix
        (WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:454-459 (c220104 steady-state)
        **Basis**: Linear per-method heating capital; MFE analogue of IFE ignition
        */

        in attribute nbi_per_mw : Real;
        in attribute p_nbi : Real;
        in attribute icrf_per_mw : Real;
        in attribute p_icrf : Real;
        in attribute ecrh_per_mw : Real;
        in attribute p_ecrh : Real;
        in attribute lhcd_per_mw : Real;
        in attribute p_lhcd : Real;

        out attribute cost : Real =
            nbi_per_mw * p_nbi + icrf_per_mw * p_icrf
            + ecrh_per_mw * p_ecrh + lhcd_per_mw * p_lhcd;
    }

    calc def 'Linear Power Cost' {
        doc /*
        Generic balance-of-plant account cost linear in plant-total power:

          cost = n_mod * power * cost_per_mw

        Reused for the four flat BOP accounts, each with its own driving power
        and per-MW unit cost (concept/power-cycle inputs, WI-011):
          - Turbine plant       : power = p_the,  turbine_per_mw
          - Electric plant      : power = p_et,   electric_per_mw
          - Heat rejection      : power = p_th,   heat_rej_per_mw
          - Miscellaneous plant : power = p_et,   misc_per_mw

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
        **Basis**: Balance-of-plant cost linear in plant-total driving power
        */

        in attribute power : Real;
        in attribute cost_per_mw : Real;

        // Module count (plant-total = n_mod x per-module). Source: costs.py:154
        // (n_mod factor); single-module demo baseline.
        in attribute n_mod : Real default 1.0;

        out attribute cost : Real =
            n_mod * power * cost_per_mw;
    }

    calc def 'Contingency Cost' {
        doc /*
        CAS29 contingency on direct costs:

          cost = contingency_rate * direct_subtotal

        `contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
        source) — a concept/maturity input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:220 (cas29_contingency)
        **Basis**: Fractional contingency on the direct-cost subtotal
        */

        in attribute contingency_rate : Real;
        in attribute direct_subtotal : Real;

        out attribute cost : Real =
            contingency_rate * direct_subtotal;
    }

    calc def 'Indirect Cost' {
        doc /*
        CAS30 indirect service costs, a fraction of total direct cost scaled by
        construction time relative to a reference duration:

          cost = indirect_fraction * direct_cost
               * (construction_time / reference_construction_time)

        `indirect_fraction` (0.20 of direct in the source) is a concept input.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:231-236 (cas30_indirect)
        **Basis**: Direct-cost fraction scaled by construction-time ratio
        */

        in attribute indirect_fraction : Real;
        in attribute direct_cost : Real;
        in attribute construction_time : Real;

        // Construction-time scaling baseline [yr]. Source: costs.py:235
        // (reference_construction_time), costing_constants.yaml:239 (=6.0).
        in attribute reference_construction_time : Real default 6.0;

        out attribute cost : Real =
            indirect_fraction * direct_cost
            * (construction_time / reference_construction_time);
    }
}
