# 1costingfe Model Update: Helical Coil Stellarator

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Stellarator current-drive advantage not distinguished from heating recirculation in cross-concept comparison

- **Target:** Section 7 (Cross-Concept Notes) — Key divergences from the ST-E1 and broader tokamak family
- **Category:** analysis
- **Finding:** The Kovari source explicitly states that stellarators have zero internal power demand for current drive — "A stellarator does not have this issue" — in contrast to tokamaks, which carry both current-drive recirculating power and heating recirculating power. The analysis identifies HESTIA's recirculating power as approximately 50% of gross output (Q_eng = 2.0), and notes ECRH wall-plug (~40 MW) as a dominant component. However, Section 7 does not distinguish that HESTIA's entire recirculating power load is attributable to heating, cryogenics, and BOP — with zero current-drive component. For tokamaks, current drive can consume an additional 10–30% of gross output on top of heating. This is a structural differentiator relevant to Goals 2 and 3: it means HESTIA's Q_eng figure is not directly comparable to tokamak Q_eng figures that must also absorb current-drive losses, and that the recirculating power margin is structured differently even when the headline Q_eng numbers appear similar.
- **Recommendation:** Add a paragraph to Section 7 under the key divergences block noting that stellarators carry zero current-drive recirculating power (confirming the Kovari review). Clarify that HESTIA's Q_eng = 2.0 figure includes ECRH heating (~40 MW wall-plug) and cryogenic/BOP loads but no current-drive term — and that this is why steady-state operation does not carry the same recirculating power structure as current-driven tokamaks. This is relevant when comparing HESTIA's Q_eng to published tokamak Q_eng values; a tokamak at Q_eng = 2.0 pays an additional current-drive cost that HESTIA does not.
- **Priority:** important

---

### F-2: sCO₂ efficiency ceiling anchored to CSP literature rather than fusion-specific review; Kovari "no consistent solution" finding not incorporated

- **Target:** Section 2, Challenge 4 (Novel power conversion — sCO₂ at >50% efficiency — undemonstrated at scale) and Section 3 (sCO₂ Brayton Power Conversion — TRL 3–4)
- **Category:** analysis
- **Finding:** The analysis cites "~40–47% in CSP applications" as the state-of-the-art reference for sCO₂ Brayton efficiency. The Kovari source is a fusion-specific review that independently establishes **47% gross efficiency** for a CO₂ recompression Brayton cycle combined with a Rankine bottoming cycle in a fusion plant design study — confirming the upper bound but in the fusion engineering context rather than CSP. More importantly, the Kovari review concludes that "no fully consistent solution for engineering design, coolant and working cycle" has been found for fusion energy conversion. This is a substantive finding that goes beyond "the specific HESTIA target is undemonstrated" — it characterizes the field-wide state as unresolved. The analysis frames the sCO₂ risk as HESTIA-specific (the concept has set an aggressive target), but the Kovari review indicates the underlying challenge is endemic to fusion energy conversion more broadly. This distinction matters for how the risk is framed in TEA terms (Goal 5): is this a HESTIA-specific execution risk, or a cross-concept design uncertainty that affects all fusion concepts?
- **Recommendation:** In Section 2 Challenge 4, update the efficiency reference to cite the Kovari fusion-specific review (47% for CO₂ recompression + Rankine bottoming in fusion design study) alongside the CSP figures, and note this as the authoritative upper bound from a fusion engineering context. Add one sentence noting that the Kovari review characterizes fusion energy conversion as an unsolved design problem field-wide — framing HESTIA's sCO₂ target as an instance of a cross-concept challenge, not merely a company-specific execution gap. In Section 3, add the Kovari citation to the sCO₂ TRL section's "Demonstrated" block as the reference source for the 47% efficiency ceiling.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: H confinement factor identified as blocking gap but absent from model sensitivity
- **Target:** Model sensitivity sweep (model_setup.py / Key Assumptions §13)
- **Category:** model
- **Finding:** The analysis correctly identifies H=1.3 above ISS04 as a blocking unvalidated
  assumption with "first-order" capital cost impact — a ±30% change in H translates directly
  to machine size and all cost estimates. Yet the model sensitivity table shows zero elasticity
  for every plasma physics parameter (B, T_e, n_e, plasma_volume = 0.0000). Key Assumption §13
  acknowledges this qualitatively ("Not modeled directly; captured as cost lower-bound caveat")
  but provides no quantitative scenario. This is the most important physics risk in the analysis,
  and it is completely invisible in the model output.
- **Recommendation:** Add an H-factor scenario sweep to the model: hold Q=13 constant and scale
  R₀ (or plasma volume) to find the machine size required at H=1.0 vs. H=1.3. For ISS04-class
  scaling, confinement time ∝ R₀^(2.28) × a^(2.28) × B^(0.64) roughly, so the volume penalty
  at H=1.0 is estimable. Run two capital cost scenarios — base (H=1.3) and penalized (H=1.0)
  — and report the LCOE spread. If the framework cannot parameterize H directly, apply a
  multiplicative volume/cost penalty derived from the ISS04 scaling law and flag it as an
  engineering scenario branch.
- **Priority:** blocking

### F-2: sCO₂ threshold failure mode absent from scenario sweep
- **Target:** Model scenario sweep (sCO₂ EFFICIENCY SCENARIO SWEEP section)
- **Category:** model
- **Finding:** The sCO₂ scenario sweep shows only ~$30/MWh LCOE variation ($1158→$1194/MWh)
  across 53%→38% efficiency range, and net electric output stays constant at 70.4 MWe across
  all scenarios. Q_eng is also constant at 1.71 throughout. The model is holding net output
  fixed and adjusting costing — it does not model the physics constraint the analysis correctly
  identifies: below a threshold efficiency, the recirculating power budget cannot close and net
  output approaches zero. The scenario note says "At η_th < ~40%, recirculating power exceeds
  a major fraction of gross output" but does not show the failure point, and the current
  demonstration state (η_th = 20%, kW-scale) does not appear as a scenario at all. The
  resulting flat LCOE response understates the structural risk relative to the analysis
  narrative, which calls sCO₂ efficiency "load-bearing" and "essential."
- **Recommendation:** Extend the scenario sweep to η_th = 0.20 (current demo state) and 0.33
  (steam Rankine fallback). For each scenario, model gross electric and recirculating power
  explicitly as functions of η_th, and report Q_eng as an output variable rather than fixing
  net output. Show the efficiency threshold below which Q_eng < 1.0 (design cannot close).
  This replaces the misleadingly flat LCOE curve with a response that breaks at the threshold,
  consistent with the analysis narrative.
- **Priority:** important

### F-3: Heliotron not positioned against QI stellarator neighbors
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The analysis anchors its cross-concept comparison to 21-spherical-tokamak-hts
  (HTS supply chain) and 20b-renaissance-stellarator (liquid metal wall), but does not
  position HESTIA against its nearest structural neighbors in the stellarator subfamily:
  09-qi-stellarator-hts (Proxima Fusion) and 10-large-scale-stellarator (Gauss Fusion). These
  are the most direct TEA comparators — both are D-T MFE stellarators with HTS coils — but
  they use QI-optimized modular coil topologies rather than the heliotron's two continuous
  helical coils. The analysis notes this distinction ("No other concept in this portfolio uses
  this approach") but does not synthesize the TEA implication: does the heliotron's continuous
  coil architecture produce a cost advantage (fewer joints, simpler system) or penalty (longer
  unbroken REBCO runs, no demountable sections, harder to manufacture at scale) relative to
  QI modular alternatives? Without this comparison the analysis does not answer whether
  heliotron is the low-cost or high-cost path within the stellarator family.
- **Recommendation:** Add a paragraph in Section 7 comparing HESTIA explicitly to 09
  (QI stellarator) and 10 (large-scale QI) on two TEA axes: (1) coil cost structure —
  continuous helical vs. modular coil tape length, joint count, and manufacturing premium;
  (2) scale thesis — HESTIA 70 MWe fleet model vs. Gauss 1+ GWe single-plant model and what
  each implies for specific capital cost trajectory. Conclude with an explicit statement of
  whether the heliotron coil topology is expected to be a cost advantage or penalty relative
  to QI modular designs, and whether this changes the modeling approach for coil cost (C220103).
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-2/model_setup.py`
