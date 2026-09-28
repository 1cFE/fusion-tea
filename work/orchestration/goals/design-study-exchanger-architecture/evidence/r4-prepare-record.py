"""Prepare the corrected identity against exactly the retained1277 input maps."""
import argparse,gzip,hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from exploration.exchanger_architecture.thermal_requirements.studies import study_route as route,oracle_entry
from scripts.study import common,manifest,verify
HERE=route.HERE;OLD=HERE/'20260927-exchanger-thermal-comparison';NEW=HERE/'20260927-exchanger-thermal-comparison-b'
GOAL=ROOT/'work/orchestration/goals/design-study-exchanger-architecture'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(path,value):
 with path.open('x') as f:json.dump(value,f,separators=(',',':'),allow_nan=False);f.write('\n')
def prepare():
 common.assert_tree_clean(route.PACKAGE_DIR)
 loaded=manifest.load(route.MANIFEST_PATH)
 assert route.interface()['executable_fingerprint']!='cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7'
 manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
 assert not NEW.exists();NEW.mkdir()
 copies=('proposed-points.json','axes.json','axis-plan.json','oracle-selection.json','oracle-scan-summary.json','oracle-refinement-receipt.json','proposal-finalization.json','owner-brief.md','owner-supplement-r2.md','owner-supplement-r3.md','r2-thermal-requirements.md','r2-source-review.md','r3-study-contract.md','r3-cost-boundary.md','r3-protocol-review.md')
 for name in copies:shutil.copyfile(OLD/name,NEW/name)
 prior=NEW/'prior-attempt';prior.mkdir()
 for name in ('oracle-scan.json.gz','candidate-ledger.json.gz','baseline-inputs.json','attempt-snapshot.json','lossless-compression.json','failed-package-preservation.json','sealed-package.tar.gz','record.md'):
  shutil.copyfile(OLD/name,prior/name)
 for name in ('cases.json','verification-attempt.json'):
  raw=(OLD/'results'/name).read_bytes();target=prior/(name+'.gz')
  target.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(target.read_bytes())==raw
 write(NEW/'manifest.json',loaded.data|{'ties':read(OLD/'manifest.json')['ties']})
 write(NEW/'prior-attempt.json',{'record':OLD.relative_to(ROOT).as_posix(),'commit':'ca25c49c','attempt_snapshot_sha256':sha(OLD/'attempt-snapshot.json'),'input_maps_sha256':sha(OLD/'proposed-points.json'),'new_input_maps_sha256':sha(NEW/'proposed-points.json'),'case_count':1277,'correlation':'Exact full numeric input maps and case labels; package-only stable numerical evaluation changes. Original archive, scans and failed store remain immutable.','prior_scan_paths':['oracle-scan.json.gz','candidate-ledger.json.gz','scan-checkpoints'],'oracle_sources_unchanged':{p.relative_to(ROOT).as_posix():sha(p) for p in (HERE/'oracle_entry.py',HERE/'thermal_oracle.py')}})
 template=(OLD/'record-template-source.md').read_text();(NEW/'record-template-source.md').write_text(template)
 heads=[line for line in (OLD/'record.md').read_text().splitlines() if line.startswith('## ')]
 (NEW/'record.md').write_text('# Corrected thermal comparison — preparation\n\n'+'\n\n'.join(h+'\n\nExact-map replay pending.' for h in heads)+'\n')
 print(json.dumps({'record':str(NEW),'cases':1277,'exact_proposals':sha(NEW/'proposed-points.json')==sha(OLD/'proposed-points.json')}))
def scan():
 proposals=read(NEW/'proposed-points.json')['cases'];catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR);bindings=oracle_entry.operand_bindings();rows=[];edges=[]
 def evaluate(point,label):
  try:
   values=oracle_entry.evaluate(point);verdicts={cid:'satisfied' if verify.derive_verdict(cid,e,bindings,point,{},values)[0] else 'violated' for cid,e in catalog.items()}
   return {'case':label,'status':'evaluated','net_MW':values['aries_integrated_plant__plant_ledger__evaluate__net_electric'],'lcoe_USD2004_MWh':values['aries_integrated_plant__lifecycle_price__evaluate__lcoe'],'verdicts':verdicts}
  except Exception as e:return {'case':label,'status':'refused','error':type(e).__name__+': '+str(e)}
 for p in proposals:
  result=evaluate(p['point'],p['case']);assert result['status']=='evaluated',result;rows.append(result)
 selected=read(NEW/'oracle-selection.json')['selected'];by_scan={p['scan_id']:p for p in proposals}
 for s in selected:
  if s['scenario']!='main' or s['best_scan_id'] is None:continue
  p=by_scan[s['best_scan_id']]['point']
  for axis,values in [('cycle__selected_flow',(500.,2400.)),('heat_exchangers__pbli_split_fraction',(.1,.9))]:
   if s['mode']==0 and axis.endswith('split_fraction'):continue
   for value in values:
    point=p|{'aries_integrated_plant__'+axis:value};result=evaluate(point,str((s['load'],s['offer'],s['mode'],axis,value)))
    result.update(parent_scan_id=s['best_scan_id'],axis=axis,value=value);edges.append(result)
 assert len(rows)==1277
 write(NEW/'oracle-window-recheck.json',{'kind':'Fresh independent recheck at corrected identity, before native execution','executable_fingerprint':route.interface()['executable_fingerprint'],'source_inputs_sha256':sha(NEW/'proposed-points.json'),'case_count':len(rows),'cases':rows,'outer_edges':edges,'interpretation':'Prior full scan retained under immutable prior-attempt reference. Every supplied map is re-evaluated independently; matched leading anchors and original outer edges are rechecked. No candidate or requirement changes.'})
 print(json.dumps({'proposals_rechecked':len(rows),'edges_rechecked':len(edges),'all_proposals_finite':True}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=('prepare','scan'));a=parser.parse_args();{'prepare':prepare,'scan':scan}[a.action]()
