"""Presentation-only attribution ledger for the reconciliation study; reads native cases only.

Every number is selected from results/cases.json (or, for a dry run, from the oracle scan);
differences are arithmetic on native quantities and never replace a model output.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

P = 'aries_integrated_plant__'
CH = {
    'net': P + 'plant_ledger__evaluate__net_electric', 'gross': P + 'plant_ledger__evaluate__gross_electric',
    'aux': P + 'plant_ledger__evaluate__auxiliary_electric', 'accepted': P + 'heat_exchangers__evaluate__accepted_heat',
    'unmet': P + 'heat_exchangers__evaluate__unmet_heat', 'he_unmet': P + 'heat_exchangers__evaluate__he_unmet',
    'pbli_unmet': P + 'heat_exchangers__evaluate__pbli_unmet', 'div_unmet': P + 'heat_exchangers__evaluate__divertor_unmet',
    'available': P + 'plant_ledger__evaluate__total_available_heat', 'turbine_K': P + 'heat_exchangers__evaluate__turbine_temperature',
    'heater_in_K': P + 'heat_exchangers__evaluate__heater_inlet', 'eta': P + 'plant_ledger__evaluate__thermal_efficiency',
    'he_delivered': P + 'he_coolant__evaluate__delivered_heat', 'pbli_delivered': P + 'pbli_coolant__evaluate__delivered_heat',
    'div_delivered': P + 'divertor_coolant__evaluate__delivered_heat', 'he_hot_K': P + 'heat_exchangers__evaluate__he_hot',
    'pbli_return_K': P + 'heat_exchangers__evaluate__pbli_return', 'pbli_secondary_in_K': P + 'heat_exchangers__evaluate__pbli_secondary_in',
    'residual': P + 'plant_ledger__evaluate__plant_residual',
}
REFERENCE = {'net': 1000., 'gross': 1253., 'available': 2916., 'unmet': 0., 'turbine_K': 981.15}


def load(path: Path):
    doc = json.loads(path.read_text())
    rows = doc['cases']
    out = {}
    for row in rows:
        values = row.get('outputs') or row.get('values')
        if values is None:
            continue
        out[row['case']] = {k: float(values[c]) for k, c in CH.items() if c in values}
        out[row['case']]['verdicts'] = row.get('verdicts', {})
    return out


def delta(a, b, keys=('net', 'gross', 'unmet', 'accepted', 'turbine_K', 'eta')):
    return {k: b[k] - a[k] for k in keys if k in a and k in b}


def ledger(cases):
    base = cases['nominal-source-assumed']
    oat = {n: delta(base, cases[n]) for n in cases if n.startswith('oat-')}
    combos = {n: delta(base, cases[n]) for n in cases if n.startswith('combined-')}
    reverse = {}
    for c2, prefix in (('combined-source-thermal-lyon-aux', 'c2-minus-'), ('combined-c3-partition', 'c3-minus-')):
        for n in cases:
            if n.startswith(prefix):
                reverse[n] = delta(cases[c2], cases[n])
    brackets = {n: {'cycle_flow_case': n, **{k: cases[n][k] for k in ('net', 'gross', 'unmet', 'turbine_K')}} for n in cases if 'cycle-flow' in n}
    interactions = {}
    forward = {'recuperator_effectiveness': 'oat-recuperator-0.95', 'cycle_flow': 'oat-cycle-flow-1600', 'divertor_primary_flow': 'oat-divertor-flow-283', 'lyon_auxiliaries': 'oat-lyon-auxiliaries', 'source_partition': 'oat-source-partition'}
    backward = {'recuperator_effectiveness': 'c3-minus-recuperator', 'cycle_flow': 'c2-minus-cycle-flow', 'divertor_primary_flow': 'c2-minus-divertor-flow'}
    for name, fcase in forward.items():
        entry = {'forward_from_original': oat.get(fcase, {}).get('net')}
        if name in backward and backward[name] in cases:
            c = 'combined-c3-partition' if backward[name].startswith('c3') else 'combined-source-thermal-lyon-aux'
            entry['backward_from_combined'] = -(cases[backward[name]]['net'] - cases[c]['net'])
        interactions[name] = entry
    sum_oat = sum(v['net'] for k, v in oat.items() if k in forward.values())
    pick = lambda case, keys: {k: case[k] for k in keys if k in case}
    return {'original': pick(base, ('net', 'gross', 'aux', 'accepted', 'unmet', 'he_unmet', 'pbli_unmet', 'div_unmet', 'available', 'turbine_K', 'eta')),
            'reference': REFERENCE,
            'original_minus_reference': {k: base[k] - v for k, v in REFERENCE.items() if k in base},
            'one_at_a_time_from_original': oat, 'combined_from_original': combos,
            'reverse_one_at_a_time': reverse, 'cycle_flow_bracket': brackets,
            'interaction_check': {'sum_of_forward_net_deltas': sum_oat,
                                  'combined_c3_net_delta': combos.get('combined-c3-partition', {}).get('net'),
                                  'per_cause': interactions},
            'revised_cases': {n: pick(cases[n], ('net', 'gross', 'aux', 'accepted', 'unmet', 'he_unmet', 'pbli_unmet', 'div_unmet', 'available', 'turbine_K', 'eta', 'residual')) for n in ('combined-source-thermal', 'combined-source-thermal-lyon-aux', 'combined-c3-partition', 'combined-plus-ua-x10', 'c3-plus-ua-x10') if n in cases}}


def markdown(led):
    o, r = led['original'], led['reference']
    lines = ['| Case | Δnet MW | Δgross MW | Δunmet MW | Δaccepted MW | Δturbine K |', '|---|---:|---:|---:|---:|---:|']
    for group in ('one_at_a_time_from_original', 'combined_from_original', 'reverse_one_at_a_time'):
        for n, d in led[group].items():
            lines.append(f"| `{n}` | {d['net']:.3f} | {d['gross']:.3f} | {d['unmet']:.3f} | {d['accepted']:.3f} | {d['turbine_K']:.2f} |")
    head = [f"Original source-conditioned case: net {o['net']:.3f} MW (reference {r['net']}), gross {o['gross']:.3f} (reference {r['gross']}), unmet {o['unmet']:.3f} MW (PbLi {o.get('pbli_unmet', float('nan')):.3f}, He {o.get('he_unmet', float('nan')):.3f}, divertor {o.get('div_unmet', float('nan')):.3f}), available {o.get('available', float('nan')):.3f} MW (reference {r['available']}).", '']
    tail = ['', f"Sum of forward one-at-a-time net deltas: {led['interaction_check']['sum_of_forward_net_deltas']:.3f} MW; combined C3 net delta: {led['interaction_check']['combined_c3_net_delta']:.3f} MW. The difference is the interaction, not an error."]
    return '\n'.join(head + lines + tail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    led = ledger(load(args.cases))
    args.out.write_text(json.dumps(led, indent=2) + '\n')
    print(markdown(led))


if __name__ == '__main__':
    main()
