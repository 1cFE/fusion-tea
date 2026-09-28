"""Check every original tracked model/package/study against the pre-change receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASELINE = Path(__file__).with_name("original-preservation-before.json")


def verify() -> dict:
    baseline = json.loads(BASELINE.read_text())
    differences = []
    for row in baseline["files"]:
        path = ROOT / row["path"]
        if path.is_symlink():
            kind, data = "symlink", os.readlink(path).encode()
        elif path.is_file():
            kind, data = "file", path.read_bytes()
        else:
            differences.append({"path": row["path"], "condition": "missing"})
            continue
        digest = hashlib.sha256(data).hexdigest()
        if kind != row["kind"] or digest != row["sha256"]:
            differences.append({"path": row["path"], "expected": row,
                                "actual": {"kind": kind, "sha256": digest}})
    return {"status": "pass" if not differences else "fail",
            "baseline_revision": baseline["revision"],
            "baseline_sha256": hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
            "checked_files": len(baseline["files"]), "differences": differences}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify()
    with args.out.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "differences"}))
    raise SystemExit(0 if result["status"] == "pass" else 1)
