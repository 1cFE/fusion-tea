# Design: Concept Explorer Web Hosting

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-14 16:52 PDT
**Complexity:** MEDIUM
**Branch:** TBD (suggest `feat/explorer-web-hosting`)

## Overview

Deploy the concept-explorer FastAPI server as a public, always-warm web service on Railway, built from a single small Dockerfile that installs a slim serving-only dependency set and runs the existing app from the cloned repo tree — no application code changes — with native push-to-main auto-deploy.

## Related Artifacts

- **Spec:** `.project/active/explorer-web-hosting/spec.md`
- **Research:** `.project/research/20260612-110915_concept-explorer-web-hosting.md`
- **Explorer reference:** `exploration/concept_explorer/README.md`
- **Parity evidence:** spec appendix "Parity Verification (2026-06-14)"

## Research Findings

**Codebase (drives the "zero code change" result):**
- `exploration/concept_explorer/server.py:1090` — module-level `app = create_app()`; lifespan runs only when uvicorn starts. So `uvicorn exploration.concept_explorer.server:app` works as a start target.
- `server.py:1098-1107` — `main()` hardcodes `127.0.0.1` and `--port`, but is bypassed entirely when we invoke uvicorn by import string with `--host 0.0.0.0 --port $PORT`.
- `server.py:35-37` — inserts project root on `sys.path` at import; the compute path inserts `concept_analysis/scripts` (`server.py:134-137`). Both resolve correctly when the repo tree is present and CWD is repo root.
- `pyproject.toml` has **no `[build-system]`** → uv treats fusion-tea as a *virtual* project (deps only, never built/installed). The explorer runs from source on disk, so the deploy is "repo tree + third-party deps," not a wheel.
- Runtime import surface (verified): serving needs `fastapi, uvicorn[standard], jinja2, pydantic, pyyaml, markdown, numpy`; `/api/compute` adds `costingfe` (→ jax/jaxlib) + in-repo `lib.model_setup_helpers`. Nothing needs `agentic-mbse`/`sysml-codegen`/`docling`/`torch`.
- 801 tracked files live under `iter-*/` (intermediate analyzer artifacts) — not needed at runtime; excluded from the build context.

**Platform/tooling (web):**
- uv issue **#11675**: `uv sync --only-group`/`--no-extra` *still evaluates* `[tool.uv.sources]` `path =` entries not in the selected set → a slim `uv sync` fails building `../1costingfe` on a clean clone. ([github.com/astral-sh/uv/issues/11675](https://github.com/astral-sh/uv/issues/11675))
- Railway custom build command "is run *after* languages and packages have been installed" — i.e. Railpack auto-runs `uv sync` first when it detects `uv.lock`, so it would fail before our command. ([docs.railway.com/builds/build-and-start-commands](https://docs.railway.com/builds/build-and-start-commands))
- Railway with a Dockerfile **ignores Railpack**, rebuilds the image on every push to the connected branch, and injects `$PORT`. ([docs.railway.com/deployments/github-autodeploys](https://docs.railway.com/deployments/github-autodeploys), [docs.railway.com/builds/build-configuration](https://docs.railway.com/builds/build-configuration))
- HF Spaces Docker SDK: container must listen on **7860** (or set `app_port` in README frontmatter); deploy is a git push to the Space repo. ([huggingface.co/docs/hub/spaces-sdks-docker](https://huggingface.co/docs/hub/en/spaces-sdks-docker))

## Core Concept

The explorer already runs as `uvicorn server:app` from the source tree; the *only* thing that stops it running in the cloud is that `pyproject.toml` pins three sibling packages to local paths that don't exist on a clean clone, and drags in a 6.1 GB extraction toolchain it never uses to serve. The design is therefore not "build a deployment system" — it is "describe a clean container that installs only the ~8 serving deps and runs the app unchanged." A **Dockerfile** is the right unit because it sidesteps `pyproject`/`uv.lock`/`[tool.uv.sources]` completely (so the offline pipeline install stays untouched), pins the install deterministically, and is the *same artifact* every candidate platform consumes. CI/CD is then a property of the platform, not code we write: Railway (and Render) rebuild the Dockerfile on every push to `main`. The result is zero application code change, one new manifest (`requirements-serve.txt`), one Dockerfile, and one optional `railway.toml`.

## Key Bets

- **B1.** A single always-warm uvicorn process is sufficient for expected traffic (internal analysts + occasional public viewers). *If false → in-memory `/api/state`, the LRU compute cache, and `app.state` give inconsistent results under concurrent load and we need externalized state / multi-worker (a different design).* (Hosting confirmed 2026-06-14: **Railway, always-on** — HF-free fallback not chosen, kept documented only.)
- **B2.** The cloud build context contains the full runtime tree — `concept_explorer/` (with committed `data/`, `static/`, `templates/`), `concept_analysis/analyses/*/{model_setup.py,analysis.md}`, `concept_analysis/scripts/lib/`, `concept_analysis/tables/archetype_fit.csv`, and `archive/concept_analysis_pre_rework/`. *If false → `/api/compute` and `/api/concepts/{id}/findings` 500 at runtime even though pages load.*
- **B3.** `1costingfe` remains installable from PyPI at the verified version and is numerically identical to local. *If false → slider recompute returns wrong or failed numbers.* (Already verified 2026-06-14; near-zero residual risk.)

## Key Decisions

- **D1. [CONFIRMED 2026-06-14]** **Dockerfile** as the build unit (Railway, Render, HF all consume it). *Rejected: native uv build — verified by test that uv treats one `pyproject.toml` as an indivisible resolution: it fails the whole lock on the `[tool.uv.sources]` local paths even when those deps are optional and not installed (uv #11675, reproduced 2026-06-14: optional-group+path → fail; optional-group+unpublished → fail; slim-only → works). Making the native build work would require gutting `pyproject.toml` to serving-only + publishing agentic-mbse/sysml-codegen to PyPI + a new dev-side editable mechanism — far more invasive than one 12-line Dockerfile that leaves `pyproject.toml` untouched.* The spec's "no Dockerfile" preference is consciously overridden; the Dockerfile is the lighter touch here.
- **D2.** A standalone **`requirements-serve.txt`** as the serving manifest. *Rejected: a `pyproject` `serve` extra or PEP-735 group — extras are additive (don't exclude the heavy base deps) and groups still evaluate the path sources (#11675). A separate file bypasses `pyproject` entirely, so FR-3 "pipeline install unchanged" is satisfied by construction.*
- **D3.** **No application code changes**; host/port supplied by the uvicorn start command against the module-level `app`. *Rejected: editing `main()` to read env vars — unnecessary, and would still be bypassed by the import-string start command. (Optional nicety, deferred.)*
- **D4.** Pin `requirements-serve.txt` fully via **`uv pip compile`** (direct + transitive). *Rejected: hand-pinning only direct deps — weaker reproducibility for a quantitative tool; jax/jaxlib transitive pins matter for numerical determinism.*
- **D5.** **Manual** version-bump trigger for `1costingfe` (edit pin → push). *Rejected (for now): Renovate/Dependabot auto-PRs — the PyPI release is a pre-release and numerical output must be reviewed on bump; automation can be added later without redesign.*

## Architecture

```
GitHub: 1cFE/fusion-tea @ main
   │  (push → native webhook, no GH Actions)
   ▼
Railway service ── builds Dockerfile (ignores Railpack)
   │   build:  pip install -r requirements-serve.txt   ← slim set, no path deps
   │   image:  python:3.12-slim + repo tree (minus .dockerignore)
   ▼
Container (1 process, 1 worker)
   uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT
   │   lifespan: _load_data() + _load_taxonomy() + _stamp_identity() + render dist/
   ▼
Public URL  ──  /  /compare  /cost-landscape  /concept/{id}
                /api/* (manifest, concepts, compute[JAX], findings, taxonomy)
```

- **Boundary:** the deploy never touches `pyproject.toml`/`uv.lock`/`[tool.uv.sources]`. Dev keeps using `uv sync` (path deps); the cloud uses the Dockerfile (`requirements-serve.txt`). Two non-overlapping install paths over one source tree.
- **Data flow at runtime:** unchanged from local — pages are shells, data comes from `/api/*` reading the in-memory state built at startup from committed `data/*.json`; compute dynamically imports `model_setup.py` by path.
- **CI/CD flow:** source-data edits and the `1costingfe` pin both live in the repo, so a push to `main` is the single trigger that ships them.

## Required Invariants

1. **Single worker / single process** — uvicorn started with no `--workers` (or `--workers 1`). `app.state`, `_compute_cached` LRU, and in-memory `/api/state` assume one process.
2. **Runtime tree present & rooted** — the container runs with CWD = repo root and the `exploration/` + `archive/` trees in place at their committed relative paths (B2).
3. **`import costingfe` resolves** to the PyPI `1costingfe` build at the pinned version; `agentic-mbse`/`sysml-codegen`/`torch`/`docling` are **absent** from the image.
4. **Writable filesystem** — `dist/` is rendered at startup (`server.py:939`); the container FS must be writable (default for all three platforms).
5. **App code unchanged** — `server.py` et al. are byte-identical to `main`; the deploy is config-only.

## Component Overview

New artifacts (all small, repo-root unless noted):
- **`requirements-serve.txt`** — fully-pinned slim serving deps (compiled from a short `requirements-serve.in`). The single source of truth for the deployed environment.
- **`Dockerfile`** — `python:3.12-slim`, copy repo, `pip install -r requirements-serve.txt`, `CMD` shell-form uvicorn binding `0.0.0.0:${PORT}`. ~12 lines.
- **`.dockerignore`** — excludes `.git`, `.venv`, `knowledge/concept_research/**` binaries, `**/iter-*/`, logs, caches, `archive/*` except the findings fallback. Keeps the build context small.
- **`railway.toml`** — declares Dockerfile builder + start command + restart policy (config-as-code so the service is reproducible from the repo). Optional but recommended.
- **`RUNBOOK.md`** (in the work-item dir) — the operator steps (account/billing/connect/verify) and the `1costingfe` bump procedure (FR-8). Seeded from the spec appendix.

Unchanged but load-bearing: `exploration/concept_explorer/server.py` (run target), the committed `data/`, and the `concept_analysis/` runtime tree.

## Non-Goals

- No multi-worker / horizontal scaling / externalized session state (B1).
- No change to `pyproject.toml`, `uv.lock`, or the offline pipeline install (FR-3).
- No auth — the service is public by decision (spec).
- No custom domain / TLS beyond platform defaults.
- No static-only export (would drop compute/findings/state — explicitly not pursued).
- No `main()` refactor (start command supersedes it).

## Implementation Notes

- **CMD must expand `$PORT`** → shell form, with a local default:
  `CMD ["sh","-c","uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port ${PORT:-8421}"]`
  (Exec-form `["uvicorn",...]` would not expand the variable.)
- **Build context vs runtime tree**: `.dockerignore` trims `iter-*/` (801 files) and R2/`.git` bulk, but must **keep** `analyses/*/model_setup.py`, `analyses/*/analysis.md`, `scripts/lib/`, `tables/archetype_fit.csv`, and `archive/concept_analysis_pre_rework/` (findings fallback, `server.py:760`).
- **`requirements-serve.txt` generation**: `uv pip compile requirements-serve.in -o requirements-serve.txt`; `.in` lists `1costingfe==0.1.0a2` (exact — pre-release) + the 7 serving libs. Regenerate on any bump; commit both.
- **HF Spaces nuance**: a Space is a *separate* git repo, so GitHub push-to-main does **not** auto-deploy there — you push to the HF remote (or add a mirror GH Action). Set `app_port: 7860` in the Space README and pass `PORT=7860`. Documented as fallback only.
- **Render**: Dockerfile auto-detected, native GitHub push-to-main, `$PORT` injected — works with the same Dockerfile, no extra files.
- **Public content reminder**: `/api/concepts/{id}/findings` serves full analysis prose; only display names are anonymized. Intended (spec), but flag at review.

## Potential Risks

- **Build context too large / slow** → mitigate with `.dockerignore` (drop `.git` via platform clone depth, R2 binaries already gitignored, `iter-*/`). Target image ≈ 400–500 MB (jaxlib floor).
- **`$PORT` not expanded / wrong host** → 502 on Railway. Mitigated by shell-form CMD + local `docker run` validation before connecting the platform.
- **Missing runtime file** (e.g. an over-aggressive `.dockerignore` drops `scripts/lib/`) → pages load but compute/findings 500. Mitigated by the post-build smoke test hitting `/api/compute` and `/api/concepts/{id}/findings`.
- **PyPI pre-release drift** → bare `1costingfe` could stop resolving the alpha once a stable ships; exact pin + committed `requirements-serve.txt` removes this.
- **Cold start on a sleeping fallback** (HF free) re-imports JAX (~slow first request) — acceptable for fallback, non-issue on always-warm Railway.

## Integration Strategy

- Adds a parallel, config-only deploy path; the existing dev workflow (`uv run python ... server.py`, `uv sync`) is untouched. Complements, replaces nothing.
- The legacy `.github/workflows/notify_visualization.yml` targets a *different* walkthrough viz repo and is left as-is (not the pattern for this explorer).
- Dependency bumps integrate through normal PRs: bump `requirements-serve.in`, recompile, push → auto-redeploy.

## Validation Approach

1. **Local image parity** — `docker build`; `docker run -e PORT=8421 -p 8421:8421`; curl `/api/health`, load `/concept/01`, `POST /api/compute` for a costingfe concept → recomputed LCOE. Confirms the slim image serves the full feature set before any cloud spend.
2. **Slim-set assertion** — `pip list` in the image shows no `torch`/`docling`/`agentic-mbse`/`sysml-codegen`; image size near target.
3. **Cloud smoke test** — after Railway deploy: same endpoint checks against the live URL + one slider recompute (FR-5, FR-7).
4. **CI/CD proof** — push a trivial `data/*.json` change to `main`; confirm the live site updates with no manual action (FR-6).
5. **Regression** — `uv run python -m pytest exploration/concept_explorer/tests/` still passes; `uv sync` (pipeline install) still works (FR-3).

## Next-Stage Handoff

**Fixed for the plan:**
- Dockerfile + `requirements-serve.txt` mechanism; no app code change; single worker; Railway primary with the same Dockerfile for Render/HF fallbacks.
- `1costingfe==0.1.0a2` exact pin from PyPI.

**Open for the plan to settle:**
- Exact `.dockerignore` keep/drop list and base image (`python:3.12-slim` vs `-bookworm`).
- Whether `railway.toml` is committed or the service is UI-configured.
- `requirements-serve.in` exact version pins for the 7 non-costingfe libs (match current `uv.lock`).
- Whether to also make `main()` env-aware (optional).

**De-risk first:** build and run the image locally (Validation step 1) before touching Railway — it exercises B2 (tree completeness) and the `$PORT`/CMD form, the two most likely failure points.

## Next Steps

After approval → `/_my_plan` (or `/_my_implement`).

---

## Appendix (Optional — does not count toward the main-body budget)

### A. Dockerfile sketch (~12 lines, plan will finalize)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements-serve.txt .
RUN pip install --no-cache-dir -r requirements-serve.txt
COPY . .
CMD ["sh","-c","uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port ${PORT:-8421}"]
```

### B. requirements-serve.in (pre-compile input)

```
1costingfe==0.1.0a2      # → costingfe import, jax, jaxlib
fastapi
uvicorn[standard]
jinja2
pydantic>=2
pyyaml
markdown
numpy
```
(Compile to fully-pinned `requirements-serve.txt` via `uv pip compile`.)

### C. railway.toml sketch

```toml
[build]
builder = "dockerfile"
[deploy]
startCommand = "uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "on_failure"
```

### D. Platform CI/CD matrix (from research)

| Platform | Same Dockerfile? | Push-to-main auto-deploy, no GH Actions | Port | Notes |
|---|---|---|---|---|
| Railway (primary) | yes | **yes** (native git) | `$PORT` injected | always-warm; $5/mo |
| Render | yes | **yes** (native git) | `$PORT` injected | free tier sleeps; paid warm |
| HF Spaces | yes | **no** — push to HF remote or mirror action | 7860 (`app_port`) | free 16 GB, sleeps 48 h |
| Vercel | n/a | n/a | n/a | ruled out (serverless + size) |

### E. Sources

- Railway build/start commands — https://docs.railway.com/builds/build-and-start-commands
- Railway GitHub autodeploys — https://docs.railway.com/deployments/github-autodeploys
- Railway config-as-code — https://docs.railway.com/reference/config-as-code
- uv #11675 (path sources evaluated under `--only-group`) — https://github.com/astral-sh/uv/issues/11675
- HF Docker Spaces — https://huggingface.co/docs/hub/en/spaces-sdks-docker
