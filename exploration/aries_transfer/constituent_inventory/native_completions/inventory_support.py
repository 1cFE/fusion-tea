"""Finite domain checks shared by the four small native inventory identities."""
import math

def numeric(inputs):
    values = {name.removesuffix('_in'): value for name, value in inputs.model_dump().items()}
    for name, value in values.items():
        if isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ValueError(name + ' must be finite nonnegative numeric')
    return values

def fraction(values, name):
    if values[name] > 1:
        raise ValueError(name + ' must be in [0,1]')

def checked(outputs):
    for name, value in outputs.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(name + ' must be finite nonnegative')
    return outputs
