package FoundationImportTest {
    doc /*
    Test file to validate foundation package imports work correctly.

    **Purpose**: Verify FoundationTypes, FoundationUnits, and FoundationMaterials
    can all be imported and used together in downstream files.

    **Test Date**: 2026-01-26
    */

    // Import all three foundation packages
    private import FoundationTypes::*;
    private import FoundationUnits::*;
    private import FoundationMaterials::*;

    // Test part that uses elements from each package
    part def 'Foundation Test Part' {
        doc /*
        Test part demonstrating usage of all foundation packages.

        **Source**: Test artifact
        **Last Updated**: 2026-01-26
        */

        // Use enum from FoundationTypes
        attribute reactor_type : ReactorType = ReactorType::MFE;
        attribute confinement : ConfinementType = ConfinementType::SPHERICAL_TOKAMAK;
        attribute fuel : FuelType = FuelType::DT;
        attribute blanket_type : BlanketType = BlanketType::SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER;

        // Use custom units from FoundationUnits
        // Note: Custom unit attribute defs provide semantic typing but values are Real
        attribute capital_cost : Real = 100.0;           // M_USD semantic
        attribute material_cost_rate : Real = 50.0;      // USD_KG semantic
        attribute volume_cost_rate : Real = 1000.0;      // USD_M3 semantic
        attribute power_cost_rate : Real = 0.001;        // USD_W semantic
        attribute efficiency : Real = 40.0;              // Percent semantic
        attribute multiplier : Real = 1.5;               // Ratio semantic

        // Use material from FoundationMaterials
        part first_wall_material : 'Tungsten';
        part blanket_structure : 'Ferritic Martensitic Steel';
        part coolant : 'Lead Lithium';
    }

    // Test instantiation
    part test_instance : 'Foundation Test Part';
}
