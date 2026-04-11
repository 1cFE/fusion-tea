---
ID: 12-levitated-dipole
Concept: Levitated Dipole (D-T)
Company: OpenStar Technologies
Status: draft
Created: 2026-03-30
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Levitated Dipole (D-T) — OpenStar Technologies

**Concept**: Levitated Dipole — D-T fuel
**Company**: OpenStar Technologies (Wellington, New Zealand)
**Design Point**: Reactor A (208 MWe net) and Reactor B (74.5 MWe net) from Simpson et al. 2026
**Confinement Family**: MFE — Levitated Dipole

---

## Section 1: Availability of Data

**Rating: Moderate**

The levitated dipole concept sits in an unusual position relative to most non-mainstream fusion approaches: a single, remarkably detailed power plant design paper exists (Simpson et al., arXiv 2602.20564), providing full 0D power balance equations, neutronics calculations, coil design parameters, and mass breakdowns for two reactor variants. This is materially more than most early-stage companies publish. However, the absolute LCOE and overnight capital cost figures are deliberately withheld — described as "preliminary results from this model which are subject to change" — and no independent techno-economic analysis of the concept exists. The data is therefore deep in physics and engineering but shallow on the cost side.

**Power plant design documentation:**
Simpson et al. (2026), "Deuterium-Tritium Levitated Dipole Fusion Power Plants" (arXiv 2602.20564) is the primary reference. It presents a 0D power balance model, two optimized reactor design points (Reactor A at 208 MWe and Reactor B at 74.5 MWe), full neutron transport calculations for the shield and blanket, coil stress and field analysis, and a component mass table. The methodology is transparent and peer-reviewed. This is an unusually complete disclosure for a company at OpenStar's funding level.

> "OpenStar is currently in the process of developing a model for estimating the overnight capital cost and LCOE...This study uses preliminary results from this model which are subject to change."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Discussion

**Prototype documentation:**
The Junior prototype paper (arXiv 2508.17691) provides full engineering specifications for the experimental device: magnet geometry, HTS tape quantity, flux pump design, vacuum vessel dimensions, and initial plasma results. It is a clean engineering paper with no significant proprietary omissions.

**Company transparency:**
OpenStar's public communications (website, press releases, news coverage) confirm the development roadmap (Junior → Tahi → Maui → Tama Nui), funding milestones (NZ$10M seed round for Junior, public NZ$35M disclosed in 2026 coverage), and key claims. These are narrative sources without engineering detail.

**Independent analyses:**
No independent techno-economic analysis of levitated dipole fusion power has been published. The LDX experiment at MIT (Boxer et al. 2010) and the RT-1 experiment at University of Tokyo provide the experimental heritage, but neither was oriented toward power plant analysis. No ARIES, PROCESS, or equivalent system-code study of a levitated dipole power plant exists in the public literature.

**Phase 1a dossier completeness:**
After two research iterations, the dossier achieved high confidence on all structural columns (confinement family, fuel, magnet type, neutron management, operation mode) and resolved one important correction (plasma state from "Burning" to "Sustained" after careful re-reading of the power balance equation). Remaining medium-confidence items — thermal cycle specification, full blanket engineering details — are confirmed as genuinely unpublished.

**Key data gaps limiting this analysis:**
1. Absolute LCOE and overnight capital cost figures withheld by OpenStar
2. Thermal conversion cycle (Rankine vs. sCO₂) not specified in any published source
3. Sacrificial coil replacement cost not quantified
4. No confinement scaling data beyond LDX heritage (τ_e ~ 14.5 ms) toward the 3.5 s target
5. No independent system-code or TEA validation of the Simpson et al. design

---

## Section 2: Challenges in Capturing System Function

Challenges ranked by impact on LCOE modeling.

**1. The LCOE model is deliberately withheld (Impact: Critical)**

The Simpson et al. (2026) paper explicitly states that OpenStar's cost model exists but its outputs are "preliminary and subject to change" — absolute cost figures are not reported, only relative constraints (Reactor A maximum overnight cost set to a normalized value of 1.0; Reactor B at 0.5 of that). An LCOE model for the levitated dipole therefore has no company anchor point. All capital cost estimates must be built from analogues: REBCO tape at market price, tungsten at commodity price, blanket by mass, concrete outer vessel by standard construction rates. This is a more severe gap than for any approved prior concept, where at least the design team's own estimate provides a sanity check.

**2. Confinement scaling extrapolation spans six orders of magnitude in triple product (Impact: Critical)**

The only experimental levitated dipole database comes from LDX (MIT/Columbia, 2004–2011) and RT-1 (Tokyo, 2006–present). LDX demonstrated energy confinement times of ~14.5 ms at laboratory parameters. The Reactor A design requires τ_e = 3.5 s — roughly 240× longer. The scaling path through Tahi (the next prototype, ~2028, target 20 T) is not quantified in any publication. The paper is explicit about this dependency:

> "The assumption that these reactors will be Q_sci = 15 is only valid if a smaller demonstration device...displays adequate plasma performance."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Discussion

The designs assume Bohm-like or better confinement scaling. No empirical data confirms which scaling law applies to a high-β levitated dipole. Reactor B is specifically flagged as requiring "a more significant increase" over Bohm-like scaling — i.e., it depends on achieving better-than-Bohm transport. This propagates directly into fusion power and recirculating power fraction, both of which are LCOE-critical.

**3. Annual sacrificial coil replacement — a genuinely novel operating cost structure (Impact: High)**

The outer ~20% of the levitated REBCO coil is "sacrificial": it accumulates neutron fluence to the 1 MW-year/m² threshold over approximately one year, then must be replaced. The inner ~80% is intended to last a decade or more. The docking operation takes ~5 minutes. But the cost of the sacrificial section — its REBCO tape content, winding labor, magnet qualification testing, and remote handling — is nowhere quantified in the public literature. This is a recurring annual operating cost with no analogue in any other fusion concept. Its magnitude relative to capital cost determines whether the modular replacement strategy is an economic advantage or a hidden cost burden. A rough estimate: if the sacrificial section contains ~20% of the 4,320 km of REBCO tape (Reactor A), that is ~864 km/year of tape replacement, at current tape prices of $50–100/kA-m.

> "Intrinsic decoupling of the confining magnetic field-generating REBCO magnets and the vacuum vessel offer unparalleled accessibility and maintainability."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Introduction

The claim of accessibility is engineering-plausible, but the cost of maintaining it annually — under neutron activation conditions — has not been demonstrated or costed.

**4. Plasma edge physics is explicitly uncharacterized (Impact: High)**

The paper's own assessment of the plasma boundary condition is notable for its candor:

> "The physics defining an upper bound on the value of p_lcfs is not well understood as no dipole experiments have yet had enough heating power to generate edge conditions applicable to fusion power plants."
> — arxiv-2602-20564-plasma-state-clarification.md, §2.1.4

The design uses upper bounds on edge temperature (800 eV) and pressure (10³ Pa) borrowed from I-mode tokamak data, not from dipole experiments. If actual edge conditions are more constraining, the plasma triple product falls, Q_sci drops, and the recirculating power fraction rises — directly elevating LCOE.

**5. Thermal cycle unspecified — affects thermal efficiency and BOP cost (Impact: Moderate)**

Despite a stated thermal efficiency of 40%, the actual thermodynamic cycle (steam Rankine, supercritical CO₂ Brayton, or organic Rankine) is nowhere specified in the Simpson et al. paper or any OpenStar public material. The 40% efficiency is consistent with sCO₂ or advanced Rankine, but this is the analyst's inference. The balance-of-plant capital cost — the major cost driver for the thermal island — cannot be accurately estimated without knowing the cycle type and working fluid temperature.

**6. Remote handling of an annually replaced, radioactively activated levitated HTS coil (Impact: Moderate)**

The sacrificial coil replacement requires removing a 550 kg (Junior scale) to ~500 kg (sacrificial section, scaled from 2,560 tonne total) component from a radioactive environment, refurbishing it externally, and re-inserting it. The paper claims a 5-minute docking time, but this appears to refer to the cryogenic coupling operation, not the full replacement cycle including remote handling, testing, and logistics. In D-T operation, the magnet assembly accumulates activation from 14 MeV neutrons, requiring hot-cell handling. No remote handling system for this specific geometry has been designed or costed.

**Modeling Approach Recommendation: Free-Form Analogue Estimation**

Because no reference fusion concept shares the levitated dipole's architecture (single internal levitated coil, modular annual replacement, solid ceramic blanket, concrete outer vessel), 1costingfe-style adaptation from a reference concept is not appropriate — there is no anchor concept whose cost structure can be rescaled. The recommended approach is free-form analogue estimation anchored to the component mass data in Simpson et al. Table 5, with four primary estimation paths:

1. **Core magnet** (cost-dominant): REBCO tape quantity (4,320 km, Reactor A) × $/kA-m at projected market price, plus structural CICC conduit, coil winding labor, and cryostat. The paper explicitly benchmarks magnet physical scale against CFS ARC — ARC magnet cost estimates are the nearest published analogue for a high-field REBCO coil at this stored energy (~20 GJ). Annual sacrificial section replacement (~864 km/yr of tape + remote handling + qualification testing) must be modeled as a separate recurring O&M capex line with no analogue in any other fusion concept.
2. **Blanket and neutron shield**: Material quantities given in Table 5 (Li₂O: 3,490 t; W-B₄C-W tiles: 1,760 t) allow direct commodity-price estimates. Apply manufacturing and installation multipliers (ceramic tile fabrication, tungsten tile processing above recrystallization temperature). Li₂O uses natural lithium — no enrichment cost.
3. **Outer vacuum vessel**: Reinforced concrete (38,700 t) and structural steel — dominated by commodity construction costs. The paper argues this is explicitly cost-advantaged vs. precision steel tokamak VVs, and the mass breakdown supports treating this as a straightforward civil engineering analogue.
4. **Balance of plant / thermal island**: Standard thermal power island $/kWth, with cycle type held as a scenario variable (sCO₂ Brayton at ~44% vs. steam Rankine at ~37% efficiency brackets the 40% placeholder). This is the most transferable analogue from other fusion or advanced fission concepts.

**Key Hypotheses for the Cost Model**

The three parameters with the highest continuous LCOE leverage are:

- **τ_e / Q_sci (confinement scaling)**: Required τ_e = 3.5 s (Reactor A) vs. 14.5 ms demonstrated (LDX) — a 240× extrapolation under Bohm-like scaling; Reactor B requires better-than-Bohm. Sensitivity range: 0.5–2× the required value, propagating directly into recirculating power fraction and net output. *If Tahi fails to reach the Bohm-like n·τ_e threshold (3.23×10¹⁹ s·m⁻³ at 1 keV), Reactor A is not viable as designed — the optimizer must either increase magnet scale, raising overnight capital cost above the normalized baseline, or accept Q_sci < 15, elevating LCOE.*
- **Annual sacrificial coil replacement cost (% of overnight capex)**: Driven by REBCO tape price (~864 km/yr × $/kA-m) plus remote handling and qualification labor. The paper asserts this "does not make a significant impact" but provides no dollar figure. *If annual replacement cost exceeds ~3–5% of overnight capital per year — the threshold above which it dominates O&M — the concept loses its operating-cost edge vs. an ST-HTS that also uses REBCO but does not require annual internal component replacement.*
- **Thermal efficiency (η_th)**: Single-point assumption of 40% with no cycle specified. Plausible range 35–47%. *A 5 percentage-point reduction (40% → 35%) lowers net output by ~12% at constant fusion power, raising LCOE proportionally — equivalent to requiring a ~12% reduction in overnight capital to maintain cost competitiveness.*

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature to most mature.

---

**D-T Fusion at Q_sci = 15 in a Levitated Dipole — TRL 2**

- **Demonstrated**: Laboratory-scale levitated dipole plasma confinement. LDX demonstrated plasma pressure peaking and good confinement properties at low parameters (ne ~ 10¹⁷ m⁻³, Te ~ 200 eV). RT-1 demonstrated high-β plasma. Junior demonstrated levitated HTS coil confinement with <50 kW ECRH heating (Feb 2026). No levitated dipole has operated with D-T fuel, neutral beam or ICRH heating, or at fusion-relevant triple products.
- **On paper only**: Confinement scaling from laboratory parameters to τ_e = 3.5 s. D-T operation and 14 MeV neutron environment in a levitated configuration. ICRH heating at 44.5 MW in a dipole geometry. Alpha particle confinement and thermalization (ASCOT5 simulations exist but are exploratory). Q_sci = 15 operating point.
- **Missing at scale**: Any experimental demonstration in the 10–100 keV temperature range. Triple product validation. Plasma stability at high beta with D-T alpha heating. Any in-situ neutron environment testing.

---

**Annual Sacrificial Coil Replacement Cycle — TRL 2–3**

- **Demonstrated**: In principle: Junior's modular coil design has been built and the vacuum vessel features a custom DN1240 ISO-F port sized for core magnet removal. The concept of replacing a superconducting magnet periodically is novel but the mechanical interfaces exist in Junior. The 5-minute docking operation for cryogen exchange has been described in the patent.
- **On paper only**: Full annual replacement cycle at power-plant scale. Handling procedures for an activated (neutron-irradiated) HTS coil assembly. Qualification and testing of replacement coils prior to installation. Logistics of maintaining a coil spare pool for continuous operation.
- **Missing at scale**: Any demonstration of coil replacement under activation conditions. REBCO tape behavior after neutron fluence at 1 MW-year/m² threshold. Full cost data for the replacement cycle including handling, testing, and refurbishment.

---

**Levitated HTS Coil at 23 T with On-Board Superconducting Flux Pump — TRL 3–4**

- **Demonstrated**: Junior achieved levitation with ~2.35 T core field and a world-record HTS flux pump delivery of ~170 kJ stored energy. The transformer-rectifier flux pump design (patented) functioned as intended. Tahi prototype targets 20 T (~2028). The Junior coil used 6.3 km of REBCO tape in 14 non-insulated solder-impregnated coils.

> "greatest magnetic stored energy delivered by an HTS flux pump to date"
> — arxiv-2508-17691-junior-design-results.md, §Flux Pump Results

- **On paper only**: 23 T peak field in the power plant CICC architecture with neon slush cooling at 24.6 K. Flux pump output sufficient to charge a 20+ GJ stored-energy coil. Two-section coil architecture with defined interface between sacrificial outer and semi-permanent inner sections. Current lead elimination during levitated operation.
- **Missing at scale**: HTS flux pump scaling to 29.4 kA operating current (vs ~600 A demonstrated). REBCO tape performance at 23 T peak field and 30 K operating temperature under combined mechanical stress and neutron irradiation. Structural integrity of the coil conduit at the sacrificial/inner section interface under differential fluence.

---

**Li₂O Solid Ceramic Tritium Breeding Blanket — TRL 3–4**

- **Demonstrated**: Li₂O ceramic tritium breeding material tested in fission reactor environments (ITER HCPB TBM program). Small-scale neutron irradiation experiments. Solid ceramic breeders are the ITER/DEMO baseline.
- **On paper only**: Full blanket module for the levitated dipole geometry: modular panels mounted to the inner vacuum vessel outer wall, achieving TBR = 1.1 with ~75% neutron coverage (the remaining ~25% intercepted by the core magnet region). Tritium extraction system at kg/day throughput from solid Li₂O. Cooling scheme for the blanket under simultaneous neutron and gamma heating. Blanket panel replacement schedule.
- **Missing at scale**: 14 MeV neutron irradiation of Li₂O at fusion-relevant fluences and temperatures. Tritium inventory and permeation characterization from Li₂O at operating conditions. Structural performance of modular blanket panels under thermal cycling and neutron swelling over plant lifetime.

**Note on breeding geometry**: The paper achieves TBR = 1.1 with natural (unenriched) Li₂O, relying on neutron multiplication in the tungsten shield. The core magnet region intercepts ~25% of fusion neutrons — this coverage loss is partially compensated by the high neutron multiplication factor of tungsten.

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: Gram-scale tritium handling in existing fusion experiments (JET, TFTR). Laboratory-scale tritium extraction from solid breeders. Tritium accountability and permeation barrier technology exists.
- **On paper only**: Closed-loop tritium fuel cycle at kg/day scale. Self-sufficient TBR > 1 in an operating D-T power plant. Tritium extraction from Li₂O ceramic at plant operating temperatures. Startup tritium inventory (~1 kg) management during the critical initial period before self-sufficiency.
- **Missing at scale**: Industrial-scale tritium processing. Low-inventory tritium storage compatible with the regulatory framework. Permeation-resistant primary loop materials validated under 14 MeV neutron flux.

---

**ICRH Heating System at 44.5 MW Wall-Plug Input — TRL 4–5**

- **Demonstrated**: MW-class ICRH systems routinely operated in major tokamaks (JET, ITER construction). ICRH antenna design is mature at ~40–55 MHz. Wall-plug efficiency ~70% is achievable with current transmitter technology.
- **On paper only**: ICRH in a dipole magnetic geometry. The field topology of a levitated dipole differs fundamentally from a tokamak — wave coupling and single-pass absorption are not characterized. Antenna placement around the levitated coil assembly. 44.5 MW total heating at 70% efficiency = 63.6 MW wall plug power.
- **Missing at scale**: Any experimental demonstration of ICRH in a levitated dipole configuration. RF coupling models for dipole field geometry. Antenna geometry compatible with coil docking access and neutron shielding.

---

**Neon Slush Cryogenic System — TRL 4–5**

- **Demonstrated**: Liquid neon cooling systems exist at smaller scale. Slush neon (neon + solid neon ice at melting point 24.6 K) is used in industrial applications for latent heat storage.
- **On paper only**: Onboard neon slush reservoir sized for 45-minute float time between docking cycles. Rapid drain-and-refill system ("slushy is pumped out of reservoir channels, and new slushy is quickly pumped right back in"). Neon supply chain at the scale required for continuous plant operation.
- **Missing at scale**: Engineering demonstration of the full dock-undock-redock cycle with the specific reservoir geometry. Neon production capacity assessment for a fleet of plants (neon is a byproduct of air liquefaction with limited dedicated production capacity). The paper acknowledges this risk: "if procuring and maintaining a supply of neon proves challenging it would be a viable alternative" [referring to hydrogen as backup].

---

**Layered W-B₄C-W Neutron Shield — TRL 4–5**

- **Demonstrated**: Tungsten fabrication and tungsten tile technology are mature in fusion (ITER divertor, W-monoblock). B₄C neutron absorption well-characterized. The neutron transport calculation for the 475 mm shield (W/B₄C/WC layered architecture) achieves the required 4-decade attenuation of fast neutron flux to protect REBCO tape.
- **On paper only**: Tungsten tiles at 1950 K operating temperature in steady-state — above the recrystallization temperature, requiring grain size control to manage creep. Radiatively cooled (not actively cooled) shield design for the dipole geometry. Integration of shield with blanket panel attachment.
- **Missing at scale**: Long-term creep and mechanical performance of tungsten tiles above 1950 K under 14 MeV neutron irradiation. Joint design between shield and blanket that maintains structural integrity over plant lifetime. Tungsten tile replacement strategy as the shield activates.

> "Tungsten will undergo recrystallization and it is possible that the onset of degraded mechanical properties can be delayed until other forms of damage dominate."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §4.3 Neutron Transport

---

**REBCO HTS Magnets (General Technology) — TRL 6–7**

The underlying REBCO tape technology benefits from active commercial development across multiple fusion programs. CFS demonstrated a 20 T full-bore REBCO insert magnet in January 2024. Tokamak Energy's Demo4 validated a complete 14+2 coil HTS set at 11.8 T in November 2025. The Junior prototype demonstrated the non-insulated solder-impregnated coil architecture at 2.35 T.

- **On paper only at 23 T**: The power plant peak field of 23 T has not been demonstrated in a levitated coil configuration. Consistent Jc > 150 MA/cm² at 23 T, 30 K in radiation environment is not yet demonstrated.
- **Missing at scale**: REBCO tape production at several thousand km per year with consistent critical current properties. Long-term performance under combined radiation, mechanical stress, and cryogenic cycling.

---

**Balance of Plant / Power Conversion — TRL 8–9**

Thermal power conversion systems (steam Rankine, sCO₂ Brayton, ORC) are fully commercial at GW scale. The specific cycle for the levitated dipole is unspecified, but no exotic BOP technology is required — the concept outputs thermal energy to a conventional cycle.

- **Missing**: Integration of tritium-bearing primary coolant with the power conversion system. Heat exchanger qualification for tritium permeation control. Specific BOP design for the dipole reactor geometry has not been developed.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape**

Reactor A requires approximately 4,320 km of REBCO tape in the core magnet, plus an additional ~1,200 km equivalent for the top magnet [arxiv-2602-20564-dt-dipole-power-plants.md, §Table 5]. This total of ~5,520 km is comparable to estimates for compact HTS tokamaks (the CFS ARC reference design requires >5,000 km). However, the levitated dipole adds a recurring demand: the sacrificial outer section (~20% of core magnet tape = ~864 km) requires annual replacement. Over a 30-year plant life, cumulative tape consumption approaches ~31,000 km per Reactor A — roughly 5× the initial inventory.

Global REBCO production capacity is currently on the order of 1,000–2,000 km/year across all manufacturers (SUNAM, Faraday Factory Japan, Shanghai Superconductor, SuperPower). This is already insufficient for a single Reactor A deployment let alone fleet scale. Tape prices (~$50–100/kA-m at current volumes) must fall substantially for the annual replacement cost to be acceptable. The shared supply chain with HTS tokamaks (CFS, Tokamak Energy, and others) creates both competition for limited tape and potential economies of scale if multiple programs drive down costs simultaneously.

**Tungsten**

The W-B₄C-W shield requires 1,760 tonnes of tungsten for Reactor A [arxiv-2602-20564-dt-dipole-power-plants.md, §Table 5]. Global tungsten production is approximately 80,000–90,000 tonnes per year (primarily from China). A single Reactor A deployment therefore represents ~2% of annual global tungsten output. A fleet of ten plants would consume ~20% of annual production for initial builds, plus replacement over time. Tungsten is not a scarce material at current production levels, but the high-temperature tile fabrication (above recrystallization temperature behavior at 1950 K) requires specialized processing that is not currently industrialized at fusion scale.

**Lithium and Li₂O for Breeding Blanket**

The blanket requires 3,490 tonnes of Li₂O for Reactor A [arxiv-2602-20564-dt-dipole-power-plants.md, §Table 5]. A notable advantage: the paper achieves TBR = 1.1 using natural (unenriched) lithium, exploiting neutron multiplication in tungsten. This avoids the supply chain and cost burden of Li-6 isotope enrichment — a significant differentiator from FLiBe or lithium-6-enriched blankets used in other concepts. Natural Li₂O is produced industrially; at 3,490 tonnes per plant, global lithium production (approaching 200,000 tonnes/year) presents no bottleneck.

**Tritium**

Standard D-T startup and operation constraints apply. Global civilian tritium inventory is ~25 kg; a power plant startup requires ~1 kg, but the fleet cannot scale without self-sufficient TBR > 1 breeding. The design TBR of 1.1 provides a 10% margin — adequate but not generous. Tritium decay (5.5%/year half-life element) constrains how long tritium can be stockpiled between prototype milestones. Unique to the levitated dipole: the annual coil replacement may introduce a tritium inventory disruption during docking, as the core magnet passes through the blanket region. Tritium accounting during docking cycles has not been addressed in published materials.

**Neon (Cryogen)**

Neon is required for the onboard slush cryogen reservoir. Neon is produced as a byproduct of air liquefaction (0.0018% of atmosphere) and global supply is limited — production is approximately 200,000 m³/year, concentrated among a small number of air separation unit operators. Unlike helium (a cryogen with explicit supply chain concerns for fusion), neon is domestically producible but at low volumes. A fleet of plants requiring continuous neon circulation and top-off could create a material supply tension. The paper acknowledges this and proposes hydrogen as an alternative, requiring a 5× larger cryogen reservoir volume.

**Concrete and Structural Steel**

The outer vacuum vessel is primarily reinforced concrete (38,700 tonnes for Reactor A) — a non-exotic material abundant at any construction site. This is a deliberate design choice: the paper notes that "can be built with contemporary materials and traditional manufacturing methods, substantially reducing cost and technology risk." The dominance of concrete in the mass budget (38,700 of 45,100 total tonnes for Reactor A) is economically favorable.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion power (Reactor A) | 667 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | Primary design point |
| Fusion power (Reactor B) | 237 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | Smaller/industrial variant |
| Net electrical output (A) | 208 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Table 9 | high | After all recirculating loads |
| Net electrical output (B) | 74.5 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Table 9 | high | After all recirculating loads |
| Q_sci (scientific gain) | 15 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | medium | Target requiring Tahi validation; not yet demonstrated |
| Thermal efficiency (η_th) | 40% | arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 | medium | Assumed value; thermal cycle unspecified |
| Auxiliary heating efficiency (η_aux) | 70% (ICRH) | arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 | high | ICRH baseline; higher than ECRH |
| Auxiliary heating power (A) | 44.5 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | Wall plug: 63.6 MW |
| Auxiliary heating power (B) | 15.8 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | Wall plug: 22.6 MW |
| Gross electrical output (A) | ~296 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Table 9 | high | Before recirculating loads; "Total electrical power" |
| Recirculating power fraction (A) | ~30% | [inferred: (296 − 208)/296 from Table 9 gross vs. net electric] | medium | Dominated by heating wall-plug (63.6 MW) + other loads (~23 MW) |
| Plant duty cycle | 90.1% (A), 90.2% (B) | arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 | high | Pulsed by cryogenic limits, not plasma physics |
| Plant availability | 96% | arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 | medium | Includes 2-week annual maintenance; unverified |
| Energy confinement time (A) | 3.5 s | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | medium | Required; not yet demonstrated at any scale |
| Energy confinement time (B) | 5.9 s | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | medium | Required; longer than Reactor A due to lower density |
| Peak magnetic field (A) | 23.0 T | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | At REBCO winding; CICC architecture |
| Peak magnetic field (B) | 21.8 T | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | |
| Global plasma beta (A) | 4.37% | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | |
| Global plasma beta (B) | 4.84% | arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 | high | |
| Peak ion temperature (A) | 10.9 keV | arxiv-2602-20564-plasma-state-clarification.md §Table 9 | high | Lower than typical tokamak designs (~15–20 keV) |
| Peak electron density (A) | 1.95 × 10²⁰ m⁻³ | arxiv-2602-20564-plasma-state-clarification.md §Table 9 | high | |
| Tritium breeding ratio | 1.1 | arxiv-2602-20564-dt-dipole-power-plants.md §4.3 | medium | With natural Li₂O + W neutron multiplication |
| Core magnet mass (A) | 2,560 tonnes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Includes REBCO coil, shield, structure |
| Total plant mass (A) | 45,100 tonnes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Dominated by concrete (38,700 t) |
| Tungsten shield mass (A) | 1,760 tonnes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | W-B₄C-W layers |
| Li₂O blanket mass (A) | 3,490 tonnes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Natural lithium; solid ceramic |
| REBCO tape requirement (A) | 4,320 km | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Core magnet only; +~1.2 km top magnet |
| Sacrificial coil section | ~20% of total | arxiv-2602-20564-dt-dipole-power-plants.md §4.1 | medium | Annual replacement; ~864 km/yr tape |
| Cryogenic float time | 45.5 min (A), 46.1 min (B) | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Between docking cycles |
| Cryogenic efficiency (η_cryo) | 1.25% | arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 | high | Neon slush at 24.6 K; very poor efficiency as expected for deep cryogenics |
| Cryogenic cooling load (A) | 14.1 kW deposited, 1.31 MW wall plug | arxiv-2602-20564-dt-dipole-power-plants.md §Table 9 | high | [inferred: 14.1 kW / 0.0125 efficiency = 1.13 kW wall plug; paper states 1.31 MW, implying additional fixed loads] |
| Junior prototype cost | <$10M USD | arxiv-2508-17691-junior-design-results.md §3 | high | "designed and built in under 2 years at a cost of <$10M USD" |
| Junior HTS tape (core magnet) | 6.3 km | arxiv-2508-17691-junior-design-results.md §3 | high | 14 NI solder-impregnated coils |
| Junior peak field (design) | 5.63 T | arxiv-2508-17691-junior-design-results.md §Table | high | Operated at 2.35 T (~42% of design) |
| Junior flux pump stored energy | ~170 kJ (world record) | arxiv-2508-17691-junior-design-results.md §Flux Pump | high | World record for HTS flux pump delivery |
| Tahi target field | 20 T | dossier (arXiv 2602.20564 ref.) | high | Next prototype, ~2028 |
| Tama Nui commercial range | 50–200 MWe | openstar-2026-funding-tahi-timeline.md | medium | Fourth-generation commercial plant; scale TBD |
| Overnight capital cost (relative) | A = 1.0, B = 0.5 (relative) | arxiv-2602-20564-dt-dipole-power-plants.md §3.3 | low | Relative only; absolute numbers withheld |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Absolute overnight capital cost ($/kWe) | proprietary | blocking | OpenStar model exists but figures withheld as "preliminary" |
| LCOE estimate ($/MWh) | proprietary | blocking | Same withholding policy |
| Thermal cycle type (Rankine vs. sCO₂) | truly-unknown | important | No source mentions a specific cycle; affects BOP cost and efficiency |
| Sacrificial coil replacement cost ($/year) | truly-unknown | blocking | No cost published; critical recurring O&M item |
| O&M cost breakdown (fixed + variable) | truly-unknown | important | No O&M estimates in any public source |
| Disruption-driven first wall replacement rate (avoided) | not-yet-sourced | important | Section 7 identifies disruption-free operation as a genuine LCOE advantage vs. inductive tokamaks. No tokamak comparator cost figure exists to quantify the avoided cost; flag as qualitative advantage unless a reference tokamak disruption O&M cost is sourced and applied as a delta |
| Thermal energy storage capital cost (avoided) | not-yet-sourced | important | Inductive tokamaks require thermal energy storage for grid decoupling during disruptions; levitated dipole mechanically cannot disrupt. Quantifying this avoided cost requires a tokamak BOP reference; treat as qualitative advantage until sourced |
| First wall thermal load (MW/m²) | not-yet-sourced | important | Wall loading drives first wall replacement schedule and cost |
| First wall material and lifetime | not-yet-sourced | important | Paper discusses shield but not first wall specifically |
| Plasma startup time and energy | truly-unknown | nice-to-have | Affects capacity factor and heating system sizing |
| ICRH antenna design and cost | truly-unknown | important | No ICRH design for dipole geometry exists |
| Top magnet design and cost | truly-unknown | important | Paper states "details of levitation coil have not been considered" |
| Li₂O blanket module unit cost | not-yet-sourced | important | Mass known; cost per tonne requires manufacturing estimate |
| Remote handling system design | truly-unknown | important | Required for activated coil replacement; no design published |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Absolute overnight capital cost ($/kWe) | S1, S5 | proprietary | blocking | OpenStar internal model; watch for future publications |
| 2 | Sacrificial coil annual replacement cost | S2, S5 | truly-unknown | blocking | Requires cost model for REBCO winding + remote handling + testing |
| 3 | Thermal conversion cycle specification | S2, S5 | truly-unknown | important | Contact company; likely decided internally but not published |
| 4 | Confinement scaling law for levitated dipole | S2, S3 | truly-unknown | blocking | Requires Tahi experimental results (~2028–2030); no proxies exist |
| 5 | ICRH coupling in dipole geometry | S3 | truly-unknown | important | No published RF physics study for dipole configuration |
| 6 | Plasma edge conditions in D-T dipole | S2, S3 | truly-unknown | important | Requires high-power dipole experiments; acknowledged gap in paper |
| 7 | Top magnet design and cost | S3, S5 | truly-unknown | important | Explicitly out of scope in Simpson et al.; paper assumes negligible cost |
| 8 | Remote handling system for activated coil | S3, S5 | truly-unknown | important | No design study published |
| 9 | First wall thermal load and material choice | S3, S5 | not-yet-sourced | important | Paper focuses on shield/blanket; first wall not detailed |
| 10 | O&M cost breakdown (fixed vs. variable) | S2, S5 | truly-unknown | important | No O&M estimates in any published source |
| 11 | Neon supply chain assessment at fleet scale | S4 | not-yet-sourced | important | Industrial neon capacity has not been evaluated for fusion applications |
| 12 | Tritium accounting during docking cycles | S4 | truly-unknown | nice-to-have | Core magnet passes through blanket region during replacement |
| 13 | REBCO critical current at 23 T under neutron irradiation | S3 | truly-unknown | important | Irradiation database exists up to ~10–12 T; 23 T regime uncharacterized |
| 14 | Li₂O blanket module unit cost | S5 | not-yet-sourced | important | Mass known; cost requires manufacturing analogues |
| 15 | Independent TEA or system-code analysis | S1 | truly-unknown | nice-to-have | No ARIES/PROCESS equivalent for levitated dipole exists |

---

## Section 7: Cross-Concept Notes

**Nearest neighbors**: spherical tokamak HTS (technology comparator — shared REBCO supply chain, common HTS magnet challenges, and parallel commercial timeline) and field-reversed configuration (physics comparator — high-beta compact MFE with a comparable confinement uncertainty profile and no wall-connected field lines).

### Key Differentiators vs. Conventional Tokamak

The levitated dipole diverges from a conventional tokamak across all five structurally load-bearing dimensions for TEA:

- **Confinement mechanism**: Plasma confined by turbulent inward pinch in a dipole field — peaked pressure profiles arise spontaneously, not from active control. Conventional tokamaks work to suppress this same class of turbulent transport. The inverted physics challenge provides no experimental scaling database above laboratory parameters. Cost implication: this is a **binary threshold risk**, not a continuous cost penalty. If Tahi validates Bohm-like or better scaling (n·τ_e ≥ 3.23×10¹⁹ s·m⁻³ at 1 keV), the concept is viable at the modeled capital cost. If scaling is sub-Bohm, the reactor requires a larger magnet assembly — raising overnight capital above the normalized baseline — or is nonviable as designed. There is no intermediate "more expensive but viable" outcome at current design margins.
- **Coil topology**: Single superconducting coil levitated inside the plasma volume; no toroidal field coils, no central solenoid, no plasma current drive. A conventional tokamak requires 16–18 external coils (TF + PF + CS). Cost is concentrated in one component that must be periodically replaced rather than distributed across a large fixed external coil set. Cost implication: **penalty risk**. Periodic replacement of the core magnet assembly creates a recurring O&M capital line with no analogue in any other fusion concept (or in fission). Where a tokamak's external coils are a one-time capital cost, the levitated dipole's internal coil is also a running cost — estimated at ~864 km/yr of REBCO tape plus remote handling, qualification testing, and spare pool logistics. The magnitude is unquantified, and until it is, the claim that this cost "does not make a significant impact" (Simpson et al.) cannot be verified from outside the company.
- **No plasma current → no disruptions**: Levitated dipole carries no toroidal plasma current; MHD disruptions are mechanistically absent. No disruption mitigation system, thermal dump resistors, or first-wall fatigue from disruption energy deposition. In LCOE terms: no disruption-driven first-wall replacement schedule and no need for thermal energy storage for grid decoupling.
- **Operating mode basis**: Plasma is inherently steady-state; the 90.1% "duty cycle" is set by cryogenic coil thermal limits, not plasma pulse length. Inductive tokamaks are pulse-limited by central solenoid flux swing. This is a more favorable capacity-factor basis — the plasma never needs to restart.
- **Cost structure shape**: Tokamak capital cost is distributed across external coil set, blanket, divertor, and VV. The levitated dipole concentrates capital in a single magnet assembly and trades divertor scheduled maintenance for annual sacrificial coil replacement. Neither the magnitude of that trade nor which side wins is determinable without published cost figures.

**Prior analysis referenced**: 21-spherical-tokamak-hts (approved, 2026-03-20)

### Shared with Spherical Tokamak HTS (21-spherical-tokamak-hts)

The levitated dipole and spherical tokamak share the REBCO HTS technology foundation. Both concepts require thousands of km of REBCO tape per plant, face the same tape cost trajectory challenge ($50–100/kA-m current vs. ~$10/kA-m target), and depend on the same set of manufacturers (SUNAM, Faraday Factory Japan, Shanghai Superconductor). Supply chain constraints and cost assumptions from the ST analysis apply here.

Both concepts are D-T with unspecified thermal cycles, and both cite 40% thermal efficiency as a placeholder — suggesting this is a community default, not a design-specific value. Both analyses flag the missing thermal cycle specification as a data gap.

Neither concept has published absolute capital cost estimates. OpenStar explicitly withholds its LCOE model; Tokamak Energy has not published any cost data.

### Key Divergences from Spherical Tokamak HTS

**Coil architecture**: Where the spherical tokamak uses multiple external coils (TF + PF sets), the levitated dipole uses a single levitated internal coil. This is radically simpler in coil count but introduces the novel challenge of periodic replacement under neutron activation. The ST analysis noted center stack shielding (WC cermet) as a key TRL challenge; the levitated dipole faces an analogous geometry-specific shielding problem with its core magnet assembly.

**Blanket geometry**: The ST uses an outboard-only liquid lithium blanket forced by the compact center stack constraint (< 32 cm shielding depth). The levitated dipole uses a modular Li₂O solid blanket covering ~75% of the neutron solid angle — the remaining 25% intercepted by the core magnet. Both face partial coverage challenges from their respective geometries. However, Li₂O ceramic requires no enrichment (unlike the ST's proposed liquid Li approach), and the levitated dipole achieves TBR = 1.1 without neutron multipliers other than the tungsten already required for shielding.

**Heating method**: ST-E1 uses ECRH exclusively during flat-top; levitated dipole uses ICRH as the baseline, claiming higher wall-plug efficiency (70% vs. ~50–55% for gyrotrons). If realized, this improves Q_engineering. However, ICRH coupling in a dipole geometry is undemonstrated, while ECRH in tokamaks is operationally mature.

**Operating mode**: Both are quasi-steady, but for different reasons. ST pulses are limited by central solenoid flux swing. The levitated dipole "pulses" due to cryogenic reservoir thermal limits — the plasma itself is steady-state capable. This is a more favorable physical basis for high capacity factor.

**Disruption risk**: The ST analysis flagged plasma disruptions as a material risk to first-wall and divertor lifetime, requiring thermal energy storage for each pulse. Levitated dipoles are inherently disruption-free. This is a genuine LCOE advantage — no disruption-driven first-wall fatigue, no thermal energy storage required for grid coupling, and no divertor component replacement schedule.

**Cost structure shape**: The ST cost structure is dominated by the magnet and blanket capital costs, with divertor replacement contributing significantly to operating costs. The levitated dipole trades divertor cost for the annual sacrificial coil replacement cost. Which is lower cannot be determined without published figures from either company.

### Comparison with Field-Reversed Configuration (Helion, concept 08-frc-w-direct-conversion)

The FRC is the second nearest neighbor in the high-beta compact MFE space. Both concepts confine plasma without wall-connected field lines, operate at near-maximum beta, and depend on physics uncertainty as the dominant cost lever — in both cases, if confinement or plasma performance doesn't scale, LCOE is undefined rather than merely elevated. Key TEA divergences: Helion's FRC is pulsed (2 Hz commercial target), making LCOE a per-pulse × rep-rate calculation with a threshold structure (magnetic energy recovery efficiency η_recovery below ~85–90% makes the plant a net consumer) — while the levitated dipole is steady-state, with LCOE driven continuously by capacity factor and confinement scaling. Helion's D-³He mode targets elimination of the tritium breeding blanket and thermal conversion cycle entirely through direct inductive energy recovery, potentially removing two major capex categories that the levitated dipole retains; the FRC's dominant capex uncertainty is the pulsed capacitor bank (no published $/J figure), while the levitated dipole's is the internal coil system and confinement scale-up. Neither concept has a published independent plant study equivalent to ARIES or PROCESS, and neither has disclosed absolute capital costs.

---

## Section 8: Sources

**1. Simpson et al. (2026). "Deuterium-Tritium Levitated Dipole Fusion Power Plants." arXiv:2602.20564.**
The primary source for all power plant parameters: 0D power balance, two design points (Reactor A and B), coil specifications, neutronics, component masses, and the cost optimization framework. Provides the most complete publicly available design for a commercial levitated dipole D-T reactor. Path: `exploration/phase_1a/research/12-levitated-dipole/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md` (also accessed as iter-02 plasma-state-clarification variant).

**2. OpenStar Team (2025). "Design and Initial Results from Junior LDX." arXiv:2508.17691.**
Engineering specifications for the Junior prototype: HTS coil design (14 NI solder-impregnated coils, 6.3 km REBCO tape, 550 kg floating mass), flux pump design and world-record performance (~170 kJ stored energy), vacuum vessel geometry, and first plasma results. Establishes current TRL baseline. Path: `exploration/phase_1a/research/12-levitated-dipole/iter-01/sources/arxiv-2508-17691-junior-design-results.md`

**3. OpenStar Technologies website and news coverage (2025–2026).**
Development roadmap (Junior → Tahi → Maui → Tama Nui), funding disclosures (NZ$10M seed, public NZ$35M round), and levitation milestone announcement (February 2026). Commercial targets: Tama Nui at 50–200 MWe. Path: `exploration/phase_1a/research/12-levitated-dipole/iter-01/sources/openstar-prototype-roadmap.md`; `iter-02/sources/openstar-2026-funding-tahi-timeline.md`

**4. Phase 1a Dossier: Levitated Dipole (D-T). (2026-03-07).**
Consolidated per-column values with confidence ratings from two research iterations. Corrects the plasma state classification from "Burning" to "Sustained" with evidence from the power balance equation. Path: `exploration/phase_1a/research/12-levitated-dipole/dossier.md`

**5. Boxer, A.C. et al. (2010). "Turbulent inward pinch of plasma confined by a levitated dipole magnet." *Nature Physics* 6, 207–212.**
Foundational LDX experimental result demonstrating peaked density profiles from turbulent pinch — the key confinement mechanism that distinguishes a levitated from a supported dipole. Not in Phase 1a sources; referenced for heritage context.

**6. Hasegawa, A. et al. (1990). "A D-³He fusion reactor based on a dipole magnetic field." *Nuclear Fusion* 30(11), 2405.**
Original theoretical proposal for the dipole fusion concept. Not in Phase 1a sources; historical reference.
