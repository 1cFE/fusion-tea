#!/usr/bin/env bash
# Spike probe (throwaway): does recapturing the instance-graph snapshot from the
# same models path differ from the tracked stellarator.snapshot.json only in
# `captured_at` (design.md bet B2)?
#
# Never writes the real repo tree. Captures are written into /tmp only. The real
# models/ directory is READ from (that is what gate 4 does); a scratch copy of
# models/ is also captured from, to detect any sensitivity to the models path.
set -uo pipefail

REPO=/home/reid/1cfe/fusion-tea
BASE=${BASE:-/tmp/spike-snap/$(git -C "$REPO" rev-parse --short HEAD)}
OUT="$BASE/out"
SCRATCH="$BASE/models"
SRC="$REPO/exploration/stellarator_e2e"
TRACKED="$SRC/stellarator.snapshot.json"

rm -rf "$BASE"; mkdir -p "$OUT" "$SCRATCH"
set -a; source /home/reid/1cfe/agentic-mbse/.env; set +a
echo "== env: SYSIDE_LICENSE_KEY ${SYSIDE_LICENSE_KEY:+set}${SYSIDE_LICENSE_KEY:-UNSET}" | sed 's/=.*set/= set/'

echo "== 0. stage a scratch copy of models/"
rsync -a --exclude '__pycache__' "$SRC/models/" "$SCRATCH/"

capture () {  # $1 = label, $2 = models root
  echo "== capture ($1) from $2"
  ( cd "$REPO" && /usr/bin/time -f "   wall=%es" \
    uv run python -c "
from pathlib import Path
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
capture_instance_graph_snapshot([Path('$2')], Path('$OUT/$1.snapshot.json'))
print('captured')
" ) > "$OUT/cap_$1.log" 2>&1
  echo "   exit=$? ; log=$OUT/cap_$1.log"
  tail -6 "$OUT/cap_$1.log" | sed 's/^/   | /'
  [ -f "$OUT/$1.snapshot.json" ] && sha256sum "$OUT/$1.snapshot.json" | sed 's/^/   sha256 /'
}

# Gate 4's own shape: recapture from the REAL models root (read-only).
capture real1 "$SRC/models"
capture real2 "$SRC/models"
# Path-sensitivity control: same content, different absolute path.
capture scratch1 "$SCRATCH"

echo
echo "== byte comparison against tracked $TRACKED"
sha256sum "$TRACKED" | sed 's/^/   tracked /'
for f in real1 real2 scratch1; do
  [ -f "$OUT/$f.snapshot.json" ] || { echo "   $f: MISSING (capture failed)"; continue; }
  if cmp -s "$TRACKED" "$OUT/$f.snapshot.json"; then
    echo "   $f vs tracked: BYTE-IDENTICAL"
  else
    echo "   $f vs tracked: BYTES DIFFER ($(stat -c%s "$TRACKED") vs $(stat -c%s "$OUT/$f.snapshot.json") bytes)"
  fi
done
cmp -s "$OUT/real1.snapshot.json" "$OUT/real2.snapshot.json" \
  && echo "   real1 vs real2: BYTE-IDENTICAL (recapture-vs-recapture stable)" \
  || echo "   real1 vs real2: BYTES DIFFER"
cmp -s "$OUT/real1.snapshot.json" "$OUT/scratch1.snapshot.json" \
  && echo "   real1 vs scratch1: BYTE-IDENTICAL (models path does not leak)" \
  || echo "   real1 vs scratch1: BYTES DIFFER (models path leaks into the snapshot)"

echo
echo "== key-by-key deep diff (every differing key path, fully recursive)"
uv run python - "$TRACKED" "$OUT/real1.snapshot.json" "$OUT/real2.snapshot.json" "$OUT/scratch1.snapshot.json" <<'PY' | tee "$OUT/keydiff.txt"
import json, sys, itertools
from pathlib import Path

def load(p): return json.loads(Path(p).read_text())

def diff(a, b, path=""):
    """Yield (keypath, kind, a_repr, b_repr) for every leaf that differs."""
    if type(a) is not type(b):
        yield (path or ".", "type", type(a).__name__, type(b).__name__); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            p = f"{path}.{k}"
            if k not in a: yield (p, "only-in-B", "<absent>", repr(b[k])[:120])
            elif k not in b: yield (p, "only-in-A", repr(a[k])[:120], "<absent>")
            else: yield from diff(a[k], b[k], p)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield (path, "length", str(len(a)), str(len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            yield from diff(x, y, f"{path}[{i}]")
    elif a != b:
        yield (path, "value", repr(a)[:120], repr(b)[:120])

tracked = load(sys.argv[1])
for label, p in zip(("real1", "real2", "scratch1"), sys.argv[2:]):
    if not Path(p).exists():
        print(f"\n--- tracked vs {label}: capture MISSING"); continue
    got = load(p)
    ds = list(diff(tracked, got))
    print(f"\n--- tracked vs {label}: {len(ds)} differing key path(s)")
    for kp, kind, x, y in ds[:200]:
        print(f"    {kp}  [{kind}]  tracked={x}  {label}={y}")
    if len(ds) > 200: print(f"    ... and {len(ds)-200} more")

r1, r2 = load(sys.argv[2]), load(sys.argv[3])
ds = list(diff(r1, r2))
print(f"\n--- real1 vs real2: {len(ds)} differing key path(s)")
for kp, kind, x, y in ds[:200]: print(f"    {kp}  [{kind}]  real1={x}  real2={y}")

print("\n--- top-level key sets")
print(f"    tracked : {sorted(tracked)}")
print(f"    real1   : {sorted(r1)}")
print(f"    'captured_at' present anywhere in tracked : {'captured_at' in Path(sys.argv[1]).read_text()}")
print(f"    'captured_at' present anywhere in real1   : {'captured_at' in Path(sys.argv[2]).read_text()}")
PY

echo
echo "== artifacts in $OUT"
