"""Tests for explorer-slider-override-semantics, Phase 1 (compute-path correctness).

Spec/design/plan: .project/active/explorer-slider-override-semantics/

Phase 1 covers the backend only — the `apply_analyst_overrides` flag threaded
through `POST /api/compute`:

- FR-SO1 / INV-1: a no-op recompute at default UI state (`apply=True`,
  `overrides={}`) reproduces the stored `result_1gw` headline, because the
  recompute re-applies the analyst override registry exactly as
  `run_native_and_1gw` does. `apply=False` drops the registry → the library-bare
  LCOE, which is lower by the registry's magnitude.
- FR-SO5 / INV-4: `apply_analyst_overrides` participates in the LRU cache key, so
  the same (concept, overrides) with a different flag does NOT collide.
- INV-6: an empty / absent registry makes the two branches identical.

The FR-SO1 proof asserts against the *live* concept 01 module (never a hardcoded
155.17 — guards param drift), per the plan's first proof point. The cache-key and
INV-6 checks use a self-contained fake module so they run without costingfe.
"""

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.server import create_app

# Real concept 01 — the load-bearing FR-SO1 regression target.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_REAL_DATA_01 = _REPO_ROOT / "exploration" / "concept_explorer" / "data" / "01.json"
_REAL_CONCEPT_01_DIR = (
    _REPO_ROOT / "exploration" / "concept_analysis" / "analyses" / "01-hts-compact-tokamak"
)


# ---------------------------------------------------------------------------
# FR-SO1 / INV-1 — live regression against the real concept 01 module
# ---------------------------------------------------------------------------


@pytest.fixture
def real_concept_01_client(tmp_path: Path) -> Generator[TestClient, None, None]:
    """A server loaded with only the real concept 01 JSON.

    The copied JSON's `sources.model_setup` is an absolute path to the real
    module, so the compute path re-applies the actual analyst registry. Requires
    costingfe (skipped otherwise) — the compute endpoint loads the real module.
    """
    pytest.importorskip("costingfe")
    if not _REAL_DATA_01.is_file():
        pytest.skip(f"real concept 01 data not found at {_REAL_DATA_01}")

    # base_dir must nest one level deep: the compute path resolves the concept's
    # model_setup.py via `_analyses_root(base_dir) == base_dir.parent /
    # concept_analysis / analyses` (server.py, since efa8e885 dropped the
    # per-concept stored module path). So put the explorer dir under tmp_path and
    # expose the real analyses tree as its sibling via a symlink — the fixture
    # otherwise FileNotFoundErrors before any costing runs.
    explorer_dir = tmp_path / "concept_explorer"
    data_dir = explorer_dir / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "01.json").write_text(_REAL_DATA_01.read_text())

    analyses_parent = tmp_path / "concept_analysis"
    analyses_parent.mkdir()
    (analyses_parent / "analyses").symlink_to(
        _REAL_CONCEPT_01_DIR.parent, target_is_directory=True
    )

    app = create_app(base_dir=explorer_dir)
    with TestClient(app) as c:
        yield c


def test_fr_so1_noop_compute_matches_stored_headline(
    real_concept_01_client: TestClient,
) -> None:
    """apply=True no-op recompute ≡ stored headline; apply=False is bare (lower)."""
    stored = json.loads(_REAL_DATA_01.read_text())
    stored_lcoe = stored["cost_model"]["headline"]["lcoe_per_mwh"]

    applied = real_concept_01_client.post(
        "/api/compute",
        json={"concept_id": "01", "overrides": {}, "apply_analyst_overrides": True},
    )
    bare = real_concept_01_client.post(
        "/api/compute",
        json={"concept_id": "01", "overrides": {}, "apply_analyst_overrides": False},
    )
    assert applied.status_code == 200
    assert bare.status_code == 200

    applied_lcoe = applied.json()["headline"]["lcoe_per_mwh"]
    bare_lcoe = bare.json()["headline"]["lcoe_per_mwh"]

    # INV-1: re-applied forward reproduces the stored result_1gw headline.
    assert applied_lcoe == pytest.approx(stored_lcoe, rel=1e-5)
    # Registry dropped → strictly lower (concept 01's C220103 magnet override is
    # large; spec records ~-17.8%). Assert direction + non-trivial magnitude, not
    # a literal, so the test survives param drift.
    assert bare_lcoe < stored_lcoe
    assert (stored_lcoe - bare_lcoe) / stored_lcoe > 0.05


def test_fr_so1_default_flag_matches_explicit_true(
    real_concept_01_client: TestClient,
) -> None:
    """Omitting apply_analyst_overrides defaults to True (the FR-SO1 default state)."""
    default = real_concept_01_client.post(
        "/api/compute", json={"concept_id": "01", "overrides": {}}
    )
    explicit_true = real_concept_01_client.post(
        "/api/compute",
        json={"concept_id": "01", "overrides": {}, "apply_analyst_overrides": True},
    )
    assert default.status_code == 200
    assert explicit_true.status_code == 200
    assert (
        default.json()["headline"]["lcoe_per_mwh"]
        == explicit_true.json()["headline"]["lcoe_per_mwh"]
    )


# ---------------------------------------------------------------------------
# FR-SO5 / INV-4 / INV-6 — flag in the cache key; empty-registry equivalence
#
# Self-contained fake module whose forward() responds to cost_overrides, so the
# applied vs bare branches diverge without needing costingfe.  Registry has one
# enabled and one disabled entry; result_1gw is built overrides-on (mirroring
# run_native_and_1gw) so the apply=True no-op reproduces it.
# ---------------------------------------------------------------------------

_FAKE_MODULE_WITH_REGISTRY = """\
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
    p_net: float = 1000.0
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
    def forward(
        self,
        net_electric_mw,
        availability,
        lifetime_yr=40.0,
        n_mod=1,
        construction_time_yr=6.0,
        interest_rate=0.07,
        inflation_rate=0.02,
        noak=True,
        cost_overrides=None,
        override_reference_mw=None,
        **kwargs,
    ):
        # Base library-bare LCOE; the registry adds a fixed, observable bump so
        # applied != bare. (override_reference_mw is accepted but the toy model
        # does not scale by it — n_mod effects are out of scope for this unit.)
        lcoe = 100.0 * 0.85 / float(availability)
        if cost_overrides:
            lcoe += 0.01 * sum(cost_overrides.values())
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
P_native = 500.0
overrides = [
    {"account": "C220103", "value": 1000.0, "enabled": True,
     "provenance": "direct", "source": "test", "rationale": "test",
     "cost_basis": "noak"},
    {"account": "CAS27", "value": 999.0, "enabled": False,
     "provenance": "direct", "source": "test", "rationale": "test",
     "cost_basis": "noak", "blocked_by": "org/repo#1"},
]
# Mirror run_native_and_1gw: result_1gw is computed overrides-ON.
result_1gw = model.forward(
    net_electric_mw=1000.0,
    n_mod=2,
    availability=0.85,
    cost_overrides={"C220103": 1000.0},
    override_reference_mw=P_native,
)
"""

# Same shape but an empty registry (INV-6).
_FAKE_MODULE_EMPTY_REGISTRY = _FAKE_MODULE_WITH_REGISTRY.replace(
    """overrides = [
    {"account": "C220103", "value": 1000.0, "enabled": True,
     "provenance": "direct", "source": "test", "rationale": "test",
     "cost_basis": "noak"},
    {"account": "CAS27", "value": 999.0, "enabled": False,
     "provenance": "direct", "source": "test", "rationale": "test",
     "cost_basis": "noak", "blocked_by": "org/repo#1"},
]""",
    "overrides = []",
).replace(
    'cost_overrides={"C220103": 1000.0},\n    override_reference_mw=P_native,',
    "cost_overrides={},\n    override_reference_mw=P_native,",
)


def _make_client(tmp_path: Path, module_src: str) -> TestClient:
    """Build a TestClient with one fake costingfe concept ('04') from *module_src*."""
    from exploration.concept_explorer.models import (
        ConceptData,
        ConceptStatus,
        ConfinementFamily,
        ModelType,
    )

    # model_setup.py goes where the server derives it from the concept_id:
    # base_dir.parent/concept_analysis/analyses/{id}-* (no stored path).
    base_dir = tmp_path / "concept_explorer"
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True)

    analyses_dir = tmp_path / "concept_analysis" / "analyses" / "04-fake"
    analyses_dir.mkdir(parents=True)
    (analyses_dir / "model_setup.py").write_text(module_src)

    concept = ConceptData(
        concept_id="04",
        name="Fake Registry Concept",
        confinement_family=ConfinementFamily.MFE,
        status=ConceptStatus.IN_PROGRESS,
        has_cost_model=True,
        has_sensitivities=False,
        model_type=ModelType.COSTINGFE,
    )
    (data_dir / "04.json").write_text(concept.model_dump_json())

    app = create_app(base_dir=base_dir)
    return TestClient(app)


def test_fr_so1_fake_module_applied_reproduces_result_1gw(tmp_path: Path) -> None:
    """apply=True no-op reproduces the overrides-on result_1gw (FR-SO1, no costingfe)."""
    with _make_client(tmp_path, _FAKE_MODULE_WITH_REGISTRY) as client:
        applied = client.post(
            "/api/compute",
            json={"concept_id": "04", "overrides": {}, "apply_analyst_overrides": True},
        )
        assert applied.status_code == 200
        # base 100*0.85/0.85 = 100; bump 0.01*1000 = 10 → 110 (matches result_1gw).
        assert applied.json()["headline"]["lcoe_per_mwh"] == pytest.approx(110.0)


def test_cache_key_includes_flag_no_collision(tmp_path: Path) -> None:
    """INV-4/FR-SO5: same (concept, overrides), different flag → different result.

    If the flag were absent from the LRU key, the second (apply=False) call would
    return the first (apply=True) cached value. Distinct values prove the key
    includes the flag.
    """
    with _make_client(tmp_path, _FAKE_MODULE_WITH_REGISTRY) as client:
        applied = client.post(
            "/api/compute",
            json={"concept_id": "04", "overrides": {}, "apply_analyst_overrides": True},
        )
        bare = client.post(
            "/api/compute",
            json={"concept_id": "04", "overrides": {}, "apply_analyst_overrides": False},
        )
        assert applied.status_code == 200
        assert bare.status_code == 200
        applied_lcoe = applied.json()["headline"]["lcoe_per_mwh"]
        bare_lcoe = bare.json()["headline"]["lcoe_per_mwh"]
        assert applied_lcoe == pytest.approx(110.0)
        assert bare_lcoe == pytest.approx(100.0)
        assert applied_lcoe != bare_lcoe


def test_inv6_empty_registry_applied_equals_bare(tmp_path: Path) -> None:
    """INV-6: with an empty registry, apply=True and apply=False agree."""
    with _make_client(tmp_path, _FAKE_MODULE_EMPTY_REGISTRY) as client:
        applied = client.post(
            "/api/compute",
            json={"concept_id": "04", "overrides": {}, "apply_analyst_overrides": True},
        )
        bare = client.post(
            "/api/compute",
            json={"concept_id": "04", "overrides": {}, "apply_analyst_overrides": False},
        )
        assert applied.status_code == 200
        assert bare.status_code == 200
        assert (
            applied.json()["headline"]["lcoe_per_mwh"]
            == bare.json()["headline"]["lcoe_per_mwh"]
        )


# ---------------------------------------------------------------------------
# Phase 2 — FR-SO4: extractor emits both sensitivities + analyst_override_count
# ---------------------------------------------------------------------------


def test_fr_so4_real_concept_01_both_sensitivities_and_count() -> None:
    """FR-SO4 / INV-3 (live): concept 01 extracts applied + bare sensitivities that
    differ for ≥1 param, and analyst_override_count == enabled registry size."""
    pytest.importorskip("costingfe")
    if not (_REAL_CONCEPT_01_DIR / "model_setup.py").is_file():
        pytest.skip(f"real concept 01 dir not found at {_REAL_CONCEPT_01_DIR}")

    from exploration.concept_explorer.extract_explorer_data import (
        extract_costingfe,
        load_module_from_path,
        parse_frontmatter,
    )

    analysis_path = _REAL_CONCEPT_01_DIR / "analysis.md"
    frontmatter = parse_frontmatter(analysis_path)
    cd = extract_costingfe(
        concept_dir=_REAL_CONCEPT_01_DIR,
        concept_id="01",
        frontmatter=frontmatter,
        analysis_path=analysis_path,
        narrative=None,
        param_metadata={},
        comparison_status=str(frontmatter.get("Comparison-Status", "")),
    )

    cm = cd.cost_model
    assert cm is not None
    assert cm.sensitivities is not None and cm.sensitivities_bare is not None

    # Same param keys in both flavors (cost_overrides changes values, not the key
    # set); at least one elasticity differs (INV-3 — applied is not bare).
    eng_keys = set(cm.sensitivities.engineering) & set(cm.sensitivities_bare.engineering)
    fin_keys = set(cm.sensitivities.financial) & set(cm.sensitivities_bare.financial)
    differs = any(
        cm.sensitivities.engineering[k].elasticity
        != cm.sensitivities_bare.engineering[k].elasticity
        for k in eng_keys
    ) or any(
        cm.sensitivities.financial[k].elasticity
        != cm.sensitivities_bare.financial[k].elasticity
        for k in fin_keys
    )
    assert differs, "applied and bare sensitivities are identical — registry had no effect"

    # Count matches the live registry projection.
    module = load_module_from_path(_REAL_CONCEPT_01_DIR / "model_setup.py")
    from lib.model_setup_helpers import enabled_overrides

    assert cd.analyst_override_count == len(enabled_overrides(module.overrides))
    assert cd.analyst_override_count >= 1  # concept 01 has the C220103 magnet override


def test_fr_so4_mock_wiring_both_present_and_count(tmp_path: Path) -> None:
    """FR-SO4 wiring without costingfe: a mock whose sensitivity() varies with
    cost_overrides yields differing applied/bare payloads; count = enabled size."""
    import types
    from unittest.mock import MagicMock, patch

    from exploration.concept_explorer.extract_explorer_data import extract_costingfe
    from exploration.concept_explorer.tests.test_extraction import (
        _make_concept_dir,
        _make_forward_result,
    )

    def _sensitivity(params: dict, cost_overrides: dict | None = None) -> dict:
        # Applied (registry present) returns different elasticities than bare.
        if cost_overrides:
            return {
                "engineering": {"availability": 0.55, "thermal_efficiency": -0.30},
                "financial": {"interest_rate": 0.80},
            }
        return {
            "engineering": {"availability": 0.75, "thermal_efficiency": -0.42},
            "financial": {"interest_rate": 0.85},
        }

    model = MagicMock()
    model.sensitivity.side_effect = _sensitivity

    registry = [
        {"account": "C220103", "value": 1000.0, "enabled": True, "provenance": "direct",
         "source": "t", "rationale": "t", "cost_basis": "noak"},
        {"account": "CAS27", "value": 9.0, "enabled": False, "provenance": "direct",
         "source": "t", "rationale": "t", "cost_basis": "noak", "blocked_by": "o/r#1"},
    ]
    mock_module = types.SimpleNamespace(
        model=model, result_1gw=_make_forward_result(), overrides=registry, P_native=233.0
    )
    concept_dir = _make_concept_dir(tmp_path, with_model_setup=True)

    with patch(
        "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
        return_value=mock_module,
    ):
        cd = extract_costingfe(
            concept_dir=concept_dir,
            concept_id="04",
            frontmatter={"Concept": "Mock", "Status": "approved"},  # no P-Native → skip verify
            analysis_path=concept_dir / "analysis.md",
            narrative=None,
            param_metadata={},
        )

    cm = cd.cost_model
    assert cm is not None
    assert cm.sensitivities is not None and cm.sensitivities_bare is not None
    # Applied availability elasticity (0.55) differs from bare (0.75).
    assert cm.sensitivities.engineering["availability"].elasticity == pytest.approx(0.55)
    assert cm.sensitivities_bare.engineering["availability"].elasticity == pytest.approx(0.75)
    # Only the one enabled entry counts.
    assert cd.analyst_override_count == 1
