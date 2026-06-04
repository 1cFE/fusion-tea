VERDICT: FINDINGS

### F-1: Modeling framework choice not stated
- **Target:** Section 2 (Key Hypotheses or modeling approach preamble)
- **Category:** analysis
- **Finding:** The analysis never states whether 1costingfe or free-form modeling is appropriate for this concept, nor why. The model clearly uses a FOAK-anchored free-form approach (NOAK overnight = FOAK × noak_fraction), but the analysis provides no rationale for this choice. For a concept with a single published cost disclosure and no CAS-level breakdown, this is the right approach — but that reasoning should be explicit. Without it, a reader cannot tell whether the model's central LCOE ($186/MWh) reflects a bottom-up cost build or a top-down scaling from one data point, which changes how the uncertainty range should be interpreted. (Goal 4: Modeling Approach)
- **Recommendation:** Add a short paragraph in Section 2 before the Key Hypotheses stating: (a) the model uses FOAK-anchored free-form modeling because no CAS-level breakdown is available — the only public cost reference is a single FOAK figure; (b) this means the model is testing the FOAK-to-NOAK learning hypothesis rather than validating a bottom-up cost build; (c) the NOAK fraction sweep is therefore the primary modeling contribution, not a secondary sensitivity. One paragraph suffices.
- **Priority:** important

### F-2: Blanket geometry complexity penalty not parameterized in model
- **Target:** Section 5 (Missing Parameters) and model sensitivity sweep
- **Category:** model
- **Finding:** Challenge #3 (3D blanket segment diversity — 80+ unique shapes vs. ~2 for a conventional tokamak) is rated "High" TEA impact and identified as having "no analogue in the tokamak cost literature." Despite this, no parameter exists in Section 5 or the model to capture the fabrication cost premium from this complexity. The model allocates CAS22 as a fixed 65% of NOAK overnight with no internal sensitivity to blanket geometry. This means the concept's most distinctive cost-penalty differentiator is absorbed invisibly into the NOAK fraction sweep — a reader cannot see whether GIGA's blanket penalty is already priced into the NOAK fraction assumption or treated as zero. (Goal 3: TEA Implications; Goal 4: Modeling Approach)
- **Recommendation:** Add a `blanket_complexity_multiplier` to the Section 5 missing parameters table (gap type: truly-unknown, criticality: important). Add a sensitivity sweep in the model over a plausible range — e.g., 1.0–2.5× applied to the blanket sub-component of CAS22, even if CAS22 must be split by assumption (e.g., 40% coil system, 40% blanket/VV, 20% other). This makes the cost risk explicit in the output rather than hidden in an aggregate parameter.
- **Priority:** important

### F-3: CAS-level cost structure absent from cross-concept comparison
- **Target:** Section 7, Comparison 1 (vs. DEMO/ARIES-AT)
- **Category:** analysis
- **Finding:** The Section 7 divergence table has a "TEA Impact" column with qualitative direction but no CAS account references. The analysis identifies divergences with direct CAS implications — no current drive (removes CS magnet from CAS22), scale premium (increases CAS22 coil mass and CAS21 buildings), blanket segment diversity (increases CAS22 blanket sub-accounts), steady-state operation (reduces CAS70 unplanned outage cost) — but none are mapped to CAS accounts. This makes the comparison hard to translate into modeling decisions: which accounts are structurally lower vs. higher for GIGA relative to the reference? (Goal 3: TEA Implications)
- **Recommendation:** Add a CAS column to the Section 7 divergence table. Four mappings suffice: no current drive → CAS22 (no CS, reduced auxiliary heating capital); scale premium → CAS22 (coil system) + CAS21 (buildings); blanket geometry → CAS22 (blanket fabrication sub-accounts); steady-state operation → CAS70 (O&M, reduced unplanned outage).
- **Priority:** minor
