"""Presentation-only ledger for the reconciled-alternative economics study; reads native cases only.

Every number is selected from results/cases.json (or, for a dry run, from the oracle scan's values);
differences are arithmetic on native quantities and never replace a model output. Materiality
lines are copied from the goal's evidence/comparison-basis.md § 3 (declared before execution).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

P = 'aries_integrated_plant__'
L = P + 'lifecycle_accounts__evaluate__'
SL = P + 'source_lifecycle_accounts__evaluate__'
CONTRIB = ['capital', 'om', 'tritium', 'supply', 'deuterium', 'consumables', 'replacement', 'other_overhaul', 'terminal', 'salvage', 'imports']
CH = {
    'net': P + 'plant_ledger__evaluate__net_electric', 'gross': P + 'plant_ledger__evaluate__gross_electric', 'unmet': P + 'heat_exchangers__evaluate__unmet_heat',
    'annual_mwh': L + 'annual_energy', 'direct': P + 'cost_ledger__evaluate__direct', 'overnight': P + 'cost_ledger__evaluate__overnight', 'idc': L + 'idc', 'financed': L + 'financed_capital',
    'annual_operating': P + 'cost_ledger__evaluate__annual_operating', 'annual_om': P + 'annual_om__evaluate__annual_om', 'tritium_cost': P + 'fuel_inventory__annual__annual_cost', 'deuterium_cost': P + 'fuel_inventory__deuterium__annual_fuel',
    'gross_makeup': L + 'gross_makeup', 'new_feed': L + 'new_feed', 'external_kg': L + 'external_shortfall', 'curtailed': L + 'curtailed_feed',
    'event_count': P + 'replacement__evaluate__event_count', 'event_cost': P + 'replacement__evaluate__event_cost', 'lifetime_replacement': P + 'replacement__evaluate__lifetime_total', 'pv_replacement': L + 'pv_replacement',
    'overhaul': L + 'other_overhaul_cost', 'gross_terminal': L + 'gross_terminal', 'salvage': L + 'salvage', 'pv_total': L + 'pv_total_cost', 'pv_energy': L + 'pv_energy',
    'lcoe': P + 'lifecycle_price__evaluate__lcoe', 'branch_lcoe': P + 'source_lifecycle_price__evaluate__lcoe', 'branch_annual_mwh': SL + 'annual_energy', 'branch_financed': SL + 'financed_capital',
    'compressor_margin': P + 'compressor_capacity__evaluate__margin', 'compressor_purchase': P + 'compressor_equipment__purchase__capital',
}
CH.update({f'lcoe_{c}': L + c + '_lcoe' for c in CONTRIB})
CH.update({f'branch_lcoe_{c}': SL + c + '_lcoe' for c in CONTRIB})
PUBLISHED = {'lcoe': 77.6, 'net': 1000.0, 'annual_mwh': 7446000.0, 'direct_musd': 2619.572, 'inclusive_musd': 5055.77396}
MATERIAL = {'lcoe_reported_not_separated': 0.1, 'lcoe_material_aligned': 1.0, 'lcoe_material_fraction': 0.01, 'overnight_material': 1e7}
SCENARIOS = ['alt-canonical-no-credit', 'alt-canonical-feed100', 'alt-unscaled-no-credit', 'alt-unscaled-feed100', 'baseline-no-credit', 'baseline-feed100', 'original-source-assumed-no-credit']
LADDER_FEED = ['alt-canonical-feed100', 'diag-L3-om-source-derived-feed100', 'diag-L34-cumulative-om-life47-feed100', 'diag-L345-cumulative-om-life47-cadence-feed100', 'diag-L7-aligned-combined-at-1000']
ONE_AT_A_TIME = [('diag-L3-om-source-derived-feed100', 'alt-canonical-feed100'), ('diag-L4-life-47y-feed100', 'alt-canonical-feed100'), ('diag-L5-source-cadence-40y-feed100', 'alt-canonical-feed100'), ('diag-L5-source-cadence-47y-feed100', 'diag-L4-life-47y-feed100'), ('diag-L6-fuel-self-sufficient', 'alt-canonical-no-credit')]
LADDER_COMBINED = ['alt-canonical-no-credit', 'diag-L6-fuel-self-sufficient', 'diag-L7-aligned-combined-at-our-net', 'diag-L8-aligned-discount-0.00', 'diag-L8-aligned-discount-0.03', 'diag-L8-aligned-discount-0.08', 'diag-L8-aligned-discount-0.10']
BRANCH_AT_OUR_NET = ['diag-L1-source-capital-at-our-net-no-credit', 'diag-L1-source-capital-at-our-net-feed100', 'diag-L7-aligned-combined-at-our-net']


def load(path: Path):
    doc = json.loads(path.read_text())
    out = {}
    for row in doc['cases']:
        values = row.get('outputs') or row.get('values')
        if values is None:
            continue
        rec = {k: float(values[c]) for k, c in CH.items() if c in values}
        rec['verdicts'] = row.get('verdicts', {})
        rec['inputs'] = row.get('inputs') or row.get('point') or {}
        out[row['case']] = rec
    return out


def checks(c):
    v = c.get('verdicts') or {}
    return {'all': bool(v) and all(x == 'satisfied' for x in v.values()), 'failed': sorted(k.split('__')[1] + '/' + k.split('__')[2] for k, x in v.items() if x != 'satisfied')}


def scenario_rows(cases):
    rows = {}
    for name in SCENARIOS:
        if name not in cases:
            continue
        c = cases[name]
        rows[name] = {k: c.get(k) for k in ('net', 'gross', 'unmet', 'annual_mwh', 'direct', 'overnight', 'idc', 'financed', 'annual_operating', 'annual_om', 'tritium_cost', 'deuterium_cost', 'gross_makeup', 'new_feed', 'external_kg', 'curtailed', 'event_count', 'event_cost', 'lifetime_replacement', 'pv_replacement', 'overhaul', 'gross_terminal', 'salvage', 'pv_total', 'pv_energy', 'lcoe', 'branch_lcoe', 'compressor_margin', 'compressor_purchase')}
        rows[name]['contributions'] = {k: c.get(f'lcoe_{k}') for k in CONTRIB}
        rows[name]['branch_contributions'] = {k: c.get(f'branch_lcoe_{k}') for k in CONTRIB}
        rows[name]['checks'] = checks(c)
    return rows


def attribution_by_contribution(cases, a, b):
    """Exact decomposition of LCOE(b) - LCOE(a) by contribution (contributions sum to the total)."""
    ca, cb = cases[a], cases[b]
    parts = {k: cb.get(f'lcoe_{k}', 0.0) - ca.get(f'lcoe_{k}', 0.0) for k in CONTRIB}
    return {'from': a, 'to': b, 'lcoe_from': ca['lcoe'], 'lcoe_to': cb['lcoe'], 'delta': cb['lcoe'] - ca['lcoe'], 'by_contribution': parts, 'sum_of_parts': sum(parts.values()),
            'net_from': ca['net'], 'net_to': cb['net'], 'overnight_from': ca['overnight'], 'overnight_to': cb['overnight']}


def ladder(cases):
    steps = []
    prev = None
    for name in LADDER_FEED + LADDER_COMBINED:
        if name not in cases:
            continue
        c = cases[name]
        row = {'case': name, 'lcoe_ours': c['lcoe'], 'lcoe_branch': c.get('branch_lcoe'), 'branch_annual_mwh': c.get('branch_annual_mwh'), 'annual_mwh': c['annual_mwh'], 'net': c['net'], 'overnight': c['overnight'], 'financed': c['financed'], 'event_count': c.get('event_count'), 'external_kg': c.get('external_kg'), 'checks': checks(c),
               'gap_ours_vs_published': c['lcoe'] - PUBLISHED['lcoe'], 'gap_branch_vs_published': (c.get('branch_lcoe') - PUBLISHED['lcoe']) if c.get('branch_lcoe') is not None else None}
        if prev is not None and name in LADDER_FEED:
            row['step_from'] = prev; row['step_delta_ours'] = c['lcoe'] - cases[prev]['lcoe']
        steps.append(row); prev = name if name in LADDER_FEED else prev
    # interaction: sum of single steps L3, L4, L5 vs L4+L5 combined (feed100 chain)
    inter = None
    if all(n in cases for n in ('alt-canonical-feed100', 'diag-L4-life-47y-feed100', 'diag-L5-source-cadence-40y-feed100', 'diag-L5-source-cadence-47y-feed100')):
        b = cases['alt-canonical-feed100']['lcoe']
        d4 = cases['diag-L4-life-47y-feed100']['lcoe'] - b; d5 = cases['diag-L5-source-cadence-40y-feed100']['lcoe'] - b; d45 = cases['diag-L5-source-cadence-47y-feed100']['lcoe'] - b
        inter = {'L4_alone': d4, 'L5_alone': d5, 'sum': d4 + d5, 'combined_L4_L5': d45, 'interaction': d45 - (d4 + d5)}
    combined = None
    if all(n in cases for n in ('alt-canonical-no-credit', 'diag-L6-fuel-self-sufficient', 'diag-L7-aligned-combined-at-1000', 'diag-L3-om-source-derived-feed100', 'alt-canonical-feed100', 'diag-L5-source-cadence-47y-feed100')):
        b0 = cases['alt-canonical-no-credit']['lcoe']
        d6 = cases['diag-L6-fuel-self-sufficient']['lcoe'] - b0
        bf = cases['alt-canonical-feed100']['lcoe']
        d3 = cases['diag-L3-om-source-derived-feed100']['lcoe'] - bf
        d45 = cases['diag-L5-source-cadence-47y-feed100']['lcoe'] - bf
        d7 = cases['diag-L7-aligned-combined-at-1000']['lcoe'] - b0
        combined = {'from_no_credit_L6_fuel': d6, 'L3_om_on_feed100': d3, 'L4_L5_on_feed100': d45, 'sum_L6_plus_L3_plus_L45': d6 + d3 + d45, 'combined_L7_from_no_credit': d7, 'interaction': d7 - (d6 + d3 + d45)}
    branch = {n: {'lcoe_branch_at_our_net': cases[n].get('branch_lcoe'), 'lcoe_ours': cases[n]['lcoe'], 'capital_scope_effect': cases[n].get('branch_lcoe') - cases[n]['lcoe'] if cases[n].get('branch_lcoe') is not None else None} for n in BRANCH_AT_OUR_NET if n in cases}
    for n, base in (('alt-canonical-no-credit', 'diag-L1-source-capital-at-our-net-no-credit'), ('alt-canonical-feed100', 'diag-L1-source-capital-at-our-net-feed100'), ('diag-L7-aligned-combined-at-1000', 'diag-L7-aligned-combined-at-our-net')):
        if n in cases and base in cases:
            branch[base]['lcoe_branch_at_1000'] = cases[n].get('branch_lcoe'); branch[base]['denominator_effect_at_source_capital'] = cases[n].get('branch_lcoe') - cases[base].get('branch_lcoe')
    one = [{'case': n, 'base': b, 'lcoe_base': cases[b]['lcoe'], 'lcoe': cases[n]['lcoe'], 'delta': cases[n]['lcoe'] - cases[b]['lcoe'], 'branch_lcoe': cases[n].get('branch_lcoe')} for n, b in ONE_AT_A_TIME if n in cases and b in cases]
    return {'steps': steps, 'one_at_a_time': one, 'interaction_L4_L5': inter, 'combined_interaction': combined, 'branch_reads': branch}


def sensitivities(cases):
    rows = []
    for name, c in cases.items():
        if not (name.startswith('sens-') or name.startswith('adverse-') or name.startswith('diag-estimate')):
            continue
        base = 'alt-canonical-no-credit' if name.endswith('no-credit') else 'alt-canonical-feed100'
        b = cases[base]
        rows.append({'case': name, 'base': base, 'lcoe': c['lcoe'], 'delta_lcoe': c['lcoe'] - b['lcoe'], 'relative': (c['lcoe'] - b['lcoe']) / b['lcoe'], 'overnight': c['overnight'], 'delta_overnight': c['overnight'] - b['overnight'], 'net': c['net'], 'delta_net': c['net'] - b['net'], 'external_kg': c.get('external_kg'), 'branch_lcoe': c.get('branch_lcoe'), 'checks': checks(c),
                     'material_independent': abs(c['lcoe'] - b['lcoe']) >= MATERIAL['lcoe_material_fraction'] * b['lcoe']})
    rows.sort(key=lambda r: -abs(r['delta_lcoe']))
    return rows


def fmt(x, nd=3):
    if x is None:
        return '—'
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, float)):
        return f'{x:,.{nd}f}' if abs(x) >= 1e5 else f'{x:.{nd}f}'
    return str(x)


def markdown(led):
    M = ['# Reconciled-alternative economics ledger (presentation only; every number is a native stored channel or arithmetic on two of them)\n']
    M.append(f"Published comparison figure: {PUBLISHED['lcoe']} USD2004/MWh at {PUBLISHED['net']:.0f} MW net, {PUBLISHED['annual_mwh']:,.0f} MWh/year (Lyon 2008 Table VII). Materiality declared before execution: differences below {MATERIAL['lcoe_reported_not_separated']} USD2004/MWh are not separated; ≥ {MATERIAL['lcoe_material_aligned']} USD2004/MWh is material in the aligned comparison; ≥ {MATERIAL['lcoe_material_fraction']:.0%} of the alternative's LCOE is material in the independent assessment; ≥ {MATERIAL['overnight_material']/1e6:.0f} MUSD2004 overnight is material.\n")
    M.append('## A. Scenario results (independent alternative, controls; USD2004)\n')
    heads = ['net MW', 'annual MWh', 'direct', 'overnight', 'IDC', 'financed', 'annual operating', 'O&M', 'external T cost', 'gross makeup kg', 'new feed kg', 'external kg', 'curtailed kg', 'events', 'event cost', 'PV replacements', 'overhaul', 'gross terminal', 'salvage', 'LCOE', 'source-branch LCOE (diagnostic)', 'all checks', 'failed']
    keys = ['net', 'annual_mwh', 'direct', 'overnight', 'idc', 'financed', 'annual_operating', 'annual_om', 'tritium_cost', 'gross_makeup', 'new_feed', 'external_kg', 'curtailed', 'event_count', 'event_cost', 'pv_replacement', 'overhaul', 'gross_terminal', 'salvage', 'lcoe', 'branch_lcoe']
    M.append('| Case | ' + ' | '.join(heads) + ' |'); M.append('|---|' + '---:|' * len(keys) + '---|---|')
    for name, r in led['scenarios'].items():
        M.append(f"| `{name}` | " + ' | '.join(fmt(r[k], 6 if k == 'lcoe' or k == 'branch_lcoe' else 3) for k in keys) + f" | {r['checks']['all']} | {', '.join(r['checks']['failed']) or '—'} |")
    M.append('\n### A2. LCOE contributions (USD2004/MWh)\n')
    M.append('| Case | ' + ' | '.join(CONTRIB) + ' | total |'); M.append('|---|' + '---:|' * (len(CONTRIB) + 1))
    for name, r in led['scenarios'].items():
        M.append(f"| `{name}` | " + ' | '.join(fmt(r['contributions'][k], 6) for k in CONTRIB) + f" | {fmt(r['lcoe'], 6)} |")
    M.append('\n## B. Attribution by contribution (exact: the contributions sum to the total)\n')
    for a in led['attributions']:
        M.append(f"- `{a['from']}` → `{a['to']}`: LCOE {fmt(a['lcoe_from'], 6)} → {fmt(a['lcoe_to'], 6)} (Δ {fmt(a['delta'], 6)}); net {fmt(a['net_from'])} → {fmt(a['net_to'])} MW; overnight {fmt(a['overnight_from'], 2)} → {fmt(a['overnight_to'], 2)}; by contribution: " + ', '.join(f"{k} {fmt(v, 6)}" for k, v in a['by_contribution'].items()) + f"; sum of parts {fmt(a['sum_of_parts'], 6)}.")
    M.append('\n## C. Aligned-convention ladder (every `diag-*` row is a labelled diagnostic substitution; the source branch column supplies 1000 MW and the already-financed 5,055.77 MUSD capital; L3 and every rung inheriting it carry the target-derived O&M)\n')
    M.append('### C0. One-at-a-time steps, each from its named base\n')
    M.append('| Step | base | LCOE base | LCOE | Δ | branch LCOE |'); M.append('|---|---|---:|---:|---:|---:|')
    for o in led['ladder']['one_at_a_time']:
        M.append(f"| `{o['case']}` | `{o['base']}` | {fmt(o['lcoe_base'], 6)} | {fmt(o['lcoe'], 6)} | {fmt(o['delta'], 6)} | {fmt(o['branch_lcoe'], 6)} |")
    M.append('\n### C1. Cumulative chain in the stated order (feed100 → L3 → L3+L4 → L3+L4+L5 → L3+L4+L5+L6 = L7), then the combined reads and every swept discount rate (no rate designated as the published one)\n')
    M.append('| Case | LCOE ours | step Δ (feed100 chain) | source-branch LCOE | ours − 77.6 | branch − 77.6 | net MW | annual MWh | overnight | financed | events | external kg | all checks |'); M.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|')
    for s in led['ladder']['steps']:
        M.append(f"| `{s['case']}` | {fmt(s['lcoe_ours'], 6)} | {fmt(s.get('step_delta_ours'), 6)} | {fmt(s['lcoe_branch'], 6)} | {fmt(s['gap_ours_vs_published'], 3)} | {fmt(s['gap_branch_vs_published'], 3)} | {fmt(s['net'])} | {fmt(s['annual_mwh'], 0)} | {fmt(s['overnight'], 0)} | {fmt(s['financed'], 0)} | {fmt(s['event_count'], 0)} | {fmt(s['external_kg'])} | {s['checks']['all']} |")
    M.append(f"\nInteraction L4 × L5 (feed100 chain): {json.dumps({k: round(v, 6) for k, v in led['ladder']['interaction_L4_L5'].items()}) if led['ladder']['interaction_L4_L5'] else 'n/a'}.")
    M.append(f"\nCombined interaction (from no-credit through L6, L3, L4+L5 to L7): {json.dumps({k: round(v, 6) for k, v in led['ladder']['combined_interaction'].items()}) if led['ladder']['combined_interaction'] else 'n/a'}.")
    M.append('\n### C2. Source-branch reads at our net (capital scope alone) against 1000 MW (capital scope and denominator)\n')
    M.append('| Case | LCOE ours | branch at our net | capital-scope effect | branch at 1000 MW | denominator effect at source capital |'); M.append('|---|---:|---:|---:|---:|---:|')
    for n, b in led['ladder']['branch_reads'].items():
        M.append(f"| `{n}` | {fmt(b['lcoe_ours'], 6)} | {fmt(b['lcoe_branch_at_our_net'], 6)} | {fmt(b['capital_scope_effect'], 6)} | {fmt(b.get('lcoe_branch_at_1000'), 6)} | {fmt(b.get('denominator_effect_at_source_capital'), 6)} |")
    M.append('\n## D. Sensitivities (one at a time on the named base; sorted by |Δ LCOE|)\n')
    M.append('| Case | base | LCOE | Δ LCOE | relative | Δ overnight | Δ net MW | external kg | branch LCOE | material (≥ 1 % of base) | all checks | failed |'); M.append('|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|')
    for r in led['sensitivities']:
        M.append(f"| `{r['case']}` | `{r['base']}` | {fmt(r['lcoe'], 6)} | {fmt(r['delta_lcoe'], 6)} | {r['relative']:+.2%} | {fmt(r['delta_overnight'], 0)} | {fmt(r['delta_net'])} | {fmt(r['external_kg'])} | {fmt(r['branch_lcoe'], 6)} | {r['material_independent']} | {r['checks']['all']} | {', '.join(r['checks']['failed']) or '—'} |")
    return '\n'.join(M) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--dry-run', action='store_true', help='read the oracle scan instead of results/cases.json')
    args = parser.parse_args()
    src = args.record / ('oracle-window-scan.json' if args.dry_run else 'results/cases.json')
    cases = load(src)
    led = {'source': str(src), 'published': PUBLISHED, 'materiality': MATERIAL, 'scenarios': scenario_rows(cases),
           'attributions': [attribution_by_contribution(cases, a, b) for a, b in (('baseline-no-credit', 'alt-canonical-no-credit'), ('baseline-feed100', 'alt-canonical-feed100'), ('alt-unscaled-no-credit', 'alt-canonical-no-credit'), ('alt-canonical-no-credit', 'alt-canonical-feed100')) if a in cases and b in cases],
           'ladder': ladder(cases), 'sensitivities': sensitivities(cases)}
    out_dir = args.record / ('preparation' if args.dry_run else 'results')
    (out_dir / ('attribution-dry-run.json' if args.dry_run else 'attribution.json')).write_text(json.dumps(led, indent=2) + '\n')
    (out_dir / ('attribution-dry-run.md' if args.dry_run else 'attribution.md')).write_text(markdown(led))
    print(json.dumps({'cases': len(cases), 'scenarios': {n: round(r['lcoe'], 6) for n, r in led['scenarios'].items()}, 'ladder_last': [(s['case'], round(s['lcoe_ours'], 3), round(s['lcoe_branch'], 3) if s['lcoe_branch'] is not None else None) for s in led['ladder']['steps'][-4:]], 'top_sens': [(r['case'], round(r['delta_lcoe'], 3)) for r in led['sensitivities'][:6]]}, indent=1))


if __name__ == '__main__':
    main()
