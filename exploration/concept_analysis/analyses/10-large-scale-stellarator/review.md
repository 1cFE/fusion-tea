# Review: Large-Scale Stellarator

**Iteration:** 1
**Date:** 2026-04-06
**Files reviewed:** analysis.md, model_setup.py, model_output.txt, iter-3/feedback.md, iter-3/verdict.json
**Source documents:** 9 files (gauss-fusion-technical-summary.md, helias-reactor-context.md, helias-blanket-studies.md, arxiv-2512-08027v1.md, frontiersin-journals-nuclear-engineering-articles-10-3389.md, gauss-fusion-cdr-review-2026.md, gauss-fusion-partnerships-2025.md, core-outputs-100308302.md, depositonce-bitstreams-39e36af5-b43a-4d14-b7fd-50c4e8b23aea.md)

---

## Strategic Assessment

### 1. Modeling Approach

The FOAK-anchored free-form approach is the correct methodology given the data constraints. There is no published CAS breakdown for GIGA, and fabricating one from allocations invented whole-cloth would create false precision. Anchoring to the single public cost reference (€15–18B FOAK) and testing the NOAK learning hypothesis via a `noak_fraction` sweep is honest and well-suited to the question: the model is correctly positioned as bounding commercial viability conditions rather than estimating cost.

The blanket complexity multiplier — introduced in response to prior assessment feedback (F-2 in iter-2) — is a genuine methodological improvement. Making GIGA's most distinctive cost-penalty differentiator (80+ unique 3D segment shapes vs. ~2 for a tokamak) visible in the output as a named parameter, rather than buried in an aggregate NOAK fraction, is the right choice. The sweep from 1.0× to 2.5× with a defensible central of 1.5× is appropriately conservative.

However, three issues affect the modeling layer's integrity:

**F-1 (blocking):** There is a material inconsistency between the analysis text and the model output. H1 states that a 50–60% NOAK fraction yields "~$100–120/MWh — the threshold for commercial competitiveness," but the NOAK sweep in model_output.txt shows $199.7/MWh at 50% and $212.9/MWh at 55% — roughly 2× the claimed threshold. Even the most optimistic NOAK fraction modeled (40%) produces $173.5/MWh, well above $100/MWh. The Modeling Framework paragraph also contains a stale central estimate of "~$186/MWh" against the model's actual $212.9/MWh. The discrepancy is traceable: H1 appears to have been derived from a capital-cost-only calculation that omitted IDC ($5.1B), indirect costs (CAS30 = $3.2B), and O&M — components that together approximately double the effective capital in the LCOE calculation. As written, H1 leads to an incorrect conclusion about when GIGA becomes commercially viable.

**F-2 (important):** The cryogenic parasitic load is correctly identified in Section 2 and §Section 5 as a GIGA-specific risk — "a lower bound" at 90 MW, likely higher at 18 m scale per the WISTELL-D analog (63.3 MWe at 10.1 m). Yet `p_cryo` appears only as a fixed point in the elasticity table. At the model operating point, the elasticity is +0.0136, which understates the concern because the range of p_cryo for GIGA is not 90 → ~100 MW but potentially 90 → 270–300 MW. The analysis identifies the risk clearly; the model doesn't demonstrate it quantitatively, and the section ends with a claim about net efficiency advantage that the model cannot currently support or refute.

**F-3 (important):** The model's elasticity table places `construction_time_yr` at +0.53 — the third-highest lever after interest rate (+0.93) and availability (−0.89), and higher than every plasma and engineering parameter. IDC already represents $5.1B (28% of total capital) at the central 10-year case. For an 18 m FOAK machine with non-planar coil manufacturing at 3× the scale of any prior project, schedule elongation to 12–18 years is a plausible risk (ITER reference: ~20 years from construction start to first plasma). This risk is entirely absent from Section 2's challenge ranking and from H1–H4.

### 2. Strategic Positioning

The analysis correctly characterizes GIGA's competitive position: the stellarator TEA case is not about inherent cost efficiency but about whether NOAK learning can overcome a large FOAK capital penalty, with operational advantages (steady-state, disruption-free, longer blanket lifetime) providing a modest LCOE offset. This framing is correct, nuanced, and not self-congratulatory about stellarator physics.

The QI vs. QA design-path note (Section 7) is strategically important and well-handled. Making explicit that the non-planar coil complexity, scale premium, and manufacturing challenges are QI-specific (not inherent stellarator constraints) positions GIGA correctly relative to both the Helios/Thea Energy path and conventional tokamaks. The implication — that GIGA's capital cost premium may be a design-choice risk rather than a physics-imposed constraint — is the right framing for cross-concept comparison purposes.

The hypothesis structure (H1–H4) is well-scoped. H4 (scale premium as design-space risk) is the most strategically valuable proposition: it directly tests whether the QI physics argument justifies the capital cost it imposes, and it is not found in the tokamak cost literature. The missing H5 (construction schedule risk) would complete the set.

The comparison tables in Section 7 are structurally clean and identify the right divergences: the current-drive elimination, capacity factor advantage, and disruption-free operation on one side; machine scale, blanket geometry complexity, and coil manufacturing novelty on the other. The net assessment — that the operational advantages are real but bounded, and are smaller in magnitude than the scale penalty at FOAK — is defensible and analytically sound.

### 3. Risk and Uncertainty Framing

The risk inventory is comprehensive and technically credible. Blocking gaps (NOAK cost, blanket type, capacity factor) are correctly designated. The cryogenic parasitic load discussion (Section 2) is notable for being the only analysis in this set that identifies a significant recirculating power component *absent* in tokamak models — this is a genuine insight with quantitative consequence that the model currently undersells.

The TBR/shielding trade-off constraint (from Moreno et al. 2024, via the ParaStell WISTELL-D study) is identified as a structural design risk specific to QI non-planar architectures — another non-obvious finding that is absent in the comparative cost literature. Its inclusion elevates the analysis above a parameter lookup.

Supply chain risks are well-calibrated. The REBCO 26M-meter requirement vs. global production is correctly flagged as an order-of-magnitude gap. Beryllium, EUROFER, and Li₄SiO₄ constraints are correctly tiered as secondary but non-trivial.

The blanket type uncertainty (HCPB vs. DCLL) is rated "blocking" and discussed substantively. The 20–25% LCOE range between HCPB and DCLL thermal efficiencies (35% vs. 40%+) is correctly identified as material, and the two options are distinguished on TBR margin, power cycle type, and supply chain implications.

One risk is understated: the Segment 5 structural failure under accident loads (helias-blanket-studies §6) is identified in Section 3 but not carried forward into the gap inventory's risk rating. This is the only published blanket component that demonstrably fails its design criterion; that it has no published resolution strengthens the TRL 3–4 assessment and arguably should appear in the gap inventory as a named item.

### 4. Data Sufficiency

Data sufficiency is adequate given the constraints imposed by the CDR being behind an access gate. The HELIAS heritage literature (helias-reactor-context.md, helias-blanket-studies.md) substitutes well for CDR-level parameter coverage: plasma geometry, coil mass, blanket segment counts, TBR estimates, and operating conditions are all sourced from peer-reviewed literature on the HELIAS 5-B and HSR4/18 reactor studies, which GIGA explicitly inherits.

The Thea Energy Helios preconceptual design paper (arxiv-2512-08027v1.md) is used with appropriate care — as a capacity factor plausibility anchor, not as a direct analog. The analysis correctly notes the QA/QI distinction and applies a modest downward adjustment for GIGA's more complex maintenance geometry.

The ParaStell WISTELL-D study (frontiersin-journals-nuclear-engineering-articles-10-3389.md) is the highest-quality new source in the research set. It provides the only quantified cryogenic load estimate for a QI non-planar stellarator at reactor scale, and its use here as an analog is well-reasoned and correctly labeled a lower bound.

Gaps that remain unaddressed and are material: (1) the CDR cost structure by CAS account is inaccessible; (2) blanket type selection is proprietary; (3) GIGA-specific O&M cost estimates do not exist in the public literature. All three are documented accurately. The model handles these correctly — by treating them as hypothesis parameters rather than known quantities.

### 5. Cross-Concept Consistency

This is the first review in the set, so consistency can only be assessed against internal logic and against the 21-spherical-tokamak-hts analysis referenced in Section 7.

The reuse of REBCO supply chain assumptions from 21-spherical-tokamak-hts is appropriate and correctly documented. The shared constraint (26M meters HTS superconductor requirement vs. global production) is cited consistently. The Tokamak Energy HTS collaboration with Gauss Fusion — which creates literal supply chain interdependence between the two concept companies — is noted.

Financial parameters (7% interest, 2.45% inflation, 40-year lifetime) and the NOAK modeling framework appear consistent with project conventions. The CAS numbering and cost structure follow the framework schema.

The cross-concept comparison in Section 7 is strategically disciplined: it does not overclaim advantages or understate penalties. The net assessment that GIGA's operational advantages (~10–15% LCOE improvement from capacity factor, a few percent from recirculating power reduction) are smaller than the scale penalty is consistent with what the model output actually shows.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The modeling approach is correctly scoped to the available data, the risk framing is technically credible and above average in identifying GIGA-specific mechanisms (cryogenic load, TBR/shielding coupling, QI vs. QA design-space risk) absent from the comparative literature, and the cross-concept positioning is well-reasoned. The three automated findings (F-1 through F-3) require correction but do not indicate a flawed approach — they are a stale docstring, a missing sensitivity sweep whose parameters are fully specified in the feedback, and a missing text section whose content is derivable from existing model output. None warrant a new research iteration.

---

## Minor Fixes (PROCEED only)

### PA-1: Correct H1 commercial viability threshold and stale central estimate
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §Modeling Framework paragraph; §Key Hypotheses H1; model_setup.py docstring (both root and iter-3/)
- **Finding:** H1 states that 50–60% NOAK fraction yields "~$100–120/MWh — the threshold for commercial competitiveness." The NOAK sweep shows $199.7/MWh at 50% and $212.9/MWh at 55%. The Modeling Framework paragraph also states "~$186/MWh" as the central estimate; the model produces $212.9/MWh. H1 appears derived from a capital-cost-only calculation omitting IDC ($5.1B), CAS30 ($3.2B), and O&M. The model implies GIGA cannot approach $100/MWh through NOAK learning alone at any modeled fraction.
- **Proposed Fix:** Revise H1 to cite the actual model sweep range ($173–252/MWh over 40–70% NOAK fraction) and reframe the competitive threshold: note that $150/MWh requires roughly 40% NOAK fraction plus additional levers (carbon price, lower FCR, value-stacking), and that H1's claim should be restated accordingly. Update the Modeling Framework central estimate to $212.9/MWh. Update model_setup.py docstring to remove "$186/MWh." Remove the "# STALE: analysis-updated-iter-3" marker from root model_setup.py once corrected.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Add cryogenic load sensitivity sweep (Sensitivity 5)
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py — after existing Sensitivity 4 block
- **Finding:** p_cryo is identified in Section 2 and §Section 5 as a GIGA-specific risk with a lower bound of 90 MW. The analysis text states the total recirculating power estimate "may be understated" and explicitly calls 90 MW a lower bound for the 18 m geometry. Yet no sensitivity sweep demonstrates the quantitative consequence. The elasticity at the model operating point (+0.0136) understates the concern because the plausible range is 90–300 MW, not 90–100 MW.
- **Proposed Fix:** Add Sensitivity 5 in model_setup.py: sweep p_cryo from 50 to 300 MW in ~50 MW steps, with WISTELL-D analog (~63 MW) and GIGA lower bound (90 MW) marked. Hold noak_fraction=0.55 and blanket_complexity_multiplier=1.5. Add a brief callout in analysis.md §H2 noting the sweep result and whether the net efficiency advantage over current-drive tokamaks survives at the upper end of the cryogenic load range.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Add construction schedule risk to Section 2 challenge list
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §Section 2; §Key Hypotheses
- **Finding:** The model elasticity for construction_time_yr is +0.53 — third-highest overall, above all plasma and blanket parameters. IDC is already $5.1B (28% of total capital) at the central 10-year assumption. GIGA at 18 m with non-planar coil manufacturing at 3× the scale of any prior project carries real schedule elongation risk; ITER ran ~20 years from construction start to first plasma. Section 2 contains no challenge addressing this, and none of H1–H4 cover schedule risk.
- **Proposed Fix:** Add a brief sub-challenge under §Section 2 Challenge 1 (FOAK Capital Cost) — or as standalone Challenge 7 — noting construction schedule risk: the +0.53 elasticity means each 2-year extension adds roughly $1,000/kWe in IDC; a 14-year schedule vs. the central 10-year assumption adds ~$2,000/kWe (~$2B) in financing cost alone. Optionally add H5: "If construction time exceeds 14 years, IDC growth pushes LCOE above $250/MWh regardless of NOAK fraction." No new model run required — the existing elasticity result and the NOAK sweep output support this claim directly.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
