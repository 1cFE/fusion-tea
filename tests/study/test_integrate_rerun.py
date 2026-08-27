"""SC3: calling the seam twice on unchanged inputs does not mint a second identity.

What "the same identity" covers is stated rather than assumed. Three of the candidate's
eight fields are paths under ``--out-dir`` — the identity document, the baseline result and
the verification summary — and two runs are given different output directories on purpose,
so those three differ by construction and are not part of the claim. The claim is the five
fields that describe the package: its root, its manifest, its pin, and both fingerprints.
"""

from __future__ import annotations

import json

from tests.study.conftest import read_return, run_seam_raw

IDENTITY_FIELDS = (
    "package", "manifest", "pin", "semantic_fingerprint", "executable_fingerprint",
)
OUT_DIR_FIELDS = ("identity_document", "baseline_result", "verification_summary")


def test_two_runs_return_the_same_identity(integration_workspace, tmp_path):
    documents = []
    for name in ("a", "b"):
        out = tmp_path / name
        done = run_seam_raw(integration_workspace.request_argv(out))
        document = read_return(done, out)
        assert done.returncode == 0, json.dumps(document["blocker"], indent=2)
        documents.append(document)

    first, second = (document["candidate"] for document in documents)
    for field in IDENTITY_FIELDS:
        assert first[field] == second[field], field
    for field in OUT_DIR_FIELDS:
        assert first[field] != second[field], (
            f"{field} is a path under --out-dir and must differ between two runs"
        )


def test_the_second_run_is_a_candidate_not_a_refusal(integration_workspace, tmp_path):
    """Re-running regenerates again, in place, on a tree the first run already regenerated.

    That is only safe because regeneration on the pin is byte-stable; if it were not, the
    second run would find a dirtied tree and refuse. The contract holds either way — a
    re-run returns the prior identity or a blocker, never a second conflicting identity —
    but which branch fires is worth pinning, because a seam that always refused on its
    second call would be useless to a caller that retries.
    """
    for name in ("first", "second"):
        out = tmp_path / name
        done = run_seam_raw(integration_workspace.request_argv(out))
        document = read_return(done, out)
        assert document["class"] == "CANDIDATE", name + " run: " + json.dumps(
            document["blocker"], indent=2
        )[:2500]
