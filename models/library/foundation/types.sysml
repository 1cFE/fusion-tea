package FoundationTypes {
    doc /*
    Foundation type enumerations for fusion power plant modeling.
    Maps directly to PyFECONS enums.py for validation compatibility.

    **Source**: /home/reid/PyFECONS/pyfecons/enums.py
    **Last Updated**: 2026-01-23
    */

    // ============================================================
    // SECTION 1: REACTOR CLASSIFICATION
    // ============================================================

    enum def ReactorType {
        doc /*
        Top-level fusion reactor classification.

        **Source**: PyFECONS enums.py lines 4-8
        */
        MFE;
        IFE;
        MIF;
    }

    enum def ConfinementType {
        doc /*
        Specific confinement approach within reactor type.
        Includes active values and placeholders for future concepts.

        Active MFE: SPHERICAL_TOKAMAK, MAGNETIC_MIRROR
        Active IFE: LASER_DRIVEN_DIRECT_DRIVE
        Placeholders marked with comments for future expansion.

        **Source**: PyFECONS enums.py lines 10-29
        */
        SPHERICAL_TOKAMAK;
        MAGNETIC_MIRROR;
        LASER_DRIVEN_DIRECT_DRIVE;
        STELLARATOR;
        CONVENTIONAL_TOKAMAK;
        COMPACT_TOKAMAK;
        SPHEROMAK;
        RFP;
        FRC;
        LASER_DRIVEN_INDIRECT_DRIVE;
        FAST_IGNITION;
        IEC;
    }

    enum def EnergyConversion {
        doc /*
        Power conversion method.

        **Source**: PyFECONS enums.py lines 37-40
        */
        DIRECT;
        TURBINE;
    }

    // ============================================================
    // SECTION 2: FUEL TYPE
    // ============================================================

    enum def FuelType {
        doc /*
        Plasma fuel composition.
        DT = Deuterium-Tritium
        DD = Deuterium-Deuterium
        DHE3 = Deuterium-Helium-3
        PB11 = Proton-Boron-11

        **Source**: PyFECONS enums.py lines 43-53
        */
        DT;
        DD;
        DHE3;
        PB11;
    }

    // ============================================================
    // SECTION 3: BLANKET CONFIGURATION
    // ============================================================

    enum def BlanketFirstWall {
        doc /*
        First wall material selection.

        **Source**: PyFECONS enums.py lines 56-67
        */
        TUNGSTEN;
        LIQUID_LITHIUM;
        BERYLLIUM;
        FLIBE;
    }

    enum def BlanketType {
        doc /*
        Blanket configuration type.

        **Source**: PyFECONS enums.py lines 69-95
        */
        FLOWING_LIQUID_FIRST_WALL;
        SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER;
        SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4;
        SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3;
        SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL;
    }

    enum def BlanketPrimaryCoolant {
        doc /*
        Primary coolant type for blanket system.

        **Source**: PyFECONS enums.py lines 98-111
        */
        LEAD_LITHIUM_PBLI;
        LITHIUM_LI;
        FLIBE;
        OTHER_EUTECTIC_SALT;
        HELIUM;
        DUAL_COOLANT_PBLI_AND_HE;
        WATER;
    }

    enum def BlanketSecondaryCoolant {
        doc /*
        Secondary coolant type (if dual coolant system).

        **Source**: PyFECONS enums.py lines 114-128
        */
        NONE;
        LEAD_LITHIUM_PBLI;
        LITHIUM_LI;
        FLIBE;
        OTHER_EUTECTIC_SALT;
        HELIUM;
        DUAL_COOLANT_PBLI_AND_HE;
        WATER;
    }

    enum def BlanketNeutronMultiplier {
        doc /*
        Neutron multiplier material in blanket.
        BE = Beryllium
        PB = Lead
        BE12TI = Beryllium titanide

        **Source**: PyFECONS enums.py lines 131-142
        */
        NONE;
        BE;
        PB;
        PB_AS_PART_OF_PBLI;
        BE12TI;
    }

    enum def BlanketStructure {
        doc /*
        Structural material for blanket.
        SS = Stainless Steel
        FMS = Ferritic Martensitic Steel
        ODS = Oxide Dispersion Strengthened

        **Source**: PyFECONS enums.py lines 145-161
        */
        STAINLESS_STEEL_SS;
        FERRITIC_MARTENSITIC_STEEL_FMS;
        OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL;
        VANADIUM;
    }

    // ============================================================
    // SECTION 4: STRUCTURAL AND MAGNET TYPES
    // ============================================================

    enum def StructurePga {
        doc /*
        Peak ground acceleration for seismic design.
        Higher values indicate higher seismic risk regions.
        PGA_01 = 0.1g, PGA_02 = 0.2g, PGA_03 = 0.3g, PGA_05 = 0.5g

        **Source**: PyFECONS enums.py lines 164-169
        */
        PGA_01;
        PGA_02;
        PGA_03;
        PGA_05;
    }

    enum def MagnetType {
        doc /*
        Superconducting magnet coil type.
        PF = Poloidal Field
        CS = Central Solenoid
        TF = Toroidal Field

        **Source**: PyFECONS enums.py lines 172-181
        */
        PF;
        CS;
        TF;
    }

    enum def MagnetMaterialType {
        doc /*
        Magnet conductor material type.
        HTS_CICC = High-Temperature Superconductor Cable-in-Conduit
        HTS_PANCAKE = HTS Pancake coils
        COPPER = Resistive copper coils

        **Source**: PyFECONS enums.py lines 184-194
        */
        HTS_CICC;
        HTS_PANCAKE;
        COPPER;
    }
}
