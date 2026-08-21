"""Per-key provenance round-trips, and never changes what is traced.

Invariant 8. A tie key and a fan-out key are traced identically; what provenance
changes is what a cold reader can tell about why the key is in the group.
"""

from tests.study.conftest import DATA_DIR, REAL_MANIFEST, REAL_PACKAGE, run_tool

KNOWN_ANSWERS = DATA_DIR / "axes.known_answers.json"


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


def test_the_tie_key_is_marked_and_the_others_are_not():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    tied = {e["key"]: e["provenance"] for e in group_by_axis(doc, "R+tie")["declared_keys"]}
    assert tied["stellarator_09__stellaris__magnet__R0"] == "tie"
    assert tied["stellarator_09__stellaris__geom__R"] == "fan_out"
    assert tied["stellarator_09__stellaris__rb__R"] == "fan_out"


def test_a_tie_key_traces_identically_to_a_fan_out_key(package_copy):
    """Flip the tie key's provenance to fan_out: only the provenance field moves."""
    copy = package_copy(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    copy.edit_axes(
        lambda data: [
            key.update(provenance="fan_out")
            for group in data["groups"]
            if group["axis"] == "R+tie"
            for key in group["keys"]
        ]
    )
    rc, out, err = copy.run()
    assert rc == 0, err

    import json

    as_fan_out = group_by_axis(json.loads(out), "R+tie")
    as_declared = group_by_axis(run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS), "R+tie")
    def without_declared_keys(group):
        return {k: v for k, v in group.items() if k != "declared_keys"}

    assert without_declared_keys(as_fan_out) == without_declared_keys(as_declared)
    assert [e["provenance"] for e in as_fan_out["declared_keys"]] == ["fan_out"] * 3


def test_entry_type_is_reported_per_declared_key():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    types = {
        entry["key"]: entry["entry_type"]
        for group in doc["groups"]
        for entry in group["declared_keys"]
    }
    assert types["stellarator_09__stellaris__beta"] == "design_attribute"
    assert types["stellarator_09__stellaris__magnet__R0"] == "design_attribute"
    assert types["stellarator_09__stellaris__geom__R"] == "usage_literal"
