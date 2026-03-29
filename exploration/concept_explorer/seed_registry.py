"""Seed the concept registry and decision tree from table_v2.csv.

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
from pathlib import Path

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from exploration.concept_explorer.models import ConfinementFamily, FuelType  # noqa: E402
from exploration.concept_explorer.taxonomy_models import (  # noqa: E402
    ConceptRegistry,
    ConceptTaxonomy,
    EnergyCapture,
    IFEDriver,
    LaserApproach,
    MagnetType,
    MFETopology,
    MIFMethod,
    NeutronManagement,
    NonStandardMechanism,
    OperationMode,
    PlasmaState,
    PrimaryHeating,
    RepetitionRate,
    StellaratorType,
    TaxonomyConfidence,
    TokamakShape,
    TritiumBreeding,
)

CSV_PATH = Path(__file__).parent.parent / "phase_1b_v2" / "table_v2.csv"
DATA_DIR = Path(__file__).parent / "data"

# ---------------------------------------------------------------------------
# Known cost model IDs (concept name -> explorer ID)
# ---------------------------------------------------------------------------

COST_MODEL_IDS: dict[str, str] = {
    "Laser ICF - p-B11 Fast Ignition": "04",
    "Planar Coil Stellarator": "05",
    "Magnetic Mirror (p-B11)": "06",
    "FRC w/ Direct Conversion": "08",
}

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


def _na_or_enum(value: str, enum_cls: type) -> object | None:
    """Map CSV value to enum, treating 'N/A' as None."""
    value = value.strip()
    if value == "N/A":
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
        concept_id=slugify(name),
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
        energy_capture=_na_or_enum(row["Energy Capture"], EnergyCapture),
        plasma_state=_na_or_enum(row["Plasma State"], PlasmaState),
        magnet_type=_na_or_enum(row["Magnet Type"], MagnetType),
        tritium_breeding=_na_or_enum(row["Tritium Breeding"], TritiumBreeding),
        neutron_management=_na_or_enum(
            row["Neutron Management"], NeutronManagement
        ),
        operation_mode=OperationMode(row["Operation Mode"].strip()),
        repetition_rate=_na_or_enum(row["Repetition Rate"], RepetitionRate),
        driver_technology=row["Driver Technology"].strip() or None,
        confidence=TaxonomyConfidence(row["Overall Confidence"].strip()),
        cost_model_id=COST_MODEL_IDS.get(name),
    )


# ---------------------------------------------------------------------------
# Decision tree builder
# ---------------------------------------------------------------------------

# Hierarchy definition: for each family, which fields form the tree levels
_HIERARCHY: dict[ConfinementFamily, list[tuple[str, str, str]]] = {
    # (field_name, attribute_name, label)
    ConfinementFamily.MFE: [
        ("mfe_topology", "mfe_topology", "MFE Topology"),
        # Sub-type depends on topology — handled dynamically
    ],
    ConfinementFamily.IFE: [
        ("ife_driver", "ife_driver", "IFE Driver"),
    ],
    ConfinementFamily.MIF: [
        ("mif_method", "mif_method", "MIF Method"),
    ],
    ConfinementFamily.NONSTANDARD: [
        ("non_standard_mechanism", "non_standard_mechanism", "Mechanism"),
    ],
}

# Sub-type fields keyed by (family, topology/driver value)
_SUBTYPES: dict[tuple[str, str], tuple[str, str]] = {
    ("mfe_topology", "Tokamak"): ("tokamak_shape", "Tokamak Shape"),
    ("mfe_topology", "Stellarator"): ("stellarator_type", "Stellarator Type"),
    ("ife_driver", "Laser"): ("laser_approach", "Laser Approach"),
}

FAMILY_LABELS: dict[str, str] = {
    "MFE": "Magnetic Fusion Energy",
    "IFE": "Inertial Fusion Energy",
    "MIF": "Magneto-Inertial Fusion",
    "NONSTANDARD": "Non-Standard",
}


def _build_decision_tree(concepts: list[ConceptTaxonomy]) -> dict:
    """Build the decision tree JSON from the concept list."""
    # Group by family
    by_family: dict[str, list[ConceptTaxonomy]] = defaultdict(list)
    for c in concepts:
        by_family[c.confinement_family.value].append(c)

    family_children = []
    for family_enum in [
        ConfinementFamily.MFE,
        ConfinementFamily.IFE,
        ConfinementFamily.MIF,
        ConfinementFamily.NONSTANDARD,
    ]:
        fval = family_enum.value
        family_concepts = by_family.get(fval, [])
        if not family_concepts:
            continue

        hierarchy = _HIERARCHY[family_enum]
        if not hierarchy:
            # No sub-levels, just list concepts
            family_children.append({
                "value": fval if fval != "NONSTANDARD" else "Non-Standard",
                "label": FAMILY_LABELS[fval],
                "concepts": [c.concept_id for c in family_concepts],
            })
            continue

        field_name, attr_name, _label = hierarchy[0]

        # Group by first hierarchy level
        by_level1: dict[str, list[ConceptTaxonomy]] = defaultdict(list)
        for c in family_concepts:
            val = getattr(c, attr_name)
            if val is not None:
                by_level1[val.value].append(c)
            else:
                by_level1["_none_"].append(c)

        level1_children = []
        for l1_val, l1_concepts in by_level1.items():
            if l1_val == "_none_":
                continue

            # Check for sub-type
            subtype_key = (field_name, l1_val)
            if subtype_key in _SUBTYPES:
                sub_field, sub_label = _SUBTYPES[subtype_key]

                # Group by sub-type
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

                # Sort sub-children by value for stable output
                sub_children.sort(key=lambda x: x["value"])

                level1_children.append({
                    "value": l1_val,
                    "label": l1_val,
                    "field": sub_field,
                    "children": sub_children,
                })
            else:
                # No sub-type, concepts are leaves
                level1_children.append({
                    "value": l1_val,
                    "label": l1_val,
                    "concepts": [c.concept_id for c in l1_concepts],
                })

        # Sort level1 children by value for stable output
        level1_children.sort(key=lambda x: x["value"])

        family_node = {
            "value": fval if fval != "NONSTANDARD" else "Non-Standard",
            "label": FAMILY_LABELS[fval],
            "field": field_name,
            "children": level1_children,
        }
        family_children.append(family_node)

    return {
        "version": "1.0",
        "root": {
            "field": "confinement_family",
            "label": "Confinement Approach",
            "children": family_children,
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
        generated_from="table_v2.csv",
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
