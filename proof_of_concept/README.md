# Visualization POC - Cytoscape.js Demo

Proof of concept for rendering SysML v2 structural views using Cytoscape.js.

## Quick Start

Open directly in browser (no server required):
```bash
# From project root
xdg-open proof_of_concept/cytoscape_demo.html

# Or on macOS
open proof_of_concept/cytoscape_demo.html
```

Or serve via HTTP:
```bash
cd proof_of_concept
python -m http.server 8080
# Open http://localhost:8080/cytoscape_demo.html
```

## Features

- **Hierarchical Layout**: Dagre algorithm for automatic top-to-bottom arrangement
- **Compound Nodes**: Nested containment hierarchy (coffee_maker → brewing → heater)
- **Expand/Collapse**: Toggle visibility of child nodes
- **Zoom-to-Node**: Double-click any node to zoom and center on it
- **Info Panel**: Click a node to see its details (name, type, depth, multiplicity)
- **PNG Export**: Download high-resolution (2x) diagram image

## Files

```
proof_of_concept/
├── cytoscape_demo.html              # Self-contained demo page
├── golden_references/
│   └── coffee_maker_structural.json # Hand-written test fixture
└── README.md                        # This file
```

## Golden Reference

The `golden_references/coffee_maker_structural.json` file contains the expected output format for structural view extraction. It defines:

- **10 nodes**: The coffee maker part hierarchy
- **9 edges**: Containment relationships (parent → child)
- **Metadata**: View type, root element, node count, max depth

This serves as the test fixture for validating the extraction implementation (Sprint Item 2).

## Data Schema

```typescript
interface ViewResult {
  nodes: StructuralNode[];
  edges: ContainmentEdge[];
  metadata: {
    view: "structural";
    root: string;
    total_nodes: number;
    max_depth: number;
  };
}

interface StructuralNode {
  id: string;
  name: string;
  type_name: string;
  element_type: "part";
  parent: string | null;
  depth: number;
  multiplicity: [number, number | null] | null;
}

interface ContainmentEdge {
  id: string;
  source: string;
  target: string;
  edge_type: "containment";
}
```

## Sprint Context

This POC is Item 1 of the Visualization Sprint. See:
- `.project/active/golden-reference-cytoscape-poc/` for spec, design, and plan
- `.project/backlog/epic_visualization-poc.md` for the full epic
