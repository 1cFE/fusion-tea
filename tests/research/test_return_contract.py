"""Phase 7 — the return class is computed from receipts, not from the agent's report.

Covers every row of the vocabulary-mapping table (design D13), plus R-A5's
"name the limit you stopped at" and R-B9's "disk is the truth".
"""

import json

import pytest
import research_seam

REQUEST = {
    "request_id": "REQ-100",
    "question": "Does the seam compute its own return class?",
    "consumer": "WI-031",
    "gap_type": "unsourced_value",
    "priority": "P1",
    "where_to_look": ["the receipts"],
    "limits": {"max_searches": 2, "max_captures": 2},
}


@pytest.fixture
def opened(tmp_path):
    root = tmp_path / "requests"
    root.mkdir()
    (root / "REQ-100.json").write_text(json.dumps(REQUEST))
    home = research_seam.SeamHome(root=root)
    result = research_seam.open_run(root / "REQ-100.json", home=home)
    assert result.exit_code == 0
    return home, result.run_dir


def _receipt(run_dir, outcome, *, triage="keeper", slug=None, path=None,
             source_id=None, rule_id=None, reason="", captured=True, scope="candidate"):
    directory = run_dir / "receipts"
    directory.mkdir(exist_ok=True)
    attempt = len(list(directory.iterdir())) + 1
    (directory / f"20260825T000000-{attempt:03d}.json").write_text(json.dumps({
        "attempt": attempt, "outcome": outcome, "candidate": f"https://example.org/{attempt}",
        "slug": slug, "path": path, "source_id": source_id, "triage": triage,
        "reason": reason, "rule_id": rule_id, "captured": captured, "scope": scope,
        "at": "2026-08-25T00:00:00+00:00",
    }))


MAPPING_TABLE_ROWS = [
    ("any registered", [("registered", "keeper")], "REGISTERED"),
    ("registered beside a queued candidate",
     [("registered", "keeper"), ("holdout_hit", "keeper")], "REGISTERED"),
    ("keeper duplicate only", [("duplicate", "keeper")], "REGISTERED"),
    ("rejected duplicate only", [("duplicate", "rejected")], "BOUNDED_NEGATIVE"),
    ("holdout hit only", [("holdout_hit", "keeper")], "OPERATOR_QUEUE"),
    ("capture failure only", [("capture_failed", "keeper")], "OPERATOR_QUEUE"),
    ("no receipts at all", [], "BOUNDED_NEGATIVE"),
]


@pytest.mark.parametrize("label,receipts,expected",
                         MAPPING_TABLE_ROWS, ids=[r[0] for r in MAPPING_TABLE_ROWS])
def test_class_computed_from_receipts(opened, label, receipts, expected):
    _, run_dir = opened
    for outcome, triage in receipts:
        _receipt(run_dir, outcome, triage=triage,
                 slug="s" if outcome in {"registered", "duplicate"} else None,
                 path="knowledge/sources/s/" if outcome in {"registered", "duplicate"} else None,
                 source_id="a" * 64 if outcome in {"registered", "duplicate"} else None)
    assert research_seam.close(run_dir)["class"] == expected


def test_a_keeper_duplicate_is_marked_pre_existing(opened):
    _, run_dir = opened
    _receipt(run_dir, "duplicate", slug="widget", path="knowledge/sources/widget/",
             source_id="a" * 64)
    returned = research_seam.close(run_dir)
    assert returned["class"] == "REGISTERED"
    assert returned["registered"] == [
        {"slug": "widget", "path": "knowledge/sources/widget/",
         "source_id": "a" * 64, "pre_existing": True}
    ]


def test_a_registration_is_not_marked_pre_existing(opened):
    _, run_dir = opened
    _receipt(run_dir, "registered", slug="widget", path="knowledge/sources/widget/",
             source_id="b" * 64)
    assert research_seam.close(run_dir)["registered"][0]["pre_existing"] is False


def test_queued_candidates_ride_inside_a_registered_return(opened):
    _, run_dir = opened
    _receipt(run_dir, "registered", slug="widget", path="knowledge/sources/widget/",
             source_id="b" * 64)
    _receipt(run_dir, "holdout_hit", rule_id="term:example", reason="term:example matched 1x")
    returned = research_seam.close(run_dir)
    assert returned["class"] == "REGISTERED"
    assert len(returned["queued"]) == 1
    assert returned["queued"][0]["reason"] == "term:example matched 1x"


def test_an_agent_claim_of_a_negative_is_overridden_by_a_registered_receipt(opened):
    """R-B9: what landed on disk is the truth; the agent's log entry is advisory."""
    _, run_dir = opened
    research_seam.log_candidate(run_dir, "https://example.org/1", "rejected", "nothing usable")
    _receipt(run_dir, "registered", slug="widget", path="knowledge/sources/widget/",
             source_id="b" * 64)
    returned = research_seam.close(run_dir, adequacy="exhausted")
    assert returned["class"] == "REGISTERED"
    assert returned["negative"] is None


def test_a_limit_reached_receipt_names_the_limit(opened):
    _, run_dir = opened
    _receipt(run_dir, "limit_reached", reason="run has spent its max_captures limit of 2",
             captured=False)
    returned = research_seam.close(run_dir)
    assert returned["class"] == "BOUNDED_NEGATIVE"
    assert returned["limit_reached"] == "max_captures"


def test_a_declared_search_limit_is_named_at_close(opened):
    _, run_dir = opened
    for i in range(REQUEST["limits"]["max_searches"]):
        research_seam.log_search(run_dir, f"query {i}")
    returned = research_seam.close(run_dir)
    assert returned["limit_reached"] == "max_searches"


def test_a_run_scoped_fault_with_no_candidates_is_a_blocker(opened):
    _, run_dir = opened
    research_seam.log_fault(run_dir, "registry is not writable")
    returned = research_seam.close(run_dir)
    assert returned["class"] == "BLOCKER"
    assert "not writable" in returned["reason"]


def test_a_run_scoped_fault_after_a_registration_stays_registered(opened):
    _, run_dir = opened
    _receipt(run_dir, "registered", slug="widget", path="knowledge/sources/widget/",
             source_id="b" * 64)
    research_seam.log_fault(run_dir, "registry went read-only afterwards")
    returned = research_seam.close(run_dir)
    assert returned["class"] == "REGISTERED"
    assert "read-only" in returned["reason"]


def test_every_return_resolves_to_native_references(opened):
    """R-A4: a reader reaches the evidence without reconstructing what the agent did."""
    _, run_dir = opened
    _receipt(run_dir, "registered", slug="widget", path="knowledge/sources/widget/",
             source_id="b" * 64)
    returned = research_seam.close(run_dir)
    assert returned["request_id"] == "REQ-100"
    assert returned["run"] == str(run_dir)
    assert returned["registered"][0]["path"].startswith("knowledge/sources/")
    assert (run_dir / "return.json").is_file()
    assert json.loads((run_dir / "return.json").read_text()) == returned


def test_close_refuses_a_directory_that_is_not_a_run(tmp_path):
    with pytest.raises(research_seam.SeamError):
        research_seam.close(tmp_path)
