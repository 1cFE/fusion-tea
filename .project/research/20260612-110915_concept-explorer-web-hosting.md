---
date: 2026-06-12T11:09:15-07:00
researcher: Claude
topic: "Hosting the concept-explorer as a web service (Vercel/Railway/alternatives) with push-to-main CI/CD"
tags: [research, concept-explorer, hosting, deployment, ci-cd, fastapi, jax]
status: complete
last_updated: 2026-06-12
---

# Research: Hosting the Concept Explorer as a Web Service

**Date**: 2026-06-12T11:09:15-07:00
**Researcher**: Claude
**Research Type**: Architecture / Integration / Deployment feasibility

## Research Question

Can we host the concept-explorer as a web service that is (1) easy to set up, (2) supports all our Python dependencies, (3) redeploys on every push to `main` — including source-data changes and dependency-version bumps (e.g. a new `1costingfe` release), and (4) is low-cost or free? The owner is weighing **Vercel vs Railway**, and notes that `1costingfe` is now on PyPI (https://pypi.org/project/1costingfe/) and the sibling packages could be published too if needed.

## Summary

- **The explorer is a stateful, long-running FastAPI/uvicorn server — not a static site.** `POST /api/compute` dynamically imports each concept's `model_setup.py` at request time and runs **JAX** (`costingfe`) computations, keeping ~46 concept JSONs and precomputed similarity/constellation data in memory across requests (`server.py:1038`, `server.py:960`, `server.py:925`). This single fact drives every hosting decision.
- **Vercel is the wrong tool and should be ruled out.** It runs ephemeral serverless functions (no persistent in-memory state), and its Python function bundle ceiling (~500 MB, AWS-Lambda-enforced, not configurable) is blown by `jaxlib` alone (327 MB installed) before anything else. Cold starts would re-import JAX on every wake — the exact cost the architecture avoids by staying warm.
- **Railway Hobby ($5/mo) is the best fit**, and matches all four requirements cleanly: native git push-to-main auto-deploy (no GitHub Actions, no Dockerfile required), native `uv`/`pyproject.toml` build via Railpack, always-warm process (no JAX cold-start, in-memory state survives), 48 GB RAM ceiling. **Hugging Face Spaces (free, 16 GB RAM, native git deploy)** is the best *truly-free* option if a 48-hour idle-sleep is acceptable.
- **Two blockers must be fixed before any platform will build**, both in `pyproject.toml`:
  1. The three sibling packages are pinned to **local editable paths** (`costingfe = { path = "../1costingfe" }`, plus `agentic-mbse`, `sysml-codegen`) that don't exist in a clean clone — the build fails immediately. Fix: point `costingfe` at PyPI `1costingfe`, and **drop `agentic-mbse` + `sysml-codegen` from the serving install entirely** (the explorer never imports them at runtime).
  2. The full dependency tree is **6.1 GB installed** — dominated by `torch` (1.1 GB), pulled transitively by `agentic-mbse[extract-full]`→`docling`. The explorer needs none of that to serve. A **slim serving dependency set is ~400 MB** (jaxlib is the floor), which fits every container platform comfortably.
- **CI/CD is essentially free** on Railway/Render/HF: connect the GitHub repo once; every push to `main` rebuilds and redeploys. Source-data changes (the committed `data/*.json`) ship automatically. Dependency bumps flow by editing the version pin in `pyproject.toml` and pushing — the platform won't auto-redeploy when `1costingfe` publishes a new PyPI release, so a version-bump commit (or a tiny scheduled job) is the trigger.

---

## Detailed Findings

### 1. Architecture — this is a server, not a static export

The README's mental model ("HTML pages are structural shells, all data fetched via `/api/*`", `README.md:107`) can mislead toward "just host the static `dist/`." It is **not** a static site. Three runtime behaviors require a live Python process:

- **`POST /api/compute` (`server.py:1038`, `_compute_cached` `server.py:960`)** — slider what-if recompute. For a costingfe-backed concept it calls `_load_model_module()` (`server.py:160`) to **import the concept's `model_setup.py` from disk at request time**, reads its module-level `model`/`result_1gw`/`overrides`/`P_native`, and re-runs `model.forward(...)` — a **JAX** computation (`costingfe`). LRU-cached per `(concept_id, overrides, apply_analyst_overrides)`.
- **In-memory state built once at startup** — `_load_data()` loads all concept JSONs; `_load_taxonomy()` precomputes the full similarity matrix + constellation (`server.py:640-653`); `_stamp_identity()` overlays canonical names. This is held in `app.state.data` for the process lifetime (`server.py:941`). A serverless model that spins a fresh instance per request recomputes all of this every cold start.
- **`GET /api/concepts/{id}/findings` (`server.py:745`)** renders concept-analysis markdown (`analysis.md`, archived fallbacks) to HTML on demand from the sibling `concept_analysis/analyses/` tree.

**Implication:** the deploy target must be a persistent process (uvicorn) with the repo's `exploration/` tree present on disk, not a static-file host or a stateless function.

### 2. Runtime dependency surface — slim vs full (the size story)

The project `pyproject.toml` install is enormous and almost entirely irrelevant to serving:

| Package | Installed size | Needed to **serve** the explorer? | Why it's there |
|---|---|---|---|
| `torch` | **1.1 GB** | **No** | Transitive via `agentic-mbse[extract-full]` → `docling` |
| `scipy` | 94 MB | No | Transitive (extraction/codegen side) |
| `jaxlib` | **327 MB** | **Yes** | `costingfe` compute engine |
| `jax` | 21 MB | Yes | `costingfe` |
| `docling` | 2.5 MB (+models) | No | PDF extraction pipeline only |
| **Full `.venv`** | **6.1 GB** | — | Includes the entire analysis/extraction toolchain |

What the explorer actually imports at runtime (verified by grepping every `concept_explorer/*.py` and every `analyses/*/model_setup.py`):

- **Serving the app**: `fastapi`, `uvicorn[standard]`, `jinja2`, `pydantic>=2`, `markdown` (findings), `pyyaml`, `numpy` (similarity).
- **`POST /api/compute` only**: `costingfe` (→ `jax`, `jaxlib`), plus the **in-repo** `lib.model_setup_helpers` (which imports `costingfe.validation`) — every `model_setup.py` does `from costingfe import ...` and `from lib.model_setup_helpers import ...`.
- **Never imported by the explorer at runtime**: `agentic-mbse`, `sysml-codegen`, `docling`, `torch`, `pymupdf*`, `gmft`, `matplotlib`, `pyzotero`, `graphviz`. These belong to the extraction/analysis/codegen pipelines, which run *offline* to produce the committed `data/*.json` and the `analyses/` artifacts.

**A slim serving install is ~400 MB** (jaxlib dominates). That fits Railway/Render/Fly/HF/Cloud Run easily and is the single most important deployment optimization.

### 3. What must be on disk at runtime

The deploy is the **repo itself** (git clone), not a pip-installed package — because compute loads `.py` files and findings reads `.md` files by path. Required tracked paths:

- `exploration/concept_explorer/` — server, models, `static/` (1.9 MB incl. vendored Plotly 1.0 MB + Cytoscape 0.4 MB), `templates/`, and **committed `data/*.json`** (1.4 MB, 46 files, all tracked — confirmed via `git ls-files`).
- `exploration/concept_analysis/analyses/*/model_setup.py` + `analysis.md` (+ archived fallback `archive/concept_analysis_pre_rework/`). The `analyses/` tree is **7.7 MB excluding `iter-*/`** (22 MB with them — those intermediate dirs are not needed at runtime and could be excluded from the deploy).
- `exploration/concept_analysis/scripts/lib/` — `model_setup_helpers.py` and siblings (model_setup.py walks up `sys.path` to find `scripts/`).
- `exploration/concept_analysis/tables/archetype_fit.csv` — read by `_load_fit_grades` (`server.py:445`); non-fatal if absent.

Nothing here needs R2 binaries or the `knowledge/concept_research/` corpus — those are gitignored and irrelevant to the explorer.

### 4. The local-editable-path blocker and the PyPI fix

`pyproject.toml` currently has:

```toml
[tool.uv.sources]
costingfe   = { path = "../1costingfe",   editable = true }
agentic-mbse = { path = "../agentic-mbse", editable = true }
sysml-codegen = { path = "../sysml-codegen", editable = true }
```

A clean clone on any host has no sibling repos → `uv sync` fails. `1costingfe` being on PyPI solves the only one that matters for serving:

- **Name nuance**: the local package's distribution name is `costingfe` (`name = "costingfe"`, import package `src/costingfe/`), but it is **published on PyPI as `1costingfe`** (PyPI names can't start with a digit-free collision; the "1" prefix is the published dist). So the deploy must depend on **`1costingfe`** and `import costingfe` keeps working. **Action item to verify at implementation time**: confirm `pip install 1costingfe` exposes `import costingfe` and that the published version matches the local `0.1.0` API the explorer relies on (`forward(..., cost_overrides=, override_reference_mw=)`, `model.sensitivity()`, `ConfinementConcept`, `Fuel`).
- `agentic-mbse` and `sysml-codegen` should simply **not be in the serving dependency set** (see §2). Publishing them to PyPI is unnecessary for hosting; only do it if some *other* consumer needs them. (`costingfe`'s own deps are clean and small: `jax`, `jaxlib`, `pydantic`, `pyyaml`.)

**Recommended mechanism** — a dedicated serving dependency group so the offline pipeline install is untouched:

```toml
[project.optional-dependencies]
serve = [
  "1costingfe>=<pinned>",
  "fastapi>=0.128.0", "uvicorn[standard]>=0.40.0",
  "jinja2>=3.1.6", "pydantic>=2", "pyyaml>=6.0.3",
  "markdown>=3.10.2", "numpy>=2.4.0",
]
```

Then the host runs `uv sync --extra serve` (or `uv pip install .[serve]`) and `uvicorn exploration.concept_explorer.server:app`. This sidesteps the 6.1 GB tree and the path-deps in one move. (Alternative: a separate slim `requirements-serve.txt`, or a Dockerfile that installs only the slim set — see §6 on which platforms need a Dockerfile.)

### 5. Platform comparison (2026 facts — verify free-tier terms at signup)

| Platform | Persistent server? | Push-to-main, **no** GH Actions? | Dockerfile needed? | `uv` support | Cheapest | Fit |
|---|---|---|---|---|---|---|
| **Railway** | Yes — always warm, no scale-to-zero | **Yes** | No (Railpack auto-detects) | Native | $5/mo Hobby (incl. $5 usage); one-time $5 trial | **Best** |
| **Render** | Paid always-on; free **spins down** ~30-60 s cold | **Yes** | No (Docker optional) | Build cmd / Docker | Free (sleeps, 512 MB) / $7+/mo Starter | Good (use paid; size RAM up) |
| **Hugging Face Spaces** | Free **sleeps at 48 h** idle; paid always-on | **Yes** (git push to Space) | Optional (Docker SDK) | Docker/requirements | Free CPU Basic **2 vCPU / 16 GB** | **Best free** (if 48 h sleep ok) |
| **Fly.io** | Yes (scale-to-zero opt) | **No** — `fly deploy` / GH Action | Effectively yes | Via Dockerfile | No perma-free; ~$2-5/mo | OK, more wiring |
| **Koyeb** | Yes (scale-to-zero opt) | Yes | No (buildpack) | Buildpack/Docker | Free svc **512 MB** (too small for JAX) / $29 Pro | Free RAM too small |
| **Cloud Run** | Scales to zero (cold start) | **No** — Cloud Build trigger/GH Action | No (buildpacks) | Buildpack/Docker | Generous perma-free tier | Powerful; cold-start fights JAX |
| **Vercel** | **No** (ephemeral functions) | n/a | n/a | n/a | Hobby free | **Avoid** |

Notes that matter for *this* app:

- **Vercel — ruled out, concretely**: serverless functions don't keep in-memory state across invocations (the 46-JSON warm cache + similarity matrix + LRU compute cache all break); the Python bundle limit (~500 MB uncompressed, Lambda-enforced, non-configurable) is exceeded by `jaxlib` (327 MB) + everything else; every cold invocation re-imports JAX. Wrong execution model on all three axes.
- **Railway**: Railpack reads `pyproject.toml`/`uv.lock`, runs `uv sync`. With the `serve` extra you'd set the install/start commands (`uv sync --extra serve`; `uvicorn ...server:app --host 0.0.0.0 --port $PORT`). Always-warm = no JAX cold start. 48 GB RAM ceiling is far more than needed.
- **Render free tier** spins down after 15 min idle with a 30-60 s cold start, and base RAM is 512 MB — tight once JAX + data are resident. Use the $7 Starter and size RAM up if chosen.
- **HF Spaces** free CPU Basic gives **16 GB RAM** and native git-push deploy; the catch is the 48 h idle sleep on free hardware (can't customize sleep on cpu-basic). For an internal analyst tool used in bursts, a 48 h sleep + slow first request may be perfectly acceptable — making this the best zero-cost option.

### 6. CI/CD design — push-to-main, source data, and dependency bumps

The repo is already on GitHub (`origin → https://github.com/1cFE/fusion-tea.git`), so native git integration is available immediately on Railway/Render/HF.

- **Push-to-main → redeploy**: connect the repo once in the platform UI; select branch `main`. No `.github/workflows/*` needed on Railway/Render/HF/Koyeb. (Fly.io and Cloud Run are the exceptions — they need `fly deploy` / a Cloud Build trigger, i.e. a GitHub Action you author.)
- **"All the source data"**: the explorer reads committed `data/*.json` + the `analyses/` tree. A commit that changes any of those *is* a push to main, so the redeploy ships them automatically. No separate data-sync step (contrast the legacy `.github/workflows/notify_visualization.yml`, which fires a `repository_dispatch` to a **separate** older viz repo `fusion-tea-walkthrough-visualization` on `model_output.txt` changes — that is a different visualization, not this explorer, and is not the pattern to copy here).
- **"Dependency version updates (e.g. 1costingfe updates)"**: with `1costingfe` pinned in `pyproject.toml`, a new PyPI release does **not** auto-trigger fusion-tea's deploy (the platform only watches the fusion-tea repo). The clean trigger is a one-line version-bump commit to `main` (manual, or automated with Dependabot/Renovate, or a small scheduled GH Action that bumps + pushes when a new `1costingfe` appears). If you'd rather have *latest-on-every-deploy*, pin loosely (`1costingfe>=X`) and force periodic rebuilds — but reproducible pinned builds are the safer default for a quantitative tool.
- **Build determinism**: commit `uv.lock` (already tracked) and have the platform honor it, so deploys are reproducible.

### 7. Secondary considerations

- **`claude` CLI dependency**: only `extract_explorer_data.py`'s narrative step shells out to `claude -p` (`README.md:688`). That runs **offline** to produce `data/*.json`; the *server* never calls it. No LLM/API key is needed in the deployed environment.
- **Binding host**: `server.py:1107` runs `uvicorn.run(app, host="127.0.0.1", ...)`. For a container the start command must bind `0.0.0.0` and read `$PORT` (use `uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT` rather than `python server.py`, or parameterize `main()`).
- **`dist/` is rendered at startup** from templates into a writable dir (`server.py:939`, gitignored) — fine on any container with a writable filesystem; no prebuild step required.
- **State endpoint is in-memory and process-local** (`/api/state`, resets on restart, single-worker assumption). Run **one uvicorn worker** (the LRU caches and `app.state` assume a single process); don't scale to multiple replicas without rethinking shared state.
- **Auth/visibility**: nothing in the app restricts access. If the explorer should not be public (company names, internal analysis), put it behind the platform's access control or basic auth — the generic-name/company-disclaimer overlay (`server.py:336-417`) anonymizes display names but the underlying analysis findings are served in full.

## Code References

- `exploration/concept_explorer/server.py:1038` — `compute()` endpoint (runtime JAX recompute).
- `exploration/concept_explorer/server.py:960-1036` — `_compute_cached`, dynamic `model_setup.py` import + `model.forward()`.
- `exploration/concept_explorer/server.py:160-175` — `_load_model_module` (imports concept `.py` at request time).
- `exploration/concept_explorer/server.py:925-952` — lifespan: loads all data + taxonomy + similarity into `app.state`.
- `exploration/concept_explorer/server.py:745-770` — findings endpoint (reads sibling `analyses/` markdown).
- `exploration/concept_explorer/server.py:1107` — `uvicorn.run(host="127.0.0.1")` (must become `0.0.0.0`/`$PORT`).
- `exploration/concept_analysis/analyses/*/model_setup.py:19-20` — `from costingfe import ...` + `from lib.model_setup_helpers import ...` (the runtime import contract).
- `pyproject.toml` `[tool.uv.sources]` — the three local editable path deps (the build blocker).
- `../1costingfe/pyproject.toml` — costingfe deps are `jax`, `jaxlib`, `pydantic`, `pyyaml` (clean, small).
- `.github/workflows/notify_visualization.yml` — legacy cross-repo dispatch for a *different* (walkthrough) visualization; not the model for this explorer.

## Architecture Insights

- The "structural shells + API" design is good for hosting: re-extracting data doesn't require re-rendering templates, and the only mutable build artifact (`dist/`) regenerates at startup. But it is a *server* architecture — the API is not optional.
- The single hardest constraint is **JAX at request time**. It both rules out serverless (cold-start + size) and argues for an always-warm process. Everything else (data, templates, static) is small and trivial to ship.
- The project already separates "offline pipeline" from "online serving" *conceptually* (data is committed, narrative runs offline). The deployment just needs to make that split **explicit in the dependency manifest** (the `serve` extra), which also fixes the 6.1 GB → ~400 MB problem.

## Feasibility Assessment

**Feasible and low-effort**, contingent on two `pyproject.toml` changes:

1. Add a slim `serve` optional-dependency group depending on PyPI `1costingfe` (not the local path), and excluding `agentic-mbse`/`sysml-codegen`.
2. Make the server bind `0.0.0.0:$PORT` for containers.

With those, Railway can deploy from the existing GitHub repo with zero GitHub Actions and no Dockerfile. Risks/prerequisites:

- **PyPI `1costingfe` parity** — must confirm the published version exposes `import costingfe` with the API surface the explorer uses (the local dep is `0.1.0`; verify the PyPI release is at/after the API the compute path needs). This is the one item that could bite.
- **Build size/time** — only an issue if the slim split isn't done; with it, ~400 MB is unremarkable.
- **Single-worker assumption** — fine for an internal tool; documented, not a blocker.

## Recommendations

1. **Primary: Railway Hobby ($5/mo).** Native push-to-main (no Actions, no Dockerfile), native `uv`, always-warm (no JAX cold start, state survives), generous RAM. Cleanest match to all four requirements.
2. **Free alternative: Hugging Face Spaces (CPU Basic, 16 GB, free).** Native git-push deploy; accept the 48 h idle-sleep + slow first request. Good for an internal/bursty analyst tool with zero spend.
3. **Do NOT use Vercel** for this app (wrong execution model + size limit + JAX cold start). If a Vercel-style static deploy is ever wanted, it would require first removing the compute/findings/state endpoints and pre-baking all data into static JSON — a different, lesser product.
4. **Prerequisite work (small, do first)**:
   - Add the `serve` optional-dependency group pinned to PyPI `1costingfe`; verify import parity.
   - Parameterize the uvicorn bind to `0.0.0.0:$PORT`.
   - Set platform install = `uv sync --extra serve`, start = `uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT --workers 1`.
   - Optionally exclude `iter-*/` from the deploy to trim the `analyses/` tree (22 MB → 7.7 MB).
   - Decide access control (public vs basic-auth) given the analysis content is served unredacted.
5. **Dependency-bump CI/CD**: pin `1costingfe` and bump-and-push to redeploy (optionally automate with Renovate/Dependabot or a scheduled bump job). Keep `uv.lock` committed for reproducible builds.

## Open Questions

1. **PyPI `1costingfe` version parity** — does the published release match the local `0.1.0` API (`forward(cost_overrides=, override_reference_mw=)`, `sensitivity()`, three-forward `result_1gw`)? Must verify before pinning. If it lags, either publish a new release or deploy `costingfe` from a git ref instead of PyPI.
2. **Public or private?** Should the hosted explorer be internet-public, or behind auth/VPN? Affects platform choice details (HF Spaces can be private; Railway needs an auth layer you add).
3. **Always-on vs sleep tolerance** — is a 48 h idle-sleep + slow first request acceptable (→ free HF Spaces), or is always-warm required (→ Railway/Render paid)?
4. **Single instance acceptable?** The in-memory `/api/state` and LRU caches assume one process. Confirm no need for horizontal scaling.
5. **Do the sibling packages (`agentic-mbse`, `sysml-codegen`) ever need PyPI publication** for other reasons? Not required for hosting the explorer; only relevant if another external consumer appears.
