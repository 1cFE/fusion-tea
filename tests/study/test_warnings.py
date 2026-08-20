"""Advisory is advisory: warnings never change which keys are traced.

Invariant 3. A group with warnings and the same group with the manifest tie
removed produce identical trace fields.
"""

import json

from tests.study.conftest import DATA_DIR, REAL_MANIFEST, REAL_PACKAGE, run_tool

EXTRAS = DATA_DIR / "axes.extras.json"

TRACE_FIELDS = (
    "declared_keys",
    "constraints_reachable",
    "constraints_unreachable",
    "bounds",
    "objectives_reachable",
    "objectives_unreachable",
    "trace_size",
    "no_constraint_response",
    "sibling_candidates",
)


def group_by_axis(doc, axis):
    return next(g for g in doc["groups"] if g["axis"] == axis)


def trace_fields(doc, axis):
    group = group_by_axis(doc, axis)
    return {field: group[field] for field in TRACE_FIELDS}


def warning_kinds(doc, axis):
    return sorted(w["kind"] for w in group_by_axis(doc, axis)["warnings"])


def test_advisory_never_changes_the_trace(package_copy):
    """Remove the manifest's tie catalog entry: the warning goes, the trace does not
    move a single field."""
    with_tie = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    copy = package_copy(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    copy.edit_manifest(lambda data: data.update(ties=[]))
    rc, out, err = copy.run()
    assert rc == 0, err
    without_tie = json.loads(out)

    assert trace_fields(with_tie, "R_partial") == trace_fields(without_tie, "R_partial")
    assert warning_kinds(with_tie, "R_partial") == ["tie_candidate"]
    assert warning_kinds(without_tie, "R_partial") == []


def test_the_tie_candidate_names_the_key_and_says_it_was_not_added():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    (warning,) = group_by_axis(doc, "R_partial")["warnings"]
    assert warning["kind"] == "tie_candidate"
    assert "magnet__R0" in warning["detail"]
    assert "not added" in warning["detail"]


def test_a_declared_tie_earns_no_candidate_warning():
    """The tie is already in the group, so there is nothing to suggest."""
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, DATA_DIR / "axes.known_answers.json")
    assert warning_kinds(doc, "R+tie") == []
    assert warning_kinds(doc, "R") == ["tie_candidate"]


def test_suffix_siblings_land_in_their_own_named_field():
    """M2: sibling_candidates is an Appendix A name and is never folded into
    warnings — there is exactly one place to read them."""
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    group = group_by_axis(doc, "n_mod")
    assert len(group["sibling_candidates"]) == 17  # 18 keys share the suffix, 1 declared
    assert all(key.endswith("__n_mod") for key in group["sibling_candidates"])
    assert group["sibling_candidates"] == sorted(group["sibling_candidates"])
    assert warning_kinds(doc, "n_mod") == []
    assert "sibling" not in json.dumps(group["warnings"])


def test_suffix_siblings_never_join_the_traced_set():
    """Invariant 3: 17 candidates, 1 traced key."""
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    group = group_by_axis(doc, "n_mod")
    assert len(group["declared_keys"]) == 1
    assert group["sibling_candidates"]


def test_the_declared_tie_is_not_a_suffix_sibling():
    """The concrete demonstration that suffixes are not identity: magnet__R0 has
    suffix R0, so no suffix scan will ever surface it — the tie must be declared."""
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    siblings = group_by_axis(doc, "R_partial")["sibling_candidates"]
    assert not any(key.endswith("magnet__R0") for key in siblings)


def test_a_key_in_two_groups_earns_a_document_warning():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    duplicates = [w for w in doc["warnings"] if w["kind"] == "duplicate_key_across_groups"]
    assert len(duplicates) == 1
    assert "geom__R" in duplicates[0]["detail"]
    assert "R_partial" in duplicates[0]["detail"] and "R_shared" in duplicates[0]["detail"]


def test_provenance_drift_warns_on_both_recorded_fingerprints(package_copy):
    """S5: the drift case is a re-pin that left recorded_provenance stale. Neither
    fingerprint gates — gating on either is the false gate the spec ruled out."""
    copy = package_copy(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    copy.edit_manifest(
        lambda data: data["fingerprints"]["recorded_provenance"].update(
            semantic_fingerprint="stale" * 12, executable_fingerprint="alsostale" * 7
        )
    )
    rc, out, err = copy.run()
    assert rc == 0, err  # provenance never gates
    drift = [w for w in json.loads(out)["warnings"] if w["kind"] == "provenance_drift"]
    assert len(drift) == 2
    assert any("executable_fingerprint" in w["detail"] for w in drift)
    assert any("semantic_fingerprint" in w["detail"] for w in drift)
