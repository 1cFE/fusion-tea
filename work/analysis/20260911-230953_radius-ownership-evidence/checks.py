"""Independent geometry identities and a temporary oracle-input isolation experiment.

Uses retained native outputs. No source/package mutation; restores oracle globals.
"""
import json,math,sys
from pathlib import Path
ROOT=Path.cwd(); HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
import oracle_entry as oracle
r=json.loads((HERE/'results.json').read_text()); P='stellarator_09__stellaris__'; inputs=r['inputs']
def same(a,b): assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b)
checks={}; b=r['cases']['baseline']['native']['outputs']
for name in ['baseline','plant_only_R14','magnet_only_R14','tied_R14']:
 c=r['cases'][name]; i=inputs|c['changes']; o=c['native']['outputs']; R=i[P+'R']; Rm=i[P+'magnet__R0']
 same(o[P+'geom__V']/b[P+'geom__V'],R/12.7)
 same(o[P+'field_calc__B_axis']/b[P+'field_calc__B_axis'],12.7/Rm)
 same(o[P+'coil_length__c_coil']/b[P+'coil_length__c_coil'],Rm/12.7)
 same(o[P+'stored_energy__W_mag']/b[P+'stored_energy__W_mag'],12.7/Rm)
 same(o[P+'magnet_cost__capital_cost'],b[P+'magnet_cost__capital_cost'])
 bore=r['derived_baseline_geometry']['coil_centre']; same(o[P+'peak_field_calc__B_peak'],b[P+'peak_field_calc__B_peak']*(12.7-bore)/(Rm-bore))
 checks[name]={'geometry_identities':'pass','conductor_procurement_invariance':'pass'}
# Isolate the single incorrect radius operand in the independent oracle. Field B
# is already calculated and passed in; change only the local sustainment input.
saved=oracle.vs._sustainment
try:
 def corrected(p,V,B): return saved(dict(p,magnet_R0=p['R']),V,B)
 oracle.vs._sustainment=corrected
 for name in ['baseline','plant_only_R14','magnet_only_R14','tied_R14']:
  c=r['cases'][name]; out=oracle.evaluate(c['changes']); native=c['native']['outputs']
  differences={k:{'native':native[k],'oracle':v} for k,v in out.items() if k in native and not math.isclose(native[k],v,rel_tol=1e-9,abs_tol=1e-9)}
  assert not differences,differences
  checks[name]['isolated_oracle_R_fix']='all published shared channels match'; checks[name]['compared_channels']=len([k for k in out if k in native])
finally: oracle.vs._sustainment=saved
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
