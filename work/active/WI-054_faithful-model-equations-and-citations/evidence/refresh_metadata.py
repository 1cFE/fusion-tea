"""Native snapshot and current-manifest refresh only; frozen studies untouched."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.study import manifest
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
rows={}
for family,folder,snapshot in [('mfe','stellarator_e2e','stellarator.snapshot.json'),('ife','ife_e2e','ife.snapshot.json')]:
    base=ROOT/'exploration'/folder;package=base/'generated'
    capture_instance_graph_snapshot([base/'models'],base/snapshot)
    path=base/'studies/manifest.json';original=path.read_text();data=json.loads(original);old=data['fingerprints']
    pin=manifest.indicator_input_fingerprint(package)
    data['fingerprints']={'indicator_inputs':{**pin,'files':[r['path'] for r in pin['files']]},'recorded_provenance':{'executable_fingerprint':manifest.read_executable_fingerprint(package),'semantic_fingerprint':manifest.read_semantic_fingerprint(package)}}
    validated=manifest.validate(data)
    if validated != json.loads(original):path.write_text(json.dumps(validated,indent=1)+'\n')
    loaded=manifest.load(path);manifest.assert_package_identity(loaded,package);manifest.assert_pin_matches(loaded,pin)
    rows[family]={'before':old,'after':data['fingerprints']}
contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text());by_type={}
for row in contract['parameters']:by_type.setdefault(row['entry_type'],[]).append(row['qualified_name'])
census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in by_type.items()}}
assert census==json.loads((ROOT/'tests/models/data/mfe_census.json').read_text())
(HERE/'derived-census.json').write_text(json.dumps(census,indent=2)+'\n')
(HERE/'metadata.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS both native snapshots/current manifests; unchanged MFE census')
