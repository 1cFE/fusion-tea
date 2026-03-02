# Design: Single-Source End-to-End Pipeline (KNOW-DB Item 2)

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-08 22:28 UTC
**Branch:** proj-modeling-0
**Commit:** a94c653

---

## Overview

Manual, step-by-step execution of the full knowledge pipeline: download one PDF from the 1cfe Zotero group library, extract it with `agentic-mbse extract --enhance`, register it in SOURCE_INDEX.md with extended metadata, tag the Zotero item as `extracted`, create LOCAL_SOURCES.yaml, and commit.

## Related Artifacts

- **Spec:** `.project/active/knowledge-database-integration/spec.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Research:** `.project/research/20260203-knowledge-database-architecture.md`
- **Item 1 Script:** `scripts/zotero_test.py`

---

## Research Findings

### Existing Codebase Analysis

**Item 1 script** (`scripts/zotero_test.py`):
- Uses `zotero.Zotero(LIBRARY_ID, "user", API_KEY)` — connects to the **personal user library**
- Reads `ZOTERO_ID` and `ZOTERO_KEY` from `.env` via `python-dotenv`
- Downloads via `zot.dump(child_key, filename, output_dir)` — proven working
- Cleans up test downloads (line 102) — we need to keep them
- No group library support — Item 2 needs `zotero.Zotero(5428393, 'group', API_KEY)`

**`.env` variables** (already exist):
- `ZOTERO_KEY` — API key (works for both user and group libraries)
- `ZOTERO_ID` — personal library ID (19065806)
- No `ZOTERO_GROUP_ID` yet

**`agentic-mbse extract` CLI** (`~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py`):
- Accepts: `path`, `--output`, `--index`, `--summarize`, `--enhance`, `--no-tables`, `--force`
- Produces: `full_document.md`, `INDEX.md` (if `--index`), `summary.json`, `images/`
- `summary.json` schema: `source_file`, `source_format`, `processed_at`, `backend_used`, `processing_completed`, `file_hash` (md5), `statistics` (total_images, total_characters, file_size_bytes), `error`
- Output dir sanitization: non-alphanumeric chars → underscores, truncated to 100 chars
- Does NOT update SOURCE_INDEX.md — that's our responsibility
- Does NOT read LOCAL_SOURCES.yaml — no toolchain consumer exists

**Project structure** (already in place):
- `knowledge/raw/` exists with `.gitignore` excluding `*.pdf` (created in Item 1)
- `knowledge/sources/` has one file: `COST_MODELING.md` (manually written, not in a subdirectory)
- `.gitignore` excludes `.env`
- `pyzotero>=1.10.0` and `python-dotenv>=1.2.1` already in `pyproject.toml`
- `agentic-mbse[extract-tables]` installed (gmft available for Layer 2)

**SOURCE_INDEX.md** current format:
- One entry: PyFECONS with 4 fields (Type, Location, Use for, Validation)
- Under `## Primary Sources` heading
- No checksums, Zotero keys, or extraction metadata

### Key Technical Facts

1. **Group vs user library API**: Only difference is second argument to `zotero.Zotero()` — `'group'` vs `'user'`. The same API key works for both (if it has group access permissions).
2. **Target document**: Item key `PMXLGPKG` — "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants"
3. **Tagging via pyzotero**: `zot.add_tags(item_key, 'extracted')` adds a tag to an item
4. **SHA256 computation**: Standard `hashlib.sha256(file_bytes).hexdigest()`
5. **Slug derivation**: The spec says "filesystem-safe, human-readable" — `agentic-mbse extract` auto-sanitizes to underscores/truncation, but we control `--output` so we choose the slug

---

## Proposed Design

This is a **manual, step-by-step process** — no new automation script. Each step is executed interactively. A download helper script bridges the gap between Zotero API and the extraction CLI.

### Component 1: Download Script (`scripts/zotero_group_download.py`)

**Purpose:** Connect to the 1cfe group library, find item `PMXLGPKG`, download its PDF attachment to `knowledge/raw/`, and print metadata needed for SOURCE_INDEX.md.

**Why a script (not just CLI commands):** pyzotero requires Python. The script is minimal and reusable for Item 3's automation work.

**Location:** `scripts/zotero_group_download.py`

**Behavior:**
1. Load `.env` for `ZOTERO_KEY`; hardcode group ID `5428393` (it's project-specific, not a secret)
2. Connect: `zotero.Zotero(5428393, 'group', api_key)`
3. Fetch item `PMXLGPKG` metadata via `zot.item(item_key)`
4. Find PDF attachment via `zot.children(item_key)` filtered by `contentType == 'application/pdf'`
5. Download: `zot.dump(child_key, filename, 'knowledge/raw/')` — keep the file (don't clean up)
6. Compute SHA256 of downloaded PDF
7. Print summary: filename, size, SHA256, title, Zotero key
8. Tag item as `extracted`: `zot.add_tags('PMXLGPKG', 'extracted')`

**Interface:**
```python
#!/usr/bin/env python3
"""Download a PDF from the 1cfe Zotero group library.

Usage:
    uv run python scripts/zotero_group_download.py PMXLGPKG
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-extracted
    uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only
"""
```

Arguments:
- `item_key` (positional, required): Zotero item key to download
- `--tag-extracted` (flag): Tag the item as `extracted` after successful download.
- `--tag-only` (flag): Skip download entirely, just tag the item as `extracted`. For use when the PDF has already been downloaded in a previous run.
- `--output-dir` (optional, default `knowledge/raw/`): Download destination

**Skip-if-exists behavior:** When not using `--tag-only`, the script checks if the PDF already exists in `--output-dir`. If it does, the download is skipped and the existing file's metadata is printed. This prevents unnecessary re-downloads on flaky networks.

**Output (stdout):**
```
Title: Techno-economic analysis of deuterium-tritium ...
Zotero Key: 5428393:PMXLGPKG
Filename: <actual-filename>.pdf
Size: X,XXX bytes
SHA256: <hex>
Saved to: knowledge/raw/<filename>.pdf
```

**Dependencies:** `pyzotero`, `python-dotenv`, `hashlib` (stdlib)

**Patterns reused from `scripts/zotero_test.py`:**
- `.env` loading via `dotenv` (line 24)
- PDF child discovery pattern (lines 53-56)
- `zot.dump()` download (line 89)
- SHA256 computation (line 95)

### Component 2: PDF Extraction (existing CLI)

**Purpose:** Run `agentic-mbse extract` on the downloaded PDF.

**No new code.** Execute interactively:

```bash
uv run agentic-mbse extract knowledge/raw/<filename>.pdf \
    --output knowledge/sources/tea_dt_mfe_cost_analysis/ \
    --index --summarize --enhance
```

**Slug choice:** `tea_dt_mfe_cost_analysis` — derived from the paper title "Techno-Economic Analysis of Deuterium-Tritium Magnetic confinement Fusion power plants". Filesystem-safe, human-readable, concise.

**Expected outputs:**
```
knowledge/sources/tea_dt_mfe_cost_analysis/
├── full_document.md
├── INDEX.md
├── summary.json
└── images/
```

### Component 3: SOURCE_INDEX.md Update (manual edit)

**Purpose:** Add a new entry with the 4 canonical fields plus extended metadata.

**Format evolution:** Add extended fields after the canonical 4, under a clear sub-heading. The existing PyFECONS entry remains unchanged.

**New entry structure:**
```markdown
### TEA D-T MFE Cost Analysis
- **Type**: documentation
- **Location**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Use for**: Techno-economic analysis methodology, D-T MFE cost breakdowns, LCOE calculation approach, fusion power plant economics
- **Validation**: Compare cost model structure and assumptions against this reference study

#### Extended Metadata
- **Zotero Key**: 5428393:PMXLGPKG
- **Raw SHA256**: <sha256 of source PDF>
- **Extracted Path**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Extract SHA256**: <sha256 of full_document.md>
- **Date Added**: 2026-02-08
```

**Placement:** Under `## Primary Sources`, after the existing PyFECONS entry.

**Note on `COST_MODELING.md`:** The existing `knowledge/sources/COST_MODELING.md` is a flat file predating the per-source subdirectory convention established by `agentic-mbse extract`. New extracted sources use subdirectories (`knowledge/sources/<slug>/`). The flat file is left as-is — no migration needed.

**Backward compatibility:** The 4 canonical fields (`Type`, `Location`, `Use for`, `Validation`) remain in exactly the same format. The `#### Extended Metadata` sub-heading creates a clear boundary. Toolchain parsers that only look for the 4 fields will ignore the extension.

### Component 4: LOCAL_SOURCES.yaml

**Purpose:** Establish the convention for machine-specific paths. Template file, gitignored.

**Location:** `knowledge/LOCAL_SOURCES.yaml`

**Content:**
```yaml
# LOCAL_SOURCES.yaml — Machine-specific paths for knowledge sources
#
# This file maps logical source names to their local filesystem paths.
# It is gitignored because paths vary by machine.
#
# STATUS: Convention only. No code currently reads this file.
# Future agentic-mbse releases may consume it. For now, it serves as
# documentation of where external sources live on this machine.
#
# To set up on a new machine:
#   1. Copy this template (or create fresh)
#   2. Fill in the paths for your local environment

# External codebases
pyfeconds:
  path: /path/to/PyFECONS  # Replace with your local path
  description: Python Fusion Energy Cost of Nuclear Systems

# Zotero configuration (API key is in .env, not here)
zotero:
  group_id: 5428393
  group_name: 1cfe
```

**Gitignore update:** Add `knowledge/LOCAL_SOURCES.yaml` to root `.gitignore`.

**What gets committed:** The `.gitignore` update (so other developers know the file is expected to be local). The template file itself is NOT committed — but a `knowledge/LOCAL_SOURCES.yaml.example` COULD be committed as a reference. However, the spec says the template itself should be gitignored, so we follow that.

### Component 5: Git Commit

**Staged files:**
- `scripts/zotero_group_download.py` (new)
- `knowledge/sources/tea_dt_mfe_cost_analysis/` (new directory, all files)
- `knowledge/SOURCE_INDEX.md` (modified)
- `.gitignore` (modified — LOCAL_SOURCES.yaml entry)

**NOT staged:**
- `.env` (already gitignored)
- `knowledge/raw/*.pdf` (already gitignored)
- `knowledge/LOCAL_SOURCES.yaml` (newly gitignored)

---

## Execution Sequence

```
1. Create scripts/zotero_group_download.py
2. Run: uv run python scripts/zotero_group_download.py PMXLGPKG
   → PDF downloaded to knowledge/raw/, metadata printed
3. Run: uv run agentic-mbse extract knowledge/raw/<filename>.pdf \
        --output knowledge/sources/tea_dt_mfe_cost_analysis/ \
        --index --summarize --enhance
   → Extracted markdown + INDEX.md + summary.json
4. Compute SHA256 of full_document.md
5. Edit knowledge/SOURCE_INDEX.md — add new entry with all metadata
6. Create knowledge/LOCAL_SOURCES.yaml
7. Add LOCAL_SOURCES.yaml to .gitignore
8. Run: uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only
   → Zotero item tagged (no re-download)
9. Spot-check extraction quality
10. Git commit
```

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Group library API permissions | Blocks download | The same API key should work if it has group read access. Test connectivity first before download. |
| Large/complex PDF causes extraction failure | Blocks pipeline | Use `--enhance` for best quality. If it fails, try without `--enhance` or with `--structure-only`. Document issues but don't block. |
| GMFT table extraction crashes on complex tables | Delays pipeline | Can use `--no-tables` to skip Layer 2. Tables will be lower quality but pipeline continues. |
| `zot.add_tags()` API differs from expected | Minor — tag not applied | Test separately. pyzotero docs confirm `add_tags(item_key, tag_string)` syntax. |
| Extraction quality poor (garbled equations, broken tables) | Acceptable — per spec, document issues but don't block | Spot-check output. File upstream issues against agentic-mbse if needed. |

## Integration Strategy

This is a **proof-of-concept** for the full knowledge pipeline architecture. The download script (`zotero_group_download.py`) will be superseded by the automation script in Item 3 (`zotero_ingest.py`), but the patterns established here (group library connection, slug naming, SOURCE_INDEX.md extended format, tagging convention) become the foundation.

The SOURCE_INDEX.md extended metadata format is designed to be forward-compatible: new entries use it, old entries don't need migration, and the canonical 4-field format is preserved for toolchain compatibility.

## Validation Approach

1. **Download verification:** File exists in `knowledge/raw/`, non-zero size, SHA256 computed
2. **Extraction verification:** `full_document.md` exists, >1000 chars, `INDEX.md` has sections, `summary.json` has `processing_completed: true`
3. **SOURCE_INDEX.md verification:** New entry has all 9 fields (4 canonical + 5 extended), PyFECONS entry unchanged
4. **Zotero tag verification:** Re-query item via API, confirm `extracted` tag present
5. **LOCAL_SOURCES.yaml verification:** File exists, is gitignored, contains documented fields
6. **Git verification:** `git status` shows no untracked secrets, no PDFs staged, all extraction outputs committed
7. **Quality spot-check:** Open `full_document.md`, verify document is readable and section structure makes sense

---

**Next Step:** After approval → `/_my_implement`
