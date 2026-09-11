"""
Verify IFE LCOE calculation with Hawker default parameters.

Implements Hawker's closed-form DCF LCOE model (Equations 2.1-2.16) using
historical module defaults. The independent check sums discounted annual cash
flows explicitly; the production model uses closed-form present-value factors.

The historical broad range is not a source-fidelity acceptance criterion.

Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
Ref: Equations 2.1-2.16, Table 1
"""


def compute_ife_lcoe(
    availability: float = 0.70,
    blanket_energy_multiple: float = 1.2,
    discount_rate: float = 0.08,
    driver_cost_constant: float = 5.0,        # $/J
    driver_efficiency: float = 0.10,
    driver_energy: float = 10.0e6,             # J
    driver_lifetime_shots: float = 5.0e7,
    frequency: float = 0.2,                    # Hz
    gain: float = 500.0,
    om_cost_constant: float = 30.0,            # $/kWe-yr
    plant_cost_constant: float = 3000.0,       # $/kWe
    target_cost_constant: float = 10.0,        # $/target
    thermal_efficiency: float = 0.40,
    yield_cost_constant: float = 5.0e6,        # $/GJ
    construction_years: float = 5.0,
    operational_years: float = 40.0,
) -> dict:
    """Source-equation oracle; historical defaults are not the computed Osiris plant."""

    if int(construction_years) != construction_years:
        raise ValueError("Annual-sum oracle requires whole construction years")
    if int(operational_years) != operational_years:
        raise ValueError("Annual-sum oracle requires whole operating years")

    # Physics intermediates
    energy_on_target = driver_efficiency * driver_energy
    fusion_energy_per_shot = gain * energy_on_target

    # Net electric power [W] (Eqs. 2.12-2.14, 2.16 combined)
    # P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
    net_electric_power = driver_energy * frequency * (
        thermal_efficiency * blanket_energy_multiple * gain * driver_efficiency - 2.0
    )
    net_electric_kw = net_electric_power / 1000.0

    # Shot economics
    seconds_per_year = 31557600.0  # Julian year
    shots_per_year = seconds_per_year * frequency * availability
    driver_lifetime_years = driver_lifetime_shots / shots_per_year

    # Annual costs
    annual_capital_cost = (
        plant_cost_constant * net_electric_kw
        + yield_cost_constant * fusion_energy_per_shot / 1.0e9
        + driver_cost_constant * driver_energy
    ) / construction_years

    annual_operating_cost = (
        target_cost_constant * shots_per_year
        + om_cost_constant * net_electric_kw
        + driver_cost_constant * driver_energy / driver_lifetime_years
    )

    # Annual energy [MWh/year]
    annual_energy = 8760.0 * net_electric_kw * availability / 1000.0

    # Independent annual cash-flow sums (Hawker Eq. 2.1), retaining the
    # model's construction/operation timing and 8760 h / Julian-shot-year bases.
    pvf_construction = sum((1 + discount_rate) ** -year
                           for year in range(1, int(construction_years) + 1))
    pvf_operation = sum((1 + discount_rate) ** -year
                        for year in range(int(construction_years) + 1,
                                          int(construction_years + operational_years) + 1))
    generating = net_electric_power > 0
    lcoe = ((annual_capital_cost * pvf_construction
             + annual_operating_cost * pvf_operation)
            / (annual_energy * pvf_operation)) if generating else float("nan")

    # Recirculating power fraction
    fusion_cycle_gain = (
        driver_efficiency * gain * blanket_energy_multiple * thermal_efficiency
    )
    f_recirc = 1.0 / fusion_cycle_gain

    return {
        "generating": generating,
        "energy_on_target_J": energy_on_target,
        "fusion_energy_per_shot_J": fusion_energy_per_shot,
        "net_electric_power_W": net_electric_power,
        "net_electric_kw": net_electric_kw,
        "shots_per_year": shots_per_year,
        "driver_lifetime_years": driver_lifetime_years,
        "annual_capital_cost": annual_capital_cost,
        "annual_operating_cost": annual_operating_cost,
        "annual_energy_MWh": annual_energy,
        "pvf_construction": pvf_construction,
        "pvf_operation": pvf_operation,
        "lcoe_per_MWh": lcoe,
        "fusion_cycle_gain": fusion_cycle_gain,
        "recirculating_fraction": f_recirc,
    }


if __name__ == "__main__":
    cases = {
        "Historical Hawker default module scenario": compute_ife_lcoe(),
        "Historical realistic-HIF module scenario": compute_ife_lcoe(
            availability=0.85, driver_efficiency=0.25, driver_energy=5e6,
            driver_lifetime_shots=1e9, frequency=5.0, gain=100.0,
            discount_rate=0.05, target_cost_constant=0.50),
    }
    for label, result in cases.items():
        print(f"{label}: {result['lcoe_per_MWh']:.8f} $/MWh; "
              f"net {result['net_electric_power_W'] / 1e6:.4f} MW")
    print("Annual cash-flow oracle; use run_anchors.py to compare generated execution.")
    print("These historical module scenarios do not represent the computed Osiris point.")
