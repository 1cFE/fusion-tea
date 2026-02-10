#!/usr/bin/env python3
"""Combine individual result JSON files into a single combined.json file."""

import json
import sys
from pathlib import Path


def combine_results(results_dir: Path) -> dict:
    """Combine all value-only JSON files into a single dictionary."""
    combined = {}

    for json_file in sorted(results_dir.glob("*.json")):
        # Skip manifest.json and any existing combined.json
        if json_file.name in ("manifest.json", "combined.json"):
            continue

        key = json_file.stem  # basename without .json
        content = json_file.read_text().strip()

        # Parse the value (could be number, string, etc.)
        try:
            value = json.loads(content)
        except json.JSONDecodeError:
            # If it's not valid JSON, store as string
            value = content

        combined[key] = value

    return combined


def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_results.py <results_directory>")
        sys.exit(1)

    results_dir = Path(sys.argv[1])
    if not results_dir.is_dir():
        print(f"Error: {results_dir} is not a directory")
        sys.exit(1)

    combined = combine_results(results_dir)

    # Write combined.json to the same directory
    output_path = results_dir / "combined.json"
    with open(output_path, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Combined {len(combined)} results into {output_path}")


if __name__ == "__main__":
    main()
