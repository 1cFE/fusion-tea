"""Presentation-only ledger for the flow-scaling check; reads native cases only (no model arithmetic replaced)."""
import json
import sys
from pathlib import Path

P = 'aries_integrated_plant__'
CH = {'unmet': 'heat_exchangers__evaluate__unmet_heat', 'he_unmet': 'heat_exchangers__evaluate__he_unmet', 'pbli_unmet': 'heat_exchangers__evaluate__pbli_unmet',
      'div_unmet': 'heat_exchangers__evaluate__divertor_unmet', 'T1_K': 'heat_exchangers__evaluate__he_secondary_out', 'turbine_K': 'heat_exchangers__evaluate__turbine_temperature',
      'pbli_return_K': 'heat_exchangers__evaluate__pbli_return', 'pbli_cold_td_K': 'heat_exchangers__evaluate__pbli_cold_terminal_difference', 'he_hot_td_K': 'heat_exchangers__evaluate__he_hot_terminal_difference',
      'gross': 'plant_ledger__evaluate__gross_electric', 'net': 'plant_ledger__evaluate__net_electric', 'eta': 'plant_ledger__evaluate__thermal_efficiency', 'compressor_demand': 'plant_ledger__evaluate__compressor_demand'}
IN = {'he_flow': 'heat_exchangers__he_flow', 'pbli_flow': 'heat_exchangers__pbli_flow', 'div_flow': 'heat_exchangers__divertor_flow', 'cycle_flow': 'cycle__selected_flow', 'rating': 'compressor_capacity__selected_rating', 'split': 'heat_exchangers__pbli_split_fraction'}
record = Path(sys.argv[1])
rows = json.loads((record / 'results/cases.json').read_text())['cases']
cases = {}
for r in rows:
    d = {k: float(r['outputs'][P + c]) for k, c in CH.items()}
    d.update({k: float(r['inputs'][P + c]) for k, c in IN.items()})
    d['all_checks'] = all(v == 'satisfied' for v in r['verdicts'].values())
    cases[r['case']] = d
base, sc, pb, he = cases['network-c3-0.85'], cases['network-c3-scaledflows-0.85'], cases['network-c3-scaledflows-pbli-only-0.85'], cases['network-c3-scaledflows-he-only-0.85']
delta = lambda a, b, k: b[k] - a[k]
led = {'study': record.name, 'cases': cases,
       'artefact_at_1600': {'all_flows_scaled': {k: delta(base, sc, k) for k in ('unmet', 'he_unmet', 'pbli_unmet', 'net', 'gross', 'turbine_K')},
                            'pbli_only': {k: delta(base, pb, k) for k in ('unmet', 'he_unmet', 'pbli_unmet', 'net', 'gross', 'turbine_K')},
                            'he_only': {k: delta(base, he, k) for k in ('unmet', 'he_unmet', 'pbli_unmet', 'net', 'gross', 'turbine_K')}},
       'threshold_bracket': {n: {'unmet': cases[n]['unmet'], 'all_checks': cases[n]['all_checks'], 'net': cases[n]['net']} for n in ('network-c3-0.85', 'resized-compressor-1650-network-0.85', 'resized-compressor-1700-network-0.85', 'network-c3-scaledflows-0.85', 'resized-compressor-1650-network-scaledflows-0.85', 'resized-compressor-1700-network-scaledflows-0.85')},
       'steady_invariance': {k: cases['resized-compressor-1700-network-scaledflows-0.85'][k] - cases['resized-compressor-1700-network-0.85'][k] for k in ('net', 'gross', 'turbine_K', 'eta')}}
(record / 'results/attribution.json').write_text(json.dumps(led, indent=2) + '\n')
f = lambda x: f'{x:.3f}'
lines = ['# Flow-scaling check ledger (presentation only)', '', '| Case | He / PbLi / div flow kg/s | cycle kg/s | split | unmet (He / PbLi / div) | after He stage °C | turbine °C | PbLi return °C | PbLi cold ΔT K | gross | net | all checks |', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for n, c in cases.items():
    lines.append(f"| {n} | {c['he_flow']:.0f} / {c['pbli_flow']:.0f} / {c['div_flow']:.1f} | {c['cycle_flow']:.0f} | {c['split']:.2f} | {f(c['unmet'])} ({f(c['he_unmet'])} / {f(c['pbli_unmet'])} / {f(c['div_unmet'])}) | {c['T1_K']-273.15:.1f} | {c['turbine_K']-273.15:.1f} | {c['pbli_return_K']-273.15:.1f} | {c['pbli_cold_td_K']:.1f} | {f(c['gross'])} | {f(c['net'])} | {c['all_checks']} |")
a = led['artefact_at_1600']
lines += ['', f"Scaling artefact at 1600 kg/s, split 0.85 (network case): all three flows scaled with the duties change unmet heat by {f(a['all_flows_scaled']['unmet'])} MW (PbLi {f(a['all_flows_scaled']['pbli_unmet'])}, helium {f(a['all_flows_scaled']['he_unmet'])}) and net by {f(a['all_flows_scaled']['net'])} MW; PbLi flow alone: unmet {f(a['pbli_only']['unmet'])} (PbLi {f(a['pbli_only']['pbli_unmet'])}, helium {f(a['pbli_only']['he_unmet'])}); helium flow alone: unmet {f(a['he_only']['unmet'])}.",
          f"Threshold: at 1650 kg/s the network leaves {f(cases['resized-compressor-1650-network-0.85']['unmet'])} MW unremoved (scaled flows {f(cases['resized-compressor-1650-network-scaledflows-0.85']['unmet'])}); at 1700 kg/s 0 in both. Steady invariance at 1700 kg/s: net differs by {led['steady_invariance']['net']:.3e} MW between unscaled and scaled flows."]
(record / 'results/attribution.md').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines[-2:]))
