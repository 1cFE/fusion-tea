# Free-Form Model Update: Acoustic ICF / Sonofusion (D-D)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/iter-4/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/iter-4/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: D₂O fuel cost estimate is materially overstated; supply concentration data missing
- **Target:** Section 4 (Materials and Supply Chain) and Section 5 (Parameter Table, D₂O fuel cost row)
- **Category:** model
- **Finding:** The analysis cites D₂O at ~$700/kg sourced by analogy to CANDU industry pricing. The 2023 UN Comtrade data (wits-trade-comtrade source) shows actual global market export prices of $300–$475/kg: India ~$458/kg (100,331 kg exported), Canada ~$474/kg (80,701 kg), Romania ~$301/kg (20,297 kg). The $700/kg figure overstates the fuel cost input by roughly 50–130%. The same source reveals that India and Canada together account for ~$84M of ~$108M in global D₂O exports (roughly 80% supply concentration), a supply chain risk factor the analysis does not mention. This partially addresses data gap #14 (Deuterium fuel cost and supply chain).
- **Recommendation:** Update the D₂O fuel cost row in the Section 5 parameter table from "~$700/kg" to "$300–$475/kg" with source `wits-trade-comtrade-en-country-all-year-2023-tradeflow.md` and confidence "medium." Add one sentence in Section 4 noting that India and Canada account for ~80% of global D₂O exports by value (2023), creating moderate geographic supply concentration risk. Update gap #14 in Section 6 from "nice-to-have" to partially resolved, noting the empirical price range and remaining gap (commercial-scale fusion demand has not been modeled).
- **Priority:** important

### F-2: Transducer electromechanical coupling factor is available from commercial datasheets; driver efficiency floor claim lacks citation
- **Target:** Section 2 (Testable Proposition 3 — Driver efficiency floor) and Section 5 (Parameter Table)
- **Category:** analysis
- **Finding:** Section 2 states that "PZT transducer wall-plug efficiency above ~85% provides minimal further LCOE leverage" without citing a source. The americanpiezo-products-services source provides the first commercial datasheet anchor for this subsystem: APC's Model 90-4040 (28 kHz) specifies electromechanical coupling Kp ≥ 55% and mechanical quality factor Qm = 800; the 50 kHz power transducer specifies resonant resistance ≤ 60Ω. These are the coupling and loss characteristics that bound transducer efficiency. The coupling factor (Kp ~55%) is a material property distinct from wall-plug efficiency, and commercial composite transducers achieve efficiency benefits over single-piece ceramics. The 85% wall-plug efficiency claim as stated is plausible but unsourced, and Kp ≥ 55% is the only datasheet number available — the analysis should not present the 85% figure as though it were established.
- **Recommendation:** In Section 2 (Testable Proposition 3), replace the uncited 85% wall-plug efficiency threshold with a sourced statement: "Commercial PZT transducers at 28–50 kHz have electromechanical coupling Kp ≥ 55% (APC International datasheets); practical wall-plug efficiency is higher but unspecified in open literature." Add a row to the Section 5 parameter table for "Transducer electromechanical coupling (Kp)" with value "≥55%" and source `americanpiezo-products-services-ultrasonic-power-transducers.md`. This anchors the one cited driver efficiency datapoint to a real source rather than an assertion.
- **Priority:** minor

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: STALE marker on model_setup.py unresolved for iter-3
- **Target:** `model_setup.py` line 0
- **Category:** model
- **Finding:** The file begins with `# STALE: analysis-updated-iter-2`, indicating the model was not updated after an analysis revision in iter-2. The docstring only documents "Changes from iter-1," confirming the model is the iter-2 version. We are now generating an iter-3 assessment. If the analysis was updated in iter-2 after the last model run, the `model_output.txt` may not reflect the current analysis parameters. This violates the integrity requirement that model output reflect actual model computations (Goal 4).
- **Recommendation:** Either (a) remove the STALE marker and confirm the model reflects the current analysis state, or (b) update the model to incorporate any analysis changes made in iter-2 that were not propagated to the model, then re-run to regenerate `model_output.txt`. Document what changed and why in the docstring "Changes from iter-2" section.
- **Priority:** important

### F-2: Vessel capital cost omitted from Section 2 sensitivity framing
- **Target:** Section 2 (Conditional LCOE Framing and Testable Propositions)
- **Category:** analysis
- **Finding:** Section 2 correctly identifies plant availability (|ε| = 0.95), WACC (|ε| = 0.94), thermal efficiency (|ε| = 0.75), and Q (|ε| = 0.56) as the top LCOE drivers conditional on physics viability. However, the model's own KEY BINDING CONSTRAINTS section ranks D₂O vessel capital cost as binding constraint #2, and the elasticity table shows vessel_inner_radius_m at |ε| = 0.493 — nearly as elastic as Q. At $700/kg and 113 m³ per module, the D₂O fill alone is ~$87M/module ($348M total), a structural cost floor that does not diminish with higher Q (unlike LCOE per kWh). Section 2's framing implies vessel cost is a testable proposition rather than a binding capital lever, which is inconsistent with the model's own ranking (Goal 3 — TEA implications).
- **Recommendation:** Add vessel inner radius / D₂O capital cost to the Section 2 sensitivity summary with its elasticity value (|ε| = 0.493) and note that unlike availability or WACC, it represents a hard capital floor: a larger vessel improves power density but also raises $/kWe at fixed Q. This is the primary design-space trade-off the model reveals, and it should be stated in Section 2 alongside the other top levers.
- **Priority:** important

### F-3: Tokamak differentiator list not explicitly compiled
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The checklist requires key differentiators from a conventional tokamak to be explicitly listed (Goal 2). The analysis correctly orients comparison toward IFE nearest neighbors (laser ICF, heavy-ion ICF, MTF) rather than MFE, and individual differences are mentioned across Sections 2, 3, 4, and 7. But there is no single compiled list. For a reader working across the full concept portfolio, it is not immediately clear which cost accounts are completely eliminated (C220103 coils → $0, C220104 supplementary heating → $0, C220109 direct energy conversion → $0, no breeding blanket) and which are replaced by acoustic-specific items (C220107 acoustic transducer array). Scattering these facts across sections makes cross-concept comparison harder (Goal 1 — concept positioning).
- **Recommendation:** Add a brief explicit list to Section 7 under a "Differentiators from conventional tokamak" heading: (1) no plasma confinement — acoustic cavitation replaces both the confinement and heating subsystems; (2) no HTS magnets or cryoplant at scale; (3) no tritium breeding blanket; (4) acoustic driver replaces both the magnet coils and the RF/NBI heating. Two to four bullet points with the CAS account mapping is sufficient. This does not require new research — the information is already present in the analysis.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/iter-4/model_setup.py`
