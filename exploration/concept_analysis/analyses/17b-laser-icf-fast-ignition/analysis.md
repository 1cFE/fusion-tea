---
ID: 17b-laser-icf-fast-ignition
Concept: Laser ICF - Fast Ignition (D-T)
Company: Focused Energy
Status: draft
Created: 2026-04-19
Approved-Date:
Reuses: []
---

# D1+ Analysis: Laser ICF - Fast Ignition (D-T)

**Company**: Focused Energy  
**Concept**: Proton fast ignition — DPSSL compression + petawatt ignition laser  
**Fuel**: D-T  
**Classification**: IFE / Laser / Fast Ignition  

---

## Section 1: Availability of Data

**Rating: Limited**

Focused Energy is a private startup with tightly controlled public disclosures. The available information is qualitative and aspirational; no plant studies, system-code outputs, or independent techno-economic analyses have been published.

**Peer-reviewed / technical literature**: The company has published very limited technical content in open literature. A 2023 Journal of Fusion Energy concept paper exists but was not accessible (Springer paywall; abstract only confirms the approach). Academic literature on proton fast ignition (TNSA-based) is broader but primarily covers small-scale experiments (sub-kJ lasers, non-D-T targets) that cannot be extrapolated to plant scale. The Optica OPN June 2023 feature provides a useful science overview [1].

**Company transparency**: The most informative public source is a Physics World interview with Principal Scientist Debbie Callahan [2], which discloses gain targets, rep rate, laser efficiency targets, and energy conversion approach. The company website and press releases add manufacturing emphasis and the Amplitude partnership but are marketing documents [3][4]. No whitepaper, no system-level design disclosure, and no cost estimates have been published.

**Independent analyses**: The Xcimer/IFE commercialization white paper (XEC 2026) provides IFE-class benchmarks relevant to driver costs but addresses Xcimer's KrF architecture, not Focused Energy's DPSSL + petawatt scheme [5]. The OSTI IFE status review (purl-2561299) provides laser IFE energetics requirements that apply generically [6].

**Phase 1a dossier coverage**: The dossier (17-laser-icf-direct-drive) captured Focused Energy taxonomy values but was originally compiled alongside Xcimer. After concept splitting, most quantitative plant data in the dossier traces to Xcimer or HYLIFE heritage sources. Focused Energy-specific economics are absent.

**Key data gaps that limit this analysis**: no chamber design, no published capsule design (Pearl™ geometry is unpublished), no disclosed blanket type, no LCOE or capital cost estimate, no laser cost for the Focused Energy specific configuration, and no experimental fast ignition gain data at relevant scale.

---
[1] optica-opn-home-articles-volume-34-june-2023-features.md, §Direct-drive overview and fast ignition  
[2] focused-energy-callahan-interview.md, §Gain targets and plant parameters  
[3] focused-energy-technology.md, §Pearl fuel and manufacturing  
[4] prnewswire-news-releases-focused-energy-and-amplitude-enter.md, §Amplitude partnership  
[5] xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md, §Xcimer Laser Cost and Schedule  
[6] osti-servlets-purl-2561299.md, §Basic IFE power-plant energetics requirements  

---

## Section 2: Challenges in Capturing System Function

### Challenge 1: Proton Coupling Efficiency — The Central Unknown

The proton fast ignition scheme inserts an additional physics step between laser energy and fusion yield that is entirely absent from central hot spot (CHS) ignition (indirect or direct drive). A petawatt short-pulse laser irradiates a metal foil embedded in the capsule, generating a proton beam via Target Normal Sheath Acceleration (TNSA). That proton beam must then propagate through the cone structure into the compressed DT core and deposit its energy in a small, correctly positioned hot spot.

The coupling efficiency of this chain — petawatt laser energy → proton kinetic energy → hot-spot heating — is the dominant LCOE uncertainty and has never been measured at the areal densities, pressures, and spatial scales required for ignition. Small-scale experiments at single-shot petawatt facilities have characterized TNSA proton spectra, but the conversion efficiencies achieved (typically ~1–10% laser-to-proton-beam, with broad energy spectra and large angular divergence) impose severe constraints on the fraction of proton energy that reaches the compressed hot spot. Focused Energy does not disclose their assumed coupling efficiency.

For TEA purposes, the coupling efficiency η_coup acts as a multiplier on the gain: if only 5% of petawatt laser energy deposits usefully in the core, the effective gain attributed to the ignition pulse is dramatically reduced. This cannot be constrained with existing data; the range of defensible assumptions spans roughly an order of magnitude. Any LCOE model should treat η_coup as the primary sensitivity parameter and bracket the result between optimistic (30%) and pessimistic (5%) coupling.

### Challenge 2: Dual-Laser System Sizing and Cost

Unlike single-driver IFE concepts (Xcimer's KrF or Inertia's DPSSL), Focused Energy operates two fundamentally different laser systems:

- **Compression laser**: DPSSL (Nd:glass or similar), frequency-doubled to 527 nm, nanosecond pulses, ~10% wall-plug efficiency target [2], $40M Amplitude partnership for development [4]
- **Ignition laser**: Petawatt-class ultrashort pulse (picoseconds), generates proton beam; technology class: Ti:sapphire CPA or OPCPA

These two laser systems have different cost scaling laws, different component supply chains, different maintenance rhythms, and different repetition-rate limitations. The compression laser must run at ~10 Hz continuously; petawatt Ti:sapphire lasers have never been demonstrated at 10 Hz at relevant energies. The laserfocusworld source states the experimental facility is designed for "about 10 per second" eventually, but the T-STAR facility initially operates at "one shot every 60 seconds" for design iteration [7].

The DPSSL cost class (comparable to Inertia's Thunderwall) runs $700–$1,000/J at FOAK scale [5]. The petawatt ignition laser adds a second capital cost line item with no published cost estimate. The combined driver cost will be higher than a single-driver DPSSL plant of equivalent compression energy, while the net gain benefit of fast ignition (if realized) must justify this premium.

> "one of the big thrusts for our company is to develop more efficient lasers that are driven by diodes"
> — focused-energy-callahan-interview.md, §Laser technology

The primary published systems study for fast ignition economics is Meier (2006) [OSTI purl-1438678], which finds FI achieves approximately 15% lower COE than central ignition (CI) at 10 Hz operation (~6.1 ¢/kWeh FI vs. ~7.2 ¢/kWeh CI) and a similar advantage at the unconstrained optimal rep rate (~5.9 ¢/kWeh FI vs. ~6.8 ¢/kWeh CI). However, this advantage rests on an explicit assumption: the ignition laser carries zero incremental $/J capital cost relative to the compression driver. The Meier study notes this directly:

> "The 3ω fast ignition gain curve gives a 15% decrease in the COE (assuming no added $/J for the ignitor laser)."
> — osti-servlets-purl-1438678.md, §Results and Potential Advantages for Fast Ignition

The Meier study makes no attempt to model what happens if the ignition laser carries a positive $/J premium. Because this analysis cannot constrain the ignitor laser cost (Gap #3), the sign of the FI economic advantage relative to CHS direct drive is unresolved: FI may be cheaper or more expensive than CI depending entirely on whether the ignitor laser's $/J cost is near zero (full advantage) or comparable to the compression laser (advantage eliminated). This conditional structure should be made explicit in any LCOE model.

### Challenge 3: Gain Requirement vs. Physics Maturity Gap

Commercial IFE requires the product of laser wall-plug efficiency and target gain to exceed ~10: η_wp × G > 10 [6]. With η_wp ~ 10%, the minimum gain is G > 100 (including proton coupling losses).

> "Total diode cost is a dominant capital cost for such fusion power plant. A diode cost of ~$0.01/W is required for a cost competitive fusion power plant."
> — osti-servlets-purl-2561299.md, §Basic IFE power-plant energetics requirements

Focused Energy targets G > 50, stating they need "significantly higher gains of more like 50 to 100" [2]. The NIF's best indirect-drive result is Qsci ~ 4.1 (April 2025). Direct-drive ignition has not been demonstrated in any configuration. Fast ignition has not demonstrated gain > 1 at any scale. The gap between current experimental state-of-art and the commercial requirement is larger for fast ignition than for CHS direct drive, because fast ignition must validate an additional undemonstrated physics step. This propagates into a very wide uncertainty band on the LCOE: if the physics falls short, the required laser energy (and cost) rises steeply.

Two gain thresholds are relevant for TEA, and they are materially different: (1) the **energetics viability threshold** — G > 100 at η_wp = 10%, sufficient for net electricity production with non-catastrophic recirculating power fraction [6]; and (2) the **economic competitiveness threshold** — G > ~400 under mid-range economic parameters, as found by Hawker (2020) [PMC-7658748], which is the gain level required for competitive LCOE in an electricity market context. The Hawker study makes the distinction explicit:

> "It is often stated that a gain of 30–100 is required for power production from inertial fusion. This conclusion comes from consideration of the driver and thermodynamic efficiencies... Taken literally, the conclusion on required gain is true; a gain in that range is necessary for power production, but the analysis says nothing about cost. Fusion must be cost competitive in a market of different energy technologies."
> — pmc-articles-pmc7658748.md, §Introduction

Focused Energy's commercial target of G = 50–100 falls below both thresholds. Achieving ignition at G = 50–100 would confirm net energy gain but would not produce a commercially competitive LCOE under mid-range cost assumptions — further gain improvements would still be required. The Hawker framework also notes that if cost parameters fall toward the optimistic end of their range, competitive LCOE is achievable at G < 100, but this requires simultaneously favorable assumptions on multiple cost parameters. The TEA should model the Focused Energy scenario against both thresholds and quantify the gain shortfall to each.

### Challenge 4: Target Fabrication at ~10 Hz (900,000/day)

> "it's pretty complicated to figure out how to build 900,000 targets a day at a reasonable cost"
> — focused-energy-callahan-interview.md, §Target manufacturing challenge

The fast ignition capsule (Pearl™) is more complex than a CHS direct-drive capsule: it incorporates a metal cone structure in the shell wall to guide the proton beam to the compressed core. This cone must be precisely aligned and fabricated to tolerances that the high-pressure implosion does not degrade before ignition. No mass production process for cone-in-shell cryogenic DT capsules exists; the geometry is inherently more difficult to fabricate and quality-check than a symmetric sphere. NIF fabricates ~400 targets per year; Focused Energy requires 900,000 per day (a factor of ~800,000× increase).

> "It's a very complicated design that needs to bring together all the pieces of the power plant in a consistent way"
> — focused-energy-callahan-interview.md, §Target design integration

### Challenge 5: Chamber Clearing at 10 Hz

Each shot vaporizes and partially ionizes the target and surrounding gas. At 10 Hz, the chamber must clear debris within ~100 ms to allow injection of the next target. Unlike Xcimer's thick-liquid FLiBe concept (which uses gravity-fed jets that clear between shots on a sub-Hz timescale), Focused Energy has disclosed no specific chamber concept. The combination of higher rep rate, the cone-in-shell target geometry (which may produce asymmetric debris), and the absence of any disclosed chamber design creates a major modeling gap.

### Challenge 6: O&M Structure (Missing)

No breakdown of fixed vs. variable O&M costs, scheduled vs. unplanned maintenance intervals, or component replacement schedules has been published. As a pulsed system at 10 Hz, the laser optics, beam delivery, and target injection systems will accumulate shot-cycle fatigue at high rates. Placeholder O&M should be included in any LCOE model at ~5–8% of direct capital per year (IFE analogue from HYLIFE-II heritage [8]) with wide uncertainty bounds.

### Modeling Approach

**Framework**: The 1costingfe cost model is appropriate for this concept. Focused Energy's plant is D-T fuel with a conventional steam Rankine cycle — the standard IFE cost architecture applies. The dual-laser driver is handled as an additive cost overlay on the CAS22 driver sub-account: a `ignition_laser_cost_premium_frac` parameter multiplies the base DPSSL driver cost to represent the petawatt ignition laser capital, sweeping from 0.0 (Meier "free ignitor" assumption) to 0.65 (pessimistic dual-driver premium).

**Top three LCOE levers (ranked by uncertainty-weighted leverage)**:
1. **Availability / capacity factor** — pulsed systems at 10 Hz accumulate shot-cycle fatigue; availability drives the revenue denominator and is the highest-elasticity parameter
2. **Engineering gain (q_eng)** — determined by η_coup × G product; every 10% reduction in coupling efficiency translates directly to lower q_eng and higher required laser energy
3. **Driver capital (CAS22)** — DPSSL cost floor ($0.01/W diode target) is unachieved; ignitor laser cost premium is unquantified; combined they are the largest single CAPEX uncertainty

Note: eta_th and construction_time_yr carry higher raw elasticity (−0.246 and +0.260 vs. +0.064 for driver capital) but are treated as near-fixed for this concept — the Rankine steam cycle is confirmed by Focused Energy, and construction time is constrained by project scheduling assumptions. Driver capital is the most consequential *uncertain* lever despite its lower elasticity coefficient.

**Three testable hypotheses for the cost model**:
- **H1**: Achieving η_coup ≥ 15% is necessary for q_eng > 4.0 at the stated compression + ignition laser energies — test by sweeping η_coup from 0.05 to 0.30
- **H2**: The FI economic advantage over CI (from Meier 2006) disappears when ignitor laser cost premium exceeds ~20% of compression driver cost — test by sweeping `ignition_laser_cost_premium_frac` from 0 to 0.65
- **H3 (not model-testable in 1costingfe)**: The 1costingfe framework treats repetition rate as a revenue-denominator scaling variable, producing negligible LCOE elasticity (f_rep: −0.004). The Meier 2006 result (+4% COE penalty at 10 Hz vs. the 20–25 Hz optimum, +16% at 5 Hz) arises from rep-rate-dependent driver capital amortization — per-shot driver costs spread over more shots at higher rep rate — a cost structure not implemented in 1costingfe. The Meier result should be treated as an external constraint from a Meier-class systems model (citing ~6.1 ¢/kWeh at 10 Hz vs. ~5.9 ¢/kWeh at 21 Hz for FI), not as a 1costingfe output. A rep rate sweep is retained in the model for reference but cannot reproduce the Meier penalty structure.

---
[2] focused-energy-callahan-interview.md  
[4] prnewswire-news-releases-focused-energy-and-amplitude-enter.md  
[5] xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md, §DPSSL costs  
[6] osti-servlets-purl-2561299.md, §Energetics  
[7] laserfocusworld-lasers-sources-article-14274951-can-high.md, §Funding fusion  
[8] osti-servlets-purl-6137961.md, §Summary and conclusions  
[9] osti-servlets-purl-1438678.md, §Results and Potential Advantages for Fast Ignition (Meier 2006)  
[10] pmc-articles-pmc7658748.md, §Results and Introduction (Hawker 2020)  

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**Proton Fast Ignition Physics at Relevant Scale — TRL 1–2**

- **Demonstrated**: TNSA proton acceleration at single-shot petawatt facilities (OMEGA EP, NIF ARC, ELI, Amplitude); proton beams with energies up to ~100 MeV generated; cone-guided fast electron experiments at Osaka (FIREX-I), though not achieving ignition. Focused Energy has completed "first two science and technical milestones" under a DOE cooperative agreement [4].
- **On paper only**: Proton fast ignition gain calculations in ICF hydrocodes; cone-in-shell implosion simulations predicting hot-spot coupling efficiency.
- **Missing at scale**: Demonstration of ignition-relevant proton coupling at compressed areal densities (ρR > 0.3 g/cm²); gain > 1 under any fast ignition configuration; scaling of coupling efficiency from kJ experiments to 150 kJ ignition laser; suppression of proton beam divergence and energy spread at large aperture.

> "In fast ignition, a high intensity ultrashort picosecond laser pulse (delivering ≈10^15 W/cm^2 on target) is used to generate a fast electron or proton beam that locally heats the compressed fuel to ignition temperatures."
> — osti-servlets-purl-2561299.md, §Laser fusion schemes

> "In principle relaxes symmetry requirements and saves laser energy [but] creates major headaches of its own."
> — optica-opn-home-articles-volume-34-june-2023-features.md, §Pros and cons

---

**High-Repetition-Rate Petawatt Ignition Laser — TRL 2–3**

- **Demonstrated**: Single-shot petawatt lasers at multiple facilities (NIF ARC, OMEGA EP, ELI-NP); Amplitude's ultrafast lasers at sub-Hz repetition. The T-STAR facility is planned with 4 short-pulse beamlines from 2028.
- **On paper only**: 10 Hz petawatt-class operation at kJ energy scale; thermal management of Ti:sapphire or OPCPA gain media at high average power.
- **Missing at scale**: 10 Hz repetitive operation at 150 kJ picosecond pulse energy; thermal deformation control of large aperture optics under continuous 10 Hz loading; optics damage mitigation at high fluence.

The T-STAR experimental facility is initially operating at 1 shot per minute for design iteration [7]; the gap to 10 Hz plant operation is substantial.

---

**Cone-in-Shell Target Design and Mass Production — TRL 2–3**

- **Demonstrated**: Single targets fabricated by Focused Energy's Darmstadt targetry lab; company self-identifies as "one of the only target labs in the world to design and optimize fusion fuel" [3]. NIF-class symmetric spherical DT capsule fabrication at ~400/year.
- **On paper only**: Pearl™ capsule design with cone insert; mass fabrication process concepts (3D printing, emulsion polymerization, holographic methods noted in literature [6]).
- **Missing at scale**: Cone-in-shell geometry at DT cryogenic conditions; quality-control processes for 900,000 capsules/day; demonstrated cone alignment tolerance surviving implosion pre-ignition; laser–proton conversion at production-quality targets vs. hand-fabricated research targets. The cone introduces a crack in spherical symmetry that likely increases hydrodynamic instability sensitivity relative to symmetric CHS targets.

> "there is little experimental data on wetted foam targets. Their viability in terms of target physics and low cost of ~10¢'s/target must be demonstrated."
> — osti-servlets-purl-2561299.md, §Target manufacturing and delivery

---

**DPSSL Compression Laser at 10% Efficiency / 10 Hz — TRL 3–4**

- **Demonstrated**: DPSSL technology at kJ scale demonstrated; Amplitude Ti:sapphire / OPCPA systems at Hz-class rates; Focused Energy's Bay Area facility developing kilo-joule class compression beamlines with Amplitude [4]; NIF-class Nd:glass at <0.1% efficiency (single-shot reference only).
- **On paper only**: 400 kJ compression laser at 10 Hz with 10% wall-plug efficiency; required laser diode cost floor of ~$0.01/W [6] not yet achieved at scale.
- **Missing at scale**: Diode-pumped average power at 10 Hz continuously; thermal management of gain medium at 40 kW average optical input; beam uniformity requirements for symmetric direct-drive implosion at this scale; full 8-beamline (4 long-pulse + 4 short-pulse) integration planned for T-STAR.

---

**Chamber Clearing and Debris Mitigation at 10 Hz — TRL 4–5**

- **Demonstrated**: Conceptual chamber clearing schemes (gas jet, magnetic divertor, liquid wall) analyzed in ICF literature; Xcimer's FLiBe thick-liquid concept analyzed for sub-Hz clearing.
- **On paper only**: No chamber concept disclosed by Focused Energy. At 10 Hz, chamber must clear within 100 ms — significantly more demanding than Xcimer's ~1–2 second clearing interval.
- **Missing at scale**: Chamber geometry compatible with both beam delivery and target injection at 10 Hz; debris characterization from cone-in-shell targets (asymmetric explosion expected); final optics protection from 14 MeV neutron and X-ray flash.

---

**Tritium Breeding and Extraction — TRL 4–6**

- **Demonstrated**: Lithium blanket breeding confirmed as the approach; SRNL (Savannah River National Lab) partnership for tritium extraction system design [2]. Li-6 enrichment for tritium breeding is commercially practiced for fission (ITER uses it).
- **On paper only**: Integrated tritium extraction at 10 Hz pulsed plant. Blanket type not specified; no TBR analysis published.
- **Missing at scale**: Specific blanket chemistry, tritium inventory management, permeation barriers; extraction at rate matching 10 Hz production.

> "Making sure that we have enough tritium, and figuring out how to extract that material to use it for future shots, is a big task."
> — focused-energy-callahan-interview.md, §Tritium challenges

---

**Steam Rankine Energy Conversion — TRL 9**

Focused Energy explicitly adopts a conventional steam cycle without modification [2]. This is the sole TRL-9 subsystem.

> "We will use a conventional steam cycle to convert the heat into electricity. It's funny – we'll have this very hi-tech way of producing heat, but at the end of the day, we will use a traditional system to produce the electricity from that heat."
> — focused-energy-callahan-interview.md, §Energy conversion

---

## Section 4: Key Materials and Supply Chain Considerations

### Tritium (D-T Fuel Cycle)

Standard D-T IFE constraints apply. Tritium is bred from lithium in the blanket; deuterium is extracted from seawater. The startup tritium inventory (estimated 1–3 kg for initial loading before breeding equilibrium) must be sourced from CANDU or fission reactor production. Blanket type is unspecified for Focused Energy, preventing TBR calculation. At 10 Hz with target DT inventory per shot (approximately 0.1–0.5 mg DT per target, consistent with IFE-class capsules), tritium consumption is high: at 10 Hz and ~0.2 mg DT per shot, annual tritium throughput is ~63 g/year through the plasma (before breeding credit). A breeding ratio TBR > 1.05 is required for self-sufficiency. Without a disclosed blanket design, this constraint cannot be verified.

### Laser Diodes (DPSSL Supply Chain)

The compression laser is a DPSSL, making semiconductor laser diodes the principal capital-cost scaling challenge. Literature consistently identifies the diode cost floor as the binding economic constraint:

> "A diode cost of ~$0.01/W is required for a cost competitive fusion power plant."
> — osti-servlets-purl-2561299.md, §Laser driver requirements

Current commercial diode pump modules for Nd:YAG applications cost approximately $0.1–$1/W. The factor-of-10 to factor-of-100 cost reduction required is significant. The Xcimer/TRUMPF analysis (cited in the indirect drive exemplar) places the floor at $0.007/W for economic viability. Focused Energy's Amplitude partnership is explicitly aimed at laser technology development toward this target, but no specific cost trajectory has been published.

Diodes for ultrashort petawatt lasers (Ti:sapphire or OPCPA pump) represent a separate supply chain. Ti:sapphire pump lasers (Nd:YAG or Nd:YLF) also use diode pump technology at shorter pulse lengths, but different suppliers than the long-pulse compression chain.

### Target Materials (Cone-in-Shell Capsule)

The Pearl™ capsule geometry is not publicly described beyond "millimeter-scale deuterium/tritium fusion fuel targets" [4]. Inferred from fast ignition literature: a plastic or beryllium ablator shell, a DT ice layer, and a high-Z metal cone (typically gold or copper in research experiments) inserted through the shell wall. Gold is a scarce and expensive material; substitution of aluminum or other low-Z metals has been studied but with reduced coupling efficiency. If gold cones are required at 900,000 targets/day, this creates a significant supply chain demand: at ~1 mg gold per cone (representative research experiment scale), annual demand would be ~30 tonnes — a small but non-negligible fraction of annual global gold production (~3,500 tonnes/year). Reduced-gold or non-gold designs are being pursued but remain unvalidated.

### Blanket and Chamber Materials

No blanket material disclosed. Focused Energy confirms "lithium in the reactor" [2] for tritium breeding, but the chemistry (liquid Li, LiPb, FLiBe, or solid ceramic) is unknown. The choice has major supply chain implications: FLiBe requires beryllium (limited suppliers, export-controlled); liquid Li requires active safety systems; LiPb is less restrictive. Li-6 enrichment is required regardless of blanket type to achieve adequate TBR.

### Final Optics (Laser Beam Delivery)

Both laser systems require final focusing optics that are exposed to X-ray and neutron flux from each shot. At 10 Hz, damage accumulates rapidly. Neither a protective scheme nor an optics replacement strategy has been disclosed. The IFE literature treats this as one of the most intractable engineering problems:

> "significant progress is required in developing materials that can withstand the neutron and radiation fluxes"
> — osti-servlets-purl-2561299.md, §Additional considerations

Xcimer's KrF approach uses nonlinear gas optics (SBS/Raman compression) to avoid final solid optics in the damage zone — an approach not available to the DPSSL-based Focused Energy concept.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Target gain (Qsci) | 50–100 | focused-energy-callahan-interview.md §Gain targets | medium | Commercial target; not yet demonstrated at any scale in fast ignition |
| Engineering gain (Qeng) | >1 (pilot target) | focused-energy-callahan-interview.md §LightHouse | low | LightHouse pilot plant goal; no supporting calc published |
| Laser wall-plug efficiency (DPSSL) | ~10% | focused-energy-callahan-interview.md §Laser efficiency | medium | Target, not demonstrated at 10 Hz / plant scale |
| Repetition rate | ~10 Hz (900,000 shots/day) | focused-energy-callahan-interview.md §Rep rate | high | Commercial plant target; T-STAR at 1 shot/60 s currently. Meier 2006 (purl-1438678) finds COE minimized at 20–25 Hz; 10 Hz constraint imposes ~+4% COE penalty vs. optimal |
| Compression laser energy per shot | ~400 kJ (long-pulse) | laserfocusworld-lasers-sources-article-14274951-can-high.md §Facility specs | medium | T-STAR facility spec; commercial plant undefined |
| Ignition laser energy per shot | ~150 kJ (picosecond) | laserfocusworld-lasers-sources-article-14274951-can-high.md §Facility specs | medium | T-STAR facility spec; commercial plant undefined |
| Energy conversion cycle | Conventional steam (Rankine) | focused-energy-callahan-interview.md §Steam cycle | high | Explicitly confirmed |
| Net electrical output | ~GWe scale | focused-energy-callahan-interview.md §Power plant scale | low | "Gigawatt-scale" only; no specific number |
| Pilot plant cost (LightHouse) | ~$3B | laserfocusworld-lasers-sources-article-14274951-can-high.md §Funding fusion | low | Single data point, no breakdown |
| DPSSL driver cost (class) | $700–$1,000/J (FOAK) | xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Laser cost benchmarks | low | Applies to DPSSL class broadly; Focused Energy has not published own figure |
| Tritium source | Li blanket (type unspecified) | focused-energy-callahan-interview.md §Tritium | medium | SRNL partnership for extraction design |
| Target cost requirement | <10% electricity value per target | xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Target economics | medium | Industry benchmark (Goodin et al. 2004); [inferred: ~$0.25–$1 per shot at 10 Hz plant economics] |
| η_wp × G minimum for energetics viability | >10 (G > 100 at η_wp = 10%) | osti-servlets-purl-2561299.md §Energetics | high | Fundamental IFE net-electricity threshold; necessary but not sufficient for economic competitiveness |
| G minimum for economic competitiveness | ~400 (mid-range parameters) | pmc-articles-pmc7658748.md §Results | medium | Hawker 2020 LCOE model; "For the mid-range default parameters used in this study, this gain threshold is around 400." Competitive LCOE achievable at G < 100 only if multiple cost parameters are simultaneously optimistic. Focused Energy's G = 50–100 target falls below both thresholds. |
| FI COE advantage over CI (Meier 2006) | ~15% lower at 10 Hz (6.1 vs. 7.2 ¢/kWeh) | osti-servlets-purl-1438678.md §Results and Potential Advantages for Fast Ignition | low | Explicitly assumes zero added $/J for ignition laser. Advantage sign unresolved if ignitor carries positive capital cost. |
| Fuel: D-T burn-up fraction | ~30% [analogue] | osti-servlets-purl-2561299.md §Target gains | low | High-gain IFE target analogue; Focused Energy specific unconfirmed |
| Capacity factor assumption | ~75% [analogue] | osti-biblio-7021072.md §HYLIFE-II baseline | low | HYLIFE-II conservative baseline; 85% sensitivity case; Focused Energy undisclosed |
| O&M (annual, % of CAPEX) | ~5–8% [analogue] | osti-servlets-purl-6137961.md §Summary | low | HYLIFE-II heritage; no Focused Energy data |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Proton coupling efficiency (η_coup) | truly-unknown | blocking | The key fast-ignition-specific parameter; range ~5–30% from first principles; never measured at plant-relevant conditions |
| Capsule gain at relevant compression + fast ignition | truly-unknown | blocking | No fast ignition experiment has achieved gain > 1 at any scale |
| DPSSL cost $/J (Focused Energy specific configuration) | proprietary | blocking | Class cost $700–1,000/J; Amplitude partnership may reduce; no figure published |
| Petawatt ignition laser cost $/J | truly-unknown | blocking | Ti:sapphire / OPCPA at 10 Hz, 150 kJ — no commercial precedent |
| Chamber design (geometry, material, clearing scheme) | proprietary | blocking | Not disclosed; required for 14 MeV neutron load, debris mitigation, final optics protection |
| Blanket type and TBR | proprietary | blocking | Lithium blanket confirmed but chemistry undisclosed; TBR calculation impossible |
| Net electric power (plant-level) | proprietary | blocking | "Gigawatt-scale" only |
| Capacity factor | proprietary | important | Not published |
| Target design (Pearl™ composition, cone material, geometry) | proprietary | important | Required for target cost model; mass production feasibility assessment |
| Target cost ($/target at 900,000/day) | proprietary | important | Feasibility threshold ~$0.25–$1; no cost estimate published |
| LCOE estimate | truly-unknown | nice-to-have | No independent analysis or company projection published |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Proton coupling efficiency (η_coup): petawatt laser → proton beam → compressed core | S2, S5 | truly-unknown | blocking | TNSA coupling literature; FIREX-I experimental data; Focused Energy J. Fusion Energy 2023 (Springer, behind paywall) |
| 2 | Fast ignition gain at relevant areal density; capsule gain in full compression + fast ignition experiments | S2, S5 | truly-unknown | blocking | Osaka FIREX-I/II results; RAL experimental data; NIF ARC fast ignition experiments |
| 3 | Petawatt ignition laser cost ($/J) at 10 Hz | S2, S3, S5 | truly-unknown | blocking | No commercial precedent; engineering study required |
| 4 | DPSSL compression laser cost (Focused Energy specific $/J) | S5 | proprietary | blocking | Amplitude partnership details not public |
| 5 | Chamber design (geometry, material, clearing scheme, first-wall approach) | S2, S3 | proprietary | blocking | Focused Energy technical papers; DOE cooperative agreement deliverables |
| 6 | Blanket type and TBR analysis | S3, S4, S5 | proprietary | blocking | Focused Energy J. Fusion Energy 2023; SRNL collaboration outputs |
| 7 | Net electrical output and plant-level energy balance | S5 | proprietary | blocking | No published system-level design study |
| 8 | Target design (Pearl™ geometry, cone material) | S3, S4 | proprietary | important | Darmstadt targetry lab publications; patent filings |
| 9 | Target cost at mass production scale (900,000/day) | S4, S5 | truly-unknown | important | No mass-production feasibility study published for cone-in-shell geometry |
| 10 | Capacity factor and availability model | S5 | proprietary | important | Not disclosed; engineering estimate from pulsed IFE analogues |
| 11 | Final optics protection scheme at 10 Hz | S3 | truly-unknown | important | No concept disclosed; requires independent design study |
| 12 | Energy split optimization between compression and ignition lasers | S2 | truly-unknown | important | Hydrosimulation study; not publicly available |
| 13 | O&M cost breakdown (fixed/variable, scheduled maintenance, replacement cycles) | S2 | proprietary | important | No IFE O&M breakdown published; HYLIFE heritage analogue available |
| 14 | LCOE estimate (independent) | S5 | not-yet-sourced | nice-to-have | GEM (LLNL) could be applied; PROCESS (UKAEA) supports IFE configurations |

---

## Section 7: Cross-Concept Notes

Only one approved prior analysis was available at the time of this analysis: **21-spherical-tokamak-hts** (Tokamak Energy). The spherical tokamak shares no cost structures, subsystems, or materials with fast ignition IFE. No cross-concept assumptions were reused.

**Nearest-neighbor analyses (not yet approved, referenced for context):**

**17a-laser-icf-hybrid-drive (Xcimer Energy — D-T Hybrid Direct Drive)** is the closest TEA comparator: same fuel (D-T), same driver class (DPSSL for Xcimer's baseline), same chamber clearing challenge (~sub-Hz), same broad IFE economic framework, and same steam or gas Brayton energy conversion. The key difference for TEA is the ignition scheme: Xcimer uses hybrid direct drive (single KrF driver, CHS implosion) while Focused Energy uses DPSSL compression + a separate petawatt ignition laser. The 17a model baseline (400 MWe, He Brayton 45%, laser at $70/J) produces 100.2 $/MWh (87.1 $/MWh scaled to 1 GWe). The 17b FI baseline is 67.6 $/MWh at 1 GWe with Rankine 40%. These figures are not directly comparable — they differ in scale, thermal cycle, driver cost parameterization, and availability assumptions — but both inhabit the same IFE capital structure.

**04-laser-icf (HB11 Energy — p-B11 fast ignition)** shares the fast ignition physics architecture (petawatt ignition laser, TNSA-class particle beam, dual-driver) but is TEA-dissimilar: p-B11 fuel eliminates the tritium breeding cost (blanket CAS22 sub-account), reduces the neutron management cost, and requires substantially higher gain due to the lower reaction cross-section. The dual-driver cost uncertainty is structurally identical, but cross-concept LCOE comparisons are misleading without isolating the physics step from the fuel cycle.

**26-laser-icf-indirect-drive** (Inertia Enterprises) and **17a** provide the most directly relevant benchmarks for IFE economics (DPSSL cost class, chamber, target economics). Key divergences relative to fast ignition:

- *Driver technology*: Indirect drive (Inertia) uses a single DPSSL (~$700–1,000/J FOAK). Fast ignition uses DPSSL compression + petawatt ignition — two capital line items vs. one. The DPSSL cost class is shared; the petawatt laser adds cost with no CHS analogue.
- *Rep rate*: Focused Energy (10 Hz) is comparable to Inertia (10 Hz) and much higher than Xcimer (sub-Hz). Chamber clearing requirements are similarly demanding at 10 Hz.
- *Target complexity*: CHS direct-drive capsules are symmetric spheres. Fast ignition cone-in-shell capsules are inherently asymmetric and more complex to fabricate, likely more expensive per unit. The $1/target CHS benchmark cannot be assumed transferable.
- *Physics maturity*: Indirect drive ignition demonstrated (NIF, 2022). Direct drive ignition not demonstrated. Fast ignition gain > 1 not demonstrated. The physics maturity gap is the defining risk differentiator.
- *Energy conversion*: All IFE D-T concepts converge on thermal cycles (steam or He Brayton). This is shared infrastructure.
- *Tritium breeding*: Focused Energy's undisclosed blanket vs. Xcimer's characterized FLiBe HYLIFE-III design. FLiBe cost data cannot be applied without blanket type confirmation.

**TEA threshold analysis — ignitor laser cost premium**: The central TEA question for fast ignition is whether the FI economic advantage over CHS direct drive (~15% lower COE at 10 Hz, per Meier 2006, assuming zero ignitor cost) survives once the petawatt ignition laser is priced as a real capital line item. Applying the Meier FI/CI ratio, a CHS D-T equivalent in the 1costingfe framework would be approximately 67.6 / 0.85 ≈ 79.5 $/MWh at the same scale and cost assumptions. The ignitor premium sweep shows LCOE rising from 67.6 to 70.0 $/MWh at +65% ignitor premium — a 3.5% increase, still 12% below the Meier-implied CI reference. The FI economic advantage persists across the entire modeled premium range. Two caveats apply: (1) the model's driver capital elasticity is only 6.4%, and the baseline CAS22 driver cost is already a lower bound (dual-driver architecture not yet fully captured), so the true breakeven likely requires a larger premium than the model can cleanly test; and (2) cone-in-shell target fabrication cost and asymmetric debris mitigation — both FI-specific cost penalties — are not isolated in the 1costingfe structure. The Focused Energy scenario falls below the theoretical FI/CI breakeven in the modeled range, but a formal comparison against a CHS-equivalent 1costingfe parameterization has not been performed.

**Key implication for cross-concept comparisons**: Focused Energy's fast ignition concept carries an additional undemonstrated physics step (proton fast ignition) on top of the already-undemonstrated direct-drive ignition — making it strictly more speculative than its nearest IFE neighbors. The TEA should flag this as a risk multiplier on any cost estimate derived from CHS IFE analogues.

---

## Section 8: Sources

Listed in order of importance to this analysis.

1. **Physics World / Focused Energy — Debbie Callahan Interview** (2023)  
   *"Focusing on Fusion: Debbie Callahan talks commercial laser fusion"*, Physics World  
   Primary source for Focused Energy-specific parameters: gain targets (50–100), rep rate (10 Hz / 900,000 shots/day), laser efficiency (~10%), steam cycle confirmation, tritium breeding approach, SRNL partnership.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-02/sources/focused-energy-callahan-interview.md`

2. **Laser Focus World — "Can High-Power Lasers Enable Fusion Energy?"** (2023)  
   Facility specifications for Focused Energy's T-STAR laser system: 400 kJ compression, 150 kJ picosecond ignition, ~$3B total facility cost, 2029 ignition timeline.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/laserfocusworld-lasers-sources-article-14274951-can-high.md`

3. **Optica OPN — "Fusion's Direct Drive"** (June 2023, Vol. 34)  
   Scientific context for fast ignition: relaxed symmetry requirement, coupling challenges, facility cost landscape, Focused Energy pilot plant timeline (end of 2030s), commercial gain and rep rate requirements.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features.md`

4. **OSTI purl-2561299 — IFE Status and Prospects Post-NIF Ignition** (~2023)  
   IFE energetics requirements (η_wp × G > 10), diode cost floor ($0.01/W), target production requirements (900,000/day), description of fast ignition and shock ignition physics relative to CHS approaches, burn-up fraction ~30%.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/osti-servlets-purl-2561299.md`

5. **Xcimer / XEC Commercialization White Paper** (February 2026, Xcimer Energy + TRUMPF)  
   *"Commercialization of Laser Fusion Energy"*  
   DPSSL cost class benchmarks ($700–1,000/J; floor estimate); IFE energetics requirements; Xcimer-specific architecture for comparison context. Not directly about Focused Energy but provides the best published IFE cost benchmarks available.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md`

6. **PRNewswire — Focused Energy and Amplitude $40M Agreement** (2024)  
   Amplitude partnership details; Bay Area Laser Development Facility; T-STAR rep rate (1 shot/60 s initially); Darmstadt targetry lab; $175M+ total funding raised.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/prnewswire-news-releases-focused-energy-and-amplitude-enter.md`

7. **Focused Energy Technology Website** (2024)  
   Pearl™ capsule marketing description; "+30x vs. NIF indirect drive" performance claim; mass production and modularity emphasis.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-01/sources/focused-energy-technology.md`

8. **Xcimer Energy Approach Website** (2024)  
   Xcimer architecture context (HDD, KrF, sub-Hz); cost-per-joule comparison vs. NIF; liquid-wall chamber principle. Referenced for IFE class benchmarks.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-01/sources/xcimer-energy-approach.md`

9. **OSTI biblio-7021072 — HYLIFE-II Abstract** (Moir et al., 1994)  
   HYLIFE-II LCOE reference: 4.4 ¢/kWh at 1 GWe (heavy-ion driver, 1994 dollars); 75% availability baseline; 30-year chamber lifetime with FLiBe liquid wall. Used as IFE O&M and availability analogue.  
   Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/osti-biblio-7021072.md`

10. **OSTI purl-6137961 — HYLIFE-II Power Conversion System Design and Cost Study** (M.A. Hoffman, LLNL, 1990)  
    BOP subsystem breakdown; IHX cost estimates ($18–55/kWth depending on material); BOP fraction of direct CAPEX (~32–48%); preliminary LCOE "much higher than we would like"; 1988-dollar baseline. Used as engineering analogue for BOP cost structure.  
    Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/osti-servlets-purl-6137961.md`

11. **ScienceDirect — HYLIFE-III Nuclear Analysis** (Fusion Engineering and Design, 2024)  
    FLiBe TBR > 1.2 for thick-liquid-wall concept; neutron activation analysis; optics lifespan requirements. Relevant to Xcimer chamber heritage; referenced for IFE blanket TBR context only.  
    Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/sciencedirect-science-article-pii-s0920379624001868.md`

12. **OSTI purl-1438678 — Meier (2006): HAPL Systems Modeling for Fast Ignition** (LLNL)  
    Primary published systems study for FI economics. FI achieves ~15% lower COE than CI at 10 Hz (~6.1 vs. ~7.2 ¢/kWeh) explicitly assuming zero added $/J for the ignition laser. COE minimized at 20–25 Hz; 10 Hz constraint imposes +4% COE penalty vs. optimal; 5 Hz constraint imposes +16%.  
    Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/osti-servlets-purl-1438678.md`

13. **PMC-7658748 — Hawker (2020): A Simplified Economic Model for Inertial Fusion**  
    Technology-agnostic IFE LCOE framework. Finds gain > ~400 required for economic competitiveness under mid-range cost parameters; distinguishes energetics viability (G > 30–100) from economic competitiveness (G > 400). Minimum LCOE of ~$25/MWh achievable with optimistic but not unrealistic parameters. Driver efficiency default 10%; Monte Carlo parameter scan.  
    Path: `knowledge/concept_research/17-laser-icf-direct-drive/iter-03/sources/pmc-articles-pmc7658748.md`
