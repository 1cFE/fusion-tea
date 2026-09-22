"""The eight-field compatibility binding (design.md D-Architecture, INV-E).

Isolation-clean: stdlib only. Bound once at store creation; any later open
with a differing value fails explicitly (`IncompatibleStore`), starting a new
study lineage instead of silently mixing datasets.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Compatibility:
    study_id: str
    executable_fingerprint: str
    model_contract_fingerprint: str
    study_definition_fingerprint: str
    input_schema_version: str
    evidence_schema_version: str
    strategy_identity: str
    strategy_config: str  # order-preserving digest for grids (D8)

    def as_row(self) -> tuple:
        return (
            1,
            self.study_id,
            self.executable_fingerprint,
            self.model_contract_fingerprint,
            self.study_definition_fingerprint,
            self.input_schema_version,
            self.evidence_schema_version,
            self.strategy_identity,
            self.strategy_config,
        )

    @classmethod
    def from_row(cls, row) -> "Compatibility":
        return cls(
            study_id=row["study_id"],
            executable_fingerprint=row["executable_fingerprint"],
            model_contract_fingerprint=row["model_contract_fingerprint"],
            study_definition_fingerprint=row["study_definition_fingerprint"],
            input_schema_version=row["input_schema_version"],
            evidence_schema_version=row["evidence_schema_version"],
            strategy_identity=row["strategy_identity"],
            strategy_config=row["strategy_config"],
        )
