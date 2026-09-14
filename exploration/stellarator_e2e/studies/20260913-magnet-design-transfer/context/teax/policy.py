"""Assessment/policy seam: a `Policy` protocol and a minimal `DispositionPolicy`.

Just enough to produce the three case states and exercise
`assessment_failed`. The full study-policy interpretation protocol, result
queries, and CLI are Item 12 (spec.md#assessment-policy-boundary);
`ModelEvidence` is never mutated.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Literal, Mapping, Protocol

from simkit.evaluation.evidence import ModelEvidence, UnknownHeadlineToken

ObjectiveRole = Literal["minimize", "maximize", "penalty"]


@dataclass(frozen=True)
class ObjectiveSpec:
    """One configured objective: which output to read and how to weigh it.

    `penalty_threshold` bounds the "satisfied but beyond threshold ->
    penalize" disposition (`ObjectivePolicy`, design.md#the-policy).
    """

    output: str
    role: ObjectiveRole
    penalty_threshold: float | None = None


_DISPOSITION_BY_HEADLINE = {
    "satisfied": "feasible",
    "violated": "infeasible",
    "indeterminate": "indeterminate",
    # A candidate whose gates were only partly assessed is not feasible and not infeasible.
    # It gets its own disposition rather than being folded into either, because folding it
    # into "feasible" is precisely the claim CONSTRAINT-SEMANTICS Item 3 exists to stop.
    # These values surface as ``CaseView.disposition`` out of ``assessment_json``; the
    # ``cases.state`` lifecycle column is untouched and needs no migration.
    "partial_coverage": "partial_coverage",
    "not_assessed": "not_assessed",
}


def _disposition_for(headline: str, table: Mapping[str, str], table_name: str) -> str:
    """Look a headline up in a dispatch table, or refuse by name.

    The bare subscripts these replace raised ``KeyError``. A study that met a headline its
    policy had never been taught would crash with a bare token and no instruction; worse, a
    table that silently defaulted would give a partially-covered candidate a disposition
    nobody chose. Both tables fail closed, and the message says what has to be decided.
    """
    try:
        return table[headline]
    except KeyError:
        raise UnknownHeadlineToken(
            f"{table_name} has no disposition for headline {headline!r} (known: "
            f"{sorted(table)}): this study's policy has not been taught what to do with a "
            "candidate in that state."
        ) from None


def _coverage_of(evidence: ModelEvidence) -> dict[str, Any]:
    """The report's coverage account and catalog fingerprint, for the assessment record.

    A **copy** into `assessment_json`, never a write to evidence (invariant 49). The account
    already reaches the durable record for free inside the evidence artifact, because that
    artifact is the report tree whole; carrying it here as well is what lets a study query
    answer "how covered was this candidate" off the case row without opening artifacts.

    Empty for a constraint-free package, which has no report at all.
    """
    report = evidence.report
    if report is None:
        return {}
    return {
        "coverage": _thawed(report.get("coverage")),
        "catalog_fingerprint": report.get("catalog_fingerprint"),
    }


def _thawed(value: Any) -> Any:
    """Plain, JSON-serializable containers from evidence's frozen ones.

    ``ModelEvidence`` deep-freezes the report tree at attach (invariant 41), so `coverage`
    arrives as a ``MappingProxyType`` of ``MappingProxyType``. `assessment_json` is
    ``json.dumps``-ed into the case row, and ``json`` refuses a mappingproxy. Thawing on the
    way *out* is the right direction: the evidence copy stays frozen and unshared, and the
    assessment gets its own plain structure to serialize.
    """
    if isinstance(value, Mapping):
        return {key: _thawed(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_thawed(item) for item in value]
    return value


class AssessmentFailed(Exception):
    """Policy/objective extraction failed; the runner preserves real evidence
    for this case (spec.md#runner)."""


class Policy(Protocol):
    def assess(self, evidence: ModelEvidence, *, candidate_id: str) -> dict[str, Any]: ...


class DispositionPolicy:
    """Maps evidence to a disposition using the real canonical headline
    vocabulary (`satisfied|violated|indeterminate|partial_coverage|not_assessed`).

    `partial_coverage` joined at CONSTRAINT-SEMANTICS Item 3 and gets its own disposition
    rather than folding into `feasible` or `infeasible`: a candidate whose gates were only
    partly assessed is neither.

    `reject_candidate_ids` is an injected set this policy raises
    `AssessmentFailed` for — the seam Item 11 needs to exercise
    `assessment_failed` against real evidence, since the deterministic
    fixture cannot itself fail assessment (design.md#validation-approach).
    """

    def __init__(self, reject_candidate_ids: frozenset[str] = frozenset()) -> None:
        self.reject_candidate_ids = reject_candidate_ids

    def assess(self, evidence: ModelEvidence, *, candidate_id: str) -> dict[str, Any]:
        if candidate_id in self.reject_candidate_ids:
            raise AssessmentFailed(f"policy rejected {candidate_id}")
        if "headline" not in evidence.responses:
            # Constraint-free package: empty evidence, no headline (46a). Distinct
            # from `not_assessed` (a present report with zero eligible entries).
            return {"disposition": "unconstrained", "headline": None}
        headline = evidence.responses["headline"]
        disposition = _disposition_for(
            headline, _DISPOSITION_BY_HEADLINE, "_DISPOSITION_BY_HEADLINE"
        )
        return {
            "disposition": disposition,
            "headline": headline,
            **_coverage_of(evidence),
        }


# Headline -> disposition, the extraction-independent half of the mapping
# (design.md#the-policy step 3). "satisfied" is resolved by `ObjectivePolicy`
# itself, since it also depends on the configured penalty threshold.
_HEADLINE_DISPOSITION: Mapping[str, str] = {
    "violated": "reject",
    "indeterminate": "keep-for-boundary",
    # The conservative default. A partially-covered candidate is kept as boundary evidence
    # but does NOT steer the search, because "every gate that ran passed" is not the same
    # claim as "this candidate is feasible", and a design search that conflates them is
    # steering on gates nobody checked. A study that wants it in the steering loop says so in
    # writing — see `PolicyConfig.partial_coverage`, which is digested into
    # `study_definition_fingerprint` and therefore starts a new lineage.
    "partial_coverage": "keep-for-boundary",
    "not_assessed": "keep-for-boundary",
}


def _beyond_penalty_threshold(objective: ObjectiveSpec, value: float) -> bool:
    if objective.penalty_threshold is None or not math.isfinite(value):
        return False
    if objective.role == "maximize":
        return value < objective.penalty_threshold
    return value > objective.penalty_threshold  # minimize | penalty


class ObjectivePolicy:
    """The real study-policy interpretation: extracts configured objectives
    and response roles from immutable evidence, then maps the headline
    verdict (plus, for "satisfied", each objective's raw value against its
    configured `penalty_threshold`) to one of the four dispositions
    (design.md#the-policy).
    """

    def __init__(
        self,
        objectives: tuple[ObjectiveSpec, ...],
        response_roles: Mapping[str, str],
        config: Any = None,
    ) -> None:
        self.objectives = tuple(objectives)
        self.response_roles = dict(response_roles)
        # Which headlines take the objective path — the one that reads objective values
        # against `penalty_threshold` and yields `penalize` or `feed-strategy`. `satisfied`
        # always does. `partial_coverage` does only when a study opted in, and then it takes
        # the *identical* path rather than a third bespoke one, so its disposition is always
        # explainable by the configuration. The assessment record still carries
        # `headline: "partial_coverage"`, so the opt-in is visible in every case row.
        # `config is None` is the no-study-config construction the protocol allows, and it
        # takes the conservative default. A config that exists must carry the field — reading
        # it by attribute rather than by `getattr` fallback means a renamed field is an
        # AttributeError here, not a silent reversion to the default.
        opt_in = "keep-for-boundary" if config is None else config.partial_coverage
        self._headlines_taking_the_objective_path = frozenset(
            {"satisfied", "partial_coverage"} if opt_in == "feed-strategy" else {"satisfied"}
        )

    def assess(self, evidence: ModelEvidence, *, candidate_id: str) -> dict[str, Any]:
        # Constraint-free empty evidence (46a) — resolved BEFORE the objective /
        # response-role loops (m1), which would otherwise raise AssessmentFailed
        # on a configured role before the headline is ever read.
        if "headline" not in evidence.responses:
            return {
                "disposition": "unconstrained", "headline": None,
                "objectives": {}, "penalty": None,
            }
        objective_values: dict[str, float] = {}
        for objective in self.objectives:
            if objective.output not in evidence.outputs:
                raise AssessmentFailed(
                    f"{candidate_id}: objective output {objective.output!r} "
                    "absent from evidence.outputs"
                )
            objective_values[objective.output] = evidence.outputs[objective.output]

        for role, constraint_id in self.response_roles.items():
            if constraint_id not in evidence.responses:
                raise AssessmentFailed(
                    f"{candidate_id}: response role {role!r} names constraint "
                    f"{constraint_id!r}, absent from evidence.responses"
                )

        headline = evidence.responses["headline"]
        if headline not in self._headlines_taking_the_objective_path:
            disposition = _disposition_for(
                headline, _HEADLINE_DISPOSITION, "_HEADLINE_DISPOSITION"
            )
            return {
                "disposition": disposition, "headline": headline,
                "objectives": objective_values, "penalty": None,
                **_coverage_of(evidence),
            }

        for objective in self.objectives:
            value = objective_values[objective.output]
            if _beyond_penalty_threshold(objective, value):
                return {
                    "disposition": "penalize", "headline": headline,
                    "objectives": objective_values, "penalty": value,
                    **_coverage_of(evidence),
                }
        return {
            "disposition": "feed-strategy", "headline": headline,
            "objectives": objective_values, "penalty": None,
            **_coverage_of(evidence),
        }


PolicyFactory = Callable[[tuple[ObjectiveSpec, ...], Mapping[str, str], Any], Policy]

# name -> factory(objectives, response_roles, policy_config). `policy_config`
# is the raw `study.config.PolicyConfig` (typed loosely here to avoid a
# policy<->config import cycle; only `ObjectivePolicy` needs it, and since
# CONSTRAINT-SEMANTICS Item 3 it reads one field off it — `partial_coverage`.
POLICY_REGISTRY: dict[str, PolicyFactory] = {
    "objective/v1": ObjectivePolicy,
}
