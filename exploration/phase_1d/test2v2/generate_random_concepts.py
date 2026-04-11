#!/usr/bin/env python3
"""Generate random fusion concepts by family-conditional sampling from table_corrected.csv.

Uses the original (non-decomposed) differentiation table where "Confinement Concept"
is a single column. Samples non-confinement columns from their family-conditional
vocabularies to test within-family design freedom.

Rationale: The original test2 sampled from table_v2's decomposed hierarchy independently,
creating cross-family contamination (e.g., IFE-specific heating paired with MFE family).
This test conditions on confinement family to isolate within-family coupling.
"""

import argparse
import csv
import json
import random
from pathlib import Path

TABLE_PATH = Path(__file__).parent.parent.parent / "phase_1b" / "table_corrected.csv"
DEFAULT_OUTPUT = Path(__file__).parent / "random_concepts.json"

# Confinement anchor (sampled together — concept determines family)
ANCHOR_COLUMNS = ["Confinement Family", "Confinement Concept"]

# Non-confinement columns sampled from family-conditional vocabularies
# Driver Technology excluded: free-text, too concept-specific
SAMPLED_COLUMNS = [
    "Fuel",
    "Primary Heating",
    "Energy Capture",
    "Plasma State",
    "Magnet Type",
    "Tritium Breeding",
    "Neutron Management",
    "Operation Mode",
    "Repetition Rate",
]

ALL_COLUMNS = ANCHOR_COLUMNS + SAMPLED_COLUMNS

# Conditional N/A rules (non-confinement)
CONDITIONAL_NA = [
    {
        "if_column": "Fuel",
        "if_values": ["p-B11", "D-D", "D-He3"],
        "then_na": ["Tritium Breeding"],
    },
    {
        "if_column": "Operation Mode",
        "if_values": ["Steady-state", "Quasi-steady"],
        "then_na": ["Repetition Rate"],
    },
]

SKIP_VALUES = {"N/A", "TBD", "Unknown", ""}


def load_table(table_path: Path):
    """Load table and extract per-family conditional vocabularies."""
    rows = []
    with open(table_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # Build concept -> family mapping (deduplicated)
    concept_family: dict[str, str] = {}
    for row in rows:
        concept = row["Confinement Concept"].strip()
        family = row["Confinement Family"].strip()
        concept_family[concept] = family

    # Build per-family conditional vocabularies for sampled columns
    family_vocabs: dict[str, dict[str, set[str]]] = {}
    for row in rows:
        family = row["Confinement Family"].strip()
        if family not in family_vocabs:
            family_vocabs[family] = {col: set() for col in SAMPLED_COLUMNS}
        for col in SAMPLED_COLUMNS:
            val = row[col].strip()
            if val not in SKIP_VALUES:
                family_vocabs[family][col].add(val)

    # Sort for reproducibility
    family_vocabs_sorted: dict[str, dict[str, list[str]]] = {}
    for family in family_vocabs:
        family_vocabs_sorted[family] = {
            col: sorted(vals) for col, vals in family_vocabs[family].items()
        }

    # Unique concept types
    unique_concepts = sorted(concept_family.keys())

    # Build row signatures for "matches existing concept" detection
    existing_signatures: set[tuple] = set()
    for row in rows:
        sig = tuple(row.get(col, "").strip() for col in ALL_COLUMNS)
        existing_signatures.add(sig)

    return rows, concept_family, family_vocabs_sorted, unique_concepts, existing_signatures


def generate_one(
    concept_family: dict[str, str],
    family_vocabs: dict[str, dict[str, list[str]]],
    unique_concepts: list[str],
    rng: random.Random,
) -> dict[str, str]:
    """Generate one random concept with family-conditional sampling."""
    row: dict[str, str] = {}
    na_cols: set[str] = set()

    # 1. Sample a confinement concept (determines family)
    concept = rng.choice(unique_concepts)
    family = concept_family[concept]
    row["Confinement Family"] = family
    row["Confinement Concept"] = concept

    # 2. Sample conditioning columns first (Fuel, Operation Mode)
    for col in ["Fuel", "Operation Mode"]:
        vocab = family_vocabs[family][col]
        if vocab:
            row[col] = rng.choice(vocab)
        else:
            row[col] = "N/A"

    # 3. Apply conditional N/A rules
    for rule in CONDITIONAL_NA:
        if row.get(rule["if_column"]) in rule["if_values"]:
            na_cols.update(rule["then_na"])

    # 4. Sample remaining columns from family-conditional vocabulary
    for col in SAMPLED_COLUMNS:
        if col in row:
            continue
        if col in na_cols:
            row[col] = "N/A"
        else:
            vocab = family_vocabs[family][col]
            if vocab:
                row[col] = rng.choice(vocab)
            else:
                row[col] = "N/A"

    return row


def main():
    parser = argparse.ArgumentParser(
        description="Generate random fusion concepts (family-conditional sampling)"
    )
    parser.add_argument("--count", type=int, default=30, help="Number of concepts")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--table", type=Path, default=TABLE_PATH)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    rows, concept_family, family_vocabs, unique_concepts, existing_sigs = load_table(
        args.table
    )

    # Print vocabulary info
    families = sorted(family_vocabs.keys())
    print(
        f"Loaded {len(rows)} rows, {len(unique_concepts)} unique concept types "
        f"across {len(families)} families"
    )
    print()
    for family in families:
        concepts_in_family = [c for c, f in concept_family.items() if f == family]
        print(f"  {family} ({len(concepts_in_family)} concept types):")
        for col in SAMPLED_COLUMNS:
            vocab = family_vocabs[family][col]
            print(f"    {col}: {len(vocab)} values — {vocab}")
    print()

    concepts = []
    exact_matches = 0
    for i in range(args.count):
        row = generate_one(concept_family, family_vocabs, unique_concepts, rng)
        ordered = {col: row[col] for col in ALL_COLUMNS}

        # Check if this exactly matches an existing concept
        sig = tuple(ordered[col] for col in ALL_COLUMNS)
        is_exact_match = sig in existing_sigs

        if is_exact_match:
            exact_matches += 1

        concepts.append({"id": i + 1, "exact_match": is_exact_match, **ordered})

    # Family distribution in generated set
    family_dist = {}
    for c in concepts:
        fam = c["Confinement Family"]
        family_dist[fam] = family_dist.get(fam, 0) + 1

    output = {
        "seed": args.seed,
        "count": len(concepts),
        "exact_matches": exact_matches,
        "table": str(args.table),
        "method": "family-conditional sampling",
        "description": (
            "Confinement Concept sampled uniformly from unique concept types. "
            "Non-confinement columns sampled from family-conditional vocabularies "
            "(only values observed for that family in the real table). "
            "Driver Technology excluded (free-text, too concept-specific). "
            "Tests within-family design freedom, not cross-family compatibility."
        ),
        "family_distribution": family_dist,
        "family_vocabularies": family_vocabs,
        "concepts": concepts,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Generated {len(concepts)} random concepts -> {args.output}")
    print(f"Exact matches to existing concepts: {exact_matches}/{len(concepts)}")
    print(f"Family distribution: {family_dist}")
    print()

    # Show a few examples
    for c in concepts[:5]:
        match_tag = " [EXACT MATCH]" if c["exact_match"] else ""
        print(f"--- Concept #{c['id']}{match_tag} ---")
        for col in ALL_COLUMNS:
            if c[col] != "N/A":
                print(f"  {col}: {c[col]}")
        print()


if __name__ == "__main__":
    main()
