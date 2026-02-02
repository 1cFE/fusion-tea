"""CLI entry point for SysML structural view extraction.

Usage:
    uv run python -m proof_of_concept.extraction <model-path> [options]

Options:
    --format {cytoscape,dot}  Output format (default: cytoscape)
    --output FILE             Write to file instead of stdout
    --root NAME               Root element name (default: auto-detect)
"""

import argparse
import json
import sys
from pathlib import Path

from .visualization import extract_structural_view, load_model, to_cytoscape, to_dot


def main():
    parser = argparse.ArgumentParser(
        description="Extract and convert SysML structural views"
    )
    parser.add_argument("model_path", help="Path to SysML model directory or file")
    parser.add_argument(
        "--format",
        choices=["cytoscape", "dot"],
        default="cytoscape",
        help="Output format (default: cytoscape)",
    )
    parser.add_argument(
        "--output", "-o", help="Output file (default: stdout)", type=Path
    )
    parser.add_argument("--root", help="Root element name (default: auto-detect)")

    args = parser.parse_args()

    # Load model
    try:
        model = load_model(args.model_path)
    except ValueError as e:
        sys.exit(f"Error: {e}")

    # Extract
    view_result = extract_structural_view(model, root=args.root)

    # Check for extraction errors
    if "error" in view_result.get("metadata", {}):
        sys.exit(f"Error: {view_result['metadata']['error']}")

    # Convert
    if args.format == "cytoscape":
        output = json.dumps(to_cytoscape(view_result), indent=2)
    else:
        output = to_dot(view_result)

    # Output
    if args.output:
        args.output.write_text(output)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
