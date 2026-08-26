#!/usr/bin/env python3
"""The bookkeeper for one research invocation.

It owns the parts that cannot be left to prompt text: validating the bounded
request, refusing to start when a durable negative already answers it, keeping
the run record, and computing the return class from the receipts
`source_registry.py` wrote — not from what the agent says happened.

    uv run python scripts/research_seam.py open knowledge/research/requests/REQ-001.json
    uv run python scripts/research_seam.py log <run-dir> --candidate URL --triage keeper
    uv run python scripts/research_seam.py close <run-dir> --adequacy exhausted

Design: `.project/active/goal-research-seam/design.md` (D8, D9, D13).
"""

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path("knowledge/research/requests")

REQUIRED_REQUEST_FIELDS = (
    "request_id", "question", "consumer", "gap_type", "priority", "where_to_look",
)
RUN_RECORD = "run.jsonl"
RUN_META = "run.json"
PROCESS_LOG = "process_log.md"
RETURN_FILE = "return.json"
RECEIPTS = "receipts"

QUEUEING_OUTCOMES = frozenset({"holdout_hit", "capture_failed", "precondition_failed"})


class SeamError(RuntimeError):
    """The bookkeeper was asked to work on something that is not a run."""


@dataclass(frozen=True)
class SeamHome:
    """Where requests, negatives and runs live. Injectable so tests need no `chdir`."""

    root: Path

    @property
    def negatives(self) -> Path:
        return self.root / "negatives"

    @property
    def runs(self) -> Path:
        return self.root / "runs"


@dataclass(frozen=True)
class OpenResult:
    exit_code: int
    run_dir: Path | None
    message: str


def request_key(request: dict) -> str:
    """A stable hash of what the request is asking, order-insensitive in the list.

    Priority and limits are how hard we look, not what we are looking for, so
    they stay out of the key: raising a limit does not make it a new request (D9).
    """
    identity = {
        "question": request["question"],
        "consumer": request["consumer"],
        "gap_type": request["gap_type"],
        "where_to_look": sorted(request.get("where_to_look") or []),
    }
    canonical = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def open_run(
    request_path: Path,
    *,
    home: SeamHome | None = None,
    override_reason: str | None = None,
) -> OpenResult:
    """Validate the request, honour any recorded negative, and create the run directory.

    This is the only producer of a run directory, and `close` refuses without one.
    That chain is what makes R-D6 bind: an invocation cannot reach a return without
    having passed the negative check first.
    """
    home = home or SeamHome(root=DEFAULT_ROOT)
    try:
        request = json.loads(Path(request_path).read_text())
    except (OSError, json.JSONDecodeError) as error:
        return OpenResult(2, None, f"request is unreadable: {error}")

    missing = [f for f in REQUIRED_REQUEST_FIELDS if not request.get(f)]
    if missing:
        return OpenResult(2, None, f"request is missing required field(s): {', '.join(missing)}")

    key = request_key(request)
    negative_path = home.negatives / f"{key}.json"
    reason = (override_reason or "").strip()
    if negative_path.exists() and not reason:
        return OpenResult(
            3, None,
            f"a bounded negative already answers this request (key {key}): {negative_path}. "
            "Read it. To search again, supply --override-reason.",
        )

    run_dir = home.runs / request["request_id"] / _utc_stamp()
    (run_dir / RECEIPTS).mkdir(parents=True)
    (run_dir / RUN_META).write_text(json.dumps({
        "request_id": request["request_id"],
        "request_key": key,
        "request_path": str(request_path),
        "home_root": str(home.root),
        "limits": request.get("limits", {}),
        "opened_at": _utc_now(),
        "override_reason": reason or None,
    }, indent=2) + "\n")
    (run_dir / RUN_RECORD).touch()
    (run_dir / PROCESS_LOG).write_text(
        f"# Research run {request['request_id']}\n\n"
        f"**Question:** {request['question']}\n\n"
        f"**Consumer:** {request['consumer']}  ·  **Request key:** `{key}`\n\n"
    )

    if reason:
        _record_reopen(negative_path, run_dir, reason)

    return OpenResult(0, run_dir, f"run opened at {run_dir}")


def log_search(run_dir: Path, query: str) -> None:
    """Record a query the agent ran. Counted against `max_searches` at close (D8)."""
    _append(run_dir, {"kind": "search", "query": query}, f"- searched: `{query}`")


def log_candidate(run_dir: Path, ref: str, triage: str, note: str = "") -> None:
    """Record a candidate and what triage decided about it (R-C5)."""
    _append(
        run_dir,
        {"kind": "candidate", "ref": ref, "triage": triage, "note": note},
        f"- candidate {ref} — **{triage}** {note}".rstrip(),
    )


def log_failure(run_dir: Path, ref: str, reason: str) -> None:
    """Record a candidate that could not be brought in, and why."""
    _append(
        run_dir,
        {"kind": "failure", "ref": ref, "reason": reason},
        f"- failed {ref} — {reason}",
    )


def log_fault(run_dir: Path, reason: str) -> None:
    """Record a run-scoped fault: the seam itself could not proceed."""
    _append(run_dir, {"kind": "fault", "reason": reason}, f"- **run fault**: {reason}")


def close(run_dir: Path, *, adequacy: str = "exhausted") -> dict:
    """Compute the seam's return class from the receipts and write `return.json`.

    The agent's log entries describe the search; the receipts describe what
    actually reached the registry. Where they disagree, the receipts win (R-B9).
    """
    run_dir = Path(run_dir)
    meta_path = run_dir / RUN_META
    if not meta_path.is_file():
        raise SeamError(f"{run_dir} is not a run directory — no {RUN_META}")

    meta = json.loads(meta_path.read_text())
    receipts = _read_receipts(run_dir)
    entries = _read_run_record(run_dir)

    registered = _registered_entries(receipts)
    queued = [
        {"candidate": r["candidate"], "reason": r.get("reason") or r.get("outcome")}
        for r in receipts if r["outcome"] in QUEUEING_OUTCOMES
    ]
    faults = [e["reason"] for e in entries if e["kind"] == "fault"]
    limit = _limit_reached(meta, receipts, entries)

    seam_class = _seam_class(
        registered=registered, queued=queued, faults=faults, candidates=receipts
    )

    home = SeamHome(root=Path(meta["home_root"]))
    negative_path = None
    if seam_class == "BOUNDED_NEGATIVE":
        negative_path = _write_negative(
            home, meta, entries, receipts,
            adequacy="limit_reached" if limit else adequacy,
        )

    payload = {
        "request_id": meta["request_id"],
        "run": str(run_dir),
        "class": seam_class,
        "registered": registered,
        "queued": queued,
        "negative": str(negative_path) if negative_path else None,
        "limit_reached": limit,
        "reason": "; ".join(faults) if faults else _default_reason(seam_class),
    }
    (run_dir / RETURN_FILE).write_text(json.dumps(payload, indent=2) + "\n")
    return payload


# --- class computation (design D13's mapping table) --------------------------


def _seam_class(*, registered: list, queued: list, faults: list, candidates: list) -> str:
    """One class per invocation, in the mapping table's precedence.

    A run-scoped fault outranks the queue only when the run never got as far as a
    candidate: with a named candidate on the receipts, something *is* established
    about the search, which is the spec's own boundary between the two.
    """
    if registered:
        return "REGISTERED"
    if queued:
        return "OPERATOR_QUEUE"
    if faults and not candidates:
        return "BLOCKER"
    return "BOUNDED_NEGATIVE"


def _registered_entries(receipts: list[dict]) -> list[dict]:
    """Sources this return can name a citable path for.

    A duplicate whose candidate was triaged a keeper answers the request just as
    well; the only untrue thing would be claiming this run wrote it, which
    `pre_existing` records.
    """
    entries = []
    for receipt in receipts:
        if receipt["outcome"] == "registered":
            pre_existing = False
        elif receipt["outcome"] == "duplicate" and receipt.get("triage") == "keeper":
            pre_existing = True
        else:
            continue
        entries.append({
            "slug": receipt["slug"],
            "path": receipt["path"],
            "source_id": receipt["source_id"],
            "pre_existing": pre_existing,
        })
    return entries


def _limit_reached(meta: dict, receipts: list[dict], entries: list[dict]) -> str | None:
    """Which declared limit stopped the search, if one did (R-A5)."""
    if any(r["outcome"] == "limit_reached" for r in receipts):
        return "max_captures"
    max_searches = meta.get("limits", {}).get("max_searches")
    if max_searches is not None:
        searched = sum(1 for e in entries if e["kind"] == "search")
        if searched >= max_searches:
            return "max_searches"
    return None


def _default_reason(seam_class: str) -> str:
    return {
        "REGISTERED": "at least one source is registered and citable",
        "OPERATOR_QUEUE": "a named candidate is blocked on something a human must resolve",
        "BOUNDED_NEGATIVE": "the search ran and found no usable source",
        "BLOCKER": "the seam could not proceed",
    }[seam_class]


# --- negatives (design D9) ---------------------------------------------------


def _write_negative(
    home: SeamHome, meta: dict, entries: list[dict], receipts: list[dict], *, adequacy: str
) -> Path:
    """Write the durable negative under the request key, preserving any reopen history."""
    home.negatives.mkdir(parents=True, exist_ok=True)
    path = home.negatives / f"{meta['request_key']}.json"
    reopened = json.loads(path.read_text())["reopened"] if path.exists() else []

    candidates = [
        {"ref": e["ref"], "triage": e["triage"], "note": e["note"]}
        for e in entries if e["kind"] == "candidate"
    ]
    failures = [{"ref": e["ref"], "reason": e["reason"]}
                for e in entries if e["kind"] == "failure"]
    failures += [{"ref": r["candidate"], "reason": r.get("reason") or r["outcome"]}
                 for r in receipts if r["outcome"] not in {"registered", "duplicate"}]

    path.write_text(json.dumps({
        "request_key": meta["request_key"],
        "request_id": meta["request_id"],
        "queries": [e["query"] for e in entries if e["kind"] == "search"],
        "candidates": candidates,
        "failures": failures,
        "adequacy": adequacy,
        "reopened": reopened,
        "recorded_at": _utc_now(),
    }, indent=2) + "\n")
    return path


def _record_reopen(negative_path: Path, run_dir: Path, reason: str) -> None:
    """An override never erases the negative; it appends to its history."""
    negative = json.loads(negative_path.read_text())
    negative.setdefault("reopened", []).append(
        {"reason": reason, "run": str(run_dir), "at": _utc_now()}
    )
    negative_path.write_text(json.dumps(negative, indent=2) + "\n")


# --- run record --------------------------------------------------------------


def _append(run_dir: Path, entry: dict, prose: str) -> None:
    run_dir = Path(run_dir)
    if not (run_dir / RUN_META).is_file():
        raise SeamError(f"{run_dir} is not a run directory — no {RUN_META}")
    entry = dict(entry, at=_utc_now())
    with open(run_dir / RUN_RECORD, "a") as handle:
        handle.write(json.dumps(entry) + "\n")
    with open(run_dir / PROCESS_LOG, "a") as handle:
        handle.write(prose + "\n")


def _read_run_record(run_dir: Path) -> list[dict]:
    path = run_dir / RUN_RECORD
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _read_receipts(run_dir: Path) -> list[dict]:
    directory = run_dir / RECEIPTS
    if not directory.is_dir():
        return []
    return [json.loads(p.read_text()) for p in sorted(directory.iterdir())]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")


# --- CLI ---------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    opener = sub.add_parser("open", help="Validate a request and open a run directory")
    opener.add_argument("request", type=Path)
    opener.add_argument("--override-reason",
                        help="Why this request is being searched again despite a "
                             "recorded bounded negative. Recorded on the negative.")

    logger = sub.add_parser("log", help="Record one step of the invocation")
    logger.add_argument("run_dir", type=Path)
    what = logger.add_mutually_exclusive_group(required=True)
    what.add_argument("--search", help="A query that was run")
    what.add_argument("--candidate", help="A candidate reference that was triaged")
    what.add_argument("--failure", help="A candidate reference that could not be brought in")
    what.add_argument("--fault", help="A run-scoped fault: the seam could not proceed")
    logger.add_argument("--triage", choices=["keeper", "rejected"],
                        help="Required with --candidate")
    logger.add_argument("--note", default="", help="Free text for --candidate")
    logger.add_argument("--reason", default="", help="Required with --failure")

    closer = sub.add_parser("close", help="Compute the return class and write return.json")
    closer.add_argument("run_dir", type=Path)
    closer.add_argument("--adequacy", choices=["exhausted", "limit_reached"],
                        default="exhausted",
                        help="Why the search is considered adequate (R-D5)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "open":
        result = open_run(args.request, override_reason=args.override_reason)
        print(result.message)
        if result.run_dir:
            print(result.run_dir)
        return result.exit_code
    if args.command == "log":
        return _run_log(args)
    print(json.dumps(close(args.run_dir, adequacy=args.adequacy), indent=2))
    return 0


def _run_log(args) -> int:
    if args.search:
        log_search(args.run_dir, args.search)
    elif args.candidate:
        if not args.triage:
            print("ERROR: --candidate requires --triage")
            return 2
        log_candidate(args.run_dir, args.candidate, args.triage, args.note)
    elif args.failure:
        if not args.reason:
            print("ERROR: --failure requires --reason")
            return 2
        log_failure(args.run_dir, args.failure, args.reason)
    else:
        log_fault(args.run_dir, args.fault)
    return 0


if __name__ == "__main__":
    sys.exit(main())
