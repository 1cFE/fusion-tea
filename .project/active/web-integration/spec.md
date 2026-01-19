# Spec: Web Integration

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-18 23:46:05 UTC
**Complexity:** LOW
**Branch:** visualization

---

## Business Goals

### Why This Matters

This item completes the vertical slice from SysML model to interactive browser visualization. Currently, users must run a CLI command, copy the JSON output, and paste it into an HTML file to see a diagram. Web integration eliminates this friction, enabling stakeholders to explore model visualizations directly in their browser.

### Success Criteria

- [x] Complete workflow: model file → browser diagram with no manual steps
- [x] Stakeholders can independently explore fusion model visualizations
- [x] Technical approach is validated for full implementation

### Priority

P0 - Item 4 of 5-day POC sprint. Depends on Items 1-3 (complete).

---

## Problem Statement

### Current State

The extraction pipeline (Item 3) outputs Cytoscape JSON to stdout or a file. To visualize:
1. Run CLI: `uv run python -m proof_of_concept.extraction <model-path>`
2. Copy JSON output
3. Paste into `cytoscape_demo.html` replacing the `cytoscapeData` constant
4. Open HTML file in browser

This manual process is unsuitable for stakeholder demos or iterative exploration.

### Desired Outcome

Users navigate to `http://localhost:8000`, enter a model path, and immediately see an interactive diagram. No file editing or copy-paste required.

---

## Scope

### In Scope

1. **FastAPI server** with:
   - API endpoint returning Cytoscape elements for a model path
   - Static file serving for frontend assets

2. **Web frontend** with:
   - Model path input
   - Cytoscape.js diagram rendering
   - Expand/collapse, zoom, info panel (existing features)
   - PNG export button

3. **Documentation** (README with setup instructions)

### Out of Scope

- Authentication or authorization
- Real-time model file watching
- Multiple simultaneous views
- WebSocket connections
- Cost annotations (Item 5)
- Production deployment concerns

### Edge Cases & Considerations

- Invalid model path: Return clear error message
- Model with no structural elements: Handle gracefully (empty diagram or message)
- Large models: No special handling for POC; note for future work if issues arise

---

## Requirements

### Functional Requirements

> Requirements below are from epic/sprint plan unless marked [INFERRED]

1. **FR-1**: Server SHALL expose `GET /api/model/{path}` endpoint that returns Cytoscape.js elements JSON
2. **FR-2**: Server SHALL serve static files for the web frontend
3. **FR-3**: Frontend SHALL provide an input field for model path
4. **FR-4**: Frontend SHALL render Cytoscape diagram using data from API
5. **FR-5**: Frontend SHALL support expand/collapse, zoom-to-node, and info panel (existing features)
6. **FR-6**: Frontend SHALL provide PNG export functionality
7. **FR-7**: [INFERRED] API SHALL return appropriate HTTP error codes for invalid paths or extraction failures

### Non-Functional Requirements

- Server SHOULD start with a single command (`uv run python -m proof_of_concept.web` or similar)
- Page SHOULD load and render diagram within a few seconds for coffee_maker model

---

## Acceptance Criteria

### Core Functionality

- [x] Navigate to `http://localhost:8000`
- [x] Enter `models/tests/coffee_maker` in input field
- [x] See interactive diagram rendered
- [x] Expand/collapse nodes works
- [x] Double-click zoom-to-node works
- [x] Click node shows details in info panel
- [x] Export PNG produces readable image

### Error Handling

- [x] Invalid path shows user-friendly error message
- [x] Server logs errors for debugging

### Quality & Integration

- [x] Existing tests continue to pass (27 tests)
- [x] Server can be started and stopped cleanly

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_visualization-poc.md` (Item 4)
- **Research:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md` (Day 4, lines 337-358)
- **Design:** `.project/active/web-integration/design.md` (to be created)
- **Dependencies:** Item 3 deliverables in `proof_of_concept/extraction/`

---

**Next Steps:** After approval, proceed to `/_my_design`
