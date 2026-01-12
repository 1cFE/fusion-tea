package MultiplicityAlternativesTest {
    doc /*
    Test alternative approaches for multiplicity cost rollup.

    **Purpose**: Find what ACTUALLY works for array aggregation
    **Test Date**: 2026-01-12
    */

    private import ScalarValues::Real;
    private import ScalarValues::Integer;

    // Try importing collection functions (if they exist)
    // private import CollectionFunctions::*;
    // private import BaseFunctions::*;

    // Simple costed component
    part def 'Simple Component' {
        attribute capital_cost : Real;
    }

    // ============================================================
    // TEST 2: Try explicit indexing with #()
    // ============================================================
    part def 'Test Explicit Index' {
        part child : 'Simple Component' [2];

        // Try accessing individual elements
        attribute cost_1 : Real = child#(1).capital_cost;
        attribute cost_2 : Real = child#(2).capital_cost;
        attribute total_cost : Real = cost_1 + cost_2;
    }

    // ============================================================
    // TEST 3: Try reduce syntax
    // ============================================================
    part def 'Test Reduce Syntax' {
        part child : 'Simple Component' [2];

        // Try reduce/collect syntax variations
        // attribute total_cost : Real = child.capital_cost->reduce('+');
    }

    // ============================================================
    // TEST 4: Named individual parts (workaround)
    // ============================================================
    part def 'Test Named Parts' {
        part child_1 : 'Simple Component';
        part child_2 : 'Simple Component';

        // This definitely works
        attribute total_cost : Real = child_1.capital_cost + child_2.capital_cost;
    }

    // ============================================================
    // TEST 5: Use calc to multiply unit cost
    // ============================================================
    calc def MultiplyCalc {
        in attribute unit_cost : Real;
        in attribute quantity : Real;
        out attribute total : Real = unit_cost * quantity;
    }

    part def 'Test Calc Multiply' {
        attribute unit_cost : Real;
        attribute quantity : Real = 2.0;

        calc cost_rollup : MultiplyCalc {
            in unit_cost = unit_cost;
            in quantity = quantity;
        }

        attribute total_cost : Real = cost_rollup.total;
    }

    // ============================================================
    // INSTANTIATIONS
    // ============================================================

    part test_explicit : 'Test Explicit Index' {
        part child : 'Simple Component' [2] {
            :>> capital_cost = 10.0;
        }
    }

    part test_named : 'Test Named Parts' {
        part child_1 : 'Simple Component' {
            :>> capital_cost = 10.0;
        }
        part child_2 : 'Simple Component' {
            :>> capital_cost = 10.0;
        }
    }

    part test_calc : 'Test Calc Multiply' {
        :>> unit_cost = 10.0;
    }
}
