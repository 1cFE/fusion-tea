---
ID: 12-levitated-dipole
Concept: Levitated Dipole (D-T)
Company: OpenStar Technologies
Type: synthesis
Status: draft
Created: 2026-03-22
Stale: true
Stale-Reason: analysis-rewritten-by-force
---

# Synthesis: Levitated Dipole (D-T) — OpenStar Technologies

---

## 1. Executive Summary

- **Most important risk**: Confinement scaling from 26 eV (demonstrated on Junior, February 2026) to 10–20 keV (D-T fusion-relevant) is unvalidated, extrapolates across more than two orders of magnitude in plasma temperature, and is the load-bearing assumption behind the entire Reactor A design point. Tahi (~2028) is designed to demonstrate Lawson-criterion plasma — not net energy — meaning the concept cannot be claimed physics-validated before 2031 at the earliest (Maui, first neutron production). Until Tahi produces data, the Bohm confinement scaling that the 667 MW / 208 MWe design point rests on is a model assumption, not an empirical result.

- **Most important advantage**: A single floating coil replaces the entire magnet system of a tokamak. This is not an incremental simplification — it removes dozens of HTS coils, all their interconnects, correction coils, and PF coil infrastructure, along with the disruption and ELM management systems that drive tokamak operations costs. The levitated dipole's total REBCO demand over a plant lifetime is likely one order of magnitude below that of a comparable HTS tokamak, and the quasi-steady >95% duty cycle is structurally superior to any pulsed or disruption-prone design.

- **LCOE ballpark**: **13.82 ¢/kWh (138 $/MWh) NOAK moderate baseline**; **33.86 ¢/kWh (339 $/MWh) conservative FOAK**; **6.82 ¢/kWh (68 $/MWh) optimistic NOAK**. The specific capital is $9,097/kWe at baseline, with O&M bearing an unusual structural burden: the annual coil replacement contributes 22.5% of total annual revenue requirement ($55M/yr, accumulating to $2.2B nominal over 40 years). Baseline LCOE is not commercially competitive; the optimistic scenario would be.

- **Confidence verdict: Low.** The power balance is well-anchored to the published 667 MW / 208 MWe pair, but every capital cost line is either estimated from indirect analogues or has no analogue at all. The three largest LCOE drivers — coil system capital, annual coil replacement cost, and thermal efficiency — are all genuinely unknown. The model is best read as a structural framework that correctly identifies what will determine commercial viability, not as a prediction of what LCOE will be.

---

## 2. What Matters Most for LCOE

Ranked by combined magnitude of sensitivity sweep and parametric uncertainty, using the model output.

### 1. Annual Sacrificial Coil Replacement Cost — elasticity qualitative: HIGH, uncertainty: CRITICAL

**Assumed value**: $55M/yr (CAS72b), estimated from REBCO tape quantity and manufacturing cost analogues. No published cost estimate or manufacturing specification from OpenStar.
**Sensitivity magnitude**: Sweep from $10M to $120M/yr changes LCOE by −1.98 to +4.25 ¢/kWh from the 13.82 ¢/kWh baseline. At $120M/yr, LCOE reaches 18.07 ¢/kWh — a 31% increase. Over 40 years at $120M/yr, this single line item accumulates to $4.8B nominal, exceeding the entire overnight capital cost.
**What flips the economics**: If the annual coil section material and labor cost exceeds ~$90M/yr, LCOE climbs above 17 ¢/kWh and ceases to be competitive with advanced fission. If the cost comes in at $10–20M/yr (arguably possible if the replaceable section is small and the manufacturing process is mature), LCOE approaches 12 ¢/kWh — competitive territory. This is the single parameter most likely to move the economic conclusion dramatically in either direction, and it is currently the most unconstrained parameter in the model.

### 2. Interest Rate / WACC

**Assumed value**: 8.0% nominal.
**Sensitivity magnitude**: The strongest lever in the model. Range from 4% to 12% WACC changes LCOE from 9.76 to 19.23 ¢/kWh — a 97% swing. At 4% (concessional financing, government-backed), the baseline scenario becomes commercially interesting. At 10%+ (realistic for a first-of-kind concept without demonstrated physics), the concept is clearly uneconomic.
**What flips the economics**: A government-backed or strategic-investor financing structure at 4–5% WACC would put LCOE below 11 ¢/kWh even at the conservative capital assumption. Any project finance structure at prevailing commercial rates (10–12%) pushes LCOE above 19 ¢/kWh — uncompetitive in any plausible electricity market. The capital intensity ($9,097/kWe baseline) makes this concept highly financing-rate-sensitive, more so than lower-capital alternatives.

### 3. HTS Coil System Capital Cost — HIGH UNCERTAINTY, NO ANALOGUE

**Assumed value**: $250M (C220103 override), covering the 23 T REBCO CICC coil, on-board flux pump, and precision docking mechanism. This is an analyst estimate with no direct precedent — the only remotely comparable HTS assembly (CFS SPARC, 18 TF coils) is architecturally dissimilar and covers a different set of subsystems.
**Sensitivity magnitude**: Sweep from $100M to $1,000M changes LCOE from 12.58 to 20.03 ¢/kWh. A 2× overrun ($500M) adds approximately 1.2 ¢/kWh; a 4× overrun ($1B) adds 6.2 ¢/kWh. The $250M baseline is an optimistic-to-moderate estimate — the coil's novelty (levitation-compatible, neutron-tolerant, partially replaceable annually) could easily push costs higher.
**What flips the economics**: At $600M, the concept exceeds the 17 ¢/kWh threshold where commercial competitiveness with advanced fission becomes doubtful. At $100–150M (plausible if manufacturing is modular and learning-curve effects apply to REBCO coil winding), LCOE improves to ~13 ¢/kWh. This parameter cannot be bounded without OpenStar publishing a coil specification and manufacturing plan.

### 4. Thermal Efficiency — TRULY UNKNOWN

**Assumed value**: 38%, set to close the published power balance pair (667 MW fusion → 208 MWe net) at Qsci = 15. The actual conversion cycle (Rankine vs. sCO₂ Brayton) is unspecified in any OpenStar publication.
**Sensitivity magnitude**: Range from 32% to 45% efficiency changes LCOE from 16.65 to 11.75 ¢/kWh — a 4.9 ¢/kWh swing. The two-temperature shield design (>2000 K hot, ~600°C warm) is physically compatible with high-efficiency sCO₂ Brayton, but this is unconfirmed.
**What flips the economics**: If the conversion cycle achieves 42–45% (sCO₂, feasible given the high heat source temperature), LCOE improves to 12–13 ¢/kWh without any other change. If limited to 32–35% (standard steam Rankine), LCOE worsens to 15–17 ¢/kWh. A single BOP disclosure from OpenStar would reduce one of the largest free parameters in the model.

### 5. Qsci (Science Gain) — INFERRED, NOT PUBLISHED

**Assumed value**: 15, inferred from the published 667 MW / 208 MWe pair at assumed thermal efficiency of 38% and ICRH wall-plug efficiency of 70%.
**Sensitivity magnitude**: Range from Qsci = 8 to 25 changes LCOE from 16.99 to 12.74 ¢/kWh. This parameter moves LCOE primarily through the recirculating power fraction — lower Qsci means more ICRH grid draw, higher auxiliary load, lower net output. At Qsci = 8, the recirculating fraction reaches ~37% and net output falls to 171 MWe.
**What flips the economics**: Qsci below ~10 would indicate significant recirculating power and push LCOE above 15 ¢/kWh at baseline. The inferred range of 12–19 is consistent with the published net output and makes the baseline assumptions internally consistent, but the true value is in the published paper and inaccessible in the HTML preprint.

---

## 3. Risk Verdicts

**Challenge 1: Confinement scaling from 26 eV to 10–20 keV D-T operating conditions.**
**Verdict: Genuinely uncertain — and concept-gating.**
**Rationale**: LDX demonstrated Bohm-like confinement in hydrogen at sub-keV temperatures. Junior achieved 300,000°C plasma in levitation for 20 seconds in February 2026 — a legitimate milestone, but 26 eV is more than two orders of magnitude below the 10–20 keV required for D-T fusion. The interpolation across this range is theoretically grounded (the inward turbulent pinch is well-characterized in the Hasegawa-Mima framework) but empirically unconstrained at any fusion-relevant condition. If Bohm-level confinement degrades at high beta or high temperature — which is common in other concepts — the Reactor A design point is unreachable.
**What would retire this risk**: Tahi operating and achieving a measured point on the Lawson criterion curve for D-T conditions (~2028–2029). Even Q << 1 fusion yield with measured nTτ matching the Bohm prediction would confirm the scaling law. Any measured deviation from Bohm scaling at fusion-relevant pressures would require redesign.

**Challenge 2: Plasma exhaust and fueling — completely unaddressed.**
**Verdict: Genuinely uncertain — and the most underappreciated gap.**
**Rationale**: In five published sources covering the OpenStar power plant design, no mention of helium ash management, impurity control, fueling strategy, or plasma boundary handling appears anywhere. The levitated dipole's closed magnetic topology has no natural exhaust channel — there is no divertor equivalent described. A device operating at >95% duty cycle in D-T conditions accumulates helium ash and impurities continuously. OpenStar must have an answer to this; the absence from every publication suggests it is either proprietary or deferred to later design stages. Either interpretation carries risk.
**What would retire this risk**: Any published description of a plasma boundary management approach — even a conceptual outline of how helium is pumped, where impurities accumulate, or what the fueling injection mechanism is. This gap must be closed before Tahi's design is finalized if D-T plasma is part of the Maui mission.

**Challenge 3: Annual sacrificial coil replacement — novel OPEX with no cost analogue.**
**Verdict: Genuinely uncertain — the key OPEX differentiator.**
**Rationale**: No fusion concept in this analysis — tokamak, mirror, FRC, or laser — replaces a superconducting magnet component on an annual scheduled basis. The concept is physically motivated (neutron fluence of 1 MW-year/m² at the outer coil section determines a ~1-year lifetime), but the manufacturing sequence — pump down neon slush, dock magnet, remove outer section, install replacement, recharge via flux pump, re-levitate — has never been demonstrated at any scale. The cost of each replacement cycle depends on the replaceable section's REBCO tape quantity, the manufacturing process, and the remote handling infrastructure.
**What would retire this risk**: A manufacturing specification for the sacrificial outer section and a first-principles cost estimate for the replacement cycle, even at order-of-magnitude accuracy. Alternatively, demonstration of the docking-and-replacement sequence at subscale on Tahi would establish operational feasibility.

**Challenge 4: Flux pump and levitated coil capital cost — no precedent.**
**Verdict: Genuinely uncertain.**
**Rationale**: The on-board superconducting transformer-rectifier flux pump is patented and has no power-plant-scale precedent. Junior's flux pump operates at ~10 W continuous power delivering up to 170 kJ — a world record for HTS flux pump energy delivery but at a device cost of <$10M that cannot scale to a 23 T power plant coil. The stored energy scaling from Junior (0.095 MJ demonstrated) to the Reactor A power plant coil (approximately 16× higher field energy density at B² ratio, substantially larger volume) implies a gap of several orders of magnitude in flux pump capability.
**What would retire this risk**: A Tahi-scale flux pump specification, including energy delivery target, continuous operating power, and estimated capital cost. The Tahi device (targeting 20 T, ~2028) is the appropriate vehicle for demonstrating flux pump scaling in the range relevant to the power plant.

**Challenge 5: Balance of plant thermal cycle undefined.**
**Verdict: Likely resolvable — but currently a large free parameter.**
**Rationale**: Steam Rankine and sCO₂ Brayton cycles are mature at GW-scale. The BOP is not a physics risk. But the two-temperature shield (>2000 K / ~600°C) presents a non-standard heat source profile that requires integration work and would benefit from sCO₂ cycle deployment to capture the high-temperature potential. The cycle choice changes net output and LCOE by ~15%.
**What would retire this risk**: Any BOP section in a future OpenStar design paper, or a disclosure of the intended power conversion cycle. This could be addressed by Tahi's design documentation without any experimental work.

**Challenge 6: Li₂O blanket — preliminary design, acknowledged by OpenStar.**
**Verdict: Likely resolvable — consistent with D-T tokamak design state.**
**Rationale**: Li₂O ceramic tritium breeding is characterized in ITER HCPB TBM programs. The physics is established; the integration challenge (conforming to the spherical dipole geometry with the large bottom opening for coil removal) is real but solvable in engineering design. OpenStar explicitly notes this is early-stage.
**What would retire this risk**: A blanket module conceptual design document for the power plant, including cooling scheme and tritium extraction path. Maui (~2031) is the appropriate milestone.

---

## 4. Structural Advantages and Disadvantages

Compared against a conventional 1 GWe-class D-T HTS tokamak baseline (01-hts-compact-tokamak).

### Eliminated or Reduced Cost Categories

| Item | Approximate Saving vs. Tokamak | Confidence |
|---|---|---|
| Toroidal field and poloidal field coil system (dozens of REBCO coils → one floating coil) | ~$400–$800M per plant; ~$500–$1,500/kWe capital reduction | Medium — rough analogue from SPARC coil estimates |
| REBCO tape supply chain demand (~10× lower total tape over plant lifetime) | Eliminates HTS supply chain bottleneck risk; frees capacity for other users | High — qualitative; single coil vs. ~5,000 km for tokamak |
| Plasma disruption management systems (fast shutdown, runaway electron mitigation, disruption detectors) | ~$20–$50M capital; eliminates major failure mode | High — no plasma current, no disruption physics |
| ELM-driven first-wall fatigue (no ELMs in dipole topology) | Reduces first-wall replacement frequency vs. tokamak | Medium — first-wall regime unstudied for levitated dipole geometry |
| Pulsed energy storage (quasi-steady operation, >95% duty cycle) | ~$10–$30M vs. pulsed MFE designs | High — >95% duty cycle is published and physically motivated |
| High-field shaping coils (no complex 3D winding) | ~$50–$150M for precision TF coil shaping hardware | Medium |

**Net REBCO advantage**: The single-coil architecture is the most meaningful structural simplification in the levitated dipole relative to any tokamak. For equivalent fusion power, the total HTS tape demand is probably one order of magnitude lower. This does not eliminate HTS risk (23 T is at the frontier of demonstrated REBCO performance), but it changes its scale and supply chain implications dramatically.

### Added or Amplified Cost Categories

| Item | Cost Premium vs. Tokamak | Confidence |
|---|---|---|
| Annual sacrificial coil replacement (CAS72b = $55M/yr baseline) | No analogue in any approved prior concept. $55M/yr × 40 yr = $2.2B nominal — exceeds overnight capital | Low — completely unconstrained |
| Precision coil docking and levitation mechanism (C220110 = $88.6M) | Novel remote handling with no precedent; tokamak RH is for planar blanket modules | Low |
| On-board flux pump (included in C220103 = $250M) | Patented, no prior commercial precedent | Low |
| ICRH antenna in dipole geometry (unique RF coupling challenge) | Incremental vs. tokamak ICRH; geometry is harder | Medium |
| Neon slush cryogenics with rapid thermal cycling for annual maintenance | More demanding than steady-state LHe cooling | Low |

### Net Assessment

The capital structure on paper looks comparable to a mid-range D-T tokamak: $9,097/kWe overnight, versus HTS compact tokamak targets of $3,000–$6,000/kWe. The tokamak targets are optimistic; the levitated dipole baseline is moderate-to-conservative. The critical divergence is in the OPEX structure: **the annual coil replacement creates a recurring capital-equivalent expenditure that has no parallel in any other concept analyzed.** If this cost is real at $55M/yr, it contributes more to lifetime cost than the entire blanket replacement schedule of a comparable tokamak. If it can be driven to $10–20M/yr through manufacturing efficiency, it becomes a manageable annuity. This single item — more than any other — determines whether the levitated dipole's simplified magnet architecture produces an economic advantage.

---

## 5. Cross-Concept Positioning

The levitated dipole occupies a position that is structurally unique: **the only closed-field MFE concept that has dramatically simplified the magnet system without eliminating the thermal cycle.** This makes it a genuine outlier in the design space.

**Closest economic analog — Magnetic Mirror (concept 11, Realta Fusion):**
Both concepts produce the same baseline LCOE in the model (levitated dipole 13.82 ¢/kWh; mirror 13.52 ¢/kWh) and both carry a Low confidence rating with similar capital intensity ($9,097/kWe vs. $9,620/kWe). Both are thermal D-T with quasi-steady operation (mirror) or >95% duty cycle (levitated dipole). But the risk character is opposite: the mirror's risk is almost entirely physics-driven (Q > 5 is simulation-only, end-plug confinement undemonstrated), while the levitated dipole has a published design point with a physics basis from LDX and the inward turbulent pinch. The mirror's advantage is the linear scaling thesis (cheap center-cell extension); the levitated dipole's advantage is the single-coil architecture. Neither has been demonstrated at commercially relevant scale.

**Least similar concept — FRC w/ Direct Conversion (concept 08, Helion):**
Helion's economic case rests on eliminating the thermal conversion cycle entirely — a structural difference that changes the capital category. The levitated dipole retains the full thermal cycle and therefore must compete on capital cost and capacity factor, not on cycle efficiency. Helion's $50/MWh NOAK model represents a qualitatively different commercial target enabled by D-He3 and direct energy recovery. The levitated dipole cannot reach Helion's low end even in the optimistic scenario without improved confinement AND a better thermal cycle AND low coil replacement costs simultaneously.

**HTS Compact Tokamak comparison (concept 01, CFS ARC-class):**
The tokamak's physics is better-validated (ARC design is based on SPARC, which has extensive pre-SPARC experimental support); the levitated dipole's magnet architecture is simpler and cheaper in total tape demand. The tokamak's LCOE target is probably lower than the levitated dipole baseline ($5,000–$7,000/kWe vs. $9,097/kWe here), but if the tokamak's cost overruns from HTS supply chain and complexity materialize while the levitated dipole's coil replacement cost is managed, the gap could narrow.

**What makes the levitated dipole fundamentally different:**
1. It is the only concept that stakes its economic case on having ONE magnet instead of many. Every other MFE concept relies on a complete magnet set that defines most of the CAPEX. This is not an incremental advantage — it is a different design philosophy.
2. It is the only concept whose primary scheduled maintenance item is a superconducting magnet replacement. This is a novel OPEX risk with no precedent in any prior approved fusion analysis.
3. It has the highest ratio of "physics confidence per prototype dollar spent" of any concept at this TRL. Junior cost <$10M and demonstrated levitated plasma. This operational efficiency matters for the commercial development timeline.

---

## 6. Modeling Confidence

**Rating: Low.**

| Parameter | Data-Anchored? | Uncertainty Range |
|---|---|---|
| Fusion power (667 MW, Reactor A Bohm) | Yes — published design point | ±5% (inherent to Bohm assumption) |
| Net electric (208 MWe) | Yes — published | Well-constrained given power balance |
| Qsci (~15, inferred) | No — derived from net/fusion power pair; actual value in paper but inaccessible | 12–19 (±25%) |
| Thermal efficiency (38%) | No — assumed to close power balance | 32–45% (±20 percentage points) |
| HTS coil system ($250M) | No — analyst estimate, no analogue | $100M–$1,000M (factor of 4–10) |
| Annual coil replacement ($55M/yr) | No — no specification exists | $10M–$150M (factor of 3–15) |
| ICRH system ($150M) | Partially — ITER ICRH cost analogues | ±50% |
| Remote handling ($88.6M) | No — novel docking mechanism | ±100% |
| Blanket/shield costs | Partially — literature analogues | ±30–50% |
| Duty cycle (95%) | Yes — published | Low uncertainty |
| Buildings | Standard analogue | ±30% |

**Dominant source of LCOE uncertainty**: The annual coil replacement cost. This parameter has the widest absolute uncertainty ($10–$150M/yr), the highest leverage on LCOE (4.25 ¢/kWh swing from the stated range), and zero empirical anchoring in any public source. It also compounds over 40 years, making it unique among the model's cost items.

**Secondary source**: Capital cost of the coil system + flux pump assembly ($250M assumed). This item has no direct analogue in any prior fusion cost analysis, meaning the true value could be anywhere from $100M (if modular, scalable REBCO winding is achievable) to $1B (if the novel levitation-compatible design drives up unit costs).

**The model is best interpreted as establishing the cost structure and identifying what will determine commercial viability — not as a prediction of the LCOE that a Tama Nui-class plant would produce.** The 6.82–33.86 ¢/kWh scenario range honestly reflects the state of knowledge: the physics could support a competitive concept or an uneconomic one depending on parameters that are currently unknown.

---

## 7. What Would Change My Mind

**1. Tahi operating with measured confinement time and plasma parameters at fusion-relevant conditions (~2028–2029).**
This is the single most important disclosure in the near term. If Tahi achieves a measured nTτE within a factor of 2 of the Bohm prediction at temperatures above 1 keV, the Reactor A design point transitions from a theoretical projection to an experimentally anchored scaling. If confinement underperforms Bohm scaling, the 667 MW fusion power assumption requires revision — and LCOE rises accordingly. A confirmed Tahi result matching Bohm scaling at even 1–2 keV would shift modeling confidence from Low to Medium and compress the LCOE scenario range substantially.

**2. A manufacturing specification and cost estimate for the sacrificial coil section and annual replacement cycle.**
A single engineering study — even a pre-conceptual estimate — of the annual coil section cost would do more to constrain the LCOE model than any other publication. If OpenStar or a third-party analyst publishes a cost breakdown showing $15–20M/yr per replacement cycle (achievable if the outer section is relatively small and manufacturing is streamlined), the baseline LCOE improves to ~12 ¢/kWh and the concept's competitive position strengthens materially. If the estimate comes in at $100M+/yr, the concept becomes structurally non-competitive regardless of capital cost improvements. At present, this item is the dominant source of LCOE uncertainty, and it is entirely within OpenStar's power to reduce that uncertainty without any experimental program.

**3. A disclosed plasma exhaust and boundary management approach for D-T operation.**
Absence of information on helium ash accumulation, impurity control, and fueling is not a neutral observation — it is a signal that a fundamental design problem has not been publicly addressed. If OpenStar publishes a credible description of how helium ash is removed from a closed-field topology operating at >95% duty cycle, it eliminates what is currently the most underappreciated binary risk in the concept: a closed-field device that accumulates helium ash without a workable exhaust path cannot sustain D-T plasma regardless of confinement quality. Any credible answer here — even a conceptual one — would materially improve confidence in the commercial pathway.
