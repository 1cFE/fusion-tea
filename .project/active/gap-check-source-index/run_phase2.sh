#!/usr/bin/env bash
# Phase 2 regeneration driver. Regenerates gap_report.md for every concept in
# /tmp/concept_ids.txt, then immediately builds a per-concept diff file at
# .project/active/gap-check-source-index/diffs/<concept_id>.md.
#
# Skips concept 33 (regenerated in Phase 1). Concept 01 IS in the list (we want
# to remove its special-case surgical-fix status by regenerating it like the rest).
set -u

REPO=/home/reid/1cfe/fusion-tea
cd "$REPO"

BASELINE_DIR=/tmp/gap_baselines_2026-05-22
LOG_DIR=/tmp/gap_baselines_2026-05-22/logs
DIFF_DIR="$REPO/.project/active/gap-check-source-index/diffs"
mkdir -p "$LOG_DIR" "$DIFF_DIR"

extract_count() {
  # $1 = file, $2 = field name (blocking_count or important_count)
  grep -m1 "^${2}:" "$1" 2>/dev/null | sed 's/.*: *//' | tr -d ' '
}

extract_rating() {
  grep -m1 '^overall_rating:' "$1" 2>/dev/null | sed 's/.*: *"\?//; s/"$//'
}

build_diff() {
  local cid="$1"
  local baseline="$BASELINE_DIR/${cid}.md"
  local newr="$REPO/exploration/concept_analysis/analyses/${cid}/gap_report.md"
  local out="$DIFF_DIR/${cid}.md"

  if [ ! -f "$newr" ]; then
    echo "MISSING new report: $newr" >&2
    return
  fi

  local bc_old bc_new ic_old ic_new r_old r_new
  bc_old=$(extract_count "$baseline" blocking_count)
  bc_new=$(extract_count "$newr" blocking_count)
  ic_old=$(extract_count "$baseline" important_count)
  ic_new=$(extract_count "$newr" important_count)
  r_old=$(extract_rating "$baseline")
  r_new=$(extract_rating "$newr")

  local delta_bc
  if [ -n "$bc_old" ] && [ -n "$bc_new" ]; then
    delta_bc=$(( bc_new - bc_old ))
  else
    delta_bc="?"
  fi

  {
    echo "# Diff: $cid"
    echo
    echo "**Generated:** $(date -Is)"
    echo
    echo "## Counts"
    echo
    echo "| field | baseline | new | Δ |"
    echo "|-------|----------|-----|---|"
    echo "| blocking_count   | ${bc_old:-?} | ${bc_new:-?} | ${delta_bc} |"
    echo "| important_count  | ${ic_old:-?} | ${ic_new:-?} | - |"
    echo "| overall_rating   | ${r_old:-?} | ${r_new:-?} | - |"
    echo
    echo "## Fleet-source citations (new only — grep \`knowledge/sources/\` or \`PyFECONS\`)"
    echo
    echo '```'
    grep -nE 'knowledge/sources/|PyFECONS|/home/reid/PyFECONS' "$newr" || echo "(none)"
    echo '```'
    echo
    echo "## Blocking-tier lines (baseline)"
    echo
    echo '```'
    grep -nE '\| blocking \||\*\*blocking\*\*|— blocking —|`blocking`' "$baseline" || echo "(none)"
    echo '```'
    echo
    echo "## Blocking-tier lines (new)"
    echo
    echo '```'
    grep -nE '\| blocking \||\*\*blocking\*\*|— blocking —|`blocking`' "$newr" || echo "(none)"
    echo '```'
    echo
    echo "## Full unified diff (truncated to 400 lines)"
    echo
    echo '```diff'
    diff -u "$baseline" "$newr" 2>/dev/null | head -400 || echo "(diff failed)"
    echo '```'
    echo
    echo "## Acceptance notes (fill during Phase 3)"
    echo
    echo "- Deviation class (1-6 per plan.md): "
    echo "- Justified by fleet source? "
    echo "- Notes: "
  } > "$out"
}

START=$(date -Is)
echo "[$START] Phase 2 start. Concepts: $(wc -l < /tmp/concept_ids.txt)"

# Also build a diff for concept 33 from the Phase 1 baseline (already regenerated)
build_diff "33-state-backed-tokamak-best"
echo "[$(date -Is)] concept 33 diff built (from Phase 1)"

i=0
TOTAL=$(wc -l < /tmp/concept_ids.txt)
while IFS= read -r cid; do
  i=$((i+1))
  TS=$(date -Is)
  echo "[$TS] ($i/$TOTAL) $cid : regenerating ..."
  uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check "$cid" --force \
    > "$LOG_DIR/${cid}.log" 2>&1
  rc=$?
  echo "[$(date -Is)] ($i/$TOTAL) $cid : rc=$rc"
  if [ $rc -ne 0 ]; then
    echo "  FAILED — see $LOG_DIR/${cid}.log"
  fi
  build_diff "$cid"
done < /tmp/concept_ids.txt

echo "[$(date -Is)] Phase 2 complete."
