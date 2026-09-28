"""Guard and output-order helpers for the reviewed native WI-089 calculations."""
import importlib
import math


def values(inputs):
    data = inputs.model_dump()
    if not all(math.isfinite(value) for value in data.values()):
        raise ValueError('all integrated inputs must be finite')
    return {name.removesuffix('_in'): value for name, value in data.items()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finish(schema, outputs):
    require(all(math.isfinite(value) for value in outputs.values()), 'nonfinite integrated output')
    module = importlib.import_module('whole_plant_conversion_tea.schemas.' + schema + '_output')
    name = ''.join(word.capitalize() + '_' for word in schema.split('_')).removesuffix('_') + 'Output'
    order = getattr(module, name).model_fields
    require(set(order) == set(outputs), 'completion output contract mismatch')
    return tuple(outputs[key] for key in order)
