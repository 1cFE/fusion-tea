#!/usr/bin/env python3
"""Migrate Phase 1a research to knowledge/concept_research/.

Copies research directories, creates symlink for backward compatibility,
generates inner SOURCE_INDEX.md, and creates local .gitignore for binaries.

Usage:
    uv run python scripts/migrate_research.py              # full migration
    uv run python scripts/migrate_research.py --dry-run    # report only
    uv run python scripts/migrate_research.py --reindex    # regenerate SOURCE_INDEX.md only
"""

import argparse
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "exploration" / "phase_1a" / "research"
DEST_DIR = REPO_ROOT / "knowledge" / "concept_research"
SYMLINK_PATH = SOURCE_DIR  # after migration, this becomes a symlink

BINARY_EXTENSIONS = {".pdf", ".html", ".png", ".jpg", ".jpeg", ".gif", ".svg"}
TEXT_EXTENSIONS = {".md", ".json"}

GITIGNORE_CONTENT = """\
# Binary artifacts — synced via R2, not git
*.pdf
*.html
*.png
*.jpg
*.jpeg
*.gif
*.svg
"""


def count_files_by_type(directory: Path) -> Counter:
    """Count files grouped by extension."""
    counts = Counter()
    for f in directory.rglob("*"):
        if f.is_file():
            counts[f.suffix.lower()] += 1
    return counts


def is_already_migrated() -> bool:
    """Check if migration has already been performed."""
    return DEST_DIR.is_dir() and SYMLINK_PATH.is_symlink()


def detect_source_type(source_dir: Path) -> str:
    """Detect the type of a source based on its companion directory contents."""
    if (source_dir / "raw.pdf").exists():
        return "PDF"
    if (source_dir / "raw.html").exists():
        return "HTML"
    if (source_dir / "images").is_dir():
        return "PDF"  # images without raw file = extracted PDF
    return "extraction"


def generate_source_index(base_dir: Path) -> str:
    """Generate the inner SOURCE_INDEX.md content by scanning the directory tree."""
    lines = [
        "# Concept Research — Source Index",
        "",
        "Per-concept research dossiers and source extractions for the Fusion TEA",
        "concept landscape. Binary artifacts (PDF, HTML, PNG) synced via R2;",
        "markdown and JSON tracked in git.",
        "",
        "Sync: `./scripts/sync_research.sh pull`",
        "",
        "## Concepts",
        "",
    ]

    concept_dirs = sorted(
        [d for d in base_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name,
    )

    for concept_dir in concept_dirs:
        concept_id = concept_dir.name
        lines.append(f"### {concept_id}")

        # Check for dossier
        dossier = concept_dir / "dossier.md"
        if dossier.exists():
            lines.append(f"- **Dossier**: `{concept_id}/dossier.md`")

        # Find iterations
        iter_dirs = sorted(
            [d for d in concept_dir.iterdir() if d.is_dir() and d.name.startswith("iter-")],
            key=lambda d: d.name,
        )

        if iter_dirs:
            iter_names = ", ".join(d.name for d in iter_dirs)
            lines.append(f"- **Iterations**: {len(iter_dirs)} ({iter_names})")

        # Collect all sources across iterations
        sources = []
        for iter_dir in iter_dirs:
            sources_dir = iter_dir / "sources"
            if not sources_dir.is_dir():
                continue
            for item in sorted(sources_dir.iterdir()):
                if item.is_dir():
                    stype = detect_source_type(item)
                    rel = f"{iter_dir.name}/sources/{item.name}"
                    sources.append((rel, stype))
                elif item.suffix == ".md" and item.name.endswith(".orig.md"):
                    # .orig.md files are processed extractions alongside companion dirs
                    pass
                elif item.suffix == ".md":
                    rel = f"{iter_dir.name}/sources/{item.name}"
                    sources.append((rel, "processed .md"))

        if sources:
            lines.append(f"- **Sources** ({len(sources)}):")
            for rel_path, stype in sources:
                lines.append(f"  - `{rel_path}` — [{stype}]")
        else:
            lines.append("- **Sources**: none")

        lines.append("")

    return "\n".join(lines)


def do_dry_run():
    """Report what would happen without making changes."""
    if is_already_migrated():
        print("Already migrated. Use --reindex to regenerate SOURCE_INDEX.md.")
        return

    if not SOURCE_DIR.is_dir():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        sys.exit(1)

    counts = count_files_by_type(SOURCE_DIR)
    total = sum(counts.values())
    binary_count = sum(v for k, v in counts.items() if k in BINARY_EXTENSIONS)
    text_count = sum(v for k, v in counts.items() if k in TEXT_EXTENSIONS)

    concept_dirs = [d for d in SOURCE_DIR.iterdir() if d.is_dir()]

    print("=== Migration Dry Run ===")
    print(f"Source: {SOURCE_DIR}")
    print(f"Destination: {DEST_DIR}")
    print()
    print(f"Concept directories: {len(concept_dirs)}")
    print(f"Total files: {total}")
    print()
    print("By extension:")
    for ext, count in sorted(counts.items(), key=lambda x: -x[1]):
        category = "binary (R2)" if ext in BINARY_EXTENSIONS else "text (git)"
        print(f"  {ext:8s}  {count:5d}  [{category}]")
    print()
    print(f"Binary files (gitignored, R2-synced): {binary_count}")
    print(f"Text files (git-tracked): {text_count}")
    print()
    print("Actions that would be taken:")
    print(f"  1. Copy {SOURCE_DIR.relative_to(REPO_ROOT)} → {DEST_DIR.relative_to(REPO_ROOT)}")
    print(f"  2. Create .gitignore in {DEST_DIR.relative_to(REPO_ROOT)}/")
    print(f"  3. Generate SOURCE_INDEX.md in {DEST_DIR.relative_to(REPO_ROOT)}/")
    print(f"  4. Remove original directory")
    print(f"  5. Create symlink: {SOURCE_DIR.relative_to(REPO_ROOT)} → ../../knowledge/concept_research")


def do_reindex():
    """Regenerate SOURCE_INDEX.md from existing migrated directory."""
    if not DEST_DIR.is_dir():
        print(f"ERROR: Destination not found: {DEST_DIR}")
        print("Run migration first (without --reindex).")
        sys.exit(1)

    index_content = generate_source_index(DEST_DIR)
    index_path = DEST_DIR / "SOURCE_INDEX.md"
    index_path.write_text(index_content)
    print(f"Regenerated: {index_path.relative_to(REPO_ROOT)}")


def do_migrate():
    """Execute the full migration."""
    # Idempotency check
    if is_already_migrated():
        print("Already migrated (destination exists and symlink is in place).")
        print("Use --reindex to regenerate SOURCE_INDEX.md.")
        sys.exit(0)

    # Pre-checks
    if SYMLINK_PATH.is_symlink():
        print(f"ERROR: Symlink already exists at {SYMLINK_PATH} but destination missing.")
        print("Remove the symlink and re-run, or investigate manually.")
        sys.exit(1)

    if not SOURCE_DIR.is_dir():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        sys.exit(1)

    if DEST_DIR.exists():
        print(f"ERROR: Destination already exists: {DEST_DIR}")
        print("Remove it manually if you want to re-migrate.")
        sys.exit(1)

    # Count source files
    print("Counting source files...")
    source_counts = count_files_by_type(SOURCE_DIR)
    source_total = sum(source_counts.values())
    print(f"  Source: {source_total} files")

    # Copy
    print(f"Copying {SOURCE_DIR.relative_to(REPO_ROOT)} → {DEST_DIR.relative_to(REPO_ROOT)}...")
    shutil.copytree(SOURCE_DIR, DEST_DIR, symlinks=False)

    # Verify counts
    print("Verifying file counts...")
    dest_counts = count_files_by_type(DEST_DIR)
    dest_total = sum(dest_counts.values())

    if source_counts != dest_counts:
        print("ERROR: File count mismatch!")
        print(f"  Source: {dict(source_counts)}")
        print(f"  Dest:   {dict(dest_counts)}")
        print("Destination left in place for inspection. Not removing source.")
        sys.exit(1)

    print(f"  Destination: {dest_total} files — counts match")

    # Create .gitignore
    gitignore_path = DEST_DIR / ".gitignore"
    gitignore_path.write_text(GITIGNORE_CONTENT)
    print(f"Created: {gitignore_path.relative_to(REPO_ROOT)}")

    # Generate SOURCE_INDEX.md
    index_content = generate_source_index(DEST_DIR)
    index_path = DEST_DIR / "SOURCE_INDEX.md"
    index_path.write_text(index_content)
    print(f"Generated: {index_path.relative_to(REPO_ROOT)}")

    # Remove original and create symlink
    print(f"Removing original: {SOURCE_DIR.relative_to(REPO_ROOT)}")
    shutil.rmtree(SOURCE_DIR)

    # Create relative symlink
    symlink_target = os.path.relpath(DEST_DIR, SYMLINK_PATH.parent)
    SYMLINK_PATH.symlink_to(symlink_target)
    print(f"Created symlink: {SYMLINK_PATH.relative_to(REPO_ROOT)} → {symlink_target}")

    # Verify symlink
    resolved = SYMLINK_PATH.resolve()
    if resolved == DEST_DIR.resolve():
        print(f"Symlink verified: resolves to {resolved}")
    else:
        print(f"WARNING: Symlink resolves to {resolved}, expected {DEST_DIR.resolve()}")

    # Summary
    binary_count = sum(v for k, v in dest_counts.items() if k in BINARY_EXTENSIONS)
    text_count = sum(v for k, v in dest_counts.items() if k in TEXT_EXTENSIONS)
    print()
    print("=== Migration Complete ===")
    print(f"  Files copied: {dest_total}")
    print(f"  Binary (R2-synced, gitignored): {binary_count}")
    print(f"  Text (git-tracked): {text_count}")
    print(f"  SOURCE_INDEX.md generated with {len(list(DEST_DIR.iterdir()))} entries")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate Phase 1a research to knowledge/concept_research/"
    )
    parser.add_argument("--dry-run", action="store_true", help="Report only, no changes")
    parser.add_argument("--reindex", action="store_true", help="Regenerate SOURCE_INDEX.md only")
    args = parser.parse_args()

    if args.dry_run:
        do_dry_run()
    elif args.reindex:
        do_reindex()
    else:
        do_migrate()


if __name__ == "__main__":
    main()
