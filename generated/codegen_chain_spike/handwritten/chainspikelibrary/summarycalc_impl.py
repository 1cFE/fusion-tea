from chain_spike.modules.chainspikelibrary.summarycalc import SummaryCalcInput


def run_summarycalc(inputs: SummaryCalcInput) -> float:
    """Execute SummaryCalc calculation.

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:18

SysML Expressions:
    cost_per_area = cost / area

Args:
    inputs: Input parameters validated against SummaryCalcInput schema

Returns:
    float: cost_per_area

Example:
    >>> inputs = SummaryCalcInput(...)
    >>> result = run_summarycalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        area = inputs.area
        cost = inputs.cost
        # Perform calculation using extracted values
        # Return result(s)
    """
    return inputs.cost / inputs.area
