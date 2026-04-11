# Review: FRC w/ Direct Conversion

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 5 files (contrary-research-helion.md, docslib-helion-arpa-e-presentation.md, helion-website-technology.md, helion-milestones-feb2026.md, helion-prototype-generations.md)

---

## Citation Verification

### CV-1: "Regular aluminum magnets" — CEO quote; no superconductors
- **Source cited:** contrary-research-helion.md (analysis §S4, model_setup.py docstring)
- **Status:** FOUND
- **Actual text:** `"Regular aluminum magnets" — direct quote from CEO Kirtley`
- **Notes:** Used repeatedly across both files; exact match. Model docstring correctly states "CEO direct quote."

### CV-2: η (=Ed/Eplasma) · Gain = 0.2 · 1.2; η_recovery = 0.7
- **Source cited:** docslib-helion-arpa-e-presentation.md §Energy Efficiency (analysis §S2, model_setup.py comment)
- **Status:** FOUND
- **Actual text:** `"η (=Ed/Eplasma) · Gain = 0.2 · 1.2 with magnetic energy recovery. Magnetic energy recovery efficiency: η=0.7. Input efficiency target: <$0.03/MJ"`
- **Notes:** Exact match, including the <$0.03/MJ target. Correctly quoted in both files.

### CV-3: 50 MW at 2 Hz repetition rate (ARPA-E design point)
- **Source cited:** docslib-helion-arpa-e-presentation.md §Power and Repetition
- **Status:** FOUND
- **Actual text:** `"50 MW at 2 Hz repetition rate (Fusion Engine design point)"`
- **Notes:** Match.

### CV-4: 20 T ARPA-E experiment / 40 T reactor compression field
- **Source cited:** docslib-helion-arpa-e-presentation.md §Magnetic Fields
- **Status:** FOUND
- **Actual text:** `"20 Tesla: ARPA-E experiment compression capability. 40 Tesla: Target reactor compression field."`
- **Notes:** Match.

### CV-5: Formation density 1×10²¹ m⁻³; compressed density 1×10²³ m⁻³; FRC velocity >300 km/s
- **Source cited:** docslib-helion-arpa-e-presentation.md §Plasma Parameters, §Fusion Approach
- **Status:** FOUND
- **Actual text:** `"Formation density: 1E21 m⁻³. Compressed density target: 1E23 m⁻³ deuterium."` / `"FRC velocity: >300 km/s"`
- **Notes:** 100× compression factor stated in analysis is consistent (10²³/10²¹ = 100). Match.

### CV-6: Trenta — ~1 pulse per 10 minutes; Polaris target ~1 Hz
- **Source cited:** helion-website-technology.md §Repetition Rate
- **Status:** FOUND
- **Actual text:** `"Trenta: ~1 pulse per 10 minutes. Polaris target: 1 Hz (one pulse per second)."`
- **Notes:** Match for both values.

### CV-7: Polaris achieved 150M°C (13 keV), first private D-T fusion (January 2026)
- **Source cited:** helion-milestones-feb2026.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** `"Plasma temperature: 150 million degrees Celsius (150M°C) = 13 keV... First privately-funded machine to demonstrate D-T fusion (January 2026)"`
- **Notes:** Exact match. Polaris described as "7th-generation prototype, operational since end of 2024" — consistent with analysis.

### CV-8: Orion — 50 MWe+, Malaga WA, Microsoft PPA, 2028 target
- **Source cited:** helion-milestones-feb2026.md §Orion Specifications
- **Status:** FOUND
- **Actual text:** `"50 MWe or greater after one-year ramp-up period. Location: Chelan County, Washington (land leased from Chelan County PUD)."` And body text: `"Commercial machine: Orion, Malaga, Washington, construction began July 2025"`
- **Notes:** Match. "Malaga, WA" is correct (Malaga is in Chelan County). The "one-year ramp-up period" qualifier appears in analysis §S5 table. Microsoft PPA / 2028 confirmed in both milestones and contrary sources.

### CV-9: DD side reactions — 50% He3 + 50% T; T decays to He3 at t½ = 12.3 yr
- **Source cited:** helion-website-technology.md §Fuel (analysis §S2, §S3, §S4)
- **Status:** FOUND
- **Actual text:** `"DD side reactions produce He3 directly (50%) and tritium (50%) which decays to He3 (t½ = 12.3 yr)"`
- **Notes:** Exact match. Used correctly throughout analysis and model.

### CV-10: D-He3 requires ~200 million degrees C; yields 18.3 MeV (3.6 MeV α + 14.7 MeV p)
- **Source cited:** helion-website-technology.md §Fuel
- **Status:** FOUND
- **Actual text:** `"D-He3 requires ~200 million degrees C. D-He3 reaction yields 18.3 MeV (3.6 MeV alpha + 14.7 MeV proton)"`
- **Notes:** Match. 200M°C ≈ 17.2 keV (conversion verified separately).

### CV-11: D-He3 ~5% neutron energy fraction
- **Source cited:** helion-website-technology.md §Fuel
- **Status:** FOUND (with caveat)
- **Actual text:** `"D-He3 releases 'only 5% of its energy in the form of fast neutrons' (from Wikipedia search snippet)"`
- **Notes:** The source attribute is "(from Wikipedia search snippet)" — the source document is presenting a secondhand figure, not Helion's primary claim. The analysis treats this as a Helion-sourced number. The citation is traceable but the authority is Wikipedia, not Helion directly. The analysis appropriately notes "schema default ~10%" discrepancy.

### CV-12: Capacitor bank >50 MJ, charged to tens of kV; "thousands of high-voltage pulsed capacitors"
- **Source cited:** helion-website-technology.md §Capacitor Bank
- **Status:** FOUND
- **Actual text:** `"Thousands of high-voltage pulsed capacitors. >50 MJ total energy storage. Charged to tens of thousands of volts."`
- **Notes:** Match.

### CV-13: ~720 miles of coaxial cables (copper, aluminum, custom alloys)
- **Source cited:** helion-website-technology.md §Magnets/Coils
- **Status:** FOUND
- **Actual text:** `"Energy carried through coaxial cables with copper, aluminum, and custom-metal alloys (~720 miles total)"`
- **Notes:** Match.

### CV-14: Direct energy recovery efficiency 85–95% (Contrary Research)
- **Source cited:** contrary-research-helion.md §Energy Recovery
- **Status:** FOUND
- **Actual text:** `"Direct electricity capture efficiency: 85-95% without steam turbines"`
- **Notes:** Match. Section header in source file is "### Energy Recovery" — correctly cited.

### CV-15: "Supply chain identified as 'main potential risk'" — Contrary Research
- **Source cited:** contrary-research-helion.md §In-House Manufacturing
- **Status:** FOUND
- **Actual text:** `"Supply chain identified as 'main potential risk'"`
- **Notes:** Match.

### CV-16: Prototype temperature progression — Grande 5 keV, Venti 2 keV, Trenta 8 keV ions
- **Source cited:** helion-prototype-generations.md §Prototype Timeline
- **Status:** FOUND
- **Actual text:** `"Grande: 4 T magnetic compression, cm-scale FRCs, 5 keV plasma temp. Venti: 7 T magnetic fields, 2 keV ion temperature at high density. Trenta: 100M°C (8 keV ions, >1 keV electrons)..."`
- **Notes:** Match. However see CALC-2 note: 100M°C converts to 8.6 keV, not exactly 8 keV. The source itself has an internal inconsistency (8 keV in prototype table vs. "9 keV" in helion-website-technology.md §Plasma Parameters for the same milestone).

### CV-17: Trenta ran 16 months, >10,000 pulses
- **Source cited:** helion-prototype-generations.md and helion-website-technology.md
- **Status:** FOUND
- **Actual text:** helion-prototype-generations.md: `">10,000 pulses over 16 months"`; helion-website-technology.md §Prototypes: `"Trenta — 100M°C, 10,000 pulses, 16 months continuous operation"`
- **Notes:** Match.

### CV-18: Polaris — 3,800 diagnostics, 50 MJ+ bank, 15 T+ target
- **Source cited:** helion-milestones-feb2026.md §Key Technical Details; helion-website-technology.md §Capacitor Bank
- **Status:** FOUND
- **Actual text:** helion-website-technology.md §Prototypes: `"Polaris — 19m long, 50 MJ+ bank, 15 T+, 3,800 diagnostics, 150M°C achieved Feb 2026"`
- **Notes:** Match. The analysis attributes 3,800 diagnostics to helion-milestones-feb2026.md but it appears in helion-website-technology.md §Prototypes — same fact, different source location. Not a factual error.

### CV-19: He3 global supply ~8 kg/year; cost $2,000–$15,000 per NTP liter; $16,000–$120,000/g
- **Source cited:** NOT CITED — no footnote or inline reference for these figures in §S4 Helium-3
- **Status:** NOT FOUND
- **Actual text:** not found in any of the 5 source documents
- **Notes:** The entire He3 supply/price paragraph in §S4 presents specific quantitative claims ($2,000–$15,000/NTP liter, ~8 kg/year, $16,000–$120,000/g) with no citations. These appear to be analyst background knowledge. The conversion: NTP liter of He3 at STP ≈ 0.125 g/L → $2,000/NTP-L ÷ 0.125 g = $16,000/g (matches the stated figure), so the math is internally consistent but the underlying price data has no sourced reference.

### CV-20: "Helion is the best-funded private fusion company in the world"
- **Source cited:** NOT CITED — no footnote in §S1
- **Status:** NOT FOUND
- **Actual text:** not in any source document
- **Notes:** Unsupported superlative claim in §S1 opening paragraph. May be accurate (consistent with known fundraising), but lacks a citation.

### CV-21: >95% round-trip energy recovery for >1 million pulses using IGBTs (2015)
- **Source cited:** dossier.md §Energy Capture (analysis §S2 footnote [8]; §S3; model_setup.py)
- **Status:** NOT IN SCOPE (dossier.md not provided for review)
- **Actual text:** helion-website-technology.md says only "Magnets run at >90% energy efficiency" and "95% of input energy after each pulse must be recovered" (the latter is a design requirement, not a demonstrated result). The specific ">95% for >1M pulses, 2015, IGBTs" claim is not in any of the 5 in-scope sources.
- **Notes:** The claim may be accurate but cannot be verified from the 5 provided source documents. This is the primary performance claim driving eta_th=0.90–0.95 model assumptions.

### CV-22: D-He3 operating temperature "~17–200 keV window" in §S5 parameter table
- **Source cited:** helion-website-technology.md §Fuel
- **Status:** PARTIAL MATCH
- **Actual text:** `"D-He3 requires ~200 million degrees C"` — the source gives only the lower threshold (~17 keV). The "200 keV" upper bound of the stated operating window is not present in any of the 5 source documents.
- **Notes:** 200M°C ≈ 17 keV is correct. The additional claim that the "operating window" extends to 200 keV is an analyst extrapolation (likely from D-He3 cross-section physics or dossier.md). This should be cited or the parameter table should read "~17 keV threshold" rather than "~17–200 keV window."

---

## Calculation Verification

### CALC-1: Trenta rep rate ~0.002 Hz from "~1 pulse per 10 minutes"
- **Claimed:** ~0.002 Hz
- **Re-derived:** 1/(10 min × 60 s/min) = 1/600 s = 0.00167 Hz ≈ 0.002 Hz
- **Status:** MATCH
- **Notes:** Rounding to 0.002 is reasonable.

### CALC-2: 500–1,000× rep-rate gap (Trenta → commercial target)
- **Claimed:** "500–1,000× increase in repetition speed"
- **Re-derived:** 1 Hz / 0.00167 Hz ≈ 600×; 2 Hz / 0.00167 Hz ≈ 1,200×. Using rounded 0.002 Hz: 1/0.002 = 500×; 2/0.002 = 1000×.
- **Status:** MATCH (using rounded Trenta figure)
- **Notes:** The 500–1,000× range is correct as stated against the rounded 0.002 Hz baseline.

### CALC-3: ~10⁹ total shots at 1 Hz over 30 years
- **Claimed:** "~10⁹ total shots" for 30-year lifetime at 1 Hz
- **Re-derived:** 1 Hz × 86,400 s/day × 365 days/yr × 30 yr = 946,080,000 ≈ 10⁹
- **Status:** MATCH
- **Notes:** At 85% availability: 946M × 0.85 = 804M ≈ 10⁹. Order-of-magnitude statement holds either way.

### CALC-4: Polaris bank cost ~$250M at >50 MJ × ~$5/J
- **Claimed:** "$250M for Polaris-class hardware" (analysis §S4, §S2)
- **Re-derived:** 50 × 10⁶ J × $5/J = $250M (minimum; bank is stated as ">50 MJ")
- **Status:** MATCH
- **Notes:** Correctly stated as a lower bound ("implies a bank cost of order $250M").

### CALC-5: 200M°C ≈ 17 keV (D-He3 threshold)
- **Claimed:** "~200M°C (~17 keV)"
- **Re-derived:** 200 × 10⁶ °C ÷ (11.604 × 10⁶ °C/keV) = 17.24 keV ≈ 17 keV
- **Status:** MATCH

### CALC-6: 100M°C ≈ 8 keV (Trenta milestone)
- **Claimed:** "8 keV ions" (analysis uses this throughout)
- **Re-derived:** 100 × 10⁶ °C ÷ 11.604 × 10⁶ = 8.62 keV
- **Status:** MISMATCH (minor)
- **Notes:** 8.62 keV rounds to 9 keV. The analysis consistently uses "8 keV" matching helion-prototype-generations.md. However, helion-website-technology.md §Plasma Parameters says "100 million °C (9 keV)" for the same milestone — which is the accurate rounded conversion. Using "8 keV" slightly understates the achieved temperature. The discrepancy is within the sources (prototype-generations.md says "8 keV"; helion-website-technology.md says "9 keV"). Not a blocking error, but the analysis should acknowledge the source inconsistency or use "~9 keV."

### CALC-7: C220111 installation = $4M at "14% of ~$27M per-module subtotal"
- **Claimed:** `"$4M ... 14% of ~$27M per-module subtotal"` (model_setup.py comment, line 210)
- **Re-derived:** $4M / 0.14 = $28.57M ≠ $27M
- **Status:** MISMATCH (minor arithmetic error in comment)
- **Notes:** The comment says "~$27M" but the math requires ~$28.6M as the base. The $4M value itself may be correct (derived programmatically by the framework at 14% of actual sum), but the comment's stated base is off by ~$1.6M. Does not affect the computed LCOE; it is a documentation inconsistency.

### CALC-8: Capacitor bank implied unit cost — $10M/module vs "$0.50/J or better"
- **Claimed:** `"$10M/module assumes NOAK volume manufacturing at ~$0.50/J or better"` (model_setup.py comment, line 165)
- **Re-derived:** If commercial module bank ≈ 50 MJ (Polaris-scale): $0.50/J × 50 × 10⁶ J = $25M ≠ $10M. For $10M at $0.50/J: bank = 20 MJ. For $10M at 50 MJ: implied price = $0.20/J.
- **Status:** MISMATCH (comment is internally inconsistent)
- **Notes:** Either the commercial module bank is ~20 MJ (not Polaris-scale 50+ MJ), or the implied unit cost is $0.20/J — more aggressive than the stated "$0.50/J" threshold. The comment does not clarify the assumed bank size for a commercial 50 MWe module. This is a key cost driver and the comment's ambiguity makes the $10M figure hard to evaluate. The analysis correctly calls this UNCERTAIN but the stated derivation path doesn't close.

---

## Model Setup Audit

### MSA-1: ConfinementConcept.MAG_TARGET
- **Value:** `ConfinementConcept.MAG_TARGET`
- **Source:** model_setup_prompt.md §Concept Mapping; dhe3_pulsed_frc.py (both out of review scope)
- **Status:** TRACED (to out-of-scope references)
- **Notes:** The rationale — pulsed EM driver, compressed plasma, linear geometry — is explained and defensible. The docstring explicitly states "FRC not natively supported in framework." This is a known approximation with appropriate disclosure. Cannot verify against model_setup_prompt.md.

### MSA-2: fuel=Fuel.DHE3
- **Value:** `Fuel.DHE3`
- **Source:** helion-website-technology.md §Fuel; analysis.md §S3
- **Status:** TRACED
- **Notes:** D-He3 as commercial fuel target is unambiguous across all sources.

### MSA-3: burn_fraction=0.10
- **Value:** 0.10
- **Source:** analysis.md §S2 Challenge 1; docslib-helion-arpa-e-presentation.md §Energy Efficiency; dhe3_pulsed_frc.py
- **Status:** TRACED (partially — ARPA-E source confirmed, 10% derivation from dhe3_pulsed_frc.py out of scope)
- **Notes:** Marked UNCERTAIN in code. The ARPA-E formula (η·Gain = 0.2×1.2) does not directly yield a burn fraction without additional assumptions about plasma composition. The 10% is an engineering analogy from dhe3_pulsed_frc.py. Acknowledged uncertainty is appropriate.

### MSA-4: eta_th=0.90
- **Value:** 0.90
- **Source:** Three in-scope data points: contrary-research-helion.md (85–95%), docslib-helion-arpa-e-presentation.md (η=0.70), helion-website-technology.md (">90% energy efficiency"). One out-of-scope: dossier.md (>95% subscale demo).
- **Status:** TRACED
- **Notes:** The model correctly triangulates three conflicting values and selects the midpoint of the range supported by in-scope sources. The ARPA-E 0.70 is the most credible quantitative measurement (design document with formula); 85–95% from Contrary is a range without test conditions. 0.90 is within the stated range but skews toward optimistic. The selection is disclosed and UNCERTAIN is flagged.

### MSA-5: eta_pin=0.95
- **Value:** 0.95
- **Source:** dossier.md §Energy Capture; analysis.md §S3 (TRL 4-5 for direct energy recovery)
- **Status:** TRACED (to out-of-scope dossier.md)
- **Notes:** 0.95 for modern solid-state IGBT wall-plug efficiency is a reasonable engineering estimate for IGBT switching hardware at subscale. The TRL 4-5 rating in analysis.md §S3 confirms demonstration at subscale. No in-scope source gives a specific eta_pin figure.

### MSA-6: C220103 = $5M/module (aluminum pulsed EM coils)
- **Value:** $5M per module
- **Source:** dhe3_pulsed_frc.py; analysis.md §S4 (Al coils, ~$2–3/kg)
- **Status:** TRACED (partially — primary source dhe3_pulsed_frc.py is out of scope)
- **Notes:** The $5M figure originates from dhe3_pulsed_frc.py baseline. The in-scope support is qualitative (aluminum at commodity pricing; no supply chain constraint). No independent coil mass estimate or detailed cost derivation is in scope to verify.

### MSA-7: C220104 = $10M/module (capacitor bank + IGBT switches)
- **Value:** $10M per module
- **Source:** dhe3_pulsed_frc.py; analysis.md §S4 (cap bank section)
- **Status:** TRACED (partially) — see CALC-8
- **Notes:** See CALC-8. The stated justification ("~$0.50/J or better") does not close at $10M if the commercial module uses a Polaris-scale bank (50+ MJ). Either the commercial bank energy is ~20 MJ or the implied unit cost is $0.20/J — neither is explicitly stated.

### MSA-8: C220108 = $0 (no target factory)
- **Value:** $0
- **Source:** helion-website-technology.md §Technology; analysis.md §S4
- **Status:** TRACED
- **Notes:** In-situ FRC plasmoid formation from gas is consistent with all sources. Correct to eliminate target factory.

### MSA-9: CAS23 = $0 (no steam turbine plant)
- **Value:** $0
- **Source:** handwritten/08-frc-w-direct-conversion.md §Quantitative LCOE Model; analysis.md §S2 Challenge 6
- **Status:** TRACED (source partially out of scope)
- **Notes:** Elimination of steam cycle is unambiguous across all in-scope sources. The $0 override is correct.

### MSA-10: CAS21 = $400M (adjusted buildings)
- **Value:** $400M
- **Source:** costing_constants.yaml building_costs_per_kw; analysis.md §S2 Challenge 6; dhe3_pulsed_frc.py
- **Status:** UNTRACED (all three cited sources are out of scope)
- **Notes:** The $400M figure is entirely sourced to out-of-scope documents. The qualitative reasoning (remove turbine hall, cryogenics building, heat exchanger; add cap bank storage and power electronics hall) is sound and internally consistent with the rest of the model design, but the specific dollar figure cannot be verified from the 5 provided sources.

### MSA-11: p_driver=12.0 MW
- **Value:** 12 MW average per module
- **Source:** dhe3_pulsed_frc.py baseline; docslib-helion-arpa-e-presentation.md §Power and Repetition
- **Status:** TRACED (partially)
- **Notes:** The ARPA-E citation is for "50 MW at 2 Hz" fusion power — not driver power. The 12 MW figure itself comes from dhe3_pulsed_frc.py. The comment says "~12 MJ per pulse → 12 MW average" implying a ~1 Hz rep rate, while the ARPA-E design point is 2 Hz. At 2 Hz with 12 MJ/pulse, average driver power would be 24 MW. The comment conflates two different parameters (ARPA-E design rep rate vs. baseline model rep rate). Marked UNCERTAIN; disclosure is adequate.

### MSA-12: mn=1.0 (no neutron multiplier / no breeding blanket)
- **Value:** 1.0
- **Source:** analysis.md §S4; helion-website-technology.md §Fuel
- **Status:** TRACED
- **Notes:** D-He3 eliminates the tritium breeding blanket unambiguously. Correct.

### MSA-13: p_trit=0.5 MW (tritium monitoring only)
- **Value:** 0.5 MW
- **Source:** analysis.md §S4 (No Tritium Breeding Blanket); helion-website-technology.md §Fuel
- **Status:** TRACED (qualitatively)
- **Notes:** The distinction between "monitoring only" (0.5 MW) vs. full D-T processing (10 MW default) is correctly drawn. The specific 0.5 MW value is not independently sourced — it is a judgment call. But contrast with default is clearly explained.

### MSA-14: blanket_t=0.05 m, ht_shield_t=0.05 m (thin wall, minimal shielding)
- **Value:** 0.05 m / 0.05 m
- **Source:** helion-website-technology.md §Neutron Management; analysis.md §S4
- **Status:** TRACED (qualitatively)
- **Notes:** Source says "~1 m borated poly/concrete at plant boundary" and "similar to hospital particle beam shielding." The 0.05 m in-machine shield is consistent with no breeding blanket and low-energy DD neutrons. The "~1 m at plant boundary" note implies this is a site-boundary parameter, not the per-module shell thickness. The 0.05 m reactor shell value is an engineering judgment not directly derivable from the cited sources.

---

## Consistency Check

**Section 5 parameter table vs. Section 2 narrative:** The parameter table values are consistent with the narrative in all cases checked. The capacitor bank >50 MJ appears correctly in both. The Trenta and Polaris milestones are cited consistently. The ARPA-E energy balance (η×Gain = 0.2×1.2) and the conflicting efficiency values are correctly represented in both §S2 and §S5.

**TRL ratings vs. challenge narrative:** TRL assignments in §S3 are internally coherent with the challenge descriptions in §S2:
- D-He3 Fusion Plasma at TRL 2: consistent with S2 Challenge 3 (undemonstarted at any FRC)
- He3 Self-Breeding at TRL 2–3: consistent with S2 Challenge 4
- Rep-rated FRC at TRL 3–4: consistent with S2 Challenge 2 (500–1000× gap vs. commercial)
- Compression to 40 T at TRL 3: consistent with S2 Challenge 1 (only ~15 T demonstrated on Polaris)
- Direct inductive recovery at TRL 4–5: consistent with S2 Challenge 6 (subscale demo only)
- Pulsed EM coil system at TRL 5–6: consistent with the Polaris functional hardware data

**Model setup vs. analysis §S5 parameter table:**
- eta_th=0.90 is consistent with the three-value range in §S5 (η=0.7, 85-95%, >90%)
- burn_fraction=0.10 is consistent with the §S2 UNCERTAIN characterization
- 50 MWe per module consistent with §S5 (Orion design point)
- p_driver=12 MW is UNCERTAIN with no §S5 cross-check available (not in parameter table)
- blanket_t=0.05 is reasonable given "no blanket" description but §S5 doesn't specify this value

**One inconsistency flagged:** The parameter table in §S5 describes the D-He3 operating temperature as "~200M°C (~17–200 keV window)" but the §S2 narrative correctly says "requires ~200M°C (~17 keV)" as the threshold. The "200 keV" upper bound in the parameter table is inconsistent with the §S2 text and has no in-scope source. This appears to be an unintentional addition in the table (see PA-3).

---

## Proposed Actions

### PA-1: He3 supply and price figures lack citations
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §S4 Helium-3 (paragraphs on global supply and price)
- **Finding:** The specific claims — ~8 kg/year global production, $2,000–$15,000 per NTP liter, $16,000–$120,000/g — appear in the analysis without any footnote or inline citation. None of the 5 source documents contain these figures. The price-to-mass conversion ($2,000/0.125 g = $16,000/g) is internally consistent, so the underlying data is coherent, but the source for the raw figures is not documented.
- **Proposed Fix:** Add a footnote citing the source for He3 pricing and global supply (e.g., US DOE He3 program data, IAEA report, or academic literature). If sourced from background knowledge, mark as "[background: He3 market literature]" or similar.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: "Best-funded private fusion company" lacks a citation
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §S1, opening paragraph
- **Finding:** "Helion Energy is the best-funded private fusion company in the world" is an unqualified superlative with no citation. The statement is plausible given known fundraising rounds (~$2.2B+ total), but is not supported by any of the 5 source documents.
- **Proposed Fix:** Either add a citation (e.g., Fusion Industry Association 2025 report or public fundraising data) or soften to "one of the best-funded private fusion companies."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: D-He3 operating temperature "~17–200 keV window" — upper bound unsourced
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §S5, parameter table, row "Plasma temperature (D-He3 required)"
- **Finding:** The in-scope sources state only "D-He3 requires ~200 million degrees C" (~17 keV). The parameter table extends this to "~17–200 keV window." The "200 keV" upper bound does not appear in any of the 5 source documents. It may derive from D-He3 cross-section peak considerations (~300–500 keV c.o.m.) or from dossier.md — but it is inconsistent with §S2's own text ("requires ~200M°C (~17 keV)") and is not cited.
- **Proposed Fix:** Correct the parameter table to read "~17 keV (threshold per Helion)" or cite the source for "200 keV" explicitly. If the intent is to convey the physics cross-section range (not the operating point), that distinction should be clarified.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: Capacitor bank cost comment is internally inconsistent ($10M vs "$0.50/J or better" at 50 MJ)
- **Category:** model-bug
- **Severity:** important
- **Location:** model_setup.py lines 161–167 (C220104 comment); also model_setup.py line 204 comment
- **Finding:** The comment states "$10M/module assumes NOAK volume manufacturing at ~$0.50/J or better." But at $0.50/J with a Polaris-scale bank (>50 MJ): cost = $25M, not $10M. For the math to reach $10M at $0.50/J, the commercial module bank would need to be ~20 MJ — less than half the Polaris research device's storage. Alternatively, the implied unit cost is $0.20/J ($10M ÷ 50 MJ). Neither of these assumptions is explicitly stated, making the $10M figure non-reproducible from the comment.
- **Proposed Fix:** Clarify one of: (a) the assumed commercial bank energy (e.g., "assuming 20 MJ per commercial module at $0.50/J"), or (b) the actual assumed unit price (e.g., "~$0.20/J NOAK, i.e., 25× reduction from today's $5/J"). Update analysis.md §S4 cross-concept note correspondingly if the bank energy assumption differs from Polaris-scale.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: C220111 installation comment arithmetic error
- **Category:** model-bug
- **Severity:** minor
- **Location:** model_setup.py line 210–211
- **Finding:** Comment reads: "Installation labor (14% of ~$27M per-module subtotal)." But $4M ÷ 0.14 = $28.6M, not $27M. The comment is off by ~$1.6M in the stated base. The $4M value itself is likely computed correctly by the framework; only the explanatory comment is wrong.
- **Proposed Fix:** Update comment to read "14% of ~$29M per-module subtotal" or, better, list the per-module items that sum to the base ($5M coils + $10M cap bank + $3M aux + defaulted values for first wall, shield, structure, vacuum, DEC, remote handling).
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-6: Trenta 8 keV vs. 9 keV — source inconsistency unacknowledged
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §S1, §S2, §S3, §S5 (uses "8 keV" throughout)
- **Finding:** The analysis consistently uses "8 keV ions" for Trenta's 100M°C milestone, citing helion-prototype-generations.md. However, helion-website-technology.md §Plasma Parameters says "100 million °C (9 keV)" for the same milestone. The correct conversion is 100M°C / 11.604 = 8.6 keV, which rounds to 9 keV. Using "8 keV" slightly understates the achieved temperature and creates a minor inconsistency between cited sources.
- **Proposed Fix:** Use "~9 keV" (or "~8.6 keV") to match the accurate conversion and helion-website-technology.md's own figure. Note the minor source discrepancy in a footnote if desired.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-7: CAS21 = $400M is entirely untraced to in-scope sources
- **Category:** model-bug
- **Severity:** minor
- **Location:** model_setup.py line 215–216; model_setup.py docstring CAS21 block (lines 74–78)
- **Finding:** The $400M buildings override is cited to costing_constants.yaml, analysis.md §S2 Challenge 6, and dhe3_pulsed_frc.py. The analysis.md §S2 Challenge 6 discusses the absence of a steam cycle qualitatively but provides no dollar figure. The dollar figure is entirely derived from out-of-scope sources. The qualitative logic is sound, but the specific number cannot be independently evaluated from the 5 provided source documents.
- **Proposed Fix:** This is acceptable given the model relies on dhe3_pulsed_frc.py as a baseline analogue (itself out of scope). Add a note in the model comment that "$400M derives from dhe3_pulsed_frc.py baseline, not from Helion-specific sources, and carries high uncertainty." No in-scope source fix possible; document the dependency.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-8: >95% subscale demo claim (primary efficiency basis) not verifiable from in-scope sources
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §S2 footnote [8]; §S3 TRL 4-5 section; model_setup.py eta_th comment
- **Finding:** The claim "In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs" is cited exclusively to dossier.md §Energy Capture, which is not among the 5 provided source documents. The in-scope sources show: helion-website-technology.md states ">90% energy efficiency" for magnets (not round-trip) and "95% of input energy must be recovered" (a requirement, not a demonstration). The >95% demonstrated result is unchecked.
- **Proposed Fix:** If dossier.md is the canonical research synthesis for this concept, it should be included in future review scope. Alternatively, note in the analysis that the >95% claim derives from a 2015 Helion press release (presumably synthesized into dossier.md) and that the original press release should be cited as the primary source.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 22
- **Citations verified (FOUND or exact match in scope):** 17
- **Citations not found / partial / out-of-scope:** 5 (CV-19 no citation, CV-20 no citation, CV-21 out-of-scope, CV-22 partial, PA-8 out-of-scope)
- **Calculations checked:** 8
- **Calculations matched:** 6
- **Calculations mismatched:** 2 (CALC-6: minor temperature rounding; CALC-8: comment doesn't close)
- **Model parameters audited:** 14
- **Proposed Actions:** 8 (blocking: 0, important: 2, minor: 6)
- **Overall:** HAS ISSUES

**Summary of key findings:**

The analysis is well-researched, the citation network is largely intact, and the model setup is internally coherent with appropriate UNCERTAIN flags on every major assumption. No blocking issues were found. The two important findings are:

1. **(PA-3)** The D-He3 "~17–200 keV operating window" in the §S5 parameter table has no in-scope source for the 200 keV upper bound and contradicts the §S2 text.

2. **(PA-4)** The $10M/module capacitor bank estimate is not derivable from the stated "$0.50/J or better" unit cost at Polaris-scale bank energy; the comment needs to clarify assumed bank size or unit price.

All other findings are minor documentation issues (arithmetic in comments, missing citations for background facts, unacknowledged source inconsistency on Trenta temperature).
