# Pre-execution framing critique — `20260903-priced-levers` — verdict MAJOR

Fresh non-author session, 2026-09-03; spawn prompt at `T-007_precritique_prompt.md`. Three major findings, five minor. **Both major findings were independently reproduced by the executor before dispositioning** — they are not taken on the critic's word, and both stand.

## The two that change the answer

### MAJOR 1 — the "priced" lever is barely priced

`j_wp` reaches **no magnet capital at all**. Executor's reproduction, oracle probe at the design point, p = 110, sweeping `j_wp` 60 → 140 A/mm² (a 2.3× swing in winding-pack cross-section):

| channel | j = 60 | j = 140 | change |
|---|---|---|---|
| `magnet_capital_rollup` | 5,401,032,000 | 5,401,032,000 | **0** |
| `magnet_cost` (1cfe form) | 6,323,469,946 | 6,323,469,946 | **0** |
| `aux_cooling__cryo_cost` | 20,976,293 | 15,999,989 | −5.0 M |
| `lcoe` | 365.572 | 365.206 | **−0.10%** |

And the relief that matters costs almost nothing: at 18 MA, moving `j_wp` from 118.83 to 112 takes stress from 821 → 797 MPa and moves LCOE by **+0.0258 $/MWh**.

**The executor's own indicator run had this evidence before execution** — `j_wp`'s reachable objectives were `cas72, lcoe, lcoe_1cfe, total_capital`, with `magnet_capital` absent — and the study docstring nonetheless described the arm as pricing "what a wider pack costs in cold mass, cryoplant load and capital." The design's D8 disclosed the cause honestly ("the pack's non-conductor mass has no cost home… 85% of the winding pack is steel, insulation, copper and helium, and only the conductor is costed") and the study framing then contradicted the disclosure.

**This is the goal's own defect, reappearing in the lever built to fix it.** `wp_stress_ok` is now relievable at essentially zero price. Priced-levers exists to remove exactly that.

### MAJOR 2 — the surviving fence is not the conductor ceiling; it is the wall load

The pre-registration ("at 50 MW the only fence left standing is the conductor ceiling") is an artifact of holding `T_i0` at 14.63 keV, the slice both this scan and the predecessor's grid arms inherited. Executor's reproduction, at p = 50, **below** the conductor ceiling, with temperature and density free:

| I_coil | T_i0 | n/n₀ | B_peak | σ | ε | p_aux req | wall load | violated |
|---|---|---|---|---|---|---|---|---|
| 15.4 MA | 17 | 1.2× | 24.900 | 566 MPa | 0.189% | 36.3 MW | 5.76 | **wall only** |
| 15.4 MA | 18 | 1.3× | 24.900 | 566 MPa | 0.189% | **−1.5 MW** | 7.36 | **wall only** |
| 15.0 MA | 18 | 1.2× | 24.253 | 544 MPa | 0.181% | 49.3 MW | 6.62 | **wall only** |

**Eleven such points.** Two of them require *negative* auxiliary heating — the plasma is self-sustaining with the heating off. Field, stress, strain, beta, net-positive and recirculation are all satisfied.

So at the printed 50 MW the machine's actual deadlock is **sustainment against neutron wall load**, not the conductor. The machine can sustain itself below the existing ceiling by running hotter and denser — and then the first wall cannot take the neutron flux. A better conductor grade does not touch that fence.

## The rest

3. **MAJOR — window provenance misstated.** The scan covered `I_coil` × `j_wp` at two heating levels; `n_e0` was never scanned and `T_i0` was not a candidate, yet the windows are commented as scan-derived across all axes. The `n_e0` window is also too narrow to test `beta_ok` (beta reaches 0.036 against a 0.05 limit everywhere in it), so the record would read "beta is not binding" when the window never asked.
4. **MINOR — declined axes not declared or traced.** Runbook step 3 requires indicators for declined axes too; `B_max`, `sigma_allow`, `T_i0`, `R`+tie and `a` are argued in prose but absent from `axes.json`. The predecessor's critique won this same fix.
5. **MINOR — arm attribution bug.** `arm_of()` infers the transect arm by value-matching, and `J_TRANSECT` shares 90/100/130 with `J_VALUES`, so three transect points are mislabelled into the p110 grid arm — carrying an off-window I column, the one sitting exactly on the ceiling.
6. **MINOR — the I grid cannot resolve the band it looks for.** The p110 feasible band is ~0.8 MA wide against a 1.0 MA step.
7. **MINOR — both WI-036 fences are inert where the machine is field-feasible.** σ maxes at ~654 MPa against 800, ε at 0.0022 against 0.004, for I ≤ 15.4 MA across the whole `j_wp` window. `wp_stress_ok` only flips at I ≥ 18 MA, where `peak_field_ok` has already failed.
8. **MINOR — the cross-pin comparison to 293.468 needs the § 12 treatment**, not a docstring mention.

## The critic's closing judgment, recorded because it is correct

> "The window was drawn where the expected answer lives, and the one axis that would disturb it is the one that was dropped."

## Dispositions — all eight accepted

1. **Accepted.** Reframe the transect from "what pack sizing costs" to "how little the priced chain charges for it, quantified", and register the missing cost home as a first-class model-development finding with a home, not an aside.
2. **Accepted.** `T_i0` becomes a declared swept axis; the scan is re-run over it before windows are fixed. The unqualified fence claim does not reach WI-038.
3. **Accepted.** Scan extended to `n_e0` and `T_i0`; windows re-fixed from it; the `n_e0` window widened until it can reach the beta limit or the record says it cannot.
4. **Accepted.** Declined axes declared and traced with reasons.
5. **Accepted.** Arms tagged at construction, not inferred from values.
6. **Accepted.** I refined to 0.2 MA over the band.
7. **Accepted.** Registered as a finding — it is the honest measured answer to "did pricing the pack change the fence structure."
8. **Accepted.** § 12 records the semantic boundary and what the comparison does and does not license.
