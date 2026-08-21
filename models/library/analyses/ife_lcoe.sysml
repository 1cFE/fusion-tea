package ife_lcoe {
    private import ScalarValues::*;

    calc def 'IFE LCOE' {
        doc /*
        Levelized Cost of Electricity for an IFE power plant using
        Hawker's 14-parameter discounted cash flow model.

        The formula evaluates a full DCF over a construction period
        (Yc years) and operational lifetime (N_op years). Capital costs
        are spread evenly across construction; operating costs accrue
        during operation. Both cost and energy streams are discounted
        to present value.

        Closed-form present value factors replace year-by-year iteration:
          PVF_con = (1 - (1+d)^(-Yc)) / d
          PVF_op  = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d

        Net electric power per Hawker Eq. 2.12-2.16:
          P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
        where the factor of 2 approximates recirculating power as
        2x driver power (driver + cooling).

        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Equations 2.1-2.16 (complete LCOE model)
        **Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
            closed-form PVF replaces year-by-year iteration per DD-3
        */

        // === The 14 Hawker parameters ===
        in attribute availability_in : Real;
        in attribute blanket_energy_multiple : Real;
        in attribute discount_rate_in : Real;
        in attribute driver_cost_constant : Real;
        in attribute driver_efficiency : Real;
        in attribute driver_energy : Real;
        in attribute driver_lifetime_shots : Real;
        in attribute frequency_in : Real;
        in attribute gain_in : Real;
        in attribute om_cost_constant_in : Real;
        in attribute plant_cost_constant_in : Real;
        in attribute target_cost_constant : Real;
        in attribute thermal_efficiency_in : Real;
        in attribute yield_cost_constant : Real;

        // === Fixed model constants ===
        in attribute construction_years : Real default 5.0;
        in attribute operational_years : Real default 40.0;

        // === Intermediate: physics ===

        // Energy on target [J] (Eq. 2.16)
        attribute energy_on_target : Real =
            driver_efficiency * driver_energy;

        // Fusion energy per shot [J] (Eq. 2.15)
        attribute fusion_energy_per_shot : Real =
            gain_in * energy_on_target;

        // Net electric power [W] (Eqs. 2.12-2.14, 2.16 combined)
        // P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
        attribute net_electric_power : Real =
            driver_energy * frequency_in * (thermal_efficiency_in * blanket_energy_multiple * gain_in * driver_efficiency - 2.0);

        // Net electric power [kWe]
        attribute net_electric_kw : Real =
            net_electric_power / 1000.0;

        // === Intermediate: shot economics ===

        // Shots per year (Eq. 2.9)
        // 31557600 = seconds per Julian year (365.25 * 24 * 3600)
        attribute shots_per_year : Real =
            31557600.0 * frequency_in * availability_in;

        // Driver lifetime in years (Eq. 2.8)
        attribute driver_lifetime_years : Real =
            driver_lifetime_shots / shots_per_year;

        // === Intermediate: annual costs ===

        // Annual capital cost during construction [$/year] (Eqs. 2.4-2.6)
        // = (plant_cost + yield_cost + driver_construction_cost) / Yc
        attribute annual_capital_cost : Real =
            (plant_cost_constant_in * net_electric_kw
             + yield_cost_constant * fusion_energy_per_shot / 1.0e9
             + driver_cost_constant * driver_energy)
            / construction_years;

        // Annual operating cost during operation [$/year] (Eqs. 2.7, 2.10-2.11)
        // = target_cost + om_cost + driver_replacement_cost
        attribute annual_operating_cost : Real =
            target_cost_constant * shots_per_year
            + om_cost_constant_in * net_electric_kw
            + driver_cost_constant * driver_energy / driver_lifetime_years;

        // Annual energy production [MWh/year] (Eq. 2.2)
        attribute annual_energy : Real =
            8760.0 * net_electric_kw * availability_in / 1000.0;

        // === Intermediate: present value factors ===

        // Capital recovery factor for construction period
        // PVF_con = (1 - (1+d)^(-Yc)) / d
        attribute discount_factor_con : Real =
            (1.0 + discount_rate_in) ** construction_years;

        attribute pvf_construction : Real =
            (1.0 - 1.0 / discount_factor_con) / discount_rate_in;

        // Present value factor for operation period
        // PVF_op = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d
        attribute discount_factor_op : Real =
            (1.0 + discount_rate_in) ** operational_years;

        attribute pvf_operation : Real =
            (1.0 / discount_factor_con)
            * (1.0 - 1.0 / discount_factor_op)
            / discount_rate_in;

        // === Result: LCOE [$/MWh] ===
        out attribute lcoe : Real =
            (annual_capital_cost * pvf_construction
             + annual_operating_cost * pvf_operation)
            / (annual_energy * pvf_operation);
    }
}
