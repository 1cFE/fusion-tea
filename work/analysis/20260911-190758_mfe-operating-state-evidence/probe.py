"""Read-only T-015 probe; run through .codex-test/run from repository root."""
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e'))
import run_stellaris as rs
import run_stellaris_single as single
import verify_stellaris as oracle

P = rs.P
watched = ['sustain__p_aux_required', 'sustain__p_alpha_heat', 'fusion__p_fus',
           'heat__p_coupled', 'heat__p_wallplug_total', 'heat__p_delivered',
           'source_heat__q_source', 'primary_loop__mdot_loop',
           'primary_loop__p_pump_total', 'primary_loop__q_recovered_total',
           'cycle__eta_th', 'pb__p_th', 'pb__p_et', 'pb__p_net', 'pb__rec_frac',
           'heating_cost__cost', 'total_capital__total_capital', 'lcoe_calc__lcoe',
           'divheat__p_heat_abs', 'divheat__q_target_peak',
           'divheat__p_heat_operating_minus_installed']

def execute_case(name, reserve=None):
    case = OUT / name
    (case / 'pipelines').mkdir(parents=True, exist_ok=True)
    shutil.copytree(rs.GEN / 'inputs', case / 'inputs', dirs_exist_ok=True)
    shutil.copy2(rs.PIPELINE, case / 'pipelines/pipeline.yaml')
    if reserve is not None:
        path = case / 'inputs/stellarator_plant_params.json'
        data = json.loads(path.read_text())
        data[P + 'p_wallplug_heat'] = reserve
        path.write_text(json.dumps(data, indent=2) + '\n')
    original = rs.PIPELINE, rs.E2E
    rs.PIPELINE, rs.E2E = case / 'pipelines/pipeline.yaml', case
    try:
        outputs = single._execute_package()
    finally:
        rs.PIPELINE, rs.E2E = original
    serial = {k: v.model_dump(mode='json') if hasattr(v, 'model_dump') else v
              for k, v in outputs.items()}
    (case / 'all_outputs.json').write_text(json.dumps(serial, indent=2) + '\n')
    numbers = single._numeric_outputs(outputs)
    summary = {k: numbers[P + k] for k in watched}
    summary['verdicts'] = {k.removeprefix(P): v for k, v in serial.items()
                           if isinstance(v, dict)}
    return summary, numbers

baseline, numbers = execute_case('baseline')
reserve, _ = execute_case('reserve_120MW', 120.0)
o = oracle.compute()
parity_keys = ['p_fus', 'p_th', 'p_et', 'p_net', 'rec_frac', 'q_eng',
               'heating', 'lcoe', 'p_alpha_heat', 'p_aux_required', 'p_rad']
errors = {k: abs(numbers[rs.CH[k]] - o[k]) / max(abs(o[k]), 1e-30)
          for k in parity_keys}
assert max(errors.values()) < 1e-9, errors
assert reserve['sustain__p_aux_required'] == baseline['sustain__p_aux_required']
assert reserve['fusion__p_fus'] == baseline['fusion__p_fus']
assert reserve['heat__p_coupled'] == 60.0
assert reserve['heating_cost__cost'] > baseline['heating_cost__cost']
assert reserve['pb__p_net'] < baseline['pb__p_net']

# Algebraic counterfactual only: evaluate the existing mirror equations with
# required heating and the HELD constant efficiencies. Do not publish its cost
# outputs: that substitution also downsizes equipment in this uncorrected model.
old = oracle.IN['p_wallplug_heat']
oracle.IN['p_wallplug_heat'] = o['p_aux_required'] / o['heat_eta_pin_eff']
try:
    demand = oracle.compute()
finally:
    oracle.IN['p_wallplug_heat'] = old
keys = ['heat_coupled', 'heat_wallplug_total', 'p_aux_required', 'p_net', 'p_th',
        'p_et', 'loop_mdot_loop', 'loop_p_pump_total', 'loop_q_recovered_total',
        'divheat_p_heat_abs', 'divheat_q_target_peak']
counterfactual = {k: {'installed': o[k], 'required_substitution': demand[k],
                      'delta': demand[k] - o[k]} for k in keys}
files = sorted((ROOT / 'models/designs/generic_mfe').glob('*.sysml'))
files += sorted((ROOT / 'models/designs/stellarator_09').glob('*.sysml'))
files += sorted((ROOT / 'models/library/analyses').glob('mfe*.sysml'))
results = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
           'executable_fingerprint': rs.EXECUTABLE_FINGERPRINT,
           'model_sha256': {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
           'baseline': baseline, 'reserve_120MW': reserve,
           'baseline_oracle_max_relative_error': max(errors.values()),
           'baseline_oracle_channels_checked': len(errors),
           'algebraic_counterfactual_held_efficiencies_not_corrected_model': counterfactual}
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps({k: v for k, v in results.items() if k != 'model_sha256'}, indent=2))
