"""Build/verify a deterministic draft archive from an explicit reviewed file list."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile


def sha(data): return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path=PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or str(path)!=name:
        raise ValueError('unsafe member: '+name)
    if any(part in ('.git','.venv','.codex-test','__pycache__','pkg_link','candidate-archives','independent-review') for part in path.parts):
        raise ValueError('excluded member: '+name)
    if path.name=='.env' or path.name.endswith(('-wal','-shm','.pyc')):
        raise ValueError('credential/cache/transient member: '+name)
    if name.startswith('knowledge/holdout/') and name!='knowledge/holdout/aries-cs/PROTOCOL.md':
        raise ValueError('sealed material is forbidden')
    if name=='.project/concepts/stellarator-mbse-demo.md':
        raise ValueError('excluded concept is forbidden')
    barred_prefixes = (
        'exploration/concept_analysis/analyses/09-qi-stellarator-hts/',
        'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-compact-stellarator-study',
        'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-systems-optimization',
        'knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison',
        'knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/',
        'knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion',
        'knowledge/sources/aries_cost_account_documentation/',
        'knowledge/sources/tea_dt_mfe_cost_analysis/',
        'knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md',
    )
    if name.startswith(barred_prefixes) or ('WI-009_mfe-cost-structure-library' in path.parts and path.name=='design.md'):
        raise ValueError('protocol-barred member: '+name)
    return path


def read_members(root, member_file):
    names=json.loads(Path(member_file).read_text())
    if not isinstance(names,list) or not all(isinstance(n,str) for n in names) or len(names)!=len(set(names)):
        raise ValueError('member list must contain unique relative filenames')
    root=Path(root).resolve();files={}
    for name in sorted(names):
        parts=safe_name(name).parts
        path=root
        for part in parts:
            path=path/part
            if path.is_symlink(): raise ValueError('symlink member: '+name)
        if not path.resolve().is_relative_to(root) or not path.is_file(): raise ValueError('missing/nonlocal member: '+name)
        if path.suffix in ('.db','.sqlite','.sqlite3') and any(Path(str(path)+suffix).exists() for suffix in ('-wal','-shm')):
            raise ValueError('database is not quiescent: '+name)
        files[name]=path.read_bytes()
    if 'COMPARISON-SHA256SUMS' in files: raise ValueError('reserved index member')
    return files


def build(root, here, out):
    root=Path(root).resolve();here=Path(here);out=Path(out)
    identity=json.loads((here/'candidate-identity.json').read_text())
    if identity['status']!='draft_candidate': raise ValueError('only draft candidate publication is authorized')
    files=read_members(root,here/'archive-members.json')
    index=''.join(f'{sha(data)}  {name}\n' for name,data in files.items()).encode()
    out.mkdir(parents=True,exist_ok=False)
    archive=out/'comparison-freeze.tar.gz'
    with archive.open('xb') as stream:
        with gzip.GzipFile(filename='',fileobj=stream,mode='wb',mtime=0) as zipped:
            with tarfile.open(fileobj=zipped,mode='w',format=tarfile.PAX_FORMAT) as tar:
                for name,data in [*files.items(),('COMPARISON-SHA256SUMS',index)]:
                    info=tarfile.TarInfo(name)
                    info.size=len(data);info.mtime=0;info.mode=0o644;info.uid=info.gid=0
                    info.uname=info.gname=''
                    tar.addfile(info,io.BytesIO(data))
    record={'status':'draft_candidate','base_revision':identity['base_revision'],
            'archive':archive.name,'archive_sha256':sha(archive.read_bytes()),'index_sha256':sha(index),
            'file_count':len(files),'archive_bytes':archive.stat().st_size,
            'predecessor_r2_sha256':'fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21',
            'candidate_identity':identity,'member_list_sha256':sha((here/'archive-members.json').read_bytes())}
    (out/'SHA256SUMS').write_bytes(index)
    (out/'freeze-record.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    verify(archive)
    return record


def verify(archive):
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers();names=[m.name for m in members]
        if len(names)!=len(set(names)): raise ValueError('duplicate archive members')
        for member in members:
            safe_name(member.name)
            if not member.isfile(): raise ValueError('non-regular archive member')
        raw=tar.extractfile('COMPARISON-SHA256SUMS').read()
        expected={}
        for line in raw.decode().splitlines():
            digest,name=line.split('  ',1)
            if name in expected or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
                raise ValueError('malformed/duplicate checksum record')
            expected[name]=digest
        if set(names)!=set(expected)|{'COMPARISON-SHA256SUMS'}: raise ValueError('archive/index membership differs')
        for name,digest in expected.items():
            if sha(tar.extractfile(name).read())!=digest: raise ValueError('content mismatch: '+name)
    return {'status':'pass','archive_sha256':sha(Path(archive).read_bytes()),'files':len(expected)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--out-dir',type=Path)
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    if bool(args.verify)==bool(args.out_dir): parser.error('choose exactly one of --verify or --out-dir')
    print(json.dumps(verify(args.verify) if args.verify else build(args.root,Path(__file__).parent,args.out_dir),indent=2))
