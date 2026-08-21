"""The identity recipe, its canonical text, and the gate that recomputes it.

The design probe confirmed the *mechanism* — the teax stack accepts a computed
fingerprint at the loader seam, and a store bound to one refuses another — but it
emitted a single `adapter <digest>` line where the design emits one
`adapter <path> <sha256>` line per declared source (N1). Nothing rests on the
probe's bytes. These tests pin the designed ones.
"""

import hashlib
import json

import jsonschema
import pytest

from scripts.study import common, identity

SEALED = "ab" * 32
MOD = [("inputs/x.json", "11" * 32)]
SRC = [("a/route_adapter.py", "22" * 32)]


def test_the_recipe_canonical_text_is_exactly_this():
    assert identity.canonical_text(SEALED, MOD, SRC) == (
        "effective-executable-fingerprint/v1\n"
        "sealed " + "ab" * 32 + "\n"
        "modified inputs/x.json " + "11" * 32 + "\n"
        "adapter a/route_adapter.py " + "22" * 32 + "\n"
    )


def test_the_digest_is_sha256_of_that_text():
    text = identity.canonical_text(SEALED, MOD, SRC)
    assert identity.effective_digest(SEALED, MOD, SRC) == (
        hashlib.sha256(text.encode("utf-8")).hexdigest()
    )


def test_the_canonical_text_sorts_by_path_not_by_argument_order():
    """Two agents listing the same files in different orders must agree."""
    a = [("z/b.py", "33" * 32), ("a/a.py", "44" * 32)]
    assert identity.canonical_text(SEALED, MOD, a) == identity.canonical_text(
        SEALED, MOD, list(reversed(a))
    )


def test_adapter_source_digest_is_over_the_sorted_adapter_lines_alone():
    """S1: the record snapshot takes one sha256 while a route declares several sources."""
    sources = [("z/b.py", "33" * 32), ("a/a.py", "44" * 32)]
    expected = hashlib.sha256(
        ("adapter a/a.py " + "44" * 32 + "\nadapter z/b.py " + "33" * 32 + "\n").encode("utf-8")
    ).hexdigest()
    assert identity.adapter_source_digest(sources) == expected
    assert identity.adapter_source_digest(list(reversed(sources))) == expected


def test_touching_any_of_the_three_inputs_changes_the_digest():
    base = identity.effective_digest(SEALED, MOD, SRC)
    assert identity.effective_digest("cd" * 32, MOD, SRC) != base
    assert identity.effective_digest(SEALED, [("inputs/x.json", "99" * 32)], SRC) != base
    assert identity.effective_digest(SEALED, MOD, [("a/route_adapter.py", "99" * 32)]) != base


# ------------------------------------------------------------------ the document


def test_the_sealed_kind_reduces_to_the_sealed_fingerprint(real_package_path):
    from scripts.study import manifest as manifest_mod

    doc = identity.build_sealed(package_name="ignored", package_root=real_package_path)
    sealed = manifest_mod.read_executable_fingerprint(real_package_path)
    assert doc["identity"]["kind"] == "sealed"
    assert doc["identity"]["digest"] == sealed
    assert doc["identity"]["allowed_modified_files"] == []
    assert doc["identity"]["adapter_sources"] == []
    # The sealed case is the degenerate member of the same gate, not a special case.
    assert identity.recompute(doc, real_package_path) == sealed


def test_an_effective_identity_that_bypasses_nothing_is_refused():
    """An empty allowed-modified set is the sealed case wearing the wrong label."""
    with pytest.raises(identity.IdentityError) as exc:
        identity.build_effective(
            package_name="p", package_root=".", sealed_fingerprint=SEALED,
            allowed_modified=[], adapter_sources=SRC, glue_ledger=[],
        )
    assert "sealed" in str(exc.value)


def test_the_documents_validate_against_the_committed_schema(real_package_path, load_schema):
    schema = load_schema("package_identity.v1")
    jsonschema.validate(identity.build_sealed(
        package_name="p", package_root=real_package_path), schema)
    jsonschema.validate(
        identity.build_effective(
            package_name="p", package_root=real_package_path, sealed_fingerprint=SEALED,
            allowed_modified=MOD, adapter_sources=SRC,
            glue_ledger=[{"rung": "g3", "keys": ["k"], "supplies": "a value",
                          "independently_verified": False, "note": "n"}],
        ),
        schema,
    )


def test_the_document_is_deterministic_across_working_directories(real_package_path, tmp_path,
                                                                  monkeypatch):
    """Paths come from the repo root, never from the caller's cwd."""
    first = identity.build_sealed(package_name="p", package_root=real_package_path)
    monkeypatch.chdir(tmp_path)
    assert identity.build_sealed(package_name="p", package_root=real_package_path) == first


# ---------------------------------------------------------------------- the gate


def _effective_doc(package_root, modified_rel, source_rel):
    from scripts.study import manifest as manifest_mod

    return identity.build_effective(
        package_name=manifest_mod.read_package_name(package_root),
        package_root=package_root,
        sealed_fingerprint=manifest_mod.read_executable_fingerprint(package_root),
        allowed_modified=[(r, manifest_mod.sha256_file(package_root / r)) for r in modified_rel],
        adapter_sources=[
            (r, manifest_mod.sha256_file(manifest_mod.repo_root() / r)) for r in source_rel
        ],
        glue_ledger=[],
    )


ADAPTER_SOURCE = "exploration/stellarator_e2e/studies/oracle_entry.py"
GLUE_FILES = ["inputs/stellarator_plant_params.json", "pipelines/pipeline.yaml"]


def test_the_gate_passes_on_the_real_package(real_package_path):
    doc = _effective_doc(real_package_path, GLUE_FILES, [ADAPTER_SOURCE])
    assert identity.assert_matches(doc, real_package_path) == doc["identity"]["digest"]


def test_a_recompute_mismatch_fails_naming_both_values(real_package_path):
    doc = _effective_doc(real_package_path, GLUE_FILES, [ADAPTER_SOURCE])
    declared = doc["identity"]["digest"]
    doc["identity"]["digest"] = "0" * 64
    with pytest.raises(identity.IdentityError) as exc:
        identity.assert_matches(doc, real_package_path)
    assert "0" * 64 in str(exc.value) and declared in str(exc.value)


def test_a_missing_declared_file_fails_naming_it(real_package_path):
    doc = _effective_doc(real_package_path, GLUE_FILES, [ADAPTER_SOURCE])
    doc["identity"]["adapter_sources"].append({"path": "no/such/file.py", "sha256": "0" * 64})
    with pytest.raises(identity.IdentityError) as exc:
        identity.recompute(doc, real_package_path)
    assert "no/such/file.py" in str(exc.value)


def test_the_gate_recomputes_and_does_not_trust(real_package_path, tmp_path):
    """A route could assert any digest. The gate reads the bytes instead."""
    import shutil

    copy = tmp_path / "pkg"
    shutil.copytree(real_package_path, copy)
    doc = _effective_doc(copy, GLUE_FILES, [ADAPTER_SOURCE])
    identity.assert_matches(doc, copy)
    target = copy / "inputs" / "stellarator_plant_params.json"  # an allowed-modified file
    target.write_text(target.read_text().replace("}", ", \"x\": 1}", 1))
    with pytest.raises(identity.IdentityError) as exc:
        identity.assert_matches(doc, copy)
    assert "digest mismatch" in str(exc.value)


def test_a_sealed_artifact_outside_the_allowed_set_fails_naming_the_file(
    real_package_path, tmp_path
):
    """Invariant 3 at the document level: the exception may not widen."""
    import shutil

    copy = tmp_path / "pkg"
    shutil.copytree(real_package_path, copy)
    doc = _effective_doc(copy, GLUE_FILES, [ADAPTER_SOURCE])
    target = copy / "inputs" / "mfe_plant_params.json"  # sealed, NOT in the allowed set
    target.write_text(target.read_text().replace("}", ", \"x\": 1}", 1))
    with pytest.raises(identity.IdentityError) as exc:
        identity.assert_seal_outside_allowed_set(doc, copy)
    assert "inputs/mfe_plant_params.json" in str(exc.value)


def test_an_allowed_modified_file_that_is_not_a_sealed_artifact_is_refused(real_package_path):
    doc = _effective_doc(real_package_path, GLUE_FILES, [ADAPTER_SOURCE])
    doc["identity"]["allowed_modified_files"].append(
        {"path": "not/sealed.json", "sha256": "0" * 64}
    )
    with pytest.raises(identity.IdentityError) as exc:
        identity.assert_seal_outside_allowed_set(doc, real_package_path)
    assert "not/sealed.json" in str(exc.value)


# ------------------------------------------------------------------- load/write


def test_load_refuses_a_wrong_schema_version(tmp_path, real_package_path):
    doc = identity.build_sealed(package_name="p", package_root=real_package_path)
    doc["schema_version"] = "study-package-identity/v2"
    path = common.write_document(doc, tmp_path / "package_identity.json")
    with pytest.raises(identity.IdentityError) as exc:
        identity.load(path)
    assert "v2" in str(exc.value)


@pytest.mark.parametrize(
    "mutate,needle",
    [
        (lambda d: d["identity"].pop("digest"), "digest"),
        (lambda d: d["identity"].update(kind="other"), "kind"),
        (lambda d: d["identity"].update(recipe="nope/v1"), "recipe"),
        (lambda d: d["identity"].update(allowed_modified_files={}), "allowed_modified_files"),
        (lambda d: d.update(glue_ledger={}), "glue_ledger"),
    ],
)
def test_load_refuses_a_malformed_document(mutate, needle, tmp_path, real_package_path):
    doc = identity.build_sealed(package_name="p", package_root=real_package_path)
    mutate(doc)
    path = common.write_document(doc, tmp_path / "package_identity.json")
    with pytest.raises(identity.IdentityError) as exc:
        identity.load(path)
    assert needle in str(exc.value)


def test_a_written_document_round_trips_and_its_digest_is_stable(tmp_path, real_package_path):
    doc = identity.build_sealed(package_name="p", package_root=real_package_path)
    path = common.write_document(doc, tmp_path / "results" / "package_identity.json")
    assert identity.load(path) == doc
    assert json.loads(path.read_text()) == doc
    assert common.digest_of_document(doc) == hashlib.sha256(path.read_bytes()).hexdigest()
