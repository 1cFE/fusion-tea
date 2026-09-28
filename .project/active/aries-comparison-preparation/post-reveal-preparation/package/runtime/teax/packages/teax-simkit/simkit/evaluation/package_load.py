"""Sealed-package loading (touches the generated package — D2).

Every generated package carries the canonical stdlib-only verifier at ``contracts/verify.py``
(sysml-codegen Item 9, INV-8), so a teax environment can verify a package with nothing but the
package itself — it does not import sysml-codegen (B3). But the package cannot be trusted to
supply its own verifier: a tampered package could ship an unconditional-success stub. So this
loader carries two **runtime-owned trust anchors** (Item 7):

- ``TRUSTED_VERIFIER_SHA256`` — the sha256 of the canonical verifier. The loader reads the
  package-local ``verify.py`` once, authenticates its bytes against this constant, and executes
  *exactly those bytes*. A stub has different bytes and is rejected before any package code
  runs. This is a hash, not a second verifier: verification semantics stay in the one canonical
  module; only its fingerprint is vendored, so there is nothing to drift.
- ``ACCEPTED_RUNTIME_CONTRACT_VERSIONS`` — the runtime-contract versions this loader speaks.
  A seal recorded against any other version is rejected, fail-closed in both skew directions.

Both anchors are vendored from ``sysml_codegen.contracts.versions`` (a package cannot influence
them). B3 forbids importing that module at runtime, so cross-repo agreement rests on those
constants plus manual re-vendoring, backed by sysml-codegen's own drift test. The
symlink-under-declared-name import mechanism below is unrelated and unchanged.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Protocol

ACCEPTED_RUNTIME_CONTRACT_VERSIONS = frozenset({"2.0.0"})
"""The runtime-contract versions this loader accepts. Vendored from
``sysml_codegen.contracts.versions.RUNTIME_CONTRACT_VERSION`` (one image per version, Item 7
D3). A seal recorded against a version outside this set is rejected — fail-closed whether the
package is newer or older than the runtime.

Re-vendored to ``2.0.0`` at CONSTRAINT-SEMANTICS Item 3. The set is **replaced, not extended**:
a package built before that item emits the retired headline token ``all_satisfied`` and carries
no ``coverage`` block, so accepting it would mean reading a report this runtime cannot map.
Refusing at seal verification is the earliest and clearest place to say so."""

ACCEPTED_CATALOG_SCHEMA_VERSIONS = frozenset({"3.0.0"})
"""The embedded-catalog schema versions this runtime reads (Item 8). Vendored from
``sysml_codegen.contracts.versions.CATALOG_SCHEMA_VERSION`` — the same by-copy rail as the
runtime-contract set (B3 forbids importing sysml-codegen). ``study.model_contract.load_model_contract``
fails closed on any ``catalog_schema_version`` outside this set, before reading a catalog field,
in both skew directions. Re-vendor in lockstep with a codegen schema bump; codegen's
``test_catalog_schema_version`` guards the source side.

Re-vendored to ``3.0.0`` at CONSTRAINT-SEMANTICS Item 3, catching up with Item 2's codegen-side
bump — that widened ``usage_records`` from admitted-only to the whole authored domain and re-keyed
every row on ``declaration_id``, which is exactly the population ``ships_constraint_report`` now
reads. Item 3 itself adds no catalog field."""

TRUSTED_VERIFIER_SHA256 = "ad0a855af17d18af5f3e8c36b1a6c500f492d88ec777b40f307c646306c67284"
"""sha256 of the canonical ``contracts/verify.py``, vendored from
``sysml_codegen.contracts.versions.TRUSTED_VERIFIER_SHA256``. The loader authenticates a
package-local verifier's bytes against this before executing them. Re-vendor in lockstep with a
verify.py change (and its version bump); sysml-codegen's drift test guards the source side."""


class SealVerificationError(Exception):
    """The on-disk package no longer matches its sealed contract."""


class PackageLoader(Protocol):
    def load(self) -> tuple[ModuleType, str]:
        """Load the sealed package, returning (module, executable_fingerprint)."""
        ...


def _load_authenticated_verifier(package_dir: Path) -> ModuleType:
    """Authenticate the package-local ``contracts/verify.py`` bytes, then execute *those* bytes.

    Read the file once, hash it against ``TRUSTED_VERIFIER_SHA256``, and on match execute the
    exact bytes just hashed via ``exec(compile(...))``. This closes the time-of-check/
    time-of-use seam that ``exec_module`` would open by re-reading an attacker-controlled path:
    the authenticated bytes and the executed bytes are one and the same read. No package code
    runs before the hash gate (INV-A).
    """
    verify_path = package_dir / "contracts" / "verify.py"
    try:
        source = verify_path.read_bytes()
    except OSError as error:
        raise SealVerificationError(
            f"seal violation: cannot read verifier at {verify_path}: {error}"
        ) from error
    actual = hashlib.sha256(source).hexdigest()
    if actual != TRUSTED_VERIFIER_SHA256:
        raise SealVerificationError(
            "seal violation: package-local verifier is not the trusted canonical verifier "
            f"(sha256 {actual} != {TRUSTED_VERIFIER_SHA256}); refusing to execute it"
        )
    module = ModuleType("_package_contract_verify")
    module.__file__ = str(verify_path)
    sys.modules[module.__name__] = module
    exec(compile(source, str(verify_path), "exec"), module.__dict__)
    return module


@dataclass(frozen=True)
class ProvisionalPackageLoader:
    """Loads a sealed package tree under its declared import name.

    The package's internal imports are absolute to its declared name (e.g.
    ``from my_plant_pkg. ...``), so the on-disk directory is exposed under that
    name via a symlink placed in ``link_root`` (caller-supplied — this loader
    has no opinion on where that lives).
    """

    package_dir: Path
    package_name: str
    link_root: Path
    strict: bool = True

    def load(self) -> tuple[ModuleType, str]:
        fingerprint = self._verify_seal()
        module = self._load_module()
        return module, fingerprint

    def _verify_seal(self) -> str:
        seal_path = self.package_dir / "contracts" / "package_contract.json"
        try:
            seal = json.loads(seal_path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise SealVerificationError(f"seal violation: seal is unreadable: {error}") from error

        # (1) Fail-closed version policy (Item 7). Reject a seal recorded against a runtime
        # contract this loader does not speak, in either skew direction. Reads seal data only —
        # no package code — so it is safe ahead of verifier authentication.
        recorded_version = seal.get("runtime_contract_version")
        if recorded_version not in ACCEPTED_RUNTIME_CONTRACT_VERSIONS:
            raise SealVerificationError(
                f"seal violation: recorded runtime_contract_version {recorded_version!r} is not "
                f"in the accepted runtime-contract versions "
                f"{sorted(ACCEPTED_RUNTIME_CONTRACT_VERSIONS)}"
            )

        # (2) Authenticate the verifier bytes, then run them for the integrity check. The
        # loader owns version acceptance (above), so the verifier's own env-compat check is a
        # satisfied no-op here — pass the seal's own version.
        verify = _load_authenticated_verifier(self.package_dir)
        result = verify.verify_package(
            self.package_dir,
            self.package_name,
            runtime_version=recorded_version,
            strict=self.strict,
        )
        if not result.ok:
            details = "; ".join(f"{d.kind}({d.path}): {d.message}" for d in result.diagnostics)
            raise SealVerificationError(f"seal violation: {details}")
        return seal["executable_fingerprint"]

    def _load_module(self) -> ModuleType:
        self.link_root.mkdir(parents=True, exist_ok=True)
        link = self.link_root / self.package_name
        if not link.exists():
            link.symlink_to(self.package_dir, target_is_directory=True)
        if str(self.link_root) not in sys.path:
            sys.path.insert(0, str(self.link_root))
        return importlib.import_module(self.package_name)
