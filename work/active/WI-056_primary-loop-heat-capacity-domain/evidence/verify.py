"""Verify native before/after identities and deliberate component/public refusal."""
import ast,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE));from implement import inventory
before=json.loads((HERE/'entering-native.json').read_text());after=json.loads((HERE/'corrected-native.json').read_text())
controls=('baseline','double_cp','double_dT','dormant','finance_zero','magnet_half')
for name in controls:assert before['cases'][name]==after['cases'][name],name
invalid=[name for name in after['cases'] if name not in controls]
for name in invalid:
 row=after['cases'][name]
 assert row['error']=='EvaluationFailed' and 'Primary Coolant Loop:' in row['message'] and 'must be finite and positive' in row['message'],(name,row)
local=json.loads((HERE/'corrected-local.json').read_text());oldlocal=json.loads((HERE/'entering-local.json').read_text())
for name,row in local.items():
 if name.endswith('/baseline'):assert oldlocal[name]==row
 else:assert row['error']=='ValueError' and 'Primary Coolant Loop:' in row['message'],(name,row)
# Preserve every arithmetic expression and output tuple exactly after guards.
old=ast.parse((HERE/'entering-primary-body.py').read_text());new=ast.parse((ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py').read_text())
fun=lambda tree:next(n for n in tree.body if isinstance(n,ast.FunctionDef))
assert [ast.dump(n) for n in fun(old).body[1:]]==[ast.dump(n) for n in fun(new).body[3:]]
package=ROOT/'exploration/stellarator_e2e/generated';hashes=inventory(package)
assert hashes==json.loads((HERE/'candidate-package-hashes.json').read_text())
seeds=json.loads((HERE/'candidate-seeds.json').read_text());oldseeds=json.loads((HERE/'entering-seeds.json').read_text())
assert len(seeds)==13 and all(seeds[n]==h and hashes[n]==h for n,h in oldseeds.items())
assert (ROOT/'models/library/analyses/mfe_primary_loop.sysml').read_bytes()==(ROOT/'exploration/stellarator_e2e/models/analyses/mfe_primary_loop.sysml').read_bytes()
# Baseline valid domain includes an existing engineering violation, not full feasibility.
base=after['cases']['baseline']; report=base['report']
summary={'public_controls':{k:after['cases'][k].get('error','exact outputs/report preserved') for k in controls},'public_deliberate_refusals':len(invalid),'local_cases':len(local),'local_deliberate_refusals':sum('error' in r for r in local.values()),'ordered_body_AST_equal':True,'package_files':len(hashes),'seeds':len(seeds),'entering_seeds_preserved':len(oldseeds),'baseline_report':report}
(HERE/'acceptance-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
