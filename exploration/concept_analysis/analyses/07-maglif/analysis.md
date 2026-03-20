---
ID: 07-maglif
Concept: MagLIF (D-T)
Company: Pacific Fusion, Fuse Energy Technologies
Status: approved
Created: 2026-03-20
Approved-Date: 2026-03-20
Reuses: []
---

# D1+ Analysis: MagLIF (D-T)

**Concept**: Magnetized Liner Inertial Fusion (MagLIF) — D-T fuel
**Companies**: Pacific Fusion (Fremont, CA), Fuse Energy Technologies (San Leandro, CA)
**Confinement Family**: MIF (Magneto-Inertial Fusion)
**Operation Mode**: Pulsed (~100 ns implosion, target destroyed each shot)

---

## Section 1: Availability of Data

**Rating: Moderate**

MagLIF has a substantial and growing body of peer-reviewed literature originating from Sandia National Laboratories, where the concept was proposed (Slutz et al., *Phys. Plasmas* 17, 056303, 2010) and has been experimentally investigated since 2013 on the Z machine. More than 70 integrated MagLIF experiments have been conducted, generating high-quality publications documenting fusion-relevant conditions (Gomez et al., *PRL* 113, 155003, 2014), record performance metrics (Yager-Elorriaga et al., *Nucl. Fusion* 62, 042015, 2022), and physics scaling projections. The 2025 multi-institutional overview paper by Ellison et al. (*Phys. Plasmas* 32, 090601, 2025), co-authored by Pacific Fusion, Sandia, LLNL, LANL, and University of Rochester, provides the most detailed public roadmap for scaling MagLIF to commercial fusion energy applications. It covers IMG driver architecture, yield scaling relations (χ ∝ I³max), rep rate requirements, chamber clearing challenges, and tritium breeding needs.

Private company transparency is moderate. Pacific Fusion ($900M committed funding) has published substantive technical content: validated FLASH simulation results, the October 2025 self-magnetizing target breakthrough results (Lewis et al. / LeChien, Pacific Fusion blog, February 2026), detailed demonstration facility architecture through The Fusion Report interview, and explicit commercial targets ($0.02/kWh electricity by 2040). Fuse Energy Technologies has published hardware specifications for their TITAN IMG platform through the Not Boring deep dive, including peak power (1 TW), repetitive shot count (100+), and their roadmap to Z-STAR and APEIRON-I. Both companies have filed significant patent portfolios (18+ by Fuse Energy).

**Power plant design studies are sparse and dated.** The most detailed reactor concept study is Z-IFE (SAND2006-7148, Sandia, 2006), which predates the MagLIF concept itself; it was based on older dynamic hohlraum targets and LTD driver architecture. No published power plant study exists for the modern MagLIF + IMG architecture that Pacific Fusion or Fuse Energy are pursuing. No equivalent of ARIES (for tokamaks) or LIFE (for laser ICF) has been published for MagLIF. No system-code outputs analogous to PROCESS or ACCOME exist for this concept family.

**Key data gaps limiting this analysis:**
- No published plant-level system code or cost study for IMG-based MagLIF
- No blanket design disclosed by either company for pure-fusion operation
- No first-wall lifetime or maintenance schedule estimates in the public literature
- Commercial rep rate not disclosed by either Pacific Fusion or Fuse Energy
- Target fabrication cost at volume production not characterized
- Fuse Energy's APEIRON-I is a hybrid fusion-fission concept (not pure MagLIF) and is excluded from this analysis

---

## Section 2: Challenges in Capturing System Function

MagLIF presents several challenges that are structurally distinct from steady-state fusion concepts and require purpose-built LCOE modeling approaches.

### 1. Rep Rate Is the Dominant LCOE Lever (Impact: Critical)

MagLIF produces energy in discrete ~100 ns bursts at sub-Hz rates. Annual energy output equals yield per shot × rep rate × availability. This means rep rate has a multiplicative effect on all capital utilization: a 10× increase in rep rate (0.1 Hz → 1 Hz) produces 10× more annual energy from the identical driver, chamber, and BOP. No other parameter in the model has comparable leverage — not driver cost, not yield, not thermal efficiency. Small changes in rep rate produce non-linear effects on specific capital cost ($/kWe). Standard fusion LCOE formulations that treat capacity factor as an availability-only parameter misrepresent this dynamic: for MagLIF, "effective capacity factor" has two components — plant uptime (maintenance-driven) and achieved rep rate as a fraction of design rep rate (engineering-driven). These failure modes have different cost implications and must be modeled separately.

The published Z-IFE baseline is 0.1 Hz per chamber; Pacific Fusion and Fuse Energy target ~1 Hz, but neither has publicly demonstrated rep-rated operation above single shots at plant-relevant parameters (Ellison et al., 2025, Phase 1a: arxiv-2408-15206-pulsed-magnetic-fusion.md).

### 2. Per-Shot Consumables Create a Cost Floor Without Analogue in MFE (Impact: High)

Each shot destroys the target liner, the recyclable transmission line (RTL), and potentially other hardware. At 1 Hz, this is ~28 million consumable cycles per year. The only public cost estimate for an RTL is $0.70/shot (Olson et al., 2003, Phase 1a: z-ife-power-plant-concept.md), which predates the MagLIF target design. Traditional MagLIF additionally destroys external magnetization coils each shot; Pacific Fusion's February 2026 self-magnetizing target demonstration (composite plastic + aluminum, 50–200 µm Al layer) eliminates external coils from the per-shot bill, which was identified as a "showstopper" cost item (Pacific Fusion blog, 2026, Phase 1a: pacific-fusion-website-technology.md). Per-shot target cost at volume — for either gas-fill or cryo ice-layer configurations — is completely uncharacterized. For GJ-class yields, cryogenic DT ice-layer targets are required (Slutz & Vesey, 2012), adding cryogenic handling infrastructure, per-target cooling time, and DT ice quality control with no cost estimates in the literature.

### 3. Driver Capital Is a Novel Cost Category With No Published Estimate for IMG Architecture (Impact: High)

The pulsed power driver (capacitor banks, switches, transmission lines) is the dominant capital cost item — estimated at 40–60% of total direct capital in system-level analyses — and has no cost analogue in other fusion concepts or conventional power generation. The Z-IFE study estimated $372–400M for an LTD-based driver (SAND2006-7148). The SfA white paper (May 2023) quantified the needed cost reduction: capacitor costs must fall from ~$5/J (current commercial) to <$0.50/J, and component lifetimes must increase from ~10⁴ shots to ~10⁹ shots for commercial viability. No published bottom-up cost estimate exists for the IMG architecture that Pacific Fusion and Fuse Energy are pursuing, despite it being architecturally different from LTD technology. Pacific Fusion's demonstration facility uses 156 modules × 320 bricks at 800 J/capacitor storing ~80 MJ total (Pacific Fusion interview, The Fusion Report, 2026, Phase 1a: pacific-fusion-interview-fusion-report.md), but facility cost is not disclosed.

### 4. Yield Scaling to GJ-Class Relies Entirely on Simulations (Impact: High)

Current Z machine experiments achieve χ = 0.084 ± 0.009 (far below gain > 1) with ~20 MA drive current (Ellison et al., 2025). The yield scaling relation χ ∝ I³max means a 3× increase in current (to 60 MA) produces ~27× more yield, and simulations project ~60 MJ fusion yield at 60 MA, scaling to hundreds of MJ with cryogenic DT fuel liners (Ellison et al., 2025). GJ-class yields — the level needed for baseload power at 0.1 Hz — require ice-layer targets at 60+ MA and rely entirely on 2D simulation (LASNEX, HYDRA, FLASH). The transition from gas-fill to ice-layer targets introduces additional physics uncertainties around impurity mix, ice layer uniformity, and fuel compression dynamics. No experimental validation exists for this critical scaling step.

### 5. Chamber / First-Wall Lifetime Under Combined Loading Is Uncharacterized (Impact: Moderate-High)

Unlike steady-state concepts where neutron wall loading drives blanket replacement schedules, MagLIF chamber components face a unique combination: repetitive GJ-scale mechanical shock (28 million cycles/year at 1 Hz), 14 MeV neutron flux (partially attenuated by FLiBe liquid wall), debris impingement, and FLiBe fluoride corrosion. The thick-liquid-wall concept is designed to protect structural components, but the liquid wall itself must reform between shots. Axial openings where the RTL connects are particularly vulnerable — these components see the full neutron spectrum plus blast loading, with no analogous operational database. The combined loading environment (shock fatigue + neutron embrittlement + thermal cycling + fluoride corrosion) is completely uncharacterized experimentally.

### 6. Regulatory and Licensing Path for Pulsed D-T Facilities (Impact: Moderate)

Tritium handling regulations for a facility processing 28 million D-T shots/year are not established. NRC's 2023 decision to regulate fusion under 10 CFR Part 30 applies, but detailed rulemaking for facilities with this operational profile — pulsed, high-repetition, large activated debris throughput — has not been developed. The licensing cost multiplier observed for steady-state D-T concepts (Stewart & Shirvan's 2.2× building cost factor) may apply in modified form but is not quantified for pulsed architectures.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature.

---

**Rep-Rated Operation — TRL 1–2**
- **Demonstrated**: Single-shot MagLIF fusion on Z machine (70+ experiments). Fuse Energy TITAN completed 100+ repetitive shots at 1 TW (Phase 1a: fuse-energy-technology.md), but this is a technology demo, not fusion-producing. No facility has fired a fusion-producing MagLIF shot at any rep rate.
- **On paper only**: All rep-rated fusion-producing operation. The entire shot cycle — chamber clearing, liquid wall regeneration, RTL insertion and electrical contact at 60+ MA, target insertion (cryo or ambient), capacitor recharge, vacuum re-establishment — must be completed in <1 second at 1 Hz. Each individual step has been studied; none have been integrated.
- **Missing at scale**: Automated RTL insertion and alignment under post-blast conditions; debris clearing from GJ-class shots within ~1 second; liquid FLiBe jet reformation after GJ blast loading; cryo target preservation during chamber insertion; integrated shot-cycle automation at plant-relevant rep rates.

---

**Recyclable Transmission Line (RTL) — TRL 2–3**
- **Demonstrated**: Conceptual studies and cost estimates conducted at Sandia (Olson et al., 2003, Phase 1a: z-ife-power-plant-concept.md). FLiBe-based and steel-based RTL designs analyzed. Single-shot RTL operation inherent to Z machine experiments (the RTL is sacrificial by design).
- **On paper only**: Rep-rated RTL manufacturing and deployment. Automated fabrication at ~28 million units/year. Conical RTL geometry providing standoff while maintaining 60+ MA current capacity.
- **Missing at scale**: RTL insertion robotics operating within a ~1 second cycle in a post-blast environment. RTL material compatibility with FLiBe coolant. Cost-validated mass production (the $0.70/shot estimate from 2003 has not been updated for modern target designs or manufacturing methods).

---

**Tritium Breeding Blanket — TRL 2**
- **Demonstrated**: FLiBe material properties well-characterized from molten salt reactor research (MSRE program). Small-scale lithium-6 tritium production demonstrated. No MagLIF-specific blanket design exists.
- **On paper only**: FLiBe thick-liquid-wall blanket concept studied in Z-IFE (SAND2006-7148, Phase 1a: z-ife-sand2006-7148-thermal-cycles.md) as combined blanket/coolant/shield. Tritium extraction from FLiBe via vacuum degassing or permeation barriers analyzed but not demonstrated at scale.
- **Missing at scale**: Blanket design that survives repetitive GJ-scale shock loading. Tritium extraction systems at kg/day throughput. Tritium permeation barriers on hot metal surfaces in contact with FLiBe. Tritium inventory management for 28M shots/year with sub-percent burn fraction. Neither Pacific Fusion nor Fuse Energy has disclosed a blanket approach for pure-fusion commercial operation.

---

**Fusion Chamber / First Wall — TRL 2–3**
- **Demonstrated**: Thick-liquid FLiBe wall concept analyzed in Z-IFE (SAND2006-7148). Pacific Fusion's demonstration facility uses a deionized water tank as neutron/X-ray absorber (Phase 1a: pacific-fusion-interview-fusion-report.md) — a demo-specific architecture not representative of a power plant.
- **On paper only**: FLiBe liquid jet injection systems (HYLIFE-II heritage), jet reformation timescales, shock absorption capacity. Chamber designs accommodating RTL insertion through the liquid curtain. Electrode and power-feed structures at axial openings.
- **Missing at scale**: Chamber that survives repetitive GJ-scale explosions at 1 Hz over a 30-year plant lifetime. Liquid FLiBe jet systems at the required flow rates and temperatures. Axial electrode structures with characterized lifetime under combined neutron streaming + blast + corrosion loading. Multi-chamber architectures (the Z-IFE concept proposed 12 chambers per plant) not demonstrated at component level.

---

**MagLIF Target Physics — TRL 3–4**
- **Demonstrated**: Fusion-relevant conditions demonstrated on Z (Gomez et al., 2014): magnetized, laser-preheated implosion achieving nτ > 10²¹ keV·m⁻³·s at ~3 keV ion temperature (Knapp et al., 2022, cited in Yager-Elorriaga et al., 2022). 70+ integrated experiments. Pacific Fusion demonstrated self-magnetizing composite targets (plastic + aluminum) at 22 MA, 120 ns on Z machine in late 2025, with FLASH simulations accurately predicting magnetic field penetration (Pacific Fusion blog, February 2026, Phase 1a: pacific-fusion-website-technology.md).
- **On paper only**: Ice-layer cryogenic DT targets needed for GJ-class yields — simulated in Slutz & Vesey (2012) but never tested experimentally. Pacific Fusion's goal to eliminate laser preheat (announced as next milestone post-self-magnetization).
- **Missing at scale**: χ > 1 (net fusion gain) at any current level. 60+ MA driver facility for testing GJ-class yield projections. Demonstration that self-magnetizing targets scale to higher currents. Cryo ice-layer target fabrication pipeline.

---

**Pulsed Power Driver (IMG Architecture) — TRL 4–5**
- **Demonstrated**: Z machine at 27 MA has operated reliably for decades (traditional Marx/PFN architecture). IMG architecture: Fuse Energy TITAN I achieved 1 TW at 0.8 MA / 1.6 MV with 100+ repetitive shots, claiming 3× compactness, 1000× longer lifetime, 2× efficiency, 5× lower cost vs. existing generators (Phase 1a: fuse-energy-not-boring-details.md). Pacific Fusion's demonstration facility uses 156 IMG modules storing ~80 MJ, delivering ~8 MJ to target (~10% coupling) at 60+ MA in ~100 ns (Phase 1a: pacific-fusion-interview-fusion-report.md). IMGs achieve ~90% energy efficiency versus ~50-60% for conventional Marx generators (Ellison et al., 2025).
- **On paper only**: Plant-scale IMG cost reduction from $5/J to <$0.50/J capacitor pricing. Multi-million shot lifetime at full plant parameters. Distributed recharge architecture for 1 Hz operation (requiring ~80–130 MW continuous charging power at GJ-class yields).
- **Missing at scale**: 60+ MA drive capability (current demos at ~1 MA scale for rep-rated operation). Verified shot lifetime >10⁶ at relevant current levels. Bottom-up cost estimate for full plant driver.

---

**Laser Preheat System (if retained) — TRL 5–6**
- **Demonstrated**: Z-Beamlet (kJ-class Nd:glass laser) routinely used for MagLIF preheat on Z. Industrial kJ-class lasers exist and are commercially available.
- **On paper only**: Pacific Fusion's announced goal is to eliminate laser preheat entirely following their self-magnetization success (Pacific Fusion blog, February 2026). If eliminated, this subsystem drops from the cost model entirely.
- **Missing at scale**: Rep-rated laser operation at required specifications (if retained). Laser-chamber integration with RTL insertion cycle. Beam alignment for ~mm-positioning of MagLIF targets.
- **Note**: Elimination of laser preheat is a stated near-term objective for Pacific Fusion. If achieved, this subsystem is replaced by a design credit — no capital cost, no optics maintenance, fewer chamber penetrations.

---

**Energy Conversion / Balance of Plant — TRL 6–7**
- **Demonstrated**: Conventional steam Rankine, gas Brayton, and supercritical CO₂ Brayton cycles at GW scale in fission and fossil plants. Z-IFE study evaluated all four and concluded combined Brayton-Rankine offers highest thermal efficiency (SAND2006-7148, Phase 1a: z-ife-sand2006-7148-thermal-cycles.md). Achievable thermal efficiency: ~40%.
- **On paper only**: Integration with pulsed thermal source. Thermal buffering system to smooth GJ bursts at 0.1–1 Hz into steady turbine input. sCO₂ cycles optimized for fusion thermal profiles.
- **Missing at scale**: Thermal inertia requirements for GJ-class pulsed source at 0.1 Hz — substantial thermal buffer mass required, representing a capital cost not present in steady-state concepts. FLiBe-compatible heat exchanger design under combined tritium permeation and moderate neutron flux.

---

## Section 4: Key Materials and Supply Chain Considerations

**Beryllium (liner/target material — traditional MagLIF)**
Current Z machine experiments use beryllium cylindrical liners. Beryllium is toxic, expensive (~$800/kg), carcinogenic in powder form, and supply is dominated by a single US producer (Materion Corp., global production ~300 t/year). At 28 million shots/year with even mg-scale Be per target, the aggregate Be demand is significant and the supply chain is not equipped for fusion-scale production. Pacific Fusion's composite targets (plastic + aluminum) directly address this constraint — their self-magnetizing design uses no beryllium in the target liner, representing a material supply chain advantage (Phase 1a: pacific-fusion-website-technology.md). If FLiBe is used as blanket, beryllium reappears as a blanket material supply concern (shared with the FLiBe constraint below).

**Tritium**
Standard D-T constraint. Required startup inventory ~1–5 kg at ~$30,000/g (current market). Global inventory ~25–30 kg (primarily from CANDU heavy-water reactor byproduct production), declining as CANDU fleet retires. Must breed at TBR > 1 in FLiBe blanket. The pulsed operation creates a more complex tritium dynamics problem than steady-state: unburned tritium (~97% of fuel per shot) disperses into chamber exhaust gas and FLiBe coolant with each pulse, requiring continuous extraction rather than periodic batch processing. Tritium permeation through hot FLiBe-facing metals is a leak risk requiring permeation barriers. Regulatory tritium inventory limits may constrain plant design.

**FLiBe (Li₂BeF₄)**
The baseline blanket/coolant material for Z-IFE and the leading candidate for MagLIF power plants. Not currently produced at industrial scale. Requires both beryllium (supply constraints above) and lithium-6-enriched lithium for tritium breeding. Li-6 enrichment to >90% is commercially available but at low volume; scaling to a fleet of fusion plants would strain existing enrichment capacity. Li-6 enrichment uses legacy mercury amalgam processes (Russia, China) or more recently isotopic separation — neither is established at fusion-fleet scale. The FLiBe supply chain is shared with certain fission concepts (Kairos Power), which may provide co-development leverage. Estimated future NOAK cost of FLiBe ~$154/kg (Araiinejad & Shirvan, 2025, cited in handwritten exemplar for HTS tokamak).

**Capacitors and Switches (Driver)**
The IMG driver is built from thousands of identical capacitor-switch "bricks." These use commodity materials (ceramics, metals, dielectrics) but require precision manufacturing at high voltage (±100 kV per brick for Pacific Fusion's system). The SfA white paper (May 2023) quantified the required cost trajectory: from ~$5/J (current commercial pulsed power capacitors) to <$0.50/J — a 10× reduction. Component lifetime must improve from ~10⁴ shots (current pulsed power) to ~10⁹ shots (~30 years at 1 Hz). Pacific Fusion's architecture explicitly targets manufacturing learning as the cost reduction mechanism, with "bricks" designed as mass-producible units analogous to battery modules. No production-volume cost data exists for IMG bricks at the required specifications. The Tier 1 idiot-index priority: current $/J idiot index for driver components is estimated at 10–50× over raw material cost, making this the primary manufacturing cost compression opportunity in the entire cost structure.

**No HTS or Rare Earth Superconductors Required**
Unlike tokamak, stellarator, and high-field compact concepts, MagLIF requires no REBCO tape, no Nb₃Sn, and no large superconducting magnets. External magnetic field premagnetization was historically provided by conventional copper Helmholtz coils — themselves destroyed per shot in traditional MagLIF — now eliminated by Pacific Fusion's self-magnetizing targets. The drive field is generated entirely by the pulsed current through the liner. This represents a significant supply chain advantage: the REBCO supply bottleneck (global production capacity ~thousands km/year vs. >5,000 km needed per reactor for compact tokamak concepts) is entirely absent from MagLIF economics.

**Target Mass Production Infrastructure**
Whether beryllium-based (traditional) or composite plastic + aluminum (Pacific Fusion), targets require high-precision fabrication at ~28 million units/year for 1 Hz operation. For cryogenic ice-layer targets (needed at GJ-class yields), each target must reach <19 K with adequate DT ice layer uniformity, requiring a parallel batch-cooling pipeline running continuously. NIF requires 15–20 hours per target for acceptable cryogenic layering; Sandia's Z machine cryostat achieves ~5 minutes per target. At 1 Hz, neither approach is remotely compatible with rep-rate demands without a fundamental paradigm shift in target manufacturing. The per-target capital infrastructure and cost for mass-produced cryo targets has no published estimate.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Rep rate (Z-IFE baseline) | 0.1 Hz (10 s cycle) | Z-IFE SAND2006-7148 | high | Per chamber; 12-chamber plant at 0.1 Hz each = ~1 Hz effective |
| Rep rate (company target) | ~1 Hz | Ellison et al. 2025; Pacific Fusion "piston engine" description | medium | Not publicly demonstrated; Z-IFE proposed multi-chamber as alternative |
| Fusion yield (Z-IFE baseline) | 2–3 GJ/shot | Z-IFE SAND2006-7148 | medium | High-yield, low-rep-rate paradigm; requires 60+ MA and cryo targets |
| Fusion yield (simulation, 60 MA gas-fill) | ~60 MJ/shot | Ellison et al. 2025 (χ ∝ I³) | medium | Scaling from current Z experiments; not experimentally validated at 60 MA |
| Fusion yield (simulation, 60 MA cryo) | hundreds of MJ | Ellison et al. 2025; Slutz & Vesey 2012 | low | Cryo DT ice-layer targets; entirely simulation-based |
| Current achieved on Z (experimental) | ~20–27 MA | Sandia Z Machine; Yager-Elorriaga et al. 2022 | high | 70+ MagLIF experiments conducted |
| Pacific Fusion demo driver — stored energy | ~80 MJ | Pacific Fusion interview, The Fusion Report 2026 | high | 156 modules × 320 bricks × 800 J/capacitor |
| Pacific Fusion demo driver — target coupling | ~8 MJ (~10%) | Pacific Fusion interview, The Fusion Report 2026 | high | ~10% of stored energy reaches target |
| Pacific Fusion demo driver — current | 60+ MA in ~100 ns | Pacific Fusion interview, The Fusion Report 2026 | high | Design spec; not yet achieved experimentally |
| IMG energy efficiency | ~90% | Ellison et al. 2025; Fuse Energy TITAN specs | high | Compared to ~50–60% for conventional Marx generators |
| Fuse Energy TITAN peak power | 1 TW | Fuse Energy / Not Boring deep dive 2026 | high | 0.8 MA, 1.6 MV; 100+ repetitive shots demonstrated |
| Fuse Energy Z-STAR target current | ~12.8 MA | Not Boring deep dive 2026 | medium | 16 TITAN units, planned 2027 |
| RTL cost (per shot) | $0.70/shot | Olson et al. 2003 | low | 2003 estimate; predates MagLIF target design; excludes cryo target cost |
| Driver capital (Z-IFE LTD estimate) | $372–400M | Z-IFE SAND2006-7148 | low | LTD architecture; does not apply to modern IMG design |
| Capacitor cost (current commercial) | ~$5/J | SfA White Paper, May 2023 | medium | Current pulsed power commercial pricing |
| Capacitor cost (required commercial) | <$0.50/J | SfA White Paper, May 2023 | medium | 10× reduction needed; no timeline or manufacturing data |
| Driver component lifetime (current) | ~10⁴ shots | SfA White Paper, May 2023 | medium | Current pulsed power; must reach ~10⁹ for commercial viability |
| Thermal conversion efficiency | ~40% | Z-IFE SAND2006-7148 (combined Brayton-Rankine) | medium | Based on 2006 Z-IFE study; sCO₂ could achieve similar |
| Blanket energy multiplication (estimated) | ~1.1× | [analogue — standard D-T FLiBe blanket] | low | No MagLIF-specific blanket design published; analogous to FLiBe blanket in other D-T concepts |
| Neutron energy fraction | ~80% | Ellison et al. 2025 | high | ~80% of fusion energy in 14 MeV neutrons |
| Startup tritium inventory | ~1–5 kg | [analogue — standard D-T, inferred from handwritten exemplar] | medium | At ~$30,000/g; consistent across D-T fusion concepts |
| Pacific Fusion LCOE target | ~$0.02/kWh | Pacific Fusion website 2026 | medium | Company claim; 2040 target |
| Net electric output (baseline LCOE model) | ~114 MWe | [inferred — handwritten exemplar model, baseline scenario] | medium | 0.1 Hz, 3 GJ yield, $400M driver, 80% availability |
| Net electric output (optimistic LCOE model) | ~950 MWe | [inferred — handwritten exemplar model, optimistic scenario] | low | 1 Hz, 2 GJ yield, $150M driver, 90% availability |
| LCOE (baseline) | ~20 ¢/kWh | [inferred — handwritten exemplar model, baseline scenario] | medium | 73% capital, 27% OPEX; specific capital ~$11,400/kWe |
| LCOE (optimistic) | ~1.1 ¢/kWh | [inferred — handwritten exemplar model, optimistic scenario] | low | Requires 1 Hz, $150M driver, no laser/magnets; ~$620/kWe specific capital |
| Pacific Fusion facility footprint | 73 m × 80 m | Pacific Fusion interview, The Fusion Report 2026 | high | Demo facility; includes 156 modules in spherical arrangement around 6 m insulator stack |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q_fusion (net fusion gain > 1) | truly-unknown | blocking | Not yet demonstrated at any current level; χ = 0.084 at 20 MA is far below ignition |
| Commercial rep rate (Pacific Fusion / Fuse) | proprietary | blocking | Neither company has disclosed; Z-IFE baseline 0.1 Hz; company targets ~1 Hz |
| Target cost at volume production | truly-unknown | blocking | $0.70/shot RTL estimate (2003) does not include target; cryo target cost completely unknown |
| IMG driver capital cost (full plant) | proprietary | blocking | No published bottom-up estimate for IMG architecture; Z-IFE LTD estimate not applicable |
| Blanket design for pure-fusion MagLIF | proprietary/TBD | blocking | Neither company has disclosed; Z-IFE FLiBe concept is 2006 baseline; Fuse APEIRON-I is fission-hybrid |
| First-wall / chamber lifetime | truly-unknown | blocking | Combined neutron + shock + corrosion loading has no experimental database |
| Cryo target fabrication cost at 1 Hz rate | truly-unknown | blocking | No published cost estimate; NIF cryo targets cost ~$1000s each; mass production pathway unknown |
| Tritium system capital + operating cost | not-yet-sourced | important | $50M analogue from ITER-family used in models; commercial fusion-specific data absent |
| RTL insertion automation cycle time | truly-unknown | important | Must complete in <1 second at 1 Hz; no prototype demonstrated |
| Thermal buffering capital cost (pulsed source) | truly-unknown | important | Required for GJ burst smoothing; no design or cost in literature |
| Multi-chamber vs. single-chamber architecture | proprietary | important | Z-IFE proposed 12 chambers; companies haven't disclosed commercial plant architecture |
| Electrode lifetime at axial openings | truly-unknown | important | Highest neutron + shock exposure in plant; no characterization data |
| Specific power plant construction cost ($/kWe) | not-yet-sourced | important | No power plant study for IMG-based MagLIF; FOAK estimates would require system study |
| Q_engineering (recirculating power fraction) | derivable | important | Derivable from driver efficiency + rep rate + thermal efficiency once other parameters known |
| Pacific Fusion demo net yield | proprietary | nice-to-have | Demo aims for ">100 MJ"; specific target yield not disclosed |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_fusion > 1 not demonstrated; χ = 0.084 at Z-machine scale | S1, S3 | truly-unknown | blocking | Requires 60+ MA experimental facility; Pacific Fusion demo facility or equivalent |
| 2 | Commercial rep rate not disclosed by either company | S1, S2, S5 | proprietary | blocking | Company press releases; CRADA publications; FIA submissions |
| 3 | Target cost at volume production (esp. cryo ice-layer) | S2, S4, S5 | truly-unknown | blocking | No published estimate; requires manufacturing feasibility study analogous to IFE target factory literature |
| 4 | IMG driver capital cost for full plant (no published estimate) | S2, S5 | proprietary | blocking | Company disclosures; future CRADA reports; ARPA-E award documentation |
| 5 | Blanket design and tritium extraction approach for pure-fusion operation | S1, S3, S5 | proprietary/TBD | blocking | Neither company has disclosed; Z-IFE FLiBe remains only baseline; future company technical publications |
| 6 | First-wall / chamber lifetime under combined neutron + shock + corrosion loading | S2, S3, S5 | truly-unknown | blocking | No experimental analog; requires dedicated materials testing in relevant environment |
| 7 | Cryo DT ice-layer target fabrication at ~28M units/year | S3, S4, S5 | truly-unknown | blocking | Literature only addresses single-target NIF production; IFE target factory studies provide upper bound |
| 8 | RTL insertion automation cycle time and prototype status | S3 | truly-unknown | important | Z-IFE conceptual studies; no prototype demonstrated; relevant robotics literature |
| 9 | Thermal buffering capital cost for GJ-class pulsed thermal source | S3, S5 | truly-unknown | important | No design study for MagLIF thermal buffering; HYLIFE-II and IFE chamber studies provide partial analog |
| 10 | Electrode lifetime at axial openings (neutron streaming + blast loading) | S3, S5 | truly-unknown | important | Most vulnerable components in design; requires dedicated analysis and experimental data |
| 11 | IMG component lifetime at operational parameters (10⁹ shot target) | S3, S5 | truly-unknown | important | Fuse Energy TITAN at 100+ shots is orders of magnitude short of commercial requirement |
| 12 | Multi-chamber vs. single-chamber plant architecture choice | S5 | proprietary | important | Architectural choice changes capital structure significantly; Z-IFE multi-chamber vs. company single-chamber targeting |
| 13 | Tritium processing system cost for pulsed D-T operation at 1 Hz | S4, S5 | not-yet-sourced | important | ITER tritium plant oversized; commercial fusion-specific tritium system cost studies needed |
| 14 | FLiBe production scale-up cost and timeline | S4 | not-yet-sourced | nice-to-have | Shared constraint with other D-T fusion concepts; Kairos Power FLiBe development relevant |
| 15 | Self-magnetizing target performance at 60+ MA | S3 | truly-unknown | nice-to-have | Only demonstrated at 22 MA; scaling to commercial drive currents unknown |

---

## Section 7: Cross-Concept Notes

No approved prior analyses available for cross-referencing.

The following cross-concept observations are based on domain knowledge and should be formalized when approved prior analyses become available:

**Shared supply chain with other D-T concepts:** Tritium startup inventory, Li-6 enrichment, and FLiBe production are constraints shared with D-T tokamak, stellarator, and General Fusion concepts. The FLiBe supply chain overlap with laser ICF (Xcimer's thick-liquid-wall design) and some D-T MFE concepts means co-development leverage is possible. Conversely, unlike HTS-based compact tokamaks, MagLIF has no REBCO or superconductor supply chain dependency — a structural advantage worth noting explicitly in cross-concept comparisons.

**Pulsed architecture creates distinctive LCOE parameter structure:** MagLIF's per-shot consumables, rep rate dominance, and driver capital structure are shared at a high level with laser ICF (Xcimer, Inertia). However, the driver architecture (electrical vs. optical), target-driver coupling mechanism (contact vs. optical standoff), and chamber clearing approach (RTL insertion vs. free-flight injection) are fundamentally different, producing different cost scaling behaviors. Laser ICF concepts target higher rep rates (5–10 Hz) with lower per-shot yields; MagLIF targets lower rep rates (0.1–1 Hz) with higher per-shot yields. Both approaches can in principle produce the same time-averaged power, but the cost structure is different. A cross-pulsed-concept analysis should make this tradeoff explicit.

**FLiBe thick-liquid-wall concept is shared with Xcimer (laser ICF):** Both Z-IFE/MagLIF and Xcimer use or contemplate thick FLiBe liquid wall chambers. Cost and engineering development in one program (FLiBe redox control, nozzle design, jet reformation dynamics) would benefit the other. This is a potential co-development opportunity across the two pulsed concept families.

---

## Section 8: Sources

1. **Ellison et al., "Opportunities in pulsed magnetic fusion energy," *Physics of Plasmas* 32, 090601 (2025)** — arXiv:2408.15206. Multi-institutional paper (Pacific Fusion, Sandia, LLNL, LANL, U. Rochester) providing the most comprehensive public roadmap for MagLIF commercialization. Covers IMG driver technology, χ ∝ I³ scaling, rep rate requirements, cryogenic DT liner yield enhancement, chamber clearing challenges, and tritium breeding requirements. Primary source for physics scaling, rep rate constraints, and driver architecture characterization. Phase 1a path: `iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md`.

2. **Z-IFE FY2006 Study (SAND2006-7148), Sandia National Laboratories, October 2006** — Most detailed published power plant concept for pulsed-power-driven MIF. Provides baseline rep rate (0.1 Hz), target yield paradigm (2–3 GJ/shot, or 20 GJ single-chamber), multi-chamber architecture (12 chambers per plant), RTL concept, FLiBe blanket baseline, and thermal cycle evaluation (concluded combined Brayton-Rankine is optimal at ~40% efficiency). Primary quantitative reference for plant-level parameters despite predating MagLIF and IMG architecture. Phase 1a paths: `iter-01/sources/z-ife-power-plant-concept.md`, `iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md`.

3. **Pacific Fusion interview — The Fusion Report (Substack), 2026** — Provides detailed Pacific Fusion demonstration facility specifications: 73 m × 80 m footprint, 156 modules, 320 bricks/module, ±100 kV/brick, 160 nF/brick, 800 J/capacitor, ~80 MJ stored energy, ~8 MJ to target, 60+ MA in ~100 ns, 6 m insulator stack diameter. Commercial targets (net facility gain by 2030, first commercial plant by mid-2030s, $0.02/kWh by 2040). Phase 1a path: `iter-02/sources/pacific-fusion-interview-fusion-report.md`.

4. **Pacific Fusion press releases and blog posts (2023–2026)** — Founders' letter confirms D-T fuel. February 2026 post (authored by Keith LeChien, CTO) describes self-magnetizing composite target (plastic + aluminum, 50–200 µm Al) demonstration on Z at 22 MA / 120 ns: eliminates external magnetization coils from per-shot BOM; next goal is laser preheat elimination. CRADA with Sandia confirmed. Phase 1a path: `iter-01/sources/pacific-fusion-website-technology.md`.

5. **Fuse Energy Technologies — Not Boring deep dive, 2026** — Provides TITAN I hardware specs: 238 bricks, 14 stages, 0.8 MA, 1.6 MV, 1 TW peak power, 100+ repetitive shots. Z-STAR roadmap (16 TITAN units, ~15 TW, 12.8 MA, 2027). Critical clarification: APEIRON-I (90 TITAN modules) is a **hybrid fusion-fission** concept with uranium/spent-fuel blanket (~20 MW fusion → ~3 GW thermal → ~1 GWe), fundamentally different from pure MagLIF fusion and excluded from this analysis. Phase 1a path: `iter-02/sources/fuse-energy-not-boring-details.md`.

6. **Fuse Energy Technologies homepage and Wikipedia**, accessed 2026-03-07 — Company overview, TITAN specifications, FAETON neutron source. Phase 1a path: `iter-01/sources/fuse-energy-technology.md`.

7. **Yager-Elorriaga et al., "An overview of magneto-inertial fusion on the Z Machine at Sandia National Laboratories," *Nuclear Fusion* 62, 042015 (2022)** — Comprehensive overview of Z machine MagLIF experimental program; 70+ experiments; record performance χ = 0.084 ± 0.009; magnetic trapping of fusion products demonstrated; simulation-based yield projections for higher-current machines. Cited in dossier.

8. **Gomez et al., "Experimental Demonstration of Fusion-Relevant Conditions in Magnetized Liner Inertial Fusion," *Physical Review Letters* 113, 155003 (2014)** — First experimental demonstration of fusion-relevant conditions in MagLIF. Cited in dossier and handwritten exemplar.

9. **Slutz & Vesey, "High-Gain Magnetized Inertial Fusion," *Physical Review Letters* 108, 025003 (2012)** — Simulation paper showing GJ-class yields are achievable with cryogenic DT ice-layer targets at 60+ MA; defines the pathway from current gas-fill experiments to power-plant-relevant yields. Cited in handwritten exemplar.

10. **Olson et al., "Recyclable transmission line concept for z-pinch driven IFE," Sandia (2003)** — Only published RTL cost estimate ($0.70/shot); conceptual design for rep-rated RTL fabrication and deployment. Cited in handwritten exemplar.

11. **Science for America, "New Opportunities in Fusion Power," White Paper, May 2023** — Catalyzed creation of Pacific Fusion; contributors include Will Regan (Pacific Fusion co-founder/president), reviewed by Keith LeChien (Pacific Fusion CTO/co-founder). Quantifies required capacitor cost reduction (~$5/J → <$0.50/J), lifetime improvement (10⁴ → 10⁹ shots), and efficiency/scale arguments for pulsed magnetic fusion vs. laser ICF. Cited in dossier and handwritten exemplar.

12. **Slutz et al., "Pulsed-power-driven cylindrical liner implosions of laser preheated fuel magnetized with an axial field," *Physics of Plasmas* 17, 056303 (2010)** — Original MagLIF proposal paper. Cited in dossier and handwritten exemplar.

13. **Phase 1a Dossier, MagLIF (D-T), iterations 1–2, 2026-03-07** — Structured research summary with per-column values, confidence ratings, and citations covering confinement family, driver technology, fuel, energy capture, tritium breeding, operational mode, rep rate, and driver technology. Consolidated source for dossier values. Path: `exploration/phase_1a/research/07-maglif/dossier.md`.
