"""Read-only projection from a run result + generated report into evidence.

Isolation-clean and duck-typed: never imports the generated report type,
reads it only by attribute access (``report.headline``, ``report.results``,
``r.constraint_id``, ``r.status``). See ``design.md#required-invariants``
INV1 and B1.
"""
from __future__ import annotations

from numbers import Real
from typing import Any

from .evidence import (
    CorruptConstraintEvidence,
    EvidenceProvenance,
    ModelEvidence,
    canonical_headline,
)

#: The pipeline channel/field carrying the aggregated constraint report. The
#: single tolerant read of this channel lives here (D1) — both evaluator routes
#: funnel through ``project``; neither reads the channel itself.
REPORT_CHANNEL = "constraint_report"


def _numeric_output(value: Any) -> float | None:
    """Extract a bare or one-level wrapped real number, including Python bool."""
    scalar = getattr(value, "root", value)
    if isinstance(scalar, Real):
        return float(scalar)
    return None


def project(result: Any, *, provenance: EvidenceProvenance, expects_report: bool) -> ModelEvidence:
    """Project a run result into ``ModelEvidence`` — the single report-read seam.

    ``result`` need only expose ``.outputs`` (a mapping of channel/field name to
    value). The constraint report is read tolerantly here (46a):

    - present -> today's projection (headline + per-constraint responses), then
      the report is sealed into an immutable ``model_dump(mode="json")`` tree (D2);
    - absent and ``expects_report`` false -> empty constraint evidence
      (``responses={}``, ``report=None``); a constraint-free package;
    - absent and ``expects_report`` true -> ``CorruptConstraintEvidence`` (M3): a
      constraint-bearing package whose report channel vanished. Loud, never a
      silent empty case.

    ``expects_report`` is the catalog authority, and since CONSTRAINT-SEMANTICS Item 3 it
    is derived in exactly ONE place: ``study.model_contract.ships_constraint_report``, over
    ``usage_records`` — the same population the producer's rule reads. A model that declares
    constraints and executes none of them still ships a report, so ``concrete_entries`` is the
    wrong question and is no longer asked.

    The evaluation layer has no spec-derived default any more. It had one, and its docstring
    said "the two must agree", which is what a second derivation always has to say. It was
    deleted rather than re-synced, and ``expects_constraint_report`` is a required constructor
    argument on both evaluators — this layer is isolation-clean and genuinely has no catalog
    authority to derive one from, so every caller states its expectation instead of inventing it.
    """
    report = result.outputs.get(REPORT_CHANNEL)
    if report is None:
        if expects_report:
            raise CorruptConstraintEvidence(
                f"constraint report channel {REPORT_CHANNEL!r} is absent, but the package "
                "catalog declares constraints — the report was dropped (corruption), not "
                "a constraint-free package"
            )
        responses: dict[str, Any] = {}
        report_tree = None
    else:
        responses = {"headline": canonical_headline(report.headline)}
        for constraint_result in report.results:
            responses[constraint_result.constraint_id] = constraint_result.status
        # Seal at attach: dump once here, freeze in ``ModelEvidence`` (D2). The
        # live generated model is not retained.
        report_tree = report.model_dump(mode="json")

    outputs = {
        key: scalar
        for key, value in result.outputs.items()
        if (scalar := _numeric_output(value)) is not None
    }

    return ModelEvidence(
        responses=responses,
        outputs=outputs,
        provenance=provenance,
        report=report_tree,
    )
