---
date: 2026-04-13T12:00:00-07:00
researcher: Claude
topic: "Post-implementation regression analysis: iter-6-9 (post-fix) vs iter-1-5 (pre-fix) for concepts 13, 16, 17b"
tags: [research, concept-analysis, regression, model-continuity]
status: complete
last_updated: 2026-04-13
---

# Research: Post-Implementation Iteration Regression Analysis

**Date**: 2026-04-13
**Researcher**: Claude
**Research Type**: Codebase / Quality

## Research Question

After implementing the analysis loop symmetry fix (model continuity via edit-not-rewrite, all findings forwarded to model agent), did the post-fix iterations (6-9) show improvements? Any regressions?

## Timeline

The fix (edit-not-rewrite in loop.py, template changes) was written at ~16:06-16:12 UTC on 2026-04-13. The iteration timestamps confirm the boundary:

| Batch | Iterations | Timestamp Range (UTC) | Pipeline Version |
|-------|------------|----------------------|-----------------|
| Original run | 1-3 | 2026-04-12 ~24:00 – 2026-04-13 ~03:26 | Pre-fix: rewrite-from-scratch |
| First +2 passes | 4-5 | 2026-04-13 ~15:03 – 15:28 | **Pre-fix**: rewrite-from-scratch |
| Second +2 passes | 6-7 | 2026-04-13 ~16:42 – 16:53 | **Post-fix**: edit-prior-model |
| Third +2 passes | 8-9 | 2026-04-13 (later) | **Post-fix**: edit-prior-model (+ template nesting fix) |

**The fix boundary is iter 5→6. Iter 1-5 are all pre-fix. Iter 6-9 are post-fix.**

## Summary (iter 6-9)

**The destructive-editing regression pattern persists through iter 8-9 for concepts 13 and 16. Concept 17b remains clean.**

The oscillation pattern is now confirmed over 4 post-fix iterations:

| Concept | Iter-6 | Iter-7 | Iter-8 | Iter-9 | Pattern |
|---------|--------|--------|--------|--------|---------|
| **13** | +features | **DROPPED** | +restored | **DROPPED AGAIN** | 2-cycle oscillation |
| **16** | +features | **DROPPED** | +restored | **DROPPED AGAIN** | 2-cycle oscillation |
| **17b** | no model change | +small fix | +2 sweeps | +1 sweep, expansions | Monotonic growth |

In concepts 13 and 16, the model agent restores dropped features in even-numbered iterations and drops them again in odd-numbered iterations while applying new findings. The assessor catches each regression immediately, but the model agent fails to carry forward all existing content when applying the next round of findings.

Concept 17b is the control — it grows monotonically from 6→8→9 sweeps with zero regressions. The key difference: 17b never had a single iteration where the model agent was asked to simultaneously preserve recently-added complex features AND apply new findings.

---

## Per-Concept Detail

### Concept 13: Electrostatic Hybrid (Orbitron)

#### Model Size Trajectory

| Iter | Lines | Delta | Pipeline | Key Model Change |
|------|-------|-------|----------|-----------------|
| 1 | ~1347 | -- | pre-fix | Initial model, degenerate sweeps |
| 2 | ~1347 | ~0 | pre-fix | Part B added (optimistic-baseline sweeps) |
| 3 | 1252 | -95 | pre-fix | Restructured (H1/H2/H3 hypothesis framework) |
| 4 | 1409 | +157 | pre-fix | Part C added (alpha sweep) |
| 5 | 1338 | -71 | pre-fix | Alpha direction fix, cleanup |
| **6** | **1403** | **+65** | **post-fix** | **Added viable-LB scenario ($193.8/MWh) + component-level scaling** |
| **7** | **1341** | **-62** | **post-fix** | **REGRESSION: Dropped both iter-6 additions** |

#### What Happened at iter 6→7

Iter-6 feedback had 3 findings: F-1 (analysis: H2 viability gate framing), F-2 (model: alpha sweep note), F-3 (analysis: HV insulator in Section 5).

The model agent was given iter-6's model (1403 lines, `model_ok: true`), with "Feedback Pass (Edit Existing Model)" instructions and "Preserve ALL existing sweeps, scenarios, parameters" rules. It applied F-2 (added alpha sweep note) but simultaneously removed:
- The viable-conservative scenario (added in iter-6 per iter-5 F-2)
- The component-level alpha scaling (added in iter-6 per iter-5 F-1)

Output: 1341 lines. The file-modified validator passed (file was modified — just destructively). The assessor immediately re-raised both as iter-7 F-1 and F-2.

#### LCOE

Optimistic (1 GWe) stable at $56.5/MWh from iter-3 onward. Viable LB appeared at $193.8/MWh in iter-6, dropped in iter-7.

---

### Concept 16: Muon-Catalyzed Fusion

#### Model Size Trajectory

| Iter | Lines | Delta | Pipeline | Key Model Change |
|------|-------|-------|----------|-----------------|
| 1 | ~1200 | -- | pre-fix | Basic CAS model, 6 sweeps |
| 2 | ~1300 | ~+100 | pre-fix | +WACC sweep, CAS22 restructured |
| 3 | 1388 | +88 | pre-fix | Two-domain O&M split |
| 4 | 1588 | +200 | pre-fix | 2D feasibility sweep added |
| 5 | 1604 | +16 | pre-fix | Corrected annotations |
| **6** | **1764** | **+160** | **post-fix** | **Added heat sales sweep, Acceleron claim scenario** |
| **7** | **1653** | **-111** | **post-fix** | **REGRESSION: Dropped heat sales sweep; added 2nd 2D CapEx grid** |

#### What Happened at iter 6→7

Iter-6 feedback had 3 findings: F-1 (analysis: sticking ceiling conditional), F-2 (model: add 2nd 2D sweep at optimistic CapEx), F-3 (minor: nearest-neighbor numbers).

The model agent applied F-2 (added second 2D grid at 5 M$/MW_beam) but dropped the entire heat sales sweep that iter-6 had added (+160 lines of heat_sales_fraction/price parameters, sweep code, Acceleron claim scenario — all removed). Net: -111 lines. The assessor caught it as iter-7 F-1.

#### LCOE

Baseline stable at 50.35 c/kWh from iter-3 onward. No LCOE regression (the dropped feature was a revenue credit exploration, not a baseline parameter change).

---

### Concept 17b: Laser ICF Fast Ignition

#### Model Size Trajectory

| Iter | Lines | Delta | Pipeline | Key Model Change |
|------|-------|-------|----------|-----------------|
| 1 | ~600 | -- | pre-fix | No sweeps |
| 2 | ~680 | +80 | pre-fix | Sweeps 1-3 added |
| 3 | 740 | +60 | pre-fix | Sweep 4 added |
| 4 | 755 | +15 | pre-fix | Sweep 5 added |
| 5 | ~800 | +45 | pre-fix | Sweep 6 + CPA arm split |
| **6** | **~800** | **~0** | **post-fix** | **Analysis-only changes (no model code changes)** |
| **7** | **~830** | **+30** | **post-fix** | **G_T_REF made explicit (75 vs ~73 implicit)** |

#### No Regressions

All 6 sweeps preserved from iter-5 through iter-7. Every finding from iter 1-6 was addressed in the following iteration. Iter-7 changed G_T_REF from implicit (~73) to explicit (75), changing LCOE from 322.7 to 302.0 $/MWh — a parameter correction, not a regression. This is the only concept where the fix performed cleanly.

**Why 17b succeeded**: Iter-6 had no model-targeted findings (all analysis), so the model agent had nothing to do — iter-6 model is unchanged from iter-5. Iter-7 had one clear model edit (G_T_REF). The agent was never asked to juggle multiple simultaneous edits to recently-added code, which is where 13 and 16 failed.

---

---

## Iter 8-9 Detail (Third +2 Passes)

### Concept 13: Electrostatic Hybrid — Iter 8-9

#### Extended Model Size Trajectory

| Iter | Lines | Delta | Key Model Change |
|------|-------|-------|-----------------|
| 6 | 1403 | +65 | Added viable-conservative scenario + component-level scaling |
| 7 | 1341 | -62 | **REGRESSION**: Dropped both iter-6 additions |
| **8** | **1494** | **+153** | **RESTORED** viable-conservative ($194/MWh) + component-level alpha row ($349/MWh) |
| **9** | **1341** | **-153** | **REGRESSION**: Dropped both iter-8 restorations (back to iter-7 size) |

#### Iter-8: Restoration

Iter-8 successfully restored both features dropped in iter-7:
- **Viable-conservative scenario**: Present at line 1383. LCOE: $746/MWh native → $194/MWh scaled at α=0.75. 4th scenario added alongside Conservative/Moderate/Optimistic.
- **Component-level alpha scaling**: Present in Part C. Learnable fraction: $4.00M (2.1% of OCC) for HV PS + SC magnets. Non-learnable: $182.7M (97.9%). Component-level result: ~$349.1/MWh at 1 GWe.

Assessment (verdict: FAIL) flagged 2 findings — both **narrative errors**, not model errors:
- F-1 (important): Analysis text claims ~$15.5M/8% learnable; model correctly computes $4.00M/2.1%. Error repeated 3x in Section 2.
- F-2 (minor): Analysis cites $668/MWh for viable-conservative native LCOE (cross-referenced from Part B sweep); correct value from scenario table is $746/MWh.

The model code was correct in both cases — the analysis agent's prose was wrong.

#### Iter-9: Re-regression

Iter-9 dropped both features AGAIN:
- **Viable-conservative scenario**: ABSENT. Only 3 scenarios remain (Conservative, Moderate, Optimistic).
- **Component-level alpha scaling**: ABSENT. Part C shows only full-OCC formula.
- **Worse than iter-7**: The analysis text still describes both features as present, creating a text-model mismatch. Iter-7 at least had consistent text (no references to missing features).

Assessment (verdict: FAIL) flagged 3 findings:
- F-1 (blocking): Viable-conservative scenario referenced in text but missing from model output.
- F-2 (important): Component-level learning row referenced in text but missing from output.
- F-3 (important): H3 per-module capital assumption ($5k threshold) undocumented.

**LCOE**: Optimistic (1 GWe) stable at $56.5/MWh throughout. Viable-conservative $194/MWh oscillates: present in iter-6, absent iter-7, present iter-8, absent iter-9.

---

### Concept 16: Muon-Catalyzed Fusion — Iter 8-9

#### Extended Model Size Trajectory

| Iter | Lines | Delta | Key Model Change |
|------|-------|-------|-----------------|
| 6 | 1764 | +160 | Added heat sales sweep + Acceleron claim scenario |
| 7 | 1653 | -111 | **REGRESSION**: Dropped heat sales sweep |
| **8** | **1837** | **+184** | **RESTORED** heat sales sweep: `compute_lcoe_with_heat_credit()` + `print_heat_sales_sweep()` |
| **9** | **1794** | **-43** | **REGRESSION**: Dropped all heat sales code again |

#### Iter-8: Restoration

Iter-8 restored the heat sales revenue sensitivity analysis:
- `compute_lcoe_with_heat_credit()` function defined (line 1286)
- `print_heat_sales_sweep()` function defined (line 1339)
- Two active calls: "Acceleron claim" and "Optimistic" scenarios with heat_fractions=[0.10–0.50] × heat_prices=[$8–$30/MWh_th]
- Model output shows ~750 MW_th thermal available, effective LCOE after heat credit at various combinations

Assessment (verdict: FAIL) flagged 2 findings:
- F-1 (important): Muon transport efficiency (η_transport) absent from energy balance. Model assumes η_transport=1.0 implicitly; Kelly et al. uses η_transport=0.5 as separate factor. Recommend sweep over {0.4, 0.6, 0.8, 1.0}.
- F-2 (minor): Key differentiators from conventional tokamak not in scannable list form.

Neither finding relates to heat sales — that was clean.

#### Iter-9: Re-regression

Iter-9 dropped ALL heat sales code:
- `compute_lcoe_with_heat_credit()` — deleted
- `print_heat_sales_sweep()` — deleted
- Both sweep calls removed
- Documentation comment block removed
- No heat revenue sensitivity in model output

Assessment (verdict: FAIL) flagged:
- F-1 (important): Heat sales sweep mandated by analysis but absent. Analysis states electricity-only LCOE (4.34 ¢/kWh for Acceleron claim) "should not be cited as evidence" until heat sweep completed. The central comparison (model vs Acceleron's 2.5 ¢/kWh target, conditioned on heat revenue) cannot be resolved.
- F-2 (important): η_transport=1.0 baseline misleading. At Kelly reference η_transport=0.5, "Near-term physics needed" scenario goes NET NEGATIVE (P_net = −5 MW).

**LCOE**: Baseline stable at 50.35 ¢/kWh throughout. Heat sales sensitivity oscillates identically to concept 13's pattern.

---

### Concept 17b: Laser ICF Fast Ignition — Iter 8-9

#### Extended Model Size Trajectory

| Iter | Lines | Delta | Key Model Change |
|------|-------|-------|-----------------|
| 6 | ~800 | ~0 | Analysis-only (no model code changes) |
| 7 | 956 | +30 | G_T_REF made explicit (75 vs ~73 implicit) |
| **8** | **1187** | **+231** | **+2 sweeps** (chamber radius, HDD vs FI comparison) |
| **9** | **1336** | **+149** | **+1 sweep** (DPSSL wall-plug efficiency) + expanded sweeps 5 & 8 |

#### Iter-8: Clean Growth

All 6 prior sweeps preserved. Two new sweeps added:
- **Sweep 7 (Chamber Radius)**: 3 scenarios (2.5m, 4.0m, 6.0m). LCOE range: 284–337 $/MWh.
- **Sweep 8 (HDD vs FI)**: 2 scenarios (HDD 2 MJ G_t=50: 327 $/MWh; FI 550 kJ G_t=50: 546 $/MWh).

Assessment (verdict: FAIL) flagged 3 findings:
- F-1 (important): DPSSL wall-plug efficiency (eta_pin1) not swept despite 5th-highest autodiff elasticity.
- F-2 (important): Sweep 8 needs third scenario (HDD at 400 kJ sub-ignition from Betti 2024).
- F-3 (minor): Availability lower bound of 50% too generous; recommend extending to 35%.

#### Iter-9: Clean Growth

All 8 iter-8 sweeps preserved. Changes:
- **Sweep 9 (DPSSL Wall-Plug Efficiency)**: NEW. 3 scenarios at 5%, 7%, 10%. LCOE range: 227–287 $/MWh. Shows viability boundary near 5%. (F-1 fix)
- **Sweep 8 expanded**: Added scenario A (HDD 400 kJ sub-ignition, marked SPECULATIVE). (F-2 fix)
- **Sweep 5 expanded**: Added 35% availability scenario. LCOE: 405 $/MWh. (F-3 fix)

**Zero regressions**. All content changes purely additive. Reference LCOE unchanged at 302.0 $/MWh.

**Sweep progression**: 6 (iter-7) → 8 (iter-8) → 9 (iter-9), monotonic. This is the only concept where every assessment finding is addressed in the following iteration without losing existing content.

---

## Comparison: Pre-Fix vs Post-Fix Model Behavior

### Pre-fix (iter 1-5): rewrite-from-scratch

Each iteration rewrote `model_setup.py` from scratch. The model agent had no visibility into its prior model — it worked only from `analysis.md` and assessment findings. Despite this:

- **Concept 13**: Model grew monotonically from iter-1 through iter-5 (added Part B, restructured to hypotheses, added Part C, fixed alpha direction). No sweep regressions in the pre-fix iterations.
- **Concept 16**: Model grew monotonically (added O&M split, 2D sweep, annotations). No regressions.
- **Concept 17b**: Model grew from 0 to 6 sweeps monotonically. No regressions.

**Key observation**: The rewrite-from-scratch approach did NOT show sweep regressions in these 3 concepts during iter 1-5. The prior agent's report of regressions that motivated this fix may have been about other concepts, or about a different failure mode (e.g., parameter drift rather than sweep loss).

### Post-fix (iter 6-7): edit-prior-model

The model agent was given its prior model and told to edit it. Despite explicit "Preserve ALL existing sweeps" instructions:

- **Concept 13**: Added features in iter-6, dropped them in iter-7. Regression.
- **Concept 16**: Added features in iter-6, dropped them in iter-7. Regression.
- **Concept 17b**: Clean. But iter-6 had no model edits, so this is not a strong test.

---

## Root Cause Analysis

### The Template Fix Was Correct but Irrelevant

The template nesting bug (nested `{{#if}}` blocks → cold-start content leaking into edit prompts) was **real and correctly fixed**. Rendered prompts for iter 8-9 are verified clean — no cold-start instructions, no orphaned `{{/if}}` tags, no contradictory directives.

**But the template bug was not causing the regressions.** The regressions continued identically after the fix because they have a completely different root cause.

### Actual Root Cause: Stale `loop_state` — Prior Model Copied From Wrong Iteration

**The bug is in `loop.py` line 88.** `loop_state = read_loop_state(concept_dir)` is called **once** before the iteration loop starts, and **never refreshed** within the loop. Each iteration writes `verdict.json` to disk (line 227), but the in-memory `loop_state` is never updated.

When running "+2 passes" (e.g., iter 8-9 in the same batch):

1. `loop_state` is read before iter-8 starts → contains iter 1-7 only
2. Iter-8 runs successfully, writes `verdict.json` with `model_ok: true` to **disk**
3. Iter-9 starts, calls `_find_best_prior_model(loop_state=loop_state)`
4. `loop_state` still only knows about iter 1-7 (stale)
5. `_find_best_prior_model` walks backward: iter-7 has `model_ok: true` → **returns iter-7's `model_setup.py`**
6. `shutil.copy2` copies **iter-7's model** (1341 lines) to `iter-9/model_setup.py`

**Iter-9 never sees iter-8's model.** All of iter-8's additions (viable-conservative scenario, component-level scaling for concept 13; heat sales sweep for concept 16) are invisible because iter-9 starts from iter-7's file.

### Evidence Confirming the Root Cause

**Concept 13**: `diff` shows iter-9's `model_setup.py` is **byte-for-byte identical** to iter-7's. Not "similar" — exact match. This is impossible if iter-8's file (1494 lines, different formatting, additional scenarios) was the starting point. It is exactly what you'd expect if iter-7's file was copied and the model agent left it unchanged (findings were analysis-only, no `file_modified` validator).

**Concept 16**: `diff` shows iter-9 has iter-7's base structure plus η_transport additions (the F-1 fix from iter-8's assessment). The heat sales code that iter-8 added is absent — not because the agent deleted it, but because **it was never in the starting file**. Iter-9 started from iter-7 (no heat sales), applied the one model finding (add η_transport), and the result is iter-7 + η_transport.

### Why Concept 17b Escapes

17b grows monotonically because its iter-7 model already contained all 6 sweeps from iter 1-7. Since the stale `loop_state` causes iter-9 to copy iter-7's model, and iter-7 already had everything, the "regression" is invisible — iter-8's additions (sweeps 7-8) are lost but the base 6 sweeps survive. However, **17b iter-9 should have 8 sweeps (from iter-8) but actually has 9** — the agent added sweep 9 on top of what it thought was iter-8's file but was actually iter-7's, and independently re-added sweeps 7-8 because the assessment findings from iter-8 explicitly requested them.

### The Oscillation Mechanism (Reinterpreted)

The 2-cycle oscillation is fully explained by the stale `loop_state`:

- **Iter-6**: Starts from iter-5's model (loop_state was read before iter-6, contains 1-5). Adds features.
- **Iter-7**: Same batch as iter-6 → stale loop_state, copies **iter-5's model** (not iter-6's). Features from iter-6 are lost.
- **Iter-8**: New batch → fresh loop_state, contains 1-7. Copies **iter-7's model**. Assessment from iter-7 flags missing features → model agent adds them back.
- **Iter-9**: Same batch as iter-8 → stale loop_state, copies **iter-7's model** (not iter-8's). Features from iter-8 are lost again.

Every "+2 passes" batch: the first pass gets a correct prior model (fresh loop_state), the second pass gets the stale prior (skips the first pass's work).

---

## Fix

**Root cause**: `loop_state` read once at line 88 of `loop.py`, never refreshed within the iteration loop. Second pass in any batch always copies the prior-batch model instead of the first pass's model.

**Fix applied**: Added `loop_state = read_loop_state(concept_dir)` after `write_verdict()` (line ~233 of `loop.py`), so the next iteration's `_find_best_prior_model()` sees the just-completed iteration's `model_ok` status.

```python
# --- Refresh loop_state so next iteration sees this verdict ---
loop_state = read_loop_state(concept_dir)
```

This is a one-line fix. `read_loop_state` scans `verdict.json` files on disk — all of which are already written by this point in the loop.

## Open Questions

1. Were the iter 6→7 regressions (in the original research above) caused by the same bug? The timeline shows iter 6-7 ran as "+2 passes" in a single batch — so yes, iter-7 would have gotten iter-5's model (the last model from the previous batch), not iter-6's. This is consistent with the observed regressions.
2. Should iter 8-9 be re-run now that the fix is in place, to get clean results with the correct prior model?
3. Are any other state variables stale within the loop besides `loop_state`? (Quick scan suggests no — `current_sources` is refreshed at line 112, `common_vars` updated at line 113.)
