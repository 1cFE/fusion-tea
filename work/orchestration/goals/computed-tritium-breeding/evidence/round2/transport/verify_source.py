"""Independent checks of exact uniform-volume toroidal source sampling."""
import json
import math
from pathlib import Path
import numpy as np
import openmc

N=1_000_000
R=1270.
a=130.
r=openmc.stats.PowerLaw(R-a,R+a,1).sample(N,seed=918)
z=openmc.stats.Uniform(-a,a).sample(N,seed=919)
phi=openmc.stats.Uniform(0,2*math.pi).sample(N,seed=920)
mask=(r-R)**2+z**2<a*a
r,z,phi=r[mask],z[mask],phi[mask]
variables={'z':(z,0.),'z_squared':(z*z,a*a/4), 'cylindrical_radius':(r,R+a*a/(4*R)),
           'minor_radius_squared':((r-R)**2+z*z,a*a/2)}
report={'candidate_samples':N,'accepted_samples':len(r),'acceptance':len(r)/N,'expected_acceptance':math.pi/4,'moments':{}}
for name,(values,expected) in variables.items():
 mean=float(values.mean()); se=float(values.std(ddof=1)/math.sqrt(len(values)))
 report['moments'][name]={'mean':mean,'expected':expected,'standard_error':se,'standardized_residual':(mean-expected)/se}
 assert abs(mean-expected)<5*se,name
# Independent region membership check through the actual ZTorus surface implementation.
surface=openmc.ZTorus(a=R,b=a,c=a)
points=np.column_stack((r*np.cos(phi),r*np.sin(phi),z))
assert all(surface.evaluate(tuple(p))<1e-12 for p in points[::100])
report['sampled_surface_membership']='PASS'
Path(__file__).with_name('source-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
