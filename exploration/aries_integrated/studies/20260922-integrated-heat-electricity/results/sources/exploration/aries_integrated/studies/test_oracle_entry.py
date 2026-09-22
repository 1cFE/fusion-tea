"""Independent checker invariants; never execute the native package."""
import json
from pathlib import Path

import pytest

from exploration.aries_integrated.studies.oracle_entry import evaluate, output, plasma_power, P, A


@pytest.fixture
def baseline():
    return json.loads((Path(__file__).parent / "manifest.json").read_text())["baseline"]["point"]


def test_density_power_scaling(baseline):
    changed = baseline | {A+"amplitude": 1.1*baseline[A+"amplitude"]}
    assert plasma_power(changed)/plasma_power(baseline) == pytest.approx(1.21, rel=1e-12)


def test_rating_changes_no_physical_demand(baseline):
    original = evaluate(baseline)
    changed = evaluate(baseline | {P+"fuel_capacity__selected_rating": 1e22})
    margin = output("fuel_capacity", "margin")
    assert changed[margin] < 0 < original[margin]
    assert {k: v for k, v in changed.items() if k != margin} == {
        k: v for k, v in original.items() if k != margin}
