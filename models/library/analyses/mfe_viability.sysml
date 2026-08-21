package mfe_viability {
    private import ScalarValues::*;

    constraint def 'Net Power Positive' {
        doc /*
        Hard physics bound: the plant must produce positive net electric power
        (equivalently engineering Q > 1, recirculating fraction < 1). A design
        that fails this consumes more power than it generates and is not a power
        plant at all.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/validation.py
        **Ref**: validation.py:500-505 (p_net non-positive check)
        **Basis**: Net electric > 0 is the unambiguous physics viability floor
        */

        in attribute net_electric : Real;

        net_electric > 0.0
    }

    constraint def 'Economic Recirculating Threshold' {
        doc /*
        Economic viability knee: the recirculating power fraction should stay at
        or below a threshold (default 0.5). Above ~0.5, parasitic power load is
        excessive and the plant's economics deteriorate sharply. The threshold
        is an adjustable, documented parameter (not a hard physics bound) — the
        default matches the 1costingFE "excessive parasitic power load" warning.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/validation.py
        **Ref**: validation.py:512-515 (rec_frac > 0.5 excessive-parasitic knee)
        **Basis**: DI-001-analogue for MFE — recirculating fraction knee at 0.5
        */

        in attribute rec_frac : Real;
        in attribute threshold : Real default 0.5;

        rec_frac <= threshold
    }

    constraint def 'Beta Limit' {
        doc /*
        Plasma stability bound: the volume-averaged plasma pressure ratio (beta)
        must stay at or below the configuration's beta limit. Above it the plasma
        loses MHD equilibrium/stability. For a stellarator the limit is the
        configuration's design/optimization target (Stellaris: <beta>_V = 5% at
        which the QI equilibrium and coils were optimized); the operating point
        must sit at or below it.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: line 273 (coils + boundary optimized at targeted <beta>_V = 5%)
        **Basis**: MHD beta limit — operating beta must not exceed the design beta
        */

        in attribute beta_in : Real;
        in attribute beta_limit_in : Real;

        beta_in <= beta_limit_in
    }

    constraint def 'Neutron Wall Load Limit' {
        doc /*
        First-wall lifetime bound: the neutron wall load [MW/m^2] must stay at or
        below the first-wall material/design limit. Excessive neutron flux drives
        displacement damage (DPA) and shortens the first-wall replacement
        interval below viability. Pair with 'Neutron Wall Load' (mfe_plasma_
        scaling), which forward-computes the load from fusion power and wall area.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load 4.05 MW/m^2), lines 1757-1766 (DPA-limited first-wall lifetime)
        **Basis**: Neutron wall load must not exceed the first-wall design limit
        */

        in attribute wall_load : Real;
        in attribute wall_load_limit_in : Real;

        wall_load <= wall_load_limit_in
    }

    constraint def 'TBR Floor' {
        doc /*
        Tritium self-sufficiency bound: the tritium breeding ratio (TBR) must be
        at or above a floor (typically ~1.05) so the plant breeds enough tritium
        to refuel itself plus margin for losses, decay, and startup inventory.
        Below the floor the D-T fuel cycle is not self-sustaining.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: line 1530 (TBR > 1.05 target), line 1659 (achieved TBR 1.074)
        **Basis**: D-T tritium self-sufficiency floor
        */

        in attribute tbr_in : Real;
        in attribute tbr_floor_in : Real;

        tbr_in >= tbr_floor_in
    }
}
