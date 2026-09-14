"""`load_model_contract`: the one seam that reads a package's embedded catalog + identity.

Codegen's embedded constraint catalog is the sole schema authority (owner decision D-3): every
generated package ships ``contracts/model_contract.json`` carrying the catalog by value plus the
real ``semantic_fingerprint``. TEAx reads it here and nowhere else — no alternate standalone
``constraint_catalog.json``, no QN-splitting, no predicate-text reconstruction.

Fail-closed skew (INV-4): the read rejects any ``catalog_schema_version`` outside the vendored
accepted set *before* any field is read, in both directions (package newer or older than TEAx).
TEAx never imports ``sysml_codegen`` (B3); the accepted set is vendored by copy in
``evaluation/package_load.py`` beside ``ACCEPTED_RUNTIME_CONTRACT_VERSIONS``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from simkit.evaluation.package_load import ACCEPTED_CATALOG_SCHEMA_VERSIONS


class IncompatibleCatalogSchema(Exception):
    """The package's embedded-catalog schema version is not one this runtime accepts."""


@dataclass(frozen=True)
class ModelContractData:
    """The parsed, version-checked model contract — the embedded catalog + real identity."""

    semantic_fingerprint: str
    catalog_schema_version: str
    #: ``constraint_id -> concrete entry dict`` (empty on a constraint-free package).
    concrete_entries: Mapping[str, Mapping[str, Any]]
    #: Admitted per-usage records, verbatim.
    usage_records: list[Mapping[str, Any]]
    #: The whole parsed contract, for callers that need more than the catalog.
    raw: Mapping[str, Any]


def load_model_contract(package_dir: str | Path) -> ModelContractData:
    """Read ``contracts/model_contract.json``, fail closed on an unaccepted schema version."""
    path = Path(package_dir) / "contracts" / "model_contract.json"
    raw = json.loads(path.read_text())
    version = raw.get("catalog_schema_version")
    if version not in ACCEPTED_CATALOG_SCHEMA_VERSIONS:
        raise IncompatibleCatalogSchema(
            f"{path}: catalog_schema_version {version!r} is not accepted by this runtime "
            f"(accepts {sorted(ACCEPTED_CATALOG_SCHEMA_VERSIONS)}). The generated package and "
            "the runtime are on incompatible catalog schemas — regenerate or update the runtime; "
            "no field is read across a schema skew."
        )
    catalog = raw.get("constraint_catalog") or {}
    entries = {e["constraint_id"]: e for e in catalog.get("concrete_entries", [])}
    return ModelContractData(
        semantic_fingerprint=raw["semantic_fingerprint"],
        catalog_schema_version=version,
        concrete_entries=entries,
        usage_records=list(catalog.get("usage_records", [])),
        raw=raw,
    )


def ships_constraint_report(contract: ModelContractData) -> bool:
    """Does this package ship a constraint report? The one consumer-side authority.

    The same population the producer's rule reads: a report exists iff the model authored at
    least one constraint usage. Reading `concrete_entries` instead answers "is there anything
    to execute", which since CONSTRAINT-SEMANTICS Item 3 is a different question — a model
    with 65 declared constraints and none eligible ships a report that says so.

    This used to be answered twice on the consumer side: here, from the catalog, and again in
    `evaluation/evaluator.py` from the pipeline spec. The evaluation layer is isolation-clean
    and genuinely has no catalog authority, so its derivation was invented rather than read;
    it is deleted and `expects_constraint_report` is a required argument there instead.
    """
    return bool(contract.usage_records)
