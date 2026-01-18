# Implementation Plan: Golden Reference + Cytoscape POC

**Status:** Complete
**Created:** 2026-01-18 19:55:02 UTC
**Last Updated:** 2026-01-18

## Source Documents

- **Spec:** `.project/active/golden-reference-cytoscape-poc/spec.md`
- **Design:** `.project/active/golden-reference-cytoscape-poc/design.md` - See here for component details, data schemas, code snippets

## Implementation Strategy

**Phasing Rationale:**
This is a static file creation task (JSON + HTML) with no code dependencies. We build incrementally:
1. Create the data (golden reference JSON) first
2. Render it with core Cytoscape functionality
3. Add interactive features last

Each phase produces a verifiable artifact. No automated tests - validation is manual/visual since we're creating static demo files.

**Overall Validation Approach:**
- JSON validation via `jq`
- Browser-based manual testing for HTML
- Console check for JavaScript errors

---

## Phase 1: Golden Reference JSON

### Goal

Create the hand-written ViewResult JSON defining the coffee maker structural hierarchy. This becomes the test fixture for Item 2 (extraction) and the data source for the Cytoscape demo.

### Changes Required

**See `design.md` for:**
- Schema definition → `design.md#component-1-golden-reference-json`
- Node mapping table (10 nodes) → `design.md#component-1-golden-reference-json`
- Edge mapping table (9 edges) → `design.md#component-1-golden-reference-json`

**Specific file changes:**

#### 1. Create directory structure
- [x] `mkdir -p proof_of_concept/golden_references`

#### 2. Golden Reference JSON
**File:** `proof_of_concept/golden_references/coffee_maker_structural.json` (NEW)
- [x] Create file with ViewResult schema
- [x] Add 10 nodes per mapping table in design.md
- [x] Add 9 containment edges per mapping table
- [x] Add metadata section

### Validation

**Automated:**
- [x] `jq . proof_of_concept/golden_references/coffee_maker_structural.json` → Valid JSON, no errors
- [x] `jq '.nodes | length' proof_of_concept/golden_references/coffee_maker_structural.json` → Returns `10`
- [x] `jq '.edges | length' proof_of_concept/golden_references/coffee_maker_structural.json` → Returns `9`

**Manual:**
- [x] Review JSON structure matches design.md schema
- [x] Verify heater node has `multiplicity: [2, 2]`
- [x] Verify parent references are correct (n2→n1, n3→n2, etc.)

**What We Know Works After This Phase:**
- ViewResult data shape is finalized
- Golden reference is ready for Cytoscape demo and future extraction tests

---

## Phase 2: Cytoscape Demo - Core Rendering

### Goal

Create the HTML demo that loads the golden reference JSON and renders a basic diagram with dagre layout and compound nodes. Validates that Cytoscape.js can handle our data shape before adding interactive features.

### Changes Required

**See `design.md` for:**
- CDN dependencies → `design.md#cytoscape-js-extension-research`
- Cytoscape initialization → `design.md#component-2-cytoscape-demo-html`
- Stylesheet → `design.md#component-2-cytoscape-demo-html`
- Data flow → `design.md#component-2-cytoscape-demo-html`

**Specific file changes:**

#### 1. Cytoscape Demo HTML
**File:** `proof_of_concept/cytoscape_demo.html` (NEW)
- [x] Create HTML structure with container div
- [x] Add CDN script tags (cytoscape, dagre, cytoscape-dagre)
- [x] Add basic CSS for full-page layout
- [x] Implement `convertToCytoscape()` function
- [x] Implement `initCytoscape()` with dagre layout
- [x] Add `DOMContentLoaded` handler to load JSON and render

**Note:** For Phase 2, embed JSON directly in HTML to avoid fetch/CORS issues. Phase 3 can switch to external fetch if desired.

### Validation

**Automated:**
- [x] Open in browser → No console errors

**Manual:**
- [x] Diagram renders with visible hierarchy
- [x] 3-level nesting visible: coffee_maker contains brewing/housing, which contain children
- [x] Compound nodes display correctly (nested boxes)
- [x] Dagre layout produces readable arrangement (no overlapping)
- [x] Heater label shows `heater [2]` (multiplicity)

**What We Know Works After This Phase:**
- Cytoscape.js renders compound nodes with dagre layout
- ViewResult → Cytoscape format conversion works
- Core rendering pipeline is validated

---

## Phase 3: Interactive Features + Polish

### Goal

Add expand/collapse, zoom-to-node, PNG export, control bar, and info panel. Complete all acceptance criteria from spec.

### Changes Required

**See `design.md` for:**
- Expand/collapse setup → `design.md#component-2-cytoscape-demo-html`
- Zoom-to-node → `design.md#component-2-cytoscape-demo-html`
- PNG export → `design.md#component-2-cytoscape-demo-html`
- UI architecture diagram → `design.md#component-2-cytoscape-demo-html`

**Specific file changes:**

#### 1. Update Cytoscape Demo
**File:** `proof_of_concept/cytoscape_demo.html` (MODIFY)
- [x] Add cytoscape-expand-collapse CDN script
- [x] Add control bar HTML (Expand All, Collapse All, Fit View, Export PNG buttons)
- [x] Add info panel HTML for selected node details
- [x] Implement `setupExpandCollapse()` function
- [x] Implement `exportPNG()` function
- [x] Add double-click zoom-to-node handler
- [x] Add click handler to update info panel
- [x] Add button click handlers
- [x] Style collapsed nodes with double border

#### 2. README
**File:** `proof_of_concept/README.md` (NEW)
- [x] Add setup instructions (serve via HTTP server)
- [x] Document features and usage
- [x] Note that this is POC for visualization sprint

### Validation

**Automated:**
- [x] Open in browser → No console errors

**Manual (per spec acceptance criteria):**
- [x] Click "Collapse All" → Compound nodes collapse, showing double border
- [x] Click "Expand All" → All children visible again
- [x] Double-click `brewing` node → View zooms to fit that node
- [x] Click "Fit View" → Diagram fits to viewport
- [x] Click "Export PNG" → Downloads `coffee_maker_diagram.png`
- [x] Open exported PNG → Image is clear at 2x resolution, shows full hierarchy
- [x] Click a node → Info panel shows node details (name, type, depth)

**Final Acceptance Checklist (from spec):**
- [x] `proof_of_concept/golden_references/coffee_maker_structural.json` exists and is valid JSON
- [x] JSON contains 10 nodes matching coffee maker hierarchy
- [x] JSON contains 9 containment edges
- [x] `proof_of_concept/cytoscape_demo.html` opens in browser without errors
- [x] Diagram displays with 3-level nesting visible
- [x] Clicking expand/collapse toggles child visibility
- [x] Double-clicking a node zooms to fit it
- [x] Export button produces a PNG file
- [x] PNG shows the diagram clearly at 2x resolution
- [x] No console errors in browser developer tools
- [x] Diagram layout is automatically computed (no manual positioning)

**What We Know Works After This Phase:**
- Full POC is complete and ready for demo
- All interactive features work as expected
- PNG export produces publication-quality images
- Ready to proceed with Item 2 (extraction implementation)

---

## Environment Setup

**Serving the demo:**
```bash
cd proof_of_concept
python -m http.server 8080
# Open http://localhost:8080/cytoscape_demo.html
```

**Note:** Phase 2 embeds JSON to avoid server requirement during initial development. Phase 3 can optionally switch to fetch.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 2:** If dagre layout doesn't handle compound nodes well, adjust `nodeSep`/`rankSep` parameters or try different layout options
- **Phase 3:** If expand-collapse extension has issues, pin to known working version or implement manual collapse via CSS

---

## Implementation Notes

[IMPLEMENTATION COMPLETE]

### Phase 1 Completion
**Completed:** 2026-01-18
**Actual Changes:**
- Created `proof_of_concept/golden_references/` directory
- Created `proof_of_concept/golden_references/coffee_maker_structural.json` with ViewResult schema
- 10 nodes representing coffee maker hierarchy (coffee_maker → brewing/reservoir/carafe/housing → children)
- 9 containment edges connecting parent → child relationships
- Heater node includes multiplicity `[2, 2]` per design spec

**Issues:** None

**Deviations:** None - implemented exactly as specified in design.md

### Phase 2 Completion
**Completed:** 2026-01-18
**Actual Changes:**
- Created `proof_of_concept/cytoscape_demo.html` with embedded golden reference JSON
- CDN dependencies: cytoscape@3.28.1, dagre@0.8.5, cytoscape-dagre@2.5.0
- Implemented `convertToCytoscape()` to transform ViewResult → Cytoscape elements
- Implemented `getNodeLabel()` for multiplicity notation (e.g., "heater [2]")
- Dagre layout with TB direction, 50px node separation, 80px rank separation
- Stylesheet with compound node styling (blue borders, light blue background)

**Issues:** None

**Deviations:** None - core rendering works as specified

### Phase 3 Completion
**Completed:** 2026-01-18
**Actual Changes:**
- Added cytoscape-expand-collapse@4.1.0 CDN dependency
- Added control bar with title and 4 buttons (Expand All, Collapse All, Fit View, Export PNG)
- Added info panel (280px sidebar) showing node details on click
- Implemented `setupExpandCollapse()` with dagre relayout on expand/collapse
- Implemented `exportPNG()` with 2x scale, white background, blob download
- Added `dbltap` handler for zoom-to-node animation
- Added `tap` handler for info panel updates
- Added collapsed node styling (double border, darker blue)
- Created `proof_of_concept/README.md` with setup instructions and data schema docs

**Issues:** None

**Deviations:** None - all features implemented as specified

---

**Status**: Complete
