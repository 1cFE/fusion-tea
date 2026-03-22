---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion
Company: Helion Energy
Status: draft
Created: 2026-03-22
Approved-Date:
Reuses: [07-maglif, 01-hts-compact-tokamak]
---

# D1+ Analysis: FRC w/ Direct Conversion (Helion Energy)

**Concept**: Pulsed colliding FRC with direct electromagnetic energy recovery — D-He3 fuel
**Company**: Helion Energy (Everett, WA)
**Commercial Plant**: Orion (50 MWe, Malaga, WA — under construction, Microsoft PPA, 2028 target)
**Confinement Family**: MIF (Magneto-Inertial Fusion)
**Operation Mode**: Pulsed (~millisecond plasma lifetime per cycle)

---

## Section 1: Availability of Data

**Rating: Limited**

Helion Energy is the best-funded private fusion company in the world, but one of the least transparent technically. The concept has a solid experimental heritage through seven prototype generations (Grande through Polaris), and the broader FRC experimental database is extensive — spanning six decades, multiple national programs, and hundreds of published papers from U.S. and Japanese programs (LANL FRX series, University of Washington LSX, RPPL TCS experiments). However, the specific colliding-and-compressing FRC approach that Helion pursues is proprietary in its key details, and no independent cost studies, system code outputs, or peer-reviewed plant design papers exist for Helion's concept specifically.

**Experimental heritage (Helion-specific):**

> "Creation of high-temperature plasma through merging and compression of supersonic field reversed configuration plasmoids"
> — Slough, Votroubek, Pihl, *Nuclear Fusion* 51(5), 2011
> (Phase 1a dossier §Key Sources — peer-reviewed anchor paper from Helion founders)

This 2011 paper from the University of Washington / MSNW LLC precursor group (Helion founders Slough, Votroubek, Pihl, Kirtley) is the primary peer-reviewed basis for the merging/compression approach. It provides the physics foundation but not power-plant-scale engineering. Subsequent peer-reviewed work includes Kirtley et al. (IEEE SOFE 2021) and Kirtley & Milroy (J. Fusion Energy 2023) on FRC compression scaling. A "Comments on Kirtley & Milroy" response paper appeared in J. Fusion Energy (2026), indicating active peer engagement.[1]

**Prototype performance (recent):**

> "Helion has achieved 150 million degrees Celsius, surpassing its previous record of 100 million degrees Celsius set by Trenta... first privately-funded machine to demonstrate D-T fusion (January 2026)"
> — helion-milestones-feb2026.md, §Key Technical Details

Polaris (seventh-generation, operational since late 2024) achieved 13 keV ion temperature, and has a 50 MJ+ capacitor bank, 15 T+ compression target, and 3,800 diagnostics. Trenta (sixth-generation) ran for 16 months and >10,000 pulses. These prototype milestones are the strongest public data in the analysis.[2]

**Company transparency:**
Helion publishes milestone announcements, technology overview pages, and business updates, but withholds detailed plasma parameters (triple product, density, confinement time), energy balance figures, achieved rep rate on Polaris, and any plant-level engineering or cost estimates. The third-party Contrary Research report and DocsLib ARPA-E presentation provide some quantitative data, but these are investor and government grant documents, not engineering design reports.[3]

**Key data gaps limiting this analysis:**
- No published D-He3 fusion yield (all milestones are D-D or D-T intermediate steps)
- No published energy gain (Q value) target for commercial operation
- No published plant-level cost estimate or LCOE model
- No independent techno-economic analysis equivalent to Araiinejad & Shirvan (2025) for tokamaks
- Achieved rep rate on Polaris not disclosed despite operational machine
- No published power plant study (no equivalent of ARIES, ARC, Z-IFE for Helion's architecture)
- Orion's detailed specifications are proprietary despite construction being underway

---
[1] dossier.md §Key Sources — peer-reviewed / academic: Kirtley & Milroy (2023), Comments on Kirtley & Milroy (2026), Slough et al. Nuclear Fusion 51(5) 2011.
[2] helion-milestones-feb2026.md §Key Technical Details and §Orion Specifications.
[3] contrary-research-helion.md §Key Technical Details; docslib-helion-arpa-e-presentation.md §Energy Efficiency.

---

## Section 2: Challenges in Capturing System Function

Helion's LCOE depends on a set of interlocked parameters, most of which are not publicly disclosed. The challenges below are ranked by their impact on LCOE model closure.

### 1. Energy Balance Is Underclosed: Gain and Recirculating Power Unknown (Impact: Blocking)

The fundamental LCOE question for Helion is: for each joule invested in the capacitor bank, how many joules of net electricity are recovered? This requires knowing (a) plasma gain Q_plasma, (b) direct energy recovery efficiency η_rec, and (c) recirculating power fraction for bank recharging and auxiliary systems.

The ARPA-E presentation discloses a partial energy balance: η (= E_delivered/E_plasma) · Gain = 0.2 · 1.2, with η_recovery = 0.7 [1]. This implies that at the ARPA-E design point, 24% of input energy is amplified by fusion and 70% of plasma energy is recovered — suggesting significant recirculating power to maintain operation. Helion's website states that "95% of input energy after each pulse must be recovered" for net electricity generation and claims >95% round-trip recovery in a subscale demonstration. The tension between the 70% recovery in the ARPA-E formula and the >95% claim on the website may reflect different definitions (magnetic energy recovery vs. total round-trip efficiency) or different system configurations. This cannot be resolved from available sources.

> "η (=Ed/Eplasma) · Gain = 0.2 · 1.2 with magnetic energy recovery. Magnetic energy recovery efficiency: η=0.7. Input efficiency target: <$0.03/MJ"
> — docslib-helion-arpa-e-presentation.md, §Energy Efficiency

No commercial-plant Q target is stated anywhere in available sources. The 1.2× plasma gain at the ARPA-E design point is almost certainly not the commercial target — the actual commercial gain requirement depends on the round-trip efficiency of the full electrical cycle, which Helion has not disclosed. This gap is blocking for LCOE model construction.

### 2. Rep Rate Is the Dominant LCOE Output Lever (Impact: Critical)

Like all pulsed fusion concepts, Helion's annual energy output equals (fusion yield per pulse) × (rep rate) × (plant availability). Unlike MagLIF — where the driver is always on standby but targets are destroyed per shot — Helion's coils serve dual duty as plasma compressors and energy recovery inductors, and the capacitor bank charges/discharges cyclically. Rep rate thus directly determines both energy output and the duty cycle of the bank. Small changes in rep rate (1 Hz → 2 Hz) double the energy output from identical capital, having a larger LCOE impact than almost any other parameter.

Trenta operated at ~1 pulse per 10 minutes (~0.002 Hz) — four orders of magnitude below the commercial design point.[2] Polaris targets ~1 Hz, and the ARPA-E presentation specifies 2 Hz at 50 MW as the design point.[3] However, no public data exists on the rep rate actually achieved on Polaris — the 150M°C milestone announcement did not disclose pulse frequency. The jump from ~0.002 Hz (Trenta) to 1–2 Hz (commercial target) is a 500–1,000× increase in repetition speed, with entirely different engineering requirements for bank recharging, coil cooling, FRC formation reliability, and plasma exhaust clearing.

### 3. D-He3 Physics: Temperature Gap and Undemonstrated Fuel Cycle (Impact: Critical)

The current Polaris milestone of 150M°C (13 keV) is an intermediate demonstration step using D-T fuel. Commercial D-He3 operation requires ~200M°C (~17 keV) — a 33% ion temperature increase from the current record.[4] The D-He3 fusion cross-section peaks much higher (~300–500 keV) than D-T (~65 keV), and at operating temperatures around 200 keV, the D-D side reactions that produce He3 are also active. No public data exists on D-He3 plasma behavior in a colliding FRC configuration, and D-He3 fusion has not been demonstrated in any FRC experiment.

The 20× temperature scale-up from the clearest FRC experimental database (Trenta: 8 keV ions) to the D-He3 commercial operating temperature (~17–200 keV) represents the largest single physics extrapolation in this concept's development path, as noted in the handwritten exemplar.[5] This gap is particularly concerning because the ARPA-E gain data (Q ~ 1.2) appears to represent an early design point, and no gain measurements at D-He3-relevant temperatures have been published.

### 4. He3 Breeding Bootstrap: Inventory Buildup Timeline Unknown (Impact: High)

Commercial operation is designed to use only deuterium as external fuel, with He3 self-bred via DD side reactions (50% direct He3 + 50% tritium, which decays to He3 at t½ = 12.3 years).[6] This strategy is elegant but creates a bootstrapping problem: each new plant requires an initial He3 inventory large enough to sustain D-He3 operation while waiting for DD-bred inventory to accumulate. The 12.3-year half-life of tritium means some He3 production is delayed by over a decade. The inventory requirement, DD operation period, and transition timeline are not disclosed.

Global He3 supply is severely constrained. He3 is primarily produced from tritium decay in nuclear weapons programs; the US DOE manages the supply and has rationed it for years due to demand from neutron detectors and medical imaging. Commercial He3 costs have historically ranged from ~$2,000 to >$15,000 per NTP liter, and global production is estimated at ~8 kg/year (predominantly US program reprocessing). If Helion requires even a few kilograms of He3 inventory per plant — a figure that has not been published — sourcing that inventory would represent a significant early-plant cost and a potential fleet deployment bottleneck.

### 5. Capacitor Bank Cost and Lifetime (Impact: High)

The Polaris capacitor bank stores >50 MJ, charged to tens of thousands of volts. At commercial-grade capacitor prices (~$5/J, per the MIF/MagLIF pulsed-power literature [07-maglif analysis §Key Materials and Supply Chain Considerations]), this implies a bank cost of order $250M for Polaris-class hardware. The reactor target is 40 T compression versus Polaris's 15 T+ — requiring more stored energy in the bank and higher field coils. Helion manufactures some capacitors in-house and has demonstrated >1M pulses at subscale with modern high-voltage IGBTs. But commercial operation at 1–2 Hz for 30 years requires ~10⁹ total shots — a 1,000× scale-up from the demonstrated 1M-pulse mark. Bank cost reduction through volume manufacturing (analogous to the SfA white paper argument for MagLIF) is the critical capital cost lever, but no Helion-specific cost targets or manufacturing roadmaps are public.

### 6. No Thermal Cycle — But Direct Conversion Is Unvalidated at Plant Scale (Impact: Medium)

The absence of a steam cycle is Helion's most cited cost advantage: no turbines, no heat exchangers, no Rankine/Brayton system. The handwritten exemplar estimates ~$127M in turbine/BOP savings at the 50 MWe scale.[7] But the flip side is that the direct inductive energy recovery system at 1–2 Hz, 50+ MW, has no precedent. The >95% round-trip efficiency was demonstrated "for over 1 million pulses" in subscale hardware using "modern high-voltage IGBTs."[8] Scaling this to reactor voltage levels, power levels, and pulse counts while maintaining efficiency is not demonstrated. The IGBT switching hardware cost at reactor scale is not characterized.

---
[1] docslib-helion-arpa-e-presentation.md §Energy Efficiency.
[2] helion-website-technology.md §Repetition Rate: "Trenta: ~1 pulse per 10 minutes."
[3] docslib-helion-arpa-e-presentation.md §Power and Repetition: "50 MW at 2 Hz repetition rate."
[4] helion-website-technology.md §Fuel: "D-He3 requires ~200 million degrees C."
[5] handwritten/08-frc-w-direct-conversion.md §Maturity of Key Subsystems and Components: "The 20x temperature scale-up from demonstrated to required is the largest single physics extrapolation."
[6] helion-website-technology.md §Fuel: "DD side reactions produce He3 directly (50%) and tritium (50%) which decays to He3 (t½ = 12.3 yr)."
[7] handwritten/08-frc-w-direct-conversion.md §Quantitative LCOE Model: "not requiring turbines saves $127M."
[8] dossier.md §Energy Capture: "In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs."

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**D-He3 Fusion Plasma at Commercial Conditions — TRL 2**

- **Demonstrated**: D-T fusion at 150M°C (13 keV) on Polaris (January 2026), making Helion the first privately funded company to demonstrate D-T fusion. Trenta demonstrated D-D plasma at 100M°C (8 keV) over >10,000 pulses for 16 months. Plasma temperature progression across prototypes: 5 keV (Grande), 2 keV ions at high density (Venti), 8 keV ions / >1 keV electrons (Trenta), 13 keV (Polaris).[1]
- **On paper only**: D-He3 fusion in a colliding FRC geometry at ~200M°C (~17–200 keV operating window). No published D-He3 plasma operation in any FRC device from any program.
- **Missing at scale**: Demonstration of D-He3 fusion yield at any temperature; triple product measurements at D-He3-relevant conditions; scaling of Q from the ARPA-E estimate (~1.2) to commercially viable levels; compression to the 40 T reactor field needed for D-He3 temperatures.

---

**He3 Self-Breeding Cycle — TRL 2–3**

- **Demonstrated**: DD fusion physics is well-established academically. Helion has demonstrated DD plasma (in early prototype generations). The 50/50 split of DD reactions into He3+n and T+p is textbook physics. Tritium decay to He3 at 12.3-year half-life is well-characterized.[2]
- **On paper only**: Continuous DD operation at rep rate to produce He3 inventory; in-plasma separation of He3, tritium, and unburned deuterium; tritium storage and handling infrastructure within the Helion device loop.
- **Missing at scale**: A working He3 breeding system integrated into the plant; characterization of the DD burn fraction and breeding efficiency per pulse; quantification of the inventory ramp-up timeline; regulatory framework for tritium byproducts during breeding operation (tritium storage invites regulatory burden, as noted in the handwritten exemplar [3]).

---

**Repetitive FRC Formation, Acceleration, and Collision at Plant Scale — TRL 3–4**

- **Demonstrated**: Merging of two FRC plasmoids at >300 km/s confirmed experimentally in multiple prototype generations, documented in Slough et al. (Nuclear Fusion 51(5), 2011). Trenta ran 16 months with >10,000 pulses at low rep rate (~1/10 min). Polaris is operational but publicly reported performance is temperature only — rep rate not disclosed.[4]
- **On paper only**: Rep-rated FRC formation at 1–2 Hz with consistent plasmoid quality; automated formation, acceleration, and collision with high shot-to-shot reliability.
- **Missing at scale**: Coil cooling systems adequate for sustained 1+ Hz operation; FRC velocity and plasmoid size consistency across >10⁸ shots; plasma exhaust (neutral ash, unburned fuel) removal within the ~1-second inter-shot period; failure modes at sustained high rep rate.

---

**Compression to Reactor Field (40 T) — TRL 3**

- **Demonstrated**: >8 T compression on Trenta; 15 T+ is the Polaris target. The ARPA-E presentation specifies 20 T as the ARPA-E experiment design and 40 T as the reactor design.[5]
- **On paper only**: 40 T compression field in an FRC geometry; coil current density and structural integrity at 40 T with aluminum pulsed EM design; magnetic flux compression physics at the reactor scale.
- **Missing at scale**: Aluminum coils designed for 40 T pulses at 1–2 Hz without fatigue failure; energy storage and switching hardware capable of driving 40 T compression at those rep rates; coil lifetime at reactor field and rep rate.

---

**Direct Inductive Energy Recovery at Plant Scale — TRL 4–5**

- **Demonstrated**: >95% round-trip energy recovery demonstrated at subscale for >1M pulses using IGBTs (2015 Helion press release, cited in dossier). The concept — expanding magnetized plasma inducing current in surrounding coils via Faraday's law — is well-understood physics.[6]
- **On paper only**: Energy recovery at reactor voltage, current, and power levels (50+ MW per pulse); integration of IGBT switching with 40 T compression coils; recovery efficiency at 1–2 Hz and 50+ MJ stored energy.
- **Missing at scale**: IGBT (or equivalent power electronics) reliability at 10⁹ switching cycles; efficiency validation at full scale; thermal management of switching losses at 1–2 Hz; capital cost of reactor-scale switching hardware.

---

**Pulsed EM Coil System (Aluminum Coils + Capacitor Bank) — TRL 5–6**

- **Demonstrated**: Polaris has a functional 50 MJ+ capacitor bank charged to tens of kV, driving aluminum electromagnetic coils. Prototype progression across seven generations. Capacitor manufacturing in-house.[7]
- **On paper only**: Full-scale reactor bank at the energy level needed for 40 T compression; IGBT switching reliability at plant scale and rep rate.
- **Missing at scale**: Bank cost at reactor scale; lifetime to 10⁹ shots; integration of charging and discharging circuits without cross-coupling or stability loss.

---

**Plasma Diagnostics and Machine Control — TRL 6–7**

- **Demonstrated**: Polaris operates with 3,800 diagnostics. Real-time FRC formation, velocity, and temperature monitoring shown across multiple prototype generations.[8]
- **Missing at scale**: Closed-loop control for consistent FRC quality at 1–2 Hz; integration of diagnostics into automated shutdown/fault response for 30-year plant operation.

---
[1] helion-prototype-generations.md §Prototype Timeline; helion-milestones-feb2026.md §Key Technical Details.
[2] helion-website-technology.md §Fuel: "50% of DD reactions produce He3 directly, 50% produce tritium."
[3] handwritten/08-frc-w-direct-conversion.md §He3 breeding: "If tritium decay is a path for He3, this can invite a large regulatory burden."
[4] helion-prototype-generations.md §Prototype Timeline; helion-milestones-feb2026.md §Key Technical Details.
[5] docslib-helion-arpa-e-presentation.md §Magnetic Fields: "20 Tesla: ARPA-E experiment compression capability. 40 Tesla: Target reactor compression field."
[6] dossier.md §Energy Capture: "In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses."
[7] helion-website-technology.md §Capacitor Bank; contrary-research-helion.md §In-House Manufacturing.
[8] helion-milestones-feb2026.md §Key Technical Details: "3,800 diagnostics."

---

## Section 4: Key Materials and Supply Chain Considerations

### Helium-3

He3 is the scarcest material in Helion's supply chain, and its availability during the pre-breeding phase represents the binding constraint on fleet deployment speed. He3 is not commercially produced; global supply derives almost entirely from tritium decay in nuclear weapons programs (predominantly US DOE). The US has rationed He3 since ~2010 due to competing demand from radiation detection (homeland security), neutron scattering instruments, and medical imaging (MRI polarization). Global production is estimated at ~8 kg/year. Commercial prices have ranged from ~$2,000 to >$15,000 per NTP liter (~0.125 g/L at STP), equivalent to roughly $16,000–$120,000/g.

Helion's long-term strategy requires only deuterium as external fuel, with He3 self-bred from DD side reactions.[1] However, each new plant requires an initial He3 inventory sufficient to sustain D-He3 ignition attempts while DD breeding accumulates. Since 50% of He3 comes via tritium decay at 12.3-year half-life, significant He3 inventory can only be built up over many years of DD operation. The size of this startup inventory and the timeline to self-sufficiency are not public. Helion's fleet deployment rate is fundamentally limited by either external He3 supply (at high cost) or the time needed to breed inventory at each new plant (at low marginal cost but multi-year delay).

Helion has confirmed it possesses licensed tritium for Polaris D-T experiments — making it the first private company with such regulatory approval.[2] This does not directly address the He3 supply question but confirms Helion is engaging with tritium inventory issues early.

### Deuterium

Deuterium is extracted from ordinary water (ocean: 33 mg D/L) by isotopic enrichment. Global production capacity is adequate for any plausible fusion fleet. Commercial price is approximately $500–$1,000/kg, making fuel cost for a deuterium-only plant essentially negligible at commercial scale — this is one of Helion's key cost advantages.[3] No supply chain constraint.

### Aluminum (Coil Material)

Helion uses aluminum electromagnetic coils, not superconductors. Aluminum is the third most abundant element in Earth's crust with ~70 million tonnes/year global production and mature supply chains. Coil construction uses aluminum wire/rod at commodity pricing (~$2–$3/kg). No supply chain constraint. This is a major advantage relative to REBCO-dependent concepts (01-hts-compact-tokamak, 21-spherical-tokamak-hts), where global REBCO tape production (~few thousand km/year) would need to scale by 1–2 orders of magnitude per plant.[4]

### High-Voltage Capacitors and IGBT Switches

The capacitor bank uses "thousands of high-voltage pulsed capacitors" charged to tens of thousands of volts.[5] Helion manufactures some capacitors in-house; others are purchased externally. At current commercial capacitor prices of ~$5/J (per pulsed-power industry estimates, consistent with the MagLIF analysis [07-maglif analysis §Key Materials]), the Polaris bank (>50 MJ) represents ~$250M at component cost — though Helion's in-house manufacturing and bulk procurement may significantly reduce this. For commercial plants, the analogy to MagLIF applies: capacitor costs must decline substantially (potentially to ~$0.50/J or better) through volume manufacturing to reach acceptable $/kWe installed capital. IGBT switching hardware is commercially available but its lifetime at 10⁹ cycles (1 Hz for 30 years) is an open question; high-cycle-life designs are a manufacturing challenge.

Contrary Research lists supply chain as "the main potential risk" identified by Helion management, specifically calling out quartz tubes and high-voltage capacitors.[6]

### Copper (Cabling)

The Polaris coaxial cable system uses copper, aluminum, and custom alloys totaling ~720 miles of cable.[7] At reactor scale, copper demand is non-trivial but far below the scale that would stress global copper supply (~25 million tonnes/year). No material constraint.

### No Tritium Breeding Blanket Required (at commercial D-He3 operation)

Helion's D-He3 fuel cycle explicitly avoids the tritium breeding blanket that is the most technologically uncertain component of D-T tokamak designs (TRL ~3–4 per the 01-hts-compact-tokamak and 07-maglif analyses). There is no FLiBe, no lithium enrichment, no beryllium requirement, and no 14 MeV neutron wall-loading problem. This is a major structural cost and supply chain advantage for Helion relative to all D-T concepts. The neutron flux from D-He3 (primarily 2.45 MeV DD neutrons rather than 14.1 MeV D-T neutrons) is much lower in energy and easier to shield, with ~1 m of borated polyethylene and concrete — similar to hospital particle beam shielding.[8]

---
[1] helion-website-technology.md §Fuel: "Only deuterium (from water) needed as external input."
[2] helion-milestones-feb2026.md §Key Technical Details: "Helion received regulatory approval to possess and use tritium."
[3] Deuterium price and water abundance are well-established; no specific source needed.
[4] For REBCO constraints see 01-hts-compact-tokamak analysis §Key Materials and Supply Chain Considerations.
[5] helion-website-technology.md §Capacitor Bank.
[6] contrary-research-helion.md §In-House Manufacturing: "Supply chain identified as 'main potential risk.'"
[7] helion-website-technology.md §Magnets / Coils: "~720 miles total" of coaxial cables.
[8] helion-website-technology.md §Neutron Management; dossier.md §Neutron Management.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (Orion) | 50 MWe+ | helion-milestones-feb2026.md §Orion Specifications | high | First commercial plant; "after one-year ramp-up period" |
| Net electrical output (future) | 500 MWe | helion-website-technology.md §Power Output | medium | Nucor partnership; not a published design study |
| Plasma temperature (Polaris, achieved) | 150M°C (13 keV) | helion-milestones-feb2026.md §Key Technical Details | high | D-T interim milestone; Jan 2026 |
| Plasma temperature (D-He3 required) | ~200M°C (~17–200 keV window) | helion-website-technology.md §Fuel | high | Helion stated threshold; actual operating window not specified |
| Plasma temperature (Trenta, achieved) | 100M°C (8 keV ions, >1 keV electrons) | helion-prototype-generations.md §Prototype Timeline | high | |
| FRC velocity | >300 km/s | docslib-helion-arpa-e-presentation.md §Fusion Approach | high | Both plasmoids; collision kinetic energy → ion thermal |
| Formation plasma density | 1×10²¹ m⁻³ | docslib-helion-arpa-e-presentation.md §Plasma Parameters | medium | ARPA-E design point; may not reflect Polaris |
| Compressed plasma density target | 1×10²³ m⁻³ | docslib-helion-arpa-e-presentation.md §Plasma Parameters | medium | 100× compression factor |
| Compression field (Trenta) | >8 T | helion-prototype-generations.md §Prototype Timeline | high | |
| Compression field (Polaris target) | 15 T+ | helion-website-technology.md §Magnets / Coils | high | Target; achieved value not stated |
| Compression field (ARPA-E experiment) | 20 T | docslib-helion-arpa-e-presentation.md §Magnetic Fields | medium | |
| Compression field (reactor target) | 40 T | docslib-helion-arpa-e-presentation.md §Magnetic Fields | medium | |
| Plasma lifetime per pulse | >1 ms | helion-website-technology.md §Plasma Parameters | high | |
| Repetition rate (Trenta) | ~0.002 Hz (1/10 min) | helion-website-technology.md §Repetition Rate | high | Demonstrated |
| Repetition rate (Polaris target) | ~1 Hz | helion-website-technology.md §Repetition Rate | medium | Target, not demonstrated publicly |
| Repetition rate (design point) | 2 Hz | docslib-helion-arpa-e-presentation.md §Power and Repetition | medium | 50 MW at 2 Hz per ARPA-E presentation |
| Capacitor bank energy (Polaris) | >50 MJ | helion-website-technology.md §Capacitor Bank | high | |
| Capacitor bank voltage | Tens of kV | helion-website-technology.md §Capacitor Bank | high | |
| Cable length | ~720 miles total | helion-website-technology.md §Magnets / Coils | medium | Polaris scale; coaxial cables with copper, aluminum, custom alloys |
| Direct energy recovery efficiency (subscale demo) | >95% round-trip | dossier.md §Energy Capture | medium | Subscale; 1M pulses at unspecified voltage/power |
| Direct energy recovery efficiency (Contrary claim) | 85–95% | contrary-research-helion.md §Energy Recovery | medium | Range stated without test conditions |
| Magnetic energy recovery efficiency η (ARPA-E) | 0.7 | docslib-helion-arpa-e-presentation.md §Energy Efficiency | low | May use different definition than >95% claim |
| Plasma gain (ARPA-E design point) | ~1.2 | docslib-helion-arpa-e-presentation.md §Energy Efficiency | low | Early design point; η × Gain = 0.2 × 1.2; not the commercial target |
| D-He3 reaction energy | 18.3 MeV (3.6 MeV α + 14.7 MeV p) | helion-website-technology.md §Fuel | high | Well-established nuclear physics |
| Neutron energy fraction (D-He3) | ~5% | helion-website-technology.md §Fuel | medium | Helion claim; depends on D-D side reaction rate; schema default ~10% |
| Neutron energy (from D-D side reactions) | 2.45 MeV | dossier.md §Neutron Management | high | Much lower than 14.1 MeV D-T |
| Shielding requirement | ~1 m borated poly/concrete | helion-website-technology.md §Neutron Management | medium | Comparable to hospital particle beam facility |
| Input energy cost target | <$0.03/MJ | docslib-helion-arpa-e-presentation.md §Energy Efficiency | medium | Driver economics target |
| LCOE target (third-party estimate) | 1–6 ¢/kWh | dossier.md §Key Sources (Thunder Said Energy, 2022) | low | Informal estimate; no published model; 2022 vintage |
| Capacitor bank cost estimate (Polaris scale) | ~$250M | [inferred: >50 MJ × ~$5/J; bank energy from helion-website-technology.md §Capacitor Bank; unit cost from pulsed-power industry estimates as cited in 07-maglif analysis §Key Materials] | low | $5/J is current commercial capacitor price; Helion's in-house manufacturing may reduce significantly |
| Turbine/BOP savings vs thermal cycle | ~$127M (50 MWe) | [analogue: handwritten/08-frc-w-direct-conversion.md §Quantitative LCOE Model; first-pass estimate for 50 MWe scale] | low | No detailed cost breakdown in available sources |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion power per pulse / Q_plasma (commercial target) | proprietary | blocking | Not disclosed; required to close any energy balance model |
| Recirculating power fraction | proprietary | blocking | Bank recharging efficiency and auxiliary power load unknown |
| He3 startup inventory requirement | proprietary | blocking | Determines bootstrap cost and fleet deployment rate |
| He3 breeding rate per unit time | proprietary | blocking | DD operation efficiency and He3 production rate not published |
| Plant capital cost (Orion or any design) | proprietary | blocking | No cost estimate published; Orion under construction |
| O&M cost estimate | truly-unknown | important | No analogous system exists; cannot estimate from published sources |
| Capacity factor target | proprietary | important | Depends on bank/coil maintenance schedule; not published |
| Coil/bank lifetime (shots to replacement) | proprietary | important | Scales directly to per-shot capital cost amortization |
| Fusion yield per pulse | proprietary | important | Basis for energy balance; not published for any prototype |
| Achieved rep rate on Polaris | proprietary | important | Most critical near-term data point; not released with 150M°C milestone |
| First wall / plasma-facing component lifetime | proprietary | important | Not applicable for neutron-facing structure (reduced neutron flux), but coil integrity matters |
| IGBT switching hardware cost at reactor scale | not-yet-sourced | important | Pulsed power electronics cost literature may have analogues |
| He3 commercial inventory (global, available to Helion) | not-yet-sourced | important | US DOE He3 supply data is public; needs dedicated research |
| Tritium inventory during DD breeding phase | proprietary | nice-to-have | Regulatory and storage cost implications |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Commercial Q value / plasma gain target not published | S1, S2, S5 | proprietary | blocking | Direct disclosure required; Helion ARPA-E documents may have more context |
| 2 | Recirculating power fraction and full energy balance not disclosed | S2, S5 | proprietary | blocking | Derivable from η_recovery × Q if both were known; requires both |
| 3 | He3 startup inventory requirement per plant not published | S2, S4, S5 | proprietary | blocking | Could be derived from plasma volume, density, D-He3 ratio, and shot count; needs Q data |
| 4 | He3 breeding rate per unit time not characterized | S2, S3, S5 | proprietary | blocking | Depends on DD fusion rate at rep rate; requires Q and rep rate data |
| 5 | Orion plant capital cost not disclosed | S1, S5 | proprietary | blocking | Construction underway; SEC filings or DOE milestone reports may eventually surface numbers |
| 6 | Achieved rep rate on Polaris not reported | S1, S2, S3, S5 | proprietary | important | Helion's most critical near-term data point; could be inferred from power consumption measurements |
| 7 | Capacity factor target for Orion not published | S5 | proprietary | important | No analogous pulsed direct-conversion system to derive from |
| 8 | Coil and capacitor bank lifetime (shots to replacement) | S3, S5 | proprietary | important | Determines per-shot capital cost; IGBT literature provides partial analogy |
| 9 | D-He3 fusion yield (any conditions) not demonstrated | S1, S3 | truly-unknown | important | No FRC program anywhere has published D-He3 results at relevant temperatures |
| 10 | O&M cost estimate — no analogous system for benchmarking | S5 | truly-unknown | important | No published O&M model for a direct-conversion pulsed FRC plant |
| 11 | IGBT switching hardware cost at reactor scale | S4, S5 | not-yet-sourced | important | Power electronics literature and industrial IGBT pricing could bound this |
| 12 | Global He3 supply accessible to Helion | S4 | not-yet-sourced | important | US DOE He3 program reports are public; needs dedicated research |
| 13 | Fusion power per pulse / neutron yield measurements on Polaris | S3, S5 | proprietary | important | Even qualitative neutron count data would constrain energy balance |
| 14 | Compression field actually achieved on Polaris (15 T+ target stated, achieved not reported) | S3 | proprietary | nice-to-have | Would narrow the gap between Trenta (8 T) and reactor (40 T) |
| 15 | Neutron energy fraction at D-He3 operating temperature | S4 | not-yet-sourced | nice-to-have | Physics papers on D-He3 reaction rates vs temperature could bound the 5% vs 10% discrepancy |

---

## Section 7: Cross-Concept Notes

This analysis references three approved prior analyses: 01-hts-compact-tokamak (Commonwealth Fusion Systems), 07-maglif (Pacific Fusion / Fuse Energy), and 21-spherical-tokamak-hts (Tokamak Energy). The most relevant cross-concept comparison is with 07-maglif.

### Shared with 07-maglif: Pulsed Operation Economics Framework

Both Helion and MagLIF are pulsed fusion concepts where annual energy output = (yield per pulse) × (rep rate) × (availability), and rep rate is the dominant LCOE leverage point. The basic framework from the MagLIF analysis — that standard fusion LCOE formulations treat capacity factor as availability-only, misrepresenting pulsed dynamics — applies equally to Helion.

**Critical divergence**: MagLIF destroys a target (liner, RTL) per shot, creating a per-shot consumable cost floor of ~$0.70–$1/shot at scale with no analogue in magnetic confinement. Helion's coils serve as both plasma compressor and energy recovery inductor and are **not** destroyed per shot. This is a significant structural advantage: Helion's operating cost structure resembles a magnetic confinement device (capital amortized over lifetime shots) rather than an IFE device (capital + per-shot consumables). Once the bank and coils have acceptable lifetime, Helion's O&M cost drivers are maintenance, deuterium fuel (negligible cost), and periodic hardware replacement — not per-shot consumables.

### Shared with 07-maglif: No HTS Requirement

Both Helion and MagLIF use resistive coils (aluminum and copper, respectively) rather than superconducting magnets. This eliminates the REBCO supply chain bottleneck that gates 01-hts-compact-tokamak and 21-spherical-tokamak-hts. At the fleet scale, REBCO production would need to increase by 1–2 orders of magnitude (from current ~few-thousand km/year to >5,000 km per reactor per year for HTS concepts). Helion and MagLIF avoid this constraint entirely, which is a meaningful deployment-speed advantage in a world where multiple fusion concepts commercialize simultaneously.

### Shared with 07-maglif: Capacitor Bank Cost Challenge

The pulsed EM driver in both concepts requires capacitors at a price of ~$5/J today, with commercial viability requiring ~$0.50/J or better. At Polaris's >50 MJ bank, today's pricing implies ~$250M in capacitors alone — manageable for a single device but challenging at plant scale with higher stored energy for 40 T compression. The MagLIF analysis (07-maglif §Key Materials) and SfA White Paper identify this as the central manufacturing scale challenge. The same dynamic applies to Helion, though Helion's in-house manufacturing strategy directly addresses it.

### Diverges from 07-maglif: No Per-Shot Consumables, No Blanket, No Thermal Cycle

Helion eliminates three major cost categories that MagLIF must address:
1. **No per-shot consumables** — coils and bank are capital items, not operating costs
2. **No tritium breeding blanket** — D-He3 eliminates the TRL ~2-3 blanket subsystem that MagLIF shares with all D-T concepts
3. **No thermal conversion cycle** — direct inductive energy recovery replaces a ~$100M+ steam plant

These three divergences are the basis for the handwritten analyst's estimate of ~4 ¢/kWh in the optimistic case. The pessimistic case (~20 ¢/kWh) assumes HTS magnets are required — but this conflicts with all available sources confirming aluminum coils.

### Diverges from 01-hts-compact-tokamak and 21-spherical-tokamak-hts: No Published TEA

The most analytically limiting gap relative to the tokamak concepts is the complete absence of independent TEA work for Helion. Araiinejad & Shirvan (2025) provides a quantitative foundation for CFS ARC-class plants; Foster et al. (2024) and Hidalgo-Salaverri et al. (2025) provide frameworks for spherical tokamaks. No equivalent study exists for Helion. An LCOE model for Helion must be built from first principles using the sparse public data, with much larger uncertainty bounds than for any tokamak concept.

### Reused Assumptions

- Capacitor unit cost (~$5/J current commercial pricing): adopted from 07-maglif analysis §Key Materials and Supply Chain Considerations, citing pulsed-power industry context.
- Tokamak BOP/turbine cost (~$127M at 50 MWe): adopted directionally from handwritten/08-frc-w-direct-conversion.md §Quantitative LCOE Model as a reference for the value of Helion's turbine-free design.

---

## Section 8: Sources

**1. Helion Energy — Technology Website and Articles** (primary technical source)
- Covers: confinement concept, fuel cycle, energy recovery, magnets, prototypes, commercial plans
- Key URLs documented in dossier.md §Key Sources
- Path: helion-website-technology.md

**2. Helion Energy — Fusion Milestones Announcement (February 2026)**
- Author: Helion Energy
- Date: February 2026
- Covers: Polaris 150M°C achievement, D-T fusion milestone, Orion specifications, construction timeline
- Path: helion-milestones-feb2026.md

**3. Helion Energy — ARPA-E Presentation (DocsLib)**
- Title: "Helion Energy — David Kirtley CEO/Project Lead — 20 Tesla ARPA-E experiment, 40 Tesla Reactor"
- Source URL: https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor
- Covers: Magnetic field targets (20 T/40 T), design point (50 MW at 2 Hz), plasma parameters, energy efficiency formula (η × Gain = 0.2 × 1.2), input cost target
- Path: docslib-helion-arpa-e-presentation.md

**4. Contrary Research — Helion Energy Company Report**
- Author: Contrary Research
- Source URL: https://research.contrary.com/company/helion
- Covers: Magnet materials ("regular aluminum magnets," CEO direct quote), energy recovery efficiency range (85–95%), supply chain risk identification, Microsoft PPA terms, rep rate characterization
- Path: contrary-research-helion.md

**5. Helion Prototype Generations (compiled from Wikipedia and web sources)**
- Date fetched: 2026-03-07
- Covers: Seven prototype generations (Grande through Polaris), FRC velocities, published research bibliography (Votroubek/Slough 2008, Slough/Votroubek/Pihl 2011, Kirtley IEEE SOFE 2021, Kirtley & Milroy J. Fusion Energy 2023), LANL/MSNW heritage
- Path: helion-prototype-generations.md

**6. Slough, J., Votroubek, G., Pihl, C. (2011). "Creation of a High-Temperature Plasma through Merging and Compression of Supersonic Field-Reversed Configuration Plasmoids." *Nuclear Fusion* 51(5), 053008.**
- Foundational peer-reviewed paper from Helion founders; provides physics basis for FRC merging/compression approach
- DOI: 10.1088/0029-5515/51/5/053008
- Cited in: dossier.md §Key Sources, helion-prototype-generations.md §Published Research

**7. Kirtley, D. & Milroy, R. (2023). "Fundamental Scaling of Adiabatic Compression of FRC Thermonuclear Fusion Plasmas." *Journal of Fusion Energy* 42.**
- Covers FRC compression scaling theory; peer-reviewed
- Cited in: dossier.md §Key Sources

**8. Phase 1a Dossier** (comprehensive research synthesis)
- Author: Phase 1a research iterations 1–2 (2026-03-07)
- Covers: All 12 differentiation table columns at high confidence, source citations for each
- Path: /exploration/phase_1a/research/08-frc-w-direct-conversion/dossier.md

**9. Handwritten Exemplar: FRC w/ Direct Conversion (First-Pass Analysis)**
- Author: Project team (Damien / Mallory attribution not explicit)
- Covers: Qualitative LCOE assessment, back-of-envelope cost estimates, key risk identification; includes 1costingfe model output (~4 ¢/kWh baseline, ~20 ¢/kWh with HTS)
- Path: /exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md

**10. Thunder Said Energy — Helion (2022)**
- Third-party analyst report; covers LCOE target range (1–6 ¢/kWh), plant size range (50–200 MWe modular)
- Referenced in dossier.md §Key Sources
- Note: 2022 vintage; predates Polaris milestones; treat LCOE range as aspirational

**11. D1+ Analysis: MagLIF (07-maglif)**
- Status: Approved
- Used for: Pulsed operation economics framework, capacitor unit cost analogy (~$5/J), per-shot consumable cost structure comparison
- Path: /exploration/concept_analysis/analyses/07-maglif/analysis.md

**12. D1+ Analysis: HTS Compact Tokamak (01-hts-compact-tokamak)**
- Status: Approved
- Used for: REBCO supply chain context (baseline for no-HTS advantage comparison), TEA methodology benchmark
- Path: /exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md
