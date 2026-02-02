from chain_spike.modules.chainspikelibrary.areacalc import AreaCalcInput


def run_areacalc(inputs: AreaCalcInput) -> float:
    """Execute AreaCalc calculation.

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:4

SysML Expressions:
    area = length * width

Args:
    inputs: Input parameters validated against AreaCalcInput schema

Returns:
    float: area

Example:
    >>> inputs = AreaCalcInput(...)
    >>> result = run_areacalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        length = inputs.length
        width = inputs.width
        # Perform calculation using extracted values
        # Return result(s)
    """
    return inputs.length * inputs.width
