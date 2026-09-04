# Study record — `20260903-wall-and-heating`

## 1. Study header

- **Study id:** `20260903-wall-and-heating`
- **Package:** `stellarator_tea` (`exploration/stellarator_e2e/pkg/stellarator_tea`)
- **Date executed:** 2026-09-03
- **Executor:** round agent, goal `wall-and-heating` round 1, task T-004. The 639 points executed on 2026-09-03; runbook steps 5, 6 and 10–15 were completed and this record written on 2026-09-04 by the resuming round-1 session, from the committed results and nothing else.
- **Mode:** execute
- **Arms:** `arm-fence-p100`, `arm-search-p220`, `arm-transect-eta`, `arm-couple-132`

## 2. Intake

The owner's goal and scope, in their own words, verbatim. The goal this study serves was directed by:

> "we need to create a new goal for the wall-load and the heating structure" — [OWNER-VERBATIM 2026-09-03, relayed by the `priced-levers` round-1 handoff]

The round-1 strategy that names this study as its one committed study was ratified with:

> "great, please write a /_my_handoff for the next goal agent to run this" — [OWNER 2026-09-03]

under the standing delegation, re-ruled for this goal:

> "no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!" — [OWNER-VERBATIM 2026-09-02; re-ruled for `wall-and-heating` 2026-09-03, `goal.md` § Reserved gates ruling 5]

**Executor's own additions, kept separate from the quotes.** The study question — *with the heating chain live, what does the heating system do to LCOE and to the fence structure at the printed heating level and at the higher one, and does the chain's new lever, source efficiency, buy anything the old held `eta_pin` could not?* — is the executor's phrasing of the trail's § T-004 scope, not the owner's words. The four arms, their windows, the five declined axes, and the constant-coupled arm are the executor's under the delegation, shaped by the pre-execution critique (§ 14). **One scope extension, stated rather than slipped in:** § T-004 scope authorized `p_wallplug_heat` "at the two levels the predecessor study used"; `arm-couple-132` sweeps it continuously as `132 / eta_source_heat`, a third level set outside the scope as written. It was added because the critique showed the scope as written could only produce a forced answer to the study's own question (§ 14, F1); both axes it moves are authorized, only their joint pattern is new; recorded in `study.py` and in the trail so the round review sees the extension rather than discovering it.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` (headline); `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` (comparison form)
- **LCOE result:** **267.159 $/MWh**, the constrained optimum of `arm-search-p220` under the wall fence **as bound**, at `eta_source_heat` 0.60, wall-plug 220 MW (132.0 MW coupled), I_coil 14.25 MA, T_i0 16.00 keV, n_e0 5.06e20 (1.0×), case `c0550`; its wall load is 4.004 against the 4.05 limit and its `lcoe_1cfe` reads 262.089. `arm-fence-p100` has **no feasible point** and therefore no constrained optimum; the pinned baseline is a member of that arm by construction and reproduces there at 307.08712042841586 with `sustainment_ok` violated (`c0113`). The study's lowest feasible LCOE, 255.970 at `eta_source_heat` 0.75 in `arm-couple-132`, is a transect endpoint at one held operating point and is not a search optimum. Under T-001's low wall-correction bound (§ 15 #3) the cheapest point that survives is **326.201** (`c0546`: eta 0.60, I 14.25 MA, T 14.63 keV, n 1.0×).

Over the studied space the objective is set by feasibility first and by the heating parameterization second. At 220 MW wall-plug the 91 feasible points span 267.159–461.616 $/MWh. At 100 MW wall-plug LCOE spans 136.387–437.495 and none of it is feasible. Along the constant-coupled transect LCOE falls 317.234 → 255.970 over efficiency 0.35 → 0.75, a 61.264 $/MWh swing with heating capital constant to the dollar. Along the fixed-wall-plug transect it *rises* 269.823 → 273.675 over 0.35 → 0.65. Same model, opposite signs — § 6 `eta_source_heat` and § 15 #2.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, over all 639 executed points. "Alone" means that verdict reads `violated` while the other eight read `satisfied`.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | mixed | violated **381 / 639** — the most common fence in this study (175 of 240 at 100 MW; 203 of 384 at 220 MW; 3 of 7 on the fixed-wall-plug transect); alone 36 times at 100 MW and 124 at 220 MW; violated at the pinned baseline (90.6 MW required vs 50 coupled, the disclosed WI-037 state). Computed-vs-**computed** since WI-039: the installed side is the chain's `heat__p_coupled`, so both sides move under a heating sweep |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | mixed | violated **318 / 639** (174 at 100 MW, 144 at 220 MW); alone 10 times at 100 MW and 77 at 220 MW; max observed 10.284 against 4.05. **The fence as bound compares a flat-wall average operand to a printed peak limit**; every verdict in this column carries that caveat, and `points.csv` carries T-001's correction bounds as shadow columns (§ 15 #3) |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | mixed | violated 96 / 639, all in `arm-fence-p100` at I ≥ 16 MA (max B_peak 27.487 against 24.9); alone 9 times, all at I 17 MA; never at 220 MW, whose window tops at 15.25 MA (B_peak 24.657) |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | mixed | violated 25 / 639, all in `arm-search-p220` at n 0.8× (max rec_frac 0.591 against 0.5); alone 13 times — the fence that catches the bottom of the density window |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | mixed | violated 12 / 639, all in `arm-fence-p100` at I 14–15 MA, T 19–22 keV, n 1.1–1.2× (max beta 0.0588 against 0.050); never alone. The 220 MW window reaches beta 0.0441 and does not test it |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied everywhere | violated 0 / 639; max strain 0.251% against 0.400% — inert here as in `20260903-priced-levers#3` |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied everywhere | violated 0 / 639; max 754 MPa against 800. The scan saw it fire 280 times of 6160 candidates and never alone; the executed windows do not reach it |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied everywhere | violated 0 / 639; the evaluability pre-screen excluded nothing (§ 11) |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied everywhere | violated 0 / 639 — held-vs-held, unreachable from every declared axis, unchanged since first recorded |

Four fences decide anything in this study and effectively two: sustainment and the wall. That is the critique's F8 confirmed on the executed points.

## 5. Framing

**As proposed at intake** — the framing submitted to the pre-execution critique (step 4). Where the first design differed, the Why column says so.

| Axis | Framing proposed | Why |
|---|---|---|
| `eta_source_heat` | search | The axis this round created. The first design framed it as an optimum hunt; the critique (F1) showed the "interior optimum" was a fence-edge artifact, so it was re-framed as a **boundary locator** for the sustainment crossing at fixed wall-plug, with the economics measured along two held parameterizations. |
| `I_coil` | search | The field lever; carried because the heating question cannot be read without the field fences that bound the same operating point. Window bracketed after F4. |
| `T_i0` | search | Swept past 18 keV at both levels (`20260903-priced-levers#5`; `goal.md` § Invariants). |
| `n_e0` | search | The power-density lever; window carried from the predecessor's critique-widened range so beta is testable. |
| `p_wallplug_heat` | sensitivity | Two levels (100 and 220 MW, the predecessor's 50 and 110 MW coupled restated at eta 0.50) plus the reciprocal transect. Not searched. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `eta_source_heat` | search | no | It locates a boundary — the sustainment crossing at eta* = 0.5238 on the transect (blocked at 0.475, feasible at 0.525), and per-efficiency feasible counts 7 / 18 / 28 / 38 over 0.45–0.60 in the search arm — and it finds **no interior economic optimum** at either held parameterization: LCOE is monotone in it both ways (§ 6). |
| `I_coil` | search | no | A bounded feasible band exists at 220 MW (14.25–15.25 MA) with the constrained optimum at 14.25, interior: every 14.0 MA point fails sustainment (28 of the 64 also fail the wall). At 100 MW no band exists at any current. |
| `T_i0` | search | no | At 220 MW the optimum sits at **16 keV, interior** (14.63 and 17 keV both feasible around it); nothing is feasible above 18 keV at either level though the windows reach 18 and 22 keV. The `#5` window-edge failure does not recur. |
| `n_e0` | search | no | Feasible band 0.8–1.1× at 220 MW with the optimum at 1.0×, interior: 0.8× is caught by `recirc_ok` (all 25 violations), 1.1× by the wall. |
| `p_wallplug_heat` | sensitivity | no | Two levels; no boundary claim in installed power (§ 6). |

## 6. Per-axis account

#### `eta_source_heat` — feasible structure (search framing)
**Applies:** yes

**The boundary.** At fixed 220 MW wall-plug and the transect anchor (I 14.5 MA, T 16 keV, n 1.0×), the plasma requires 115.241 MW coupled and the chain delivers `220 × eta`; the crossing is at eta* = 115.241 / 220 = **0.5238** (`results/oracle_operands.csv`, column `eta_source_crossing`), and the executed transect brackets it: 0.475 blocked by `sustainment_ok` alone, 0.525 feasible with 0.259 MW of margin. In the search arm the feasible count rises with efficiency, 7 / 18 / 28 / 38 over 0.45 / 0.50 / 0.55 / 0.60, and the cheapest feasible point at each is 283.559 / 272.533 / 272.412 / 267.159 — a fence-edge envelope over *different* (I, T, n) points, which is exactly the comparison the critique warned is not an optimum (§ 14, F1).

**At the printed level the boundary is out of reach.** In `arm-fence-p100` (100 MW wall-plug = 50 MW coupled at 0.50), 0 of 240 points are feasible. Among the 36 points blocked by `sustainment_ok` **alone** — the only ones a better source could rescue — the minimum required coupled power is **87.061 MW** (`c0036`: I 15.4 MA, T 17 keV, n 0.9×), so at 100 MW wall-plug the level opens only at `eta_source_heat` ≥ 0.871, and that at the optimistic `eta_couple_heat` = 1.00; across the 36 the crossing runs 0.871–1.629. The other 204 blocked points also fail the wall or the conductor ceiling, which no efficiency touches. The scan pre-registered this threshold at 0.92 over its 245 sustain-alone candidates on a coarser grid; the executed grid governs and its number is lower. The pinned 1costingFE gyrotron value is 0.50 (`defaults.py:96-108` at pin `0254385`); no source in the repository bounds achievable gyrotron efficiency, so this record states the threshold and makes **no buildability claim** beyond the pinned value — the critique's "no gyrotron is within a factor of 1.5 of that" (F5) is its own remark, unsourced here.

**The economics, which are not an optimum but a sign that depends on what is held.** At **fixed wall-plug** (the transect): LCOE 269.823 / 270.803 / 271.451 / 272.093 / 272.730 / 273.361 / 273.675 over eta 0.35 → 0.65, strictly rising; heating capital 406.78 → 755.45 M$, exactly linear in eta (rate × wall-plug × eta_source); the wall-plug draw constant at 220.0 MW; coupled power 77.0 → 143.0 MW; net electric 910.0 → 931.3 MW from the added coupled power; `p_fus`, wall load and `p_aux_required` constant to every digit. Better efficiency at fixed hardware buys feasibility and never economics. At **fixed coupled power** (`arm-couple-132`, 132 MW coupled at I 14.25 MA, T 16 keV, n 1.0×): LCOE 317.234 / 300.248 / 288.297 / 279.432 / 272.594 / [267.159 at 0.60, read from `c0550` in the search arm] / 262.736 / 259.065 / 255.970 over eta 0.35 → 0.75, strictly falling with diminishing returns (28.9 $/MWh from 0.35 to 0.45; 6.8 from 0.65 to 0.75); heating capital constant at 697.34 M$; wall-plug draw 377.14 → 176.0 MW; `rec_frac` 0.4499 → 0.3096; net electric 788.66 → 989.81 MW; every point feasible with 3.363 MW of sustainment margin. The whole effect lands on the recirculating draw. **Fusion performance does not respond to heating anywhere in this package:** `p_fus`, wall load, beta and `p_aux_required` are bit-identical across the four efficiencies in all 96 (I, T, n) cells of the search arm (`results/points.csv`, `results/oracle_operands.csv`).

**What is and is not new about this, checked before it was claimed.** The pre-change model held coupled power and divided it by a held `eta_pin` inside the recirculating sum, so sweeping `eta_pin` at held `p_input` produced a falling curve of the same sign as the constant-coupled arm — the constant-coupled economics are **not** new to WI-039 (verified by running the pre-change oracle from a scratch worktree; its absolute numbers are not quoted as a matched comparison). What is new is narrower: **the fixed-wall-plug experiment was not expressible before**, because wall-plug power was not a quantity in the model but the expression `p_input / eta_pin`, and holding it fixed meant moving two held constants together by hand; and `eta_source_heat` reaches `sustainment_ok` where `eta_pin` did not (§ 8). Only one of the two opposite-signed experiments could be asked before.

#### `eta_source_heat` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed; the monotone responses above are reported under the search account because the axis also locates a fence.

#### `I_coil` — feasible structure (search framing)
**Applies:** yes

At 220 MW the feasible band is **14.25–15.25 MA**. The bottom is caught inside the window: at 14.0 MA every one of the 64 points fails `sustainment_ok` (required ≥ 134.4 MW against at most 132 coupled; 28 of them also fail the wall). Feasible counts rise with current — 4 / 10 / 17 / 25 / 35 over 14.25 → 15.25 — because higher field relieves the wall (lower `p_fus` per unit area at fixed n, T) and the sustainment requirement (ISS04). The top of the executed window, 15.25 MA, is not fence-caught inside the executed points; the conductor ceiling catches it one grid step above, at 15.5 MA, in the scan (280 field-alone candidates at 220 MW) and in the critique's F4 probe. The constrained optimum sits at **14.25 MA, interior** to the window, and at fixed (T, n) LCOE **rises** with current (261.460 wall-blocked at 14.0, then 267.159 / 273.046 / 279.5 / 285.408 / 291.897 feasible over 14.25 → 15.25 at eta 0.60, T 16, n 1.0×); the per-current best-feasible envelope (267.159 / 272.412 / 277.875 / 283.559 / 272.533) is not monotone because the feasible set changes with current, not because the response does. At 100 MW no band exists: I 14–15.4 MA is sustainment-blocked everywhere, I ≥ 16 MA is field-blocked everywhere (96 verdicts), and the points that clear both (10 wall-alone, 9 field-alone) fail a third fence.

#### `I_coil` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `T_i0` — feasible structure (search framing)
**Applies:** yes

At 220 MW the feasible temperature range is 14.63–18 keV (36 / 33 / 16 / 6 feasible over 14.63 / 16 / 17 / 18) and the constrained optimum sits at **16 keV, interior**: 14.63 keV's best is 275.089 and 17 keV's is 288.693, both feasible. Temperature relieves sustainment and loads the wall — at 17 and 18 keV the wall is violated at 48 and 68 of 96 points — and at fixed (I, n) LCOE falls with temperature until the wall stops it (at I 14.25 MA, n 1.0×, eta 0.60: 326.201 / 267.159 / 238.659 wall-and-sustainment-blocked / 217.350 wall-and-sustainment-blocked over 14.63 / 16 / 17 / 18 keV). Nothing is feasible above 18 keV at either level: the 100 MW window reaches 22 keV and the scan 24 keV, and every point there fails the wall or sustainment. The `20260903-priced-levers#5` failure — an optimum on the window's upper edge — does not recur here.

#### `T_i0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `n_e0` — feasible structure (search framing)
**Applies:** yes

At 220 MW the feasible density band is **0.8–1.1× baseline** with the optimum at 1.0×, interior. The bottom is caught by `recirc_ok` — all 25 of its violations sit at 0.8× (13 alone), where fusion power is too low for the recirculating fraction — and the top by the wall (50 of 96 points at 1.1× are wall-blocked alone, 22 more with sustainment). At fixed (I, T) LCOE falls with density until the wall: at I 14.25 MA, T 16 keV, eta 0.60 — 414.156 (sustainment-blocked) / 322.122 (sustainment-blocked) / 267.159 / 231.067 (wall-blocked) over 0.8 → 1.1×. Density carries the machine into the wall-limited region at both levels; at 100 MW the 1.2× column is wall-blocked at 44 of 60 points and the only wall-alone points sit at n 1.1–1.2×. `beta_ok` fires only at 100 MW (12 points at T 19–22 keV, n 1.1–1.2×); the 220 MW window tops at beta 0.0441 and makes no claim about the beta fence.

#### `n_e0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `p_wallplug_heat` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `p_wallplug_heat` — observed response (sensitivity framing)
**Applies:** yes

Two levels and one reciprocal transect. At 100 MW wall-plug (50 MW coupled at 0.50): 0 of 240 feasible. At 220 MW (110 MW coupled at 0.50): 91 of 384 feasible. Along `arm-couple-132` the wall-plug draw runs 377.14 → 176.0 MW at constant 132 MW coupled and every point is feasible. **No boundary claim is made in installed power**: this study does not locate the sustainment flip in wall-plug or coupled power, and the predecessor `20260901-sustainment-fence`'s committed flip between 90 and 100 MW coupled is neither refined nor contradicted. Where `sustainment_ok` goes violated across the swept space: everywhere at 100 MW except the 19 field- or wall-only points; at 220 MW at 203 of 384 points, concentrated at low current, low efficiency and low density; on the transect below eta 0.5238.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `p_wallplug_heat` | `stellarator_09__stellaris__p_wallplug_heat` | fan_out | The entry point WI-039 minted. **No tie is declared, and that is the change:** the `p_input`/`p_ecrh` tie the predecessor carried was removed because both powers now descend from this key through the chain. |
| `eta_source_heat` | `stellarator_09__stellaris__eta_source_heat` | fan_out | Did not exist before this round; the old `eta_pin` was a held constant. |
| `T_i0` | `stellarator_09__stellaris__T_i0` | fan_out | `T_e0` rides the held 0.95 ratio inside the sustainment calc. |
| `n_e0` | `stellarator_09__stellaris__n_e0` | fan_out | |
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | fan_out | |
| `eta_couple_heat` (declined) | `stellarator_09__stellaris__eta_couple_heat` | fan_out | Traced, held at 1.00 — § 8. |
| `R+tie` (declined) | `stellarator_09__stellaris__R` | fan_out | Traced, not swept — § 8. |
| `R+tie` (declined) | `stellarator_09__stellaris__magnet__R0` | **tie** | Same physical major radius; ANNEX § Declared ties; data in `manifest.json → ties`. |
| `a` (declined) | `stellarator_09__stellaris__a` | fan_out | Traced, not swept — § 8. |
| `B_max` (declined) | `stellarator_09__stellaris__magnet__B_max` | fan_out | Traced, not swept — § 8. |
| `j_wp` (declined) | `stellarator_09__stellaris__magnet__j_wp` | fan_out | Traced, checked, not swept — § 8. |

Eleven declared keys across ten groups; all validated as package inputs at preflight. Every held key — `a`, `availability`, `discount_rate`, `R` and its tie, `j_wp`, `eta_couple_heat`, and both dormant direct-heat terms — is asserted per case in `study.py` `export()`, not merely intended.

## 8. Indicators and rulings

Per proposed axis, including the five proposed and declined. Source: `indicators.json`, run over all ten groups (`subset: false`), tool digest `e53d7027…`.

| Axis | Indicator | Constraints reachable | Objectives reachable | Modules fired | Ruling |
|---|---|---|---|---|---|
| `I_coil` | `constraints_reachable` | 8 / 9 (all but `tbr_ok`) | 10 / 11 | 68 | swept |
| `R+tie` | `constraints_reachable` | 8 / 9 | 11 / 11 | 71 | **declined** — geometry is the wall half's and round 2's; `R`'s effect on wall load at this pin is an open measurement, and sweeping it here would confound the heating question with the wall question this round did not touch |
| `a` | `constraints_reachable` | 5 / 9 | 10 / 11 | 59 | **declined** — same reason; the committed `20260829-p-pump-fence` result (wall violated at every a ≥ 1.70) makes it the most confounding axis to add |
| `T_i0` | `constraints_reachable` | 5 / 9 | 8 / 11 | 55 | swept |
| `n_e0` | `constraints_reachable` | 5 / 9 | 8 / 11 | 55 | swept |
| `j_wp` | `constraints_reachable` | 4 / 9 | 4 / 11 | 53 | **declined, and checked rather than assumed** (critique F7) — see below |
| `p_wallplug_heat` | `constraints_reachable` | 3 / 9 (`net_positive`, `recirc_ok`, `sustainment_ok`) | 4 / 11 (`cas72`, `lcoe`, `lcoe_1cfe`, `total_capital`) | 49 | swept, two levels plus the reciprocal transect |
| `eta_source_heat` | `constraints_reachable` | 3 / 9 (the same three) | 4 / 11 (the same four) | 49 | swept |
| `eta_couple_heat` | `constraints_reachable` | 3 / 9 (the same three) | 4 / 11 (the same four) | 49 | **declined** — degenerate with `eta_source_heat` in the fence (they enter only as their product), so sweeping the source efficiency over 0.40–0.60 at `eta_couple` 1.00 already delivers the whole `eta_pin` 0.40–0.60 fence sensitivity; the two differ only in the cost term, second-order here. **1.00 is the optimistic end of the assumption, so every feasibility claim here is made at the most generous possible coupling** |
| `B_max` | `constraints_reachable` | **1 / 9** | **0 / 11** | 2 | **declined** — a pure fence-relaxer as bound; still unpriced, WI-038 is its vehicle after WI-040 |

**No axis reported `no_constraint_response`, so no owner ruling was owed under runbook step 4's fail-closed condition.**

**The structural comparison the study exists to make, read from `pre_wi039_indicators.json` (the same tool at the pre-WI-039 pin `6262dbf4…`) beside `indicators.json`.** Before WI-039 the held `eta_pin` reached `net_positive` and `recirc_ok` and four objectives; `p_input+tie` reached those two plus `sustainment_ok`. After it, `eta_source_heat`, `eta_couple_heat` and `p_wallplug_heat` each reach exactly `net_positive`, `recirc_ok`, `sustainment_ok` and the same four objectives. So **the one new reach in the whole comparison is efficiency → `sustainment_ok`**, through the installed side of the inequality only; the wall-plug key's reach is not new (the first design claimed it was — critique F3), and no efficiency reaches `p_fus`, wall load or beta, which the executed points confirm bit-identical across efficiency (§ 6).

**Not derivable, disclosed in every record.** Monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output. The monotone responses reported in § 6 are executed observations on the swept grids, not indicator claims.

**Model-development findings.** No axis reported `no_constraint_response`, so the table's obligation is discharged by a stated nil: none owed. The observations recorded alongside the rulings, because a ruling does not discharge them:

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `eta_couple_heat` | The deposition and coupling fraction is a held **assumption** at its optimistic end (1.00) with no sourced figure behind it; a sourced coupling value is the one input the chain still lacks. Standing at WI-039 as a stated assumption in the model text; no finding id minted for it | none — disclosed, not a new sighting |
| `j_wp` | Probed by the critique at 95–145 A/mm² at the search arm's best point: a 53% swing moves LCOE by 0.08 $/MWh (0.03%) and moves B_peak, `p_aux_required` and wall load not at all, including at a field-blocked current (`work/orchestration/goals/wall-and-heating/evidence/T-004_precritique.md` F7). WI-036 priced the winding pack and the current density still reaches almost no cost | `20260903-wall-and-heating#7` (re-sighting of `20260903-priced-levers#2`, routed to WI-040) |
| `B_max` | One inequality and nothing else; every feasibility claim at the ceiling is a claim about where that literal is set. Standing route WI-038 | none — standing at `20260901-sustainment-fence#1` |
| (none) | `tbr_ok` remains held-vs-held and reaches no swept axis. Standing, rubric Row 2c | none — standing |

## 9. Preflight results

`results/preflight_results.json`. **All six gates ran; all six pass.** The identity gate read `results/package_identity.json` and the baseline gate read `results/baseline_result.json`, both deposited by `study_route.execute_baseline` at step 5.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation (`declared_keys`) | pass | 11 declared keys across 10 groups, all package inputs |
| Suffix-sibling scan (warnings only; `sibling_scan`) | pass | no suffix-sibling findings |
| Identity (`identity`), against `results/package_identity.json` | pass | kind `sealed`, digest `b0c5f3eda9014fa1…` recomputed from 0 allowed-modified files and 0 declared sources; every other sealed artifact matches |
| Baseline gate against the pinned headline (`baseline_headline`), against `results/baseline_result.json` | pass | `stellarator_09__stellaris__lcoe_calc__lcoe` reproduces at relative deviation 0.000e+00 (307.08712042841586); **9/9** pinned verdicts match, `sustainment_ok` expected-violated |
| Manifest / package fingerprint match (`manifest_currency`) | pass | both recorded package fingerprints match the package on disk |
| Package cleanliness (`package_clean`) | pass | package tree byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API definition (`study.py` + `study_route.py`, `StudyRunner` + `PreparedListStrategy`)
- **Why this route:** the arms are coordinated axis-group blocks — each proposal carries all five swept keys, the declared `R` tie, and every held key including the two dormant direct-heat terms, and the fourth arm couples wall-plug power to efficiency as a reciprocal — which is not a plain Cartesian product over independent keys and so is outside the `teax-study` CLI's shape. The route was exercised at step 5 (identity and baseline emitted) and gated at step 6 before this rationale was written, so this is an account of a route already known to load.

**Glue disclosure — glue ledger: none.** `results/package_identity.json` records `kind: sealed`, zero allowed-modified files and zero adapter sources. The harness supplies no value the model does not compute; the package is sealed at runtime contract 2.0.0 on stock teax.

## 11. Study definition and window provenance

**Window provenance: `engineered`** — fixed after an oracle scan, and the scan is committed at `results/window_scan.json` (6160 candidates over `p_wallplug_heat` × `eta_source_heat` × `I_coil` × `T_i0` × `n_e0`, 0 oracle errors).

**The ordering deviation, recorded rather than hidden.** The runbook puts the scan at step 7, after the step-4 critique. The scan was run **before** the critique so the critique could read real numbers instead of proposed windows; no point ran through the sealed package, which is what step 4's "before any point runs" governs. The critique accepted the deviation and noted that reading real numbers is what made three of its findings (F1, F2, F4) possible at all. The same choice is available to a later study; disclose it the same way.

**What the scan fixed.** At 100 MW wall-plug the feasible set is empty at every efficiency scanned (0 of 3080 over 0.40–0.60); blocked-alone counts there were sustainment 245, field 118, wall 46, and the minimum required coupled power among the sustain-alone candidates was 92.0 MW. At 220 MW there were 35 feasible candidates in a band at I 14.5–15.0 MA (0.5 MA scan resolution), T 14.63–18 keV, n 0.8–1.1×, with the feasible count rising with efficiency 0 / 1 / 7 / 11 / 16 over 0.40–0.60. The density window reached beta 0.087 in the scan, so `beta_ok` is testable rather than inert. T was scanned to 24 keV, past the predecessor's window edge; nothing feasible appeared above 18 keV at either level, so the executed windows stop at 19–22 keV rather than carrying dead range.

**What the critique changed about the windows (§ 14).** F4 showed the scan's 0.5 MA current band was a grid artifact on both ends — 14.25 MA is feasible and cheaper than the scan's best, and feasibility continues past 15.0 — so the executed 220 MW current window brackets 14.0 through 15.25 at 0.25 MA, with 14.0 fence-caught. F1 turned the efficiency transect from an optimum hunt into a crossing locator whose values straddle the analytic eta* and are disjoint from the grid's, and added the constant-coupled arm. The executed values per arm are snapshot values under `arms[].window` and are not restated here.

**Two defects in this study's own design surfaced in execution, and both are recorded as findings.** (1) The constant-coupled arm's first anchor held 110 MW coupled, below the 128.64 MW its anchor point requires, so all nine points came back sustainment-blocked and the arm measured nothing; it was re-anchored at 132 MW — the coupled power the search arm's cheapest feasible point actually runs at — and re-executed (§ 15 #6). (2) Its `eta` 0.60 member (132 / 0.60 = 220.0 MW wall-plug) is exactly a search-grid case, and two arms sharing a point silently mis-tagged it, losing one search-arm case; 0.60 is excluded from the couple arm, which cites `c0550` instead, and `proposals()` now raises on any shared point (§ 15 #5). A third defect of a different kind — the four `heat__*` chain channels returning blank — is § 15 #4.

**Validity mask.** The evaluability pre-screen (oracle `p_net` above zero, the `20260829-p-pump-fence` pattern, exception-hardened and routed through the seam's published `evaluate` after critique F9) ran over all 639 proposals and **excluded none** — `results/excluded_points.csv` is empty of rows, as the scan predicted (`net_positive` never fires in 6160 candidates). Kept anyway, because a silent screen is the anti-pattern.

**Arms are tagged at construction**, not inferred from values afterwards (the predecessor's critique MINOR 5), and the pinned baseline is a member of `arm-fence-p100` by construction, not by value-matching (`c0113`, `is_baseline_point` true).

## 12. Cross-fingerprint correlation and what it means

**Within this record: single fingerprint — no cross-arm correlation needed.** All four arms ran from one store against one sealed executable fingerprint `b0c5f3eda9014fa1…`, semantic `48731d1570bb20cd…`, indicator-input pin `2649e0ea2a987f3e…`, all verified against the package at preflight and recorded in `snapshot.json`.

**A semantic boundary crosses between this record and `20260903-priced-levers` (semantic `3cb690aa…`, pin `6262dbf4…`), and it is the boundary this study exists to measure across.** WI-039 retired three entry points (`p_input`, `p_ecrh`, `eta_pin`), minted five (`p_wallplug_heat`, `eta_source_heat`, `eta_couple_heat`, `p_delivered_direct_heat`, `p_coupled_direct_heat`), moved the census 197 → 199, removed the `p_input`/`p_ecrh` tie from the manifest, and changed `sustainment_ok`'s installed operand from a bound design attribute to the chain's computed coupled power. The constraint set is unchanged — the same nine `constraint_id`s on both sides — and every predicate is unchanged except that operand's class.

What the correlation licenses, and what it does not:

- **Licensed, and stronger than the predecessor's § 12 could claim:** the two studies share **36 operating points** — `arm-fence-p100` at eta 0.50 and the predecessor's `arm-fence-p50` at `j_wp` 118.827 coincide on (I, T, n) at I 15.0 / 15.4 / 16 / 17 MA × T 14.63 / 17 / 19 keV × n 1.0 / 1.1 / 1.2× — and at every one of them LCOE, wall load, `p_fus`, beta, heating capital, total capital and all nine verdicts are **identical to every digit** (worst relative deviation 0 over the six channels, no verdict differs; recount from the two `results/points.csv` files). The WI-039 increment is neutral not only at the pinned baseline but at every point the two grids share. The 100 and 220 MW wall-plug levels are therefore exact restatements of the predecessor's 50 and 110 MW coupled levels at eta 0.50, and any number this record quotes at eta 0.50 is directly comparable to the predecessor's at the same (I, T, n, `j_wp`).
- **Not licensed:** feasibility-count comparisons between whole arms. This study's 100 MW grid (I 14–17, T 14.63–22, n 0.9–1.2×, `j_wp` 118.827 only) and its 220 MW grid (I 14.0–15.25, T 14.63–18, n 0.8–1.1×) are different grids from the predecessor's, so "0 of 240" here and "0 of 240" there are the same conclusion on different points, and "91 of 384" is not comparable to "87 of 192".
- **Not licensed:** attributing the 267.159 vs 271.359 optimum difference to WI-039. The two optima sit at different points — this study's at I 14.25 MA, which the predecessor's window did not include, and at `j_wp` 118.827 against the predecessor's 130 — and where the grids coincide the increment moves nothing. The difference is the window, not the model.
- **Licensed with its caveat:** the sustainment-crossing and efficiency-threshold numbers are new quantities the predecessor could not express; they carry the same wall-fence caveat as everything else at these levels.

## 13. Verification

`results/verification_summary.json`. **Outcome: pass.** 1 store, **20 sampled rows** stratified by verdict combination over **11 observed strata** (so the sample cannot miss a produced verdict combination), **13 channels** compared against the package-owned oracle at relative deviation below 1e-9 with **worst observed 5.55e-16** (`c0268`, the headline LCOE channel, 307.0249), and **9 verdicts re-derived** from the oracle's own operands through the package's published bindings rather than compared to themselves — 0 mismatches.

**What verification did not cover, stated as part of the outcome:**

- The `pb__*` power-balance fields, the `sustain__*` sustainment fields, and — new in this record — the four `heat__*` heating-chain fields (`p_delivered`, `p_coupled`, `eta_pin_eff`, `p_wallplug_total`) are fields of multi-field modules and cannot reach the evidence store (ANNEX § Oracle; § 15 #4). They are exported oracle-side in `results/oracle_operands.csv` and are **oracle-derived on both sides**: consistent with the verified verdicts (`sustainment_ok` re-derives from `p_aux_required` against `heat__p_coupled` through the bindings), but not independently verified numbers. Every sustainment-margin, crossing, `rec_frac` and net-electric number in § 6 is in this class.
- `aux_cooling__cryo_cost` and `aux_cost` are oracle-side only, as in the predecessor.
- `p_fus` sits outside generic channel coverage, as in every prior record on this package.
- `verification_summary.json`'s `not_independently_verified` list is **empty although the coverage above is incomplete** — the known tooling gap first filed beside `20260903-priced-levers#4`. An empty list is not proof of full coverage and must not be read as one.
- The tool records `teax.revision` as unrecorded (`20260821-power-cycle-ab#8`); the revision that executed this run, `744745f895677f33…`, is carried in `snapshot.json` from the teax checkout and from the integration return this pin came from.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| **Pre-execution framing critique** (fresh non-author session, 2026-09-03, before any point ran) | **MAJOR** — 4 major (F1–F4), 4 minor (F5, F6, F8, F9), 1 checked clean (F7) | **All nine accepted.** The three MAJOR findings were re-verified against the oracle by the executor before acting. Full text `work/orchestration/goals/wall-and-heating/evidence/T-004_precritique.md`; spawn prompt `T-004_precritique_prompt.md`. F1 deleted the "interior efficiency optimum" (a fence-edge artifact) and added the constant-coupled arm; F2 extended the wall-fence caveat to every 220 MW claim and put T-001's correction bounds into `points.csv` as shadow columns; F3 cut two inflated structural claims back to their true, smaller form; F4 re-bracketed the current window; F5 made the printed-level negative absolute rather than window-limited; F6 replaced a wrong reason for declining `eta_couple_heat` with the right one and disclosed the optimism; F7 checked `j_wp` rather than assuming it; F8 disclosed that three verdict columns carry no information here; F9 routed the pre-screen through the seam's published surface. |
| Correctness | pass | Preflight 6/6; verification pass at worst 5.55e-16 with 9 verdicts re-derived; the pinned baseline reproduces exactly with 9/9 verdicts; 36 operating points shared with the predecessor reproduce to every digit across the WI-039 boundary (§ 12). |
| Honesty | findings, all dispositioned | **Three claims were cut back after checking, before publication**, and the corrected version was smaller and sound each time: (a) "both efficiencies and the wall-plug power now reach `sustainment_ok`" — the pre-change `p_input+tie` already reached it; the one new reach is efficiency → `sustainment_ok` (§ 8); (b) "there is an interior efficiency optimum" — there is not (§ 6); (c) "efficiency paying at constant coupled power is new to WI-039" — it is not; what is new is that the fixed-wall-plug experiment became expressible (§ 6). Two defects in the executor's own design surfaced in execution and are recorded as findings rather than repaired silently (§ 15 #5, #6). |
| Readability | pass | Every number in §§ 3–6 and § 12 traces to `results/points.csv`, `results/oracle_operands.csv`, `results/window_scan.json`, `results/baseline_result.json` or `results/verification_summary.json`, or is arithmetic on them shown in place; the one exception, the `j_wp` probe in § 8, cites the critique file by path. |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `20260903-wall-and-heating#n`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260903-wall-and-heating#1` | `model` | **At the printed heating level nothing is feasible, and the negative is absolute in source efficiency.** 100 MW wall-plug (50 MW coupled at 0.50, `eta_couple` 1.00): 0 of 240. Among the 36 points blocked by `sustainment_ok` alone the minimum required coupled power is 87.061 MW (`c0036`: I 15.4 MA, T 17 keV, n 0.9×), so the level opens only at `eta_source_heat` ≥ 0.871 at the most optimistic coupling; the other 204 blocked points also fail the wall or the conductor ceiling, which no efficiency touches. The scan put the threshold at 0.92 on its coarser grid; the executed grid governs. | first-order fence-anatomy reading, pre-registered as such by the scan; every wall verdict at this level is the fence as bound | goal `wall-and-heating` round result; the wall half, `goal.md` § Answered when (b) |
| `20260903-wall-and-heating#2` | `model` | **Whether source efficiency pays depends entirely on which quantity is held.** At fixed 220 MW wall-plug LCOE rises monotonically with efficiency (269.823 → 273.675 over 0.35 → 0.65; heating capital 406.8 → 755.5 M$ linear; wall-plug draw constant) and efficiency buys only feasibility, at the sustainment crossing eta* = 0.5238. At fixed 132 MW coupled it falls 317.234 → 255.970 over 0.35 → 0.75 (61.264 $/MWh; heating capital constant at 697.3 M$; `rec_frac` 0.4499 → 0.3096). Fusion performance is bit-identical across efficiency in all 96 (I, T, n) cells. | disclosed with the newness claim cut back: the fixed-wall-plug experiment is new (wall-plug power was not a quantity before WI-039); the falling constant-coupled curve is not (the pre-change model produced the same sign) | goal round result; Row-4 re-grade evidence, `goal.md` § Answered when (a) |
| `20260903-wall-and-heating#3` | `model` | **Every economic result at 220 MW is set by the wall fence as bound.** At fixed (T, n) LCOE rises with current, and it falls with density and with temperature until the wall stops it; the constrained optimum (267.159, `c0550`) sits at wall load 4.004 against 4.05, 98.9% of the limit. Under T-001's low correction bound (1.15× on the circular-torus average) it reads 4.604, violated; 51 of 91 feasible search-arm points survive that bound, 0 survive the high bound (1.83×); the cheapest survivor is 326.201 (`c0546`: I 14.25 MA, T 14.63 keV, n 1.0×, eta 0.60). | carried as data — `wall_load_shadow_lo/hi`, `wall_load_ok_shadow_lo/hi`, `feasible_shadow_lo` in `results/points.csv` — never as prose only; the honest fence's form, its area basis and the 0.10 m standoff transfer are round 2's to decide on T-001's sources | goal `wall-and-heating` round 2 (the wall half); `goal.md` § Answered when (b) |
| `20260903-wall-and-heating#4` | `process` | **All four `heat__*` chain channels came back blank in all 639 rows on the first execution.** 'Heating Power Chain' has four outputs, so it is a multi-field module exactly like `pb__*` and `sustain__*`, and the evidence store records only single-field float channels; the store accepted the declaration and emitted blank columns with no gate. Fourth committed sighting of the class (`20260821-power-cycle-ab#5`, `20260901-sustainment-fence#3`, `20260903-priced-levers#4`), third of the silent-blank-column mode. | the four channels were removed from the store declaration and exported oracle-side in `results/oracle_operands.csv`, labelled as such, and the study re-executed; no blank left, no value invented | documented seam, `ANNEX.md` § Oracle (now naming `heat__*`); joins `20260903-priced-levers#4` and its proposed declaration-time channel-shape guard |
| `20260903-wall-and-heating#5` | `process` | **Two arms silently shared a point on the first execution.** The constant-coupled arm's eta 0.60 member (132 / 0.60 = 220.0 MW wall-plug) is exactly a search-grid case; arm tagging keys on the input tuple, so the shared point took whichever arm was appended last and one search-arm case was lost — caught by counting rows per arm, not by any gate. Same class as the predecessor's value-matching mis-tag. | eta 0.60 excluded from the couple arm, whose curve cites `c0550` for that point; `proposals()` now raises on any point two arms share | study definition convention (`study.py` beside each record): a definition asserts no two arms share a point |
| `20260903-wall-and-heating#6` | `process` | **The constant-coupled arm's first anchor held 110 MW coupled, below the 128.64 MW its anchor point requires**, so all nine points came back sustainment-blocked and the arm measured nothing. A transect anchored at "the search arm's cheapest feasible point" must carry that point's own coupled power (132 MW), not the level the arm was named for. | re-anchored at 132 MW coupled and re-executed; disclosed in `study.py` and § 11 | runbook step 7, executor practice: a transect's held level is read off its anchor's own operands, never assumed from the arm's name |
| `20260903-wall-and-heating#7` | `model` | **`j_wp` is inert in this window.** Probed 95–145 A/mm² at the search arm's best point by the pre-execution critique: a 53% swing moves LCOE by 0.08 $/MWh (0.03%) and moves B_peak, `p_aux_required` and wall load not at all, including at a field-blocked current. WI-036 priced the winding pack and the current density still reaches almost no cost. Re-sighting of `20260903-priced-levers#2` at the WI-039 pin. | declined axis, held at 118.827 and asserted per case in `export()`; no new work routed | WI-040, the standing route from `20260903-priced-levers#2` (`work/BACKLOG.md`) |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `547958abbe772a4b3762013c058dab8e4366762a6fd234b8d4ecb136d498e73e`
- **Schema version:** `1`

No snapshot content is restated here. It carries the three package fingerprints and the sealed executable fingerprint; the manifest digest with the tie, baseline, objective catalog and oracle content actually used, the oracle's own source digest included; the one store's complete compatibility tuple; per-arm windows with their `engineered` provenance, evaluated and feasible counts, the shadow-column survivor counts, and the verification values; digests for all eight `results/` artifacts plus `indicators.json`, `pre_wi039_indicators.json`, `axes.json`, `study.py` and `scan.py`; the three tools' source digests; the preflight outcome; the counts (639 proposed, 639 evaluated, 0 excluded, 103 feasible — 91 in `arm-search-p220`, 8 in `arm-couple-132`, 4 in `arm-transect-eta`, **0 in `arm-fence-p100`**; 51 survive the low wall shadow, 0 the high); and the teax revision. **The per-point store is uncommitted** (`_work/`, gitignored by the studies convention); every value this record cites is in `results/points.csv` or `results/oracle_operands.csv`, both digested.

## 17. What this record does not contain

- **No geometry claim.** `R` and `a` were declined (§ 8). Every wall-load number is about this machine at R 12.7 m, a 1.3 m; wall area scales with machine size and this study did not sweep it. That is round 2's question and this record does not answer it.
- **No claim about the honest wall fence.** The shadow columns apply T-001's two correction bounds (net 1.15× and 1.83×) to the current operand as data; they are bounds from sources, not a chosen form, an area basis, or a standoff transfer. Choosing those is round 2's model task.
- **No `eta_couple_heat` sensitivity.** It is degenerate with the source efficiency in the fence and was held at 1.00, the optimistic end. Every feasibility claim here is made at the most generous possible coupling.
- **No buildability claim about gyrotron efficiency.** The threshold 0.871 is stated against the pinned source's 0.50; no source in the repository bounds what is achievable, and the couple arm's 0.65–0.75 points show the curve's shape, not a claim that such sources exist.
- **No boundary in installed power.** Two levels and one reciprocal transect; the sustainment flip in coupled power stands where `20260901-sustainment-fence` committed it.
- **No claim that the constant-coupled economics are new to WI-039, and no matched pre-change comparison of them.** The pre-change oracle produced a falling curve of the same sign from a scratch worktree; its numbers were not confirmed at an identical operating point and are not quoted.
- **No priced conductor option.** `B_max` was held (§ 8); every statement at the ceiling is a statement about where that literal is set.
- **No feasibility-count comparison across the WI-039 boundary** (§ 12): the grids differ. The 36-point identity is a comparison at shared points and licenses nothing about the arms as wholes.
- **No statement about T_i0 above 22 keV at 100 MW or above 18 keV at 220 MW, below 14.63 keV at either, about densities outside 0.9–1.2× (100 MW) or 0.8–1.1× (220 MW), or about currents outside 14–17 MA (100 MW) or 14.0–15.25 MA (220 MW).** The windows are engineered and the structure inside them is not a claim about the frame's rightness. The top of the 220 MW current window is not fence-caught inside the executed points (§ 6 `I_coil`).
- **No independent verification of the power-balance, sustainment, heating-chain or cryo-cost quantities** (§ 13) — oracle-derived on both sides.
- **The teax revision that executed this run** is `744745f895677f3344b9884627369a6a47ed987f`, from the teax checkout and the integration return; `results/verification_summary.json` records it as unrecorded, the gap every record on this package carries.
- **A stale sentence in `study.py`.** The docstring of `export_oracle_operands` says the `heat__*` channels "are single-field and do appear in the store, so they are in `points.csv` where they belong". That was the first execution's belief and it is wrong; the `CHANNELS` comment in the same file and § 15 #4 carry the correct account, and the four values are in `oracle_operands.csv`. `study.py` is left as digested and executed rather than edited after the fact (`20260821-power-cycle-ab#9` precedent).
- **The critique's F4 probe reported the 14.0 MA point as "wall-blocked"**; the executed data shows every 14.0 MA point sustainment-blocked, 28 of them also wall-blocked. The executed verdicts govern; the probe's reading was incomplete, not wrong about the wall.
- **`results/_work/`** is the baseline executor's gitignored working directory, not evidence, and is correctly absent from the snapshot's artifact list.
