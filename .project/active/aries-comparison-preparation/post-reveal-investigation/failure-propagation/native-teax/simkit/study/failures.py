"""Study-layer exceptions.

Isolation-clean: stdlib only.
"""
from __future__ import annotations


class IncompatibleStore(Exception):
    """Raised when opening a store whose bound compatibility fingerprints differ."""


class StudyLocked(Exception):
    """Raised when acquiring a runner lease that another runner still holds live."""


class StudyLeaseLost(Exception):
    """Raised when a fenced write finds the lease no longer held by this writer (D4/MF-1)."""


class StudyBridgeDefect(Exception):
    """Raised when the bridge produces an ENTRY_VALIDATION failure — a runner defect, never a case."""

    def __init__(self, failure) -> None:
        super().__init__(f"bridge produced an invalid entry model: {failure.cause}")
        self.failure = failure


class RetryableStoreError(Exception):
    """A transient store-I/O fault (staging/commit OSError, SQLite OperationalError)."""
