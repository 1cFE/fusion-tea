"""Compare diagnostic identities against the retained entering model copy."""
import argparse
import json
from pathlib import Path
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def rows(result):
    return {json.dumps({'code': str(i.code), 'severity': str(i.severity),
                       'element': i.element_name, 'message': i.message}, sort_keys=True)
            for i in result.structured_issues}


parser = argparse.ArgumentParser()
parser.add_argument('--entering-models', required=True)
args = parser.parse_args()
report = {}
for name, check in [('L2', validate_structure), ('L6', validate_architecture)]:
    before = check(args.entering_models)
    after = check(str(ROOT / 'exploration/stellarator_e2e/models'))
    a, b = rows(before), rows(after)
    report[name] = {'before_success': before.success, 'after_success': after.success,
                    'before_count': len(before.structured_issues), 'after_count': len(after.structured_issues),
                    'removed': [json.loads(x) for x in sorted(a-b)],
                    'added': [json.loads(x) for x in sorted(b-a)],
                    'unchanged_identities': len(a & b)}
(HERE / 'validation-delta.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
