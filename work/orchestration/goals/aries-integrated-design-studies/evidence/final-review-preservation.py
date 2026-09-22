import json,hashlib,sqlite3
from pathlib import Path
R=Path.cwd();E=R/'work/orchestration/goals/aries-integrated-design-studies/evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
entry=read(E/'entry-preservation.json')['files'];bad=[n for n,h in entry.items() if not (R/n).is_file() or sha(R/n)!=h];assert not bad
actual=read(E/'final-stellaris-regression-actual.json');baseline=read(R/'work/analysis/model-evaluation-diagnostics/baseline.json');assert all(actual[k]==baseline[k] for k in ('outputs','responses'))
s=R/'exploration/aries_integrated/studies/20260922-aries-integrated-design-robustness';db=sqlite3.connect(f'file:{s}/results/native/20260922-aries-integrated-design-robustness.db?mode=ro&immutable=1',uri=True);states=dict(db.execute('select state,count(*) from attempt_transitions group by state'));assert states=={'started':174,'committed':174};assert db.execute('select distinct attempt_number from attempt_transitions').fetchall()==[(1,)]
c=read(s/'results/cases.json')['cases'];passed=sum(all(v=='satisfied' for v in x['verdicts'].values()) for x in c);assert passed==168
v=read(s/'results/verification_summary.json');assert v['outcome']=='pass' and len(v['channels_checked'])==364 and len(v['constraints_rederived'])==14
r={'status':'PASS','protected_files':len(entry),'changed':bad,'stored_stellaris_replay_exact':True,'stellaris_outputs':len(actual['outputs']),'stellaris_responses':len(actual['responses']),'attempts':states,'all_attempt_numbers':[1],'pass_evaluated':passed,'adverse':len(c)-passed,'verification_channels':len(v['channels_checked']),'verification_predicates':len(v['constraints_rederived'])};(E/'final-review-preservation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
