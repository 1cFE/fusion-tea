"""F2 regression — a candidate blocked at triage reaches OPERATOR_QUEUE.

The spec names "paywall, login wall, repeated fetch failure" first among the
reasons to queue a source (`spec.md:39`). Those are found at triage, before
anything is worth calling `register` on, so they leave no receipt. Reading the
class from receipts alone closed such a run `BOUNDED_NEGATIVE` and wrote a
durable negative that then blocked the request — burying a named, human-
resolvable candidate under "nothing there."
"""

import json

import pytest
import research_seam

REQUEST = {
    "request_id": "REQ-200",
    "question": "Where is the paywalled conductor paper?",
    "consumer": "WI-031",
    "gap_type": "unsourced_value",
    "priority": "P1",
    "where_to_look": ["a publisher behind a paywall"],
    "limits": {"max_searches": 3, "max_captures": 2},
}


@pytest.fixture
def opened(tmp_path):
    root = tmp_path / "requests"
    root.mkdir()
    (root / "REQ-200.json").write_text(json.dumps(REQUEST))
    home = research_seam.SeamHome(root=root)
    result = research_seam.open_run(root / "REQ-200.json", home=home)
    assert result.exit_code == 0
    return home, result.run_dir


def _negative_path(home):
    return home.negatives / f"{research_seam.request_key(REQUEST)}.json"


def test_the_guides_paywall_sequence_closes_operator_queue(opened):
    """The exact sequence `docs/research_seam_operator_guide.md` teaches."""
    home, run_dir = opened
    research_seam.log_search(run_dir, "nb3sn conductor paper")
    research_seam.log_failure(run_dir, "https://example.org/b", "paywalled")

    returned = research_seam.close(run_dir)

    assert returned["class"] == "OPERATOR_QUEUE"
    assert returned["queued"] == [
        {"candidate": "https://example.org/b", "reason": "paywalled"}
    ]
    assert returned["registered"] == []


def test_no_durable_negative_is_written_when_a_candidate_is_queued(opened):
    """R-D6 exists to stop fruitless repeats, not to bury a source behind a paywall."""
    home, run_dir = opened
    research_seam.log_failure(run_dir, "https://example.org/b", "paywalled")

    returned = research_seam.close(run_dir)

    assert returned["negative"] is None
    assert not _negative_path(home).exists()


def test_a_queued_run_does_not_block_the_next_invocation(opened, tmp_path):
    """The whole point: the request stays searchable while a human works the queue."""
    home, run_dir = opened
    research_seam.log_failure(run_dir, "https://example.org/b", "login wall")
    assert research_seam.close(run_dir)["class"] == "OPERATOR_QUEUE"

    again = research_seam.open_run(home.root / "REQ-200.json", home=home)
    assert again.exit_code == 0, again.message


@pytest.mark.parametrize("reason", ["paywalled", "login wall required",
                                    "repeated fetch failure after 3 attempts"])
def test_every_spec_named_queue_reason_queues(opened, reason):
    home, run_dir = opened
    research_seam.log_failure(run_dir, "https://example.org/b", reason)
    returned = research_seam.close(run_dir)
    assert returned["class"] == "OPERATOR_QUEUE"
    assert returned["queued"][0]["reason"] == reason


def test_a_closed_failure_stays_in_the_negative_and_does_not_queue(opened):
    """A dead link nobody should chase is recorded, not routed to a person."""
    home, run_dir = opened
    research_seam.log_search(run_dir, "nb3sn conductor paper")
    research_seam.log_failure(run_dir, "https://example.org/gone", "404, link is dead",
                              disposition="closed")

    returned = research_seam.close(run_dir)

    assert returned["class"] == "BOUNDED_NEGATIVE"
    assert returned["queued"] == []
    negative = json.loads(_negative_path(home).read_text())
    assert negative["failures"] == [
        {"ref": "https://example.org/gone", "reason": "404, link is dead"}
    ]


def test_a_rejected_candidate_is_not_a_queue_entry(opened):
    """Triaged-and-judged-useless is not the same event as could-not-be-brought-in."""
    home, run_dir = opened
    research_seam.log_candidate(run_dir, "https://example.org/c", "rejected", "off topic")

    returned = research_seam.close(run_dir)

    assert returned["class"] == "BOUNDED_NEGATIVE"
    assert returned["queued"] == []


def test_a_registration_still_outranks_a_queued_candidate(opened):
    """Mapping-table row 1 is unchanged: the queue rides inside a REGISTERED return."""
    home, run_dir = opened
    research_seam.log_failure(run_dir, "https://example.org/b", "paywalled")
    receipts = run_dir / "receipts"
    receipts.mkdir(exist_ok=True)
    (receipts / "20260826T000000-001.json").write_text(json.dumps({
        "attempt": 1, "outcome": "registered", "candidate": "https://example.org/a",
        "slug": "widget", "path": "knowledge/sources/widget/", "source_id": "a" * 64,
        "triage": "keeper", "reason": "", "rule_id": None, "captured": True,
        "at": "2026-08-26T00:00:00+00:00",
    }))

    returned = research_seam.close(run_dir)

    assert returned["class"] == "REGISTERED"
    assert len(returned["queued"]) == 1
    assert returned["negative"] is None


def test_receipt_and_triage_queue_entries_share_one_shape(opened):
    """Both kinds of queue entry read the same to the operator."""
    home, run_dir = opened
    research_seam.log_failure(run_dir, "https://example.org/b", "paywalled")
    receipts = run_dir / "receipts"
    receipts.mkdir(exist_ok=True)
    (receipts / "20260826T000000-001.json").write_text(json.dumps({
        "attempt": 1, "outcome": "holdout_hit", "candidate": "https://example.org/h",
        "slug": None, "path": None, "source_id": None, "triage": "keeper",
        "reason": "term:example matched 1x", "rule_id": "term:example",
        "captured": False, "at": "2026-08-26T00:00:00+00:00",
    }))

    returned = research_seam.close(run_dir)

    assert returned["class"] == "OPERATOR_QUEUE"
    assert all(set(entry) == {"candidate", "reason"} for entry in returned["queued"])
    assert {e["candidate"] for e in returned["queued"]} == {
        "https://example.org/h", "https://example.org/b",
    }


def test_the_cli_defaults_a_failure_to_queued(opened):
    home, run_dir = opened
    assert research_seam.main(
        ["log", str(run_dir), "--failure", "https://example.org/b", "--reason", "paywalled"]
    ) == 0
    assert research_seam.close(run_dir)["class"] == "OPERATOR_QUEUE"


def test_the_cli_can_close_a_failure_explicitly(opened):
    home, run_dir = opened
    assert research_seam.main(
        ["log", str(run_dir), "--failure", "https://example.org/gone",
         "--reason", "404", "--disposition", "closed"]
    ) == 0
    assert research_seam.close(run_dir)["class"] == "BOUNDED_NEGATIVE"
