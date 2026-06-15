#!/usr/bin/env python3
"""Tests for lib/model_setup_helpers.py — the shared three-forward model_setup API.

Oracle: the Phase 0 prototype for concept 01-hts-compact-tokamak. Re-pinned
2026-06-15 against 1costingfe@b9b0a4c after the tokamak 0D inverse + feasibility
gate adoption. Tokamak concepts now route through ``tokamak_0d_inverse`` via
``use_0d_model=True`` so the β_N / Greenwald / Troyon plasma-limit gate fires;
the 1 GWe projection switches from n_mod stacking to ``size_from_power=True``
so the library back-solves a single bigger geometry. ``B=9.2`` is now part of
ARC_SPEC because the 0D solve needs all four geometry knobs (R0, a, B, elon)
to land β_N inside Troyon at the native power target — omit B and the gate
fires at native scale.

    generic (P_native=233, n_mod=1, overrides off)   LCOE = 189.0 $/MWh
    native  (P_native=233, n_mod=1, overrides on)    LCOE = 628.3 $/MWh
    result_1gw (1 GWe projection, overrides on)      LCOE = 206.0 $/MWh

    1 GWe projection, library-bare (no overrides)    LCOE = 156.7 $/MWh

See .project/active/concept-rework-three-forward-contract/design.md (Validation
Approach) for the pinned-oracle provenance. Spy tests now patch both
``run_costing`` (non-tokamak / gate-off path) and ``_run_costing_no_sensitivity``
(tokamak 0D path) because the helper dispatches between them per concept family.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest
from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.adapter import FusionTeaInput
from costingfe.validation import CostingInput, default_availability

import lib.model_setup_helpers as helpers
from lib.model_setup_helpers import (
    enabled_overrides,
    generic_reference,
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
    B=9.2,        # required for 0D — without it β_N exceeds Troyon at native scale
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
# Capture — records each FusionTeaInput passed to run_costing without touching
# the library. The helper now routes the three forwards through
# costingfe.adapter.run_costing(FusionTeaInput(...)); install CaptureCosting via
# monkeypatch over helpers.run_costing to inspect the inputs it builds.
# ---------------------------------------------------------------------------


@dataclass
class _StubOut:
    """Minimal FusionTeaOutput stand-in so helpers._wrap() succeeds when
    run_costing is captured. The costed values are irrelevant to kwarg-shape
    assertions, so they default to empty/zero."""

    lcoe: float = 0.0
    overnight_cost: float = 0.0
    total_capital: float = 0.0
    costs: dict = field(default_factory=dict)
    power_table: dict = field(default_factory=dict)
    sensitivity: dict = field(default_factory=dict)
    overridden: list = field(default_factory=list)


class CaptureCosting:
    """Records each FusionTeaInput passed to run_costing, returning a stub
    output. The real library is never invoked, so spec/override validity is not
    exercised here — only the input shape the helper builds."""

    def __init__(self):
        self.inputs: list[FusionTeaInput] = []

    def __call__(self, inp: FusionTeaInput) -> _StubOut:
        self.inputs.append(inp)
        return _StubOut()


# ---------------------------------------------------------------------------
# Oracle — the load-bearing reproduction against the fixed library.
# ---------------------------------------------------------------------------


class TestOracle:
    def test_oracle_concept01(self):
        model = _tokamak_model()
        generic = generic_reference(model, ARC_SPEC, P_NATIVE)
        native, result_1gw = run_native_and_1gw(
            model, ARC_SPEC, ARC_OVERRIDES, P_NATIVE
        )
        assert generic.costs.lcoe == pytest.approx(189.0, abs=0.5)  # overrides OFF
        assert native.costs.lcoe == pytest.approx(628.3, abs=0.5)  # overrides ON, 233 MWe
        assert result_1gw.costs.lcoe == pytest.approx(206.0, abs=0.5)  # all-on, 1 GWe (size_from_power)

    def test_empty_overrides_is_library_bare(self):
        """No overrides → native == generic, and the 1 GWe projection is the
        library-bare answer."""
        model = _tokamak_model()
        generic = generic_reference(model, ARC_SPEC, P_NATIVE)
        native, result_1gw = run_native_and_1gw(model, ARC_SPEC, [], P_NATIVE)
        assert generic.costs.lcoe == pytest.approx(189.0, abs=0.5)
        assert native.costs.lcoe == pytest.approx(generic.costs.lcoe)  # empty ⇒ equal
        assert result_1gw.costs.lcoe == pytest.approx(156.7, abs=0.5)  # 1 GWe via size_from_power


# ---------------------------------------------------------------------------
# FR-1 / Invariant 1 — exact kwarg shape, no financial defaults from the file.
# ---------------------------------------------------------------------------


def _patch_both_run_costing(monkeypatch, cap):
    """Tokamak routes through ``_run_costing_no_sensitivity`` (0D path workaround
    for the upstream adapter sensitivity bug); non-tokamak routes through
    ``run_costing``. Patch both with the same spy so the captured inputs
    cover every dispatch path."""
    monkeypatch.setattr(helpers, "run_costing", cap)
    monkeypatch.setattr(helpers, "_run_costing_no_sensitivity", cap)


class TestForwardKwargShape:
    def test_no_financial_defaults_from_caller(self, monkeypatch):
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        run_native_and_1gw(_tokamak_model(), ARC_SPEC, [], P_NATIVE)
        assert len(cap.inputs) == 2
        for inp in cap.inputs:
            # The per-concept file contributes no financial values; the helper
            # passes none explicitly, so they ride the adapter/library defaults.
            assert inp.interest_rate == 0.07
            assert inp.inflation_rate == 0.02
            assert inp.construction_time_yr == 6.0
            # availability / lifetime_yr are passed but library-sourced.
            assert inp.availability == 0.85
            assert inp.lifetime_yr == 40.0
            assert inp.noak is True
            # Tokamak 1 GWe projection uses size_from_power=True (which solves
            # for geometry, so R0/plasma_t/B are stripped from overrides);
            # native call keeps n_mod=1 and pins the analyst's geometry.
            if inp.net_electric_mw == P_NATIVE:
                assert inp.n_mod == 1
                assert inp.overrides["R0"] == 3.3  # analyst geometry pinned
                assert inp.overrides.get("use_0d_model") is True
                assert "size_from_power" not in inp.overrides
            else:
                assert inp.net_electric_mw == 1000.0
                assert inp.n_mod == 1  # single bigger machine, not stacked
                assert inp.overrides.get("use_0d_model") is True
                assert inp.overrides.get("size_from_power") is True
                # Geometry the library back-solves must NOT be passed.
                for k in ("R0", "plasma_t", "B", "b_center"):
                    assert k not in inp.overrides

    def test_native_call_passes_overrides(self, monkeypatch):
        """The native forward is overrides-ON at the design point: it carries the
        enabled overrides and override_reference_mw=P_native (FR-3)."""
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        run_native_and_1gw(_tokamak_model(), ARC_SPEC, ARC_OVERRIDES, P_NATIVE)
        native = next(i for i in cap.inputs if i.net_electric_mw == P_NATIVE)
        assert native.override_reference_mw == P_NATIVE
        assert native.cost_overrides == {
            "C220103": 6901.0,
            "C220101": 348.0,
            "C220106": 123.0,
            "CAS27": 146.0,
        }

    def test_projection_passes_override_reference_mw(self, monkeypatch):
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        run_native_and_1gw(_tokamak_model(), ARC_SPEC, ARC_OVERRIDES, P_NATIVE)
        proj = next(i for i in cap.inputs if i.net_electric_mw == 1000.0)
        assert proj.override_reference_mw == P_NATIVE
        assert proj.cost_overrides == {
            "C220103": 6901.0,
            "C220101": 348.0,
            "C220106": 123.0,
            "CAS27": 146.0,
        }

    def test_availability_concept_sourced(self, monkeypatch):
        """availability comes from default_availability(model.concept), not a
        hardcoded literal — a MIRROR model gets 0.87, not 0.85."""
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)
        run_native_and_1gw(model, ARC_SPEC, [], P_NATIVE)
        expected = default_availability(ConfinementConcept.MIRROR)
        assert expected == 0.87  # guard: the library default we rely on
        for inp in cap.inputs:
            assert inp.availability == expected

    def test_lifetime_sourced_from_library_default(self, monkeypatch):
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        run_native_and_1gw(_tokamak_model(), ARC_SPEC, [], P_NATIVE)
        lib_default = CostingInput.model_fields["lifetime_yr"].default
        for inp in cap.inputs:
            assert inp.lifetime_yr == lib_default

    def test_mirror_uses_n_mod_stacking_not_size_from_power(self, monkeypatch):
        """Non-tokamak MFE concepts stay on the n_mod stacking projection until
        the library exposes 0D for them. Validates the family dispatch."""
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)
        run_native_and_1gw(model, dict(R0=2.0, plasma_t=0.5), [], P_NATIVE)
        proj = next(i for i in cap.inputs if i.net_electric_mw == 1000.0)
        assert proj.n_mod == round(1000.0 / P_NATIVE)
        assert "size_from_power" not in proj.overrides
        assert "use_0d_model" not in proj.overrides


# ---------------------------------------------------------------------------
# Invariant 3 — P_native == 1000 collapses native and projection.
# ---------------------------------------------------------------------------


class TestPNative1000Collapses:
    def test_n_mod_is_one(self, monkeypatch):
        cap = CaptureCosting()
        _patch_both_run_costing(monkeypatch, cap)
        run_native_and_1gw(_tokamak_model(), ARC_SPEC, [], 1000.0)
        proj = next(i for i in cap.inputs if i.net_electric_mw == 1000.0)
        assert proj.n_mod == 1

    def test_native_finite_at_1gw_pnative(self):
        """When P_native==1000, native and projection both target 1 GWe but
        take different sizing semantics: native pins the analyst's geometry
        (R0=3.3, B=9.2, etc. — ARC's design point), while the projection
        switches to size_from_power=True which back-solves a fresh geometry
        at 1 GWe. They may land at *different* machines, so the LCOE-equality
        invariant from the pre-0D era no longer holds. The invariant kept
        here is that both calls produce finite numbers (no crash, no nan)."""
        model = _tokamak_model()
        native, result_1gw = run_native_and_1gw(model, ARC_SPEC, [], 1000.0)
        assert native.costs.lcoe > 0
        assert result_1gw.costs.lcoe > 0


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
        generic = generic_reference(model, ARC_SPEC, P_NATIVE)
        native, result_1gw = run_native_and_1gw(
            model, ARC_SPEC, ARC_OVERRIDES, P_NATIVE
        )
        print_cas_breakdown(generic, native, result_1gw, ARC_OVERRIDES)
        out = capsys.readouterr().out
        # run_model greps this exact pattern from model_setup.py stdout.
        m = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", out)
        assert m, "print_cas_breakdown must emit a `LCOE: <n> $/MWh` line"
        assert float(m.group(1)) == pytest.approx(206.0, abs=0.5)
