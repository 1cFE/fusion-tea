"""Execute only the four reviewed replacement inputs through the stock lifecycle."""
from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[6];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion.studies import execute_study,study_route as route
P='whole_plant_conversion__plant__';source=route.HERE/'20260927-design-study-whole-plant-conversion'
old=json.loads((source/'results/cases.json').read_text())['cases'];center=json.loads((source/'preparation/extension-plan.json').read_text())['cryogenic_brackets'][0]['threshold_W_m3'];record=HERE/'cryo-native';record.mkdir(exist_ok=False)
points=[]
for case in old:
 if not case['case'].startswith('cryo-capacity-'):continue
 point=dict(case['inputs']);point[P+'cryogenic_demand__q_nuc_W_m3']=center+(-.01 if '-below-' in case['case'] else .01)
 delta={k:v for k,v in point.items() if v!=case['inputs'][k]};assert list(delta)==[P+'cryogenic_demand__q_nuc_W_m3']
 points.append(dict(case='r2-'+case['case'],point=point,original_case=case['case'],original_candidate_id=case['candidate_id'],changed_inputs=delta))
assert len(points)==4
(record/'proposed-points.json').write_text(json.dumps(dict(cases=points,scope='reviewed four-point diagnostic spacing replacement; original failed points remain unchanged'),indent=2)+'\n')
integration=source/'integration/integration_return.json';execute_study.execute(record,integration)
cmd=[sys.executable,str(ROOT/'scripts/study/verify.py'),'--package',str(route.PACKAGE_DIR),'--manifest',str(route.MANIFEST_PATH),'--identity',str(source/'integration/package_identity.json'),'--store',str(record/'results/native/cryo-native.db'),'--sample-size','4','--out',str(record/'results/verification_summary.json')]
with (record/'verification.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=ROOT,check=True)
v=json.loads((record/'results/verification_summary.json').read_text());assert v['outcome']=='pass' and v['stores'][0]['sampling']['sampled_rows']==4
results=json.loads((record/'results/cases.json').read_text())['cases'];behavior=[]
for case in results:
 margin=case['outputs'][P+'cryogenic_demand__evaluate__cold_margin_W'];above='-above-' in case['case'];assert (margin<0)==above
 failed=[k for k,status in case['verdicts'].items() if status!='satisfied'];assert len(failed)==int(above) and all('cryogenic_demand__cold_margin_w_ok' in k for k in failed)
 behavior.append(dict(case=case['case'],q_nuc_W_m3=case['inputs'][P+'cryogenic_demand__q_nuc_W_m3'],cold_margin_W=margin,extra_cold_capacity_W=case['outputs'][P+'cryogenic_demand__evaluate__extra_cold_capacity_W'],failed_predicates=failed))
summary=dict(status='pass',native_points=4,scalars_per_point=len(v['channels_checked']),predicates_per_point=len(v['constraints_rederived']),verification_command=cmd,behavior=behavior)
(HERE/'cryo-native-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
