"""`CandidateBridge`: builds the complete typed entry-channel mapping for a
candidate over zero, one, or many entry channels (Lifecycle Item 9).

The bridge holds the package's `channel -> model` map (the executable truth
`PreparedEvaluator.entry_models` exposes) and a `field -> owning channel`
index. `build` produces one complete typed model per channel — the candidate's
selected fields applied over each model's own modeled defaults — and never
omits an unrelated channel (contract invariant 47).

Channel-level type validation stays in `MappingEntrySource.validate` (the
evaluate seam). This module owns only field-level checks: an unknown field
(declared by no channel) or a malformed field value fails closed as
`EvaluationFailed(ENTRY_VALIDATION)`, which the runner records as a
`StudyBridgeDefect` (design.md#d4). A field two channels declare is a
package-shape defect and fails loudly at construction (design.md#d2/A2).
"""
from __future__ import annotations

from typing import Any, Mapping

from pydantic import BaseModel, ValidationError

from ..evaluation.failure import EvaluationFailed, EvaluationFailure, EvaluationPhase


def _index_fields(entry_models: Mapping[str, type[BaseModel]]) -> dict[str, str]:
    """field name -> owning channel. Fail closed if two channels declare one
    field: a real package's entry-model field names are globally-unique PQNs,
    so a collision is a package defect, not a resolvable candidate input."""
    owner: dict[str, str] = {}
    for channel, model in entry_models.items():
        for field_name in model.model_fields:
            prior = owner.get(field_name)
            if prior is not None:
                raise ValueError(
                    f"Entry field {field_name!r} is declared by two channels "
                    f"({prior!r} and {channel!r}); the candidate namespace is ambiguous."
                )
            owner[field_name] = channel
    return owner


class CandidateBridge:
    """Builds the complete `channel -> typed model` mapping for a candidate."""

    def __init__(self, entry_models: Mapping[str, type[BaseModel]]) -> None:
        self._entry_models = dict(entry_models)
        self._owner = _index_fields(self._entry_models)

    def build(self, selected_fields: Mapping[str, Any]) -> dict[str, BaseModel]:
        # Partition selected fields onto their owning channels; an unknown
        # field fails closed before any model is constructed.
        by_channel: dict[str, dict[str, Any]] = {ch: {} for ch in self._entry_models}
        for name, value in selected_fields.items():
            channel = self._owner.get(name)
            if channel is None:
                raise EvaluationFailed(
                    EvaluationFailure(
                        phase=EvaluationPhase.ENTRY_VALIDATION,
                        cause=f"Unknown entry field {name!r} (declared by no channel)",
                    )
                )
            by_channel[channel][name] = value

        # Every channel gets a complete typed model: selected fields over the
        # model's own defaults. A defaultless required field the candidate did
        # not select, or a malformed value, fails closed here (never invented).
        try:
            return {
                channel: model(**by_channel[channel])
                for channel, model in self._entry_models.items()
            }
        except ValidationError as error:
            raise EvaluationFailed(
                EvaluationFailure(
                    phase=EvaluationPhase.ENTRY_VALIDATION,
                    cause=f"Malformed or missing entry field: {error}",
                )
            ) from error
