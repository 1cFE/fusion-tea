# Gap Report: Acoustic ICF (Sonofusion)

**Concept:** Acoustic ICF / Sonofusion (D-D)
**Company:** Sonofusion Energy
**Analysis Date:** 2026-03-22
**Synthesis Date:** 2026-06-08

---

## Executive Gap Summary

This concept cannot be analyzed using standard techno-economic methods. The gap is not "missing parameters" — it is an unresolved fundamental physics question. The temperature differential between demonstrated acoustic cavitation (16,000 K) and D-D fusion requirements (100,000,000 K) represents a 6,000× leap with no theoretical pathway in peer-reviewed literature.

**Critical distinction:** This is not a data collection problem. No additional literature search, company disclosure, or analogical engineering estimate can bridge a 4-order-of-magnitude temperature gap. The concept requires experimental physics breakthroughs before any cost parameter becomes meaningful.

The model in `model_setup.py` exists only to test cross-concept comparison infrastructure. All parameters are invented. The 102 MWe "native power" is not extracted from company disclosures — it is a modeling artifact with the same epistemic status as assuming cold fusion works.

---

## Critical Gaps (Blocking All Analysis)

### Gap 1: Fusion Physics Demonstration

**What's missing:** Any credible evidence that acoustic cavitation can achieve thermonuclear fusion.

**Why it's critical:** Until Q > 0 is demonstrated in a laboratory, all downstream parameters (driver efficiency, vessel cost, energy conversion, etc.) are meaningless. This is not a parametric uncertainty — it is a binary viability gate.

**Current evidence:**
- Best demonstrated sonoluminescence temperature: 16,000 K (Flannigan & Suslick 2010)
- D-D fusion requirement: ~100,000,000 K (~10 keV ion temperature)
- Temperature gap: ~6,000× (4 orders of magnitude)
- Taleyarkhan bubble fusion claims (2002): Discredited, research misconduct finding (2008), zero independent replications
- UCLA Putterman group (30+ years expertise): "No fusion neutrons detected — at least 100,000× less than Taleyarkhan claimed"

**What would partially resolve:**
Peer-reviewed experimental demonstration of ion temperatures ≥ 1 million K (100 eV) via acoustic bubble collapse, independently replicated. This would still be 100× short of fusion requirements but would demonstrate access to a new temperature regime and justify further R&D investment.

**What would fully resolve:**
Detection of D-D fusion neutrons (2.45 MeV) or tritium production from acoustic cavitation, with published fusion rate vs. driver power, independently replicated by at least two groups.

**Resolvability:** Unlikely without major physics breakthrough. No theoretical mechanism exists in published literature.

---

### Gap 2: Reactor Design (All Subsystems)

**What's missing:** Any reactor design — conceptual, preliminary, or detailed. No vessel geometry, shielding concept, energy conversion pathway, coolant system, or balance-of-plant specification.

**Why it's critical:** CAS-structured costing requires design-point data. Without a design, no cost account can be estimated beyond analogical placeholders. The model's chamber radius (1.5 m), vessel thickness (0.08 m), and all geometry parameters are invented.

**Current evidence:**
- Company website: References "table-top fusion generators" to "utility-scale reactors" — marketing language with no technical content
- Only published hardware: Impulse Devices historical research reactor (~$250K, 1-foot stainless steel sphere, heavy water fill) — an experimental vessel, not a power plant analogue
- No published design in peer-reviewed literature, patents, or ARPA-E grant proposals

**What would partially resolve:**
Conceptual reactor design whitepaper specifying: vessel geometry, transducer array layout, neutron shielding approach, energy conversion pathway (thermal cycle vs. direct conversion), coolant system, and target net electrical output. Does not require fusion demonstration — can be designed as a conditional architecture.

**What would fully resolve:**
Preliminary engineering design with: material specifications, thermal-hydraulic analysis, neutron transport calculations, structural analysis, and cost basis for major subsystems (driver, vessel, shielding, BOP).

**Resolvability:** In principle solvable — this is an engineering design problem, not a physics blocker. Company has disclosed nothing.

---

### Gap 3: Driver Efficiency at Reactor Scale (η_driver)

**What's missing:** Wall-plug electrical-to-acoustic conversion efficiency for ultrasonic driver systems at 10–100 MW power levels.

**Why it's critical:** Driver efficiency directly determines recirculating power fraction. The model documents |ε(η_driver)| ≈ 0.521 — nearly identical LCOE elasticity to Q_sci (|ε(Q)| ≈ 0.531). If η_driver = 60% rather than the model's assumed 85%, breakeven Q rises from ~3.5 to ~5.2 (a 50% increase). This is a co-equal blocking parameter with fusion gain.

**Current evidence:**
- Commercial PZT transducers: Kp ≥ 55% (planar coupling coefficient — a material/geometry property at resonance, NOT system wall-plug efficiency)
- APC International Model 90-4040 datasheet: Qualitative claim of "high electro-acoustical efficiency" but no numerical wall-plug figure
- Largest commercial ultrasonic unit: 16 kW (Hielscher UIP16000); largest cluster: 64 kW (4 × 16 kW)
- No published wall-plug efficiency data for ultrasonic systems above 64 kW

**What would partially resolve:**
Prototype 1–10 MW ultrasonic driver (no fusion requirement) with documented: electrical input power, thermal losses (driver electronics, transducer heating), and acoustic power delivered into test medium. Measured efficiency curve across operating range (20%–100% power).

**What would fully resolve:**
100 MW driver prototype with validated η_driver ≥ 75% under continuous operation (8,760 hours/year duty cycle representative of baseload power plant). Includes long-term reliability testing (transducer fatigue, thermal management, acoustic coupling stability).

**Resolvability:** Genuinely uncertain. This is an engineering scale-up problem, testable independent of fusion physics. Expensive (~$10M–$50M prototype cost) but not blocked by fundamental physics. No organization has attempted reactor-scale ultrasonic power systems.

---

### Gap 4: Acoustic Power Scale-Up (3 Orders of Magnitude)

**What's missing:** Engineering design for 100 MW acoustic power per module. Physical constraints on transducer array packing, acoustic interference, cavitation threshold, and coherent cavity volume are undefined.

**Why it's critical:** The model assumes 100 MW driver power per module — 1,560× larger than the largest demonstrated ultrasonic system (64 kW). This is not a validated design point; it is a speculative placeholder. Sensitivity analysis shows LCOE varies from 163.3 ¢/kWh (20 MW driver) to 13.0 ¢/kWh (100 MW driver), but Q is likely coupled to driver power.

**Current evidence:**
- Largest commercial system: 64 kW (Hielscher 4 × UIP16000 cluster)
- UCLA single-bubble sonoluminescence: ~kW-scale acoustic input (not disclosed precisely)
- No published reactor-scale transducer array design, packing analysis, or thermal management approach

**Physical constraints requiring analysis:**
1. **Acoustic cavity volume:** Maximum liquid volume over which coherent standing-wave cavitation can be sustained
2. **Transducer packing density:** Fraction of vessel surface area that can be covered with actively driven transducers, constrained by mechanical resonance coupling and thermal dissipation
3. **Cavitation threshold:** Minimum acoustic pressure amplitude (Blake threshold) for bubble nucleation — limits spatial uniformity of cavitation field
4. **Acoustic interference:** Large transducer arrays produce standing wave patterns with nodes/antinodes — locally suppress or enhance cavitation intensity; may create "dead zones" with no fusion

**What would partially resolve:**
Engineering analysis (finite element acoustic modeling) of transducer array geometry, acoustic field uniformity, and thermal management for 10 MW acoustic power into a 1–2 m spherical chamber. Does not require fusion — can be validated with bubble collapse imaging and acoustic field mapping.

**What would fully resolve:**
10 MW acoustic driver prototype operating into a test chamber (water or D₂O), with measured: spatial distribution of cavitation intensity, bubble nucleation rate vs. position, transducer thermal load, and acoustic power coupling efficiency. Scale-up pathway to 100 MW with identified engineering constraints.

**Resolvability:** Genuinely uncertain. This is a conventional engineering problem (expensive, but not physics-blocked). Acoustic interference and thermal management may impose hard limits on achievable power density — limits are currently unknown.

---

### Gap 5: Q and Driver Power Coupling (Joint Design Space)

**What's missing:** Relationship between fusion gain (Q) and acoustic driver power. Model treats them as independent variables — physically incorrect.

**Why it's critical:** The model's sensitivity sweeps assume Q = 5 (or Q = 10) holds across driver power ranging from 1 MW to 1,000 MW. This is unjustified. Fusion gain depends on bubble collapse intensity, which depends on acoustic pressure amplitude and power density. A 1 MW driver operating near the demonstrated 64 kW range would not sustain the same cavitation regime as a 100 MW driver.

**Current evidence:**
- No experimental data on fusion yield vs. acoustic power (fusion has never been demonstrated)
- Sonoluminescence literature documents temperature and light intensity vs. driver frequency and amplitude, but not fusion-relevant parameters

**What would partially resolve:**
If fusion were demonstrated at any power level (e.g., 1 kW driver achieving Q = 0.01), map Q vs. driver power across 1 kW → 1 MW → 10 MW. Determine whether Q scales linearly, saturates, or peaks at specific power densities.

**What would fully resolve:**
Experimental characterization of Q(P_driver, frequency, chamber geometry) across reactor-relevant parameter space. Identify optimal operating point for maximum Q at minimum driver cost.

**Resolvability:** Blocked by Gap 1 (fusion physics demonstration). Until acoustic cavitation produces detectable fusion, the Q–power coupling cannot be measured.

---

## Secondary Gaps (Important but Not Blocking)

### Gap 6: Energy Conversion Pathway

**What's missing:** Specification of how fusion energy is converted to electrical output. Model assumes thermal cycle (Rankine steam) with η_th = 35%, but no conversion pathway has been disclosed or published.

**Why it matters:** Thermal efficiency elasticity is |ε(η_th)| ≈ 0.75 — higher than Q at baseline. A 5-percentage-point improvement (35% → 40%) reduces LCOE by ~30%. sCO₂ cycles achieve 45%+ at high temperature; this is potentially solvable independent of fusion physics.

**Resolvability:** In principle solvable. Requires disclosure of conversion approach (direct charged-particle collection, thermal via liquid heating, or hybrid). Standard thermal cycle engineering is well-established.

---

### Gap 7: Native Power Target (P_net)

**What's missing:** Any company-disclosed target for net electrical output. Model derives 102 MWe from speculative physics parameters.

**Why it matters:** Under the D1+ analysis framework, quantitative models require validated design-point data before modeling. This concept has no design point. The 102 MWe is a modeling artifact, not an extracted value.

**What would resolve:** Company disclosure of target net electrical output per module or per plant. Even without fusion demonstration, a target power level is needed to ground cost scaling.

**Resolvability:** Solvable by company disclosure. Currently no public information.

---

### Gap 8: Tritium Byproduct Handling

**What's missing:** D-D fusion produces tritium (D + D → T + p in ~50% of reactions). Byproduct extraction and containment approach not specified.

**Why it matters:** Lower regulatory burden than D-T breeding (no lithium blanket, smaller tritium inventory), but still requires containment system. Cost impact is derivable once fusion rate is known — likely minor compared to driver capital.

**Resolvability:** Derivable from fusion power. Standard tritium handling methods (cryogenic distillation, permeation barriers) are well-established from D-T fusion programs. Not a fundamental blocker.

---

### Gap 9: Component Lifetimes Under Neutron Irradiation

**What's missing:** PZT transducer lifetime under 2.45 MeV neutron flux. Acoustic cavitation erosion effects on vessel first wall. Active region replacement schedule.

**Why it matters:** Replacement costs (CAS72) affect LCOE. Model assumes 8 FPY core lifetime (longer than D-T blankets due to lower neutron energy), but cavitation-induced erosion is unknown.

**Resolvability:** Requires neutron irradiation testing of PZT materials and erosion testing of first-wall materials under acoustic cavitation. Standard materials qualification — expensive but not blocked.

---

---

## Data Collection Recommendations

### Priority 1: Cease quantitative modeling until fusion is demonstrated

**Action:** Flag this concept as "physics demonstration gap — no LCOE estimate possible" in all cross-concept comparisons. Suppress headline LCOE in explorer visualizations (already implemented via `DATA_GROUNDED = False` flag).

**Rationale:** The model creates an illusion of analytical completeness. Every parameter is speculative. Presenting "24.8 ¢/kWh at ~102 MWe" without exhaustive disclaimers misleads readers into treating this as a parametric uncertainty rather than a viability gate.

### Priority 2: Monitor for experimental fusion demonstrations

**Action:** Set up literature alerts for:
- Acoustic cavitation achieving ion temperatures ≥ 1 million K
- D-D neutron detection from bubble collapse
- Independent replication attempts of any positive fusion result
- Theoretical mechanisms for acoustic compression to thermonuclear conditions

**Rationale:** If the temperature gap is bridged (even partially), the concept moves from "unviable" to "genuinely uncertain." This would justify revisiting the analysis with updated physics constraints.

### Priority 3: Request company disclosure (low expectation)

**Action:** Contact Sonofusion Energy requesting:
- Reactor conceptual design (vessel geometry, driver architecture, energy conversion pathway)
- Target net electrical output per module
- Transducer array engineering design or scaling analysis
- Any experimental fusion results (peer-reviewed or internal)

**Rationale:** Low probability of response (company website provides no technical detail), but disclosure would enable replacing speculative placeholders with company-specified design parameters.

### Priority 4: Driver efficiency prototype (if funded)

**Action:** If external funding becomes available (~$10M–$50M), build a 1–10 MW ultrasonic driver prototype (no fusion requirement) to measure wall-plug efficiency, thermal management feasibility, and transducer reliability at extended duty cycle.

**Rationale:** η_driver is a co-equal blocking parameter with Q. This is testable independent of fusion physics and would derisk half of the recirculating power uncertainty.

---

## Comparison to Other Opaque Concepts

Among the 38+ concepts in the fusion TEA pipeline, acoustic ICF is the **most opaque**:

- **01-hts-compact-tokamak (CFS ARC/SPARC):** Extensive published literature, disclosed Q targets, validated HTS magnet performance. LCOE estimate is "medium confidence."
- **07-maglif (Sandia Z-pinch):** Published experimental results (partial fusion conditions), disclosed pulsed-power parameters, engineering design studies. LCOE estimate is "low-medium confidence."
- **17b-laser-icf-fast-ignition (NIF):** Achieved Q ~ 1.5 (2022), exhaustive published cost data, detailed driver specifications. LCOE estimate is "medium-high confidence."

**Acoustic ICF:** No fusion demonstration, no design disclosure, no quantitative parameters beyond laboratory-scale acoustic driver specifications. LCOE estimate is **"not applicable — physics demonstration gap."**

The only concept with comparable opacity would be entirely speculative approaches (e.g., muon-catalyzed fusion, pyroelectric fusion) — but those are not represented in the current pipeline.

---

## Bottom Line

This concept cannot be analyzed. The gaps are not "data we could find with more research" — they are "fundamental physics questions without theoretical answers." The model exists to test cross-concept comparison infrastructure, not to inform LCOE estimates.

**Recommended treatment in cross-concept comparisons:**
- Exclude from LCOE landscape charts (or annotate as "speculative — no fusion demonstration")
- Exclude from cost account breakdowns (all accounts are invented)
- Include in taxonomy and confinement family trees (belongs structurally to ICF family)
- Cite as a limiting case: "If driver capital could be reduced by 10× vs. laser ICF AND if fusion physics were demonstrated, this architecture could be viable — but both conditions are highly speculative."

**Do not present this concept as having a credible LCOE estimate.** The 24.8 ¢/kWh figure is a modeling artifact, not an economic forecast.