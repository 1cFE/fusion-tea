"""Refresh current native snapshot/manifest; verify unchanged public census."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.study import manifest
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
package=ROOT/'exploration/stellarator_e2e/generated'
capture_instance_graph_snapshot([ROOT/'exploration/stellarator_e2e/models'],ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json')
contract=json.loads((package/'contracts/model_contract.json').read_text())
by_type={}
for row in contract['parameters']:
    by_type.setdefault(row['entry_type'],[]).append(row['qualified_name'])
census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in by_type.items()}}
existing=json.loads((ROOT/'tests/models/data/mfe_census.json').read_text())
assert census==existing
(HERE/'corrected-derived-census.json').write_text(json.dumps(census,indent=2)+'\n')
path=ROOT/'exploration/stellarator_e2e/studies/manifest.json'
data=json.loads(path.read_text())
old=data['fingerprints']
pin=manifest.indicator_input_fingerprint(package)
data['fingerprints']={'indicator_inputs':{**pin,'files':[r['path'] for r in pin['files']]},'recorded_provenance':{'executable_fingerprint':manifest.read_executable_fingerprint(package),'semantic_fingerprint':manifest.read_semantic_fingerprint(package)}}
path.write_text(json.dumps(manifest.validate(data),indent=1)+'\n')
loaded=manifest.load(path)
manifest.assert_package_identity(loaded,package)
manifest.assert_pin_matches(loaded,pin)
(HERE/'corrected-metadata.json').write_text(json.dumps({'before':old,'after':data['fingerprints'],'census_equal':True},indent=2)+'\n')
print('PASS snapshot refreshed; census unchanged; current manifest identity/pin verified')
