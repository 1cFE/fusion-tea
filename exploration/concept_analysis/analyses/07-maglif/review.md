# Review: MagLIF (D-T)

**Iteration:** 4 (analysis.md reflects iter-6 model updates; source integration through iter-4)
**Date:** 2026-04-06
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 16 files across iter-01 through iter-03, plus iter-04 source integration output

---

## Strategic Assessment

### 1. Modeling Approach

The analysis makes a correct and important judgment call: standard MFE cost frameworks (1costingfe, ARIES, PROCESS) are not applicable to MagLIF, because the three dominant cost categories — pulsed power driver capital, per-shot consumables, and rep-rated chamber clearing — have no analogues in any published MFE cost database. The recommendation in §2 for a "free-form parametric model" treating rep rate, yield per shot, driver capital ($/J), and target cost ($/shot) as the four primary free variables is exactly the right modeling strategy for this concept class.

The tension is that the implementation (model_setup.py) does not execute this recommendation — it remains a 1costingfe MAG_TARGET model with 3 CAS account overrides. The authors are fully aware of this; the script's header and output notes explicitly caveat the limitation, and the sensitivity table is accompanied by a note explaining that the printed elasticities (dominated by availability and construction time) do not represent MagLIF's actual cost drivers. This creates a structurally awkward document: the analysis diagnoses why reference-class tools are wrong, then uses them anyway as a cross-concept comparison scaffold.

This approach is defensible as a placeholder — and the Z-IFE reference comparison validates it (model output 6.75 ¢/kWh vs. Z-IFE published 7.0 ¢/kWh at 0.5 Hz is a reasonable sanity check). The dual-scenario comparison (Scenario A: 1000 MWe Z-IFE reference; Scenario B: 250 MWe Pacific Fusion commercial target) is a high-value addition showing the +85.9% LCOE penalty from economy-of-scale reduction — this is a concrete, actionable finding rather than a hand-waving concern.

CAS mapping choices are defensible: C220104 ($372M LTD driver) is taken directly from the only published plant-level cost study; C220103 ($5M Cu coils) reflects the self-magnetizing target milestone with appropriate uncertainty range; C220109 ($0 DEC) is clearly correct for D-T thermal cycle. Accounts left at framework defaults (C220108 RTL Factory, CAS21 Buildings, CAS70 O&M) are correctly flagged as uncertain placeholders rather than endorsed values.

One meaningful unresolved issue: the per-shot consumable O&M gap is acknowledged in the "CRITICAL UNCERTAINTIES" footer but is not surfaced as a concrete line item in the CAS70 output. The model reports $132.4M/yr O&M for Scenario A; the acknowledged omission (~$15.75M/yr additional at $1/shot × 0.5 Hz, potentially far more for cryo targets) represents a 10–200%+ undercount on the annual operating cost line. A placeholder line with explicit $0 (placeholder) notation — alongside the bounding estimate — would make the gap concrete rather than buried in footer notes.

### 2. Strategic Positioning

The concept's position in the broader landscape is correctly characterized. MagLIF is treated as a structural outlier relative to both MFE and conventional laser IFE: it shares the pulsed architecture with laser IFE but differs on driver efficiency (~90% IMG wall-plug vs. ~10% laser), target tolerances (mm vs. µm), and absence of final optic survivability risk. It shares the capacitor-bank-plus-rep-rate cost structure with Helion (08-frc-w-direct-conversion) but with D-T fuel, a full tritium breeding blanket, and a metallic liner destruction consumable that Helion avoids.

The "no superconducting magnets" differentiator is correctly positioned as a supply chain advantage of first order — eliminating REBCO tape dependency entirely. This is not oversold; the analysis correctly notes FLiBe's own supply chain challenges (BeF₂ toxicity, no industrial-scale production) and shared D-T tritium constraints.

The comparison axis that MagLIF is most unusual on — rep rate as the primary LCOE lever, not capacity factor — is clearly articulated in §1 and §2 and is more than just a qualitative claim: it is supported by the Z-IFE COE spread (0.1 Hz → 20 ¢/kWh, 0.5 Hz → 7 ¢/kWh, 1.0+ Hz → 5 ¢/kWh) that quantifies the sensitivity precisely.

The commercial scale mismatch (250 MWe vs. 1000 MWe Z-IFE reference) is identified as a lower-bound issue for all current COE estimates — exactly right. This is one of the more important findings in the analysis and is placed prominently in §2.

Pacific Fusion's January 2025 framing correction (DS goal is net facility gain Q_facility > 1, not "100× NIF gain" which resolves to Q ≈ 0.7) has been correctly incorporated following iter-4 source integration. The nuance that their stated 100+ MJ from ~80 MJ stored implies Q_facility ≥ 1.25 is a meaningful precision upgrade.

### 3. Risk and Uncertainty Framing

This is the strongest part of the analysis. The six blocking gaps in §6 are not generic hedges — each carries a quantified TEA consequence of failure:

- Rep rate failure (< 0.1 Hz permanent): locks COE at ~20 ¢/kWh, 3–4× above competitive threshold, no path to viable economics
- Target cost failure (> $10/shot cryo): annual consumable O&M at 1 Hz exceeds $300M/yr, rivaling or exceeding annual capital amortization on the driver
- Driver gain scaling failure (10× energy shortfall): driver CapEx scales as TW^0.6, roughly tripling capital cost
- Driver cost failure (> $0.50/J commercial pulsed power): plant CapEx reaches multiple billions regardless of other improvements

The TRL inventory in §3 is graduated and credible. Assigning TRL 2 to tritium breeding blanket (on paper only, no MagLIF-specific design published) and TRL 4–5 to the pulsed power driver/IMG (Z Machine operational decades, TITAN I fired 100+ shots, Pacific Fusion DS documented) correctly captures the asymmetry between physics demonstration and engineering integration. The TRL 3–4 for target physics (χ ≈ 0.1 demonstrated; ignition undemonstrated experimentally; simulation anchored to Z data per arXiv:2504.10680 is the right framing of the current physics basis) is defensible.

One calibration note: the analysis occasionally conflates "things Pacific Fusion says on press releases" with sourced engineering data. The Pacific Fusion DS cost claim ("1/10 NIF cost" = ~$350M) appears in §5 with a "low" confidence tag and "not decomposed" annotation — which is the right treatment, but it still enters the parameter table. The model_setup.py correctly notes this figure as unverifiable. This is correctly handled and does not require remediation.

The economic risk framing for the 250 MWe commercial design point is good: "all published COE figures should be treated as lower bounds" is a strong, clear statement that appropriately flags the structural problem without overstating it.

### 4. Data Sufficiency

Source coverage is genuinely strong for a TRL 3–4 concept. The Z-IFE SAND2006-7148 study (277 KB extracted) provides all the quantitative plant-level anchors. Ellison et al. 2025 (84 KB) is the right community roadmap anchor. The Fuse Energy / Not Boring article (91 KB) provides TITAN I specs at hardware level. The Pacific Fusion interview provides DS facility architecture. The Schmit et al. 2025 (arXiv:2504.10680) paper upgrades the gain physics basis from "pure simulation extrapolation" to "simulation anchored to Z experimental data" — a meaningful precision upgrade captured in iter-03.

The three most critical gaps — IMG driver capital at plant scale, commercially viable cryo target cost, and rep-rated yield demonstration — are correctly tagged as "truly-unknown" or "not-yet-sourced" and "blocking." No amount of additional source search will resolve them from existing literature; they require experimental milestones (Z STAR 2027, Pacific Fusion DS 2030).

The Apeiron I gap resolution (Gap 12) is a model of how source integration should work: claim in Not Boring article was traced to Sandia primary literature (SAND2006-6590, In-Zinerator), parameters confirmed at source (20 MW fusion → 3,000 MWth, 1,280 kg/yr actinide burn), and gap was closed. This level of rigor applied throughout the source integration process.

The analysis is honest about the 20-year age of the Z-IFE study and its LTD vs. IMG architecture mismatch. The statement "No published power plant study exists for the MagLIF + IMG architecture" is accurate and is correctly positioned as a blocking limitation on all COE estimates.

### 5. Cross-Concept Consistency

Section 7 is substantive rather than perfunctory. The parallel to Helion (08-frc-w-direct-conversion) on cost structure — capacitor bank capital and rep rate as the two dominant LCOE levers — is a real cross-concept insight that validates both analyses. The identification of Helion's D-He3 advantage (no blanket, no tritium, electromagnetic energy recovery) as the structural divergence from MagLIF's D-T path is correctly framed.

The D-T fuel cycle cost sharing with tokamaks (01-hts-compact-tokamak, 21-spherical-tokamak-hts) is well-handled: same startup inventory constraint, same TBR > 1 requirement, same Li-6 enrichment dependency, same FLiBe supply chain concerns (beryllium toxicity, Kairos Power development pathway noted). The divergence — MagLIF's thick liquid wall potentially eliminating the periodic first-wall replacement that constrains tokamak capacity factor — is correctly framed as conditional ("if demonstrated") and not assumed in the model.

The laser IFE divergence framing is complete and correct. The five structural differences (driver efficiency, target tolerance, no final optics, lower rep rate target, simpler geometry) are each meaningful for cross-concept cost comparison.

No approved cross-concept analyses are available for full consistency audit of shared subsystem cost estimates — this is expected at this stage of the pipeline. The Section 7 qualitative framing is adequate given this constraint.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The concept's unique cost structure is correctly diagnosed; the impossibility of standard MFE costing tools is properly documented and the resulting implementation is used only as a cross-concept comparison scaffold with explicit caveats. The Z-IFE reference anchoring is the right choice (only published plant-level study for this concept class), the dual-scenario comparison adds real value on the economy-of-scale issue, and the blocking gap inventory with quantified consequence-of-failure reasoning is among the most rigorous in the pipeline. Source integration through iter-4 correctly incorporated the CRADA relationship formalization and net facility gain milestone clarification. Minor documentation inconsistencies do not undermine the analytical conclusions.

---

## Minor Fixes (PROCEED only)

### PA-1: Sensitivity table misleads on MagLIF cost drivers
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py lines 409–434; model_output.txt lines 111–150
- **Finding:** The printed sensitivity table shows `availability` as the dominant elasticity (−0.90) and `construction_time_yr` (+0.25) as the second-largest lever — MFE-style parameters that do not represent MagLIF's actual cost structure. The explanatory note is printed after the table and is easy to miss. A reader focused on the model output may take away that MagLIF economics are most sensitive to availability (analogous to a tokamak) rather than rep rate, target cost, and driver capital.
- **Proposed Fix:** Suppress or clearly demote the sensitivity table in model_output.txt. Add a header before the table (in the print statement) such as: `"WARNING: The following sensitivity table reflects 1costingfe framework gradients and is NOT representative of MagLIF cost drivers. See 'four dominant levers' note below."` Move the "dominant levers" note to appear immediately before the table rather than after it.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: CAS70 O&M undercount should appear as explicit placeholder line
- **Category:** improvement
- **Severity:** minor
- **Location:** model_output.txt lines 47–49; model_setup.py lines 231–235
- **Finding:** Model reports CAS70 O&M at $132.4M/yr for Scenario A. The acknowledged omission — per-shot consumable O&M (~$15.75M/yr at $1/shot × 0.5 Hz; potentially $50–300M+/yr for cryo ice-layer targets) — is listed in the "CRITICAL UNCERTAINTIES" footer but does not appear as a concrete entry in the CAS breakdown. The gap is large enough (10% to >100% of the stated O&M) that it should be surfaced in-line, not only in notes.
- **Proposed Fix:** Add a commented line in the CAS breakdown output: `  CAS70-add  Per-shot consumable O&M (placeholder)    $0 (omitted — est. $15.75M/yr at $1/shot×0.5Hz; cryo targets could be $50-300M+/yr)`. This makes the gap size visible at the point where a reader is scanning costs, rather than requiring them to read the uncertainty footer.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: "STALE" tag on model_setup.py is ambiguous
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py line 1: `# STALE: analysis-updated-iter-6`
- **Finding:** The file header says "STALE: analysis-updated-iter-6" but the docstring says "1costingfe costing model setup (iter-6)" and lists "ITER-6 UPDATES vs. ITER-5" — suggesting the file IS the iter-6 model, not that it is stale relative to iter-6. The tag's meaning is ambiguous: does it mean "stale, was updated at iter-6" or "stale relative to post-iter-6 work"? If there are pending iter-7 changes, the tag should say what they are. If the file is current, the STALE tag should be removed.
- **Proposed Fix:** Remove the `# STALE:` prefix if model_setup.py is current as of iter-6. If there are known pending updates (e.g., to reflect analysis changes not yet modeled), replace with `# TODO (iter-7): [specific pending change]`.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-4: §2 "parametric model required" recommendation is unimplemented — should be positioned as future work
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §2, "Modeling recommendation" paragraph
- **Finding:** §2 concludes "A free-form parametric model is required" but the implementation does not deliver this — it is a 1costingfe-based estimate with 3 CAS overrides. The recommendation is correct but reads as an unfulfilled directive rather than a documented design choice. A future reader of the analysis will not know whether the recommended approach was ever executed.
- **Proposed Fix:** Append a parenthetical to the modeling recommendation: "(The current model_setup.py provides a 1costingfe-based cross-concept comparison scaffold pending development of this parametric model — see model_setup.py header for the rationale and explicit limitations.)" This clarifies that the recommendation is deferred future work, not an oversight.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
