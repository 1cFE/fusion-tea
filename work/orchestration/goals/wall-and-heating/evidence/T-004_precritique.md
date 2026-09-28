# T-004 pre-execution framing critique — verdict **MAJOR**

Fresh non-author `general-purpose` session, 2026-09-03, run before any of the study's points executed. Spawn prompt: `T-004_precritique_prompt.md`. This discharges `run-study` runbook step 4's obligation and is recorded as a named review outcome in the study record § 14.

The critique read the study definition, the axis declarations, the oracle scan, both indicator files, the study policy, the runbook, and the goal's T-004 scope. Its numbers come from the committed `results/window_scan.json` plus its own read-only oracle probes. It executed nothing, edited nothing, committed nothing.

**All nine findings accepted.** The three MAJOR ones were re-verified by the round agent against the oracle before acting — the verification is reproduced below each, because a critique taken on trust is not evidence.

---

## F1 (MAJOR) — there is no interior efficiency optimum, and the study was built to find one

The first design read "0.55 beats 0.60" off the scan (272.412 against 273.046) and built a transect to resolve an interior optimum. That comparison was between the **best point at each efficiency**, which are different (I, T, n) points. It is a fence-edge artifact: 0.55 was simply the lowest efficiency whose best point cleared the sustainment fence.

**Round-agent verification, at fixed (I = 14.5 MA, T = 16, n = 1.0x, wall-plug 220):**

| eta_source | 0.350 | 0.425 | 0.475 | 0.525 | 0.550 | 0.575 | 0.600 | 0.625 | 0.650 |
|---|---|---|---|---|---|---|---|---|---|
| LCOE | 269.823 | 270.803 | 271.451 | 272.093 | 272.412 | 272.730 | 273.046 | 273.361 | 273.675 |
| `p_wallplug_total` | 220.0 | 220.0 | 220.0 | 220.0 | 220.0 | 220.0 | 220.0 | 220.0 | 220.0 |

Strictly monotone increasing, and **structurally so**: at fixed wall-plug power the recirculating term *is* the wall-plug key, so it does not move with efficiency at all, while heating capital = rate x p_wallplug x eta_source rises exactly linearly (4.068e8 → 7.555e8 across the row). The only gain is coupled power, which does not pay for the capital.

**So efficiency at fixed wall-plug buys feasibility and never economics** — and the study's headline question was being asked in the one parameterization where the answer is forced by construction.

**Disposition:** accepted in full. The interior-optimum claim is deleted everywhere. `arm-transect-eta` is reframed as a **sustainment-crossing locator** (analytic `eta* = p_aux_required / p_wallplug = 115.24 / 220 = 0.52382` at the anchor). A fourth arm, **`arm-couple-110`**, is added at constant *coupled* power (`p_wallplug = 110 / eta_source`), where delivered power and heating capital are held and the whole effect of efficiency lands on the wall-plug draw. That is the parameterization in which efficiency can pay, and it is a **scope extension** recorded as such in `study.py` and in the trail.

## F2 (MAJOR) — every number the 220 MW arm produces is a wall-fence boundary result

At 220 MW the LCOE optimum, the feasible band and the efficiency threshold are all set by `wall_load_ok` and nothing else. LCOE falls monotonically with density (n 1.0 → 1.1 takes 273.05 → 235.78), with temperature (T 16 → 17 takes 273.05 → 243.50), and with decreasing current — and the only thing that stops it each time is the wall. The best feasible point sits at wall load **3.949 against the 4.05 limit, 97.5% of it**.

Combining T-001's two corrections — shaped area 1.15–1.30x larger (which lowers the average) and peak-to-shaped-average 1.5–2.1 — gives a net **1.15x to 1.83x** on the current operand. At the low end the best point reads 4.54 against 4.05 and is **violated**.

**Disposition:** accepted. The caveat is extended from "every fence claim" to **every claim the search arm makes**, and `points.csv` gains shadow columns `wall_load_shadow_lo/hi` at both bounds with their verdicts and a `feasible_shadow_lo` column — the caveat becomes data a later reader can act on rather than prose they must remember. This pre-registers round 2's impact on round 1's result instead of leaving the next agent to discover the reading was fragile.

## F3 (MAJOR) — two structural claims contradicted the study's own indicator files

**(a)** The first design said "both efficiencies and the wall-plug power now reach `sustainment_ok`". `pre_wi039_indicators.json` shows the pre-change `p_input+tie` **already reached it**. The one genuinely new reach in the whole comparison is **`eta_source_heat` → `sustainment_ok`**. Bundling the wall-plug key into the gain inflated a real, single, clean result.

**(b)** The first design said the efficiency "now moves coupled power (hence fusion performance and the sustainment fence)". False: `eta_source_heat`'s reachable objectives are identical to the old `eta_pin`'s.

**Round-agent verification, at fixed (I, T, n), across eta 0.40 / 0.50 / 0.60:** `p_fus` = 3465.678934 at all three; wall load = 3.948919; beta = 0.03325703; `p_aux_required` = 115.240710. Bit-identical. **Fusion performance does not respond to heating anywhere in this package.**

The critique also checked the comparison's mechanics and found them fair: same tool digest on both files, same package path, same nine-constraint catalog, same schema.

**Disposition:** accepted. Both claims restated to their true, smaller form in `study.py` and `axes.json`. The correction matters beyond this study — the inflated version would have propagated into the record and into the Row-4 re-grade.

## F4 (MAJOR/MINOR) — the I band was a 0.5 MA grid artifact on both ends

**Round-agent verification at eta 0.60, T = 16, n = 1.0x, 220 MW:**

| I (MA) | 14.00 | 14.25 | 14.50 | 15.00 | 15.25 | 15.50 |
|---|---|---|---|---|---|---|
| LCOE | 261.460 | **267.159** | 273.046 | 285.408 | 291.897 | 298.602 |
| wall load | 4.059 | 4.004 | 3.949 | 3.841 | 3.788 | 3.735 |
| verdict | wall-blocked | ok | ok | ok | ok | field-blocked |

14.25 is feasible **and cheaper** than the scan's "best" point, and feasibility continues past 15.0. The first design's window (14.25–15.0) would have reported its optimum at 14.25, its own lower edge, with nothing below it — precisely the `20260903-priced-levers#5` failure `goal.md` § Invariants bars.

**Disposition:** accepted. `I_P220` now runs 14.0 through 15.25, so a fence catches the bottom (14.0 is wall-blocked) and the top is not silently truncated. 64 extra points.

## F5 (MINOR) — the 100 MW negative can be stated absolutely instead of window-limited

Across the 245 points blocked by sustainment alone at 100 MW, the minimum required auxiliary power is **92.00 MW**. So the printed heating level opens only at `eta_source >= 0.92`. The honest claim is not "not in 0.40–0.60" but "not at any physically available source efficiency, by a factor of about 1.5". **Accepted**; stated in `study.py`.

## F6 (MINOR) — the `eta_couple_heat` declination was right for the wrong reason

The first reason given — that sweeping an unmeasured assumption "reads as knowledge the model does not have" — is wrong as a principle: a sensitivity to an assumption is how fragility is shown. The real reason is **degeneracy**: the two efficiencies enter the fence only as their product, so sweeping `eta_source` 0.40–0.60 at `eta_couple = 1.0` already delivers the entire `eta_pin` 0.40–0.60 fence sensitivity. What must travel with every result instead: **1.00 is the optimistic end**, so every feasibility claim here is made at the most generous possible coupling. **Accepted**; the reason is replaced and the optimism disclosed.

## F7 (checked, CLEAN) — `j_wp` is not shaping anything

The prompt named this as the hardest thing to check, on the predecessor's held-`T_i0` precedent. The critique probed 95 → 145 A/mm² at the search arm's best point: LCOE moves 0.08 $/MWh (0.03%) and `B_peak`, `p_aux_required` and wall load do not move at all, including at a field-blocked current. **This is not the predecessor's failure repeating.** Two items fall out: `j_wp` and the two direct-heat terms are now declared as declined axes and asserted in `export()`; and the inertness is itself a model-development observation — WI-036 priced the pack and the current density still reaches almost no cost.

## F8 (MINOR) — three of the nine verdict columns carry no information here

Across all 6160 scanned candidates `cond_strain_ok` never fires, `wp_stress_ok` fires 280 times but never alone, and `tbr_ok` is unreachable from every declared axis. Four fences decide anything, and effectively two. **Accepted**; disclosed so the record does not read as nine live fences.

## F9 (MINOR) — the pre-screen used the oracle seam's private API

`oracle_probe` called `oe._compute(oe._oracle_overrides(pt))`, against `oracle_entry.py`'s own stated contract of two published surfaces. It works today, but `evaluate` is the layer that fails closed on an unmapped output — exactly the protection a pre-screen wants. **Accepted**; rewritten to go through `evaluate`.

## What the critique checked and found sound

The ordering deviation (scan before critique) — accepted, and the critique notes that reading real numbers is what made F1, F2 and F4 possible at all. The scan's arithmetic reproduces exactly and independently: 6160 candidates, 0 errors, 0/3080 feasible at 100 MW, 35/3080 at 220 MW, blocked-alone counts sustain 245 / field 118 / wall 46, per-eta feasible counts 0, 1, 7, 11, 16. Baseline membership is by construction, not value-matching. Arm tagging is at construction. `manifest.json` carries only the `magnet__R0` tie, as claimed. The pre-screen will exclude nothing (`net_positive` never fires) and keeping it is right because a silent screen is the anti-pattern. Temperature is interior at 220 MW, so the `#5` invariant is satisfied on that axis.
