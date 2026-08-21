"""The multi-pipeline stance, asserted against a synthetic two-pipeline package.

This is the one behaviour with no real package data behind it — only
``mfe_stellarator.yaml`` exists in the stellarator package — so it gets a fixture
built for the purpose, and the fixture is read by hand before it is trusted.
"""

import json

import pytest

from tests.study.conftest import SYNTHETIC_DIR, run_tool


@pytest.fixture(scope="module")
def synthetic_report():
    return run_tool(
        SYNTHETIC_DIR / "pkg", SYNTHETIC_DIR / "manifest.json", SYNTHETIC_DIR / "axes.json"
    )


def group_by_axis(doc, axis):
    return next(g for g in doc["groups"] if g["axis"] == axis)


def reached(doc, axis):
    return sorted(
        c["source_local_identity"] for c in group_by_axis(doc, axis)["constraints_reachable"]
    )


def test_graph_is_package_scoped_across_files(synthetic_report):
    """A key declared through pipeline A's entry point reaches the constraint that
    pipeline B defines, through the channel A produces and B consumes."""
    assert reached(synthetic_report, "cross") == ["a_ok", "b_ok"]
    assert group_by_axis(synthetic_report, "cross")["objectives_reachable"] == ["w", "y"]


def test_the_cross_file_reach_discriminates(synthetic_report):
    """Not everything is reachable from everything: B's own key never reaches A."""
    assert reached(synthetic_report, "b_only") == ["b_ok"]
    group = group_by_axis(synthetic_report, "b_only")
    assert group["objectives_reachable"] == ["w"]
    assert group["objectives_unreachable"] == ["y"]


def test_a_literal_operand_comes_from_predicate_ir(synthetic_report):
    """R8: b_ok compares a computed channel against a literal that exists in no artifact."""
    b_ok = next(
        c
        for c in group_by_axis(synthetic_report, "cross")["constraints_reachable"]
        if c["source_local_identity"] == "b_ok"
    )
    literal = next(o for o in b_ok["operands"] if o["class"] == "literal")
    assert literal["value"] == 0.0
    assert "ref" not in literal


def _duplicate_channel_across_files(copy):
    copy.edit(
        "pipelines/b.yaml",
        "root: RootModel[float] syn__b__w",
        "root: RootModel[float] syn__a__y",
    )


def _second_entrypoint_in_one_file(copy):
    copy.edit("pipelines/a.yaml", "module_type: synthetic.ACalcModule", "module_type: EntryPoint")


def _stray_yml_file(copy):
    copy.write("pipelines/c.yml", "metadata: {}\nmodules: {}\n")


@pytest.mark.parametrize(
    "mutate,expect,repin",
    [
        (_duplicate_channel_across_files, "produced by more than one module", True),
        (_second_entrypoint_in_one_file, "expected exactly one EntryPoint", True),
        # The stray file changes no digested byte, and the glob check raises before
        # any digest is compared, so re-pinning would only re-raise the same error.
        (_stray_yml_file, "'*.yaml' glob would miss", False),
    ],
)
def test_mechanical_failure(synthetic_copy, mutate, expect, repin, tmp_path):
    mutate(synthetic_copy)
    out_path = tmp_path / "indicators.json"
    rc, out, err = synthetic_copy.run(repin=repin, out=out_path)
    assert rc != 0
    assert expect in err
    assert out == ""
    assert not out_path.exists()  # Invariant 1


def test_a_duplicate_channel_names_both_producing_modules(synthetic_copy):
    _duplicate_channel_across_files(synthetic_copy)
    _, _, err = synthetic_copy.run()
    assert "syn__a_calc" in err and "syn__b_calc" in err
    assert "pipelines/b.yaml" in err


def test_a_module_declared_in_two_files_is_a_failure(synthetic_copy):
    synthetic_copy.edit("pipelines/b.yaml", "syn__b_calc:", "syn__a_calc:")
    rc, out, err = synthetic_copy.run()
    assert rc != 0
    assert "declared in two pipeline files" in err
    assert out == ""


def test_the_assert_before_mutating_rule_fires(synthetic_copy):
    """The factory's own guard, proven once: a mutation whose target is not there
    fails the test rather than quietly running against an unmodified file."""
    with pytest.raises(AssertionError, match="mutation target not found"):
        synthetic_copy.edit("pipelines/a.yaml", "module_type: NotAThingInThisFile", "x")


def test_the_synthetic_manifest_pin_is_live():
    """The committed fixture's own pin matches its committed bytes, so a test that
    forgets to re-pin fails at the gate rather than passing for the wrong reason."""
    from scripts.study import manifest

    pinned = json.loads((SYNTHETIC_DIR / "manifest.json").read_text())
    computed = manifest.indicator_input_fingerprint(SYNTHETIC_DIR / "pkg")
    assert pinned["fingerprints"]["indicator_inputs"]["digest"] == computed["digest"]
