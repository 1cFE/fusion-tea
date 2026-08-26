"""Phase 7 — bounded negatives, and the block on silently re-searching (R-D5, R-D6, SC6)."""

import json

import pytest

import research_seam

REQUEST = {
    "request_id": "REQ-001",
    "question": "What is the winding-pack current density for the Nb3Sn arm?",
    "consumer": "WI-031",
    "gap_type": "unsourced_value",
    "priority": "P1",
    "where_to_look": ["EPFL infoscience", "IEEE TAS"],
    "limits": {"max_searches": 3, "max_captures": 2},
}


@pytest.fixture
def seam(tmp_path):
    root = tmp_path / "requests"
    root.mkdir()
    request_path = root / "REQ-001.json"
    request_path.write_text(json.dumps(REQUEST))
    return research_seam.SeamHome(root=root), request_path


def _negative_for(home, request_path) -> dict:
    key = research_seam.request_key(json.loads(request_path.read_text()))
    return json.loads((home.negatives / f"{key}.json").read_text())


def _dry_run(home, request_path, adequacy="exhausted"):
    opened = research_seam.open_run(request_path, home=home)
    assert opened.exit_code == 0
    research_seam.log_search(opened.run_dir, "nb3sn winding pack current density")
    research_seam.log_candidate(opened.run_dir, "https://example.org/a", "rejected", "paywalled")
    research_seam.log_failure(opened.run_dir, "https://example.org/b", "404")
    return research_seam.close(opened.run_dir, adequacy=adequacy)


def test_adequate_zero_source_run_writes_all_five_negative_fields(seam):
    home, request_path = seam
    returned = _dry_run(home, request_path)

    assert returned["class"] == "BOUNDED_NEGATIVE"
    negative = json.loads(research_seam.Path(returned["negative"]).read_text())
    assert {"request_key", "request_id", "queries", "candidates", "failures",
            "adequacy", "reopened"} <= set(negative)
    assert negative["queries"] == ["nb3sn winding pack current density"]
    assert negative["candidates"] == [
        {"ref": "https://example.org/a", "triage": "rejected", "note": "paywalled"}
    ]
    assert negative["failures"] == [{"ref": "https://example.org/b", "reason": "404"}]
    assert negative["adequacy"] == "exhausted"


def test_the_negative_is_keyed_on_the_request_not_the_clock(seam):
    home, request_path = seam
    _dry_run(home, request_path)
    negative = _negative_for(home, request_path)
    assert negative["request_key"] == research_seam.request_key(REQUEST)
    assert "expires" not in negative and "ttl" not in negative


def test_a_changed_premise_is_a_different_request_key(seam):
    home, request_path = seam
    other = dict(REQUEST, question="A different question entirely")
    assert research_seam.request_key(other) != research_seam.request_key(REQUEST)


def test_where_to_look_order_does_not_change_the_key():
    reordered = dict(REQUEST, where_to_look=list(reversed(REQUEST["where_to_look"])))
    assert research_seam.request_key(reordered) == research_seam.request_key(REQUEST)


def test_second_open_refuses_without_an_override(seam):
    home, request_path = seam
    _dry_run(home, request_path)

    again = research_seam.open_run(request_path, home=home)
    assert again.exit_code != 0
    assert again.run_dir is None
    assert research_seam.request_key(REQUEST) in again.message


def test_override_proceeds_and_is_recorded_on_the_negative(seam):
    home, request_path = seam
    _dry_run(home, request_path)

    again = research_seam.open_run(request_path, home=home,
                                   override_reason="new preprint 2026-08")
    assert again.exit_code == 0 and again.run_dir is not None

    negative = _negative_for(home, request_path)
    assert negative["reopened"][-1]["reason"] == "new preprint 2026-08"
    assert negative["reopened"][-1]["run"]


def test_an_empty_override_reason_is_not_an_override(seam):
    home, request_path = seam
    _dry_run(home, request_path)
    again = research_seam.open_run(request_path, home=home, override_reason="   ")
    assert again.exit_code != 0


def test_a_malformed_request_blocks_before_any_run_directory_exists(seam, tmp_path):
    home, _ = seam
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"request_id": "REQ-002"}))

    opened = research_seam.open_run(bad, home=home)
    assert opened.exit_code != 0 and opened.run_dir is None
    assert "question" in opened.message
    assert not home.runs.exists() or not list(home.runs.iterdir())
