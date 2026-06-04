# Review: HTS Compact Tokamak

**Iteration:** 1
**Date:** 2026-04-05
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 5 files (arc-reactor-specifications.md, sparc-icrf-heating-paper.md, arc-power-conversion-studies.md, cfs-2025-2026-updates.md, osti-etdeweb-servlets-purl-20261446.md)

---

## Strategic Assessment

### 1. Modeling Approach

The analysis makes a defensible and well-reasoned departure from a full structured CAS build. The ARC cost database (Sorbom 2015) covers only three fabricated subsystems — vacuum vessel, blanket, and magnet/structure — and explicitly excludes balance of plant. Attempting a structured CAS breakdown without that foundation would produce false precision. The decision to use three targeted cost overrides (C220103 for REBCO coils, C220104 for LHCD+ICRF heating, CAS27 for FLiBe fill) anchored to published ARC data, with framework defaults filling remaining accounts, is the right call given available information.

The three cost overrides are each correctly sourced and calculated. The REBCO coil computation (5,730 km at 250 A/m, NOAK $50/kAm, 8× manufacturing markup) is traceable to arc-reactor-specifications.md §4.1. The heating split (25 MW LHCD at $4.0M/MW + 13.6 MW ICRF at $4.1494M/MW, no NBI) is consistent with both arc-reactor-specifications.md §5.1 and the SPARC ICRF paper. The FLiBe fill (950 t × $154/kg NOAK) correctly flags the Araiinejad & Shirvan (2025) source and acknowledges the 20% learning rate assumption.

One structural tension exists in the power conversion modeling. The ARC abstract (arc-reactor-specifications.md) specifies a helium Brayton cycle at 46% efficiency for the conservative Pilot phase (1100 K outlet), and notes the FNSF phase uses a Brayton at ~40% efficiency for Pnet = 190 MWe. The model uses 46% net efficiency (eta_th=0.46) from the Colliva et al./power-conversion-studies source, which applied a supercritical Rankine cycle to the FNSF phase with 565°C intermediate FLiBe conditions. These two sources disagree on both cycle type and temperature conditions for the phases they analyze. The analysis acknowledges this complexity and recommends supercritical Rankine, which is defensible as the more recent independent thermodynamic analysis — but the 270 MWe net output modeled does not precisely match either source's calculated outputs (190, 233, or 261 MWe from the ARC paper phases; the Colliva study finds ~297 MWe gross for the FNSF phase at 46% net). This inconsistency is flagged in the model comments but not fully resolved.

The minor radius parameter (plasma_t=1.13 m) correctly uses the machine parameter table value from arc-reactor-specifications.md (Table 6: a = 1.13 m, aspect ratio 3), not the abstract's rounded 1.1 m. This is the right choice and is consistent with the paper's detailed design section.

The identification of the three primary scaling axes — REBCO tape cost ($/kAm), capacity factor (%), and regulatory multiplier (discrete 1.0× vs. 2.2×) — correctly captures the structure of the LCOE uncertainty space for this concept. The capacity factor sweep (50–90%) and REBCO price sweep (NOAK $50/kAm through 6× NOAK at $300/kAm) are appropriately ranged. The REBCO scenarios correctly convert from $/m to $/kAm and show the computation chain transparently.

The ARIES-AT BOP transfer caveat (Section 5) is particularly well-executed. The analysis correctly identifies which CAS accounts transfer cleanly (CAS-20, -21, -24) and which require independent treatment (CAS-22 turbine plant), and articulates *why* — the SiC/PbLi/Brayton vs. FLiBe/Rankine architecture difference. This level of sourcing granularity is appropriate for a first-pass analysis and avoids a common systematic error in tokamak cost modeling.

The FLiBe chemistry plant gap (Gap #15) is correctly flagged as a truly-unknown additive BOP cost with no ARIES analogue. This is an intellectually honest acknowledgment that the analysis cannot close this line item from available sources.

### 2. Strategic Positioning

The cross-concept notes (Section 7) correctly characterize ARC's position in the landscape. The comparison with ST-E1 (concept 21) is the right primary comparator — both HTS REBCO D-T tokamaks, with the key axis being aspect ratio and field strategy. The observation that ARC's $5.56B is magnet-structure-dominated while ST-E1 with lower field trades magnet cost for volume is correct and consequential for cross-concept cost modeling.

The contrast with Helion (concept 08) is handled appropriately: near-zero cost structure overlap, with the shared element being REBCO supply chain for HTS magnets. The cross-referencing with MagLIF (concept 07) on FLiBe shared challenges (MHD, tritium extraction, radiation compatibility) identifies a real research leverage point.

The analysis correctly characterizes the compact HTS high-field strategy as primarily a CAPEX mitigation strategy — not an O&M or regulatory mitigation. This framing holds across all three tokamak-class concepts reviewed so far and will be important for consistent cross-concept positioning in Stage 2.

The "1/3 the cost of ARIES-RS at ~1/4 the output" benchmark from arc-reactor-specifications.md §6 is cited, and the analysis correctly notes this is component-fabricated cost only (excluding BOP, indirect, financing). The inference that a full plant cost would be "substantially higher" per kWe is well-supported. The analysis resists the temptation to take the ARC paper's cost claim at face value, which is the right analytical stance.

One framing gap: the analysis does not address where ARC sits relative to the broader fusion cost landscape in terms of $/kWe. The ARIES-AT benchmark (~5¢/kWh at ~2000–2003 USD for 1,000 MWe) is noted, but the analysis does not draw the implication that ARC, being ~1/4 the output at a disputed fraction of the CAPEX, faces a size-scale LCOE disadvantage that REBCO cost reduction must overcome. This connection is implicit in the sensitivity analysis but could be made more explicit in the strategic framing.

### 3. Risk and Uncertainty Framing

The risk inventory is comprehensive and correctly ranked. The ordering — magnet cost dominance → capacity factor → FLiBe blanket behavior → I-mode extrapolation → LHCD system → regulatory framework → O&M — places the highest-impact items first.

The three testable hypotheses (Section 2) are a structural strength of the analysis. Framing REBCO cost as a necessary condition (Hypothesis 1), capacity factor as the primary LCOE lever (Hypothesis 2), and I-mode as a necessary condition for economic viability — not just physics viability (Hypothesis 3) — organizes the uncertainty space in a way that supports prioritized sensitivity analysis.

The I-mode risk framing is notably sharp. The analysis correctly identifies that if I-mode is not accessible at ARC's design point (0.55 MW/m²/n₂₀ at 9.2 T, above the published I-mode experimental range), net output could drop from ~261 MWe to ~80–100 MWe while capital cost remains essentially fixed — a 2.5–3× $/kWe penalty. This is a risk that most concept analyses in this family miss or understate.

The beryllium supply chain analysis (Section 4) is a valuable addition that most TEA analyses omit. The extrapolation that a 10-plant fleet would require ~3,000 tonnes/year of Be against a current global production of ~300 tonnes/year correctly identifies this as a gating constraint for fleet-scale deployment. However, the 950 tonnes of FLiBe per reactor implies approximately 75 tonnes of Be per reactor (FLiBe is LiF·BeF₂, with Be comprising roughly 8% by weight), not "~300 tonnes/year of Be per plant." This arithmetic warrants a check — the analysis's claim should be verified against the molecular weight fractions.

The tritium supply framing (Section 4) is accurate. The CANDU retirement timeline tension and the "no margin for breeding shortfalls in the early commercial phase" characterization are correct. The TBR ≥ 1.1 (optimizable to ~1.22) value is directly verified in arc-reactor-specifications.md §5.4.

The regulatory risk treatment (Section 2, Challenge 6; Gap #13) correctly flags the NRC 2023 Part 30 decision as favorable but notes that detailed rulemaking is incomplete. The Araiinejad & Shirvan (2025) 2.2× building cost multiplier under Part 50 is cited in the model's unmodeled risk list, and the model correctly applies the Part 30 baseline (no multiplier). Modeling this as a discrete scenario branch rather than a continuous parameter is correct.

One underweighted risk: the demountable TF coil joint technology. The analysis acknowledges this in Section 3 (HTS Magnets subsection) noting that joints were "only bench-top tested at 77 K without background field" as of the 2015 paper. However, the maintenance schedule — which drives capacity factor — depends critically on how fast demountable coil operations can be performed at 23 T peak field conditions with full radiation hardening. This is both a TRL gap and a direct LCOE lever, but it appears in Section 3 without explicit connection to the capacity factor sensitivity in Hypothesis 2.

### 4. Data Sufficiency

The data availability rating of "Rich" is justified for the source domain. The CFS/ARC concept has more peer-reviewed published technical content than any other private fusion concept. The five ingested source documents cover reactor dimensions, magnet specifications, FLiBe blanket design, component-level costs, ICRF physics basis, power conversion thermodynamics, current construction status, and an independent benchmark (ARIES-AT).

The gap inventory (Section 6, 15 items) is thorough and correctly typed (blocking vs. important vs. nice-to-have; proprietary vs. truly-unknown vs. not-yet-sourced). The two blocking gaps — full plant capital cost and capacity factor — are correctly identified and their blocking status is justified. The analysis cannot produce a defensible LCOE point estimate without capacity factor; the model's 80% baseline is explicitly flagged as uncertain.

The analysis is appropriately honest about what the 2015 paper's cost estimate does and does not cover: "While a full costing of the ARC reactor is beyond the scope of this paper..." is quoted directly. The inference that BOP could double-to-triple component cost (per ITER analogues) is the right order-of-magnitude warning, even if imprecise.

A minor data verification note: the analysis consistently cites the REBCO tape requirement as 5,730 km from arc-reactor-specifications.md §4.1. This figure is verified in the source (Table listing TF + PF coil requirements). The critical current of 250 A/m at 20 K, 20 T is cited in the model_setup.py but the source table in arc-reactor-specifications.md appears to list current per unit width rather than per unit length — the exact parameterization (A/m vs. A/m-width vs. kA/m) should be confirmed to ensure the kAm calculation is correct. This is a minor traceability question, not a finding of error.

The ARIES-AT source (osti-etdeweb-servlets-purl-20261446.md) was a gap-filling addition in iter-04. Its integration into the BOP caveat analysis (Section 5) is correctly executed. The analysis correctly notes that the ARIES-AT COE of 5¢/kWh (~$50/MWh) is from approximately 2000–2003 USD and cannot be compared directly to contemporary LCOE estimates without inflation adjustment.

### 5. Cross-Concept Consistency

No prior approved syntheses exist against which to check consistency. Internal consistency across the analysis is strong. The REBCO supply chain analysis in Section 4 is consistent with the magnet cost dominance discussion in Section 2. The capacity factor discussion in Section 2 (Hypothesis 2) is consistent with the sensitivity sweep in model_setup.py. The regulatory multiplier scenario in Section 2 is consistent with its treatment in model_setup.py's unmodeled risks.

The claim that ARC's HTS magnet approach requires REBCO at "~$10/kA-m" for commercial viability is consistent across Sections 2, 4, and the model sensitivity sweep. The model's NOAK baseline at $50/kAm is labeled as the commercial viability threshold — which at 5× the ultimate target ($10/kAm) suggests the model's NOAK baseline is itself optimistic. The analysis acknowledges this implicitly but could make the gap between the $50/kAm model baseline and the $10/kAm ultimate target more explicit in the strategic framing.

The cross-concept Section 7 notes that the ST-E1 analysis (concept 21) uses ARC as an analogue for magnet cost structure. This creates a dependency: if ARC's REBCO cost assumptions are revised, they should propagate to concept 21. This is an appropriate model dependency to flag for the cross-concept consistency check in Stage 2.

The shared D-T tokamak cost structure pattern — CAPEX dominance by magnets + blanket + structure, capacity factor as primary LCOE lever, regulatory cost adder as scenario branch — is correctly identified as spanning all three reviewed tokamak-class concepts (ARC, ST-E1, and implicitly the ARIES benchmarks). This is a sound architectural pattern for Stage 2 cross-concept modeling.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The modeling approach correctly diagnoses the limits of available ARC cost data and responds with a calibrated set of targeted overrides plus framework defaults, rather than false-precision structured costing. The risk inventory is comprehensive, correctly ordered, and framed around testable hypotheses. The cross-concept positioning is coherent. The gap inventory is thorough and honestly typed. The primary structural concerns — power conversion cycle parameter consistency and the Be content arithmetic — are minor corrections that do not alter the strategic conclusions or the LCOE sensitivity structure.

---

## Minor Fixes (PROCEED only)

### PA-1: Power conversion cycle consistency — phase, cycle type, and net output
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §5 (LCOE-Relevant Parameters table, Net electric output row; Modeling Approach sub-section); model_setup.py lines 87–95
- **Finding:** The ARC paper (arc-reactor-specifications.md abstract and §2) specifies a helium Brayton cycle for the FNSF/Pilot phases, with net outputs of 190 MWe (FNSF, 900 K, ~40% Brayton), 233 MWe (conservative Pilot, 1100 K, ~46% Brayton), and 261 MWe (aggressive Pilot, 1200 K). The Colliva et al. / arc-power-conversion-studies.md source applies a supercritical Rankine cycle to the FNSF phase at 565°C intermediate conditions and finds ~297 MWe gross (46% net efficiency). The model uses eta_th=0.46 (from the Rankine study) with net_electric_mw=270 (described as "aggressive pilot rounded up"), but 46% efficiency in the ARC paper corresponds to the conservative Pilot Brayton cycle at 1100 K — not the Rankine analysis of FNSF conditions. The three-way mix of phase, cycle type, and efficiency is not fully reconciled in analysis.md, leaving the power balance basis ambiguous.
- **Proposed Fix:** Add a dedicated reconciliation note in analysis.md §5 (Modeling Approach) that explicitly states: (a) the 2015 ARC paper uses Brayton for efficiency estimates; (b) the Colliva/arc-power-conversion-studies source uses Rankine for the FNSF phase and recommends it as superior; (c) the model adopts the Rankine conclusion (46% net) as the preferred cycle per the independent thermodynamic study, applied to the aggressive Pilot phase output target (270 MWe); (d) the resulting power balance is approximate because the two sources use different intermediate conditions (900 K vs. 565°C). Flag this as a modeling caveat, not an error.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Beryllium content arithmetic in supply chain analysis
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §4, FLiBe supply chain paragraph
- **Finding:** The analysis states "~300 tonnes/year of Be per plant or ~3,000 tonnes/year for a 10-plant fleet." FLiBe (LiF·BeF₂) has molecular weight ~33.0 (Li=6.9, F=19×2=38, Be=9.0, F=19×2=38 → LiF = 25.9, BeF₂ = 47.0, total = 72.9 g/mol). Beryllium fraction by mass = 9.0/72.9 ≈ 12.3%. At 950 tonnes FLiBe per reactor, Be content = ~117 tonnes/reactor, not ~300 tonnes. At a fleet of 10 reactors: ~1,170 tonnes/year of Be, not ~3,000. The conclusion (exceeds global production by a meaningful factor) may still hold depending on fleet ramp rate — current global Be production is ~300 tonnes/year, so 10 plants at ~117 t each would require ~4× current production — but the specific figures cited appear to be overestimates by roughly 2.5×.
- **Proposed Fix:** Recalculate Be content from FLiBe molecular weight fractions: Be = 9.0/(6.9 + 19.0 + 9.0 + 38.0) = 9.0/72.9 ≈ 12.3% by mass. Update the per-plant and fleet-scale Be figures accordingly, and verify whether the "exceeds global production by an order of magnitude" characterization still holds at corrected figures. Retain the qualitative conclusion if supported, but correct the numbers.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Demountable coil joint risk — connection to capacity factor gap
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §3 (HTS Magnets subsection), §2 (Hypothesis 2)
- **Finding:** The demountable TF coil joint technology is correctly identified as a TRL gap in Section 3 (joints bench-top tested at 77 K without background field), but this risk is not explicitly linked to Hypothesis 2 (capacity factor dominance). The ability to replace vacuum vessel modules quickly — the entire strategic argument for demountable coils — depends on joint operations at 23 T peak field under activation conditions being reliably fast. If joint operations take weeks rather than hours, the maintenance schedule advantage evaporates and capacity factor falls. This connection between TRL gap and primary LCOE lever should be made explicit.
- **Proposed Fix:** Add one sentence in the HTS Magnets subsection linking the joint TRL gap to the capacity factor sensitivity: e.g., "Joint reliability and speed of operation under reactor conditions is a prerequisite for ARC's claimed maintenance schedule advantage; if coil exchange takes weeks per event rather than days, the 80% capacity factor baseline is not achievable regardless of other subsystem performance."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-4: REBCO kAm calculation — clarify current density parameterization
- **Category:** factual-concern
- **Severity:** minor
- **Location:** model_setup.py lines 56–62; analysis.md §5 (REBCO tape materials cost row, Notes column)
- **Finding:** The model computes total kAm as (5,730 km × 1,000 m/km) × (250 A/m ÷ 1,000) = 1,432,500 kA-m. The 250 A/m figure is cited as "A/m at 20 K, 20 T" but REBCO tape critical current is typically specified in A/mm-width or A/cm-width (a per-unit-tape-width metric), not A per linear meter of tape length. If 250 is actually 250 A/mm-width, and typical tape width is ~4 mm, then Ic per tape meter ≈ 1,000 A/m-length, and total kAm would be ~5.7 million kAm — a 4× difference. The arc-reactor-specifications.md table specifying this figure should be checked for units. Analysis.md §5 notes column says "250 A/m at 20K, 20T" without unit clarification.
- **Proposed Fix:** Verify the units of the 250 A/m figure against arc-reactor-specifications.md §4.1 (the table or figure that specifies REBCO tape critical current). If the figure is per mm-width, update the kAm computation accordingly and recalculate C220103. Document the unit interpretation explicitly in the model_setup.py comment for this parameter.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
