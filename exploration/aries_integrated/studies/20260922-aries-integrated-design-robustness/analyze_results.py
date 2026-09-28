"""Matched OAT comparisons from stored native outputs; no evaluator import."""
from pathlib import Path
import csv
import json
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

R = Path(__file__).resolve().parent
read = lambda name: json.loads((R / name).read_text())
write = lambda name, value: (R / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def analyze():
    accounting = read('results/accounting.json')
    config = read('config.json')
    assert read('results/verification_summary.json')['outcome'] == 'pass'
    rows = accounting['cases']
    assert len(rows) == 174 and all(r['state'] == 'completed' for r in rows)
    metadata = {d['name']: d for d in config['designs']}
    metadata['baseline'] = config['automatic_baseline_metadata']
    for row in rows:
        row.update({k: metadata[row['design']][k] for k in ('physical_design', 'uncertainty_setting')})
    conn = sqlite3.connect('file:' + str(R / 'results/native' / (R.name + '.db')) + '?mode=ro&immutable=1', uri=True)
    attempts = dict(conn.execute('select state,count(*) from attempt_transitions group by state'))
    assert attempts == {'started': 174, 'committed': 174}
    assert conn.execute('select max(attempt_number) from attempt_transitions').fetchone()[0] == 1
    conn.close()
    cases = {(r['physical_design'], r['uncertainty_setting'], r['scenario']): r for r in rows}
    settings = [s['name'] for s in config['uncertainty_settings']]
    designs = ['area45k', 'near-feed-floor', 'high-density-demand']
    scenarios = ['no-credit', 'feed100-service30m']
    comparisons = []
    for scenario in scenarios:
        for setting in settings:
            base = cases['baseline', setting, scenario]
            for design in designs:
                candidate = cases[design, setting, scenario]
                rankable = base['passes_evaluated_checks'] and candidate['passes_evaluated_checks']
                delta = {k: candidate['contributions'][k] - v for k, v in base['contributions'].items()}
                comparisons.append({'physical_design': design, 'uncertainty_setting': setting,
                    'supply_scenario': scenario, 'baseline_case': base['case'], 'candidate_case': candidate['case'],
                    'passes_evaluated_checks_both': rankable,
                    'comparison_status': ('lower conditional LCOE' if delta['lcoe_sum'] < 0 else 'higher conditional LCOE' if delta['lcoe_sum'] > 0 else 'equal conditional LCOE') if rankable else 'not ranked: evaluated failure',
                    'scientific_qualification': 'absent for all designs', 'contribution_deltas': delta,
                    'native_quantity_deltas': {k: candidate[k] - base[k] for k in ('net_mw', 'annual_mwh', 'gross_makeup_kg_year',
                        'external_purchases_kg_year', 'curtailed_feed_kg_year', 'overnight_usd2004', 'nonfuel_nonsupply_lcoe_subtotal')},
                    'baseline_failed_checks': {k: v for k, v in base['verdicts'].items() if v != 'satisfied'},
                    'candidate_failed_checks': {k: v for k, v in candidate['verdicts'].items() if v != 'satisfied'}})
    write('results/matched-comparisons.json', {'basis': 'Same uncertainty setting and fixed supply scenario; native contribution differences only.',
        'attempts': attempts, 'comparisons': comparisons, 'cases': rows})
    fields = ['case', 'physical_design', 'uncertainty_setting', 'scenario', 'net_mw', 'annual_mwh', 'gross_makeup_kg_year',
              'new_feed_kg_year', 'service_annual_usd2004', 'external_purchases_kg_year', 'curtailed_feed_kg_year',
              'overnight_usd2004', 'unmet_heat_mw', 'nonfuel_nonsupply_lcoe_subtotal', 'passes_evaluated_checks', 'scientific_qualification']
    contributions = list(rows[0]['contributions'])
    equipment = [branch + '_' + field for branch in ('he', 'pbli') for field in ('area_m2', 'ua_mw_k', 'price_factor', 'purchased_quantity_m2', 'capital_usd2004')]
    with (R / 'results/all-case-accounting.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields + contributions + equipment + ['failed_checks', 'support_flags'])
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r[k] for k in fields} | r['contributions'] |
                {branch + '_' + field: value for branch, values in r['equipment'].items() for field, value in values.items()} |
                {'failed_checks': json.dumps({k: v for k, v in r['verdicts'].items() if v != 'satisfied'}), 'support_flags': json.dumps(r['support_flags'])})
    (R / 'plots').mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(15, 12), constrained_layout=True)
    for ax, scenario in zip(axes, scenarios):
        matrix = np.full((len(settings), len(designs)), np.nan)
        selected = {(c['uncertainty_setting'], c['physical_design']): c for c in comparisons if c['supply_scenario'] == scenario}
        for i, setting in enumerate(settings):
            for j, design in enumerate(designs):
                c = selected[setting, design]
                if c['passes_evaluated_checks_both']:
                    matrix[i, j] = c['contribution_deltas']['lcoe_sum']
        limit = float(np.nanmax(np.abs(matrix)))
        cmap = plt.colormaps['RdBu_r'].copy()
        cmap.set_bad('#bbbbbb')
        im = ax.imshow(matrix, aspect='auto', cmap=cmap, vmin=-limit, vmax=limit)
        for i in range(len(settings)):
            for j in range(len(designs)):
                value = matrix[i, j]
                ax.text(j, i, 'FAIL' if np.isnan(value) else f'{value:+.2f}', ha='center', va='center', fontsize=8,
                        bbox={'facecolor': 'white', 'alpha': .65, 'pad': 1})
        ax.set(xticks=range(3), xticklabels=designs, yticks=range(len(settings)), yticklabels=settings, title=scenario)
        ax.tick_params(axis='x', rotation=20)
        fig.colorbar(im, ax=ax, shrink=.6, label='Candidate minus matched baseline (USD2004/MWh)')
    fig.suptitle('Matched OAT conditional LCOE differences: same uncertainty and supply in each comparison.\nGray FAIL: either point fails evaluated checks and is not ranked. Scientific qualification absent throughout.')
    for ext in ('png', 'pdf'):
        fig.savefig(R / 'plots' / ('matched-uncertainty-differences.' + ext), dpi=180)
    plt.close(fig)
    defaults = [cases[design, 'default', scenario] for scenario in scenarios
                for design in ['baseline'] + designs]
    fig, axes = plt.subplots(3, 1, figsize=(13, 12), sharex=True, constrained_layout=True)
    bottom = [0.] * len(defaults)
    for component in [k for k in defaults[0]['contributions'] if k != 'lcoe_sum']:
        values = [r['contributions'][component] for r in defaults]
        axes[0].bar(range(len(defaults)), values, bottom=bottom, label=component,
                    hatch='///' if component == 'tritium_lcoe' else None)
        bottom = [a + b for a, b in zip(bottom, values)]
    axes[0].set_ylabel('Native contributions (USD2004/MWh)')
    axes[0].legend(ncol=4, fontsize=8)
    axes[1].bar(range(len(defaults)), [r['net_mw'] for r in defaults], color='#2166ac')
    axes[1].set_ylabel('Net electricity (MW)')
    positions = np.arange(len(defaults))
    axes[2].bar(positions-.2, [r['gross_makeup_kg_year'] for r in defaults], width=.4, label='Gross new makeup')
    axes[2].bar(positions+.2, [r['external_purchases_kg_year'] for r in defaults], width=.4, label='External purchases')
    axes[2].set_ylabel('Tritium (kg/calendar year)')
    axes[2].set_xticks(positions, [r['physical_design']+'\n'+r['scenario'] for r in defaults], rotation=30)
    axes[2].legend()
    fig.suptitle('Fixed physical designs at default assumptions; both supply scenarios.\nAll shown points pass evaluated checks; scientific qualification absent. All 174 cases retained in CSV/JSON.')
    for ext in ('png', 'pdf'):
        fig.savefig(R / 'plots' / ('default-design-accounting.' + ext), dpi=180)
    plt.close(fig)
    findings = {}
    for scenario in scenarios:
        for design in designs:
            selected = [c for c in comparisons if c['supply_scenario'] == scenario and c['physical_design'] == design]
            good = [c for c in selected if c['passes_evaluated_checks_both']]
            findings[scenario + '/' + design] = {
                'rankable': len(good), 'not_ranked': len(selected)-len(good),
                'lower': [c['uncertainty_setting'] for c in good if c['contribution_deltas']['lcoe_sum'] < 0],
                'higher': [c['uncertainty_setting'] for c in good if c['contribution_deltas']['lcoe_sum'] > 0],
                'delta_range': [min(c['contribution_deltas']['lcoe_sum'] for c in good), max(c['contribution_deltas']['lcoe_sum'] for c in good)] if good else None}
    write('results/robustness-findings.json', {'cases': len(rows), 'passes_evaluated_checks': sum(r['passes_evaluated_checks'] for r in rows),
        'comparisons': len(comparisons), 'rankable_comparisons': sum(c['passes_evaluated_checks_both'] for c in comparisons),
        'findings': findings, 'limits': 'Engineered OAT windows only; no joint uncertainty coverage or probability.'})
    adverse = [r for r in rows if not r['passes_evaluated_checks']]
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    axes[0].scatter(range(len(adverse)), [r['contributions']['lcoe_sum'] for r in adverse], marker='x', color='#b2182b')
    axes[0].set_ylabel('Native LCOE (USD2004/MWh)')
    axes[1].bar(range(len(adverse)), [r['unmet_heat_mw'] for r in adverse], color='#b2182b')
    axes[1].set(ylabel='Native unmet heat (MW)', xticks=range(len(adverse)),
                xticklabels=[r['physical_design']+'\n'+r['scenario'] for r in adverse])
    axes[1].tick_params(axis='x', rotation=30)
    fig.suptitle('Preserved source controls: every case fails evaluated heat-removal check.\nFinite conditional LCOE does not make these ranked designs; scientific qualification absent.')
    for ext in ('png', 'pdf'):
        fig.savefig(R / 'plots' / ('preserved-failed-controls.' + ext), dpi=180)
    plt.close(fig)
    report(rows, comparisons, findings, settings, cases)
    print(json.dumps(read('results/robustness-findings.json'), indent=2))


def report(rows, comparisons, findings, settings, cases):
    lines = ['# Robustness of conditional area and demand comparisons', '',
        '[AGENT executor interpretation] All 174 declared native cases completed once. Independent all-point checking passes 364 numerical channels and 14 rederived predicates per point. The 168 design/uncertainty cases pass evaluated checks; all six inherited source controls retain heat-removal failures. Scientific qualification is absent throughout.', '',
        'Reducing both purchased exchanger areas to 45,000 m² remains a small saving in every tested uncertainty setting and both fixed fuel scenarios. The near-feed-floor operating diagnostic is less stable: its apparent feed100 advantage reverses under lower neutron multiplication, lower availability and lower tritium price. These are conditional results from twenty one-at-a-time settings plus default, not joint-uncertainty robustness or a physical optimum.', '',
        '## Cases, matching and quantities', '',
        'Four fixed physical designs are the assumed integrated baseline (50k/50k m², density 5e20 m⁻³), area45k at the same density, near-feed-floor at 45k/45k and 4.875e20, and high-density-demand at 45k/45k and 5.25e20. Three physical descriptor groups and ten uncertainty groups give thirteen declared groups; the correlated HX price group has two explicitly tied independent keys. No automatic resizing occurs.', '',
        'Every design receives the same 21 assumption settings and the same two fixed supply scenarios. No-credit supplies zero new feed and zero service. Feed100 supplies 100 kg/calendar-year and charges 30 million USD2004/year service, even when feed is curtailed. Exhaust recycling is already credited before gross new makeup. The six source controls retain inherited assumptions and are excluded from ranking.', '',
        'results/all-case-accounting.csv is the compact full 174-row account: physical/uncertainty/supply labels, net MW and MWh/year, gross/feed/purchases/curtailment, annual service, all eleven native LCOE contributions and total, installed area/UA in MW/K/quantity/capital, unmet heat and qualification. results/accounting.json retains every native margin and predicate. results/matched-comparisons.json compares each candidate to the baseline at the SAME uncertainty setting and supply scenario. Generic default-baseline deltas are not used for robustness conclusions.', '',
        'All 126 intended comparisons pass evaluated checks on both sides. The reporting guard would mark either-side failures unrankable while retaining their numerical differences. This evaluated status never establishes scientific feasibility.', '',
        '## Matched conditional LCOE differences', '',
        'Values are candidate minus matched baseline in USD2004/MWh; negative means lower conditional cost. The default row is the only comparison against original default assumptions. Each other row uses its own changed baseline. The two supply scenarios remain separate.', '',
        '| Uncertainty setting | Area45k no-credit | Near-floor no-credit | High-demand no-credit | Area45k feed100 | Near-floor feed100 | High-demand feed100 |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for setting in settings:
        values = []
        for supply in ('no-credit', 'feed100-service30m'):
            for design in ('area45k', 'near-feed-floor', 'high-density-demand'):
                c = next(c for c in comparisons if (c['uncertainty_setting'], c['supply_scenario'], c['physical_design']) == (setting, supply, design))
                values.append(f"{c['contribution_deltas']['lcoe_sum']:+.6f}" if c['passes_evaluated_checks_both'] else 'not ranked: failed check')
        lines.append('| ' + setting + ' | ' + ' | '.join(values) + ' |')
    lines += ['', '## Equipment savings and missing physical response', '',
        'Area45k saves 0.190957–0.636126 USD2004/MWh against its matched baseline across these OAT settings. At default it saves 17.381059 million USD2004 overnight and 0.381913 USD2004/MWh. At matched assumptions, native net electricity and gross fuel makeup stay unchanged; the saving comes through selected purchased quantity, financing and capital-proportional overhaul/terminal/salvage allowances. Each reduction remains within the tested assumption window; no minimum adequate area is found.', '',
        'Changing U from 1000 to 500 or 1500 W/(m² K) changes native UA, but all tested selected areas still remove the modeled heat. Thus these U endpoints do not reverse the rankings or locate the heat-removal boundary. Deposition partitions change internal heat routing without changing the modeled total conversion result in this adequate-area window. These bounded observations do not qualify geometry, pumping pressure drop, MHD, materials or neutron transport.', '',
        'The HX price factors are a common uncertainty multiplier on two independently owned purchase inputs, not a physical hardware identity. Both price factor and discount have no modeled constraint response. Before execution, record §8 quoted the owner’s authorization for sensitivity-only assumptions and retained separate missing price/quality and financing/credit-response findings. Neither endpoint is promoted as an optimized choice.', '',
        '## Why the operating ordering reverses', '',
        'Without breeding credit, near-feed-floor is more expensive than matched baseline in all 21 settings; high-density-demand is cheaper in all 21. These are fixed-hardware imposed-demand diagnostics. Confinement and controllability are unqualified, so the lower price does not select a realizable operating point.', '',
        'With feed100, near-feed-floor is cheaper at default, but becomes more expensive at neutron multiplier 1, availability 0.75, and tritium price 10 million USD2004/kg. High-density-demand becomes cheaper at availability 0.75 and tritium price 10 million; it is more expensive in the other 19 settings. The following native quantities explain the reversals.', '',
        '| Setting / physical design, feed100 | Net MW | MWh/year | Gross T kg/year | Purchases kg/year | LCOE USD2004/MWh |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for setting in ('default', 'neutron_multiplier=1', 'availability=0.75', 'availability=0.95', 'tritium_price=10000000.0', 'tritium_price=100000000.0'):
        for design in ('baseline', 'near-feed-floor', 'high-density-demand'):
            r = cases[design, setting, 'feed100-service30m']
            lines.append(f'| {setting} / {design} | {r["net_mw"]:.6f} | {r["annual_mwh"]:.3f} | {r["gross_makeup_kg_year"]:.6f} | {r["external_purchases_kg_year"]:.6f} | {r["contributions"]["lcoe_sum"]:.6f} |')
    lines += ['', 'At availability 0.75 the baseline and near-floor designs both require less than the fixed 100 kg/year supply, removing the near-floor purchase advantage; the lower electricity then makes near-floor more expensive. At 0.95 both require supplemental purchases, and near-floor remains slightly cheaper. Availability does not multiply the independently supplied feed or service charge.', '',
        'Reducing neutron multiplication to 1 lowers native thermal/electrical output without changing gross makeup at the same density. The near-floor design still avoids purchases, but its reduced denominator outweighs that advantage. At the lower tritium price, purchases matter less and the high-demand design’s larger denominator becomes cheaper.', '',
        'Tritium price changes initial stock purchase capital as well as annual external purchases. At 10 million USD2004/kg baseline overnight capital is 4.052208470 billion USD2004; at 100 million it is 5.393208470 billion. A fuel-price interpretation that holds initial stock capital fixed would misstate the native graph. The default remains 30 million per kg.', '',
        'Other-load sensitivity changes only the 5 MW generator auxiliary allowance to 2.5 or 7.5 MW. Cryogenic and control assumptions remain held. This narrow test does not establish robustness to all parasitic loads. The nonfuel/nonsupply subtotal in the JSON is presentation arithmetic excluding tritium, deuterium and supply service; exact contribution differences remain available for every comparison.', '',
        '## Source controls and unsupported checks', '',
        '| Source control, both supply scenarios | Unmet heat MW | Failed qualified predicates |',
        '| --- | ---: | --- |']
    for r in rows:
        if r['classification'] == 'preserved source control' and r['scenario'] == 'no-credit':
            lines.append(f'| {r["physical_design"]} | {r["unmet_heat_mw"]:.6f} | ' + '; '.join(k+'='+v for k,v in r['verdicts'].items() if v!='satisfied') + ' |')
    lines += ['', 'Source controls retain finite conditional LCOE and their actual failures. No published-source numerical agreement is asserted; earlier source-boundary and unmatched-comparison evidence remains applicable. Plant scientific flags for magnets, deposition, hydraulics, machine maps, breeding and materials remain unsupported. New-feed/extraction support remains unsupported; passing a numerical capacity screen is a different claim.', '',
        '## Verification and replay', '',
        'The 174 unique maps completed once through the stock native lifecycle, with 174 starts and 174 commits. All-point independent verification passes 63,336 scalar comparisons and 2,436 rederived predicate comparisons under reviewed relative/channel-specific absolute tolerances. No model, runtime, live manifest, prior frozen study or physical oracle was changed. All production quantities came from native generated outputs.', '',
        'plots/matched-uncertainty-differences.png and .pdf show matched conditional differences; plots/default-design-accounting.* show major native contributions, electricity and fuel at the four default designs; plots/preserved-failed-controls.* visibly retain all six adverse cases and unmet heat. Every figure states the missing scientific qualification. The full CSV/JSON retain all outputs needed to inspect any other setting.', '',
        'The skeleton preceded dispatch and populated framing/rulings preceded coordinator GO and native launch. Exact execution commit and commands are in results/execution-context.json and replay.md. Reused baseline identity and fresh preflight are retained in preparation/ and results/integration/. Frozen snapshot/archive/commit are coordinator-owned.', '',
        'These engineered one-at-a-time scenarios have no assigned probabilities and do not cover simultaneous uncertainty, unknown machine maps, price calibration or scientific qualification. Equipment savings persist in the tested settings; the fuel-floor operating benefit does not. No global optimum or fully feasible reactor is claimed.']
    (R / 'report.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    analyze()
