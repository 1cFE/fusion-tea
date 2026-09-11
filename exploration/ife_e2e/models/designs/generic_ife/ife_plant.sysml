package ife_plant {
    private import ScalarValues::*;
    private import ife_subsystems::*;
    private import ife_lcoe::*;
    private import fusion_cycle::*;

    part def 'IFE Power Plant' {
        doc /*
        Generic driver-agnostic IFE power plant model. Composes
        subsystems (driver, target factory, reaction chamber) and
        wires Hawker's 14 technology-agnostic parameters to the
        library's LCOE calculation.

        The driver is abstract — concrete instantiations (HIF, laser,
        pulser) specialize the driver with specific parameter values.
        All other subsystem and plant-level parameters can be set
        directly via feature redefinition. Table 2 defines parameters and
        Table 3 gives sampled ranges, not default values; concrete designs
        supply their source-backed inputs or explicitly chosen scenarios.

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Equations 2.1-2.16 (complete IFE LCOE model)
        **Basis**: Hawker 2020 parametric IFE LCOE model with 14
            technology-agnostic parameters mapped to physical subsystems
        **Reference**: Hawker Eqs. 2.1-2.16
        **Last Updated**: 2026-09-10
        */

        // === Subsystems ===

        part driver : 'IFE Driver';
        part target_factory : 'Target Factory';
        part chamber : 'Reaction Chamber';

        // === Plant-Level Operations Parameters ===

        attribute availability : Real {
            doc /*
            Plant availability factor (fraction of time operating).
            Hawker parameter mu_a. 6th highest sensitivity (-0.127).
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations). Units: dimensionless fraction.
            */
        }

        attribute frequency : Real {
            doc /*
            Target shot repetition rate.
            Hawker parameter f. Units: Hz.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations).
            */
        }

        attribute gain : Real {
            doc /*
            Target gain (thermonuclear yield / energy on target).
            Hawker parameter G. 4th highest sensitivity (-0.164).
            Plant-level because gain depends on the target-driver
            interaction, not on any single subsystem.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations). Units: dimensionless.
            */
        }

        attribute thermal_efficiency : Real {
            doc /*
            Thermal-to-electric conversion efficiency.
            Hawker parameter mu_th. Units: dimensionless fraction.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations).
            */
        }

        // === Plant-Level Financial Parameters ===

        attribute discount_rate : Real {
            doc /*
            Discount rate for DCF calculation. Highest sensitivity
            parameter in the model (+0.247).
            Hawker parameter d. Units: dimensionless fraction.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations).
            */
        }

        attribute plant_cost_constant : Real {
            doc /*
            Balance-of-plant capital cost per kWe. Covers BOP, heat
            exchangers, turbines, generator, grid connection, land,
            buildings. 2nd highest sensitivity (+0.210).
            Hawker parameter alpha. Units: $/kWe.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations).
            */
        }

        attribute om_cost_constant : Real {
            doc /*
            Annual operations and maintenance cost per kWe capacity.
            Hawker parameter epsilon. Units: $/kWe-year.
            Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            Table 2 (definition); Table 3 (sampled ranges and correlations).
            */
        }

        // === LCOE Calculation ===

        attribute construction_duration : Real = 5.0 {
            doc /*
            Construction duration in years, supplied to both factor and cost calculations.
            **Source**: Hawker, A simplified economic model for inertial fusion
            **Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:148
            **Ref**: Construction and operational durations following Eq. 2.1
            **Basis**: Existing Hawker default, retained as Real.
            **Last Updated**: 2026-09-11
            */
        }
        attribute operational_duration : Real = 40.0 {
            doc /*
            Operation duration in years, supplied to both factor and cost calculations.
            **Source**: Hawker, A simplified economic model for inertial fusion
            **Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:148
            **Ref**: Construction and operational durations following Eq. 2.1
            **Basis**: Existing Hawker default, retained as Real.
            **Last Updated**: 2026-09-11
            */
        }

        calc pv_factors : 'IFE Present Value Factors' {
            in discount_rate_in = discount_rate;
            in construction_years_in = construction_duration;
            in operational_years_in = operational_duration;
        }

        calc lcoe_calc : 'IFE LCOE' {
            doc /*
            Binds all 14 Hawker parameters from their physical subsystem
            sources to the library's LCOE calculation.

            Driver params (4): efficiency, cost/J, energy, lifetime
            Target factory params (1): cost per target
            Chamber params (2): blanket energy multiple, yield cost constant
            Plant operations params (4): availability, frequency, gain, thermal eff
            Plant financial params (3): discount rate, plant cost, O&M cost

            **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
            **Ref**: Equations 2.1-2.16
            **Basis**: Hawker 2020 parameter-to-subsystem mapping
            */

            in availability_in = availability;
            in blanket_energy_multiple = chamber.blanket_energy_multiple;
            in discount_rate_in = discount_rate;
            in driver_cost_constant = driver.cost_per_joule;
            in driver_efficiency = driver.efficiency;
            in driver_energy = driver.energy;
            in driver_lifetime_shots = driver.lifetime_shots;
            in frequency_in = frequency;
            in gain_in = gain;
            in om_cost_constant_in = om_cost_constant;
            in plant_cost_constant_in = plant_cost_constant;
            in target_cost_constant = target_factory.cost_per_target;
            in thermal_efficiency_in = thermal_efficiency;
            in yield_cost_constant = chamber.yield_cost_constant;
            in construction_years = construction_duration;
            in operational_years = operational_duration;
            in pvf_construction = pv_factors.construction_factor;
            in pvf_operation = pv_factors.operation_factor;
        }

        calc hawker_price : 'Generating Electricity Price' {
            in numerator = lcoe_calc.discounted_cost;
            in denominator = lcoe_calc.discounted_energy;
            in net_power = lcoe_calc.net_electric_power;
        }
        // Dollars/MWh. Zero is invalid unless generating=1 and net_positive is satisfied.
        attribute lcoe : Real = hawker_price.price;
        attribute generating : Real = hawker_price.generating;
        // Hawker Eqs. 2.12-2.16; all powers in W, fractions dimensionless.
        attribute fusion_power : Real = lcoe_calc.fusion_power;
        attribute thermal_power : Real = lcoe_calc.thermal_power;
        attribute gross_electric_power : Real = lcoe_calc.gross_electric_power;
        attribute driver_electric_power : Real = lcoe_calc.driver_electric_power;
        attribute other_parasitic_power : Real = lcoe_calc.other_parasitic_power;
        attribute net_electric_power : Real = lcoe_calc.net_electric_power;
        attribute driver_recirculating_fraction : Real = lcoe_calc.driver_recirculating_fraction;
        attribute total_recirculating_fraction : Real = lcoe_calc.total_recirculating_fraction;

        assert constraint net_positive : 'Positive Net Generation' {
            in net_power = net_electric_power;
        }

        // === Power Balance ===

        calc recirc_calc : 'Recirculating Power Fraction' {
            doc /*
            Computes recirculating power fraction from driver efficiency,
            target gain, blanket multiplier, and thermal efficiency.
            Values above ~0.25 indicate marginal economic viability.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Components section (fusion cycle gain)
            **Basis**: DI-001 — eta*G*M*epsilon_th determines power balance
            */

            in eta = driver.efficiency;
            in gain_in = gain;
            in blanket_multiplier = chamber.blanket_energy_multiple;
            in thermal_efficiency_in = thermal_efficiency;
        }

        // Compatibility alias: driver-only fraction of gross output, excludes cooling.
        attribute recirculating_fraction : Real = recirc_calc.f_recirc;

        // === Viability Constraint ===

        assert constraint viability : 'Viability Threshold' {
            doc /*
            Retained eta-times-gain economic heuristic. Passing does not imply
            positive net electricity; net_positive checks the actual priced balance.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md,
                knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
            **Ref**: EIF-1992 Components section; Accel-2013 Section 3
            **Basis**: DI-001 — approximate economic viability heuristic
            */

            in eta = driver.efficiency;
            in gain_in = gain;
        }
    }
}
