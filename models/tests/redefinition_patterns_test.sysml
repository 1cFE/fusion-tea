package RedefinitionPatternsTest {
    doc /*
    Test different patterns for part instantiation and attribute binding.
    Goal: Find the cleanest pattern that avoids shadowing warnings.
    */

    private import ScalarValues::Real;
    private import ScalarValues::Integer;
    private import NumericalFunctions::sum;

    // ============================================================
    // BASE DEFINITIONS
    // ============================================================

    part def 'Heating Element' {
        attribute power_rating : Real;
        attribute material_mass : Real;
        attribute capital_cost : Real = material_mass * 50.0;
    }

    // ============================================================
    // PATTERN A: Part declared in def, redeclared in usage (CURRENT)
    // This is what we're doing now - causes shadowing warnings
    // ============================================================

    part def 'Assembly Pattern A' {
        part heater : 'Heating Element' [2];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    part assembly_a : 'Assembly Pattern A' {
        // Redeclaring the part - this causes the warning
        part heater : 'Heating Element' [2] {
            :>> power_rating = 1000.0;
            :>> material_mass = 0.15;
        }
    }

    // ============================================================
    // PATTERN B: Just redefine attributes, don't redeclare part
    // ============================================================

    part def 'Assembly Pattern B' {
        part heater : 'Heating Element' [2];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    part assembly_b : 'Assembly Pattern B' {
        // Don't redeclare part, just redefine its attributes
        :>> heater.power_rating = 1000.0;
        :>> heater.material_mass = 0.15;
    }

    // ============================================================
    // PATTERN C: Use redefines keyword explicitly
    // ============================================================

    part def 'Assembly Pattern C' {
        part heater : 'Heating Element' [2];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    part assembly_c : 'Assembly Pattern C' {
        // Explicitly redefine the part
        part redefines heater {
            :>> power_rating = 1000.0;
            :>> material_mass = 0.15;
        }
    }

    // ============================================================
    // PATTERN D: Multiplicity as a parameter?
    // ============================================================

    part def 'Assembly Pattern D' {
        attribute heater_count : Integer;
        part heater : 'Heating Element' [heater_count];  // Can multiplicity be parameterized?
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    // ============================================================
    // PATTERN E: Default values in definition, override in usage
    // ============================================================

    part def 'Heating Element With Defaults' {
        attribute power_rating : Real default := 500.0;
        attribute material_mass : Real default := 0.10;
        attribute capital_cost : Real = material_mass * 50.0;
    }

    part def 'Assembly Pattern E' {
        part heater : 'Heating Element With Defaults' [2];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    part assembly_e : 'Assembly Pattern E' {
        // Override defaults using redefines
        part redefines heater {
            :>> power_rating = 1000.0;
            :>> material_mass = 0.15;
        }
    }
}
