"""Read-only review of committed exports and cited native artifact histories."""
import json
import math
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
STUDY = ROOT / 'exploration/stellarator_e2e/studies/20260911-operating-heating'


def read(name):
    return json.loads((STUDY / name).read_text())


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9), (actual, expected)


cases = read('results/cases.json')
raw = {case['candidate_id']: case for case in read('results/raw-cases.json')}
channels = read('preparation/required-channels.json')
inputs = read('results/package-inputs.json')
prefix = 'stellarator_09__stellaris__'
counts = Counter()
base = cases[2]['values']
for case in cases:
    values = case['values']
    original = raw[case['candidate_id']]
    assert len(case['verdicts']) == 18
    assert case['verdicts'] == original['verdicts']
    for name, channel in channels.items():
        assert values[name] == original['outputs'][channel]
    counts.update(key for key, verdict in case['verdicts_by_local_identity'].items() if verdict == 'violated')
    actual_inputs = {**inputs, **case['inputs']}
    parameter = lambda name: actual_inputs[prefix + name]
    demand = values['p_aux_required']
    close(values['operating_heat_coupled'], demand)
    close(values['operating_heat_delivered'], demand / parameter('eta_couple_heat'))
    close(values['operating_heat_wallplug'], demand / parameter('eta_couple_heat') / parameter('eta_source_heat'))
    close(values['divheat_p_heat_operating_minus_installed'], demand - values['heat_coupled'])
    close(values['heating'], values['heat_delivered'] * 5282900)
    close(values['q_source'], parameter('mn') * values['p_fus'] * (1 - 3.52 / 17.58) + values['p_fus'] * 3.52 / 17.58 + demand)
    discount = parameter('discount_rate')
    years = parameter('operational_years')
    recovery = discount / (1 - (1 + discount) ** (-years))
    annual = sum(original['outputs'][prefix + name] for name in ['cas71_calc__levelized', 'cas80_calc__levelized']) + values['cas72_annual']
    energy = 8760 * values['p_net'] * values['calendar_availability']
    close(values['lcoe'], (values['total_capital'] * (1 + discount) ** (parameter('construction_years') / 2) * recovery + annual) / energy)
    close(values['lcoe_1cfe'], ((values['overnight_capital'] + values['idc_capital']) * recovery + annual) / energy)
    if case['arm_id'] == 'arm-reserve':
        for name in ['operating_heat_coupled', 'q_source', 'p_net', 'divheat_q_target_peak', 'calendar_availability', 'cas72_annual']:
            assert values[name] == base[name]
    else:
        assert values['heating'] == base['heating']
assert len(cases) == 15 and len(channels) == 141
assert counts == Counter(divertor_heat_ok=15, sustainment_ok=2, wall_load_ok=6, loop_capacity_ok=6, burn_hold_ok=2)
assert not any(case['feasible'] for case in cases)
assert cases[13]['values']['p_aux_required'] > 0 > cases[14]['values']['p_aux_required']
extra = read('results/additional-verification.json')
assert len(extra['identities']) == 566 and len(extra['oracle_comparisons']) == 2115
assert not extra['failed'] and all(row['pass'] for row in extra['identities'] + extra['oracle_comparisons'])

# Git history is read directly; this adds no goal-level fingerprint guard.
references = [
    ('work/active/WI-050_mfe-coherent-operating-heating', '55456198'),
    ('.project/active/mfe-operating-heating-study-package', '07c33fee'),
    ('work/orchestration/goals/fusion-audit-remediation/evidence/T-018_integration', '0f6e4bef'),
    ('exploration/stellarator_e2e/studies/20260911-operating-heating', '91b0d96e'),
    ('exploration/stellarator_e2e/studies/20260911-operating-heating/synthesis.md', 'a408429a'),
]
history = {}
for path, revision in references:
    subprocess.run(['git', 'cat-file', '-e', f'{revision}:{path}'], cwd=ROOT, check=True)
    history[path] = subprocess.check_output(['git', 'log', '--oneline', f'{revision}..HEAD', '--', path], cwd=ROOT, text=True).strip()
subprocess.run(['git', 'merge-base', '--is-ancestor', 'dde47316', 'HEAD'], cwd=ROOT, check=True)
print(json.dumps({'outcome': 'PASS', 'cases': len(cases), 'raw_channel_matches': len(cases) * len(channels), 'violation_counts': dict(counts), 'history_after_citation': history, 'scope': 'Export arithmetic and native history reading; no model execution or source recertification.'}, indent=2))
