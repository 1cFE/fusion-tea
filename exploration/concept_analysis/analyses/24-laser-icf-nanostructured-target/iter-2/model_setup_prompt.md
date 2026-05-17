# 1costingfe Model Update: Laser ICF - Nanostructured Target (p-B11)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: NIF optics damage data fills documented Gap #9 with available analogue
- **Target:** Section 5 (Missing Parameters table, row: "Laser optic replacement rate at 10 Hz PW class") and Section 6 (Gap #9)
- **Category:** analysis
- **Finding:** Section 6, Gap #9 lists "Laser optic damage and replacement rate at 10 Hz petawatt class" as not-yet-sourced, and explicitly recommends "NIF Annual Report optic damage sections; LLNL laser optics literature (imperfect analogue)." The new source osti-servlets-purl-1400089 (LLNL-TR-739796, 2017) is exactly that literature: it reports ~2,000 optic replacements per year and ~$5.6M additional annual operational cost when scaling NIF from 1.8 MJ to 2.6 MJ single-shot operations. This is the best available published analogue for laser IFE optics lifecycle cost, despite the regime difference (MJ nanosecond single-shot vs. 100 J femtosecond 10 Hz).
- **Recommendation:** Update Section 5 to add a row in the Missing Parameters table (or a new analogue row): NIF optics replacement cost analogue: ~2,000 replacements/year, ~$5.6M/year additional O&M, at 2.6 MJ per shot single-shot. Add a brief note quantifying why this analogue is imperfect: Marvel's per-shot energy is ~4 orders of magnitude lower (100 J vs. 2.6 MJ) but cumulative annual fluence on optics may be comparable or higher at 10 Hz continuous. Update Section 6 Gap #9 status from "not-yet-sourced" to "analogue available: LLNL-TR-739796" and note the analogue limitations. This converts an unresolvable gap into a bounded uncertainty.
- **Priority:** important

### F-2: Laser IFE has structural physics advantages over p-B11 MFE — absent from cross-concept comparison
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 currently compares the p-B11 laser IFE concept only against D-T laser IFE and against HB11 vs. Marvel. It does not compare against the p-B11 MFE route, which is the most direct alternative within the same fuel cycle. The new source arxiv-2201-12818 (published Fusion Science and Technology, 2021) provides a quantified physics analysis of tokamak-based p-B11 fusion and identifies two structural blockers that are absent from the laser IFE approach: (1) synchrotron radiation reduces Q from 4.14 to 0.84 when wall reflectivity is 0.95 — an ~80% loss that the paper concludes makes the tokamak p-B11 reactor "not come true unless some techniques have been found to avoid excessive synchrotron radiation loss"; and (2) helium ash accumulation at breakeven parameters drives helium ion density to ~9.5×10²⁰ m⁻³, equaling or exceeding the fuel ion density within 5–50 seconds, requiring helium confinement time strictly less than energy confinement time (inverse of all fusion experience). Both of these blockers are absent from laser IFE: femtosecond pulses at ultrashort timescales do not rely on strong external magnetic fields (no synchrotron penalty), and each shot produces and destroys a fresh plasma target so helium ash cannot accumulate between shots. These are not minor advantages — the tokamak paper's own analysis shows p-B11 MFE is not viable with any existing or near-term confinement technology at realistic wall reflectivity. Goal 1 (Concept Positioning) and Goal 2 (Key Differentiators) are partially unmet because the analysis does not explain why laser confinement is the viable pathway for p-B11 where magnetic confinement is not.
- **Recommendation:** Add a subsection to Section 7: "Comparison with p-B11 MFE (tokamak/mirror routes)." Summarize the synchrotron radiation Q-kill (80% loss at η_w = 0.95) and the helium ash accumulation problem from the 2021 physics paper. Explain that laser IFE avoids both: no strong static magnetic field means no synchrotron emission penalty, and the pulsed fresh-target approach means helium produced in one shot does not contaminate the next. Frame this as a key structural reason why laser IFE (not magnetic confinement) is the appropriate confinement strategy for p-B11 fuel — this explains the concept's positioning within the IFE family and why the physics risk profile is fundamentally different from HB11 concept 04 being pursued via any MFE route.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Direct energy conversion efficiency disconnected from model
- **Target:** Section 2 (Challenge 3) and model sensitivity sweep (eta_dec)
- **Category:** model
- **Finding:** The analysis dedicates an entire Section 2 challenge to hybrid direct energy conversion, calling it a "first-order LCOE lever" that "roughly doubles" net electrical output (35% steam vs 70% Marvel hybrid target). However, the model sensitivity table shows `eta_dec` with elasticity 0.0000, while `eta_th` shows -0.099. This indicates the model is computing only the steam-cycle thermal path and the hybrid direct conversion branch is either absent or disconnected from the LCOE calculation. The two-scenario structure (HB11 steam-only vs Marvel hybrid) is described in Section 7 but not implemented as a scenario branch in the model. The checklist requirement for Section 2 to identify the 2-3 highest-sensitivity parameters cannot be satisfied when the analysis's stated #1 lever (conversion efficiency) shows no model response.
- **Recommendation:** Implement the Marvel hybrid conversion scenario as a model branch where `eta_dec` (alpha particle capture efficiency) and `eta_th` (residual steam fraction) combine to produce net conversion efficiency. The existing model appears to run both Marvel and HB11 cases but uses only `eta_th` for both. Add a scenario sweep over eta_dec from 0% (steam-only fallback) to 60% (near-claim), weighted by `f_direct` (direct fraction of thermal output), and report LCOE vs this parameter. This will produce a non-zero elasticity consistent with the analysis's claim of a 2× lever.
- **Priority:** blocking

### F-2: NaN sensitivity values for availability and core lifetime
- **Target:** Model sensitivity sweep output
- **Category:** model
- **Finding:** The sensitivity output shows `availability = +nan` and `core_lifetime_pb11 = +nan`. Availability is a direct LCOE multiplier (it sets the denominator of annual energy production) — a NaN sensitivity for this parameter indicates a division-by-zero or undefined derivative in the sweep implementation. Similarly, `interest_rate = +nan` is anomalous. These are not informative NaN values from physically undefined scenarios; they are numerical failures in the sweep. The checklist requires that at least 3 parameters show |elasticity| > 0.01 for the sensitivity results to be non-trivial. With availability broken, the sweep understates uncertainty on a parameter that controls whether the 75% placeholder assumption (noted in the model output as a placeholder with no analogue plant) propagates into LCOE at all.
- **Recommendation:** Debug the sensitivity sweep for `availability`, `interest_rate`, and `core_lifetime_pb11`. The most likely cause is that the sweep is computing ΔLCOE / Δparam at a point where a ratio or logarithm is undefined (e.g., if `availability` enters as a multiplicative factor and the base case is already at the boundary). Fix the numerical derivative or switch to finite-difference elasticity for these parameters. Once fixed, verify that availability elasticity is on the order of -1.0 (LCOE scales inversely with availability for a fixed capital cost) — if it is, it should rank as the highest-sensitivity engineering lever and the analysis narrative should flag it accordingly.
- **Priority:** important

### F-3: Section 2 narrative overemphasizes laser capital cost; model shows O&M and target factory dominate
- **Target:** Section 2 (Challenge 2) and Section 5 parameter table
- **Category:** analysis
- **Finding:** Section 2 frames the laser system as "the dominant capital cost component" and the primary recirculating power load, with detailed discussion of cost-per-joule and the 500-laser plant requirement. However, the model sensitivity output shows `driver_laser_per_mw` with elasticity 0.027 — well below `om_cost_pb11` (0.204) and `target_factory_base` (0.134). In the model, O&M and target factory together are roughly 12× more sensitive to LCOE than the laser driver unit cost. The analysis does not acknowledge this ordering, and Section 2 does not identify the 2-3 highest-sensitivity LCOE parameters as required by the modeling recommendations goal. The `om_cost_pb11` constant is a placeholder with no sourced basis (noted in the model output), yet it carries the highest sensitivity of any costing constant — this should be flagged as a priority gap in Section 5 or Section 6 but is not.
- **Recommendation:** Add a paragraph in Section 2 (or a dedicated subsection) that explicitly names the 2-3 highest-sensitivity LCOE parameters for this concept, cross-referencing the model's sensitivity ordering. Acknowledge that target factory cost and O&M cost dominate over laser driver capital cost in the model's current parameterization, and note that this ranking is sensitive to the laser capital cost assumption (currently 8 M$/MW_driver as a framework default). Add an O&M cost basis row to the Section 5 parameter table with gap type "truly-unknown" and criticality "blocking" to match what the model sensitivity implies.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/iter-2/model_setup.py`
