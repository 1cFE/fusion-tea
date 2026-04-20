VERDICT: FINDINGS

---

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
