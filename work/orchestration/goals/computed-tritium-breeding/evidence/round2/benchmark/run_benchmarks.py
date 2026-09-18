"""Approximate OKTAVIAN integral checks; assumptions frozen in preexecution.md."""
import hashlib
import json
import math
from pathlib import Path
import openmc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
DATA = ROOT / '.codex-test/breeding-transport/data/cross_sections.xml'

def run(assembly, label, energy=14.1e6, li_density=0.534, li6=0.0759, casing=0.0, seed=981731):
    out = HERE / 'runs' / f'{assembly}_{label}'
    out.mkdir(parents=True, exist_ok=True)
    result_path = out / 'result.json'
    if result_path.exists():
        return json.loads(result_path.read_text())
    openmc.reset_auto_ids()
    li = openmc.Material(name='natural lithium approximation', temperature=294)
    li.add_nuclide('Li6', li6); li.add_nuclide('Li7', 1-li6)
    li.set_density('g/cm3', li_density)
    pb = openmc.Material(name='natural lead approximation', temperature=294)
    for isotope, fraction in [('Pb204',.014),('Pb206',.241),('Pb207',.221),('Pb208',.524)]:
        pb.add_nuclide(isotope,fraction)
    pb.set_density('g/cm3',11.34)
    steel = openmc.Material(name='illustrative Fe Cr Ni casing',temperature=294)
    for element,fraction in [('Fe',.70),('Cr',.19),('Ni',.11)]:
        steel.add_element(element,fraction,percent_type='wo')
    steel.set_density('g/cm3',8)
    radius_inner = 10 if assembly == 'Li' else 20
    inner = openmc.Sphere(r=radius_inner)
    outer = openmc.Sphere(r=60,boundary_type='vacuum')
    cells=[]
    if assembly == 'PbLi':
        cavity=openmc.Sphere(r=10)
        cells += [openmc.Cell(region=-cavity),openmc.Cell(fill=pb,region=+cavity & -inner)]
    else:
        cells.append(openmc.Cell(region=-inner))
    if casing:
        in_li=openmc.Sphere(r=radius_inner+casing)
        out_li=openmc.Sphere(r=60-casing)
        cells += [openmc.Cell(fill=steel,region=+inner & -in_li),openmc.Cell(fill=steel,region=+out_li & -outer)]
    else:
        in_li,out_li=inner,outer
    breeder=openmc.Cell(fill=li,region=+in_li & -out_li)
    cells.append(breeder)
    settings=openmc.Settings()
    settings.run_mode='fixed source'; settings.particles=10000; settings.batches=40
    settings.seed=seed
    settings.source=openmc.IndependentSource(space=openmc.stats.Point(),angle=openmc.stats.Isotropic(),energy=openmc.stats.Discrete([energy],[1]))
    tally=openmc.Tally(name='breeder tritium')
    tally.filters=[openmc.CellFilter(breeder)]
    tally.nuclides=['Li6','Li7','total']; tally.scores=['(n,Xt)']
    materials=openmc.Materials([li]+([pb] if assembly=='PbLi' else [])+([steel] if casing else []))
    materials.cross_sections=str(DATA)
    model=openmc.Model(geometry=openmc.Geometry(cells),materials=materials,settings=settings,tallies=openmc.Tallies([tally]))
    sp_path=model.run(cwd=out,threads=2,output=False)
    with openmc.StatePoint(sp_path) as sp:
        t=sp.get_tally(name='breeder tritium')
        means=t.mean.reshape(-1); std=t.std_dev.reshape(-1)
        result=dict(assembly=assembly,case=label,energy_eV=energy,li_density_g_cm3=li_density,li6_atom_fraction=li6,casing_cm=casing,seed=seed,histories=400000,Li6=float(means[0]),Li7=float(means[1]),total=float(means[2]),std_dev=float(std[2]),isotope_sum_error=float(means[0]+means[1]-means[2]),openmc_version=openmc.__version__)
        exp,rsd=(.685,.056) if assembly=='Li' else (.530,.060)
        result.update(experiment=exp,experiment_rsd=rsd,C_over_E=result['total']/exp,z_diagnostic=(result['total']-exp)/math.sqrt((exp*rsd)**2+result['std_dev']**2))
    result['artifacts_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in {'.xml','.h5'}}
    result_path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result

if __name__=='__main__':
    cases=[('baseline',{}),('repeat',{'seed':78131}),('energy14',{'energy':14e6}),('energy14p8',{'energy':14.8e6}),('density050',{'li_density':.50}),('density056',{'li_density':.56}),('li6_074',{'li6':.074}),('li6_080',{'li6':.080}),('casing02',{'casing':.2})]
    results=[run(assembly,label,**params) for assembly in ['Li','PbLi'] for label,params in cases]
    (HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
