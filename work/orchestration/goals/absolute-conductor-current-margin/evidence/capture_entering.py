"""Capture entering nineteen-predicate package before any current-margin changes."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if os.environ.get('STOP_PARSER_TEAX_ROOT'):
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))

from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values
from simkit.study.bridge import CandidateBridge

HERE = Path(__file__).resolve().parent
DEST = HERE / 'entering'
DEST.mkdir(exist_ok=True)
ROOT = Path('exploration/stellarator_e2e')
for rel in ('studies/oracle_entry.py', 'verify_stellaris.py', 'oracle_finance.py',
            'studies/manifest.json', 'generated/contracts/model_contract.json',
            'generated/contracts/package_contract.json', 'generated/inputs/stellarator_plant_params.json'):
    target = DEST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / rel, target)

prior = ROOT / 'studies/20260915-winding-pack-casing-fit/preparation/unique-proposals.json'
proposals = [{'proposal_id': 'reference', 'point': {}}] + json.loads(prior.read_text())
catalog = route._catalog_by_constraint_id(route.PACKAGE_DIR)
params = package_input_values(route.PACKAGE_DIR)
bindings = oe.operand_bindings()
rows = []
for proposal in proposals:
    channels = oe.evaluate(proposal['point'])
    verdicts = {entry['source_local_identity']: (
        'satisfied' if derive_verdict(cid, entry, bindings, proposal['point'], params, channels)[0]
        else 'violated') for cid, entry in catalog.items()}
    rows.append(proposal | {'channels': channels, 'verdicts': verdicts})
(DEST / 'comparison.json').write_text(json.dumps({
    'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    'scope': 'Entering independent-oracle evaluations; historical coordinates evaluated against current package',
    'rows': rows}, indent=2) + '\n')
with tempfile.TemporaryDirectory(prefix='current-margin-entering-') as tmp:
    evaluator = route.prepare(route.PACKAGE_DIR, Path(tmp))
    native = evaluator.evaluate(CandidateBridge(evaluator.entry_models).build({}))
    assert native.outputs
    (DEST / 'native-reference.json').write_text(json.dumps({
        'outputs': dict(native.outputs), 'responses': dict(native.responses)}, indent=2, default=str) + '\n')
route.write_identity_document(route.PACKAGE_DIR, DEST / 'package-identity.json')
print(f'Captured {len(rows)} entering oracle cases, native reference and package identity')
