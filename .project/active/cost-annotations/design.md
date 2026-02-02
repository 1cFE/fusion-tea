# Design: Cost Annotations + Polish

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-19 00:54:29 UTC
**Branch:** visualization
**Commit:** 905c155

---

## Overview

Add cost attribute extraction to the structural view and enable cost-based node styling in the web UI, completing the visualization POC sprint.

## Related Artifacts

- **Spec:** `.project/active/cost-annotations/spec.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md` (Item 5)
- **Sprint Plan:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Test Model:** `models/tests/coffee_maker/`

---

## Research Findings

### Cost Extraction Patterns

The codebase has proven patterns for extracting attribute values from SysML models in `models/tests/coffee_maker/generate_costs.py`.

**Key accessors for cost attributes:**

| Pattern | Source | Purpose |
|---------|--------|---------|
| `owned_members` / `owned_features` | `generate_costs.py:122-130` | Iterate attributes on a definition |
| `feature_value_expression` | `generate_costs.py:137-142` | Get value expression from attribute |
| `isinstance(syside.AttributeUsage)` | `types.py:123-129` | Type check for attributes |
| Follow `.types[0]` to definition | `visualization.py:283-296` | Get child features via type definition |

**Cost attribute structure in coffee maker:**

The model defines cost attributes on part definitions via the `'Costed Component'` abstract base:
```sysml
abstract part def 'Costed Component' {
    attribute capital_cost : Real;
    attribute raw_material_cost : Real;
    attribute fabrication_cost : Real;
    attribute installation_cost : Real;
    attribute idiot_index : Real;
}
```

Each concrete part redefines these via embedded calc models:
```sysml
part def 'Heating Element' :> 'Costed Component' {
    calc cost_model : HeatingElementCostCalc { ... }
    :>> capital_cost = cost_model.total_cost;
}
```

**Critical insight:** Cost attributes are defined on the **PartDefinition**, not the PartUsage. To extract them:
1. Get the part's type definition via `.types[0]`
2. Iterate `type_def.owned_features` for `AttributeUsage` elements
3. Filter by attribute name matching requested cost attributes
4. Extract value from `feature_value_expression` (may need evaluation)

### Value Extraction Approach

Cost attributes in this model are **computed expressions**, not literals. The `feature_value_expression` references a calc output (e.g., `cost_model.total_cost`), which requires evaluation.

**Decision:** Reuse the existing `generate_costs.py` evaluation logic. This script already has working code (~200 lines) that:
- Parses expression ASTs
- Follows feature references
- Topologically sorts dependencies
- Evaluates arithmetic
- Returns final numeric values

We'll refactor the key evaluation functions into a reusable module (or call `generate_costs.py` directly) rather than duplicating this logic in `visualization.py`.

### Cytoscape Visualization Options

The web UI (`proof_of_concept/web/static/index.html`) uses Cytoscape.js with existing patterns we can extend.

**Color-based styling (heatmap):**
```javascript
// Compute normalized value and interpolate color
function lerpColor(color1, color2, t) { /* linear interpolation */ }

cy.nodes().forEach(node => {
  const cost = node.data('capital_cost');
  const normalized = (cost - minCost) / (maxCost - minCost);
  const color = lerpColor('#ffffff', '#ff0000', normalized);
  node.style('background-color', color);
});
```

**Size-based styling:**
```javascript
{
  selector: 'node',
  style: {
    'width': 'mapData(capital_cost, minVal, maxVal, 50, 200)',
    'height': 'mapData(capital_cost, minVal, maxVal, 50, 200)'
  }
}
```

**Style toggle pattern:** Define multiple stylesheet variants and switch with `cy.style().fromJson(stylesheet).update()`.

---

## Proposed Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Flow                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SysML Model                                                    │
│      │                                                          │
│      ▼                                                          │
│  extract_structural_view(model, include_cost_attributes=[...]) │
│      │                                                          │
│      ├── For each PartUsage node:                              │
│      │   1. Get type definition via .types[0]                  │
│      │   2. Find AttributeUsage matching cost attr names       │
│      │   3. Extract/evaluate value                             │
│      │   4. Populate node["costs"] dict                        │
│      │                                                          │
│      ▼                                                          │
│  StructuralViewResult (with costs)                             │
│      │                                                          │
│      ▼                                                          │
│  to_cytoscape(view_result)                                     │
│      │                                                          │
│      ├── Pass costs through to element data                    │
│      │                                                          │
│      ▼                                                          │
│  Cytoscape Elements JSON                                       │
│      │                                                          │
│      ▼                                                          │
│  Web UI                                                         │
│      ├── Info panel shows costs when node selected             │
│      └── Toggle applies color/size styling by capital_cost     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component 1: TypedDict Update

**File:** `proof_of_concept/extraction/types.py`

**Changes:**
```python
class StructuralNode(TypedDict):
    id: str
    name: str
    type_name: str
    element_type: str
    parent: str | None
    depth: int
    multiplicity: list[int] | None
    costs: dict[str, float] | None  # NEW: attribute name → value
```

### Component 2: Cost Extraction

**File:** `proof_of_concept/extraction/visualization.py`

**API change:**
```python
def extract_structural_view(
    model,
    root: str | None = None,
    max_depth: int = 10,
    include_multiplicity: bool = True,
    exclude_stdlib: bool = True,
    include_cost_attributes: list[str] | None = None,  # NEW
) -> StructuralViewResult:
```

**New helper function:**
```python
def _extract_cost_attributes(
    type_def,
    attribute_names: list[str],
) -> dict[str, float] | None:
    """Extract cost attribute values from a type definition.

    Args:
        type_def: PartDefinition to extract costs from
        attribute_names: List of attribute names to extract

    Returns:
        Dict mapping attribute name to value, or None if no costs found
    """
```

**Implementation strategy:**

Reuse the evaluation logic from `generate_costs.py`:

1. Refactor `generate_costs.py` to expose a `compute_costs(model_path) -> dict[str, CostResult]` function
2. In `_extract_node()`, after building the node, look up costs by qualified path
3. Populate `node["costs"]` with the computed values

This avoids duplicating the expression evaluation logic and leverages tested code.

### Component 3: Cytoscape Converter Update

**File:** `proof_of_concept/extraction/visualization.py`

**Update `to_cytoscape()`:**
```python
def to_cytoscape(view_result: StructuralViewResult) -> dict:
    elements = []
    for node in view_result["nodes"]:
        data = {
            "id": node["id"],
            "label": _format_label(node["name"], node.get("multiplicity")),
            "name": node["name"],
            "type_name": node["type_name"],
            "element_type": node["element_type"],
            "parent": node["parent"],
            "depth": node["depth"],
            "multiplicity": node.get("multiplicity"),
        }
        # Add cost fields if present
        costs = node.get("costs")
        if costs:
            data["costs"] = costs
            # Also flatten for Cytoscape mapData access
            for attr_name, value in costs.items():
                data[attr_name] = value
        elements.append({"data": data})
    return {"elements": elements}
```

### Component 4: Server API Update

**File:** `proof_of_concept/web/server.py`

**Update endpoint to always include costs:**
```python
# Default cost attributes for coffee maker demo
DEFAULT_COST_ATTRIBUTES = [
    "capital_cost",
    "raw_material_cost",
    "fabrication_cost",
    "installation_cost",
    "idiot_index",
]

@app.get("/api/model/{path:path}")
def get_model_view(path: str) -> dict:
    model = load_model(path)
    view_result = extract_structural_view(
        model,
        include_cost_attributes=DEFAULT_COST_ATTRIBUTES,
    )
    return to_cytoscape(view_result)
```

### Component 5: Web UI Updates

**File:** `proof_of_concept/web/static/index.html`

#### 5a. Info Panel Cost Display

Update `updateInfoPanel()` function (around line 357):

```javascript
function updateInfoPanel(node) {
  const data = node.data();

  // ... existing fields ...

  // Cost section
  let costHtml = '';
  if (data.costs && Object.keys(data.costs).length > 0) {
    costHtml = `
      <div class="field">
        <div class="field-label">Costs</div>
        <div class="field-value cost-table">
          ${Object.entries(data.costs).map(([name, value]) => `
            <div class="cost-row">
              <span class="cost-name">${formatCostName(name)}</span>
              <span class="cost-value">${formatCostValue(value)}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  infoContent.innerHTML = `
    <!-- existing fields -->
    ${costHtml}
  `;
}

function formatCostName(name) {
  // capital_cost → Capital Cost
  return name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function formatCostValue(value) {
  if (typeof value !== 'number') return '-';
  return value.toFixed(2);
}
```

**Add CSS for cost display:**
```css
.cost-table {
  font-family: monospace;
  font-size: 13px;
}
.cost-row {
  display: flex;
  justify-content: space-between;
  padding: 2px 0;
  border-bottom: 1px solid #eee;
}
.cost-name {
  color: #666;
}
.cost-value {
  font-weight: 500;
}
```

#### 5b. Style Toggle Control

Add toggle button to control bar (after export button):
```html
<div class="spacer"></div>
<label style="font-size: 13px; display: flex; align-items: center; gap: 6px;">
  <input type="checkbox" id="cost-styling-toggle">
  Color by Cost
</label>
```

#### 5c. Cost-Based Styling

Add color interpolation and styling functions:

```javascript
// Linear color interpolation
function lerpColor(color1, color2, t) {
  const r1 = parseInt(color1.slice(1, 3), 16);
  const g1 = parseInt(color1.slice(3, 5), 16);
  const b1 = parseInt(color1.slice(5, 7), 16);
  const r2 = parseInt(color2.slice(1, 3), 16);
  const g2 = parseInt(color2.slice(3, 5), 16);
  const b2 = parseInt(color2.slice(5, 7), 16);
  const r = Math.round(r1 + (r2 - r1) * t);
  const g = Math.round(g1 + (g2 - g1) * t);
  const b = Math.round(b1 + (b2 - b1) * t);
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

// Apply cost-based coloring
function applyCostStyling(enabled) {
  if (!cy) return;

  if (enabled) {
    // Get min/max capital_cost
    const costs = cy.nodes()
      .map(n => n.data('capital_cost'))
      .filter(v => typeof v === 'number');

    if (costs.length === 0) return;

    const minCost = Math.min(...costs);
    const maxCost = Math.max(...costs);

    // Apply gradient colors (white → red)
    cy.nodes().forEach(node => {
      const cost = node.data('capital_cost');
      if (typeof cost === 'number') {
        const t = (cost - minCost) / (maxCost - minCost || 1);
        const color = lerpColor('#e3f2fd', '#ff5252', t);
        node.style('background-color', color);
      }
    });
  } else {
    // Reset to default styling
    cy.nodes().forEach(node => {
      node.style('background-color', '#e3f2fd');
    });
  }
}

// Wire up toggle
document.getElementById('cost-styling-toggle').addEventListener('change', function() {
  applyCostStyling(this.checked);
});
```

### Component 6: Golden Reference with Costs

**File:** `proof_of_concept/golden_references/coffee_maker_with_costs.json`

Structure mirrors existing golden reference with added `costs` field:

```json
{
  "nodes": [
    {
      "id": "coffee_maker",
      "name": "coffee_maker",
      "type_name": "Coffee Maker",
      "element_type": "part",
      "parent": null,
      "depth": 0,
      "multiplicity": null,
      "costs": {
        "capital_cost": 113.96,
        "raw_material_cost": 65.48,
        "fabrication_cost": 33.56,
        "installation_cost": 8.42,
        "idiot_index": 1.74
      }
    }
    // ... other nodes with costs
  ],
  // edges and metadata unchanged
}
```

**Note:** Exact cost values will be computed by running `generate_costs.py` and capturing the output.

### Component 7: Tests

**File:** `proof_of_concept/tests/test_visualization.py`

**New test cases:**

```python
# =============================================================================
# Phase 5: Cost Extraction (POC Item 5)
# =============================================================================

@pytest.fixture
def extracted_result_with_costs():
    """Run extraction with cost attributes enabled."""
    from proof_of_concept.extraction.visualization import extract_structural_view
    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, _ = syside.try_load_model(files)

    return extract_structural_view(
        model,
        root="coffee_maker",
        include_cost_attributes=[
            "capital_cost",
            "raw_material_cost",
            "fabrication_cost",
            "installation_cost",
            "idiot_index",
        ],
    )


def test_costs_field_present(extracted_result_with_costs):
    """Nodes have costs field when cost extraction enabled."""
    for node in extracted_result_with_costs["nodes"]:
        assert "costs" in node


def test_root_has_all_cost_attributes(extracted_result_with_costs):
    """Root node has all requested cost attributes."""
    root = next(n for n in extracted_result_with_costs["nodes"] if n["id"] == "coffee_maker")
    costs = root.get("costs", {})

    expected_attrs = {"capital_cost", "raw_material_cost", "fabrication_cost", "installation_cost", "idiot_index"}
    assert set(costs.keys()) == expected_attrs


def test_cost_values_are_numeric(extracted_result_with_costs):
    """All cost values are floats."""
    for node in extracted_result_with_costs["nodes"]:
        costs = node.get("costs")
        if costs:
            for value in costs.values():
                assert isinstance(value, (int, float))


def test_to_cytoscape_includes_costs(extracted_result_with_costs):
    """to_cytoscape passes through cost data."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result_with_costs)

    # Find root element
    root_el = next(el for el in result["elements"] if el["data"]["id"] == "coffee_maker")

    assert "costs" in root_el["data"]
    assert "capital_cost" in root_el["data"]  # Flattened for Cytoscape access


def test_backward_compatible_no_costs():
    """Extraction without cost attributes still works."""
    from proof_of_concept.extraction.visualization import extract_structural_view
    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, _ = syside.try_load_model(files)

    result = extract_structural_view(model, root="coffee_maker")

    # Should work, costs field should be None or missing
    assert len(result["nodes"]) == 10
```

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Refactoring generate_costs.py introduces bugs | Low | Medium | Keep changes minimal; run existing tests |
| Cytoscape styling breaks expand/collapse | Low | Medium | Test thoroughly; use non-destructive style updates |
| Cost values don't match expected | Low | Low | Using same evaluation logic as generate_costs.py |

---

## Integration Strategy

This builds on existing POC infrastructure:
- **Extraction:** Extends existing `extract_structural_view()` with optional parameter
- **Converter:** Extends existing `to_cytoscape()`
- **Server:** Minor change to pass default cost attributes
- **UI:** Additive changes to info panel and controls

No changes to existing functionality when costs not requested (backward compatible).

---

## Validation Approach

### Unit Tests
- Cost field structure validation
- Value type validation
- Backward compatibility test

### Integration Tests
- Golden reference comparison with costs
- API response includes cost data
- Cytoscape elements have flattened cost fields

### Manual Testing
1. Start server: `uv run python -m proof_of_concept.web`
2. Load coffee maker model
3. Click nodes → verify costs in info panel
4. Toggle "Color by Cost" → verify visual differentiation
5. Export PNG → verify colors in export

---

**Implementation Complete:** 2026-01-19 - All phases executed successfully. See `plan.md` for implementation notes.
