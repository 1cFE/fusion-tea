"""Focused native numerical regression; never writes an existing receipt or runs a study.

Replays six original mismatches and eight neighboring offers, plus the baseline.
All full inputs come verbatim from the sealed old native record. The original
independent oracle and its exact predicate/tolerance contract remain unchanged.
"""
import argparse, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'exploration/component_alternatives'
sys.path.insert(0,str(HERE))
import run,verify
P=run.P
IDS={'c0035','c0040','c0160','c0206','c0480','c0484',
     'c0036','c0041','c0161','c0205','c0207','c0481','c0482','c0485'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    if args.out.exists():raise FileExistsError(args.out)
    args.out.mkdir(parents=True)
    runtime=run.load_runtime();rows=json.loads((HERE/'studies/20260926-design-study-component-alternatives/results/cases.json').read_text())['cases']
    summary=[]
    baseline=run.execute_case('baseline',{},runtime,args.out/'runs')
    check=verify.verify_row(baseline);summary.append(dict(case='baseline',verification=check));print('baseline',check['status'],flush=True)
    for old in rows:
        cid=old['candidate_id'].rsplit(':',1)[-1]
        if cid not in IDS:continue
        new=run.execute_case(cid,old['inputs'],runtime,args.out/'runs')
        check=verify.verify_row(new)
        reports={v['constraint_id']:v['status'] for v in new['outputs']['constraint_report']['results']} if new['status']=='evaluated' else {}
        changes={k:dict(old=v,new=reports.get(k)) for k,v in old['verdicts'].items() if reports.get(k)!=v}
        assert new['effective_inputs']==old['inputs']
        item=dict(case=cid,label=old['case'],verification=check,verdict_changes=changes,
                  original_failed_predicates=[k for k,v in old['verdicts'].items() if v=='violated'],
                  fingerprint=new['fingerprint'])
        summary.append(item);print(cid,check['status'],len(changes),'predicate changes',check.get('differences'),flush=True)
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    assert len(summary)==15
    assert all(r['verification']['status']=='pass' and not r.get('verdict_changes') for r in summary)

if __name__=='__main__':main()
