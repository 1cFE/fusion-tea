# Spec: Cost Annotations + Polish

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-19 00:51:42 UTC
**Complexity:** MEDIUM
**Branch:** visualization

---

## Business Goals

### Why This Matters

This is the final item of the visualization POC sprint. It demonstrates the core value proposition: showing cost data directly on structural diagrams. Without cost annotations, the visualization is just a hierarchy viewer; with them, it becomes a techno-economic analysis tool that supports design decisions and stakeholder communication.

### Success Criteria

- [x] Cost values appear in the info panel when clicking a node
- [x] Nodes can be styled (sized or colored) by total cost
- [x] Golden reference with costs matches extraction output
- [x] Demo-ready: load coffee maker and see costs immediately

### Priority

P0 (Critical) - Completes POC sprint and enables stakeholder feedback.

---

## Problem Statement

### Current State

The structural view extraction and web UI work correctly for hierarchy visualization, but:
- No cost data is extracted from the model
- The info panel shows structural info only (name, type, multiplicity)
- All nodes look identical regardless of their cost contribution

### Desired Outcome

Users can load a SysML model with cost attributes and immediately see:
1. Cost details when clicking any node
2. Visual indication of relative cost across the hierarchy (via size or color)

---

## Scope

### In Scope

1. **Extraction Enhancement**
   - Add `include_cost_attributes` parameter to `extract_structural_view()`
   - Extract specified cost attributes from `AttributeUsage` elements on parts
   - Populate `costs` dict on `StructuralNode`

2. **TypedDict Update**
   - Add `costs: dict[str, float] | None` field to `StructuralNode`

3. **Web UI - Info Panel**
   - Display all cost attributes when a node is selected
   - Format values appropriately (numbers with reasonable precision)

4. **Web UI - Node Styling**
   - Add option/toggle to style nodes by `capital_cost`
   - Support either size-based or color-based styling (implementer choice)
   - Include visual legend or explanation

5. **Golden Reference**
   - Create `golden_references/coffee_maker_with_costs.json`
   - Include expected cost values for all nodes

6. **Tests**
   - Test cost extraction produces expected structure
   - Test cost values match golden reference

### Out of Scope

- Cost rollup visualization (edges showing aggregation paths)
- Dependency tracing
- Currency formatting or unit labels
- Demo script/recording (working example is sufficient)

### Edge Cases & Considerations

- **Parts without costs**: Some parts may not have cost attributes; `costs` should be `None` or empty dict
- **Calculated vs literal values**: Cost attributes in the coffee maker model are calculated via `calc` usages; extraction needs to handle resolved values
- **Attribute naming**: Cost attributes use snake_case (`capital_cost`, not `capitalCost`)

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED]

1. **FR-1**: `extract_structural_view()` MUST accept an `include_cost_attributes` parameter specifying which attributes to extract
2. **FR-2**: When cost attributes are requested, nodes MUST include a `costs` dict with attribute name → value mappings
3. **FR-3**: The default cost attributes to extract MUST include: `capital_cost`, `raw_material_cost`, `fabrication_cost`, `installation_cost`, `idiot_index`
4. **FR-4**: The info panel MUST display all extracted cost attributes when a node is selected
5. **FR-5**: The UI MUST provide an option to style nodes by `capital_cost` (via size or color)
6. **FR-6**: [INFERRED] Nodes without cost data SHOULD display gracefully (no errors, show "-" or similar)
7. **FR-7**: [INFERRED] The `to_cytoscape()` converter MUST pass cost data through to the Cytoscape elements

### Non-Functional Requirements

- Cost extraction SHOULD NOT significantly impact load time (< 100ms additional)
- Cost styling SHOULD update without full re-render when toggled

---

## Acceptance Criteria

### Core Functionality

- [x] Load `models/tests/coffee_maker` with cost attributes enabled
- [x] Click on `heater` node → info panel shows capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index
- [x] Click on `coffee_maker` root node → info panel shows aggregated costs
- [x] Toggle "style by cost" → nodes visually differentiate by capital_cost
- [x] Run `pytest proof_of_concept/tests/` → all tests pass including new cost tests (23 pass)

### Quality & Integration

- [x] Existing tests continue to pass
- [x] Golden reference `coffee_maker_with_costs.json` validates extraction
- [x] No console errors in browser when loading model

---

## Technical Notes

### Cost Attribute Extraction Approach

The coffee maker model uses this pattern:
```sysml
part def 'Heating Element' :> 'Costed Component' {
    attribute capital_cost : Real;
    // ... computed via calc cost_model
    :>> capital_cost = cost_model.total_cost;
}
```

Extraction needs to:
1. For each `PartUsage` node, look for `AttributeUsage` children
2. Filter to attributes matching the requested names
3. Get the resolved value (may need to evaluate or check cached value)

### API Changes

```python
# visualization.py
def extract_structural_view(
    model,
    root: str | None = None,
    max_depth: int = 10,
    include_multiplicity: bool = True,
    exclude_stdlib: bool = True,
    include_cost_attributes: list[str] | None = None,  # NEW
) -> StructuralViewResult:
```

Default when `include_cost_attributes` is `None`: no costs extracted (backward compatible)

To get all costs:
```python
include_cost_attributes=["capital_cost", "raw_material_cost", "fabrication_cost", "installation_cost", "idiot_index"]
```

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_visualization-poc.md` (Item 5)
- **Sprint Plan:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md` (Day 5, lines 360-380)
- **Design:** `.project/active/cost-annotations/design.md` (to be created)
- **Test Model:** `models/tests/coffee_maker/`

---

**Next Steps:** After approval, proceed to `/_my_design`
