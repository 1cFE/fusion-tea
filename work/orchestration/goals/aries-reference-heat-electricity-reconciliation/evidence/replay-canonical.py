"""T-001: replay the canonical run.py scenarios and the frozen-study variants against the current package.

Writes only to the scratch root given by --root and the summary path given by --summary.
Compares common channels with the frozen fourteen-point record (cases.json@8e6fb2f2).
"""
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'exploration/aries_integrated'))
import run as runner  # noqa: E402  (exploration/aries_integrated/run.py)
PREFIX = runner.PREFIX
FROZEN = ROOT / 'exploration/aries_integrated/studies/20260922-integrated-heat-electricity/results/cases.json'
parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--summary', type=Path, required=True)
args = parser.parse_args()
args.root.mkdir(parents=True, exist_ok=True)
scenarios = dict(runner.SCENARIOS)
# frozen-study variant: literal Lyon without the pump-mode keys (the stored point at 8e6fb2f2)
scenarios['literal-Lyon-frozen-variant'] = {PREFIX + 'cycle__recuperator_effectiveness': .95}
scenarios['literal-Raffray-frozen-variant'] = {PREFIX + 'source__reference_fusion_mw': 2365., PREFIX + 'deposition__heat_mode': 1., PREFIX + 'cycle__recuperator_effectiveness': .95}
runtime = runner.load_runtime()
_fz = json.load(open(FROZEN)); frozen = {c['case']: c for c in (_fz['cases'] if isinstance(_fz, dict) else _fz)}
CHANNELS = {
    'source': ['selected_power', 'selected_mode'],
    'deposition': ['neutron_power', 'charged_power', 'nuclear_gain', 'he_deposition', 'pbli_deposition', 'divertor_deposition', 'exchange', 'he_friction', 'pbli_friction', 'divertor_friction', 'pump_electric', 'pump_recovered', 'source_residual'],
    'he_coolant': ['delivered_heat'], 'pbli_coolant': ['delivered_heat'], 'divertor_coolant': ['delivered_heat'],
    'compressor_3': ['temperature_out', 'pressure_out'],
    'heat_exchangers': ['turbine_temperature', 'heater_inlet', 'expansion_factor', 'accepted_heat', 'unmet_heat', 'he_transferred', 'he_unmet', 'he_capability', 'he_hot', 'he_return', 'he_secondary_in', 'he_secondary_out', 'he_hot_bound_margin', 'divertor_transferred', 'divertor_unmet', 'divertor_capability', 'divertor_hot', 'divertor_return', 'divertor_secondary_in', 'divertor_secondary_out', 'pbli_transferred', 'pbli_unmet', 'pbli_capability', 'pbli_hot', 'pbli_return', 'pbli_secondary_in', 'pbli_secondary_out'],
    'turbine': ['temperature_out', 'shaft_produced'], 'recuperator': ['cold_out', 'hot_out', 'recovered_heat', 'bypass_active'], 'precooler': ['heat_into_fluid'],
    'generator_auxiliaries': ['compressor_demand', 'net_shaft', 'gross_electric', 'generator_loss', 'heating_electric', 'fuel_electric', 'cryo_electric', 'control_electric', 'other_electric_demand', 'primary_pump_electric', 'auxiliary_electric', 'net_electric'],
    'plant_ledger': ['cycle_rejection', 'thermal_efficiency', 'total_available_heat', 'plant_residual', 'branch_residual', 'cycle_residual', 'electrical_residual', 'source_energy_residual', 'comparison_gross_difference', 'comparison_net_difference', 'comparison_turbine_temperature_difference', 'comparison_heater_temperature_difference'],
    'he_pump': ['electric', 'operating_flow'], 'pbli_pump': ['electric'], 'divertor_pump': ['electric'],
}
summary = {'runtime_fingerprint': runtime[2], 'cases': {}}
for name, changes in scenarios.items():
    row = runner.execute_case(name, changes, runtime, root=args.root)
    entry = {'status': row['status'], 'changes': changes}
    if row['status'] != 'evaluated':
        entry['error'] = row['error']
    else:
        out = row['outputs']
        entry['channels'] = {}
        for owner, keys in CHANNELS.items():
            for key in keys:
                full = PREFIX + owner + '__evaluate__' + key
                if full in out:
                    entry['channels'][owner + '.' + key] = out[full]
        entry['verdicts'] = {k: v for k, v in out.items() if isinstance(v, str) or isinstance(v, bool)}
        # comparison with the frozen record on common numeric channels
        frozen_name = {'literal-Lyon-frozen-variant': 'literal-Lyon-source-input', 'literal-Raffray-frozen-variant': 'literal-Raffray-accounting'}.get(name, name)
        if frozen_name in frozen:
            fo = frozen[frozen_name]['outputs']
            common = [k for k in fo if k in out and isinstance(fo[k], (int, float)) and isinstance(out[k], (int, float))]
            diffs = {k: (fo[k], out[k]) for k in common if abs(fo[k] - out[k]) > 1e-9 * max(1., abs(fo[k]))}
            entry['frozen_comparison'] = {'frozen_case': frozen_name, 'common_numeric_channels': len(common), 'differing': diffs,
                                          'frozen_only_channels': len([k for k in fo if k not in out]), 'current_only_channels': len([k for k in out if k not in fo])}
    summary['cases'][name] = entry
    print(json.dumps({'case': name, 'status': entry['status'], **{k: entry.get('channels', {}).get(k) for k in ('source.selected_power', 'heat_exchangers.accepted_heat', 'heat_exchangers.unmet_heat', 'generator_auxiliaries.gross_electric', 'generator_auxiliaries.net_electric')}, 'diffs_vs_frozen': len(entry.get('frozen_comparison', {}).get('differing', {})) if 'frozen_comparison' in entry else None}))
args.summary.write_text(json.dumps(summary, indent=1) + '\n')
