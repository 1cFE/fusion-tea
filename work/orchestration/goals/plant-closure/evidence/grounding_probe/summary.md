# Grounding probe — goal `plant-closure` — 2026-09-08

An oracle-side diagnostic at the WI-044 pin (`30abb21be6d7…`), computed by `probe_design_point.py` on `exploration/stellarator_e2e/verify_stellaris.py`'s `compute()` with the three held multipliers overridden by what the candidate closures would produce at the design point. **Never package evidence.** Every number is a prediction to be tested by the model items and the round's study, not a target; the sourced shapes and their anchors are stated so a reviewer can re-derive each line. Results in `probe_results.json`.

## What was computed

**(i) The primary loop.** The Moscato 2017 reference circuit (`knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md` lines 79–81, 89–91, Table 1 at 105–113, Table 2 at 128, Table 3 at 151–154; raw PDF pp. 6–7, renders `../grounding_sources/moscato_p6_tables2_3.png`, `moscato_p7_table4.png`): helium at 8 MPa, 300 → 500 °C, 2101.7 MW blanket heat at 2025.7 kg/s over 9 loops; per-path losses IB 214 + 62 + 87.9 = 363.9 kPa and OB 174 + 56.6 + 85.1 = 315.7 kPa (Table 3's kPa basis; Table 2's "MPa" label for the IHX row is the source's own inconsistency); IHX duty 3 × 208.1 + 6 × 267.8 = 2231.1 MW; printed circulator power 3 × 2 × 6.8 + 6 × 2 × 7.5 = 130.8 MW. Transferred as a **representative circuit**: the loop count sized at the design point so the per-loop flow does not exceed the reference's (integer, held in the instance afterwards), constant loss coefficients per component (`dp ∝ (mdot_loop / mdot_loop_ref)²` at the same nominal density), an isentropic compressor from the pressure ratio `r = p2 / (p2 − dp)` with the blanket inlet held at 300 °C, ideal-gas helium (`cp` 5193 J/(kg K), γ 5/3).

**(ii) The cycle.** Kovari et al. 2016 Table 4 (`../grounding_sources/kovari2016_p9_table4.png`, read this session): helium-primary steam Rankine `η = 0.1802 ln(T2 + 273) − 0.7823 − Δη`, T2 the secondary-side turbine-inlet temperature, valid 384–642 °C, primary–secondary approach 20 °C, the divertor correction Δη separate; supercritical CO2 `η = 0.4347 ln(T2 + 273) − 2.5043`, 135–750 °C. Evaluated at T2 = 500 − 20 = 480 °C with Δη = 0 (no low-temperature divertor loop in the model).

**(iii) The calendar.** A deterministic finite horizon (30 yr) with one bundled first-wall/blanket/divertor event: physical life `L = fluence_limit / q_peak` = 18 / 3.978845 = **4.524 FPY**; the outage `d` = 7/12 yr (Stellaris §2.11, `../grounding_sources/stellaris_p29_maintenance.png`: "a completion time of seven months is estimated"; the five-month window and the 90 % availability are targets on the same page); a residual unplanned fraction `u` of scheduled-online time with no admissible source, run at 0, 0.05 and 0.10; a replacement is bought only if restart falls strictly before the horizon; availability `A = F / N` with `F` the productive FPY.

## What it predicts at the design point

| Quantity | Held (pin `30abb21b…`) | Candidate closure | Note |
|---|---|---|---|
| Reactor source heat `Q_b = mn·p_n + p_α + p_coupled` | 3126.85 MW (inside `p_th` 3224.35 with the 97.5 MW pump credit) | same | no pump credit in `Q_b` |
| Loop flow | — | 3010.6 kg/s | `Q_b / (cp · 200 K)`; the source's implied `cp` is 5187.6 |
| Loop count | — | 14 (per-loop 215.0 kg/s vs the reference's 225.1) | sized at the design point, then held |
| Per-path pressure loss | — | 300.5 kPa | flow-weighted reference 329.2 kPa × (215.0 / 225.1)² |
| Compressor isentropic efficiency | — | 0.777 | derived at the reference from the source's own energy check (IHX 2231.1 − 2101.7 = 129.4 MW fluid work ⇒ ΔT 12.30 K against the isentropic 9.55 K) — a source-point calibration, labelled; not also a validation |
| Circulator fluid work = loop electrical | `p_pump` 195.0 MW, `eta_p` 0.5 | **174.6 MW**, 5.58 % of `Q_b` | the source's printed boundary (130.8 printed ≈ 129.4 fluid); electrical ≥ fluid work, so a lower bound on the draw — disclosed, the WI-033 pattern |
| Thermal power to conversion | 3224.35 MW | **3301.45 MW** (`Q_b` + fluid work, all of it recovered) | the source's IHX residual supports full recovery of fluid work |
| Cycle efficiency | 0.333 | **0.41136** (Rankine, He primary, 480 °C) — sCO2 would read 0.37518 | inside the 384–642 °C domain |
| Gross electric | 1073.71 MW | 1358.07 MW (all three) | |
| Net electric | 716.63 MW | 1012.87 MW (all three) | `rec_frac` 0.3326 → 0.2542 |
| First-wall life | 4.524 FPY → calendar 5.32 yr at A 0.85; `n_rep` 5 | 4.524 FPY; events at 4.52 / 9.63 / 14.74 / 19.85 / 24.95 yr; **5 replacements** | same count as the held chain at `u` 0 |
| Availability | 0.85 held | **0.9028** at `u` 0; 0.8576 at 0.05; 0.8125 at 0.10 | at five months: 0.9167 (**six** replacements fit before the horizon), 0.884, 0.8375 — the integer step is live |
| CAS72 | 126.65 M$/yr | 134.89 M$/yr (all three, `u` 0) | dated events, the replacement cost per event moved by the cycle's gross power through the divertor account |

**LCOE at the design point, one closure at a time (oracle, $/MWh):**

| Arm | LCOE | Move |
|---|---|---|
| held, the pin | 322.3184 | — |
| loop only (174.6 MW, fluid work fully recovered) | 305.5832 | −5.2 % |
| cycle only (0.41136) | 247.7050 | −23.1 % |
| calendar only, `u` 0 (A 0.9028) | 304.6095 | −5.5 % |
| calendar only, `u` 0.05 (A 0.8576) | 319.6245 | −0.8 % |
| all three, `u` 0 | **224.0805** | −30.5 % |
| all three, `u` 0.05 | 235.1446 | −27.0 % |

## Reading

1. **Every closure moves the design point, and each move is attributable.** Unlike the last four goals, this one will not land with "no number moves": replacing three held multipliers by computed producers changes the headline by roughly a third, most of it the cycle. The goal therefore needs the compatibility bridge stated up front — a form in which each new chain can be set to reproduce the held value exactly, so the pinned baseline is reproduced bit-for-bit in the same package and every $/MWh of the move is assigned to one closure (this table, executed in-package).
2. **The loop's number lands near the held one for a reason the model can now state**: 5.6 % of source heat inside DI-008's 4–6 % helium-primary band, from a stated circuit with a stated loop count, not a fraction. Off the design point it responds as `mdot³ / N²` at fixed loop count (a hydraulic law), which is exactly what the owner's 2026-08-28 ruling said a fraction of `p_th` could not assert.
3. **The cycle's move is the largest and rests on the thinnest transfer**: the Stellaris paper models a local first-wall segment at 350 °C inlet / under 370 °C outlet and names no cycle; the 300 → 500 °C window and the 480 °C turbine inlet are the EU DEMO HCPB circuit's, carried as a representative-loop assumption. The study's held-temperature transect (blanket outlet 450–520 °C) is the sensitivity that must accompany every cycle number.
4. **The calendar's availability is above the held 0.85 at `u` 0 and below it at `u` 0.10** — the residual unplanned fraction is the missing input, surfaced: no admissible source gives it, the instance holds 0 with the label "conditional on the in-vessel calendar", and the study arms at 0.05 / 0.10 are declared stress scenarios, never a probability.
5. **The integer replacement step is live in the calendar too** (six events at five months versus five at seven), so the study reads the count beside every availability and LCOE (minor-radius L-002's rule extended).
6. **What did not move**: `p_fus`, the wall peak, `p_aux_required`, the magnet channels — the closures are downstream of the plasma and magnet chains, so the physics fences (`beta_ok`, `wall_load_ok`, `sustainment_ok`, `burn_hold_ok`, the three magnet fences) do not flip at the design point; `net_positive` and `recirc_ok` gain margin. Off the design point the loop's cubic law can lose it — the study's window re-read is where that is measured.

## What the probe does not do

No divertor, fuel or vacuum quantity is computed here (their candidate forms are in the breadth report; their anchors are checked in `../grounding_sources/stellaris_p14_divertor.png`, `stellaris_p15_divertor.png`, `stellaris_p19_tbr.png`). No off-design point is evaluated. No property table is used (ideal helium; the source's own implied `cp` differs by 0.1 %). The oracle's `p_pump` / `eta_p` / `eta_th` / `availability` inputs were overridden as scalars; the candidate chains' internal structure (states, domain verdicts, the IHX) is not represented — the model items build it.
