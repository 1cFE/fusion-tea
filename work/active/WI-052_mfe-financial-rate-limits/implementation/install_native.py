"""Install the verified native family after checking the entering production bytes."""
import json
import shutil
from regenerate import HERE,ROOT,PRODUCTION,hashes,seed_inventory,NAMES
from tests.models.test_model_family_spines import _by_entry_type
recorded=HERE/'production-hashes.json'
before=json.loads(recorded.read_text()) if recorded.exists() else json.loads((HERE/'entering/inventory.json').read_text())['package']
expected=dict(before,**seed_inventory())
assert hashes(PRODUCTION)==expected,'Concurrent production drift beyond explicitly edited finance seeds'
record=json.loads((HERE/'regeneration.json').read_text());scratch=__import__('pathlib').Path(record['destination'])
assert hashes(scratch/'generated')==record['inventory']
shutil.rmtree(PRODUCTION)
shutil.copytree(scratch/'generated',PRODUCTION,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
assert hashes(PRODUCTION)==record['inventory']
shutil.copyfile(scratch/'stellarator.snapshot.json',ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json')
contract=json.loads((PRODUCTION/'contracts/model_contract.json').read_text())
census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in _by_entry_type(PRODUCTION).items()}}
(ROOT/'tests/models/data/mfe_census.json').write_text(json.dumps(census,indent=2)+'\n')
(HERE/'production-hashes.json').write_text(json.dumps(hashes(PRODUCTION),indent=2)+'\n')
print('PASS guarded native installation; generated snapshot and census refreshed')
