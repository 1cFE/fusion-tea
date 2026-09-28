"""The pure half of build.py: what counts as added, changed, moved and removed, the calc-to-file
rule, the churn filter, and the manifest check. Small synthetic graphs; no git and no browser."""

import importlib.util
from pathlib import Path

import pytest

BUILDER = Path(__file__).resolve().parents[2] / "src/model_viz/evolution/build.py"
spec = importlib.util.spec_from_file_location("evolution_build", BUILDER)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def calc(path, formula, *, doc="doc", inputs=("a",), name=None):
    return {
        "display_path": path,
        "display_name": name or path.split("__")[-1],
        "node_id": "id:" + path,
        "calc_expressions": [formula, f"\nDocumentation:\n{doc}"],
        "expression_ir": None,
        "doc_comment": doc,
        "inputs": [{"name": n, "edge": {"kind": "literal", "value": 1}, "metadata": {"qualified_name": n}} for n in inputs],
        "outputs": [{"name": "out"}],
    }


def graph(*calcs):
    return {"calcs": list(calcs), "constraints": [], "occurrences": [], "attrs": []}


def test_added_removed_and_changed():
    before = graph(calc("p__keep", "x = a"), calc("p__edit", "y = a"), calc("p__gone", "z = a"))
    after = graph(calc("p__keep", "x = a"), calc("p__edit", "y = a * 2"), calc("p__new", "w = a"))
    d = build.diff_calcs(before, after)
    assert (d["added"], d["removed"], d["changed"], d["moved"], d["doc_only"]) == (["p__new"], ["p__gone"], ["p__edit"], {}, [])


def test_a_new_input_is_a_change():
    d = build.diff_calcs(graph(calc("p__c", "x = a")), graph(calc("p__c", "x = a", inputs=("a", "b"))))
    assert d["changed"] == ["p__c"]


def test_a_doc_edit_is_not_a_formula_change():
    # codegen appends the doc comment to calc_expressions; the signature must not see it
    d = build.diff_calcs(graph(calc("p__c", "x = a", doc="old")), graph(calc("p__c", "x = a", doc="new")))
    assert (d["changed"], d["doc_only"]) == ([], ["p__c"])


def test_a_relocated_calc_is_a_move_not_an_add_and_a_remove():
    before = graph(calc("root__coil_cost", "x = a"))
    after = graph(calc("root__magnet__coil_cost", "x = a"))
    d = build.diff_calcs(before, after)
    assert (d["added"], d["removed"], d["moved"], d["changed"]) == ([], [], {"root__magnet__coil_cost": "root__coil_cost"}, [])


def test_a_calc_moved_and_edited_is_both():
    d = build.diff_calcs(graph(calc("root__c", "x = a")), graph(calc("root__part__c", "x = a + 1")))
    assert (list(d["moved"]), d["changed"]) == (["root__part__c"], ["root__part__c"])


@pytest.mark.parametrize(
    "qualified_name, expected",
    [
        ("mfe_cooling_equipment::'Cooling Equipment'", "mfe_cooling_equipment/cooling_equipment_impl.py"),
        ("mfe_account_costs::'1cfe-Form Capital Charge'", "mfe_account_costs/n_1cfe_form_capital_charge_impl.py"),
        ("outer_pkg::inner_pkg::'Some Calc'", "outer_pkg/inner_pkg/some_calc_impl.py"),
    ],
)
def test_impl_relpath(qualified_name, expected):
    assert build.impl_relpath(qualified_name) == expected


def test_line_number_churn_is_not_a_change():
    churn = "diff --git a/x b/x\n--- a/x\n+++ b/x\n@@ -1,3 +1,3 @@\n-SysML Source: root-0/a.sysml:825\n+SysML Source: root-0/a.sysml:826\n"
    assert build.substantive_diff(churn) is None


def test_a_real_edit_survives_the_churn_filter():
    real = "diff --git a/x b/x\n--- a/x\n+++ b/x\n@@ -1,3 +1,4 @@\n-SysML Source: a:1\n+SysML Source: a:2\n+    raise ValueError('bad')\n"
    assert build.substantive_diff(real).startswith("@@ -1,3 +1,4 @@")


class FakeHistory:
    def __init__(self, versions):
        self._versions = versions

    def full_sha(self, sha):
        return sha

    def versions(self, last_sha, path):
        return self._versions


def manifest_of(*frames):
    return {"snapshot_path": "s.json", "baseline": {"sha": "v1"}, "frames": [{"slug": f"g{i}", "shas": list(shas)} for i, shas in enumerate(frames)]}


def test_manifest_matching_history_passes():
    assert build.check_manifest(manifest_of(["v2"], ["v3", "v4"]), FakeHistory(["v0", "v1", "v2", "v3", "v4"])) == ["v1", "v2", "v3", "v4"]


def test_a_version_in_no_frame_is_refused():
    with pytest.raises(build.BuildRefused, match=r"Versions in no frame: \['v3'\]"):
        build.check_manifest(manifest_of(["v2"], ["v4"]), FakeHistory(["v1", "v2", "v3", "v4"]))


def test_a_version_named_unframed_needs_no_frame():
    manifest = manifest_of(["v2"], ["v4"]) | {"unframed": [{"sha": "v3", "reason": "comments only"}]}
    assert build.check_manifest(manifest, FakeHistory(["v1", "v2", "v3", "v4"])) == ["v1", "v2", "v4"]


def test_an_unframed_entry_that_a_frame_also_lists_is_refused():
    manifest = manifest_of(["v2"], ["v3"]) | {"unframed": [{"sha": "v2", "reason": "x"}]}
    with pytest.raises(build.BuildRefused, match="unframed entries must be snapshot versions that no frame lists"):
        build.check_manifest(manifest, FakeHistory(["v1", "v2", "v3"]))


def test_a_commit_that_is_not_a_snapshot_version_is_refused():
    with pytest.raises(build.BuildRefused, match=r"not snapshot versions: \['zz'\]"):
        build.check_manifest(manifest_of(["v2", "zz"], ["v3"]), FakeHistory(["v1", "v2", "v3"]))
