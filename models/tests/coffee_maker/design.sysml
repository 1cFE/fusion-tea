package CoffeeMakerDesign {
    doc /*
    Concrete coffee maker design instance with all parameter values.

    **Purpose**: Validate Pattern A (nested cost models) with specific values.
    **Last Updated**: 2026-01-12
    */

    private import CoffeeMakerLibrary::*;

    // Top-level design instance
    part coffee_maker : 'Coffee Maker' {
        doc /* Standard home coffee maker design */

        part brewing : 'Brewing System' {
            // Dual heating elements (tests multiplicity)
            part heater : 'Heating Element' [2] {
                :>> power_rating = 1000.0;
                :>> material_mass = 0.15;
            }

            part pump : 'Water Pump' {
                :>> flow_rate = 0.5;
            }

            part chamber : 'Brew Chamber' {
                :>> volume = 0.3;
            }

            // Bind the heater totals for 2 heaters
            // Each heater: material=7.50, fab=4.50, install=1.125, total=13.125
            // Two heaters: material=15.0, fab=9.0, install=2.25, total=26.25
            :>> heater_total_cost = 26.25;
            :>> heater_total_material = 15.0;
            :>> heater_total_fab = 9.0;
            :>> heater_total_install = 2.25;
        }

        part reservoir : 'Water Reservoir' {
            :>> capacity = 1.5;
        }

        part carafe : 'Carafe' {
            :>> capacity = 1.2;
        }

        part housing : 'Housing' {
            part shell : 'Outer Shell' {
                :>> surface_area = 0.15;
            }

            part panel : 'Control Panel' {
                :>> button_count = 3.0;
            }
        }
    }
}
