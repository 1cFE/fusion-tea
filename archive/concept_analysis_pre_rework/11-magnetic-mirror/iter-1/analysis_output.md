# D1+ Analysis: Magnetic Mirror (D-T) — Realta Fusion

**Concept**: Axisymmetric tandem mirror (CoSMo — Compact, Scalable, Modular) with HTS REBCO magnets and hybrid thermal + direct energy conversion — D-T fuel
**Company**: Realta Fusion (Madison, WI — UW-Madison spinout, founded 2022)
**Development Stage**: Experimental (WHAM operational July 2024) → End-plug demonstrator (Anvil, ~2028) → Pilot plant (Hammir, mid-2030s)
**Confinement Family**: MFE (linear open-ended magnetic confinement)
**Operation Mode**: Steady-state

---

## Section 1: Availability of Data

**Rating: Limited**

Realta Fusion is more transparent than many private fusion companies at a comparable stage. One peer-reviewed confinement modeling paper exists specifically for their commercial design (arXiv:2411.06644), and the WHAM experiment has produced citable results. The APS DPP 2025 conference talk by Sutherland provides quantitative pilot plant performance targets. However, no plant-level cost study, engineering design report, or techno-economic analysis has been published for any modern HTS-based magnetic mirror. The company explicitly expects to publish a Hammir pre-conceptual design paper in 2026, which would substantially improve data availability.

**Peer-reviewed and conference publications:**
The arXiv confinement predictions paper (arXiv:2411.06644) is the primary quantitative anchor for commercial performance claims. It models Q = 5.8 at a 50-meter center cell (Optimum operating point, Table 3). The Q > 10 extrapolation for longer center cells is a secondary characterization from The Fusion Report interview — not a direct arXiv result. The APS DPP 2025 abstract (Sutherland) states Hammir targets Qe > 1 and Pe > 50 MWe for at least 3 hours continuously, with Anvil serving as the end-plug physics demonstrator. The WHAM physics basis paper (Endrizzi et al., Journal of Plasma Physics, 2023) provides the experimental foundation.

> "50-meter center cell → Q = 5.8 (Optimum operating point)"
> — arxiv-2411-06644-confinement-predictions.md, Table 3 (primary source for 50 m operating point)

> "Q > 10 possible with longer center cell" (extrapolated from 50 m scaling behavior)
> — fusion-report-interview-realta.md (secondary-source characterization of arXiv scaling; specific length not given)

> "electric gain Qe > 1, net electricity Pe,out > 50 MWe, for at least 3 hours continuously"
> — aps-dpp-2025-sutherland.md, §Hammir Facility (Pilot Plant)

**Company communications:**
The Fusion Hub Startup Spotlight and The Fusion Report interview with Realta are the richest available sources for system architecture, confirming D-T fuel, HTS REBCO magnets (mirror ratio 10+), dual energy capture (venetian blind DEC + thermal blanket), and the ~7 MW/m center cell scaling law. The February 2026 SVB facility announcement ($9.5M growth capital) confirms ongoing operations and identifies industrial heat delivery as the primary near-term application.

> "neutron energy is captured through traditional thermal blankets (which also produce tritium from lithium)... charged helium 'ash' is captured via direct energy conversion as it exits the fusion chamber. Dual approach lowers the Q required to reach net-electric while still using DT fuel"
> — fusion-report-interview-realta.md, §Energy Conversion

**Historical analogues:**
The Mirror Advanced Reactor Study (MARS, 1983) and MINIMARS (1985) are the most detailed magnetic mirror plant studies in existence. MARS projected ~7 ¢/kWh (1983 dollars) with LCOE saturating around 600 MWe, using LiPb blanket (TBR 1.15) and gridless direct converters achieving ~54% efficiency. Both studies used yin-yang coils at mirror ratios of ~2, which are not directly applicable to Realta's HTS axisymmetric design, but they provide the only bottom-up cost account structure for a mirror power plant.

**Independent analyses:**
No independent TEA for a modern HTS magnetic mirror exists. The 1costingfe-based quantitative models in the handwritten and automated analyses (80.2 vs. 135.2 $/MWh) represent the two available parametric estimates, but these are first-pass academic exercises with significant parameter disagreements, not peer-reviewed plant studies.

**Key data gaps limiting this analysis:**
1. No Hammir engineering design study (expected 2026)
2. No published cost targets for any subsystem in the Realta design
3. Blanket type unspecified (FLiBe, LiPb, liquid Li, HCPB)
4. NBI and ECH input power for commercial Hammir not disclosed
5. Recirculating power fraction for Hammir not published
6. DEC efficiency in D-T fusion conditions not demonstrated or published by Realta

---
[1] arxiv-2411-06644-confinement-predictions.md, §Hammir Design
[2] aps-dpp-2025-sutherland.md, §Hammir Facility (Pilot Plant) and §Anvil Device (Next Step)
[3] fusion-report-interview-realta.md, §Energy Conversion; realta-fusion-hub-spotlight.md §Fuel & Reaction

---

## Section 2: Challenges in Capturing System Function

Ranked by impact on LCOE model closure.

### 1. End-Plug Confinement Physics Is Concept-Gating (Impact: Blocking)

The fundamental economic claim of the tandem mirror rests on end-plug stability: hot, dense end-plug plasmas must create an electrostatic potential barrier deep enough to confine the main-cell ions at commercial Q. Realta's HTS REBCO magnets achieve mirror ratios of 10+ (vs. historical ~2), which they argue fundamentally improves end-plug confinement effectiveness. However, the Anvil end-plug demonstrator has not yet been built, and the performance of electrostatic end-plugging at the conditions required for Q > 5 has never been experimentally validated.

The key instability risks are DCLC (drift cyclotron loss cone) and Alfvén ion cyclotron modes, both cited as requiring active stabilization via kinetic injection (sloshing ions) and vortex flows. The arXiv paper explicitly acknowledges that "stabilization against MHD and trapped particle modes" is required and applies machine learning optimization to the design parameters — indicating that the stabilization solution is still being developed computationally [1]. If DCLC management is less effective than modeled, the achievable Q drops substantially. The comparison-report analysis from the prior automated pipeline characterized the end-plug physics challenge as "comparable to claiming Q=10 before achieving burning plasma" — a strong statement that remains operative.

Quantifying the LCOE impact: a factor-of-2 reduction in Q (e.g., from Q=5 to Q=2.5) at fixed net electrical output would roughly double the required fusion power and the input heating power, driving up the recirculating fraction from ~35% to potentially >50% and eliminating net electricity production at modest plant sizes.

### 2. The Linear Scaling Thesis Is Physically Plausible but Uncosted (Impact: Critical)

Realta's core economic argument is that the center cell is modular and cheap: each additional meter adds ~7 MW of fusion power while input power remains roughly constant, enabling Q to scale with length without requiring larger or more expensive end-plug systems. This physics claim is stated in the Fusion Report interview and is consistent with the arXiv paper's Q projections. If true, it implies a uniquely favorable cost scaling — longer plants approach higher Q at roughly constant capital per MWe for the heating systems.

> "~7 MW per meter as center cell lengthens... Input power remains constant despite increased output... Theoretical: 500 MW from Q=20 system"
> — fusion-report-interview-realta.md, §Performance Scaling

However, the cost per meter of center cell has never been estimated in any modern study. MARS costed its full 100-meter device, but the magnet technology, building, and blanket cost structures were completely different. The center cell coil costs scale with the number of solenoid modules; the building scales approximately linearly with length; the blanket area scales with length; but none of these have been estimated for an HTS axisymmetric design. The linear scaling thesis may be economically transformative or may simply shift cost growth from heating to structural systems — and no data exists to determine which.

### 3. Recirculating Power Fraction Is Unknown and Potentially Large (Impact: Critical)

A steady-state mirror requires continuous NBI and ECH input to sustain end-plug temperature and density. For WHAM, the heating systems include a 110 GHz gyrotron (ECH), NBI, and HHFW. The commercial Hammir input power is not published. The handwritten model used 40 MW input and the automated model used 100 MW, producing Q_plasma estimates of 28 and 17 respectively — both physically implausible at face value, indicating that the parameter is genuinely undetermined.

For context: the MARS study (1983 technology) required substantial recirculating power to maintain its end plugs. Modern NBI and ECH systems are more efficient, but the end-plug sustainment power demand depends critically on DCLC stability behavior. If end-plug conditions require more heating than modeled, the recirculating fraction could rise significantly above the ~35% baseline (automated model estimate), reducing Qe below 1 and eliminating the net electricity claim. This is the physical lever that most directly couples the Section 2.1 stability risk to LCOE.

### 4. DEC Contribution: Real but Modest for D-T (Impact: High)

The venetian blind direct energy converter is a genuine Realta differentiator. However, its thermodynamic contribution in D-T is limited by physics: 80% of D-T fusion energy is carried by 14.1 MeV neutrons (captured in the thermal blanket) and only 20% by the 3.5 MeV alpha particles (capturable by DEC). At ~54% DEC efficiency (MARS historical value), the electrical contribution from DEC is at most 0.20 × 0.54 ≈ 11% of the thermal output. This is meaningful but not transformative. The handwritten analysis's dismissal of DEC as "not worth considering" overstates the case (11% is real), but its observation that DEC survivability — thin, uncooled electrodes downstream of a fusion reactor — is a genuine engineering concern is correct and unaddressed in Realta's published materials.

The uncertainty range: if DEC is excluded entirely (f_dec = 0), LCOE rises by roughly 10-15% from the baseline. If DEC works at MARS efficiency (η_de = 0.54), it provides meaningful but not game-changing improvement. The decision of whether to include DEC in the model has modest LCOE impact but is relevant for plant complexity and cost.

### 5. Tritium Breeding: Blanket Type Undisclosed, TBR Unverified (Impact: High)

The Fusion Report interview confirms a lithium-based blanket that captures neutron energy and breeds tritium. The specific blanket architecture (FLiBe, LiPb, liquid Li, solid ceramic HCPB) is not disclosed by Realta. This matters for cost modeling because blanket type drives: (a) breeding ratio (TBR), (b) thermal efficiency (outlet temperature varies from ~350°C for LiPb to >700°C for FLiBe), (c) blanket structural cost, and (d) tritium extraction complexity. MARS used LiPb (TBR 1.15), but this was optimized for yin-yang coil geometry. Realta's cylindrical center cell with axisymmetric blanket geometry is well-suited to a cylindrical breeding module, which could support any of these options with different cost consequences.

---
[1] arxiv-2411-06644-confinement-predictions.md, §Key Technical Details
[2] fusion-report-interview-realta.md, §Performance Scaling
[3] realta-fusion-hub-spotlight.md, §Stabilization

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest LCOE model risk) to most mature.

---

**Tritium Breeding Blanket — TRL 2–3**

- **Demonstrated**: Small-scale tritium breeding experiments in fission-neutron environments globally. MARS/MINIMARS costed LiPb blanket with TBR 1.15 for a linear mirror geometry — the closest available analogue. Kairos Power (fission) developing FLiBe at scale but at very different operating conditions.
- **On paper only**: A blanket design for Realta's axisymmetric cylindrical center cell. No Hammir blanket architecture has been published. The 2026 pre-conceptual design paper is expected to address this.
- **Missing at scale**: TBR >1 validated with 14 MeV fusion neutrons. Any tritium extraction system at kg/day throughput. Full-scale lithium blanket module operating under simultaneous neutron flux, thermal load, and tritium extraction for a linear device.

---

**End-Plug Confinement System (Tandem Mirror Cells) — TRL 3–4**

- **Demonstrated**: Tandem mirror physics demonstrated at TMX and MFTF-B (1980s, now decommissioned). Realta's WHAM demonstrates the end-plug magnetic geometry (17 T HTS solenoid) and basic plasma operation (first plasma July 2024). WHAM targets validation of the end-plug plasma confinement physics.
- **On paper only**: Stable, sustained end-plug operation at commercial Q conditions. Electrostatic plugging potential sufficient to confine main-cell D-T plasma at Q > 5. DCLC stabilization via sloshing ions and vortex flows at commercial densities and temperatures.
- **Missing at scale**: The Anvil device (planned ~2028) is the first dedicated end-plug confinement demonstrator. Commercial-scale end-plug plasma parameters — end-plug density, electron temperature, and electrostatic potential barrier depth — have not been achieved or validated in any experiment.

---

**Direct Energy Conversion — Venetian Blinds — TRL 4–5**

- **Demonstrated**: Venetian blind direct energy converter demonstrated in laboratory settings in the 1970s by Moir & Barr (Nuclear Fusion, 1973). Achieves ~50–65% efficiency for monoenergetic ion beams. MARS incorporated DEC at ~54% efficiency in its plant design.
- **On paper only**: Axisymmetric ferromagnetic venetian blind geometry as described by Realta. Integration with the full mirror end region, including magnetic field expansion to reduce heat flux on electrodes.
- **Missing at scale**: Survival of thin uncooled electrodes under continuous bombardment from a D-T fusion plasma exhaust stream (including neutron activation, energetic neutral particles, and alpha particles). No DEC device has operated in fusion conditions. DEC survivability over commercial plant lifetime (30 years) is undemonstrated and not analyzed in available Realta materials.

---

**End Divertor and Heat Exhaust Management — TRL 2–3**

- **Demonstrated**: The open-ended mirror geometry naturally creates two loss-cone "divertors" at the ends of the machine. Heat load handling at relevant particle and energy fluxes has not been specifically studied for Realta's design.
- **On paper only**: Any analysis of end divertor heat loads for a Hammir-class device operating at Q > 5.
- **Missing at scale**: Heat flux on end structures and venetian blind electrodes at commercial fusion power. Plasma exhaust pumping and fueling systems for the tandem end regions. Remote handling of activated end structures in a linear geometry (hot-cell operations would require access along the full machine length).

---

**HTS Axisymmetric Mirror Magnets — TRL 6–7**

- **Demonstrated**: WHAM operates with two CFS-built REBCO HTS solenoid magnets at 17 T in-bore (>20 T on conductor [unverified in ingested sources; likely from Endrizzi et al. 2023 WHAM physics basis paper]), achieving a world-record field for magnetically confined plasma experiments at WHAM's scale. Axisymmetric solenoid coil geometry is geometrically simpler than 3D stellarator coils or MFTF-B yin-yang coils. CFS has demonstrated commercial HTS magnet manufacturing capability.
- **On paper only**: Full complement of center-cell solenoid modules and end-mirror coils for Hammir (50-meter design). Cost per meter at commercial length not estimated.
- **Missing at scale**: Radiation shielding design for HTS coils in a 14 MeV neutron environment over 30-year plant lifetime. Large-magnet-radius implications of neutron shielding layers (shielding increases the physical distance between coil and plasma, potentially increasing coil stress and cost). Integration of multiple center-cell solenoid modules with demountable connections for maintenance.

> "Two 17 T HTS magnets from Commonwealth Fusion Systems... world record magnetic field strength for magnetically confined plasmas"
> — wham-experiment-details.md, §Magnet System

---

**Neutral Beam Injection (NBI) — TRL 6–7**

- **Demonstrated**: NBI systems routinely operated on major fusion experiments globally (JET, JT-60SA, DIII-D). WHAM uses NBI for end-plug fueling and heating. Modern NBI technology at 80–120 keV beam energy and multi-MW power levels is commercially available from multiple vendors.
- **On paper only**: NBI power requirements for Hammir at commercial Q conditions. Optimal beam energy and injection geometry for Realta's tandem mirror configuration.
- **Missing at scale**: High-power NBI systems with >50% wall-plug efficiency at sustained commercial operation. NBI port penetrations in a 50-meter cylindrical center cell at a small fraction of surface area (a cited Realta advantage — the long center cell allows NBI penetration without large fractional port area).

---

**ECH and HHFW Heating Systems — TRL 6–7**

- **Demonstrated**: 110 GHz gyrotron ECH demonstrated in WHAM for electron heating and end-plug potential formation. HHFW (high-harmonic fast wave) systems demonstrated in multiple fusion devices. Gyrotron manufacturing at MW class is commercially available.
- **On paper only**: ECH and HHFW power requirements at Hammir commercial conditions. Gyrotron wall-plug efficiency optimization for ~45–55% efficiency range at sustained high power.
- **Missing at scale**: Long-pulse, high-reliability gyrotron operation in a neutron environment. Cost reduction pathway from current ~$1M/MW gyrotron costs to commercially competitive levels.

---

## Section 4: Key Materials and Supply Chain Considerations

**HTS REBCO Tape**

REBCO is the most immediate supply chain constraint. Realta's WHAM required $50M in REBCO tape from CFS for its two end-mirror magnets. A commercial Hammir plant with ~50 meters of center cell solenoids plus two end-mirror coils would require substantially more — the end-mirrors are the field-intensive components while the center-cell solenoids operate at lower field (a stated cost advantage), but the total tape length could run to hundreds or thousands of km depending on center-cell field strength design. Global REBCO production capacity is currently on the order of thousands of km/year and is ramping, with key manufacturers including Shanghai Superconductor Technology, Faraday Factory Japan, and CFS. Current tape prices ($30–100/kA-m) must approach $10/kA-m for commercial viability, requiring one to two orders of magnitude scale-up in production [01-hts-compact-tokamak analysis, §Materials].

> "$50 million in REBCO tape alone for WHAM++"
> — realta-fusion-hub-spotlight.md, §Magnet Specifications

The mirror geometry's axisymmetric solenoid coils are simpler to wind than the 3D saddle coils required for stellarators or the shaped D-coils of a tokamak. This is a genuine manufacturing advantage — lower fabrication cost per unit tape length — but does not reduce the total tape quantity required, only the manufacturing complexity per coil.

**Tritium**

The global tritium inventory is ~25–30 kg, produced primarily as a byproduct of CANDU heavy-water reactors, with market prices above $35,000/g. A Hammir startup inventory requirement has not been published by Realta, but is likely on the order of 1 kg (consistent with tokamak startup estimates). The tritium supply constraint binds the entire D-T fusion fleet, and Realta is no exception. The lithium blanket must achieve TBR > 1 to be self-sufficient, and demonstrated TBR > 1 at fusion-relevant 14 MeV neutron fluences does not exist for any blanket concept. Shared supply chain context is discussed in Section 7.

**Lithium-6 Enrichment**

The tritium-producing nuclear reaction requires Li-6, which is the minority isotope in natural lithium (~7.6%). Enrichment to 90%+ Li-6 is currently dominated by Russian and Chinese suppliers using mercury-based processes banned in the West. Developing Western enrichment capacity is a fleet-level constraint shared with all D-T fusion concepts [01-hts-compact-tokamak analysis, §Materials]. The MARS study used LiPb breeder with natural Li enrichment assumptions — modern TBR analysis typically requires higher Li-6 enrichment.

**Gyrotrons for ECH**

Continuous-wave gyrotron systems at 110 GHz for commercial Hammir heating represent a significant capital and operating cost item. Current commercial gyrotrons cost roughly $1M/MW, and sustained operation (unlike tokamak pulsed heating) means higher total cycle loading. The 40–100 MW input power range implied by the two model estimates means $40–100M in gyrotrons alone. Gyrotron technology is mature but high wall-plug efficiency (>50%) at sustained full power is still an active development area.

**NBI System Components**

Modern NBI systems for tokamak and mirror applications are commercially available from INL, Budker Institute, QST (Japan), and ITER suppliers. NBI capital costs scale with beam power and energy. No Realta-specific NBI cost data has been published. NBI neutralizers and ion sources require periodic replacement, contributing to operating costs.

**First Wall and Structural Materials**

The D-T first wall requires materials resistant to 14 MeV neutron damage at high fluence. Tungsten (for plasma-facing surfaces) and reduced-activation ferritic/martensitic steels (RAFM, such as Eurofer-97 or F82H) are the leading candidates, shared with all D-T fusion concepts. Beryllium, used as a neutron multiplier in some blanket designs, is a critical material with a limited Western supply chain (Materion Corp, ~300 tonnes/year). The choice of blanket type will determine whether beryllium or other multipliers are required.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (target) | >50 MWe | aps-dpp-2025-sutherland.md §Hammir Facility | high | Hammir pilot plant target; commercial plant likely larger |
| Electrical gain Qe | >1 (target) | aps-dpp-2025-sutherland.md §Hammir Facility | medium | Target, not yet demonstrated; commercial plant needs Qe >> 1 |
| Q plasma (50m center cell) | >5 | arxiv-2411-06644-confinement-predictions.md §Hammir Design | medium | Modeled, not demonstrated; Q>10 for longer cells |
| Q plasma (longer center cell) | >10 | arxiv-2411-06644-confinement-predictions.md §Hammir Design | low | Projection; no length specified |
| Center cell fusion power scaling | ~7 MW/m | fusion-report-interview-realta.md §Performance Scaling | medium | Physics claim; cost per meter unquantified |
| Continuous operation duration | 3+ hours (target) | aps-dpp-2025-sutherland.md §Hammir Facility | medium | Milestone demonstration, not commercial steady-state |
| DEC efficiency (historical analogue) | ~54% | [analogue: MARS study, Logan 1983 — MARS achieved ~54% with gridless direct converters] | low | Not Realta-specific; venetian blind geometry differs from gridless |
| Charged particle fraction (D-T physics) | ~20% | [inferred: D-T produces 80% neutron energy, 20% alpha energy by physics] | high | Fixed by D-T nuclear physics; alphas captured by DEC |
| Thermal efficiency (MARS analogue) | ~36% | [analogue: MARS study §Plant Performance — "36% plant efficiency"] | low | MARS used steam Rankine; sCO2 could reach 40-45% |
| Magnet tape cost (WHAM++ signal) | $50M (REBCO only) | realta-fusion-hub-spotlight.md §Magnet Specifications | medium | WHAM++ sub-scale; commercial Hammir tape cost not published |
| LCOE range (parametric models) | 80–135 $/MWh | [analogue: 11-magnetic-mirror-comparison.md §Quantitative Model Comparison — two model variants] | low | Parametric only; 69% spread reflects key parameter disagreements |
| Overnight capital (parametric) | 5,862–9,620 $/kW | [analogue: 11-magnetic-mirror-comparison.md §Summary of Results] | low | Same caveat as LCOE; not a Realta estimate |
| LCOE scaling saturation (historical) | ~600 MWe (1983$) | [analogue: MARS/MINIMARS studies — "LCOE saturates around 600 MWe" per handwritten exemplar §Data Availability] | low | 1983-technology MARS finding; likely different for HTS design |
| Historical LCOE projection | ~7 ¢/kWh (1983$) | [analogue: MARS/MINIMARS — stated in handwritten exemplar §Data Availability] | low | 40-year-old estimate with fundamentally different magnet technology |
| Input heating power (WHAM) | ~1 MW ECH class | [inferred from wham-experiment-details.md §Heating Methods — 110 GHz gyrotron listed] | low | WHAM is sub-commercial; Hammir power undisclosed |
| NBI + ECH input power (arXiv pilot model) | ≈30–40 MW | arxiv-2411-06644-confinement-predictions.md Table 3 | medium | Derived: P_fusion = 175 MW, Q = 5.8 → P_input ≈ 30 MW for 50 m pilot (Optimum case); 35 MW used as midpoint for arXiv-anchored estimate. Present in full output.md but absent from .orig.md summary. |
| Funding secured to date | $9.5M (SVB, Feb 2026) | realta-svb-funding-feb2026.md §Key Details | high | Growth capital only; total funding not published |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Total NBI + ECH input power for Hammir | proprietary | blocking | Determines recirculating power fraction and Qe; hand-written model used 40 MW, automated used 100 MW — 2.5× spread |
| Recirculating power fraction for Hammir | proprietary | blocking | Directly determines whether Qe > 1 is achievable at target fusion power |
| Center cell length for commercial Hammir | not-yet-sourced | blocking | 50m for pilot (Q>5); commercial length for Q>>5 and Pe >> 50 MWe unknown |
| Blanket type and TBR | proprietary | blocking | FLiBe vs. LiPb vs. other drives thermal efficiency, TBR, and blanket cost |
| Thermal cycle type (steam vs. sCO₂) | proprietary | important | Efficiency range 36–45% depending on choice; Realta has not disclosed |
| Hammir fusion power | derivable | blocking | ~7 MW/m × center cell length, but commercial length unknown |
| End-plug input power fraction | truly-unknown | blocking | Fraction of total input power consumed by end-plug heating vs. center-cell heating |
| Capital cost breakdown by subsystem | truly-unknown | important | No Hammir cost estimate exists for any subsystem |
| Capacity factor target | proprietary | important | Realta implies continuous operation but no availability target published |
| DEC electrode lifetime | truly-unknown | important | No fusion-condition DEC survivability data; directly affects plant availability and replacement cost |
| End divertor heat load | truly-unknown | important | Not analyzed in any Realta publication |
| O&M cost drivers | truly-unknown | nice-to-have | Module replacement strategy (hot-cell vs. in-situ), component replacement schedules |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | NBI + ECH input power for commercial Hammir | S2, S5 | proprietary | blocking | Hammir pre-conceptual design paper (Realta, expected 2026) |
| 2 | Recirculating power fraction (determines Qe > 1 viability) | S2, S5 | proprietary | blocking | Same as above |
| 3 | Center cell length for commercial Hammir (post-pilot) | S5 | proprietary | blocking | Realta 2026 design paper; follow-on arXiv scaling study |
| 4 | End-plug confinement validation at Q > 5 conditions | S2, S3 | truly-unknown | blocking | Anvil experiment results (~2028–2030) |
| 5 | Blanket type and TBR for Realta's design | S2, S3, S5 | proprietary | blocking | Hammir design paper (2026); MARS LiPb as interim analogue |
| 6 | Capital cost breakdown for Hammir (magnets, blanket, heating, building) | S5 | truly-unknown | important | No source likely until post-Anvil study; MARS CAS as rough analogue |
| 7 | Thermal cycle selection (steam Rankine vs. sCO₂) | S2, S5 | proprietary | important | Realta communications or 2026 design paper |
| 8 | DEC electrode lifetime in fusion conditions | S3 | truly-unknown | important | No known published data; new experiment required |
| 9 | End divertor heat flux and handling strategy | S3 | truly-unknown | important | Not addressed in any Realta or recent mirror publication |
| 10 | DCLC stabilization effectiveness at commercial density/temperature | S2, S3 | truly-unknown | important | Anvil + Hammir experimental results; ongoing simulation work (arxiv paper) |
| 11 | Center cell module replacement methodology in a radioactive environment | S3 | truly-unknown | important | Not addressed by Realta; hot-cell operations for linear machines a known practical challenge |
| 12 | Capacity factor and planned maintenance intervals | S5 | proprietary | important | Realta design paper; no current source |
| 13 | LCOE scaling behavior vs. plant size (modern HTS equivalent of MARS saturation finding) | S2, S5 | derivable | nice-to-have | Requires costing the center cell per-meter once blanket and magnet specs are known |
| 14 | NBI wall-plug efficiency at commercial beam power | S3, S4 | not-yet-sourced | nice-to-have | NBI vendor specifications for Hammir-class beam power |

---

## Section 7: Cross-Concept Notes

Cross-referencing approved prior analyses: **01-HTS Compact Tokamak (CFS)** and **08-FRC w/ Direct Conversion (Helion)**.

### Shared with 01-HTS Compact Tokamak (CFS)

**REBCO supply chain** is the most directly shared constraint. Both concepts require large quantities of REBCO tape from the same thin global supply chain (CFS, Shanghai Superconductor, Faraday Factory Japan). The Realta-CFS relationship is particularly close: CFS manufactured the WHAM magnets and has a direct supplier relationship with Realta. This creates both a benefit (proven supplier, compatible magnet technology) and a risk (single-supplier concentration, competing demand from SPARC and commercial ARC). The $30–100/kA-m current tape cost and the ~$10/kA-m commercial target are shared assumptions [01-hts-compact-tokamak analysis §Section 2].

**Tritium supply and breeding** represent shared D-T challenges. The global 25–30 kg tritium inventory, the ~$35,000/g market price, the Li-6 enrichment geographic constraint (Russia/China), and the requirement for TBR > 1 are identical across all D-T fusion concepts [01-hts-compact-tokamak analysis §Section 4]. The specific blanket type matters for Realta (unspecified) vs. ARC (FLiBe confirmed), which drives different TBR and thermal efficiency assumptions, but the supply chain and regulatory framework are shared.

**Divergence — geometry and scaling economics**: The tokamak requires a specific minimum plasma volume (major radius × minor radius relationship) to achieve ignition, creating a minimum economic size that tends toward large, expensive plants. The magnetic mirror's linear center cell claims to avoid this constraint — each additional meter adds fusion power at roughly constant end-plug cost — potentially enabling smaller, cheaper plants. Whether this advantage materializes depends on the uncosted center cell cost structure. The ARC-class tokamak targets ~500–800 MWt; Hammir targets 50+ MWe from a pilot. The scaling trajectories are fundamentally different and cannot be directly compared without the missing cost-per-meter data.

**Divergence — disruption risk**: Tokamaks carry disruption risk (sudden loss of plasma current driving large electromagnetic loads on structure). Magnetic mirrors have no plasma current and therefore no disruptions — a structural safety advantage that simplifies vacuum vessel design and potentially reduces maintenance costs. This advantage is not quantified in any available source.

### Shared with 08-FRC w/ Direct Conversion (Helion)

**Direct energy conversion** is the key shared feature. Both concepts exploit DEC to capture kinetic energy of charged particles that would otherwise be deposited as heat. However, the physics and economics diverge sharply: Helion pursues D-He3 fuel because ~40% of D-He3 fusion energy is in charged particles, making DEC highly impactful (potentially 35–40% efficient plant overall vs. a thermal-only alternative). For Realta's D-T fuel, only ~20% of fusion energy is in charged particles, limiting DEC's thermodynamic contribution to ~11% of plant output. The Realta DEC is a worthwhile addition; for Helion it is a design-defining requirement [08-frc-w-direct-conversion analysis §Section 2].

**Linear geometry** is a second shared feature. Both concepts avoid the toroidal geometry of tokamaks and stellarators. Helion's FRC is quasi-toroidal during the compressed burn phase but the machine itself is linear and bilaterally symmetric. Realta's mirror is inherently linear and open-ended. Both benefit from simpler magnet geometry relative to a tokamak, but the similarity ends there: Helion is pulsed with magnetic compression and DEC recovery, while Realta is steady-state with continuous plasma heating and steady thermal output. The maintenance challenges are also different — Helion must maintain capacitor bank reliability over 10⁹ shots; Realta must maintain continuous NBI/ECH operation and manage steady-state neutron activation in a linear machine.

**Divergence — fuel cycle**: Helion's D-He3 strategy eliminates tritium breeding (no Li blanket required) but introduces a He3 supply bootstrapping problem that has no analogue in Realta's approach. Realta's D-T fuel cycle is more technically mature but inherits all the tritium supply constraints. From a TEA perspective, Realta's fuel cycle is more analogous to the tokamak than to Helion.

---

## Section 8: Sources

Listed in order of analytical importance to this analysis.

**1. arXiv:2411.06644 — Confinement predictions for Hammir pilot plant**
- Authors: Realta Fusion team (specific authors not given in extracted source)
- Year: 2024
- What it contributes: The primary quantitative basis for Q > 5 at 50-meter center cell; notes Q > 10 for longer configurations; identifies DCLC and trapped-particle-mode stabilization requirements; discusses machine learning optimization of design parameters
- Phase 1a source: `iter-01/sources/arxiv-2411-06644-confinement-predictions.md`

**2. APS DPP 2025 — Sutherland talk on Hammir pilot plant**
- Authors: Sutherland (Realta Fusion)
- Year: 2025
- What it contributes: The only public source for Hammir quantitative performance targets (Qe > 1, Pe > 50 MWe, 3+ hours continuous); Anvil as dedicated end-plug demonstrator; WHAM experimental status
- Phase 1a source: `iter-01/sources/aps-dpp-2025-sutherland.md`

**3. The Fusion Report — Interview with Realta Fusion**
- Year: ~2025
- What it contributes: The richest available source for system architecture; confirms D-T fuel, lithium-based tritium breeding, dual energy conversion pathway, ~7 MW/m scaling law, constant-input-power scaling thesis, DEC lowers required Q for net electricity
- Phase 1a source: `iter-02/sources/fusion-report-interview-realta.md`

**4. Fusion Hub — Startup Spotlight: Realta Fusion**
- Year: ~2024–2025
- What it contributes: NBI + ECH + HHFW heating confirmation; venetian blind DEC description; REBCO magnets at mirror ratio 10+; $50M REBCO tape cost for WHAM++; DCLC and Alfvén instability modes requiring stabilization; industrial heat as primary near-term application
- Phase 1a source: `iter-01/sources/realta-fusion-hub-spotlight.md`

**5. WHAM Experiment Details (wham.physics.wisc.edu)**
- Year: 2024
- What it contributes: WHAM operational parameters (17 T in-bore, >20 T on conductor, CFS-built magnets); first plasma July 15, 2024; ECH/NBI/HHFW heating system details; target plasma parameters (1 keV electron temperature, 20 keV average ion energy); BEAT conceptual follow-on target ($100M device)
- Phase 1a source: `iter-01/sources/wham-experiment-details.md`

**6. Realta SVB Funding Feb 2026 (PR Newswire)**
- Year: February 2026
- What it contributes: $9.5M SVB growth capital facility; confirms CoSMo modular concept; identifies target markets (industrial heat, data centers, chemical processing, metal recycling, remote mining, heavy industry); physics derisking as stated near-term purpose
- Phase 1a source: `iter-02/sources/realta-svb-funding-feb2026.md`

**7. MARS Study (Logan et al., 1983)**
- Logan, B.G. et al., "The Mirror Advanced Reactor Study (MARS)," Lawrence Livermore National Laboratory, 1983
- What it contributes: The most detailed magnetic mirror plant study available; LiPb blanket with TBR 1.15; ~36% plant efficiency; gridless direct converters at ~54% efficiency; LCOE ~7 ¢/kWh (1983$); LCOE saturation ~600 MWe; cost structure analogue for center cell, building, and blanket
- Location: OSTI/Semantic Scholar (not ingested as Phase 1a source; used as historical analogue via handwritten exemplar)

**8. MINIMARS Conceptual Design (Lee, 1985)**
- Lee, J.D., "MINIMARS conceptual design," UCID-20559, Lawrence Livermore National Laboratory, 1985
- What it contributes: Complementary to MARS; confirms LCOE saturation result and provides alternative design point; relevant to understanding historical mirror economic performance
- Location: LLNL OSTI (not ingested as Phase 1a source; referenced via handwritten exemplar)

**9. Phase 1a Dossier — Magnetic Mirror (D-T)**
- Iteration 2, overall confidence: medium-high
- What it contributes: Synthesized column values with citations; identifies remaining gaps (blanket type, plasma state ambiguity at Q > 10); provides key source inventory
- Path: `exploration/phase_1a/research/11-magnetic-mirror/dossier.md`

**10. Handwritten Exemplar and Comparison Report (Concept 11)**
- What they contribute: Expert physics intuition on end-plug taxonomy (tandem, centrifugal, ponderomotive, non-axisymmetric); LCOE saturation insight; back-solve floor analysis (2.70 ¢/kWh best case); quantitative model parameter comparison; DEC survivability judgment; hot-cell operations as practical concern
- Paths: `handwritten/11-magnetic-mirror.md`, `handwritten/11-magnetic-mirror-comparison.md`

**11. Endrizzi et al. — Physics Basis for WHAM (Journal of Plasma Physics, 2023)**
- Endrizzi, D., Anderson, J.K., Brown, M., et al., *Journal of Plasma Physics* 89(5), 2023
- What it contributes: Foundational peer-reviewed physics basis for WHAM experiment; confinement physics validation
- Location: Cambridge University Press (not ingested as Phase 1a source; referenced via handwritten exemplar)

**12. Moir & Barr — Venetian Blind Direct Energy Converter (Nuclear Fusion, 1973)**
- Moir, R.W. and Barr, W.L., *Nuclear Fusion* 13(1):35–45, 1973
- What it contributes: Original DEC design reference; 50–65% efficiency range; TRL 5 basis
- Location: IOP Publishing (not ingested; referenced via handwritten exemplar)
