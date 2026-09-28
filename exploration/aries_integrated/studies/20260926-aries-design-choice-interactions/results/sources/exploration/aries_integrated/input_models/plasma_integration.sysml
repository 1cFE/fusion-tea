package aries_cs_plasma_integration {
    private import ScalarValues::*;
    private import radial_density_profile::*;
    private import supplied_profile_plasma::*;
    private import mfe_plasma_scaling::*;

    part plasma {
        doc /* Conditioned forward plasma scenario, not the ARIES reference reconstruction.
        Behavior: supplied density/temperature/species distribution produces fusion
        reactions and thermal pressure; pressure feeds unchanged thermal beta.
        Amplitude, volume measure, local helium, DT split and T sensitivity shape
        are supplied choices, never fitted to published power or mean density.
        **Source**: work/active/WI-083_aries-supplied-profile-plasma-integration/spec.md
        **Reference**: Lyon 2008 Eq. (3) p701, Eq. (8) p713, Table IV p708,
        Table VII p716; knowledge/holdout/aries-cs/08-FST-Lyon.pdf
        **Last Updated**: 2026-09-21 */
        attribute amplitude : Real = 5.0e20;
        attribute edge_ratio : Real = 0.1;
        attribute edge_density : Real = amplitude * edge_ratio;
        attribute density_radial_exponent : Real = 12.0;
        attribute density_profile_exponent : Real = 1.0;
        attribute hollowness : Real = 0.66;
        attribute sample_rho : Real = 0.5;
        attribute temperature_axis : Real = 11.83;
        attribute temperature_edge : Real = 0.2;
        attribute temperature_radial_exponent : Real = 2.0;
        attribute temperature_profile_exponent : Real = 1.0;
        attribute helium_fraction : Real = 0.0335;
        attribute deuterium_fraction : Real = 0.5;
        attribute volume : Real = 444.0;
        attribute volume_exponent : Real = 2.0;
        attribute field : Real = 5.70;
        calc density_sample : 'Radial Density Profile' {
            in amplitude_in = amplitude;
            in edge_density_in = edge_density;
            in rho_in = sample_rho;
            in radial_exponent_in = density_radial_exponent;
            in profile_exponent_in = density_profile_exponent;
            in hollowness_in = hollowness;
        }
        calc integration : 'Supplied Profile Plasma' {
            in amplitude_in = amplitude;
            in edge_density_in = edge_density;
            in density_radial_exponent_in = density_radial_exponent;
            in density_profile_exponent_in = density_profile_exponent;
            in hollowness_in = hollowness;
            in temperature_axis_in = temperature_axis;
            in temperature_edge_in = temperature_edge;
            in temperature_radial_exponent_in = temperature_radial_exponent;
            in temperature_profile_exponent_in = temperature_profile_exponent;
            in helium_fraction_in = helium_fraction;
            in deuterium_fraction_in = deuterium_fraction;
            in volume_in = volume;
            in volume_exponent_in = volume_exponent;
            in field_in = field;
        }
        attribute density_mean : Real = integration.density_mean;
        attribute density_weighted_temperature : Real = integration.density_weighted_temperature;
        attribute thermal_pressure : Real = integration.thermal_pressure;
        attribute fusion_power_MW : Real = integration.fusion_power_MW;
        attribute stored_thermal_MJ : Real = integration.stored_thermal_MJ;
        attribute field_for_beta : Real = integration.field_for_beta;
        attribute quadrature_intervals : Real = integration.quadrature_intervals;
        attribute quadrature_relative_change : Real = integration.quadrature_relative_change;
        calc beta_calculation : 'Volume-Averaged Beta' {
            in p_avg_in = thermal_pressure;
            in B_in = field_for_beta;
        }
        attribute beta : Real = beta_calculation.beta;
    }
}
