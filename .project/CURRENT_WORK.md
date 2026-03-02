# Current Work

**Last Updated**: 2026-02-27

---

## Active Work

### Extraction Pipeline Integration (KNOW-DB Item 5)

**Status**: In Progress
**Epic**: `.project/backlog/epic-knowledge-database-integration.md`
**Started**: 2026-02-27

**Objective**: Update `scripts/zotero_ingest.py` to align with redesigned agentic-mbse 8-step extraction pipeline.

**Current Phase**: Phase 3 (partially complete — re-extraction done, new ingestion pending)

**Completed**:
- [x] Phase 1: Core script modernization (constants, CLI, run_extraction, flatten, SHA256)
- [x] Phase 2: Re-extract mode (_cleanup_legacy_files, re_extract_sources, --re-extract flag)
- [x] Phase 3a: Re-extract all 6 existing sources — all verified with output.md, metrics.json, decisions.json
- [x] Phase 3b: Quality spot-checks (Delene PASS, Hsu PASS, Hawker unchanged — upstream OCR issue)

**Remaining**:
- [ ] Phase 3c: User adds ~6 PDFs to Zotero, tags them `new`
- [ ] Phase 3d: Run `uv run python scripts/zotero_ingest.py --tag new` to ingest new docs
- [ ] Phase 3e: Verify 12+ total sources, both paths work

**Blockers**: Needs user to add PDFs to Zotero for new ingestion

**Location**: `.project/active/extraction-pipeline-integration/`

**Key files changed**: `scripts/zotero_ingest.py` (only code change)

---

## Recently Completed

_(none yet)_

---

## Up Next

1. Complete KNOW-DB Item 5 (add ~6 new docs, verify 12+ total)
2. KNOW-DB Item 4 completion (first corpus ingestion at scale)
3. Downstream knowledge research work

---

## Session Notes

### 2026-02-27
- Implemented all code changes in Phases 1-2 of extraction-pipeline-integration
- Ran full `--re-extract` of 6 sources — all succeeded with opus/$50
- Found/fixed flatten bug: `_flatten_extraction_output()` failed during re-extraction when `images/` dir existed (changed from `len(subdirs)==1` to candidate-based search)
- Hawker strikethrough is upstream agentic-mbse OCR limitation (17 markers, identical to old extraction)
- All changes are uncommitted on branch `processing-work`
