#!/usr/bin/env bash
# Extract all 6 fusion source PDFs with agentic-mbse v4 pipeline.
# Run from repo root: ./scripts/extract_all.sh
#
# Runs all extractions in parallel. Each extraction logs to
# .project/active/extraction-validation/logs/extract_<slug>.log
# Output goes to test-extract/<subdir>/

set -euo pipefail

LOGDIR=".project/active/extraction-validation/logs"
OUTDIR="test-extract"

mkdir -p "$LOGDIR" "$OUTDIR"

PDFS=(
  "knowledge/raw/Araiinejad and Shirvan - 2025 - Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants.pdf"
  "knowledge/raw/Delene et al. - 2001 - An Assessment of the Economics of Future Electric Power Generation Options and the Implications for.pdf"
  "knowledge/raw/Hawker - 2020 - A simplified economic model for inertial fusion.pdf"
  "knowledge/raw/Hsu et al. - 2020 - Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts.pdf"
  "knowledge/raw/Swanson et al. - 2026 - Overview of the Helios Design A Practical Planar Coil Stellarator Fusion Power Plant.pdf"
  "knowledge/raw/Waganer - ARIES Cost Account Documentation.pdf"
)

SLUGS=(
  "araiinejad"
  "delene"
  "hawker"
  "hsu"
  "swanson"
  "waganer"
)

PIDS=()
for i in "${!PDFS[@]}"; do
  pdf="${PDFS[$i]}"
  slug="${SLUGS[$i]}"
  log="$LOGDIR/extract_${slug}.log"

  echo "Starting: $slug -> $log"
  uv run agentic-mbse extract \
    --force \
    --budget 50 \
    --model opus \
    --index \
    --summarize \
    --output "$OUTDIR" \
    "$pdf" \
    > "$log" 2>&1 &
  PIDS+=($!)
done

echo ""
echo "All 6 extractions launched. Waiting for completion..."
echo ""

FAILURES=0
for i in "${!PIDS[@]}"; do
  pid="${PIDS[$i]}"
  slug="${SLUGS[$i]}"
  if wait "$pid"; then
    echo "  DONE: $slug"
  else
    echo "  FAIL: $slug (exit $?)"
    FAILURES=$((FAILURES + 1))
  fi
done

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "All 6 extractions completed successfully."
else
  echo "$FAILURES extraction(s) failed. Check logs in $LOGDIR/"
fi

echo ""
echo "Output in $OUTDIR/:"
ls "$OUTDIR"/
