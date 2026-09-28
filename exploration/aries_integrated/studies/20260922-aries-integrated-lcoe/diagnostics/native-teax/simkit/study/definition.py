"""`StudyDefinition`: binds a study's strategy, injected validator/policy, and
the compatibility fingerprints the store binds at creation (INV-E).

Variable selection resolves to a *field* of some entry-channel model (Item 9:
zero, one, or many channels), not a flat parameter-ID map — the raw dicts a
strategy proposes are keyed by entry-model field name, and `CandidateBridge`
routes each field to its owning channel and builds the complete typed mapping.
"Cannot redefine a predicate": this item carries no API for mutating constraint
definitions, only for selecting existing contract parameters via the
strategy/bridge (spec.md#studydefinition).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from pydantic import BaseModel

from .compatibility import Compatibility
from .policy import ObjectiveSpec, Policy
from .strategy import CandidateStrategy

ProposalValidator = Callable[[Mapping[str, Any]], Mapping[str, Any] | None]
"""Returns canonicalized inputs for a valid proposal, or `None` if invalid.

Validity means malformed / missing / wrong-type only — **never** non-finite;
a non-finite value is a well-formed candidate the model evaluates to
`indeterminate` (spec.md#runner).
"""


@dataclass(frozen=True)
class StudyDefinition:
    study_id: str
    # Complete channel -> typed model map (Item 9), from PreparedEvaluator.entry_models.
    # Replaces the single-entry scalar entry_channel/entry_model.
    entry_models: Mapping[str, type[BaseModel]]
    strategy: CandidateStrategy
    validate_proposal: ProposalValidator
    policy: Policy
    executable_fingerprint: str
    model_contract_fingerprint: str
    input_schema_version: str
    evidence_schema_version: str
    study_definition_fingerprint: str
    # Objective/response-role interpretation for the policy (Item 12 D4);
    # empty defaults keep Item 11's hand-assembled definitions compiling.
    objectives: tuple[ObjectiveSpec, ...] = ()
    response_roles: Mapping[str, str] = field(default_factory=dict)
    # Carried per spec.md#studydefinition; interpretation is Item 12's.
    budget: Any = None
    retention: Any = None

    def compatibility(self) -> Compatibility:
        return Compatibility(
            study_id=self.study_id,
            executable_fingerprint=self.executable_fingerprint,
            model_contract_fingerprint=self.model_contract_fingerprint,
            study_definition_fingerprint=self.study_definition_fingerprint,
            input_schema_version=self.input_schema_version,
            evidence_schema_version=self.evidence_schema_version,
            strategy_identity=self.strategy.identity,
            strategy_config=self.strategy.config_fingerprint(),
        )
