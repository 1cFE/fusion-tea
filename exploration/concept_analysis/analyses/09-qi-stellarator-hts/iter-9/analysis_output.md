# D1+ Analysis: QI Stellarator - HTS (Proxima Fusion / Stellaris)

**Concept**: Quasi-Isodynamic Stellarator with HTS magnets — D-T fuel
**Company**: Proxima Fusion (Munich, Germany; Max Planck IPP spin-off)
**Published Plant Study**: Stellaris (Fusion Engineering and Design, Vol. 214, May 2025)
**Confinement Family**: MFE — Stellarator (QI)

---

## Section 1: Availability of Data

**Rating: Moderate**

Proxima Fusion has published more design detail than most private fusion companies in a comparable stage, primarily through the peer-reviewed Stellaris paper (DOI: 10.1016/j.fusengdes.2025.114868). However, the paper is paywalled, and the extracted source document (`stellaris-design-details.md`, 337 KB) frames this as "a high-level 'version 1' of what a QI stellarator fusion power plant design can be" — the authors explicitly note that "at time of writing (late 2024)...it is already evident that more commercially attractive Stellarator designs are possible." The "Moderate" rating reflects: the company has published sufficient technical depth to anchor a preliminary LCOE framework, but capital costs, major radius, and plasma current are not in the public record.

**Published machine design documentation:**
The Stellaris paper covers electromagnetic design, plasma-facing components, first-wall cooling, blanket design and neutronics, magnet quench safety, support structures, and remote maintenance — a scope broader than most pre-conceptual fusion plant studies. The extracted source provides global design parameters (Table 3): peak fusion power ~2700 MW, peak thermal power ~3300 MW, net electrical ~1000 MW, peak first wall load 4.05 MW/m², and stored magnetic energy 111 GJ. Plasma parameters (ion temperature 15 keV, electron density 5×10²⁰ m⁻³, triple product 12.4×10²¹ keV·s·m⁻³, beta 2.76%) are stated explicitly. The Proxima technology page and press releases confirm the company's W7-X heritage, HTS strategy, and the February 2026 MoU with RWE, the Free State of Bavaria, and Max Planck IPP.

> "These stellarators have the ability to run in steady-state, intrinsically reducing thermal and mechanical component fatigue"
> — stellaris-design-details.md, §2 (Performance advantages)

> "It is important to note that the feasibility of this manufacturing process will be the focus of subsequent studies"
> — stellaris-design-details.md, §2.8 (Blanket manufacturing note)

**High-quality analogue source:**
The Helios stellarator design paper (Thea Energy, arXiv:2512.08027) is a pre-conceptual QA/QI stellarator commercial plant study using the same optimization philosophy, also targeting D-T with HTS magnets. It provides global parameters not published for Stellaris: thermal efficiency (40%), capacity factor (88%), ECRH power breakdown (10 MW startup, 1 MW ignited), and a detailed cost-relevant blanket and divertor engineering description. This source fills critical gaps in the LCOE analysis and is treated as a primary analogue.

**Independent comparative analyses:**
Brown (2018, *IEEE Transactions on Plasma Science*) provides the most quantitative published comparison of major cost elements across spherical tokamak, standard tokamak, and stellarator configurations. ARIES-CS and ARIES-AT (ARIES Team, late 1990s–early 2000s) remain the only published plant-level cost studies for optimized stellarators, both using LTS conductors and significantly larger machine sizes than Stellaris. These studies give a cost floor but not a ceiling for modern HTS stellarator magnets. Note that ARIES-CS studied quasi-axisymmetric (QA) configurations, not quasi-isodynamic (QI) — the cost floor inference carries an additional structural assumption that QA and QI stellarators of similar size and field strength have comparable cost structures, which may not hold, particularly in the CAS21 coil account where different magnetic symmetry classes imply different coil topologies.

**Phase 1a dossier completeness:**
High confidence on 8 of 12 differentiation columns (confinement family, concept, fuel, magnet type, tritium breeding, operation mode, repetition rate, driver technology). Medium confidence on 4: primary heating (ECRH inferred from stellarator physics), energy capture (steam Rankine inferred from WCLL coolant temperature), plasma state (burning inferred from 2.7 GW target), neutron management (integrated blanket/shield inferred from WCLL design). The full Stellaris paper would likely resolve all 4 medium-confidence items.

**Key data gaps limiting this analysis:**
1. Capital cost estimate for Stellaris — not published; internal cost optimization mentioned but not disclosed
2. Major radius and plasma volume — not in public sources
3. Gross thermal efficiency and power conversion cycle confirmed specification — inferred from WCLL blanket temperature limits
4. 3D non-planar HTS coil manufacturing cost — no commercial precedent; SMC demo milestone targeted for 2027
5. O&M cost breakdown — no data in any source

---

## Section 2: Challenges in Capturing System Function

Challenges are ranked by expected LCOE impact. The QI stellarator presents a different cost uncertainty profile from the HTS compact tokamak: the largest source of uncertainty is not physics performance but manufacturing cost of the confinement coils.

**1. 3D Non-Planar HTS Coil CAPEX — No Commercial Precedent (Impact: Critical)**

The dominant LCOE uncertainty for Stellaris is the cost of its non-planar modular HTS coils. These coils produce the helical magnetic field entirely via external windings, requiring complex 3D freeform geometry that has no equivalent in tokamak manufacturing. The only existing data points are W7-X (LTS conductors, 6 T, mid-1990s design, approximately €370 million hardware investment over 1997–2014 — the total 18-year site cost including operations reached €1.06 billion, but the overrun was driven by a 9-year schedule delay doubling personnel costs, not by coil manufacturing; the hardware reference for a full W7-X-scale stellarator is ~€370M), and Proxima's planned Stellarator Model Coil (SMC) demo targeted for 2027. REBCO tape costs for stellarator coils are expected to exceed the wound-tokamak case per unit fusion power because: (a) the 3D coil geometry requires more tape per coil turn-length to achieve equivalent field strength; (b) winding mandrels, precision positioning, and quality assurance for freeform geometry add fabrication cost; and (c) no mass-production learning curve exists. Brown (2018) provides a comparative framework across stellarator and tokamak cost categories, showing the stellarator magnet system carrying a substantial premium in the CAS21 account. The uncertainty range on coil CAPEX spans roughly 1.5–5× the equivalent wound-coil tokamak magnet cost — a wider range than for any other MFE concept currently under analysis.

**2. Low-Beta Machine Scale Penalty (Impact: High)**

Stellaris operates at volume-averaged plasma beta of 2.76% [stellaris-design-details.md §Table 3]. This is roughly half the 5–8% beta typical of compact tokamaks with equivalent field strength. Lower beta requires more plasma volume to achieve the same fusion power density, which propagates directly into first wall area, blanket mass, structural steel, and vacuum vessel cost. Producing 2.7 GW fusion power at 6.1 MW/m³ average power density in a low-beta plasma implies a larger physical machine than an ARC-class HTS compact tokamak at equivalent peak fusion power. The Helios analogue (2.7% beta, 958 MW fusion power) gives a rough scale reference, but Stellaris targets ~2.8× higher fusion power in a larger device. The compactness benefit of HTS (which drives the CFS ARC economic case) is materially reduced by the low-beta operating point.

Critically, however, 2.76% is a **Stellaris v1 design-point choice, not an inherent ceiling for QI stellarator physics**. The CIEMAT-QI4X configuration (arXiv:2512.08825, December 2025) — a four-field-period QI stellarator — demonstrates resilience at beta up to 4% while maintaining small neoclassical and turbulent transport, good fast-ion confinement across the full beta range, small bootstrap current, and an edge island structure compatible with an island divertor: "CIEMAT-QI4X has a 4/4 island chain at the edge that is resilient at least up to β=4%, even when the bootstrap current is included" [arxiv-2512-08825.md, abstract]. This is roughly 45% higher than Stellaris's design point and is consistent with Proxima's own statement that "more commercially attractive designs are possible." A follow-on QI design at 4% beta would reduce the required plasma volume (and hence first wall area, blanket mass, and vacuum vessel scale) at equivalent fusion power by a factor proportional to the beta ratio — partially closing the gap to compact tokamak power density. For TEA purposes, the scale penalty described here applies specifically to Stellaris v1; next-generation QI designs should be treated as a scenario branch rather than the same design point.

**3. Burning Plasma Assumption Driving H&CD Cost (Impact: High)**

The H&CD cost advantage for stellarators depends critically on achieving ignition. The Helios analogue requires only 1 MW ECRH in steady-state ignited operation [helios-stellarator-comparison.md §3.1], which would make the H&CD account a large negative delta relative to a tokamak requiring 50–100 MW of NBI + ECRH. The Stellaris paper specifies 50 MW ECRH [stellaris-design-details.md §2], which represents the operational steady-state auxiliary power — not a post-ignition nominal. It is unclear whether this 50 MW is a conservative operational assumption or reflects that Stellaris does not reach full ignition. If Stellaris requires sustained 50 MW ECRH (rather than reducing to ~1–5 MW after alpha self-heating takes over), the H&CD CAS22 account approaches parity with the tokamak rather than a large discount. No Q value is published for Stellaris; the dossier infers "burning plasma" from the 2.7 GW fusion power target at medium confidence.

**3a. Alpha Particle Confinement — QI Advantage Partially Validated (Impact: High)**

ARIES-CS phase 1 explicitly identified "high {alpha} particle loss of these configurations is a critical issue" for compact stellarator configurations [aries-cs-compact-stellarator-study.md, abstract]. This was a central motivation for the QI optimization strategy: the maximum-j property — which controls variation of the second adiabatic invariant J∥ along field lines — bounds trapped fast-particle bounce-averaged drifts, improving alpha retention relative to non-optimized or QA-class designs. Stellaris quantifies this: SIMPLE code simulations give ~0.7% collisionless alpha loss fraction, and ANTS code (collisional, full slowing-down) gives ~0.8% total alpha energy loss, corresponding to lost fusion power below ~10 MW at the design point [stellaris-design-details.md §2.2]. The maximum-j property is tracked as an explicit design metric alongside neoclassical transport coefficients. For comparison, the Helios QA analogue shows 6.6% alpha energy loss [helios-stellarator-comparison.md §3.3] — confirming QI outperforms QA on this metric — but the Helios paper notes that "diffusive drift is the dominant loss mechanism. The majority of lost alpha orbits exhibit significant variation in J∥ associated with diffusive drift" [helios-stellarator-comparison.md §3.3], and that further optimization of this loss channel is ongoing.

Two residual risks remain for Stellaris:
1. **Burning plasma validation**: The SIMPLE and ANTS simulations model alpha confinement at the design-point MHD equilibrium but exclude wave-particle interactions at burning plasma beta. The SMC demo (2027) tests coil manufacturing only — alpha self-heating validation requires the Alpha device (Q>1, ~2031). If QI optimization in the simulation is optimistic about losses in the actual burning plasma regime, H4 is at risk: the 50 MW steady-state ECRH may not be reducible to ~1–5 MW after startup.
2. **Scale extrapolation**: Stellaris targets 2.7 GW fusion power (vs. ARIES-CS sub-GW configurations and Helios's 958 MW). At larger scale and higher field (14.4 T peak on-coil), loss channels and their magnitudes may deviate from existing simulation benchmarks. No burning-plasma-condition alpha confinement experiment in a QI configuration exists.

This challenge connects directly to H4 (ignition assumption) in the modeling approach: the alpha confinement quality determines whether Stellaris achieves full self-heating or requires sustained high auxiliary power. It is also a key differentiator from the ARIES-CS starting point — the QI innovation is specifically designed to resolve the alpha loss problem that limited earlier compact stellarators.

> "High {alpha} particle loss of these configurations is a critical issue"
> — aries-cs-compact-stellarator-study.md, abstract (ARIES-CS Phase 1 finding)

> "diffusive drift is the dominant loss mechanism. The majority of lost alpha orbits exhibit significant variation in J∥ associated with diffusive drift. Further optimizations will target this loss channel."
> — helios-stellarator-comparison.md, §3.3 (Alpha confinement in QA stellarator)

---

**4. TBR Margin Adequacy in 3D Blanket Geometry (Impact: Moderate)**

The Stellaris blanket achieves a baseline TBR of 1.1070 ± 0.0002 in Monte Carlo modeling, reduced to 1.074 after applying a 3% correction for heating ports [stellaris-design-details.md §2.8]. This 1.074 post-correction TBR is close to the typical minimum engineering requirement of ≥ 1.05–1.1 for tritium self-sufficiency at reasonable doubling time. The stellarator's complex 3D first wall geometry creates more blanket penetrations (diagnostic ports, heating ducts, island divertor structure) than a tokamak, increasing neutron leakage pathways. The paper itself acknowledges that "margins to account for uncertainties and potential incomplete models" were applied, and that "divertor recycling efficiency, ash removal, and erosion rates are left for further exploration." If additional engineering losses reduce the effective TBR below 1.05, Stellaris requires either higher Li-6 enrichment (currently 70%), reduced port area, or external tritium supplementation during early plant years.

**5. Island Divertor Scaling to Burning Plasma Power Density (Impact: Moderate)**

The island divertor — Stellaris's heat exhaust system — is unique to the QI stellarator and represents a physics bet not shared with tokamak designs. W7-X has demonstrated the island divertor concept in steady-state operation and showed advantages over tokamak divertors in terms of wetted area and access to complete detachment [stellaris-design-details.md §2.5]. However, W7-X operates at power densities far below the 4.05 MW/m² first wall load of Stellaris. The paper characterizes the island divertor approach as a "tungsten-based island divertor that operates with strong detachment in steady-state," but explicitly defers detailed divertor physics (recycling efficiency, ash removal, erosion) to subsequent studies. Unlike the tokamak poloidal divertor, the island divertor geometry is tightly coupled to the magnetic topology and has limited adjustment freedom if it fails to manage burning-plasma exhaust power.

---

### Recommended Modeling Approach

The appropriate LCOE modeling framework for Stellaris is a **CAS-modified tokamak reference model** — use the HTS compact tokamak (01-hts-compact-tokamak / CFS ARC) as the base cost structure, then apply account-level multipliers and deltas for the stellarator-specific differences. This approach is viable because: the two concepts share D-T fuel, WCLL-type breeding blanket architecture, HTS REBCO tape technology, steam Rankine power conversion, and the same nuclear island balance-of-plant structure. A from-scratch LCOE model would require assumptions about all shared accounts that are already anchored in the tokamak literature; the delta approach makes the comparison explicit and the assumptions auditable.

The sensitivity axes fall into two distinct roles that should not be conflated:

**Viability threshold (scenario gate):**
1. **3D coil cost multiplier** (C220103): Range 1.5–5× wound-coil tokamak magnet cost; SMC demo data (2027) is the first real data point. This parameter functions as a go/no-go gate: if the manufacturing premium exceeds ~2×, stellarator CAPEX is unlikely to be competitive against compact HTS tokamaks at any plausible capacity factor advantage. A 400% increase in the multiplier (from DEFAULT to 5×) moves LCOE by ~34% — an elasticity of ~0.08 — which means it is not the largest LCOE lever per unit of uncertainty, but it determines whether the concept is viable at all.

**Primary continuous sensitivity parameter (LCOE lever):**
2. **Capacity factor** (availability): Formal sensitivity analysis shows availability elasticity at approximately −0.89, roughly 10× higher than the coil multiplier elasticity. Steady-state, disruption-free operation is the primary continuous knob for optimizing LCOE within a viable design. Range 85–95% [analogue: Helios targets 88%; W7-X demonstrated >97% run-time availability in experimental context, though plant availability will be lower due to blanket/divertor maintenance]. A reader prioritizing modeling effort should focus on the availability parameter first; coil cost defines the viability envelope, but availability drives LCOE within it.

**Secondary continuous parameters:**
3. **Plasma volume / major radius** (machine scale): The low-beta penalty propagates into all nuclear island cost accounts. Range: constrained by the 2.7 GW fusion power target and 6.1 MW/m³ power density; derivable from Helios scaling but not published for Stellaris.

4. **Construction time** (IDC / CAS60): Model sensitivity analysis shows `construction_time_yr` at elasticity +0.40 — the third-highest engineering lever, ranking above major radius (+0.31). This parameter is directly linked to Challenge 2 (machine scale penalty): a 13 m major radius machine with complex 3D non-planar coil installation requirements plausibly requires a longer first-of-kind construction schedule than an ARC-class compact device (R0 ≈ 3–4 m). IDC (CAS60) is among the largest single cost accounts in the model. IDC elasticity of +0.40 means a 20% schedule extension adds ~8% to LCOE — a larger incremental effect than major radius (R0) elasticity alone. Construction time should be treated as the financial expression of the machine scale penalty, not merely a scheduling assumption.

**Key Hypotheses for the cost model:**

**H1 (3D Coil Manufacturing):** The 3D HTS stellarator coil manufacturing cost premium over a wound tokamak coil of equivalent peak field strength is less than 2× per kAm of conductor. If false (premium exceeds 2×), stellarator CAPEX is unlikely to be competitive against compact HTS tokamaks regardless of availability benefit at any plausible capacity factor advantage.

**H2 (Capacity Factor Advantage):** Stellaris achieves a capacity factor materially above the HTS compact tokamak reference (01-hts-compact-tokamak / CFS ARC), sufficient to offset the low-beta CAPEX penalty at a coil cost multiplier of ≤ 1.5×. **Important:** the 01-hts-compact-tokamak analysis does not publish a CF target for the ARC-class device; the appropriate comparison baseline is therefore unresolved. The Araiinejad & Shirvan (2025) ARPA-E framework uses 90% availability; ARC-class designs with active disruption prediction and avoidance plausibly target 87–90% CF. If the HTS compact tokamak reference achieves 87–90% CF, Stellaris's 88% Helios-analogue target yields an advantage of 0–1 percentage points — negligible and insufficient to offset the coil cost premium. The H2 gate cannot be quantitatively evaluated until the 01-hts-compact-tokamak analysis provides a comparable CF estimate. As currently framed, Stellaris's disruption-free advantage is real but may be much smaller than the ~3–5 pp gap to a conventional disruption-limited tokamak (~83–85%) that was the original viability threshold. The 88% target is anchored in the Helios design [helios-stellarator-comparison.md §2]; blanket and divertor scheduled maintenance sets the practical ceiling (see H5); no published availability model exists for Stellaris. If the capacity factor advantage over the actual HTS tokamak reference is ≤ 2 percentage points, it does not compensate for the coil cost premium even at the optimistic end.

**H2a (Higher-Beta QI Design Scenario):** A follow-on QI stellarator design operating at ~4% beta (as demonstrated feasible by CIEMAT-QI4X [arXiv:2512.08825]) would materially reduce the scale penalty relative to Stellaris v1. This should be treated as a separate scenario branch in the LCOE sensitivity sweep, not a variation of the Stellaris design point. At 4% beta vs. 2.76%, plasma volume at fixed fusion power density scales down by ~31%, with proportional reductions in first wall area and blanket mass — bringing the machine closer to compact tokamak scale and partially closing the CAS23 and CAS28 cost gaps. The 3D coil manufacturing cost (CAS21) and capacity factor advantage (H2) remain as the primary differentiators in either scenario.

**H3 (TBR Adequacy):** The 1.074 post-correction TBR holds against full engineering losses (additional penetrations, diagnostic ports, material uncertainties, blanket lifetime evolution). If the engineering TBR falls below 1.05, external tritium supply is required during a critical startup window, adding an operational cost component and a potential sequencing constraint.

**H4 (Ignition / H&CD Cost):** Stellaris achieves alpha self-heating such that steady-state ECRH drops to ≤ 5 MW in normal operation. If false (sustained 50 MW ECRH required), the H&CD CAS22 account reverts from a large negative delta to cost parity or a penalty relative to the tokamak reference, and the net directional cost comparison in Section 7 changes sign on the most important offset. H4 depends on Challenge 3a: the QI maximum-j optimization yields ~0.8% simulated alpha energy loss [stellaris-design-details.md §2.2], which is consistent with adequate self-heating, but burning plasma conditions cannot be validated before the Alpha device (~2031). ARIES-CS (QA, not QI) had high alpha losses that prevented ignition in its configurations — Stellaris's QI approach is specifically designed to solve this problem, but the validation gap remains open through the SMC demo milestone.

**H5 (Island Divertor at Burning Plasma):** The island divertor successfully manages exhaust power at 4.05 MW/m² average first wall load in steady-state detached operation. If false, the required mitigation — geometry-constrained divertor redesign within the stellarator magnetic topology, or acceptance of higher tungsten target erosion and shorter replacement intervals — increases maintenance cost and reduces effective availability. Unlike the tokamak divertor, the island divertor geometry cannot be independently optimized from the magnetic equilibrium; failure has no straightforward engineering fallback within the QI approach.

---
[1] stellaris-design-details.md, §2: "These stellarators have the ability to run in steady-state, intrinsically reducing thermal and mechanical component fatigue"
[2] stellaris-design-details.md, §2.5: "Stellarators do not exhibit the unfavorable 'Eich-scaling' of heat exhaust deposition width on divertor plates seen in tokamaks"
[3] stellaris-design-details.md, §2.8: TBR 1.1070 baseline, 1.074 post-correction
[4] helios-stellarator-comparison.md, §3.1: "only nominal heating (1 MW) is required once the plasma self-heats in the ignited phase"
[5] helios-stellarator-comparison.md, §2: "enabling an 88% capacity factor"

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**3D Non-Planar HTS Coil Manufacturing — TRL 3–4**
- **Demonstrated**: W7-X demonstrated the physics and mechanics of non-planar modular stellarator coils using LTS conductors at 6 T. HTS single-coil prototypes (CFS, Commonwealth tokamak-geometry) have validated REBCO tape behavior at high field. Proxima is developing coils with PSI & BNET. The Stellarator Model Coil (SMC) demo is targeted for 2027 to de-risk manufacturing.
- **On paper only**: Full-scale 3D non-planar HTS coil set at 14.4 T peak on-axis and 20 T peak on-coil for a burning plasma device. Winding, insulation, and quench protection schemes for stellarator-geometry REBCO coils at plant scale.
- **Missing at scale**: Production-scale fabrication of multiple geometrically complex HTS coil units meeting dimensional tolerances required by the magnetic field optimization. REBCO neutron irradiation performance at stellarator coil fluences (~9.5×10¹³ n/m²/s estimated at the 99th quantile; 10-year lifetime at 2.7 GW [stellaris-design-details.md §2.8]). Radiation-hardened coil insulation at fusion neutron energies. Quench detection and protection for 111 GJ stored energy in a distributed 3D geometry.

> "Estimating the allowable fluence for ReBCO superconductors...as 3×10²² 1/m², the magnet system would have a lifetime of approximately 10 full power years at a fusion power of 2700 MW"
> — stellaris-design-details.md, §2.8 (Magnet lifetime estimate)

---

**WCLL Blanket Adapted to Stellarator Geometry — TRL 3–4**
- **Demonstrated**: Water-cooled lithium-lead blanket developed extensively for EU DEMO (tokamak geometry). Small-scale PbLi flow experiments. Neutron multiplication by lead verified in mock-up tests. Helium-cooled first wall concept demonstrated at component scale.
- **On paper only**: WCLL blanket adapted to the complex 3D plasma-facing surface of a QI stellarator — 73.5% PbLi / 12.5% water / 14% EUROFER97 by volume, with helium-cooled EUROFER97 first wall and 2 mm tungsten armor. Single Module Segment (SMS) design with poloidal splitting every ~1 m for modularity [stellaris-design-details.md §2.8]. TBR 1.074 validated by Monte Carlo.
- **Missing at scale**: The Stellaris paper explicitly states: "the feasibility of this manufacturing process will be the focus of subsequent studies." 14 MeV neutron irradiation testing of EUROFER97 + PbLi interface at fusion-relevant fluences (~150–200 dpa). Tritium extraction from PbLi at kg/day throughput. Thermal-hydraulic validation of the dual helium-water cooling circuit under 3D geometry.

---

**Tritium Fuel Cycle and Extraction — TRL 4–5**
- **Demonstrated**: Lab-scale tritium handling loops and liquid-metal extraction circuits. JET and TFTR historically handled gram-scale tritium. PbLi tritium transport modeling (ITER TBM program).
- **On paper only**: Closed-loop tritium extraction from PbLi at kg/day throughput. Permeation-resistant barriers in PbLi circuits. Tritium inventory accounting at plant scale.
- **Missing at scale**: Industrial-scale tritium processing plants compatible with the WCLL coolant system. Low-inventory storage and sub-percent permeation loss rate under steady-state operation. TBR confirmation through full integrated operation. (This challenge is shared with all D-T MFE concepts; see 01-hts-compact-tokamak §3 for full treatment.)

---

**Island Divertor at Burning Plasma Power Density — TRL 5–6**
- **Demonstrated**: W7-X island divertor demonstrated steady-state operation with strong detachment at low power density, showing large wetted areas and reduced heat flux concentration. Tungsten divertor target fabrication at W7-X scale. Two recent milestones directly validate the steady-state capability: in February 2023, W7-X achieved up to 30 minutes of continuous plasma discharge, explicitly described as demonstrating "an essential feature of a future fusion power plant: continuous operation" [en-wiki-wendelstein-7-x.md]; and in June 2025, W7-X achieved 1.8 GJ energy turnover in a 6-minute run using continuous pellet injection, surpassing the EAST tokamak's 2025 record and confirming the island divertor's ability to sustain high-energy discharge [en-wiki-wendelstein-7-x.md]. These are the most direct experimental evidence for the steady-state island divertor concept at meaningful plasma durations.
- **On paper only**: Island divertor operating at burning plasma power density (4.05 MW/m² average first wall load for Stellaris). Divertor plasma recycling efficiency, neutral gas compression, and ash removal at the power levels required for self-sustaining D-T burn.
- **Missing at scale**: Long-term tungsten erosion and redeposition behavior in an island divertor under fusion-relevant neutron flux and plasma heat flux. Divertor replacement scheme within the constrained geometry of the Stellaris remote maintenance architecture [stellaris-design-details.md §2.11]. The power density gap between W7-X experimental conditions and Stellaris remains the primary TRL limitation — the 2025 energy record is a duration/energy demonstration, not a power density demonstration.

> "Divertor operational aspects — such as recycling efficiency, ash removal, neutral gas compression, and erosion rates — are acknowledged, but left for further exploration in subsequent studies"
> — stellaris-design-details.md, §2.5 (Divertor limitations)

---

**ECRH Heating System — TRL 7–8**
- **Demonstrated**: MW-class 140 GHz gyrotrons at W7-X (10 gyrotrons); 170 GHz ITER-specification gyrotrons validated. 10 MW-class ECRH systems routinely operated on W7-X and other tokamaks.
- **On paper only**: 50 MW continuous ECRH system for Stellaris at plant scale, running at wall-plug efficiency >50% (current state ~50%; >60% possible with multi-stage depressed collectors [stellaris-design-details.md §2, gyrotron efficiency note]).
- **Missing at scale**: Long-duration high-power gyrotron operation under neutron/gamma background. High-availability replacement scheduling in a plant context. ECRH power reduction in ignited phase (from 50 MW startup to ~1–5 MW steady-state if ignition achieved) requires operational flexibility not yet demonstrated.

---

**Balance of Plant (Steam Rankine) — TRL 8–9**
- **Demonstrated**: Steam Rankine cycles at GW scale in fission and fossil plants. The EUROFER97 temperature limit (<550°C) constrains the steam temperature and thus cycle efficiency; this is an integration challenge rather than a technology gap.
- **Missing at scale**: Interface with tritium-permeating PbLi primary loop; intermediate heat exchanger design for WCLL-steam interface under fusion neutron environment. The ~32% overall plant efficiency (thermal-to-net-electric, inferred from 1.0 GW net / 3.1 GW thermal [dossier.md §Summary]) is consistent with a steam Rankine cycle at EUROFER97's temperature limit, but this is lower than the 40% achieved in the Helios design (which uses a higher-temperature vanadium alloy first wall permitting 635°C steam [helios-stellarator-comparison.md §4.2]) and significantly below what sCO₂ Brayton could achieve. The choice to use EUROFER97 over vanadium alloy trades supply-chain maturity for cycle efficiency.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape**

The QI stellarator requires REBCO tape at the same or higher linear quantities per plant as an HTS compact tokamak, with the additional constraint that the tape must be wound into geometrically precise 3D non-planar coils rather than the D-shaped planar geometry of tokamak coils. Global REBCO production capacity is currently on the order of thousands of kilometers per year, while a QI stellarator plant with 111 GJ stored magnetic energy likely requires significantly more tape than the ~5,000 km estimated for an ARC-class device (exact stellarator demand not published). Proxima has signed an agreement with Faraday Factory Japan for REBCO tape supply for the SMC demo magnet, establishing a supply relationship but not yet at production scale [proxima-fusion-technology-page.md; dossier.md §Magnet Type]. Planned magnet factory with up to 1,000 jobs indicates vertical integration intent. The REBCO fluence constraint (~3×10²² m⁻², corresponding to ~10 full-power years at 2.7 GW) means magnet replacement is a planned maintenance event during a 30-year plant lifetime — adding a lifetime cost component unique to the stellarator's high stored energy.

**Lithium-6 Enrichment (70% for WCLL)**

Stellaris uses 70% Li-6 enrichment in the PbLi eutectic to achieve TBR 1.074 [stellaris-design-details.md §2.8]. This is a well-defined isotopic enrichment requirement with limited global supply chain: primary suppliers are China and Russia, both historically using the mercury-based COLEX process that is banned in most countries due to environmental hazard. Western enrichment capacity (separation by laser or ion exchange) is in development but not yet at industrial scale. The 70% enrichment level is higher than some tokamak designs (EU DEMO WCLL targets 60–90%), and the global civilian supply of enriched Li-6 is constrained by the same supply dynamics affecting all D-T fusion plants.

**EUROFER97 Reduced-Activation Ferritic-Martensitic Steel**

EUROFER97 is the primary structural material for the first wall, blanket modules, and vacuum vessel backwall in Stellaris. Its 550°C operating limit directly constrains steam cycle efficiency. EUROFER97 is not currently produced at industrial scale — it exists as experimental heats for the EU DEMO/fusion program — but it is a well-characterized alloy with an established production route. The fusion community's DEMO program provides a shared supply development path. A key property for Stellaris: EUROFER97's low activation and ferromagnetic behavior (below Curie temperature at operating conditions) must be compatible with the stellarator magnetic field topology — a consideration not relevant for tokamaks.

**Tungsten (First Wall Armor and Divertor Targets)**

Stellaris uses 2 mm tungsten armor bonded to EUROFER97 as the plasma-facing surface [stellaris-design-details.md §2.7], and tungsten targets for the island divertor. The QI stellarator presents an additional challenge not shared with tokamaks: the first wall follows a complex 3D curved plasma boundary, requiring tungsten tiles shaped to non-planar geometry. Flat or cylindrical tungsten tiles used in tokamak designs (ITER-style monoblock, W7-X plates) are more straightforward to manufacture than the 3D-curved tiles required here. The Stellaris paper notes risk of tungsten sputtering causing radiative collapse [stellaris-design-details.md §2.7], consistent with the known tokamak challenge. Tungsten supply is adequate globally; precision fabrication for stellarator geometry is the binding constraint, not material availability.

> "Tungsten atoms can be sputtered and potentially accumulate in the core of the plasma. This accumulation can lead to a radiative collapse, causing operations to halt"
> — stellaris-design-details.md, §2.7 (Tungsten first wall risk)

**PbLi Eutectic (Breeding Blanket)**

Lead-lithium at 16 at% lithium is a well-established blanket material in the EU DEMO program. Lead supply is globally adequate (primary commodity) and lithium supply from brine and spodumene is sufficient at fleet scale. The main cost uncertainty is the Li-6 enrichment (addressed above) and the tritium extraction system for PbLi (a shared challenge with EU DEMO). Proxima notes the WCLL is a "concept, not a complete engineering design" and that they hold a patent for an "innovative liquid-metal breeding blanket" that may differ from the WCLL baseline [dossier.md §Tritium Breeding]. This introduces a potential supply-chain bifurcation between the WCLL analogue and the eventual as-built design.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Peak fusion power | 2,700 MW | stellaris-design-details.md §Table 3 | high | "Peak" value; average may be lower during part-load or startup |
| Peak thermal power | ~3,300 MW | stellaris-design-details.md §Table 3 | high | Includes blanket neutron multiplication (~1.2×) |
| Net electrical output | ~1,000 MWe | dossier.md §Summary | high | Derived from Stellaris paper; aggregate figure |
| Overall plant efficiency (net/thermal) | ~32% | [inferred: 1,000/3,100 MWe/MWth] | medium | Based on 3.1 GW thermal; gross efficiency likely ~38–40% with ~20–25% recirculating power fraction |
| Recirculating power fraction | ~20–25% | [inferred: gross electric ~1,200–1,300 MWe at 38–40% thermal; recirculating = gross − 1,000 MWe] | low | Coil conduction 111 MW + ECRH 50 MW + pumping ~50 MW; consistent with ~24% recirculating fraction |
| Volume-averaged plasma beta | 2.76% | stellaris-design-details.md §Table 3 | high | Low by MFE standards; ~half of ARC-class compact tokamak |
| Peak ion temperature | 15 keV | stellaris-design-details.md §Table 3 | high | Design point |
| Peak electron density | 5 × 10²⁰ m⁻³ | stellaris-design-details.md §Table 3 | high | |
| Peak triple product | 12.4 × 10²¹ keV·s·m⁻³ | stellaris-design-details.md §Table 3 | high | Sufficient for burning plasma regime |
| Magnetic field (average on-axis) | 9.0 T | stellaris-design-details.md §Table 3 | high | |
| Magnetic field (peak on-coil) | 14.4 T | stellaris-design-details.md §Table 3 | high | Sets REBCO tape operating point |
| ECRH auxiliary power | 50 MW | stellaris-design-details.md §Table 3 | high | Operational steady-state; may reduce to ~1 MW if ignition achieved |
| Conduction power to coils | 111 MW | stellaris-design-details.md §Table 3 | high | Thermal load on cryogenic system; significant recirculating power contribution |
| Stored magnetic energy | 111 GJ | stellaris-design-details.md §Table 3 | high | Large; quench protection engineering challenge |
| Average plasma power density | 6.1 MW/m³ | stellaris-design-details.md §Table 3 | high | |
| Average first wall load | 4.05 MW/m² | stellaris-design-details.md §2.7 | high | Design heat flux limit for tungsten armor |
| TBR (baseline) | 1.1070 ± 0.0002 | stellaris-design-details.md §2.8 | high | Monte Carlo; homogenized, no penetrations |
| TBR (post-correction, with ports) | 1.074 | stellaris-design-details.md §2.8 | high | After 3% port correction; margins applied |
| Li-6 enrichment | 70% | stellaris-design-details.md §2.8 | high | Required to achieve TBR > 1.05 |
| REBCO magnet lifetime | ~10 full-power years at 2.7 GW | stellaris-design-details.md §2.8 | medium | At allowable fluence 3×10²² m⁻²; magnet replacement is a planned plant-life event |
| Fast neutron flux (99th quantile at coil) | 9.5 × 10¹³ n/m²/s | stellaris-design-details.md §2.8 | medium | Drives magnet lifetime estimate |
| Operation mode | Steady-state, disruption-free | dossier.md §Operation Mode | high | Inherent stellarator property |
| **Capacity factor** | **85–95%** | **[analogue: helios-stellarator-comparison.md §2; en-wiki-wendelstein-7-x.md; disruption-free steady-state argument]** | **medium** | **Helios design targets 88%; W7-X demonstrated >97% experimental run-time. Key experimental milestones: February 2023 — 30-minute continuous discharge demonstrating "an essential feature of a future fusion power plant: continuous operation"; June 2025 — 1.8 GJ energy record in 6-minute run using continuous pellet injection, surpassing EAST tokamak's 2025 record. These are the strongest direct evidence for the stellarator long-pulse advantage underpinning the 85–95% CF range. Plant availability floor set by blanket/divertor scheduled maintenance; disruption-free operation removes a major tokamak availability-limiting event. The lower bound (85%) is constrained by the blanket/divertor replacement interval (see row below): at a 4-week outage per replacement and a 1-year interval, availability ceiling is ~92%; at a 4-week outage per 4-year interval, ceiling is ~98%. The specific downtime per replacement event for Stellaris is a critical missing input (Gap #7).** |
| Blanket/divertor replacement interval | 1–4 years | arxiv-2501-04640.md (abstract; HSR3 context) | low | General stellarator reactor constraint from Queral et al. (2025): "blankets and divertor modules will have to be replaced periodically (about each 1–4 years depending on the design) due to neutron damage, and also erosion of divertor targets." Not Stellaris-specific; applicable as calibration for the availability lower bound. The specific downtime per replacement event (days or weeks) is unknown and is the critical missing input for Gap #7 (O&M cost breakdown). |
| Alpha demo capital cost | €2 billion | proxima-fusion-2026-updates.md §Agreement | high | For Alpha (Q>1, non-commercial demo, ~2031) at Garching |
| Confinement scaling used | ISS-04 with confinement factor | stellaris-design-details.md §Table 4 | high | Energy confinement scaling; standard for stellarators |

**Helios Analogue Parameters** (Thea Energy QI stellarator; not Stellaris, but same confinement family):

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion power (Helios) | 958 MW | helios-stellarator-comparison.md §2 | high | ~3× smaller than Stellaris target |
| Net electrical (Helios) | 390 MWe | helios-stellarator-comparison.md §2 | high | |
| Gross thermal efficiency (Helios) | 40% | helios-stellarator-comparison.md §2 | high | Steam Rankine, vanadium FW (higher T than EUROFER97) |
| Capacity factor (Helios) | 88% | helios-stellarator-comparison.md §2 | high | Design target |
| ECRH startup power (Helios) | 10 MW | helios-stellarator-comparison.md §3.1 | high | Over hours-long startup |
| ECRH ignited steady-state (Helios) | 1 MW | helios-stellarator-comparison.md §3.1 | high | "Only nominal heating (1 MW) is required once plasma self-heats" |
| Peak field on-coil (Helios) | 20 T | helios-stellarator-comparison.md §2 | high | Planar coil design; REBCO tape |
| Volume-averaged beta (Helios) | 2.7% | helios-stellarator-comparison.md §2 | high | Consistent with Stellaris (2.76%) |
| Tritium startup inventory | 1–2 kg | helios-stellarator-comparison.md §4.3 | medium | Applicable to all D-T stellarators of this scale |
| TBR (Helios, with engineering losses) | 1.1 | helios-stellarator-comparison.md §4.3 | high | Consistent with Stellaris 1.074 |

> "Net electric power: 390 MWe... Thermal conversion efficiency: 40%... enabling an 88% capacity factor"
> — helios-stellarator-comparison.md, §2 (Table 1 global parameters)

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown (CAS20–CAS80) | proprietary | blocking | No cost figures published for Stellaris; internal cost optimization referenced but not disclosed |
| Major radius / plasma volume | not-yet-sourced | blocking | Required to derive first wall area and blanket mass independently; not in public sources |
| Q value (plasma gain) | not-yet-sourced | important | Can be roughly inferred (~54 from 2,700 MW / 50 MW ECRH) but not stated; Alpha targets Q>1 only |
| Gross thermal efficiency (Stellaris-specific) | derivable | important | Inferred ~38–40% from steam Rankine + EUROFER97 limit; Helios analogue gives 40% |
| O&M cost breakdown | truly-unknown | important | No source contains scheduled vs. unplanned maintenance cost split; magnet replacement interval (10 yr) adds a non-standard O&M item |
| 3D coil manufacturing cost per unit | truly-unknown | blocking | Key sensitivity parameter; SMC demo (2027) will provide first real data point |
| Plasma current / rotational transform profile | not-yet-sourced | important | Structural constraint on confinement scaling and bootstrap current; not stated publicly |
| Coil number and per-coil mass | not-yet-sourced | important | Affects remote maintenance scheme and coil replacement cost |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Capital cost estimate for Stellaris plant | S1, S5 | proprietary | blocking | Proxima internal; ARIES-CS LTS stellarator studies as floor analogue — but ARIES-CS studied QA (quasi-axisymmetric) configurations, not QI; the analogue gap extends beyond LTS→HTS to include different symmetry classes with potentially different coil topology costs. Brown (2018) for relative account weights. |
| 2 | Major radius and plasma volume | S5 | not-yet-sourced | blocking | Full Stellaris paper (paywalled); derivable from published power density (6.1 MW/m³) and fusion power if plasma volume is given |
| 3 | 3D HTS coil manufacturing cost per coil | S2, S5, S7 | truly-unknown | blocking | SMC demo (2027) first data point; W7-X LTS coil cost per unit as historical floor |
| 4 | Gross thermal efficiency and power cycle specification | S1, S5 | not-yet-sourced | important | Full Stellaris paper; Helios analogue (40%) is best available proxy |
| 5 | Capacity factor target for Stellaris | S5, S7 | proprietary | important | Proxima has not published; Helios (88%) is primary analogue; W7-X operational availability provides physics basis |
| 6 | Q value and steady-state ECRH requirement post-ignition | S2, S5 | not-yet-sourced | important | Full Stellaris paper; resolves H4 branching condition |
| 7 | O&M cost breakdown (fixed vs. variable, scheduled maintenance intervals) | S3, S5 | truly-unknown | important | No fusion stellarator O&M cost models published; ARIES-CS provides rough analogue |
| 8 | Engineering TBR after all blanket penetrations and module supports | S2, S5 | not-yet-sourced | important | Full Stellaris paper claims 1.074 post-correction; additional engineering losses not yet quantified |
| 9 | Island divertor power handling validation at burning plasma density | S2, S3 | truly-unknown | important | W7-X high-performance experiments provide best data; no burning plasma equivalent available before Alpha demo |
| 10 | REBCO tape total demand per plant (3D stellarator geometry) | S4 | derivable | important | Derivable from magnet cross-section and stored energy (111 GJ) with assumptions about conductor current density; no published estimate |
| 11 | Coil number, per-coil mass, and replacement scheme | S3, S5 | not-yet-sourced | important | Full Stellaris paper §2.11 (remote maintenance) likely contains this |
| 12 | Plasma current profile and bootstrap fraction | S2 | not-yet-sourced | nice-to-have | Affects recirculating power and operational complexity |

---

## Section 7: Cross-Concept Notes

### Nearest-Neighbor Positioning

Stellaris occupies a specific region in the fusion concept design space: **high-field QI stellarator, HTS magnets, D-T fuel, commercial power plant, European private sector**. Its three nearest neighbors are:

1. **Helios / Thea Energy** (United States) — the closest within-family comparator: another private-sector commercial plant study using QI magnetic optimization and HTS planar coil arrays. Key similarity: same physics optimization family (quasi-axisymmetric / QI), same D-T fuel, same HTS REBCO technology, same approximate beta (~2.7%). Key difference: Helios uses planar convex coil arrays (simpler to wind, lower manufacturing risk) whereas Stellaris uses non-planar modular coils (stronger field per conductor, more complex geometry). Helios's 40% thermal efficiency versus Stellaris's ~32% reflects Helios's use of vanadium alloy structural material (higher temperature) vs. Stellaris's EUROFER97 choice (lower temperature, more proven supply).

2. **EUROfusion HELIAS concept / W7-X → DEMO pathway** (EU public sector) — the large-device public-sector QI stellarator lineage. Key similarity: same QI physics heritage from Max Planck IPP, same WCLL blanket concept, same EUROFER97 structural steel. Key difference: HELIAS/EU-DEMO targets a much larger device at lower field with LTS or mixed LTS/HTS conductors; Stellaris's compactness strategy via high-field HTS is the private-sector departure from this path. W7-X is the direct experimental ancestor for both.

3. **Type One Energy** (United States) — another HTS stellarator startup using modular coil architecture, targeting solid ceramic breeder (HCPB) rather than WCLL blanket. Not yet at commercial plant study stage publicly. Similar driver technology bet (3D HTS coil manufacturing) but different blanket and heating system choices.

### Shared Assumptions with Prior Analyses

The following assumptions are borrowed from the HTS compact tokamak analysis (01-hts-compact-tokamak):

- **REBCO tape supply chain constraints**: Same global production capacity issue (~thousands km/year vs. multi-thousand km/plant demand); cost trajectory from ~$30–100/kA-m toward $10/kA-m target; key manufacturers Shanghai Superconductor Technology, Faraday Factory Japan. The stellarator tape demand per plant is likely higher per unit net electric output due to 3D coil geometry and larger stored energy at equivalent fusion power.
- **Tritium supply dynamics**: Global civilian inventory ~25–30 kg; TBR > 1 not optional; sequencing constraint for early fleet deployment. Stellaris TBR = 1.074 provides only modest margin.
- **Regulatory framework**: Same NRC / international regulatory uncertainty for fusion as for tokamaks. Stewart & Shirvan (2022) fission-style regulatory markup (2.2×) applies equally if fusion regulatory framework defaults to fission-style.
- **D-T fuel cycle infrastructure**: Tritium extraction from PbLi; same order-of-magnitude tritium startup inventory (~1–2 kg, per Helios analogue [helios-stellarator-comparison.md §4.3]).

### CAS-Level Cost Delta: Stellaris vs. HTS Compact Tokamak Reference

The following table shows the directional cost delta for each major CAS account relative to the 01-hts-compact-tokamak (CFS ARC-class) reference concept. Direction: "+" = Stellaris more expensive, "−" = Stellaris less expensive, "0" = comparable.

**CAS account structure note:** The model uses the standard ARIES/fusion CAS20X convention, where CAS22 (Reactor Plant Equipment, $3,142M) is a super-account containing all nuclear island sub-accounts. The coil system lives at C220103 and heating at C220104 — both within CAS22, not at a separate CAS21. This differs from PROCESS-style per-subsystem top-level numbering; "CAS21" in the model is Buildings ($930M), not magnets.

| CAS Account | Direction | Magnitude | Basis | Notes |
|-------------|-----------|-----------|-------|-------|
| **C220103 (under CAS22): Coils** | **Large +** | **1.5–5×** | Brown (2018); no commercial HTS stellarator precedent | 3D non-planar coil geometry vs. D-shaped wound coils; primary LCOE uncertainty. Includes higher cryogenic load (111 MW conduction). Model default ($516M) is lower bound — 3D manufacturing premium not modeled. |
| **C220104 (under CAS22): Heating System** | **Large −** | **−50% to −80%** | helios-stellarator-comparison.md §3.1 (1 MW ignited) | ECRH only; no NBI, no ICRF, no CS; no current drive needed. Conditional on H4: if 50 MW sustained, advantage largely disappears. No CS cost is a firm saving. |
| **C220101 (under CAS22): First Wall / Blanket** | **Small +** | **5–15%** | stellaris-design-details.md §2.7, §2.8 | 3D curved tungsten tile fabrication premium over flat tokamak tiles; WCLL complexity adapted to helical geometry. WCLL vs. FLiBe: WCLL likely somewhat simpler than ARC-class FLiBe (lower temperature, water coolant). Net: small positive delta due to geometry, partially offset by blanket simplicity. |
| **C220108 (under CAS22): Divertor (Island)** | **Small −** | **uncertain; directional only** | stellaris-design-details.md §2.5; W7-X heritage; Challenge 5; Gap #9 | The island divertor provides a larger wetted area than a tokamak poloidal divertor, distributing heat load over a greater surface and reducing peak heat flux concentration — potentially reducing divertor hardware cost per unit heat load handled. W7-X heritage gives the concept credibility: "Stellarators do not exhibit the unfavorable 'Eich-scaling' of heat exhaust deposition width on divertor plates seen in tokamaks" [stellaris-design-details.md §2.5]. The Stellaris divertor is tungsten-based, operating in strong detachment steady-state — a geometry the tokamak poloidal divertor does not share. **Caveat**: the island divertor geometry is tightly constrained by the magnetic topology (no independent redesign freedom if it underperforms), and port-access constraints from the modular coil architecture limit maintenance accessibility — this O&M penalty is already captured in the structural "+" row below. On a pure hardware-cost-per-unit-heat-load basis the direction is Small −; on a lifecycle-inclusive basis the O&M constraint partially offsets this. Magnitude is uncertain because no Stellaris divertor cost estimate has been published and burning-plasma power density validation remains open (Gap #9). |
| **CAS24: Heat Transport** | **Small −** | **~−10%** | WCLL water cooling vs. FLiBe (ARC) | Water-cooled WCLL is a more mature industrial technology than FLiBe molten salt; lower-temperature primary loop simplifies heat transport engineering. |
| **CAS25: Power Conversion** | **Small −** | **~−5–10%** | [inferred: water Rankine vs. sCO₂ Brayton technology cost differential] | Water Rankine at ~500°C (EUROFER97 temperature limit) is a significantly cheaper technology per unit thermal capacity than sCO₂ Brayton at higher temperatures: lower capital cost per GWth, mature industrial supply chain, no novel turbomachinery. This technology cost discount is the primary driver of the "Small −" direction. Note the competing effect: 32% efficiency requires ~3.1 GWth input to deliver 1 GWe net, vs. ~2.5 GWth for a 40%-efficient reference — requiring a larger steam plant at fixed net output. The Rankine cost-per-GWth advantage must outweigh this additional thermal throughput to yield a net "−" direction; the small magnitude reflects this tension, and the direction could be "0" if steam plant sizing dominates. The direction is not driven by lower efficiency per se — at fixed net output, lower efficiency always requires more thermal plant, not less. |
| **CAS26: Fuel Cycle / Tritium** | **0 (neutral)** | — | Shared D-T infrastructure | Comparable tritium breeding complexity; PbLi vs. FLiBe tritium extraction both undemonstrated at scale. |
| **CAS27: Balance of Plant** | **0 (neutral)** | — | Standard electrical, water, cooling towers | No major structural difference at BoP level. |
| **CAS21: Buildings / Site** | **Small +** | **5–15%** | [inferred: machine footprint differential; Gundremmingen site reuse offset] | Two competing effects: (a) reactor building volume scales with machine footprint — a QI stellarator with R0 ≈ 13 m requires a substantially larger containment and assembly building than an ARC-class compact tokamak (R0 ≈ 3–4 m), driving a positive delta; (b) Proxima targets the decommissioned Gundremmingen nuclear site, which reduces land acquisition and permitting cost, providing a partial offset. Site reuse reduces site prep cost, not reactor building volume. Net direction: small positive. See Challenge 2 for the machine scale narrative that logically links to this account. |
| **Net directional assessment** | **Uncertain** | Dominated by C220103 vs. C220104 | The competitiveness case depends entirely on whether the 3D coil manufacturing premium (large +) is more than offset by: the H&CD saving (large −, conditional on ignition) + the capacity factor advantage (not in table — affects LCOE denominator, not capital cost). **Important:** the base LCOE of $106/MWh (Scenario A) excludes periodic magnet replacement, which adds $4.5–$22/MWh depending on coil multiplier (see model_output.txt replacement sweep). This cost is not shared by the compact HTS tokamak reference, making the raw $106/MWh figure a stellarator-specific lower bound. The replacement-inclusive LCOE at the optimistic 1.5× coil multiplier is $117.6/MWh vs. $110.9 initial-build only. |

**O&M Cost Delta — Structural Port-Size Disadvantage**

Queral et al. (2025) state that the periodic blanket and divertor replacement requirements "imply relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks" [arxiv-2501-04640.md, abstract]. This is a structural, not design-specific, consequence of modular stellarator coil architecture: convoluted non-planar coil sets leave less room for large maintenance ports than a tokamak's toroidal geometry. The CAS delta table has no explicit O&M row, but the port-size argument provides a directional cross-concept signal independent of Stellaris-specific choices: **stellarator O&M cost is structurally higher (+) than an HTS compact tokamak reference at unknown magnitude**, because blanket and divertor module size and accessibility are constrained by coil geometry in all advanced stellarators with non-planar modular coils. This complements Gap #11 (constrained divertor geometry, stellarator-specific) and Gap #7 (O&M cost breakdown, truly unknown). The magnitude of the disadvantage depends on the as-built remote maintenance scheme and is not quantifiable from available sources.

> "Eliminating the need for an expensive plasma current drive system"
> — stellaris-design-details.md, §Introduction (Key stellarator economic advantage)

> "Greatly reduces the need for active control of the plasma — circumventing the need for in-vessel coils, which present challenges in environments subjected to high neutron fluxes"
> — stellaris-design-details.md, §Introduction (Active control cost saving)

---
[1] 01-hts-compact-tokamak analysis, §Key Materials: REBCO supply chain; tritium supply dynamics; regulatory framework
[2] helios-stellarator-comparison.md §2: capacity factor 88%, thermal efficiency 40%, confirmed analogue for Stellaris gap-filling
[3] Brown (2018) IEEE TPS: stellarator vs. tokamak comparative cost framework — referenced for CAS21 direction
[4] stellaris-design-details.md §Introduction: H&CD cost advantages explicitly stated

---

## Section 8: Sources

**Primary Sources (extracted documents)**

1. **stellaris-design-details.md** (337 KB) — Extracted from: Proxima Fusion, "Stellaris: A high-field quasi-isodynamic stellarator for a prototypical fusion power plant," *Fusion Engineering and Design*, Vol. 214, May 2025 (DOI: 10.1016/j.fusengdes.2025.114868; also KIT repository: publikationen.bibliothek.kit.edu/1000179851). The primary engineering reference for this analysis. Covers plasma design, first wall, blanket, divertor, magnets, neutronics, support structures, and remote maintenance. Framed by authors as "version 1" of a QI stellarator commercial plant concept. Paywalled on ScienceDirect.

2. **helios-stellarator-comparison.md** (132 KB) — Extracted from: Thea Energy, "Helios: A Planar Coil Stellarator Fusion Power Plant," arXiv:2512.08027v1 (December 2024). Pre-conceptual design of a QI stellarator commercial plant using planar coil arrays with REBCO HTS. Open access. Used in this analysis as the primary analogue source for parameters not published in Stellaris: thermal efficiency (40%), capacity factor (88%), ECRH ignited power (1 MW), divertor engineering, and blanket design details. Directly comparable physics family (QA/QI optimization, D-T, HTS).

3. **proxima-fusion-2026-updates.md** (8 KB) — Coverage of Proxima Fusion MoU signed February 2026 with RWE, Free State of Bavaria, and Max Planck IPP. Provides Alpha demo specifications: €2 billion, Q>1, 2031 target, Garching site; Stellaris siting at Gundremmingen (decommissioned RWE nuclear plant). Also: up to €400 million Bavarian High-Tech Agenda support, 1,000-job magnet factory.

4. **proxima-fusion-technology-page.md** (4 KB) — Proxima Fusion technology overview page. Confirms QI design philosophy, W7-X heritage, HTS magnets, steady-state operation, island divertor, and Stellaris as a peer-reviewed plant concept. High-level; no quantitative parameters.

**Comparative and Background Sources (referenced, not extracted)**

5. **Brown, T.G. (2018)** — "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. The only published comparative cost decomposition across stellarator and tokamak geometries. Used to support the CAS21 directional cost delta (stellarator magnet premium). Available at: ieeexplore.ieee.org/abstract/document/8361148.

6. **ARIES Team (various, late 1990s–early 2000s)** — ARIES-CS and ARIES-AT conceptual design studies for optimized stellarators with LTS conductors. Only plant-level cost breakdowns for the stellarator concept family. Basis values, not NOAK. Available at: qedfusion.org/DOCS/bib.shtml.

7. **W7-X operational publications** — W7-X island divertor validation and high-performance plasma results. Provides the physics basis for stellarator divertor performance claims. Proxima blog (proxima-fusion-technology-page.orig.md) summarizes W7-X heritage.

**Cross-Concept Comparators**

8. **arxiv-2512-08825.md** — Extracted from: CIEMAT team, "CIEMAT-QI4X: A quasi-isodynamic stellarator configuration with resilient island divertor compatibility," arXiv:2512.08825 (December 2025). Pre-print presenting a four-field-period QI stellarator configuration that demonstrates beta tolerance up to 4% while maintaining small neoclassical and turbulent transport, good fast-ion confinement, small bootstrap current, and edge island structure compatible with an island divertor. Used in this analysis as evidence that Stellaris's 2.76% design-point beta is a v1 choice, not a QI physics ceiling; provides the upper-bound beta reference for the higher-beta scenario branch (H2a).

**Phase 1a Dossier**

9. **dossier.md** — Phase 1a research summary: 2 iterations, 12 differentiation columns, overall confidence medium. 8 high-confidence values, 4 medium-confidence values. Summary statistics: peak fusion power 2.7 GW, net electrical ~1 GW, W7-X heritage confirmed, HTS REBCO magnets at 20 T, WCLL TBR 1.07, steady-state disruption-free operation. Location: `exploration/phase_1a/research/09-qi-stellarator-hts/dossier.md`.
