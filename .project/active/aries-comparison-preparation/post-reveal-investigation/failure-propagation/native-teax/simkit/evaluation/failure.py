"""Normalized evaluator failure taxonomy.

Isolation-clean: imports only stdlib and ``simkit``-internal modules. See
``design.md#required-invariants`` INV1.
"""
from __future__ import annotations

from enum import Enum

from ..config.schema import StrictBaseModel


class EvaluationPhase(str, Enum):
    """The four points at which an evaluation can fail.

    An ``indeterminate`` verdict is never one of these — it is evidence
    (INV5).
    """

    ENTRY_VALIDATION = "entry_validation"
    PREPARATION = "preparation"
    MODULE_EXECUTION = "module_execution"
    OUTPUT_WRITE = "output_write"


class EvaluationFailure(StrictBaseModel):
    """Immutable record of one evaluator failure.

    ``retryable`` defaults to ``False`` and evaluator code never sets it
    otherwise: a deterministic function fails the same way every time, so
    transient/infra retry belongs to the runner, not the evaluator (D4).
    """

    phase: EvaluationPhase
    cause: str
    module_or_channel: str | None = None
    retryable: bool = False
    partial_artifacts: tuple[str, ...] = ()


class EvaluationFailed(Exception):
    """Raised when an evaluation cannot produce evidence."""

    def __init__(self, failure: EvaluationFailure) -> None:
        super().__init__(f"{failure.phase.value}: {failure.cause}")
        self.failure = failure
