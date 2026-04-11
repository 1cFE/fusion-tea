"""Re-source .orig.md files by extracting header URLs and searching for proper sources.

Discovers .orig.md files (Haiku-paraphrased multi-source compilations with broken
provenance), invokes a claude -p agent per file to find and extract actual source
URLs via add-source, and produces per-file coverage reports.

Usage:
    uv run python scripts/resurface_orig.py --all --dry-run
    uv run python scripts/resurface_orig.py FILE [FILE ...] --dry-run
    uv run python scripts/resurface_orig.py --all --max-extractions 3
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

from lib.claude import invoke_claude
from lib.paths import CONCEPT_ANALYSIS_DIR, RESEARCH_DIR, TEMPLATES_DIR
from lib.sources import find_sources
from lib.templating import fill_template

REPORT_DIR = CONCEPT_ANALYSIS_DIR / "resurface_reports"
TEMPLATE_PATH = TEMPLATES_DIR / "resurface.md"


def parse_concept_from_path(orig_path: Path) -> tuple[str, str]:
    """Extract concept_id and concept_num from .orig.md path.

    Path pattern: .../knowledge/concept_research/<concept_id>/iter-NN/sources/<name>.orig.md
    Returns (concept_id, concept_num) e.g. ("22-projectile-icf", "22").
    """
    # Walk up: sources/ -> iter-NN/ -> concept_id/
    concept_dir = orig_path.parent.parent.parent
    concept_id = concept_dir.name
    m = re.match(r"^(\d+[a-z]?)-", concept_id)
    if not m:
        print(f"  error: cannot parse concept number from '{concept_id}'")
        sys.exit(1)
    return concept_id, m.group(1)


def ensure_new_iter(concept_id: str, created_iters: dict[str, Path]) -> Path:
    """Create a new iter-NN+1/sources/ dir for this concept. Idempotent.

    Uses created_iters dict to track already-created dirs within this run
    (so concepts with multiple .orig.md files share one new iter).

    Returns the new sources dir path.
    """
    if concept_id in created_iters:
        return created_iters[concept_id]

    concept_dir = RESEARCH_DIR / concept_id
    existing = sorted(concept_dir.glob("iter-*"))
    if existing:
        latest = existing[-1]
        latest_sources = latest / "sources"
        # Reuse latest iter if its sources/ dir is empty (no .md files yet)
        if latest_sources.exists() and not list(latest_sources.glob("*.md")):
            created_iters[concept_id] = latest_sources
            return latest_sources
        latest_num = int(latest.name.split("-")[1])
        new_num = latest_num + 1
    else:
        new_num = 1

    new_dir = concept_dir / f"iter-{new_num:02d}" / "sources"
    new_dir.mkdir(parents=True, exist_ok=True)
    created_iters[concept_id] = new_dir
    return new_dir


def parse_agent_output(output_path: Path) -> dict:
    """Read and parse agent output JSON. Gracefully handles missing/malformed."""
    if not output_path.exists():
        return {"error": "output file not found"}
    try:
        text = output_path.read_text(encoding="utf-8")
        return json.loads(text)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {"error": f"failed to parse output: {e}"}


def process_one(
    orig_path: Path,
    new_sources_dir: Path,
    template_text: str,
    args: argparse.Namespace,
) -> dict:
    """Process a single .orig.md file. Returns result dict."""
    concept_id, concept_num = parse_concept_from_path(orig_path)
    stem = orig_path.stem.replace(".orig", "")  # e.g. "first-light-fusion-technology"
    report_name = f"{concept_num}-{stem}"
    report_path = REPORT_DIR / f"{report_name}.json"

    # Read .orig.md content
    content = orig_path.read_text(encoding="utf-8")

    # Output path for agent JSON (in /tmp to avoid clutter)
    output_path = Path(f"/tmp/resurface/{report_name}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build prompt from template
    prompt = fill_template(template_text, {
        "orig_filename": orig_path.name,
        "orig_content": content,
        "concept_num": concept_num,
        "concept_id": concept_id,
        "max_extractions": str(args.max_extractions),
        "output_path": str(output_path),
    })

    # Save prompt (audit trail)
    prompt_path = REPORT_DIR / f"{report_name}.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run: saved prompt to {prompt_path.name}")
        return {
            "status": "dry-run",
            "orig_path": str(orig_path),
            "concept_id": concept_id,
            "prompt_saved": str(prompt_path),
        }

    # Snapshot current sources before agent invocation
    pre_sources = set(str(s) for s in find_sources(concept_id))

    # Invoke agent
    print(f"  invoking claude ({args.model or 'default'})...")
    t0 = time.time()
    stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0
    print(f"  done in {elapsed:.0f}s (rc={rc})")

    # Detect acquired sources via filesystem diff
    post_sources = set(str(s) for s in find_sources(concept_id))
    acquired = sorted(post_sources - pre_sources)

    # Parse agent output JSON
    agent_report = parse_agent_output(output_path)

    # Build result
    result = {
        "status": "complete",
        "orig_path": str(orig_path),
        "concept_id": concept_id,
        "concept_num": concept_num,
        "elapsed_s": round(elapsed, 1),
        "return_code": rc,
        "acquired": acquired,
        "acquired_count": len(acquired),
        "agent_report": agent_report,
        "recommendation": agent_report.get("recommendation", "unknown"),
    }

    # Save per-file report
    report_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"  acquired {len(acquired)} source(s), recommendation: {result['recommendation']}")

    return result


def discover_orig_files() -> list[Path]:
    """Glob for all .orig.md files under concept_research."""
    paths = sorted(RESEARCH_DIR.glob("**/iter-*/sources/*.orig.md"))
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Re-source .orig.md files via claude -p agent"
    )
    parser.add_argument("files", nargs="*", default=[],
                        help=".orig.md file paths to process")
    parser.add_argument("--all", action="store_true",
                        help="Discover and process all .orig.md files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Save prompts without invoking Claude")
    parser.add_argument("--max-extractions", type=int, default=5,
                        help="Max source extractions per file (default: 5)")
    parser.add_argument("--model", type=str, default=None,
                        help="Claude model to use (default: sonnet)")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Per-file timeout in seconds (default: 600)")
    parser.add_argument("--force", action="store_true",
                        help="Reprocess files even if report exists")

    args = parser.parse_args()

    if not args.all and not args.files:
        parser.error("provide .orig.md file paths or use --all")

    # Discover or validate files
    if args.all:
        orig_paths = discover_orig_files()
    else:
        from lib.paths import REPO_ROOT
        orig_paths = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                # Try relative to CWD first, then repo root
                if p.exists():
                    p = p.resolve()
                elif (REPO_ROOT / p).exists():
                    p = (REPO_ROOT / p).resolve()
                else:
                    p = p.resolve()  # will fail existence check below
            if not p.exists():
                print(f"error: file not found: {p}")
                sys.exit(1)
            if not p.name.endswith(".orig.md"):
                print(f"error: not a .orig.md file: {p}")
                sys.exit(1)
            orig_paths.append(p)

    if not orig_paths:
        print("No .orig.md files found.")
        return

    # Group by concept
    by_concept: dict[str, list[Path]] = {}
    for p in orig_paths:
        cid, _ = parse_concept_from_path(p)
        by_concept.setdefault(cid, []).append(p)

    print(f"Found {len(orig_paths)} .orig.md file(s) across {len(by_concept)} concept(s)")

    # Load prompt template
    if not TEMPLATE_PATH.exists():
        if args.dry_run:
            # Use a placeholder for dry-run if template not yet created
            template_text = "{{orig_content}}\n\n[TEMPLATE NOT YET CREATED — Phase 2]"
            print("warning: prompt template not found, using placeholder for dry-run")
        else:
            print(f"error: prompt template not found: {TEMPLATE_PATH}")
            sys.exit(1)
    else:
        template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Create report directory
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Process each concept's files
    created_iters: dict[str, Path] = {}
    results = []

    for concept_id in sorted(by_concept.keys()):
        files = by_concept[concept_id]
        new_sources_dir = None  # Defer iter creation until needed

        for orig_path in files:
            concept_num = parse_concept_from_path(orig_path)[1]
            stem = orig_path.stem.replace(".orig", "")
            report_name = f"{concept_num}-{stem}"

            # Check resumability before creating iter dir
            report_path = REPORT_DIR / f"{report_name}.json"
            if report_path.exists() and not args.force:
                try:
                    existing = json.loads(report_path.read_text(encoding="utf-8"))
                    if existing.get("status") == "complete":
                        print(f"  skip (existing report): {orig_path.name}")
                        results.append({"status": "skipped", "orig_path": str(orig_path),
                                        "concept_id": concept_id, "reason": "existing report"})
                        continue
                except (json.JSONDecodeError, KeyError):
                    pass

            # Create iter dir on first non-skipped file
            if new_sources_dir is None:
                new_sources_dir = ensure_new_iter(concept_id, created_iters)
                print(f"\n{concept_id}: new iter at {new_sources_dir.parent.name}/ ({len(files)} file(s))")

            print(f"  processing: {orig_path.name}")
            result = process_one(orig_path, new_sources_dir, template_text, args)
            results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")

    statuses = {}
    total_acquired = 0
    for r in results:
        s = r.get("status", "unknown")
        statuses[s] = statuses.get(s, 0) + 1
        total_acquired += r.get("acquired_count", 0)

    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")
    if total_acquired:
        print(f"  total sources acquired: {total_acquired}")

    # Recommendation breakdown (for completed results)
    recs = {}
    for r in results:
        if r.get("status") == "complete":
            rec = r.get("recommendation", "unknown")
            recs[rec] = recs.get(rec, 0) + 1
    if recs:
        print(f"\nRecommendations:")
        for rec, count in sorted(recs.items()):
            print(f"  {rec}: {count}")

    # Write summary JSON
    summary_path = REPORT_DIR / "summary.json"
    summary = {
        "total_files": len(orig_paths),
        "total_concepts": len(by_concept),
        "statuses": statuses,
        "total_acquired": total_acquired,
        "recommendations": recs,
        "results": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSummary written to: {summary_path}")


if __name__ == "__main__":
    main()
