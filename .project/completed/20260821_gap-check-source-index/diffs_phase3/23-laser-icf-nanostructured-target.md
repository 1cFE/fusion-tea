# Phase 3 diff: 23-laser-icf-nanostructured-target

**Generated:** 2026-05-22T15:15:23-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 8 | 5 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source dispositions in new report

```
120:1. **Hawker simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — **Integrated**. Read and used. Provides the complete 14-parameter technology-agnostic IFE LCOE framework. Driver cost reference values (NIF $9.5/J, First Light $1.7/J), yield cost bound ($70k/GJ lower, $44M/GJ upper), plant cost proxy ($3600/kWe from HYLIFE), and parameterized O&M structure. This source provides the modeling framework for §5 even where specific parameters remain unknown. Addresses the "no IFE cost methodology" gap — downgraded from blocking to important for the framework itself (the specific physics parameters remain blocking).
122:2. **Xcimer commercialization of laser fusion energy** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — **Integrated**. Read and used. Provides detailed DPSSL cost breakdown directly applicable to Marvel Fusion's architecture: current cost $0.3-0.4/W for diodes; absolute floor $0.02/W after supply chain buildout; total DPSSL cost $700-1000/J on-target. Wall-plug efficiency target ~15% commercial DPSSL. Quantifies why DPSSL laser cost dominates IFE plant economics and benchmarks the reduction required. This source provides the best available analogue for Marvel's laser cost structure; does not resolve gain Q or target cost.
132:7. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — **Disqualified**. MFE-specific; cost structure for magnetic confinement does not transfer to pulsed IFE concepts. BOP cost components (heat exchangers, steam turbines) are common to HB11's steam cycle approach but at a level of generality that the Hawker model already covers. No concept-specific content applicable to Marvel or HB11.
134:8. **Economic studies for heavy-ion-fusion** (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`) — **Disqualified**. HIF driver cost structure (induction linac, multi-unit scaling at 5-10 Hz) differs fundamentally from DPSSL laser systems. COE range 3.9-5.8 ¢/kWh for 1.5-3 GWe HIF is a historical analogue but the cost driver (accelerator vs. laser) makes it inapplicable for quantitative laser cost estimation.
136:9. **Energy from Inertial Fusion** (`knowledge/sources/energy_from_inertial_fusion/`) — **Disqualified**. 1992 IFE review predates the ultrashort-pulse / block ignition approach entirely. Contains no data relevant to femtosecond DPSSL on nanostructured targets, non-thermal p-B11 ignition, or direct alpha energy conversion.
138:10. **Accelerators for IFE** (`knowledge/sources/accelerators_for_inertial_fusion_energy_production/`) — **Disqualified**. Accelerator-driver-specific; no overlap with DPSSL laser driver architecture used by Marvel or HB11.
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I have now read all the relevant sources. Let me compile the gap assessment.
```

## Blocking-tier lines (new)

```
104:| Target gain (G) | truly-unknown | blocking | HB11 stated "4 orders of magnitude from net gain" (2022). Marvel has not disclosed gain from 2,000+ shots. No non-thermal p-B11 gain has been demonstrated publicly. |
105:| Fusion yield per shot (Ef, GJ) | truly-unknown | blocking | Required for Hawker yield cost (βEf) term. Completely absent from all sources. |
106:| Laser energy per shot (Ed, J) | proprietary | blocking | Marvel ATLAS has two 100 J lasers in demo phase; commercial plant uncharacterized. |
107:| Actual laser wall-plug efficiency (μd) | proprietary + not-yet-demonstrated | blocking | Femtosecond DPSSL at 10 Hz, petawatt class: no demonstrated system. 10% is target only. |
108:| Target cost (δ, $/target) | derivable (but unverified) | blocking | Marvel cites semiconductor lithography; no cost projection. NIF targets ~$1M each; semiconductor analogy might reach $0.10-1.00/target at volume, but entirely unvalidated. |
109:| Reaction chamber capital cost | not-yet-sourced | blocking | No published design; HB11 UNSW study just commenced; Marvel-Siemens conceptual design unpublished. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/23-laser-icf-nanostructured-target.md	2026-05-22 12:59:21.079525384 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/gap_report.md	2026-05-22 15:15:23.120761784 -0700
@@ -1,109 +1,79 @@
-I have enough information to write the full assessment. Let me compile it now.
-
----
+I have now read all the relevant sources. Let me compile the gap assessment.
 
 # Gap Assessment: Laser ICF - Nanostructured Target (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-
-**Summary**: The available data covers company roadmaps, basic physics constraints, and DPSSL driver technology in reasonable depth, but is nearly empty on the two things LCOE modeling requires most: an experimentally grounded fusion gain value and any published plant-level cost structure. Both Marvel Fusion and HB11 Energy are pre-ignition companies; all claims about gain, energy conversion, and capacity factor are targets, not demonstrated results. A parameterized LCOE model can be built using the Hawker IFE framework, but the key inputs (gain G, laser wall-plug efficiency in the femtosecond regime, target cost per shot) are either proprietary or genuinely unknown.
-
----
+**Summary**: Two companies (Marvel Fusion and HB11 Energy) have produced enough public material to characterize the concept architecture, technology trajectory, and qualitative cost structure. However, both lack published plant studies, neither has approached net gain (HB11 explicitly stated "four orders of magnitude from net gain" in 2022), target gain G is entirely uncharacterized, and no laser wall-plug efficiency has been demonstrated at the femtosecond pulse durations and repetition rates required. The Hawker IFE economic model and Xcimer DPSSL cost paper provide applicable fleet-wide analogues for framework and driver cost parameters, but the blocking physics and engineering unknowns (G, yield per shot, target cost at scale) cannot be resolved by analogues alone.
 
 ## Section Coverage
 
 ### 1. Availability of Data
 **Coverage**: Partial
 
-**Available**:
-- Company technology descriptions with moderate depth: Marvel Fusion (femtosecond DPSSL on nanostructured Si targets, 10 Hz target, ATLAS facility, ~EUR385M funding, ~500 lasers per plant, Siemens Energy power plant co-design announced) [`optics-news-16-4-4.md`, `binding-ultrashort-pulse-laser-fusion.md`, `marvel-fusion-2025-updates.md`]
-- HB11 Energy approach: thousands of commercial DPSSL units, foam targets 10× more efficient than solid for proton acceleration, ~1 Hz, steam cycle conversion [`energynewsbulletin-energy-transition-features-articles.md`, `iter-02/sources/hb11-energy-2025-updates.md`]
-- EU CORDIS CFE-NANO project fact sheet: 100 MW pilot target 2033, demo facility at CSU 2027 — confirms Marvel roadmap at EU official level [`marvel-fusion-2025-updates.md`]
-- Theoretical p-B11 physics in a *tokamak* context (ENN/Cai et al.): establishes breakeven constraints (nτ ~ 2.3×10²¹ m⁻³·s at Ti~380 keV, H-factor requirements), bremsstrahlung and synchrotron radiation barriers [`arxiv-2201-12818.md`]
-- DPSSL driver technology: comprehensive 2025 LLNL/FBH review covering diode pump requirements for IFE (10 kJ, 10–20 Hz beamlines), cost drivers ($0.3–1.3/W today → $0.01/W target at IFE volume), reliability gaps (demonstrated 28 Mshots vs. required 3–20 Gshots), packaging bottlenecks [`osti-servlets-purl-3008974.md`]
-- Mercury DPSSL program: demonstrated 10% wall-plug efficiency at 10 Hz / 100 J with nanosecond pulses — the benchmark DPSSL architecture for IFE [`osti-servlets-purl-15013216.md`, `osti-servlets-purl-15013230.md`]
-- NIF optics cost data: replacement costs for NIF-scale ns-laser systems ($5.6M/yr incremental at 2.6 MJ operation) — useful as upper-bound analog [`osti-servlets-purl-1400089.md`]
-- HB11 foundational physics abstract: Hora et al. avalanche boron fusion concept, block ignition + magnetic trapping as the theoretical basis [`arxiv-1603-02579.md`]
-
-**Missing**:
-- Peer-reviewed publications reporting actual p-B11 gain from *laser* experiments (contrast with the 2,000+ internal experiments cited by Marvel in CORDIS but unpublished)
-- Published plant study or pre-conceptual reactor design from either company
-- Any independent techno-economic analysis specific to this concept
+**Available**: Company websites, press releases, and investor-grade materials for both Marvel Fusion (€385M total funding, CSU demo facility $150M, Siemens Energy conceptual plant design partnership) and HB11 Energy (UNSW materials collaboration, Applied Sciences 2022 paper). The CORDIS CFE-NANO project sheet (`iter-02/sources/marvel-fusion-2025-updates.md`) confirms 2,000+ experiments, 100 MW pilot target 2033, and a proof-of-technology demo at CSU by 2027. HB11's 2022 Osaka University experiment (`newatlas-energy-hb11-laser-fusion-demonstration.md`) provides the only peer-reviewed experimental result — ~1.4×10¹¹ alpha particles, 0.005% laser-to-alpha energy conversion efficiency. A p-B11 tokamak system code paper (`arxiv-2201-12818.md`) exists but covers a different (MCF/thermal) approach to p-B11 and is not directly applicable to the non-thermal block ignition pathway. DPSSL technology papers from LLNL/FBH (`osti-servlets-purl-3008974.md`, Mercury laser activation and design, `osti-servlets-purl-15013216.md`, `osti-servlets-purl-15013230.md`) provide driver TRL context.
+
+**Missing**: No published plant design study from either company (Siemens Energy conceptual design is in progress but unpublished). No peer-reviewed experimental data from Marvel Fusion — all 2,000+ experiments are undisclosed. No published target gain or Q value from either company.
 
 **Gaps**:
-- No experimental gain data published — `truly-unknown` (Marvel has internal data from 2,000+ shots; not disclosed) — **blocking**
-- No independent TEA or plant study — `proprietary` — **blocking**
-- Both companies are pre-ignition; all "data" is target claims, not measured results — `truly-unknown` — **blocking**
+- Published plant study (either company) — proprietary — blocking
+- Marvel Fusion experimental results (2,000+ shots) — proprietary — blocking
+- HB11 experimental program post-2022 — proprietary — important
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**:
-- Physics challenge structure is well-characterized: the bremsstrahlung barrier in p-B11 (fusion power < radiation power without synchrotron suppression and Ti/Te ≫ 1) is quantified in the ENN tokamak system code paper. Synchrotron radiation with wall reflectivity <0.99 severely penalizes gain in magnetic systems; laser ICF bypasses this by operating on inertial timescales too short for synchrotron loss to accumulate [`arxiv-2201-12818.md`]
-- Non-thermal block ignition mechanism described qualitatively: femtosecond laser creates a density-modulated plasma block that accelerates and triggers avalanche via elastic alpha collisions rather than thermal equilibration [`arxiv-1603-02579.md` abstract; `binding-ultrashort-pulse-laser-fusion.md`]
-- The DPSSL laser system as a cost modeling challenge is well-characterized: diode laser costs dominate (at least ⅓–½ of beamline cost even at IFE scale), packaging is the bottleneck, 10 Hz / 10% wall-plug efficiency is the target for nanosecond systems [`osti-servlets-purl-3008974.md`]
-- Marvel's hybrid energy conversion (magnetic + electrostatic + steam, claimed ~70% overall) is identified but not engineering-validated [`dossier.md`]
-
-**Missing**:
-- Quantified gain model for non-thermal block ignition: what ignition conditions Marvel's nanostructured targets actually achieve is not in public literature. The ENN paper shows Q > 1 requires H-factor >> current capability in a *tokamak*; whether block ignition bypasses this is the core unvalidated claim
-- Wall-plug efficiency for femtosecond DPSSL systems: Crump 2025 covers nanosecond systems (target ≥10% wall-plug). Femtosecond / petawatt systems are fundamentally less efficient due to CPA pulse stretching/compression losses, grating losses, and lower average power. This is a significant and poorly-quantified gap for cost modeling
-- Coupling efficiency between femtosecond pulse and nanostructured target: how much of delivered laser energy actually reaches the fuel is unquantified in public sources
-- Alpha particle energy collection efficiency for hybrid conversion: "~70%" claimed by Marvel but no engineering design or validation available
+**Available**: The fundamental physics challenge is well-characterized in the literature. The non-thermal block ignition mechanism (HB11 uses picosecond pulses + kilotesla magnetic field; Marvel uses femtosecond pulses on nanostructured silicon nanowire arrays) bypasses classical ICF compression but introduces novel plasma physics not covered by standard ICF system codes. The p-B11 tokamak system code paper (`arxiv-2201-12818.md`) documents the enormous requirements for thermal MCF p-B11 (nτ ~2.3×10²¹ m⁻³s minimum, H factor 10+ needed, synchrotron radiation losses reducing Q=4.14 to 0.84 at 95% wall reflectivity) — these are MCF constraints but illustrate why p-B11 physics is fundamentally harder than D-T regardless of approach. The Xcimer whitepaper (`commercialization_of_laser_fusion_energy/output.md`) documents the laser IFE challenge set: wall-plug efficiency × scientific gain product must reach ~10 for commercial viability, versus NIF's current ~0.02. Marvel's approach produces this challenge acutely: femtosecond DPSSL systems have lower demonstrated efficiency (~5% wall-plug for Mercury-class systems per `osti-servlets-purl-15013230.md`) and the non-thermal gain mechanism has not been validated at relevant scale. HB11's 2022 experiment demonstrated ~0.005% laser-to-alpha conversion efficiency — four orders of magnitude short.
+
+**Missing**: No system-level energy balance model from either company. No published neutron/x-ray/debris characterization from Marvel Fusion's LION 2 chamber. No validated gain scaling law for the non-thermal block ignition mechanism.
 
 **Gaps**:
-- Femtosecond DPSSL wall-plug efficiency (commercial scale) — `proprietary` / `not-yet-sourced` — **blocking** (drives recirculating power fraction)
-- Target coupling efficiency and ignition threshold — `proprietary` — **blocking** (drives required laser energy per shot)
-- Gain G from block ignition — `proprietary` — **blocking** (existential for LCOE)
-- Direct alpha capture engineering efficiency — `proprietary` / `not-yet-sourced` — **important**
+- Energy balance model (Q_sci pathway, drive efficiency × gain product) — truly-unknown for femtosecond block ignition — blocking
+- Gain scaling law for non-thermal p-B11 under laser acceleration — not-yet-sourced (may be in classified/proprietary Marvel results or CA-PROBONO publications) — blocking
+- Alpha particle energy capture efficiency in non-thermal regime — truly-unknown at commercial scale — important
+- Plasma debris, x-ray, and thermal loading per shot — not-yet-sourced — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- DPSSL pump diodes: TRL 4–5 for IFE conditions. Current state: 1 kW/bar, 65% electro-optical efficiency, 28 Mshots demonstrated. IFE requirements: 500 W–1 kW/bar, 70% efficiency, 3–20 Gshots — a 100–700× reliability gap. Path exists but not demonstrated [`osti-servlets-purl-3008974.md`]
-- Mercury DPSSL: demonstrated TRL 4 at 100 J / 10 Hz / 10% wall-plug for nanosecond pulses (1999–2001 era). Scales to kilojoule/megajoule class in principle [`osti-servlets-purl-15013216.md`]
-- Nanostructured target fabrication: Marvel uses standard semiconductor lithography (300 mm wafer, ~5000 targets/wafer) — manufacturing process exists commercially, but IFE-rate target injection and debris management at 10 Hz are undemonstrated. TRL ~3 for this specific application [`dossier.md`; patent US20230073280A1]
-- HB11 low-density foam targets: in-house production established, 10× proton acceleration efficiency vs. solid targets claimed. TRL ~3–4 for production; injection at 1 Hz undemonstrated [`energynewsbulletin-energy-transition-features-articles.md`]
-- CALA LION 2 experimental chamber (Marvel): operational July 2025, but this is an experimental facility not a prototype power plant
-- Partner ecosystem: Trumpf (laser manufacturing), Thales (laser components), Siemens Energy (power plant design), Fraunhofer, CEA — mature industrial partners reduce TRL transition risk
-
-**Missing**:
-- Reaction chamber design: no published chamber design for non-thermal p-B11 laser ICF. NIF-style chambers are for nanosecond implosion and spherical geometry; Marvel's non-compressive approach requires fundamentally different chamber architecture
-- Alpha particle collection system: no published TRL assessment for the magnetic/electrostatic direct conversion
-- Target injection and debris clearing at IFE rep rate: for 10 Hz, targets must be injected and debris cleared in 100 ms windows — no demonstrated prototype
-- DPSSL at petawatt class / femtosecond pulse duration: the ATLAS facility at CSU is described as ~7 PW combined at 10 Hz but this is a planned system, not operating at full specification
+**Available**: The DPSSL driver subsystem is reasonably characterized through the literature:
+- Mercury laser (`osti-servlets-purl-15013216.md`, `osti-servlets-purl-15013230.md`): demonstrated 100 J at 10 Hz, 10% wall-plug efficiency (TRL ~6 for 100 J class DPSSL at 10 Hz)
+- HAPLS at CSU: demonstrated ~3.3 PW at 3.3 Hz (Marvel uses CSU for ATLAS demo). Commercial plant requires ~7 PW combined at 10 Hz.
+- Diode laser pumps (`osti-servlets-purl-3008974.md`): current state-of-art at ~1 kW/bar, cost $0.3-1.3/W. For 10-20 Hz IFE, need 3-20 Gshots lifetime — currently demonstrated only to ~100 Mshots. No qualification standard exists for IFE reliability. TRL ~4-5 for IFE-spec diodes.
+- NIF optics damage assessment (`osti-servlets-purl-1400089.md`): demonstrates $5.6M/year additional O&M cost at 2.6 MJ nanosecond operation (proxy for optics damage complexity; femtosecond regime is different but illustrates cost magnitude).
+- Nanostructured silicon targets: semiconductor lithography demonstrated at ~5,000 targets/300mm wafer. No public data on target survivability in fusion chamber environment. TRL ~3.
+- HB11 foam targets: in-house manufacturing demonstrated per `energynewsbulletin.md`. TRL ~3.
+- Reaction chamber: HB11 UNSW study just commenced (postdoc positions open as of August 2025 per `hb11-2025.md`). Marvel has Siemens Energy partnership for conceptual plant design. TRL ~1-2.
+- Direct energy conversion (Marvel's hybrid magnetic/electrostatic/steam): claimed "~70% efficiency" on website but no published engineering concept. TRL ~2.
+- Target injection and alignment at 10 Hz: not discussed publicly. TRL ~2.
+
+**Missing**: TRL for the actual ignition mechanism (block ignition on nanostructured target). No experimental demonstration at conditions relevant to commercial operation from either company.
 
 **Gaps**:
-- Reaction chamber TRL — `not-yet-sourced` / `proprietary` — **important**
-- Target injection system TRL — `not-yet-sourced` — **important**
-- Femtosecond DPSSL at IFE average power (10 Hz, PW class, sustained) — TRL 2–3, `not-yet-sourced` — **blocking** for timing
-- Direct energy conversion TRL — `not-yet-sourced` — **important**
+- DPSSL system at petawatt-class 10 Hz demonstrated — not-yet-demonstrated; TRL 4-5 — blocking
+- Block ignition mechanism validated at commercially relevant conditions — truly-unknown — blocking
+- Target injection/tracking system at 10 Hz — not-yet-sourced — important
+- Direct energy conversion engineering prototype (Marvel) — truly-unknown — important
+- Reaction chamber design and TRL — truly-unknown — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- Aneutronic fuel cycle advantage: no tritium breeding, no lithium, no beryllium, no LiPb blanket. Steel construction for reaction chamber is sufficient (no activation issues from high-energy neutrons). UNSW materials collaboration with HB11 specifically validating conventional steel for chamber construction [`dossier.md`; `hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to.md`]
-- Diode laser supply chain: bottleneck clearly identified — GaAs diode bars, facet passivation, CuW submounts, FAC collimators. Manufacturing is dominated by packaging costs (>50% of stack cost). Requires 100–1000× production scale-up from today; learning curve models suggest $0.01/W is achievable at sustained IFE demand [`osti-servlets-purl-3008974.md`]
-- Nanostructured Si targets: use standard CMOS-fab silicon processes; supply chain for silicon wafers is mature. The specialized nanowire lithography is a variant of existing semiconductor manufacturing [`dossier.md`]
-- HB11 foam targets: proprietary in-house production, not externally sourced. Supply chain dependency on maintaining proprietary process at scale
-
-**Missing**:
-- Boron-11 isotope enrichment: natural boron is 80% B-11 / 20% B-10. For IFE applications, enrichment to near-100% B-11 is required. No data on B-11 enrichment production capacity, cost per kg, or supply chain for IFE-scale operations. This is a potentially significant gap that could affect fuel cost estimates
-- Optical coatings and laser optics lifecycle at 10 Hz PW class: NIF's optics recycle/replacement cost is documented for nanosecond pulses. Femtosecond pulse optics face different damage mechanisms (multiphoton ionization, B-integral) and no IFE-rate cost data exists
-- High-power laser amplifier crystals (Yb:YAG or Nd:glass) at scale: not addressed in concept-scoped sources
+**Available**: The fuel materials (hydrogen and natural boron, which is ~80% ¹¹B by atom) are abundant and present no supply chain concern — this is a stated advantage of both concepts. The UNSW/HB11 collaboration (`hb11-2025.md`) confirms that the low-neutron environment allows steel construction rather than tungsten or other activation-resistant materials, reducing first-wall material challenges significantly. Silicon wafers for Marvel's nanostructured targets use standard semiconductor lithography supply chains — a deliberate architectural choice noted in both `optics-news-15-10-4.md` and `binding-ultrashort-pulse-laser-fusion.md`. The DPSSL supply chain bottleneck is well-documented: current diode bar cost $0.3-1.3/W (`osti-servlets-purl-3008974.md`), requiring ~1,000× production scaling to reach the floor of $0.01/W. The Xcimer paper (`commercialization_of_laser_fusion_energy/output.md`) provides the absolute floor cost analysis: $0.02/W for diode pump power after full supply chain buildout, with a commercial 10 MJ DPSSL requiring ~170 GW of diode pump power at today's prices = ~$50B in diodes alone.
+
+**Missing**: No published laser diode procurement strategy or volume production timeline from Marvel or HB11. No supply chain analysis for Yb:YAG or Nd:glass gain media at 500-laser plant scale. No analysis of crystal growth scalability (Mercury laser faced S-FAP crystal growth defect challenges per `osti-servlets-purl-15013216.md`).
 
 **Gaps**:
-- B-11 enrichment cost and supply chain — `not-yet-sourced` — **important** (affects fuel cost per shot)
-- Laser optics replacement rate at femtosecond / PW class — `not-yet-sourced` — **important**
-- Target volume manufacturing cost — `proprietary` — **blocking** for LCOE
+- Laser diode production plan (500 lasers needed per PLT/SPRIND per `optics-news-16-4-4.md`) — proprietary/not-yet-sourced — important
+- Gain medium crystal supply (Yb:YAG at plant scale) — not-yet-sourced — important
+- Target manufacturing scale-up (billions of targets per plant-year) — not-yet-sourced — important
+- HB11 foam target supply chain at 1 Hz plant scale — not-yet-sourced — important
 
 ---
 
@@ -112,73 +82,76 @@
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Repetition rate | 10 Hz (Marvel), ~1 Hz (HB11) | dossier | m |
-| Fuel type | p-B11, aneutronic | dossier | h |
-| Tritium breeding cost | N/A | dossier | h |
-| Neutron shielding cost | Minimal (thin steel) | dossier; UNSW | m |
-| Plant output target | 100 MW pilot (2033), commercial scale unspecified | CORDIS | l |
-| Diode laser cost (current) | $0.3–1.3/W | Crump 2025 | h |
-| Diode laser cost (IFE target) | ~$0.01/W at 1000× volume scale | Crump 2025 | m |
-| Driver laser count (commercial) | ~500 laser systems | optics-news-16-4-4 | l |
-| DPSSL wall-plug efficiency (ns) | ~10% (target), demonstrated at 100 J | Mercury/Payne 1999 | h (for ns) |
-| DPSSL wall-plug efficiency (fs) | <1% current, target unclear | dossier gap | l |
-| Target yield per wafer (Marvel) | ~5000 per 300 mm wafer | dossier | m |
-| Energy conversion efficiency | ~70% claimed (Marvel hybrid) | dossier | l |
-| Total capital raised | EUR385M (Marvel) | optics-news | h (not plant cost) |
-| IFE LCOE range (generic) | ~$25/MWh under optimistic assumptions | Hawker 2020 (fleet-wide) | m (generic IFE) |
+| Repetition rate (f) | 10 Hz (Marvel), ~1 Hz (HB11) | Dossier (company websites) | m |
+| Wall-plug efficiency target (μd) | ~10% target (HB11); ~10-15% (DPSSL class, Marvel analogue) | `energynewsbulletin.md`; `commercialization_of_laser_fusion_energy/output.md` | l |
+| Pilot plant output | 100 MW (Marvel 2033 pilot) | `marvel-fusion-2025-updates.md` (CORDIS) | m |
+| Commercial concept output | ~1 GW baseload (HB11) | Dossier (HB11 website) | l |
+| Fuel cycle | p+¹¹B → 3α, aneutronic, no tritium | Dossier | h |
+| Target material | Silicon nanostructures (Marvel); low-density foam (HB11) | `optics-news-15-10-4.md`; `energynewsbulletin.md` | h |
+| First-wall material | Steel (HB11, per low-neutron environment) | `hb11-2025.md` | m |
+| Driver cost analogue (γ) | DPSSL current ~$700-1000/J on-target; absolute floor ~$0.02/W diode pump → ~$100-200/J system | `commercialization_of_laser_fusion_energy/output.md` | l (analogue) |
+| Driver cost reference (γ) | NIF: $9.5/J; First Light pulsed power: $1.7/J | `a_simplified_economic_model_for_inertial_fusion/output.md` | l (analogue) |
+| Plant cost analogue (α) | IFE proxy $3600/kWe (HYLIFE); range $1000-6000/kWe | `a_simplified_economic_model_for_inertial_fusion/output.md` | l (analogue) |
+| O&M analogue (ε) | IFE framework: ε in $/kWe-yr (parameterized) | Hawker model | l (analogue) |
+| Laser count (commercial plant) | ~500 laser systems | `optics-news-16-4-4.md` (PLT/SPRIND) | m |
+| Energy conversion pathway | Hybrid (Marvel: magnetic+electrostatic+steam); Steam cycle (HB11) | Dossier | m |
+| Conversion efficiency claim | ~70% (Marvel, unengineered claim) | Dossier (Marvel website) | l |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion gain G (target or achieved) | proprietary | blocking | Core LCOE driver; without this, cannot compute fusion energy per shot. Marvel has 2,000+ unpublished experiments |
-| Laser energy per shot (E_laser) | proprietary | blocking | Required with G to get fusion yield; ATLAS design implies PW class but not quantified |
-| Wall-plug efficiency (femtosecond DPSSL) | not-yet-sourced | blocking | Nanosecond target is 10%; femtosecond systems have fundamentally higher losses (CPA gratings, stretcher/compressor). Could be 0.1–1%. Drives recirculating power |
-| Target cost per shot (nanostructured) | proprietary | blocking | Semiconductor litho cost per target at IFE rate. Critical IFE cost driver. No published estimate |
-| Plant capital cost (any CAS breakdown) | proprietary | blocking | Siemens Energy co-design is in progress but not published |
-| Capacity factor / availability | derivable | important | Analogous to other pulsed IFE; likely ~85–90% with component redundancy but unverified |
-| O&M cost | derivable | important | Can estimate from DPSSL diode replacement schedule + NIF analog; highly uncertain |
-| Laser optics replacement rate (fs) | not-yet-sourced | important | NIF data (osti-purl-1400089) covers ns systems; fs regime not documented |
-| B-11 isotope cost | not-yet-sourced | important | Small fraction of IFE fuel cost but unquantified |
-| First wall / chamber replacement schedule | not-yet-sourced | important | Aneutronic reduces radiation damage; but X-rays and particle debris will still erode surfaces |
-| Balance of plant cost | derivable | important | Can use IFE/MFE analogs from CAS documentation |
-| Alpha particle collection system cost | not-yet-sourced | important | No cost analog exists; direct conversion hardware is novel |
+| Target gain (G) | truly-unknown | blocking | HB11 stated "4 orders of magnitude from net gain" (2022). Marvel has not disclosed gain from 2,000+ shots. No non-thermal p-B11 gain has been demonstrated publicly. |
+| Fusion yield per shot (Ef, GJ) | truly-unknown | blocking | Required for Hawker yield cost (βEf) term. Completely absent from all sources. |
+| Laser energy per shot (Ed, J) | proprietary | blocking | Marvel ATLAS has two 100 J lasers in demo phase; commercial plant uncharacterized. |
+| Actual laser wall-plug efficiency (μd) | proprietary + not-yet-demonstrated | blocking | Femtosecond DPSSL at 10 Hz, petawatt class: no demonstrated system. 10% is target only. |
+| Target cost (δ, $/target) | derivable (but unverified) | blocking | Marvel cites semiconductor lithography; no cost projection. NIF targets ~$1M each; semiconductor analogy might reach $0.10-1.00/target at volume, but entirely unvalidated. |
+| Reaction chamber capital cost | not-yet-sourced | blocking | No published design; HB11 UNSW study just commenced; Marvel-Siemens conceptual design unpublished. |
+| Alpha direct conversion efficiency (actual) | not-yet-sourced | important | Marvel claims ~70% hybrid but no engineering basis published. |
+| Laser component lifetime (Nd, shots) | not-yet-sourced | important | IFE diode requirement: 3-20 Gshots; demonstrated to date: ~100 Mshots (`osti-servlets-purl-3008974.md`). Gap of 30-200× from requirement. |
+| Capacity factor / availability (μa) | derivable | important | No basis for estimate beyond generic IFE analogues. |
+| O&M cost (ε, $/kWe-yr) | not-yet-sourced | important | No published plant O&M model. |
+| Blanket multiplier (Eb) | truly-unknown | nice-to-have | p-B11 is aneutronic so no tritium breeding; fusion alpha energy capture replaces blanket function — but chamber thermal efficiency is unknown. |
 
 ---
 
 ## Source Recommendations
 
-1. **Marvel Fusion / PLT SPRIND publications** — search SPRIND website and Marvel's patent portfolio for detailed laser specifications and any engineering cost estimates. The PLT (Pulsed Light Technologies) technical documents may have more detail than the company press materials. — `unverified — confirm existence before searching`
+1. **Hawker simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — **Integrated**. Read and used. Provides the complete 14-parameter technology-agnostic IFE LCOE framework. Driver cost reference values (NIF $9.5/J, First Light $1.7/J), yield cost bound ($70k/GJ lower, $44M/GJ upper), plant cost proxy ($3600/kWe from HYLIFE), and parameterized O&M structure. This source provides the modeling framework for §5 even where specific parameters remain unknown. Addresses the "no IFE cost methodology" gap — downgraded from blocking to important for the framework itself (the specific physics parameters remain blocking).
+
+2. **Xcimer commercialization of laser fusion energy** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — **Integrated**. Read and used. Provides detailed DPSSL cost breakdown directly applicable to Marvel Fusion's architecture: current cost $0.3-0.4/W for diodes; absolute floor $0.02/W after supply chain buildout; total DPSSL cost $700-1000/J on-target. Wall-plug efficiency target ~15% commercial DPSSL. Quantifies why DPSSL laser cost dominates IFE plant economics and benchmarks the reduction required. This source provides the best available analogue for Marvel's laser cost structure; does not resolve gain Q or target cost.
+
+3. **CA-PROBONO p-B11 research network (ELI ERIC)** — `not-yet-sourced`. The multi-institutional EU COST Action focused specifically on p-B11 physics may contain more recent experimental gain or alpha yield results from Marvel's CSU experiments or European collaborators. Search: "CA-PROBONO COST Action p-B11 fusion 2025-2026" + ELI ERIC publications.
 
-2. **Femtosecond DPSSL wall-plug efficiency** — search CLEO/IFSA/SPIE proceedings (2020–2025) for petawatt-class DPSSL efficiency measurements, especially the HAPLS system at ELI-ALPS (a Marvel partner). The Crump 2025 paper cites HAPLS [ref 10] as a relevant DPSSL milestone — that paper should have efficiency data. — `not-yet-sourced`
+4. **IFSA / CLEO 2025-2026 proceedings** — `not-yet-sourced`. Marvel Fusion has been presenting at laser fusion conferences; IFSA (Inertial Fusion Sciences and Applications) and CLEO are the primary venues. Search for "Marvel Fusion nanostructured target gain" or "HB11 block ignition alpha yield" in 2024-2026 conference proceedings. Note: `unverified — confirm existence before searching`.
 
-3. **LIFE design studies (Bayramian et al., LLNL)** — "Compact, Efficient Laser Systems Required for Laser Inertial Fusion Energy," FST 2011 (cited in Crump as ref 7). This contains the most detailed DPSSL-based IFE plant cost model available publicly, including diode cost breakdown by component. Already cited in Crump 2025. — `not-yet-sourced`
+5. **Marvel Fusion–Siemens Energy conceptual plant design** — proprietary. Expected output would directly address the reaction chamber capital cost and energy conversion pathway gaps. Track through Siemens Energy press releases or EU industrial partnership announcements.
 
-4. **HB11 Energy J. Fusion Energy 2023 paper** — cited in dossier as source 8: "HB11 energy conversion options." This may contain the most technical detail on HB11's energy balance and conversion pathway — `not-yet-sourced`
+6. **OSTI LIFE reactor studies (2011, Dunne et al. / Meier et al.)** — `not-yet-sourced`. The LIFE laser IFE power plant concept from LLNL (2008-2012) provides the most detailed published IFE power plant engineering study for a DPSSL-based approach, including chamber design, target factory costs, and O&M schedules. This is the closest published plant study to Marvel's architecture even though it uses nanosecond rather than femtosecond pulses. Search OSTI for "LIFE laser inertial fusion energy power plant". Note: `unverified — confirm existence before searching`.
 
-5. **Xcimer whitepaper** (fleet-wide: `knowledge/sources/commercialization_of_laser_fusion_energy/`) — covers KrF excimer laser cost breakdown at <$100/J, including detailed laser cost-by-component. Useful analog for driver cost structure even though Marvel uses DPSSL, not KrF. The cost decomposition methodology transfers directly.
+7. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — **Disqualified**. MFE-specific; cost structure for magnetic confinement does not transfer to pulsed IFE concepts. BOP cost components (heat exchangers, steam turbines) are common to HB11's steam cycle approach but at a level of generality that the Hawker model already covers. No concept-specific content applicable to Marvel or HB11.
 
-6. **Hawker 2020 simplified IFE model** (fleet-wide: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable framework. The 14-parameter technology-agnostic model can be parameterized for this concept using Marvel's targets; the Monte Carlo sensitivity analysis will identify which unknowns matter most. **Recommend reading this before building the LCOE model.**
+8. **Economic studies for heavy-ion-fusion** (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`) — **Disqualified**. HIF driver cost structure (induction linac, multi-unit scaling at 5-10 Hz) differs fundamentally from DPSSL laser systems. COE range 3.9-5.8 ¢/kWh for 1.5-3 GWe HIF is a historical analogue but the cost driver (accelerator vs. laser) makes it inapplicable for quantitative laser cost estimation.
 
-7. **p-B11 reactivity and gain physics** — search for Putvinski, Ryutov & Yushmanov (2019), "Fusion reactivity of the pB11 plasma revisited," Nuclear Fusion 59:076018. This updates the reactivity cross-sections and includes a hard upper-bound argument on p-B11 gain. Critical context for evaluating Marvel's non-thermal claims. — `not-yet-sourced` (cited in arxiv-2201-12818.md)
+9. **Energy from Inertial Fusion** (`knowledge/sources/energy_from_inertial_fusion/`) — **Disqualified**. 1992 IFE review predates the ultrashort-pulse / block ignition approach entirely. Contains no data relevant to femtosecond DPSSL on nanostructured targets, non-thermal p-B11 ignition, or direct alpha energy conversion.
+
+10. **Accelerators for IFE** (`knowledge/sources/accelerators_for_inertial_fusion_energy_production/`) — **Disqualified**. Accelerator-driver-specific; no overlap with DPSSL laser driver architecture used by Marvel or HB11.
 
 ---
 
 ## Summary
 
-Proceed to full analysis with explicit acknowledgment of the concept's pre-ignition status. The LCOE model should be built as a parametric sensitivity exercise using the Hawker framework rather than a point estimate. Key moves: (1) read Hawker 2020 for methodology; (2) use Crump 2025 to ground the laser system cost and efficiency; (3) treat fusion gain G as the primary sweep variable (range: 1 to ~1000); (4) treat fs DPSSL wall-plug efficiency as a sweep variable (range: 0.1–5%, noting the nanosecond target of 10% likely does not apply); (5) treat target cost as a sweep variable. The qualitative write-up should be rich — the physics rationale, aneutronic advantages, company ecosystem, and roadmap are all well-documented. The quantitative model will be necessarily speculative but instructive.
-
-The most important sources to acquire before modeling: Hawker 2020 (already in fleet-wide sources), Bayramian et al. 2011 LIFE design study, and HB11 J. Fusion Energy 2023 conversion paper.
+The available data supports a well-characterized qualitative analysis of the architecture, differentiation, and technology trajectory for both Marvel Fusion and HB11 Energy. A quantitative LCOE model can be structured using the Hawker 14-parameter IFE framework and DPSSL cost analogues from the Xcimer paper, but the most critical physics and cost parameters — target gain G, fusion yield per shot, actual laser wall-plug efficiency, and target cost per shot — are either proprietary, undemonstrated, or truly unknown. HB11's own 2022 peer-reviewed results place both companies at least 4 orders of magnitude from net gain. No published plant study exists for either company. Proceeding to a full D1+ quantitative analysis is possible at the qualitative level and with heavy reliance on analogues, but any LCOE estimate will have extremely wide uncertainty bounds (multiple orders of magnitude) and should be framed explicitly as a back-solve / sensitivity analysis rather than a point estimate.
 
----
+**Recommendation**: Proceed to full analysis with explicit acknowledgment that G is the binding unknown. The analysis should be structured around the Hawker model with G, Ef, and target cost as free parameters, back-solved to identify what would be required for commercial viability. Acquisition of the LIFE reactor plant studies from OSTI is recommended before constructing the detailed capital cost model.
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
 blocking_count: 6
-important_count: 8
-counting_method: "deduplicated across all sections: blocking = {fusion gain G, target cost per shot, fs DPSSL wall-plug efficiency, plant capital cost structure, target coupling efficiency/ignition threshold, no experimental gain data published}; important = {chamber TRL, target injection TRL, direct energy conversion TRL, B-11 supply chain, laser optics replacement rate (fs), capacity factor, O&M cost, first wall replacement schedule}"
+important_count: 5
+counting_method: "deduplicated across all sections; blocking = target gain G, fusion yield per shot, laser wall-plug efficiency demonstrated, target cost at scale, reaction chamber capital cost, laser energy per shot; important = driver cost analog precision, direct conversion efficiency, laser component lifetime, capacity factor, O&M cost"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
```
