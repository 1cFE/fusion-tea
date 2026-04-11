# Product Backlog

Prioritized list of epics and features.

**Last Updated**: 2026-04-11

---

## Priority Legend

- **P0**: Critical - Blocking, do immediately
- **P1**: High - Important, do soon
- **P2**: Medium - Valuable, do when possible
- **P3**: Low - Nice to have, do eventually

---

## In Progress

| Epic | Priority | Status | Started | Notes |
|------|----------|--------|---------|-------|
| Knowledge Database Integration | P1 | In Progress | 2026-02-06 | Items 1-3 complete, pipeline proven. Items 4-5 archived (blocked on user action, infrastructure works). |
| Source Extraction Fix & Re-extraction | P0 | Draft | 2026-03-29 | HTML extraction broken (tables, images, quality). Fix upstream → re-extract → clean .orig.md. |
| Pipeline Hardening (ad-hoc) | P0 | **Complete 2026-04-11** | 2026-04-05 | 6 items archived (pipeline-hardening, output-validation-retry, concept-landscape-context, orig-md-research, feedback-routing-fix, explorer-merge). Analysis pipeline now safe for batch runs. |

---

## P1 - High Priority

### Knowledge Database Integration

**Priority**: P1
**Effort**: ~4-5 days (4 items + ongoing)
**Status**: In Progress (infrastructure complete)

Zotero → pyzotero → agentic-mbse extract → SOURCE_INDEX.md pipeline. Batch automation script works. 6+ sources ingested. Ready to scale when new sources are needed.

**Items**:
- [x] Item 1: Zotero API De-Risk (0.5 day) - Complete 2026-02-06
- [x] Item 2: Single-Source E2E Pipeline (1 day) - Complete 2026-02-06
- [x] Item 3: Ingestion Automation Script (1.5 days) - Complete 2026-02-09
- [~] Item 4: First Corpus Ingestion — Abandoned (superseded by IFE source ingestion)
- [x] Item 5: Extraction Pipeline Integration — Complete 2026-02-27 (script modernized for v4 pipeline)

**File**: `epic-knowledge-database-integration.md`

---

## Active Work Items

| Item | Priority | Status | Location |
|------|----------|--------|----------|
| Batch Pipeline Run | P0 | Not started; unblocked by pipeline-hardening | `.project/active/batch-pipeline-run/` |
| Loop Dry-Run Symmetry | P2 | Spec only (2026-04-10); LOW complexity follow-up | `.project/active/loop-dry-run-symmetry/` |
| Traceability System | P1 | Spec + plan complete, awaiting prioritization | `.project/active/traceability-system/` |

---

## Completed

| Epic | Completed | Duration | Notes |
|------|-----------|----------|-------|
| Visualization POC Sprint | 2026-01-19 | 2 days | Full Cytoscape.js pipeline, 23+ tests |
| Cost Modeling Patterns De-Risking | 2026-03-06 | ~2 months | Learnings handed off to sysml-codegen, all changes implemented |
| End-to-End Pipeline De-Risking | 2026-03-06 | ~5 weeks | Solar+battery pipeline proven, codegen enhancements in open PR |
| Full Workflow Demo | 2026-03-06 | 5 days | Interactive HTML explainer + IFE modeling demo |

---

## Ideas / Future Considerations

- MFE concept modeling (next stage after IFE)
- Cross-concept comparison tooling
- Traceability audit automation (blocked on traceability-system implementation)
