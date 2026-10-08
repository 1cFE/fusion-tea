"""Per-key provenance round-trips, and never changes what is traced.

Invariant 8. A tie key and a fan-out key are traced identically; what provenance
changes is what a cold reader can tell about why the key is in the group.
"""

import json

import pytest

from tests.study.conftest import KNOWN_ANSWER_DECLARATION, REAL_MANIFEST, REAL_PACKAGE, run_tool

KNOWN_ANSWERS = KNOWN_ANSWER_DECLARATION


def group_by_axis(doc, axis):
    return next(g for g in doc["groups"] if g["axis"] == axis)


def test_every_declared_key_carries_its_provenance():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    for group in doc["groups"]:
        for entry in group["declared_keys"]:
            assert entry["provenance"] in ("fan_out", "tie")


def test_provenance_round_trips_from_the_declaration(request):
    """The record snapshots declared groups with per-key provenance, so the tool must
    not flatten a group to a bare key list."""
    import json

    declared = {
        group["axis"]: {key["key"]: key["provenance"] for key in group["keys"]}
        for group in json.loads(KNOWN_ANSWERS.read_text())["groups"]
    }
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    for group in doc["groups"]:
        got = {entry["key"]: entry["provenance"] for entry in group["declared_keys"]}
        assert got == declared[group["axis"]]


@pytest.fixture
def provenance_copy(package_copy):
    """Test-only provenance annotation; no physical identity is claimed."""
    copy = package_copy(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    copy.edit_axes(
        lambda d: d["groups"].append(
            {
                "axis": "test_tie",
                "keys": [
                    {"key": "stellarator_09__stellaris__plasma__R", "provenance": "fan_out"},
                    {
                        "key": "stellarator_09__stellaris__magnet__coil__turn_current",
                        "provenance": "tie",
                    },
                ],
            }
        )
    )
    return copy


def test_the_tie_key_is_marked_and_the_others_are_not(provenance_copy):
    rc, out, err = provenance_copy.run()
    assert rc == 0, err
    tied = {
        e["key"]: e["provenance"]
        for e in group_by_axis(json.loads(out), "test_tie")["declared_keys"]
    }
    assert tied["stellarator_09__stellaris__magnet__coil__turn_current"] == "tie"
    assert tied["stellarator_09__stellaris__plasma__R"] == "fan_out"


def test_a_tie_key_traces_identically_to_a_fan_out_key(provenance_copy):
    rc, out, err = provenance_copy.run()
    assert rc == 0, err
    declared = group_by_axis(json.loads(out), "test_tie")
    provenance_copy.edit_axes(
        lambda d: [
            k.update(provenance="fan_out")
            for g in d["groups"]
            if g["axis"] == "test_tie"
            for k in g["keys"]
        ]
    )
    rc, out, err = provenance_copy.run()
    assert rc == 0, err
    plain = group_by_axis(json.loads(out), "test_tie")
    assert {k: v for k, v in declared.items() if k != "declared_keys"} == {
        k: v for k, v in plain.items() if k != "declared_keys"
    }
    assert [e["provenance"] for e in plain["declared_keys"]] == ["fan_out"] * 2


def test_entry_type_is_reported_per_declared_key():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    types = {
        entry["key"]: entry["entry_type"]
        for group in doc["groups"]
        for entry in group["declared_keys"]
    }
    # WI-030: the bound beta retired. WI-035: the bound field retired in turn —
    # the coil-set current lever and its facts are the design attributes now.
    assert types["stellarator_09__stellaris__magnet__coil__turn_current"] == "design_attribute"
    assert "stellarator_09__stellaris__magnet__R0" not in types
    # Since the model migration the swept plant attributes are design attributes too
    # (one entry point per authored attribute); the usage-literal class is exercised
    # by the known-answers test on the recirc threshold.
    assert types["stellarator_09__stellaris__plasma__R"] == "design_attribute"
