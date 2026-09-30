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

It is also the one removal door. `retire` takes a registered slug and a reason,
removes that entry's four artifacts together under the same lock, and leaves one
durable line in `knowledge/RETIRED.jsonl`; `verify` then treats the slug as
expected-absent and reports it if it ever reappears:

    uv run python scripts/source_registry.py retire --slug <slug> --reason "..."

Design: `.project/active/goal-research-seam/design.md` (D1–D14); retirement was
added under goal magnet-material-comparison Round 2 (brief T-010, R1–R5).
"""

import argparse
import fcntl
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import holdout_guard
from zotero_ingest import EXTRACT_OUTPUT, append_source_index_entry
from zotero_lib import (
    RegistryPaths,
    default_paths,
    load_manifest_rows,
    slugify,
    truncate_manifest,
)

FRONTMATTER_HASH_RE = re.compile(r'^content_hash_sha256: "([0-9a-f]{64})"', re.MULTILINE)
CAPTURE_TIMEOUT_S = 900
DEFAULT_BUDGET = 0.0

# A staging directory older than this cannot belong to a live attempt: capture is
# hard-bounded by CAPTURE_TIMEOUT_S and commit is a few syscalls under the lock.
# Four times the bound is the conservative margin (design D7, amended 2026-08-26).
STALE_STAGING_AGE_S = 4 * CAPTURE_TIMEOUT_S

# `--index`/`--summarize` invoke the `claude` CLI, which refuses to run inside a
# Claude Code session. The seam is agent-invoked by construction, so it never
# passes them (design, Implementation Notes).
EXTRACT_BASE_FLAGS = ("--save-source",)


class RegistrationError(RuntimeError):
    """A commit rung failed. The ladder has already undone everything above it."""


@dataclass(frozen=True)
class UrlSource:
    """A source fetched from a URL."""

    url: str

    kind = "url"
    index_profile = "seam"
    slug_suffix = None

    @property
    def identity(self) -> str:
        return self.url

    @property
    def capture_target(self) -> str:
        return self.url

    @property
    def staged_input(self) -> Path | None:
        return None

    @property
    def row_extras(self) -> dict:
        return {"source_url": self.url}


@dataclass(frozen=True)
class LocalPdfSource:
    """A PDF already on this machine, handed in by an operator."""

    path: Path

    kind = "local_pdf"
    index_profile = "seam"
    slug_suffix = None

    @property
    def identity(self) -> str:
        return str(self.path)

    @property
    def capture_target(self) -> Path:
        return self.path

    @property
    def staged_input(self) -> Path:
        return self.path

    @property
    def row_extras(self) -> dict:
        return {"origin_path": str(self.path)}


@dataclass(frozen=True)
class ZoteroSource:
    """A PDF downloaded from the Zotero group library by the batch ingest.

    Registers through the same door as everything else, but keeps the batch
    index-block profile: an unattended run over a large queue has no per-item
    prose to supply, and inventing it would be a fallback (design D6).
    """

    path: Path
    item_key: str

    kind = "zotero"
    index_profile = "zotero-batch"

    @property
    def slug_suffix(self) -> str:
        return self.item_key

    @property
    def identity(self) -> str:
        return f"zotero:{self.item_key}"

    @property
    def capture_target(self) -> Path:
        return self.path

    @property
    def staged_input(self) -> Path:
        return self.path

    @property
    def row_extras(self) -> dict:
        return {"zotero_key": self.item_key}


Source = UrlSource | LocalPdfSource | ZoteroSource


@dataclass(frozen=True)
class SourceMetadata:
    """What the caller must say about a source before it may be registered.

    Drawn from the request and the triage record (spec R-B7). Registration never
    invents any of it.

    The three prose fields are required for a seam-profile source and left empty
    by the unattended Zotero batch, which has no per-item prose to supply (D6).
    """

    title: str
    use_for: str = ""
    validation: str = ""
    caveat: str = ""


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
    source: Source,
    metadata: SourceMetadata,
    *,
    paths: RegistryPaths | None = None,
    budget: float = DEFAULT_BUDGET,
    run_dir: Path | None = None,
    triage: str = "keeper",
) -> RegistrationResult:
    """Capture, holdout-check and register one source. The only door into `knowledge/`.

    Returns a `RegistrationResult` for every refusal the seam expects — bad
    metadata, a holdout hit, a duplicate, a failed capture. Raises
    `RegistrationError` only when a commit rung failed after the ladder ran.

    `run_dir` is what a research invocation passes so the attempt is receipted
    and counted against the run's `max_captures` (design D8). A standalone
    operator call passes none and is unaffected.
    """
    paths = paths or default_paths()
    result = _attempt(source, metadata, paths=paths, budget=budget, run_dir=run_dir)
    if run_dir is not None:
        _write_receipt(run_dir, source, result, triage=triage)
    return result


def _attempt(
    source: Source,
    metadata: SourceMetadata,
    *,
    paths: RegistryPaths,
    budget: float,
    run_dir: Path | None,
) -> RegistrationResult:
    """The seven-step flow, without the receipt bookkeeping wrapped around it."""
    _sweep_stale_staging(paths)

    refusal = _pre_capture_refusal(source, metadata, paths=paths, run_dir=run_dir)
    if refusal is not None:
        return refusal

    staging = paths.staging / uuid.uuid4().hex
    staging.mkdir(parents=True)
    try:
        captured = _capture(source, staging, budget=budget)
        if isinstance(captured, RegistrationResult):
            return captured

        refusal = _post_capture_refusal(captured, paths=paths)
        if refusal is not None:
            return refusal

        return _commit(source, metadata, captured, paths=paths)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


# --- steps 1-3: preconditions, capture, provenance ---------------------------


def _sweep_stale_staging(paths: RegistryPaths) -> None:
    """Discard staging left behind by a killed run — and nothing else.

    Each attempt works in its own `knowledge/.staging/<uuid>/` and removes it in a
    `finally`, so the only thing this has to collect is what a hard kill orphaned.
    It takes the registry lock and removes only entries older than
    `STALE_STAGING_AGE_S`, because the alternative — clearing the whole staging
    root — deletes the working directory of every other attempt in flight.

    The threshold is safe by construction: capture is hard-bounded by the
    subprocess timeout (`CAPTURE_TIMEOUT_S`), and commit is a handful of
    filesystem calls under the lock, so no live attempt can reach four times that
    age. See design.md D7, amendment 2026-08-26.
    """
    paths.staging.mkdir(parents=True, exist_ok=True)
    cutoff = time.time() - STALE_STAGING_AGE_S
    with _registry_lock(paths):
        for leftover in paths.staging.iterdir():
            if _modified_at(leftover) > cutoff:
                continue
            if leftover.is_dir():
                shutil.rmtree(leftover, ignore_errors=True)
            else:
                leftover.unlink(missing_ok=True)


def _modified_at(path: Path) -> float:
    """The entry's own mtime, or now if it vanished under us — never sweep a racer."""
    try:
        return path.stat().st_mtime
    except OSError:
        return time.time()


def _pre_capture_refusal(
    source: Source,
    metadata: SourceMetadata,
    *,
    paths: RegistryPaths,
    run_dir: Path | None,
) -> RegistrationResult | None:
    """Step 1 — everything checkable before a byte is fetched. None means proceed.

    Ordered so the cheapest refusals come first and nothing is downloaded that a
    later check would have thrown away.
    """
    required = ("title", "use_for", "validation", "caveat") \
        if source.index_profile == "seam" else ("title",)
    blank = [name for name in required if not getattr(metadata, name).strip()]
    if blank:
        return RegistrationResult(
            outcome="precondition_failed",
            reason=f"caller must supply non-empty {', '.join(blank)}",
        )
    staged = source.staged_input
    if staged is not None and not staged.is_file():
        return RegistrationResult(
            outcome="precondition_failed", reason=f"input file not found: {staged}"
        )

    hit = _input_identity_holdout_hit(source, metadata)
    if hit is not None:
        return hit

    existing = _row_matching_input_identity(source, paths)
    if existing is not None:
        return _duplicate_of(existing, reason=f"already registered as {existing['slug']}")

    return _limit_refusal(run_dir)


def _input_identity_holdout_hit(
    source: Source, metadata: SourceMetadata
) -> RegistrationResult | None:
    """Bar the *input identity* — the path or URL handed in, and the caller's title.

    The destination slug is newly minted and could never match, so it is not checked.
    """
    staged = source.staged_input
    if staged is not None:
        path_match = holdout_guard.check_input_path(staged)
        if path_match is not None:
            return _holdout_refusal(path_match)
    for text in (source.identity, metadata.title):
        matches = holdout_guard.scan_terms(text)
        if matches:
            return _holdout_refusal(matches[0])
    return None


def _limit_refusal(run_dir: Path | None) -> RegistrationResult | None:
    """Refuse when this run has spent its `max_captures` (design D8)."""
    if run_dir is None:
        return None
    limit = _run_limits(run_dir).get("max_captures")
    if limit is None:
        return None
    spent = sum(1 for receipt in _read_receipts(run_dir) if receipt.get("captured"))
    if spent < limit:
        return None
    return RegistrationResult(
        outcome="limit_reached",
        reason=f"run has spent its max_captures limit of {limit}",
    )


def _post_capture_refusal(
    captured: "_Captured", *, paths: RegistryPaths
) -> RegistrationResult | None:
    """Steps 4-5 — the content holdout scan, then dedupe on the bytes as fetched."""
    for artifact in (captured.extract, captured.raw_artifact):
        matches = holdout_guard.scan_file(artifact)
        if matches:
            return _holdout_refusal(matches[0])

    existing = _row_matching_source_id(captured.source_id, paths)
    if existing is not None:
        return _duplicate_of(
            existing, reason=f"same bytes already registered (source_id {captured.source_id})"
        )
    return None


def _holdout_refusal(match: holdout_guard.Match) -> RegistrationResult:
    """Record the rule that fired and where — never the content that fired it (R-D4)."""
    return RegistrationResult(
        outcome="holdout_hit",
        reason=f"{match.rule_id} matched {match.count}x",
        rule_id=match.rule_id,
        offsets=match.offsets,
    )


def _duplicate_of(row: dict, *, reason: str) -> RegistrationResult:
    return RegistrationResult(
        outcome="duplicate",
        reason=reason,
        source_id=row.get("source_id"),
        existing_slug=row["slug"],
        existing_path=f"knowledge/sources/{row['slug']}/",
    )


def _row_matching_input_identity(source: Source, paths: RegistryPaths) -> dict | None:
    """Dedupe before the fetch, on whatever identity the input already carries.

    A Zotero key is exact; a URL also matches scheme/host-lowercased and
    fragment-stripped (design D2). A bare local PDF carries neither, so it is
    caught after capture by its `source_id` instead.
    """
    if isinstance(source, ZoteroSource):
        return _first_row(paths, lambda row: row.get("zotero_key") == source.item_key)
    if isinstance(source, UrlSource):
        normalized = _normalize_url(source.url)
        return _first_row(
            paths,
            lambda row: bool(row.get("source_url"))
            and (row["source_url"] == source.url
                 or _normalize_url(row["source_url"]) == normalized),
        )
    return None


def _first_row(paths: RegistryPaths, matches) -> dict | None:
    for row in load_manifest_rows(paths):
        if matches(row):
            return row
    return None


def _row_matching_source_id(source_id: str, paths: RegistryPaths) -> dict | None:
    return _first_row(paths, lambda row: row.get("source_id") == source_id)


def _normalize_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((
        parts.scheme.lower(), parts.netloc.lower(),
        posixpath.normpath(parts.path) if parts.path else parts.path,
        parts.query, "",
    ))


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
    source: Source, staging: Path, *, budget: float
) -> _Captured | RegistrationResult:
    """Run the real extractor into staging, flatten it, and read the provenance."""
    original = source.staged_input
    if original is not None:
        staged_input = staging / ".rawin" / original.name
        staged_input.parent.mkdir(parents=True)
        shutil.copy2(original, staged_input)
        target = staged_input
    else:
        staged_input = None
        target = source.capture_target

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

    if staged_input is not None:
        raw_artifact = staged_input
    else:
        # The web backend stores the fetched page as raw.html; for a PDF URL the
        # extractor downloads the document and saves it as raw.pdf instead
        # (extract_cli --save-source). Accept whichever one this capture stored
        # (WI-033: the raw.html-only check failed every PDF-URL registration).
        stored = [p for p in (staging / "raw.html", staging / "raw.pdf") if p.is_file()]
        raw_artifact = stored[0] if stored else None
    if raw_artifact is None or not raw_artifact.is_file():
        return RegistrationResult(
            outcome="capture_failed",
            reason="no stored raw artifact at raw.html or raw.pdf",
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
    source: Source,
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
        slug = _resolve_slug(slugify(metadata.title), paths.sources, source.slug_suffix)
        source_dir = paths.sources / slug
        raw_copy = _raw_copy_destination(source, paths)
        manifest_mark = paths.manifest.stat().st_size if paths.manifest.exists() else 0

        try:
            _rename_into_sources(captured.staging, source_dir)
            staged_raw = _move_raw_copy(source_dir, raw_copy)
            # Digested once, here, and handed to both writers. Deriving it twice
            # gave the manifest and the index two routes to one number that had to
            # stay in step, with nothing checking they did (audit F7).
            raw_artifact_sha256 = (
                _sha256(staged_raw) if staged_raw else captured.raw_artifact_sha256
            )
            row = _manifest_row(source, metadata, captured, slug=slug,
                                raw_artifact_sha256=raw_artifact_sha256)
            _append_manifest_row(row, paths)
            _insert_index_block(source, metadata, captured, slug=slug, paths=paths,
                                raw_artifact_sha256=raw_artifact_sha256)
        except Exception as error:
            _roll_back(source_dir, raw_copy, manifest_mark, paths)
            raise RegistrationError(f"commit failed for {source.identity}: {error}") from error

    return RegistrationResult(
        outcome="registered",
        slug=slug,
        path=source_dir,
        location=f"knowledge/sources/{slug}/",
        source_id=captured.source_id,
        raw_sha256=captured.source_id,
        raw_artifact_sha256=raw_artifact_sha256,
        extract_sha256=captured.extract_sha256,
    )


def _roll_back(
    source_dir: Path, raw_copy: Path | None, manifest_mark: int, paths: RegistryPaths
) -> None:
    """Undo the commit rungs in reverse. Each step is a no-op if its rung never ran.

    The slug was resolved against a non-existent directory under the lock, so
    removing `source_dir` can only ever remove what this attempt created.
    """
    truncate_manifest(manifest_mark, paths)
    if raw_copy is not None:
        raw_copy.unlink(missing_ok=True)
    shutil.rmtree(source_dir, ignore_errors=True)


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


def _resolve_slug(slug: str, sources_dir: Path, suffix: str | None) -> str:
    """Disambiguate a slug collision (design D10).

    A Zotero source disambiguates with its item key, as it always has; anything
    else takes a numeric suffix.
    """
    if not (sources_dir / slug).exists():
        return slug
    if suffix is not None:
        return f"{slug}_{suffix}"
    n = 2
    while (sources_dir / f"{slug}_{n}").exists():
        n += 1
    return f"{slug}_{n}"


def _raw_copy_destination(source: Source, paths: RegistryPaths) -> Path | None:
    """Where the staged raw input belongs, for the kinds that stage one."""
    staged = source.staged_input
    return paths.raw / staged.name if staged is not None else None


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


def _manifest_row(
    source: Source,
    metadata: SourceMetadata,
    captured: _Captured,
    *,
    slug: str,
    raw_artifact_sha256: str,
) -> dict:
    row = {
        "source_id": captured.source_id,
        "source_kind": source.kind,
        "slug": slug,
        "title": metadata.title,
    }
    row.update(source.row_extras)
    row["raw_sha256"] = captured.source_id
    row["raw_artifact_sha256"] = raw_artifact_sha256
    row["extract_sha256"] = captured.extract_sha256
    row["date_extracted"] = date.today().isoformat()
    return row


def _append_manifest_row(row: dict, paths: RegistryPaths) -> None:
    """Rung (c): one JSON line, flushed."""
    with open(paths.manifest, "a") as handle:
        handle.write(json.dumps(row) + "\n")
        handle.flush()


def _insert_index_block(
    source: Source,
    metadata: SourceMetadata,
    captured: _Captured,
    *,
    slug: str,
    paths: RegistryPaths,
    raw_artifact_sha256: str,
) -> None:
    """Rung (d): the index read-modify-write, last because it is the riskiest."""
    extras = source.row_extras
    append_source_index_entry(
        profile=source.index_profile,
        title=metadata.title,
        slug=slug,
        source_kind=source.kind,
        source_url=extras.get("source_url"),
        origin_path=extras.get("origin_path"),
        item_key=extras.get("zotero_key"),
        pdf_sha256=captured.source_id,
        use_for=metadata.use_for,
        validation=metadata.validation,
        caveat=metadata.caveat,
        source_id=captured.source_id,
        raw_sha256=captured.source_id,
        raw_artifact_sha256=raw_artifact_sha256,
        extract_sha256=captured.extract_sha256,
    )


# --- verify: report drift, repair nothing (design D14) ------------------------


@dataclass(frozen=True)
class Finding:
    """One thing `verify` noticed. `klass` says whether it is this seam's problem."""

    kind: str
    klass: str
    path: str
    detail: str


@dataclass(frozen=True)
class VerifyReport:
    findings: list[Finding]

    @property
    def has_faults(self) -> bool:
        return any(f.klass == "fault" for f in self.findings)


def verify(paths: RegistryPaths | None = None) -> VerifyReport:
    """Check that every source directory has one row and one block, and vice versa.

    Reports the two windows a hard kill inside the commit lock can leave, plus
    pre-existing drift. Entries listed in the checked-in baseline are reported as
    `legacy` so the first run does not read as a broken tool. Writes nothing.

    A slug recorded in `knowledge/RETIRED.jsonl` is expected absent: its absence is
    no finding, and any of its artifacts reappearing — a row, a block whose
    Location names it, or its source directory — is a `retired_reappeared` fault.
    Prose elsewhere in the index that mentions a retired path (a superseding
    entry's caveat, say) is history, not reappearance.
    """
    paths = paths or default_paths()
    baseline = _load_baseline(paths)
    rows = load_manifest_rows(paths)
    index_text = paths.index.read_text() if paths.index.exists() else ""
    retired = set(_load_retired(paths))

    findings: list[Finding] = []
    slugs_with_rows = {row["slug"] for row in rows if "slug" in row}

    def reappeared(slug: str, what: str) -> Finding:
        return Finding(
            kind="retired_reappeared",
            klass="fault",
            path=f"knowledge/sources/{slug}",
            detail=f"{what} for a slug retired in knowledge/RETIRED.jsonl",
        )

    for entry in sorted(paths.sources.iterdir()) if paths.sources.exists() else []:
        location = f"knowledge/sources/{entry.name}"
        if not entry.is_dir():
            findings.append(Finding(
                kind="loose_file",
                klass=_klass(location, baseline["loose_files"]),
                path=location,
                detail="not a source directory",
            ))
        elif entry.name in retired:
            findings.append(reappeared(entry.name, "source directory"))
        elif entry.name not in slugs_with_rows:
            findings.append(Finding(
                kind="orphan_source_dir",
                klass=_klass(location, baseline["orphan_source_dirs"]),
                path=location,
                detail="source directory with no manifest row",
            ))

    for block in _index_blocks(index_text):
        if block.slug in retired:
            findings.append(reappeared(block.slug, "SOURCE_INDEX.md block"))

    for row in rows:
        slug = row.get("slug")
        if slug is None:
            continue
        location = f"knowledge/sources/{slug}"
        if slug in retired:
            findings.append(reappeared(slug, "manifest row"))
        elif not (paths.sources / slug).is_dir():
            findings.append(Finding(
                kind="unresolvable_path",
                klass=_klass(location, baseline["orphan_source_dirs"]),
                path=location,
                detail="manifest row whose source directory does not exist",
            ))
        elif f"knowledge/sources/{slug}/" not in index_text:
            findings.append(Finding(
                kind="row_without_block",
                klass=_klass(location, baseline["orphan_source_dirs"]),
                path=location,
                detail="manifest row with no SOURCE_INDEX.md block",
            ))

    return VerifyReport(findings=findings)


def _load_baseline(paths: RegistryPaths) -> dict:
    """The checked-in list of pre-seam drift. An absent baseline means none is expected."""
    if not paths.baseline.exists():
        return {"orphan_source_dirs": [], "loose_files": []}
    recorded = json.loads(paths.baseline.read_text())
    return {
        "orphan_source_dirs": [p.rstrip("/") for p in recorded.get("orphan_source_dirs", [])],
        "loose_files": [p.rstrip("/") for p in recorded.get("loose_files", [])],
    }


def _klass(location: str, baseline_entries: list[str]) -> str:
    return "legacy" if location in baseline_entries else "fault"


def _load_retired(paths: RegistryPaths) -> dict[str, dict]:
    """Every RETIRED.jsonl line, keyed by slug. An absent file means nothing retired."""
    if not paths.retired.exists():
        return {}
    lines = [json.loads(line) for line in paths.retired.read_text().splitlines() if line.strip()]
    return {line["slug"]: line for line in lines}


# --- retire: the one removal door, with its own ladder (T-010 brief, R1–R5) -------

#: A registry slug as `slugify` mints it (plus Zotero's `_<ITEMKEY>` suffix): one
#: path segment, nothing that could name a directory elsewhere.
SLUG_RE = re.compile(r"[A-Za-z0-9_]+")

#: Where the registry lives as the hold-out protocol's globs spell it. The guard is
#: run on this canonical path, not on the injected tree, so a barred slug refuses
#: whichever tree the caller points at.
CANONICAL_SOURCES = Path("knowledge/sources")

INDEX_HEADING_RE = re.compile(r"^(?:### |## |# )", re.MULTILINE)
INDEX_LOCATION_RE = re.compile(r"^- \*\*Location\*\*: knowledge/sources/([^/\s]+)/", re.MULTILINE)


class RetirementError(RuntimeError):
    """A removal rung failed. The ladder has already put everything back."""


@dataclass(frozen=True)
class IndexBlock:
    """One `### ` block of SOURCE_INDEX.md: its span in the file and the slug it locates."""

    start: int
    end: int
    text: str
    slug: str | None


@dataclass(frozen=True)
class RetirementResult:
    """The outcome of one retirement attempt.

    `retired` is the only outcome that wrote anything. Every refusal — unknown
    slug, hold-out hit, a reference from another entry, a precondition — returns
    with nothing written. `RetirementError` is raised only when a removal rung
    failed after the ladder ran, and then the ladder has already rolled back.
    """

    outcome: str
    reason: str = ""
    slug: str | None = None
    removed: dict = field(default_factory=dict)
    retired_line: dict | None = None
    rule_id: str | None = None
    offsets: tuple[int, ...] = ()
    references: tuple[str, ...] = ()


def retire(
    slug: str, reason: str, *, paths: RegistryPaths | None = None
) -> RetirementResult:
    """Remove one registered entry — row, block, directory, raw copy — or nothing.

    Refuses (R3), with nothing written, when the reason is blank, when the slug
    trips the hold-out guard, when it is not a registry slug, when no manifest
    row carries it, when its block or directory cannot be identified (that is
    drift: run `verify`), or when another entry depends on it.

    On a reference from another entry: a `supersedes` claim *about* the retiree
    ("Supersedes ... knowledge/sources/<slug>/") is the announcement that the
    retiree was replaced, and retiring it completes that announcement, so such a
    claim does not block. Any other mention of the slug by another entry does.

    Leaves one line in RETIRED.jsonl (R2): the removed row verbatim under `row`,
    `retired_at`, `reason`, and the SHA-256 of the removed block text as the
    writer wrote it (heading through last metadata line, no trailing newline).
    """
    paths = paths or default_paths()
    with _registry_lock(paths):
        refusal = _retire_refusal(slug, reason, paths)
        if refusal is not None:
            return refusal
        return _remove(slug, reason, paths)


def _retire_refusal(slug: str, reason: str, paths: RegistryPaths) -> RetirementResult | None:
    """Everything checkable before a byte moves. None means proceed. Cheapest first."""
    if not reason.strip():
        return RetirementResult(
            outcome="precondition_failed", reason="caller must supply a non-empty reason",
        )

    for candidate in (Path(slug), CANONICAL_SOURCES / slug):
        match = holdout_guard.check_input_path(candidate)
        if match is not None:
            return _holdout_retirement_refusal(match)
    matches = holdout_guard.scan_terms(slug)
    if matches:
        return _holdout_retirement_refusal(matches[0])

    if not SLUG_RE.fullmatch(slug):
        return RetirementResult(
            outcome="precondition_failed", reason=f"not a registry slug: {slug!r}",
        )

    rows = [row for row in load_manifest_rows(paths) if row.get("slug") == slug]
    if not rows:
        return RetirementResult(outcome="unknown_slug", reason=f"no manifest row carries slug {slug}")
    if len(rows) > 1:
        return RetirementResult(
            outcome="precondition_failed",
            reason=f"{len(rows)} manifest rows carry slug {slug}; run verify and resolve the drift first",
        )

    index_text = paths.index.read_text() if paths.index.exists() else ""
    blocks = [block for block in _index_blocks(index_text) if block.slug == slug]
    if len(blocks) != 1:
        return RetirementResult(
            outcome="precondition_failed",
            reason=f"{len(blocks)} SOURCE_INDEX.md blocks locate {slug}; expected exactly one — "
                   "run verify and resolve the drift first",
        )
    if not (paths.sources / slug).is_dir():
        return RetirementResult(
            outcome="precondition_failed",
            reason=f"source directory knowledge/sources/{slug}/ does not exist; run verify",
        )

    references = _references_to(slug, paths, index_text)
    if references:
        return RetirementResult(
            outcome="referenced",
            reason="another registry entry references this slug: " + "; ".join(references),
            slug=slug,
            references=tuple(references),
        )
    return None


def _holdout_retirement_refusal(match: holdout_guard.Match) -> RetirementResult:
    """The rule that fired and where — never the content that fired it (R-D4, D12)."""
    return RetirementResult(
        outcome="holdout_hit",
        reason=f"{match.rule_id} matched {match.count}x",
        rule_id=match.rule_id,
        offsets=match.offsets,
    )


def _index_blocks(index_text: str) -> list[IndexBlock]:
    """Every `### ` block: from its heading to the next heading of any level.

    A block's span includes the blank lines that separate it from what follows,
    so removing the span leaves the file as it was before the block was inserted.
    Its `text` is what the writer wrote — heading through last metadata line.
    """
    headings = [m.start() for m in INDEX_HEADING_RE.finditer(index_text)]
    blocks = []
    for i, start in enumerate(headings):
        if not index_text.startswith("### ", start):
            continue
        end = headings[i + 1] if i + 1 < len(headings) else len(index_text)
        span = index_text[start:end]
        located = INDEX_LOCATION_RE.search(span)
        blocks.append(IndexBlock(
            start=start, end=end, text=span.rstrip("\n"),
            slug=located.group(1) if located else None,
        ))
    return blocks


def _references_to(slug: str, paths: RegistryPaths, index_text: str) -> list[str]:
    """Other entries that depend on `slug`, as `<where> (<their slug>)` labels.

    A mention on a line that says the other entry *supersedes* the retiree is a
    supersession claim about it, not a dependency on it, and is left out.
    """
    mention = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(slug) + r"(?![A-Za-z0-9_])")
    supersedes = re.compile(r"\bsupersedes\b", re.IGNORECASE)
    found = []
    for row in load_manifest_rows(paths):
        other = row.get("slug")
        if other == slug or other is None:
            continue
        for key, value in row.items():
            if key == "slug" or not isinstance(value, str) or not mention.search(value):
                continue
            if key == "supersedes" and value.strip() == slug:
                continue
            found.append(f"manifest row field {key} ({other})")
    for block in _index_blocks(index_text):
        if block.slug == slug:
            continue
        for line in block.text.splitlines():
            hit = mention.search(line)
            if hit is None:
                continue
            if supersedes.search(line[:hit.start()]):
                continue
            found.append(f"SOURCE_INDEX.md block ({block.slug or block.text.splitlines()[0]})")
            break
    return found


def _remove(slug: str, reason: str, paths: RegistryPaths) -> RetirementResult:
    """The ladder, under the lock: park, rewrite, record — or put everything back.

    The directory and the raw copy are parked in staging by rename (reversible)
    and destroyed only after every rung succeeded. The manifest and the index are
    rewritten from byte snapshots that rollback writes straight back. The
    RETIRED.jsonl line is last: the durable record exists only for a removal that
    completed.
    """
    rows = load_manifest_rows(paths)
    row = next(r for r in rows if r.get("slug") == slug)
    index_text = paths.index.read_text()
    block = next(b for b in _index_blocks(index_text) if b.slug == slug)
    source_dir = paths.sources / slug
    raw_copy = _retired_raw_copy(row, rows, paths)

    manifest_bytes = paths.manifest.read_bytes()
    index_bytes = paths.index.read_bytes()
    retired_existed = paths.retired.exists()
    retired_mark = paths.retired.stat().st_size if retired_existed else 0

    staging = paths.staging / uuid.uuid4().hex
    parked_dir = staging / "sources" / slug
    parked_raw = staging / "raw" / raw_copy.name if raw_copy is not None else None
    line = {
        "slug": slug,
        "retired_at": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "index_block_sha256": hashlib.sha256(block.text.encode("utf-8")).hexdigest(),
        "row": row,
    }

    parked_dir.parent.mkdir(parents=True, exist_ok=True)
    moved_dir = moved_raw = False
    try:
        source_dir.rename(parked_dir)
        moved_dir = True
        if raw_copy is not None:
            parked_raw.parent.mkdir(parents=True, exist_ok=True)
            raw_copy.rename(parked_raw)
            moved_raw = True
        _write_manifest_without(slug, manifest_bytes, paths)
        _write_index_without(block, index_text, paths)
        _append_retired_line(line, paths)
    except Exception as error:
        _roll_back_retirement(
            manifest_bytes, index_bytes, retired_existed, retired_mark,
            (parked_dir, source_dir) if moved_dir else None,
            (parked_raw, raw_copy) if moved_raw else None,
            paths,
        )
        shutil.rmtree(staging, ignore_errors=True)
        raise RetirementError(f"retire failed for {slug}: {error}") from error

    shutil.rmtree(staging, ignore_errors=True)
    return RetirementResult(
        outcome="retired",
        slug=slug,
        removed={
            "manifest_row": row,
            "index_block": block.text,
            "source_dir": f"knowledge/sources/{slug}/",
            "raw_copy": f"knowledge/raw/{raw_copy.name}" if raw_copy is not None else None,
        },
        retired_line=line,
    )


def _retired_raw_copy(row: dict, rows: list[dict], paths: RegistryPaths) -> Path | None:
    """The `knowledge/raw/` copy this row owns, if the design stored one and no other row shares it.

    Only a local-PDF row records the name it was stored under (`origin_path`);
    the Zotero batch records its item key and not the file, so its raw copy is
    left where it is.
    """
    origin = row.get("origin_path")
    if not origin:
        return None
    name = Path(origin).name
    shared = any(
        r is not row and r.get("origin_path") and Path(r["origin_path"]).name == name
        for r in rows
    )
    candidate = paths.raw / name
    return candidate if candidate.is_file() and not shared else None


def _write_manifest_without(slug: str, manifest_bytes: bytes, paths: RegistryPaths) -> None:
    """Rewrite the manifest with every other line byte-identical."""
    kept = []
    for raw_line in manifest_bytes.splitlines(keepends=True):
        text = raw_line.decode("utf-8")
        if text.strip() and json.loads(text).get("slug") == slug:
            continue
        kept.append(raw_line)
    paths.manifest.write_bytes(b"".join(kept))


def _write_index_without(block: IndexBlock, index_text: str, paths: RegistryPaths) -> None:
    """Cut the block's span out; the rest of the index is untouched."""
    paths.index.write_text(index_text[:block.start] + index_text[block.end:])


def _append_retired_line(line: dict, paths: RegistryPaths) -> None:
    with open(paths.retired, "a") as handle:
        handle.write(json.dumps(line) + "\n")
        handle.flush()


def _roll_back_retirement(
    manifest_bytes: bytes,
    index_bytes: bytes,
    retired_existed: bool,
    retired_mark: int,
    parked_dir: tuple[Path, Path] | None,
    parked_raw: tuple[Path, Path] | None,
    paths: RegistryPaths,
) -> None:
    """Undo the rungs in reverse. Each step is a no-op if its rung never ran."""
    if retired_existed:
        with open(paths.retired, "r+b") as handle:
            handle.truncate(retired_mark)
    else:
        paths.retired.unlink(missing_ok=True)
    paths.index.write_bytes(index_bytes)
    paths.manifest.write_bytes(manifest_bytes)
    if parked_raw is not None:
        parked, original = parked_raw
        if parked.exists():
            parked.rename(original)
    if parked_dir is not None:
        parked, original = parked_dir
        if parked.exists():
            parked.rename(original)


# --- receipts: what a run can count on, written by the door itself (D8) ----------

RECEIPTS_DIRNAME = "receipts"
RUN_RECORD_NAME = "run.json"

# Outcomes reached only after the extractor actually ran. These are what spend a
# capture; a refusal decided before the fetch costs the run nothing.
POST_CAPTURE_OUTCOMES = frozenset({"registered", "capture_failed"})


def _run_limits(run_dir: Path) -> dict:
    return json.loads((run_dir / RUN_RECORD_NAME).read_text()).get("limits", {})


def _read_receipts(run_dir: Path) -> list[dict]:
    directory = run_dir / RECEIPTS_DIRNAME
    if not directory.is_dir():
        return []
    return [json.loads(p.read_text()) for p in sorted(directory.iterdir())]


def _write_receipt(
    run_dir: Path,
    source: Source,
    result: RegistrationResult,
    *,
    triage: str,
) -> Path:
    """One receipt per attempt, whatever the outcome. This is what `close` reads.

    `captured` records whether the extractor ran, which is what `max_captures`
    counts — a duplicate or holdout hit caught before the fetch costs nothing.
    """
    directory = run_dir / RECEIPTS_DIRNAME
    directory.mkdir(parents=True, exist_ok=True)
    attempt = len(_read_receipts(run_dir)) + 1
    now = datetime.now(timezone.utc)
    receipt = {
        "attempt": attempt,
        "outcome": result.outcome,
        "candidate": source.identity,
        "slug": result.slug,
        "path": result.location,
        "source_id": result.source_id,
        "triage": triage,
        "reason": result.reason,
        "rule_id": result.rule_id,
        "captured": _spent_a_capture(result),
        "at": now.isoformat(),
    }
    path = directory / f"{now.strftime('%Y%m%dT%H%M%S')}-{attempt:03d}.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    return path


def _spent_a_capture(result: RegistrationResult) -> bool:
    if result.outcome in POST_CAPTURE_OUTCOMES:
        return True
    # A duplicate or a holdout hit can be decided either side of the fetch; only
    # the post-capture ones carry a source_id read out of the extraction.
    return result.outcome in {"duplicate", "holdout_hit"} and result.source_id is not None


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
    reg.add_argument("--run", dest="run_dir", type=Path,
                     help="Research run directory; receipts this attempt and counts it "
                          "against the run's max_captures")
    reg.add_argument("--triage", choices=["keeper", "rejected"], default="keeper",
                     help="The triage decision recorded on the receipt (default: keeper)")

    sub.add_parser("verify", help="Report registry drift. Never repairs, never writes.")

    ret = sub.add_parser(
        "retire",
        help="Retire one registered source: remove its manifest row, index block, source "
             "directory and raw copy together, and record the removal in knowledge/RETIRED.jsonl",
    )
    ret.add_argument("--slug", required=True, help="The registry slug to retire")
    ret.add_argument("--reason", required=True,
                     help="Why it is retired; recorded verbatim on the RETIRED.jsonl line")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "verify":
        return _run_verify()
    if args.command == "retire":
        return _run_retire(args.slug, args.reason)
    source = UrlSource(url=args.url) if args.url else LocalPdfSource(path=args.local_pdf)
    result = register(
        source,
        SourceMetadata(
            title=args.title, use_for=args.use_for,
            validation=args.validation, caveat=args.caveat,
        ),
        budget=args.budget,
        run_dir=args.run_dir,
        triage=args.triage,
    )
    print(json.dumps(_result_as_json(result), indent=2))
    return 0 if result.outcome == "registered" else 1


def _run_verify() -> int:
    report = verify()
    for finding in report.findings:
        print(f"{finding.klass:7} {finding.kind:20} {finding.path} — {finding.detail}")
    legacy = sum(1 for f in report.findings if f.klass == "legacy")
    faults = sum(1 for f in report.findings if f.klass == "fault")
    print(f"\n{faults} fault(s), {legacy} legacy entry(ies)")
    return 1 if report.has_faults else 0


def _run_retire(slug: str, reason: str) -> int:
    """Print what was removed and the RETIRED.jsonl line (R4), or the refusal."""
    result = retire(slug, reason)
    if result.outcome != "retired":
        payload = {"outcome": result.outcome, "reason": result.reason}
        if result.rule_id:
            payload["rule_id"] = result.rule_id
            payload["offsets"] = list(result.offsets)
        if result.references:
            payload["references"] = list(result.references)
        print(json.dumps(payload, indent=2))
        return 1
    removed = result.removed
    print(f"retired {result.slug}")
    print(f"  removed manifest row:   {json.dumps(removed['manifest_row'])}")
    print(f"  removed source dir:     {removed['source_dir']}")
    print(f"  removed raw copy:       {removed['raw_copy'] or '(none stored outside the source dir)'}")
    print("  removed index block:")
    for line in removed["index_block"].splitlines():
        print(f"    {line}")
    print("  RETIRED.jsonl line:")
    print(f"    {json.dumps(result.retired_line)}")
    return 0


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
