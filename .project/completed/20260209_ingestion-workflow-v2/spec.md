# Spec: Ingestion Workflow V2 — Git-Authoritative Pipeline

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-09 15:50 UTC
**Complexity:** MEDIUM
**Branch:** proj-modeling-0
**Epic:** `.project/backlog/epic-knowledge-database-integration.md` — extends Item 3

---

## Business Goals

### Why This Matters

The current ingestion pipeline (`scripts/zotero_ingest.py`) uses Zotero tags as the queue mechanism: items must be manually tagged `new`, and the script eagerly tags them `extracted` after extraction — before quality review, before git commit. This creates two problems:

1. **State desync**: Zotero says "done" but git has nothing. If extraction quality is bad and you discard the files, Zotero still thinks the item is extracted. There's no rollback without manual API intervention.
2. **Manual tagging doesn't scale**: With 150+ items in the library, requiring a `new` tag on every item to queue it for ingestion is unsustainable.

The fix is to make **git the authoritative source of truth**. A source is "extracted" if and only if it's committed to git. The ingestion script determines what to process by comparing the Zotero library against what's already in git — no manual tagging required.

### Success Criteria

- [ ] Running the ingestion script with no arguments automatically identifies unprocessed items (no manual `new` tag needed)
- [ ] Zotero `extracted` tag is only written AFTER git commit (or as a separate explicit step)
- [ ] Discarding a bad extraction (deleting files, not committing) automatically re-queues the item on next run
- [ ] Standalone PDF attachments (top-level, no parent item) are processed alongside normal bibliographic items
- [ ] The pipeline is idempotent: running it twice with no changes produces no side effects

### Priority

P1 — blocks the first corpus ingestion (KNOW-DB Item 4) and all future ingestion work.

---

## Problem Statement

### Current State

The pipeline has 4 independent state surfaces that can desync:

| Surface | Location | When Written | Reversible? |
|---------|----------|-------------|-------------|
| Raw PDF | `knowledge/raw/` (gitignored) | On download | Yes (delete file) |
| Extracted files | `knowledge/sources/<slug>/` | On extraction | Yes (delete dir) |
| SOURCE_INDEX.md | `knowledge/SOURCE_INDEX.md` | After extraction | Yes (don't commit) |
| Zotero `extracted` tag | Remote API | After extraction, before review | **No** (requires API call) |

The Zotero tag is written eagerly (step 7 of 8) and controls the queue. If you discard a bad extraction, Zotero still thinks it's done — the item disappears from the queue with no way to recover except manual tag removal via the API.

Additionally:
- Queue requires manual `new` tagging (doesn't scale to 150+ items)
- Standalone PDF attachments (6 in library) are silently skipped
- No machine-readable manifest on the git side

### Desired Outcome

Git is the single source of truth. The script compares the Zotero library against a git-side manifest to determine what needs processing. Zotero tags become a downstream reflection of git state, not an upstream control mechanism. Bad extractions are handled by simply not committing — the item automatically re-queues on next run.

---

## Scope

### In Scope

1. **Git-side manifest** — A machine-readable file tracking which Zotero items have been extracted and committed
2. **Git-authoritative queue** — Script determines "pending" items by diffing Zotero library against manifest
3. **Deferred Zotero tagging** — `extracted` tag written only after commit (separate step or flag)
4. **Standalone attachment support** — Process top-level PDF attachments (not just parent items with children)
5. **Batch size control** — Flag to limit how many items are processed per run
6. **Script changes** — Modify `zotero_ingest.py` and `zotero_lib.py`

### Out of Scope

- Changes to `agentic-mbse extract` itself
- Automatic quality scoring or validation
- CI/CD integration
- SOURCE_INDEX.md format changes (manifest is a new file, SOURCE_INDEX.md continues as-is)
- Splitting SOURCE_INDEX.md
- Migration of existing Zotero tags (existing `extracted` tags can stay as-is)

### Edge Cases & Considerations

- **Git conflicts on SOURCE_INDEX.md**: Multiple branches extracting different sources could conflict on SOURCE_INDEX.md and the manifest. Markdown append conflicts are straightforward to resolve. JSON manifest conflicts may need a merge strategy (discussed in design).
- **Re-extraction**: If a source directory exists in git but quality is bad, user deletes it and removes the manifest entry. Next run re-processes automatically.
- **Items without PDFs**: 39 parent items in the library have no PDF attachment. These SHOULD be silently skipped but logged.
- **Duplicate detection**: If a Zotero item's key is in the manifest, skip it regardless of whether files exist on disk. If files were deleted but manifest says "done," that's a manual reconciliation (user removes manifest entry to trigger re-extraction).
- **Standalone attachments with no title**: Use cleaned-up filename for slug and SOURCE_INDEX title. Quality won't be as good as bibliographic metadata, but it works.

---

## Requirements

### Functional Requirements

> Requirements are from user direction unless marked [INFERRED].

**FR-1: Git-Side Manifest**

A machine-readable manifest file MUST be maintained in the repository that tracks which Zotero items have been successfully extracted. The manifest MUST contain at minimum:
- Zotero item key
- Extraction slug (directory name under `knowledge/sources/`)
- Title (from Zotero metadata or filename)
- Date extracted

The manifest MUST be the authoritative record of "what has been ingested." An item is considered extracted if and only if it has an entry in the manifest AND the corresponding source directory exists in git.

**FR-2: Git-Authoritative Queue**

The ingestion script MUST determine pending items by comparing the Zotero library against the manifest — NOT by querying Zotero tags. Specifically:
- Fetch all top-level items from Zotero (or all items in a specified collection)
- Filter to items that have a PDF (either as a child attachment or as a standalone attachment)
- Exclude items whose Zotero key appears in the manifest
- The remaining items are the queue

The `new` tag MUST NOT be required to queue items. [INFERRED] The `new` tag MAY still be supported as an optional filter (`--tag new`) for selective batch processing.

**FR-3: Deferred Zotero Tagging**

The script MUST NOT write the `extracted` tag to Zotero during the extraction run. [INFERRED] A separate command or flag (e.g., `--sync-tags`) SHOULD be provided to update Zotero tags to match the manifest after the user has committed and is satisfied with quality. This makes Zotero tags a convenience for browsing, not a control mechanism.

**FR-4: Standalone Attachment Support**

The script MUST handle top-level items where `itemType == 'attachment'` and `contentType == 'application/pdf'`. For these items:
- Download the PDF directly (no child lookup needed)
- Use the filename (cleaned up) as the title if no better metadata is available
- Process through the same extraction pipeline as normal items

**FR-5: Batch Size Control**

[INFERRED] The script SHOULD support a `--limit N` flag to process at most N items per run. This prevents accidentally kicking off extraction of all 150 items when you only want 5.

**FR-6: Idempotency**

Running the script twice with no intervening changes MUST produce no side effects. Items already in the manifest MUST be skipped. SOURCE_INDEX.md MUST NOT get duplicate entries.

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv run python scripts/zotero_ingest.py --dry-run` lists pending items by diffing Zotero library against manifest (no `new` tag required)
- [ ] `uv run python scripts/zotero_ingest.py --limit 5` processes at most 5 items
- [ ] Standalone PDF attachments appear in the pending list and are processable
- [ ] After extraction (before commit), Zotero items do NOT have `extracted` tag
- [ ] After commit + `--sync-tags`, Zotero items DO have `extracted` tag
- [ ] Deleting a source directory + removing its manifest entry causes the item to reappear in the pending queue on next dry-run
- [ ] Running the script twice in a row (after committing) processes 0 items on the second run

### Quality & Integration

- [ ] Existing `tea_dt_mfe_cost_analysis` source continues to work (backward compatible)
- [ ] Manifest file is committed to git
- [ ] No secrets in manifest
- [ ] Existing Zotero `extracted` tags are not removed or modified (migration is out of scope)

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 3 extension
- **Current Script:** `scripts/zotero_ingest.py`
- **Shared Library:** `scripts/zotero_lib.py`
- **SOURCE_INDEX.md:** `knowledge/SOURCE_INDEX.md`
- **Existing Source:** `knowledge/sources/tea_dt_mfe_cost_analysis/`
- **Paused Work:** `.project/active/first-corpus-ingestion/` (Item 4, waiting on this)

---

**Next Steps:** After approval, proceed to `/_my_design`
