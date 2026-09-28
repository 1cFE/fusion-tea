"""Independent equation fixtures, including unresolved binary64 terminal gaps."""
from math import exp, log

import mpmath as mp
import pytest

from exploration.exchanger_architecture.thermal_requirements.studies import thermal_oracle as oracle


@pytest.mark.parametrize("ratio", [0.1, 0.99999999999, 1.0, 1.00000000001, 10.0])
@pytest.mark.parametrize("ua", [0.001, 2.0, 50.0, 1000.0])
def test_passive_lmtd_against_high_precision(ratio, ua):
    ch, cs, drive = 4*ratio, 4.0, 300.0
    low = oracle.precise_passive_transfer(drive, ua, ch, cs, 80)
    high = oracle.precise_passive_transfer(drive, ua, ch, cs, 160)
    assert low == high
    assert oracle.passive_transfer(drive, ua, ch, cs) == pytest.approx(high, rel=2e-14)


@pytest.mark.parametrize("hot_gap,cold_gap", [(30., 30.), (200., 30.), (30., 200.), (230., 1e-30), (1e-25, 230.)])
def test_log_domain_inverse_retains_both_terminal_limits(hot_gap, cold_gap):
    with mp.workdps(100):
        a, b = mp.mpf(hot_gap), mp.mpf(cold_gap)
        mean = a if a == b else (a-b)/mp.log(a/b)
    reconstructed, logarithm = oracle.cold_gap_from_lmtd(hot_gap, float(mean))
    assert reconstructed == pytest.approx(cold_gap, rel=2e-11)
    assert logarithm == pytest.approx(log(cold_gap), abs=1e-11)


def test_equal_capacity_energy_and_lmtd():
    q = oracle.passive_transfer(200., 5., 2., 2.)
    gap = 200-q/2
    assert q == pytest.approx(5*gap)


@pytest.mark.parametrize("duty,ua,hot,secondary", [(0., 5., 900., 600.), (100., 0., 900., 600.), (100., 5., 600., 900.)])
def test_inactive_domains(duty, ua, hot, secondary):
    result = oracle.stage(duty=duty, ua=ua, ch=4., cs=3., source_hot=hot,
                          secondary=secondary, controlled=True)
    assert result["state_defined"] == 0
    assert result["transferred"] == 0
    assert result["unmet"] == duty
    assert result["bypass_fraction"] == 0
    assert result["mixed_return"] == hot


def test_saturated_cold_gap_keeps_transfer_and_mixing():
    duty, ch, cs, hot, secondary = 276.5, 2.5965, 5.7123, 952.6395051030233, 674.4473216951321
    result = oracle.stage(duty=duty, ua=50., ch=ch, cs=cs, source_hot=hot,
                          secondary=secondary, controlled=True)
    assert result["state_defined"] == 1
    assert result["transferred"] == duty
    assert result["cold_terminal_difference"] < 1e-10
    assert result["cold_gap_log"] < -35
    active = result["active_capacity"]
    bypass = result["bypass_fraction"]
    assert active*(hot-result["hx_return"]) == pytest.approx(duty)
    assert bypass*hot+(1-bypass)*result["hx_return"] == pytest.approx(hot-duty/ch)
    # Compute LMTD from its retained logarithmic gap, avoiding subtraction.
    a = result["hot_terminal_difference"]
    b = exp(result["cold_gap_log"])
    assert 50*(a-b)/(log(a)-result["cold_gap_log"]) == pytest.approx(duty, rel=2e-12)


def test_saturated_hot_gap_preserves_finite_state():
    result = oracle.stage(duty=100., ua=1000., ch=10., cs=1., source_hot=900.,
                          secondary=800., controlled=True)
    assert result["state_defined"] == 1
    assert result["transferred"] == 100.
    assert result["hot_terminal_difference"] == 0.
    assert result["mixed_return"] == 890.
    log_a, log_b = oracle.passive_log_terminal_gaps(100., 1000., 10., 1.)
    assert log_a < -800  # A positive gap smaller than binary64 can represent.
    assert 1000*(exp(log_b)-exp(log_a))/(log_b-log_a) == pytest.approx(100.)


def test_insufficient_area_keeps_partial_transfer_and_return_error():
    result = oracle.stage(duty=500., ua=1., ch=4., cs=3., source_hot=900.,
                          secondary=600., controlled=True)
    assert 0 < result["transferred"] < 500
    assert result["bypass_fraction"] == 0
    target = 900-500/4
    assert result["mixed_return"]-target == pytest.approx(result["unmet"]/4)


@pytest.mark.parametrize("network", [0, 1])
def test_coupled_cycle_balances_partial_duty(network):
    branches = {name: dict(duty=q, ua=u, ch=ch, source_hot=h, controlled=True)
                for name, q, u, ch, h in [("he", 500., 3., 10., 730.),
                    ("divertor", 300., 2., 3., 960.), ("pbli", 900., 0.5, 5., 1000.)]}
    t, inlet, states, residual = oracle.solve_cycle(400., .65, .8, 6., network, .75, branches)
    accepted = sum(s["transferred"] for s in states.values())
    assert 6*(t-inlet) == pytest.approx(accepted, abs=1e-8)
    assert abs(residual) < 1e-8
    assert any(s["unmet"] > 0 for s in states.values())
    if network:
        assert states["pbli"]["secondary_in"] == states["divertor"]["secondary_in"]
        assert t == pytest.approx(.75*states["pbli"]["secondary_out"]+.25*states["divertor"]["secondary_out"])
    else:
        assert states["pbli"]["secondary_in"] == states["divertor"]["secondary_out"]
        assert t == pytest.approx(states["pbli"]["secondary_out"])
