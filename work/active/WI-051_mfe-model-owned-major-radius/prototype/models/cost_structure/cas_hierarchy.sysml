package cas_hierarchy {
    private import ScalarValues::*;
    private import costed_component::*;
    private import economic_parameter::'CAS Scope';

    part def 'CAS Account' :> 'Costed Component' {
        doc /*
        A single cost account in the CAS (Cost Account Structure) hierarchy.
        The CAS framework applies to both MFE and IFE fusion power plants.
        Each account carries a scope classification indicating whether the
        cost structure is shared across confinement approaches or divergent.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: L185-186 (universality across MFE/IFE)
        **Basis**: CAS framework from Schulte et al. 1978, used in all
            MFE and IFE power plant design studies since
        */

        attribute account_name : String;
        attribute scope : 'CAS Scope';
    }

    part def 'CAS20 Land' :> 'CAS Account' {
        doc /*
        CAS Account 20: Land and Land Rights.
        Scope: shared. HIF may require ~2000 acres vs ~1000 for MFE
        due to accelerator tunnel length, but cost structure is identical.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS20 section
        **Basis**: ARIES CAS framework — shared structure across confinement approaches
        */
    }

    part def 'CAS21 Structures' :> 'CAS Account' {
        doc /*
        CAS Account 21: Structures and Site Facilities.
        Scope: shared. Building volumes differ by concept (laser buildings
        are much larger than tokamak buildings), but cost methodology
        ($/m3 unit costs) is the same.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS21 section
        **Basis**: ARIES CAS framework — shared methodology, concept-varying volumes
        */
    }

    part def 'CAS22 Power Core' :> 'CAS Account' {
        doc /*
        CAS Account 22: Power Core Equipment.
        Scope: ife_divergent. The PRIMARY divergence point between MFE
        and IFE. Sub-accounts 22.1.3 (magnets vs driver), 22.1.4
        (heating vs ignition), and 22.1.8 (divertor vs target factory)
        have completely different cost structures by confinement approach.
        Sub-accounts 22.1.1 (blanket), 22.1.2 (shield), 22.1.5
        (primary structure) are shared.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: L1005-1008 (CAS22 divergence description)
        **Basis**: DI-002 — CAS22 is the IFE-MFE divergence point
        */
    }

    part def 'CAS23 Turbine Plant' :> 'CAS Account' {
        doc /*
        CAS Account 23: Turbine Plant Equipment.
        Scope: shared. Thermal power conversion is concept-agnostic.
        Cost scales with thermal power output.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS23 section
        **Basis**: ARIES CAS framework — concept-agnostic thermal conversion
        */
    }

    part def 'CAS24 Electric Plant' :> 'CAS Account' {
        doc /*
        CAS Account 24: Electric Plant Equipment.
        Scope: shared. Cost scales with gross electric output.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS24 section
        **Basis**: ARIES CAS framework — scales with gross electric output
        */
    }

    part def 'CAS25 Heat Rejection' :> 'CAS Account' {
        doc /*
        CAS Account 25: Heat Rejection Equipment.
        Scope: shared.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS25 section
        **Basis**: ARIES CAS framework — shared structure across confinement approaches
        */
    }

    part def 'CAS26 Miscellaneous' :> 'CAS Account' {
        doc /*
        CAS Account 26: Miscellaneous Plant Equipment.
        Scope: shared.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS26 section
        **Basis**: ARIES CAS framework — shared structure across confinement approaches
        */
    }

    part def 'CAS27 Special Materials' :> 'CAS Account' {
        doc /*
        CAS Account 27: Special Materials.
        Scope: shared (coolant-dependent). Initial coolant inventory,
        special nuclear materials. Cost depends on coolant type
        (FLiBe, Li, LiPb) which varies by concept.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS27 section
        **Basis**: ARIES CAS framework — shared structure, coolant-varying costs
        */
    }

    part def 'CAS90 Indirect Costs' :> 'CAS Account' {
        doc /*
        CAS Accounts 91-99: Indirect Costs.
        Scope: shared. Percentages vary by LSA (Level of Safety
        Assurance) level but structure is identical across concepts.
        Includes construction management, engineering services,
        contingency, interest during construction.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS90 section
        **Basis**: ARIES CAS framework — shared structure, LSA-varying percentages
        */
    }
}
