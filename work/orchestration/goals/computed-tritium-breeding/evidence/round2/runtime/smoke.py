"""Runtime plumbing check only; this toy sphere is not a scientific benchmark."""
import hashlib
import json
from pathlib import Path
import openmc
import openmc.data

ROOT = Path(__file__).resolve().parents[7]
RUNTIME = ROOT / '.codex-test/breeding-transport'
data = RUNTIME / 'data'
library = openmc.data.DataLibrary()
for path in sorted(data.glob('*.h5')):
    library.register_file(path)
library.export_to_xml(data / 'cross_sections.xml')

material = openmc.Material(name='smoke lithium')
material.add_nuclide('Li6', 0.5)
material.add_nuclide('Li7', 0.5)
material.set_density('g/cm3', 0.5)
materials = openmc.Materials([material])
materials.cross_sections = str(data / 'cross_sections.xml')
sphere = openmc.Sphere(r=30, boundary_type='vacuum')
cell = openmc.Cell(fill=material, region=-sphere)
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 10
settings.particles = 1000
settings.seed = 1739
settings.source = openmc.IndependentSource(space=openmc.stats.Point(), energy=openmc.stats.Discrete([14.1e6], [1]))
tally = openmc.Tally(name='tritium production')
tally.filters = [openmc.CellFilter(cell)]
tally.scores = ['(n,Xt)']
model = openmc.Model(geometry=openmc.Geometry([cell]), materials=materials, settings=settings, tallies=openmc.Tallies([tally]))
output = RUNTIME / 'smoke'
output.mkdir(exist_ok=True)
statepoint = model.run(cwd=output, threads=2)
with openmc.StatePoint(statepoint) as sp:
    result = sp.get_tally(name='tritium production')
    summary = dict(openmc_version=openmc.__version__, batches=10, particles_per_batch=1000, seed=1739, score='(n,Xt)', mean=float(result.mean.flat[0]), std_dev=float(result.std_dev.flat[0]), scope='runtime smoke only; not physics validation')
    assert summary['mean'] > 0
for name in ['materials.xml','geometry.xml','settings.xml','tallies.xml','model.xml']:
    path = output / name
    if path.exists():
        summary[name + '_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
(output / 'smoke.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
