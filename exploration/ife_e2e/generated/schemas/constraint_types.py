"""Constraint evidence schemas (Item 7 / D5, Appendix B).

A violation is evidence, never an exception (INV-3) — `ConstraintEvaluation` carries the
three-valued verdict and the operands that explain it; `ConstraintReport` aggregates every
assessed constraint's evidence for one design point.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class ConstraintEvaluation(BaseModel):
    """One assertion verdict in one concrete context."""

    constraint_id: str
    actual_value: Optional[bool] = None
    status: Literal["satisfied", "violated", "indeterminate"]
    margin: Optional[float] = None
    observed: dict[str, float]


class ConstraintReport(BaseModel):
    """Assertion evidence and coverage for one design point."""

    catalog_fingerprint: str
    assessed_count: int
    headline: Literal["violation", "indeterminate", "all_satisfied", "not_assessed"]
    results: list[ConstraintEvaluation]
