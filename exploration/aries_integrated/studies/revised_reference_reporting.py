"""Presentation-only ledger for the revised-reference network study; reads native cases only.

Every number is selected from results/cases.json (or, for a dry run, from the oracle scan);
differences are arithmetic on native quantities and never replace a model output. The
materiality budget lines are copied from the goal's evidence/materiality-budget.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exploration.aries_integrated.studies import reconciliation_reporting as base

P = base.P
CH = dict(base.CH)
CH.update({
    'mode': P + 'heat_exchangers__evaluate__network_mode_used', 'split': P + 'heat_exchangers__evaluate__pbli_split_used',
    'pbli_stream_K': P + 'heat_exchangers__evaluate__pbli_stream_out', 'div_stream_K': P + 'heat_exchangers__evaluate__divertor_stream_out',
    'mixed_K': P + 'heat_exchangers__evaluate__mixed_outlet', 'he_secondary_out_K': P + 'heat_exchangers__evaluate__he_secondary_out',
    'compressor_demand': P + 'plant_ledger__evaluate__compressor_demand', 'compressor_rating': P + 'compressor_capacity__selected_rating',
})
REFERENCE = base.REFERENCE
BUDGET = {'net': 15.0, 'gross': 15.0, 'available': 10.0, 'unmet': 0.0, 'turbine_K': 5.0}
PICK = ('mode', 'split', 'net', 'gross', 'aux', 'available', 'accepted', 'unmet', 'he_unmet', 'pbli_unmet', 'div_unmet',
        'turbine_K', 'heater_in_K', 'he_secondary_out_K', 'pbli_stream_K', 'div_stream_K', 'eta', 'compressor_demand', 'residual')
ORDER_BASES = [('original', 'nominal-source-assumed', 'network-original-0.85'), ('C1', 'combined-source-thermal', 'network-c1-0.85'),
               ('C2', 'combined-source-thermal-lyon-aux', 'network-c2-0.85'), ('C3', 'combined-c3-partition', 'network-c3-0.85')]
SPLITS = ['network-c3-0.50', 'network-c3-0.60', 'network-c3-0.70', 'network-c3-0.80', 'network-c3-0.85', 'network-c3-0.90', 'network-c3-0.95', 'network-c3-0.98']
CANDIDATES = ['network-c3-eps0.8-0.70', 'network-c3-eps0.8-0.85', 'network-c3-eps0.8-0.95', 'c3-minus-recuperator']
FLOW = ['network-c3-1700-0.85', 'network-c3-1800-0.85', 'resized-compressor-1700-series', 'resized-compressor-1700-network-0.85',
        'resized-compressor-1800-series', 'resized-compressor-1800-network-0.85']
HEADLINE = ['nominal-source-assumed', 'combined-c3-partition', 'network-c3-0.85', 'network-c3-0.90', 'network-c3-eps0.8-0.85',
            'c3-minus-recuperator', 'resized-compressor-1800-network-0.85', 'resized-compressor-1800-series']


def load(path: Path):
    doc = json.loads(path.read_text())
    out = {}
    for row in doc['cases']:
        values = row.get('outputs') or row.get('values')
        if values is None:
            continue
        out[row['case']] = {k: float(values[c]) for k, c in CH.items() if c in values}
        out[row['case']]['verdicts'] = row.get('verdicts', {})
    return out


def pick(case, keys=PICK):
    return {k: case[k] for k in keys if k in case}


def all_checks(case):
    v = case.get('verdicts') or {}
    return bool(v) and all(x == 'satisfied' for x in v.values())


def failed_checks(case):
    return sorted(k for k, x in (case.get('verdicts') or {}).items() if x != 'satisfied')


def against_reference(case):
    row = {}
    for k, ref in REFERENCE.items():
        if k in case:
            diff = case[k] - ref
            row[k] = {'model': case[k], 'reference': ref, 'difference': diff,
                      'within_budget': abs(diff) <= BUDGET[k] if k != 'unmet' else case[k] <= 1e-6}
    return row


def ledger(cases):
    delta = base.delta
    orig = cases['nominal-source-assumed']
    chain_names = ['nominal-source-assumed', 'combined-source-thermal', 'combined-source-thermal-lyon-aux', 'combined-c3-partition']
    chain = []
    for i, name in enumerate(chain_names):
        entry = {'case': name, 'values': pick(cases[name]), 'all_checks': all_checks(cases[name]), 'failed_checks': failed_checks(cases[name])}
        if i:
            entry['step_delta'] = delta(cases[chain_names[i - 1]], cases[name])
            entry['cumulative_delta_from_original'] = delta(orig, cases[name])
        chain.append(entry)
    order = []
    for label, series, network in ORDER_BASES:
        if series in cases and network in cases:
            order.append({'position': label, 'series_case': series, 'network_case': network,
                          'network_delta': delta(cases[series], cases[network]),
                          'series': pick(cases[series]), 'network': pick(cases[network]),
                          'network_all_checks': all_checks(cases[network]), 'network_failed_checks': failed_checks(cases[network])})
    sweep = [{'case': n, **pick(cases[n]), 'all_checks': all_checks(cases[n]), 'failed_checks': failed_checks(cases[n])} for n in SPLITS if n in cases]
    candidates = [{'case': n, **pick(cases[n]), 'all_checks': all_checks(cases[n]), 'failed_checks': failed_checks(cases[n]),
                   'delta_from_original': delta(orig, cases[n]), 'against_reference': against_reference(cases[n])} for n in CANDIDATES if n in cases]
    flow = [{'case': n, **pick(cases[n]), 'compressor_rating': cases[n].get('compressor_rating'), 'all_checks': all_checks(cases[n]),
             'failed_checks': failed_checks(cases[n]), 'delta_from_original': delta(orig, cases[n])} for n in FLOW if n in cases]
    c3 = cases['combined-c3-partition']
    n_orig = cases['network-original-0.85']
    n_c3 = cases['network-c3-0.85']
    interaction = {
        'corrections_alone_net': c3['net'] - orig['net'], 'network_alone_at_original_net': n_orig['net'] - orig['net'],
        'sum_net': (c3['net'] - orig['net']) + (n_orig['net'] - orig['net']), 'combined_net': n_c3['net'] - orig['net'],
        'interaction_net': (n_c3['net'] - orig['net']) - ((c3['net'] - orig['net']) + (n_orig['net'] - orig['net'])),
        'corrections_alone_unmet': c3['unmet'] - orig['unmet'], 'network_alone_at_original_unmet': n_orig['unmet'] - orig['unmet'],
        'combined_unmet': n_c3['unmet'] - orig['unmet'],
        'interaction_unmet': (n_c3['unmet'] - orig['unmet']) - ((c3['unmet'] - orig['unmet']) + (n_orig['unmet'] - orig['unmet']))}
    headline = {n: {'values': pick(cases[n]), 'all_checks': all_checks(cases[n]), 'failed_checks': failed_checks(cases[n]),
                    'against_reference': against_reference(cases[n])} for n in HEADLINE if n in cases}
    return {'study': '20260925-aries-revised-reference-network', 'reference': REFERENCE, 'budget': BUDGET,
            'controls': {n: pick(cases[n]) for n in ('nominal-calculated', 'nominal-source-assumed', 'literal-Lyon-source-input') if n in cases},
            'series_chain': chain, 'network_step_by_position': order, 'split_sweep_at_c3': sweep,
            'revised_candidates': candidates, 'flow_bracket_and_resized_alternative': flow,
            'interaction_check': interaction, 'headline_against_reference': headline,
            'all_checks_cases': sorted(n for n in cases if all_checks(cases[n]))}


def fmt(x):
    return f'{x:.3f}' if isinstance(x, float) else str(x)


def markdown(led):
    lines = ['# Revised-reference network ledger (presentation only)', '']
    lines += ['## Series chain (retained round-1 cases)', '', '| Case | unmet | he | PbLi | div | turbine K | gross | net | all checks | step Δnet | cumulative Δnet |', '|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|']
    for e in led['series_chain']:
        v = e['values']
        lines.append(f"| {e['case']} | {fmt(v['unmet'])} | {fmt(v['he_unmet'])} | {fmt(v['pbli_unmet'])} | {fmt(v['div_unmet'])} | {fmt(v['turbine_K'])} | {fmt(v['gross'])} | {fmt(v['net'])} | {e['all_checks']} | {fmt(e.get('step_delta', {}).get('net', 0.0))} | {fmt(e.get('cumulative_delta_from_original', {}).get('net', 0.0))} |")
    lines += ['', '## Network step by position in the change order (split 0.85)', '', '| Position | series unmet | network unmet (he / PbLi / div) | Δunmet | series net | network net | Δnet | network all checks |', '|---|---:|---:|---:|---:|---:|---:|---|']
    for o in led['network_step_by_position']:
        s, n = o['series'], o['network']
        lines.append(f"| {o['position']} | {fmt(s['unmet'])} | {fmt(n['unmet'])} ({fmt(n['he_unmet'])} / {fmt(n['pbli_unmet'])} / {fmt(n['div_unmet'])}) | {fmt(o['network_delta']['unmet'])} | {fmt(s['net'])} | {fmt(n['net'])} | {fmt(o['network_delta']['net'])} | {o['network_all_checks']} |")
    lines += ['', '## Split sensitivity at C3 (0.95 recuperation, 1600 kg/s)', '', '| Case | split | unmet | he | PbLi | div | turbine K | PbLi stream K | div stream K | gross | net | all checks |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in led['split_sweep_at_c3']:
        lines.append(f"| {r['case']} | {fmt(r['split'])} | {fmt(r['unmet'])} | {fmt(r['he_unmet'])} | {fmt(r['pbli_unmet'])} | {fmt(r['div_unmet'])} | {fmt(r['turbine_K'])} | {fmt(r.get('pbli_stream_K'))} | {fmt(r.get('div_stream_K'))} | {fmt(r['gross'])} | {fmt(r['net'])} | {r['all_checks']} |")
    lines += ['', '## Revised candidates (0.8 recuperation, 1600 kg/s) and the series steady point', '', '| Case | mode | split | unmet | turbine K | eta | gross | net | all checks | failed |', '|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
    for r in led['revised_candidates']:
        lines.append(f"| {r['case']} | {fmt(r['mode'])} | {fmt(r['split'])} | {fmt(r['unmet'])} | {fmt(r['turbine_K'])} | {fmt(r['eta'])} | {fmt(r['gross'])} | {fmt(r['net'])} | {r['all_checks']} | {', '.join(r['failed_checks']) or '—'} |")
    lines += ['', '## Flow bracket on the inherited rating and the declared resized-compressor alternative', '', '| Case | mode | rating MW | compressor demand MW | unmet | turbine K | gross | net | all checks | failed |', '|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
    for r in led['flow_bracket_and_resized_alternative']:
        lines.append(f"| {r['case']} | {fmt(r['mode'])} | {fmt(r.get('compressor_rating'))} | {fmt(r.get('compressor_demand'))} | {fmt(r['unmet'])} | {fmt(r['turbine_K'])} | {fmt(r['gross'])} | {fmt(r['net'])} | {r['all_checks']} | {', '.join(r['failed_checks']) or '—'} |")
    i = led['interaction_check']
    lines += ['', f"Interaction (net): corrections alone {fmt(i['corrections_alone_net'])} + network alone at the original inputs {fmt(i['network_alone_at_original_net'])} = {fmt(i['sum_net'])} MW against the combined {fmt(i['combined_net'])} MW; the difference {fmt(i['interaction_net'])} MW is the order interaction, not an error. Unmet heat: {fmt(i['corrections_alone_unmet'])} + {fmt(i['network_alone_at_original_unmet'])} against combined {fmt(i['combined_unmet'])} (interaction {fmt(i['interaction_unmet'])})."]
    lines += ['', '## Headline cases against the Lyon reference and the declared budget', '', '| Case | all checks | net (Δ vs 1000) | gross (Δ vs 1253) | available (Δ vs 2916) | unmet | turbine K (Δ vs 981.15) | within budget |', '|---|---|---:|---:|---:|---:|---:|---|']
    for n, h in led['headline_against_reference'].items():
        a = h['against_reference']
        within = ', '.join(k for k, r in a.items() if r['within_budget']) or 'none'
        lines.append(f"| {n} | {h['all_checks']} | {fmt(a['net']['model'])} ({fmt(a['net']['difference'])}) | {fmt(a['gross']['model'])} ({fmt(a['gross']['difference'])}) | {fmt(a['available']['model'])} ({fmt(a['available']['difference'])}) | {fmt(a['unmet']['model'])} | {fmt(a['turbine_K']['model'])} ({fmt(a['turbine_K']['difference'])}) | {within} |")
    lines += ['', f"Cases with every scoped check satisfied: {', '.join(led['all_checks_cases']) or 'none'}."]
    return '\n'.join(lines) + '\n'


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
