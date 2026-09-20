"""Retained native verification, independent original-table oracle versus public execution."""
import json
import math
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT),str(ROOT/'exploration/stellarator_e2e/studies'),str(ROOT/'exploration/stellarator_e2e')]
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
import oracle_entry as oracle
import study_route
from simkit.study.bridge import CandidateBridge
from scripts.study import verify

P = oracle.P
package = ROOT/'exploration/stellarator_e2e/generated'
contract = json.loads((package/'contracts/model_contract.json').read_text())
inputs = verify.package_input_values(package)
entries = contract['constraint_catalog']['concrete_entries']
engine = study_route.prepare(package,Path(tempfile.mkdtemp(prefix='wi073-native-')))
bridge = CandidateBridge(engine.entry_models)
CASES = [
 ('baseline',{}),
 ('legacy',{'turbine__matched_cycle_enabled':0.,'heat_rejection__cooling_water_enabled':0.}),
 ('condenser40',{'turbine__condenser__temperature_C':40.}),
 ('condenser50',{'turbine__condenser__temperature_C':50.}),
 ('steam435',{'turbine__main_steam_generator__outlet_temperature_C':435.,'turbine__reheater__outlet_temperature_C':435.}),
 ('circuits18',{'heat_transport__n_loops':18.}),
 ('cooling_disabled',{'heat_rejection__cooling_water_enabled':0.}),
 ('cooling_zero_approach',{'heat_rejection__water_outlet_C':42.}),
 ('disabled_bad_properties',{'turbine__matched_cycle_enabled':0.,'heat_rejection__cooling_water_enabled':0.,'turbine__main_steam_generator__pressure_MPa':-1.,'heat_rejection__water_inlet_C':-999.}),
]
results = []
for label,changes in CASES:
    proposal={P+k:v for k,v in changes.items()}
    row=engine.evaluate(bridge.build(proposal))
    actual=row.outputs
    expected=oracle.evaluate(proposal)
    if not actual:
        raise AssertionError((label,str(row)))
    failures=[]
    for key,value in expected.items():
        atol=1e-18 if '__inventory__' in key else 1e-6
        boolean_channel = next((x['python_type']=='bool' for x in contract['outputs'] if x['channel_name']==key),False)
        agrees = key in actual and (actual[key]==value if boolean_channel else math.isclose(actual[key],value,rel_tol=1e-9,abs_tol=atol))
        if not agrees:
            failures.append({'channel':key,'actual':actual.get(key),'expected':value,'absolute_tolerance':atol})
    print(label, 'scalar failures', failures, flush=True)
    predicates=[]
    for entry in entries:
        cid=entry['constraint_id']
        expected_ok,_=verify.derive_verdict(cid,entry,oracle.operand_bindings(),proposal,inputs,expected)
        wanted='satisfied' if expected_ok else 'violated'
        actual_verdict=row.responses[cid]
        predicates.append({'id':cid,'expected':wanted,'actual':actual_verdict})
        if actual_verdict!=wanted:
            failures.append({'constraint':cid,'actual':actual_verdict,'expected':wanted})
    headline={name:actual[P+path] for name,path in {
        'gross_MW':'pb__p_the','net_MW':'pb__p_net','eta_selected':'turbine__cycle_selection__eta_selected',
        'cycle_pumps_MW':'turbine__matched_cycle__p_cycle_pumps_MW',
        'cooling_pump_MW':'heat_rejection__cooling_water__p_cooling_pump_electric_MW',
        'total_capital':'total_capital__total_capital','overnight_capital':'overnight_capital__overnight_capital',
        'lcoe':'lcoe_calc__lcoe','lcoe_1cfe':'lcoe_1cfe_calc__lcoe',
        'raw_legacy_cycle_interface_ok':'heat_transport__equipment__cycle_interface_ok',
    }.items()}
    checks=[]
    if actual[P+'turbine__matched_cycle__active']:
        assert math.isclose(actual[P+'pb__p_the'],actual[P+'turbine__matched_cycle__p_gross_MW'],rel_tol=1e-12,abs_tol=1e-8)
        for name in ('salt_heat_residual_MW','heater_mass_residual_kg_s','heater_energy_residual_MW','cycle_shaft_residual_MW','cycle_electric_residual_MW'):
            v=actual[P+'turbine__matched_cycle__'+name]
            if abs(v)>1e-8:failures.append({'balance':name,'actual':v})
    results.append({'label':label,'inputs':proposal,'semantic_fingerprint':contract['semantic_fingerprint'],
                    'executable_fingerprint':str(engine.fingerprint),'mapped_scalar_count':len(expected),'predicate_count':len(predicates),
                    'headlines':headline,'predicates':predicates,'failures':failures,'outputs':dict(actual)})
    (HERE/'native-check-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(label,len(expected),'scalars',len(predicates),'predicates',len(failures),'failures',headline,flush=True)
assert not any(r['failures'] for r in results)
