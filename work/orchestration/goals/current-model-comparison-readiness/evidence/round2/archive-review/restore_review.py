"""Independent actual-byte archive reviewer. Launch through .codex-test/run.

Stages are explicit so a failed attempt is retained, never overwritten or silently
repaired from the source checkout. No stage executes until an archive is supplied.
"""
import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import quote

CANDIDATE = Path('.project/active/aries-comparison-preparation/current-readiness/candidate')
TESTS = ['tests/test_compare_fixed_point.py', 'tests/test_current_comparison_candidate.py',
         'tests/test_candidate_report_custody.py', 'tests/test_dependency_provenance.py',
         'tests/study/test_read_set_coverage.py']
BARRED = ('knowledge/holdout/', 'exploration/concept_analysis/analyses/09-qi-stellarator-hts/',
          'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-compact-stellarator-study',
          'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-systems-optimization',
          'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison',
          'knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/',
          'knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion',
          'knowledge/sources/aries_cost_account_documentation/', 'knowledge/sources/tea_dt_mfe_cost_analysis/',
          'knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def safe(name):
    p = PurePosixPath(name)
    assert name and not p.is_absolute() and '..' not in p.parts and str(p) == name, name
    assert not set(p.parts) & {'.git', '.venv', '.codex-test', '__pycache__', 'pkg_link', 'candidate-archives'}, name
    assert p.name != '.env' and not p.name.endswith(('-wal', '-shm', '.pyc')), name
    assert name != '.project/concepts/stellarator-mbse-demo.md', name
    assert not ('WI-009_mfe-cost-structure-library' in p.parts and p.name == 'design.md'), name
    assert name == 'knowledge/holdout/aries-cs/PROTOCOL.md' or not name.startswith(BARRED), name
    return p


def inspect(archive, expected):
    assert sha(archive.read_bytes()) == expected, 'external archive hash differs'
    with tarfile.open(archive, 'r:gz') as tar:
        members = tar.getmembers()
        names = [m.name for m in members]
        assert len(names) == len(set(names)), 'duplicate member'
        for member in members:
            safe(member.name)
            assert member.isfile(), member.name
        files = {m.name: tar.extractfile(m).read() for m in members}
    records = {}
    for line in files.pop('COMPARISON-SHA256SUMS').decode().splitlines():
        digest, name = line.split('  ', 1)
        safe(name)
        assert len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), name
        assert name not in records, name
        records[name] = digest
    assert set(files) == set(records)
    assert all(sha(data) == records[name] for name, data in files.items())
    return files, records


def environment(root):
    env = os.environ.copy()
    teax = Path(env['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'
    env['PYTHONPATH'] = os.pathsep.join(map(str, (root, root/'scripts', teax)))
    env['STUDY_REQUIRE_TEAX'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def command(state, label, args, expected=0):
    review = Path(state['review']); root = Path(state['root'])
    log = review/(label+'.log')
    with log.open('xb') as stream:
        result = subprocess.run([sys.executable, *map(str, args)], cwd=root,
                                env=environment(root), stdout=stream, stderr=subprocess.STDOUT)
    write(review/(label+'.command.json'), {'argv': [sys.executable, *map(str, args)],
          'cwd': str(root), 'exit_code': result.returncode, 'expected_exit': expected,
          'log_sha256': sha(log.read_bytes())})
    print(label, result.returncode, flush=True)
    assert result.returncode == expected, f'{label}: see {log}'


def prepare(args):
    source = Path.cwd(); archive = args.archive.resolve()
    files, records = inspect(archive, args.sha256)
    base = json.loads(files[str(CANDIDATE/'candidate-identity.json')])['base_revision']
    subprocess.run(['git', 'cat-file', '-e', base+'^{commit}'], cwd=source, check=True)
    members = json.loads(files[str(CANDIDATE/'archive-members.json')])
    assert members == sorted(records) and len(members) == len(set(members))
    base_files = json.loads(files[str(CANDIDATE/'base-required-files.json')])
    assert isinstance(base_files, dict)
    review = args.review.resolve(); review.mkdir(parents=True, exist_ok=False)
    root = Path(tempfile.mkdtemp(prefix='wi073-actual-archive-'))
    for name, digest in base_files.items():
        safe(name)
        assert name not in records, 'base-only file also in overlay'
        data = subprocess.check_output(['git', 'show', f'{base}:{name}'], cwd=source)
        assert sha(data) == digest
        p = root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    for name, data in files.items():
        p = root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    pkg = root/'exploration/stellarator_e2e/pkg'; pkg.mkdir(exist_ok=True)
    (pkg/'stellarator_tea').symlink_to('../generated')
    assert (pkg/'stellarator_tea').resolve() == root/'exploration/stellarator_e2e/generated'
    state = {'archive': str(archive), 'archive_sha256': args.sha256, 'root': str(root),
             'review': str(review), 'base_revision': base, 'base_files': base_files,
             'member_hashes': records, 'helper_sha256': sha(Path(__file__).read_bytes())}
    write(review/'state.json', state)
    print(str(review/'state.json'), flush=True)


def audit_members(state):
    root = Path(state['root'])
    assert all(sha((root/name).read_bytes()) == value for name,value in state['member_hashes'].items())
    assert all(sha((root/name).read_bytes()) == value for name,value in state['base_files'].items())
    assert sha(Path(state['archive']).read_bytes()) == state['archive_sha256']
    assert not (root/CANDIDATE.parent/'revealed-results').exists()


def run_stage(state, stage):
    root=Path(state['root']);review=Path(state['review']);c=root/CANDIDATE
    audit_members(state)
    if stage == 'lineage':
        command(state,'archive-builder-verify',[c/'build_freeze.py','--verify',state['archive']])
        command(state,'lineage',[c/'check_lineage.py','--root',root,'--out',review/'lineage.json'])
        probe = """import sys,json,hashlib,pathlib,importlib
r=pathlib.Path.cwd();sys.path.insert(0,str(r/'exploration/stellarator_e2e/studies'))
names=['study_route','oracle_entry','exploration.stellarator_e2e.oracle_matched_cycle','scripts.study.verify']
o={}
for n in names:
 p=pathlib.Path(importlib.import_module(n).__file__).resolve();assert p.is_relative_to(r),(n,p);o[n]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for n in ['models/library/data/matched_steam_properties.json','exploration/stellarator_e2e/models/data/matched_steam_properties.json','exploration/stellarator_e2e/oracle_matched_cycle_properties.json']:
 p=r/n;o[n]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
print(json.dumps(o,indent=2))"""
        command(state,'restored-imports',['-c',probe])
    elif stage == 'tests':
        command(state,'five-file-pytest',['-m','pytest',*TESTS,'-q','-p','no:cacheprovider',
                 '--basetemp',review/'pytest-temp','--junitxml',review/'five-file.xml'])
    elif stage in ('selected-forward','table5-conditioned'):
        attempt=review/stage
        command(state,stage+'-execute',[c/'execute_frozen.py','--root',root,'--rules',c/'input-rules.json',
                '--request',c/'requests'/f'{stage}.json','--out-dir',attempt])
        result=attempt/'native-result.json'
        for script,label in [('check_selected_mode.py','independent'),('check_accounting.py','accounts')]:
            command(state,stage+'-'+label,[c/script,'--root',root,'--native-result',result,'--out',review/f'{stage}-{label}.json'])
        command(state,stage+'-export',[c/'export_model_values.py','--root',root,'--manifest',c/'manifest.json',
                '--native-result',result,'--out',review/f'{stage}-export.json'])
        checked=json.loads((review/f'{stage}-independent.json').read_text())
        assert checked['numeric_channels']==1050 and len(checked['predicate_checks'])==28
        assert checked['status']=='pass' and all(x['passed'] for x in checked['predicate_checks'])
    elif stage == 'stores':
        stores=[]
        for name in sorted(state['member_hashes']):
            if not name.endswith(('.db','.sqlite','.sqlite3')):continue
            p=root/name;before=sha(p.read_bytes())
            conn=sqlite3.connect('file:'+quote(str(p),safe='/')+'?mode=ro&immutable=1',uri=True)
            assert conn.execute('pragma integrity_check').fetchall()==[('ok',)]
            tables=[row[0] for row in conn.execute("select name from sqlite_master where type='table' order by name")]
            counts={t:conn.execute('select count(*) from "'+t.replace('"','""')+'"').fetchone()[0] for t in tables}
            schema={t:[row[1] for row in conn.execute('pragma table_info("'+t.replace('"','""')+'")')] for t in tables}
            conn.close();assert before==sha(p.read_bytes())
            stores.append({'path':name,'sha256':before,'rows':counts,'columns':schema})
        assert len(stores)>=4, 'four retained case stores required'
        write(review/'immutable-stores.json',stores)
    elif stage == 'rebuild':
        for n in (1,2):
            out=review/f'rebuild-{n}'
            command(state,f'rebuild-{n}',[c/'build_freeze.py','--root',root,'--out-dir',out])
            assert (out/'comparison-freeze.tar.gz').read_bytes()==Path(state['archive']).read_bytes()
        files,_=inspect(Path(state['archive']),state['archive_sha256'])
        target=str(CANDIDATE/'scientific-summary.md');assert target in files
        tamper=review/'tampered.tar.gz'
        with tarfile.open(state['archive'],'r:gz') as source,tarfile.open(tamper,'w:gz') as output:
            for m in source.getmembers():
                data=source.extractfile(m).read()
                if m.name==target:data+=b'\nSynthetic tamper for reviewer refusal test.\n'
                m.size=len(data);output.addfile(m,io.BytesIO(data))
        command(state,'tamper-rejection',[c/'build_freeze.py','--verify',tamper],expected=1)
    else:
        raise ValueError(stage)
    audit_members(state)
    write(review/(stage+'.pass.json'),{'status':'pass','archive_sha256':state['archive_sha256'],'stage':stage})


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','lineage','tests','selected-forward','table5-conditioned','stores','rebuild'])
    p.add_argument('--archive',type=Path);p.add_argument('--sha256');p.add_argument('--review',type=Path);p.add_argument('--state',type=Path)
    args=p.parse_args()
    if args.stage=='prepare':
        assert args.archive and args.sha256 and args.review
        prepare(args)
    else:
        assert args.state
        run_stage(json.loads(args.state.read_text()),args.stage)


if __name__=='__main__':main()
