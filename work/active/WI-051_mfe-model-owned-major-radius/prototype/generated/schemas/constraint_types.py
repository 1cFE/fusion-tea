"""Constraint evidence schemas (Item 7 / D5, Appendix B; Item 3 coverage).

A violation is evidence, never an exception (INV-3) — `ConstraintEvaluation` carries the
three-valued verdict and the operands that explain it; `ConstraintReport` aggregates every
assessed constraint's evidence for one design point.

The report carries two orthogonal facts. The **headline** is one precedence-ordered token.
The **coverage account** is the denominator: how many constraint usages the model authored,
how many of those are applicable asserted gates, how many were actually assessed, and why the
rest were not. "Partial" was never a kind of satisfaction — it is a statement about the
denominator, which is why it lives in its own block and survives a higher-precedence headline.

Per-usage detail is not here. The account is a summary addressed to the sealed catalog by the
report's `catalog_fingerprint`; the catalog in `contracts/model_contract.json` is the one
authority for the rows behind these numbers.
"""

from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class ConstraintEvaluation(BaseModel):
    """One assertion verdict in one concrete context."""

    constraint_id: str
    actual_value: Optional[bool] = None
    status: Literal["satisfied", "violated", "indeterminate"]
    margin: Optional[float] = None
    observed: dict[str, float]


class CoverageAccount(BaseModel):
    """How much of the model's authored constraint domain was assessed.

    Computed once at generation from the sealed catalog and baked in, because coverage is a
    property of the model and never of the candidate's input values.

    The two tiers are named apart deliberately. `assessed_gate_count` counts **usages** and
    `ConstraintReport.assessed_entry_count` counts **occurrences**, so one gate over forty
    occurrences reads `assessed_gate_count = 1` beside `assessed_entry_count = 40`. That is
    the two-tier rule working, not a defect to reconcile.
    """

    #: Every authored constraint usage, in every source form. Inventory totality.
    authored_usage_total: int
    #: The feasibility denominator: asserted gates the author did not declare inapplicable.
    applicable_gate_total: int
    #: Of those, the ones that actually ran.
    assessed_gate_count: int
    #: Of those, the ones that did not.
    unassessed_gate_count: int
    #: Asserted gates removed from the denominator by an explicit inapplicability marker.
    inapplicable_gate_count: int
    #: reason token -> count, over the unassessed gates only. A key appears iff a gate landed
    #: on it, so there are no zero-filled keys and no list to drift.
    unassessed_reasons: dict[str, int]
    coverage_state: Literal["complete", "partial", "none"]

    @model_validator(mode="after")
    def _identities_hold(self) -> "CoverageAccount":
        """An internally inconsistent account cannot construct.

        The producer asserts the same identities before rendering. Checking them again here
        is what catches a bake corrupted between the derivation and this constructor.
        """
        if self.assessed_gate_count + self.unassessed_gate_count != self.applicable_gate_total:
            raise ValueError(
                f"assessed {self.assessed_gate_count} + unassessed "
                f"{self.unassessed_gate_count} != applicable {self.applicable_gate_total}"
            )
        if sum(self.unassessed_reasons.values()) != self.unassessed_gate_count:
            raise ValueError(
                f"unassessed_reasons sums to {sum(self.unassessed_reasons.values())}, "
                f"not {self.unassessed_gate_count}"
            )
        if self.applicable_gate_total == 0:
            expected = "none"
        elif self.unassessed_gate_count == 0:
            expected = "complete"
        else:
            expected = "partial"
        if self.coverage_state != expected:
            raise ValueError(
                f"coverage_state {self.coverage_state!r} disagrees with the counts, "
                f"which imply {expected!r}"
            )
        return self


class ConstraintReport(BaseModel):
    """Assertion evidence and coverage for one design point."""

    catalog_fingerprint: str
    #: Occurrence tier: how many concrete evaluations arrived. Named `assessed_count` before
    #: the coverage account existed, when there was only one tier to mean.
    assessed_entry_count: int
    headline: Literal[
        "violation",
        "indeterminate",
        "full_satisfaction",
        "partial_coverage",
        "not_assessed",
    ]
    coverage: CoverageAccount
    results: list[ConstraintEvaluation]
