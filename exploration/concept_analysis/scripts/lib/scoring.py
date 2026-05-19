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

from lib.canonical_params import canonical_eta_th
from lib.validators import ValidationResult

# ---------------------------------------------------------------------------
# C2: Scalability — derived from confinement architecture in table.csv
# ---------------------------------------------------------------------------

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

    Derived from architecture columns in table.csv (Confinement Family,
    MFE Topology, IFE Driver, MIF Method, Magnet Type) plus the concept
    slug for disambiguation. Mirrors the design of ``_get_heritage_lineage``
    so the lookup survives concept ID renumbering — do NOT add a hardcoded
    ID-prefix map here.

    Returns (category_name, c2_score).
    """
    family = concept.get("Confinement Family", "").strip()
    topology = concept.get("MFE Topology", "").strip()
    mif_method = concept.get("MIF Method", "").strip()
    driver = concept.get("IFE Driver", "").strip()
    magnet_type = concept.get("Magnet Type", "").strip().lower()
    cid = concept.get("_id", "").lower()

    if family == "MFE":
        if topology == "Tokamak":
            return "Conventional Tokamak", C2_SCORES["Conventional Tokamak"]
        if topology == "Stellarator":
            return "Stellarator", C2_SCORES["Stellarator"]
        if topology in ("Open/Linear", "Mirror"):
            # Z-pinch shares the Open/Linear topology label but clusters with
            # compact pulsed MFE for scalability, not with steady-state mirrors.
            if "pinch" in cid:
                return (
                    "FRC / Compact Pulsed MFE",
                    C2_SCORES["FRC / Compact Pulsed MFE"],
                )
            return "Mirror", C2_SCORES["Mirror"]
        if topology in ("Compact Toroid", "FRC", "Compact"):
            return (
                "FRC / Compact Pulsed MFE",
                C2_SCORES["FRC / Compact Pulsed MFE"],
            )
        if topology == "Dipole":
            # Levitated dipoles (OpenStar, Zephyr) inherit the LDX research
            # heritage; non-levitated dipole approaches (e.g. PoloMac tunnel
            # supports) are a different scalability story → Exotic/Novel.
            if "levitated" in magnet_type:
                return "Levitated Dipole", C2_SCORES["Levitated Dipole"]
            return "Exotic/Novel", C2_SCORES["Exotic/Novel"]
        return "Exotic/Novel", C2_SCORES["Exotic/Novel"]

    if family == "IFE":
        if driver == "Laser":
            return "Laser IFE", C2_SCORES["Laser IFE"]
        # Heavy ion beam, projectile, acoustic, etc. — no operating fleet
        # in the relevant regime; bucket as Exotic/Novel.
        return "Exotic/Novel", C2_SCORES["Exotic/Novel"]

    if family == "MIF":
        # FRC-compression MIF (Helion) is architecturally a compact pulsed
        # MFE device; liner-imploded MIF (Pacific Fusion, General Fusion)
        # is the canonical Pulsed MIF group.
        if mif_method == "FRC compression":
            return (
                "FRC / Compact Pulsed MFE",
                C2_SCORES["FRC / Compact Pulsed MFE"],
            )
        return "Pulsed MIF", C2_SCORES["Pulsed MIF"]

    # Non-Standard family or anything otherwise unrecognized → Exotic/Novel.
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

def _get_heritage_lineage(concept: dict) -> str | None:
    """Derive heritage lineage from concept architecture, not from the concept ID.

    Reads ``Confinement Family`` + the family-specific topology columns from
    ``table.csv`` so the lookup survives ID renumbering. Returns one of the keys
    in ``HERITAGE_FLOORS`` or ``None`` if no recognized lineage applies.

    Note: this function does NOT gate on fuel. ``apply_heritage_credit`` is
    where the D-T-only check lives.
    """
    family = concept.get("Confinement Family", "").strip()
    cid = concept.get("_id", "").lower()

    if family == "MFE":
        topo = concept.get("MFE Topology", "").strip()
        if topo == "Tokamak":
            shape = concept.get("Tokamak Shape", "").strip()
            if shape == "Spherical":
                return "Spherical Tokamak"
            return "Tokamak"
        if topo == "Stellarator":
            return "Stellarator"
        if topo == "Open/Linear":
            # Disambiguate Mirror vs Z-pinch via the concept slug — the
            # MFE Topology column does not split them, but the directory slug
            # always names the architecture explicitly.
            if "pinch" in cid:
                return "Z-pinch"
            if "mirror" in cid:
                return "Mirror"
            return None
        if topo == "Compact Toroid":
            return "FRC"
        return None

    if family == "IFE":
        if concept.get("IFE Driver", "").strip() == "Laser":
            return "Laser IFE"
        return None

    if family == "MIF":
        # magLIF heritage applies specifically to Z-machine-class pulsed-power
        # implosion of magnetized targets. Mechanical / pneumatic / acoustic
        # compression schemes are not on the magLIF heritage tree.
        if concept.get("Primary Heating", "").strip() == "Pulsed power implosion":
            return "magLIF"
        return None

    return None


def _derive_peer_group(concept: dict, lineage: str | None) -> str:
    """Assign a peer-comparison group for Q6 cross-concept consistency.

    Groups are derived from fuel + heritage lineage so they survive ID
    renumbering. The "Exotic" group is exempt from Q6 adjustments per the
    calibration prompt — D-T concepts without a major lineage land here, as
    do D-D concepts and non-FRC aneutronic concepts.
    """
    fuel = concept.get("Fuel", "").strip()
    if fuel == "D-T":
        if lineage in ("Tokamak", "Spherical Tokamak"):
            return "D-T Tokamaks"
        if lineage == "Stellarator":
            return "D-T Stellarators"
        if lineage == "Mirror":
            return "D-T Mirrors"
        if lineage == "Laser IFE":
            return "D-T Laser IFE"
        if lineage in ("Z-pinch", "magLIF"):
            return "D-T Pulsed (MIF/Z-pinch)"
        return "Exotic"
    if fuel in ("D-He3", "p-B11"):
        family = concept.get("Confinement Family", "").strip()
        topology = concept.get("MFE Topology", "").strip()
        if family == "MFE" and topology == "Compact Toroid":
            return "Aneutronic FRC"
        return "p-B11" if fuel == "p-B11" else "Aneutronic"
    return "Exotic"


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

        # Surface the energy-capture category and its canonical eta_th so future
        # audits can detect propagation failures without re-reading model_setup.py.
        # See scoring_framework.md "Standardized values" for the canonical table.
        energy_capture = concept.get("Energy Capture", "").strip()
        try:
            eta_th_canonical = canonical_eta_th(energy_capture) if energy_capture else None
        except ValueError:
            eta_th_canonical = None

        # Surface heritage and peer-group context derived from architecture so
        # the calibration prompt can read them per-concept (Q2 binary-floor and
        # Q6 peer comparison) instead of relying on hardcoded ID lookups that
        # rot when concepts get renumbered.
        lineage = _get_heritage_lineage(concept)
        if concept.get("Fuel", "").strip() == "D-T" and lineage in HERITAGE_FLOORS:
            heritage_lineage = lineage
            heritage_floor = HERITAGE_FLOORS[lineage]
        else:
            heritage_lineage = None
            heritage_floor = 1.0
        peer_group = _derive_peer_group(concept, lineage)

        entry = {
            "concept_id": cid,
            "concept_name": concept.get("Concept Name", ""),
            "company": concept.get("Company", ""),
            "energy_capture": energy_capture,
            "eta_th_canonical": eta_th_canonical,
            "heritage_lineage": heritage_lineage,
            "heritage_floor": heritage_floor,
            "peer_group": peer_group,
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
    lines.append("## Energy Capture, Heritage, and Peer Group (audit trail)")
    lines.append("")
    lines.append("Heritage lineage and floor are derived from architecture (table.csv), "
                 "not from concept IDs, so they survive renumbering. Heritage credit "
                 "applies to D-T fuel only — non-D-T concepts show floor 1.0.")
    lines.append("")
    lines.append("| Concept | Energy Capture | η_th | Heritage Lineage | Floor | Peer Group |")
    lines.append("|---------|----------------|------|------------------|-------|------------|")
    for s in scores:
        ec = s.get("energy_capture", "")
        eta = s.get("eta_th_canonical")
        eta_s = f"{eta:.2f}" if eta is not None else "—"
        lin = s.get("heritage_lineage") or "—"
        floor = s.get("heritage_floor", 1.0)
        peer = s.get("peer_group", "—")
        lines.append(f"| {s['concept_id']} | {ec} | {eta_s} | {lin} | {floor:.1f} | {peer} |")

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
        if "scores:" not in block:
            continue
        # Use safe_load_all so blocks containing YAML document separators
        # (e.g. fenced ```yaml --- ... --- ``` blocks) parse correctly. This
        # mirrors parse_yaml_scores() — keep these in sync.
        try:
            documents = list(yaml.safe_load_all(block))
        except yaml.YAMLError:
            continue
        for parsed in documents:
            if isinstance(parsed, dict) and "scores" in parsed:
                parsed_scores = parsed["scores"]
                has_yaml = True
                break
            if isinstance(parsed, dict) and "C1" in parsed:
                parsed_scores = parsed
                has_yaml = True
                break
        if has_yaml:
            break

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
