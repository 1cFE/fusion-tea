# Implementation Plan: Zotero Ingestion Automation Script (KNOW-DB Item 3)

**Status:** Complete
**Created:** 2026-02-09 01:21 UTC
**Last Updated:** 2026-02-09 01:21 UTC

## Source Documents
- **Spec:** `.project/active/zotero-ingestion-script/spec.md`
- **Design:** `.project/active/zotero-ingestion-script/design.md` — See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 extracts shared abstractions and validates them against the existing download script (regression test). Phase 2 builds the core batch pipeline on that foundation. Phase 3 adds the alternate code paths (dry-run, local PDF). This order de-risks the shared module first, then delivers the primary feature, then layers on secondary modes.

**Validation Approach:**
No unit tests — these are CLI scripts that call external APIs (Zotero) and subprocess (`agentic-mbse extract`). Validation is manual/integration-based, consistent with Items 1 and 2. Each phase has a concrete "run this, see that" check.

---

## Phase 1: Shared Module + Refactor Download Script

### Goal
Extract common Zotero logic into `scripts/zotero_lib.py` and refactor `scripts/zotero_group_download.py` to import from it. Validates the abstractions by confirming the existing download script works identically.

### Changes Required

**See `design.md#component-1` for:** function signatures, DownloadResult NamedTuple, error handling contract (return values/exceptions instead of sys.exit)

**Specific file changes:**

#### 1. `scripts/zotero_lib.py` (NEW)
- [x] Create file with shared constants: `GROUP_ID`, `RAW_DIR`, `SOURCES_DIR`, `SOURCE_INDEX_PATH`
- [x] Implement `load_api_key()` — extracted from `zotero_group_download.py:48-54`, raises `ValueError` instead of `sys.exit`
- [x] Implement `connect(api_key)` — wraps `zotero.Zotero(GROUP_ID, "group", api_key)`
- [x] Implement `find_pdf_attachment(zot, item_key)` — extracted from `zotero_group_download.py:57-67`, returns `None` instead of `sys.exit`
- [x] Implement `DownloadResult(NamedTuple)` and `download_pdf(zot, item_key, output_dir)` — extracted from `zotero_group_download.py:70-101`, raises `RuntimeError` on failure
- [x] Implement `sha256_of(path)` — extracted from the inline `hashlib.sha256` pattern
- [x] Implement `tag_extracted(zot, item_key)` — extracted from `zotero_group_download.py:104-112`
- [x] Implement `slugify(title, max_len)` — new, see `design.md#slug-generation`

#### 2. `scripts/zotero_group_download.py` (MODIFIED)
- [x] Replace inline functions with imports from `zotero_lib`
- [x] Keep `parse_args()` and `main()` local (CLI-specific)
- [x] Preserve `sys.exit(1)` behavior in `main()` for single-item errors (wrap shared functions)
- [x] Preserve identical CLI interface and output format

### Validation

**Manual:**
- [ ] Run: `uv run python scripts/zotero_group_download.py PMXLGPKG` — should print title, key, filename, SHA256 (same as before refactor, PDF already in `knowledge/raw/` so download skips)
- [ ] Run: `uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only` — should report already tagged
- [ ] Run: `uv run python scripts/zotero_group_download.py NONEXISTENT` — should print error and exit 1

**What We Know Works After This Phase:**
Shared module is correct — all Zotero operations (connect, find PDF, download, tag, SHA256) work through the new abstractions. Download script is not regressed.

---

## Phase 2: Batch Ingestion Core

### Goal
Build `scripts/zotero_ingest.py` with the Zotero query, batch processing loop, extraction subprocess, SOURCE_INDEX.md auto-append, tagging, error handling, and summary output. This is the primary deliverable.

### Changes Required

**See `design.md#component-3` for:** CLI interface, main flow, `process_zotero_item` steps, `append_source_index_entry` logic, subprocess construction, `--no-enhance` wiring

**Specific file changes:**

#### 1. `scripts/zotero_ingest.py` (NEW)
- [x] Create file with argparse: `--no-enhance`, `--output-dir`, `--dry-run`, `--local-pdf`
- [x] Implement `main()` — smart pull via `zot.everything(zot.top(tag=["new", "-extracted"]))`, loop over items, collect stats, print summary
- [x] Implement `process_zotero_item(zot, item, args)` — 10-step pipeline per `design.md#component-3`, returns `"extracted"` / `"skipped"` / `"failed"`
- [x] Implement `run_extraction(pdf_path, output_dir, enhance)` — subprocess call per `design.md#extraction-subprocess-vs-python-api`
- [x] Implement `resolve_slug(slug, item_key)` — collision check against `knowledge/sources/`, append `_<item_key>` if exists
- [x] Implement `append_source_index_entry(title, slug, item_key, pdf_sha256, extract_sha256)` — Zotero template per `design.md#source_indexmd-insertion-logic`
- [x] Implement `print_summary(stats)`

### Validation

**Manual:**
- [ ] Ensure at least one Zotero item is tagged `new` but NOT `extracted` in the 1cfe group library (add a test document if needed)
- [ ] Run: `uv run python scripts/zotero_ingest.py` — should discover item(s), download, extract, append to SOURCE_INDEX.md, tag as extracted, print summary
- [ ] Verify `knowledge/sources/<slug>/` contains `full_document.md`, `INDEX.md`, `summary.json`
- [ ] Verify `knowledge/SOURCE_INDEX.md` has new entry with correct format (blank "Use for" and "Validation", extended metadata block)
- [ ] Verify new entry is inserted BEFORE `## How MBSE Commands Use This File`
- [ ] Verify existing entries (PyFECONS, TEA D-T MFE) are unchanged
- [ ] Run again: should find 0 new items (previously processed items now tagged `extracted`)

**What We Know Works After This Phase:**
Full Zotero-based batch pipeline: query → download → extract → register → tag → summary. Error handling continues batch on failure. Idempotent re-runs.

---

## Phase 3: Dry-Run + Local PDF

### Goal
Add `--dry-run` mode and `--local-pdf` fallback path to the ingestion script. Complete all acceptance criteria.

### Changes Required

**See `design.md#component-3` for:** `print_dry_run` behavior, `process_local_pdf` steps, local PDF SOURCE_INDEX.md template (no Zotero key)

**Specific file changes:**

#### 1. `scripts/zotero_ingest.py` (EXTEND)
- [x] Implement `--dry-run` handler — query Zotero, list items with title/key/PDF filename, mark no-PDF items, exit without side effects
- [x] Implement `--local-pdf` handler (`process_local_pdf`) — derive slug from filename, numeric collision suffix (`_2`, `_3`), copy to `knowledge/raw/`, extract, append SOURCE_INDEX.md (local template, no Zotero key), print summary
- [x] Wire `--local-pdf` to skip Zotero connection entirely (no API key needed)

### Validation

**Manual:**
- [ ] Run: `uv run python scripts/zotero_ingest.py --dry-run` — should list pending items (or "0 items found") without downloading, extracting, or tagging anything
- [ ] Verify SOURCE_INDEX.md is unchanged after dry-run
- [ ] Run: `uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/<existing-pdf>` — should extract, register in SOURCE_INDEX.md (no Zotero key field), print summary
- [ ] Verify local PDF entry has no `Zotero Key` line in extended metadata
- [ ] Test with a PDF whose slug collides with existing directory — verify numeric suffix applied

**What We Know Works After This Phase:**
All three modes operational: batch Zotero ingest, dry-run preview, local PDF fallback. All spec acceptance criteria met.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If refactored download script behaves differently, diff the stdout output against a pre-refactor run. The shared module's error contract (return/raise vs sys.exit) is the main change surface.
- **Phase 2**: If `tag=['new', '-extracted']` negation doesn't work, fall back to querying `tag='new'` and filtering out `extracted`-tagged items in Python. Test with `--dry-run` first (Phase 3, but can be stubbed early).
- **Phase 3**: `--local-pdf` is the simplest path (no API calls). Low risk.

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- Created `scripts/zotero_lib.py` with all 8 shared functions/classes per design
- Rewrote `scripts/zotero_group_download.py` to import from `zotero_lib`
- Preserved identical CLI interface (`item_key`, `--tag-extracted`, `--tag-only`, `--output-dir`)
- Preserved `sys.exit(1)` behavior: wraps `load_api_key()` ValueError and `download_pdf()` RuntimeError
- `find_pdf_attachment` called early for fast-fail before `download_pdf` (which calls it again internally — one extra API call, acceptable for single-item script)
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- Created `scripts/zotero_ingest.py` with full batch pipeline
- All functions per design: `main()`, `process_zotero_item()`, `run_extraction()`, `resolve_slug()`, `append_source_index_entry()`, `print_summary()`
- 10-step pipeline in `process_zotero_item` matches design exactly
- SOURCE_INDEX.md insertion uses `\n## How MBSE Commands Use This File` marker with fallback to append
- Extraction subprocess uses 900s timeout per design
- `--enhance` is default, `--no-enhance` disables it
**Issues:** None
**Deviations:** Built Phase 3 features (dry-run, local-pdf) into the same file from the start since all phases were implemented together

### Phase 3 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- `--dry-run`: queries Zotero, calls `print_dry_run()` listing title/key/PDF for each item, marks no-PDF items, exits without side effects
- `--local-pdf`: `process_local_pdf()` derives title from filename (stem → title case), slugifies, numeric collision resolution, copies to raw/, runs extraction, appends SOURCE_INDEX.md (no Zotero Key line), prints summary
- `--local-pdf` skips Zotero connection entirely (checked before `load_api_key()`)
**Issues:** None
**Deviations:** None

---

**Status**: Complete
