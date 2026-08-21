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
from pathlib import Path, PurePosixPath

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
SEAL_MISSING = "SEAL_MISSING"
SEAL_UNREADABLE = "SEAL_UNREADABLE"
SEAL_MALFORMED = "SEAL_MALFORMED"
ARTIFACT_UNREADABLE = "ARTIFACT_UNREADABLE"
INVALID_PATH = "INVALID_PATH"

_INTEGRITY_KINDS = frozenset(
    {
        TAMPER,
        MISSING,
        EXTRA,
        NAME_MISMATCH,
        SEAL_MISSING,
        SEAL_UNREADABLE,
        SEAL_MALFORMED,
        ARTIFACT_UNREADABLE,
        INVALID_PATH,
    }
)

_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_SYMLINK_MESSAGE = "symlinks are forbidden beneath the package root"


def _inspect_package_tree(root: Path) -> tuple[str | None, list[tuple[str, Path]]]:
    """Return the first forbidden symlink and a sorted clean descendant list."""
    if root.is_symlink():
        return ".", []
    paths = list(root.rglob("*"))
    entries = sorted((path.relative_to(root).as_posix(), path) for path in paths)
    for rel_path, path in entries:
        if path.is_symlink():
            return rel_path, []
    return None, entries


def _artifact_path_error(path: str) -> str | None:
    if not path:
        return "artifact path must not be empty"
    pure_path = PurePosixPath(path)
    if pure_path.is_absolute():
        return "artifact path must be package-relative"
    if pure_path.as_posix() != path or any(part in (".", "..") for part in pure_path.parts):
        return "artifact path must be canonical POSIX form without '.' or '..' segments"
    return None


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


def _seal_schema_error(seal: object) -> str | None:
    """Return a concise structural error for the stdlib-only package-seal schema."""
    if not isinstance(seal, dict):
        return "seal root must be a JSON object"

    string_fields = (
        "package_name",
        "executable_fingerprint",
        "generator_version",
        "runtime_contract_version",
    )
    for field_name in string_fields:
        if not isinstance(seal.get(field_name), str):
            return f"seal field {field_name!r} must be a string"

    artifact_hashes = seal.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in artifact_hashes.items()
    ):
        return "seal field 'artifact_hashes' must be an object of string hashes"
    for path, digest in artifact_hashes.items():
        path_error = _artifact_path_error(path)
        if path_error is not None:
            return f"invalid artifact path {path!r}: {path_error}"
        if _SHA256_HEX.fullmatch(digest) is None:
            return f"artifact digest for {path!r} must be 64 lowercase SHA-256 hex characters"
    if _SHA256_HEX.fullmatch(seal["executable_fingerprint"]) is None:
        return "seal field 'executable_fingerprint' must be 64 lowercase SHA-256 hex characters"

    policy = seal.get("coverage_policy")
    if not isinstance(policy, dict):
        return "seal field 'coverage_policy' must be an object"
    for field_name in ("exclude_globs", "runtime_output_globs"):
        patterns = policy.get(field_name)
        if not isinstance(patterns, list) or not all(
            isinstance(pattern, str) for pattern in patterns
        ):
            return f"coverage_policy field {field_name!r} must be a list of strings"
    return None


def _seal_failure(kind: str, seal_path: Path, message: str) -> VerificationResult:
    return VerificationResult(
        ok=False,
        diagnostics=[
            Diagnostic(
                kind=kind,
                path="contracts/package_contract.json",
                message=f"{seal_path}: {message}",
            )
        ],
    )


def _load_seal(seal_path: Path) -> tuple[dict | None, VerificationResult | None]:
    try:
        seal_text = seal_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, _seal_failure(SEAL_MISSING, seal_path, "seal file is missing")
    except UnicodeError as error:
        return None, _seal_failure(SEAL_MALFORMED, seal_path, f"seal is not valid UTF-8: {error}")
    except OSError as error:
        return None, _seal_failure(SEAL_UNREADABLE, seal_path, f"seal file is unreadable: {error}")
    try:
        seal = json.loads(seal_text)
    except json.JSONDecodeError as error:
        return None, _seal_failure(SEAL_MALFORMED, seal_path, f"seal is not valid JSON: {error}")
    schema_error = _seal_schema_error(seal)
    if schema_error is not None:
        return None, _seal_failure(SEAL_MALFORMED, seal_path, schema_error)
    return seal, None


def _recorded_artifact_diagnostics(
    package_dir: Path, recorded_hashes: dict[str, str]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        package_root = package_dir.resolve()
    except OSError as error:
        return [
            Diagnostic(
                kind=ARTIFACT_UNREADABLE,
                path=None,
                message=f"package root cannot be resolved: {error}",
            )
        ]
    for rel_path, expected_hash in sorted(recorded_hashes.items()):
        file_path = package_dir / rel_path
        try:
            resolved_path = file_path.resolve()
        except OSError as error:
            diagnostics.append(
                Diagnostic(kind=ARTIFACT_UNREADABLE, path=rel_path, message=str(error))
            )
            continue
        if not resolved_path.is_relative_to(package_root):
            diagnostics.append(
                Diagnostic(
                    kind=INVALID_PATH,
                    path=rel_path,
                    message="recorded artifact resolves outside the package root",
                )
            )
            continue
        try:
            is_file = file_path.is_file()
        except OSError as error:
            diagnostics.append(
                Diagnostic(kind=ARTIFACT_UNREADABLE, path=rel_path, message=str(error))
            )
            continue
        if not is_file:
            diagnostics.append(
                Diagnostic(kind=MISSING, path=rel_path, message="recorded file is missing")
            )
            continue
        try:
            content = file_path.read_bytes()
        except OSError as error:
            diagnostics.append(
                Diagnostic(kind=ARTIFACT_UNREADABLE, path=rel_path, message=str(error))
            )
            continue
        actual_hash = hashlib.sha256(content).hexdigest()
        if actual_hash != expected_hash:
            diagnostics.append(
                Diagnostic(kind=TAMPER, path=rel_path, message="content hash does not match")
            )
    return diagnostics


def _extra_artifact_diagnostics(
    entries: list[tuple[str, Path]], recorded_hashes: dict[str, str], policy: dict
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for rel_path, path in entries:
        try:
            is_file = path.is_file()
        except OSError as error:
            diagnostics.append(
                Diagnostic(
                    kind=ARTIFACT_UNREADABLE,
                    path=rel_path,
                    message=str(error),
                )
            )
            continue
        if not is_file:
            continue
        if rel_path == "contracts/package_contract.json" or not _is_covered(rel_path, policy):
            continue
        if rel_path not in recorded_hashes:
            diagnostics.append(
                Diagnostic(kind=EXTRA, path=rel_path, message="file is not in the recorded seal")
            )
    return diagnostics


def _executable_fingerprint_diagnostic(seal: dict) -> Diagnostic | None:
    recorded_hashes = seal["artifact_hashes"]
    actual = hashlib.sha256(
        "\n".join(f"{path}:{digest}" for path, digest in sorted(recorded_hashes.items())).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual == seal["executable_fingerprint"]:
        return None
    return Diagnostic(
        kind=TAMPER,
        path="contracts/package_contract.json",
        message="executable_fingerprint does not match the recorded artifact hashes",
    )


def _runtime_diagnostic(seal: dict, runtime_version: str | None) -> Diagnostic | None:
    if runtime_version is None or seal["runtime_contract_version"] == runtime_version:
        return None
    return Diagnostic(
        kind=RUNTIME_MISMATCH,
        path=None,
        message=(
            f"loading environment runtime {runtime_version!r} does not match "
            f"recorded runtime_contract_version {seal['runtime_contract_version']!r}"
        ),
    )


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
    try:
        forbidden_path, entries = _inspect_package_tree(package_dir)
    except OSError as error:
        return VerificationResult(
            ok=False,
            diagnostics=[
                Diagnostic(
                    kind=ARTIFACT_UNREADABLE,
                    path=None,
                    message=f"package artifact preflight failed: {error}",
                )
            ],
        )
    if forbidden_path is not None:
        return VerificationResult(
            ok=False,
            diagnostics=[
                Diagnostic(
                    kind=INVALID_PATH,
                    path=forbidden_path,
                    message=_FORBIDDEN_SYMLINK_MESSAGE,
                )
            ],
        )

    seal_path = package_dir / "contracts" / "package_contract.json"
    seal, failure = _load_seal(seal_path)
    if failure is not None:
        return failure
    if seal is None:  # narrowed by failure; protects optimized-Python execution too
        raise RuntimeError("seal loader returned neither a seal nor a failure")

    diagnostics: list[Diagnostic] = []

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
    fingerprint_diagnostic = _executable_fingerprint_diagnostic(seal)
    if fingerprint_diagnostic is not None:
        diagnostics.append(fingerprint_diagnostic)
    diagnostics.extend(_recorded_artifact_diagnostics(package_dir, recorded_hashes))
    diagnostics.extend(
        _extra_artifact_diagnostics(entries, recorded_hashes, seal["coverage_policy"])
    )
    runtime_diagnostic = _runtime_diagnostic(seal, runtime_version)
    if runtime_diagnostic is not None:
        diagnostics.append(runtime_diagnostic)

    fatal = any(d.kind in _INTEGRITY_KINDS for d in diagnostics) or (
        strict and any(d.kind == RUNTIME_MISMATCH for d in diagnostics)
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
    "SEAL_MISSING",
    "SEAL_UNREADABLE",
    "SEAL_MALFORMED",
    "ARTIFACT_UNREADABLE",
    "INVALID_PATH",
    "Diagnostic",
    "VerificationResult",
    "verify_package",
    "verify_package_or_raise",
]
