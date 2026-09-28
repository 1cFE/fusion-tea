"""Forensic continuation of unchanged stock checks; never changes acceptance rules."""
from pathlib import Path
import collections
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT))
from scripts.study import common,manifest,verify as stock
from exploration.whole_plant_conversion.studies import study_route as route

HERE=Path(__file__).resolve().parent
RECORD=route.HERE/'20260927-design-study-whole-plant-conversion'
P='whole_plant_conversion__plant__'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def identities():
 files=[route.MANIFEST_PATH,RECORD/'results/cases.json',RECORD/'proposed-points.json',*sorted(route.E2E.glob('oracle_*.py')),route.E2E/'verify.py',*sorted(route.PACKAGE_DIR.rglob('*'))]
 return {str(p.relative_to(ROOT)):sha(p) for p in files if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def run():
 before=identities();write('input-identities-before.json',before)
 loaded=manifest.load(route.MANIFEST_PATH);_,evaluate,bindings=stock.load_oracle(loaded)
 objectives=stock.objective_channels(loaded);wanted=set(objectives)|{b['key'] for t in bindings.values() for b in t.values() if b.get('kind')=='channel'}
 limits={r['channel']:r['value'] for r in loaded.data.get('absolute_tolerances',[])}
 catalog={r['constraint_id']:r for r in common.read_json(route.PACKAGE_DIR/'contracts/model_contract.json','contract')['constraint_catalog']['concrete_entries']}
 package_inputs=stock.package_input_values(route.PACKAGE_DIR);cases=json.loads((RECORD/'results/cases.json').read_text())['cases']
 failures=[];predicates=[];errors=[];case_summaries=[];stats={};scalar_count=predicate_count=0
 for index,case in enumerate(cases):
  cid=case['candidate_id'];name=case['case'];context=dict(candidate_id=cid,case=name)
  try:channels=evaluate(case['inputs'])
  except Exception as e:errors.append(dict(context,error=repr(e)));continue
  local=[];worst=0.;nonzero=0
  for key in sorted(wanted):
   if key not in channels or key not in case['outputs'] or not all(math.isfinite(v) for v in (channels.get(key,float('nan')),case['outputs'].get(key,float('nan')))):
    errors.append(dict(context,channel=key,error='missing or nonfinite numeric comparison'));continue
   actual,expected=case['outputs'][key],channels[key];relative=common.relative_deviation(actual,expected);absolute=abs(actual-expected);limit=limits.get(key,0.)
   scalar_count+=1;worst=max(worst,relative);nonzero+=absolute!=0
   stat=stats.setdefault(key,dict(comparisons=0,nonzero_differences=0,max_absolute_error=0.,max_relative_deviation=0.,off_tolerance=0,declared_absolute_tolerance=limit));stat['comparisons']+=1;stat['nonzero_differences']+=absolute!=0
   stat['max_absolute_error']=max(stat['max_absolute_error'],absolute);stat['max_relative_deviation']=max(stat['max_relative_deviation'],relative)
   if relative>=stock.TOLERANCE and absolute>=limit:
    failure=dict(context,channel=key,native=actual,oracle=expected,absolute_error=absolute,relative_deviation=relative,relative_tolerance=stock.TOLERANCE,declared_absolute_tolerance=limit)
    failures.append(failure);local.append(key);stat['off_tolerance']+=1
  local_predicates=[]
  for key,recorded in sorted(case['verdicts'].items()):
   try:satisfied,resolved=stock.derive_verdict(key,catalog[key],bindings,case['inputs'],package_inputs,channels)
   except Exception as e:errors.append(dict(context,constraint=key,error=repr(e)));continue
   predicate_count+=1;expected='satisfied' if satisfied else 'violated'
   if expected!=recorded:
    predicates.append(dict(context,constraint=key,native=recorded,oracle=expected));local_predicates.append(key)
  if case['executable_fingerprint']!=route.interface()['executable_fingerprint']:errors.append(dict(context,error='executable identity mismatch'))
  case_summaries.append(dict(context,scalar_comparisons=len(wanted),predicate_comparisons=len(case['verdicts']),nonzero_scalar_differences=nonzero,worst_relative_deviation=worst,off_tolerance_channels=local,predicate_mismatches=local_predicates))
  if (index+1)%100==0:print('checked',index+1,'cases; off-tolerance comparisons',len(failures),flush=True)
 after=identities();write('input-identities-after.json',after)
 summary=dict(kind='forensic scan using unchanged stock comparison and predicate rules; no acceptance waiver',cases=len(cases),evaluated=len(case_summaries),wanted_channels=len(wanted),scalar_comparisons=scalar_count,predicate_comparisons=predicate_count,off_tolerance_comparisons=len(failures),off_tolerance_cases=len({r['case'] for r in failures}),off_tolerance_channels=dict(collections.Counter(r['channel'] for r in failures)),predicate_mismatches=len(predicates),evaluation_errors=len(errors),inputs_unchanged=before==after,relative_tolerance=stock.TOLERANCE)
 write('discrepancies.json',dict(summary=summary,scalar_failures=failures,predicate_mismatches=predicates,errors=errors));write('case-checks.json',case_summaries);write('channel-statistics.json',stats)
 print(json.dumps(summary,indent=2))
 if before!=after:raise RuntimeError('input bytes changed during forensic scan')

if __name__=='__main__':run()
