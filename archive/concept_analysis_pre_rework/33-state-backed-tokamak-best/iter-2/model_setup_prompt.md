# 1costingfe Model Update: State-Backed Tokamak - BEST

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Capacity factor analogue conflicts with CFETR pulsed-operation duty cycle
- **Target:** Section 5 (LCOE-Relevant Parameters — Capacity Factor row) and Section 6 (Gap #5)
- **Category:** model
- **Finding:** The analysis applies a 75–90% capacity factor analogue borrowed from quasi-steady-state D-T MCF designs (Araiinejad & Shirvan). Source 1 (OSTI 1465662) — a CFETR Phase I physics simulation — reports a duty cycle of 0.3–0.5 for the intermediate step in China's roadmap (the "CFEDR" device). A 30–50% duty cycle for CFETR implies a fundamentally different operational regime than the steady-state or quasi-steady-state designs used as analogues. If the PFPP is designed for quasi-steady-state operation (justifying 75–90% CF), this needs to be explicitly argued and distinguished from CFETR's pulsed mode; if the PFPP inherits pulsed characteristics from CFETR, the capacity factor assumption is off by 1.5–3×, which dominates the LCOE.
- **Recommendation:** Update the capacity factor row in Section 5 to include two scenarios: (a) quasi-steady-state PFPP at 75–90% CF (current assumption, needs justification), and (b) pulsed PFPP at 30–50% CF derived from CFETR Phase I duty cycle. Flag which the model's central case assumes and why. Add a sensitivity sweep in model_setup.py over CF = 0.35–0.90.
- **Priority:** blocking

### F-2: CFETR Phase I design point is published — Section 6 gap #1 is not "truly unknown"
- **Target:** Section 5 (Available Parameters table) and Section 6 (Gap #1)
- **Category:** analysis
- **Finding:** The analysis classifies the "CFEDR/PFPP commercial design point" as a "truly-unknown / blocking" gap with no published specification. Source 1 (OSTI 1465662) is a physics simulation paper that establishes CFETR Phase I parameters: R₀ = 5.7 m, B₀ = 5 T, Ip = 10 MA, 200 MW fusion power, duty cycle 0.3–0.5, TBR target > 1.0. This is the intermediate device (the "CFEDR" step in the analysis roadmap) and its parameters are available in the published literature. The gap #1 claim that this design point is "completely unspecified" is incorrect and misleads the reader about how much intermediate-step data exists. Additionally, Source 1 shows that heating scenario matters enormously for Q: NB+EC achieves Q ≈ 2.5 at 200 MW, while the EC+LH-only scenario achieves only Q ≈ 1.2 — a quantified version of the LHCD applicability concern raised in Section 2.
- **Recommendation:** Add CFETR Phase I parameters (R₀ = 5.7 m, B₀ = 5 T, Ip = 10 MA, 200 MW fusion, duty cycle 0.3–0.5) to the Section 5 Available Parameters table with medium confidence, citing the OSTI source. Update Section 6 gap #1 to reflect that CFETR Phase I parameters are published but the commercial PFPP (Phase II / DEMO-class) remains unspecified. Update the LHCD applicability note in Section 2 and gap #7 to include the quantified Q degradation (Q = 1.2 vs. 2.5) when NB is removed.
- **Priority:** important

### F-3: UKAEA cost-scaling paper provides gross-to-net ratios and optimal plant-size range not in the analysis
- **Target:** Section 5 (LCOE-Relevant Parameters — Net electrical output and LCOE rows) and Section 7 (Modeling approach)
- **Category:** model
- **Finding:** Source 2 (the UKAEA extrapolation paper) provides a systematic LCOE-vs-plant-size scan from 100 MW to 2 GW net electric. Key results not present in the analysis: (a) gross-to-net ratio degrades from 42% at 1.2 GW down to 17% at 100 MW net output — recirculating power becomes dominant at smaller sizes; (b) LCOE reductions diminish sharply beyond 1.2 GW net, establishing an economic optimal range of 500 MW – 1.2 GW; (c) blanket fluence allowance (10–20 MW-yr/m²) and HCD wall-plug efficiency are identified as primary cost levers alongside plant size. The analysis's current PFPP output estimate (500–1000 MWe) is reasonable but lacks a cost-scaling basis, and the gross-to-net ratio degradation at modest plant sizes is not captured anywhere — this is directly relevant to whether a first-of-kind Chinese PFPP at ~500 MWe is economically viable.
- **Recommendation:** Add gross-to-net ratio as a parameter row in Section 5 with the UKAEA-derived range (17–42% depending on plant size, low confidence for PFPP). Add a note in Section 7's modeling approach that the optimal plant size range (500 MW – 1.2 GW) from the extrapolation paper supports the current PFPP output assumption and should be cited as the scaling rationale. Add blanket fluence allowance (10–20 MW-yr/m²) as a sensitivity parameter in model_setup.py alongside the existing blanket technology sweep.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Chinese construction cost discount is the central differentiator but is absent from the model
- **Target:** Section 7 (modeling recommendation) and model_setup.py
- **Category:** model
- **Finding:** Section 2 identifies Chinese state cost accounting as "Impact: High" and quantifies a 2–4× construction cost reduction vs. Western analogues. Section 7 explicitly states this discount should be "applied to ARIES/PROCESS baseline." Yet the model output shows "Chinese construction discount: NOT APPLIED." This is the single most important differentiator of the BEST/PFPP concept relative to all other tokamaks in the analysis pipeline — it could reduce LCOE from ~140 $/MWh to ~50–80 $/MWh. A model that omits it cannot test the central economic hypothesis for this concept. The model also omits the regulatory 2.2× factor scenario (NOT APPLIED), which is a second scenario branch called out in the analysis.
- **Recommendation:** Implement Chinese construction cost discount as a scenario parameter in model_setup.py with range [1.0, 2.0, 4.0] (no discount, 2×, 4× reduction). Run LCOE sensitivity on this parameter and report LCOE across the three scenarios. Also implement the regulatory cost factor as a separate scenario axis (Chinese vs. Western). These two together define the PFPP commercial case envelope and are not derivable from the current model output.
- **Priority:** blocking

### F-2: Nearest-neighbor comparison is structurally mismatched — spherical tokamak is not BEST's nearest neighbor
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The analysis uses 21-spherical-tokamak-hts (A ≈ 1.5–1.8, full-HTS, commercial intent) as the sole cross-reference, because it is the only approved analysis. However, BEST has aspect ratio A = 3.27 — a conventional-aspect-ratio tokamak. The nearest neighbors by geometry and magnet technology are 01-hts-compact-tokamak (CFS SPARC-class, compact conventional AR, full-HTS, B₀ = 20 T) and 28-hts-tokamak-full-hts (Energy Singularity, compact conventional AR, full-HTS, B₀ = 25 T). Both are in the concept landscape. The analysis correctly notes divergences from ST-HTS but does not position BEST against these structurally appropriate neighbors — the LTS-vs-HTS capital cost trade-off (the key BEST differentiator) is only resolvable by comparing to full-HTS conventional-AR tokamaks, not to a spherical one. Without this comparison, Goal 1 (nearest-neighbor identification) and Goal 3 (cost advantage of LTS approach) are incompletely addressed.
- **Recommendation:** Add a paragraph in Section 7 positioning BEST against 01-hts-compact-tokamak and 28-hts-tokamak-full-hts as the structurally appropriate nearest neighbors. State explicitly: BEST achieves B₀ = 6.15 T with LTS at larger R₀ vs. ~20–25 T with full-HTS at compact R₀; the central TEA question is whether lower conductor cost/km and Chinese construction economics offset the larger machine volume. Frame this as the comparison axis that differentiates BEST from those two concepts, even though their analyses are not yet approved.
- **Priority:** important

### F-3: Blanket technology scenario branch is unimplemented; key hypotheses are not stated as testable propositions
- **Target:** Section 2, Section 6, and model_setup.py
- **Category:** model
- **Finding:** Section 6 lists blanket technology selection as a blocking gap (Gap 3) and recommends "parametric sensitivity across COOL/WCCB/WCLL assumptions." Section 7 explicitly says blanket technology should be a "sensitivity parameter." However, the model output shows "Blanket technology: DEFAULT (PbLi)" with no scenario variation. The blanket technology choice drives blanket cost (RAFM steel vs. ceramic breeder vs. liquid metal), TBR margin, and power conversion cycle selection — all of which affect LCOE. Additionally, the analysis identifies several key uncertainties (construction discount, blanket, regulatory framework) but never states them as testable hypotheses with predicted LCOE outcomes. Goal 4 (key hypotheses as testable propositions) is unmet.
- **Recommendation:** Implement blanket technology as a model scenario branch with at least two cases: (a) COOL/PbLi coupled to sCO2 at 34.7% efficiency, (b) WCCB/ceramic breeder coupled to steam Rankine at 26.4%. Report LCOE for each case. In the analysis Section 2 or Section 7, restate the top 3 uncertainties as explicit hypotheses, e.g., "H1: If Chinese 2× construction discount holds for fusion, PFPP LCOE drops from ~140 to ~80 $/MWh" and "H2: COOL/sCO2 route achieves ~9% lower LCOE than WCCB/Rankine due to thermal efficiency difference."
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-2/model_setup.py`
