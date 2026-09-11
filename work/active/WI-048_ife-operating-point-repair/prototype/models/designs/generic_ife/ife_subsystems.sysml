package ife_subsystems {
    private import ScalarValues::*;
    private import cas_hierarchy::*;
    private import economic_parameter::'CAS Scope';

    enum def 'Wall Type' {
        doc /*
        Classification of IFE reaction chamber first wall approaches.
        Three fundamentally different engineering strategies for
        managing the impulse and radiation from each fusion shot.

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Chamber concepts section
        **Basis**: EIF-1992 three-category classification of IFE chambers
        */

        dry_wall;
        wetted_wall;
        liquid_wall;
    }

    // === CAS22 Level 3 Sub-Accounts ===

    part def 'CAS22.1.1 First Wall Blanket' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.1: First Wall and Blanket.
        Scope: shared. Captures fusion neutron energy and breeds
        tritium via lithium reactions. Structure shared across
        MFE and IFE, though geometry differs (toroidal vs spherical).

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS22.1.1 section
        **Basis**: ARIES CAS framework — blanket is concept-agnostic
        */

        :>> scope = 'CAS Scope'::shared;
    }

    part def 'CAS22.1.2 Shield' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.2: High Temperature Shield.
        Scope: shared. Protects structure and magnets/driver components
        from residual neutron flux after blanket absorption.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS22.1.2 section
        **Basis**: ARIES CAS framework — shielding is concept-agnostic
        */

        :>> scope = 'CAS Scope'::shared;
    }

    part def 'CAS22.1.3 Driver' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.3: Driver (IFE) / Coils (MFE).
        Scope: ife_divergent. The primary divergence point between
        MFE and IFE. In IFE, this is the driver system (laser,
        heavy-ion accelerator, or pulsed-power driver). In MFE,
        this is the magnet/coil system.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: L1005-1008 (CAS22 divergence)
        **Basis**: DI-002 — CAS22.1.3 is functionally different by confinement type
        */

        :>> scope = 'CAS Scope'::ife_divergent;
    }

    part def 'CAS22.1.5 Primary Structure' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.5: Primary Structure and Support.
        Scope: shared. Vacuum vessel, structural support framework.
        Geometry differs (spherical for IFE vs toroidal for MFE)
        but cost methodology is the same.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS22.1.5 section
        **Basis**: ARIES CAS framework — structural support is concept-agnostic
        */

        :>> scope = 'CAS Scope'::shared;
    }

    part def 'CAS22.1.8 Target Factory' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.8: Target Factory (IFE) / Plasma Source (MFE).
        Scope: ife_divergent. In IFE, this is the target manufacturing
        facility producing expendable targets at rep rate. In MFE,
        this is the fueling system (pellet injectors, gas puff).
        Fundamentally different cost structure and scaling.

        **Source**: knowledge/sources/aries_cost_account_documentation/output.md
        **Ref**: CAS22.1.8 section
        **Basis**: DI-003 — target cost is a unique IFE operating cost category
        */

        :>> scope = 'CAS Scope'::ife_divergent;
    }

    // === Physical Subsystem Definitions ===

    abstract part def 'IFE Driver' :> 'CAS22.1.3 Driver' {
        doc /*
        Abstract IFE driver subsystem. Concrete driver types (HIF,
        laser, pulser) specialize this with specific parameter values.

        The four attributes map to Hawker's driver-specific parameters.
        No default values — each driver type must provide its own.

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Table 1 (parameters mu_d, gamma, E_d, N_d)
        **Basis**: DI-004 — driver cost reference points span 3 orders
            of magnitude by driver type
        */

        attribute efficiency : Real;
        attribute cost_per_joule : Real;
        attribute energy : Real;
        attribute lifetime_shots : Real;
    }

    part def 'Target Factory' :> 'CAS22.1.8 Target Factory' {
        doc /*
        IFE target manufacturing facility. Produces expendable fusion
        targets consumed on each shot. The per-target cost is an
        operating expense with no MFE parallel.

        Hawker identifies target cost as the 3rd most sensitive LCOE
        parameter (+0.186 Pearson r), with a threshold effect: below
        ~$10/target, further reduction provides limited LCOE benefit.

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Table 1 (parameter delta)
        **Basis**: DI-003 — target cost is a unique IFE operating cost
        */

        attribute cost_per_target : Real;
    }

    part def 'Reaction Chamber' {
        doc /*
        IFE reaction chamber assembly. Contains first wall/blanket,
        shield, and primary structure as CAS22 sub-account parts.

        The chamber's aggregate economic parameters are blanket energy
        multiple (E_b) and yield cost constant (beta). Wall type
        classification determines first wall engineering approach.

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Chamber concepts section
        **Basis**: EIF-1992 IFE chamber classification and subsystem decomposition
        */

        attribute wall_type : 'Wall Type';
        attribute blanket_energy_multiple : Real;
        attribute yield_cost_constant : Real;

        part blanket : 'CAS22.1.1 First Wall Blanket';
        part shield : 'CAS22.1.2 Shield';
        part structure : 'CAS22.1.5 Primary Structure';
    }
}
