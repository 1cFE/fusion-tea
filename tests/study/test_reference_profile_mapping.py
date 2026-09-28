"""Public reconstruction inputs reach the oracle without state or cache leakage."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'exploration/stellarator_e2e/studies'))
import oracle_entry as oracle


@pytest.mark.parametrize('name,value', [('alpha_n', .35), ('alpha_T', 1.2), ('f_shape', 1.02)])
def test_reconstruction_input_changes_physics_and_restores_defaults(name, value):
    before = oracle.evaluate({})
    saved = dict(oracle.vs.IN)
    changed = oracle.evaluate({oracle.P + 'plasma__' + name: value})
    direct = oracle._compute({name: value})
    assert changed == {channel: float(direct[key]) for key, channel in oracle.ORACLE_OUTPUT_TO_CHANNEL.items()}
    fusion = oracle.ORACLE_OUTPUT_TO_CHANNEL['p_fus']
    assert changed[fusion] != before[fusion]
    volume = oracle.ORACLE_OUTPUT_TO_CHANNEL['V']
    if name == 'f_shape':
        assert changed[volume] / before[volume] == pytest.approx(value / saved[name])
    else:
        assert changed[volume] == before[volume]
    assert oracle.vs.IN == saved
    assert oracle.evaluate({}) == before


def test_unknown_profile_input_still_refused():
    with pytest.raises(oracle.OracleSeamError, match='no declared oracle mapping'):
        oracle.evaluate({oracle.P + 'plasma__alpha_missing': .35})
