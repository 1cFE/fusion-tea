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
    // MONEY UNIT: these formulas are unit-transparent -- the output money unit
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
        in attribute p_th_in : Real;

        // Thermal-power calibration point. Source: cas22.py:223 (P_TH_REF=2500.0).
        in attribute p_th_ref : Real default 2500.0;
        // Thermal-intensity exponent. Source: cas22.py:254 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * structure_factor * blanket_vol * (p_th_in / p_th_ref) ** alpha;
    }

    calc def 'Shield Cost' {
        doc /*
        CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
        scaling with a fuel-dependent shield-mass scale factor:

          cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

        `shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
        pB11 0.1 in the source) -- a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
        **Basis**: Volume-based shield cost with fuel neutron-load scale
        */

        in attribute unit_cost : Real;
        in attribute shield_vol : Real;
        in attribute shield_scale : Real;
        in attribute p_th_in : Real;

        // Thermal-power calibration point. Source: cas22.py:223 (P_TH_REF=2500.0).
        in attribute p_th_ref : Real default 2500.0;
        // Thermal-intensity exponent. Source: cas22.py:269 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * shield_vol * shield_scale * (p_th_in / p_th_ref) ** alpha;
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
        in attribute p_et_in : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224
        // (P_ET_REF = ref_gross_power_mwe), costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:501 (** 0.5).
        in attribute alpha : Real default 0.5;

        out attribute cost : Real =
            unit_cost * structure_vol * (p_et_in / p_et_ref) ** alpha;
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
        in attribute p_et_in : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224,
        // costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:515 (** 0.6).
        in attribute alpha : Real default 0.6;

        out attribute cost : Real =
            unit_cost * vessel_vol * (p_et_in / p_et_ref) ** alpha;
    }

    calc def 'Power Supplies Cost' {
        doc /*
        CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
        switchgear). Power-law in gross electric:

          cost = base * (p_et/p_et_ref)^alpha

        `base` is the account cost at the calibration power (power_supplies_base,
        M$ at 1 GWe in the source) -- a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
        **Basis**: Power-scaled power-supply cost
        */

        in attribute base : Real;
        in attribute p_et_in : Real;

        // Gross-electric calibration point [MWe]. Source: cas22.py:224,
        // costing_constants.yaml:12 (=1100.0).
        in attribute p_et_ref : Real default 1100.0;
        // Exponent. Source: cas22.py:554 (** 0.7).
        in attribute alpha : Real default 0.7;

        out attribute cost : Real =
            base * (p_et_in / p_et_ref) ** alpha;
    }

    calc def 'Divertor Cost' {
        doc /*
        CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
        steady-state MFE. Power-law in thermal power:

          cost = base * (p_th/p_th_ref)^alpha

        `base` is the account cost at the 1 GWth calibration point
        (divertor_base) -- a concept input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
        **Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory
        */

        in attribute base : Real;
        in attribute p_th_in : Real;

        // Thermal-power calibration point [MWth]. Source: cas22.py:570 (/1000.0
        // = 1 GWth).
        in attribute p_th_ref : Real default 1000.0;
        // Exponent. Source: cas22.py:570 (** 0.5).
        in attribute alpha : Real default 0.5;

        out attribute cost : Real =
            base * (p_th_in / p_th_ref) ** alpha;
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
        in attribute p_nbi_in : Real;
        in attribute icrf_per_mw : Real;
        in attribute p_icrf_in : Real;
        in attribute ecrh_per_mw : Real;
        in attribute p_ecrh_in : Real;
        in attribute lhcd_per_mw : Real;
        in attribute p_lhcd_in : Real;

        out attribute cost : Real =
            nbi_per_mw * p_nbi_in + icrf_per_mw * p_icrf_in
            + ecrh_per_mw * p_ecrh_in + lhcd_per_mw * p_lhcd_in;
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
        in attribute n_mod_in : Real default 1.0;

        out attribute cost : Real =
            n_mod_in * power * cost_per_mw;
    }

    calc def 'Contingency Cost' {
        doc /*
        CAS29 contingency on direct costs:

          cost = contingency_rate * direct_subtotal

        `contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
        source) -- a concept/maturity input (WI-011).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:220 (cas29_contingency)
        **Basis**: Fractional contingency on the direct-cost subtotal
        */

        in attribute contingency_rate_in : Real;
        in attribute direct_subtotal : Real;

        out attribute cost : Real =
            contingency_rate_in * direct_subtotal;
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

        in attribute indirect_fraction_in : Real;
        in attribute direct_cost : Real;
        in attribute construction_time : Real;

        // Construction-time scaling baseline [yr]. Source: costs.py:235
        // (reference_construction_time), costing_constants.yaml:239 (=6.0).
        in attribute reference_construction_time : Real default 6.0;

        out attribute cost : Real =
            indirect_fraction_in * direct_cost
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
        p_the = p_et for a no-DEC plant (costs.py:104) -- documented where the
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

        // sum of fixed-basis base costs [$]
        in attribute fixed_base : Real;
        // sum of p_fus-scaled base costs [$]
        in attribute fus_base : Real;
        // sum of staff-scaled base costs [$]
        in attribute staff_base : Real;
        // sum of p_the-scaled base costs [$]
        in attribute the_base : Real;
        // sum of p_th-scaled base costs [$]
        in attribute th_base : Real;
        // sum of p_et-scaled base costs [$]
        in attribute et_base : Real;
        // fusion power [MW]
        in attribute p_fus : Real;
        // thermal-electric power [MW]
        in attribute p_the_in : Real;
        // total thermal power [MW]
        in attribute p_th_in : Real;
        // gross electric power [MW]
        in attribute p_et_in : Real;

        // Module count (plant-total powers). Frozen n_mod = 1 at the demo
        // design point (WI-025 checkpoint ruling 1). Source: costs.py:109-112.
        in attribute n_mod_in : Real default 1.0;
        // Calibration reference powers. Source: costs.py:105 (P_TH_REF=2500),
        // :106 (P_FUS_REF=2300); costing_constants.yaml:12 (ref_gross 1100,
        // used for both p_et and p_the -- no-DEC).
        in attribute p_fus_ref : Real default 2300.0;
        in attribute p_the_ref : Real default 1100.0;
        in attribute p_th_ref : Real default 2500.0;
        in attribute p_et_ref : Real default 1100.0;

        out attribute cost : Real =
            fixed_base
            + fus_base * (p_fus * n_mod_in / p_fus_ref)
            + staff_base * (p_et_in * n_mod_in / p_et_ref) ** 0.5
            + the_base * (p_the_in * n_mod_in / p_the_ref)
            + th_base * (p_th_in * n_mod_in / p_th_ref)
            + et_base * (p_et_in * n_mod_in / p_et_ref);
    }

    calc def 'Preconstruction Cost' {
        doc /*
        CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
        plant-total net electric, anchored at ref_net_power) plus the fixed
        adders (permits + licensing + studies + reports + other -- fuel- and
        FOAK/NOAK-keyed, so a concept input). costs.py:79 adds CAS10's own
        contingency; deliberately NOT carried here -- the plant's CAS29 applies
        contingency once over the direct sum (convention preserved, MR-WI025-3).
        WI-029 doc correction: the old note "1cfe full CAS10 = this subtotal
        x 1.10 exactly" was a stale FOAK reading. At NOAK -- the regime both the
        design and handshake points run -- contingency_rate_noak = 0.0, so 1cfe's
        full CAS10 equals this subtotal exactly. No number changes; the model
        applies no CAS10 contingency and that was already NOAK-correct.
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:52-80 (cas10_preconstruction);
            costing_constants.yaml:8, :15-23
        **Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)
        */

        // fixed adders, fuel/FOAK-keyed [$]
        in attribute fixed_precon : Real;
        // net electric power [MW]
        in attribute p_net : Real;

        // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:64.
        in attribute n_mod_in : Real default 1.0;
        // Land calibration. Source: costing_constants.yaml:21 (0.25 acres/MWe
        // at ref), :22 ($10000/acre), :8 (ref_net_power_mwe 1000).
        in attribute land_intensity : Real default 0.25;
        in attribute land_cost : Real default 10000.0;
        in attribute ref_net_power : Real default 1000.0;

        out attribute cost : Real =
            land_intensity * (p_net * n_mod_in * ref_net_power) ** 0.5 * land_cost
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
        exact identity, the handshake injection path -- WI-025 D5/D6).
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:319-357 (cas70_om; annual line :353);
            costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
        **Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)
        */

        // annual O&M at ref power, fuel-keyed [$/yr]
        in attribute om_ref : Real;
        // net electric power [MW]
        in attribute p_net : Real;

        // Frozen n_mod = 1 (WI-025 ruling 1). Source: costs.py:353.
        in attribute n_mod_in : Real default 1.0;
        // Source: costing_constants.yaml:8 (ref_net_power_mwe 1000).
        in attribute ref_net_power : Real default 1000.0;
        // Staffing economy-of-scale exponent. Source: costs.py:353 (** 0.5).
        in attribute alpha : Real default 0.5;
        // directly-specified O&M (additive)
        in attribute om_direct : Real default 0.0;

        out attribute annual_om : Real =
            om_ref * (p_net * n_mod_in / ref_net_power) ** alpha + om_direct;
    }

    // =========================================================================
    // WI-028 -- CAS22 tail + CAS40 + CAS50 + CAS60 concept-agnostic calc defs.
    // Each reproduces (does not call) a 1costingFE formula at pin 0254385 and
    // fits the codegen envelope (flat all-Real arithmetic, + - * / **, no
    // exp/if/lookup/sum/nested-calc). Bases/fractions are inputs (Stellaris
    // binds $-values = M$ x 1e6, MR-3); refs/exponents are defaulted inputs
    // carrying their 1cfe citation (MR-4). n_mod is explicit so the defs
    // generalize past n_mod = 1: plant-wide accounts multiply n_mod * power;
    // per-module accounts (remote handling p_et, cryoplant p_cryo) do not.
    // =========================================================================

    // ---- Generic plant power-law account (waste, fuel, other, I&C, CAS40) ----
    calc def 'Plant Power-Law Cost' {
        doc /*
        Generic plant power-law account:

          cost = base * (n_mod * power / ref_power) ** alpha

        Plant-wide account, linear-or-power-law in plant-total driving power.
        Covers C220400 waste (base 1.96, ref 1000, a=1.0), C220500 fuel
        handling (fuel base, ref 1000, a=0.7), C220600 other (11.5, ref 1000,
        a=0.8), C220700 I&C (85.0, ref 3500, a=0.65), and CAS40 owner (owner
        base, ref 1000, a=0.5). base/ref_power/alpha are per-account concept
        inputs (MR-3, bound at the instance).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
        **Ref**: cas22.py:702 (waste), :718 (fuel), :724 (other), :731 (I&C); costs.py:256 (CAS40 owner)
        **Basis**: Plant-total power-law account cost
        */
        in attribute base : Real;
        // per-module driving power [MW]
        in attribute power : Real;
        in attribute n_mod_in : Real default 1.0;
        in attribute ref_power : Real;
        in attribute alpha : Real;
        out attribute cost : Real = base * (n_mod_in * power / ref_power) ** alpha;
    }

    // ---- C220110 remote handling (per-module p_et; fuel + concept scaled) ----
    calc def 'Remote Handling Cost' {
        doc /*
        Remote-handling account:

          cost = base * concept_scale * (p_et / p_et_ref) ** alpha

        p_et is per-module gross electric (no n_mod). concept_scale is 1.0
        toroidal (tok/stell), 0.55 end-access -- a concept input (MR-3), NOT a
        library default.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
        **Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
        **Basis**: Per-module gross-electric power law, concept-scaled
        */
        // rh_base[fuel] [$]
        in attribute base : Real;
        in attribute concept_scale_in : Real;
        // per-module gross electric [MW]
        in attribute p_et_in : Real;
        // cas22.py:224 ref_gross
        in attribute p_et_ref : Real default 1100.0;
        // cas22.py:645
        in attribute alpha : Real default 0.5;
        out attribute cost : Real = base * concept_scale_in * (p_et_in / p_et_ref) ** alpha;
    }

    // ---- C220111 installation labor = 14% of C220101..110 subtotal ----
    calc def 'Installation Labor Cost' {
        doc /*
        Installation-labor account:

          cost = installation_frac * reactor_subtotal

        reactor_subtotal = Sigma(C220101..C220110) per-module (includes C220109 = 0
        for this concept, excludes 111/112). The multi-unit labor factor (0.92)
        is a plant-aggregate concern at n_mod > 1; the account value compared
        under A-2 is single-module.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
        **Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
        **Basis**: Fixed fraction of the reactor-equipment subtotal
        */
        // cas22.py:664
        in attribute installation_frac_in : Real default 0.14;
        // Sigma(C220101..C220110) [$]
        in attribute reactor_subtotal : Real;
        out attribute cost : Real = installation_frac_in * reactor_subtotal;
    }

    // ---- C220200 main + secondary coolant (two-term, plant-total) ----
    calc def 'Coolant Cost' {
        doc /*
        Coolant account (two-term, plant-total):

          cost = primary_base * (n_mod * p_net / ref_net_power)
               + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

        primary linear in plant-total net; intermediate power-law in plant-total
        thermal.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
        **Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
        **Basis**: Plant-total two-term coolant cost
        */
        // 166.0 M$ -> $
        in attribute primary_base : Real;
        in attribute p_net : Real;
        // 40.6 M$ -> $
        in attribute intermediate_base : Real;
        in attribute p_th_in : Real;
        in attribute n_mod_in : Real default 1.0;
        // cas22.py:684
        in attribute ref_net_power : Real default 1000.0;
        // cas22.py:685
        in attribute p_th_ref : Real default 3500.0;
        // cas22.py:685
        in attribute alpha : Real default 0.55;
        out attribute cost : Real =
            primary_base * (n_mod_in * p_net / ref_net_power)
            + intermediate_base * (n_mod_in * p_th_in / p_th_ref) ** alpha;
    }

    // ---- C220300 aux cooling (plant-total p_th) + cryoplant (per-module p_cryo) ----
    calc def 'Aux Cooling Cost' {
        doc /*
        Auxiliary cooling + cryoplant account:

          cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

        aux term linear in plant-total thermal; cryoplant power-law in
        per-module cryo electric power (NOT scaled by n_mod -- each module has
        its own cryoplant).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
        **Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
        **Basis**: Plant-total aux + per-module cryoplant power law
        */
        // 1.10e-3 M$/MW -> $/MW
        in attribute aux_per_mw_in : Real;
        in attribute p_th_in : Real;
        // 200.0 M$ -> $
        in attribute cryo_base : Real;
        // per-module cryoplant elec [MW]
        in attribute p_cryo : Real;
        in attribute n_mod_in : Real default 1.0;
        // cas22.py:694
        in attribute p_cryo_ref : Real default 30.0;
        // cas22.py:694
        in attribute alpha : Real default 0.7;
        // WI-035 D7: the aux term and the cryoplant term as their own
        // outputs; cost stays their exact sum (same operations, bit-identical).
        out attribute aux_cost : Real = aux_per_mw_in * (n_mod_in * p_th_in);
        out attribute cryo_cost : Real = cryo_base * (p_cryo / p_cryo_ref) ** alpha;
        out attribute cost : Real = aux_cost + cryo_cost;
    }

    // ---- CAS50 supplementary (consumes cas20 / cas23..28 / cas30 aggregates) ----
    calc def 'Supplementary Cost' {
        doc /*
        CAS50 supplementary account:

          cost = (shipping*cas20 + spares*cas23_to_28 + tax*cas20
                  + insurance*(cas20+cas30)
                  + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
                 * (1 + contingency_rate)

        cas20 is CAS20 WITH contingency; cas23_to_28 is c23+c24+c25+c26+c27+c28
        (1cfe's param is misnamed cas22_to_28 but model.py:1492 feeds c23..c28 --
        WI-028 finding F-1). c59 internal contingency applies to the CAS50
        subtotal (NOAK 0).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        **Ref**: costs.py:259-283 (cas50_supplementary); model.py:1492 (spares base = c23..c28)
        **Basis**: Fraction-of-aggregate supplementary cost with internal contingency
        */
        // fuel-keyed
        in attribute spares_frac : Real;
        // fuel-keyed [$]
        in attribute startup_fuel_base : Real;
        // fuel-keyed [$]
        in attribute decom_base : Real;
        // CAS20 with contingency [$]
        in attribute cas20 : Real;
        // c23..c28 subtotal [$]
        in attribute cas23_to_28 : Real;
        // indirect [$]
        in attribute cas30 : Real;
        in attribute p_net : Real;
        in attribute n_mod_in : Real default 1.0;
        // Defaulted formals declared last: usages bind the formals above by name
        // and leave these at their defaults; a skipped default must not precede
        // a bound formal on the exact route (migration ledger).
        in attribute shipping_frac : Real default 0.015;
        in attribute tax_frac : Real default 0.01;
        in attribute insurance_frac : Real default 0.015;
        // NOAK 0
        in attribute contingency_rate_in : Real default 0.0;
        in attribute ref_net_power : Real default 1000.0;
        out attribute cost : Real =
            (shipping_frac * cas20
             + spares_frac * cas23_to_28
             + tax_frac * cas20
             + insurance_frac * (cas20 + cas30)
             + startup_fuel_base * (n_mod_in * p_net / ref_net_power)
             + decom_base * (n_mod_in * p_net / ref_net_power))
            * (1.0 + contingency_rate_in);
    }

    // ---- CAS60 interest during construction (closed form, uniform spend) ----
    calc def 'IDC Closed-Form Cost' {
        doc /*
        CAS60 interest-during-construction line (closed form, uniform spend):

          f_idc = ((1 + interest_rate) ** construction_years - 1)
                  / (interest_rate * construction_years) - 1
          cost  = f_idc * overnight_cost

        Variable real exponent construction_years -- the idc_factor precedent
        (mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
        Option C (owner-ruled): this line is A-2-checked and reported but
        EXCLUDED from total_capital; the DCF idc_factor is untouched.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        **Ref**: costs.py:286-297 (cas60_idc)
        **Basis**: Uniform-spend closed-form interest during construction
        */
        in attribute interest_rate : Real;
        in attribute construction_years_in : Real;
        in attribute overnight_cost : Real;
        attribute f_idc : Real =
            ((1.0 + interest_rate) ** construction_years_in - 1.0)
            / (interest_rate * construction_years_in) - 1.0;
        out attribute cost : Real = f_idc * overnight_cost;
    }

    // ---- CAS71 / CAS80 shared levelization wrapper (WI-029) ----
    calc def 'Levelized Annual Cost' {
        doc /*
        Levelized (growing-annuity) annual cost -- the shared CAS71/CAS80
        wrapper:

          crf = i*(1+i)^n / ((1+i)^n - 1)
          a1  = annual_cost * (1+g)^Tc
          pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
          levelized = crf * pv

        A real annual stream escalating at g from the first operating year is
        present-valued over n operating years at discount rate i, then
        annuitized by CRF. `project_time` Tc is the construction period that
        escalates the stream to its first operating year -- at NOAK that is
        `construction_time` alone (1cfe adds licensing_time only when FOAK,
        costs.py:41-44), so Tc = 8 at both the design and handshake points.

        Used TWICE by the plant (MR-3, one def two usages): with
        annual_cost = the unlevelized annual O&M -> CAS71, and with
        annual_cost = the raw annual DT fuel cost -> CAS80.

        Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
        **Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
            costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
        **Basis**: Growing-annuity present value annuitized by the capital recovery factor
        */

        // raw annual stream [$/yr]
        in attribute annual_cost : Real;
        // i (discount rate)
        in attribute interest_rate : Real;
        // g (escalation rate)
        in attribute inflation_rate_in : Real;
        // n
        in attribute operational_years_in : Real;
        // Tc (NOAK: construction_time)
        in attribute project_time : Real;

        // CRF(i,n). Source: economics.py:6-10. Exposed as an OUT so the plant's
        // 1cfe-form CAS90 comparison channel (WI-029 Option ii) REUSES this one
        // capital-recovery factor instead of restating CRF a second time; the
        // DCF core computes the identical CRF from the same discount_rate /
        // operational_years and is left untouched (mfe_lcoe_dcf.sysml:42-43).
        attribute disc_pow_n : Real = (1.0 + interest_rate) ** operational_years_in;
        out attribute crf : Real = interest_rate * disc_pow_n / (disc_pow_n - 1.0);

        // A1 = escalated first-operating-year cost. Source: economics.py:40.
        attribute a1 : Real = annual_cost * (1.0 + inflation_rate_in) ** project_time;

        // Growing-annuity present value. Source: economics.py:44-46.
        attribute pv : Real =
            a1 * (1.0 - ((1.0 + inflation_rate_in) / (1.0 + interest_rate)) ** operational_years_in)
            / (interest_rate - inflation_rate_in);

        out attribute levelized : Real = crf * pv;
    }

    // ---- CAS80 raw annual DT fuel cost (WI-029) ----
    calc def 'DT Fuel Cost' {
        doc /*
        CAS80 RAW (unlevelized) annual D-T fuel cost:

          annual_raw = n_mod * p_fus * (3600*8760) * availability
                       * cost_per_rxn / (q_eff * mev_to_joules)
          annual_fuel = annual_raw * (1 + (1-burn_fraction)/burn_fraction
                                          * (1 - fuel_recovery))

        The first line converts annual fusion energy to reactions (dividing by
        the per-reaction energy q_eff in MeV, converted to joules) and prices
        them at the blended deuterium + Li-6 cost per reaction. The second line
        is the burn-up recovery correction: only `burn_fraction` of the fuel
        injected is burnt, and `fuel_recovery` of the unburnt remainder is
        recycled, so the make-up stream scales the raw cost.

        The levelization to the reported CAS80 is NOT carried here -- the plant
        feeds `annual_fuel` into 'Levelized Annual Cost' (one levelization
        wrapper, MR-3). The MFE target-consumable term of 1cfe's cas80_fuel is
        structurally zero (IFE-only) and is likewise not carried.

        All fuel constants are inputs, never library defaults (MR-3) -- a
        concept binds its own fuel chemistry and unit prices.

        Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        **Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
            (M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
            physics.py:31 (Q_DT = 17.58 MeV)
        **Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction
        */

        // fusion power [MW]
        in attribute p_fus : Real;
        in attribute n_mod_in : Real default 1.0;
        in attribute availability_in : Real;
        // M_D*u_D + M_Li6*u_Li6 [$/rxn]
        in attribute cost_per_rxn : Real;
        // per-reaction energy [MeV]
        in attribute q_eff : Real;
        // MeV -> J conversion
        in attribute mev_to_joules_in : Real;
        in attribute burn_fraction_in : Real;
        in attribute fuel_recovery_in : Real;

        // reactions/yr * $/rxn -> annual fuel [$/yr]. Source: costs.py:476-544.
        // UNIT NOTE: p_fus is MW, so p_fus * seconds/yr is MJ/yr; the explicit
        // 1e6 converts to J/yr before dividing by the per-reaction energy in J.
        // 1cfe leaves that 1e6 implicit and so returns M$/yr; this def carries
        // it, so with cost_per_rxn in $/rxn the output is $/yr -- the money unit
        // the plant rolls up in (the library's unit-transparency rule).
        attribute annual_raw : Real =
            n_mod_in * p_fus * (3600.0 * 8760.0) * 1.0e6 * availability_in * cost_per_rxn
            / (q_eff * mev_to_joules_in);

        // burn-up recovery correction. Source: costs.py:476-544.
        attribute burn_correction : Real =
            1.0 + (1.0 - burn_fraction_in) / burn_fraction_in * (1.0 - fuel_recovery_in);

        out attribute annual_fuel : Real = annual_raw * burn_correction;
    }

    // ---- CAS72 levelized scheduled replacement (WI-029, Rung B) ----
    calc def 'Levelized Replacement Cost' {
        doc /*
        CAS72 levelized scheduled-replacement cost of the neutron-damage-
        limited in-vessel accounts (first wall / blanket + divertor):

          q_n              = the wall load handed in             [MW/m^2]
          core_lifetime_FPY= clip(fluence_limit / max(q_n, 1e-6),
                                  0.5, operational_years*availability)
          core_lifetime_cal= core_lifetime_FPY / availability     [cal-yr]
          s                = (1 + i)^(-core_lifetime_cal)
          n_rep            = max(0, ceil(operational_years/core_lifetime_cal) - 1)
          pv               = cost_per_event * s * (1 - s^n_rep) / (1 - s)
          cost             = CRF(i, n) * pv

        The replaceable core survives a fixed neutron fluence, so its life in
        full-power years is the fluence limit divided by the wall load, and its
        calendar life divides again by availability. Each replacement is a
        discrete event discounted at its own date; `n_rep` counts the events
        inside the plant life (the final core is never replaced, hence -1).

        THE WALL LOAD IS AN INPUT, NOT COMPUTED HERE (WI-041). The plant binds
        the PEAK neutron wall load ('Neutron Wall Load Peak'), because the
        source and its cited method set in-vessel lifetime by the peak load and
        not the average: Stellaris Table 6 derives the first-wall lifetime
        (~4-6 FPY) from the peak first-wall DPA, and Lion 2022 states "the
        lifetime of the blanket is determined by the peak loads". A concept
        with no source peak binds a calibration of 1.0 and its average arrives
        here unchanged. Before WI-041 this calc computed its own neutron power
        over the circular-torus area, i.e. the average.

        EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): `max`, `min` and `floor`
        are invocations, which fall outside the codegen arithmetic envelope
        (+ - * / ** only, calc_compat_renderer.py:39-46), so this calc routes
        to the handwritten codegen stage (manual_required). The generated
        handwritten impl is normative and is guarded bit-exact (rel 1e-9) by
        the oracle mirror in verify_stellaris.py. Both carry 1cfe's guards
        VERBATIM -- the clip floor/cap, the inner max(q_n, 1e-6), and the outer
        max(0, ...) -- rather than dropping them as point-inert no-ops: they go
        live at study-sweep extremes and a dropped guard would return a wrong
        CAS72 silently and discontinuously.

        Two faithful re-expressions in the model-resident statement, both exact
        identities changing no value: clip(z, lo, hi) is written min(max(z, lo),
        hi) -- jnp.clip's own order -- and ceil(z) is written -floor(-z) (the KerML
        Real function library has floor, min and max but no ceiling or clip). The handwritten impl
        uses Python's math.ceil and the same guards directly.

        EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
        marked for revert -- see models/stellarator_migration_ledger.md): the
        pinned codegen admits no function invocation (max/min/floor) in an
        executable expression, so the model-resident statement of the chain
        above is carried as this doc and the output is declared without an
        expression (a manual interface). The pre-migration body, with the
        intermediates p_neutron, q_n, fpy_raw, fpy_cap, core_lifetime_fpy,
        core_lifetime_cal, s, n_rep, pv, disc_pow_n, crf, is recorded verbatim
        in the ledger row and in git at the migration PR's parent.

        `n_rep` is a discontinuous step function of the live neutron/geometry
        chain and is computed every run -- never frozen as a defaulted input.

        Concept-agnostic: the fluence limit, the wall loading, the replaceable-
        account cost, and the plant life are all inputs (MR-3).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385); knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
        **Ref**: economics.py:53-75 (levelized_replacement_cost); model.py:102-111
            (_core_lifetime_fpy, the clip and inner max); economics.py:6-10 (CRF);
            defaults.py:291 (fluence_limit_dt), defaults.py:299 (replaceable accounts);
            Stellaris Table 6 image (images/page_020_table_0.png: peak DPA in the
            first wall 10.7 DPA/FPY -> estimated first-wall lifetime ~4-6 FPY);
            Lion 2022 output.md line 88 (lifetime determined by the peak loads)
        **Basis**: Fluence-limited replacement schedule on the peak wall load, discretely discounted and annuitized
        */

        // plant-total replaceable-account cost [$]
        in attribute cost_per_event : Real;
        // The wall load that sets the core's fluence-limited life [MW/m^2]. An
        // input, not computed here (WI-041): the plant binds the PEAK neutron
        // wall load ('Neutron Wall Load Peak'). A calc output is a producer
        // channel, so the binding wires cleanly on the exact route.
        in attribute q_n_in : Real;
        // core fluence limit [MW-yr/m^2]
        in attribute fluence_limit_in : Real;
        in attribute availability_in : Real;
        // i
        in attribute interest_rate : Real;
        // n
        in attribute operational_years_in : Real;

        // Manual interface on the exact route (see EXACT-ROUTE FORM in the doc):
        // the handwritten impl carries the guarded chain verbatim and is the
        // executable meaning (guarded by the oracle mirror).
        out attribute cost : Real;
    }

    // ---- WI-029 producer-shaping defs (codegen mechanics, value-preserving) ----
    // Codegen wires a calc input only from a PRODUCER channel: a calc output, or
    // an aggregation that transitively reaches a part usage. A plant attribute
    // that merely sums calc-output exposures classifies FORMULA-without-part-root
    // (or EXPOSE_COMPUTED when it mixes a calc output with a sibling) and mints no
    // channel -- the WI-028 Phase-5 adaptation class. These three defs put the same
    // arithmetic behind calc outputs so the downstream inputs resolve. No value,
    // operand, or operand order changes.

    calc def 'Annual Cost Rollup' {
        doc /*
        CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
        numerator carries (CAS70 + CAS80). Pure addition -- it introduces no new
        economics, it makes the two sums producer channels the DCF core and the
        1cfe-form comparison channel can read.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
        **Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
            economics.py:88-92 (compute_lcoe)
        **Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator
        */
        // levelized O&M [$/yr]
        in attribute cas71 : Real;
        // levelized scheduled replacement [$/yr]
        in attribute cas72 : Real;
        // levelized fuel [$/yr]
        in attribute cas80 : Real;
        out attribute cas70 : Real = cas71 + cas72;
        out attribute annual_total : Real = cas71 + cas72 + cas80;
    }

    calc def '1cfe-Form Capital Charge' {
        doc /*
        CAS90 in 1costingFE's financing form -- the annual capital charge on
        overnight capital PLUS the closed-form CAS60 interest during
        construction:

          cas90 = crf * (overnight_cost + idc_cost)

        WI-029 Option (ii), owner-ruled 2026-07-25: this is a COMPARISON channel.
        The model's own DCF headline keeps its even-spend idc_factor and keeps
        total_capital = overnight_capital (Option C), so CAS60 never enters the
        headline capital base and the two channels cannot double-count. `crf` is
        supplied by the plant from the capital-recovery factor it already
        computes; `idc_cost` is the Item-3 CAS60 reported line -- no new IDC
        arithmetic is introduced here.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        **Ref**: costs.py:547-556 (cas90_annualized_capital = CRF * total_capital);
            costs.py:286-297 (cas60_idc); model.py:1483-1605 (total_cap = overnight + c60)
        **Basis**: 1costingFE annualized capital charge over overnight + IDC
        */
        // capital recovery factor
        in attribute crf : Real;
        // overnight capital [$]
        in attribute overnight_cost : Real;
        // CAS60 interest during construction [$]
        in attribute idc_cost : Real;
        out attribute cas90 : Real = crf * (overnight_cost + idc_cost);
    }

    calc def '1cfe-Form LCOE' {
        doc /*
        LCOE in 1costingFE's form -- the comparison channel that pairs with
        '1cfe-Form Capital Charge' (WI-029 Option ii):

          lcoe = (cas90 + cas70 + cas80) / (8760 * net_electric_mw * n_mod * availability)

        Money-unit transparent: with the cost inputs in $ the result is $/MWh.
        This is NOT the design-point headline -- 'LCOE DCF' remains the headline
        and its convention is untouched. Both channels coexist by design.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
        **Ref**: economics.py:88-92 (compute_lcoe)
        **Basis**: Annual cost over annual energy sold, 1costingFE denominator form
        */
        in attribute cas90 : Real;
        in attribute cas70 : Real;
        in attribute cas80 : Real;
        in attribute net_electric_mw : Real;
        in attribute n_mod_in : Real default 1.0;
        in attribute availability_in : Real;
        attribute annual_energy_mwh : Real =
            8760.0 * net_electric_mw * n_mod_in * availability_in;
        out attribute lcoe : Real = (cas90 + cas70 + cas80) / annual_energy_mwh;
    }
}
