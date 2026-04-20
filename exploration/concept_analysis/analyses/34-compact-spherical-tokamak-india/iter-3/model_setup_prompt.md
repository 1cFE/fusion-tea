# 1costingfe Model Update: Compact Spherical Tokamak - India

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: HTS magnet type confirmed — resolves the analysis's largest blocking unknown
- **Target:** Section 1 (Data Availability), Section 2 (Challenge 3), Section 5 (parameter table and missing parameters table), Section 6 (Gap #3)
- **Category:** analysis
- **Finding:** The Pranos Fusion company website (`pranosfusion.md`) explicitly lists "HTS magnets" as one of three core platform technologies alongside PRAGYA and JENGA. The analysis designates magnet type as "proprietary / blocking" — the single largest cost item, "uncharacterized." With this confirmation, the magnet type is no longer unknown; HTS is the company's declared technology path. The Hypothesis 1 scenario branch (HTS vs. resistive copper) remains useful as a sensitivity, but the analysis should no longer frame HTS as an unconfirmed assumption.
- **Recommendation:** In Section 1, add a data point for magnet type = HTS (medium confidence, company website). In the Section 5 parameter table, add a row for magnet type = HTS with source `pranosfusion.md`. Remove magnet type from the Section 5 "missing parameters" table or demote from blocking to important (field strength, coil count, and tape specs remain unknown). Update Challenge 3 in Section 2 to note that HTS is the confirmed path, shifting the framing from "largest cost item uncharacterized" to "HTS confirmed but specifications (field, coil count, tape grade) remain unpublished." Update Gap #3 in Section 6 accordingly. The H1 scenario branch can be retained as a downside sensitivity but should no longer be presented as equiprobable with resistive copper.
- **Priority:** blocking

### F-2: $6.8M funding round reported — material update to company stage and maturity characterization
- **Target:** Section 1 (Data Availability, company funding), Section 7 (maturity gap comparison with Tokamak Energy)
- **Category:** analysis
- **Finding:** The Inc42 article (`inc42-buzz-nuclear-fusion-startup-pranos-fusion-nets-6-8-mn.md`) has a headline stating Pranos Fusion raised $6.8M USD "to fast-track R&D commercialisation." The article body failed to extract (only promotional sidebars were captured), so details — round type, investors, date — are unavailable. However, the headline alone is material: $6.8M is approximately 16× the $417K seed documented in the analysis. The analysis uses the funding gap between Pranos ($417K) and Tokamak Energy ($335M) as evidence that the maturity gap is "approximately 10–15 years" and "multiple orders of magnitude in funding." If the $6.8M round is confirmed, the gap narrows from ~3 orders of magnitude to ~2. The characterization in Section 7 would need adjustment.
- **Recommendation:** In Section 1, add a note that an Inc42 article (April 2026) reports a ~$6.8M funding round; flag that article body extraction failed and full details are unavailable. In Section 8, add the Inc42 article as a new source with a clear caveat about extraction failure and recommend retrieving the full article (URL: `https://inc42.com/buzz/nuclear-fusion-startup-pranos-fusion-nets-6-8-mn-to-fast-track-rd-commercialisation/`). In Section 7, soften the funding gap characterization from "$417K vs. $335M" to "$417K seed (as of May 2025); possible subsequent round of ~$6.8M reported April 2026, unverified." Do not revise the development timeline estimate — funding alone does not close the physics and engineering maturity gap — but remove language that implies the funding gap is static.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Factory learning hypothesis (H2) not implemented in model
- **Target:** model_setup.py — sensitivity sweep for H2
- **Category:** model
- **Finding:** H2 is explicitly labeled "the core economic thesis of the modular fleet concept" and proposes sweeping the learning curve exponent from 0 (no learning) to 0.25 (aggressive learning). The model_setup.py applies `noak=True` as a binary flag but performs no such sweep. The only result shown assumes NOAK learning has already fully occurred — exactly the assumption being tested. Goal 4 requires key hypotheses to be modeled as testable propositions; H2 is currently only an assertion.
- **Recommendation:** Implement H2 as a manual learning curve sweep. Run the model at three levels: (a) FOAK basis (noak=False or an explicit capital multiplier representing unit 1), (b) mid-fleet (approximately unit 250 of 2,500, ~3 doublings of cumulative production), (c) NOAK (current baseline). Report LCOE at each level and identify the break-even production volume at which LCOE crosses a competitive threshold (e.g., $150/MWh). If the framework does not expose a learning exponent directly, apply capital cost multipliers to total capital accounts (e.g., 2.0× FOAK, 1.4× mid-fleet) and re-run. Print results for all three scenarios.
- **Priority:** blocking

### F-2: Recirculating power fraction at 50 MWe is not quantified and contradicts Section 5 estimates
- **Target:** Section 2 (Challenge 1 — scale penalty) and Section 5 (gross thermal and fusion power estimates)
- **Category:** analysis
- **Finding:** Section 5 estimates gross thermal power at 140–200 MW using "50 MWe ÷ 30–35% thermal efficiency," which implicitly assumes zero recirculating power. The model output (fusion power = 369 MW, gross thermal ≈ 406 MW) correctly accounts for recirculating loads totaling ~47 MW (NBI 25 + tritium 8 + cooling 8 + housekeeping 3 + cryo 0.5 + coils 2 + pump 0.5), requiring gross electric ≈ 122 MWe — making recirculating power roughly 59% of gross electric. This 2× underestimate of fusion power in the analysis is a secondary issue; the primary failure is that the analysis never states the recirculating fraction explicitly, even though it is the quantitative mechanism underlying the scale penalty argument in Challenge 1. The model reveals it; the analysis does not interpret it. Goal 3 requires cost implications of key differentiators to be stated; the extreme recirculating fraction is the most important cost implication of the 50 MWe scale choice.
- **Recommendation:** Correct the Section 5 gross thermal and fusion power estimates to account for recirculating loads (gross electric ≈ net + recirculating; gross thermal = gross electric ÷ eta_th). Add a row for gross electric and recirculating fraction. In Section 2 Challenge 1, add an explicit quantitative statement: at 50 MWe net output with assumed recirculating loads, recirculating power is approximately 50–60% of gross electric — far above the ≤25% target typical for large fusion plants — making this concept acutely sensitive to any degradation in heating efficiency or Q. This is the quantitative version of the scale penalty and should be stated directly.
- **Priority:** important

### F-3: Plasma parameters have zero LCOE elasticity — model cannot propagate concept's primary uncertainty
- **Target:** model_setup.py sensitivity sweep
- **Category:** model
- **Finding:** The analysis identifies unknown machine parameters as Challenge 2 (Impact: Critical) — the single most blocking gap. Yet the sensitivity output shows T_e, n_e, B, plasma_volume, q95, Z_eff, tau_ratio, and all disruption parameters at 0.0 elasticity. Plasma physics inputs do not propagate to LCOE. The model derives fusion power from geometry (R0, plasma_t, elon) rather than plasma state, meaning the sensitivity table cannot demonstrate how uncertainty in plasma parameters — the analysis's primary blocking gap — translates to LCOE uncertainty. This was flagged as blocking in the prior assessment pass and remains unaddressed.
- **Recommendation:** Wire magnetic field strength (B or b_max) into the fusion power calculation so that field uncertainty propagates to LCOE. The sensitivity output already shows b_max at +0.36 elasticity, which suggests the pathway exists — confirm that varying B drives fusion power and not just magnet cost. Also verify that the R0 and plasma_t sensitivities (+0.09 each) reflect fusion power scaling, not just geometric cost scaling. If the framework cannot support plasma-parameter-driven fusion power, note this explicitly in the model_setup.py docstring and add a manual scenario where fusion power is varied ±50% to show LCOE sensitivity to the physics uncertainty.
- **Priority:** blocking


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-3/model_setup.py`
