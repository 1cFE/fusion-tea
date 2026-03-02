package PatternDMultiplicityTest {
    doc /*
    Test Pattern D: Can multiplicity be parameterized?
    */

    private import ScalarValues::Real;
    private import ScalarValues::Integer;
    private import NumericalFunctions::sum;

    part def 'Heating Element' {
        attribute power_rating : Real;
        attribute material_mass : Real;
        attribute capital_cost : Real = material_mass * 50.0;
    }

    // Attempt 1: Multiplicity as attribute reference
    part def 'Assembly Attempt 1' {
        attribute heater_count : Integer;
        part heater : 'Heating Element' [heater_count];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    part assembly_1 : 'Assembly Attempt 1' {
        :>> heater_count = 2;
        :>> heater.power_rating = 1000.0;
        :>> heater.material_mass = 0.15;
    }
}
