"""Execute one point on a package copy through the study route and write channels + verdicts.

usage: proto_baseline.py <package_dir> <work_dir> <point.json> <out.json> [<channels.json>]
"""
import json, sys
from pathlib import Path

REPO = Path("/home/reid/1cfe/fusion-tea")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration/stellarator_e2e/studies"))
import study_route as sr  # noqa: E402

pkg, work, point_path, out_path = (Path(a) for a in sys.argv[1:5])
point = json.loads(point_path.read_text())
channels = json.loads(Path(sys.argv[5]).read_text()) if len(sys.argv) > 5 else sr.CHANNELS
cases, db = sr.run_points("proto-baseline-v1", [point], work, pkg, required_channels=channels)
case = sr._completed(cases, "baseline point")[0]
catalog = sr._catalog_by_constraint_id(pkg)
out = {
    "executable_fingerprint": case.executable_fingerprint,
    "point": point,
    "channels": {k: float(v) for k, v in sorted(case.outputs.items())},
    "verdicts": {catalog[c]["source_local_identity"]: s for c, s in sorted(case.verdicts.items())},
}
out_path.write_text(json.dumps(out, indent=1, sort_keys=True))
print("channels", len(out["channels"]), "verdicts", len(out["verdicts"]), "fingerprint", case.executable_fingerprint[:16])
