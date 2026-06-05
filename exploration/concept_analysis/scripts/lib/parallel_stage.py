"""Generic parallel-stage runner for the concept-analysis pipeline.

Extracted from the now-deleted ``run_scoring_pipeline.py`` so ``run_regen_batch.py``
and ``test_regen_batch.py`` can still fan out ``analyze`` and ``model-critic`` over
an explicit concept list without depending on any scoring infrastructure.
"""
from __future__ import annotations

import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
RUN_ANALYSIS = SCRIPT_DIR / "run_analysis.py"


def stage_flags(stage: str, max_passes: int | None = None) -> list[str]:
    """Per-stage subprocess flags appended after the common ``--model``/``--timeout``.

    - ``analyze`` cold-starts cleanly (``--force``) and carries ``--max-passes``.
    - ``model-critic`` takes NEITHER ``--force`` nor ``--max-passes`` (its
      argparser rejects ``--force``), so it gets no extra flags.
    """
    if stage == "analyze":
        return ["--force", "--max-passes", str(max_passes if max_passes is not None else 3)]
    if stage == "model-critic":
        return []
    raise ValueError(f"Unsupported stage: {stage!r}")


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
            cmd, capture_output=True, text=True, timeout=timeout + 120,
            encoding="utf-8",
        )
        output = (result.stdout or "") + (result.stderr or "")
        return concept_id, output, result.returncode == 0
    except subprocess.TimeoutExpired as e:
        output = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        output += f"\nTIMEOUT after {timeout + 120}s"
        return concept_id, output, False


def run_parallel_stage(
    concept_ids: list[str],
    stage: str,
    workers: int,
    model: str,
    timeout: int,
    max_passes: int | None = None,
) -> tuple[list[str], list[str]]:
    """Run a stage in parallel batches. Returns (succeeded, failed) concept IDs."""
    succeeded: list[str] = []
    failed: list[str] = []
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
                    for line in output.splitlines()[-5:]:
                        line = line.strip()
                        if line:
                            print(f"    {line}")
                    failed.append(concept_id)
                else:
                    succeeded.append(concept_id)
            except Exception as e:
                print(f"  [{i}/{total}] {cid}: ERROR {e}")
                failed.append(cid)

    elapsed = time.time() - stage_start
    print(f"\n  {stage} complete: {len(succeeded)} succeeded, {len(failed)} failed ({elapsed:.0f}s)")
    if failed:
        print(f"  Failed: {', '.join(failed)}")

    return succeeded, failed
