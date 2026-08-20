"""Package-catalog seam for the study indicator tool.

Owns three things and no logic beyond them:

1. The study-package manifest schema (``study-package-manifest/v1``) and a strict,
   hand-rolled validator — every unknown key anywhere is a mechanical failure.
2. The two digest recipes: ``indicator-input-fingerprint/v1`` over the package
   artifacts the trace reads, and ``tool-source-digest/v1`` over this tool's own
   source files.
3. The small checks that read the manifest against a live package: the package
   identity check and the read-set coverage check.

Everything here is mechanism. Every failure raises :class:`ManifestError`, which
the CLI turns into a non-zero exit with no output written.

Generic by construction: this module names no package, no key prefix, and no
adapter (Invariant 6).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

MANIFEST_SCHEMA_VERSION = "study-package-manifest/v1"
INDICATOR_INPUT_RECIPE = "indicator-input-fingerprint/v1"
TOOL_SOURCE_RECIPE = "tool-source-digest/v1"

#: Files whose bytes make up the tool-source digest (M5). The schema files are in
#: the set because they are the seam Items 2 and 4 cite — a schema edit is a tool change.
TOOL_SOURCE_FILES = (
    "scripts/study/indicators.py",
    "scripts/study/manifest.py",
    "scripts/study/schemas/axis_declaration.v1.schema.json",
    "scripts/study/schemas/indicators.v1.schema.json",
    "scripts/study/schemas/study_package_manifest.v1.schema.json",
)

#: YAML-family suffixes that are *not* the globbed ``.yaml``. A pipeline carrying one
#: of these would be silently skipped by the glob, so its presence is a failure (M1).
#: Every other file in ``pipelines/`` is ignored — ``__init__.py`` is a sealed artifact
#: of every generated package, and a rule that refused it would refuse every package.
_STRAY_YAML_SUFFIXES = frozenset({".yml", ".YAML", ".Yaml", ".YML", ".Yml", ".yAML"})


class ManifestError(Exception):
    """Mechanical failure reading, validating, or checking a package manifest."""


# --------------------------------------------------------------------- paths


def repo_root() -> Path:
    """The repository root: two levels above ``scripts/study/``."""
    return Path(__file__).resolve().parents[2]


def repo_relative_posix(path: Path | str) -> str:
    """A repo-relative POSIX path string (M4).

    Never absolute, so two agents invoking from different working directories
    produce identical bytes for identical facts. A path outside the repository
    renders with leading ``..`` segments rather than as an absolute path.
    """
    return Path(os.path.relpath(Path(path).resolve(), repo_root())).as_posix()


def package_relative_posix(path: Path | str, package_root: Path | str) -> str:
    """A package-relative POSIX path string, as the manifest's pinned list uses."""
    return Path(os.path.relpath(Path(path).resolve(), Path(package_root).resolve())).as_posix()


# ------------------------------------------------------------------ digests


def sha256_file(path: Path | str) -> str:
    """sha256 over a file's raw bytes — no text normalization.

    A normalizer would hide an edit the trace can see.
    """
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _canonical_digest(recipe: str, entries: list[tuple[str, str]]) -> str:
    """sha256 of the canonical text: recipe id, then one ``<path> <sha256>`` line each.

    Entries are sorted by path, so the order is independent of the filesystem, and
    the recipe id on line 1 means a future v2 recipe cannot collide with a v1 pin.
    """
    lines = [recipe] + [f"{path} {digest}" for path, digest in sorted(entries)]
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def indicator_input_read_set(package_root: Path | str) -> list[Path]:
    """The artifacts the trace reads: every pipeline YAML, every inputs JSON, the model contract.

    Glob-only and parse-free, so the pre-parse fingerprint gate needs no reader.
    An empty leg is a mechanical failure rather than a silent skip.
    """
    root = Path(package_root)
    pipeline_dir = root / "pipelines"
    stray = sorted(
        p.name
        for p in (pipeline_dir.iterdir() if pipeline_dir.is_dir() else [])
        if p.is_file() and p.suffix in _STRAY_YAML_SUFFIXES
    )
    if stray:
        raise ManifestError(
            "pipelines/ holds YAML-family files the '*.yaml' glob would miss: " + ", ".join(stray)
        )

    pipelines = sorted(pipeline_dir.glob("*.yaml"))
    inputs = sorted((root / "inputs").glob("*.json"))
    contract = root / "contracts" / "model_contract.json"
    if not pipelines:
        raise ManifestError("no pipeline files at pipelines/*.yaml")
    if not inputs:
        raise ManifestError("no input files at inputs/*.json")
    if not contract.is_file():
        raise ManifestError("missing model contract at contracts/model_contract.json")
    return [*pipelines, *inputs, contract]


def indicator_input_fingerprint(package_root: Path | str) -> dict:
    """Compute ``indicator-input-fingerprint/v1`` over a package's trace-read artifacts.

    Returns the recipe id, the digest, and the per-file digests keyed on
    package-relative POSIX paths — the same form the manifest pins.
    """
    root = Path(package_root)
    files = [
        {"path": package_relative_posix(p, root), "sha256": sha256_file(p)}
        for p in indicator_input_read_set(root)
    ]
    files.sort(key=lambda f: f["path"])
    return {
        "recipe": INDICATOR_INPUT_RECIPE,
        "digest": _canonical_digest(
            INDICATOR_INPUT_RECIPE, [(f["path"], f["sha256"]) for f in files]
        ),
        "files": files,
    }


def tool_source_digest() -> dict:
    """Compute ``tool-source-digest/v1`` over this tool's own source files (M5)."""
    root = repo_root()
    entries = []
    for rel in TOOL_SOURCE_FILES:
        path = root / rel
        if not path.is_file():
            raise ManifestError(f"tool source file missing: {rel}")
        entries.append((rel, sha256_file(path)))
    return {"recipe": TOOL_SOURCE_RECIPE, "digest": _canonical_digest(TOOL_SOURCE_RECIPE, entries)}


# ------------------------------------------------------- schema validation


def _mapping(value: object, where: str) -> dict:
    if not isinstance(value, dict):
        raise ManifestError(f"{where}: expected an object, found {type(value).__name__}")
    return value


def _keys(
    value: dict, where: str, required: tuple[str, ...], optional: tuple[str, ...] = ()
) -> None:
    allowed = set(required) | set(optional)
    for key in value:
        if key not in allowed:
            raise ManifestError(f"{where}: unknown key {key!r}")
    for key in required:
        if key not in value:
            raise ManifestError(f"{where}.{key}: missing required key")


def _string(value: object, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{where}: expected a non-empty string, found {value!r}")
    return value


def _number(value: object, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ManifestError(f"{where}: expected a number, found {value!r}")
    return value


def _list(value: object, where: str) -> list:
    if not isinstance(value, list):
        raise ManifestError(f"{where}: expected a list, found {type(value).__name__}")
    return value


def _unique(names: list[str], where: str, what: str) -> None:
    seen = set()
    for name in names:
        if name in seen:
            raise ManifestError(f"{where}: duplicate {what} {name!r}")
        seen.add(name)


def validate(data: object) -> dict:
    """Validate a study-package manifest. Raises :class:`ManifestError` on anything unexpected.

    Every block is validated in full, including ``baseline`` and ``oracle``, which
    the indicator tool never reads — a malformed baseline is a failure at the first
    tool that opens the file, not a surprise for a later one.
    """
    root = _mapping(data, "manifest")
    _keys(
        root,
        "manifest",
        (
            "schema_version",
            "package",
            "fingerprints",
            "objective_catalog",
            "ties",
            "baseline",
            "oracle",
        ),
    )
    version = _string(root["schema_version"], "manifest.schema_version")
    if version != MANIFEST_SCHEMA_VERSION:
        raise ManifestError(
            f"manifest.schema_version: expected {MANIFEST_SCHEMA_VERSION!r}, found {version!r}"
        )

    package = _mapping(root["package"], "manifest.package")
    _keys(package, "manifest.package", ("name", "path"))
    _string(package["name"], "manifest.package.name")
    _string(package["path"], "manifest.package.path")

    _validate_fingerprints(root["fingerprints"])
    _validate_objective_catalog(root["objective_catalog"])
    _validate_ties(root["ties"])
    _validate_baseline(root["baseline"])
    _validate_oracle(root["oracle"])
    return root


def _validate_fingerprints(value: object) -> None:
    block = _mapping(value, "manifest.fingerprints")
    _keys(block, "manifest.fingerprints", ("indicator_inputs", "recorded_provenance"))

    pin = _mapping(block["indicator_inputs"], "manifest.fingerprints.indicator_inputs")
    where = "manifest.fingerprints.indicator_inputs"
    _keys(pin, where, ("recipe", "digest", "files"))
    recipe = _string(pin["recipe"], f"{where}.recipe")
    if recipe != INDICATOR_INPUT_RECIPE:
        raise ManifestError(
            f"{where}.recipe: expected {INDICATOR_INPUT_RECIPE!r}, found {recipe!r}"
        )
    _string(pin["digest"], f"{where}.digest")
    files = _list(pin["files"], f"{where}.files")
    if not files:
        raise ManifestError(f"{where}.files: must not be empty")
    for i, entry in enumerate(files):
        _string(entry, f"{where}.files[{i}]")
    _unique(files, f"{where}.files", "path")
    if list(files) != sorted(files):
        raise ManifestError(f"{where}.files: must be sorted by path")

    prov = _mapping(block["recorded_provenance"], "manifest.fingerprints.recorded_provenance")
    where = "manifest.fingerprints.recorded_provenance"
    _keys(prov, where, ("executable_fingerprint", "semantic_fingerprint"))
    _string(prov["executable_fingerprint"], f"{where}.executable_fingerprint")
    _string(prov["semantic_fingerprint"], f"{where}.semantic_fingerprint")


def _validate_objective_catalog(value: object) -> None:
    entries = _list(value, "manifest.objective_catalog")
    if not entries:
        raise ManifestError("manifest.objective_catalog: must not be empty")
    for i, entry in enumerate(entries):
        where = f"manifest.objective_catalog[{i}]"
        obj = _mapping(entry, where)
        _keys(obj, where, ("name", "channel"), ("note",))
        _string(obj["name"], f"{where}.name")
        _string(obj["channel"], f"{where}.channel")
        if "note" in obj:
            _string(obj["note"], f"{where}.note")
    _unique([e["name"] for e in entries], "manifest.objective_catalog", "objective name")
    _unique([e["channel"] for e in entries], "manifest.objective_catalog", "objective channel")


def _validate_ties(value: object) -> None:
    entries = _list(value, "manifest.ties")
    for i, entry in enumerate(entries):
        where = f"manifest.ties[{i}]"
        tie = _mapping(entry, where)
        _keys(tie, where, ("key", "rides_with"), ("note",))
        _string(tie["key"], f"{where}.key")
        partners = _list(tie["rides_with"], f"{where}.rides_with")
        if not partners:
            raise ManifestError(f"{where}.rides_with: must not be empty")
        for j, partner in enumerate(partners):
            _string(partner, f"{where}.rides_with[{j}]")
        _unique(partners, f"{where}.rides_with", "key")
        if tie["key"] in partners:
            raise ManifestError(f"{where}: key {tie['key']!r} also appears in its own rides_with")
        if "note" in tie:
            _string(tie["note"], f"{where}.note")
    _unique([t["key"] for t in entries], "manifest.ties", "tie key")


def _validate_baseline(value: object) -> None:
    block = _mapping(value, "manifest.baseline")
    _keys(block, "manifest.baseline", ("point", "headline", "verdicts"))

    point = _mapping(block["point"], "manifest.baseline.point")
    if not point:
        raise ManifestError("manifest.baseline.point: must not be empty")
    for key, val in point.items():
        _number(val, f"manifest.baseline.point[{key!r}]")

    headline = _mapping(block["headline"], "manifest.baseline.headline")
    _keys(headline, "manifest.baseline.headline", ("channel", "value"))
    _string(headline["channel"], "manifest.baseline.headline.channel")
    _number(headline["value"], "manifest.baseline.headline.value")

    verdicts = _list(block["verdicts"], "manifest.baseline.verdicts")
    if not verdicts:
        raise ManifestError("manifest.baseline.verdicts: must not be empty")
    for i, entry in enumerate(verdicts):
        where = f"manifest.baseline.verdicts[{i}]"
        verdict = _mapping(entry, where)
        _keys(verdict, where, ("source_local_identity", "expected"))
        _string(verdict["source_local_identity"], f"{where}.source_local_identity")
        expected = _string(verdict["expected"], f"{where}.expected")
        if expected not in ("satisfied", "violated"):
            raise ManifestError(
                f"{where}.expected: expected 'satisfied' or 'violated', found {expected!r}"
            )
    _unique(
        [v["source_local_identity"] for v in verdicts],
        "manifest.baseline.verdicts",
        "source_local_identity",
    )


def _validate_oracle(value: object) -> None:
    oracle = _mapping(value, "manifest.oracle")
    kind = _string(oracle.get("kind"), "manifest.oracle.kind")
    if kind != "python_callable":
        raise ManifestError(f"manifest.oracle.kind: unknown kind {kind!r}")
    _keys(oracle, "manifest.oracle", ("kind", "module", "callable", "sys_path"), ("note",))
    _string(oracle["module"], "manifest.oracle.module")
    _string(oracle["callable"], "manifest.oracle.callable")
    _string(oracle["sys_path"], "manifest.oracle.sys_path")
    if "note" in oracle:
        _string(oracle["note"], "manifest.oracle.note")


# ------------------------------------------------------------- loading


@dataclass(frozen=True)
class LoadedManifest:
    """A validated manifest plus the digest of the exact bytes it was read from."""

    path: Path
    data: dict
    digest: str

    @property
    def pinned_files(self) -> list[str]:
        return list(self.data["fingerprints"]["indicator_inputs"]["files"])

    @property
    def pinned_digest(self) -> str:
        return self.data["fingerprints"]["indicator_inputs"]["digest"]


def load(path: Path | str) -> LoadedManifest:
    """Read, digest, parse, and validate a manifest file."""
    path = Path(path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ManifestError(f"cannot read manifest {repo_relative_posix(path)}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManifestError(
            f"manifest {repo_relative_posix(path)} is not valid JSON: {exc}"
        ) from exc
    validate(data)
    return LoadedManifest(path=path, data=data, digest=hashlib.sha256(raw).hexdigest())


# ------------------------------------------------------------ live checks


def read_package_name(package_root: Path | str) -> str:
    """The live ``package_name`` from the package contract.

    That contract file is deliberately outside the digested set — the trace never
    reads it — so the identity check can only refuse a run, never let one pass over
    unreviewed artifacts.
    """
    return _read_contract_field(
        Path(package_root) / "contracts" / "package_contract.json", "package_name"
    )


def read_executable_fingerprint(package_root: Path | str) -> str:
    return _read_contract_field(
        Path(package_root) / "contracts" / "package_contract.json", "executable_fingerprint"
    )


def read_semantic_fingerprint(package_root: Path | str) -> str:
    return _read_contract_field(
        Path(package_root) / "contracts" / "model_contract.json", "semantic_fingerprint"
    )


def _read_contract_field(path: Path, field: str) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ManifestError(f"cannot read {repo_relative_posix(path)}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{repo_relative_posix(path)} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or field not in data:
        raise ManifestError(f"{repo_relative_posix(path)}: missing {field!r}")
    return _string(data[field], f"{repo_relative_posix(path)}.{field}")


def assert_package_identity(manifest: LoadedManifest, package_root: Path | str) -> None:
    """The manifest must be the one authored for this package."""
    declared = manifest.data["package"]["name"]
    live = read_package_name(package_root)
    if declared != live:
        raise ManifestError(
            f"wrong manifest for this package: manifest package.name is {declared!r} but "
            f"contracts/package_contract.json package_name is {live!r}"
        )


def assert_pin_matches(manifest: LoadedManifest, computed: dict) -> None:
    """The pre-parse gate: the manifest's pin must equal the live indicator-input fingerprint."""
    if computed["digest"] == manifest.pinned_digest:
        return
    pinned_files = set(manifest.pinned_files)
    live_files = {f["path"] for f in computed["files"]}
    detail = [
        f"indicator-input fingerprint mismatch: manifest pins {manifest.pinned_digest} "
        f"but {INDICATOR_INPUT_RECIPE} over the live package is {computed['digest']}"
    ]
    added = sorted(live_files - pinned_files)
    removed = sorted(pinned_files - live_files)
    if added:
        detail.append(f"  files present but not pinned: {', '.join(added)}")
    if removed:
        detail.append(f"  files pinned but absent: {', '.join(removed)}")
    detail.append("  live per-file digests:")
    detail += [f"    {f['path']} {f['sha256']}" for f in computed["files"]]
    detail.append("  re-pin with --print-fingerprint after reviewing the change")
    raise ManifestError("\n".join(detail))


def assert_read_set_covered(
    resolved_paths: list[Path], package_root: Path | str, manifest: LoadedManifest
) -> None:
    """Every path the reader opened must sit inside the package and inside the pin (M3).

    The reader resolves the inputs files from the pipeline's own EntryPoint refs, so a
    regenerated pipeline could point at a file the recipe never globbed — read by the
    trace, digested by nobody, pin still green. Both conditions fail closed.
    """
    root = Path(package_root).resolve()
    pinned = set(manifest.pinned_files)
    for path in resolved_paths:
        resolved = Path(path).resolve()
        if not resolved.is_relative_to(root):
            raise ManifestError(
                f"artifact resolves outside the package root: {resolved} "
                f"(package root {repo_relative_posix(root)})"
            )
        rel = package_relative_posix(resolved, root)
        if rel not in pinned:
            raise ManifestError(
                f"artifact read by the trace is not in the manifest's pinned file list: {rel}"
            )
