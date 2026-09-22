"""Synthetic route admission checks; never execute a plant model."""
from types import SimpleNamespace

import pytest

from exploration.aries_integrated.studies import study_route as route


@pytest.fixture
def declared(monkeypatch):
    document = {"entry_keys": {"a": "entry", "b": "entry"},
                "channels": {"published": "result"},
                "constraints": {"constraint-id": "check"}}
    monkeypatch.setattr(route, "interface", lambda: document)
    return document


def test_complete_proposals_only(declared):
    assert route.validate_proposal({"a": 1, "b": 2}) == {"a": 1.0, "b": 2.0}
    for point in ({"a": 1}, {"a": 1, "b": 2, "c": 3},
                  {"a": True, "b": 2}, {"a": float("nan"), "b": 2}):
        assert route.validate_proposal(point) is None


@pytest.mark.parametrize("outputs", [{}, {"result": None}, {"result": "1"}, {"result": True}])
def test_missing_or_nonnumeric_publications_refuse(outputs):
    with pytest.raises(route.RouteError):
        route.require_published(SimpleNamespace(outputs=outputs), {"published": "result"})


def test_nonfinite_evidence_is_retained():
    route.require_published(SimpleNamespace(outputs={"result": float("nan")}),
                            {"published": "result"})


def test_exact_constraint_identity(declared, monkeypatch):
    monkeypatch.setattr(route, "_catalog_by_constraint_id", lambda _: {
        "constraint-id": {"source_local_identity": "different"}})
    with pytest.raises(route.RouteError):
        route._export_catalog(route.PACKAGE_DIR)


def test_missing_interface_refuses(tmp_path, monkeypatch):
    monkeypatch.setattr(route, "INTERFACE_MODULE", "nonexistent_aries_study_interface")
    with pytest.raises(route.RouteError):
        route.interface()


def test_reused_local_names_retain_exact_ids():
    catalog = {cid: {"source_local_identity": "capacity_ok"} for cid in ("one", "two")}
    case = SimpleNamespace(verdicts={"one": "satisfied", "two": "violated"})
    assert route._short_verdicts(case, catalog) == case.verdicts
