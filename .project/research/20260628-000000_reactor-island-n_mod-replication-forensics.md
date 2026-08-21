# Forensic investigation: reactor-island ×n_mod replication in 1costingfe (b9b0a4c → 0254385)

**Date:** 2026-06-28
**Repo investigated:** `/home/reid/1cfe/1costingfe` (read-only; no modifications made)
**Range:** `b9b0a4c` (fusion-tea's frozen version, 2026-06-15) → `0254385` (tag v0.1.0, HEAD, 2026-06-26)
**Trigger:** spike on concept 01 showed CAS22 reactor-island sub-accounts returning ratio ≈ 1.0 (apparently "frozen") under the 1 GWe projection, while BOP accounts scaled ≈ n_mod.

## Headline verdict

**NOT A REGRESSION. Also not an intended remodel — there was no behavior change at all.**

Reactor-island ×n_mod replication is intact at HEAD and is *byte-for-byte the same logic* as in the frozen `b9b0a4c`. I confirmed this two ways: by reading the code at both revisions, and by running the same bare-library probe against both (a throwaway worktree + scratch venv at `b9b0a4c`, now cleaned up). The scaling ratios are identical.

The spike's "ratio ≈ 1.0" finding is **real but misread**. It is reading `cas22_detail["C2201xx"]`, which is a **per-module** reporting line *by design* — it has always been per-module, in both versions. The plant total that actually feeds LCOE — `cas22_detail["C220000"]` and the top-level `costs.cas22` — **does** scale ×n_mod. So the headline reactor-island capital is **not** under-counted, and the two-knob contract (FR-4) is **satisfied** by the library, not broken.

If there is a problem anywhere, it is on the fusion-tea consumption side (if any code reads the per-module `cas22_detail` sub-account lines and treats them as fleet/plant totals). The library is correct.

---

## Q1 — Confirm the behavior at HEAD (0254385)

Two bare `forward()` calls on a tokamak/DT model, one native single-module, one 1 GWe multi-module at the same per-module power (P_native = 233 MWe, n_mod = 4, per-module power ≈ 250 MWe). Run from fusion-tea's venv against installed HEAD.

Using concept 01's real fixture (`spike` path):

| account | native | 1 GWe (n_mod=4) | ratio | meaning |
|---|--:|--:|--:|---|
| C220103 (magnets, reactor-island sub-account) | 434.713 | 434.713 | **1.000** | per-module reporting line — flat |
| C220101 (blanket) | 136.515 | 140.539 | 1.029 | per-module + mild power-law (233→250) |
| C220200 (coolant, plant-wide BOP sub-account) | 57.717 | 207.913 | 3.602 | scales ≈ n_mod |
| C220500 (fuel handling, BOP) | 43.284 | 120.000 | 2.772 | scales (power-law in plant total) |
| **C220000 (CAS22 rollup)** | 1437.600 | 5608.722 | **3.901** | **≈ n_mod — replicated** |
| **costs.cas22 (headline)** | 1437.600 | 5608.722 | **3.901** | **≈ n_mod — replicated** |
| costs.cas24 (electrical BOP) | 30.527 | 128.166 | 4.198 | ≈ n_mod |

So Q1's literal statement is confirmed at the **sub-account** granularity (C2201xx ratio ≈ 1.0, BOP ≈ n_mod), **but** the **plant total** `cas22` is *not* frozen — it rides ×n_mod (3.901 ≈ 4). The "freeze" is purely a per-module reporting convention on the detail lines.

## Q2 — When did it change

**It did not change anywhere in `b9b0a4c..0254385`.** Evidence:

1. The CAS22 compute/return is structurally identical at both revisions. At both `b9b0a4c` and HEAD, `cas22.py` returns raw per-module `c2201xx` values and computes the rollup as
   `c220000 = per_module_equipment * n_mod + total_labor + plant_wide`
   (HEAD line 754; b9b0a4c line 714 — same expression).
2. The override-application + rollup-recompute block in `model.py` is identical at both revisions (HEAD lines 1430–1442; b9b0a4c lines 1265–1277 — same `_PER_MODULE_KEYS`, same `per_module_equipment * n_mod` recompute).
3. Behavioral proof — same bare probe, both versions:

   | quantity | b9b0a4c | HEAD (0254385) |
   |---|--:|--:|
   | C220103 sub-account ratio (native→1GWe) | **1.000** | **1.000** |
   | C220000 rollup ratio | **3.923** | **3.956** |
   | cas22 headline ratio | **3.923** | **3.956** |
   | cas24 ratio | 4.186 | 4.186 |
   | per-module override C220103=500 rides ×n_mod? | yes | yes |
   | fractional n_mod accepted? | yes | yes |

   The *ratios* (the scaling behavior) are identical. Only absolute magnitudes moved (e.g. C220103 native 515.5 → 1132.99) — that is the account **recalibration** in `a168537`, not a change to replication.

The prime suspect `a168537` ("Release prep: plant-total power scaling (n_mod)…") **does** touch `cas22.py` and `model.py`, but its changes go the *opposite* direction from the hypothesis (see Q3/Q4).

## Q3 — How (the precise code change, and what it is *not*)

### What `a168537` actually did to `cas22.py`
Pure recalibration — swapped hardcoded reference powers for `CostingConstants` fields and retuned remote handling. None of it touches replication:
```
-    P_ET_REF = 1100.0  # MW gross electric
+    P_ET_REF = cc.ref_gross_power_mwe
...
-        c220107 = cc.power_supplies_base * (p_et / 1000.0) ** 0.7
+        c220107 = cc.power_supplies_base * (p_et / P_ET_REF) ** 0.7
...
-    concept_scale = rh_concept_scale.get(concept, 0.5)
-    c220110 = rh_base[fuel] * concept_scale * (p_et / 1000.0) ** 0.5
+    concept_scale = rh_concept_scale.get(concept, 0.55)
+    c220110 = rh_base[fuel] * concept_scale * (p_et / P_ET_REF) ** 0.5
...
-    c220201 = 166.0 * (p_net_total / 1000.0)
+    c220201 = 166.0 * (p_net_total / cc.ref_net_power_mwe)
```
The replication lines (`per_module_equipment * n_mod`, the per-module return dict) are **unchanged**.

### What `a168537` did to `model.py`
It **added** n_mod to BOP/indirect accounts that previously lacked it — this is the "plant-total power scaling (n_mod)" of the title, i.e. *more* replication, not less:
```
-            cas27_special_materials(cc, blanket_fill, blanket_vol),
+            cas27_special_materials(cc, blanket_fill, blanket_vol, n_mod),
...
-        c40 = cas40_owner(cc, self.fuel, pt.p_net)
+        c40 = cas40_owner(cc, self.fuel, pt.p_net, n_mod)
...
-        c50 = cas50_supplementary(cc, self.fuel, c20, ..., pt.p_net, noak)
+        c50 = cas50_supplementary(cc, self.fuel, c20, ..., pt.p_net, n_mod, noak)
```

### The replication logic that was in force the whole time
Reactor-island ×n_mod is produced by the **rollup**, not by the per-module detail lines. `cas22.py` (HEAD lines 736–754, same at b9b0a4c):
```python
per_module_equipment = (c220101 + c220102 + c220103 + ... + c220112)   # per module
total_labor = c220111 * (1.0 + (n_mod - 1) * cc.multi_unit_labor_factor)
plant_wide  = c220200 + ... + c220700                                   # already plant-total
c220000 = per_module_equipment * n_mod + total_labor + plant_wide       # <-- ×n_mod here
```
The `return {...}` then hands back `C220101…C220112` as **per-module** numbers (deliberately) and `C220000` as the **plant total**. Reading a `C2201xx` line and dividing native-by-projected gives 1.0 because both ends are per-module at the same per-module power — that is the spike's ratio, and it is meaningless as a replication test.

Overrides on reactor-island sub-accounts also ride ×n_mod, via the recompute in `model.py` (HEAD 1430–1442): an override lands in `c22_detail[key]` as a per-module value, then `C220000` is rebuilt as `per_module_equipment * n_mod + …`. Confirmed numerically: per-module override `C220103=500` → native rollup 2270.2, 1 GWe rollup 8952.8 (the 500 replicated across 4 modules).

`_scale_overrides` (HEAD 1663–1730) closes the loop for the two-knob projection: the reference forward runs at `n_mod=1` and `reference_mw=P_native`, the target forward at the caller's `n_mod`. For a per-module reactor-island account both ends evaluate at ≈ the same per-module power, so the scale ratio ≈ 1.0 — the override stays a per-module figure, and the rollup then multiplies it by n_mod. Its docstring explicitly cites "FR-2 of costingfe-library-preconditions," i.e. the maintainer implemented the two-knob contract on purpose.

## Q4 — Why (rationale)

There is no rationale to find for "removing reactor-island replication," because it was never removed. The relevant intentional changes in the range, with their stated rationale:

- **`a168537`** ("Release prep: plant-total power scaling (n_mod), net/gross reference-power unification, account recalibrations"): widened n_mod awareness to CAS27/40/50 and recalibrated CAS22 absolute costs against `CostingConstants`. Direction: *more* plant-total scaling.
- **`e29089e`** ("Widen n_mod parameter annotations from int to float (non-integer allowed for fusion-tea two-knob projection)"): kept fractional n_mod — confirms the two-knob projection was being *supported*, not reverted. `n_mod: float = 1.0` is the HEAD signature.
- **`f526fbb`** ("Fix #37: scale absolute overrides on library-zero CAS22 sub-accounts linearly with power instead of freezing"): the *only* override-scaling change in the range, and it is a narrow, different case — accounts the library computes as **$0** (no ratio available), now scaled linearly with net power. Its comment states the principle directly: "reactor-island hardware grows with plant size, so scale it linearly … rather than freezing." This is the maintainer affirming reactor-island replication, not breaking it.

## Q5 — Intended remodel or regression? (with the deciding evidence)

**Neither — no behavioral change occurred.** The deciders:

1. Identical scaling *ratios* at b9b0a4c and HEAD across reactor-island, rollup, BOP, and override paths (Q2 table). Behavior is the same; only calibrated magnitudes moved.
2. The replication code (`per_module_equipment * n_mod`, the per-module return, the override rollup-recompute) is unchanged across the range.
3. **No tests were deleted or rewritten to unpin replication.** `git log --diff-filter=D b9b0a4c..0254385 -- tests/` is empty. No `test_override_scaling_semantics.py` ever existed in repo history. The override-scaling logic is, if anything, *more* pinned now (`f526fbb` added 67 lines of tests in `test_model.py`).
4. The new model's multi-module reactor-island story is coherent and explicit: per-module equipment is costed once per module and multiplied by n_mod in the C220000 rollup (with a labor learning-curve discount via `multi_unit_labor_factor` and the `_scale_overrides` two-knob framing). The ×n_mod did not "disappear" — it lives in the rollup, exactly as it did at b9b0a4c.

The investigation's premise ("reactor-island replication was intentionally removed/remodeled in the release") is **false**. The fusion-tea research note's account-class model ("Class U = per-unit ×n_mod includes the C2201xx sub-accounts") is actually a **correct** description of the headline behavior — the rollup includes those sub-accounts ×n_mod. The confusion came from reading the per-module `cas22_detail` lines directly.

## Q6 — Fractional n_mod (side question)

**The library accepts fractional n_mod at HEAD; the integer is the spike's doing.** Confirmed: `forward(net_electric_mw=1000, n_mod=4.2918)` runs cleanly at both HEAD and b9b0a4c. The signature is `n_mod: float = 1.0` (widened by `e29089e`). The `n_mod=4` (per-module 250, not native 233) comes from the spike script's `proj_n_mod()` (`max(1, int(round(1000/P)))`), not the library.

---

## What this means for fusion-tea (no library change needed)

There is nothing to fix in 1costingfe. The minimal-change question is moot because there is no regression.

The real action item is on the **fusion-tea side**: verify how the pipeline consumes CAS22.
- If headline reactor-island capital is taken from `costs.cas22` (or `cas22_detail["C220000"]`), it is **already correct** (×n_mod) and no low-P_native concept is under-counted.
- If any code path reads the per-module `cas22_detail["C2201xx"]` lines and treats them as plant/fleet totals (summing them for a headline, displaying them as fleet cost, or feeding them somewhere that doesn't re-multiply by n_mod), **that** path would under-count by ≈ n_mod — but the bug would be in fusion-tea's reader, not the library.

Recommend updating the two affected research notes (`20260606-093951_override-scaling-semantics-by-account-class.md`, `20260607-100000_concepts-affected-by-1gw-override-policy.md`) and the spike's conclusion to distinguish **per-module detail line** (ratio 1.0, by design) from **plant total** (×n_mod). The "frozen reactor-island" framing is an artifact of reading the detail lines.

## Method notes / reproducibility

- Bare probe `/tmp/bare_probe.py`: `CostModel(concept=TOKAMAK, fuel=DT)`, two `forward()` calls + a per-module override case + fractional-n_mod check. Run under HEAD (fusion-tea venv) and under b9b0a4c (throwaway `git worktree` + `uv venv` scratch env). Both the worktree and scratch venv have been removed; the pre-existing `1costingfe-master` worktree was left untouched.
- Concept-01 fixture probe `/tmp/q1_probe.py` reproduced the same ratios through the real fusion-tea model_setup.
- No files in `/home/reid/1cfe/1costingfe` were modified.
