package aries_nominal_brayton {
    private import ScalarValues::*;
    private import ideal_gas_brayton_components::*;
    private import mfe_viability::*;
    part operating_point {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Independent AGENT supplied flow and ideal helium properties; low/high temperatures supplied source nominal boundaries. Shared return pressure selected once; no flow sizing. Last Updated: 2026-09-21. */
        attribute selected_flow : Real = 1000.0;
        attribute cp : Real = 5193.0;
        attribute gamma : Real = 1.6666666666666667;
        attribute return_pressure : Real = 4.285714285714286;
        attribute low_temperature : Real = 308.15;
        attribute turbine_temperature : Real = 980.15;
    }
    part compressor_1 {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Independent selected stage ratio. Equal nominal ratios are an AGENT assumption, not a live rebalancing rule. Last Updated: 2026-09-21. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc performance : 'Ideal Gas Compressor' {
            in temperature_in = operating_point.low_temperature;
            in pressure_in = operating_point.return_pressure;
            in ratio_in = selected_ratio;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in gamma_in = operating_point.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = performance.temperature_out;
        attribute pressure_out : Real = performance.pressure_out;
        attribute shaft_demand : Real = performance.shaft_demand;
    }
    part intercooler_1 {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: AGENT ideal intercooling with independently supplied outlet target; zero pressure loss across this cooler. Last Updated: 2026-09-21. */
        attribute target_temperature : Real = 308.15;
        attribute heating_role : Real = 0.0;
        calc conditioning : 'Fixed Outlet Conditioning' {
            in temperature_in = compressor_1.temperature_out;
            in target_temperature_in = target_temperature;
            in pressure_in = compressor_1.pressure_out;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = conditioning.temperature_out;
        attribute pressure_out : Real = conditioning.pressure_out;
        attribute heat_into_fluid : Real = conditioning.heat_into_fluid;
    }
    part compressor_2 {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Independent selected stage ratio. Equal nominal ratios are an AGENT assumption, not a live rebalancing rule. Last Updated: 2026-09-21. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc performance : 'Ideal Gas Compressor' {
            in temperature_in = intercooler_1.temperature_out;
            in pressure_in = intercooler_1.pressure_out;
            in ratio_in = selected_ratio;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in gamma_in = operating_point.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = performance.temperature_out;
        attribute pressure_out : Real = performance.pressure_out;
        attribute shaft_demand : Real = performance.shaft_demand;
    }
    part intercooler_2 {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: AGENT ideal intercooling with independently supplied outlet target; zero pressure loss across this cooler. Last Updated: 2026-09-21. */
        attribute target_temperature : Real = 308.15;
        attribute heating_role : Real = 0.0;
        calc conditioning : 'Fixed Outlet Conditioning' {
            in temperature_in = compressor_2.temperature_out;
            in target_temperature_in = target_temperature;
            in pressure_in = compressor_2.pressure_out;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = conditioning.temperature_out;
        attribute pressure_out : Real = conditioning.pressure_out;
        attribute heat_into_fluid : Real = conditioning.heat_into_fluid;
    }
    part compressor_3 {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Independent selected stage ratio. Equal nominal ratios are an AGENT assumption, not a live rebalancing rule. Last Updated: 2026-09-21. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc performance : 'Ideal Gas Compressor' {
            in temperature_in = intercooler_2.temperature_out;
            in pressure_in = intercooler_2.pressure_out;
            in ratio_in = selected_ratio;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in gamma_in = operating_point.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = performance.temperature_out;
        attribute pressure_out : Real = performance.pressure_out;
        attribute shaft_demand : Real = performance.shaft_demand;
    }
    part hot_side_loss {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Source total fractional pressure drop; AGENT allocation entirely before turbine, no off-design pressure law. Last Updated: 2026-09-21. */
        attribute loss_fraction : Real = 0.045;
        calc loss : 'Fractional Pressure Loss' {
            in pressure_in = compressor_3.pressure_out;
            in loss_fraction_in = loss_fraction;
        }
        attribute pressure_out : Real = loss.pressure_out;
    }
    part equivalent_turbine {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Equivalent combined fluid expansion; no claim to source two-shaft pressure/work split. Last Updated: 2026-09-21. */
        attribute efficiency : Real = 0.93;
        calc performance : 'Ideal Gas Expander' {
            in temperature_in = operating_point.turbine_temperature;
            in pressure_in = hot_side_loss.pressure_out;
            in exit_pressure_in = operating_point.return_pressure;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in gamma_in = operating_point.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = performance.temperature_out;
        attribute pressure_out : Real = performance.pressure_out;
        attribute shaft_produced : Real = performance.shaft_produced;
    }
    part recuperator {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Source nominal effectiveness with equal capacity rates and constant helium properties. Last Updated: 2026-09-21. */
        attribute effectiveness : Real = 0.95;
        calc exchange : 'Equal Capacity Recuperator' {
            in cold_temperature_in = compressor_3.temperature_out;
            in hot_temperature_in = equivalent_turbine.temperature_out;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in effectiveness_in = effectiveness;
        }
        attribute cold_temperature_out : Real = exchange.cold_temperature_out;
        attribute hot_temperature_out : Real = exchange.hot_temperature_out;
        attribute transferred_heat : Real = exchange.transferred_heat;
    }
    part heater {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Required thermal conditioning at supplied boundary; derived duty is not heat availability or installed equipment. Last Updated: 2026-09-21. */
        attribute heating_role : Real = 1.0;
        calc conditioning : 'Fixed Outlet Conditioning' {
            in temperature_in = recuperator.cold_temperature_out;
            in target_temperature_in = operating_point.turbine_temperature;
            in pressure_in = hot_side_loss.pressure_out;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = conditioning.temperature_out;
        attribute pressure_out : Real = conditioning.pressure_out;
        attribute heat_into_fluid : Real = conditioning.heat_into_fluid;
    }
    part precooler {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Required thermal conditioning at supplied boundary; derived duty is not heat availability or installed equipment. Last Updated: 2026-09-21. */
        attribute heating_role : Real = 0.0;
        calc conditioning : 'Fixed Outlet Conditioning' {
            in temperature_in = recuperator.hot_temperature_out;
            in target_temperature_in = operating_point.low_temperature;
            in pressure_in = equivalent_turbine.pressure_out;
            in flow_in = operating_point.selected_flow;
            in cp_in = operating_point.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = conditioning.temperature_out;
        attribute pressure_out : Real = conditioning.pressure_out;
        attribute heat_into_fluid : Real = conditioning.heat_into_fluid;
    }
    part cycle_ledger {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: Actual component work and signed heat consumers; net fluid shaft work is not electrical plant output. Last Updated: 2026-09-21. */
        calc balance : 'Brayton Cycle Ledger' {
            in compressor_1_in = compressor_1.shaft_demand;
            in compressor_2_in = compressor_2.shaft_demand;
            in compressor_3_in = compressor_3.shaft_demand;
            in turbine_work_in = equivalent_turbine.shaft_produced;
            in intercooler_1_in = intercooler_1.heat_into_fluid;
            in intercooler_2_in = intercooler_2.heat_into_fluid;
            in precooler_in = precooler.heat_into_fluid;
            in heater_in = heater.heat_into_fluid;
            in inlet_pressure_in = operating_point.return_pressure;
            in discharge_pressure_in = compressor_3.pressure_out;
        }
        attribute compressor_demand : Real = balance.compressor_demand;
        attribute rejected_heat : Real = balance.rejected_heat;
        attribute net_shaft : Real = balance.net_shaft;
        attribute shaft_efficiency : Real = balance.shaft_efficiency;
        attribute energy_residual : Real = balance.energy_residual;
        attribute total_pressure_ratio : Real = balance.total_pressure_ratio;
    }
    part compressor_capacity {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: AGENT independently supplied hypothetical scalar capacity and assumed supported conditions; not qualified equipment. Last Updated: 2026-09-21. */
        attribute offered_rating : Real = 1100.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = offered_rating;
            in demand_in = cycle_ledger.compressor_demand;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute capacity_margin : Real = screen.margin;
        attribute capacity_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = capacity_defined;
            in margin_in = capacity_margin;
        }
    }
    part heater_capacity {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: AGENT independently supplied hypothetical scalar capacity and assumed supported conditions; not qualified equipment. Last Updated: 2026-09-21. */
        attribute offered_rating : Real = 2000.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = offered_rating;
            in demand_in = heater.heat_into_fluid;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute capacity_margin : Real = screen.margin;
        attribute capacity_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = capacity_defined;
            in margin_in = capacity_margin;
        }
    }
    part rejection_capacity {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: Raffray TableIII and Fig12/13 retained in item evidence; accepted design review. Basis: AGENT independently supplied hypothetical scalar capacity and assumed supported conditions; not qualified equipment. Last Updated: 2026-09-21. */
        attribute offered_rating : Real = 1200.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = offered_rating;
            in demand_in = cycle_ledger.rejected_heat;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute capacity_margin : Real = screen.margin;
        attribute capacity_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = capacity_defined;
            in margin_in = capacity_margin;
        }
    }
}
