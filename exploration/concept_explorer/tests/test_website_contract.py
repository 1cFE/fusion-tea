"""Self-tests for the website contract gate (exploration/concept_explorer/website_contract).

These run inside the gate. Most use a small repo-shaped fixture: three concepts with
sensitivities, an analyst override, a taxonomy registry and tree, findings text and
archetype-fit grades, served by the fake costing model from test_state_and_compute.py.
The fixture is a committed git repository with a .dockerignore, so the Files rule judges
it as it judges the real tree. Each break test records a
contract from the unbroken fixture, makes one change, and runs the gate's own `check`
entry point (design Appendix D).
"""

from __future__ import annotations

import datetime
import importlib.metadata
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import pytest
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, create_model
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

# The gate's modules import each other as top-level modules, the way contract.py runs them.
WEBSITE_CONTRACT = Path(__file__).resolve().parents[1] / "website_contract"
sys.path.insert(0, str(WEBSITE_CONTRACT))

import contract as c  # noqa: E402
import drift  # noqa: E402
import file_audit  # noqa: E402
import frontend_requests as fr  # noqa: E402
from contract_rules import record_tree  # noqa: E402
from contract_text import parse, render  # noqa: E402
from json_shapes import flatten  # noqa: E402
from pin_source import SERVING_SET, cite_errors, extract, js_blobs  # noqa: E402
from waivers import Verdict, Waiver, apply_waivers, waiver_matches  # noqa: E402

PIN = "0" * 40
CHECKOUT = c.REPO_ROOT  # this checkout; its static/js equals the pin's

# ---------------------------------------------------------------------------
# The fixture: a repo root laid out as <root>/exploration/..., so the server's
# sibling-tree lookups (analyses, tables, archive) resolve inside it.
# ---------------------------------------------------------------------------

DATA = fr.EXPLORER / "data"
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


# The fixture's build-context rules, in the shape of the repo's .dockerignore. A fixed
# copy, so editing the real file can fail the gate's Files rule but never these tests.
_FIXTURE_DOCKERIGNORE = """\
.git
knowledge
archive/*
!archive/concept_analysis_pre_rework
**/iter-*/
**/__pycache__/
*.pyc
"""


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
    (root / fr.EXPLORER / "omit_list.yaml").write_text("{}\n")

    (root / ANALYSES / "04-fake").mkdir(parents=True)
    (root / ANALYSES / "04-fake" / "model_setup.py").write_text(
        compute_tests._FAKE_MODULE_PY + _ANALYST_OVERRIDES_PY
    )
    (root / ANALYSES / "04-fake" / "analysis.md").write_text("# Findings\n\nWhat 04 found.\n")
    (root / ANALYSES / "05-fake").mkdir()
    (root / ANALYSES / "05-fake" / "model_setup.py").write_text(compute_tests._FAKE_MODULE_PY)
    (root / FIT_TABLE).parent.mkdir(parents=True)
    (root / FIT_TABLE).write_text("concept_id,fit_grade\n01-fake,High\n04-fake,Med\n05-fake,None\n")
    (root / file_audit.DOCKERIGNORE).write_text(_FIXTURE_DOCKERIGNORE)


def git(repo: Path, *args: str) -> str:
    """Run git in `repo` without the user's hooks or commit signing."""
    command = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t"]
    command += ["-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args]
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout.strip()


def commit_all(repo: Path, message: str) -> str:
    """Commit everything in `repo`, creating the repository if needed; return the SHA."""
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def fixture_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "repo"
    build_fixture(root)
    commit_all(root, "fixture")  # the Files rule judges paths tracked at HEAD
    monkeypatch.setattr(models_module, "_OMIT_LIST_PATH", root / fr.EXPLORER / "omit_list.yaml")
    monkeypatch.setenv("EXPLORER_SKIP_WARMUP", "1")
    monkeypatch.setattr(sys, "path", list(sys.path))  # `check` puts its tree first
    return root


def record_in_process(root: Path) -> Path:
    """Record the fixture's contract in this process (N7) and return the file's path."""
    path = root.parent / "contract.txt"
    path.write_text(render(record_tree(root, PIN, tools=[], js={})))
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
    s = flatten([body], map_paths={".m"})
    assert s[".a"] == {"number"} and s[".b"] == {"boolean"}  # bool tested before int
    assert s[".c"] == {"null"} and s[".d"] == {"empty"}
    assert s[".m{*}.v"] == {"number"}  # map recorded by value shape
    assert s[".r[].k"] == {"string", "absent"}  # union over elements


def test_contract_text_is_deterministic(recorded_text: str) -> None:
    assert render(parse(recorded_text)) == recorded_text


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
    sliders = fr.page_sliders(concept)
    # Top 15 by |elasticity|: "shared" (|-20|, the financial entry wins) then e15..e2.
    assert list(sliders) == ["shared", "e15", *[f"e{i}" for i in range(13, 1, -1)]]
    assert sliders["e15"] == 0.0 and sliders["shared"] == 2.0
    assert fr.page_sliders({**concept, "model_type": "standalone"}) == {}


# ---------------------------------------------------------------------------
# Machinery
# ---------------------------------------------------------------------------


def test_every_request_list_entry_yields_an_instance(fixture_root: Path) -> None:
    with fr.serve(fixture_root / fr.EXPLORER) as client:
        observation = fr.observe(client, ["01", "04", "05"])
        preflights = fr.preflight(client)
    assert set(observation) == set(fr.REQUESTS)
    statuses = {t: {r.status for r in rs} for t, rs in {**observation, **preflights}.items()}
    assert statuses == {template: {200} for template in [*fr.REQUESTS, *fr.PREFLIGHTS]}
    coverage = fr.coverage_sets(observation)
    # Narrower than the concept set, so a coverage loss is distinguishable.
    assert coverage == {fr.FINDINGS: {"04"}, fr.SLIDER: {"04", "05"}, fr.TOGGLE: {"04"}}


def test_unchanged_server_passes_its_own_recording(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run = run_check(fixture_root, record_in_process(fixture_root), capsys)
    assert (run.code, run.failed) == (0, set())


def test_no_gate_module_shadows_a_module_the_server_imports() -> None:
    """contract.py puts its directory on sys.path, and a module imported once is shared, so
    a gate module named like the standard library, an installed package, the server's
    `exploration` package or a concept-analysis helper would change the server under test."""
    gate_modules = {path.stem for path in WEBSITE_CONTRACT.glob("*.py")}
    helpers = CHECKOUT / "exploration/concept_analysis/scripts"
    taken = set(sys.stdlib_module_names) | set(importlib.metadata.packages_distributions())
    taken |= {path.stem for path in helpers.iterdir()} | {"exploration"}
    assert gate_modules >= {"contract", "frontend_requests"} and not gate_modules & taken


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


def test_a_template_with_no_200_left_fails_status(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Plan decision 8: where the pin also saw a status the website tolerates, such as a
    bare-only parameter's 404, every instance answering it still fails, as a removed route
    would. This fixture's pin saw only 200, so the recording gains the 404 here."""
    contract_path = record_in_process(fixture_root)
    contract = parse(contract_path.read_text())
    contract = replace(contract, status={**contract.status, fr.PARAMETER: (200, 404)})
    contract_path.write_text(render(contract))
    answer_with_status(monkeypatch, "GET", "/api/parameters/{name}", 404)
    run = run_check(fixture_root, contract_path, capsys)
    assert (run.code, run.failed) == (c.EXIT_FAILED, {f"status {fr.PARAMETER}"})


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


def _with_field_renamed(model: type[BaseModel], old: str, new: str) -> type[BaseModel]:
    """`model` with field `old` renamed to an optional `new`, keeping any default it had.

    Pydantic ignores the old name the pinned frontend still sends. The server's own code
    reads the new name through the old attribute, as a real rename would update it."""
    fields: dict[str, Any] = {
        name: (info.annotation, info) for name, info in model.model_fields.items()
    }
    annotation, info = fields.pop(old)
    fields[new] = (annotation | None, None if info.is_required() else info)
    renamed = create_model(model.__name__, **fields)
    setattr(renamed, old, property(lambda self: getattr(self, new)))
    return renamed


_COMPUTE_TEMPLATES = (fr.SLIDER, fr.SLIDER_RANGE, fr.TOGGLE)
_STATE_TEMPLATES = (fr.STATE_CONCEPT, fr.STATE_COMPARE)


@pytest.mark.parametrize(
    ("name", "field", "templates"),
    [
        pytest.param("ComputeRequest", "concept_id", _COMPUTE_TEMPLATES, id="compute-concept_id"),
        pytest.param("ComputeRequest", "overrides", _COMPUTE_TEMPLATES, id="compute-overrides"),
        pytest.param(
            "ComputeRequest",
            "apply_analyst_overrides",
            _COMPUTE_TEMPLATES,
            id="compute-apply_analyst_overrides",
        ),
        pytest.param(
            "ExplorerState", "current_concept_id", _STATE_TEMPLATES, id="state-current_concept_id"
        ),
        pytest.param(
            "ExplorerState", "slider_overrides", _STATE_TEMPLATES, id="state-slider_overrides"
        ),
        pytest.param(
            "ExplorerState", "comparison_set", _STATE_TEMPLATES, id="state-comparison_set"
        ),
        pytest.param("ExplorerState", "timestamp", (fr.STATE_COMPARE,), id="state-timestamp"),
    ],
)
def test_a_renamed_request_field_fails(
    fixture_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    name: str,
    field: str,
    templates: tuple[str, ...],
) -> None:
    """Audit B1: the server accepts the request but no longer reads a field the website sends."""
    contract_path = record_in_process(fixture_root)
    renamed = _with_field_renamed(getattr(models_module, name), field, f"renamed_{field}")
    monkeypatch.setattr(server_module, name, renamed)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert {f"request-field {template} {field}" for template in templates} <= run.failed


def test_omitted_concept_fails(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    omit_list = fixture_root.parent / "omit_05.yaml"
    omit_list.write_text('"05": "test"\n')
    monkeypatch.setattr(models_module, "_OMIT_LIST_PATH", omit_list)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert {f"concept-missing {name} 05" for name in fr.JOINED_LISTS} <= run.failed


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
    assert run.failed == {f"cors {t}" for t in [*fr.REQUESTS, *fr.PREFLIGHTS]}


class _PostRefusingCorsApp(FastAPI):
    """The explorer app still allowing https://1cf.energy, but not POST. Each preflight
    answers 400 and still carries the origin header, so only its status shows it."""

    def build_middleware_stack(self) -> ASGIApp:
        return CORSMiddleware(
            super().build_middleware_stack(),
            allow_origins=["https://1cf.energy"],
            allow_methods=["GET"],
            allow_headers=["Content-Type"],
        )


def test_a_refused_preflight_fails_cors(
    fixture_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    monkeypatch.setattr(server_module, "_ExplorerApp", _PostRefusingCorsApp)
    run = run_check(fixture_root, contract_path, capsys)
    assert (run.code, run.failed) == (c.EXIT_FAILED, {f"cors {t}" for t in fr.PREFLIGHTS})


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


def _add_unwritable_tree_key(root: Path) -> None:
    """A key with a space in the untyped tree, which takes its keys from data (audit A2)."""
    edit_json(root / DATA / "decision_tree.json", lambda body: body["root"].update({"a b": "c"}))


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
        pytest.param(_add_unwritable_tree_key, None, id="new-key-that-cannot-be-a-path"),
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


def test_recording_fails_on_a_key_that_cannot_be_a_path(fixture_root: Path) -> None:
    """The contract can't hold such a key, so recording stops rather than drop it."""
    _add_unwritable_tree_key(fixture_root)
    with pytest.raises(ValueError, match=r"can't be written as paths: 'a b' under \.root\."):
        record_in_process(fixture_root)


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


@pytest.mark.parametrize(
    ("match", "fix"),
    [
        pytest.param("cors GET /api/manifest", "CORS allowlist", id="cors"),
        pytest.param(
            f"files missing {FIT_TABLE}", "runtime_paths.txt or .dockerignore", id="files"
        ),
    ],
)
def test_a_cors_or_files_waiver_is_a_configuration_error(
    fixture_root: Path, capsys: pytest.CaptureFixture[str], match: str, fix: str
) -> None:
    run = run_check(fixture_root, record_in_process(fixture_root), capsys, waiver(match))
    assert run.code == c.EXIT_CONFIG
    assert "can't be waived" in run.out and fix in run.out


def test_cors_and_files_keys_are_never_waived() -> None:
    keys = ("cors GET /api/manifest", f"files missing {FIT_TABLE}")
    waivers = [Waiver(key, "fixture", "fixture", datetime.date(2026, 10, 8)) for key in keys]
    assert apply_waivers(keys, waivers) == Verdict(failing=keys, waived=(), stale=tuple(waivers))


@pytest.mark.parametrize(
    ("failing", "hint"),
    [
        pytest.param(("cors GET /api/manifest", "files missing x"), False, id="unwaivable-only"),
        pytest.param(("cors GET /api/manifest", "shape GET /api/manifest .x"), True, id="waivable"),
    ],
)
def test_the_waiver_hint_prints_only_for_a_waivable_failure(
    failing: tuple[str, ...], hint: bool
) -> None:
    out = c.report(Verdict(failing=failing, waived=(), stale=()), PIN)
    assert ("[[waiver]]" in out) is hint


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
    assert waiver_matches(match, key) is matches


# ---------------------------------------------------------------------------
# Recording at the pin: purity (I1), the cited JavaScript (I2, M5), Appendix B
# ---------------------------------------------------------------------------


@pytest.fixture
def two_commit_repo(tmp_path: Path) -> tuple[Path, str, str]:
    """A: the fixture plus this checkout's explorer code, static/js and serving set. B: A
    with 05 dropped from the registry. The explorer code makes record import the
    extract's own server (decision 11); the static/js makes the real cites resolve."""
    repo = tmp_path / "repo"
    build_fixture(repo)
    for source in (CHECKOUT / fr.EXPLORER).glob("*.py"):
        shutil.copy(source, repo / fr.EXPLORER / source.name)
    shutil.copytree(CHECKOUT / fr.STATIC_JS, repo / fr.STATIC_JS)
    shutil.copy(CHECKOUT / SERVING_SET, repo / SERVING_SET)
    a = commit_all(repo, "A")
    edit_json(repo / DATA / "concept_registry.json", _drop_05_from_registry)
    git(repo, "commit", "-q", "-am", "B: 05 leaves the registry")
    return repo, a, git(repo, "rev-parse", "HEAD")


def _contract_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """`contract.py` in a `python -I -B` subprocess of this venv, as gate.sh runs it (N7)."""
    command = [sys.executable, "-I", "-B", str(Path(c.__file__)), *args]
    return subprocess.run(command, capture_output=True, text=True, timeout=300)


def _extracted(repo: Path, sha: str) -> Path:
    tree = Path(tempfile.mkdtemp(dir=repo.parent)) / "tree"
    extract(repo, sha, tree)
    return tree


def record_extract(
    repo: Path, sha: str, tree: Path, contract_path: Path, *flags: str
) -> subprocess.CompletedProcess[str]:
    """`contract.py record` on `tree`, an extract of commit `sha` in `repo`."""
    argv = ["record", "--tree", str(tree), "--pin", sha, "--repo", str(repo)]
    return _contract_cli(*argv, "--contract", str(contract_path), *flags)


def record_from_git(
    repo: Path, sha: str, contract_path: Path, *flags: str
) -> subprocess.CompletedProcess[str]:
    return record_extract(repo, sha, _extracted(repo, sha), contract_path, *flags)


def check_from_git(repo: Path, sha: str, contract_path: Path) -> subprocess.CompletedProcess[str]:
    """`contract.py check` on a clone of `repo` at `sha`, a checkout as CI has one."""
    clone = Path(tempfile.mkdtemp(dir=repo.parent)) / "clone"
    git(repo.parent, "clone", "-q", str(repo), str(clone))
    git(clone, "checkout", "-q", sha)
    waivers = clone.parent / "waivers.toml"
    waivers.write_text("")
    return _contract_cli(
        "check", "--tree", str(clone), "--contract", str(contract_path), "--waivers", str(waivers)
    )


def test_rerecording_after_a_break_gives_identical_bytes(
    two_commit_repo: tuple[Path, str, str], tmp_path: Path
) -> None:
    repo, a, b = two_commit_repo
    contract_path = tmp_path / "contract.txt"
    first = record_from_git(repo, a, contract_path, "--js-reverified")  # no earlier header
    assert first.returncode == 0, first.stdout + first.stderr
    recorded = contract_path.read_bytes()
    contract = parse(recorded.decode())
    assert (contract.pin, contract.concepts) == (a, ("01", "04", "05"))
    assert contract.js == js_blobs(CHECKOUT)
    checked = check_from_git(repo, b, contract_path)
    assert checked.returncode == c.EXIT_FAILED, checked.stdout + checked.stderr
    assert "FAIL concept-missing registry 05" in checked.stdout.splitlines()
    again = record_from_git(repo, a, contract_path)  # the header now matches: no flag needed
    assert again.returncode == 0, again.stdout + again.stderr
    assert contract_path.read_bytes() == recorded


def test_committed_map_paths_trace_to_appendix_b() -> None:
    """Every {*} path in contract.txt is a field Appendix B declares dict[str, X]."""
    cost_model = {
        ".sensitivities.engineering",  # SensitivityAnalysis.engineering, models.py:125
        ".sensitivities.financial",  # .financial, models.py:126
        ".sensitivities_bare.engineering",
        ".sensitivities_bare.financial",
        ".cas22_detail",  # CostModelData.cas22_detail, models.py:163
        ".params",  # CostModelData.params, models.py:174
    }
    expected = {(fr.CONCEPT, ".cost_model" + path) for path in cost_model}
    expected |= {(t, path) for t in (fr.SLIDER, fr.SLIDER_RANGE, fr.TOGGLE) for path in cost_model}
    expected.add((fr.CONCEPT, ".parameter_metadata"))  # ConceptData, models.py:483
    expected.add((fr.PARAMETER_INDEX, ".parameters"))  # ParameterIndex, models.py:594
    # The POST /api/state response is declared dict[str, str] (server.py:851).
    expected |= {(fr.STATE_CONCEPT, "."), (fr.STATE_COMPARE, ".")}
    assert set(parse(c.CONTRACT_PATH.read_text()).maps) == expected


def _frontend_copy(tmp_path: Path) -> Path:
    """A repo-shaped tree holding a copy of this checkout's static/js."""
    tree = tmp_path / "tree"
    shutil.copytree(CHECKOUT / fr.STATIC_JS, tree / fr.STATIC_JS)
    return tree


def test_an_uncited_fetch_fails_recording(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    tree = _frontend_copy(tmp_path)
    assert cite_errors(tree) == []  # the cite tables match this checkout's frontend
    page = tree / fr.STATIC_JS / "index_page.js"
    page.write_text(page.read_text() + 'fetch("/api/new");\n')
    lines = len(page.read_text().splitlines())
    argv = ["record", "--tree", str(tree), "--pin", PIN, "--contract", str(tmp_path / "c.txt")]
    assert c.main([*argv, "--js-reverified"]) == c.EXIT_FAILED
    assert f"index_page.js:{lines}: calls fetch( but no request cites it" in capsys.readouterr().out
    assert not (tmp_path / "c.txt").exists()


def _changed_tornado(tree: Path, contract_path: Path) -> None:
    header = [f"pin {PIN}", *(f"js {p} {sha}" for p, sha in sorted(js_blobs(tree).items()))]
    contract_path.write_text("\n".join(header) + "\n")
    tornado = tree / fr.STATIC_JS / "tornado.js"
    tornado.write_text(tornado.read_text() + "// a changed derivation rule\n")


@pytest.mark.parametrize(
    ("setup", "reason"),
    [
        pytest.param(
            _changed_tornado,
            f"{fr.STATIC_JS.as_posix()}/tornado.js: blob changed since the last recording",
            id="changed-blob",
        ),
        pytest.param(
            lambda tree, contract_path: None,
            "no earlier c.txt to compare the cited JavaScript with",
            id="no-earlier-header",
        ),
    ],
)
def test_unverified_javascript_fails_recording_without_the_flag(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    setup: Callable[[Path, Path], None],
    reason: str,
) -> None:
    tree, contract_path = _frontend_copy(tmp_path), tmp_path / "c.txt"
    setup(tree, contract_path)
    before = contract_path.read_text() if contract_path.exists() else None
    argv = ["record", "--tree", str(tree), "--pin", PIN, "--contract", str(contract_path)]
    assert c.main(argv) == c.EXIT_FAILED
    out = capsys.readouterr().out
    assert reason in out.splitlines() and "re-verify Appendix A" in out
    assert (contract_path.read_text() if contract_path.exists() else None) == before


# ---------------------------------------------------------------------------
# The file audit and the Files rule (design D5, D6, Appendix G; decision 10)
# ---------------------------------------------------------------------------

FIT_TABLE_KEY = FIT_TABLE.as_posix()


def test_a_tracked_file_missing_from_the_tree_fails(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    (fixture_root / FIT_TABLE).unlink()  # as if the checkout lacked the tables directory
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert f"files missing {FIT_TABLE_KEY}" in run.failed


def test_dockerignore_excluding_a_touched_path_fails(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    current = (CHECKOUT / file_audit.DOCKERIGNORE).read_text()  # the real file's patterns
    dockerignore = current + "exploration/concept_analysis/tables\n"
    (fixture_root / file_audit.DOCKERIGNORE).write_text(dockerignore)
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_FAILED
    assert f"files dockerignore {FIT_TABLE_KEY}" in run.failed


def test_a_tree_without_heads_dockerignore_fails(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without the file the gate couldn't judge the image, so it doesn't pass."""
    contract_path = record_in_process(fixture_root)
    (fixture_root / file_audit.DOCKERIGNORE).unlink()
    run = run_check(fixture_root, contract_path, capsys)
    assert (run.code, run.failed) == (c.EXIT_FAILED, {"files missing .dockerignore"})


@pytest.mark.parametrize("tracked", [False, True], ids=["untracked", "tracked"])
def test_only_paths_tracked_at_head_count(
    fixture_root: Path, capsys: pytest.CaptureFixture[str], tracked: bool
) -> None:
    """The server reads 04's bytecode cache, which .dockerignore's **/__pycache__/ excludes.
    Untracked, as caches are, it can't fail the gate (decision 10); tracked, it would."""
    source = fixture_root / ANALYSES / "04-fake" / "model_setup.py"
    cache = Path(py_compile.compile(str(source), doraise=True))
    if tracked:
        git(fixture_root, "add", "-f", str(cache))
        git(fixture_root, "commit", "-q", "-m", "a tracked cache")
    contract_path = record_in_process(fixture_root)
    server_module._load_model_module.cache_clear()  # check reads the module afresh, as in the gate
    run = run_check(fixture_root, contract_path, capsys)
    key = f"files dockerignore {cache.relative_to(fixture_root).as_posix()}"
    assert (run.code, run.failed) == ((c.EXIT_FAILED, {key}) if tracked else (0, set()))


def test_an_unsupported_dockerignore_pattern_is_a_configuration_error(
    fixture_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract_path = record_in_process(fixture_root)
    (fixture_root / file_audit.DOCKERIGNORE).write_text("*.py?\n")
    run = run_check(fixture_root, contract_path, capsys)
    assert run.code == c.EXIT_CONFIG
    assert run.out.startswith("configuration error")


def test_matcher_follows_docker_rules() -> None:
    m = file_audit.Matcher(
        ["archive/*", "!archive/concept_analysis_pre_rework", "*.pyc", "**/__pycache__/"]
    )
    assert m.excluded("archive/other/x.md")
    assert not m.excluded("archive/concept_analysis_pre_rework/a/analysis.md")
    assert m.excluded("x.pyc") and not m.excluded("exploration/x.pyc")  # anchored at the root


@pytest.mark.parametrize(
    ("patterns", "path", "excluded"),
    [
        pytest.param(["knowledge"], "knowledge/a/b.md", True, id="a-directory-excludes-its-tree"),
        pytest.param(["knowledge"], "exploration/knowledge", False, id="anchored-at-the-root"),
        pytest.param(["**/__pycache__/"], "__pycache__/m.pyc", True, id="leading-**-at-the-root"),
        pytest.param(["**/__pycache__/"], "a/b/__pycache__/m.pyc", True, id="leading-**-deep"),
        pytest.param(["**/__pycache__/"], "a/my__pycache__/m.pyc", False, id="whole-segment"),
        pytest.param(["**/iter-*/"], "a/iter-3/out.md", True, id="leading-**-with-a-glob"),
        pytest.param(["a/**/t"], "a/b/c/t/f.csv", True, id="inner-**"),
        pytest.param(["a/**"], "a/b", True, id="trailing-**"),
        pytest.param(["a/**"], "ab", False, id="trailing-**-needs-the-directory"),
        pytest.param(["a/*"], "a/b/c", True, id="*-then-parent-match"),
        pytest.param(["a/*.md"], "a/b/c.md", False, id="*-stays-in-one-segment"),
        pytest.param(["a/*", "!a/keep"], "a/keep/x", False, id="!-re-includes"),
        pytest.param(["!a/keep", "a/*"], "a/keep/x", True, id="the-last-match-wins"),
        # BuildKit judges each path with its parent's per-pattern results, and a pattern
        # it skipped at a directory isn't inherited: the third pattern was skipped at
        # `a` (already excluded), so the re-include of `a/b` stands (fsutil filter.go).
        pytest.param(["a", "!a/b", "a"], "a/b/c", False, id="skipped-patterns-not-inherited"),
    ],
)
def test_matcher_cases_from_docker(patterns: list[str], path: str, excluded: bool) -> None:
    assert file_audit.Matcher(patterns).excluded(path) is excluded


@pytest.mark.parametrize("pattern", ["*.py?", "data/[ab].json", "a\\b", "!"])
def test_the_matcher_refuses_syntax_it_does_not_implement(pattern: str) -> None:
    with pytest.raises(file_audit.UnsupportedPattern):
        file_audit.Matcher([pattern])


def test_dockerignore_lines_are_read_as_docker_reads_them() -> None:
    text = "\ufeff# comment\n\n/knowledge/\r\n ! archive/./keep \n  # a pattern\n**/x/\n"
    assert file_audit.dockerignore_patterns(text) == [
        "knowledge",
        "!archive/keep",
        "# a pattern",  # only a line that starts with "#" is a comment
        "**/x",
    ]


def test_tracked_paths_include_directories(fixture_root: Path) -> None:
    tracked = file_audit.tracked_paths(fixture_root, "HEAD")
    assert {FIT_TABLE_KEY, "exploration/concept_analysis/tables", "exploration"} <= tracked
    assert "" not in tracked and "exploration/concept_explorer/dist" not in tracked


def test_recording_fails_when_the_extract_lacks_a_file_the_pin_reads(
    two_commit_repo: tuple[Path, str, str], tmp_path: Path
) -> None:
    repo, a, _ = two_commit_repo
    tree = _extracted(repo, a)
    (tree / FIT_TABLE).unlink()  # as if runtime_paths.txt missed the tables directory
    contract_path = tmp_path / "contract.txt"
    run = record_extract(repo, a, tree, contract_path, "--js-reverified")
    assert run.returncode == c.EXIT_FAILED, run.stdout + run.stderr
    assert f"FAIL files missing {FIT_TABLE_KEY}" in run.stdout.splitlines()
    assert not contract_path.exists()


# ---------------------------------------------------------------------------
# Workflows (I4, I5) and the drift check (D8, Appendix G)
# ---------------------------------------------------------------------------

WORKFLOWS = CHECKOUT / ".github" / "workflows"


def _triggers(workflow: Path) -> dict[str, Any]:
    """A workflow's events by name, each with its filters (None when it has none)."""
    document = yaml.safe_load(workflow.read_text())
    on = document.get("on", document.get(True))  # PyYAML reads the key `on` as True
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return dict.fromkeys(on)
    return dict(on)


def test_the_gate_workflow_has_no_filters() -> None:
    """A skipped run never blocks a deploy, so nothing may skip the gate (I5, D10)."""
    on = _triggers(WORKFLOWS / "website-contract.yml")
    assert set(on) >= {"push", "pull_request", "workflow_dispatch"}
    filters = {"paths", "paths-ignore", "branches", "branches-ignore", "tags", "tags-ignore"}
    assert not set(on["push"] or {}) & filters


def test_the_drift_workflow_never_runs_on_push() -> None:
    """Railway waits on push workflows; drift must never hold a deploy (I5, D8)."""
    assert set(_triggers(WORKFLOWS / "website-pin-drift.yml")) == {"schedule", "workflow_dispatch"}


def test_push_workflows_equal_the_reviewed_list() -> None:
    """Any failing push workflow skips the deploy, so each is reviewed to fail only on
    purpose (I4): the gate fails on a break; notify_visualization.yml can't fail (D11)."""
    workflows = [*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")]
    push = {workflow.name for workflow in workflows if "push" in _triggers(workflow)}
    assert push == {"website-contract.yml", "notify_visualization.yml"}


def _source_link(sha: str) -> str:
    url = f"https://github.com/1cFE/fusion-tea/tree/{sha}/exploration/concept_explorer"
    return f'<p>Frontend source: <a href="{url}">fusion-tea</a></p>'


@pytest.mark.parametrize(
    ("answer", "verdict"),
    [
        pytest.param(drift.Page(200, _source_link(PIN)), drift.Drift.PASS, id="links-the-pin"),
        pytest.param(drift.Page(200, _source_link("f" * 40)), drift.Drift.FAIL, id="another-sha"),
        pytest.param(drift.Page(200, "<p>Concept 01</p>"), drift.Drift.FAIL, id="no-link"),
        pytest.param(drift.Page(503, ""), drift.Drift.WARN, id="not-200"),
        pytest.param(urllib.error.URLError("unreachable"), drift.Drift.WARN, id="network-error"),
    ],
)
def test_drift_verdicts(answer: drift.Page | OSError, verdict: drift.Drift) -> None:
    requested = []

    def fetch(url: str) -> drift.Page:
        requested.append(url)
        if isinstance(answer, OSError):
            raise answer
        return answer

    result, message = drift.public_pin_drift(PIN, "01", fetch)
    assert (result, requested) == (verdict, ["https://1cf.energy/tools/concepts/concept/01/"])
    assert message.startswith(requested[0])
