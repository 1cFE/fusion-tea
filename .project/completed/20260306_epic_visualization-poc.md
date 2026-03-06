# Epic: Visualization POC Sprint

**Epic ID**: EPIC-001
**Priority**: P0 (Critical - enables stakeholder feedback)
**Total Effort**: 5 days
**Status**: Complete

---

## Overview

Build a proof-of-concept visualization pipeline to de-risk the technical approach and enable early user feedback.

**Goal**: Working vertical slice from SysML model → interactive web diagram with export.

**Reference**: Full research, risk assessment, and technical specifications are in:
`.project/research/20260118-191541_visualization-poc-sprint-plan.md`

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Extraction works | Tests pass comparing to golden reference |
| Rendering works | Coffee maker hierarchy visible in browser |
| Export works | PNG export produces readable image |
| Pipeline complete | Model file → interactive diagram in browser |
| De-risked | No blocking unknowns for full implementation |

---

## Backlog Items

### Item 1: Golden Reference + Cytoscape POC [Effort: 1 day]

**Type**: Research / Prototyping
**Objective**: Validate Cytoscape.js can render the diagram we want, independent of extraction.

**Scope**:
1. Create `golden_references/coffee_maker_structural.json` - Hand-written JSON in ViewResult format
2. Create `proof_of_concept/cytoscape_demo.html` - Static HTML with:
   - Dagre layout
   - Compound nodes (part hierarchy)
   - Node type styling
   - Basic expand/collapse
   - Zoom to node
   - PNG export

**Out of Scope**:
- Backend integration
- Dynamic model loading

**Success Criteria**:
- [x] Diagram looks reasonable
- [x] 3-level hierarchy renders correctly
- [x] Expand/collapse works
- [x] Export produces clean PNG

**Status**: Complete (2026-01-18)
**Dependencies**: None
**Deliverables**: `proof_of_concept/golden_references/`, `proof_of_concept/cytoscape_demo.html`, `proof_of_concept/README.md`
**Reference**: Sprint Plan - Day 1 (lines 259-279)

---

### Item 2: Extraction Implementation [Effort: 1 day]

**Type**: Implementation
**Objective**: Implement `extract_structural_view()` that produces output matching golden reference.

**Scope**:
1. Create `proof_of_concept/extraction/visualization.py` with `extract_structural_view()` function
2. Create `proof_of_concept/tests/test_visualization.py` comparing extraction to golden reference

**Out of Scope**:
- Cost view extraction
- Dependency view extraction
- CLI interface

**Success Criteria**:
- [x] `pytest proof_of_concept/tests/` passes (19 tests)
- [x] Extracted JSON matches golden reference structure

**Status**: Complete (2026-01-18)
**Dependencies**: Item 1 (golden reference needed for comparison)
**Deliverables**:
- `proof_of_concept/extraction/types.py` - TypedDicts and mapping registries
- `proof_of_concept/extraction/visualization.py` - Extraction function
- `proof_of_concept/tests/test_visualization.py` - Golden reference comparison tests
- Updated `proof_of_concept/golden_references/coffee_maker_structural.json` with qualified path IDs
**Reference**: Sprint Plan - Day 2 (lines 281-309)
**Spec/Design/Plan**: `.project/active/extraction-implementation/`

---

### Item 3: End-to-End Pipeline [Effort: 1 day]

**Type**: Implementation
**Objective**: Connect extraction to rendering with output converters and CLI.

**Scope**:
1. Add `to_cytoscape()` function - Convert ViewResult to Cytoscape.js format
2. Add `to_dot()` function - Convert ViewResult to DOT format for Graphviz
3. Add CLI command: `uv run python -m proof_of_concept.extraction <model-path>`

**Out of Scope**:
- Web server
- Interactive features beyond Day 1 POC

**Success Criteria**:
- [x] CLI produces valid JSON loadable by Cytoscape POC from Day 1
- [x] DOT output renders correctly in Graphviz (syntax validated)
- [x] End-to-end: model → extraction → JSON → Cytoscape → diagram

**Status**: Complete (2026-01-18)
**Dependencies**: Item 2 (extraction functions)
**Deliverables**:
- `proof_of_concept/extraction/visualization.py` - Added `load_model()`, `to_cytoscape()`, `to_dot()`
- `proof_of_concept/extraction/__main__.py` - CLI entry point
- `proof_of_concept/extraction/__init__.py` - Updated exports
- `proof_of_concept/tests/test_visualization.py` - 5 new tests (24 total)
- `proof_of_concept/cytoscape_demo.html` - Updated to accept CLI output directly
**Reference**: Sprint Plan - Day 3 (lines 311-335)
**Spec/Design/Plan**: `.project/active/end-to-end-pipeline/`

---

### Item 4: Web Integration [Effort: 1 day]

**Type**: Implementation
**Objective**: Create minimal web app that loads model and renders diagram.

**Scope**:
1. Create `proof_of_concept/web/server.py` - FastAPI server with:
   - `GET /api/model/{path}` - Returns Cytoscape.js elements for model at path
   - Static file serving
2. Create `proof_of_concept/web/index.html` - Web page with model input and export button
3. Create README with setup instructions

**Out of Scope**:
- Authentication
- Real-time updates
- Multiple simultaneous views

**Success Criteria**:
- [x] Navigate to `http://localhost:8000`
- [x] Enter `models/tests/coffee_maker`
- [x] See interactive diagram
- [x] Export PNG works

**Status**: Complete (2026-01-19)
**Dependencies**: Item 3 (CLI/converters working)
**Deliverables**:
- `proof_of_concept/web/__init__.py` - Package marker
- `proof_of_concept/web/__main__.py` - Entry point for `uv run python -m proof_of_concept.web`
- `proof_of_concept/web/server.py` - FastAPI server with API endpoint and static serving
- `proof_of_concept/web/static/index.html` - Interactive Cytoscape viewer with model path input
- `proof_of_concept/tests/test_web.py` - 3 API tests
**Reference**: Sprint Plan - Day 4 (lines 337-358)
**Spec/Design/Plan**: `.project/active/web-integration/`

---

### Item 5: Cost Annotations + Polish [Effort: 1 day]

**Type**: Implementation / Documentation
**Objective**: Add cost data to structural view; polish for demo.

**Scope**:
1. Update `extract_structural_view()` with `include_cost_attributes` parameter
2. Update Cytoscape styling to show costs in info panel + "Color by Cost" toggle
3. Create `golden_references/coffee_maker_with_costs.json`
4. Update tests for cost extraction
5. Demo: load coffee maker model and see costs immediately

**Out of Scope**:
- Cost rollup visualization (edges)
- Dependency tracing

**Success Criteria**:
- [x] Cost values appear in info panel when node selected
- [x] "Color by Cost" toggle applies gradient styling
- [x] Golden reference with costs matches extraction (23 tests pass)
- [x] Demo-ready: load coffee maker and see costs immediately

**Status**: Complete (2026-01-19)
**Dependencies**: Item 4 (web integration working)
**Deliverables**:
- `models/tests/coffee_maker/generate_costs.py` - Added `compute_costs()` API
- `proof_of_concept/extraction/types.py` - Added `costs` field to `StructuralNode`
- `proof_of_concept/extraction/visualization.py` - Added cost extraction + Cytoscape passthrough
- `proof_of_concept/web/server.py` - Passes `DEFAULT_COST_ATTRIBUTES` to extraction
- `proof_of_concept/web/static/index.html` - Info panel costs + "Color by Cost" toggle
- `proof_of_concept/golden_references/coffee_maker_with_costs.json` - Golden reference with costs
- `proof_of_concept/tests/test_visualization.py` - 6 new cost tests (23 total)
**Reference**: Sprint Plan - Day 5 (lines 360-380)
**Spec/Design/Plan**: `.project/active/cost-annotations/`

---

## Deferred to Future Sprints

See Sprint Plan Part 5 (lines 541-560) for full deferred work list:

- Dependency view (high complexity - expression trees)
- Agent integration
- Real-time model watching
- Multiple view types in UI
- Fusion model support

---

## Technical References

All technical specifications including data models, golden reference schema, Cytoscape.js stylesheet, and file structure are in the sprint plan document:

`.project/research/20260118-191541_visualization-poc-sprint-plan.md`

Key sections:
- Part 4.1: ViewResult Data Model (lines 399-423)
- Part 4.2: Golden Reference Schema (lines 425-458)
- Part 4.3: Cytoscape.js Stylesheet (lines 461-509)
- Part 4.4: File Structure (lines 514-537)
