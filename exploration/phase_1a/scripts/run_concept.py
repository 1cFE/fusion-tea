#!/usr/bin/env python3
"""
Per-concept research orchestration for Phase 1a.

Runs N research+synthesis cycles for a single fusion concept.
Each cycle:
  1. Generates a research prompt from template + current state
  2. Invokes research agent (claude -p) → captures output.md
  3. Generates a synthesis prompt from template
  4. Invokes synthesis agent (claude -p) → updates dossier.md + changelog.md

Usage:
  uv run python exploration/phase_1a/scripts/run_concept.py \\
    --concept 01-hts-compact-tokamak --cycles 2

  uv run python exploration/phase_1a/scripts/run_concept.py \\
    --concept "CFS" --cycles 1 --dry-run
"""

import argparse
import csv
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths — all relative to the phase_1a directory
# ---------------------------------------------------------------------------

PHASE_1A_DIR = Path(__file__).resolve().parent.parent
RESEARCH_DIR = PHASE_1A_DIR / "research"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
RESEARCH_TEMPLATE_PATH = PHASE_1A_DIR / "prompt_templates" / "research.md"
SYNTHESIS_TEMPLATE_PATH = PHASE_1A_DIR / "prompt_templates" / "synthesis.md"
CSV_PATH = PHASE_1A_DIR.parent / "context" / "initial-fusion-concepts.csv"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(name: str) -> str:
    """Convert concept name to a directory-safe slug."""
    # Strip trailing parenthetical fuel annotations like (D-T), (p-B11)
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug


def read_file(path: Path) -> str:
    """Read file contents. Returns empty string if file does not exist."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------


def load_concepts(csv_path: Path) -> list[dict]:
    """Load concepts from CSV. Adds _index, _slug, _dir_name to each row."""
    concepts = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            row["_index"] = i
            row["_slug"] = slugify(row["Concept Name"])
            row["_dir_name"] = f"{i:02d}-{row['_slug']}"
            concepts.append(row)
    return concepts


def find_concept(concepts: list[dict], query: str) -> dict | None:
    """Find a concept by dir_name, slug, numeric index, or partial name."""
    # Exact dir_name
    for c in concepts:
        if c["_dir_name"] == query:
            return c
    # Exact slug
    for c in concepts:
        if c["_slug"] == query:
            return c
    # Numeric index
    try:
        idx = int(query)
        for c in concepts:
            if c["_index"] == idx:
                return c
    except ValueError:
        pass
    # Partial name or company (case-insensitive)
    q = query.lower()
    matches = [
        c
        for c in concepts
        if q in c["Concept Name"].lower() or q in c.get("Companies Pursuing", "").lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Ambiguous query '{query}' matched {len(matches)} concepts:", file=sys.stderr)
        for m in matches:
            print(f"  {m['_dir_name']}: {m['Concept Name']}", file=sys.stderr)
        return None
    return None


# ---------------------------------------------------------------------------
# Gap identification
# ---------------------------------------------------------------------------


def identify_gaps(dossier_text: str) -> str:
    """Parse the dossier markdown to find columns needing research."""
    if not dossier_text:
        return "All columns — this is the first iteration. No prior research exists."

    gaps = []

    # Split by ### headings to get per-column sections
    sections = re.split(r"^### ", dossier_text, flags=re.MULTILINE)
    for section in sections:
        if not section.strip():
            continue
        # Extract column name (first line of section)
        lines = section.strip().split("\n")
        col_name = lines[0].strip()

        section_text = "\n".join(lines[1:])

        # Check for TBD/Unknown values
        value_match = re.search(r"\*\*Value\*\*:\s*(.+)", section_text)
        if value_match:
            val = value_match.group(1).strip()
            if val in ("TBD", "Unknown"):
                gaps.append(f"- **{col_name}**: currently {val}")
                continue

        # Check for low confidence
        conf_match = re.search(r"\*\*Confidence\*\*:\s*(.+)", section_text)
        if conf_match:
            conf = conf_match.group(1).strip()
            if conf == "low":
                gaps.append(f"- **{col_name}**: low confidence — needs better source")

    if not gaps:
        return "No obvious gaps — verify and strengthen existing values."

    return "\n".join(gaps)


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------


def fill_research_prompt(
    concept: dict, schema_text: str, dossier_text: str, gaps: str
) -> str:
    """Fill the research prompt template with concept-specific data."""
    template = read_file(RESEARCH_TEMPLATE_PATH)
    if not template:
        print(f"ERROR: Research template not found at {RESEARCH_TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    # Build current knowledge section
    if dossier_text:
        current_knowledge = (
            "From previous research iterations (see dossier for full context):\n\n"
            + dossier_text
        )
    else:
        fields = {
            "Confinement Approach": concept.get("Confinement Approach", "Unknown"),
            "Description": concept.get("Description", "None available"),
            "Fuel Type": concept.get("Fuel Type", "Unknown"),
            "Operation Mode": concept.get("Operation Mode", "Unknown"),
            "Published Machine/Plant?": concept.get("Published Machine/Plant?", "Unknown"),
            "Lab Experiments": concept.get("University / Lab Experiments", "Unknown"),
        }
        lines = ["From the initial concept CSV (no prior research):"]
        for k, v in fields.items():
            lines.append(f"- **{k}**: {v}")
        current_knowledge = "\n".join(lines)

    replacements = {
        "{{concept_name}}": concept["Concept Name"],
        "{{company_name}}": concept.get("Companies Pursuing", "Unknown"),
        "{{confinement_approach}}": concept.get("Confinement Approach", "Unknown"),
        "{{description}}": concept.get("Description", "None available"),
        "{{fuel_type}}": concept.get("Fuel Type", "Unknown"),
        "{{operation_mode}}": concept.get("Operation Mode", "Unknown"),
        "{{schema_content}}": schema_text,
        "{{current_knowledge}}": current_knowledge,
        "{{gaps_list}}": gaps,
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, str(value))

    return result


def fill_synthesis_prompt(
    concept: dict,
    iteration: int,
    concept_dir: Path,
    iter_dir: Path,
    first_iteration: bool,
) -> str:
    """Fill the synthesis prompt template with paths and concept data."""
    template = read_file(SYNTHESIS_TEMPLATE_PATH)
    if not template:
        print(f"ERROR: Synthesis template not found at {SYNTHESIS_TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    today = date.today().isoformat()

    replacements = {
        "{{concept_name}}": concept["Concept Name"],
        "{{company_name}}": concept.get("Companies Pursuing", "Unknown"),
        "{{dossier_path}}": str(concept_dir / "dossier.md"),
        "{{output_path}}": str(iter_dir / "output.md"),
        "{{schema_path}}": str(SCHEMA_PATH),
        "{{changelog_path}}": str(concept_dir / "changelog.md"),
        "{{iteration_number}}": str(iteration),
        "{{date}}": today,
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, str(value))

    # Process conditional blocks
    if first_iteration:
        # Remove {{#unless first_iteration}}...{{/unless}} blocks
        result = re.sub(
            r"\{\{#unless first_iteration\}\}.*?\{\{/unless\}\}",
            "",
            result,
            flags=re.DOTALL,
        )
        # Unwrap {{#if first_iteration}}...{{/if}} blocks (keep content)
        result = re.sub(
            r"\{\{#if first_iteration\}\}(.*?)\{\{/if\}\}",
            r"\1",
            result,
            flags=re.DOTALL,
        )
        # Fill baseline data placeholders
        baseline = {
            "{{confinement_approach}}": concept.get("Confinement Approach", "Unknown"),
            "{{description}}": concept.get("Description", "None available"),
            "{{fuel_type}}": concept.get("Fuel Type", "Unknown"),
            "{{operation_mode}}": concept.get("Operation Mode", "Unknown"),
            "{{published_machine}}": concept.get("Published Machine/Plant?", "Unknown"),
            "{{lab_experiments}}": concept.get("University / Lab Experiments", "Unknown"),
        }
        for key, value in baseline.items():
            result = result.replace(key, str(value))
    else:
        # Remove {{#if first_iteration}}...{{/if}} blocks
        result = re.sub(
            r"\{\{#if first_iteration\}\}.*?\{\{/if\}\}",
            "",
            result,
            flags=re.DOTALL,
        )
        # Unwrap {{#unless first_iteration}}...{{/unless}} blocks (keep content)
        result = re.sub(
            r"\{\{#unless first_iteration\}\}(.*?)\{\{/unless\}\}",
            r"\1",
            result,
            flags=re.DOTALL,
        )

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
    """
    Invoke claude in print mode via stdin.
    Returns (stdout, stderr, returncode).
    """
    cmd = ["claude", "-p"]
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
        return "", "Timed out", -1
    except FileNotFoundError:
        return "", "'claude' command not found — is Claude Code installed and on PATH?", -2


# ---------------------------------------------------------------------------
# Cycle execution
# ---------------------------------------------------------------------------


def run_cycle(
    concept: dict,
    concept_dir: Path,
    iteration: int,
    schema_text: str,
    model: str | None = None,
    timeout: int = 900,
) -> bool:
    """Run one research+synthesis cycle. Returns True on success."""
    iter_dir = concept_dir / f"iter-{iteration:02d}"
    iter_dir.mkdir(parents=True, exist_ok=True)
    (iter_dir / "sources").mkdir(exist_ok=True)

    first_iteration = not (concept_dir / "dossier.md").exists()
    dossier_text = read_file(concept_dir / "dossier.md")

    # ── Research phase ────────────────────────────────────────────────────
    print(f"  [iter-{iteration:02d}] Generating research prompt...")
    gaps = identify_gaps(dossier_text)
    research_prompt = fill_research_prompt(concept, schema_text, dossier_text, gaps)

    # Save prompt for traceability (immutable once written)
    (iter_dir / "prompt.md").write_text(research_prompt, encoding="utf-8")
    print(f"  [iter-{iteration:02d}] Prompt saved ({len(research_prompt):,} chars)")

    print(f"  [iter-{iteration:02d}] Running research agent...")
    stdout, stderr, rc = invoke_claude(research_prompt, cwd=iter_dir, timeout=timeout, model=model)

    if rc != 0 or not stdout.strip():
        print(f"  [iter-{iteration:02d}] ERROR: Research agent failed (rc={rc})", file=sys.stderr)
        if stderr:
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        if stdout:
            (iter_dir / "output.md").write_text(stdout, encoding="utf-8")
        return False

    (iter_dir / "output.md").write_text(stdout, encoding="utf-8")
    print(f"  [iter-{iteration:02d}] Research complete ({len(stdout):,} chars → output.md)")

    # ── Synthesis phase ───────────────────────────────────────────────────
    print(f"  [iter-{iteration:02d}] Generating synthesis prompt...")
    synthesis_prompt = fill_synthesis_prompt(
        concept, iteration, concept_dir, iter_dir, first_iteration
    )

    (iter_dir / "synthesis_prompt.md").write_text(synthesis_prompt, encoding="utf-8")

    print(f"  [iter-{iteration:02d}] Running synthesis agent...")
    stdout, stderr, rc = invoke_claude(synthesis_prompt, cwd=concept_dir, timeout=timeout, model=model)

    if rc != 0:
        print(f"  [iter-{iteration:02d}] WARNING: Synthesis agent exited rc={rc}", file=sys.stderr)
        if stderr:
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)

    # Verify dossier was created/updated
    new_dossier = read_file(concept_dir / "dossier.md")
    if not new_dossier:
        print(f"  [iter-{iteration:02d}] ERROR: Dossier was not created", file=sys.stderr)
        # Save synthesis output for debugging
        if stdout:
            (iter_dir / "synthesis_output.md").write_text(stdout, encoding="utf-8")
        return False

    if new_dossier == dossier_text:
        print(f"  [iter-{iteration:02d}] WARNING: Dossier unchanged after synthesis")
    else:
        print(f"  [iter-{iteration:02d}] Dossier updated ({len(new_dossier):,} chars)")

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def detect_start_iteration(concept_dir: Path) -> int:
    """Find the next iteration number based on existing iter-NN directories."""
    existing = sorted(concept_dir.glob("iter-*/"))
    if not existing:
        return 1
    # Parse the highest existing iteration number
    numbers = []
    for d in existing:
        m = re.match(r"iter-(\d+)", d.name)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers) + 1 if numbers else 1


def print_summary(concept_dir: Path):
    """Print a quick summary of the dossier state."""
    dossier = read_file(concept_dir / "dossier.md")
    if not dossier:
        print("Dossier: not created")
        return

    # Count column sections and TBD/Unknown values
    sections = re.findall(r"^### .+", dossier, re.MULTILINE)
    tbds = len(re.findall(r"\*\*Value\*\*:\s*(TBD|Unknown)", dossier))
    nas = len(re.findall(r"\*\*Value\*\*:\s*N/A", dossier))
    total = len(sections)
    filled = total - tbds - nas

    print(f"Dossier: {filled} filled, {nas} N/A, {tbds} TBD — out of {total} columns")


def main():
    parser = argparse.ArgumentParser(
        description="Run research+synthesis cycles for a single fusion concept.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --concept 01-hts-compact-tokamak --cycles 2
  %(prog)s --concept "CFS" --cycles 1
  %(prog)s --concept 5 --cycles 1 --dry-run
  %(prog)s --concept hts-compact-tokamak --cycles 2 --model sonnet
""",
    )
    parser.add_argument(
        "--concept",
        required=False,
        default=None,
        help="Concept identifier: dir name, index, slug, or partial company/concept name",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=2,
        help="Number of research+synthesis cycles (default: 2)",
    )
    parser.add_argument(
        "--start-iter",
        type=int,
        default=None,
        help="Starting iteration number (default: auto-detect)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Claude model to use (e.g., sonnet, opus, haiku). Default: user's CC default.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Timeout per claude invocation in seconds (default: 900)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate prompts without invoking claude",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all concepts and exit",
    )
    args = parser.parse_args()

    # Load concepts
    if not CSV_PATH.exists():
        print(f"ERROR: Concept CSV not found at {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    concepts = load_concepts(CSV_PATH)

    if args.list:
        for c in concepts:
            print(f"  {c['_dir_name']}: {c['Concept Name']} ({c.get('Companies Pursuing', '?')})")
        sys.exit(0)

    if not args.concept:
        parser.error("--concept is required (or use --list)")

    concept = find_concept(concepts, args.concept)
    if not concept:
        print(f"ERROR: Concept '{args.concept}' not found.", file=sys.stderr)
        print("Use --list to see all available concepts.", file=sys.stderr)
        sys.exit(1)

    # Load schema
    schema_text = read_file(SCHEMA_PATH)
    if not schema_text:
        print(f"ERROR: Schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)

    # Set up concept directory
    concept_dir = RESEARCH_DIR / concept["_dir_name"]
    concept_dir.mkdir(parents=True, exist_ok=True)

    # Determine starting iteration
    start = args.start_iter if args.start_iter is not None else detect_start_iteration(concept_dir)

    # Header
    print(f"{'=' * 60}")
    print(f"Concept:    {concept['Concept Name']}")
    print(f"Company:    {concept.get('Companies Pursuing', 'Unknown')}")
    print(f"Directory:  {concept_dir}")
    print(f"Cycles:     {args.cycles} (iterations {start}–{start + args.cycles - 1})")
    if args.model:
        print(f"Model:      {args.model}")
    if args.dry_run:
        print(f"Mode:       DRY RUN (prompts only)")
    print(f"{'=' * 60}")
    print()

    # Run cycles
    for i in range(args.cycles):
        iteration = start + i
        print(f"--- Cycle {i + 1}/{args.cycles} (iter-{iteration:02d}) ---")

        if args.dry_run:
            iter_dir = concept_dir / f"iter-{iteration:02d}"
            iter_dir.mkdir(parents=True, exist_ok=True)
            (iter_dir / "sources").mkdir(exist_ok=True)

            dossier_text = read_file(concept_dir / "dossier.md")
            gaps = identify_gaps(dossier_text)

            research_prompt = fill_research_prompt(concept, schema_text, dossier_text, gaps)
            (iter_dir / "prompt.md").write_text(research_prompt, encoding="utf-8")

            synthesis_prompt = fill_synthesis_prompt(
                concept, iteration, concept_dir, iter_dir, iteration == 1
            )
            (iter_dir / "synthesis_prompt.md").write_text(synthesis_prompt, encoding="utf-8")

            print(f"  [iter-{iteration:02d}] Prompts written to {iter_dir.relative_to(PHASE_1A_DIR)}")
            print()
            continue

        success = run_cycle(
            concept,
            concept_dir,
            iteration,
            schema_text,
            model=args.model,
            timeout=args.timeout,
        )

        if not success:
            print(f"\nCycle {i + 1} failed. Stopping early.")
            sys.exit(1)

        print()

    # Summary
    print(f"{'=' * 60}")
    print("Done.")
    print_summary(concept_dir)


if __name__ == "__main__":
    main()
