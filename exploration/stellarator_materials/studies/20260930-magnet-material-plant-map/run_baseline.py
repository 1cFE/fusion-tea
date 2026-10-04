"""Step 5: load each unit's route and execute the record manifest's pinned baseline point into results/.

Deposits results/package_identity_<unit>.json and results/baseline_result_<unit>.json; the stores go to
results/_work/stellarator-materials-<unit>-baseline-r3.db (machine-local, digests in the snapshot).

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/run_baseline.py'
"""
from __future__ import annotations

import json
from pathlib import Path

import record_common as rc
import route_entry

if __name__ == "__main__":
    for unit in rc.UNITS:
        for name in (f"package_identity_{unit}.json", f"baseline_result_{unit}.json"):
            if (rc.RESULTS / name).exists():
                raise FileExistsError(f"{name} already exists; preserve evidence")
        deposited = route_entry.execute_unit_baseline(unit, rc.RESULTS, manifest_path=rc.manifest_path(unit),
                                                      suffix=f"_{unit}")
        result = json.loads(Path(deposited["baseline_result"]).read_text())
        manifest = json.loads(rc.manifest_path(unit).read_text())
        channel = manifest["baseline"]["headline"]["channel"]
        print(unit, "headline", result["channels"][channel], "pinned", manifest["baseline"]["headline"]["value"],
              "store", result["executed_under"]["store_id"],
              "violated", sorted(v["source_local_identity"] for v in result["verdicts"] if v["status"] != "satisfied"))
