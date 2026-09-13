"""Regenerate current documentation-bearing packages without changing executable bodies."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from tests.model_families import FAMILIES
from preservation import PACKAGES,inventory
from sysml_codegen.cli import GenerationConfig,run_codegen
before=json.loads((HERE/'entering.json').read_text())
for name,family in FAMILIES.items():
    package=PACKAGES[name]
    handwritten={p: h for p,h in before['packages'][name]['hashes'].items() if p.startswith('handwritten/')}
    for smart in (False,True):
        old=inventory(package)
        assert run_codegen(GenerationConfig(models_path=family.twin,output_path=package,package_name={'ife':'ife_tea','mfe':'stellarator_tea'}[name],overwrite=True,preserve_handwritten=True,smart_regen=smart))
        new=inventory(package)
        assert all(new[p]==h for p,h in handwritten.items()), name+' handwritten changed'
        if smart:assert new==old,name+' repeated generation drift'
    print('PASS',name,'all handwritten bodies preserved; second generation byte-stable')
