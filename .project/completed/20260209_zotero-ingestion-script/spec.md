# Spec: Zotero Ingestion Automation Script (KNOW-DB Item 3)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-09 00:47 UTC
**Complexity:** MEDIUM
**Branch:** proj-modeling-0
**Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 3

---

## Business Goals

### Why This Matters

Items 1 and 2 proved the full knowledge pipeline works end-to-end for a single document. But each ingestion currently requires ~10 manual steps: run the download script, run extraction, compute checksums, hand-edit SOURCE_INDEX.md, tag in Zotero. This is tedious and error-prone at scale. Item 3 collapses the entire process into one command, which gates Item 4 (batch ingesting 5-10 real fusion sources into the corpus).

### Success Criteria

- [ ] `uv run python scripts/zotero_ingest.py` processes all `new`-tagged Zotero items in one command
- [ ] Each processed item gets: PDF downloaded, markdown extracted, SOURCE_INDEX.md entry appended, Zotero tag updated
- [ ] `--dry-run` lists items without modifying anything
- [ ] `--local-pdf <path>` extracts a PDF not managed by Zotero
- [ ] Items with no PDF attachment are skipped with a warning
- [ ] Extraction failures are logged and the item is NOT tagged as extracted
- [ ] Script output summarizes: N items found, N extracted, N skipped, N failed

### Priority

P1 — gates Item 4 (First Corpus Ingestion). Sequential within the KNOW-DB epic.

---

## Problem Statement

### Current State

- Single-source pipeline proven end-to-end (Item 2 complete)
- SOURCE_INDEX.md extended metadata format established (Zotero key, checksums, extraction path, date)
- `scripts/zotero_group_download.py` handles single-item download from the 1cfe group library
- `agentic-mbse extract --index --summarize --enhance` proven on a real fusion PDF
- Each source ingestion requires ~10 manual steps across multiple tools
- Reference implementation exists in research report (Section 8)

### Desired Outcome

A single CLI command (`uv run python scripts/zotero_ingest.py`) that batch-processes all pending Zotero items through the full pipeline: download, extract, register, tag. Plus a `--local-pdf` fallback for PDFs not in Zotero, and a `--dry-run` mode for safe previewing.

---

## Scope

### In Scope

1. **Smart pull** — Query 1cfe Zotero group library for items tagged `new` but NOT `extracted`
2. **Batch download + extract loop** — For each item: download PDF, generate slug, run extraction, compute checksums
3. **SOURCE_INDEX.md auto-registration** — Append new entries using the extended metadata format from Item 2
4. **Zotero state update** — Tag each successfully processed item as `extracted`
5. **Error handling** — Skip items with no PDF (warn), handle extraction failures (don't tag), handle duplicate slugs (append Zotero key suffix)
6. **`--local-pdf <path>` fallback** — Process a PDF not managed by Zotero (Path B from research)
7. **`--dry-run` mode** — List what would be processed without modifying anything
8. **Summary output** — Report counts: found, extracted, skipped, failed
9. **Shared abstractions** — Extract common logic from `zotero_group_download.py` to avoid duplication, while keeping both scripts as separate tools (single-item download vs. batch ingest)

### Out of Scope

- CI/CD integration
- Automatic `/research` invocation after extraction
- Version-based incremental sync (tag-based is sufficient)
- SOURCE_INDEX.md splitting into per-type files
- Changes to `agentic-mbse` toolchain itself
- Extraction quality repair (file upstream if issues found)

### Edge Cases & Considerations

- **Duplicate slugs**: If two documents produce the same slug, append the Zotero item key as a suffix (e.g., `fusion_cost_study_PMXLGPKG`)
- **Items with multiple PDFs**: Use the first PDF attachment (same pattern as `zotero_group_download.py`)
- **Items with no PDF**: Skip with a logged warning, do not count as failure
- **Extraction failure**: Log the error, do NOT tag the item as `extracted` in Zotero, count as failure in summary
- **Network interruption mid-batch**: Each item is processed independently. Partially-completed items (PDF downloaded but extraction failed) are safe to re-run — download skips existing files, extraction overwrites output dir
- **SOURCE_INDEX.md "Use for" and "Validation" fields**: Auto-generated entries leave these blank (placeholder text) for manual curation later
- **`--local-pdf` without Zotero**: No Zotero metadata available — slug derived from filename, no Zotero key in SOURCE_INDEX.md entry, no tag update

---

## Requirements

### Functional Requirements

> Requirements are from the epic definition and user direction unless marked [INFERRED] or [FROM INVESTIGATION].

**FR-1: Smart Zotero Query**

The script MUST connect to the 1cfe group library (id=5428393) and query for items tagged `new` but NOT `extracted` using pyzotero's tag filtering (`tag=['new', '-extracted']`). The API key MUST be loaded from `.env` via `ZOTERO_KEY`.

**FR-2: Batch Processing Loop**

For each discovered item, the script MUST:
1. Download the PDF attachment to `knowledge/raw/` (skip if already exists)
2. Generate a filesystem-safe slug from the item title
3. Run `uv run agentic-mbse extract <pdf> --output knowledge/sources/<slug>/ --index --summarize --enhance`
4. Compute SHA256 of the raw PDF and the extracted `full_document.md`
5. Append a new entry to `knowledge/SOURCE_INDEX.md` with the extended metadata format
6. Tag the Zotero item as `extracted` via API

`--enhance` MUST be the default extraction mode.

**FR-3: SOURCE_INDEX.md Auto-Registration**

Each new entry MUST follow the format established in Item 2:

```markdown
### <Title from Zotero metadata>
- **Type**: documentation
- **Location**: knowledge/sources/<slug>/
- **Use for**:
- **Validation**:

#### Extended Metadata
- **Zotero Key**: 5428393:<item-key>
- **Raw SHA256**: <sha256 of PDF>
- **Extracted Path**: knowledge/sources/<slug>/
- **Extract SHA256**: <sha256 of full_document.md>
- **Date Added**: <ISO 8601 date>
```

The "Use for" and "Validation" fields MUST be left blank for manual curation. New entries MUST be appended under `## Primary Sources`, after all existing entries.

**FR-4: Error Handling**

- Items with no PDF attachment MUST be skipped with a warning (not counted as failure)
- Extraction failures MUST be logged with the error message
- Failed items MUST NOT be tagged as `extracted` in Zotero
- Failed items MUST NOT have entries appended to SOURCE_INDEX.md
- The script MUST continue processing remaining items after a failure

**FR-5: Dry-Run Mode**

`--dry-run` MUST list all items that would be processed (title, Zotero key, PDF filename) without downloading, extracting, modifying SOURCE_INDEX.md, or tagging in Zotero.

**FR-6: Local PDF Fallback**

`--local-pdf <path>` MUST process a PDF file directly from disk, bypassing the Zotero query entirely:
- Slug derived from the PDF filename (minus extension, sanitized)
- No Zotero key in the SOURCE_INDEX.md entry
- No Zotero tag update
- All other steps (extraction, SOURCE_INDEX.md registration, checksums) apply normally

**FR-7: Duplicate Slug Handling**

If a generated slug collides with an existing directory in `knowledge/sources/`, the script MUST append the Zotero item key as a suffix (e.g., `<slug>_<item_key>`). For `--local-pdf`, append a numeric suffix.

**FR-8: Summary Output**

After processing, the script MUST print a summary:
```
Summary: N found, N extracted, N skipped (no PDF), N failed
```

**FR-9: Shared Abstractions with zotero_group_download.py**

[INFERRED] Common logic between `zotero_ingest.py` and `zotero_group_download.py` SHOULD be extracted into a shared module to avoid duplication. Both scripts remain separate CLI entry points. Shared concerns include:
- Zotero group library connection (group ID, API key loading)
- PDF attachment discovery
- PDF download with skip-if-exists
- SHA256 computation
- Zotero tagging

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv run python scripts/zotero_ingest.py` connects to the 1cfe group library and discovers `new`-tagged items
- [ ] Each discovered item with a PDF is downloaded, extracted, registered, and tagged
- [ ] SOURCE_INDEX.md entries match the extended metadata format from Item 2
- [ ] "Use for" and "Validation" fields are left blank in auto-generated entries
- [ ] `--dry-run` lists items without modifying anything (no downloads, no extractions, no tags, no SOURCE_INDEX.md edits)
- [ ] `--local-pdf <path>` extracts a non-Zotero PDF and registers it in SOURCE_INDEX.md
- [ ] Items with no PDF attachment are skipped with a warning
- [ ] Extraction failures are logged and the item is NOT tagged as `extracted`
- [ ] Duplicate slugs are handled (Zotero key suffix or numeric suffix)
- [ ] Summary line printed at end: found, extracted, skipped, failed
- [ ] `scripts/zotero_group_download.py` still works independently after refactoring shared code

### Quality & Integration

- [ ] Existing tests continue to pass
- [ ] No secrets committed to git
- [ ] No PDF files committed to git
- [ ] `--enhance` is the default extraction mode
- [ ] Shared module avoids code duplication between download and ingest scripts

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Research:** `.project/research/20260203-knowledge-database-architecture.md` (Section 8: reference implementation)
- **Item 2 Spec:** `.project/active/knowledge-database-integration/spec.md`
- **Item 2 Design:** `.project/active/knowledge-database-integration/design.md`
- **Download Script:** `scripts/zotero_group_download.py` (single-item, to share abstractions with)
- **De-risk Script:** `scripts/zotero_test.py` (Item 1, superseded by group download)
- **SOURCE_INDEX.md:** `knowledge/SOURCE_INDEX.md` (target for auto-registration)
- **Design:** `.project/active/zotero-ingestion-script/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
