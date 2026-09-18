"""Release test for the frozen 1D response, including independent refinement runs."""
import bisect
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'table-plan.json').read_text())
aggregates=[]
for case in plan['cases']:
    name=case['name']
    paths=sorted((HERE/'results').glob(name+'/result.json'))+sorted((HERE/'results').glob(name+'-refine*/result.json'))
    if not paths:
        raise RuntimeError(f'Incomplete table: {name}')
    estimates=[json.loads(p.read_text()) for p in paths]
    n=sum(x['histories'] for x in estimates)
    mean=sum(x['histories']/n*x['recoverable_TBR']['mean'] for x in estimates)
    li6=sum(x['histories']/n*x['Li6']['mean'] for x in estimates)
    li7=sum(x['histories']/n*x['Li7']['mean'] for x in estimates)
    variance=sum((x['histories']/n)**2*x['recoverable_TBR']['std_error']**2 for x in estimates)
    target=.001 if abs(mean-plan['requirement_reference'])<=plan['near_requirement_band'] else .002
    aggregates.append(dict(name=name,role=case['role'],thickness_m=case['arguments']['thickness'],histories=n,mean=mean,tbr_li6=li6,tbr_li7=li7,std_error=math.sqrt(variance),target=target,precision_pass=math.sqrt(variance)<=target,run_paths=[str(p.relative_to(HERE)) for p in paths]))
nodes=sorted([x for x in aggregates if x['role']=='node'],key=lambda x:x['thickness_m'])
withheld=[x for x in aggregates if x['role']=='withheld']
xs=[x['thickness_m'] for x in nodes]
checks=[]
for x in withheld:
    i=max(0,min(len(nodes)-2,bisect.bisect_right(xs,x['thickness_m'])-1))
    lo,hi=nodes[i:i+2]
    f=(x['thickness_m']-lo['thickness_m'])/(hi['thickness_m']-lo['thickness_m'])
    prediction=(1-f)*lo['mean']+f*hi['mean']
    prediction_var=(1-f)**2*lo['std_error']**2+f*f*hi['std_error']**2
    combined_se=math.sqrt(prediction_var+x['std_error']**2)
    residual=prediction-x['mean']
    allowance=abs(residual)+2*combined_se
    checks.append(dict(thickness_m=x['thickness_m'],prediction=prediction,direct=x['mean'],residual=residual,combined_std_error=combined_se,conservative_discrepancy=allowance,tolerance=plan['interpolation_conservative_residual_limit'],passes=allowance<=plan['interpolation_conservative_residual_limit']))
report=dict(status='PASS' if all(x['precision_pass'] for x in aggregates) and all(x['passes'] for x in checks) else 'PENDING_REFINEMENT',nodes=nodes,withheld=withheld,checks=checks,physical_scope='conditional single-opening toroidal assembly, fixed uniform source and frozen cards; no shaped-stellarator accuracy bound')
(HERE/'table-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
