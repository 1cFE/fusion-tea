"""Cost-model extractor tests (slice 2)."""
from __future__ import annotations

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
        cost_model.extract(
            "02-acoustic-icf-sonofusion", "w_coils", {"extractor": "cost_model"}
        )


def test_dollars_dominated_subsystem_matches_design_expectation():
    # 01-hts-compact-tokamak: coils (REBCO magnets+struct) dominate CAS22.
    weights = cost_model.compute_weights("01-hts-compact-tokamak")
    assert weights["coils"] > 0.5
    # 10-large-scale-stellarator: coils still the largest single subsystem
    # under format-B parsing of the GIGA sub-allocation prose.
    stell = cost_model.compute_weights("10-large-scale-stellarator")
    assert stell is not None
    assert stell["coils"] > stell["vessel"]
