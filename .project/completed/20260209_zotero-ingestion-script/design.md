# Design: Zotero Ingestion Automation Script (KNOW-DB Item 3)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-09 01:21 UTC
**Branch:** proj-modeling-0
**Commit:** 6fbb243

---

## Overview

A batch ingestion script (`scripts/zotero_ingest.py`) that queries the 1cfe Zotero group library for `new`-tagged items, downloads their PDFs, runs `agentic-mbse extract`, appends entries to SOURCE_INDEX.md, and tags items as `extracted`. Shares common logic with `scripts/zotero_group_download.py` via a new `scripts/zotero_lib.py` module.

## Related Artifacts

- **Spec:** `.project/active/zotero-ingestion-script/spec.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Research:** `.project/research/20260203-knowledge-database-architecture.md` (Section 8)
- **Item 2 Design:** `.project/active/knowledge-database-integration/design.md`
- **Download Script:** `scripts/zotero_group_download.py`
- **SOURCE_INDEX.md:** `knowledge/SOURCE_INDEX.md`

---

## Research Findings

### Existing Code Analysis

**`scripts/zotero_group_download.py`** (133 lines):
- Hardcodes `GROUP_ID = 5428393` (line 22)
- `get_api_key()` (line 48): loads `.env`, reads `ZOTERO_KEY`, exits on missing
- `find_pdf_attachment(zot, item_key)` (line 57): queries `zot.children()`, filters by `contentType == 'application/pdf'`, exits if none found
- `download_pdf(zot, item_key, output_dir)` (line 70): fetches item metadata, finds PDF child, downloads via `zot.dump()`, skips if file already exists, computes SHA256
- `tag_item(zot, item_key)` (line 104): fetches item, checks for existing `extracted` tag, calls `zot.add_tags(item, "extracted")`
- All error handling uses `sys.exit(1)` — not suitable for batch processing where we need to continue after failures

**Key reuse candidates** from this script:
- `get_api_key()` — identical in both scripts
- `find_pdf_attachment()` — same logic but needs to return `None` instead of `sys.exit(1)` for batch use
- `download_pdf()` — core download + skip-if-exists + SHA256, but prints to stdout and exits on error
- `tag_item()` — identical in both scripts
- `GROUP_ID` constant — same value

**`scripts/zotero_test.py`** (129 lines):
- Uses personal user library (`zotero.Zotero(LIBRARY_ID, "user", API_KEY)`) — different from group library
- Superseded by `zotero_group_download.py` for actual work. Not relevant for shared abstractions.

**`agentic-mbse extract` CLI** (from investigation):
- Exit codes: `0` (all succeeded), `1` (any failed)
- Python API available: `agentic_mbse.extraction.base.ExtractionResult` dataclass, backend-specific `extract()` functions
- However, the CLI also runs Layer 2 (GMFT tables), Layer 3 (structural repair), Layer 4 (quality repair), and `--index`/`--summarize` — these are orchestrated in `cmd_extract()` and not trivially callable as a single Python function
- **Recommendation: use subprocess** — the CLI is the stable public interface, handles all layer orchestration, and `--enhance` already wires up Layers 3+4. The Python API gives us individual backends but not the full pipeline.

**SOURCE_INDEX.md** current format (from Item 2):
- PyFECONS entry: 4 canonical fields under `### PyFECONS`
- TEA D-T MFE entry: 4 canonical fields + `#### Extended Metadata` sub-heading with 5 fields
- New entries go under `## Primary Sources`, appended after existing entries
- File ends with `## How MBSE Commands Use This File` and `### Adding More Sources` sections — new entries must be inserted BEFORE these sections

### pyzotero API Patterns (from existing code)

The existing `zotero_group_download.py` demonstrates all the pyzotero patterns we need:
- Connection: `zotero.Zotero(GROUP_ID, "group", api_key)` (line 119)
- Item fetch: `zot.item(item_key)` → dict with `data.title`, `data.tags` (line 72, 106)
- Children: `zot.children(item_key)` → list of attachment dicts (line 59)
- Download: `zot.dump(child_key, filename, output_dir)` (line 85)
- Tagging: `zot.add_tags(item, "extracted")` where `item` is the full dict (line 111)

For the batch query (new in Item 3):
- `zot.top(tag=['new', '-extracted'])` — pyzotero supports tag negation with `-` prefix
- `zot.everything(zot.top(...))` — paginates through all results (the research report Section 8 uses this pattern)

---

## Proposed Design

### Architecture

Three files, one new module:

```
scripts/
├── zotero_lib.py              # NEW — shared Zotero utilities
├── zotero_group_download.py   # MODIFIED — imports from zotero_lib
└── zotero_ingest.py           # NEW — batch ingestion script
```

### Component 1: `scripts/zotero_lib.py` (Shared Module)

Extracts common logic from `zotero_group_download.py` into reusable functions. All functions return values or raise exceptions instead of calling `sys.exit()`.

```python
GROUP_ID = 5428393
RAW_DIR = Path("knowledge/raw")
SOURCES_DIR = Path("knowledge/sources")
SOURCE_INDEX_PATH = Path("knowledge/SOURCE_INDEX.md")

def load_api_key() -> str:
    """Load ZOTERO_KEY from .env. Raises ValueError if missing."""

def connect(api_key: str) -> zotero.Zotero:
    """Return a pyzotero client for the 1cfe group library."""

def find_pdf_attachment(zot, item_key: str) -> dict | None:
    """Find first PDF child attachment. Returns None if no PDF found."""

class DownloadResult(NamedTuple):
    path: Path
    sha256: str
    title: str

def download_pdf(zot, item_key: str, output_dir: Path) -> DownloadResult:
    """Download PDF, return DownloadResult. Skips if file already exists.
    Raises RuntimeError on download failure."""

def sha256_of(path: Path) -> str:
    """Compute SHA256 hex digest of a file."""

def tag_extracted(zot, item_key: str) -> None:
    """Tag a Zotero item as 'extracted'. Skips if already tagged."""

def slugify(title: str, max_len: int = 60) -> str:
    """Convert title to filesystem-safe slug.
    Lowercase, spaces/non-alnum → underscores, collapse runs, strip edges."""
```

**Design notes:**
- `find_pdf_attachment` returns `None` instead of exiting — lets callers decide how to handle (skip in batch, exit in single-item)
- `download_pdf` raises `RuntimeError` on failure — callers can catch or let propagate
- `slugify` is new — the existing code didn't need it (slugs were hand-chosen in Item 2)

### Component 2: `scripts/zotero_group_download.py` (Refactored)

Refactored to import from `zotero_lib`. Same CLI interface, same behavior. The only change is replacing inline functions with imports.

```python
from zotero_lib import load_api_key, connect, find_pdf_attachment, download_pdf, tag_extracted, GROUP_ID

def main():
    args = parse_args()
    api_key = load_api_key()
    zot = connect(api_key)

    if args.tag_only:
        tag_extracted(zot, args.item_key)
        return

    pdf_child = find_pdf_attachment(zot, args.item_key)
    if pdf_child is None:
        print(f"ERROR: No PDF attachment found for item {args.item_key}")
        sys.exit(1)

    filepath, sha256, title = download_pdf(zot, args.item_key, Path(args.output_dir))
    # ... print metadata as before ...

    if args.tag_extracted:
        tag_extracted(zot, args.item_key)
```

Key: the script preserves its `sys.exit(1)` behavior for single-item errors, while the shared functions underneath are batch-friendly.

### Component 3: `scripts/zotero_ingest.py` (New)

The main deliverable. CLI entry point for batch ingestion.

**CLI Interface:**

```
uv run python scripts/zotero_ingest.py [OPTIONS]

Options:
  --dry-run           List pending items without processing
  --local-pdf PATH    Process a local PDF (bypass Zotero query)
  --no-enhance        Disable --enhance (use basic extraction only)
  --output-dir DIR    Override raw PDF download dir (default: knowledge/raw/)
```

**Main flow:**

```python
def main():
    args = parse_args()

    if args.local_pdf:
        process_local_pdf(args)
        return

    api_key = load_api_key()
    zot = connect(api_key)

    # Smart pull: items tagged 'new' but NOT 'extracted'
    items = zot.everything(zot.top(tag=["new", "-extracted"]))

    if args.dry_run:
        print_dry_run(zot, items)
        return

    stats = {"found": len(items), "extracted": 0, "skipped": 0, "failed": 0}

    for item in items:
        result = process_zotero_item(zot, item, args)
        stats[result] += 1

    print_summary(stats)
```

**`process_zotero_item(zot, item, args) -> str`:**

Returns one of `"extracted"`, `"skipped"`, `"failed"`.

```
1. Get title, item_key from item["data"]
2. Find PDF attachment → if None, log warning, return "skipped"
3. Download PDF to knowledge/raw/ (skip-if-exists)
4. Generate slug from title via slugify()
5. Resolve slug collision (check if knowledge/sources/<slug>/ exists → append _<item_key>)
6. Run extraction via subprocess:
     uv run agentic-mbse extract <pdf> \
       --output knowledge/sources/<slug>/ \
       --index --summarize --enhance
   Check return code. On failure → log error, return "failed"
7. Compute SHA256 of full_document.md
8. Append SOURCE_INDEX.md entry
9. Tag item as 'extracted' in Zotero
10. Return "extracted"
```

Each step that can fail is wrapped in try/except. Failures at steps 3-6 return `"failed"`. The script continues to the next item.

**`process_local_pdf(args)`:**

Handles `--local-pdf <path>`:
```
1. Verify file exists
2. Derive slug from filename (stem, slugified)
3. Resolve slug collision (append numeric suffix: _2, _3, ...)
4. Copy PDF to knowledge/raw/ if not already there
5. Run extraction (same subprocess call)
6. Compute checksums
7. Append SOURCE_INDEX.md entry (no Zotero key, no tag update)
8. Print summary: 1 found, 1 extracted (or 1 failed)
```

**`append_source_index_entry(...)`:**

Appends a new entry to SOURCE_INDEX.md. The function:
1. Reads the file
2. Finds the insertion point — before `## How MBSE Commands Use This File` (or at end of file if that heading doesn't exist)
3. Inserts the entry block

Entry template for Zotero sources:
```markdown

### <Title>
- **Type**: documentation
- **Location**: knowledge/sources/<slug>/
- **Use for**:
- **Validation**:

#### Extended Metadata
- **Zotero Key**: 5428393:<item_key>
- **Raw SHA256**: <pdf_sha256>
- **Extracted Path**: knowledge/sources/<slug>/
- **Extract SHA256**: <full_document_sha256>
- **Date Added**: <YYYY-MM-DD>
```

Entry template for local PDFs (no Zotero key):
```markdown

### <Title derived from filename>
- **Type**: documentation
- **Location**: knowledge/sources/<slug>/
- **Use for**:
- **Validation**:

#### Extended Metadata
- **Raw SHA256**: <pdf_sha256>
- **Extracted Path**: knowledge/sources/<slug>/
- **Extract SHA256**: <full_document_sha256>
- **Date Added**: <YYYY-MM-DD>
```

**`print_dry_run(zot, items)`:**

Lists each item with title, key, and PDF filename (fetched via `find_pdf_attachment`). Marks items with no PDF as "(no PDF — will skip)".

**`print_summary(stats)`:**

```
Summary: 5 found, 3 extracted, 1 skipped (no PDF), 1 failed
```

### Extraction: subprocess vs. Python API

The `agentic-mbse extract` CLI orchestrates a 4-layer pipeline (base extraction, GMFT tables, structural repair, quality repair) plus `--index` and `--summarize`. The Python API exposes individual backends (`docling_backend.extract()`) but not the full orchestration.

**Decision: use subprocess.** The CLI is the stable public interface and handles all layer orchestration. Calling it via subprocess:

```python
cmd = [
    "uv", "run", "agentic-mbse", "extract", str(pdf_path),
    "--output", str(output_dir),
    "--index", "--summarize",
]
if not args.no_enhance:
    cmd.append("--enhance")

result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
if result.returncode != 0:
    # extraction failed
```

`--enhance` is included by default. When `--no-enhance` is passed (`argparse` `store_true`), the flag is omitted from the subprocess command, falling back to basic extraction (Layer 1 only + Layer 2 GMFT tables).

The 900-second timeout gives generous headroom over the CLI's internal 600-second default.

### Slug Generation

```python
import re

def slugify(title: str, max_len: int = 60) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)  # non-alnum → underscore
    slug = re.sub(r"_+", "_", slug)            # collapse runs
    slug = slug.strip("_")                     # strip edges
    return slug[:max_len]
```

Example: "Techno-Economic Analysis of Deuterium-Tritium Magnetic Confinement Fusion Power Plants" → `techno_economic_analysis_of_deuterium_tritium_magnetic_confi`

Collision resolution:
- Zotero items: append `_<item_key>` (e.g., `techno_economic_..._PMXLGPKG`)
- Local PDFs: append `_2`, `_3`, etc.

### SOURCE_INDEX.md Insertion Logic

The current file structure is:

```markdown
# Source Index                          ← file start
...
## Primary Sources                      ← entries go under here
### PyFECONS                            ← existing entry
...
### TEA D-T MFE Cost Analysis           ← existing entry (from Item 2)
...
                                        ← INSERT NEW ENTRIES HERE
## How MBSE Commands Use This File      ← marker for insertion point
...
```

The insertion function:
1. Reads the full file as a string
2. Searches for `\n## How MBSE Commands Use This File` as the boundary
3. If found: inserts the new entry block before that line
4. If not found: appends to end of file
5. Writes the file back

This is simple string manipulation — no markdown parser needed.

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| pyzotero `tag=['new', '-extracted']` negation syntax doesn't work as expected | Blocks smart pull | The research report documents this syntax and it's from pyzotero docs. Test in dry-run mode first. Fallback: query all `new`-tagged items and filter in Python. |
| `agentic-mbse extract --enhance` fails on some PDFs | Single item fails, batch continues | Error handling catches subprocess failure, logs it, skips to next item. User can re-run with `--no-enhance` or process individually. |
| SOURCE_INDEX.md insertion point not found (file format changed) | Entry appended to wrong location | The `## How MBSE Commands Use This File` heading is a stable marker. If not found, append to end (safe default). Log a warning. |
| Concurrent edits to SOURCE_INDEX.md | Corruption | Not a real risk — single-user, single-process script. |
| Zotero API rate limits during large batch | Slows down or blocks | pyzotero handles rate limiting internally. Batch sizes of <20 items (Item 4 scope) are well within limits. |
| Slug collision with existing manually-created directories | Directory overwrite | Collision check runs before extraction. Zotero key suffix ensures uniqueness. |

## Integration Strategy

- `zotero_ingest.py` is the primary tool going forward for adding sources to the knowledge base
- `zotero_group_download.py` remains useful for one-off downloads or debugging (e.g., downloading a specific item without extracting)
- Both share `zotero_lib.py` — changes to connection logic or tagging behavior propagate to both
- `zotero_test.py` (Item 1 de-risk) is not modified — it uses the personal library and serves a different purpose

## Validation Approach

1. **Dry-run test**: `uv run python scripts/zotero_ingest.py --dry-run` — should list pending items without side effects
2. **Single-item batch**: Tag one Zotero item as `new`, run the script, verify the full pipeline (download, extract, SOURCE_INDEX.md, tag)
3. **No-PDF handling**: Create a Zotero item with no PDF attachment, tag it `new`, verify it's skipped with a warning
4. **Local PDF**: Run `--local-pdf` on a known PDF, verify extraction and SOURCE_INDEX.md entry (no Zotero fields)
5. **Re-run idempotency**: Run the script again — already-tagged items should not appear in the query, already-downloaded PDFs should be skipped
6. **`zotero_group_download.py` regression**: Run the existing download script to confirm it still works after refactoring to use `zotero_lib.py`

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`
