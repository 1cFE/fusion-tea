"""Reporting for 20260926-aries-design-choice-interactions: factorial tables, main effects, interactions, rankings, limiting checks.

Reads only results/cases.json and results/constraint_catalog.json of the frozen record; writes
results/interactions.json and results/interactions.md. Presentation arithmetic only (differences of
stored channels); it fills no model output.
"""
import json, re, sys
from pathlib import Path
R = Path(sys.argv[1]).resolve()
P = 'aries_integrated_plant__'
cases = {c['case']: c for c in json.loads((R / 'results/cases.json').read_text())['cases']}
config = json.loads((R / 'config.json').read_text())
aliases = config.get('aliases', {})
def case(name):
    return cases[aliases.get(name, name)]
CH = {'net': P+'plant_ledger__evaluate__net_electric', 'gross': P+'plant_ledger__evaluate__gross_electric', 'eff': P+'plant_ledger__evaluate__thermal_efficiency',
      'tt': P+'heat_exchangers__evaluate__turbine_temperature', 'inlet': P+'heat_exchangers__evaluate__heater_inlet', 'unmet': P+'heat_exchangers__evaluate__unmet_heat',
      'he_unmet': P+'heat_exchangers__evaluate__he_unmet', 'pbli_unmet': P+'heat_exchangers__evaluate__pbli_unmet', 'div_unmet': P+'heat_exchangers__evaluate__divertor_unmet',
      'accepted': P+'heat_exchangers__evaluate__accepted_heat', 'comp': P+'plant_ledger__evaluate__compressor_demand', 'aux': P+'plant_ledger__evaluate__auxiliary_electric',
      'pump_e': P+'he_pump__evaluate__electric', 'fus': P+'source__evaluate__selected_power', 'lcoe': P+'lifecycle_accounts__evaluate__lcoe_sum',
      'ext_t': P+'fuel_inventory__annual__annual_external', 'm_comp': P+'compressor_capacity__evaluate__margin', 'm_he': P+'he_capacity__evaluate__margin',
      'm_pbli': P+'pbli_capacity__evaluate__margin', 'm_div': P+'divertor_capacity__evaluate__margin', 'm_turb': P+'turbine_capacity__evaluate__margin',
      'm_gen': P+'generator_capacity__evaluate__margin', 'm_rej': P+'rejection_capacity__evaluate__margin', 'm_fuel': P+'fuel_capacity__evaluate__margin',
      'm_hepump': P+'he_pump__screen__margin', 'm_pblipump': P+'pbli_pump__screen__margin', 'm_divpump': P+'divertor_pump__screen__margin', 'm_stock': P+'fuel_inventory__screen__margin'}
RATING = {'m_comp': P+'compressor_capacity__selected_rating', 'm_he': P+'he_capacity__selected_rating', 'm_pbli': P+'pbli_capacity__selected_rating', 'm_div': P+'divertor_capacity__selected_rating',
          'm_turb': P+'turbine_capacity__selected_rating', 'm_gen': P+'generator_capacity__selected_rating', 'm_rej': P+'rejection_capacity__selected_rating', 'm_fuel': P+'fuel_capacity__selected_rating',
          'm_hepump': P+'he_pump__selected_flow_capacity', 'm_pblipump': P+'pbli_pump__selected_flow_capacity', 'm_divpump': P+'divertor_pump__selected_flow_capacity', 'm_stock': P+'fuel_inventory__selected_tritium_kg'}
def val(c, k):
    v = c['outputs'].get(CH[k]); return None if v is None else float(v)
def short_violated(c):
    return sorted(k.split('__')[1] + '__' + k.split('__')[2] for k, v in c['verdicts'].items() if 'violated' in str(v).lower())
def limiting(c):
    """The check with the smallest normalized margin (margin / selected rating); violated checks first."""
    rows = []
    for k, rk in RATING.items():
        m, r = val(c, k), c['inputs'].get(rk)
        if m is None or r in (None, 0): continue
        rows.append((m / float(r), k, m))
    rows.sort()
    return {'violated': short_violated(c), 'smallest_normalized_margin': [{'check': k, 'margin': m, 'normalized': n} for n, k, m in rows[:3]]}
def row(name):
    c = case(name)
    return {k: val(c, k) for k in CH} | {'case': name, 'stored_as': aliases.get(name, name), 'violated': short_violated(c), 'limiting': limiting(c)}
out = {'study_id': R.name, 'cases': len(cases)}
md = [f'# Interactions reading — {R.name}', '', '[AGENT: executor] Every number is a stored channel of `results/cases.json` or a difference of two; nothing is modelled here. Margins are `rating − demand` in the screen\'s own units; "limiting" is the violated set, else the smallest margin normalized by the selected rating.', '']
def table(title, names, cols):
    md.extend([f'### {title}', '', '| case | ' + ' | '.join(cols) + ' | violated |', '|---|' + '---|' * (len(cols) + 1)])
    rows = []
    for n in names:
        r = row(n); rows.append(r)
        md.append(f'| {n} | ' + ' | '.join('' if r[c] is None else (f'{r[c]:.3f}' if abs(r[c]) < 1e6 else f'{r[c]:.3e}') for c in cols) + ' | ' + (', '.join(r['violated']) or '—') + ' |')
    md.append('')
    return rows
# ---- B1
b1 = {}
for tag in ('N', 'A'):
    names = [f'b1-{tag}-rec{rec}-lvl{lvl:+d}' for rec in (0.5, 0.8, 0.95) for lvl in (-60, 0, 60)]
    rows = table(f'B1 on the {tag} base: recuperation × source temperature level', names, ['net', 'eff', 'tt', 'inlet', 'accepted', 'unmet', 'he_unmet', 'lcoe', 'm_comp', 'm_he'])
    grid = {(re.search(r'-rec([0-9.]+)', r['case']).group(1), int(re.search(r'-lvl([+-]\d+)', r['case']).group(1))): r for r in rows}
    recs, lvls = ['0.5', '0.8', '0.95'], [-60, 0, 60]
    ranking = {lvl: sorted(recs, key=lambda rc: -grid[(rc, lvl)]['net']) for lvl in lvls}
    best = {lvl: ranking[lvl][0] for lvl in lvls}
    # difference of differences on net: (rec 0.95 − rec 0.5) at +60 minus the same at −60
    dod = (grid[('0.95', 60)]['net'] - grid[('0.5', 60)]['net']) - (grid[('0.95', -60)]['net'] - grid[('0.5', -60)]['net'])
    main_rec = {rc: sum(grid[(rc, l)]['net'] for l in lvls) / 3 for rc in recs}
    main_lvl = {l: sum(grid[(rc, l)]['net'] for rc in recs) / 3 for l in lvls}
    unmet_max = {rc: max(grid[(rc, l)]['unmet'] for l in lvls) for rc in recs}
    b1[tag] = {'ranking_by_net': {str(k): v for k, v in ranking.items()}, 'preferred_recuperation_by_level': {str(k): v for k, v in best.items()}, 'net_difference_of_differences_MW': dod,
               'main_effect_recuperation_net': main_rec, 'main_effect_level_net': main_lvl, 'max_unmet_by_recuperation': unmet_max, 'rows': rows}
    md.extend([f'Ranking of recuperation by net electricity per level ({tag}): ' + '; '.join(f'level {l:+d} K: {" > ".join(ranking[l])}' for l in lvls) + '.',
               f'Difference of differences on net ({tag}), (0.95 − 0.5) at +60 K minus (0.95 − 0.5) at −60 K: {dod:.3f} MW. Main effects on net: recuperation ' + ', '.join(f'{k} → {v:.3f}' for k, v in main_rec.items()) + '; level ' + ', '.join(f'{k:+d} → {v:.3f}' for k, v in main_lvl.items()) + '.', ''])
corner = [f'b1-N-rec{rec}-lvl{lvl:+d}-eta0.90' for rec in (0.5, 0.95) for lvl in (-60, 60)]
rows = table('B1 assumption change: turbine efficiency 0.90 at the four N corners', corner, ['net', 'eff', 'tt', 'unmet', 'lcoe'])
g = {(re.search(r'-rec([0-9.]+)', r['case']).group(1), int(re.search(r'-lvl([+-]\d+)', r['case']).group(1))): r for r in rows}
dod90 = (g[('0.95', 60)]['net'] - g[('0.5', 60)]['net']) - (g[('0.95', -60)]['net'] - g[('0.5', -60)]['net'])
b1['eta0.90'] = {'net_difference_of_differences_MW': dod90, 'preferred_at_-60': max(('0.5', '0.95'), key=lambda rc: g[(rc, -60)]['net']), 'preferred_at_+60': max(('0.5', '0.95'), key=lambda rc: g[(rc, 60)]['net']), 'rows': rows}
md.extend([f'At turbine efficiency 0.90 the difference of differences is {dod90:.3f} MW; preferred recuperation at −60 K: {b1["eta0.90"]["preferred_at_-60"]}, at +60 K: {b1["eta0.90"]["preferred_at_+60"]}.', ''])
out['B1'] = b1
# ---- B2
names = [f'b2-N-flow{f}-pump{m}-rec{rec}' for rec in (0.8, 0.95) for m in (0, 1) for f in (2600, 3261, 3900)]
rows = table('B2 on the N base: helium flow × pump law × recuperation', names, ['net', 'pump_e', 'aux', 'unmet', 'he_unmet', 'accepted', 'lcoe', 'm_hepump', 'm_he'])
gb = {(int(re.search(r'-flow(\d+)', r['case']).group(1)), int(re.search(r'-pump(\d)', r['case']).group(1)), re.search(r'-rec([0-9.]+)', r['case']).group(1)): r for r in rows}
b2 = {'net_gain_per_flow_step': {}, 'lcoe_change_per_flow_step': {}, 'rows': rows}
for rec in ('0.8', '0.95'):
    for m in (0, 1):
        b2['net_gain_per_flow_step'][f'rec{rec}-pump{m}'] = {'2600→3261': gb[(3261, m, rec)]['net'] - gb[(2600, m, rec)]['net'], '3261→3900': gb[(3900, m, rec)]['net'] - gb[(3261, m, rec)]['net']}
        b2['lcoe_change_per_flow_step'][f'rec{rec}-pump{m}'] = {'2600→3261': gb[(3261, m, rec)]['lcoe'] - gb[(2600, m, rec)]['lcoe'], '3261→3900': gb[(3900, m, rec)]['lcoe'] - gb[(3261, m, rec)]['lcoe']}
md.append('Net gain per flow step (MW): ' + '; '.join(f'{k}: {v["2600→3261"]:+.3f} then {v["3261→3900"]:+.3f}' for k, v in b2['net_gain_per_flow_step'].items()) + '.')
md.append('LCOE change per flow step (USD2004/MWh): ' + '; '.join(f'{k}: {v["2600→3261"]:+.3f} then {v["3261→3900"]:+.3f}' for k, v in b2['lcoe_change_per_flow_step'].items()) + '.')
md.append('')
names_a = [f'b2-A-flow{f}-pump{m}-rec0.95-lvl-60' for m in (1, 0) for f in (3359, 4000, 4700)]
rows_a = table('B2 on the A base where the helium stage binds (recuperation 0.95, level −60 K): helium flow × pump law', names_a, ['net', 'pump_e', 'aux', 'unmet', 'he_unmet', 'accepted', 'lcoe', 'm_hepump', 'm_he'])
ga = {(int(re.search(r'-flow(\d+)', r['case']).group(1)), int(re.search(r'-pump(\d)', r['case']).group(1))): r for r in rows_a}
b2['A_binding'] = {'rows': rows_a, 'net_gain_per_flow_step': {f'pump{m}': {'3359→4000': ga[(4000, m)]['net'] - ga[(3359, m)]['net'], '4000→4700': ga[(4700, m)]['net'] - ga[(4000, m)]['net']} for m in (1, 0)},
                   'unmet_change_per_flow_step': {f'pump{m}': {'3359→4000': ga[(4000, m)]['unmet'] - ga[(3359, m)]['unmet'], '4000→4700': ga[(4700, m)]['unmet'] - ga[(4000, m)]['unmet']} for m in (1, 0)}}
md.append('On the binding A case, net gain per flow step (MW): ' + '; '.join(f'{k}: {v["3359→4000"]:+.3f} then {v["4000→4700"]:+.3f}' for k, v in b2['A_binding']['net_gain_per_flow_step'].items()) + '; unmet-heat change per step (MW): ' + '; '.join(f'{k}: {v["3359→4000"]:+.3f} then {v["4000→4700"]:+.3f}' for k, v in b2['A_binding']['unmet_change_per_flow_step'].items()) + '.')
md.append('')
out['B2'] = b2
# ---- B3
names = [f'b3-N-amp{a:.2f}e20-hol{h:.2f}-net{n}' for n in (0, 1) for h in (0.66, 0.60) for a in (4.75, 5.0, 5.5, 5.75)]
rows = table('B3 on the N base: density amplitude × hollowness × arrangement', names, ['fus', 'net', 'unmet', 'ext_t', 'm_fuel', 'm_he', 'm_pbli', 'm_comp', 'm_stock', 'lcoe'])
b3 = {'limiting_by_case': {r['case']: r['limiting'] for r in rows}, 'rows': rows}
md.extend(['Limiting check per case (violated set; else the smallest normalized margin):', ''] + [f'- {r["case"]}: ' + (('violated ' + ', '.join(r['violated'])) if r['violated'] else 'none violated') + '; smallest margins ' + ', '.join(f'{x["check"]} {x["normalized"]:+.3f}' for x in r['limiting']['smallest_normalized_margin']) for r in rows] + [''])
out['B3'] = b3
(R / 'results/interactions.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
(R / 'results/interactions.md').write_text('\n'.join(md) + '\n')
print(json.dumps({'B1_dod_N': b1['N']['net_difference_of_differences_MW'], 'B1_dod_A': b1['A']['net_difference_of_differences_MW'], 'B1_pref_N': b1['N']['preferred_recuperation_by_level'], 'B1_pref_A': b1['A']['preferred_recuperation_by_level'], 'B1_dod_eta90': dod90}, indent=1))
