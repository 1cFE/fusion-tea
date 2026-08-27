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


def _ids_in_record(text, prefix):
    """The `<study-id>#<n>` ids a record's findings table carries.

    § 15 rows plus any addendum rows after § 17: an addendum may add findings.
    """
    return {
        cell.strip("` ")
        for line in text.splitlines()
        if line.startswith("| `")
        for cell in [line.split("|")[1]]
        if cell.strip("` ").startswith(f"{prefix}#")
    }


def _ids_in_log(text, prefix):
    """The `<study-id>#<n>` ids the discovery log's `Record` column carries.

    Join on the Record column only: a row's Finding cell may legitimately cite
    another record's id (a recurring finding), and that is not a row for it.
    `Record` is column index 3, and the schema table's six columns keep their
    order (design I9).

    This returns a **set**, and that is load-bearing: a finding may carry a
    sighting row and one or more joined disposition rows appended later under the
    same id (ADR-004). Collecting into a list would make that multiplicity a
    failure instead of the contract.
    """
    return {
        cell
        for line in text.splitlines()
        if line.startswith("| 20")
        for cell in [line.split("|")[3].strip().strip("`")]
        if cell.startswith(f"{prefix}#")
    }


@pytest.mark.parametrize("record", RECORDS, ids=lambda p: p.name)
def test_findings_join_the_discovery_log(record):
    """Runbook step 14: every § 15 finding has a log row, and every row for this
    record names a finding § 15 carries.

    The comparison is between sets, and that is what guarantees the joined-row
    shape: a second row under an existing id is a disposition update and joins
    cleanly, while a row citing an id the record does not carry fails. That is the
    intent, not an accident of the implementation —
    `test_a_joined_disposition_row_is_legal` below goes red if it is undone.
    """
    in_record = _ids_in_record((record / "record.md").read_text(), record.name)
    in_log = _ids_in_log((STUDIES / "DISCOVERY_LOG.md").read_text(), record.name)
    assert in_record, "a committed record carries at least one finding"
    assert in_record == in_log


def test_a_joined_disposition_row_is_legal():
    """ADR-004 and design I8: a second row under an existing id is a disposition
    update, not a duplicate, and a row's kind is positional — the sighting comes
    first in file order and the disposition follows it.

    This guards the obligation that a goal round can disposition a touched finding
    at all. Rewriting `_ids_in_log` from a set comprehension to a list — the exact
    edit that kills append-as-update — turns this red.
    """
    record = "| `20260823-x#1` | model | a finding | open | `unrouted` |\n"
    log = (
        "| 2026-08-23 | `model` | `20260823-x#1` | a finding | open | `unrouted` |\n"
        "| 2026-08-25 | `model` | `20260823-x#1` | a finding | model fix | "
        "`work/active/WI-040` |\n"
    )
    assert _ids_in_record(record, "20260823-x") == _ids_in_log(log, "20260823-x")
