"""Generate explicit optional magnet construction analyses outside the live plant DAG."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = 'optional_magnet_tea'


@pytest.fixture(scope='session')
def optional_analysis(tmp_path_factory):
    from sysml_codegen.cli import GenerationConfig, run_codegen
    work = tmp_path_factory.mktemp('optional-magnet-analysis')
    models = work / 'models'
    models.mkdir()
    for name in ('mfe_magnet_field', 'mfe_conductor_grade', 'mfe_conductor_current'):
        shutil.copyfile(ROOT / f'models/library/analyses/{name}.sysml', models / f'{name}.sysml')
    scenarios = {
        'grade': ('Conductor Field Capability', dict(B_design=24.9,B_reference=24.9,field_exponent=.6,j_reference=119.)),
        'sizing': ('Winding Pack Sizing', dict(I_coil=15400000.,j_wp=119.)),
        'stress': ('Winding Pack Stress', dict(I_coil=15400000.,B_peak_in=24.9,wp_side=.36,k_sigma=.61)),
        'field': ('Coil Set Axis Field', dict(n_coils=48.,I_coil=15400000.,k_link=.77,R0=12.7)),
        'current_sizing': ('Current Driven Pack Sizing', dict(sizing_mode=1.,inventory_multiplier=1.,legacy_effective_density=119.,I_coil=15400000.,turn_current=50000.,f_copper=.35,f_solder=.12,f_steel=.36,f_helium=.08,tape_width=.006,tape_thickness=.000056,B_peak=24.,temperature=20.,reference_tape_current=200.,material_factor=1.,orientation_factor=1.,cabling_factor=1.,degradation_factor=1.,sharing_factor=1.,allowable_fraction=.8,allow_field_extrapolation=0.)),
    }
    text = 'package optional_magnet {\n private import ScalarValues::*;\n private import mfe_magnet_field::*;\n private import mfe_conductor_grade::*;\n private import mfe_conductor_current::*;\n part proposal {\n'
    for name, (definition, inputs) in scenarios.items():
        text += f" calc {name} : '{definition}' {{\n"
        text += ''.join(f'  in {key} = {value!r};\n' for key,value in inputs.items())
        text += ' }\n'
    text += ' }\n}\n'
    (models/'optional_magnet.sysml').write_text(text)
    output = work / PACKAGE
    receipt = json.loads((ROOT/'work/active/WI-075_supplied-magnet-design-evaluation/integration/candidate-seeds.json').read_text())
    for folder, name in (('mfe_conductor_grade','conductor_field_capability'),('mfe_conductor_current','current_driven_pack_sizing'),('mfe_magnet_field','winding_pack_sizing'),('mfe_magnet_field','winding_pack_stress')):
        rel = f'handwritten/{folder}/{name}_impl.py'
        src = ROOT/'exploration/stellarator_e2e/generated'/rel
        assert hashlib.sha256(src.read_bytes()).hexdigest() == receipt[rel]
        dest = output/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(src.read_text().replace('stellarator_tea.',PACKAGE+'.'))
    assert run_codegen(GenerationConfig(models_path=models,output_path=output,package_name=PACKAGE,overwrite=True,preserve_handwritten=True,smart_regen=True))
    paths = [str(work)]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
    for path in paths: sys.path.insert(0,path)
    importlib.invalidate_caches()
    yield output
    for path in paths: sys.path.remove(path)
