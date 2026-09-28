"""Readout of study 20260926-design-study-parameters-b from its stored results: every case with its bypass fraction, feasibility,
return residual, verdicts, net, nonfuel and total LCOE; the two comparison readings (arrangement B against the starting
configuration with its bypass; arrangement A among the matched-exchanger boundary points against the design-flow boundary
point). Presentation arithmetic on stored channels only. Run from the repository root: return_control_reporting.py <record-dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

P = 'costed_loop_brayton__plant__'
START = 'ir-f2500-r1.5183'
CONTRIB = ['capital', 'om', 'tritium', 'deuterium', 'consumables', 'imports', 'supply', 'replacement', 'other_overhaul', 'terminal', 'salvage']


def local(cid):
    return cid.split('__plant__')[1].rsplit('__', 1)[0]


def row(c):
    o = lambda n: c['outputs'][P + n]
    lcoe = o('lifecycle_price__evaluate__lcoe')
    contrib = {k: o(f'lifecycle_accounts__evaluate__{k}_lcoe') for k in CONTRIB}
    failed = sorted(local(cid) for cid, v in c['verdicts'].items() if v != 'satisfied')
    return {'case': c['case'], 'candidate': c['candidate_id'], 'flow': c['inputs'][P + 'cycle__selected_flow'], 'ratio': c['inputs'][P + 'compressor_1__selected_ratio'],
            'exchanger_area': c['inputs'][P + 'he_hx__selected_area'], 'compressor_rating': c['inputs'][P + 'compressor_capacity__selected_rating'],
            'net': o('electrical__evaluate__net_electric'), 'unmet': o('heat_exchangers__evaluate__unmet_heat'),
            'heater_inlet_K': o('heat_exchangers__evaluate__heater_inlet'), 'turbine_inlet_K': o('heat_exchangers__evaluate__turbine_temperature'),
            'bypass_fraction': o('return_control__evaluate__bypass_fraction'), 'feasible': o('return_control__evaluate__feasible'),
            'exchanger_primary_flow': o('return_control__evaluate__exchanger_primary_flow'), 'exchanger_return_K': o('return_control__evaluate__exchanger_return'),
            'mixed_return_K': o('return_control__evaluate__mixed_return'), 'return_residual_K': o('return_control__evaluate__return_residual'),
            'required_return_K': o('primary_loop__evaluate__T_comp_in'), 'uncontrolled_return_K': o('heat_exchangers__evaluate__he_return'),
            'passing': not failed, 'failed_checks': failed, 'annual_energy_mwh': o('lifecycle_accounts__evaluate__annual_energy'),
            'overnight': o('cost_ledger__evaluate__overnight'), 'lcoe': lcoe, 'contributions': contrib,
            'nonfuel_lcoe': lcoe - contrib['tritium'] - contrib['deuterium'] - contrib['supply']}


def deltas(r, base):
    return {'d_net': r['net'] - base['net'], 'd_lcoe': r['lcoe'] - base['lcoe'], 'd_nonfuel_lcoe': r['nonfuel_lcoe'] - base['nonfuel_lcoe'],
            'd_tritium_lcoe': r['contributions']['tritium'] - base['contributions']['tritium'], 'd_annual_energy_mwh': r['annual_energy_mwh'] - base['annual_energy_mwh']}


def main(record):
    record = Path(record)
    cases = json.load(open(record / 'results/cases.json'))['cases']
    plan = json.load(open(record / 'axis-plan.json'))
    rows = {c['case']: row(c) for c in cases}
    start = rows[START]
    boundary = {k: r for k, r in rows.items() if k.startswith('ir-boundary-')}
    design_flow_boundary = boundary['ir-boundary-f2500']
    for r in rows.values():
        r['vs_starting_configuration'] = deltas(r, start)
        r['vs_design_flow_boundary'] = deltas(r, design_flow_boundary)
    best_b = max((r for r in rows.values() if r['passing'] and r['case'].startswith('ir-')), key=lambda r: r['net'])
    best_a = max(boundary.values(), key=lambda r: r['net'])
    readout = {'study_id': record.name, 'starting_configuration': START, 'arrangement_B': {
                   'reading': 'every case that passes heat removal satisfies the completed loop model with the reported bypass fraction; the comparison base is the starting configuration with its own bypass',
                   'best_passing_case': best_b['case'], 'best_net': best_b['net'], 'starting_bypass_fraction': start['bypass_fraction']},
               'arrangement_A': {'reading': 'only the matched-exchanger boundary points (bypass fraction at the 1e-6 target) are consistent operating points; the comparison base is the design-flow boundary point',
                                 'boundary_cases': sorted(boundary), 'best_case': best_a['case'], 'best_net': best_a['net'], 'boundary_solve': plan['boundary_solve']},
               'rows': rows}
    (record / 'results/readout.json').write_text(json.dumps(readout, indent=1, allow_nan=False) + '\n')
    L = [f"# Readout: {record.name}", '', f"Stored channels of `results/cases.json` (USD2004, no-credit convention); deltas against the starting configuration `{START}` (arrangement B) and against the design-flow boundary point `ir-boundary-f2500` (arrangement A).", '',
         '## 1. Every stored case', '',
         '| Case | Flow / ratio | Net MW | Unmet MW | Bypass f | Feasible | Return residual K | Checks | Nonfuel LCOE | Tritium | Total LCOE | Δnet vs start | Δnet vs 2,500 boundary |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    order = [START] + sorted(k for k in rows if k not in (START,) and not k.startswith('ir-boundary')) + sorted(boundary)
    for k in order:
        r = rows[k]
        L.append(f"| `{k}` | {r['flow']:g} / {r['ratio']:.4f} | {r['net']:.3f} | {r['unmet']:.3f} | {r['bypass_fraction']:.4f} | {r['feasible']:.0f} | {r['return_residual_K']:+.2e} | {', '.join(x.split('__')[-1] if x.startswith('checks__') else x for x in r['failed_checks']) or 'all 11'} | {r['nonfuel_lcoe']:.2f} | {r['contributions']['tritium']:.2f} | {r['lcoe']:.2f} | {r['vs_starting_configuration']['d_net']:+.1f} | {r['vs_design_flow_boundary']['d_net']:+.1f} |")
    L += ['', '## 2. Arrangement A: the matched-exchanger boundary per flow', '', '| Flow | Bracket | Outcome | Ratio | Net MW (oracle) | Net MW (stored) |', '|---|---|---|---|---|---|']
    for e in plan['boundary_solve']:
        k = f"ir-boundary-f{e['flow']:g}"
        L.append(f"| {e['flow']:g} | {e['bracket']} | {e['outcome'][:70]} | {e.get('ratio', float('nan')):.6f} | {e.get('net_by_oracle', float('nan')):.3f} | {rows[k]['net'] if k in rows else float('nan'):.3f} |")
    L += ['', f"Best consistent point under A: `{best_a['case']}` at {best_a['net']:.3f} MW; best passing point under B: `{best_b['case']}` at {best_b['net']:.3f} MW (bypass {best_b['bypass_fraction']:.4f}); the starting configuration needs bypass {start['bypass_fraction']:.4f} under B and is not a consistent point under A."]
    (record / 'results/readout.md').write_text('\n'.join(L) + '\n')
    print(json.dumps({'cases': len(rows), 'best_B': (best_b['case'], round(best_b['net'], 3)), 'best_A': (best_a['case'], round(best_a['net'], 3)), 'start_f': round(start['bypass_fraction'], 4)}))


if __name__ == '__main__':
    main(sys.argv[1])
