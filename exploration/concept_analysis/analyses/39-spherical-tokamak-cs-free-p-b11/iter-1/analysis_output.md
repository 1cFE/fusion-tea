# D1+ Analysis: Spherical Tokamak - CS-free p-B11 (ENN Energy)

**Concept**: Central-solenoid-free spherical tokamak targeting p-B11 aneutronic fusion with direct energy conversion
**Company**: ENN Energy (ENN Group subsidiary, China)
**Current Devices**: EXL-50U (operating), EHL-2 (in design)
**Confinement Family**: MFE — Spherical Tokamak

---

## Section 1: Availability of Data

**Rating: Opaque**

ENN Energy has published an arXiv roadmap paper and an EHL-2 physics design overview, but no commercial plant study, no power plant design point, and no cost estimates exist in the public domain. The current devices (EXL-50U, EHL-2) are early-stage experimental machines separated from a commercial plant by multiple device generations. Fundamental physics questions about p-B11 ignition in a thermal tokamak remain unresolved in the scientific literature. The "Opaque" rating reflects both the pre-commercial stage of the concept and the absence of any published LCOE-relevant parameters.

**Published device documentation:**
The primary public reference is ENN's arXiv roadmap paper (arXiv:2401.11338, published in *Physics of Plasmas* 31, 062507, 2024) [enn-roadmap-pb11-arxiv-2401.11338.md]. This paper describes ENN's vision for p-B11 fusion using a spherical tokamak, documents EXL-50U parameters, and frames EHL-2 as the next physics verification step. A separate EHL-2 physics design overview paper was published in *Plasma Science and Technology* (doi:10.1088/2058-6272/ad981a), providing device parameters and mission objectives. Neither paper constitutes a commercial plant study.

**Company transparency:**
ENN's English-language website provides a brief overview of the compact fusion program and states that p-B11 fuel "offers direct energy conversion capability for higher efficiency, produces minimal neutron radiation, and enables distributed power generation" [dossier.md §Energy Capture]. This is the only public statement of the commercial energy capture strategy. No engineering details of any direct converter design have been published. ENN is a large Chinese energy conglomerate; the fusion program appears to be exploratory research rather than a near-term commercial venture.

**Independent analyses:**
A comment on ENN's roadmap was published in 2024 (pubs.aip.org/aip/pop/article/32/6/064701/3348211), indicating the concept has received critical scrutiny from the plasma physics community. The specific critiques are not available in the extracted sources but are expected to address the fundamental p-B11 physics challenges. No independent TEA or plant study of the ENN concept has been identified.

**Phase 1a dossier completeness:**
After two research iterations, the dossier achieves high confidence on confinement family, concept topology, fuel, operation mode, and driver technology. Magnet type remains low confidence (resistive copper inferred from EXL-50U datapoints). Energy capture is medium confidence (direct conversion stated as intent, no design published). No commercial plant parameters (Q, fusion power, net electric output, capital cost) exist in the public domain.

**Key data gaps limiting this analysis:**
1. No commercial plant design point — Q value, fusion power, net output, and all LCOE inputs are entirely absent
2. The fundamental p-B11 ignition physics question is unresolved — it is not established that a thermal spherical tokamak can achieve net p-B11 fusion power
3. Direct energy conversion technology is undefined — efficiency benefit is speculative
4. Magnet conductor type for EHL-2 not confirmed
5. No independent TEA or plant study exists for the ENN concept or for any p-B11 spherical tokamak design

---

## Section 2: Challenges in Capturing System Function

The ENN CS-free p-B11 spherical tokamak presents a qualitatively different LCOE modeling challenge from any other concept in this analysis pipeline. Multiple challenges are not matters of data uncertainty but of unresolved physics — the concept cannot be modeled with conventional analogue assumptions until the underlying plasma physics is demonstrated. Challenges are ranked by LCOE impact.

**1. p-B11 ignition physics: the Lawson criterion may not be achievable thermally (Impact: Fundamental)**

The proton-boron fusion reaction (p + ¹¹B → 3α, releasing ~8.7 MeV) requires ion temperatures in the range of 100–300 keV for a thermal plasma to produce useful fusion power — roughly 10–20 times higher than D-T [1]. At these temperatures, bremsstrahlung radiation losses (scaling as Z²n²T^0.5 and integrating over the boron impurity's high charge Z=5) and cyclotron radiation losses become so large that they may exceed the fusion power output for any thermal plasma, making net energy gain impossible without exotic suppression schemes. This is not a data gap — it is a fundamental published concern in plasma physics (see Rider 1997 and Nevins 1998 in the literature). EHL-2 targets Ti ≈ 30 keV [enn-roadmap-pb11-arxiv-2401.11338.md §device goals] — an order of magnitude below the temperatures needed for p-B11, and is explicitly a "physics verification" machine, not a power-producing device. Until a successor device demonstrates the relevant plasma conditions and net energy balance, no LCOE model for the ENN concept has a credible physics foundation.

> "EHL-2 will verify p-11B thermal reaction rates and establish spherical tokamak scaling laws at tens of keV ion temperatures."
> — enn-roadmap-pb11-arxiv-2401.11338.md (summarized in dossier.md §Summary)

[1] dossier.md §Fuel: EHL-2 "targets p-11B thermal reaction rate verification" — confirming this is as-yet unverified at the target temperatures.

**2. Direct energy conversion: undefined technology, central to the economic case (Impact: Critical)**

The p-B11 economic case rests on direct conversion of the three alpha particle products (~2.9 MeV each, all charged) to electricity — bypassing the Carnot-limited steam cycle and achieving theoretical efficiencies of 70–90% instead of ~35%. Without this advantage, a p-B11 plant needs ~10–30× higher plasma performance than D-T (because the Lawson condition is far harder) while capturing energy at lower efficiency than a D-T thermal plant — making it economically untenable. ENN publicly frames direct energy conversion as the commercial strategy but has published no engineering design for a direct converter system (no electrostatic decelerator design, no inertial current collector, no ion-beam recovery scheme) [dossier.md §Energy Capture]. The TRL for direct energy conversion in a tokamak geometry is effectively 1 — the concept has been theorized, and small-scale Venetian-blind collectors were tested with mirror machines in the 1970s, but no equivalent for a spherical tokamak with p-B11 alphas has been developed. The efficiency assumption — the largest single driver of p-B11 economic competitiveness — is entirely unsupported by hardware.

**3. CS-free operation: demonstrated at small scale, unproven at reactor scale (Impact: High)**

ENN's distinctive engineering bet is the elimination of the central solenoid, driven by the geometric challenge of fitting a solenoid inside the compact center stack of a low-aspect-ratio spherical tokamak. ECRH non-inductive current drive was demonstrated on EXL-50 with approximately 1 A/W efficiency [dossier.md §Driver Technology]. However, a commercial p-B11 reactor would require sustained plasma currents far beyond the 3 MA target of EHL-2 — and at the extreme plasma temperatures needed for p-B11, the ECRH accessibility and efficiency in a spherical tokamak geometry become highly uncertain. The recirculating power fraction from a purely ECRH-driven reactor would be very large: at ~50% gyrotron wall-plug efficiency and the ECRH power required to drive full plasma current non-inductively, the recirculating power could represent 30–50% or more of any gross electrical output. This directly reduces Q_engineering and makes the economic case harder. This challenge is partly shared with the Tokamak Energy ST-E1 concept (21-spherical-tokamak-hts), which also relies on ECRH for current drive, but the CS-free constraint on ENN is more severe because there is no fallback inductive drive at all.

**4. Divertor at p-B11 plasma conditions (Impact: High)**

The EHL-2 physics design notes identify divertor heat flux > 20 MW/m² at low plasma density as a "significant engineering challenge" [enn-roadmap-pb11-arxiv-2401.11338.md]. For a reactor-scale device at the temperatures required for p-B11, divertor heat fluxes would be even more extreme because (a) the plasma must operate at very high temperatures where heat exhaust is harder to radiate, and (b) the alpha particle power load is unmitigated (no blanket to absorb a neutron fraction of the energy). Unlike D-T tokamaks where ~80% of fusion energy goes to neutrons (reducing charged-particle heat to the divertor), p-B11 deposits all energy into charged particles — every MW of fusion power eventually reaches the plasma-facing components as heat. This makes the divertor challenge for a p-B11 commercial plant qualitatively more severe than for a D-T tokamak.

**5. No cost analogues exist for this configuration (Impact: High)**

An LCOE model for the ENN concept would need to build from scratch: no blanket cost (advantage, but eliminates the largest fraction of available cost analogues), an undefined direct energy converter (no cost data), a CS-free ECRH drive system at commercial scale (no cost data), and a plasma physics regime that has not been demonstrated. The nearest analogue, the ARIES-ST study (a D-T spherical tokamak plant study), addresses the geometry but uses a fundamentally different fuel cycle, energy capture, and confinement physics regime. The p-B11 FRC analysis (18-p-b11-frc, TAE Technologies) provides some fuel-cycle analogy but uses a different topology. No published plant study for a p-B11 tokamak exists.

**6. O&M cost structure: greatly simplified or undefined (Impact: Moderate)**

The absence of a tritium breeding blanket eliminates the most maintenance-intensive first-wall system in a D-T plant. No scheduled blanket module exchanges, no tritium extraction circuit, no activated liquid metal circuit — O&M costs for the neutron-facing systems are substantially reduced. However, this benefit is partially offset by the need for the direct energy converter (a novel device with unknown maintenance requirements) and the ECRH system at commercial scale (gyrotron lifetimes limit availability). Without a published plant design, the O&M cost structure cannot be estimated with any confidence. A placeholder O&M assumption of ~1.5–2.5% of overnight capital cost per year (typical for MFE concepts) would be the minimum acceptable starting point, pending any plant study.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**p-B11 Plasma at Reactor-Relevant Conditions — TRL 1–2**

- **Demonstrated**: EXL-50U has achieved H-B plasma (hydrogen-boron) at 1 MA and 1.2 T [dossier.md §Confinement Concept], confirming that boron can be introduced into the plasma. EXL-50 demonstrated ECRH non-inductive startup with ~1 A/W current drive efficiency (arXiv:2104.14844). EHL-2 is targeting Ti ≈ 30 keV — a significant advance, but still one order of magnitude below the >100 keV range needed for meaningful p-B11 fusion rates.
- **On paper only**: Any tokamak plasma at Ti > 100 keV with a significant boron fraction, let alone net p-B11 fusion power. Confinement of alpha particles from the p-B11 reaction inside the ST magnetic geometry. Suppression of bremsstrahlung and cyclotron radiation to levels below fusion power output.
- **Missing at scale**: Demonstration that the thermal p-B11 Lawson condition is achievable in any confinement device. Experimental validation of Ti/Te >> 1 regimes needed for the p-B11 reaction at low bremsstrahlung cost. A net-fusion-energy device with p-B11 fuel at any scale, in any configuration.

---

**Direct Energy Conversion System — TRL 1–2**

- **Demonstrated**: Small-scale Venetian-blind electrostatic converters were tested with mirror machines in the 1970s (Barr and Moir, Lawrence Livermore), demonstrating the physical principle of direct ion-to-electricity conversion. These experiments used different ion energies and were in open magnetic geometries — not tokamaks, not p-B11 alphas.
- **On paper only**: Any direct energy converter design for a spherical tokamak geometry. Alpha particle exhaust routing from the plasma edge to the converter structure. Converter efficiency targets and engineering specifications for p-B11 product energies (~2.9 MeV per alpha, three per reaction).
- **Missing at scale**: Any direct converter hardware for tokamak geometry at any scale. Demonstrated efficiency of direct conversion from p-B11 alpha products. Integration with the ST magnetic geometry for alpha exhaust management. Converter lifetime under the alpha particle and gamma flux from a p-B11 plasma.

---

**CS-Free Non-Inductive Current Drive at Reactor Plasma Conditions — TRL 3–4**

- **Demonstrated**: EXL-50 demonstrated ECRH-only startup and current drive with ~1 A/W efficiency [dossier.md §Driver Technology, citing arXiv:2104.14844]. EHL-2 (under design) will test sustained CS-free operation at 3 MA, 3 T. ECRH current drive is well-characterized in conventional-aspect-ratio tokamaks at moderate temperatures.
- **On paper only**: ECRH current drive at the plasma currents required for a commercial reactor, at the plasma temperatures (>100 keV) and densities needed for p-B11 fusion. ECCD efficiency as a function of plasma conditions in the required operating regime — accessibility windows for EC waves change dramatically at the temperatures and densities of a p-B11 reactor.
- **Missing at scale**: Non-inductive current drive sustaining a >10 MA plasma current without central solenoid. Wall-plug-to-plasma-current efficiency at commercial scale. ECRH system reliability over years of continuous operation at the MW-per-channel level.

---

**ST Plasma Confinement at High Ion Temperature (Ti/Te >> 1) — TRL 2–3**

- **Demonstrated**: Spherical tokamak plasmas have been sustained at Ti/Te ≈ 1–2 in NSTX-U and MAST-U. EHL-2 targets Ti/Te ≥ 2 at Ti ≈ 30 keV [enn-roadmap-pb11-arxiv-2401.11338.md]. High-Ti/Te regimes are important for p-B11 because elevated ion temperature relative to electrons reduces bremsstrahlung losses (which depend on Te) while maintaining fusion rate (which depends on Ti).
- **On paper only**: Ti ≈ 100–300 keV with Ti/Te >> 1 in a spherical tokamak. Confinement scaling at these ion temperatures in the ST geometry. Impact of fast alpha particles on plasma stability in a low-aspect-ratio tokamak at p-B11 conditions.
- **Missing at scale**: Any experimental data on ST confinement at Ti > 30 keV. Alpha particle physics in a burning p-B11 plasma. MHD stability at the high-beta conditions that would accompany the extreme temperatures needed.

---

**Divertor (p-B11 Conditions) — TRL 3–4**

- **Demonstrated**: Tungsten monoblock divertors tested at 10–20 MW/m² in WEST, GLADIS, and DTT for D-T-relevant scenarios. ST-specific Super-X divertor concepts demonstrated in MAST-U (UKAEA), significantly reducing heat loads via extended divertor leg. The EXL-50U has operated with a conventional divertor.
- **On paper only**: Divertor concepts for a device where 100% of fusion energy is deposited as charged-particle heat (no neutron fraction to the blanket). Heat load mitigation at the extreme fluxes expected from a p-B11 plasma. Divertor design compatible with a direct energy converter that needs to receive exhaust alpha particles.
- **Missing at scale**: Plasma-facing components surviving the combined heat flux from a fully-charged-particle-heated p-B11 plasma. Detachment regime in the required high-temperature, high-density boundary plasma conditions. Integration of the divertor with alpha particle exhaust routing for direct energy conversion.

---

**ECRH and NBI Heating and Current Drive Systems — TRL 5–7**

- **Demonstrated**: EHL-2 will use 17 MW NBI + 6 MW ECRH [dossier.md §Primary Heating]. At this scale, both technologies are well-developed. MW-class gyrotrons (ITER 170 GHz, 1 MW CW) are commercially available. High-energy NBI is mature from JET, JT-60SA, and ITER programs.
- **On paper only**: NBI and ECRH systems optimized for the extreme plasma conditions needed for p-B11 (Ti > 100 keV), where beam absorption and wave coupling physics differ from D-T regimes. Heating systems sustaining the required plasma state against radiation losses that may dominate at p-B11 temperatures.
- **Missing at scale**: Gyrotron array providing tens to hundreds of MW for non-inductive current drive at commercial scale. NBI at the ion energies potentially needed to sustain a >100 keV plasma. Heating efficiency that can deliver positive net energy gain despite enormous radiated power at p-B11 temperatures.

---

**Spherical Tokamak Vacuum Vessel and Magnet System — TRL 5–6 (EHL-2 level)**

- **Demonstrated**: EXL-50U operated at 1 MA, 1.2 T with 150 kA TF coil current — consistent with a well-engineered copper resistive magnet system [dossier.md §Magnet Type]. EHL-2 is designed for 3 T at R₀ = 1.05 m, within the engineering capability of copper Bitter-plate or similar resistive coil technology. ST vacuum vessel and magnet design is well-established at NSTX-U, MAST-U, and Globus-M2 scale.
- **On paper only**: Commercial-scale ST with resistive copper coils — ohmic heating of the coils would represent an enormous recirculating power penalty at reactor scale (100× worse than HTS for the same field-volume product). EHL-2 magnet engineering design is not described in detail in available sources.
- **Missing at scale**: Resistive coil power consumption at commercial reactor scale (critical LCOE input). A commercial power-positive p-B11 ST almost certainly requires HTS coils to achieve acceptable recirculating power fraction, but no HTS technology has been announced by ENN.

---

**Balance of Plant / Power Conversion — TRL Undefined**

- **Demonstrated**: Conventional steam Rankine and sCO₂ Brayton cycles are commercially mature (TRL 9). However, the ENN concept does not plan to use these — the direct energy conversion pathway bypasses the thermal cycle entirely [dossier.md §Energy Capture].
- **On paper only**: Any direct-conversion-based plant balance of plant. Integration of a direct energy converter output (high-voltage DC from decelerating alphas) with the grid. If direct conversion fails, fallback to a thermal cycle is possible but abandons the primary economic advantage.
- **Missing at scale**: Demonstrated direct energy converter plant integration. Alpha particle exhaust power routing at commercial scale. Hybrid system that captures both direct (alpha) and thermal (secondary radiation, neutrons, plasma heating) energy streams.

---

## Section 4: Key Materials and Supply Chain Considerations

**Boron-11 — Abundant, Enrichment May Be Required**

Natural boron is approximately 80% ¹¹B and 20% ¹⁰B. The ¹⁰B isotope has a very high thermal neutron capture cross-section (used in nuclear control rods), which could absorb residual secondary neutrons from side reactions in a p-B11 plasma and cause minor activation — however, the primary p-B11 reaction produces no neutrons, so this is a minor consideration. For a commercial plant, enriching boron to >95% ¹¹B would be prudent to maximize the fuel-effective boron fraction and minimize ¹⁰B-related effects. Boron isotope enrichment is a mature process (used for ¹⁰B in fission reactor control), but ¹¹B-enriched boron at commercial quantities has not been specified or sourced for any fusion application. Global boron production is ~10 million tonnes/year (boron minerals), making raw material supply a non-issue; isotopic enrichment at commercial fusion scale is an unquantified but solvable industrial problem.

**No Tritium Supply Chain — Major Cost and Complexity Elimination**

The aneutronic p-B11 fuel cycle requires no tritium. This eliminates: tritium startup inventory (~1 kg at >$35,000/g for D-T concepts), lithium-6 enrichment, tritium breeding blanket, tritium extraction circuit, tritium processing plant, and the tritium supply sequencing constraint that affects all D-T concepts. This is the single largest supply chain advantage of p-B11 over D-T — eliminating what would otherwise be a ~20–30% capital cost category (blanket system) and a complex O&M-intensive system [cross-reference: 21-spherical-tokamak-hts §Section 4].

**No Breeding Blanket Materials (FLiBe, Lithium-6, Beryllium) — Further Supply Elimination**

A p-B11 plant requires no beryllium (used in FLiBe), no enriched lithium, and no liquid metal breeding circuit. The supply chain constraints that affect all D-T MFE concepts — FLiBe production capacity, beryllium supply, liquid lithium reactivity — do not apply here. This is a genuine structural advantage, though it is only realized if p-B11 ignition is achieved.

**Resistive Copper Coils — Power Penalty, No Supply Constraint**

EXL-50U appears to use copper resistive magnets (Bitter-plate or similar) based on the 150 kA TF current at 1.2 T [dossier.md §Magnet Type]. Copper is abundantly available with no supply chain risk. However, resistive coils consume large amounts of recirculating power: ohmic losses in the coil system scale as I²R, and for a commercial-scale device the ohmic power would represent a significant fraction of gross electrical output. For comparison, an ITER-scale device (~15 MA plasma current, similar field) with copper coils rather than superconductors would consume ~300 MW just in coil ohmic heating — a severe LCOE penalty. A commercial p-B11 ST almost certainly requires a transition to HTS magnets (not yet announced by ENN), which would then introduce the same REBCO supply chain challenges as the D-T HTS tokamak concepts [cross-reference: 21-spherical-tokamak-hts §Section 4].

**ECRH Gyrotron Systems — Commercially Available at EHL-2 Scale, Scaling Challenge**

23 MW of combined ECRH + NBI for EHL-2 is commercially achievable with existing technology. At commercial reactor scale, the ECRH system needed for non-inductive current drive would grow to potentially hundreds of MW — requiring very large gyrotron arrays with long-term reliability. Gyrotron technology is mature at the 1 MW/unit level (ITER class) but maintaining 50%+ wall-plug efficiency across hundreds of units in continuous operation is an industrialization challenge, not a supply chain constraint.

**Plasma-Facing Components (Tungsten) — Adequate Supply, Manufacturing Challenges Shared with D-T**

Tungsten for the first wall and divertor is available in adequate global supply. However, the heat flux challenge for a p-B11 device (where all fusion energy is deposited as charged-particle heat) is more severe than for D-T tokamaks. Manufacturing challenges for large-area tungsten components are shared with the D-T tokamak program and are not supply-constrained.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Device major radius (EXL-50U) | ~0.58 m (estimated from 150 kA / 1.2 T specs) | dossier.md §Magnet Type | low | EXL-50U geometry not directly stated; inferred from published TF parameters |
| EHL-2 major radius | R₀ ≈ 1.05 m | dossier.md §Summary; enn-roadmap-pb11-arxiv-2401.11338.md | high | Physics verification device |
| EHL-2 aspect ratio | A ≈ 1.85 | dossier.md §Confinement Concept | high | Low aspect ratio — genuine spherical tokamak |
| EHL-2 toroidal field | B₀ ≈ 3 T | dossier.md §Summary | high | Experimental device |
| EHL-2 plasma current | Ip ≈ 3 MA | enn-roadmap-pb11-arxiv-2401.11338.md §device goals | high | Target plasma current |
| EHL-2 heating power | 17 MW NBI + 6 MW ECRH | dossier.md §Primary Heating | high | For physics verification — not scaled to power plant |
| EHL-2 target ion temperature | Ti ≈ 30 keV | enn-roadmap-pb11-arxiv-2401.11338.md §device goals | high | ~10× below p-B11 ignition requirement |
| EHL-2 Ti/Te target | ≥ 2 | enn-roadmap-pb11-arxiv-2401.11338.md §device goals | high | Elevated Ti/Te reduces bremsstrahlung |
| EXL-50U TF coil current | 150 kA | dossier.md §Magnet Type | high | Consistent with copper resistive coils |
| EXL-50U toroidal field | 1.2 T | dossier.md §Magnet Type | high | First device in ENN's sequence |
| EXL-50U plasma current | 1 MA | dossier.md §Summary | high | Demonstrated in January 2024 |
| ECRH current drive efficiency (EXL-50) | ~1 A/W | dossier.md §Driver Technology | medium | Demonstrated on EXL-50, scaled from arXiv:2104.14844 |
| Divertor heat flux concern (EHL-2) | > 20 MW/m² at low density | enn-roadmap-pb11-arxiv-2401.11338.md §challenges | high | Identified as significant challenge |
| Energy capture strategy | Direct (charged particle) | dossier.md §Energy Capture | medium | Stated intent, no design |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | Non-inductive ECRH current drive enables CS-free continuous operation |
| p-B11 reaction energy | ~8.7 MeV total (3α, ~2.9 MeV each) | Well-established nuclear physics | high | No neutrons in primary reaction |
| p-B11 peak cross-section energy | ~650 keV CM energy | Well-established nuclear physics | high | ~10× higher than D-T (68 keV) |
| Theoretical direct conversion efficiency | 70–90% | [estimated — electrostatic DEC theoretical limit] | low | Upper bound; no demonstrated system; assumes perfect alpha capture geometry |
| Gyrotron wall-plug efficiency | ~50–55% | [analogue: ITER-class gyrotron; shared with 21-spherical-tokamak-hts analysis §S5] | medium | Sets recirculating power floor for ECRH current drive |
| p-B11 Lawson criterion temperature | >100–300 keV (Ti) | [analogue: established plasma physics; see Rider 1997, Nevins 1998] | high | Fundamental physics parameter — 10–20× harder than D-T |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Commercial plant Q value | truly-unknown | blocking | No plant design exists; p-B11 Q > 1 not yet demonstrated in any device |
| Fusion power (gross), net electric output | truly-unknown | blocking | No commercial plant design; EHL-2 is non-power |
| Capital cost estimate (total or $/kWe) | truly-unknown | blocking | No plant study; no analogue plant study exists for p-B11 ST |
| Direct energy conversion system efficiency | truly-unknown | blocking | No engineering design published; TRL 1–2 |
| Direct energy conversion system capital cost | truly-unknown | blocking | No design to cost; novel device category |
| Plasma current for commercial plant | truly-unknown | blocking | EHL-2 is 3 MA experimental; commercial plant not defined |
| ECRH recirculating power fraction (commercial) | truly-unknown | blocking | Depends on unknown commercial plasma current and unknown coil system |
| Capacity factor | truly-unknown | important | Steady-state intent is favorable; no plant design to assess maintenance requirements |
| Power conversion cycle thermal efficiency | not-yet-sourced | important | If direct conversion fails, fallback thermal cycle efficiency unknown |
| Blanket and tritium system capital cost | N/A | — | Not applicable — no blanket required for p-B11 |
| Magnet type for commercial plant | truly-unknown | important | EHL-2 conductor type unconfirmed; commercial plant almost certainly requires HTS, but not stated |
| p-B11 ignition feasibility in thermal ST plasma | truly-unknown | fundamental | May require demonstration that bremsstrahlung losses can be managed below fusion power |
| Plant-scale boron consumption rate | derivable | nice-to-have | Boron is abundant; consumption rate derivable from fusion power once known |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | p-B11 net fusion gain not demonstrated in any device — fundamental physics unresolved | S1, S2, S3 | truly-unknown | blocking | EHL-2 results (expected ~2026–2027) are the next data point; Lawson criterion papers (Rider 1997, Nevins 1998) should be reviewed for theoretical constraints |
| 2 | No commercial plant design point — all LCOE inputs absent | S1, S2, S5 | truly-unknown | blocking | No action available until ENN publishes a plant study or a third-party performs a system-code run |
| 3 | Direct energy conversion system design and efficiency undefined | S2, S3, S5 | truly-unknown | blocking | No public roadmap for DEC hardware; watch ENN publications post-EHL-2 |
| 4 | Direct energy conversion system capital cost | S3, S5 | truly-unknown | blocking | No cost analogues exist; Venetian-blind DEC literature (Barr & Moir, LLNL) provides concept-level reference only |
| 5 | Commercial plant magnet type unconfirmed | S3, S4, S5 | proprietary | important | EHL-2 coil-engineering paper would resolve EHL-2 question; commercial plant requires HTS transition (unannounced) |
| 6 | Recirculating power fraction from ECRH non-inductive current drive at reactor scale | S2, S3, S5 | truly-unknown | blocking | Cannot estimate without knowing commercial plasma current and coil system; ECRH scaling from EXL-50 would require extrapolation of 3–4 orders of magnitude |
| 7 | Divertor heat load and materials solution for all-charged-particle heating | S2, S3 | truly-unknown | important | No published design; p-B11 divertor heat load exceeds D-T by design; engineering path is undefined |
| 8 | Comment paper critique of ENN roadmap (physics challenges identified) | S1, S2 | not-yet-sourced | important | Ingest AIP comment paper (pubs.aip.org/aip/pop/article/32/6/064701/3348211) to understand which physics challenges have been publicly quantified |
| 9 | EHL-2 magnet conductor type and engineering design | S3, S4 | not-yet-sourced | important | EHL-2 PST paper (doi:10.1088/2058-6272/ad981a) full text not extracted; may contain magnet engineering details not in abstract |
| 10 | Plant capacity factor and availability | S2, S5 | truly-unknown | important | Steady-state operation is favorable in principle; no maintenance model for a direct-converter equipped p-B11 plant |
| 11 | Boron-11 enrichment requirement and supply chain | S4 | not-yet-sourced | nice-to-have | Natural ~80% ¹¹B may be adequate; enrichment process is mature from ¹⁰B production; quantify demand when plant design exists |
| 12 | Independent critique of p-B11 Lawson criterion achievability | S2, S3 | not-yet-sourced | important | Rider (1997) and Nevins (1998) are the key published analyses; should be formally ingested as sources |

---

## Section 7: Cross-Concept Notes

**Approved prior analysis referenced: 21-spherical-tokamak-hts (Tokamak Energy, D-T)**

The Tokamak Energy ST-E1 analysis is the most directly applicable approved prior analysis, sharing the spherical tokamak geometry. The following elements are noted for comparison.

**Shared ST geometry characteristics:**
Both ENN's concept and Tokamak Energy's ST-E1 use a low-aspect-ratio spherical tokamak (A ≈ 1.85 for EHL-2 vs. A = 2.3 for ST-E1). Both face the center-stack constraint that limits inboard blanket space. Both rely on ECRH for current drive and both plan steady-state or quasi-steady-state operation. The ECRH wall-plug efficiency assumption (~50–55%, from 21-spherical-tokamak-hts §Section 5) is adopted here as the best available analogue. The general ST divertor physics database (MAST-U Super-X, NSTX-U) applies to both concepts.

**Key divergences from 21-spherical-tokamak-hts:**

- **Fuel: p-B11 vs. D-T** — This is the fundamental differentiator. p-B11 requires ~10–20× higher plasma temperatures, imposes a potentially insurmountable bremsstrahlung constraint, and requires an entirely different energy capture strategy. No D-T analogue parameters can be transposed to a p-B11 concept without demonstrating that the Lawson condition is achievable. The ST-E1 analysis has an unpublished-but-probable physics design point; the ENN concept has no plausible commercial design point at all.

- **Blanket: none vs. outboard liquid Li** — The ENN p-B11 concept needs no breeding blanket. This eliminates what the ST-E1 analysis describes as a TRL 2–3 subsystem with significant supply chain complexity. The blanket capital cost category (~20–30% of plant CAPEX in D-T designs) is simply absent, which is a structural cost advantage — but only if p-B11 ignition is achieved.

- **Energy conversion: direct vs. thermal** — ST-E1 plans a thermal power cycle (steam Rankine or sCO₂, ~32–38% efficiency). ENN plans direct energy conversion (~70–90% theoretical efficiency). If ENN achieves both p-B11 ignition and direct conversion, the efficiency advantage is substantial. If direct conversion is not realized, a fallback thermal cycle at D-T-equivalent efficiency would face an even harder economic case than ST-E1 because the p-B11 Lawson criterion is far more demanding.

- **Magnets: resistive copper (ENN) vs. HTS (Tokamak Energy)** — ST-E1's Demo4 HTS coil set represents the most advanced public milestone in fusion magnet technology. ENN's copper coil system (inferred from EXL-50U) is mature technology but carries enormous recirculating power costs at commercial scale. ENN would need to transition to HTS to make a commercial plant viable, introducing the same REBCO supply chain challenges documented in the ST-E1 analysis — but this transition has not been announced.

- **Tritium and blanket supply chain** — The ST-E1 analysis dedicates significant discussion to the tritium supply constraint, liquid lithium handling, Li-6 enrichment, and WC cermet shielding. None of these apply to the ENN p-B11 concept, which is genuinely free of the tritium supply chain bottleneck.

**Other in-progress p-B11 concepts (not approved; for context only, not cross-referenced):**

Three other in-progress concepts also target p-B11 fuel: 18-p-b11-frc (TAE Technologies, FRC confinement), 23-laser-icf-nanostructured-target (Marvel Fusion, IFE), and 24-dense-plasma-focus (LPPFusion). All three face the same fundamental p-B11 physics challenge. The ENN concept is unique in approaching it via a spherical tokamak with CS-free ECRH drive and direct energy conversion, rather than an FRC, laser driver, or dense plasma focus. The aneutronic fuel cycle advantage (no breeding blanket, no tritium) is shared across all p-B11 concepts.

---

## Section 8: Sources

**1. ENN Roadmap Paper (arXiv:2401.11338 / Physics of Plasmas 31, 062507, 2024)**
- Full citation: ENN Energy Research Institute. "Proton-Boron Fusion Based on Spherical Torus." *Physics of Plasmas*, 31, 062507 (2024). arXiv:2401.11338.
- Contribution: Primary authoritative source for ENN's concept definition, EXL-50U/EHL-2 device parameters, p-B11 fuel strategy, CS-free ECRH current drive approach, and commercial roadmap vision. Summary extracted in Phase 1a research.
- Location: `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-01/sources/enn-roadmap-pb11-arxiv-2401.11338.md`

**2. EHL-2 Physics Design Paper (doi:10.1088/2058-6272/ad981a)**
- Full citation: ENN Energy Research Institute. "Overview of the physics design of the EHL-2 spherical torus." *Plasma Science and Technology*, 2024. doi:10.1088/2058-6272/ad981a.
- Contribution: EHL-2 device parameters (R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA), heating design (17 MW NBI + 6 MW ECRH), target conditions (Ti ≈ 30 keV, Ti/Te ≥ 2), mission (p-¹¹B reaction rate verification), and identified challenges (CS-free startup, divertor heat flux >20 MW/m²).
- Location: Referenced in dossier.md §Summary; full text not extracted in Phase 1a

**3. EXL-50 ECRH Current Drive Paper (arXiv:2104.14844)**
- Full citation: ENN Energy Research Institute. "Solenoid-free current drive via ECRH in EXL-50." arXiv:2104.14844 (2021).
- Contribution: Demonstrates ECRH non-inductive startup and current drive with ~1 A/W efficiency — the primary evidence for the CS-free engineering approach.
- Location: Referenced in dossier.md §Driver Technology

**4. ENN Company Website — Compact Fusion Program**
- Contribution: States that p-¹¹B fuel "offers direct energy conversion capability for higher efficiency, produces minimal neutron radiation, and enables distributed power generation." Primary source for energy capture strategy classification.
- Location: https://en.ennresearch.com/researchfield/Compactfusion/ (summarized in dossier.md §Energy Capture)

**5. ENN Iter-2 Search Notes**
- Contribution: Research notes confirming magnet type inference (copper, low confidence based on 150 kA / 1.2 T EXL-50U TF data), direct energy conversion classification (medium confidence), and absence of HTS announcements in ENN publications.
- Location: `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/enn-iter2-search-notes.md`

**6. Comment on ENN's Roadmap (pubs.aip.org/aip/pop/article/32/6/064701/3348211)**
- Full citation: Published comment on ENN roadmap, *Physics of Plasmas*, 32(6), 064701 (2024).
- Contribution: Independent critical assessment of ENN's p-B11 roadmap; content not available in extracted sources but expected to address p-B11 physics feasibility concerns. Flagged as a gap (not yet ingested).
- Location: Not yet extracted — see Gap #8 in Section 6

**7. Phase 1a Dossier**
- Contribution: Consolidated research findings from two iterations: device parameters, confidence ratings, remaining ambiguities, and structured citation tracking.
- Location: `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/dossier.md`

**8. D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for spherical tokamak geometry considerations (center stack, outboard blanket coverage, ST divertor physics), ECRH wall-plug efficiency analogue (~50–55%), and D-T supply chain contrast (tritium, REBCO, liquid Li). Also provides the Brown (2018) cost comparison framework and Hidalgo-Salaverri (2025) ST TEA references that apply by family analogy.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`

---

*Footnotes:*

[1] enn-roadmap-pb11-arxiv-2401.11338.md §device goals, summarized in dossier.md §Summary: "EHL-2 will verify p-11B thermal reaction rates and establish ST scaling laws at tens of keV ion temperatures" — confirming that even the 30 keV operating point is the next scientific milestone, and p-B11 ignition conditions (~100–300 keV) are multiple device generations away.
