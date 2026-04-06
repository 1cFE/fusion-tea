# Review: Magnetized Target Fusion - Pneumatic Compression (D-T)

**Iteration:** 1
**Date:** 2026-04-05
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 12 files

---

## Strategic Assessment

### 1. Modeling Approach

The modeling approach is well-reasoned and honest about its limits. Rather than forcing a bottom-up build that the data cannot support, the analysis correctly anchors on the 300 MWe commercial target and works backward — treating the result as a scenario anchor rather than a prediction. The three primary sensitivity dimensions (availability, thermal efficiency, driver power) are correctly identified, and the model header's explicit labeling of "BLOCKING unknowns: Q, eta_th, recirculating power fraction" is exactly the right framing for a TRL 2–3 concept with no published energy balance.

The CAS mapping choices in the model code are largely defensible. The key deviations from MAG_TARGET defaults are individually justified with citations and confidence ratings:
- `p_cryo = 0.0` — correctly zeroed, confirmed by multiple sources that no HTS coils are used
- `p_target = 0.0` — correctly distinguished from MagLIF's consumable RTL+target structure
- `C220103 = $10M` — small Cu coils for CT injector; the contrast with HTS tokamak magnets is appropriately drawn
- `C220104 = $180M` — explicitly flagged as "truly-unknown" with a stated range of $50M–$500M+

The compression driver at $180M (C220104) ends up as the second-largest CAS22 line item behind Installation ($170.9M) and Remote Handling ($93.9M). Given that the analysis argues this is the *dominant non-blanket capital account*, it is worth noting the model output doesn't fully bear that out at the chosen central value — Installation and Remote Handling rival it. The $180M floor estimate rationale is transparent, but analysts looking at the output should understand this is likely underweighted at the central estimate.

The `eta_pin = 0.80` choice (steam-driven mechanical pistons rather than pulsed electrical) is one of the most structurally important deviations from the MAG_TARGET default (0.30) and is well-justified. The sensitivity analysis confirms it has a meaningful but not dominant effect on LCOE (elasticity ≈ −0.055), appropriate for a design where availability dominates (elasticity ≈ −0.94).

One factual concern: the model uses `blanket_t = 1.0 m` with a note that the thickness "is inferred from mass estimates... not published directly." However, the FST 2025 peer-reviewed paper explicitly states "1.5 m thick liquid metal blanket" (general-fusion-fst-2025-fuel-cycles.md, §Introduction). A published value exists and is not being used. Since plasma_t has elasticity +0.071 and blanket_t +0.052, this understates the reactor's physical footprint and modestly understates capital cost. This should be corrected.

### 2. Strategic Positioning

The concept is correctly placed as unique in the MIF space: the only major private fusion company using *mechanical* (pneumatic/steam) compression rather than pulsed electromagnetic, laser, or plasma-jet drivers. The tokamak comparison table in Section 7 is methodical and the "Novel / Borrowed / Shared" classification is a useful device. The key structural advantages — no HTS magnets, no cryoplant, no per-shot consumables — are correctly articulated and their LCOE implications drawn clearly.

The cross-concept framing is internally consistent. The reuse from 07-maglif (pulsed LCOE structure, rep rate as dominant lever, no-magnet advantage) is appropriate since both are pulsed MIF at ~1 Hz commercial target. The divergence — no per-shot consumables in GF vs. MagLIF's ~28M targets/year — is a genuine structural OPEX difference and is correctly identified as a CAS60 advantage.

The rep rate framing (86,400× gap between current ~1 shot/day and commercial 1 Hz) is one of the strongest parts of the analysis. The H3 threshold hypothesis — that <0.1 Hz makes the concept uncompetitive regardless of capital cost — provides a qualitative viability gate that complements the continuous LCOE model.

The concept family context section correctly identifies GF as having no direct technology analogues, which is important for setting appropriate uncertainty expectations.

### 3. Risk and Uncertainty Framing

The binary failure mode treatment is the most analytically distinctive element of this analysis and is handled well. FM-1 (compression ratio shortfall: 8:1 achieved vs. 12:1 required in water tests) and FM-2 (commercial pneumatic system infeasibility) are correctly distinguished from continuous LCOE parameters. Labeling them as "explicit go/no-go flags" rather than sensitivity ranges is the right call — these are not parameter uncertainties but architecture-level viability questions.

TRL ratings are conservative and defensible: TRL 2–3 for the commercial pneumatic compression system, TRL 5–6 for the CT plasma injector, TRL 4–5 for liquid metal heat transfer (integrated). The distinction between the LM26 electromagnetic surrogate (TRL 6) and the commercial pneumatic system (TRL 2–3) is correctly drawn — the surrogate's TRL is not transferable to the commercial mechanism.

Economic, supply chain, and regulatory risks are addressed at appropriate depth given data availability. The Li-6 enrichment supply chain concern (no Western capacity for fusion-fleet quantities) is correctly noted and linked to the analogous risk flagged in the HTS tokamak analysis. Piston seal/wear in an activated liquid metal environment is flagged as a truly-unknown O&M driver with no experimental basis.

One gap: the safety regulatory regime for a large-scale liquid lithium facility (pure Li option) is not addressed. Liquid lithium in multi-tonne quantities at a nuclear facility faces a different regulatory classification than PbLi (which is considered lower-risk). The cost of Li fire/explosion safety infrastructure is mentioned in the H2 hypothesis but is not quantified or flagged as a separate gap item in the data gap inventory.

### 4. Data Sufficiency

The analysis is admirably honest about what it doesn't know. The "blocking unknowns" label is applied correctly to Q, thermal efficiency, and recirculating power fraction. The data gap table (Section 6) is comprehensive — 14 items with gap type, criticality, and source recommendations.

The sources are adequate for the claims made. The FST 2025 peer-reviewed paper is a high-quality primary source for cavity geometry, liquid metal options, and tritium inventory. The IAEA FEC 2025 abstract confirms LM26 parameters. The APS 2018 overview is the primary anchor for compression parameters. No claims are made beyond what the sources support.

One inconsistency: the analysis lists the volume compression ratio as "~1000× (3 orders of magnitude)" in the Section 5 parameters table, citing APS 2018 data (density from 10²² to 10²⁵ ions/m³). But the FST 2025 paper states "350-fold volumetric compression would achieve the Lawson criterion." These two numbers are reconcilable if the 10²²→10²⁵ represents density (which equals 1/volume), meaning a 1000× volume compression is required for full density scaling — while the 350-fold refers to the cavity volume reduction (the cavity collapses but the plasma doesn't occupy the full initial cavity volume). However, the discrepancy is not explained and could confuse readers comparing the two sources. A clarifying note is warranted.

The model output's Q_sci = 19.8 deserves a clarifying comment. The analysis correctly states Q is unknown, but the model computes Q_sci = P_fus / P_driver = 989 MW / 50 MW using the backward-derived fusion power. This is internally consistent with the scenario anchor approach, but Q_sci = 19.8 should be clearly labeled as a derived scenario output (not an independent estimate of scientific Q), since it would be misleading to report it alongside claimed values from concepts where Q has experimental basis.

### 5. Cross-Concept Consistency

Cross-referencing with four prior analyses (07-maglif, 01-hts-compact-tokamak, 21-spherical-tokamak-hts, 08-frc-w-direct-conversion) is thorough. The shared frameworks that transfer (pulsed LCOE structure, D-T tritium costing, capacity factor sensitivity, Li-6 enrichment constraints) are correctly applied, and divergences are clearly articulated.

The comparison of tritium breeding geometry (4π solid angle in GF vs. outboard-only ~1–1.5π for tokamaks) is correctly identified as an advantage that likely relaxes Li-6 enrichment requirements vs. the tokamak cases. The absence of beryllium (vs. FLiBe-using concepts) is correctly noted as a supply chain simplification.

One labeling inconsistency: Section 7 TEA Implications table labels the compression driver's cost account as "CAS27 (compression/driver system)." CAS27 in the standard fusion cost account structure is "Special Materials" (not the compression driver system). The model correctly places the compression driver under C220104, which is a sub-account of CAS22 (Reactor Plant Equipment). The CAS27 reference in the analysis text is incorrect and should be updated to C220104 / CAS22.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The modeling approach correctly handles a genuinely underdetermined concept by anchoring on the commercial output target and treating results as scenario anchors rather than predictions. Binary failure modes are cleanly separated from continuous LCOE parameters, risk framing is conservative and well-sourced, and cross-concept consistency is strong. Three minor fixes are needed to correct a published blanket thickness, a CAS labeling error, and to clarify the compression ratio discrepancy between two primary sources.

---

## Minor Fixes (PROCEED only)

### PA-1: Correct blanket_t from 1.0 m to 1.5 m per FST 2025
- **Category:** factual-concern
- **Severity:** minor
- **Location:** `model_setup.py` §Geometry; `analysis.md` §Section 5 (parameters table, inferred rows)
- **Finding:** `blanket_t = 1.0 m` is described as inferred from mass estimates with low confidence. The FST 2025 peer-reviewed paper explicitly states "1.5 m thick liquid metal blanket" (general-fusion-fst-2025-fuel-cycles.md, §Introduction, line 46). A published value exists and should take precedence over the geometric inference.
- **Proposed Fix:** Update `blanket_t = 1.5` in model_setup.py with the FST 2025 citation; update the Section 5 parameters table row to show "1.5 m" at "high" confidence sourced to FST 2025. Re-run model to get updated LCOE (blanket_t elasticity ≈ +0.052, so ~7.5% increase in LCOE from this correction alone).
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Fix CAS27 labeling error — compression driver belongs under CAS22, not CAS27
- **Category:** inconsistency
- **Severity:** minor
- **Location:** `analysis.md` §Section 7, TEA Implications table (row: "Pneumatic compression driver")
- **Finding:** The TEA Implications table labels the compression driver cost account as "CAS27 (compression/driver system)." CAS27 in the standard fusion costing framework is "Special Materials." The model correctly places the compression driver under C220104 (a CAS22 sub-account). The analysis text has an incorrect CAS account reference.
- **Proposed Fix:** In the TEA Implications table, update "CAS27 (compression/driver system): dominant unknown" to "C220104 / CAS22 (Reactor Plant Equipment — Compression Driver): dominant unknown." Verify no other references to CAS27 in this context in the analysis.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Clarify 350-fold (FST 2025) vs. 1000× (APS 2018) compression ratio discrepancy
- **Category:** inconsistency
- **Severity:** minor
- **Location:** `analysis.md` §Section 5, parameters table (Volume compression ratio row)
- **Finding:** The parameters table lists "Volume compression ratio (target): ~1000× (3 orders of magnitude)" citing APS 2018. The FST 2025 paper states "350-fold volumetric compression would achieve the Lawson criterion." These numbers are potentially reconcilable (350× cavity volume collapse ≠ 1000× plasma density increase if the plasma doesn't initially fill the cavity), but the discrepancy is unexplained and could mislead readers comparing the two sources.
- **Proposed Fix:** Add a note to the parameters table row explaining the reconciliation: the 1000× density increase (10²²→10²⁵ ions/m³) from APS 2018 reflects plasma density scaling, while the 350-fold from FST 2025 refers to the cavity volume collapse ratio. If the plasma initially occupies ~35% of the cavity volume, these are consistent. Alternatively, flag this as a source discrepancy requiring clarification.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-4: Add clarifying note that Q_sci in model output is a derived scenario value, not an independent estimate
- **Category:** improvement
- **Severity:** minor
- **Location:** `model_setup.py` §Modeling notes; `model_output.txt` (Q_sci = 19.8 output line)
- **Finding:** The model output reports "Scientific Q (P_fus/P_driver): 19.8" computed as fusion power / driver power = 989 MW / 50 MW. Since fusion power is backward-derived from the 300 MWe net electric target (not from an independent physics estimate), Q_sci = 19.8 is a scenario-consistent derived value, not an evidence-based Q estimate. Without this context, the output line could be misread as a physics prediction.
- **Proposed Fix:** Add to the model's "Modeling notes" print block: "Q_sci = {val:.1f} is scenario-derived (P_fus inferred from 300 MWe net electric backward; not an independent Q estimate). Actual Q is unknown and undisclosed by GF."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
