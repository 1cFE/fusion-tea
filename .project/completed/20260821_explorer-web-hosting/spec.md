# Spec: Concept Explorer Web Hosting

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-14 16:52 PDT
**Complexity:** MEDIUM
**Branch:** TBD (suggest `feat/explorer-web-hosting`)

---

## Work Item Summary

Make the concept-explorer — today a localhost-only FastAPI/uvicorn server — deployable and deployed as a public web service on Railway, redeploying automatically on every push to `main`. The work splits the project's 6.1 GB pipeline install from a slim ~400 MB serving install (a new `serve` dependency group pinned to PyPI `1costingfe`), fixes the container prerequisites (bind `0.0.0.0:$PORT`, single worker), and ends with a live URL plus a runbook for the manual account/billing/connect steps the owner performs. "Done" means a collaborator can open a URL and use the explorer without running the local toolchain, and a push to `main` updates that URL with no manual deploy step.

## Why This Matters Now

The explorer is the primary way the fusion-TEA analysis becomes legible to anyone who isn't running the repo. Right now sharing it means asking someone to clone a 7+ GB repo and run a server. Hosting it removes that barrier and makes the committed analysis data and the live what-if compute available behind a link, which is the point of having built the explorer.

## Key Bets / Constraints

- **Bet (RESOLVED ✓):** PyPI `1costingfe` is API-compatible with the local `costingfe 0.1.0`. **Verified 2026-06-14** — see "Parity Verification" below. The one external risk is retired.
- **Bet:** The explorer needs only `costingfe` + a handful of small libs to *serve* — `agentic-mbse`, `sysml-codegen`, `docling`, `torch` are pipeline-only and can be excluded from the deploy (established in research §2).
- **Constraint:** The deploy is the **repo itself** (git clone), not a pip-installed package — compute loads `model_setup.py` files and findings reads `.md` files by path. The `exploration/` tree must be present at runtime.
- **Constraint:** Single uvicorn process / single worker — `app.state`, the LRU compute cache, and in-memory `/api/state` assume one process.
- **Non-goal:** Re-architecting for horizontal scale or shared/persistent state.
- **Non-goal:** Changing the offline extraction/analysis pipeline, or publishing the sibling packages to PyPI.
- **Non-goal:** Access control / auth — the service is intentionally **public** (see Edge Cases).

---

## Business Goals

### Why This Matters

Collaborators and stakeholders should be able to explore fusion-concept economics through a link, not a local dev environment. The hosting also exercises the "offline pipeline / online serving" split that the codebase already assumes conceptually but has never made explicit in its dependency manifest.

### Success Criteria

- [ ] A public URL serves the explorer with all currently-committed concepts, working profile/compare/cost-landscape pages, and working slider recompute (`/api/compute`).
- [ ] A push to `main` that changes `data/*.json`, the `analyses/` tree, or the `1costingfe` pin results in an updated live site with no manual deploy action.
- [ ] The owner can reproduce/operate the deployment from a written runbook (account, billing, repo-connect, config).
- [ ] Hosting cost is $0–$5/mo.

### Priority

Next discrete work item; raised directly by the owner. No hard dependency on other active explorer work items, but lands cleanest after the explorer is otherwise stable on `main` (it is).

---

## Problem Statement

### Current State

- The explorer runs only via `uv run python exploration/concept_explorer/server.py`, binding `127.0.0.1:8421` (`server.py:1107`).
- `pyproject.toml` pins the three sibling packages to **local editable paths** (`costingfe = { path = "../1costingfe" }`, plus `agentic-mbse`, `sysml-codegen`) — a clean clone on any host fails `uv sync` immediately.
- The full install is **6.1 GB** (torch 1.1 GB via `agentic-mbse[extract-full]`→docling, scipy, jaxlib 327 MB) — most of it irrelevant to serving.
- There is no CI/CD for the explorer. The one existing workflow (`notify_visualization.yml`) targets a *different*, older walkthrough visualization repo.

### Desired Outcome

A live, public, low-cost URL for the explorer that redeploys on push to `main`, built from a slim serving dependency set, with the manual setup captured as repeatable steps.

---

## Scope

### In Scope

- **Dependency split**: a `serve` optional-dependency group in `pyproject.toml` containing only the serving deps, pinned to PyPI `1costingfe` (not the local path); the offline pipeline install left unchanged.
- **Container prerequisites**: server binds `0.0.0.0` and reads `$PORT`; container-correct start command; single worker.
- **Railway deployment**: GitHub repo connected, branch `main`, native push-to-main auto-deploy (no GitHub Actions, no Dockerfile); install/start commands configured; live URL produced.
- **PyPI parity verification**: confirm `pip install 1costingfe` exposes `import costingfe` with the API the compute path uses, at a version ≥ what the explorer needs; if it lags, fall back to a git-ref dependency.
- **Dependency-bump path**: documented procedure to roll a new `1costingfe` (pin-bump commit → push → redeploy), keeping `uv.lock` committed for reproducibility.
- **Operator runbook**: written steps the owner acts on (account/billing, connect repo, set config vars, verify), included in this work item.
- **Fallback documentation**: Hugging Face Spaces (free, 48 h idle-sleep) and Render (Starter) documented as alternative targets, so the requirements stay platform-neutral where practical.

### Out of Scope

- Auth / access restriction (service is public by decision).
- Horizontal scaling, multi-worker, or externalized session state.
- Publishing `agentic-mbse` / `sysml-codegen` to PyPI.
- Changes to extraction/analysis/codegen pipelines.
- A static-only export of the explorer (would require removing compute/findings/state — explicitly not pursued).
- Custom domain / TLS beyond what the platform provides by default (may be a later follow-up).

### Edge Cases & Considerations

- **Public exposure of content**: only display *names*/companies are anonymized (`server.py:336-417`); the underlying analysis findings (`/api/concepts/{id}/findings`) are served in full. Public hosting is an accepted, deliberate choice here — flagged so it is a decision of record, not an oversight.
- **`1costingfe` version lag**: if PyPI trails the local API, pin to a git ref instead of PyPI; the requirement is "installs cleanly from a non-local source," not "must be PyPI."
- **`iter-*/` dirs** in `analyses/` (~14 MB) are not needed at runtime; they may be excluded from the deploy to trim build size but excluding them is optional.
- **First-request latency**: on always-warm Railway this is a non-issue; on a sleeping fallback (HF free) the first request after sleep re-imports JAX and is slow — acceptable for those fallbacks, noted not fixed.
- **`dist/` rendered at startup** into a writable dir (gitignored) — requires a writable container filesystem (standard).
- **No API keys needed at runtime** — the `claude -p` narrative step is offline-only; the server never calls it.

---

## Requirement Selection Notes

The normative requirements below cover only what must be true for a correct, reproducible, auto-deploying public deployment: the dependency split, the container prerequisites, the parity check, and the push-to-main behavior. Platform-specific mechanics (exact Railway config field values, whether to use a Dockerfile, how to exclude `iter-*/`) are left to design/implementation. The public-vs-private decision is settled (public) and therefore appears as a non-goal/edge case rather than an FR.

---

## Requirements

### Functional Requirements

> From the owner's request unless marked [INFERRED] or [FROM RESEARCH].

1. **FR-1 (SATISFIED ✓)**: The deployment MUST install `costingfe` from a non-local source whose API matches the compute path. **Verified 2026-06-14**: PyPI `1costingfe==0.1.0a2` has a byte-identical `CostModel.forward` signature to local `0.1.0` (incl. `cost_overrides`, `override_reference_mw`, `**overrides`), exposes `sensitivity()`, `ConfinementConcept`, `Fuel`, and `costingfe.validation.{CostingInput,default_availability}`, and produces an **identical LCOE** (161.68568 on concept 01) running the real compute path end-to-end. PyPI is the source of record; the git-ref fallback is unnecessary.
2. **FR-2**: `pyproject.toml` MUST provide a slim serving dependency set (e.g. a `serve` optional-dependency group) that installs the explorer without `agentic-mbse`, `sysml-codegen`, `docling`, or `torch`, and that depends on `1costingfe` rather than the local editable path. [FROM RESEARCH]
3. **FR-3**: The offline pipeline install (the default project dependencies used for extraction/analysis/codegen) MUST remain functional and unchanged in behavior. [INFERRED]
4. **FR-4**: The server MUST bind `0.0.0.0` and the platform-provided `$PORT` when run in the hosted environment, and MUST run as a single uvicorn worker. [FROM RESEARCH]
5. **FR-5**: The deployment MUST serve, against the committed data, the page routes (`/`, `/pipeline`, `/compare`, `/cost-landscape`, `/concept/{id}`) and the data + compute APIs, including working slider recompute for costingfe-backed concepts.
6. **FR-6**: A push to `main` MUST trigger a redeploy that picks up changes to committed source data (`data/*.json`, `exploration/concept_analysis/analyses/`) and to the `1costingfe` version pin, with no manual deploy step and (on the primary target) without a hand-authored GitHub Actions workflow or Dockerfile.
7. **FR-7**: The work item MUST result in a live, publicly reachable URL on Railway (primary target).
8. **FR-8**: The deployment MUST be reproducible/operable from a written runbook covering the manual owner steps (account/billing, repo connect, config vars, verification) and the `1costingfe` dependency-bump procedure.
9. **FR-9**: The requirements SHOULD be satisfiable on at least one documented fallback platform (Hugging Face Spaces free tier, and/or Render) without code changes beyond configuration. [FROM RESEARCH]
10. **FR-10**: `uv.lock` MUST stay committed so hosted builds are reproducible. [INFERRED]

### Non-Functional Requirements

- **Cost**: Recurring hosting cost SHOULD be $0–$5/mo.
- **Build footprint**: The serving install SHOULD stay near the ~400 MB slim target (well within container platform limits), not the 6.1 GB full tree.
- **Setup effort**: Initial setup SHOULD be achievable without writing platform-specific deploy code (native git integration) on the primary target.

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv sync --extra serve` (or the chosen slim mechanism) installs in a clean clone with no sibling repos present, pulling `costingfe` from `1costingfe`/git, and **without** torch/docling/agentic-mbse/sysml-codegen. (FR-2, FR-3)
- [ ] Parity check recorded: a documented command/result shows the hosted `costingfe` version satisfies the compute API. (FR-1)
- [ ] The server, started with the container command, binds `0.0.0.0:$PORT` and answers `GET /api/health`. (FR-4)
- [ ] On the live URL: matrix/pipeline/compare/cost-landscape/concept pages render, and a slider drag on a costingfe-backed concept returns a recomputed headline via `/api/compute`. (FR-5, FR-7)
- [ ] A commit to `main` that edits a `data/*.json` value is observable on the live URL after auto-redeploy, with no manual deploy action. (FR-6)
- [ ] A runbook exists in this work-item directory with the owner's manual steps and the `1costingfe` bump procedure. (FR-8)
- [ ] Fallback path (HF Spaces and/or Render) documented with config-only differences. (FR-9)

### Quality & Integration

- [ ] Existing explorer tests continue to pass (`exploration/concept_explorer/tests/`).
- [ ] The default (pipeline) install and existing offline commands still work (extraction, `agentic-mbse` CLI). (FR-3)
- [ ] `uv.lock` committed and honored by the hosted build. (FR-10)

---

## Next-Stage Handoff

**Settled in this spec:**
- Service is **public** (no auth).
- Scope ends at a **live deployed URL** on Railway, plus an operator runbook.
- Railway is **primary**; HF Spaces / Render are documented **fallbacks**.
- Serving deps exclude the pipeline toolchain and depend on `1costingfe` (or git ref).
- Single process / single worker.

**Design must figure out:**
- The exact slim-deps mechanism: `serve` optional-dependency group vs separate `requirements-serve.txt` vs a Dockerfile (and whether Railpack's native build suffices without a Dockerfile).
- ~~PyPI vs git-ref for `costingfe`~~ — **decided: PyPI** (FR-1 verified). Remaining: how the version is pinned/bumped (use exact `==0.1.0a2`; it's a pre-release).
- The container start command form (e.g. `uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT --workers 1`) and how `$PORT`/host get into the app (env-aware `main()` vs platform start command vs Procfile/railway.toml).
- Whether to exclude `iter-*/` from the deploy and how (`.railwayignore`/Docker context).
- Whether the dependency-bump trigger stays manual or is automated (Renovate/Dependabot/scheduled job) — research leans manual-pin for reproducibility.
- Exact Railway config artifacts (`railway.toml`/`nixpacks`/Railpack settings) vs pure-UI configuration.

**Watch-outs for design:**
- `costingfe` distribution-name nuance: local `name = "costingfe"`, PyPI `1costingfe`, import package `costingfe` — get the dependency string right so `import costingfe` resolves.
- **Pre-release pin**: the only PyPI release is `0.1.0a2` (an alpha). A bare `1costingfe` or `1costingfe>=0.1.0` may NOT resolve a pre-release once any stable version exists (pip/uv exclude pre-releases by default). Pin **exactly** `1costingfe==0.1.0a2` (or publish a stable release before deploy). This also means deploys track a moving target unless pinned — keep it exact + `uv.lock` committed.
- `model_setup.py` files add `scripts/` to `sys.path` at import; the deploy must include `exploration/concept_analysis/scripts/lib/` and `tables/archetype_fit.csv`, not just the explorer dir.
- Single-worker is load-bearing; don't let a platform default to multiple workers/replicas.
- Public exposure serves full findings — confirm that's still intended at design time.

---

## Related Artifacts

- **Research:** `.project/research/20260612-110915_concept-explorer-web-hosting.md`
- **Explorer reference:** `exploration/concept_explorer/README.md`
- **Design:** `.project/active/explorer-web-hosting/design.md` (to be created)
- **Sibling pkg:** PyPI `1costingfe` — https://pypi.org/project/1costingfe/

---

## Appendix (Optional — does not count toward the main-body budget)

### Parity Verification (2026-06-14) — FR-1 evidence

Ran in a throwaway venv with **only** PyPI `1costingfe` installed (`pip install 1costingfe` → `1costingfe==0.1.0a2`, deps `jax 0.10.1`, `jaxlib 0.10.1`, `pydantic`, `pyyaml`, `numpy`, `scipy`):

| Check | Result |
|---|---|
| `import costingfe`; top-level `ConfinementConcept`, `CostModel`, `Fuel` | OK |
| `CostModel.forward` signature vs local `0.1.0` | **Byte-identical** — all of `cost_overrides`, `override_reference_mw`, the 8 plant params, and `**overrides` (VAR_KEYWORD) present |
| `CostModel.sensitivity` | present |
| `costingfe.validation.{CostingInput, default_availability}` (used by `lib.model_setup_helpers`) | importable |
| Load real `analyses/01.../model_setup.py` + run server's `_compute_cached` path (`forward()` with re-applied analyst overrides) | OK → LCOE **161.68568** |
| `model.sensitivity(base)` | OK → 190 finite entries |
| Same compute against **local** costingfe | LCOE **161.68568** — **exact match** |

Conclusion: PyPI `1costingfe==0.1.0a2` is a true drop-in for the explorer's runtime. Pin exactly (it's a pre-release — see watch-outs).

### A. Draft operator runbook (Railway primary)

These are the manual steps the owner performs; the exact field values are confirmed at implementation/design time. Captured here so FR-8 has a concrete starting point.

1. **Verify `1costingfe` parity (FR-1)** — ✅ **done 2026-06-14** (see Parity Verification above; PyPI `0.1.0a2` is an exact drop-in). No action needed unless the pin changes.
2. **Land the code/config changes** on a branch and merge to `main` (slim `serve` deps, env-aware host/port, any `railway.toml`).
3. **Create Railway account / project** (Hobby plan, $5/mo). Connect GitHub → select `1cFE/fusion-tea` → branch `main`.
4. **Configure build/start** — install `uv sync --extra serve`; start `uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port $PORT --workers 1` (or via `railway.toml`/Procfile). Railpack should auto-detect `uv`/`pyproject.toml`.
5. **Deploy & verify** — open the generated URL; check `/api/health`, a concept profile, and a slider recompute.
6. **Confirm auto-deploy** — push a trivial `data/*.json` change to `main`; confirm the site updates without manual action.

### B. `1costingfe` dependency-bump procedure (FR-8)

- Reproducible default: bump the pin in `pyproject.toml` (e.g. `1costingfe==X.Y.Z`), run `uv lock`, commit both, push to `main` → Railway redeploys with the new version.
- Optional automation: Renovate/Dependabot to open the bump PR, or a scheduled GH Action that bumps when a new `1costingfe` appears on PyPI. Research recommends keeping pins explicit for a quantitative tool rather than floating `>=`.

### C. Fallback platform notes (FR-9)

- **Hugging Face Spaces** (free, CPU Basic 2 vCPU/16 GB): native git-push deploy; **sleeps after 48 h idle** (slow first request, can't customize sleep on cpu-basic). Best zero-cost option. Likely needs a Docker SDK Space (Dockerfile) or `requirements.txt` shim.
- **Render** (Starter $7/mo): native git deploy, always-warm on paid; free tier spins down ~30–60 s and 512 MB base RAM is tight for JAX. Use a custom build command (`pip install uv && uv sync --extra serve`) or Docker — `uv` not auto-detected.
- **Ruled out — Vercel**: ephemeral functions (no in-memory state), ~500 MB Python bundle cap exceeded by jaxlib alone, JAX cold-start on every wake. Documented as a non-option.

**Next Steps:** After approval, proceed to `/_my_design`.
