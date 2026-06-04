---
ID: 38-particle-accelerator-driven-fusion
Concept: Particle Accelerator-Driven Fusion (SHINE-style)
Company: SHINE Technologies
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: OTHER
Archetype:
Archetype-Fit: None
Comparison-Status: freeform-deferred
Comparables: []
---

## Design Point

(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)

---

## 1. Availability of Data

**Rating: Rich (for neutron source applications) / Not Applicable (for power generation)**

SHINE Technologies has extensive public documentation of their operational neutron source systems, including their FLARE (Fusion Linear Accelerator for Radiation Effects) system and medical isotope production facilities. The company has published technical descriptions of their beam-on-target approach, operational milestones, and commercial deployment status for medical isotopes (Mo-99, Lu-177) and materials testing applications.

However, **SHINE Technologies is not pursuing fusion power generation**. Their technology is a continuous D-T fusion neutron source in which a deuterium ion beam (electrostatically accelerated to ~300 kV) strikes a tritium gas target, producing 14.1 MeV neutrons at rates up to 5 × 10^13 reactions/second. These neutrons drive subcritical LEU fission for medical isotope production or serve as radiation sources for industrial testing — neutrons are the product, not a byproduct of electricity generation.

The available sources include:
- SHINE corporate website materials (shinefusion.com) describing FLARE and operational systems
- Press releases on partnerships (UKAEA LIBRTI) and facility expansions
- Technical conference papers on neutron source specifications
- NRC licensing documentation for isotope production facilities

**Critical gap**: There are no published design studies, performance targets, capital cost estimates, or LCOE projections for a SHINE-based fusion power plant. The company's four-phase roadmap lists fusion power as "Phase 4" — a long-horizon objective with no publicly disclosed engineering parameters. Per the extracted dossier: *"No public commercial fusion-power-plant parameters (accelerator energy, beam current, net electric power, capital cost, LCOE) — Phase 4 is not yet engineered (gap — truly-unknown / long-horizon)."*

---

## 2. Challenges in Capturing System Function

The primary challenge is that **this concept is not designed to capture system function as a power plant**. Beam-target fusion systems face fundamental physics limitations that make them unsuitable for net-positive electricity generation:

**1. Intrinsically sub-unity Q**: Beam-target fusion operates far from breakeven. The electrostatic acceleration of deuterium ions to ~300 kV delivers a mono-energetic beam that undergoes fusion reactions with the tritium gas target. However:
- Beam ions that miss the target or scatter elastically deposit their energy as heat without producing fusion
- Fusion cross-sections are maximized at center-of-mass energies (~100 keV for D-T), but beam energies must be higher to penetrate the target, leading to inefficient energy coupling
- Even with perfect beam-target overlap, the fusion power output is orders of magnitude below the beam power input
- Q_scientific for beam-target systems is typically 10^-6 to 10^-3 (fusion power / beam power)

**2. No confinement**: Unlike plasma confinement concepts (magnetic or inertial), beam-target fusion has no mechanism to confine reacting ions long enough to achieve multiple collisions or to thermalize the fusion products for energy multiplication. Each ion gets at most one chance to fuse.

**3. Cooling dominates**: The beam deposits its energy primarily as heat in the target and surrounding structures. Removing this heat requires significant auxiliary power, further degrading net energy balance.

**4. Tritium consumption without breeding**: SHINE's operational systems consume tritium purchased from external suppliers (primarily CANDU reactor byproduct). There is no breeding blanket, no neutron multiplier, and no tritium self-sufficiency. Extending this approach to a power plant would require adding all the tritium fuel cycle infrastructure of a conventional D-T fusion reactor (blanket, extraction, purification, storage) while still operating at Q << 1.

**5. Absence of a thermal cycle**: SHINE's neutron sources have no power conversion system. They are not designed to capture the kinetic energy of fusion products or neutrons for electricity generation. Adding a thermal cycle (blanket → coolant → heat exchanger → turbine) would introduce capital costs and efficiency losses with no pathway to overcoming the fundamental Q < 1 physics.

These challenges are not engineering problems to be solved — they are intrinsic to the beam-target approach. SHINE's operational success as a neutron source does not translate to viability as a power generator.

---

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity. Since SHINE is a neutron source (not a power plant), this section assesses maturity relative to neutron source applications, not power generation.

### Fusion power conversion (TRL 1-2) — **Missing entirely**
- **Demonstrated**: Nothing. SHINE's systems have no thermal cycle, no blanket, no turbines, no heat exchangers designed for energy capture.
- **On paper only**: No published studies of SHINE-style beam-target fusion adapted for electricity generation. The physics barriers (Q << 1) are widely understood; no serious engineering effort exists to overcome them.
- **Missing at scale**: Everything. Blanket design, tritium breeding, power conversion, net energy balance.

### Tritium breeding and fuel cycle (TRL 1) — **Not designed for**
- **Demonstrated**: SHINE operates open-loop: tritium is purchased externally, consumed in the target, and the products are managed as waste. No breeding, no closed fuel cycle.
- **On paper only**: No SHINE-specific breeding blanket concept exists. Adapting D-T fusion blanket technology from other concepts would be necessary but insufficient (the Q << 1 problem remains).
- **Missing at scale**: Breeding blanket, tritium extraction from blanket, tritium self-sufficiency.

### Particle accelerator and beam delivery (TRL 8-9) — **Commercially operational**
- **Demonstrated**: SHINE operates multiple beam-on-target neutron sources commercially. Accelerators deliver deuterium ion beams at up to ~300 kV with sufficient beam current to produce 5 × 10^13 D-T fusions/second. Systems are licensed by the NRC and used for FDA-approved medical isotope production (Mo-99 for Tc-99m imaging). FLARE (Fusion Linear Accelerator for Radiation Effects) is operational for materials testing and is contracted to UKAEA for LIBRTI (Lithium Blanket Radiation Testing Initiative).
- **On paper only**: Higher beam energies, higher beam currents, and optimized target geometries could increase neutron yield, but these would not change the fundamental Q < 1 limitation.
- **Missing at scale**: Nothing — for neutron source applications. For power generation: everything, because no amount of beam current or target optimization can reach Q >> 1 in a beam-target geometry.

### Target chamber and tritium handling (TRL 7-8) — **Operational for neutron source duty**
- **Demonstrated**: SHINE handles tritium gas targets safely under NRC oversight. Target chambers manage the neutron flux, heat load, and activation from continuous D-T fusion. Tritium accountability and containment meet regulatory standards for industrial operations.
- **On paper only**: Scaling to higher beam powers or neutron yields is straightforward for neutron source applications.
- **Missing at scale**: Breeding blanket integration, first-wall heat loads at fusion-power-plant scales, neutron damage management over decades of operation (SHINE's duty cycles are lower than a power plant's).

---

## 4. Key Materials and Supply Chain Considerations

Since this is a neutron source (not a power plant), materials and supply chain are assessed for neutron source applications.

**Tritium supply** (externally sourced):
- Global tritium supply is ~25-30 kg, primarily from CANDU heavy-water reactors as a byproduct of fission. Supply is limited and decaying (5.5% per year).
- SHINE's neutron sources consume tritium at rates far below the 55+ kg/year a commercial D-T fusion power plant would require. Isotope production and materials testing applications are economically viable at current tritium prices (~$30,000/gram) because neutrons are the high-value product.
- For power generation: beam-target fusion's Q << 1 means tritium consumption vastly exceeds energy output. At current tritium prices, fuel costs alone would render electricity generation economically absurd (even ignoring all other costs). Tritium breeding would be required, but the physics of beam-target fusion provides no pathway to Q >> 1 even with a breeding blanket.

**Deuterium** (commodity):
- Deuterium is extracted from natural water (150 ppm abundance) and is commercially available at ~$1,000-3,000/kg. Supply is effectively unlimited for fusion applications at any scale.

**LEU (Low-Enriched Uranium)** (for isotope production only):
- SHINE's medical isotope production uses neutrons to drive subcritical fission in an LEU aqueous solution. This is specific to isotope production and is not relevant to fusion power concepts.

**Accelerator components** (no supply chain constraints):
- Electrostatic accelerators use conventional materials (metals, ceramics, vacuum hardware). No exotic materials or bottlenecks. Components are industrially mature and commercially available.

**No breeding blanket materials** (not designed for):
- SHINE's systems have no blanket, no neutron multiplier (Be), no lithium-bearing breeder materials (Li6, FLiBe, LiPb), no structural materials for high-fluence neutron environments (RAFM steels, SiC composites). These would all be required to adapt beam-target fusion to power generation, but their addition would not overcome the Q << 1 fundamental barrier.

---

## 5. Design Point Parameters

**Not applicable — SHINE Technologies does not have a fusion power plant design.**

The following table captures the available parameters for SHINE's operational neutron source systems. These parameters describe a **neutron source**, not a power-generating reactor. There is no net electric output, no LCOE, no Q_eng, no thermal cycle.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **System type** | Beam-on-target D-T neutron source | shine-technology-overview.md | high | Not a confinement concept; not a power reactor |
| **Beam ion** | Deuterium (D+) | shine-technology-overview.md | high | |
| **Target** | Tritium gas | shine-technology-overview.md | high | Externally sourced; no breeding |
| **Beam energy** | Up to ~300 kV | dossier.md (Wikipedia citation) | high | Electrostatic acceleration |
| **Fusion neutron energy** | 14.1 MeV | shine-technology-overview.md | high | D-T fusion product |
| **Neutron yield** | Up to 5 × 10^13 reactions/second | shine-technology-overview.md | high | Continuous operation |
| **Operation mode** | Steady-state (continuous beam) | shine-accelerator-driven-fusion-overview.md | high | |
| **Applications** | Medical isotopes (Mo-99, Lu-177), materials testing (FLARE, LIBRTI) | dossier.md, shine sources | high | Neutrons are the product |
| **Electricity generation** | None | shine-technology-overview.md | high | "Not a power reactor — no electricity generation, no breeding blanket" |
| **Q_scientific** | << 1 (estimated 10^-6 to 10^-3) | [inferred: beam-target fusion physics] | low | Fusion power / beam power; intrinsic to geometry |
| **Net electric power** | N/A | N/A | N/A | No power conversion system |
| **LCOE** | N/A | N/A | N/A | No electricity generation |

**Phase 4 (fusion power) status**: Per the dossier, SHINE's four-phase roadmap lists fusion power generation as "Phase 4" — a long-horizon objective with no public engineering parameters, no design studies, no capital cost estimates, and no LCOE projections. The gap is flagged as "truly-unknown / long-horizon." As of this analysis, there is no SHINE-designed fusion power plant to model.

---

## 5b. Override Candidates

**Not applicable — no 1costingFE archetype mapping exists for this concept.**

Per the prompt, this concept has no assigned 1costingFE archetype, and therefore no canonical account schema. The concept cannot be costed using the 1costingFE library because:
1. It is not a power-generating reactor (no electricity output)
2. It operates at Q << 1 (beam power vastly exceeds fusion power)
3. It has no thermal cycle, no blanket, no power conversion equipment

Even if a hypothetical SHINE-based power plant were engineered, the physics barrier (Q << 1) would render the account-by-account override exercise moot — no combination of component-level cost optimizations can overcome a fusion-power-to-beam-power ratio of 10^-6 to 10^-3.

---

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No fusion power plant design for SHINE's beam-target approach | S2, S5 | truly-unknown | Blocking (concept-level) | Would require SHINE to engineer Phase 4, which is currently a long-horizon objective with no public timeline |
| 2 | No pathway to Q >> 1 in beam-target geometry | S2 | truly-unknown | Blocking (physics-level) | Beam-target fusion is intrinsically sub-unity Q; no published concept overcomes this |
| 3 | No blanket design for beam-target fusion | S3, S5b | truly-unknown | Blocking | Would require novel integration of breeding blanket with linear beam-target geometry |
| 4 | No thermal cycle or power conversion system | S3, S5 | truly-unknown | Blocking | SHINE's operational systems have no energy capture; adding a thermal cycle does not address Q << 1 |
| 5 | No tritium breeding or closed fuel cycle | S3, S4 | truly-unknown | Blocking | SHINE's systems consume externally sourced tritium; no breeding capability |
| 6 | No capital cost estimate for hypothetical power plant | S1, S5 | truly-unknown | Blocking | No design exists to cost |
| 7 | No LCOE projection for hypothetical power plant | S1, S5 | truly-unknown | Blocking | Cannot compute LCOE for a system with no net electric output and Q << 1 |

**Summary**: All gaps are "blocking" and "truly-unknown" because **SHINE Technologies is not pursuing fusion power generation**. The concept operates successfully as a neutron source but has no pathway to net-positive electricity production due to fundamental physics (Q << 1). Filling these gaps would require SHINE to pivot from their current commercial focus (isotope production, materials testing) to power generation — a pivot that is not currently planned and that would face physics barriers intrinsic to the beam-target approach.

---

## 7. Family-Delta vs Comparables

(No comparable concept in the corpus for this design point.)

**SHINE Technologies' beam-target fusion is not comparable to any fusion power concept** in this corpus because it is not designed for power generation. The physics, architecture, and operational goals are fundamentally different:

**vs. Magnetic Confinement (tokamaks, stellarators, mirrors)**: Magnetic confinement concepts confine a thermal plasma in which fusion reactions occur over long timescales (confinement time τ ~ 1-10 seconds) with Q_plasma >> 1 achievable. SHINE's beam-target approach has no confinement and no thermal plasma — ions get one pass through the target. Q_scientific << 1 is intrinsic.

**vs. Inertial Confinement (laser ICF, heavy-ion ICF)**: ICF concepts compress fuel to extreme densities (ρ ~ 100-1000 g/cm³) for brief confinement times (τ ~ 10 ps), achieving fusion gain through areal density (ρR > 1 g/cm²). SHINE's beam-target approach operates at gas-target densities (ρ ~ 10^-4 to 10^-3 g/cm³) with no compression, no areal density gain, and no ignition pathway.

**vs. Magneto-Inertial Fusion (MagLIF, General Fusion)**: MIF concepts combine magnetic insulation with compression to achieve intermediate-density plasmas (ρ ~ 1-10 g/cm³) at intermediate confinement times (τ ~ 1-100 ns). SHINE's approach has no compression and no magnetic field in the target region.

**vs. Electrostatic Confinement (IEC, Polywell)**: IEC concepts use converging electrostatic potential wells to accelerate ions toward a central collision point, aiming for multiple ion recirculations and cumulative fusion probability. SHINE's approach is **not IEC** — it is a linear beam on a stationary gas target with no potential well and no ion recirculation. Despite the shared use of electrostatic acceleration, the geometries and confinement philosophies are completely different.

**Structural claim**: SHINE Technologies has demonstrated commercial viability **as a neutron source**. Neutrons are the product, not a byproduct, and the economics are favorable because neutrons command high value for medical isotopes (Mo-99 for Tc-99m, used in ~40 million diagnostic imaging procedures annually) and materials testing. This success does not translate to fusion power generation, where the Q << 1 limitation is disqualifying.

**Conclusion**: SHINE's beam-target fusion is a successful commercial application of D-T fusion for **non-power purposes**. It occupies a unique niche in the fusion landscape — the only FDA-approved, commercially operational fusion technology — but it is not a fusion power concept and should not be evaluated as one.

---

## 8. Sources

**Primary sources cited**:

1. **shine-accelerator-driven-fusion-overview.md** (iter-01/sources/) — High-level roadmap document describing SHINE's four-phase plan (isotope production, industrial inspection, materials testing, fusion power as long-horizon Phase 4). Explicitly flags that no public commercial fusion-power-plant parameters exist. Contribution: Establishes that fusion power is a distant objective with no published engineering.

2. **shine-technology-overview.md** (iter-01/sources/) — Technical description of SHINE's beam-on-target D-T fusion approach. States "Not a power reactor — no electricity generation, no breeding blanket." Quantitative parameters: beam energy (~300 kV), neutron yield (up to 5 × 10^13 reactions/second), neutron energy (14.1 MeV). Contribution: Confirms SHINE's operational systems are neutron sources, not power plants.

3. **dossier.md** (concept_research/38-particle-accelerator-driven-fusion/) — Differentiation table summary. Citations: SHINE Wikipedia page, SHINE corporate website, FLARE press releases. Contribution: Summary of concept classification (beam-target fusion, Other family, steady-state, neutron applications).

**Additional context sources** (not directly cited but inform analysis):

4. SHINE corporate website (shinefusion.com) — Press releases on FLARE, UKAEA LIBRTI partnership, medical isotope production facilities. Contribution: Operational status and commercial applications.

5. Wikipedia: SHINE Technologies — Technical background on accelerator parameters ("deuterium ions fired at a target at up to 300 kV"). Contribution: Beam energy parameter.

**Source quality assessment**: SHINE's public materials are transparent about operational neutron source systems but provide no information on fusion power generation. The "truly-unknown / long-horizon" data gap for Phase 4 (fusion power) is a documented absence rather than a failure to find sources. For the intended purpose (neutron source applications), data availability is Rich. For fusion power evaluation, the concept is Not Applicable.
