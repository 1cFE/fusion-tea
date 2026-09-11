"""Freeze immutable controls and comparator coverage before generating the prototype."""
import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
H = Path(__file__).resolve().parent
E = 'work/analysis/20260911-230953_radius-ownership-evidence/'
def frozen(name):
    data = subprocess.check_output(['git','show','2f8856b7:'+E+name])
    (H/('frozen-'+name)).write_bytes(data)
    return hashlib.sha256(data).hexdigest()
hashes = {n:frozen(n) for n in ['results.json','inventory.json','checks.json','source-meaning.md']}
r = json.loads((H/'frozen-results.json').read_text())
p = 'stellarator_09__stellaris__'
spec = {
    'frozen_at':datetime.now(timezone.utc).isoformat(), 'authority':'spec.md@99aee8cd',
    'source_commit':'2f8856b7', 'source_sha256':hashes,
    'baseline':'exact complete outputs, responses and report; direct additional outputs captured before generation',
    'R14':'complete tied_R14 native outputs at rel_tol=abs_tol=1e-9; exact response IDs/verdicts',
    'channels': sorted(r['cases']['baseline']['native']['outputs']),
    'response_ids': sorted(r['cases']['baseline']['native']['responses']),
    'edges': {'rb':'R_in','geom':'R_in','sustain':'R_in','divheat':'R_in','coil_length':'R0','field_calc':'R0','peak_field_calc':'R_in','magnet_cost':'R0','stored_energy':'R0'},
    'ratios': {'geom__V':14/12.7,'coil_length__c_coil':14/12.7,'field_calc__B_axis':12.7/14,'stored_energy__W_mag':12.7/14,'peak_field_calc__B_peak':(12.7-r['derived_baseline_geometry']['coil_centre'])/(14-r['derived_baseline_geometry']['coil_centre']),'magnet_cost__capital_cost':1.0},
    'invalid_R':[4.0,r['derived_baseline_geometry']['coil_centre'],3.0,0.0,-1.0],
    'component_cases':r['component'],
    'retired_key_cases':[{p+'magnet__R0':14.0},{p+'R':14.0,p+'magnet__R0':14.0},{p+'R':14.0,p+'magnet__R0':12.7},{p+'magnet__R0':0.0}],
    'contract_delta':{'remove':[['stellarator_plant_params',p+'magnet__R0']],'add':[]},
    'anchors':['magnet__R_ref','magnet__a_coil_ref','wall_peak_R_ref','R_ref_divertor'],
}
(H/'expectations.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Frozen',len(spec['channels']),'numeric outputs and',len(spec['response_ids']),'response records',spec['frozen_at'])
