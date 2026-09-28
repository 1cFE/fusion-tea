"""Reporting arithmetic on native cases only. Never imports a model evaluator."""
import argparse
import json
from pathlib import Path

P = 'aries_integrated_plant__'
CONTRIBUTIONS = ('capital_lcoe', 'om_lcoe', 'tritium_lcoe', 'deuterium_lcoe',
                 'consumables_lcoe', 'imports_lcoe', 'supply_lcoe', 'replacement_lcoe',
                 'other_overhaul_lcoe', 'terminal_lcoe', 'salvage_lcoe', 'lcoe_sum')


def summarize(record):
    read = lambda p: json.loads((record / p).read_text())
    proposals = {r['case']: r for r in read('proposed-points.json')['cases']}
    cases = read('results/cases.json')['cases']
    if len(cases) != len(proposals) or {r['case'] for r in cases} != set(proposals):
        raise ValueError('attempted set differs from declaration')
    rows = []
    for case in cases:
        declared = proposals[case['case']]
        if case['inputs'] != declared['point']:
            raise ValueError('full input map differs: ' + case['case'])
        outputs = case['outputs']
        def get(owner, field, calc='evaluate'):
            key = P + owner + '__' + calc + '__' + field
            return outputs[key] if case['state'] == 'completed' else outputs.get(key)
        support = {k: v for k, v in outputs.items() if 'supported' in k}
        rows.append({'case': case['case'], 'design': declared['design'], 'scenario': declared['arm'],
                     'classification': declared.get('classification', 'declared design'),
                     'axis_values': declared['axis_values'], 'state': case['state'],
                     'inputs': case['inputs'],
                     'service_annual_usd2004': case['inputs'][P + 'finance__supply_service_annual'],
                     'overnight_usd2004': get('cost_ledger', 'overnight'),
                     'unmet_heat_mw': get('heat_exchangers', 'unmet_heat'),
                     'equipment': {branch: {'area_m2': get(branch + '_hx', 'area'),
                                            'ua_mw_k': get(branch + '_hx', 'ua'),
                                            'price_factor': case['inputs'][P + branch + '_hx__price_factor'],
                                            'purchased_quantity_m2': get(branch + '_hx', 'purchased_quantity', 'purchase'),
                                            'capital_usd2004': get(branch + '_hx', 'capital', 'purchase')}
                                   for branch in ('he', 'pbli')},
                     'net_mw': get('plant_ledger', 'net_electric'),
                     'annual_mwh': get('lifecycle_accounts', 'annual_energy'),
                     'gross_makeup_kg_year': get('lifecycle_accounts', 'gross_makeup'),
                     'new_feed_kg_year': get('lifecycle_accounts', 'new_feed'),
                     'external_purchases_kg_year': get('lifecycle_accounts', 'external_shortfall'),
                     'curtailed_feed_kg_year': get('lifecycle_accounts', 'curtailed_feed'),
                     'contributions': {f: get('lifecycle_accounts', f) for f in CONTRIBUTIONS},
                     'verdicts': case['verdicts'], 'support_flags': support,
                     'margins': {k: v for k, v in outputs.items() if 'margin' in k},
                     'passes_evaluated_checks': bool(case['verdicts']) and all(v == 'satisfied' for v in case['verdicts'].values()),
                     'scientific_qualification': 'not established'})
        contributions = rows[-1]['contributions']
        rows[-1]['nonfuel_nonsupply_lcoe_subtotal'] = (sum(v for k, v in contributions.items()
            if k not in ('tritium_lcoe', 'deuterium_lcoe', 'supply_lcoe', 'lcoe_sum'))
            if all(v is not None for v in contributions.values()) else None)
    baselines = {r['scenario']: r for r in rows if r['design'] == 'baseline'}
    for row in rows:
        baseline = baselines[row['scenario']]
        row['matched_baseline_deltas'] = {k: row[k] - baseline[k]
            if row[k] is not None and baseline[k] is not None else None
            for k in ('net_mw', 'annual_mwh', 'gross_makeup_kg_year', 'external_purchases_kg_year',
                      'overnight_usd2004', 'nonfuel_nonsupply_lcoe_subtotal')}
        row['matched_baseline_deltas']['contributions'] = {k: v - baseline['contributions'][k]
            if v is not None and baseline['contributions'][k] is not None else None
            for k, v in row['contributions'].items()}
    pairs = []
    for design in dict.fromkeys(r['design'] for r in rows):
        pair = {r['scenario']: r for r in rows if r['design'] == design}
        if set(pair) != {'no-credit', 'feed100-service30m'}:
            raise ValueError('missing paired scenario')
        a, b = pair['no-credit'], pair['feed100-service30m']
        differences = {f: b['contributions'][f] - a['contributions'][f]
                       if a['contributions'][f] is not None and b['contributions'][f] is not None else None
                       for f in CONTRIBUTIONS}
        pairs.append({'design': design, 'feed_minus_no_credit_contributions': differences,
                      'basis': 'Difference of named native contributions at identical physical choices; supplied-fuel scenario effect.'})
    return {'quantity_source': 'results/cases.json native outputs; completed cases require all account fields; unavailable refused-case outputs remain null',
            'axis_definitions': read('axis-plan.json')['axes'] if (record / 'axis-plan.json').exists() else [],
            'cases': rows, 'scenario_differences': pairs}


def plots(summary, destination):
    """Static scientific exports. All marks retain native failure/support status."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    destination.mkdir(exist_ok=False)
    rows = summary['cases']
    scenarios = ('no-credit', 'feed100-service30m')
    colors = dict(zip(scenarios, ('#2166ac', '#b35806')))
    save = lambda fig, name: [fig.savefig(destination / (name + '.' + ext), bbox_inches='tight', dpi=180)
                              for ext in ('png', 'pdf')]
    studied = sorted({k for r in rows for k in r['axis_values']})
    axis_definitions = {a['axis']: a for a in summary['axis_definitions']}
    for axis in studied:
        fig, panels = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
        chosen = [r for r in rows if axis in r['axis_values'] or (r['design'] == 'baseline' and axis in axis_definitions)]
        for row in chosen:
            x = row['axis_values'][axis] if axis in row['axis_values'] else row['inputs'][axis_definitions[axis]['keys'][0]['key']]
            failed = row['state'] != 'completed' or not row['passes_evaluated_checks']
            kwargs = {'color': colors[row['scenario']]} if failed else {'edgecolors': colors[row['scenario']], 'facecolors': 'none'}
            for ax, value in zip(panels, (row['contributions']['lcoe_sum'], row['net_mw'], row['external_purchases_kg_year'])):
                if value is not None:
                    ax.scatter(x, value, marker='x' if failed else 'o', **kwargs)
        for ax, label in zip(panels, ('LCOE (USD2004/MWh)', 'Net electricity (MW)', 'External T (kg/calendar year)')):
            ax.set_ylabel(label)
            ax.grid(alpha=.2)
        panels[-1].set_xlabel(axis + ' (' + axis_definitions.get(axis, {}).get('units', 'declared units') + ')')
        fig.suptitle(axis + ': blue no credit / orange feed100; crosses evaluated failures.\nOpen marks: scientific qualification absent. Density is an operating diagnostic.')
        fig.tight_layout()
        save(fig, 'axis-' + axis)
        plt.close(fig)
    # No interpolation across adverse points or different physical configurations.
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fields = [('net_mw', 'Net electricity (MW)'), ('gross_makeup_kg_year', 'Gross makeup (kg/calendar year)'),
              ('external_purchases_kg_year', 'External purchases (kg/calendar year)'),
              ('overnight_usd2004', 'Purchased overnight capital (USD2004)')]
    for ax, (field, label) in zip(axes.flat, fields):
        for row in rows:
            if row[field] is None or row['contributions']['lcoe_sum'] is None:
                continue
            failed = row['state'] != 'completed' or not row['passes_evaluated_checks']
            marker = 'x' if failed else 's' if row['classification'] == 'preserved source control' else 'o'
            kwargs = {'color': colors[row['scenario']]} if failed else {'edgecolors': colors[row['scenario']], 'facecolors': 'none'}
            ax.scatter(row[field], row['contributions']['lcoe_sum'], marker=marker, **kwargs)
        ax.set(xlabel=label, ylabel='Conditional LCOE (USD2004/MWh)')
        ax.grid(alpha=.2)
    fig.suptitle('Blue: no credit; orange: feed100/service30m. Cross: evaluated failure.\nOpen circle: passes evaluated checks; square: source control. Scientific qualification absent for all.')
    fig.tight_layout()
    save(fig, 'power-fuel-capital')
    plt.close(fig)
    for scenario in scenarios:
        selected = [r for r in rows if r['scenario'] == scenario]
        fig, (cost_ax, heat_ax) = plt.subplots(2, 1, figsize=(max(12, len(selected) * .55), 9), sharex=True)
        bottom = [0.] * len(selected)
        for field in CONTRIBUTIONS[:-1]:
            values = [r['contributions'][field] for r in selected]
            if any(v is None for v in values):
                continue
            cost_ax.bar(range(len(selected)), values, bottom=bottom, label=field,
                        hatch='///' if field == 'tritium_lcoe' else None)
            bottom = [b + v for b, v in zip(bottom, values)]
        cost_ax.set(ylabel='USD2004/MWh', title=scenario + ': native contributions; tritium hatched; negative salvage retained')
        cost_ax.legend(ncol=4, fontsize=8)
        heat_ax.bar(range(len(selected)), [r['unmet_heat_mw'] if r['unmet_heat_mw'] is not None else float('nan') for r in selected], color='#b2182b')
        heat_ax.set(ylabel='Native unmet heat (MW)', xticks=range(len(selected)),
                    xticklabels=[r['design'] + (' [FAIL]' if not r['passes_evaluated_checks'] else '') for r in selected])
        heat_ax.tick_params(axis='x', rotation=60)
        fig.suptitle('Conditional accounting: scientific qualification absent for every case; source controls labeled separately')
        fig.tight_layout()
        save(fig, 'contributions-' + scenario)
        plt.close(fig)
    # Margins have differing native units; use separate panels, never normalize into a fabricated common margin.
    keys = sorted({k for r in rows for k in r['margins']})
    for offset in range(0, len(keys), 6):
        subset = keys[offset:offset + 6]
        fig, axes = plt.subplots(len(subset), 1, figsize=(14, 2.4 * len(subset)), squeeze=False)
        for ax, key in zip(axes.flat, subset):
            for i, row in enumerate(rows):
                value = row['margins'].get(key)
                if value is not None:
                    ax.scatter(i, value, marker='o' if row['passes_evaluated_checks'] else 'x', color=colors[row['scenario']])
            ax.axhline(0, color='black', linewidth=.6)
            ax.set_title(key.removeprefix(P), fontsize=9)
            ax.set_ylabel('Native margin')
        axes[-1, 0].set_xticks(range(len(rows)), [r['case'] for r in rows], rotation=90, fontsize=6)
        fig.suptitle('Native evaluated margins; blue no credit / orange feed100. Crosses retain failed checks; scientific qualification absent.')
        fig.tight_layout()
        save(fig, 'margins-' + str(offset // 6 + 1))
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--plots-dir', type=Path)
    args = parser.parse_args()
    result = summarize(args.record)
    with args.out.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    if args.plots_dir:
        plots(result, args.plots_dir)


if __name__ == '__main__':
    main()
