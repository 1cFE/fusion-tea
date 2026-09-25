package supplied_profile_plasma {
    private import ScalarValues::*;

    calc def 'Supplied Profile Plasma' {
        doc /* Forward integration of supplied electron density, equal ion/electron
        temperature and electron/D/T/He species profiles under a chosen normalized
        shell-volume measure. No source fusion power, mean density or beta target
        enters this calculation. It does not solve confinement or select an amplitude.
        ne uses Radial Density Profile unchanged. T=(Taxis-Tedge)*(1-rho^x)^y+Tedge.
        w=m*rho^(m-1); nHe=fHe*ne; nD=fD*(1-2*fHe)*ne;
        nT=(1-fD)*(1-2*fHe)*ne. Pressure=(2-fHe)*ne*T*keV_to_J.
        density_mean=integral(w*ne); density_weighted_temperature=integral(w*ne*T)/density_mean;
        thermal_pressure=(2-fHe)*integral(w*ne*T)*keV_to_J;
        fusion_power_MW=V*integral(w*nD*nT*sigv_DT(T))*17.58*MeV_to_J*1e-6;
        stored_thermal_MJ=1.5*thermal_pressure*V*1e-6.
        SI exact eV=1.602176634e-19 J; inherited DT energy convention 17.58 MeV.
        Density m^-3, T keV, V m^3, field T, pressure Pa; other inputs dimensionless.
        field_for_beta is the unchanged supplied field after domain validation.
        Typed completion guards finite inputs/results, positive A/V/B/exponents,
        0<=edge<=A, 0<=h<=1, 0.2<=Tedge<=Taxis<=100 keV,
        0<=fHe<=0.5, 0<=fD<=1, 1<=m<=4. No clipping or extrapolation.
        Simpson refinement from 1024 to 65536 requires two consecutive changes
        <=1e-6 for each integrated moment; otherwise refuses. Reported largest
        change is numerical convergence evidence, not a rigorous error bound.
        Averages use the supplied measure, not a claimed ARIES 3D Jacobian.
        **Source**: work/active/WI-083_aries-supplied-profile-plasma-integration/spec.md
        **Reference**: authorized Lyon 2008 Eqs. (3),(8), printed pp701,713;
        /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54 (DT kernel 0.2..100 keV);
        models/library/analyses/mfe_fuel_cycle.sysml (inherited DT energy convention)
        **Last Updated**: 2026-09-21 */
        in attribute amplitude_in : Real;
        in attribute edge_density_in : Real;
        in attribute density_radial_exponent_in : Real;
        in attribute density_profile_exponent_in : Real;
        in attribute hollowness_in : Real;
        in attribute temperature_axis_in : Real;
        in attribute temperature_edge_in : Real;
        in attribute temperature_radial_exponent_in : Real;
        in attribute temperature_profile_exponent_in : Real;
        in attribute helium_fraction_in : Real;
        in attribute deuterium_fraction_in : Real;
        in attribute volume_in : Real;
        in attribute volume_exponent_in : Real;
        in attribute field_in : Real;
        out attribute density_mean : Real;
        out attribute density_weighted_temperature : Real;
        out attribute thermal_pressure : Real;
        out attribute fusion_power_MW : Real;
        out attribute stored_thermal_MJ : Real;
        out attribute field_for_beta : Real;
        out attribute quadrature_intervals : Real;
        out attribute quadrature_relative_change : Real;
    }
}
