"""WI-095 checks on the stored development receipts: the pre-change control (every channel of the WI-094 receipts equal bit for bit
on the new package) and the identities of 'Primary Bypass Control' (design section 6). Reads receipts only; writes one summary.

Run: verify_return_control.py [--runs <native_runs dir>] [--previous <WI-094 native_runs dir>] [--out <summary path>]
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
ROOT = Path(__file__).resolve().parents[2]
P = 'costed_loop_brayton__plant__'
RUNS = ROOT / 'work/active/WI-095_loop-return-control/evidence/native_runs'
PREVIOUS = ROOT / 'work/active/WI-094_costed-loop-brayton/evidence/native_runs'


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def compare_previous(new, old):
    """Every numeric channel and verdict status of the WI-094 receipt must reappear unchanged."""
    if old.get('status') != new.get('status'):
        return {'status_differs': [old.get('status'), new.get('status')]}
    if 'outputs' not in old or not old['outputs']:
        return {'compared': 0, 'differences': [], 'refused_both': True}
    diffs, compared = [], 0
    for key, value in old['outputs'].items():
        if numeric(value):
            compared += 1
            if new['outputs'].get(key) != value:
                diffs.append({'channel': key, 'previous': value, 'now': new['outputs'].get(key)})
        elif isinstance(value, dict) and 'status' in value:
            local = key.split('__plant__')[1].rsplit('__', 2)[0]
            match = [v for k, v in new['outputs'].items() if isinstance(v, dict) and 'status' in v and k.split('__plant__')[1].rsplit('__', 2)[0] == local]
            if not match or match[0]['status'] != value['status']:
                diffs.append({'verdict': key, 'previous': value['status'], 'now': match[0]['status'] if match else None})
    return {'compared': compared, 'differences': diffs}


def identities(row):
    o = row['outputs']
    g = lambda n: Decimal(repr(o[P + n]))
    tol = Decimal(repr(row['effective_inputs'][P + 'checks__energy_tolerance']))
    c_h = g('primary_loop__evaluate__mdot') * Decimal(repr(row['effective_inputs'][P + 'heat_exchangers__he_cp'])) / Decimal(1000000)
    f = g('return_control__evaluate__bypass_fraction')
    checks = {
        'capability_open_equals_closure_capability': o[P + 'return_control__evaluate__capability_open'] == o[P + 'heat_exchangers__evaluate__he_capability'],
        'feasible_iff_heat_removal_ok': (o[P + 'return_control__evaluate__feasible'] == 1.0) == (o[P + 'heat_exchangers__evaluate__unmet_heat'] <= float(tol)),
        'mixed_return_identity': abs(g('return_control__evaluate__mixed_return') - (g('primary_loop__evaluate__T_out') - g('return_control__evaluate__capability_at_solution') / c_h)) <= Decimal('1e-9'),
        'exchanger_return_le_mixed_le_T_out': o[P + 'return_control__evaluate__exchanger_return'] <= o[P + 'return_control__evaluate__mixed_return'] + 1e-9 <= o[P + 'primary_loop__evaluate__T_out'] + 2e-9,
        'residual_is_duty_minus_capability_over_C_h': abs(g('return_control__evaluate__return_residual') - ((g('primary_loop__evaluate__q_ihx') - g('return_control__evaluate__capability_at_solution')) / c_h + (g('primary_loop__evaluate__T_out') - g('primary_loop__evaluate__q_ihx') / c_h - g('primary_loop__evaluate__T_comp_in')))) <= Decimal('1e-9'),
        'zero_bypass_iff_zero_margin': (f <= Decimal('1e-9')) == (abs(g('heat_exchangers__evaluate__he_hot_bound_margin')) <= Decimal('1e-6')) or o[P + 'return_control__evaluate__feasible'] == 0.0,
        'exchanger_flow': o[P + 'return_control__evaluate__exchanger_primary_flow'] == (1.0 - o[P + 'return_control__evaluate__bypass_fraction']) * o[P + 'primary_loop__evaluate__mdot'],
        'return_check_matches_residual': ([v['status'] for k, v in o.items() if isinstance(v, dict) and 'return_condition_ok' in k][0] == 'satisfied') == (o[P + 'return_control__evaluate__return_residual_magnitude'] <= 1e-6),
    }
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=RUNS)
    parser.add_argument('--previous', type=Path, default=PREVIOUS)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    summary = {'cases': {}, 'passed': True}
    for case_dir in sorted(p for p in args.runs.iterdir() if p.is_dir()):
        row = json.loads((case_dir / 'result.json').read_text())
        old = json.loads((args.previous / case_dir.name / 'result.json').read_text())
        entry = {'pre_change_control': compare_previous(row, old)}
        if row.get('status') == 'evaluated' and row.get('outputs'):
            entry['identities'] = identities(row)
            entry['bypass_fraction'] = row['outputs'][P + 'return_control__evaluate__bypass_fraction']
            entry['feasible'] = row['outputs'][P + 'return_control__evaluate__feasible']
            entry['return_residual'] = row['outputs'][P + 'return_control__evaluate__return_residual']
            if not all(entry['identities'].values()):
                summary['passed'] = False
        if entry['pre_change_control'].get('differences') or 'status_differs' in entry['pre_change_control']:
            summary['passed'] = False
        summary['cases'][case_dir.name] = entry
    out = args.out or (args.runs.parent / 'return-control-verification.json')
    out.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'passed': summary['passed'], 'cases': {k: {'compared': v['pre_change_control'].get('compared'), 'diffs': len(v['pre_change_control'].get('differences', [])), 'f': v.get('bypass_fraction'), 'feasible': v.get('feasible'), 'identities_ok': all(v.get('identities', {True: True}).values())} for k, v in summary['cases'].items()}}, indent=1))
    raise SystemExit(0 if summary['passed'] else 1)


if __name__ == '__main__':
    main()
