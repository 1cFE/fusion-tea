"""WI-046 (goal plant-closure round 1, 2026-09-08): the lifecycle calendar's boundary cases.

The handwritten impl walks intervals; the oracle derives the closed form
t_k = k*L/b + (k-1)*d (design D1). They are checked against each other on the
lifetime research's synthetic cases (spec MR-WI046-12; the research's lines 100-110)
and against the research's stated values. The held mode is checked against the
retired chain's oracle mirror by ``==`` (spec MR-WI046-5).
"""

import math
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
E2E = REPO_ROOT / "exploration" / "stellarator_e2e"
# The impl imports the sealed package's pydantic input class, which needs teax's simkit:
# the integration env names the checkout (STOP_PARSER_TEAX_ROOT), as the single runner does.
_teax = os.environ.get("STOP_PARSER_TEAX_ROOT")
for path in ([Path(_teax) / "packages" / "teax-simkit"] if _teax else []) + [E2E, E2E / "pkg"]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
pytest.importorskip("simkit", reason="teax simkit not on the path (set STOP_PARSER_TEAX_ROOT)")

from stellarator_tea.handwritten.mfe_lifecycle.lifecycle_calendar_impl import (  # noqa: E402
    lifecycle_calendar_held,
    lifecycle_calendar_live,
)
from verify_stellaris import (  # noqa: E402
    _oracle_levelized_replacement_cost,
    _oracle_lifecycle_calendar,
)

KEYS = (
    "availability", "coil_life_margin_fpy", "replacement_pv", "planned_downtime_yr",
    "terminal_downtime_yr", "unplanned_downtime_yr", "productive_fpy", "dated_energy_ratio",
    "cas72_annual", "n_replacements", "physical_life_fpy",
)
# L = 18 / 4.5 = 4 FPY, the research's synthetic case
BASE = dict(cost_per_event=671_160_000.0, q_n=4.5, fluence_limit=18.0, interest_rate=0.07,
            operational_years=10.0, outage_years=7.0 / 12.0, unplanned_fraction=0.0,
            coil_life_fpy=10.0)


def _rel(a, b):
    if math.isinf(a) or math.isinf(b):
        return 0.0 if (math.isinf(a) and math.isinf(b)) else math.inf
    return abs(a - b) / (abs(b) or 1.0)


def _walk_equals_closed_form(arguments):
    impl = lifecycle_calendar_live(**arguments)
    orac = _oracle_lifecycle_calendar(availability_direct=0.0, **arguments)
    assert max(_rel(impl[k], orac[k]) for k in KEYS) < 1e-9
    assert all(abs(a - b) < 1e-9 for a, b in zip(impl["events"], orac["events"]))
    assert len(impl["events"]) == len(orac["events"])
    balance = (impl["productive_fpy"] + impl["planned_downtime_yr"]
               + impl["unplanned_downtime_yr"] + impl["terminal_downtime_yr"])
    assert abs(balance - arguments["operational_years"]) < 1e-9  # F + T_p + T_u + T_term = N
    return impl


def test_two_events_inside_a_ten_year_horizon():
    r = _walk_equals_closed_form(BASE)
    assert r["n_replacements"] == 2.0
    assert [round(t, 6) for t in r["events"]] == [4.0, round(8.0 + 7.0 / 12.0, 6)]
    assert abs(r["availability"] - 53.0 / 60.0) < 1e-12
    assert abs(r["planned_downtime_yr"] - 7.0 / 6.0) < 1e-12


def test_horizon_ending_inside_a_prospective_outage_buys_no_terminal_replacement():
    r = _walk_equals_closed_form(dict(BASE, operational_years=8.7))
    assert r["n_replacements"] == 1.0
    assert abs(r["terminal_downtime_yr"] - (8.7 - (8.0 + 7.0 / 12.0))) < 1e-9
    assert abs(r["productive_fpy"] - 8.0) < 1e-9


def test_restart_exactly_at_retirement_is_not_strictly_before():
    on_the_boundary = _walk_equals_closed_form(dict(BASE, operational_years=9.0 + 2.0 / 12.0))
    just_past = _walk_equals_closed_form(dict(BASE, operational_years=9.0 + 2.0 / 12.0 + 1e-6))
    assert on_the_boundary["n_replacements"] == 1.0
    assert just_past["n_replacements"] == 2.0


def test_zero_damage_means_infinite_life_and_no_event():
    r = _walk_equals_closed_form(dict(BASE, q_n=0.0))
    assert math.isinf(r["physical_life_fpy"])
    assert r["n_replacements"] == 0.0 and r["replacement_pv"] == 0.0
    assert r["availability"] == 1.0


def test_zero_outage_still_charges_the_events():
    r = _walk_equals_closed_form(dict(BASE, outage_years=0.0))
    assert r["availability"] == 1.0
    assert r["n_replacements"] == 2.0 and r["cas72_annual"] > 0.0


def test_zero_discount_gives_a_unit_energy_ratio_and_a_plain_average():
    r = _walk_equals_closed_form(dict(BASE, interest_rate=0.0))
    assert abs(r["dated_energy_ratio"] - 1.0) < 1e-12
    assert abs(r["cas72_annual"] - r["replacement_pv"] / BASE["operational_years"]) < 1e-6


def test_productive_time_is_non_increasing_in_the_unplanned_fraction():
    f = [_walk_equals_closed_form(dict(BASE, unplanned_fraction=u))["productive_fpy"]
         for u in (0.0, 0.05, 0.10)]
    assert f[0] >= f[1] >= f[2]


def test_long_horizon_approaches_the_steady_cycle_limit():
    r = _walk_equals_closed_form(dict(BASE, operational_years=3000.0))
    L, d = 4.0, 7.0 / 12.0
    assert abs(r["availability"] - L / (L + d)) < 1e-3


def test_held_mode_equals_the_retired_chain_by_identity():
    for q_n, fluence, years in ((4.5, 18.0, 30.0), (100.0 * 0.7997724687144482 / 660.0791423448563, 500.0, 30.0),
                                 (50.0 * 0.7997724687144482 / 660.0791423448563, 18.0, 5.0)):
        held = lifecycle_calendar_held(cost_per_event=671_160_000.0, q_n=q_n, fluence_limit=fluence,
                                       availability=0.9, interest_rate=0.07, operational_years=years,
                                       coil_life_fpy=10.0)
        mirror = _oracle_levelized_replacement_cost(cost_per_event=671_160_000.0, q_n=q_n,
                                                    fluence_limit=fluence, availability=0.9,
                                                    interest_rate=0.07, operational_years=years)
        assert held["cas72_annual"] == mirror
        assert held["availability"] == 0.9 and held["dated_energy_ratio"] == 1.0


@pytest.mark.parametrize("bad", [
    dict(operational_years=0.0), dict(fluence_limit=0.0), dict(q_n=-1.0), dict(outage_years=-0.1),
    dict(unplanned_fraction=1.0), dict(cost_per_event=float("nan")),
])
def test_invalid_live_inputs_raise_rather_than_floor(bad):
    with pytest.raises(ValueError):
        lifecycle_calendar_live(**dict(BASE, **bad))
