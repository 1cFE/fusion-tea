#!/usr/bin/env bash
# Phase 3 re-regeneration driver. Re-runs gap-check on all 40 active concepts
# under the strengthened prompt (mandatory source reading + preamble
# suppression + Write-tool ban). Builds per-concept diffs against the Phase 2
# state at /tmp/gap_phase2_state/.
set -u

REPO=/home/reid/1cfe/fusion-tea
cd "$REPO"

BASELINE_DIR=/tmp/gap_phase2_state
LOG_DIR=/tmp/gap_phase2_state/logs
DIFF_DIR="$REPO/.project/active/gap-check-source-index/diffs_phase3"
mkdir -p "$LOG_DIR" "$DIFF_DIR"

extract_count() {
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

  local bc_p2 bc_p3 ic_p2 ic_p3 r_p2 r_p3
  bc_p2=$(extract_count "$baseline" blocking_count)
  bc_p3=$(extract_count "$newr" blocking_count)
  ic_p2=$(extract_count "$baseline" important_count)
  ic_p3=$(extract_count "$newr" important_count)
  r_p2=$(extract_rating "$baseline")
  r_p3=$(extract_rating "$newr")

  local delta_bc
  if [ -n "$bc_p2" ] && [ -n "$bc_p3" ]; then
    delta_bc=$(( bc_p3 - bc_p2 ))
  else
    delta_bc="?"
  fi

  {
    echo "# Phase 3 diff: $cid"
    echo
    echo "**Generated:** $(date -Is)"
    echo
    echo "## Counts (Phase 2 -> Phase 3 strict-read regen)"
    echo
    echo "| field | phase2 | phase3 | Δ |"
    echo "|-------|--------|--------|---|"
    echo "| blocking_count   | ${bc_p2:-?} | ${bc_p3:-?} | ${delta_bc} |"
    echo "| important_count  | ${ic_p2:-?} | ${ic_p3:-?} | - |"
    echo "| overall_rating   | ${r_p2:-?} | ${r_p3:-?} | - |"
    echo
    echo "## Fleet-source dispositions in new report"
    echo
    echo '```'
    grep -nE "\*\*Integrated\*\*|\*\*Disqualified\*\*" "$newr" | head -20 || echo "(none — format may differ)"
    echo '```'
    echo
    echo "## Forbidden-phrase check (should be empty)"
    echo
    echo '```'
    grep -nE "has not been read|should be read before|may be applicable downstream|gap assessment is complete|I now have sufficient" "$newr" || echo "(none — good)"
    echo '```'
    echo
    echo "## First line of new report (should start with \`# Gap Assessment\`)"
    echo
    echo '```'
    head -1 "$newr"
    echo '```'
    echo
    echo "## Blocking-tier lines (new)"
    echo
    echo '```'
    grep -nE '\| blocking \||\*\*blocking\*\*|— blocking —|`blocking`' "$newr" | head -15 || echo "(none)"
    echo '```'
    echo
    echo "## Full unified diff (truncated to 400 lines)"
    echo
    echo '```diff'
    diff -u "$baseline" "$newr" 2>/dev/null | head -400 || echo "(diff failed)"
    echo '```'
  } > "$out"
}

START=$(date -Is)
TOTAL=$(wc -l < /tmp/concept_ids_phase3.txt)
echo "[$START] Phase 3 start. Concepts: $TOTAL"

i=0
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
done < /tmp/concept_ids_phase3.txt

echo "[$(date -Is)] Phase 3 complete."
