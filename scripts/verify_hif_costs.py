"""Independent source-equation checks for the computed Osiris-based IFE point.

Meier Eqs. 1–5 retain 1988 dollars and their fixed charge convention. Hawker
uses a separate annual cash-flow oracle. Printed Osiris facts remain a distinct
1992-dollar reference; proximity of the computed price is not source validation.
Source: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_ife_lcoe import compute_ife_lcoe


def compute_meier_driver_cost(
    beam_energy_mj: float,
    driver_efficiency: float,
    num_chambers: float,
    rep_rate: float,
) -> tuple[float, float]:
    """Meier Eq. 5: HIF driver cost.

    Returns (cost_billions, gamma_per_joule).
    """
    cost_billions = (
        (0.32 + 0.088 * beam_energy_mj)
        * (1.25 + 0.05 * num_chambers)
        * (1.0 + 0.0088 * (rep_rate - 5.0))
    )
    bank_energy_joules = beam_energy_mj * 1.0e6 / driver_efficiency
    gamma = cost_billions * 1.0e9 / bank_energy_joules
    return cost_billions, gamma


def compute_meier_reactor_cost(
    thermal_power_gw: float,
    num_units: float,
) -> float:
    """Meier Eq. 3: reactor plant direct cost [$B, 1988$]."""
    return 0.66 * (thermal_power_gw / 1.67) ** 0.49 * (0.72 * num_units + 0.28)


def compute_meier_capital_cost(
    reactor_cost: float,
    driver_cost: float,
    target_factory_cost: float,
) -> float:
    """Meier Eq. 2: total capital cost [$B, 1988$]."""
    return 1.83 * (reactor_cost + driver_cost + target_factory_cost)


def compute_meier_coe(
    total_capital_billions: float,
    availability: float,
    net_electric_power_gw: float,
) -> float:
    """Meier Eq. 1: cost of electricity [cents/kWh, 1988$]."""
    if net_electric_power_gw <= 0:
        return float("nan")
    return (0.113 * total_capital_billions) / (0.0876 * availability * net_electric_power_gw)


# Source transcription: Osiris column, image page_007_table_0.png in
# knowledge/sources/energy_from_inertial_fusion/images/. These rounded printed
# facts are reference data, not simultaneous exact constraints on the computed case.
OSIRIS_SOURCE = dict(beam_mj=5.0, gain=87.0, yield_mj=432.0, frequency=4.6,
                     efficiency=0.28, thermal_mw=2504.0, gross_mw=1127.0,
                     driver_mw=82.0, auxiliary_mw=45.0, net_mw=1000.0,
                     coe_1992_cents_kwh=5.6)


def computed_osiris():
    """Computed common operating point; retain Meier 1988-dollar conventions."""
    cost, gamma = compute_meier_driver_cost(5.0, 0.28, 1.0, 4.6)
    bank = 5e6 / 0.28
    thermal_gw = 5e6 * 87 * 4.6 * 1.15 / 1e9
    net_gw = thermal_gw * 0.45 - 2 * bank * 4.6 / 1e9
    capital = compute_meier_capital_cost(compute_meier_reactor_cost(thermal_gw, 1), cost, 0.1)
    hawker = compute_ife_lcoe(
        availability=0.90, blanket_energy_multiple=1.15, discount_rate=0.08,
        driver_cost_constant=gamma, driver_efficiency=0.28, driver_energy=bank,
        driver_lifetime_shots=6e9, frequency=4.6, gain=87.0,
        om_cost_constant=65.0, plant_cost_constant=2000.0,
        target_cost_constant=10.0, thermal_efficiency=0.45, yield_cost_constant=5e6)
    assert abs(gamma * bank - cost * 1e9) <= 1e-9 * cost * 1e9
    assert abs(hawker["net_electric_power_W"] / 1e9 - net_gw) < 1e-9
    assert OSIRIS_SOURCE["gross_mw"] - OSIRIS_SOURCE["driver_mw"] - OSIRIS_SOURCE["auxiliary_mw"] == OSIRIS_SOURCE["net_mw"]
    return dict(driver_cost_billions=cost, gamma=gamma, bank_j=bank,
                thermal_gw=thermal_gw, net_gw=net_gw, capital_billions=capital,
                meier_coe=compute_meier_coe(capital, 0.90, net_gw), **hawker)


if __name__ == "__main__":
    import json
    print("Computed Osiris-based point: gain 87 gives 435 MJ; printed yield is 432 MJ.")
    print("Hawker equal driver/cooling allowance, M=1.15, availability=0.90.")
    print("Hawker $/MWh and Meier 1988 cents/kWh retain distinct finance bases.")
    print(json.dumps(computed_osiris(), indent=2))
    print("Printed Osiris reference: 2504 MW thermal, 1000 MW net, 5.6 in 1992 cents/kWh.")
