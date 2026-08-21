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

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: L185-186 (universality), L1005-1008 (CAS22 divergence)
        **Basis**: Two-member classification (shared vs ife_divergent) derived
            from ARIES CAS analysis; DI-002 identifies CAS22 as divergence point
        */

        shared;
        ife_divergent;
    }
}
