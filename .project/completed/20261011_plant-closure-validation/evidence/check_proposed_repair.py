"""Bounded synthetic check of the unapplied patch; never executes a model."""
import csv
import importlib.util
import json
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
ROOT = Path(__file__).resolve().parent / 'proposed-code'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


helper = load(Path('tests/study/test_study_publication_fail_closed.py'), 'helper')
native = load(Path('tests/study/test_native_publication.py'), 'native')
results = []
for path in ROOT.glob('exploration/stellarator_e2e/studies/*/study.py'):
    original = path.relative_to(ROOT)
    study = load(original, original.parent.name)
    exec(compile(path.read_text(), str(original), 'exec'), study.__dict__)
    for bad in ['complete', 'absent', None, float('nan')]:
        with tempfile.TemporaryDirectory() as directory:
            cases = [helper._local_case(study), helper._local_case(study)]
            cases[1].candidate_id = 'second-case'
            target = Path(directory) / 'points.csv'
            target.write_text('previous\n')
            if bad == 'absent':
                del cases[1].outputs[study.CHANNELS['fuel']]
            elif bad != 'complete':
                cases[1].outputs[study.CHANNELS['fuel']] = bad
            try:
                helper._export_local(study, cases, target)
                assert bad == 'complete', 'accepted invalid value'
                rows = list(csv.DictReader(target.open()))
                assert all(float(rows[0][name]) == cases[0].outputs[channel]
                           for name, channel in study.CHANNELS.items())
            except study.route.RouteError as error:
                assert bad != 'complete'
                assert study.CHANNELS['fuel'] in str(error)
                assert target.read_text() == 'previous\n'
            results.append(dict(writer=study.__name__, case=str(bad), outcome='pass'))

native.ROOT = ROOT / 'exploration/stellarator_e2e/studies'
for bad in ['complete', 'absent', None, float('nan'), float('inf'), -float('inf')]:
    with tempfile.TemporaryDirectory() as directory:
        data = native.cases()
        target = Path(directory) / 'native-points.csv'
        target.write_text('previous\n')
        if bad == 'absent':
            del data[1].outputs['required']
        elif bad != 'complete':
            data[1].outputs['required'] = bad
        try:
            native.publication('20260912-plant-closure', data, Path(directory))
            assert bad == 'complete'
        except native.route.RouteError as error:
            assert bad != 'complete'
            assert 'required' in str(error)
            assert target.read_text() == 'previous\n'
        results.append(dict(writer='plant-closure', case=str(bad), outcome='pass'))
print(json.dumps(results, indent=2))
