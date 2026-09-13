"""Generate into guarded fresh destinations with exactly four normative manual seeds."""
import json
import shutil
import sys
from pathlib import Path
from common import H, ROOT, FROZEN, PRODUCTION, dump, hashes, sha

MANUAL = json.loads((FROZEN/'manual-preservation.json').read_text())
NAMES = {
    'handwritten/mfe_lifecycle/lifecycle_calendar_impl.py',
    'handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py',
    'handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py',
    'handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py',
}
assert set(MANUAL) == NAMES


def fresh_directory(path):
    """Refuse any nonempty/non-directory/symlink destination without modifying it."""
    path = Path(path)
    if path.is_symlink():
        raise FileExistsError(f'Symlink generation destination refused: {path}')
    if path.exists():
        if not path.is_dir() or any(path.iterdir()):
            raise FileExistsError(f'Nonempty or non-directory destination refused: {path}')
        state = 'real empty directory (including hidden entries)'
    else:
        path.mkdir(parents=False, exist_ok=False)
        state = 'absent; created exclusively'
    return {'path': str(path), 'entering_state': state}


def seed_and_generate(path, source, *, generator=None, **kwargs):
    """Single path used by both native routes and kept refusal tests."""
    if generator is None:
        from sysml_codegen.cli import run_codegen
        generator = run_codegen
    from sysml_codegen.cli import GenerationConfig
    state = fresh_directory(path)
    (path.parent/(path.name+'-freshness.json')).write_text(json.dumps(state,indent=2)+'\n')
    # Validate all originals before copying any seed. Nothing else is copied.
    for name, expected in MANUAL.items():
        if not (source/name).is_file() or (source/name).is_symlink() or sha(source/name)!=expected:
            raise ValueError(f'Missing or mismatched normative seed: {name}')
    for name in MANUAL:
        target=path/name; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source/name,target)
    verify_seed_inventory(path)
    assert generator(GenerationConfig(output_path=path,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,**kwargs))
    assert all(sha(path/name)==expected for name,expected in MANUAL.items())
    return state


def verify_seed_inventory(path):
    if hashes(path) != MANUAL:
        raise ValueError('Seed inventory must equal exactly the four normative paths and hashes')


def generate():
    from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
    seed_and_generate(H/'source-attempt-1',H/'entering-package',models_path=H/'models')
    snapshot=H/'instance_graph_snapshot.json'
    assert not snapshot.exists()
    capture_instance_graph_snapshot([H/'models'],snapshot)
    seed_and_generate(H/'snapshot-attempt-1',H/'entering-package',from_snapshot=snapshot)
    live=hashes(H/'source-attempt-1'); snapshot_files=hashes(H/'snapshot-attempt-1')
    assert live==snapshot_files
    bodies=[name for name in live if name.startswith('handwritten/') and name.endswith('_impl.py')]
    assert len(set(bodies)-NAMES)==65
    dump('generated-hashes.json',live)
    dump('generation.json',{'source_equals_snapshot':True,'manual':MANUAL,'fresh_nonmanual_bodies':sorted(set(bodies)-NAMES),'source_hashes':hashes(H/'models'),'snapshot_sha256':sha(snapshot)})
    print('Fresh source/snapshot packages equal; exactly four manual and 65 fresh generated bodies')


def promote():
    sys.path.insert(0,str(ROOT))
    from tests.models.test_model_family_spines import _by_entry_type
    expected=json.loads((H/'entering.json').read_text())['package']
    assert hashes(PRODUCTION)==expected, 'Concurrent production package change'
    assert (H/'contract-checks.json').exists()
    new=H/'source-attempt-1'
    assert hashes(new)==json.loads((H/'generated-hashes.json').read_text())
    shutil.rmtree(PRODUCTION)
    shutil.copytree(new,PRODUCTION,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    assert hashes(PRODUCTION)==hashes(new)
    shutil.copyfile(H/'instance_graph_snapshot.json',ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json')
    contract=json.loads((PRODUCTION/'contracts/model_contract.json').read_text())
    census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in _by_entry_type(PRODUCTION).items()}}
    (ROOT/'tests/models/data/mfe_census.json').write_text(json.dumps(census,indent=2)+'\n')
    dump('production-hashes.json',hashes(PRODUCTION))
    print('Published verified package, fresh snapshot and re-derived census')

if __name__=='__main__':
    promote() if sys.argv[1:]==['promote'] else generate()
