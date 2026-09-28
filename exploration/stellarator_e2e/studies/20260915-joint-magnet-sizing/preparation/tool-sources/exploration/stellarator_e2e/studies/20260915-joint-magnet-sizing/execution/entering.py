"""Evaluate every selected point with captured entering oracle; never execute old native code."""
import importlib.util
import json
import sys
from pathlib import Path

H = Path(__file__).resolve().parents[1]
R = H / 'results'
P = 'stellarator_09__stellaris__'
NEW = {P + 'magnet__winding_pack__' + k for k in ('sizing_mode', 'inventory_multiplier')}


def read(path):
    return json.loads(path.read_text())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    assert Path(module.__file__).resolve() == path.resolve()
    return module


def main():
    from scripts.study.verify import derive_verdict
    frozen = H / 'preparation/entering'
    # Explicitly install both dependencies before loading the frozen entry module.
    # This standalone process never imports any current oracle module.
    load('oracle_finance', frozen / 'oracle_finance.py')
    load('verify_stellaris', frozen / 'verify_stellaris.py')
    oe = load('wi064_entering_oracle', frozen / 'studies/oracle_entry.py')
    catalog = {e['constraint_id']: e for e in read(frozen / 'model-contract.json')['constraint_catalog']['concrete_entries']}
    assert len(catalog) == 20
    params = {k: v for k, v in read(H / 'preparation/resolved-defaults.json').items() if k not in NEW}
    current_catalog = {e['constraint_id']: e for e in read(H / 'preparation/package-contracts/model_contract.json')['constraint_catalog']['concrete_entries']}
    assert {k: e['predicate_ir'] for k, e in catalog.items()} == {k: e['predicate_ir'] for k, e in current_catalog.items()}
    path = R / 'native-cases.json'
    selected = read(path) if path.exists() else read(H / 'preparation/unique-proposals.json')
    rows = []
    for proposal in selected:
        pid = proposal.get('proposal_id', proposal.get('id'))
        point = {k: v for k, v in proposal.get('inputs', proposal.get('point')).items() if k not in NEW}
        try:
            channels = oe.evaluate(point)
            verdicts = {cid: 'satisfied' if derive_verdict(cid, e, oe.operand_bindings(), point, params, channels)[0] else 'violated' for cid, e in catalog.items()}
            rows.append({'proposal_id': pid, 'point': point, 'channels': channels, 'verdicts': verdicts, 'outcome': 'evaluated'})
        except ValueError as error:
            rows.append({'proposal_id': pid, 'point': point, 'outcome': 'refused', 'error': str(error)})
    (R / 'entering-all-points.json').write_text(json.dumps({'scope': 'Captured entering oracle evaluated at every selected point with the two new inputs removed; not old-native reexecution or historical source-study snapshots.', 'rows': rows}, indent=2, allow_nan=False) + '\n')
    print('Captured entering oracle:', len(rows), 'points;', sum(r['outcome'] == 'refused' for r in rows), 'refusals')


if __name__ == '__main__':
    main()
