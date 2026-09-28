"""Author checks only. Independent reviewer must not treat this as an oracle."""
import importlib.util,json,hashlib
from pathlib import Path
p=Path(__file__).with_name('cycle-prototype.py');spec=importlib.util.spec_from_file_location('prototype',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=json.loads(p.with_name('cycle-results.json').read_text());checks={}
for c in d['cases']:
 for key in ('first_law_residual_MW','shaft_first_law_residual_MW','cooling_water_heat_closure_MW','open_heater_residual_kJ_kg'):
  assert abs(c[key])<1e-8,(c['name'],key,c[key])
 assert 0<c['bleed_fraction']<1
 assert c['states']['bleed_s']>=c['states']['main_inlet']['s']
 assert c['main']['min_gap_K']>0
 if c['reheater']:assert c['reheater']['min_gap_K']>0
 checks[c['name']]='energy/mixing/domain/positive heat approach checks passed'
errors={}
for name,table in [('main',m.M),('bleed',m.B),('condenser',m.C)]:
 for phase in ('liquid','vapor'):
  rows=sorted([r for r in table if r['phase']==phase],key=lambda r:r['T'])
  coarse=rows[::2]
  if coarse[-1]!=rows[-1]:coarse.append(rows[-1])
  errors[name+'_'+phase]={key:max(abs(m.interp(coarse,'T',r['T'],key)-r[key]) for r in rows) for key in ('h','s')}
refusals={}
for name,fn in [('steam_above_source',lambda:m.cycle('bad',Tsteam=460)),('condenser_below_source',lambda:m.cycle('bad',Tc=10))]:
 try:fn();raise AssertionError('Expected refusal')
 except ValueError as e:refusals[name]=str(e)
result={'authority':'author self-consistency, not independent verification','prototype_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':checks,'coarse_grid_reconstruction_error':errors,'refusals':refusals}
p.with_name('cycle-author-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
