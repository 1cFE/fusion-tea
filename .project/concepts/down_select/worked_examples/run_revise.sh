#!/usr/bin/env bash
set -euo pipefail
slug="${1:?concept slug required}"
root="/home/reid/1cfe/fusion-tea"
here="$root/.project/concepts/down_select/worked_examples"
methodology="$root/.project/concepts/down_select/concept_part2.md"
trace="$here/drafts/${slug}.trace.raw.md"
critique="$here/drafts/${slug}.critique.md"
for f in "$trace" "$critique"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done
out="$here/drafts/${slug}.trace.v2.md"
err="$here/drafts/${slug}.trace.v2.err.log"
{
  cat "$here/prompts/04_revise.md"
  echo
  echo "---"
  echo "# INPUT 1 — Methodology"
  echo
  sed -n '52,191p' "$methodology"
  echo
  echo "---"
  echo "# INPUT 2 — Original trace"
  echo
  cat "$trace"
  echo
  echo "---"
  echo "# INPUT 3 — Critique of the trace"
  echo
  cat "$critique"
  echo
  echo "---"
  echo
  echo "Produce the revised trace now."
} | claude -p - --model opus --tools "" --output-format text > "$out" 2> "$err"
echo "wrote: $out"
wc -l "$out" "$err"
