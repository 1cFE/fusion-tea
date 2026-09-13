"""Independently derive baseline/candidate/final JUnit failure and skip identities."""
from collections import Counter
import json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path.cwd();native=ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence';coding=ROOT/'.project/active/mfe-domain-study-package/implementation'
def cases(path):
    rows={}
    for case in ET.parse(path).getroot().iter('testcase'):
        identity=case.attrib['classname']+'::'+case.attrib['name']
        assert identity not in rows,identity
        status=next((name for name in ['failure','error','skipped'] if case.find(name) is not None),'passed')
        rows[identity]=status
    return rows
old=cases(native/'baseline-models.xml');candidate=cases(native/'candidate-models.xml');final=cases(coding/'regressions-models-final.xml')
fails=lambda rows:{k for k,v in rows.items() if v in ['failure','error']}
new=fails(candidate)-fails(old);inherited=fails(candidate)&fails(old)
assert len(new)==63 and len(inherited)==1
changed=lambda name:name.replace('test_peak_component_preserves_open_f07','test_peak_component_preserves_valid_and_rejects_invalid_domains')
assert all(final[changed(name)]=='passed' for name in new|inherited)
assert not fails(final)
assert {k for k,v in old.items() if v=='skipped'}=={k for k,v in final.items() if v=='skipped'}
assert Counter(final.values())=={'passed':566,'skipped':13}
assert {changed(k) for k in candidate}==set(final)
result={'entering':dict(Counter(old.values())),'candidate':dict(Counter(candidate.values())),'final':dict(Counter(final.values())),'resolved_new':sorted(new),'resolved_inherited':sorted(inherited),'skips_identical':True,'all_candidate_nodes_accounted_for':True}
(ROOT/'work/analysis/20260913_domain-audit-evidence/regression-identity-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('Independent raw-JUnit join: 63 new and 1 inherited failure resolved; all candidate nodes accounted for; exact 13 inherited skips')
