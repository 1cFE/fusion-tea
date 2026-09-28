"""Resolve the final record's identities and per-file digests after review; no study execution."""
import hashlib
import importlib
import inspect
import json
from pathlib import Path
import shutil
import subprocess

from study_tools import HERE, ROOT, PACKAGE, P, EXE, SEMANTIC, dump


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    from scripts.study import common
    from simkit.study.config import load_study_config, build_definition
    from simkit.study.cli import _prepared_evaluator
    from scripts.study.manifest import _canonical_digest
    for name in ('cli','config','policy','query','store','strategy','definition','runner','model_contract'):
        module=importlib.import_module('simkit.study.'+name)
        path=Path(inspect.getfile(module))
        target=HERE/'context/teax'/path.name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    indicators=json.loads((HERE/'indicators.json').read_text())
    preflight=json.loads((HERE/'results/preflight.json').read_text())
    verification=json.loads((HERE/'results/verification_summary.json').read_text())
    manifest=json.loads((HERE/'context/manifest.json').read_text())
    cfg=load_study_config(HERE/'study-config.json')
    ev=_prepared_evaluator(cfg,HERE/'results/grid/store.sqlite')
    definition=build_definition(cfg,ev)
    assert ev.fingerprint==EXE
    common.assert_tree_clean(PACKAGE)
    oracle_files=('exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/oracle_finance.py','exploration/stellarator_e2e/studies/oracle_entry.py')
    oracle_digest=common.tool_source_digest(oracle_files)
    tools=[indicators['tool'],preflight['tool'],verification['tool']]
    for tool in tools:
        for entry in tool['source_digest']['files']:
            source=ROOT/entry['path']
            target=HERE/'context/tools'/entry['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
            assert digest(target)==entry['sha256']
    local_files=[str((HERE/name).relative_to(ROOT)) for name in ('study_tools.py','analyze_results.py','freeze_snapshot.py')]
    tools.append(dict(path=str((HERE/'analyze_results.py').relative_to(ROOT)),source_digest=common.tool_source_digest(tuple(local_files))))
    teax_files=[(str(p.relative_to(HERE)),digest(p)) for p in sorted((HERE/'context/teax').glob('*.py'))]
    tools.append(dict(path='context/teax/cli.py',source_digest=dict(recipe='tool-source-digest/v1',
        digest=_canonical_digest('tool-source-digest/v1',teax_files),files=[dict(path=p,sha256=d) for p,d in teax_files])))
    artifacts=[]
    for path in sorted((HERE/'results').rglob('*')):
        if path.is_file() and not path.is_symlink() and '_pkg_link' not in path.parts and path.suffix not in ('.pyc',) and not path.name.endswith(('-wal','-shm')):
            artifacts.append(dict(path=str(path.relative_to(HERE)),sha256=digest(path)))
    context=[dict(path=str(p.relative_to(HERE)),sha256=digest(p)) for p in sorted((HERE/'context').rglob('*')) if p.is_file()]
    dump('context-digests.json',context)
    compatibility=json.loads((HERE/'results/store-compatibility.json').read_text())
    baseline_compatibility=json.loads((HERE/'results/baseline-compatibility.json').read_text())
    manifest_content={k:manifest[k] for k in ('ties','objective_catalog','baseline','oracle')}
    manifest_content['oracle']['source_digest']=oracle_digest
    fingerprint_names=['indicator_inputs','recorded_provenance.executable_fingerprint','recorded_provenance.semantic_fingerprint']
    manifest_content['fingerprint_names']=fingerprint_names
    snapshot=dict(snapshot_schema_version='1',study_id=HERE.name,
        package=dict(path=manifest['package']['path'],package_name='stellarator_tea',repo_commit='266110f9',git_clean=True),
        fingerprints={'indicator_inputs':indicators['package']['indicator_input_fingerprint'],
                      'recorded_provenance.executable_fingerprint':EXE,'recorded_provenance.semantic_fingerprint':SEMANTIC},
        manifest=dict(path='context/manifest.json',schema_version=manifest['schema_version'],digest=digest(HERE/'context/manifest.json'),content_used=manifest_content),
        stores=[dict(store_id='grid',path='results/grid/store.sqlite',compatibility_tuple=compatibility)],
        preflight_baseline_store=dict(path='results/baseline/store.sqlite',compatibility_tuple=baseline_compatibility,
            note='Separate one-point preflight execution, not a study arm or cross-fingerprint comparison.'),
        arms=[dict(arm_id='arm-transfer',store_id='grid',effective_executable_fingerprint=dict(value=EXE,inputs=None,no_adapter=True,note='No adapter exists; the sealed fingerprint is the identity.'),
            entry_models={key:value.__name__ for key,value in definition.entry_models.items()},
            strategy=dict(kind='GridStrategy',ordered_grid=json.loads((HERE/'study-config.json').read_text())['grid'],definition_fingerprint=cfg.semantic_fingerprint()),
            window=dict(bounds=json.loads((HERE/'results/window-decision.json').read_text())['bounds'],provenance='engineered'),
            verification=dict(command=verification['command'],tool_revision=verification['tool']['source_digest'],
                sampling_scheme='exhaustive 108 grid cases; generic predicate verification plus all-161-output comparison to the pre-run oracle scan',
                tolerance=dict(oracle_relative=1e-9,identity_relative=1e-9,identity_absolute=1e-9,predicates='authored exact operators'),summary_sha256=digest(HERE/'results/verification_summary.json')),
            glue_ledger=[],glue_ledger_none=True,artifacts=artifacts)],tools=tools,
        teax=dict(revision=subprocess.check_output(['git','-C',str(Path(inspect.getfile(importlib.import_module('simkit.study.cli'))).parents[4]),'rev-parse','HEAD'],text=True).strip(),era_pin=None),
        indicators=dict(path='indicators.json',sha256=digest(HERE/'indicators.json'),output_schema_version=indicators['schema_version'],
            axis_declaration=dict(path='axes.json',schema_version='study-axis-declaration/v1',digest=digest(HERE/'axes.json'),groups_declared=['R','a','I_coil','B_max'],subset=False)),
        context_digest_index=dict(path='context-digests.json',sha256=digest(HERE/'context-digests.json')))
    assert set(fingerprint_names)==set(snapshot['fingerprints'])
    assert snapshot['teax']['revision']=='8d877460ac4f6f264561d916e40c1708adb13397'
    dump('snapshot.json',snapshot)
    print('snapshot sha256',digest(HERE/'snapshot.json'))


if __name__=='__main__':
    main()
