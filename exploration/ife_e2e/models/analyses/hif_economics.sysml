package hif_economics {
    private import ScalarValues::*;

    calc def 'Meier HIF Driver Cost' {
        doc /*
        Heavy-ion induction linac driver capital cost from Meier's
        parametric formula. Returns gamma ($/J of bank energy) as the
        primary output for use in Hawker's LCOE model. Also exposes
        cost_billions as an intermediate for Meier's COE chain.

        Input E_d is beam energy on target (MJ), consistent with Meier's
        convention. The calc converts to bank energy using driver efficiency
        to produce gamma in $/J of bank energy (Hawker's convention).

        Constants: 0.32, 0.088 = baseline + marginal accelerator cost
        coefficients (fit to induction linac studies). Reference: 5 Hz,
        single chamber.

        **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
        **Ref**: Eq. 5 (lines 173-192)
        **Basis**: Meier 1986 parametric driver cost formula for HIF
            induction linacs. Year-dollars: 1988$.
        */

        in attribute beam_energy_mj : Real;
        in attribute driver_efficiency : Real;
        in attribute num_chambers : Real;
        in attribute rep_rate : Real;

        // Meier Eq. 5: driver direct cost [$B, 1988$]
        out attribute cost_billions : Real =
            (0.32 + 0.088 * beam_energy_mj)
            * (1.25 + 0.05 * num_chambers)
            * (1.0 + 0.0088 * (rep_rate - 5.0));

        // Bridge to Hawker: gamma = C_dd / E_d_bank
        attribute bank_energy_joules : Real =
            beam_energy_mj * 1.0e6 / driver_efficiency;

        out attribute gamma : Real = cost_billions * 1.0e9 / bank_energy_joules;
    }

    calc def 'Meier Reactor Cost' {
        doc /*
        HIF reactor plant direct cost (excluding driver and target factory).
        Scales from the HYLIFE/Cascade reference design using thermal power
        and accounts for multi-unit site savings.

        Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
        b = 0.49 (power scaling exponent).

        **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
        **Ref**: Eq. 3 (lines 119-137)
        **Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.
        */

        in attribute thermal_power_gw : Real;
        in attribute num_units : Real;

        out attribute reactor_cost_billions : Real =
            0.66 * (thermal_power_gw / 1.67) ** 0.49
            * (0.72 * num_units + 0.28);
    }

    calc def 'Meier Total Capital Cost' {
        doc /*
        Total plant capital cost including indirect cost multiplier.
        Factor 1.83 = total-to-direct cost ratio (midway between coal
        at 1.53 and nuclear-best at 2.07).

        **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
        **Ref**: Eq. 2 (lines 102-117)
        **Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.
        */

        in attribute reactor_cost : Real;
        in attribute driver_cost : Real;
        in attribute target_factory_cost : Real;

        out attribute total_capital_billions : Real =
            1.83 * (reactor_cost + driver_cost + target_factory_cost);
    }

    calc def 'Meier COE' {
        doc /*
        Cost of Electricity from Meier's engineering-economic model.
        Combines fixed charge rate (8.3%) and O&M rate (3%) into a
        single capital charge rate (11.3%), then divides by annual
        energy production.

        Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
        0.0876 = GW-to-$/kWh conversion (8760 hr/yr * 1e6 kW/GW / 100 cents/$).

        **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
        **Ref**: Eq. 1 (lines 76-102)
        **Basis**: Meier 1986 COE formula. Year-dollars: 1988$.
        */

        in attribute total_capital_billions : Real;
        in attribute availability : Real;
        in attribute net_electric_power_gw : Real;

        out attribute coe_cents_kwh : Real =
            (0.113 * total_capital_billions)
            / (0.0876 * availability * net_electric_power_gw);
    }
}
