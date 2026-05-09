#!/usr/bin/env python3
"""One-shot migration: reorganize concept analysis directories into iter-N/ layout.

Moves iteration artifacts into iter-N/ subdirectories, non-iteration prompts
into prompts/, and generates verdict.json for each migrated iteration.

Usage:
  uv run python scripts/migrate_iterations.py              # migrate all
  uv run python scripts/migrate_iterations.py 02            # migrate one concept
  uv run python scripts/migrate_iterations.py --dry-run     # preview
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow imports from scripts/lib/
sys.path.insert(0, str(Path(__file__).parent))

from lib.iteration import parse_verdict_from_feedback
from lib.paths import ANALYSES_DIR


# Files that map from old flat layout to iter-N/ layout
ITER_FILE_MAP = {
    # old_pattern -> new_name (within iter-N/)
    "analysis_prompt_iter_{n}.md": "analyze_prompt.md",
    "assessment_prompt_iter_{n}.md": "assess_prompt.md",
    "feedback_iter_{n}.md": "post_feedback.md",
}

# Non-iteration prompts to move to prompts/
NON_ITER_PROMPTS = [
    "gap_check_prompt.md",
    "analysis_prompt.md",        # pre-loop era prompt (not analysis_prompt_iter_N.md)
    "review_prompt.md",
    "synthesis_prompt.md",
    "address_review_prompt.md",
    "model_setup_prompt.md",
]

# Glob patterns for update-analysis artifacts → prompts/
UPDATE_ANALYSIS_GLOBS = [
    "source_integration_prompt_*.md",
    "feedback_update_*.md",
    "update_analysis_prompt_*.md",
    "feedback_apply_prompt_*.md",
]


def detect_iterations(concept_dir: Path) -> list[int]:
    """Detect iteration numbers from existing flat artifacts."""
    iters = set()
    for f in concept_dir.glob("analysis_prompt_iter_*.md"):
        m = re.search(r"iter_(\d+)\.md$", f.name)
        if m:
            iters.add(int(m.group(1)))
    for f in concept_dir.glob("feedback_iter_*.md"):
        m = re.search(r"iter_(\d+)\.md$", f.name)
        if m:
            iters.add(int(m.group(1)))
    return sorted(iters)


def extract_body(analysis_path: Path) -> str:
    """Extract body (sans frontmatter) from analysis.md."""
    text = analysis_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def extract_sources_from_prompt(prompt_path: Path) -> list[str]:
    """Extract source file paths mentioned in a rendered analyze prompt.

    Looks for lines matching source paths in research directories. Sources
    may use either knowledge/concept_research/ or phase_1a/research/ paths
    (the latter is a symlink to the former).
    """
    if not prompt_path.exists():
        return []
    text = prompt_path.read_text(encoding="utf-8")
    sources = []
    # Match lines that look like source paths — they contain /sources/ and end with .md
    # and typically appear as bullet items with size annotations
    source_re = re.compile(
        r"`?(/[^`\s]+/(?:sources|concept_research)/[^`\s]+\.md)`?"
        r"(?:\s*\([\d.]+ [KMG]B\))?"
    )
    for line in text.splitlines():
        m = source_re.search(line)
        if m:
            path_str = m.group(1)
            # Normalize symlink paths to canonical knowledge/concept_research/
            # Old prompts used phase_1a/research/ which is a symlink.
            # find_sources() returns knowledge/concept_research/ paths, so
            # detect_new_sources() string comparison needs consistent paths.
            path_str = path_str.replace(
                "/exploration/phase_1a/research/",
                "/knowledge/concept_research/",
            )
            sources.append(path_str)
    return sources


def migrate_concept(concept_dir: Path, dry_run: bool = False) -> dict:
    """Migrate one concept directory. Returns stats dict."""
    cid = concept_dir.name
    stats = {"moved": 0, "verdicts": 0, "skipped": 0, "prompts_moved": 0}

    # Detect flat artifacts still needing migration
    iters = detect_iterations(concept_dir)
    existing_iter_dirs = sorted(concept_dir.glob("iter-*/"))

    # Already fully migrated? (iter dirs exist, no flat artifacts, all have verdicts)
    if existing_iter_dirs and not iters:
        missing_verdicts = [d for d in existing_iter_dirs if not (d / "verdict.json").exists()]
        if not missing_verdicts:
            print(f"  {cid}: already migrated (iter-*/ dirs exist, no flat artifacts)")
            stats["skipped"] = 1
            return stats
    # Also detect iterations from existing iter-N/ dirs (files already moved)
    for d in existing_iter_dirs:
        m = re.match(r"^iter-(\d+)$", d.name)
        if m:
            n = int(m.group(1))
            if n not in iters:
                iters.append(n)
    iters = sorted(set(iters))

    analysis_path = concept_dir / "analysis.md"
    has_analysis = analysis_path.exists()

    # Handle concepts with analysis but no iteration prompts or iter dirs
    if has_analysis and not iters:
        iters = [1]  # treat as single iteration

    if not iters:
        # No iterations and no analysis — gap-check-only or not-started
        # Still move non-iteration prompts if any exist
        moved_prompts = _move_non_iter_prompts(concept_dir, dry_run)
        stats["prompts_moved"] = moved_prompts
        if moved_prompts:
            print(f"  {cid}: no iterations, moved {moved_prompts} prompts")
        return stats

    print(f"  {cid}: {len(iters)} iteration(s)")

    for n in iters:
        iter_dir = concept_dir / f"iter-{n}"
        verdict_path = iter_dir / "verdict.json"

        # Skip if already migrated
        if verdict_path.exists():
            print(f"    iter-{n}: already migrated")
            continue

        if dry_run:
            print(f"    iter-{n}: would create {iter_dir}/")
        else:
            iter_dir.mkdir(parents=True, exist_ok=True)

        # Move iteration files
        for old_pattern, new_name in ITER_FILE_MAP.items():
            old_name = old_pattern.format(n=n)
            old_path = concept_dir / old_name
            new_path = iter_dir / new_name
            if old_path.exists() and not new_path.exists():
                if dry_run:
                    print(f"    move {old_name} → iter-{n}/{new_name}")
                else:
                    old_path.rename(new_path)
                stats["moved"] += 1

        # Create analysis_output.md for this iteration
        output_path = iter_dir / "analysis_output.md"
        if not output_path.exists() and has_analysis:
            if n == max(iters):
                # Latest iteration: extract body from current analysis.md
                body = extract_body(analysis_path)
                if dry_run:
                    print(f"    create iter-{n}/analysis_output.md ({len(body)} chars from analysis.md)")
                else:
                    output_path.write_text(body, encoding="utf-8")

        # Generate verdict.json
        if not verdict_path.exists():
            feedback_path = iter_dir / "post_feedback.md"
            if not feedback_path.exists():
                # Pre-move location
                feedback_path = concept_dir / f"feedback_iter_{n}.md"

            if feedback_path.exists():
                feedback_text = feedback_path.read_text(encoding="utf-8")
                verdict, finding_count = parse_verdict_from_feedback(feedback_text)
                timestamp = datetime.fromtimestamp(
                    feedback_path.stat().st_mtime, tz=timezone.utc
                ).isoformat()
            else:
                verdict = "INTERRUPTED"
                finding_count = 0
                timestamp = datetime.now(timezone.utc).isoformat()

            # Extract sources from the analyze prompt for this iteration
            prompt_path = iter_dir / "analyze_prompt.md"
            if not prompt_path.exists():
                prompt_path = concept_dir / f"analysis_prompt_iter_{n}.md"
            sources = extract_sources_from_prompt(prompt_path)

            verdict_data = {
                "iteration": n,
                "verdict": verdict,
                "finding_count": finding_count,
                "feedback_source": "cold_start" if n == 1 else "assess",
                "model_ran": False,
                "model_ok": False,
                "research_ran": False,
                "sources": sources,
                "timestamp": timestamp,
            }

            if dry_run:
                print(f"    verdict.json: {verdict} ({finding_count} findings)")
            else:
                verdict_path.write_text(
                    json.dumps(verdict_data, indent=2) + "\n", encoding="utf-8"
                )
            stats["verdicts"] += 1

    # Move non-iteration prompts to prompts/
    moved_prompts = _move_non_iter_prompts(concept_dir, dry_run)
    stats["prompts_moved"] = moved_prompts

    return stats


def _move_non_iter_prompts(concept_dir: Path, dry_run: bool) -> int:
    """Move non-iteration prompt files to prompts/ subdirectory. Returns count moved."""
    count = 0
    prompts_dir = concept_dir / "prompts"

    # Named prompts
    for name in NON_ITER_PROMPTS:
        src = concept_dir / name
        if src.exists():
            dst = prompts_dir / name
            if not dst.exists():
                if dry_run:
                    print(f"    prompt: {name} → prompts/{name}")
                else:
                    prompts_dir.mkdir(exist_ok=True)
                    src.rename(dst)
                count += 1

    # Glob-based patterns (update-analysis artifacts)
    for pattern in UPDATE_ANALYSIS_GLOBS:
        for src in concept_dir.glob(pattern):
            dst = prompts_dir / src.name
            if not dst.exists():
                if dry_run:
                    print(f"    prompt: {src.name} → prompts/{src.name}")
                else:
                    prompts_dir.mkdir(exist_ok=True)
                    src.rename(dst)
                count += 1

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Migrate concept analysis dirs to iter-N/ layout",
    )
    parser.add_argument("concepts", nargs="*", help="Concept IDs (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    args = parser.parse_args()

    if args.concepts:
        # Resolve concept dirs
        dirs = []
        for c in args.concepts:
            matches = list(ANALYSES_DIR.glob(f"{c}*"))
            if not matches:
                print(f"  error: no concept matching '{c}'")
                sys.exit(1)
            dirs.extend(sorted(matches))
    else:
        dirs = sorted(d for d in ANALYSES_DIR.iterdir() if d.is_dir())

    if args.dry_run:
        print("=== DRY RUN ===\n")

    total = {"moved": 0, "verdicts": 0, "skipped": 0, "prompts_moved": 0, "concepts": 0}
    for d in dirs:
        s = migrate_concept(d, dry_run=args.dry_run)
        for k in total:
            if k != "concepts":
                total[k] += s.get(k, 0)
        total["concepts"] += 1

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
    print(f"  {total['concepts']} concepts processed")
    print(f"  {total['moved']} files moved to iter-N/")
    print(f"  {total['verdicts']} verdict.json files generated")
    print(f"  {total['prompts_moved']} prompts moved to prompts/")
    if total["skipped"]:
        print(f"  {total['skipped']} already migrated (skipped)")


if __name__ == "__main__":
    main()
