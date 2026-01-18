# Design: End-to-End Pipeline (POC Item 3)

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-18 22:50:45 UTC
**Branch:** visualization

---

## Overview

Add two format converters (`to_cytoscape()`, `to_dot()`) and a CLI entry point that enables running the full pipeline from model file to rendered diagram output.

## Related Artifacts

- **Spec:** `.project/active/end-to-end-pipeline/spec.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md`
- **Research:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Existing Extraction:** `proof_of_concept/extraction/visualization.py`
- **Cytoscape Demo:** `proof_of_concept/cytoscape_demo.html` (lines 192-216 show target format)
- **Tests:** `proof_of_concept/tests/test_visualization.py` (lines 28-34 show model loading pattern)

---

## Research Findings

### Model Loading Pattern

Found in `proof_of_concept/tests/test_visualization.py:28-34`:
```python
import syside

files = syside.collect_files_recursively(str(MODEL_DIR))
model, diagnostics = syside.try_load_model(files)
assert not diagnostics.contains_errors()
```

This is the established pattern for loading syside models. CLI will reuse this.

### Cytoscape.js Expected Format

From `proof_of_concept/cytoscape_demo.html:192-216`, the `convertToCytoscape()` function shows:
- Output is an array of `{data: {...}}` objects
- Each node's `data` contains: `id`, `label`, `name`, `type_name`, `element_type`, `parent`, `depth`, `multiplicity`
- The `label` field is computed from name + multiplicity (e.g., `"heater [2]"`)
- Containment edges are NOT included - Cytoscape uses `parent` property for compound nodes

### Existing Package Structure

`proof_of_concept/extraction/__init__.py` exports types from `types.py`. The extraction function is in `visualization.py` but not yet exported from `__init__.py`.

### CLI Framework

No CLI framework currently in use. Given the LOW complexity and minimal flags needed, `argparse` from stdlib is sufficient.

---

## Proposed Design

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI (__main__.py)                        │
│  - Parse args (model-path, --format, --output, --root)          │
│  - Load model via syside                                         │
│  - Call extract_structural_view()                                │
│  - Call appropriate converter                                    │
│  - Output to stdout or file                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    visualization.py (existing)                   │
│  + to_cytoscape(view_result) → dict                             │
│  + to_dot(view_result) → str                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Component 1: `to_cytoscape()` Function

**Location:** `proof_of_concept/extraction/visualization.py` (add to existing file)

**Purpose:** Convert `StructuralViewResult` to Cytoscape.js elements format.

**Interface:**
```python
def to_cytoscape(view_result: StructuralViewResult) -> dict:
    """Convert structural view to Cytoscape.js elements format.

    Args:
        view_result: Output from extract_structural_view()

    Returns:
        Dict with "elements" key containing list of node data objects.
        Each node has: id, label, name, type_name, element_type, parent, depth, multiplicity.
        No edges are included (Cytoscape uses parent property for hierarchy).
    """
```

**Implementation Notes:**
- Iterate over `view_result["nodes"]`
- Compute `label` from name + multiplicity using helper function `_format_label()`
- Wrap each node in `{"data": {...}}` format
- Return `{"elements": [...]}`

**Label formatting logic** (from demo lines 178-189):
```python
def _format_label(name: str, multiplicity: list[int] | None) -> str:
    if multiplicity is None:
        return name
    lower, upper = multiplicity
    if lower == upper:
        return f"{name} [{lower}]"
    upper_str = "*" if upper == -1 else str(upper)
    return f"{name} [{lower}..{upper_str}]"
```

### Component 2: `to_dot()` Function

**Location:** `proof_of_concept/extraction/visualization.py` (add to existing file)

**Purpose:** Convert `StructuralViewResult` to DOT format for Graphviz.

**Interface:**
```python
def to_dot(view_result: StructuralViewResult) -> str:
    """Convert structural view to DOT format for Graphviz.

    Args:
        view_result: Output from extract_structural_view()

    Returns:
        DOT format string with digraph, subgraphs for compound nodes,
        and node labels including type names.
    """
```

**Implementation Notes:**
- Build hierarchical structure using `parent` relationships
- Non-leaf nodes become `subgraph cluster_X { ... }`
- Leaf nodes become simple node declarations
- Node labels: `"name [mult] : Type Name"` or `"name : Type Name"`
- Use recursive helper to emit nested subgraphs

**DOT Structure:**
```dot
digraph structural {
    rankdir=TB;
    node [shape=box, style=rounded];

    subgraph cluster_coffee_maker {
        label="coffee_maker : Coffee Maker";
        style=rounded;

        // Nested subgraphs and leaf nodes...
    }
}
```

### Component 3: CLI Entry Point

**Location:** `proof_of_concept/extraction/__main__.py` (new file)

**Purpose:** Command-line interface for the visualization pipeline.

**Interface:**
```bash
uv run python -m proof_of_concept.extraction.visualization <model-path> [options]

Options:
  --format {cytoscape,dot}  Output format (default: cytoscape)
  --output FILE             Write to file instead of stdout
  --root NAME               Root element name (default: auto-detect)
```

**Implementation:**
```python
def main():
    parser = argparse.ArgumentParser(
        description="Extract and convert SysML structural views"
    )
    parser.add_argument("model_path", help="Path to SysML model directory or file")
    parser.add_argument("--format", choices=["cytoscape", "dot"], default="cytoscape")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--root", help="Root element name")

    args = parser.parse_args()

    # Load model
    model = load_model(args.model_path)

    # Extract
    view_result = extract_structural_view(model, root=args.root)

    # Convert
    if args.format == "cytoscape":
        output = json.dumps(to_cytoscape(view_result), indent=2)
    else:
        output = to_dot(view_result)

    # Output
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
```

**Error Handling:**
- Invalid model path: `sys.exit(f"Error: Model path not found: {path}")`
- Model load errors: `sys.exit(f"Error loading model: {diagnostics}")`
- Root not found: Let extraction return empty result with error in metadata

### Component 4: Model Loading Helper

**Location:** `proof_of_concept/extraction/visualization.py` (add to existing file)

**Purpose:** Encapsulate syside model loading for reuse by CLI and tests.

**Interface:**
```python
def load_model(path: str | Path):
    """Load a SysML model from path using syside.

    Args:
        path: Path to model directory or single .sysml file

    Returns:
        Parsed syside model object

    Raises:
        ValueError: If path doesn't exist or model has errors
    """
```

**Implementation Notes:**
- Check if path exists, raise `ValueError` if not
- Use `syside.collect_files_recursively()` for directory, or single file list
- Use `syside.try_load_model()`
- Check `diagnostics.contains_errors()`, raise `ValueError` if errors
- Return model

### File Changes Summary

| File | Action | Changes |
|------|--------|---------|
| `visualization.py` | Modify | Add `_format_label()`, `to_cytoscape()`, `to_dot()`, `load_model()` |
| `__main__.py` | Create | CLI entry point with argparse |
| `__init__.py` | Modify | Export new functions |

### Dependencies

- **syside**: Already installed (used by extraction)
- **argparse**: stdlib, no install needed
- **json**: stdlib, no install needed

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| DOT subgraph nesting complexity | Low | Use recursive helper, test with coffee maker |
| Graphviz node ID escaping | Low | Qualified paths use `.` and `_`, should be safe. Add escaping if needed. |

---

## Integration Strategy

**Usage Flow:**
1. User runs CLI: `uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker`
2. CLI loads model, extracts, converts, outputs JSON
3. User copies JSON into Cytoscape demo (or Item 4 web app will do this automatically)

**Complements:**
- Item 1: Cytoscape demo can consume CLI output
- Item 4: Web integration will call `extract_structural_view()` and `to_cytoscape()` directly

---

## Validation Approach

### Unit Tests

Add to `proof_of_concept/tests/test_visualization.py`:

1. **`test_to_cytoscape_format`**: Verify output has `elements` key with correct structure
2. **`test_to_cytoscape_labels`**: Verify label formatting with/without multiplicity
3. **`test_to_dot_valid_syntax`**: Verify output can be parsed (or at minimum contains expected keywords)
4. **`test_load_model_valid_path`**: Verify model loading works
5. **`test_load_model_invalid_path`**: Verify ValueError on bad path

### Integration Tests

1. **CLI smoke test**: Run CLI on coffee_maker, verify exit code 0
2. **JSON validity**: Parse CLI JSON output, verify structure
3. **DOT validity**: Pipe CLI DOT output to `dot -Tpng`, verify exit code 0

### Manual Validation

1. Copy CLI JSON output into `cytoscape_demo.html` (replace `goldenReference`), verify renders
2. Run `uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker --format=dot | dot -Tpng > /tmp/test.png`, verify image

---

## Usage Examples

### CLI Usage

```bash
# Default: Cytoscape JSON to stdout
uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker

# DOT format to file
uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker \
  --format=dot --output=coffee_maker.dot

# Render DOT to PNG
uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker \
  --format=dot | dot -Tpng > coffee_maker.png

# Specify root element
uv run python -m proof_of_concept.extraction.visualization models/tests/coffee_maker \
  --root=coffee_maker
```

### Programmatic Usage

```python
from proof_of_concept.extraction.visualization import (
    load_model,
    extract_structural_view,
    to_cytoscape,
    to_dot,
)

# Load and extract
model = load_model("models/tests/coffee_maker")
view = extract_structural_view(model, root="coffee_maker")

# Convert to Cytoscape format
cyto = to_cytoscape(view)
print(json.dumps(cyto, indent=2))

# Convert to DOT format
dot = to_dot(view)
print(dot)
```

---

**Next Step:** After approval → `/_my_implement`
