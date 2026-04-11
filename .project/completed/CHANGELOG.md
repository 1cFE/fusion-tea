# Changelog

Historical record of completed work.

---

## [2026-04-11] - Pipeline Hardening, Explorer Merge, Source Cleanup

**Type**: Feature + robustness (8 work items + 2 deletions)
**Duration**: ~1 week on `design-space-explore`

### Summary
Pipeline-hardening closed a class of silent-corruption and transient-error failures that had been killing `stage1-all --all` runs and required manual re-runs. In parallel, output validation, feedback routing, concept-landscape context, and .orig.md re-sourcing landed as independent correctness fixes. The concept explorer (from `ralph/concept-explorer`) was merged into the analysis pipeline branch, and Phase 1a source replacement was closed out. The combined effect: `batch-pipeline-run` can now safely proceed against all concepts.

### Items Archived
- `pipeline-hardening` — Validated invocation, transient-error retry, state integrity across `loop.py`/`run_analysis.py`/`research.py`. Deleted legacy `step_runner` surface. 7 phases, audit passed clean. Commit 9d9605a.
- `output-validation-retry` — `invoke_claude_validated()` wrapper with regex-based verdict/section validators; retry-via-resume on malformed output. Commit 46afb62.
- `concept-landscape-context` — Injected cross-concept catalog into analysis prompts so agents can name verifiable nearest neighbors; simplified vestigial status codes (`D`/`M` → `iterating`). Commits 244e160, 0ab9dc0.
- `orig-md-research` — Re-sourced 21 NO-verdict `.orig.md` Haiku-paraphrased files against real HTML sources and deleted originals. Commit a8c489a.
- `feedback-routing-fix` — Added finding categories so assessment findings targeting model code reach `model_setup.py` directly instead of being laundered through analysis prose. Commit 73f6994.
- `explorer-merge` — Merged `ralph/concept-explorer` (FastAPI 4-page explorer, 140+ tests) into `design-space-explore`. Commit d8cb8ce and follow-ups.
- `source-replacement` — Phase 1a source replacement effort, coupled with `orig-md-research`. Triage report, plan, and plan-completion preserved for reference.
- `common-output-interface` — Picked up a lingering prior-session archival (staged rename to `completed/20260407_common-output-interface/` that was never committed). Plan marked Complete as of 2026-04-07.

### Deleted (not archived)
- `extraction-interface-gap/` — Empty orphan directory, never committed.
- `step-runner-validation-retry/` — Untracked spec only. Superseded by pipeline-hardening Phase 5, which explicitly deleted the legacy `step_runner` surface the spec targeted.

### Remaining Active
- `batch-pipeline-run` — Not started; unblocked now that pipeline is hardened
- `loop-dry-run-symmetry` — Small follow-up from pipeline-hardening audit (spec only)
- `traceability-system` — Still on hold awaiting prioritization

---

## [2026-04-05] - Analysis Pipeline Bulk Archival

**Type**: Housekeeping
**Duration**: 1 session

### Summary
Archived 13 completed work items from the analysis pipeline development phase. The pipeline (`run_analysis.py` + `lib/` modules) is fully operational with iterative analysis, autonomous source acquisition, cross-concept memory, PROCEED/REVISE review verdicts, and concept management tooling.

### Items Archived
- `automated-concept-analysis` — Core analysis pipeline with gap-check/analyze/approve workflows and Claude invocation. All 5 phases complete.
- `autonomous-source-acquisition` — WebSearch/WebFetch research step for automated data gap resolution. Live-tested.
- `checkpoint-test-concept17` — End-to-end validation on concept 17a with replaced sources. 6/8 spot checks passed.
- `concept-research-skill` — Consolidated research docs into README.md + `concept-research-navigation` skill.
- `constraint-atms-spike` — ATMS constraint propagation prototype for design space exploration.
- `iterative-analysis-loop` — Multi-pass analysis with config extraction, modal prompts, and convergence tracking.
- `manage-concept-agent` — Interactive `/manage-concept` command for concept vetting and comparison.
- `refactor-final-stages` — Rescoped review/synthesize/approve to PROCEED/REVISE verdicts with kick-back.
- `refactor-run-analysis` — Extracted `run_analysis.py` (2306→1380 lines) into 9 `lib/` modules.
- `refactor-stage1-loop` — `iter-N/` directory layout, `--resume` support, verdict.json tracking, migration.
- `research-artifact-sync` — R2 binary sync + migration to `knowledge/concept_research/`.
- `shared-memory-system` — Cross-concept tagged memory (concept/family/universal) loaded into analysis prompts.
- `source-addition` — `add-source` and `update-analysis` commands for incremental source addition.

### Remaining Active
- `orig-md-research` — Re-sourcing NO-verdict `.orig.md` files (3/21 processed)
- `source-replacement` — Coupled to above; extraction complete, cleanup remains
- `traceability-system` — Spec/design/plan written, awaiting prioritization

---

## [2026-03-29] - Concept Taxonomy & Interactive Explorer

**Type**: Feature (4 work items, 2 superseded)
**Duration**: 1 day

### Summary
Built taxonomy visualizer for all 38 fusion concepts: Pydantic data models, pairwise similarity engine (4-dimension decomposition + classical MDS), 7 API endpoints, and interactive frontend with tree view, Plotly constellation scatter, taxonomy cards, and Cytoscape neighborhood graph.

Neighborhood graph went through two failed iterations (procedural add/remove causing re-renders) before landing on a proper model-view architecture (GraphModel built once, GraphView toggles visibility).

### Items Archived
- `concept-taxonomy-and-similarity` — Foundation: data models, similarity engine, API, tree/constellation/cards. Complete.
- `graph-model-rewrite` — Model-view rewrite of neighborhood graph. Complete.
- `taxonomy-viz-redesign` — Intermediate attempt, superseded by graph-model-rewrite.
- `taxonomy-viz-polish` — Intermediate attempt, superseded by graph-model-rewrite.

### Deliverables
- `exploration/concept_explorer/taxonomy_models.py` — Pydantic models with typed enums
- `exploration/concept_explorer/similarity.py` — Pairwise similarity + MDS + diversity-aware bridges
- `exploration/concept_explorer/seed_registry.py` — Canonical JSON registry seeded from table_v2.csv
- Frontend: `taxonomy.js`, `taxonomy_card.js`, `neighborhood_graph.js`, `constellation.js`, `tree_view.js`
- 140+ tests (54 new for taxonomy/similarity)

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
