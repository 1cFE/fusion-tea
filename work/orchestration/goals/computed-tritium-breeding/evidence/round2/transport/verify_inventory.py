"""Check mixture atom densities against direct constituent-volume addition."""
import json
import math
from pathlib import Path
from types import SimpleNamespace
import openmc.data
from plant_transport import build,constituent

here=Path(__file__).resolve().parent
cards=json.loads((here/'material-cards.json').read_text())
args=SimpleNamespace(enrichment=.7,thickness=.8,boundary_radius=20.,batches=50,particles=2000,seed=1739,openings='single')
model,manifest=build(args,cards)
by_name={m.name:m for m in model.materials}
constituents={name:constituent(name,card,.7) for name,card in cards['constituents'].items()}
report={}
for name,fracs in cards['mixtures_volume_fractions'].items():
 if name not in by_name:continue
 expected={}
 for n,f in fracs.items():
  for isotope,density in constituents[n].get_nuclide_atom_densities().items():
   expected[isotope]=expected.get(isotope,0)+f*density
 actual=by_name[name].get_nuclide_atom_densities()
 assert set(actual)==set(expected)
 worst=max(abs(actual[n]-expected[n])/expected[n] for n in actual)
 assert worst<1e-12,(name,worst)
 mass=sum(fracs[n]*cards['constituents'][n]['density_g_cm3'] for n in fracs)
 assert math.isclose(by_name[name].get_mass_density(),mass,rel_tol=1e-12)
 report[name]={'nuclides':len(actual),'density_g_cm3':mass,'max_relative_atom_density_residual':worst}
pbli=constituents['PbLi'].get_nuclide_atom_densities()
f=pbli['Li6']/(pbli['Li6']+pbli['Li7'])
assert math.isclose(f,.7,abs_tol=1e-14)
report['PbLi_Li6_atom_fraction']=f
report['breeder_isotope_inventory_atoms']={n:float(d*1e24*next(x['volume_cm3'] for x in manifest['layers'] if x['name']=='breeder')) for n,d in by_name['breeder'].get_nuclide_atom_densities().items()}
(here/'inventory-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='breeder_isotope_inventory_atoms'})
