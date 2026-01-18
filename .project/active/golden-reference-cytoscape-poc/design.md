# Design: Golden Reference + Cytoscape POC

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-18 19:47:36 UTC
**Last Updated:** 2026-01-18
**Branch:** visualization

---

## Overview

Create a hand-written golden reference JSON representing the coffee maker structural hierarchy, and a static Cytoscape.js demo that renders it with hierarchical layout, compound nodes, expand/collapse, and PNG export.

---

## Related Artifacts

- **Spec:** `.project/active/golden-reference-cytoscape-poc/spec.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md`
- **Sprint Plan:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **AST Exploration:** `.project/design-intent/technical/explore_ast.py`
- **Test Model:** `models/tests/coffee_maker/`

---

## Research Findings

### Multiplicity Representation in syside

**Question:** How does syside represent `heater[2]` - as one node with multiplicity, or multiple nodes?

**Answer:** Single node with multiplicity bounds. Investigation shows:
- `heater` appears as **one PartUsage** with `declared_multiplicity.cached_lower_bound = 2`
- The golden reference should match this: one node with `multiplicity: [2, 2]` (or `[2, 3]` based on current model)

**Verification command:**
```bash
uv run python -c "
import syside
model, _ = syside.try_load_model(['models/tests/coffee_maker/library.sysml', 'models/tests/coffee_maker/design.sysml'])
for part in model.nodes(syside.PartUsage, include_subtypes=True):
    if part.declared_multiplicity:
        print(f'{part.name}: [{part.declared_multiplicity.cached_lower_bound}..{part.declared_multiplicity.cached_upper_bound}]')
"
```

### Name Derivation from Redefines

**Finding:** Parts using `part redefines X` syntax have:
- `declared_name = None`
- `name` = derived from redefined feature (e.g., "brewing")

The golden reference should use the computed `name` property, which gives the expected user-visible name.

### Coffee Maker Structure (Verified)

From syside extraction:
```
coffee_maker : Coffee Maker
├── brewing : Brewing System
│   ├── heater : Heating Element [2]
│   ├── pump : Water Pump
│   └── chamber : Brew Chamber
├── reservoir : Water Reservoir
├── carafe : Carafe
└── housing : Housing
    ├── shell : Outer Shell
    └── panel : Control Panel
```

**Total: 10 nodes, 9 containment edges**

### Cytoscape.js Extension Research

**Required extensions:**
1. **cytoscape-dagre** (v2.5.0+) - Dagre layout for directed graphs
   - CDN: `https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js`
   - Depends on: dagre (bundled or separate)

2. **cytoscape-expand-collapse** (v4.1.0+) - Compound node expand/collapse
   - CDN: `https://unpkg.com/cytoscape-expand-collapse@4.1.0/cytoscape-expand-collapse.js`
   - Provides: `cy.expandCollapse()` API

**CDN dependencies for demo:**
```html
<!-- Cytoscape.js core -->
<script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>

<!-- Dagre layout -->
<script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>

<!-- Expand-collapse -->
<script src="https://unpkg.com/cytoscape-expand-collapse@4.1.0/cytoscape-expand-collapse.js"></script>
```

---

## Proposed Design

### Component 1: Golden Reference JSON

**File:** `proof_of_concept/golden_references/coffee_maker_structural.json`

**Purpose:** Hand-written JSON defining the expected structural view output for the coffee maker model. This becomes the test fixture for Item 2 (extraction implementation).

**Schema:** Follows `ViewResult` from sprint plan Part 4.1-4.2:

```json
{
  "nodes": [
    {
      "id": "n1",
      "name": "coffee_maker",
      "type_name": "Coffee Maker",
      "element_type": "part",
      "parent": null,
      "depth": 0,
      "multiplicity": null
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "n1",
      "target": "n2",
      "edge_type": "containment"
    }
  ],
  "metadata": {
    "view": "structural",
    "root": "coffee_maker",
    "total_nodes": 10,
    "max_depth": 2
  }
}
```

**Node mapping (10 nodes):**

| id | name | type_name | parent | depth | multiplicity |
|----|------|-----------|--------|-------|--------------|
| n1 | coffee_maker | Coffee Maker | null | 0 | null |
| n2 | brewing | Brewing System | n1 | 1 | null |
| n3 | heater | Heating Element | n2 | 2 | [2, 2] |
| n4 | pump | Water Pump | n2 | 2 | null |
| n5 | chamber | Brew Chamber | n2 | 2 | null |
| n6 | reservoir | Water Reservoir | n1 | 1 | null |
| n7 | carafe | Carafe | n1 | 1 | null |
| n8 | housing | Housing | n1 | 1 | null |
| n9 | shell | Outer Shell | n8 | 2 | null |
| n10 | panel | Control Panel | n8 | 2 | null |

**Edge mapping (9 edges):**

| id | source | target | edge_type |
|----|--------|--------|-----------|
| e1 | n1 | n2 | containment |
| e2 | n2 | n3 | containment |
| e3 | n2 | n4 | containment |
| e4 | n2 | n5 | containment |
| e5 | n1 | n6 | containment |
| e6 | n1 | n7 | containment |
| e7 | n1 | n8 | containment |
| e8 | n8 | n9 | containment |
| e9 | n8 | n10 | containment |

**Note on heater multiplicity:** The current model shows `[2..3]` in syside due to `heater_count` attribute bounds. For the golden reference, I'll use `[2, 2]` to match the expected default (2 heaters). This can be adjusted based on user preference.

### Component 2: Cytoscape Demo HTML

**File:** `proof_of_concept/cytoscape_demo.html`

**Purpose:** Single-page HTML application that loads the golden reference JSON and renders it using Cytoscape.js with all required features.

**Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                    cytoscape_demo.html                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Control Bar                                         │   │
│  │  [Expand All] [Collapse All] [Fit View] [Export PNG] │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │              Cytoscape.js Canvas                      │   │
│  │                                                       │   │
│  │     ┌─────────────────────────────────────────┐      │   │
│  │     │ coffee_maker                            │      │   │
│  │     │  ┌───────────┐  ┌───────────┐          │      │   │
│  │     │  │ brewing   │  │ housing   │          │      │   │
│  │     │  │ ┌───────┐ │  │ ┌───────┐ │          │      │   │
│  │     │  │ │heater │ │  │ │ shell │ │          │      │   │
│  │     │  │ └───────┘ │  │ └───────┘ │          │      │   │
│  │     │  └───────────┘  └───────────┘          │      │   │
│  │     └─────────────────────────────────────────┘      │   │
│  │                                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Info Panel (selected node details)                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key Functions:**

1. **`loadGoldenReference()`** - Fetch and parse JSON file
2. **`convertToCytoscape(viewResult)`** - Transform ViewResult to Cytoscape format
3. **`initCytoscape(elements)`** - Initialize Cytoscape instance with layout and styles
4. **`setupExpandCollapse(cy)`** - Register expand-collapse extension
5. **`setupEventHandlers(cy)`** - Click handlers for zoom-to-node, selection
6. **`exportPNG(cy)`** - Export diagram at 2x resolution

**Data Flow:**

```
golden_reference.json
        │
        ▼
  loadGoldenReference()
        │
        ▼
  convertToCytoscape()      // Wrap nodes/edges in { data: {...} }
        │
        ▼
  initCytoscape()           // Create cy instance with dagre layout
        │
        ▼
  setupExpandCollapse()     // Enable compound node collapse
        │
        ▼
  Interactive diagram ready
```

**Cytoscape Initialization:**

```javascript
const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: elements,
  style: stylesheet,  // See below
  layout: {
    name: 'dagre',
    rankDir: 'TB',           // Top-to-bottom
    nodeSep: 50,             // Spacing between nodes
    rankSep: 80,             // Spacing between ranks
    fit: true,
    padding: 30
  }
});
```

**Stylesheet (from sprint plan Part 4.3, adapted):**

```javascript
const stylesheet = [
  // All nodes - base style
  {
    selector: 'node',
    style: {
      'label': 'data(label)',
      'text-valign': 'top',
      'text-margin-y': 8,
      'font-size': 12,
      'font-weight': 'bold'
    }
  },
  // Part nodes (compound containers)
  {
    selector: 'node[element_type="part"]',
    style: {
      'shape': 'round-rectangle',
      'background-color': '#e3f2fd',
      'border-color': '#1976d2',
      'border-width': 2,
      'padding': 20
    }
  },
  // Leaf nodes (no children) - smaller
  {
    selector: 'node:childless',
    style: {
      'width': 120,
      'height': 40,
      'text-valign': 'center',
      'text-margin-y': 0
    }
  },
  // Selection highlight
  {
    selector: ':selected',
    style: {
      'border-width': 4,
      'border-color': '#ff5722'
    }
  },
  // Collapsed indicator
  {
    selector: '.cy-expand-collapse-collapsed-node',
    style: {
      'border-style': 'double',
      'border-width': 4
    }
  }
];
```

**Expand/Collapse Setup:**

```javascript
cy.expandCollapse({
  layoutBy: {
    name: 'dagre',
    animate: true,
    animationDuration: 300,
    rankDir: 'TB'
  },
  fisheye: false,
  animate: true,
  undoable: false
});
```

**Zoom-to-Node:**

```javascript
cy.on('dbltap', 'node', function(evt) {
  const node = evt.target;
  cy.animate({
    fit: { eles: node, padding: 50 },
    duration: 300
  });
});
```

**PNG Export:**

```javascript
function exportPNG() {
  const png = cy.png({
    output: 'blob',
    scale: 2,  // 2x resolution
    bg: 'white'
  });

  const link = document.createElement('a');
  link.href = URL.createObjectURL(png);
  link.download = 'coffee_maker_diagram.png';
  link.click();
}
```

**Multiplicity Label Handling:**

For nodes with multiplicity, the label should include the multiplicity notation:

```javascript
function getNodeLabel(node) {
  const name = node.name;
  const mult = node.multiplicity;
  if (mult) {
    if (mult[0] === mult[1]) {
      return `${name} [${mult[0]}]`;
    } else {
      return `${name} [${mult[0]}..${mult[1] || '*'}]`;
    }
  }
  return name;
}
```

### File Structure

```
proof_of_concept/
├── golden_references/
│   └── coffee_maker_structural.json   # ViewResult JSON
├── cytoscape_demo.html                 # Self-contained demo page
└── README.md                           # Setup/usage instructions
```

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Dagre layout doesn't handle deep nesting well | Low | Medium | Coffee maker is only 3 levels; adjust `nodeSep`/`rankSep` if needed |
| Expand-collapse extension version incompatibility | Low | Medium | Pin to specific versions in CDN URLs |
| PNG export quality issues | Low | Low | Using 2x scale factor; can adjust |
| Golden reference doesn't match actual syside extraction | Medium | Low | This is the purpose of Item 2 - test and iterate |

---

## Integration Strategy

**How this fits the sprint:**

1. **Item 1 (this):** Create golden reference + validate Cytoscape rendering
2. **Item 2:** Implement `extract_structural_view()`, test against golden reference
3. **Item 3:** Connect extraction to Cytoscape demo via CLI
4. **Item 4:** Wrap in web server
5. **Item 5:** Add cost annotations

**The golden reference becomes the contract** between rendering (Cytoscape) and extraction (Python). If the Cytoscape demo works with the golden reference, we have confidence that extraction output in the same format will also render correctly.

---

## Validation Approach

### Manual Testing

1. Open `cytoscape_demo.html` in browser
2. Verify 10 nodes visible (may need to expand)
3. Verify hierarchy matches coffee maker structure
4. Click expand/collapse on `brewing` and `housing` - verify children toggle
5. Double-click a node - verify zoom-to-fit
6. Click "Export PNG" - verify download and image quality
7. Open browser console - verify no errors

### Verification Checklist

- [ ] JSON is valid (use `jq . golden_references/coffee_maker_structural.json`)
- [ ] 10 nodes present
- [ ] 9 edges present
- [ ] Heater shows multiplicity `[2]` in diagram
- [ ] Dagre layout produces readable hierarchy
- [ ] Expand/collapse toggles correctly
- [ ] PNG export at 2x resolution

---

## Implementation Notes

### JSON File Creation

Create `proof_of_concept/golden_references/coffee_maker_structural.json` with exact schema from sprint plan Part 4.2. Use the node/edge mapping tables above.

### HTML File Creation

Single file with embedded JavaScript. Include:
1. CDN script tags for dependencies
2. Stylesheet definition
3. `DOMContentLoaded` handler that:
   - Fetches golden reference JSON (relative path)
   - Converts to Cytoscape format
   - Initializes Cytoscape
   - Sets up expand-collapse and event handlers
4. Export button click handler

### Serving the Demo

The demo requires serving from an HTTP server (not `file://`) due to fetch API:

```bash
# From proof_of_concept directory:
python -m http.server 8080
# Then open http://localhost:8080/cytoscape_demo.html
```

Alternatively, embed the JSON directly in the HTML to avoid the fetch requirement.

---

**Completed:** 2026-01-18
