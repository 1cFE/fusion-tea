package CoffeeMakerDesign {
    doc /*
    Concrete coffee maker design instance with all parameter values.

    **Purpose**: Validate Pattern A (nested cost models) with specific values.
    **Pattern**: Uses dot notation for attribute binding, sum() for automatic aggregation
    **Validated**: 2026-01-12 - No hardcoded aggregate values
    **Source**: project/research/20260112-055807_multiplicity-cost-rollup-gap.md
    **Last Updated**: 2026-01-12
    */

    private import CoffeeMakerLibrary::*;

    // Top-level design instance
    part coffee_maker : 'Coffee Maker' {
        doc /* Standard home coffee maker design */

        // Brewing system with dual heaters
        // Uses dot notation - no re-declaration of parts
        part redefines brewing {
            // Heater count defaults to 2, can override here if needed
            // :>> heater_count = 2;

            // Set heater parameters via dot notation
            // These apply to ALL heaters in the array
            :>> heater.power_rating = 1000.0;
            :>> heater.material_mass = 0.15;

            // Pump parameters
            :>> pump.flow_rate = 0.5;

            // Brew chamber parameters
            :>> chamber.volume = 0.3;

            // NO hardcoded aggregate values!
            // Costs flow automatically via sum(heater.capital_cost) in library
        }

        // Water reservoir
        part redefines reservoir {
            :>> capacity = 1.5;
        }

        // Carafe
        part redefines carafe {
            :>> capacity = 1.2;
        }

        // Housing assembly
        part redefines housing {
            :>> shell.surface_area = 0.15;
            :>> panel.button_count = 3.0;
        }
    }
}
