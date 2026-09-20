"""Native parity for generated administrative flags; expected values stay independent."""
import importlib
import sys
from pathlib import Path

import pytest
from tests.models.test_supplied_thermal_capability import native_capability  # noqa: F401

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'exploration/stellarator_e2e'))
oracle = importlib.import_module('oracle_capability')


@pytest.fixture(scope='module')
def expected_reference():
    verifier = importlib.import_module('verify_stellaris')
    p = dict(verifier.IN) | oracle.DEFAULTS
    return p, verifier.compute()


@pytest.mark.parametrize('suffix', oracle.FLAG_DEFAULTS)
def test_false_public_flag_matches_independent_expected(native_capability, expected_reference, suffix):
    execute, predicates, _ = native_capability
    p, r = expected_reference
    key, _ = oracle.FLAG_DEFAULTS[suffix]
    expected = oracle.evaluate(p | {key: False}, r)
    native = execute({suffix: False})
    names = (['cold_stage', 'intercept_stage'] if suffix == oracle.CRYO_ENABLED_SUFFIX
             else [suffix.split('__')[1].removesuffix('_capability')])
    for name in names:
        for field in ('margin', 'defined', 'applicable', 'supported', 'capacity_ok'):
            result = f'capability_{name}_{field}'
            actual = native.outputs[oracle.OUTPUT_MAP[result]]
            if field == 'margin':
                assert actual == pytest.approx(expected[result], abs=1e-8)
            else:
                assert actual == expected[result]
        assert expected[f'capability_{name}_defined'] == 0.
        assert not expected[f'capability_{name}_capacity_ok']
