"""Exercise the publication sections of frozen native entrypoints without running models.

The scripts execute at import time. Compile their unchanged publication statements,
with synthetic already-returned cases; preflight, evaluation and persistence are
covered by the route tests. All writes are confined to pytest's temporary directory.
"""
import ast
import csv
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from exploration.stellarator_e2e.studies import study_route as route

ROOT = Path(route.HERE)
NATIVE = {
    "20260911-model-owned-radius": ("execute.py", "rows=[]", "store=StudyStore"),
    "20260911-operating-heating": ("run.py", "rows=[]", "clean=preflight"),
    "20260912-plant-closure": ("execute.py", "channels=study.channels()", "write(R/'case-inputs.json'"),
}


def publication(study_id, cases, directory):
    filename, start, end = NATIVE[study_id]
    path = ROOT / study_id / "execution" / filename
    source = path.read_text()
    # This is the actual complete publication section, not a reimplementation.
    begin, finish = source.index(start), source.index(end)
    code = compile(ast.parse(source[begin:finish]), str(path), "exec")
    channels = {"zero": "zero", "required": "required"}
    labels = [dict(point=dict(c.inputs), arm_id="arm", label=str(i)) for i, c in enumerate(cases)]
    study = SimpleNamespace(channels=lambda: channels, CHANNELS=channels,
                            PROPOSAL={"study_id": study_id}, labelled_proposals=lambda: labels)
    props = {str(i): dict(raw_json=json.dumps(c.inputs), candidate_id=c.candidate_id)
             for i, c in enumerate(cases)}
    def write(path, value):
        (directory / path).write_text(json.dumps(value))
    namespace = dict(route=route, cases=cases, R=directory, study=study, csv=csv,
                     json=json, write=write, compat={}, props=props,
                     mint_proposal_id=lambda _, i: str(i),
                     byid={c.candidate_id: c for c in cases},
                     catalog=route._export_catalog(route.PACKAGE_DIR))
    exec(code, namespace)
    return directory / ("native-points.csv" if study_id == "20260912-plant-closure" else "points.csv")


def cases():
    verdicts = {key: "satisfied" for key in route._catalog_by_constraint_id(route.PACKAGE_DIR)}
    return [SimpleNamespace(candidate_id=f"case-{i}", state="completed",
                            inputs={route.P + "R": 12.7 + i},
                            outputs={"zero": 0., "required": 2. + i},
                            verdicts=dict(verdicts), headline="satisfied") for i in range(2)]


@pytest.mark.parametrize("study_id", NATIVE)
def test_native_publication_preserves_values_and_case_identity(study_id, tmp_path):
    data = cases()
    output = publication(study_id, data, tmp_path)
    rows = list(csv.DictReader(output.open()))
    assert [r["candidate_id"] for r in rows] == [c.candidate_id for c in data]
    assert [float(r["zero"]) for r in rows] == [0., 0.]
    assert [float(r["required"]) for r in rows] == [2., 3.]


@pytest.mark.parametrize("study_id", NATIVE)
@pytest.mark.parametrize("bad", ["absent", None, float("nan")], ids=["absent", "null", "nan"])
def test_native_publication_refuses_before_replacing_evidence(study_id, bad, tmp_path):
    data = cases()
    if bad == "absent":
        del data[1].outputs["required"]
    else:
        data[1].outputs["required"] = bad
    previous = b"previous evidence\n"
    for name in ("native-points.csv", "points.csv", "cases.json"):
        (tmp_path / name).write_bytes(previous)
    with pytest.raises(route.RouteError, match="required"):
        publication(study_id, data, tmp_path)
    for name in ("native-points.csv", "points.csv", "cases.json"):
        assert (tmp_path / name).read_bytes() == previous


@pytest.mark.parametrize("bad", ["absent", None, float("nan"), float("inf"), -float("inf")],
                         ids=["absent", "null", "nan", "positive-inf", "negative-inf"])
def test_required_values_refuse_invalid_numbers(bad):
    data = cases()[0]
    if bad == "absent":
        del data.outputs["required"]
    else:
        data.outputs["required"] = bad
    with pytest.raises(route.RouteError, match="required"):
        route.required_outputs(data, {"zero": "zero", "required": "required"})
