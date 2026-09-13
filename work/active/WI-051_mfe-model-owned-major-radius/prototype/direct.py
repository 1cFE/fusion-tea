"""Capture pre-repair raw controls, then exercise isolated copies of both direct callers."""
import hashlib, importlib, json, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=Path.cwd(); P='stellarator_09__stellaris__'
mode=sys.argv[1]; entering=mode=='entering'; dest=H/('direct-'+mode); dest.mkdir(exist_ok=True)
source=ROOT/'exploration/stellarator_e2e'
for name in ['run_stellaris.py','run_stellaris_single.py','verify_stellaris.py']: shutil.copyfile(source/name,dest/name)
pkg=source/'generated' if entering else H/'generated'
if not (dest/'generated').exists(): (dest/'generated').symlink_to(pkg)
if not entering:
    f=dest/'run_stellaris.py'; s=f.read_text().replace('def run_pipeline(tag):','def run_pipeline(tag, *, pipeline_path=None, output_dir=None):').replace('create_output_router_with_json_schemas(["RootModel[float]"])','create_output_router_with_json_schemas(["RootModel[float]"] + [s.__name__ for s in CUSTOM_SCHEMA_TYPES])').replace('        PIPELINE,','        pipeline_path or PIPELINE,').replace('output_dir=E2E / "outputs" / tag,','output_dir=output_dir or E2E / "outputs" / tag,').replace('for c, v in result.outputs.items()}','for c, v in result.outputs.items()\n            if hasattr(v, "root") or isinstance(v, (int, float))}')
    f.write_text(s)
    f.write_text(f.read_text().replace('["RootModel[float]"] + [s.__name__ for s in CUSTOM_SCHEMA_TYPES]', 'list(dict.fromkeys(["RootModel[float]"] + [s.__name__ for s in CUSTOM_SCHEMA_TYPES]))'))
    f=dest/'run_stellaris_single.py'; f.write_text(f.read_text().replace('def _execute_package():','def _execute_package(*, pipeline_path=None, output_dir=None):').replace('        rs.PIPELINE,','        pipeline_path or rs.PIPELINE,').replace('output_dir=rs.E2E / "outputs" / "single",','output_dir=output_dir or rs.E2E / "outputs" / "single",'))
    f.write_text(f.read_text().replace('    raise SystemExit(main())', '    if len(sys.argv) != 1:\n        raise SystemExit("Unsupported command-line arguments: " + " ".join(sys.argv[1:]))\n    raise SystemExit(main())'))
sys.path.insert(0,str(dest)); rs=importlib.import_module('run_stellaris'); single=importlib.import_module('run_stellaris_single')
e=json.loads((H/'expectations.json').read_text()); frozen=json.loads((H/'frozen-results.json').read_text())
cases={'baseline':{},'R14':{P+'R':14.0,**({P+'magnet__R0':14.0} if entering else {})}}
if not entering:
    cases.update({f'retired_{i}':v for i,v in enumerate(e['retired_key_cases'])})
    cases.update({f'invalid_{i}':{P+'R':v} for i,v in enumerate(e['invalid_R'])})
results={}
for name,change in cases.items():
    scratch=dest/name; (scratch/'pipelines').mkdir(parents=True,exist_ok=True)
    shutil.copyfile(pkg/'pipelines/pipeline.yaml',scratch/'pipelines/pipeline.yaml')
    shutil.copytree(pkg/'inputs',scratch/'inputs',dirs_exist_ok=True)
    f=scratch/'inputs/stellarator_plant_params.json'; values=json.loads(f.read_text()); values.update(change); f.write_text(json.dumps(values))
    spec=scratch/'pipelines/pipeline.yaml'; row={}
    rs.PIPELINE=spec; rs.E2E=scratch
    for caller,fn in [('single',lambda:single._execute_package() if entering else single._execute_package(pipeline_path=spec,output_dir=scratch/'out-single')),('helper',lambda:rs.run_pipeline('helper') if entering else rs.run_pipeline('helper',pipeline_path=spec,output_dir=scratch/'out-helper'))]:
        try:
            output=fn(); row[caller]={'outputs':{k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in output.items()}}
        except Exception as exc: row[caller]={'error':type(exc).__name__,'message':str(exc)}
    results[name]=row; print(mode,name,{k:v.get('error',len(v.get('outputs',{}))) for k,v in row.items()},flush=True)
record={'captured_at':datetime.now(timezone.utc).isoformat(),'package':str(pkg),'results':results}
(H/f'direct-{mode}.json').write_text(json.dumps(record,indent=2)+'\n')
if entering:
    assert 'outputs' in results['baseline']['single']
    assert 'error' in results['baseline']['helper']
else:
    import math
    before=json.loads((H/'direct-entering.json').read_text())['results']
    for name,ref in [('baseline','baseline'),('R14','tied_R14')]:
        raw=results[name]['single']['outputs']; expected=before[name]['single']['outputs']
        assert set(raw)==set(expected)
        for k,v in expected.items():
            if name=='baseline' or not isinstance(v,(int,float)): assert raw[k]==v,(name,k)
            else: assert math.isclose(raw[k],v,rel_tol=1e-9,abs_tol=1e-9),(name,k)
        scalar=results[name]['helper']['outputs']; expected=frozen['cases'][ref]['native']['outputs']
        assert set(scalar)==set(expected)
        for k,v in expected.items(): assert scalar[k]==v if name=='baseline' else math.isclose(scalar[k],v,rel_tol=1e-9,abs_tol=1e-9)
    for name,row in results.items():
        if name.startswith(('retired','invalid')):
            for result in row.values():
                assert 'error' in result
                if name.startswith('retired'): assert P+'magnet__R0' in result['message']
    print('PASS both direct callers: full raw/scalar comparisons, retired key refusal, invalid failures')
