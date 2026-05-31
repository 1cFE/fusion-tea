#!/usr/bin/env python3
"""Tests for lib/model_setup_helpers.py — the shared four-step model_setup API.

Oracle: the Phase 0 prototype for concept 01-hts-compact-tokamak, re-pinned
against the Item-4 fixed library at the standardized lifetime (40 yr):

    native (P_native=233, n_mod=1, no overrides)   LCOE = 174.5 $/MWh
    1 GWe projection, library-bare (no overrides)   LCOE = 137.2 $/MWh
    1 GWe projection, all four overrides on          LCOE = 584.5 $/MWh

See .project/active/concept-rework-helpers-validators/design.md (Validation
Approach) for the re-pin provenance.
"""

from __future__ import annotations

import pytest
from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.validation import CostingInput, default_availability

from lib.model_setup_helpers import (
    enabled_overrides,
    print_cas_breakdown,
    run_native_and_1gw,
)

# ---------------------------------------------------------------------------
# Fixtures — lifted verbatim from the prototype model_setup.py (concept 01).
# ---------------------------------------------------------------------------

ARC_SPEC = dict(
    R0=3.3,
    plasma_t=1.13,
    elon=1.84,
    eta_th=0.46,
    p_input=38.6,
)

P_NATIVE = 233.0

ARC_OVERRIDES = [
    {
        "account": "C220103",
        "value": 6901.0,
        "enabled": True,
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": "Magnet+structure fabricated cost, 2014 USD inflated ×1.34.",
    },
    {
        "account": "C220101",
        "value": 348.0,
        "enabled": True,
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": "FLiBe liquid-immersion blanket, published $260M 2014 ×1.34.",
    },
    {
        "account": "C220106",
        "value": 123.0,
        "enabled": True,
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": "Double-walled Inconel-718 vacuum vessel, $92M 2014 ×1.34.",
    },
    {
        "account": "CAS27",
        "value": 146.0,
        "enabled": True,
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6; Araiinejad 2025 (price)",
        "rationale": "950 t FLiBe × $154/kg NOAK = $146M.",
    },
]


def _tokamak_model() -> CostModel:
    return CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)


# ---------------------------------------------------------------------------
# Spy — records the kwargs of every forward() call without touching the library.
# ---------------------------------------------------------------------------


class SpyModel:
    """Stand-in for CostModel that records forward() kwargs.

    Carries a real ``concept`` so ``default_availability(model.concept)`` in
    the helper resolves to the library default (0.85 for TOKAMAK).
    """

    def __init__(self, concept: ConfinementConcept = ConfinementConcept.TOKAMAK):
        self.concept = concept
        self.calls: list[dict] = []

    def forward(self, **kwargs):
        self.calls.append(kwargs)
        return None


# ---------------------------------------------------------------------------
# Oracle — the load-bearing reproduction against the fixed library.
# ---------------------------------------------------------------------------


class TestOracle:
    def test_oracle_concept01(self):
        model = _tokamak_model()
        result, result_1gw = run_native_and_1gw(
            model, ARC_SPEC, ARC_OVERRIDES, P_NATIVE
        )
        assert result.costs.lcoe == pytest.approx(174.5, abs=0.5)  # native
        assert result_1gw.costs.lcoe == pytest.approx(584.5, abs=0.5)  # all-on

    def test_empty_overrides_is_library_bare(self):
        """No overrides → the 1 GWe projection is the library-bare answer."""
        model = _tokamak_model()
        result, result_1gw = run_native_and_1gw(model, ARC_SPEC, [], P_NATIVE)
        assert result.costs.lcoe == pytest.approx(174.5, abs=0.5)
        assert result_1gw.costs.lcoe == pytest.approx(137.2, abs=0.5)


# ---------------------------------------------------------------------------
# FR-1 / Invariant 1 — exact kwarg shape, no financial defaults from the file.
# ---------------------------------------------------------------------------


class TestForwardKwargShape:
    def test_no_financial_defaults_from_caller(self):
        spy = SpyModel()
        run_native_and_1gw(spy, ARC_SPEC, [], P_NATIVE)
        assert len(spy.calls) == 2
        for call in spy.calls:
            # The per-concept file contributes no financial defaults.
            assert "interest_rate" not in call
            assert "inflation_rate" not in call
            assert "construction_time_yr" not in call
            # availability / lifetime_yr are passed but library-sourced.
            assert call["availability"] == 0.85
            assert call["lifetime_yr"] == 40.0
            # spec is splatted through.
            assert call["R0"] == 3.3
            assert call["noak"] is True
            # n_mod is keyed off net_electric_mw.
            if call["net_electric_mw"] == P_NATIVE:
                assert call["n_mod"] == 1
            else:
                assert call["net_electric_mw"] == 1000.0
                assert call["n_mod"] == pytest.approx(1000.0 / P_NATIVE)

    def test_native_call_omits_override_kwargs(self):
        spy = SpyModel()
        run_native_and_1gw(spy, ARC_SPEC, ARC_OVERRIDES, P_NATIVE)
        native = next(c for c in spy.calls if c["net_electric_mw"] == P_NATIVE)
        assert "cost_overrides" not in native
        assert "override_reference_mw" not in native

    def test_projection_passes_override_reference_mw(self):
        spy = SpyModel()
        run_native_and_1gw(spy, ARC_SPEC, ARC_OVERRIDES, P_NATIVE)
        proj = next(c for c in spy.calls if c["net_electric_mw"] == 1000.0)
        assert proj["override_reference_mw"] == P_NATIVE
        assert proj["cost_overrides"] == {
            "C220103": 6901.0,
            "C220101": 348.0,
            "C220106": 123.0,
            "CAS27": 146.0,
        }

    def test_availability_concept_sourced(self):
        """availability comes from default_availability(model.concept), not a
        hardcoded literal — a MIRROR model gets 0.87, not 0.85."""
        spy = SpyModel(concept=ConfinementConcept.MIRROR)
        run_native_and_1gw(spy, ARC_SPEC, [], P_NATIVE)
        expected = default_availability(ConfinementConcept.MIRROR)
        assert expected == 0.87  # guard: the library default we rely on
        for call in spy.calls:
            assert call["availability"] == expected

    def test_lifetime_sourced_from_library_default(self):
        spy = SpyModel()
        run_native_and_1gw(spy, ARC_SPEC, [], P_NATIVE)
        lib_default = CostingInput.model_fields["lifetime_yr"].default
        for call in spy.calls:
            assert call["lifetime_yr"] == lib_default


# ---------------------------------------------------------------------------
# Invariant 3 — P_native == 1000 collapses native and projection.
# ---------------------------------------------------------------------------


class TestPNative1000Collapses:
    def test_n_mod_is_one(self):
        spy = SpyModel()
        run_native_and_1gw(spy, ARC_SPEC, [], 1000.0)
        proj = next(c for c in spy.calls if c["net_electric_mw"] == 1000.0)
        assert proj["n_mod"] == pytest.approx(1.0)

    def test_native_equals_projection(self):
        model = _tokamak_model()
        result, result_1gw = run_native_and_1gw(model, ARC_SPEC, [], 1000.0)
        assert result.costs.lcoe == pytest.approx(result_1gw.costs.lcoe)


# ---------------------------------------------------------------------------
# enabled_overrides — filter + last-wins-on-duplicate.
# ---------------------------------------------------------------------------


class TestEnabledOverrides:
    def test_filters_disabled(self):
        overrides = [
            {"account": "A", "value": 1.0, "enabled": True, "provenance": "direct",
             "source": "s", "rationale": "r"},
            {"account": "B", "value": 2.0, "enabled": False, "provenance": "direct",
             "source": "s", "rationale": "r"},
        ]
        assert enabled_overrides(overrides) == {"A": 1.0}

    def test_empty(self):
        assert enabled_overrides([]) == {}

    def test_last_wins_on_duplicate(self):
        overrides = [
            {"account": "A", "value": 1.0, "enabled": True, "provenance": "direct",
             "source": "s", "rationale": "r"},
            {"account": "A", "value": 9.0, "enabled": True, "provenance": "direct",
             "source": "s", "rationale": "r"},
        ]
        assert enabled_overrides(overrides) == {"A": 9.0}


# ---------------------------------------------------------------------------
# print_cas_breakdown — must emit the grep-able LCOE line (Invariant 7).
# ---------------------------------------------------------------------------


class TestPrintCasBreakdown:
    def test_emits_grepable_lcoe_line(self, capsys):
        import re

        model = _tokamak_model()
        result, result_1gw = run_native_and_1gw(
            model, ARC_SPEC, ARC_OVERRIDES, P_NATIVE
        )
        print_cas_breakdown(result, result_1gw, ARC_OVERRIDES)
        out = capsys.readouterr().out
        # run_model greps this exact pattern from model_setup.py stdout.
        m = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", out)
        assert m, "print_cas_breakdown must emit a `LCOE: <n> $/MWh` line"
        assert float(m.group(1)) == pytest.approx(584.5, abs=0.5)
