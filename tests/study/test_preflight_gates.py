"""The six checks pass on the real package, and the document says so completely.

Preflight's inputs are two documents the route writes at load and at the baseline
point, so this module executes the baseline once (session-scoped) and gates against
it. The committed package is read, never written.
"""

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = REPO_ROOT / "scripts" / "study" / "preflight.py"
DECLARATION = REPO_ROOT / "tests" / "study" / "data" / "axes.known_answers.json"
MANIFEST = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies" / "manifest.json"
PACKAGE = REPO_ROOT / "exploration" / "stellarator_e2e" / "pkg" / "stellarator_tea"

ALL_SIX = {
    "declared_keys",
    "sibling_scan",
    "identity",
    "manifest_currency",
    "baseline_headline",
    "package_clean",
}
#: Record §9's five rows: the two fingerprint checks share one (S2).
RECORD_ROWS = {
    "declared_keys": "Declared-group key validation",
    "sibling_scan": "Suffix-sibling scan (warnings only)",
    "identity": "Manifest / package fingerprint match",
    "manifest_currency": "Manifest / package fingerprint match",
    "baseline_headline": "Baseline gate against the pinned headline",
    "package_clean": "Package cleanliness",
}


@pytest.fixture(scope="session")
def executed_baseline(tmp_path_factory, stock_simkit_session_path):
    """One executed baseline point plus the two documents it deposits (stock route)."""
    studies = str(REPO_ROOT / "exploration" / "stellarator_e2e" / "studies")
    if studies not in sys.path:
        sys.path.insert(0, studies)
    import study_route

    out = tmp_path_factory.mktemp("baseline")
    study_route.execute_baseline(out)
    return out


def run_preflight(*argv, expect=None):
    done = subprocess.run(
        [sys.executable, str(PREFLIGHT), *argv],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if expect is not None:
        assert done.returncode == expect, f"exit {done.returncode}\n{done.stderr}"
    return done


def gates_argv(out_dir, *, package=PACKAGE, manifest=MANIFEST, groups=DECLARATION,
               identity=None, baseline=None, results=None):
    return [
        "gates",
        "--package", str(package),
        "--manifest", str(manifest),
        "--groups", str(groups),
        "--identity", str(identity),
        "--baseline-result", str(baseline),
        "--out", str(results or out_dir / "preflight_results.json"),
    ]


@pytest.fixture
def gates_document(executed_baseline, tmp_path):
    results = tmp_path / "preflight_results.json"
    done = run_preflight(
        *gates_argv(tmp_path,
                    identity=executed_baseline / "package_identity.json",
                    baseline=executed_baseline / "baseline_result.json",
                    results=results),
        expect=0,
    )
    return json.loads(results.read_text()), done


def test_all_six_checks_pass_on_the_real_package(gates_document):
    document, _ = gates_document
    assert document["outcome"] == "pass"
    assert {g["gate"] for g in document["gates"]} == ALL_SIX
    assert all(g["status"] == "pass" for g in document["gates"]), document["gates"]


def test_the_results_document_validates_against_its_schema(gates_document, load_schema):
    document, _ = gates_document
    jsonschema.validate(document, load_schema("preflight_results.v1"))


def test_the_document_carries_a_digest_for_every_input_it_read(gates_document):
    document, _ = gates_document
    assert set(document["input_digests"]) == {
        "manifest", "axis_declaration", "identity_document", "baseline_result"
    }
    assert all(len(d) == 64 for d in document["input_digests"].values())
    assert all(not Path(p).is_absolute() for p in document["inputs"].values())


def test_the_six_results_map_onto_record_section_9s_five_rows(gates_document):
    """S2: the two fingerprint checks share a row, and its detail carries both."""
    document, _ = gates_document
    assert {RECORD_ROWS[g["gate"]] for g in document["gates"]} == set(RECORD_ROWS.values())
    assert len(set(RECORD_ROWS.values())) == 5
    shared = [g for g in document["gates"] if g["gate"] in ("identity", "manifest_currency")]
    assert len(shared) == 2 and all(g["detail"] for g in shared)


def test_the_tool_reports_its_own_revision_as_a_named_recipe_over_a_named_file_list(
    gates_document
):
    document, _ = gates_document
    digest = document["tool"]["source_digest"]
    assert digest["recipe"] == "tool-source-digest/v1"
    assert [f["path"] for f in digest["files"]] == sorted(f["path"] for f in digest["files"])
    assert "scripts/study/preflight.py" in [f["path"] for f in digest["files"]]


def test_the_sibling_scan_is_advisory_and_can_never_fail(gates_document):
    document, _ = gates_document
    scan = next(g for g in document["gates"] if g["gate"] == "sibling_scan")
    assert scan["status"] == "pass"


def test_the_identity_gate_reports_the_recomputed_digest(gates_document, executed_baseline):
    document, _ = gates_document
    declared = json.loads(
        (executed_baseline / "package_identity.json").read_text()
    )["identity"]["digest"]
    gate = next(g for g in document["gates"] if g["gate"] == "identity")
    assert declared in gate["detail"]


def test_the_clean_subcommand_gates_the_package_alone(tmp_path):
    results = tmp_path / "clean.json"
    run_preflight("clean", "--package", str(PACKAGE), "--out", str(results), expect=0)
    document = json.loads(results.read_text())
    assert document["subcommand"] == "clean"
    assert [g["gate"] for g in document["gates"]] == ["package_clean"]
    assert document["outcome"] == "pass"


def test_preflight_imports_no_teax_and_no_adapter():
    """Invariant 1 in the strongest available form: it runs with neither importable."""
    text = PREFLIGHT.read_text()
    for needle in ("simkit", "era_adapter", "oracle_entry", "StudyRunner", "StudyQuery"):
        assert needle not in text
