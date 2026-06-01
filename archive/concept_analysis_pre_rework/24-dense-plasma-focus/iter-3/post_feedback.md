VERDICT: FINDINGS

### F-1: Back-check arithmetic claim contradicts model output
- **Target:** Section 5 (LCOE-Relevant Parameters — "Back-solve to 0.3 cent/kWh" paragraph)
- **Category:** analysis
- **Finding:** The analysis states "the arithmetic works if all assumptions hold," implying LPPFusion's 0.3 ¢/kWh is internally consistent. However, the model's own LPPFusion claim back-check scenario produces 0.64 ¢/kWh — more than 2× the claimed value. The analysis does not explain this gap. The discrepancy exists because LPPFusion's simple back-of-envelope uses only device unit capital ($500K/unit) and ignores buildings, BOP, site costs, indirect costs, and IDC that the CAS-structured model includes. The "arithmetic works" framing is misleading: the arithmetic of device capital only works; the full plant arithmetic does not reproduce the claim.
- **Recommendation:** Revise the back-solve paragraph to note that LPPFusion's 0.3 ¢/kWh omits BOP, site, buildings, and indirect costs. State explicitly that the model's best-effort back-check (same physics assumptions) produces 0.64 ¢/kWh, and identify which cost categories account for the 2× gap. This corrects a factually misleading claim and quantifies what LPPFusion's estimate ignores.
- **Priority:** important

### F-2: Q_sci improvement factor (660,000×) inconsistent with yield improvement narrative (120,000×)
- **Target:** Section 2 (Challenge 1) and model output KEY BINDING CONSTRAINTS block
- **Category:** model
- **Finding:** The analysis narrative consistently uses "120,000× yield improvement" (30 kJ target / 0.25 J current) as the scale of the physics challenge. The model's KEY BINDING CONSTRAINTS output states "Required improvement: 660,000×" for Q_sci. These differ by ~5.5× because the model holds stored energy constant at the current FF-2B 115 kJ while computing Q_sci improvement, whereas LPPFusion's roadmap simultaneously expands the capacitor bank ~16× (per I⁴ scaling), changing stored energy. At 16× higher stored energy, the same 30 kJ target yield represents a much smaller Q_sci improvement. Neither the analysis nor the model explains which framing is correct for modeling purposes or what stored energy the commercial device is assumed to use. This leaves the core challenge scale ambiguous — a 120,000× barrier and a 660,000× barrier carry very different implications for R&D credibility.
- **Recommendation:** The model should explicitly state the assumed commercial stored energy (either current 115 kJ or the roadmap's expanded bank). If 115 kJ is assumed, explain why the 16× bank expansion is excluded from the Q_sci sensitivity sweep. If stored energy scales with the roadmap, update the Q_sci improvement factor and reconcile it with the 120,000× yield narrative in Section 2. Add a note in the model output explaining the relationship between yield improvement and Q_sci improvement when stored energy changes.
- **Priority:** important

### F-3: Conservative scenario parameters undocumented in model output
- **Target:** Model output — SCENARIO COMPARISON block
- **Category:** model
- **Finding:** The scenario table shows "Conservative (FOAK, pessimistic): 533 MWe, 19.10 ¢/kWh" but states no parameter values for this scenario. The conservative case produces 2.67 MWe/module vs. the baseline 5.02 MWe/module — implying either lower Q, lower DEC efficiency, or lower rep-rate than the moderate baseline. Without knowing which parameters define "pessimistic," the 19.10 ¢/kWh figure is uninterpretable: is this driven by DEC η = 0.75 (model shows 11.07 ¢/kWh for that alone), a combination of lower Q and lower DEC efficiency, or something else? Decision-makers reading a 3× range (6.43 → 19.10 ¢/kWh) across FOAK scenarios need to know what drives the spread.
- **Recommendation:** Add a parameter table in the model output for each named scenario (Conservative, Moderate, Optimistic, LPPFusion claim back-check) showing at minimum: Q_sci, DEC efficiency, rep rate, FOAK multiplier, and availability. The conservative scenario should specifically state which parameters are pessimistic relative to the moderate baseline and why those values were chosen.
- **Priority:** important
