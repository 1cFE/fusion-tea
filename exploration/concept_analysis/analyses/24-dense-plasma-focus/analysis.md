---
ID: 24-dense-plasma-focus
Concept: Dense Plasma Focus (LPP Fusion)
Company: LPPFusion
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: MFE
Archetype: DENSE_PLASMA_FOCUS
Archetype-Fit: Low
Comparison-Status: costingfe-asterisked
Comparables: []
Design-Point-Name: Focus Fusion commercial generator (Lerner et al. 2023)
Design-Point-Maturity: paper-concept
P-Native: 5.0
Grounding-Confidence: low
---

## Design Point

- Name: Focus Fusion commercial generator (Lerner et al. 2023)
- Maturity: paper-concept
- P_native: 5.0 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md
  - knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md

## Section 1: Availability of Data

**Rating: Limited**

The Dense Plasma Focus (DPF) concept as pursued by LPPFusion has a small but non-trivial body of publicly available technical information, concentrated almost entirely in the company's own publications and website. Two peer-reviewed papers provide the bulk of the quantitative foundation:

- **Lerner et al. (2023)**, "Focus Fusion: Overview of Progress Towards p-B11 Fusion with the Dense Plasma Focus," *J. Fusion Energy* 42:7 — the most comprehensive source, covering experimental results from FF-2B with deuterium, the theoretical framework (including the quantum magnetic field effect), and a conceptual description of the commercial generator.[^1]
- **Lerner et al. (2024)**, "Preparations for pB11 tests in the FF-2B dense plasma focus," *Frontiers in Physics* — describes preparations for the fuel transition to decaborane, radiation safety analysis, and diagnostic plans.[^2]

Several LPPFusion website pages provide supplementary detail on the commercial vision, including an investment-oriented "Plan to Net Energy" roadmap and an executive summary.[^3][^4] These are company-authored promotional materials without independent verification.

> "With large-scale mass production, the capital cost of a Focus Fusion generator unit will be in the area of $500,000 or $0.10 per W"
> — lerner-2023-jfe-paper.md, §Cost and Transition

The DPF device itself has a broader academic literature spanning six decades (the device was invented in 1964), but essentially no independent cost studies, no power plant conceptual design studies, and no systems-code analyses exist for the Focus Fusion concept. No independent researchers have published analyses of the commercial generator design. There are no plant-level cost breakdowns — the $500,000 capital cost and $0.003/kWh LCOE claims are top-level assertions without supporting decomposition.

**Key data gaps:**
- No subsystem cost breakdown (capacitor bank, electrodes, energy conversion, BOP)
- No independent engineering assessment of the commercial generator concept
- No plant study, systems code output, or CAS-level cost decomposition
- No experimental data with p-B11 fuel (all results are deuterium)
- No demonstrated energy conversion system of either type (ion beam decelerator or x-ray photoelectric)
- No demonstrated repetitive pulsed operation
- No capacity factor, availability, or maintenance schedule estimates

[^1]: lerner-2023-jfe-paper.md
[^2]: lerner-2024-frontiers-pB11-prep.md
[^3]: lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md
[^4]: lppfusion-investing-in-lppfusion-executive-summary/output.md

## Section 2: Challenges in Capturing System Function

The Focus Fusion concept presents exceptional modeling challenges — arguably the most severe of any concept in the corpus. The challenges stem from (1) the extreme extrapolation required from current experimental results to commercial claims, (2) the reliance on unverified physics (the quantum magnetic field effect), and (3) the complete absence of engineering data for critical subsystems.

### Challenge 1: Six-Order-of-Magnitude Yield Extrapolation (Unique, Blocking)

The best demonstrated fusion energy release from FF-2B is **0.2 J per shot** with deuterium fuel.[^5] The commercial design point requires **~60 kJ per shot** — a factor of **300,000×**. LPPFusion's scaling argument chains multiple independent multiplicative factors:

- 75× from improved compression (reducing plasmoid radius from 250 μm to ~50 μm)
- 16× from current increase (1 MA → 2.4 MA, assuming I⁴ scaling)
- 100× from switching to p-B11 fuel (composed of 2× burn rate, 3× energy per reaction, ~2× density improvement, 4× longer confinement)

> "These three improvements will increase the fusion yield by a factor of 120,000"
> — lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md

Each multiplier individually relies on physics that is either undemonstrated at the required scale or theoretically contested. The I⁴ scaling law has explicitly **plateaued above 1 MA** in all DPF devices worldwide — the very regime where LPPFusion needs it to hold.[^6] No other fusion concept in the corpus requires a comparable extrapolation from demonstrated to commercial performance.

**Uncertainty range:** The yield gap spans six orders of magnitude. Even optimistic assumptions about individual scaling factors carry multiplicative uncertainty — if any single factor achieves 50% of its projected value, the commercial design point fails.

### Challenge 2: Unverified Enabling Physics — Quantum Magnetic Field Effect (Unique, Blocking)

The entire Focus Fusion concept with p-B11 fuel depends on the quantum magnetic field effect (QMFE), which theoretically reduces bremsstrahlung losses by quantizing electron energy levels in extremely strong magnetic fields (>1 GG). Without QMFE, bremsstrahlung from the high-Z boron ions would prevent net energy.[^7]

> "such a device has never been made, although the principles of photoelectric vacuum tubes are well known"
> — lerner-2023-jfe-paper.md, §Energy Capture

The QMFE has been studied theoretically since the 1970s in the context of neutron star physics, but it has **never been experimentally verified in any laboratory plasma**. The magnetic field strengths required (~1–10 GG) are claimed to exist inside DPF plasmoids based on theoretical models, but have not been directly measured. LPPFusion's own simulations are 0-D (uniform sphere), acknowledged as "not fully realistic."[^8]

**Modeling consequence:** The QMFE is a binary gate — if it operates as predicted, p-B11 ignition may be possible in a DPF; if it does not, the concept fundamentally cannot work with aneutronic fuel. There is no gradual degradation path. This makes sensitivity analysis around QMFE essentially a scenario branch, not a parameter sweep.

### Challenge 3: No Demonstrated Energy Conversion System (Unique, Critical)

The commercial generator relies on two novel direct energy conversion channels, neither of which has been prototyped:

1. **Ion beam decelerator:** Converts ion beam kinetic energy to electricity via induced current in a coil. Claimed efficiency: up to 85% (based on accelerator beam technology, a different context). Requires fast diamond-film switches that LPPFusion acknowledges they "would probably have to bring to full development."[^9]

2. **X-ray photoelectric converter:** A multilayered foil device converting x-ray energy via the photoelectric effect. Claimed efficiency: ≥80% (calculated, never demonstrated). "Such a device has never been made."[^10]

**Modeling consequence:** The entire energy conversion pathway is theoretical. No demonstrated efficiency, no prototype, no materials qualification. The claimed ~83% combined conversion efficiency has no experimental basis. For cost modeling, the conversion subsystem cost is essentially unconstrained — no analogues exist.

### Challenge 4: Extremely Small Scale (5 MWe) Creates Unique CAS Difficulties

The 5 MWe design point is **200× smaller** than the typical fusion power plant (1 GWe). This creates fundamental difficulties for cost modeling in a CAS framework designed for utility-scale plants:

- Balance-of-plant costs do not scale linearly to 5 MWe — minimum viable site infrastructure, grid connection, and staffing represent fixed costs that dominate at small scale
- The 1costingFE library's per-MW scaling assumptions may not hold at this extreme
- At 5 MWe, Focus Fusion is in the range of distributed generation, not utility-scale power — the comparison framework itself may be inapplicable
- The concept envisions mass-produced, factory-built units "like automobiles" — a fundamentally different deployment model than any other fusion concept

[^5]: lerner-2023-jfe-paper.md, §Highest Wall-Plug Efficiency
[^6]: lerner-2023-jfe-paper.md, §Challenges — Yield Plateau
[^7]: lerner-2023-jfe-paper.md, §Quantum Magnetic Field Effect
[^8]: lerner-2023-jfe-paper.md, §Simulations of DPF Plasmoid Evolution
[^9]: lerner-2023-jfe-paper.md, §Energy Capture — Ion Beam
[^10]: lerner-2023-jfe-paper.md, §Energy Capture — X-rays

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### X-ray Photoelectric Energy Converter — On Paper Only (TRL 1)

A "highly multilayered photoelectric device" with thin metal foils converting x-ray energy to electron kinetic energy, captured on charged grids. Described as approximately 40–50 cm inner radius and 50 cm in length. Claimed efficiency ≥80%, based entirely on LPPFusion calculations. No prototype, no component testing, no experimental demonstration. The paper explicitly states this device "has never been made."[^11] No materials have been qualified for the x-ray fluence environment. No analogue exists in any industry — this is a wholly novel energy conversion concept.

### Ion Beam Decelerator — On Paper Only (TRL 1–2)

A coil or conductor geometry that captures the ion beam's kinetic energy by inducing current, transferred to capacitors via fast switches. General concept of beam energy recovery is mature in accelerator physics (TRL 5–6 for that application), but the DPF ion beam differs fundamentally: ~5 ns duration, ~120 kA peak current, multi-MeV energies, in a post-fusion debris environment. The required diamond-film switches (UV laser-triggered conversion of diamond from insulator to conductor) are at TRL 2–3 — the principle has been demonstrated in academic settings (LLNL diamond photoconductive switch at TRL 3, ~50 kW output)[^12], but nothing approaching the power levels, voltage ratings, or cycling rates needed.

### Repetitive Pulsed Operation at ~200 Hz — Not Demonstrated (TRL 1–2)

All FF-2B experiments are single-shot. The NX2 device (Singapore) has demonstrated 16 Hz repetition for DPF devices in an x-ray source application, but at much lower energy and with different electrode geometry. At 200 Hz with p-B11 fusion yields, electrode erosion, thermal management of the anode tip (requiring ~10 kW/cm² cooling), capacitor bank recharge, and vacuum re-establishment between shots are all unsolved.[^13] The capacitor bank charging power at 200 Hz would be ~12 MW continuous for a 60 kJ bank, which is 2.4× the net electric output — the recirculating power fraction for bank charging alone would need careful accounting.

### p-B11 Fusion in a DPF — Not Demonstrated (TRL 2)

No p-B11 fusion reactions have been demonstrated in any DPF device. All experimental results are with deuterium. Isotopically pure decaborane (B₁₀H₁₄, 99.9% B-11) has been procured and preparations are underway, but as of the latest publication (2024), the fuel transition has not occurred.[^14] The theoretical basis for p-B11 net energy in a DPF depends on the unverified QMFE (see Section 2).

### Plasmoid Compression and Confinement — Partially Demonstrated (TRL 2–3)

The FF-2B device has demonstrated plasmoid formation with:
- Record confined mean ion energy: 240 ± 20 keV[^15]
- Best confinement time: ~40 ns
- Best ion density: 3–4 × 10¹⁹/cm³
- Best nτT product: 3.4 ± 0.8 × 10²⁰ keV·s/m³
- Record plasma purity: z_eff = 1.004[^16]

However, the required density for net energy (~10²¹/cm³) has not been achieved simultaneously with high ion energy. The yield plateau above 1 MA — where fusion yield as a fraction of input energy ceases to improve — has persisted across all DPF devices worldwide for over 20 years.[^17]

### Capacitor Bank and Pulsed Power — Demonstrated (TRL 4–5)

The FF-2B capacitor bank (12 capacitors, 113 μF, max 45 kV, max 115 kJ stored energy) has operated reliably at up to slightly over 1 MA peak current. Switch improvements in 2023 achieved ~50% current increase. The bank is the most mature subsystem — DPF capacitor bank technology has decades of operational heritage across multiple laboratories worldwide. However, the commercial device requires ~2.7 MA, which has not been demonstrated.

### Electrode System (Beryllium Anode/Cathode) — Demonstrated at Experimental Scale (TRL 3–4)

Beryllium electrodes (anode radius 2.8 cm, cathode radius 5 cm) replaced earlier tungsten and copper designs. Beryllium provides critical advantages: near-transparency to x-rays at plasmoid energies (reducing anode heating), self-passivating oxide, and low atomic number (z=4) minimizing impurity impact.[^18] The electrode change achieved a 30-fold reduction in impurity contribution. However, electrode lifetime at commercial rep rates (~200 Hz, monthly replacement target) is completely undemonstrated. Beryllium is toxic and requires careful handling procedures.

[^11]: lerner-2023-jfe-paper.md, §Energy Capture — X-rays
[^12]: ipo-ipo-technologies-instruments-sensors-and-electronics/output.md
[^13]: lerner-2023-jfe-paper.md, §Energy Capture — Cooling
[^14]: lerner-2024-frontiers-pB11-prep.md, §Section 4
[^15]: lerner-2023-jfe-paper.md, §World-Record Confined Ion Energies
[^16]: lerner-2023-jfe-paper.md, §Achieving Near-Zero Impurities
[^17]: lerner-2023-jfe-paper.md, §Challenges — Yield Plateau
[^18]: lerner-2023-jfe-paper.md, §Electrode Changes

## Section 4: Key Materials and Supply Chain Considerations

### Beryllium (Electrodes)

The FF-2B uses beryllium electrodes, which are critical to device performance (x-ray transparency, low impurity impact). Current global beryllium production is ~400 tonnes/year. The Lerner 2023 paper states that a full Focus Fusion economy would require a ~10× scale-up of beryllium production.[^19] Beryllium is "not rare, being about as common as lead in the Earth's crust," but currently only rich ores are commercially exploited. At 5 MWe per unit with electrode replacement approximately monthly, the per-unit beryllium consumption would be modest (the electrodes are small — 2.8 cm radius anode), but a fleet of thousands of units would create aggregate demand.

Beryllium is toxic (inhalation of dust/fumes causes chronic beryllium disease), requiring specialized handling procedures and safety measures. This adds manufacturing and maintenance cost. The initial FF-2B beryllium installation required hand-polishing to remove oxide layers, producing toxic dust — not compatible with factory-scale production without significant engineering.

### Boron-11 (Fuel)

The fuel is decaborane (B₁₀H₁₄), requiring isotopically enriched boron-11 (99.9% B-11 vs. 80% in natural boron) to minimize radioactive Be-7 production from B-10 side reactions. Current supply is bespoke laboratory production: 93 grams of isotopically pure decaborane cost $56,000 (~$600/gram), sourced from Russia (isotope separation) and Czech Republic (chemical synthesis).[^20]

> "This extremely expensive fuel had to be produced by hand in laboratories"
> — lppfusion-proton-boron-p11b-fuel-arrives/output.md

At the commercial consumption rate of ~5 kg/year per 5 MWe unit, laboratory-scale fuel costs would be $3M/year — clearly not viable. LPPFusion claims mass production would reduce costs "many hundred-fold," but no mass-production process exists or has been costed. The isotopic enrichment step is the key cost driver; natural-abundance boron is cheap and abundant. The fuel supply chain is currently entirely dependent on foreign sources (Russia, Czech Republic) — a geopolitical vulnerability.

### Diamond-Film Switches (Energy Conversion)

The ion beam decelerator requires fast high-voltage switches, with diamond photoconductive semiconductor switches (PCSS) identified as the leading candidate. LLNL has a TRL 3 diamond PCSS achieving ~20% efficiency and ~50 kW output power.[^21] Academic research (University of Illinois) has demonstrated 44 A/cm current density at 60 V DC bias with ~2 ns switching times.[^22] Neither is close to the voltage (tens of kV), current (hundreds of kA), or cycling rate (~200 Hz) required. Diamond PCSS is an active research area but remains years from engineering application at fusion-relevant specifications.

### No Exotic Superconductors or Rare Materials

Unlike nearly every other fusion concept in the corpus, Focus Fusion requires no HTS tape (REBCO), no Nb₃Sn, no large superconducting magnets, no FLiBe, no enriched lithium-6, and no tritium. The device has no external magnets of any kind. The structural materials are conventional (stainless steel vacuum chamber, standard power electronics components). This is a genuine supply chain advantage — the critical materials are beryllium (electrodes) and isotopically enriched boron (fuel), neither of which is shared with other fusion concepts' supply chains.

[^19]: lerner-2023-jfe-paper.md, §Cost and Transition
[^20]: lppfusion-proton-boron-p11b-fuel-arrives/output.md
[^21]: ipo-ipo-technologies-instruments-sensors-and-electronics/output.md
[^22]: compoundsemiconductor-119149-us-team-reinvents-the/output.md

## Section 5: Design Point Parameters

The following table describes the Focus Fusion commercial generator as specified in Lerner et al. (2023) and the LPPFusion investment materials. All parameters describe the **named design point at native scale (5 MWe)**.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 5.0 MWe | lerner-2023-jfe-paper.md §Energy Capture | medium | spec key: `p_net`; drives P_native |
| Fusion yield per pulse | ~60 kJ | lerner-2023-jfe-paper.md §Current Experimental Challenges | low | Required for net energy; not demonstrated |
| Net electricity per pulse | ~25 kJ | lerner-2023-jfe-paper.md §Energy Capture | low | Implies ~42% net conversion from fusion yield |
| Repetition rate | ~200 Hz | lerner-2023-jfe-paper.md §Energy Capture | low | Design target; never demonstrated in any DPF at fusion-relevant conditions; spec key: `rep_rate` |
| Capacitor bank stored energy | ~115 kJ (max, FF-2B) | lerner-2023-jfe-paper.md §Experimental Device | medium | FF-2B value; commercial bank not separately specified |
| Peak current (design) | 2.7 MA | lerner-2024-frontiers-pB11-prep.md §Section 2 | medium | FF-2B design maximum; current demonstrated is ~1 MA |
| Anode radius | 2.8 cm | lerner-2023-jfe-paper.md §Experimental Device | high | FF-2B dimension; commercial may differ |
| Cathode radius | 5 cm | lerner-2023-jfe-paper.md §Experimental Device | high | FF-2B dimension |
| Plasmoid radius (demonstrated) | ~250 μm | lerner-2023-jfe-paper.md §Challenges | medium | Target for commercial: ~50 μm |
| Plasmoid density (demonstrated) | 3–4 × 10¹⁹ /cm³ | lerner-2023-jfe-paper.md §Highest nτT | medium | Target for net energy: ~10²¹ /cm³ |
| Plasmoid confinement time | ~40 ns | lerner-2023-jfe-paper.md §Highest nτT | medium | Best demonstrated |
| Ion temperature (demonstrated) | 240 ± 20 keV | lerner-2023-jfe-paper.md §World-Record Ion Energies | high | Record for any fusion device |
| nτT product (demonstrated) | 3.4 ± 0.8 × 10²⁰ keV·s/m³ | lerner-2023-jfe-paper.md §Highest nτT | medium | |
| z_eff (demonstrated) | 1.004 | lerner-2023-jfe-paper.md §Near-Zero Impurities | medium | Record plasma purity |
| Ion beam conversion efficiency | up to 85% | lerner-2023-jfe-paper.md §Energy Capture — Ion Beam | low | Based on accelerator beam analogues; not demonstrated for DPF beams |
| X-ray conversion efficiency | ≥80% | lerner-2023-jfe-paper.md §Energy Capture — X-rays | low | Calculated; device has never been built |
| Energy fraction as x-rays | ~1/3 of fusion energy | lerner-2023-jfe-paper.md §Energy Capture — X-rays | medium | |
| Device mass | ~3 tonnes | lerner-2023-jfe-paper.md §Energy Capture | low | Commercial estimate |
| Device volume | ~30 m³ | lerner-2023-jfe-paper.md §Energy Capture | low | Commercial estimate |
| Capital cost (unit) | ~$500,000 ($0.10/W) | lerner-2023-jfe-paper.md §Cost and Transition | low | Mass production estimate; no decomposition |
| Claimed LCOE | ~0.3 ¢/kWh | lerner-2023-jfe-paper.md §Cost and Transition | low | Company claim; no supporting analysis |
| Fuel consumption | ~5 kg/year | lerner-2023-jfe-paper.md §Cost and Transition | medium | Decaborane |
| Electrode replacement | ~monthly | lerner-2023-jfe-paper.md §Energy Capture | low | Target; not demonstrated |
| Anode tip cooling requirement | ~10 kW/cm² | lerner-2023-jfe-paper.md §Energy Capture — Cooling | medium | "High, but still feasible" per Lerner |
| Fuel type | p-B11 (decaborane, B₁₀H₁₄) | lerner-2023-jfe-paper.md §Fuel; lerner-2024-frontiers-pB11-prep.md §Section 2 | high | |
| Confinement concept | Dense plasma focus | dossier.md §Confinement Concept | high | |
| Operation mode | Pulsed | dossier.md §Operation Mode | high | |
| Magnet type | None (self-confined) | dossier.md §Magnet Type | high | |
| Energy capture | Direct (charged particle) | dossier.md §Energy Capture | high | Two channels: ion beam decelerator + x-ray photoelectric |
| Blanket config | N/A (no tritium) | dossier.md §Tritium Breeding | high | p-B11, aneutronic |
| Thermal efficiency (eta_th) | 0.0 | [inferred: no thermal cycle; all energy conversion is direct] | high | spec key: `eta_th = 0.0` |

**Critical note on design-point coherence:** Nearly all quantitative parameters for the commercial generator are extrapolations from the FF-2B experimental device or from theoretical calculations. The "commercial generator" is a paper concept — no engineering design exists. The FF-2B device itself has achieved peak current of ~1 MA (vs. 2.7 MA design), fusion yield of 0.2 J (vs. 60 kJ needed), and has operated only with deuterium fuel. The gap between demonstrated and required performance is larger than for any other concept in the corpus.

## Section 5b: Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier:**
No override. p-B11 fuel is aneutronic (<1% neutron energy from side reactions). No tritium breeding blanket is needed. No blanket structure costs apply. The library default for an aneutronic concept should handle this — the account cost is effectively zero or near-zero for shielding against minor secondary neutrons. No company-grounded figure justifies a specific override.

**C220102 — Radiation shield:**
No override. The concept produces negligible neutrons. LPPFusion claims the device "requires no costly containment structure" and is "safe enough to place in residential neighborhoods."[^23] Thin shielding for secondary radiation (x-rays, minor neutrons from p-B11 side reactions) would be needed, but no company-published cost figure exists for this. The library default for a low-neutron/aneutronic concept stands.

**C220104 — Primary pulsed driver:**
Override candidate. The capacitor bank is the primary pulsed driver. The FF-2B bank consists of 12 capacitors, 113 μF total, max 45 kV, max 115 kJ stored energy, and achieved slightly over 1 MA.[^24] The commercial device requires ~2.7 MA, implying a larger bank, but no separate cost is published. The FF-1 device (comparable to FF-2B) was constructed for ~$500,000 total — but this includes the entire device, not just the bank.[^25] No published decomposition exists to isolate the capacitor bank cost. Without a company-grounded figure for the driver subsystem alone, no accountable override can be constructed.

**C220105 — Primary structure:**
Override. The device is extremely compact (~3 tonnes total mass, ~30 m³ volume) with no external magnets, no large vacuum vessel, and minimal structural support requirements. The paper states the DPF is "very simple in construction, without either the need for external magnets nor lasers" and that "powerful experimental devices… [were] constructed for less than $500,000" total.[^29] The primary structure for a ~3 tonne device consists of a small steel frame supporting the electrode assembly, vacuum chamber (~10 cm radius), and capacitor bank — no gravity supports for superconducting coils, no inter-coil structure, no massive machine base. While no company-grounded structural cost is published, the radical reduction in structural mass (3 tonnes vs. thousands of tonnes for conventional MFE) justifies a scaling override.

```yaml
  - account: C220105
    value: 0.03 * generic.costs.c220105
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Dense Plasma Focus (DPF); §Energy Capture"
    rationale: |
      The entire device is ~3 tonnes — roughly 1000× lighter than a conventional
      MFE reactor module. No superconducting coil gravity supports, no inter-coil
      structure, no thermal shields, no massive machine base. Primary structure
      is a small steel frame for the electrode assembly, vacuum chamber (~10 cm
      radius), and capacitor bank. 3% of generic C220105 reflects the ~1000×
      mass reduction. No company figure for structural cost alone.
```

**C220106 — Vacuum system:**
No override. The FF-2B vacuum chamber is 10 cm radius — far smaller than any conventional fusion vacuum system. No company-grounded cost figure.

**C220107 — Pulsed-power capacitor bank:**
This account overlaps with C220104 for electrically-driven pulsed concepts. The capacitor bank is the dominant driver subsystem. The stored energy is 115 kJ at maximum for FF-2B; commercial requirements are not separately specified but implied to be similar scale (the commercial generator extrapolates physics, not bank size — the same bank at higher voltage/current is the concept). No published $/J figure for the bank. The library default on $/J stored stands in the absence of company-grounded data.

**C220109 — Direct energy converter:**
Override candidate — but no company-grounded cost figure exists. The concept relies entirely on direct energy conversion (ion beam decelerator + x-ray photoelectric converter), and this is the most novel subsystem. LPPFusion has not published any cost estimate for either conversion device. The x-ray converter is described as ~40–50 cm inner radius, ~50 cm length, but no materials cost or manufacturing cost estimate exists.[^26] The ion beam decelerator requires diamond-film switches that are at TRL 2–3. No override can be constructed from the available evidence — the library would need to apply a DEC cost, but there is no company figure to anchor it.

**C220110 — Remote handling & maintenance:**
Override. The device uses aneutronic p-B11 fuel, producing "insignificant amounts of induced radioactivity, and no radioactive waste."[^30] Neutrons carry only 0.2% of fusion energy and are low-energy, easily shielded. Monthly electrode replacement is envisioned as contact (hands-on) maintenance — the paper discusses "maintenance labor" without any mention of remote handling, shielded tooling, or restricted access.[^31] LPPFusion states the device is "safer than any existing energy source" and envisions regulation "under existing power safety regulations."[^32] No rad-hardened remote handling equipment, no hot cell, no master-slave manipulators are needed. While no company-grounded cost figure exists, the structural elimination of remote handling for an aneutronic, contact-maintained device justifies a scaling override.

```yaml
  - account: C220110
    value: 0.05 * generic.costs.c220110
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Cost and Transition; §Introduction"
    rationale: |
      Aneutronic p-B11 fuel produces negligible activation — neutrons carry
      only 0.2% of fusion energy. No remote handling equipment, no hot cell,
      no master-slave manipulators needed. Monthly electrode replacement is
      contact maintenance. 5% of generic C220110 covers basic lifting/tooling
      for electrode changeout but eliminates rad-hardened remote handling
      entirely. No company figure.
```

**C220111 — Installation & assembly:**
No override. No company-grounded figure.

**CAS21 — Buildings & site structures:**
Override candidate. The device is ~3 tonnes and ~30 m³ — it "fits within a small room 4 m on a side."[^27] This is orders of magnitude smaller than any conventional fusion reactor building. The company envisions mass-produced units deployed at distributed scales, not utility-scale plant sites. However, no published building cost or site cost figure exists. A relative override scaling from device size could be constructed, but would be purely analyst-derived, not company-grounded.

```yaml
overrides:
  - account: CAS21
    value: 0.05 * generic.costs.cas21
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Energy Capture"
    rationale: |
      The entire device is ~3 tonnes, ~30 m³, fits in a 4m×4m room. No reactor
      building, no hot cell, no heavy-lift crane bay. At 5 MWe with aneutronic fuel
      and no tritium handling, the building requirement is a small industrial
      enclosure, not a nuclear-grade reactor building. 5% of the generic CAS21
      is an order-of-magnitude estimate reflecting the ~100× reduction in
      building volume vs. a conventional fusion plant. No company-published
      building cost exists; this is analyst-derived.
```

**CAS23 — Turbine plant equipment:**
Override required. The design point uses direct energy conversion with no thermal cycle. eta_th = 0, so CAS23 = 0.

```yaml
  - account: CAS23
    value: 0.0
    enabled: true
    provenance: direct
    source: "lerner-2023-jfe-paper.md §Energy Capture"
    rationale: |
      No thermal cycle. All energy conversion is direct (ion beam decelerator +
      x-ray photoelectric). No steam turbine, no sCO2 cycle, no thermal BOP.
      CAS23 is structurally zero for this design point.
```

**CAS24 — Electric plant equipment:**
Override candidate. At 5 MWe, the switchyard and plant electrical distribution are far smaller than for a GWe-class plant. However, no company figure exists.

```yaml
  - account: CAS24
    value: 0.10 * generic.costs.cas24
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Cost and Transition"
    rationale: |
      At 5 MWe, the switchyard, transformers, and plant distribution are
      at small industrial/distributed generation scale, not utility scale.
      10% of generic CAS24 reflects the ~200× power reduction and
      correspondingly smaller electrical infrastructure. No company figure.
```

**CAS26 — Heat rejection system:**
Override required. No thermal cycle means no conventional heat rejection (cooling towers, circulating water for a Rankine/Brayton cycle). Some cooling is required for electrodes and electronics, but at a scale comparable to industrial equipment, not a power plant.

```yaml
  - account: CAS26
    value: 0.05 * generic.costs.cas26
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Energy Capture — Cooling"
    rationale: |
      No thermal cycle, so no condenser or cooling tower for a turbine island.
      Cooling requirements limited to: electrode tip cooling (~10 kW/cm² at
      anode tip, using compressed helium), capacitor bank thermal management,
      and electronics cooling. Total heat rejection is a small fraction of
      the 5 MWe output. 5% of generic CAS26 is an order-of-magnitude
      estimate. No company figure.
```

**CAS27 — Special materials:**
Override candidate. No tritium startup inventory, no FLiBe fill, no beryllium neutron multiplier. The initial material inventory is dominated by the beryllium electrodes (small mass — the anode is 2.8 cm radius) and the initial decaborane fuel charge. At $600/gram for isotopically pure decaborane (laboratory scale) and ~5 kg/year consumption, even the first year's fuel at laboratory prices would be ~$3M — but this is expected to drop "many hundred-fold" with mass production.

```yaml
  - account: CAS27
    value: 0.10 * generic.costs.cas27
    enabled: true
    provenance: derived
    source: "lppfusion-proton-boron-p11b-fuel-arrives/output.md"
    rationale: |
      No tritium inventory, no FLiBe, no lithium blanket fill. Initial
      inventory consists of beryllium electrodes (small mass, commercial
      Be is ~$800/kg) and initial decaborane fuel charge. Laboratory-
      scale isotopically pure decaborane costs $600/gram, but mass
      production is claimed to reduce this "many hundred-fold." At even
      $1/gram (optimistic mass production), 5 kg = $5,000. Total initial
      materials inventory is negligible vs. conventional fusion concepts.
      10% of generic CAS27 is conservative. No company-published figure
      for total initial materials cost.
```

**CAS70 — Annualized O&M + scheduled component replacement:**
Override candidate. The dominant O&M item is electrode replacement (~monthly). The device's small size and simplicity (no magnets, no tritium handling, no large vacuum system) should reduce staffing requirements. LPPFusion states that "the main costs initially will be in maintenance labor, although eventually much of this could be automated."[^28] No specific O&M cost figure is published.

```yaml
  - account: CAS70
    value: 0.25 * generic.costs.cas70
    enabled: false
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Cost and Transition; §Energy Capture"
    rationale: |
      O&M dominated by monthly electrode replacement (small beryllium
      components), capacitor bank maintenance, and staffing. No tritium
      handling, no remote maintenance, no large component changeouts.
      Device simplicity and small size should reduce staffing vs. conventional
      fusion plants. 25% of generic CAS70 reflects reduced complexity
      partially offset by high-frequency electrode replacement. No company
      O&M cost breakdown exists.
      **Framework limitation:** The 1costingFE library does not currently
      support CAS70 overrides — operating-cost accounts (CAS70, CAS80) are
      computed post-override and bypass the co.get() injection path used for
      capital costs. This override is disabled until the framework adds
      operating-cost override support. The native LCOE therefore carries the
      full generic CAS70, overstating O&M for this concept.
```

**CAS80 — Annualized fuel cost:**
Override candidate. Fuel is decaborane (B₁₀H₁₄) at ~5 kg/year. At laboratory scale, this costs ~$3M/year (93 g for $56,000). At mass-produced prices, LPPFusion claims "many hundred-fold" reduction — implying $1–6/gram, or $5,000–30,000/year. Even at laboratory prices, this is small relative to plant capital. LPPFusion describes fuel cost as "negligible."

```yaml
  - account: CAS80
    value: 0.03
    enabled: false
    provenance: derived
    source: "lppfusion-proton-boron-p11b-fuel-arrives/output.md; lerner-2023-jfe-paper.md §Cost and Transition"
    rationale: |
      Fuel is decaborane at ~5 kg/year. Laboratory cost is ~$600/gram
      ($3M/year) but requires mass production for commercial viability.
      Assuming 100-fold cost reduction to ~$6/gram: 5,000 g × $6/g = $30,000/year
      = 0.03 M$/year (model framework convention). Even at this level,
      fuel cost is negligible relative to capital amortization. Natural
      boron is abundant; isotopic enrichment to 99.9% B-11 is the cost driver.
      **Framework limitation:** The 1costingFE library does not currently
      support CAS80 overrides — operating-cost accounts (CAS70, CAS80) are
      computed by cas80_fuel() and bypass the co.get() injection path used
      for capital costs. This override is disabled until the framework adds
      operating-cost override support. The native LCOE therefore carries the
      full generic CAS80, overstating fuel cost for this concept.
```

### Override Count Check

**Enabled overrides: 7** (C220105, C220110, CAS21, CAS23, CAS24, CAS26, CAS27)

The archetype-fit is Low, expecting 6–12 enabled overrides. My count of 7 falls within the expected band. CAS70 and CAS80 are proposed but disabled due to a framework limitation (the 1costingFE library does not currently inject operating-cost overrides — CAS70 and CAS80 are computed by cas70_om()/cas80_fuel() and bypass the co.get() path used for capital costs; see the CAS70 and CAS80 entries above). If operating-cost override support is added, the enabled count would rise to 9. The overrides fall into two categories: (1) structural elimination or near-elimination of subsystems that do not exist in this concept (CAS23 zero, C220105 and C220110 at 3–5% of generic, CAS26 at 5%), and (2) drastic scale-down of infrastructure accounts for a 5 MWe distributed-generation device (CAS21 at 5%, CAS24 at 10%, CAS27 at 10%). Notably absent are overrides for C220104/C220107 (driver) and C220109 (DEC), where the concept is most novel but where no company-grounded cost data exists to construct an accountable departure from library defaults.

[^23]: lppfusion-investing-in-lppfusion-executive-summary/output.md
[^24]: lerner-2023-jfe-paper.md, §Experimental Device
[^25]: lerner-2023-jfe-paper.md, §Experimental Device — cost
[^26]: lerner-2023-jfe-paper.md, §Energy Capture — X-rays
[^27]: lerner-2023-jfe-paper.md, §Experimental Device
[^28]: lerner-2023-jfe-paper.md, §Cost and Transition
[^29]: lerner-2023-jfe-paper.md, §Dense Plasma Focus (DPF)
[^30]: lerner-2023-jfe-paper.md, §Introduction
[^31]: lerner-2023-jfe-paper.md, §Cost and Transition
[^32]: lerner-2023-jfe-paper.md, §Cost and Transition

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No demonstrated p-B11 fusion in any DPF device — the entire fuel-change yield multiplier (~100×) is theoretical | S2, S3 | truly-unknown | blocking | Await LPPFusion experimental results with decaborane; no external source can close this gap |
| 2 | Quantum magnetic field effect (QMFE) never verified in laboratory plasma — binary gate for p-B11 viability | S2 | truly-unknown | blocking | Fundamental physics experiment needed; no existing source addresses this |
| 3 | Yield plateau above 1 MA unresolved — I⁴ scaling not demonstrated in the operating regime | S2 | truly-unknown | blocking | Independent DPF scaling studies at >1 MA; Sandia or other national lab data |
| 4 | No engineering design for ion beam decelerator — no cost, no efficiency data, no prototype | S3, S5 | truly-unknown | blocking | Patent US #7,482,607 may contain detail; diamond switch development at LLNL |
| 5 | No engineering design for x-ray photoelectric converter — device "has never been made" | S3, S5 | truly-unknown | blocking | No known source; novel concept requiring dedicated R&D |
| 6 | No subsystem cost breakdown — the $500k unit cost is undecomposed | S1, S5b | proprietary | important | LPPFusion internal estimates; independent engineering assessment |
| 7 | Repetitive pulsed operation at ~200 Hz never demonstrated — electrode erosion, cooling, cycling all untested | S3 | truly-unknown | important | NX2 (Singapore) rep-rate DPF data; high-rep-rate pulsed power literature |
| 8 | Electrode lifetime at commercial conditions unknown — monthly replacement is aspirational | S3, S4 | truly-unknown | important | Electrode erosion studies in DPF literature (multiple labs) |
| 9 | Isotopically enriched decaborane mass-production cost unknown — current price is $600/g | S4 | not-yet-sourced | important | Isotope enrichment cost literature; boron processing industry data |
| 10 | Recirculating power fraction not quantified — capacitor bank recharge at 200 Hz requires ~12 MW for 60 kJ bank, which is 2.4× the 5 MWe output | S2, S5 | derivable | important | Can be derived from bank energy × rep rate; implies Q_eng must be very high or bank energy must be much less than 115 kJ per shot |
| 11 | Capacity factor and availability not discussed — no maintenance schedule, no downtime model | S1 | truly-unknown | important | No source; requires engineering assessment |
| 12 | Diamond-film switch development status unclear for fusion-relevant specs | S3, S4 | not-yet-sourced | nice-to-have | LLNL diamond PCSS program; academic pulsed power literature |

**Note on Gap #10 — Recirculating Power Paradox:** At 200 Hz with a 115 kJ bank, continuous recharge power is 23 MW — 4.6× the 5 MWe net output. This implies either (a) the commercial bank stores much less energy than FF-2B's 115 kJ (possible if higher current at lower voltage achieves fusion with less stored energy), (b) the conversion efficiency is much higher than implied (extracting >25 kJ net from 60 kJ fusion yield while also recharging the bank), or (c) the 200 Hz / 5 MWe / 25 kJ-per-pulse numbers are not self-consistent. The available sources do not resolve this. The 25 kJ net electricity per pulse × 200 Hz = 5 MW arithmetic is internally consistent only if the capacitor bank recharge is treated as part of the gross-to-net conversion, meaning the ~60 kJ fusion yield must cover both the ~25 kJ net output and the bank recharge energy, with the balance coming from the high conversion efficiency of the DEC systems recovering most of the bank's stored energy that doesn't go into fusion.

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point. The upstream pipeline assigned an empty comparables list (`Comparables: []`), meaning the family-delta contract is satisfied vacuously: no comparables were assigned, so no subsystem-level cost delta can be computed against a fixed baseline. The qualitative positioning that follows is **supplementary context only** — it does not substitute for the formal delta that would be articulated if a comparable were assigned.

The Dense Plasma Focus is classified upstream under confinement family MFE — the plasma is confined by its own current-generated magnetic fields, making it formally a magnetic confinement device. However, the DPF's self-confinement, pulsed operation (~10 ns events at near-solid densities), lack of any external magnets, and reliance on direct energy conversion rather than a thermal cycle place it at the extreme fringe of the MFE family. The geometry (plasmoid at the anode tip) has no analogue among the other MFE concepts in the corpus. These structural differences — not a reclassification — define the qualitative cost positioning below.

While no formal comparable exists, the concept's cost-relevant position relative to the broader MFE family and the corpus can be characterized along several dimensions:

**vs. All Magnetic Confinement Concepts (MFE):** Focus Fusion has no external magnets, no superconducting coils, no vacuum vessel in the MFE sense, and no steady-state or quasi-steady plasma. The entire confinement event is ~10 ns — shorter than the pulse duration of even the most pulsed MFE concept (Z-pinch at ~100 ns). The device cost ($500k claimed) is 3–4 orders of magnitude below any MFE plant concept.

**vs. Pulsed Concepts (IFE, MIF):** Focus Fusion shares the pulsed architecture with IFE and MIF concepts but differs in that the "driver" is simply a capacitor bank discharging through electrodes — no laser, no projectile, no mechanical compression, no external magnetic field. There are no per-shot consumable targets in the IFE sense (the electrodes erode but are replaced monthly, not per-shot). The rep rate target (~200 Hz) is far higher than any IFE concept (typically 1–10 Hz) and comparable only to Helion (~1 Hz actual, higher targets).

**vs. Other p-B11 Concepts:** Focus Fusion shares the p-B11 fuel choice with TAE Technologies (FRC-based) and HB11 Energy (laser-based). All three face the fundamental challenge of achieving fusion conditions with p-B11's extremely high temperature requirement and unfavorable cross-section. Focus Fusion's claimed advantage is the QMFE suppressing bremsstrahlung — a physics mechanism not invoked by any other concept. TAE uses beam-driven FRC confinement; HB11 uses ultra-short-pulse laser interaction. Focus Fusion's DPF approach is the lowest-cost, simplest device but relies on the most speculative physics.

**Cost structure uniqueness:** The concept's cost structure is unlike any other in the corpus. The device is 3 tonnes, mass-producible, and targeted at distributed generation (5 MWe). There is no reactor building, no tritium plant, no thermal cycle, and no heavy civil construction. If the physics works, the LCOE would be dominated by manufacturing cost and electrode maintenance, not by the capital-intensive subsystems that dominate every other fusion concept. If the physics does not work, there is no cost model to build.

## Section 8: Sources

1. **Lerner, E. J. et al. (2023)** "Focus Fusion: Overview of Progress Towards p-B11 Fusion with the Dense Plasma Focus." *J. Fusion Energy* 42:7. — Primary source for device parameters, experimental results, theoretical framework (QMFE), energy conversion concept, and commercial generator vision. The most comprehensive single source for the Focus Fusion concept.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md`

2. **Lerner, E. J. et al. (2024)** "Preparations for pB11 tests in the FF-2B dense plasma focus." *Frontiers in Physics*. — Preparations for fuel transition to decaborane, radiation safety analysis (Be-7, C-11 production), diagnostic plans for p-B11 fusion products. Provides FF-2B device parameters and references prior achievements.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2024-frontiers-pB11-prep.md`

3. **LPPFusion website — "Our Plan to Net Energy"** — Investment-oriented roadmap. Phase 2 budget (~$100M), yield scaling argument (75× × 16× × 100× = 120,000×), commercialization strategy (non-exclusive licensing), capacitor bank upgrade path.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md`

4. **LPPFusion website — Executive Summary** — High-level summary of achievements and claims. Device cost (<$1M), claimed temperature records, comparison to other fusion approaches.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-executive-summary/output.md`

5. **LPPFusion website — "Focus Fusion Energy / DPF Device"** — Technical description of the DPF device and energy conversion concept. Electrode dimensions, plasmoid characteristics, energy flow architecture.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lppfusion-website-technology.md` and `iter-02/sources/lppfusion-technology-focus-fusion-energy-dpf-device/output.md`

6. **LPPFusion — "Proton-Boron (p11B) Fuel Arrives"** — Fuel procurement details. Decaborane specification (99.9% B-11), cost ($56,000 for 93 g), supply chain (Russia + Czech Republic).
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-proton-boron-p11b-fuel-arrives/output.md`

7. **Compound Semiconductor (2024)** — "US team reinvents the diamond switch." University of Illinois diamond PCSS research. Record current density (44 A/cm), fast switching (~2 ns). Relevant as enabling technology for DPF high-speed switching.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/compoundsemiconductor-119149-us-team-reinvents-the/output.md`

8. **LLNL/IPO — Diamond photoconductive switch listing** — TRL 3 diamond PCSS with ~20% efficiency and ~50 kW output power. Pulsed power listed as target application.
   - Path: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/ipo-ipo-technologies-instruments-sensors-and-electronics/output.md`
