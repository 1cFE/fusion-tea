from exp_toy_tea.modules.exp_toy.gaindoublings import GainDoublingsInput


def run_gaindoublings(inputs: GainDoublingsInput) -> float:
    """Execute GainDoublings calculation.

Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
Out-of-envelope: two inline invocations of Ln.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:53

SysML Expressions:
    doublings = Ln(target_gain) / Ln(LiteralRationalEvaluation())
    
Documentation:
Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
Out-of-envelope: two inline invocations of Ln.

Args:
    inputs: Input parameters validated against GainDoublingsInput schema

Returns:
    float: doublings

Example:
    >>> inputs = GainDoublingsInput(...)
    >>> result = run_gaindoublings(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        target_gain = inputs.target_gain
        # Perform calculation using extracted values
        # Return result(s)
    """
    # AI-pass implementation (exp() spike). Faithful translation of the SysML
    # expression at models/exp_toy.sysml:60:
    #   doublings = Ln(target_gain) / Ln(2.0)
    # Ln is the model's uninterpreted natural log -> math.log.
    import math

    return math.log(inputs.target_gain) / math.log(2.0)
