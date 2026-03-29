# Review: Laser ICF - Hybrid Direct Drive (D-T)

**Iteration:** 1
**Date:** 2026-03-29
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 10 files (7 primary content files + 3 .orig.md researcher notes)

---

## Citation Verification

### CV-1: "By using a gas laser architecture, we've reduced the cost per joule by more than 30x compared to the National Ignition Facility (NIF)."
- **Source cited:** xcimer-energy-approach.md (§2 Challenge 1, §S5 Table)
- **Status:** FOUND
- **Actual text:** "By using a gas laser architecture, we've reduced the cost per joule by more than 30x compared to the National Ignition Facility (NIF)." (xcimer-energy-approach.md line 14)
- **Notes:** Exact verbatim match.

---

### CV-2: "We need approximately a 1000x increase in wall-plug gain compared to the NIF, allowing for a commercially viable system. Fortunately, we believe we can achieve this by implementing advances in three areas, each contributing roughly a factor of 10."
- **Source cited:** xcimer-science-page.md (§2 Challenge 2)
- **Status:** PARTIAL MATCH — composite paraphrase formatted as a direct quote
- **Actual text:** "These together provide a 1000x increase in wall-plug gain compared to the NIF, allowing for a commercially viable system." (xcimer-science-page.md line 88). The phrasing "We need approximately a 1000x increase" and "Fortunately, we believe we can achieve this by implementing advances in three areas, each contributing roughly a factor of 10" do not appear verbatim in the source. The science page describes the three factors (10× capsule gain, 10× laser efficiency, 7.5× coupling) separately and states the combined 1000× result — the quoted text is an editorial synthesis.
- **Notes:** See PA-1. The underlying claim is fully supported by the source; the issue is quotation formatting, not accuracy.

---

### CV-3: "Xcimer's approach utilizing a liquid first wall allows us to use readily available commercial materials that minimize activation, extend the lifetime and comply with our waste and safety goals."
- **Source cited:** xcimer-science-page.md (§S4 Structural Materials)
- **Status:** FOUND
- **Actual text:** "Xcimer's approach utilizing a liquid first wall allows us to use readily available commercial materials that minimize activation, extend the lifetime and comply with our waste and safety goals." (xcimer-science-page.md line 54)
- **Notes:** Exact verbatim match.

---

### CV-4: "Making sure that we have enough tritium, and figuring out how to extract that material to use it for future shots, is a big task. We have to be able to breed enough tritium to keep the plant going."
- **Source cited:** focused-energy-callahan-interview.md §Tritium Breeding
- **Status:** FOUND
- **Actual text:** "Making sure that we have enough tritium, and figuring out how to extract that material to use it for future shots, is a big task. We have to be able to breed enough tritium to keep the plant going." (focused-energy-callahan-interview.md lines 88–89)
- **Notes:** Exact verbatim match. Correctly attributed to Callahan describing D-T IFE generally, not Xcimer specifically.

---

### CV-5: NIF best-shot gain ~4.1, April 2025
- **Source cited:** focused-energy-callahan-interview.md §NIF Best Performance
- **Status:** FOUND
- **Actual text:** "the best shot at NIF... occurred during an experiment in April 2025, which had a target gain of about 4.1." (focused-energy-callahan-interview.md lines 31–32)
- **Notes:** The section heading "§NIF Best Performance" does not exist verbatim in the source; the actual header is "What is the current state of the art at NIF..." — the citation is a loose label, not a structural heading. Content is verifiable and accurate. The Callahan interview also states "so they got out about eight megajoules" (4.1 × 2 MJ ≈ 8.2 MJ). Compare: xcimer-science-page.md claims "8.6 MJ... scientific gain of 4.13" (8.6 / 2 = 4.3 ≠ 4.13 — an internal inconsistency in that source). The analysis correctly cites the Callahan interview which is internally consistent.

---

### CV-6: NIF cost $3.5B, 2 MJ, 192 beams
- **Source cited:** xcimer-science-page.md §S5 Table (NIF Comparison)
- **Status:** FOUND (with in-source discrepancy)
- **Actual text (line 74):** "The entire NIF facility requires 192 beam lines and 120 tons of precision glass, with a total system cost of over $3,600,000,000"; **(line 92):** "NIF's $3.5B cost." The analysis uses $3.5B, which matches line 92.
- **Notes:** The source itself contains two figures ($3.5B and $3.6B) for what appears to be the same facility. The analysis uses $3.5B, which is defensible from line 92. No action required from the analysis side.

---

### CV-7: >90% coupling efficiency (HDD) vs. 12% (NIF indirect drive)
- **Source cited:** xcimer-science-page.md (§S5 Table, §2 Challenge 2)
- **Status:** FOUND
- **Actual text:** "we'll couple over 90% of the laser energy directly to the fuel capsule, vs. only 12% coupled via the x-ray bath on the NIF" (xcimer-science-page.md line 88); also "the fuel capsule absorbed 12% of the energy that was in the laser pulse" (line 84).
- **Notes:** Exact match.

---

### CV-8: HYLIFE-II reference design — 940 MWe, 6 Hz, 350 MJ yield
- **Source cited:** hylife-energy-conversion-notes.orig.md §HYLIFE-II
- **Status:** FOUND
- **Actual text:** "Heavy-ion driver (5 MJ), 350 MJ fusion yield, 6 Hz → 940 MWe" (hylife-energy-conversion-notes.orig.md line 18)
- **Notes:** hylife-energy-conversion-notes.orig.md is a researcher notes file (dated 2026-03-07), not a direct extraction of the HYLIFE-II Final Report. The numbers synthesized therein correctly reflect the canonical HYLIFE-II design. The analysis accurately labels the source as notes rather than primary text.

---

### CV-9: He Brayton cycle at ~45% thermal efficiency for HYLIFE heritage
- **Source cited:** hylife-energy-conversion-notes.orig.md §HYLIFE-II; xcimer-energy-approach.md
- **Status:** FOUND in researcher notes; NOT FOUND in primary extracted web content
- **Actual text in notes:** "exchange heat with helium to drive a gas turbine that extracts 45% of the fusion energy as electricity" (hylife-energy-conversion-notes.orig.md line 10); "~45% thermal-to-electric conversion efficiency" (xcimer-energy-approach.orig.md line 25)
- **Notes:** The 45% figure is present in the .orig.md researcher notes but does not appear in xcimer-energy-approach.md (the actual web extraction). The model_setup.py constant `ETA_TH_BRAYTON = 0.45` derives from researcher notes rather than a direct primary source extraction. The citation "xcimer-energy-approach.md" in the model code header is inaccurate for this specific value — the correct citation is the .orig.md notes file (or ultimately the HYLIFE-II Final Report, not yet extracted). See PA-2.

---

### CV-10: KrF wall-plug efficiency at kJ scale ~2–5% (NRL Electra)
- **Source cited:** None (uncited assertion in §2 Challenge 2)
- **Status:** NOT FOUND in available Phase 1a sources
- **Actual text:** xcimer-science-page.md mentions NRL Electra "demonstrated key technology necessary for enabling an excimer laser" (line 152) but gives no efficiency number. The NIF laser efficiency of 0.5% appears in xcimer-science-page.md line 84 (for Nd:glass, not KrF).
- **Notes:** The 2–5% KrF efficiency claim appears uncited in §2 Challenge 2. The claim is plausible (KrF excimer at kJ-scale is known to achieve ~5–7% from program literature) but lacks an inline source reference in the available documents. See PA-3.

---

## Calculation Verification

### CALC-1: Q_eng at 7% laser efficiency ≈ 5.7
- **Claimed:** "1.8 GJ yield × 0.45 thermal efficiency / (10 MJ / 0.07) ≈ 5.7" (§2 Challenge 2)
- **Re-derived:** Gross output = 1.8 × 10⁹ J × 0.45 = 810 MJ; Laser input = 10 MJ / 0.07 = 142.9 MJ; Q_eng = 810 / 142.9 = 5.67 ≈ 5.7 ✓
- **Status:** MATCH
- **Notes:** None.

---

### CALC-2: Q_eng at 10% laser efficiency ≈ 8.1–8.2
- **Claimed:** "Q_eng ≈ 8.1–8.2" (§2 Challenge 2; §S5 Table: "~8.2")
- **Re-derived:** Gross output = 810 MJ; Laser input = 10 MJ / 0.10 = 100 MJ; Q_eng = 810 / 100 = 8.1
- **Status:** MATCH (lower bound 8.1 verified; upper bound 8.2 from Xcimer-TRUMPF whitepaper is unverified but directionally consistent)
- **Notes:** The §S5 Table reports "~8.2" citing the whitepaper via 26-laser-icf-indirect-drive.md. The derivation gives 8.1. The 0.1 discrepancy likely comes from using 1.8 GJ as the lower bound of the "1.6–1.8 GJ" yield range vs. the whitepaper's specific value. Not a concern.

---

### CALC-3: NIF cost per joule ~$1,750/J
- **Claimed:** "$3.5B for 2 MJ equals ~$1,750/J" (§2 Challenge 1)
- **Re-derived:** $3.5 × 10⁹ / (2 × 10⁶ J) = $1,750/J ✓
- **Status:** MATCH
- **Notes:** Correctly supports the "22–29× reduction" calculation: $1,750 / $80 = 21.9× and $1,750 / $60 = 29.2× for the $60–80/J NOAK range.

---

### CALC-4: HYLIFE-II thermal efficiency derivation
- **Claimed:** "940 MWe / 2.1 GW thermal = 44.8%" (§2 Challenge 3; implied in notes citation)
- **Re-derived:** Thermal power = 350 MJ/shot × 6 Hz = 2,100 MW; η = 940 / 2100 = 44.76% ≈ 44.8% ✓
- **Status:** MATCH
- **Notes:** Consistent with "~45%" used throughout.

---

### CALC-5: Annual target count at 0.5 Hz, 85% CF
- **Claimed:** "0.5 Hz × 365 days × 86,400 s/day × 0.85 ≈ 13.4 million targets/year" (§2.7, §H-4)
- **Re-derived:** 0.5 × 86,400 × 365 × 0.85 = 0.5 × 26,805,600 = 13,402,800 ≈ 13.4 × 10⁶ ✓
- **Status:** MATCH
- **Notes:** Same value confirmed in model_setup.py `SHOTS_PER_YEAR` computation.

---

### CALC-6: Annual electricity production
- **Claimed:** "400 MWe × 0.85 CF × 8,760 h/yr ≈ 2,978 GWh/yr" (§H-4)
- **Re-derived:** 400 × 0.85 × 8,760 = 2,978,400 MWh = 2,978.4 GWh ✓
- **Status:** MATCH
- **Notes:** None.

---

### CALC-7: H-4 LCOE contributions at $1/$10/$100/target
- **Claimed:** "$1/target → $4.5/MWh; $10/target → $45/MWh; $100/target → $450/MWh"
- **Re-derived:**
  - $1/target: $1 × 13.4M / yr / 2,978 GWh × (10⁶/10³) = $4.50/MWh ✓
  - $10/target: $10 × 13.4M / 2,978 GWh × 1000 = $44.97/MWh ≈ $45 ✓
  - $100/target: $449.7/MWh ≈ $450 ✓
- **Status:** MATCH
- **Notes:** All three point calculations are correct.

---

### CALC-8: H-4 threshold statement — "$5/target for <10% of $50/MWh LCOE"
- **Claimed:** "target cost must remain below ~$5/target for the target factory to represent less than ~10% of a $50/MWh LCOE target" (§H-4); model_setup.py marks `tgt_cost == 5.0` as `"← viability threshold"`
- **Re-derived:**
  - At $5/target: LCOE contribution = $5 × 13.4M / 2,978 GWh × 1000 = **$22.5/MWh**
  - $22.5/MWh ÷ $50/MWh = **45%** of LCOE — not less than 10%
  - For <10% of $50/MWh (= <$5/MWh): required target cost ≤ $5/MWh × 2,978 GWh / (13.4M × 1000) = **$1.11/target**
- **Status:** MISMATCH — the threshold is ~$1/target, not ~$5/target
- **Notes:** The text correctly calculates each LCOE contribution (CALC-7 checks out) but then states an incorrect threshold. The Goodin et al. "$1–5/target criterion" and the "<10% of LCOE" criterion are cited together but point to different limits: Goodin's viability range is $1–5/target as a standalone judgment; the 10%-of-LCOE math supports only $1/target. The analysis conflates these two criteria. The model_setup.py viability threshold flag (`tgt_cost == 5.0`) propagates the same error. See PA-4.

---

### CALC-9: Indirect drive laser energy requirement (75 MJ for equal yield)
- **Claimed:** "HDD requires ~10 MJ, indirect drive requires ~75 MJ [inferred: 10 MJ × 90% / 12% = 75 MJ]" (§7)
- **Re-derived:** 10 MJ × (0.90 / 0.12) = 75 MJ ✓ (given constant capsule gain assumption)
- **Status:** MATCH
- **Notes:** The calculation is internally consistent with stated coupling efficiencies. The implicit assumption — that an indirect drive plant would use the same ~200× capsule gain as the HDD design — is heroic; in practice, indirect drive capsules are optimized for x-ray drive and may achieve different gains at different driver energies. The analysis correctly marks this [inferred] and notes it requires verification against concept 26 analysis. No action needed but the economic comparison ($5.25B laser capital for indirect drive) should not be cited outside this analysis as a confirmed figure.

---

## Model Setup Audit

### MSA-1: `NET_ELECTRIC_MW = 400.0`
- **Value:** 400.0 MWe
- **Source:** analysis.md §S5 Table "Net electrical output (pilot)" citing 26-laser-icf-indirect-drive.md (via Xcimer-TRUMPF whitepaper gap #7)
- **Status:** TRACED (with UNCERTAIN flag)
- **Notes:** Correctly flagged as uncertain pending whitepaper extraction.

---

### MSA-2: `LASER_ENERGY_MJ = 10.0`, `REP_RATE_HZ = 0.5`
- **Value:** 10 MJ/pulse, 0.5 Hz
- **Source:** xcimer-energy-approach.md (10+ MJ energy, sub-Hz rep rate); analysis.md §S5 Table
- **Status:** TRACED
- **Notes:** 10 MJ is the design driver; 0.5 Hz is the nominal central estimate within the "0.25–1 Hz" range. Consistent with analysis.

---

### MSA-3: `ETA_PIN1 = 0.07` (laser wall-plug efficiency)
- **Value:** 7% (conservative demonstrated-scale)
- **Source:** analysis.md §S2 Challenge 2; xcimer-science-page.md (10% target)
- **Status:** TRACED (with UNCERTAIN flag)
- **Notes:** Xcimer's target is 10%; 7% is conservative. Using the conservative value as model default is defensible. Sensitivity sweep on η_laser is the appropriate mechanism to explore the range.

---

### MSA-4: `eta_pin2 = ETA_PIN1 = 0.07` when `p_ignition = 0.0`
- **Value:** 0.07
- **Source:** analysis.md §S3 HDD Target Physics ("brief hohlraum pre-pulse is part of ASPEN main beam")
- **Status:** TRACED (intent clear; framework behavior warrants verification)
- **Notes:** Setting `p_ignition=0.0` likely causes the framework to zero out any ignition power flow regardless of `eta_pin2`. However, if the framework uses `eta_pin2` for a non-ignition purpose (e.g., secondary beam efficiency circuit), the value 0.07 could silently introduce an incorrect term. The safest approach would be to set `eta_pin2=1.0` (identity/passthrough) or confirm the framework documentation explicitly defines the behavior of `eta_pin2` when `p_ignition=0.0`. See PA-5.

---

### MSA-5: `C220104` override — NOAK $700M / FOAK $1,100M
- **Value:** 700.0 M$ / 1100.0 M$
- **Source:** 26-laser-icf-indirect-drive.md §Comparison Table (citing Xcimer-TRUMPF whitepaper Feb 2026, gap #7)
- **Status:** TRACED (secondary source; primary not yet extracted)
- **Notes:** Unit check: $70/J × 10 MJ = $70 × 10⁶ = $700M = 700 M$ ✓. The ×1000 conversion in the comment is correctly documented. The UNCERTAIN flag and gap #7 reference are appropriate.

---

### MSA-6: `C220103 = 0.0` (magnets)
- **Value:** 0.0 M$
- **Source:** xcimer-energy-approach.md; analysis.md §S7 cross-concept table
- **Status:** TRACED
- **Notes:** Correct — IFE architecture has no superconducting coils.

---

### MSA-7: `C220108 = 0.0` (divertor)
- **Value:** 0.0 M$
- **Source:** xcimer-energy-approach.md (FLiBe liquid wall); xcimer-science-page.md; analysis.md §S7
- **Status:** TRACED
- **Notes:** Correct — liquid FLiBe wet wall eliminates plasma-facing component account.

---

### MSA-8: `OVERRIDES_NOAK_BRAYTON` reused for `result_steam` scenario
- **Value:** Same `C220104/C220103/C220108` overrides in both NOAK-Brayton and NOAK-Steam runs
- **Source:** Intentional design (analysis.md §H-3)
- **Status:** TRACED
- **Notes:** Correct. Laser capital does not depend on thermal cycle choice; only `eta_th` changes between scenarios. The reuse is deliberate and properly documented.

---

### MSA-9: `mn = 1.1` (neutron energy multiplier), `eta_p = 0.5` (pumping efficiency)
- **Value:** 1.1, 0.5
- **Source:** DEFAULT (ife_laser_ife.yaml framework defaults)
- **Status:** UNTRACED (framework defaults with no concept-specific source)
- **Notes:** Both are labeled DEFAULT. `mn = 1.1` is a standard D-T neutron multiplier and is physically reasonable (slightly above 1.0 from n,2n and n,gamma reactions in FLiBe). `eta_p = 0.5` (pumping efficiency) is a framework default with no Xcimer-specific basis and no inline citation. For a concept where FLiBe pumping power may be significant, this parameter could affect the power balance calculation. Consider adding a note that pumping efficiency is unconstrained for this architecture.

---

### MSA-10: `plasma_t = 4.0` (chamber radius, m)
- **Value:** 4.0 m (DEFAULT)
- **Source:** DEFAULT: ife_laser_ife.yaml — comment flags as "UNCERTAIN: Xcimer HYLIFE-III scale unconfirmed"
- **Status:** UNTRACED (no Xcimer-specific source)
- **Notes:** Flagged appropriately as UNCERTAIN. HYLIFE-II chamber dimensions are available in the 1994 Final Report (gap #4). Once extracted, this should be updated with a confirmed radius.

---

## Consistency Check

**Section 5 parameter table vs. narrative**: Values in §S5 Table are consistent with §2 Challenge claims throughout. The yield range "1.6–1.8 GJ" in the table correctly brackets the §2 derivation of 1.8 GJ (upper bound from targets achieved simultaneously) and the 1.6 GJ figure from the reference artifact. The rep rate "0.25–1 Hz" in the table is consistent with "every couple seconds" in the xcimer-science-page.md source.

**TRL ratings vs. challenges**: Section 3 assigns TRL 2–3 for HDD target physics, TRL 2 for target fabrication, TRL 3–4 for KrF ASPEN laser, and TRL 3–4 for chamber clearing. These ratings are consistent with the challenge descriptions in Section 2 — particularly the identification of the 10 MJ ASPEN scale as undemonstrated (constraining TRL to 3–4) and the capsule gain of ~200 as extrapolated from NIF data (TRL 2–3). The FLiBe BOP rating of TRL 7–8 for the conventional side / TRL 4–5 for the FLiBe interface is internally consistent with the identified missing-at-scale items.

**H-4 threshold consistency**: There is an internal inconsistency between the LCOE calculation results (CALC-7: $1/target → $4.5/MWh is the only point below 10% of $50/MWh) and the stated threshold text ("below ~$5/target"). The surrounding narrative ("within range, but only at the lower end") implicitly signals awareness that $5/target is too high, but the stated criterion is incorrect. This inconsistency propagates into model_setup.py. See PA-4.

**Model setup vs. §S5 parameter table**: All model_setup.py forward() parameters that map to §S5 table entries are consistent:
- NET_ELECTRIC_MW = 400 MWe ✓ (§S5: "~400 MWe")
- LASER_ENERGY_MJ = 10 MJ ✓ (§S5: "~10+ MJ")
- REP_RATE_HZ = 0.5 Hz ✓ (§S5: "0.25–1 Hz, central 0.25–0.5 Hz")
- ETA_PIN1 = 0.07 ✓ (§S5: "5–7% demonstrated, 10% target")
- ETA_TH_BRAYTON = 0.45 ✓ (§S5: "~45% He Brayton heritage")
- ETA_TH_STEAM = 0.33 ✓ (§S5: "~33% Steam Rankine")
- LIFETIME_YR = 30 ✓ (§S5: "30 years, no first-wall replacement")

**Phoenix milestone timing**: The analysis §3 states the Phoenix milestone was completed "June 2025" citing dossier.md. The xcimer-energy-approach.orig.md (extracted 2026-03-07) states "Long Pulse Kinetics (LPK) platform completed early 2025" and "Phoenix on track for completion in 2026." As of the source extraction date (March 2026), the full Phoenix system had not yet completed. The "June 2025" date likely refers to the LPK subsystem milestone, not the Phoenix laser system itself. The analysis may be conflating these two milestones. See PA-6.

---

## Proposed Actions

### PA-1: Fix composite quote CV-2 (1000× wall-plug gain)
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §2 Challenge 2, quotation block
- **Finding:** The quoted text "We need approximately a 1000x increase in wall-plug gain compared to the NIF, allowing for a commercially viable system. Fortunately, we believe we can achieve this by implementing advances in three areas, each contributing roughly a factor of 10." does not appear verbatim in xcimer-science-page.md. The source says "These together provide a 1000x increase in wall-plug gain compared to the NIF, allowing for a commercially viable system" (one sentence). The full quote as written is a composite paraphrase of the science page narrative formatted as a blockquote.
- **Proposed Fix:** Replace with the exact source sentence, adding a prose summary for the "three areas each contributing ~10×" context: *"These together provide a 1000x increase in wall-plug gain compared to the NIF, allowing for a commercially viable system." — xcimer-science-page.md. The three contributing factors (10× capsule gain, 10× laser efficiency, ~7.5× coupling improvement) are described individually elsewhere in the same page.*
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-2: Fix model_setup.py citation for `ETA_TH_BRAYTON = 0.45`
- **Category:** citation-error
- **Severity:** minor
- **Location:** model_setup.py line 108; also analysis.md §S5 Table thermal efficiency row
- **Finding:** The model_setup.py comment cites `hylife-energy-conversion-notes.orig.md §HYLIFE-II` for ETA_TH_BRAYTON = 0.45. This is correct. However, the §S5 Table in analysis.md cites `xcimer-energy-approach.md` as a source for He Brayton / 45% efficiency. The actual web extraction (xcimer-energy-approach.md) does not contain the 45% figure or "He Brayton" language — these appear only in the .orig.md researcher notes. The analysis.md citation trail for 45% He Brayton should be updated to cite xcimer-energy-approach.orig.md and hylife-energy-conversion-notes.orig.md as the actual sources, noting that primary confirmation from the HYLIFE-II Final Report (gap #4) is pending.
- **Proposed Fix:** In §S5 Table thermal efficiency row, change source from `xcimer-energy-approach.md` to `xcimer-energy-approach.orig.md; hylife-energy-conversion-notes.orig.md §HYLIFE-II` and note that the .orig.md files are researcher notes rather than primary extractions.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-3: Add inline citation for KrF 2–5% efficiency (NRL Electra)
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §2 Challenge 2, sentence "Current KrF laser wall-plug efficiency at kJ scale is ~2–5% (NRL Electra)"
- **Finding:** The 2–5% KrF efficiency claim for NRL Electra has no inline source citation. The Phase 1a sources confirm Electra demonstrated "key technology necessary" at "five shots per second" (xcimer-science-page.md) but do not state an efficiency number. The claim is physically plausible but uncited in the available documents.
- **Proposed Fix:** Either (a) add a citation to a primary source for Electra efficiency (e.g., dossier.md §Driver Technology if it contains the figure, or gap #18 in §S6 "NRL Electra / HAPL KrF efficiency"), or (b) rewrite as "Current KrF laser wall-plug efficiency at kJ scale is typically ~2–5% based on HAPL-era literature [gap #18 — not directly extracted]" to mark it as an unverified-in-sources claim.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-4: Fix H-4 threshold calculation error ($5/target ≠ <10% of $50/MWh LCOE)
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §H-4 (second paragraph), "The threshold: target cost must remain below ~$5/target for the target factory to represent less than ~10% of a $50/MWh LCOE target"; model_setup.py line 399 `flag = " ← viability threshold" if tgt_cost == 5.0`
- **Finding:** At $5/target and the stated plant parameters (0.5 Hz, 85% CF, 400 MWe, 2,978 GWh/yr), the annual target cost is $67M/yr and the LCOE contribution is $22.5/MWh — 45% of a $50/MWh LCOE target, not less than 10%. For less than 10% of $50/MWh (= < $5/MWh), the required target cost is ≤ $1.11/target. The "viability threshold" flag in model_setup.py at $5/target propagates this error into the model output. The adjacent text "within range, but only at the lower end" suggests the author may have been thinking of a different criterion (the Goodin et al. $1–5/target manufacturing threshold), but the written statement is incorrect.
- **Proposed Fix:**
  1. In analysis.md §H-4, change: *"target cost must remain below ~$5/target for the target factory to represent less than ~10% of a $50/MWh LCOE target"* → *"target cost must remain below ~$1/target for the target factory to represent less than ~10% of a $50/MWh LCOE target ($4.5/MWh ÷ $50/MWh = 9%). The Goodin et al. $1–5/target viability criterion is a separate manufacturing-economics threshold; at $5/target, the LCOE contribution is $22.5/MWh (45% of a $50/MWh target), which is not viable."*
  2. In model_setup.py line 399, change viability threshold flag from `tgt_cost == 5.0` to `tgt_cost == 1.0`.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-5: Verify `eta_pin2` behavior when `p_ignition = 0.0`
- **Category:** model-bug (potential)
- **Severity:** minor
- **Location:** model_setup.py lines 172–173 (`eta_pin2=ETA_PIN1, # Same laser train; no separate ignition driver`)
- **Finding:** Setting `eta_pin2 = 0.07` alongside `p_ignition = 0.0` is intended to model a single-beam laser train with no separate ignition pulse. If the 1costingfe framework interprets `eta_pin2` solely as the efficiency of the ignition power circuit and zeros out that circuit when `p_ignition=0.0`, this is correct. If the framework uses `eta_pin2` for any purpose that is independent of `p_ignition` (e.g., a general secondary power circuit), the value 0.07 could silently affect the power balance. The comment documents intent clearly, but the correctness depends on the framework's internal handling.
- **Proposed Fix:** Check 1costingfe documentation or source for the semantics of `eta_pin2` when `p_ignition=0.0`. If the parameter is fully gated by `p_ignition`, no change is needed. If not, set `eta_pin2=1.0` (or the framework's no-op value) and add a comment explaining the choice.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-6: Clarify Phoenix milestone timing (June 2025 vs. "on track for 2026")
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §3, KrF Excimer Laser section: "Xcimer completed the first private-sector electron-beam pumped excimer laser (Phoenix milestone, June 2025)"
- **Finding:** The xcimer-energy-approach.orig.md (extracted 2026-03-07) states "Long Pulse Kinetics (LPK) platform completed early 2025" and "Phoenix on track for completion in 2026." As of March 2026, the full Phoenix laser had not yet completed per this source. The "June 2025" milestone cited in the analysis (from dossier.md) likely refers to the LPK subsystem milestone, not the Phoenix laser system itself. This potential conflation may overstate the maturity of the full laser system.
- **Proposed Fix:** Clarify the description: *"Xcimer completed the Long Pulse Kinetics (LPK) subsystem milestone (early/June 2025) [dossier.md §Driver Technology]; the Phoenix laser system itself was on track for completion in 2026 as of March 2026 [xcimer-energy-approach.orig.md]."* Update TRL assessment commentary if the Phoenix system remains unfinished as of analysis date (2026-03-29).
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 10
- **Citations verified:** 7
- **Citations not found / partial:** 3 (CV-2 partial match/composite quote; CV-9 in notes not primary web extraction; CV-10 uncited claim)
- **Calculations checked:** 9
- **Calculations matched:** 8
- **Calculations mismatched:** 1 (CALC-8: H-4 threshold statement)
- **Model parameters audited:** 10
- **Model parameters with concerns:** 2 (MSA-4 eta_pin2 semantics; MSA-10 untraced chamber radius)
- **Proposed Actions:** 6 (blocking: 0, important: 1, minor: 5)
- **Overall:** HAS ISSUES — one important calculation error (H-4 threshold PA-4), five minor issues (PA-1 through PA-3, PA-5, PA-6)
