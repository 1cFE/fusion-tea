"""T-002: scratch native screens of the input-expressible compatibility-map rows on both live packages.

Direct stock route (strict PreparedEvaluator + CandidateBridge), one evaluation per case, exceptions caught
and recorded as refusals with the body's message. Writes only the scratchpad (--work) and the receipt (--out).
No study record, no store, no package write. Cases are diagnostic screens, never designs.
"""
import argparse, json, os, shutil, sys, tempfile, traceback
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
from simkit.study.bridge import CandidateBridge  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
args.work.mkdir(parents=True, exist_ok=True)

def run(prepared, base, cases, keep):
    bridge = CandidateBridge(prepared.entry_models)
    results = []
    for name, overrides, note in cases:
        point = dict(base); point.update(overrides)
        rec = {'case': name, 'note': note, 'overrides': overrides}
        try:
            row = prepared.evaluate(bridge.build(point))
            outs = {k: v for k, v in dict(row.outputs).items() if any(s in k for s in keep)}
            resp = {k: (v if isinstance(v, (str, int, float, bool)) else str(v)) for k, v in dict(row.responses).items()}
            verdicts = {k: v for k, v in resp.items() if k != 'headline'}
            counts = {}
            for v in verdicts.values():
                key = str(v).split('.')[-1].split("'")[0].lower()
                counts[key] = counts.get(key, 0) + 1
            rec.update(state='completed', outputs=outs, verdicts=verdicts, verdict_counts=counts,
                       violated=[k for k, v in verdicts.items() if 'violated' in str(v).lower()])
        except Exception as exc:
            msg = str(exc)
            rec.update(state='refused', exception_type=type(exc).__name__, message=msg[:600],
                       traceback_tail=traceback.format_exc().splitlines()[-3:])
        results.append(rec)
        print(json.dumps({'case': name, 'state': rec['state'], 'msg': rec.get('message', '')[:160]}))
    return results

receipt = {'head': '7cb0ae46 (entry)', 'packages': {}}

# ---------------- ARIES: single-branch Stellaris-like supply to the Brayton (map H1/H10/O1) ----------------
from exploration.aries_integrated.studies import study_route as aries  # noqa: E402
sealed = json.loads((ROOT / 'exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json').read_text())['cases']
base = dict(next(r for r in sealed if r['case'] == 'nominal-calculated')['inputs'])
P = 'aries_integrated_plant__'
STELLARIS_LIKE = {  # the Stellaris loop's own numbers (baseline.json): p_fus 2652.563, q_ihx 3301.213 MW, mdot 3009.756 kg/s, T_out 773.15 K
    P+'source__producer_mode': 0.0, P+'source__reference_fusion_mw': 2652.5632625175904,
    P+'deposition__heat_mode': 0.0, P+'deposition__neutron_multiplier': 1.305669, P+'deposition__radiation_fraction': 1.0,
    P+'deposition__helium_fraction': 1.0, P+'deposition__exchange_fraction': 0.0, P+'deposition__auxiliary_heat': 0.0,
    P+'heat_exchangers__he_flow': 3009.7557068000247, P+'heat_exchangers__he_cp': 5193.0, P+'heat_exchangers__he_limit': 773.15,
    P+'pbli_hx__selected_area': 0.0, P+'divertor_hx__selected_area': 0.0,
    P+'heat_exchangers__network_mode': 0.0,
}
KEEP_A = ['heat_exchangers__evaluate__turbine_temperature', 'heat_exchangers__evaluate__heater_inlet', 'heat_exchangers__evaluate__accepted_heat',
          'heat_exchangers__evaluate__unmet_heat', 'heat_exchangers__evaluate__he_transferred', 'heat_exchangers__evaluate__he_unmet', 'heat_exchangers__evaluate__he_hot',
          'heat_exchangers__evaluate__he_return', 'heat_exchangers__evaluate__he_capability', 'heat_exchangers__evaluate__pbli_transferred', 'heat_exchangers__evaluate__divertor_transferred',
          'deposition__evaluate__he_deposition', 'deposition__evaluate__source_residual', 'he_coolant__evaluate__delivered_heat',
          'plant_ledger__evaluate__net_electric', 'plant_ledger__evaluate__gross_electric', 'plant_ledger__evaluate__thermal_efficiency', 'plant_ledger__evaluate__compressor_demand',
          'plant_ledger__evaluate__cycle_rejection', 'plant_ledger__evaluate__auxiliary_electric', 'plant_ledger__evaluate__plant_residual', 'plant_ledger__evaluate__unmatched_source_heat',
          'plant_ledger__evaluate__primary_pump_electric', 'capacity__evaluate__margin', 'he_pump__evaluate__electric', 'lcoe', 'fuel_capacity', 'annual_external']
cases_a = [('aries-nominal-calculated-control', {}, 'sealed nominal-calculated replayed as the control')]
for flow in (1400.0, 2500.0, 4000.0, 6000.0, 8000.0):
    for eff in (0.8, 0.5, 0.2):
        cases_a.append((f'stellaris-supply-flow{int(flow)}-rec{eff}', dict(STELLARIS_LIKE, **{P+'cycle__selected_flow': flow, P+'cycle__recuperator_effectiveness': eff}),
                        'map H1/H10: Stellaris loop as the only branch; PbLi and divertor UA 0; ARIES ratings unchanged'))
cases_a.append(('stellaris-supply-flow6000-rec0.5-area150k', dict(STELLARIS_LIKE, **{P+'cycle__selected_flow': 6000.0, P+'cycle__recuperator_effectiveness': 0.5, P+'he_hx__selected_area': 150000.0}), 'H1 with three times the He exchanger area'))
cases_a.append(('stellaris-supply-flow6000-rec0.5-comp3200', dict(STELLARIS_LIKE, **{P+'cycle__selected_flow': 6000.0, P+'cycle__recuperator_effectiveness': 0.5, P+'compressor_capacity__selected_rating': 3200.0, P+'turbine_capacity__selected_rating': 7000.0, P+'generator_capacity__selected_rating': 3600.0, P+'rejection_capacity__selected_rating': 5000.0}), 'H1 with doubled cycle ratings (explicit re-selection, not sizing)'))
work_a = args.work / 'aries'
prepared_a = aries.prepare(aries.PACKAGE_DIR, work_a)
receipt['packages']['aries_integrated'] = {'executable_fingerprint': prepared_a.fingerprint, 'base': 'nominal-calculated (sealed 20260925-aries-revised-reference-network)',
                                           'cases': run(prepared_a, base, cases_a, KEEP_A)}

# ---------------- Stellaris: salt boundary, steam temperature and loop rise (map O2/O4) ----------------
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
import study_route as stel  # noqa: E402
original = ROOT / 'exploration/stellarator_e2e/generated'
scratch_pkg = args.work / 'stellaris' / 'stellarator_tea'
if scratch_pkg.exists():
    shutil.rmtree(scratch_pkg)
shutil.copytree(original, scratch_pkg, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
S = 'stellarator_09__stellaris__'
KEEP_S = ['pb__p_net', 'pb__p_th', 'pb__p_the', 'matched_cycle__p_gross_MW', 'matched_cycle__eta_gross', 'matched_cycle__main_min_gap_K', 'matched_cycle__reheat_min_gap_K',
          'matched_cycle__main_admission_ok', 'matched_cycle__t_main_C', 'primary_loop__T_out', 'primary_loop__mdot', 'primary_loop__q_ihx', 'equipment__salt_return_C',
          'equipment__conversion_heat_MW', 'equipment__ihx_capacity_margin_m2', 'equipment__ihx_hot_approach', 'equipment__ihx_cold_approach', 'lcoe_calc__lcoe', 'turbine__eta_th']
cases_s = [
    ('stellaris-baseline-control', {}, 'package defaults; must reproduce the documented baseline'),
    ('salt-hot-436', {S+'heat_transport__salt_hot_C': 436.0}, 'map O2: lowered salt boundary alone; predicted refusal at the salt heat join'),
    ('salt-hot-436-steam-416', {S+'heat_transport__salt_hot_C': 436.0, S+'turbine__main_steam_generator__outlet_temperature_C': 416.0, S+'turbine__reheater__outlet_temperature_C': 416.0}, 'map O2: lowered salt boundary with lowered steam; predicted refusal at the salt heat join'),
    ('steam-416', {S+'turbine__main_steam_generator__outlet_temperature_C': 416.0, S+'turbine__reheater__outlet_temperature_C': 416.0}, 'steam side alone at the temperature an ARIES helium branch could support; predicted to execute with lower efficiency'),
    ('loop-rise-156', {S+'heat_transport__loop_dT_blanket': 156.0}, 'map O4: helium hot leg 729.15 K (456 C); predicted refusal at the IHX hot approach'),
    ('loop-inlet-530', {S+'heat_transport__loop_T_in': 530.0}, 'map O4 variant: colder loop inlet; reads whether the IHX cold approach refuses'),
]
prepared_s = stel.prepare(scratch_pkg, args.work / 'stellaris' / 'evaluation')
receipt['packages']['stellarator_tea'] = {'executable_fingerprint': getattr(prepared_s, 'fingerprint', None), 'base': 'package defaults (copied package)',
                                          'cases': run(prepared_s, {}, cases_s, KEEP_S)}
args.out.write_text(json.dumps(receipt, indent=1) + '\n')
print(json.dumps({p: {'cases': len(v['cases']), 'completed': sum(c['state'] == 'completed' for c in v['cases']), 'refused': sum(c['state'] == 'refused' for c in v['cases'])} for p, v in receipt['packages'].items()}))
