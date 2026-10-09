"""Self-tests for the website contract gate (exploration/concept_explorer/website_contract).

These run inside the gate. Most use a small repo-shaped fixture: three concepts with
sensitivities, an analyst override, a taxonomy registry and tree, findings text and
archetype-fit grades, served by the fake costing model from test_state_and_compute.py.
Each break test records a contract from the unbroken fixture, makes one change, and runs
the gate's own `check` entry point (design Appendix D).
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from starlette.types import ASGIApp, Message, Receive, Scope, Send

import exploration.concept_explorer.models as models_module
import exploration.concept_explorer.server as server_module
from exploration.concept_explorer.models import (
    CASAccount,
    ComputeRequest,
    ConceptData,
    ConceptStatus,
    Confidence,
    ConfinementFamily,
    CostModelData,
    ExplorerState,
    FuelType,
    HeadlineEconomics,
    ModelType,
    NarrativeData,
    OverrideRecord,
    ParameterCategory,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
)
from exploration.concept_explorer.taxonomy_models import (
    ConceptRegistry,
    ConceptTaxonomy,
    IFEDriver,
    MFETopology,
    OperationMode,
    TaxonomyConfidence,
)
from exploration.concept_explorer.tests import test_state_and_compute as compute_tests
from exploration.concept_explorer.website_contract import contract as c

PIN = "0" * 40

# ---------------------------------------------------------------------------
# The fixture: a repo root laid out as <root>/exploration/..., so the server's
# sibling-tree lookups (analyses, tables, archive) resolve inside it.
# ---------------------------------------------------------------------------

DATA = c.EXPLORER / "data"
ANALYSES = Path("exploration/concept_analysis/analyses")
FIT_TABLE = Path("exploration/concept_analysis/tables/archetype_fit.csv")

# Parameter name -> (elasticity, baseline, range low, range high). 04 and 05 share
# `availability`, so that parameter's concepts[] lists both.
_PARAMETERS_04 = {
    "engineering": {
        "availability": (-1.0, 0.85, 0.5, 0.95),
        "net_electric_mw": (-0.3, 500.0, 300.0, 1000.0),
    },
    "financial": {
        "interest_rate": (0.5, 0.07, 0.03, 0.1),
        "lifetime_yr": (-0.2, 30.0, 20.0, 40.0),
    },
}
_PARAMETERS_05 = {
    "engineering": {
        "availability": (-0.9, 0.85, 0.5, 0.95),
        "construction_time_yr": (0.1, 6.0, 4.0, 10.0),
    },
    "financial": {"inflation_rate": (0.1, 0.0245, 0.01, 0.04)},
}
# The module-level registry the compute route re-applies for 04's slider bodies.
_ANALYST_OVERRIDES_PY = """
overrides = [
    {"account": "CAS27", "value": 1.0, "enabled": True, "provenance": "direct",
     "source": "fixture", "rationale": "fixture", "cost_basis": "noak"},
]
P_native = 500.0
"""


def _cost_model(sensitivities: SensitivityAnalysis) -> CostModelData:
    account = CASAccount(name="Account", cost_m_usd=1.0)
    top_level = (10, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90)
    return CostModelData(
        **{f"cas{number}": account for number in top_level},
        cas22_detail={"C220101": account},
        headline=HeadlineEconomics(
            lcoe_per_mwh=100.0,
            overnight_cost_per_kw=5000.0,
            p_net_mw=500.0,
            q_eng=5.0,
            capacity_factor=0.85,
        ),
        sensitivities=sensitivities,
        sensitivities_bare=sensitivities,
    )


def _costingfe(
    concept_id: str,
    family: ConfinementFamily,
    parameters: dict[str, dict[str, tuple[float, float, float, float]]],
    **fields: Any,
) -> ConceptData:
    sensitivities = SensitivityAnalysis(
        **{
            group: {
                name: SensitivityEntry(elasticity=elasticity, baseline=baseline)
                for name, (elasticity, baseline, _, _) in entries.items()
            }
            for group, entries in parameters.items()
        }
    )
    metadata = {
        name: ParameterMetadata(
            display_name=name,
            category=ParameterCategory.WELL_ESTABLISHED,
            confidence=Confidence.MEDIUM,
            baseline=baseline,
            range=(low, high),
        )
        for entries in parameters.values()
        for name, (_, baseline, low, high) in entries.items()
    }
    return ConceptData(
        concept_id=concept_id,
        name=f"Fake {concept_id}",
        confinement_family=family,
        status=ConceptStatus.APPROVED,
        has_cost_model=True,
        has_sensitivities=True,
        model_type=ModelType.COSTINGFE,
        cost_model=_cost_model(sensitivities),
        parameter_metadata=metadata,
        **fields,
    )


def _taxonomy(concept_id: str, family: ConfinementFamily, **fields: Any) -> ConceptTaxonomy:
    return ConceptTaxonomy(
        concept_id=concept_id,
        slug=f"fake-{concept_id}",
        name=f"Fake {concept_id}",
        confinement_family=family,
        fuel=FuelType.DT,
        operation_mode=OperationMode.STEADY_STATE,
        confidence=TaxonomyConfidence.HIGH,
        **fields,
    )


def build_fixture(root: Path) -> None:
    """Write the fixture repo under `root`: 01 standalone, 04 and 05 costingfe."""
    concepts = [
        ConceptData(
            concept_id="01",
            name="Fake 01",
            confinement_family=ConfinementFamily.MFE,
            status=ConceptStatus.IN_PROGRESS,
            has_cost_model=False,
            has_sensitivities=False,
            model_type=ModelType.STANDALONE,
        ),
        _costingfe(
            "04",
            ConfinementFamily.IFE,
            _PARAMETERS_04,
            analyst_override_count=1,
            overrides=[
                OverrideRecord(
                    account="CAS27", account_name="Special Materials", value=1.0, enabled=True
                )
            ],
        ),
        _costingfe("05", ConfinementFamily.MFE, _PARAMETERS_05),
    ]
    (root / DATA).mkdir(parents=True)
    for concept in concepts:
        (root / DATA / f"{concept.concept_id}.json").write_text(concept.model_dump_json())
    registry = ConceptRegistry(
        version="1",
        concepts=[
            _taxonomy("01", ConfinementFamily.MFE, mfe_topology=MFETopology.TOKAMAK),
            _taxonomy("04", ConfinementFamily.IFE, ife_driver=IFEDriver.LASER),
            _taxonomy("05", ConfinementFamily.MFE, mfe_topology=MFETopology.STELLARATOR),
        ],
    )
    (root / DATA / "concept_registry.json").write_text(registry.model_dump_json())
    tree = {
        "version": "1",
        "root": {
            "field": "tree_group",
            "label": "Confinement Approach",
            "children": [
                {
                    "value": "MFE",
                    "label": "Magnetic",
                    "field": "mfe_topology",
                    "children": [
                        {"value": "Tokamak", "label": "Tokamak", "concepts": ["01"]},
                        {"value": "Stellarator", "label": "Stellarator", "concepts": ["05"]},
                    ],
                },
                {"value": "IFE", "label": "Inertial", "concepts": ["04"]},
            ],
        },
    }
    (root / DATA / "decision_tree.json").write_text(json.dumps(tree))
    (root / c.EXPLORER / "omit_list.yaml").write_text("{}\n")

    (root / ANALYSES / "04-fake").mkdir(parents=True)
    (root / ANALYSES / "04-fake" / "model_setup.py").write_text(
        compute_tests._FAKE_MODULE_PY + _ANALYST_OVERRIDES_PY
    )
    (root / ANALYSES / "04-fake" / "analysis.md").write_text("# Findings\n\nWhat 04 found.\n")
    (root / ANALYSES / "05-fake").mkdir()
    (root / ANALYSES / "05-fake" / "model_setup.py").write_text(compute_tests._FAKE_MODULE_PY)
    (root / FIT_TABLE).parent.mkdir(parents=True)
    (root / FIT_TABLE).write_text("concept_id,fit_grade\n01-fake,High\n04-fake,Med\n05-fake,None\n")


@pytest.fixture
def fixture_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "repo"
    build_fixture(root)
    monkeypatch.setattr(models_module, "_OMIT_LIST_PATH", root / c.EXPLORER / "omit_list.yaml")
    monkeypatch.setenv("EXPLORER_SKIP_WARMUP", "1")
    monkeypatch.setattr(sys, "path", list(sys.path))  # `check` puts its tree first
    return root


def record_in_process(root: Path) -> Path:
    """Record the fixture's contract in this process (N7) and return the file's path."""
    path = root.parent / "contract.txt"
    path.write_text(c.render(c.record_tree(root, PIN, tools=[], js={})))
    return path


@dataclass(frozen=True)
class GateRun:
    code: int
    out: str

    def lines(self, label: str) -> set[str]:
        return {
            line.removeprefix(label + " ")
            for line in self.out.splitlines()
            if line.startswith(label + " ")
        }

    @property
    def failed(self) -> set[str]:
        return self.lines("FAIL")

    @property
    def waived(self) -> set[str]:
        return self.lines("WAIVED")


def run_check(
    root: Path, contract_path: Path, capsys: pytest.CaptureFixture[str], waivers: str = ""
) -> GateRun:
    """Run `contract.py check` on `root`, with `waivers` as the whole waivers.toml."""
    waivers_path = root.parent / "waivers.toml"
    waivers_path.write_text(waivers)
    argv = ["check", "--tree", str(root), "--contract", str(contract_path)]
    code = c.main([*argv, "--waivers", str(waivers_path)])
    return GateRun(code, capsys.readouterr().out)


def waiver(match: str, evidence: str = "parameter_card.js:258 builds the link") -> str:
    return (
        f'[[waiver]]\nmatch = "{match}"\nreason = "fixture"\n'
        f'evidence = "{evidence}"\ndate = 2026-10-08\n'
    )


def edit_json(path: Path, change: Callable[[Any], None]) -> None:
    body = json.loads(path.read_text())
    change(body)
    path.write_text(json.dumps(body))


# ---------------------------------------------------------------------------
# Break helpers for what fixture data can't express (design Phase 2, item 2)
# ---------------------------------------------------------------------------


def rewrite_json(
    monkeypatch: pytest.MonkeyPatch, method: str, route: str, change: Callable[[Any], Any]
) -> None:
    """Serve `change(body)` in place of every 2xx JSON body for `method route`."""
    _rewrite(
        monkeypatch,
        method,
        route,
        lambda status, body: (status, change(body) if 200 <= status < 300 else body),
    )


def answer_with_status(
    monkeypatch: pytest.MonkeyPatch, method: str, route: str, status: int
) -> None:
    """Answer every `method route` request with `status`, as a removed route or method does."""
    _rewrite(monkeypatch, method, route, lambda _status, _body: (status, {"detail": "test"}))


def _rewrite(
    monkeypatch: pytest.MonkeyPatch,
    method: str,
    route: str,
    change: Callable[[int, Any], tuple[int, Any]],
) -> None:
    """Wrap every app `create_app` builds in ASGI middleware that changes one route's response."""
    pattern = "/".join(
        "[^/]+" if part.startswith("{") else re.escape(part) for part in route.split("/")
    )
    create_app = server_module.create_app

    def changed(app: ASGIApp) -> ASGIApp:
        async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
            if scope["type"] != "http" or scope["method"] != method:
                return await app(scope, receive, send)
            if not re.fullmatch(pattern, scope["path"]):
                return await app(scope, receive, send)
            messages: list[Message] = []

            async def keep(message: Message) -> None:
                messages.append(message)

            await app(scope, receive, keep)
            start, chunks = messages[0], [m.get("body", b"") for m in messages[1:]]
            status, body = change(start["status"], json.loads(b"".join(chunks)))
            payload = json.dumps(body).encode()
            headers = [
                (name, value)
                for name, value in start["headers"]
                if name.lower() not in (b"content-length", b"content-type")
            ]
            headers += [
                (b"content-type", b"application/json"),
                (b"content-length", b"%d" % len(payload)),
            ]
            await send({"type": "http.response.start", "status": status, "headers": headers})
            await send({"type": "http.response.body", "body": payload})

        return middleware

    monkeypatch.setattr(server_module, "create_app", lambda base_dir: changed(create_app(base_dir)))


# ---------------------------------------------------------------------------
# Core (Phase 1)
# ---------------------------------------------------------------------------


@pytest.fixture
def recorded_text(fixture_root: Path) -> str:
    return record_in_process(fixture_root).read_text()


def test_flatten_kinds_and_containers() -> None:
    body = {"a": 1, "b": True, "c": None, "d": [], "m": {"x": {"v": 1.5}}, "r": [{"k": "s"}, {}]}
    s = c.flatten([body], map_paths={".m"})
    assert s[".a"] == {"number"} and s[".b"] == {"boolean"}  # bool tested before int
    assert s[".c"] == {"null"} and s[".d"] == {"empty"}
    assert s[".m{*}.v"] == {"number"}  # map recorded by value shape
    assert s[".r[].k"] == {"string", "absent"}  # union over elements


def test_contract_text_is_deterministic(recorded_text: str) -> None:
    assert c.render(c.parse(recorded_text)) == recorded_text


def test_page_sliders_follow_the_tornado_rules() -> None:
    def entry(elasticity: float) -> dict[str, float]:
        return {"elasticity": elasticity, "baseline": 0.0}

    engineering = {f"e{i}": entry(i) for i in range(16)}
    engineering["shared"] = entry(0.5)
    metadata = {name: {"range": [0.0, 10.0], "baseline": 2.0} for name in engineering}
    # No finite baseline: the slider starts at range[0]. High == low: no slider.
    metadata["e15"] = {"range": [0.0, 10.0], "baseline": None}
    metadata["e14"] = {"range": [5.0, 5.0], "baseline": 5.0}
    concept = {
        "model_type": "costingfe",
        "has_sensitivities": True,
        "cost_model": {
            "sensitivities": {"engineering": engineering, "financial": {"shared": entry(-20.0)}}
        },
        "parameter_metadata": metadata,
    }
    sliders = c.page_sliders(concept)
    # Top 15 by |elasticity|: "shared" (|-20|, the financial entry wins) then e15..e2.
    assert list(sliders) == ["shared", "e15", *[f"e{i}" for i in range(13, 1, -1)]]
    assert sliders["e15"] == 0.0 and sliders["shared"] == 2.0
    assert c.page_sliders({**concept, "model_type": "standalone"}) == {}


# ---------------------------------------------------------------------------
# Machinery
# ---------------------------------------------------------------------------


def test_every_request_list_entry_yields_an_instance(fixture_root: Path) -> None:
    with c.serve(fixture_root / c.EXPLORER) as client:
        observation = c.observe(client, ["01", "04", "05"])
        preflights = c.preflight(client)
    assert set(observation) == set(c.REQUESTS)
    statuses = {t: {r.status for r in rs} for t, rs in {**observation, **preflights}.items()}
    assert statuses == {template: {200} for template in [*c.REQUESTS, *c.PREFLIGHTS]}
    coverage = c.coverage_sets(observation)
    # Narrower than the concept set, so a coverage loss is distinguishable.
    assert coverage == {c.FINDINGS: {"04"}, c.SLIDER: {"04", "05"}, c.TOGGLE: {"04"}}


def test_unchanged_server_passes_its_own_recording(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run = run_check(fixture_root, record_in_process(fixture_root), capsys)
    assert (run.code, run.failed) == (0, set())


# ---------------------------------------------------------------------------
# Breaks that must fail (spec criterion 1)
# ---------------------------------------------------------------------------


def _drop_name(body: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in body.items() if key != "name"}


def _rename_family(body: dict[str, Any]) -> dict[str, Any]:
    renamed = {**body, "family": body["confinement_family"]}
    del renamed["confinement_family"]
    return renamed


def _lcoe_as_string(body: dict[str, Any]) -> dict[str, Any]:
    for entry in body["concepts"]:
        if entry["lcoe_per_mwh"] is not None:
            entry["lcoe_per_mwh"] = str(entry["lcoe_per_mwh"])
    return body


def _rename_status(body: dict[str, Any]) -> dict[str, Any]:
    for entry in body["concepts"]:
        entry["status"] = entry["status"].replace("approved", "complete")
    return body


@pytest.mark.parametrize(
    ("route", "change", "key"),
    [
        pytest.param(
            "/api/concepts/{id}", _drop_name, "shape GET /api/concepts/{id} .name", id="removed"
        ),
        pytest.param(
            "/api/concepts/{id}",
            _rename_family,
            "shape GET /api/concepts/{id} .confinement_family",
            id="renamed",
        ),
        pytest.param(
            "/api/manifest",
            _lcoe_as_string,
            "shape GET /api/manifest .concepts[].lcoe_per_mwh",
            id="number-to-string",
        ),
        pytest.param(
            "/api/manifest",
            _rename_status,
            "enum GET /api/manifest .concepts[].status",
            id="enum-value-renamed",
        ),
    ],
)
def test_response_field_breaks_fail(
    fixture_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    route: str,
    change: Callable[[Any], Any],
    key: str,
) -> None:
    contract_path = record_in_process(fixture_root)
    rewrite_json(monkeypatch, "GET", route, change)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert key in run.failed


def test_required_value_turned_null_fails(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    rewrite_json(
        monkeypatch, "GET", "/api/concepts/{id}", lambda body: {**body, "confinement_family": None}
    )
    code = c.main(["check", "--tree", str(fixture_root), "--contract", str(contract_path)])
    assert code != 0
    assert "shape GET /api/concepts/{id} .confinement_family" in capsys.readouterr().out


def test_always_null_field_carrying_data_is_unpopulated_only(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    narrative = NarrativeData(
        key_bets=["a bet"], eliminated_costs=[], novel_costs=[], risks=[{"severity": "High"}]
    )
    edit_json(
        fixture_root / DATA / "04.json",
        lambda body: body.update(narrative=narrative.model_dump()),
    )
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert run.failed == {"unpopulated GET /api/concepts/{id} .narrative"}  # never also Shape (N3)


def test_fit_grade_outside_the_pinned_palette_fails(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    table = fixture_root / FIT_TABLE
    table.write_text(table.read_text().replace("04-fake,Med", "04-fake,Medium"))
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert run.failed == {
        "literal GET /api/manifest .concepts[].fit_grade",
        "literal GET /api/concepts/{id} .fit_grade",
    }


@pytest.mark.parametrize(
    ("method", "route", "status", "keys"),
    [
        pytest.param(
            "GET",
            "/api/cost-landscape",
            404,
            {"status GET /api/cost-landscape"},
            id="route-removed",
        ),
        pytest.param(
            "POST",
            "/api/state",
            405,
            {"status POST /api/state:concept", "status POST /api/state:compare"},
            id="post-turned-into-put",
        ),
    ],
)
def test_request_breaks_fail(
    fixture_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    method: str,
    route: str,
    status: int,
    keys: set[str],
) -> None:
    contract_path = record_in_process(fixture_root)
    answer_with_status(monkeypatch, method, route, status)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert keys <= run.failed


class _ComputeRequestWithRequiredField(ComputeRequest):
    scenario: str  # the pinned frontend never sends it


class _StateRejectingNullConcept(ExplorerState):
    current_concept_id: str  # the compare page sends null


class _StateRejectingEmptyTimestamp(ExplorerState):
    timestamp: str = Field("set", min_length=1)  # the compare page sends ""


@pytest.mark.parametrize(
    ("name", "model", "key"),
    [
        pytest.param(
            "ComputeRequest",
            _ComputeRequestWithRequiredField,
            "status POST /api/compute:slider 04",
            id="new-required-compute-field",
        ),
        pytest.param(
            "ExplorerState",
            _StateRejectingNullConcept,
            "status POST /api/state:compare",
            id="state-rejects-null-concept",
        ),
        pytest.param(
            "ExplorerState",
            _StateRejectingEmptyTimestamp,
            "status POST /api/state:compare",
            id="state-rejects-empty-timestamp",
        ),
    ],
)
def test_request_model_breaks_fail(
    fixture_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    name: str,
    model: type,
    key: str,
) -> None:
    contract_path = record_in_process(fixture_root)
    # The routes resolve their string annotations from the server module when
    # create_app registers them, so a stricter model there yields a real 422.
    monkeypatch.setattr(server_module, name, model)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert key in run.failed


def test_omitted_concept_fails(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    omit_list = fixture_root.parent / "omit_05.yaml"
    omit_list.write_text('"05": "test"\n')
    monkeypatch.setattr(models_module, "_OMIT_LIST_PATH", omit_list)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert {f"concept-missing {name} 05" for name in c.JOINED_LISTS} <= run.failed


def _drop_05_from_registry(body: dict[str, Any]) -> None:
    body["concepts"] = [entry for entry in body["concepts"] if entry["concept_id"] != "05"]


def _drop_05_from_tree(body: dict[str, Any]) -> None:
    body["root"]["children"][0]["children"][1]["concepts"] = []


@pytest.mark.parametrize(
    ("file", "change", "key"),
    [
        pytest.param(
            "concept_registry.json",
            _drop_05_from_registry,
            "concept-missing registry 05",
            id="registry",
        ),
        pytest.param(
            "decision_tree.json", _drop_05_from_tree, "concept-missing tree 05", id="tree"
        ),
    ],
)
def test_concept_dropped_from_one_joined_list_fails(
    fixture_root: Path,
    capsys: pytest.CaptureFixture[str],
    file: str,
    change: Callable[[Any], None],
    key: str,
) -> None:
    contract_path = record_in_process(fixture_root)
    edit_json(fixture_root / DATA / file, change)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert key in run.failed


def _null_05_sensitivities(root: Path) -> None:
    edit_json(root / DATA / "05.json", lambda body: body["cost_model"].update(sensitivities=None))


def _no_04_overrides(root: Path) -> None:
    edit_json(root / DATA / "04.json", lambda body: body.update(analyst_override_count=0))


def _no_04_analysis(root: Path) -> None:
    (root / ANALYSES / "04-fake" / "analysis.md").unlink()


@pytest.mark.parametrize(
    ("change", "key"),
    [
        pytest.param(_null_05_sensitivities, "coverage POST /api/compute:slider 05", id="sliders"),
        pytest.param(_no_04_overrides, "coverage POST /api/compute:toggle 04", id="toggle"),
        pytest.param(_no_04_analysis, "coverage GET /api/concepts/{id}/findings 04", id="findings"),
    ],
)
def test_lost_feature_fails_coverage(
    fixture_root: Path,
    capsys: pytest.CaptureFixture[str],
    change: Callable[[Path], None],
    key: str,
) -> None:
    contract_path = record_in_process(fixture_root)
    change(fixture_root)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert key in run.failed


def _add_concept_40(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Serve a new concept 40 the way a real one arrives: data, a fit row, a company entry."""
    concept = json.loads((root / DATA / "05.json").read_text())
    (root / DATA / "40.json").write_text(json.dumps({**concept, "concept_id": "40"}))
    with (root / FIT_TABLE).open("a") as table:
        table.write("40-fake,Low\n")
    monkeypatch.setitem(server_module._COMPANIES, "40", ("Fake Co", "https://example.com"))


def test_unlisted_concept_fails(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    _add_concept_40(fixture_root, monkeypatch)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert run.failed == {"concept-unlisted manifest 40", "concept-unlisted parameters/{name} 40"}


class _StaticOnlyCorsApp(FastAPI):
    """The explorer app with https://1cf.energy dropped from the CORS allowlist."""

    def build_middleware_stack(self) -> ASGIApp:
        return CORSMiddleware(
            super().build_middleware_stack(),
            allow_origins=["https://static.1cf.energy"],
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type"],
        )


def test_website_origin_dropped_from_cors_fails(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    monkeypatch.setattr(server_module, "_ExplorerApp", _StaticOnlyCorsApp)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert run.failed == {f"cors {t}" for t in [*c.REQUESTS, *c.PREFLIGHTS]}


# ---------------------------------------------------------------------------
# Changes that must pass (spec criterion 2)
# ---------------------------------------------------------------------------


class _ComputeRequestWithOptionalField(ComputeRequest):
    scenario: str | None = None


def _add_cas22_account(root: Path) -> None:
    def change(body: dict[str, Any]) -> None:
        body["cost_model"]["cas22_detail"]["C220102"] = {"name": "New", "cost_m_usd": 2.0}

    edit_json(root / DATA / "04.json", change)


def _drop_availability_from_05(root: Path) -> None:
    def change(body: dict[str, Any]) -> None:
        for group in ("sensitivities", "sensitivities_bare"):
            del body["cost_model"][group]["engineering"]["availability"]
        del body["parameter_metadata"]["availability"]

    edit_json(root / DATA / "05.json", change)


def _new_response_field(monkeypatch: pytest.MonkeyPatch) -> None:
    rewrite_json(monkeypatch, "GET", "/api/concepts/{id}", lambda body: {**body, "new_field": 1})


def _new_optional_request_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server_module, "ComputeRequest", _ComputeRequestWithOptionalField)


@pytest.mark.parametrize(
    ("data_change", "server_change"),
    [
        pytest.param(None, _new_response_field, id="new-response-field"),
        pytest.param(None, _new_optional_request_field, id="new-optional-request-field"),
        pytest.param(_add_cas22_account, None, id="new-map-key"),
        pytest.param(_drop_availability_from_05, None, id="concept-leaves-a-parameter"),
    ],
)
def test_additive_change_passes(
    fixture_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    data_change: Callable[[Path], None] | None,
    server_change: Callable[[pytest.MonkeyPatch], None] | None,
) -> None:
    contract_path = record_in_process(fixture_root)
    if data_change is not None:
        data_change(fixture_root)
    if server_change is not None:
        server_change(monkeypatch)
    run = run_check(fixture_root, contract_path, capsys)
    assert (run.code, run.failed) == (0, set())


def test_new_concept_with_a_waiver_passes(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    _add_concept_40(fixture_root, monkeypatch)
    run = run_check(fixture_root, contract_path, capsys, waiver("concept-unlisted * 40"))
    assert (run.code, run.failed) == (0, set())
    assert run.waived == {"concept-unlisted manifest 40", "concept-unlisted parameters/{name} 40"}


# ---------------------------------------------------------------------------
# Waivers (design D7, Appendix E)
# ---------------------------------------------------------------------------


def test_a_waiver_clears_exactly_its_key(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    table = fixture_root / FIT_TABLE
    table.write_text(table.read_text().replace("04-fake,Med", "04-fake,Medium"))
    run = run_check(
        fixture_root,
        contract_path,
        capsys,
        waiver("literal GET /api/manifest .concepts[].fit_grade"),
    )
    assert run.code == c.EXIT_FAILED
    assert run.waived == {"literal GET /api/manifest .concepts[].fit_grade"}
    assert run.failed == {"literal GET /api/concepts/{id} .fit_grade"}


def test_a_stale_waiver_warns_and_passes(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run = run_check(
        fixture_root, record_in_process(fixture_root), capsys, waiver("concept-unlisted * 40")
    )
    assert (run.code, run.failed) == (0, set())
    assert run.lines("STALE") == {"concept-unlisted * 40"}


@pytest.mark.parametrize(
    "entry",
    [
        pytest.param(
            waiver("status GET /api/manifest").replace('reason = "fixture"\n', ""), id="no-reason"
        ),
        pytest.param(waiver("status GET /api/manifest", evidence=" "), id="empty-evidence"),
        pytest.param(
            waiver("status GET /api/manifest").replace("date = 2026-10-08\n", ""), id="no-date"
        ),
        pytest.param(waiver("status GET /api/manifest") + 'note = "x"\n', id="unknown-field"),
        pytest.param(waiver("shape GET /api/concepts/{id} .cost_model.cas*"), id="partial-glob"),
        pytest.param(waiver("* GET /api/manifest"), id="wildcard-rule"),
        pytest.param(
            waiver("unpopulated GET /api/concepts/{id} .narrative", "read it"),
            id="unpopulated-no-cite",
        ),
    ],
)
def test_a_malformed_waiver_is_a_configuration_error(
    fixture_root: Path, capsys: pytest.CaptureFixture[str], entry: str
) -> None:
    contract_path = record_in_process(fixture_root)
    run = run_check(fixture_root, contract_path, capsys, entry)
    assert run.code == c.EXIT_CONFIG
    assert run.out.startswith("configuration error")


@pytest.mark.parametrize(
    "evidence",
    [
        pytest.param("concept_page.js:318 lowercases each risk severity", id="js-cite"),
        pytest.param(
            "unread: narrative risks severity (git grep, pinned static/js)", id="unread-terms"
        ),
    ],
)
def test_an_unpopulated_waiver_with_evidence_clears_its_key(
    fixture_root: Path, capsys: pytest.CaptureFixture[str], evidence: str
) -> None:
    contract_path = record_in_process(fixture_root)
    narrative = NarrativeData(key_bets=[], eliminated_costs=[], novel_costs=[], risks=[])
    edit_json(
        fixture_root / DATA / "04.json", lambda body: body.update(narrative=narrative.model_dump())
    )
    run = run_check(
        fixture_root,
        contract_path,
        capsys,
        waiver("unpopulated GET /api/concepts/{id} .narrative", evidence),
    )
    assert (run.code, run.waived) == (0, {"unpopulated GET /api/concepts/{id} .narrative"})


def test_cors_failures_ignore_waivers(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    monkeypatch.setattr(server_module, "_ExplorerApp", _StaticOnlyCorsApp)
    run = run_check(fixture_root, contract_path, capsys, waiver("cors GET /api/manifest"))
    assert run.code == c.EXIT_FAILED
    assert "cors GET /api/manifest" in run.failed and run.waived == set()


@pytest.mark.parametrize(
    ("match", "key", "matches"),
    [
        (
            "shape GET /api/concepts/{id} .cost_model.*.cost_m_usd",
            "shape GET /api/concepts/{id} .cost_model.cas10.cost_m_usd",
            True,
        ),
        # One whole segment, its {*} or [] included.
        (
            "shape GET /api/concepts/{id} .cost_model.*.cost_m_usd",
            "shape GET /api/concepts/{id} .cost_model.cas22_detail{*}.cost_m_usd",
            True,
        ),
        (
            "shape GET /api/concepts/{id} .cost_model.*.cost_m_usd",
            "shape GET /api/concepts/{id} .cost_model.a.b.cost_m_usd",
            False,
        ),
        (
            "shape GET /api/concepts/{id} .cost_model.params{*}",
            "shape GET /api/concepts/{id} .cost_model.params{*}",
            True,
        ),
        (
            "shape GET /api/concepts/{id} .cost_model.params{*}",
            "shape GET /api/concepts/{id} .cost_model.paramsX",
            False,
        ),
        ("status POST /api/compute:slider *", "status POST /api/compute:slider 05", True),
        ("status POST /api/compute:slider *", "status POST /api/compute:slider", False),
    ],
)
def test_waiver_wildcards_match_one_whole_token_or_segment(
    match: str, key: str, matches: bool
) -> None:
    assert c.waiver_matches(match, key) is matches
