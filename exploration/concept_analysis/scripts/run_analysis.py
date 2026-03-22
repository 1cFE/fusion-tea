#!/usr/bin/env python3
"""
Automated concept analysis pipeline for Fusion TEA.

Produces D1+ concept analyses for fusion concepts using Phase 1a dossiers
and extracted sources as input. Orchestrates headless Claude calls with
template-driven prompts and an approval-based reuse pool.

Usage:
  uv run python exploration/concept_analysis/scripts/run_analysis.py list
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check 01 --dry-run
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 01
  uv run python exploration/concept_analysis/scripts/run_analysis.py approve 01
"""

import argparse
import csv
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — relative to concept_analysis directory
# ---------------------------------------------------------------------------

CONCEPT_ANALYSIS_DIR = Path(__file__).resolve().parent.parent
TABLE_PATH = CONCEPT_ANALYSIS_DIR / "table.csv"
ANALYSES_DIR = CONCEPT_ANALYSIS_DIR / "analyses"
HANDWRITTEN_DIR = CONCEPT_ANALYSIS_DIR / "handwritten"
TEMPLATES_DIR = CONCEPT_ANALYSIS_DIR / "prompt_templates"
BRIEF_PATH = CONCEPT_ANALYSIS_DIR / "concept_analysis_brief.md"

PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
RESEARCH_DIR = PHASE_1A_DIR / "research"

# 1costingfe reference paths (read-only)
COSTINGFE_DIR = Path("/home/reid/1cfe/1costingfe")
COSTINGFE_EXAMPLES_DIR = COSTINGFE_DIR / "examples"
COSTINGFE_DEFAULTS_DIR = COSTINGFE_DIR / "src" / "costingfe" / "data" / "defaults"
COSTINGFE_CONSTANTS_PATH = COSTINGFE_DEFAULTS_DIR / "costing_constants.yaml"
COSTINGFE_README_PATH = COSTINGFE_DIR / "README.md"

# Free-form model exemplar
FREEFORM_EXEMPLAR_PATH = Path("/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py")


# ---------------------------------------------------------------------------
# Model setup: concept → 1costingfe mapping
# ---------------------------------------------------------------------------

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

# Concepts that get the free-form path (no good 1costingfe mapping)
FREEFORM_CONCEPTS = {
    "12",   # Levitated Dipole (OpenStar) — dipole geometry
    "13",   # Electrostatic Hybrid — electrostatic confinement
    "15",   # Sheared-Flow Z-Pinch (Zap Energy) — continuous MFE, not IFE z-pinch
    "16",   # Muon-Catalyzed Fusion — no plasma confinement
    "18",   # p-B11 FRC (TAE) — FRC + aneutronic
    "19",   # Orbital Levitated Dipole (Zephyr) — dipole
    "24",   # Dense Plasma Focus (LPPFusion) — DPF
    "27",   # Polywell (EMC2) — electrostatic cusp
    "35",   # PoloMac (Deutelio) — custom dipole
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


def get_model_path(concept: dict) -> str:
    """Determine model-setup path for a concept.

    Returns: 'costingfe' | 'freeform'
    """
    if concept["_num"] in FREEFORM_CONCEPTS:
        return "freeform"

    # Check concept-specific override first
    cid = concept["_id"]
    if cid in COSTINGFE_MAPPING:
        return "costingfe"

    # Family-level lookup
    family = concept.get("Confinement Family", "")
    sub = _get_subcategory(concept)
    family_key = FAMILY_KEY_MAP.get((family, sub))
    if family_key and family_key in COSTINGFE_MAPPING:
        return "costingfe"

    # Default: freeform for anything not explicitly mapped
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


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Concept ID resolution
# ---------------------------------------------------------------------------


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
            print(f"Error: no concept matching '{q}'", file=sys.stderr)
            sys.exit(1)
        elif len(matches) > 1:
            print(f"Error: ambiguous query '{q}' matched {len(matches)} concepts:", file=sys.stderr)
            for m in matches:
                print(f"  {m['_id']}: {m['Concept Name']}", file=sys.stderr)
            sys.exit(1)
        resolved.append(matches[0])

    if family:
        resolved = [c for c in resolved if c.get("Confinement Family", "") == family]

    return resolved


# ---------------------------------------------------------------------------
# YAML frontmatter parsing
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Returns dict of key-value pairs. Simple parser — handles single-line
    key: value pairs and list items under a key.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    result = {}
    current_list_key = None

    for line in fm_text.splitlines():
        stripped = line.strip()
        if not stripped:
            current_list_key = None
            continue

        # List item under current key
        if stripped.startswith("- ") and current_list_key:
            if current_list_key not in result:
                result[current_list_key] = []
            if isinstance(result[current_list_key], list):
                result[current_list_key].append(stripped[2:].strip())
            continue

        # Key: value pair
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = val
                current_list_key = None
            else:
                # Key with no value — next lines might be list items
                result[key] = []
                current_list_key = key

    return result


def update_frontmatter_field(text: str, key: str, value: str) -> str:
    """Update or insert a field in YAML frontmatter.

    If the key exists (with or without a value), replace the line.
    If the key doesn't exist, insert before the closing ---.
    """
    if not text.startswith("---"):
        return text

    end = text.find("---", 3)
    if end == -1:
        return text

    fm_section = text[3:end]
    body = text[end:]

    # Try to replace existing key
    pattern = re.compile(rf"^({re.escape(key)})\s*:.*$", re.MULTILINE)
    new_line = f"{key}: {value}"
    if pattern.search(fm_section):
        fm_section = pattern.sub(new_line, fm_section)
    else:
        # Insert before end of frontmatter
        fm_section = fm_section.rstrip("\n") + f"\n{new_line}\n"

    return "---" + fm_section + body


# ---------------------------------------------------------------------------
# State detection
# ---------------------------------------------------------------------------


def get_concept_state(concept_id: str, analyses_dir: Path = ANALYSES_DIR) -> str:
    """Check filesystem to determine concept state.

    Returns: 'not-started' | 'gap-checked' | 'drafted' | 'model-setup' |
             'reviewed' | 'synthesized' | 'approved'

    Detection order (highest to lowest):
      approved → synthesized → reviewed → model-setup → drafted → gap-checked → not-started
    """
    analysis_path = analyses_dir / concept_id / "analysis.md"
    gap_path = analyses_dir / concept_id / "gap_report.md"
    model_path = analyses_dir / concept_id / "model_setup.py"
    synthesis_path = analyses_dir / concept_id / "synthesis.md"

    if analysis_path.exists():
        fm = parse_frontmatter(analysis_path)

        if fm.get("Status") == "approved":
            return "approved"
        if synthesis_path.exists():
            return "synthesized"

        review_status = fm.get("Review-Status", "")
        if review_status in ("addressed", "clean"):
            return "reviewed"

        if model_path.exists():
            return "model-setup"

        return "drafted"

    if gap_path.exists():
        return "gap-checked"
    return "not-started"


# ---------------------------------------------------------------------------
# Template engine
# ---------------------------------------------------------------------------


def make_frontmatter(concept: dict) -> str:
    """Generate YAML frontmatter deterministically.

    Reuses starts as [] — the agent updates it via Edit tool if it
    references approved prior analyses during Stage 2.
    """
    today = date.today().isoformat()
    lines = [
        "---",
        f"ID: {concept['_id']}",
        f"Concept: {concept['Concept Name']}",
        f"Company: {concept.get('Company', '')}",
        "Status: draft",
        f"Created: {today}",
        "Approved-Date:",
        "Reuses: []",
        "---",
    ]
    return "\n".join(lines) + "\n"


def fill_template(template_text: str, replacements: dict[str, str]) -> str:
    """{{variable}} substitution with {{#if var}}...{{/if}} conditionals."""
    result = template_text

    # Process conditionals first
    def replace_conditional(m):
        var_name = m.group(1)
        content = m.group(2)
        return content if replacements.get(var_name) else ""

    result = re.sub(
        r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
        replace_conditional,
        result,
        flags=re.DOTALL,
    )

    # Then substitute variables
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


# ---------------------------------------------------------------------------
# Claude invocation
# ---------------------------------------------------------------------------


def invoke_claude(
    prompt: str,
    cwd: Path,
    timeout: int = 900,
    model: str | None = None,
) -> tuple[str, str, int]:
    """Invoke claude in print mode via stdin.

    Returns (stdout, stderr, returncode).
    Adapted from Phase 1a run_concept.py.
    """
    cmd = ["claude", "-p", "--dangerously-skip-permissions", "--verbose"]
    if model:
        cmd.extend(["--model", model])

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Timed out after {timeout}s", -1
    except FileNotFoundError:
        return "", "'claude' command not found — is Claude Code installed and on PATH?", -2


# ---------------------------------------------------------------------------
# Source file discovery
# ---------------------------------------------------------------------------


def find_sources(concept_id: str, research_dir: Path = RESEARCH_DIR) -> list[Path]:
    """Find all extracted source documents for a concept from Phase 1a.

    Scans all iter-*/sources/ directories for .md files.
    Returns sorted list of absolute paths.
    """
    concept_dir = research_dir / concept_id
    if not concept_dir.exists():
        return []

    sources = []
    for iter_dir in sorted(concept_dir.glob("iter-*")):
        sources_dir = iter_dir / "sources"
        if sources_dir.exists():
            sources.extend(sorted(sources_dir.glob("*.md")))
    return sources


def get_dossier_path(concept_id: str, research_dir: Path = RESEARCH_DIR) -> Path | None:
    """Get path to Phase 1a dossier for a concept. Returns None if not found."""
    path = research_dir / concept_id / "dossier.md"
    return path if path.exists() else None


def format_source_list(sources: list[Path]) -> str:
    """Format source file list for inclusion in prompts.

    Shows each source with its file size for context.
    """
    if not sources:
        return "(no extracted source documents found)"

    lines = []
    for src in sources:
        size_kb = src.stat().st_size / 1024
        lines.append(f"- `{src}` ({size_kb:.0f} KB)")
    return "\n".join(lines)


def parse_proposed_actions(review_path: Path) -> list[dict]:
    """Parse Proposed Actions from review.md.

    Returns list of dicts with keys: id, description, category, severity,
    location, finding, proposed_fix, decision, user_notes.
    """
    text = review_path.read_text(encoding="utf-8")
    actions = []
    # Split on ### PA-N: headers
    pa_pattern = re.compile(r"^### (PA-\d+):\s*(.+)$", re.MULTILINE)

    matches = list(pa_pattern.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        action = {
            "id": m.group(1),
            "description": m.group(2).strip(),
        }

        # Extract fields from **Key:** Value pattern
        for field_key, dict_key in [
            ("Category", "category"),
            ("Severity", "severity"),
            ("Location", "location"),
            ("Finding", "finding"),
            ("Proposed Fix", "proposed_fix"),
            ("Decision", "decision"),
            ("User Notes", "user_notes"),
        ]:
            field_pattern = re.compile(
                rf"^\-\s*\*\*{re.escape(field_key)}:\*\*\s*(.+)$",
                re.MULTILINE,
            )
            field_match = field_pattern.search(block)
            if field_match:
                val = field_match.group(1).strip()
                # Strip italic placeholder markers
                if val.startswith("_[") and val.endswith("]_"):
                    val = ""  # unfilled placeholder
                elif val.startswith("_") and val.endswith("_"):
                    val = ""
                action[dict_key] = val
            else:
                action[dict_key] = ""

        actions.append(action)

    return actions


def find_approved(analyses_dir: Path = ANALYSES_DIR) -> list[Path]:
    """Find all approved analysis.md files (the reuse pool).

    Returns sorted list of absolute paths to analysis.md files
    where frontmatter Status == approved.
    """
    approved = []
    if not analyses_dir.exists():
        return approved

    for analysis_path in sorted(analyses_dir.glob("*/analysis.md")):
        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            approved.append(analysis_path)
    return approved


def find_exemplars(handwritten_dir: Path = HANDWRITTEN_DIR) -> list[Path]:
    """Find all handwritten exemplar analysis files.

    Returns sorted list of absolute paths.
    """
    if not handwritten_dir.exists():
        return []
    return sorted(handwritten_dir.glob("*.md"))


def format_path_list(paths: list[Path], empty_msg: str = "(none)") -> str:
    """Format a list of paths as markdown bullet points."""
    if not paths:
        return empty_msg
    return "\n".join(f"- `{p}`" for p in paths)


# ---------------------------------------------------------------------------
# Subcommand: list
# ---------------------------------------------------------------------------


def cmd_list(concepts: list[dict], _args: argparse.Namespace) -> None:
    """Print all concepts with IDs."""
    print(f"{'ID':<45} {'Concept Name':<40} {'Company':<30} {'Family'}")
    print("-" * 145)
    for c in concepts:
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {c.get('Company', ''):<30} {c.get('Confinement Family', '')}")
    print(f"\n{len(concepts)} concepts total")


# ---------------------------------------------------------------------------
# Subcommand: status
# ---------------------------------------------------------------------------


def cmd_status(concepts: list[dict], args: argparse.Namespace) -> None:
    """Print per-concept status table."""
    # Resolve which concepts to show (default: all)
    if args.concepts or args.family:
        targets = resolve_concepts(
            args.concepts, concepts, family=args.family,
        )
    else:
        targets = concepts

    # State symbols for compact display
    state_symbols = {
        "not-started": "  -",
        "gap-checked": "  G",
        "drafted":     "  D",
        "model-setup": "  M",
        "reviewed":    "  R",
        "synthesized": "  S",
        "approved":    "  A",
    }

    print(f"{'ID':<45} {'Concept Name':<40} {'State'}")
    print("-" * 95)

    counts = {s: 0 for s in state_symbols}
    for c in targets:
        state = get_concept_state(c["_id"])
        counts[state] = counts.get(state, 0) + 1
        sym = state_symbols.get(state, "  ?")
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {sym}")

    print(f"\n{len(targets)} concepts: "
          f"{counts['approved']} approved, {counts['synthesized']} synthesized, "
          f"{counts['reviewed']} reviewed, {counts['model-setup']} model-setup, "
          f"{counts['drafted']} drafted, {counts['gap-checked']} gap-checked, "
          f"{counts['not-started']} not-started")
    print("\nLegend: A=approved  S=synthesized  R=reviewed  M=model-setup  "
          "D=drafted  G=gap-checked  -=not-started")


# ---------------------------------------------------------------------------
# Stub subcommands (implemented in later phases)
# ---------------------------------------------------------------------------


def cmd_gap_check(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 1: Gap assessment."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="gap-checked",
    )
    if not targets:
        print("No concepts to gap-check.")
        return

    template_text = (TEMPLATES_DIR / "gap_check.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        gap_report_path = out_dir / "gap_report.md"

        # Skip if already done (unless --force)
        if gap_report_path.exists() and not args.force:
            print(f"  skip {cid} (gap_report.md exists, use --force to re-run)")
            continue

        # Gather inputs (use _research_id for Phase 1a lookup)
        rid = c["_research_id"]
        dossier_path = get_dossier_path(rid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(rid)
        source_list_text = format_source_list(sources)

        # Fill template
        prompt = fill_template(template_text, {
            "concept_id": cid,
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "dossier_path": str(dossier_path),
            "source_file_list": source_list_text,
            "brief_path": str(BRIEF_PATH),
            "schema_path": str(SCHEMA_PATH),
        })

        # Save prompt
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "gap_check_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Live invocation
        print(f"  gap-check {cid} ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            continue

        # Save output
        gap_report_path.write_text(stdout, encoding="utf-8")
        print(f" done ({elapsed:.0f}s, {len(stdout)} chars)")


def cmd_analyze(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 2: D1+ analysis (sequential — each concept re-scans reuse pool)."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="approved",
    )
    if not targets:
        print("No concepts to analyze.")
        return

    template_text = (TEMPLATES_DIR / "analysis.md").read_text(encoding="utf-8")
    exemplars = find_exemplars()
    output_template_path = TEMPLATES_DIR / "output_template.md"

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"

        # Skip if already done (unless --force)
        if analysis_path.exists() and not args.force:
            print(f"  skip {cid} (analysis.md exists, use --force to re-run)")
            continue

        # Gather inputs (use _research_id for Phase 1a lookup)
        rid = c["_research_id"]
        dossier_path = get_dossier_path(rid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(rid)

        # Re-scan approved pool before each concept (mid-batch approvals picked up)
        approved = find_approved()

        # Claude writes body to a temp file; script assembles final analysis.md
        body_path = out_dir / "analysis_body.md"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Fill template
        prompt = fill_template(template_text, {
            "concept_id": cid,
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "dossier_path": str(dossier_path),
            "source_paths": format_source_list(sources),
            "brief_path": str(BRIEF_PATH),
            "schema_path": str(SCHEMA_PATH),
            "exemplar_paths": format_path_list(exemplars, "(no exemplars found)"),
            "approved_analyses": format_path_list(approved, "No approved prior analyses available."),
            "output_template_path": str(output_template_path),
            "output_path": str(body_path),
            "analysis_path": str(analysis_path),
        })

        # Save prompt
        prompt_path = out_dir / "analysis_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Pre-write analysis.md with frontmatter before invoking Claude.
        # Claude may edit the Reuses field via Edit tool during analysis.
        analysis_path.write_text(make_frontmatter(c), encoding="utf-8")

        # Live invocation — Claude writes body to body_path via Write tool
        print(f"  analyze {cid} ...", end="", flush=True)
        t0 = time.time()
        _stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            analysis_path.unlink(missing_ok=True)
            continue

        # Verify Claude wrote the body file
        if not body_path.exists():
            print(f" FAILED ({elapsed:.0f}s) — Claude did not write {body_path}")
            analysis_path.unlink(missing_ok=True)
            continue

        # Assemble: read back frontmatter (Claude may have updated Reuses) + body
        fm_raw = analysis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
        body = body_path.read_text(encoding="utf-8")
        analysis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
        body_path.unlink()

        # Verify assembly
        if not analysis_path.read_text(encoding="utf-8").startswith("---"):
            print(f" WARNING ({elapsed:.0f}s): analysis.md doesn't start with ---")
            continue

        print(f" done ({elapsed:.0f}s, {len(body)} chars)")


def cmd_model_setup(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 3: Generate model setup script (1costingfe or free-form)."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="model-setup",
    )
    if not targets:
        print("No concepts to model-setup.")
        return

    costingfe_template = (TEMPLATES_DIR / "model_setup_costingfe.md").read_text(encoding="utf-8")
    freeform_template = (TEMPLATES_DIR / "model_setup_freeform.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        model_path = out_dir / "model_setup.py"
        analysis_path = out_dir / "analysis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        if model_path.exists() and not args.force:
            print(f"  skip {cid} (model_setup.py exists, use --force)")
            continue

        model_path_type = get_model_path(c)

        if model_path_type == "costingfe":
            mapping = get_costingfe_mapping(c)
            prompt = fill_template(costingfe_template, {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(analysis_path),
                "example_path": str(COSTINGFE_EXAMPLES_DIR / mapping["example"]),
                "defaults_path": str(COSTINGFE_DEFAULTS_DIR / mapping["defaults"]),
                "readme_path": str(COSTINGFE_README_PATH),
                "costing_constants_path": str(COSTINGFE_CONSTANTS_PATH),
                "costingfe_concept": mapping["concept"],
                "costingfe_fuel": FUEL_MAPPING.get(c.get("Fuel", "D-T"), "DT"),
                "mapping_notes": mapping.get("notes", ""),
                "output_path": str(model_path),
            })
            path_label = "1costingfe"
        else:
            prompt = fill_template(freeform_template, {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(analysis_path),
                "costing_constants_path": str(COSTINGFE_CONSTANTS_PATH),
                "output_path": str(model_path),
            })
            path_label = "free-form"

        # Save prompt
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "model_setup_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid} ({path_label}): prompt saved to {prompt_path}")
            continue

        # Live invocation
        print(f"  model-setup {cid} ({path_label}) ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            continue

        # Verify Claude wrote the model file
        if not model_path.exists():
            print(f" FAILED ({elapsed:.0f}s) — Claude did not write {model_path}")
            continue

        size = model_path.stat().st_size
        print(f" done ({elapsed:.0f}s, {size} bytes)")
        print(f"    hint: uv run python {model_path} | tee {out_dir / 'model_output.txt'}")


def cmd_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 4: Structured review with proposed actions."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="reviewed",
    )
    if not targets:
        print("No concepts to review.")
        return

    template_text = (TEMPLATES_DIR / "review.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        rid = c["_research_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        review_path = out_dir / "review.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        if not model_path.exists():
            print(f"  warn {cid}: no model_setup.py — reviewing analysis only")

        if review_path.exists() and not args.force:
            print(f"  skip {cid} (review.md exists, use --force to re-run)")
            continue

        # Determine iteration number (always increment, even with --force)
        fm = parse_frontmatter(analysis_path)
        prev_iterations = fm.get("Review-Iterations", "0")
        iteration = int(prev_iterations) + 1

        sources = find_sources(rid)

        prompt = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "source_paths": format_source_list(sources),
            "source_count": str(len(sources)),
            "output_path": str(review_path),
            "iteration": str(iteration),
            "date": date.today().isoformat(),
        })

        # Save prompt
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "review_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Live invocation
        print(f"  review {cid} (iteration {iteration}) ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            continue

        # Verify Claude wrote the review file
        if not review_path.exists():
            # Claude may have printed output instead of writing to file
            if stdout.strip():
                review_path.write_text(stdout, encoding="utf-8")
            else:
                print(f" FAILED ({elapsed:.0f}s) — no review output")
                continue

        review_text = review_path.read_text(encoding="utf-8")

        # Determine review status from output
        review_status = "has-actions"
        if re.search(r"\*\*Overall:\*\*\s*CLEAN", review_text, re.MULTILINE):
            review_status = "clean"

        # Update analysis frontmatter
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Review-Iterations", str(iteration))
        text = update_frontmatter_field(text, "Last-Review", date.today().isoformat())
        text = update_frontmatter_field(text, "Review-Status", review_status)
        analysis_path.write_text(text, encoding="utf-8")

        size = len(review_text)
        print(f" done ({elapsed:.0f}s, {size} chars) — {review_status}")


def cmd_address_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Apply user decisions from review report."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts to address-review.")
        return

    template_text = (TEMPLATES_DIR / "address_review.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        review_path = out_dir / "review.md"
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        log_path = out_dir / "address_log.md"

        if not review_path.exists():
            print(f"  skip {cid} (no review.md — run review first)")
            continue

        # Parse proposed actions
        actions = parse_proposed_actions(review_path)
        actionable = [
            a for a in actions
            if a.get("decision") and a["decision"] not in ("", "_")
        ]

        if not actionable:
            print(f"  skip {cid} (no decisions filled in review.md — "
                  f"edit review.md and fill in Decision fields)")
            continue

        # Build decisions block for prompt
        decisions_lines = []
        for a in actionable:
            decisions_lines.append(f"### {a['id']}: {a['description']}")
            decisions_lines.append(f"- **Decision:** {a['decision']}")
            decisions_lines.append(f"- **User Notes:** {a.get('user_notes', '')}")
            decisions_lines.append(f"- **Location:** {a['location']}")
            decisions_lines.append(f"- **Proposed Fix:** {a['proposed_fix']}")
            decisions_lines.append("")

        fm = parse_frontmatter(analysis_path)
        iteration = fm.get("Review-Iterations", "1")

        prompt = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "decisions_block": "\n".join(decisions_lines),
            "log_path": str(log_path),
            "iteration": iteration,
            "date": date.today().isoformat(),
        })

        # Save prompt
        prompt_path = out_dir / "address_review_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path} "
                  f"({len(actionable)} actions)")
            continue

        # Live invocation — Claude uses Edit tool to modify analysis.md / model_setup.py
        print(f"  address-review {cid} ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            continue

        # Update frontmatter: Review-Status → addressed
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Review-Status", "addressed")
        analysis_path.write_text(text, encoding="utf-8")

        print(f" done ({elapsed:.0f}s, {len(actionable)} actions processed)")


def cmd_synthesize(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 5: Generate editorial synthesis."""
    print("synthesize: not yet implemented")


def cmd_approve(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 6: Approve a reviewed analysis."""
    targets = resolve_concepts(args.concepts, concepts)
    if not targets:
        print("No concepts to approve.")
        return

    today = date.today().isoformat()

    for c in targets:
        cid = c["_id"]
        analysis_path = ANALYSES_DIR / cid / "analysis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md found — run analyze first)")
            continue

        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            print(f"  skip {cid} (already approved on {fm.get('Approved-Date', '?')})")
            continue

        # Update frontmatter: Status → approved, set Approved-Date
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Status", "approved")
        text = update_frontmatter_field(text, "Approved-Date", today)
        analysis_path.write_text(text, encoding="utf-8")
        print(f"  approved {cid}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_analysis.py",
        description="Automated concept analysis pipeline for Fusion TEA",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- list --
    sub.add_parser("list", help="List all concepts with IDs")

    # -- status --
    p_status = sub.add_parser("status", help="Show per-concept state table")
    p_status.add_argument("concepts", nargs="*", default=[], help="Concept IDs to show (default: all)")
    p_status.add_argument("--family", help="Filter by confinement family (MFE, IFE, MIF, Non-Standard)")

    # -- gap-check --
    p_gap = sub.add_parser("gap-check", help="Run Stage 1 gap assessment")
    p_gap.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_gap.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_gap.add_argument("--family", help="Filter by confinement family")
    p_gap.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_gap.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_gap.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_gap.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- analyze --
    p_analyze = sub.add_parser("analyze", help="Run Stage 2 D1+ analysis")
    p_analyze.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_analyze.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_analyze.add_argument("--family", help="Filter by confinement family")
    p_analyze.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_analyze.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_analyze.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_analyze.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- model-setup --
    p_ms = sub.add_parser("model-setup", help="Generate 1costingfe model setup script")
    p_ms.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_ms.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_ms.add_argument("--family", help="Filter by confinement family")
    p_ms.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_ms.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_ms.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_ms.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- review --
    p_rev = sub.add_parser("review", help="Structured review with proposed actions")
    p_rev.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_rev.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_rev.add_argument("--family", help="Filter by confinement family")
    p_rev.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_rev.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_rev.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_rev.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- address-review --
    p_addr = sub.add_parser("address-review", help="Apply user decisions from review")
    p_addr.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_addr.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_addr.add_argument("--family", help="Filter by confinement family")
    p_addr.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_addr.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_addr.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")

    # -- synthesize --
    p_syn = sub.add_parser("synthesize", help="Generate editorial synthesis")
    p_syn.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_syn.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_syn.add_argument("--family", help="Filter by confinement family")
    p_syn.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_syn.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_syn.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_syn.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- approve --
    p_approve = sub.add_parser("approve", help="Approve a reviewed analysis")
    p_approve.add_argument("concepts", nargs="+", help="Concept IDs to approve")
    p_approve.add_argument("--force", action="store_true", help="Approve even without synthesis")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    table = load_table()

    dispatch = {
        "list": cmd_list,
        "status": cmd_status,
        "gap-check": cmd_gap_check,
        "analyze": cmd_analyze,
        "model-setup": cmd_model_setup,
        "review": cmd_review,
        "address-review": cmd_address_review,
        "synthesize": cmd_synthesize,
        "approve": cmd_approve,
    }

    handler = dispatch[args.command]
    handler(table, args)


if __name__ == "__main__":
    main()
