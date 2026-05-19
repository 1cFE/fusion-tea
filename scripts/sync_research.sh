#!/usr/bin/env bash
# Sync binary research artifacts between local and Cloudflare R2.
#
# IMPORTANT: This uses `rclone sync` (mirror), NOT `rclone copy` (additive).
# `push` makes R2 mirror LOCAL — any concept directory present on R2 but
# NOT present locally will be DELETED FROM R2. Likewise `pull` deletes
# local files that aren't on R2.
#
# Practical consequence: after retiring or renaming a concept directory
# locally, the next `push` will purge the old prefix from R2. This is by
# design (keeps R2 in lockstep with the canonical concept set) but is
# destructive. Always:
#   1. Snapshot the prefix(es) you're about to retire (rclone copy to a
#      safe local location), and
#   2. Run with --dry-run first to confirm the deletion set is what you
#      expect.
#
# Usage:
#   ./scripts/sync_research.sh pull                          # pull all (mirrors R2->local)
#   ./scripts/sync_research.sh push                          # push all (mirrors local->R2; deletes R2-only dirs)
#   ./scripts/sync_research.sh pull --dry-run                # preview
#   ./scripts/sync_research.sh push --dry-run                # preview (recommended before any push)
#   ./scripts/sync_research.sh pull 01-hts-compact-tokamak   # single concept
set -euo pipefail

# Configuration
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_DIR="$REPO_ROOT/knowledge/concept_research"
REMOTE="r2:1cfe-research/concept_research"
INCLUDE_ARGS=(--include "*.pdf" --include "*.html" --include "*.png"
              --include "*.jpg" --include "*.jpeg" --include "*.gif"
              --include "*.svg")

# Parse arguments
ACTION="${1:?Usage: sync_research.sh <pull|push> [--dry-run] [concept-id]}"
shift
DRY_RUN=""
CONCEPT=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="--dry-run" ;;
    *) CONCEPT="$arg" ;;
  esac
done

# Preflight checks
command -v rclone >/dev/null 2>&1 || { echo "error: rclone not installed (see knowledge/concept_research/README.md)"; exit 1; }
if ! rclone listremotes 2>/dev/null | grep -q '^r2:$'; then
  echo "error: R2 remote 'r2' not configured in rclone (run: rclone config)"
  exit 1
fi
# Verify credentials work (test the specific bucket, not all buckets)
if ! rclone lsd r2:1cfe-research >/dev/null 2>&1; then
  echo "error: cannot access R2 bucket 'r2:1cfe-research'. Check your credentials."
  echo "       Run: rclone config reconnect r2:"
  rclone lsd r2:1cfe-research 2>&1 | tail -3
  exit 1
fi

# Build paths
if [[ -n "$CONCEPT" ]]; then
  LOCAL_DIR="$LOCAL_DIR/$CONCEPT"
  REMOTE="$REMOTE/$CONCEPT"
  if [[ ! -d "$LOCAL_DIR" && "$ACTION" == "push" ]]; then
    echo "error: concept directory not found: $CONCEPT"
    exit 1
  fi
fi

# Execute
case "$ACTION" in
  pull) rclone sync "$REMOTE" "$LOCAL_DIR" "${INCLUDE_ARGS[@]}" $DRY_RUN --progress ;;
  push) rclone sync "$LOCAL_DIR" "$REMOTE" "${INCLUDE_ARGS[@]}" $DRY_RUN --progress ;;
  *) echo "error: unknown action '$ACTION' (use pull or push)"; exit 1 ;;
esac
