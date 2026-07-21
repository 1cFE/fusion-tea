package mfe_tail_supplementary_costs {
    private import ScalarValues::*;

    // =========================================================================
    // WI-028 PROTOTYPE — CAS22 tail + CAS40 + CAS50 + CAS60 concept-agnostic
    // calc defs. Each reproduces (does not call) a 1costingFE formula at pin
    // 0254385 and fits the codegen envelope (flat all-Real arithmetic,
    // + - * / **, no exp/if/lookup/sum/nested-calc). Bases/fractions are inputs
    // (Stellaris binds $-values = M$ x 1e6); refs/exponents are defaulted
    // inputs carrying their 1cfe citation. n_mod is explicit so the defs
    // generalize past n_mod = 1 (MR-WI028-6): plant-wide accounts multiply
    // n_mod * power; per-module accounts (remote handling p_et, cryoplant
    // p_cryo) do not.
    // =========================================================================

    // ---- Generic plant power-law account (waste, fuel, other, I&C, CAS40) ----
    calc def 'Plant Power-Law Cost' {
        doc /*
        cost = base * (n_mod * power / ref_power) ** alpha
        Plant-wide account linear-or-power-law in plant-total driving power.
        Covers C220400 waste (base 1.96, ref 1000, a=1.0), C220500 fuel
        (fuel base, ref 1000, a=0.7), C220600 other (11.5, ref 1000, a=0.8),
        C220700 I&C (85.0, ref 3500, a=0.65), and CAS40 owner (owner base,
        ref 1000, a=0.5). Source: cas22.py:702,718,724,731; costs.py:256.
        */
        in attribute base : Real;
        in attribute power : Real;              // per-module driving power [MW]
        in attribute n_mod : Real default 1.0;
        in attribute ref_power : Real;
        in attribute alpha : Real;
        out attribute cost : Real = base * (n_mod * power / ref_power) ** alpha;
    }

    // ---- C220110 remote handling (per-module p_et; fuel + concept scaled) ----
    calc def 'Remote Handling Cost' {
        doc /* cost = base * concept_scale * (p_et / p_et_ref) ** 0.5
           Source: cas22.py:631-645. p_et per-module; ref_gross 1100.
           concept_scale 1.0 toroidal (tok/stell), 0.55 end-access — a concept
           input (kept out of the library, MR-3). */
        in attribute base : Real;               // rh_base[fuel] [$]
        in attribute concept_scale : Real;
        in attribute p_et : Real;               // per-module gross electric [MW]
        in attribute p_et_ref : Real default 1100.0;   // cas22.py:224 ref_gross
        in attribute alpha : Real default 0.5;
        out attribute cost : Real = base * concept_scale * (p_et / p_et_ref) ** alpha;
    }

    // ---- C220111 installation labor = 14% of C220101..110 subtotal ----
    calc def 'Installation Labor Cost' {
        doc /* cost = installation_frac * reactor_subtotal
           Source: cas22.py:652-664. reactor_subtotal = Σ(C220101..C220110)
           per-module (includes C220109 = 0 for this concept, excludes 111/112).
           Multi-unit labor factor (0.92) is a plant-aggregate concern at
           n_mod > 1; the account value compared under A-2 is single-module. */
        in attribute installation_frac : Real default 0.14;   // cas22.py:664
        in attribute reactor_subtotal : Real;   // Σ(C220101..C220110) [$]
        out attribute cost : Real = installation_frac * reactor_subtotal;
    }

    // ---- C220200 main + secondary coolant (two-term, plant-total) ----
    calc def 'Coolant Cost' {
        doc /* cost = primary_base*(n_mod*p_net/ref_net)
                    + intermediate_base*(n_mod*p_th/3500)**0.55
           Source: cas22.py:684-686. primary linear in net; intermediate
           power-law in thermal. Both plant-total. */
        in attribute primary_base : Real;       // 166.0 M$ -> $
        in attribute p_net : Real;
        in attribute intermediate_base : Real;  // 40.6 M$ -> $
        in attribute p_th : Real;
        in attribute n_mod : Real default 1.0;
        in attribute ref_net_power : Real default 1000.0;   // cas22.py:684
        in attribute p_th_ref : Real default 3500.0;        // cas22.py:685
        in attribute alpha : Real default 0.55;             // cas22.py:685
        out attribute cost : Real =
            primary_base * (n_mod * p_net / ref_net_power)
            + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha;
    }

    // ---- C220300 aux cooling (plant-total p_th) + cryoplant (per-module p_cryo) ----
    calc def 'Aux Cooling Cost' {
        doc /* cost = aux_per_mw*(n_mod*p_th) + cryo_base*(p_cryo/30)**0.7
           Source: cas22.py:693-695. aux linear in plant-total thermal;
           cryoplant power-law in per-module cryo electric power (NOT scaled by
           n_mod — each module has its own cryoplant). */
        in attribute aux_per_mw : Real;         // 1.10e-3 M$/MW -> $/MW
        in attribute p_th : Real;
        in attribute cryo_base : Real;          // 200.0 M$ -> $
        in attribute p_cryo : Real;             // per-module cryoplant elec [MW]
        in attribute n_mod : Real default 1.0;
        in attribute p_cryo_ref : Real default 30.0;    // cas22.py:694
        in attribute alpha : Real default 0.7;          // cas22.py:694
        out attribute cost : Real =
            aux_per_mw * (n_mod * p_th)
            + cryo_base * (p_cryo / p_cryo_ref) ** alpha;
    }

    // ---- CAS50 supplementary (consumes cas20 / cas23..28 / cas30 aggregates) ----
    calc def 'Supplementary Cost' {
        doc /* cost = (shipping*cas20 + spares*cas23_28 + tax*cas20
                       + insurance*(cas20+cas30)
                       + startup*(n_mod*p_net/ref) + decom*(n_mod*p_net/ref))
                      * (1 + contingency_rate)
           Source: costs.py:259-283. cas20 is CAS20 WITH contingency; cas23_28
           is c23+c24+c25+c26+c27+c28 (1cfe's param is misnamed cas22_to_28 but
           model.py:1492 feeds c23..c28 — WI-028 finding). c59 internal
           contingency applies to the CAS50 subtotal. */
        in attribute shipping_frac : Real default 0.015;
        in attribute tax_frac : Real default 0.01;
        in attribute insurance_frac : Real default 0.015;
        in attribute spares_frac : Real;        // fuel-keyed
        in attribute startup_fuel_base : Real;  // fuel-keyed [$]
        in attribute decom_base : Real;         // fuel-keyed [$]
        in attribute contingency_rate : Real default 0.0;   // NOAK 0
        in attribute cas20 : Real;              // CAS20 with contingency [$]
        in attribute cas23_to_28 : Real;        // c23..c28 subtotal [$]
        in attribute cas30 : Real;              // indirect [$]
        in attribute p_net : Real;
        in attribute n_mod : Real default 1.0;
        in attribute ref_net_power : Real default 1000.0;
        out attribute cost : Real =
            (shipping_frac * cas20
             + spares_frac * cas23_to_28
             + tax_frac * cas20
             + insurance_frac * (cas20 + cas30)
             + startup_fuel_base * (n_mod * p_net / ref_net_power)
             + decom_base * (n_mod * p_net / ref_net_power))
            * (1.0 + contingency_rate);
    }

    // ---- CAS60 interest during construction (closed form, uniform spend) ----
    calc def 'IDC Closed-Form Cost' {
        doc /* f_idc = ((1+i)^T - 1)/(i*T) - 1;  cost = f_idc * overnight
           Source: costs.py:286-297. Variable real exponent T (construction
           years) — the idc_factor precedent (mfe_lcoe_dcf.sysml:47) proves the
           codegen envelope handles it. Placement into total_capital is the
           reserved CAS60 convention gate; this def only reproduces the line. */
        in attribute interest_rate : Real;
        in attribute construction_years : Real;
        in attribute overnight_cost : Real;
        attribute f_idc : Real =
            ((1.0 + interest_rate) ** construction_years - 1.0)
            / (interest_rate * construction_years) - 1.0;
        out attribute cost : Real = f_idc * overnight_cost;
    }
}
