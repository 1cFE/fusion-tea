---
ID: 31-laser-icf-oec-architecture
Concept: Laser ICF OEC Architecture (BLF)
Company: Blue Laser Fusion
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: IFE
Archetype: LASER_IFE
Archetype-Fit: Low
Comparison-Status: costingfe
Comparables:
  - 17b-laser-icf-fast-ignition
  - 26-laser-icf-indirect-drive
  - 30-laser-icf-nif-commercialization
  - 32-laser-icf-french-national
  - 17a-laser-icf-hybrid-drive
Design-Point-Name: BLF OEC Reactor, 10 Hz design point (Sunahara et al., 2025)
Design-Point-Maturity: paper-concept
P-Native: 1000
Grounding-Confidence: medium
---

## Design Point

- Name: BLF OEC Reactor, 10 Hz design point (Sunahara et al., 2025)
- Maturity: paper-concept
- P_native: 2820 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/optics-express-2025-paper.md
  - knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/blf-website-and-news.md

## 1. Availability of Data

**Rating: Limited**

The BLF OEC Reactor concept rests on a single peer-reviewed publication — Sunahara et al., "Laser-based inertial fusion energy system enabled by optical enhancement cavities and a direct-drive configuration reactor," *Optics Express* 33(22), 47104–47120 (2025).[^1] This paper provides the complete reactor power balance, OEC prototype results, and a schematic reactor layout, but contains **no cost estimates of any kind** — no capital cost breakdown, no LCOE projection, no subsystem cost figures, and no target fabrication cost targets.

The company website (bluelaserfusion.com) adds qualitative confirmation of the technology approach but no additional quantitative data beyond what the paper provides; the website extraction captured only cookie-consent boilerplate.[^2] News coverage and press releases confirm:
- $37.5M Series Seed funding (March 2024) from SoftBank, Itochu, JAFCO Group, SPARX Group, and others.[^3]
- DOE INFUSE award (2025) for advanced OEC optical coatings collaboration with Colorado State University.[^4]
- Japan Moonshot Program Goal 10 selection (2025) with University of Osaka.[^5]

No independent cost analysis or techno-economic study of the BLF concept exists. No GEM-class (LLNL) or PROCESS-class (UKAEA) system code run has been published for this design. The iter-02 sources contain useful background on IFE tritium breeding blankets (Fuerst et al., INL; Meier, LLNL) and helium Brayton power conversion (Wright et al., Sandia), but none are BLF-specific.

**Key data gaps:**
- Zero dollar figures for any subsystem (laser, blanket, target factory, buildings, BOP)
- No target fabrication cost target or manufacturing concept
- No first-wall lifetime estimate or replacement interval
- No blanket TBR calculation
- No detailed DEC system design
- No O&M cost breakdown (fixed vs. variable, scheduled maintenance, unplanned outage)

[^1]: optics-express-2025-paper.md — peer-reviewed paper with full reactor parameters
[^2]: blf-website-and-news.md — extraction failed; cookie-consent only
[^3]: finance-news-blue-laser-fusion-completes-37-114500457/output.md §Body
[^4]: semiconductor-today-news-items-2025-oct-blue-laser-fusion/output.md §Body
[^5]: semiconductor-today-news-items-2025-oct-bluelaserfusion/output.md §Body

## 2. Challenges in Capturing System Function

The BLF OEC Reactor presents several modeling challenges, ranked by LCOE impact:

### 2.1 No Published Cost Data for the OEC Laser System (Critical)

The OEC/CBC fiber laser architecture is the concept's defining innovation and its primary capital cost driver. BLF claims this architecture will "substantially reduce the cost of the system" relative to DPSSL-based approaches like LIFE and HiPER,[^6] but provides no quantitative basis for this claim. The paper contains no $/J figure for the laser driver, no cost estimate for the 500 OEC modules, and no fiber laser unit cost. Without a laser driver cost, the dominant capital cost account (C220104) cannot be grounded.

> "Unlike HiPER and LIFE, which relied on DPSSL-driven glass amplifiers, our approach employs CBC of fiber lasers injected into OEC. This architecture is expected to substantially reduce the cost of the system."
> — optics-express-2025-paper.md §4.1

### 2.2 Target Gain Assumption Is Unvalidated (Critical)

The entire power balance depends on a target gain of G = 160 at 5 MJ laser energy. This value is extrapolated from Froula et al. gain curves for CBET-mitigated direct drive, and BLF explicitly claims performance "beyond the CBET-mitigated curve."[^7] No shock ignition experiment at any facility has achieved this gain. The gain assumption directly scales fusion power, net electric output, and recirculating power fraction — a 2× error in gain produces roughly a 2× error in net power.

> "We anticipate a higher target gain G beyond the CBET-mitigated curve of Froula (ii) and achieving a target gain of G = 160 at EL = 5 MJ."
> — optics-express-2025-paper.md §4.2

### 2.3 No Target Factory Cost or Concept (High)

At 10 Hz, the reactor requires ~315 million cryogenic D-T targets per year. The paper acknowledges target fabrication is a "major issue" but provides no cost target, no manufacturing concept, and no throughput estimate.[^8] This is a shared challenge across all laser ICF concepts, but the cost of the target factory (C220108) is one of the largest unknowns.

### 2.4 DEC System at 0.44 Efficiency Is Assumed, Not Designed (High)

The power balance assumes 30% of fusion energy is captured by direct energy conversion at η_DEC = 0.44. The paper describes this as "conservative" and cites theoretical work (Rax et al., 2025) on adiabatic DEC, but no DEC hardware design exists for this reactor.[^9] The DEC channel contributes ~13% of gross electric output at 10 Hz.

**DEC-off scenario (model limitation):** The LASER_IFE archetype models 100% thermal conversion (`pulsed_conversion=thermal`) and has no hybrid thermal+DEC mode. For this specific design point, η_th = η_DEC = 0.44, so the net η_e = 0.44 regardless of the thermal/DEC split — the model's structural mismatch is numerically invisible at native scale. However, this coincidental equality masks a real risk: if DEC is unavailable (TRL ~2), the 30% charged-particle fraction must either be dumped or recovered thermally at lower efficiency. In the DEC-off case, assuming the 30% charged-particle energy is recovered thermally at η_th = 0.44, the net η_e remains 0.44; but if that energy is simply lost (no recovery path designed), η_e drops to 0.7 × 0.44 = 0.308, P_gross falls from ~3,520 MWe to ~2,464 MWe, and the recirculating fraction rises from 0.170 to 600/2,464 = 0.244. Net output would fall from 2,820 MWe to ~1,864 MWe — a 34% reduction. This DEC-off scenario should be carried as a sensitivity in the model.

### 2.5 Very Large Native Plant Size Creates Scaling Uncertainty (Moderate)

At 2820 MWe native, the BLF design is ~3× larger than a typical 1 GWe fusion plant comparison point. The 1costingFE library scales this to 1 GWe for comparison, but the native design's economics at 2.8 GWe may differ — buildings, site infrastructure, and cooling systems scale sublinearly, while the laser driver cost may scale nearly linearly with beam count. The paper presents a parametric range (1–10 Hz), not a single optimized design point; the 10 Hz point represents the upper end of performance claims.

[^6]: optics-express-2025-paper.md §4.1
[^7]: optics-express-2025-paper.md §4.2
[^8]: optics-express-2025-paper.md §4.1: "Although these are still major issues, development will continue with the aim of demonstrating power generation in early 2030"
[^9]: optics-express-2025-paper.md §4.2: "actual efficiency eta_DEC depends heavily on the design, we conservatively assume eta_DEC = 0.44"

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity:

### Direct Energy Conversion (DEC) — TRL ~2

- **On paper only**: The paper assumes η_DEC = 0.44 based on theoretical adiabatic DEC in axisymmetric fields (Rax et al., 2025). No DEC hardware for IFE exists.
- **Missing at scale**: Complete DEC electrode design, magnetic guiding system for charged particles to exhaust ports, materials qualification under IFE charged-particle flux, and integration with the reactor chamber.

### Cryogenic Target Fabrication at Rate — TRL ~2–3

- **On paper only**: The paper requires cryogenic D-T targets with sub-micrometer surface roughness, uniform cryo-layering, and precise injection at 10 Hz. No manufacturing concept is described.
- **Missing at scale**: Batch cryogenic cooling pipeline producing a target every 100 ms, in-line quality control at production rate, target survival during injection into a post-shot chamber environment.

### First Wall and Blanket — TRL ~3

- **On paper only**: Layered tungsten/RAFM steel first wall with helium gas cooling; LiPb blanket with Pb neutron multiplier and SiC-based ceramics. The paper describes investigating HTGR technology integration.[^10]
- **Missing at scale**: No blanket TBR calculation, no first-wall lifetime estimate under IFE cyclic loading, no activation analysis, no replacement interval. The paper acknowledges: "Survivability and radioactivation modeling of the first wall and chamber components will inform replacement intervals and long-term operational planning."[^10]

### OEC at Reactor Scale (150 m) — TRL ~3

- **Demonstrated**: 1.5 m prototype OEC achieved finesse 419,000 and enhancement factor 59,000 in CW mode (2024).[^11] 15 m systems under construction at Goleta and Osaka (2025).
- **On paper only**: Scaling to 150 m cavity length with pulsed operation, high thermal loads, and UV frequency conversion. Active alignment and stabilization under reactor conditions.
- **Missing at scale**: Pulsed-mode OEC operation at any scale, 150 m cavity alignment stability, thermal management under 10 Hz cycling, radiation-resistant mirror coatings.

### Coherent Beam Combining (CBC) of Fiber Lasers — TRL ~4

- **Demonstrated**: CBC of fiber lasers is commercially mature at kW CW power levels for industrial/defense applications. BLF's innovation is applying CBC to pulsed, high-energy operation injected into OECs.
- **On paper only**: 500-beam CBC system with the required phase coherence, bandwidth, and temporal profile for shock ignition.
- **Missing at scale**: Integrated CBC + OEC system producing 10 kJ UV pulses per module at 10 Hz.

### Shock Ignition Physics — TRL ~4

- **Demonstrated**: Shock ignition experiments on OMEGA have demonstrated strong shock generation and energy coupling. PIC simulations show LPI mitigation via polarization rotation and broadband irradiation.[^12]
- **On paper only**: Gain of 160 at 5 MJ via multicolor direct-drive shock ignition with broadband CBET suppression. BLF cites upcoming FLUX experiments at OMEGA for quantitative LPI validation.
- **Missing at scale**: Any shock ignition experiment at MJ scale; validation of the BLF-specific multicolor/broadband approach.

### Balance of Plant (Thermal Power Conversion) — TRL ~7–8

- **Demonstrated**: Helium gas-cooled Brayton or Rankine cycles are mature power conversion technology at GW scale (fission heritage). SiC-based ceramics for high-temperature applications are under active development.
- **Missing at scale**: Integration with IFE pulsed thermal source; thermal buffering for 10 Hz cyclic loading; tritium-compatible heat exchangers.

[^10]: optics-express-2025-paper.md §4.1
[^11]: optics-express-2025-paper.md §2.2
[^12]: optics-express-2025-paper.md §3

## 4. Key Materials and Supply Chain Considerations

### Fiber Lasers and Telecom-Grade Optical Components

BLF's core supply-chain argument is that fiber lasers are "mass-produced" commodity components from the telecom and industrial laser industries.[^13] This is broadly accurate for CW fiber lasers at kW power levels, but the specific fiber amplifiers needed for BLF's pulsed CBC architecture (high peak power, precise temporal profile, narrow linewidth for coherent combining) are specialty items, not off-the-shelf telecom components. The 500-module reactor requires ~500 fiber amplifier chains, each with associated pump diodes, phase modulators, and electronics. This is a substantial but feasible manufacturing scale, comparable to a medium-sized telecom deployment.

### High-Reflectivity OEC Mirrors

The OEC requires mirrors with reflectivity ≥99.9995% (total optical losses <10 ppm). BLF demonstrated this with 2-inch commercial mirrors (Thorlabs mounts).[^14] Scaling to 150 m cavities requires larger aperture mirrors with the same coating quality, plus radiation-resistant coatings that survive the reactor neutron and X-ray environment. The DOE INFUSE award with Colorado State University specifically targets this challenge.[^4] LIGO-heritage mirror coating technology provides a strong foundation, but the IFE radiation environment is far harsher than gravitational-wave detector conditions.

### KDP/DKDP Frequency Conversion Crystals

Each of the 500 beams requires nonlinear crystals (KDP or DKDP) for third-harmonic generation to 350 nm UV. KDP/DKDP crystal growth is a mature but specialized industry (NIF heritage). At 500 beams, crystal demand is comparable to NIF's ~200 frequency converters, roughly a 2.5× scale-up of an existing supply chain. Crystal damage under high-fluence UV and 10 Hz rep rate is a known concern; NIF crystals are qualified for single-shot operation, not continuous cycling.

### Tungsten First-Wall Facing Material

Tungsten is available in adequate supply globally. Fabricating large tungsten armor tiles qualified for IFE cyclic thermal and neutron loading is an active research area shared with all D-T fusion concepts. No IFE-specific tungsten qualification exists.

### Lithium-Lead (LiPb) Blanket Material

The LiPb blanket uses natural lithium (7.5% Li-6) and lead as neutron multiplier. Both are commodity materials with no supply-chain constraints at reactor scale. LiPb handling infrastructure (pumps, heat exchangers, purification) is being developed for EU-DEMO (WCLL and DCLL concepts) and benefits from shared MFE development.

### Tritium

Standard D-T concern: global civilian inventory ~25–30 kg, decaying at 5.5%/year. A 2.2 GWth IFE reactor requires ~0.37 kg/day.[^15] BLF's IFE architecture has a tritium inventory advantage — only a few mg per target in the chamber at any time, vs. the multi-kg plasma inventory in a tokamak — but the breeding blanket must still achieve TBR > 1.05 for self-sufficiency, and no TBR calculation is published for this design.

### SiC-Based Ceramics

The blanket design investigates SiC-based ceramic structural materials and integration with HTGR technology. SiC/SiC composites are under development for fission and fusion applications but are not yet qualified for fusion neutron environments. Manufacturing at the scale needed for a 2.8 GWe blanket is well beyond current production capability.

[^13]: optics-express-2025-paper.md §1, §2.1: "our approach coherently combines mass-produced fiber lasers"
[^14]: optics-express-2025-paper.md §2.2
[^15]: lasers-sites-lasers-files-2023-11-fuerst-idaho-ife-workshop/output.md §Body

## 5. Design Point Parameters

All parameters describe the BLF OEC Reactor at 10 Hz, the native design point at P_native = 2820 MWe.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Laser energy on target (E_L) | 5 MJ (UV, 350 nm) | optics-express-2025-paper.md §Table 2 | high | spec key: `E_driver` |
| Number of beams | 500 (360 compression + 140 ignition) | optics-express-2025-paper.md §4.1 | high | |
| Energy per OEC module | ~10 kJ | optics-express-2025-paper.md §2.3 | medium | at 150 m cavity, 100 kW injection |
| Target gain (G) | 160 | optics-express-2025-paper.md §Table 2, §4.2 | low | extrapolated from Froula et al. CBET-mitigated gain curves; BLF claims "beyond" this curve; not experimentally validated |
| Repetition rate (f) | 10 Hz | optics-express-2025-paper.md §Table 2 | high | design range 1–10 Hz; 10 Hz is upper bound |
| Fusion power (P_fus) | 8000 MW | optics-express-2025-paper.md §4.2 (= E_L × G × f) | low | directly dependent on unvalidated G=160 |
| net_electric_MWe | 2820 MWe | optics-express-2025-paper.md §Table 2 | medium | drives P_native |
| Wall-plug-to-IR efficiency (η_w) | 0.16 | optics-express-2025-paper.md §Table 1, §Table 2 | medium | fiber laser + CBC efficiency |
| Frequency conversion efficiency (η_3ω) | 0.60 | optics-express-2025-paper.md §Table 2 | medium | 1.06 μm → 0.35 μm via THG in KDP/DKDP |
| Wall-plug-to-UV efficiency (η_w*) | 0.10 | optics-express-2025-paper.md §Table 2 (= 0.16 × 0.6) | medium | spec key: `eta_driver` |
| Thermal conversion efficiency (η_th) | 0.44 | optics-express-2025-paper.md §Table 2 | medium | includes 10% exothermic 6Li breeding boost over base 0.40 |
| DEC efficiency (η_DEC) | 0.44 | optics-express-2025-paper.md §Table 2 | low | "conservative" assumption; theoretical basis only (Rax et al., 2025) |
| Total fusion-to-electric efficiency (η_e) | 0.44 | optics-express-2025-paper.md §Table 2 (= 0.7 × 0.44 + 0.3 × 0.44) | medium | coincidental equality of thermal and DEC efficiencies |
| Neutron energy fraction | 0.70 | optics-express-2025-paper.md §4.1 | high | standard D-T |
| Charged particle / plasma exhaust fraction | 0.30 | optics-express-2025-paper.md §4.1 | high | alpha + plasma exhaust directed to DEC |
| Blanket energy multiplication (M_n) | 1.10 | optics-express-2025-paper.md §4.2 | medium | exothermic 6Li(n,α)T reaction |
| Recirculating power fraction (f_re) | 0.170 | optics-express-2025-paper.md §Table 2 | medium | at 10 Hz; rises to 0.426 at 1 Hz |
| Laser operating power (P_Lop) | 500 MW | optics-express-2025-paper.md §Table 2 (= E_L × f / η_w*) | medium | |
| Facility operating power (P_op, non-laser) | 100 MW | optics-express-2025-paper.md §Table 2 | low | stated as fixed; no breakdown provided |
| p_input_MW | 600 MW | [inferred: P_Lop + P_op = 500 + 100] | medium | spec key: `p_input`; total wallplug recirculation |
| Chamber radius | 8–10 m | optics-express-2025-paper.md §4.1 | medium | |
| First wall material | W facing + RAFM steel structure | optics-express-2025-paper.md §4.1 | high | He gas cooled |
| Blanket type | LiPb (natural Li + Pb multiplier), He-gas-cooled | optics-express-2025-paper.md §4.1 | high | SiC-based ceramics investigated |
| Laser wavelength on target | 0.35 μm (UV) | optics-express-2025-paper.md §Table 2 | high | frequency-tripled from 1.06 μm |
| Relative bandwidth (Δω/ω₀) | ~1.9% | optics-express-2025-paper.md §Table 2 | high | broadband for LPI suppression |
| Target type | Cryogenic D-T, direct-drive shock ignition | optics-express-2025-paper.md §4.1 | high | |
| OEC enhancement factor (demonstrated) | 59,000 (CW, 1.5 m) | optics-express-2025-paper.md §2.2 | high | |
| OEC mirror reflectivity | ≥99.9995% | optics-express-2025-paper.md §2.2 | high | demonstrated |
| Target mass | No data found in available sources | — | — | |
| Burnup fraction | No data found in available sources | — | — | |

**Derivation chain for p_input**: The paper states P_Lop = E_L × f / η_w* = 5 MJ × 10 / 0.10 = 500 MW for the laser system, plus P_op = 100 MW for non-laser facility power. Total wallplug recirculating power = 600 MW. This is confirmed by the recirculating power fraction: f_re = (P_Lop + P_op) / P_gross = 600 / (P_fus × η_e + P_Lop + P_op... The paper's own accounting gives f_re = 0.170 at 10 Hz with P_grid = 2820 MWe, implying P_gross = P_grid / (1 − f_re) = 2820 / 0.83 ≈ 3398 MW, and recirculating = 3398 − 2820 = 578 MW. The slight discrepancy (~600 vs. 578 MW) likely reflects rounding or the blanket multiplication factor feeding into the thermal channel. We use the paper's stated P_grid and f_re as authoritative.

## 5b. Override Candidates

The per-account walkthrough below applies the canonical 1costingFE schema for this archetype against the BLF dossier.

**C220101 (First wall, blanket & neutron multiplier):** The paper describes a LiPb blanket with natural lithium, Pb neutron multiplier, SiC-based ceramics, and He gas cooling.[^10] However, no cost figure, material quantity, or unit cost is published. No company-grounded data to override the library default. No override proposed.

**C220102 (Radiation shield):** No shielding specifications or activation analysis beyond the blanket description. No override proposed.

**C220104 (Primary pulsed driver — laser):** The OEC/CBC fiber laser system is the concept's defining subsystem and represents a fundamentally different architecture than the DPSSL drivers the library default likely assumes for IFE. BLF provides zero dollar figures for the OEC/CBC system. However, the IFE comparable literature provides a bracketing range: Xcimer's published KrF excimer cost is $100–$120/J FOAK / $60–$80/J NOAK (Xcimer white paper, 2024),[^17] while the DPSSL class estimate is $700–$1,000/J (ibid.). The BLF laser delivers E_L = 5 MJ UV on target. Using the geometric mean of the NOAK range ($70/J) and the DPSSL midpoint ($850/J) gives a bracket of $350M–$4,250M for the laser driver alone. A central estimate of ~$400/J × 5 MJ = $2,000M is proposed as the override value, positioned between the commodity-fiber-laser aspiration (closer to excimer) and the DPSSL heritage (closer to glass amplifiers). This is a derived override with high uncertainty — the OEC/CBC architecture is structurally different from both KrF and DPSSL, so the bracket is indicative, not predictive. **Override proposed (derived).**

**C220105 (Primary structure):** No data. No override proposed.

**C220106 (Vacuum system):** No data. No override proposed.

**C220107 (Pulsed-power capacitor bank):** Not applicable — BLF uses an optical driver (laser), not an electrical pulsed-power driver. The laser cost is in C220104. No override proposed.

**C220108 (Target factory):** The paper acknowledges target fabrication as a "major issue" but provides no BLF-specific cost target, manufacturing concept, or throughput estimate. However, Goodin et al. (2004, GA-A24429) published an nth-of-a-kind direct-drive target factory cost for a 1 GWe IFE plant: $100M installed capital, $31M/yr operating (labor $9M, materials/utilities $4M, maintenance $6M), producing 500,000 targets/day at <$0.17 each (2004$).[^18] BLF at 10 Hz requires ~864,000 targets/day (~315M/yr), roughly 1.7× the GA baseline. CPI-adjusting the $100M capex from 2004 to 2024 (factor ~1.59) gives ~$159M; scaling by 1.7× for throughput (assuming sublinear scaling at ~0.6 exponent, factor 1.7^0.6 ≈ 1.38) gives ~$219M. This is a derived, analogue-based override with substantial uncertainty — BLF targets may differ from the GA reference design, and no BLF-specific manufacturing concept exists. **Override proposed (derived).**

**C220110 (Remote handling):** The paper mentions "Remote handling and robotic inspection systems are incorporated for component replacement"[^10] but provides no cost data. No override proposed.

**C220111 (Installation & assembly):** No data. No override proposed.

**CAS21 (Buildings & site):** No data. No override proposed.

**CAS23 (Turbine plant):** The design uses a hybrid thermal + DEC energy conversion. The thermal channel (70% of fusion energy) uses conventional turbine equipment. The DEC channel (30%) has no hardware cost data. No override proposed.

**CAS24 (Electric plant equipment):** No data. No override proposed.

**CAS26 (Heat rejection):** No data. No override proposed.

**CAS27 (Special materials — initial inventory):** The LiPb blanket requires an initial lithium-lead inventory, but no quantity is specified and no blanket volume is given. No override proposed.

**CAS70 (O&M + scheduled replacement):** No O&M breakdown is provided. No first-wall or blanket replacement interval is stated. No override proposed.

**CAS80 (Fuel cost):** Standard D-T fuel. No override proposed.

```yaml
overrides:
  - account: C220104
    value: 2000.0
    enabled: true
    provenance: derived
    source: "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule; optics-express-2025-paper.md §Table 2"
    rationale: |
      BLF publishes no laser driver cost. Bracketed from IFE comparable literature:
      Xcimer KrF excimer at $60–$80/J NOAK / $100–$120/J FOAK (Xcimer white paper);
      DPSSL class estimate at $700–$1,000/J (ibid.). BLF E_L = 5 MJ UV on target.
      OEC/CBC fiber laser architecture is structurally between excimer (commodity gas
      laser) and DPSSL (specialty glass amplifiers). Central estimate: ~$400/J × 5 MJ
      = $2,000M. This is a geometric-mean positioning — fiber lasers share the
      commodity-component argument with excimer but lack excimer's published cost
      basis. High uncertainty: true cost could range from $350M ($70/J, excimer-like)
      to $4,250M ($850/J, DPSSL-like). Sensitivity sweeps over this range are
      essential.
  - account: C220108
    value: 219.0
    enabled: true
    provenance: derived
    source: "osti-servlets-purl-828518/output.md §IV.A. Direct Drive Target Cost Analysis Results"
    rationale: |
      BLF publishes no target factory cost. Derived from Goodin et al. (2004,
      GA-A24429) nth-of-a-kind DD target factory for 1 GWe IFE plant: $100M
      installed capital (2004$), 500K targets/day. BLF at 10 Hz needs ~864K
      targets/day. CPI 2004→2024 factor ~1.59 → $159M; throughput scale-up
      1.7× at 0.6 exponent → 1.7^0.6 ≈ 1.38 → $159M × 1.38 ≈ $219M.
      Excludes tritium plant (separate account). High uncertainty: BLF cryogenic
      D-T targets may differ from GA reference design; no BLF-specific
      manufacturing concept exists.
  # Remaining 14 accounts reviewed — no company-grounded data found:
  # C220101 (blanket): LiPb described but no cost/quantity data.
  # C220102 (shield): No data.
  # C220105 (primary structure): No data.
  # C220106 (vacuum system): No data.
  # C220107 (pulsed-power): N/A — optical driver, not electrical.
  # C220110 (remote handling): Mentioned but no cost data.
  # C220111 (installation): No data.
  # CAS21 (buildings): No data.
  # CAS23 (turbine plant): Conventional thermal; no override basis.
  # CAS24 (electric plant): No data.
  # CAS26 (heat rejection): No data.
  # CAS27 (special materials): No blanket volume or inventory quantity.
  # CAS70 (O&M): No breakdown provided.
  # CAS80 (fuel): Standard D-T; no override basis.
  #
  # Override count: 2 enabled.
  # Expected band (Low archetype-fit): 6–12.
  # DISCREPANCY: Count (2) falls below the expected band.
  # Reason: The primary source (Optics Express 2025) publishes no cost data.
  # The two overrides are derived entirely from cross-concept analogue data
  # (Xcimer KrF $/J bracket for C220104; Goodin et al. 2004 DD target factory
  # for C220108). No other account has sufficient analogue evidence to justify
  # a derived override — the remaining 14 accounts have no published IFE-specific
  # cost data in the dossier or comparable literature that would narrow them
  # beyond the library default. The shortfall reflects genuinely thin economic
  # data for this paper-concept, not analytical omission.
```

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No laser driver cost ($/J or total $) for OEC/CBC system | S2, S5b | derivable | blocking | BLF company disclosure needed for direct data; currently bracketed at $70–$850/J from Xcimer KrF NOAK ($60–$80/J) and DPSSL class ($700–$1,000/J) via C220104 override. Override carries high uncertainty. |
| 2 | Target gain G=160 at 5 MJ unvalidated | S2, S5 | truly-unknown | blocking | FLUX experiments at OMEGA (BLF cites as forthcoming); independent target physics review |
| 3 | No target factory cost or manufacturing concept | S2, S5b | derivable | blocking | BLF company disclosure needed; currently bracketed from Goodin et al. 2004 (GA-A24429) DD target factory at $100M/500K targets/day via C220108 override ($219M CPI- and throughput-scaled). Override carries high uncertainty — no BLF-specific manufacturing concept exists. |
| 4 | No DEC hardware design or cost | S2, S3, S5b | truly-unknown | blocking | Literature on IFE DEC: Rax et al. 2025 (theoretical only); check MFE DEC heritage (mirrors, GAMMA-10) |
| 5 | No blanket TBR calculation | S3, S4 | not-yet-sourced | important | Standard LiPb + Pb multiplier TBR studies; LLNL Meier (2014) TBB assessment for methodology |
| 6 | No first-wall lifetime or replacement interval | S3 | truly-unknown | important | IFE first-wall survivability studies; BLF paper acknowledges this analysis is pending |
| 7 | No O&M cost breakdown | S5b | truly-unknown | important | Analogue from LIFE/HYLIFE-II plant studies; GEM model O&M module |
| 8 | No building/site cost data | S5b | truly-unknown | important | IFE plant study analogues (HYLIFE-II, SOMBRERO, LIFE); chamber radius 8–10 m provides sizing basis |
| 9 | OEC pulsed-mode operation not demonstrated | S3 | truly-unknown | important | BLF 15 m system (under construction) will be first pulsed-mode test |
| 10 | No KDP/DKDP crystal lifetime under 10 Hz cycling | S4 | not-yet-sourced | nice-to-have | NIF optics damage literature; LLNL FOAK optics replacement rates |
| 11 | Target mass and burnup fraction not stated | S5 | not-yet-sourced | nice-to-have | Direct-drive shock ignition target physics literature |
| 12 | Non-laser facility power (100 MW) not decomposed | S5 | proprietary | nice-to-have | Plant auxiliary power breakdown from any IFE plant study |

## 7. Family-Delta vs Comparables

### vs. 17b — Laser ICF Fast Ignition (Focused Energy)

**Shared**: Both use direct-drive laser illumination of cryogenic D-T targets at ~10 Hz, with DPSSL-class laser energies in the MJ range.

**Deltas**:
- **Driver architecture** (cost direction: unknown, potentially large advantage): BLF replaces the entire DPSSL amplifier chain with fiber laser CBC + OEC pulse stacking. This eliminates large doped glass slabs, flash lamps, and the thermal management systems that dominate DPSSL cost. Fiber lasers have demonstrated manufacturing learning curves from telecom/industrial markets. However, no cost comparison exists — the advantage is structural (commodity components vs. specialty optics) but unquantified.
- **Ignition physics** (cost direction: neutral to unknown): BLF uses shock ignition (single-wavelength, two-stage temporal pulse) rather than fast ignition (separate petawatt ignition laser). Shock ignition avoids the cost and complexity of a separate PW laser system and the cone-in-shell target geometry, but requires higher main laser energy (5 MJ vs. ~1–2 MJ for fast ignition) to compensate. The net cost effect depends on laser $/J at each scale.
- **Beam count** (cost direction: penalty): BLF requires 500 beams vs. ~100–200 for fast ignition concepts, increasing the number of OEC modules, frequency converters, and beam transport components. However, each OEC module is smaller (~10 kJ) than a DPSSL beamline (~50–100 kJ).

### vs. 26 — Laser ICF Indirect Drive (Inertia Enterprises / Thunderwall)

**Shared**: Both target ~10 Hz D-T operation with MJ-class laser drivers and thermal power conversion. Both claim low-cost driver architectures relative to NIF heritage.

**Deltas**:
- **Drive scheme** (cost direction: advantage): BLF uses direct drive (laser → target surface directly), while Inertia uses indirect drive (laser → hohlraum → X-rays → capsule). Direct drive eliminates the hohlraum from the per-shot target cost and improves coupling efficiency (~50–80% for direct drive vs. ~12% for indirect via hohlraum). This means BLF needs less laser energy for the same energy on capsule, or achieves higher gain at the same laser energy.
- **Laser architecture** (cost direction: unknown): Inertia uses ~1000 modular Thunderwall DPSSL beamlines at ~$700–1000/J.[^16] BLF's OEC/CBC architecture has no published cost. If BLF achieves <$100/J (which would be comparable to Xcimer's excimer target of $60–80/J NOAK), the driver cost advantage could be substantial. If it is >$500/J, the advantage evaporates.
- **Target complexity** (cost direction: advantage): BLF's direct-drive target is a simple cryogenic D-T sphere, while Inertia's indirect-drive target includes a hohlraum enclosure, raising per-target cost.

### vs. 30 — Laser ICF NIF Commercialization (LIFE-class)

**Shared**: D-T fuel, cryogenic targets, thermal power conversion via blanket.

**Deltas**:
- **Driver architecture** (cost direction: likely advantage): LIFE used NIF-heritage DPSSL technology — large glass amplifiers, flash-lamp or diode-pumped, single-shot or low-rep-rate. BLF's OEC/CBC replaces this with fiber lasers + optical cavities, which are structurally lower-cost per watt at high rep rate (no large glass slabs, no thermal management crisis). LIFE was estimated at $5–10B+ total plant cost; BLF claims to achieve comparable or higher gain with a fundamentally different driver.
- **Drive scheme** (cost direction: advantage): LIFE used indirect drive with hohlraum targets. BLF uses direct drive, eliminating hohlraum cost and improving coupling efficiency (same delta as vs. concept 26).
- **Plant scale** (cost direction: neutral): Both target GW-class output, but BLF's native 2.8 GWe is unusually large.

### vs. 32 — Laser ICF French National (GenF)

**Shared**: European/international laser ICF program, D-T fuel.

**Deltas**:
- **Driver architecture** (cost direction: unknown): GenF uses a national-lab-heritage DPSSL approach (LMJ/Petal lineage). BLF's OEC/CBC is a wholly different technology base. The cost comparison depends entirely on the BLF $/J figure that does not exist.
- **Program maturity** (neutral): Both are paper-concept reactor designs without experimental facilities. GenF benefits from LMJ operational experience but LMJ is a single-shot facility, not a power plant driver.

### vs. 17a — Laser ICF Hybrid Drive (Xcimer Energy)

**Shared**: Laser-driven IFE with D-T fuel, targeting commercial power generation.

**Deltas**:
- **Laser type** (cost direction: unknown): Xcimer uses KrF excimer lasers at $60–80/J (NOAK target), which is the lowest published $/J in IFE. BLF's OEC/CBC has no published cost. If BLF cannot beat $60–80/J, Xcimer retains the driver cost advantage.
- **Drive scheme** (cost direction: mixed): Xcimer uses hybrid direct drive (brief hohlraum then direct) with ~50% coupling efficiency. BLF uses pure direct drive with potentially higher coupling but needs more beams (500 vs. ~2 final beams for Xcimer).
- **Rep rate and yield tradeoff** (cost direction: mixed): Xcimer targets 0.25–1 Hz with >1 GJ yields. BLF targets 10 Hz with 800 MJ yield per shot. Higher rep rate at lower yield per shot means more target throughput (BLF: ~315M/yr vs. Xcimer: ~8–30M/yr), amplifying target factory cost but enabling smaller chamber clearing requirements per shot.
- **Chamber design** (cost direction: advantage BLF): BLF uses a dry-wall chamber with embedded magnetic fields and DEC. Xcimer uses thick-liquid FLiBe walls. BLF avoids FLiBe inventory cost, FLiBe pumping power, and beryllium supply-chain constraints, but the dry wall faces higher direct neutron loading and requires more frequent first-wall replacement.

[^16]: Inertia laser cost from handwritten laser ICF indirect drive analysis
[^17]: xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule: "Xcimer internal architecture described above can be constructed with total costs of approximately $100 to $120 / joule of laser light on-target in first-of-a-kind (FOAK) systems, and costs of $60 to $80 / joule in nth-of-a-kind (NOAK) systems, roughly an order of magnitude lower than the long-term DPSSL costs estimated above at $700 - $1,000 / joule."
[^18]: osti-servlets-purl-828518/output.md §IV.A. Direct Drive Target Cost Analysis Results: "The results for a 1,000 MW(e) baseline plant indicate that the installed capital cost is about $100M and the annual operating costs will be about $31M (labor $9M; materials/utilities $4M; maintenance $6M); for a cost per target of slightly less than $0.17 each." (Goodin et al., GA-A24429, March 2004)

### Summary of Family Position

BLF's OEC/CBC architecture is a genuine departure from all comparables' driver technology. The potential cost advantage is structural — fiber lasers and optical cavities vs. large glass amplifiers or excimer gas systems — but BLF publishes no $/J figure. The C220104 override brackets the driver cost at $350M–$4,250M (5 MJ × $70–$850/J) using the Xcimer KrF NOAK floor and DPSSL class ceiling from the comparable literature,[^17] with a central estimate of $2,000M (~$400/J). This wide range reflects genuine uncertainty about where fiber-laser OEC technology falls on the cost curve. The direct-drive advantage (no hohlraum, better coupling) vs. indirect-drive comparables is real and reduces both laser energy requirements and per-target cost. Against Xcimer, which publishes $60–$80/J NOAK for KrF excimer, BLF's cost advantage is uncertain — fiber lasers may approach excimer-like costs through commodity scaling, but the OEC pulse-stacking architecture adds optical complexity absent from the KrF design.

## 8. Sources

1. **Sunahara et al., "Laser-based inertial fusion energy system enabled by optical enhancement cavities and a direct-drive configuration reactor," *Optics Express* 33(22), 47104–47120 (2025).**
   - Primary authority source. Provides complete reactor power balance, OEC prototype results, shock ignition physics basis, and reactor concept layout. Contains all quantitative parameters used in this analysis. No cost data.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/optics-express-2025-paper.md`

2. **Blue Laser Fusion website (bluelaserfusion.com).**
   - Company overview, technology description, and D-T/dual-conversion confirmation. Extraction captured only cookie-consent text; qualitative claims come from the dossier's characterization of website content.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/blf-website-and-news.md`

3. **Yahoo Finance press release: "Blue Laser Fusion Completes $37.5M Series Seed" (March 2024).**
   - Funding amount ($37.5M), investor list (SoftBank, Itochu, JAFCO, SPARX, Waseda), and milestone targets (prototype 2025, demonstration reactor 2030).
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/finance-news-blue-laser-fusion-completes-37-114500457/output.md`

4. **Semiconductor Today: "Blue Laser Fusion wins DOE INFUSE project award" (October 2025).**
   - DOE INFUSE award for OEC optical coatings collaboration with Colorado State University.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/semiconductor-today-news-items-2025-oct-blue-laser-fusion/output.md`

5. **Semiconductor Today: "Blue Laser Fusion's Fujioka selected as Japan Moonshot PM" (October 2025).**
   - Japan Moonshot Program Goal 10 selection; University of Osaka joint research institute.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/semiconductor-today-news-items-2025-oct-bluelaserfusion/output.md`

6. **Fuerst et al., "Efficient tritium extraction from PbLi: a potential IFE breeding material" (INL, IFE Workshop).**
   - IFE tritium breeding blanket comparison; tritium demand estimate of 0.366 kg/day for a 2.2 GWth IFE reactor.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/lasers-sites-lasers-files-2023-11-fuerst-idaho-ife-workshop/output.md`

7. **Wong et al., "Helium-Cooling in Fusion Power Plants" (General Atomics, GA-A21804, 1994).**
   - COE estimates for He-cooled blanket concepts: 75 mills/kWh (SiC/SiC ARIES-I) to 55 mills/kWh (advanced SiC Brayton), all in 1994 dollars. Efficiency data for He Brayton cycles.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/osti-servlets-purl-10104516/output.md`

8. **Meier, "Assessment of Tritium Breeding Blankets from a Systems Perspective" (LLNL-TR-658973, 2014).**
   - Comprehensive TBB systems engineering assessment; recommends DCLL-FCI for US program. TBR targets, blanket comparison framework.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/osti-servlets-purl-1165762/output.md`

9. **Wright et al., "Concept Design for a High Temperature Helium Brayton Cycle" (SAND2006-4147, 2013).**
   - He Brayton cycle efficiency: 42.8–45.8% for 1C/1T to 2C/1T configurations at 1000K source temperature. Relative cost methodology for BOP components.
   - Path: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/osti-servlets-purl-1323907/output.md`

10. **Xcimer Energy, "Commercialization of Laser Fusion Energy" (white paper, February 2024).**
    - Published KrF excimer laser driver cost: $100–$120/J FOAK, $60–$80/J NOAK. DPSSL class estimate: $700–$1,000/J. Component-level cost breakdown (Table 1). Used as bracketing evidence for C220104 override.
    - Path: `knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md`

11. **Goodin et al., "Cost-Effective Target Fabrication for Inertial Fusion Energy" (GA-A24429, General Atomics, March 2004).**
    - Nth-of-a-kind DD target factory cost for 1 GWe IFE plant: $100M installed capital, $31M/yr operating, <$0.17/target at 500K targets/day. Used as analogue basis for C220108 override.
    - Path: `knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/osti-servlets-purl-828518/output.md`
