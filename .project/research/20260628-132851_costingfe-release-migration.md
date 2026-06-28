# Research: What it would take to bring fusion-tea onto current `1costingfe`

**Date**: 2026-06-28
**Author**: Claude (investigation session)
**Trigger**: Phase-1 explorer re-verification stalled when `1costingfe` local checkout was pulled fresh and the explorer's concept modules stopped importing.
**costingfe state examined**: `origin/master` @ `0254385` (tag `v0.1.0`), vs the pre-pull local `b9b0a4c`.
**fusion-tea state**: branch `feat/explorer-web-hosting` (explorer tree byte-identical to `main`).

---

## Bottom line

The current `1costingfe` master is a **v0.1.0 release build** that deliberately narrowed the library's scope to *"cost a user-supplied physics operating point."* In doing so it **gated off the two capabilities the fusion-tea concept pipeline is built on**: the bundled 0D physics inverse (`use_0d_model`) and power→geometry sizing/optimization (`size_from_power`, `optimize_lcoe`). It also recalibrated the cost constants, reworked plant-power (`n_mod`) scaling, and renamed the distribution package.

fusion-tea `main` was built and last regenerated (06-24) against a **pre-release** costingfe (`b9b0a4c`, 06-15). It has **never run against the release build**. Bringing it onto current `1costingfe` is **not a verification task — it is a migration project** with a real fork-vs-rewrite decision at its center.

Concretely, against `0254385` today:

| Surface | Status on release build |
|---|---|
| `uv run` (whole repo) | **Broken** — package renamed `costingfe`→`1costingfe`; fusion-tea's `pyproject`/`uv.lock` still say `costingfe` |
| 5 tokamak concepts (01, 21, 28, 29, 33) | **Hard fail** at import — `use_0d_model` gated → `NotImplementedError` |
| ~35 other concepts | Import OK, **but numbers moved** (recalibration + n_mod rework); all stored `data/*.json` headlines stale |
| Concept 24 (DPF) example | 19.09 → **234.78** $/MWh (structural, from the new n_mod sizing for module-replication concepts) |

A separate finding fell out of this: **concept 01's `data/01.json` was already stale on `main`** before any of this — even the pre-pull local costingfe (`b9b0a4c`) rejects concept 01's `dhe3_dd_frac_pin`, so the 06-24 regen could not have rebuilt it. FR-SO1 for concept 01 was broken independent of the release stripping.

---

## 1. What "stripped" means — precisely

"Stripped" is shorthand; the release did four distinct things. Only the first is "removal," and even that is **gating, not deletion**.

### 1a. Feature gating (the blocker) — *gated behind constants, code still on disk*

`src/costingfe/model.py` now carries two module-level flags (lines ~92/99):

```python
SIZING_FEATURES_ENABLED = False   # size_from_power, optimize_lcoe
MODELS_0D_ENABLED        = False   # use_0d_model (0D tokamak + mirror inverse)
```

`forward()` checks them (model.py ~960–981) and raises:

- `optimize_lcoe`/`size_from_power` → *"…optimization (optimize_lcoe) are not available in this release."*
- `use_0d_model` → *"The bundled 0D physics models (use_0d_model) are not available in this release; supply the physics operating point as inputs."*

The comments are explicit: *"The solver modules (layers/tokamak.py, layers/mirror.py, the model._size_* helpers) remain on disk but are unreachable through forward(). **Flip to True to re-enable.**"* So the physics code is present; it is fenced off behind a boolean to keep the released build to "cost a user-supplied operating point."

**This is the single thing that makes tokamak concepts un-runnable.** fusion-tea's tokamak path *requires* `use_0d_model=True` (see §2).

### 1b. Cost recalibration — *every number moves*

Independent of gating, the release re-baselined the costing:

- `47aa7a4` (06-23) — *"Standardize cost constants to 2025 USD, promote conductor costs to CostingConstants"* (`costing_constants.yaml` +41/−, `defaults.py` +89/−, `types.py` −13).
- `a168537` (06-25) — *"Release prep: plant-total power scaling (n_mod), net/gross reference-power unification, account recalibrations"* (`costs.py` +82, `cas22.py`, `model.py`, `validation.py`).
- `a09e76f` (06-17) — split `overnight_cost` into overnight M$ and `capital_per_kw` ($/kW).
- `17f9ab3` (06-16) — `n_mod`-from-power sizing for module-replication concepts (orbitron, DPF, Zap, FRC) — this is what swung concept 24 (DPF) from ~19 to ~235.

Consequence: **even the concepts that still import produce different LCOE than the stored JSON.** A full data regen is mandatory regardless of the tokamak question.

### 1c. Package rename — *breaks `uv run` repo-wide*

- `50ffebf` (06-25) — *"set distribution name to 1costingfe (import package stays costingfe)."*
- `865d470` (06-26) — regenerate `uv.lock` for the rename.

fusion-tea's `pyproject.toml` declares the dependency as `costingfe` (line 9) sourced editable from `../1costingfe` (line 34); `uv.lock` pins name `costingfe`. The distribution is now `1costingfe`, so `uv` fails metadata resolution: *"Package metadata name `1costingfe` does not match given name `costingfe`."* Until fusion-tea's manifest is updated, **no `uv run` command in the repo works** with the fresh checkout. (Direct `.venv/bin/python` still imports, because the import package is still `costingfe` and the editable `src/` is on the path — that's how the evidence below was gathered.)

### 1d. Mirror physics overhaul + paper/blog churn — *behavioural drift on non-tokamak MFE*

The June window also rewrote mirror physics substantially (`layers/mirror.py` +813; energy-balance closure, tandem plug confinement, fluence-based core lifetime, collisionality gating) and reworked the paper/blog. This isn't a blocker but means mirror/MFE concept numbers (06, 11, etc.) drifted on their own merits, not just from constant recalibration.

---

## 2. Why this hits fusion-tea so hard — the dependency surface

fusion-tea's costing all funnels through `exploration/concept_analysis/scripts/lib/model_setup_helpers.py`. The release gated off exactly the primitives this file is built on:

- **`use_0d_model=True` for tokamak.** `_use_0d_path()` returns True for every `ConfinementConcept.TOKAMAK` spec that hasn't opted out with `enforce_plasma_limits=False`. Both `generic_reference()` and `run_native_and_1gw()` then set `use_0d_model=True`. → Gated off ⇒ `NotImplementedError`.
- **The R0/β_N bisection 1 GWe projection** (`_bisect_r0_at_native_beta`). The standardized cross-concept headline for tokamaks is produced by repeatedly calling the **0D inverse** at varying R0 and reading β_N off `model._plasma_state` (a *private* attribute) to match the native operating point. This entire projection method is unreachable without `use_0d_model`.
- **`model._plasma_state.beta_N`** — private state captured via `_run_costing_with_plasma_state()`. No 0D path ⇒ no plasma state ⇒ the bisection can't set its target.
- **Adapter API** (`costingfe.adapter`): `FusionTeaInput`, `run_costing`, `FusionTeaOutput.params` (added in costingfe PR #38), `override_reference_mw`, plus `costingfe.layers.physics.OperatingPointInfeasible` and the FD-based `model.sensitivity()`. These survived the release, but are the seams that would shift under any further upstream change.

**Breadth (measured on `0254385`):** the 5 tokamak concepts that route the 0D path fail — **01, 21, 28, 29, 33**. Concepts **34** and **39** are tokamaks/STs that route *around* it (`use_0d_model=False` in their `result_1gw.params`; 39 via `enforce_plasma_limits=False`), so they import. Every non-tokamak concept imports. So the "0D wall" is contained to those 5 — but they include the flagship concept 01 (ARC/CFS), the explorer's canonical demo.

---

## 3. Timeline — when the release changes landed on costingfe master

All on `origin/master`; local was 62 commits behind (sat at `b9b0a4c` 06-15 → `0254385` 06-28 per reflog).

| Date | Commit | What |
|---|---|---|
| 06-16 | `17f9ab3` | n_mod-from-power sizing for module-replication concepts (DPF/FRC/Zap/orbitron) |
| 06-17 | `a09e76f` | split `overnight_cost` → overnight M$ + `capital_per_kw` |
| **06-18** | **`b65bdfe`** | **Gate `size_from_power` + `optimize_lcoe` off for release** (solvers stay on disk) |
| 06-23 | `47aa7a4` | Standardize constants to **2025 USD**, promote conductor costs |
| **06-23** | **`4bf6784`** | **Release-gate `use_0d_model`** ← the tokamak blocker |
| 06-23 | `94f66e9` | Paper: remove gated-sizing + 0D-model sections (v0.1.0-alpha.3) |
| **06-25** | **`a168537`** | **Release prep: n_mod plant-total power scaling, net/gross power unification, account recalibrations** |
| **06-25** | **`50ffebf`** | **Rename distribution `costingfe`→`1costingfe`** |
| 06-26 | `865d470` | Regenerate `uv.lock` for the rename |
| 06-26 | `0254385` | HEAD (handoff smoke-test fix) |

So the "stripping" is a **2026-06-18 → 06-26 release-prep series**, tagged `v0.1.0`. fusion-tea's last explorer-data regen was **06-24** (`70090fc8`, "restore R0-bisection projection + regen"), against the 06-15 local checkout — i.e. **after** `use_0d_model` was gated upstream (06-23) but **before** that gating was ever pulled locally. fusion-tea main therefore encodes the *pre-release* contract end-to-end.

---

## 4. Migration options

Three coherent strategies. They are not equivalent in spirit — A keeps fusion-tea's analysis method, B adopts upstream's new contract, C declines the migration.

### Option A — Re-enable the gated physics (fork/patch costingfe)
Flip `MODELS_0D_ENABLED = True` (and `SIZING_FEATURES_ENABLED = True` if any concept uses sizing) in the local/forked costingfe. The solver modules are still on disk, so the 0D inverse becomes reachable again.

- **Pros:** Smallest fusion-tea code change. Preserves the R0/β_N bisection projection method as-authored. Could be running tokamaks again within an afternoon (plus the cross-cutting work in §5).
- **Cons:** You are running **code upstream explicitly declared unsupported for release** — against its stated intent. The 0D layers changed during the release window (mirror overhaul, tokamak validation commits); re-enabling doesn't guarantee the *same* β_N the 06-24 data assumed. You inherit a **maintained divergence** from upstream forever, or until upstream un-gates. The released *numbers* (recalibrated constants) still differ from any prior data, so a full regen is still required, and tokamak headlines won't match the public v0.1.0 explorer.
- **Effort:** Library patch ~trivial; validating that re-enabled 0D reproduces sane β_N/headlines for the 5 tokamaks ~0.5–1 day; + §5.

### Option B — Adopt the release contract (supply explicit operating points)
Rewrite the tokamak path to hand the library a **user-supplied physics operating point** instead of relying on the 0D inverse — the usage the release is built for. The 1 GWe projection would need a new derivation that doesn't depend on `use_0d_model`/β_N bisection.

- **Pros:** Aligned with upstream; no fork; fusion-tea tracks `1costingfe` releases cleanly going forward. Tokamak numbers would match the supported library.
- **Cons:** **Substantial.** It deletes the analytical core of the tokamak projection (`_bisect_r0_at_native_beta`, `_run_costing_with_plasma_state`, the `_use_0d_path` branch). You must define, per tokamak concept, what operating point to supply and how to project to 1 GWe without the inverse — a modeling decision, not a mechanical edit. Touches `model_setup_helpers.py`, all 5 tokamak `model_setup.py` files, and the extractor's two-knob verification. This is Phase-2-scale work with its own spec.
- **Effort:** ~3–6 days+ and a modeling design decision; + §5.

### Option C — Pin costingfe to the pre-release commit (decline the migration for now)
Keep fusion-tea on the costingfe contract it was built against. Pin the editable source to a pre-`4bf6784` commit (the 06-24 regen baseline, ≈ `b9b0a4c` era), or vendor that revision. This is **not** "use 1costingfe as it exists now" — it's the honest baseline for finishing Phase-1 verification and shipping the explorer as-is.

- **Pros:** Unblocks Phase-1 verification immediately; no analysis rewrite. Decouples the explorer ship from the upstream release decision.
- **Cons:** Frozen against an unsupported old library; diverges from the public v0.1.0 explorer; defers the inevitable. Note even the pinned baseline has the concept-01 `dhe3_dd_frac_pin` staleness to resolve (the 06-24 regen never rebuilt it).
- **Effort:** Pin + relock ~1–2h; then proceed with the original Phase-1 verification.

---

## 5. Cross-cutting work required under **any** option (A or B)

1. **Rename the dependency.** `pyproject.toml`: dependency `costingfe`→`1costingfe` and `[tool.uv.sources]` key; relock (`uv lock`). Import statements stay `import costingfe`. (~1h)
2. **Adapt to API/semantic changes** between `b9b0a4c` and `0254385`: `capital_per_kw` split, net/gross reference-power unification, `construction_time_yr` sourced from YAML, strict unknown-kwarg rejection on `forward()`, any adapter signature drift. Audit `model_setup_helpers.py` against the new `forward()`/adapter. (~0.5–1 day)
3. **Full data regen + integrity audit.** Re-run `extract_explorer_data.py` for all served concepts against the chosen library; re-add the headline-vs-`result_1gw` audit (epic Item 1-FU2) so stale headlines (like concept 01/24) can't ship silently. Use isolated per-concept extraction to dodge the jax cross-contamination noted in FU2. (~0.5–1 day, longer if 0D re-enable needs per-tokamak validation)
4. **Re-verify Phase 1** (the original task) against the regenerated data: FR-SO1 headline invariant for 01/17a/24, slider/tornado coherence, override panel. (~0.5 day)

---

## 6. Recommendation

For the **immediate goal** (finish Phase-1 verification, keep the explorer shippable): **Option C** — pin costingfe to the 06-24 regen baseline, verify Phase 1, and resolve the concept-01 staleness. This is reversible and unblocks now.

For the **strategic goal** (track the public `1costingfe` v0.1.0): **Option B**, scoped as its own Phase-2 work item with a modeling-design decision on the tokamak operating-point handoff. **Option A** is a legitimate bridge if tokamak coverage is needed *before* B lands, but treat it as a temporary fork with eyes open about running un-gated, recalibrated code whose numbers won't match either the old data or the public explorer.

What **not** to do: silently leave costingfe at `0254385` and patch fusion-tea piecemeal until things stop erroring — that path produces tokamak data from re-enabled-but-unvalidated 0D physics mixed with new recalibrated constants, matching neither baseline, with no audit trail.

---

## 7. Open questions for the user

1. Is `1costingfe` v0.1.0 the **intended long-term** engine for the explorer, or a parallel public/paper release while fusion-tea stays on the richer internal physics? (Determines B vs C.)
2. Does the public v0.1.0 explorer at `1cf.energy` (referenced in costingfe's blog commits) already cost tokamaks **without** the 0D inverse? If so, its method is the template for Option B.
3. Should I roll the local `1costingfe` back to `b9b0a4c` (where you found it), or leave it at `0254385`? I have not changed it again since the pull.

---

## Appendix — evidence & repro

```bash
# costingfe was 62 commits behind; pulled b9b0a4c → 0254385 (tag v0.1.0)
git -C ../1costingfe reflog --date=short        # b9b0a4c sat from 06-15 to 06-28

# release gates (model.py ~92/99):  SIZING_FEATURES_ENABLED=False ; MODELS_0D_ENABLED=False
grep -n "MODELS_0D_ENABLED\|SIZING_FEATURES_ENABLED" ../1costingfe/src/costingfe/model.py

# breadth: only tokamak-0D concepts fail on 0254385
.venv/bin/python  # import each analyses/*/model_setup.py:
#   FAIL (use_0d_model gated): 01, 21, 28, 29, 33
#   OK but renumbered:         24 DPF 19.09→234.78, etc.

# uv breakage from rename:
uv run python -c "import costingfe"
#   error: Package metadata name `1costingfe` does not match given name `costingfe`

# concept 01 already stale on the OLD local b9b0a4c (independent of release):
#   ValueError: forward() got unknown parameter(s) ... dhe3_dd_frac_pin
```

**Key files**
- Gating: `../1costingfe/src/costingfe/model.py` (`MODELS_0D_ENABLED`, lines ~89–99, ~960–998).
- fusion-tea dependency surface: `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` (`_use_0d_path`, `_bisect_r0_at_native_beta`, `run_native_and_1gw`).
- Server recompute path that loads modules live: `exploration/concept_explorer/server.py` (`_forward_with_overrides` ~192, `_compute_cached` ~993).
- fusion-tea manifest to rename: `pyproject.toml` lines 9, 34; `uv.lock`.
- Related prior note: epic `.project/backlog/epic_explorer_ux_v3.md` (Item 1-FU2 headline-audit; "Post-merge status").
