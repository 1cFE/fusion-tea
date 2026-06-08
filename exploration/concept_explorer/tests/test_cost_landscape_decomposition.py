"""Cost-landscape LCOE decomposition (Theme F, Phase 1).

The cost-landscape page stacks a concept's *annualised* cost components so they
sum to its headline LCOE (Bet B1 / invariant I1). This module proves the
decomposition is exact, and that the new ``cas71``/``cas72`` O&M split is wired
correctly with honest degradation when a concept's model never separated it.

Two layers, deliberately:

- **Served data (today).** The annualised buckets that already ship — capital
  (cas90), combined O&M (cas70), fuel (cas80) — must reconstruct the stored
  headline LCOE through the real energy formula. This is the load-bearing B1
  proof and it runs on the *current* served JSON; it does not need the cas71/72
  re-extract (the split sums back to cas70, so the combined bucket suffices for
  the reconstruction).
- **Split wiring (synthetic).** ``from_forward_result`` builds cas71/cas72 when
  the forward result carries them (and ``cas71 + cas72 == cas70``), and leaves
  them ``None`` when it does not — exercised through the constructor so it holds
  before the served concepts are re-extracted.

The remaining proof — that the cas71/72 split is present in the *re-extracted
served JSON* and sums there too (plan Phase 1 "first proof point") — is
intentionally deferred with the re-extract and is not asserted here.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from exploration.concept_explorer.models import CASAccount, CostModelData
from exploration.concept_explorer.server import BASE_DIR

_DATA_DIR = BASE_DIR / "data"

# costingfe-backed concepts spanning the LCOE range (cheap module farm → mid →
# expensive), each chosen so the headline reconstructs exactly from components.
_SERVED_CONCEPTS = ["01", "24", "23"]

# The annualised components additive to LCOE (see economics.py:78):
# LCOE = (CAS90 + CAS70 + CAS80) * 1e6 / (8760 * p_net * n_mod * availability)
_HOURS_PER_YEAR = 8760.0


# ---------------------------------------------------------------------------
# Served-data B1/I1 proof — runs on the current JSON, no re-extract needed
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cid", _SERVED_CONCEPTS)
def test_served_components_reconstruct_headline_lcoe(cid: str) -> None:
    """B1/I1: capital + O&M + fuel reconstruct the stored headline LCOE.

    Loads the served cost model through the (now cas71/72-aware) schema and
    rebuilds LCOE from the annualised components via the real energy formula.
    Equality here is what makes the stacked bar honest — the segments sum to
    the headline.
    """
    cm = _load_served_cost_model(cid)

    # The combined-O&M schema still loads cleanly pre-re-extract: the split is
    # genuinely absent in today's JSON, so it must read as None, not a zero.
    assert cm.cas71 is None
    assert cm.cas72 is None

    annualised = cm.cas90.cost_m_usd + cm.cas70.cost_m_usd + cm.cas80.cost_m_usd
    n_mod = cm.params["n_mod"]
    denom = _HOURS_PER_YEAR * cm.headline.p_net_mw * cm.headline.capacity_factor * n_mod
    reconstructed = annualised * 1e6 / denom

    assert reconstructed == pytest.approx(cm.headline.lcoe_per_mwh, rel=1e-4)


@pytest.mark.parametrize("cid", _SERVED_CONCEPTS)
def test_served_component_shares_sum_to_headline(cid: str) -> None:
    """The chart's $/MWh decomposition (D2) sums to the headline LCOE.

    Mirrors the front-end math: each component's $/MWh = its share of the
    annualised sum × LCOE. Today only the combined-O&M bucket is available, so
    the buckets are capital/O&M/fuel; the cas71/72 split refines the O&M bucket
    without changing the sum (cas71 + cas72 == cas70).
    """
    cm = _load_served_cost_model(cid)

    lcoe = cm.headline.lcoe_per_mwh
    annualised = cm.cas90.cost_m_usd + cm.cas70.cost_m_usd + cm.cas80.cost_m_usd
    buckets = [cm.cas90, cm.cas70, cm.cas80]
    per_mwh_sum = sum(b.cost_m_usd / annualised * lcoe for b in buckets)

    assert per_mwh_sum == pytest.approx(lcoe, rel=1e-9)


# ---------------------------------------------------------------------------
# Split wiring (synthetic) — exercises cas71/cas72 before the re-extract
# ---------------------------------------------------------------------------


def test_from_forward_result_builds_split_and_reconstitutes_cas70() -> None:
    """from_forward_result reads cas71/cas72 and they reconstitute cas70 (I6)."""
    cmd = CostModelData.from_forward_result(
        _forward_result_with_split(cas71=130.0, cas72=17.99, cas70=147.99),
        sensitivities=None,
    )

    assert isinstance(cmd.cas71, CASAccount)
    assert isinstance(cmd.cas72, CASAccount)
    assert cmd.cas71.cost_m_usd == 130.0
    assert cmd.cas72.cost_m_usd == 17.99
    assert cmd.cas71.name == "Fixed O&M (annualised)"
    assert cmd.cas72.name == "Scheduled Replacement (annualised)"
    # The split must reconstitute the combined bucket the rest of the model uses.
    assert cmd.cas71.cost_m_usd + cmd.cas72.cost_m_usd == pytest.approx(
        cmd.cas70.cost_m_usd, rel=1e-9
    )


def test_split_four_way_decomposition_sums_to_headline() -> None:
    """With the split present, the four-segment $/MWh decomposition sums to LCOE.

    This is exactly what the stacked bar renders: capital (cas90), fixed O&M
    (cas71), replacement (cas72), fuel (cas80), each as its share of the
    annualised sum × LCOE (I1).
    """
    cmd = CostModelData.from_forward_result(
        _forward_result_with_split(cas71=130.0, cas72=17.99, cas70=147.99),
        sensitivities=None,
    )

    lcoe = cmd.headline.lcoe_per_mwh
    annualised = cmd.cas90.cost_m_usd + cmd.cas70.cost_m_usd + cmd.cas80.cost_m_usd
    segments = [cmd.cas90, cmd.cas71, cmd.cas72, cmd.cas80]
    per_mwh_sum = sum(s.cost_m_usd / annualised * lcoe for s in segments)

    assert per_mwh_sum == pytest.approx(lcoe, rel=1e-9)


def test_from_forward_result_absent_split_degrades_to_none() -> None:
    """A forward result without cas71/cas72 yields None, not a fabricated zero.

    This is the honest-degradation path for concepts whose model never separated
    fixed O&M from scheduled replacement (37/39) — the cost-landscape shows a
    combined-O&M segment for them rather than a fake split (FR-F10).
    """
    result = _forward_result_with_split(cas71=130.0, cas72=17.99, cas70=147.99)
    del result["costs"]["cas71"]
    del result["costs"]["cas72"]

    cmd = CostModelData.from_forward_result(result, sensitivities=None)

    assert cmd.cas71 is None
    assert cmd.cas72 is None
    # The combined bucket is unaffected — only the split is absent.
    assert isinstance(cmd.cas70, CASAccount)
    assert cmd.cas70.cost_m_usd == 147.99


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_served_cost_model(cid: str) -> CostModelData:
    """Load one served concept's cost model through the live schema."""
    payload = json.loads((_DATA_DIR / f"{cid}.json").read_text(encoding="utf-8"))
    return CostModelData.model_validate(payload["cost_model"])


def _forward_result_with_split(*, cas71: float, cas72: float, cas70: float) -> dict[str, Any]:
    """A minimal forward-result dict carrying the cas71/cas72 O&M split.

    Mirrors ``dataclasses.asdict(ForwardResult)`` with a self-consistent
    annualised set so the decomposition math is exercised on real-shaped data.
    """
    return {
        "costs": {
            "cas10": 0.0, "cas21": 0.0, "cas22": 0.0, "cas23": 0.0, "cas24": 0.0,
            "cas25": 0.0, "cas26": 0.0, "cas27": 0.0, "cas28": 0.0, "cas29": 0.0,
            "cas30": 0.0, "cas40": 0.0, "cas50": 0.0, "cas60": 0.0,
            "cas70": cas70, "cas71": cas71, "cas72": cas72,
            "cas80": 0.93, "cas90": 1006.5,
            "lcoe": 155.17, "overnight_cost": 8500.0, "total_capital": 4200.0,
        },
        "power_table": {"p_net": 250.0, "q_eng": 3.5, "capacity_factor": 0.85},
        "cas22_detail": {},
        "overridden": [],
        "params": {"n_mod": 4.0, "availability": 0.85},
    }
