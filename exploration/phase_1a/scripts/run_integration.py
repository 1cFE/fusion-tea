#!/usr/bin/env python3
"""
Cross-concept integration orchestration for Phase 1a.

Fills the integration.md prompt template with batch-specific dossier paths,
invokes a Claude agent to produce the master differentiation table, citation
registry, and consistency checkpoint.

Usage:
  uv run python exploration/phase_1a/scripts/run_integration.py --batch 1 --dry-run
  uv run python exploration/phase_1a/scripts/run_integration.py --batch 3
  uv run python exploration/phase_1a/scripts/run_integration.py --all
  uv run python exploration/phase_1a/scripts/run_integration.py --list-batches
"""

import argparse
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
TEMPLATE_PATH = PHASE_1A_DIR / "prompt_templates" / "integration.md"
TABLE_PATH = PHASE_1A_DIR / "table.csv"
CITATIONS_PATH = PHASE_1A_DIR / "citations.csv"
CHECKPOINTS_DIR = PHASE_1A_DIR / "checkpoints"

# Superseded composite concepts — skipped in --all mode
SUPERSEDED_DIRS = {"20-modular-hts-stellarator"}


# ---------------------------------------------------------------------------
# Batch definitions — hardcoded to match sprint_plan_1a.md
# ---------------------------------------------------------------------------

BATCHES = {
    1: {
        "name": "Tokamaks",
        "concepts": [
            "01-hts-compact-tokamak",
            "21-spherical-tokamak-hts",
            "28-hts-tokamak-full-hts",
            "29-negative-triangularity-tokamak",
            "33-state-backed-tokamak-best",
            "34-compact-spherical-tokamak-india",
        ],
    },
    2: {
        "name": "Stellarators",
        "concepts": [
            "05-planar-coil-stellarator",
            "09-qi-stellarator-hts",
            "10-large-scale-stellarator",
            "20a-type-one-stellarator",
            "20b-renaissance-stellarator",
            "36-helical-coil-stellarator",
        ],
    },
    3: {
        "name": "FRC, Z-Pinch, Mirrors",
        "concepts": [
            "08-frc-w-direct-conversion",
            "18-p-b11-frc",
            "15-sheared-flow-stabilized-z-pinch",
            "06-magnetic-mirror",
            "11-magnetic-mirror",
        ],
    },
    4: {
        "name": "Magnetized Target + Levitated Dipole",
        "concepts": [
            "07-maglif",
            "14-magnetized-target-fusion-pneumatic-compression",
            "12-levitated-dipole",
            "19-orbital-levitated-dipole",
        ],
    },
    5: {
        "name": "Laser & Non-Laser IFE",
        "concepts": [
            "17-laser-icf-direct-drive",
            "26-laser-icf-indirect-drive",
            "30-laser-icf-nif-commercialization",
            "31-laser-icf-oec-architecture",
            "32-laser-icf-french-national",
            "03-laser-icf-liquid-jet-target",
            "04-laser-icf",
            "23-laser-icf-nanostructured-target",
            "22-projectile-icf",
            "25-heavy-ion-beam-icf",
        ],
    },
    6: {
        "name": "Exotic & Other",
        "concepts": [
            "02-acoustic-icf-sonofusion",
            "13-electrostatic-hybrid",
            "16-muon-catalyzed-fusion",
            "24-dense-plasma-focus",
            "27-polywell",
            "35-polomac-magnetic-confinement",
        ],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_file(path: Path) -> str:
    """Read file contents. Returns empty string if file does not exist."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def invoke_claude(
    prompt: str,
    cwd: Path,
    timeout: int = 1800,
    model: str | None = None,
) -> tuple[str, str, int]:
    """
    Invoke claude in print mode via stdin.
    Returns (stdout, stderr, returncode).
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
        return "", "Timed out", -1
    except FileNotFoundError:
        return "", "'claude' command not found — is Claude Code installed and on PATH?", -2


# ---------------------------------------------------------------------------
# Batch helpers
# ---------------------------------------------------------------------------


def get_dossier_path(concept_dir_name: str) -> Path:
    """Return the dossier path for a concept directory name."""
    return RESEARCH_DIR / concept_dir_name / "dossier.md"


def check_batch_dossiers(concepts: list[str]) -> tuple[list[str], list[str]]:
    """Check which concepts have dossiers. Returns (found, missing)."""
    found = []
    missing = []
    for c in concepts:
        if get_dossier_path(c).exists():
            found.append(c)
        else:
            missing.append(c)
    return found, missing


def all_concepts_with_dossiers() -> list[str]:
    """Scan research/ for all concept dirs that have a dossier.md, skipping superseded."""
    concepts = []
    if not RESEARCH_DIR.exists():
        return concepts
    for d in sorted(RESEARCH_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name in SUPERSEDED_DIRS:
            continue
        if (d / "dossier.md").exists():
            concepts.append(d.name)
    return concepts


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------


def fill_integration_prompt(
    batch_number: int | str,
    batch_name: str,
    concepts: list[str],
) -> str:
    """Fill the integration.md template with batch-specific data."""
    template = read_file(TEMPLATE_PATH)
    if not template:
        print(f"ERROR: Integration template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    # Build dossier file list — absolute paths for the agent
    dossier_lines = []
    for c in concepts:
        path = get_dossier_path(c)
        dossier_lines.append(f"- `{path}`")
    dossier_file_list = "\n".join(dossier_lines)

    checkpoint_num = f"{batch_number:02d}" if isinstance(batch_number, int) else batch_number
    checkpoint_path = CHECKPOINTS_DIR / f"checkpoint-{checkpoint_num}.md"

    replacements = {
        "{{batch_number}}": str(batch_number),
        "{{batch_name}}": batch_name,
        "{{dossier_file_list}}": dossier_file_list,
        "{{schema_path}}": str(SCHEMA_PATH),
        "{{table_path}}": str(TABLE_PATH),
        "{{citations_path}}": str(CITATIONS_PATH),
        "{{checkpoint_path}}": str(checkpoint_path),
        "{{date}}": date.today().isoformat(),
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)

    return result


# ---------------------------------------------------------------------------
# List batches
# ---------------------------------------------------------------------------


def list_batches():
    """Print batch status overview."""
    print(f"{'=' * 60}")
    print("Phase 1a — Batch Status")
    print(f"{'=' * 60}")
    print()

    for num, batch in sorted(BATCHES.items()):
        found, missing = check_batch_dossiers(batch["concepts"])
        total = len(batch["concepts"])
        checkpoint = CHECKPOINTS_DIR / f"checkpoint-{num:02d}.md"
        ckpt_status = "done" if checkpoint.exists() else "pending"

        status_char = "+" if len(found) == total else ("~" if found else "-")
        print(f"  Batch {num}: {batch['name']}")
        print(f"    Dossiers: {len(found)}/{total} {'(all present)' if len(found) == total else ''}")
        if missing:
            print(f"    Missing:  {', '.join(missing)}")
        print(f"    Checkpoint: {ckpt_status}")
        print()

    # Summary of all dossiers
    all_dossiers = all_concepts_with_dossiers()
    print(f"  Total dossiers found: {len(all_dossiers)}")
    print(f"  Table exists: {'yes' if TABLE_PATH.exists() else 'no'}")
    print(f"  Citations exists: {'yes' if CITATIONS_PATH.exists() else 'no'}")


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def verify_outputs(batch_number: int | str) -> bool:
    """Check that integration outputs exist. Returns True if all present."""
    checkpoint_num = f"{batch_number:02d}" if isinstance(batch_number, int) else batch_number
    checkpoint_path = CHECKPOINTS_DIR / f"checkpoint-{checkpoint_num}.md"

    ok = True
    for path, name in [
        (TABLE_PATH, "table.csv"),
        (CITATIONS_PATH, "citations.csv"),
        (checkpoint_path, f"checkpoint-{checkpoint_num}.md"),
    ]:
        if path.exists():
            size = path.stat().st_size
            print(f"  [ok] {name} ({size:,} bytes)")
        else:
            print(f"  [MISSING] {name}")
            ok = False

    # Quick table row count
    if TABLE_PATH.exists():
        lines = TABLE_PATH.read_text(encoding="utf-8").strip().split("\n")
        data_rows = len(lines) - 1  # subtract header
        print(f"  Table rows: {data_rows} (excluding header)")

    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Run cross-concept integration for Phase 1a.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --batch 1 --dry-run        # Fill template, save prompt, don't invoke
  %(prog)s --batch 3                   # Integrate batch 3
  %(prog)s --all                       # Final consolidation across all concepts
  %(prog)s --list-batches              # Show batch status
""",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--batch",
        type=int,
        choices=range(1, 7),
        metavar="N",
        help="Batch number to integrate (1-6)",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Final consolidation across all completed concepts",
    )
    group.add_argument(
        "--list-batches",
        action="store_true",
        help="Show batch status and exit",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Claude model to use (e.g., sonnet, opus). Default: user's CC default.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Timeout per claude invocation in seconds (default: 1800)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fill template and save prompt without invoking claude",
    )
    args = parser.parse_args()

    if args.list_batches:
        list_batches()
        sys.exit(0)

    if not args.batch and not args.all:
        parser.error("one of --batch N, --all, or --list-batches is required")

    # Resolve batch → concepts
    if args.batch:
        batch_num = args.batch
        batch = BATCHES[batch_num]
        batch_name = batch["name"]
        concepts = batch["concepts"]
        prompt_label = f"{batch_num:02d}"
    else:
        # --all mode
        concepts = all_concepts_with_dossiers()
        if not concepts:
            print("ERROR: No dossiers found in research/", file=sys.stderr)
            sys.exit(1)
        batch_num = "all"
        batch_name = "Final Consolidation"
        prompt_label = "all"

    # Verify dossiers exist
    found, missing = check_batch_dossiers(concepts)
    if missing:
        print(f"ERROR: Missing dossiers for {len(missing)} concept(s):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        print(file=sys.stderr)
        print("Run concept research first:", file=sys.stderr)
        for m in missing:
            print(
                f"  uv run python exploration/phase_1a/scripts/run_concept.py --concept {m} --cycles 2",
                file=sys.stderr,
            )
        sys.exit(1)

    # Fill template
    prompt = fill_integration_prompt(batch_num, batch_name, concepts)

    # Ensure checkpoints dir exists
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save prompt
    prompt_path = CHECKPOINTS_DIR / f"integration-prompt-{prompt_label}.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    # Header
    print(f"{'=' * 60}")
    print(f"Integration: Batch {batch_num} — {batch_name}")
    print(f"Concepts:    {len(concepts)}")
    print(f"Prompt:      {prompt_path.relative_to(PHASE_1A_DIR)}")
    if args.model:
        print(f"Model:       {args.model}")
    if args.dry_run:
        print(f"Mode:        DRY RUN (prompt saved, not invoking claude)")
    print(f"{'=' * 60}")
    print()

    if args.dry_run:
        print(f"Prompt saved to {prompt_path}")
        print(f"  {len(prompt):,} chars, {len(concepts)} dossier paths")
        sys.exit(0)

    # Invoke claude
    print("Running integration agent...")
    stdout, stderr, rc = invoke_claude(
        prompt, cwd=PHASE_1A_DIR, timeout=args.timeout, model=args.model
    )

    # Save agent log
    log_path = CHECKPOINTS_DIR / f"integration-log-{prompt_label}.md"
    if stdout:
        log_path.write_text(stdout, encoding="utf-8")
        print(f"Agent log saved ({len(stdout):,} chars)")

    if rc != 0:
        print(f"WARNING: Agent exited with rc={rc}", file=sys.stderr)
        if stderr:
            print(f"  stderr: {stderr[:500]}", file=sys.stderr)

    # Verify outputs
    print()
    print("Verifying outputs...")
    ok = verify_outputs(batch_num)

    print()
    if ok:
        print("Integration complete.")
    else:
        print("WARNING: Some expected outputs are missing — check agent log.")
        sys.exit(1)


if __name__ == "__main__":
    main()
