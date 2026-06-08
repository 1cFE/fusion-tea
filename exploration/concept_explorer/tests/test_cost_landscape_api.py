"""Cost-landscape aggregate + endpoint (Theme F, Phase 2).

Covers ``build_cost_landscape`` and the ``/api/cost-landscape`` route:

- The account→component roll-up is *total* (I6): every override lands on exactly
  one of {capital, fixed_om, replacement, fuel}, and an unknown account fails
  loudly rather than being silently bucketed.
- The aggregate is correct against the real served data (LCOE matches the
  manifest, only costed concepts appear, concept 01 carries its magnet override).
- Honest degradation: the O&M split is None on the current (pre-re-extract) data
  while om_combined is always present; a missing rationale stays None.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.models import (
    CostComponent,
    OverrideRecord,
    build_cost_landscape,
    _override_component,
    _override_rationale_short,
)
from exploration.concept_explorer.server import BASE_DIR, _load_data, create_app
from exploration.concept_explorer.tests.test_models import (
    _make_concept,
    _make_cost_model,
)

_COMPONENT_VALUES = {c.value for c in CostComponent}


# ---------------------------------------------------------------------------
# Fixtures — the real served data
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def served_concepts() -> list:
    """All served concepts (default omit list applied), unstamped."""
    concepts, _, _ = _load_data(BASE_DIR / "data")
    return list(concepts.values())


@pytest.fixture(scope="module")
def real_client() -> Generator[TestClient, None, None]:
    app = create_app(base_dir=BASE_DIR)
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Roll-up totality (I6) against real data
# ---------------------------------------------------------------------------


def test_rollup_is_total_and_components_present(served_concepts: list) -> None:
    """Every entry exposes all four segments and every override lands on one."""
    landscape = build_cost_landscape(served_concepts)
    assert landscape.concepts, "expected at least one costed concept"

    for entry in landscape.concepts:
        comp = entry.components
        # The four additive segments + the always-present combined-O&M source.
        assert comp.capital is not None
        assert comp.fuel is not None
        assert comp.om_combined is not None
        for override in entry.overrides:
            assert override.component.value in _COMPONENT_VALUES


def test_only_costed_concepts_with_finite_lcoe_appear(served_concepts: list) -> None:
    """The aggregate holds exactly the costed concepts (I5)."""
    landscape = build_cost_landscape(served_concepts)
    landscape_ids = {e.concept_id for e in landscape.concepts}
    costed_ids = {
        c.concept_id
        for c in served_concepts
        if c.cost_model is not None
    }
    assert landscape_ids == costed_ids


def test_entry_lcoe_matches_headline(served_concepts: list) -> None:
    """Each entry's LCOE is the concept's stored headline (the bar height)."""
    by_id = {c.concept_id: c for c in served_concepts}
    for entry in build_cost_landscape(served_concepts).concepts:
        headline = by_id[entry.concept_id].cost_model.headline.lcoe_per_mwh
        assert entry.lcoe == pytest.approx(headline, rel=1e-12)


def test_concept_01_has_capital_override_on_magnets(served_concepts: list) -> None:
    """Concept 01's authored C220103 (magnets) override rolls up to capital."""
    landscape = build_cost_landscape(served_concepts)
    entry = next(e for e in landscape.concepts if e.concept_id == "01")
    magnets = [ov for ov in entry.overrides if ov.account == "C220103"]
    assert magnets, "concept 01 should carry a C220103 override"
    assert all(ov.component is CostComponent.CAPITAL for ov in magnets)


def test_served_split_absent_but_om_combined_present(served_concepts: list) -> None:
    """Pre-re-extract: the 71/72 split is None, the combined O&M is present.

    This is the honest-degradation state the front-end renders as a single
    combined-O&M segment until the re-extract lands the split.
    """
    landscape = build_cost_landscape(served_concepts)
    entry = next(e for e in landscape.concepts if e.concept_id == "01")
    assert entry.components.fixed_om is None
    assert entry.components.replacement is None
    assert entry.components.om_combined > 0


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------


def test_endpoint_serves_shaped_landscape(real_client: TestClient) -> None:
    resp = real_client.get("/api/cost-landscape")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "generated_at" in body
    assert body["concepts"], "expected costed concepts in the payload"

    row = next(r for r in body["concepts"] if r["concept_id"] == "01")
    assert {"capital", "fixed_om", "replacement", "fuel", "om_combined"} <= set(
        row["components"]
    )
    assert row["lcoe"] > 0
    for ov in row["overrides"]:
        assert ov["component"] in _COMPONENT_VALUES


# ---------------------------------------------------------------------------
# Roll-up map — unit (incl. the CAS70 decision and fail-loud)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("account", "expected"),
    [
        ("CAS70", CostComponent.FIXED_OM),  # combined O&M → fixed_om (settled)
        ("CAS71", CostComponent.FIXED_OM),
        ("CAS72", CostComponent.REPLACEMENT),
        ("CAS80", CostComponent.FUEL),
        ("C220103", CostComponent.CAPITAL),  # CAS22 sub-account
        ("C220108", CostComponent.CAPITAL),
        ("CAS27", CostComponent.CAPITAL),  # top-level capital account
        ("CAS21", CostComponent.CAPITAL),
        ("cas80", CostComponent.FUEL),  # case-insensitive
    ],
)
def test_override_component_map(account: str, expected: CostComponent) -> None:
    assert _override_component(account) is expected


def test_override_component_unknown_account_raises() -> None:
    """An account outside the vocabulary fails loudly (no silent bucket)."""
    with pytest.raises(ValueError, match="no LCOE-component mapping"):
        _override_component("CAS99")


def test_rationale_short_prefers_first_sentence() -> None:
    ov = _make_override(rationale="First claim here. Second sentence with detail.")
    assert _override_rationale_short(ov) == "First claim here."


def test_rationale_short_skips_abbreviation_boundaries() -> None:
    """'et al.' is not a sentence end — the first sentence runs past it."""
    ov = _make_override(
        rationale="Sorbom et al. 2015 reports a fabricated magnet cost. Next sentence."
    )
    assert (
        _override_rationale_short(ov)
        == "Sorbom et al. 2015 reports a fabricated magnet cost."
    )


def test_rationale_short_falls_back_to_structured_basis() -> None:
    ov = _make_override(rationale=None, cost_basis="noak", provenance="direct")
    assert _override_rationale_short(ov) == "noak · direct"


def test_rationale_short_none_when_nothing_recorded() -> None:
    ov = _make_override(rationale=None, cost_basis=None, provenance=None)
    assert _override_rationale_short(ov) is None


# ---------------------------------------------------------------------------
# build_cost_landscape — unit, on a synthetic concept with overrides
# ---------------------------------------------------------------------------


def test_build_projects_overrides_onto_segments() -> None:
    concept = _make_concept(cost_model=_make_cost_model())
    concept.overrides = [
        _make_override(account="C220103", rationale="Magnet cost from vendor quote."),
        _make_override(account="CAS70", rationale=None, cost_basis="noak", provenance=None),
        _make_override(account="CAS80", enabled=False, blocked_by="org/repo#7"),
    ]

    landscape = build_cost_landscape([concept])
    assert len(landscape.concepts) == 1
    overrides = {ov.account: ov for ov in landscape.concepts[0].overrides}

    assert overrides["C220103"].component is CostComponent.CAPITAL
    assert overrides["C220103"].rationale_short == "Magnet cost from vendor quote."
    assert overrides["CAS70"].component is CostComponent.FIXED_OM
    assert overrides["CAS70"].rationale_short == "noak"
    assert overrides["CAS80"].component is CostComponent.FUEL
    assert overrides["CAS80"].enabled is False
    assert overrides["CAS80"].blocked_by == "org/repo#7"


def test_build_skips_concepts_without_cost_model() -> None:
    costed = _make_concept(cost_model=_make_cost_model())
    uncosted = _make_concept(cost_model=None)
    uncosted.concept_id = "99"

    landscape = build_cost_landscape([costed, uncosted])
    assert {e.concept_id for e in landscape.concepts} == {costed.concept_id}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_override(
    *,
    account: str = "C220103",
    rationale: str | None = "A rationale.",
    source: str | None = "a-source.md",
    cost_basis: str | None = "noak",
    provenance: str | None = "direct",
    enabled: bool = True,
    blocked_by: str | None = None,
) -> OverrideRecord:
    return OverrideRecord(
        account=account,
        account_name=account,
        value=1.0,
        enabled=enabled,
        provenance=provenance,
        source=source,
        rationale=rationale,
        cost_basis=cost_basis,
        blocked_by=blocked_by,
    )
