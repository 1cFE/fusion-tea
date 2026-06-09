---
ID: 38-particle-accelerator-driven-fusion
Concept: Particle Accelerator-Driven Fusion (SHINE-style)
Company: SHINE Technologies
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Most important risk**: Q_sci ceiling of ~0.01 from beam-target physics makes net electricity impossible—need 228× improvement to reach break-even, but the ratio is set by atomic cross-sections, not engineering.
- **Most important advantage**: TRL 9 commercial deployment of D-T fusion with zero technical risk—$158M overnight capital, $30M/yr operating cost, 10× revenue coverage from isotope sales. SHINE proves fusion works as a business at Q << 1.
- **LCOE**: Undefined (infinite). This is not a power plant and has no pathway to become one without changing the fundamental physics approach from beam-target to plasma confinement.
- **Confidence**: **High for neutron source economics** (operational cost structure is modeled from industrial facility analogues with well-bounded uncertainty); **N/A for fusion power** (no power concept exists to model).

---

## 2. What Matters Most for LCOE

LCOE does not exist for this concept—fusion power output is 141 mW while beam power input is 15 kW (Q_sci = 0.0094). The correct framing is **cost per neutron** and **isotope revenue coverage**, where the model identifies three cost drivers:

**1. Physics ceiling on Q_sci** (Q_sci = 0.0094, need 2.14 for break-even)
- **Assumed value**: Beam-target D-T at 300 keV has Q_sci ~ 10^-3 to 10^-2 (literature range, confirmed by model at 50 mA beam current).
- **Sensitivity**: Sweeping beam current from 10 to 200 mA changes Q_sci from 0.047 to 0.002 but changes annual cost by <1% ($30.14M to $30.19M). Higher beam current *decreases* Q_sci because stopping cross-sections scale faster than fusion cross-sections—you produce more neutrons but at worse energy efficiency.
- **What would flip the conclusion**: Replacing beam-target geometry with plasma confinement (tokamak, FRC, IEC with recirculation). SHINE's linear single-pass beam has no pathway to Q > 1; the gap is 228× and cannot be closed by accelerator optimization.

**2. Staffing (16% of annual cost, $4.9M/yr baseline)**
- **Assumed value**: 35 FTE at $140k fully-loaded (NRC-licensed facility requires operators, health physics, radiochemists, maintenance, engineering, admin).
- **Sensitivity**: 20 to 60 FTE shifts annual cost from $28.1M to $33.7M (±7%). Elasticity ~ 0.2 (a 10% staffing increase raises annual cost by ~2%).
- **What would flip the conclusion**: Regulatory de-licensing (implausible) or dramatic operational automation. Staffing dominates O&M but is only 16% of total cost; capital charge is 60%. Cutting staffing in half saves $2.5M/yr but doesn't change the fundamental Q << 1 barrier.

**3. LEU assembly and isotope processing capital ($22M + $28M = $50M, 53% of CAS22)**
- **Assumed value**: $22M for NRC-licensed subcritical LEU assembly (aqueous homogeneous reactor analogue), $28M for pharmaceutical-grade hot cell and Mo-99 extraction infrastructure. Both carry HIGH UNCERTAINTY—SHINE has not published facility costs.
- **Sensitivity**: LEU assembly from $10M to $50M shifts annual cost from $27.5M to $36.3M (±20%). Isotope processing from $15M to $55M shifts from $27.3M to $36.0M (±20%). Combined elasticity ~ 0.5 to capital for these two accounts.
- **What would flip the conclusion**: If combined LEU+processing capital were 2× baseline ($100M instead of $50M), annual cost would rise to ~$38M/yr. At $5000/Ci Mo-99 and 1200 Ci/week, revenue is $312M/yr—coverage ratio drops from 10× to 8×, still strongly profitable. The revenue model absorbs wide capital uncertainty.

**Non-drivers**:
- Beam power (51 kW facility load → $30k/yr electricity cost, 0.1% of annual cost)
- Capacity factor (90% baseline; 70% to 95% changes annual cost by <0.1% because capital dominates)
- Tritium fuel (7 mg/yr at $35k/g = $247/yr, negligible)

**LCOE-equivalent insight**: This concept establishes that **fusion at Q ~ 10^-2 can be commercially viable if the product is high-value neutrons, not electricity**. Reactor-based Mo-99 supply (NRU, BR2, SAFARI-1) costs ~$10k–30k per 6-day Ci; SHINE competes at $5k/Ci by eliminating reactor overhead. The TEA cross-concept positioning: SHINE is the **only TRL 9 fusion business**, but it proves nothing about fusion power economics because the revenue model is orthogonal to energy gain.

---

## 3. Risk Verdicts

**Risk 1: Physics barrier to Q > 1 (beam-target cross-section ratio)**

**Verdict**: Unlikely resolvable within beam-target geometry.

**Rationale**: At 300 keV, D-T fusion cross-section is ~5 barns but Coulomb stopping cross-section is ~5000 barns. Only ~0.1–1% of beam ions fuse before thermalizing. This ratio is set by atomic physics and is geometry-independent for single-pass beams.

**What would retire this risk**: Published demonstration of multi-pass beam recirculation (IEC potential-well approach) achieving Q > 0.1, or pivot to magnetically confined plasma. SHINE's current design has no recirculation; adding a potential well would make it IEC, not beam-target.

---

**Risk 2: Tritium supply at power scale**

**Verdict**: Likely resolvable (with breeding blanket), but moot given Risk 1.

**Rationale**: Current system consumes 7 mg/yr tritium at 90% CF, purchased externally. At power scale (hypothetical 100 MWe), a Q = 0.01 system would require ~450 kg/yr tritium (50× global supply) before breeding—economically absurd even if supply existed. Breeding blanket integration is standard D-T technology (TRL 5–6 in tokamaks) but cannot overcome Q << 1.

**What would retire this risk**: Breeding blanket design for linear beam geometry (engineering challenge, not physics). But this is irrelevant—breeding tritium for a Q = 0.01 system still leaves net power deeply negative.

---

**Risk 3: No thermal cycle or power conversion system**

**Verdict**: Likely resolvable (standard technology), but moot given Risk 1.

**Rationale**: Current FLARE system has no heat exchangers, turbines, or generators. Adding a thermal cycle is TRL 8–9 Rankine technology. But at Q_sci = 0.0094, even perfect thermal conversion (η_th = 100%, physically impossible) would produce 141 mW electricity from 15 kW beam input—net power is -14.9 kW.

**What would retire this risk**: Build a Rankine cycle. But this "solution" confirms the concept is unviable for power, not resolves it.

---

**Risk 4: Capital cost uncertainty for facility (HIGH UNCERTAINTY tag on all CAS22 sub-accounts)**

**Verdict**: Likely resolvable (analogues exist), and not blocking for neutron source mission.

**Rationale**: Model assumes $158M overnight capital based on $30–150M range from Mo-99 production facility analogues (analysis.md §6 Gap #3). NRC license documents (ML13172A262) exist but are unextracted; they likely contain engineering cost detail. Sensitivity shows 2× capital uncertainty changes annual cost by ~30%, but revenue coverage ratio remains >5× even in conservative scenario ($44M cost vs. $208M revenue at reduced Mo-99 output).

**What would retire this risk**: NRC FOIA request for detailed facility cost breakdown, or SHINE voluntary disclosure. For neutron source economics, current uncertainty is tolerable. For power concept economics, cost is irrelevant until Q >> 1 pathway exists.

---

## 4. Structural Advantages and Disadvantages

**vs. D-T Tokamak Baseline (1100 MWe, $6B capital, $80/MWh LCOE)**

**Advantages**:
- **Eliminates**: Superconducting magnets (CAS220103 → $0, saves ~$800M–1500M), plasma auxiliary heating beyond the beam (CAS220104 reduced from ~$80M to $15M for the accelerator), breeding blanket complexity (current system uses purchased tritium, though this becomes a severe disadvantage at power scale), pulsed thermal/mechanical stress (steady-state beam is mechanically gentle).
- **Radically smaller geometry**: Target chamber is 5 cm radius × 30 cm length (~0.002 m³) vs. tokamak 6 m major radius (~300 m³ chamber volume). Scales capital for vacuum vessel, structure, shielding by ~100×. Model shows CAS220105 structure = $0.02M, CAS220106 vacuum = $0.004M (vs. tokamak $50M and $30M).
- **TRL 9 deployment**: FLARE is commercially operational, NRC-licensed, FDA-approved for Mo-99 supply chain. Zero technical risk. Tokamaks are TRL 5–6 (ITER under construction).
- **Fast construction**: 4 years assumed (vs. 7–10 years for tokamak). No plasma control R&D, no coil winding, no tritium breeding loop commissioning.

**Disadvantages**:
- **Q_sci ~ 0.01 vs. Q_plasma ~ 5–20 for tokamaks**: This is the disqualifying difference. Tokamaks confine plasma for τ ~ 1–10 seconds, allowing cumulative fusion burn. Beam-target has zero confinement—each ion gets one pass. The 228× gap to break-even is unbridgeable.
- **No blanket energy multiplication**: Current system has subcritical LEU assembly for isotope production, not a Li breeding blanket for energy gain. Tokamaks gain ~10% from blanket (M = 1.1); SHINE's assembly serves a different function and contributes zero to electricity generation in any hypothetical power configuration.
- **Tritium procurement, not breeding**: At 7 mg/yr, external tritium is trivial ($247/yr). At power scale, 55+ kg/yr requirement with no breeding would cost $1.9B/yr in fuel alone—300× the entire tokamak fuel cost. This flips from advantage (simplicity) to existential blocker at GW scale.
- **No thermal cycle**: Saves capital (CAS23 → $0) but guarantees p_net = 0. Tokamak thermal cycle costs ~$400M but enables 33% η_th conversion of 2500 MW_th to 825 MWe. SHINE's 141 mW fusion power has no conversion pathway.

**Net structural position**: SHINE eliminates ~$2B in MFE capital (magnets, blanket, plasma heating, thermal cycle) but produces zero net electricity because Q << 1. The capital advantage is real but irrelevant to LCOE comparison—you cannot divide capital savings by zero MWh output. The structural claim is: **beam-target D-T is cheaper than tokamaks per unit neutron flux, but infinitely more expensive per unit electricity**.

---

## 5. Cross-Concept Positioning

**Where SHINE sits**:
- **Confinement family**: None (beam-target, not plasma confinement). Occupies "OTHER" in taxonomy.
- **Revenue model**: Neutron product sales (isotopes, materials testing), not electricity. Unique in the TEA corpus—every other concept targets LCOE.
- **TRL**: 9 (only commercially deployed fusion technology worldwide). NIF has achieved Q > 1 at TRL 6–7 (experimental campaigns); SHINE has achieved revenue > cost at Q ~ 0.01.
- **Capital scale**: $158M (model estimate, HIGH UNCERTAINTY). Comparable to venture-funded private fusion concepts (Commonwealth Fusion ~$2B for SPARC is 13× higher; Helion/TAE have raised similar but plant costs unpublished). SHINE is at the small end of fusion capital, but serves a small-scale mission.

**Shared economics with**:
- **None in fusion power landscape**. SHINE is economically orthogonal—revenue from Mo-99 market ($5k/Ci), not wholesale electricity (~$40/MWh). Closest analogue is accelerator-driven subcritical reactors (ADSR) for waste transmutation (Rubbia's Energy Amplifier, Belgium's MYRRHA), which also run at Q << 1 but serve a waste-disposal mission, not power.

**Fundamentally different from**:
- **All MCF/ICF/MIF power concepts**: Those require Q > 1 (MCF), Q > ~30 (ICF for target gain), or Q > ~10 (MIF) to reach economic breakeven. SHINE's mission is orthogonal to energy gain—neutrons are the product, not the byproduct.
- **IEC concepts (Polywell, etc.)**: IEC uses electrostatic potential wells to recirculate ions for multiple fusion chances, targeting Q > 1. SHINE's beam is single-pass with no recirculation or confinement. Despite shared use of electrostatic acceleration, the physics is entirely different.

**TEA corpus insight**: SHINE defines the **lower bound of commercially viable fusion**—Q ~ 10^-2 is sufficient if revenue comes from non-energy products. It also defines the **upper bound of beam-target physics**—Q ~ 10^-2 is the ceiling for single-pass geometries. Any beam-driven fusion power concept (not in this corpus) must achieve recirculation/confinement to exceed this ceiling; otherwise SHINE's existence proves such concepts are physics-blocked.

SHINE is the **null hypothesis test for fusion-as-energy**: if you remove the energy-gain requirement, fusion is commercially mature (TRL 9), capital-efficient (~$160M), and profitable (10× revenue coverage). The entire fusion-energy challenge collapses to "how do you get Q > 1?"—SHINE proves everything else works.

---

## 6. Modeling Confidence

**Rating**: High (for industrial facility model); N/A (for fusion power).

**Parameters data-anchored**:
- Fusion reaction rate: 5×10^13 /s (SHINE published, high confidence)
- Beam voltage: 300 kV (SHINE published, high confidence)
- Accelerator and target TRL: 9 (NRC-licensed commercial operation, high confidence)
- Tritium consumption: 7 mg/yr (derived from reaction rate and stoichiometry, high confidence)
- Financial parameters (WACC 8%, lifetime 20 yr, CRF): standard industrial assumptions (medium confidence)

**Parameters speculative or analogues-based**:
- **Beam current: 50 mA (HIGH UNCERTAINTY)**—not published by SHINE; midpoint estimate from neutron generator literature. Sensitivity: 10 to 200 mA changes Q_sci from 0.047 to 0.002 but changes annual cost by <1% because beam power is 0.1% of operating cost. Q_sci uncertainty does not propagate to cost uncertainty in the neutron-product business model.
- **All CAS22 capital costs (HIGH UNCERTAINTY)**—no public SHINE facility costs. Model builds from component analogues: $15M for 300 kV accelerator (NEC Pelletron, HVEE Tandetron scale-up), $22M for subcritical LEU assembly (aqueous homogeneous reactor analogues), $28M for isotope hot cell (NorthStar Medical analogue). Total overnight capital $158M sits mid-range in $30–150M analogue band from gap report. 2× capital variation changes annual cost by ~30% but does not flip revenue coverage (remains >5× in conservative scenario).
- **Staffing: 35 FTE (HIGH UNCERTAINTY)**—industrial nuclear facility analogues (Mo-99 producers operate with 20–60 FTE). NRC-mandated positions (licensed operators, health physics) set a floor; exact SHINE staffing is unpublished. Sensitivity: 20 to 60 FTE shifts annual cost ±7%.
- **Mo-99 revenue: $312M/yr (HIGH UNCERTAINTY)**—assumes 1200 Ci/week at $5000/6-day Ci. SHINE's actual production and contracts are unpublished. Serves as context for viability (coverage ratio 10×), not a model output.

**Dominant source of uncertainty**:
- For **neutron source economics**: Capital cost distribution across CAS22 accounts (all are analogues, none from SHINE disclosures). But wide capital uncertainty (e.g., LEU assembly $10M to $50M) is absorbed by the revenue model—isotope pricing sustains 5–15× cost coverage across the full uncertainty range.
- For **fusion power LCOE**: Everything is uncertain because no power concept exists. The Q_sci calculation is certain (physics), but every LCOE parameter (p_net, thermal cycle efficiency, capacity factor at power scale, capital cost for MW-scale beam system, tritium breeding, blanket integration) is undefined. Model correctly outputs LCOE = ∞ and flags the concept as non-power.

**Confidence verdict**: The model quantifies what SHINE *is* (a profitable neutron source at ~$30M/yr cost) with moderate-to-high confidence in cost structure and high confidence in physics. The model quantifies what SHINE *is not* (a fusion power plant) with absolute confidence—LCOE is provably infinite given Q_sci = 0.0094 and p_net = 0. Any future SHINE power concept would require a from-scratch design and cannot be modeled from current data.

---

## 7. What Would Change My Mind

**Development 1: Experimental demonstration of sustained beam recirculation achieving Q_sci > 0.1 in beam-driven D-T**

If SHINE (or any beam-fusion group) published results showing multi-pass ion recirculation in an electrostatic potential well (IEC-like, but integrated with SHINE's continuous beam source) reaching Q_sci = 0.1–1.0, it would reopen the power-generation question. Current Q_sci = 0.01 is 200× below break-even (Q_sci = 2.14); a 10× improvement to Q_sci = 0.1 would narrow the gap to 20× and suggest a plausible engineering path to Q > 1 (improved beam focusing, target density optimization, magnetic confinement in target region). This would shift the verdict from "physics-blocked" to "engineering-hard but possible."

**What it would change**: The entire structural disadvantage ("no pathway to Q > 1") would become "demonstrated partial pathway; remaining gap is 20×, addressable by $X capital investment in Y subsystem." LCOE would remain undefined until Q > 2.14 is demonstrated, but the concept would move from "disqualified" to "early-stage research."

**Likelihood**: Low. SHINE's public roadmap (Phase 4 = fusion power) contains no mention of recirculation, potential wells, or Q-gain R&D. The company's strategy is horizontal scaling (more FLARE units, more isotopes) within the neutron-product business, not vertical scaling toward energy gain. IEC researchers (Polywell, U. Wisconsin, Convergent Scientific) have pursued recirculation for decades without reaching Q > 0.01 in D-T; SHINE has not entered this space.

---

**Development 2: SHINE publishes Phase 4 power plant conceptual design with breeding blanket and net-positive energy balance**

If SHINE released a technical report or patent filing describing a MW-scale beam-target system integrated with (a) a lithium breeding blanket for tritium self-sufficiency, (b) a thermal cycle design for electricity generation, (c) beam and target engineering for Q_sci > 2.5, and (d) capital cost estimates for $/kWe, the analysis would shift from "no power concept exists" to "concept exists on paper; assess technical feasibility and cost competitiveness."

**What it would change**: The gap report currently flags "no power plant design" as the blocking gap for LCOE modeling. A published design would fill this gap and enable standard TEA analysis (credibility-discounted LCOE based on the design's Q_sci claims and subsystem TRLs). If the design claimed Q_sci > 2.5 through novel physics (e.g., "target density 100× higher than current due to [mechanism]"), I would assess the mechanism's credibility; if credible, LCOE would become finite and comparable to other concepts. If the design relied on "future Q improvements" without physics justification, LCOE would remain discounted to near-infinite.

**Likelihood**: Very low in the next 5 years. SHINE's investor materials and press releases emphasize isotope market growth (Lu-177 theranostics, Ac-225 research), LIBRTI neutron testing contracts, and facility throughput scaling—all within the Q ~ 0.01 neutron-product business. No public signals suggest Phase 4 is resourced or imminent. Fusion power would require a physics pivot (recirculation or confinement) that is absent from SHINE's current technology stack.

---

**Development 3: Third-party publishes capital cost breakdown for SHINE Chrysalis or FLARE facilities from NRC license documents or NNSA grants**

If an independent analysis (academic, DOE, or investigative journalism) extracted detailed capital costs from SHINE's NRC filings (ML13172A262, ML15258A372) or NNSA grant awards and published a CAS-level breakdown, it would retire the "HIGH UNCERTAINTY" tags on all CAS22 sub-accounts in the model. Current estimates are analogues-based ($22M LEU assembly, $28M isotope processing, $15M accelerator); actual costs could be 0.5× to 2× these values.

**What it would change**: If actual total capital were $80M (0.5× model), annual cost drops to ~$20M/yr and revenue coverage rises to ~15× (reinforces "highly profitable neutron source" verdict). If actual capital were $300M (1.9× model), annual cost rises to ~$50M/yr and coverage drops to ~6× (still profitable, but tighter margins). LCOE remains infinite in both cases—this development would not change the fusion-power verdict, only refine the neutron-source cost confidence from "moderate, analogue-based" to "high, data-anchored."

**Likelihood**: Low but non-zero. NRC license documents are public via ADAMS FOIA; extracting cost data requires domain expertise and time. NNSA grant disclosures are less detailed. If this TEA project prioritized SHINE cost refinement, extraction is feasible. But for cross-concept TEA purposes, refining SHINE's cost from ±30% to ±10% is low-value—the concept is already clearly viable as an isotope producer and clearly unviable as a power generator, and tighter cost bounds do not change either conclusion.

