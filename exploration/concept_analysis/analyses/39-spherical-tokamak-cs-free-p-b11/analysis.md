---
ID: 39-spherical-tokamak-cs-free-p-b11
Concept: Spherical Tokamak CS-Free PB11 (ENN)
Company: ENN Energy
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: MFE
Archetype: TOKAMAK
Archetype-Fit: Low
Comparison-Status: costingfe-asterisked
Comparables: []
---

## Design Point

ENN Energy has not published a commercial plant design with net electric power output. The EHL-2 device described in available sources (arXiv 2401.11338, Plasma Science and Technology 2024) is a physics experiment with no net power target (P_net = 0 MWe), no energy conversion system, and no commercial-scale design parameters (Q_eng, capacity factor, capital cost). The concept dossier contains only EHL-2's experimental geometry (R₀ = 1.05 m, B₀ = 3 T, Ip = 3 MA) and physics objectives (hot-ion mode verification, p-B11 thermal reaction rate measurement).

The quantitative model in Section 5 uses EHL-2's experimental geometry and an exploratory P_native = 500 MWe as stand-in values to demonstrate 1costingFE library defaults for the PB11 TOKAMAK archetype. These outputs should NOT be interpreted as grounded in ENN's commercial plans or as realistic cost projections — they serve to exercise the framework in the absence of a published design point, and are known to underestimate the LCOE penalties documented in Sections 2 and 7.

## 1. Availability of Data

**Rating: Limited**

ENN Energy has published a conceptual roadmap paper for proton-boron-11 fusion using a spherical tokamak geometry (arXiv 2401.11338, Physics of Plasmas 31, 062507, 2024) and detailed physics design parameters for their experimental device EHL-2. The company's public website provides milestone updates (EXL-50U achieved 1 MA plasma current at 1.2 T in January 2024 with 150 kA TF coil current) and broad strategic framing ("direct energy conversion capability for higher efficiency"). However, the available information has three major gaps:

1. **No commercial plant design exists**. EHL-2 is explicitly positioned as a physics demonstration device to verify p-B11 thermal reaction rates and hot-ion mode operation at ~30 keV ion temperature. The roadmap paper states that EHL-2 is a physics-basis machine, not a power-producing reactor. No plant-scale parameters (net electric power, capacity factor, LCOE, or capital cost) are published.

2. **Energy conversion pathway is exploratory**. While ENN's website states that p-B11 "offers direct energy conversion capability," no engineering design for a direct converter (electrostatic decelerator, inverse cyclotron converter, or ion beam recovery system) has been disclosed. The arXiv roadmap notes that energy extraction is "preliminary considerations and challenges" — a companion paper is referenced but does not contain a detailed converter design.

3. **Magnet technology is unconfirmed**. The EXL-50U predecessor device operated TF coils at 150 kA / 1.2 T, consistent with resistive copper magnets. EHL-2 targets 3 T field at R₀ ≈ 1.05 m, still within copper-coil reach. No public statement announces HTS adoption, and the EHL-2 physics design paper (doi:10.1088/2058-6272/ad981a) does not specify conductor type in the accessible abstract.

The concept dossier draws from:
- arXiv 2401.11338 (ENN roadmap for p-B11 spherical torus fusion)
- EHL-2 physics design paper (Plasma Science and Technology, 2024)
- ENN Research website milestones and device pages (EXL-50U, EHL-2)
- Frontiers in Nuclear Engineering 2026 paper on p-B11 Lawson criterion (not ENN-specific, but provides physics constraints)
- arXiv 2406.15495 (critical comment on ENN roadmap, questioning hot-ion mode Ti/Te = 4 feasibility — abstract only, PDF extraction failed)

A recent critical paper (arXiv 2406.15495) argues that the hot-ion mode Ti/Te = 4 assumed in ENN's roadmap is "far from accessible" under realistic conditions, stating that achieving this ratio would require "near 20 times fusion power" in auxiliary heating, questioning "whether it makes sense economically." Full text was not successfully extracted, limiting assessment of this critique.

**Key data gaps**:
- Commercial plant design (P_net, geometry, Q_eng, capacity factor)
- Direct energy converter engineering (technology choice, efficiency, cost)
- Magnet conductor type for EHL-2 and future plants
- Blanket or first-wall design for commercial scale (EHL-2 has no blanket)
- Cost estimates for any subsystem or plant-scale capital cost
- Comparison to D-T spherical tokamaks at equivalent scale

## 2. Challenges in Capturing System Function

ENN's CS-free spherical tokamak targeting p-B11 aneutronic fusion presents four major LCOE modeling challenges, ranked by impact:

### 1. No Commercial Plant Design or Performance Data (Critical)

EHL-2 is a physics experiment with no net power output, no blanket, and no energy conversion system. The device parameters (R₀ = 1.05 m, B₀ = 3 T, Ip = 3 MA, Ti₀ ≈ 30 keV) describe a research machine intended to verify p-B11 thermal reaction rates and hot-ion mode (Ti/Te ≥ 2), not a commercial reactor. The gap between EHL-2 and a net-power plant is undefined:
- What major radius, field strength, and plasma current are needed for net power?
- What Q_eng is achievable, and what auxiliary heating power is required?
- What capacity factor and maintenance downtime should be assumed?

Without a published plant study, LCOE modeling requires inventing a design point from analogue scaling, introducing large uncertainty.

> "No commercial plant net-power / capital-cost / LCOE figures (EHL-2 is a physics-basis device, not a power plant — gap)."
> — enn-pb11-spherical-torus-roadmap.md §Roadmap & timeline

### 2. p-B11 Physics Constraints Impose Extreme Confinement Requirements (High uncertainty)

Proton-boron fusion has a high Coulomb barrier requiring ion temperatures ~200-300 keV for appreciable reactivity, far above D-T's ~10-20 keV. The Frontiers in Nuclear Engineering 2026 Lawson criterion analysis shows:
- Minimum Lawson triple product: neτT ≥ 1.5 × 10²² m⁻³s (hot-ion mode Te = 0.25Ti), versus ~10²¹ m⁻³s for D-T — roughly **15× worse confinement requirement**
- Optimal operating window: Ti = 190-330 keV for Te = 0.5Ti, or Ti ≥ 125 keV for Te = 0.25Ti
- Energy per reaction: 8.68 MeV (about half of D-T's 17.6 MeV)

> "Net energy production is achieved only when Te < Ti, with optimal operating windows identified at 190–330 keV for Te = 0.5Ti and 125–500 keV for Te = 0.25Ti."
> — frontiersin-journals-nuclear-engineering-articles-10-3389.md §Abstract

> "The minimum Lawson values obtained were 1.3 × 10²² m⁻³s (no radiation), 1.2 × 10²³ m⁻³s (Te = 0.5Ti), and 1.5 × 10²² m⁻³s (Te = 0.25Ti)"
> — frontiersin-journals-nuclear-engineering-articles-10-3389.md §3.3 Lawson criterion analysis

EHL-2's target of Ti₀ ≈ 30 keV is far below the 125-200 keV threshold, confirming it is a proof-of-concept for hot-ion mode physics, not a burning plasma device. The critical technical question is whether the hot-ion mode (Ti/Te ≥ 2 or higher) can be sustained at the required 200-300 keV temperatures. A critical comment (arXiv 2406.15495, abstract) argues that Ti/Te = 4 is "far from accessible" and would require "near 20 times fusion power" in auxiliary heating, questioning economic viability. If this critique is correct, the concept's entire premise is undermined.

The confinement penalty translates directly to LCOE impact: achieving 15× higher neτ requires either larger magnets (higher capital cost), higher density (higher bremsstrahlung radiation losses), or longer confinement time (larger volume, more shielding, higher first-wall fluence). The narrow operating temperature window (190-330 keV for Te = 0.5Ti) constrains design flexibility.

### 3. Direct Energy Conversion Technology is Undefined (Moderate-to-high uncertainty)

ENN's website states that p-B11 "offers direct energy conversion capability for higher efficiency," consistent with the aneutronic fuel producing 8.68 MeV in charged alpha particles. However, no engineering design for the converter is published. The options include:
- Electrostatic deceleration (as used in WHAM's end-loss venetian blinds, ~50-65% efficiency)
- Inverse cyclotron converter (ICC, never demonstrated at fusion scale)
- Ion beam recovery (conceptual, no prototypes)

Each technology has different efficiency, capital cost, and integration complexity. The arXiv roadmap notes that energy extraction is "preliminary considerations and challenges" for EHL-2, with no timeline for maturing the technology. Direct conversion efficiency could range from 40% (conservative electrostatic DEC) to 60%+ (optimistic ICC), a spread that moves net electric power by a factor of 1.5× for the same fusion power. This uncertainty propagates through the entire LCOE calculation.

If direct conversion proves impractical at scale, the concept would fall back to thermal conversion of charged particle energy via a blanket, eliminating the claimed efficiency advantage and adding tritium-free blanket cost (still needed for shielding and heat exchange even without tritium breeding). The absence of a blanket on EHL-2 means no experimental validation of this pathway either.

### 4. Central-Solenoid-Free (CS-Free) Operation Adds Subsystem Complexity (Moderate uncertainty)

ENN's distinguishing feature is non-inductive ECRH current drive to eliminate the central solenoid, enabling a lower aspect ratio (A ≈ 1.85) for better plasma confinement at smaller size. The arXiv roadmap states:

> "The central solenoid provides very limited volt-seconds, so plasma start-up and the MA-level toroidal-current ramp must be achieved by non-inductive current drive — identified as a central design challenge."
> — enn-pb11-spherical-torus-roadmap.md §Central-solenoid-free challenge

EXL-50 demonstrated ECRH current drive at ~1 A/W efficiency (arXiv 2104.14844). EHL-2 requires 3 MA plasma current, implying ~3 GW of ECRH power if the same efficiency holds — far beyond the stated 6 MW ECRH + 17 MW NBI heating budget. This discrepancy suggests either:
1. ECRH current drive efficiency must improve by orders of magnitude, or
2. The 3 MA target is reached via a different mechanism (NBI current drive, bootstrap current), or
3. The published parameters are incomplete or inconsistent.

If non-inductive startup requires GW-scale ECRH, the recirculating power fraction could be prohibitive for net power operation. The published parameters do not resolve this tension, adding modeling uncertainty.

**Summary**: The dominant challenge is the absence of any commercial plant design, forcing LCOE modeling to invent a design point from limited physics data. The p-B11 physics constraints (15× worse Lawson criterion, 200-300 keV operating temperature, hot-ion mode requirement) and undefined energy conversion pathway add major performance and cost uncertainties. The CS-free startup challenge is a subsystem-level risk that could affect recirculating power.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Direct Energy Conversion (DEC) for p-B11 Charged Particles — TRL ~1-2

**Demonstrated**: Electrostatic decelerators (venetian blinds) tested in mirror machine end-loss experiments in the 1970s at ~50-65% efficiency on low-power ion beams. Helion Energy has published conceptual designs for inductive energy recovery from expanding FRC plasmas (D-He3 fuel), but no test results.

**On paper only**: Inverse cyclotron converter (ICC) for aneutronic fusion products — proposed but never built at any scale. Ion beam recovery systems for p-B11 alpha particles — conceptual only. ENN's arXiv roadmap references energy extraction as "preliminary considerations and challenges" with no engineering design published.

**Missing at scale**: A direct converter integrated with a burning p-B11 plasma at fusion-relevant power levels (MW-scale alpha particle flux). The technology choice (electrostatic DEC vs ICC vs hybrid) is not disclosed. Efficiency at scale, cost per kW, and integration with plasma-facing components are unknown. The Frontiers paper notes that alpha particle heating effects were excluded from the Lawson analysis, making power balance estimates conservative but also leaving the converter's input power spectrum undefined.

### Hot-Ion Mode Plasma Sustainment at 200-300 keV — TRL ~2-3

**Demonstrated**: Hot-ion mode (Ti > Te) operation has been achieved in tokamaks and mirrors at modest temperatures (~10-50 keV ion, 5-20 keV electron). TFTR reached Ti/Te ≈ 2 transiently with NBI heating. EXL-50U (ENN) achieved 1 MA plasma current with ECRH heating, but ion/electron temperatures are not disclosed.

**On paper only**: Sustained hot-ion mode at Ti = 200-300 keV with Te = 0.25Ti or 0.5Ti as required for p-B11 net energy. The Frontiers paper states:

> "Theoretically, the Te/Ti ratios can be optimized... However, in practice, the condition is very difficult to apply because electrons absorb energy more easily than ions"
> — frontiersin-journals-nuclear-engineering-articles-10-3389.md §1 Introduction

The critical comment (arXiv 2406.15495 abstract) argues that Ti/Te = 4 is "far from accessible" under realistic conditions and would require "near 20 times fusion power" in auxiliary heating, questioning economic viability. If correct, the entire concept is non-viable. Full text extraction failed, limiting verification.

**Missing at scale**: A 200-300 keV ion temperature plasma with Te < Ti maintained for steady-state fusion burn. The required auxiliary heating efficiency and power are unknown. Bremsstrahlung radiation losses scale with Z² (boron charge = 5) and electron temperature, so maintaining low Te while heating ions to 200+ keV is a fundamental challenge. EHL-2 targets only ~30 keV ion temperature, confirming it cannot validate the high-temperature regime needed for net power.

### Non-Inductive Current Drive at 3 MA Scale — TRL ~3-4

**Demonstrated**: ECRH current drive at ~1 A/W efficiency on EXL-50 (arXiv 2104.14844) for solenoid-free startup to ~1 MA. NBI current drive is standard on existing tokamaks (DIII-D, JT-60SA) but typically supplements ohmic or bootstrap current rather than providing full steady-state drive.

**On paper only**: Non-inductive drive to 3 MA plasma current for EHL-2 with only 6 MW ECRH + 17 MW NBI. At 1 A/W efficiency, 3 MA would require 3 GW ECRH — a factor of 500× more than the stated 6 MW. This discrepancy suggests either the published efficiency is an optimistic target, bootstrap current provides most of the 3 MA, or the parameters are inconsistent. The arXiv roadmap identifies non-inductive startup as a "central design challenge" but does not resolve the power budget.

**Missing at scale**: Steady-state non-inductive current drive at multi-MA scale for a burning plasma, especially at the 200-300 keV temperatures required for p-B11 net energy. If ECRH efficiency cannot be improved by orders of magnitude, the recirculating power fraction could render the concept non-viable.

### CS-Free Spherical Tokamak Confinement (Baseline MFE) — TRL ~5-6

**Demonstrated**: Spherical tokamaks at modest field and current (NSTX, MAST, EAST) with conventional central solenoids. EXL-50U (ENN) achieved 1 MA plasma current at 1.2 T without a solenoid, using ECRH current drive. EHL-2 design targets 3 MA at 3 T in a low aspect ratio (A ≈ 1.85) geometry.

**On paper only**: Spherical tokamak confinement at the neτT ≥ 1.5 × 10²² m⁻³s required for p-B11 ignition (15× higher than D-T). The Frontiers paper shows that the Lawson criterion is minimized at Ti ≈ 245 keV for Te = 0.25Ti, but whether a spherical tokamak can achieve this confinement at 200-300 keV temperatures is unproven. Conventional tokamak scaling laws (ITER H-mode) are derived from D-T plasmas at 10-20 keV; extrapolation to 200 keV is uncertain.

**Missing at scale**: A burning p-B11 plasma in any magnetic confinement configuration. No tokamak, stellarator, or mirror has operated above ~100 keV ion temperature for sustained periods. The divertor heat flux challenge (>20 MW/m² at low density, per the roadmap notes) at 200-300 keV plasma temperatures has no experimental basis.

### Resistive Magnets at 3 T Field (if copper is used) — TRL ~7-8

**Demonstrated**: Copper resistive magnets at 1-3 T are standard in existing tokamaks (EAST, DIII-D, smaller devices). EXL-50U operated TF coils at 150 kA / 1.2 T. If EHL-2 uses copper, 3 T at R₀ = 1.05 m is within demonstrated capability.

**Missing at scale**: If a commercial p-B11 plant requires higher fields (>5 T) for confinement, resistive copper magnets become impractical due to resistive losses (recirculating power fraction >50%). HTS magnets would be needed, but ENN has not announced HTS adoption. The conductor choice for future plants is unspecified.

### Heating Systems (NBI, ECRH) — TRL ~7-8

**Demonstrated**: Neutral beam injectors and ECRH gyrotrons are mature technologies on existing tokamaks. EHL-2 specifies 17 MW NBI + 6 MW ECRH, achievable with current systems.

**Missing at scale**: Continuous-wave heating at the power levels required for p-B11 net energy (likely hundreds of MW based on the 15× Lawson penalty and critical power balance). NBI and ECRH wall-plug efficiency (~30-50%) means large recirculating power. If auxiliary heating must be "near 20 times fusion power" as the arXiv 2406.15495 critique suggests, Q_eng < 0.1 and the concept is non-viable.

### Balance of Plant (Thermal or Direct Conversion) — TRL ~N/A (No design)

**Demonstrated**: Steam Rankine and sCO2 Brayton cycles at GW scale in fission and fossil plants (TRL 8-9). Direct conversion systems do not exist at fusion power plant scale.

**On paper only**: Direct energy conversion for p-B11 charged particles. ENN states the fuel "offers direct energy conversion capability" but has published no converter engineering. Thermal conversion of charged particle energy via a blanket is an alternative but eliminates the efficiency advantage.

**Missing at scale**: Either pathway (direct or thermal) for p-B11 aneutronic energy at commercial scale. EHL-2 has no energy conversion system, so no experimental basis exists.

**Summary**: The critical subsystems blocking commercialization are:
1. Direct energy conversion (TRL 1-2) — no engineering, no prototypes
2. Hot-ion mode at 200-300 keV (TRL 2-3) — physics questioned by critical literature
3. Non-inductive current drive at 3 MA+ (TRL 3-4) — power budget unclear

The baseline spherical tokamak confinement (TRL 5-6) is relatively mature but unproven at p-B11 conditions. Heating systems and resistive magnets are demonstrated at EHL-2 scale (TRL 7-8) but may not scale to commercial requirements.

## 4. Key Materials and Supply Chain Considerations

### Boron-11 Fuel Supply

Natural boron is ~80% B-11 and ~20% B-10. Boron is industrially produced at ~1 million tonnes/year globally, primarily for glass, ceramics, and detergents. Enrichment to >95% B-11 (to minimize neutron production from B-10(n,α) reactions with stray neutrons) is not a current industrial process but is feasible via calutron-style electromagnetic isotope separation or gas centrifuge. The Frontiers paper assumes a proton:boron density ratio of 90:10, implying that B-11 consumption per unit energy is modest — no supply constraint is expected. The main unknowns are:
- Enrichment cost ($/kg B-11 at 95%+)
- Fuel injection mechanism for a steady-state plasma (gas puff, pellet injection, or neutral beam)
- Fuel recycling and inventory control (boron is not radioactive, simplifying handling)

No evidence of a sole-source bottleneck. Boron supply is decentralized (Turkey, USA, Chile, Argentina are major producers).

### Magnet Conductor (Copper or HTS)

If EHL-2 and future plants use resistive copper magnets, as inferred from the 150 kA / 1.2 T EXL-50U data, the conductor cost is low but the recirculating power fraction is high. Copper is a globally traded commodity with no supply constraints. The tradeoff is:
- **Resistive copper**: Low capital cost, high operating cost (continuous MW-scale resistive losses), limits achievable field to ~3-5 T before recirculating power becomes prohibitive.
- **HTS (REBCO tape)**: High capital cost (~$30-100/kA-m current pricing, targeting $10/kA-m for commercial viability), enables 10-20 T fields with minimal resistive losses. Supply chain is ramping (Shanghai Superconductor, Faraday Factory Japan, CFS) but not yet at GW-fusion-fleet scale.

The conductor choice is unspecified for EHL-2 and future plants. If the 15× Lawson penalty for p-B11 requires >5 T fields, HTS becomes mandatory and shares the same supply-chain scaling challenges as D-T HTS tokamaks. If resistive magnets are sufficient, the concept avoids HTS cost and supply risk but incurs higher recirculating power.

### First Wall and Vacuum Vessel Materials

p-B11 is aneutronic — neutron energy is <1% of total fusion energy, versus 80% for D-T. This dramatically reduces neutron wall loading (NWL) and fluence. The Frontiers paper emphasizes:

> "energetic neutrons... cause severe damage to reactor materials... tritium fuel is very rare and must be produced through a series of complex processes... produces high-energy neutrons, which cause neutron activation in reactor materials and subsequent production of radioactive waste"
> — frontiersin-journals-nuclear-engineering-articles-10-3389.md §1 Introduction

For a p-B11 plant, first-wall materials (stainless steel, tungsten, or advanced RAFM steels) face minimal neutron damage, allowing longer service life and simpler maintenance compared to D-T tokamaks. Tungsten divertor armor, if used, avoids the 14 MeV neutron embrittlement issue. However, the ENN roadmap notes "divertor heat flux > 20 MW/m² at low density" as a challenge, which is comparable to D-T tokamaks — the aneutronic advantage is neutrons, not heat load.

The roadmap also requires "high wall reflection to minimize electron radiation (bremsstrahlung/synchrotron) losses," suggesting a low-Z first wall coating (lithium, beryllium, or boron) to reduce impurity radiation. Beryllium is toxic and in limited global supply (~300 tonnes/year, dominated by Materion Corp in the USA), shared with D-T blanket concepts. Lithium is abundant but chemically reactive. Boron coatings would be self-consistent with the fuel but have never been tested as plasma-facing materials.

**Supply chain risk**: Low for boron fuel and structural materials. Moderate for beryllium if used as a first-wall coating. Unknown for the magnet conductor (depends on copper vs HTS decision). The aneutronic fuel eliminates tritium breeding (no lithium-6 enrichment, no FLiBe molten salt supply chain, no tritium handling).

### Direct Energy Converter Materials

If a direct energy converter is pursued, the materials requirements depend on the technology choice:
- **Electrostatic DEC**: High-voltage electrodes (tungsten, molybdenum, or carbon) in a magnetic expansion region. Venetian blinds (1970s concept) used thin ribbon electrodes, vulnerable to heat load and erosion. Modern materials (tungsten monoblock, CuCrZr heat sinks) could improve survivability but have never been tested in a fusion alpha-particle environment.
- **Inverse cyclotron converter (ICC)**: Superconducting coils to decelerate ions via inverse cyclotron resonance, then collect on electrodes. No prototypes exist, so materials requirements are speculative.

No supply-chain assessment is possible without a converter design.

**Summary**: The aneutronic fuel simplifies materials requirements by eliminating tritium breeding and reducing neutron damage, but the concept still faces divertor heat flux challenges comparable to D-T. Boron fuel supply is unconstrained. Magnet conductor choice (copper vs HTS) is the main supply-chain unknown, determining whether the concept shares HTS scaling risks with other tokamaks or avoids them at the cost of higher recirculating power. First-wall and converter materials are undefined pending engineering design.

## 5. Design Point Parameters

**No design point exists for this concept.** EHL-2 is a physics demonstration device, not a commercial reactor. The dossier and available sources provide device parameters for EHL-2 and theoretical constraints for p-B11 fusion from academic literature, but no published plant-scale design (net electric power, fusion power, Q_eng, capacity factor, or cost) from ENN.

The following table summarizes the available physics parameters for EHL-2 and the theoretical requirements for p-B11 net energy, noting that these do NOT constitute a commercial design point.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **EHL-2 Experimental Device** | | | | |
| R0 (major radius) | 1.05 m | enn-pb11-spherical-torus-roadmap.md §Device | high | EHL-2 physics experiment scale |
| plasma_t (minor radius) | [inferred: 1.05 / 1.85 ≈ 0.57 m] | [aspect ratio A ≈ 1.85 from roadmap] | medium | Not directly stated; computed from R0/A |
| elon (elongation) | not stated | — | — | Typical spherical tokamak: 1.8-2.5 |
| B (on-axis field) | 3 T | enn-pb11-spherical-torus-roadmap.md §Device | high | EHL-2 target field |
| Ip (plasma current) | 3 MA | enn-pb11-spherical-torus-roadmap.md §Device | high | CS-free (non-inductive drive) |
| Ti0 (core ion temp) | ~30 keV | enn-pb11-spherical-torus-roadmap.md §Device | high | Far below 200-300 keV needed for p-B11 net energy |
| Ti/Te (hot-ion ratio) | ≥ 2 | enn-pb11-spherical-torus-roadmap.md §Physics objective | high | EHL-2 goal; commercial plant may need ≥ 4 |
| p_input (auxiliary heating) | 23 MW (17 MW NBI + 6 MW ECRH) | enn-pb11-spherical-torus-roadmap.md §Device | high | Wallplug power for EHL-2 |
| fusion_power_MW | 0 (non-power device) | — | high | EHL-2 does not target net fusion power |
| net_electric_MWe | 0 | — | high | No energy conversion system on EHL-2 |
| **Theoretical p-B11 Requirements (Frontiers 2026 paper)** | | | | |
| Ti_min (ion temp for ignition) | 125-190 keV (Te = 0.25Ti or 0.5Ti) | frontiersin-journals-nuclear-engineering §Abstract | high | Academic analysis, not ENN-specific |
| Ti_optimal | 245-270 keV | frontiersin-journals-nuclear-engineering §3.3 | high | Minimizes Lawson criterion |
| Lawson triple product (neτT) | ≥ 1.5 × 10²² m⁻³s (Te = 0.25Ti) | frontiersin-journals-nuclear-engineering §Abstract | high | 15× worse than D-T (~10²¹ m⁻³s) |
| Energy per reaction | 8.68 MeV | frontiersin-journals-nuclear-engineering | high | Fixed by p-B11 fusion cross-section |
| Zeff (effective charge) | 2.4 | frontiersin-journals-nuclear-engineering §2.1 | high | Proton:boron 90:10 ratio |
| **Commercial Plant (Unknown)** | | | | |
| R0_commercial | not stated | — | — | No ENN plant design published |
| B_commercial | not stated (> 3 T likely) | — | — | Higher field likely needed for confinement |
| P_fus | not stated | — | — | Unknown; depends on confinement scaling |
| P_net | not stated | — | — | No commercial plant design |
| Q_eng | not stated (possibly < 1 per arXiv 2406.15495 critique) | — | — | Critical comment argues auxiliary heating >> fusion power |
| eta_th or eta_direct | not stated (claimed "higher efficiency" for direct conversion) | enn-iter2-search-notes.md §Energy Capture | low | No converter design or efficiency estimate |

**Critical gap**: The absence of a commercial plant design means LCOE modeling requires inventing a design point by analogy or scaling, introducing large uncertainty. The physics constraints (15× Lawson penalty, 200-300 keV operating temperature) suggest that a p-B11 plant would be substantially larger and more capital-intensive than a D-T tokamak at the same net electric power — but without a published design, the magnitude of the penalty is unknown.

**Contradictions**: The arXiv roadmap positions EHL-2 as a step toward commercial p-B11 fusion, but the critical comment (arXiv 2406.15495) argues the approach is economically questionable. The EHL-2 heating power budget (23 MW) appears inconsistent with the non-inductive current drive requirement (3 MA at ~1 A/W efficiency would need 3 GW), suggesting either the efficiency is much better than stated, bootstrap current dominates, or the parameters are incomplete.

## 5b. Override Candidates

**No overrides proposed.** The absence of a commercial plant design and the lack of company-grounded cost data for any subsystem mean that no evidence-based departure from 1costingFE library defaults is possible. The concept is too early-stage for override discovery via the per-account walkthrough — every account is missing company data.

```yaml
overrides: []
```

**Rationale**: The per-account walkthrough requires "company-grounded quantity, unit cost, or published dollar figure" for each account. ENN has published:
- Physics parameters for EHL-2 (R0, B, Ip, Ti, heating power) — but no cost estimates
- Qualitative statements ("direct energy conversion capability") — but no engineering or efficiency
- Device-scale milestones (1 MA at 1.2 T achieved) — but no commercial plant design

No account in the canonical schema (C220101 first wall/blanket, C220103 magnets, C220104 heating, C220108 divertor, CAS23 turbine, CAS70 O&M, etc.) can be priced from the available data. Even the magnet conductor type is unconfirmed (copper vs HTS), preventing a C220103 override. The energy capture pathway is undefined (direct vs thermal), preventing overrides to CAS23 (turbine) or a hypothetical direct-converter account.

When a commercial plant design is published with subsystem costs or grounded quantities, the walkthrough should be repeated. Until then, the library's per-archetype defaults are the only available cost basis, and they will be wrong (likely underestimating cost due to the 15× Lawson penalty and 200-300 keV operating temperature).

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No commercial plant design (R0, B, Ip, P_fus, P_net, Q_eng, capacity factor) | S1, S2, S5 | truly-unknown | blocking | ENN plant-scale design study with net power targets and cost estimates |
| 2 | Direct energy converter technology choice and efficiency | S1, S2, S3, S5b | proprietary | blocking | Engineering design for electrostatic DEC, ICC, or alternative; efficiency and cost estimates |
| 3 | Magnet conductor type (copper vs HTS) for EHL-2 and future plants | S1, S4, S5b | not-yet-sourced | important | EHL-2 engineering paper with TF/PF coil specifications; or ENN press release on HTS adoption |
| 4 | Non-inductive current drive power budget and efficiency | S2, S3, S5 | truly-unknown | important | Resolution of 23 MW heating vs 3 MA current at 1 A/W; bootstrap current fraction; ECRH efficiency scaling |
| 5 | Hot-ion mode Ti/Te ≥ 4 feasibility at 200-300 keV | S2, S3 | truly-unknown | blocking | Full text of arXiv 2406.15495 critique; experimental validation of Ti/Te > 2 at Ti > 100 keV; auxiliary heating efficiency |
| 6 | Blanket or first-wall design for commercial plant (aneutronic, but still needs shielding and heat exchange) | S4, S5 | truly-unknown | important | Plant-scale engineering study with blanket chemistry, materials, and thermal management |
| 7 | Capital cost estimates for any subsystem or total plant overnight cost | S5b | proprietary | blocking | ENN cost model or published $/kW estimate for commercial plant |
| 8 | Capacity factor and maintenance downtime assumptions | S2, S5 | truly-unknown | important | Plant availability model accounting for divertor/first-wall replacement (if any) and magnet maintenance |
| 9 | Comparison to D-T spherical tokamaks at equivalent scale | S7 | derivable | nice-to-have | Cross-analysis with ARIES-ST, NSTX-Upgrade, or Tokamak Energy's ST40/ST-E1 designs |
| 10 | Cross-section data uncertainty (Tentori-Belloni vs Nevins-Swain parameterizations) | S2 | truly-unknown | nice-to-have | Updated p-B11 reactivity measurements or consensus parameterization |

**Gap type definitions**:
- **truly-unknown**: ENN may not have this information internally (e.g., commercial plant design likely not finalized)
- **proprietary**: ENN has this information but has not disclosed it (e.g., direct converter engineering)
- **not-yet-sourced**: Information may be public but not found in available sources (e.g., EHL-2 magnet specs in Chinese-language publications)
- **derivable**: Can be estimated by analogy or scaling (e.g., comparison to other spherical tokamaks)

**Critical path**: Gaps 1, 2, 5, and 7 are blocking for LCOE modeling. Without a commercial plant design (1), energy conversion pathway (2), validation of hot-ion mode feasibility (5), and cost estimates (7), any LCOE calculation is speculative. Gaps 3, 4, 6, and 8 are important for accuracy but could be estimated by analogy to other concepts. Gaps 9 and 10 are refinements.

## 7. Family-Delta vs Comparables

**No comparable concept in the corpus for this design point.**

The differentiation table categorizes this concept as **MFE / Spherical tokamak / p-B11 fuel / RF + NBI heating / Direct (charged particle) energy capture**. No other concept in the 39-concept corpus matches this combination:
- D-T spherical tokamaks (HTS Compact Tokamak, Tokamak Energy's ST-E1) use D-T fuel, thermal cycle energy capture, and breed tritium in a blanket.
- Other p-B11 concepts (HB11 Energy's laser-boron fusion) use IFE confinement, not MFE.
- ENN's design is the only MFE p-B11 entry, and the only spherical tokamak targeting aneutronic fuel.

The family-delta is therefore articulated against external reference designs (ARIES-ST D-T spherical tokamak, ARIES-AT advanced tokamak) to establish the cost implications of p-B11 fuel and CS-free operation relative to D-T baseline, since no in-corpus concept shares this combination of MFE confinement, spherical tokamak geometry, and aneutronic fuel. These external references provide the only available quantitative baselines for the subsystem-level cost effects documented below.

### Delta 1: Aneutronic Fuel (p-B11 vs D-T) — Major LCOE Impact, Direction Uncertain

**Difference**: p-B11 produces 8.68 MeV in three alpha particles (charged) with <1% neutron energy, versus D-T's 17.6 MeV with 80% in 14 MeV neutrons.

**Cost effects**:
- **Advantage**: No tritium breeding blanket → eliminates CAS27 (special materials) for lithium-6 enrichment, FLiBe inventory, and tritium extraction plant. Saves $50-200M capital cost (ARIES-AT FLiBe inventory ~$90M, CFETR tritium plant ~$100M). Also eliminates ongoing tritium procurement ($35k/kg market rate, though self-sufficient D-T plants breed their own after startup).
- **Advantage**: Minimal neutron damage → first wall and blanket structure (C220101, C220102 shielding) have longer service life. ARIES-AT assumes 5-7 year first-wall replacement; p-B11 could extend to 10-20 years, reducing scheduled downtime and remote handling (C220110) utilization. Reduces capacity factor penalty by ~5-10 percentage points.
- **Advantage**: Reduced activation → lower radioactive waste disposal cost (not in CAS, but contributes to lifecycle cost and social license).
- **Penalty**: 15× worse Lawson criterion → requires 15× higher neτ product for ignition. Achievable via higher density (limited by bremsstrahlung), higher field (higher C220103 magnet cost), or larger volume (higher C220105 structure, C220106 vacuum system, C221 buildings cost). The physics scaling is unforgiving: if ENN targets D-T-equivalent confinement (neτ ~ 10²¹ m⁻³s), p-B11 would not ignite. If they scale up by 15× in neτ, the cost penalty could be 50-100% higher reactor CAPEX (CAS22 subtotal) to achieve the same net power.
- **Penalty**: Half the energy per reaction → requires 2× higher reaction rate (higher density or larger volume) for the same fusion power. This amplifies the Lawson penalty.
- **Penalty**: 200-300 keV operating temperature vs 10-20 keV for D-T → requires more auxiliary heating (C220104) wallplug power, higher recirculating power fraction, lower Q_eng. The arXiv 2406.15495 critique argues auxiliary heating could be "near 20 times fusion power," implying Q_eng < 0.1 and non-viability. Even if the critique is pessimistic, the high temperature and hot-ion mode requirement (Ti/Te ≥ 4) likely mean Q_eng < 2, versus Q_eng = 5-10 for D-T tokamaks.

**Magnitude**: The aneutronic savings ($50-200M blanket + tritium handling) are dwarfed by the confinement and auxiliary heating penalties. If the 15× Lawson penalty translates to even a 30% larger reactor for the same net power, the CAS22 cost increase (~$2B × 30% = $600M) is 3-6× the blanket savings. If Q_eng < 2 due to auxiliary heating, the recirculating power fraction rises to >50%, halving net output and doubling $/kW overnight cost. The net effect is likely a **LCOE penalty** relative to D-T, magnitude unknown but potentially 50-200% higher $/MWh. Data is insufficient to quantify — this is the dominant modeling uncertainty.

### Delta 2: Direct Energy Conversion vs Thermal Cycle — Moderate LCOE Impact, Advantage if Achievable

**Difference**: ENN's roadmap frames p-B11 as compatible with "direct energy conversion capability for higher efficiency," converting charged alpha particles to electricity without a thermal cycle, versus D-T's neutron energy → blanket heat → steam or sCO2 turbine (CAS23).

**Cost effects**:
- **Advantage**: Direct conversion efficiency 40-60% vs thermal cycle 35-45% (steam Rankine) or 45-50% (sCO2 Brayton). The 10-15 percentage point efficiency gain reduces the fusion power requirement for a given net electric power by ~25%, shrinking the reactor (C220101-C220108) and lowering capital cost. For a 1 GWe plant, a 10-point efficiency gain saves ~$200-400M in reactor CAPEX (assuming CAS22 ~ $2B for a D-T tokamak).
- **Advantage**: Eliminates CAS23 (turbine plant) entirely if direct conversion is the sole pathway. ARIES-AT turbine plant cost ~$300M for 1 GWe. However, this is partially offset by the cost of the direct converter itself, which is unknown but likely $50-150M for a 1 GWe plant (analogue: venetian blinds in MARS mirror study were <10% of plant cost).
- **Penalty**: Direct converter technology is undefined (TRL 1-2). If the converter efficiency is lower than claimed, or if thermal fallback is needed, the advantage evaporates. If thermal conversion is used, p-B11 loses the efficiency edge but still incurs the blanket/shielding cost (C220101, C220102) since charged particles would be thermalized in a blanket for heat exchange.

**Magnitude**: If direct conversion achieves 50% efficiency vs 40% thermal, the net LCOE benefit is ~10-15% lower $/MWh (holding all else equal). If direct conversion fails and thermal fallback is used, no benefit accrues. The advantage is **contingent on converter engineering**, which does not exist in any published form.

### Delta 3: CS-Free Operation (Non-Inductive Startup) — Moderate Cost, Neutral-to-Penalty

**Difference**: ENN eliminates the central solenoid, enabling a lower aspect ratio (A ≈ 1.85) and smaller device footprint. Conventional spherical tokamaks (NSTX, MAST) use a central solenoid for inductive current drive; some HTS compact tokamaks (CFS SPARC) also rely on the solenoid for plasma current. CS-free operation requires non-inductive ECRH or NBI current drive, demonstrated by ENN at 1 MA scale.

**Cost effects**:
- **Advantage**: Smaller aspect ratio (A ≈ 1.85 vs 2.5-3.0 for solenoid-equipped spherical tokamaks) improves plasma confinement for a given major radius, potentially reducing reactor size for the same fusion power. This is a physics optimization, not a subsystem cost savings — the magnets (C220103) and structure (C220105) still scale with R0 and B.
- **Penalty**: Non-inductive current drive requires continuous auxiliary heating (C220104) at high power. If ECRH efficiency is ~1 A/W (EXL-50 demonstrated), sustaining 3 MA requires 3 GW wallplug power, which is prohibitive. If ECRH efficiency can reach 10 A/W (no evidence), the power requirement drops to 300 MW, still a large recirculating power fraction. The arXiv roadmap identifies this as a "central design challenge" but does not provide a solution. The cost impact is an increase in C220104 (heating systems capital cost) and ongoing electrical cost (CAS70 O&M).
- **Neutral**: The absence of a central solenoid eliminates one component but is not a major cost driver in itself. ITER's solenoid is a large engineering challenge (peak field 13 T, structural loads, pulsed power) but is <5% of reactor CAPEX in cost models. The CS-free design avoids this complexity but adds auxiliary heating capital and operating cost.

**Magnitude**: If non-inductive current drive requires 10% of gross electric power (P_gross = P_net + P_recirc) for steady-state sustainment, the recirculating power penalty is ~100 MW for a 1 GWe plant, requiring an additional ~250 MW fusion power to compensate (at 40% overall efficiency). This increases reactor size and cost by ~10-15%. If current drive efficiency is worse, the penalty is proportionally higher. The net effect is **neutral to small penalty** (~10-20% LCOE increase) unless current drive efficiency improves dramatically.

### Delta 4: Resistive Magnets (Inferred) vs HTS or LTS — Major Cost, Penalty

**Difference**: ENN's EXL-50U operated TF coils at 150 kA / 1.2 T, consistent with resistive copper magnets. EHL-2 targets 3 T at R₀ = 1.05 m, still within copper-coil reach. No HTS adoption announced. In contrast, leading D-T spherical tokamaks (CFS SPARC, Tokamak Energy ST-E1) use HTS REBCO coils to achieve 12-20 T fields.

**Cost effects**:
- **Advantage**: Resistive magnets have lower capital cost than HTS. ARIES-AT HTS coils ~$400M for a 1 GWe plant; copper coils ~$50-100M (MARS mirror study). Saves ~$300M upfront.
- **Penalty**: Resistive magnets incur continuous resistive losses (MW-scale), increasing recirculating power fraction by 5-15% of gross electric power. For a 1 GWe plant, this is 50-150 MW recirc, reducing net output or requiring a larger reactor to compensate. The ongoing electrical cost (CAS70 O&M) rises by ~$5-15M/year (at $0.05/kWh industrial rate, 50-150 MW × 8760 hr × 0.05 $/kWh).
- **Penalty**: Resistive magnets limit achievable field to ~3-5 T before resistive losses become prohibitive. If the 15× Lawson penalty for p-B11 requires >5 T for confinement, resistive magnets are inadequate and HTS becomes mandatory, negating the capital cost advantage.

**Magnitude**: The resistive loss penalty is ~5-10% higher LCOE due to increased recirculating power and ongoing electrical cost. The capital cost savings (~$300M) are partially offset by the need for a slightly larger reactor to compensate for lower field confinement. If higher field is needed (>5 T), the concept must adopt HTS, incurring the $300M upfront cost and sharing the HTS supply-chain risks of other tokamaks. The net effect is **10-20% LCOE penalty if resistive magnets are used**, or **parity with D-T HTS tokamaks if HTS is adopted**.

### Summary of Family-Delta

The dominant deltas are:
1. **Aneutronic fuel (p-B11 vs D-T)**: Saves $50-200M on blanket/tritium but incurs 15× Lawson penalty and 2× energy-per-reaction penalty → likely **50-200% LCOE penalty** due to larger reactor, lower Q_eng, and higher auxiliary heating. Magnitude unknown due to lack of commercial plant design.
2. **Direct energy conversion**: Potential **10-15% LCOE advantage** if 50% efficiency is achieved, but technology is undefined (TRL 1-2). If thermal fallback is needed, no advantage.
3. **CS-free operation**: **10-20% LCOE penalty** due to non-inductive current drive recirculating power, unless ECRH efficiency improves by order of magnitude.
4. **Resistive magnets**: **10-20% LCOE penalty** vs HTS tokamaks due to resistive losses, or parity if HTS is adopted (capital cost +$300M, operating cost -$10M/year).

The net family-delta is likely a **LCOE penalty of 50-150% vs D-T HTS spherical tokamaks** at the same net electric power, driven primarily by the aneutronic fuel's confinement and auxiliary heating penalties. The direct conversion efficiency advantage (~10-15% LCOE benefit if realized) is insufficient to offset the physics penalties. The concept's viability hinges on whether hot-ion mode at 200-300 keV is achievable with Q_eng > 1 — the arXiv 2406.15495 critique argues it is not, but full analysis awaits the complete paper.

## 8. Sources

### Primary Sources (ENN Concept-Specific)

1. **arXiv:2401.11338 (Physics of Plasmas 31, 062507, 2024)** — "ENN's Roadmap for Proton-Boron Fusion Based on Spherical Torus"
   - **Contribution**: EHL-2 device parameters (R0 = 1.05 m, B0 = 3 T, Ip = 3 MA, Ti0 ~ 30 keV), CS-free operation description, hot-ion mode physics objective, p-B11 fuel cycle framing, roadmap strategy
   - **Location**: Dossier sources: iter-01/sources/enn-roadmap-pb11-arxiv-2401.11338.md

2. **EHL-2 Physics Design Paper (Plasma Science and Technology, doi:10.1088/2058-6272/ad981a, 2024)** — "Overview of the physics design of the EHL-2 spherical torus"
   - **Contribution**: EHL-2 engineering overview (abstract accessed), magnet system mentioned but conductor type not specified
   - **Location**: Cited in dossier; full PDF not successfully extracted

3. **ENN Research Website — Compact Fusion Pages**
   - EXL-50U device page (https://en.ennresearch.com/researchfield/Compactfusion/Experiment/): TF coils at 150 kA / 1.2 T milestone (January 2024)
   - EHL-2 device page (https://en.ennresearch.com/researchfield/Compactfusion/EHL_2/): Design target overview
   - Compact Fusion overview (https://en.ennresearch.com/researchfield/Compactfusion/): "p-11B fuel cycle… offers direct energy conversion capability for higher efficiency, produces minimal neutron radiation, and enables distributed power generation"
   - **Contribution**: Device milestones, magnet conductor inference (150 kA / 1.2 T consistent with copper), direct conversion framing
   - **Location**: Dossier sources: iter-02/sources/enn-iter2-search-notes.md

4. **arXiv:2104.14844** — "Solenoid-free current drive via ECRH in EXL-50"
   - **Contribution**: ECRH current drive efficiency ~1 A/W demonstrated on predecessor device
   - **Location**: Cited in dossier

### Critical / Commentary Sources

5. **arXiv:2406.15495 (2024)** — Critical comment on ENN's roadmap
   - **Contribution**: Argues hot-ion mode Ti/Te = 4 is "far from accessible" and would require "near 20 times fusion power" in auxiliary heating, questioning economic viability. Abstract only; full PDF not successfully extracted.
   - **Location**: Dossier sources: iter-02/sources/arxiv-2406-15495/output.md

### Academic Physics Sources (p-B11 General)

6. **Frontiers in Nuclear Engineering (2026)** — "Lawson Criterion Analysis for Proton-Boron Fusion" (doi:10.3389/...)
   - **Contribution**: Minimum Lawson triple product neτT ≥ 1.5 × 10²² m⁻³s (15× worse than D-T), optimal operating temperature Ti = 190-330 keV, hot-ion mode requirement (Te < Ti), bremsstrahlung radiation dominance, cross-section data uncertainty
   - **Location**: Dossier sources: iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389/output.md

### Sources Not Found or Inaccessible

7. **ENN commercial plant design study** — Not published. Gap 1 in inventory.
8. **Direct energy converter engineering design** — Not published. Gap 2 in inventory.
9. **EHL-2 magnet conductor specification** — Not found in English-language sources; may exist in Chinese-language ENN publications or internal reports. Gap 3 in inventory.

### Supporting Context (Comparables)

10. **ARIES-ST Study** — D-T spherical tokamak plant design (R0 ~ 3.2 m, 1 GWe, HTS magnets, FLiBe blanket, sCO2 cycle)
    - **Contribution**: Cost structure baseline for D-T spherical tokamaks (CAS breakdown, blanket cost ~$200M, HTS coils ~$400M, turbine ~$300M)
    - **Location**: Referenced for family-delta analysis; full study at https://qedfusion.org/DOCS/bib.shtml

11. **MARS and MINIMARS Mirror Studies (1983-1986)** — D-T magnetic mirror plant designs with direct conversion
    - **Contribution**: Venetian blinds DEC cost <10% of plant cost, resistive copper magnets ~$50-100M
    - **Location**: Referenced for resistive magnet and DEC cost analogues