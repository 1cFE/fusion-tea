import json,os,subprocess,sys,shutil
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight
H=Path(__file__).resolve().parents[1];R=H/'results'
p=route.prepare(route.PACKAGE_DIR,R/'_runtime')
entry={k:{'class':v.__module__+'.'+v.__qualname__,'schema':v.model_json_schema()} for k,v in p.entry_models.items()}
(R/'entry-models.json').write_text(json.dumps(entry,indent=2)+'\n')
shutil.copyfile(route.spec_path(route.PACKAGE_DIR),H/'context/pipeline.yaml')
for name in ['mfe_plasma_sustainment.sysml','mfe_power_balance.sysml']:
 shutil.copyfile(Path('models/library/analyses')/name,H/'context'/name)
rt={'python':sys.version,'python_executable':sys.executable,'teax_root':os.environ['STOP_PARSER_TEAX_ROOT'],'teax_revision':subprocess.check_output(['git','-C',os.environ['STOP_PARSER_TEAX_ROOT'],'rev-parse','HEAD'],text=True).strip(),'repo_revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'launcher':'.codex-test/run','pythonpath':'$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit','STUDY_REQUIRE_TEAX':'1','era_pin':None,'no_dependency_installation':True}
(R/'runtime.json').write_text(json.dumps(rt,indent=2)+'\n')
clean=preflight.run_clean(route.PACKAGE_DIR);(R/'post-verification-clean.json').write_text(json.dumps(clean,indent=2)+'\n');assert clean['outcome']=='pass'
print('Captured',len(entry),'entry models and runtime; package clean')
