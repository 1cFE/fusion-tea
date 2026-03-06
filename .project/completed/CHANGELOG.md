# Changelog

Historical record of completed work.

---

## [2026-03-06] - Project Cleanup & Archival

**Type**: Housekeeping
**Duration**: 1 session

### Summary
Comprehensive review and archival of all active work items and backlog epics. Project infrastructure phase is complete; modeling work continues under the modeling PM system.

### Items Archived
- `extraction-pipeline-integration` — Script modernized for v4 pipeline, 6 sources re-extracted. Infrastructure proven.
- `extraction-validation` — v4 pipeline validated against 6-source corpus. Verdict: proceed.
- `project-reframing` — Massive scope change from CATF-MFE to broad comparative investigation. 8 phases complete.
- `ife-source-ingestion` — 5 IFE sources ingested into knowledge/sources/. SOURCE_INDEX updated.
- `ife-domain-research` — Domain insights produced from IFE literature review.
- `ife-modeling-epic-setup` — *Completed for demo purposes.* Set up IFE Cost Modeling epic (WI-006/007/008) in modeling PM.
- `ife-cost-model-full-workflow` — *Completed for demo purposes.* Meta-orchestrator for IFE modeling workflow demo. All 3 WIs (WI-006/007/008) completed successfully.
- `visualization-demo` — Section 8 of workflow explainer populated with structural view, calc flow, and parameter table.

### Items Abandoned
- `first-corpus-ingestion` — Superseded by `ife-source-ingestion` which ingested 5 IFE-focused sources.

### Epics Archived
- **Visualization POC Sprint** — Complete (all 5 items delivered 2026-01-19)
- **Cost Modeling Patterns De-Risking** — Complete. Learnings from coffee maker and solar+battery models handed off to sysml-codegen; all changes implemented upstream.
- **End-to-End Pipeline De-Risking** — Complete. Solar+battery LCOE pipeline proven end-to-end. Codegen enhancements (Item 6: nested CalcUsage discovery) in open PR.
- **Full Workflow Demo** — Complete. Interactive HTML explainer shipped; IFE modeling demo delivered through modeling PM.

### Remaining Active
- `traceability-system` — Spec + plan written, ready for implementation when prioritized.
- Knowledge DB Integration epic — Kept (infrastructure works, ready to scale).

---

## [2026-01-18] - Visualization POC Sprint (EPIC-001)

**Type**: Epic (5 items)
**Duration**: 2 days (estimated: 5 days)

### Summary
End-to-end proof-of-concept: SysML model → structural extraction → Cytoscape.js interactive web diagram with cost coloring, tree layout, expand/collapse, and PNG export.

### Items Closed
- `golden-reference-cytoscape-poc` — Hand-written JSON + Cytoscape demo de-risking rendering
- `extraction-implementation` — `extract_structural_view()` producing ViewResult data structures
- `end-to-end-pipeline` — `to_cytoscape()`, `to_dot()` converters + CLI entry point
- `visualization-options` — Inside-box labels, tree layout, %-of-parent cost coloring
- `cost-annotations` — Cost attribute extraction + cost-based node styling
- `web-integration` — FastAPI server: model path → extraction → interactive diagram

### Deliverables
- `proof_of_concept/web/` — FastAPI server + Cytoscape frontend
- Extraction pipeline with format converters
- 23+ tests passing

---

## [2026-01-26] - Costed Component Interface

**Type**: Item (Cost Patterns De-Risking epic)
**Duration**: 1 day

### Summary
Production-ready `'Costed Component'` interface with type-safe `CASCategory` enum containing all PyFECONS CAS codes. Foundation for all cost modeling.

### Deliverables
- `models/library/foundation/costing/` — Costed Component interface + CAS enum

---

## [2026-02-01] - Codegen Chain Spike

**Type**: Item (End-to-End Pipeline De-Risking epic)
**Duration**: ~2 days

### Summary
Validated that sysml-codegen handles CalcUsage dependency chains. GO verdict — extraction pipeline's chain binding support works end-to-end. Revisit confirmed 3 runtime gaps fixed upstream.

### Deliverables
- Spike models in `models/tests/codegen_chain_spike/`
- Findings and fix plan documented

---

## [2026-02-09] - Solar+Battery End-to-End Pipeline

**Type**: Epic (6 items, 5 complete, 1 deferred)
**Duration**: ~10 days

### Summary
Full LCOE pipeline proof: SysML model → codegen → calc implementations → ComponentCostEvaluator → LCOE verification. Solar+battery plant model produces $288.68/MWh within 1% tolerance.

### Items Closed
- `solar-battery-sysml-model` — Full SysML model (3 hierarchy levels, 9 leaf parts, 15 calc defs)
- `solar-battery-cost-evaluation` — Cost evaluation script + JSON entry points, all 10 tests passing
- `hybrid-pipeline-e2e` — Complete pipeline: codegen → calcs → evaluator → LCOE verified
- `gap1-default-value-debug` — Root cause: path filter mismatch. Fix plan for upstream repos.

### Deferred
- Item 6 (Codegen nested CalcUsage discovery) — upstream enhancement, not blocking

### Deliverables
- `models/tests/solar_battery/` — Complete SysML model + expected outputs
- Pipeline YAML, registry, integration tests
- 28 pipeline tests + 10 regression tests passing

---

## [2026-02-09] - Knowledge Database Integration (KNOW-DB Items 1-3)

**Type**: Epic (partial — Items 1-3 of 5)
**Duration**: ~3 days

### Summary
Built git-authoritative Zotero ingestion pipeline: API de-risk → single-source E2E → batch automation → manifest-based diffing. 6 fusion sources ingested.

### Items Closed
- `knowledge-database-integration` — Items 1-2: Zotero API de-risk + single-source pipeline
- `zotero-ingestion-script` — Item 3: Batch ingestion with --dry-run, --local-pdf
- `ingestion-workflow-v2` — Manifest diffing replaces tag-based queue

### Deliverables
- `scripts/zotero_ingest.py` — Batch ingestion automation
- `scripts/zotero_lib.py` — Shared Zotero API helpers
- `knowledge/MANIFEST.jsonl` — Git-side source tracking
- 6 sources in `knowledge/sources/`

---

## [2026-01-12] - Cost Evaluation Script (Archived)

**Type**: Item (Cost Patterns De-Risking epic)
**Status**: Never started — superseded by `solar-battery-cost-evaluation`

### Summary
Spec and design drafted for coffee maker cost evaluation script. Work was superseded when the solar+battery model became the primary evaluation target.

---
