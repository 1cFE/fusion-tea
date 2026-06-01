#!/usr/bin/env python3
"""Full scoring pipeline runner with parallel batch execution.

Orchestrates: synthesize → score → extract-scores → calibrate → heatmap
with configurable parallelism for the Claude-calling stages.

Usage:
    uv run python scripts/run_scoring_pipeline.py
    uv run python scripts/run_scoring_pipeline.py --workers 4
    uv run python scripts/run_scoring_pipeline.py --workers 4 --model sonnet
    uv run python scripts/run_scoring_pipeline.py --dry-run
    uv run python scripts/run_scoring_pipeline.py --stage score  # resume from score stage
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RUN_ANALYSIS = SCRIPT_DIR / "run_analysis.py"
ANALYSES_DIR = SCRIPT_DIR.parent / "analyses"
SCORES_DIR = SCRIPT_DIR.parent / "scores"

# Stages in pipeline order.
# "synthesize" now produces Section 8 with YAML scores block (no separate "score" step needed).
# "score" is available for legacy syntheses that lack Section 8.
STAGES = ["synthesize", "extract-scores", "calibrate", "heatmap"]


def get_concept_ids() -> list[str]:
    """Get all concept IDs that have analysis.md files."""
    ids = []
    for d in sorted(ANALYSES_DIR.iterdir()):
        if d.is_dir() and (d / "analysis.md").exists():
            ids.append(d.name)
    return ids


def stage_flags(stage: str, max_passes: int | None = None) -> list[str]:
    """Per-stage subprocess flags appended after the common ``--model``/``--timeout``.

    Scoring stages (synthesize and friends) keep their historical ``--force`` —
    and synthesize additionally keeps ``--skip-review-gate`` — so the existing
    scoring pipeline's subprocess invocation is unchanged. The Item 11 batch
    stages diverge:

    - ``analyze`` cold-starts cleanly (``--force``) and carries ``--max-passes``.
    - ``model-critic`` takes NEITHER ``--force`` nor ``--max-passes`` (its
      argparser rejects ``--force``), so it gets no extra flags.
    """
    if stage == "analyze":
        return ["--force", "--max-passes", str(max_passes if max_passes is not None else 3)]
    if stage == "model-critic":
        return []
    # Scoring stages: --force everywhere, --skip-review-gate only for synthesize.
    flags = ["--force"]
    if stage == "synthesize":
        flags.append("--skip-review-gate")
    return flags


def run_for_concept(
    concept_id: str, stage: str, model: str, timeout: int,
    max_passes: int | None = None,
) -> tuple[str, str, bool]:
    """Run a pipeline stage for a single concept. Returns (concept_id, output, success)."""
    cmd = [
        "uv", "run", "python", str(RUN_ANALYSIS),
        stage, concept_id,
        "--model", model,
        "--timeout", str(timeout),
        *stage_flags(stage, max_passes),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(SCRIPT_DIR),
            timeout=timeout + 120,  # subprocess timeout > Claude timeout
        )
        output = result.stdout + result.stderr
        # Check for synthesis/score-level failure — ignore model_setup warnings
        # which contain "FAILED" in non-fatal model run messages.
        has_stage_failure = False
        for line in result.stdout.splitlines():
            stripped = line.strip()
            if stripped.startswith(f"  {stage}") and "FAILED" in stripped:
                has_stage_failure = True
                break
            if "validation exhausted" in stripped:
                has_stage_failure = True
                break
        success = result.returncode == 0 and not has_stage_failure
        return concept_id, output, success
    except subprocess.TimeoutExpired:
        return concept_id, f"TIMEOUT after {timeout + 120}s", False
    except Exception as e:
        return concept_id, f"ERROR: {e}", False


def run_parallel_stage(
    concept_ids: list[str],
    stage: str,
    workers: int,
    model: str,
    timeout: int,
    max_passes: int | None = None,
) -> tuple[list[str], list[str]]:
    """Run a stage in parallel batches. Returns (succeeded, failed) concept IDs."""
    succeeded = []
    failed = []
    total = len(concept_ids)

    print(f"\n{'='*70}")
    print(f"Stage: {stage} | {total} concepts | {workers} workers | model: {model}")
    print(f"{'='*70}")

    stage_start = time.time()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(run_for_concept, cid, stage, model, timeout, max_passes): cid
            for cid in concept_ids
        }

        for i, future in enumerate(as_completed(futures), 1):
            cid = futures[future]
            try:
                concept_id, output, success = future.result()
                status = "OK" if success else "FAILED"
                elapsed = time.time() - stage_start
                print(f"  [{i}/{total}] {concept_id}: {status} ({elapsed:.0f}s elapsed)")

                if not success:
                    # Print failure details (truncated)
                    for line in output.splitlines()[-5:]:
                        line = line.strip()
                        if line:
                            print(f"    {line}")
                    failed.append(concept_id)
                else:
                    succeeded.append(concept_id)
            except Exception as e:
                print(f"  [{i}/{total}] {cid}: EXCEPTION: {e}")
                failed.append(cid)

    elapsed = time.time() - stage_start
    print(f"\n  {stage} complete: {len(succeeded)} succeeded, {len(failed)} failed ({elapsed:.0f}s)")
    if failed:
        print(f"  Failed: {', '.join(failed)}")

    return succeeded, failed


def run_sequential_stage(stage: str, model: str, timeout: int, extra_args: list[str] | None = None) -> bool:
    """Run a non-parallelizable stage. Returns success."""
    print(f"\n{'='*70}")
    print(f"Stage: {stage} (sequential)")
    print(f"{'='*70}")

    cmd = [
        "uv", "run", "python", str(RUN_ANALYSIS),
        stage,
    ]
    if extra_args:
        cmd.extend(extra_args)
    if stage in ("calibrate",):
        cmd.extend(["--model", model, "--timeout", str(timeout)])

    t0 = time.time()
    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR), timeout=timeout + 120,
                           encoding="utf-8")
    elapsed = time.time() - t0

    success = result.returncode == 0
    status = "OK" if success else "FAILED"
    print(f"  {stage}: {status} ({elapsed:.0f}s)")
    return success


def main():
    parser = argparse.ArgumentParser(
        description="Full scoring pipeline with parallel execution"
    )
    parser.add_argument("--workers", type=int, default=3,
                       help="Number of parallel workers (default: 3)")
    parser.add_argument("--model", default="sonnet",
                       help="Claude model (default: sonnet)")
    parser.add_argument("--synth-timeout", type=int, default=1200,
                       help="Timeout per synthesize call (default: 1200s)")
    parser.add_argument("--calibrate-timeout", type=int, default=3600,
                       help="Timeout for calibration call (default: 3600s)")
    parser.add_argument("--stage", choices=STAGES,
                       help="Resume from this stage (skip earlier stages)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Print what would be done without executing")
    args = parser.parse_args()

    concept_ids = get_concept_ids()
    start_stage = STAGES.index(args.stage) if args.stage else 0

    print(f"Fusion TEA Scoring Pipeline")
    print(f"  Concepts: {len(concept_ids)}")
    print(f"  Workers: {args.workers}")
    print(f"  Model: {args.model}")
    print(f"  Start stage: {STAGES[start_stage]}")
    print(f"  Started: {datetime.now().isoformat()}")

    if args.dry_run:
        print("\n  DRY RUN — no commands will be executed")
        for stage in STAGES[start_stage:]:
            print(f"\n  Would run: {stage}")
            if stage in ("synthesize", "score"):
                print(f"    {len(concept_ids)} concepts in parallel ({args.workers} workers)")
            else:
                print(f"    Sequential")
        return

    pipeline_start = time.time()
    all_failures = {}

    # Stage 1: Synthesize (parallel) — now includes Section 8 with YAML scores
    if start_stage <= 0:
        succeeded, failed = run_parallel_stage(
            concept_ids, "synthesize", args.workers, args.model, args.synth_timeout,
        )
        all_failures["synthesize"] = failed

    # Stage 2: Extract scores (sequential, no Claude)
    if start_stage <= 1:
        ok = run_sequential_stage("extract-scores", args.model, 60)
        if not ok:
            print("\nERROR: extract-scores failed. Stopping pipeline.")
            _print_summary(pipeline_start, all_failures)
            sys.exit(1)

    # Stage 3: Calibrate (sequential, single Claude call)
    if start_stage <= 2:
        ok = run_sequential_stage("calibrate", args.model, args.calibrate_timeout)
        if not ok:
            print("\nERROR: calibrate failed. Stopping pipeline.")
            _print_summary(pipeline_start, all_failures)
            sys.exit(1)

    # Stage 4: Heatmap (sequential, no Claude)
    if start_stage <= 3:
        ok = run_sequential_stage("heatmap", args.model, 60)
        if not ok:
            print("\nERROR: heatmap failed.")

    _print_summary(pipeline_start, all_failures)


def get_concepts_with_synthesis() -> list[str]:
    """Get concept IDs that have synthesis.md files."""
    ids = []
    for d in sorted(ANALYSES_DIR.iterdir()):
        if d.is_dir() and (d / "synthesis.md").exists():
            ids.append(d.name)
    return ids


def _print_summary(pipeline_start: float, all_failures: dict):
    """Print final pipeline summary."""
    elapsed = time.time() - pipeline_start
    hours = elapsed / 3600
    print(f"\n{'='*70}")
    print(f"Pipeline complete: {hours:.1f} hours")
    print(f"Finished: {datetime.now().isoformat()}")

    total_failures = sum(len(v) for v in all_failures.values())
    if total_failures:
        print(f"\nFailures ({total_failures} total):")
        for stage, fails in all_failures.items():
            if fails:
                print(f"  {stage}: {', '.join(fails)}")
    else:
        print("\nAll stages succeeded.")

    # Check outputs
    scores_dir = SCRIPT_DIR.parent / "scores"
    heatmap = SCRIPT_DIR.parent / "heatmap.html"
    if (scores_dir / "calibrated_scores.json").exists():
        print(f"\nOutputs:")
        print(f"  Verified scores: {scores_dir / 'verified_scores.json'}")
        print(f"  Calibrated scores: {scores_dir / 'calibrated_scores.json'}")
        if heatmap.exists():
            print(f"  Heatmap: {heatmap}")


if __name__ == "__main__":
    main()
