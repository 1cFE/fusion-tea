# Diff: 23-laser-icf-nanostructured-target

**Generated:** 2026-05-22T10:51:52-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 7 | 6 | -1 |
| important_count  | 4 | 8 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
159:5. **Xcimer whitepaper** (fleet-wide: `knowledge/sources/commercialization_of_laser_fusion_energy/`) — covers KrF excimer laser cost breakdown at <$100/J, including detailed laser cost-by-component. Useful analog for driver cost structure even though Marvel uses DPSSL, not KrF. The cost decomposition methodology transfers directly.
161:6. **Hawker 2020 simplified IFE model** (fleet-wide: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable framework. The 14-parameter technology-agnostic model can be parameterized for this concept using Marvel's targets; the Monte Carlo sensitivity analysis will identify which unknowns matter most. **Recommend reading this before building the LCOE model.**
```

## Blocking-tier lines (baseline)

```
29:- No published plant design from either company — `proprietary` — **blocking** for quantitative LCOE; workable for qualitative
53:- Alpha particle capture efficiency / actual direct conversion efficiency — `truly-unknown` (Marvel claims "up to 70%" with no breakdown; no comparable demonstrated system) — **blocking** for energy conversion modeling
54:- Q value / ignition physics validation — `truly-unknown` at demonstrated scale — **blocking** for credible quantitative analysis; forces use of stated targets as assumptions
77:- Energy conversion subsystem TRL — `truly-unknown` (no comparable system has been built) — **blocking** for TRL section rigor
126:| Capital cost by subsystem (laser, chamber, balance of plant) | proprietary | blocking | No published estimates from either company; analogy to NIF/OMEGA possible but tenuous |
127:| Laser system cost per PW at rep rate | not-yet-sourced | blocking | DPSSL cost scaling from industrial laser literature possible; search LLNL, ELI cost studies |
128:| Target fabrication cost per target | proprietary | blocking | Semiconductor fab analogy possible; ~5000/wafer provides floor; no yield or cycle time data |
129:| Target replacement cost per year | derivable (from rep rate × unit cost) | blocking | Can be derived once unit cost estimated |
131:| Alpha capture efficiency (validated) | truly-unknown | blocking | Marvel claims "up to 70%"; no demonstrated analogue; must treat as free parameter |
132:| Capacity factor / availability | truly-unknown | blocking | No published estimate; no comparable pulsed IFE plant exists |
134:| Q value (fusion gain) | truly-unknown at power-relevant scale | blocking | Currently 4 OOM below Q=1; must treat target Q as free parameter with wide uncertainty range |
```

## Blocking-tier lines (new)

```
35:- No experimental gain data published — `truly-unknown` (Marvel has internal data from 2,000+ shots; not disclosed) — **blocking**
36:- No independent TEA or plant study — `proprietary` — **blocking**
37:- Both companies are pre-ignition; all "data" is target claims, not measured results — `truly-unknown` — **blocking**
57:- Femtosecond DPSSL wall-plug efficiency (commercial scale) — `proprietary` / `not-yet-sourced` — **blocking** (drives recirculating power fraction)
58:- Target coupling efficiency and ignition threshold — `proprietary` — **blocking** (drives required laser energy per shot)
59:- Gain G from block ignition — `proprietary` — **blocking** (existential for LCOE)
84:- Femtosecond DPSSL at IFE average power (10 Hz, PW class, sustained) — TRL 2–3, `not-yet-sourced` — **blocking** for timing
106:- Target volume manufacturing cost — `proprietary` — **blocking** for LCOE
134:| Fusion gain G (target or achieved) | proprietary | blocking | Core LCOE driver; without this, cannot compute fusion energy per shot. Marvel has 2,000+ unpublished experiments |
135:| Laser energy per shot (E_laser) | proprietary | blocking | Required with G to get fusion yield; ATLAS design implies PW class but not quantified |
136:| Wall-plug efficiency (femtosecond DPSSL) | not-yet-sourced | blocking | Nanosecond target is 10%; femtosecond systems have fundamentally higher losses (CPA gratings, stretcher/compressor). Could be 0.1–1%. Drives recirculating power |
137:| Target cost per shot (nanostructured) | proprietary | blocking | Semiconductor litho cost per target at IFE rate. Critical IFE cost driver. No published estimate |
138:| Plant capital cost (any CAS breakdown) | proprietary | blocking | Siemens Energy co-design is in progress but not published |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/23-laser-icf-nanostructured-target.md	2026-05-22 09:21:13.869719205 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/gap_report.md	2026-05-22 10:51:52.920391440 -0700
@@ -1,178 +1,188 @@
+I have enough information to write the full assessment. Let me compile it now.
+
+---
+
 # Gap Assessment: Laser ICF - Nanostructured Target (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
 
-**Summary**: Public information is adequate for a qualitative narrative covering system concept, physics approach, company landscape, and materials — but is nearly absent for quantitative LCOE modeling. No published plant studies, cost estimates, or Q values exist for either company. The core physics (non-thermal block ignition yielding net energy gain) remains undemonstrated at a level 4 orders of magnitude from Q≥1. A D1+ analysis can be written, but the quantitative model will rest almost entirely on stated targets and analogues rather than validated parameters.
+**Summary**: The available data covers company roadmaps, basic physics constraints, and DPSSL driver technology in reasonable depth, but is nearly empty on the two things LCOE modeling requires most: an experimentally grounded fusion gain value and any published plant-level cost structure. Both Marvel Fusion and HB11 Energy are pre-ignition companies; all claims about gain, energy conversion, and capacity factor are targets, not demonstrated results. A parameterized LCOE model can be built using the Hawker IFE framework, but the key inputs (gain G, laser wall-plug efficiency in the femtosecond regime, target cost per shot) are either proprietary or genuinely unknown.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial — qualitative landscape is reasonably well documented; quantitative/engineering data is sparse to absent
+**Coverage**: Partial
 
 **Available**:
-- Company technology overviews (Marvel Fusion website, HB11 Energy website) — concept description, claimed targets, timeline, partners
-- EU CORDIS CFE-NANO project record — 100 MW pilot target, partner list, 2027 Colorado facility milestone
-- Peer-reviewed physics: Hora et al. (arXiv:1603.02579) — theoretical foundation for avalanche mechanism; J. Fusion Energy 2023 — HB11 energy conversion options analysis; CA-PROBONO / Matter Radiation Extremes (May 2025) — multi-lab p-B11 experimental results
-- Patent US20230073280A1 — nanostructured silicon target design details (nanowire geometry, fuel embedding, non-thermal ignition concept)
-- Funding/partnership announcements (Optics.org, CALA) — team size, investor identity, facility milestones
-- UNSW collaboration (Burr et al.) — early reaction chamber materials framing for HB11
+- Company technology descriptions with moderate depth: Marvel Fusion (femtosecond DPSSL on nanostructured Si targets, 10 Hz target, ATLAS facility, ~EUR385M funding, ~500 lasers per plant, Siemens Energy power plant co-design announced) [`optics-news-16-4-4.md`, `binding-ultrashort-pulse-laser-fusion.md`, `marvel-fusion-2025-updates.md`]
+- HB11 Energy approach: thousands of commercial DPSSL units, foam targets 10× more efficient than solid for proton acceleration, ~1 Hz, steam cycle conversion [`energynewsbulletin-energy-transition-features-articles.md`, `iter-02/sources/hb11-energy-2025-updates.md`]
+- EU CORDIS CFE-NANO project fact sheet: 100 MW pilot target 2033, demo facility at CSU 2027 — confirms Marvel roadmap at EU official level [`marvel-fusion-2025-updates.md`]
+- Theoretical p-B11 physics in a *tokamak* context (ENN/Cai et al.): establishes breakeven constraints (nτ ~ 2.3×10²¹ m⁻³·s at Ti~380 keV, H-factor requirements), bremsstrahlung and synchrotron radiation barriers [`arxiv-2201-12818.md`]
+- DPSSL driver technology: comprehensive 2025 LLNL/FBH review covering diode pump requirements for IFE (10 kJ, 10–20 Hz beamlines), cost drivers ($0.3–1.3/W today → $0.01/W target at IFE volume), reliability gaps (demonstrated 28 Mshots vs. required 3–20 Gshots), packaging bottlenecks [`osti-servlets-purl-3008974.md`]
+- Mercury DPSSL program: demonstrated 10% wall-plug efficiency at 10 Hz / 100 J with nanosecond pulses — the benchmark DPSSL architecture for IFE [`osti-servlets-purl-15013216.md`, `osti-servlets-purl-15013230.md`]
+- NIF optics cost data: replacement costs for NIF-scale ns-laser systems ($5.6M/yr incremental at 2.6 MJ operation) — useful as upper-bound analog [`osti-servlets-purl-1400089.md`]
+- HB11 foundational physics abstract: Hora et al. avalanche boron fusion concept, block ignition + magnetic trapping as the theoretical basis [`arxiv-1603-02579.md`]
 
 **Missing**:
-- Peer-reviewed experimental yield / gain measurements for either company's configuration
-- Any published reactor design, system architecture, or plant study from either company
-- Published cost estimates or analogues at component level
+- Peer-reviewed publications reporting actual p-B11 gain from *laser* experiments (contrast with the 2,000+ internal experiments cited by Marvel in CORDIS but unpublished)
+- Published plant study or pre-conceptual reactor design from either company
+- Any independent techno-economic analysis specific to this concept
 
 **Gaps**:
-- No published plant design from either company — `proprietary` — **blocking** for quantitative LCOE; workable for qualitative
-- Experimental gain data (Q values) not published beyond qualitative statements ("4 orders of magnitude from Q=1") — `proprietary` / `not-yet-sourced` — **important** for framing analysis credibility
-- No system code outputs (ARIES, HYLIFE, or equivalent) — `truly-unknown` at this stage — **important**
+- No experimental gain data published — `truly-unknown` (Marvel has internal data from 2,000+ shots; not disclosed) — **blocking**
+- No independent TEA or plant study — `proprietary` — **blocking**
+- Both companies are pre-ignition; all "data" is target claims, not measured results — `truly-unknown` — **blocking**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good — enough to write a thorough qualitative treatment
+**Coverage**: Partial
 
 **Available**:
-- Physics mechanism described in sources: non-thermal block ignition (Marvel), avalanche proton fast ignition (HB11) — both companies' websites and Hora et al. provide conceptual description
-- Divergence between the two companies is documented (target type, rep rate, energy conversion)
-- Energy conversion novelty noted: Marvel's hybrid magnetic/electrostatic + steam approach with claimed ~70% efficiency; HB11's pivot to conventional steam cycle
-- Pulse energy and repetition rate stated as targets (Marvel: 10 Hz, ~7 PW combined; HB11: 1 Hz, ~300 kWh/shot)
-- Experimental gap quantified qualitatively: HB11 "four orders of magnitude from net energy gain"
+- Physics challenge structure is well-characterized: the bremsstrahlung barrier in p-B11 (fusion power < radiation power without synchrotron suppression and Ti/Te ≫ 1) is quantified in the ENN tokamak system code paper. Synchrotron radiation with wall reflectivity <0.99 severely penalizes gain in magnetic systems; laser ICF bypasses this by operating on inertial timescales too short for synchrotron loss to accumulate [`arxiv-2201-12818.md`]
+- Non-thermal block ignition mechanism described qualitatively: femtosecond laser creates a density-modulated plasma block that accelerates and triggers avalanche via elastic alpha collisions rather than thermal equilibration [`arxiv-1603-02579.md` abstract; `binding-ultrashort-pulse-laser-fusion.md`]
+- The DPSSL laser system as a cost modeling challenge is well-characterized: diode laser costs dominate (at least ⅓–½ of beamline cost even at IFE scale), packaging is the bottleneck, 10 Hz / 10% wall-plug efficiency is the target for nanosecond systems [`osti-servlets-purl-3008974.md`]
+- Marvel's hybrid energy conversion (magnetic + electrostatic + steam, claimed ~70% overall) is identified but not engineering-validated [`dossier.md`]
 
 **Missing**:
-- No validated gain curve or ignition threshold data
-- No wall-plug efficiency breakdown for Marvel Fusion's laser system
-- No published thermal-hydraulic or chamber design analysis
-- No treatment of driver energy recycling fraction (only HB11 mentions "a portion recycled to laser system")
+- Quantified gain model for non-thermal block ignition: what ignition conditions Marvel's nanostructured targets actually achieve is not in public literature. The ENN paper shows Q > 1 requires H-factor >> current capability in a *tokamak*; whether block ignition bypasses this is the core unvalidated claim
+- Wall-plug efficiency for femtosecond DPSSL systems: Crump 2025 covers nanosecond systems (target ≥10% wall-plug). Femtosecond / petawatt systems are fundamentally less efficient due to CPA pulse stretching/compression losses, grating losses, and lower average power. This is a significant and poorly-quantified gap for cost modeling
+- Coupling efficiency between femtosecond pulse and nanostructured target: how much of delivered laser energy actually reaches the fuel is unquantified in public sources
+- Alpha particle energy collection efficiency for hybrid conversion: "~70%" claimed by Marvel but no engineering design or validation available
 
 **Gaps**:
-- Laser wall-plug efficiency for Marvel Fusion — `not-yet-sourced` (HB11 targets ~10%; Marvel not characterized in sources) — **important** for energy balance; search CLEO/IFSA proceedings for DPSSL efficiency data
-- Alpha particle capture efficiency / actual direct conversion efficiency — `truly-unknown` (Marvel claims "up to 70%" with no breakdown; no comparable demonstrated system) — **blocking** for energy conversion modeling
-- Q value / ignition physics validation — `truly-unknown` at demonstrated scale — **blocking** for credible quantitative analysis; forces use of stated targets as assumptions
+- Femtosecond DPSSL wall-plug efficiency (commercial scale) — `proprietary` / `not-yet-sourced` — **blocking** (drives recirculating power fraction)
+- Target coupling efficiency and ignition threshold — `proprietary` — **blocking** (drives required laser energy per shot)
+- Gain G from block ignition — `proprietary` — **blocking** (existential for LCOE)
+- Direct alpha capture engineering efficiency — `proprietary` / `not-yet-sourced` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial — TRL assessments possible at subsystem level but rely on analogues; no published TRL self-assessments
+**Coverage**: Partial
 
 **Available**:
-- **Laser driver (DPSSL)**: Commercial DPSSL technology exists; Trumpf and Thales are active partners; petawatt-class demonstrated at ALEPH/CSU; 10 Hz rep rate not yet demonstrated at full energy — technology basis established, scaling is the gap
-- **Nanostructured target manufacturing**: Semiconductor lithography process described; ~5000 targets/300 mm wafer; standard fab equipment; room-temperature handling (no cryogenics) — manufacturing route credible, mass-production cost unknown
-- **LION 2 experimental chamber**: Operational at CALA July 2025 — validates Marvel's experimental program maturity
-- **ATLAS facility**: Under construction at CSU; opening mid-2026 — next validation milestone
-- **HB11 foam targets**: In-house manufacturing described; "10x more efficient at proton acceleration" — no independent validation
-- **Reaction chamber / blanket**: UNSW collaboration framing steel construction as feasible (aneutronic environment); no detailed design published
+- DPSSL pump diodes: TRL 4–5 for IFE conditions. Current state: 1 kW/bar, 65% electro-optical efficiency, 28 Mshots demonstrated. IFE requirements: 500 W–1 kW/bar, 70% efficiency, 3–20 Gshots — a 100–700× reliability gap. Path exists but not demonstrated [`osti-servlets-purl-3008974.md`]
+- Mercury DPSSL: demonstrated TRL 4 at 100 J / 10 Hz / 10% wall-plug for nanosecond pulses (1999–2001 era). Scales to kilojoule/megajoule class in principle [`osti-servlets-purl-15013216.md`]
+- Nanostructured target fabrication: Marvel uses standard semiconductor lithography (300 mm wafer, ~5000 targets/wafer) — manufacturing process exists commercially, but IFE-rate target injection and debris management at 10 Hz are undemonstrated. TRL ~3 for this specific application [`dossier.md`; patent US20230073280A1]
+- HB11 low-density foam targets: in-house production established, 10× proton acceleration efficiency vs. solid targets claimed. TRL ~3–4 for production; injection at 1 Hz undemonstrated [`energynewsbulletin-energy-transition-features-articles.md`]
+- CALA LION 2 experimental chamber (Marvel): operational July 2025, but this is an experimental facility not a prototype power plant
+- Partner ecosystem: Trumpf (laser manufacturing), Thales (laser components), Siemens Energy (power plant design), Fraunhofer, CEA — mature industrial partners reduce TRL transition risk
 
 **Missing**:
-- No TRL table or subsystem breakdown published by either company
-- No demonstrated repetition rate at commercial-relevant energy levels
-- No demonstrated energy conversion at any scale
-- Foam target manufacturing process not characterized beyond marketing claims
+- Reaction chamber design: no published chamber design for non-thermal p-B11 laser ICF. NIF-style chambers are for nanosecond implosion and spherical geometry; Marvel's non-compressive approach requires fundamentally different chamber architecture
+- Alpha particle collection system: no published TRL assessment for the magnetic/electrostatic direct conversion
+- Target injection and debris clearing at IFE rep rate: for 10 Hz, targets must be injected and debris cleared in 100 ms windows — no demonstrated prototype
+- DPSSL at petawatt class / femtosecond pulse duration: the ATLAS facility at CSU is described as ~7 PW combined at 10 Hz but this is a planned system, not operating at full specification
 
 **Gaps**:
-- Repetition rate scaling (Marvel 10 Hz at PW class) — `not-yet-sourced` / `truly-unknown` at this scale — **important**; CLEO / high-power laser engineering literature may have DPSSL rep-rate roadmaps
-- Energy conversion subsystem TRL — `truly-unknown` (no comparable system has been built) — **blocking** for TRL section rigor
-- Target fabrication at production scale (unit economics, yield, throughput) — `proprietary` — **important** for operating cost section
+- Reaction chamber TRL — `not-yet-sourced` / `proprietary` — **important**
+- Target injection system TRL — `not-yet-sourced` — **important**
+- Femtosecond DPSSL at IFE average power (10 Hz, PW class, sustained) — TRL 2–3, `not-yet-sourced` — **blocking** for timing
+- Direct energy conversion TRL — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good — enough for a complete qualitative treatment; this is one of the concept's strengths
+**Coverage**: Partial
 
 **Available**:
-- p-B11 fuel: Boron is abundant (Turkey, USA, Chile reserves; well-characterized industrial supply); proton source trivial (hydrogen); no enrichment required
-- Silicon nanostructured targets: Standard semiconductor materials (Si, established global supply chain); no exotic elements
-- No tritium requirement — confirmed aneutronic; eliminates the most supply-constrained material in D-T concepts
-- No HTS tape, no beryllium, no Li-6 enrichment — confirmed by technology descriptions
-- Conventional steel for reaction chamber (aneutronic environment) — UNSW confirms standard structural materials viable
-- DPSSL components: Commercial laser supply chain (Trumpf, Thales as partners) — established industrial base
+- Aneutronic fuel cycle advantage: no tritium breeding, no lithium, no beryllium, no LiPb blanket. Steel construction for reaction chamber is sufficient (no activation issues from high-energy neutrons). UNSW materials collaboration with HB11 specifically validating conventional steel for chamber construction [`dossier.md`; `hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to.md`]
+- Diode laser supply chain: bottleneck clearly identified — GaAs diode bars, facet passivation, CuW submounts, FAC collimators. Manufacturing is dominated by packaging costs (>50% of stack cost). Requires 100–1000× production scale-up from today; learning curve models suggest $0.01/W is achievable at sustained IFE demand [`osti-servlets-purl-3008974.md`]
+- Nanostructured Si targets: use standard CMOS-fab silicon processes; supply chain for silicon wafers is mature. The specialized nanowire lithography is a variant of existing semiconductor manufacturing [`dossier.md`]
+- HB11 foam targets: proprietary in-house production, not externally sourced. Supply chain dependency on maintaining proprietary process at scale
 
 **Missing**:
-- No characterization of boron purity requirements or target-grade boron availability
-- No treatment of laser optical component lifetime / replacement rates (damage thresholds at petawatt intensities)
-- No treatment of vacuum vessel or chamber material replacement schedules
+- Boron-11 isotope enrichment: natural boron is 80% B-11 / 20% B-10. For IFE applications, enrichment to near-100% B-11 is required. No data on B-11 enrichment production capacity, cost per kg, or supply chain for IFE-scale operations. This is a potentially significant gap that could affect fuel cost estimates
+- Optical coatings and laser optics lifecycle at 10 Hz PW class: NIF's optics recycle/replacement cost is documented for nanosecond pulses. Femtosecond pulse optics face different damage mechanisms (multiphoton ionization, B-integral) and no IFE-rate cost data exists
+- High-power laser amplifier crystals (Yb:YAG or Nd:glass) at scale: not addressed in concept-scoped sources
 
 **Gaps**:
-- Laser optic replacement rates at 10 Hz petawatt class — `not-yet-sourced` — **important** for operating cost; search laser damage threshold literature or LLNL NIF optic lifetime studies as analogues
-- Boron purity / isotopic requirements (natural boron is 20% B-11 / 80% B-10; enrichment may be needed) — `not-yet-sourced` — **important**; search boron isotope separation literature (unverified — confirm whether enriched B-11 is required before searching)
+- B-11 enrichment cost and supply chain — `not-yet-sourced` — **important** (affects fuel cost per shot)
+- Laser optics replacement rate at femtosecond / PW class — `not-yet-sourced` — **important**
+- Target volume manufacturing cost — `proprietary` — **blocking** for LCOE
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor — stated targets only; no validated parameters
-
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Plant output target (Marvel) | 100 MW pilot | CFE-NANO CORDIS | m |
-| Plant output target (HB11) | ~1 GW baseload | HB11 website | l |
-| Repetition rate (Marvel) | 10 Hz | Marvel website | m |
-| Repetition rate (HB11) | ~1 Hz | HB11 website | m |
-| Energy per shot (HB11 estimate) | ~300 kWh | iter-01 source (derived) | l |
-| Energy conversion efficiency (Marvel) | "up to 70%" hybrid | Marvel website | l |
-| Energy conversion efficiency (HB11) | ~35-40% (steam) | J. Fusion Energy 2023 | m |
-| Laser wall-plug efficiency (HB11 target) | ~10% | HB11 website | l |
-| Target production (Marvel) | ~5000/wafer, standard litho | Patent + website | m |
-| Fuel cost driver | p-B11, no enrichment required (assumed) | websites | m |
-| Experimental gain status | ~4 OOM below Q=1 | HB11 website | h |
-| Pilot timeline | 2033 (Marvel) | CFE-NANO | m |
+|-----------|-------------|--------|------------|
+| Repetition rate | 10 Hz (Marvel), ~1 Hz (HB11) | dossier | m |
+| Fuel type | p-B11, aneutronic | dossier | h |
+| Tritium breeding cost | N/A | dossier | h |
+| Neutron shielding cost | Minimal (thin steel) | dossier; UNSW | m |
+| Plant output target | 100 MW pilot (2033), commercial scale unspecified | CORDIS | l |
+| Diode laser cost (current) | $0.3–1.3/W | Crump 2025 | h |
+| Diode laser cost (IFE target) | ~$0.01/W at 1000× volume scale | Crump 2025 | m |
+| Driver laser count (commercial) | ~500 laser systems | optics-news-16-4-4 | l |
+| DPSSL wall-plug efficiency (ns) | ~10% (target), demonstrated at 100 J | Mercury/Payne 1999 | h (for ns) |
+| DPSSL wall-plug efficiency (fs) | <1% current, target unclear | dossier gap | l |
+| Target yield per wafer (Marvel) | ~5000 per 300 mm wafer | dossier | m |
+| Energy conversion efficiency | ~70% claimed (Marvel hybrid) | dossier | l |
+| Total capital raised | EUR385M (Marvel) | optics-news | h (not plant cost) |
+| IFE LCOE range (generic) | ~$25/MWh under optimistic assumptions | Hawker 2020 (fleet-wide) | m (generic IFE) |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Capital cost by subsystem (laser, chamber, balance of plant) | proprietary | blocking | No published estimates from either company; analogy to NIF/OMEGA possible but tenuous |
-| Laser system cost per PW at rep rate | not-yet-sourced | blocking | DPSSL cost scaling from industrial laser literature possible; search LLNL, ELI cost studies |
-| Target fabrication cost per target | proprietary | blocking | Semiconductor fab analogy possible; ~5000/wafer provides floor; no yield or cycle time data |
-| Target replacement cost per year | derivable (from rep rate × unit cost) | blocking | Can be derived once unit cost estimated |
-| Laser wall-plug efficiency (Marvel) | not-yet-sourced | important | HB11 cites ~10% target; Marvel not characterized; critical for recirculating power fraction |
-| Alpha capture efficiency (validated) | truly-unknown | blocking | Marvel claims "up to 70%"; no demonstrated analogue; must treat as free parameter |
-| Capacity factor / availability | truly-unknown | blocking | No published estimate; no comparable pulsed IFE plant exists |
-| Laser optic replacement rate (10 Hz, PW class) | not-yet-sourced | important | Analogues from NIF optic damage literature possible (unverified — confirm applicability) |
-| Q value (fusion gain) | truly-unknown at power-relevant scale | blocking | Currently 4 OOM below Q=1; must treat target Q as free parameter with wide uncertainty range |
-| First wall / chamber replacement schedule | truly-unknown | important | UNSW doing early materials work; no schedule published |
-| Staffing and O&M cost basis | truly-unknown | nice-to-have | No plant design from which to derive |
-| Recirculating power fraction | derivable | important | Depends on wall-plug efficiency and energy conversion efficiency |
+|-----------|----------|-------------|-------|
+| Fusion gain G (target or achieved) | proprietary | blocking | Core LCOE driver; without this, cannot compute fusion energy per shot. Marvel has 2,000+ unpublished experiments |
+| Laser energy per shot (E_laser) | proprietary | blocking | Required with G to get fusion yield; ATLAS design implies PW class but not quantified |
+| Wall-plug efficiency (femtosecond DPSSL) | not-yet-sourced | blocking | Nanosecond target is 10%; femtosecond systems have fundamentally higher losses (CPA gratings, stretcher/compressor). Could be 0.1–1%. Drives recirculating power |
+| Target cost per shot (nanostructured) | proprietary | blocking | Semiconductor litho cost per target at IFE rate. Critical IFE cost driver. No published estimate |
+| Plant capital cost (any CAS breakdown) | proprietary | blocking | Siemens Energy co-design is in progress but not published |
+| Capacity factor / availability | derivable | important | Analogous to other pulsed IFE; likely ~85–90% with component redundancy but unverified |
+| O&M cost | derivable | important | Can estimate from DPSSL diode replacement schedule + NIF analog; highly uncertain |
+| Laser optics replacement rate (fs) | not-yet-sourced | important | NIF data (osti-purl-1400089) covers ns systems; fs regime not documented |
+| B-11 isotope cost | not-yet-sourced | important | Small fraction of IFE fuel cost but unquantified |
+| First wall / chamber replacement schedule | not-yet-sourced | important | Aneutronic reduces radiation damage; but X-rays and particle debris will still erode surfaces |
+| Balance of plant cost | derivable | important | Can use IFE/MFE analogs from CAS documentation |
+| Alpha particle collection system cost | not-yet-sourced | important | No cost analog exists; direct conversion hardware is novel |
 
 ---
 
 ## Source Recommendations
 
-1. **DPSSL cost and efficiency at high rep rate** — search CLEO proceedings, ELI-NP design reports, and DiPOLE/HAPLS program publications for cost-per-joule and wall-plug efficiency data for high-rep-rate DPSSL systems. `not-yet-sourced` — `unverified — confirm existence before searching`
+1. **Marvel Fusion / PLT SPRIND publications** — search SPRIND website and Marvel's patent portfolio for detailed laser specifications and any engineering cost estimates. The PLT (Pulsed Light Technologies) technical documents may have more detail than the company press materials. — `unverified — confirm existence before searching`
 
-2. **p-B11 cross-section and ignition physics** — CA-PROBONO COST Action publications (CA21128), particularly the May 2025 Matter Radiation Extremes paper "Laser-initiated p–11B fusion reactions in petawatt high-repetition-rate laser facilities" — this paper is cited in the dossier and likely contains experimental yield data useful for gain estimation.
+2. **Femtosecond DPSSL wall-plug efficiency** — search CLEO/IFSA/SPIE proceedings (2020–2025) for petawatt-class DPSSL efficiency measurements, especially the HAPLS system at ELI-ALPS (a Marvel partner). The Crump 2025 paper cites HAPLS [ref 10] as a relevant DPSSL milestone — that paper should have efficiency data. — `not-yet-sourced`
 
-3. **Semiconductor wafer cost analogy for nanostructured targets** — semiconductor process cost literature (SEMI standards, fab cost modeling papers) could provide a floor estimate for $/target based on 300 mm wafer processing. `not-yet-sourced` — widely available in semiconductor industry literature.
+3. **LIFE design studies (Bayramian et al., LLNL)** — "Compact, Efficient Laser Systems Required for Laser Inertial Fusion Energy," FST 2011 (cited in Crump as ref 7). This contains the most detailed DPSSL-based IFE plant cost model available publicly, including diode cost breakdown by component. Already cited in Crump 2025. — `not-yet-sourced`
 
-4. **NIF/OMEGA optic replacement costs as laser operating cost analogue** — LLNL annual reports and NIF operations papers document optic damage and replacement rates. Applicability to DPSSL at 10 Hz is imperfect but the best available analogue. `not-yet-sourced` — `unverified — confirm NIF damage threshold regime matches DPSSL regime before applying`.
+4. **HB11 Energy J. Fusion Energy 2023 paper** — cited in dossier as source 8: "HB11 energy conversion options." This may contain the most technical detail on HB11's energy balance and conversion pathway — `not-yet-sourced`
 
-5. **Boron-11 isotope enrichment** — search whether natural boron (20% B-11) is usable or whether enrichment is required. If enrichment is needed, isotope separation industry literature provides cost context. `not-yet-sourced` — `unverified — confirm whether Marvel/HB11 require enriched B-11`.
+5. **Xcimer whitepaper** (fleet-wide: `knowledge/sources/commercialization_of_laser_fusion_energy/`) — covers KrF excimer laser cost breakdown at <$100/J, including detailed laser cost-by-component. Useful analog for driver cost structure even though Marvel uses DPSSL, not KrF. The cost decomposition methodology transfers directly.
 
-6. **HB11 J. Fusion Energy 2023 paper** (already cited in dossier: `link.springer.com/article/10.1007/s10894-023-00349-9`) — this paper discusses energy conversion options in detail and is likely the best available source for conversion efficiency numbers. Should be extracted as a full source document if not already done.
+6. **Hawker 2020 simplified IFE model** (fleet-wide: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable framework. The 14-parameter technology-agnostic model can be parameterized for this concept using Marvel's targets; the Monte Carlo sensitivity analysis will identify which unknowns matter most. **Recommend reading this before building the LCOE model.**
 
-7. **HYLIFE-II or laser IFE plant study analogues** — older Lawrence Livermore laser IFE plant studies (HYLIFE-II, SOMBRERO) provide system-level cost structure analogues for laser-driven IFE even though the physics approach differs. `not-yet-sourced` — these are public documents; confirm relevance to non-classical IFE before applying cost breakdowns.
+7. **p-B11 reactivity and gain physics** — search for Putvinski, Ryutov & Yushmanov (2019), "Fusion reactivity of the pB11 plasma revisited," Nuclear Fusion 59:076018. This updates the reactivity cross-sections and includes a hard upper-bound argument on p-B11 gain. Critical context for evaluating Marvel's non-thermal claims. — `not-yet-sourced` (cited in arxiv-2201-12818.md)
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with caveats.** The qualitative sections (data availability, system function challenges, subsystem maturity, materials/supply chain) can be written to a high standard with the existing sources. The concept is well-defined, the two-company landscape is documented, and the physics basis is traceable to peer-reviewed literature.
+Proceed to full analysis with explicit acknowledgment of the concept's pre-ignition status. The LCOE model should be built as a parametric sensitivity exercise using the Hawker framework rather than a point estimate. Key moves: (1) read Hawker 2020 for methodology; (2) use Crump 2025 to ground the laser system cost and efficiency; (3) treat fusion gain G as the primary sweep variable (range: 1 to ~1000); (4) treat fs DPSSL wall-plug efficiency as a sweep variable (range: 0.1–5%, noting the nanosecond target of 10% likely does not apply); (5) treat target cost as a sweep variable. The qualitative write-up should be rich — the physics rationale, aneutronic advantages, company ecosystem, and roadmap are all well-documented. The quantitative model will be necessarily speculative but instructive.
 
-The quantitative LCOE model will be **assumption-heavy by necessity**. Q≥1 has not been demonstrated; no plant study exists; energy conversion efficiency is a marketing claim. The model should be structured as a parametric sensitivity analysis using stated targets as central estimates with wide uncertainty bands — the back-solve to $0.01/kWh will be informative precisely because it reveals how many simultaneous breakthroughs are required. The most important gaps to fill before building the model are: (1) a better laser system cost analogue from DPSSL literature, (2) the J. Fusion Energy 2023 HB11 paper extracted as a full source, and (3) a treatment of whether B-11 enrichment is required. None of these are strictly blocking — the analysis can proceed with documented assumptions.
+The most important sources to acquire before modeling: Hawker 2020 (already in fleet-wide sources), Bayramian et al. 2011 LIFE design study, and HB11 J. Fusion Energy 2023 conversion paper.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 7
-important_count: 4
-counting_method: "section_5_missing_parameters"
+blocking_count: 6
+important_count: 8
+counting_method: "deduplicated across all sections: blocking = {fusion gain G, target cost per shot, fs DPSSL wall-plug efficiency, plant capital cost structure, target coupling efficiency/ignition threshold, no experimental gain data published}; important = {chamber TRL, target injection TRL, direct energy conversion TRL, B-11 supply chain, laser optics replacement rate (fs), capacity factor, O&M cost, first wall replacement schedule}"
 section_coverage:
-  availability_of_data:       "Partial — qualitative landscape is reasonably well documented; quantitative/engineering data is sparse to absent"
-  system_function:            "Good — enough to write a thorough qualitative treatment"
-  subsystem_maturity:         "Partial — TRL assessments possible at subsystem level but rely on analogues; no published TRL self-assessments"
-  materials_supply_chain:     "Good — enough for a complete qualitative treatment; this is one of the concept's strengths"
-  lcoe_parameter_extraction:  "Poor — stated targets only; no validated parameters"
-```
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
