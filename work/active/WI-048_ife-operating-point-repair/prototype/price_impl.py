def run_generating_electricity_price(inputs):
    """Price only generating points; zero is an invalid sentinel, never rankable."""
    if inputs.net_power <= 0.0:
        return 0.0, 0.0
    return inputs.numerator / inputs.denominator, 1.0
