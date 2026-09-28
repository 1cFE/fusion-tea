"""Read-only T-002 diagnostics; output contains no acceptance changes."""
import collections
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT), str(ROOT/'exploration/stellarator_e2e/studies'), str(ROOT/'exploration/stellarator_e2e/pkg'), str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
import oracle_entry as oe
import study_route as route
from tests.models.current_mfe_regressions import WI059_REPLAY, WI059_REPLAY_LOCAL
from simkit.study.bridge import CandidateBridge

out = {}
duplicates = collections.defaultdict(list)
for name, channel in oe.ORACLE_OUTPUT_TO_CHANNEL.items():
    duplicates[channel].append(name)
out['duplicate_channels'] = {k:v for k,v in duplicates.items() if len(v)>1}
out['replay_mapping_disagreement'] = {k:dict(hand=v, mapped=oe._oracle_overrides(WI059_REPLAY).get(k)) for k,v in WI059_REPLAY_LOCAL.items() if oe._oracle_overrides(WI059_REPLAY).get(k) != v}
out['route_boolean_refusals'] = {k:v for k,v in WI059_REPLAY.items() if route.validate_proposal({k:v}) is None}
out['route_whole_replay'] = route.validate_proposal(WI059_REPLAY)
base = oe._compute({})
out['duplicate_values'] = {channel:{name:base[name] for name in names} for channel,names in out['duplicate_channels'].items()}
out['inventory_effect'] = {key: dict(current=base[key], held=oe._compute({'inventory_inventory_enabled':False,'inventory_held_inventory':0.,'processing_enabled':False})[key]) for key in ('fuel_tbr_required','fuel_tbr_margin')}
entering = ROOT/'work/orchestration/goals/divertor-peak-heat-load/evidence/entering/verify_stellaris.py'
spec = importlib.util.spec_from_file_location('entering_probe', entering)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
prepared = route.prepare(route.PACKAGE_DIR, Path('/tmp/t002-boundary-probe'))
bridge = CandidateBridge(prepared.entry_models)
out['boundary'] = []
for sized in (False,True):
    point = {oe.P+'plasma__R':13.5, oe.P+'plasma__a':1.5, oe.P+'magnet__coil__I_coil':16e6}
    if sized:
        point.update({oe.P+'magnet__winding_pack__sizing_mode':1.,oe.P+'magnet__coil__coil_t':.65,oe.P+'magnet__casing__interior_y':.65})
    old.IN.update(oe._oracle_overrides(point))
    prior = old.compute()
    current = oe._compute(oe._oracle_overrides(point))
    native = prepared.evaluate(bridge.build(point))
    names = ['sizing_required_conductor_area','conductor_margin_current','conductor_margin_fraction']
    row = dict(sized=sized, values={})
    for name in names:
        if name in current:
            channel = oe.ORACLE_OUTPUT_TO_CHANNEL.get(name)
            row['values'][name] = dict(entering=prior.get(name), current=current[name],native=native.outputs.get(channel),ulp_difference=(current[name]-prior[name])/math.ulp(prior[name]) if name in prior and prior[name] != 0 else None)
    row['strict_native_predicates'] = dict(native.responses)
    row['native_evaluations'] = {k:dict(v) for k,v in native.evaluations.items()} if hasattr(native,'evaluations') else str(native)
    out['boundary'].append(row)
print(json.dumps(out,indent=2,default=lambda obj:dict(obj)))
