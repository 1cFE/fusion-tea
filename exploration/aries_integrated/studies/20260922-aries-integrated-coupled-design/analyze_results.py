"""Reporting-only coupled-grid reading; native outputs are never recomputed."""
from pathlib import Path
import json
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parent
read = lambda name: json.loads((R / name).read_text())
A = read('results/accounting.json')
rows = A['cases']
assert read('results/verification_summary.json')['outcome'] == 'pass'
assert len(rows) == 68 and all(r['state'] == 'completed' for r in rows)
conn = sqlite3.connect('file:' + str(R / 'results/native' / (R.name + '.db')) + '?mode=ro&immutable=1', uri=True)
attempts = dict(conn.execute('select state,count(*) from attempt_transitions group by state'))
assert attempts == {'started': 68, 'committed': 68}
assert conn.execute('select max(attempt_number) from attempt_transitions').fetchone()[0] == 1
conn.close()
by = {(r['design'], r['scenario']): r for r in rows}
P = 'aries_integrated_plant__'
density_key = 'aries_cs_plasma_integration__plasma__amplitude'
price = lambda r: r['contributions']['lcoe_sum']
base = by['baseline', 'feed100-service30m']
area = by['grid-he45000-pbli45000-n5e+20', 'feed100-service30m']
probe = by['probe-he45000-pbli45000-n4.875e20', 'feed100-service30m']
base_probe = by['probe-he50000-pbli50000-n4.875e20', 'feed100-service30m']
science = {k: v for k, v in base['support_flags'].items() if '__plant_ledger__' in k}
assert science and all(v == 0 for v in science.values())
assert all(r['support_flags'] == base['support_flags'] for r in rows)
assert all(r['unmet_heat_mw'] == 0 for r in rows if r['classification'] not in ('preserved source control', 'inadequate equipment control'))

# Grid panels condition on density; no line interpolates between tested designs.
fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
for j, scenario in enumerate(('no-credit', 'feed100-service30m')):
    for i, density in enumerate((4.75e20, 5e20, 5.25e20)):
        selected = [r for r in rows if r['scenario'] == scenario and
                    (r['design'].startswith('grid-') or r['design'] == 'baseline') and r['inputs'][density_key] == density]
        matrix = [[price(next(r for r in selected if r['equipment']['he']['area_m2'] == he and r['equipment']['pbli']['area_m2'] == pb))
                   for he in (45000., 50000., 55000.)] for pb in (45000., 50000., 55000.)]
        ax = axes[j, i]
        im = ax.imshow(matrix, origin='lower', cmap='viridis')
        for y in range(3):
            for x in range(3):
                ax.text(x, y, f'{matrix[y][x]:.3f}', ha='center', va='center', color='white',
                        bbox={'facecolor': 'black', 'alpha': .35, 'pad': 2})
        ax.set(xticks=range(3), xticklabels=['45k', '50k', '55k'], yticks=range(3), yticklabels=['45k', '50k', '55k'],
               xlabel='Helium area (m²)', ylabel='PbLi area (m²)', title=f'{scenario}; density {density:.3g} m⁻³')
        fig.colorbar(im, ax=ax, shrink=.7, label='USD2004/MWh')
fig.suptitle('Native conditional LCOE; each panel has its own color scale.\nAll grid points pass evaluated checks; scientific qualification absent. Adverse controls retained separately.')
for ext in ('png', 'pdf'):
    fig.savefig(R / 'plots' / ('coupled-grid.' + ext), dpi=180)
plt.close(fig)

lines = ['# Coupled area and operating-demand comparison', '',
    '[AGENT executor interpretation] All 68 declared native maps completed in one attempt each. Independent all-point verification passes 364 numerical channels and 14 rederived predicates per point. Fifty-eight pass evaluated checks; ten adverse equipment/source controls retain heat-removal failures. Every point remains scientifically unqualified.', '',
    f'At baseline density, buying 45,000 m² for both helium and PbLi exchangers saves {(base["overnight_usd2004"]-area["overnight_usd2004"])/1e6:.6f} million USD2004 overnight and {price(base)-price(area):.6f} USD2004/MWh in either supply scenario. Net electricity and gross fuel demand remain unchanged. This is the supported conditional equipment saving in the tested grid.', '',
    f'The lowest tested feed100/service30m price is {price(probe):.6f} USD2004/MWh at the interior density probe 4.875e20 m⁻³ and 45k/45k areas. Its net electricity is {probe["net_mw"]:.6f} MW and gross makeup {probe["gross_makeup_kg_year"]:.6f} kg/calendar-year, just below the assumed 100 kg/year supply. External purchases fall to zero. This is an operating diagnostic governed by the supplied-fuel threshold, not a qualified physical optimum.', '',
    '## Sampling and roles', '',
    'The 27 physical grid configurations combine independently selected helium/PbLi areas 45k/50k/55k m² and imposed plasma density 4.75/5/5.25e20 m⁻³. Two interior probes use density 4.875e20 at baseline and 45k/45k areas. Two insufficient-area controls and three inherited source controls bring the total to 34 physical configurations, each evaluated with feed/service 0/0 and 100 kg/calendar-year/30 million USD2004/year. The explicit grid baseline is represented once by the automatic baseline; no map was discarded after execution.', '',
    'Areas are purchased hardware choices with provisional price/capability propagation. Density is a fixed-hardware operating diagnostic with unqualified confinement and control. The seven declared indicator groups include declined cycle-flow and independent compressor-ratio axes; possible constraint reachability does not license their design optimization. The engineered windows and two probes were reviewed before execution. No feed, service or efficiency input is optimized.', '',
    '## Complete attempted set', '',
    'All values below come from results/cases.json through results/accounting.json. The latter also retains exact effective inputs, all 11 lifecycle contributions and their total, selected areas and UA in MW/K, purchase quantities/capital, unmet heat, every qualified predicate, all scientific flags and native margins. Annual fuel quantities already account for internal exhaust recycling.', '',
    '| Design | Supply scenario | Net MW | MWh/year | Gross T kg/year | Feed kg/year | Purchased T kg/year | LCOE USD2004/MWh | Checks |',
    '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for r in rows:
    lines.append(f'| {r["design"]} | {r["scenario"]} | {r["net_mw"]:.6f} | {r["annual_mwh"]:.3f} | {r["gross_makeup_kg_year"]:.6f} | {r["new_feed_kg_year"]:.0f} | {r["external_purchases_kg_year"]:.6f} | {price(r):.6f} | ' + ('passes evaluated checks' if r['passes_evaluated_checks'] else 'heat-removal failure') + ' |')
lines += ['', '## Purchased equipment effect at fixed demand', '',
    'All nine area combinations pass evaluated checks at each of the three grid density levels. For a fixed density, native electricity and gross makeup are identical across the area grid; price responds through purchase capital, financing and the capital-proportional overhaul/terminal/salvage allowances. This does not establish a smaller-area limit or hydraulic feasibility. The lowest tested area pair remains an engineered endpoint, not an optimum.', '',
    '| Density m⁻³ | Net MW | Gross kg/year | Saving: 50k/50k → 45k/45k USD2004/MWh | Net-power change MW |',
    '| ---: | ---: | ---: | ---: | ---: |']
for density in (4.75e20, 5e20, 5.25e20):
    group = [r for r in rows if r['scenario'] == 'no-credit' and (r['design'].startswith('grid-') or r['design'] == 'baseline') and r['inputs'][density_key] == density]
    assert len({r['net_mw'] for r in group}) == 1 and len({r['gross_makeup_kg_year'] for r in group}) == 1
    pair = lambda area: next(r for r in group if r['equipment']['he']['area_m2'] == area and r['equipment']['pbli']['area_m2'] == area)
    hi, lo = pair(50000.), pair(45000.)
    lines.append(f'| {density:.3g} | {lo["net_mw"]:.6f} | {lo["gross_makeup_kg_year"]:.6f} | {price(hi)-price(lo):.6f} | {lo["net_mw"]-hi["net_mw"]:.6f} |')
lines += ['', '## Interior probe: physical denominator versus fuel floor', '',
    f'Against the baseline feed100 case, the 45k/45k interior probe lowers total LCOE by {price(base)-price(probe):.6f} USD2004/MWh. Its nonfuel/nonsupply subtotal rises from {base["nonfuel_nonsupply_lcoe_subtotal"]:.6f} to {probe["nonfuel_nonsupply_lcoe_subtotal"]:.6f} because electricity falls. The subtotal is presentation arithmetic excluding tritium, deuterium and supply service; it is not a second native plant calculation.', '',
    f'At the same interior density, changing 50k/50k to 45k/45k saves only {price(base_probe)-price(probe):.6f} USD2004/MWh. The larger apparent benefit versus baseline is therefore chiefly the assumed purchase-floor interaction. Service remains 30 million USD2004/year even when excess new feed is curtailed. The probe curtails {probe["curtailed_feed_kg_year"]:.6f} kg/year without sales revenue.', '',
    '| Native contribution | Baseline feed100 | Interior 45k/45k feed100 | Difference USD2004/MWh |',
    '| --- | ---: | ---: | ---: |']
for key in base['contributions']:
    a, b = base['contributions'][key], probe['contributions'][key]
    lines.append(f'| {key} | {a:.9f} | {b:.9f} | {b-a:+.9f} |')
lines += ['', f'Without breeding credit, that same probe costs {price(by[probe["design"], "no-credit"]):.6f} USD2004/MWh, above the baseline {price(by["baseline", "no-credit"]):.6f}. The lowest tested no-credit case is the 5.25e20 density and 45k/45k area combination at {price(by["grid-he45000-pbli45000-n5.25e+20", "no-credit"]):.6f}; its higher density is still an unqualified operating diagnostic. The conclusions reverse with the fixed supply scenario, so neither is a hardware optimum.', '',
    '## Failures and unsupported science', '',
    'Source controls and insufficient-area cases are excluded from design ranking. All ten are retained in the attempted set, contribution plots and native margins. Their paired finite LCOE is not evidence that their heat-removal failure is acceptable. No numerical source-LCOE agreement is asserted; predecessor source comparisons retain their unmatched price-year/life/capital scope.', '',
    '| Control, each in both supply scenarios | Native unmet heat MW | Failed qualified predicates |',
    '| --- | ---: | --- |']
for r in rows:
    if r['scenario'] == 'no-credit' and not r['passes_evaluated_checks']:
        lines.append(f'| {r["design"]} | {r["unmet_heat_mw"]:.6f} | ' + '; '.join(k + '=' + v for k, v in r['verdicts'].items() if v != 'satisfied') + ' |')
lines += ['', 'All plant-level scientific flags remain zero for magnet, materials, deposition, hydraulics, machine maps and breeding; native supply/extraction flags also remain zero. Supported capacity-screen arithmetic is distinct from scientific applicability. The accepted package, source modes, constant USD2004 lifecycle accounting, financing once, dated replacements without the reserve, terminal cost and negative salvage remain unchanged.', '',
    '## Plots, verification and provenance', '',
    'plots/coupled-grid.png and .pdf condition each area grid on density and supply scenario. Each panel has its own explicitly labeled color scale. The other figure pairs show axes, native electricity/fuel/capital, all case contributions, unmet heat and individual margins. Failed checks use crosses or failed labels; all plots retain the absent scientific qualification. The complete contribution arrays and exact native units remain in accounting/package artifacts.', '',
    'All 68 cases ran once through the stock native lifecycle. Independent checking covers 24,752 scalar comparisons and 952 predicate comparisons. Two reviewed channel-specific absolute tolerances supplement relative tolerance; numerical agreement does not qualify assumptions. Verification retains its explicit non-independent channels and scope.', '',
    'Process finding: reviewed T-004 scope, owner intake, framing/checkpoint, configuration, oracle scan and passed preflight existed before launch, but the coordinator assembled record.md after launch. execution-context.json and the goal trail preserve this ordering. No gate or authorization was skipped; no point was rerun to obscure timing. Future record skeletons should precede dispatch.', '',
    'Exact commands and execution HEAD are retained in replay.md and results/execution-context.json. The reused baseline receipt is identified under preparation/reused-baseline-provenance.json. All report arithmetic reads stored native values only. Immutable archive, snapshot and commit are coordinator-owned.']
(R / 'report.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'cases': len(rows), 'passes_evaluated_checks': sum(r['passes_evaluated_checks'] for r in rows), 'attempts': attempts,
                  'feed_probe_lcoe': price(probe), 'report': str(R / 'report.md')}))
