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
)
from exploration.concept_explorer.server import create_app

# Path to seeded taxonomy JSON files
_DATA_DIR = Path(__file__).parent.parent / "data"


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
    assert data["root"]["field"] == "confinement_family"


# ---------------------------------------------------------------------------
# Registry endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_registry_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/registry")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["concepts"]) == 38


# ---------------------------------------------------------------------------
# Single concept endpoint
# ---------------------------------------------------------------------------


def test_taxonomy_concept_endpoint(client: TestClient):
    resp = client.get("/api/taxonomy/concepts/01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "HTS Compact Tokamak"
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
    assert len(data["points"]) == 38
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
