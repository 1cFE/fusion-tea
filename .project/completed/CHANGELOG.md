# Changelog

Historical record of completed work.

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
