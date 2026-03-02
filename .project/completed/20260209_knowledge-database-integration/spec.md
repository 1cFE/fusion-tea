# Spec: Single-Source End-to-End Pipeline (KNOW-DB Item 2)

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-08 22:25 UTC
**Complexity:** MEDIUM
**Branch:** proj-modeling-0
**Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 2

---

## Business Goals

### Why This Matters

The fusion-tea knowledge base has zero machine-extracted sources. The only entry in `knowledge/sources/` is `COST_MODELING.md`, which was manually written. The extraction pipeline (`agentic-mbse extract`) is merged and available but has never been used in this project. The Zotero API connectivity was proven in Item 1, but only against the personal user library — the project's documents live in the **1cfe group library**.

This item proves the full architecture works end-to-end on a real fusion document before investing in automation (Item 3) or bulk ingestion (Item 4).

### Success Criteria

- [ ] One real fusion PDF downloaded from the 1cfe Zotero group library to `knowledge/raw/`
- [ ] `agentic-mbse extract` produces structured markdown in `knowledge/sources/<slug>/`
- [ ] SOURCE_INDEX.md has a new entry with Zotero metadata, checksums, and extraction path
- [ ] Zotero item is tagged `extracted` via API
- [ ] LOCAL_SOURCES.yaml template exists (gitignored) for machine-specific paths
- [ ] All extracted content committed to git

### Priority

P1 — gates Items 3 and 4. Strictly sequential within the KNOW-DB epic.

---

## Problem Statement

### Current State

- `knowledge/sources/` has 1 manually-written file (`COST_MODELING.md`)
- SOURCE_INDEX.md has 1 entry (PyFECONS codebase) in the base 4-field format — no checksums, Zotero keys, or extraction metadata
- Item 1 de-risk script (`scripts/zotero_test.py`) connects to the **user** library — the project's documents are in the **1cfe group library** (id=5428393), which is a different API call
- `knowledge/LOCAL_SOURCES.yaml` does not exist — machine-specific paths (e.g., PyFECONS at `/home/reid/PyFECONS`) are hardcoded in SOURCE_INDEX.md
- No code reads LOCAL_SOURCES.yaml — it is a proposed pattern from the research document with no toolchain consumer yet
- `gmft` is now installed (`agentic-mbse[extract-tables]`), so Layer 2 table extraction is available

### Desired Outcome

One complete end-to-end proof: Zotero group library download → `agentic-mbse extract` with `--enhance` → SOURCE_INDEX.md registration with extended metadata → Zotero tag update → git commit. Plus a LOCAL_SOURCES.yaml template establishing the pattern for machine-specific configuration.

---

## Scope

### In Scope

1. **Zotero group library download** — connect to 1cfe group (id=5428393), download one PDF
2. **PDF extraction** — run `agentic-mbse extract` with full enhancement pipeline
3. **SOURCE_INDEX.md evolution** — extend the existing format with new metadata fields
4. **Zotero state update** — tag processed item as `extracted` via API
5. **LOCAL_SOURCES.yaml** — create template with `.gitignore` entry; document purpose and intended evolution
6. **Git commit** — stage and commit all artifacts

### Out of Scope

- Batch processing or automation scripting (Item 3)
- Ingesting multiple sources (Item 4)
- SRC-XXX source ID system (no toolchain support exists — defer)
- Changes to agentic-mbse toolchain itself
- Fixing extraction quality issues (file upstream if encountered)
- Splitting SOURCE_INDEX.md into per-type files

### Edge Cases & Considerations

- The 1cfe group library uses `zotero.Zotero(5428393, 'group', key)` — different from the user library API call in `zotero_test.py`. This is a new integration point.
- The target document (`PMXLGPKG`) may have complex tables or equations. `--enhance` enables Layer 3+4 repair, and `gmft` provides Layer 2 table extraction.
- If extraction quality is poor, document the issues but do NOT block on fixing them — file upstream against agentic-mbse if needed.
- `knowledge/raw/` already exists with `.gitignore` excluding `*.pdf` (created in Item 1).

---

## Requirements

### Functional Requirements

> Requirements are from the epic definition and user direction unless marked [INFERRED] or [FROM INVESTIGATION].

**FR-1: Zotero Group Library Download**

The download script MUST connect to the **1cfe group library** (id=5428393) using `zotero.Zotero(5428393, 'group', api_key)`. It MUST download the PDF attachment for item `PMXLGPKG` ("Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants") to `knowledge/raw/`.

The `.env` file already has `ZOTERO_ID` and `ZOTERO_KEY`. The group library ID (5428393) MAY be added to `.env` as `ZOTERO_GROUP_ID` or hardcoded in the download script — this is an implementation choice for design.

**FR-2: PDF Extraction**

Run `agentic-mbse extract` on the downloaded PDF with these flags:
- `--output knowledge/sources/<slug>/` — output directory under knowledge/sources
- `--index` — generate INDEX.md
- `--summarize` — include AI summaries in INDEX.md
- `--enhance` — enable Layer 3 (structural repair) + Layer 4 (AI quality repair)

The slug MUST be a filesystem-safe, human-readable directory name derived from the document title.

Expected outputs in `knowledge/sources/<slug>/`:
- `full_document.md` — the extracted markdown
- `INDEX.md` — section index with summaries
- `summary.json` — extraction metadata (backend used, char count, image count, checksums)
- `images/` — extracted images (if any)

**FR-3: SOURCE_INDEX.md Evolution**

The existing SOURCE_INDEX.md format uses four fields per entry:
```markdown
### [Source Name]
- **Type**: codebase | documentation | database | reference
- **Location**: path or URL
- **Use for**: free-text description
- **Validation**: comparison method or "N/A"
```

These four fields MUST be preserved (they are consumed by the agentic-mbse toolchain). The following additional fields MUST be added for the new entry, and SHOULD be added to a documented "Extended Metadata" convention:

- **Zotero Key**: `<group-id>:<item-key>` (e.g., `5428393:PMXLGPKG`)
- **Raw SHA256**: SHA256 hash of the source PDF file
- **Extracted Path**: Relative path to `knowledge/sources/<slug>/`
- **Extract SHA256**: SHA256 hash of `full_document.md`
- **Date Added**: ISO 8601 date when the source was ingested

The existing PyFECONS entry MUST NOT be modified (it predates this convention).

[INFERRED] The new fields are placed after the existing four fields in each entry, maintaining backward compatibility with the toolchain parser.

**FR-4: Zotero State Update**

After successful extraction and SOURCE_INDEX.md registration, the Zotero item MUST be tagged `extracted` via the API. This enables Item 3's smart pull query (`tag=['new', '-extracted']`).

The tag update MUST use the group library API (`zotero.Zotero(5428393, 'group', key)`).

**FR-5: LOCAL_SOURCES.yaml Template**

Create `knowledge/LOCAL_SOURCES.yaml` as a template file for machine-specific paths. The file MUST:
- Be listed in `.gitignore` (at project root or in `knowledge/`)
- Contain documented fields for machine-specific external paths (e.g., PyFECONS location)
- Include comments explaining its purpose and relationship to SOURCE_INDEX.md
- Contain placeholder values that a developer would fill in for their machine

Current known machine-specific paths:
- PyFECONS codebase (currently hardcoded as `/home/reid/PyFECONS` in SOURCE_INDEX.md)

[FROM INVESTIGATION] No code in either repo currently reads this file. It is established as a convention for future toolchain support and human documentation. The spec MUST document this gap explicitly in the file's comments.

**FR-6: Git Commit**

Stage and commit:
- `knowledge/sources/<slug>/` (extracted outputs)
- `knowledge/SOURCE_INDEX.md` (updated)
- `knowledge/LOCAL_SOURCES.yaml` (template — only if not gitignored; if fully gitignored, commit the `.gitignore` update instead)
- Any `.gitignore` updates
- Download/extraction script(s) used

MUST NOT commit:
- `.env`
- PDF files in `knowledge/raw/`

---

## Acceptance Criteria

### Core Functionality

- [ ] pyzotero connects to 1cfe group library (id=5428393) and lists items
- [ ] PDF for item `PMXLGPKG` is downloaded to `knowledge/raw/`
- [ ] `uv run agentic-mbse extract` completes successfully with `--index --summarize --enhance`
- [ ] `knowledge/sources/<slug>/full_document.md` exists with non-trivial content (>1000 chars)
- [ ] `knowledge/sources/<slug>/INDEX.md` exists with section entries
- [ ] `knowledge/sources/<slug>/summary.json` exists with extraction metadata
- [ ] SOURCE_INDEX.md has a new entry with all four canonical fields plus extended metadata
- [ ] Existing PyFECONS entry in SOURCE_INDEX.md is unchanged
- [ ] Zotero item `PMXLGPKG` has tag `extracted` in the group library
- [ ] `knowledge/LOCAL_SOURCES.yaml` exists with documented template fields
- [ ] LOCAL_SOURCES.yaml is gitignored

### Quality & Integration

- [ ] No PDF files committed to git
- [ ] No secrets committed to git
- [ ] `.env` is not staged
- [ ] Extraction quality spot-checked: document is readable, section structure is sensible
- [ ] If extraction quality issues found: documented as notes, NOT blocking

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Research:** `.project/research/20260203-knowledge-database-architecture.md`
- **Item 1 Plan:** `.project/active/knowledge-database-integration/plan.md` (complete)
- **Item 1 Script:** `scripts/zotero_test.py` (user library proof-of-concept)
- **Design:** `.project/active/knowledge-database-integration/design.md` (to be created)

### Key References

- agentic-mbse SOURCE_INDEX.md template: `~/1cfe/agentic-mbse/SOURCE_INDEX.md.template`
- agentic-mbse source-index docs: `~/1cfe/agentic-mbse/docs/source-index.md`
- agentic-mbse extract CLI: `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py`
- Zotero group library: 1cfe (id=5428393), API type `group`

---

**Next Steps:** After approval, proceed to `/_my_design`
