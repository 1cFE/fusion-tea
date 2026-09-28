"""Check every stored case of study 20260926-design-study-parameters against the loop's required return condition (owner direction 4, 2026-09-26): the 'Primary Coolant Loop' definition holds the blanket inlet at loop_T_in and states that the IHX must deliver the helium to the circulator at T_comp_in (mfe_primary_loop.sysml doc, "T_comp_in is what the IHX must deliver, not evidence that it can"); the assembly binds the loop's T_out, mdot and q_ihx into the closure and never compares the closure's he_return with T_comp_in. Residual = T_comp_in - he_return (K); a positive residual is helium returned colder than the loop assumes (the exchanger has more capability than the point uses); the bypass-equivalent fraction f = residual / (T_out - he_return) is the share of primary flow a plant would route around the exchanger to lift the return to T_comp_in (mixing at T_out), an inlet control the model does not include. Reads stored channels only."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
R = ROOT / 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters'
P = 'costed_loop_brayton__plant__'
cases = json.load(open(R / 'results/cases.json'))['cases']
rows = []
for c in cases:
    o = c['outputs']
    tci, ret, tout = o[P + 'primary_loop__evaluate__T_comp_in'], o[P + 'heat_exchangers__evaluate__he_return'], o[P + 'primary_loop__evaluate__T_out']
    res = tci - ret
    rows.append({'case': c['case'], 'candidate': c['candidate_id'], 'T_comp_in_K': tci, 'he_return_K': ret, 'residual_K': res,
                 'he_hot_bound_margin_K': o[P + 'heat_exchangers__evaluate__he_hot_bound_margin'], 'unmet_MW': o[P + 'heat_exchangers__evaluate__unmet_heat'],
                 'bypass_equivalent_fraction': res / (tout - ret) if res > 0 else 0.0, 'net_MW': o[P + 'electrical__evaluate__net_electric'],
                 'passing': all(v == 'satisfied' for v in c['verdicts'].values())})
by = {r['case']: r for r in rows}
identity = sum(abs(r['residual_K'] - r['he_hot_bound_margin_K']) < 1e-6 for r in rows if r['unmet_MW'] <= 1e-6)
leading = ['ir-f2500-r1.5183', 'ir-f2250-r1.5183', 'ir-f2750-r1.3750', 'ir-f3000-r1.3250', 'ir-f2500-r1.4500', 'ir-f2500-r1.4250', 's6-hx75000-f2500-r1.4000', 's6-hx75000-f2250-r1.5000']
passing = sorted((r for r in rows if r['passing'] and r['case'].startswith('ir-')), key=lambda r: r['residual_K'])
summary = {'condition': 'he_return == T_comp_in (the loop definition: the IHX must deliver T_comp_in so that the circulator returns the helium to the held blanket inlet loop_T_in)',
           'source_of_condition': 'models/library/analyses/mfe_primary_loop.sysml doc; loop_T_in and loop_dT_blanket bound in models/designs/stellarator_09/stellarator_plant.sysml:1257-1260 to Moscato et al. output.md:79 (helium at 8 MPa and 300 C, outlet 500 C); inherited by combinations_loop_brayton.sysml:28-29 and costed_loop_brayton.sysml:34',
           'checked_in_assembly': False, 'T_comp_in_K': rows[0]['T_comp_in_K'],
           'identity_residual_equals_he_hot_bound_margin_when_all_heat_removed': {'holds_at': identity, 'of': sum(r['unmet_MW'] <= 1e-6 for r in rows)},
           'leading_cases': [by[k] for k in leading],
           'passing_ir_residual_K': {'min': passing[0]['residual_K'], 'median': passing[len(passing) // 2]['residual_K'], 'max': passing[-1]['residual_K'], 'count': len(passing)},
           'passing_ir_within_5K': [r['case'] for r in passing if r['residual_K'] < 5], 'passing_ir_within_15K': [r['case'] for r in passing if r['residual_K'] < 15],
           'rows': rows}
(Path(__file__).with_suffix('.json')).write_text(json.dumps(summary, indent=1) + '\n')
L = ['# Return-condition check (owner direction 4)', '',
     'Condition: the helium must return from the exchanger at the loop\'s compressor inlet temperature `T_comp_in` (' + f"{rows[0]['T_comp_in_K']:.2f} K" + ') so that the circulator delivers the blanket inlet the loop holds (573.15 K, Moscato et al. output.md:79). It is stated in the loop definition and not checked in the assembly. Residual = `T_comp_in` − `he_return`; it equals the stored `he_hot_bound_margin` at every case where all heat is removed (' + f"{identity} of {summary['identity_residual_equals_he_hot_bound_margin_when_all_heat_removed']['of']}" + ').', '',
     '| Case | Net MW | Unmet MW | Return K | Residual K | Bypass-equivalent | Passing |', '|---|---|---|---|---|---|---|']
for k in leading:
    r = by[k]
    L.append(f"| `{k}` | {r['net_MW']:.3f} | {r['unmet_MW']:.3f} | {r['he_return_K']:.2f} | {r['residual_K']:+.3f} | {r['bypass_equivalent_fraction']:.1%} | {'yes' if r['passing'] else 'no'} |")
L += ['', f"Passing I-R grid points ({len(passing)}): residual min {passing[0]['residual_K']:.2f} K (`{passing[0]['case']}`), median {passing[len(passing)//2]['residual_K']:.1f} K, max {passing[-1]['residual_K']:.1f} K (`{passing[-1]['case']}`); within 5 K: " + ', '.join(f'`{c}`' for c in summary['passing_ir_within_5K']) + '; within 15 K: ' + ', '.join(f'`{c}`' for c in summary['passing_ir_within_15K']) + '.']
(Path(__file__).with_suffix('.md')).write_text('\n'.join(L) + '\n')
print(json.dumps({'identity': identity, 'leading': [(by[k]['case'], round(by[k]['residual_K'], 3)) for k in leading], 'within5': summary['passing_ir_within_5K'], 'within15': summary['passing_ir_within_15K']}))
