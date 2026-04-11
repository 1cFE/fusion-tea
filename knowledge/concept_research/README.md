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

## Reading Research Data

Start with `{concept-id}/dossier.md` for a synthesized overview: what the concept is, company, key parameters, differentiation table values. Use it for orientation, but do NOT treat it as authoritative for specific numbers — trace quantitative claims to the individual sources.

Evidence lives in `{concept-id}/iter-NN/sources/`. Each iteration may add new sources — check ALL `iter-*` directories when gathering evidence on a topic.

**Companion directory pattern.** Each source appears as a `.md` file plus a same-named directory:

```
iter-NN/sources/
├── {name}.md        # Source text — read this
├── {name}/          # Companion directory (artifact bundle)
│   ├── output.md    # Same content as ../{name}.md (a copy)
│   ├── images/      # Tables, equations, figures (R2-synced)
│   ├── metrics.json # Extraction quality metrics
│   ├── raw.html     # Original HTML snapshot (R2-synced)
│   └── raw.pdf      # Original PDF (R2-synced)
```

`{name}.md` and `{name}/output.md` are identical. Read `{name}.md`; use the companion dir for images and provenance artifacts.

## Source Quality Tiers

Sources fall into three tiers. Check the first lines of `sources/{name}.md` to identify which:

| Tier | How to identify | Trust level |
|------|----------------|-------------|
| **Direct extraction** | Starts with `---` and has `source:`, `backend:`, `content_hash_sha256:` in YAML frontmatter | Authoritative for what it contains. Text may still be lossy — verify quantitative data against images. |
| **Haiku paraphrase** | Starts with `# Title` directly, no YAML frontmatter (or is a `.orig.md` file) | Lossy summary. Specific numbers and technical details may be wrong. Flag as unverified if citing values. |
| **Dossier** | `{concept-id}/dossier.md` | Synthesized overview. Good for orientation. Not authoritative for specific claims — trace to sources. |

When sources disagree: peer-reviewed paper > technical report > company website > news article > Haiku paraphrase. Direct extraction beats Haiku paraphrase for the same underlying source. Later iterations supersede earlier ones on the same topic.

## Image Inspection

Text extraction from sources is **lossy**. Tables get garbled (dropped columns, merged cells, corrupted scientific notation like `1.66 1020` instead of `1.66 × 10²⁰`). Equations in PDFs have no text form at all. The `images/` directory in the companion dir holds the ground truth.

### When you MUST read images

1. **You see `![](images/page_NNN_eq_N.png)` in the text.** The equation exists ONLY in the image.
2. **You are extracting a number for analysis or modeling.** Cross-check against the table image — do not trust text-extracted tables for quantitative work.
3. **The text references a table or figure by number** ("see Table 3", "Figure 7 shows"). Find and read the corresponding image.
4. **Numbers don't add up or text seems incomplete.** The missing data is probably in a table/figure image.

### Image path resolution

Image references in the source `.md` file (like `![](images/page_003_table_0.png)`) are relative to the **companion directory**, not to the `.md` file. Resolve as:

```
iter-NN/sources/{name}/images/page_003_table_0.png
```

### What's in `images/`

**PDF sources** (YAML `backend: "agentic-mbse"` or `source_type: "local_file"`):
- `page_NNN_table_N.png` — tables (authoritative; text extraction mangles them)
- `page_NNN_eq_N.png` — equations (no text form; markdown only has the image reference)
- `tmp*.pdf-N-N.png` — figures, charts, diagrams, schematics

**arXiv HTML sources** (YAML `backend: "pandoc-arxiv"`):
- Original filenames (e.g., `flux_contours.png`). Figures only — tables and equations are in the text as markdown.

Images are R2-synced binaries, not in git. If `images/` is empty or missing, run `./scripts/sync_research.sh pull`.

## Tracing to Original Source

When extraction seems wrong or incomplete, trace back:

1. **YAML frontmatter `source:` field** — the original URL or PDF path
2. **`sources/{name}/raw.html` or `raw.pdf`** — the original fetched content in the companion dir (R2-synced)
3. **`sources/{name}/metrics.json`** — extraction quality warnings and metrics
4. **Fetch the URL directly** if the above are still insufficient

## Known Limitations

- **JS-heavy company websites** extract thinly — the rendered page often relies on JavaScript that the fetcher doesn't execute. Haiku paraphrases of these sites may actually contain more information than direct extraction.
- **arXiv HTML viewer image 404s** — some arXiv papers have missing images in the HTML viewer output, even when the PDF contains them. Fall back to the PDF (`raw.pdf`) if available.
- **Paywalled papers** — extracted from local PDFs supplied by the user. Identified by `source_type: local_file` in frontmatter. No URL to re-fetch; the `raw.pdf` in the companion dir is the only copy.
