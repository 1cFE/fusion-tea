## Design Point

- Name: Z-IFE reference plant, 10-chamber 0.1 Hz baseline (Olson et al. 2006, SAND2006-7148)
- Maturity: paper-concept
- P_native: 1000 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/07-maglif/iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md
  - knowledge/concept_research/07-maglif/iter-01/sources/z-ife-power-plant-concept.md

## 1. Availability of Data

**Rating: Moderate**

MagLIF has a substantial body of peer-reviewed literature from Sandia National Laboratories, where the concept was proposed (Slutz et al., 2010) and has been experimentally investigated since 2013. Over 70 integrated MagLIF experiments have been conducted on the Z machine, documented in high-quality publications. The multi-institutional roadmap paper by Ellison et al. (2025) — jointly authored by Pacific Fusion, Sandia, LLNL, LANL, and U. Rochester — provides the most detailed public technical assessment of pulsed magnetic fusion energy scaling and commercialization.[^1]

However, the **power plant design literature is sparse and dated**. The most detailed reactor concept study is the Z-IFE program (SAND2006-7148, Olson et al. 2006), which predates the modern MagLIF concept itself and was based on older dynamic hohlraum targets and LTD driver architecture — not the impedance-matched Marx generators (IMGs) that Pacific Fusion is pursuing. The Z-IFE study includes a systems-level cost model, a detailed LTD driver cost analysis ($372M median for a 1 PW driver), thermal cycle evaluation, thick-liquid-wall chamber design, and fatigue analysis for F82H steel chamber structures.[^2]

> "The original SNL reference design for a Z-IFE power plant consisted of ten chambers each producing ~100 MWe net power for a total plant power of ~1000 MWe"
> — z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3

Pacific Fusion has disclosed high-level architecture details through press releases, interviews, and a founders' letter, but no detailed power plant design study or bottom-up cost estimate has been published for the modern IMG + self-magnetizing target architecture. The Fusion Report interview provides the most detailed Pacific Fusion demonstration system (DS) specifications: 156 modules, ~80 MJ stored energy, >60 MA, 6 m insulator stack diameter.[^3] Fuse Energy Technologies is covered in a Not Boring deep-dive with TITAN I specifications (238 bricks, 0.8 MA, 1.6 MV, 1 TW peak) and Apeiron I hybrid fusion-fission concept.[^4]

**Key data gaps:**
- No published power plant study exists for the modern MagLIF + IMG architecture
- No systems code outputs analogous to ARIES/PROCESS for tokamaks exist for MagLIF
- No published tritium breeding blanket design specific to a MagLIF chamber
- No published first-wall lifetime or maintenance schedule estimates for pulsed MagLIF operation
- No bottom-up capital cost estimate for an IMG-based driver at power-plant scale
- Per-shot target + RTL fabrication costs at volume production are unknown

[^1]: arxiv-2408-15206-pulsed-magnetic-fusion.md §1, §3, §7
[^2]: z-ife-sand2006-7148-thermal-cycles.md §3.1 (Systems Economic Modeling)
[^3]: pacific-fusion-interview-fusion-report.md §The Architecture of the Pacific Fusion DS
[^4]: fuse-energy-not-boring-details.md §The TITAN Path

## 2. Challenges in Capturing System Function

MagLIF presents distinctive LCOE modeling challenges rooted in its pulsed operation and the absence of modern plant-level design studies.

**1. Pulsed operation changes the cost structure fundamentally (highest impact).** Unlike steady-state concepts, MagLIF produces energy in discrete GJ-scale bursts at sub-Hz rates. Power output is directly proportional to rep rate × yield. Small changes in rep rate (0.1 Hz to 0.5 Hz) produce 5× changes in effective power output from the same driver, making this the single most leveraged LCOE parameter. The Z-IFE study confirms this:

> "Only the 1 and 3-chamber plants reach a COE less than 10 ¢/kWeh... The 10 unit, 0.1 Hz plant has a COE of ~20 ¢/kWeh, which is a factor of 2-3 higher than needed to compete with other fusion concepts."
> — z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6

**2. Per-shot consumables create an operating cost floor (high impact).** Each shot destroys the target liner, the recyclable transmission line (RTL), and in traditional MagLIF, the external magnetization coils. At the 10-chamber baseline (1 shot/s aggregate), this is ~31.5 million consumable sets per year. The Z-IFE study uses cast FLiBe RTLs as the baseline to reduce RTL remanufacturing energy:

> "A steel RTL however requires an extensive amount of energy (170 MWe of a 1000 MWe power plant) to remanufacture."
> — z-ife-sand2006-7148-thermal-cycles.md §3.4

Pacific Fusion's self-magnetizing targets (plastic + aluminum, demonstrated on Z at 22 MA in February 2026) address the coil cost component, and they frame the traditional per-shot cost as a "showstopper":

> "the cost of the components destroyed far exceeds the value of the energy that would be released on each shot"
> — pacificfusion-updates-experimental-breakthrough-by-pacific/output.md

**3. Driver cost is a novel cost category (high impact).** The pulsed power driver (capacitor banks, switches, transmission lines) has no analogue in other fusion concepts. The Z-IFE study estimated $372M (median) for a single 1 PW LTD-based driver, with LTD cavities comprising 96% of the cost ($353M for 12,600 cavities at ~$28,000 median per cavity). Since each of the 10 chambers requires its own independent driver, total plant driver capital is 10× the per-chamber driver cost — though each 10-chamber driver is much smaller (lower energy/power) than a 1 PW driver. The systems model used $15/J delivered to pinch as a driver unit cost per chamber, derived from the claim that "current pulsed power machines cost ~$30/J and the linear transformer driver should be a factor of two lower."[^5] For the IMG architecture Pacific Fusion is pursuing, no published cost estimate exists.

**4. Yield scaling is extrapolated from simulation (medium-high impact).** Current Z machine experiments achieve modest yields at 20–27 MA. The Z-IFE gain curve (G = 30.15 × (E − 1.22)^2.038 for E > 1.22 MJ) is based on three dynamic hohlraum simulation cases, not MagLIF targets. Scaling to 60+ MA and GJ-class yields relies on 2D simulations. Cryogenic DT ice-layer targets — required for GJ yields — have never been experimentally tested on Z.[^6]

**5. Design-point vintage mismatch (medium impact).** The Z-IFE study (2006) predates the MagLIF concept (Slutz 2010) and used dynamic hohlraum targets, not MagLIF magnetized liner targets. The gain curves, target physics, and driver architecture (LTD, not IMG) do not directly describe the Pacific Fusion approach. The study remains the only published systems-level cost analysis for a Z-pinch-driven fusion power plant, making it the best available design point while acknowledging the mismatch.

[^5]: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.2
[^6]: arxiv-2408-15206-pulsed-magnetic-fusion.md §4.2

## 3. Maturity of Key Subsystems and Components

Subsystems listed in ascending order of maturity.

### Cryogenic DT ice-layer targets — TRL 1–2
**On paper only.** Simulations by Slutz & Vesey (2012) show that GJ-class yields require a ~100 μm cryogenic DT ice layer frozen onto the inner liner wall at <19 K. No cryogenic MagLIF target has been fabricated or tested on Z. NIF's cryogenic target system takes 15–20 hours per target; Sandia's MagLIF cryostat requires ~5 minutes per target. Mass production at 1 Hz (parallel batch cooling pipelines) has not been designed or costed. Pacific Fusion's self-magnetizing composite targets have only been demonstrated at room temperature; compatibility with cryogenic ice layers is not publicly addressed.[^7]

### Rep-rated chamber operations — TRL 1–2
**On paper only.** The Z-IFE study evaluated a thick liquid curtain chamber with a cycle time of ~1.9 seconds (~0.53 Hz), including RTL insertion, liquid wall reformation, and vacuum re-establishment. No prototype chamber has been built or operated at any rep rate. Chamber clearing after GJ-scale explosions, debris management, and vacuum reconditioning within ~1–10 seconds remain undemonstrated.[^8]

### Recyclable Transmission Line (RTL) — TRL 2–3
**On paper only.** Conceptual studies by Olson et al. (2003) established the RTL concept. The Z-IFE study proposed frangible FLiBe RTLs that "shatter following a shot and quickly become part of the coolant." RTL mass: ~130–250 kg depending on wall thickness. Insertion, alignment, and electrical connection at 60+ MA within ~1 second post-blast is a major unsolved robotics challenge. Ellison et al. note that PMFE has the advantage of "electrically coupling to the target at reduced alignment tolerances versus laser-based approaches."[^9]

### Tritium breeding blanket — TRL 2
**On paper only.** FLiBe (Li₂BeF₄) is the assumed blanket/coolant for Z-IFE. The Z-IFE study performed tritium permeation analysis (estimated 0.0467 g/year tritium losses through all ten chambers with 304 stainless steel piping at PRF=100), but no integrated blanket module has been designed or tested for a MagLIF chamber. Tritium extraction from FLiBe at fusion-plant scale is undemonstrated.[^10]

### Thick liquid wall chamber — TRL 2–3
**On paper only.** The Z-IFE baseline uses a thick-liquid FLiBe curtain: pocket dimensions 3.5 m tall × 2.2 m diameter, with 1 m of FLiBe shielding all structures from neutrons, X-rays, and debris. University of Wisconsin and UC Berkeley conducted scaled water experiments on jet reformation timescales, showing compatibility with ~Hz operation at reduced blast loads. No experiments have been conducted with GJ-scale blasts, activated debris, or FLiBe at operating temperature (~850 K).[^11]

### Self-magnetizing composite targets — TRL 3
**Demonstrated.** Pacific Fusion tested composite liner targets (plastic + aluminum, 50 and 200 μm aluminum layers) on Z at 22 MA in 120 ns pulses (4 shots over 5 days, February 2026). B-dot probes confirmed magnetic field penetration without external coils. FLASH simulations accurately predicted target behavior. Fusion yield has not been demonstrated with these targets; next step is demonstrating elimination of laser preheating.[^12]

### MagLIF target physics — TRL 3–4
**Demonstrated.** Fusion-relevant conditions demonstrated on Z: nτ > 10²¹ keV m⁻³ s at ~3 keV ion temperature (2022 data). The concept achieved the second-highest Pτ value in laboratory history (3.6 bar-s), behind only NIF ignition shots. But this is far below ignition/gain thresholds. All experiments used gas-fill targets at 20–27 MA; the path to GJ yields at 60+ MA with ice-layer targets is simulation-based.[^13]

### Pulsed power driver (IMG architecture) — TRL 4–5
**Demonstrated at sub-scale.** The Z machine (27 MA) has operated reliably for decades with conventional Marx generators. The IMG concept, invented in 2017, was first demonstrated in the 4-stage, 8-brick Sirius-1 prototype at LLNL (60 GW). Pacific Fusion has built and tested modules (156 modules planned for DS, each ~1.9 m diameter, 320 bricks, ~0.5 MJ stored). Fuse Energy's TITAN I (238 bricks, 0.8 MA, 1.6 MV, 1 TW) has demonstrated >100 consecutive shots. Scaling to 60+ MA at plant scale remains a major step.[^14]

> "An IMG is a pulsed-power analog of a laser, with an energy efficiency of 90%."
> — arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2

### Energy conversion / balance of plant — TRL 6–7
**Mature technology.** The Z-IFE study evaluated four thermal cycles: supercritical CO₂ Brayton, steam Rankine, helium Brayton, and combined Brayton-Rankine. The combined cycle was recommended for highest efficiency. Baseline thermal-to-electric efficiency: 42% for steel chamber, 50% for carbon-composite chamber. The main uncertainty is coupling to a pulsed thermal source and managing thermal cycling at sub-Hz rates.[^15]

**O&M Considerations:** No published O&M cost breakdown exists for a MagLIF power plant. The Z-IFE study includes annual O&M costs in the COE calculation but does not decompose them into fixed vs. variable, scheduled maintenance, or unplanned outage categories. The per-shot consumable cost (target + RTL) is the dominant operating cost component, distinct from conventional O&M. Component replacement schedules for electrodes, power-feed structures, and chamber internals are not characterized.

[^7]: arxiv-2408-15206-pulsed-magnetic-fusion.md §4.2; z-ife-sand2006-7148-thermal-cycles.md §4.2.1
[^8]: z-ife-sand2006-7148-thermal-cycles.md §4.2.1
[^9]: arxiv-2408-15206-pulsed-magnetic-fusion.md §7.2
[^10]: z-ife-sand2006-7148-thermal-cycles.md §3.3
[^11]: z-ife-sand2006-7148-thermal-cycles.md §4.2.1, §4.1
[^12]: pacificfusion-updates-experimental-breakthrough-by-pacific/output.md; ans-news-2026-02-06-article-7739-fusion-simplification/output.md
[^13]: arxiv-2408-15206-pulsed-magnetic-fusion.md §4.2
[^14]: arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2; pacific-fusion-interview-fusion-report.md §Architecture
[^15]: z-ife-sand2006-7148-thermal-cycles.md §3.2

## 4. Key Materials and Supply Chain Considerations

### FLiBe (Li₂BeF₄) — blanket, coolant, and RTL material
FLiBe serves triple duty in the Z-IFE concept: neutron shielding, tritium breeding, and coolant. In the proposed frangible RTL concept, FLiBe is also the RTL material (shattering on each shot and reintegrating into the coolant). FLiBe is not currently produced at industrial scale. Beryllium, a component of FLiBe, is toxic and produced globally at ~300 tonnes/year, dominated by a single US producer (Materion Corp). Li-6 enrichment for tritium breeding is commercially available at small scale but not at fusion-fleet quantities. The Z-IFE study constrains FLiBe piping to 304 stainless steel at ≤850 K operating temperature to limit tritium permeation.[^16]

### Capacitors and switches — driver building blocks
The pulsed power driver is built from thousands of identical capacitor-switch "bricks." These use commodity materials (ceramics, metals, dielectrics) but require precision manufacturing. Ellison et al. identify the key commercialization requirements: "The cost of energy storage and switching must decrease by a factor of 5 to 10" and "The energy storage and switching component replacement lifespan must extend by at least a factor of 1000 at Hertz operating rate." Current capacitor costs are ~$5/J; the target is <$0.50/J. Current lifetimes are ~10⁴ shots; the target is ~10⁹ shots (~30 years at 1 Hz).[^17] Fuse Energy built 12 TITAN I components in-house at "10x cheaper and 4x faster than off-the-shelf components."[^18]

### Target materials — beryllium vs. composites
Traditional MagLIF uses beryllium (Be) cylindrical liners. Be is toxic, expensive (~$800/kg), and supply-constrained. Pacific Fusion's self-magnetizing targets use plastic and aluminum (50–200 μm aluminum), eliminating both beryllium and external copper coils from the per-shot bill of materials. At 28+ million shots/year, this material substitution has major supply-chain implications: aluminum and plastics are commodity materials with unlimited scalability; beryllium is not.[^19]

### Tritium
Standard D-T concern. Startup inventory (~1–5 kg at ~$30,000/g) required. The plant must breed tritium at TBR > 1. Global civilian tritium inventory is ~25 kg, decaying at 5.5%/year. The Z-IFE study estimated total tritium permeation losses of 0.0467 g/year across all ten chambers — "slightly less than 1/20th the total losses predicted for ITER."[^20]

### No HTS or exotic superconductors required
Unlike tokamak/stellarator concepts, MagLIF does not require REBCO tape, Nb₃Sn, or large superconducting magnets. The driver uses conventional electrical components. Pacific Fusion's website explicitly states the system "uses common materials, simplifying supply chains."[^21] This eliminates the most constrained supply chain bottleneck shared by most MFE concepts.

### F82H and chamber structural materials
The Z-IFE study uses F82H low-activation ferritic steel for the chamber structure (Fe-8%Cr-2%WVTa). F82H meets Class C low-level waste limits at all times and maintains reasonable strength up to 973 K. Operating temperature window is 673–823 K (avoiding both irradiation damage and creep). Fatigue analysis for 0.1 Hz pulsed loading showed that F82H can tolerate ~560 bar total strain for a 10-year design life with safety factor 3.5.[^22]

[^16]: z-ife-sand2006-7148-thermal-cycles.md §3.3, §3.4
[^17]: arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2.4
[^18]: fuse-energy-not-boring-details.md §Scaling TITANs
[^19]: pacificfusion-updates-experimental-breakthrough-by-pacific/output.md
[^20]: z-ife-sand2006-7148-thermal-cycles.md §3.3.1
[^21]: pacific-fusion-website-technology.md §Designed for pragmatic economics
[^22]: z-ife-sand2006-7148-thermal-cycles.md §4.2.3, §4.2.5

## 5. Design Point Parameters

The Z-IFE reference plant is a paper-concept from 2006 (SAND2006-7148), predating the MagLIF concept itself. It used dynamic hohlraum targets, not MagLIF magnetized liner targets. The following parameters describe the **10-chamber 0.1 Hz baseline** as published; the study also showed that fewer chambers at higher rep rate are more economical (see notes).

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Plant configuration | 10 chambers, each with independent driver, heat transfer, and power conversion; only heat rejection (cooling towers) and RTL/target factories shared | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3, §3.1.1.4 | high | Original SNL baseline; 10 independent drivers is critical for cost — total driver capital = 10 × per-chamber driver cost |
| Net electric power (P_native) | 1000 MWe | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3 | high | ~100 MWe per chamber; spec key: drives `P_native` |
| Repetition rate (per chamber) | 0.1 Hz | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | high | 1 shot/s aggregate across 10 chambers |
| Target yield (per shot) | 3–30 GJ range; ~4600 MJ at 42 MJ driver energy (optimized 1-chamber case at 0.5 Hz) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6, §2.1.1 | medium | Gain curve: G = 30.15 × (E − 1.22)^2.038 for dynamic hohlraum targets |
| Fusion power (aggregate) | ~1.6 GW (thick-liquid-curtain chamber at 3 GJ / 1.9 s per chamber) | z-ife-sand2006-7148-thermal-cycles.md §4.2.1 | medium | informational; `p_fus` is back-solved by library |
| Driver stored energy (per chamber) | ~20–60 MJ depending on configuration | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | 10-chamber baseline needs less per chamber; 1-chamber needs ~42 MJ |
| Driver architecture | LTD-based; detailed estimate describes a 1 PW reference driver (210 stacks × 60 LTD cavities = 12,600 total; 75 m × 10 m water tank) | z-ife-sand2006-7148-thermal-cycles.md §3.1.2 | high | The 1 PW reference driver is a standalone estimate; each of the 10 chambers has its own independent, smaller driver sized to per-chamber energy |
| Driver efficiency | 60% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.2 | medium | LTD-era assumption; IMG architecture claims ~90% |
| Driver unit cost | $15/J (delivered to pinch) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.2 | low | "based on statements by SNL researchers that current pulsed power machines cost ~$30/J and the LTD should be a factor of two lower" |
| Driver capital cost (detailed estimate, single 1 PW driver) | $372M median per driver (1 PW LTD) | z-ife-sand2006-7148-thermal-cycles.md §3.1.2 | medium | Per-driver cost, not total plant; 96% is LTD cavities ($28,000 median per cavity); 95th percentile: $862M. Not used by the systems model for COE calculation. |
| Thermal-to-electric efficiency | 42% (steel chamber); 50% (carbon-composite) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3 | high | Combined Brayton-Rankine recommended |
| Plant capacity factor | 85% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | medium | Fixed assumption in systems code |
| Indirect costs | 93.6% of total direct capital cost | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | medium | "consistent with other fusion economic studies" |
| Fixed charge rate | 9.66% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | medium | Standard fusion study assumption |
| Chamber geometry | Thick-liquid FLiBe curtain; pocket 3.5 m tall × 2.2 m diameter; 1 m FLiBe shielding | z-ife-sand2006-7148-thermal-cycles.md §4.2.1 | high | All structures shielded from neutrons |
| Chamber structural material | F82H low-activation ferritic steel | z-ife-sand2006-7148-thermal-cycles.md §4.2.3 | high | Operating window 673–823 K |
| FLiBe operating temperature | ~850 K (~100 K above freeze point of 733 K) | z-ife-sand2006-7148-thermal-cycles.md §3.3.1 | high | |
| RTL material (baseline) | Cast frangible FLiBe | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.4 | medium | Preferred over steel to avoid 170 MWe remanufacturing penalty |
| RTL mass | ~130–250 kg per shot | z-ife-sand2006-7148-thermal-cycles.md §4.2.1 | medium | Depends on wall thickness (1–2 mm) |
| RTL inductance | 15 nH out to 2 m radius | z-ife-sand2006-7148-thermal-cycles.md §4.2.1 | high | |
| Target type | Dynamic hohlraum (not MagLIF) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.1 | high | Z-IFE predates MagLIF; gain curve applies to dynamic hohlraum |
| Target capsule cost basis | 2× laser IFE capsule cost (GA study), to account for dynamic hohlraum | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.4 | low | No specific $/shot figure extracted |
| Tritium permeation (all 10 chambers) | 0.0467 g/year | z-ife-sand2006-7148-thermal-cycles.md §3.3.1 | medium | 304 SS piping with PRF=100 |
| COE (10-chamber baseline at 0.1 Hz) | ~20 ¢/kWeh (2005 dollars) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | |
| COE (optimized 1-chamber at 0.5 Hz) | 7.0 ¢/kWeh (2005 dollars) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Requires 42 MJ driver energy, ~4600 MJ yield |
| p_input_MW | [inferred: ~80–130 MW continuous for capacitor recharging at 1 Hz; at 0.1 Hz per chamber, ~8–13 MW per chamber] | [inferred from stored energy / rep rate; handwritten analysis §Rep Rate Constraints] | low | spec key: `p_input` — recirculating power for driver recharge, not fusion power |

**Notes on MagLIF-era vs. Z-IFE-era differences:** The Z-IFE gain curve and target physics are for dynamic hohlraum targets, not MagLIF magnetized liner targets. MagLIF at equivalent driver current is expected to produce different (potentially higher) yields due to magnetic insulation of the fuel. Pacific Fusion's IMG-based driver would have ~90% efficiency (vs. 60% for LTD), substantially changing the recirculating power and net electric output calculations. These differences mean the Z-IFE design point should be treated as an indicative envelope, not a precise description of the Pacific Fusion architecture.

**Note on driver multiplicity:** The 10-chamber baseline requires 10 independent pulsed-power drivers (one per chamber). The $372M detailed cost estimate in §3.1.2 is for a single 1 PW driver — a reference-scale unit developed independently from the systems model. The systems model's COE calculations use $15/J × per-chamber driver energy, applied independently to each chamber. Total plant driver capital is 10× the per-chamber driver cost, which is a major reason the 10-chamber configuration is uneconomic (~20 ¢/kWeh vs. ~7 ¢/kWeh for a single-chamber plant at 0.5 Hz).

## 5b. Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier:** The Z-IFE study uses a thick-liquid FLiBe curtain serving as blanket, neutron shield, and first wall protection simultaneously. This integrated liquid-wall architecture is fundamentally different from the solid first-wall + blanket modules assumed by the library for most archetypes. However, no company-grounded dollar figure for the blanket/first-wall system is published. The Z-IFE cost scaling uses Osiris-based models escalated to 2005 dollars without extracting a standalone blanket cost figure. **No override — no company-grounded cost figure available.**

**C220102 — Radiation shield:** The thick FLiBe liquid wall (1 m) provides neutron shielding as an integrated function of the blanket/coolant system, not as a separate structural shield. No separate shielding cost figure is published. **No override.**

**C220103 — Confinement magnets / coils:** MagLIF uses no external superconducting confinement magnets. Traditional MagLIF uses conventional copper Helmholtz coils for pre-magnetization, destroyed per shot (a consumable, not a capital item). Pacific Fusion's self-magnetizing targets eliminate even these coils. The library default for this archetype should already handle the absence of superconducting magnets. **No override.**

**C220104 — Supplementary plasma heating / primary pulsed driver (laser preheat):** Traditional MagLIF uses a kJ-class laser for preheat. Pacific Fusion is working to eliminate laser preheat entirely. The Z-IFE study does not use laser preheat (dynamic hohlraum targets). No company-grounded cost figure for a laser system is published for this design point. **No override.**

**C220105 — Primary structure:** The Z-IFE study specifies F82H steel chamber structure but does not publish a standalone structural cost figure. Osiris-derived cost models are embedded in the systems code. **No override.**

**C220106 — Vacuum system:** The Z-IFE chamber outside the RTL "does not need to be under vacuum" (only the RTL interior requires vacuum). This is architecturally distinct from tokamak vacuum vessels, but no cost figure is published. **No override.**

**C220107 — Pulsed-power capacitor bank:** This is the dominant driver cost. The Z-IFE study provides two cost models: (1) a systems-code formula of $15/J delivered to the pinch, applied per chamber; and (2) a detailed bottom-up cost estimate for a standalone 1 PW LTD-based driver: **$372M median** (12,600 LTD cavities at $28,000 median each, comprising 96% of driver cost), with scaling C_tot = 372 × (TW/1000)^0.6 in $M (2004 dollars).[^c107a]

Critically, the 10-chamber baseline has **10 independent drivers** — one per chamber:

> "Consistent with previous SNL conceptual designs, each chamber is assumed to have an independent driver, heat transfer system and power conversion system. Only the heat rejection system (e.g., cooling towers) is shared in chamber plants."
> — z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3

The $372M figure is for a single 1 PW driver — a much larger unit than any individual 10-chamber driver. Each of the 10 chambers requires a smaller driver (lower energy per shot at 0.1 Hz), and the per-chamber driver energy for the 10-chamber case is shown in Figure 3.3 but not stated numerically in text. The systems model's actual COE calculation used $15/J × per-chamber energy × 10 chambers, not the $372M figure (which was developed separately as a detailed estimate and "not received" for integration into the systems code at the time of the report).[^c107b]

Neither the $15/J parametric unit cost nor the $372M single-driver estimate provides a directly applicable total driver cost for the 10-chamber baseline. The $15/J is a researcher-estimated parametric assumption (not a company-grounded cost), and the $372M applies to a different (single, larger) driver than what any of the 10 chambers uses. **No override — no extractable company-grounded total driver cost for the 10-chamber baseline is available.**

[^c107a]: z-ife-sand2006-7148-thermal-cycles.md §3.1.2, §3.1.1.2
[^c107b]: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.2 ("The Z-IFE systems code does not have a detailed model for the pulsed power driver. At this point the driver cost is simply given as the product of the energy delivered to the pinch (J) times a unit cost expressed in $/J.")

**C220108 — Target factory:** The Z-IFE study includes target and RTL factory costs in the systems model, based on General Atomics' direct-drive laser IFE capsule cost study with a 2× multiplier for the dynamic hohlraum. However, the specific dollar figure for the target factory capital cost is not extracted as a standalone number in the report — it is embedded in the Osiris-derived systems code. No company-grounded standalone target factory cost is published. **No override — the factory cost is part of the integrated systems model, not an extractable standalone figure.**

**C220109 — Direct energy converter:** The Z-IFE design point does not use direct energy conversion. Energy capture is thermal (Brayton-Rankine combined cycle). **Not applicable for this design point; no override.**

**C220110 — Remote handling & maintenance:** No published figures. **No override.**

**C220111 — Reactor-equipment installation:** No published figures. **No override.**

**CAS21 — Buildings & site structures:** The Z-IFE driver requires a "large (75 m diameter by 10 m high) water tank" for the pulsed power system, which is architecturally distinct from tokamak buildings. However, the building cost is embedded in the Osiris-derived systems model without an extractable standalone figure. **No override.**

**CAS23 — Turbine plant equipment:** Thermal cycle; baseline 42% efficiency with steel chamber. Combined Brayton-Rankine recommended. Standard commercial technology. **No override — library default thermal cycle pricing is appropriate.**

**CAS24 — Electric plant equipment:** No specific published figures. **No override.**

**CAS26 — Heat rejection system:** Shared across chambers in the Z-IFE design. No specific published cost. **No override.**

**CAS27 — Special materials (initial FLiBe inventory):** FLiBe serves as coolant, tritium breeder, neutron shield, and (in the frangible RTL concept) the RTL material itself. The Z-IFE study uses FLiBe throughout but does not publish a standalone initial inventory cost. No company-grounded figure for FLiBe $/kg at scale is published in this dossier. **No override.**

**CAS70 — Annualized O&M:** The Z-IFE study includes annual O&M in the COE calculation but does not decompose it. No standalone O&M cost figure is extractable. **No override.**

**CAS80 — Annualized fuel cost:** D-T fuel cost is negligible for all D-T concepts. Per-shot consumable costs (target + RTL) are the dominant operating cost for MagLIF but are structurally different from "fuel cost" — they are manufacturing costs, not isotope procurement. No company-grounded per-shot cost figure is published for the Z-IFE design point. **No override.**

### Override Count Assessment

**0 enabled overrides.** The archetype-fit grade is High, with an expected band of 0–4 overrides. Zero overrides is consistent with this band.

Despite the Z-IFE study containing substantial cost analysis, no override is justified because: (1) the $372M detailed driver cost estimate applies to a single 1 PW driver, not to any of the 10 smaller independent drivers in the baseline plant; (2) the systems model's $15/J unit cost is a researcher-estimated parametric assumption rather than a company-grounded cost; (3) all other subsystem costs (chamber, BOP, target factory) are embedded in the Osiris-derived systems code without extractable standalone figures. The library defaults stand for all accounts.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published power plant study for modern MagLIF + IMG architecture (Pacific Fusion) | S1, S2 | truly-unknown | blocking | Await Pacific Fusion plant study publication or ARPA-E project reports |
| 2 | Yield scaling from 20 MA (demonstrated) to 60+ MA (required) unvalidated experimentally; gain curve based on dynamic hohlraum, not MagLIF targets | S2, S5 | truly-unknown | blocking | Track Pacific Fusion DS commissioning results (~2030); watch for Sandia Z-machine upgrades |
| 3 | Per-shot target + RTL cost at volume production unknown; no published $/shot for MagLIF-era targets | S2, S4 | truly-unknown | blocking | General Atomics target fabrication studies; Pacific Fusion manufacturing partnerships |
| 4 | Cryogenic DT ice-layer target fabrication never demonstrated for MagLIF; mass production cost and pipeline design unknown | S3 | truly-unknown | blocking | Track Sandia cryogenic target program; NIF target fabrication literature for analogues |
| 5 | IMG driver cost at power-plant scale not published; only LTD cost available ($372M per single 1 PW driver, 2004$); total plant driver cost for 10-chamber baseline not extractable | S2, S5 | not-yet-sourced | important | Pacific Fusion cost disclosures; pulsed power industry cost benchmarks |
| 6 | Chamber lifetime under combined pulsed shock + neutron + thermal cycling + FLiBe corrosion is uncharacterized | S3 | truly-unknown | important | Materials testing programs for F82H under combined loading environments |
| 7 | Electrode and power-feed structure lifetime at axial openings (direct neutron exposure + blast loading) | S3 | truly-unknown | important | Engineering design studies; there is no experimental analogue |
| 8 | Tritium breeding blanket design specific to MagLIF chamber — no published design exists | S3 | not-yet-sourced | important | Z-IFE follow-on studies; FLiBe blanket R&D (shared with molten salt fission) |
| 9 | O&M cost breakdown (fixed vs. variable, scheduled maintenance, component replacement schedule) | S3 | not-yet-sourced | important | Analogue from Z-IFE or laser IFE plant studies |
| 10 | FLiBe initial inventory cost at scale; FLiBe industrial production not established | S4 | not-yet-sourced | nice-to-have | Kairos Power FLiBe procurement data; ORNL FLiBe production studies |
| 11 | Self-magnetizing target compatibility with cryogenic ice-layer operation unknown | S3 | truly-unknown | important | Await Pacific Fusion experimental results |
| 12 | Thermal buffering cost for pulsed thermal source to turbine coupling not characterized | S2 | derivable | nice-to-have | IFE thermal hydraulics literature; Z-IFE follow-on studies |

## 7. Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

The Z-IFE/MagLIF concept occupies a unique position in the landscape: it is the only pulsed-power-driven magneto-inertial fusion (MIF) concept under analysis. It shares some architectural features with laser ICF concepts (pulsed operation, per-shot consumables, liquid-wall chamber) but diverges fundamentally in driver technology (electrical vs. optical), target coupling (physical RTL vs. free-flight + laser beams), and rep-rate regime (sub-Hz vs. 1–10 Hz). It shares the D-T fuel cycle and thermal energy conversion pathway with most MFE concepts but has no superconducting magnets, no steady-state plasma, and no divertor.

The key distinguishing features that would drive cost deltas against any future comparable:
- **Driver modularity**: The pulsed power driver is built from thousands of identical capacitor-switch bricks amenable to mass manufacturing, unlike the bespoke superconducting magnets of tokamaks/stellarators or the precision optics of laser ICF.
- **No superconducting magnets**: Eliminates the HTS supply chain constraint entirely. This is a cost advantage relative to any MFE concept.
- **Per-shot consumables**: Creates a fundamentally different operating cost structure. At 28M+ shots/year, even small per-unit target/RTL costs dominate OPEX.
- **Thick liquid wall**: If validated, eliminates periodic blanket replacement that dominates tokamak availability projections (10–20% of lifetime in DEMO studies).
- **Rep rate as dominant LCOE lever**: No other concept type has a single parameter with comparable LCOE leverage (~10× change from 0.1 Hz to 1 Hz).

## 8. Sources

1. **z-ife-sand2006-7148-thermal-cycles.md** — Z-IFE Power Plant Final Report FY 2006 (SAND2006-7148), Sandia National Laboratories. The primary design-point source: systems cost model, LTD driver cost analysis ($372M), thermal cycle evaluation, thick-liquid-wall chamber design, F82H fatigue analysis, tritium permeation study. Found in: knowledge/concept_research/07-maglif/iter-02/sources/.

2. **arxiv-2408-15206-pulsed-magnetic-fusion.md** — Ellison et al., "Opportunities in Pulsed Magnetic Fusion Energy," Phys. Plasmas 32, 090601 (2025). Multi-institutional roadmap paper (Pacific Fusion, Sandia, LLNL, LANL, U. Rochester). IMG architecture, MagLIF scaling physics, engineering challenges, commercialization requirements. Found in: knowledge/concept_research/07-maglif/iter-01/sources/.

3. **pacificfusion-updates-experimental-breakthrough-by-pacific/output.md** — Pacific Fusion blog post (February 2026). Self-magnetizing composite target demonstration on Z (22 MA, 120 ns, 4 shots). Plastic + aluminum targets eliminate external coils. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

4. **pacific-fusion-interview-fusion-report.md** — Pacific Fusion interview in The Fusion Report. Detailed DS specifications: 156 modules, ~80 MJ stored energy, >60 MA, 6 m insulator stack, deionized water tank. Found in: knowledge/concept_research/07-maglif/iter-02/sources/.

5. **fuse-energy-not-boring-details.md** — Packy McCormick, Not Boring deep-dive on Fuse Energy Technologies. TITAN I specifications, Z STAR plans, Apeiron I hybrid concept, capacitor lifetime framing, in-house manufacturing cost advantages. Found in: knowledge/concept_research/07-maglif/iter-02/sources/.

6. **z-ife-power-plant-concept.md** — Derzon et al., "Z-pinch power plant concept" (SAND2000-3132J). OSTI abstract only: 4 m radius chamber, 80 cm FLiBe blanket, 6061-T6 Al chamber wall, 0.01–0.1 Hz rep rate, 1–30 GJ yields. Found in: knowledge/concept_research/07-maglif/iter-01/sources/.

7. **ans-news-2025-04-24-article-6980-pacific-fusion-fusing/output.md** — Nuclear News article (April 2025). Pacific Fusion DS specs: ~2 TW per module, ~250 MWe hypothetical power plant, GA collaboration for cryogenics and target fabrication, ~90% IMG energy delivery efficiency. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

8. **ans-news-2026-02-06-article-7739-fusion-simplification/output.md** — Nuclear News article (February 2026). Coverage of self-magnetizing target breakthrough. Targets made of plastic and aluminum; exploring different metallic conductors and ceramics. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

9. **pacific-fusion-website-technology.md** — Pacific Fusion website technology page. Three-part architecture (pulser, chamber, fuel containers), "common materials" emphasis, net facility gain target. Found in: knowledge/concept_research/07-maglif/iter-01/sources/.

10. **pacificfusion-updates-founders-letter/output.md** — Pacific Fusion founders' letter (October 2024). Brick-module architecture, $900M+ Series A, IMG first demonstrated at LLNL in 2022. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

11. **fuse-energy-technology.md** — Fuse Energy website. TITAN (1 TW IMG) and Z-Star (15 TW) milestones, 3,000 shots, brick inductance 150 nH. Found in: knowledge/concept_research/07-maglif/iter-01/sources/.

12. **pacificfusion-updates-crada-sandia-national-laboratories/output.md** — Pacific Fusion CRADA announcement (December 2024). Collaboration with Sandia on pulser architectures and high-yield operation. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

13. **arxiv-2602-19389/output.md** — Woodruff Scientific, "Extension of the Fusion Power Plant Costing Standard" (CATF IWG, Feb 2026). Defines MIFE pulsed-power cost accounts (22.1.3 Driver, 22.1.7 Power Supplies). Methodology paper, no concept-specific LCOE numbers. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.

14. **frontiersin-journals-nuclear-engineering-articles-10-3389/output.md** — Pettinari et al., "Assessment of structural materials in compact fusion reactor design" (Frontiers in Nuclear Engineering, 2025). Blanket material TBR values with enriched FLiBe (0.90–1.25 range); V-4Cr-4Ti highest TBR (1.26). Not MagLIF-specific but relevant to blanket material selection. Found in: knowledge/concept_research/07-maglif/iter-03/sources/.
