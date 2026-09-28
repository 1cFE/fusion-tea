"""Fresh completion review: committed AST, preservation and exact affected identities."""
import ast
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
R=Path.cwd()
I=R/'work/active/WI-052_mfe-financial-rate-limits'
C=R/'.project/active/mfe-financial-study-package'
A=I/'completion-audit-evidence'
def git(*args):
    return subprocess.check_output(['git',*args],text=True)
def prior(rev,path):
    return git('show',rev+':'+path)
def executable(text):
    tree=ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
            node.body.pop(0)
    return ast.dump(tree)
changed=git('diff','--name-only','59b1ff97','708dddef','--','models','exploration/stellarator_e2e/generated','exploration/stellarator_e2e/models').splitlines()
checks=[]
for path in changed:
    if path.endswith('.py'):
        assert executable(prior('59b1ff97',path))==executable(prior('708dddef',path)),path
        checks.append(path)
    elif path.endswith('.sysml'):
        strip=lambda s:re.sub(r'doc /\*.*?\*/','',s,flags=re.S)
        assert strip(prior('59b1ff97',path))==strip(prior('708dddef',path)),path
for file,names in {'mfe_account_costs.sysml':['IDC Closed-Form Cost','Levelized Annual Cost'],'mfe_lcoe_dcf.sysml':['LCOE DCF'],'mfe_lifecycle.sysml':['Lifecycle Calendar']}.items():
    path=R/'models/library/analyses'/file
    assert path.read_bytes()==(R/'exploration/stellarator_e2e/models/analyses'/file).read_bytes()
    for name in names:
        block=path.read_text().split("calc def '"+name+"'",1)[1].split('*/',1)[0]
        source=block.rsplit('**Source**: ',1)[1].splitlines()[0]
        assert (R/source).is_file(),source
fuel=(R/'models/library/analyses/mfe_account_costs.sysml').read_text().split("calc def 'DT Fuel Cost'",1)[1].split('*/',1)[0]
assert 'generate the fuel arithmetic directly' in fuel and 'manual completion' not in fuel
protected=json.loads((C/'implementation/preservation.json').read_text())['protected_git_paths']
assert not git('diff','--name-only','708dddef','6140321','--',*protected)
# Only the current live manifest and annex may differ inside studies; dated records remain unchanged.
assert set(git('diff','--name-only','708dddef','6140321','--','exploration/stellarator_e2e/studies').splitlines()) <= {'exploration/stellarator_e2e/studies/manifest.json','exploration/stellarator_e2e/studies/ANNEX.md'}
old=json.loads(prior('708dddef','exploration/stellarator_e2e/studies/manifest.json'))
new=json.loads((R/'exploration/stellarator_e2e/studies/manifest.json').read_text())
for v in (old,new):
    v.pop('fingerprints');v['baseline']['headline'].pop('value')
assert old==new
original=json.loads((I/'implementation/new-downstream-failures.json').read_text())
if isinstance(original,dict):
    print('original keys',list(original))
rows=json.loads((C/'implementation/affected-differential.json').read_text())
xml=ET.parse(C/'implementation/affected-nodes.xml')
statuses={x.attrib['classname'].replace('.','/')+'.py::'+x.attrib['name']:('passed' if len(x)==0 or all(y.tag=='properties' for y in x) else 'not-passed') for x in xml.iter('testcase')}
ids={x['node_id'] for x in rows}
assert len(ids)==22 and ids==set(statuses) and all(statuses[x]=='passed' for x in ids)
original_ids={x['node_id'] for x in original}
assert original_ids==ids
assert json.loads((I/'repair-1/native.json').read_text())==json.loads((I/'audit-evidence/native-absolute/native.json').read_text())
assert ast.parse((R/'exploration/stellarator_e2e/oracle_finance.py').read_text()).body[1].module=='decimal'
result={'reviewed_revision':'614032136b7918a47a889a73147ca51dc15511e2','doc_only_python_asts':checks,'non_doc_sysml_equal':True,'direct_source_fields':4,'fuel_description_correct':True,'protected_paths_unchanged':protected,'manifest_only_provenance_and_headline_change':True,'retained_affected_node_statuses':statuses,'doc_repair_ten_cases_exact_to_prior_independent_audit':True}
(A/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
# Fresh native execution and isolated producer output versus retained records.
import shutil
assert json.loads((A/'native.json').read_text())==json.loads((I/'repair-1/native.json').read_text())
metadata=Path('/tmp/wi052-audit-metadata')
record=json.loads((C/'implementation/metadata-reproduction.json').read_text())
import hashlib
for name in record['byte_identical_outputs']:
    assert hashlib.sha256((metadata/name).read_bytes()).hexdigest()==record['produced_output_hashes'][name],name
assert (metadata/'manifest.json').read_bytes()==(R/'exploration/stellarator_e2e/studies/manifest.json').read_bytes()
route_files=[Path('/tmp/wi052-completion-audit-tests/test_current_rate_route_and_co0/finance-route-evidence.json')]
assert len(route_files)==1
route=json.loads(route_files[0].read_text())
assert len(route['cases'])==30 and len(route['covered_finance'])==7
worst=max(abs((v['native']-v['oracle'])/v['oracle']) if v['oracle'] else abs(v['native']) for row in route['cases'] for v in row['finance'].values())
assert worst<=1e-9
shutil.copyfile(route_files[0],C/'audit-evidence/finance-route-evidence.json')
shutil.copyfile(Path('/tmp/wi052-completion-audit-tests/test_current_radius_controls_m0/controls.json'),C/'audit-evidence/radius-controls.json')
result.update({'fresh_ten_case_native_exact':True,'fresh_metadata_hashes_equal_to_retained':record['byte_identical_outputs'],'fresh_route_cases':30,'fresh_route_worst_finance_relative_deviation':worst,'fresh_input_coverage':[len(route['mapping']),len(route['native_inputs'])],'fresh_output_coverage':[len(route['oracle_mapping']),len(route['native_outputs'])]})
(A/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('FRESH native, metadata and route comparisons PASS',worst)
from collections import Counter
import importlib.util
spec=importlib.util.spec_from_file_location('identity_rules',I/'implementation/differentials.py')
diff=importlib.util.module_from_spec(spec);spec.loader.exec_module(diff)
old=json.loads((I/'implementation/entering/issues-mirror.json').read_text())
new=json.loads((A/'issues.json').read_text())
identities=[]
for a,b in zip(old,new):
    assert a['level']==b['level']
    assert Counter(map(diff.identity,a['issues']))==Counter(map(diff.identity,b['issues']))
    assert a['warnings']==b['warnings'] and a['success']==b['success']
    identities.append({'level':b['level'],'success':b['success'],'retained_issues':len(b['issues']),'new_issues':0})
(A/'validation-identities.json').write_text(json.dumps(identities,indent=2)+'\n')
print('FRESH six-level issue identity comparison PASS',identities)
