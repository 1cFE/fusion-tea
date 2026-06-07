## Design Point

- Name: Orion — Helion 8th-generation first commercial plant (50 MWe Microsoft PPA, 2028 target)
- Maturity: pilot-demonstrator
- P_native: 50 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md
  - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md

---

## Section 1: Availability of Data

**Rating: Limited**

Helion is more transparent than most private fusion startups. Seven prototype generations have produced published results, the FRC physics heritage (FRX-L at LANL, TCS at UW, IPA at MSNW, FRX-L/FRCHX at LANL/AFRL) is well documented in peer-reviewed literature, and the company publishes detailed explanatory articles on its website. The Feb 2026 D-T milestone announcement disclosed a plasma temperature (150 million °C / 13 keV) and site construction progress for Orion. Contrary Research and the DocsLib ARPA-E presentation add a modest layer of quantitative grounding.

However, the data that matters most for an LCOE model of Orion is almost entirely absent from the public record:

> "Orion's detailed specifications are proprietary. No peer-reviewed reactor engineering design document (like ARIES or ARC) has been published." — dossier.md §Remaining Gaps

The ARPA-E presentation gives a `50 MW, 2 Hz` design point and a 40 T reactor field target but provides no cost breakdown, no bill of materials, and no component cost estimates. Device geometry for Orion (plasma radius, compression zone length, coil configuration) is not published. Q > 1 has not been demonstrated on any prototype. The energy balance at commercial power levels — the coupling between capacitor bank energy, fusion gain, and DEC efficiency that determines net electrical output — is proprietary and not inferable from available public data.

**Key data gaps:** Orion device geometry; capacitor bank energy at commercial scale; validated Q > 1; D-He3 plasma operation at any temperature; He3 self-breeding rate; component cost breakdown; p_input (wall-plug power to capacitor charging).


---

## Section 2: Challenges in Capturing System Function

### 1. Direct-conversion energy balance is the dominant LCOE lever — and its closure is unverified

Helion's entire economic thesis rests on inductive DEC recovering 85–95% of the input energy per pulse, so that a modest fusion gain per pulse (Q_plasma > 1) yields substantial net electricity. The constraint is binding: the Contrary Research report states that "95% of input energy after each pulse must be recovered for net electricity" — a hard system requirement, not a target. A 1% shortfall (94% recovery instead of 95%) approximately doubles the net loss fraction, which at 50 MWe output would cut net power significantly.

> "95% of input energy after each pulse must be recovered for net electricity." — contrary-research-helion.md §Energy

This constraint has been demonstrated at subscale (>95% round-trip efficiency over 1 million pulses on Grande, 2014), but never at commercial power levels or at multi-Hz rep rates with the full compression and expansion cycle. The coupling between Q_plasma, DEC efficiency η_DEC, and net electrical output is the single highest-impact unknown for the LCOE model.

### 2. Repetition rate — a 1,000× scale-up from current demonstrated performance

> "Trenta operated at ~1 pulse per 10 minutes." — dossier.md §Repetition Rate

The ARPA-E presentation specifies 2 Hz for the 50 MW commercial design point. Trenta's achieved rate of ~1/10 min is roughly 1/600 Hz. Polaris targets ~1 Hz. The step from 1/600 Hz to 2 Hz is a 1,200× increase in pulse frequency, requiring the shot cycle (FRC formation, acceleration, collision, compression, expansion, energy recovery, plasma exhaust, recharging) to execute reliably in 0.5 seconds. No data is available on the engineering margin for this cycle at Polaris, let alone Orion.

Rep rate directly multiplies power output and is the second most leveraged economic parameter after DEC efficiency. Unlike the DEC, rep rate has no demonstrated near-commercial analog.

### 3. D-He3 fusion not yet demonstrated in any device

Helion's commercial fuel is D-He3. D-T fusion was demonstrated on Polaris at 150M°C in February 2026. D-He3 requires 200M°C (Helion's figure) or ~65 keV / 750 million K (Contrary Research). Neither has been achieved in any FRC device. The Polaris result retires one milestone but leaves the most fundamental physics question — whether the device can operate at nearly twice the demonstrated temperature with the correct fuel — unanswered.

### 4. He3 self-breeding infrastructure is uncharacterized

Helion's fuel cycle relies on DD side reactions producing tritium, which decays to He3 over 12.3 years. The self-breeding scheme is physically sound but the engineering to extract and store tritium, manage the radioactive inventory, and accumulate sufficient He3 to fuel a commercial plant is nowhere described in public sources. The scale of the He3 startup inventory requirement (and its cost) is a genuine unknown.

### 5. Capacitor bank cost at NOAK is assumed, not demonstrated

Current commercial capacitor technology costs approximately $5/J. The SfA white paper (Science for America, 2023) identifies that this must fall to <$0.50/J for pulsed magnetic fusion to be economically viable — a 10× reduction. Helion manufactures some capacitor components in-house but no public data exists on achieved cost per joule for Helion's own hardware.

### 6. Library archetype mis-fit is severe

The 1costingFE MIF archetype was calibrated for D-T concepts with thermal conversion cycles and tritium breeding blankets. Helion eliminates three of the most expensive canonical accounts: CAS23 (turbine plant), C220103 (HTS magnets), and the large Li-bearing blanket fill in CAS27. Simultaneously, it adds an account (C220107, pulsed-power capacitor bank) that is the dominant driver cost and for which no library default exists calibrated to Helion's architecture. The model requires extensive per-account departures (see Section 5b) to produce a meaningful LCOE estimate.


---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

### D-He3 Fusion at Commercial Conditions — TRL 2

**Missing at scale.** D-He3 fusion has not been attempted in any FRC device. The reaction requires ion temperatures of 200M°C (Helion) to 750M K (~65 keV, Contrary Research) — nearly twice the 150M°C demonstrated on Polaris with D-T fuel. The 20× extrapolation from Trenta's demonstrated 100M°C (9 keV, D-D) to 750M K is the largest single physics leap in the roadmap.

### He3 Self-Breeding System — TRL 2

**On paper only.** DD reactions produce tritium (12.3-yr half-life to He3) and He3 directly. The chemistry is understood. The engineering to separate, store, and manage tritium inventory at sufficient rate to fuel a commercial D-He3 plant has not been demonstrated. Tritium handling involves regulatory burden comparable to D-T fission systems.

### Commercial Rep Rate (2 Hz) — TRL 2

**Missing at scale.** Trenta demonstrated ~1 pulse per 10 minutes. Polaris targets ~1 Hz. The 2 Hz commercial requirement demands a 500 ms shot cycle including FRC formation, supersonic translation, collision, compression, fusion, expansion, energy recovery, plasma exhaust, and capacitor recharging. No public data exists on Polaris shot cycle timing.

### Q_plasma > 1 / Net Electricity Demonstration — TRL 3

**On paper only.** Polaris's stated goal is to demonstrate net electricity. D-T fusion at 150M°C has been achieved but no Q measurement has been published. The energy balance (fusion yield vs. capacitor bank energy) is proprietary.

### Commercial Magnetic Field (40 T compression) — TRL 3

**Missing at scale.** Trenta demonstrated 8 T, Polaris targets 15 T+, and the commercial design requires 40 T peak compression. The 5× field increase from demonstrated conditions drives the entire plasma parameter improvement cascade. Coil design for 40 T pulsed operation at multi-Hz rep rate is not characterized.

### Pulsed Electromagnetic Coil System (Commercial Scale) — TRL 4–5

**On paper only at commercial scale; demonstrated at sub-scale.** The Trenta and Polaris coils are aluminum EM coils driven by capacitor banks — confirmed aluminum by CEO Kirtley.

> "CEO Kirtley: 'regular aluminum magnets'" — contrary-research-helion.md

Aluminum coils at 8–15 T have been built across prototype generations. The 40 T commercial coil design at multi-Hz rep rate has not been demonstrated; coil fatigue at repetitive high-field pulsing is a major engineering challenge.

### Direct Inductive Energy Recovery (Subscale Demonstrated) — TRL 5

**Demonstrated at subscale; not at commercial power or rep rate.** Grande (4th generation, 2014) demonstrated >95% round-trip energy recovery efficiency over 1 million pulses at subscale.

> "In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs." — helion-website-technology.md §Energy Capture

Commercial operation requires this performance at 50 MWe per module output, 2 Hz, for decades. No commercial-scale DEC demonstration exists.

### FRC Formation and Supersonic Translation — TRL 5–6

**Demonstrated in prototype.** FRC formation, supersonic translation at >300 km/s, collision, and merging are demonstrated across Helion's prototype generations and in the academic heritage (IPA experiments at MSNW/UW). Polaris successfully formed FRCs and achieved D-T fusion, confirming the formation-and-compression sequence works at the 13 keV level.

### Capacitor Banks and IGBT Switch Systems — TRL 6

**Mature pulsed power technology.** Capacitor banks and high-voltage IGBT switches are commercially available. The challenge is NOAK cost reduction (from ~$5/J to <$0.50/J) rather than technical viability.

### Shielding System — TRL 7–8

**Demonstrated analog.** Helion's shield vault uses borated polyethylene and borated concrete — standard materials with extensive hospital particle-accelerator heritage. The low neutron energy from D-He3 (~2.45 MeV DD side-reaction neutrons vs 14.1 MeV D-T) makes this a solved engineering problem at modest scale.

> "Borated polyethylene and borated concrete shield vault… approximately one-meter solid barrier… similar to hospital particle beam shielding." — dossier.md §Neutron Management

### Power Conditioning and Grid Interface — TRL 8–9

**Commercially mature.** Direct electricity output from the inductive DEC needs power conditioning to produce grid-compatible AC. High-power inverters, transformers, and grid-interconnect hardware are commercially mature. No turbine plant, steam generator, or heat exchangers are required.


---

## Section 4: Key Materials and Supply Chain Considerations

### Helium-3 — Critical, Limited Supply

He3 is the commercial fuel. Global civilian stockpiles are small (~25 kg worldwide); the primary source has historically been tritium decay from U.S. weapons programs. Industrial demand already exceeds new production in some years. Helion's self-breeding approach (DD → tritium → He3 via 12.3-yr beta decay) addresses the supply problem in principle but creates a time lag: a fleet of 1 GWe would require 20 Orion modules, each needing He3. The startup inventory before sufficient self-bred He3 accumulates represents an upfront procurement cost with no published estimate.

Market price for He3 is approximately $5,000–$20,000 per liter (STP). The breeding time constant is set by tritium's half-life (12.3 years), so He3 accumulation is slow. If the startup inventory before net He3 self-sufficiency is on the order of kilograms, the cost could be significant.

### Capacitors — Cost-Reduction Dependent

The capacitor bank (>50 MJ, tens of kV per module) is built from high-voltage capacitors and IGBT switches. Current commercial capacitor pricing is approximately $5/J stored. The SfA white paper identifies that this must fall to <$0.50/J for commercial viability — a 10× reduction driven by manufacturing scale. Helion manufactures some capacitor components in-house; whether this achieves target cost is proprietary.

> "The main risk is the supply chain for in-house components: capacitors, quartz tubes, and other key components." — contrary-research-helion.md §Risk

### Aluminum and Copper Coils — No Constraint

Pulsed electromagnetic coils wound from aluminum and copper alloys are fabricated from commodity materials with no supply chain constraint. This is a significant advantage over HTS concepts requiring REBCO tape (limited suppliers, tight production capacity). Helion's deliberate choice of resistive coils eliminates the HTS supply chain risk entirely.

### IGBT Switches — Moderate Supply

High-voltage, high-current IGBTs (enabling >95% energy recovery) are commercially available from multiple vendors (Infineon, ABB, Mitsubishi). Helion uses custom configurations. No sole-source risk, but qualification to fusion duty cycles (multi-Hz, decades of operation) needs demonstration.

### Deuterium — No Constraint

D2 is separated from ordinary water by electrolysis at approximately $0.30/liter. Supply is essentially unlimited. Fuel cost is negligible.

### Structural Materials — No Constraint

Standard structural steel, borated concrete, borated polyethylene. All commodity. No supply constraint. The absence of beryllium, Li-bearing ceramics, FLiBe, or exotic first-wall materials (tungsten tiles, EUROFER) means Helion's material supply chain is the simplest of any fusion concept.

### Quartz Tubes — Minor

Helion uses quartz tubes as part of the vacuum and plasma system. Industrial quartz manufacturers (Heraeus, Saint-Gobain) supply the scientific instrumentation market at adequate scale. No bottleneck risk.


---

## Section 5: Design Point Parameters

All values describe the Orion commercial design point at native scale (50 MWe per module). Parameters derived from the ARPA-E presentation's explicit "50 MW, 2 Hz" design point are treated as the primary Orion specification; Polaris prototype data are noted separately as informational.

| Parameter | Value | Source | Confidence | Note |
|---|---|---|---|---|
| Net electric power | 50 MWe | docslib-helion-arpa-e-presentation.md §Fusion Engine Design Point; helion-milestones-feb2026.md §Orion | high | spec key: `net_electric_MWe`; equals P_native; Microsoft PPA commitment |
| Repetition rate | 2 Hz | docslib-helion-arpa-e-presentation.md §Fusion Engine | high | ARPA-E presentation states "2 Hz @ 50 MW"; Polaris targets ~1 Hz as intermediate step |
| Compression field (B) | 40 T | docslib-helion-arpa-e-presentation.md §Reactor Target | medium | 40 T is reactor design target per ARPA-E; 20 T for ARPA-E experiment; Polaris targets 15 T+; spec key: `B` |
| Capacitor bank energy (per module) | >50 MJ | helion-website-technology.md §Capacitor Bank | medium | stated lower bound; commercial scale likely higher; charged to "tens of kV" |
| Plasma density (compressed) | 10²³ m⁻³ | docslib-helion-arpa-e-presentation.md §Parameters | medium | compressed target density from ARPA-E presentation |
| Plasma velocity (FRC) | >300 km/s | dossier.md §Confinement Concept | high | FRC translation velocity before collision; "supersonic" |
| Ion temperature (D-He3 target) | ~65 keV (~750 million K) | contrary-research-helion.md §Fuel | medium | Helion states "200M°C" (17 keV); Contrary Research states "750 million K" (65 keV); discrepancy noted; 13 keV (150M°C) demonstrated on Polaris for D-T |
| Device length (Orion) | ~38 m [inferred] | helion-prototype-generations.md §8th Prototype | low | Polaris is 19 m; Orion "expected to be twice the size of Polaris" |
| Plasma beta | ~100% [inferred] | contrary-research-helion.md §Confinement | medium | high-beta FRC; company describes plasma pressure approaching magnetic pressure |
| DEC round-trip efficiency | 95% required; ≥85% claimed | contrary-research-helion.md §Energy; helion-website-technology.md §Energy Capture | medium | 95% is system constraint; 85–95% is range cited for commercial operation; >95% demonstrated at subscale |
| Neutron energy fraction | ~5% | dossier.md §Neutron Management | high | D-He3 with DD side reactions; Helion published claim; 2.45 MeV neutrons from DD side reactions only |
| Fuel cycle | D-He3 (self-bred He3) | dossier.md §Fuel | high | Commercial target fuel; D-T used on Polaris as intermediate test step |
| p_input_MW | [unknown] | No source | — | Wall-plug power to capacitor charging system; not published; requires Q_plasma and DEC efficiency to calculate; critical LCOE input |
| R0 (FRC equivalent) | N/A for linear device | — | — | Major radius concept does not apply; relevant geometry is device length and compression zone radius; neither published for Orion |
| Plasma elongation | N/A for FRC | — | — | Toroidal elongation concept does not apply to linear FRC geometry |
| Compression zone minor radius | [unknown] | No source | — | FRC plasma half-width at peak compression; not published; needed for wall loading calculation |

**Geometry note:** The standard 1costingFE spec keys for torus geometry (R0, `plasma_t` as minor radius, `elon`) do not map meaningfully to Helion's linear bilateral FRC device. The relevant geometric parameters (compression zone radius, device half-length, FRC separatrix dimensions) are not published for Orion. The model-setup agent should note these gaps explicitly and apply analogue estimates or flag as blocking.


---

## Section 5b: Override Candidates

The following overrides are derived from a per-account walkthrough of the canonical schema. All relative values use the modular-fleet frame: `M × generic.cas22_detail["C2201xx"]` for Class-U accounts, `M × generic.costs.<rollup>` for Class-S and Class-P accounts. Rationales are anchored to "the library's default for a fleet of this device at 1 GWe," not to a monolithic 1 GWe plant.

The expected override band for Low Archetype-Fit is 6–12 enabled overrides. This walkthrough yields 10 enabled overrides, within the band.

```yaml
overrides:
  - account: C220101
    value: 0.10 * generic.cas22_detail["C220101"]
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; helion-website-technology.md §Shielding"
    rationale: |
      Library C220101 prices a tritium-breeding blanket (first wall + breeding material +
      multiplier) appropriate to a D-T or D-D MIF concept. Helion's D-He3 fuel produces
      only ~5% of its energy as neutrons (2.45 MeV from DD side reactions), and there is no
      tritium breeding blanket — the fuel cycle is self-contained via DD → tritium → He3 decay.
      The "blanket" reduces to the vacuum vessel wall plus a modest borated shielding layer
      (comparable to hospital particle-beam shielding). No Li-bearing breeding material, no
      beryllium neutron multiplier, no liquid metal first-wall loop. The library's modular-fleet
      default for this account (one blanket per module × n_mod modules) is ~10× the
      Helion equivalent. 0.10 × library default captures a basic energy-containment wall
      with shielding but no breeding structure.

  - account: C220102
    value: 0.25 * generic.cas22_detail["C220102"]
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; helion-website-technology.md §Shielding"
    rationale: |
      Library C220102 prices a radiation shield sized to 14.1 MeV D-T neutron wall loading.
      D-He3 DD side-reaction neutrons are 2.45 MeV — far less penetrating. Helion states
      "approximately one-meter solid barrier" of borated polyethylene and borated concrete,
      explicitly compared to hospital particle-beam shielding. At 2.45 MeV, penetration depth
      in concrete is roughly 1/5 that of 14.1 MeV neutrons, and the neutron energy fraction
      is ~5% vs ~80% for D-T. Shield mass, material cost, and installation complexity are all
      dramatically reduced. 0.25 × library default for a fleet of this device at 1 GWe
      reflects the much lighter shielding requirement.

  - account: C220103
    value: 0.05 * generic.cas22_detail["C220103"]
    enabled: true
    provenance: derived
    source: "dossier.md §Magnet Type; helion-website-technology.md §Magnets; contrary-research-helion.md §Magnets"
    rationale: |
      Library C220103 prices HTS-REBCO confinement coils (conductor + winding + cryostat)
      at roughly $44k/kg-equivalent for REBCO tape. Helion uses pulsed aluminum
      electromagnetic coils ("regular aluminum magnets" per CEO Kirtley) driven by a capacitor
      bank. There is no REBCO, no cryostat, no cryogenic plant, and no quench protection
      system. Pulsed aluminum coils are wound from commodity conductor material with no exotic
      procurement. The per-module coil cost is a small fraction of HTS coil cost; the driver
      capital has moved entirely into C220107 (capacitor bank). For the library's modular-fleet
      default at 1 GWe (n_mod = 20 modules each contributing one coil set), 0.05 × captures
      the aluminum coil winding cost without any superconductor, cryostat, or cryogenic
      infrastructure premium.

  - account: C220107
    value: 25.0
    enabled: true
    provenance: derived
    source: "helion-website-technology.md §Capacitor Bank; docslib-helion-arpa-e-presentation.md §Fusion Engine"
    rationale: |
      C220107 prices the pulsed-power capacitor bank at $/J stored. Helion stores >50 MJ per
      module at tens of kV. Unit cost: the SfA white paper (Science for America, May 2023)
      identifies that commercial viability requires capacitor cost to fall from the current ~$5/J
      to <$0.50/J through NOAK manufacturing learning, analogous to battery cost trajectories.
      Helion manufacturers some components in-house. At the NOAK target of $0.50/J and a
      50 MJ bank: 50,000,000 J × $0.50/J = $25M per module. This is Class U (per-module),
      so the 1 GWe fleet of n_mod = 20 modules costs $500M in total capacitor bank capital.
      The library's generic value for C220107 at $/J stored likely differs from this assumption;
      25.0 M$ per module is the NOAK-derived estimate. The $0.50/J unit cost is from a sector
      analogue (SfA 2023), not a Helion-published figure — provenance is derived.

  - account: C220109
    value: 0.0
    enabled: true
    provenance: direct
    source: "helion-website-technology.md §Energy Capture; contrary-research-helion.md §Energy"
    rationale: |
      Helion's inductive DEC is physically integrated into the pulsed electromagnetic coil
      system: the same coils that compress the plasma also recover energy from the expanding
      magnetized plasma via Faraday induction. There is no separate direct-energy-converter
      hardware — the DEC IS the coil system (C220103) and the capacitor bank (C220107). Pricing
      C220109 as a standalone account would double-count the coil and bank capital already
      captured above. The correct per-module charge for C220109 in a 1 GWe fleet of this
      device is $0. Company-published architecture confirms the integrated approach.

  - account: C220110
    value: 0.20 * generic.cas22_detail["C220110"]
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; helion-website-technology.md §Shielding"
    rationale: |
      Library C220110 prices remote handling equipment sized for a high-neutron D-T environment
      (rad-hardened manipulators, hot cells, shielded transport casks). Helion's D-He3 fuel
      produces ~5% neutron energy at 2.45 MeV — a neutron environment comparable to hospital
      accelerator facilities, not a fission or D-T fusion plant. Personnel access to the machine
      with modest shielding is feasible; full remote-handling infrastructure is not required.
      The library's per-module remote handling cost for a 1 GWe fleet is ~5× what Helion needs.
      0.20 × library default captures a basic maintenance infrastructure with minimal radiation
      hardening.

  - account: CAS23
    value: 0.0
    enabled: true
    provenance: direct
    source: "helion-website-technology.md §Energy Capture; contrary-research-helion.md §Energy"
    rationale: |
      Helion converts fusion energy directly to electricity via inductive DEC — expanding
      magnetized plasma induces current in the surrounding coils. There is no thermal cycle:
      no steam generator, no turbine, no condenser. Company publications explicitly state
      "No steam cycle required." CAS23 for a 1 GWe fleet of this device is $0. This is
      Class P (power-proportional); the library default scales with electrical output.

  - account: CAS24
    value: 0.60 * generic.costs.cas24
    enabled: true
    provenance: derived
    source: "helion-website-technology.md §Energy Capture"
    rationale: |
      CAS24 covers switchyard, transformers, and plant electrical distribution. Helion's
      direct electricity output still requires power conditioning (AC conversion from pulsed DC
      inductive output), step-up transformers, and grid interconnect hardware. However, without
      a turbine-generator interface, turbine-hall electrical plant, and large synchronous
      generator switchgear, CAS24 is materially reduced. 0.60 × the library's 1 GWe
      power-proportional default captures the grid interconnect and power electronics while
      removing the turbine-side electrical infrastructure. Class P.

  - account: CAS26
    value: 0.10 * generic.costs.cas26
    enabled: true
    provenance: derived
    source: "helion-website-technology.md §Energy Capture; contrary-research-helion.md §Energy"
    rationale: |
      CAS26 prices heat rejection (cooling towers, circulating water) sized for the waste heat
      from a thermal-cycle plant, which rejects roughly 55–60% of fusion thermal power.
      Helion's DEC recovers 85–95% of fusion energy as electricity; waste heat to reject is
      primarily from resistive losses in coils, neutron capture in the shield (~5% of fusion
      energy), and DEC inefficiency (~5–15% of fusion energy). Total heat rejection requirement
      is roughly 10–20% of a comparable thermal-cycle plant at the same electrical output.
      0.10 × the library's 1 GWe power-proportional default reflects this dramatically
      reduced cooling burden. Class P.

  - account: CAS27
    value: 0.05 * generic.costs.cas27
    enabled: true
    provenance: derived
    source: "dossier.md §Fuel; dossier.md §Neutron Management"
    rationale: |
      CAS27 covers the initial blanket material inventory (LiPb, FLiBe, or equivalent) —
      the special materials fill that must be procured before first plasma. Helion has no
      Li-bearing breeding blanket, no LiPb or FLiBe inventory, and no tritium startup
      inventory (D-He3 fuel; He3 is self-bred from DD reactions). The only "special materials"
      are a modest deuterium startup charge (from water, negligible cost) and a He3 startup
      inventory whose size is unknown but likely small relative to a LiPb blanket fill.
      0.05 × the library's 1 GWe power-proportional default represents the near-elimination
      of the blanket fill account, leaving a small residual for any specialty materials
      (e.g., shielding fill, initial He3 procurement). Class P.
```

**Count check:** 10 enabled overrides. Expected band for Low Archetype-Fit: 6–12. Count is within band.


---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|---|---|---|---|---|
| 1 | Q_plasma (fusion gain per pulse) — not published; required to close energy balance at 50 MWe | S2, S5 | proprietary | blocking | Helion SEC/NRC filings; Polaris experimental results publication |
| 2 | p_input_MW (wall-plug power to capacitor charging) — cannot be derived without Q and η_DEC | S5 | proprietary | blocking | Same as Gap 1; interlocked |
| 3 | Orion device geometry (compression zone radius, coil dimensions, device half-length) | S5 | proprietary | blocking | No public source; Helion site press releases may disclose partial data post-groundbreaking |
| 4 | Capacitor bank energy per module for Orion (currently lower-bounded at 50 MJ) | S5 | proprietary | important | DocsLib ARPA-E presentation notes ">50 MJ"; commercial scale may differ |
| 5 | D-He3 plasma operation in any device (temperature, density, confinement time at D-He3 conditions) | S2, S3 | truly-unknown | blocking | First demonstration expected on Polaris (2026–2027 Helion roadmap) |
| 6 | Commercial repetition rate demonstrated (target 2 Hz; current state ~1/600 Hz on Trenta) | S2, S3 | truly-unknown | blocking | Polaris operational milestones (not yet published) |
| 7 | He3 startup inventory requirement and cost before self-breeding reaches steady state | S4, S5 | not-yet-sourced | important | Helion He3 breeding rate article; tritium decay calculator with assumed D-D reaction rate |
| 8 | Capacitor bank unit cost at Helion's in-house manufacturing scale ($/J achieved) | S4, S5b | proprietary | important | Company has not published; SfA white paper $0.50/J target is sector-level aspiration |
| 9 | He3 breeding rate per module (DD reaction rate × tritium production × decay rate = He3/yr) | S4 | derivable | important | DD fusion cross-section at operating temperature + plasma burn fraction calculation |
| 10 | Component replacement schedule (pulsed coil lifetime under repetitive 40 T pulsing) | S3 | truly-unknown | important | No published fatigue data for aluminum coils at 40 T, multi-Hz, multi-year |
| 11 | Net electricity demonstration on Polaris (milestone in progress as of analysis date) | S3 | not-yet-sourced | important | Helion milestone announcements (expected 2026) |
| 12 | CAS21 (buildings) footprint and cost for Malaga WA Orion site | S5b | not-yet-sourced | nice-to-have | Orion construction filings, NRC/DOE permitting documents |


---

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

For context: the closest concepts in the landscape by confinement family (MIF) are MagLIF (Pacific Fusion) and MTF Pneumatic Compression (General Fusion). Both are D-T pulsed MIF concepts with thermal conversion cycles and are structurally different in every cost-relevant dimension from Helion's D-He3 direct-conversion design. The MagLIF analysis (concept 07) provides useful reference points for pulsed power cost assumptions (SfA white paper $5/J → $0.50/J) and the general challenge of rep-rate-dominated LCOE economics, but the concepts share no account-level cost structure.

If a comparable is added to the corpus in the future, the primary family-delta dimensions to articulate would be:

**Against any D-T MIF concept (MagLIF, MTF):**
- CAS23 (turbine plant): Helion = $0; D-T MIF concepts carry a full thermal cycle — a ~$200M penalty for D-T relative to Helion.
- C220101 (blanket): Helion has no tritium breeding blanket — a ~$200–500M per-module advantage at conventional blanket pricing.
- C220103 (magnets): Helion's aluminum coils vs. no external steady-state magnets in MagLIF (per-shot consumable coils for MagLIF); roughly comparable given both avoid HTS.
- C220107 (capacitor bank): Both families need large pulsed-power banks; cost per joule is the shared uncertainty.
- CAS26 (heat rejection): Helion ~10% of MIF D-T requirement; a meaningful operating cost advantage.
- He3 fuel cost (CAS80, not overridable): No public estimate available; likely a material OPEX difference vs. tritium for D-T concepts.


---

## Section 8: Sources

1. **Helion Energy ARPA-E Presentation** (DocsLib)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md`
   - Contribution: quantitative design-point parameters (50 MW, 2 Hz, 20 T experiment, 40 T reactor target, plasma density 10²³ m⁻³, ion temperature 8+ keV, FRC velocity >300 km/s); energy cost target <$0.03/MJ input; η × Gain = 0.7 × 1.2 figure of merit.
   - Most useful single source for physics parameters.

2. **Helion Website Technology Articles** (multiple pages)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md`
   - Contribution: conceptual description of FRC formation, compression, and direct inductive energy recovery; >50 MJ capacitor bank; aluminum coil confirmation; "no steam cycle" explicit; 95% energy recovery requirement; Polaris dimensions (19 m); shielding description.

3. **Contrary Research: Helion Energy** (investor analysis)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/contrary-research-helion.md`
   - Contribution: 85–95% direct conversion efficiency claim; D-He3 temperature requirement (750 MK / 65 keV); 95% recirculating energy recovery as hard constraint; in-house capacitor and quartz tube manufacturing; Nucor 500 MWe partnership; supply chain risk identification.

4. **Helion Energy Milestones (Feb 2026)** (milestone press release)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-milestones-feb2026.md`
   - Contribution: D-T fusion at 150M°C (13 keV) on Polaris as of February 2026; construction begun on Orion site in Malaga WA (July 2025); Microsoft PPA confirmed; Dr. Alan Hoffman expert endorsement of DEC approach.

5. **Helion Prototype Generations** (Wikipedia-sourced overview)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md`
   - Contribution: prototype generation table (Grande → Polaris); Orion described as "twice the size of Polaris"; direct conversion demonstrated at subscale (Grande, >95% efficiency, 1 million pulses); MITRE/JASON critique (40 T commercial requirement, 8 T demonstrated as of 2018); Microsoft PPA (50 MWe, 2028).

6. **Concept Dossier** (internal research summary)
   - Path: `knowledge/concept_research/08-frc-w-direct-conversion/dossier.md`
   - Contribution: all 12 differentiation table columns with citations and confidence ratings; FRC confinement classification (MIF); D-He3 fuel cycle description; He3 self-breeding mechanism; repetition rate data (Trenta: 1/10 min, Polaris: ~1 Hz target); neutron management description.

7. **Science for America White Paper, "New Opportunities in Fusion Power" (May 2023)**
   - Used for capacitor cost analogue ($5/J current → <$0.50/J NOAK target); not a direct Helion source; cited as sector-level cost reference for C220107 derivation.
   - Not in `knowledge/` directory — external reference.
