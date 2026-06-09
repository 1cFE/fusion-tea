---
ID: 17b-laser-icf-fast-ignition
Concept: Laser ICF Fast Ignition (Focused Energy)
Company: Focused Energy
Status: draft
Created: 2026-06-08
Approved-Date:
Confinement-Family: IFE
Archetype: LASER_IFE
Archetype-Fit: Med
Comparison-Status: freeform-deferred
Comparables:
  - 26-laser-icf-indirect-drive
  - 30-laser-icf-nif-commercialization
  - 31-laser-icf-oec-architecture
  - 32-laser-icf-french-national
  - 17a-laser-icf-hybrid-drive
---

## Design Point

(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)

## 1. Availability of Data

**Rating: Limited**

Focused Energy's proton fast ignition approach has a narrow public data footprint. The company has published high-level technology descriptions on their website and through interviews, but quantitative plant parameters, detailed subsystem specifications, and cost structures remain undisclosed. The most substantive public sources are:

- **Company technology page** (focused-energy-technology.md) — confirms D-T fuel, direct-drive proton fast ignition architecture, and the Pearl™ capsule branding, but provides minimal quantitative detail beyond a claimed 30× output increase relative to NIF indirect drive.
- **Callahan Physics World interview** (focused-energy-callahan-interview.md, 2024) — the most detailed single source, confirming ~10 Hz repetition rate, target gain targets of 50–100, laser efficiency goal of ~10%, lithium blanket tritium breeding with Savannah River National Lab collaboration, conventional steam cycle, and pilot plant timeline (LightHouse by end of 2030s). This interview is the primary anchor for most LCOE-relevant parameters.
- **LaserFocusWorld 2021** — describes the two-pulse architecture (compression + 150 kJ short-pulse ignitor producing proton beam), cites Texas Petawatt heritage and Ditmire's National Energetics ELI Beamlines background, and projects "around 80 beamlines" as an ultimate facility scale (Ditmire's estimate, not a committed design).
- **PRNewswire 2024** — announces $40M Amplitude DPSSL partnership and $65M Laser Development Facility in the San Francisco Bay Area, confirming diode-pumped solid-state laser as the compression driver.

**Key gaps:**

1. **No published power plant study.** Unlike indirect-drive IFE (where NIF's LIFE program and LLNL's generalized economics model provide reference points) or hybrid-drive laser concepts (Xcimer's whitepaper with TRUMPF), Focused Energy has not released system-level cost breakdowns, thermal power targets, or chamber-level engineering details.
2. **Blanket chemistry undisclosed.** "Lithium blankets" are confirmed (Callahan interview), but the specific composition (FLiBe vs LiPb vs liquid Li) and chamber architecture are not public. The Focused Energy J. Fusion Energy 2023 paper (Springer paywall) is cited in external references but has not been ingested into this corpus.
3. **Quantitative plant parameters sparse.** No net electric output, thermal power, or net efficiency figures. The company describes "gigawatt-scale" ambitions without specifics.
4. **Proton fast ignition validation gap.** The concept relies on petawatt-driven proton beam coupling to compressed core; not yet experimentally demonstrated at ignition-relevant scale. Academic fast-ignition literature (Tabak et al., Norreys HiPER studies) provides physics context but not Focused Energy-specific validation data.
5. **Target manufacturing cost.** The Pearl™ cone-in-shell geometry is described as "structurally more complex than a symmetric D-T capsule" (analyst-patch-target-unit-cost.md), but Focused Energy has not disclosed per-target fabrication costs. The analyst patch estimates $0.80/shot (uncertainty band $0.50–$1.20) based on NOAK assumptions and a 1.3× complexity multiplier over symmetric capsules.

**Comparison to IFE neighbors:** Indirect-drive concepts (Inertia's NIF-heritage Thunderwall architecture) and hybrid-drive concepts (Xcimer's HDD approach) have published more detailed cost and performance projections. Focused Energy's opacity places it closer to the "Limited" data tier than "Moderate."

## 2. Challenges in Capturing System Function

Laser ICF fast ignition introduces modeling challenges distinct from both indirect-drive IFE and magnetic confinement concepts:

**1. Two-pulse compression + ignition architecture creates subsystem interdependencies with no validated cost analogue.**

Fast ignition decouples compression (long-pulse DPSSL driver) from ignition (short-pulse petawatt-class laser generating proton beam). This creates two distinct driver cost categories:
- Compression laser: DPSSL beamlines (Nd:glass, frequency-doubled to ~527 nm, ~10% wall-plug efficiency). The Amplitude partnership and Laser Development Facility investment suggest this is the primary capital cost driver, but no per-beamline or total driver cost has been published.
- Ignition laser: ~150 kJ short-pulse (LaserFocusWorld), petawatt-class, chirped-pulse amplification architecture. The number of ignitor beamlines, their unit cost, and maintenance requirements are not disclosed.

The two-pulse approach theoretically reduces required compression energy relative to single-pulse direct drive (enabling smaller per-shot yield + higher rep-rate operation), but whether this translates to lower driver capital cost depends on the relative costs of many DPSSL beamlines vs. fewer but more complex petawatt systems. No public cost comparison exists.

**2. Target gain pathway relies on proton beam coupling physics not yet validated at scale.**

> "To make inertial fusion energy successful and use it in a power plant, we need significantly higher gains of more like 50 to 100."
> — Callahan interview

NIF's best indirect-drive shot achieved target gain ~4.1 (Callahan interview). Focused Energy's 50–100 target gain projection for direct-drive proton fast ignition rests on:
- Compression stage achieving symmetric implosion of a cryogenic D-T capsule (direct-drive geometry).
- Ignitor pulse hitting a "nearby target" (LaserFocusWorld) to generate a proton beam.
- Proton beam coupling efficiently to the compressed core to ignite the fuel.

The third step — proton beam ignition — is the novel physics element. Academic fast-ignition studies (Tabak 1994, Norreys HiPER 2007–2012) provide simulation-based confidence, but no experiment has demonstrated proton-driven ignition at fusion-relevant densities. This is a higher physics risk than indirect drive (where NIF validated the hohlraum → X-ray → capsule → ignition chain) or hybrid drive (where Xcimer's two-beam symmetric implosion is an incremental step from NIF's validated indirect-drive platform).

**3. High repetition rate (10 Hz) drives chamber clearing and target injection challenges shared with other high-rep-rate IFE concepts, but with cone-in-shell target complexity.**

> "While NIF does 400 shots per year, we will need to do about 900,000 shots a day – about 10 per second. We'll also have to efficiently remove the exploded target material from the reactor chamber so that it can be cleared for the next shot."
> — Callahan interview, §"How do you develop the capsule"

At 10 Hz, the chamber must clear debris, re-establish vacuum, inject a new target, and align compression + ignition optics within ~100 ms. The cone-in-shell geometry (required for proton fast ignition — the cone guides the ignitor beam to the compressed core) adds target complexity:
- Cone alignment relative to both compression beams and ignitor beam is more stringent than symmetric capsule alignment.
- Cone fabrication and cryogenic handling (if ice-layer targets are required for high gain) add manufacturing steps.
- Debris from the cone material (typically gold or high-Z metal in academic designs) adds to chamber contamination between shots.

**4. Laser optics survivability under 10 Hz operation.**

Each fusion pulse exposes final optics to X-rays, debris, and neutrons. At 10 Hz over 30 years, final optics see ~9 × 10⁹ shots. Optics degradation, protective schemes (grazing-incidence mirrors, debris shields), and replacement intervals are critical cost drivers for all laser IFE, but fast ignition's two-beam architecture doubles the number of beam paths that must be protected. No published optics lifetime estimate exists for Focused Energy's configuration.

**5. Tritium breeding sufficiency without disclosed blanket design.**

> "Making sure that we have enough tritium, and figuring out how to extract that material to use it for future shots, is a big task. We have to be able to breed enough tritium to keep the plant going."
> — Callahan interview, §"What are the challenges of working with deuterium and tritium"

Lithium blankets are confirmed, with SRNL collaboration on tritium extraction. But without knowing the blanket chemistry (FLiBe, LiPb, liquid Li), neutron multiplier strategy, or tritium breeding ratio target, it is impossible to assess whether the blanket design achieves TBR > 1 or to estimate blanket capital and replacement costs. The absence of this data is a modeling blocker for CAS27 (special materials), C220101 (blanket structure), and CAS80 (fuel cycle operating cost).

**Ranking of challenges by LCOE impact (descending):**

1. **Driver capital cost** — Unknown beamline count × unknown unit cost; likely the dominant capital item.
2. **Target gain validation** — If 50–100 gain is not achieved, either yield per shot drops (requiring higher rep rate or larger driver to compensate) or the concept is uneconomic.
3. **Target fabrication cost at 10 Hz** — Cone-in-shell targets at 900,000/day throughput; analyst patch estimates $0.80/shot but uncertainty band is wide ($0.50–$1.20).
4. **Final optics lifetime** — Optics degradation at 10 Hz drives replacement frequency and capital reserve requirements.
5. **Chamber + blanket cost** — Undisclosed architecture prevents bottom-up estimation.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in **ascending order of maturity** (least mature first):

### Proton fast ignition physics — TRL ~2

**Demonstrated:** Petawatt lasers have generated high-energy proton beams via target normal sheath acceleration (TNSA) in laboratory experiments (Texas Petawatt, ELI Beamlines, OMEGA EP). Proton energies of 10–100 MeV and beam currents of ~10¹³ protons/shot have been measured.

**On paper only:** Coupling a proton beam to a compressed D-T core to achieve ignition. Academic simulations (Tabak 1994, Roth 2001, Temporal 2002) suggest this pathway is viable, but no experiment has demonstrated proton-driven ignition at fusion-relevant core densities (>100 g/cm³). The cone-in-shell target geometry required to guide the ignitor beam into the compressed fuel adds alignment and hydrodynamic instability challenges not present in symmetric capsule designs.

**Missing at scale:** Fast ignition at target gains of 50–100. The highest gain demonstrated by any IFE approach is NIF's ~3.5× capsule gain (indirect drive), achieved after decades of optimization. Fast ignition's claimed advantage — lower compression energy requirements enabling higher gain — has not been validated experimentally.

**Impact on LCOE:** If proton fast ignition cannot achieve the 50–100 gain required for economic breakeven (as stated by Callahan), the concept reduces to a less-efficient variant of direct drive, requiring either larger drivers or accepting higher LCOE.

### High-repetition-rate diode-pumped solid-state laser — TRL ~3

**Demonstrated:** DPSSL technology exists at laboratory scale (e.g., Mercury laser at LLNL, Lucia laser at Czech ELI Beamlines). Wall-plug efficiencies of ~10% have been achieved in single-shot or low-rep-rate configurations. Diode arrays (the pump source) are commercially available but not at the scale or cost required for fusion ($0.007/W is the LLNL/TRUMPF target; current commercial pricing is ~$0.02/W per Xcimer estimates).

**On paper only:** DPSSL operation at 10 Hz continuously for 30+ years. The Amplitude partnership ($40M, PRNewswire 2024) is developing modular beamlines, but no 10 Hz fusion-class DPSSL has been built or operated. Thermal management (removing waste heat from amplifier slabs at 10 Hz), gain medium lifetime (Nd:glass radiation damage and thermally-induced stress), and frequency-conversion optics durability at high average power are all unresolved.

**Missing at scale:** Unknown number of beamlines required for compression. LaserFocusWorld cites Ditmire's projection of "around 80 beamlines" as an ultimate facility scale, but this is not a committed Focused Energy design specification. The capital cost of N beamlines × $X/beamline is the dominant cost driver for any laser IFE concept, and neither N nor X is publicly known for Focused Energy.

**Impact on LCOE:** Driver capital cost is likely 40–60% of total overnight capital (by analogy to NIF's LIFE studies and Xcimer's cost breakdowns). Without knowing beamline count and unit cost, LCOE estimates for Focused Energy are speculative.

### Cone-in-shell cryogenic target fabrication — TRL ~3

**Demonstrated:** Cryogenic D-T capsules have been manufactured for NIF (symmetric spheres with ice layer). Cone-in-shell targets have been fabricated for fast-ignition experiments (HiPER, OMEGA EP), but not at cryogenic specifications or at high throughput. LLNL's target fabrication facility produces ~400 targets/year for NIF (Callahan interview); scaling to 900,000 targets/day (10 Hz × 0.8 availability × 86,400 s/day ≈ 691,200 shots/day, rounded to ~900k in company statements) requires a ~6,000× throughput increase.

**On paper only:** Automated batch production of cone-in-shell cryogenic targets at $0.50–$1.20/shot (analyst patch range). The cone adds fabrication complexity: cone-to-capsule alignment, cone material selection (gold is traditional but expensive; cheaper alternatives degrade coupling efficiency), and cryogenic handling (ice layer must remain intact during cone attachment and target insertion). Mass production paradigms (analogous to pharmaceutical pill manufacturing or ammunition production) have been proposed in LLNL IFE studies but never demonstrated.

**Missing at scale:** 10 Hz target factory delivering cone-in-shell cryo targets continuously for 30 years. The target factory is a complex facility requiring D-T fuel handling, cryogenic layering systems, cone fabrication and attachment, quality control at production rate (statistical sampling, not per-target inspection), and automated delivery to the chamber.

**Impact on LCOE:** At $0.80/shot and 10 Hz, annualized target cost is ~$220M/year (assuming 80% availability). If target cost rises to the high end of the uncertainty band ($1.20/shot), this becomes ~$330M/year — a significant operating cost that scales directly with plant lifetime and cannot be reduced by capital equipment learning curves.

### Chamber clearing and debris management at 10 Hz — TRL ~2

**Demonstrated:** Single-shot IFE chambers have operated at NIF, OMEGA, and other facilities. Debris mitigation strategies (magnetic deflection, gas jets, liquid walls) have been tested at low repetition rates or with surrogates (water jets as FLiBe analog).

**On paper only:** Chamber clearing within ~100 ms to permit next-shot target insertion. After each fusion pulse, vaporized target debris (cone material, capsule ablator, unburned D-T) must condense, be pumped out, and vacuum re-established. At 10 Hz, this cycle repeats ~900,000 times/day. Thick liquid walls (if used) must reform and stabilize between shots; the debris removal system must handle activated materials (tritium, neutron-activated cone metals) at high throughput.

**Missing at scale:** No 10 Hz IFE chamber has been operated. The Z-IFE study (MagLIF pulsed-power IFE) baselined 0.1 Hz specifically because chamber clearing at 1+ Hz is hard; laser IFE target gains are typically lower than MagLIF's GJ-class projections, reducing per-shot debris mass but not eliminating the challenge.

**Impact on LCOE:** If chamber clearing limits achievable repetition rate below 10 Hz, time-averaged power output drops proportionally, increasing LCOE. Chamber availability losses (due to debris-induced downtime) directly reduce capacity factor.

### Tritium breeding blanket (lithium, unspecified chemistry) — TRL ~2–3

**Demonstrated:** Small-scale tritium breeding experiments (LIBRA/BABY series with D-T neutrons), helium-cooled pebble-bed and water-cooled lead-lithium mock-ups, FLiBe molten salt loops in fission reactor heritage (MSRE). ITER TBM designs are in detailed engineering.

**On paper only:** Full-scale lithium blanket integrated with an IFE chamber, achieving TBR > 1 and extracting tritium at kg/day rates. The Focused Energy collaboration with SRNL (Callahan interview) targets tritium extraction system design, but the blanket itself is not described. For IFE, blanket geometry is simpler than MFE (no divertor, no complex 3D shaping to avoid magnet coils), but must survive pulsed neutron loading and integrate with chamber clearing systems.

**Missing at scale:** IFE-specific blanket designs are sparse in the literature. HYLIFE-II (thick liquid FLiBe wall) and SOMBRERO (liquid Flibe spray) are reference concepts, but neither was built or tested under fusion conditions.

**Impact on LCOE:** Without knowing blanket chemistry, it is impossible to estimate CAS27 (special materials — FLiBe inventory, enriched Li-6), C220101 (blanket structure capital cost), or tritium extraction operating cost. This is a modeling blocker.

### Final optics and beam transport — TRL ~4–5

**Demonstrated:** NIF's final optics (grazing-incidence mirrors, debris shields, frequency-conversion crystals) survive single-shot operation at ~2 MJ laser energy. UV laser transport at 351 nm (NIF) and 527 nm (frequency-doubled Nd:glass) is established. Protective schemes (sacrificial debris shields, gas curtains) extend optics lifetime but require periodic replacement.

**On paper only:** Final optics surviving 10 Hz operation for 30 years (~9 × 10⁹ shots). Each shot exposes optics to X-rays, debris, and neutrons. Grazing-incidence mirror geometries reduce direct debris impingement but increase system size and alignment complexity. Fast ignition's two-beam architecture (compression + ignitor) doubles the number of beam paths requiring protection.

**Missing at scale:** No high-rep-rate laser IFE facility has operated long enough to validate optics lifetime projections. Optics replacement frequency and cost are critical unknowns for all laser IFE concepts.

**Impact on LCOE:** If final optics require replacement every N shots, the replacement cost ($/optic × number of beamlines × replacement frequency) becomes a significant operating cost. Optics degradation can also reduce laser coupling efficiency over time, lowering effective target gain.

### Petawatt short-pulse ignitor laser — TRL ~4–5

**Demonstrated:** Petawatt-class lasers exist (Texas Petawatt, ELI Beamlines, OMEGA EP). Chirped-pulse amplification (CPA) is a mature technology for generating ultrashort high-intensity pulses. The LaserFocusWorld article cites Ditmire's Texas Petawatt heritage and National Energetics' ELI Beamlines delivery as relevant background.

**On paper only:** Petawatt laser operating at 10 Hz continuously. Current petawatt systems are single-shot or low-rep-rate due to thermal management, gain medium damage, and compressor grating lifetime constraints. The 150 kJ short-pulse specification (LaserFocusWorld) is large for a petawatt system; this energy level at 10 Hz requires ~1.5 MW average power from the ignitor laser alone (before wall-plug efficiency losses).

**Missing at scale:** High-rep-rate petawatt laser integrated with a fusion chamber. The ignitor beamline(s) must deliver the short pulse on target within ~100 ms of the compression pulse, requiring fast pulse sequencing and beam alignment.

**Impact on LCOE:** The ignitor laser is a separate capital cost item from the compression driver. If it requires exotic components (e.g., large-aperture gratings, high-damage-threshold optics) or frequent maintenance, it adds both capital and operating cost. The 1.5 MW average power draw (before efficiency losses) also increases recirculating power fraction.

### Energy conversion / Balance of Plant — TRL ~7–8

**Demonstrated:** Conventional steam Rankine cycle at GW scale in fission and fossil plants.

> "We will use a conventional steam cycle to convert the heat into electricity."
> — Callahan interview, §"How will you capture the heat"

**Missing at scale:** Integration with pulsed IFE thermal source. At 10 Hz, the thermal power delivered to steam generators is time-averaged continuous, but the neutron energy deposition in the blanket is pulsed. Thermal buffering (via blanket thermal mass or intermediate coolant loops) smooths the pulse, but thermal cycling effects on blanket materials and heat exchanger integrity are not characterized.

**Impact on LCOE:** Balance of plant is a mature technology with well-understood costs. This is a lower-risk subsystem relative to the driver and chamber.

## 4. Key Materials and Supply Chain Considerations

### Tritium (startup inventory + breeding)

**Requirement:** D-T fuel requires tritium at ~1–5 kg startup inventory plus continuous breeding at TBR > 1.

**Supply constraint:** Global civilian tritium inventory is ~25 kg, produced primarily as a byproduct of CANDU heavy-water reactors. A single D-T reactor startup consumes a meaningful fraction of global supply. Current market rate is >$30,000/kg (Callahan interview does not cite this figure; this is external context from tokamak TEA literature).

**Breeding pathway:** Lithium blankets confirmed (Callahan interview); SRNL collaboration on tritium extraction. Specific blanket chemistry (FLiBe, LiPb, liquid Li) not disclosed. Li-6 enrichment is required for efficient breeding; enrichment capacity is limited globally (Russia and China use mercury-based processes banned elsewhere; US/EU enrichment is small-scale).

**Impact on LCOE:** Tritium supply is a fleet-level constraint, not a single-plant cost driver. But tritium fuel cycle operating cost (extraction, purification, storage, handling) is non-trivial. Without knowing blanket chemistry, CAS80 (fuel cycle OPEX) cannot be estimated from first principles.

### Laser diodes (for DPSSL pump arrays)

**Requirement:** DPSSL compression driver uses diode arrays to pump Nd:glass amplifiers. At ~10% laser efficiency and unknown beamline count, the diode array represents a significant capital cost.

**Supply constraint:** Commercial laser diodes are available, but fusion-class DPSSL requires diodes at $0.007/W (LLNL/TRUMPF target for economic viability) vs. ~$0.02/W current commercial pricing (Xcimer estimate in their whitepaper). Focused Energy's Amplitude partnership ($40M) is developing diode-pumped laser technology, but has not disclosed unit cost targets or production volumes.

**Scaling analogy:** Xcimer's indirect-drive competitor estimates that diode scale-up "has already been seen for similar lasers in all devices with FaceID" (consumer electronics analogy). But fusion-class diodes require higher power, longer lifetime, and better thermal management than consumer applications.

**Impact on LCOE:** Diode cost is embedded in the DPSSL beamline capital cost. If diodes achieve the $0.007/W target via mass production, driver capital cost could drop significantly. If diodes remain expensive, driver cost stays high.

### Cone-in-shell target materials (gold cone, D-T capsule, cryogenic ice layer)

**Requirement:** Cone-in-shell targets at 900,000/day throughput. The analyst patch estimates $0.80/shot (uncertainty $0.50–$1.20) based on a 1.3× complexity multiplier over symmetric capsules, which in turn are priced from Meier 2006 HYLIFE-II target factory economics ($0.30–$0.50/symmetric capsule in 2006 dollars, CPI-adjusted to $0.61 in 2024 dollars).

**Material components:**
- D-T fuel (deuterium from seawater, tritium bred from lithium — Callahan interview, §"Meanwhile, Pearl is the capsule").
- Ablator shell (plastic or other low-Z material).
- Cryogenic ice layer (if required for high gain; not explicitly confirmed by Focused Energy but implied by gain targets of 50–100).
- Gold cone or alternative high-Z cone material to guide ignitor beam.

**Supply constraint:** Gold is expensive (~$60,000/kg) but used in small quantities per target (cone mass is ~mg to tens of mg in academic designs). The binding constraint is not material cost but manufacturing complexity: cone-to-capsule alignment, cryogenic handling, and throughput at 900,000/day. The cone adds fabrication steps relative to symmetric capsules, justifying the 1.3× complexity multiplier in the analyst patch.

**Impact on LCOE:** At $0.80/shot and 10 Hz (80% availability), annualized target cost is ~$220M. This is a significant operating cost (~10–20% of total OPEX for a GW-scale plant by analogy to Xcimer's $1/target goal and Inertia's target cost assumptions). If target cost rises to $1.20/shot, this becomes ~$330M/year — a material LCOE penalty.

### FLiBe or alternative molten salt (if used as blanket/coolant)

**Requirement:** If Focused Energy uses FLiBe (Li₂BeF₄) as blanket coolant (not confirmed; lithium blankets are confirmed but chemistry is undisclosed), the plant requires a large FLiBe inventory (~1,000–2,000 tonnes for a GW-scale IFE chamber by analogy to HYLIFE-II).

**Supply constraint:** Beryllium is toxic and produced in limited quantities globally (~300 tonnes/year, dominated by Materion Corp in the US). Lithium enrichment (Li-6) adds cost and supply-chain dependency. FLiBe production at industrial scale does not currently exist.

**Cost analogy:** The Araiinejad tokamak TEA study estimates future NOAK FLiBe cost at ~$154/kg (assuming 20% learning rate). At 1,500 tonnes, this is ~$230M for initial inventory (CAS27 special materials). FLiBe has a shared supply chain with certain molten-salt fission concepts (Kairos Power), which could aid economies of scale.

**Impact on LCOE:** If FLiBe is the blanket coolant, CAS27 (special materials) is a significant capital item ($200–300M). If Focused Energy uses an alternative blanket chemistry (LiPb, liquid Li), the material cost and supply-chain profile differ. Without knowing the blanket design, this cost cannot be estimated.

### Final optics consumables (debris shields, frequency-conversion crystals)

**Requirement:** Final optics exposed to X-rays, debris, and neutrons degrade over time. Sacrificial debris shields must be replaced periodically; frequency-conversion crystals (for Nd:glass → 527 nm) may require replacement if laser-induced damage accumulates.

**Supply constraint:** Large-aperture KDP or DKDP crystals (standard for NIF-class frequency conversion) are grown at limited facilities (Cleveland Crystals, LLNL). Grazing-incidence mirrors require precision optical fabrication. At 10 Hz over 30 years, the cumulative number of optics replacements is large.

**Impact on LCOE:** Optics replacement is an operating cost (OPEX) that scales with shot count, not calendar time. If final optics require replacement every 10⁶ shots, the plant experiences ~9,000 optics replacements over its lifetime. At $10k–$100k per optic (depending on size and complexity) × number of beamlines, this is a non-trivial cost.

### Deuterium (fuel feedstock)

**Requirement:** Deuterium is extracted from seawater (Callahan interview). D-T fuel cycle consumes deuterium continuously.

**Supply constraint:** Deuterium is abundant (1 in 6,700 hydrogen atoms in seawater). Extraction is commercially available; heavy water (D₂O) is produced for CANDU reactors and other applications. Cost is ~$300/kg for heavy water (containing deuterium), making fuel cost negligible relative to other plant costs.

**Impact on LCOE:** Deuterium fuel cost is negligible (order $1M/year for a GW-scale plant). This is a non-binding constraint.

## 5. Design Point Parameters

No design-point selection exists upstream for this concept. The parameters below are extracted from the dossier for the pilot plant (LightHouse) and the eventual commercial-scale plant, where distinguishable. All values are at native scale (power output as designed, not scaled to 1 GWe).

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Confinement concept | Laser ICF (fast ignition) | dossier.md §Confinement Concept | high | Proton fast ignition; two-pulse architecture (compression + ignitor) |
| Fuel | D-T | focused-energy-technology.md §general description; callahan-interview.md §"Meanwhile, Pearl is the capsule" | high | Deuterium from seawater, tritium bred from lithium |
| Repetition rate | ~10 Hz | callahan-interview.md §"How do you develop the capsule" ("about 10 per second"; "900,000 shots a day" ≈ 10.4 Hz) | high | Distinctly higher than indirect-drive concepts (sub-Hz); lower yield per shot |
| Target gain (goal) | 50–100 | callahan-interview.md §"What is the current state of the art at NIF" | medium-high | Required for economic viability per Callahan; NIF achieved ~4.1; fast ignition's advantage is lower compression energy → higher gain potential |
| Laser efficiency (goal) | ~10% | callahan-interview.md §"So is boosting efficiency one of your key goals" | high | DPSSL compression driver; NIF's flashlamp-pumped system is <1% |
| Engineering gain (goal) | >1 | callahan-interview.md §"Can you tell us about Focused Energy's two technologies" (LightHouse pilot plant) | medium-high | Net electricity production; implies recirculating power fraction <50% |
| Driver technology | DPSSL (Nd:glass, ~527 nm assumed) + CPA short-pulse (~150 kJ petawatt-class) | prnewswire-2024.md (Amplitude $40M partnership); laserfocusworld-2021.md (150 kJ short-pulse, Texas Petawatt heritage) | medium-high | Two-pulse architecture; frequency doubling to 527 nm is standard but not explicitly stated |
| Beamline count | "around 80 beamlines" (Ditmire projection, not committed design) | laserfocusworld-2021.md | low | Ultimate facility scale; not a committed Focused Energy specification |
| Energy capture | Thermal (steam) | callahan-interview.md §"How will you capture the heat" | high | Conventional steam Rankine cycle |
| Tritium breeding | Li blanket (chemistry undisclosed) | callahan-interview.md §"What are the challenges of working with deuterium and tritium"; prnewswire-2024.md (SRNL collaboration) | medium | FLiBe vs LiPb vs liquid Li not specified; SRNL partnership on tritium extraction |
| Target type | Pearl™ cone-in-shell D-T capsule (cryogenic assumed for high gain) | focused-energy-technology.md ("Pearl™ fuel capsules"); laserfocusworld-2021.md ("nearby target" for proton generation); analyst-patch.md (cone-in-shell geometry) | medium | Cone guides ignitor beam to compressed core; cryogenic ice layer implied by 50–100 gain target but not explicitly stated |
| Target unit cost | $0.80/shot [analyst patch; uncertainty $0.50–$1.20] | analyst-patch-target-unit-cost.md (1.3× complexity multiplier over symmetric capsules, NOAK volume) | low | No company-published figure; derived from Meier 2006 HYLIFE-II baseline ($0.61 for symmetric, CPI-adjusted) + 30% cone-in-shell penalty |
| Pilot plant timeline | End of 2030s (LightHouse) | callahan-interview.md §"So what's the timeline on development?" | medium | "Fairly aggressive timeline"; startup risk acknowledged |
| Net electric output | Not disclosed ("gigawatt-scale" ambition) | callahan-interview.md (qualitative only) | N/A | No quantitative power target published |
| Thermal power | Not disclosed | N/A | N/A | Cannot be derived without knowing yield/shot and repetition rate at design point |
| Fusion power | Not disclosed | N/A | N/A | Cannot be derived without yield/shot |
| Compression laser energy/shot | Not disclosed | N/A | N/A | Lower than NIF's ~2 MJ (direct drive eliminates X-ray conversion losses), but no figure given |
| Ignitor laser energy/shot | ~150 kJ [LaserFocusWorld; petawatt-class short pulse] | laserfocusworld-2021.md §description of two-pulse architecture | low | Cited in third-party interview, not Focused Energy materials; confidence low pending direct confirmation |

**Notes:**
- No `P_native` can be assigned; no net electric output is published. The "gigawatt-scale" ambition is qualitative.
- No `p_input` (auxiliary power) can be estimated without knowing compression laser energy, ignitor laser energy, and repetition rate at the design point.
- No `p_fus` (fusion power) can be derived without knowing yield/shot (which depends on target gain, which is a goal not a demonstrated value).
- The Pearl™ capsule's "30x output increase" (focused-energy-technology.md) is relative to NIF indirect drive, not an absolute yield/shot specification.

## 5b. Override Candidates

Per-account walkthrough of the canonical 1costingFE schema for this archetype (`IFE_laser_pulsed_driver`). The walkthrough below considers each account, asks whether the dossier provides company-grounded data justifying a departure from the library default, and proposes overrides only where evidence exists.

**Override-count expectation:** Archetype-Fit is Med → expect 3–8 enabled overrides.

### Walkthrough

**C220101 (First wall, blanket & neutron multiplier):** Lithium blankets confirmed, but chemistry (FLiBe vs LiPb vs liquid Li) undisclosed. Blanket geometry and neutron multiplier strategy not described. **No company-grounded quantity or cost → no override.** Library default stands.

**C220102 (Radiation shield):** No company data on shielding architecture. Fast ignition's cone-in-shell geometry may affect shielding penetration paths (cone opening), but no quantitative basis for override. **No override.**

**C220104 (Primary pulsed driver — laser):** DPSSL compression driver + CPA short-pulse ignitor. Two-pulse architecture is unique, but no company-published driver cost, beamline count, or unit cost exists. LaserFocusWorld cites "around 80 beamlines" (Ditmire projection, not committed design) and 150 kJ ignitor energy, but these are not company disclosures. **No company-grounded cost → no override.** This is the highest-impact account (likely 40–60% of capital by IFE analogy), but absence of data prevents justified override.

**C220105 (Primary structure):** No company data on chamber structural design. **No override.**

**C220106 (Vacuum system):** 10 Hz operation requires fast chamber clearing and vacuum re-establishment, but no company-published vacuum system specifications or cost. **No override.**

**C220107 (Power supplies — pulsed-power capacitor bank):** This account is for electrically-driven pulsed schemes (MagLIF, Z-pinch). Laser IFE uses laser driver power supplies (not capacitor banks); those are costed under C220104. **Not applicable to this archetype → no override.**

**C220108 (Target factory):** Cone-in-shell D-T targets at ~10 Hz (900,000 shots/day per Callahan). The analyst patch provides a per-target unit cost ($0.80/shot, uncertainty $0.50–$1.20), derived from Meier 2006 HYLIFE-II baseline + 1.3× cone-in-shell complexity multiplier. This is `provenance: derived` (analyst-sourced unit cost × company-stated throughput). The library's default target factory cost is built for symmetric capsules; the cone-in-shell geometry justifies a relative override.

However, **C220108 is the target *factory* capital cost, not the per-shot consumable cost.** The per-shot cost belongs in CAS80 (annualized fuel cost). The analyst patch's $0.80/shot is the *input* to a factory capital cost calculation (factory must deliver N targets/year at $X/target → factory capex scales with throughput × target complexity), but the patch does not provide a factory capex figure. Without a company-grounded factory cost or a published factory cost model that accepts the $0.80/shot input, I cannot construct a justified override for C220108.

**No override for C220108** (target factory capital). The $0.80/shot figures into CAS80 (fuel cycle OPEX), which is not overridable per the override semantics policy (CAS80 overrides are silently dropped; see output template Rule 5).

**C220110 (Remote handling & maintenance):** No company data on remote handling strategy. IFE chambers are simpler than MFE (no in-vessel magnets to avoid, no divertor cassettes), but cone-in-shell target debris may complicate chamber maintenance. **No company-grounded data → no override.**

**C220111 (Reactor-equipment installation & assembly):** Fraction of CAS22 subtotal; no company-specific data. **No override.**

**CAS21 (Buildings & site structures):** No company data on building footprint, hot cell requirements, or turbine hall specifications. **No override.**

**CAS23 (Turbine plant equipment):** Conventional steam cycle confirmed (Callahan interview). No company-specific thermal power, efficiency, or turbine specifications. Library default assumes standard Rankine cycle for D-T thermal plants; no evidence of departure. **No override.**

**CAS24 (Electric plant equipment):** No company data. **No override.**

**CAS26 (Heat rejection system):** No company data. **No override.**

**CAS27 (Special materials — initial reactor material inventory / blanket fill):** Lithium blankets confirmed, but chemistry undisclosed. If FLiBe, this would be a large capital item (~$200–300M for GW-scale by tokamak analogy). But without knowing whether it's FLiBe, LiPb, or liquid Li, and without a company-disclosed inventory quantity or unit cost, I cannot construct a justified override. **No override** (data gap blocks override discovery).

**CAS70 (Annualized O&M):** Not overridable per policy (silently dropped). **No override.**

**CAS80 (Annualized fuel cost):** Not overridable per policy (silently dropped). The $0.80/shot target unit cost (analyst patch) would flow into CAS80 if CAS80 were overridable, but the override semantics note that CAS80 overrides are no-ops. **No override.**

### Override Registry

No justified overrides discovered. The dossier provides high-level architectural features (two-pulse laser, lithium blankets, 10 Hz, cone-in-shell targets) but lacks the quantitative cost figures, component masses, or unit prices required to justify departures from library defaults.

**Discrepancy flag:** The expected override count for Archetype-Fit = Med is 3–8, but the evidence supports zero overrides. This reflects the opacity of Focused Energy's public disclosures rather than a concept that perfectly aligns with library defaults. The absence of overrides is a data-gap symptom, not an archetype-fit validation.

```yaml
overrides: []
```

**Key blocked overrides (would be proposed if data existed):**
1. **C220104 (laser driver):** Company has not disclosed beamline count, unit cost, or total driver capex. This is likely the dominant cost account.
2. **CAS27 (blanket inventory):** Lithium blankets confirmed but chemistry and inventory undisclosed.
3. **C220108 (target factory):** $0.80/shot per-target cost is known (analyst patch), but factory capex is not. The library default factory cost may underestimate cone-in-shell complexity.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Net electric output and thermal power at design point | S5 | proprietary | blocking | Focused Energy J. Fusion Energy 2023 paper (paywalled, not ingested); company technical disclosures |
| 2 | Laser driver capital cost (beamline count × unit cost) | S2, S5b | proprietary | blocking | Company engineering studies or investor disclosures; DPSSL cost models from Amplitude partnership |
| 3 | Blanket chemistry (FLiBe vs LiPb vs liquid Li) and inventory quantity | S3, S4, S5b | proprietary | blocking | J. Fusion Energy 2023 paper; chamber design publications |
| 4 | Target gain validation at proton fast ignition conditions | S2, S3 | truly-unknown (physics risk) | blocking | Experimental campaigns at petawatt facilities (Texas Petawatt, ELI Beamlines, OMEGA EP); Focused Energy's own ignition experiments (if/when conducted) |
| 5 | Final optics lifetime at 10 Hz (replacement frequency) | S3, S4 | not-yet-sourced | important | Laser IFE optics degradation studies (LLNL, Xcimer optics roadmaps); high-average-power laser facility operational data |
| 6 | Target factory capital cost for cone-in-shell targets at 900k/day throughput | S5b | derivable (with cost model) | important | LLNL IFE target factory studies (Meier 2006 provides per-target cost; factory capex model needed); Focused Energy disclosures |
| 7 | Chamber clearing and debris management at 10 Hz | S2, S3 | not-yet-sourced | important | IFE chamber engineering studies (HYLIFE-II, SOMBRERO for thick liquid walls; Z-IFE for pulsed clearing); chamber simulation papers |
| 8 | Ignitor laser specifications (beamline count, unit cost, maintenance) | S3, S5 | proprietary | important | Focused Energy technical disclosures; petawatt laser capital cost benchmarks |
| 9 | Tritium breeding ratio and extraction efficiency for undisclosed blanket chemistry | S3, S4 | proprietary | important | SRNL collaboration outputs (if published); blanket neutronic studies |
| 10 | Pilot plant (LightHouse) specifications and timeline validation | S5 | proprietary | nice-to-have | Company roadmap updates; engineering milestone publications |

**Gap-type definitions:**
- **proprietary:** Company holds the data but has not disclosed it publicly.
- **truly-unknown:** Data does not exist (physics not validated, engineering not designed).
- **not-yet-sourced:** Data likely exists in published literature but not yet ingested into dossier.
- **derivable:** Can be calculated from available data with appropriate cost models or scaling relationships.

**Criticality definitions:**
- **blocking:** LCOE model cannot produce meaningful estimate without this data.
- **important:** LCOE estimate possible but with wide uncertainty bands; data significantly narrows corridor.
- **nice-to-have:** Refines model but does not change order-of-magnitude LCOE estimate.

## 7. Family-Delta vs Comparables

Fixed comparables for this concept:
- 26-laser-icf-indirect-drive (Inertia Thunderwall)
- 30-laser-icf-nif-commercialization (Focused Energy LIFE-class? — this may be a labeling error; LIFE is LLNL's NIF-heritage design, not Focused Energy)
- 31-laser-icf-oec-architecture (Blue Laser Fusion)
- 32-laser-icf-french-national (GenF Systems)
- 17a-laser-icf-hybrid-drive (Xcimer Energy)

**Note:** Comparables 30 and 32 may not have approved analyses available (per "No approved prior analyses available" in the prompt). The family-delta below is written against the general characteristics of these concept types from the handwritten exemplar (26-laser-icf-indirect-drive.md) and the dossier for 17a.

### vs Indirect Drive (26, 30, 31, 32)

**Subsystem divergence:** Drive architecture.

- **Indirect drive** (NIF heritage): Laser → hohlraum → X-rays → capsule ablation. The hohlraum (gold or depleted uranium cylinder) converts laser energy to X-rays, which then symmetrically compress the capsule. Coupling efficiency is ~12% (laser energy → X-ray energy absorbed by capsule).
- **Fast ignition** (Focused Energy): Two-pulse architecture. Compression pulse → direct capsule ablation (no hohlraum, no X-ray conversion). Ignitor pulse → proton beam → ignites compressed core. Coupling efficiency is claimed >50% (LaserFocusWorld cites 80% from "energy on target of Athena" context, but this is not a Focused Energy-specific figure and confidence is low).

**Cost effect:** **Potential cost advantage, magnitude unknown.**

Eliminating the hohlraum removes:
- Hohlraum fabrication cost (gold or DU cylinders).
- X-ray conversion losses (laser → X-ray efficiency is <10% in indirect drive).

But fast ignition adds:
- Second laser system (ignitor beamline(s) with petawatt-class short-pulse capability).
- Cone-in-shell target complexity (cone adds fabrication steps, materials cost, and alignment requirements).

The net cost effect depends on whether [compression driver cost reduction from eliminating hohlraum] > [ignitor laser cost + cone-in-shell target cost premium]. No public data from Focused Energy quantifies this trade. Xcimer's hybrid-drive approach (which uses a brief hohlraum pulse + direct drive) claims cost advantages over pure indirect drive; Focused Energy's fast ignition makes a similar but more aggressive claim (eliminating hohlraum entirely). **Direction: likely advantage; magnitude: unquantified.**

**Target gain:** Focused Energy targets 50–100 gain (Callahan interview). NIF's best indirect-drive shot achieved ~4.1 target gain (8 MJ out / ~2 MJ laser in). If fast ignition achieves the 50–100 gain target, it produces 10–25× more fusion energy per unit laser energy than demonstrated indirect drive. This would reduce required driver size (fewer beamlines) or permit higher repetition rate with the same driver, both of which lower LCOE. **Direction: advantage if target validated; risk if not.**

### vs Hybrid Drive (17a — Xcimer Energy)

**Subsystem divergence:** Ignition mechanism and driver type.

- **Hybrid drive** (Xcimer): KrF excimer laser (248 nm deep-UV), two-beam symmetric direct drive with shaped intensity rings, brief hohlraum pulse to create uniform ablation plasma. Compression + ignition in a single integrated pulse sequence; coupling efficiency >50% claimed.
- **Fast ignition** (Focused Energy): DPSSL (Nd:glass, ~527 nm), two-pulse architecture (compression + separate ignitor producing proton beam). Cone-in-shell target geometry.

**Cost effect:** **Ambiguous direction.**

Xcimer's KrF excimer laser is more expensive per joule than DPSSL (Xcimer's whitepaper estimates $100–$120/J FOAK, $60–$80/J NOAK for their driver), but excimer lasers have no gain medium to degrade (gas is replaced, not damaged) and no final optics in the beam path (the gas cell window is the last optic). DPSSL has lower $/J but faces gain medium damage and final optics degradation at high rep-rate.

Xcimer's symmetric two-beam direct drive eliminates the cone (simpler targets than fast ignition), but Xcimer's hohlraum pulse adds a laser → hohlraum → X-ray step that Focused Energy's pure direct-drive compression avoids.

**Net cost comparison:** Xcimer's published cost structure ($3.5B total plant cost, $60–80/J driver NOAK) provides a benchmark, but Focused Energy has not disclosed comparable figures. Without knowing Focused Energy's driver $/J and beamline count, the cost delta is unquantifiable. **Direction: unknown; both claim advantages over indirect drive but via different pathways.**

**Target gain and repetition rate:** Xcimer targets >200× capsule gain at ~1 Hz (lower rep-rate than Focused Energy, higher yield/shot to compensate). Focused Energy targets 50–100 gain at ~10 Hz (higher rep-rate, lower yield/shot). The two approaches converge on similar time-averaged fusion power but with different engineering trade-offs: Xcimer's lower rep-rate simplifies chamber clearing; Focused Energy's higher rep-rate tolerates lower gain per shot. **Cost effect: chamber clearing at 10 Hz is harder (penalty for Focused Energy); cone-in-shell targets are more complex (penalty for Focused Energy); proton fast ignition's gain is less validated (risk for Focused Energy). Xcimer's approach appears lower-risk but with higher per-shot energy requirements.**

### Shared IFE Challenges (all comparables)

All laser IFE concepts share:
- **D-T fuel cycle:** Tritium breeding, extraction, handling; FLiBe or alternative blanket chemistry.
- **High-rep-rate target fabrication:** Cryogenic D-T capsules at sub-Hz to ~10 Hz throughput; cost target ~$1/shot for economic viability.
- **Final optics survivability:** X-rays, debris, and neutrons degrade optics; replacement frequency is a cost driver.
- **Chamber clearing and debris management:** Vaporized target debris must be removed between shots.
- **Laser driver capital cost dominance:** Driver is 40–60% of total overnight capital (by analogy to NIF's LIFE studies).

Focused Energy's departures (two-pulse architecture, cone-in-shell targets, proton fast ignition) are concept-distinctive but do not eliminate these shared challenges. The cost effect of the departures is **unknown due to absence of published cost data.**

### Summary Table

| Comparable | Divergent Subsystem | Cost Effect Direction | Cost Effect Magnitude | Confidence |
|---|---|---|---|---|
| Indirect drive (26, 30, 31, 32) | Drive architecture (no hohlraum, two-pulse fast ignition) | Likely advantage (eliminate X-ray conversion losses, higher target gain potential) | Unknown (ignitor laser + cone-in-shell target penalty vs hohlraum elimination savings) | Low (no Focused Energy cost data) |
| Hybrid drive (17a) | Ignition mechanism (proton fast ignition vs two-beam symmetric direct drive) and driver type (DPSSL vs excimer) | Unknown (trade-offs in driver $/J, target complexity, chamber clearing rate, gain validation risk) | Unknown (no Focused Energy driver cost or plant cost disclosed) | Low |
| All IFE | Shared D-T fuel cycle, tritium breeding, target factory, final optics, chamber clearing | Neutral (shared challenges) | — | — |

**What is genuinely novel:** Proton fast ignition as the ignition mechanism. This is the core physics innovation. All other subsystems (DPSSL driver, D-T fuel, tritium breeding, steam cycle) are borrowed from other IFE or fusion concepts. The novelty is not in the components but in their integration into a two-pulse compression + proton-ignition architecture.

**What is borrowed:** DPSSL laser technology (LLNL Mercury laser heritage, Amplitude partnership), D-T fuel cycle (shared with all D-T fusion), lithium blanket tritium breeding (shared with D-T MFE and IFE), steam Rankine cycle (conventional power), cryogenic target fabrication (NIF heritage).

## 8. Sources

Listed in order of importance:

1. **Callahan, T. J. (Focused Energy CEO) — Physics World interview** (2024, exact date not in file metadata).
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-02/sources/focused-energy-callahan-interview.md`
   **Contribution:** Most substantive single source. Confirms ~10 Hz repetition rate (900,000 shots/day), target gain goals (50–100), laser efficiency goal (~10%), engineering gain >1 for LightHouse pilot plant, lithium blankets with SRNL collaboration on tritium extraction, conventional steam cycle, D-T fuel from seawater + lithium, pilot plant timeline (end of 2030s). Establishes that NIF achieved ~4.1 gain and that direct drive eliminates X-ray conversion losses from indirect-drive hohlraums. This interview is the quantitative anchor for the entire analysis.

2. **Analyst patch: Target unit cost** (2024, internal analyst source).
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-04/sources/analyst-patch-target-unit-cost.md`
   **Contribution:** Per-target manufacturing cost estimate ($0.80/shot, uncertainty $0.50–$1.20) for cone-in-shell D-T capsules at NOAK production volumes. Derived from Meier 2006 HYLIFE-II symmetric capsule baseline ($0.30–$0.50 in 2006 dollars → $0.61 CPI-adjusted to 2024) × 1.3× cone-in-shell complexity multiplier (from Norreys HiPER conceptual design qualitative assessments). This is the only quantitative cost figure in the dossier and is critical for CAS80 fuel-cycle OPEX estimation (though CAS80 is not overridable). The patch explicitly notes it should be superseded if Focused Energy publishes a per-target cost.

3. **LaserFocusWorld** (2021) — "Can high-rep-rate lasers enable inertial fusion energy?"
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/laserfocusworld-lasers-sources-article-14274951-can-high.md`
   **Contribution:** Describes Focused Energy's two-pulse architecture: "focusing long-pulse lasers onto the pellet to compress it, blasting it with a 150 kJ short-pulse laser, and then hitting a nearby target to produce a burst of protons that ignites the pellet." Cites Todd Ditmire's Texas Petawatt heritage and National Energetics' ELI Beamlines delivery as background for the ignitor laser. Projects "around 80 beamlines" as an ultimate facility scale (Ditmire's estimate, not a committed Focused Energy design). This source provides the 150 kJ short-pulse ignitor specification, which is not stated in Focused Energy's own materials and carries lower confidence.

4. **PRNewswire** (2024) — "Focused Energy and Amplitude enter $40M partnership".
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/prnewswire-news-releases-focused-energy-and-amplitude-enter.md`
   **Contribution:** Announces $40M Amplitude DPSSL partnership and $65M Laser Development Facility in the San Francisco Bay Area. Confirms diode-pumped solid-state laser as the compression driver technology. Mentions DOE milestone-program work on "igniting the fusion fuel using laser-accelerated protons" and CSU proton-acceleration experiments. This source establishes the DPSSL compression driver and the proton-ignition pathway as company-committed directions.

5. **Focused Energy — Technology page** (date not in file; likely 2023–2024).
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-01/sources/focused-energy-technology.md`
   **Contribution:** Confirms D-T fuel, direct-drive proton fast ignition branding, and Pearl™ capsule name. States Pearl™ targets "will increase output +30x compared to the current NIF indirect drive fuel system." This is the only quantitative performance claim on the company website but is a relative improvement (vs NIF) rather than an absolute yield/shot specification. Emphasizes "manufacturability, with components that can be mass-produced and easily shipped" and "modulatory creates the highest reliability and serviceability of any fusion system" (qualitative claims without supporting data).

6. **HYLIFE-II energy conversion notes** (OSTI bibliographic record; full report not extracted).
   `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-02/sources/hylife-energy-conversion-notes.md`
   **Contribution:** OSTI catalog entry for UCRL-CR-105908 (1991). Identifies FLiBe as primary coolant, IHX's, steam generators, and balance-of-plant for HYLIFE-II (thick liquid wall IFE chamber design). This is not a Focused Energy-specific source but provides IFE chamber and BOP context. The full report was not successfully extracted (file contains only the bibliographic metadata).

7. **Focused Energy — Dossier summary** (internal research consolidation, 2026-05-19).
   `knowledge/concept_research/17b-laser-icf-fast-ignition/dossier.md`
   **Contribution:** Consolidated summary of all sources, differentiation table values with confidence assessments, and provenance notes. This is the structured research layer that synthesizes the individual sources above. Notes the 2026-05-19 split from the former shared `17-laser-icf-direct-drive` dossier (which also included Xcimer Energy before Xcimer was reclassified to hybrid drive). Identifies remaining gaps (blanket chemistry, quantitative plant parameters, proton fast ignition experimental validation).

**Sources cited but not yet ingested:**
- Focused Energy J. Fusion Energy 2023 (Springer paywall) — likely the best public single-source for blanket chemistry, chamber architecture, and plant parameters. Cited in external references but not in the local corpus.
- Meier, W. R. (2006) — "Target factory economics for inertial fusion energy," HYLIFE-II program documentation, LLNL. This is the anchor for the analyst patch's $0.30–$0.50 symmetric capsule baseline but has not been directly ingested. The analyst patch cites it, and the citation is trusted, but the original Meier source is not in `iter-04/sources/`.

**Academic context sources (not Focused Energy-specific but relevant to fast ignition physics):**
- Tabak et al. (1994) — seminal fast ignition proposal.
- Roth et al. (2001) — proton beam generation via TNSA.
- Norreys et al. (HiPER conceptual design, 2007–2012) — cone-in-shell fast ignition European program.
- Temporal et al. (2002) — proton beam coupling simulations.

These are referenced in the analysis for physics context but are not in the local source tree and were not directly read for this analysis.
