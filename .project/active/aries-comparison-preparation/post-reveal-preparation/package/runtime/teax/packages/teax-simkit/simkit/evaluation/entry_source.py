"""Typed, in-memory entry source (Shape A — instantiated-models-only).

Isolation-clean: imports only stdlib, ``pydantic``, and ``simkit``-internal
modules. See ``design.md#required-invariants`` INV1 and ``design.md`` D1.

Ported from ``real_evaluator.py``'s ``MappingEntrySource``, unchanged in
shape: the caller owns building each channel's typed model; this source only
refuses a missing/extra/wrong channel-model instance. A non-finite float
passes by construction (B3, INV2) — nothing here performs float validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from pydantic import BaseModel

from .failure import EvaluationFailed, EvaluationFailure, EvaluationPhase


@dataclass(frozen=True)
class MappingEntrySource:
    """Strict, already-typed values keyed by EntryPoint channel ID."""

    expected_types: Mapping[str, type[BaseModel]]

    @classmethod
    def from_spec(cls, specification: Any, schema_types: Mapping[str, type]) -> "MappingEntrySource":
        entry = next(m for m in specification.modules.values() if m.is_entry)
        expected: dict[str, type[BaseModel]] = {}
        for binding in entry.outputs.values():
            expected_type = schema_types.get(binding.type_name)
            if expected_type is None:
                raise TypeError(
                    f"Entry channel {binding.channel_name!r} has unknown type {binding.type_name!r}"
                )
            expected[binding.channel_name] = expected_type
        return cls(expected_types=MappingProxyType(expected))

    def validate(self, values: Mapping[str, Any]) -> Mapping[str, BaseModel]:
        expected_keys = set(self.expected_types)
        supplied_keys = set(values)
        missing = sorted(expected_keys - supplied_keys)
        extra = sorted(supplied_keys - expected_keys)
        if missing or extra:
            raise EvaluationFailed(
                EvaluationFailure(
                    phase=EvaluationPhase.ENTRY_VALIDATION,
                    cause=f"Entry mapping key mismatch: missing={missing}, extra={extra}",
                )
            )
        validated: dict[str, BaseModel] = {}
        for channel_name, expected_type in self.expected_types.items():
            value = values[channel_name]
            if not isinstance(value, expected_type):
                raise EvaluationFailed(
                    EvaluationFailure(
                        phase=EvaluationPhase.ENTRY_VALIDATION,
                        cause=(
                            f"Entry channel {channel_name!r} expects "
                            f"{expected_type.__name__}, got {type(value).__name__}"
                        ),
                        module_or_channel=channel_name,
                    )
                )
            validated[channel_name] = value
        return MappingProxyType(validated)
