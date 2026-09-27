"""Finite scalar ABI helpers for reviewed equipment completions."""
import importlib
import math
def require(condition, message):
    if not condition: raise ValueError(message)
def values(inputs):
    data=inputs.model_dump()
    require(all(not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x) for x in data.values()), 'inputs must be finite numeric scalars')
    return {k.removesuffix('_in'):v for k,v in data.items()}
def finish(module, values):
    require(all(math.isfinite(x) for x in values.values()), 'outputs must be finite')
    if len(values)==1: return next(iter(values.values()))
    mod=importlib.import_module('component_alternatives_tea.schemas.'+module+'_output')
    schema=getattr(mod, '_'.join(x.capitalize() for x in module.split('_'))+'Output')
    require(set(schema.model_fields)==set(values), 'completion output contract mismatch')
    return next(iter(values.values())) if len(schema.model_fields)==1 else tuple(values[k] for k in schema.model_fields)
