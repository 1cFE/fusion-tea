"""Record-local preparation, oracle scan and read-only study export; never executes a native sweep."""
import argparse
import dataclasses
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKAGE = ROOT / 'exploration/stellarator_e2e/generated'
STUDIES = HERE.parent
P = 'stellarator_09__stellaris__'
EXE = '8ff5bb7c3d71f235be697e254766d3e0f552f3b94b46831da62a08a9755122a5'
SEMANTIC = '2c2788662c148ccae3f61d1f58e510cedcfcddb6b0b489878ec8d7ebd6f1c08e'
GRID = [(P+'plasma__R', [11.43,12.7,13.97]), (P+'plasma__a',[1.17,1.3,1.43]),
        (P+'magnet__coil__I_coil',[14e6,15.4e6,17e6]),
        (P+'magnet__winding_pack__B_max',[20.,24.9,27.5,30.])]
sys.path[:0] = [str(ROOT), str(STUDIES)]


def dump(path, value):
    path = HERE / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def defaults():
    values = {}
    for path in (PACKAGE/'inputs').glob('*.json'):
        values.update(json.loads(path.read_text()))
    assert len(values) == 265
    return values


def catalog():
    from simkit.study.model_contract import load_model_contract
    result = load_model_contract(PACKAGE)
    assert result.semantic_fingerprint == SEMANTIC
    assert len(result.concrete_entries) == 18
    return result.concrete_entries


def prepare():
    import oracle_entry
    source_paths = {
        'ANNEX.md': STUDIES/'ANNEX.md', 'manifest.json': STUDIES/'manifest.json',
        'WI038-design.md': ROOT/'work/active/WI-038_conductor-grade-lever/design.md',
        'WI038-basis.md': ROOT/'work/active/WI-038_conductor-grade-lever/basis.md',
        'WI038-audit.md': ROOT/'work/active/WI-038_conductor-grade-lever/audit.md',
        'WI040-design.md': ROOT/'work/active/WI-040_winding-pack-mass-cost/design.md',
        'WI040-material-research.md': ROOT/'work/active/WI-040_winding-pack-mass-cost/evidence/material-research.md',
        'WI040-accounting-research.md': ROOT/'work/active/WI-040_winding-pack-mass-cost/evidence/accounting-research.md',
        'transfer-evidence-assessment.md': ROOT/'work/orchestration/goals/magnet-design-transfer/evidence/transfer-evidence-assessment.md',
        'STUDY_POLICY.md': ROOT/'modeling_project/STUDY_POLICY.md',
        'integration_return.json': ROOT/'work/orchestration/goals/magnet-design-transfer/evidence/T005-integration/integration_return.json',
        'model_contract.json': PACKAGE/'contracts/model_contract.json',
        'package_contract.json': PACKAGE/'contracts/package_contract.json',
        'pipeline.yaml': PACKAGE/'pipelines/pipeline.yaml',
        'oracle/verify_stellaris.py': STUDIES.parent/'verify_stellaris.py',
        'oracle/oracle_finance.py': STUDIES.parent/'oracle_finance.py',
        'oracle/oracle_entry.py': STUDIES/'oracle_entry.py',
    }
    for name, path in source_paths.items():
        dest = HERE/'context'/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
    for path in (PACKAGE/'inputs').glob('*.json'):
        target = HERE/'context/inputs'/path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path,target)
    inputs = defaults()
    dump('context/constraint_catalog.json', catalog())
    dump('context/oracle_operand_bindings.json', oracle_entry.operand_bindings())
    dump('context/oracle_output_mapping.json', oracle_entry.ORACLE_OUTPUT_TO_CHANNEL)
    dump('context/oracle_input_mapping.json', oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT)
    fixed = {key:inputs[key] for key in oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT
             if key.startswith(P+'magnet__') or key == P+'cryoplant__T_cold_cryo'}
    for key, _ in GRID:
        fixed.pop(key,None)
    assert fixed[P+'magnet__winding_pack__j_wp'] == 118.8271604938272
    assert fixed[P+'magnet__winding_pack__B_grade_ref'] == 24.9
    assert fixed[P+'cryoplant__T_cold_cryo'] == 20.
    common = dict(package=dict(dir=str(PACKAGE),name='stellarator_tea',spec='pipelines/pipeline.yaml'),
                  policy=dict(name='objective/v1',objectives=[dict(output=P+'lcoe_calc__lcoe',role='minimize')],
                              response_roles={},partial_coverage='keep-for-boundary'),retention='keep')
    manifest = json.loads((STUDIES/'manifest.json').read_text())
    dump('baseline-config.json', dict(common,study_id='20260913-magnet-design-transfer-baseline',grid=[],fixed=manifest['baseline']['point']))
    dump('candidate-config.json', dict(common,study_id='20260913-magnet-design-transfer',grid=GRID,fixed=fixed))
    from simkit.study.config import load_study_config
    for name in ('baseline','candidate'):
        cfg = load_study_config(HERE/(name+'-config.json'))
        assert cfg.policy.name == 'objective/v1'
    dump('context/source-copy-index.json', {name:dict(original=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for name,path in source_paths.items()})


def cases(store):
    from simkit.study.store import StudyStore
    from simkit.study.query import StudyQuery
    db = StudyStore(HERE/store)
    try:
        rows = [dataclasses.asdict(row) for row in StudyQuery(db,PACKAGE).cases()]
        db.conn.row_factory = __import__('sqlite3').Row
        compatibility = dict(db.conn.execute('SELECT * FROM compatibility').fetchone())
    finally:
        db.close()
    return rows,compatibility


def baseline():
    from scripts.study import identity
    rows,compatibility = cases('results/baseline/store.sqlite')
    assert len(rows) == 1 and rows[0]['state'] == 'completed'
    row = rows[0]
    assert row['executable_fingerprint'] == EXE
    assert len(row['outputs']) == 177 and len(row['verdicts']) == 18
    identity_doc = identity.build_sealed(package_name='stellarator_tea',package_root=PACKAGE)
    dump('results/package_identity.json',identity_doc)
    cats = catalog()
    dump('results/baseline_result.json',dict(schema_version='study-baseline-result/v1',
        executed_under=dict(identity_digest=EXE,store_id=str((HERE/'results/baseline/store.sqlite').relative_to(ROOT)),case_id=row['candidate_id']),
        point=row['inputs'],channels=row['outputs'],verdicts=[dict(constraint_id=k,
        definition_qualified_name=cats[k]['definition_qualified_name'],source_local_identity=cats[k]['source_local_identity'],status=v) for k,v in sorted(row['verdicts'].items())]))
    dump('results/baseline-query.json',rows)
    dump('results/baseline-compatibility.json',compatibility)


def scan():
    import oracle_entry
    from scripts.study.verify import derive_verdict
    cfg = json.loads((HERE/'candidate-config.json').read_text())
    held = cfg['fixed']
    rows=[]
    for values in itertools.product(*(values for _,values in cfg['grid'])):
        point = held | dict(zip((key for key,_ in cfg['grid']),values))
        out = oracle_entry.evaluate(point)
        assert len(out)==161 and all(math.isfinite(x) for x in out.values())
        verdicts={}
        for cid,entry in catalog().items():
            satisfied, count = derive_verdict(cid,entry,oracle_entry.operand_bindings(),point,defaults(),out)
            verdicts[cid] = dict(status='satisfied' if satisfied else 'violated',operands_resolved=count)
        rows.append(dict(point=point,outputs=out,verdicts=verdicts))
    dump('results/oracle-scan.json',rows)
    # The completed no-refusal scan fixes precisely the candidate grid, with no mask.
    assert len(rows)==108
    shutil.copyfile(HERE/'candidate-config.json',HERE/'study-config.json')
    dump('results/window-decision.json',dict(provenance='engineered',scanned=108,refusals=0,
        bounds={key:values for key,values in cfg['grid']},validity_mask='none: all R > a + 2.25 m',
        rationale='Retain the complete proposed sensitivity grid; all oracle evaluations are finite. This does not establish continuous feasibility or a qualified engineering boundary.'))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=('prepare','baseline','scan'))
    globals()[parser.parse_args().stage]()
