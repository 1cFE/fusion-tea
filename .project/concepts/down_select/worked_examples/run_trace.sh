#!/usr/bin/env bash
# Assemble inputs and run a per-concept trace via claude headless.
# Usage: ./run_trace.sh <concept-slug> <NN>
#   e.g. ./run_trace.sh 01-hts-compact-tokamak 01
set -euo pipefail

slug="${1:?concept slug required}"
nn="${2:?explorer NN required (e.g. 01)}"
root="/home/reid/1cfe/fusion-tea"
here="$root/.project/concepts/down_select/worked_examples"

methodology="$root/.project/concepts/down_select/concept_part2.md"
brief="$here/ecosystem_markets.md"
dossier="$root/knowledge/concept_research/$slug/dossier.md"
analysis="$root/exploration/concept_analysis/analyses/$slug/analysis.md"
synthesis="$root/exploration/concept_analysis/analyses/$slug/synthesis.md"
explorer="$root/exploration/concept_explorer/data/$nn.json"

for f in "$methodology" "$brief" "$dossier" "$analysis" "$synthesis" "$explorer"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done

out="$here/drafts/${slug}.trace.raw.md"
err="$here/drafts/${slug}.trace.err.log"

{
  cat "$here/prompts/02_trace_template.md"
  echo
  echo "---"
  echo "# INPUT 1 — Methodology (concept_part2.md, §Per-stage factors and §Evaluation procedure)"
  echo
  # Lines 52-191 cover §Per-stage factors through §Evaluation procedure
  sed -n '52,191p' "$methodology"
  echo
  echo "---"
  echo "# INPUT 2 — Ecosystem markets brief"
  echo
  cat "$brief"
  echo
  echo "---"
  echo "# INPUT 3 — Concept dossier ($slug)"
  echo
  cat "$dossier"
  echo
  echo "---"
  echo "# INPUT 4 — Prior analysis ($slug/analysis.md)"
  echo
  cat "$analysis"
  echo
  echo "---"
  echo "# INPUT 5 — Prior synthesis ($slug/synthesis.md)"
  echo
  cat "$synthesis"
  echo
  echo "---"
  echo "# INPUT 6 — Explorer JSON (CAS decomposition + sensitivities)"
  echo '```json'
  cat "$explorer"
  echo '```'
  echo
  echo "---"
  echo
  echo "Now produce the trace document for **$slug** following the format and quality bar above."
} | claude -p - --model opus --tools "" --output-format text > "$out" 2> "$err"

echo "wrote: $out"
wc -l "$out" "$err"
