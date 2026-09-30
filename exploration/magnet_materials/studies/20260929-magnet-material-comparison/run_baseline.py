"""Step 5: load the stock route and execute the record manifest's pinned baseline point into results/.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/run_baseline.py'
"""
from __future__ import annotations

import json
from pathlib import Path

from exploration.magnet_materials.studies import study_route as route

RECORD = Path(__file__).resolve().parent

if __name__ == "__main__":
    out = RECORD / "results"
    for name in ("package_identity.json", "baseline_result.json"):
        if (out / name).exists():
            raise route.RouteError(f"{name} already exists; preserve evidence")
    deposited = route.execute_baseline(out, package_dir=route.PACKAGE_DIR, manifest_path=RECORD / "manifest.json")
    result = json.loads(Path(deposited["baseline_result"]).read_text())
    print(json.dumps({k: str(v) for k, v in deposited.items()}))
    print("headline", result["channels"]["magnet_subsystem__subsystem__pair__cost_difference"])
    print("store", result["executed_under"]["store_id"])
    print("verdicts", {v["source_local_identity"] + "@" + v["constraint_id"].split("__")[3]: v["status"] for v in result["verdicts"]})
