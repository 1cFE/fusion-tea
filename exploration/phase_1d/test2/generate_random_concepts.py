#!/usr/bin/env python3
"""Generate random fusion concepts by sampling from the v2 table vocabulary.

Reads table_v2.csv, extracts the controlled vocabulary per column,
and generates random rows with structural N/A rules applied.
"""

import argparse
import csv
import json
import random
from pathlib import Path

TABLE_PATH = Path(__file__).parent.parent / "phase_1b_v2" / "table_v2.csv"
DEFAULT_OUTPUT = Path(__file__).parent / "random_concepts.json"

# The 18 differentiation columns (excludes Concept Name, Company, Overall Confidence)
DIFF_COLUMNS = [
    "Confinement Family",
    "MFE Topology",
    "IFE Driver",
    "MIF Method",
    "Non-Standard Mechanism",
    "Tokamak Shape",
    "Stellarator Type",
    "Laser Approach",
    "Fuel",
    "Primary Heating",
    "Energy Capture",
    "Plasma State",
    "Magnet Type",
    "Tritium Breeding",
    "Neutron Management",
    "Operation Mode",
    "Repetition Rate",
    "Driver Technology",
]

# --- Structural N/A rules ---
# Each confinement family makes certain columns inapplicable.
FAMILY_NA: dict[str, list[str]] = {
    "MFE": [
        "IFE Driver",
        "MIF Method",
        "Non-Standard Mechanism",
        "Laser Approach",
    ],
    "IFE": [
        "MFE Topology",
        "MIF Method",
        "Non-Standard Mechanism",
        "Tokamak Shape",
        "Stellarator Type",
        "Magnet Type",
    ],
    "MIF": [
        "MFE Topology",
        "IFE Driver",
        "Non-Standard Mechanism",
        "Tokamak Shape",
        "Stellarator Type",
        "Laser Approach",
    ],
    "Non-Standard": [
        "MFE Topology",
        "IFE Driver",
        "MIF Method",
        "Tokamak Shape",
        "Stellarator Type",
        "Laser Approach",
    ],
}

# Sub-type columns: which parent value makes them applicable.
# If the parent has a different value (or is N/A), the child is N/A.
SUBTYPE_APPLICABLE: dict[str, tuple[str, str]] = {
    # child_column: (parent_column, required_parent_value)
    "Tokamak Shape": ("MFE Topology", "Tokamak"),
    "Stellarator Type": ("MFE Topology", "Stellarator"),
    "Laser Approach": ("IFE Driver", "Laser"),
}

# Non-confinement conditional N/As
CONDITIONAL_NA: list[dict] = [
    {
        "if_column": "Operation Mode",
        "if_values": ["Steady-state", "Quasi-steady"],
        "then_na": ["Repetition Rate"],
    },
    {
        "if_column": "Fuel",
        "if_values": ["p-B11", "D-D", "D-He3"],
        "then_na": ["Tritium Breeding"],
    },
]

SKIP_VALUES = {"N/A", "TBD", "Unknown", ""}


def load_vocabularies(table_path: Path) -> dict[str, list[str]]:
    """Extract unique non-N/A, non-TBD values per column from the real table."""
    vocabs: dict[str, set[str]] = {col: set() for col in DIFF_COLUMNS}
    with open(table_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for col in DIFF_COLUMNS:
                val = row[col].strip()
                if val not in SKIP_VALUES:
                    vocabs[col].add(val)
    return {col: sorted(vals) for col, vals in vocabs.items()}


def generate_one(vocabs: dict[str, list[str]], rng: random.Random) -> dict[str, str]:
    """Generate one random concept row with structural N/A rules applied."""
    row: dict[str, str] = {}
    na_cols: set[str] = set()

    # 1. Sample confinement family (always applicable, 4 values)
    family = rng.choice(vocabs["Confinement Family"])
    row["Confinement Family"] = family
    na_cols.update(FAMILY_NA.get(family, []))

    # 2. Sample family-specific sub-type columns
    for col in ["MFE Topology", "IFE Driver", "MIF Method", "Non-Standard Mechanism"]:
        if col in na_cols:
            row[col] = "N/A"
        else:
            row[col] = rng.choice(vocabs[col])

    # 3. Apply sub-type rules for deeper columns
    for child_col, (parent_col, required_val) in SUBTYPE_APPLICABLE.items():
        if child_col in na_cols:
            continue  # already N/A from family rules
        if row.get(parent_col, "N/A") != required_val:
            na_cols.add(child_col)

    for col in ["Tokamak Shape", "Stellarator Type", "Laser Approach"]:
        if col in na_cols:
            row[col] = "N/A"
        else:
            row[col] = rng.choice(vocabs[col])

    # 4. Sample conditioning columns first (Fuel, Operation Mode)
    for col in ["Fuel", "Operation Mode"]:
        row[col] = rng.choice(vocabs[col])

    # 5. Apply conditional N/A rules
    for rule in CONDITIONAL_NA:
        if row.get(rule["if_column"]) in rule["if_values"]:
            na_cols.update(rule["then_na"])

    # 6. Sample remaining columns
    for col in DIFF_COLUMNS:
        if col in row:
            continue
        if col in na_cols:
            row[col] = "N/A"
        else:
            row[col] = rng.choice(vocabs[col])

    return row


def main():
    parser = argparse.ArgumentParser(description="Generate random fusion concepts")
    parser.add_argument("--count", type=int, default=30, help="Number of concepts to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSON path")
    parser.add_argument("--table", type=Path, default=TABLE_PATH, help="Input CSV path")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    vocabs = load_vocabularies(args.table)

    print("Vocabulary sizes:")
    for col, vals in vocabs.items():
        print(f"  {col}: {len(vals)} values")
    print()

    concepts = []
    for i in range(args.count):
        row = generate_one(vocabs, rng)
        ordered = {col: row[col] for col in DIFF_COLUMNS}
        concepts.append({"id": i + 1, **ordered})

    output = {
        "seed": args.seed,
        "count": len(concepts),
        "vocabularies": {col: vals for col, vals in vocabs.items()},
        "concepts": concepts,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Generated {len(concepts)} random concepts -> {args.output}")
    print()

    # Show a few examples
    for c in concepts[:3]:
        print(f"--- Concept #{c['id']} ---")
        for col in DIFF_COLUMNS:
            if c[col] != "N/A":
                print(f"  {col}: {c[col]}")
        print()


if __name__ == "__main__":
    main()
