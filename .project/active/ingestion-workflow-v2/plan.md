# Implementation Plan: Ingestion Workflow V2 — Git-Authoritative Pipeline

**Status:** Complete
**Created:** 2026-02-09
**Last Updated:** 2026-02-09

## Source Documents
- **Spec:** `.project/active/ingestion-workflow-v2/spec.md`
- **Design:** `.project/active/ingestion-workflow-v2/design.md` — See here for component details, function signatures, schema, architecture

## Implementation Strategy

**Phasing Rationale:**
Three phases following dependency order: manifest infrastructure first (everything depends on it), then standalone attachment support (needed before rewiring the ingest script), then the ingest script rewire itself (which consumes both). Each phase produces independently testable output.

**Overall Validation Approach:**
- No automated test suite exists for these scripts — validation is manual via `--dry-run` and real Zotero API calls
- Each phase has specific manual validation commands
- The final phase validates all spec acceptance criteria end-to-end

**Environment:** All commands use `uv run python` per CLAUDE.md

---

## Phase 1: Manifest Infrastructure

### Goal
Add the JSONL manifest file and its read/write functions to `zotero_lib.py`. Seed the manifest with the existing `PMXLGPKG` extraction. This is the foundation — Phases 2 and 3 depend on being able to load and append manifest entries.

### Test Stencil (Validate Manually)
```python
# Quick REPL validation after implementation:
# uv run python -c "
# import sys; sys.path.insert(0, 'scripts')
# from zotero_lib import load_manifest, manifest_keys, append_manifest_entry
# print('keys:', manifest_keys())          # Should show {'PMXLGPKG'}
# print('manifest:', load_manifest())      # Should show full entry dict
# append_manifest_entry('TESTKEY', 'test_slug', 'Test Title')
# print('after append:', manifest_keys())  # Should show {'PMXLGPKG', 'TESTKEY'}
# "
# Then remove the TESTKEY line from MANIFEST.jsonl
```

### Changes Required

**See `design.md#component-1` for:** manifest schema, function signatures, JSONL format

#### 1. Seed Manifest File
**File:** `knowledge/MANIFEST.jsonl` (NEW)
- [x] Create file with single seed entry for existing `PMXLGPKG` extraction:
  ```
  {"zotero_key": "PMXLGPKG", "slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE Cost Analysis", "date_extracted": "2026-02-08"}
  ```

#### 2. Add Manifest Functions to Library
**File:** `scripts/zotero_lib.py`
- [x] Add `import json` to imports (line 7 area)
- [x] Add `MANIFEST_PATH = Path("knowledge/MANIFEST.jsonl")` constant (after line 19)
- [x] Add `load_manifest() -> dict[str, dict]` — reads JSONL, returns `{zotero_key: entry_dict}`
- [x] Add `manifest_keys() -> set[str]` — convenience wrapper returning just the keys
- [x] Add `append_manifest_entry(zotero_key: str, slug: str, title: str) -> None` — appends one JSONL line with today's date
- [x] Export new functions and `MANIFEST_PATH` (they'll be imported by `zotero_ingest.py` in Phase 3)

### Validation

**Manual:**
- [x] `knowledge/MANIFEST.jsonl` exists with exactly 1 line (the seed entry)
- [x] Run the REPL test stencil above — `manifest_keys()` returns `{'PMXLGPKG'}`
- [x] Run `load_manifest()` — returns dict keyed by `'PMXLGPKG'` with slug, title, date
- [x] Run `append_manifest_entry()` with a test key — verify a second line appears in the file
- [x] Clean up test entry after validation

**What We Know Works After This Phase:**
Manifest can be created, read, queried for keys, and appended to. The seed entry prevents re-processing of the existing extraction.

---

## Phase 2: Standalone Attachment Support

### Goal
Add `PdfInfo` NamedTuple and `resolve_pdf_info()` to `zotero_lib.py`, and adapt `download_pdf()` to work with PdfInfo. This enables the ingest script (Phase 3) to handle both parent items and standalone PDF attachments through a single interface. Keep `find_pdf_attachment()` intact for backward compatibility with `zotero_group_download.py`.

### Test Stencil (Validate Manually)
```python
# Requires Zotero API access:
# uv run python -c "
# import sys; sys.path.insert(0, 'scripts')
# from zotero_lib import load_api_key, connect, resolve_pdf_info
# zot = connect(load_api_key())
# # Test with a known parent item (has PDF child)
# item = zot.item('PMXLGPKG')
# info = resolve_pdf_info(zot, item)
# print('Parent item PdfInfo:', info)        # Should show child_key, filename, title, is_standalone=False
# # Test with a known standalone attachment (if one exists)
# # items = zot.everything(zot.top())
# # standalone = [i for i in items if i['data']['itemType'] == 'attachment']
# # if standalone: print(resolve_pdf_info(zot, standalone[0]))
# "
```

### Changes Required

**See `design.md#component-3` for:** `PdfInfo` schema, `resolve_pdf_info()` logic, `download_pdf()` adaptation

#### 1. Add PdfInfo and resolve_pdf_info
**File:** `scripts/zotero_lib.py`
- [x] Add `PdfInfo` NamedTuple (after existing `DownloadResult` at line 48):
  - Fields: `child_key`, `filename`, `title`, `is_standalone`
- [x] Add `resolve_pdf_info(zot, item: dict) -> PdfInfo | None`:
  - If `itemType == 'attachment'` and `contentType == 'application/pdf'`: return PdfInfo with `is_standalone=True`, use item's own key as `child_key`, use filename (cleaned) as title
  - Otherwise: call existing `find_pdf_attachment()` to get PDF child, return PdfInfo with `is_standalone=False`
  - Return `None` if no PDF available

#### 2. Adapt download_pdf for PdfInfo
**File:** `scripts/zotero_lib.py`
- [x] Add new `download_pdf_from_info(zot, pdf_info: PdfInfo, output_dir: Path) -> DownloadResult` function:
  - Uses `pdf_info.child_key` for `zot.dump()` call
  - Uses `pdf_info.filename` for local path
  - Uses `pdf_info.title` for `DownloadResult.title`
  - Reuses existing skip-if-exists and SHA256 logic
- [x] Keep existing `download_pdf()` unchanged (used by `zotero_group_download.py`)

### Validation

**Manual:**
- [x] REPL test with known parent item (`PMXLGPKG`) — `resolve_pdf_info()` returns PdfInfo with `is_standalone=False`
- [x] Verify `find_pdf_attachment()` still works (backward compat for `zotero_group_download.py`)
- [x] If standalone attachments exist in library, test `resolve_pdf_info()` with one
- [x] Test `download_pdf_from_info()` with a PdfInfo from a parent item — verify download works

**What We Know Works After This Phase:**
Both parent items and standalone attachments can be resolved to a uniform `PdfInfo` and downloaded. Existing `find_pdf_attachment()` and `download_pdf()` are untouched.

---

## Phase 3: Rewire Ingest Script

### Goal
Replace the tag-based queue in `zotero_ingest.py` with manifest-based diffing. Add `--limit`, `--tag`, `--sync-tags` flags. Remove eager Zotero tagging. Add manifest writes after successful extraction. Update dry-run output. This is the core behavioral change.

### Test Stencil (Validate Against Real Library)
```bash
# 1. Dry run — should list all items NOT in manifest (no 'new' tag required)
uv run python scripts/zotero_ingest.py --dry-run

# 2. Dry run with limit — should show at most 3
uv run python scripts/zotero_ingest.py --dry-run --limit 3

# 3. Dry run with tag filter — should show only 'new'-tagged items not in manifest
uv run python scripts/zotero_ingest.py --dry-run --tag new

# 4. Extract one item — should NOT tag in Zotero, SHOULD append to manifest
uv run python scripts/zotero_ingest.py --limit 1

# 5. Idempotency — should process 0 items
uv run python scripts/zotero_ingest.py --limit 1

# 6. Sync tags — should tag manifested items in Zotero
uv run python scripts/zotero_ingest.py --sync-tags

# 7. Local PDF — should still work (no manifest interaction)
uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/some_paper.pdf --dry-run
```

### Changes Required

**See `design.md#component-2,4,5,6` for:** queue logic, deferred tagging, batch control, CLI interface

#### 1. Update Imports
**File:** `scripts/zotero_ingest.py` (lines 25-37)
- [x] Add imports: `manifest_keys`, `load_manifest`, `append_manifest_entry`, `resolve_pdf_info`, `download_pdf_from_info`, `MANIFEST_PATH`
- [x] Remove import: `find_pdf_attachment` (no longer used directly in this file)
- [x] Remove import: `tag_extracted` (no longer called during extraction; `--sync-tags` uses it via `zotero_lib`)
- [x] Keep `tag_extracted` import actually — needed for `sync_tags_command()`

#### 2. Update parse_args
**File:** `scripts/zotero_ingest.py` (lines 40-65)
- [x] Add `--limit` argument (type=int, help text about batch size)
- [x] Add `--sync-tags` argument (store_true, help text about post-commit tag sync)
- [x] Add `--tag` argument (type=str, help text about optional tag filter)
- [x] Update module docstring (lines 2-16) to reflect new CLI

#### 3. Add sync_tags_command
**File:** `scripts/zotero_ingest.py` (new function)
- [x] Add `sync_tags_command(zot)` — loads manifest, calls `tag_extracted()` for each entry
- [x] Print summary of how many items tagged

#### 4. Add fetch + queue logic
**File:** `scripts/zotero_ingest.py` (new functions)
- [x] Add `fetch_all_processable_items(zot) -> list[dict]`:
  - Fetch `zot.everything(zot.top())` for parent items
  - Also fetch standalone PDF attachments (items where `itemType=='attachment'`, `contentType=='application/pdf'`, no `parentItem`)
  - Combine and return
- [x] Add `compute_pending_queue(all_items, known_keys) -> list[dict]`:
  - Filter to items whose key is not in `known_keys`

#### 5. Rewire main()
**File:** `scripts/zotero_ingest.py` (lines 317-348)
- [x] Add `--sync-tags` early exit path (after connecting, before queue logic)
- [x] Replace tag-based query (lines 332-335) with:
  - `fetch_all_processable_items()` → `compute_pending_queue()` with `manifest_keys()`
  - Apply `--tag` filter if provided
  - Apply `--limit` if provided
- [x] Update messaging (remove references to `tag=['new', '-extracted']`)

#### 6. Rewire process_zotero_item
**File:** `scripts/zotero_ingest.py` (lines 173-231)
- [x] Replace `find_pdf_attachment()` call (line 182) with `resolve_pdf_info()`
- [x] Replace `download_pdf()` call (line 189) with `download_pdf_from_info()` using PdfInfo
- [x] Use `pdf_info.title` for the title (instead of `item["data"].get("title")` — `resolve_pdf_info` already resolves the best title)
- [x] Remove `tag_extracted()` call (lines 223-228)
- [x] Add `append_manifest_entry()` call after successful SOURCE_INDEX.md append (after line 221)

#### 7. Update print_dry_run
**File:** `scripts/zotero_ingest.py` (lines 234-251)
- [x] Replace `find_pdf_attachment()` with `resolve_pdf_info()`
- [x] Update header message (remove tag reference)
- [x] Show manifest context: total library items, already extracted, pending

### Validation

**Automated (syntax check):**
- [x] `uv run python -c "import sys; sys.path.insert(0, 'scripts'); import zotero_ingest"` — no import errors

**Manual (requires Zotero API):**
- [x] `--dry-run` lists items not in manifest (should show all except `PMXLGPKG`)
- [x] `--dry-run --limit 3` shows exactly 3 items
- [x] `--dry-run --tag new` shows only `new`-tagged items not in manifest
- [x] `--limit 1` extracts one item: manifest gets new entry, Zotero does NOT get `extracted` tag
- [x] Run `--limit 1` again: 0 items processed (idempotency)
- [x] `--sync-tags` tags all manifested items in Zotero
- [x] Delete source dir + remove manifest line → item reappears in `--dry-run`
- [x] `--local-pdf` still works without manifest interaction

**Spec Acceptance Criteria:**
- [x] SC-1: `--dry-run` diffs against manifest ✓ (test 1)
- [x] SC-2: `--limit 5` works ✓ (test 2)
- [x] SC-3: Standalone PDFs in pending list ✓ (test 1, if standalone exists)
- [x] SC-4: No `extracted` tag after extraction ✓ (test 4)
- [x] SC-5: `--sync-tags` adds tags ✓ (test 6)
- [x] SC-6: Delete + re-queue works ✓ (test 7)
- [x] SC-7: Idempotent ✓ (test 5)
- [x] SC-8: Existing source backward compatible ✓ (seed manifest)

**What We Know Works After This Phase:**
The full git-authoritative pipeline is operational. All spec acceptance criteria are validated.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Low risk — pure data functions with no API calls. Validate with REPL.
- **Phase 2**: Medium risk — standalone attachment API behavior is ambiguous. Mitigated by testing with `resolve_pdf_info()` against real library items before Phase 3 depends on it. If standalone items don't appear in `zot.top()`, adjust `fetch_all_processable_items()` to query them separately.
- **Phase 3**: Medium risk — largest change surface. Mitigated by `--dry-run` validation before any real extraction. The `--local-pdf` path is intentionally left untouched to avoid regression.

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- Created `knowledge/MANIFEST.jsonl` with seed entry for `PMXLGPKG`
- Added `import json` and `from datetime import date` to `scripts/zotero_lib.py`
- Added `MANIFEST_PATH` constant to `scripts/zotero_lib.py`
- Added `load_manifest()`, `manifest_keys()`, `append_manifest_entry()` to `scripts/zotero_lib.py`
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- Added `PdfInfo` NamedTuple to `scripts/zotero_lib.py` (after line 80)
- Added `resolve_pdf_info()` — handles both parent items and standalone attachments
- Added `download_pdf_from_info()` — downloads using PdfInfo, reuses skip-if-exists and SHA256 logic
- Kept `find_pdf_attachment()` and `download_pdf()` untouched for backward compat
**Issues:** None
**Deviations:** None

### Phase 3 Completion
**Completed:** 2026-02-09
**Actual Changes:**
- Updated module docstring to reflect new CLI
- Updated imports: added `append_manifest_entry`, `download_pdf_from_info`, `load_manifest`, `manifest_keys`, `resolve_pdf_info`, `MANIFEST_PATH`; removed `find_pdf_attachment`, `download_pdf` (no longer used directly)
- Added `--limit`, `--tag`, `--sync-tags` arguments to `parse_args()`
- Added `fetch_all_processable_items()` — fetches `zot.top()` + standalone PDF attachments
- Added `compute_pending_queue()` — filters by manifest keys
- Added `sync_tags_command()` — tags manifested items in Zotero
- Rewired `process_zotero_item()`: uses `resolve_pdf_info()` + `download_pdf_from_info()`, removed eager `tag_extracted()`, added `append_manifest_entry()` after successful extraction
- Rewired `print_dry_run()`: uses `resolve_pdf_info()`, shows manifest context (total/extracted/pending), labels standalone PDFs
- Rewired `main()`: `--sync-tags` early exit, manifest-based queue via `fetch_all_processable_items()` → `compute_pending_queue()`, optional `--tag` filter, optional `--limit`
- `process_local_pdf()` unchanged (no manifest interaction, as designed)
**Issues:** None
**Deviations:** None

---

**Status**: ~~Draft~~ → ~~In Progress~~ → **Complete**
