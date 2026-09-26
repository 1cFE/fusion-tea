"""Write config.json for 20260926-aries-design-choice-interactions: three small factorials on two sealed bases.

Every case is a named full point composed on a canonical base by the reconciliation composer; the grids
are enumerated here and duplicates of a base or of another cell are recorded as aliases, never re-run.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
SID = '20260926-aries-design-choice-interactions'
P = 'aries_integrated_plant__'
Q = 'aries_cs_plasma_integration__plasma__'
N, A = 'nominal-calculated', 'resized-compressor-1700-network-scaledflows-0.85'
axis = lambda name, key, units, role, basis, missing: {'axis': name, 'keys': [{'key': key, 'provenance': 'fan_out'}], 'units': units, 'role': role, 'framing': 'sensitivity', 'window_provenance': 'engineered', 'basis': basis, 'missing_response': missing, 'declined': False}
AXES = [
    axis('recuperation', P+'cycle__recuperator_effectiveness', '1', 'operating', 'A3 nominal 0.8 (WI-089); source-supported 0.95 (reconciliation goal L-002/L-004); 0.5 a low-recovery counterfactual inside the closure domain [0,1].', 'The recuperator has no purchase, rating or screen (economics goal L-003); only the thermal closure and the downstream ratings respond.'),
    axis('he_limit', P+'heat_exchangers__he_limit', 'K', 'source', 'Source-supported blanket-helium outlet 729.15 K (reference-case contract § 2), shifted −60/0/+60 K with the other two limits as one temperature-level scenario at unchanged duty.', 'No blanket thermal-hydraulic model links the outlet temperature to duty and flow; coolant and material limits are not checked; the branch return temperature is computed.'),
    axis('divertor_limit', P+'heat_exchangers__divertor_limit', 'K', 'source', 'Source-supported divertor-helium outlet 973.15 K, shifted with the level scenario.', 'As he_limit.'),
    axis('pbli_limit', P+'heat_exchangers__pbli_limit', 'K', 'source', 'Source-supported PbLi outlet 1011.15 K, shifted with the level scenario.', 'As he_limit.'),
    axis('he_flow', P+'heat_exchangers__he_flow', 'kg/s', 'operating', 'Raffray blanket-helium flow 3261 kg/s; ±20 % window (2600, 3900) on the N base with the selected pump capacity held at 3261 so the flow screen can fail; on the A base 3359, 4000, 4700 where the helium stage binds (r1 oracle probe).', 'No hydraulic or pressure-drop model; the cubic pump proxy and the pump capacity screen are the only responses.'),
    axis('he_pump_mode', P+'he_pump__pump_mode', '1', 'assumed', 'E3 (WI-090): mode 0 cubic proxy from 156 MW at 3261 kg/s; mode 1 fixed 156 MW source power.', 'No pump map; the two laws bracket the pump-power response to flow.'),
    axis('density_amplitude', Q+'amplitude', 'm^-3', 'operating', 'WI-083 reference amplitude 5.0e20; window 4.75–5.75e20 fixed by the r1 oracle scan (4.0e20 and 6.0e20 gave nonpositive net or a bound helium stage; evidence/window-probe.txt).', 'Fixed-hardware source-demand change; no confinement or transport qualification.'),
    axis('hollowness', Q+'hollowness', '1', 'operating', 'WI-081 reference hollowness 0.66; 0.60 fixed by the r1 oracle scan (0.30 gave nonpositive net at every amplitude; 0.55 and 0.50 refuse at the low amplitudes; evidence/window-probe.txt).', 'As density_amplitude.'),
    axis('network_mode', P+'heat_exchangers__network_mode', '1', 'operating', 'WI-092 N1: 0 series (reviewed), 1 published series-then-parallel with the supplied split 0.85.', 'The split is a stand-in for the unmodelled branch hydraulic balance.'),
    axis('turbine_efficiency', P+'cycle__turbine_efficiency', '1', 'assumed', 'A3 0.93 (WI-089); 0.90 as the declared assumption change for the B1 explanation.', 'No turbine map.'),
]
LEVEL = {-60: (669.15, 913.15, 951.15), 0: (729.15, 973.15, 1011.15), 60: (789.15, 1033.15, 1071.15)}
KEYMAP = {a['axis']: [k['key'] for k in a['keys']] for a in AXES}
SEALED = {N: ROOT / 'exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json',
          A: ROOT / 'exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/results/cases.json'}
BASES = {name: next(r for r in json.loads(path.read_text())['cases'] if r['case'] == name)['inputs'] for name, path in SEALED.items()}
designs, aliases, seen = [], {}, {}
def add(name, base, values, cls):
    point = {k: float(v) for k, v in BASES[base].items()}
    for axis_name, value in values.items():
        for k in KEYMAP[axis_name]:
            point[k] = float(value)
    key = tuple(sorted(point.items()))
    if key in seen:
        aliases[name] = seen[key]; return
    seen[key] = name
    designs.append({'name': name, 'classification': cls, 'canonical_base': base, 'values': values})
add('N-control', N, {}, 'control: the sealed nominal-calculated point, verbatim')
add('A-control', A, {}, 'control: the sealed 891 MW alternative, verbatim')
for base, tag in ((N, 'N'), (A, 'A')):
    for rec in (0.5, 0.8, 0.95):
        for lvl in (-60, 0, 60):
            v = {'recuperation': rec, 'he_limit': LEVEL[lvl][0], 'divertor_limit': LEVEL[lvl][1], 'pbli_limit': LEVEL[lvl][2]}
            add(f'b1-{tag}-rec{rec}-lvl{lvl:+d}', base, v, f'B1 recuperation × source temperature level on the {tag} base')
for rec in (0.5, 0.95):
    for lvl in (-60, 60):
        v = {'recuperation': rec, 'he_limit': LEVEL[lvl][0], 'divertor_limit': LEVEL[lvl][1], 'pbli_limit': LEVEL[lvl][2], 'turbine_efficiency': 0.90}
        add(f'b1-N-rec{rec}-lvl{lvl:+d}-eta0.90', N, v, 'B1 corner with the turbine-efficiency assumption changed')
for flow in (2600.0, 3261.0, 3900.0):
    for mode in (0.0, 1.0):
        for rec in (0.8, 0.95):
            add(f'b2-N-flow{int(flow)}-pump{int(mode)}-rec{rec}', N, {'he_flow': flow, 'he_pump_mode': mode, 'recuperation': rec}, 'B2 helium flow × pump law × recuperation on the N base')
for amp in (4.75e20, 5.0e20, 5.5e20, 5.75e20):
    for hol in (0.66, 0.60):
        for net in (0.0, 1.0):
            add(f'b3-N-amp{amp/1e20:.2f}e20-hol{hol:.2f}-net{int(net)}', N, {'density_amplitude': amp, 'hollowness': hol, 'network_mode': net}, 'B3 density amplitude × hollowness × exchanger arrangement on the N base (window fixed after the r1 oracle scan)')
LVL = LEVEL[-60]
for flow in (3359.0, 4000.0, 4700.0):
    for mode in (1.0, 0.0):
        add(f'b2-A-flow{int(flow)}-pump{int(mode)}-rec0.95-lvl-60', A, {'he_flow': flow, 'he_pump_mode': mode, 'recuperation': 0.95, 'he_limit': LVL[0], 'divertor_limit': LVL[1], 'pbli_limit': LVL[2]}, 'B2 on the A base where the helium stage binds (rec 0.95, level −60 K): helium flow × pump law, pump capacity held at 3359')
config = {'study_id': SID,
          'question': "On the unchanged WI-092 ARIES package: (B1) does the preferred recuperator effectiveness depend on the heat-source temperature level, and does that dependence survive a lower turbine efficiency; (B2) does more blanket-helium flow buy net electricity or lower LCOE once the pump-power law and the pump capacity screen are counted, and does the answer depend on recuperation; (B3) does a change in the plasma density profile change which equipment check binds, and does the exchanger arrangement change that. Every case is a named full point composed on a sealed base; nothing is optimized; no rating is changed from demand; the reading reports main effects, the difference-of-differences interaction, ranking reversals and the limiting check per case.",
          'axes': AXES, 'designs': designs, 'aliases': aliases}
out = ROOT / 'exploration/aries_integrated/studies' / SID
out.mkdir(parents=True, exist_ok=True)
(out / 'config.json').write_text(json.dumps(config, indent=1) + '\n')
print(json.dumps({'designs': len(designs), 'aliases': aliases}))
