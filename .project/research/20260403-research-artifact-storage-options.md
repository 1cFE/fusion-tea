---
date: 2026-04-03T12:00:00-05:00
researcher: Claude
topic: "Storage options for large research artifacts alongside a Git repository"
tags: [research, infrastructure, git, artifacts, storage]
status: complete
last_updated: 2026-04-03
---

# Research: Storage Options for Large Research Artifacts

**Date**: 2026-04-03
**Researcher**: Claude
**Research Type**: Infrastructure / Tooling

## Research Question

What is the best way to store and share ~136 MB (growing) of binary research artifacts — extracted images, HTML snapshots, and PDFs — alongside the fusion-tea Git repo, for a team of 2-5 researchers with low DevOps tolerance?

## Summary

- **Git LFS** is simplest to set up but has bandwidth cost scaling risks and poor performance with many small files (we have 918 images)
- **Cloudflare R2 + rclone** offers the best cost profile (free up to 10 GB, zero egress fees ever) with a one-command sync workflow
- **DVC** is viable but overengineered — 90% of its features (ML pipelines, experiments) are irrelevant here
- **Git submodules** and **git-annex** are not recommended — too much friction for a small research team
- **Recommendation: Cloudflare R2 + rclone** — best balance of cost, simplicity, and path preservation

## Current State

The repo currently `.gitignore`s binary artifacts:
- `knowledge/raw/*.pdf` — raw PDFs stored in Zotero, not git
- `exploration/concept_explorer/data/` — explorer data directory
- No Git LFS, DVC, or git-annex configuration exists

Artifact breakdown:
- Extracted images (PNGs): ~93 MB, 918 files
- Raw HTML snapshots: ~23 MB, 90 files
- Raw PDFs: ~20 MB, 11 files
- Total: ~136 MB today, growing with each research iteration

## Detailed Findings

### Option 1: Git LFS

**How it works**: Git LFS replaces large files with pointer files in the repo. The actual content is stored on GitHub's LFS servers and downloaded transparently on clone/checkout.

**Setup complexity**: Very low. Three commands:
```bash
git lfs install
git lfs track "*.pdf" "*.png" "*.html"
git add .gitattributes
```

**Daily workflow**: Transparent — `git add/commit/push/pull` work as normal. LFS handles the rest.

**Cost**:
- GitHub Free: 10 GB storage + 10 GB bandwidth/month included
- Overage: $0.07/GB storage, $0.0875/GB bandwidth
- At 136 MB with 5 users: comfortably within free tier
- At 1 GB with 5 users: bandwidth becomes the concern — every clone = full download

**Path preservation**: Perfect. Files appear at their normal paths.

**Gotchas**:
- **Many small files are slow**: LFS uploads/downloads each file individually via HTTP. With 918 images, clones can be very slow. GitHub issue #4819 documents this — 19,000 small files took over an hour.
- **Bandwidth multiplier**: Every clone by every user consumes bandwidth quota. 5 researchers cloning a 500 MB repo = 2.5 GB in one day.
- **Public repo risk**: If the repo goes public, anyone cloning burns your bandwidth.
- **No selective fetch by default**: You download ALL LFS files, not just the subset you need (`git lfs fetch --include` exists but is manual).
- **GitHub lock-in**: Migrating LFS content away from GitHub requires re-extracting all files.

**Verdict**: Simplest setup, but the bandwidth model and small-file performance are real risks as the collection grows past ~1 GB.

### Option 2: Separate Artifact Repo (Submodule or Manual)

**How it works**: Binary artifacts live in a second Git repo. The main repo references it via `git submodule` or by convention.

**Setup complexity**: Medium. Submodule config requires `.gitmodules`, `git submodule init/update`. Manual approach is just a README instruction.

**Daily workflow**: High friction.
- Submodules: Researchers must remember `git submodule update --init` after cloning. Detached HEAD states are common. Commits must be coordinated across two repos.
- Manual: No synchronization at all.

**Cost**: Free (second GitHub repo). But still subject to GitHub's ~5 GB soft repo size limit and 100 MB per-file limit.

**Path preservation**: Fragile. Submodule must be mounted at the exact relative path markdown files expect. Mount point is rigid.

**Gotchas**:
- Submodules are widely regarded as painful (accidental detached HEAD, teammates forgetting to pull, merge conflicts on pointer commits)
- Still stores binaries in git — every version of every file in history
- Does not solve the fundamental problem, just isolates the bloat

**Verdict**: Adds complexity without solving the core problem. Not recommended.

### Option 3: Object Storage (Cloudflare R2 + rclone)

**How it works**: Binary artifacts are stored in a cloud object storage bucket. Researchers sync them to/from local using rclone (a mature, widely-available CLI tool). The local sync target is the .gitignored artifact directory.

**Setup complexity**: Medium. One-time:
1. Create Cloudflare account (free)
2. Create R2 bucket
3. Generate API keys, distribute to team (via .env or rclone config)
4. Install rclone (`apt install rclone` / `brew install rclone`)
5. Add a Makefile target or shell script wrapper

**Daily workflow**: Low friction. One command:
```bash
make sync-artifacts  # wraps: rclone sync r2:fusion-artifacts ./knowledge/ --include "*.pdf" --include "*.png" --include "*.html"
```

Could also be integrated as a post-checkout git hook for automation.

**Cost (Cloudflare R2)**:
- **Free tier**: 10 GB storage, 1M writes, 10M reads per month. **Zero egress fees.**
- Beyond free tier: $0.015/GB/month storage
- At 136 MB with 5 users: **completely free**
- At 1 GB: still free
- At 10 GB: still free (within free tier)
- At 50 GB: ~$0.75/month

For comparison:
- AWS S3: $0.023/GB/month + $0.09/GB egress — egress kills you
- GCS: $0.020/GB/month + $0.12/GB egress — same problem
- R2 wins decisively for download-heavy workloads (which research is)

**Path preservation**: Perfect. rclone preserves directory structure exactly. Files land at the same relative paths markdown expects.

**Gotchas**:
- Requires a Cloudflare account (free tier is sufficient)
- Credential distribution — each researcher needs R2 API keys
- No automatic versioning by default (R2 supports versioning, but it's opt-in)
- No content-addressed deduplication
- Researchers must remember the sync command (mitigated by Makefile/hook)
- rclone is very mature and widely available

**Verdict**: Best cost profile. Moderate one-time setup, trivial daily workflow. Zero egress means 5 researchers can sync freely without cost concern.

### Option 4: DVC (Data Version Control)

**How it works**: DVC creates `.dvc` pointer files (like LFS) committed to git. Actual content is stored on a configurable remote (S3, GCS, Google Drive, R2, SSH, etc.). `dvc push`/`dvc pull` syncs content.

**Setup complexity**: Medium.
```bash
pip install dvc dvc-s3  # or dvc-gdrive for Google Drive
dvc init
dvc remote add -d myremote s3://bucket/path
dvc add knowledge/sources/
git add knowledge/sources/.dvc .gitignore
```

**Daily workflow**: Two-command pattern:
```bash
dvc pull    # after git pull
dvc push    # after dvc add + git push
```

**Cost**: DVC is free/open-source. Cost depends on backend (R2 free tier, Google Drive free 15 GB, etc.).

**Path preservation**: Good. Files materialize at original locations after `dvc pull`.

**Gotchas**:
- **lakeFS acquisition (November 2025)**: Iterative.ai sold DVC to lakeFS. They promise continued open-source maintenance, but long-term direction is uncertain.
- **ML-oriented UX**: Documentation, tutorials, and features are ML-focused. For simple "track binary files", you use ~10% of the tool. Confusing learning surface.
- **Two-command workflow**: Every operation needs both git and DVC commands. Easy to forget one half.
- **`.dvc` file clutter**: Each tracked file/directory gets a pointer file in the repo.
- **Google Drive backend**: Works but has OAuth auth complexity.

**Verdict**: Technically capable but overengineered for this use case. The two-command workflow and ML-oriented UX add unnecessary friction.

### Option 5: Other Options Considered

#### git-annex
- **Pros**: Most powerful fine-grained control, actively maintained
- **Cons**: Steep learning curve (Haskell-based, unique conceptual model), symlink-based approach confuses some tools, small community
- **Verdict**: Too complex for a small research team

#### Hugging Face Hub
- **Pros**: Free, generous storage with Xet backend
- **Cons**: Separate repo (like submodule approach), ML-oriented, poor relative path preservation
- **Verdict**: Not a natural fit

#### Git Partial Clone / Large Object Promisors
- Git is developing built-in large file support (pieces merged March 2025)
- **Not production-ready** — worth watching but not usable today

## Comparison Matrix

| Criterion | Git LFS | Separate Repo | R2 + rclone | DVC | git-annex |
|---|---|---|---|---|---|
| **Setup effort** | Very low | Medium | Medium | Medium | High |
| **Daily friction** | None | High | Low (one cmd) | Low-med (two cmds) | Med-high |
| **Cost at 136 MB** | Free | Free | Free | Free | Free |
| **Cost at 1 GB** | Free | Free | Free | Free | Free |
| **Cost at 10 GB** | ~$0.70/mo + bandwidth | Hits GitHub limits | Free | Depends on backend | Free |
| **Relative paths** | Perfect | Fragile | Perfect | Good | Good |
| **Small-file perf** | Poor (918 images) | Normal git | Good (batched) | Good | Good |
| **Versioning** | Full (git history) | Full (git history) | Manual/opt-in | Full (content-addressed) | Full |
| **Team learning** | Minimal | Minimal but error-prone | rclone basics | DVC concepts | Significant |
| **Long-term risk** | Bandwidth costs scale | Submodule pain | Vendor (mitigated by S3-compat API) | lakeFS acquisition uncertainty | Haskell ecosystem |

## Recommendation

**Primary: Cloudflare R2 + rclone sync script**

For this project's profile — small team, cost-sensitive, low DevOps tolerance, 136 MB growing, relative paths needed — R2 + rclone is the best fit:

1. **Cost**: Free up to 10 GB with zero egress fees. Even at 50 GB, costs are negligible.
2. **Workflow**: One sync command, wrappable in a Makefile target or git hook.
3. **Path preservation**: rclone mirrors directory structure exactly — markdown relative links work unchanged.
4. **Small-file performance**: rclone batches operations efficiently, unlike LFS's per-file HTTP requests.
5. **Portability**: R2 uses the S3 API, so migrating to S3/GCS/MinIO later is a config change, not a rewrite.
6. **No lock-in**: Unlike LFS (tied to GitHub) or DVC (potential lakeFS concerns), rclone + S3-compatible storage is a commodity.

**Implementation sketch**:
```bash
# One-time setup (per researcher)
rclone config  # interactive: create "r2" remote pointing to Cloudflare R2

# Makefile targets
sync-pull:
    rclone sync r2:fusion-tea-artifacts/knowledge ./knowledge --include "*.pdf" --include "*.png" --include "*.html"

sync-push:
    rclone sync ./knowledge r2:fusion-tea-artifacts/knowledge --include "*.pdf" --include "*.png" --include "*.html"
```

**Runner-up: Git LFS** — choose this if zero daily friction is paramount and you're confident the collection stays under ~2 GB. The 918 small images will make clones slow, and bandwidth scales with team size.

## Open Questions

- Should we enable R2 bucket versioning for artifact recovery, or is the Zotero source-of-truth sufficient for PDFs?
- Should the sync be bidirectional (researchers can upload new artifacts) or pull-only (only the extraction pipeline uploads)?
- Should we add a post-checkout git hook to auto-sync, or keep it as an explicit Makefile target?
- For HTML snapshots: are these reproducible (re-crawlable) or are they point-in-time captures that need preservation?
