/*
 * COMMENTED OUT - Known bad SysML syntax
 *
package MultiplicitySumTest {
    doc /*
    Test file to validate whether sum() works with part multiplicities.

    **Purpose**: De-risk cost rollup patterns before implementation
    **Test Date**: 2026-01-12
    * /

    private import ScalarValues::Real;

    // Simple costed component
    part def 'Simple Component' {
        attribute capital_cost : Real;
    }

    // Test 1: Direct sum() on multiplicity array
    part def 'Test Assembly Direct Sum' {
        part child : 'Simple Component' [3];

        // Attempt: Use sum() directly on child.capital_cost
        attribute total_cost : Real = sum(child.capital_cost);
    }

    // Test 2: Instantiate and see if it works
    part test_assembly_1 : 'Test Assembly Direct Sum' {
        part child : 'Simple Component' [3] {
            :>> capital_cost = 10.0;
        }
    }
}
*/
