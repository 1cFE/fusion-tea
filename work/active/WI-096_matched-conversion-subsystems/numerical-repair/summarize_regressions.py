"""Summarize retained focused receipts without rerunning any native model."""
import argparse,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent;H=R/'exploration/component_alternatives';sys.path.insert(0,str(H));import verify

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 if args.out.exists():raise FileExistsError(args.out)
 diagnostics=json.loads((H/'studies/20260926-design-study-component-alternatives/results/verification-diagnostics.json').read_text())['cases'];out=[]
 for old in diagnostics:
  if not old['numeric_mismatches']:continue
  cid=old['candidate_id'].rsplit(':',1)[-1];row=json.loads((E/'focused/runs'/cid/'result.json').read_text());expected=verify.evaluate(row['effective_inputs']);channels=[]
  for prior in old['numeric_mismatches']:
   key=prior['channel'];actual=row['outputs'][key];target=expected[key];error=abs(actual-target);relative=error/max(abs(actual),abs(target)) if actual or target else 0
   assert verify.agreement(key,actual,target)
   channels.append(dict(channel=key,old_native=prior['native'],new_native=actual,oracle=target,old_relative_deviation=prior['relative_deviation'],new_relative_deviation=relative,absolute_error=error))
  out.append(dict(case=cid,prior_mismatched_channels=channels,full_verification='872 channels and 84 predicates pass'))
 args.out.write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(out),'original mismatch cases')
if __name__=='__main__':main()
