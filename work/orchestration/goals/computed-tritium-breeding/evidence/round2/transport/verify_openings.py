"""Check explicit window membership and held first wall with independent angles."""
import json
import math
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from plant_transport import build

here=Path(__file__).resolve().parent
cards=json.loads((here/'material-cards.json').read_text())
rng=np.random.default_rng(33229)
report={}
for scenario in ['single','split']:
    model,manifest=build(SimpleNamespace(enrichment=.7,thickness=.8,boundary_radius=20.,batches=50,particles=2000,seed=1739,openings=scenario),cards)
    phi=rng.uniform(-math.pi,math.pi,20000)
    theta=rng.uniform(0,2*math.pi,20000)
    half=math.radians(5.4 if scenario=='single' else 2.7)
    removed=(np.abs(phi)<half)
    if scenario=='split': removed|=np.abs(np.abs(phi)-math.pi)<half
    tests=0
    for name,minor in [('breeder',185.),('reflector',235.),('ht_shield',255.),('first_wall',142.)]:
        r=1270+minor*np.cos(theta)
        for i in range(0,len(phi),10):
            point=(r[i]*math.cos(phi[i]),r[i]*math.sin(phi[i]),minor*math.sin(theta[i]))
            cell=model.geometry.find(point)[-1]
            expected=name+'_opening_void' if removed[i] and name!='first_wall' else name
            assert cell.name==expected,(scenario,point,cell.name,expected)
            tests+=1
    report[scenario]=dict(points_checked=tests,geometric_removed_fraction=.03,sampled_angle_fraction=float(removed.mean()),first_wall_retained=True,
                          removed_breeder_m3=next(x['removed_volume_cm3']/1e6 for x in manifest['layers'] if x['name']=='breeder'))
(here/'opening-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
