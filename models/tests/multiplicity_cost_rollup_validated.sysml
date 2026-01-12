package MultiplicityCostRollupValidated {
    doc /*
    VALIDATED cost rollup pattern using NumericalFunctions::sum.

    **Purpose**: Prove that automatic cost aggregation works with part multiplicities
    **Test Date**: 2026-01-12
    **Status**: VALIDATED - This is the correct pattern
    */

    private import ScalarValues::Real;
    private import NumericalFunctions::sum;
    private import NumericalFunctions::product;

    // ============================================================
    // SECTION 1: ABSTRACT INTERFACE
    // ============================================================

    abstract part def 'Costed Component' {
        doc /* Base interface for all cost-bearing components */

        attribute capital_cost : Real;
        attribute raw_material_cost : Real;
        attribute fabrication_cost : Real;
        attribute installation_cost : Real;
    }

    // ============================================================
    // SECTION 2: LEAF COMPONENT (Direct Calculation)
    // ============================================================

    calc def HeatingElementCostCalc {
        in attribute power : Real;
        in attribute mass : Real;
        in attribute material_cost_per_kg : Real default := 50.0;
        in attribute fab_factor : Real default := 0.6;
        in attribute install_factor : Real default := 0.15;

        out attribute material_cost : Real = mass * material_cost_per_kg;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Real;
        attribute material_mass : Real;

        calc cost_model : HeatingElementCostCalc {
            in power = power_rating;
            in mass = material_mass;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
    }

    // ============================================================
    // SECTION 3: ASSEMBLY WITH MULTIPLICITY - THE KEY PATTERN
    // ============================================================

    part def 'Brewing System' :> 'Costed Component' {
        doc /*
        Assembly demonstrating AUTOMATIC cost rollup with multiplicity.

        Uses NumericalFunctions::sum to aggregate costs from heater[2].
        NO HARDCODED VALUES - costs flow automatically from children.
        */

        // Child parts with multiplicity
        part heater : 'Heating Element' [2];

        // AUTOMATIC AGGREGATION using sum()
        :>> capital_cost = sum(heater.capital_cost);
        :>> raw_material_cost = sum(heater.raw_material_cost);
        :>> fabrication_cost = sum(heater.fabrication_cost);
        :>> installation_cost = sum(heater.installation_cost);
    }

    // ============================================================
    // SECTION 4: DESIGN INSTANCE
    // ============================================================

    part brewing_system : 'Brewing System' {
        part heater : 'Heating Element' [2] {
            :>> power_rating = 1000.0;
            :>> material_mass = 0.15;
        }
        // Expected: Each heater costs 13.125
        // Total capital_cost should be 26.25 (automatically!)
    }

    // ============================================================
    // SECTION 5: MULTI-LEVEL RECURSIVE TEST
    // ============================================================

    part def 'Top Assembly' :> 'Costed Component' {
        doc /* Tests recursive rollup through multiple levels */

        part brewing : 'Brewing System' [2];  // TWO brewing systems

        // Recursive sum: sum of sums
        :>> capital_cost = sum(brewing.capital_cost);
        :>> raw_material_cost = sum(brewing.raw_material_cost);
        :>> fabrication_cost = sum(brewing.fabrication_cost);
        :>> installation_cost = sum(brewing.installation_cost);
    }

    part top_assembly : 'Top Assembly' {
        part brewing : 'Brewing System' [2] {
            part heater : 'Heating Element' [2] {
                :>> power_rating = 1000.0;
                :>> material_mass = 0.15;
            }
        }
        // Expected: 2 brewing systems × 2 heaters × 13.125 = 52.50
    }
}
