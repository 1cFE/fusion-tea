"""Independent static review; no model executions or package writes."""
import hashlib
import json
from pathlib import Path
import yaml

root = Path.cwd()
evidence = root / 'work/orchestration/goals/aries-integrated-design-studies/evidence'
audit = json.loads((evidence / 'audit-bindings.json').read_text())
package = root / 'exploration/aries_integrated/aries_integrated'
pipeline = yaml.safe_load((package / 'pipelines/pipeline.yaml').read_text())
for name, digest in audit['files'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
checked = []
for row in audit['attributes']:
    group = row['group']
    entries = json.loads((package / 'inputs' / (group + '.json')).read_text())
    keys = row['entry_keys']
    assert len(keys) == 1
    key = keys[0]
    assert entries[key] == row['baseline']
    assert key in (package / 'schemas' / (group + '.py')).read_text()
    actual = {(module, port, binding) for module, config in pipeline['modules'].items()
              for port, binding in config.get('inputs', {}).items()
              if isinstance(binding, str) and binding.split()[-1] == group + '.' + key}
    declared = {(x['module'], x['port'], x['binding']) for x in row['direct_consumers']}
    assert actual == declared and actual, key
    checked.append({'key': key, 'consumers': len(actual)})
contract = json.loads((package / 'contracts/model_contract.json').read_text())
assert audit['constraints'] == [{k: c[k] for k in ('constraint_id', 'owner_instance_path', 'source_local_identity', 'evaluation_channel')} for c in contract['constraint_catalog']['concrete_entries']]
handoff = json.loads((root / 'work/completed/20260922_WI-091_aries-integrated-lifecycle-cost/evidence/interface-handoff.json').read_text())
for name, value in audit['fingerprints'].items():
    assert handoff[name] == value
result = {'status': 'PASS', 'scope': 'Static file digests, actual input/schema fanout, constraint catalog and reviewed handoff identity; no native executions', 'files': audit['files'], 'fingerprints': audit['fingerprints'], 'attributes': checked, 'constraint_count': len(audit['constraints'])}
(evidence / 'axis-review-bindings.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
