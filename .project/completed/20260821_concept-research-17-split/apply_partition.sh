#!/usr/bin/env bash
# apply_partition.sh — copy partitioned sources from legacy 17-laser-icf-direct-drive/
# to new 17a-laser-icf-hybrid-drive/ and 17b-laser-icf-fast-ignition/ dirs per the manifest.
#
# Shared rule: duplicate into BOTH sides.
# Idempotent: cp -a; existing targets overwritten.

set -euo pipefail

REPO_ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$REPO_ROOT"

SRC=knowledge/concept_research/17-laser-icf-direct-drive
DST_A=knowledge/concept_research/17a-laser-icf-hybrid-drive
DST_B=knowledge/concept_research/17b-laser-icf-fast-ignition
MANIFEST=.project/active/concept-research-17-split/source_partition.csv

copy_to_side() {
  local iter=$1 base=$2 side=$3
  local src_dir="$SRC/$iter/sources/$base"
  local src_md="$SRC/$iter/sources/$base.md"
  local src_origmd="$SRC/$iter/sources/$base.orig.md"

  local targets=()
  case "$side" in
    17a)    targets=("$DST_A") ;;
    17b)    targets=("$DST_B") ;;
    shared) targets=("$DST_A" "$DST_B") ;;
    *) echo "bad side '$side' for $iter/$base"; exit 1 ;;
  esac

  for dst in "${targets[@]}"; do
    mkdir -p "$dst/$iter/sources"
    if [ -d "$src_dir" ]; then
      cp -a "$src_dir" "$dst/$iter/sources/"
    fi
    if [ -f "$src_md" ]; then
      cp -a "$src_md" "$dst/$iter/sources/"
    fi
    if [ -f "$src_origmd" ]; then
      cp -a "$src_origmd" "$dst/$iter/sources/"
    fi
  done
}

# Skip header line; parse iter,basename,side,notes
tail -n +2 "$MANIFEST" | while IFS=',' read -r iter base side notes; do
  [ -z "$iter" ] && continue
  echo "  $iter/$base -> $side"
  copy_to_side "$iter" "$base" "$side"
done

echo "done."
