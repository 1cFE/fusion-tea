"""The identity seam: what executed, and what it earned the right to be called.

A generated package is sealed — every artifact's sha256 is pinned in
``contracts/package_contract.json``, and the contract also carries an
``executable_fingerprint`` that teax binds as the identity of whatever ran. A study
store refuses to resume under a different one, and that refusal is the whole of
teax's lineage discipline.

A route that *bypasses* part of the seal and then reports the sealed fingerprint is
lying about what ran: an edit to a bypassed file changes the numbers and changes
nothing about the identity. This module defines the honest alternative — an
**effective executable fingerprint** over three declared inputs:

* the sealed ``executable_fingerprint``,
* the sha256 of each file the route was allowed to have modified, and
* the sha256 of each of the route's own source files.

Touch any of them and the identity changes, so the pre-existing store refuses.

The identity travels as a small **document** (``study-package-identity/v1``), not as
an import. The route writes it; teax binds the digest in it; a generic gate
recomputes it from the document's declared inputs plus the bytes on disk and
compares. Recomputation is what makes the gate honest: it never trusts the
document's own asserted digest.

A route that bypasses nothing is the degenerate member, not a special case:
``kind: "sealed"`` has empty input lists and the sealed fingerprint as its digest,
so the same gate covers both and deleting a route's adapter changes no gate.

Generic by construction: this module names no package, no key prefix, and no adapter
(Invariant 1). It imports no teax.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

from scripts.study import common
from scripts.study import manifest as manifest_mod

IDENTITY_SCHEMA_VERSION = "study-package-identity/v1"
EFFECTIVE_RECIPE = "effective-executable-fingerprint/v1"

KIND_EFFECTIVE = "effective"
KIND_SEALED = "sealed"


class IdentityError(common.ToolError):
    """A malformed, unreadable, or disagreeing identity document."""


# ------------------------------------------------------------------- the recipe


def canonical_text(
    sealed: str,
    allowed_modified: Sequence[tuple[str, str]],
    adapter_sources: Sequence[tuple[str, str]],
) -> str:
    """The exact bytes the effective fingerprint digests.

    Line 1 the recipe id, then the sealed fingerprint, then one ``modified`` line per
    allowed-modified file and one ``adapter`` line per declared source, each sorted by
    path. Sorting makes the digest independent of the filesystem; the recipe id on
    line 1 means a future v2 cannot collide with a v1 pin.
    """
    lines = [EFFECTIVE_RECIPE, f"sealed {sealed}"]
    lines += [f"modified {path} {digest}" for path, digest in sorted(allowed_modified)]
    lines += [f"adapter {path} {digest}" for path, digest in sorted(adapter_sources)]
    return "\n".join(lines) + "\n"


def effective_digest(
    sealed: str,
    allowed_modified: Sequence[tuple[str, str]],
    adapter_sources: Sequence[tuple[str, str]],
) -> str:
    """sha256 of the recipe's canonical text."""
    text = canonical_text(sealed, allowed_modified, adapter_sources)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def adapter_source_digest(adapter_sources: Sequence[tuple[str, str]]) -> str:
    """sha256 over just the sorted ``adapter`` lines (design S1).

    The record's snapshot takes a *single* sha256 for the route's sources while a route
    may declare several. This is that value; the document also carries the per-file list
    so the single value stays auditable.
    """
    lines = [f"adapter {path} {digest}" for path, digest in sorted(adapter_sources)]
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


# ----------------------------------------------------------------- the document


def build_effective(
    *,
    package_name: str,
    package_root: Path | str,
    sealed_fingerprint: str,
    allowed_modified: Sequence[tuple[str, str]],
    adapter_sources: Sequence[tuple[str, str]],
    glue_ledger: Sequence[dict],
) -> dict:
    """The identity document for a route that bypassed part of the seal."""
    if not allowed_modified:
        raise IdentityError(
            "an effective identity with no allowed-modified files bypasses nothing; "
            f"emit kind {KIND_SEALED!r} instead"
        )
    modified = sorted(allowed_modified)
    sources = sorted(adapter_sources)
    return {
        "schema_version": IDENTITY_SCHEMA_VERSION,
        "package": {
            "name": package_name,
            "path": manifest_mod.repo_relative_posix(package_root),
        },
        "identity": {
            "kind": KIND_EFFECTIVE,
            "recipe": EFFECTIVE_RECIPE,
            "sealed_executable_fingerprint": sealed_fingerprint,
            "allowed_modified_files": [{"path": p, "sha256": d} for p, d in modified],
            "adapter_sources": [{"path": p, "sha256": d} for p, d in sources],
            "adapter_source_digest": adapter_source_digest(sources),
            "digest": effective_digest(sealed_fingerprint, modified, sources),
        },
        "glue_ledger": [dict(rung) for rung in glue_ledger],
    }


def build_sealed(*, package_name: str, package_root: Path | str) -> dict:
    """The identity document for a route that bypassed nothing.

    Its digest is *defined* to be the sealed fingerprint rather than a digest over an
    empty canonical text, so removing a route's adapter restores the package's own
    identity instead of inventing a second value for the same thing.
    """
    sealed = manifest_mod.read_executable_fingerprint(package_root)
    return {
        "schema_version": IDENTITY_SCHEMA_VERSION,
        "package": {
            "name": manifest_mod.read_package_name(package_root),
            "path": manifest_mod.repo_relative_posix(package_root),
        },
        "identity": {
            "kind": KIND_SEALED,
            "recipe": EFFECTIVE_RECIPE,
            "sealed_executable_fingerprint": sealed,
            "allowed_modified_files": [],
            "adapter_sources": [],
            "adapter_source_digest": adapter_source_digest([]),
            "digest": sealed,
        },
        "glue_ledger": [],
    }


# --------------------------------------------------------------------- reading


def _files(block: dict, field: str) -> list[tuple[str, str]]:
    entries = block.get(field)
    if not isinstance(entries, list):
        raise IdentityError(f"identity.{field}: expected a list, found {type(entries).__name__}")
    out = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
            raise IdentityError(
                f"identity.{field}[{i}]: expected {{path, sha256}}, found {entry!r}"
            )
        if not isinstance(entry["path"], str) or not isinstance(entry["sha256"], str):
            raise IdentityError(f"identity.{field}[{i}]: path and sha256 must be strings")
        out.append((entry["path"], entry["sha256"]))
    return out


def load(path: Path | str) -> dict:
    """Read and structurally validate an identity document. Does not gate it."""
    document = common.read_json(path, "package identity document")
    if not isinstance(document, dict):
        raise IdentityError("package identity document: expected an object")
    version = document.get("schema_version")
    if version != IDENTITY_SCHEMA_VERSION:
        raise IdentityError(
            f"package identity document: expected schema_version "
            f"{IDENTITY_SCHEMA_VERSION!r}, found {version!r}"
        )
    block = document.get("identity")
    if not isinstance(block, dict):
        raise IdentityError("package identity document: missing the 'identity' block")
    kind = block.get("kind")
    if kind not in (KIND_EFFECTIVE, KIND_SEALED):
        raise IdentityError(
            f"identity.kind: expected {KIND_EFFECTIVE!r} or {KIND_SEALED!r}, found {kind!r}"
        )
    if block.get("recipe") != EFFECTIVE_RECIPE:
        raise IdentityError(
            f"identity.recipe: expected {EFFECTIVE_RECIPE!r}, found {block.get('recipe')!r}"
        )
    for field in ("sealed_executable_fingerprint", "digest", "adapter_source_digest"):
        if not isinstance(block.get(field), str) or not block[field]:
            raise IdentityError(f"identity.{field}: expected a non-empty string")
    _files(block, "allowed_modified_files")
    _files(block, "adapter_sources")
    if not isinstance(document.get("glue_ledger"), list):
        raise IdentityError("package identity document: 'glue_ledger' must be a list")
    return document


# ------------------------------------------------------------------- the gate


def recompute(document: dict, package_root: Path | str) -> str:
    """Recompute the identity digest from the document's declared inputs and disk.

    Every declared file is read fresh. A file that has moved or vanished is a failure
    naming it, never a skipped input that leaves the digest looking earned.
    """
    block = document["identity"]
    package_root = Path(package_root)
    repo = manifest_mod.repo_root()
    sealed = manifest_mod.read_executable_fingerprint(package_root)

    modified = []
    for rel, _ in _files(block, "allowed_modified_files"):
        path = package_root / rel
        if not path.is_file():
            raise IdentityError(f"declared allowed-modified file is missing: {rel}")
        modified.append((rel, manifest_mod.sha256_file(path)))

    sources = []
    for rel, _ in _files(block, "adapter_sources"):
        path = repo / rel
        if not path.is_file():
            raise IdentityError(f"declared adapter source is missing: {rel}")
        sources.append((rel, manifest_mod.sha256_file(path)))

    if block["kind"] == KIND_SEALED:
        if modified or sources:
            raise IdentityError(
                f"identity.kind is {KIND_SEALED!r} but the document declares "
                f"{len(modified)} modified file(s) and {len(sources)} adapter source(s)"
            )
        return sealed
    return effective_digest(sealed, modified, sources)


def assert_seal_outside_allowed_set(document: dict, package_root: Path | str) -> None:
    """Every sealed artifact *outside* the allowed-modified set must still match.

    This is what keeps a scoped exception from widening into a blanket seal bypass:
    the route may differ on the files it declared and on nothing else.
    """
    package_root = Path(package_root)
    contract = common.read_json(
        package_root / "contracts" / "package_contract.json", "package contract"
    )
    hashes = contract.get("artifact_hashes")
    if not isinstance(hashes, dict) or not hashes:
        raise IdentityError("package contract carries no artifact_hashes")
    allowed = {rel for rel, _ in _files(document["identity"], "allowed_modified_files")}
    unknown = sorted(allowed - set(hashes))
    if unknown:
        raise IdentityError(
            "identity declares allowed-modified files that are not sealed artifacts: "
            + ", ".join(unknown)
        )
    offenders = []
    for rel, want in sorted(hashes.items()):
        if rel in allowed:
            continue
        path = package_root / rel
        if not path.is_file():
            offenders.append(f"{rel} (missing)")
        elif manifest_mod.sha256_file(path) != want:
            offenders.append(rel)
    if offenders:
        raise IdentityError(
            "sealed artifacts differ outside the declared allowed-modified set: "
            + ", ".join(offenders)
        )


def assert_matches(document: dict, package_root: Path | str) -> str:
    """The full gate. Returns the recomputed digest; raises naming the first fault."""
    recomputed = recompute(document, package_root)
    declared = document["identity"]["digest"]
    if recomputed != declared:
        raise IdentityError(
            f"identity digest mismatch: the document declares {declared} but "
            f"{EFFECTIVE_RECIPE} recomputed over the package as it stands is {recomputed}"
        )
    assert_seal_outside_allowed_set(document, package_root)
    return recomputed
