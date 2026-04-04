# Concept Research

Per-concept techno-economic research dossiers for 38 fusion concepts in the Fusion TEA investigation. Produced by the Phase 1a research pipeline (`exploration/phase_1a/`).

## Directory Structure

```
concept_research/
├── SOURCE_INDEX.md              # Per-concept source listing
├── README.md                    # This file
├── .gitignore                   # Excludes binary artifacts from git
├── {concept-id}/                # e.g., 01-hts-compact-tokamak/
│   ├── dossier.md               # Consolidated research findings
│   ├── changelog.md             # Iteration history
│   └── iter-NN/
│       ├── prompt.md            # Research prompt
│       ├── output.md            # Claude output
│       ├── synthesis_prompt.md  # Synthesis prompt
│       └── sources/
│           ├── {source}.md      # Processed extraction (git-tracked)
│           ├── {source}.orig.md # Original extraction (git-tracked)
│           └── {source}/        # Source artifact directory
│               ├── output.md    # Extracted text (git-tracked)
│               ├── metrics.json # Extraction metrics (git-tracked)
│               ├── raw.html     # Original HTML snapshot (R2-synced)
│               ├── raw.pdf      # Original PDF (R2-synced)
│               └── images/      # Extracted figures (R2-synced)
└── ...
```

## What's in Git vs R2

| In Git (always available) | In R2 (sync to get) |
|---------------------------|---------------------|
| `*.md` — dossiers, prompts, outputs, extractions | `*.pdf` — original PDF documents |
| `*.json` — extraction metrics, cost/decision data | `*.html` — original HTML snapshots |
| | `*.png` / `*.jpg` / `*.svg` — extracted figures |

The analysis pipeline (`run_analysis.py`) only reads `.md` files — it works without binary artifacts.

## Syncing Binary Artifacts

Binary artifacts (PDFs, HTML snapshots, extracted images) are stored in Cloudflare R2 and excluded from git via `.gitignore`.

### First-time Setup

1. **Install rclone** (v1.63+ required):
   ```bash
   # Ubuntu/Debian — apt version may be too old, install from rclone.org instead:
   curl https://rclone.org/install.sh | sudo bash

   # macOS
   brew install rclone

   # Windows (winget)
   winget install Rclone.Rclone

   # Windows (scoop)
   scoop install rclone
   ```

2. **Get R2 credentials** from Cloudflare:
   - Go to [Cloudflare dashboard](https://dash.cloudflare.com/) → **R2 Object Storage** → **Manage R2 API Tokens**
   - Create an **Account API Token** with read/write access to `1cfe-research`
   - On the success page, copy the **Access Key ID** and **Secret Access Key** (shown below the token value — these are the S3-compatible credentials, separate from the API token itself)
   - Save them to your `.env` file:
     ```bash
     R2_ACCESS_KEY="<your-access-key-id>"
     R2_SECRET_ACCESS_KEY="<your-secret-access-key>"
     ```

3. **Configure the rclone remote** — either interactively or from `.env`:

   **Option A: From `.env` (recommended)**:
   ```bash
   source .env
   rclone config create r2 s3 \
     provider Cloudflare \
     access_key_id "$R2_ACCESS_KEY" \
     secret_access_key "$R2_SECRET_ACCESS_KEY" \
     endpoint https://985ab2e0dede4b8be7f56c00b861ca9b.r2.cloudflarestorage.com \
     env_auth false
   ```

   **Option B: Interactive** (`rclone config`):
   ```
   n/s/q> n
   name> r2
   Storage> 5                        # Amazon S3 Compliant
   provider> 5                       # Cloudflare
   env_auth> false
   access_key_id> <paste from .env>
   secret_access_key> <paste from .env>
   region>                            # leave blank
   endpoint> https://985ab2e0dede4b8be7f56c00b861ca9b.r2.cloudflarestorage.com
   ```
   Accept defaults for remaining prompts, then confirm with `y`.

4. **Verify**:
   ```bash
   rclone lsd r2:1cfe-research    # should return without error (empty output = success)
   ```

5. **Pull artifacts**:
   ```bash
   ./scripts/sync_research.sh pull
   ```

### Windows Notes

The `sync_research.sh` script requires bash. On Windows, run it via WSL or Git Bash. Alternatively, run rclone directly:

```powershell
# Pull
rclone sync r2:1cfe-research/concept_research knowledge/concept_research --include "*.pdf" --include "*.html" --include "*.png" --include "*.jpg" --include "*.jpeg" --include "*.gif" --include "*.svg" --progress

# Push
rclone sync knowledge/concept_research r2:1cfe-research/concept_research --include "*.pdf" --include "*.html" --include "*.png" --include "*.jpg" --include "*.jpeg" --include "*.gif" --include "*.svg" --progress
```

### Ongoing Use

```bash
# Pull all binary artifacts from R2
./scripts/sync_research.sh pull

# Push local binary artifacts to R2
./scripts/sync_research.sh push

# Preview what would transfer (no changes)
./scripts/sync_research.sh pull --dry-run

# Sync a single concept
./scripts/sync_research.sh pull 01-hts-compact-tokamak
```

## Relationship to Concept Analysis Pipeline

The concept analysis pipeline at `exploration/concept_analysis/scripts/run_analysis.py` reads research dossiers and source extractions from this directory. It resolves the path via `RESEARCH_DIR` in the script constants. A symlink at `exploration/phase_1a/research/` also points here for backward compatibility.
