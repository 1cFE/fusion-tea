#!/usr/bin/env bash
# regen_source_index.sh — regenerate knowledge/concept_research/SOURCE_INDEX.md
# from the current filesystem state.

set -euo pipefail

REPO_ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$REPO_ROOT"

ROOT=knowledge/concept_research
OUT=$ROOT/SOURCE_INDEX.md

# infer source type from contents of the source dir;
# falls back to reading source_type frontmatter from output.md when binary not present locally
src_type() {
  local d=$1
  if [ -f "$d/raw.pdf" ]; then echo "PDF"; return; fi
  if [ -f "$d/raw.html" ]; then echo "HTML"; return; fi
  if [ -f "$d/output.md" ]; then
    local st
    st=$(awk -F'"' '/^source_type:/ {print $2; exit}' "$d/output.md" 2>/dev/null)
    case "$st" in
      url) echo "HTML" ;;
      local_file)
        # check the source field for .pdf hint
        local sf
        sf=$(awk -F'"' '/^source:/ {print $2; exit}' "$d/output.md" 2>/dev/null)
        case "$sf" in
          *.pdf) echo "PDF" ;;
          *.html|*.htm) echo "HTML" ;;
          *) echo "file" ;;
        esac
        ;;
      *) echo "unknown" ;;
    esac
  else
    echo "unknown"
  fi
}

{
  echo "# Concept Research — Source Index"
  echo ""
  echo "Per-concept research dossiers and source extractions for the Fusion TEA"
  echo "concept landscape. Binary artifacts (PDF, HTML, PNG) synced via R2;"
  echo "markdown and JSON tracked in git."
  echo ""
  echo "Sync: \`./scripts/sync_research.sh pull\`"
  echo ""
  echo "## Concepts"
  echo ""

  for concept in $(ls "$ROOT" | grep -E '^[0-9]' | sort); do
    echo "### $concept"
    if [ -f "$ROOT/$concept/dossier.md" ]; then
      echo "- **Dossier**: \`$concept/dossier.md\`"
    fi

    iters=$(find "$ROOT/$concept" -maxdepth 1 -mindepth 1 -type d -name "iter-*" -printf "%f\n" | sort | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')
    iter_count=$(echo "$iters" | tr ',' '\n' | grep -c "iter-" || true)
    echo "- **Iterations**: $iter_count ($iters)"

    # collect all sources
    src_lines=()
    while IFS= read -r d; do
      [ -z "$d" ] && continue
      base=$(basename "$d")
      iter=$(basename "$(dirname "$(dirname "$d")")")
      [ "$base" = "images" ] && continue
      typ=$(src_type "$d")
      src_lines+=("  - \`$iter/sources/$base\` — [$typ]")
      if [ -f "$ROOT/$concept/$iter/sources/$base.md" ]; then
        src_lines+=("  - \`$iter/sources/$base.md\` — [processed .md]")
      fi
    done < <(find "$ROOT/$concept" -maxdepth 3 -mindepth 3 -path "*/sources/*" -type d | sort)

    echo "- **Sources** (${#src_lines[@]}):"
    for line in "${src_lines[@]}"; do
      echo "$line"
    done
    echo ""
  done
} > "$OUT"

echo "wrote $OUT"
