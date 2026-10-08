"""Cost-model extractor tests (slice 2)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from exploration.scoring_v2.lib.extractors import cost_model


def test_cost_model_extractor_sums_to_one():
    weights = cost_model.compute_weights("01-hts-compact-tokamak")
    assert weights is not None
    assert set(weights) == set(cost_model.SUBSYSTEMS)
    assert abs(sum(weights.values()) - 1.0) < 1e-6


def test_cost_model_missing_returns_none_no_fallback():
    # 02-acoustic-icf-sonofusion has no model_output.txt in the slice-2 corpus.
    assert cost_model.compute_weights("02-acoustic-icf-sonofusion") is None


def test_cost_model_dispatcher_signature_matches_taxonomy():
    val, prov, conf = cost_model.extract(
        "01-hts-compact-tokamak", "w_coils", {"extractor": "cost_model"}
    )
    assert isinstance(val, float)
    assert 0.0 <= val <= 1.0
    assert prov.endswith("model_output.txt")
    assert conf == "medium"


def test_cost_model_dispatcher_raises_for_concept_without_model():
    # Mirror of taxonomy.extract's KeyError shape — caller treats it as
    # "leave this feature absent" (no fallback per design).
    with pytest.raises(KeyError, match="no model_output.txt"):
        cost_model.extract("02-acoustic-icf-sonofusion", "w_coils", {"extractor": "cost_model"})


def test_dollars_dominated_subsystem_matches_design_expectation():
    # fd76070c2 source table: last numeric column is the 1 GWe basis. Shares
    # use all seven classified buckets, rather than CAS22 alone.
    amounts = {
        "vessel": {"C220105": "10.4", "C220106": "50.4", "C220108": "57.8"},
        "coils": {"C220103": "1030.0", "C220107": "40.0"},
        "blanket": {"C220101": "140.5", "CAS27": "10.0"},
        "bop": {
            "C220109": "0.0",
            "C220200": "207.9",
            "CAS23": "293.2",
            "CAS24": "124.9",
            "CAS26": "126.7",
        },
        "fuel_cycle": {"C220112": "0.0", "C220400": "7.3", "C220500": "120.0"},
        "aux": {
            "C220104": "215.0",
            "C220110": "91.3",
            "C220300": "15.5",
            "C220600": "11.5",
            "C220700": "88.3",
            "CAS25": "76.0",
            "CAS28": "5.0",
        },
        "civil": {"C220102": "94.1", "C220111": "177.3", "CAS10": "17.2", "CAS21": "741.4"},
    }
    source = (
        Path(__file__).resolve().parents[2]
        / "exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_output.txt"
    )
    expected_rows = {
        code: Decimal(value) for group in amounts.values() for code, value in group.items()
    }
    # Independent reader of this explicit three-column fixture; production regex is not reused.
    rows = {
        parts[0]: Decimal(parts[3])
        for line in source.read_text().splitlines()
        if (parts := line.split()) and parts[0] in expected_rows
    }
    assert rows == expected_rows
    buckets = {
        name: sum(Decimal(value) for value in group.values()) for name, group in amounts.items()
    }
    total = sum(buckets.values())
    assert total == Decimal("3751.7")
    assert buckets["coils"] == Decimal("1070.0")
    weights = cost_model.compute_weights("01-hts-compact-tokamak")
    assert weights == pytest.approx(
        {name: float(value / total) for name, value in buckets.items()}, rel=1e-12
    )
    assert weights["coils"] > weights["vessel"] and weights["coils"] > weights["blanket"]
    # 10-large-scale-stellarator: coils still the largest single subsystem
    # under format-B parsing of the GIGA sub-allocation prose.
    stell = cost_model.compute_weights("10-large-scale-stellarator")
    assert stell is not None
    assert stell["coils"] > stell["vessel"]
