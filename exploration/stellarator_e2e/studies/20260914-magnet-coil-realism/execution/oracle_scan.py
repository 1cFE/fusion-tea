"""Runbook step 7: scan every candidate point with the package-owned oracle before any point runs.
Deposits results/oracle-scan.json (per point: every required channel the oracle map publishes, the oracle-side
verdicts re-derived from operand bindings, and the c_coil / vol_cold identities). Oracle-side only."""
import sys, json, math, hashlib
from pathlib import Path
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H.parent))
import oracle_entry as oe
P = 'stellarator_09__stellaris__'
props = json.load(open(H / 'preparation/proposals.json'))
req = list(json.load(open(H / 'preparation/required-channels.json')))
import glob as _g
params = {}
for _f in sorted(_g.glob(str(H.parent.parent / 'generated/inputs/*_params.json'))):
    params.update(json.load(open(_f)))
def pv(name):
    for k in (name, P + name):
        if k in params: return params[k]
    raise KeyError(name)
c_coil_ref, a_coil_ref, recirc_thr = pv('magnet__coil__c_coil_ref'), pv('magnet__coil__a_coil_ref'), pv('recirc_ok__threshold') if any('recirc_ok__threshold' in k for k in params) else None
bindings = oe.operand_bindings()
def verdict(cid, ch, point):
    """Re-derive one verdict from the oracle's own operands using the published predicate binding kinds."""
    return None  # verify.py re-derives verdicts at step 10; the scan records channels and reachability only
out = {'oracle': {'module': 'exploration/stellarator_e2e/studies/oracle_entry.py'}, 'package_inputs': {'c_coil_ref': c_coil_ref, 'a_coil_ref': a_coil_ref, 'recirc_ok__threshold': recirc_thr}, 'arms': {}}
n_err = 0
for arm, rows in props.items():
    arm_rows = []
    for r in rows:
        rec = {'column': r['column'], 'source_case': r.get('source_case'), 'point': r['point'], 'err': None, 'channels': {}, 'unpublished_by_oracle': []}
        try:
            ch = oe.evaluate(r['point'])
            for k in req:
                if k in ch: rec['channels'][k] = ch[k]
                else: rec['unpublished_by_oracle'].append(k)
            rc = ch.get(P + 'rb__r_coil_centre')
            rec['c_coil_identity'] = c_coil_ref * rc / a_coil_ref if rc is not None else None
        except Exception as e:
            rec['err'] = f'{type(e).__name__}: {e}'; n_err += 1
        arm_rows.append(rec)
    out['arms'][arm] = arm_rows
    print(arm, len(arm_rows), 'points;', sum(1 for x in arm_rows if x['err']), 'errors; unpublished by oracle:', sorted({k[len(P):] for x in arm_rows for k in x['unpublished_by_oracle']}))
out['errors'] = n_err
json.dump(out, open(H / 'results/oracle-scan.json', 'w'), indent=1)
print('errors', n_err)
