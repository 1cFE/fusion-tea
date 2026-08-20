"""Spot-check three mechanical failure paths by running the real CLI."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path("/home/reid/1cfe/fusion-tea-stellarator-mbse-demo")
PKG = ROOT / "exploration/stellarator_e2e/pkg/stellarator_tea"
MAN = ROOT / "exploration/stellarator_e2e/studies/manifest.json"
sys.path.insert(0, str(ROOT))
from scripts.study import manifest as m  # noqa: E402

T = pathlib.Path(tempfile.mkdtemp())


def decl(path, key):
    path.write_text(json.dumps({
        "schema_version": "study-axis-declaration/v1",
        "groups": [{"axis": "probe", "keys": [{"key": key, "provenance": "fan_out"}]}],
    }))
    return path


def run(label, pkg, man, groups):
    out = T / (label + ".json")
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts/study/indicators.py"),
         "--package", str(pkg), "--manifest", str(man),
         "--groups", str(groups), "--out", str(out)],
        capture_output=True, text=True, cwd=ROOT)
    print("=== " + label)
    print("rc          :", p.returncode)
    print("stderr      :", p.stderr.strip())
    print("stdout bytes:", len(p.stdout))
    print("out file    :", "exists" if out.exists() else "absent")
    print()


run("A_absent_key", PKG, MAN, decl(T / "a.json", "stellarator_09__stellaris__geom__NOPE"))
run("B_computed_quantity", PKG, MAN, decl(T / "b.json", "stellarator_09__stellaris__pb__p_net"))

# C: corrupt a pipeline value line in a copy, then re-pin so the fingerprint gate passes.
shutil.copytree(PKG, T / "pkg")
shutil.copy(MAN, T / "manifest.json")
yml = T / "pkg/pipelines/mfe_stellarator.yaml"
text = yml.read_text()
TARGET = "float system_design.stellarator_09__stellaris__geom__R"
assert TARGET in text, "mutation target absent - refusing to pretend the test corrupted anything"
yml.write_text(text.replace(TARGET, "floatonly_one_token", 1))
data = json.loads((T / "manifest.json").read_text())
fp = m.indicator_input_fingerprint(T / "pkg")
data["fingerprints"]["indicator_inputs"]["digest"] = fp["digest"]
data["fingerprints"]["indicator_inputs"]["files"] = sorted(f["path"] for f in fp["files"])
(T / "manifest.json").write_text(json.dumps(data, indent=2))
run("C_corrupt_pipeline_line", T / "pkg", T / "manifest.json",
    ROOT / "tests/study/data/axes.known_answers.json")

print("tmp:", T)
