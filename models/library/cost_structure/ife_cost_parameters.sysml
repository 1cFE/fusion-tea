package ife_cost_parameters {
    private import ScalarValues::*;
    private import economic_parameter::'Economic Parameter';

    part def 'IFE Cost Parameters' {
        doc /*
        The 14 technology-agnostic parameters that characterize IFE LCOE,
        from Hawker's simplified economic model. Each parameter carries
        a default value, Monte Carlo range (min/max), and Pearson
        sensitivity coefficient from 10M-sample Monte Carlo analysis.

        Sensitivity ranking (by |Pearson r|):
        1. discount_rate (+0.247)
        2. plant_cost_constant (+0.210)
        3. target_cost_constant (+0.186)
        4. gain (-0.164)
        5. driver_lifetime (-0.134)
        6. availability (-0.127)

        "No single parameter is strongly dominant" — Hawker 2020.

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Table 1 (parameter definitions), Figure 3 (sensitivity)
        **Basis**: Complete parameter set from Hawker 2020 Monte Carlo analysis
        */

        attribute availability : 'Economic Parameter' {
            doc /*
            Plant availability factor (fraction of time operating).
            Source: Hawker 2020 Table 1, parameter mu_a.
            Units: dimensionless fraction.
            */
            :>> value = 0.70;
            :>> min_value = 0.50;
            :>> max_value = 1.00;
            :>> sensitivity = -0.127;
        }

        attribute blanket_energy_multiple : 'Economic Parameter' {
            doc /*
            Blanket energy multiplication factor. Nuclear energy
            multiplier from exothermic lithium reactions.
            Source: Hawker 2020 Table 1, parameter E_b.
            Units: dimensionless.
            */
            :>> value = 1.2;
            :>> min_value = 0.6;
            :>> max_value = 1.4;
            :>> sensitivity = -0.038;
        }

        attribute discount_rate : 'Economic Parameter' {
            doc /*
            Discount rate for DCF calculation. Highest sensitivity
            parameter in the model (+0.247).
            Source: Hawker 2020 Table 1, parameter d.
            Units: dimensionless fraction.
            */
            :>> value = 0.08;
            :>> min_value = 0.02;
            :>> max_value = 0.12;
            :>> sensitivity = 0.247;
        }

        attribute driver_cost_constant : 'Economic Parameter' {
            doc /*
            Driver capital cost per joule of bank energy. Reference
            points span 3 orders of magnitude by driver type:
            NIF $9.5/J, DPSSL $700-1000/J, Xcimer $60-120/J,
            pulsed-power $1.7-6/J.
            Source: Hawker 2020 Table 1, parameter gamma.
            Units: $/J.
            Basis: DI-004 driver cost reference points.
            */
            :>> value = 5.0;
            :>> min_value = 2.0;
            :>> max_value = 10.0;
            :>> sensitivity = 0.075;
        }

        attribute driver_efficiency : 'Economic Parameter' {
            doc /*
            Driver wall-plug efficiency (energy to target / energy
            from grid). Varies by driver type: heavy-ion 20-30%,
            pulser ~10%, laser 5-15%.
            Source: Hawker 2020 Table 1, parameter mu_d.
            Units: dimensionless fraction.
            */
            :>> value = 0.10;
            :>> min_value = 0.05;
            :>> max_value = 0.30;
            :>> sensitivity = -0.063;
        }

        attribute driver_energy : 'Economic Parameter' {
            doc /*
            Driver bank energy (total stored energy per shot).
            Source: Hawker 2020 Table 1, parameter E_d.
            Units: J (range expressed as 0.5-50 MJ).
            */
            :>> value = 10.0e6;
            :>> min_value = 0.5e6;
            :>> max_value = 50.0e6;
            :>> sensitivity = 0.011;
        }

        attribute driver_lifetime : 'Economic Parameter' {
            doc /*
            Driver lifetime in number of shots before replacement.
            Converted to years via shots_per_year = 365.25*24*3600*f*mu_a.
            Source: Hawker 2020 Table 1, parameter N_d.
            Units: shots.
            */
            :>> value = 5.0e7;
            :>> min_value = 1.0e6;
            :>> max_value = 1.0e9;
            :>> sensitivity = -0.134;
        }

        attribute frequency : 'Economic Parameter' {
            doc /*
            Target shot repetition rate.
            Source: Hawker 2020 Table 1, parameter f.
            Units: Hz.
            */
            :>> value = 0.2;
            :>> min_value = 0.01;
            :>> max_value = 10.0;
            :>> sensitivity = 0.035;
        }

        attribute gain : 'Economic Parameter' {
            doc /*
            Target gain (thermonuclear yield / energy on target).
            4th highest sensitivity parameter (-0.164).
            Diminishing returns above ~400 per Hawker; HIF gains
            range 68-500 per Bangerter Table 1.
            Source: Hawker 2020 Table 1, parameter G.
            Units: dimensionless.
            */
            :>> value = 500.0;
            :>> min_value = 10.0;
            :>> max_value = 1000.0;
            :>> sensitivity = -0.164;
        }

        attribute om_cost_constant : 'Economic Parameter' {
            doc /*
            Annual operations and maintenance cost per kWe capacity.
            Source: Hawker 2020 Table 1, parameter epsilon.
            Units: $/kWe-year.
            */
            :>> value = 30.0;
            :>> min_value = 10.0;
            :>> max_value = 100.0;
            :>> sensitivity = 0.050;
        }

        attribute plant_cost_constant : 'Economic Parameter' {
            doc /*
            Balance-of-plant capital cost per kWe. Covers BOP, heat
            exchangers, turbines, generator, grid connection, land,
            buildings. 2nd highest sensitivity (+0.210).
            Source: Hawker 2020 Table 1, parameter alpha.
            Units: $/kWe.
            */
            :>> value = 3000.0;
            :>> min_value = 1000.0;
            :>> max_value = 6000.0;
            :>> sensitivity = 0.210;
        }

        attribute target_cost_constant : 'Economic Parameter' {
            doc /*
            Per-target manufacturing cost. IFE-unique operating cost
            with no MFE parallel. 3rd highest sensitivity (+0.186).
            Threshold effect: below ~$10/target, further reduction
            provides limited LCOE benefit.
            Source: Hawker 2020 Table 1, parameter delta.
            Units: $/target.
            Basis: DI-003 target cost as unique IFE operating cost.
            */
            :>> value = 10.0;
            :>> min_value = 1.0;
            :>> max_value = 100.0;
            :>> sensitivity = 0.186;
        }

        attribute thermal_efficiency : 'Economic Parameter' {
            doc /*
            Thermal-to-electric conversion efficiency.
            Source: Hawker 2020 Table 1, parameter mu_th.
            Units: dimensionless fraction.
            */
            :>> value = 0.40;
            :>> min_value = 0.30;
            :>> max_value = 0.60;
            :>> sensitivity = -0.033;
        }

        attribute yield_cost_constant : 'Economic Parameter' {
            doc /*
            Reaction vessel cost per GJ of fusion energy per shot.
            Captures chamber/blanket cost proportional to yield.
            Source: Hawker 2020 Table 1, parameter beta.
            Units: $/GJ.
            */
            :>> value = 5.0e6;
            :>> min_value = 5.0e5;
            :>> max_value = 5.0e7;
            :>> sensitivity = 0.026;
        }
    }
}
