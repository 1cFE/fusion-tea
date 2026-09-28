"""Independent selected native replays and closed-form/energy verification."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile

ROOT=Path(__file__).resolve().parents[5]
HERE=ROOT/'exploration/aries_integrated'
EVIDENCE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('reviewed_run',HERE/'run.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
from simkit.evaluation.package_load import ProvisionalPackageLoader
scratch=Path(tempfile.mkdtemp(prefix='reviewer-aries-native-'))
module,fingerprint=ProvisionalPackageLoader(package_dir=HERE/'aries_integrated',package_name='aries_integrated',link_root=scratch/'links').load()
runtime=(module,module.create_aries_integrated_registry(),str(fingerprint))
p='aries_integrated_plant__'; a='aries_cs_plasma_integration__plasma__amplitude'
cases={
 'reviewer-calculated':{p+'source__producer_mode':1.},
 'reviewer-density-up':{p+'source__producer_mode':1.,a:5.15e20},
 'reviewer-he-bypass':{p+'source__producer_mode':1.,p+'heat_exchangers__he_limit':200.},
 'reviewer-low-power':{p+'source__reference_fusion_mw':600.},
}
rows=[runner.execute_case(name,changes,runtime,scratch) for name,changes in cases.items()]
def out(row,owner,key):return row['outputs'][p+owner+'__evaluate__'+key]
def inp(row,owner,key):return row['effective_inputs'][p+owner+'__'+key]
def close(actual,expected,atol=2e-7,rtol=2e-10):
 assert math.isclose(actual,expected,abs_tol=atol,rel_tol=rtol),(actual,expected)
summary=[]
for row in rows:
 assert row['status']=='evaluated',(row['case'],row.get('error'))
 get=lambda owner,key:out(row,owner,key)
 chosen=lambda owner,key:inp(row,owner,key)
 c=chosen('cycle','selected_flow')*chosen('cycle','cp')/1e6
 wt=get('turbine','shaft_produced'); wc=sum(get('compressor_'+str(i),'shaft_demand') for i in (1,2,3))
 q=get('heat_exchangers','accepted_heat')
 rejected=-sum(get(o,'heat_into_fluid') for o in ('intercooler_1','intercooler_2','precooler'))
 close(q,rejected+wt-wc)
 net=get('generator_auxiliaries','net_electric')
 gross=get('generator_auxiliaries','gross_electric'); shaft_import=get('generator_auxiliaries','shaft_import')
 heating=chosen('deposition','auxiliary_heat')/chosen('generator_auxiliaries','heating_efficiency')
 pumps=sum(chosen('deposition',b+'_pump') for b in ('he','pbli','divertor'))
 fuel=chosen('generator_auxiliaries','fuel_base')+chosen('generator_auxiliaries','fuel_coefficient')*get('fuel','exhaust_rate')
 extras=sum(chosen('generator_auxiliaries',k) for k in ('cryo','control','other_electric'))
 close(net,gross-shaft_import-heating-pumps-fuel-extras)
 close(get('plant_ledger','plant_residual'),0)
 for b in ('he','divertor','pbli'):
  transfer=get('heat_exchangers',b+'_transferred')
  close(transfer+get('heat_exchangers',b+'_unmet'),get(b+'_coolant','delivered_heat'))
  if get('heat_exchangers',b+'_state_defined'):
   hot=get('heat_exchangers',b+'_hot'); ret=get('heat_exchangers',b+'_return')
   ti=get('heat_exchangers',b+'_secondary_in'); to=get('heat_exchangers',b+'_secondary_out')
   ch=chosen('heat_exchangers',b+'_flow')*chosen('heat_exchangers',b+'_cp')/1e6
   close(ch*(hot-ret),transfer);close(c*(to-ti),transfer)
   dt1=hot-to;dt2=ret-ti
   assert dt1>=-1e-8 and dt2>=-1e-8
   # Independent LMTD relation rather than copying the epsilon/NTU evaluation.
   lmtd=(dt1-dt2)/math.log(dt1/dt2) if abs(dt1-dt2)>1e-8 else dt1
   close(chosen('heat_exchangers',b+'_ua')*lmtd,transfer,atol=1e-5,rtol=1e-7)
   assert get('heat_exchangers',b+'_hot_bound_margin')>=-1e-8
 for support in ('magnet','breeding','deposition','hydraulics','materials','machine_map'):
  assert get('plant_ledger','supported_'+support)==0
 summary.append(dict(case=row['case'],power=get('source','selected_power'),exhaust=get('fuel','exhaust_rate'),available=get('plant_ledger','total_available_heat'),accepted=q,unmet=get('heat_exchangers','unmet_heat'),turbine=get('heat_exchangers','turbine_temperature'),shaft=wt-wc,net=net,shaft_import=shaft_import,plant_residual=get('plant_ledger','plant_residual'),he_state=get('heat_exchangers','he_state_defined'),recuperator_bypass=get('recuperator','bypass_active')))
base,perturbed=rows[:2]
assert {k for k,v in base['effective_inputs'].items() if v!=perturbed['effective_inputs'][k]}=={a}
ratio=(5.15/5.)**2
close(out(perturbed,'source','selected_power')/out(base,'source','selected_power'),ratio)
close(out(perturbed,'fuel','exhaust_rate')/out(base,'fuel','exhaust_rate'),ratio)
for row in (base,perturbed):
 assert out(row,'heat_exchangers','unmet_heat')==0
 c=inp(row,'cycle','selected_flow')*inp(row,'cycle','cp')/1e6
 tc=out(row,'compressor_3','temperature_out'); eps=inp(row,'cycle','recuperator_effectiveness')
 # All branch heat is accepted here: solve the coupled temperature algebra directly.
 k=out(row,'turbine','temperature_out')/out(row,'heat_exchangers','turbine_temperature')
 expected_t=(tc*(1-eps)+out(row,'plant_ledger','total_available_heat')/c)/(1-eps*k)
 close(out(row,'heat_exchangers','turbine_temperature'),expected_t)
assert out(perturbed,'plant_ledger','net_electric')>out(base,'plant_ledger','net_electric')
assert out(rows[2],'heat_exchangers','he_state_defined')==0
assert out(rows[2],'heat_exchangers','he_unmet')>0
assert out(rows[3],'generator_auxiliaries','net_shaft')<0
assert out(rows[3],'generator_auxiliaries','shaft_import')>0
sources=[ROOT/'models/library/analyses/integrated_heat_electricity.sysml',ROOT/'models/designs/aries_cs_integrated/plant.sysml']
report=dict(fingerprint=str(fingerprint),scratch=str(scratch),sources={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sources},checks='PASS: fixed hardware density chain; independent cycle/electrical/branch/LMTD identities; direct all-heat temperature solution; bypass definedness; motor import; unsupported science retained',summary=summary,rows=rows)
(EVIDENCE/'reviewer-native.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
