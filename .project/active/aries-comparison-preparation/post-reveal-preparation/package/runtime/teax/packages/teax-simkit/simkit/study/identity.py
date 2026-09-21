"""Canonical JSON bytes, sha256 digests, and positional ID minting.

Isolation-clean: stdlib only. `canonical_bytes` sorts *object keys*
(`sort_keys=True`); it never reorders a JSON array. That distinction is what
makes D8's order-sensitive `strategy_config` shape work: encoding declared
variable order as an array of `[name, domain]` pairs (never a `{name:
domain}` object) keeps the order-bearing bytes order-sensitive, because
`sort_keys` cannot touch array element order.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(obj: Any) -> bytes:
    """Deterministic JSON bytes: sorted object keys, no incidental whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_of(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def mint_proposal_id(study_id: str, index: int) -> str:
    return f"{study_id}:p{index:04d}"


def mint_candidate_id(study_id: str, index: int) -> str:
    return f"{study_id}:c{index:04d}"


def mint_attempt_id(candidate_id: str, attempt_number: int) -> str:
    return f"{candidate_id}:a{attempt_number}"
