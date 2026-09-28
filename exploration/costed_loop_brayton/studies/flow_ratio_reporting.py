"""Readout of study 20260926-design-study-parameters from its stored results (goal design-study-parameters). Reads
results/cases.json, oracle-window-scan.json and axis-plan.json; writes results/readout.json and results/readout.md.
Presentation arithmetic only (deltas against the starting point, bands, rankings); no plant arithmetic, nothing optimized.

Run from the repository root: flow_ratio_reporting.py <record-dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

P = 'costed_loop_brayton__plant__'
START = 'ir-f2500-r1.5183'
MATERIAL_NET_MW = 5.0       # contract § 9
MATERIAL_LCOE_FRACTION = 0.01
CONTRIB = ['capital', 'om', 'tritium', 'deuterium', 'consumables', 'imports', 'supply', 'replacement', 'other_overhaul', 'terminal', 'salvage']
MARGINS = {'compressor': 'compressor_capacity__evaluate__margin', 'turbine': 'turbine_capacity__evaluate__margin',
           'generator': 'generator_capacity__evaluate__margin', 'rejection': 'rejection_capacity__evaluate__margin',
           'he_duty': 'he_capacity__evaluate__margin', 'loop': 'primary_loop__evaluate__capacity_margin',
           'fuel_stock': 'fuel_inventory__screen__margin'}
PURCHASES = {'compressor': 'compressor_equipment__purchase__capital', 'turbine': 'turbine_equipment__purchase__capital',
             'generator': 'generator_equipment__purchase__capital', 'heat_rejection': 'heat_rejection_equipment__purchase__capital',
             'he_duty': 'he_duty_equipment__purchase__capital', 'exchanger': 'he_hx__purchase__capital',
             'conversion_services': 'conversion_services__purchase__cost'}


def local(cid):
    return cid.split('__plant__')[1].rsplit('__', 1)[0]


def row(c):
    o = lambda n: c['outputs'][P + n]
    lcoe = o('lifecycle_price__evaluate__lcoe')
    contrib = {k: o(f'lifecycle_accounts__evaluate__{k}_lcoe') for k in CONTRIB}
    failed = sorted(local(cid) for cid, v in c['verdicts'].items() if v != 'satisfied')
    return {'case': c['case'], 'candidate': c['candidate_id'], 'arm': c['case'].split('-')[0] if c['case'].startswith(('ir-', 'ia-')) else 'sensitivity',
            'flow': c['inputs'][P + 'cycle__selected_flow'], 'ratio': c['inputs'][P + 'compressor_1__selected_ratio'],
            'net': o('electrical__evaluate__net_electric'), 'gross': o('electrical__evaluate__gross_electric'),
            'auxiliary': o('electrical__evaluate__auxiliary_electric'), 'unmet': o('heat_exchangers__evaluate__unmet_heat'),
            'accepted_heat': o('heat_exchangers__evaluate__accepted_heat'), 'turbine_inlet_K': o('heat_exchangers__evaluate__turbine_temperature'),
            'heater_inlet_K': o('heat_exchangers__evaluate__heater_inlet'), 'he_hot_bound_margin_K': o('heat_exchangers__evaluate__he_hot_bound_margin'),
            'compressor_demand': sum(o(f'compressor_{i}__evaluate__shaft_demand') for i in (1, 2, 3)),
            'turbine_work': o('turbine__evaluate__shaft_produced'), 'rejected_heat': o('rejection_capacity__rejected_heat__rejected_heat'),
            'bypass_active': o('recuperator__evaluate__bypass_active'), 'margins': {k: o(v) for k, v in MARGINS.items()},
            'passing': not failed, 'failed_checks': failed,
            'annual_energy_mwh': o('lifecycle_accounts__evaluate__annual_energy'), 'overnight': o('cost_ledger__evaluate__overnight'),
            'direct': o('cost_ledger__evaluate__direct'), 'priced_total': o('priced_equipment__evaluate__total'),
            'purchases': {k: o(v) for k, v in PURCHASES.items()},
            'extrapolated': {k: o(v.replace('__capital', '__extrapolated')) for k, v in PURCHASES.items() if v.endswith('__capital')},
            'tritium_annual_kg': o('lifecycle_accounts__evaluate__gross_makeup'),
            'lcoe': lcoe, 'contributions': contrib, 'plant_side_lcoe': lcoe - contrib['tritium'] - contrib['deuterium'] - contrib['supply']}


def with_deltas(r, base):
    d = dict(r)
    d['d_net'] = r['net'] - base['net']
    d['d_lcoe'] = r['lcoe'] - base['lcoe']
    d['d_plant_side_lcoe'] = r['plant_side_lcoe'] - base['plant_side_lcoe']
    d['d_contributions'] = {k: r['contributions'][k] - base['contributions'][k] for k in CONTRIB}
    d['d_lcoe_material'] = abs(d['d_lcoe']) >= MATERIAL_LCOE_FRACTION * base['lcoe']
    d['d_net_material'] = abs(d['d_net']) >= MATERIAL_NET_MW
    return d


def bands(rows, scan_refused, flows, ratios):
    out = []
    for f in flows:
        col = {r['ratio']: r for r in rows if r['flow'] == f}
        refused = {rt: e for (fl, rt), e in scan_refused.items() if fl == f}
        status = []
        for rt in ratios:
            if rt in col:
                r = col[rt]
                status.append({'ratio': rt, 'status': 'pass' if r['passing'] else 'fail', 'failed_checks': r['failed_checks'], 'net': r['net'], 'unmet': r['unmet']})
            else:
                status.append({'ratio': rt, 'status': 'refused', 'error': refused.get(rt)})
        passing = [s['ratio'] for s in status if s['status'] == 'pass']
        entry = {'flow': f, 'ratios': status, 'passing_ratios': passing}
        if passing:
            lo, hi = min(passing), max(passing)
            below = [s for s in status if s['ratio'] < lo]
            above = [s for s in status if s['ratio'] > hi]
            entry['lower_edge'] = {'lowest_passing_ratio': lo, 'next_below': below[-1] if below else None}
            entry['upper_edge'] = {'highest_passing_ratio': hi, 'next_above': above[0] if above else None}
            entry['best_passing'] = max((s for s in status if s['status'] == 'pass'), key=lambda s: s['net'])
        out.append(entry)
    return out


def main(record):
    record = Path(record)
    cases = json.load(open(record / 'results/cases.json'))['cases']
    scan = json.load(open(record / 'oracle-window-scan.json'))
    plan = json.load(open(record / 'axis-plan.json'))
    rows = {c['case']: row(c) for c in cases}
    base = rows[START]
    rows = {k: with_deltas(r, base) for k, r in rows.items()}
    flows, ratios = plan['grid']['flows'], plan['grid']['ratios']
    refused = {}
    for s in scan['cases']:
        if s['status'] == 'refused':
            refused[(s['arm'], s['axis_values']['cycle_flow'], s['axis_values']['stage_ratio'])] = s['error']
    ir = [r for r in rows.values() if r['arm'] == 'ir']
    ia = [r for r in rows.values() if r['arm'] == 'ia']
    sens = [r for r in rows.values() if r['arm'] == 'sensitivity']
    ir_pass = sorted([r for r in ir if r['passing']], key=lambda r: -r['net'])
    best_net = ir_pass[0]['net']
    best_band = [r for r in ir_pass if best_net - r['net'] < MATERIAL_NET_MW]
    elec_best = max(ir, key=lambda r: r['net'])
    ir_bands = bands(ir, {(f, rt): e for (a, f, rt), e in refused.items() if a == 'ir'}, flows, ratios)
    ia_bands = bands(ia, {(f, rt): e for (a, f, rt), e in refused.items() if a == 'ia'}, flows, ratios)
    from collections import Counter
    ia_sets = Counter(tuple(r['failed_checks']) for r in ia)
    # sensitivities grouped by level and anchor
    anchors = plan['anchors']['points']
    sens_table = []
    for r in sorted(sens, key=lambda r: r['case']):
        level = r['case'].rsplit('-f', 1)[0]
        anchor_case = f"ir-f{r['flow']:g}-r{r['ratio']:.4f}"
        anchor = rows[anchor_case]
        labels = [k for k, v in anchors.items() if v[0] == r['flow'] and abs(v[1] - r['ratio']) < 1e-12]
        sens_table.append({'case': r['case'], 'level': level, 'sensitivity': level.split('-')[0].upper(), 'anchor_case': anchor_case,
                           'anchor_labels': labels, 'flow': r['flow'], 'ratio': r['ratio'], 'net': r['net'], 'unmet': r['unmet'],
                           'passing': r['passing'], 'failed_checks': r['failed_checks'], 'lcoe': r['lcoe'], 'plant_side_lcoe': r['plant_side_lcoe'],
                           'anchor_passing': anchor['passing'], 'd_net_vs_anchor': r['net'] - anchor['net'],
                           'd_lcoe_vs_anchor': r['lcoe'] - anchor['lcoe'], 'd_tritium_lcoe_vs_anchor': r['contributions']['tritium'] - anchor['contributions']['tritium'],
                           'd_plant_side_vs_anchor': r['plant_side_lcoe'] - anchor['plant_side_lcoe'], 'overnight': r['overnight']})
    s6_column = sorted([s for s in sens_table if s['level'] == 's6-hx75000' and s['flow'] == 2500.0], key=lambda s: s['ratio'])
    key_cases = [START] + [r['case'] for r in best_band] + ['ir-f2500-r1.4500', 'ia-f2500-r1.5183', 'ia-f2250-r1.5183', 's5-feed100-f2500-r1.5183', 's6-hx75000-f2500-r1.4000']
    key_cases = [k for i, k in enumerate(key_cases) if k in rows and k not in key_cases[:i]]
    readout = {
        'study_id': record.name, 'starting_point': START, 'materiality': {'net_mw': MATERIAL_NET_MW, 'lcoe_fraction': MATERIAL_LCOE_FRACTION},
        'counts': {'stored': len(rows), 'ir': len(ir), 'ia': len(ia), 'sensitivity': len(sens), 'ir_passing': len(ir_pass), 'ia_passing': sum(r['passing'] for r in ia),
                   'refused_by_scan': len(refused)},
        'best_passing_band': [r['case'] for r in best_band], 'best_passing': best_band[0]['case'], 'electricity_only_best': elec_best['case'],
        'ir_bands': ir_bands, 'ia_bands': ia_bands, 'ia_failed_sets': [{'checks': list(k), 'count': v} for k, v in ia_sets.most_common()],
        'anchors': anchors, 'sensitivities': sens_table, 's6_column_2500': s6_column, 'key_cases': key_cases,
        'refused': [{'arm': a, 'flow': f, 'ratio': rt, 'error': e} for (a, f, rt), e in sorted(refused.items())],
        'rows': rows}
    (record / 'results/readout.json').write_text(json.dumps(readout, indent=1, allow_nan=False) + '\n')
    write_md(record, readout)
    print(json.dumps({'stored': len(rows), 'ir_passing': len(ir_pass), 'best_band': readout['best_passing_band'], 'electricity_only_best': elec_best['case'],
                      'refused': len(refused)}))


def write_md(record, ro):
    rows = ro['rows']
    L = []
    L.append(f"# Readout: {ro['study_id']}\n")
    L.append(f"Presentation of stored channels (`results/cases.json`), one row per stored case; deltas against the starting point `{START}`. USD2004; no-credit fuel convention unless the case says otherwise. Materiality (contract § 9): net {MATERIAL_NET_MW} MW, LCOE {MATERIAL_LCOE_FRACTION:.0%} of the base.\n")
    b = rows[START]
    L.append("## 1. Starting point\n")
    L.append(f"`{START}`: net {b['net']:.3f} MW (gross {b['gross']:.3f}, auxiliaries {b['auxiliary']:.3f}), unmet heat {b['unmet']:.3f} MW, turbine inlet {b['turbine_inlet_K']:.2f} K, heater inlet {b['heater_inlet_K']:.2f} K, compressor demand {b['compressor_demand']:.2f} MW, annual energy {b['annual_energy_mwh']:,.0f} MWh, overnight {b['overnight']:,.2f}, LCOE {b['lcoe']:.3f} USD/MWh (plant-side {b['plant_side_lcoe']:.3f}; tritium {b['contributions']['tritium']:.3f}), all checks satisfied.\n")
    L.append("## 2. Best passing and electricity-only best (inventory I-R)\n")
    L.append("| Case | Net MW | Δnet | Unmet MW | Failed checks | LCOE | ΔLCOE | Plant-side LCOE | Δplant-side |\n|---|---|---|---|---|---|---|---|---|")
    for k in ro['best_passing_band'] + [ro['electricity_only_best'], 'ir-f2500-r1.4500']:
        r = rows[k]
        L.append(f"| `{k}` | {r['net']:.3f} | {r['d_net']:+.3f} | {r['unmet']:.3f} | {', '.join(r['failed_checks']) or 'none'} | {r['lcoe']:.3f} | {r['d_lcoe']:+.3f} | {r['plant_side_lcoe']:.3f} | {r['d_plant_side_lcoe']:+.3f} |")
    L.append("")
    L.append("## 3. Passing band per flow (I-R)\n")
    L.append("| Flow kg/s | Passing ratios | Lower edge (below it) | Upper edge (above it) | Best passing net MW |\n|---|---|---|---|---|")
    for e in ro['ir_bands']:
        if e['passing_ratios']:
            nb, na = e['lower_edge']['next_below'], e['upper_edge']['next_above']
            below = f"{nb['ratio']:.4f}: {nb['status']}{' ' + ', '.join(nb.get('failed_checks', [])) if nb.get('failed_checks') else ''}{(' unmet %.1f MW' % nb['unmet']) if nb.get('unmet') else ''}" if nb else 'grid edge'
            above = f"{na['ratio']:.4f}: {na['status']}{' ' + ', '.join(na.get('failed_checks', [])) if na.get('failed_checks') else ''}" if na else 'grid edge'
            L.append(f"| {e['flow']:g} | {', '.join(f'{x:.4f}' for x in e['passing_ratios'])} | {below} | {above} | {e['best_passing']['net']:.3f} at {e['best_passing']['ratio']:.4f} |")
        else:
            L.append(f"| {e['flow']:g} | none | | | |")
    L.append("")
    L.append("## 4. Inventory I-A (ARIES-selected ratings) at the same points\n")
    L.append(f"Passing points: {ro['counts']['ia_passing']} of {ro['counts']['ia']}. Violated-screen sets: " + '; '.join(f"{{{', '.join(s['checks'])}}} × {s['count']}" for s in ro['ia_failed_sets']) + ".\n")
    L.append("## 5. Sensitivities at the anchors\n")
    L.append("| Case | Anchor | Anchor passes | Net MW | Δnet vs anchor | Unmet MW | Passes | Failed checks | LCOE | ΔLCOE vs anchor | Δtritium LCOE | Δplant-side |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s in ro['sensitivities']:
        L.append(f"| `{s['case']}` | {','.join(s['anchor_labels']) or 'column'} | {'yes' if s['anchor_passing'] else 'no'} | {s['net']:.3f} | {s['d_net_vs_anchor']:+.3f} | {s['unmet']:.3f} | {'yes' if s['passing'] else 'no'} | {', '.join(s['failed_checks']) or 'none'} | {s['lcoe']:.3f} | {s['d_lcoe_vs_anchor']:+.3f} | {s['d_tritium_lcoe_vs_anchor']:+.3f} | {s['d_plant_side_vs_anchor']:+.3f} |")
    L.append("")
    L.append("## 6. Contributions at the key cases (USD/MWh)\n")
    L.append("| Case | Net MW | " + ' | '.join(CONTRIB) + " | LCOE | Overnight |\n|---|---|" + '---|' * len(CONTRIB) + "---|---|")
    for k in ro['key_cases']:
        r = rows[k]
        L.append(f"| `{k}` | {r['net']:.3f} | " + ' | '.join(f"{r['contributions'][c]:.3f}" for c in CONTRIB) + f" | {r['lcoe']:.3f} | {r['overnight']:,.0f} |")
    L.append("")
    L.append("## 7. Refused by the oracle scan (never stored)\n")
    L.append("| Arm | Flow | Ratio | Guard |\n|---|---|---|---|")
    for x in ro['refused']:
        L.append(f"| {x['arm']} | {x['flow']:g} | {x['ratio']:.4f} | {x['error']} |")
    L.append("")
    L.append("## 8. Every stored grid case\n")
    L.append("| Case | Net MW | Δnet | Unmet MW | Turbine inlet K | Heater inlet K | Compressor MW | Failed checks | LCOE | ΔLCOE |\n|---|---|---|---|---|---|---|---|---|---|")
    for k in sorted(rows):
        r = rows[k]
        if r['arm'] == 'sensitivity':
            continue
        L.append(f"| `{k}` | {r['net']:.3f} | {r['d_net']:+.3f} | {r['unmet']:.3f} | {r['turbine_inlet_K']:.2f} | {r['heater_inlet_K']:.2f} | {r['compressor_demand']:.1f} | {', '.join(r['failed_checks']) or 'none'} | {r['lcoe']:.3f} | {r['d_lcoe']:+.3f} |")
    (record / 'results/readout.md').write_text('\n'.join(L) + '\n')


if __name__ == '__main__':
    main(sys.argv[1])
