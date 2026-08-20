"""Each negative fails closed, names the fault, and still writes a complete document.

D9 is the rule under test as much as the checks are: a failed check is recorded as
`fail` with its detail, every other check still carries its real outcome, and the
process exits non-zero. Writing zero bytes on failure would make record §9 fillable
only by hand from stderr, and would lose the outcome of every check after the failing
one.

The committed package is read-only here. Four of the five negatives are produced by
mutating the *documents* preflight reads, in tmp_path. The fifth — a dirty tree — is
aimed at the `clean` subcommand against a scratch tree inside the repository, because
a tree git cannot see is a different failure than a tree git can see is dirty.
"""

import json

import pytest

from tests.study.test_preflight_gates import (
    ALL_SIX,
    DECLARATION,
    MANIFEST,
    executed_baseline,  # noqa: F401  (fixture)
    gates_argv,
    run_preflight,
)

P = "stellarator_09__stellaris__"


def _copy_json(source, dest, mutate):
    data = json.loads(source.read_text())
    mutate(data)
    dest.write_text(json.dumps(data, indent=2) + "\n")
    return dest


def remove_declared_key(tmp_path):
    """A declared key no package input defines."""
    absent = f"{P}geom__no_such_axis_key"
    path = _copy_json(
        DECLARATION, tmp_path / "axes.json",
        lambda d: d["groups"][0]["keys"].append({"key": absent, "provenance": "fan_out"}),
    )
    return {"groups": path}, "declared_keys", absent


def point_key_at_a_channel(tmp_path):
    """A declared key that names a produced channel — a computed quantity, not an input."""
    channel = f"{P}lcoe_calc__lcoe"
    path = _copy_json(
        DECLARATION, tmp_path / "axes.json",
        lambda d: d["groups"][0]["keys"].append({"key": channel, "provenance": "fan_out"}),
    )
    return {"groups": path}, "declared_keys", "computed quantity"


def corrupt_the_identity(tmp_path, identity_doc):
    path = _copy_json(
        identity_doc, tmp_path / "package_identity.json",
        lambda d: d["identity"].update(digest="0" * 64),
    )
    return {"identity": path}, "identity", "recomputed"


def stale_the_manifest(tmp_path):
    path = _copy_json(
        MANIFEST, tmp_path / "manifest.json",
        lambda d: d["fingerprints"]["recorded_provenance"].update(semantic_fingerprint="0" * 64),
    )
    return {"manifest": path}, "manifest_currency", "semantic_fingerprint"


NEGATIVES = ["missing_declared_key", "key_names_a_channel", "wrong_fingerprint", "stale_manifest"]


@pytest.mark.parametrize("case", NEGATIVES)
def test_each_negative_fails_closed_and_still_writes_a_complete_document(
    case, executed_baseline, tmp_path  # noqa: F811
):
    identity_doc = executed_baseline / "package_identity.json"
    baseline_doc = executed_baseline / "baseline_result.json"
    if case == "missing_declared_key":
        overrides, gate, needle = remove_declared_key(tmp_path)
    elif case == "key_names_a_channel":
        overrides, gate, needle = point_key_at_a_channel(tmp_path)
    elif case == "wrong_fingerprint":
        overrides, gate, needle = corrupt_the_identity(tmp_path, identity_doc)
    else:
        overrides, gate, needle = stale_the_manifest(tmp_path)

    results = tmp_path / "preflight_results.json"
    argv = gates_argv(
        tmp_path,
        manifest=overrides.get("manifest", MANIFEST),
        groups=overrides.get("groups", DECLARATION),
        identity=overrides.get("identity", identity_doc),
        baseline=baseline_doc,
        results=results,
    )
    done = run_preflight(*argv)

    assert done.returncode != 0, "a refused gate must exit non-zero"
    document = json.loads(results.read_text())
    assert {g["gate"] for g in document["gates"]} == ALL_SIX, "D9: complete, not torn"
    assert document["outcome"] == "fail"

    failing = next(g for g in document["gates"] if g["gate"] == gate)
    assert failing["status"] == "fail"
    assert needle in failing["detail"], failing["detail"]

    # Every other check carried its real outcome rather than being abandoned.
    others = [g for g in document["gates"] if g["gate"] != gate]
    assert all(g["status"] in ("pass", "fail") for g in others)
    assert any(g["status"] == "pass" for g in others)


def test_the_wrong_fingerprint_message_names_both_values(executed_baseline, tmp_path):  # noqa: F811
    overrides, _, _ = corrupt_the_identity(tmp_path, executed_baseline / "package_identity.json")
    declared = json.loads(
        (executed_baseline / "package_identity.json").read_text()
    )["identity"]["digest"]
    results = tmp_path / "preflight_results.json"
    run_preflight(*gates_argv(
        tmp_path, identity=overrides["identity"],
        baseline=executed_baseline / "baseline_result.json", results=results,
    ))
    detail = next(
        g for g in json.loads(results.read_text())["gates"] if g["gate"] == "identity"
    )["detail"]
    assert "0" * 64 in detail and declared in detail


def test_an_unreadable_input_is_did_not_run_with_its_condition(executed_baseline, tmp_path):  # noqa: F811, E501
    """A gate that never got the chance must not look like a gate that refused."""
    broken = tmp_path / "package_identity.json"
    broken.write_text("{not json")
    results = tmp_path / "preflight_results.json"
    done = run_preflight(*gates_argv(
        tmp_path, identity=broken,
        baseline=executed_baseline / "baseline_result.json", results=results,
    ))
    assert done.returncode != 0
    document = json.loads(results.read_text())
    gate = next(g for g in document["gates"] if g["gate"] == "identity")
    assert gate["status"] == "did not run"
    assert "not valid JSON" in gate["detail"]
    assert "identity_document" not in document["input_digests"]
    # The checks that did not depend on it still ran.
    assert next(
        g for g in document["gates"] if g["gate"] == "manifest_currency"
    )["status"] == "pass"


def test_a_baseline_executed_under_another_identity_is_refused(executed_baseline, tmp_path):  # noqa: F811, E501
    """Invariant 5: the identity gated and the identity executed are one value."""
    baseline = _copy_json(
        executed_baseline / "baseline_result.json", tmp_path / "baseline_result.json",
        lambda d: d["executed_under"].update(identity_digest="0" * 64),
    )
    results = tmp_path / "preflight_results.json"
    done = run_preflight(*gates_argv(
        tmp_path, identity=executed_baseline / "package_identity.json",
        baseline=baseline, results=results,
    ))
    assert done.returncode != 0
    gate = next(
        g for g in json.loads(results.read_text())["gates"] if g["gate"] == "identity"
    )
    assert gate["status"] == "fail"
    assert "different identity" in gate["detail"]


def test_a_wrong_headline_is_refused_naming_the_channel(executed_baseline, tmp_path):  # noqa: F811
    baseline = _copy_json(
        executed_baseline / "baseline_result.json", tmp_path / "baseline_result.json",
        lambda d: d["channels"].update({f"{P}lcoe_calc__lcoe": 999.0}),
    )
    results = tmp_path / "preflight_results.json"
    run_preflight(*gates_argv(
        tmp_path, identity=executed_baseline / "package_identity.json",
        baseline=baseline, results=results,
    ))
    gate = next(
        g for g in json.loads(results.read_text())["gates"] if g["gate"] == "baseline_headline"
    )
    assert gate["status"] == "fail"
    assert f"{P}lcoe_calc__lcoe" in gate["detail"] and "999.0" in gate["detail"]


def test_a_differing_baseline_verdict_is_refused_naming_the_constraint(
    executed_baseline, tmp_path  # noqa: F811
):
    def flip(data):
        data["verdicts"][0]["status"] = "violated"

    baseline = _copy_json(
        executed_baseline / "baseline_result.json", tmp_path / "baseline_result.json", flip
    )
    name = json.loads(baseline.read_text())["verdicts"][0]["source_local_identity"]
    results = tmp_path / "preflight_results.json"
    run_preflight(*gates_argv(
        tmp_path, identity=executed_baseline / "package_identity.json",
        baseline=baseline, results=results,
    ))
    gate = next(
        g for g in json.loads(results.read_text())["gates"] if g["gate"] == "baseline_headline"
    )
    assert gate["status"] == "fail"
    assert name in gate["detail"] and "violated" in gate["detail"]


def test_a_dirty_tree_is_refused_naming_the_file(repo_root, tmp_path):
    """The cleanliness gate must see a tree git can see, and name what it found there."""
    tree = repo_root / "tests" / "study" / "_preflight_clean_probe"
    tree.mkdir()
    intruder = tree / "left_behind.txt"
    results = tmp_path / "clean.json"
    try:
        run_preflight("clean", "--package", str(tree), "--out", str(results), expect=0)
        intruder.write_text("a file a run left behind\n")
        done = run_preflight("clean", "--package", str(tree), "--out", str(results))
        assert done.returncode != 0
        document = json.loads(results.read_text())
        assert document["outcome"] == "fail"
        gate = document["gates"][0]
        assert gate["gate"] == "package_clean" and gate["status"] == "fail"
        assert "left_behind.txt" in gate["detail"]
    finally:
        intruder.unlink(missing_ok=True)
        tree.rmdir()
