# Review: HTS Tokamak - Full HTS

**Iteration:** 1
**Date:** 2026-04-06
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 4 files (energy-singularity-overview.md, energy-singularity-technical-summary.md, pii-s092037962500537x.md, pii-s2211467x25003839.md)

---

## Strategic Assessment

### 1. Modeling Approach

The modeling approach is correct and the CAS mapping choices are defensible. The decision to use CFS ARC/SPARC as a proxy for HH380 is the only viable choice given Energy Singularity's commercial-parameter blackout, and the model is explicit that this is what it's doing. The two structural additions in iter-3 are both analytically sound:

**F-1 (full HTS coil premium):** Correctly placed in C220103 with a named multiplier (×1.1–×1.3 range, base ×1.20). The sensitivity sweep establishes that this uncertainty contributes only ~3–5% LCOE spread across the full ×1.0–×1.3 range — small relative to the structural unknowns — which is the right analytical conclusion and prevents this parameter from being over-weighted. The footnote noting C220103 is ~16% of total capital explains the small sensitivity magnitude.

**F-2 (design-point scenarios):** Scenarios C and D correctly implement discrete design-point bracketing rather than marginal perturbations. The unified 5-scenario LCOE table (84–164 $/MWh range) is the most useful output in the analysis: it simultaneously shows the technical-bet failure band (A/B, +14–22% from base) and the design-point uncertainty band (C/D, −21% to +54% from base), making the sources of LCOE uncertainty visible and distinguishable.

One note: C220104 (ICRH heating system) at $353M is the second-largest CAS22 sub-account. With no heating configuration disclosed for HH380 and P_INPUT held at the 50 MW framework default, this is a hidden assumption. The eta_pin sensitivity is modest (−0.041), but if HH380 uses a different heating modality (e.g., NBI or ECRH) or significantly different power, the heating system cost structure could change. This doesn't warrant a blocking finding — P_INPUT = 50 MW is a reasonable analogue for a Q > 10 machine — but it is an undocumented assumption at the CAS22 sub-account level.

### 2. Strategic Positioning

The analysis correctly identifies the defining differentiator: full HTS (TF + PF + CS all in REBCO) vs. TF-only HTS competitors (CFS, Tokamak Energy). The comparison is correctly framed against the live commercial competitors operating in the same compact high-field regime, not against the LTS/ITER-class baseline, which is the strategically appropriate framing for a cross-concept TEA. The cross-concept notes (Section 7) distinguish the Energy Singularity concept from ST-E1 on all relevant axes: geometry (D-shaped vs. spherical tokamak), coil scope, field level, supply chain, and data availability.

The observation that CFS SPARC/ARC is the most technically relevant comparator — not ST-E1 — is correct and appropriately noted even though 21-spherical-tokamak-hts is the approved prior used for supply chain reuse. The reuse is defensible: REBCO supply chain and tritium fuel cycle constraints apply across all D-T HTS tokamak concepts regardless of geometry. The geometry-specific differences are correctly identified in the divergence list.

The China-domestic supply chain dimension is handled well: positioned as a cost advantage for China-domestic deployment that creates an opaque basis for international comparison, rather than being hand-waved away or treated as uniformly positive.

### 3. Risk and Uncertainty Framing

Risk framing is comprehensive and correctly prioritized. The two concept-specific technical bets — CS coil reliability at 25 T cyclic EM loading, and AI plasma control at burning-plasma conditions — are structurally important to this concept in a way they would not be for other tokamak designs. Both are modeled as explicit scenario branches rather than absorbed into a single base-case assumption, which is the right approach.

TRL assignments are appropriate and conservative: blanket TRL 1–2 (no disclosed concept — correctly lower than the global fusion program baseline of TRL 3–4), full HTS CS coil at 25 T TRL 4–5 (Jingtian proves the physics at 21.7 T but commercial coil reliability is undemonstrated), AI plasma control TRL 5–6 (1,337 s demonstrated on a low-field prototype, not burning plasma). The "data rating: Limited, LCOE carries ±50% or greater uncertainty" statement is prominent and correct.

The regulatory dimension (Section 2, Challenge 6) is appropriately framed: pii-s2211467x25003839 covers international harmonization proposals, not Chinese domestic rules, and the analysis correctly flags gap #12 as partially-sourced and open. The inclusion of this regulatory context — which most TEA analyses omit — is a strength.

Supply chain risk is correctly characterized: REBCO tape cost target (~$10/kA-m commercial vs. ~$30–100/kA-m current) is the shared bottleneck with all HTS tokamak concepts, and the full HTS coil scope creates an incremental demand vs. TF-only HTS designs that is explicitly called out.

### 4. Data Sufficiency

The source coverage is adequate for the claims being made — which is to say, the analysis correctly concludes that adequate sources for LCOE modeling do not exist and cannot be found before HH380 enters the engineering phase (post-2030). The four sources in the dossier are appropriate: two established the factual record (company overview, 1,337-second milestone announcement), one provided peer-reviewed machine parameters for HH70 (the commissioning paper abstract), and one provided regulatory context. The paywalled ScienceDirect commissioning paper is correctly assessed as likely to cover the HH70 experimental machine without commercial design parameters.

The analysis is honest about what the sources cannot provide. The missing parameters table (Section 5) distinguishes blocking/proprietary gaps (commercial parameters that exist but aren't published) from truly-unknown gaps (things not yet decided, like blanket design) from derivable gaps (things calculable once design data exists). This three-way classification is more informative than a flat "data gap" list.

No critical gap is under-reported. The five blocking gaps (net electric, fusion power, Q, thermal efficiency, capital cost for HH380; blanket design; tritium fuel cycle; power conversion cycle; capital cost) are all genuine and correctly classified.

### 5. Cross-Concept Consistency

With no approved prior analyses yet established in this pipeline, this review cannot assess cross-concept numerical consistency for shared parameters (REBCO tape cost, tritium startup inventory, O&M assumptions). The analysis does reference values from 21-spherical-tokamak-hts (REBCO ~$30–100/kA-m, tritium ~$35,000/g, startup ~1 kg) which are consistent with the standard literature. These are the right numbers to use.

The P_CRYO = 8.0 MW choice (vs. framework default 0.5 MW) is a conceptually sound distinction — all coils at 20 K requires a larger unified cryoplant than a partial-HTS design with room-temperature PF/CS — but the ×16 jump from the framework default has no published anchor. The sensitivity elasticity for p_cryo is +0.021 (very low), so this assumption doesn't materially affect the conclusions. However, as approved prior analyses accumulate, a consistent cryoplant sizing methodology across HTS tokamak concepts will be needed to avoid ad-hoc per-concept estimates.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The modeling approach correctly identifies and brackets the two defining structural unknowns (full HTS coil cost premium, HH380 design point) through scenario structure and sensitivity sweeps, uses the most defensible available proxy (CFS ARC/SPARC), and is appropriately explicit about the ±50% uncertainty floor inherent to this concept. Risk framing covers all material risks including supply chain, regulatory, and the concept-specific CS coil reliability and AI control bets. The cross-concept comparison framework is correct. The minor issues noted below do not warrant a stage1 re-run.

---

## Minor Fixes (PROCEED only)

### PA-1: Remove stale file marker from model_setup.py
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py line 1
- **Finding:** `# STALE: analysis-updated-iter-3` appears as the first line of the file. The file's content IS the iter-3 model (it self-describes throughout as "iter-3" and documents the F-1 and F-2 additions). The "STALE" prefix is an artifact from a prior pipeline state and is misleading — it implies the file is outdated when it is the current model.
- **Proposed Fix:** Remove the `# STALE: analysis-updated-iter-3` prefix, leaving the docstring starting at the triple-quote.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Correct availability-impact estimate in scenario structure comment
- **Category:** factual-concern
- **Severity:** minor
- **Location:** model_setup.py lines 261–264 (Scenario A comment block)
- **Finding:** The comment states "LCOE impact vs. base case (80% availability) is approximately +14% on LCOE from the availability drop alone (elasticity ≈ −0.94)." The actual sensitivity output shows elasticity = −0.962; going from 80% to 65% availability is a −18.75% change in the parameter, yielding an expected LCOE increase of ~18% from availability alone. The actual Scenario A LCOE is +21.7% (which includes both the availability drop and the CAS72 penalty). The "+14%" figure appears to be from an earlier iteration's estimate, before the CAS72 penalty and updated elasticity were in place.
- **Proposed Fix:** Update the comment to reflect the actual output: "LCOE impact from availability drop alone: ~+18% (elasticity −0.96 × −18.75%); total Scenario A impact including CAS72 penalty: ~+22% (per model output)."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Document P_INPUT = 50 MW as a hidden heating-system cost assumption
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py §Power balance (P_INPUT comment block); analysis.md §Section 5 Missing Parameters
- **Finding:** C220104 (ICRH heating system) is $353M — the second-largest CAS22 sub-account (19% of CAS22). Its magnitude is driven by P_INPUT = 50 MW, which is the framework default. The current comment notes ICRH is confirmed on HH70 but heating configuration for HH380 is undisclosed. However, neither the analysis.md missing parameters table nor the model_setup.py comment explicitly identifies heating system capital cost (C220104) as an uncertain output driven by an uncertain input. If HH380 uses a different modality (NBI, ECRH) or significantly different power, C220104 could change materially. The sensitivity is modest (eta_pin elasticity −0.041) but C220104 absolute magnitude deserves acknowledgment.
- **Proposed Fix:** Add to analysis.md §Section 5 Missing Parameters table: "Heating system power and type for HH380" as a row with criticality "important" (if not already present — gap #7 covers heating power, but not capital cost implications). Update the P_INPUT model_setup.py comment to note: "C220104 (ICRH capital cost, $353M in base case) scales with P_INPUT; this is the second-largest CAS22 sub-account and carries the same uncertainty as the heating configuration choice."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-4: Flag P_CRYO sizing methodology for future cross-concept alignment
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py lines 170–177 (P_CRYO comment block); analysis.md §Section 7
- **Finding:** P_CRYO = 8.0 MW is a ×16 increase from the mfe_tokamak.yaml default of 0.5 MW, representing a judgment call about full-HTS cryoplant sizing with no published source. The low elasticity (+0.021) means this doesn't affect the conclusions. However, as multiple HTS tokamak concepts accumulate in the pipeline (CFS, Tokamak Energy, Energy Singularity), inconsistent ad-hoc cryoplant sizing across concepts will create a cross-concept inconsistency that is hard to audit later.
- **Proposed Fix:** Add a one-line note in the P_CRYO comment acknowledging that a consistent cross-concept cryoplant sizing methodology is needed and flagging this value as a candidate for alignment once other HTS tokamak analyses are approved: "TODO(cross-concept): align P_CRYO with methodology used in 01-hts-compact-tokamak (CFS) once that analysis is reviewed."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
