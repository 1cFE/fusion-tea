import json, sys
from pathlib import Path
ROOT = Path('/home/reid/1cfe/fusion-tea'); sys.path.insert(0, str(ROOT))
from exploration.aries_integrated.studies import oracle_entry
P = 'aries_integrated_plant__'; Q = 'aries_cs_plasma_integration__plasma__'
rows = json.loads((ROOT / 'exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json').read_text())['cases']
base = {k: float(v) for k, v in next(r for r in rows if r['case'] == 'nominal-calculated')['inputs'].items()}
A = json.loads((ROOT / 'exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/results/cases.json').read_text())['cases']
abase = {k: float(v) for k, v in next(r for r in A if r['case'] == 'resized-compressor-1700-network-scaledflows-0.85')['inputs'].items()}
def probe(pt):
    try:
        v = oracle_entry.evaluate(pt)
        return {'fus': round(v[P+'source__evaluate__selected_power'], 1), 'net': round(v[P+'plant_ledger__evaluate__net_electric'], 1), 'unmet': round(v[P+'heat_exchangers__evaluate__unmet_heat'], 1), 'ext_t': round(v[P+'fuel_inventory__annual__annual_external'], 1)}
    except Exception as e:
        return {'refused': str(e)[:60]}
print('--- B3 window probe on N (oracle only)')
for amp in (4.5e20, 4.75e20, 5.0e20, 5.25e20, 5.5e20, 5.75e20):
    for hol in (0.66, 0.6, 0.55, 0.5):
        for net in (0.0,):
            pt = dict(base); pt[Q+'amplitude'] = amp; pt[Q+'hollowness'] = hol; pt[P+'heat_exchangers__network_mode'] = net
            print(f'amp {amp/1e20:.2f}e20 hol {hol} net {int(net)}:', probe(pt))
print('--- B2 binding probe on A at rec 0.95, level -60 (oracle only)')
for flow in (3359.0, 4000.0, 4700.0):
    for mode in (1.0, 0.0):
        pt = dict(abase); pt[P+'cycle__recuperator_effectiveness'] = 0.95
        for k, v in ((P+'heat_exchangers__he_limit', 669.15), (P+'heat_exchangers__divertor_limit', 913.15), (P+'heat_exchangers__pbli_limit', 951.15)): pt[k] = v
        pt[P+'heat_exchangers__he_flow'] = flow; pt[P+'he_pump__pump_mode'] = mode
        print(f'flow {flow} mode {int(mode)}:', probe(pt))
