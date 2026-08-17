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
        directly via feature redefinition.

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Equations 2.1-2.16 (complete IFE LCOE model)
        **Basis**: Hawker 2020 parametric IFE LCOE model with 14
            technology-agnostic parameters mapped to physical subsystems
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
            Source: Hawker 2020 Table 1. Units: dimensionless fraction.
            */
        }

        attribute frequency : Real {
            doc /*
            Target shot repetition rate.
            Hawker parameter f. Units: Hz.
            Source: Hawker 2020 Table 1.
            */
        }

        attribute gain : Real {
            doc /*
            Target gain (thermonuclear yield / energy on target).
            Hawker parameter G. 4th highest sensitivity (-0.164).
            Plant-level because gain depends on the target-driver
            interaction, not on any single subsystem.
            Source: Hawker 2020 Table 1. Units: dimensionless.
            */
        }

        attribute thermal_efficiency : Real {
            doc /*
            Thermal-to-electric conversion efficiency.
            Hawker parameter mu_th. Units: dimensionless fraction.
            Source: Hawker 2020 Table 1.
            */
        }

        // === Plant-Level Financial Parameters ===

        attribute discount_rate : Real {
            doc /*
            Discount rate for DCF calculation. Highest sensitivity
            parameter in the model (+0.247).
            Hawker parameter d. Units: dimensionless fraction.
            Source: Hawker 2020 Table 1.
            */
        }

        attribute plant_cost_constant : Real {
            doc /*
            Balance-of-plant capital cost per kWe. Covers BOP, heat
            exchangers, turbines, generator, grid connection, land,
            buildings. 2nd highest sensitivity (+0.210).
            Hawker parameter alpha. Units: $/kWe.
            Source: Hawker 2020 Table 1.
            */
        }

        attribute om_cost_constant : Real {
            doc /*
            Annual operations and maintenance cost per kWe capacity.
            Hawker parameter epsilon. Units: $/kWe-year.
            Source: Hawker 2020 Table 1.
            */
        }

        // === LCOE Calculation ===

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
        }

        attribute lcoe : Real = lcoe_calc.lcoe;

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

        attribute recirculating_fraction : Real = recirc_calc.f_recirc;

        // === Viability Constraint ===

        assert constraint viability : 'Viability Threshold' {
            doc /*
            The product of driver efficiency and target gain must
            exceed ~10 for economically viable IFE. Failing this
            constraint means the plant recirculates too much power.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md,
                knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
            **Ref**: EIF-1992 Components section; Accel-2013 Section 3
            **Basis**: DI-001 — physics-derived viability threshold
            */

            in eta = driver.efficiency;
            in gain_in = gain;
        }
    }
}
