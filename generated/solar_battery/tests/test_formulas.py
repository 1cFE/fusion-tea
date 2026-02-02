"""Formula verification tests for the 5 system-level calc implementations.

Uses known design parameter values from models/tests/solar_battery/design_params.json
and expected outputs from expected_system_outputs.csv.
"""

import pytest

from solar_battery.modules.solarbatterylibrary.energyproductioncalc import EnergyProductionCalcInput
from solar_battery.modules.solarbatterylibrary.annualizedomcalc import AnnualizedOMCalcInput
from solar_battery.modules.solarbatterylibrary.annualizedfuelcalc import AnnualizedFuelCalcInput
from solar_battery.modules.solarbatterylibrary.annualizedfinancialcalc import AnnualizedFinancialCalcInput
from solar_battery.modules.solarbatterylibrary.lcoecalc import LCOECalcInput

from solar_battery.handwritten.solarbatterylibrary.energyproductioncalc_impl import run_energyproductioncalc
from solar_battery.handwritten.solarbatterylibrary.annualizedomcalc_impl import run_annualizedomcalc
from solar_battery.handwritten.solarbatterylibrary.annualizedfuelcalc_impl import run_annualizedfuelcalc
from solar_battery.handwritten.solarbatterylibrary.annualizedfinancialcalc_impl import run_annualizedfinancialcalc
from solar_battery.handwritten.solarbatterylibrary.lcoecalc_impl import run_lcoecalc


def test_energy_production_formula():
    """8760 * 0.008 * 1.0 * 0.159 = 11.14272"""
    inputs = EnergyProductionCalcInput(p_net_mw=0.008, n_mod=1.0, plant_availability=0.159)
    result = run_energyproductioncalc(inputs)
    assert result == pytest.approx(11.14272, rel=0.001)


def test_annualized_om_formula():
    """20.0 * 8.0 = 160.0"""
    inputs = AnnualizedOMCalcInput(om_rate_per_kw_year=20.0, p_net_kw=8.0)
    result = run_annualizedomcalc(inputs)
    assert result == pytest.approx(160.0, rel=0.001)


def test_annualized_fuel_formula():
    """0.0 * 0.0 = 0.0"""
    inputs = AnnualizedFuelCalcInput(fuel_unit_cost=0.0, fuel_consumption=0.0)
    result = run_annualizedfuelcalc(inputs)
    assert result == 0.0


def test_annualized_financial_formula():
    """CRF = 0.05 * (1.05)^25 / ((1.05)^25 - 1) = 0.070952
    annualized_capital_cost = 0.070952 * 41205.0 = 2923.60"""
    inputs = AnnualizedFinancialCalcInput(
        total_capex=41205.0, discount_rate=0.05, plant_lifetime=25.0
    )
    crf, annualized_capital_cost = run_annualizedfinancialcalc(inputs)
    assert crf == pytest.approx(0.070952, rel=0.001)
    assert annualized_capital_cost == pytest.approx(2923.60, rel=0.001)


def test_lcoe_formula():
    """(2923.60 + (160.0 + 0.0) * (1.0245)^25) / 11.14272 ≈ 288.68"""
    inputs = LCOECalcInput(
        annualized_capital_cost=2923.60,
        annual_om_cost=160.0,
        annual_fuel_cost=0.0,
        yearly_inflation=0.0245,
        plant_lifetime=25.0,
        annual_energy_mwh=11.14272,
    )
    result = run_lcoecalc(inputs)
    assert result == pytest.approx(288.68, rel=0.01)
