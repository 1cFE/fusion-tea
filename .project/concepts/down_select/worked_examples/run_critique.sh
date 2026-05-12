#!/usr/bin/env bash
# Run Pass B critique against an existing trace draft.
# Usage: ./run_critique.sh <concept-slug>
set -euo pipefail
slug="${1:?concept slug required}"
root="/home/reid/1cfe/fusion-tea"
here="$root/.project/concepts/down_select/worked_examples"
methodology="$root/.project/concepts/down_select/concept_part2.md"
trace="$here/drafts/${slug}.trace.raw.md"
[[ -f "$trace" ]] || { echo "missing trace: $trace" >&2; exit 1; }
out="$here/drafts/${slug}.critique.md"
err="$here/drafts/${slug}.critique.err.log"
{
  cat "$here/prompts/03_critique.md"
  echo
  echo "---"
  echo "# INPUT 1 — Methodology (§Per-stage factors and §Evaluation procedure)"
  echo
  sed -n '52,191p' "$methodology"
  echo
  echo "---"
  echo "# INPUT 2 — Trace under review"
  echo
  cat "$trace"
  echo
  echo "---"
  echo
  echo "Now produce the critique for the trace above."
} | claude -p - --model opus --tools "" --output-format text > "$out" 2> "$err"
echo "wrote: $out"
wc -l "$out" "$err"
