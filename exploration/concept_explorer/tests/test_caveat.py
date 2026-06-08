"""Tests for the honest-caveat device (Theme A / A3, Phase 3).

Backend: archetype-fit grade loads from tables/archetype_fit.csv and is stamped
onto served ConceptData + the manifest, preserving the recorded-"None" vs
absent (not-recorded) distinction.

Frontend (static-text guards, no browser): the ⚠ marker markup is authored in
exactly one place (caveat_marker.js); the ~5 former sites delegate to it;
templates load it. Behavioral correctness of caveatMarker() is verified live
via browser-inspect.
"""

from __future__ import annotations

import re
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.server import BASE_DIR, _load_fit_grades, create_app

_FIT_CSV = BASE_DIR.parent / "concept_analysis" / "tables" / "archetype_fit.csv"
_JS_DIR = BASE_DIR / "static" / "js"
_TEMPLATES_DIR = BASE_DIR / "templates"

# The former marker sites that now delegate to caveatMarker().
_CAVEAT_SITES = [
    "index_page.js",
    "concept_page.js",
    "taxonomy_card.js",
    "comparison.js",
    "neighborhood_graph.js",
]
_TEMPLATES = ["index.html.j2", "concept.html.j2", "compare.html.j2", "taxonomy.html.j2"]


# ---------------------------------------------------------------------------
# Backend — archetype-fit grade loading + overlay
# ---------------------------------------------------------------------------


def test_load_fit_grades_parses_and_maps_short_codes():
    grades = _load_fit_grades(_FIT_CSV)
    assert grades["01"] == "High"
    assert grades["24"] == "Low"
    assert grades["02"] == "None"  # recorded "None" grade, not absent
    # Suffix variants keep their letter (code = token before first hyphen).
    assert "17a" in grades and "20b" in grades


def test_load_fit_grades_missing_file_returns_empty(tmp_path: Path):
    assert _load_fit_grades(tmp_path / "nope.csv") == {}


@pytest.fixture(scope="module")
def real_client() -> Generator[TestClient, None, None]:
    app = create_app(base_dir=BASE_DIR)
    with TestClient(app) as c:
        yield c


@pytest.mark.parametrize(
    ("cid", "expected"),
    [("01", "High"), ("24", "Low"), ("02", "None"), ("35", "None")],
)
def test_fit_grade_in_overlay(real_client: TestClient, cid: str, expected: str):
    payload = real_client.get(f"/api/concepts/{cid}").json()
    assert payload["fit_grade"] == expected
    assert payload["fit_grade"] in {"High", "Med", "Low", "None", None}


def test_manifest_carries_fit_grade(real_client: TestClient):
    by_id = {e["concept_id"]: e for e in real_client.get("/api/manifest").json()["concepts"]}
    assert by_id["01"]["fit_grade"] == "High"
    assert by_id["02"]["fit_grade"] == "None"


# ---------------------------------------------------------------------------
# Frontend — single authorship + delegation + template wiring
# ---------------------------------------------------------------------------


def test_caveat_helper_exists_and_exports_global():
    text = (_JS_DIR / "caveat_marker.js").read_text()
    assert "window.caveatMarker" in text
    # Covers all three caveat dimensions (FR-A3.2).
    assert "single-source" in text  # asterisk / low-grounding
    assert "Archetype fit" in text  # fit-None
    assert "not recorded" in text  # honest absence (FR-A3.3)
    assert 'fitGrade === "None"' in text


def test_marker_markup_authored_only_in_caveat_marker():
    """The ⚠ glyph and marker classes appear in exactly one JS file."""
    glyph = "⚠"
    offenders = []
    for path in _JS_DIR.glob("*.js"):
        if path.name == "caveat_marker.js":
            continue
        text = path.read_text()
        if glyph in text or "caveat-marker" in text or "low-grounding-marker" in text:
            offenders.append(path.name)
    assert not offenders, f"marker markup leaked into: {offenders}"


@pytest.mark.parametrize("fname", _CAVEAT_SITES)
def test_site_delegates_to_caveat_marker(fname: str):
    text = (_JS_DIR / fname).read_text()
    assert "caveatMarker(" in text, f"{fname} does not delegate to caveatMarker()"


@pytest.mark.parametrize("template", _TEMPLATES)
def test_template_loads_caveat_helper_first(template: str):
    text = (_TEMPLATES_DIR / template).read_text()
    helper = "/static/js/caveat_marker.js"
    assert helper in text, f"{template} does not load {helper}"
    helper_pos = text.index(helper)
    for site in _CAVEAT_SITES:
        ref = f"/static/js/{site}"
        if ref in text:
            assert text.index(ref) > helper_pos, (
                f"{template}: {site} loads before caveat_marker.js"
            )
