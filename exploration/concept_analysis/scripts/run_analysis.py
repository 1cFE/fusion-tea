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

    Returns: 'not-started' | 'gap-checked' | 'drafted' | 'approved'
    """
    analysis_path = analyses_dir / concept_id / "analysis.md"
    gap_path = analyses_dir / concept_id / "gap_report.md"

    if analysis_path.exists():
        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            return "approved"
        return "drafted"
    if gap_path.exists():
        return "gap-checked"
    return "not-started"


# ---------------------------------------------------------------------------
# Template engine
# ---------------------------------------------------------------------------


def fill_template(template_text: str, replacements: dict[str, str]) -> str:
    """Simple {{variable}} substitution in template text."""
    result = template_text
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
        "drafted": "  D",
        "approved": "  A",
    }

    print(f"{'ID':<45} {'Concept Name':<40} {'State'}")
    print("-" * 95)

    counts = {"not-started": 0, "gap-checked": 0, "drafted": 0, "approved": 0}
    for c in targets:
        state = get_concept_state(c["_id"])
        counts[state] += 1
        sym = state_symbols.get(state, "  ?")
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {sym}")

    print(f"\n{len(targets)} concepts: "
          f"{counts['approved']} approved, {counts['drafted']} drafted, "
          f"{counts['gap-checked']} gap-checked, {counts['not-started']} not-started")
    print("\nLegend: A=approved  D=drafted  G=gap-checked  -=not-started")


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

        # Gather inputs
        dossier_path = get_dossier_path(cid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(cid)
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

        # Gather inputs
        dossier_path = get_dossier_path(cid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(cid)

        # Re-scan approved pool before each concept (mid-batch approvals picked up)
        approved = find_approved()

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
        })

        # Save prompt
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "analysis_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Live invocation
        print(f"  analyze {cid} ...", end="", flush=True)
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
        analysis_path.write_text(stdout, encoding="utf-8")
        print(f" done ({elapsed:.0f}s, {len(stdout)} chars)")


def cmd_approve(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 4: Approve a reviewed analysis."""
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

    # -- approve --
    p_approve = sub.add_parser("approve", help="Approve a reviewed analysis")
    p_approve.add_argument("concepts", nargs="+", help="Concept IDs to approve")

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
        "approve": cmd_approve,
    }

    handler = dispatch[args.command]
    handler(table, args)


if __name__ == "__main__":
    main()
