package CoffeeMakerLibrary {
    doc /*
    Cost patterns demo library - validates Pattern A (nested cost models).

    **Purpose**: De-risk cost modeling architecture before Phase 4 implementation.
    **Source**: project/research/20260110-strategic-cost-patterns.md
    **Last Updated**: 2026-01-12
    */

    // Standard imports
    private import ScalarValues::Real;

    // ============================================================
    // SECTION 1: ABSTRACT INTERFACE
    // ============================================================

    abstract part def 'Costed Component' {
        doc /*
        Abstract interface for all cost-bearing components.
        Every costed part must specialize this and provide values for cost attributes.

        **Source**: Cost Patterns Research
        **Reference**: project/research/20260110-strategic-cost-patterns.md
        **Last Updated**: 2026-01-12
        */

        // Required cost attributes
        attribute capital_cost : Real;
        attribute raw_material_cost : Real;
        attribute fabrication_cost : Real;
        attribute installation_cost : Real;

        // Derived efficiency metric
        attribute idiot_index : Real;
    }

    // ============================================================
    // SECTION 2: CALC DEFINITIONS
    // ============================================================

    calc def HeatingElementCostCalc {
        doc /*
        Cost calculation for heating elements.

        Formula: Based on power rating and material mass.
        - Material: mass * material_cost_per_kg
        - Fabrication: material * fab_factor
        - Installation: material * install_factor

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        // Inputs
        in attribute power : Real;
        in attribute mass : Real;

        // Cost factors (defaults)
        in attribute material_cost_per_kg : Real default := 50.0;
        in attribute fab_factor : Real default := 0.6;
        in attribute install_factor : Real default := 0.15;

        // Outputs
        out attribute material_cost : Real = mass * material_cost_per_kg;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def WaterPumpCostCalc {
        doc /*
        Cost calculation for water pump.

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute flow_rate : Real;
        in attribute material_cost_per_kg : Real default := 30.0;
        in attribute pump_mass : Real default := 0.3;
        in attribute fab_factor : Real default := 0.8;
        in attribute install_factor : Real default := 0.1;

        out attribute material_cost : Real = pump_mass * material_cost_per_kg;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def BrewChamberCostCalc {
        doc /*
        Cost calculation for brew chamber.

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute volume : Real;
        in attribute material_cost_per_liter : Real default := 15.0;
        in attribute fab_factor : Real default := 0.5;
        in attribute install_factor : Real default := 0.1;

        out attribute material_cost : Real = volume * material_cost_per_liter;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def WaterReservoirCostCalc {
        doc /*
        Cost calculation for water reservoir.

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute capacity : Real;
        in attribute material_cost_per_liter : Real default := 5.0;
        in attribute fab_factor : Real default := 0.4;
        in attribute install_factor : Real default := 0.1;

        out attribute material_cost : Real = capacity * material_cost_per_liter;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def CarafeCostCalc {
        doc /*
        Cost calculation for carafe (coffee pot).

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute capacity : Real;
        in attribute material_cost_per_liter : Real default := 8.0;
        in attribute fab_factor : Real default := 0.3;
        in attribute install_factor : Real default := 0.05;

        out attribute material_cost : Real = capacity * material_cost_per_liter;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def OuterShellCostCalc {
        doc /*
        Cost calculation for outer shell housing.

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute surface_area : Real;
        in attribute material_cost_per_sqm : Real default := 20.0;
        in attribute fab_factor : Real default := 0.5;
        in attribute install_factor : Real default := 0.1;

        out attribute material_cost : Real = surface_area * material_cost_per_sqm;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def ControlPanelCostCalc {
        doc /*
        Cost calculation for control panel.

        **Source**: Demo model (fictional values)
        **Last Updated**: 2026-01-12
        */

        in attribute button_count : Real;
        in attribute base_cost : Real default := 10.0;
        in attribute cost_per_button : Real default := 2.0;
        in attribute fab_factor : Real default := 0.7;
        in attribute install_factor : Real default := 0.15;

        out attribute material_cost : Real = base_cost + button_count * cost_per_button;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    calc def AllocationCostCalc {
        doc /*
        Bundled allocation costs for assembly-level minor items.
        Covers items not modeled as separate parts: fasteners, seals, wiring.

        **Pattern**: Rule R3 from strategic cost patterns
        **Source**: project/research/20260110-strategic-cost-patterns.md
        **Last Updated**: 2026-01-12
        */

        in attribute child_count : Real;
        in attribute total_child_mass : Real;

        // Allocation factors
        in attribute fastener_cost_per_child : Real default := 0.50;
        in attribute seal_cost_per_child : Real default := 0.30;
        in attribute wiring_cost_per_kg : Real default := 2.0;

        out attribute fastener_cost : Real = child_count * fastener_cost_per_child;
        out attribute seal_cost : Real = child_count * seal_cost_per_child;
        out attribute wiring_cost : Real = total_child_mass * wiring_cost_per_kg;
        out attribute total_allocation : Real = fastener_cost + seal_cost + wiring_cost;

        // Material portion for idiot index (80% of allocation is material)
        out attribute material_portion : Real = total_allocation * 0.8;
    }

    // ============================================================
    // SECTION 3: LEAF PART DEFINITIONS
    // ============================================================

    part def 'Heating Element' :> 'Costed Component' {
        doc /*
        Heating element that converts electricity to heat.
        Contains embedded cost model that computes cost from parameters.

        **Pattern**: Nested cost model (Pattern A)
        **Source**: project/research/20260107-final-cost-architecture.md
        **Last Updated**: 2026-01-12
        */

        // Design parameters (set by usage)
        attribute power_rating : Real;
        attribute material_mass : Real;

        // Embedded cost model
        calc cost_model : HeatingElementCostCalc {
            in power = power_rating;
            in mass = material_mass;
        }

        // Expose cost outputs via redefinition
        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Water Pump' :> 'Costed Component' {
        doc /*
        Pump that moves water through the brewing system.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute flow_rate : Real;

        calc cost_model : WaterPumpCostCalc {
            in flow_rate = flow_rate;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Brew Chamber' :> 'Costed Component' {
        doc /*
        Chamber that holds coffee grounds during extraction.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute volume : Real;

        calc cost_model : BrewChamberCostCalc {
            in volume = volume;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Water Reservoir' :> 'Costed Component' {
        doc /*
        Tank that stores water for brewing.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute capacity : Real;

        calc cost_model : WaterReservoirCostCalc {
            in capacity = capacity;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Carafe' :> 'Costed Component' {
        doc /*
        Glass carafe that holds brewed coffee.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute capacity : Real;

        calc cost_model : CarafeCostCalc {
            in capacity = capacity;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Outer Shell' :> 'Costed Component' {
        doc /*
        External plastic shell housing.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute surface_area : Real;

        calc cost_model : OuterShellCostCalc {
            in surface_area = surface_area;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    part def 'Control Panel' :> 'Costed Component' {
        doc /*
        User interface panel with buttons.

        **Pattern**: Nested cost model (Pattern A)
        **Last Updated**: 2026-01-12
        */

        attribute button_count : Real;

        calc cost_model : ControlPanelCostCalc {
            in button_count = button_count;
        }

        :>> capital_cost = cost_model.total_cost;
        :>> raw_material_cost = cost_model.material_cost;
        :>> fabrication_cost = cost_model.fab_cost;
        :>> installation_cost = cost_model.install_cost;
        :>> idiot_index = cost_model.idiot_index;
    }

    // ============================================================
    // SECTION 4: ASSEMBLY PART DEFINITIONS
    // ============================================================

    part def 'Brewing System' :> 'Costed Component' {
        doc /*
        Sub-assembly that produces coffee.
        Contains heating elements (x2), pump, and brew chamber.
        Includes allocation costs for fasteners, seals, and wiring.

        **Pattern**: Assembly aggregation (Rule R2) + Allocation costs (Rule R3)
        **Source**: project/research/20260110-strategic-cost-patterns.md
        **Last Updated**: 2026-01-12
        */

        // Child parts
        part heater : 'Heating Element' [2];
        part pump : 'Water Pump';
        part chamber : 'Brew Chamber';

        // Allocation cost model for minor items
        calc allocation_model : AllocationCostCalc {
            in child_count = 4.0;
            in total_child_mass = 0.8;
        }

        // Expose allocation details
        attribute misc_hardware_cost : Real = allocation_model.total_allocation;

        // For assembly aggregation with multiplicity, we need to handle heater[2]
        // The heater.capital_cost reference accesses the array
        // For now, we express 2x heater cost explicitly in the design file
        // This is a known pattern - multiplicity handling varies by tooling
        attribute heater_total_cost : Real;
        attribute heater_total_material : Real;
        attribute heater_total_fab : Real;
        attribute heater_total_install : Real;

        // Aggregate costs from children + allocation
        :>> capital_cost =
            heater_total_cost +
            pump.capital_cost +
            chamber.capital_cost +
            misc_hardware_cost;

        :>> raw_material_cost =
            heater_total_material +
            pump.raw_material_cost +
            chamber.raw_material_cost +
            allocation_model.material_portion;

        :>> fabrication_cost =
            heater_total_fab +
            pump.fabrication_cost +
            chamber.fabrication_cost;

        :>> installation_cost =
            heater_total_install +
            pump.installation_cost +
            chamber.installation_cost;

        :>> idiot_index = capital_cost / raw_material_cost;
    }

    part def 'Housing' :> 'Costed Component' {
        doc /*
        Enclosure sub-assembly containing shell and control panel.

        **Pattern**: Assembly aggregation (Rule R2)
        **Last Updated**: 2026-01-12
        */

        // Child parts
        part shell : 'Outer Shell';
        part panel : 'Control Panel';

        // Aggregate costs from children (no allocation for this simple assembly)
        :>> capital_cost = shell.capital_cost + panel.capital_cost;
        :>> raw_material_cost = shell.raw_material_cost + panel.raw_material_cost;
        :>> fabrication_cost = shell.fabrication_cost + panel.fabrication_cost;
        :>> installation_cost = shell.installation_cost + panel.installation_cost;
        :>> idiot_index = capital_cost / raw_material_cost;
    }

    part def 'Coffee Maker' :> 'Costed Component' {
        doc /*
        Top-level assembly representing the complete coffee maker product.
        Aggregates all subsystems: brewing system, reservoir, carafe, housing.

        **Pattern**: Assembly aggregation (Rule R2)
        **Last Updated**: 2026-01-12
        */

        // Child sub-assemblies and parts
        part brewing : 'Brewing System';
        part reservoir : 'Water Reservoir';
        part carafe : 'Carafe';
        part housing : 'Housing';

        // Top-level aggregation
        :>> capital_cost =
            brewing.capital_cost +
            reservoir.capital_cost +
            carafe.capital_cost +
            housing.capital_cost;

        :>> raw_material_cost =
            brewing.raw_material_cost +
            reservoir.raw_material_cost +
            carafe.raw_material_cost +
            housing.raw_material_cost;

        :>> fabrication_cost =
            brewing.fabrication_cost +
            reservoir.fabrication_cost +
            carafe.fabrication_cost +
            housing.fabrication_cost;

        :>> installation_cost =
            brewing.installation_cost +
            reservoir.installation_cost +
            carafe.installation_cost +
            housing.installation_cost;

        :>> idiot_index = capital_cost / raw_material_cost;
    }
}
