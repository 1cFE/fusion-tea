"""
Phase 2a Column Mapping

Bidirectional mapping between LLM natural language vocabulary and
table_v2.csv column names/values. Used by validate.py to check
LLM-derived constraints against empirical data.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Table loading
# ---------------------------------------------------------------------------

TABLE_PATH = Path(__file__).parent.parent / "phase_1b_v2" / "table_v2.csv"

# Columns to skip during validation (metadata, not design variables)
METADATA_COLUMNS = {"Concept Name", "Company", "Driver Technology", "Overall Confidence"}

# All design variable columns in the table
DESIGN_COLUMNS = [
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
    "Magnet Type",
    "Blanket Config",
    "Operation Mode",
    "Repetition Rate",
]


def load_table(path: Path | None = None) -> list[dict[str, str]]:
    """Load table_v2.csv as a list of row dicts."""
    p = path or TABLE_PATH
    with open(p) as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row.get("Concept Name", "").strip()]
    return rows


# ---------------------------------------------------------------------------
# Vocabulary mapping
# ---------------------------------------------------------------------------

@dataclass
class MappedTerm:
    """A table column + match predicate."""
    column: str
    match_type: str  # "exact" | "not" | "contains" | "in_set" | "not_na"
    value: str | list[str] | None = None

    def matches(self, cell_value: str) -> bool:
        """Check if a cell value matches this term.

        TBD values are treated as "unknown" — they don't count as matches
        or non-matches (handled by the caller via is_tbd()).
        """
        cell = cell_value.strip()
        if self.match_type == "exact":
            return cell == self.value
        elif self.match_type == "not":
            return cell != self.value
        elif self.match_type == "contains":
            return self.value.lower() in cell.lower()
        elif self.match_type == "in_set":
            return cell in self.value
        elif self.match_type == "not_na":
            return cell not in ("N/A", "")
        return False

    @staticmethod
    def is_tbd(cell_value: str) -> bool:
        """Check if a cell value is TBD/Unknown (ambiguous, not a real violation)."""
        return cell_value.strip() in ("TBD", "Unknown")


# Map from normalized LLM vocabulary → MappedTerm
# Keys are lowercase, stripped. The map is searched with normalized input.
VOCABULARY: dict[str, MappedTerm] = {
    # Confinement Family
    "magnetic confinement": MappedTerm("Confinement Family", "exact", "MFE"),
    "mfe": MappedTerm("Confinement Family", "exact", "MFE"),
    "inertial confinement": MappedTerm("Confinement Family", "exact", "IFE"),
    "ife": MappedTerm("Confinement Family", "exact", "IFE"),
    "magnetized target": MappedTerm("Confinement Family", "exact", "MIF"),
    "magnetized target fusion": MappedTerm("Confinement Family", "exact", "MIF"),
    "mif": MappedTerm("Confinement Family", "exact", "MIF"),
    "non-standard": MappedTerm("Confinement Family", "exact", "Non-Standard"),

    # MFE Topology
    "tokamak": MappedTerm("MFE Topology", "exact", "Tokamak"),
    "stellarator": MappedTerm("MFE Topology", "exact", "Stellarator"),
    "mirror": MappedTerm("MFE Topology", "contains", "Mirror"),
    "magnetic mirror": MappedTerm("MFE Topology", "contains", "Mirror"),
    "open/linear": MappedTerm("MFE Topology", "exact", "Open/Linear"),
    "frc": MappedTerm("MFE Topology", "exact", "Compact Toroid"),
    "field-reversed configuration": MappedTerm("MFE Topology", "exact", "Compact Toroid"),
    "compact toroid": MappedTerm("MFE Topology", "exact", "Compact Toroid"),
    "dipole": MappedTerm("MFE Topology", "exact", "Dipole"),
    "levitated dipole": MappedTerm("MFE Topology", "exact", "Dipole"),

    # IFE Driver
    "laser driver": MappedTerm("IFE Driver", "exact", "Laser"),
    "laser": MappedTerm("IFE Driver", "exact", "Laser"),
    "projectile driver": MappedTerm("IFE Driver", "exact", "Projectile"),
    "projectile": MappedTerm("IFE Driver", "exact", "Projectile"),
    "heavy ion beam": MappedTerm("IFE Driver", "exact", "Heavy ion beam"),
    "acoustic driver": MappedTerm("IFE Driver", "exact", "Acoustic"),

    # Fuel
    "d-t": MappedTerm("Fuel", "exact", "D-T"),
    "d-t fuel": MappedTerm("Fuel", "exact", "D-T"),
    "deuterium-tritium": MappedTerm("Fuel", "exact", "D-T"),
    "d-he3": MappedTerm("Fuel", "exact", "D-He3"),
    "deuterium-helium-3": MappedTerm("Fuel", "exact", "D-He3"),
    "p-b11": MappedTerm("Fuel", "exact", "p-B11"),
    "proton-boron": MappedTerm("Fuel", "exact", "p-B11"),
    "proton-boron-11": MappedTerm("Fuel", "exact", "p-B11"),
    "d-d": MappedTerm("Fuel", "exact", "D-D"),
    "deuterium-deuterium": MappedTerm("Fuel", "exact", "D-D"),
    "aneutronic fuel": MappedTerm("Fuel", "in_set", ["p-B11", "D-He3"]),

    # Operation Mode
    "pulsed": MappedTerm("Operation Mode", "exact", "Pulsed"),
    "pulsed operation": MappedTerm("Operation Mode", "exact", "Pulsed"),
    "steady-state": MappedTerm("Operation Mode", "exact", "Steady-state"),
    "steady state": MappedTerm("Operation Mode", "exact", "Steady-state"),
    "quasi-steady": MappedTerm("Operation Mode", "exact", "Quasi-steady"),

    # Magnet Type
    "needs magnets": MappedTerm("Magnet Type", "not", "N/A"),
    "requires magnets": MappedTerm("Magnet Type", "not", "N/A"),
    "no magnets": MappedTerm("Magnet Type", "exact", "N/A"),
    "hts magnets": MappedTerm("Magnet Type", "contains", "HTS"),
    "superconducting magnets": MappedTerm("Magnet Type", "not", "Resistive"),

    # Blanket Config (v3 — replaces Tritium Breeding and Neutron Management)
    "liquid metal blanket": MappedTerm("Blanket Config", "exact", "Liquid metal"),
    "liquid metal": MappedTerm("Blanket Config", "exact", "Liquid metal"),
    "liquid lithium blanket": MappedTerm("Blanket Config", "exact", "Liquid metal"),
    "molten salt blanket": MappedTerm("Blanket Config", "exact", "Molten salt"),
    "molten salt": MappedTerm("Blanket Config", "exact", "Molten salt"),
    "flibe blanket": MappedTerm("Blanket Config", "exact", "Molten salt"),
    "solid breeder": MappedTerm("Blanket Config", "exact", "Solid breeder"),
    "solid breeder blanket": MappedTerm("Blanket Config", "exact", "Solid breeder"),
    "hybrid blanket": MappedTerm("Blanket Config", "exact", "Other/hybrid"),
    "other blanket": MappedTerm("Blanket Config", "exact", "Other/hybrid"),
    "no tritium breeding": MappedTerm("Blanket Config", "exact", "N/A (no tritium)"),
    "no blanket": MappedTerm("Blanket Config", "exact", "N/A (no tritium)"),
    "non-power blanket": MappedTerm("Blanket Config", "exact", "N/A (non-power)"),
    "tritium breeding": MappedTerm(
        "Blanket Config", "in_set",
        ["Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid"],
    ),
    "must breed tritium": MappedTerm(
        "Blanket Config", "in_set",
        ["Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid"],
    ),

    # Energy Capture
    "thermal conversion": MappedTerm("Energy Capture", "contains", "Thermal"),
    "thermal energy conversion": MappedTerm("Energy Capture", "contains", "Thermal"),
    "direct conversion": MappedTerm("Energy Capture", "contains", "Direct"),
    "direct energy conversion": MappedTerm("Energy Capture", "contains", "Direct"),
    "hybrid conversion": MappedTerm("Energy Capture", "contains", "Hybrid"),

    # Primary Heating
    "rf heating": MappedTerm("Primary Heating", "contains", "RF"),
    "neutral beam injection": MappedTerm("Primary Heating", "contains", "NBI"),
    "nbi": MappedTerm("Primary Heating", "contains", "NBI"),
    "ohmic heating": MappedTerm("Primary Heating", "contains", "Ohmic"),
    "laser heating": MappedTerm("Primary Heating", "contains", "Laser"),
    "compression heating": MappedTerm("Primary Heating", "contains", "compression"),
}


def normalize_key(text: str) -> str:
    """Normalize text for vocabulary lookup."""
    return text.strip().lower()


def lookup_term(text: str) -> MappedTerm | None:
    """Look up a natural language term in the vocabulary map."""
    key = normalize_key(text)
    return VOCABULARY.get(key)


# ---------------------------------------------------------------------------
# Constraint-to-table mapping
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Result of validating a constraint against the table."""
    table_check: str         # PASS | FAIL | FLAG | UNMAPPABLE
    concepts_checked: int
    concepts_matched: int
    violations: list[str]    # concept names that violate
    notes: str


def map_and_validate(
    condition: dict,
    consequence: dict,
    constraint_type: str,
    table: list[dict[str, str]],
) -> ValidationResult:
    """Map constraint condition/consequence to table and validate.

    condition: dict with keys that are natural-language descriptions
               e.g., {"confinement_approach": "magnetic"}
    consequence: dict with keys like "variable" and "value"
               e.g., {"variable": "magnet_type", "value": "not N/A"}
    constraint_type: "force" | "eliminate" | "activate"
    """
    # Try to map condition to a table filter
    condition_filters = _map_dict_to_filters(condition)
    if not condition_filters:
        return ValidationResult("UNMAPPABLE", 0, 0, [], "Condition not mappable to table columns")

    # Try to map consequence to a table check
    consequence_term = _map_consequence(consequence)
    if consequence_term is None:
        return ValidationResult("UNMAPPABLE", 0, 0, [], "Consequence not mappable to table columns")

    # Filter rows matching ALL conditions
    matching_rows = table
    for filt in condition_filters:
        matching_rows = [r for r in matching_rows if filt.matches(r.get(filt.column, ""))]

    if not matching_rows:
        return ValidationResult(
            "FLAG", 0, 0, [],
            f"No table rows match condition filters (columns: {[f.column for f in condition_filters]})"
        )

    # Check consequence against matching rows
    # TBD/Unknown values are excluded — they're ambiguous, not real violations
    violations = []
    tbd_count = 0
    for row in matching_rows:
        cell_value = row.get(consequence_term.column, "")
        if MappedTerm.is_tbd(cell_value):
            tbd_count += 1
            continue  # skip TBD — not enough info to call it a violation
        if constraint_type == "eliminate":
            # Eliminate: the value should NOT appear. Violation = value IS present.
            if consequence_term.matches(cell_value):
                violations.append(row["Concept Name"])
        else:
            # Force/activate: the consequence SHOULD hold
            if not consequence_term.matches(cell_value):
                violations.append(row["Concept Name"])

    n_checked = len(matching_rows) - tbd_count  # only count decidable rows
    n_violations = len(violations)

    if n_checked == 0:
        status = "FLAG"
        note = f"All {len(matching_rows)} matching rows are TBD"
    elif n_violations == 0:
        status = "PASS"
        note = f"{n_checked}/{n_checked} decidable concepts match"
    elif n_violations <= max(1, int(0.2 * n_checked)):
        status = "FLAG"
        note = f"{n_checked - n_violations}/{n_checked} decidable concepts match"
    else:
        status = "FAIL"
        note = f"{n_checked - n_violations}/{n_checked} decidable concepts match"

    if tbd_count:
        note += f" ({tbd_count} TBD excluded)"

    return ValidationResult(
        table_check=status,
        concepts_checked=n_checked,
        concepts_matched=n_checked - n_violations,
        violations=violations,
        notes=note,
    )


def _map_dict_to_filters(d: dict) -> list[MappedTerm]:
    """Try to map a condition dict to MappedTerm filters.

    The dict may have keys like:
      {"confinement_approach": "magnetic"}
      {"fuel": "D-T", "confinement_approach": "magnetic"}

    We try to match each value against the vocabulary.
    """
    filters = []
    for key, value in d.items():
        # Try the value directly
        term = lookup_term(str(value))
        if term:
            filters.append(term)
            continue
        # Try "key value" combination
        term = lookup_term(f"{key} {value}")
        if term:
            filters.append(term)
            continue
        # Try key as column name directly
        term = _try_direct_column_match(key, value)
        if term:
            filters.append(term)
    return filters


def _map_consequence(consequence: dict) -> MappedTerm | None:
    """Map a consequence dict to a MappedTerm for checking.

    consequence may look like:
      {"variable": "magnet_type", "value": "not N/A"}
      {"variable": "blanket_config", "value": "liquid metal"}
      {"type": "activate", "variable": "blanket_config"}
    """
    # Try the value
    value = consequence.get("value", "")
    if value:
        term = lookup_term(str(value))
        if term:
            return term

    # Try variable + value
    variable = consequence.get("variable", "")
    if variable and value:
        term = lookup_term(f"{variable} {value}")
        if term:
            return term

    # For "activate" type, try the variable name
    if consequence.get("type") == "activate" and variable:
        term = lookup_term(variable)
        if term:
            # Convert to a "not N/A" check
            return MappedTerm(term.column, "not_na")

    # Try variable name alone
    if variable:
        term = lookup_term(variable)
        if term:
            return term

    return None


KEY_TO_COLUMN = {
    "confinement_approach": "Confinement Family",
    "confinement_family": "Confinement Family",
    "confinement": "Confinement Family",
    "mfe_topology": "MFE Topology",
    "topology": "MFE Topology",
    "fuel": "Fuel",
    "fuel_type": "Fuel",
    "heating": "Primary Heating",
    "primary_heating": "Primary Heating",
    "energy_conversion": "Energy Capture",
    "energy_capture": "Energy Capture",
    "magnet_type": "Magnet Type",
    "magnets": "Magnet Type",
    "blanket_config": "Blanket Config",
    "blanket": "Blanket Config",
    "operation_mode": "Operation Mode",
    "ife_driver": "IFE Driver",
    "driver": "IFE Driver",
    "repetition_rate": "Repetition Rate",
    "tokamak_shape": "Tokamak Shape",
    "stellarator_type": "Stellarator Type",
    "laser_approach": "Laser Approach",
    "mif_method": "MIF Method",
}

# Map from short LLM value → table value, grouped by column
VALUE_ALIASES: dict[str, dict[str, str]] = {
    "Confinement Family": {
        "magnetic": "MFE",
        "inertial": "IFE",
        "magnetized target": "MIF",
        "hybrid": "MIF",
    },
    "Operation Mode": {
        "pulsed": "Pulsed",
        "steady-state": "Steady-state",
        "steady state": "Steady-state",
        "quasi-steady": "Quasi-steady",
    },
    "Fuel": {
        "dt": "D-T",
        "d-t": "D-T",
        "deuterium-tritium": "D-T",
        "d-he3": "D-He3",
        "p-b11": "p-B11",
        "d-d": "D-D",
    },
    "Blanket Config": {
        "liquid metal": "Liquid metal",
        "liquid lithium": "Liquid metal",
        "flibe": "Molten salt",
        "molten salt": "Molten salt",
        "solid breeder": "Solid breeder",
        "hybrid": "Other/hybrid",
        "other": "Other/hybrid",
        "none": "N/A (no tritium)",
        "n/a": "N/A (no tritium)",
    },
}


def _try_direct_column_match(key: str, value: str) -> MappedTerm | None:
    """Try matching key directly as a column name, resolving value aliases."""
    col = KEY_TO_COLUMN.get(key.lower().strip())
    if not col:
        return None

    # Try value alias for this column
    val_lower = value.lower().strip()
    aliases = VALUE_ALIASES.get(col, {})
    resolved = aliases.get(val_lower)
    if resolved:
        return MappedTerm(col, "exact", resolved)

    # Fall back to contains match with raw value
    return MappedTerm(col, "contains", str(value))
