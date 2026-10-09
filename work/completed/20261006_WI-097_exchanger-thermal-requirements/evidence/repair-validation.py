"""Run existing acceptance tests against fresh receipts without overwriting old evidence."""
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
TARGET = EVIDENCE / 'repair-validation'
TARGET.mkdir(exist_ok=True)
rows = json.loads((EVIDENCE / 'repair-native-controls.json').read_text())
core = [r for r in rows if not r['case'].startswith('repair-')]
assert len(core) == 18
(TARGET / 'native-controls.json').write_text(json.dumps(core, indent=2) + '\n')


class FreshEvidence:
    def pytest_collection_modifyitems(self, items):
        for item in items:
            module = item.module
            if module.__name__ == 'test_native_controls':
                module.EVIDENCE = TARGET
            elif module.__name__ == 'test_native_boundaries':
                module.runner.EVIDENCE = TARGET


raise SystemExit(pytest.main([
    str(ROOT / 'exploration/exchanger_architecture/thermal_requirements/tests/test_controlled_closure.py'),
    str(ROOT / 'exploration/exchanger_architecture/thermal_requirements/tests/test_native_controls.py'),
    str(ROOT / 'exploration/exchanger_architecture/thermal_requirements/tests/test_native_boundaries.py'),
    str(ROOT / 'exploration/exchanger_architecture/thermal_requirements/tests/test_repair_regression.py'),
    '-q',
], plugins=[FreshEvidence()]))
