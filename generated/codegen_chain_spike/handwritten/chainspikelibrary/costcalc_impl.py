from chain_spike.modules.chainspikelibrary.costcalc import CostCalcInput


def run_costcalc(inputs: CostCalcInput) -> float:
    """Execute CostCalc calculation.

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:11

SysML Expressions:
    total_cost = area * rate

Args:
    inputs: Input parameters validated against CostCalcInput schema

Returns:
    float: total_cost

Example:
    >>> inputs = CostCalcInput(...)
    >>> result = run_costcalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        area = inputs.area
        rate = inputs.rate
        # Perform calculation using extracted values
        # Return result(s)
    """
    return inputs.area * inputs.rate
