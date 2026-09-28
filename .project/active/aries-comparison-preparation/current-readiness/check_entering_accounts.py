"""Recheck the retained entering baseline; this does not execute a plant."""
import argparse
import json
import sys
import tempfile
from pathlib import Path


def check(root):
    here=root/'.project/active/aries-comparison-preparation/current-readiness/candidate'
    sys.path.insert(0,str(here))
    from candidate_common import digest
    from check_accounting import check as accounting
    source=root/'work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json'
    baseline=json.loads(source.read_text())
    rules=json.loads((here/'input-rules.json').read_text())
    with tempfile.TemporaryDirectory(prefix='current-entering-accounts-') as scratch:
        adapted=Path(scratch)/'adapted.json'
        adapted.write_text(json.dumps({'state':'completed','effective_inputs':rules['default_values']|baseline['point'],
            'outputs':baseline['channels'],'verdicts':{row['constraint_id']:row['status'] for row in baseline['verdicts']}}))
        result=accounting(root,adapted)
    return result|{'original_source':str(source.relative_to(root)),'original_source_sha256':digest(source),
                   'meaning':'Existing evidence adaptation; zero new physical evaluations'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();root=Path.cwd();sys.path.insert(0,str(root/'.project/active/aries-comparison-preparation/current-readiness/candidate'))
    from candidate_common import exclusive_document
    result,ok=exclusive_document(args.out,lambda:check(root))
    raise SystemExit(0 if ok and result['status']=='pass' else 1)
