from ife_tea.modules.ife_lcoe.generating_electricity_price import Generating_Electricity_PriceInput


def run_generating_electricity_price(inputs: Generating_Electricity_PriceInput) -> tuple[float, float]:
    """Return price and 0/1 validity; non-generating zero is an invalid sentinel.

    Finance and power arithmetic remain in SysML. This implements only the
    final strict-positive quotient specified by Generating Electricity Price.
    """
    if inputs.net_power > 0.0:
        return inputs.numerator / inputs.denominator, 1.0
    return 0.0, 0.0
