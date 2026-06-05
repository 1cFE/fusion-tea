---
ID: 15-sheared-flow-stabilized-z-pinch
Concept: Sheared-Flow Z-Pinch (Zap Energy)
Company: Zap Energy
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: MFE
Archetype: STAGED_ZPINCH
Archetype-Fit: High
Comparison-Status: costingfe
Comparables: []
Design-Point-Name: Zap Energy SFS Z-Pinch Commercial Power Plant Module (Thompson et al. FST 2023; Zap October 2024)
Design-Point-Maturity: paper-concept
P-Native: 50
Grounding-Confidence: medium
---

## Design Point

- Name: Zap Energy SFS Z-Pinch Commercial Power Plant Module (Thompson et al. FST 2023; Zap October 2024)
- Maturity: paper-concept
- P_native: 50 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/engineering-paradigms-paper-summary.md
  - knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/century-demo-system.md

## 1. Availability of Data

**Rating: Moderate**

The SFS Z-pinch concept has a credible foundation in peer-reviewed plasma physics literature spanning three decades, beginning with the theoretical proposal by Shumlak and Hartman in 1995[^1] and progressing through sustained experimental programs at the University of Washington and Zap Energy. The primary power-plant conceptual design paper — Thompson, Levitt, Nelson, and Shumlak, "Engineering Paradigms for Sheared-Flow-Stabilized Z-Pinch Fusion Energy," *Fusion Science and Technology* 79:8 (2023)[^2] — is the single most important source for LCOE modeling. It provides the only published quantitative design point for a commercial SFS Z-pinch core, including plasma parameters at each development step, core dimensions, thermal power, fusion yield per pulse, drive efficiency, and the liquid-metal blanket concept.

Experimental validation is documented in several key papers: Zhang et al. (PRL 2019)[^3] demonstrated sustained neutron production from a sheared-flow-stabilized Z-pinch on FuZE, and Mitrani et al. (2021)[^4] confirmed thermonuclear neutron spectra. More recently, Zap Energy's FuZE-3 device achieved electron pressures up to 830 MPa (total plasma pressure ~1.6 GPa assuming Ti ≈ Te), electron densities of 3–5 × 10²⁴ m⁻³, and electron temperatures above 1 keV, as reported in a November 2025 press release[^5]. The Century engineering demonstration platform has achieved over 1,000 consecutive plasma pulses at ≥100 kA[^6] and is testing liquid-metal wall integration.

> "The SFS Z-pinch approach to fusion energy aims to improve the economic viability of fusion power by creating a system that can use the DT fuel cycle as advantageously as possible."
> — engineering-paradigms-paper-summary.md §I. Introduction

However, **no published power-plant system code output, LCOE estimate, or detailed CAS-level cost breakdown exists** for the SFS Z-pinch. The Thompson et al. (2023) paper is a conceptual description, not a systems engineering study. There is no equivalent to ARIES-AT, PROCESS, or Z-IFE-level cost decomposition for this concept. The 50 MWe module output figure comes from a Zap Energy press release describing Century as a stepping stone to "a single Zap Energy module that will produce 50 megawatts of electricity"[^7], not from a published thermal-hydraulic or power-balance calculation.

The Levitt (APS DPP 2025) conference abstract[^8] confirms the current experimental program structure but provides no new quantitative parameters beyond what FuZE-3 results already established. An OSTI pulsed-power roadmap paper (Curry et al. 2025)[^9] provides useful context on capacitor supply-chain constraints and component lifetime requirements but is not specific to the Zap design point.

**Key data gaps:**
- No published net electric output calculation (thermal efficiency, recirculating power fraction, parasitic loads)
- No published capital cost estimates for any subsystem
- No published pulse repetition rate demonstration above 0.2 Hz (Century), versus 10 Hz commercial target
- No published cathode lifetime data under reactor-relevant conditions
- No published neutronics/shielding analysis beyond "initial calculations" of TBR ≈ 1.1
- Ion temperature on FuZE-3 not directly measured (inferred from Ti ≈ Te assumption)

[^1]: Shumlak and Hartman, PRL 75(18), 3285 (1995)
[^2]: Thompson et al., FST 79:8, 1051–1058 (2023); DOI: 10.1080/15361055.2023.2209131
[^3]: Zhang et al., PRL 122(13), 135001 (2019)
[^4]: Mitrani et al., Phys. Plasmas 28, 112509 (2021)
[^5]: fuze-q-and-fuze-3.md §Why Extreme Pressure Matters for Fusion
[^6]: century-demo-system.md §DOE milestone paragraph
[^7]: century-demo-system.md §Module description paragraph
[^8]: century-and-fuze-a-updates-2025.md §Abstract
[^9]: osti-servlets-purl-2588719/output.md (Curry et al., LLNL-JRNL-2001600, August 2025)

## 2. Challenges in Capturing System Function

The SFS Z-pinch presents several distinctive challenges for LCOE modeling, ranked by impact on cost uncertainty:

### 2.1 No Published Power Balance (Critical)

The Thompson et al. (2023) paper states the single-core thermal power is 200 MW at nominal maximum, with 19 MJ fusion energy per pulse and Q > 10. But no explicit thermal-to-electric conversion efficiency, recirculating power fraction, or net electric output is published. The 50 MWe figure from the Century press release is not derived in any published analysis. Bridging from 200 MWth to a net electric output requires assumptions about:
- Thermal cycle efficiency (steam Rankine from LiPb at ~600 K implies η_th ≈ 0.33–0.38)
- Recirculating power (pulsed power recharge at ~70% drive efficiency, pumping, tritium processing)
- Parasitic loads (vacuum, cooling, control systems)

The implied net electric efficiency of ~25% (50 MWe / 200 MWth) is plausible for a low-temperature steam cycle with significant recirculating power but is an analyst inference, not a published figure.

### 2.2 Repetition Rate Scaling (Critical)

The concept targets 10 Hz commercial operation. Century has demonstrated 0.2 Hz (one shot every 5 seconds)[^10]. The 50× gap between demonstrated and required rep rate is the single largest physics-to-engineering extrapolation. At 10 Hz with 19 MJ per pulse, thermal power reaches 190 MWth — consistent with the "~200 MW nominal maximum" in the paper. But at the demonstrated 0.2 Hz, the same system produces only 3.8 MWth, illustrating why rep rate dominates the economics.

> "The pulse rate is variable to allow for controllably output power and load-following with a nominal maximum thermal power of 200 MW."
> — engineering-paradigms-paper-summary.md §III

### 2.3 Cathode Lifetime Under Reactor Conditions (High)

The plasma cathode is a solid structure in direct contact with the plasma, exposed to erosion, heat flux, and the full neutron flux from the fusing plasma. Thompson et al. (2023) acknowledges this is the one component not protected by the liquid-metal blanket but argues it is "a small volume and mass of material" with "simple geometry" facilitating "straightforward remote removal and replacement"[^11]. No lifetime estimate is published. Arc smelting furnace experience at powers up to 60 MW is cited as an analogy, but those are non-nuclear environments without 14.1 MeV neutron damage.

### 2.4 Confinement Scaling to Reactor Parameters (High)

The paper acknowledges directly:

> "Delivering pinch currents of ~1 MA is well within the technical state of the art in the field of pulsed power and numerical simulations suggest that sheared-flow stabilization is robust, but the question remains if sheared flows will continue to be effective at stabilizing laboratory Z pinches with higher fusion performance and longer pulse durations."
> — engineering-paradigms-paper-summary.md §III

Current experimental pinch currents on FuZE are 0.25–0.3 MA; the power plant requires 1.2–1.5 MA. FuZE-Q (designed for ~0.6–0.7 MA) was undergoing commissioning at time of the 2023 paper. FuZE-3 results at higher compression are encouraging but the current levels and fusion yields remain far below reactor requirements.

### 2.5 Pulsed Thermal Load on BOP (Moderate)

At 10 Hz with 19 MJ pulses, each pulse deposits energy in the LiPb blanket in microseconds. The thermal inertia of the thick liquid-metal blanket should smooth these pulses, but the coupling to a conventional steam Rankine cycle under repetitive pulsed thermal input is uncharacterized. This is shared with other pulsed concepts (MagLIF, laser ICF) but is less severe here due to lower individual pulse yield (19 MJ vs. hundreds of MJ to GJ for MagLIF/ICF).

[^10]: century-demo-system.md §Lightning Strikes paragraph; dossier.md §Repetition Rate
[^11]: engineering-paradigms-paper-summary.md §V

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### SFS Z-Pinch Plasma Confinement at Reactor Parameters — TRL 2–3

**On paper only at reactor scale.** The core physics claim — that sheared flows stabilize Z-pinch plasmas at currents of 1.2–1.5 MA, temperatures of 30–35 keV, and densities of 1.5 × 10²⁶ m⁻³ for 200 μs — is supported by numerical simulations referenced in Forbes et al. (2019) but has not been experimentally validated at anything close to these parameters. FuZE has demonstrated sustained DD neutron production at 0.25–0.3 MA with temperatures of 1–2 keV and densities of 10²³–10²⁴ m⁻³. FuZE-3 has reached pressures equivalent to ~1.6 GPa and densities of 3–5 × 10²⁴ m⁻³ but at much shorter confinement times (~1 μs) and without fusion-relevant current levels.

The APS DPP 2025 abstract states Zap is "seeking to complete the physics basis for the concept" and "determine the scaling laws to high-gain performance"[^12] — an explicit acknowledgment that the physics basis is not yet established.

### Plasma Cathode (High-Duty-Cycle) — TRL 3

**Demonstrated at sub-scale, not at reactor duty cycle.** Century is testing cathode damage mitigation techniques, and Zap Energy has an active program on electrode longevity. The cathode must withstand megaampere-scale currents, plasma erosion, and neutron flux at 10 Hz for commercial operation. Arc smelting furnace experience (60 MW, non-nuclear) provides partial confidence. No published lifetime data under neutron irradiation exists.

### Liquid-Metal Wall System (LiPb Weir-Wall) — TRL 3

**Partially demonstrated at sub-scale.** Century includes "one of the largest tests of a plasma-facing liquid metal blanket to date"[^13] and the first test of plasmas with flowing liquid metal occurred in mid-2024. However, Century uses liquid bismuth (not LiPb), since it is a non-DT engineering platform. The weir-wall concept for forming a cavity of flowing LiPb under gravity is novel and has not been demonstrated with the commercial LiPb eutectic at reactor temperatures.

### Tritium Breeding Blanket — TRL 2

**On paper only.** The LiPb blanket is designed to serve as both first wall and tritium breeder with a calculated TBR of ~1.1[^14]. This is from "initial calculations" (Forbes et al. 2019), not from a detailed neutronics analysis. A TBR of 1.1 is marginal — most D-T fusion designs target TBR ≥ 1.15 to ensure self-sufficiency accounting for losses. No detailed tritium extraction, processing, or inventory analysis is published.

### Repetitive Pulsed Power Supply — TRL 3–4

**Component-level demonstrations exist.** Thompson et al. (2023) reports 80% efficiency for solid-state thyristor switch stacks at 5 Hz operation, and 90% AC-DC rectification efficiency, combining to ~70% wall-plug-to-cathode efficiency[^15]. Century is testing a "cutting-edge pulsed power capacitor bank"[^16] at 0.2 Hz with 500 kA. The pulsed power pre-roadmap (Curry et al. 2025) notes that Zap Energy operates at 50 kV to 200 kV — significantly lower voltage than Z-machine-class systems (5–10 MV), which simplifies switch and capacitor requirements. However, scaling to 10 Hz at 1.2–1.5 MA with 10⁹-shot component lifetimes remains undemonstrated.

### Energy Conversion / BOP (Steam Rankine from LiPb) — TRL 5–6

**Mature technology in principle.** Steam Rankine cycle is conventional power-conversion technology. The coupling to a pulsed liquid-metal heat source at LiPb temperatures (~600 K) is non-standard but does not require novel components. The low source temperature limits thermal efficiency to ~33–38%.

[^12]: century-and-fuze-a-updates-2025.md §Abstract
[^13]: century-demo-system.md §Liquid metal paragraph
[^14]: engineering-paradigms-paper-summary.md §V; Forbes et al. FST 75:7 (2019)
[^15]: engineering-paradigms-paper-summary.md §IV
[^16]: century-demo-system.md §Funding paragraph

## 4. Key Materials and Supply Chain Considerations

### Lithium-Lead Eutectic (LiPb)

LiPb (17% Li, 83% Pb by atomic fraction) is the blanket, first wall, neutron multiplier, and heat-transfer medium. Both lithium and lead are globally abundant — lead production is ~12 Mt/year and lithium production is ~180 kt/year (2024). A single 200 MWth core with a 25 m³ blanket volume at LiPb density (~9,400 kg/m³) requires ~235 tonnes of LiPb. This is not a supply-chain constraint for a single plant, though lithium-6 enrichment for tritium breeding would draw on the same supply chain as battery and fission industries.

LiPb produces activation products (²¹⁰Po and ²⁰³Hg) that require waste management, though these can be mitigated by controlling isotope mix[^17].

### Capacitor Banks and Pulsed Power Components

The pulsed power driver is the dominant capital subsystem. The OSTI pulsed-power roadmap paper (Curry et al. 2025) quantifies a critical supply-chain bottleneck:

> "If 150 fusion power plants were to be built today to service the United States, the time required to build the required capacitors is approximately 125 years to 250 years given the western world's available manufacturers and supply chain of high voltage capacitors."
> — osti-servlets-purl-2588719/output.md §Energy Storage

Each plant may require 10,000 to 216,000 capacitors, with delivery times of 4–6 years per order at current manufacturing capacity. Labor is identified as "a major fraction of the capacitor cost at the present time." Capacitor lifetime improvements of 2–6 orders of magnitude are required for fusion applications (from ~10⁴ shots to 10⁶–10⁹ shots). Zap's lower voltage range (50–200 kV vs. 5–10 MV for Z-machine-class drivers) may ease capacitor specifications somewhat.

### Cathode Materials

The cathode must withstand megaampere plasma currents, erosion, and neutron damage at 10 Hz. Specific cathode materials are not named in any Zap Energy publication. Arc smelting furnaces use graphite electrodes — whether this or another material (tungsten, molybdenum) is suitable under neutron irradiation is not addressed.

### No Superconducting Materials Required

A distinctive advantage: the SFS Z-pinch requires no REBCO tape, Nb₃Sn, NbTi, or any superconducting wire. This eliminates the supply-chain constraints that affect tokamak, stellarator, and mirror concepts (REBCO at ~$40–100/m, limited global production capacity). No cryogenic helium or nitrogen systems are needed.

### No Laser Components Required

No precision optics, frequency conversion crystals, or high-power laser diode arrays. This eliminates supply-chain dependencies shared with laser ICF concepts.

[^17]: engineering-paradigms-paper-summary.md §V; Kondo et al. JPCS 1090 (2018)

## 5. Design Point Parameters

All parameters describe the named design point: Zap Energy SFS Z-Pinch Commercial Power Plant Module, a single fusion core at ~200 MWth / ~50 MWe. The multi-module plant configuration (multiple cores sharing infrastructure) is noted but not parameterized — per the design point selection, P_native = 50 MWe refers to a single module.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Pinch current | 1.2–1.5 MA | engineering-paradigms-paper-summary.md §III, Table I | high | Power plant column |
| Pinch radius | 0.15 mm | engineering-paradigms-paper-summary.md §III, Table I | high | spec key: `plasma_t` (minor radius equivalent) |
| Pinch length | 0.5 m | engineering-paradigms-paper-summary.md §III, Table I | high | Constant across all development steps |
| Electron density | 1.5 × 10²⁶ m⁻³ | engineering-paradigms-paper-summary.md §III, Table I | medium | Ti = Te assumed; not experimentally validated at this density |
| Temperature | 30–35 keV | engineering-paradigms-paper-summary.md §III, Table I | medium | Ti = Te assumed; simulation-based |
| Plasma lifetime per pulse | 200 μs | engineering-paradigms-paper-summary.md §III, Table I | medium | spec key: relevant to duty cycle |
| Fusion energy per pulse | 19 MJ | engineering-paradigms-paper-summary.md §III, Table I | medium | Derived from simulations at plant-relevant currents |
| Fusion Q (P_fus/P_input) | >10 | engineering-paradigms-paper-summary.md §V | medium | From Forbes et al. [14]; simulation, not experimental |
| Repetition rate | 10 Hz (target) | dossier.md §Repetition Rate; engineering-paradigms-paper-summary.md §III | high | 0.2 Hz demonstrated on Century |
| fusion_power_MW | ~190 MW | [inferred: 19 MJ × 10 Hz = 190 MW] | medium | informational — library back-solves from p_input + P_native |
| Single-core thermal power | 200 MW (nominal max) | engineering-paradigms-paper-summary.md §III | high | Includes P_fus + P_input deposited in blanket |
| net_electric_MWe | 50 MWe | century-demo-system.md §Module description | medium | Press release figure; no published derivation. Drives P_native |
| Drive efficiency (wall-plug to cathode) | ~70% | engineering-paradigms-paper-summary.md §IV | medium | Composed from 90% AC-DC × 80% modulator, rounded down |
| p_input_MW | ~19 MW | [inferred: 190 MW fusion / Q of 10 = 19 MW fusion input → at 70% drive efficiency, wall-plug draw ≈ 27 MW] | low | spec key: `p_input`. Recirculating power estimate is analyst-derived |
| Thermal efficiency (η_th) | ~0.33–0.38 | [estimated: steam Rankine from LiPb at ~600 K] | low | Not published; analyst estimate for low-temperature Rankine |
| Core diameter | ~3 m | engineering-paradigms-paper-summary.md §III | high | Set by blanket thickness |
| Core volume | 25 m³ | engineering-paradigms-paper-summary.md §V, Table II | high | |
| Blanket material | LiPb eutectic (17% Li, 83% Pb) | engineering-paradigms-paper-summary.md §V | high | |
| Blanket thickness | ~1 m+ | engineering-paradigms-paper-summary.md §V | medium | "on the order of a meter or more" |
| TBR | ~1.1 | engineering-paradigms-paper-summary.md §V | medium | "Initial calculations"; Forbes et al. (2019) |
| Magnet type | None | dossier.md §Magnet Type | high | Self-confined plasma; no external magnets |
| Fuel | D-T | dossier.md §Fuel | high | |
| Energy capture | Thermal (steam Rankine) | dossier.md §Energy Capture; engineering-paradigms-paper-summary.md §V | high | |
| Operation mode | Pulsed | dossier.md §Operation Mode | high | Each pulse ~200 μs, target 10 Hz |

**Key inferred values and derivation chains:**

- **p_input_MW ≈ 19 MW**: P_fusion ≈ 190 MW at 10 Hz; Q > 10 implies P_input < 19 MW fusion heating power. At 70% drive efficiency, wall-plug draw is ~27 MW. This is the recirculating power to the pulsed power system alone; additional parasitic loads (pumping, tritium, vacuum) are unquantified.
- **η_th ≈ 0.33–0.38**: No published value. LiPb outlet temperature is implied to be around 600 K (327°C) based on the resistivity reference in the paper. A subcritical steam Rankine cycle at this source temperature yields 33–38% gross thermal efficiency. This is a significant analyst assumption.
- **net_electric_MWe = 50 MWe**: From press release. Consistency check: 200 MWth × 0.35 η_th = 70 MWe gross – ~27 MW pulsed power recharge – parasitic loads ≈ 40–50 MWe net. This is broadly consistent, suggesting the 50 MWe figure is plausible but sensitive to thermal efficiency and parasitic load assumptions.

## 5b. Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier**: The design uses a flowing LiPb weir-wall as an integrated first wall and breeding blanket. This is architecturally distinctive (no solid first wall; the liquid metal itself IS the first wall), but no company-grounded cost figure, mass estimate, or unit price for the LiPb inventory or tank structure is published. The library default for a liquid-metal blanket account will apply. **No override.**

**C220102 — Radiation shield**: The thick LiPb blanket (~1 m+) serves as the radiation shield. No separate shield structure is described in the design. The shielding function is integrated into C220101. No company-grounded cost data. **No override.**

**C220104 — Primary pulsed driver**: The pulsed power capacitor bank is the primary driver. Thompson et al. (2023) describes the architecture (AC-DC rectification + solid-state thyristor pulsed-power modulator) and drive efficiency (~70%), but publishes no cost figure, stored energy specification, or capacitor count for the power-plant-scale system. The OSTI pulsed-power roadmap gives generic capacitor counts (10,000–216,000 per plant) and delivery timelines but no Zap-specific pricing. **No override.**

**C220105 — Primary structure**: The core is described as a ~3 m diameter, 25 m³ tank. No structural mass, material specification, or cost estimate is published. **No override.**

**C220106 — Vacuum system**: Required but no specifications or cost data published. **No override.**

**C220107 — Power supplies / pulsed-power capacitor bank**: This is the canonical account for the pulsed-power driver cost. The same situation as C220104 applies — architectural description exists but no cost figure. The drive efficiency of ~70% and voltage range (50–200 kV) are published, which could inform a bottom-up estimate, but no company-grounded dollar figure exists to justify departing from the library default. **No override.**

**C220109 — Direct energy converter**: Not applicable. The design uses thermal (steam Rankine) conversion, not direct energy conversion. **No override.**

**C220110 — Remote handling & maintenance**: The cathode is described as requiring periodic remote removal and replacement, with "simple geometry" facilitating this. No cost data. **No override.**

**C220111 — Reactor-equipment installation & assembly**: No data. **No override.**

**CAS21 — Buildings & site structures**: The core is ~3 m diameter / 25 m³ — dramatically smaller than tokamak or ICF chambers. This should result in significantly lower building costs, but no company-grounded cost figure is published. The library default for this archetype will apply, and the small core volume will naturally produce lower costs through the library's size-scaling. **No override.**

**CAS23 — Turbine plant equipment**: Steam Rankine cycle is conventional. No concept-specific data to override the library default. **No override.**

**CAS24 — Electric plant equipment**: No data. **No override.**

**CAS26 — Heat rejection system**: No data. **No override.**

**CAS27 — Special materials (initial blanket fill)**: The LiPb inventory for a 25 m³ core at ~9,400 kg/m³ density is approximately 235 tonnes. At commodity LiPb prices (~$5–10/kg for the eutectic), this is roughly $1.2–2.4M — modest but quantifiable. However, this is an analyst-derived estimate using commodity pricing, not a company-published figure. The lithium-6 enrichment cost (if required for TBR) is an additional unknown. **No override** — the quantity is derivable but the company has not published a costed bill of materials.

**CAS70 — Annualized O&M**: No published maintenance schedule, staffing model, or component replacement plan. Cathode replacement frequency is the key unknown. **No override.**

**CAS80 — Annualized fuel cost**: D-T fuel costs are standard. Tritium startup inventory requirements are not quantified. **No override.**

```yaml
overrides: []
```

**Override count: 0 enabled.** The archetype-fit grade is High, which expects 0–4 enabled overrides. A count of 0 is within band. The design point is architecturally distinctive (no magnets, liquid-metal first wall, pulsed power driver) but the company has published no cost figures, unit prices, or quantified bills of material for any subsystem. The library defaults for the pulsed-electrical-drive archetype are the best available baseline.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published power balance (η_th, recirculating fraction, parasitic loads, net electric derivation) | S2, S5 | truly-unknown | blocking | Request from Zap Energy or derive from thermal-hydraulic analysis of LiPb Rankine system |
| 2 | Repetition rate demonstrated at 0.2 Hz vs. 10 Hz target — 50× gap | S2, S3 | truly-unknown | blocking | Track Century rep-rate progression; no external source can close this gap |
| 3 | Cathode lifetime under reactor conditions (neutron flux + erosion + 10 Hz cycling) | S2, S3 | truly-unknown | blocking | No analogue exists; requires Zap experimental data |
| 4 | Pulsed power system cost (capacitor count, stored energy, unit price at volume) | S5b | proprietary | important | OSTI pulsed-power roadmap provides generic capacitor costs; Zap-specific data needed |
| 5 | TBR validated by detailed neutronics (current value of ~1.1 from "initial calculations") | S3 | not-yet-sourced | important | Request Monte Carlo neutronics study (MCNP/Serpent) from Zap or independent analysis |
| 6 | Ion temperature confirmation on FuZE-3 (Ti ≈ Te assumption not directly measured) | S2, S3 | truly-unknown | important | Await peer-reviewed FuZE-3 publication |
| 7 | LiPb operating temperature (inlet/outlet) and thermal cycle specification | S5 | not-yet-sourced | important | Required for thermal efficiency estimate; could be derived from LiPb thermodynamics |
| 8 | Cathode material specification | S3, S4 | proprietary | nice-to-have | Zap has not disclosed; arc smelting analogy suggests graphite but not confirmed |
| 9 | Structural material for core tank (material, nuclear-grade requirements) | S4 | not-yet-sourced | nice-to-have | LiPb compatibility studies suggest ferritic-martensitic steels or Hastelloy |
| 10 | Multi-module plant configuration details (shared infrastructure, N × 50 MWe scaling) | S5 | truly-unknown | nice-to-have | No published plant-level layout |

## 7. Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

The SFS Z-pinch is the only self-confined, pulsed, magnet-free, electrically-driven MFE concept in the portfolio. Its nearest conceptual neighbors would be:

- **MagLIF (Pacific Fusion)**: Shares the pulsed-power-driven architecture and liquid-wall concept, but MagLIF uses Z-machine-class drivers at 60+ MA with GJ-class yields, external magnetization (or self-magnetizing targets), and optional laser preheat. The SFS Z-pinch operates at much lower current (1.2–1.5 MA), much lower yield per pulse (19 MJ), and much higher rep rate (10 Hz vs. ~1 Hz), with no magnets and no laser. The economic tradeoff is fundamentally different: MagLIF bets on high yield per shot to amortize driver cost; Z-pinch bets on high rep rate from a simpler, cheaper driver.

- **General Fusion (MTF Pneumatic Compression)**: Shares the liquid-metal wall concept and pulsed operation, but uses mechanical compression of a magnetized plasma rather than electrical current. The Z-pinch eliminates the mechanical compression system entirely.

Without an approved comparable in the corpus, no quantitative family-delta can be articulated. The qualitative positioning is: the SFS Z-pinch trades physics performance per pulse for engineering simplicity and high capital utilization through rep rate, with the absence of magnets, lasers, and cryogenics as the central cost thesis.

## 8. Sources

1. **Thompson, Levitt, Nelson, Shumlak, "Engineering Paradigms for Sheared-Flow-Stabilized Z-Pinch Fusion Energy," FST 79:8, 1051–1058 (2023)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/engineering-paradigms-paper-summary.md`
   Contribution: Primary source for the commercial design point — plasma parameters at each development step (Table I), core geometry, LiPb blanket concept, drive efficiency, comparative analysis vs. tokamaks and ICF. The only published peer-reviewed paper describing a SFS Z-pinch power plant concept.

2. **Century Demo System Press Release (Zap Energy, October 2024)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/century-demo-system.md`
   Contribution: 50 MWe module output figure, Century operating parameters (100 kW input, 500 kA, 0.2 Hz, 1000+ shots), multi-module plant architecture concept, liquid-metal wall testing milestone.

3. **FuZE-3 Gigapascal Results (Zap Energy press release, November 2025)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/fuze-3-gigapascal-results-2025.md`
   Contribution: Latest experimental performance — 830 MPa electron pressure, 3–5 × 10²⁴ m⁻³ density, >1 keV Te. Three-electrode architecture for independent acceleration/compression control.

4. **FuZE-Q and FuZE-3 Overview (Zap Energy press release)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/fuze-q-and-fuze-3.md`
   Contribution: FuZE-3 experimental results, three-electrode design rationale, qualitative cost positioning claims.

5. **Curry et al., "Challenges and Gaps in the Development of Pulsed Power for Fusion Applications," LLNL-JRNL-2001600 (August 2025)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-03/sources/osti-servlets-purl-2588719/output.md`
   Contribution: Capacitor supply-chain constraints (125–250 years to build 150 plants' worth at current manufacturing capacity), component lifetime requirements (10⁶–10⁹ shots), Zap-specific voltage range (50–200 kV), labor cost dominance in capacitor manufacturing.

6. **Levitt, "Progress Towards Commercial Fusion..." APS DPP 2025 Abstract**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/century-and-fuze-a-updates-2025.md`
   Contribution: Current program structure (FuZE-3, FuZE-Q, FuZE-A, Century), acknowledgment that physics basis and scaling laws are still being determined.

7. **Zap Energy Website — How It Works**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/zap-energy-website-how-it-works.md`
   Contribution: Qualitative concept description, 10 Hz target, no-magnets/no-lasers architectural claim.

8. **Dossier — Sheared-Flow Stabilized Z-Pinch (D-T)**
   Path: `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md`
   Contribution: Consolidated differentiation table values with confidence assessments, source index, key references.

9. **Forbes et al., "Progress Toward a Compact Fusion Reactor Using the Sheared-Flow-Stabilized Z-Pinch," FST 75:7, 599 (2019)**
   Referenced but not directly available as an extracted source. Cited in Thompson et al. (2023) for TBR calculations and Q > 10 projections.
