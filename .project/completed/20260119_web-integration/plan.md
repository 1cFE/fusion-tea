# Implementation Plan: Web Integration

**Status:** Complete
**Created:** 2026-01-19 00:01:43 UTC
**Last Updated:** 2026-01-19

## Source Documents

- **Spec:** `.project/active/web-integration/spec.md`
- **Design:** `.project/active/web-integration/design.md` ← See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks backend integration by testing the API endpoint against the same golden reference used by existing extraction tests. Phase 2 makes the server runnable and adds static file serving. Phase 3 connects the frontend - saved for last since it's mostly adapting working code.

**Overall Validation Approach:**
- Each phase starts with tests (Phase 1 & 2 automated, Phase 3 manual)
- Continuous verification via `uv run python -m pytest proof_of_concept/tests/`
- Final validation matches spec acceptance criteria

---

## Phase 1: Dependencies + API Endpoint with Tests

### Goal

Add FastAPI/uvicorn dependencies, create the server with API endpoint, and verify the extraction pipeline integration works via tests. This de-risks the core backend functionality first.

### Test Stencil (Write This First)

```python
# proof_of_concept/tests/test_web.py
import pytest
from fastapi.testclient import TestClient

from proof_of_concept.web.server import app

client = TestClient(app)

def test_get_model_valid_path():
    """API returns Cytoscape elements for valid model."""
    response = client.get("/api/model/models/tests/coffee_maker")
    assert response.status_code == 200
    data = response.json()
    assert "elements" in data
    assert len(data["elements"]) == 10  # Matches golden reference

def test_get_model_invalid_path():
    """API returns 404 for nonexistent path."""
    response = client.get("/api/model/nonexistent/path")
    assert response.status_code == 404
    assert "detail" in response.json()
```

### Changes Required

**See `design.md` for:**
- API endpoint specification → `design.md#1-server`
- Error handling strategy → `design.md#error-handling`
- Dependencies → `design.md#dependencies`

**Specific file changes:**

#### 1. Add Dependencies
**File:** `pyproject.toml`
- [x] Run: `uv add fastapi uvicorn`

#### 2. Test File (Write First)
**File:** `proof_of_concept/tests/test_web.py` (NEW)
- [x] Create test file with stencil above
- [x] Test valid path returns 200 with 10 elements
- [x] Test invalid path returns 404

#### 3. Server Implementation
**File:** `proof_of_concept/web/server.py` (NEW)
- [x] Create `proof_of_concept/web/` directory
- [x] Implement FastAPI app with `GET /api/model/{path:path}` endpoint
- [x] Import and use `load_model`, `extract_structural_view`, `to_cytoscape` from extraction
- [x] Handle `ValueError` → HTTP 404
- [x] Handle extraction errors → HTTP 422

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/test_web.py` → All pass
- [x] `uv run python -m pytest proof_of_concept/tests/` → No regressions (24+ tests pass)

**Manual:**
- [x] Import check: `uv run python -c "from proof_of_concept.web.server import app; print('OK')"`

**What We Know Works After This Phase:**
- FastAPI app exists and can be imported
- API endpoint correctly calls extraction pipeline
- Error handling returns appropriate HTTP codes

---

## Phase 2: Entry Point + Static Serving

### Goal

Add `__main__.py` entry point so server can be started with `uv run python -m proof_of_concept.web`, and configure static file serving for the frontend.

### Test Stencil (Write This First)

```python
# Add to proof_of_concept/tests/test_web.py

def test_index_served():
    """GET / returns HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

### Changes Required

**See `design.md` for:**
- Entry point code → `design.md#2-entry-point`
- Static file configuration → `design.md#1-server`

**Specific file changes:**

#### 1. Package Init
**File:** `proof_of_concept/web/__init__.py` (NEW)
- [x] Create empty `__init__.py` (package marker)

#### 2. Entry Point
**File:** `proof_of_concept/web/__main__.py` (NEW)
- [x] Implement uvicorn runner per `design.md#2-entry-point`

#### 3. Static File Serving
**File:** `proof_of_concept/web/server.py` (MODIFY)
- [x] Create `proof_of_concept/web/static/` directory
- [x] Add route for `/` → `static/index.html`
- [x] Mount static files directory

#### 4. Placeholder HTML
**File:** `proof_of_concept/web/static/index.html` (NEW - placeholder)
- [x] Create minimal HTML placeholder: `<html><body>Placeholder</body></html>`

#### 5. Update Tests
**File:** `proof_of_concept/tests/test_web.py` (MODIFY)
- [x] Add `test_index_served` from stencil above

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/test_web.py` → All pass (3 tests)

**Manual:**
- [x] Start server: `uv run python -m proof_of_concept.web` (should show uvicorn startup)
- [x] In another terminal: `curl http://localhost:8000/` → Returns HTML
- [x] `curl http://localhost:8000/api/model/models/tests/coffee_maker` → Returns JSON with elements
- [ ] Ctrl+C stops server cleanly

**What We Know Works After This Phase:**
- Server starts with single command
- Static files are served
- API endpoint still works alongside static serving

---

## Phase 3: Frontend Integration

### Goal

Adapt `cytoscape_demo.html` to fetch from API instead of hardcoded data. This completes the end-to-end workflow.

### Test Stencil (Manual Testing)

No new automated tests - this phase is validated manually per spec acceptance criteria. The existing `test_index_served` confirms HTML is served; frontend behavior is validated in browser.

### Changes Required

**See `design.md` for:**
- Frontend changes → `design.md#3-frontend`
- UI layout → `design.md#3-frontend`
- Error display → `design.md#error-handling`

**Specific file changes:**

#### 1. Frontend Implementation
**File:** `proof_of_concept/web/static/index.html` (REPLACE placeholder)
- [x] Copy structure from `proof_of_concept/cytoscape_demo.html`
- [x] Add model path input field and Load button to control bar
- [x] Remove hardcoded `const cytoscapeData = {...}` (lines 153-279 in original)
- [x] Add `loadModel(path)` function that fetches from `/api/model/{path}`
- [x] Add error display (show message in diagram area or alert)
- [x] Add loading state (disable button during fetch)
- [x] Wire Load button to call `loadModel()` with input value
- [x] Initialize Cytoscape with empty state, re-init on successful fetch

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/` → All pass (no regressions)

**Manual (per spec acceptance criteria):**
- [x] Start server: `uv run python -m proof_of_concept.web`
- [x] Navigate to `http://localhost:8000`
- [x] Enter `models/tests/coffee_maker` in input field
- [x] Click Load → diagram renders with 10 nodes
- [x] Expand/collapse nodes works
- [x] Double-click zoom-to-node works
- [x] Click node shows details in info panel
- [x] Export PNG produces readable image
- [x] Enter invalid path → shows error message

**What We Know Works After This Phase:**
- Complete end-to-end workflow: model file → browser diagram
- All interactive features preserved from POC
- Error handling works for invalid paths

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Key commands:
- Run tests: `uv run python -m pytest proof_of_concept/tests/`
- Start server: `uv run python -m proof_of_concept.web`
- Add deps: `uv add <package>`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Test against same golden reference (10 nodes) to ensure extraction integration works
- **Phase 2**: Test static serving before frontend work to isolate issues
- **Phase 3**: Copy working code from `cytoscape_demo.html` - minimal new JS needed

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Added dependencies: `fastapi`, `uvicorn`, `httpx` (for TestClient)
- Created `proof_of_concept/web/` directory
- Created `proof_of_concept/web/server.py` with FastAPI app and `/api/model/{path:path}` endpoint
- Created `proof_of_concept/tests/test_web.py` with 2 tests

**Issues:**
- TestClient requires `httpx` package (not mentioned in plan) - added via `uv add httpx`

**Deviations:**
- None - implementation matches plan

### Phase 2 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Created `proof_of_concept/web/__init__.py` (package marker with docstring)
- Created `proof_of_concept/web/__main__.py` (uvicorn entry point)
- Created `proof_of_concept/web/static/` directory
- Created `proof_of_concept/web/static/index.html` (placeholder)
- Modified `proof_of_concept/web/server.py` to add FileResponse for `/` and StaticFiles mount
- Added `test_index_served` test to `proof_of_concept/tests/test_web.py`

**Issues:**
- None

**Deviations:**
- None - implementation matches plan

### Phase 3 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Replaced placeholder `index.html` with full Cytoscape viewer (514 lines)
- Added model path input with default value `models/tests/coffee_maker`
- Added Load button with loading state (disables during fetch, shows "Loading...")
- Added `loadModel(path)` async function that fetches from `/api/model/{path}`
- Added message overlay for loading/error states
- Added Enter key support in input field
- Buttons disabled until model is loaded
- All features preserved: expand/collapse, zoom-to-node, info panel, PNG export

**Issues:**
- None

**Deviations:**
- None - implementation matches plan

---

**Status**: Draft → In Progress → Complete
