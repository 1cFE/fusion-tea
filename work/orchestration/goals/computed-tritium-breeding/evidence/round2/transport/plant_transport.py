"""Declared toroidal HCLL prototype; run with round2/runtime/run.

This executable writes evidence only. It does not change the production model.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import time
from pathlib import Path

import numpy as np
import openmc

ROOT = Path(__file__).resolve().parents[7]
RUNTIME = ROOT / '.codex-test/breeding-transport'
DATA = RUNTIME / 'data/cross_sections.xml'


def constituent(name, card, enrichment):
    m = openmc.Material(name=name)
    m.temperature = card['temperature_K']
    if card['density_g_cm3'] is None:
        raise ValueError(f'{name}: unresolved density authority')
    m.set_density('g/cm3', card['density_g_cm3'])
    kind = {'atomic':'ao','weight':'wo'}[card['composition_basis']]
    if not math.isclose(sum(card['composition'].values()),1,abs_tol=1e-10):
        raise ValueError(f'{name}: fractions do not sum to one')
    for element, fraction in card['composition'].items():
        if re.search(r'\d',element):
            m.add_nuclide(element,fraction,kind)
            continue
        natural = {n:f for n,f in openmc.data.NATURAL_ABUNDANCE.items() if re.sub(r'\d+$','',n)==element}
        if not natural:
            raise ValueError(f'No natural-abundance expansion for {element}')
        denominator = sum(f*(openmc.data.atomic_mass(n) if kind=='wo' else 1) for n,f in natural.items())
        for n,f in natural.items():
            isotope_fraction = f*(openmc.data.atomic_mass(n) if kind=='wo' else 1)/denominator
            m.add_nuclide(n,fraction*isotope_fraction,kind)
    if name == 'PbLi':
        n_li = sum(d.percent for d in m.nuclides if d.name.startswith('Li'))
        if not n_li:
            raise ValueError('PbLi card must contain explicit atomic lithium')
        if any(d.percent_type != 'ao' for d in m.nuclides):
            raise ValueError('PbLi requires atom fractions')
        for n in list(m.get_nuclides()):
            if n.startswith('Li'):
                m.remove_nuclide(n)
        m.add_nuclide('Li6', n_li*enrichment, 'ao')
        m.add_nuclide('Li7', n_li*(1-enrichment), 'ao')
    return m


def build(args, cards):
    openmc.reset_auto_ids()
    openmc.config['cross_sections'] = str(DATA)
    constituents = {n: constituent(n, c, args.enrichment) for n,c in cards['constituents'].items()}
    mixtures = {}
    for n, card in cards['mixtures_volume_fractions'].items():
        ingredients = list(card)
        fractions = list(card.values())
        if not math.isclose(sum(fractions), 1, abs_tol=1e-12):
            raise ValueError(f'{n}: invalid volume fractions')
        m = openmc.Material.mix_materials([constituents[x] for x in ingredients], fractions, 'vo', name=n)
        temperatures = {constituents[x].temperature for x in ingredients}
        if len(temperatures)!=1:
            raise ValueError(f'{n}: mixture constituents have different physical temperatures')
        m.temperature = temperatures.pop()
        mixtures[n] = m
    materials_by_name = constituents | mixtures
    # metres; source assembly geometry is circular-average, not shaped stellarator CAD.
    layers = [('plasma',1.3,None), ('plasma_gap',.1,None), ('armor',.002,'W'),
              ('first_wall',.048,'first_wall_bulk'), ('breeder',args.thickness,'breeder'),
              ('reflector',.2,'reflector'), ('ht_shield',.2,'ht_shield'),
              ('structure',.15,'SS316'), ('assembly_gap',.1,None), ('vessel',.1,'vessel')]
    if getattr(args,'external_steel',False):
        layers += [('external_gap',.1,None),('external_steel',.2,'SS316')]
    R = 12.7
    cells, inventory = [], []
    previous, radius = None, 0.
    for name, thickness, material in layers:
        inner = radius
        radius += thickness
        surface = openmc.ZTorus(a=100*R,b=100*radius,c=100*radius,name=name+'_outer')
        region = -surface if previous is None else +previous & -surface
        cell = openmc.Cell(name=name,fill=materials_by_name[material] if material else None,region=region)
        cell.volume = 2*math.pi**2*R*(radius**2-inner**2)*1e6
        cells.append(cell)
        inventory.append(dict(cell_id=cell.id,name=name,inner_m=inner,outer_m=radius,volume_cm3=cell.volume,material=material))
        previous = surface
    outer = openmc.Sphere(r=args.boundary_radius*100,boundary_type='vacuum',name='convex_outer_vacuum')
    if args.boundary_radius <= R+radius:
        raise ValueError('Enclosing sphere must contain complete torus')
    cells.append(openmc.Cell(name='exterior_void',region=+previous & -outer))
    openings = getattr(args,'openings','none')
    if openings != 'none':
        centers = [0.] if openings == 'single' else [0.,math.pi]
        half_width = math.radians(5.4 if openings=='single' else 2.7)
        windows = None
        for center in centers:
            lo,hi=center-half_width,center+half_width
            bottom=openmc.Plane(a=-math.sin(lo),b=math.cos(lo),c=0,d=0)
            top=openmc.Plane(a=-math.sin(hi),b=math.cos(hi),c=0,d=0)
            window=+bottom & -top
            windows=window if windows is None else windows | window
        for cell in list(cells):
            if cell.name in ('breeder','reflector','ht_shield'):
                removed=cell.region & windows
                cell.region=cell.region & ~windows
                nominal=cell.volume
                cell.volume=nominal*.97
                cells.append(openmc.Cell(name=cell.name+'_opening_void',region=removed))
                entry=next(x for x in inventory if x['name']==cell.name)
                entry.update(nominal_volume_cm3=nominal,removed_volume_cm3=nominal*.03,volume_cm3=cell.volume)
    used = list({c.fill.id:c.fill for c in cells if c.fill is not None}.values())
    materials = openmc.Materials(used)
    materials.cross_sections = str(DATA)
    available = openmc.data.DataLibrary.from_xml(DATA)
    missing = sorted({n for m in used for n in m.get_nuclides() if available.get_by_material(n) is None})
    if missing:
        raise ValueError(f'Missing nuclide data: {missing}')
    settings = openmc.Settings()
    settings.run_mode = 'fixed source'
    settings.batches = args.batches
    settings.particles = args.particles
    settings.seed = args.seed
    settings.temperature = {'method':'interpolation', 'range':(250.,1200.)}
    settings.source = openmc.IndependentSource(
        space=openmc.stats.CylindricalIndependent(openmc.stats.PowerLaw(1140.,1400.,1),openmc.stats.Uniform(0,2*math.pi),openmc.stats.Uniform(-130,130)),
        angle=openmc.stats.Isotropic(),energy=openmc.stats.Discrete([14.06e6],[1.]),strength=1.,
        constraints={'domains':[cells[0]],'rejection_strategy':'resample'})
    settings.statepoint = {'batches':list(range(1,args.batches+1))}
    settings.sourcepoint = {'write':False}
    settings.output = {'summary':False,'tallies':False}
    breeder = next(c for c in cells if c.name=='breeder')
    lithium = openmc.Tally(name='recoverable_lithium_components')
    lithium.filters = [openmc.CellFilter(breeder)]
    lithium.nuclides = ['Li6','Li7']
    lithium.scores = ['(n,Xt)']
    all_t = openmc.Tally(name='all_material_tritium')
    all_t.scores = ['(n,Xt)']
    breeder_t = openmc.Tally(name='all_breeder_tritium')
    breeder_t.filters = [openmc.CellFilter(breeder)]
    breeder_t.scores = ['(n,Xt)']
    diagnostics = openmc.Tally(name='neutron_diagnostics')
    diagnostics.scores = ['absorption','nu-scatter','scatter']
    model = openmc.Model(geometry=openmc.Geometry(cells), materials=materials, settings=settings,
                         tallies=openmc.Tallies([lithium,all_t,breeder_t,diagnostics]))
    manifest = {'major_radius_m':R,'plasma_minor_radius_m':1.3,'openings':openings,'layers':inventory,
        'materials':[{ 'name':m.name,'temperature_K':m.temperature,'density_g_cm3':m.get_mass_density(),
                       'atom_density_b_cm':{n:float(v) for n,v in m.get_nuclide_atom_densities().items()}} for m in used]}
    return model, manifest


def read_batches(output, batches):
    previous = np.zeros(4)
    observations = []
    for b in range(1,batches+1):
        with openmc.StatePoint(output/f'statepoint.{b:0{len(str(batches))}d}.h5') as sp:
            li = sp.get_tally(name='recoverable_lithium_components')
            total = sp.get_tally(name='all_material_tritium')
            breeder = sp.get_tally(name='all_breeder_tritium')
            current = np.array([*li.sum.ravel(),total.sum.item(),breeder.sum.item()])
        observations.append(current-previous)
        previous = current
    a = np.asarray(observations)
    useful = a[:,0]+a[:,1]
    nonrecoverable = a[:,2]-useful
    def stats(x):
        return {'mean':float(np.mean(x)),'std_error':float(np.std(x,ddof=1)/math.sqrt(len(x)))}
    return {'Li6':stats(a[:,0]),'Li7':stats(a[:,1]),'recoverable_TBR':stats(useful),
            'all_material_TBR':stats(a[:,2]),'nonrecoverable_TBR':stats(nonrecoverable),
            'breeder_nonlithium_TBR':stats(a[:,3]-useful),
            'batch_columns':['Li6','Li7','all_material','all_breeder'],
            'batch_means':a.tolist(),'Li6_Li7_batch_covariance':float(np.cov(a[:,:2],rowvar=False)[0,1])}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cards',type=Path,required=True)
    p.add_argument('--thickness',type=float,default=.8)
    p.add_argument('--enrichment',type=float,default=.7)
    p.add_argument('--batches',type=int,default=50)
    p.add_argument('--particles',type=int,default=2000)
    p.add_argument('--seed',type=int,default=1739)
    p.add_argument('--boundary-radius',type=float,default=20.)
    p.add_argument('--openings',choices=['none','single','split'],default='none')
    p.add_argument('--external-steel',action='store_true')
    p.add_argument('--source-profile',choices=['uniform','peaked'],default='uniform')
    p.add_argument('--name',required=True)
    p.add_argument('--export-only',action='store_true')
    args=p.parse_args()
    if not (0 < args.enrichment <= 1 and args.thickness > 0 and args.batches >= 2 and args.particles > 0):
        raise ValueError('Invalid parameter domain')
    out=RUNTIME/'plant'/args.name
    out.mkdir(parents=True,exist_ok=False)
    cards=json.loads(args.cards.read_text())
    model,manifest=build(args,cards)
    if args.source_profile=='peaked':
        from peaked_source import write
        source_path=(out/'peaked-source.h5').resolve()
        manifest['source_bank']=write(source_path,args.seed+70000000)
        model.settings.source=openmc.FileSource(source_path)
    model.export_to_model_xml(out/'model.xml')
    manifest['cards_sha256']=hashlib.sha256(args.cards.read_bytes()).hexdigest()
    manifest['builder_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest['cross_sections_index_sha256']=hashlib.sha256(DATA.read_bytes()).hexdigest()
    manifest['data_manifests_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).parent.parent/'runtime/data-manifest.json',Path(__file__).parent/'data-manifest-extra.json']}
    manifest['model_xml_sha256']=hashlib.sha256((out/'model.xml').read_bytes()).hexdigest()
    manifest['arguments']={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.export_only:
        print(out)
        return
    begin=time.monotonic()
    model.run(cwd=out,threads=2)
    result=read_batches(out,args.batches)
    result.update(wall_seconds=time.monotonic()-begin,histories=args.batches*args.particles,
                  manifest_sha256=hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest(),
                  status='unvalidated physical prototype; not an adequacy verdict')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='batch_means'},indent=2))


if __name__=='__main__':
    main()
