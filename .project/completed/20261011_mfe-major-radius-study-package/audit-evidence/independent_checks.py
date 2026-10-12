import ast,hashlib,json,math,subprocess
from pathlib import Path
root=Path.cwd(); out=root/'.project/active/mfe-major-radius-study-package/audit-evidence'; impl=out.parent/'implementation'; p='stellarator_09__stellaris__'
def load(path): return json.loads(Path(path).read_text())
def mapping(source):
    tree=ast.parse(source)
    assignment=next(n for n in tree.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=='ENTRY_KEY_TO_ORACLE_INPUT')
    return eval(compile(ast.Expression(assignment.value),'<mapping-only>','eval'),{'P':p})
file='exploration/stellarator_e2e/studies/oracle_entry.py'
old=mapping(subprocess.check_output(['git','show','f07015bb:'+file],text=True)); new=mapping((root/file).read_text()); coverage=load(impl/'contract-coverage.json')
assert old==coverage['entering_mapping'] and len(old)==100 and len(new)==99
assert new=={k:v for k,v in old.items() if k!=p+'magnet__R0'}
controls=load(out/'controls/controls.json'); native=load(out/'native/results.json'); frozen=load(root/'work/active/WI-051_mfe-model-owned-major-radius/prototype/frozen-results.json')
worst=0; summary={}
for name,old_name in [('baseline','baseline'),('R14','tied_R14')]:
    case=controls[name]; expect=frozen['cases'][old_name]['native']; assert len(case['outputs'])==158
    assert case['outputs']==native[name]['outputs']
    assert native[name]['responses']==expect['responses'] and len(expect['responses'])==19
    assert len(case['verdicts'])==18
    for key,row in case['oracle_channels'].items():
        assert math.isclose(row['oracle'],expect['outputs'][key],rel_tol=1e-9,abs_tol=1e-9)
        worst=max(worst,row['relative_deviation'])
    summary[name]={'native_scalars':len(case['outputs']),'oracle_channels':len(case['oracle_channels']),'verdicts':case['verdicts'],'responses_exact':True}
assert controls['baseline']['inputs']=={} and controls['R14']['inputs']=={p+'R':14.0}
# Independently spell geometry expectations, not values freshly generated from the plant.
ratio_expect={'geom__V':14/12.7,'coil_length__c_coil':14/12.7,'field_calc__B_axis':12.7/14,'stored_energy__W_mag':12.7/14,'peak_field_calc__B_peak':(12.7-3.1500000000000004)/(14-3.1500000000000004)}
ratios={}
for suffix,expected in ratio_expect.items():
    key=p+suffix; actual=controls['R14']['outputs'][key]/controls['baseline']['outputs'][key]; assert math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9); ratios[key]={'expected':expected,'actual':actual}
expectations=root/'work/active/WI-051_mfe-model-owned-major-radius/prototype/expectations.json'
assert hashlib.sha256(expectations.read_bytes()).hexdigest()=='a16c0731e81230060d6c74d0cc93189445ba7f4c06bb002ab2338fe07b25648a'
(out/'independent-checks.json').write_text(json.dumps({'mapping_old':len(old),'mapping_new':len(new),'survivors_unchanged':True,'controls':summary,'ratios':ratios,'worst_all_oracle_deviation':worst,'expectations_handoff_hash_exact':True},indent=2)+'\n')
print('PASS independent mapping extraction, actual/frozen outputs, exact native responses, geometric ratios, frozen expectations digest; worst oracle deviation',worst)
