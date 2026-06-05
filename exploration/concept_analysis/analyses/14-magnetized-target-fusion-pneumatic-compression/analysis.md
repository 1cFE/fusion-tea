---
ID: 14-magnetized-target-fusion-pneumatic-compression
Concept: MTF Pneumatic Compression (General Fusion)
Company: General Fusion
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: MIF
Archetype: MAG_TARGET
Archetype-Fit: Med
Comparison-Status: costingfe
Comparables: []
Design-Point-Name: GF MTF Commercial Power Plant — Krotez et al. 2023 SOFE conceptual design (150 MWe per module, two-module architecture)
Design-Point-Maturity: paper-concept
P-Native: 150
Grounding-Confidence: high
---

## Design Point

- Name: GF MTF Commercial Power Plant — Krotez et al. 2023 SOFE conceptual design (150 MWe per module, two-module architecture)
- Maturity: paper-concept
- P_native: 150 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-04/sources/en-wiki-general-fusion/output.md
  - knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-fst-2025-fuel-cycles.md

## Section 1: Availability of Data

**Rating: Moderate**

General Fusion's MTF concept benefits from a peer-reviewed publication on the tritium fuel cycle (Flynn et al., FST 2025, DOI: 10.1080/15361055.2025.2526266) co-authored by Savannah River National Laboratory and General Fusion staff, plus a conceptual power plant design presented at the 30th IEEE SOFE (Krotez et al. 2023). The company has disclosed its system architecture through multiple channels — its website, COMSOL-sponsored technical articles, IAEA FEC 2025 conference abstracts (Hildebrand et al.), and a Wikipedia page with extensive cited references.

The FST 2025 paper is the strongest quantitative source, providing detailed tritium fuel-cycle parameters (burn fraction, fueling efficiency, burn rate, TBR, startup inventories, and processing times) for both lead-lithium eutectic and pure lithium blanket variants. The Krotez 2023 SOFE paper establishes the commercial plant architecture (two 150 MWe modules producing 300 MWe total) but the paper itself is not in the available dossier — only the citation via Wikipedia[^1].

LM26 experimental results are documented through company press releases and the IAEA FEC abstract. Key demonstrated parameters include >10 ms energy confinement time, >400 eV electron temperature (from PI3), and ~6×10¹⁹ m⁻³ plasma density[^2]. In April 2025, General Fusion achieved first integrated plasma compression with lithium in LM26[^3].

**Key data gaps:**
- No published fusion power (MWth), fusion gain Q, or thermal efficiency for the commercial plant
- No capital cost breakdown or LCOE projection from the company
- No detailed piston system design or costing
- The Krotez 2023 SOFE paper is referenced but not directly available in the source corpus — plant parameters are inferred from secondary citations
- No published power conversion cycle parameters (steam temperature, pressure, efficiency)
- No O&M cost breakdown or maintenance schedule

[^1]: en-wiki-general-fusion/output.md §Technology — "the MTF power plant proposed by General Fusion would produce about 300 MWe from two 150 MW machines running in tandem"
[^2]: generalfusion-post-peer-reviewed-publication-confirms/output.md — "approximately 12 milliseconds" confinement, "approximately 6x10^19 m^-3" density, "exceeded 400 eV" temperature
[^3]: general-fusion-lm26-milestones-2025.md — "successfully compressed a large-scale magnetized plasma with lithium"

## Section 2: Challenges in Capturing System Function

The GF MTF concept presents several distinctive LCOE modeling challenges, ranked by impact:

**1. Absence of fusion power and Q values (blocking).** No source in the dossier states the fusion power output, energy gain factor Q, or thermal-to-electric efficiency for the commercial plant. The design point specifies 150 MWe net electric per module, but the fusion power, recirculating power, and thermal balance that produce this output are not published. This forces the 1costingFE model to infer or assume these values.

**2. Pulsed operation economics.** Like all pulsed concepts, the plant's time-averaged power output is the product of per-pulse energy yield × repetition rate. The commercial target is ~1 Hz[^4]. At this rate, achieving 150 MWe net from a single module requires each pulse to deliver sufficient thermal energy (after conversion losses and recirculating power) to sustain continuous electrical output. The piston recharge cycle, liquid metal reset, and vacuum re-establishment must all fit within ~1 second — and none of these have been demonstrated at rate.

> "1 pulse per day repetition rate vs 1 pulse per second for a power plant... this increases the time available to re-establish the high vacuum conditions required for plasma formation by a factor of 86,400, avoiding a significant engineering obstacle"
> — en-wiki-general-fusion/output.md §Fusion Demonstration Program

**3. LM26 is not a prototype of the commercial design.** LM26 uses electromagnetic theta-pinch compression of a solid lithium liner, while the commercial plant uses pneumatic piston compression of a liquid metal liner[^5]. The compression mechanism, liner state (solid vs. liquid), and driver technology differ fundamentally. Extrapolating from LM26 physics results to commercial plant performance introduces substantial uncertainty.

**4. Liquid metal composition undecided.** The FST 2025 paper evaluates both lead-lithium eutectic (LLE) and pure lithium, without selecting one for the commercial plant[^6]. The choice has cascading effects: LLE risks plasma poisoning by high-Z lead contamination during compression; pure lithium has higher tritium retention (>99% of fuel ions gettered by the blanket) requiring different extraction technology at low TRL. The blanket material affects TBR, tritium inventory, pumping power, corrosion management, and extraction system capital cost.

**5. No manufactured consumables — but unproven at rate.** General Fusion claims a structural advantage over laser ICF:

> "the plasma target enables a pulsed system without manufactured consumables"
> — general-fusion-fst-2025-fuel-cycles.md §1 Introduction

Unlike laser ICF targets or MagLIF liners that are destroyed per shot, the liquid metal liner is recycled. However, the liquid metal must reform a stable vortex cavity, re-establish vacuum, and accept a new plasma injection within ~1 second. Whether the liquid metal surface sprays, vaporizes, or contaminates under repetitive GJ-scale fusion pulses is an open question — early experiments showed "the wall of the liquid metal vortex turned to a spray soon after the arrival of the pressure wave"[^7].

**6. O&M cost structure is opaque.** No published maintenance schedule, component replacement intervals, or staffing model exists. The liquid metal loop, piston array, plasma injector, and tritium processing system all have uncharacterized maintenance requirements. Per cross-concept memory: the assessment agent flags missing O&M breakdown in >80% of first-pass analyses. For GF MTF, the piston wear and seal replacement under repetitive high-speed impacts is a unique maintenance cost category with no analogue in other fusion concepts.

[^4]: general-fusion-technical-details.md §Compressing the Timeline — "repeats once per second in a commercial plant"
[^5]: general-fusion-iaea-fec-2025-abstract.md — "LM26 is using an electromagnetic theta-pinch to implode a solid lithium liner... Although the commercial compression solution remains liquid metal"
[^6]: general-fusion-fst-2025-fuel-cycles.md §1 Introduction
[^7]: en-wiki-general-fusion/output.md §History — citing Laberge et al. 2013 SOFE

## Section 3: Maturity of Key Subsystems and Components

Subsystems listed in ascending order of maturity (least mature first).

### Pneumatic piston compression system at ~1 Hz — TRL 2–3

- **On paper only:** Commercial design calls for dozens to hundreds of steam-driven pistons around a spherical vessel, synchronized to within ~2 μs[^8], compressing liquid metal at ~1 Hz. The Krotez 2023 SOFE paper presents the conceptual design.
- **Demonstrated (partial):** A 2013 proof-of-concept used 14 full-size pistons around a 1 m diameter sphere, achieving synchronized impacts with 100 kg, 30 cm diameter hammers at 50 m/s[^9]. Over 1,000 compression shots on a 1:10 scale water system demonstrated cavity collapse shaping[^10]. Piston-compression technology is being co-developed with "a major automaker"[^11].
- **Missing at scale:** Full-scale (~4 m cavity), liquid-metal, ~1 Hz repetitive compression with vacuum re-establishment between pulses. No integrated piston-plus-liquid-metal compression test at commercial parameters exists.

### Liquid metal vortex formation and reset at ~1 Hz — TRL 2–3

- **On paper only:** The liquid metal is pumped tangentially at the equator, exits radially at the poles, creating a stable vertical cavity[^12]. Between pulses the vortex must reform within ~1 second.
- **Demonstrated (partial):** Scaled water experiments showed cavity reformation at broadly compatible timescales. Shape-controlled compression of rotating liquid liners was demonstrated with pneumatic pistons (Mangione et al. 2024, FED).
- **Missing at scale:** Reformation under GJ-scale blast loading, with activated debris, at ~4 m diameter, at 1 Hz. The spray problem noted in 2013 experiments is not confirmed resolved.

### Tritium fuel cycle and extraction — TRL 3–4

- **Demonstrated:** SRNL modeled the complete fuel cycle for both LLE and Li blankets (FST 2025). Processing technologies include palladium diffusers, cryogenic distillation, CECE, and gas liquid contactors — these exist at laboratory scale.
- **On paper only (for Li):** Direct LiT Electrolysis for pure lithium blanket extraction. The FST paper states: "the process is in its infancy and will require more research to determine to what level of throughput it can handle"[^13].
- **Missing at scale:** Blanket extraction at 2 m³/s lithium throughput (requiring 314 centrifugal contactors for the Maroni process alternative[^14]), closed-loop tritium self-sufficiency at kg/day rates.

### Plasma injector (Marshall gun / compact toroid) — TRL 4–5

- **Demonstrated:** PI3 injector achieved 10 ms energy confinement times and 250 eV temperatures (2022)[^15]. SPECTOR generation achieved >400 eV and 2 ms lifespans[^16]. Over 200,000 plasma shots fired across multiple injector generations. Performance improved with lithium wall coating.
- **Missing at scale:** Consistent injection into a liquid metal cavity at ~1 Hz with sufficient confinement time (>5 ms compression timescale) and magnetic field quality for fusion.

### Electromagnetic compression (LM26 surrogate) — TRL 4

- **Demonstrated:** LM26 achieved first plasma compression with lithium in April 2025. Ion temperature and density increases observed during compression[^17]. Pre-compression targets: 1 keV → 10 keV → scientific breakeven equivalent.
- **Missing at scale:** LM26 is 50% commercial plasma scale and uses a fundamentally different compression method (EM theta-pinch of solid lithium vs. pneumatic pistons on liquid metal).

### Energy conversion / BOP — TRL 6–8

- **Demonstrated:** Steam Rankine cycle is mature commercial technology. General Fusion's concept uses heated liquid metal → heat exchanger → steam → turbine, with steam partially recycled to power pistons[^18].
- **Missing at scale:** Coupling to a pulsed thermal source at ~1 Hz, thermal buffering between pulses, liquid-metal-to-steam heat exchangers at fusion temperature with tritium permeation barriers. Partnership with Hatch for power-plant engineering and Kyoto Fusioneering for balance-of-plant[^19].

[^8]: en-wiki-general-fusion/output.md §Technology — "timing of these strikes had to be controlled to within 10 μs... synchronized within 2 μs"
[^9]: en-wiki-general-fusion/output.md §History
[^10]: globenewswire press release 2022 — "over 1,000 shots, behaving as predicted"
[^11]: generalfusion-fusion-demo-plant/output.md — "a major automaker on piston-compression technology development"
[^12]: en-wiki-general-fusion/output.md §Technology
[^13]: general-fusion-fst-2025-fuel-cycles.md §3 Results (Li discussion)
[^14]: general-fusion-fst-2025-fuel-cycles.md §3 Results — "314 units to handle the full throughput of 2 m³/s of Li"
[^15]: en-wiki-general-fusion/output.md §History — "PI3 reached 10 ms confinement times and temperatures of 250 eV"
[^16]: en-wiki-general-fusion/output.md §History — "SPECTOR lifespans of up to 2 milliseconds and temperatures in excess of 400 eV"
[^17]: metaltechnews-story-2025-05-14/output.md — "early diagnostics showed increases in ion temperature and density"
[^18]: en-wiki-general-fusion/output.md §Technology — "liquid metal... pumped through a heat exchanger to generate electricity via a steam turbine... Some of the steam is recycled to power the pistons"
[^19]: generalfusion-fusion-demo-plant/output.md §Commercialization

## Section 4: Key Materials and Supply Chain Considerations

### Liquid metal (lithium or lead-lithium eutectic)

The blanket/liner material is the single largest material requirement. The ~4 m diameter cavity with 1.5 m blanket thickness at 4π coverage implies hundreds of cubic meters of liquid metal in continuous circulation. The material choice remains undecided:

- **Lead-lithium eutectic (LLE):** More extensively studied, lower melting point, favorable neutronics, low tritium solubility. However, its higher density increases pumping costs, and lead contamination of the plasma during compression is a potentially disqualifying risk: "can poison the plasma as a high Z contaminant, which may seriously impact the GF MTF approach since the liquid metal first wall will be used to compress the plasma"[^20]. Lead supply is ample globally.
- **Pure lithium:** Higher TBR potential (1.25–1.80 vs. 1.40 for LLE), no high-Z plasma contamination risk. However, higher reactivity, significant tritium retention (>99% of fuel ions), and less-developed extraction technology. Lithium supply competes with the rapidly growing battery industry, though lithium metal for fusion uses natural lithium (a mix of Li-6 and Li-7), not the lithium carbonate/hydroxide the battery industry primarily consumes.

### Tritium

Startup inventory requirements are modest by fusion standards: 0.317 kg for LLE or 0.747 kg for Li (with 20% contingency)[^21]. At ~$30,000/g, this represents ~$9.5M–$22.4M — significantly less than tokamak designs (ARC: 0.3–1.5 kg; DEMO: 4–10 kg). The GF MTF plant doubling time of 56–67 days is dramatically shorter than ARC (730 days) or DEMO (1,825 days)[^22], implying rapid fleet deployment potential once the first plant operates.

The global civilian tritium inventory is ~25 kg and shrinking as CANDU reactors retire. GF's low startup requirement and fast doubling time are genuine supply-chain advantages.

### Piston and mechanical components

The piston array is GF's distinctive engineering subsystem. The 2013 proof-of-concept used 100 kg, 30 cm diameter hammer pistons driven by compressed air[^23]. The commercial design uses steam-driven pistons. Key materials are conventional industrial steel and alloys. The partnership with "a major automaker" suggests that automotive-scale manufacturing and precision is considered applicable. Seal technology — isolating pistons from hot liquid metal under repetitive impacts — was a recognized challenge, leading to a $20,000 crowdsourced innovation challenge[^24].

### No exotic materials required

Unlike tokamak and stellarator concepts, GF MTF requires no REBCO HTS tape, no large superconducting magnets, no tungsten divertor tiles, and no beryllium first wall. The plasma is self-confined (compact toroid with internal currents), the driver is mechanical, and the blanket/shield/first-wall is liquid metal. This is a structural supply-chain advantage: the concept's critical materials are commodity industrial metals and lithium/lead.

### Tritium processing equipment

Palladium diffusers, cryogenic distillation columns, and heat exchangers are required for the tritium fuel cycle. For the Li blanket option, 314 centrifugal contactors (25 cm × 45 cm each, 3.7 kW continuous draw) are needed for the Maroni extraction process, drawing ~1.2 MW parasitic power[^25]. These are specialized but not exotic items.

[^20]: general-fusion-fst-2025-fuel-cycles.md §1 Introduction
[^21]: general-fusion-fst-2025-fuel-cycles.md §3 Results, Table 3
[^22]: general-fusion-fst-2025-fuel-cycles.md §3 Results, Table 3 — GF LLE: 56 days, GF Li: 67 days, ARC: 730 days, DEMO: 1825 days
[^23]: en-wiki-general-fusion/output.md §History
[^24]: en-wiki-general-fusion/output.md §Crowdsourced innovations — "$20,000 prize" for robust seal technology
[^25]: general-fusion-fst-2025-fuel-cycles.md §3 Results — "314 units... 3.7 kW of power during continuous operation"

## Section 5: Design Point Parameters

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 150 MWe | en-wiki-general-fusion/output.md §Technology — "300 MWe from two 150 MW machines running in tandem"; Krotez et al. 2023 SOFE | high | Per module. spec key: `net_electric_MWe` |
| Cavity diameter (pre-compression) | ~4 m | general-fusion-fst-2025-fuel-cycles.md §Abstract — "large (~4 m diameter) cavity formed in liquid metal" | high | This is the uncompressed cavity diameter, analogous to chamber radius |
| Blanket thickness | 1.5 m | general-fusion-fst-2025-fuel-cycles.md §1 Introduction — "1.5 m thick liquid metal blanket with 4π coverage" | high | Liquid metal blanket/shield/first-wall combined |
| Volumetric compression ratio | 350× | general-fusion-fst-2025-fuel-cycles.md §1 Introduction — "350-fold volumetric compression would achieve the Lawson criterion and ignition" | medium | Target, not demonstrated |
| Repetition rate | ~1 Hz | general-fusion-technical-details.md §Introduction — "repeats once per second in a commercial plant"; en-wiki-general-fusion/output.md §FDP | high | spec key: `rep_rate` |
| Fuel | D-T | general-fusion-fst-2025-fuel-cycles.md §Abstract — "spherical torus of deuterium-tritium plasma" | high | |
| Plasma type | Compact toroid (spherical torus) | en-wiki-general-fusion/output.md §Technology | high | Formed by coaxial Marshall gun |
| Pre-compression T_e | >400 eV | generalfusion-post-peer-reviewed-publication-confirms/output.md — "exceeded 400 eV" | high | Demonstrated on PI3; target is 10 keV post-compression |
| Pre-compression n_e | ~6×10¹⁹ m⁻³ | generalfusion-post-peer-reviewed-publication-confirms/output.md — "approximately 6x10^19 m^-3" | high | Demonstrated on PI3 |
| Pre-compression τ_E | ~12 ms | generalfusion-post-peer-reviewed-publication-confirms/output.md — "approximately 12 milliseconds" | high | Demonstrated on PI3 |
| Compression timescale | ~5 ms | globenewswire-2022 press release — "a shaped collapse in a liquid metal cavity within approximately five milliseconds" | medium | At 1:10 scale in water |
| Post-compression T_i target | 10 keV | general-fusion-iaea-fec-2025-abstract.md — "over 100 million degrees Celsius (10 keV)" | medium | LM26 target, extrapolated to commercial |
| Lawson nTτ target | >10²¹ m⁻³ keV s | general-fusion-iaea-fec-2025-abstract.md — "nTtau exceeds 1e21 m^-3 keV s" | medium | LM26/2026 target |
| fusion_power_MW | Unknown | No data found in available sources | — | Not published; library back-solves from p_input + P_native |
| Q (fusion gain) | Unknown | No data found in available sources | — | Not published anywhere in the dossier |
| p_input_MW | Unknown | No data found in available sources | — | Piston drive energy + plasma injector + liquid metal pumping; not published. spec key: `p_input` |
| Thermal efficiency (η_th) | [estimated] ~33% | No company data; standard steam Rankine assumed | low | No published cycle parameters; 33% is conservative for steam Rankine without reheat. spec key: `eta_th` |
| Energy capture | Thermal (steam Rankine) | general-fusion-technical-details.md §Introduction — "heat exchanger to create steam and ultimately produce electricity"; en-wiki-general-fusion/output.md §Technology | high | Some steam recycled to power pistons |
| Blanket material | LLE or Li (undecided) | general-fusion-fst-2025-fuel-cycles.md §1 — both candidates under evaluation | medium | Choice affects TBR, tritium inventory, and extraction system |
| TBR | 1.25–1.80 (Li) or 1.40 (LLE) | general-fusion-fst-2025-fuel-cycles.md §2, Table 2 | high | |
| Burn fraction (β) | 0.0163 (LLE) / 0.0206 (Li) | general-fusion-fst-2025-fuel-cycles.md §2, Table 2 | high | |
| Fueling efficiency (η_fuel) | 0.25 | general-fusion-fst-2025-fuel-cycles.md §2, Table 2 | high | |
| Tritium burn rate | 77 g/day (LLE) / 96 g/day (Li) | general-fusion-fst-2025-fuel-cycles.md §2, Table 2 | high | |
| Startup T inventory | 0.317 kg (LLE) / 0.747 kg (Li) | general-fusion-fst-2025-fuel-cycles.md §3, Table 3 | high | With 20% contingency |
| Plant doubling time | 56 days (LLE) / 67 days (Li) | general-fusion-fst-2025-fuel-cycles.md §3, Table 3 | high | |
| B (on-axis, pre-compression) | ~0.5–1 T | [inferred from compact toroid physics: self-generated field from plasma currents, not external coils] | low | No published value; compact toroids at these densities typically carry 0.1–1 T internal fields. spec key: `B` |
| B (post-compression) | ~200 T | dossier §Primary Heating — "magnetic field 2 to 200 T" from APS 2018 overview | medium | At peak compression; 350× volumetric compression from ~0.5 T yields ~175 T (B scales as V^(-2/3)) |
| Sphere diameter | ~3 m | en-wiki-general-fusion/output.md §Technology — "a ~3 meter sphere filled with liquid metal" | medium | May differ from the 4 m cavity diameter cited in FST 2025 — the sphere is the outer vessel, the cavity is the inner void |
| Magnet type | None | Schema: self-confined compact toroid | high | No external confinement magnets |

**Note on missing spec keys:** The critical parameters `p_input`, `B`, and `eta_th` are not directly published for this design point. The `p_input` is the sum of piston drive power (steam), plasma injector electrical power, and liquid metal pumping — none are quantified in available sources. The model-setup agent will need to work with the library defaults or derive values from the compression energy budget.

## Section 5b: Override Candidates

The per-account walkthrough below considers each canonical 1costingFE account for the MIF archetype. The archetype-fit grade is Med, expecting 3–8 enabled overrides.

**C220101 — First wall, blanket & neutron multiplier:** The GF MTF design replaces a solid first wall and structured blanket with a flowing liquid metal that serves as liner, blanket, breeder, and shield simultaneously. The 1.5 m thick, 4π-coverage liquid metal provides "excellent neutron shielding for all structural components"[^26] and eliminates the need for a separate first wall structure. This is a fundamental departure from the library default (which prices a solid breeding blanket). The dossier does not publish a dollar figure for the liquid metal inventory or loop capital cost, but the architecture eliminates the solid blanket structure entirely. Propose override as a fraction of the library default to reflect the elimination of solid blanket fabrication and the substitution of a simpler liquid metal loop.

**C220102 — Radiation shield:** The 1.5 m liquid metal blanket at 4π coverage is the radiation shield. No separate shielding structure is needed beyond the liquid metal containment vessel. The library default prices a separate shield structure; this concept eliminates it. However, no company cost figure is available — the override would be derived from the structural simplification.

**C220103 — Confinement magnets / coils:** The GF MTF concept uses **no external confinement magnets**. The plasma is a self-confined compact toroid; compression is mechanical. This account should be zero.

**C220104 — Primary pulsed driver:** The pneumatic piston array is the primary driver. General Fusion explicitly positions this as "low-cost" relative to lasers and superconducting magnets: "Pistons are unique to General Fusion's approach, as other fusion methods rely on superconducting coils, lasers, or other expensive equipment"[^27]. However, no dollar figure or $/J cost for the piston system is published. The Fusion Demonstration Plant (70% scale, non-power-producing) had a reported cost of US$400M total[^28], but this is for the entire demo facility, not the driver subsystem alone. No override can be grounded to a company-published driver cost.

**C220105 — Primary structure:** No company data for structural cost. Library default stands.

**C220106 — Vacuum system:** The concept requires re-establishing high vacuum within ~1 second between pulses. The Wikipedia article notes this is "a significant engineering obstacle that will need to be solved"[^29]. No company cost figure. Library default stands.

**C220107 — Power supplies / pulsed-power bank:** The piston compression is steam-driven (mechanical), not electrically driven. The capacitor bank for the plasma injector (Marshall gun) is needed but is a relatively small subsystem. No published cost. The library default for a $/J pulsed-power bank likely overestimates this account, since the main driver energy comes from steam, not electrical pulsed power.

**C220108 — Target factory (IFE/MIF target manufacturing):** General Fusion explicitly claims "a pulsed system without manufactured consumables"[^30]. The liquid metal liner is recycled, not destroyed per shot. There is no target factory. This account should be near zero — perhaps a small allocation for plasma injector consumables (a few milligrams of D-T gas per pulse, capacitor bank maintenance). This is a major cost advantage relative to the library default for MIF targets.

**C220109 — Direct energy converter:** Not applicable. The design uses thermal (steam Rankine) conversion, not direct energy conversion. No override needed — the library default correctly zeroes this for thermal-conversion concepts.

**C220110 — Remote handling & maintenance:** No company data. Library default stands.

**C220111 — Installation & assembly:** No company data. Library default stands.

**CAS21 — Buildings & site:** No company data. Library default stands.

**CAS23 — Turbine plant equipment:** Standard steam Rankine cycle. No company data suggesting departure from library default.

**CAS24 — Electric plant equipment:** No company data. Library default stands.

**CAS26 — Heat rejection system:** No company data. Library default stands.

**CAS27 — Special materials (initial fill):** The liquid metal inventory for a ~4 m cavity with 1.5 m blanket at 4π coverage is substantial. For a sphere of ~3.5 m outer radius (2 m cavity radius + 1.5 m blanket), the liquid metal volume is approximately (4/3)π(3.5³ - 2³) ≈ 146 m³. Lithium density is ~512 kg/m³ at operating temperature; this implies ~75 tonnes of lithium. At current lithium metal prices (~$20–40/kg depending on grade), the initial lithium fill would cost ~$1.5–3M. For LLE (PbLi at ~9,400 kg/m³), the mass is ~1,370 tonnes at ~$5–15/kg → ~$7–20M. These are rough estimates but both are modest relative to overall plant capital. No company figure is published for the initial fill cost.

**CAS70 — O&M:** No published O&M breakdown. The unique maintenance items are piston seal replacement, liquid metal loop maintenance, plasma injector refurbishment, and tritium processing system upkeep. Library default stands.

**CAS80 — Fuel cost:** Tritium startup inventory of 0.317–0.747 kg is a one-time cost amortized over plant life. Annual deuterium procurement is negligible. The library default likely handles this adequately.

```yaml
overrides:
  - account: C220103
    value: 0.0
    enabled: true
    provenance: direct
    source: "en-wiki-general-fusion/output.md §Technology"
    rationale: |
      GF MTF uses no external confinement magnets. The plasma is a self-confined compact toroid
      with magnetic fields sustained by internal plasma currents. Compression is mechanical
      (pneumatic pistons), not magnetic. The library default prices HTS-REBCO magnets; this
      concept has zero magnet cost.

  - account: C220108
    value: 0.0
    enabled: true
    provenance: direct
    source: "general-fusion-fst-2025-fuel-cycles.md §1 Introduction"
    rationale: |
      GF MTF explicitly has "a pulsed system without manufactured consumables." The liquid metal
      liner is recycled, not destroyed per shot. There is no target factory. Unlike laser ICF
      (hohlraum/capsule) or MagLIF (liner + RTL), GF MTF has zero per-shot consumable hardware.
      A few milligrams of D-T gas per pulse is the only consumable, covered by CAS80.

  - account: C220104
    value: 0.15 * generic.costs.c220104
    enabled: true
    provenance: derived
    source: "general-fusion-technical-details.md §LM26 section; en-wiki-general-fusion/output.md §Technology"
    rationale: |
      The primary driver is a pneumatic piston array — steam-driven mechanical hammers around
      a sphere. GF positions this as fundamentally cheaper than lasers or pulsed-power drivers:
      "other fusion methods rely on superconducting coils, lasers, or other expensive equipment."
      No dollar figure is published, but the piston system uses commodity industrial components
      (steel hammers, pneumatic cylinders, steam valves, digital servo controls). The library
      default for C220104 prices a laser or pulsed-power driver at $/J; pneumatic pistons are
      qualitatively a fraction of this. 15% of the library default is an aggressive but
      directionally correct estimate given the architectural simplification. The exact fraction
      is highly uncertain.

  - account: C220107
    value: 0.10 * generic.costs.c220107
    enabled: true
    provenance: derived
    source: "en-wiki-general-fusion/output.md §Technology"
    rationale: |
      The library default for C220107 prices a pulsed-power capacitor bank ($/J stored) as the
      dominant driver cost for electrically-driven pulsed schemes. GF MTF is mechanically driven —
      the main compression energy comes from steam pistons, not electrical pulsed power. The only
      electrical pulsed system is the plasma injector capacitor bank (ionizes a few mg of gas via
      Marshall gun). This is a small fraction of the pulsed-power cost assumed for electrically
      driven concepts. 10% of the library default reflects that only the injector subsystem draws
      from this account.

  - account: C220101
    value: 0.40 * generic.costs.c220101
    enabled: true
    provenance: derived
    source: "general-fusion-fst-2025-fuel-cycles.md §1 Introduction"
    rationale: |
      The GF MTF design replaces a solid structured breeding blanket with a flowing liquid metal
      that serves as liner, blanket, breeder, and shield. No solid first wall, no solid blanket
      modules, no neutron multiplier structure. The library default prices solid blanket fabrication
      (e.g., HCPB or liquid metal channels in a structured module). The GF approach needs only a
      liquid metal containment vessel and pumping infrastructure, which is structurally simpler.
      40% of library default reflects the remaining cost of the containment vessel, liquid metal
      piping, and pump systems, while removing the solid blanket/FW fabrication premium.

  - account: CAS27
    value: 3.0
    enabled: true
    provenance: derived
    source: "general-fusion-fst-2025-fuel-cycles.md §1 Introduction; en-wiki-general-fusion/output.md §Technology"
    rationale: |
      Initial liquid metal fill for a ~3.5 m outer radius sphere (2 m cavity + 1.5 m blanket)
      ≈ 146 m³. For pure lithium at ~512 kg/m³ = ~75 tonnes at ~$30/kg ≈ $2.25M. For LLE at
      ~9400 kg/m³ = ~1370 tonnes at ~$10/kg ≈ $13.7M. Taking the lithium case (which appears
      to be the leading candidate given plasma contamination concerns with LLE), $3M is a
      reasonable estimate including procurement and initial charging. $3M = 3.0 in $M units.
      This is likely lower than the library default for special materials which may price
      exotic blanket fills.
```

**Override count: 6 enabled.** This falls within the expected 3–8 band for Med archetype-fit.

[^26]: general-fusion-fst-2025-fuel-cycles.md §1 Introduction
[^27]: general-fusion-technical-details.md §LM26 Relies on Electromagnetic Compression
[^28]: en-wiki-general-fusion/output.md §Fusion Demonstration Program — "reported cost of US$400 million"
[^29]: en-wiki-general-fusion/output.md §Fusion Demonstration Program
[^30]: general-fusion-fst-2025-fuel-cycles.md §1 Introduction

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Fusion power (MWth) and energy gain Q not published for commercial plant | S5 | truly-unknown | blocking | Krotez et al. 2023 SOFE paper (not in corpus); contact General Fusion |
| 2 | Thermal efficiency (η_th) not published; steam cycle parameters unknown | S5 | not-yet-sourced | blocking | CNL/Hatch BOP integration study (announced April 2024) |
| 3 | Recirculating power (p_input) not published — piston drive, pumping, injector | S5 | truly-unknown | blocking | No known source; critical for net electric derivation |
| 4 | Piston system capital cost ($/unit, number of pistons, total driver cost) | S5b | proprietary | important | GF/automaker partnership deliverables; Krotez 2023 SOFE |
| 5 | Liquid metal composition not selected (LLE vs. Li) — affects TBR, tritium inventory, extraction system, and plasma contamination risk | S2, S4 | truly-unknown | important | General Fusion internal trade study in progress |
| 6 | O&M cost breakdown — piston wear, seal replacement, liquid metal loop maintenance, tritium system upkeep | S2 | not-yet-sourced | important | No known public source |
| 7 | Vacuum re-establishment time at ~1 Hz between pulses | S2, S3 | truly-unknown | important | No demonstration; ~86,400× gap between LM26 (1/day) and commercial (1/sec) |
| 8 | Liquid metal vortex reformation and stability under repetitive GJ-scale pulses | S3 | truly-unknown | important | Mangione et al. 2024 provides partial data at subscale with water |
| 9 | LM26-to-commercial extrapolation basis (solid Li EM compression → liquid metal pneumatic compression) | S2, S3 | derivable | important | Krotez 2023 SOFE; GF internal scaling analysis |
| 10 | Post-compression plasma parameters (achieved T_i, n_e, τ_E at compression) | S3 | truly-unknown | important | LM26 ongoing experiments; IAEA FEC 2025 results |
| 11 | Heat exchanger design for liquid-metal-to-steam transfer with tritium permeation barriers | S3 | not-yet-sourced | nice-to-have | Kyoto Fusioneering collaboration |
| 12 | FDP (70% scale UK plant) status and lessons learned — currently on hold | S3 | proprietary | nice-to-have | General Fusion corporate updates |

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

**Contextual positioning within the MIF family:** General Fusion's pneumatic MTF occupies a unique position among magneto-inertial fusion concepts:

- **vs. MagLIF / Pacific Fusion (pulsed power MIF):** MagLIF uses pulsed electrical power (capacitor banks at tens of MA) to implode a solid metal liner, which is destroyed every shot. GF MTF uses mechanical (pneumatic) compression of a recycled liquid metal liner — no per-shot consumable hardware. This eliminates the target factory (C220108) and recyclable transmission line costs that dominate MagLIF operating costs. However, GF MTF faces the unique engineering challenge of reforming the liquid metal vortex at ~1 Hz, which MagLIF avoids (fresh liner each shot).

- **vs. NearStar (plasma railgun MIF):** NearStar uses plasma armature railguns to compress magnetized targets — also destroying targets per shot. GF MTF's liquid metal recycling is a structural advantage, but NearStar's approach allows higher compression velocities.

- **vs. Helion (pulsed FRC compression):** Helion uses capacitor-bank-driven magnetic compression of colliding FRCs, targeting D-He3 fuel and direct inductive energy recovery. GF MTF uses D-T fuel with conventional steam Rankine conversion. Helion avoids the tritium fuel cycle entirely (at the cost of much harder plasma physics); GF MTF embraces D-T but gains the liquid metal's triple function (blanket/shield/breeder).

The key architectural differentiator is the liquid metal liner: it is the only pulsed fusion concept in the landscape where the compression medium is recycled rather than destroyed per shot. This eliminates the target factory cost account but creates the unique challenges of liquid metal vortex management, vacuum re-establishment, and seal/piston maintenance at ~1 Hz.

## Section 8: Sources

1. **Flynn, H.B., Larsen, G.K., Rowell, A.P., and Skrecky, K. (2025).** "Comparison of Fuel Cycles for Lead-Lithium and Pure Lithium Liquid Metal Walls in a Magnetized Target Fusion Power Plant." *Fusion Science and Technology*. DOI: 10.1080/15361055.2025.2526266. — The richest quantitative source: tritium fuel cycle parameters, blanket material trade study, startup inventories, plant doubling times, comparison to ARC/ITER/DEMO. Path: `iter-02/sources/general-fusion-fst-2025-fuel-cycles.md`

2. **Wikipedia: General Fusion.** Comprehensive secondary source with cited references to primary publications. Provides commercial plant architecture (2×150 MWe), LM26 design, challenges list, funding history, and research collaborations. Contains the Krotez 2023 SOFE citation. Path: `iter-04/sources/en-wiki-general-fusion/output.md`

3. **COMSOL News (July 2025): "Compressing the Timeline to a Fusion Future."** Technical article on LM26 simulation and validation with Veryst Engineering. Provides compression physics details, lithium material characterization, and the 1 Hz commercial rep rate. Path: `iter-01/sources/general-fusion-technical-details.md`

4. **Hildebrand, M. et al. (2025).** IAEA FEC 2025 Abstract: LM26 MTF experimental results. Provides LM26 scale (50% commercial), temperature targets (10 keV), and Lawson criterion target (nTτ > 10²¹ m⁻³ keV s). Path: `iter-02/sources/general-fusion-iaea-fec-2025-abstract.md`

5. **General Fusion (2025): "Peer-Reviewed Publication Confirms Plasma Energy Confinement Time for LM26."** Reports >10 ms confinement, >400 eV temperature, ~6×10¹⁹ m⁻³ density on PI3 injector, and the 300 MWe (2×150 MWe) commercial target. Path: `iter-03/sources/generalfusion-post-peer-reviewed-publication-confirms/output.md`

6. **General Fusion: "Commercialization Path."** Outlines the Lawson Program, FOAK target, and partnerships (Hatch, Kyoto Fusioneering, automaker). Path: `iter-03/sources/generalfusion-fusion-demo-plant/output.md`

7. **GlobeNewsWire (Dec 2022): "General Fusion Exceeds Core Technology Performance Targets."** Reports 10 ms confinement, 250 eV temperature, 200,000+ plasma shots, 1,000+ compression shots at 1:10 scale, and 5 ms compression time. Path: `iter-04/sources/globenewswire-news-release-2022-12-12/output.md`

8. **Metal Tech News (May 2025): "General Fusion Compresses Plasma with Lithium."** Reports the April 2025 first integrated compression in LM26 with early diagnostic results. Path: `iter-03/sources/metaltechnews-story-2025-05-14/output.md`

9. **General Fusion (April 2025): "LM26 Achieves First Plasma Compression."** Press release confirming the April 2025 milestone. Path: `iter-02/sources/general-fusion-lm26-milestones-2025.md`

10. **General Fusion Technology Page.** Marketing overview with minimal quantitative content. Path: `iter-01/sources/general-fusion-technology-overview.md`

11. **Krotez, D., Segas, R., Khalzov, I., and Suponitsky, V. (July 2023).** "Conceptual Design of a Magnetized Target Fusion Power Plant." 30th IEEE Symposium on Fusion Engineering (SOFE), E-267. — Primary design-point reference (not directly in corpus; cited via Wikipedia). Establishes the 2×150 MWe commercial architecture.
