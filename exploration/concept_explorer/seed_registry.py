"""Seed the concept registry and decision tree from concept_analysis/table.csv.

One-time migration script. Reads the taxonomy CSV, validates each row
through ConceptTaxonomy Pydantic models, and writes:
  - data/concept_registry.json
  - data/decision_tree.json

Usage:
    uv run python exploration/concept_explorer/seed_registry.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import TypeVar

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from exploration.concept_explorer.models import ConfinementFamily, FuelType  # noqa: E402
from exploration.concept_explorer.taxonomy_models import (  # noqa: E402
    BlanketConfig,
    ConceptRegistry,
    ConceptTaxonomy,
    DriverType,
    EnergyCapture,
    IFEDriver,
    LaserApproach,
    MagnetType,
    MFETopology,
    MIFMethod,
    NonStandardMechanism,
    OperationMode,
    PrimaryHeating,
    RepetitionRate,
    StellaratorType,
    TaxonomyConfidence,
    TokamakShape,
)

CSV_PATH = Path(__file__).parent.parent / "concept_analysis" / "table.csv"
DATA_DIR = Path(__file__).parent / "data"

# ---------------------------------------------------------------------------
# Value mappings: CSV string -> enum value
# ---------------------------------------------------------------------------

CONFINEMENT_FAMILY_MAP: dict[str, ConfinementFamily] = {
    "MFE": ConfinementFamily.MFE,
    "IFE": ConfinementFamily.IFE,
    "MIF": ConfinementFamily.MIF,
    "Non-Standard": ConfinementFamily.NONSTANDARD,
}

FUEL_MAP: dict[str, FuelType] = {
    "D-T": FuelType.DT,
    "D-D": FuelType.DD,
    "D-He3": FuelType.DHE3,
    "p-B11": FuelType.PB11,
}


E = TypeVar("E", bound=Enum)


def _na_or_enum(value: str, enum_cls: type[E]) -> E | None:
    """Map CSV value to enum, treating 'N/A' or empty as None."""
    value = value.strip()
    if value == "N/A" or value == "":
        return None
    # Direct lookup by value
    for member in enum_cls:
        if member.value == value:
            return member
    raise ValueError(f"No {enum_cls.__name__} member for {value!r}")


def slugify(name: str) -> str:
    """Convert concept name to a URL-safe slug.

    "HTS Compact Tokamak" -> "hts-compact-tokamak"
    "Laser ICF - p-B11 Fast Ignition" -> "laser-icf-p-b11-fast-ignition"
    "FRC w/ Direct Conversion" -> "frc-w-direct-conversion"
    """
    s = name.lower()
    # Replace / and special chars with hyphens
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # Strip leading/trailing hyphens
    s = s.strip("-")
    return s


def _parse_row(row: dict[str, str]) -> ConceptTaxonomy:
    """Parse a single CSV row into a ConceptTaxonomy."""
    name = row["Concept Name"].strip()
    family = CONFINEMENT_FAMILY_MAP[row["Confinement Family"].strip()]

    return ConceptTaxonomy(
        concept_id=row["ID"].split("-", 1)[0],
        slug=slugify(name),
        name=name,
        company=row["Company"].strip() or None,
        confinement_family=family,
        mfe_topology=_na_or_enum(row["MFE Topology"], MFETopology),
        ife_driver=_na_or_enum(row["IFE Driver"], IFEDriver),
        mif_method=_na_or_enum(row["MIF Method"], MIFMethod),
        non_standard_mechanism=_na_or_enum(
            row["Non-Standard Mechanism"], NonStandardMechanism
        ),
        tokamak_shape=_na_or_enum(row["Tokamak Shape"], TokamakShape),
        stellarator_type=_na_or_enum(row["Stellarator Type"], StellaratorType),
        laser_approach=_na_or_enum(row["Laser Approach"], LaserApproach),
        fuel=FUEL_MAP[row["Fuel"].strip()],
        primary_heating=_na_or_enum(row["Primary Heating"], PrimaryHeating),
        heating_type=row["Heating Type"].strip() or None,
        driver_type=_na_or_enum(row["Driver Type"], DriverType),
        energy_capture=_na_or_enum(row["Energy Capture"], EnergyCapture),
        magnet_type=_na_or_enum(row["Magnet Type"], MagnetType),
        blanket_config=_na_or_enum(row["Blanket Config"], BlanketConfig),
        operation_mode=OperationMode(row["Operation Mode"].strip()),
        repetition_rate=_na_or_enum(row["Repetition Rate"], RepetitionRate),
        driver_technology=row["Driver Technology"].strip() or None,
        confidence=TaxonomyConfidence(row["Overall Confidence"].strip()),
    )


# ---------------------------------------------------------------------------
# Decision tree builder
# ---------------------------------------------------------------------------
#
# ADR — display-only tree_group layer (2026-05-17):
# v3 introduces six top-level display groups (MFE, IFE, MIF, Cmpt-Tor, Estatic,
# Other) that sit *between* the four-bucket ConfinementFamily enum and the
# decision tree the explorer renders. We deliberately do NOT extend
# ConfinementFamily — doing so would cascade through taxonomy_models.py
# validators, every per-concept JSON, lib/scoring.py, Phase 2a, and every test
# fixture, in exchange for a UI-only benefit. Instead, tree_group(c) derives
# a display group from existing architecture columns; _HIERARCHY here keys on
# that derived string. Keep tree_group(), the scoring.py:detect_c2_category
# pattern, and any other architecture-driven classifier consistent — if a
# new mechanism or topology lands, update tree_group() and verify the test in
# tests/test_seed_registry.py still partitions every CSV row into exactly one
# group.


def tree_group(c: ConceptTaxonomy) -> str:
    """v3 display-only sibling grouping for the decision tree.

    Mirrors lib/scoring.py:detect_c2_category pattern (architecture columns,
    no ID-prefix lookup); keep slug overrides in sync if any are added.

    Returns one of: "MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other".
    """
    if c.confinement_family == ConfinementFamily.NONSTANDARD:
        if c.non_standard_mechanism == NonStandardMechanism.ELECTROSTATIC:
            return "Estatic"
        return "Other"
    if (
        c.confinement_family == ConfinementFamily.MFE
        and c.mfe_topology == MFETopology.COMPACT_TOROID
    ):
        return "Cmpt-Tor"
    return c.confinement_family.value  # "MFE" | "IFE" | "MIF"


GROUP_LABELS: dict[str, str] = {
    "MFE": "Magnetic Fusion Energy",
    "IFE": "Inertial Fusion Energy",
    "MIF": "Magneto-Inertial Fusion",
    "Cmpt-Tor": "Compact Toroid",
    "Estatic": "Electrostatic Confinement",
    "Other": "Other Non-Standard",
}

# Display order of top-level groups in the rendered tree
_GROUP_ORDER: list[str] = ["MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other"]

# Per-group level-1 grouping: (field_name, attribute_name).
# A group with no entry collapses to a flat concept list under the group node.
_GROUP_LEVEL1: dict[str, tuple[str, str]] = {
    "MFE": ("mfe_topology", "mfe_topology"),
    "IFE": ("ife_driver", "ife_driver"),
    "MIF": ("mif_method", "mif_method"),
    "Other": ("non_standard_mechanism", "non_standard_mechanism"),
    # "Cmpt-Tor" and "Estatic" intentionally flat — small populations.
}

# Sub-type fields keyed by (field_name, level-1 value)
_SUBTYPES: dict[tuple[str, str], tuple[str, str]] = {
    ("mfe_topology", "Tokamak"): ("tokamak_shape", "Tokamak Shape"),
    ("mfe_topology", "Stellarator"): ("stellarator_type", "Stellarator Type"),
    ("ife_driver", "Laser"): ("laser_approach", "Laser Approach"),
}


def _build_decision_tree(concepts: list[ConceptTaxonomy]) -> dict:
    """Build the decision tree JSON from the concept list."""
    # Group by display tree_group (not by ConfinementFamily enum — see ADR above)
    by_group: dict[str, list[ConceptTaxonomy]] = defaultdict(list)
    for c in concepts:
        by_group[tree_group(c)].append(c)

    group_children = []
    for group in _GROUP_ORDER:
        group_concepts = by_group.get(group, [])
        if not group_concepts:
            continue

        level1_cfg = _GROUP_LEVEL1.get(group)
        if level1_cfg is None:
            # Flat group — concepts as direct leaves
            group_children.append({
                "value": group,
                "label": GROUP_LABELS[group],
                "concepts": [c.concept_id for c in group_concepts],
            })
            continue

        field_name, attr_name = level1_cfg

        # Group by first hierarchy level
        by_level1: dict[str, list[ConceptTaxonomy]] = defaultdict(list)
        for c in group_concepts:
            val = getattr(c, attr_name)
            if val is not None:
                by_level1[val.value].append(c)
            else:
                by_level1["_none_"].append(c)

        level1_children = []
        for l1_val, l1_concepts in by_level1.items():
            if l1_val == "_none_":
                continue

            subtype_key = (field_name, l1_val)
            if subtype_key in _SUBTYPES:
                sub_field, _sub_label = _SUBTYPES[subtype_key]

                by_sub: dict[str, list[ConceptTaxonomy]] = defaultdict(list)
                for c in l1_concepts:
                    sub_val = getattr(c, sub_field)
                    if sub_val is not None:
                        by_sub[sub_val.value].append(c)
                    else:
                        by_sub["_none_"].append(c)

                sub_children = []
                for s_val, s_concepts in by_sub.items():
                    if s_val == "_none_":
                        continue
                    sub_children.append({
                        "value": s_val,
                        "label": s_val,
                        "concepts": [c.concept_id for c in s_concepts],
                    })

                sub_children.sort(key=lambda x: x["value"])

                level1_children.append({
                    "value": l1_val,
                    "label": l1_val,
                    "field": sub_field,
                    "children": sub_children,
                })
            else:
                level1_children.append({
                    "value": l1_val,
                    "label": l1_val,
                    "concepts": [c.concept_id for c in l1_concepts],
                })

        level1_children.sort(key=lambda x: x["value"])

        group_children.append({
            "value": group,
            "label": GROUP_LABELS[group],
            "field": field_name,
            "children": level1_children,
        })

    return {
        "version": "1.0",
        "root": {
            "field": "tree_group",
            "label": "Confinement Approach",
            "children": group_children,
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    if not CSV_PATH.exists():
        print(f"ERROR: CSV not found at {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Parse CSV
    concepts: list[ConceptTaxonomy] = []
    errors: list[str] = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # Row 2 = first data row
            try:
                concept = _parse_row(row)
                concepts.append(concept)
            except Exception as exc:
                name = row.get("Concept Name", f"row {i}")
                errors.append(f"  Row {i} ({name}): {exc}")

    if errors:
        print(f"Validation errors ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        if not concepts:
            sys.exit(1)
        print(
            f"\nProceeding with {len(concepts)} valid concepts "
            f"({len(errors)} failed).",
            file=sys.stderr,
        )

    # Check for duplicate IDs
    ids = [c.concept_id for c in concepts]
    dupes = [x for x in set(ids) if ids.count(x) > 1]
    if dupes:
        print(f"WARNING: Duplicate concept IDs: {dupes}", file=sys.stderr)

    # Build registry
    registry = ConceptRegistry(
        version="1.0",
        generated_from="concept_analysis/table.csv",
        concepts=concepts,
    )

    # Build decision tree
    tree = _build_decision_tree(concepts)

    # Write outputs
    registry_path = DATA_DIR / "concept_registry.json"
    registry_path.write_text(
        registry.model_dump_json(indent=2, exclude_none=False) + "\n"
    )
    print(f"Wrote {len(concepts)} concepts to {registry_path}")

    tree_path = DATA_DIR / "decision_tree.json"
    tree_path.write_text(json.dumps(tree, indent=2) + "\n")
    print(f"Wrote decision tree to {tree_path}")


if __name__ == "__main__":
    main()
