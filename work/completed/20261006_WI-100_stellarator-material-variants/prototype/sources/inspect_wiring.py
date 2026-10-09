"""Scratch probe reader: the generated wiring of the reads P1 asks about, the P3 entry keys and the P4 stub."""
import json
import sys
from pathlib import Path

import yaml

pkg = Path(sys.argv[1])
prefix = sys.argv[2]
spec = yaml.safe_load((pkg / 'pipelines/pipeline.yaml').read_text())['modules']
contract = json.loads((pkg / 'contracts/model_contract.json').read_text())
keys = {p['qualified_name']: p for p in contract['parameters']}


def reads(module_suffix, formal=None):
    name = prefix + module_suffix
    if name not in spec:
        return {'module': name, 'missing': True}
    ins = spec[name]['inputs']
    return {'module': name, formal: ins.get(formal)} if formal else {'module': name, 'inputs': ins}


def producer_of(formal_value):
    """Name the source of an input spelled 'type source'."""
    return formal_value.split(' ', 1)[1] if formal_value else None


found = {}
for mod, body in spec.items():
    if not mod.startswith(prefix):
        continue
    for formal, value in (body.get('inputs') or {}).items():
        if formal in ('p_cryo', 'p_tf_extra', 'winding_cost', 'purchase_cost_in') or (
                mod.endswith(('cold_stage_capability', 'intercept_stage_capability')) and formal in ('demand_in', 'demand_available_in')):
            found.setdefault(mod, {})[formal] = producer_of(value)
out = dict(
    package=str(pkg), prefix=prefix,
    reads=found,
    entry_keys_matching={k: dict(entry_type=v['entry_type'], default=v.get('default_value'), python_type=v['python_type'])
                         for k, v in keys.items() if k.startswith(prefix) and any(
                             s in k for s in ('rebco_law_enabled', 'inventory_enabled', 'intercept_demand_available',
                                              'arm_slope', 'arm_x_ref', 'winding_account', 'purchase_cost_per_module'))},
)
print(json.dumps(out, indent=1))
