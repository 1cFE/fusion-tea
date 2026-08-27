"""R-C9: a package that verifies cleanly but is not the lineage the caller named.

This is the Item 6 failure one level up — a manifest and a package that agreed with
themselves and not with each other, with nothing at the hop to catch it. Gate 9 is the
check that was missing, and it is last because a package that failed an earlier gate has
no lineage worth reporting.
"""

from __future__ import annotations

from tests.study.conftest import run_seam


def _one_digit_off(digest: str) -> str:
    return ("1" if digest[0] == "0" else "0") + digest[1:]


def test_wrong_expected_fingerprint_refuses_at_gate_9(integration_workspace, tmp_path):
    out = tmp_path / "out"
    wrong = _one_digit_off(integration_workspace.expected_semantic_fingerprint)
    argv = integration_workspace.request_argv(
        out, **{"--expected-semantic-fingerprint": wrong}
    )

    document = run_seam(argv, out)

    blocker = document["blocker"]
    assert blocker["gate"] == "lineage"
    assert blocker["producer"] == "scripts/integrate.py"
    assert blocker["scope"] == "request"
    assert blocker["mode"] == "refused"
    assert blocker["condition"] == "lineage-mismatch"
    assert blocker["expected"]["semantic_fingerprint"] == wrong
    assert blocker["actual"]["semantic_fingerprint"] == (
        integration_workspace.expected_semantic_fingerprint
    )
    assert [gate["status"] for gate in document["gates"][:9]] == ["pass"] * 9, (
        "the whole sequence must have passed for a lineage mismatch to mean anything"
    )
    assert document["gates"][9]["status"] == "fail", (
        "gate 9 read both fingerprints and compared them; recording it 'not reached' would "
        "tell a reader the lineage was never checked"
    )
    assert document["gates"][9]["detail"] == blocker["detail"]
    assert document["candidate"] is None


def test_absent_expected_fingerprints_could_not_run_rather_than_pass(
    integration_workspace, tmp_path
):
    out = tmp_path / "out"
    argv = integration_workspace.request_argv(
        out,
        **{"--expected-semantic-fingerprint": None,
           "--expected-executable-fingerprint": None},
    )
    document = run_seam(argv, out)
    blocker = document["blocker"]
    assert blocker["gate"] == "lineage"
    assert blocker["mode"] == "could_not_run"
    assert blocker["condition"] == "input-missing"
    assert document["gates"][9]["status"] == "did not run"
    assert "executable_fingerprint" in blocker["detail"]
    assert "semantic_fingerprint" in blocker["detail"]
