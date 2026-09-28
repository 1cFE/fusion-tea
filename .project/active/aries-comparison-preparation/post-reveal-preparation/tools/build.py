"""Build a self-contained source snapshot; Python environment/license stay external."""
import gzip
import io
import json
import os
from pathlib import Path
import shutil
import tarfile
import adapter as a


def build():
    package = a.HERE.parent / 'package'
    runtime = package / 'runtime'
    if (package / 'post-reveal-v1.tar.gz').exists():
        raise FileExistsError('version already frozen')
    source = Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'
    target = runtime / 'teax/packages/teax-simkit'
    shutil.copytree(source / 'simkit', target / 'simkit', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', 'tests', '*.pyc'))
    shutil.copy2(source / 'pyproject.toml', target / 'pyproject.toml')
    wheels = {}
    for key in ('AGENTIC','CODEGEN','COSTINGFE'):
        original=Path(os.environ['STOP_PARSER_'+key+'_WHEEL'])
        dest=runtime / 'wheels' / original.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(original,dest)
        wheels[key]={'path':str(dest.relative_to(a.ROOT)), 'sha256':a.sha(dest)}
    files=set()
    for directory in (a.PACKAGE,a.ROOT/'models',a.ROOT/'scripts/study',runtime,a.HERE,a.HERE.parent/'mapping'):
        files.update(p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='identity.json')
    files.add(a.ROOT/'scripts/compare_fixed_point.py')
    files.add(a.ROOT/'exploration/stellarator_e2e/studies/study_route.py')
    for rel in ('scripts/__init__.py','scripts/study/__init__.py'):
        if (a.ROOT/rel).exists(): files.add(a.ROOT/rel)
    contract=a.strict((a.PACKAGE/'contracts/package_contract.json').read_bytes())
    identity={'schema_version':'post-reveal-package/v1','executable_fingerprint':contract['executable_fingerprint'],
              'files':{str(p.relative_to(a.ROOT)):a.sha(p) for p in sorted(files)},
              'runtime':'Python 3.12 sealed environment; licensed SysIDE 0.8.4; dependencies external, bundled teax source and sealed wheels', 'wheels':wheels}
    a.document(a.HERE/'identity.json',identity)
    files.add(a.HERE/'identity.json')
    archive=package/'post-reveal-v1.tar.gz'
    with archive.open('xb') as stream, gzip.GzipFile(fileobj=stream,mode='wb',mtime=0,filename='') as zipped, tarfile.open(fileobj=zipped,mode='w') as tar:
        for p in sorted(files):
            data=p.read_bytes();info=tarfile.TarInfo(str(p.relative_to(a.ROOT)))
            info.size=len(data);info.mode=0o644
            tar.addfile(info,io.BytesIO(data))
    a.document(package/'freeze-record.json',{'schema_version':'post-reveal-freeze/v1','archive':archive.name,
               'sha256':a.sha(archive),'files':len(files),'identity_sha256':a.sha(a.HERE/'identity.json'),
               'executable_fingerprint':contract['executable_fingerprint'],'reference_executed':False})
    print(json.dumps(a.strict((package/'freeze-record.json').read_bytes()),indent=2))

if __name__=='__main__': build()
