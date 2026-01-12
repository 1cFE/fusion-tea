package MultiplicitySumImportTest {
    doc /*
    Test sum() with proper imports from NumericalFunctions.
    */

    private import ScalarValues::Real;
    private import NumericalFunctions::sum;

    // Simple costed component
    part def 'Simple Component' {
        attribute capital_cost : Real;
    }

    // Test: Use imported sum() on multiplicity array
    part def 'Test Assembly With Import' {
        part child : 'Simple Component' [3];

        // Try with imported sum
        attribute total_cost : Real = sum(child.capital_cost);
    }

    // Instantiate
    part test_assembly : 'Test Assembly With Import' {
        part child : 'Simple Component' [3] {
            :>> capital_cost = 10.0;
        }
    }
}
