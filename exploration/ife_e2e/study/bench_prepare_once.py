"""W4: prepare-once vs rebuild-per-case benchmark on the real, sealed fusion-tea
IFE package (S5 carry-forward (2)). A recorded measurement, not a tuning target.

Run:  uv run python exploration/ife_e2e/study/bench_prepare_once.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader

from run_viability_study import (  # noqa: E402
    ETA_FIELD, ETA_GRID, G_GRID, GAIN_FIELD, MultiChannelEvaluator, PACKAGE_DIR, PACKAGE_NAME,
)

N = 200
LINK_ROOT = Path("/tmp/ife_bench_pkg_link")


def _points(n: int) -> list[tuple[float, float]]:
    pts = []
    for i in range(n):
        pts.append((ETA_GRID[i % len(ETA_GRID)], G_GRID[i % len(G_GRID)]))
    return pts


def main() -> None:
    loader = ProvisionalPackageLoader(
        package_dir=PACKAGE_DIR, package_name=PACKAGE_NAME, link_root=LINK_ROOT
    )
    module, _ = loader.load()
    module.ToyPlantParams = module.IfePlantParams
    prepared = PreparedEvaluator(loader, PACKAGE_DIR / "pipelines" / "ife_hif.yaml")
    evaluator = MultiChannelEvaluator(prepared, PACKAGE_DIR, prepared.package)
    points = _points(N)

    # Prepare-once: PreparedEvaluator built once above; evaluate N cases against it.
    t0 = time.perf_counter()
    prepared_verdicts = []
    for eta, gain in points:
        typed = {"ife_plant_params": prepared.package.IfePlantParams(**{
            ETA_FIELD: eta, GAIN_FIELD: gain,
        })}
        evidence = evaluator.evaluate(typed)
        prepared_verdicts.append(evidence.responses)
    prepared_elapsed = time.perf_counter() - t0

    # Rebuild-per-case: construct a fresh PreparedEvaluator (full topology + write-handler
    # validation) for every single case — the naive alternative prepare-once replaces.
    t0 = time.perf_counter()
    rebuild_verdicts = []
    for eta, gain in points:
        loader_i = ProvisionalPackageLoader(
            package_dir=PACKAGE_DIR, package_name=PACKAGE_NAME, link_root=LINK_ROOT
        )
        module_i, _ = loader_i.load()
        module_i.ToyPlantParams = module_i.IfePlantParams
        prepared_i = PreparedEvaluator(loader_i, PACKAGE_DIR / "pipelines" / "ife_hif.yaml")
        evaluator_i = MultiChannelEvaluator(prepared_i, PACKAGE_DIR, prepared_i.package)
        typed = {"ife_plant_params": prepared_i.package.IfePlantParams(**{
            ETA_FIELD: eta, GAIN_FIELD: gain,
        })}
        evidence = evaluator_i.evaluate(typed)
        rebuild_verdicts.append(evidence.responses)
    rebuild_elapsed = time.perf_counter() - t0

    parity = sum(1 for a, b in zip(prepared_verdicts, rebuild_verdicts) if a == b)
    report = {
        "n": N,
        "prepared_total_s": prepared_elapsed,
        "prepared_ms_per_case": 1000 * prepared_elapsed / N,
        "rebuild_total_s": rebuild_elapsed,
        "rebuild_ms_per_case": 1000 * rebuild_elapsed / N,
        "prepare_once_speedup_over_rebuild": rebuild_elapsed / prepared_elapsed,
        "verdict_parity_cases": parity,
    }
    print(json.dumps(report, indent=2))
    out = Path(__file__).parent / "prepare_once_benchmark.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
