# D1+ Analysis: Laser ICF — Liquid Jet Target (D-D)

**Concept**: Plasmonic nanoshell IFE — femtosecond laser on D2O-filled gold nanoshells delivered via continuous liquid jet, D-D fuel
**Company**: Cortex Fusion Systems (New York, NY — founded 2021, $2.6M funding)
**Confinement Family**: IFE (non-implosion variant)
**Operation Mode**: Pulsed (kHz to MHz rep rate — projected)

---

## Section 1: Availability of Data

**Rating: Opaque**

Cortex Fusion Systems is one of the least transparent and least validated concepts in the IFE landscape. The public record consists of: one theoretical preprint, one earlier single-author arXiv paper from the company's founder, a company website, and one independent paper from Cambridge (not affiliated with Cortex) demonstrating the general feasibility of kHz-rate liquid-target D-D fusion on entirely different hardware. No experimental results from Cortex have been published. No machine or plant design has been disclosed. No cost estimates, energy balance, or system design have appeared anywhere in the public record.

**Primary sources and their limitations:**

> "Systems, methods, and underlying principles [for nuclear fusion using plasmonic field enhancement —paraphrase] are the intellectual property of Cortex Fusion Systems, Inc."
> — arxiv-2503-nanoshell-paper.md, §IP Notice

The core technical reference is arXiv:2503.15531 (Kharzeev, Levitt, Trallero-Herrero, submitted February 2025, revised April 2025), a theoretical preprint titled "Fusion in a Nanoshell: Harnessing Plasmonic Fields for Nuclear Reactions." It presents the physics mechanism and projects reactor-scale parameters but acknowledges "many practical challenges exist" without detailing them. The paper has not yet appeared in a peer-reviewed journal as of this writing.[1]

The 2023 Levitt arXiv preprint (arXiv:2308.07417) establishes the quantum-control framing for the company's laser architecture but provides no specific reactor engineering.[2]

The Cortex Fusion Systems website (accessed March 2026) provides a technology overview, describes the liquid jet delivery mechanism, kHz rep rate, and OAM laser approach, but discloses no quantitative parameters beyond a $2.6M funding figure and a claim to be "building the first electricity-producing fusion reactor."[3]

The Cambridge kHz paper (High Power Laser Science and Engineering, 2024) demonstrates that kHz-rate laser-driven D-D fusion on thin liquid sheets is physically achievable — but at ~10^5 n/s, using a conventional relativistic-intensity Ti:sapphire laser (5×10^18 W/cm²) with no nanoshells. This paper is independent of Cortex and uses a fundamentally different mechanism; it validates the general liquid-target concept but not Cortex's plasmonic approach.[4]

**Key data gaps limiting this analysis:**
- No experimental data from Cortex (zero published fusion results)
- No energy capture or conversion architecture disclosed
- No neutron management, blanket, or chamber design disclosed
- No capital cost estimates or plant engineering
- No peer review of primary technical claims (preprint only)
- Anomalous energy-per-fusion calculation (3333 MeV vs. standard ~3.65 MeV/event) unresolved
- No third-party assessment or independent techno-economic analysis exists

---
[1] arxiv-2503-nanoshell-paper.md, §What's NOT Addressed: "Many practical challenges exist" — acknowledged but not detailed
[2] arxiv-2308-levitt-quantum-control.md, §Summary — framework paper, no reactor engineering
[3] cortex-fusion-website.md, §Status — "currently building the first electricity-producing fusion reactor"
[4] kHz-liquid-sheet-fusion-paper.md, §Key Technical Details — 1 kHz, ~10^5 n/s demonstrated on liquid D2O sheet

---

## Section 2: Challenges in Capturing System Function

LCOE modeling for this concept is fundamentally blocked by missing information at every level of the system hierarchy. The challenges below are ranked by impact.

### 1. No Energy Capture Architecture (Impact: Blocking)

This is not a modeling uncertainty — it is a structural absence. No Cortex source discloses any method for converting the energy released by D-D fusion into electricity. D-D fusion produces a mix of charged particles (T, He-3, protons) and neutrons (2.45 MeV). Direct conversion could in principle recover energy from the charged-particle branch, but no architecture has been described. Thermal conversion would require a blanket/heat exchanger of some kind, also undisclosed. Without an energy capture method, it is impossible to estimate the energy conversion efficiency (η_conv), net electrical output (P_net), or the cost of the energy conversion subsystem — which are foundational inputs to any LCOE calculation.[1]

### 2. Extraordinary Physics Claims Not Experimentally Validated (Impact: Blocking)

The projected reactor parameters — Q~100, 10^19 n/s neutron flux — are derived entirely from the theoretical model in arXiv:2503.15531. The closest independent experimental analogue achieves 10^5 n/s (Cambridge, 2024), which is 14 orders of magnitude below the projected flux (note: the paper itself claims "nine orders" compared to high-flux fission devices at ~10^10 n/s; the Cambridge kHz result at 10^5 n/s is used here as the closest experimental analogue). The claimed plasmonic field amplification from ~10^9 to ~10^11 V/cm inside nanoshells, and the resulting deuteron acceleration to ~25 keV equivalent energy, have not been demonstrated experimentally. Until these physics claims are validated at even laboratory scale, all downstream LCOE estimates rest on a theoretical foundation with no empirical support.[2]

An additional anomaly compounds this concern: the paper reports 3333 MeV of energy per D-D fusion event — approximately 1000× the standard value of ~3.65 MeV. Standard D-D produces either He-3 + n (3.27 MeV) or T + p (4.03 MeV), and secondary reactions (D + T → He-4 + n, 17.6 MeV; D + He-3 → He-4 + p, 18.3 MeV) can boost total energy per initial D-D event, but not by three orders of magnitude. The paper does not explain this figure. If it reflects a calculation error, the claimed Q~100 is unreliable. If it reflects a different physics claim (e.g., a chain of secondary reactions in the dense nanoshell environment), it is extraordinary and unverified.[3]

### 3. Nanoshell Delivery Rate at Scale (Impact: High)

The reactor scenario in arXiv:2503.15531 requires 1 million nanoshells ignited per pulse at 1 MHz, implying 10^12 nanoshell delivery events per second. At ~100 nm radius gold nanoshells, this represents on the order of ~100 grams of gold per second in the target stream (extremely rough order of magnitude — full mass flow depends on fill fraction). The paper describes a "continuous liquid jet" as the delivery mechanism, but:
- Gold nanoshell synthesis at industrial scale is not characterized in any Cortex source
- Nanoshell recovery, recycling, or disposal is not addressed
- Liquid jet velocity, pressure, and geometry requirements at MHz rep rates are not disclosed

The kHz liquid sheet paper (Cambridge, 2024) demonstrates stable sub-micrometer liquid targets at 1 kHz, providing partial support for liquid-jet delivery at moderate rep rates, but does not involve nanoshells.[4]

### 4. D-D Fuel Cycle and Neutron Management (Impact: High)

D-D fuel cycle is simpler than D-T in that no tritium breeding or supply is required — heavy water (D2O) is the fuel medium and is available at ~$600/kg from CANDU reactor operations. However, D-D is not aneutronic: 50% of D-D reactions produce 2.45 MeV neutrons. At the projected 10^19 n/s, a commercial plant would face a neutron flux similar in magnitude to large D-T facilities. Neutron management — shielding, blanket, activation of structural materials — is completely unaddressed in any Cortex source. The dossier notes this under "neutron management: heavy shielding, low confidence" but the company has not disclosed any approach.[5]

Unlike D-T concepts, the absence of tritium breeding simplifies one dimension of the neutron economy, but shielding mass, activation products, and structural material selection are still required for a commercial facility. This gap is important: it affects structural capital costs, maintenance access, and plant regulatory classification.

### 5. Scaling from Laboratory to Reactor: Factor of 10^14 (Impact: High)

The demonstrated experimental baseline for this concept family (Cambridge, 2024) is ~10^5 n/s from a kHz liquid-target system. Cortex's projected commercial reactor target is 10^19 n/s — a 14-order-of-magnitude increase in neutron production. Even if we accept the plasmonic enhancement physics, the scaling pathway involves:
- Validated plasmonic enhancement in nanoshells (not yet demonstrated)
- Nanoshell delivery at MHz rates (not demonstrated)
- Integration of millions of simultaneous nanoshell events per pulse (not demonstrated)
- Energy gain > 1 (not demonstrated in any laser ICF system outside NIF)

For comparison, NIF achieved ignition after decades of development starting from a concept with vastly more validated prior experimental work.

### 6. Capital Cost Estimation Without Analogues (Impact: Moderate)

Even if the physics were validated, cost modeling would face unusual challenges. The dominant driver technology — commercially available femtosecond lasers at ~1 μm with OAM at kHz rates — has no established cost-per-watt analogues at power-plant scale. Femtosecond laser costs are typically $100k-$1M per system for scientific instruments; scaling to the power levels needed for fusion is entirely uncharacterized. The nanoshell target factory, liquid-jet nozzle system, and beam-focusing optics also have no cost precedents.

---
[1] dossier.md, §Energy Capture: "No disclosed energy conversion method"
[2] kHz-liquid-sheet-fusion-paper.md, §Key Technical Details — 10^5 n/s baseline; arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters — 10^19 n/s projected
[3] arxiv-2503-nanoshell-paper.md, §Fusion Parameters — "Energy per D-D fusion: 3333 MeV (note: standard D-D is 3.27 MeV...)"
[4] arxiv-2503-nanoshell-paper.md, §Projected Reactor Parameters — "1 MHz rep rate, 1 million nanoshells ignited per pulse"; kHz-liquid-sheet-fusion-paper.md, §Key Technical Details — "Sub-micrometer scale target is extremely stable and can operate at kHz or above"
[5] dossier.md, §Neutron Management — "Not addressed by any Cortex source... 10^19 n/s neutron flux...would require substantial shielding infrastructure"

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature.

---

**Plasmonic Nanoshell Fusion — TRL 1**
- **Demonstrated**: Theoretical mechanism described in arXiv:2503.15531. Plasmonic field enhancement in gold nanoshells is a well-established nanophotonics phenomenon in other contexts (cancer treatment, surface-enhanced Raman spectroscopy). Its application to nuclear fusion is the novel claim — not yet experimentally demonstrated by any group.
- **On paper only**: The full mechanism — laser → plasmonic field amplification → deuteron acceleration → D-D fusion above threshold — exists only in the theoretical paper. No experimental measurement of fusion-relevant deuteron energies inside nanoshells has been published.
- **Missing at scale**: Any laboratory demonstration at any fusion-relevant parameters. This subsystem has not entered experimental validation. The TRL is 1 (basic principles observed in nanophotonics; application to fusion is a new concept).

---

**Energy Capture and Conversion — TRL 0**
- **Demonstrated**: Nothing. No energy capture architecture has been described by Cortex in any source.
- **On paper only**: Nothing. This subsystem does not exist even as a design concept in the available literature.
- **Missing at scale**: Everything — the architecture, efficiency target, materials, and cost. This is the most critical gap in the entire system. It is not possible to assign a TRL above 0 for a subsystem that has not been conceived in any disclosed form.

---

**Nanoshell Target Delivery (Liquid Jet) — TRL 2–3**
- **Demonstrated**: General liquid-jet D2O target delivery at kHz rates demonstrated by Cambridge group (2024) — thin (<1 μm) D2O sheets from intersecting 25 μm cylindrical jets, stable operation at 1 kHz verified.[1] This is not Cortex hardware.
- **On paper only**: Cortex's specific implementation — liquid D2O filled with suspended gold nanoshells, delivered at kHz-to-MHz rates with sufficient spatial precision to overlap with femtosecond laser focal spot. The gold nanoshell suspension chemistry and stability in a flowing jet are not characterized.
- **Missing at scale**: MHz-rate nozzle performance with nanoshell-laden fluid; nanoshell synthesis at scale; jet replacement and recovery systems; interaction between the jet and post-shot plasma debris; fluid dynamics at target-relevant densities and geometries.

---

**Femtosecond Laser Driver (Off-the-Shelf Component) — TRL 5–6**
- **Demonstrated**: Commercial femtosecond lasers at ~1 μm wavelength, 3–40 fs pulse duration, kHz rep rates exist (e.g., Ti:sapphire systems used in the Cambridge kHz paper at 8 mJ/pulse, 1 kHz).[2] Orbital angular momentum (OAM) beam generation in laboratory settings is well-established.
- **On paper only**: Integration of commercial laser systems into a fusion power plant context. Average power scaling to levels needed for MW-class fusion output. OAM at high average power for inverse Faraday effect magnetic field generation at kilo-Tesla scale.
- **Missing at scale**: Wall-plug-to-beam efficiency at fusion-relevant average power; optics degradation under repeated plasma debris exposure; cost at MW-class average power; laser lifetime and replacement schedule in an operating reactor environment.

---

**Neutron Shielding and Activation Management — TRL 2 (Design Study Level)**
- **Demonstrated**: D-D neutron shielding physics is well-understood from neutron source applications and accelerator facilities. 2.45 MeV neutron cross-sections and material activation data exist.
- **On paper only**: No Cortex-specific design or shielding concept. Generic D-D neutron sources (e.g., industrial neutron generators) provide some analogue.
- **Missing at scale**: A shielding design for 10^19 n/s (projected) at plant scale. This exceeds all existing D-D neutron sources by many orders of magnitude. Structural material selection, activation inventory management, remote handling design — none exists for this concept.

---

**Balance of Plant — TRL N/A (No Architecture)**
- **Demonstrated**: Conventional steam cycle / Rankine cycle BOP is well-developed for other heat sources.
- **On paper only**: Nothing specific to Cortex.
- **Missing at scale**: Cannot assess — BOP design requires knowing the energy capture architecture, thermal power, coolant type, and operating temperature, none of which have been specified.

---
[1] kHz-liquid-sheet-fusion-paper.md, §Key Technical Details — "Sub-micrometer scale target is extremely stable and can operate at kHz or above"; laser: "1-kHz Ti:sapphire laser, 8 mJ, 40 fs pulses"
[2] kHz-liquid-sheet-fusion-paper.md, §Key Technical Details — "Laser: 1-kHz Ti:sapphire laser, 8 mJ, 40 fs pulses; Intensity: ~5×10^18 W/cm²"

---

## Section 4: Key Materials and Supply Chain Considerations

### Heavy Water (D2O) — Fuel

Heavy water is the fuel medium and is commercially available from CANDU reactor operations. The current world supply is substantial — roughly 7,000–8,000 tonnes in storage from CANDU operations globally, with production capacity of several hundred tonnes per year. At the scale of a power plant, D2O consumption depends entirely on the target mass per pulse and rep rate, neither of which is disclosed. Even at aggressive consumption rates, D2O supply is unlikely to be a binding constraint for early deployment.[1] Cost is approximately $300–$600/kg, which would contribute to operating costs but is not a showstopper at reasonable consumption rates.

No tritium supply or breeding is required for a D-D fuel cycle, eliminating the most critical supply chain constraint in D-T concepts. This is a genuine advantage over D-T IFE and MFE.

### Gold for Nanoshells

Gold nanoshells are the core target element. The paper specifies gold with ~100 nm radius thin shells (thickness ≤ skin depth, ~25 nm at optical frequencies). At 1 million nanoshells per pulse at 1 MHz, and assuming each nanoshell weighs approximately:

m ≈ ρ_Au × 4π × R² × δ ≈ 19,300 kg/m³ × 4π × (100×10⁻⁹ m)² × 25×10⁻⁹ m ≈ 6 × 10⁻¹⁷ kg

This implies ~6 × 10⁻⁸ g of gold per pulse, or ~60 mg/s at 1 MHz → roughly 1.9 tonnes of gold per year if not recovered — ~0.05% of world annual production (~3,500 t/yr). Viable but not negligible. Recovery fraction is still the critical constraint.[2]

In practice, gold nanoshell recycling from the spent liquid jet would be essential. Whether gold survives the plasma event as recoverable material — or is vaporized, dissolved into the jet fluid, or mixed with deuterium plasma products — is not addressed in any source. If nanoshells are destroyed each pulse and gold is not recovered, supply chain and cost implications are severe.

Gold price is currently ~$85,000/kg (early 2026). At 60 mg/s (unrecovered) and ~$85k/kg: ~$18,000/hr — economically punishing but not the $0.5M/hr originally estimated. Viable operation still requires near-complete nanoshell recycling, which is entirely undemonstrated.

### Femtosecond Laser Components

The laser driver uses "commercially available femtosecond lasers" — in practice, Ti:sapphire or Yb-fiber systems. Key supply chain considerations:
- Ti:sapphire crystals: Specialty crystal growth, limited global suppliers (few hundred kg/year production capacity). Scaling to MW-class average power would require substantial ramp-up.
- Laser amplifier diodes: At high average power, diode lifetimes and costs dominate. Analogue from laser ICF work: DPSSL diodes must achieve <$0.007/W for economic viability in laser IFE (TRUMPF/LLNL study cited in 26-laser-icf-indirect-drive exemplar). Femtosecond oscillators and amplifiers at plant scale have no cost benchmarks.
- Nonlinear optical components for OAM generation: specialized photonics, limited supply.

No supply chain assessment for femtosecond laser systems at fusion plant scale exists in any public source.

### Structural and Shielding Materials

Without a chamber design, material requirements cannot be quantified. At the projected 10^19 n/s flux, structural materials would face significant activation. Unlike D-T concepts where 14 MeV neutrons drive design (ODS steel, W, SiC), D-D 2.45 MeV neutrons have lower per-neutron damage potential but are still capable of embrittling structural materials at high fluence. Standard shielding materials (polyethylene, water, steel, lead) apply but dimensions and costs are unconstrained.

---
[1] General knowledge: world CANDU D2O production ~300 t/year; D2O market price ~$300-600/kg
[2] [inferred: nanoshell mass from geometry in arxiv-2503-nanoshell-paper.md §Target Design: "Typical radius: ~100 nm"; thin-shell regime: "thickness ≤ skin depth" → ~25 nm Au; 10^6 nanoshells/pulse × 10^6 Hz = 10^12/s; mass per nanoshell ~6×10^-18 kg → ~6 g/s; gold price ~$85k/kg current market]

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fuel | D-D (liquid D2O) | arxiv-2503-nanoshell-paper.md §Fuel | high | No tritium required |
| Operation mode | Pulsed | cortex-fusion-website.md §Technology Description | high | Discrete femtosecond pulses |
| Repetition rate (projected) | 1 MHz | arxiv-2503-nanoshell-paper.md §Laser Specifications | low | "Target repetition frequency for reactor: 1 MHz" — not demonstrated |
| Repetition rate (website claim) | "thousands of pulses per second" (kHz) | cortex-fusion-website.md §Technology Description | low | Website number, no demonstration |
| Rep rate (independent demo) | 1 kHz | kHz-liquid-sheet-fusion-paper.md §Key Technical Details | medium | Cambridge paper — different hardware, no nanoshells |
| Fusion power (projected) | ~1 MW | arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters | low | 1 MW projected, no experimental basis |
| Q-factor (projected) | ~100 | arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters | low | Assumes 30% conversion efficiency and 3 kW laser input — both unvalidated |
| Neutron flux (projected) | ~10^19 n/s | arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters | low | "Exceeds current devices by nine orders of magnitude" |
| Neutron energy | 2.45 MeV | [inferred from D-D physics] | high | Standard D-D → He-3 + n branch; lower than D-T 14 MeV |
| Laser input power at Q~100 | ~3 kW | arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters | low | "With 30% conversion efficiency, 3 kW laser consumption" |
| Peak laser intensity | ~1 atomic unit (~10^9 V/cm external) | arxiv-2503-nanoshell-paper.md §Laser Specifications | medium | "Modest by fusion standards" |
| Internal field after enhancement | ~10^11 V/cm | arxiv-2503-nanoshell-paper.md §Physics Mechanism | low | Theoretical plasmonic enhancement — not measured |
| Deuteron effective energy | ~25 keV equivalent | arxiv-2503-nanoshell-paper.md §Physics Mechanism | low | "Equivalent to thermonuclear plasma at ~25 keV (~10^8 K)" |
| Nanoshells per pulse | 1 million | arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters | low | Reactor scenario, not demonstrated |
| Nanoshell radius | ~100 nm | arxiv-2503-nanoshell-paper.md §Target Design | medium | "Typical radius: ~100 nm or larger" |
| Laser wavelength | ~1 μm | arxiv-2503-nanoshell-paper.md §Laser Specifications | medium | Standard near-IR femtosecond laser |
| Laser pulse duration | ~3 fs | arxiv-2503-nanoshell-paper.md §Laser Specifications | medium | Specified in paper |
| Fusion rate per nanoshell | ~10^7 s⁻¹ | arxiv-2503-nanoshell-paper.md §Fusion Parameters | low | Theoretical calculation |
| Power per nanoshell | ~1 μW | arxiv-2503-nanoshell-paper.md §Fusion Parameters | low | Derived from fusion rate × energy per event. Note: internally inconsistent with the same paper's 10^7 s⁻¹ fusion rate × 3333 MeV/event (which would give ~0.5 mW); compounds the 3333 MeV anomaly (see §Section 2, Challenge 2). |
| D2O fuel cost | ~$300–600/kg | [analogue: commercial CANDU D2O market price] | medium | Well-characterized commodity; consumption rate unknown |
| Net electrical output | Unknown | No Cortex source | — | Requires energy capture architecture |
| Thermal efficiency | Unknown | No Cortex source | — | No energy conversion method disclosed |
| Capital cost | Unknown | No Cortex source | — | No plant design disclosed |
| Capacity factor | Unknown | No Cortex source | — | No maintenance or operational data |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net electrical output | truly-unknown | blocking | Requires energy capture architecture — not disclosed |
| Energy conversion method / efficiency | truly-unknown | blocking | Completely absent from all Cortex sources |
| Capital cost (total, by subsystem) | truly-unknown | blocking | No plant design or cost estimate published |
| Capacity factor | truly-unknown | blocking | No operational experience, no maintenance model |
| Nanoshell recycling rate and mechanism | truly-unknown | blocking | Critical for gold consumption and operating cost |
| First-wall / chamber design and lifetime | truly-unknown | blocking | No chamber architecture disclosed |
| Blanket design and tritium/neutron management | truly-unknown | important | No approach disclosed; D-D neutrons require shielding at projected flux |
| Recirculating power fraction | derivable | important | Q~100 implies low recirculating fraction, but laser wall-plug efficiency unknown |
| Laser cost at plant scale | not-yet-sourced | important | Commercial fs laser analogue costs exist but not at fusion plant scale |
| Experimental validation of plasmonic D-D fusion | truly-unknown | blocking | No experimental result published by Cortex |
| Gold consumption rate and recovery fraction | derivable | important | Can estimate from nanoshell geometry × rep rate × pulse count |
| Regulatory classification | truly-unknown | important | D-D facility with 10^19 n/s — no licensing precedent |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Energy capture architecture (method, efficiency, BOP) | S2, S3, S5 | truly-unknown | blocking | Cortex patent applications may contain engineering detail; contact company |
| 2 | Experimental validation of plasmonic field enhancement driving D-D fusion in nanoshells | S1, S2, S3 | truly-unknown | blocking | Await Cortex experimental publications; independent group replication |
| 3 | Resolution of anomalous 3333 MeV/event energy figure | S1, S2, S5 | truly-unknown | blocking | Author clarification or peer review of arXiv:2503.15531 |
| 4 | Net electrical output and Q-value experimental basis | S2, S5 | truly-unknown | blocking | No basis exists; blocking until physics validated |
| 5 | Capital cost estimate (any component, any level) | S5 | truly-unknown | blocking | No published estimate; would require plant design |
| 6 | Nanoshell delivery at MHz rate with gold recovery | S3, S4 | truly-unknown | blocking | Engineering demonstration required |
| 7 | Capacity factor (maintenance model, component lifetimes) | S5 | truly-unknown | blocking | No operational experience |
| 8 | Gold consumption rate and recycling scheme | S4, S5 | truly-unknown | important | Calculable from geometry; recycling requires demonstration |
| 9 | Neutron shielding design for 10^19 n/s D-D source | S3, S4, S5 | truly-unknown | important | Standard neutronics tools applicable once flux and geometry are defined |
| 10 | Laser wall-plug efficiency at plant-relevant average power | S5 | not-yet-sourced | important | Commercial femtosecond laser efficiency data exists but not at MW-class scale |
| 11 | Laser cost at plant-scale average power | S4, S5 | not-yet-sourced | important | Indirect analogue from DPSSL studies in laser IFE; not applicable directly |
| 12 | Regulatory classification for high-rep-rate D-D facility | S2 | truly-unknown | important | No NRC rulemaking for this operation profile; 10 CFR Part 30 applies in principle |
| 13 | Blanket design and activation inventory management | S3, S4 | truly-unknown | important | Depends on energy capture architecture and chamber design |
| 14 | Recirculating power fraction at demonstrated efficiency | S5 | derivable | nice-to-have | Q~100 claim implies ~1% recirculating; laser wall-plug efficiency is the missing factor |
| 15 | D2O consumption rate | S4, S5 | derivable | nice-to-have | Calculable from target mass × rep rate once target geometry confirmed |

---

## Section 7: Cross-Concept Notes

No approved prior analyses provide cost assumptions or subsystem designs directly applicable to this concept. The brief comparison below identifies what is shared and what diverges.

**Shared with laser IFE broadly (26-laser-icf-indirect-drive exemplar):**
The general IFE challenge set — final optics survivability, target delivery, chamber clearing — applies in principle to Cortex. The key difference is that Cortex proposes to eliminate the dominant cost items of conventional laser ICF: no hohlraum, no cryogenic target fabrication, no high-energy DPSSL or KrF driver. The laser energy per pulse is vastly lower (~1 atomic unit peak intensity vs. MJ-class NIF pulses), which potentially sidesteps the laser cost problem entirely. However, this is predicated on the plasmonic enhancement physics actually working — which is undemonstrated.

The exemplar analysis notes that laser IFE target costs must be less than 10% of electricity produced per shot to be economical. For Cortex, the equivalent question is nanoshell cost per pulse: at 1 MHz with 10^6 nanoshells per pulse, target cost must remain negligible relative to energy value per pulse. This is plausibly achievable *if* nanoshells are recycled — gold in nanoshell form is reusable — but not if gold is consumed.

**Shared with pulsed IFE concepts (07-maglif analysis §Challenges):**
The rep rate leverage principle identified in the MagLIF analysis applies here: annual energy output scales as yield × rep rate × availability, so rep rate is the dominant LCOE lever. A 10× increase in rep rate (100 kHz → 1 MHz) from the same driver produces 10× more annual energy from identical capital. The difference is that MagLIF has achieved single-shot fusion yields and the rep rate challenge is a scaling problem; Cortex has not achieved single-shot fusion at all and faces a physics demonstration challenge before the rep rate challenge becomes relevant.

**Divergences from all approved analyses:**
- No external magnets, no cryogenics, no tritium — Cortex's cost structure would be fundamentally different from MFE concepts (01-hts-compact-tokamak, 11-magnetic-mirror, 08-frc-w-direct-conversion) in capital cost composition.
- D-D fuel eliminates the tritium supply chain that is a key constraint in all D-T concepts.
- The driver technology (commercial femtosecond laser) is qualitatively different from all other fusion drivers and has no cost analogue in the prior analyses.
- The concept is so early in development that no subsystem cost reuse from prior analyses is warranted.

---

## Section 8: Sources

**1. Kharzeev, D.E., Levitt, J., Trallero-Herrero, C. (2025). "Fusion in a Nanoshell: Harnessing Plasmonic Fields for Nuclear Reactions." arXiv:2503.15531 (submitted 2025-02-27, revised 2025-04-04).**
- Primary technical reference for the concept. Provides physics mechanism, target design, projected reactor parameters (Q~100, 10^19 n/s, 1 MW, 1 MHz), and the anomalous 3333 MeV/event figure.
- Phase 1a path: `iter-01/sources/arxiv-2503-nanoshell-paper.md`

**2. Cortex Fusion Systems website (accessed 2026-03-07). https://www.cortexfusion.systems/**
- Company overview, technology description (OAM laser, kHz rep rate, liquid jet, plasmonic nanostructures), funding ($2.6M), key personnel (Levitt, Kharzeev), IP (11+ patent applications), and current status ("building the first electricity-producing fusion reactor").
- Phase 1a path: `iter-01/sources/cortex-fusion-website.md`

**3. Levitt, J. (2023). "Ultrafast Laser Architectures for Quantum Control of Nuclear Fusion." arXiv:2308.07417 (2023-08-14).**
- Earlier single-author paper establishing the quantum-control framing for the company's laser approach. No reactor engineering. References U.S. Patent Application No. 17/855,476.
- Phase 1a path: `iter-01/sources/arxiv-2308-levitt-quantum-control.md`

**4. [Authors unspecified]. "Detailed Characterization of kHz-rate Laser-Driven Fusion at a Thin Liquid Sheet." High Power Laser Science and Engineering, Cambridge University Press, 2024.**
- Independent (non-Cortex) demonstration of kHz-rate D-D fusion on thin D2O liquid sheets. Achieved ~10^5 n/s at 1 kHz with a conventional Ti:sapphire relativistic-intensity laser. Validates the general liquid-jet D-D concept; does not validate Cortex's plasmonic approach. Key baseline for assessing the magnitude of Cortex's scaling claims.
- Phase 1a path: `iter-01/sources/kHz-liquid-sheet-fusion-paper.md`

**5. Cortex Fusion Systems internal dossier (concept summary).**
- Cited in §Section 2 footnotes [1] and [5] for energy capture gap and neutron management gap. Primary internal summary document for the concept, assembled from all available Cortex sources. Contains structured gap inventory used in this analysis.
- Phase 1a path: `iter-01/sources/dossier.md`
