#!/usr/bin/env bash
# verify.sh — verification harness for concept-research-17-split work item
# Usage: bash .project/active/concept-research-17-split/verify.sh

set -uo pipefail

REPO_ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$REPO_ROOT"

PASS=0
FAIL=0
report() {
  local status=$1; shift
  if [ "$status" = "0" ]; then
    echo "  PASS: $*"
    PASS=$((PASS+1))
  else
    echo "  FAIL: $*"
    FAIL=$((FAIL+1))
  fi
}

echo "=== Canonical alignment ==="
FS_IDS=$(ls knowledge/concept_research/ 2>/dev/null | grep -E '^[0-9]' | sort)
CANON_IDS=$(awk -F',' 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort)
EXTRA_ON_FS=$(comm -23 <(echo "$FS_IDS") <(echo "$CANON_IDS"))
MISSING_ON_FS=$(comm -13 <(echo "$FS_IDS") <(echo "$CANON_IDS"))
[ -z "$EXTRA_ON_FS" ]; report $? "filesystem has no IDs outside canonical (extras: $(echo $EXTRA_ON_FS | tr '\n' ' '))"
[ -z "$MISSING_ON_FS" ]; report $? "canonical IDs all present on filesystem (missing: $(echo $MISSING_ON_FS | tr '\n' ' '))"

echo ""
echo "=== Manifest roundtrip ==="
MANIFEST=.project/active/concept-research-17-split/source_partition.csv
if [ -f "$MANIFEST" ]; then
  # legacy source basenames currently on disk
  if [ -d knowledge/concept_research/17-laser-icf-direct-drive ]; then
    SRC_ROOT=knowledge/concept_research/17-laser-icf-direct-drive
  else
    SRC_ROOT=archive/concept_research_legacy/17-laser-icf-direct-drive
  fi
  if [ -d "$SRC_ROOT" ]; then
    LEGACY_BASENAMES=$(find "$SRC_ROOT" -maxdepth 3 -mindepth 3 -path "*/sources/*" -type d -printf "%f\n" | grep -v "^images$" | sort -u)
    MANIFEST_BASENAMES=$(awk -F',' 'NR>1 {print $2}' "$MANIFEST" | sort -u)
    DIFF=$(diff <(echo "$LEGACY_BASENAMES") <(echo "$MANIFEST_BASENAMES"))
    [ -z "$DIFF" ]; report $? "manifest covers all legacy source dirs"
  fi
  # all sides valid
  BAD_SIDE=$(awk -F',' 'NR>1 && $3 !~ /^(17a|17b|shared)$/' "$MANIFEST")
  [ -z "$BAD_SIDE" ]; report $? "all manifest rows have valid side {17a,17b,shared}"
else
  report 1 "manifest file present at $MANIFEST"
fi

echo ""
echo "=== Per-side dirs (Phase 2+) ==="
for side in 17a-laser-icf-hybrid-drive 17b-laser-icf-fast-ignition; do
  d=knowledge/concept_research/$side
  if [ -d "$d" ]; then
    [ -f "$d/dossier.md" ]; report $? "$side has dossier.md"
    [ -f "$d/changelog.md" ]; report $? "$side has changelog.md"
    grep -q "^## Differentiation Table Values" "$d/dossier.md" 2>/dev/null
    report $? "$side dossier has Differentiation Table Values section"
  else
    echo "  SKIP: $d not yet present (expected before Phase 2)"
  fi
done

echo ""
echo "=== Archive (Phase 3+) ==="
if [ -d archive/concept_research_legacy ]; then
  [ -f archive/concept_research_legacy/README.md ]; report $? "archive README present"
  for d in 17-laser-icf-direct-drive 20-modular-hts-stellarator 34-compact-spherical-tokamak-india; do
    [ -d "archive/concept_research_legacy/$d" ]; report $? "archived: $d"
    [ ! -d "knowledge/concept_research/$d" ]; report $? "removed from concept_research: $d"
  done
else
  echo "  SKIP: archive/concept_research_legacy/ not yet present (expected before Phase 3)"
fi

echo ""
echo "=== SOURCE_INDEX.md (Phase 4+) ==="
INDEX=knowledge/concept_research/SOURCE_INDEX.md
if [ -f "$INDEX" ]; then
  N=$(grep -cE '^### [0-9]' "$INDEX")
  [ "$N" = "40" ]; report $? "SOURCE_INDEX has exactly 40 concept sections (found $N)"
  ! grep -q "^### 17-laser-icf-direct-drive" "$INDEX"; report $? "SOURCE_INDEX does not list 17-laser-icf-direct-drive"
  ! grep -q "^### 20-modular-hts-stellarator" "$INDEX"; report $? "SOURCE_INDEX does not list 20-modular-hts-stellarator"
  ! grep -q "^### 34-compact-spherical-tokamak-india" "$INDEX"; report $? "SOURCE_INDEX does not list 34-compact-spherical-tokamak-india"
  grep -q "^### 17a-laser-icf-hybrid-drive" "$INDEX"; report $? "SOURCE_INDEX lists 17a-laser-icf-hybrid-drive"
  grep -q "^### 17b-laser-icf-fast-ignition" "$INDEX"; report $? "SOURCE_INDEX lists 17b-laser-icf-fast-ignition"
  grep -q "^### 37-magnetized-target-inertial-fusion-mtif" "$INDEX"; report $? "SOURCE_INDEX lists 37"
  grep -q "^### 38-particle-accelerator-driven-fusion" "$INDEX"; report $? "SOURCE_INDEX lists 38"
  grep -q "^### 39-spherical-tokamak-cs-free-p-b11" "$INDEX"; report $? "SOURCE_INDEX lists 39"
fi

echo ""
echo "=== Summary ==="
echo "PASS: $PASS  FAIL: $FAIL"
exit $FAIL
