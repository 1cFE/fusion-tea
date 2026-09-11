"""IFE consumer eligibility. A zero price sentinel never represents a generator."""

import math

P = "hif_plant_pkg__hif_plant__"
NET_POSITIVE_ID = P + "net_positive__1d299cceab19c61c"


def price_eligible(price, generating, net_positive):
    """Require both execution evidence fields before using a positive finite price."""
    return (generating == 1.0 and net_positive == "satisfied"
            and isinstance(price, (int, float)) and math.isfinite(price) and price > 0)


def require_price(price, generating, net_positive):
    """Fail an anchor closed when generation evidence is absent or contradictory."""
    if not price_eligible(price, generating, net_positive):
        raise ValueError("IFE price is ineligible: require generating=1 and satisfied net_positive")
    return price


def module_price(balance):
    """Compose the generated balance, guarded quotient and named generation predicate."""
    from ife_tea.handwritten.ife_lcoe.generating_electricity_price_impl import run_generating_electricity_price
    from ife_tea.modules.ife_lcoe.generating_electricity_price import Generating_Electricity_PriceInput
    from ife_tea.modules.constraints.predicates import (
        _finalize_assertion, constraint_pred_definition_fusion_cycle__positive_net_generation,
    )
    from ife_tea.schemas.generating_electricity_price_output import Generating_Electricity_PriceOutput
    price, generating = run_generating_electricity_price(Generating_Electricity_PriceInput(
        net_power=balance.net_electric_power, numerator=balance.discounted_cost,
        denominator=balance.discounted_energy))
    verdict = _finalize_assertion(
        constraint_pred_definition_fusion_cycle__positive_net_generation(balance.net_electric_power),
        is_negated=False, expected_value=True)
    return Generating_Electricity_PriceOutput(price=price, generating=generating), verdict.status


def lcoe_inputs(params):
    """Map historical module scenario names to the generated calculation interface."""
    renamed = {"thermal_efficiency", "discount_rate", "availability", "om_cost_constant",
               "plant_cost_constant", "gain", "frequency"}
    return {key + "_in" if key in renamed else key: value for key, value in params.items()}


def module_balance(params):
    """Use the generated wrapper's named outputs, avoiding positional tuple guesses."""
    from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEModule
    from ife_tea.modules.ife_lcoe.ife_present_value_factors import IFE_Present_Value_FactorsModule
    inputs = lcoe_inputs(params)
    factors = IFE_Present_Value_FactorsModule().run(
        discount_rate_in=inputs['discount_rate_in'],
        construction_years_in=inputs.get('construction_years', 5.0),
        operational_years_in=inputs.get('operational_years', 40.0)).data
    return IFE_LCOEModule().run(
        **inputs, pvf_construction=factors.construction_factor,
        pvf_operation=factors.operation_factor).data
