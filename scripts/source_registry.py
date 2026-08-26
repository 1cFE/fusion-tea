#!/usr/bin/env python3
"""The one write door into `knowledge/`.

Takes a URL or a local PDF plus the metadata the caller must supply, captures it
with `agentic-mbse extract` into a staging directory, and only then commits four
artifacts together: the source directory, the raw copy, one manifest row, one
index block. Nothing lands under `knowledge/` outside staging before that.

Callable by an operator, by another script, or by an agent's Bash tool:

    uv run python scripts/source_registry.py register \\
        --url https://example.org/paper \\
        --title "Paper Title" \\
        --use-for "..." --validation "..." --caveat "..."

Design: `.project/active/goal-research-seam/design.md` (D1–D14).
"""

import argparse
import fcntl
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from zotero_ingest import EXTRACT_OUTPUT, append_source_index_entry
from zotero_lib import RegistryPaths, default_paths, slugify, truncate_manifest

FRONTMATTER_HASH_RE = re.compile(r'^content_hash_sha256: "([0-9a-f]{64})"', re.MULTILINE)
CAPTURE_TIMEOUT_S = 900
DEFAULT_BUDGET = 0.0

# `--index`/`--summarize` invoke the `claude` CLI, which refuses to run inside a
# Claude Code session. The seam is agent-invoked by construction, so it never
# passes them (design, Implementation Notes).
EXTRACT_BASE_FLAGS = ("--save-source",)


class RegistrationError(RuntimeError):
    """A commit rung failed. The ladder has already undone everything above it."""


@dataclass(frozen=True)
class UrlSource:
    """A source identified by the URL it is fetched from."""

    url: str

    kind = "url"

    @property
    def identity(self) -> str:
        return self.url


@dataclass(frozen=True)
class LocalPdfSource:
    """A source identified by a PDF already on this machine."""

    path: Path

    kind = "local_pdf"

    @property
    def identity(self) -> str:
        return str(self.path)


@dataclass(frozen=True)
class SourceMetadata:
    """What the caller must say about a source before it may be registered.

    Drawn from the request and the triage record (spec R-B7). Registration never
    invents any of it.
    """

    title: str
    use_for: str
    validation: str
    caveat: str


@dataclass(frozen=True)
class RegistrationResult:
    """The lower-layer outcome of one registration attempt (design D13).

    These are *not* the seam's four return classes — `research_seam.py close`
    computes those from a run's receipts.
    """

    outcome: str
    reason: str = ""
    slug: str | None = None
    path: Path | None = None
    location: str | None = None
    source_id: str | None = None
    raw_sha256: str | None = None
    raw_artifact_sha256: str | None = None
    extract_sha256: str | None = None
    rule_id: str | None = None
    offsets: tuple[int, ...] = ()
    existing_slug: str | None = None
    existing_path: str | None = None


def register(
    source: UrlSource | LocalPdfSource,
    metadata: SourceMetadata,
    *,
    paths: RegistryPaths | None = None,
    budget: float = DEFAULT_BUDGET,
) -> RegistrationResult:
    """Capture, holdout-check and register one source. The only door into `knowledge/`.

    Returns a `RegistrationResult` for every refusal the seam expects — bad
    metadata, a holdout hit, a duplicate, a failed capture. Raises
    `RegistrationError` only when a commit rung failed after the ladder ran.
    """
    paths = paths or default_paths()
    _sweep_staging(paths)

    refusal = _precondition_refusal(source, metadata)
    if refusal is not None:
        return refusal

    staging = paths.staging / uuid.uuid4().hex
    staging.mkdir(parents=True)
    try:
        captured = _capture(source, staging, budget=budget)
        if isinstance(captured, RegistrationResult):
            return captured
        return _commit(source, metadata, captured, paths=paths)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


# --- steps 1-3: preconditions, capture, provenance ---------------------------


def _sweep_staging(paths: RegistryPaths) -> None:
    """Discard anything a previous run left behind. Unscanned content never persists."""
    if not paths.staging.exists():
        paths.staging.mkdir(parents=True)
        return
    for leftover in paths.staging.iterdir():
        shutil.rmtree(leftover, ignore_errors=True) if leftover.is_dir() else leftover.unlink()


def _precondition_refusal(
    source: UrlSource | LocalPdfSource, metadata: SourceMetadata
) -> RegistrationResult | None:
    """Everything checkable before a byte is fetched. None means proceed."""
    blank = [
        name for name in ("title", "use_for", "validation", "caveat")
        if not getattr(metadata, name).strip()
    ]
    if blank:
        return RegistrationResult(
            outcome="precondition_failed",
            reason=f"caller must supply non-empty {', '.join(blank)}",
        )
    if isinstance(source, LocalPdfSource) and not source.path.is_file():
        return RegistrationResult(
            outcome="precondition_failed", reason=f"local PDF not found: {source.path}"
        )
    return None


@dataclass(frozen=True)
class _Captured:
    """A staged extraction whose provenance has been read off disk."""

    staging: Path
    raw_artifact: Path
    extract: Path
    source_id: str
    raw_artifact_sha256: str
    extract_sha256: str


def _capture(
    source: UrlSource | LocalPdfSource, staging: Path, *, budget: float
) -> _Captured | RegistrationResult:
    """Run the real extractor into staging, flatten it, and read the provenance."""
    if isinstance(source, LocalPdfSource):
        staged_input = staging / ".rawin" / source.path.name
        staged_input.parent.mkdir(parents=True)
        shutil.copy2(source.path, staged_input)
        target = staged_input
    else:
        staged_input = None
        target = source.url

    completed = subprocess.run(
        ["uv", "run", "agentic-mbse", "extract", str(target),
         *EXTRACT_BASE_FLAGS, "--output", str(staging), "--budget", str(budget)],
        capture_output=True, text=True, timeout=CAPTURE_TIMEOUT_S,
    )
    if completed.returncode != 0:
        return RegistrationResult(
            outcome="capture_failed",
            reason=_last_error_line(completed.stderr) or f"extract exited {completed.returncode}",
        )

    _flatten(staging)
    extract = staging / EXTRACT_OUTPUT
    if not extract.is_file():
        return RegistrationResult(
            outcome="capture_failed", reason=f"extract produced no {EXTRACT_OUTPUT}"
        )

    raw_artifact = staged_input if staged_input is not None else staging / "raw.html"
    if not raw_artifact.is_file():
        return RegistrationResult(
            outcome="capture_failed", reason=f"no stored raw artifact at {raw_artifact.name}"
        )

    match = FRONTMATTER_HASH_RE.search(extract.read_text())
    if match is None:
        return RegistrationResult(
            outcome="capture_failed",
            reason=f"{EXTRACT_OUTPUT} carries no content_hash_sha256 frontmatter field",
        )

    return _Captured(
        staging=staging,
        raw_artifact=raw_artifact,
        extract=extract,
        source_id=match.group(1),
        raw_artifact_sha256=_sha256(raw_artifact),
        extract_sha256=_sha256(extract),
    )


def _flatten(staging: Path) -> None:
    """Lift a nested `<stem>/` extraction directory up into staging.

    The PDF backend nests; the web backend does not. Same shape as
    `zotero_ingest._flatten_extraction_output`, against the staging dir.
    """
    nested = [
        d for d in staging.iterdir()
        if d.is_dir() and d.name != ".rawin" and (d / EXTRACT_OUTPUT).exists()
    ]
    if len(nested) != 1:
        return
    for item in nested[0].iterdir():
        item.rename(staging / item.name)
    nested[0].rmdir()


def _last_error_line(stderr: str) -> str:
    lines = [line.strip() for line in (stderr or "").strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- step 6: commit, and the ladder that undoes it ---------------------------


def _commit(
    source: UrlSource | LocalPdfSource,
    metadata: SourceMetadata,
    captured: _Captured,
    *,
    paths: RegistryPaths,
) -> RegistrationResult:
    """Move four artifacts into place under the registry lock, or undo cleanly.

    Order is chosen so the riskiest write — the index read-modify-write — is last,
    and its failure only has to undo cheap, exactly-known things.
    """
    with _registry_lock(paths):
        slug = _resolve_slug(slugify(metadata.title), paths.sources)
        source_dir = paths.sources / slug
        raw_copy = _raw_copy_destination(source, paths)
        manifest_mark = paths.manifest.stat().st_size if paths.manifest.exists() else 0

        _rename_into_sources(captured.staging, source_dir)
        try:
            staged_raw = _move_raw_copy(source_dir, raw_copy)
            row = _manifest_row(source, metadata, captured, slug=slug, raw_copy=staged_raw)
            _append_manifest_row(row, paths)
            try:
                _insert_index_block(source, metadata, captured, slug=slug, paths=paths)
            except Exception:
                truncate_manifest(manifest_mark, paths)
                raise
        except Exception as error:
            _undo_raw_copy(raw_copy)
            shutil.rmtree(source_dir, ignore_errors=True)
            raise RegistrationError(f"commit failed for {source.identity}: {error}") from error

    return RegistrationResult(
        outcome="registered",
        slug=slug,
        path=source_dir,
        location=f"knowledge/sources/{slug}/",
        source_id=captured.source_id,
        raw_sha256=captured.source_id,
        raw_artifact_sha256=row["raw_artifact_sha256"],
        extract_sha256=captured.extract_sha256,
    )


@contextmanager
def _registry_lock(paths: RegistryPaths):
    """Serialize commits so two runs cannot interleave the index read-modify-write."""
    paths.lock.parent.mkdir(parents=True, exist_ok=True)
    with open(paths.lock, "w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _resolve_slug(slug: str, sources_dir: Path) -> str:
    """Numeric suffix on collision (design D10). Seam slugs carry no Zotero key."""
    if not (sources_dir / slug).exists():
        return slug
    n = 2
    while (sources_dir / f"{slug}_{n}").exists():
        n += 1
    return f"{slug}_{n}"


def _raw_copy_destination(
    source: UrlSource | LocalPdfSource, paths: RegistryPaths
) -> Path | None:
    """Where the staged raw input belongs, for the one kind that stages one."""
    if isinstance(source, LocalPdfSource):
        return paths.raw / source.path.name
    return None


def _rename_into_sources(staging: Path, source_dir: Path) -> None:
    """Rung (a): one atomic syscall, same filesystem."""
    source_dir.parent.mkdir(parents=True, exist_ok=True)
    staging.rename(source_dir)


def _move_raw_copy(source_dir: Path, raw_copy: Path | None) -> Path | None:
    """Rung (b): lift the staged input out of the source directory into `knowledge/raw/`."""
    if raw_copy is None:
        return None
    staged = source_dir / ".rawin" / raw_copy.name
    raw_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staged), str(raw_copy))
    shutil.rmtree(source_dir / ".rawin", ignore_errors=True)
    return raw_copy


def _undo_raw_copy(raw_copy: Path | None) -> None:
    if raw_copy is not None:
        raw_copy.unlink(missing_ok=True)


def _manifest_row(
    source: UrlSource | LocalPdfSource,
    metadata: SourceMetadata,
    captured: _Captured,
    *,
    slug: str,
    raw_copy: Path | None,
) -> dict:
    row = {
        "source_id": captured.source_id,
        "source_kind": source.kind,
        "slug": slug,
        "title": metadata.title,
    }
    if isinstance(source, UrlSource):
        row["source_url"] = source.url
    else:
        row["origin_path"] = str(source.path)
    row["raw_sha256"] = captured.source_id
    row["raw_artifact_sha256"] = _sha256(raw_copy) if raw_copy else captured.raw_artifact_sha256
    row["extract_sha256"] = captured.extract_sha256
    row["date_extracted"] = date.today().isoformat()
    return row


def _append_manifest_row(row: dict, paths: RegistryPaths) -> None:
    """Rung (c): one JSON line, flushed."""
    with open(paths.manifest, "a") as handle:
        handle.write(json.dumps(row) + "\n")
        handle.flush()


def _insert_index_block(
    source: UrlSource | LocalPdfSource,
    metadata: SourceMetadata,
    captured: _Captured,
    *,
    slug: str,
    paths: RegistryPaths,
) -> None:
    """Rung (d): the index read-modify-write, last because it is the riskiest."""
    append_source_index_entry(
        profile="seam",
        title=metadata.title,
        slug=slug,
        source_kind=source.kind,
        source_url=source.url if isinstance(source, UrlSource) else None,
        origin_path=str(source.path) if isinstance(source, LocalPdfSource) else None,
        use_for=metadata.use_for,
        validation=metadata.validation,
        caveat=metadata.caveat,
        source_id=captured.source_id,
        raw_sha256=captured.source_id,
        raw_artifact_sha256=captured.raw_artifact_sha256,
        extract_sha256=captured.extract_sha256,
    )


# --- CLI ---------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    reg = sub.add_parser("register", help="Register one URL or local PDF")
    origin = reg.add_mutually_exclusive_group(required=True)
    origin.add_argument("--url", help="URL to fetch and register")
    origin.add_argument("--local-pdf", type=Path, help="Local PDF to register")
    reg.add_argument("--title", required=True, help="Title for the index block and slug")
    reg.add_argument("--use-for", required=True,
                     help="What this source establishes, and which RQ it serves")
    reg.add_argument("--validation", required=True, help="How a reader checks its numbers")
    reg.add_argument("--caveat", required=True, help="What limits its authority")
    reg.add_argument("--budget", type=float, default=DEFAULT_BUDGET,
                     help=f"Claude budget in USD for extraction (default {DEFAULT_BUDGET})")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    source = UrlSource(url=args.url) if args.url else LocalPdfSource(path=args.local_pdf)
    result = register(
        source,
        SourceMetadata(
            title=args.title, use_for=args.use_for,
            validation=args.validation, caveat=args.caveat,
        ),
        budget=args.budget,
    )
    print(json.dumps(_result_as_json(result), indent=2))
    return 0 if result.outcome == "registered" else 1


def _result_as_json(result: RegistrationResult) -> dict:
    payload = {"outcome": result.outcome}
    for field in ("reason", "slug", "location", "source_id", "raw_sha256",
                  "raw_artifact_sha256", "extract_sha256", "rule_id",
                  "existing_slug", "existing_path"):
        value = getattr(result, field)
        if value:
            payload[field] = value
    if result.offsets:
        payload["offsets"] = list(result.offsets)
    return payload


if __name__ == "__main__":
    sys.exit(main())
