"""Check captured component and combined batch statistics against engine outputs."""
import json
import math
from pathlib import Path
import numpy as np
import openmc

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
rows=[]
for path in sorted((HERE/'results').glob('*/result.json')):
 r=json.loads(path.read_text())
 batches=np.asarray(r['batch_means'])
 latest=ROOT/'.codex-test/breeding-transport/plant'/path.parent.name/f'statepoint.{len(batches)}.h5'
 with openmc.StatePoint(latest) as sp:
  tally=sp.get_tally(name='recoverable_lithium_components')
  for i,name in enumerate(['Li6','Li7']):
   assert math.isclose(r[name]['mean'],tally.mean.ravel()[i],rel_tol=1e-12)
   assert math.isclose(r[name]['std_error'],tally.std_dev.ravel()[i],rel_tol=1e-8,abs_tol=1e-12)
  diag=sp.get_tally(name='neutron_diagnostics')
  diagnostic_means=dict(zip(diag.scores,map(float,diag.mean.ravel())))
  leakage=float(sp.global_tallies['mean'][3])
  balance=1+diagnostic_means['nu-scatter']-diagnostic_means['scatter']-diagnostic_means['absorption']-leakage
  assert abs(balance)<1e-9,(path,balance)
 assert math.isclose(r['recoverable_TBR']['mean'],r['Li6']['mean']+r['Li7']['mean'],rel_tol=1e-12)
 variance=float(np.var(batches[:,0]+batches[:,1],ddof=1)/len(batches))
 assert math.isclose(r['recoverable_TBR']['std_error']**2,variance,rel_tol=1e-12)
 assert math.isclose(r['all_material_TBR']['mean']-r['recoverable_TBR']['mean'],r['nonrecoverable_TBR']['mean'],abs_tol=1e-12)
 log=path.with_name('engine.log')
 if log.exists():
  text=log.read_text().lower()
  assert 'lost particle' not in text and 'could not be located' not in text,path
 rows.append({'case':path.parent.name,'component_means_and_errors_match_OpenMC':True,'sum_covariance_checked':True,'lost_particle_warnings':False,'neutron_diagnostic_means':diagnostic_means,'leakage':leakage,'neutron_balance_mean_residual':balance})
(HERE/'tally-verification.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Verified',len(rows),'recorded cases')
