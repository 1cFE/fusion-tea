"""Runtime-owned evidence envelope.

Isolation-clean: imports only stdlib and ``simkit``-internal modules, and
never imports a generated model class. See ``design.md#required-invariants``
INV1.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Literal, Mapping

from pydantic import ConfigDict, field_validator

from ..config.schema import StrictBaseModel


def _freeze(value: Any) -> Any:
    """Recursively convert to a read-only structure: ``Mapping`` ->
    ``MappingProxyType``, ``list``/``tuple`` -> ``tuple``. The result has no
    mutable container reachable, so a downstream holder cannot change nested
    status/margin/observations (INV-C, contract 41). The three encode/decode
    walkers accept ``Mapping``/``(list, tuple)`` so the frozen tree still
    encodes byte-identically (INV-G)."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(val) for key, val in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(val) for val in value)
    return value


class CorruptConstraintEvidence(RuntimeError):
    """A constraint-bearing package (its catalog declares constraints) produced
    no constraint report — a vanished channel, not a constraint-free package
    (invariant 46a / design M3). Raised loudly, and deliberately *not* an
    ``EvaluationFailed``, so the run stops instead of recording a healthy-looking
    empty case."""

class UnknownHeadlineToken(RuntimeError):
    """A report or canonical headline token this runtime cannot map.

    Deliberately **not** an ``AssessmentFailed``: a token the runtime cannot map means the
    runtime does not understand the package, which must stop the run — not record a per-case
    policy failure that looks healthy in the store. It is also not a
    ``CorruptConstraintEvidence``: the evidence is intact, the vocabulary is not shared.

    This is the fail-closed half of CONSTRAINT-SEMANTICS Item 3's rename. The generated
    ``all_satisfied`` became ``full_satisfaction`` because state 3's meaning strengthened from
    "nothing failed" to "everything was checked and passed". A reader that silently defaulted
    on the unknown token would hide the strengthened claim; one that raises exposes it.
    """


# Runtime-owned verdict vocabulary, split so one type stops doing two jobs.
#
# A per-constraint status is a verdict about one assertion in one context. A headline is a
# statement about the whole design point, and it has states no single constraint can have —
# "partial" is not a kind of satisfaction, it is a statement about the denominator.
ConstraintStatus = Literal["satisfied", "violated", "indeterminate"]
HeadlineResponse = Literal[
    "satisfied", "violated", "indeterminate", "partial_coverage", "not_assessed"
]
ResponseEntry = ConstraintStatus | HeadlineResponse

# Read-only projection from the generated report's headline vocabulary (underscore) onto the
# runtime-owned canonical vocabulary (D6). One report token per canonical token, both ways.
CANONICAL_HEADLINE: Mapping[str, HeadlineResponse] = MappingProxyType(
    {
        "violation": "violated",
        "indeterminate": "indeterminate",
        "full_satisfaction": "satisfied",
        "partial_coverage": "partial_coverage",
        "not_assessed": "not_assessed",
    }
)


def canonical_headline(token: str) -> HeadlineResponse:
    """Map a generated report headline onto the canonical vocabulary, or refuse by name.

    The bare subscript this replaces raised ``KeyError`` on an unmapped token, which
    invariant 46a forbids: an unrecognized token must never be swallowed into something that
    reads satisfied or unconstrained.
    """
    try:
        return CANONICAL_HEADLINE[token]
    except KeyError:
        raise UnknownHeadlineToken(
            f"generated report headline {token!r} is not one of "
            f"{sorted(CANONICAL_HEADLINE)}: this runtime does not understand the package it "
            "is reading. If the package is older than this runtime, regenerate it; if it is "
            "newer, update the runtime."
        ) from None


class EvidenceProvenance(StrictBaseModel):
    """Identity fields the evaluator is entitled to stamp.

    Deliberately excludes study/candidate/proposal identity and wall-clock
    timestamps — those are runner-owned (Item 11) and stamping them here
    would break determinism (B2). See
    ``design.md#deferred-item-decisions``.
    """

    executable_fingerprint: str
    evidence_schema_version: str
    evaluator_version: str
    input_digest: str


class ModelEvidence(StrictBaseModel):
    """Immutable evidence produced by one evaluation.

    ``responses`` is keyed by constraint ID plus the reserved key
    ``"headline"`` for the aggregate verdict — empty (``{}``) for a
    constraint-free package. ``outputs`` holds ExitPoint-selected ``numbers.Real`` values,
    bare or unwrapped once from numeric ``.root`` wrappers, converted to float under
    their existing exit keys. Python bool becomes 0.0/1.0; non-real values are excluded. Nonfinite
    floats are retained. ``report`` is the generated report's
    ``model_dump(mode="json")`` tree, deep-frozen at attach (D2) — never the
    live generated model — or ``None`` when there is no constraint report. All
    three are sealed read-only so nested status/margin cannot be mutated
    (contract 41).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", arbitrary_types_allowed=True)

    responses: Mapping[str, ResponseEntry]
    outputs: Mapping[str, float]
    provenance: EvidenceProvenance
    #: The generated report's ``model_dump(mode="json")`` tree, deep-frozen at
    #: the projection seam (D2) — or ``None`` for a constraint-free package
    #: (empty evidence, 46a). Never the live generated model.
    report: Mapping[str, Any] | None

    @field_validator("responses", "outputs", "report", mode="after")
    @classmethod
    def _seal(cls, value: Any) -> Any:
        """Deep-freeze the mappings and the report tree so no nested container
        reachable from the envelope is mutable (INV-C, contract 41)."""
        return _freeze(value)
