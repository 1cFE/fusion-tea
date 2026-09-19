"""WI-071 bounded implementation receipts, not an uncertainty study."""
import json
import math
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
for path in [ROOT, ROOT/'exploration/stellarator_e2e/pkg', ROOT/'exploration/stellarator_e2e/studies']:
    sys.path.insert(0, str(path))
if os.environ.get('STOP_PARSER_TEAX_ROOT'):
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from simkit.study.bridge import CandidateBridge
import study_route
import oracle_entry

P = oracle_entry.P
KEY = P+'heat_transport__equipment_stainless_fabrication_usd2017_per_kg'
old = json.loads((HERE/'entering-baseline.json').read_text())
old_verdicts = {v['constraint_id']: v['status'] for v in old['verdicts']}
records=[]
with tempfile.TemporaryDirectory(prefix='wi071-implementation-') as tmp:
    engine=study_route.prepare(ROOT/'exploration/stellarator_e2e/generated',Path(tmp))
    bridge=CandidateBridge(engine.entry_models)
    for contingency in [.1,0.]:
        for rate in [310.,240.,360.]:
            inputs={KEY:rate,P+'contingency_rate':contingency}
            row=engine.evaluate(bridge.build(inputs))
            assert row.outputs, row
            expected=oracle_entry.evaluate(inputs)
            for k,value in expected.items():
                assert math.isclose(row.outputs[k],value,rel_tol=1e-9,
                    abs_tol=1e-18 if '__inventory__' in k else 1e-6),(rate,contingency,k)
            assert {k:row.responses[k] for k in old_verdicts}==old_verdicts
            nominal=(rate==310. and contingency==.1)
            if nominal:
                assert dict(row.outputs)==old['channels']
            records.append(dict(inputs=inputs,outputs=dict(row.outputs),responses=dict(row.responses),
                mapped_comparisons=len(expected),nominal_all_outputs_exact=nominal))
result=dict(purpose='Six implementation validation cases; no scenario-study or probability claim',
    records=records,mapped_comparisons=sum(r['mapped_comparisons'] for r in records),
    authored_predicate_comparisons=6*len(old_verdicts),nominal_exact_output_count=len(old['channels']),
    executed_cases=len(records),failed_calculations=0,all_checks_pass=True)
(HERE/'native-candidate-cases.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
