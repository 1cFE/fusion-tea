"""Crash-safe SQLite study store: content-addressed staging, fenced lease, GC.

Isolation-clean: stdlib only (`sqlite3`, `hashlib`, `json`, `os`, `socket`,
`threading`, `time`, `uuid`).

**Store contract (NF-3, design.md#implementation-notes):** `journal_mode=WAL`
and `synchronous=FULL` are required behavior, asserted on every open — the
crash-safety proof binds to exactly these settings. The store is
**single-host**: the lease/GC reasoning and SQLite+WAL durability assume a
local filesystem. A network filesystem is out of contract.

**Durability boundary:** the protocol survives a killed *process*
(`fsync`-before-return). It does not claim power-loss or disk-cache-loss
safety.

Staging layout: `root/staging/{lease_id}/{attempt_id}.tmp` -> fsync -> atomic
rename -> `root/artifacts/{digest}.json` -> fsync dir (INV-B, INV-C). The
per-lease subdir attributes a crashed orphan tmp to its (dead) lease,
distinguishing it from a live runner's in-flight tmp.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Mapping

from .compatibility import Compatibility
from .crash import NO_CRASH, CrashController
from .failures import IncompatibleStore, RetryableStoreError, StudyLeaseLost, StudyLocked
from .identity import canonical_bytes

_SCHEMA = """
CREATE TABLE compatibility (
  singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
  study_id TEXT NOT NULL,
  executable_fingerprint TEXT NOT NULL, model_contract_fingerprint TEXT NOT NULL,
  study_definition_fingerprint TEXT NOT NULL, input_schema_version TEXT NOT NULL,
  evidence_schema_version TEXT NOT NULL, strategy_identity TEXT NOT NULL,
  strategy_config TEXT NOT NULL
);

CREATE TABLE proposals (
  proposal_id TEXT PRIMARY KEY, raw_json TEXT NOT NULL,
  valid INTEGER NOT NULL, reject_reason TEXT, candidate_id TEXT
);

CREATE TABLE attempt_transitions (
  transition_seq INTEGER PRIMARY KEY AUTOINCREMENT,
  attempt_id TEXT NOT NULL, candidate_id TEXT NOT NULL, proposal_id TEXT NOT NULL,
  attempt_number INTEGER NOT NULL,
  state TEXT NOT NULL
);
CREATE INDEX ix_attempt_by_candidate ON attempt_transitions(candidate_id, attempt_number);

CREATE TABLE cases (
  commit_order INTEGER PRIMARY KEY AUTOINCREMENT,
  study_id TEXT NOT NULL, candidate_id TEXT NOT NULL, proposal_id TEXT NOT NULL,
  attempt_id TEXT NOT NULL, state TEXT NOT NULL,
  inputs_json TEXT NOT NULL,
  evidence_digest TEXT,
  failure_json TEXT,
  assessment_json TEXT,
  UNIQUE (study_id, candidate_id)
);

CREATE TABLE runner_lease (
  singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
  lease_id TEXT NOT NULL, pid INTEGER NOT NULL, hostname TEXT NOT NULL,
  acquired_at REAL NOT NULL, heartbeat_at REAL NOT NULL, released INTEGER NOT NULL DEFAULT 0
);
"""


def _dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _fsync_dir(path: Path) -> None:
    fd = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class StudyStore:
    """SQLite study store. One instance is one open handle; at most one
    instance at a time may hold the live runner lease (INV-F)."""

    LEASE_TTL_SECONDS = 30.0
    HEARTBEAT_INTERVAL_SECONDS = 10.0

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.root = self.db_path.parent
        self.artifacts_dir = self.root / "artifacts"
        self.staging_dir = self.root / "staging"
        self.conn = sqlite3.connect(str(self.db_path), timeout=30.0, isolation_level=None)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.row_factory = sqlite3.Row
        self._assert_pragma_contract()
        self._study_id: str | None = None
        self.lease_id: str | None = None
        self._heartbeat_stop: threading.Event | None = None
        self._heartbeat_thread: threading.Thread | None = None

    def _assert_pragma_contract(self) -> None:
        journal_mode = self.conn.execute("PRAGMA journal_mode").fetchone()[0]
        synchronous = self.conn.execute("PRAGMA synchronous").fetchone()[0]
        if str(journal_mode).lower() != "wal" or int(synchronous) != 2:  # FULL == 2
            raise RuntimeError(
                f"store contract violated: journal_mode={journal_mode!r} synchronous={synchronous!r}"
            )

    # -- lifecycle -------------------------------------------------------

    @classmethod
    def create_or_open(cls, db_path: Path, compat: Compatibility) -> "StudyStore":
        exists = Path(db_path).exists()
        store = cls(db_path)
        if not exists:
            store._init_schema()
            store._bind_compatibility(compat)
        else:
            store._check_compatibility(compat)
        store._study_id = compat.study_id
        store.artifacts_dir.mkdir(parents=True, exist_ok=True)
        store.staging_dir.mkdir(parents=True, exist_ok=True)
        return store

    def _init_schema(self) -> None:
        self.conn.executescript(_SCHEMA)

    def _bind_compatibility(self, compat: Compatibility) -> None:
        self.conn.execute(
            "INSERT INTO compatibility VALUES (?,?,?,?,?,?,?,?,?)", compat.as_row()
        )

    def _check_compatibility(self, compat: Compatibility) -> None:
        row = self.conn.execute("SELECT * FROM compatibility").fetchone()
        bound = Compatibility.from_row(row)
        if bound != compat:
            raise IncompatibleStore(f"store bound to {bound} but opened with {compat}")

    @property
    def study_id(self) -> str:
        assert self._study_id is not None, "store not opened via create_or_open"
        return self._study_id

    def close(self) -> None:
        self._stop_heartbeat()
        self.conn.close()

    # -- runner lease (D4, MF-1, INV-F) -----------------------------------

    def _lease_is_dead(self, row: sqlite3.Row, now: float) -> bool:
        """Hard pid-death fast path (same host only), else soft TTL expiry."""
        if row["hostname"] == socket.gethostname():
            try:
                os.kill(row["pid"], 0)
            except ProcessLookupError:
                return True
            except PermissionError:
                pass  # pid exists, owned by someone else -> not dead via this path
        return (now - row["heartbeat_at"]) > self.LEASE_TTL_SECONDS

    def acquire_lease(self) -> str:
        """Acquire or reclaim the singleton runner lease.

        Refuses (`StudyLocked`) a live lease; reclaims a released/dead one by
        minting a fresh `lease_id`.
        """
        now = time.time()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT * FROM runner_lease WHERE singleton = 1"
            ).fetchone()
            if row is not None and not row["released"] and not self._lease_is_dead(row, now):
                raise StudyLocked(
                    f"study lease held by pid={row['pid']} host={row['hostname']!r}"
                )
            new_lease_id = uuid.uuid4().hex
            if row is None:
                self.conn.execute(
                    "INSERT INTO runner_lease VALUES (1,?,?,?,?,?,0)",
                    (new_lease_id, os.getpid(), socket.gethostname(), now, now),
                )
            else:
                self.conn.execute(
                    "UPDATE runner_lease SET lease_id=?, pid=?, hostname=?, "
                    "acquired_at=?, heartbeat_at=?, released=0 WHERE singleton = 1",
                    (new_lease_id, os.getpid(), socket.gethostname(), now, now),
                )
        except Exception:
            self.conn.rollback()
            raise
        self.conn.commit()
        self.lease_id = new_lease_id
        (self.staging_dir / self.lease_id).mkdir(parents=True, exist_ok=True)
        self._start_heartbeat(new_lease_id)
        return self.lease_id

    def release_lease(self) -> None:
        if self.lease_id is None:
            return
        self._stop_heartbeat()
        self.conn.execute(
            "UPDATE runner_lease SET released = 1 WHERE singleton = 1 AND lease_id = ?",
            (self.lease_id,),
        )
        self.lease_id = None

    def _start_heartbeat(self, lease_id: str) -> None:
        self._stop_heartbeat()
        stop = threading.Event()
        self._heartbeat_stop = stop
        thread = threading.Thread(
            target=self._heartbeat_loop, args=(lease_id, stop), daemon=True
        )
        self._heartbeat_thread = thread
        thread.start()

    def _heartbeat_loop(self, lease_id: str, stop: threading.Event) -> None:
        # Own connection: sqlite3 connections are not safe to share across
        # threads without external serialization.
        conn = sqlite3.connect(str(self.db_path), timeout=30.0, isolation_level=None)
        try:
            while not stop.wait(self.HEARTBEAT_INTERVAL_SECONDS):
                conn.execute(
                    "UPDATE runner_lease SET heartbeat_at = ? WHERE singleton = 1 AND lease_id = ?",
                    (time.time(), lease_id),
                )
        finally:
            conn.close()

    def _stop_heartbeat(self) -> None:
        if self._heartbeat_stop is not None:
            self._heartbeat_stop.set()
        if self._heartbeat_thread is not None:
            self._heartbeat_thread.join(timeout=5.0)
        self._heartbeat_stop = None
        self._heartbeat_thread = None

    # -- fenced writes (MF-1) ---------------------------------------------

    def _fenced_execute(self, sql: str, params: tuple) -> None:
        """Run one write inside a transaction fenced on the held lease_id.

        A `sqlite3.OperationalError` (e.g. a lock-contention timeout) is a
        transient store-I/O fault, not a lease loss or a caller bug — wrapped
        as `RetryableStoreError` so the runner retries under a new attempt
        (D7).
        """
        if self.lease_id is None:
            raise StudyLeaseLost("no lease held")
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT lease_id FROM runner_lease WHERE singleton = 1"
            ).fetchone()
            if row is None or row["lease_id"] != self.lease_id:
                raise StudyLeaseLost(f"lease {self.lease_id} no longer held")
            self.conn.execute(sql, params)
        except sqlite3.OperationalError as error:
            self.conn.rollback()
            raise RetryableStoreError(str(error)) from error
        except Exception:
            self.conn.rollback()
            raise
        self.conn.commit()

    # -- proposals (append-only, idempotent re-persist; L3-3) --------------

    def record_proposal(
        self,
        proposal_id: str,
        raw: Mapping[str, Any],
        *,
        valid: bool,
        candidate_id: str | None,
        reason: str | None,
    ) -> None:
        self._fenced_execute(
            "INSERT OR IGNORE INTO proposals VALUES (?,?,?,?,?)",
            (proposal_id, _dumps(raw), int(valid), reason, candidate_id),
        )

    # -- attempt transitions (append-only-per-transition, D2) ---------------

    def next_attempt_number(self, candidate_id: str) -> int:
        row = self.conn.execute(
            "SELECT COALESCE(MAX(attempt_number), 0) + 1 AS n "
            "FROM attempt_transitions WHERE candidate_id = ?",
            (candidate_id,),
        ).fetchone()
        return row["n"]

    def record_transition(
        self,
        *,
        attempt_id: str,
        candidate_id: str,
        proposal_id: str,
        attempt_number: int,
        state: str,
    ) -> None:
        self._fenced_execute(
            "INSERT INTO attempt_transitions "
            "(attempt_id, candidate_id, proposal_id, attempt_number, state) "
            "VALUES (?,?,?,?,?)",
            (attempt_id, candidate_id, proposal_id, attempt_number, state),
        )

    # -- cases (append-only; INV-A, INV-C) ----------------------------------

    def has_case(self, candidate_id: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM cases WHERE study_id = ? AND candidate_id = ?",
            (self.study_id, candidate_id),
        ).fetchone()
        return row is not None

    def _stage_artifact(
        self,
        attempt_id: str,
        evidence_json: Mapping[str, Any],
        crash: CrashController,
        candidate_id: str,
    ) -> str:
        """Content-addressed staging: tmp -> fsync -> atomic rename -> fsync dir.

        A reader never sees a half-written file at the final path (INV-B):
        the final path only ever appears via an atomic rename of a fully
        fsync'd tmp. One function produces both the on-disk bytes and the
        digest, so they cannot drift (INV-H).
        """
        payload = canonical_bytes(evidence_json)
        digest = hashlib.sha256(payload).hexdigest()
        final_path = self.artifacts_dir / f"{digest}.json"
        if final_path.exists():
            return digest  # already durably staged (resume / replicate dedup)

        if self.lease_id is None:
            raise StudyLeaseLost("no lease held")
        lease_dir = self.staging_dir / self.lease_id
        tmp = lease_dir / f"{attempt_id}.tmp"
        try:
            lease_dir.mkdir(parents=True, exist_ok=True)
            with open(tmp, "wb") as handle:
                half = len(payload) // 2
                handle.write(payload[:half])
                handle.flush()
                os.fsync(handle.fileno())
                crash.maybe_crash("mid_staging", candidate_id)  # tmp truncated, final absent
                handle.write(payload[half:])
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, final_path)  # atomic
            _fsync_dir(self.artifacts_dir)
        except OSError as error:
            # Transient store-I/O fault, not a lease/logic error (D7).
            raise RetryableStoreError(str(error)) from error
        return digest

    def commit_case(
        self,
        *,
        candidate_id: str,
        proposal_id: str,
        attempt_id: str,
        state: str,
        inputs: Mapping[str, Any],
        evidence_json: Mapping[str, Any] | None,
        failure_json: Mapping[str, Any] | None = None,
        assessment_json: Mapping[str, Any] | None = None,
        crash: CrashController = NO_CRASH,
    ) -> str | None:
        """Stage the artifact durably (if any), then atomically commit the case row.

        `evidence_json=None` is the D5 shape for `execution_failed`: no
        evidence was produced, so `evidence_digest` stays NULL and
        `failure_json` carries the failure instead.
        """
        digest = None
        if evidence_json is not None:
            digest = self._stage_artifact(attempt_id, evidence_json, crash, candidate_id)
        crash.maybe_crash("before_commit", candidate_id)  # artifact durable, case not yet committed
        self._fenced_execute(
            "INSERT INTO cases "
            "(study_id, candidate_id, proposal_id, attempt_id, state, inputs_json, "
            " evidence_digest, failure_json, assessment_json) VALUES (?,?,?,?,?,?,?,?,?)",
            (
                self.study_id,
                candidate_id,
                proposal_id,
                attempt_id,
                state,
                _dumps(inputs),
                digest,
                _dumps(failure_json) if failure_json is not None else None,
                _dumps(assessment_json) if assessment_json is not None else None,
            ),
        )
        return digest

    def ordered_cases(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM cases ORDER BY commit_order").fetchall()
        return [dict(row) for row in rows]

    def referenced_digests(self) -> set[str]:
        return {
            row["evidence_digest"]
            for row in self.conn.execute(
                "SELECT evidence_digest FROM cases WHERE evidence_digest IS NOT NULL"
            )
        }

    # -- GC (L2-1, L3-5) -----------------------------------------------------

    def gc(self) -> dict:
        """Collect orphaned staging tmps and unreferenced artifacts.

        Refuses while any lease is live: a live runner's in-flight
        `staging/{lease}/*.tmp` are untouchable. Safe to run once the lease
        is released or dead (reclaim already proved it dead).
        """
        now = time.time()
        row = self.conn.execute("SELECT * FROM runner_lease WHERE singleton = 1").fetchone()
        if row is not None and not row["released"] and not self._lease_is_dead(row, now):
            raise StudyLocked("GC refused: a runner lease is live")

        referenced = self.referenced_digests()
        tmps_collected = 0
        for lease_dir in sorted(p for p in self.staging_dir.glob("*") if p.is_dir()):
            for tmp in lease_dir.glob("*.tmp"):
                tmp.unlink()
                tmps_collected += 1

        artifacts_collected = 0
        for artifact in sorted(self.artifacts_dir.glob("*.json")):
            if artifact.stem not in referenced:
                artifact.unlink()
                artifacts_collected += 1

        return {"tmps_collected": tmps_collected, "artifacts_collected": artifacts_collected}
