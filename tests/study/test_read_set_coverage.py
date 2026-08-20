"""M3 / Invariant 10: what the reader opens must be what the pin covers.

The reader resolves the inputs files from the EntryPoint block's own declared paths,
so a regenerated pipeline could point at a file the recipe never globbed — read by
the trace, digested by nobody, pin still green. Two conditions, both fail-closed.

Each copy is re-pinned before the run, so these tests reach the coverage check
rather than stopping at the pre-parse fingerprint gate.
"""

import json

from scripts.study import manifest

PIPELINE = "pipelines/mfe_stellarator.yaml"
ENTRY_REF = "system_design: SystemDesign ../inputs/system_design.json"


def test_a_ref_outside_the_pinned_file_list_fails(real_copy, tmp_path):
    """The file is inside the package and readable, but no digest covers it."""
    (real_copy.path / "handwritten" / "params.json").write_text(
        (real_copy.path / "inputs" / "system_design.json").read_text()
    )
    real_copy.edit(
        PIPELINE, ENTRY_REF, "system_design: SystemDesign ../handwritten/params.json"
    )
    out_path = tmp_path / "indicators.json"
    rc, out, err = real_copy.run(out=out_path)
    assert rc != 0
    assert "not in the manifest's pinned file list" in err
    assert "handwritten/params.json" in err
    assert out == ""
    assert not out_path.exists()


def test_a_ref_outside_the_package_root_fails(real_copy, tmp_path):
    outside = real_copy.path.parent / "outside.json"
    outside.write_text((real_copy.path / "inputs" / "system_design.json").read_text())
    real_copy.edit(PIPELINE, ENTRY_REF, "system_design: SystemDesign ../../outside.json")
    out_path = tmp_path / "indicators.json"
    rc, out, err = real_copy.run(out=out_path)
    assert rc != 0
    assert "resolves outside the package root" in err
    assert out == ""
    assert not out_path.exists()


def test_the_coverage_check_runs_before_the_inputs_are_opened(real_copy, tmp_path):
    """A file outside the package root is refused by path, not after being read."""
    outside = real_copy.path.parent / "not_even_json.txt"
    outside.write_text("this is not JSON at all")
    real_copy.edit(PIPELINE, ENTRY_REF, "system_design: SystemDesign ../../not_even_json.txt")
    _, _, err = real_copy.run(out=tmp_path / "x.json")
    assert "resolves outside the package root" in err
    assert "not valid JSON" not in err


def test_the_pinned_file_list_covers_exactly_what_the_reader_opens(real_package_path):
    """The invariant stated positively on the committed package."""
    from scripts.study import indicators

    parsed = indicators.read_pipelines(real_package_path)
    opened = {
        manifest.package_relative_posix(p, real_package_path)
        for p in parsed.artifact_paths
    } | {"contracts/model_contract.json"}
    pinned = {
        f["path"] for f in manifest.indicator_input_fingerprint(real_package_path)["files"]
    }
    assert opened == pinned


def test_pipelines_init_py_does_not_fail_the_glob_gate(real_package_path):
    """M1: __init__.py is a sealed artifact of every generated package. A rule that
    refused it would refuse the only package that exists."""
    assert (real_package_path / "pipelines" / "__init__.py").is_file()
    files = [f["path"] for f in manifest.indicator_input_fingerprint(real_package_path)["files"]]
    assert "pipelines/__init__.py" not in files


def test_a_renamed_inputs_file_is_followed_not_guessed(real_copy, tmp_path):
    """The reader resolves the EntryPoint's declared path rather than reconstructing
    inputs/<group>.json, so a rename is followed — and then caught by the pin."""
    (real_copy.path / "inputs" / "renamed.json").write_text(
        (real_copy.path / "inputs" / "system_design.json").read_text()
    )
    (real_copy.path / "inputs" / "system_design.json").unlink()
    real_copy.edit(PIPELINE, ENTRY_REF, "system_design: SystemDesign ../inputs/renamed.json")
    rc, out, err = real_copy.run(out=tmp_path / "y.json")
    assert rc == 0, err
    report = json.loads((tmp_path / "y.json").read_text())
    files = [f["path"] for f in report["package"]["indicator_input_fingerprint"]["files"]]
    assert "inputs/renamed.json" in files
    assert "inputs/system_design.json" not in files
