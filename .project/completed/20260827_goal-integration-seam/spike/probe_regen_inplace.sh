#!/usr/bin/env bash
# Spike probe (throwaway): is `sysml-codegen generate --smart-regen --preserve-handwritten`
# byte-stable when run IN PLACE on an already-sealed package?
#
# Never touches the real repo working tree: it copies the sealed package into a scratch
# git repo and generates with absolute --models/--output paths pointing at the scratch.
set -uo pipefail

REPO=/home/reid/1cfe/fusion-tea
BASE=${BASE:-/tmp/spike-regen/$(git -C "$REPO" rev-parse --short HEAD)}
SCRATCH="$BASE/tree"   # git root: ONLY the package lives here
OUT="$BASE/out"       # probe artifacts live outside the git root
SRC="$REPO/exploration/stellarator_e2e"
PKG="$SCRATCH/stellarator_e2e"

rm -rf "$BASE"; mkdir -p "$PKG" "$OUT"

echo "== 0. stage sealed package into scratch: $PKG"
rsync -a --exclude '__pycache__' "$SRC/models" "$SRC/generated" "$SRC/pkg" \
      "$SRC/stellarator.snapshot.json" "$PKG/"
git -C "$SCRATCH" init -q
git -C "$SCRATCH" -c user.email=s@s -c user.name=s add -A
git -C "$SCRATCH" -c user.email=s@s -c user.name=s commit -qm sealed
echo "-- clean at start: [$(git -C "$SCRATCH" status --porcelain | wc -l) entries]"

fingerprints () {  # $1 = label
  python3 - "$PKG" "$1" <<'PY'
import json,sys,hashlib,os
root,label=sys.argv[1],sys.argv[2]
mc=json.load(open(f"{root}/generated/contracts/model_contract.json"))
pc=json.load(open(f"{root}/generated/contracts/package_contract.json"))
print(f"[{label}] semantic   = {mc['semantic_fingerprint']}")
print(f"[{label}] executable = {pc['executable_fingerprint']}")
PY
}

generate () {  # $1 = label
  echo "== generate ($1)"
  ( cd "$REPO" && /usr/bin/time -f "   wall=%es" \
    uv run sysml-codegen generate \
      --models "$PKG/models" --output "$PKG/generated" \
      --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten \
    ) > "$OUT/gen_$1.log" 2>&1
  echo "   exit=$? ; log=$OUT/gen_$1.log"
  tail -25 "$OUT/gen_$1.log" | sed 's/^/   | /'
}

snap () {  # $1 = label -> record porcelain + full-tree digest
  git -C "$SCRATCH" status --porcelain > "$OUT/status_$1.txt"
  echo "-- git status --porcelain after $1: $(wc -l < "$OUT/status_$1.txt") entries"
  sed 's/^/   | /' "$OUT/status_$1.txt" | head -40
  ( cd "$PKG" && find generated -type f ! -path '*__pycache__*' -print0 \
      | sort -z | xargs -0 sha256sum ) > "$OUT/tree_$1.sha256"
  ( cd "$PKG" && find generated -type f ! -path '*__pycache__*' -printf '%T@ %p\n' ) \
      | sort > "$OUT/mtime_$1.txt"
  fingerprints "$1"
}

snap sealed
generate 1; snap 1
echo "== compare sealed vs run1 (first in-place regeneration)"
diff -u "$OUT/tree_sealed.sha256" "$OUT/tree_1.sha256" > "$OUT/tree_diff_sealed_1.txt" \
  && echo "   IDENTICAL tree (sealed == run1) — first in-place regen changed no bytes" \
  || { echo "   TREE MOVED sealed -> run1:"; sed 's/^/   | /' "$OUT/tree_diff_sealed_1.txt" | head -40; }
echo "-- files whose mtime moved in run1: $(comm -13 <(sort "$OUT/mtime_sealed.txt") <(sort "$OUT/mtime_1.txt") | wc -l) of $(wc -l < "$OUT/mtime_sealed.txt")"
generate 2; snap 2

echo "== compare run1 vs run2"
diff -u "$OUT/tree_1.sha256" "$OUT/tree_2.sha256" > "$OUT/tree_diff.txt" \
  && echo "   IDENTICAL tree (run1 == run2)" \
  || { echo "   TREE MOVED between run1 and run2:"; sed 's/^/   | /' "$OUT/tree_diff.txt" | head -40; }
echo "== artifacts in $OUT"
