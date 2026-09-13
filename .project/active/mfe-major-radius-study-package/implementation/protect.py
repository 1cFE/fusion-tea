"""Record protected tracked surfaces and all generated package bytes."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
out = Path(__file__).parent
paths = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
owned = [
    "exploration/stellarator_e2e/verify_stellaris.py",
    "exploration/stellarator_e2e/studies/oracle_entry.py",
    "exploration/stellarator_e2e/studies/study_route.py",
    "exploration/stellarator_e2e/studies/manifest.json",
    "exploration/stellarator_e2e/studies/ANNEX.md",
]
paths = [
    p
    for p in paths
    if p
    and p not in owned
    and not p.startswith("knowledge/holdout/")
    and not p.startswith(("tests/study/", ".project/active/mfe-major-radius-study-package/"))
]
paths += [
    str(p)
    for p in Path("exploration/stellarator_e2e/generated").rglob("*")
    if p.is_file() and "__pycache__" not in p.parts
]
result = {
    p: hashlib.sha256((root / p).read_bytes()).hexdigest()
    for p in sorted(set(paths))
    if (root / p).is_file()
}
if sys.argv[1] == "before":
    (out / "protected-before.json").write_text(json.dumps(result, indent=2) + "\n")
else:
    before = {
        p: digest
        for p, digest in json.loads((out / "protected-before.json").read_text()).items()
        if not p.startswith("knowledge/holdout/")
    }
    delta = {
        p: [before.get(p), result.get(p)]
        for p in before.keys() | result.keys()
        if before.get(p) != result.get(p)
    }
    (out / "protected-after.json").write_text(json.dumps(result, indent=2) + "\n")
    (out / "protected-delta.json").write_text(json.dumps(delta, indent=2) + "\n")
    assert not delta, delta
print(len(result))
