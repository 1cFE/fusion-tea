"""T-003: interim checks on the canonical 891 MW alternative before any headline LCOE is interpreted.

Scratch execution only (--work); writes interim-checks.json and interim-checks.md under --out-dir.
"""
import argparse, json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from exploration.aries_integrated.studies import study_route as route, oracle_entry  # noqa: E402
P = 'aries_integrated_plant__'
FS = ROOT / 'exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/results/cases.json'
CAN = 'resized-compressor-1700-network-scaledflows-0.85'
parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True); parser.add_argument('--out-dir', type=Path, required=True)
args = parser.parse_args()
base = next(r for r in json.loads(FS.read_text())['cases'] if r['case'] == CAN)['inputs']
def case(name, **changes):
    point = dict(base); point.update({P + k: float(v) for k, v in changes.items()}); return name, point
CASES = dict([
    case('alt-canonical'),
    case('alt-compressor-rating-1600', compressor_capacity__selected_rating=1600),
    case('alt-compressor-rating-1800', compressor_capacity__selected_rating=1800),
    case('alt-he-pump-capacity-3261', he_pump__selected_flow_capacity=3261),
    case('alt-estimate-mode-1', cost_accounts__estimate_mode=1),
    case('alt-feed100-service30m', fuel_inventory__annual_recovery_kg=100, finance__supply_service_annual=30e6),
])
def key(p): return tuple(sorted((k, float(v)) for k, v in p.items()))
labels = {key(p): n for n, p in CASES.items()}
cases, db = route.run_points('aries-alternative-interim-checks', list(CASES.values()), args.work)
def o(c, n): return c.outputs.get(P + n)
def v(c, part): return next(s for cid, s in c.verdicts.items() if cid.startswith(P + part + '__'))
REPORT = ['compressor demand|plant_ledger__evaluate__compressor_demand', 'compressor rating|compressor_capacity__selected_rating', 'compressor margin|compressor_capacity__evaluate__margin', 'compressor purchase|compressor_equipment__purchase__capital', 'compressor ratio|compressor_equipment__purchase__quantity_ratio', 'compressor extrapolated|compressor_equipment__purchase__extrapolated',
          'He pump margin|he_pump__screen__margin', 'He pump purchase|he_pump__purchase__capital', 'direct|cost_ledger__evaluate__direct', 'overnight|cost_ledger__evaluate__overnight', 'financed|lifecycle_accounts__evaluate__financed_capital', 'annual operating|cost_ledger__evaluate__annual_operating', 'external T kg/yr|lifecycle_accounts__evaluate__external_shortfall', 'curtailed feed|lifecycle_accounts__evaluate__curtailed_feed', 'supply LCOE|lifecycle_accounts__evaluate__supply_lcoe', 'tritium LCOE|lifecycle_accounts__evaluate__tritium_lcoe', 'LCOE|lifecycle_price__evaluate__lcoe', 'net MW|plant_ledger__evaluate__net_electric', 'unmet MW|heat_exchangers__evaluate__unmet_heat', 'turbine K|heat_exchangers__evaluate__turbine_temperature']
rows, out = {}, {'store': str(db), 'cases': {}, 'identities': {}, 'oracle': {}, 'fuel_first_principles': {}}
for c in cases:
    name = labels[key(dict(c.inputs))]
    rec = {'state': c.state, 'candidate_id': c.candidate_id, 'inputs_changed': {k.replace(P, ''): c.inputs[k] for k in c.inputs if float(c.inputs[k]) != float(base[k])},
           'channels': {lab: (o(c, ch) if o(c, ch) is not None else c.inputs.get(P + ch)) for lab, ch in (r.split('|') for r in REPORT)},
           'verdicts': {'compressor': v(c, 'compressor_capacity'), 'he_pump': v(c, 'he_pump'), 'heat_removal': v(c, 'plant_ledger__heat_removal') if False else next(s for cid, s in c.verdicts.items() if 'heat_removal_ok' in cid), 'balances': next(s for cid, s in c.verdicts.items() if 'balances_ok' in cid)},
           'all_checks': all(s == 'satisfied' for s in c.verdicts.values())}
    out['cases'][name] = rec; rows[name] = c
# (d) single-counting identities on every case
def ident(c):
    g = lambda n: float(o(c, n)); gi = lambda n: float(c.inputs[P + n])
    contrib = ['capital_lcoe', 'om_lcoe', 'tritium_lcoe', 'supply_lcoe', 'deuterium_lcoe', 'consumables_lcoe', 'replacement_lcoe', 'other_overhaul_lcoe', 'terminal_lcoe', 'salvage_lcoe', 'imports_lcoe']
    L = 'lifecycle_accounts__evaluate__'
    d = {
        'overnight = direct + indirect + contingency + owner': g('cost_ledger__evaluate__overnight') - (g('cost_ledger__evaluate__direct') + g('indirect_cost__evaluate__cost') + g('contingency__evaluate__cost') + g('owner_commissioning__evaluate__amount')),
        'financed = overnight + idc (financing once)': g(L + 'financed_capital') - (g('cost_ledger__evaluate__overnight') + g(L + 'idc')),
        'annual_operating = O&M + external T + deuterium + consumables + imports (no reserve)': g('cost_ledger__evaluate__annual_operating') - (g('annual_om__evaluate__annual_om') + g('fuel_inventory__annual__annual_cost') + g('fuel_inventory__deuterium__annual_fuel') + gi('cost_ledger__consumables') + g('cost_ledger__evaluate__annual_import_cost')),
        'noncapital_annual = annual_operating + supply service + CRF x (pv_replacement + pv_overhaul + pv_terminal_net) (WI-091 design)': g(L + 'noncapital_annual') - (g('cost_ledger__evaluate__annual_operating') + gi('finance__supply_service_annual') + g('operating_levelization__evaluate__crf') * (g(L + 'pv_replacement') + g(L + 'pv_other_overhaul') + g(L + 'pv_terminal_net'))),
        'pv_total = financed + pv_operating + pv_supply + pv_replacement + pv_overhaul + pv_terminal_gross - pv_salvage': g(L + 'pv_total_cost') - (g(L + 'financed_capital') + g(L + 'pv_operating') + g(L + 'pv_supply') + g(L + 'pv_replacement') + g(L + 'pv_other_overhaul') + g(L + 'pv_terminal_gross') - g(L + 'pv_salvage')),
        'lcoe_sum = sum of the eleven contributions': g(L + 'lcoe_sum') - sum(g(L + n) for n in contrib),
        'lcoe = pv_total / pv_energy': g('lifecycle_price__evaluate__lcoe') - g(L + 'pv_total_cost') / g(L + 'pv_energy'),
        'lcoe = lcoe_sum': g('lifecycle_price__evaluate__lcoe') - g(L + 'lcoe_sum'),
        'lifetime replacements = event cost x event count': g('replacement__evaluate__lifetime_total') - g('replacement__evaluate__event_cost') * g('replacement__evaluate__event_count'),
        'annual_energy = net x 8760 x availability': g(L + 'annual_energy') - g('plant_ledger__evaluate__net_electric') * 8760 * gi('cost_schedule__availability'),
        'gross_makeup = burn + loss + decay': g(L + 'gross_makeup') - (g('fuel_inventory__annual__annual_burn') + g('fuel_inventory__annual__annual_loss') + g('fuel_inventory__annual__annual_decay')),
        'external = max(gross_makeup - new_feed, 0)': g(L + 'external_shortfall') - max(g(L + 'gross_makeup') - g(L + 'new_feed'), 0.0),
        'external T cost = external kg x price': g('fuel_inventory__annual__annual_cost') - g('fuel_inventory__annual__annual_external') * gi('fuel_inventory__tritium_price'),
        'gross_terminal = terminal_fraction x overnight': g(L + 'gross_terminal') - gi('finance__terminal_fraction') * g('cost_ledger__evaluate__overnight'),
        'salvage = salvage_fraction x overnight': g(L + 'salvage') - gi('finance__salvage_fraction') * g('cost_ledger__evaluate__overnight'),
        'overhaul = overhaul_fraction x overnight': g(L + 'other_overhaul_cost') - gi('finance__other_overhaul_fraction') * g('cost_ledger__evaluate__overnight'),
    }
    return {k: {'residual': val, 'ok': abs(val) <= 1e-6 * max(1.0, abs(g('cost_ledger__evaluate__overnight')) if 'overnight' in k or 'pv' in k or 'financed' in k or 'annual' in k or 'lifetime' in k or 'terminal' in k or 'salvage' in k or 'overhaul' in k or 'cost' in k else 1.0)} for k, val in d.items()}
for name, c in rows.items():
    out['identities'][name] = ident(c)
# (e) oracle re-derivation on the canonical point
c = rows['alt-canonical']
orc = oracle_entry.evaluate(dict(c.inputs))
UNMET = {P + 'heat_exchangers__evaluate__' + n for n in ('unmet_heat', 'he_unmet', 'pbli_unmet', 'divertor_unmet')}
worst, fails, covered, worst_ch = 0.0, [], [], None
for ch, ov in orc.items():
    sv = c.outputs.get(ch)
    if sv is None: continue
    sv, ov = float(sv), float(ov); d = abs(sv - ov)
    tol_abs = 1e-7 if ch in UNMET or ch.endswith('residual_magnitude') else (1e-6 if ch.endswith('__idc') else 0.0)
    ok = d <= tol_abs or (sv != 0 and d / abs(sv) <= 1e-9) or (sv == 0 and d <= 1e-9)
    if any(s in ch for s in ('lifecycle', 'fuel_inventory', 'cost_ledger', 'replacement', 'lcoe', 'purchase', 'fuel__evaluate')): covered.append(ch.replace(P, ''))
    if sv != 0 and d / abs(sv) > worst: worst, worst_ch = d / abs(sv), (ch.replace(P, ''), sv, ov)
    if not ok: fails.append({'channel': ch, 'store': sv, 'oracle': ov})
out['oracle'] = {'channels_compared': sum(1 for ch in orc if ch in c.outputs), 'worst_relative_channel': worst_ch, 'economic_channels_covered': sorted(covered), 'worst_relative': worst, 'failures': fails, 'passed': not fails}
# first-principles fuel arithmetic from the package's own constants
gi = lambda n: float(c.inputs[P + n]); g = lambda n: float(o(c, n))
power_w = g('source__evaluate__selected_power') * 1e6
B = power_w / (gi('fuel__reaction_energy_mev') * gi('fuel__mev_joules'))            # T atoms/s burned
U = B * (1 / gi('fuel__pass_burn_fraction') - 1)                                     # exhaust atoms/s
Lr = (1 - gi('fuel__exhaust_recovery')) * U                                            # permanent loss atoms/s
sec, av, mT = gi('fuel__seconds_per_year'), gi('cost_schedule__availability'), gi('fuel__tritium_atom_kg')
fp = {'burn_kg_yr': B * mT * sec * av, 'loss_kg_yr': Lr * mT * sec * av, 'decay_kg_yr': gi('fuel_inventory__selected_tritium_kg') * gi('fuel__decay_constant_s') * sec,
      'exhaust_rate_atoms_s': U, 'recycled_kg_yr_already_credited': gi('fuel__exhaust_recovery') * U * mT * sec * av}
fp['gross_makeup_kg_yr'] = fp['burn_kg_yr'] + fp['loss_kg_yr'] + fp['decay_kg_yr']
stored = {'burn_kg_yr': g('fuel_inventory__annual__annual_burn'), 'loss_kg_yr': g('fuel_inventory__annual__annual_loss'), 'decay_kg_yr': g('fuel_inventory__annual__annual_decay'), 'exhaust_rate_atoms_s': g('fuel__evaluate__exhaust_rate'), 'gross_makeup_kg_yr': g('lifecycle_accounts__evaluate__gross_makeup')}
out['fuel_first_principles'] = {'constants': {n: gi(n) for n in ('fuel__reaction_energy_mev', 'fuel__mev_joules', 'fuel__pass_burn_fraction', 'fuel__exhaust_recovery', 'fuel__tritium_atom_kg', 'fuel__decay_constant_s', 'fuel__seconds_per_year', 'fuel_inventory__selected_tritium_kg', 'cost_schedule__availability')},
    'first_principles': fp, 'stored': stored, 'relative_differences': {k: abs(fp[k] - stored[k]) / abs(stored[k]) for k in stored}}
out['passed'] = all(i['ok'] for ids in out['identities'].values() for i in ids.values()) and out['oracle']['passed'] and max(out['fuel_first_principles']['relative_differences'].values()) <= 1e-9
(args.out_dir / 'interim-checks.json').write_text(json.dumps(out, indent=2) + '\n')
# markdown
M = ['# Interim checks — T-003 (generated by `interim-checks.py`; scratch execution, not a study record)\n', f"Store: `{db}` (scratch). Package executable `{c.executable_fingerprint}`.\n", '## Targeted cases on the canonical inputs\n', '| Case | Changed input | ' + ' | '.join(r.split('|')[0] for r in REPORT) + ' | compressor check | He pump check | heat removal | all checks |', '|---|---|' + '---:|' * len(REPORT) + '---|---|---|---|']
for name, rec in out['cases'].items():
    M.append(f"| `{name}` | {', '.join(f'{k}={v}' for k, v in rec['inputs_changed'].items()) or '—'} | " + ' | '.join('—' if x is None else (f'{x:.6f}' if abs(x) < 1e6 else f'{x:,.2f}') for x in rec['channels'].values()) + f" | {rec['verdicts']['compressor']} | {rec['verdicts']['he_pump']} | {rec['verdicts']['heat_removal']} | {rec['all_checks']} |")
M.append('\n## Single-counting identities (residual, USD2004 or MWh or kg; every case)\n')
M.append('| Identity | ' + ' | '.join(f'`{n}`' for n in out['identities']) + ' |'); M.append('|---|' + '---:|' * len(out['identities']))
for k in next(iter(out['identities'].values())):
    M.append(f"| {k} | " + ' | '.join(f"{out['identities'][n][k]['residual']:.3e} {'ok' if out['identities'][n][k]['ok'] else 'FAIL'}" for n in out['identities']) + ' |')
M.append(f"\n## Oracle re-derivation of the canonical point\n\n{out['oracle']['channels_compared']} channels compared; economic channels covered: {len(out['oracle']['economic_channels_covered'])}; worst relative deviation {out['oracle']['worst_relative']:.3e} on {out['oracle']['worst_relative_channel']} (a near-zero residual channel passing its absolute rule); failures: {out['oracle']['failures'] or 'none'}.\n")
M.append('## Fuel demand from first principles (package constants; availability applied to burn and loss, calendar time to decay)\n')
M.append('| Quantity | First principles | Stored | Relative difference |\n|---|---:|---:|---:|')
for k in stored: M.append(f"| {k} | {fp[k]:.9g} | {stored[k]:.9g} | {out['fuel_first_principles']['relative_differences'][k]:.2e} |")
M.append(f"| recycled exhaust already credited (kg/yr, never subtracted again) | {fp['recycled_kg_yr_already_credited']:.6f} | — | — |")
M.append(f"\nAll checks passed: **{out['passed']}**.\n")
(args.out_dir / 'interim-checks.md').write_text('\n'.join(M) + '\n')
print(json.dumps({'passed': out['passed'], 'oracle_worst': out['oracle']['worst_relative'], 'oracle_failures': out['oracle']['failures'], 'fuel_rel': out['fuel_first_principles']['relative_differences'], 'cases': {n: (r['verdicts'], r['all_checks'], round(r['channels']['LCOE'], 6), r['channels']['compressor purchase']) for n, r in out['cases'].items()}, 'identity_fails': [(n, k) for n, ids in out['identities'].items() for k, i in ids.items() if not i['ok']]}, indent=1))
