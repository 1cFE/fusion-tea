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
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all 01 02 03
"""

import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from datetime import date, datetime
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
MEMORY_DIR = CONCEPT_ANALYSIS_DIR / "memory"

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

# Extraction output filename (matches agentic-mbse convention)
EXTRACT_OUTPUT = "output.md"


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

    Appends '*' suffix if downstream artifacts are stale.

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
            state = "approved"
        elif synthesis_path.exists():
            state = "synthesized"
        elif fm.get("Review-Status", "") in ("addressed", "clean"):
            state = "reviewed"
        elif model_path.exists():
            state = "model-setup"
        else:
            state = "drafted"

        # Check for staleness in downstream artifacts
        has_stale = False
        for artifact in ["review.md", "synthesis.md"]:
            artifact_path = analyses_dir / concept_id / artifact
            if artifact_path.exists():
                afm = parse_frontmatter(artifact_path)
                if afm.get("Stale") == "true":
                    has_stale = True
        if not has_stale and model_path.exists():
            first_line = model_path.read_text(encoding="utf-8").split("\n", 1)[0]
            if "# STALE:" in first_line:
                has_stale = True

        return state + ("*" if has_stale else "")

    if gap_path.exists():
        return "gap-checked"
    return "not-started"


def propagate_staleness(concept_id: str, reason: str,
                         analyses_dir: Path = ANALYSES_DIR) -> list[str]:
    """Mark downstream artifacts as stale when analysis.md changes.

    Returns list of files marked stale.
    """
    out_dir = analyses_dir / concept_id
    stale_files = []

    downstream = [
        out_dir / "model_setup.py",
        out_dir / "review.md",
        out_dir / "synthesis.md",
    ]

    for path in downstream:
        if not path.exists():
            continue

        if path.suffix == ".py":
            text = path.read_text(encoding="utf-8")
            if "# STALE:" not in text:
                text = f"# STALE: {reason}\n" + text
                path.write_text(text, encoding="utf-8")
            stale_files.append(path.name)
        else:
            text = path.read_text(encoding="utf-8")
            if text.startswith("---"):
                if "Stale: true" not in text:
                    text = update_frontmatter_field(text, "Stale", "true")
                    text = update_frontmatter_field(text, "Stale-Reason", reason)
                    path.write_text(text, encoding="utf-8")
                stale_files.append(path.name)

    return stale_files


def _has_downstream_artifacts(out_dir: Path) -> bool:
    """Check if downstream artifacts exist (for staleness on --force)."""
    return any((out_dir / f).exists()
               for f in ["model_setup.py", "review.md", "synthesis.md"])


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


def fill_template(template_text: str, replacements: dict[str, str],
                  templates_dir: Path = TEMPLATES_DIR) -> str:
    """{{variable}} substitution with {{#if var}}...{{/if}} conditionals
    and {{@path}} config file inclusion."""
    result = template_text

    # Process file inclusions first: {{@config/analysis_goals.md}}
    def replace_inclusion(m):
        rel_path = m.group(1)
        file_path = templates_dir / rel_path
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return f"[CONFIG FILE NOT FOUND: {rel_path}]"

    result = re.sub(r"\{\{@([^}]+)\}\}", replace_inclusion, result)

    # Process conditionals
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


def run_model(model_path: Path, output_path: Path, timeout: int = 120) -> tuple[bool, str]:
    """Run a model_setup.py script, save output to model_output.txt, sanity-check results.

    Returns (success, message). On success, message is the stdout. On failure, message
    is the error description.
    """
    model_path = model_path.resolve()
    if not model_path.exists():
        return False, f"model script not found: {model_path}"

    try:
        result = subprocess.run(
            ["uv", "run", "python", str(model_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(model_path.parent),
        )
    except subprocess.TimeoutExpired:
        return False, f"model timed out after {timeout}s"
    except FileNotFoundError:
        return False, "'uv' command not found — is uv installed and on PATH?"

    if result.returncode != 0:
        stderr_snippet = result.stderr.strip()[:300] if result.stderr else "(no stderr)"
        return False, f"model failed (rc={result.returncode}): {stderr_snippet}"

    stdout = result.stdout
    if not stdout.strip():
        return False, "model produced no output"

    if "lcoe" not in stdout.lower():
        return False, "model output missing LCOE — may be incomplete or broken"

    output_path.write_text(stdout, encoding="utf-8")
    return True, stdout


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


# ---------------------------------------------------------------------------
# Source addition helpers
# ---------------------------------------------------------------------------


def _slugify_text(text: str, max_len: int = 60) -> str:
    """Slugify text into a hyphenated lowercase string."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) <= max_len:
        return slug
    truncated = slug[:max_len]
    last_sep = truncated.rfind("-")
    return truncated[:last_sep] if last_sep > max_len // 2 else truncated


def _slugify_url(url: str, max_len: int = 60) -> str:
    """Slugify a URL into a descriptive hyphenated name."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    # Use domain + path for descriptive names
    domain = parsed.netloc.replace("www.", "").split(".")[0]  # e.g., "arxiv", "realta"
    path = parsed.path.rstrip("/")
    # Strip common prefixes
    for prefix in ("/abs/", "/pdf/", "/html/", "/article/", "/papers/"):
        if path.startswith(prefix):
            path = path[len(prefix) :]
            break
    # Strip file extensions
    path = re.sub(r"\.(pdf|html|htm)$", "", path)
    # Combine domain + meaningful path
    combined = f"{domain}-{path}" if path else domain
    return _slugify_text(combined, max_len)


def slugify_source(input_str: str, max_len: int = 60) -> str:
    """Derive a hyphenated source name from a file path or URL."""
    if input_str.startswith(("http://", "https://")):
        return _slugify_url(input_str, max_len)
    # Local file: use stem
    name = Path(input_str).stem
    return _slugify_text(name, max_len)


def flatten_companion_dir(companion_dir: Path) -> None:
    """Flatten nested extraction subdirectory if present.

    PDF extraction via agentic-mbse creates a nested subdir named after the
    input file. This moves its contents up one level and removes the empty
    nested dir.
    """
    subdirs = [d for d in companion_dir.iterdir() if d.is_dir()]
    candidates = [d for d in subdirs if (d / EXTRACT_OUTPUT).exists()]
    if len(candidates) != 1:
        return  # already flat or ambiguous
    nested = candidates[0]
    for item in nested.iterdir():
        dest = companion_dir / item.name
        if item.is_file():
            item.rename(dest)
        elif not dest.exists():
            item.rename(dest)
    if not any(nested.iterdir()):
        nested.rmdir()


def find_latest_sources_dir(
    concept_id: str, research_dir: Path = RESEARCH_DIR
) -> Path:
    """Find the latest iter-NN/sources/ dir, or create iter-01/sources/."""
    concept_dir = research_dir / concept_id
    iter_dirs = sorted(concept_dir.glob("iter-*"))
    if iter_dirs:
        sources_dir = iter_dirs[-1] / "sources"
        sources_dir.mkdir(exist_ok=True)
        return sources_dir
    # No iterations exist — create iter-01
    sources_dir = concept_dir / "iter-01" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    return sources_dir


def check_duplicate_source(
    concept_id: str, name: str, research_dir: Path = RESEARCH_DIR
) -> Path | None:
    """Check if a source with this name already exists in any iteration."""
    concept_dir = research_dir / concept_id
    for iter_dir in concept_dir.glob("iter-*"):
        candidate = iter_dir / "sources" / f"{name}.md"
        if candidate.exists():
            return candidate
    return None


def resolve_source_names(
    concept_id: str, names: list[str], research_dir: Path = RESEARCH_DIR
) -> list[Path]:
    """Resolve short source names to full paths under the concept."""
    concept_dir = research_dir / concept_id
    resolved = []
    for name in names:
        # Append .md if not present
        fname = name if name.endswith(".md") else f"{name}.md"
        matches = list(concept_dir.glob(f"iter-*/sources/{fname}"))
        if not matches:
            print(
                f"  error: source '{name}' not found under {concept_dir}/iter-*/sources/"
            )
            sys.exit(1)
        if len(matches) > 1:
            print(
                f"  error: source '{name}' found in multiple iterations: {matches}"
            )
            sys.exit(1)
        resolved.append(matches[0])
    return resolved


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


def find_approved_syntheses(analyses_dir: Path = ANALYSES_DIR) -> list[Path]:
    """Find synthesis.md files from approved concepts for cross-concept context."""
    results = []
    if not analyses_dir.exists():
        return results

    for analysis_path in sorted(analyses_dir.glob("*/analysis.md")):
        synthesis_path = analysis_path.parent / "synthesis.md"
        if synthesis_path.exists():
            fm = parse_frontmatter(analysis_path)
            if fm.get("Status") == "approved":
                results.append(synthesis_path)
    return results


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
# Cross-concept memory
# ---------------------------------------------------------------------------

# Regex for metadata line: "Date: 2026-03-29 | Concepts: 09, IFE, all"
_MEMORY_META_RE = re.compile(
    r"^Date:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Concepts:\s*(.+)$", re.MULTILINE
)


def load_relevant_memories(
    concept_id: str, memory_dir: Path, family: str = "",
) -> str:
    """Load memory entries relevant to a concept.

    Args:
        concept_id: Full concept ID, e.g. "09-laser-ife". Short ID
            extracted as the leading numeric segment.
        memory_dir: Path to the memory directory.
        family: Confinement family tag, e.g. "IFE". Empty string if unknown.

    Returns:
        Matched entries as a markdown string, or "" if none found
        or memory dir doesn't exist.
    """
    if not memory_dir.is_dir():
        return ""

    md_files = sorted(memory_dir.glob("*.md"))
    if not md_files:
        return ""

    # Extract short ID: "09" from "09-laser-ife"
    short_id = concept_id.split("-")[0]

    # Build match set, dropping empty strings
    match_set = {short_id, family.upper(), "all"} - {""}

    matched: list[str] = []
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        # Split on H2 boundaries — everything from one "## " to the next (or EOF)
        entries = re.split(r"(?=^## )", content, flags=re.MULTILINE)
        for entry in entries:
            entry = entry.strip()
            if not entry.startswith("## "):
                continue
            m = _MEMORY_META_RE.search(entry)
            if not m:
                continue
            tags = {t.strip() for t in m.group(1).split(",")}
            if tags & match_set:
                matched.append(entry)

    return "\n\n".join(matched)


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
    stale_count = 0
    for c in targets:
        state = get_concept_state(c["_id"])
        base_state = state.rstrip("*")
        counts[base_state] = counts.get(base_state, 0) + 1
        sym = state_symbols.get(base_state, "  ?")
        if state.endswith("*"):
            sym = sym + "*"
            stale_count += 1
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {sym}")

    print(f"\n{len(targets)} concepts: "
          f"{counts['approved']} approved, {counts['synthesized']} synthesized, "
          f"{counts['reviewed']} reviewed, {counts['model-setup']} model-setup, "
          f"{counts['drafted']} drafted, {counts['gap-checked']} gap-checked, "
          f"{counts['not-started']} not-started"
          + (f", {stale_count} stale" if stale_count else ""))
    print("\nLegend: A=approved  S=synthesized  R=reviewed  M=model-setup  "
          "D=drafted  G=gap-checked  -=not-started  *=stale downstream")


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
    """Stage 2: D1+ analysis with iterative assessment loop."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="approved",
    )
    if not targets:
        print("No concepts to analyze.")
        return

    # Validate --feedback constraints
    feedback = getattr(args, "feedback", None)
    if feedback:
        if args.force:
            print("Error: --feedback and --force are mutually exclusive.")
            print("  --feedback applies changes to existing analysis.md")
            print("  --force re-creates analysis.md from scratch")
            sys.exit(1)
        if not feedback.is_file():
            print(f"Error: feedback file not found: {feedback}")
            sys.exit(1)
        if len(targets) > 1:
            print("Error: --feedback can only be used with a single concept")
            sys.exit(1)

    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")
    assessment_template = (TEMPLATES_DIR / "assessment.md").read_text(encoding="utf-8")
    exemplars = find_exemplars()
    output_template_path = TEMPLATES_DIR / "output_template.md"
    max_passes = args.max_passes

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        had_existing_downstream = _has_downstream_artifacts(out_dir)

        # For feedback mode, analysis.md must exist
        if feedback:
            if not analysis_path.exists():
                print(f"  skip {cid} (no analysis.md — --feedback requires existing analysis)")
                continue
        # Skip if already done (unless --force)
        elif analysis_path.exists() and not args.force:
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
        out_dir.mkdir(parents=True, exist_ok=True)

        # Load cross-concept memories relevant to this concept
        memory_context = load_relevant_memories(
            cid, MEMORY_DIR, family=c.get("Confinement Family", ""),
        )

        # Common template vars shared across all modes
        common_vars = {
            "concept_id": cid,
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "dossier_path": str(dossier_path),
            "source_paths": format_source_list(sources),
            "brief_path": str(BRIEF_PATH),
            "schema_path": str(SCHEMA_PATH),
            "exemplar_paths": format_path_list(exemplars, "(no exemplars found)"),
            "approved_analyses": format_path_list(
                approved, "No approved prior analyses available."),
            "output_template_path": str(output_template_path),
            "analysis_path": str(analysis_path),
            "memory_context": memory_context,
        }

        # === FEEDBACK MODE: apply external feedback file ===
        if feedback:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt = fill_template(analysis_template, {
                **common_vars,
                "output_path": "",  # not used in feedback mode
                "cold_start": "",
                "feedback_pass": "true",
                "feedback_path": str(feedback),
                "self_advance": "",
            })

            # Save prompt for audit trail
            prompt_path = out_dir / f"feedback_apply_prompt_{ts}.md"
            prompt_path.write_text(prompt, encoding="utf-8")

            if args.dry_run:
                print(f"  dry-run {cid}: feedback prompt saved to {prompt_path}")
                continue

            print(f"  apply feedback {cid} ...", end="", flush=True)
            t0 = time.time()
            _stdout, stderr, rc = invoke_claude(
                prompt, cwd=CONCEPT_ANALYSIS_DIR,
                timeout=args.timeout, model=args.model,
            )
            elapsed = time.time() - t0

            if rc != 0:
                print(f" FAILED ({elapsed:.0f}s, rc={rc})")
                print(f"    stderr: {stderr[:500]}", file=sys.stderr)
                continue

            print(f" done ({elapsed:.0f}s)")

            # Propagate staleness
            stale = propagate_staleness(cid, "feedback-applied-from-change-requests")
            if stale:
                print(f"    stale: {', '.join(stale)}")

            # Archive consumed feedback file
            archive_name = f"change_requests_{ts}.md"
            archived = feedback.parent / archive_name
            feedback.rename(archived)
            print(f"    archived: {feedback.name} → {archive_name}")

            continue

        # === COLD START (analysis pass 1) ===
        body_path = out_dir / "analysis_body.md"
        prompt = fill_template(analysis_template, {
            **common_vars,
            "output_path": str(body_path),
            "cold_start": "true",
            "feedback_pass": "",
            "feedback_path": "",
            "self_advance": "",
        })

        prompt_path = out_dir / "analysis_prompt_iter_1.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Pre-write analysis.md with frontmatter before invoking Claude.
        # Claude may edit the Reuses field via Edit tool during analysis.
        analysis_path.write_text(make_frontmatter(c), encoding="utf-8")

        print(f"  analyze {cid} pass 1/{max_passes} ...", end="", flush=True)
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

        if not body_path.exists():
            print(f" FAILED ({elapsed:.0f}s) — Claude did not write {body_path}")
            analysis_path.unlink(missing_ok=True)
            continue

        # Assemble: read back frontmatter (Claude may have updated Reuses) + body
        fm_raw = analysis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
        body = body_path.read_text(encoding="utf-8")
        analysis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
        body_path.unlink()
        print(f" done ({elapsed:.0f}s, {len(body)} chars)")

        # Staleness: --force cold start rewrites analysis.md
        if args.force and had_existing_downstream:
            stale = propagate_staleness(cid, "analysis-rewritten-by-force")
            if stale:
                print(f"    stale: {', '.join(stale)}")

        # === ASSESSMENT LOOP ===
        # FR-23: --max-passes 1 skips assessment entirely
        if max_passes <= 1:
            continue

        converged = False
        for pass_num in range(1, max_passes + 1):
            # --- Assess the current analysis.md ---
            feedback_path = out_dir / f"feedback_iter_{pass_num}.md"
            assess_prompt = fill_template(assessment_template, {
                "concept_name": c["Concept Name"],
                "analysis_path": str(analysis_path),
                "feedback_path": str(feedback_path),
            })

            assess_prompt_path = out_dir / f"assessment_prompt_iter_{pass_num}.md"
            assess_prompt_path.write_text(assess_prompt, encoding="utf-8")

            print(f"  assess {cid} iter {pass_num} ...", end="", flush=True)
            t0 = time.time()
            _stdout, stderr, rc = invoke_claude(
                assess_prompt, cwd=CONCEPT_ANALYSIS_DIR,
                timeout=args.timeout, model=args.model,
            )
            elapsed = time.time() - t0

            if rc != 0:
                print(f" FAILED ({elapsed:.0f}s, rc={rc})")
                break

            if not feedback_path.exists():
                print(f" FAILED ({elapsed:.0f}s) — no feedback file")
                break

            # Parse convergence signal (anchor to start of line)
            feedback_text = feedback_path.read_text(encoding="utf-8")
            converged = bool(
                re.search(r"^VERDICT:\s*PASS", feedback_text, re.MULTILINE))
            finding_count = len(
                re.findall(r"^### F-\d+:", feedback_text, re.MULTILINE))

            if converged:
                print(f" PASS ({elapsed:.0f}s)")
                break

            print(f" {finding_count} findings ({elapsed:.0f}s)")

            # If this was the last allowed pass, no room for another analyze
            if pass_num >= max_passes:
                print(f"  warn: {cid} did not converge in {max_passes} passes "
                      f"(see feedback_iter_{pass_num}.md)")
                break

            # --- Feedback pass: analyze again ---
            next_analysis_num = pass_num + 1
            prompt = fill_template(analysis_template, {
                **common_vars,
                "output_path": "",  # not used in feedback mode
                "cold_start": "",
                "feedback_pass": "true",
                "feedback_path": str(feedback_path),
                "self_advance": "",
            })

            prompt_path = out_dir / f"analysis_prompt_iter_{next_analysis_num}.md"
            prompt_path.write_text(prompt, encoding="utf-8")

            print(f"  analyze {cid} pass {next_analysis_num}/{max_passes} ...",
                  end="", flush=True)
            t0 = time.time()
            _stdout, stderr, rc = invoke_claude(
                prompt, cwd=CONCEPT_ANALYSIS_DIR,
                timeout=args.timeout, model=args.model,
            )
            elapsed = time.time() - t0

            if rc != 0:
                print(f" FAILED ({elapsed:.0f}s, rc={rc})")
                break

            print(f" done ({elapsed:.0f}s)")

            # Staleness: feedback pass modified analysis.md
            stale = propagate_staleness(cid, "analysis-updated-by-feedback-loop")
            if stale:
                print(f"    stale: {', '.join(stale)}")


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

        # Run the model and capture output
        model_output_path = out_dir / "model_output.txt"
        print(f"    running model ...", end="", flush=True)
        ok, msg = run_model(model_path, model_output_path)
        if ok:
            lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
            lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
            print(f" ok{lcoe_str}")
        else:
            print(f" FAILED: {msg}")
            print(f"    hint: fix model_setup.py and run: uv run python {model_path}")


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

        # Re-run model if it exists (address-review may have modified model_setup.py)
        model_output_path = out_dir / "model_output.txt"
        if model_path.exists():
            print(f"    re-running model ...", end="", flush=True)
            ok, msg = run_model(model_path, model_output_path)
            if ok:
                lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                print(f" ok{lcoe_str}")
            else:
                print(f" FAILED: {msg}")
                print(f"    warn: model may be broken after review changes")

        # Update frontmatter: Review-Status → addressed
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Review-Status", "addressed")
        analysis_path.write_text(text, encoding="utf-8")

        print(f" done ({elapsed:.0f}s, {len(actionable)} actions processed)")


def cmd_synthesize(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 5: Generate editorial synthesis."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="synthesized",
    )
    if not targets:
        print("No concepts to synthesize.")
        return

    template_text = (TEMPLATES_DIR / "synthesis.md").read_text(encoding="utf-8")

    # Gather approved prior syntheses for cross-concept context
    prior_syntheses = find_approved_syntheses()

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        model_setup_path = out_dir / "model_setup.py"
        model_output_path = out_dir / "model_output.txt"
        synthesis_path = out_dir / "synthesis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        # Enforce ordering: must be reviewed
        fm = parse_frontmatter(analysis_path)
        review_status = fm.get("Review-Status", "")
        if review_status not in ("addressed", "clean"):
            print(f"  skip {cid} (Review-Status is '{review_status}'; "
                  f"run review and address-review first)")
            continue

        if synthesis_path.exists() and not args.force:
            print(f"  skip {cid} (synthesis.md exists, use --force to re-run)")
            continue

        # Ensure model output is fresh before synthesizing
        if model_setup_path.exists():
            need_run = False
            reason = ""
            if not model_output_path.exists():
                need_run = True
                reason = "model_output.txt missing"
            elif model_setup_path.stat().st_mtime > model_output_path.stat().st_mtime:
                need_run = True
                reason = "model_setup.py newer than model_output.txt"

            if need_run:
                print(f"    running model ({reason}) ...", end="", flush=True)
                ok, msg = run_model(model_setup_path, model_output_path)
                if ok:
                    lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                    lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                    print(f" ok{lcoe_str}")
                else:
                    print(f" FAILED: {msg}")
                    print(f"    warn: synthesizing without model output")

        # Format approved prior syntheses (exclude current concept)
        synth_list = [s for s in prior_syntheses if s.parent.name != cid]
        if synth_list:
            approved_syntheses = format_path_list(synth_list)
        else:
            approved_syntheses = "(none yet — this is among the first syntheses)"

        # Claude writes body to a temp file; script assembles final synthesis.md
        body_path = out_dir / "synthesis_body.md"

        prompt = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_setup_path) if model_setup_path.exists() else "",
            "model_output_path": str(model_output_path) if model_output_path.exists() else "",
            "approved_syntheses": approved_syntheses,
            "output_path": str(body_path),
        })

        # Save prompt
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "synthesis_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Pre-write synthesis.md with controlled frontmatter
        today = date.today().isoformat()
        synth_fm = (
            f"---\n"
            f"ID: {cid}\n"
            f"Concept: {c['Concept Name']}\n"
            f"Company: {c.get('Company', '')}\n"
            f"Type: synthesis\n"
            f"Status: draft\n"
            f"Created: {today}\n"
            f"---\n"
        )
        synthesis_path.write_text(synth_fm, encoding="utf-8")

        # Live invocation — Claude writes body to body_path via Write tool
        print(f"  synthesize {cid} ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            synthesis_path.unlink(missing_ok=True)
            continue

        # Verify Claude wrote the body file
        if not body_path.exists():
            if stdout.strip():
                body_path.write_text(stdout, encoding="utf-8")
            else:
                print(f" FAILED ({elapsed:.0f}s) — Claude did not write {body_path}")
                synthesis_path.unlink(missing_ok=True)
                continue

        # Assemble: frontmatter + body
        fm_raw = synthesis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
        body = body_path.read_text(encoding="utf-8")
        # Strip any frontmatter Claude may have added to the body
        if body.startswith("---"):
            fm_end = body.find("---", 3)
            if fm_end != -1:
                body = body[fm_end + 3:].lstrip("\n")
        synthesis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
        body_path.unlink()

        size = len(synthesis_path.read_text(encoding="utf-8"))
        print(f" done ({elapsed:.0f}s, {size} chars)")


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

        # Synthesis gate: warn and skip if no synthesis.md (unless --force)
        synthesis_path = ANALYSES_DIR / cid / "synthesis.md"
        if not synthesis_path.exists() and not args.force:
            print(f"  skip {cid} (no synthesis.md — run synthesize first, or use --force)")
            continue

        # Update frontmatter: Status → approved, set Approved-Date
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Status", "approved")
        text = update_frontmatter_field(text, "Approved-Date", today)
        analysis_path.write_text(text, encoding="utf-8")

        # Also update synthesis.md frontmatter if it exists
        if synthesis_path.exists():
            synth_text = synthesis_path.read_text(encoding="utf-8")
            synth_text = update_frontmatter_field(synth_text, "Status", "approved")
            synth_text = update_frontmatter_field(synth_text, "Approved-Date", today)
            synthesis_path.write_text(synth_text, encoding="utf-8")

        print(f"  approved {cid}")


# ---------------------------------------------------------------------------
# Composite: stage1-all (gap-check → analyze → model-setup → review)
# ---------------------------------------------------------------------------


def cmd_stage1_all(concepts: list[dict], args: argparse.Namespace) -> None:
    """Run gap-check → analyze → model-setup → review for specified concepts.

    Each stage's own skip logic handles prerequisites and existing outputs,
    so re-running is safe (picks up where it left off).
    """
    # Resolve once for summary display
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts to process.")
        return

    names = ", ".join(c["_num"] for c in targets)
    print(f"=== stage1-all: {len(targets)} concepts ({names}) ===")
    print("    Pipeline: gap-check → analyze → model-setup → review")

    stages = [
        ("Gap Check", cmd_gap_check),
        ("Analyze", cmd_analyze),
        ("Model Setup", cmd_model_setup),
        ("Review", cmd_review),
    ]

    for stage_name, handler in stages:
        print(f"\n--- {stage_name} ---")
        handler(concepts, args)

    # Final status summary
    print(f"\n=== stage1-all complete ===")
    for c in targets:
        state = get_concept_state(c["_id"])
        print(f"  {c['_num']} ({c['Concept Name']}): {state}")


# ---------------------------------------------------------------------------
# cmd_add_source — add a PDF or URL source to a concept
# ---------------------------------------------------------------------------


def cmd_add_source(concepts: list[dict], args: argparse.Namespace) -> None:
    """Add a PDF or URL source to a concept's sources directory."""
    # Resolve single concept
    matches = resolve_one(concepts, args.concept)
    if len(matches) == 0:
        print(f"  error: no concept matching '{args.concept}'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"  error: '{args.concept}' matches multiple concepts:")
        for c in matches:
            print(f"    {c['_num']} {c['Concept Name']}")
        sys.exit(1)
    concept = matches[0]
    research_id = concept["_research_id"]

    # Determine source name
    name = args.name if args.name else slugify_source(args.source)
    if not name:
        print("  error: could not derive source name — use --name to specify")
        sys.exit(1)

    print(f"  concept: {concept['_num']} ({concept['Concept Name']})")
    print(f"  source:  {args.source}")
    print(f"  name:    {name}")

    # Duplicate check
    existing = check_duplicate_source(research_id, name)
    if existing:
        if args.force:
            # NOTE: existing source may be in an older iter-NN; the new
            # extraction will land in the latest iter (find_latest_sources_dir).
            # This effectively moves the source forward, which is intentional.
            print(f"  force: removing existing source '{name}' at {existing.parent}")
            existing.unlink(missing_ok=True)
            companion = existing.parent / name
            if companion.is_dir():
                shutil.rmtree(companion)
        else:
            print(f"  error: source '{name}' already exists: {existing}")
            print("  use --force to re-extract")
            sys.exit(1)

    # Find placement
    sources_dir = find_latest_sources_dir(research_id)
    companion_dir = sources_dir / name
    symlink_path = sources_dir / f"{name}.md"

    print(f"  target:  {symlink_path}")

    if args.dry_run:
        print(f"\n  [dry-run] would create:")
        print(f"    companion dir: {companion_dir}/")
        print(f"    symlink:       {symlink_path} → {name}/{EXTRACT_OUTPUT}")
        print(f"    extraction:    uv run agentic-mbse extract {args.source} --save-source --output {companion_dir}/")
        return

    # Create companion dir
    companion_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Run extraction
        print(f"\n  extracting source...")
        cmd = [
            "uv", "run", "agentic-mbse", "extract", args.source,
            "--save-source", "--output", str(companion_dir),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode != 0:
            stderr_snippet = result.stderr.strip()[:500] if result.stderr else "(no stderr)"
            print(f"  error: extraction failed (rc={result.returncode})")
            print(f"  stderr: {stderr_snippet}")
            raise RuntimeError("extraction failed")

        # Flatten nested PDF subdirectory if present
        flatten_companion_dir(companion_dir)

        # Verify output.md exists
        output_path = companion_dir / EXTRACT_OUTPUT
        if not output_path.exists():
            print(f"  error: extraction completed but {EXTRACT_OUTPUT} not found in {companion_dir}")
            raise RuntimeError("output.md missing")

        # Create symlink (relative path)
        symlink_path.symlink_to(f"{name}/{EXTRACT_OUTPUT}")
        print(f"  created: {symlink_path}")
        print(f"  done — source '{name}' added successfully")

    except Exception as exc:
        # Clean up partial artifacts
        if companion_dir.exists():
            shutil.rmtree(companion_dir)
        if symlink_path.is_symlink():
            symlink_path.unlink()
        # RuntimeError messages already printed above; print others
        if not isinstance(exc, RuntimeError):
            print(f"  error: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# cmd_update_analysis — incrementally update analysis with new sources
# ---------------------------------------------------------------------------


def cmd_update_analysis(concepts: list[dict], args: argparse.Namespace) -> None:
    """Update analysis to incorporate new sources via pre-pass + feedback-pass."""
    # Resolve single concept
    matches = resolve_one(concepts, args.concept)
    if len(matches) == 0:
        print(f"  error: no concept matching '{args.concept}'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"  error: '{args.concept}' matches multiple concepts:")
        for c in matches:
            print(f"    {c['_num']} {c['Concept Name']}")
        sys.exit(1)
    concept = matches[0]
    cid = concept["_id"]
    rid = concept["_research_id"]

    print(f"  concept: {concept['_num']} ({concept['Concept Name']})")

    # Resolve source names to full paths
    new_source_paths = resolve_source_names(rid, args.sources)
    print(f"  new sources: {len(new_source_paths)}")
    for sp in new_source_paths:
        print(f"    {sp.name}")

    # Verify analysis.md exists
    out_dir = ANALYSES_DIR / cid
    analysis_path = out_dir / "analysis.md"
    if not analysis_path.exists():
        print(f"  error: no analysis.md for {cid} — run 'analyze' first")
        sys.exit(1)

    # Generate timestamp for filenames
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")

    # === Step 1: Source-Integration Pre-Pass ===
    print(f"\n  step 1: source-integration pre-pass...")

    integration_template = (TEMPLATES_DIR / "source_integration.md").read_text(
        encoding="utf-8"
    )
    feedback_path = out_dir / f"feedback_update_{ts}.md"

    new_source_list = format_source_list(new_source_paths)
    integration_prompt = fill_template(integration_template, {
        "concept_name": concept["Concept Name"],
        "analysis_path": str(analysis_path),
        "new_source_paths": new_source_list,
        "feedback_path": str(feedback_path),
    })

    # Save prompt for audit trail
    integration_prompt_path = out_dir / f"source_integration_prompt_{ts}.md"
    integration_prompt_path.write_text(integration_prompt, encoding="utf-8")
    print(f"  prompt: {integration_prompt_path}")

    # Invoke Claude for pre-pass
    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        integration_prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f"  pre-pass FAILED ({elapsed:.0f}s, rc={rc})")
        print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        sys.exit(1)

    if not feedback_path.exists():
        print(f"  pre-pass FAILED ({elapsed:.0f}s) — no feedback file created")
        sys.exit(1)

    feedback_text = feedback_path.read_text(encoding="utf-8")
    is_pass = bool(re.search(r"^VERDICT:\s*PASS", feedback_text, re.MULTILINE))
    finding_count = len(re.findall(r"^### F-\d+:", feedback_text, re.MULTILINE))

    if is_pass:
        print(f"  pre-pass: PASS ({elapsed:.0f}s) — no material additions needed")
        return

    print(f"  pre-pass: {finding_count} findings ({elapsed:.0f}s)")
    print(f"  feedback: {feedback_path}")

    if args.dry_run:
        print(f"\n  [dry-run] feedback content:")
        print(feedback_text)
        print(f"\n  [dry-run] would invoke feedback-pass on analysis.md — stopping here")
        return

    # === Step 2: Feedback Pass ===
    print(f"\n  step 2: feedback-pass (updating analysis.md)...")

    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")
    exemplars = find_exemplars()
    approved = find_approved()
    sources = find_sources(rid)
    dossier_path = get_dossier_path(rid)
    output_template_path = TEMPLATES_DIR / "output_template.md"

    common_vars = {
        "concept_id": cid,
        "concept_name": concept["Concept Name"],
        "company": concept.get("Company", ""),
        "dossier_path": str(dossier_path) if dossier_path else "",
        "source_paths": format_source_list(sources),
        "brief_path": str(BRIEF_PATH),
        "schema_path": str(SCHEMA_PATH),
        "exemplar_paths": format_path_list(exemplars, "(no exemplars found)"),
        "approved_analyses": format_path_list(
            approved, "No approved prior analyses available."),
        "output_template_path": str(output_template_path),
        "analysis_path": str(analysis_path),
    }

    feedback_prompt = fill_template(analysis_template, {
        **common_vars,
        "output_path": "",  # not used in feedback mode
        "cold_start": "",
        "feedback_pass": "true",
        "feedback_path": str(feedback_path),
        "self_advance": "",
    })

    # Save prompt for audit trail
    feedback_prompt_path = out_dir / f"update_analysis_prompt_{ts}.md"
    feedback_prompt_path.write_text(feedback_prompt, encoding="utf-8")

    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        feedback_prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f"  feedback-pass FAILED ({elapsed:.0f}s, rc={rc})")
        print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        sys.exit(1)

    print(f"  feedback-pass done ({elapsed:.0f}s)")

    # Propagate staleness
    stale = propagate_staleness(cid, f"analysis-updated-by-source-integration-{ts}")
    if stale:
        print(f"  stale: {', '.join(stale)}")

    print(f"\n  done — analysis updated with {finding_count} source integration(s)")


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
    p_analyze.add_argument("--max-passes", type=int, default=3,
                            help="Max analyze→assess iterations (default: 3; 1=no assessment)")
    p_analyze.add_argument("--feedback", type=Path, metavar="PATH",
                            help="Apply feedback file to existing analysis (skips cold-start)")

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

    # -- stage1-all --
    p_s1 = sub.add_parser(
        "stage1-all",
        help="Run full pipeline through review: gap-check → analyze → model-setup → review",
    )
    p_s1.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_s1.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_s1.add_argument("--family", help="Filter by confinement family")
    p_s1.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_s1.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_s1.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_s1.add_argument("--force", action="store_true", help="Re-run even if output exists")
    p_s1.add_argument("--max-passes", type=int, default=3,
                       help="Max analyze→assess iterations (default: 3; 1=no assessment)")

    # -- add-source --
    p_add = sub.add_parser("add-source", help="Add a PDF or URL source to a concept")
    p_add.add_argument("concept", help="Concept ID (single concept)")
    p_add.add_argument("source", help="PDF path or URL to extract")
    p_add.add_argument("--name", help="Override automatic source name")
    p_add.add_argument("--force", action="store_true",
                       help="Re-extract even if source name already exists")
    p_add.add_argument("--dry-run", action="store_true", help="Show what would be created")

    # -- update-analysis --
    p_upd = sub.add_parser("update-analysis",
                           help="Update analysis to incorporate new sources")
    p_upd.add_argument("concept", help="Concept ID (single concept)")
    p_upd.add_argument("--sources", nargs="+", required=True,
                       help="Source names to incorporate (e.g., sparc-icrf-heating-paper)")
    p_upd.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_upd.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout")
    p_upd.add_argument("--dry-run", action="store_true",
                       help="Run pre-pass and show feedback, but don't invoke analysis agent")

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
        "stage1-all": cmd_stage1_all,
        "add-source": cmd_add_source,
        "update-analysis": cmd_update_analysis,
    }

    handler = dispatch[args.command]
    handler(table, args)


if __name__ == "__main__":
    main()
