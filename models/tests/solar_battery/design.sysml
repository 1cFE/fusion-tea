package SolarBatteryDesign {
    doc /*
    Concrete solar+battery plant design instance with all parameter values.
    Includes system-level CalcUsages for energy production, O&M, fuel,
    financial, and LCOE — wired together via dot notation.

    **Purpose**: Validate full LCOE pipeline with PyFECONS-aligned calculations.
    **Pattern**: Parameter binding via :>>, system-level CalcUsages at top level.
    **Reference**: models/tests/coffee_maker/design.sysml
    **Spec**: .project/active/solar-battery-sysml-model/spec.md (FR-9 through FR-12)
    **Last Updated**: 2026-02-01
    */

    private import ScalarValues::Real;
    private import SolarBatteryLibrary::*;

    // Top-level design instance
    part solar_battery_plant : 'Solar Battery Plant' {

        // ================================================================
        // SUBSYSTEM PARAMETER BINDINGS
        // ================================================================

        // Solar Array subsystem
        part redefines solar_array : 'Solar Array' {
            :>> pv_module.wattage = 400.0;       // 400W panels
            :>> pv_module.efficiency = 0.21;      // 21% efficiency
            :>> inverter.power_rating = 2000.0;   // 2kW string inverters
            :>> array_bos.string_count = 4.0;     // 4 strings
            :>> array_bos.panel_count = 20.0;     // 20 panels
        }

        // Battery System subsystem
        part redefines battery_system : 'Battery System' {
            :>> battery_pack.capacity_kwh = 5.0;       // 5kWh per pack
            :>> battery_pack.chemistry_factor = 1.0;    // LFP baseline
            :>> hybrid_inverter.power_rating = 10000.0; // 10kW bidirectional
            :>> battery_bos.pack_count = 8.0;           // 8 packs
        }

        // Site Infrastructure subsystem
        part redefines site_infra : 'Site Infrastructure' {
            :>> racking.panel_count = 20.0;           // 20 panels
            :>> racking.tilt_angle = 30.0;            // 30 degree tilt
            :>> electrical_panel.circuit_count = 4.0;  // 4 circuits
            :>> permitting.system_capacity_kw = 8.0;   // 8kW system
        }

        // ================================================================
        // OPERATING AND FINANCIAL PARAMETERS
        // ================================================================

        attribute p_net_mw : Real = 0.008;              // 8 kW
        attribute n_mod : Real = 1.0;
        attribute plant_availability : Real = 0.159;     // (4.5/24) * 0.85
        attribute plant_lifetime : Real = 25.0;          // years
        attribute yearly_inflation : Real = 0.0245;      // BLS long-run
        attribute discount_rate : Real = 0.05;           // 5% real
        attribute om_rate_per_kw_year : Real = 20.0;     // $/kW-yr
        attribute p_net_kw : Real = p_net_mw * 1000.0;  // Derived from p_net_mw
        attribute fuel_unit_cost : Real = 0.0;           // No fuel for solar
        attribute fuel_consumption : Real = 0.0;         // No fuel for solar

        // ================================================================
        // SYSTEM-LEVEL CALC USAGES (visible to codegen)
        // ================================================================

        calc energy_production : EnergyProductionCalc {
            in p_net_mw = p_net_mw;
            in n_mod = n_mod;
            in plant_availability = plant_availability;
        }

        calc annualized_om : AnnualizedOMCalc {
            in om_rate_per_kw_year = om_rate_per_kw_year;
            in p_net_kw = p_net_kw;
        }

        calc annualized_fuel : AnnualizedFuelCalc {
            in fuel_unit_cost = fuel_unit_cost;
            in fuel_consumption = fuel_consumption;
        }

        calc annualized_financial : AnnualizedFinancialCalc {
            in total_capex = capital_cost;  // from 'Solar Battery Plant' rollup
            in discount_rate = discount_rate;
            in plant_lifetime = plant_lifetime;
        }

        calc lcoe : LCOECalc {
            in annualized_capital_cost = annualized_financial.annualized_capital_cost;
            in annual_om_cost = annualized_om.annual_om_cost;
            in annual_fuel_cost = annualized_fuel.annual_fuel_cost;
            in yearly_inflation = yearly_inflation;
            in plant_lifetime = plant_lifetime;
            in annual_energy_mwh = energy_production.annual_energy_mwh;
        }
    }
}
