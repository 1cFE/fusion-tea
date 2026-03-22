---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Status: approved
Created: 2026-03-22
Approved-Date: 2026-03-22
Reuses: [01-hts-compact-tokamak, 07-maglif, 08-frc-w-direct-conversion, 21-spherical-tokamak-hts]
Review-Iterations: 1
Last-Review: 2026-03-22
Review-Status: addressed
---

# D1+ Analysis: Magnetic Mirror (D-T) — Realta Fusion

**Concept**: Axisymmetric tandem magnetic mirror — D-T fuel, hybrid thermal + direct energy conversion
**Company**: Realta Fusion (Madison, WI; UW-Madison spin-out, founded 2022)
**Pilot Plant**: Hammir (axisymmetric tandem mirror pilot; targeting Qe > 1, >50 MWe, ≥3 hours continuous)
**Confinement Family**: MFE — Magnetic mirror
**Operation Mode**: Steady-state

---

## Section 1: Availability of Data

**Rating: Limited**

Realta Fusion is at an early stage — WHAM (Wisconsin HTS Axisymmetric Mirror) achieved first plasma in July 2024, and the Hammir pre-conceptual design paper has not yet been published as of this writing (expected 2026). The company is moderately transparent about its roadmap and qualitative approach, but plant-level engineering data, capital cost estimates, and quantitative energy balance parameters are entirely absent from the public record.

**Peer-reviewed and technical literature:**

The primary technical reference is a 2024 arXiv paper from the Realta/UW-Madison team that reformulates the POPCON technique for a tandem mirror central cell and uses machine learning to optimize the design, concluding that HTS end-plugs with modern neutral beams yield a classical tandem mirror pilot plant with Q > 5 at 50-meter center cell length:

> "End plug: HTS magnets + modern neutral beams → classical tandem mirror pilot plant with Q > 5"
> — arxiv-2411-06644-confinement-predictions.md, §Key Technical Details

This paper is the primary quantitative physics basis for Hammir but presents simulations — no Hammir hardware exists. The broader tandem mirror literature is substantial (MFTF-B, TMX, MARS study from the 1980s DOE program) but reflects copper-magnet designs and lower mirror ratios; the HTS-enabled mirror ratio of 10+ is qualitatively different from those historical experiments. No independent techno-economic analysis equivalent to the Araiinejad & Shirvan (2025) tokamak study exists for this concept. [1]

**Experimental heritage:**
WHAM is the only currently operating Realta-relevant experiment. It uses two REBCO HTS magnets from Commonwealth Fusion Systems, achieved 17 T in-bore (>20 T on-conductor), and validated the high-field simple mirror configuration with ECH, NBI, and HHFW heating. First plasma was July 15, 2024. WHAM targets a $100M "Break Even Axisymmetric Tandem" (BEAT) conceptual design as its end-product goal — it is not itself a gain-producing device. [2]

**Company transparency:**
The APS DPP 2025 talk (Sutherland) provided the clearest public summary of the development roadmap and Hammir performance targets. The Fusion Hub spotlight and Fusion Report interview filled out the technical picture on heating, energy conversion, and performance scaling. The February 2026 SVB funding announcement ($9.5M facility) confirms continued development but adds no new technical parameters. [3]

No published items: capital cost estimates, detailed blanket design, tritium breeding TBR target, DEC efficiency characterization for Realta's venetian-blind design, NBI/ECH power requirements for Hammir, or any LCOE estimate.

**Key data gaps limiting this analysis:**
- Hammir pre-conceptual design paper not yet published (expected 2026) — would provide the first plant-level engineering parameters
- Tritium blanket type (FLiBe, LiPb, liquid Li, solid ceramic) undisclosed
- Thermal power conversion cycle (steam, sCO2) undisclosed
- NBI and ECH power requirements for Hammir → recirculating power and Qe relationship unknown
- DEC efficiency for Realta's venetian-blind design uncharacterized (only MARS historical ~54% available)
- No capital cost estimates at any stage (WHAM cost ~$10M ARPA-E, but no Anvil or Hammir cost data)

---
[1] arxiv-2411-06644-confinement-predictions.md §Key Technical Details; dossier.md §Key Sources — historical mirror context.
[2] wham-experiment-details.md §Key Technical Details, §Funding & Partners, §End Product Goal.
[3] aps-dpp-2025-sutherland.md §Hammir Facility; realta-svb-funding-feb2026.md §Key Details.

---

## Section 2: Challenges in Capturing System Function

Realta's LCOE structure is anchored on a novel combination of four technical bets: (1) HTS-enabled high mirror ratios resolving end-loss, (2) linear center-cell scaling at ~7 MW/m, (3) hybrid energy capture (thermal blanket + direct energy conversion), and (4) inherent steady-state operation. Each bet introduces LCOE modeling challenges ranked below by impact.

### 1. End-Plug Tandem Mirror Confinement Is Undemonstrated — No Physics Anchor for Hammir (Impact: Critical)

The entire Hammir performance projection depends on end-plug confinement physics that has not been experimentally validated with HTS magnets. WHAM is a simple mirror — it does not have the end-plug cells that create the electrostatic potential to plug the loss cone. Anvil is specifically designed to demonstrate end-plug sustainment at commercial scale:

> "Primary objective: demonstrate stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant"
> — aps-dpp-2025-sutherland.md, §Anvil Device (Next Step)

The Q > 5 projection in the arxiv paper is a simulation result, not an experimental extrapolation from measured confinement. The tandem mirror concept has historical precedents (MFTF-B, TMX at Livermore; GAMMA-10 in Japan), but those operated at much lower mirror ratios (~2) and with copper magnets. The HTS-enabled mirror ratio of 10+ is the key claim, but it has only been tested in the simple mirror WHAM geometry — not in the tandem configuration with end plugs. This gap is comparable to Helion's D-He3 extrapolation or a tokamak claiming Q = 10 before achieving burning plasma: the physics basis exists in simulation, but the experiment is one or two device generations away. [1]

### 2. Direct Energy Conversion: Efficiency and Capital Cost Are Undefined for Realta's Design (Impact: High)

Realta's hybrid energy capture is central to its claimed economic advantage — DEC lowers the Q threshold for net electricity:

> "Dual approach 'lowers the Q required to reach net-electric while still using DT fuel'"
> — fusion-report-interview-realta.md, §Energy Conversion

The only published DEC efficiency number for an axisymmetric tandem mirror is from the 1983 MARS study: ~54% for gridless direct converters. Realta's venetian-blind DEC design uses axisymmetric "ferromagnetic venetian blinds" to convert escaping ion beams to electrical current. This design has not been built or tested at any scale. No efficiency target, capital cost estimate, or operational lifetime for the venetian-blind system has been published. The DEC system interacts with the charged particle exhaust stream (helium ash, unburned D-T ions) in a way that creates a combined exhaust management and energy recovery challenge unique to the linear mirror geometry — there is no analogue in closed-geometry fusion concepts. [2]

The fraction of fusion power captured by DEC vs. the thermal blanket is also uncharacterized. In D-T fusion, 80% of energy is in 14.1 MeV neutrons (captured in the blanket) and 20% in 3.5 MeV alpha particles. Alphas escape through the ends and are available for DEC. The DEC efficiency of ~54% thus applies to ~20% of fusion energy — a meaningful but not dominant contribution. The exact energy split (including bremsstrahlung losses, neutron wall loading on end structures, and end-plug heating power) is not published. [3]

### 3. Linear Center-Cell Scaling: The Key Cost Lever, With Unknown Cost Floor (Impact: High)

Realta's most compelling economic argument is that commercial-scale fusion power is achieved by adding center-cell length, with approximately constant input power:

> "~7 MW per meter as center cell lengthens. Input power remains constant despite increased output."
> — fusion-report-interview-realta.md, §Performance Scaling

This creates a favorable scaling relationship: capital cost per meter of center-cell is dominated by relatively weak, inexpensive solenoid magnets, while end-plug hardware costs remain fixed. A 50-meter center cell achieves Q > 5; longer cells approach Q > 10-20. For an LCOE model, this is the primary performance lever — but the marginal cost per meter of center cell is not characterized. The central solenoid magnets are weaker than end-plug magnets (and therefore cheaper per unit field), but the structure, vacuum vessel, blanket, and neutron shielding add cost per meter. Without a pre-conceptual design, the cost-per-meter breakdown cannot be estimated from available sources. [4]

### 4. Plasma Stability at Full Scale: DCLC and MHD Uncertainties (Impact: Moderate)

The historical demise of mirror machines was driven partly by microinstabilities — particularly the Drift Cyclotron Loss Cone (DCLC) instability that enhanced particle losses and thermal conductivity beyond classical predictions. Realta addresses this with "sloshing ions" and kinetic stabilization, and relies on vortex flow stabilization for MHD modes. The arxiv paper identifies DCLC stabilization as a requirement and notes that machine learning was used to optimize parameters accounting for it. But the DCLC mitigation has not been demonstrated in a tandem mirror configuration with HTS end-plug fields — this is partly what Anvil is designed to demonstrate:

> "Requires stabilization against MHD and trapped particle modes"
> — arxiv-2411-06644-confinement-predictions.md, §Key Technical Details

For LCOE modeling, instability at full scale would manifest as either reduced confinement time (lower effective Q) or increased heating power requirements (higher recirculating power fraction). The range of impact is large — historically, instability was the dominant failure mode of mirror machines. If Realta's stabilization approach works, it could be a non-issue; if it doesn't, it is concept-ending. The uncertainty spans from "works as modeled" to "Q is 2× lower than projected," representing large LCOE uncertainty. [5]

### 5. Regulatory and Licensing Context for Linear Geometry (Impact: Moderate)

Steady-state D-T magnetic confinement is the most studied category for fusion licensing (ITER, SPARC, etc.), but the linear open-field geometry creates distinct regulatory questions. End-plug plasma exhaust exits through open ends of the device — unlike a closed toroidal geometry, the neutral gas and ion exhaust must be managed in expanding "expander" regions that are part of the system boundary. Tritium handling in the exhaust stream adds regulatory complexity. Realta has not disclosed any regulatory pathway analysis, and no prior regulatory precedent exists for a commercial tandem mirror facility. The NRC's 2023 decision to regulate fusion under 10 CFR Part 30 is favorable in principle, but the detailed rulemaking applicable to a mirror machine with open-ended plasma exhaust is undefined. [6]

---
[1] aps-dpp-2025-sutherland.md §Anvil Device; arxiv-2411-06644-confinement-predictions.md §Key Technical Details.
[2] fusion-report-interview-realta.md §Energy Conversion; realta-fusion-hub-spotlight.md §Energy Conversion.
[3] realta-fusion-hub-spotlight.md §Fuel & Reaction: "80% of output energy in neutrons."
[4] fusion-report-interview-realta.md §Performance Scaling.
[5] arxiv-2411-06644-confinement-predictions.md §Key Technical Details.
[6] dossier.md §Remaining Gaps; general regulatory context from 01-hts-compact-tokamak handwritten analysis.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**Tritium Breeding Blanket (Li type unspecified) — TRL 2–3**

- **Demonstrated**: Lab-scale tritium breeding experiments shared with all D-T concepts. The MARS study (1983) modeled a Li17Pb83 (LiPb) blanket for a tandem mirror with TBR = 1.15, and the linear central-cell geometry was found favorable for a surrounding cylindrical blanket design. JET and TFTR have handled gram-scale tritium. ITER TBM program includes Li-containing concepts for toroidal geometry.
- **On paper only**: Any blanket design specific to Realta's linear geometry — the Hammir pre-conceptual design paper has not been published. The specific blanket type (FLiBe, LiPb, liquid Li, solid ceramic) has not been disclosed. A cylindrical blanket surrounding the center cell is the obvious configuration, and the MARS geometry is a valid historical precedent, but none of this has been engineered for HTS mirror conditions.
- **Missing at scale**: 14 MeV neutron irradiation testing at fusion-relevant fluences for the linear geometry. Tritium extraction system at kg/day rates from whatever blanket type is chosen. Full TBR validation accounting for the open ends, end-plug structure, and diagnostic penetrations, which reduce effective breeding coverage from the ideal cylindrical geometry. Compatibility of blanket choice with the DEC exhaust expander at the open ends of the device. [1]

---

**Direct Energy Conversion (Venetian Blinds) — TRL 2–3**

- **Demonstrated**: Gridless direct conversion was analyzed in the 1983 MARS study at ~54% efficiency for axisymmetric tandem mirror escaping ions. The physics basis (electrostatic deceleration of escaping ions) is understood. Helion Energy pursues a different form of DEC (inductive energy recovery from compressed FRCs), and TAE Technologies has developed DEC for aneutronic fuel cycles — neither is directly analogous to Realta's venetian-blind design for escaping end-loss ions. [2]
- **On paper only**: Realta's "axisymmetric ferromagnetic venetian blinds" design. Efficiency characterization of the venetian-blind collector geometry for D-T alpha particles and unburned deuterium/tritium escaping through the end-plug expander. Integration of DEC with the neutral beam exhaust and helium ash management systems.
- **Missing at scale**: Any prototype of Realta's venetian-blind DEC design. Lifetime and materials characterization of the collector surfaces under ion bombardment from the escaping plasma stream. Integration with high-voltage electrical generation and grid synchronization at power-plant scale. Performance under continuous operation with high-energy 3.5 MeV alphas and ~100 keV D-T beam ions. [3]

---

**Tandem Mirror Confinement with HTS End Plugs — TRL 3–4**

- **Demonstrated**: WHAM has demonstrated stable simple mirror confinement with REBCO HTS magnets at 17 T, including ECH and NBI heating, with first plasma in July 2024. The simple mirror geometry is validated at these fields. Historical tandem mirror physics was extensively studied at Livermore (MFTF-B, TMX, TMX-U) and Japan (GAMMA-10), but at much lower mirror ratios (~2) and without HTS.
- **On paper only**: Tandem mirror confinement with HTS end-plug fields at 17+ T and mirror ratios of 10+. The electrostatic plugging potential required to suppress end losses in Hammir. Machine learning–optimized design parameters for the Hammir plasma scenario at Q > 5. [4]
- **Missing at scale**: Anvil — the device specifically designed to demonstrate stable sustainment of end-plug plasma conditions at commercial scale — has not yet been built. The transition from Anvil (single end plug demonstrator) to Hammir (tandem configuration) is itself a major integration step. DCLC and trapped-particle mode stabilization at the Hammir plasma parameters have not been demonstrated experimentally. Classical radial transport (identified in the arxiv paper as significant) may not be the only transport channel at full scale. [5]

---

**Plasma Stability (DCLC and MHD) — TRL 4**

- **Demonstrated**: Sloshing ions for DCLC stabilization were studied extensively in historical mirror experiments (the Baseball II/C2 program at Livermore, GAMMA-10). The vortex stabilization mechanism for MHD was developed theoretically and tested in simple mirrors. WHAM has demonstrated stable plasmas with ECH and NBI, validating basic plasma sustainment.
- **On paper only**: Machine learning–optimized sloshing ion injection parameters specifically tuned for Hammir end-plug conditions. Full MHD stability in the Hammir tandem configuration with non-Maxwellian end-plug velocity distributions. Stability margins over the operational parameter range needed for commercial power production.
- **Missing at scale**: Experimental validation of DCLC stabilization in the HTS tandem mirror configuration with mirror ratio 10+. Characterization of anomalous transport that may persist even with DCLC suppression. Stability tracking over hours-long continuous operation with slowly evolving plasma parameters. [6]

---

**HTS Mirror Magnets (REBCO, Axisymmetric) — TRL 6–7**

- **Demonstrated**: WHAM is operating with two CFS-built REBCO HTS magnets at 17 T in-bore (>20 T on-conductor), currently the world record for magnetically confined plasmas. Axisymmetric solenoid geometry is simpler to wind and structurally more uniform than tokamak TF coils or stellarator coils. The WHAM magnets have demonstrated the HTS mirror coil concept in the relevant geometry.
- **On paper only**: Full Hammir magnet set — a series of end-plug magnets (17+ T) and central-cell solenoid coils (weaker field, cost-optimized). Quench protection for an integrated array of HTS mirror coils in a neutron-producing plasma. Radiation damage management for the HTS coil set over a multi-year plant lifetime.
- **Missing at scale**: Reliable km-scale REBCO tape supply chain with consistent Jc (the same bottleneck as for tokamaks — see Section 4). Magnet performance under neutron and gamma irradiation for the end-plug coil positions closest to the plasma. Cost optimization of the center-cell solenoid array, which is less demanding field-wise but must cover the full 50+ meter length. [7]

---

**NBI + ECH + HHFW Heating — TRL 6–8**

- **Demonstrated**: All three heating technologies are operational on WHAM: 110 GHz gyrotron (ECH), NBI for ion fueling, HHFW for in-situ ion acceleration. MW-class NBI and ECH systems are routinely operated on major fusion devices worldwide (JET, DIII-D, EAST, ITER under construction). WHAM proved the specific combination in a mirror geometry.
- **On paper only**: Hammir-scale NBI power for end-plug sustainment (specific power requirements not published). Integration of NBI beam trajectory with the tandem mirror geometry for efficient end-plug density maintenance without excessive gas injection.
- **Missing at scale**: CW high-power NBI systems at the rep-rates and beam energies required for Hammir. Long-term NBI source lifetime under high-flux operation. ECH gyrotron efficiency improvements toward 50–60% wall-plug efficiency (current generation: ~45–55%) to reduce recirculating power. [8]

---

**Balance of Plant / Thermal Conversion — TRL 7–9 (BOP) / TRL 2–4 (Integrated System)**

- **Demonstrated**: Conventional Rankine and sCO₂ power cycles are commercially mature. The thermal side of the tandem mirror (cylindrical blanket, heat exchangers) follows conventional D-T blanket engineering. No inherent pulsing requirement (unlike pulsed concepts), so no thermal buffer is needed — the steady-state heat source is compatible with standard thermal cycles.
- **On paper only**: Integration of the thermal cycle with the specific Realta blanket (type unspecified). Heat exchanger design compatible with tritium-bearing primary coolant. Thermal cycle efficiency target and selection (steam vs. sCO₂) — Realta has not disclosed this.
- **Missing at scale**: First-wall and blanket module replacement tooling for the linear geometry — the open-ended device enables more direct maintenance access than toroidal concepts (a potential advantage), but specific remote-handling tooling is undeveloped. [9]

---
[1] dossier.md §Tritium Breeding; fusion-report-interview-realta.md §Energy Conversion; dossier.md §Key Sources (MARS study).
[2] realta-fusion-hub-spotlight.md §Energy Conversion.
[3] realta-fusion-hub-spotlight.md §Energy Conversion; fusion-report-interview-realta.md §Energy Conversion.
[4] wham-experiment-details.md §Key Technical Details; aps-dpp-2025-sutherland.md §Anvil Device.
[5] aps-dpp-2025-sutherland.md §Anvil Device; arxiv-2411-06644-confinement-predictions.md §Key Technical Details.
[6] arxiv-2411-06644-confinement-predictions.md §Key Technical Details; realta-fusion-hub-spotlight.md §Stabilization.
[7] wham-experiment-details.md §Magnet System.
[8] wham-experiment-details.md §Heating Methods; realta-fusion-hub-spotlight.md §Heating Methods.
[9] fusion-report-interview-realta.md §Energy Conversion.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO HTS Tape**

The Fusion Hub spotlight includes a striking data point: "$50 million in REBCO tape alone for WHAM++" — Realta's proposed scientific breakeven device, an intermediate step between WHAM and Anvil:

> "$50 million in REBCO tape alone for WHAM++"
> — realta-fusion-hub-spotlight.md, §Magnet Specifications

This is the only published cost proxy in the Realta source set. WHAM++ is a pre-commercial, scientific-scale device. If the tape cost alone is $50M for that machine, the REBCO requirement for Hammir — which must have high-field end-plug magnets (17+ T) at commercial scale plus the center-cell solenoid array — could represent hundreds of millions of dollars. The same global supply constraints apply here as for tokamak-class devices: current global REBCO production is thousands of kilometers per year, while even a single ARC-class reactor requires >5,000 km of tape (01-hts-compact-tokamak handwritten analysis §Key Materials). Realta's axisymmetric solenoid geometry is mechanically simpler to wind than 3D tokamak TF coils, which may reduce waste and winding complexity — but the fundamental REBCO quantity required is governed by the stored magnetic energy, which scales with the mirror field strength and plasma volume.

The center-cell solenoid magnets operate at lower field than end-plug magnets (~1–5 T vs. 17+ T) and can potentially use less REBCO per unit length — but the total center-cell length is 50+ meters, and the accumulated tape requirement may dominate the weaker-field sections. No Hammir-specific tape quantity has been published. [1]

**Tritium**

Standard D-T startup constraint. The global tritium inventory is approximately 25–30 kg, primarily from CANDU heavy-water reactor operation, decaying at 5.5% per year. Startup inventory for a D-T fusion plant is typically ~1 kg. At current market rates (~$35,000/g cited in 01-hts-compact-tokamak handwritten analysis §Key Materials), the startup tritium cost is ~$35M per plant — not the binding capital constraint, but a real sequencing issue as CANDU reactors age. The Hammir pilot plant must demonstrate tritium self-sufficiency (TBR > 1) before commercial scale-up is feasible. The blanket type for Realta (unspecified Li variety) will determine the specific Li-6 enrichment requirement and tritium extraction process — these are standard D-T supply chain issues shared with all D-T concepts. [2]

**Lithium (Li-6 Enrichment)**

The blanket will require lithium enriched in Li-6 for effective tritium breeding. Natural lithium is 7.4% Li-6; blanket designs typically target 30–90% enrichment depending on design and TBR requirements. Li-6 enrichment is a mature but geographically concentrated industrial process — Russia and China currently dominate production, and the mercury-based isotope separation process used historically is banned in most jurisdictions. A Western enrichment restart would require capital investment. The specific Li-6 requirement for Realta depends on the unspecified blanket type and TBR target. This is a shared supply chain item with all D-T concepts, flagged identically in the tokamak analyses. [3]

**NBI Components and Gyrotrons**

NBI systems and ECH gyrotrons are established industrial products, but high-power CW versions at Hammir scale remain at the upper end of the commercial envelope. The ITER NBI program provides the most relevant precedent for large-scale NBI procurement. For Hammir, the NBI requirements are unusual: beams must be injected into the end-plug regions at specific angles to create the sloshing ion distribution for DCLC stabilization, requiring custom geometry. The 110 GHz gyrotrons used on WHAM are commercially available but the multi-megawatt CW versions needed for Hammir are at the frontier of current industrial capability. These are not blocking supply chain constraints but add cost and lead time to any plant procurement plan. [4]

**No Pulsed Power or Laser Components**

Unlike MagLIF (which requires capacitor banks at $5/J current prices, with a requirement to reach $0.50/J for viability) or laser IFE (which requires multi-kJ laser systems), the magnetic mirror has no high-energy pulsed driver requirement. The capital cost structure is dominated by HTS magnets, heating systems, and blanket — not pulsed power. This is a supply chain advantage relative to IFE and MIF concepts, though the REBCO requirement remains challenging. [5]

---
[1] realta-fusion-hub-spotlight.md §Magnet Specifications; 01-hts-compact-tokamak handwritten §Key Materials (REBCO supply chain characterization reused).
[2] 01-hts-compact-tokamak handwritten §Key Materials (tritium supply chain characterization); fusion-report-interview-realta.md §Energy Conversion (breeding confirmed).
[3] 01-hts-compact-tokamak handwritten §Key Materials (Li-6 enrichment context).
[4] wham-experiment-details.md §Heating Methods; dossier.md §Driver Technology.
[5] 07-maglif handwritten §Key Materials (capacitor cost baseline for contrast).

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electric output (Hammir pilot) | >50 MWe | aps-dpp-2025-sutherland.md §Hammir Facility | high | Pilot plant target; commercial scale not disclosed |
| Electric gain (Hammir) | Qe > 1 | aps-dpp-2025-sutherland.md §Hammir Facility | high | Minimum pilot plant target |
| Plasma Q (50m center cell) | >5 | arxiv-2411-06644-confinement-predictions.md §Hammir Design | high | Simulation result, not yet experimentally validated |
| Plasma Q (longer cell variants) | >10 | arxiv-2411-06644-confinement-predictions.md §Hammir Design; fusion-report-interview-realta.md §Performance Scaling | medium | Qualitative projection from center cell length scaling |
| Theoretical output (Q=20 variant) | 500 MW (interpreted as thermal fusion power; source does not specify unit) | fusion-report-interview-realta.md §Performance Scaling | low | Theoretical bound only; design not specified |
| Center-cell thermal power scaling | ~7 MWt/m | fusion-report-interview-realta.md §Performance Scaling | medium | "Input power remains constant despite increased output"; scaling relation, not verified experimentally |
| Continuous operation target | ≥3 hours | aps-dpp-2025-sutherland.md §Hammir Facility | high | National Academies pilot plant standard; not a physical limit on operation duration |
| Operation mode | Steady-state | dossier.md §Operation Mode; schema definition | high | Inherent to mirror geometry; no inductive pulse, no disruptions |
| D-T neutron energy fraction | 80% | realta-fusion-hub-spotlight.md §Fuel & Reaction | high | Physics constant for D-T: 14.1 MeV neutron vs. 3.5 MeV alpha |
| Historical DEC efficiency (MARS) | ~54% | dossier.md §Key Sources (MARS study, Logan 1983) | low | Gridless direct converters, copper-magnet design; Realta's venetian-blind DEC uncharacterized |
| REBCO tape cost proxy (WHAM++) | ~$50M (tape only) | realta-fusion-hub-spotlight.md §Magnet Specifications | medium | Unusual data point; applies to intermediate pre-commercial device, not Hammir |
| WHAM ARPA-E grant | $10M | wham-experiment-details.md §Funding & Partners | high | Early validation experiment only; not a plant cost proxy |
| Anvil funding context | $9.5M SVB facility (Feb 2026) | realta-svb-funding-feb2026.md §Key Details | high | Growth capital; purpose: derisking physics toward commercial delivery |
| Magnet field strength (WHAM, operational) | 17 T in-bore; >20 T on-conductor | wham-experiment-details.md §Magnet System | high | CFS-built REBCO magnets; world record for magnetically confined plasmas |
| Mirror ratio (HTS-enabled) | 10+ | realta-fusion-hub-spotlight.md §Magnet Specifications | high | Versus historical maximum of ~2 with copper magnets |
| Historical plant efficiency (MARS) | ~36% overall | dossier.md §Key Sources (MARS study, OSTI 5981974) | low | 1983 copper-magnet design; not directly applicable to Realta's HTS approach |
| Historical TBR (MARS) | 1.15 | dossier.md §Key Sources (MARS study) | low | LiPb blanket; illustrative of achievable TBR in linear geometry |
| Hammir center cell length (design point) | 50 m | arxiv-2411-06644-confinement-predictions.md §Hammir Design | high | Minimum Q > 5 design point |
| Tritium breeding source | Li blanket | fusion-report-interview-realta.md §Energy Conversion | medium | Specific type (FLiBe, LiPb, liquid Li) undisclosed |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Total plant capital cost (Hammir or commercial) | proprietary | blocking | No cost estimate published at any level |
| LCOE estimate or target | truly-unknown | blocking | No company or independent estimate exists |
| Thermal efficiency / power conversion cycle | proprietary | blocking | Thermal cycle type (steam, sCO₂) undisclosed; needed for LCOE closure |
| NBI + ECH auxiliary power for Hammir | proprietary | blocking | Determines recirculating power fraction and Qe from plasma Q |
| Capacity factor target | truly-unknown | important | No maintenance schedule or availability model published |
| DEC efficiency (Realta venetian-blind design) | truly-unknown | important | Only MARS historical data (~54%) available; Realta's design uncharacterized |
| Blanket TBR target and design | proprietary | important | Li breeding confirmed but type, TBR target, and engineering undisclosed |
| First-wall heat flux and replacement schedule | truly-unknown | important | Linear geometry creates different wall loading profile; no published data |
| Commercial plant net electric target | truly-unknown | blocking | Only pilot (>50 MWe) disclosed; commercial scale undefined |
| Hammir capital cost | proprietary | blocking | Expected in 2026 pre-conceptual design paper |
| Hammir REBCO tape quantity | derivable | important | [derivable: end-plug magnets ≈ WHAM++ scale (>$50M tape); center-cell solenoids at lower field — total likely $100–500M range by analogy; extreme uncertainty without published coil specifications] |
| DEC capital cost | truly-unknown | important | No precedent for venetian-blind DEC at this scale |
| Center-cell solenoid magnet cost per meter | truly-unknown | important | Key parameter for scaling economics; weaker field than end plugs but covers 50+ m |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Hammir pre-conceptual design paper: capital cost, detailed plant parameters | S1, S5 | not-yet-sourced | blocking | Realta 2026 paper (expected); monitor arXiv and APS DPP 2026 |
| 2 | Thermal efficiency and power conversion cycle type (steam vs. sCO₂) | S2, S5 | proprietary | blocking | Realta disclosure or MARS-analogous assumption with stated basis |
| 3 | NBI + ECH auxiliary power for Hammir (→ recirculating power, Qe characterization) | S2, S5 | proprietary | blocking | Realta technical disclosure; arxiv paper may include in future revision |
| 4 | Total plant capital cost at any level | S5 | proprietary | blocking | 2026 pre-conceptual design; no near-term public source expected |
| 5 | DEC efficiency for Realta venetian-blind design | S2, S3, S5 | truly-unknown | important | Anvil will generate relevant data; no published estimate |
| 6 | Tritium blanket type and TBR target | S3, S4, S5 | proprietary | important | 2026 pre-conceptual design paper; MARS LiPb (TBR=1.15) as analogue with caveat |
| 7 | End-plug confinement physics validation (Anvil results) | S2, S3 | truly-unknown | blocking | Anvil experimental results (~2028) |
| 8 | Center-cell solenoid cost per meter | S2, S5 | truly-unknown | important | No published data; derivable from REBCO requirements once coil specs known |
| 9 | Capacity factor target and maintenance philosophy | S5 | truly-unknown | important | Open geometry may simplify maintenance; no published model |
| 10 | DCLC stabilization validation at Hammir plasma parameters | S2, S3 | truly-unknown | important | Anvil or dedicated experiments; critical for Q projection validity |
| 11 | Commercial plant size and net electric target | S5 | truly-unknown | blocking | Only Hammir pilot (>50 MWe) published; CoSMo modularity implies multiple units |
| 12 | First-wall materials and replacement schedule in linear geometry | S3, S5 | truly-unknown | important | No published data; linear geometry simplifies access but wall loading differs |

---

## Section 7: Cross-Concept Notes

Four approved prior analyses were consulted: 01-hts-compact-tokamak (handwritten), 07-maglif (handwritten), 08-frc-w-direct-conversion, and 21-spherical-tokamak-hts.

**Shared with 01-hts-compact-tokamak and 21-spherical-tokamak-hts — REBCO supply chain:**
The characterization of the global REBCO supply chain (thousands of km/year current capacity, $30–100/kA-m current price, requirement to scale by 1–2 orders of magnitude for commercial fusion) from the tokamak analyses applies directly here. The axisymmetric mirror solenoid geometry is mechanically simpler to wind than TF coils, which may reduce winding waste and manufacturing complexity — but the tape quantity requirement is governed by stored energy and current density, not geometry complexity. The end-plug magnets (17+ T) make equivalent demands on REBCO performance to SPARC-class TF coils.

**Shared with 01-hts-compact-tokamak — Tritium supply chain:**
The tritium constraints (global ~25–30 kg inventory, $35,000/g market rate, CANDU-produced, 5.5% per year decay, ~1 kg startup requirement) are identical to those for all D-T concepts. The breeding blanket TRL discussion in the tokamak analysis (integrated blanket TRL 3–4) is directly analogous for the lithium blanket layer — the main difference is geometry (cylindrical linear vs. toroidal), which simplifies the blanket in some respects (more uniform neutron flux distribution along the center cell) and complicates it in others (open ends reduce total solid angle for breeding).

**Shared with 08-frc-w-direct-conversion — Direct energy conversion:**
Both Helion (inductive FRC compression) and Realta (venetian blinds for escaping ions) pursue direct energy conversion as a core economic differentiator. The challenges diverge significantly in mechanism: Helion recovers magnetic energy from collapsing plasma inductance at ~1 Hz, while Realta's DEC operates continuously on a directed ion beam. The Helion analysis notes that the >95% round-trip efficiency claim was demonstrated at subscale with modern IGBTs; Realta's venetian-blind DEC has no analogous demonstration. The common thread is that DEC at plant scale — any mechanism — is TRL 2–3 and represents a significant capital and engineering uncertainty. The FRC analysis caution that DEC is "unvalidated at plant scale" applies here with even more force: no Realta DEC prototype exists, while Helion at least has subscale round-trip efficiency demonstrations.

**Diverges from all tokamak analyses — linear geometry advantages:**
The magnetic mirror's open linear geometry creates a set of advantages absent from closed-geometry tokamaks: (a) no disruptions (no toroidal current, no runaway electron risk, no disruption-induced loads on vessel); (b) direct physical access for maintenance along the center cell without remote-handling robotics for every maintenance action; (c) modular scaling by adding center-cell length rather than redesigning the whole machine; (d) no need for a current-drive system to sustain plasma current (the mirror is current-free). These advantages are real but none of them translate directly into a published cost advantage — they are potential cost saving opportunities whose magnitude is unknown without a plant study.

**Diverges from all tokamak analyses — end-loss is the dominant physics challenge:**
All tokamak and stellarator analyses in this project deal with closed-flux-surface confinement, where the physics challenge is managing heat and particle exhaust through the divertor. The mirror's challenge is fundamentally different: particles escape along field lines through the open ends. The tandem mirror configuration with HTS end plugs addresses this, but it has not been demonstrated in the tandem configuration. There is no tokamak analogue for the Anvil/Hammir step of validating end-plug confinement — this is a concept-specific physics risk with no parallel in the tokamak development path.

---

## Section 8: Sources

1. **arxiv-2411-06644-confinement-predictions.md** — Realta Fusion / UW-Madison team (2024), "Confinement performance predictions for a high field axisymmetric tandem mirror," arXiv:2411.06644. Primary quantitative physics basis: Q > 5 at 50m center cell, POPCON technique, ML optimization, DCLC stabilization requirement. Phase 1a source: `iter-01/sources/arxiv-2411-06644-confinement-predictions.md`.

2. **aps-dpp-2025-sutherland.md** — Derek A. Sutherland (Realta Fusion), APS DPP 2025, Session: DOE Milestone Awardee Physics Basis I, November 18, 2025. Primary source for development roadmap: WHAM → Anvil → Hammir; Hammir targets (Qe > 1, >50 MWe, ≥3 hours). Phase 1a source: `iter-01/sources/aps-dpp-2025-sutherland.md`.

3. **realta-fusion-hub-spotlight.md** — Fusion Hub, "Startup Spotlight: Realta Fusion," undated (retrieved 2026). Key technical overview: DT fuel, NBI + ECH, REBCO HTS magnets, venetian-blind DEC, plasma stabilization, device timeline. Notable: "$50M in REBCO tape alone for WHAM++." Phase 1a source: `iter-01/sources/realta-fusion-hub-spotlight.md`.

4. **fusion-report-interview-realta.md** — The Fusion Report, "Interview with Realta Fusion," August 2025. Key details: tritium breeding from lithium confirmed, DEC for charged particles, ~7 MW/m center-cell scaling, Q > 10 possible with longer cell, theoretical 500 MW at Q=20. Phase 1a source: `iter-02/sources/fusion-report-interview-realta.md`.

5. **wham-experiment-details.md** — WHAM project website (wham.physics.wisc.edu; wippl.wisc.edu). REBCO HTS magnets (17 T, CFS-built), ECH + NBI + HHFW heating, first plasma July 15, 2024, $10M ARPA-E grant, BEAT conceptual design goal. Phase 1a source: `iter-01/sources/wham-experiment-details.md`.

6. **realta-svb-funding-feb2026.md** — PR Newswire, February 17, 2026. $9.5M SVB growth capital facility; CoSMo branding; target markets (industrial heat, data centers, chemical processing, heavy industry). No new technical parameters. Phase 1a source: `iter-02/sources/realta-svb-funding-feb2026.md`.

7. **MARS Study** (Logan et al., 1983) — "The Mirror Advanced Reactor Study (MARS)," LLNL / DOE, OSTI 5981974 and Semantic Scholar. Historical tandem mirror power plant study: LiPb blanket (TBR = 1.15), gridless direct converters (~54% efficiency), ~36% plant efficiency, 1200 MWe design. Not directly in Phase 1a source documents but cited in dossier.md §Key Sources as a historical reference. Applies as a lower-bound analogue only — copper magnets, lower mirror ratio, 1983-era engineering.

8. **01-hts-compact-tokamak handwritten analysis** — Fusion TEA project, handwritten exemplar for HTS compact tokamak. Tritium supply chain characterization ($35,000/g, 25–30 kg global inventory) and REBCO supply chain characterization ($30–100/kA-m, thousands km/yr production) reused for Section 4 with adaptation to mirror geometry context.
