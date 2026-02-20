"""Auto-generated implementation for volume.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    length * width * height
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.volume import volumeInput


def run_volume(inputs: volumeInput) -> float:
    """Execute volume calculation.

SysML Source: unknown:0

SysML Expressions:
    length * width * height

Args:
    inputs: Input parameters validated against volumeInput schema

Returns:
    float: volume

Example:
    >>> inputs = volumeInput(...)
    >>> result = run_volume(inputs)
    """
    return ((inputs.length * inputs.width) * inputs.height)
