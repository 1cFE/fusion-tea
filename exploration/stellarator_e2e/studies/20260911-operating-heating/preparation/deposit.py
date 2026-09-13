"""Deposit a reviewable study proposal; never executes a package."""
import hashlib
import json
import shutil
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as o
R=Path('exploration/stellarator_e2e/studies/20260911-operating-heating')
P=o.P
manifest=json.loads(Path('exploration/stellarator_e2e/studies/manifest.json').read_text())
base=manifest['baseline']['point']
root=json.loads((R/'preparation/preliminary-signed-density-probe.json').read_text())['root_fraction']
def arm(name, points, note):
    return {'arm_id':'arm-'+name,'provenance':'engineered','note':note,'cases':[{'label':label,'point':{**base,**{P+k:v for k,v in values.items()}}} for label,values in points]}
arms=[
arm('reserve',[(f'installed-{x:.15g}',{'p_wallplug_heat':x}) for x in [80.,98.15920157585356,100.,110.,120.]],'Fixed plasma, efficiencies and all other modeled inputs. Capacity-limited, equality candidate, baseline, and extra reserve controls.'),
arm('retained-alpha',[(f'alpha-{x}',{'f_alpha_fast':x}) for x in [.94,.95,.96]],'At fixed installation and baseline plasma density/temperature; physical retained-alpha assumption control. Divertor absorbed heat cancels algebraically here.'),
arm('density',[(f'density-{x}',{'n_e0':5.06e20*x}) for x in [1.,1.1,1.2,1.3,1.4]],'Public plasma-density sensitivity at fixed installed heating. Positive and negative signed demand; all other physical couplings and verdicts remain visible. No density-limit or engineering-feasibility claim.'),
arm('coordinated-zero',[(label,{'n_e0':6.578e20,'f_alpha_fast':value}) for label,value in [('positive-near-zero',root-1e-5),('algebraic-zero-candidate',root),('negative-near-zero',root+1e-5)]],'Separate coordinated density + retained-alpha diagnostic. The affine zero construction is preselected, not a pure-density control, optimization, or discovered physical boundary. Exact native zero remains unproved; call near-zero for any nonzero native residual.')]
proposal={'status':'PREPARATION ONLY; fresh critique and formal Step 7 scan pending','study_id':R.name,'baseline_point':base,'arms':arms,'case_count':sum(len(a['cases']) for a in arms),'held':{'eta_source_heat':.5,'eta_couple_heat':1.,'f_ren':1.,'T_i0':14.63,'p_wallplug_heat_except_reserve':100.,'finance':'unchanged modeled defaults','calendar':'live, unchanged modeled defaults','geometry':'baseline R and a, complete baseline magnet radius tie'},'declined':{'T_i0':'Temperature-only probe stayed positive over its candidate range. Density provides signed-demand cases without changing temperature; no temperature point will run.'},'zero_construction':{'density':6.578e20,'formula':'f*=f0 + (f1-f0)*D(f0)/(D(f0)-D(f1)), using f0=.95 and f1=1 at held density; D is affine in this fraction at held plasma solution.','f0':.95,'f1':1.,'fraction':root,'fraction_in_unit_interval':0<=root<=1,'oracle_residual_mw':-1.1368683772161603e-13,'native_residual':'not executed; never round a nonzero value to exact zero'},'verification':{'generic_sample_size':16,'scheme':'all completed cases, hence every verdict stratum; stock generic verify.py plus additional independently stated conservation/cost identities','tolerance':{'relative':1e-9,'absolute_for_signed_zero':1e-9},'all_constraints_required':18,'failures':'Keep failed case evidence; stop execution/publication under runbook Step 9; never suppress or regrade. No execution-failure point intentionally scheduled; negative demand is an expected completed invalid verdict.'}}
(R/'preparation/proposal.json').write_text(json.dumps(proposal,indent=2)+'\n')
(R/'preparation/required-channels.json').write_text(json.dumps(o.ORACLE_OUTPUT_TO_CHANNEL,indent=2)+'\n')
contract=json.loads(Path('exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
(R/'preparation/model-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
files={
 'manifest.json':'exploration/stellarator_e2e/studies/manifest.json',
 'ANNEX.md':'exploration/stellarator_e2e/studies/ANNEX.md',
 'oracle_entry.py':'exploration/stellarator_e2e/studies/oracle_entry.py',
 'verify_stellaris.py':'exploration/stellarator_e2e/verify_stellaris.py',
 'study_route.py':'exploration/stellarator_e2e/studies/study_route.py',
 'model-audit.md':'work/active/WI-050_mfe-coherent-operating-heating/audit.md',
 'package-audit.md':'.project/active/mfe-operating-heating-study-package/audit.md',
 'inherited-baseline-attribution.json':'work/active/WI-050_mfe-coherent-operating-heating/implementation/baseline-attribution.json',
 'inherited-baseline-attribution.md':'work/active/WI-050_mfe-coherent-operating-heating/implementation/baseline-attribution.md',
 'inherited-finance.json':'work/active/WI-050_mfe-coherent-operating-heating/audit-evidence/independent-finance.json',
 'inherited-boundary-results.json':'work/active/WI-050_mfe-coherent-operating-heating/implementation/boundary-results.json',
 'inherited-boundary-runner.py':'work/active/WI-050_mfe-coherent-operating-heating/implementation/run_acceptance.py',
 'integration_return.json':'work/orchestration/goals/fusion-audit-remediation/evidence/T-018_integration/integration_return.json',
}
(R/'context').mkdir(exist_ok=True)
index=[]
for dest,src in files.items():
    b=Path(src).read_bytes(); (R/'context'/dest).write_bytes(b)
    index.append({'copy':'context/'+dest,'source':src,'sha256':hashlib.sha256(b).hexdigest(),'scope':'Inherited evidence/source snapshot, not new study execution'})
(R/'context/index.json').write_text(json.dumps(index,indent=2)+'\n')
print('Deposited',proposal['case_count'],'proposed cases; no TEAx execution')
