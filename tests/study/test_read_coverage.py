"""Actual Python opens, imports and route-gate refusals; no public-input proxies."""
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import integrate
from scripts.study import read_coverage as coverage


@pytest.fixture
def observed_route(tmp_path):
    package = tmp_path / "package"
    (package / "contracts").mkdir(parents=True)
    value = package / "value.json"
    value.write_text('{"value": 3}')
    (package / "contracts/package_contract.json").write_text(json.dumps({
        "artifact_hashes": {"value.json": coverage.digest(value)},
    }))
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{}')
    route = tmp_path / "route"
    route.mkdir()
    out = tmp_path / "out"
    out.mkdir()
    request = SimpleNamespace(route=(route, "probe_route", "execute"), package=package,
                              manifest=manifest, out_dir=out)

    def write(body):
        (route / "probe_route.py").write_text(
            'from pathlib import Path\nimport sys, os, subprocess\n'
            'def execute(out, *, package_dir, manifest_path):\n'
            + ''.join('    ' + line + '\n' for line in body.splitlines())
            + '    return {}\n'
        )

    def run(body):
        write(body)
        done = subprocess.run([sys.executable, '-c', integrate.ROUTE_DRIVER_SOURCE,
                               str(route), 'probe_route', 'execute', str(out),
                               str(package), str(manifest), 'test-token'],
                              text=True, capture_output=True)
        return done, json.loads((out / 'read_coverage.json').read_text())

    return SimpleNamespace(package=package, route=route, manifest=manifest, out=out,
                           request=request, run=run, write=write)


def test_declared_package_manifest_and_source_reads(observed_route):
    done, receipt = observed_route.run('''(package_dir / "value.json").read_text()
manifest_path.read_text()''')
    assert done.returncode == 0, done.stderr
    assert receipt['outcome'] == 'pass'
    assert {'package-seal', 'manifest', 'declared-source'} <= {r['category'] for r in receipt['reads']}


@pytest.mark.parametrize('location', ['package', 'route', 'outside'])
def test_undeclared_actual_data_reads(observed_route, tmp_path, location):
    roots = {'package': observed_route.package, 'route': observed_route.route, 'outside': tmp_path}
    unexpected = roots[location] / 'unexpected.csv'
    unexpected.write_text('changed data')
    done, receipt = observed_route.run(f'Path({str(unexpected)!r}).read_text()')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


def test_symlink_escape(observed_route, tmp_path):
    outside = tmp_path / 'external.json'
    outside.write_text('outside')
    (observed_route.package / 'escape.json').symlink_to(outside)
    done, receipt = observed_route.run('(package_dir / "escape.json").read_text()')
    assert done.returncode != 0
    assert str(outside) in str(receipt['violations'])


@pytest.mark.parametrize('when', ['before', 'after'])
def test_declared_dependency_mutation(observed_route, when):
    read = '(package_dir / "value.json").read_text()'
    write = '(package_dir / "value.json").write_text("mutated")'
    done, receipt = observed_route.run('\n'.join([write, read] if when == 'before' else [read, write]))
    assert done.returncode != 0
    assert 'changed' in str(receipt['violations'])


def test_new_output_can_be_read(observed_route):
    done, receipt = observed_route.run('''(out / "new.json").write_text("new")
(out / "new.json").read_text()''')
    assert done.returncode == 0, done.stderr
    assert any(r['category'] == 'new-output' for r in receipt['reads'])


@pytest.mark.parametrize('mode', ['a', 'r+'])
def test_preexisting_output_write_does_not_admit_old_data(observed_route, mode):
    (observed_route.out / 'old.json').write_text('old')
    done, receipt = observed_route.run(f'''with (out / "old.json").open({mode!r}) as handle:
    handle.write("new")
(out / "old.json").read_text()''')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


@pytest.mark.parametrize('mutate', [False, True])
def test_cached_import_records_actual_cache_and_source(observed_route, mutate):
    source = observed_route.route / 'cached_dependency.py'
    source.write_text('VALUE = 7\n')
    cache = Path(py_compile.compile(str(source), doraise=True))
    original = coverage.digest(cache)
    body = 'import cached_dependency\nassert cached_dependency.VALUE == 7'
    if mutate:
        body += f'\nPath({str(cache)!r}).write_bytes(b"changed cached bytes")'
    done, receipt = observed_route.run(body)
    assert (done.returncode != 0) is mutate
    row = next(row for row in receipt['reads'] if row['path'] == str(cache))
    assert row['category'] == 'bytecode'
    assert row['sha256'] == original
    assert any(row['path'] == str(source) for row in receipt['reads'])
    if mutate:
        assert 'changed after read' in str(receipt['violations'])


def test_sourceless_bytecode_refused(observed_route):
    source = observed_route.route / 'only_cache.py'
    source.write_text('VALUE = 3\n')
    py_compile.compile(str(source), cfile=str(source.with_suffix('.pyc')), doraise=True)
    source.unlink()
    done, receipt = observed_route.run('import only_cache')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


def test_child_process_refused(observed_route):
    done, receipt = observed_route.run('subprocess.run([sys.executable, "-c", "pass"])')
    assert done.returncode != 0
    assert 'child execution' in str(receipt['violations'])


def test_integer_descriptor_is_explicitly_unsupported(observed_route):
    done, receipt = observed_route.run('''fd = os.open(package_dir / "value.json", os.O_RDONLY)
with open(fd) as handle:
    handle.read()''')
    assert done.returncode != 0
    assert 'integer-descriptor' in str(receipt['violations'])


def test_caught_violation_still_refuses_integration(observed_route):
    extra = observed_route.package / 'unlisted.csv'
    extra.write_text('unexpected')
    observed_route.write('''try:
    (package_dir / "unlisted.csv").read_text()
except RuntimeError:
    pass''')
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.execute_baseline(observed_route.request, dict(os.environ))
    assert caught.value.condition == 'read-coverage-refused'
    receipt = json.loads((observed_route.out / 'read_coverage.json').read_text())
    assert receipt['violations']
    assert caught.value.evidence


@pytest.mark.parametrize('receipt_kind', ['missing', 'malformed', 'stale', 'empty', 'violation'])
def test_integration_rejects_invalid_receipt_even_on_zero_exit(observed_route, monkeypatch, receipt_kind):
    path = observed_route.out / 'read_coverage.json'
    path.write_text('{"outcome":"pass"}')  # Existing evidence cannot satisfy new invocation.

    def fake_producer(argv, env):
        assert not path.exists()
        if receipt_kind == 'malformed':
            path.write_text('not json')
        elif receipt_kind != 'missing':
            document = {'schema_version': coverage.SCHEMA,
                        'invocation': 'old-token' if receipt_kind == 'stale' else argv[-1],
                        'outcome': 'pass', 'route_error': None,
                        'violations': ['caught'] if receipt_kind == 'violation' else [],
                        'reads': [], 'declarations': [], 'limitations': coverage.LIMITATIONS}
            path.write_text(json.dumps(document))
        return subprocess.CompletedProcess(argv, 0, '{}', '')

    monkeypatch.setattr(integrate, 'run_producer', fake_producer)
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.execute_baseline(observed_route.request, {})
    assert caught.value.condition == 'read-coverage-refused'


def test_integration_tool_identity_includes_new_dependencies():
    identity = integrate.common.tool_source_digest(integrate.TOOL_SOURCE_FILES)
    assert {'scripts/study/indicators.py', 'scripts/study/read_coverage.py'} <= {entry['path'] for entry in identity['files']}


def test_static_gate_rejects_unpinned_pipeline_reference(synthetic_copy, tmp_path):
    package = synthetic_copy.path
    pipeline = next((package / 'pipelines').glob('*.yaml'))
    text = pipeline.read_text()
    # Redirect an actual EntryPoint ref, leaving the manifest glob unchanged.
    import re
    match = re.search(r'\.\./inputs/[^\s\"\']+\.json', text)
    assert match, text
    pipeline.write_text(text.replace(match.group(), '../outside.json', 1))
    (package / 'outside.json').write_text('{}')
    synthetic_copy.repin()
    request = SimpleNamespace(manifest=synthetic_copy.manifest, package=package, out_dir=tmp_path)
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.gate_manifest(request, {}, None)
    assert caught.value.condition == 'manifest-stale'
    assert 'not in the manifest' in caught.value.detail


def test_route_failure_preserves_earlier_violation(observed_route):
    observed_route.write('try:\n    (package_dir / "unknown.txt").read_text()\nexcept RuntimeError:\n    pass\nraise ValueError("route failed too")')
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.execute_baseline(observed_route.request, dict(os.environ))
    receipt = json.loads((observed_route.out / 'read_coverage.json').read_text())
    assert receipt['violations']
    assert receipt['route_error'] == 'ValueError: route failed too'
    assert caught.value.condition == 'read-coverage-refused'


def test_static_gate_produces_coverage_receipt(synthetic_copy, tmp_path):
    request = SimpleNamespace(manifest=synthetic_copy.manifest, package=synthetic_copy.path, out_dir=tmp_path)
    integrate.gate_manifest(request, {}, None)
    receipt = json.loads((tmp_path / 'manifest_read_coverage.json').read_text())
    assert receipt['outcome'] == 'pass'
    assert any('/inputs/' in path for path in receipt['paths'])


@pytest.mark.parametrize('preexisting', [False, True])
def test_atomic_output_rename_preserves_only_new_admission(observed_route, preexisting):
    if preexisting:
        (observed_route.out / 'final.json').write_text('old')
    done, receipt = observed_route.run('''(out / "temp.json").write_text("new")
(out / "temp.json").replace(out / "final.json")
(out / "final.json").read_text()''')
    assert (done.returncode != 0) is preexisting, done.stderr
    assert bool(receipt['violations']) is preexisting


def test_receipt_structural_validation(observed_route):
    done, receipt = observed_route.run('(package_dir / "value.json").read_text()')
    assert done.returncode == 0
    assert coverage.valid_receipt(receipt, 'test-token')
    receipt['reads'] = ['unstructured']
    assert not coverage.valid_receipt(receipt, 'test-token')


def test_declared_dependency_metadata_change(observed_route, monkeypatch, tmp_path):
    teax = tmp_path / 'teax'
    metadata = teax / 'packages/teax-simkit/probe.egg-info/entry_points.txt'
    metadata.parent.mkdir(parents=True)
    metadata.write_text('original')
    monkeypatch.setenv('STOP_PARSER_TEAX_ROOT', str(teax))
    done, receipt = observed_route.run(f'Path({str(metadata)!r}).read_text()\nPath({str(metadata)!r}).write_text("changed")')
    assert done.returncode != 0
    assert 'changed after read' in str(receipt['violations'])
    assert any(r['category'] == 'declared-dependency-metadata' for r in receipt['reads'])


def test_route_exception_without_coverage_violation_is_could_not_run(observed_route):
    observed_route.write('(package_dir / "value.json").read_text()\nraise ValueError("unsupported physics domain")')
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.execute_baseline(observed_route.request, dict(os.environ))
    assert caught.value.mode == integrate.COULD_NOT_RUN
    assert caught.value.condition != 'read-coverage-refused'
    receipt = json.loads((observed_route.out / 'read_coverage.json').read_text())
    assert receipt['violations'] == []
    assert 'unsupported physics domain' in receipt['route_error']
    assert caught.value.evidence


@pytest.mark.parametrize('replacement', ['rename', 'replace', 'hardlink', 'symlink'])
def test_output_admission_cannot_survive_old_content_replacement(observed_route, replacement):
    (observed_route.out / 'old.json').write_text('old untracked content')
    moves = {
        'rename': '(out / "old.json").rename(out / "temp.json")',
        'replace': '(out / "old.json").replace(out / "temp.json")',
        'hardlink': 'os.link(out / "old.json", out / "temp.json")',
        'symlink': '(out / "temp.json").symlink_to(out / "old.json")',
    }
    done, receipt = observed_route.run('''(out / "temp.json").write_text("new")
(out / "temp.json").rename(out / "final.json")
''' + moves[replacement] + '\nassert (out / "temp.json").read_text() == "old untracked content"')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


def test_replacement_revokes_current_destination_admission(observed_route):
    (observed_route.out / 'old.json').write_text('old untracked content')
    done, receipt = observed_route.run('''(out / "new.json").write_text("new")
(out / "old.json").replace(out / "new.json")
assert (out / "new.json").read_text() == "old untracked content"''')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


@pytest.mark.parametrize('replacement', ['rename', 'hardlink'])
def test_unlink_revokes_admission_before_old_file_replacement(observed_route, replacement):
    (observed_route.out / 'old.json').write_text('old')
    move = '(out / "old.json").rename(out / "new.json")' if replacement == 'rename' else 'os.link(out / "old.json", out / "new.json")'
    done, receipt = observed_route.run('''(out / "new.json").write_text("new")
(out / "new.json").unlink()
''' + move + '\n(out / "new.json").read_text()')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


def test_directory_move_revokes_descendant_admission(observed_route):
    old = observed_route.out / 'old_dir'
    old.mkdir()
    (old / 'file.json').write_text('old')
    done, receipt = observed_route.run('''(out / "new_dir").mkdir()
(out / "new_dir/file.json").write_text("new")
(out / "new_dir").rename(out / "moved_dir")
(out / "old_dir").rename(out / "new_dir")
(out / "new_dir/file.json").read_text()''')
    assert done.returncode != 0
    assert 'undeclared' in str(receipt['violations'])


def test_delete_then_genuinely_create_new_output_is_admitted(observed_route):
    done, receipt = observed_route.run('''(out / "new.json").write_text("first")
(out / "new.json").unlink()
(out / "new.json").write_text("second")
assert (out / "new.json").read_text() == "second"''')
    assert done.returncode == 0, done.stderr


def test_sqlite_existing_store_refused_by_integration(observed_route):
    import sqlite3
    old = observed_route.out / 'old.db'
    with sqlite3.connect(old) as db:
        db.execute('CREATE TABLE old_data (value TEXT)')
        db.execute("INSERT INTO old_data VALUES ('old contents')")
    observed_route.write('import sqlite3\nwith sqlite3.connect(out / "old.db") as db:\n    db.execute("SELECT * FROM old_data").fetchall()')
    with pytest.raises(integrate.SeamBlocker) as caught:
        integrate.execute_baseline(observed_route.request, dict(os.environ))
    assert caught.value.condition == 'read-coverage-refused'
    receipt = json.loads((observed_route.out / 'read_coverage.json').read_text())
    assert 'SQLite store must be new' in str(receipt['violations'])


def test_new_sqlite_store_can_reconnect(observed_route):
    done, receipt = observed_route.run('''import sqlite3
with sqlite3.connect(out / "new.db") as db:
    db.execute("CREATE TABLE new_data (value TEXT)")
with sqlite3.connect(out / "new.db") as db:
    db.execute("SELECT * FROM new_data").fetchall()''')
    assert done.returncode == 0, done.stderr
    assert receipt['admitted_new_sqlite_stores'] == [str(observed_route.out / 'new.db')]


def test_sqlite_replacement_revokes_native_store_admission(observed_route):
    import sqlite3
    with sqlite3.connect(observed_route.out / 'old.db') as db:
        db.execute('CREATE TABLE old_data (value TEXT)')
    done, receipt = observed_route.run('''import sqlite3
db = sqlite3.connect(out / "new.db")
db.close()
(out / "old.db").replace(out / "new.db")
with sqlite3.connect(out / "new.db") as db:
    db.execute("SELECT * FROM old_data").fetchall()''')
    assert done.returncode != 0
    assert 'SQLite store must be new' in str(receipt['violations'])


@pytest.mark.parametrize('suffix', ['-wal', '-shm', '-journal'])
def test_sqlite_preexisting_sidecar_refused(observed_route, suffix):
    (observed_route.out / ('new.db' + suffix)).write_bytes(b'old sidecar')
    done, receipt = observed_route.run('import sqlite3\nsqlite3.connect(out / "new.db")')
    assert done.returncode != 0
    assert 'SQLite store must be new' in str(receipt['violations'])
