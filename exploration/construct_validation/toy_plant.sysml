package toy_plant {
    private import ScalarValues::*;
    private import toy_library::*;

    part def 'Toy Plant' {
        doc /*
        Minimal part def exercising both WI-010 wiring constructs:
        1. Usage-level calc chaining — `cost_calc.in area` bound to
           `area_calc.area` (a sibling calc usage's result).
        2. Part-level `assert constraint` taking a calc output.

        Expected values at the literals below:
          area = 4.0 * 3.0            = 12.0
          cost = 12.0 * 250.0         = 3000.0
          viable: 3000.0 <= 5000.0    = true

        **Source**: work/backlog/epic-pipeline-derisk-demo.md (Item 2)
        **Ref**: WI-009 design.md "Structure ↔ behavior binding"
        **Basis**: Synthetic validation fixture — no domain content
        */

        // NOTE (live validation 2026-07-05): part attributes are deliberately
        // named differently from the calc def parameters they feed. A binding
        // like `in length = length;` parses and passes `syside check`, but at
        // evaluation time syside resolves the right-hand `length` to the calc
        // usage's own `in` parameter (self-reference), and evaluation spins
        // until the step limit ("Evaluating expression took too long").
        // Renaming the part attributes (plant_*) makes the reference
        // unambiguous and evaluation succeeds.
        attribute plant_length : Real = 4.0;
        attribute plant_width : Real = 3.0;
        attribute plant_unit_cost : Real = 250.0;
        attribute plant_budget : Real = 5000.0;

        // Stage 1: geometry
        calc area_calc : 'Panel Area' {
            in length = plant_length;
            in width = plant_width;
        }

        // Stage 2: cost — input chained from stage 1's result
        calc cost_calc : 'Panel Cost' {
            in area = area_calc.area;
            in unit_cost = plant_unit_cost;
        }

        // Derived attribute reading a calc result
        attribute total_cost : Real = cost_calc.cost;

        // Part-level asserted constraint fed by a calc output
        assert constraint affordable : 'Cost Within Budget' {
            in cost = cost_calc.cost;
            in budget = plant_budget;
        }
    }

    part demo_plant : 'Toy Plant';
}
