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
    physical_owners=('source','fuel','he_coolant','pbli_coolant','divertor_coolant',
                     'heat_exchangers','deposition','plant_ledger','generator_auxiliaries')
    physical=lambda row:{k:v for k,v in row.items() if any(k.startswith(P+owner+'__') for owner in physical_owners)}
    assert physical(changed)==physical(original)
    cost=P+'fuel_processing_equipment__purchase__capital'
    assert changed[cost]<original[cost]
