"""Tests for exploration/concept_explorer/server.py.

Coverage:
- GET /api/health
- GET /api/manifest  (found)
- GET /api/concepts/{concept_id}  (found and 404)
- GET /api/parameter_index  (full index)
- GET /api/parameters/{param_name}  (found and 404)
- Page routes: /, /compare, /concept/{concept_id}  (found and 404)
- Startup failure when data/ is missing
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.models import (
    CASAccount,
    ConceptData,
    ConceptManifest,
    ConceptStatus,
    ConfinementFamily,
    Confidence,
    CostModelData,
    ParameterCategory,
    ParameterIndex,
    ParameterIndexEntry,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
    SourcePaths,
)
from exploration.concept_explorer.server import _load_data, create_app

# ---------------------------------------------------------------------------
# Helpers — minimal valid model instances
# ---------------------------------------------------------------------------


def _minimal_concept(concept_id: str = "01") -> ConceptData:
    """Return the smallest valid ConceptData that satisfies all Pydantic constraints."""
    return ConceptData(
        concept_id=concept_id,
        name="Test Tokamak",
        confinement_family=ConfinementFamily.MFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=False,
        has_sensitivities=False,
        sources=SourcePaths(),
    )


def _concept_with_sensitivities(concept_id: str = "01") -> ConceptData:
    """ConceptData carrying the sensitivities the API tests expect.

    The fixture intentionally produces a parameter_index that contains an
    "availability" entry — that is what the parameter-endpoint tests query.
    """
    zero_cas = CASAccount(name="zero", cost_m_usd=0.0)
    cas22_detail = {k: CASAccount(name=k, cost_m_usd=0.0) for k in CostModelData.CAS22_NAMES}
    cost_model = CostModelData(
        cas10=zero_cas, cas21=zero_cas, cas22=zero_cas, cas23=zero_cas,
        cas24=zero_cas, cas25=zero_cas, cas26=zero_cas, cas27=zero_cas,
        cas28=zero_cas, cas29=zero_cas, cas30=zero_cas, cas40=zero_cas,
        cas50=zero_cas, cas60=zero_cas, cas70=zero_cas, cas80=zero_cas,
        cas90=zero_cas,
        cas22_detail=cas22_detail,
        headline={  # type: ignore[arg-type]
            "lcoe_per_mwh": 75.0,
            "overnight_cost_per_kw": 5000.0,
            "p_net_mw": 1000.0,
            "q_eng": 8.0,
            "capacity_factor": 0.85,
        },
        sensitivities=SensitivityAnalysis(
            engineering={
                "availability": SensitivityEntry(elasticity=0.85, baseline=0.85),
            },
            financial={},
        ),
    )
    return ConceptData(
        concept_id=concept_id,
        name="Test Tokamak",
        confinement_family=ConfinementFamily.MFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=True,
        has_sensitivities=True,
        cost_model=cost_model,
        parameter_metadata={
            "availability": ParameterMetadata(
                display_name="Plant Availability",
                category=ParameterCategory.SHARED_BASELINE,
                confidence=Confidence.MEDIUM,
                baseline=0.85,
                range=(0.5, 0.95),
            ),
        },
        sources=SourcePaths(),
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def base_dir(tmp_path: Path) -> Path:
    """Minimal base_dir with data/ populated (no templates → no dist/ rendering).

    The server computes the manifest and parameter index at startup from the
    per-concept JSON files, so we only need to write those.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    concept = _concept_with_sensitivities("01")
    (data_dir / "01.json").write_text(concept.model_dump_json())

    return tmp_path


@pytest.fixture
def base_dir_with_pages(base_dir: Path) -> Path:
    """Extends base_dir with pre-built dist/ files to test page-serving routes.

    Templates for index/compare/concept pages are written in Tasks 10–12.
    We create the dist files directly here so the page routes are testable
    without the full template pipeline being complete.
    """
    dist_dir = base_dir / "dist"
    dist_dir.mkdir()
    (dist_dir / "index.html").write_text("<html>index</html>")
    (dist_dir / "compare.html").write_text("<html>compare</html>")
    concept_dir = dist_dir / "concept"
    concept_dir.mkdir()
    (concept_dir / "01.html").write_text("<html>concept 01</html>")
    return base_dir


@pytest.fixture
def client(base_dir: Path) -> Generator[TestClient, None, None]:
    """TestClient backed by a data-only base_dir (no dist pages)."""
    app = create_app(base_dir=base_dir)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client_with_pages(base_dir_with_pages: Path) -> Generator[TestClient, None, None]:
    """TestClient backed by a base_dir that includes pre-built dist/ pages."""
    app = create_app(base_dir=base_dir_with_pages)
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def test_health(client: TestClient) -> None:
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


def test_manifest_returns_200(client: TestClient) -> None:
    resp = client.get("/api/manifest")
    assert resp.status_code == 200


def test_manifest_validates_as_concept_manifest(client: TestClient) -> None:
    resp = client.get("/api/manifest")
    # Pydantic validation would raise if the shape is wrong
    manifest = ConceptManifest.model_validate(resp.json())
    assert len(manifest.concepts) == 1
    assert manifest.concepts[0].concept_id == "01"


# ---------------------------------------------------------------------------
# Concepts — found
# ---------------------------------------------------------------------------


def test_concept_found_returns_200(client: TestClient) -> None:
    resp = client.get("/api/concepts/01")
    assert resp.status_code == 200


def test_concept_found_validates_as_concept_data(client: TestClient) -> None:
    resp = client.get("/api/concepts/01")
    data = ConceptData.model_validate(resp.json())
    assert data.concept_id == "01"
    assert data.name == "Test Tokamak"


def test_concept_cache_hit_returns_same_data(client: TestClient) -> None:
    """Repeated requests must return identical data (LRU cache must not corrupt)."""
    r1 = client.get("/api/concepts/01").json()
    r2 = client.get("/api/concepts/01").json()
    assert r1 == r2


# ---------------------------------------------------------------------------
# Concepts — not found
# ---------------------------------------------------------------------------


def test_concept_not_found_returns_404(client: TestClient) -> None:
    resp = client.get("/api/concepts/nonexistent")
    assert resp.status_code == 404


def test_concept_not_found_detail_message(client: TestClient) -> None:
    resp = client.get("/api/concepts/nonexistent")
    # FastAPI detail format: {"detail": "..."}
    assert resp.json()["detail"] == "Concept nonexistent not found"


# ---------------------------------------------------------------------------
# Parameter index — full index endpoint
# ---------------------------------------------------------------------------


def test_parameter_index_returns_200(client: TestClient) -> None:
    resp = client.get("/api/parameter_index")
    assert resp.status_code == 200


def test_parameter_index_validates_as_parameter_index(client: TestClient) -> None:
    resp = client.get("/api/parameter_index")
    index = ParameterIndex.model_validate(resp.json())
    # Fixture concept has an "availability" sensitivity → server-computed
    # parameter_index includes it.
    assert "availability" in index.parameters


# ---------------------------------------------------------------------------
# Parameters — found
# ---------------------------------------------------------------------------


def test_parameter_found_returns_200(client: TestClient) -> None:
    resp = client.get("/api/parameters/availability")
    assert resp.status_code == 200


def test_parameter_found_validates_as_parameter_index_entry(client: TestClient) -> None:
    resp = client.get("/api/parameters/availability")
    entry = ParameterIndexEntry.model_validate(resp.json())
    assert entry.param_name == "availability"


# ---------------------------------------------------------------------------
# Parameters — not found
# ---------------------------------------------------------------------------


def test_parameter_not_found_returns_404(client: TestClient) -> None:
    resp = client.get("/api/parameters/does_not_exist")
    assert resp.status_code == 404


def test_parameter_not_found_detail_message(client: TestClient) -> None:
    resp = client.get("/api/parameters/does_not_exist")
    assert resp.json()["detail"] == "Parameter does_not_exist not found"


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------


def test_index_page_returns_200(client_with_pages: TestClient) -> None:
    resp = client_with_pages.get("/")
    assert resp.status_code == 200
    assert "index" in resp.text


def test_compare_page_returns_200(client_with_pages: TestClient) -> None:
    resp = client_with_pages.get("/compare")
    assert resp.status_code == 200
    assert "compare" in resp.text


def test_concept_page_returns_200(client_with_pages: TestClient) -> None:
    resp = client_with_pages.get("/concept/01")
    assert resp.status_code == 200
    assert "concept 01" in resp.text


def test_concept_page_not_found_returns_404(client_with_pages: TestClient) -> None:
    # No dist file for concept_id "99"
    resp = client_with_pages.get("/concept/99")
    assert resp.status_code == 404


def test_index_page_not_found_when_no_dist(client: TestClient) -> None:
    """Without dist/ files (templates not rendered), / returns 404."""
    resp = client.get("/")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Startup failure — data/ missing
# ---------------------------------------------------------------------------


def test_startup_fails_when_data_dir_missing(tmp_path: Path) -> None:
    """Server must abort with a clear RuntimeError if data/ does not exist.

    data/ is created by extract_explorer_data.py; an empty base_dir means the
    operator skipped that step. Failing loudly here prevents silent bad state.
    """
    app = create_app(base_dir=tmp_path)  # tmp_path has no data/ subdirectory
    with pytest.raises(RuntimeError, match="data/ directory not found"):
        with TestClient(app):
            pass  # startup runs lifespan; RuntimeError propagates here


def test_startup_fails_when_data_dir_empty(tmp_path: Path) -> None:
    """Server must abort if data/ exists but contains no concept files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    app = create_app(base_dir=tmp_path)
    with pytest.raises(RuntimeError, match="No concept data files found"):
        with TestClient(app):
            pass


# ---------------------------------------------------------------------------
# AC-1: server starts with only per-concept JSONs (no manifest.json files)
# ---------------------------------------------------------------------------


def test_load_data_without_manifest_files(tmp_path: Path) -> None:
    """Server computes manifest/parameter_index from per-concept JSONs alone."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    concept = _minimal_concept("01")
    (data_dir / "01.json").write_text(concept.model_dump_json())

    concepts, manifest, param_index = _load_data(data_dir)

    assert set(concepts.keys()) == {"01"}
    assert len(manifest.concepts) == 1
    assert manifest.concepts[0].concept_id == "01"
    # No sensitivities in minimal concept → empty parameter index
    assert param_index.parameters == {}


def test_load_data_ignores_stale_manifest_files(tmp_path: Path) -> None:
    """Stale manifest.json/parameter_index.json on disk must not break startup."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    concept = _minimal_concept("01")
    (data_dir / "01.json").write_text(concept.model_dump_json())
    # Pre-existing legacy files — should be ignored, not parsed as concepts
    (data_dir / "manifest.json").write_text('{"this_is": "stale_garbage"}')
    (data_dir / "parameter_index.json").write_text('{"this_is": "stale_garbage"}')

    concepts, manifest, _ = _load_data(data_dir)

    assert set(concepts.keys()) == {"01"}
    assert len(manifest.concepts) == 1
