package CostingImportTest {
    doc /*
    Test that Costing package can be imported and used correctly.
    Validates:
    1. CASCategory enum is accessible
    2. 'Costed Component' can be specialized
    3. All cost attributes can be bound
    4. Enum values can be assigned to cas_category

    **Purpose**: Import and specialization validation for costing.sysml
    **Last Updated**: 2026-01-26
    */

    private import Costing::*;

    // Test 1: Basic specialization with all attributes bound
    part def 'Test Costed Part' :> 'Costed Component' {
        doc /* Simple test part to verify specialization works. */

        :>> cas_category = CASCategory::CAS220103;  // Magnets
        :>> capital_cost = 100.0;
        :>> raw_material_cost = 50.0;
        :>> fabrication_cost = 30.0;
        :>> installation_cost = 20.0;
        :>> idiot_index = 2.0;
    }

    // Test 2: Different CAS category (Level 1)
    part def 'Test Building' :> 'Costed Component' {
        doc /* Test Level 2 CAS category. */

        :>> cas_category = CASCategory::CAS21;  // Buildings and Structures
        :>> capital_cost = 500.0;
        :>> raw_material_cost = 200.0;
        :>> fabrication_cost = 150.0;
        :>> installation_cost = 150.0;
        :>> idiot_index = 2.5;
    }

    // Test 3: Level 3 CAS category (Reactor Auxiliary)
    part def 'Test Coolant System' :> 'Costed Component' {
        doc /* Test Level 3 auxiliary CAS category. */

        :>> cas_category = CASCategory::CAS2202;  // Main and Secondary Coolant
        :>> capital_cost = 75.0;
        :>> raw_material_cost = 40.0;
        :>> fabrication_cost = 20.0;
        :>> installation_cost = 15.0;
        :>> idiot_index = 1.875;
    }

    // Test 4: Instantiation of test parts
    part test_magnet : 'Test Costed Part';
    part test_building : 'Test Building';
    part test_coolant : 'Test Coolant System';
}
