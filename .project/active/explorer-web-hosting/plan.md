# Implementation Plan: Concept Explorer Web Hosting

**Status:** In Progress (Phase 1 complete)
**Created:** 2026-06-14
**Last Updated:** 2026-06-15

## Source Documents
- **Spec:** `.project/active/explorer-web-hosting/spec.md`
- **Design:** `.project/active/explorer-web-hosting/design.md` ← component details, decisions, invariants, gotchas live here

## Implementation Strategy

**Phasing Rationale:** De-risk the only real uncertainty first — *is the slim dependency set complete enough to serve every feature?* — using a throwaway venv (no Docker, no cloud). Once that's proven, packaging into a Dockerfile and validating it locally is mechanical, and only then do we touch Railway (which costs money and involves manual owner steps). Each phase's output is the input the next phase assumes.

**Critical Path:** slim `requirements-serve.txt` proven in a clean venv → same set baked into a Dockerfile, built & run locally → deployed on Railway with push-to-main auto-redeploy.

**First Proof Point (Phase 1):** `server.py` runs against a venv containing *only* `requirements-serve.txt`, and `/api/compute` returns a recomputed LCOE — with `torch`/`docling`/`agentic-mbse`/`sysml-codegen` absent. If that works, the design's core bet (B2/B3, design.md#key-bets) holds.

**Validation Approach:** This is a config-only feature (design.md#core-concept — zero app code change). "Tests" are therefore **smoke gates**: a small reusable endpoint-smoke script run against (1) the slim venv, (2) the local container, (3) the live URL. No new pytest unit tests; the existing explorer suite is the regression guard.

**Required invariants to hold throughout:** design.md#required-invariants (single worker; runtime tree present & rooted; `import costingfe` → PyPI build; writable FS; app code byte-identical).

---

## Phase 1: Slim manifest + clean-venv proof

### Goal
Produce the pinned serving manifest and prove, in a venv containing only that manifest, that the full explorer (incl. compute + findings) serves correctly. No Docker, no cloud.

### Assumption Under Test
The 8-package slim set (design.md#component-overview, appendix B) is *sufficient and complete* — nothing the running server imports is missing, and the runtime tree on disk satisfies the compute/findings paths (B2).

### Test Stencil (Write This First)
Create a reusable smoke script `scripts/smoke_explorer.py` that takes a base URL and asserts the feature surface:
```python
# scripts/smoke_explorer.py  (usage: uv run python scripts/smoke_explorer.py http://127.0.0.1:8421)
import sys, httpx
base = sys.argv[1].rstrip("/")
assert httpx.get(f"{base}/api/health").json()["status"] == "ok"
m = httpx.get(f"{base}/api/manifest").json(); cid = m["concepts"][0]["concept_id"]
assert httpx.get(f"{base}/concept/{cid}").status_code == 200          # page shell
assert "analysis_html" in httpx.get(f"{base}/api/concepts/{cid}/findings").json()
r = httpx.post(f"{base}/api/compute", json={"concept_id": cid, "overrides": {}}).json()
assert r["headline"]["lcoe_per_mwh"] > 0                              # JAX recompute works
print("SMOKE OK", cid, r["headline"]["lcoe_per_mwh"])
```
(Pick a costingfe-backed concept for the compute assertion; if `m["concepts"][0]` is standalone, choose one with `has_cost_model`.)

### Changes Required
**See design.md#component-overview and appendix B for the manifest contents.**

- [x] Create `requirements-serve.in` — `1costingfe==0.1.0a2` + the 7 serving libs (design.md appendix B).
- [x] Compile: `uv pip compile requirements-serve.in -o requirements-serve.txt --prerelease=explicit` (fully pinned; commit both). **Deviation:** used `--prerelease=explicit`, not `--prerelease=allow` — see Phase 1 Completion.
- [x] Create `scripts/smoke_explorer.py` (stencil above, adapted — stdlib-only, compute-concept iteration; see notes).
- [x] Build a throwaway venv with ONLY the manifest and run the server against it (validation below).

### Validation
**Automated / manual:**
- [x] `uv venv /tmp/serve-venv && uv pip install --python /tmp/serve-venv/bin/python -r requirements-serve.txt` (29 packages).
- [x] `uv pip list --python /tmp/serve-venv/bin/python` shows **no** `torch`, `docling`, `agentic-mbse`, `sysml-codegen`. (NB: `pip` isn't present in a uv venv, so `pip list` is empty — used `uv pip list`, which is authoritative.)
- [x] Start server with that interpreter from repo root: `/tmp/serve-venv/bin/python -m uvicorn exploration.concept_explorer.server:app --host 127.0.0.1 --port 8421` (single worker). Healthy in ~1s.
- [x] `python scripts/smoke_explorer.py http://127.0.0.1:8421` → `SMOKE OK  page/findings=33  compute=33  lcoe_per_mwh=162.28`. Concept 01 recompute = **161.68568420410156**, exact match to spec parity (161.68568).
- [x] Installed size of `/tmp/serve-venv` = **600 MB** (over the ~400–500 MB design target; jaxlib + scipy + numpy dominate — flagged for the Phase 2 image-size expectation).

**What We Know Works After This Phase:** the exact package set destined for the image serves every endpoint, including JAX recompute and findings, with the heavy/local deps absent. The biggest risk is retired.

---

## Phase 2: Container artifacts + local Docker build/run

### Goal
Package the proven set into a `Dockerfile` + `.dockerignore` + `railway.toml`, install Docker locally, and build/run the actual image — smoke-passing — before any cloud spend.

### Assumption Under Test
The container mechanics work: `.dockerignore` excludes the 7 GB of gitignored bulk while keeping the runtime tree; the shell-form `CMD` expands `$PORT`; the image is ~400–500 MB.

### Test Stencil (Write This First)
Reuse `scripts/smoke_explorer.py` from Phase 1 against the running container:
```bash
docker build -t explorer .
docker run --rm -e PORT=8421 -p 8421:8421 explorer &     # shell-form CMD must expand $PORT
sleep 8 && uv run python scripts/smoke_explorer.py http://127.0.0.1:8421
```

### Changes Required
**See design.md#implementation-notes and appendices A/C for the exact sketches.**

- [x] `Dockerfile` — `python:3.12-slim`, copy `requirements-serve.txt`, `pip install --no-cache-dir`, copy repo, shell-form `CMD` with `${PORT:-8421}` (design.md appendix A). Added `PYTHONUNBUFFERED=1`/`PYTHONDONTWRITEBYTECODE=1` for log streaming.
- [x] `.dockerignore` — excludes `.git`, `.venv`, `**/iter-*/`, `*.log`, `__pycache__`, `.pytest_cache`, `archive/*` **except** `archive/concept_analysis_pre_rework`. **Deviation:** excludes ALL of `knowledge/` (not just `knowledge/concept_research`) — no serving-runtime code references `knowledge/` (grep-verified), saving an extra ~151 MB; the Phase 2 docker smoke is the safety net. Keep-paths verified present: `analyses/*/{model_setup.py,analysis.md}`, `scripts/lib/`, `tables/archetype_fit.csv`, `concept_analysis_pre_rework/*/analysis.md` (30 concepts).
- [x] `railway.toml` — dockerfile builder + start command (single worker) + `restartPolicyType="on_failure"` (design.md appendix C).

### Validation
**Docker setup (owner runs; needs sudo — run via `! <cmd>` in-session):**
- [ ] `! sudo apt-get update && sudo apt-get install -y docker.io`
- [ ] `! sudo systemctl enable --now docker`
- [ ] `! sudo usermod -aG docker $USER` then **log out/in** (or `! newgrp docker`) so `docker` runs without sudo
- [ ] `docker run --rm hello-world` → succeeds

**Image build/run:** *(run via `sg docker -c '…'` — the Bash shells predate the `docker` group add, so the socket is otherwise permission-denied; the interactive `! docker` worked because that shell had the group)*
- [x] `docker build -t explorer .` → succeeds. **Image = 1.16 GB** (over the ~400–500 MB SHOULD-target — see note below).
- [x] Build context transferred = **78.3 MB** (not huge; `.dockerignore` working).
- [x] `docker run -e PORT=8421 -p 8421:8421 explorer` → healthy in 1s → smoke → `SMOKE OK  page/findings=33  compute=33  lcoe=162.28`. `$PORT` expands, tree complete.
- [x] `docker exec … pip list` shows **no** torch/docling/agentic-mbse/sysml-codegen, and **no nvidia/cuda** wheels (CPU jaxlib).

**Image-size note (deviation from NFR ~400 MB target):** 1.16 GB is essentially the floor for a CPU-JAX serving image. The 684 MB pip layer is jaxlib (347 MB) + scipy (111 MB) + numpy (42 MB) + `.libs`/ml_dtypes — all required by `/api/compute`; none droppable. python:3.12-slim base (~130 MB) + 78 MB context complete it. The actual goal — excluding the multi-GB *pipeline* toolchain (torch/docling) — is met. Acceptable for Railway (no blocking size limit); flagged because it misses the NFR SHOULD.

**What We Know Works After This Phase:** the real artifact that Railway will build runs locally and passes the full smoke — `$PORT`, tree completeness, and size all confirmed.

---

## Phase 3: Railway deploy + CI/CD proof + regression wrap

### Goal
Get a live public URL on Railway via the runbook, prove push-to-main auto-redeploy, and confirm nothing regressed in the dev/pipeline workflow.

### Assumption Under Test
Railway builds the Dockerfile on connect, injects `$PORT`, exposes a public URL, and redeploys on every push to `main` with no GitHub Actions (FR-6/FR-7); and the deploy work left `pyproject.toml`/pipeline untouched (FR-3).

### Test Stencil (Write This First)
The smoke script again, now against the live URL, plus a CI/CD proof:
```bash
uv run python scripts/smoke_explorer.py https://<service>.up.railway.app
# CI/CD proof: edit one value in exploration/concept_explorer/data/<id>.json, commit, push main
#   → watch Railway redeploy → re-run smoke → confirm the changed value is live
```

### Changes Required
- [ ] `RUNBOOK.md` (in this work-item dir) — operator steps (Docker setup recap, Railway account/billing/connect, enable public networking, set branch=`main`) + the `1costingfe` bump procedure (spec appendix A/B; design.md#component-overview). FR-8.
- [ ] Owner executes RUNBOOK to create the Railway service (Hobby plan; connect `1cFE/fusion-tea`; branch `main`; generate public domain).

### Validation
**Live deploy:**
- [ ] Live URL resolves; `scripts/smoke_explorer.py <url>` → `SMOKE OK` (FR-5, FR-7).
- [ ] A slider drag on a costingfe concept in the browser updates the headline (manual, design.md#validation-approach).

**CI/CD (FR-6):**
- [ ] Push a trivial `data/*.json` change to `main` → Railway auto-redeploys with no manual action → change visible on live URL.

**Regression (FR-3):**
- [ ] `uv sync` (default/pipeline install) still resolves and works.
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` → passes.

**What We Know Works After This Phase:** a public, always-on URL that redeploys on push, with the offline pipeline workflow intact. Spec acceptance criteria met.

---

## Environment Setup

**See CLAUDE.md** — always `uv run ...` for Python. Docker install steps are in Phase 2 validation. The throwaway/serve venvs in Phases 1–2 are intentionally outside the project `.venv`.

## Risk Management

**See design.md#potential-risks.** Phase-specific:
- **Phase 1:** if a dep is missing, the smoke script fails loudly *before* any container/cloud work — add the dep to `requirements-serve.in`, recompile, rerun.
- **Phase 2:** if build context is huge or a runtime file 500s in-container, the `.dockerignore` keep/drop list is wrong — fix and rebuild (cheap, local).
- **Phase 3:** Railway billing/account is owner-only; the runbook makes it repeatable. If auto-redeploy doesn't fire, check the service's trigger branch (design research: Railway Service Settings → branch).

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-06-15

**Actual Changes:**
- `requirements-serve.in` — `1costingfe==0.1.0a2` + 7 serving libs (per design appendix B).
- `requirements-serve.txt` — fully pinned (29 packages) via `uv pip compile … --prerelease=explicit`.
- `scripts/smoke_explorer.py` — reusable endpoint smoke gate (health, manifest, page shell, findings, `/api/compute` recompute).

**What was proven:** in a throwaway venv containing ONLY `requirements-serve.txt` (no torch/docling/agentic-mbse/sysml-codegen), the explorer serves every endpoint — including JAX/costingfe recompute. Concept 01 recompute = 161.68568420410156, exact match to the spec's parity value. The design's core bet (B2/B3 — slim set sufficient, PyPI `1costingfe` numerically identical) holds. The biggest risk is retired.

**Issues (both PRE-EXISTING bugs on `main`, surfaced by the clean-venv proof — neither caused by the dependency split; fixed via separate PRs):**
1. **Non-UTF-8 bytes in `concept_registry.json`** — two raw Latin-1 `0xd7` (`×`) bytes broke `read_text()` at lifespan startup, so the server wouldn't boot in any UTF-8 environment (incl. the target container). Fixed: PR #81 (`02124c13`, re-encode to UTF-8).
2. **Machine-absolute Windows `model_setup` paths in 38 committed data files** — `C:\Users\mallo\…\model_setup.py` baked in by the extractor; `server.py` loaded them verbatim, so `/api/compute` returned 500 (`FileNotFoundError`) on every non-Windows host. Fixed: `efa8e885` (derive `model_setup` path from `concept_id`, drop stored machine paths). **Currently on branch `fix/explorer-derive-model-setup-path` — needs merge to `main` before/with the hosting deploy, else the deployed container's compute path 500s.**

**Deviations from plan:**
- **Compile flag:** `--prerelease=explicit`, not the design's `--prerelease=allow`. `allow` was globally permitting pre-releases and had pulled in `pydantic==2.14.0a1` (alpha), `numpy==2.5.0rc1`, `scipy==1.18.0rc2` — a stability/reproducibility hazard for a quantitative tool. `explicit` confines the pre-release allowance to the one explicitly-pinned package (`1costingfe`), so the rest resolve stable (`pydantic 2.13.4`, `numpy 2.4.6`, `scipy 1.17.1`). The `.in` header documents the corrected command.
- **Smoke script:** stdlib `urllib` instead of `httpx` (zero deps → runs from any interpreter, incl. the slim venv). It iterates `has_cost_model` concepts and asserts the first that genuinely recomputes, because `/api/compute` is gated on `concept.sources.model_setup` (server.py:1042), which is stricter than `has_cost_model`.
- **Venv size:** 600 MB vs the ~400–500 MB design target — not a blocker, but the Phase 2 image-size expectation should be revised upward (jaxlib/scipy/numpy floor).

**Not yet done (intentionally — owner-gated, deferred to later phases):** committing the Phase 1 artifacts. Holding the commit until you confirm, since the `model_setup` fix lives on a separate branch and we'll want the hosting commits to land on `main` in a coherent order.

### Phase 2 Completion
**Completed:** 2026-06-15. Build + run + container smoke all PASS.

**Actual Changes:**
- `Dockerfile`, `.dockerignore`, `railway.toml` at repo root (not yet committed).

**What was proven:** the real artifact Railway will build runs locally and passes the full smoke (`/api/compute` recompute works in-container, `$PORT` expands, runtime tree complete), with no heavy deps and no CUDA wheels. Build context 78.3 MB.

**Issues:**
- Docker socket permission-denied from the agent's Bash shells (they predate the `docker` group membership add). Worked around with `sg docker -c '…'`; a fresh login shell would also fix it.
- Image is **1.16 GB**, ~2.5× the NFR ~400 MB SHOULD-target. Root cause is the irreducible CPU-JAX floor (jaxlib 347 MB + scipy 111 MB + numpy 42 MB), not misconfig. Not a blocker for Railway. (See Validation note.)

**Deviations:**
- `.dockerignore` excludes ALL of `knowledge/` (design said `knowledge/concept_research`) — zero runtime references; smoke-verified.
- Image size misses the NFR target (above) — accepted as the CPU-jax floor.

### Phase 3 Completion

---

**Status**: Draft → In Progress → Complete
