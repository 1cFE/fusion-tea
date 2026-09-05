"""Required numeric evidence survives the store and cannot be silently skipped."""

from types import SimpleNamespace

import pytest

from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import verify


@pytest.mark.parametrize("side", ["store", "oracle"])
@pytest.mark.parametrize("missing", [True, False], ids=["absent", "null"])
@pytest.mark.parametrize("kind", ["objective", "operand"])
def test_verification_refuses_partial_numeric_coverage(side, missing, kind):
    outputs = {"control": 1.0, "required": 2.0}
    oracle = dict(outputs)
    target = outputs if side == "store" else oracle
    if missing:
        del target["required"]
    else:
        target["required"] = None
    case = SimpleNamespace(
        candidate_id="case-1",
        executable_fingerprint="pin",
        inputs={},
        outputs=outputs,
        verdicts={},
    )
    objectives = {"control": "control"}
    bindings = {}
    if kind == "objective":
        objectives["required"] = "required"
    else:
        bindings = {"check": {"left": {"kind": "channel", "key": "required"}}}
    with pytest.raises(verify.VerifyError, match="missing required numeric comparisons") as exc:
        verify.check_case(case, lambda _: oracle, bindings, {}, objectives, {}, "pin")
    assert f"{side}=['required']" in str(exc.value)


def test_missing_publication_refuses_before_bulk_run_or_store_creation(
    stock_simkit_path,
    monkeypatch,
    tmp_path,
):
    calls = []

    def evaluate(inputs):
        calls.append(inputs)
        return SimpleNamespace(outputs={"control": 1.0})

    monkeypatch.setattr(
        route,
        "prepare",
        lambda *_: SimpleNamespace(
            entry_models={},
            evaluate=evaluate,
        ),
    )
    with pytest.raises(route.RouteError, match="required result channels.*missing"):
        route.run_points(
            "missing-output",
            [{}] * 100,
            tmp_path,
            required_channels={"missing": "not-published"},
        )
    assert len(calls) == 1
    assert not (tmp_path / "missing-output.db").exists()


def test_real_multi_output_values_survive_reopened_store_and_export(
    stock_simkit_path,
    tmp_path,
):
    from simkit.study.query import StudyQuery
    from simkit.study.store import StudyStore

    required = {
        "p_net": f"{route.P}pb__p_net",
        "rec_frac": f"{route.P}pb__rec_frac",
        "q_eng": f"{route.P}pb__q_eng",
        "p_th": f"{route.P}pb__p_th",
        "p_et": f"{route.P}pb__p_et",
        "lcoe": route.CHANNELS["lcoe"],
    }
    cases, db = route.run_points(
        "numeric-evidence",
        [route.proposal_for(**route.BASELINE)],
        tmp_path,
        required_channels=required,
    )
    assert len(cases) == 1 and cases[0].state == "completed"
    store = StudyStore(db)
    try:
        reopened = StudyQuery(store, route.PACKAGE_DIR).cases()[0]
        assert (
            store.conn.execute("SELECT evidence_schema_version FROM compatibility").fetchone()[0]
            == "v3"
        )
    finally:
        store.close()
    values = route.required_outputs(reopened, required)
    assert values == route.required_outputs(cases[0], required)
    assert all(isinstance(value, float) for value in values.values())
    assert values["p_net"] == pytest.approx(values["p_et"] * (1 - values["rec_frac"]))
    assert values["p_et"] == pytest.approx(0.333 * values["p_th"])
    assert values["q_eng"] == pytest.approx(1 / values["rec_frac"])
    assert values["lcoe"] > 0
    path = route.write_csv([values], tmp_path / "numeric.csv")
    assert ",," not in path.read_text()


def test_required_channel_map_change_refuses_store_resume(stock_simkit_path, tmp_path):
    from simkit.study.store import IncompatibleStore

    proposals = [route.proposal_for(**route.BASELINE)]
    required = {"lcoe": route.CHANNELS["lcoe"]}
    route.run_points("map-binding", proposals, tmp_path, required_channels=required)
    changed = dict(required, p_net=f"{route.P}pb__p_net")

    with pytest.raises(IncompatibleStore, match="study_definition_fingerprint"):
        route.run_points("map-binding", proposals, tmp_path, required_channels=changed)


def test_resume_refuses_incomplete_stored_evidence_despite_complete_preflight(
    stock_simkit_path,
    monkeypatch,
    tmp_path,
):
    from simkit.evaluation.evaluator import PreparedEvaluator

    original_evaluate = PreparedEvaluator.evaluate
    calls = []
    channel = f"{route.P}pb__p_net"

    def evaluate(self, typed_inputs):
        evidence = original_evaluate(self, typed_inputs)
        calls.append(evidence)
        if len(calls) == 2:  # Admit complete evidence, then persist one incomplete case.
            outputs = dict(evidence.outputs)
            del outputs[channel]
            return evidence.model_copy(update={"outputs": outputs})
        return evidence

    monkeypatch.setattr(PreparedEvaluator, "evaluate", evaluate)
    proposals = [route.proposal_for(**route.BASELINE)]
    required = {"p_net": channel}
    for _ in range(2):
        with pytest.raises(route.RouteError, match="required result channels.*pb__p_net"):
            route.run_points("incomplete-resume", proposals, tmp_path, required_channels=required)
    assert (tmp_path / "incomplete-resume.db").exists()
    assert len(calls) == 3  # Resume checks a fresh point but does not re-execute the stored case.
