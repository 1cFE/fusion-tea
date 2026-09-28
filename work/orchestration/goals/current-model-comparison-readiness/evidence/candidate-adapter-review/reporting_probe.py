"""Synthetic wrapper joins and source-aware account recheck, no plant execution."""
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6]
HERE=ROOT/'.project/active/aries-comparison-preparation/current-readiness/candidate'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from candidate_common import digest
from compare_candidate import compare
spec=importlib.util.spec_from_file_location('artificial_report_fixture',ROOT/'tests/test_compare_fixed_point.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
manifest, observations=fixture.fixture()
manifest['quantities'][1]['producers']=['prediction']
manifest['quantities'][2]['producers']=['component']
temp=Path(tempfile.mkdtemp(prefix='report-wrapper-review-'))
here=temp/'candidate';here.mkdir()
package=temp/'artificial/contracts';package.mkdir(parents=True)
(package/'model_contract.json').write_text(json.dumps({'parameters':[],'constraint_catalog':{'concrete_entries':[
    {'constraint_id':'artificial_constraint','evaluation_channel':'predicate'}]}}))
(here/'manifest.json').write_text(json.dumps(manifest))
(here/'diagnostic-inventory.json').write_text(json.dumps({'diagnostics':[{'id':'heat','channel':'heat','kind':'physical_screen','interpretation':'equal_one','active_input':None}], 'unresolved_essential_evidence':[]}))
native={'state':'completed','run_kind':'blind','outputs':{'prediction':1.,'component':1.,'heat':0.},
        'verdicts':{'artificial_constraint':'satisfied'},'held_fallback':True,'missing_independent_inputs':['synthetic_missing_input']}
def run(n,o):
    np=temp/'native.json';op=temp/'observations.json';np.write_text(json.dumps(n));op.write_text(json.dumps(o))
    return compare(temp,np,op,here)
base=run(native,observations)
receipt={'adverse_heat_with_all_predicates_pass':base['engineering_evidence'],
         'fallback_report_keys':list(base),'fallback_numerical_pass':base['numerical_comparison']['pass']}
missing_verdicts=copy.deepcopy(observations);missing_verdicts['constraints']={}
r=run(native|{'outputs':native['outputs']|{'heat':1.},'verdicts':{}},missing_verdicts)
receipt['missing_predicate_inventory']={'constraints_complete':r['numerical_comparison']['constraints_complete'],
    'engineering_acceptance_withheld':r['engineering_evidence']['engineering_acceptance_withheld']}
bad=copy.deepcopy(observations);bad['quantities']['prediction']['model']['value']=2.
try:run(native,bad)
except ValueError as error:receipt['wrong_model_value_refused']=str(error)
else:raise AssertionError('wrong model value accepted')
bad=copy.deepcopy(observations);bad['constraints']['artificial_constraint']=False
try:run(native,bad)
except ValueError as error:receipt['wrong_predicate_refused']=str(error)
else:raise AssertionError('wrong predicate accepted')
missing=copy.deepcopy(observations);missing['quantities']['prediction']['reference']['value']=None
r=run(native,missing)
receipt['missing_reference_prediction']=next(row for row in r['numerical_comparison']['rows'] if row['id']=='prediction')
r=run(native|{'supplied_input_keys':['prediction']},observations)
receipt['supplied_prediction']=next(row for row in r['numerical_comparison']['rows'] if row['id']=='prediction')
assert not receipt['supplied_prediction']['independent_credit']
assert receipt['missing_reference_prediction']['status']=='blocked'
spec=importlib.util.spec_from_file_location('entering_accounts_review',HERE.parent/'check_entering_accounts.py')
accounts=importlib.util.module_from_spec(spec);spec.loader.exec_module(accounts)
receipt['entering_accounts']=accounts.check(ROOT)
assert receipt['entering_accounts']['status']=='pass'
receipt['reviewed_hashes']={str((HERE/name).relative_to(ROOT)):digest(HERE/name) for name in ('compare_candidate.py','diagnostic-inventory.json','check_accounting.py','account-inventory.json')}
Path(__file__).with_name('reporting-probe.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'account_checks':len(receipt['entering_accounts']['checks']),'account_status':receipt['entering_accounts']['status'],'fallback_report_keys':receipt['fallback_report_keys'],'fallback_numerical_pass':receipt['fallback_numerical_pass'],'missing_reference':receipt['missing_reference_prediction']['status'],'supplied_credit':receipt['supplied_prediction']['independent_credit']},indent=2))
