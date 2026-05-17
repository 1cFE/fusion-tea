"""Concept table loading, resolution, and 1costingfe mapping."""

import csv
import re
from pathlib import Path

from lib.paths import TABLE_PATH

# Family-level and concept-specific 1costingfe mappings
COSTINGFE_MAPPING = {
    # Family-level mappings (key = "Family-subcategory")
    "MFE-tokamak": {
        "concept": "TOKAMAK",
        "example": "dt_tokamak.py",
        "defaults": "mfe_tokamak.yaml",
    },
    "MFE-stellarator": {
        "concept": "STELLARATOR",
        "example": "dt_tokamak.py",  # no stellarator example; tokamak is closest
        "defaults": "mfe_stellarator.yaml",
    },
    "MFE-mirror": {
        "concept": "MIRROR",
        "example": "dt_mirror.py",
        "defaults": "mfe_mirror.yaml",
    },
    "IFE-laser": {
        "concept": "LASER_IFE",
        "example": "dt_tokamak.py",  # no laser IFE example
        "defaults": "ife_laser_ife.yaml",
    },
    "IFE-heavy-ion": {
        "concept": "HEAVY_ION",
        "example": "dt_tokamak.py",  # no heavy-ion example
        "defaults": "ife_heavy_ion.yaml",
    },
    "MIF-mag-target": {
        "concept": "MAG_TARGET",
        "example": "dt_tokamak.py",  # no generic mag-target example
        "defaults": "mif_mag_target.yaml",
    },
    # Concept-specific overrides (key = concept ID)
    "08-frc-w-direct-conversion": {
        "concept": "MAG_TARGET",
        "example": "dhe3_pulsed_frc.py",  # existing example for this exact concept
        "defaults": "mif_mag_target.yaml",
        "notes": "FRC not natively supported; use MAG_TARGET with overrides per dhe3_pulsed_frc.py",
    },
}

FUEL_MAPPING = {
    "D-T": "DT", "D-D": "DD", "D-He3": "DHE3", "p-B11": "PB11",
}

# Maps CSV (Confinement Family, Sub-type) → COSTINGFE_MAPPING key
FAMILY_KEY_MAP = {
    ("MFE", "Tokamak"): "MFE-tokamak",
    ("MFE", "Stellarator"): "MFE-stellarator",
    ("MFE", "Open/Linear"): "MFE-mirror",
    ("IFE", "Laser"): "IFE-laser",
    ("IFE", "Heavy ion beam"): "IFE-heavy-ion",
    ("MIF", "Magnetized target"): "MIF-mag-target",
}


def _is_freeform_architecture(concept: dict) -> bool:
    """Architectural overrides that force the freeform model path.

    Concepts whose architecture columns would otherwise route them to a
    costingfe template but whose physics doesn't fit that template.
    Derived from table.csv columns + slug so the override survives
    concept ID renumbering.
    """
    family = concept.get("Confinement Family", "").strip()
    topology = concept.get("MFE Topology", "").strip()
    cid = concept.get("_id", "").lower()

    # Z-pinch shares the Open/Linear topology label with mirrors, but the
    # mirror costingfe template doesn't capture its physics — freeform.
    if family == "MFE" and topology == "Open/Linear" and "pinch" in cid:
        return True

    return False


def get_model_path(concept: dict) -> str:
    """Determine model-setup path for a concept.

    Returns: 'costingfe' | 'freeform'
    """
    # Concept-specific override wins (e.g. 08-frc-w-direct-conversion).
    cid = concept["_id"]
    if cid in COSTINGFE_MAPPING:
        return "costingfe"

    # Architectural override (e.g. Z-pinch under Open/Linear).
    if _is_freeform_architecture(concept):
        return "freeform"

    # Family-level lookup.
    family = concept.get("Confinement Family", "")
    sub = _get_subcategory(concept)
    family_key = FAMILY_KEY_MAP.get((family, sub))
    if family_key and family_key in COSTINGFE_MAPPING:
        return "costingfe"

    # Default: freeform for anything not explicitly mapped (Non-Standard
    # family, MFE/Dipole, MFE/Compact Toroid, IFE non-laser drivers, etc.).
    return "freeform"


def get_costingfe_mapping(concept: dict) -> dict:
    """Get the 1costingfe mapping dict for a concept.

    Returns the mapping with keys: concept, example, defaults, notes (optional).
    Checks concept-specific override first, then family-level.
    """
    cid = concept["_id"]
    if cid in COSTINGFE_MAPPING:
        return COSTINGFE_MAPPING[cid]

    family = concept.get("Confinement Family", "")
    sub = _get_subcategory(concept)
    family_key = FAMILY_KEY_MAP.get((family, sub))
    if family_key and family_key in COSTINGFE_MAPPING:
        return COSTINGFE_MAPPING[family_key]

    raise ValueError(f"No costingfe mapping for {cid} (family={family}, sub={sub})")


def _get_subcategory(concept: dict) -> str:
    """Extract the relevant sub-category column based on confinement family."""
    family = concept.get("Confinement Family", "")
    if family == "MFE":
        return concept.get("MFE Topology", "")
    elif family == "IFE":
        return concept.get("IFE Driver", "")
    elif family == "MIF":
        return concept.get("MIF Method", "")
    elif family == "Non-Standard":
        return concept.get("Non-Standard Mechanism", "")
    return ""


def load_table(csv_path: Path = TABLE_PATH) -> list[dict]:
    """Load concept table from CSV. Returns list of concept dicts.

    Each dict has all CSV columns plus:
      - _id: the ID column value (e.g., '01-hts-compact-tokamak')
      - _num: the numeric prefix (e.g., '01', '17a')
    """
    concepts = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["_id"] = row["ID"]
            # Extract numeric prefix: '01' from '01-hts-compact-tokamak',
            # '17a' from '17a-laser-icf-hybrid-drive'
            m = re.match(r"^(\d+[a-z]?)-", row["ID"])
            row["_num"] = m.group(1) if m else row["ID"]
            # Research ID maps to Phase 1a directory (for split concepts like 17a/17b)
            row["_research_id"] = row.get("Research ID") or row["_id"]
            concepts.append(row)
    return concepts


def resolve_one(concepts: list[dict], query: str) -> list[dict]:
    """Resolve a single query to matching concepts.

    Matches against: numeric prefix (01, 17a), full ID, slug portion,
    or partial company name (case-insensitive).
    Returns list of matches (0, 1, or many).
    """
    q = query.strip()

    # Exact ID match
    for c in concepts:
        if c["_id"] == q:
            return [c]

    # Numeric prefix match (e.g., '01' or '17a')
    for c in concepts:
        if c["_num"] == q:
            return [c]

    # Slug match — query matches the part after the numeric prefix
    for c in concepts:
        slug = c["_id"].split("-", 1)[1] if "-" in c["_id"] else ""
        if slug == q:
            return [c]

    # Partial name or company (case-insensitive)
    ql = q.lower()
    matches = [
        c
        for c in concepts
        if ql in c["Concept Name"].lower() or ql in c.get("Company", "").lower()
    ]
    return matches


def resolve_concepts(
    args: list[str], concepts: list[dict], *, family: str | None = None, all_remaining: bool = False,
    target_state: str | None = None,
) -> list[dict]:
    """Resolve CLI concept arguments to a list of concept dicts.

    Handles: numeric IDs, full IDs, partial names, --all, --family.
    target_state: for --all filtering, skip concepts already at this state.
    """
    from lib.state import get_concept_state

    if all_remaining:
        result = concepts
        if family:
            result = [c for c in result if c.get("Confinement Family", "") == family]
        if target_state:
            result = [
                c for c in result
                if get_concept_state(c["_id"]) != target_state
            ]
        return result

    if family and not args:
        return [c for c in concepts if c.get("Confinement Family", "") == family]

    resolved = []
    for q in args:
        matches = resolve_one(concepts, q)
        if len(matches) == 0:
            raise ValueError(f"No concept matching '{q}'")
        elif len(matches) > 1:
            detail = ", ".join(f"{m['_id']}: {m['Concept Name']}" for m in matches)
            raise ValueError(
                f"Ambiguous query '{q}' matched {len(matches)} concepts: {detail}"
            )
        resolved.append(matches[0])

    if family:
        resolved = [c for c in resolved if c.get("Confinement Family", "") == family]

    return resolved
