from probe_selector.modules.probe.match import MatchInput
PROPERTY_CALLS = 0
def run_match(inputs: MatchInput) -> tuple[float,float,float]:
    global PROPERTY_CALLS
    if inputs.enabled_in == 0.0:
        return inputs.legacy_in, 0.0, 0.0
    if inputs.enabled_in != 1.0:
        raise ValueError("mode must be zero or one")
    PROPERTY_CALLS += 1
    if inputs.property_in <= 0.0:
        raise ValueError("toy property domain")
    return inputs.property_in * 10.0, inputs.property_in * 100.0, 2.0
