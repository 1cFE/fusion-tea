package PatternBDetailedTest {
    doc /*
    Test Pattern B: Redefine nested attributes without redeclaring the part.
    */

    private import ScalarValues::Real;
    private import NumericalFunctions::sum;

    part def 'Heating Element' {
        attribute power_rating : Real;
        attribute material_mass : Real;
        attribute capital_cost : Real = material_mass * 50.0;
    }

    part def 'Brewing System' {
        part heater : 'Heating Element' [2];
        attribute total_cost : Real = sum(heater.capital_cost);
    }

    // Pattern B: Dot notation to redefine nested attributes
    part brewing_system : 'Brewing System' {
        :>> heater.power_rating = 1000.0;
        :>> heater.material_mass = 0.15;
    }
}
