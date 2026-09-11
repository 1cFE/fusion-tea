import sys,importlib.util,tempfile,shutil,json
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root));h=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('acceptance',h.parent/'implementation/run_acceptance.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from tests.model_families import MFE,materialize_canonical_subset
from sysml_codegen.cli import GenerationConfig,run_codegen
scratch=Path(tempfile.mkdtemp(prefix='wi050-audit-fixedpoint-'));models=materialize_canonical_subset(MFE,scratch/'models');package=scratch/'generated';shutil.copytree(root/'exploration/stellarator_e2e/generated',package)
before=m.hashes(package);assert run_codegen(GenerationConfig(models_path=models,output_path=package,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True));after=m.hashes(package)
assert before==after,sorted(k for k in before if before[k]!=after.get(k))
(h/'fixedpoint.json').write_text(json.dumps({'scratch':str(scratch),'files':len(before),'fixedpoint':True,'hashes':after},indent=2)+'\n');print('PASS unchanged regeneration fixed point',len(before),'files')
