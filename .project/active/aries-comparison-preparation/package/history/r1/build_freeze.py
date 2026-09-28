"""Build a deterministic, content-indexed comparison overlay without secrets/holdout data.

Restore over the recorded entering Git revision. Existing model/evidence files come
from named tracked paths; this preparation package and its code/tests are explicit.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TRACKED_PATHS = [
    'models', 'exploration/stellarator_e2e/models', 'exploration/stellarator_e2e/generated',
    'exploration/stellarator_e2e/verify_stellaris.py', 'exploration/stellarator_e2e/studies/study_route.py',
    'exploration/stellarator_e2e/studies/oracle_entry.py', 'exploration/stellarator_e2e/studies/manifest.json',
    'exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer',
    'scripts/study', 'scripts/integrate.py', 'tests/study', 'tests/test_dependency_provenance.py',
    'work/orchestration/goals/bounded-feasibility-transfer',
    'work/orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md',
    'work/orchestration/goals/divertor-peak-heat-load/evidence/T-003_integration',
    '.project/completed/20260821_demo-anchor-acceptance-spec',
    'knowledge/holdout/aries-cs/PROTOCOL.md', 'pyproject.toml', 'uv.lock',
]
NEW_FILES = ['scripts/compare_fixed_point.py', 'tests/test_compare_fixed_point.py',
             'tests/test_frozen_comparison_execution.py',
             '.project/active/aries-comparison-preparation/spec.md',
             'work/orchestration/goals/aries-fixed-point-comparison-readiness/goal.md']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(out):
    names = set(subprocess.check_output(['git', 'ls-files', '--', *TRACKED_PATHS], cwd=ROOT, text=True).splitlines())
    names.update(NEW_FILES)
    names = {name for name in names if 'pkg_link' not in Path(name).parts}
    evidence = ROOT / 'work/orchestration/goals/aries-fixed-point-comparison-readiness/evidence'
    for p in evidence.rglob('*'):
        if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts:
            names.add(p.relative_to(ROOT).as_posix())
    for p in HERE.rglob('*'):
        if p.is_file() and not p.is_symlink() and not any(x in p.relative_to(HERE).parts for x in ('freeze', '__pycache__', 'pkg_link')):
            names.add(p.relative_to(ROOT).as_posix())
    files = {}
    for name in sorted(names):
        if name.startswith('knowledge/holdout/') and name != 'knowledge/holdout/aries-cs/PROTOCOL.md':
            raise ValueError('holdout content is forbidden in freeze')
        p = ROOT / name
        if p.is_symlink() or not p.resolve().is_relative_to(ROOT):
            raise ValueError(f'nonlocal or symbolic artifact: {name}')
        files[name] = p.read_bytes()
    sums = ''.join(f'{digest(data)}  {name}\n' for name, data in files.items()).encode()
    out.mkdir(parents=True, exist_ok=False)
    archive = out / 'comparison-freeze.tar.gz'
    with archive.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w', format=tarfile.PAX_FORMAT) as tar:
                for name, data in [*files.items(), ('COMPARISON-SHA256SUMS', sums)]:
                    info = tarfile.TarInfo(name)
                    info.size, info.mtime, info.mode, info.uid, info.gid = len(data), 0, 0o644, 0, 0
                    info.uname = info.gname = ''
                    tar.addfile(info, io.BytesIO(data))
    (out / 'SHA256SUMS').write_bytes(sums)
    record = {
        'schema_version': 1,
        'entering_revision': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'archive': archive.name, 'archive_sha256': digest(archive.read_bytes()),
        'file_count': len(files), 'archive_bytes': archive.stat().st_size,
        'index_sha256': digest(sums),
        'excluded': ['credentials/environment files', 'holdout contents except protocol', 'runtime caches/import links',
                     'freeze output directory', 'unrelated untracked owner files'],
        'runtime': 'Pinned licensed runtime is external; see freeze-procedure.md. No credentials are bundled.',
    }
    (out / 'freeze-record.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))


def verify(archive):
    with tarfile.open(archive, 'r:gz') as tar:
        members = tar.getmembers()
        names = [m.name for m in members]
        if len(names) != len(set(names)) or any(not m.isfile() or Path(m.name).is_absolute() or '..' in Path(m.name).parts for m in members):
            raise ValueError('unsafe or duplicate archive member')
        index = tar.extractfile('COMPARISON-SHA256SUMS').read().decode()
        expected = {line.split('  ',1)[1]:line.split('  ',1)[0] for line in index.splitlines()}
        if set(names) != set(expected) | {'COMPARISON-SHA256SUMS'}:
            raise ValueError('archive/index membership mismatch')
        for name, sha in expected.items():
            if digest(tar.extractfile(name).read()) != sha:
                raise ValueError(f'archive content mismatch: {name}')
    print(f'verified {len(expected)} frozen files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out-dir', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    verify(args.verify) if args.verify else build(args.out_dir)
