"""Serializes `ModelEvidence` for staging (D3, INV-H, MF-3).

Isolation-clean: never imports a generated report class — reads `report`
only via `model_dump(mode="json")` (a `pydantic.BaseModel` method every
generated report has, never introspected further). The dict this module
produces is handed unchanged to `StudyStore.commit_case`, which is the
single function that turns it into both the on-disk bytes and the digest
(INV-H: one source, so the two cannot drift).
"""
from __future__ import annotations

import math
from typing import Any, Mapping

from simkit.evaluation.evidence import ModelEvidence

NONFINITE_KEY = "__nonfinite__"


def _tag_nonfinite(value: Any) -> Any:
    # Walk ``Mapping``/``(list, tuple)`` so the deep-frozen report tree
    # (``MappingProxyType``/``tuple``, D2) is traversed and emitted as plain
    # ``dict``/``list`` — INV-G byte-identity and the MF-3 guard both hold on it.
    if isinstance(value, float) and not math.isfinite(value):
        tag = "nan" if math.isnan(value) else ("inf" if value > 0 else "-inf")
        return {NONFINITE_KEY: tag}
    if isinstance(value, Mapping):
        if set(value) == {NONFINITE_KEY}:
            raise ValueError(
                f"reserved key {NONFINITE_KEY!r} collision in evidence payload: {value!r}"
            )
        return {key: _tag_nonfinite(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_tag_nonfinite(val) for val in value]
    return value


def encode_evidence(evidence: ModelEvidence) -> dict[str, Any]:
    """Recursively sentinel-tag non-finite floats across the whole payload.

    Used for **both** the digest input and the on-disk bytes (D3) — unlike
    Item 10's `_json_safe` (`evaluator.py`), which is digest-input only and
    never read back. Rejects loudly (`ValueError`) if a genuine value is
    already a one-key `{"__nonfinite__": ...}` mapping (MF-3): the generated
    report is a typed schema that cannot emit this key, so a collision means
    an unexpected report shape that must fail rather than be papered over.
    """
    payload = {
        "responses": dict(evidence.responses),
        "outputs": dict(evidence.outputs),
        "provenance": evidence.provenance.model_dump(mode="json"),
        # The report is already the sealed ``model_dump(mode="json")`` tree (D2)
        # — no second dump here; ``_tag_nonfinite`` walks the frozen tree and
        # emits plain dict/list. ``None`` for a constraint-free package (46a).
        "report": evidence.report,
    }
    return _tag_nonfinite(payload)


def _untag_nonfinite(value: Any) -> Any:
    if isinstance(value, Mapping):
        if set(value) == {NONFINITE_KEY}:
            return {"nan": math.nan, "inf": math.inf, "-inf": -math.inf}[value[NONFINITE_KEY]]
        return {key: _untag_nonfinite(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_untag_nonfinite(val) for val in value]
    return value


def decode_evidence(payload: dict[str, Any]) -> dict[str, Any]:
    """The exact inverse of `encode_evidence`'s sentinel tagging (D5, INV-3):
    a one-key `{"__nonfinite__": ...}` dict decodes back to the real float;
    every other dict/list is recursed identically, so no sentinel-shaped
    dict leaks to the caller and no other one-key dict is ever touched.
    """
    return _untag_nonfinite(payload)
