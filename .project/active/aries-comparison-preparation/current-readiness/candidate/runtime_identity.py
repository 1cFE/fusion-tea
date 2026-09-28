"""Record external licensed runtime identities without capturing credentials."""
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(expected, actual=None):
    """Check runtime content while allowing a restored checkout to relocate."""
    actual=capture() if actual is None else actual
    mismatches=[]
    if actual['python'] != expected['python']: mismatches.append('Python build')
    for section, fields in [('modules',('module_file_sha256','version')),
                            ('sealed_wheels',('filename','sha256'))]:
        if set(actual[section]) != set(expected[section]):
            mismatches.append(section+' inventory')
        for name, required in expected[section].items():
            observed=actual[section].get(name,{})
            for field in fields:
                if observed.get(field) != required[field]:
                    mismatches.append(section+'.'+name+'.'+field)
    for field in ('commit','runtime_python_files'):
        if actual['teax'][field] != expected['teax'][field]:
            mismatches.append('teax.'+field)
    if actual['teax']['runtime_dirty_status'] or expected['teax']['runtime_dirty_status']:
        mismatches.append('teax runtime is dirty')
    if mismatches:
        raise ValueError('runtime identity mismatch: '+', '.join(mismatches))
    return {'status':'pass','python':actual['python'],'teax_commit':actual['teax']['commit'],
            'runtime_python_file_count':len(actual['teax']['runtime_python_files']),
            'module_count':len(actual['modules']),'sealed_wheel_count':len(actual['sealed_wheels']),
            'relocation':'Filesystem locations are recorded but are not content identities.'}


def capture():
    modules={}
    for name in ('agentic_mbse','sysml_codegen','costingfe','syside'):
        module=importlib.import_module(name)
        path=Path(module.__file__).resolve()
        modules[name]={'import_path':str(path),'module_file_sha256':sha(path),'version':getattr(module,'__version__',None)}
    wheels={}
    for name in ('AGENTIC','CODEGEN','COSTINGFE'):
        path=Path(os.environ['STOP_PARSER_'+name+'_WHEEL']).resolve()
        wheels[name.lower()]={'filename':path.name,'external_path':str(path),'sha256':sha(path)}
    teax=Path(os.environ['STOP_PARSER_TEAX_ROOT']).resolve()
    def git(*args): return subprocess.check_output(['git',*args],cwd=teax,text=True).strip()
    source=teax/'packages/teax-simkit'
    tree={path.relative_to(source).as_posix():sha(path) for path in sorted(source.rglob('*.py'))
          if not path.is_symlink() and '__pycache__' not in path.parts and '.venv' not in path.parts}
    return {'python':sys.version,'interpreter':str(Path(sys.executable).resolve()),
            'modules':modules,'sealed_wheels':wheels,
            'teax':{'root':str(teax),'commit':git('rev-parse','HEAD'),
                    'dirty_status':git('status','--porcelain'),
                    'runtime_dirty_status':git('status','--porcelain','--','packages/teax-simkit'),
                    'runtime_python_files':tree},
            'environment_names':['STOP_PARSER_TEAX_ROOT','STOP_PARSER_WHEEL_TARGET','STOP_PARSER_AGENTIC_WHEEL',
                                 'STOP_PARSER_CODEGEN_WHEEL','STOP_PARSER_COSTINGFE_WHEEL','STUDY_REQUIRE_TEAX'],
            'prerequisites':'Licensed SysIDE and the recorded sealed wheels/teax checkout are external. Obtain license via the documented launcher; credentials are never archived.'}


if __name__=='__main__':
    from candidate_common import exclusive_document
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();_,ok=exclusive_document(args.out,capture)
    raise SystemExit(0 if ok else 1)
