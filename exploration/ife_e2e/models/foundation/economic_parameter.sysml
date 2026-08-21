package economic_parameter {
    private import ScalarValues::*;

    attribute def 'Economic Parameter' {
        doc /*
        A scalar economic parameter with value bounds and sensitivity metadata.
        Used to define cost model inputs with Monte Carlo range information.

        **Source**: work/active/WI-006_ife-cost-structure-library/spec.md
        **Ref**: MR-WI006-1 (parameter metadata pattern)
        **Basis**: Designed to carry Monte Carlo range data from Hawker 2020;
            bundles value/min/max/sensitivity per DD-2
        */

        attribute value : Real;
        attribute min_value : Real;
        attribute max_value : Real;
        attribute sensitivity : Real;
    }

    enum def 'CAS Scope' {
        doc /*
        Classification of CAS cost accounts by applicability across
        fusion confinement approaches.

        Three-member classification: `shared` (cost structure common to all
        approaches), `ife_divergent` (IFE-specific power-core structure), and
        `mfe_divergent` (MFE-specific power-core structure — the CAS22.1.x
        magnet/heating/divertor sub-accounts).

        **Source**: models/library/cost_structure/cas_hierarchy.sysml ('CAS22 Power Core'); 1costingFE CAS account structure
        **Ref**: DI-002 (CAS22 is the IFE/MFE divergence point)
        **Basis**: DI-002 identifies CAS22 as the IFE/MFE divergence point;
            `mfe_divergent` added (WI-009) to tag the MFE CAS22.1.x sub-accounts,
            mirroring `ife_divergent`. Additive — existing IFE members unchanged.
        */

        shared;
        ife_divergent;
        mfe_divergent;
    }
}
