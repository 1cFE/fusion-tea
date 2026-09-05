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


def test_missing_publication_refuses_before_bulk_run_or_evidence_commit(
    stock_simkit_path,
    monkeypatch,
    tmp_path,
):
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.study.store import StudyStore

    calls = []

    def evaluate(self, inputs):
        calls.append(inputs)
        return SimpleNamespace(outputs={"control": 1.0})

    monkeypatch.setattr(PreparedEvaluator, "evaluate", evaluate)
    with pytest.raises(route.RouteError, match="required result channels.*missing"):
        route.run_points(
            "missing-output",
            [{}] * 100,
            tmp_path,
            required_channels={"missing": "not-published"},
        )
    assert len(calls) == 1
    store = StudyStore(tmp_path / "missing-output.db")
    try:
        assert store.conn.execute("SELECT count(*) FROM cases").fetchone()[0] == 0
        store.acquire_lease()  # Refusal released the previous lease.
        store.release_lease()
    finally:
        store.close()


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


def test_adding_persisted_column_reuses_store_without_evaluation(
    stock_simkit_path,
    monkeypatch,
    tmp_path,
):
    from simkit.evaluation.evaluator import PreparedEvaluator

    proposals = [route.proposal_for(**route.BASELINE)]
    required = {"lcoe": route.CHANNELS["lcoe"]}
    original, db = route.run_points("map-binding", proposals, tmp_path, required_channels=required)
    changed = dict(required, p_net=f"{route.P}pb__p_net")

    def unexpected_evaluation(*args):
        pytest.fail("a presentation-only change re-executed a stored case")

    monkeypatch.setattr(PreparedEvaluator, "evaluate", unexpected_evaluation)
    resumed, resumed_db = route.run_points(
        "map-binding", proposals, tmp_path, required_channels=changed
    )
    assert resumed_db == db
    assert resumed[0].evidence_digest == original[0].evidence_digest
    assert (
        route.required_outputs(resumed[0], changed)["p_net"]
        == original[0].outputs[changed["p_net"]]
    )


@pytest.mark.parametrize("interrupted", [False, True], ids=["complete", "partial"])
def test_resume_refuses_a_required_column_absent_from_persisted_evidence(
    stock_simkit_path,
    monkeypatch,
    tmp_path,
    interrupted,
):
    from simkit.evaluation.evaluator import PreparedEvaluator

    original_evaluate = PreparedEvaluator.evaluate
    calls = []
    channel = f"{route.P}pb__p_net"

    def evaluate(self, typed_inputs):
        evidence = original_evaluate(self, typed_inputs)
        calls.append(evidence)
        if interrupted and len(calls) == 2:
            raise RuntimeError("interrupted after one durable case")
        outputs = dict(evidence.outputs)
        del outputs[channel]
        return evidence.model_copy(update={"outputs": outputs})

    monkeypatch.setattr(PreparedEvaluator, "evaluate", evaluate)
    proposals = [route.proposal_for(**route.BASELINE)] * (2 if interrupted else 1)

    def initial_run():
        route.run_points(
            "incomplete-resume",
            proposals,
            tmp_path,
            required_channels={"lcoe": route.CHANNELS["lcoe"]},
        )

    if interrupted:
        with pytest.raises(RuntimeError, match="interrupted"):
            initial_run()
    else:
        initial_run()
    with pytest.raises(route.RouteError, match="required result channels.*pb__p_net"):
        route.run_points(
            "incomplete-resume", proposals, tmp_path, required_channels={"p_net": channel}
        )
    assert (tmp_path / "incomplete-resume.db").exists()
    assert len(calls) == len(proposals)  # Resume refuses before running any remaining work.


@pytest.mark.parametrize("failures", [1, 2], ids=["first-fails", "all-fail"])
def test_execution_failures_remain_recorded_cases(
    stock_simkit_path, monkeypatch, tmp_path, failures
):
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.evaluation.failure import EvaluationFailed, EvaluationFailure, EvaluationPhase

    original = PreparedEvaluator.evaluate
    calls = []

    def evaluate(self, inputs):
        calls.append(inputs)
        if len(calls) <= failures:
            raise EvaluationFailed(
                EvaluationFailure(
                    phase=EvaluationPhase.MODULE_EXECUTION,
                    cause="fence probe execution failed",
                )
            )
        return original(self, inputs)

    monkeypatch.setattr(PreparedEvaluator, "evaluate", evaluate)
    proposals = [route.proposal_for(**route.BASELINE)] * 2
    cases, db = route.run_points("execution-failure", proposals, tmp_path)
    assert len(calls) == 2 and db.exists()
    assert [case.state for case in cases] == ["execution_failed"] * failures + ["completed"] * (
        2 - failures
    )


def test_nonfinite_declared_value_is_persisted_and_refused_only_at_export(
    stock_simkit_path, monkeypatch, tmp_path
):
    """[OWNER 2026-09-05] A nonfinite value is a model result, not a tooling omission:
    the run keeps it and the exporter refuses it."""
    import math

    from simkit.evaluation.evaluator import PreparedEvaluator

    original = PreparedEvaluator.evaluate
    channel = f"{route.P}pb__p_net"
    calls = []

    def evaluate(self, inputs):
        calls.append(inputs)
        evidence = original(self, inputs)
        outputs = dict(evidence.outputs)
        outputs[channel] = float("nan")
        return evidence.model_copy(update={"outputs": outputs})

    monkeypatch.setattr(PreparedEvaluator, "evaluate", evaluate)
    required = {"p_net": channel, "lcoe": route.CHANNELS["lcoe"]}
    proposals = [route.proposal_for(**route.BASELINE)]
    cases, db = route.run_points(
        "nonfinite-result", proposals, tmp_path, required_channels=required
    )
    assert [case.state for case in cases] == ["completed"]
    assert math.isnan(cases[0].outputs[channel])
    resumed, _ = route.run_points(
        "nonfinite-result", proposals, tmp_path, required_channels=required
    )
    assert len(calls) == 1  # the result is kept; the resume re-executes nothing
    with pytest.raises(route.RouteError, match="nonfinite.*pb__p_net"):
        route.required_outputs(resumed[0], required)
