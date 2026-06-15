# Runbook: Deploy & Operate the Concept Explorer on Railway

**Audience:** the repo owner (the manual account/billing/connect steps can't be done by an agent).
**Goal:** a public, always-on URL for the concept explorer that **redeploys automatically on every push to `main`**.
**Prereq:** the hosting code is on `main` — i.e. branch `feat/explorer-web-hosting` (the `Dockerfile`, `.dockerignore`, `railway.toml`, `requirements-serve.txt`, `scripts/smoke_explorer.py`) has been merged. The two pre-existing startup bugs it depends on are already merged (PR #81 UTF-8 registry, PR #82 `model_setup` path).

Everything Railway needs is already in the repo:
- **`Dockerfile`** — Railway sees this and builds the image with it (it ignores its own auto-builder when a Dockerfile is present).
- **`railway.toml`** — declares the Dockerfile builder, the start command, and restart policy, so you don't have to type those into the Railway UI.
- The start command binds `0.0.0.0` on Railway's injected `$PORT`, single worker. **Don't add `--workers`** — the app keeps state in one process; multiple workers would give inconsistent results.

---

## What "done" looks like

- A URL like `https://<service>.up.railway.app` loads the explorer.
- `scripts/smoke_explorer.py <url>` prints `SMOKE OK`.
- Editing a `data/*.json` value and pushing to `main` updates the live site with no manual deploy step.
- Cost is ~$5/mo (Railway Hobby plan).

---

## One-time setup

### 1. Confirm the code is on `main`
Merge the `feat/explorer-web-hosting` branch first. Railway builds from a branch (you'll point it at `main`), so the artifacts must be there.

### 2. Create a Railway account + project
1. Go to https://railway.com and sign up (GitHub login is easiest — it also makes step 3 smoother).
2. Add a payment method and select the **Hobby plan** (~$5/mo, always-on). The free trial sleeps and has low limits; Hobby is what keeps the URL warm.

### 3. Connect the GitHub repo
1. **New Project → Deploy from GitHub repo.**
2. Authorize Railway for the `1cFE` org if prompted, then pick **`1cFE/fusion-tea`**.
3. When asked which branch to deploy, choose **`main`**.
   - Railway detects the `Dockerfile` and `railway.toml` automatically — you should **not** need to set a build or start command by hand. If the UI shows a build/start command field, leave it empty (railway.toml supplies them) or paste the start command from `railway.toml`.

### 4. First build & deploy
- Railway starts building immediately. The build runs `pip install -r requirements-serve.txt` then copies the repo tree. Expect a few minutes (the jaxlib/scipy install is the slow part; the image is ~1.16 GB — normal for this app, well within Railway limits).
- Watch the **Deploy Logs**. A healthy start ends with uvicorn logging `Application startup complete` and `Uvicorn running on http://0.0.0.0:<port>`.
- If the build or startup fails, see **Troubleshooting** below.

### 5. Make it public (generate a domain)
1. Open the service → **Settings → Networking** (or **Public Networking**).
2. Click **Generate Domain**. Railway gives you `https://<service>.up.railway.app`.
   - If it asks for a port, it's already handled — the app reads `$PORT`, which Railway injects.

### 6. Verify the deploy
From a clone of the repo (any interpreter — the smoke script is standard-library only):
```bash
python scripts/smoke_explorer.py https://<service>.up.railway.app
# expect: SMOKE OK  page/findings=<id>  compute=<id>  lcoe_per_mwh=<number>
```
Then open the URL in a browser and confirm:
- the matrix/pipeline/compare/cost-landscape/concept pages render, and
- dragging a slider on a cost-model concept updates the headline LCOE (this exercises `/api/compute`).

### 7. Confirm auto-redeploy (push-to-main)
1. Edit one value in a committed `exploration/concept_explorer/data/*.json` (e.g. a display field), commit, push to `main`.
2. Watch Railway: a new deployment should start on its own within seconds — **no GitHub Action, no manual deploy**.
3. After it goes live, re-run the smoke script (or reload the page) and confirm the changed value is visible.

Once steps 6 and 7 pass, the deployment meets its acceptance criteria.

---

## Operating: bumping `1costingfe` (or any serving dependency)

`1costingfe` is pinned **exactly** (`==0.1.0a2`) because the only PyPI release is a pre-release, and because the numerical output must be reviewed whenever it changes. To move to a new version:

1. Edit the pin in **`requirements-serve.in`** (e.g. `1costingfe==0.1.0aN`).
2. Recompile the fully-pinned lockfile (the `--prerelease=explicit` flag is required — it allows the pre-release **only** for the explicitly-pinned `1costingfe`, keeping numpy/scipy/pydantic on stable releases):
   ```bash
   uv pip compile requirements-serve.in -o requirements-serve.txt --prerelease=explicit
   ```
3. **Review the numbers.** Rebuild and smoke locally before pushing, so a bad bump never reaches the live URL:
   ```bash
   sg docker -c 'docker build -t explorer .'        # or plain `docker build` if your shell is in the docker group
   sg docker -c 'docker run --rm -d --name explorer_check -e PORT=8421 -p 8421:8421 explorer'
   python scripts/smoke_explorer.py http://127.0.0.1:8421
   sg docker -c 'docker rm -f explorer_check'
   ```
   Spot-check that a known concept's LCOE is what you expect (concept 01 baseline ≈ **161.69**).
4. Commit **both** `requirements-serve.in` and `requirements-serve.txt`, push to `main`. Railway rebuilds the image and redeploys automatically.

The same edit-recompile-review-push loop applies to bumping any of the other serving libs.

---

## Troubleshooting

- **Build fails on `pip install`** — usually a bad/unresolvable pin in `requirements-serve.txt`. Reproduce locally with `docker build`; fix the `.in`, recompile, push.
- **Deploy "succeeds" but the URL 502s / won't load** — the app didn't bind the right port. Confirm the start command uses `--host 0.0.0.0 --port $PORT` (it's in `railway.toml`). Don't hard-code a port.
- **Pages load but a slider drag errors / `/api/compute` 500s** — a runtime file the compute path needs got excluded from the image. Check `.dockerignore` didn't drop `exploration/concept_analysis/analyses/*/model_setup.py`, `scripts/lib/`, or `tables/archetype_fit.csv`. The local `docker run` + smoke catches this before deploy — always smoke locally after editing `.dockerignore`.
- **Findings page shows nothing for some concepts** — those concepts read their analysis from `archive/concept_analysis_pre_rework/<slug>/analysis.md`; make sure `.dockerignore` still keeps that subtree.
- **Push to `main` didn't redeploy** — check the service's connected branch is `main` (Settings → the GitHub trigger/branch). Railway redeploys only on pushes to the connected branch.
- **First request is slow after idle** — not expected on Hobby (always-warm). If you ever fall back to a sleeping free tier (HF Spaces / Render free), the first request after sleep re-imports JAX and is slow; that's inherent to those tiers, not a bug.

---

## Notes / decisions of record

- **Public by design.** The service has no auth and serves the full analysis findings (only display names/companies are anonymized). This is intentional.
- **Single worker is load-bearing.** Don't scale to multiple workers/replicas without redesigning state handling.
- **Image size ~1.16 GB** is the CPU-JAX floor (jaxlib + scipy + numpy); the heavy *pipeline* deps (torch/docling/agentic-mbse/sysml-codegen) are excluded. Fine for Railway.
- **Fallback platforms** (documented, not set up): Render uses the same Dockerfile with native push-to-main (`$PORT` injected). Hugging Face Spaces needs the container to listen on 7860 (`app_port: 7860` in the Space README) and deploys by pushing to the **HF** git remote, not GitHub — so GitHub push-to-main does **not** auto-deploy there.
