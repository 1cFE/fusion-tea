"""Legacy data adapter: unchanged input guards, dictionary output for new wrapper.

The stock generator omits the unbound legacy schema. Returning named values here
avoids fabricating a second generated module; legacy arithmetic is unchanged.
"""
import math


def values(inputs):
    data = inputs.model_dump()
    require(all(math.isfinite(value) for value in data.values()), 'all integrated inputs must be finite')
    return {name.removesuffix('_in'): value for name, value in data.items()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finish(schema, outputs):
    require(schema == 'network_heat_driven_closure', 'unexpected legacy schema')
    require(all(math.isfinite(value) for value in outputs.values()), 'nonfinite integrated output')
    return outputs
