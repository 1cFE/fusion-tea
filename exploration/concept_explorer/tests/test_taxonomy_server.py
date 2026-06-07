"""Tests for taxonomy API endpoints and page route.

Coverage:
- GET /api/taxonomy/tree
- GET /api/taxonomy/registry
- GET /api/taxonomy/concepts/{concept_id} (found and 404)
- GET /api/taxonomy/similarity/{concept_id} (found and 404)
- GET /api/taxonomy/compare/{concept_a}/{concept_b} (found and 404)
- GET /api/taxonomy/constellation
- GET /taxonomy (page route)
- Regression: existing endpoints still work
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.models import (
    ConceptData,
    ConceptStatus,
    ConfinementFamily,
    SourcePaths,
    load_omit_list,
)
from exploration.concept_explorer.server import _load_taxonomy, create_app

# Path to seeded taxonomy JSON files
_DATA_DIR = Path(__file__).parent.parent / "data"

# The omit list is applied at server startup (lifespan -> _load_taxonomy), so the
# `client` fixture below — which seeds the real registry/tree — serves the omitted
# concepts excluded. Derive the post-omit count from the source files rather than
# hard-coding it, so the assertions track the shipped omit_list.yaml.
_OMITTED = load_omit_list()
_FULL_REGISTRY_IDS = {
    c["concept_id"]
    for c in json.loads((_DATA_DIR / "concept_registry.json").read_text())["concepts"]
}
_OMITTED_IN_REGISTRY = _OMITTED & _FULL_REGISTRY_IDS
_EXPECTED_REGISTRY_COUNT = len(_FULL_REGISTRY_IDS) - len(_OMITTED_IN_REGISTRY)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_concept(concept_id: str = "01") -> ConceptData:
    return ConceptData(
        concept_id=concept_id,
        name="Test Tokamak",
        confinement_family=ConfinementFamily.MFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=False,
        has_sensitivities=False,
        sources=SourcePaths(),
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def base_dir(tmp_path: Path) -> Path:
    """Minimal base_dir with cost model data + taxonomy JSON files.

    The server computes the manifest and parameter index from the per-concept
    JSON files at startup, so we only seed those (plus taxonomy seeds).
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Existing cost model data
    concept = _minimal_concept("01")
    (data_dir / "01.json").write_text(concept.model_dump_json())

    # Copy taxonomy JSON files from seeded data
    shutil.copy(_DATA_DIR / "concept_registry.json", data_dir / "concept_registry.json")
    shutil.copy(_DATA_DIR / "decision_tree.json", data_dir / "decision_tree.json")

    return tmp_path


@pytest.fixture
def base_dir_with_pages(base_dir: Path) -> Path:
    """Extends base_dir with pre-built dist/ files for page routes."""
    dist_dir = base_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / "taxonomy.html").write_text("<html>taxonomy</html>")
    return base_dir


@pytest.fixture
def client(base_dir: Path) -> Generator[TestClient, None, None]:
    app = create_app(base_dir=base_dir)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client_with_pages(base_dir_with_pages: Path) -> Generator[TestClient, None, None]:
    app = create_app(base_dir=base_dir_with_pages)
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Tree endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_tree_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/tree")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == "1.0"
    assert "root" in data
    assert data["root"]["field"] == "tree_group"


# ---------------------------------------------------------------------------
# Registry endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_registry_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/registry")
    assert resp.status_code == 200
    data = resp.json()
    # Omitted concepts (FR-5) are filtered at startup, so the count is the full
    # registry minus the omitted IDs that were present in it.
    assert len(data["concepts"]) == _EXPECTED_REGISTRY_COUNT
    returned_ids = {c["concept_id"] for c in data["concepts"]}
    assert returned_ids.isdisjoint(_OMITTED)


# ---------------------------------------------------------------------------
# Single concept endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_concept_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/concepts/01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"].startswith("HTS Compact Tokamak")
    assert data["confinement_family"] == "MFE"


def test_taxonomy_concept_404(client: TestClient):
    resp = client.get("/api/taxonomy/concepts/nonexistent")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Similarity endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_similarity_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/similarity/01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["query_concept_id"] == "01"
    assert len(data["nearest"]) > 0


def test_taxonomy_similarity_404(client: TestClient):
    resp = client.get("/api/taxonomy/similarity/nonexistent")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Compare endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_compare_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/compare/01/09")
    assert resp.status_code == 200
    data = resp.json()
    assert "comparison" in data
    assert data["concept_id"] == "09"


def test_taxonomy_compare_404(client: TestClient):
    resp = client.get("/api/taxonomy/compare/01/nonexistent")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Constellation endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_constellation_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/constellation")
    assert resp.status_code == 200
    data = resp.json()
    # Constellation is computed from the omit-filtered registry (I-5), so the
    # point count matches the post-omit registry count.
    assert len(data["points"]) == _EXPECTED_REGISTRY_COUNT
    assert "variance_explained" in data


# ---------------------------------------------------------------------------
# Page route
# ---------------------------------------------------------------------------


def test_taxonomy_page_route(client_with_pages: TestClient):
    resp = client_with_pages.get("/taxonomy")
    assert resp.status_code == 200


def test_taxonomy_page_404_without_dist(client: TestClient):
    resp = client.get("/taxonomy")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Regression: existing endpoints still work
# ---------------------------------------------------------------------------


def test_existing_endpoints_still_work(client: TestClient):
    """Existing API endpoints are unaffected by taxonomy additions."""
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/manifest").status_code == 200


# ---------------------------------------------------------------------------
# Omit list enforcement (Consumer #2B: taxonomy) — FR-5, FR-6, I-3, I-5, I-6
# ---------------------------------------------------------------------------


def _collect_tree_concept_ids(node: dict, acc: set[str]) -> None:
    """Recursively gather every concept ID referenced in a decision-tree node."""
    acc.update(node.get("concepts", []))
    for child in node.get("children", []):
        _collect_tree_concept_ids(child, acc)


def test_taxonomy_tree_excludes_omitted(client: TestClient):
    """FR-5: omitted IDs are pruned from the decision tree."""
    resp = client.get("/api/taxonomy/tree")
    assert resp.status_code == 200
    tree_ids: set[str] = set()
    _collect_tree_concept_ids(resp.json()["root"], tree_ids)
    assert tree_ids.isdisjoint(_OMITTED)


def test_taxonomy_constellation_excludes_omitted(client: TestClient):
    """FR-5/I-5: omitted IDs do not appear as constellation points."""
    resp = client.get("/api/taxonomy/constellation")
    assert resp.status_code == 200
    point_ids = {p["concept_id"] for p in resp.json()["points"]}
    assert point_ids.isdisjoint(_OMITTED)


def test_taxonomy_similarity_omits_from_neighbors(client: TestClient):
    """FR-5/I-5: omitted IDs never surface as a nearest-neighbor of a kept concept."""
    resp = client.get("/api/taxonomy/similarity/01")
    assert resp.status_code == 200
    neighbor_ids = {n["concept_id"] for n in resp.json()["nearest"]}
    assert neighbor_ids.isdisjoint(_OMITTED)


def test_taxonomy_similarity_404_for_omitted(client: TestClient):
    """An omitted concept is gone from the registry, so its similarity 404s.

    26 is present in the seeded registry but is in the omit list, so after the
    startup filter the endpoint must not find it.
    """
    assert "26" in _OMITTED_IN_REGISTRY  # guard: this ID is a meaningful case
    resp = client.get("/api/taxonomy/similarity/26")
    assert resp.status_code == 404


def test_load_taxonomy_explicit_omit_filters_all_surfaces():
    """FR-6/I-3/I-5/I-6: with an explicit omit set, _load_taxonomy excludes the ID
    from registry, tree, similarity reports, and constellation — reading the real
    on-disk files without modifying them."""
    registry, tree, reports, constellation = _load_taxonomy(_DATA_DIR, omitted={"27"})

    assert registry is not None and tree is not None and constellation is not None
    assert all(c.concept_id != "27" for c in registry.concepts)

    tree_ids: set[str] = set()
    _collect_tree_concept_ids(tree["root"], tree_ids)
    assert "27" not in tree_ids

    assert "27" not in reports
    for report in reports.values():
        assert all(n.concept_id != "27" for n in report.nearest)

    assert all(p.concept_id != "27" for p in constellation.points)

    # I-6: the source taxonomy files are read-filtered only, never deleted/modified.
    assert (_DATA_DIR / "concept_registry.json").exists()
    assert (_DATA_DIR / "decision_tree.json").exists()


def test_load_taxonomy_empty_omit_keeps_full_registry():
    """FR-8: an explicit empty omit set yields the full, unfiltered registry."""
    registry, _, _, _ = _load_taxonomy(_DATA_DIR, omitted=set())
    assert registry is not None
    assert len(registry.concepts) == len(_FULL_REGISTRY_IDS)
