"""TEMPORARY era adapter for the stellarator package. Delete it whole when it expires.

**Deletion condition.** The stock ``ProvisionalPackageLoader`` accepts the
(regenerated) package with ``strict=True``. When it does, this file is deleted
whole, the study-local definition swaps this loader for the stock one and
``scripts/study/identity.py``'s sealed emitter, the sealed ``executable_fingerprint``
becomes the identity again, ``promotion_equivalence.py`` is deleted with it, and
``oracle_entry.py`` stays — it is the verification seam, not glue. There is no
partial retirement and no dormant compatibility branch.

This file is the *only* home for six things, and no generic tool asserts any of them:

* **The loader exception (glue rung g1).** The package's two glue-edited files differ
  from their sealed hashes. This loader runs the era's full verification and accepts
  only if every diagnostic is a ``TAMPER`` on one of exactly those two files. Any
  other diagnostic — a different file, a different diagnostic kind, an era-version
  mismatch — still refuses. It is a precisely scoped exception, not a relaxation of
  sealing, and its scope is asserted by a negative test.
* **The glue rungs g2 and g3**, the values the harness supplies that the model does
  not. The per-point ones come from ``oracle_entry.glue_values()`` so the injection
  and the verifier's recompute are one mapping in one file.
* **The self-checks**, above all the dead-filler assertion. They run on every load
  and fail closed.
* **The era-pin prerequisite**, asserted rather than merely recorded.
* **The effective executable fingerprint**, computed through
  ``scripts.study.identity``'s recipe and returned from ``load()`` in place of the
  sealed value the route did not earn.
* **The identity document**, which the route writes and the generic tools read.

**Editing this file, ``oracle_entry.py``, or ``verify_stellaris.py`` retires every
existing study store.** All three are declared sources of the effective fingerprint
(design Invariant 4, D13) because all three can move a number that is fed into a
run. That is the correct consequence and it is a sharp edge: the refusal message
names the file whose digest moved.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
E2E = HERE.parent
REPO_ROOT = E2E.parent.parent
for _path in (str(REPO_ROOT), str(HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import oracle_entry  # noqa: E402  (package-owned, beside this file)

from scripts.study import identity  # noqa: E402

#: The era teax worktree this package's v1.0.0 seal was generated and certified under.
#: Current teax main refuses that seal, and its refusal is principled — see ANNEX.md
#: § Era pin. The pin is asserted on every load, not merely recorded.
ERA_PIN_COMMIT = "fa0e06a"

#: Glue rung g1: the two sealed artifacts the committed glue edits changed. Nothing
#: else may differ. This set is the loader's entire accept-set and the identity
#: document's entire allowed-modified set.
GLUE_EDITED_FILES = ("inputs/system_design.json", "pipelines/mfe_stellarator.yaml")

#: Invariant 4: every file whose content can change a glue value or the accept-set.
DECLARED_SOURCES = (
    "exploration/stellarator_e2e/studies/era_adapter.py",
    "exploration/stellarator_e2e/studies/oracle_entry.py",
    "exploration/stellarator_e2e/verify_stellaris.py",
)

#: Glue rung g2, the constant half: values codegen could not resolve a default for.
#: The per-point half of g2 and all of g3 come from ``oracle_entry.glue_values()``.
P = oracle_entry.P
GLUE_CONSTANTS: dict[str, float] = {
    f"{P}cas23_to_28_capital__cas28_capital": 5_000_000.0,
    f"{P}cas2x_pre_contingency__cas28_capital": 5_000_000.0,
    f"{P}replacement_cost_per_event__n_mod": 1.0,
}

#: What the record snapshots as this route's glue ledger.
GLUE_LEDGER = [
    {
        "rung": "g1",
        "keys": list(GLUE_EDITED_FILES),
        "supplies": "the two sealed artifacts the committed glue edits changed: the BOP "
                    "repoint and three schema fillers. The loader accepts a TAMPER on "
                    "exactly these two and refuses anything else.",
        "independently_verified": True,
        "note": "Verified by recomputation, not by assertion: every other sealed artifact "
                "is checked against the seal on every load, and the effective executable "
                "fingerprint carries these two files' actual digests.",
    },
    {
        "rung": "g2",
        "keys": sorted(GLUE_CONSTANTS)
        + ["mfe_plant__MFE_Power_Plant__p_th",
           "mfe_plant__MFE_Power_Plant__p_the",
           "mfe_plant__MFE_Power_Plant__p_et"],
        "supplies": "constant injections per proposal: the CAS28 costing constant (2 keys, "
                    "5.0 M$), the declared replacement n_mod default codegen could not "
                    "resolve, and three dead schema fillers.",
        "independently_verified": True,
        "note": "The three p_* fillers are asserted dead on every load — nothing in the "
                "executed pipeline spec reads them — so they move no number either way.",
    },
    {
        "rung": "g3",
        "keys": [f"{P}cas23_to_28_capital__special_materials_capital",
                 f"{P}cas2x_pre_contingency__special_materials_capital"],
        "supplies": "CAS27 special materials capital, a function of the radial-build "
                    "blanket volume the package cannot wire cross-part. Recomputed per "
                    "point from the same formula the oracle uses, so off-baseline points "
                    "stay self-consistent.",
        "independently_verified": False,
        "note": "Fed identically to the package and to the oracle, so oracle parity "
                "verifies the package's arithmetic GIVEN this value. The CAS27 "
                "ingredient itself is NOT independently verified.",
    },
]


class EraAdapterError(Exception):
    """A self-check failed. Every one fails the load closed."""


# ---------------------------------------------------------------- prerequisites


def assert_era_pin(simkit_module) -> str:
    """The pinned era teax must be the one on ``sys.path``. Asserted, not recorded."""
    worktree = Path(simkit_module.__file__).resolve().parents[2]
    done = subprocess.run(
        ["git", "-C", str(worktree), "rev-parse", "HEAD"], capture_output=True, text=True
    )
    found = done.stdout.strip()
    if done.returncode != 0 or not found.startswith(ERA_PIN_COMMIT):
        raise EraAdapterError(
            f"era pin violated: this adapter runs only under teax at {ERA_PIN_COMMIT}, "
            f"but the simkit on sys.path is {worktree}, which is at "
            f"{found or 'no git HEAD'}. See ANNEX.md § Era pin."
        )
    return found


def assert_schema_fillers_are_dead(package_root: Path, spec_path: Path) -> None:
    """The three ``p_*`` fillers must be read by nothing in the executed pipeline.

    Glue feeds these fillers per point from the oracle. A live consumer wired from
    *any* channel would therefore be undisclosed both-sides circularity, so the
    pattern is deliberately broad: a resurrection of any kind trips this.
    """
    text = spec_path.read_text()
    if "MFE_Power_Plant__p_" in text:
        raise EraAdapterError(
            f"schema fillers are LIVE in the executed pipeline spec "
            f"({spec_path.relative_to(package_root)}): glue feeds these keys per point "
            f"from the oracle, so a consumer makes the run undisclosed both-sides "
            f"circularity. Stale-input hazard; refusing to load."
        )


# ------------------------------------------------------------- the glue-aware loader


class GlueAwareLoader:
    """A ``ProvisionalPackageLoader`` accepting EXACTLY the documented glue edits.

    Runs the era's full verification — version gate, authenticated verifier, per-file
    hashes — and returns the **effective** executable fingerprint, never the sealed
    one the route did not earn.
    """

    def __init__(self, inner, spec_path: Path) -> None:
        self._inner = inner
        self._spec_path = Path(spec_path)

    @property
    def package_dir(self) -> Path:
        return Path(self._inner.package_dir)

    def load(self):
        from simkit.evaluation import package_load as pl

        package_dir = self.package_dir
        seal = json.loads((package_dir / "contracts" / "package_contract.json").read_text())
        version = seal.get("runtime_contract_version")
        if version not in pl.ACCEPTED_RUNTIME_CONTRACT_VERSIONS:
            raise pl.SealVerificationError(
                f"era mismatch: package declares runtime_contract_version {version!r}, "
                f"which this teax does not accept"
            )
        verifier = pl._load_authenticated_verifier(package_dir)
        result = verifier.verify_package(
            package_dir, self._inner.package_name, runtime_version=version, strict=True
        )
        offenders = {(d.kind, d.path) for d in result.diagnostics}
        unexpected = offenders - {("TAMPER", path) for path in GLUE_EDITED_FILES}
        if unexpected:
            raise pl.SealVerificationError(
                f"seal diagnostics beyond the documented glue edits: {sorted(unexpected)}. "
                f"The accept-set is exactly a TAMPER on {list(GLUE_EDITED_FILES)}; "
                f"anything else refuses."
            )

        # Self-checks run on every load, not once at authoring time.
        import simkit

        assert_era_pin(simkit)
        assert_schema_fillers_are_dead(package_dir, self._spec_path)

        return self._inner._load_module(), effective_fingerprint(package_dir)


def loader(package_dir: Path | str, link_root: Path | str, *,
           package_name: str = "stellarator_tea", spec_path: Path | str | None = None):
    """Build the glue-aware loader for a package tree.

    ``link_root`` is the caller's, deliberately with no default: the era loader writes
    an import symlink into it, and a default under the package would dirty the very
    tree the cleanliness gate watches. Both paths are resolved, because the symlink
    the era writes is absolute-or-broken.
    """
    from simkit.evaluation.package_load import ProvisionalPackageLoader

    package_dir = Path(package_dir).resolve()
    spec_path = Path(spec_path) if spec_path else package_dir / "pipelines" / "mfe_stellarator.yaml"
    link_root = Path(link_root).resolve()
    inner = ProvisionalPackageLoader(
        package_dir=package_dir, package_name=package_name, link_root=link_root
    )
    return GlueAwareLoader(inner, spec_path)


# --------------------------------------------------------------- the identity seam


def _declared_digests(package_dir: Path):
    from scripts.study import manifest as manifest_mod

    modified = []
    for rel in GLUE_EDITED_FILES:
        path = package_dir / rel
        if not path.is_file():
            raise EraAdapterError(f"declared glue-edited file is missing from the package: {rel}")
        modified.append((rel, manifest_mod.sha256_file(path)))
    sources = []
    for rel in DECLARED_SOURCES:
        path = REPO_ROOT / rel
        if not path.is_file():
            raise EraAdapterError(f"declared adapter source is missing: {rel}")
        sources.append((rel, manifest_mod.sha256_file(path)))
    return modified, sources


def identity_document(package_dir: Path | str) -> dict:
    """The document the route writes: what this adapter bypassed, and what that earns."""
    from scripts.study import manifest as manifest_mod

    package_dir = Path(package_dir)
    modified, sources = _declared_digests(package_dir)
    return identity.build_effective(
        package_name=manifest_mod.read_package_name(package_dir),
        package_root=package_dir,
        sealed_fingerprint=manifest_mod.read_executable_fingerprint(package_dir),
        allowed_modified=modified,
        adapter_sources=sources,
        glue_ledger=GLUE_LEDGER,
    )


def effective_fingerprint(package_dir: Path | str) -> str:
    """The identity teax binds: the digest of the document above."""
    return identity_document(package_dir)["identity"]["digest"]


def write_identity_document(package_dir: Path | str, out_path: Path | str) -> Path:
    from scripts.study import common

    return common.write_document(identity_document(package_dir), out_path)


# --------------------------------------------------------------------- glue rungs


def glue_fields(point: Mapping[str, float]) -> dict[str, float]:
    """Rungs g2 and g3 at one point: the constants, plus the per-point oracle values."""
    fields = dict(GLUE_CONSTANTS)
    fields.update(oracle_entry.glue_values(point))
    return fields
