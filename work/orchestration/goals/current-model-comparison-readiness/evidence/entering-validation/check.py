"""Read-only entering baseline and static diagnostic classification."""
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
for p in (ROOT, ROOT/'exploration/stellarator_e2e/studies', ROOT/'exploration/stellarator_e2e/pkg', Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'):
    sys.path.insert(0, str(p))
import study_route
paths = study_route.execute_baseline(HERE/'baseline')
actual = json.loads(paths['baseline_result'].read_text())
prior = json.loads((ROOT/'work/analysis/20260919-201643_stellarator-integrated-depth-reassessment.evidence/baseline_result.json').read_text())
receipt = {'outputs':len(actual['channels']), 'verdicts':len(actual['verdicts']), 'output_differences': {k:[prior['channels'].get(k),v] for k,v in actual['channels'].items() if prior['channels'].get(k)!=v}, 'missing_outputs':sorted(set(prior['channels'])-set(actual['channels'])), 'verdicts_exact':actual['verdicts']==prior['verdicts'], 'failed_verdicts':[v for v in actual['verdicts'] if v['status'] != 'satisfied']}
(HERE/'baseline-comparison.json').write_text(json.dumps(receipt,indent=2)+'\n')
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
old = json.loads((ROOT/'work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static-delta.json').read_text())
static = {}
normalize = lambda x:re.sub(r' at file:.*$', '', x)
for level,fn in [('2',validate_structure),('6',validate_architecture)]:
    r = fn(str(ROOT/'exploration/stellarator_e2e/models'))
    before,after = Counter(map(normalize,old[level]['issues'])),Counter(map(normalize,r.issues))
    categories = Counter(re.sub(r"(?: '.*|:.*)", '', s) for s in r.issues)
    static[level]={'success':r.success,'metrics':r.metrics,'issues':r.issues,'added':list((after-before).elements()),'removed':list((before-after).elements()),'categories':dict(categories)}
(HERE/'static.json').write_text(json.dumps(static,indent=2,default=str)+'\n')
print(json.dumps({'baseline':receipt, 'static':{k:{x:v[x] for x in ['success','metrics','categories','added','removed']} for k,v in static.items()}},indent=2))
