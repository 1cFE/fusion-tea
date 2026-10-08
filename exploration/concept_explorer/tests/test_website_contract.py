"""Self-tests for the website contract gate (exploration/concept_explorer/website_contract).

These run inside the gate. The fixture is the fake costing model from
test_state_and_compute.py, reused the way test_cors.py reuses it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from exploration.concept_explorer.tests import test_state_and_compute as compute_tests
from exploration.concept_explorer.website_contract import contract as c

costingfe_base_dir = compute_tests.costingfe_base_dir

PIN = "0" * 40


@pytest.fixture
def no_warmup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXPLORER_SKIP_WARMUP", "1")


@pytest.fixture
def recorded_text(costingfe_base_dir: Path, no_warmup: None) -> str:
    with c.serve(costingfe_base_dir) as client:
        schema = c.classify(client.get("/openapi.json").json())
        observation = c.observe(client, c.manifest_concept_ids(client))
    return c.render(c.record(observation, schema, PIN, tools=[], js={}))


def test_flatten_kinds_and_containers() -> None:
    body = {"a": 1, "b": True, "c": None, "d": [], "m": {"x": {"v": 1.5}}, "r": [{"k": "s"}, {}]}
    s = c.flatten([body], map_paths={".m"})
    assert s[".a"] == {"number"} and s[".b"] == {"boolean"}  # bool tested before int
    assert s[".c"] == {"null"} and s[".d"] == {"empty"}
    assert s[".m{*}.v"] == {"number"}  # map recorded by value shape
    assert s[".r[].k"] == {"string", "absent"}  # union over elements


def test_contract_text_is_deterministic(recorded_text: str) -> None:
    assert c.render(c.parse(recorded_text)) == recorded_text


def test_unchanged_server_passes_its_own_recording(
    costingfe_base_dir: Path,
    no_warmup: None,
    recorded_text: str,
) -> None:
    contract = c.parse(recorded_text)
    with c.serve(costingfe_base_dir) as client:
        observation = c.observe(client, contract.concepts)
    assert c.check(observation, contract) == []


def test_observe_sends_what_the_fixture_supports(costingfe_base_dir: Path, no_warmup: None) -> None:
    with c.serve(costingfe_base_dir) as client:
        observation = c.observe(client, ["01", "04"])
    statuses = {
        template: [(r.instance, r.status) for r in responses]
        for template, responses in observation.items()
    }
    assert statuses == {
        c.MANIFEST: [(None, 200)],
        c.REGISTRY: [(None, 404)],  # the fixture has no taxonomy files
        c.TREE: [(None, 404)],
        c.COST_LANDSCAPE: [(None, 200)],
        c.PARAMETER_INDEX: [(None, 200)],
        c.CONCEPT: [("01", 200), ("04", 200)],
        c.FINDINGS: [("01", 200), ("04", 200)],
        c.PARAMETER: [],  # no sensitivities, so no parameters
        c.STATE_CONCEPT: [(None, 200)],
        c.STATE_COMPARE: [(None, 200)],
        c.SLIDER: [],
        c.SLIDER_RANGE: [],
        c.TOGGLE: [],  # no analyst overrides
    }
    assert all(r.body is not None for responses in observation.values() for r in responses if r.ok)


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
