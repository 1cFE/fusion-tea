"""Refresh the five structural reachability expectations through the native producer."""
from pathlib import Path
import sys,json,pprint,re
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from tests.study.conftest import run_tool, DATA_DIR
from scripts.study.manifest import read_semantic_fingerprint
pkg=ROOT/'exploration/stellarator_e2e/generated'
report=run_tool(pkg,ROOT/'exploration/stellarator_e2e/studies/manifest.json', DATA_DIR/'axes.known_answers.json')
Path(__file__).with_name('indicator-report.json').write_text(json.dumps(report,indent=2)+'\n')
fp=read_semantic_fingerprint(pkg);contract={}
for group in report['groups']:
 axis=group['axis']
 (DATA_DIR/f'{axis}.expected.json').write_text(json.dumps({'derived_against_semantic_fingerprint':fp,'group':group},indent=2)+'\n')
 contract[axis]=(group['no_constraint_response'],sorted(x['source_local_identity'] for x in group['constraints_reachable']),group['objectives_reachable'],group['trace_size']['modules_fired'],group['trace_size']['channels_tainted'])
p=ROOT/'tests/study/test_known_answers.py';s=p.read_text();s=re.sub(r"EXPECTED_SEMANTIC_FINGERPRINT = '[^']+'",f'EXPECTED_SEMANTIC_FINGERPRINT = {fp!r}',s)
a=s.index('FIXTURE_CONTRACT = ');b=s.index('\n\n\n@pytest.fixture',a);s=s[:a]+'FIXTURE_CONTRACT = '+pprint.pformat(contract,sort_dicts=True)+s[b:];p.write_text(s)
print('Five expectation files and explicit contract rederived:',fp)
