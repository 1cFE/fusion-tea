"""Check the explicitly protected prior model/package/study evidence; not a goal-authority digest gate."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PROTECTED = [
    "models", "exploration/stellarator_e2e", "exploration/aries_integrated",
    "exploration/component_alternatives", "exploration/exchanger_architecture",
    "work/active/WI-096_matched-conversion-subsystems",
    "work/active/WI-097_exchanger-thermal-requirements",
    "work/orchestration/goals/design-study-component-alternatives",
    "work/orchestration/goals/design-study-exchanger-architecture",
]
def digest(path):
    if path.is_symlink():
        return {"symlink": str(path.readlink())}
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    baseline = HERE / "preservation-before.json"
    if args.capture:
        paths = subprocess.check_output(["git", "ls-files", "-z", "--", *PROTECTED], cwd=ROOT).decode().split("\0")
        document = {"protected": {name: digest(ROOT/name) for name in paths if name}, "scope": "Existing tracked files only; new isolated files are permitted."}
    else:
        prior = json.loads(baseline.read_text())["protected"]
        changes = {name: {"before": expected, "after": digest(ROOT/name) if (ROOT/name).exists() or (ROOT/name).is_symlink() else None}
                   for name, expected in prior.items()
                   if not ((ROOT/name).exists() or (ROOT/name).is_symlink()) or digest(ROOT/name) != expected}
        document = {"checked": len(prior), "changes": changes, "pass": not changes}
    with args.out.open("x") as stream:
        json.dump(document, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"path":str(args.out), "checked":len(document.get("protected", {})) or document.get("checked"), "pass":document.get("pass")}))
if __name__ == "__main__":
    main()
