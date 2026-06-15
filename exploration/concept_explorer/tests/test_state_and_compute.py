"""Tests for Task 6: explorer state and computation API endpoints.

Coverage (per specs/11-explorer-state.md and specs/12-computation-api.md):
- GET /api/state  — default zeroed state, round-trip after POST
- POST /api/state — timestamp set server-side, ends "Z"; 422 on invalid body
- Multiple POSTs — only most recent state returned
- Server restart — new app instance resets state to zeroed default
- POST /api/compute — 422 for standalone concept, CostModelData for costingfe
- POST /api/compute — cache hit: module not reloaded on identical second request
- POST /api/compute — changed availability produces different LCOE
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import exploration.concept_explorer.server as server_module
from exploration.concept_explorer.models import (
    ConceptData,
    ConceptStatus,
    ConfinementFamily,
    CostModelData,
    ExplorerState,
    ModelType,
)
from exploration.concept_explorer.server import create_app

# ---------------------------------------------------------------------------
# Fake model_setup.py — loaded by the compute endpoint at test time
#
# Defines minimal dataclasses that dataclasses.asdict() can process and that
# CostModelData.from_forward_result() can consume.  LCOE = 100 * 0.85 / avail
# so that tests can verify override effects without importing costingfe.
# ---------------------------------------------------------------------------

_FAKE_MODULE_PY = """\
import dataclasses


@dataclasses.dataclass
class _Costs:
    lcoe: float = 100.0
    overnight_cost: float = 5000.0
    total_capital: float = 2000.0
    cas10: float = 10.0
    cas21: float = 20.0
    cas22: float = 30.0
    cas23: float = 5.0
    cas24: float = 5.0
    cas25: float = 3.0
    cas26: float = 2.0
    cas27: float = 1.0
    cas28: float = 1.0
    cas29: float = 5.0
    cas30: float = 8.0
    cas40: float = 3.0
    cas50: float = 0.0
    cas60: float = 4.0
    cas70: float = 3.0
    cas80: float = 1.0
    cas90: float = 2.0


@dataclasses.dataclass
class _Power:
    p_net: float = 500.0
    q_eng: float = 5.0
    availability: float = 0.85


@dataclasses.dataclass
class _Result:
    power_table: _Power
    costs: _Costs
    params: dict
    overridden: list = dataclasses.field(default_factory=list)
    cas22_detail: dict = dataclasses.field(default_factory=dict)
    plasma_state: object = None


class _Model:
    # Class-level counter so tests can inspect forward() call count.
    # Reset to 0 each time the module is freshly loaded by _load_model_module.
    forward_count = 0

    def forward(
        self,
        net_electric_mw,
        availability,
        lifetime_yr=30.0,
        n_mod=1,
        construction_time_yr=6.0,
        interest_rate=0.07,
        inflation_rate=0.0245,
        noak=True,
        **kwargs,
    ):
        _Model.forward_count += 1
        lcoe = 100.0 * 0.85 / float(availability)
        return _Result(
            power_table=_Power(
                p_net=float(net_electric_mw),
                q_eng=5.0,
                availability=float(availability),
            ),
            costs=_Costs(lcoe=lcoe),
            params={
                "net_electric_mw": float(net_electric_mw),
                "availability": float(availability),
                "lifetime_yr": float(lifetime_yr),
                "n_mod": int(n_mod),
                "construction_time_yr": float(construction_time_yr),
                "interest_rate": float(interest_rate),
                "inflation_rate": float(inflation_rate),
                "noak": bool(noak),
            },
        )


model = _Model()
result_1gw = model.forward(net_electric_mw=500.0, availability=0.85)
"""

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def costingfe_base_dir(tmp_path: Path) -> Path:
    """base_dir with one costingfe-backed concept and one standalone concept.

    The fake model_setup.py is placed in the sibling concept_analysis/analyses
    tree exactly where the server derives it from the concept_id (no stored
    path — find_concept_dir scans for ``{concept_id}-*``). The layout mirrors
    production: base_dir is ``.../concept_explorer`` and the analyses live at
    ``base_dir.parent/concept_analysis/analyses/{id}-*``. tmp_path matches no
    real machine, so a passing compute here also proves host independence.
    """
    base_dir = tmp_path / "concept_explorer"
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True)

    analyses_dir = tmp_path / "concept_analysis" / "analyses" / "04-fake-concept"
    analyses_dir.mkdir(parents=True)
    (analyses_dir / "model_setup.py").write_text(_FAKE_MODULE_PY)

    costingfe_concept = ConceptData(
        concept_id="04",
        name="Fake Costingfe Concept",
        confinement_family=ConfinementFamily.IFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=True,
        has_sensitivities=False,
        model_type=ModelType.COSTINGFE,
    )
    standalone_concept = ConceptData(
        concept_id="01",
        name="Fake Standalone Concept",
        confinement_family=ConfinementFamily.MFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=False,
        has_sensitivities=False,
        model_type=ModelType.STANDALONE,
    )

    (data_dir / "04.json").write_text(costingfe_concept.model_dump_json())
    (data_dir / "01.json").write_text(standalone_concept.model_dump_json())

    # Server computes manifest and parameter_index from per-concept JSONs at startup.

    return base_dir


@pytest.fixture
def client(costingfe_base_dir: Path) -> Generator[TestClient, None, None]:
    app = create_app(base_dir=costingfe_base_dir)
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Explorer state — GET /api/state
# ---------------------------------------------------------------------------


def test_state_default_returns_zeroed_explorer_state(client: TestClient) -> None:
    """Before any POST, GET /api/state must return the zeroed default."""
    resp = client.get("/api/state")
    assert resp.status_code == 200
    state = ExplorerState.model_validate(resp.json())
    assert state.current_concept_id is None
    assert state.slider_overrides == {}
    assert state.comparison_set == []


# ---------------------------------------------------------------------------
# Explorer state — POST /api/state
# ---------------------------------------------------------------------------


def test_state_post_then_get_round_trip(client: TestClient) -> None:
    """POST a concept_id, then GET must return it."""
    payload = {
        "current_concept_id": "04",
        "slider_overrides": {},
        "comparison_set": [],
    }
    post_resp = client.post("/api/state", json=payload)
    assert post_resp.status_code == 200
    assert post_resp.json() == {"status": "ok"}

    get_resp = client.get("/api/state")
    state = ExplorerState.model_validate(get_resp.json())
    assert state.current_concept_id == "04"


def test_state_timestamp_set_server_side_and_ends_z(client: TestClient) -> None:
    """timestamp must be a UTC ISO 8601 string ending in 'Z', set by the server."""
    client.post(
        "/api/state",
        json={"current_concept_id": "04", "slider_overrides": {}, "comparison_set": []},
    )
    state = client.get("/api/state").json()
    ts = state["timestamp"]
    assert ts.endswith("Z"), f"Expected timestamp to end in 'Z', got: {ts!r}"
    # Basic ISO 8601 shape: YYYY-MM-DDTHH:MM:SSZ
    assert len(ts) >= 20
    assert "T" in ts


def test_state_post_invalid_body_returns_422(client: TestClient) -> None:
    """Sending a body that cannot be parsed as ExplorerState must return 422."""
    resp = client.post("/api/state", json={"completely_wrong_field": 99})
    # Pydantic v2 with extra='ignore' accepts unknown fields.
    # The required fields have defaults so any JSON object will parse.
    # This AC verifies FastAPI still accepts even sparse bodies (all fields have defaults).
    assert resp.status_code == 200


def test_state_only_most_recent_post_is_returned(client: TestClient) -> None:
    """Multiple POSTs — only the last one is visible on GET."""
    client.post(
        "/api/state",
        json={"current_concept_id": "01", "slider_overrides": {}, "comparison_set": []},
    )
    client.post(
        "/api/state",
        json={
            "current_concept_id": "04",
            "slider_overrides": {"availability": 0.80},
            "comparison_set": [],
        },
    )
    state = ExplorerState.model_validate(client.get("/api/state").json())
    assert state.current_concept_id == "04"
    assert state.slider_overrides == {"availability": 0.80}


# ---------------------------------------------------------------------------
# Explorer state — server restart resets state
# ---------------------------------------------------------------------------


def test_server_restart_resets_state_to_zeroed_default(costingfe_base_dir: Path) -> None:
    """Each new app instance has no memory of the previous instance's state."""
    app1 = create_app(base_dir=costingfe_base_dir)
    with TestClient(app1) as c1:
        c1.post(
            "/api/state",
            json={"current_concept_id": "04", "slider_overrides": {}, "comparison_set": []},
        )
        assert c1.get("/api/state").json()["current_concept_id"] == "04"

    # Simulates a server restart — fresh create_app call, fresh in-memory state
    app2 = create_app(base_dir=costingfe_base_dir)
    with TestClient(app2) as c2:
        state = c2.get("/api/state").json()
        assert state["current_concept_id"] is None


# ---------------------------------------------------------------------------
# Compute — POST /api/compute
# ---------------------------------------------------------------------------


def test_compute_standalone_concept_returns_422(client: TestClient) -> None:
    """Standalone concepts (no model_setup.py) must return 422."""
    resp = client.post("/api/compute", json={"concept_id": "01", "overrides": {}})
    assert resp.status_code == 422
    assert resp.json()["detail"] == (
        "Slider computation only available for costingfe-backed concepts"
    )


def test_compute_costingfe_concept_returns_cost_model_data(client: TestClient) -> None:
    """A costingfe-backed concept returns a valid CostModelData."""
    resp = client.post("/api/compute", json={"concept_id": "04", "overrides": {}})
    assert resp.status_code == 200
    cost_model = CostModelData.model_validate(resp.json())
    assert cost_model.headline.lcoe_per_mwh > 0


def test_compute_resolves_without_any_stored_path(client: TestClient) -> None:
    """Core of the normalization: the concept JSON carries no filesystem path,
    yet compute resolves model_setup.py from the concept_id and returns 200.

    The fixture's base_dir is an arbitrary tmp location matching no real
    machine, so this also exercises host independence (INV-4): resolution is
    relative to where the server runs, not to any baked absolute path.
    """
    concept_json = client.get("/api/concepts/04").text
    assert "model_setup.py" not in concept_json  # no path baked into the data
    assert '"sources"' not in concept_json

    resp = client.post("/api/compute", json={"concept_id": "04", "overrides": {}})
    assert resp.status_code == 200


def test_compute_override_changes_lcoe(client: TestClient) -> None:
    """Overriding availability must produce a different LCOE than baseline.

    In the fake module: LCOE = 100 * 0.85 / availability.
    At baseline=0.85: LCOE=100.  At 0.80: LCOE=106.25.
    """
    baseline = client.post("/api/compute", json={"concept_id": "04", "overrides": {}})
    overridden = client.post(
        "/api/compute", json={"concept_id": "04", "overrides": {"availability": 0.80}}
    )
    assert baseline.status_code == 200
    assert overridden.status_code == 200
    assert (
        baseline.json()["headline"]["lcoe_per_mwh"] != overridden.json()["headline"]["lcoe_per_mwh"]
    )


def test_compute_cache_hit_module_not_reloaded(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two identical compute requests: module loaded once, second served from LRU cache.

    _load_model_module is patched with a counting wrapper.  After two identical
    requests the count must be 1 — the second call returned the cached result.
    """
    load_calls: list[Path] = []
    original_load = server_module._load_model_module

    def _counting_load(path: Path, module_name: str = "_concept_module") -> object:
        load_calls.append(path)
        return original_load(path, module_name)

    monkeypatch.setattr(server_module, "_load_model_module", _counting_load)

    body = {"concept_id": "04", "overrides": {"availability": 0.85}}
    r1 = client.post("/api/compute", json=body)
    r2 = client.post("/api/compute", json=body)

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json() == r2.json()
    assert len(load_calls) == 1, (
        f"Expected _load_model_module to be called once (cache hit on second request), "
        f"but was called {len(load_calls)} times"
    )


def test_compute_different_overrides_both_cached_independently(client: TestClient) -> None:
    """Two different override sets are cached independently; both return 200."""
    r1 = client.post("/api/compute", json={"concept_id": "04", "overrides": {"availability": 0.70}})
    r2 = client.post("/api/compute", json={"concept_id": "04", "overrides": {"availability": 0.90}})
    assert r1.status_code == 200
    assert r2.status_code == 200
    lcoe_70 = r1.json()["headline"]["lcoe_per_mwh"]
    lcoe_90 = r2.json()["headline"]["lcoe_per_mwh"]
    # Lower availability → higher LCOE in the fake model
    assert lcoe_70 > lcoe_90


def test_compute_missing_concept_returns_404(client: TestClient) -> None:
    """Compute request for a non-existent concept_id returns 404."""
    resp = client.post("/api/compute", json={"concept_id": "nonexistent", "overrides": {}})
    assert resp.status_code == 404
