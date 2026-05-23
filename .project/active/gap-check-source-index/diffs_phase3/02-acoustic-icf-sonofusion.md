# Phase 3 diff: 02-acoustic-icf-sonofusion

**Generated:** 2026-05-22T13:10:06-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 8 | 9 | 1 |
| important_count  | 5 | 7 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: Acoustic ICF / Sonofusion (D-D)
```

## Blocking-tier lines (new)

```
26:- No independently verified evidence of D-D fusion from acoustic cavitation exists in the peer-reviewed literature — `truly-unknown` — **blocking** (the entire concept's physical basis is unvalidated)
27:- Sonofusion Energy has disclosed no technical details about their approach beyond the UCLA spin-off framing — `proprietary` — **blocking** (cannot distinguish from prior failed attempts without access to company thesis)
48:- Physical mechanism for reaching thermonuclear temperatures not disclosed or demonstrated — `truly-unknown`/`proprietary` — **blocking** (system function cannot be modeled without a validated physics basis)
49:- Energy conversion pathway undefined — `truly-unknown` — **blocking** (no plant-level power cycle described anywhere)
50:- Reactor chamber and liquid medium design: does not exist — `truly-unknown` — **blocking**
68:- All fusion-specific subsystems are at TRL 1 or below (no design exists) — `truly-unknown` — **blocking**
89:- PZT transducer lifetime under D-D neutron flux: unknown and potentially fatal to the concept — `not-yet-sourced` — **blocking** (PZT ceramics are known to be radiation-sensitive; this is a fundamental material compatibility question; search radiation effects literature for PZT)
112:| Fusion gain G (target gain) | truly-unknown | blocking | Fusion not demonstrated; best sonoluminescence T is 16,000 K vs. ~10⁸ K needed |
113:| Net electrical output / plant capacity | truly-unknown | blocking | No design exists; requires demonstrated Q > 1 first |
114:| Capital cost (plant, driver, chamber) | truly-unknown | blocking | No plant design; driver would scale very differently from laser/HIF plants |
115:| Operating cost (O&M, liquid replacement, transducer replacement) | truly-unknown | blocking | No design; transducer lifetime in radiation environment unknown |
116:| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | Power cycle undesigned; liquid thermalization plausible but no analysis |
117:| Capacity factor / availability | truly-unknown | blocking | No design; transducer rep-rate wear is uncharacterized at fusion scale |
119:| Target cost (cost per bubble/pulse) | truly-unknown | blocking | "Bubble" is not a manufactured target, but liquid medium replacement rate, transducer replacement, and liquid activation are all unquantified |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/02-acoustic-icf-sonofusion.md	2026-05-22 12:59:21.056246547 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/gap_report.md	2026-05-22 13:10:06.860672953 -0700
@@ -1,14 +1,8 @@
-The gap report already exists and is comprehensive. I've read all the source documents and can validate it. Let me produce the assessment, incorporating observations from the transducer industry sources (Hielscher, APC) that provide some driver cost data.
-
----
-
 # Gap Assessment: Acoustic ICF / Sonofusion (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-**Summary**: Sonofusion Energy is a pre-publication, opaque company with essentially no disclosed technical or engineering specifications. The publicly available literature addresses the physics of sonoluminescence — not a fusion reactor — and the concept's primary scientific challenge (achieving ~10⁸ K from a ~16,000 K demonstrated baseline) remains entirely unaddressed in public sources. A standard D1+ analysis is feasible only if it focuses on the physics gap, historical context, and analogue-based parametric bounding; no LCOE modeling grounded in actual performance parameters is possible.
-
----
+**Summary**: Sonofusion Energy (acoustic cavitation ICF) is categorically pre-scientific for techno-economic analysis: no independently replicated evidence of D-D fusion from acoustic cavitation exists, no plant design has been disclosed, and no LCOE-relevant parameters can be grounded. The concept's founder (Putterman) himself could not replicate Taleyarkhan's earlier fusion claims. Source coverage is adequate for sonoluminescence physics and for documenting the scientific controversy, but there is effectively no data usable for a D1+ economic analysis. Proceeding to full analysis would produce a mostly speculative document with little numerical content.
 
 ## Section Coverage
 
@@ -16,47 +10,45 @@
 **Coverage**: Poor
 
 **Available**:
-- Basic company identity (UCLA spin-off, co-founders Putterman and Camara) — `sonofusion-energy-website.md`
-- General marketing claims (modular, scalable, simple, low cost) without technical substance — `sonofusion-energy-website.md`
-- Underlying sonoluminescence physics: energy concentration ~12 orders of magnitude, plasma density >10²¹ cm⁻³, temperatures 7,000–16,000 K, 40 kHz operating regime — `ucla-putterman-group-sonoluminescence.md`
-- Full history of Taleyarkhan fraud and failed replications across 4+ independent labs (including Putterman's own null neutron result) — `bubble-fusion-scientific-history.md`
-- Historical comparator: Impulse Devices built a ~$250K 1-foot stainless steel sphere sonofusion research reactor — `bubble-fusion-scientific-history.md`
-- Commercial ultrasonic transducer specifications: APC catalog 50W/28kHz to 50kHz units, Hielscher UIP4000hdT at 4kW industrial grade (~24/7 operation) — `americanpiezo-products-services-ultrasonic-power-transducers.md`, `hielscher-uip4000hdt-4kw-high-performance-ultrasonics.md`
-- Statement: >$10M government funding at UCLA — `sonofusion-energy-website.md`
+- **UCLA Putterman Group website** (`iter-01/sources/ucla-putterman-group-sonoluminescence.md`): Documents sonoluminescence physics in detail — energy focusing by 12 orders of magnitude, free electron density >10²¹ cm⁻³, flash durations <50 ps, driving frequencies 30–40 kHz, rep rates up to 10 million/s in multi-bubble mode. Putterman himself attempted to replicate Taleyarkhan's fusion claims (BBC Horizon, 2005) and found no fusion neutrons.
+- **Bubble fusion Wikipedia** (`iter-01/sources/bubble-fusion-scientific-history.md`): Comprehensive record of the 2002–2008 Taleyarkhan affair — original Science paper, Oak Ridge and Purdue failed replications, Naranjo's finding that the reported neutron spectrum was consistent with Californium-252 contamination (not D-D fusion), Purdue misconduct finding (2008), ONR debarment. Establishes the scientific state of the field.
+- **Sonofusion Energy website** (`iter-01/sources/sonofusion-energy-website.md`): Confirms UCLA spin-off, co-founders (Seth Putterman and Carlos Camara PhD), ICF framing ("imploding shockwaves"), and >$10M prior government funding. Zero technical parameters disclosed.
+- **Commercial transducer specs** (Hielscher UIP4000hdT, UIP16000; APC International sources): Industrial ultrasonicators from 4–16 kW per unit at 19–26 kHz using PZT ceramic/titanium construction. Confirms commercial maturity of the driver hardware for non-fusion industrial applications.
+- **Heavy water trade data** (`iter-01/sources/wits-trade-comtrade-en-country-all-year-2023-tradeflow.md`): 2023 global heavy water exports — India ($46M, 100 t), Canada ($38M, 81 t), EU ($8.7M), US ($8.6M). Supply exists but is primarily for CANDU reactor markets.
+- **OSTI piezoelectric harvesting paper** (`iter-01/sources/osti-pages-biblio-1224334.md`): A bibliography of piezoelectric energy harvesting literature (wearables, sensors). Not useful — covers low-power energy scavenging, not high-intensity acoustic transduction for fusion. Provides no relevant data.
 
 **Missing**:
-- Any technical white paper, conference presentation, or DOE/ARPA-E award document from Sonofusion Energy as a company
-- Independent assessment of the company's specific thesis for crossing the ~16,000 K → ~10⁸ K temperature gap
-- Any peer-reviewed paper attributable to the Sonofusion Energy entity (as distinct from Putterman's academic UCLA work)
+- Any technical white paper, investor deck, or DOE/ARPA-E award from Sonofusion Energy explaining their physical thesis for bridging the ~4-orders-of-magnitude temperature gap
+- Peer-reviewed literature demonstrating fusion-relevant conditions in acoustic cavitation
+- Any post-2008 experimental results from the Putterman/Camara group bearing on fusion
 
 **Gaps**:
-- Company technical thesis (mechanism for exceeding sonoluminescence temperature limits) — `truly-unknown` — **blocking** (the entire concept validity rests on this)
-- Funding status and investor disclosures — `proprietary` — **important** (signals whether concept is active beyond website)
-- ARPA-E or DOE program records post-2020 — `not-yet-sourced` — **important**; search ARPA-E Explorer and USASpending.gov for "Sonofusion Energy" or "Seth Putterman" grant awards (`unverified — confirm existence before searching`)
+- No independently verified evidence of D-D fusion from acoustic cavitation exists in the peer-reviewed literature — `truly-unknown` — **blocking** (the entire concept's physical basis is unvalidated)
+- Sonofusion Energy has disclosed no technical details about their approach beyond the UCLA spin-off framing — `proprietary` — **blocking** (cannot distinguish from prior failed attempts without access to company thesis)
+- No post-2008 experimental progress documented in accessible sources — `not-yet-sourced` — **important** (Putterman group may have published new sonoluminescence work; search OSTI, arXiv, PRL)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- Core physics challenge is precisely quantified: demonstrated temperatures (~16,000 K per Flannigan & Suslick 2010) are ~4 orders of magnitude below D-D ignition (~10⁸ K) — `bubble-fusion-scientific-history.md`, `ucla-putterman-group-sonoluminescence.md`
-- Driver mechanism well-understood: piezoelectric ultrasonic transducers, 20–40 kHz, standing-wave liquid chamber; Putterman group achieves 10⁶–10⁷ events/second
-- Pulse structure understood: each bubble collapse is a discrete picosecond event; 40 kHz → 40,000 events/second minimum
-- Liquid medium implies inherent neutron thermalization — natural energy deposition pathway if D-D fusion were achieved
-- Driver simplicity relative to laser or magnetic systems is a genuine claimed advantage; no laser, magnets, particle beams, or pulsed power needed
+- Sonoluminescence bubble collapse physics is well-documented: plasma density >10²¹ cm⁻³, temperatures demonstrated up to ~16,000 K (Flannigan & Suslick 2010, cited in dossier), picosecond pulse durations. Putterman's group characterizes these as a "dense microplasma."
+- D-D fusion requires ~10⁸ K — approximately 6,000× higher than the best experimentally demonstrated sonoluminescence temperature. No physical mechanism for bridging this gap via acoustic cavitation is publicly specified.
+- The operation mode (pulsed at kHz acoustic frequency) and driver architecture (piezoelectric transducer in liquid medium) are described at a high level.
 
 **Missing**:
-- No disclosed path from sonoluminescence plasma (~16,000 K) to fusion-relevant plasma (~10⁸ K) — the company's core scientific claim
-- No system-level description: bubble nucleation technique, chamber geometry, transducer array configuration, liquid recirculation design
-- No energy balance or Q-value projection under any assumption set
-- No failure-mode or plasma stability analysis
+- No description of how the company proposes to reach thermonuclear temperatures
+- No reactor chamber design (geometry, liquid volume, shielding configuration)
+- No energy conversion pathway (how fusion energy deposited in liquid would be extracted as useful heat or electricity)
+- No description of how multi-bubble configurations would be managed for power-producing operation
+- No description of neutron management approach for 2.45 MeV D-D neutrons
 
 **Gaps**:
-- Mechanism for temperature amplification — `truly-unknown` — **blocking**
-- System architecture (chamber geometry, transducer array count and layout, liquid loop) — `proprietary` — **blocking** for any engineering LCOE model
-- Energy gain (Q) projection — `truly-unknown` / `proprietary` — **blocking**
-- Repetition rate needed for net power at plant scale — `derivable` from assumed Q and target power, but Q is unknown — **blocking**
+- Physical mechanism for reaching thermonuclear temperatures not disclosed or demonstrated — `truly-unknown`/`proprietary` — **blocking** (system function cannot be modeled without a validated physics basis)
+- Energy conversion pathway undefined — `truly-unknown` — **blocking** (no plant-level power cycle described anywhere)
+- Reactor chamber and liquid medium design: does not exist — `truly-unknown` — **blocking**
+- Neutron management approach for a liquid-medium D-D system: undefined — `truly-unknown` — **important** (2.45 MeV neutrons would thermalize in liquid medium, but no shielding, activation, or waste management analysis exists)
 
 ---
 
@@ -64,47 +56,39 @@
 **Coverage**: Poor
 
 **Available**:
-- **Ultrasonic transducers**: Commercially mature (TRL 9) for industrial, medical, and sonochemical use. APC standard units at 28–120 kHz; Hielscher industrial units up to 16 kW/unit, 24/7 continuous rated — `americanpiezo-products-services-ultrasonic-power-transducers.md`, `hielscher-uip4000hdt-4kw-high-performance-ultrasonics.md`
-- **Liquid deuterium medium** (heavy water or deuterated acetone): commercially available; no supply constraints at laboratory scale
-- **Sonoluminescence phenomenon itself**: TRL 9 as a physics phenomenon; well-established, reproducible
-- **Neutron detection**: Putterman group designed high-efficiency (20%) nanosecond-timing detectors — relevant to diagnostics only
-- **Historical comparator TRL**: Impulse Devices research reactor (~$250K, tabletop) was TRL 2–3 for basic science, not power generation
-- **Sonofusion as a fusion energy source**: TRL 1 at best; no credible independent fusion demonstration exists
+- **Ultrasonic transducer technology** is commercially mature for non-fusion industrial applications. Hielscher produces units from 50 W to 16 kW (UIP16000), operable 24/7, with PZT/titanium construction. APC International produces 28–120 kHz sandwich transducers with electroacoustic efficiency >50–60%. These are TRL 9 for industrial processing.
+- The acoustic driver subsystem (for industrial use) is the only component at mature readiness. Everything downstream (fusion chamber, energy conversion, shielding, tritium-free D-D fuel handling at scale) is undefined.
 
 **Missing**:
-- Any demonstrated fusion yield from acoustic cavitation (concept is TRL 1 as a fusion energy source)
-- No disclosed engineering design for energy capture, power conversion, or plant integration
-- No materials qualification for neutron-irradiated liquid medium or chamber walls under sustained operation
-- No radiation hardness data for piezoelectric transducers in fusion-relevant neutron flux environments
+- TRL assessment for fusion-specific application of acoustic cavitation (effectively TRL 1–2 at best — basic principles observed but fusion not demonstrated)
+- No subsystem-level TRL assessment exists for any fusion-specific component of a hypothetical sonofusion power plant
+- No design or readiness assessment for: fusion chamber, first wall, neutron shielding, heat exchanger/power cycle, tritium/activation product management, structural materials under D-D neutron fluence
 
 **Gaps**:
-- Acoustic-to-fusion demonstration — `truly-unknown` — **blocking**
-- Energy capture subsystem design and TRL — `truly-unknown` — **blocking**
-- Chamber wall materials qualification under neutron flux — `truly-unknown` — **blocking**
-- Radiation hardness of piezoelectric transducers in D-D neutron environment — `not-yet-sourced` — **important**; PZT ceramics are radiation-sensitive but no data exists for this application
-- Tritium buildup in liquid medium (D-D produces tritium in ~50% of reactions) — `not-yet-sourced` — **important**; no treatment in any available source
+- All fusion-specific subsystems are at TRL 1 or below (no design exists) — `truly-unknown` — **blocking**
+- Acoustic transducer scaling from kilowatt industrial units to power-plant driver arrays: acoustic coupling physics changes at scale; no published scaling study for fusion-relevant power densities — `not-yet-sourced` — **important** (search acoustics/ultrasonics journals for high-intensity cavitation scaling)
+- Reactor vessel/first wall materials for a liquid-medium D-D environment: completely undefined — `truly-unknown` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial
+**Coverage**: Partial (driver materials only)
 
 **Available**:
-- Fuel: deuterium (heavy water ~$1/g, deuterated acetone) — globally available, no supply constraint
-- No rare-earth magnets, no HTS tape, no tritium supply, no beryllium, no cryogenic targets — concept's claimed material simplicity is legitimate
-- Ultrasonic transducers: PZT piezoelectric ceramics — commercial supply chain mature; multiple vendors (APC, Hielscher, others); no strategic material constraints
-- No high-energy laser systems, pulsed power, or cryogenic infrastructure needed
+- **PZT (lead zirconate titanate)** ceramics for piezoelectric transducers: commercially available at industrial scale. APC International source confirms manufacturing process and material specifications for multi-layer stack transducers. Supply chain is mature for industrial ultrasonics.
+- **Titanium and stainless steel** for sonotrodes and reactor bodies (Hielscher UIP series): well-characterized industrial supply chains.
+- **Deuterium (heavy water)**: commercially available; 2023 global exports ~370 tonnes/year, primarily from India and Canada (`iter-01/sources/wits-trade-comtrade-en-country-all-year-2023-tradeflow.md`). Deuterated acetone and deuterated liquids are also commercially available laboratory chemicals. Fuel supply is not a near-term constraint for R&D scale.
 
 **Missing**:
-- Chamber wall materials specification under sustained D-D neutron flux (2.45 MeV, lower penetrating than 14.1 MeV D-T but still activating)
-- Long-term deuterium consumption and recirculation system design
-- Tritium accumulation management in liquid medium (regulatory and safety issue, especially for organic liquids like deuterated acetone)
-- Radiolysis of liquid medium under sustained neutron and gamma flux (potential maintenance cost driver)
+- No assessment of materials for a fusion-neutron environment (2.45 MeV D-D neutrons would activate structural materials and degrade PZT ceramic transducers over time — PZT is radiosensitive)
+- No analysis of lead supply/environmental concerns in PZT at fusion scale
+- No analysis of deuterium supply at power-plant scale (current market is tiny: ~370 t/yr globally, primarily for existing fission reactors; sonofusion at multi-GWe scale would require orders of magnitude more)
+- No consideration of what liquid medium would be used (heavy water, deuterated acetone, or other deuterated fluid) and its irradiation chemistry
 
 **Gaps**:
-- Tritium accumulation in liquid medium — `not-yet-sourced` — **important**; CANDU heavy water moderator literature provides closest analogue; AECL/CNL reports likely relevant (`unverified — confirm existence before searching`)
-- Radiation damage to liquid medium (deuterated acetone radiolysis) — `not-yet-sourced` — **important**; no data in available sources
-- Long-term transducer degradation under radiation exposure — `truly-unknown` — **important**
+- PZT transducer lifetime under D-D neutron flux: unknown and potentially fatal to the concept — `not-yet-sourced` — **blocking** (PZT ceramics are known to be radiation-sensitive; this is a fundamental material compatibility question; search radiation effects literature for PZT)
+- Deuterium supply at power-plant scale: small current market, scaling path unknown — `derivable` — **important** (derivable from isotope enrichment economics)
+- Irradiation chemistry of deuterated liquid medium: undefined — `not-yet-sourced` — **important**
 
 ---
 
@@ -112,69 +96,59 @@
 **Coverage**: Poor
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Driver frequency | 20–40 kHz | UCLA Putterman group (`ucla-putterman-group-sonoluminescence.md`) | high |
-| Plasma density (demonstrated) | >10²¹ cm⁻³ | Flannigan & Suslick 2010, via `bubble-fusion-scientific-history.md` | high |
-| Plasma temperature (demonstrated) | 7,000–16,000 K | Flannigan & Suslick 2010 | high |
-| Flash duration | <50 picoseconds | UCLA Putterman group | high |
-| Repetition rate (demonstrated) | 40,000–10,000,000/s | `ucla-putterman-group-sonoluminescence.md` | medium |
-| Industrial transducer cost (analogue) | ~$1,000–10,000 per unit at 4 kW | Hielscher UIP4000hdT market price range | low |
-| Research reactor cost (comparator) | ~$250K (Impulse Devices, 1-ft sphere) | `bubble-fusion-scientific-history.md` | low |
-| Government R&D invested | >$10M (UCLA program) | `sonofusion-energy-website.md` | low |
-| Deuterium fuel cost | ~$1/g heavy water | general market data | high |
+| Driving frequency | 20–40 kHz (single-bubble); up to 10⁷ Hz (multi-bubble) | UCLA Putterman group website | m |
+| Driver power per unit (industrial analog) | 4–16 kW per unit (Hielscher UIP4000–UIP16000) | Hielscher sources | l (analog only) |
+| Electroacoustic efficiency (industrial analog) | >50–60% (implied by APC "high electro-acoustical efficiency") | APC International | l (analog only) |
+| Deuterium fuel cost basis | ~$460/kg (India export price, 2023) | WITS trade data | m |
+| Heavy water market scale | ~370 t/yr global exports, dominated by India/Canada | WITS trade data | h |
 
-**Missing Parameters**:
+**Note on fleet-wide source (Hawker, "A simplified economic model for inertial fusion," `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`)**: The Hawker 14-parameter IFE LCOE framework (driver efficiency `μ_d`, driver cost constant `γ` in $/J, driver energy `E_d`, frequency `f`, gain `G`, target cost `δ` in $/target, plant cost constant `α` in $/kWe, O&M cost constant `ε`, thermal efficiency `μ_th`, blanket multiplier, availability, discount rate, yield cost constant, driver lifetime) maps structurally onto sonofusion: the acoustic transducer array is the "driver," each bubble collapse is the "target," the acoustic driving frequency is `f`, and the plasma temperature × density × confinement product determines `G`. However, since fusion has not been demonstrated, **no value can be assigned to any physics-dependent parameter** (`G`, `E_d`, `δ`, `μ_d` in fusion context). This source formalizes the parameter space that would be needed but cannot supply values — it does not downgrade any blocking gap. It is cited here to establish the LCOE modeling framework that would eventually apply.
 
+**Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion gain (Q) | truly-unknown | blocking | No fusion achieved; Q is undefined |
-| Fusion power per bubble collapse | truly-unknown | blocking | Requires demonstrated fusion yield |
-| Plant electrical output (MWe) | truly-unknown | blocking | No plant design exists |
-| Capital cost (reaction chamber at plant scale) | derivable | blocking | Impulse Devices ~$250K is only analogue; far from plant scale |
-| Capital cost (transducer array at plant scale) | derivable | important | Unit cost analogue exists (Hielscher 4kW); array size unknown |
-| Capital cost (balance of plant) | derivable | important | Standard thermal BOP if Carnot/steam cycle assumed |
-| Energy conversion efficiency | truly-unknown | blocking | No energy capture mechanism disclosed |
-| Thermal cycle type | truly-unknown | blocking | Speculative: liquid thermalization → steam turbine |
-| Capacity factor | derivable | important | Transducer systems have high availability; limiting factor unknown |
-| First-wall / chamber lifetime under neutron flux | truly-unknown | blocking | No design; no neutron flux calculation |
-| O&M staffing requirements | truly-unknown | important | No plant concept to derive from |
-| Fuel cost (deuterium consumption rate) | derivable | low | Rate unknown but low cost relative to ICF targets |
-| Repetition rate needed for net power | derivable | blocking | Requires Q; Q is unknown |
+| Fusion gain G (target gain) | truly-unknown | blocking | Fusion not demonstrated; best sonoluminescence T is 16,000 K vs. ~10⁸ K needed |
+| Net electrical output / plant capacity | truly-unknown | blocking | No design exists; requires demonstrated Q > 1 first |
+| Capital cost (plant, driver, chamber) | truly-unknown | blocking | No plant design; driver would scale very differently from laser/HIF plants |
+| Operating cost (O&M, liquid replacement, transducer replacement) | truly-unknown | blocking | No design; transducer lifetime in radiation environment unknown |
+| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | Power cycle undesigned; liquid thermalization plausible but no analysis |
+| Capacity factor / availability | truly-unknown | blocking | No design; transducer rep-rate wear is uncharacterized at fusion scale |
+| Driver wall-plug efficiency in fusion context | derivable | important | Industrial PZT electroacoustic efficiency ~50–80%; unknown whether this holds at cavitation-relevant power densities for fusion |
+| Target cost (cost per bubble/pulse) | truly-unknown | blocking | "Bubble" is not a manufactured target, but liquid medium replacement rate, transducer replacement, and liquid activation are all unquantified |
+| Blanket/neutron multiplier | truly-unknown | important | No blanket designed; liquid medium provides some moderation |
 
 ---
 
 ## Source Recommendations
 
-1. **ARPA-E Explorer** — search "Sonofusion" or "Seth Putterman" for any awarded programs post-2015. Award abstracts sometimes contain the only public technical disclosures for early-stage companies. `not-yet-sourced` — `unverified — confirm existence before searching`
+1. **Search for recent Putterman/Camara group publications (2010–2026)** on dense microplasma conditions, temperature limits of sonoluminescence, and any updated neutron measurement attempts — `not-yet-sourced` — search APS Physical Review Letters, Journal of the Acoustical Society of America, and arXiv:physics.plasm-ph for "Putterman" + "sonoluminescence" + "plasma."
 
-2. **USASpending.gov / SBIR/STTR database** — search for "Sonofusion Energy" as a contractor or awardee. Any SBIR Phase I/II award would include a technical abstract. `not-yet-sourced` — `unverified — confirm existence before searching`
+2. **Radiation effects on PZT piezoelectric ceramics** — `not-yet-sourced` — search Nuclear Instruments and Methods or Journal of Nuclear Materials for PZT/piezoelectric radiation tolerance studies. This gap is potentially fatal to the concept design; understanding it would improve TRL assessment even without a plant design. `unverified — confirm existence before searching.`
 
-3. **IEEE Xplore / AIP / ASA** (Acoustical Society of America) — Putterman group publications post-2020, particularly any paper using "inertial confinement" framing or with energy-balance data (as opposed to basic sonoluminescence physics). `not-yet-sourced` — `unverified — confirm existence before searching`
+3. **Sonofusion Energy patent filings** — `not-yet-sourced` — search USPTO and EPO for assignee "Sonofusion Energy" or inventors "Putterman, Seth" + "Camara, Carlos" post-2020. Patent applications often contain more technical detail than websites. `unverified — confirm existence before searching.`
 
-4. **CANDU reactor / AECL literature** — tritium accumulation in heavy water moderator systems provides the closest available analogue for managing tritium in a D-D liquid-medium concept. Relevant for Section 4 materials/supply-chain analysis. `not-yet-sourced` — `unverified — confirm existence before searching`
+4. **ARPA-E program records for Sonofusion Energy** — `not-yet-sourced` — the company website claims ">$10M in government funding." Search ARPA-E projects database and USASpending.gov for awards to Sonofusion Energy or UCLA PI Putterman. Award abstracts typically describe technical approach. `unverified — confirm existence before searching.`
 
-5. **IEEE Spectrum "bubble-power" article** — referenced in dossier (`https://spectrum.ieee.org/bubble-power`) but not extracted. Likely contains historical context and independent physicist commentary. `not-yet-sourced`
+5. **Impulse Devices Inc. historical documentation** — `not-yet-sourced` — a prior sonofusion company (mentioned in dossier, cited from Spacedaily article) conducted experiments in the early 2000s. Any technical reports from that program would provide the closest analog to a structured sonofusion R&D effort. Search OSTI or Google Scholar for "Impulse Devices" + "sonofusion."
 
-6. **Impulse Devices, Inc. records** — dossier mentions a ~$250K research reactor built by this company. Archived news coverage (SpaceDaily already cited) or FOIA-accessible records may yield basic engineering specs usable as a cost analogue. `not-yet-sourced` — `unverified — confirm existence before searching`
-
-7. **Hawker (2020) IFE simplified economic model** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` — the 14-parameter technology-agnostic IFE LCOE model is applicable here as a parametric framework. It does not resolve physics unknowns, but provides the correct mathematical structure for a back-solve exercise showing what Q and shot yield would need to be. Confirmed relevant; already in repo.
+**Disqualified fleet-wide sources:**
+- **Progress toward fusion breakeven (Wurzel & Hsu)** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Covers ICF, MCF, and MIF concepts with peer-reviewed Lawson parameter measurements. Sonofusion has no peer-reviewed Lawson parameter data — the concept is not included in the compilation and cannot be plotted. Disqualified: provides no data for sonofusion.
+- **A simplified economic model for inertial fusion** (Hawker, `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Read and partially integrated above. The 14-parameter framework maps structurally to sonofusion but supplies no values — no blockingLevel gaps are downgraded because the fundamental issue is that fusion is undemonstrated, not that a modeling framework is lacking.
+- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): D-T tokamak focused; entirely different confinement family, no applicable cost structure analog for acoustic cavitation.
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): CAS framework is generic fusion infrastructure, but sonofusion has no plant design to which CAS categories could be applied. Disqualified for this concept at this stage.
+- **Revisit of 2017 ARPA-E ALPHA Concepts** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Covers Field-Reversed Configuration, Magnetized Target Fusion, Dense Plasma Focus, and Sheared-Flow Z-Pinch concepts — none is acoustically driven. Disqualified.
+- **Energy from Inertial Fusion** (1992, `knowledge/sources/energy_from_inertial_fusion/`): Covers laser, heavy-ion, and light-ion IFE drivers in a 1992 review. Acoustic/sonofusion is not an IFE concept in this taxonomy. Disqualified.
+- **Remaining fleet sources** (HIF economics, accelerators for IFE, AMPS, Xcimer, Helios stellarator): All technology-specific to drivers (heavy-ion, laser, pulsed power) or confinement families (MFE) with no structural overlap with acoustic cavitation. Disqualified.
 
 ---
 
 ## Summary
 
-**Recommendation: Proceed to analysis with explicit "Insufficient Data" framing — do not attempt a standard LCOE model.**
-
-The available data is sufficient to write a thorough **qualitative** analysis covering sections 1–4, with an honest treatment of the concept's scientific status (pre-fusion demonstration, ~10⁴ K temperature gap, fraud history in the field, null neutron results from Putterman's own lab). The data is **not** sufficient to produce a credible LCOE model — there are no Q values, no plant design, no energy conversion pathway, and no capital cost basis beyond a ~$250K research reactor comparator.
-
-For the quantitative deliverable, the appropriate approach is:
-- Adapt Hawker's 14-parameter IFE LCOE framework as a parametric placeholder, treating Q, plant size, rep rate, and conversion efficiency as free parameters
-- Back-solve from $0.01/kWh to show what would need to be true under optimistic and pessimistic assumptions
-- Contrast the required parameters against the physics ceiling (~16,000 K demonstrated vs. ~10⁸ K needed) to bound the implausibility gap quantitatively
+**Do not proceed to full D1+ analysis with current sources.** The concept is pre-scientific for techno-economic purposes: D-D fusion from acoustic cavitation has not been independently demonstrated, no plant design or power conversion pathway exists, and Sonofusion Energy has not disclosed any technical details beyond the UCLA spin-off framing. A full analysis would consist almost entirely of speculative placeholders, with the only quantitative content being commercial transducer specifications (irrelevant at fusion scale), heavy water market data, and sonoluminescence physics describing conditions ~4 orders of magnitude below fusion relevance.
 
-This is analytically informative: the back-solve will show that even under heroic assumptions, the concept requires physics advances ~4 orders of magnitude beyond what has been demonstrated. That quantified gap is itself a meaningful output for the comparative study.
+The recommended path is: (1) search for any Sonofusion Energy patent filings or ARPA-E award records that contain their technical thesis, (2) review recent Putterman/Camara group publications for updated experimental results, and (3) investigate PZT radiation hardness literature to assess whether the driver concept is even physically viable in a radiation environment. If no new technical material surfaces, the concept should be documented as "TRL 1 / scientific basis unverified" with analysis deferred until the company publishes technical material or achieves credible experimental fusion results.
 
 ---
 
@@ -182,12 +156,12 @@
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 8
-important_count: 5
-counting_method: "section_5_missing_parameters_blocking_rows_only; important_count from sections_1_to_4_important_gaps_deduplicated"
+blocking_count: 9
+important_count: 7
+counting_method: "deduplicated across all sections: (1) fusion physics undemonstrated, (2) company technical thesis undisclosed, (3) reactor/system design does not exist, (4) energy conversion pathway undefined, (5) all capital cost parameters unknown, (6) all operating cost parameters unknown, (7) fusion gain/Q not demonstrated, (8) capacity factor/availability undefined, (9) PZT radiation tolerance in fusion environment unknown and potentially concept-fatal. Important gaps: (1) recent Putterman group publications not sourced, (2) transducer scaling physics at fusion power density, (3) reactor vessel/first wall materials undefined, (4) driver efficiency in fusion context (derivable), (5) deuterium supply at scale (derivable), (6) irradiated liquid medium chemistry, (7) neutron management approach"
 section_coverage:
   availability_of_data:       "Poor"
-  system_function:            "Partial"
+  system_function:            "Poor"
   subsystem_maturity:         "Poor"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Poor"
```
