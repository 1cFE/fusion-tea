# Design: Ingestion Workflow V2 — Git-Authoritative Pipeline

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-09 15:52 UTC
**Branch:** proj-modeling-0
**Commit:** 1a4d8c0

---

## Overview

Refactor `scripts/zotero_ingest.py` and `scripts/zotero_lib.py` to replace the Zotero-tag-based queue with a git-authoritative manifest. The script determines "pending" items by diffing the Zotero library against a JSON manifest file, defers Zotero tagging to a separate explicit step, and adds support for standalone PDF attachments and batch size control.

## Related Artifacts

- **Spec:** `.project/active/ingestion-workflow-v2/spec.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md` — extends Item 3
- **Current Script:** `scripts/zotero_ingest.py`
- **Shared Library:** `scripts/zotero_lib.py`
- **SOURCE_INDEX.md:** `knowledge/SOURCE_INDEX.md`
- **Blocked Work:** `.project/active/first-corpus-ingestion/` (Item 4, waiting on this)

---

## Research Findings

### Existing Codebase Analysis

**`scripts/zotero_ingest.py`** (351 lines):
- Queue mechanism: `zot.top(tag=["new", "-extracted"])` — requires manual `new` tag (line 334)
- Eager tagging: `tag_extracted()` called in `process_zotero_item()` step 9 (line 224) — before commit
- No manifest file — no machine-readable record of what's been extracted
- No batch size control
- Supports `--dry-run`, `--local-pdf`, `--no-enhance`, `--output-dir`
- `append_source_index_entry()` (line 129) inserts before the "How MBSE Commands Use This File" marker
- `resolve_slug()` (line 113) handles collision by appending `_<item_key>` for Zotero items

**`scripts/zotero_lib.py`** (116 lines):
- Constants: `GROUP_ID = 5428393`, `RAW_DIR`, `SOURCES_DIR`, `SOURCE_INDEX_PATH`
- Key functions: `connect()`, `find_pdf_attachment()`, `download_pdf()`, `tag_extracted()`, `slugify()`, `sha256_of()`
- `find_pdf_attachment()` (line 36) looks for PDF children of a parent item — does NOT handle standalone attachments where the item itself is the PDF
- `download_pdf()` (line 54) fetches parent item metadata then downloads the child — needs adaptation for standalone attachments
- `tag_extracted()` (line 89) adds the `extracted` tag to an item

**pyzotero API patterns**:
- `zot.top()` returns top-level items (parent items, NOT standalone attachments)
- `zot.items()` returns ALL items including child attachments — but this is too broad
- `zot.everything(zot.top())` handles pagination automatically
- Standalone attachments (`itemType == 'attachment'` with no `parentItem`) may or may not appear in `zot.top()` — the Zotero API behavior for standalone attachments in `top()` is ambiguous
- Safest approach: fetch with `zot.top()` for parent items, then also query for standalone attachments separately

**SOURCE_INDEX.md** (61 lines):
- Currently has 2 sources: PyFECONS (codebase reference) and TEA D-T MFE cost analysis (extracted)
- Extended metadata block includes: Zotero Key, Raw SHA256, Extracted Path, Extract SHA256, Date Added
- Insertion point: before `## How MBSE Commands Use This File` marker

### Manifest Format Research

The spec requires a machine-readable manifest tracking extracted items. Key considerations:
- Must be git-friendly (diffs should be readable)
- Must be easy to parse programmatically
- Must support manual editing (removing entries to re-queue)
- JSON is standard but merge conflicts can be painful with arrays
- JSONL (one JSON object per line) is merge-friendly, append-only, and easy to parse
- YAML would also work but adds a dependency for writing (reading is fine with PyYAML)

---

## Design Decision: Manifest Format

**Context**: The manifest must be machine-readable, git-friendly, and manually editable. The spec mentions JSON merge conflicts as a consideration.

**Options considered**:

### Option A: Single JSON file (array of objects)
```json
[
  {"zotero_key": "PMXLGPKG", "slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE...", "date_extracted": "2026-02-08"}
]
```
- **Pro**: Standard, easy to parse, pretty-printable
- **Con**: Array-level merge conflicts when two branches add entries (the closing `]` conflicts)
- **Con**: Entire file must be read/written for each update

### Option B: JSON file (object keyed by Zotero key)
```json
{
  "PMXLGPKG": {"slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE...", "date_extracted": "2026-02-08"}
}
```
- **Pro**: O(1) lookup by key, natural dedup
- **Con**: Same closing `}` merge conflict issue
- **Pro**: Slightly better mergeability since entries are on distinct lines

### Option C: JSONL (one JSON object per line) — Recommended
```
{"zotero_key": "PMXLGPKG", "slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE...", "date_extracted": "2026-02-08"}
{"zotero_key": "7E42ICWG", "slug": "helios_stellarator", "title": "Helios...", "date_extracted": "2026-02-09"}
```
- **Pro**: Append-only — new entries are new lines, no structural conflicts
- **Pro**: Git merges are trivial (each branch adds different lines at the end)
- **Pro**: Easy to parse: `[json.loads(line) for line in f if line.strip()]`
- **Pro**: Easy to manually edit: delete a line to re-queue
- **Pro**: No external dependencies (just `json` stdlib)
- **Con**: Not as pretty as formatted JSON, but this is a machine file

**Recommendation**: **Option C (JSONL)** — best merge characteristics and append-only semantics match the use case perfectly. The manifest is primarily machine-read, and JSONL eliminates the main risk (merge conflicts on concurrent branch work).

---

## Proposed Design

### Architecture Overview

```
Zotero API                          Git Repository
┌─────────────┐                     ┌─────────────────────────────┐
│ All items    │──── fetch ────────▶│ Compare against manifest    │
│ (top-level + │                    │                             │
│  standalone) │                    │ knowledge/                  │
└─────────────┘                    │   MANIFEST.jsonl  ◄── source of truth
                                    │   sources/<slug>/           │
                                    │   SOURCE_INDEX.md           │
                                    └─────────────────────────────┘

Pipeline: fetch all → diff against manifest → download → extract → update manifest + SOURCE_INDEX
Tagging: separate --sync-tags step AFTER user commits
```

### Component 1: Manifest File (`knowledge/MANIFEST.jsonl`)

**Purpose**: Machine-readable record of all successfully extracted Zotero items.

**Location**: `knowledge/MANIFEST.jsonl` (git-tracked, committed alongside sources)

**Schema** (one JSON object per line):
```json
{"zotero_key": "PMXLGPKG", "slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE Cost Analysis", "date_extracted": "2026-02-08"}
```

Fields:
- `zotero_key` (string): Zotero item key (e.g., `"PMXLGPKG"`)
- `slug` (string): Directory name under `knowledge/sources/`
- `title` (string): Human-readable title from Zotero metadata or filename
- `date_extracted` (string): ISO date when extraction was performed

**New functions in `zotero_lib.py`**:

```python
MANIFEST_PATH = Path("knowledge/MANIFEST.jsonl")

def load_manifest() -> dict[str, dict]:
    """Load manifest as {zotero_key: entry_dict}. Returns empty dict if file missing."""

def append_manifest_entry(zotero_key: str, slug: str, title: str) -> None:
    """Append a single entry to MANIFEST.jsonl."""

def manifest_keys() -> set[str]:
    """Return set of Zotero keys present in the manifest. Fast path for queue diffing."""
```

### Component 2: Git-Authoritative Queue (`zotero_lib.py`)

**Purpose**: Determine pending items by diffing Zotero library against manifest.

**New function in `zotero_lib.py`**:

```python
def fetch_all_processable_items(zot) -> list[dict]:
    """Fetch all Zotero items that could be processed.

    Returns parent items with PDF children AND standalone PDF attachments.
    Combines zot.top() (parent items) with a filtered zot.items() call
    for standalone attachments (itemType='attachment', no parentItem,
    contentType='application/pdf').
    """
```

**Queue logic in `zotero_ingest.py`**:

```python
def compute_pending_queue(all_items: list[dict], manifest_keys: set[str]) -> list[dict]:
    """Filter items to those not in the manifest.
    Returns items whose Zotero key is NOT in manifest_keys."""
```

The existing `tag=["new", "-extracted"]` filter is removed from the default path. An optional `--tag <tag>` flag is added to allow selective filtering (e.g., `--tag new` to only process items with a specific tag, for backward compatibility or selective batching).

### Component 3: Standalone Attachment Support (`zotero_lib.py`)

**Purpose**: Handle top-level items where `itemType == 'attachment'` and `contentType == 'application/pdf'`.

**Changes to `find_pdf_attachment()`** — rename/refactor to `resolve_pdf_info()`:

```python
class PdfInfo(NamedTuple):
    """Resolved PDF information for download."""
    child_key: str       # Key of the attachment item to download
    filename: str        # Original filename
    title: str           # Best available title
    is_standalone: bool  # True if top-level attachment (no parent)

def resolve_pdf_info(zot, item: dict) -> PdfInfo | None:
    """Resolve PDF download info for any item type.

    For parent items (journalArticle, book, etc.):
        - Look up children, find first PDF attachment
        - Use parent's title

    For standalone attachments (itemType='attachment'):
        - The item itself is the PDF
        - Use filename (cleaned up) as title if no better metadata

    Returns None if no PDF is available.
    """
```

**Changes to `download_pdf()`**:

The current `download_pdf()` fetches the parent item to get the title, then finds the PDF child. For standalone attachments, the item IS the PDF — no child lookup needed. The function signature changes to accept `PdfInfo` instead of doing its own resolution:

```python
def download_pdf(zot, pdf_info: PdfInfo, output_dir: Path) -> DownloadResult:
    """Download PDF using resolved PdfInfo. Skips if file already exists."""
```

### Component 4: Deferred Zotero Tagging (`zotero_ingest.py`)

**Purpose**: Remove eager `extracted` tagging from the extraction pipeline. Provide a separate `--sync-tags` command.

**Changes**:
1. **Remove** the `tag_extracted()` call from `process_zotero_item()` (currently line 224)
2. **Add** `--sync-tags` flag to the argparser
3. **Add** `sync_tags()` function:

```python
def sync_tags(zot, manifest: dict[str, dict]) -> None:
    """Tag all manifest items as 'extracted' in Zotero.

    For each entry in the manifest, check if the Zotero item already
    has the 'extracted' tag. If not, add it. This is idempotent.
    """
```

When `--sync-tags` is passed, the script loads the manifest, compares against Zotero tags, and updates only items that are in the manifest but not yet tagged. This makes Zotero tags a downstream reflection of git state.

### Component 5: Batch Size Control (`zotero_ingest.py`)

**Purpose**: Limit how many items are processed per run.

**Changes**: Add `--limit N` flag to argparser. Apply after computing the pending queue:

```python
if args.limit:
    pending = pending[:args.limit]
```

### Component 6: Updated CLI Interface

```
# Default: process all unmanifested items
uv run python scripts/zotero_ingest.py

# Dry run: show what would be processed
uv run python scripts/zotero_ingest.py --dry-run

# Limit batch size
uv run python scripts/zotero_ingest.py --limit 5

# Filter by tag (optional, for selective processing)
uv run python scripts/zotero_ingest.py --tag new

# Sync Zotero tags to match manifest (after committing)
uv run python scripts/zotero_ingest.py --sync-tags

# Process a local PDF (unchanged)
uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/some_paper.pdf

# Disable enhance (unchanged)
uv run python scripts/zotero_ingest.py --no-enhance
```

### Component 7: Seed Manifest with Existing Source

The existing `tea_dt_mfe_cost_analysis` source (Zotero key `PMXLGPKG`) was extracted before the manifest existed. The implementation must seed `MANIFEST.jsonl` with this entry so it isn't re-processed:

```json
{"zotero_key": "PMXLGPKG", "slug": "tea_dt_mfe_cost_analysis", "title": "TEA D-T MFE Cost Analysis", "date_extracted": "2026-02-08"}
```

This is a one-time manual step during implementation (or an `--init-manifest` helper, but manual is fine for one entry).

---

## File Change Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `knowledge/MANIFEST.jsonl` | **New** | Git-authoritative manifest (JSONL format) |
| `scripts/zotero_lib.py` | **Modify** | Add manifest functions, `MANIFEST_PATH`, refactor `find_pdf_attachment()` → `resolve_pdf_info()`, adapt `download_pdf()` |
| `scripts/zotero_ingest.py` | **Modify** | Replace tag-based queue with manifest diff, add `--limit`, `--sync-tags`, `--tag`, remove eager tagging, update `process_zotero_item()` and `print_dry_run()` |

No other files are modified. SOURCE_INDEX.md format and `append_source_index_entry()` are unchanged.

---

## Detailed Implementation Notes

### `zotero_lib.py` changes

**New constant** (after existing constants at line 19):
```python
MANIFEST_PATH = Path("knowledge/MANIFEST.jsonl")
```

**New functions** (after existing functions):
- `load_manifest()` — reads JSONL, returns `{zotero_key: entry_dict}`
- `manifest_keys()` — returns `set[str]` of keys (convenience wrapper)
- `append_manifest_entry()` — appends one line to MANIFEST.jsonl
- `resolve_pdf_info()` — replaces `find_pdf_attachment()` for the queue logic

**Refactored `find_pdf_attachment()`**: Keep the existing function for backward compatibility (it's used in `zotero_group_download.py` at line 69), but add `resolve_pdf_info()` as the new primary interface used by the ingest script.

**Adapted `download_pdf()`**: Change signature to accept `PdfInfo` (or keep flexible with optional `pdf_info` parameter). For standalone attachments, the download key is the item itself, not a child.

### `zotero_ingest.py` changes

**`parse_args()`** — add:
- `--limit` (int, optional)
- `--sync-tags` (store_true)
- `--tag` (string, optional) — filter to items with this tag (replaces hardcoded `new`)

**`main()`** — replace the tag-based query block (lines 333-335):
```python
# OLD: items = zot.everything(zot.top(tag=["new", "-extracted"]))
# NEW:
all_items = fetch_all_processable_items(zot)
known_keys = manifest_keys()
pending = compute_pending_queue(all_items, known_keys)
if args.tag:
    pending = [i for i in pending if args.tag in [t["tag"] for t in i["data"].get("tags", [])]]
if args.limit:
    pending = pending[:args.limit]
```

**`process_zotero_item()`** — changes:
1. Use `resolve_pdf_info()` instead of `find_pdf_attachment()` (lines 182-185)
2. Adapt download call to use PdfInfo
3. **Remove** `tag_extracted()` call (line 224-228)
4. **Add** `append_manifest_entry()` call after successful extraction + SOURCE_INDEX append
5. The manifest entry is written to disk immediately (append to file), so if the script crashes mid-batch, completed items are recorded

**`print_dry_run()`** — update to use `resolve_pdf_info()` instead of `find_pdf_attachment()`, and show the manifest diff context (how many total vs. how many already extracted vs. how many pending).

**New `sync_tags_command()`**:
```python
def sync_tags_command(zot) -> None:
    manifest = load_manifest()
    for key, entry in manifest.items():
        try:
            tag_extracted(zot, key)
        except Exception as e:
            print(f"  WARNING: Failed to tag {key}: {e}")
```

### Idempotency (FR-6)

The pipeline is naturally idempotent because:
1. **Manifest check**: Items already in MANIFEST.jsonl are excluded from the queue
2. **SOURCE_INDEX.md**: Only appended during extraction — if item is in manifest, extraction is skipped, so no duplicate append
3. **File existence**: `download_pdf()` already skips existing files (line 72 of `zotero_lib.py`)
4. **Manifest append**: Only called on successful new extraction — never for already-manifested items

### Standalone Attachment Handling

The key insight is that standalone attachments in Zotero have:
- `itemType: "attachment"`
- `contentType: "application/pdf"`
- No `parentItem` field (or `parentItem: false`)
- The `key` of the item IS the download key (no child lookup)

`fetch_all_processable_items()` must handle both:
1. Regular items from `zot.top()` — then check children for PDFs
2. Standalone attachments — found by fetching `zot.items(itemType='attachment')` and filtering to those with `contentType == 'application/pdf'` and no `parentItem`

To avoid excessive API calls, the implementation can:
- Fetch `zot.everything(zot.top())` for parent items
- Then fetch `zot.everything(zot.items(itemType='attachment'))` filtered to standalone PDFs
- This is 2 paginated API calls regardless of library size

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Standalone attachments not appearing in `zot.top()` or `zot.items()` as expected | Medium — 6 items would be silently skipped | Test with a known standalone attachment during implementation. Fall back to `zot.items()` unfiltered + local filtering if API doesn't support `itemType` filter. |
| JSONL manifest corruption (partial write on crash) | Low — append-only is atomic at OS level for small writes | Each append is a single `write()` + `flush()`. Even if truncated, all prior lines are intact. |
| Large library size causing slow API responses | Low — 150 items is small | `zot.everything()` handles pagination. Two paginated calls is fine for this scale. |
| `--sync-tags` running before commit | Low — user error, easily recoverable | Document in help text: "Run after committing extracted sources." Tags are additive and idempotent — no data loss. |
| Backward compatibility with `zotero_group_download.py` | Low — it uses `find_pdf_attachment()` directly | Keep `find_pdf_attachment()` as-is; add `resolve_pdf_info()` as new function. No breaking changes. |

---

## Integration Strategy

- **Replaces**: Tag-based queue mechanism (`tag=["new", "-extracted"]`)
- **Preserves**: `--local-pdf` path (unchanged — local PDFs don't have Zotero keys and don't go in the manifest), `--no-enhance`, `--output-dir`, `append_source_index_entry()`, `resolve_slug()`, `run_extraction()`
- **Preserves**: `zotero_group_download.py` — uses `find_pdf_attachment()` directly, no changes needed
- **Unblocks**: `.project/active/first-corpus-ingestion/` (Item 4) — can run immediately after this ships
- **Existing `extracted` tags in Zotero**: Left as-is (out of scope per spec). The manifest is seeded with the one existing extraction (`PMXLGPKG`). Future `--sync-tags` runs will tag new items but won't touch old ones.

---

## Validation Approach

### Manual Testing

1. **Seed manifest**: Create `MANIFEST.jsonl` with existing `PMXLGPKG` entry
2. **Dry run**: `uv run python scripts/zotero_ingest.py --dry-run` — verify it lists items NOT in manifest (should show all Zotero items except `PMXLGPKG`)
3. **Limit**: `uv run python scripts/zotero_ingest.py --dry-run --limit 3` — verify only 3 shown
4. **Tag filter**: `uv run python scripts/zotero_ingest.py --dry-run --tag new` — verify only `new`-tagged items shown
5. **Extract one**: `uv run python scripts/zotero_ingest.py --limit 1` — verify extraction works, manifest updated, Zotero NOT tagged
6. **Idempotency**: Run same command again — verify 0 items processed
7. **Re-queue**: Delete the source directory + remove manifest line, run `--dry-run` — verify item reappears
8. **Sync tags**: `uv run python scripts/zotero_ingest.py --sync-tags` — verify Zotero items in manifest now have `extracted` tag
9. **Standalone PDF**: If a standalone attachment exists in the library, verify it appears in `--dry-run` and can be processed
10. **Local PDF**: `uv run python scripts/zotero_ingest.py --local-pdf <path>` — verify still works (no manifest interaction)

### Acceptance Criteria Mapping

| Spec Acceptance Criterion | Validated By |
|---------------------------|-------------|
| `--dry-run` lists pending by diffing against manifest | Test 2 |
| `--limit 5` processes at most 5 items | Test 3 |
| Standalone PDFs appear in pending list | Test 9 |
| After extraction, Zotero items do NOT have `extracted` tag | Test 5 |
| After commit + `--sync-tags`, items DO have `extracted` tag | Test 8 |
| Deleting source dir + manifest entry re-queues item | Test 7 |
| Running twice processes 0 items second time | Test 6 |
| Existing source continues to work | Test 1 (seed manifest) |

---

Next Step: After approval → `/_my_implement`
