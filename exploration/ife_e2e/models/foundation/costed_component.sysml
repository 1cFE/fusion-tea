package costed_component {
    private import ScalarValues::*;

    abstract part def 'Costed Component' {
        doc /*
        Abstract base for any component that participates in CAS cost rollup.
        All cost-bearing subsystems specialize this definition and provide
        concrete cost values. Supports cross-concept comparison per MR-2.

        **Source**: modeling_project/REQUIREMENTS.md
        **Ref**: MR-2 (standard costed component interface)
        **Basis**: Minimal interface (capital_cost + cas_code) for CAS cost
            rollup; additional attributes added as needed without breaking
            existing specializations
        */

        attribute capital_cost : Real;
        attribute cas_code : String;
    }
}
