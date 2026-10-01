"""CORS for the public site and protected preview, with API behavior preserved.

The existing fake costing model exercises the real compute route without the
modeling toolchain. CORS controls browser access, not access to this public API.
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

import exploration.concept_explorer.server as server_module
from exploration.concept_explorer.server import create_app
from exploration.concept_explorer.tests import test_state_and_compute as compute_tests

# Reuse the existing isolated model fixture through pytest's fixture discovery.
costingfe_base_dir = compute_tests.costingfe_base_dir

ALLOWED_ORIGINS = ("https://1cf.energy", "https://static.1cf.energy")
DENIED_ORIGINS = (
    "https://example.com",
    "http://1cf.energy",
    "https://www.1cf.energy",
    "https://other.1cf.energy",
    "https://1cf.energy.example.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "null",
)


@pytest.fixture
def cors_client(
    costingfe_base_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("EXPLORER_SKIP_WARMUP", "1")
    app = create_app(base_dir=costingfe_base_dir)
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_allowed_get_preserves_response(cors_client: TestClient, origin: str) -> None:
    original = cors_client.get("/api/manifest")
    response = cors_client.get("/api/manifest", headers={"Origin": origin})
    assert response.status_code == original.status_code == 200
    assert response.content == original.content
    assert response.headers["access-control-allow-origin"] == origin
    assert "Origin" in response.headers["vary"]
    assert "access-control-allow-credentials" not in response.headers
    assert "access-control-allow-origin" not in original.headers


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_compute_preflight(cors_client: TestClient, origin: str) -> None:
    response = cors_client.options(
        "/api/compute",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert response.headers["access-control-allow-methods"] == "GET, POST"
    # Starlette always includes the browser's CORS-safelisted headers.
    assert set(response.headers["access-control-allow-headers"].split(", ")) == {
        "Accept", "Accept-Language", "Content-Language", "Content-Type",
    }
    assert "access-control-allow-credentials" not in response.headers


@pytest.mark.parametrize("origin", DENIED_ORIGINS)
def test_unapproved_origins_cannot_read_api(cors_client: TestClient, origin: str) -> None:
    response = cors_client.get("/api/manifest", headers={"Origin": origin})
    assert response.status_code == 200  # The API remains public.
    assert "access-control-allow-origin" not in response.headers
    preflight = cors_client.options(
        "/api/compute",
        headers={"Origin": origin, "Access-Control-Request-Method": "POST"},
    )
    assert preflight.status_code == 400
    assert "access-control-allow-origin" not in preflight.headers


@pytest.mark.parametrize("method", ("PUT", "PATCH", "DELETE"))
def test_unapproved_methods_fail_preflight(cors_client: TestClient, method: str) -> None:
    response = cors_client.options(
        "/api/compute",
        headers={
            "Origin": ALLOWED_ORIGINS[0],
            "Access-Control-Request-Method": method,
        },
    )
    assert response.status_code == 400
    assert response.headers["access-control-allow-methods"] == "GET, POST"


@pytest.mark.parametrize("header", ("Authorization", "X-Requested-With", "Content-Type, X-Token"))
def test_unapproved_headers_fail_preflight(cors_client: TestClient, header: str) -> None:
    response = cors_client.options(
        "/api/compute",
        headers={
            "Origin": ALLOWED_ORIGINS[0],
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": header,
        },
    )
    assert response.status_code == 400
    assert "Disallowed CORS headers" in response.text


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_cross_origin_compute_matches_same_origin(cors_client: TestClient, origin: str) -> None:
    for overrides in ({}, {"availability": 0.5}):
        body = {"concept_id": "04", "overrides": overrides}
        original = cors_client.post("/api/compute", json=body)
        response = cors_client.post("/api/compute", json=body, headers={"Origin": origin})
        assert response.status_code == original.status_code == 200
        assert response.content == original.content
        assert response.headers["access-control-allow-origin"] == origin
        assert "access-control-allow-origin" not in original.headers


def test_cross_origin_state_round_trip(cors_client: TestClient) -> None:
    response = cors_client.post(
        "/api/state", json={"comparison_set": ["01", "04"]},
        headers={"Origin": ALLOWED_ORIGINS[0]},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGINS[0]
    assert cors_client.get("/api/state").json()["comparison_set"] == ["01", "04"]


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_api_errors_remain_readable(cors_client: TestClient, origin: str) -> None:
    headers = {"Origin": origin}
    responses = (
        (cors_client.get("/api/concepts/missing", headers=headers), 404),
        (cors_client.post("/api/compute", json={}, headers=headers), 422),
        (cors_client.post(
            "/api/compute", json={"concept_id": "01", "overrides": {}}, headers=headers,
        ), 422),
    )
    for response, expected_status in responses:
        assert response.status_code == expected_status
        assert response.json()["detail"]
        assert response.headers["access-control-allow-origin"] == origin


@pytest.mark.parametrize("origin", (*ALLOWED_ORIGINS, "https://example.com"))
def test_uncaught_compute_error_obeys_cors(
    cors_client: TestClient, monkeypatch: pytest.MonkeyPatch, origin: str,
) -> None:
    def fail_model_load(*args: object, **kwargs: object) -> None:
        raise RuntimeError("deliberate test model load failure")

    monkeypatch.setattr(server_module, "_load_model_module", fail_model_load)
    # Preserve the teardown contract of the cached production loader.
    monkeypatch.setattr(fail_model_load, "cache_clear", lambda: None, raising=False)
    response = cors_client.post(
        "/api/compute", json={"concept_id": "04", "overrides": {}}, headers={"Origin": origin},
    )
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert response.headers.get("access-control-allow-origin") == (
        origin if origin in ALLOWED_ORIGINS else None
    )


def test_factory_preserves_fastapi_contract(
    costingfe_base_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("EXPLORER_SKIP_WARMUP", "1")
    app = create_app(base_dir=costingfe_base_dir)
    assert isinstance(app, FastAPI)
    app.state.contract_marker = "retained"
    assert any(route.path == "/api/compute" for route in app.routes)

    def dependency() -> str:
        return "original"

    @app.get("/test-factory-contract")
    def contract(value: str = Depends(dependency)) -> dict[str, str]:
        return {"value": value, "marker": app.state.contract_marker}

    app.dependency_overrides[dependency] = lambda: "overridden"
    with TestClient(app) as client:
        assert app.state.data is not None
        assert client.get("/test-factory-contract").json() == {
            "value": "overridden", "marker": "retained",
        }
        schema = client.get("/openapi.json").json()
        assert "post" in schema["paths"]["/api/compute"]
        assert "get" in schema["paths"]["/api/manifest"]
    assert app.state.data is None
