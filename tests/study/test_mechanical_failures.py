"""The fail-closed half of the owner's rule, end to end.

Every case asserts three things, not one: a non-zero exit, a message that locates
the fault, and — Invariant 1 — that no output file exists and stdout is empty.
A broken analysis must never look like an empty one.

All mutation runs on a ``package_copy``; the committed package is never touched.
Because the fingerprint gate runs before the parse (D8), each copy is re-pinned by
default, or the test would fail at the gate instead of at the failure it means to
exercise. The fingerprint-mismatch case is the same helper with re-pinning off.
"""

import json

import pytest

PIPELINE = "pipelines/pipeline.yaml"
ABSENT_KEY = "stellarator_09__stellaris__geom__NOPE"
COMPUTED_QUANTITY = "stellarator_09__stellaris__pb__p_net"
UNCLASSIFIED_KEY = "stellarator_09__stellaris__not_in_the_contract"


def _declare(copy, key, axis="R"):
    def mutate(data):
        group = next(g for g in data["groups"] if g["axis"] == axis)
        group["keys"].append({"key": key, "provenance": "fan_out"})

    copy.edit_axes(mutate)


def missing_declared_key(copy):
    _declare(copy, ABSENT_KEY)


def key_names_produced_channel(copy):
    """A real channel from the trace — a model output, not an axis."""
    _declare(copy, COMPUTED_QUANTITY)


def unclassifiable_key(copy):
    """Present in inputs/ but absent from the contract parameters, so its entry type
    cannot be classified."""
    path = copy.path / "inputs" / "stellarator_plant_params.json"
    data = json.loads(path.read_text())
    assert UNCLASSIFIED_KEY not in data, "fixture key already exists in the package"
    data[UNCLASSIFIED_KEY] = 1.0
    path.write_text(json.dumps(data, indent=2) + "\n")
    _declare(copy, UNCLASSIFIED_KEY)


def fingerprint_mismatch(copy):
    copy.edit(PIPELINE, "run_description:", "run_description:  ")


def unparseable_reference(copy):
    copy.edit(
        PIPELINE,
        "wall_load: float stellarator_09__stellaris__wall_load_calc__wall_load.root",
        "wall_load: float stellarator_09__stellaris__wall_load_calc__wall_load.value.deep",
    )


def corrupt_pipeline_line(copy):
    copy.edit(
        PIPELINE,
        "R_in: float stellarator_plant_params.stellarator_09__stellaris__R",
        "R_in: floatonly_one_token",
    )


def ghost_objective_channel(copy):
    copy.edit_manifest(
        lambda data: data["objective_catalog"][0].update(channel="stellarator_09__no_such_channel")
    )


def wrong_manifest_for_package(copy):
    copy.edit_manifest(lambda data: data["package"].update(name="some_other_package"))


def malformed_manifest_baseline(copy):
    copy.edit_manifest(lambda data: data["baseline"]["headline"].update(value="two dollars"))


CASES = [
    ("missing_declared_key", missing_declared_key, ABSENT_KEY, True),
    ("key_names_produced_channel", key_names_produced_channel, "computed quantity", True),
    ("unclassifiable_key", unclassifiable_key, "not in contract parameters", True),
    ("fingerprint_mismatch", fingerprint_mismatch, "indicator-input fingerprint", False),
    ("unparseable_reference", unparseable_reference, "wall_load.value.deep", True),
    ("corrupt_pipeline_line", corrupt_pipeline_line, "pipeline.yaml:", True),
    ("ghost_objective_channel", ghost_objective_channel, "produced by no module", True),
    ("wrong_manifest_for_package", wrong_manifest_for_package, "package_name", True),
    ("malformed_manifest_baseline", malformed_manifest_baseline, "baseline", True),
]


@pytest.mark.parametrize(
    "name,mutate,expect,repin", CASES, ids=[case[0] for case in CASES]
)
def test_fails_closed(real_copy, name, mutate, expect, repin, tmp_path):
    mutate(real_copy)
    out_path = tmp_path / "indicators.json"
    rc, out, err = real_copy.run(repin=repin, out=out_path)
    assert rc != 0, f"{name} exited 0"
    assert expect in err, f"{name}: message does not locate the fault:\n{err}"
    assert out == ""
    assert not out_path.exists()  # Invariant 1


def test_the_absent_key_and_the_computed_quantity_say_different_things(real_copy, tmp_path):
    """An author told 'your key is missing' when they picked a model output goes
    looking in the wrong place."""
    missing_declared_key(real_copy)
    _, _, absent = real_copy.run(out=tmp_path / "a.json")
    assert "absent from the package inputs" in absent
    assert "computed quantity" not in absent


def test_the_computed_quantity_message_names_the_producing_module(real_copy, tmp_path):
    key_names_produced_channel(real_copy)
    _, _, err = real_copy.run(out=tmp_path / "b.json")
    assert COMPUTED_QUANTITY in err
    assert "computed quantity" in err
    assert "channel produced by module" in err


def test_the_corrupt_line_carries_file_line_and_key_path(real_copy, tmp_path):
    corrupt_pipeline_line(real_copy)
    _, _, err = real_copy.run(out=tmp_path / "c.json")
    assert "pipeline.yaml:77" in err  # the rb R_in line; moved from :49 when WI-030 added two modules
    assert "key path modules.stellarator_09__stellaris__rb.inputs.R_in" in err
    assert "floatonly_one_token" in err


def test_the_fingerprint_mismatch_names_the_live_digests(real_copy, tmp_path):
    fingerprint_mismatch(real_copy)
    _, _, err = real_copy.run(repin=False, out=tmp_path / "d.json")
    assert "manifest pins" in err
    assert "live per-file digests" in err
    assert "pipelines/pipeline.yaml" in err
    assert "--print-fingerprint" in err


def test_the_ghost_objective_names_the_channel(real_copy, tmp_path):
    ghost_objective_channel(real_copy)
    _, _, err = real_copy.run(out=tmp_path / "e.json")
    assert "stellarator_09__no_such_channel" in err


def test_a_nonstandard_node_tag_inside_modules_is_a_failure(real_copy, tmp_path):
    """S6: compose preserves node tags, so a tagged value must be refused rather
    than read. Nothing executes either way — compose does not construct."""
    real_copy.edit(
        PIPELINE,
        "R_in: float stellarator_plant_params.stellarator_09__stellaris__R",
        "R_in: !!python/object/apply:os.system ['echo pwned']",
    )
    rc, out, err = real_copy.run(out=tmp_path / "f.json")
    assert rc != 0
    assert "node tag" in err
    assert out == ""


def test_an_unknown_key_inside_a_module_is_a_failure(real_copy, tmp_path):
    real_copy.edit(
        PIPELINE,
        "  stellarator_09__stellaris__geom:\n    module_type:",
        "  stellarator_09__stellaris__geom:\n    surprise: true\n    module_type:",
    )
    rc, _, err = real_copy.run(out=tmp_path / "g.json")
    assert rc != 0
    assert "unknown key(s)" in err and "surprise" in err


def test_a_duplicate_axis_in_the_declaration_is_a_failure(real_copy, tmp_path):
    real_copy.edit_axes(lambda data: data["groups"].append(dict(data["groups"][0])))
    rc, _, err = real_copy.run(out=tmp_path / "h.json")
    assert rc != 0
    assert "duplicate axis name" in err


def test_an_unknown_provenance_is_a_failure(real_copy, tmp_path):
    real_copy.edit_axes(
        lambda data: data["groups"][0]["keys"][0].update(provenance="because_i_said_so")
    )
    rc, _, err = real_copy.run(out=tmp_path / "i.json")
    assert rc != 0
    assert "'fan_out' or 'tie'" in err


def test_an_unknown_group_named_by_the_group_flag_is_a_failure(real_copy, tmp_path):
    rc, out, err = real_copy.run(out=tmp_path / "j.json", group=("no_such_axis",))
    assert rc != 0
    assert "no_such_axis" in err
    assert out == ""
    assert not (tmp_path / "j.json").exists()
