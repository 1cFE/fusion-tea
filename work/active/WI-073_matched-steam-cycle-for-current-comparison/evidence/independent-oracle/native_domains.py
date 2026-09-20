"""Adversarial public-entry cases, retaining refusals and heat-boundary mismatches."""
import json,math,os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'exploration/stellarator_e2e/studies'),str(ROOT/'exploration/stellarator_e2e'),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
import study_route,oracle_entry
from simkit.study.bridge import CandidateBridge
engine=study_route.prepare(ROOT/'exploration/stellarator_e2e/generated',Path(tempfile.mkdtemp(prefix='wi073-domains-')))
bridge=CandidateBridge(engine.entry_models);P=oracle_entry.P
cases=[('invalid_matched_mode',{'turbine__matched_cycle_enabled':.5}),('invalid_cooling_mode',{'heat_rejection__cooling_water_enabled':-1.}),('cooling_without_cycle',{'turbine__matched_cycle_enabled':0.}),('wrong_pressure',{'turbine__main_steam_generator__pressure_MPa':6.3}),('outside_table',{'turbine__condenser__temperature_C':60.00001}),('missing_secondary_heat',{'heat_transport__secondary_energy_mode':0.}),('missing_primary_heat',{'heat_transport__loop_live':0.})]
results=[]
for label,changes in cases:
 proposal={P+k:v for k,v in changes.items()};record={'label':label,'inputs':proposal}
 try:
  row=engine.evaluate(bridge.build(proposal))
  if not row.outputs:record['native_refusal']=str(row)
  else:
   record['native_gross_MW']=row.outputs[P+'pb__p_the'];record['state_gross_MW']=row.outputs[P+'turbine__matched_cycle__p_gross_MW']
   record['gross_heat_boundary_difference_MW']=record['native_gross_MW']-record['state_gross_MW']
 except Exception as error:record['native_refusal']=str(error)
 try:oracle_entry.evaluate(proposal);record['oracle_evaluated']=True
 except Exception as error:record['oracle_refusal']=str(error)
 results.append(record);(HERE/'native-domain-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(record),flush=True)
assert all('native_refusal' in r and 'oracle_refusal' in r for r in results), results
