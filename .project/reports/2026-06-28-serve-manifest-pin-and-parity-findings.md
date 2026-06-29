# Serving-manifest pin to `1costingfe==0.1.0` + what the strict parity check found

**Date**: 2026-06-28
**Author**: Claude (working session with Reid)
**Branch**: `feat/explorer-web-hosting`
**Scope**: Step 1 of "what's next" on the explorer web-hosting track — reconcile the slim serving manifest with the v0.1.0 migration, and prove the *deployed* engine matches the *shipped* data before any Railway spend.
**Related**: `reports/2026-06-28_1costingfe-v0.1.0-migration.md` (the Option-A migration), `.project/active/explorer-web-hosting/plan.md` (Phase 1 manifest), `.project/research/20260628-132851_costingfe-release-migration.md`.

---

## TL;DR

- **The serving manifest was stale.** `requirements-serve.txt` pinned `1costingfe==0.1.0a2` (compiled 2026-06-15, pre-recalibration), but the v0.1.0 migration regenerated all `data/*.json` against `1costingfe` **v0.1.0 final** (local `0254385`). A container built off the old pin would have computed different numbers than the data it serves. **Fixed**: bumped to `1costingfe==0.1.0`, recompiled `requirements-serve.txt`.
- **The bump is verified safe.** PyPI `1costingfe==0.1.0` is byte-identical to the local `0254385` checkout for the physics modules, ships the 0D solver modules Option A re-enables at runtime, and computes **bit-identically** to the local editable engine for all 33 served concepts. The version-skew risk is closed.
- **The strict parity check found a *separate*, pre-existing coherence bug.** For 3 non-tokamak concepts with analyst overrides — **11 (mirror, +48%)**, **18 (p-B11 FRC, +2.2%)**, **37 (MTIF, +0.85%)** — the explorer's server recompute path disagrees with the stored headline. This is **not** caused by the wheel, the bump, or jax cross-contamination. It is an **FR-SO1 coherence violation** that ships on the current branch and was missed by the migration's audit.

---

## 1. What step 1 changed

- `requirements-serve.in`: `1costingfe==0.1.0a2` → `1costingfe==0.1.0`, plus a comment documenting that v0.1.0 gates the 0D solvers but the wheel still ships them (so the runtime re-enable in `model_setup_helpers.py` works — re-verify on any future bump).
- `requirements-serve.txt`: recompiled via `uv pip compile requirements-serve.in -o requirements-serve.txt --prerelease=explicit`. Transitive deps unchanged and stable (numpy 2.4.6, scipy 1.17.1, pydantic 2.13.x).

Clean-venv proof (the Phase-1 gate, re-run): a venv containing only `requirements-serve.txt` installs `1costingfe 0.1.0` + jax/jaxlib and **no** torch/docling/agentic-mbse/sysml-codegen. `smoke_explorer.py` passes (33/33 serve + compute).

## 2. How the bump was verified (and why we can trust the PyPI wheel)

The research doc's standing open question was "PyPI `1costingfe` parity." Three checks, all green:

1. **PyPI publishes `0.1.0`** (alongside `0.1.0a1`/`0.1.0a2`).
2. **The `0.1.0` wheel ships the 0D solver modules** — `costingfe/layers/{tokamak,mirror,physics}.py` are in the wheel, and `model.py` carries `MODELS_0D_ENABLED`/`SIZING_FEATURES_ENABLED` as plain module globals. This is the load-bearing fact for **Option A**: fusion-tea flips those flags on at import (`model_setup_helpers.py`), and the modules must be present in the installed wheel for the flip to reach real code. They are.
3. **Wheel == local checkout, byte-for-byte** for `tokamak.py`, `mirror.py`, `physics.py`, `model.py` (sha256 match). The 18 default-parameter YAMLs ship under `costingfe/data/defaults/`. So PyPI `0.1.0` *is* the engine the data was regenerated against.

**Engine parity, measured**: the slim-venv (PyPI wheel) server and the editable-venv (local `0254385`) server produce identical `/api/compute` results for every concept tested, including the 3 outliers below. The wheel is not a source of divergence.

## 3. The strict parity check, and what it caught

The existing `smoke_explorer.py` only asserts `lcoe > 0`. I wrote a stricter gate (`/tmp/parity_check.py`, not yet committed): for every served cost-model concept, POST a no-op recompute (`overrides={}, apply_analyst_overrides=True` — the FR-SO1 invariant) and compare to the stored `cost_model.headline.lcoe_per_mwh`.

Result: **30/33 bit-identical (0.0000%)**, **3 fail**:

| concept | family | stored headline | server recompute | gap |
|---|---|---|---|---|
| 11 | magnetic mirror | 278.84 | 413.47 | **+48.3%** |
| 18 | p-B11 FRC | 369.54 | 377.85 | +2.2% |
| 37 | MTIF (NearStar D-D) | 240.83 | 242.87 | +0.85% |

## 4. Root-cause of the 3 outliers — what it is and isn't

Ruled out, with evidence:

- **Not the PyPI wheel / the bump.** The local editable project venv's server gives the *same* 413.47 / 377.85 / 242.87. The bump didn't introduce it.
- **Not stale data.** The concept's own module value `result_1gw` (what the regen wrote to the JSON) is 278.8 / 369.5 / 240.8 — it matches the stored data. The JSON is internally consistent with the module's projection.
- **Not jax cross-contamination.** Concept 11 computed *first, alone, in a fresh process* still returns 413.47. The migration's batch-mode contamination (the reason it regenerated in isolated subprocesses) is a different failure mode and is not what this is.

What it **is**: a divergence between two compute entry points, using the *same* library, for these 3 non-tokamak concepts that carry analyst overrides:

- **Module projection path** — `run_native_and_1gw()` in `exploration/concept_analysis/scripts/lib/model_setup_helpers.py`, which produces the module-level `result_1gw` that the regen serializes into `data/*.json`. → 278.8 / 369.5 / 240.8.
- **Server recompute path** — `_forward_with_overrides` / `_compute_cached` in `exploration/concept_explorer/server.py` (~192 / ~993), which `/api/compute` runs on every slider interaction. → 413.5 / 377.9 / 242.9.

For the 5 tokamaks (0D bisection projection) and the other 30 concepts, the two paths agree to ~1e-5. They diverge only for these non-tokamak override concepts — strongly suggesting the server's no-op recompute applies the analyst overrides at a different projection scale (native vs 1 GWe) than `run_native_and_1gw` does. Concept 11's 48% gap is the headline; 18 and 37 are smaller but the same class.

**User-visible symptom**: on concepts 11/18/37 the page loads the stored headline (e.g. 278.8) but the first slider touch — a no-op recompute — jumps it to 413.5. This is exactly the FR-SO1 incoherence Phase 1 of EXPLORER-UX-V3 was built to eliminate, surviving on these 3 concepts.

## 5. Why the migration audit missed it

`reports/2026-06-28_1costingfe-v0.1.0-migration.md` reports "33/33 served costingfe concepts ≤0.5%". That audit compared **stored headline vs `result_1gw`** (module-level) — both are 278.8 for concept 11, so it passes. It never compared stored vs the **server recompute path**. The lesson: the FR-SO1 invariant must be checked against `/api/compute` (what users actually trigger), not against `result_1gw`. A `result_1gw`-only audit is blind to server-path divergence.

## 6. Recommendations / follow-ups

1. **Promote a parity gate.** `smoke_explorer.py`'s `lcoe > 0` is too weak. A committed `scripts/`-level parity check (server `/api/compute` no-op vs stored headline, FR-SO1 tolerance) would have caught both the version skew and this coherence bug, and should run pre-deploy. (Draft at `/tmp/parity_check.py`.)
2. **Open a coherence item for 11/18/37.** Root-cause the server-recompute-vs-projection divergence for non-tokamak override concepts. Belongs with the migration's open coherence judgment calls (EXPLORER-UX-V3 / FR-SO1), not the hosting track. These ship incoherent today; concept 11 badly.
3. **Hosting track is unblocked.** Manifest pinned and engine-verified. Remaining hosting work is the owner-only Railway steps + agent-runnable Phase-3 regression (`uv sync`, explorer pytest).

## Appendix — evidence / repro

```bash
# PyPI versions + wheel contents
curl -s https://pypi.org/pypi/1costingfe/json   # → 0.1.0, 0.1.0a1, 0.1.0a2
# wheel ships layers/{tokamak,mirror,physics}.py + model.py with the gate flags;
# sha256(wheel model.py) == sha256(local ../1costingfe/src/costingfe/model.py)  (and the 3 layer files)

# parity: slim-venv (PyPI 0.1.0) server, no-op /api/compute vs data/*.json
#   30/33 == 0.0000% ; FAIL: 11 (278.84→413.47), 18 (369.54→377.85), 37 (240.83→242.87)

# not the wheel — editable project venv server gives the SAME outliers:
#   11→413.465  18→377.85  37→242.8745

# not contamination — concept 11 first/alone in a fresh slim-venv server → 413.465

# module path (what regen wrote): result_1gw lcoe  →  11=278.8  18=369.5  37=240.8
```

**Key files**
- Manifest: `requirements-serve.in`, `requirements-serve.txt`.
- Server recompute path: `exploration/concept_explorer/server.py` (`_forward_with_overrides` ~192, `_compute_cached` ~993).
- Module projection path: `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` (`run_native_and_1gw`, the override scaling).
- Migration: `reports/2026-06-28_1costingfe-v0.1.0-migration.md`.
