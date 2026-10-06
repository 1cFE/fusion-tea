"""Read-only seal checks and renderer rebuild into a temporary directory."""

import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

from scripts.study import manifest as m

ROOT = Path(__file__).resolve().parents[6]
RECORD = ROOT / "exploration/stellarator_materials/studies/20260930-magnet-material-plant-map"
REPORT = ROOT / "work/orchestration/goals/magnet-material-comparison/evidence/round2-report"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
snapshot = json.loads((RECORD / "snapshot.json").read_text())
checks, failed, seen = [], [], set()


def walk(value, package_base=None):
    if isinstance(value, dict):
        if "arm_id" in value:
            package_base = ROOT / value["package"]["path"]
        path = value.get("path")
        expected = value.get("sha256") or value.get("digest")
        if isinstance(path, str) and isinstance(expected, str) and len(expected) == 64:
            p = ROOT / path
            if not p.exists():
                p = RECORD / path
            if not p.exists() and package_base is not None:
                p = package_base / path
            key = (str(p), expected)
            if key not in seen:
                seen.add(key)
                if p.is_dir() and value.get("recipe", "").startswith("sha256 over '<name>"):
                    files = sorted(p.glob("*.json"))
                    actual = hashlib.sha256(
                        "".join(f"{f.name} {sha(f)}\n" for f in files).encode()
                    ).hexdigest()
                else:
                    actual = sha(p) if p.is_file() else None
                row = {
                    "path": str(p.relative_to(ROOT)),
                    "expected": expected,
                    "actual": actual,
                    "tracked": str(p.relative_to(ROOT)) in tracked,
                    "match": actual == expected,
                }
                checks.append(row)
                if not row["match"]:
                    failed.append(row)
        for item in value.values():
            walk(item, package_base)
    elif isinstance(value, list):
        for item in value:
            walk(item, package_base)


walk(snapshot)
identities = []
for unit in ("reference", "rebco", "nb3sn"):
    loaded = m.load(RECORD / f"manifest_{unit}.json")
    package = ROOT / loaded.data["package"]["path"]
    computed = m.indicator_input_fingerprint(package)
    m.assert_package_identity(loaded, package)
    m.assert_pin_matches(loaded, computed)
    identities.append(
        {
            "unit": unit,
            "package": str(package.relative_to(ROOT)),
            "pin": computed,
            "semantic": m.read_semantic_fingerprint(package),
            "executable": m.read_executable_fingerprint(package),
        }
    )
spec = importlib.util.spec_from_file_location("report_render", REPORT / "render.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
original = {
    p.name: sha(p)
    for p in REPORT.iterdir()
    if p.suffix in (".csv", ".svg", ".png") or p.name == "provenance.json"
}
rebuild = Path(tempfile.mkdtemp(prefix="magnet-report-pr-"))
renderer.HERE = rebuild
renderer.main()
rebuilt = {name: sha(rebuild / name) for name in original}
assert original == rebuilt, {
    n: (original[n], rebuilt[n]) for n in original if original[n] != rebuilt[n]
}
assert original == {name: sha(REPORT / name) for name in original}
assert not failed, failed
receipt = {
    "snapshot_sha256": sha(RECORD / "snapshot.json"),
    "checks": checks,
    "package_identities": identities,
    "renderer": {
        "temporary_path": str(rebuild),
        "before": original,
        "rebuilt": rebuilt,
        "original_after": original,
        "all_exact": True,
    },
    "outcome": "pass",
}
(Path(__file__).parent / "seal-render-receipt.json").write_text(
    json.dumps(receipt, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "outcome": "pass",
            "hash_checks": len(checks),
            "tracked": sum(c["tracked"] for c in checks),
            "local_or_aggregate": sum(not c["tracked"] for c in checks),
            "renderer_outputs": len(original),
        }
    )
)
