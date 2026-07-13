"""Verify a sealed package against its recorded ``PackageContract`` (Item 9 / D4, D5, D7).

Stdlib-only — ``hashlib``, ``json``, ``pathlib``, ``re`` — imports nothing from
sysml-codegen or any other project package. This is the canonical source; it is emitted
verbatim as ``contracts/verify.py`` inside every generated package (INV-8), so a teax
environment can verify a package it loaded without sysml-codegen installed (B3).

The verification algorithm is generic: it reads only the seal's self-description (its
recorded coverage policy, hashes, and versions), never the model, so this one small module
serves any generated package.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

TAMPER = "TAMPER"
MISSING = "MISSING"
EXTRA = "EXTRA"
# Reserved seam (Item 14 W5a disposition): the seal records `generator_version`
# (seal.py), but `verify_package` has no caller-supplied expected value to compare
# it against — no CLI flag or loader default establishes one, unlike
# `runtime_version`. Kept as a named diagnostic kind for a future generator-version
# axis; never produced today, so it no longer participates in the `strict` fatal
# check below (that expectation was dead — nothing could ever raise it).
GENERATOR_MISMATCH = "GENERATOR_MISMATCH"
RUNTIME_MISMATCH = "RUNTIME_MISMATCH"
NAME_MISMATCH = "NAME_MISMATCH"

_INTEGRITY_KINDS = frozenset({TAMPER, MISSING, EXTRA, NAME_MISMATCH})


@dataclass(frozen=True)
class Diagnostic:
    """One verification finding.

    Attributes:
        kind: One of the module-level kind constants.
        path: The relative path the finding is about, if any (``None`` for
            package-level findings like a name mismatch).
        message: Human-readable detail.
    """

    kind: str
    path: str | None
    message: str


@dataclass(frozen=True)
class VerificationResult:
    """The outcome of ``verify_package``.

    Attributes:
        ok: ``False`` on any integrity failure (tamper/missing/extra/name-mismatch,
            always fatal — D4) or on an env-compat mismatch under ``strict`` (D5).
        diagnostics: Every finding, integrity and advisory alike.
    """

    ok: bool
    diagnostics: list[Diagnostic] = field(default_factory=list)


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a ``/``-separated glob (``*``, ``?``, ``**``) to an anchored regex.

    ``**`` adjoining a slash consumes zero or more whole path segments (including the
    slash); a bare ``*``/``?`` never crosses a ``/``. Duplicated (not imported) from
    ``sysml_codegen.contracts.seal`` — this module must stay stdlib-only (D7).
    """
    out = []
    i, n = 0, len(pattern)
    while i < n:
        if pattern[i : i + 3] == "**/":
            out.append("(?:.*/)?")
            i += 3
        elif pattern[i : i + 3] == "/**" and i + 3 == n:
            out.append("(?:/.*)?")
            i += 3
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def _is_covered(rel_path: str, policy: dict) -> bool:
    patterns = [*policy["exclude_globs"], *policy["runtime_output_globs"]]
    return not any(_glob_to_regex(pattern).match(rel_path) for pattern in patterns)


def verify_package(
    package_dir: Path,
    package_name: str,
    runtime_version: str | None = None,
    strict: bool = False,
) -> VerificationResult:
    """Verify ``package_dir`` against its recorded ``contracts/package_contract.json``.

    Args:
        package_dir: The generated package's root directory.
        package_name: The name to load by (mismatch 8) — compared against the seal's
            recorded ``package_name``.
        runtime_version: The loading environment's runtime marker. ``None`` skips
            env-compat entirely.
        strict: Promote an env-compat mismatch from advisory to fatal (D5).

    Returns:
        A ``VerificationResult``. Integrity failures (tamper, missing, extra, name
        mismatch) are always fatal; env-compat mismatches are advisory unless
        ``strict``.
    """
    diagnostics: list[Diagnostic] = []
    seal_path = package_dir / "contracts" / "package_contract.json"
    seal = json.loads(seal_path.read_text())

    if seal["package_name"] != package_name:
        diagnostics.append(
            Diagnostic(
                kind=NAME_MISMATCH,
                path=None,
                message=(
                    f"requested name {package_name!r} does not match recorded "
                    f"name {seal['package_name']!r}"
                ),
            )
        )

    recorded_hashes: dict[str, str] = seal["artifact_hashes"]
    for rel_path, expected_hash in recorded_hashes.items():
        file_path = package_dir / rel_path
        if not file_path.is_file():
            diagnostics.append(
                Diagnostic(kind=MISSING, path=rel_path, message="recorded file is missing")
            )
            continue
        actual_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            diagnostics.append(
                Diagnostic(kind=TAMPER, path=rel_path, message="content hash does not match")
            )

    policy = seal["coverage_policy"]
    for path in sorted(package_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(package_dir).as_posix()
        if rel_path == "contracts/package_contract.json":
            continue
        if not _is_covered(rel_path, policy):
            continue
        if rel_path not in recorded_hashes:
            diagnostics.append(
                Diagnostic(kind=EXTRA, path=rel_path, message="file is not in the recorded seal")
            )

    if runtime_version is not None:
        if seal["runtime_contract_version"] != runtime_version:
            diagnostics.append(
                Diagnostic(
                    kind=RUNTIME_MISMATCH,
                    path=None,
                    message=(
                        f"loading environment runtime {runtime_version!r} does not match "
                        f"recorded runtime_contract_version {seal['runtime_contract_version']!r}"
                    ),
                )
            )

    fatal = any(d.kind in _INTEGRITY_KINDS for d in diagnostics) or (
        strict and any(d.kind is RUNTIME_MISMATCH for d in diagnostics)
    )
    return VerificationResult(ok=not fatal, diagnostics=diagnostics)


def verify_package_or_raise(
    package_dir: Path,
    package_name: str,
    runtime_version: str | None = None,
    strict: bool = False,
) -> VerificationResult:
    """``verify_package``, raising ``RuntimeError`` when the result is not ``ok``."""
    result = verify_package(package_dir, package_name, runtime_version, strict)
    if not result.ok:
        raise RuntimeError(
            "package verification failed: "
            + "; ".join(f"{d.kind}({d.path}): {d.message}" for d in result.diagnostics)
        )
    return result


__all__ = [
    "TAMPER",
    "MISSING",
    "EXTRA",
    "GENERATOR_MISMATCH",
    "RUNTIME_MISMATCH",
    "NAME_MISMATCH",
    "Diagnostic",
    "VerificationResult",
    "verify_package",
    "verify_package_or_raise",
]
