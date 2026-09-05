# W counterfactual — the model's stored thermal energy forced to the printed 504.65 MJ

**Date:** 2026-09-04 · **Goal:** `stored-energy-basis`, run as **grounding evidence** (the goal was drafted owner-absent, a draft goal authorizes no task, and `GOAL_RUNBOOK.md` § Grounding a goal exists to stop a run spending a round on a question the repository can already answer) · **Scripts and raw outputs in this directory.**

**Every number here is oracle-side, not package evidence.** The model was driven through its package-owned oracle (`exploration/stellarator_e2e/verify_stellaris.py` via `studies/oracle_entry.py`) and the paper's own closure through the operating-point prototype; nothing under `models/`, `exploration/stellarator_e2e/generated/` or `exploration/stellarator_e2e/studies/manifest.json` was written, no file on disk was edited, and the pin stays `c1b0f0d1…`. W is not tuned anywhere; it is forced in a copy of one function's source, in memory, for this diagnostic only.

## 1. What was asked

Does the pinned baseline's `sustainment_ok` violation (90.6 MW required against 50 MW coupled) and the committed "no feasible driven point at the printed 100 MW wall-plug on the design geometry" result survive when the model's stored thermal energy W is set to the paper's printed 504.65 MJ instead of its own 551.4 MJ? And if not, what in the profile integral produces the +9.2 %? (Handoff `../handoff_20260904-170919.md` § Focus; the owner's ask, relayed.)

## 2. The printed values, read from the pages (not the extraction)

| Quantity | Printed | Where |
|---|---|---|
| Total plasma energy, point A | **504.65 MJ** | Table 5, raw PDF p. 10; image `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/images/page_009_table_0.png` |
| Vol. av. beta | 2.76 % | Table 5 |
| Vol. av. electron density | 3.17 × 10²⁰ m⁻³ | Table 5 |
| Peak n_e / n_D / n_T / n_He | 5.06 / 1.96 / 1.96 / 0.56 × 10²⁰ | Table 5 |
| Peak T_e / T_i | 15.40 / 14.63 keV | Table 5 |
| Confinement time | 1.46 s | Table 5 |
| Fusion power; fusion gain; aux power at the operating point | 2700 MW; ∞; 0 MW | Table 5 |
| Av. photon wall power × plasma surface | 0.70 MW/m² × 327 m² = 228.9 MW | Table 5 (the prototype's "228.9 MW photon") |
| Plasma volume | 425 m³ (Table 5); 428 (Table 2) | Table 5; Table 2 image `page_002_table_0.png` |
| Alpha slowing-down time; τ*/τ_E | 43.76 ms; 8.00 | Table 5 |
| Profile parametrization | T_e = T_e0 (1 − ρ²)^α_T (Eq. 2); n_i = n_i0 (1 − ρ²)^α_n (Eq. 3) | raw PDF p. 8, § 2.3 |
| Exponents the paper states for point A | α_T = 1.2 (Eq. 2, T_e), α_n = 0.35 (Eq. 3, the ion density); the plotted electron curve is more peaked and the helium curve much more so | Fig. 16 and its caption, raw PDF p. 10 |
| Balance and closure | A.3: p_rad + w/τ_E = f_α E_α n_D n_T⟨σv⟩ + p_aux; A.7 ISS04 with "P = W/τ_E, where W is the stored plasma energy"; τ*_α = ρ* τ_E, ρ* ~ 8; f_suppr = ½ | raw PDF p. 32, Appendix A |

The raw PDF is `…/tmpissrtbos/raw.pdf` (R2-synced, gitignored). Pages were rendered with pymupdf and read; the page images above are the extraction's own.

**Extraction hazard, recorded.** The extracted text (`…/tmpissrtbos/output.md`) rewrites the Fig. 16 caption as "Eq. (1) for α_n = 1.2 and α_T = 3.0" and its Table 5 carries phantom rows (peak T density 2.96, total heating power 37.0, confinement time 0.99). The page reads Eq. (3), α_T = 1.2, α_n = 0.35, and none of those rows. Every value in this note was read from the page.

## 3. Basis A — the model as implemented, W scaled by a constant (`w_counterfactual.py`)

**Method.** `_sustainment()` in `verify_stellaris.py` computes `W_th = 1.5 * p_avg * V * 1e-6` inside its inner `state()`, which the ash fixed-point loop calls, so the override has to live there. The function's source is read with `inspect`, that one line is replaced by the same line times `W_SCALE` (the script asserts the line occurs exactly once), the result is compiled into the oracle module's namespace and bound as `vs._sustainment`. `oracle_entry.evaluate()` then runs the oracle unchanged except for that factor. `W_SCALE = 504.65 / W_th(baseline, unmodified) = 0.915142`. Bounds and the nine predicates are read exactly as the committed study's scan read them (`generated/inputs/*.json`; `mfe_viability.sysml`).

**Parity.** Sixty committed points re-evaluated unmodified reproduce the record's verdicts, `p_aux_required` to 10⁻⁶ MW and LCOE to 10⁻⁹ relative — zero mismatches (`w_counterfactual.py parity 60`). The point construction is the record's.

**At the reference point** (`baseline_counterfactual.json`; pinned baseline `c2973`):

| | unmodified | W forced (× 0.915142) | printed |
|---|---|---|---|
| W_th | 551.444 MJ | **501.667 MJ** | 504.65 |
| τ_E | 1.4499 s | 1.6811 s | 1.46 |
| W/τ_E (conducted loss) | 380.33 MW | 298.41 MW | 345.7 (printed pair) |
| p_rad | 228.61 MW | 228.61 MW | 228.9 |
| n_He0 | 5.781 × 10¹⁹ | 6.331 × 10¹⁹ | 5.6 × 10¹⁹ |
| p_fus | 2725.4 MW | 2574.0 MW | 2700 |
| f_α × ash_frac × p_fus | 518.34 MW | 489.55 MW | 513.5 |
| **p_aux_required** | **90.60 MW** | **37.47 MW** | 0 (ignited) |
| `sustainment_ok` (50 MW coupled) | violated | **satisfied** | — |
| wall-load peak | 4.088 | 3.861 | 4.05 limit |
| `wall_load_ok` | violated | **satisfied** | — |
| β | 0.02684 | 0.02668 | 0.0276 |
| LCOE | 313.513 | 332.585 | — |

**Neither baseline violation survives.** Under the forced W every one of the nine verdicts is satisfied: the pinned baseline would be feasible and driven, at an LCOE 6.1 % higher.

**Mechanism, so the reader can see what moved.** W enters the closure twice: the closed-form ISS04 τ_E goes as W^−1.564 and the conducted loss W/τ_E as W^2.564, so a 8.5 % cut in W cuts the loss by 82 MW (380 → 298). But the longer τ_E (+16 %) raises the ash fixed point (n_He0 +9.5 %, now 13 % above the printed value), dilutes the fuel, and drops p_fus 5.6 % (now 4.7 % below the printed 2700), which takes 29 MW off the alpha heating. Net: the requirement falls 53 MW, from 90.6 to 37.5. The wall flip is entirely the p_fus fall. **The forced state buys energy fidelity with fusion-power and ash fidelity; it is not "closer to the paper" on every printed row.** The realized W is 501.7 MJ, not 504.65, because the ash re-closes after the scale is applied; across the window the realized ratio is 0.908–0.913 against the 0.915 scale.

**Two readings that do not flip the verdict.** (i) Holding τ_E at the printed 1.46 s with W at 504.65 (the printed pair, no re-closure): p_aux_required = 228.6 + 345.7 − 518.3 = 56.0 MW — still violated at 50. (ii) The printed table through the paper's own A.3 at zero auxiliary power, with f_α = 0.95 and ash_frac 0.2002: 513.5 − 228.9 − 345.7 = **−61.0 MW**. The paper's printed W, τ_E, radiation and fusion power do not close the paper's own balance at the ignition it prints; the τ_E that would balance the printed W is 1.773 s (`attribution_arithmetic.py`). So the verdict flip in the table above depends on letting the closed form raise τ_E with the lower W. It is the model's closure applied to the printed W, not the paper's printed state.

## 4. Basis B — the paper's own closure, the operating-point prototype (`op_solve_w_counterfactual.py`)

`work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/op_solve_final.py` loaded as source, its two `W=1.5*p*V*1e-6` statements patched the same way, its top-level runs dropped (`op_solve_counterfactual.json`, `op_solve_counterfactual_output.txt`):

| | unmodified | W forced |
|---|---|---|
| W | 551.327 MJ | 501.668 MJ |
| τ_E | 1.4578 s | 1.6898 s |
| residual g at p_aux = 0 | **−89.55 MW** | **−37.00 MW** |
| burn attractor at point-A levers, p_aux 0 / 50 | none / none | T = 23.1 keV, p_fus 6328, wall-proxy 7.21, β 4.2 % / T = 25.0, 7241, 8.25, 4.6 % |

Agrees with Basis A to 0.5 MW (quadrature N = 400 vs 200,000; R 12.74 vs 12.7). The prototype's finding 3 stands under the forced W: a burn attractor now exists at the design levers, but at 6.3–7.2 GW of fusion power it breaks the wall limit by 78–104 %. The forced W makes the printed point a *driven* equilibrium 37 MW short of ignition; it does not make it the ignited point the paper prints.

## 5. The committed window, re-evaluated point by point (`window_counterfactual.csv`, `window_summary.json`)

Every one of the 6,311 evaluated points of `exploration/stellarator_e2e/studies/20260904-wall-and-heating/results/points.csv` (record dir at `a5b0b96a`) re-evaluated through the oracle with the same constant scale; each verdict compared with the record's column. **61 points fail the closure's validity edge under the forced W** (28 at 100 MW, 33 at 220: non-positive fuel or a complex value — the record's § 15 #8 edge, reached by more points because the longer τ_E drives more ash); none of the 61 was feasible or ignited in the record. Field, stress and strain verdicts do not move (the field chain does not read W).

**Verdict flips against the record (6,250 points):**

| Verdict | record → forced | count | of which at 100 MW / 220 search / 220 re-read |
|---|---|---|---|
| `sustainment_ok` | violated → satisfied | **1,128** | 573 / 367 / 188 |
| `sustainment_ok` | satisfied → violated | 21 | 11 / 10 / 0 (ash dilution outweighs the loss cut) |
| `wall_load_ok` | violated → satisfied | **384** | 180 / 179 / 25 (p_fus falls with the dilution) |
| `recirc_ok` | satisfied → violated | 211 | 68 / 118 / 25 (p_net falls with p_fus) |
| `beta_ok` | violated → satisfied | 20 | 10 / 10 / 0 |

**Counts per arm, feasible / ignited / feasible-driven** (the record's definitions: feasible = all nine satisfied; ignited = `p_aux_required` < 0; driven = feasible and not ignited):

| Arm | record | W forced |
|---|---|---|
| `arm-fence-p100` (100 MW) | 458 / 787 / **257** | 776 / 1,282 / **332** |
| `arm-search-p220` | 598 / 787 / 400 | 793 / 1,282 / 390 |
| `arm-reread-p220` (round 1's points) | 24 / 0 / 24 | 58 / 51 / 58 |
| `arm-transect-ash` | 0 / 8 / 0 | 0 / 9 / 0 |

**What moves at the printed 100 MW, against the record's headline (§ 3, § 15 #1):**

- **The design geometry opens.** The record: no feasible driven point at R 12.7, a 1.3 anywhere in the window; the only feasible driven `a` on the design column is 1.7 m (257.35). Forced: **six driven points at R 12.7, a 1.3**, cheapest 315.09 $/MWh (`c0625`: I 15 MA, T 16 keV, n 0.9×; 31.4 MW required; peak 4.012 against 4.05), and the pinned baseline `c2973` itself feasible and driven at 332.585 (37.5 MW; peak 3.861). The a = 1.7 column point `c0821` stays driven at 275.88 (record 257.35).
- **The cheapest driven point barely moves and is a different point.** Record 212.460 (`c1721`: R 14.2, a 2.2, I 15 MA, T 16 keV, n 0.9×). Forced 212.314 (`c1676`: R 14.2, a 2.2, I 13 MA, T 14.63, n 0.9×; 40.0 MW required; peak 3.716). `c1721` itself reads 226.51 under the forced W (still driven, 5.9 MW required).
- **347 of the record's driven points lose driven status**: 305 ignite (the one-sided fence, § 15 #4, then passes them), 40 fail `recirc_ok`, 2 fail `sustainment_ok`. The ignited set grows from 787 to 1,282 per level. The "driven" reading the record makes every claim on is the most W-sensitive set in the study.
- **At 220 MW** the cheapest driven point moves 219.45 → 229.71 (`c4660`); round 1's re-read points go 24 → 58 driven, all at the design geometry, cheapest 371.70 (record 378.556).
- **The ash transect (§ 15 #2) shifts but keeps its shape:** on the design column τ*/τ_E = 6 goes from +44.4 MW required (driven, wall 4.54 violated) to −12.2 (ignited, wall 4.33 violated); at 12, 158.4 → 109.0 MW; nothing on the transect is feasible in either state. The knife-edge is still a knife-edge; its location depends on W.
- **R's effect (§ 15 #7)** was not re-measured here; the field fences are unchanged and the wall peak still rises with R.

## 6. What the constant scale assumes, and what it cannot say

- A constant factor treats the profile-shape error as multiplicative and geometry-independent. The *sign* of every move above is robust — the conducted loss is the largest single term in the balance and W enters it as W^2.564 — but the *location* of any boundary (which points flip) is not a claim; it is what one particular counterfactual does.
- It holds the printed W as the target and lets everything downstream re-close. § 3 shows a different reading (printed W with printed τ_E) leaves the baseline violated at 56 MW, and that the paper's printed row does not close its own balance. Which state is "the paper's" is not decidable from the paper.
- It says nothing about whether 504.65 MJ is the right target. § 7 says it is probably not.

## 7. Attribution, first pass — what the printed values give under the profile family (`attribution_arithmetic.py`)

Arithmetic only, on the printed peaks and the exponent sets in play (the model's; the caption's; the WI-022 digitization, refit from its dumped curves; a helium exponent read by eye and bracketed); the oracle's own `_profile_integral` for the fusion power; nothing fitted to the printed energy.

| Exponents (electrons / ions / T) on the printed peaks, V = 425 | W | vs printed 504.65 | p_fus | vs printed 2700 |
|---|---|---|---|---|
| **the model's** 0.596 / 0.33 / 1.19 | 551.33 MJ | +9.3 % | 2748 MW | +1.8 % |
| the caption's exponents on **every** species 0.35 / 0.35 / 1.2 (a naive reading; see 2) | 574.65 MJ | +13.9 % | 2710 MW | +0.4 % |
| the model's, with the ions at the electron exponent 0.596 / 0.596 / 1.19 | 525.97 MJ | +4.2 % | 2472 MW | −8.5 % |
| **figure-consistent**: fuel 0.33, helium peaked (α_He 1 / 2 / 3, read by eye), electrons by quasi-neutrality, T 1.19 | 558.6 / **539.1** / 527.2 MJ | +10.7 / **+6.8** / +4.5 % | 2748 MW | +1.8 % |
| exponent sum (α_n + α_T) the printed W needs, one shape | 1.904 | — | — | — (the paper's is 1.55) |

1. **Every reading reproduces the printed fusion power; none reproduces the printed energy.** The caption's exponents on every species give 575 MJ (+13.9 %) and ⟨n_e⟩ = 3.75 against the printed 3.17; the model's family 551 (+9.3 %); a figure-consistent family 527–559 (+4.5 to +10.7 %). The printed W is not derivable from the paper's plotted profiles and printed peaks under the paper's own parametrization.
2. **The model's exponents are a fair read of the figure.** The WI-022 digitization (`work/completed/20260718_WI-022_predictive-confinement/prototype/fig16_curves.json`, refit here by the same through-origin log fit to ρ ≤ 0.85: electrons 0.617, D 0.331, T 0.327, the three temperatures 1.19; no helium points were dumped) finds the electron curve more peaked than the fuel curves, as quasi-neutrality with a peaked helium curve requires — Fig. 16(a) shows the ash falling to near zero by ρ ≈ 0.8. The caption's α_n = 0.35 is the ion density's (Eq. 3); the every-species row above is a naive reading the figure itself contradicts. What the model's family gets wrong is the **ash**: it gives helium the fuel's exponent (`stellarator_plant.sysml:578`, used for n_He in the pressure integral), so its ion charge density exceeds n_e off-axis — 7.5 % at ρ = 0.5, 31 % at 0.8, 55 % at 0.9 (`attribution_arithmetic.json`). A figure-consistent family — fuel 0.33, helium peaked (α_He ≈ 2 by eye, bracketed 1–3), electrons by quasi-neutrality, T 1.19 — gives 539 MJ at α_He = 2 (⟨n_e⟩ 3.32, effective α_n_e 0.52) and 527–559 across the bracket.
3. **No reading of the plotted profiles with the printed peaks reaches 504.65.** Forcing the fuel to the electron exponent (526 MJ) costs 8.5 % of fusion power; the exponent sum the printed W needs on one shape is 1.90 against the fuel's 1.52 and the electrons' 1.81.
4. **The printed β disagrees with the printed W.** β = 2.76 % at B_0 = 9.0 T over 425 m³ implies ⟨p⟩ = 889,500 Pa and W = 567 MJ (+12.4 % over 504.65); the two printed numbers agree only if β is referenced to a field of 8.49 T. The model's β (2.683 %, computed from the same ⟨p⟩ as its W, at 9.0 T) is 2.8 % *under* the printed β while its W is 9.2 % *over* the printed W.
5. **Fast alphas do not bridge it:** P_α × τ_sd / 2 ≈ 12 MJ, 2.3 % of the printed W, whichever way "Total" is read.
6. **What remains unknown and is a research question, not a model one:** the paper's definition of its volume average and of β's reference field; what its 0.5-D code integrated for "Total plasma energy" (a different profile than Fig. 16, or a different volume element); which n19 entered its ISS04 (the model's τ_E match at −0.1 % rests on the same α_n_e = 0.596, and reading n19 at 0.35 or at 3.17 moves the implied W anywhere from 463 to 599 MJ).

**Reading.** The +9.2 % decomposes as about two points between the model's family and a figure-consistent one (551 → 539: the ash shape), and about seven points between that and the printed value, which no reading of the paper's plotted profiles and printed peaks reaches. The model's exponents are not a digitization slip, and on the source's own arithmetic the +9.2 % is not a W-form error against a sound target: the printed 504.65 MJ is the odd one out among the printed fusion power, the printed β and the plotted profiles. **L-001's premise — the W-form is the model's fidelity gap and the printed W is the target — is not supported by the source.** Surfaced here, with the dependent conclusions (§ 3, § 5) labelled as conditional on that target; not resolved.

## 8. What this does to the inherited readings (for the owner)

- `work/orchestration/goals/priced-levers/goal.md:52` and `wall-and-heating/goal.md:52` carry "the violated baseline `sustainment_ok` is … the model's own analytic W-form, +9.2 % at the printed point, never tuned." Confirmed in one half — the verdict is W-sensitive and flips at the printed value — and undercut in the other: the +9.2 % is not an error against a sound printed target (§ 7). Whether the verdict is "a disclosed fidelity fact" or "a reading of an inconsistent source" is the owner's to rule; nothing here tunes anything.
- `20260904-wall-and-heating` § 15 #1 (the design geometry closed at 100 MW), #2 (the knife-edge), #4 (787 ignited), #6 (round 1's 26 survivors) all move under the forced W; #7 stands. The round-2 C-001.r2 dispositions are written on the record's readings.
- WI-041's baseline `wall_load_ok` violation (4.088) also flips under the forced W, through p_fus, not through the fence.
- The prototype's findings 1–3 (`T-002_prototype/NOTES.md`) stand in form — the printed point is still not a self-sustained equilibrium of this closure at any reading of W, and the burn attractor still breaks the wall — with the shortfall 37 MW instead of 90 at the printed W.

## 9. Files

- `w_counterfactual.py` — Basis A; modes `baseline`, `parity N`, `window [workers]`. Run from the worktree with the primary checkout's interpreter (`docs/integration_seam_operator_guide.md` § Running from a second checkout): `/home/reid/1cfe/fusion-tea/.venv/bin/python w_counterfactual.py window 10` (about seven minutes on ten workers).
- `baseline_counterfactual.json` — § 3 numbers. `window_counterfactual.csv` (6,311 rows: record verdicts beside forced verdicts, forced operands), `window_summary.json`, `window_output.txt` — § 5.
- `op_solve_w_counterfactual.py`, `op_solve_counterfactual.json`, `op_solve_counterfactual_output.txt` — § 4.
- `attribution_arithmetic.py`, `attribution_arithmetic.json`, `attribution_arithmetic_output.txt` — § 7.
- `../handoff_20260904-170919.md` — the owner's ask as relayed by the previous session.
