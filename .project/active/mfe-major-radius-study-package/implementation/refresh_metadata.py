"""Reproduce current manifest and known answers from the unchanged native package.

Run from the repository root with the documented TEAx runtime; use a fresh work dir.
This prepares metadata identities. It does not invoke integration or promote a pin.
"""

import argparse
import json
import pprint
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
STUDIES = ROOT / "exploration/stellarator_e2e/studies"
sys.path[:0] = [str(ROOT), str(STUDIES)]
import study_route  # noqa: E402 — runtime import path established above

from scripts.study import manifest  # noqa: E402 — runtime import path established above
from tests.study.conftest import DATA_DIR  # noqa: E402 — runtime import path established above

parser = argparse.ArgumentParser()
parser.add_argument("work_dir", type=Path)
args = parser.parse_args()
path = STUDIES / "manifest.json"
data = json.loads(path.read_text())
package = study_route.PACKAGE_DIR
pin = manifest.indicator_input_fingerprint(package)
data["fingerprints"] = {
    "indicator_inputs": {**pin, "files": [f["path"] for f in pin["files"]]},
    "recorded_provenance": {
        "executable_fingerprint": manifest.read_executable_fingerprint(package),
        "semantic_fingerprint": manifest.read_semantic_fingerprint(package),
    },
}
manifest.validate(data)
path.write_text(json.dumps(data, indent=1) + "\n")
result_paths = study_route.execute_baseline(args.work_dir)
result = json.loads(result_paths["baseline_result"].read_text())
data["baseline"]["headline"]["value"] = result["channels"][data["baseline"]["headline"]["channel"]]
data["baseline"]["verdicts"] = sorted(
    [
        {"source_local_identity": v["source_local_identity"], "expected": v["status"]}
        for v in result["verdicts"]
    ],
    key=lambda v: v["source_local_identity"],
)
manifest.validate(data)
path.write_text(json.dumps(data, indent=1) + "\n")
report = json.loads(
    subprocess.check_output(
        [
            str(ROOT / ".codex-test/run"),
            "python",
            "scripts/study/indicators.py",
            "--package",
            str(package),
            "--manifest",
            str(path),
            "--groups",
            str(DATA_DIR / "axes.known_answers.json"),
        ],
        text=True,
    )
)
for group in report["groups"]:
    fixture = {
        "derived_against_semantic_fingerprint": manifest.read_semantic_fingerprint(package),
        "group": group,
    }
    (DATA_DIR / f"{group['axis']}.expected.json").write_text(json.dumps(fixture, indent=1) + "\n")
(args.work_dir / "known-answers.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"fingerprints": data["fingerprints"], "baseline": data["baseline"]}, indent=2))

contract = {}
for group in report["groups"]:
    contract[group["axis"]] = (
        group["no_constraint_response"],
        sorted(c["source_local_identity"] for c in group["constraints_reachable"]),
        group["objectives_reachable"],
        group["trace_size"]["modules_fired"],
        group["trace_size"]["channels_tainted"],
    )
test = ROOT / "tests/study/test_known_answers.py"
text = test.read_text()
start = text.index("EXPECTED_SEMANTIC_FINGERPRINT = ")
end = text.index("\n", start)
text = (
    text[:start]
    + "EXPECTED_SEMANTIC_FINGERPRINT = "
    + repr(manifest.read_semantic_fingerprint(package))
    + text[end:]
)
start = text.index("FIXTURE_CONTRACT = ")
end = text.index("\n\n", start)
text = text[:start] + "FIXTURE_CONTRACT = " + pprint.pformat(contract, sort_dicts=True) + text[end:]
test.write_text(text)
