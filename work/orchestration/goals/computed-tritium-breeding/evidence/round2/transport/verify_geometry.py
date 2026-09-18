"""Random-volume and actual CSG ownership checks against toroidal shell identities."""
import argparse
import json
import math
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from plant_transport import build

p=argparse.ArgumentParser();p.add_argument('--cards',type=Path,required=True);args=p.parse_args()
model,manifest=build(SimpleNamespace(enrichment=.7,thickness=.8,boundary_radius=20.,batches=50,particles=2000,seed=1739),json.loads(args.cards.read_text()))
R=1270.; outer=300.; N=2_000_000
rng=np.random.default_rng(90210)
r=np.sqrt((R-outer)**2+rng.random(N)*((R+outer)**2-(R-outer)**2))
z=rng.uniform(-outer,outer,N)
minor=np.sqrt((r-R)**2+z*z)
volume=math.pi*((R+outer)**2-(R-outer)**2)*2*outer
rows=[]
for layer in manifest['layers']:
 mask=(minor>=100*layer['inner_m'])&(minor<100*layer['outer_m'])
 fraction=float(mask.mean()); estimate=fraction*volume; se=volume*math.sqrt(fraction*(1-fraction)/N)
 exact=layer['volume_cm3']
 rows.append(dict(name=layer['name'],analytic_cm3=exact,sampled_cm3=estimate,standard_error_cm3=se,standardized_residual=(estimate-exact)/se))
 assert abs(estimate-exact)<5*se,layer['name']
 # Check actual CSG ownership on independently chosen interior samples.
 indices=np.flatnonzero(mask)[::max(1,int(mask.sum()/100))][:100]
 phi=rng.uniform(0,2*math.pi,len(indices))
 for i,angle in zip(indices,phi):
  point=(r[i]*math.cos(angle),r[i]*math.sin(angle),z[i])
  path=model.geometry.find(point)
  assert path[-1].name==layer['name'],(point,path)
# Central hole and exterior void are retained, including far-side return paths.
for point in [(0,0,0),(1600,0,0),(0,0,1000)]:
 assert model.geometry.find(point)[-1].name=='exterior_void'
report=dict(candidate_samples=N,layers=rows,csg_ownership='PASS',central_hole_void='PASS')
Path(__file__).with_name('geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
