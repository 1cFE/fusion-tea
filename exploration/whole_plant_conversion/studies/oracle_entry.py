"""Study API for the package's independent development verifier.

This adapter maps no physics and changes no operands or numerical tolerance.
Source/property provenance and independence limits belong to the verifier evidence.
"""
from exploration.whole_plant_conversion.verify import (
    absolute_tolerances,
    comparison_catalog,
    evaluate,
    operand_bindings,
)

__all__ = ["evaluate", "comparison_catalog", "operand_bindings", "absolute_tolerances"]
