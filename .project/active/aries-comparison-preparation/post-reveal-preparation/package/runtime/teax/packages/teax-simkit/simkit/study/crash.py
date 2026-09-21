"""Test-only crash injection at named store seams.

Isolation-clean: stdlib only. Production always uses the no-op default
instance; only test drivers construct one with a `phase:candidate_id` spec.
"""
from __future__ import annotations

import os
import sys


class CrashController:
    """Injects a hard `os._exit` at an exact (phase, candidate_id) seam.

    `phase` is `"mid_staging"` (artifact tmp fsync'd but truncated, final path
    absent) or `"before_commit"` (artifact durable, case row not yet
    committed) — see `store.py`.
    """

    def __init__(self, spec: str | None = None) -> None:
        self.phase: str | None = None
        self.candidate_id: str | None = None
        if spec:
            self.phase, self.candidate_id = spec.split(":", 1)

    def maybe_crash(self, phase: str, candidate_id: str) -> None:
        if phase == self.phase and candidate_id == self.candidate_id:
            sys.stdout.flush()
            sys.stderr.flush()
            # Hard exit: skips Python finally/atexit/buffer flushing, the way
            # a killed process would. Anything durable at this point survived
            # because it was fsync'd before we got here.
            os._exit(137)


NO_CRASH = CrashController(None)
