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

    calc def 'Buildings Cost' {
        doc /*
        CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
        once over the direct sum). Exact 6-term grouped collapse of the
        1costingFE 18-building loop (WI-025): every building is linear in
        exactly one scaling basis, so the loop groups into base-cost sums per
        basis. Grouping is exact linear algebra, not a fit (design-stage proof:
        bit-identical to the pinned loop at float64 at the executed powers).
        p_the = p_et for a no-DEC plant (costs.py:104) — documented where the
        instance binds. Base sums are concept inputs (fuel-keyed, MR-3);
        reference powers are 1cfe calibration constants.
          cost = fixed_base + fus_base*(p_fus*n_mod/p_fus_ref)
               + staff_base*(p_et*n_mod/p_et_ref)**0.5
               + the_base*(p_the*n_mod/p_the_ref)
               + th_base*(p_th*n_mod/p_th_ref) + et_base*(p_et*n_mod/p_et_ref)
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:83-144 (cas21_buildings; scale_map :121-130, refs
            :102-106, SC cryogenics gate :137); costing_constants.yaml:175-197
        **Basis**: exact linear grouping of the per-building loop (WI-025 D1)
        */

        in attribute fixed_base : Real;   // sum of fixed-basis base costs [$]
        in attribute fus_base : Real;     // sum of p_fus-scaled base costs [$]
        in attribute staff_base : Real;   // sum of staff-scaled base costs [$]
        in attribute the_base : Real;     // sum of p_the-scaled base costs [$]
        in attribute th_base : Real;      // sum of p_th-scaled base costs [$]
        in attribute et_base : Real;      // sum of p_et-scaled base costs [$]
        in attribute p_fus : Real;        // fusion power [MW]
        in attribute p_the : Real;        // thermal-electric power [MW]
        in attribute p_th : Real;         // total thermal power [MW]
        in attribute p_et : Real;         // gross electric power [MW]

        // Module count (plant-total powers). Frozen n_mod = 1 at the demo
        // design point (WI-025 checkpoint ruling 1). Source: costs.py:109-112.
        in attribute n_mod : Real default 1.0;
        // Calibration reference powers. Source: costs.py:105 (P_TH_REF=2500),
        // :106 (P_FUS_REF=2300); costing_constants.yaml:12 (ref_gross 1100,
        // used for both p_et and p_the — no-DEC).
        in attribute p_fus_ref : Real default 2300.0;
        in attribute p_the_ref : Real default 1100.0;
        in attribute p_th_ref : Real default 2500.0;
        in attribute p_et_ref : Real default 1100.0;

        out attribute cost : Real =
            fixed_base
            + fus_base * (p_fus * n_mod / p_fus_ref)
            + staff_base * (p_et * n_mod / p_et_ref) ** 0.5
            + the_base * (p_the * n_mod / p_the_ref)
            + th_base * (p_th * n_mod / p_th_ref)
            + et_base * (p_et * n_mod / p_et_ref);
    }

    calc def 'Preconstruction Cost' {
        doc /*
        CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
        plant-total net electric, anchored at ref_net_power) plus the fixed
        adders (permits + licensing + studies + reports + other — fuel/FOAK-
        keyed, so a concept input). costs.py:79 adds CAS10's own contingency;
        deliberately NOT carried here — the plant's CAS29 applies contingency
        once over the direct sum (convention preserved, MR-WI025-3; design-
        stage check: 1cfe full CAS10 = this subtotal x 1.10 exactly).
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:52-80 (cas10_preconstruction);
            costing_constants.yaml:8, :15-23
        **Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)
        */

        in attribute fixed_precon : Real;  // fixed adders, fuel/FOAK-keyed [$]
        in attribute p_net : Real;         // net electric power [MW]

        // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:64.
        in attribute n_mod : Real default 1.0;
        // Land calibration. Source: costing_constants.yaml:21 (0.25 acres/MWe
        // at ref), :22 ($10000/acre), :8 (ref_net_power_mwe 1000).
        in attribute land_intensity : Real default 0.25;
        in attribute land_cost : Real default 10000.0;
        in attribute ref_net_power : Real default 1000.0;

        out attribute cost : Real =
            land_intensity * (p_net * n_mod * ref_net_power) ** 0.5 * land_cost
            + fixed_precon;
    }

    calc def 'Annual OM Cost' {
        doc /*
        CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
        concept input) scaled by sqrt of plant-total net electric. CAS71
        inflation levelization and CAS72 scheduled replacement are documented
        Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
        om_direct is an additive direct term for concepts that specify O&M
        outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
        and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
        exact identity, the handshake injection path — WI-025 D5/D6).
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:319-357 (cas70_om; annual line :353);
            costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
        **Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)
        */

        in attribute om_ref : Real;        // annual O&M at ref power, fuel-keyed [$/yr]
        in attribute p_net : Real;         // net electric power [MW]

        // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:353.
        in attribute n_mod : Real default 1.0;
        // Source: costing_constants.yaml:8 (ref_net_power_mwe 1000).
        in attribute ref_net_power : Real default 1000.0;
        // Staffing economy-of-scale exponent. Source: costs.py:353 (** 0.5).
        in attribute alpha : Real default 0.5;
        in attribute om_direct : Real default 0.0;  // directly-specified O&M (additive)

        out attribute annual_om : Real =
            om_ref * (p_net * n_mod / ref_net_power) ** alpha + om_direct;
    }
}
