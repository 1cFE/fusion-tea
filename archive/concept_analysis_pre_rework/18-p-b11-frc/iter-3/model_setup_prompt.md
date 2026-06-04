# Free-Form Model Update: p-B11 FRC

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: NBI efficiency chain is more pessimistic than the Q_plasma viability threshold derivation assumes

- **Target:** Section 2 (Challenge 3 — NBI recirculating power fraction) and Section 5 Missing Parameters (NBI wall-plug efficiency row)
- **Category:** model
- **Finding:** The Section 2 viability threshold derivation uses η_NBI ≈ 0.50–0.60 (wall-plug to plasma heating). The OSTI 2441289 paper (*Nuclear Fusion* 2024, C-2W performance report) reveals that attenuated NB power reaching the plasma is **<50% of NBI electrical input** — this is duct and geometric losses alone, before accounting for the additional 15±5% beam shine-through measured at C-2W. If NBI source efficiency is ~60% (wall-plug to beam), coupling efficiency is <50%, and shine-through removes another 15%, the total wall-plug-to-plasma heating efficiency is roughly 0.60 × 0.50 × 0.85 ≈ 0.26. At η_NBI = 0.26, the Q_plasma breakeven (1/(η_th × η_NBI) with η_th = 0.30) rises to ~12.8, and the commercial margin target rises to Q_plasma ≥ 25–35 — roughly double the ~10–15 stated in the analysis. The existing derivation treats 50–60% as the wall-plug efficiency, but it is actually the upper bound for just the NBI source step; the plasma-coupled efficiency is substantially lower.
- **Recommendation:** In model_setup.py, split the NBI efficiency parameter into two components: source efficiency (η_NBI_source ≈ 0.55–0.65) and plasma coupling efficiency (η_NBI_couple ≈ 0.35–0.50 based on C-2W data), giving a total η_NBI ≈ 0.20–0.32. Update the Section 2 Q_plasma viability threshold derivation and the sensitivity sweep bounds in the model to use this revised range. The lower bound of the sweep should extend to η_NBI = 0.20 (aggressive coupling losses) and the upper bound to 0.45 (optimistic source + coupling). Cite the OSTI 2441289 source for the attenuation data.
- **Priority:** blocking

---

### F-2: Electron temperature cited throughout as ~300 eV is outdated — C-2W has since reached ~1 keV

- **Target:** Section 5 parameter table (C-2W electron temperature row), Section 3 (FRC Plasma Formation and Sustainment subsystem), Section 1 (experimental physics publications paragraph)
- **Category:** analysis
- **Finding:** The analysis cites "Te ~300 eV" as the C-2W electron temperature in the parameter table and Section 1 narrative, sourced from the Phase 1a tae-c2w-machine-details.md file. The OSTI 2441289 paper (*Nuclear Fusion* 2024) reports that recent C-2W campaigns have achieved peak electron temperature of ~1 keV (>0.75 keV averaged inside the separatrix), described explicitly as "the first time achieving 1 keV in C-2W." This is a 3× improvement over the cited value. The broader analysis conclusions are unchanged — 1 keV Te is still far from the ~150 keV Da Vinci target, and the ~80–100× extrapolation challenge in Section 2 remains — but the specific number is materially wrong and incorrectly represents the current experimental state in both the parameter table and TRL narratives.
- **Recommendation:** Update the Section 5 parameter table Te row to "~1 keV peak (>0.75 keV averaged, recent campaigns)" with source OSTI 2441289. Update Section 1 to note the 1 keV achievement and add this paper to Section 8 Sources. Update Section 3 (FRC Plasma Formation TRL narrative) to reference the ~1 keV milestone as the current experimental high-water mark and note that this changes the extrapolation gap from "~80–100×" in temperature to "~150×" (from 1 keV to 150 keV). Total plasma energy record is also updated to ~13 kJ (from the same source).
- **Priority:** important

---

### F-3: Fast-ion pressure dominance over thermal pressure is now directly measured — partially validates the T_i >> T_e non-equilibrium assumption

- **Target:** Section 2 (Challenge 1 — bremsstrahlung power balance), Section 3 (p-B11 High-Q Plasma Operation TRL)
- **Category:** analysis
- **Finding:** The bremsstrahlung challenge discussion (Section 2, Challenge 1) frames the T_i >> T_e non-equilibrium regime as "physically motivated but unvalidated." The OSTI 2441289 paper provides the first direct peer-reviewed quantitative evidence that C-2W operates in a fast-ion dominated regime: fast-ion pressure exceeds thermal plasma pressure by ~1.5× in the core region (reconstructed via SEQUOIIA equilibrium code). This is direct experimental validation that beam-driven NBI does maintain a meaningful fast-ion population distinct from the bulk thermal plasma at C-2W conditions. The analysis should note this as partial validation of the approach. However, the key qualification is that this is demonstrated at total plasma temperatures of ~1 keV — the fast-ion dominance must be sustained at 150+ keV ion temperatures where electron equilibration rates are dramatically different. The partial validation at low temperature does not close the gap at commercial temperatures, but it is a meaningful intermediate milestone that the current analysis omits.
- **Recommendation:** Add a sentence to Section 2 Challenge 1 noting that equilibrium reconstruction from the OSTI 2441289 C-2W paper confirms fast-ion pressure exceeds thermal pressure by ~1.5× at current operating conditions, partially validating the non-equilibrium strategy at low temperatures. Explicitly qualify that this validation holds at ~1 keV total temperature, and that the question of whether the T_i >> T_e regime persists at 150+ keV (where electron-ion equilibration timescales and bremsstrahlung losses are categorically different) remains the open gap. Update the Section 3 TRL description for "p-B11 High-Q Plasma Operation" to move the fast-ion dominance regime from "unvalidated" to "validated at 1 keV experimental conditions; unvalidated at commercial temperatures."
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Fuel cost calculation error inflates LCOE by ~$70/MWh
- **Target:** Model CAS80 fuel account and model_setup.py fuel consumption formula
- **Category:** model
- **Finding:** The model reports CAS80 fuel cost as $27.4M/yr for 2,739 kg B-11/yr, making fuel 26.75% of LCOE (~$72/MWh). This directly contradicts the analysis (Section 5), which states B-11 fuel cost is negligible (<$1/MWh). Physical check: at 390 MW fusion power and 8.7 MeV per reaction, B-11 consumption is ~160 kg/yr — roughly 17× less than the model computes. Even using the model's inflated quantity, natural boron at $2–5/kg totals ~$5,500–14,000/yr, not $27.4M/yr — implying an effective price of ~$10,000/kg in the model. The error misrepresents one of p-B11's defining TEA advantages (near-zero fuel cost), distorts the LCOE cost breakdown, and adds ~$70/MWh across all branches.
- **Recommendation:** Fix the fuel consumption calculation in model_setup.py using reaction energy 8.7 MeV = 1.394 × 10⁻¹² J/reaction and reactor thermal output to derive B-11 mass per year (~160 kg/yr at 390 MW fusion power). Apply a realistic B-11 price of $2–50/kg (natural boron to lightly enriched). After correction, fuel should appear as a negligible line item (<1% of LCOE), consistent with the analysis text. Rerun all branches and sensitivity sweeps.
- **Priority:** blocking

### F-2: Bremsstrahlung radiation loss fraction fixed at 15% — the #1 physics unknown is not swept
- **Target:** Sensitivity sweep set in model_setup.py; Section 2 Challenge 1
- **Category:** model
- **Finding:** The analysis correctly identifies bremsstrahlung power balance as the most critical physics challenge, noting it "can rival or exceed the fusion alpha power output" at Da Vinci conditions. Yet the model fixes f_rad = 0.15 across all scenarios and excludes it from all six sensitivity sweeps. At fully thermalized Maxwellian p-B11 conditions, f_rad could realistically exceed 0.80–1.0+, making Branch A the only outcome regardless of Q_plasma. TAE's non-Maxwellian T_i >> T_e strategy specifically aims to suppress bremsstrahlung — the degree of suppression achieved is the central undemonstrated claim. Keeping f_rad fixed understates the model's sensitivity to the concept's most uncertain parameter and decouples the sensitivity sweeps from the analysis's central technical bet.
- **Recommendation:** Add f_rad as a seventh sensitivity sweep spanning 0.05 to 0.90. Show LCOE and P_net at each value; identify the f_rad threshold above which Branch A is forced (P_net ≤ 0) at the baseline Q_plasma. Add a Q_plasma × f_rad viability grid analogous to the existing Q_plasma × η_NBI grid (sweep #7), converting the qualitative bremsstrahlung discussion in Section 2 Challenge 1 into a quantitative viability boundary.
- **Priority:** important

### F-3: Steam-mode economic inferiority claim not quantified against a D-T reference
- **Target:** Section 7 cross-concept notes and scenario comparison table
- **Category:** analysis
- **Finding:** Section 7 asserts "Steam-only p-B11 FRC is economically inferior to any D-T concept with equivalent Q_plasma" — an important positioning claim. This is argued logically (aneutronic structural savings cannot overcome a 60-point efficiency gap in steam mode) but is not demonstrated with a reference number. The scenario comparison table shows Branch B at ~$268/MWh and Branch C at ~$79/MWh but provides no D-T anchor. Without at least an order-of-magnitude reference — e.g., what the Helion D-He3 FRC exemplar estimates, or a generic D-T compact tokamak at Q=15 — the reader cannot assess whether the aneutronic structural advantages (no breeding blanket, no shielding, hands-on maintenance) could partially offset the efficiency penalty, or how large the gap is in $/MWh.
- **Recommendation:** Add a single reference row to the scenario comparison table for a D-T FRC or comparable concept at Q=15, steam Rankine, with a rough LCOE range drawn from the Helion D-He3 exemplar (~4 ¢/kWh) or another D-T analysis in the pipeline. Label it clearly as a rough reference, not a validated comparison. This anchors the "steam-mode p-B11 is uncompetitive" conclusion with an order-of-magnitude number and identifies what Q_plasma (if any) would close the gap given the aneutronic structural savings.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/iter-3/model_setup.py`
