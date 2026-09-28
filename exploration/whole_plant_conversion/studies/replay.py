"""Replay a sealed whole-plant study into a fresh repository-local directory.

Invoke with the prescribed .codex-test/run launcher and simkit PYTHONPATH.
The original record is read-only; every native case and stock oracle check reruns.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile

from scripts.study import common, manifest
from exploration.whole_plant_conversion.studies import execute_study, study_route as route


class ReplayError(ValueError):
    pass


def read(path):
    return json.loads(path.read_text())


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ReplayError(message)


def inside(root, relative):
    path = PurePosixPath(relative)
    require(not path.is_absolute() and '..' not in path.parts, 'unsafe recorded path: ' + relative)
    result = (root / relative).resolve()
    require(result.is_relative_to(root), 'recorded path escapes its root: ' + relative)
    return result


def runtime_check(integration):
    root = route.REPO_ROOT.resolve()
    require(Path(sys.prefix).resolve() == (root / '.venv').resolve(), 'use the sealed .codex-test/run interpreter')
    require(os.environ.get('UV_NO_SYNC') == 'true' and os.environ.get('UV_OFFLINE') == 'true', 'use .codex-test/run with synchronization disabled')
    require(os.environ.get('STOP_PARSER_TEAX_ROOT'), 'sealed integration environment is missing')
    teax_root = Path(os.environ['STOP_PARSER_TEAX_ROOT']).resolve()
    import simkit
    require(Path(simkit.__file__).resolve().is_relative_to(teax_root / 'packages/teax-simkit'), 'simkit PYTHONPATH does not select the sealed source tree')
    revision = subprocess.check_output(['git', '-C', str(teax_root), 'rev-parse', 'HEAD'], text=True).strip()
    require(revision == integration['toolchain']['teax_revision'], 'TEAx revision differs from the recorded toolchain')


def validate(record, out):
    root = route.REPO_ROOT.resolve()
    record, out = record.resolve(), out.resolve()
    require(record.is_relative_to(root) and out.is_relative_to(root), 'record and replay output must be repository-local')
    require(not out.exists(), 'replay output must be a fresh path; no overwrite or resume')
    require(not out.is_relative_to(record) and not record.is_relative_to(out), 'replay output must be separate from the sealed record')
    require((record / 'snapshot.json').is_file(), 'source study has no sealed snapshot yet')
    snapshot = read(record / 'snapshot.json')
    require(snapshot.get('record_status') == 'verified' and snapshot.get('released') is True, 'source study must be sealed and released')
    require(snapshot['study_id'] == record.name, 'source directory name differs from the sealed study identity')
    artifacts = {}
    for arm in snapshot['arms']:
        for item in arm['artifacts']:
            require(item['path'] not in artifacts or artifacts[item['path']] == item['sha256'], 'conflicting artifact hashes')
            artifacts[item['path']] = item['sha256']
    for name, expected in artifacts.items():
        path = inside(record, name)
        require(path.is_file() and sha(path) == expected, 'sealed artifact changed or missing: ' + name)
    required = ['proposed-points.json', 'preparation/candidate-freeze.json', 'sealed-package.tar.gz', 'manifest.json', 'integration/integration_return.json', 'integration/package_identity.json', 'results/manifest_used.json', 'results/integration_return_used.json']
    require(all(name in artifacts for name in required), 'snapshot omits required replay artifacts')
    integration = read(record / 'integration/integration_return.json')
    require(integration == read(record / 'results/integration_return_used.json'), 'integration receipt differs from executed receipt')
    require(integration.get('class') == 'CANDIDATE' and integration.get('exit_code') == 0, 'original integration candidate is not successful')
    runtime_check(integration)
    require(sha(record / 'manifest.json') == sha(record / 'results/manifest_used.json') == sha(route.MANIFEST_PATH), 'live manifest differs from executed manifest')
    require(sha(record / 'manifest.json') == snapshot['manifest']['digest'], 'manifest differs from snapshot digest')
    candidate = integration['candidate'];interface = route.interface()
    for name in ('executable_fingerprint', 'semantic_fingerprint'):
        require(candidate[name] == interface[name] == snapshot['fingerprints']['recorded_provenance.' + name], 'fingerprint mismatch: ' + name)
    loaded = manifest.load(route.MANIFEST_PATH)
    computed = manifest.indicator_input_fingerprint(route.PACKAGE_DIR)
    manifest.assert_pin_matches(loaded, computed)
    require(candidate['pin'] == loaded.pinned_digest == snapshot['fingerprints']['indicator_inputs']['digest'], 'live/snapshot indicator pin mismatch')
    require(snapshot['package']['package_name'] == route.PACKAGE_NAME, 'sealed archive names another package')
    common.assert_tree_clean(route.PACKAGE_DIR)
    live_files = {p.relative_to(route.PACKAGE_DIR).as_posix(): p for p in route.PACKAGE_DIR.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    archive_files = set()
    with tarfile.open(record / 'sealed-package.tar.gz', 'r:gz') as archive:
        for member in archive:
            require(member.isfile(), 'archive contains a non-regular member: ' + member.name)
            parts = PurePosixPath(member.name).parts
            require(parts and parts[0] == route.PACKAGE_NAME and '..' not in parts, 'unexpected package archive member')
            relative = '/'.join(parts[1:])
            require(relative in live_files and relative not in archive_files, 'archive/live package file set differs')
            with archive.extractfile(member) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            require(digest == sha(live_files[relative]), 'archive/live package bytes differ: ' + relative)
            archive_files.add(relative)
    require(archive_files == set(live_files), 'live package has files absent from archive')
    # The stock strict loader checks the live executable. Byte equality above
    # establishes the archive has the same executable, semantics, and input pin.
    with tempfile.TemporaryDirectory(prefix='whole-plant-replay-identity-') as tmp:
        prepared = route.prepare(route.PACKAGE_DIR, Path(tmp))
        require(prepared.fingerprint == candidate['executable_fingerprint'], 'strict loader fingerprint mismatch')
    source_prefix = 'results/sources/'
    checked_sources = []
    for name in artifacts:
        if not name.startswith(source_prefix):
            continue
        relative = name[len(source_prefix):]
        executable_source = (relative.startswith('exploration/whole_plant_conversion/') and (relative.endswith('.py') or Path(relative).name.startswith('oracle_') and relative.endswith('.json'))) or relative.startswith('scripts/study/') and relative.endswith('.py')
        if executable_source:
            live = inside(root, relative)
            require(live.is_file() and sha(live) == artifacts[name], 'restore frozen executable source before replay: ' + relative)
            checked_sources.append(relative)
    for module in (Path(__file__), Path(execute_study.__file__), Path(route.__file__)):
        require(module.resolve().relative_to(root).as_posix() in checked_sources, 'snapshot omits a replay execution source')
    frozen = read(record / 'preparation/candidate-freeze.json')
    require(sha(record / 'proposed-points.json') == frozen['artifact_sha256']['proposed-points.json'], 'proposed points differ from the pre-execution freeze')
    context = read(record / 'results/execution-context.json')
    require(sha(record / 'proposed-points.json') == context['proposal_sha256'], 'proposed points differ from original execution')
    points = read(record / 'proposed-points.json')['cases']
    require(len(points) == snapshot['case_count'] == frozen['unique_complete_points'], 'point count differs from sealed study')
    point_ids = set()
    for row in points:
        require(route.validate_proposal(row['point']) is not None, 'invalid complete proposal')
        digest = hashlib.sha256(json.dumps(row['point'], sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
        require(digest == row['point_id'] and digest not in point_ids, 'point identity differs or is duplicated')
        point_ids.add(digest)
    return record, out, snapshot, artifacts, len(points), checked_sources


def replay(record, out, check_only=False):
    record, out, snapshot, artifacts, count, sources = validate(record, out)
    context = {'source_record': str(record.relative_to(route.REPO_ROOT)), 'source_snapshot_sha256': sha(record / 'snapshot.json'), 'proposal_sha256': sha(record / 'proposed-points.json'), 'case_count': count, 'checked_executable_sources': sources, 'all_snapshot_artifact_hashes_verified': True, 'archive_matches_live_package': True}
    if check_only:
        print(json.dumps(dict(context, status='replay preflight passed; no study executed'), indent=2))
        return
    out.mkdir(parents=True, exist_ok=False)
    # Copy only immutable inputs and interpretation metadata. Native outputs are
    # created by execute_study through StudyRunner and its store lifecycle.
    for relative in ['proposed-points.json', 'manifest.json', 'window.json', 'framing.json', 'preparation', 'integration/integration_return.json', 'integration/package_identity.json']:
        source = record / relative;target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copyfile(source, target)
    common.write_document(context, out / 'replay-context.json')
    execute_study.execute(out, out / 'integration/integration_return.json')
    command = [sys.executable, str(route.REPO_ROOT / 'scripts/study/verify.py'), '--package', str(route.PACKAGE_DIR), '--manifest', str(route.MANIFEST_PATH), '--identity', str(out / 'integration/package_identity.json'), '--store', str(out / 'results/native' / (out.name + '.db')), '--sample-size', str(count), '--out', str(out / 'results/verification_summary.json')]
    with (out / 'verification.log').open('w') as log:
        subprocess.run(command, cwd=route.REPO_ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    verified = read(out / 'results/verification_summary.json')
    require(verified['outcome'] == 'pass' and sum(row['sampling']['sampled_rows'] for row in verified['stores']) == count, 'stock oracle did not verify every replay point')
    original = {row['case']: row for row in read(record / 'results/cases.json')['cases']}
    repeated = {row['case']: row for row in read(out / 'results/cases.json')['cases']}
    require(len(original) == len(repeated) == count and set(original) == set(repeated), 'replayed case labels differ')
    for label, before in original.items():
        after = repeated[label]
        for field in ('state', 'inputs', 'outputs', 'verdicts', 'executable_fingerprint'):
            require(before[field] == after[field], 'native replay differs from original: ' + label + ' / ' + field)
    for relative, digest in artifacts.items():
        require(sha(inside(record, relative)) == digest, 'original sealed artifact changed during replay: ' + relative)
    require(sha(record / 'snapshot.json') == context['source_snapshot_sha256'], 'original snapshot changed during replay')
    common.write_document(dict(context, outcome='pass', verification_command=command, verified_cases=count, exact_native_case_comparison='pass'), out / 'replay-summary.json')
    print(json.dumps({'outcome': 'pass', 'verified_cases': count, 'replay': str(out)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check-only', action='store_true', help='check sealed inputs and runtime without creating the replay directory')
    args = parser.parse_args()
    try:
        replay(args.record, args.out, args.check_only)
    except (ReplayError, common.ToolError, manifest.ManifestError) as error:
        parser.exit(1, str(error) + '\n')
