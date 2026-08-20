#!/usr/bin/env bash
# Spot-check three mechanical failure paths by running the tool for real.
set -u
ROOT=/home/reid/1cfe/fusion-tea-stellarator-mbse-demo
PKG=$ROOT/exploration/stellarator_e2e/pkg/stellarator_tea
MAN=$ROOT/exploration/stellarator_e2e/studies/manifest.json
T=$(mktemp -d)
cd "$ROOT"

mk_decl () {  # $1 = out file, $2 = key
  cat > "$1" <<EOF
{"schema_version": "study-axis-declaration/v1",
 "groups": [{"axis": "probe", "keys": [{"key": "$2", "provenance": "fan_out"}]}]}
EOF
}

echo "=== A. absent declared key"
mk_decl "$T/a.json" "stellarator_09__stellaris__geom__NOPE"
uv run python scripts/study/indicators.py --package "$PKG" --manifest "$MAN" --groups "$T/a.json" --out "$T/a.out" >"$T/a.stdout" 2>"$T/a.stderr"
echo "rc=$?"; echo "stderr: $(cat "$T/a.stderr")"; echo "stdout bytes: $(wc -c < "$T/a.stdout")"; echo "out file exists: $([ -e "$T/a.out" ] && echo yes || echo no)"

echo
echo "=== B. declared key names a produced channel"
mk_decl "$T/b.json" "stellarator_09__stellaris__pb__p_net"
uv run python scripts/study/indicators.py --package "$PKG" --manifest "$MAN" --groups "$T/b.json" --out "$T/b.out" >"$T/b.stdout" 2>"$T/b.stderr"
echo "rc=$?"; echo "stderr: $(cat "$T/b.stderr")"; echo "stdout bytes: $(wc -c < "$T/b.stdout")"; echo "out file exists: $([ -e "$T/b.out" ] && echo yes || echo no)"

echo
echo "=== C. corrupt pipeline value line (copy + re-pin)"
cp -r "$PKG" "$T/pkg"
cp "$MAN" "$T/manifest.json"
uv run python - "$T/pkg" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "pipelines" / "mfe_stellarator.yaml"
text = p.read_text()
target = "float stellarator_09__stellaris__system_design.stellarator_09__stellaris__geom__R"
assert target in text, "mutation target absent - refusing to pretend"
p.write_text(text.replace(target, "floatonly_one_token", 1))
PY
uv run python - "$T/pkg" "$T/manifest.json" <<'PY'
import sys, json, pathlib
sys.path.insert(0, "/home/reid/1cfe/fusion-tea-stellarator-mbse-demo")
from scripts.study import manifest as m
mp = pathlib.Path(sys.argv[2]); d = json.loads(mp.read_text())
fp = m.indicator_input_fingerprint(sys.argv[1])
d["fingerprints"]["indicator_inputs"]["digest"] = fp["digest"]
d["fingerprints"]["indicator_inputs"]["files"] = sorted(f["path"] for f in fp["files"])
mp.write_text(json.dumps(d, indent=2))
PY
uv run python scripts/study/indicators.py --package "$T/pkg" --manifest "$T/manifest.json" --groups tests/study/data/axes.known_answers.json --out "$T/c.out" >"$T/c.stdout" 2>"$T/c.stderr"
echo "rc=$?"; echo "stderr: $(cat "$T/c.stderr")"; echo "stdout bytes: $(wc -c < "$T/c.stdout")"; echo "out file exists: $([ -e "$T/c.out" ] && echo yes || echo no)"
echo "TMP=$T"
