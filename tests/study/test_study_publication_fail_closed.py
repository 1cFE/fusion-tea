"""Fail-closed publication gates for the stellarator demo studies.

The CSVs are evidence. A changed generated identifier must still resolve through the
embedded constraint catalog, and an incomplete case or study must leave any existing
CSV bytes untouched.
"""

from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from exploration.stellarator_e2e.studies import study_route


def _case(package_dir=study_route.PACKAGE_DIR, *, state="completed"):
    catalog = study_route._catalog_by_constraint_id(package_dir)
    return SimpleNamespace(
        state=state,
        inputs={
            study_route.AXES["R"][0]: study_route.BASELINE["R"],
            study_route.AXES["a"][0]: study_route.BASELINE["a"],
            study_route.AXES["availability"][0]: study_route.BASELINE["availability"],
        },
        outputs={
            channel: float(index)
            for index, channel in enumerate(study_route.CHANNELS.values())
        },
        verdicts={constraint_id: "satisfied" for constraint_id in catalog},
    )


def test_export_resolves_an_opaque_constraint_id_through_the_catalog(
    real_package_path, tmp_path
):
    contract = json.loads(
        (real_package_path / "contracts" / "model_contract.json").read_text()
    )
    expected_names = {
        entry["source_local_identity"]
        for entry in contract["constraint_catalog"]["concrete_entries"]
    }
    for index, entry in enumerate(contract["constraint_catalog"]["concrete_entries"]):
        entry["constraint_id"] = f"opaque-id-{index}"

    package = tmp_path / "package"
    contract_path = package / "contracts" / "model_contract.json"
    contract_path.parent.mkdir(parents=True)
    contract_path.write_text(json.dumps(contract))
    output = tmp_path / "opaque.csv"

    study_route.export_csv([_case(package)], ["R", "a"], output, package_dir=package)

    with output.open(newline="") as handle:
        row = next(csv.DictReader(handle))
    assert expected_names <= set(row)
    assert not any(name.startswith("opaque-id-") for name in row)


def _missing_result(case):
    case.outputs.pop(next(iter(study_route.CHANNELS.values())))


def _null_result(case):
    case.outputs[next(iter(study_route.CHANNELS.values()))] = None


def _no_checks(case):
    case.verdicts.clear()


def _missing_check(case):
    case.verdicts.pop(next(iter(case.verdicts)))


def _unexpected_check(case):
    case.verdicts["not-in-the-catalog"] = "satisfied"


@pytest.mark.parametrize(
    "mutate",
    [_missing_result, _null_result, _no_checks, _missing_check, _unexpected_check],
    ids=["missing-result", "null-result", "no-checks", "missing-check", "unexpected-check"],
)
def test_export_refuses_incomplete_or_unknown_case_data_without_replacing_csv(
    mutate, tmp_path
):
    case = _case()
    mutate(case)
    output = tmp_path / "study.csv"
    previous = b"previous evidence\n"
    output.write_bytes(previous)

    with pytest.raises(study_route.RouteError):
        study_route.export_csv([case], ["R", "a"], output)

    assert output.read_bytes() == previous


LOCAL_STUDIES = sorted(Path(study_route.HERE).glob("*/study.py"))


@pytest.fixture(params=LOCAL_STUDIES, ids=lambda path: path.parent.name)
def local_study(request):
    spec = importlib.util.spec_from_file_location(request.param.parent.name, request.param)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _local_case(study):
    proposal = study.proposals()[0]
    inputs = proposal[-1] if isinstance(proposal, tuple) else proposal
    case = _case()
    case.candidate_id = "test-candidate"
    case.inputs = inputs
    case.outputs = {
        channel: float(index) for index, channel in enumerate(study.CHANNELS.values())
    }
    return case


@pytest.mark.parametrize("missing", [True, False], ids=["absent", "null"])
@pytest.mark.parametrize("bad_index", [0, 1], ids=["first-case", "later-case"])
def test_local_export_refuses_incomplete_results_before_publishing(
    local_study, missing, bad_index, tmp_path
):
    cases = [_local_case(local_study), _local_case(local_study)]
    channel = next(reversed(local_study.CHANNELS.values()))
    if missing:
        del cases[bad_index].outputs[channel]
    else:
        cases[bad_index].outputs[channel] = None
    output = tmp_path / "points.csv"
    previous = b"previous evidence\n"
    output.write_bytes(previous)

    with pytest.raises(local_study.route.RouteError, match=channel):
        local_study.export(cases, output)

    assert output.read_bytes() == previous


def test_local_export_preserves_all_complete_values_including_zero(local_study, tmp_path):
    case = _local_case(local_study)
    output = local_study.export([case], tmp_path / "points.csv")
    with output.open(newline="") as handle:
        row = next(csv.DictReader(handle))
    for name, channel in local_study.CHANNELS.items():
        assert float(row[name]) == case.outputs[channel]


def _command(monkeypatch, stock_simkit_path):
    monkeypatch.setenv("STOP_PARSER_TEAX_ROOT", str(stock_simkit_path.parents[1]))
    return importlib.import_module(
        "exploration.stellarator_e2e.study.run_design_search"
    )


def _assert_publication_unchanged(work):
    radius = work / "design_search_R_a.csv"
    availability = work / "availability_sweep.csv"
    assert radius.read_bytes() == b"previous radius evidence\n"
    assert not availability.exists()


def _seed_publication(work):
    work.mkdir(exist_ok=True)
    (work / "design_search_R_a.csv").write_bytes(b"previous radius evidence\n")


def test_run_command_refuses_one_failed_case_before_publishing(
    monkeypatch, stock_simkit_path, tmp_path
):
    command = _command(monkeypatch, stock_simkit_path)
    _seed_publication(tmp_path)
    monkeypatch.setattr(command, "WORK", tmp_path)
    monkeypatch.setattr(command.route, "design_search_proposals", lambda: [{}])
    monkeypatch.setattr(command.route, "availability_sweep_proposals", lambda: [{}, {}])
    case = _case(command.route.PACKAGE_DIR)
    runs = iter([
        ([case], tmp_path / "radius.db"),
        ([case, _case(command.route.PACKAGE_DIR, state="failed")], tmp_path / "sweep.db"),
    ])
    monkeypatch.setattr(command.route, "run_points", lambda *args, **kwargs: next(runs))
    monkeypatch.setattr(command, "assert_package_untouched", lambda: None)

    with pytest.raises(command.route.RouteError):
        command.cmd_run()

    _assert_publication_unchanged(tmp_path)


def test_export_command_refuses_one_failed_case_before_publishing(
    monkeypatch, stock_simkit_path, tmp_path
):
    command = _command(monkeypatch, stock_simkit_path)
    _seed_publication(tmp_path)
    monkeypatch.setattr(command, "WORK", tmp_path)
    monkeypatch.setattr(command, "assert_package_untouched", lambda: None)

    from simkit.study import query, store

    class FakeStore:
        def __init__(self, path):
            self.path = path

    class FakeQuery:
        def __init__(self, fake_store, package_dir):
            self.store = fake_store

        def cases(self):
            complete = _case(command.route.PACKAGE_DIR)
            if "availability" in self.store.path.name:
                return [complete, _case(command.route.PACKAGE_DIR, state="failed")]
            return [complete]

    monkeypatch.setattr(store, "StudyStore", FakeStore)
    monkeypatch.setattr(query, "StudyQuery", FakeQuery)

    with pytest.raises(command.route.RouteError):
        command.cmd_export()

    _assert_publication_unchanged(tmp_path)
