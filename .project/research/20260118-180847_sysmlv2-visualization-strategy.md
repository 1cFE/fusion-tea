---
date: 2026-01-18T18:08:47-08:00
researcher: Claude
topic: "SysMLv2 Model Visualization Strategy"
tags: [research, visualization, sysml, architecture]
status: complete
last_updated: 2026-01-18
---

# Research: SysMLv2 Model Visualization Strategy

**Date**: 2026-01-18
**Researcher**: Claude
**Research Type**: Architecture / Feasibility Analysis

## Research Questions

1. Is the proposed design approach in `.project/design-intent/` well-reasoned? What can be cleaned up or simplified? Where are the hidden risks?
2. Does it make sense to keep raw AST → graph building in `agentic-mbse`? What gaps exist?
3. How should we best render the "filtered" VisualizationGraph? Can we leverage existing open-source tools?
4. Is using SysML display tools like SysON viable for a parse → filter → dump → render workflow?

---

## Executive Summary

The proposed design approach is **fundamentally sound**. The key insight - "syside already gives us a graph, we just filter and project" - is correct and avoids unnecessary complexity. However, there are risks and gaps that need attention.

**Key Findings**:

| Area | Assessment | Recommendation |
|------|------------|----------------|
| Design approach | Well-reasoned, minimal | Proceed with refinements |
| agentic-mbse integration | Sensible location | Add visualization module there |
| Rendering strategy | Custom + Cytoscape.js | Build custom; avoid SysON dependency |
| SysON as backend | Not viable for this use case | Use for reference only |

---

## 1. Design Approach Analysis

### What's Well-Reasoned

1. **"Filter and project the AST, don't rebuild it"** - This is the right insight. The syside AST already contains all structural and semantic information. Creating a new graph representation would be duplicative.

2. **Three distinct view types** (structural, cost, dependency) - These map well to user questions:
   - Structural: "What's in this system?" → ownership hierarchy
   - Cost: "Where does cost come from?" → rollup chains
   - Dependency: "What depends on what?" → calculation data flow

3. **Simple output format** (`{nodes, edges, metadata}`) - This is renderer-agnostic and can be trivially converted to Cytoscape.js, React Flow, DOT, or any other format.

4. **Query parameters for agents** - Letting agents specify `root`, `max_depth`, `include_attributes`, etc. enables flexible, question-driven visualization.

### What Can Be Simplified

1. **Redundant data-shapes.md and abstraction-interfaces.md**
   - These overlap significantly
   - **Recommendation**: Merge into a single "extraction-api.md" that covers both API and data shapes
**UPDATE:** Change complete

2. **Over-specification of renderer conversion**
   - The `to_cytoscape()`, `to_react_flow()`, `to_dot()` examples are implementation details
   - **Recommendation**: Remove from design docs; implement directly when building
**UPDATE:** Change complete

3. **View overlay complexity**
   - The "layered overlay" concept (cost + physics on structural) adds UI complexity
   - **Recommendation**: Start with separate views, add overlays only if proven necessary
**UPDATE:** Change complete

### Hidden Risks

#### Risk 1: Expression Traversal Complexity (High Impact)

**Problem**: Extracting dependency graphs requires understanding nested expressions. The exploration script notes:
- `OperatorExpression` contains nested `FeatureReferenceExpression`
- `FeatureChainExpression` represents dot paths (e.g., `cost_model.total_cost`)
- `InvocationExpression` represents function calls (e.g., `sum(heater.capital_cost)`)

**Current gap in agentic-mbse**: `extract_feature_refs()` returns a flat list without parent context. This makes it hard to reconstruct expression trees.

**Mitigation**: The `traverse_expression()` function with visitor pattern exists. Need to extend it to build tree structures, not just flat lists.

#### Risk 2: Anonymous Element Naming (Medium Impact)

**Problem**: Many AST elements are anonymous:
- Design file parts are anonymous redefinitions (`:>> brewing` creates anonymous ReferenceUsage)
- Need to derive names from `redefined_feature`
- This requires careful traversal to get user-friendly names

**Mitigation**: Already documented in ast-exploration.md. Implementation must handle this correctly.

#### Risk 3: Cross-File References (Medium Impact)

**Problem**: In multi-file models, part definitions in library/ are referenced by usages in designs/. The structural view needs to walk across files.

**Current capability**: `SysideAdapter.get_document_url()` exists; `is_cross_file` flag is tracked in bindings.

**Mitigation**: Ensure extraction functions follow type relationships across documents.

#### Risk 4: Performance with Large Models (Low-Medium Impact)

**Problem**: Fusion models may have 100+ components. Walking the full AST on every query could be slow.

**Mitigation**:
- Implement caching of parsed models (re-parse on file changes)
- Allow `max_depth` limits in queries
- Consider lazy loading of deeply nested structures

---

## 2. agentic-mbse Integration Analysis

### Current Capabilities

The `agentic-mbse/src/agentic_mbse/sysml/` module provides:

| File | Capabilities | Visualization Relevance |
|------|--------------|-------------------------|
| `syside_adapter.py` | Model loading, element iteration, type checking | **Essential** - Foundation for all extraction |
| `expression.py` | Expression traversal, feature ref extraction | **Essential** - For dependency views |
| `binding.py` | Binding classification and extraction | **High** - For cost rollup analysis |
| `graph.py` | Cycle detection, topological sort | **Medium** - For dependency ordering |
| `types.py` | Data models (BindingType, ExpressionRef) | **High** - Type definitions needed |
| `helpers.py` | Source location, parent resolution | **Medium** - For context and navigation |

### Key Patterns to Leverage

```python
# Element iteration by type
for part in SysideAdapter.elements_of_type(model, "PartUsage"):
    ...

# Expression traversal with visitor
refs = extract_feature_refs(expr)

# Binding classification
binding_type = classify_binding(expr)  # CHAIN, REFERENCE, LITERAL, EXPRESSION

# Type checking (mock-friendly)
if SysideAdapter.is_instance(elem, "CalculationDefinition"):
    ...
```

### Gaps to Address

1. **No hierarchical graph building** - Current code iterates elements linearly; needs to build parent-child trees
2. **No bidirectional references** - Can get "what A references" but not "what references A"
3. **No expression tree reconstruction** - Flat visitor pattern only
4. **No graph serialization** - No standard output format (JSON, DOT, GraphML)
5. **No metadata-rich edges** - Graph edges have only node names, not binding types

### Recommendation: Add `visualization.py` to agentic-mbse

```python
# agentic_mbse/sysml/visualization.py

def extract_structural_view(model, root=None, max_depth=10, ...) -> ViewResult:
    """Walk ownership tree, return {nodes, edges, metadata}."""

def extract_cost_view(model, root=None, cost_attributes=None, ...) -> ViewResult:
    """Extract cost attributes and rollup chains."""

def extract_dependency_view(model, target, direction="upstream", ...) -> ViewResult:
    """Trace calculation dependencies."""
```

This keeps all SysML analysis in one place and allows the visualization frontend to be decoupled.

---

## 3. Rendering Strategy Analysis

### Option A: Cytoscape.js (Recommended)

**Pros**:
- Native compound graph support (containment hierarchy)
- Multiple layout algorithms (dagre, cose-bilkent, klay)
- `{nodes, edges}` format matches our output
- Good event system for interaction
- Can export to PNG/SVG

**Cons**:
- Learning curve for custom styling
- Requires layout configuration

**Fit for SysML**: **Excellent** - Compound graphs map directly to part containment.

### Option B: React Flow

**Pros**:
- Modern React integration
- Custom node components (good for detailed views)
- Built-in minimap, controls
- Sub-flows for nesting

**Cons**:
- Requires explicit positions (needs layout engine)
- React-specific
- Less mature for hierarchical layouts

**Fit for SysML**: **Good** - Better for rich node content, worse for auto-layout.

### Option C: D3.js

**Pros**:
- Maximum flexibility
- Excellent tree/hierarchy layouts
- Industry standard

**Cons**:
- Low-level API
- More development effort
- Need to build interaction from scratch

**Fit for SysML**: **Good** but high effort.

### Option D: ELK.js + Custom Renderer

**Pros**:
- Professional layout algorithms (developed by KIELER/Eclipse)
- Supports ports, compartments, nested graphs
- Used by Sirius Web internally

**Cons**:
- Layout only - need separate renderer
- Complex configuration

**Fit for SysML**: **Excellent** layout quality, but requires custom rendering.

### Recommended Approach

**Primary**: Cytoscape.js with dagre layout for MVP
- Simple integration with our `{nodes, edges}` format
- Good enough layout for initial needs
- Fast to implement

**Future**: Consider ELK.js + React Flow for production
- Better layout quality
- Richer node rendering

---

## 4. SysON Viability Assessment

### Can SysON serve as a rendering backend?

**Short answer: No - Not viable for this use case**

### What SysON Can Do

1. **Import .sysml files** via UI (upload) or potentially GraphQL
2. **Auto-create diagrams** when ViewUsage elements are imported
3. **Apply auto-layout** (basic ELK-based)
4. **Export diagrams** via experimental image server (SVG/PNG, REST API)

### Why It's Not Viable

| Requirement | SysON Support | Gap |
|-------------|---------------|-----|
| Programmatic file upload | No documented API | Major |
| Filtered subset rendering | Requires ViewUsage | Medium |
| Custom layout control | Not programmatic | Medium |
| Fast iteration | Heavy infrastructure | Major |
| Lightweight embedding | Requires Docker + servers | Major |

### Specific Issues

1. **No programmatic file upload**
   - REST API: "Does not allow fine-grained changes to the model"
   - Would need undocumented GraphQL mutation or custom integration

2. **Requires ViewUsage for diagrams**
   - To render, must include ViewUsage in the .sysml file
   - Complicates the "dump filtered subset" workflow

3. **Separate image server**
   - Sirius Web 2025.8 added experimental diagram export
   - Requires running *another* Docker container
   - REST API is not fully documented

4. **Infrastructure overhead**
   - SysON itself: PostgreSQL + Spring Boot + React
   - Image server: Separate process
   - Overkill for generating diagrams from filtered models

### When SysON IS Appropriate

- Interactive modeling environment for domain experts
- Full MBSE workflow with collaborative editing
- When you need the complete SysML v2 diagram types

### Recommendation

**Don't use SysON as a rendering backend.**

Instead:
1. Use SysON for reference/validation (as in your existing syson-setup-guide.md)
2. Build a custom lightweight renderer using Cytoscape.js or React Flow
3. Export to DOT/GraphViz for quick static diagrams during development

---

## 5. Open-Source Tools to Leverage or Learn From

### For Immediate Use

| Tool | Use Case | Link |
|------|----------|------|
| **Cytoscape.js** | Primary graph rendering | https://js.cytoscape.org/ |
| **Graphviz/DOT** | Quick static diagrams | https://graphviz.org/ |
| **ts-graphviz** | Programmatic DOT generation | https://ts-graphviz.github.io/ts-graphviz/ |

### For Reference/Learning

| Tool | What to Learn | Link |
|------|---------------|------|
| **AST Explorer** | Source ↔ tree sync UI pattern | https://astexplorer.net/ |
| **Mermaid** | Diagram-as-code approach | https://mermaid.js.org/ |
| **ELK.js** | Layout algorithm options | https://github.com/kieler/elkjs |

### SysML-Specific Tools

| Tool | Status | Notes |
|------|--------|-------|
| **SysML v2 Pilot** | Reference | Uses PlantUML for viz |
| **Tom Sawyer Viewer** | Commercial | Professional quality |
| **Syside** | In use | Parser (no diagram) |

---

## 6. Implementation Recommendations

### Phase 1: Foundation (MVP)

1. **Add `visualization.py` to agentic-mbse**
   - Implement `extract_structural_view()` first
   - Use existing patterns from expression.py and binding.py
   - Output `{nodes, edges, metadata}` dict

2. **Create basic CLI for testing**
   ```bash
   uv run python -m agentic_mbse.sysml.visualization --model models/tests/coffee_maker
   ```

3. **Generate DOT output**
   - Simple Python function to convert ViewResult to DOT
   - Use Graphviz to render PNG/SVG
   - Validates extraction logic before building UI

### Phase 2: Interactive Viewer

1. **Set up web frontend**
   - React + Cytoscape.js
   - WebSocket for model updates

2. **Implement cost and dependency views**
   - Cost: Parse rollup expressions, annotate nodes
   - Dependency: Trace upstream/downstream refs

3. **Add agent integration**
   - Query parameters from agent
   - Highlight/focus commands

### Phase 3: Production Features

1. **Consider ELK.js** for better layouts
2. **Add export** (PNG, SVG, interactive HTML)
3. **Optimize** for large models

---

## 7. Summary

### Design Approach Verdict

The proposed approach is **sound**. Key strengths:
- "Filter and project" avoids unnecessary abstraction
- `{nodes, edges}` format is renderer-agnostic
- Query parameters enable agent-driven visualization

Key refinements needed:
- Merge redundant docs (data-shapes + abstraction-interfaces)
- Address expression tree reconstruction gap
- Handle anonymous element naming carefully

### Where to Put the Code

**In agentic-mbse/sysml/visualization.py** - keeps SysML analysis co-located with existing utilities.

### How to Render

**Cytoscape.js for MVP** - best balance of features, hierarchical support, and development speed.

### SysON Verdict

**Not viable as rendering backend** - too much infrastructure overhead, limited programmatic API. Keep using for reference and manual validation only.

---

## References

### Design Documents Read
- `.project/design-intent/README.md`
- `.project/design-intent/concepts.md`
- `.project/design-intent/requirements.md`
- `.project/design-intent/personas.md`
- `.project/design-intent/user-stories.md`
- `.project/design-intent/technical/abstraction-interfaces.md`
- `.project/design-intent/technical/data-shapes.md`
- `.project/design-intent/technical/ast-exploration.md`
- `.project/design-intent/technical/tool-research.md`

### Code Analyzed
- `/home/reid/1cfe/agentic-mbse/src/agentic_mbse/sysml/*.py`

### External Sources
- [Cytoscape.js](https://js.cytoscape.org/)
- [React Flow](https://reactflow.dev/)
- [D3.js](https://d3js.org/)
- [ELK.js](https://github.com/kieler/elkjs)
- [SysON Documentation](https://doc.mbse-syson.org/)
- [Sirius Web GitHub](https://github.com/eclipse-sirius/sirius-web)
- [AST Explorer](https://astexplorer.net/)
- [Graphviz](https://graphviz.org/)
