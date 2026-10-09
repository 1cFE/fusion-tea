"""Replay retained conversion controls through the strict native development route.

These are model regression tests, separate from the later stock-lifecycle study.
Small output batches bound the development runner's per-case checkpoint writes.
"""
import argparse
import hashlib
import json
from pathlib import Path

from exploration.whole_plant_conversion import run
from exploration.whole_plant_conversion.studies.migrate_controls import migrate

OLD = Path("exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/results/cases.json")
DEFAULTS = Path("work/active/WI-098_whole-plant-conversion-comparison/evidence/development-final/complete-defaults.json")
EXPECTED = "6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f"


def main(out):
    out = Path(out)
    if out.exists():
        raise ValueError("preserve prior control attempts; choose a fresh output directory")
    out.mkdir(parents=True)
    old = json.loads(OLD.read_text())["cases"]
    defaults = json.loads(DEFAULTS.read_text())
    points = [{"case": row["case"], "inputs": migrate(row["inputs"], defaults),
               "predecessor_candidate_id": row["candidate_id"]} for row in old]
    (out / "migrated-controls.json").write_text(json.dumps({"cases": points}, indent=2) + "\n")
    rows = []
    for start in range(0, len(points), 25):
        result = run.execute(points[start:start + 25], out / f"batch-{start // 25:02d}")
        if any(row["executable_fingerprint"] != EXPECTED for row in result):
            raise ValueError("control batch ran a different executable")
        rows.extend(result)
    (out / "cases.json").write_text(json.dumps({"cases": rows}, indent=2) + "\n")
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    summary = {"expected_executable": EXPECTED, "cases": len(rows),
               "completed": sum(row["state"] == "completed" for row in rows),
               "old_cases_sha256": digest(OLD), "new_defaults_sha256": digest(DEFAULTS),
               "migration": "studies/migrate_controls.py; legacy shared finance preserved",
               "native_route": "exploration.whole_plant_conversion.run.execute",
               "scope": "development regression; not the main study"}
    (out / "execution.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)
    if summary["completed"] != len(points):
        raise ValueError("one or more controls failed native evaluation; evidence retained")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    main(parser.parse_args().out)
