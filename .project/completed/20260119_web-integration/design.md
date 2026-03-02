# Design: Web Integration

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-18 23:47:00 UTC
**Branch:** visualization

---

## Overview

Minimal FastAPI web application that serves an interactive Cytoscape.js diagram for any SysML model, eliminating the manual copy-paste workflow currently required.

## Related Artifacts

- **Spec:** `.project/active/web-integration/spec.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md` (Item 4)
- **Research:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Dependencies:** `proof_of_concept/extraction/` (Items 2-3)

---

## Research Findings

### Existing Extraction API

The extraction pipeline (`proof_of_concept/extraction/visualization.py`) provides:

| Function | Purpose | Returns |
|----------|---------|---------|
| `load_model(path)` | Load SysML model from directory or file | syside model object |
| `extract_structural_view(model, root=None)` | Extract containment hierarchy | `StructuralViewResult` dict |
| `to_cytoscape(view_result)` | Convert to Cytoscape.js format | `{"elements": [...]}` |

Error handling pattern (from `visualization.py:332-342`):
- `load_model()` raises `ValueError` for invalid path or model errors
- `extract_structural_view()` returns error in metadata: `{"metadata": {"error": "..."}}`

### Existing Frontend

`proof_of_concept/cytoscape_demo.html` contains:
- Complete Cytoscape.js rendering with dagre layout
- Expand/collapse, zoom-to-node, info panel, PNG export
- Data is currently embedded as `const cytoscapeData = {...}` (line 153)
- All JS libraries loaded from CDN (Cytoscape, dagre, expand-collapse)

The frontend expects `{elements: [...]}` format - exactly what `to_cytoscape()` produces.

### Project Patterns

- **Package management:** `uv` (per CLAUDE.md)
- **Testing:** pytest with fixtures in `conftest.py`
- **Dependencies:** Listed in `pyproject.toml` - FastAPI not currently installed

---

## Proposed Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser                                  │
│  ┌─────────────┐    ┌──────────────────────────────────────┐   │
│  │ Model Path  │───▶│        Cytoscape.js Diagram          │   │
│  │   Input     │    │  (expand/collapse, zoom, info panel) │   │
│  └─────────────┘    └──────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTP
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Server (server.py)                    │
│  ┌───────────────────────┐    ┌──────────────────────────────┐ │
│  │ GET /api/model/{path} │    │  Static: / → index.html      │ │
│  └───────────┬───────────┘    └──────────────────────────────┘ │
│              │                                                   │
│              ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ load_model() → extract_structural_view() → to_cytoscape()│   │
│  │            (from proof_of_concept.extraction)            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### File Structure

```
proof_of_concept/
├── web/
│   ├── __init__.py      # Package marker
│   ├── __main__.py      # Entry point: uv run python -m proof_of_concept.web
│   ├── server.py        # FastAPI app and routes
│   └── static/
│       └── index.html   # Frontend (adapted from cytoscape_demo.html)
├── extraction/          # (existing)
└── ...
```

### Component Details

#### 1. Server (`proof_of_concept/web/server.py`)

**Purpose:** FastAPI application with API endpoint and static file serving.

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from proof_of_concept.extraction import load_model, extract_structural_view, to_cytoscape

app = FastAPI(title="SysML Structural View")

@app.get("/api/model/{path:path}")
def get_model_view(path: str) -> dict:
    """Return Cytoscape.js elements for model at path."""
    ...

# Static files and index route
```

**API Endpoint:**
- Route: `GET /api/model/{path:path}`
- Path parameter uses `path` converter to allow slashes (e.g., `models/tests/coffee_maker`)
- Returns: `{"elements": [...]}` on success
- Returns: HTTP 404 with `{"detail": "..."}` for invalid path
- Returns: HTTP 422 with `{"detail": "..."}` for extraction errors

**Error Handling:**
- Catch `ValueError` from `load_model()` → HTTP 404
- Check `metadata.error` from extraction → HTTP 422
- Both return JSON with `detail` field for frontend display

**Static Files:**
- Mount `static/` directory at root
- Explicit route for `/` → `static/index.html`

#### 2. Entry Point (`proof_of_concept/web/__main__.py`)

**Purpose:** Allow running with `uv run python -m proof_of_concept.web`

```python
import uvicorn
from .server import app

def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
```

Default port 8000 matches spec acceptance criteria.

#### 3. Frontend (`proof_of_concept/web/static/index.html`)

**Purpose:** Interactive diagram viewer with model path input.

**Changes from existing `cytoscape_demo.html`:**

1. **Add model path input** - Text input + "Load" button in control bar
2. **Remove hardcoded data** - Replace `const cytoscapeData = {...}` with empty initial state
3. **Add fetch logic** - On "Load" click, fetch from `/api/model/{path}`
4. **Add error display** - Show user-friendly message if fetch fails
5. **Add loading state** - Disable button and show spinner during fetch

**Preserved features** (no changes needed):
- Cytoscape.js initialization and styling
- Expand/collapse functionality
- Zoom-to-node (double-click)
- Info panel (click node)
- PNG export

**UI Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Structural View    [models/tests/coffee_maker] [Load] [Export] │
├─────────────────────────────────────────────────────────────────┤
│                                                    │ Node Info  │
│                   Cytoscape Diagram                │            │
│                                                    │ Name: ...  │
│                                                    │ Type: ...  │
└────────────────────────────────────────────────────┴────────────┘
```

### Dependencies

**New dependencies to add:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server

Add via:
```bash
uv add fastapi uvicorn
```

### Data Flow

1. User navigates to `http://localhost:8000`
2. Server returns `static/index.html`
3. User enters model path (e.g., `models/tests/coffee_maker`)
4. Frontend fetches `GET /api/model/models/tests/coffee_maker`
5. Server calls: `load_model(path)` → `extract_structural_view(model)` → `to_cytoscape(result)`
6. Server returns `{"elements": [...]}`
7. Frontend initializes Cytoscape with elements
8. User interacts (expand/collapse, zoom, info panel, export)

### Error Handling

| Scenario | Server Response | Frontend Display |
|----------|-----------------|------------------|
| Path doesn't exist | 404 `{"detail": "Model path not found: ..."}` | "Model not found: ..." |
| Model has errors | 422 `{"detail": "Model has errors: ..."}` | "Model error: ..." |
| No root element found | 422 `{"detail": "Root element not found"}` | "No structural elements found" |
| Network error | - | "Failed to connect to server" |

### Testing Strategy

**New test file:** `proof_of_concept/tests/test_web.py`

Tests using FastAPI TestClient:
1. `test_get_model_valid_path` - Returns 200 with elements
2. `test_get_model_invalid_path` - Returns 404
3. `test_index_served` - GET `/` returns HTML
4. `test_elements_match_cli` - API output matches CLI output for same model

**Manual validation:**
- Start server: `uv run python -m proof_of_concept.web`
- Navigate to `http://localhost:8000`
- Enter `models/tests/coffee_maker`
- Verify diagram renders with all 10 nodes
- Test expand/collapse, zoom, info panel
- Export PNG

---

## Potential Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Path traversal (security) | Low | FastAPI path validation + model loading validates path exists |
| Large model performance | Low (POC) | Out of scope; note for future |
| CDN unavailability | Very Low | Libraries are stable CDN URLs; could vendor later |

---

## Integration Strategy

This completes the POC vertical slice. After this:
- Item 5 adds cost annotations to this same frontend
- Future work could add model file watching, multiple views, etc.

The web server is additive - existing CLI and `cytoscape_demo.html` remain functional.

---

## Validation Approach

**Automated:**
- New tests in `proof_of_concept/tests/test_web.py`
- Existing extraction tests continue passing

**Manual (per spec acceptance criteria):**
- [x] Navigate to `http://localhost:8000`
- [x] Enter `models/tests/coffee_maker` → diagram renders
- [x] Expand/collapse works
- [x] Double-click zoom works
- [x] Info panel shows on click
- [x] PNG export produces image
- [x] Invalid path shows error message

---

**Implementation Complete:** 2026-01-19
