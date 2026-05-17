"""Deterministic scoring computations for the LCOE Downselect pipeline.

Implements C2 (confinement category), C6 (fuel x mode), heritage credit,
C7 computation (mean of F1-F7 with cap), and YAML score extraction.

Design principle: Claude does judgment, Python does arithmetic.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from lib.validators import ValidationResult

# ---------------------------------------------------------------------------
# C2: Scalability — deterministic lookup by confinement category
# ---------------------------------------------------------------------------

# Concept ID prefix -> C2 category (from SCORING_SYSTEM.md)
_C2_CONCEPT_MAP: dict[str, str] = {
    "01": "Conventional Tokamak",
    "21": "Conventional Tokamak",
    "28": "Conventional Tokamak",
    "29": "Conventional Tokamak",
    "33": "Conventional Tokamak",
    "34": "Conventional Tokamak",
    "05": "Stellarator",
    "09": "Stellarator",
    "10": "Stellarator",
    "20a": "Stellarator",
    "20b": "Stellarator",
    "36": "Stellarator",
    "06": "Mirror",
    "11": "Mirror",
    "08": "FRC / Compact Pulsed MFE",
    "15": "FRC / Compact Pulsed MFE",
    "18": "FRC / Compact Pulsed MFE",
    "03": "Laser IFE",
    "04": "Laser IFE",
    "17a": "Laser IFE",
    "17b": "Laser IFE",
    "26": "Laser IFE",
    "30": "Laser IFE",
    "31": "Laser IFE",
    "32": "Laser IFE",
    "07": "Pulsed MIF",
    "14": "Pulsed MIF",
    "22": "Pulsed MIF",
    "12": "Levitated Dipole",
    "19": "Levitated Dipole",
    "02": "Exotic/Novel",
    "13": "Exotic/Novel",
    "16": "Exotic/Novel",
    "24": "Exotic/Novel",
    "25": "Exotic/Novel",
    "27": "Exotic/Novel",
    "35": "Exotic/Novel",
}

C2_SCORES: dict[str, float] = {
    "Conventional Tokamak": 2.5,
    "Stellarator": 2.5,
    "Mirror": 3.5,
    "FRC / Compact Pulsed MFE": 3.5,
    "Laser IFE": 3.5,
    "Pulsed MIF": 3.0,
    "Levitated Dipole": 2.0,
    "Exotic/Novel": 4.0,
}


def detect_c2_category(concept: dict) -> tuple[str, float]:
    """Map a concept to its C2 confinement category and score.

    Uses the explicit concept ID mapping from SCORING_SYSTEM.md.
    Falls back to table.csv Confinement Family for unmapped concepts.

    Returns (category_name, c2_score).
    """
    num = concept["_num"]
    if num in _C2_CONCEPT_MAP:
        cat = _C2_CONCEPT_MAP[num]
        return cat, C2_SCORES[cat]

    # Fallback: map from table.csv columns
    family = concept.get("Confinement Family", "")
    topology = concept.get("MFE Topology", "")
    driver = concept.get("IFE Driver", "")

    if family == "MFE":
        if topology == "Tokamak":
            return "Conventional Tokamak", C2_SCORES["Conventional Tokamak"]
        elif topology == "Stellarator":
            return "Stellarator", C2_SCORES["Stellarator"]
        elif topology in ("Open/Linear", "Mirror"):
            return "Mirror", C2_SCORES["Mirror"]
        elif topology in ("FRC", "Compact"):
            return "FRC / Compact Pulsed MFE", C2_SCORES["FRC / Compact Pulsed MFE"]
    elif family == "IFE":
        if driver in ("Laser", "laser"):
            return "Laser IFE", C2_SCORES["Laser IFE"]
    elif family == "MIF":
        return "Pulsed MIF", C2_SCORES["Pulsed MIF"]

    # Default: Exotic/Novel for anything unmapped
    return "Exotic/Novel", C2_SCORES["Exotic/Novel"]


# ---------------------------------------------------------------------------
# C6: Upper Capacity Factor — deterministic lookup by fuel x operation mode
# ---------------------------------------------------------------------------

C6_SCORES: dict[tuple[str, str], float] = {
    ("D-T", "Steady-State"): 2.5,
    ("D-T", "Pulsed"): 2.0,
    ("D-D", "Steady-State"): 3.5,
    ("D-D", "Pulsed"): 3.0,
    ("D-He3", "Steady-State"): 4.0,
    ("D-He3", "Pulsed"): 3.5,
    ("p-B11", "Steady-State"): 4.5,
    ("p-B11", "Pulsed"): 4.0,
}


def detect_c6_category(concept: dict) -> tuple[str, float]:
    """Map a concept to its C6 fuel x mode category and score.

    Uses the Fuel and Operation Mode columns from table.csv.

    Returns (category_label, c6_score).
    """
    fuel = concept.get("Fuel", "").strip()
    mode_raw = concept.get("Operation Mode", "").strip().lower()

    # Normalize operation mode to Pulsed or Steady-State
    if "pulsed" in mode_raw:
        mode = "Pulsed"
    elif "steady" in mode_raw or "quasi" in mode_raw or "continuous" in mode_raw:
        mode = "Steady-State"
    else:
        # Default: steady-state for ambiguous modes
        mode = "Steady-State"

    # Normalize fuel
    fuel_normalized = fuel  # table.csv uses D-T, D-D, D-He3, p-B11 directly
    if fuel_normalized not in ("D-T", "D-D", "D-He3", "p-B11"):
        # Try common variations
        fuel_map = {"DT": "D-T", "DD": "D-D", "DHe3": "D-He3", "PB11": "p-B11"}
        fuel_normalized = fuel_map.get(fuel.replace("-", "").replace(" ", ""), "D-T")

    key = (fuel_normalized, mode)
    score = C6_SCORES.get(key, 2.5)  # default to D-T Steady-State
    return f"{fuel_normalized} {mode}", score


# ---------------------------------------------------------------------------
# Heritage credit — D-T fuel only, floors F1-F3
# ---------------------------------------------------------------------------

HERITAGE_FLOORS: dict[str, float] = {
    "Tokamak": 4.0,
    "Stellarator": 4.0,
    "Laser IFE": 3.5,
    "Mirror": 2.5,
    "FRC": 2.5,
    "Spherical Tokamak": 3.0,
    "Z-pinch": 2.5,
    "magLIF": 3.0,
}

# Concept ID prefix -> heritage lineage
_HERITAGE_MAP: dict[str, str] = {
    "01": "Tokamak", "21": "Tokamak", "28": "Tokamak",
    "29": "Tokamak", "33": "Tokamak", "34": "Tokamak",
    "05": "Stellarator", "09": "Stellarator", "10": "Stellarator",
    "20a": "Stellarator", "20b": "Stellarator", "36": "Stellarator",
    "11": "Mirror",
    "03": "Laser IFE", "04": "Laser IFE",
    "17a": "Laser IFE", "17b": "Laser IFE",
    "26": "Laser IFE", "30": "Laser IFE", "31": "Laser IFE", "32": "Laser IFE",
    "08": "FRC", "18": "FRC",
    "15": "Z-pinch",
    "07": "magLIF",
    "06": "Mirror",
}


def _get_heritage_lineage(concept: dict) -> str | None:
    """Get the heritage lineage for a concept, if any."""
    return _HERITAGE_MAP.get(concept["_num"])


def apply_heritage_credit(
    scores: dict, concept: dict
) -> dict:
    """Apply D-T heritage credit to F1-F7 scores.

    Heritage credit only applies to D-T fuel. It provides a floor on every
    function score (F1-F7), overriding only if the scored value falls below
    the floor. Heritage acknowledges decades of engineering work across the
    full plant (plasma physics, divertor, neutron handling, fuel cycle, BOP),
    not just plasma physics.

    Returns a new dict with potentially updated F1-F7.
    """
    fuel = concept.get("Fuel", "").strip()
    if fuel != "D-T":
        return dict(scores)

    lineage = _get_heritage_lineage(concept)
    if lineage is None or lineage not in HERITAGE_FLOORS:
        return dict(scores)

    floor = HERITAGE_FLOORS[lineage]
    result = dict(scores)
    for key in ("F1", "F2", "F3", "F4", "F5", "F6", "F7"):
        if key in result and result[key] < floor:
            result[key] = floor

    return result


# ---------------------------------------------------------------------------
# C7 computation — mean of F1-F7 with function-level cap
# ---------------------------------------------------------------------------

def compute_c7(scores: dict) -> float:
    """Compute C7 from F1-F7 function-level means.

    1. C7 = mean of F1-F7
    2. Round to nearest 0.5
    3. Function-level cap: if any function mean <= 1.5, C7 is capped at
       that function's actual value

    Expects scores dict with keys F1-F7 (floats).
    """
    f_keys = ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]
    f_values = [scores[k] for k in f_keys]

    # Check function-level cap
    min_f = min(f_values)
    raw_mean = sum(f_values) / len(f_values)

    if min_f <= 1.5:
        c7 = min(raw_mean, min_f)
    else:
        c7 = raw_mean

    # Round to nearest 0.5
    c7 = round(c7 * 2) / 2
    return c7


# ---------------------------------------------------------------------------
# YAML score extraction from synthesis.md
# ---------------------------------------------------------------------------

def parse_yaml_scores(synthesis_path: Path) -> dict | None:
    """Extract the YAML scores block from a synthesis.md file.

    Looks for a fenced YAML block containing a 'scores:' key at the end
    of the file (Section 8). Returns the scores dict or None if not found.

    No regex fallback — if the YAML block is missing or malformed, returns None.
    """
    text = synthesis_path.read_text(encoding="utf-8")

    # Find the last YAML block (delimited by --- or ```yaml)
    # Strategy: look for the scores YAML block pattern
    # It should be near the end of the file, after Section 8

    # Try fenced code block first: ```yaml ... ```
    yaml_blocks = re.findall(
        r"```ya?ml\s*\n(.*?)```",
        text,
        re.DOTALL,
    )

    # Also try bare --- delimited blocks at the end (not the frontmatter)
    # The frontmatter is at the very start; we want the last --- block
    bare_blocks = []
    # Skip the frontmatter (first --- ... --- block)
    body = text
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    if fm_match:
        body = text[fm_match.end():]
    bare_matches = re.findall(r"^---\s*\n(.*?)\n---\s*$", body, re.DOTALL | re.MULTILINE)
    bare_blocks.extend(bare_matches)

    # Combine all candidates, prefer the last one with 'scores:'
    candidates = yaml_blocks + bare_blocks
    for block in reversed(candidates):
        if "scores:" not in block:
            continue
        # Use safe_load_all so blocks containing YAML document separators
        # (e.g. fenced ```yaml --- ... --- ``` blocks) parse correctly.
        try:
            documents = list(yaml.safe_load_all(block))
        except yaml.YAMLError:
            continue
        for parsed in documents:
            if isinstance(parsed, dict) and "scores" in parsed:
                return parsed["scores"]
            if isinstance(parsed, dict) and "C1" in parsed:
                return parsed

    return None


def has_section8(synthesis_path: Path) -> bool:
    """Check if a synthesis already has Section 8."""
    text = synthesis_path.read_text(encoding="utf-8")
    markers = [
        "## 8. LCOE Downselect",
        "## 8 LCOE Downselect",
        "LCOE Downselect Scoring",
        "## 8.",
    ]
    return any(m in text for m in markers)


# ---------------------------------------------------------------------------
# Verified scores: orchestrate extraction for all concepts
# ---------------------------------------------------------------------------

def build_verified_scores(
    concepts: list[dict], analyses_dir: Path
) -> tuple[list[dict], list[str]]:
    """Extract and compute verified scores for all concepts with YAML blocks.

    Returns:
        (scores_list, warnings) where each score dict has:
        - concept_id, concept_name, company
        - C1-C8 (all eight criteria)
        - F1-F7 (function means, after heritage)
        - binary_risks (list of strings)
        - c2_category, c6_category
    """
    scores_list = []
    warnings = []

    for concept in concepts:
        cid = concept["_id"]
        synthesis_path = analyses_dir / cid / "synthesis.md"

        if not synthesis_path.exists():
            continue

        if not has_section8(synthesis_path):
            continue

        raw = parse_yaml_scores(synthesis_path)
        if raw is None:
            warnings.append(f"{cid}: synthesis has Section 8 but YAML block missing or malformed")
            continue

        # Validate required Claude-scored fields
        required_claude = ["C1", "C3", "C4", "C5", "C8"]
        required_functions = ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]
        missing = [k for k in required_claude + required_functions if k not in raw]
        if missing:
            warnings.append(f"{cid}: YAML block missing fields: {', '.join(missing)}")
            continue

        # Compute deterministic scores
        c2_cat, c2_score = detect_c2_category(concept)
        c6_cat, c6_score = detect_c6_category(concept)

        # Build function scores dict and apply heritage
        f_scores = {k: float(raw[k]) for k in required_functions}
        f_scores_heritage = apply_heritage_credit(f_scores, concept)

        # Compute C7
        c7 = compute_c7(f_scores_heritage)

        entry = {
            "concept_id": cid,
            "concept_name": concept.get("Concept Name", ""),
            "company": concept.get("Company", ""),
            "C1": float(raw["C1"]),
            "C2": c2_score,
            "C3": float(raw["C3"]),
            "C4": float(raw["C4"]),
            "C5": float(raw["C5"]),
            "C6": c6_score,
            "C7": c7,
            "C8": float(raw["C8"]),
            "F1": f_scores_heritage["F1"],
            "F2": f_scores_heritage["F2"],
            "F3": f_scores_heritage["F3"],
            "F4": f_scores_heritage["F4"],
            "F5": f_scores_heritage["F5"],
            "F6": f_scores_heritage["F6"],
            "F7": f_scores_heritage["F7"],
            "binary_risks": raw.get("binary_risks", []),
            "binary_count": len(raw.get("binary_risks", [])),
            "c2_category": c2_cat,
            "c6_category": c6_cat,
        }
        scores_list.append(entry)

    return scores_list, warnings


def write_verified_json(scores: list[dict], path: Path) -> None:
    """Write verified scores to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(scores, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_verified_md(scores: list[dict], path: Path) -> None:
    """Write verified scores as a markdown table."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# Verified Scores", ""]
    lines.append(
        "| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Binary Risks |"
    )
    lines.append(
        "|---------|----|----|----|----|----|----|----|----|-------------|"
    )
    for s in scores:
        binary = len(s.get("binary_risks", []))
        lines.append(
            f"| {s['concept_id']} | {s['C1']:.1f} | {s['C2']:.1f} | "
            f"{s['C3']:.1f} | {s['C4']:.1f} | {s['C5']:.1f} | {s['C6']:.1f} | "
            f"{s['C7']:.1f} | {s['C8']:.1f} | {binary} |"
        )

    lines.append("")
    lines.append("## Function-Level Means (after heritage credit)")
    lines.append("")
    lines.append(
        "| Concept | F1 | F2 | F3 | F4 | F5 | F6 | F7 |"
    )
    lines.append(
        "|---------|----|----|----|----|----|----|-----|"
    )
    for s in scores:
        lines.append(
            f"| {s['concept_id']} | {s['F1']:.1f} | {s['F2']:.1f} | "
            f"{s['F3']:.1f} | {s['F4']:.1f} | {s['F5']:.1f} | {s['F6']:.1f} | "
            f"{s['F7']:.1f} |"
        )

    lines.append("")
    lines.append("## Binary Risks per Concept")
    lines.append("")
    for s in scores:
        risks = s.get("binary_risks", [])
        if risks:
            lines.append(f"### {s['concept_id']}")
            for r in risks:
                lines.append(f"- {r}")
            lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Calibrated score parsing — parse Claude's calibration output
# ---------------------------------------------------------------------------

def _clean_score_cell(cell: str) -> str:
    """Strip markdown bold markers, asterisks, and whitespace from a table cell."""
    return cell.strip().strip("*").strip()


def parse_calibrated_table(text: str) -> list[dict]:
    """Parse the calibrated score table from Claude's calibration output.

    Expects format: | concept_id | C1 | C2 | ... | C8 |
    Returns list of dicts with concept_id and C1-C8 as floats.

    Robust to: bold markers (**X.X**), trailing whitespace, multiple tables
    in output (finds the one with 9+ columns including concept_id + C1-C8).
    """
    results = []
    in_table = False
    header_seen = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and header_seen and results:
                break  # table ended after we got data
            in_table = False
            header_seen = False
            continue

        cells = [_clean_score_cell(c) for c in stripped.split("|")[1:-1]]
        if not cells:
            continue

        # Separator row (---|---|...)
        if all(set(c) <= set("-: ") for c in cells):
            in_table = True
            continue

        # Header row detection
        if any(c.lower() in ("concept_id", "concept") for c in cells[:1]):
            in_table = True
            header_seen = True
            continue
        if any("C1" in c for c in cells):
            in_table = True
            header_seen = True
            continue

        if not in_table:
            continue

        # Data row — need at least 9 cells (concept + C1-C8)
        if len(cells) >= 9:
            concept_id = cells[0]
            # Validate concept_id looks like a concept ID (starts with digits)
            if not concept_id or not concept_id[0].isdigit():
                continue
            try:
                entry = {
                    "concept_id": concept_id,
                    "C1": float(_clean_score_cell(cells[1])),
                    "C2": float(_clean_score_cell(cells[2])),
                    "C3": float(_clean_score_cell(cells[3])),
                    "C4": float(_clean_score_cell(cells[4])),
                    "C5": float(_clean_score_cell(cells[5])),
                    "C6": float(_clean_score_cell(cells[6])),
                    "C7": float(_clean_score_cell(cells[7])),
                    "C8": float(_clean_score_cell(cells[8])),
                }
                results.append(entry)
            except (ValueError, IndexError):
                continue

    return results


def validate_calibration_output(text: str) -> ValidationResult:
    """Validate that calibration output contains a parseable score table.

    Checks for:
    1. Non-empty output
    2. At least one parseable row in a calibrated score table
    """
    if not text.strip():
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your output was empty. Please re-read the calibration instructions "
                "and produce the calibrated score table and adjustments report."
            ),
            details="Output is empty",
        )

    rows = parse_calibrated_table(text)
    if not rows:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Could not parse any rows from your calibrated score table. "
                "Your table MUST use this exact format with plain numbers only:\n\n"
                "| concept_id | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |\n"
                "|------------|----|----|----|----|----|----|----|----|----|\n"
                "| 01-hts-compact-tokamak | 3.5 | 2.5 | 3.0 | 3.0 | 2.5 | 2.5 | 3.0 | 3.5 |\n\n"
                "Do NOT use bold markers, annotations, or non-numeric values in score cells. "
                "Please output the complete calibrated table now."
            ),
            details="No parseable rows in calibrated score table",
        )

    return ValidationResult(
        valid=True,
        details=f"Calibrated table: {len(rows)} rows parsed",
    )


def validate_score_output(text: str) -> ValidationResult:
    """Validate that score output contains a well-formed YAML scores block.

    Checks for:
    1. Non-empty output
    2. Presence of a YAML block with 'scores:' key
    3. Required fields: C1, C3, C4, C5, C8, F1-F7, binary_risks
    """
    if not text.strip():
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your output was empty. Please re-read the instructions "
                "and produce Section 8 with the score table, risk matrix, "
                "and YAML scores block."
            ),
            details="Output is empty",
        )

    # Check for YAML block presence
    has_yaml = False
    yaml_blocks = re.findall(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    bare_blocks = re.findall(r"^---\s*\n(.*?)\n---\s*$", text, re.DOTALL | re.MULTILINE)
    candidates = yaml_blocks + bare_blocks

    parsed_scores = None
    for block in reversed(candidates):
        if "scores:" in block:
            try:
                parsed = yaml.safe_load(block)
                if isinstance(parsed, dict) and "scores" in parsed:
                    parsed_scores = parsed["scores"]
                    has_yaml = True
                    break
            except yaml.YAMLError:
                continue

    if not has_yaml or parsed_scores is None:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your output is missing the required YAML scores block. "
                "You MUST end Section 8 with a YAML block in this format:\n\n"
                "```yaml\n---\nscores:\n  C1: X.X\n  C3: X.X\n  C4: X.X\n"
                "  C5: X.X\n  C8: X.X\n  F1: X.X\n  F2: X.X\n  F3: X.X\n"
                "  F4: X.X\n  F5: X.X\n  F6: X.X\n  F7: X.X\n  binary_risks:\n"
                "    - \"risk description\"\n---\n```\n\n"
                "Please add the YAML scores block now."
            ),
            details="YAML scores block missing or malformed",
        )

    # Check required fields
    required = ["C1", "C3", "C4", "C5", "C8", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]
    missing = [k for k in required if k not in parsed_scores]
    if missing:
        return ValidationResult(
            valid=False,
            fix_message=(
                f"Your YAML scores block is missing required fields: {', '.join(missing)}. "
                f"All of these must be present: {', '.join(required)} plus binary_risks. "
                f"Please add the missing fields to the YAML block."
            ),
            details=f"YAML block missing fields: {', '.join(missing)}",
        )

    # Check binary_risks is present (can be empty list)
    if "binary_risks" not in parsed_scores:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your YAML scores block is missing the 'binary_risks' field. "
                "Add 'binary_risks:' with a list of binary risk descriptions "
                "(or an empty list [] if no binary risks)."
            ),
            details="YAML block missing binary_risks field",
        )

    return ValidationResult(valid=True, details="YAML scores block valid")


def parse_adjustments(text: str) -> list[dict]:
    """Parse the adjustments report table from Claude's calibration output.

    Expects format: | Concept | Question | Criterion | Original | Adjusted | Justification |
    Looks for this table anywhere in the text (not just the first table).
    """
    results = []
    in_table = False
    is_adjustment_table = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and is_adjustment_table and results:
                break  # adjustment table ended after getting data
            in_table = False
            is_adjustment_table = False
            continue

        cells = [_clean_score_cell(c) for c in stripped.split("|")[1:-1]]
        if not cells:
            continue

        if all(set(c) <= set("-: ") for c in cells):
            in_table = True
            continue

        # Detect the adjustments table header specifically
        cell_text = " ".join(c.lower() for c in cells[:3])
        if "question" in cell_text or "criterion" in cell_text or "adjustment" in cell_text:
            in_table = True
            is_adjustment_table = True
            continue

        if not in_table or not is_adjustment_table:
            continue

        if len(cells) >= 5:
            results.append({
                "concept": cells[0],
                "question": cells[1] if len(cells) > 1 else "",
                "criterion": cells[2] if len(cells) > 2 else "",
                "original": cells[3] if len(cells) > 3 else "",
                "adjusted": cells[4] if len(cells) > 4 else "",
                "justification": cells[5] if len(cells) > 5 else "",
            })

    return results
