#!/usr/bin/env bash
# File and list architecture decision records under .project/adr/.
# Usage: adr.sh list | new <slug> | supersede <old-id> <new-id>
set -euo pipefail

ADR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../adr" && pwd)"
INDEX="$ADR_DIR/INDEX.md"

usage() { echo "usage: adr.sh list | new <slug> | supersede <old-id> <new-id>" >&2; exit 2; }

record_for() {  # id -> path, or empty
  find "$ADR_DIR" -maxdepth 1 -name "$1-*.md" -print -quit
}

case "${1-}" in
  list)
    cat "$INDEX"
    ;;
  new)
    [ $# -eq 2 ] || usage
    slug="$2"
    last=$(ls "$ADR_DIR" | grep -Eo '^[0-9]{3}' | sort -n | tail -1 || true)
    id=$(printf '%03d' $(( 10#${last:-000} + 1 )))
    file="$ADR_DIR/$id-$slug.md"
    [ -e "$file" ] && { echo "adr.sh: $file already exists" >&2; exit 1; }
    sed -e "s/^# ADR-NNN: .*/# ADR-$id: <one-line decision, stated as a decision>/" \
        -e "s/^date: YYYY-MM-DD/date: $(date +%F)/" "$ADR_DIR/template.md" > "$file"
    row=$(printf '| `%s` | [<title>](%s-%s.md) | accepted | `[GRADE — copy from source]` | %s |' \
      "$id" "$id" "$slug" "$(date +%F)")
    last_row=$(grep -n '^| `[0-9]' "$INDEX" | tail -1 | cut -d: -f1)
    [ -n "$last_row" ] || { echo "adr.sh: no table rows found in $INDEX" >&2; exit 1; }
    sed -i "${last_row}a\\$row" "$INDEX"
    echo "$file"
    echo "adr.sh: index row appended to $INDEX — fill in the title, grade, and the six sections" >&2
    ;;
  supersede)
    [ $# -eq 3 ] || usage
    old=$(record_for "$2"); new=$(record_for "$3")
    [ -n "$old" ] || { echo "adr.sh: no record for id $2" >&2; exit 1; }
    [ -n "$new" ] || { echo "adr.sh: no record for id $3" >&2; exit 1; }
    newname=$(basename "$new")
    sed -i -e "s/^status: accepted/status: superseded/" \
           -e "0,/^# ADR-/s|^\(# ADR-.*\)$|\1\n\n> Superseded by [ADR-$3]($newname).|" "$old"
    sed -i -e "s/^supersedes: none/supersedes: $2/" "$new"
    sed -i -E "s/^(\| \`$2\` \|.*\|) accepted (\|.*)$/\1 superseded \2/" "$INDEX"
    echo "adr.sh: $2 superseded by $3 — check the index row and cross-links" >&2
    ;;
  *) usage ;;
esac
