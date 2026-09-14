"""Fail-closed publication gates for the stellarator demo studies.

The CSVs are evidence. A changed generated identifier must still resolve through the
embedded constraint catalog, and an incomplete case or study must leave any existing
CSV bytes untouched.
"""

from __future__ import annotations

import csv
import importlib
import json
import inspect
import math
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
            study_route.AXES["availability_direct"][0]: study_route.BASELINE["availability_direct"],  # WI-046
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


# These exporters accept cases directly. Native execution scripts are tested separately.
LOCAL_STUDIES = [Path(study_route.HERE) / name / "study.py" for name in (
    "20260821-power-cycle-ab", "20260823-magnet-technology-ab", "20260829-p-pump-fence",
    "20260830-stress-fence", "20260901-sustainment-fence", "20260903-priced-levers",
    "20260903-wall-and-heating", "20260904-wall-and-heating", "20260905-stored-energy-basis",
    "20260907-burn-control", "20260907-minor-radius",
)]


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
    case.study_arm = proposal[0] if isinstance(proposal, tuple) else None
    case.outputs = {
        channel: float(index) for index, channel in enumerate(study.CHANNELS.values())
    }
    # Satisfy the exporter's independent physical consistency guards. These are
    # synthetic publication inputs, not numerical model expectations.
    if "W_mag" in study.CHANNELS:
        centre = 3.15
        case.outputs[study.CHANNELS["r_coil_centre"]] = centre
        energy = 111e9 * (inputs[study.P + "magnet__coil__I_coil"] / 15400000)**2 * (centre / 3.1500000000000004)**2 * (12.7 / inputs[study.P + "magnet__R0"])
        case.outputs[study.CHANNELS["W_mag"]] = energy
        case.outputs[study.CHANNELS["m_casing"]] = 63000 * (energy / 111e9)**0.78
    return case


def _export_local(study, cases, path):
    kwargs = {"cases": cases, "path": path}
    parameters = inspect.signature(study.export).parameters
    if "arms" in parameters:
        kwargs["arms"] = {study._key(c.inputs): c.study_arm for c in cases}
    if "oracle" in parameters:
        study.EXPECTED_CALIBRATION = cases[0].outputs[study.CHANNELS["wall_peak_calibration"]]
        study.BASELINE_MAGNET = (1.0, 1.0)
        study.COMMITTED, study.COMMITTED_EXCLUDED = {}, set()
        oracle = {}
        for c in cases:
            values = {name: c.outputs.get(channel) for name, channel in study.CHANNELS.items()}
            thermal = (values["beta"] * values["B_axis"]**2 * 1.5 * values["plasma_volume"] / (2 * (4e-7 * math.pi)) * 1e-6) if "plasma_volume" in values else 1.0
            oracle[c.candidate_id] = dict(p_aux_required=1., p_net=100., n_He0=1., W_th=thermal, tau_E=1., alpha_He_eff=1., alpha_n_e_eff=1., n_e_volav=1.)
        kwargs["oracle"] = oracle
    return study.export(**kwargs)


@pytest.mark.parametrize(
    "bad_value", ["absent", None, float("nan")],
    ids=["absent", "null", "nan"],
)
def test_local_export_refuses_incomplete_results_before_publishing(
    local_study, bad_value, tmp_path
):
    cases = [_local_case(local_study), _local_case(local_study)]
    cases[1].candidate_id = "test-candidate-2"
    bad_index = 1
    channel = local_study.CHANNELS["fuel"] if "fuel" in local_study.CHANNELS else next(reversed(local_study.CHANNELS.values()))
    if bad_value == "absent":
        del cases[bad_index].outputs[channel]
    else:
        cases[bad_index].outputs[channel] = bad_value
    output = tmp_path / "points.csv"
    previous = b"previous evidence\n"
    output.write_bytes(previous)

    with pytest.raises(local_study.route.RouteError, match=channel):
        _export_local(local_study, cases, output)

    assert output.read_bytes() == previous


def test_local_export_preserves_all_complete_values_including_zero(local_study, tmp_path):
    case = _local_case(local_study)
    output = _export_local(local_study, [case], tmp_path / "points.csv")
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
