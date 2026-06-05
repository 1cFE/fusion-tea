#!/usr/bin/env python3
"""Parallel batch runner for concept regeneration (Item 11).

Fans out ``analyze --max-passes N`` then ``model-critic`` across an **explicit,
operator-supplied** concept list, reusing the scoring pipeline's
``ProcessPoolExecutor`` machinery (``run_parallel_stage`` / ``run_for_concept``).
The run **stops after the critic** — a human checkpoint, not the full chain.

There is deliberately no run-all default and no automation of downstream stages
(review / synthesize / score / approve); see spec FR-4.

Usage:
    uv run python scripts/run_regen_batch.py 01-hts-compact-tokamak 07-foo
    uv run python scripts/run_regen_batch.py 01-hts-compact-tokamak --max-passes 5 --workers 4
    uv run python scripts/run_regen_batch.py 01-hts-compact-tokamak --model opus
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime

from lib.parallel_stage import run_parallel_stage

# Batch stages, in order. Stops after model-critic (FR-4) — no downstream chain.
STAGES = ["analyze", "model-critic"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_regen_batch.py",
        description="Parallel analyze + model-critic over an explicit concept list",
    )
    # Required: explicit concept list. nargs="+" => argparse errors on empty
    # input, which is the FR-4 "no run-all default" guarantee.
    parser.add_argument("concepts", nargs="+", help="Explicit concept IDs to regenerate")
    parser.add_argument("--workers", type=int, default=3,
                        help="Number of parallel workers (default: 3, matches scoring runner)")
    parser.add_argument("--max-passes", type=int, default=3,
                        help="Max analyze→assess iterations per concept (default: 3)")
    parser.add_argument("--model", default="sonnet",
                        help="Claude model (default: sonnet)")
    parser.add_argument("--timeout", type=int, default=900,
                        help="Per-invocation timeout in seconds (default: 900)")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    concept_ids = args.concepts

    print("Fusion TEA Concept Regeneration Batch")
    print(f"  Concepts: {len(concept_ids)} — {', '.join(concept_ids)}")
    print(f"  Workers: {args.workers}")
    print(f"  Model: {args.model}")
    print(f"  Max passes (analyze): {args.max_passes}")
    print(f"  Stages: {' → '.join(STAGES)} (stops after critic)")
    print(f"  Started: {datetime.now().isoformat()}")

    batch_start = time.time()
    all_failures: dict[str, list[str]] = {}

    for stage in STAGES:
        # max_passes is only consumed by the analyze stage's stage_flags(); it is
        # ignored (None-equivalent) for model-critic.
        mp = args.max_passes if stage == "analyze" else None
        _, failed = run_parallel_stage(
            concept_ids, stage, args.workers, args.model, args.timeout, mp,
        )
        all_failures[stage] = failed

    elapsed = time.time() - batch_start
    print(f"\n{'='*70}")
    print(f"Batch complete: {elapsed:.0f}s")
    print(f"Finished: {datetime.now().isoformat()}")

    total_failures = sum(len(v) for v in all_failures.values())
    if total_failures:
        print(f"\nFailures ({total_failures} total):")
        for stage, fails in all_failures.items():
            if fails:
                print(f"  {stage}: {', '.join(fails)}")
        return 1
    print("\nAll concepts passed analyze + model-critic. Ready for human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
