---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion (Helion Energy)
Company: Helion Energy
Status: draft
Created: 2026-06-09
Approved-Date:
Confinement-Family: MFE
Archetype: PULSED_FRC
Archetype-Fit: Low
Comparison-Status: costingfe
Comparables: []
Design-Point-Name: Orion — Helion 8th-generation first commercial plant (50 MWe Microsoft PPA, 2028 target)
Design-Point-Maturity: pilot-demonstrator
P-Native: 50
Grounding-Confidence: medium
---

## Design Point

- Name: Orion — Helion 8th-generation first commercial plant (50 MWe Microsoft PPA, 2028 target)
- Maturity: pilot-demonstrator
- P_native: 50 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md

## 1. Availability of Data

**Rating: Limited**

Helion Energy's public disclosure sits in an unusual position: rich milestone and technical approach data, but opaque on plant-level engineering and economics. The company has published extensive material on its technology philosophy, prototype progression through seven generations (Grande through Polaris), and fusion physics achievements. The February 2026 announcement of 150 million degrees Celsius (13 keV) D-T fusion in Polaris represents a quantified physics milestone with expert validation. Academic heritage is well-documented: founders Slough, Kirtley, Pihl, and Votroubek came from University of Washington / MSNW LLC, where Inductive Plasmoid Accelerator (IPA) experiments (2005-2012) established the colliding FRC formation and acceleration technique. Peer-reviewed publications by Slough et al. in *Nuclear Fusion* (2011) and Kirtley & Milroy in *Journal of Fusion Energy* (2023) describe FRC merging/compression physics and scaling relations.

However, no published power plant design study analogous to ARIES (tokamak/stellarator studies) or Z-IFE (for MagLIF) exists for Helion's commercial concept. The company has not released:
- Engineering drawings or detailed specifications for Orion beyond "50 MWe, 2028 target, Microsoft PPA"
- Quantitative Q (fusion gain) values for any prototype, including Polaris
- Direct conversion efficiency measurements (85-95% is claimed but not validated in peer review)
- System-level cost breakdown (capital cost, LCOE target, subsystem cost allocation)
- Tritium breeding ratio or He3 production rate data from DD side reactions
- Component lifetime projections (magnets, capacitors, plasma-facing structures under pulsed loading)

> "Helion has achieved 100+ million degrees Celsius … in its seventh-generation Polaris prototype"
> — helion-milestones-feb2026.md, §Fusion Milestones

The ARPA-E presentation (docslib-helion-arpa-e-presentation.md) provides some performance targets: 50 MW at 2 Hz repetition rate, 40 Tesla reactor field goal, and an input efficiency target of <$0.03/MJ. These are design targets, not demonstrated values. The company's website (helion-website-technology.md) describes architecture comprehensively but provides no engineering detail on chamber design, blanket structure, or thermal management.

Third-party analyses exist but rely on the same sparse data: Contrary Research notes the use of "regular aluminum magnets" and quotes CEO Kirtley on 85-95% efficiency, but cites no independent validation. A 2018 MITRE/JASON technical assessment identified the need for 40 Tesla fields for commercial viability versus 8 Tesla demonstrated in the then-current prototype (Trenta), a gap that remains partially closed (Polaris targets 15 T+, Orion targets higher).

**Key data gaps:**
- Achieved vs. target repetition rate on Polaris (1 Hz target stated, no public achievement data)
- Net electricity production from any prototype (never announced, though Polaris was originally targeted to demonstrate this in 2024)
- D-He3 fuel cycle operation (all fusion results to date use D-D or D-T; commercial D-He3 operation at ~200M°C remains undemonstrated)
- Cost structure and LCOE estimate from company or independent technical study

The data availability is **Limited** because while the approach and milestones are documented, the quantitative engineering parameters and economic data needed for first-principles LCOE modeling are largely absent from the public record.

## 2. Challenges in Capturing System Function

The unique architecture of Helion's pulsed FRC with direct conversion creates several modeling challenges that depart from both steady-state magnetic confinement and inertial confinement fusion:

### Challenge 1: Direct Conversion Efficiency is the Dominant Economic Lever (High Impact, High Uncertainty)

The claimed 85-95% direct electricity capture efficiency via inductive energy recovery is the single largest departure from all other fusion concepts. Traditional thermal cycles (Rankine, Brayton, sCO₂) cap at ~40-45% gross thermal efficiency, then subtract parasitic loads. Helion's direct conversion bypasses this entirely: expanding magnetized plasma induces current in surrounding aluminum coils via Faraday's law, analogous to regenerative braking in electric vehicles.

> "hot plasma expands and pushes back on the magnetic field around it. That push induces current in the coils"
> — helion-website-technology.md, §Energy Capture

This eliminates the turbine hall, steam generators, condensers, cooling towers, and the entire thermal power conversion island that dominates balance-of-plant cost in D-T tokamaks and IFE concepts. If the efficiency claim holds, LCOE drops dramatically. If direct conversion degrades to 50-60% due to resistive losses, plasma kinetic energy that doesn't couple to the field, or magnetic field leakage, the economic advantage evaporates.

The 2015 demonstration of ">95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs" (helion-prototype-generations.md, Grande prototype) validates the power electronics at subscale, but does not validate the plasma-to-field coupling efficiency at fusion-relevant temperatures and compression ratios. The claim that "as much as 90% of system energy ends up in the magnetic fields" suggests that most input energy is recoverable *if* the FRC retains high magnetization through compression and expansion, but this is an assumption, not a measured value from Polaris.

**Uncertainty range:** If direct conversion efficiency is 85-95%, the concept has a major cost advantage. If it is 50-70%, it loses its primary differentiator and becomes comparable to or worse than thermal-cycle approaches. The 1costingFE library does not yet allow setting concept-specific direct conversion efficiency (per analyst-patch-spec-anchors.md, §upstream_blocker), so current models use the library default for `INDUCTIVE_DEC`, which may not reflect Helion's claim.

### Challenge 2: Pulsed Operation Creates Capital Utilization and Per-Shot Cost Structures (High Impact, Shared with IFE/MIF)

Unlike steady-state tokamaks or stellarators that produce power continuously (modulo downtime), Helion's system produces energy in discrete millisecond-duration pulses. At 1 Hz, the capacitor banks discharge for ~100 microseconds, plasma forms/collides/compresses/expands over ~1-10 milliseconds, then the system recharges for the next pulse. The driver hardware (capacitor banks, coils, power electronics) is idle >99% of the time. This extreme capital underutilization is why repetition rate has such high LCOE leverage.

The economic structure resembles inertial fusion concepts (MagLIF, laser ICF) more than magnetic confinement: LCOE scales with (capital cost / shots per year) + (per-shot consumable cost × shots per year) + fixed O&M. Unlike laser ICF, Helion has no per-shot target fabrication cost in the traditional sense (no cryogenic capsules or laser targets), but the pulsed electromagnetic loading on coils, capacitors, and structural elements creates wear that may drive component replacement cycles not present in steady-state concepts.

**Uncertainty:** The transition from Trenta's "1 pulse per 10 minutes" (helion-prototype-generations.md) to Polaris's "1 Hz target" to commercial targets of "possibly 2 Hz to 10 Hz or even 60 Hz" (helion-website-technology.md, §Repetition Rate) represents a 600× to 3600× scaling in pulse frequency. No data on achieved repetition rate from Polaris has been released. The mechanical, thermal, and electrical stresses at 1+ Hz with GJ-scale energy throughput are not validated. Component fatigue under millions to billions of pulses per year is uncharacterized.

### Challenge 3: He3 Breeding from DD Side Reactions is Unproven at Scale (High Impact, Unique to Concept)

Helion's fuel strategy depends on breeding He3 on-site from deuterium-deuterium (DD) side reactions rather than sourcing external He3 (terrestrial He3 is extraordinarily scarce, ~$2000/g). The breeding pathway is:
- 50% of DD reactions produce He3 directly: D + D → He3 (0.82 MeV) + n (2.45 MeV)
- 50% of DD reactions produce tritium: D + D → T (1.01 MeV) + p (3.02 MeV)
- Tritium decays to He3 with 12.3-year half-life (5.5%/year)

> "D-He3 target commercial fuel cycle" assumes breeding from DD side reactions
> — helion-website-technology.md, §Fuel

This creates a startup problem: Orion must operate initially on DD fuel (or externally-sourced tritium for D-T, as Polaris currently does) while building up a He3 inventory. The system becomes self-sufficient over years as tritium decays. The tritium inventory management, tritium handling infrastructure, and the transition from DD-heavy operation to D-He3-dominant operation at commercial scale have not been demonstrated.

Commercial D-He3 fusion requires ~200 million degrees Celsius (versus 150M°C achieved with D-T in Polaris), introducing additional plasma physics risk. The claim that "only 5% of its energy in the form of fast neutrons" applies to pure D-He3, but during the breeding phase, DD reactions produce 2.45 MeV neutrons, and any residual D-T reactions produce 14.1 MeV neutrons. The neutron environment and shielding requirements are thus time-dependent and depend on fuel mix, adding modeling complexity.

### Challenge 4: Magnetic Field Scaling from 8T → 40T (Moderate Impact, Shared Physics/Engineering Risk)

The 2018 MITRE/JASON assessment identified 40 Tesla as required for commercial viability. Trenta demonstrated 8T, Polaris targets 15T+, and Orion must reach higher fields. Pulsed aluminum coils at 40T face:
- Resistive heating proportional to B² (Joule losses in non-superconducting coils)
- Magnetic pressure proportional to B² / (2μ₀) ≈ 640 MPa at 40T (requires robust structural support)
- Electromagnetic forces on coils during fast ramp-up and ramp-down
- Repetitive mechanical stress cycling at Hz rates

> "40 Tesla target (reactor)" versus "8 Tesla demonstrated"
> — analyst-patch-spec-anchors.md, §4. Technical risks

Aluminum's resistivity and mechanical properties under these conditions are well-characterized in pulsed magnet literature, but sustained operation at 40T and 1+ Hz for years is not demonstrated. The trade-off is that avoiding superconducting magnets eliminates cryogenics and the REBCO/Nb₃Sn supply chain, but imposes higher recirculating power for resistive losses.

### Challenge 5: FRC Plasma Stability During Compression (High Impact, Shared with General FRC Research)

The MITRE/JASON report flagged "whether they can simultaneously achieve sufficiently high compression while maintaining plasma stability" as the primary challenge. FRCs are known to suffer from tilt and rotational instabilities, particularly under strong compression. Helion's approach relies on:
- Colliding FRCs with opposite toroidal field directions to provide rotational stabilization during merging
- Adiabatic compression (fast relative to MHD timescales, slow relative to Alfvén transit time) to heat plasma to fusion conditions

The FRC community's empirical scaling (Kirtley & Milroy, J. Fusion Energy 2023) suggests confinement improves with plasma size and temperature, but the database is limited at high compression ratios. Polaris's achievement of 150M°C at >8T compression validates the concept at intermediate parameters but does not close the gap to 200M°C at 40T with D-He3 fuel.

**Ranked by LCOE impact:**
1. Direct conversion efficiency (85-95% vs. 50-70%) — determines whether concept has cost advantage
2. Repetition rate scaling (1 Hz → 10+ Hz) — determines capital utilization and plant throughput
3. He3 breeding and D-He3 fuel cycle validation — determines fuel cost and neutron environment
4. Magnetic field scaling to 40T — determines whether commercial operation is achievable
5. FRC plasma stability under high compression — determines whether target performance is accessible

All five challenges are interlinked: achieving 40T fields enables higher compression, which improves FRC stability and confinement, which allows D-He3 operation, which reduces neutron damage and enables efficient direct conversion at scale.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first):

### He3 Breeding and Fuel Cycle Management (TRL 2-3)

**Demonstrated:** Laboratory-scale tritium handling for D-T experiments in Polaris (regulatory approval obtained August 2024, helion-prototype-generations.md). DD fusion reactions produce tritium and He3 as byproducts (demonstrated in FRC literature). Tritium decay to He3 is well-characterized nuclear physics.

**On paper only:** Closed-loop He3 breeding at commercial scale where DD side reactions provide sufficient He3 inventory to sustain continuous D-He3 operation. Tritium extraction, storage, and decay management as a He3 production pathway. Transition from DD-dominant fuel mix during startup to D-He3-dominant steady-state operation.

**Missing at scale:** Industrial He3 separation from exhaust plasma, tritium inventory management and regulatory licensing for kg-scale tritium storage, and demonstration that breeding ratio can sustain plant operations without external He3 input (terrestrial He3 supply is negligible). The 12.3-year tritium half-life means He3 inventory builds slowly; startup requirements and inventory dynamics are uncharacterized.

### D-He3 Fusion at 200M°C+ in Pulsed FRC (TRL 3-4)

**Demonstrated:** D-T fusion in Polaris at 150 million degrees Celsius (13 keV ion temperature), confirming that pulsed FRC compression can reach fusion-relevant temperatures (helion-milestones-feb2026.md). DD fusion demonstrated in earlier prototypes. FRC plasma confinement and stability at compression ratios sufficient for >100M°C have been validated.

**On paper only:** D-He3 fusion at ~200M°C with sufficient confinement time and density to achieve net energy gain (Q > 5-10 range needed for commercial operation with high direct conversion efficiency). D-He3 requires higher temperatures than D-T due to higher Coulomb barrier. FRC confinement scaling to D-He3 temperatures is extrapolated from lower-temperature data.

**Missing at scale:** Sustained D-He3 operation in Polaris or Orion. Energy gain (Q) measurements at any fuel cycle (DD, D-T, or D-He3) have not been publicly released. Plasma-to-field energy coupling efficiency at fusion-relevant temperatures has not been validated—claimed 85-95% direct conversion efficiency remains unverified in peer-reviewed literature.

### Pulsed Electromagnetic Coils at 40 Tesla, Hz Repetition Rate (TRL 4-5)

**Demonstrated:** Pulsed aluminum coils at 4T (Grande, 2014), 7T (Venti, 2018), >8T (Trenta, 2021), and 15T+ target (Polaris). Modern high-voltage IGBTs demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses (Grande, 2015). Capacitor banks storing >50 MJ have been built and cycled. Coil systems use copper, aluminum, and custom alloys, with ~720 miles of coaxial cable in current prototypes (helion-website-technology.md).

**On paper only:** 40 Tesla operation at 1-10 Hz for years to decades. Fatigue life of aluminum coils under repetitive high-field pulsing (billions of cycles over plant lifetime). Resistive heating management and cooling systems for sustained high-duty-cycle operation. Structural reinforcement to withstand magnetic pressure (~640 MPa at 40T).

**Missing at scale:** Long-term reliability data for pulsed high-field electromagnets at Hz rates. Coil lifetime projections (replacement intervals, degradation mechanisms). Thermal management systems for continuous operation (Polaris has operated for months, but not at commercial pulse rates). The transition from 15T+ (Polaris) to 40T (Orion target) is a major engineering step with uncharacterized risks.

### Capacitor Bank and Pulsed Power Electronics (TRL 5-6)

**Demonstrated:** Thousands of high-voltage pulsed capacitors storing >50 MJ total energy (helion-website-technology.md). Energy recovery circuits using modern IGBTs with >95% efficiency demonstrated over 1 million pulses. Pulsed power at tens of kV and multi-MA currents for FRC formation and compression. Helion manufactures some capacitors in-house and sources others externally.

**On paper only:** Scaling to hundreds of MJ for commercial systems (Orion, and larger plants). Capacitor lifetime at 1-10 Hz for 30-year plant life (requires billions of charge-discharge cycles, far beyond demonstrated millions). Cost reduction to commodity levels via mass manufacturing. Supply chain at scale for capacitor and IGBT production to support fleet deployment.

**Missing at scale:** Capacitor degradation rates and replacement schedules at commercial duty cycles. Supply chain analysis for high-voltage capacitors at GW-scale fleet production rates. Cost-optimized designs that balance performance and cost (current prototypes optimize for R&D, not production cost).

### Direct Energy Conversion via Inductive Coils (TRL 4-5)

**Demonstrated:** Laboratory-scale direct magnetic energy recovery at >95% round-trip efficiency (Grande, helion-prototype-generations.md). FRC expansion against magnetic field is well-characterized in FRC physics literature. Faraday induction is textbook electromagnetics.

**On paper only:** Direct capture of fusion-born charged particle energy at 85-95% efficiency in a plant-scale system. Coupling between FRC plasma kinetic energy and magnetic field energy at compression ratios and temperatures needed for commercial D-He3 operation. Energy recovery circuits sized for hundreds of MW throughput with minimal losses.

**Missing at scale:** Validated measurements of direct conversion efficiency in fusion-producing shots. Proof that expanding fusion plasma retains sufficient magnetization to couple efficiently to coils. Thermal management for direct conversion hardware handling hundreds of MW pulsed power. The 85-95% efficiency claim is a projection, not a measured result from fusion experiments.

### Vacuum Vessel and Plasma-Facing Components (TRL 5-6)

**Demonstrated:** Seven generations of prototype vacuum vessels from Grande (2014) through Polaris (2025). Linear cylindrical geometry with electromagnetic coils surrounding the vessel. Polaris operates at 15T+ fields and 150M°C plasma temperatures. Vessels have survived thousands to tens of thousands of pulses in Trenta and Polaris.

**On paper only:** First-wall materials that survive 1-10 Hz pulsed operation for 30 years with D-He3 fuel (low but non-zero 2.45 MeV neutron flux from DD side reactions, plus thermal cycling and electromagnetic forces). Maintenance and replacement strategies for plasma-facing components. Remote handling requirements (if activated components need replacement).

**Missing at scale:** Component lifetime projections for pulsed electromagnetic and thermal loading at Hz rates. Materials selection for first wall and structural elements (neutron damage accumulation, fatigue under pulsed mechanical stress). Activation levels and waste characterization for decommissioning (lower than D-T due to aneutronic D-He3, but non-zero due to DD side reactions and material activation).

### Balance of Plant (Power Conditioning, Grid Integration) (TRL 6-7)

**Demonstrated:** No steam cycle required (direct conversion eliminates turbines, condensers, heat exchangers). Power conditioning electronics for pulsed DC power to grid AC at utility scale are mature technology (inverters, transformers). Helion's modular "shipping container sized" design concept (helion-website-technology.md) suggests transportable power electronics packages.

**On paper only:** Grid integration of pulsed power source with 1-10 Hz fundamental frequency. Power smoothing and buffering to deliver stable grid power from pulsed fusion output. Switchgear and transformers sized for Orion's 50 MWe output and larger commercial plants (500 MWe Nucor partnership announced).

**Missing at scale:** Demonstrated grid connection and power delivery from a fusion-producing prototype (Polaris is not grid-connected). Utility acceptance of non-traditional power plant architecture. Regulatory and interconnection approval processes for fusion plants (Washington State has passed legislation classifying fusion as distinct from fission, enabling permitting pathways).

## 4. Key Materials and Supply Chain Considerations

### Deuterium: Abundant, No Supply Constraint

Deuterium is extracted from water (D₂O, heavy water) at ~150 ppm natural abundance. Commercial deuterium production is established, with suppliers worldwide. A 50 MWe plant operating on D-D initially and D-He3 at steady-state requires kg-scale deuterium per year. No supply constraint or cost concern. Fuel cost is negligible compared to capital and O&M.

### Helium-3: Must Be Bred On-Site, No External Supply

Terrestrial He3 is extraordinarily scarce (~15 kg accumulated global inventory from tritium decay in nuclear weapons programs, with some consumed by neutron detector manufacturing and research). Lunar regolith mining has been proposed but is not a near-term source. Helion's entire fuel strategy depends on breeding He3 from DD side reactions:
- 50% direct: D + D → He3 + n
- 50% via tritium decay: D + D → T + p, then T → He3 (12.3-year half-life)

This eliminates external He3 sourcing as a supply chain constraint but imposes a startup phase where the plant operates on DD or D-T while building He3 inventory over years. Tritium handling and storage infrastructure is required. The breeding ratio must exceed consumption (analogous to tritium breeding ratio > 1 in D-T fusion) or the plant eventually starves of He3. This ratio has not been published or validated experimentally.

### Tritium: Startup Inventory Required, Regulatory Burden

Polaris currently uses externally-sourced tritium for D-T fusion experiments (regulatory approval obtained August 2024, helion-prototype-generations.md). Startup tritium inventory for Orion may be needed if DD-to-He3 breeding is too slow to reach commercial D-He3 operation. Global tritium supply is limited (~20-25 kg, primarily from CANDU heavy-water reactors), and existing fusion programs (ITER, private D-T tokamaks) compete for supply. Tritium's 12.3-year half-life means inventory decays at 5.5%/year, requiring continuous breeding or external resupply during the startup phase.

Tritium handling imposes regulatory requirements (radiation safety, containment, waste management) that Helion has begun addressing but will scale significantly for commercial plants. NRC or equivalent oversight for tritium facilities may add licensing cost and timeline risk.

### Aluminum, Copper, and Structural Metals: Commodity Materials, No Constraint

Helion's use of "regular aluminum magnets" and copper/aluminum coaxial cables (contrary-research-helion.md, helion-website-technology.md) avoids the superconducting magnet supply chain bottleneck facing tokamaks and stellarators (REBCO tape, Nb₃Sn, cryogenic infrastructure). Aluminum is produced globally at ~65 million tonnes/year. A single plant requires tonnes to tens of tonnes of aluminum for coils (vastly less than REBCO/Nb₃Sn requirements for equivalent-field superconducting coils). Copper for cables is similarly abundant.

This is a major supply chain advantage: no rare-earth elements, no exotic superconductors, no beryllium (unlike some tokamak blankets), no tungsten plasma-facing tiles (unlike tokamak divertors). Structural materials for the vacuum vessel are conventional (likely stainless steel or aluminum alloys).

**Trade-off:** Resistive losses in aluminum coils require continuous power input during pulses, reducing overall efficiency compared to superconducting coils (which have zero resistive loss). The recirculating power for coil resistive heating must be factored into net electric output.

### High-Voltage Capacitors: Specialty Component, Potential Bottleneck

Helion uses thousands of high-voltage pulsed capacitors (>50 MJ total storage, tens of kV rating, helion-website-technology.md). Some are manufactured in-house, others sourced externally (contrary-research-helion.md identifies supply chain as "main potential risk"). High-voltage capacitors for pulsed power are a specialty market, not commodity electronics. Scaling to fleet production (dozens to hundreds of plants) would require either:
- Major expansion of in-house capacitor manufacturing (capital-intensive, slow)
- Development of external suppliers at scale (currently low-volume market)

Capacitor lifetime at 1-10 Hz for billions of cycles is a known weak point of pulsed power systems. Dielectric breakdown, electrode erosion, and capacitance degradation over time are industry-wide challenges. Replacement intervals and costs for capacitor banks in a commercial plant are uncharacterized but could be a significant operating cost (analogous to blanket replacement in D-T tokamaks).

### Boron and Concrete for Neutron Shielding: Standard Materials, Adequate Supply

Helion's neutron shielding uses "borated polyethylene and borated concrete" (helion-website-technology.md), analogous to hospital particle beam shielding. This is much simpler and cheaper than D-T fusion blanket/shield systems (which must breed tritium and withstand 14.1 MeV neutrons). Boron-10 is a stable isotope used in neutron shielding and control rods; supply is adequate. Shielding thickness is cited as "approximately one meter" solid barrier, much less than D-T reactor shielding (typically 1-2 meters of blanket/shield plus biological shielding).

The reduced neutron flux (5% of energy output, per Helion claim, vs. 80% for D-T) and lower neutron energy (2.45 MeV from DD side reactions vs. 14.1 MeV from D-T) reduce shielding mass and cost. This is a materials and supply chain advantage relative to D-T concepts.

### IGBTs and Power Electronics: Mature Technology, Established Supply Chain

Modern high-voltage IGBTs (Insulated Gate Bipolar Transistors) for energy recovery circuits are mature industrial components, used in motor drives, HVDC transmission, and power conditioning. Helion's >95% round-trip efficiency demonstration (Grande, 2015) used off-the-shelf IGBTs. Supply chain is established; manufacturers include Infineon, ABB, Mitsubishi Electric. Scaling to plant-level power throughput (hundreds of MW) is within demonstrated capability of existing industrial products. No supply constraint or technical bottleneck identified.

**Summary of supply chain priorities:**
- **Highest risk:** High-voltage capacitor supply at scale (specialty component, potential bottleneck)
- **Moderate risk:** He3 breeding must work (no external supply, unproven at scale)
- **Low risk:** Aluminum, copper, deuterium, shielding materials (all commodity or abundant)
- **Advantage:** No superconductor supply chain constraint (REBCO, Nb₃Sn, cryogenics)

## 5. Design Point Parameters

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 50 MWe | helion-prototype-generations.md §Orion; helion-website-technology.md §Power Output | high | Orion design point, Microsoft PPA target 2028; drives `P_native` (and module count at 1 GWe comparison) |
| p_input_MW | [inferred: ~12.5 MW, assumes Q_eng=4.0] | analyst-patch-spec-anchors.md §Verified spec values; derived from P_out / Q_eng | low | Auxiliary power for capacitor charging, coil resistive losses; Q_eng=4.0 is inferred from net gain requirement, not directly stated; spec key: `p_input` |
| q_eng (engineering Q) | [inferred: 4.0] | analyst-patch-spec-anchors.md — "Inferred from need for net gain after recirculating power; consistent with Helion's published Q claims for Orion-class" | low | Net fusion gain after recirculating power for coils and energy recovery inefficiencies; not a published value from company |
| fuel_cycle | D-He3 (with DD side reactions for He3 breeding) | helion-website-technology.md §Fuel; helion-milestones-feb2026.md | high | Commercial target fuel; Polaris currently operating on D-D and D-T as intermediate steps; ~200M°C required for D-He3; spec key: `fuel` (enum) |
| repetition_rate_Hz | [inferred: 1.5 Hz, range 1-2 Hz] | analyst-patch-spec-anchors.md §Verified spec values; helion-website-technology.md §Repetition Rate; docslib-helion-arpa-e-presentation.md | medium | Polaris target 1 Hz; ARPA-E presentation shows 2 Hz @ 50 MW design point; actual achieved rate not publicly disclosed; spec key: `f_rep` |
| fusion_power_MW | [inferred: ~62 MW, back-solved from 50 MWe / 0.90 direct conversion efficiency + p_input] | derived from net electric + direct conversion efficiency + recirculating power | low | Informational only — `p_fus` is back-solved by library from `p_input` + `P_native`; do NOT put `p_fus` in spec |
| direct_conversion_efficiency | [claimed: 85-95%] | helion-website-technology.md §Energy Capture; contrary-research-helion.md | low | Inductive direct energy conversion via Faraday's law; validated at subscale (>95% round-trip on Grande) but not at fusion-scale; NOT settable in 1costingFE spec (library default for `INDUCTIVE_DEC` enum used) |
| magnetic_field_compression_T | 15 T+ (Polaris), 40 T target (Orion/commercial) | helion-prototype-generations.md §Polaris; analyst-patch-spec-anchors.md §Technical risks; docslib-helion-arpa-e-presentation.md | medium | Pulsed electromagnetic coil peak field during compression; 8T demonstrated (Trenta), 15T+ target (Polaris), 40T required for commercial viability per MITRE/JASON; spec key: `B` (on-axis field, though FRC geometry complicates "on-axis" definition) |
| ion_temperature_keV | 13 keV (150M°C, D-T in Polaris); ~17 keV (200M°C target for D-He3) | helion-milestones-feb2026.md §Fusion Milestones; helion-website-technology.md §Fuel | high (for 13 keV), medium (for 17 keV target) | Achieved with D-T; D-He3 requires higher temperature due to Coulomb barrier |
| FRC_formation_velocity_km_s | >300 km/s | helion-website-technology.md §Technology; docslib-helion-arpa-e-presentation.md | medium | FRC plasmoid acceleration velocity before collision; kinetic energy converts to thermal during merging |
| plasma_density_m3 | [target: 1E23 m⁻³ post-compression] | docslib-helion-arpa-e-presentation.md §Plasma Parameters; formation density ~1E21 m⁻³ | low | 100× compression from formation (1E21) to fusion (1E23); not validated in published data |
| machine_length_m | [estimated: ~30-40 m for Orion, based on 2× Polaris] | helion-prototype-generations.md §Orion — "Expected to be twice the size of Polaris"; Polaris ~60 ft (18m) | low | Linear cylindrical geometry; detailed dimensions not disclosed; spec key: `plasma_t` (if applicable to FRC geometry) |
| capacitor_bank_energy_MJ | >50 MJ (Polaris) | helion-website-technology.md §Capacitor Bank | medium | Stored energy for coil pulsing; Orion/commercial likely higher (hundreds of MJ); drives capital cost of pulsed power system |
| coil_cable_length_km | ~1160 km (~720 miles) | helion-website-technology.md §Magnets/Coils | medium | Total coaxial cable length in Polaris prototype; copper, aluminum, custom alloys |
| neutron_energy_fraction | [claimed: 5% for D-He3] | helion-website-technology.md §Fuel — "only 5% of its energy in the form of fast neutrons" | medium | Lower than typical D-He3 models (~10% from DD side reactions); depends on fuel mix and reaction rate ratios |
| shielding_thickness_m | ~1 m | helion-website-technology.md §Neutron Management | medium | Borated polyethylene and borated concrete; much thinner than D-T blanket/shield (1-2 m) |

**Notes on spec keys and 1costingFE library constraints:**
- `P_native` = 50 MWe is the primary driving parameter; all other values support this headline
- `p_input` and `q_eng` are inferred from net electric requirement and must be self-consistent
- `p_fus` (fusion power) is computed by library from `p_input` and `P_native`; do NOT include in spec
- Direct conversion efficiency (85-95% claimed) is NOT settable via spec — library uses `PulsedConversion.INDUCTIVE_DEC` enum with embedded efficiency; this is a modeling limitation (analyst-patch-spec-anchors.md, §upstream_blocker)
- FRC geometry parameters (R0, plasma_t, elongation) are not applicable or not disclosed; library's `PULSED_FRC` class encodes Helion-class geometry defaults

## 5b. Override Candidates

The canonical account schema for this archetype includes 15 accounts. I walk each one against the dossier to discover override candidates:

### Per-Account Walkthrough

**C220101 (First wall, blanket & neutron multiplier):** D-He3 aneutronic fuel produces ~5% neutron energy fraction (helion-website-technology.md) versus ~80% for D-T. Neutron wall loading is dramatically lower. However, no company-published blanket cost, first-wall material specification, or replacement interval exists in the dossier. The library's default for aneutronic/low-neutron concepts is a reduced blanket cost. **No override candidate** — no company-grounded figure.

**C220102 (Radiation shield):** Shielding uses borated polyethylene and borated concrete, ~1 m thickness (helion-website-technology.md). Simpler and cheaper than D-T shields (no tritium breeding, lower neutron energy). However, no published cost figure or detailed shielding mass/volume specification. **No override candidate** — no company-grounded figure.

**C220103 (Confinement magnets / coils):** Pulsed aluminum electromagnets, not superconducting. Polaris uses ~1160 km (~720 miles) of coaxial cable (copper, aluminum, custom alloys). The library default prices HTS-REBCO conductor at ~$44k/kg (from ARC tokamak). Helion's aluminum coils are fundamentally different: commodity metal, no cryogenics, but higher resistive losses and structural reinforcement for 40T pulsed fields. No published cost per kg of aluminum coil assembly or total coil system cost. **Candidate for relative override** if we had a grounded unit cost, but **no direct company figure in dossier** → no override proposed in this iteration.

**C220104 (Supplementary plasma heating or primary pulsed driver):** This account costs "primary pulsed driver (laser/accelerator/gun) on $/J of driver energy." Helion's driver is the capacitor bank (>50 MJ, helion-website-technology.md). No published cost for capacitor banks or $/J figure. The ARPA-E presentation cites an input efficiency target of <$0.03/MJ, but this is an operational cost target, not a capital cost. **No override candidate** — no company-grounded figure for capacitor bank capital cost.

**C220105 (Primary structure):** Conventional structural materials (likely steel or aluminum, based on coil materials). No published cost or mass specification. **No override candidate**.

**C220106 (Vacuum system):** Linear cylindrical vessel, electromagnetic coils external to vacuum. No published vacuum system cost. **No override candidate**.

**C220107 (Power supplies or pulsed-power capacitor bank on $/J stored):** This is the account for "pulsed-power capacitor bank ($/J stored)." Helion uses thousands of high-voltage capacitors, >50 MJ total (helion-website-technology.md). Some built in-house, some external (contrary-research-helion.md). No published $/J cost. Contrary Research identifies supply chain as "main potential risk," suggesting high cost or limited supply at scale. **No override candidate** — no company-grounded figure, though this is a critical cost driver.

**C220109 (Direct energy converter):** Helion's inductive direct conversion uses the same aluminum coils for compression and energy recovery (helion-website-technology.md: "Direct inductive energy recovery via Faraday's law"). The hardware is the coil system itself plus power electronics (IGBTs for >95% round-trip efficiency, Grande demonstration). No published cost for direct energy conversion subsystem separate from coils. **No override candidate** — covered by coil cost in C220103 and power electronics in C220107; no separate company figure for DEC-specific hardware.

**C220110 (Remote handling & maintenance equipment):** No published maintenance strategy, remote handling requirement, or equipment cost. Pulsed operation and low neutron activation (relative to D-T) may reduce remote handling needs, but this is speculative. **No override candidate**.

**C220111 (Reactor-equipment installation & assembly):** Helion's modular "shipping container sized" design philosophy (helion-website-technology.md) suggests factory assembly, potentially reducing on-site construction cost. No published figure. **No override candidate** — though a relative override <1.0 could be justified by factory assembly if we had grounding; absent that, no override.

**CAS21 (Buildings & site structures):** No published building cost or footprint data. Elimination of turbine hall (no steam cycle) reduces building size relative to thermal-cycle plants. Washington State permitting advantages (fusion classified as distinct from fission, House Bill 1018, helion-prototype-generations.md) may reduce regulatory cost. **No override candidate** — no company-grounded figure.

**CAS23 (Turbine plant equipment):** Direct conversion eliminates the steam cycle entirely (helion-website-technology.md: "No steam cycle required"). The library should automatically set this to zero for direct-conversion concepts. **Proposed override: 0.0** (absolute), **provenance: direct**, **enabled: true**.

**CAS24 (Electric plant equipment):** Standard switchyard, transformers, grid connection. Pulsed DC-to-AC conversion via power electronics (mature technology). No published cost. **No override candidate** — library default stands.

**CAS26 (Heat rejection system):** Direct conversion eliminates condenser cooling (no steam cycle). Resistive heating in aluminum coils and power electronics still requires cooling, but much less than a thermal plant. No published cooling system cost. **No override candidate** — though a relative override <1.0 is plausible; absent company data, no override.

**CAS27 (Special materials):** No published reactor material inventory cost (e.g., initial FLiBe fill, if used, or other blanket materials). **No override candidate**.

**CAS70 (Annualized O&M + scheduled component replacement):** Taught but NOT overridable today (no-op per 1costingFE issue #106). The dossier provides no O&M cost breakdown anyway. **No override possible** — tool limitation.

**CAS80 (Annualized fuel cost):** Taught but NOT overridable today. Deuterium fuel cost is negligible (commodity). He3 breeding eliminates external He3 sourcing (terrestrial He3 is ~$2000/g, but Helion doesn't buy it). **No override possible** — tool limitation.

### Override Registry

After the per-account walkthrough, only **one** account has sufficient company-grounded data to justify an override:

```yaml
overrides:
  - account: CAS23
    value: 0.0
    enabled: true
    provenance: direct
    source: "helion-website-technology.md §Energy Capture"
    rationale: |
      Direct inductive energy conversion via Faraday's law eliminates the steam cycle entirely.
      No turbines, condensers, steam generators, or heat exchangers are required. The library's
      thermal cycle cost (CAS23) does not apply to this concept. This is a direct architectural
      fact, not a cost estimate — the subsystem does not exist.
```

**Override count sanity-check:** Expected band for low archetype-fit is 6-12 enabled overrides. Actual count: **1 enabled override**. This falls well below the band. The discrepancy reflects the data gap: Helion has not published subsystem-level cost breakdowns, unit costs, or dollar figures for any CAS22 reactor-island account. The sole override (CAS23 = 0) is an architectural elimination, not a cost figure. A fully-grounded analysis would likely add overrides for:
- C220103 (coils) — if Helion published aluminum coil cost vs. library's HTS-REBCO pricing
- C220107 (capacitor banks) — if Helion published $/J for pulsed power system
- C220109 (direct converter) — if Helion published DEC subsystem cost separate from coils
- CAS21 (buildings) — if factory-assembly cost data or building footprint reduction factor were published
- CAS26 (heat rejection) — if cooling system cost for direct-conversion plant were published

Absent those data, the override registry remains sparse. The low count is evidence of limited public disclosure, not evidence that the concept matches library defaults.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Direct conversion efficiency at fusion-scale (claimed 85-95%, validated only at subscale >95% round-trip on Grande without fusion plasma) | S2, S3 | not-yet-sourced | blocking | Peer-reviewed measurement of plasma-to-field coupling efficiency during fusion shots on Polaris; or engineering report quantifying losses (resistive, magnetic leakage, kinetic energy not coupled to field) |
| 2 | Achieved repetition rate on Polaris (1 Hz target stated, no public achievement data) | S1, S2 | proprietary | blocking | Company disclosure of Polaris operational pulse rate over sustained periods (hours to months), failure modes, and pacing constraints (chamber clearing, capacitor recharge, coil thermal recovery) |
| 3 | Engineering Q (fusion gain) for any prototype (Polaris, Trenta, earlier); net energy balance never published | S1, S2, S5 | proprietary | blocking | Q = (fusion energy out) / (auxiliary energy in); required to validate q_eng=4.0 assumption and assess proximity to commercial breakeven |
| 4 | D-He3 fuel cycle operation and He3 breeding validation (all fusion results to date use D-D or D-T) | S1, S2, S3, S5 | not-yet-sourced | blocking | Demonstration of D-He3 fusion in Polaris or Orion, tritium-to-He3 breeding ratio measurements, He3 inventory buildup rate, and startup fuel mix transition plan |
| 5 | Magnetic field scaling 15T+ (Polaris) → 40T (commercial) and coil lifetime under pulsed loading at Hz rates | S2, S3, S4 | not-yet-sourced | important | Engineering study of 40T pulsed aluminum coil design (structural reinforcement, resistive heating, fatigue life over billions of cycles), or demonstration of 40T fields in a test rig |
| 6 | Capacitor bank capital cost ($/J) and lifetime at 1-10 Hz duty cycle | S4, S5b | proprietary | important | Bottom-up cost estimate for high-voltage capacitor system at commercial scale (hundreds of MJ), replacement intervals, and degradation mechanisms; or reference to analogous pulsed power systems (e.g., Z machine upgrades, LTD bricks for MagLIF) |
| 7 | Subsystem-level cost breakdown (coils, capacitors, vacuum vessel, power electronics, buildings, direct converter hardware, etc.) | S1, S5b | proprietary | important | Engineering cost estimate or bottom-up BOM for Orion, or analogous cost study (like ARC for tokamaks, Z-IFE for MagLIF) |
| 8 | First-wall and structural materials specification, component lifetimes under pulsed EM and thermal loading | S3, S4 | not-yet-sourced | important | Materials selection report for plasma-facing and structural components, neutron damage projections (DD side-reaction neutrons + activation), fatigue life under Hz-rate pulsing, and replacement schedules |
| 9 | Plasma stability and confinement scaling to D-He3 temperatures (~200M°C / 17 keV) with high compression ratios | S2, S3 | not-yet-sourced | important | Peer-reviewed FRC confinement scaling data at D-He3-relevant parameters, or demonstration of >15 keV ion temperatures in Polaris FRC with confinement time sufficient for fusion |
| 10 | Tritium inventory management, regulatory licensing, and transition timeline from DD/D-T startup to D-He3 steady-state | S3, S4 | not-yet-sourced | nice-to-have | Tritium handling system design, storage capacity, decay-to-He3 inventory model, NRC/equivalent licensing requirements for kg-scale tritium, and startup fuel cycle timeline (years to reach He3 self-sufficiency) |
| 11 | LCOE estimate or target from company or independent study | S1 | proprietary | nice-to-have | Published LCOE projection for Orion or commercial plants, with stated assumptions (capacity factor, capital cost, O&M, fuel cost, discount rate) |
| 12 | Heat rejection and thermal management system for resistive coil losses and power electronics at continuous 1-10 Hz operation | S3, S4 | not-yet-sourced | nice-to-have | Cooling system design for aluminum coils (likely water-cooled, but not specified), heat load calculations, and cooling power requirements; impacts net electric output via parasitic load |

**Gap summary:** The most critical gaps are **direct conversion efficiency validation** (determines whether concept has cost advantage), **achieved repetition rate** (determines capital utilization and throughput), **Q values** (determines proximity to net energy), and **D-He3 fuel cycle demonstration** (determines whether commercial operation is feasible). These are all blocking for first-principles LCOE modeling. The subsystem cost breakdown (gap #7) is critical for grounded override discovery but is proprietary. Gaps #1-4 are the minimum data set needed to assess commercial viability.

## 7. Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

Helion's pulsed FRC with inductive direct energy conversion has no close analogue in the current concept landscape. The nearest neighbors by confinement family would be other MIF concepts (MagLIF, General Fusion's pneumatic compression), but those use magnetized target fusion with thermal power conversion, not direct conversion. TAE Technologies' beam-driven steady-state FRC (C-2W/Norman) shares the FRC topology but is steady-state with auxiliary heating, not pulsed compression. Laser ICF and heavy-ion ICF are pulsed but use inertial confinement and (typically) thermal cycles, not magnetic confinement with direct conversion.

The unique deltas that would define a comparison, were a comparable available:
- **Direct conversion vs. thermal cycle:** Helion's 85-95% claimed efficiency vs. ~40-45% for Rankine/Brayton cycles eliminates CAS23 (turbine plant equipment) and most of CAS26 (heat rejection), a major cost reduction if the efficiency claim holds.
- **Pulsed aluminum coils vs. superconducting magnets:** Eliminates REBCO/Nb₃Sn supply chain, cryogenics (CAS22 cryoplant), and magnet capital cost typical of tokamaks/stellarators; trades for higher recirculating power (resistive losses) and pulsed power electronics (capacitor banks, C220107).
- **D-He3 fuel vs. D-T:** Reduces neutron wall loading (~5% vs. ~80%), eliminates tritium breeding blanket (simplified C220101), reduces shielding (C220102), and reduces activation/waste (affects O&M and decommissioning, CAS70/CAS90); trades for higher temperature requirement (~200M°C vs. ~150M°C) and unproven He3 breeding pathway.
- **Pulsed operation vs. steady-state:** Introduces repetition rate as a first-order economic parameter (capital utilization scales with Hz), capacitor bank and power electronics as major cost drivers (C220107), and potential per-shot consumable costs (coil fatigue, capacitor degradation) analogous to IFE target costs; no direct analogue in steady-state magnetic confinement.

In a future iteration where comparable MIF or pulsed concepts are analyzed (e.g., MagLIF with IMG driver, or a pulsed Z-pinch with inductive energy recovery), the family-delta would articulate these deltas quantitatively, measuring the cost impact of direct conversion efficiency, coil type, and fuel choice against the comparable's baseline.

## 8. Sources

Listed in order of importance to this analysis:

1. **helion-website-technology.md** — Helion Energy website technical overview (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/). Primary source for system architecture: direct inductive energy conversion via Faraday's law, pulsed aluminum electromagnets, capacitor banks (>50 MJ), coaxial cables (~720 miles / 1160 km), D-He3 fuel cycle with He3 breeding from DD side reactions, 1 Hz repetition rate target, 50 MWe Orion design point, and elimination of steam cycle. Sections: §Technology, §Energy Capture, §Fuel, §Magnets/Coils, §Capacitor Bank, §Repetition Rate, §Power Output, §Neutron Management.

2. **helion-prototype-generations.md** — Wikipedia article on Helion Energy prototypes (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/). Comprehensive prototype progression: Grande (2014, 4T, >95% energy recovery demonstrated), Venti (2018, 7T), Trenta (2021, >8T, 10,000 pulses, 16-month continuous operation), Polaris (2025, 15T+ target, D-T fusion at 150M°C achieved February 2026), Orion (under construction, 50 MWe, 2028 target, Microsoft PPA). Also: 2018 MITRE/JASON technical assessment (40T commercial field requirement, plasma stability challenge), IPA experimental heritage (2005-2012, MSNW/UW), Washington State regulatory framework (fusion classified as distinct from fission, enabling permitting). Sections: §Overview table, §Technology, §Fuel, §Criticism, prototypes 1-8.

3. **helion-milestones-feb2026.md** — Helion Energy press release (February 2026) announcing D-T fusion achievement in Polaris (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/). Confirms 150 million degrees Celsius (13 keV) ion temperature, validation by Dr. Alan Hoffman (PPPL), and progression from D-D to D-T to D-He3 fuel cycles as part of Polaris testing program. Orion construction site in Malaga, WA confirmed. Sections: §Fusion Milestones, §About Helion.

4. **analyst-patch-spec-anchors.md** — Internal analyst-derived specification document (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-03/sources/). Provides modeling parameters for 1costingFE library: P_native=50 MWe, q_eng=4.0 (inferred), f_rep=1.5 Hz (midpoint of 1-2 Hz range), architectural mapping to `ConfinementConcept.PULSED_FRC` and `PulsedConversion.INDUCTIVE_DEC`, and critical note that direct conversion efficiency (85-95% claimed) is NOT settable via spec — requires upstream library changes. Identifies data gaps: limited published geometry, efficiency validation, Q values. Sections: §Verified spec values, §Architectural mapping, §What NOT to set, §upstream_blocker.

5. **docslib-helion-arpa-e-presentation.md** — Helion ARPA-E project presentation (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/). Technical performance targets: 50 MW at 2 Hz repetition rate, 40 Tesla reactor field goal, input efficiency target <$0.03/MJ, plasma density 1E23 m⁻³ post-compression (vs. 1E21 m⁻³ formation), FRC velocity >300 km/s, ion temperature 8+ keV, and magnetic energy recovery efficiency η=0.7. Also: high shot rate capability (2000 shots/month vs. NIF's 20). Sections: §Power and Repetition, §Magnetic Fields, §Plasma Parameters, §Energy Efficiency, §Neutron Diagnostics.

6. **contrary-research-helion.md** — Contrary Research company profile (accessed via knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/). Confirms "regular aluminum magnets" (quote from CEO Kirtley), 85-95% direct electricity capture efficiency, 95% energy recovery requirement per pulse, Microsoft PPA 50 MW 2028 with "significant monetary penalties" for non-delivery, in-house manufacturing of quartz tubes and high-voltage capacitors, and supply chain identified as "main potential risk." Also: one-meter solid neutron shield, repetition rate progression from 10-minute pulses (Trenta) to "every few seconds" (commercial target). Sections: §Key Technical Details, §Power Output, §Energy Recovery, §Magnet Materials, §Neutron Management, §In-House Manufacturing.

7. **Kirtley & Milroy, Journal of Fusion Energy (2023)** — Peer-reviewed paper on FRC scaling (cited in helion-prototype-generations.md and dossier.md). FRC confinement scaling relations and merging/compression physics. Not directly accessed in this analysis but cited as primary academic reference.

8. **Slough et al., Nuclear Fusion 51(5), 2011** — Peer-reviewed paper on merging and compression of FRC plasmoids (cited in helion-prototype-generations.md and dossier.md). Experimental results from IPA program at MSNW/University of Washington. Not directly accessed but cited as heritage for colliding FRC technique.

9. **MITRE/JASON technical assessment (2018)** — Independent review identifying 40 Tesla field requirement for commercial viability, 8 Tesla demonstrated capability (Trenta), and plasma stability during compression as primary technical challenge (cited in helion-prototype-generations.md, §Criticism). Original report not accessed; findings summarized via Wikipedia article.

**Source quality note:** Helion's public materials (website, press releases) are detailed on approach and milestones but opaque on cost, Q values, and subsystem specifications. Peer-reviewed literature (Kirtley, Slough) validates FRC physics but does not address Helion's commercial design. No independent power plant study (analogous to ARIES for tokamaks) exists. The analysis relies heavily on company statements, with limited third-party validation for key claims (85-95% efficiency, Q values, repetition rate achievements).
