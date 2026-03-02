# Design: Extraction Pipeline Integration (agentic-mbse Redesign)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-02-27 08:09:05 PST
**Branch:** processing-work
**Spec:** `.project/active/extraction-pipeline-integration/spec.md`

---

## Overview

Update `scripts/zotero_ingest.py` to align with the redesigned agentic-mbse 8-step extraction pipeline, replacing deprecated flags and broken filename references, adding smart defaults for maximum quality, and adding a re-extraction mode for existing sources.

## Related Artifacts

- **Spec:** `.project/active/extraction-pipeline-integration/spec.md`
- **Research:** `.project/research/20260227-074139_extraction-pipeline-redesign-integration.md`
- **agentic-mbse Docs:** `~/1cfe/agentic-mbse/docs/extraction.md`
- **Corpus Audit:** `work/analysis/corpus-ingestion-quality-audit.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md` (KNOW-DB)

## Research Findings

### agentic-mbse Integration Boundary

The CLI is the stable interface. Key behaviors confirmed by source code analysis:

**Output directory nesting** (`base.py:56-65`): `get_output_dir()` always creates a subdirectory named after `sanitize_filename(input_path.name)` under the `--output` base. When fusion-tea calls `agentic-mbse extract paper.pdf --output knowledge/sources/my_slug/`, output lands at `knowledge/sources/my_slug/<sanitized_pdf_name>/output.md`. The `_flatten_extraction_output()` workaround is still needed.

**`--force` behavior** (`extract_cli.py:230-234`): Only bypasses the `output.md` existence check. Does NOT delete old files. After re-extraction, old files (`full_document.md`, `summary.json`, `style.json`) will coexist with new files unless explicitly removed.

**INDEX.md generation** (`extract_cli.py:269-279`): When `--index` is passed, the CLI reads the just-written `output.md` (not `full_document.md`) and generates `INDEX.md` from it. This works correctly with the new pipeline.

**CLI flags confirmed** (from `~/1cfe/agentic-mbse/docs/extraction.md`):

| Flag | Default | Fusion-tea usage |
|------|---------|------------------|
| `--budget USD` | 2.0 | Override to 50.0 |
| `--model {opus,sonnet,haiku}` | sonnet | Override to opus |
| `--force` | off | Used for re-extraction |
| `--output DIR` | alongside input | Always passed |
| `--index` | off | Always passed |
| `--summarize` | off | Always passed |

### Current Script Structure

`scripts/zotero_ingest.py` (445 lines) is a single-file batch script. It has one external integration point: the `run_extraction()` function that shells out to `agentic-mbse extract`. The agentic-mbse interface details (output filename, CLI flags) are scattered across 5 locations in the file:

| Location | What's hardcoded |
|----------|-----------------|
| `run_extraction()` :90-113 | CLI flags (`--enhance`) |
| `_flatten_extraction_output()` :116-132 | Output filename (`full_document.md`) |
| `process_zotero_item()` :285-291 | Output filename (`full_document.md`) |
| `process_local_pdf()` :376-382 | Output filename (`full_document.md`) |
| `parse_args()` :61-64 | `--no-enhance` flag |

`scripts/zotero_lib.py` has no agentic-mbse references — no changes needed.

### Re-extraction Constraint

The current script only processes NEW items (not in manifest). Re-extracting existing sources requires a mechanism to bypass the manifest filter and reuse existing slugs. All 6 manifested entries have Zotero keys, so Zotero API access can resolve their PDFs. The raw PDFs are also cached in `knowledge/raw/` from the initial extraction.

---

## Proposed Design

### Design Rationale

**Stay with CLI subprocess.** The Python API (`extract_pdf()`, `PipelineConfig`, `PipelineResult`) would eliminate the flatten hack and give structured results, but the CLI is the documented stable interface. fusion-tea already depends on agentic-mbse as a package (editable dep), so coupling exists either way — but the CLI boundary absorbs internal refactors without breaking consumers. The flatten hack is 15 lines and well-understood; it's not worth changing the integration model to eliminate it.

**Isolate the integration boundary with constants.** The agentic-mbse interface details are currently scattered across the file. Extracting them as named constants at the top makes the dependency explicit: when agentic-mbse changes again (it will), there's one place to look. This is the minimum useful abstraction — no new files, no new classes, just clarity.

**Add `--re-extract` as a first-class mode.** Re-extraction is a recurring need: upstream pipeline improves, quality issues are found, output format changes. Making it a script mode (like `--sync-tags`) prevents ad-hoc manual workarounds and ensures legacy file cleanup happens automatically.

### Component 1: Integration Constants

Add a constants block at the top of `zotero_ingest.py`, after imports and before `parse_args()`:

```python
# -- agentic-mbse extraction interface --
# These reflect the agentic-mbse CLI contract. Update here if upstream changes.
EXTRACT_OUTPUT = "output.md"
EXTRACT_LEGACY_FILES = ("full_document.md", "summary.json", "style.json")
DEFAULT_BUDGET = 50.0
DEFAULT_MODEL = "opus"
```

Every downstream reference to the output filename, budget default, or model default uses these constants. If agentic-mbse changes `output.md` to something else in the future, one constant update fixes the entire script.

### Component 2: CLI Interface (`parse_args()`)

**Remove:**
```python
parser.add_argument("--no-enhance", action="store_true",
    help="Disable --enhance (use basic extraction only)")
```

**Add:**
```python
parser.add_argument("--budget", type=float, default=DEFAULT_BUDGET,
    help=f"Claude budget in USD per document (default: {DEFAULT_BUDGET}, 0 = no Claude)")
parser.add_argument("--model", choices=["opus", "sonnet", "haiku"], default=DEFAULT_MODEL,
    help=f"Claude model for enhancement (default: {DEFAULT_MODEL})")
parser.add_argument("--re-extract", action="store_true",
    help="Re-extract all manifested sources (uses --force, cleans up legacy files)")
```

**Update docstring** to reflect new flags:
```
Usage:
    uv run python scripts/zotero_ingest.py                    # process all pending
    uv run python scripts/zotero_ingest.py --dry-run           # list pending items
    uv run python scripts/zotero_ingest.py --budget 0          # no Claude enhancement
    uv run python scripts/zotero_ingest.py --model sonnet      # use sonnet instead of opus
    uv run python scripts/zotero_ingest.py --re-extract        # re-extract existing sources
    uv run python scripts/zotero_ingest.py --local-pdf path.pdf
```

### Component 3: `run_extraction()` Signature

**Current:** `run_extraction(pdf_path: Path, output_dir: Path, enhance: bool) -> bool`

**New:** `run_extraction(pdf_path: Path, output_dir: Path, *, budget: float = DEFAULT_BUDGET, model: str = DEFAULT_MODEL, force: bool = False) -> bool`

The function builds the CLI command:
```python
cmd = [
    "uv", "run", "agentic-mbse", "extract", str(pdf_path),
    "--output", str(output_dir),
    "--index", "--summarize",
    "--budget", str(budget),
    "--model", model,
]
if force:
    cmd.append("--force")
```

Key changes:
- `--budget` and `--model` are always passed (no conditional)
- `--force` is conditional (only for re-extraction)
- `--enhance` is gone entirely
- `--index` and `--summarize` remain unchanged

### Component 4: `_flatten_extraction_output()`

Minimal change: replace the hardcoded filename with the constant.

```python
def _flatten_extraction_output(output_dir: Path) -> None:
    """If agentic-mbse extract created a single nested subdir, move contents up."""
    if (output_dir / EXTRACT_OUTPUT).exists():
        return  # already flat
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    if len(subdirs) == 1 and (subdirs[0] / EXTRACT_OUTPUT).exists():
        nested = subdirs[0]
        for item in nested.iterdir():
            dest = output_dir / item.name
            if dest.exists():
                continue
            item.rename(dest)
        if not any(nested.iterdir()):
            nested.rmdir()
        print(f"  Flattened extraction output from {nested.name}/")
```

### Component 5: Legacy File Cleanup

New function, called after successful extraction in re-extract mode:

```python
def _cleanup_legacy_files(output_dir: Path) -> None:
    """Remove legacy extraction files if new output exists."""
    if not (output_dir / EXTRACT_OUTPUT).exists():
        return
    for name in EXTRACT_LEGACY_FILES:
        legacy = output_dir / name
        if legacy.exists():
            legacy.unlink()
            print(f"  Removed legacy file: {name}")
```

This is called:
- After `_flatten_extraction_output()` during re-extraction
- Not during normal ingestion (new directories won't have legacy files)

### Component 6: SHA256 Computation

Both `process_zotero_item()` and `process_local_pdf()` use the constant:

```python
extract_doc = output_dir / EXTRACT_OUTPUT
if not extract_doc.exists():
    print(f"  WARNING: {EXTRACT_OUTPUT} not found at {extract_doc}")
    extract_sha = "(not found)"
else:
    extract_sha = sha256_of(extract_doc)
```

### Component 7: Call Sites

**`process_zotero_item()`** (line 278):
```python
# Old: ok = run_extraction(result.path, output_dir, enhance=not args.no_enhance)
ok = run_extraction(result.path, output_dir, budget=args.budget, model=args.model)
```

**`process_local_pdf()`** (line 367):
```python
# Old: ok = run_extraction(raw_copy, output_dir, enhance=not args.no_enhance)
ok = run_extraction(raw_copy, output_dir, budget=args.budget, model=args.model)
```

### Component 8: `--re-extract` Mode

New function and `main()` integration:

```python
def re_extract_sources(zot, args) -> None:
    """Re-extract all manifested sources with the current pipeline."""
    manifest = load_manifest()
    if not manifest:
        print("Manifest is empty — nothing to re-extract.")
        return

    items = list(manifest.values())
    if args.limit:
        items = items[:args.limit]

    if args.dry_run:
        print(f"\n{len(items)} source(s) would be re-extracted:\n")
        for entry in items:
            print(f"  [{entry['zotero_key']}] {entry['title']}")
            print(f"           slug: {entry['slug']}")
        return

    print(f"\n{len(items)} source(s) to re-extract")
    stats = {"found": len(items), "extracted": 0, "skipped": 0, "failed": 0}

    for entry in items:
        slug = entry["slug"]
        title = entry["title"]
        zotero_key = entry["zotero_key"]
        output_dir = SOURCES_DIR / slug
        print(f"\n--- {title} [{zotero_key}] ---")

        # Resolve PDF (download if not cached)
        try:
            item = zot.item(zotero_key)
        except Exception as e:
            print(f"  Failed to fetch Zotero item: {e}")
            stats["failed"] += 1
            continue

        pdf_info = resolve_pdf_info(zot, item)
        if pdf_info is None:
            print(f"  No PDF attachment — skipping")
            stats["skipped"] += 1
            continue

        try:
            dl_result = download_pdf_from_info(zot, pdf_info, args.output_dir)
        except RuntimeError as e:
            print(f"  Download failed: {e}")
            stats["failed"] += 1
            continue

        # Run extraction with --force
        try:
            ok = run_extraction(
                dl_result.path, output_dir,
                budget=args.budget, model=args.model, force=True,
            )
        except subprocess.TimeoutExpired:
            print(f"  Extraction timed out")
            stats["failed"] += 1
            continue
        if not ok:
            stats["failed"] += 1
            continue

        # Clean up legacy files
        _cleanup_legacy_files(output_dir)

        # Report new SHA256
        extract_doc = output_dir / EXTRACT_OUTPUT
        if extract_doc.exists():
            new_sha = sha256_of(extract_doc)
            print(f"  New {EXTRACT_OUTPUT} SHA256: {new_sha[:16]}...")
        stats["extracted"] += 1

    print_summary(stats)
```

**`main()` integration** — add after the `--sync-tags` early exit:
```python
if args.re_extract:
    re_extract_sources(zot, args)
    return
```

**Interaction with other flags:**
- `--dry-run` + `--re-extract`: lists what would be re-extracted
- `--limit` + `--re-extract`: re-extract at most N sources
- `--budget` / `--model` + `--re-extract`: control extraction quality
- `--tag` is ignored (re-extract uses manifest, not Zotero tags)

### Data Flow Summary

**Normal ingestion** (unchanged flow, updated flags):
```
Zotero query → filter pending → download PDF → run_extraction(budget, model)
→ flatten → SHA256(output.md) → SOURCE_INDEX.md → MANIFEST.jsonl
```

**Re-extraction** (new flow):
```
MANIFEST.jsonl → for each entry → resolve PDF via Zotero → download if needed
→ run_extraction(budget, model, force=True) → flatten → cleanup legacy files
→ report new SHA256
```

**Local PDF** (unchanged flow, updated flags):
```
Copy to raw/ → run_extraction(budget, model) → flatten
→ SHA256(output.md) → SOURCE_INDEX.md
```

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| agentic-mbse `--force` overwrites but doesn't clean legacy files | Medium — old `full_document.md` lingers | `_cleanup_legacy_files()` runs after extraction in re-extract mode |
| Opus model + $50 budget = slow per-document extraction | Low — user explicitly chose quality over speed | `--model` and `--budget` can be overridden per run |
| `_flatten_extraction_output()` race condition: dir has no `output.md` yet and no subdirs | Low — only if extraction produced no output | Existing error handling in `run_extraction()` catches non-zero exit codes before flatten runs |
| Zotero API access required for `--re-extract` | Low — same requirement as normal batch mode | Document in help text; user already has API key configured |
| `get_output_dir()` nesting changes in future agentic-mbse release | Low — would require flatten logic update | Integration constants + flatten function isolate this; easy to update |

---

## Integration Strategy

This is a **surgical update** to one file (`scripts/zotero_ingest.py`). No new files, no new dependencies, no architectural changes. The script's responsibilities and overall structure remain identical.

**What changes:** The agentic-mbse integration point (CLI flags, output filename) and the CLI interface (new flags for budget/model/re-extract).

**What doesn't change:** `zotero_lib.py`, the Zotero query/download logic, slug generation, SOURCE_INDEX.md format, MANIFEST.jsonl format, the overall batch processing flow.

**Execution after code changes:**
1. Re-extract existing 6 sources: `uv run python scripts/zotero_ingest.py --re-extract`
2. Add ~6 more PDFs to Zotero, tag `new`
3. Ingest new sources: `uv run python scripts/zotero_ingest.py`
4. Verify 12+ sources in `knowledge/sources/`, all with `output.md`

---

## Validation Approach

### Automated Checks
- Run extraction on one known-good PDF to verify CLI command builds correctly
- Verify `output.md` exists in output directory after extraction
- Verify legacy files are removed after `--re-extract`
- Verify `--budget 0` produces extraction with no Claude calls (check for absence of `cost.json`)

### Manual Verification
- **Delene (Source 3):** Confirm no LLM dialogue contamination in re-extracted `output.md`
- **Hawker (Source 1):** Confirm no strikethrough table headers
- **All 12+ sources:** Confirm each directory contains `output.md`, `metrics.json`, `decisions.json`, `INDEX.md`
- **Zero deprecation warnings:** Run with verbose output and grep for "DeprecationWarning"
- **Both paths work:** Test one Zotero-sourced extraction and one `--local-pdf` extraction

### Acceptance Criteria Mapping

| Spec Criterion | How Verified |
|----------------|--------------|
| `run_extraction()` uses `--budget`/`--model` | Code inspection |
| `_flatten_extraction_output()` checks `output.md` | Run extraction, check output |
| SHA256 from `output.md` | Check SOURCE_INDEX.md entries |
| `--budget` default 50.0 | `--help` output |
| `--model` default opus | `--help` output |
| All 6 re-extracted with `output.md` | `ls knowledge/sources/*/output.md` |
| Legacy files removed | `ls knowledge/sources/*/full_document.md` (should be empty) |
| `metrics.json` and `decisions.json` present | `ls knowledge/sources/*/metrics.json` |
| 12+ total sources | Count directories in `knowledge/sources/` |
| Zero deprecation warnings | Grep extraction output |
| Both Zotero and `--local-pdf` work | Test both paths |

---

**Next Step:** After approval → `/_my_plan` (multi-phase: code changes, re-extraction, new ingestion)
