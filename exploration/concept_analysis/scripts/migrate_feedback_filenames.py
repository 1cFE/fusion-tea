#!/usr/bin/env python3
"""One-shot migration: rename iter-N/feedback.md → iter-N/post_feedback.md.

Part of the feedback-dispatch symmetry refactor. After this migration,
`feedback.md` (the ambiguous name used for both input and output) becomes
`post_feedback.md` (assess output only). The new `pre_feedback.md` (input
to analyze) is created by the updated dispatch chain — not by this script.

Usage:
  uv run python scripts/migrate_feedback_filenames.py              # migrate all
  uv run python scripts/migrate_feedback_filenames.py 02            # migrate one concept
  uv run python scripts/migrate_feedback_filenames.py --dry-run     # preview
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

# Allow imports from scripts/lib/ when run as a script
sys.path.insert(0, str(Path(__file__).parent))

from lib.paths import ANALYSES_DIR


@dataclass
class MigrationResult:
    """Summary of a migration run."""
    renamed: int = 0
    skipped: int = 0


def run_migration(
    analyses_dir: Path,
    *,
    dry_run: bool = False,
    concept_filter: str | None = None,
) -> MigrationResult:
    """Rename feedback.md → post_feedback.md in every iter-N/ directory.

    Args:
        analyses_dir: Root directory containing concept subdirectories.
        dry_run: If True, report what would happen without modifying files.
        concept_filter: If set, only process concept dirs whose name contains
            this substring (e.g., "02" matches "02-bar").

    Returns:
        MigrationResult with counts of renamed and skipped files.
    """
    result = MigrationResult()

    for old_path in sorted(analyses_dir.glob("*/iter-*/feedback.md")):
        # Apply concept filter if provided
        concept_name = old_path.parent.parent.name
        if concept_filter and concept_filter not in concept_name:
            continue

        new_path = old_path.parent / "post_feedback.md"

        if new_path.exists():
            result.skipped += 1
            if dry_run:
                print(f"  skip (already exists): {old_path.relative_to(analyses_dir)}")
            continue

        result.renamed += 1
        if dry_run:
            print(f"  would rename: {old_path.relative_to(analyses_dir)} → post_feedback.md")
        else:
            old_path.rename(new_path)
            print(f"  renamed: {old_path.relative_to(analyses_dir)} → post_feedback.md")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Rename iter-N/feedback.md → iter-N/post_feedback.md")
    parser.add_argument(
        "concept", nargs="?", default=None,
        help="Optional concept ID filter (e.g., '02' matches '02-bar')")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview renames without modifying files")
    parser.add_argument(
        "--analyses-dir", type=Path, default=ANALYSES_DIR,
        help=f"Analyses directory (default: {ANALYSES_DIR})")
    args = parser.parse_args()

    print(f"Scanning {args.analyses_dir} ...")
    result = run_migration(
        args.analyses_dir,
        dry_run=args.dry_run,
        concept_filter=args.concept,
    )

    mode = "DRY RUN" if args.dry_run else "DONE"
    print(f"\n{mode}: {result.renamed} renamed, {result.skipped} skipped (already migrated)")


if __name__ == "__main__":
    main()
