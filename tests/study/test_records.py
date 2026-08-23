"""Every committed study record is closed.

Generic over every record directory under ``exploration/stellarator_e2e/studies/``
(RUN-STUDY Item 6 plan, Phase 2 stencil). A record is closed when its snapshot
resolves (every arm names a store that exists in ``stores[]``), its ``record.md``
carries no unreplaced ``<...>`` placeholder (runbook step 15), and the arms the
exported points carry are exactly the arms the snapshot declares. Vacuous when no
record has been committed yet.
"""

import csv
import json
from pathlib import Path

import pytest

STUDIES = Path(__file__).resolve().parents[2] / "exploration" / "stellarator_e2e" / "studies"
RECORDS = sorted(p for p in STUDIES.glob("2*-*") if p.is_dir())


@pytest.mark.parametrize("record", RECORDS, ids=lambda p: p.name)
def test_record_is_closed(record):
    snap = json.loads((record / "snapshot.json").read_text())
    stores = {s["store_id"] for s in snap["stores"]}
    assert all(a["store_id"] in stores for a in snap["arms"])
    assert "<" not in (record / "record.md").read_text()  # no placeholders
    with (record / "results" / "points.csv").open(newline="") as fh:
        csv_arms = {row["arm_id"] for row in csv.DictReader(fh)}
    assert csv_arms == {a["arm_id"] for a in snap["arms"]}


@pytest.mark.parametrize("record", RECORDS, ids=lambda p: p.name)
def test_arms_share_one_store_when_fingerprints_agree(record):
    snap = json.loads((record / "snapshot.json").read_text())
    fps = {a["effective_executable_fingerprint"]["value"] for a in snap["arms"]}
    if len(fps) == 1:
        assert len(snap["stores"]) == 1


@pytest.mark.parametrize("record", RECORDS, ids=lambda p: p.name)
def test_findings_join_the_discovery_log(record):
    """Runbook step 14: every § 15 finding has a log row, and every row for this
    record names a finding § 15 carries."""
    # § 15 rows plus any addendum rows after § 17: an addendum may add findings.
    text = (record / "record.md").read_text()
    in_record = {
        cell.strip("` ")
        for line in text.splitlines()
        if line.startswith("| `")
        for cell in [line.split("|")[1]]
        if cell.strip("` ").startswith(f"{record.name}#")
    }
    log = (STUDIES / "DISCOVERY_LOG.md").read_text()
    # Join on the Record column only: a row's Finding cell may legitimately cite
    # another record's id (a recurring finding), and that is not a row for it.
    in_log = {
        cell
        for line in log.splitlines()
        if line.startswith("| 20")
        for cell in [line.split("|")[3].strip().strip("`")]
        if cell.startswith(f"{record.name}#")
    }
    assert in_record, "a committed record carries at least one finding"
    assert in_record == in_log
