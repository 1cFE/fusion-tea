---
ID: 12-levitated-dipole
Concept: Levitated Dipole (D-T)
Company: OpenStar Technologies
Status: draft
Created: 2026-03-22
Approved-Date:
Reuses: [01-hts-compact-tokamak, 08-frc-w-direct-conversion, 11-magnetic-mirror, 21-spherical-tokamak-hts]
Review-Iterations: 1
Last-Review: 2026-03-22
Review-Status: addressed
---

# D1+ Analysis: Levitated Dipole (D-T) — OpenStar Technologies

**Concept**: Single floating HTS coil levitated dipole — D-T fuel, quasi-steady-state operation
**Company**: OpenStar Technologies (Wellington, New Zealand; founded 2021)
**Commercial Target**: Tama Nui (50–200 MWe); preceded by Maui (~2031, neutron-producing) and Tahi (~2028, Lawson criterion demonstration)
**Confinement Family**: MFE — Levitated Dipole
**Operation Mode**: Quasi-steady (>95% duty cycle; pulsed only by cryogenic reservoir thermal limits)

---

## Section 1: Availability of Data

**Rating: Moderate**

OpenStar Technologies published a detailed D-T power plant design paper in February 2026 (arXiv 2602.20564, Simpson et al.) — a rare level of transparency for a startup at this development stage. The paper includes a 0D power balance model, neutronics analysis, magnet design specifications, and a conceptual blanket configuration. This is supplemented by a companion paper on the Junior prototype (arXiv 2508.17691). Together, these two preprints form the core technical basis for this analysis. The "Moderate" rating reflects that OpenStar discloses more physics and engineering detail than most early-stage fusion startups, while stopping well short of the information needed to close an LCOE model: capital cost, thermal cycle choice, Qsci, auxiliary power requirements, and balance of plant are all absent.

**Peer-reviewed and technical literature:**

The Simpson et al. (2026) preprint is the primary engineering reference. It discloses the "Reactor A" conservative design point, magnet architecture (23 T REBCO HTS, CICC, neon slush cooling), plasma heating baseline (ICRH, ~70% wall-plug efficiency), tritium breeding approach (Li₂O ceramic, TBR 1.1), and the key performance output pair: ~667 MW fusion power and ~208 MWe net electric [arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance]. The paper benchmarks two confinement scaling assumptions (Bohm and "improved") and selects the conservative case as the published design point [arxiv-2602-20564-dt-dipole-power-plants.md §Plasma Physics].

> "In order to achieve rapid deployment of fusion power to the grid, the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Fuel

The Junior prototype paper (arXiv 2508.17691) provides measured hardware performance: 14 NI solder-impregnated REBCO HTS coils in series, 5.63 T design field (2.35 T achieved at 42% of design current), 550 kg floating mass, and 0.095 MJ stored energy delivered via the on-board flux pump — a world record for HTS flux pump delivery at the time of publication [arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs]. The Junior device was built in under two years for less than $10M USD [arxiv-2508-17691-junior-design-results.md §Key Notes].

**Experimental heritage:**

OpenStar's lineage traces to LDX (MIT/Columbia, 2004–2011), the only prior levitated dipole experiment. LDX demonstrated quasi-steady high-beta discharges (β up to ~20%, >20 seconds), observed the inward turbulent pinch phenomenon, and used ECRH heating exclusively [openstar-prototype-roadmap.md §Lab Experiments]. The University of Tokyo RT-1 device corroborated peaked density profiles in a similar geometry using Bi-2223 HTS [openstar-prototype-roadmap.md §Lab Experiments]. These experiments established the core physics phenomena — interchange-mode MHD stability, peaked pressure profiles, anomalous inward particle pinch — that OpenStar's design relies upon.

OpenStar demonstrated levitated plasma confinement in February 2026: the Junior magnet levitated inside the Marsden vacuum chamber, achieving plasma at ~300,000°C for 20 seconds [openstar-2026-funding-tahi-timeline.md §February 2026 Milestone]. This is the first levitated dipole plasma demonstration by a commercial entity.

**Company transparency:**

OpenStar is moderately transparent by startup standards. Published items include: device names and prototype roadmap, funding amounts (NZD 20M pre-2026 + NZD 35M in February 2026 from the NZ Regional Infrastructure Fund), key experimental milestones, and the power plant preprint with 0D physics modeling. Not published: capital cost estimates, numerical Qsci value, auxiliary heating power requirements, thermal power conversion cycle choice, or any plant economic analysis.

**Phase 1a dossier completeness:**

The dossier achieved high confidence on confinement family, fuel, plasma state (sustained, not ignited — explicitly verified via power balance equation analysis), magnet type, neutron management, and operation mode. Medium confidence remains on tritium breeding (Li₂O confirmed but cooling scheme and module design preliminary) and energy capture (thermal cycle genuinely unpublished — re-confirmed across arXiv HTML and all OpenStar website technical resources). After two research iterations, these are confirmed as publication gaps, not research gaps.

**Key data gaps limiting this analysis:**
1. Qsci numerical value present in the design paper but not accessible in the HTML preprint version
2. Auxiliary heating power (Paux) not stated → recirculating power fraction cannot be calculated
3. Thermal power conversion cycle (Rankine vs. sCO₂) not specified in any source
4. No capital cost estimate at any level of detail
5. Plasma exhaust handling not discussed anywhere in the published design
6. Li₂O blanket cooling scheme acknowledged as preliminary in the paper itself

---

## Section 2: Challenges in Capturing System Function

The levitated dipole's LCOE structure rests on four central engineering bets: (1) inherent MHD interchange stability enabling high-beta operation without ELMs or disruptions; (2) the on-board flux pump enabling indefinite coil energization without current leads penetrating the vacuum vessel; (3) a two-section sacrificial coil architecture solving neutron tolerance without abandoning the levitated geometry; and (4) quasi-steady operation at >95% duty cycle eliminating pulsed-power energy storage requirements. Each bet introduces LCOE modeling challenges ranked below by impact.

**1. Flux Pump and Levitated Coil — No Cost Analogues (Impact: Critical)**

The defining engineering innovation of the OpenStar design is the on-board superconducting transformer-rectifier flux pump, which maintains the floating coil's current without any physical current leads penetrating the vacuum vessel [arxiv-2602-20564-dt-dipole-power-plants.md §Driver Technology; openstar-prototype-roadmap.md §Key Milestones]. This system is patented and has no commercial precedent — no comparable fusion device has used an on-board flux pump in a power plant context. The capital cost of the levitated coil + flux pump + docking mechanism assembly is the single most uncharacterized CAPEX item in the design.

The entire confinement system reduces to one floating component and one external support magnet, which is a remarkable architectural simplification relative to tokamaks (dozens of TF and PF coils). But "simpler" does not mean "cheaper" when the single component must: achieve 23 T at the winding, operate in a D-T neutron environment, undergo partial replacement annually, re-levitate after each maintenance cycle, and maintain position control to within the tolerances required for stable plasma geometry. The Junior prototype cost of <$10M [arxiv-2508-17691-junior-design-results.md §Key Notes] is a scientific device at TRL 2–3 and provides no meaningful scaling basis for the power plant coil.

**2. Confinement Scaling — Bohm Assumed, Unvalidated at Fusion-Relevant Conditions (Impact: Critical)**

The Reactor A design point uses Bohm-like confinement scaling, which the paper identifies as conservative [arxiv-2602-20564-dt-dipole-power-plants.md §Plasma Physics]. The LDX experiment demonstrated quasi-steady confinement with Bohm-level energy confinement times in hydrogen isotopes at sub-keV plasma temperatures (hundreds of eV) — but LDX operated at a fraction of the plasma pressure and stored energy of a fusion-grade device. Junior currently operates at ~300,000°C (26 eV), more than two orders of magnitude below the 10–20 keV required for D-T fusion.

The entire commercial viability case depends on confinement being at least Bohm-level at the reactor design point — and preferably "improved" (a second, more optimistic scenario in the paper). The "improved confinement" scenario is not described in the HTML preprint. The extrapolation from Junior's 26 eV demonstration plasma to the Reactor A operating point has not been benchmarked against any fusion-relevant experiment. Tahi (~2028) is designed to demonstrate placement on the Lawson criterion curve — this is a critical milestone, but until it is achieved, the confinement scaling assumption remains the largest unvalidated physics element of the design.

**3. Unknown Qsci and Recirculating Power Fraction (Impact: High)**

The plasma is not ignited: the power balance equation includes Paux (auxiliary power) as an essential term, and Section 2.2.7 of the paper describes ICRH as "required" for operation rather than supplementary [arxiv-2602-20564-plasma-state-clarification.md §Evidence]. The paper treats Qsci as a fixed design parameter but does not state its numerical value in the accessible HTML version.

The published 667 MW fusion / 208 MWe net pair enables a partial inference. Assuming 35–40% thermal efficiency on the nuclear island and an energy multiplication of approximately 1.1 from breeding reactions, gross electric is roughly 255–290 MWe, implying ~50–80 MWe recirculating power [inferred from arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance; thermal efficiency range from MFE analogue designs]. With ICRH wall-plug efficiency of ~70% [arxiv-2602-20564-dt-dipole-power-plants.md §Heating], implied Paux is approximately 35–55 MW, giving Qsci in the range of 12–19. This is a derivable inference with wide uncertainty from the unspecified thermal conversion efficiency, not a published value.

**4. Sacrificial Coil Replacement — Novel OPEX Structure (Impact: High)**

The two-section coil design is innovative: the sacrificial outer section (~20% of coil volume) is designed for approximately 1 year neutron damage lifetime. The 1 MW-year/m² fluence figure is stated in the paper as the tungsten shield replacement threshold; the ~1-year coil replacement cycle is derived from the coil's design lifetime in the same neutron environment [arxiv-2602-20564-dt-dipole-power-plants.md §Magnet; dossier.md §Neutron Management]. This means the levitated coil must be docked, partially replaced, and re-levitated on an approximately annual cycle. The operational sequence — pumping out spent neon slush, docking the magnet, replacing the sacrificial outer section, recharging via flux pump, and re-levitating — is described conceptually in the paper but has never been demonstrated at any scale.

This creates an unusual OPEX structure with no precedent in any approved prior analysis. Tokamak OPEX centers on blanket and divertor module replacement; FRC OPEX involves no first-wall-comparable component; mirror OPEX centers on heating system maintenance. The levitated dipole's primary scheduled maintenance item — an annual partial coil replacement — is a recurring CAPEX-like expenditure with neither a cost estimate nor a manufacturing specification in any public source.

**5. Balance of Plant Undefined (Impact: Moderate)**

No source — the arXiv paper, OpenStar website, or any news coverage — specifies the thermal power conversion cycle. The paper focuses on the nuclear island and notes BOP engineering is outside its scope [arxiv-2602-20564-dt-dipole-power-plants.md §Energy Conversion]. This is a genuine publication gap. The two-temperature shield design (hot shield >2000 K, warm shield ~600°C) with 92% of deposited heat radiated to the first wall potentially enables higher-efficiency thermodynamic cycles than typical tokamak designs, but this has not been analyzed or published.

**6. Plasma Exhaust Handling (Impact: Moderate)**

The levitated dipole has no divertor equivalent. In a tokamak, plasma exhaust — helium ash, unburned fuel, and impurities — is directed to a localized target for pumping. In a levitated dipole, the closed magnetic topology has no natural exhaust channel. None of the OpenStar publications discuss helium ash accumulation, impurity seeding, fueling strategy, or first-wall heat load distribution. A device designed to sustain D-T plasma at >95% duty cycle must have an answer to this question, but it is absent from all available sources. [1]

---
[1] Reviewed: arxiv-2602-20564-dt-dipole-power-plants.md (full HTML); arxiv-2508-17691-junior-design-results.md; openstar-prototype-roadmap.md; openstar-2026-funding-tahi-timeline.md. No mention of divertor, plasma exhaust, helium ash, or fueling in any source.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**Plasma Exhaust and Fueling System — TRL 1**

- **Demonstrated**: Nothing. No plasma-facing component design for exhaust handling, no exhaust pathway, and no fueling mechanism (beyond ICRH as the heating source) has been described for any levitated dipole device in D-T operating conditions.
- **On paper only**: Not yet addressed in any published document.
- **Missing at scale**: The entire subsystem concept. Helium ash accumulation in a closed-field configuration, impurity control, and D-T fuel injection must all be resolved for D-T operation. This is the most significant unstated gap in the published design.

---

**D-T Confinement at Fusion-Relevant Conditions — TRL 2**

- **Demonstrated**: Junior demonstrated levitated plasma confinement at ~300,000°C (26 eV) for 20 seconds in February 2026, the first such demonstration by a commercial entity [openstar-2026-funding-tahi-timeline.md §February 2026 Milestone]. LDX previously demonstrated quasi-steady high-beta confinement (β ~20%) with hydrogen isotopes in a levitated dipole geometry for >20 seconds at keV temperatures [openstar-prototype-roadmap.md §Lab Experiments]. The Bohm-like confinement scaling used in the Reactor A design has been observed in LDX — but not at D-T-relevant triple products.
- **On paper only**: D-T confinement at fusion-relevant nTτ on the Lawson curve. Tahi (~2028) is designed to demonstrate reaching the Lawson criterion — it is not itself expected to produce neutrons [openstar-2026-funding-tahi-timeline.md §Tahi Specifications]. Peaked pressure profile stability at the local β₀ ~ 3 optimum at fusion grade.
- **Missing at scale**: D-T plasma operation and significant neutron production (planned for Maui, ~2031). Confinement scaling validation from current 26 eV baseline to 10–20 keV operating point. Demonstration of >95% duty cycle over months of operation.

---

**Tritium Breeding Blanket (Li₂O Ceramic) — TRL 3**

- **Demonstrated**: Li₂O ceramic pebble-bed tritium breeding is characterized in the ITER HCPB Test Blanket Module program; tritium release kinetics and breeding performance from Li₂O under fission neutrons are established. TBR of 1.1 is analytically modeled for the OpenStar geometry, with the favorable note that only ~25% of fusion neutrons intercept the core magnet, leaving a higher fraction available for blanket breeding [arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding; dossier.md §Tritium Breeding].
- **On paper only**: Complete Li₂O blanket module for the levitated dipole's spherical vessel geometry. Heat extraction pathway from the two-temperature tungsten/B₄C shield (>2000 K, ~600°C) through the first wall to the blanket. Neutron multiplier choice (paper notes "other ceramic materials with neutron multipliers feasible"). Full blanket cooling scheme.
- **Missing at scale**: Li₂O blanket tested under 14 MeV fusion neutrons at fusion-relevant fluences (the paper acknowledges this as early-stage design). Tritium extraction from Li₂O at power-plant throughput (kg/day scale). Blanket geometry conforming to the spherical dipole vessel with the large bottom opening required for core magnet removal.

---

**Two-Section Sacrificial Coil + Annual Replacement Scheme — TRL 3**

- **Demonstrated**: The two-section design concept is described in the arXiv preprint [arxiv-2602-20564-dt-dipole-power-plants.md §Magnet]. The Junior prototype demonstrated the basic non-insulated solder-impregnated REBCO coil construction at laboratory scale. A separate sacrificial outer section has not been fabricated or tested.
- **On paper only**: The annual docking-and-partial-replacement cycle. Neon slush rapid pump-out and recharge via the on-board reservoir mechanism ("slushy is pumped out of reservoir channels, and new slushy is quickly pumped right back in" [dossier.md §Operation Mode]). Isolation of the semi-permanent inner section from mechanical and thermal loads during outer section replacement.
- **Missing at scale**: A coil designed for 23 T in a CICC architecture with a mechanically separable replaceable outer section that has been validated under 14 MeV neutron fluence to the 1 MW-year/m² threshold. Full docking and replacement test at any representative scale. Maui (~2031) is the first device intended for significant neutron production.

---

**Flux Pump at Power-Plant Operating Levels — TRL 3–4**

- **Demonstrated**: Junior demonstrated a superconducting transformer-rectifier flux pump delivering 95 kJ (0.095 MJ) to the 550 kg REBCO coil — a world record for HTS flux pump energy delivery at the time of the Junior paper publication (arXiv 2508.17691, 2025) [arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs; openstar-prototype-roadmap.md §Key Milestones]. The flux pump requires only ~10 W of continuous power. A subsequent milestone of 170 kJ was achieved after that publication, per the prototype roadmap [dossier.md §Driver Technology; openstar-prototype-roadmap.md §Key Milestones].
- **On paper only**: Flux pump scaled to the power plant coil stored energy level, which substantially exceeds the Junior prototype (exact 23 T power plant coil stored energy not published; scales approximately as B²V relative to Junior's 5.63 T design).
- **Missing at scale**: Flux pump operation in a sustained D-T neutron and gamma radiation environment. Long-term reliability of the on-board superconducting rectifier over years of continuous power plant operation. Current regulation precision sufficient to maintain levitation position stability during plasma perturbations.

---

**HTS Coil at 23 T (REBCO CICC) — TRL 4–5**

- **Demonstrated**: CFS demonstrated a full-scale 20 T REBCO TF coil for the SPARC tokamak [referenced in 01-hts-compact-tokamak handwritten §HTS Magnets]. Tokamak Energy Demo4 validated 11.8 T in full tokamak configuration [referenced in 21-spherical-tokamak-hts §Component-Level Publications]. REBCO is routinely characterized in commercial production. Junior demonstrated 2.35 T at 42% of design current (5.63 T target), validating the NI solder-impregnated coil construction approach [arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs].
- **On paper only**: 23 T REBCO CICC in neon slush cooling at 24.6 K. Mechanical design of a levitation-compatible coil capable of withstanding Lorentz forces at 23 T while suspended with sufficient dimensional stability for plasma position control.
- **Missing at scale**: REBCO performance and degradation under the specific 14 MeV neutron spectrum experienced by the core magnet (which intercepts ~25% of fusion neutrons). Long-term coil performance across many neon slush thermal cycles. Full-scale 23 T CICC coil wound and tested — Tahi targets 20 T (~2028).

---

**ICRH Heating System — TRL 6–7**

- **Demonstrated**: MW-class ICRH systems routinely operated on JET, EAST, TFTR, and JT-60SA; ITER ICRH system under construction at 20 MW total. Wall-plug efficiency of ~70% demonstrated at multi-MW levels. The physics basis is well-established across many tokamak campaigns.
- **On paper only**: ICRH antenna design integrated into the levitated dipole geometry, where the floating coil restricts physical access and the antenna must be geometrically compatible with a rotating dipolar field topology distinct from tokamak geometry.
- **Missing at scale**: ICRH antenna positioning, coupling efficiency, and radiation hardening in a neutron-producing environment where the floating coil limits radial access. No ICRH has operated in any levitated dipole experiment; Junior uses ECRH only [arxiv-2508-17691-junior-design-results.md §Heating].

---

**Cryogenics (Neon Slush at 24.6 K) — TRL 5–6**

- **Demonstrated**: Liquid neon cryogenics are mature industrial technology. Neon slush (solid-liquid mixture at the melting point) is physically straightforward. Large-scale helium refrigeration systems (ITER-scale) are proven at 4 K, making 24.6 K operation less demanding.
- **On paper only**: Neon slush delivery and recovery at the flow rates required for rapid maintenance cycling. Integration with the docking mechanism to allow coil removal and reattachment while maintaining thermal management continuity.
- **Missing at scale**: Long-duration neon slush reservoir performance under steady-state magnet operation at the power plant coil stored energy level.

---

**Balance of Plant (Thermal Power Conversion) — TRL 7–8**

- **Demonstrated**: Conventional steam Rankine and sCO₂ Brayton cycles are mature at GW-class power levels in fission and fossil plants.
- **Missing at scale**: Integration with fusion-specific heat sources — the two-temperature tungsten/B₄C shield at >2000 K / ~600°C is a non-standard thermal source profile. Tritium-compatible primary coolant loops. Thermal power conversion cycle selection is entirely unspecified for the OpenStar design.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO HTS Tape**

The OpenStar power plant's confinement system requires one primary floating coil (23 T) and one external levitation/support magnet — a qualitatively lower total tape demand than a tokamak, which requires dozens of TF and PF coils. The handwritten 01-hts-compact-tokamak analysis documents the global supply baseline: REBCO production is currently thousands of km/year; a single ARC-class tokamak requires >5,000 km; prices are $30–100/kA-m with a commercial target near $10/kA-m [01-hts-compact-tokamak handwritten §Key Materials]. The levitated dipole's single-coil architecture is a genuine supply chain advantage — even a high-stored-energy 23 T power plant coil likely requires a small fraction of the tape demanded by a tokamak's complete magnet set.

The specific tape quantity for the OpenStar power plant coil is not published. A rough scaling estimate: the Junior coil (5.63 T design, 550 kg) consumed some quantity of REBCO; the 23 T power plant coil, operating at ~4× higher field and larger volume, would store roughly 16× more energy per unit volume (energy ∝ B²) and occupy a substantially larger volume [inferred scaling; arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs; arxiv-2602-20564-dt-dipole-power-plants.md §Magnet]. The annual replacement of the sacrificial outer section (~20% of the coil) creates a recurring REBCO demand without parallel in steady-state designs — approximately 20% of the total coil tape supply per year for replacement inventory.

**Tritium**

Standard D-T startup constraint, identical in character to all D-T concepts in this project. The global tritium inventory is approximately 25–30 kg, primarily from CANDU heavy-water reactors, decaying at 5.5% per year. Startup inventory for a plant is ~1 kg, priced at market rates exceeding $35,000/g — approximately $35M per plant [01-hts-compact-tokamak handwritten §Key Materials, tritium characterization]. The Li₂O breeding blanket targets TBR 1.1, providing a modest margin above self-sufficiency. The favorable neutron geometry (only ~25% of neutrons absorbed by the core magnet region [arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management]) means more neutrons are available for blanket breeding compared to a tokamak with equivalent fusion power — a potential TBR advantage.

**Lithium-6 Enrichment**

The Li₂O ceramic breeder requires Li-6 enrichment for effective breeding at reasonable blanket thickness. Natural lithium is 7.4% Li-6. Li-6 enrichment production is dominated by Russia and China; the mercury-based isotope separation process used historically is banned in most Western jurisdictions. A supply restart would require capital investment and lead time. This constraint is shared with all D-T concepts and is not unique to the levitated dipole [01-hts-compact-tokamak handwritten §Key Materials].

**Tungsten and Boron Carbide (B₄C)**

The two-temperature shield uses layers of tungsten and B₄C composite. The hot shield operates above 2000 K, imposing severe thermal and radiation demands on the tungsten microstructure. High-temperature tungsten fabrication at large scale — crack resistance, thermal cycling durability, and manufacturing precision — is an active materials challenge shared with all fusion first-wall programs. B₄C is an established industrial material with no supply constraints. The B₄C also functions as a tritium producer via the ¹⁰B(n,α)³H reaction, providing a secondary TBR contribution [arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding].

**Neon (Industrial Gas)**

Neon is produced as a byproduct of oxygen production from air fractionation and is widely available as an industrial product. No supply constraints are anticipated at power plant volumes. This is a significant advantage over helium (which has supply concentration and depletion concerns) for cryogenic cooling.

**Inconel 718 (Vacuum Vessel Inner Shell)**

The vacuum vessel inner wall is thin Inconel 718 with tungsten coating [arxiv-2602-20564-dt-dipole-power-plants.md §Vacuum Vessel]. Inconel 718 is a widely used nickel superalloy with established aerospace-scale manufacturing. No supply constraint is anticipated. The outer reinforced concrete dome is entirely conventional.

**No High-Energy Pulsed Power Requirements**

Unlike MagLIF (capacitor banks requiring a reduction from ~$5/J to ~$0.50/J) or laser IFE (multi-kJ laser systems), the levitated dipole has no high-energy pulsed driver. The capital cost structure is dominated by the HTS coil assembly, ICRH heating system, and blanket. This is a material supply chain simplification relative to all IFE and MIF concepts. [1]

---
[1] Contrast with 07-maglif analysis §Capacitor Costs for the MagLIF pulsed power baseline.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion power (Reactor A, conservative Bohm) | ~667 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance | high | Conservative Bohm scaling design point only; improved confinement scenario not published in HTML |
| Net electric output (Reactor A) | ~208 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance | high | Conservative design point |
| Net plant electrical efficiency | ~31% | [inferred: 208 MWe / 667 MW; arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance] | medium | Net-to-fusion ratio; thermal efficiency of conversion cycle is higher but unknown |
| Duty cycle | >95% | arxiv-2602-20564-dt-dipole-power-plants.md §Operation Mode | high | Pulsed only by neon slush reservoir thermal limits, not plasma physics; <2 weeks downtime/year |
| Tritium breeding ratio (TBR) | 1.1 | arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding | medium | Li₂O ceramic baseline; analytic model, not experimentally verified |
| Neutron fraction reaching core magnet | ~25% | arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management | high | Geometric advantage vs. tokamaks; enables thinner shielding |
| Core magnet peak field | 23 T | arxiv-2602-20564-dt-dipole-power-plants.md §Magnet | high | REBCO CICC, neon slush at 24.6 K |
| Core magnet CICC operating current density | 0–300 A/mm² | arxiv-2602-20564-dt-dipole-power-plants.md §Magnet | high | Design range for REBCO in this architecture |
| Tahi prototype target field | 20 T | openstar-2026-funding-tahi-timeline.md §Tahi Specifications | high | 4× Junior design field (~5.6 T); ~2028 target |
| Sacrificial coil section fraction | ~20% of coil volume | arxiv-2602-20564-dt-dipole-power-plants.md §Magnet | medium | Outer section only; replaces annually |
| Sacrificial coil replacement interval | ~1 year | arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management | medium | The 1 MW-year/m² fluence threshold is stated for tungsten shield replacement; ~1-year coil cycle is derived from coil design lifetime in the same neutron environment |
| Optimal local plasma β | ~3 | arxiv-2602-20564-dt-dipole-power-plants.md §Plasma Physics | high | β₀ ~ 3 optimal for Bohm-like confinement scaling |
| ICRH wall-plug efficiency | ~70% | JET/EAST published ICRH literature (primary); arxiv-2602-20564-dt-dipole-power-plants.md §Heating (context for ICRH vs. ECRH selection) | high | Demonstrated on JET, EAST at multi-MW levels; cited by OpenStar as basis for selecting ICRH over ECRH |
| Hot shield temperature | >2000 K | arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management | high | W/B₄C shield; 92% of deposited neutron heat radiated to first wall |
| Warm shield temperature | ~600°C | arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management | high | Second temperature zone in two-temperature design |
| Flux pump continuous operating power | ~10 W | openstar-prototype-roadmap.md §Key Milestones | high | Maintains full coil current indefinitely after charging |
| Flux pump delivered energy (Junior) | 0.095 MJ | arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs | high | World record for HTS flux pump delivery at time of publication |
| Junior floating mass | 550 kg | arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs | high | Current prototype; power plant coil substantially larger |
| Junior prototype cost | <$10M USD | arxiv-2508-17691-junior-design-results.md §Key Notes | high | Scientific device at TRL 2–3; no plant cost scaling basis |
| Commercial target output (Tama Nui) | 50–200 MWe | openstar-prototype-roadmap.md §Device Naming; openstar-2026-funding-tahi-timeline.md §Tama Nui | medium | Range only; no design point or power balance |
| Total estimated development cost to commercial | $500M–$1B | openstar-prototype-roadmap.md §Funding | low | Company estimate; no breakdown or basis provided |
| Gross electric (inferred) | ~255–290 MWe | [inferred: 208 MWe net from 667 MW fusion at assumed 35–40% thermal efficiency and ~1.1 energy multiplication; arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance; thermal efficiency analogue from MFE literature] | low | Wide range from unspecified thermal conversion cycle |
| Recirculating power (inferred) | ~50–80 MWe | [inferred: gross electric minus 208 MWe net; see gross electric derivation above] | low | Includes ICRH heating + cryogenics + pumping |
| Implied Qsci (inferred) | ~12–19 | [inferred: 667 MW fusion / Paux; Paux estimated as 35–55 MW from recirculating power at ~70% ICRH wall-plug efficiency; arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance and §Heating] | low | Very wide uncertainty; Qsci is in the paper as a fixed design parameter but not accessible in HTML version |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Total plant capital cost | truly-unknown | blocking | No estimate at any level of detail |
| LCOE estimate or target | truly-unknown | blocking | No company or independent estimate |
| Thermal efficiency / power conversion cycle type | truly-unknown | blocking | Rankine vs. sCO₂ undisclosed; determines gross electric and LCOE |
| Qsci numerical value | not-yet-sourced | blocking | Present in paper; request full PDF or await journal publication |
| Auxiliary heating power (Paux) | proprietary | blocking | Determines recirculating power fraction and actual Qeng |
| Capacity factor numerical target | not-yet-sourced | important | >95% stated; no maintenance schedule model or numerical availability target |
| First-wall heat flux and replacement schedule | truly-unknown | important | Two-temperature shield at >2000 K radiates to first wall; no materials specification or replacement interval |
| Li₂O blanket cooling scheme and module geometry | not-yet-sourced | important | Paper acknowledges this is preliminary |
| Core magnet stored energy and REBCO tape quantity | derivable | important | [Derivable once coil inner/outer radius and length published; scales as B²V from Junior baseline] |
| Plasma exhaust and fueling mechanism | truly-unknown | important | Not addressed anywhere; helium ash accumulation in closed-field geometry unresolved |
| Flux pump capital cost | truly-unknown | important | Patented novel technology; no industry analogue or cost estimate exists |
| Sacrificial outer section replacement cost (OPEX) | truly-unknown | important | Annual scheduled item; no cost estimate or manufacturing specification |
| Commercial plant capital cost structure | truly-unknown | blocking | No plant study or cost account breakdown at any stage |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Qsci numerical value (present in paper but not in HTML version) | S2, S5 | not-yet-sourced | blocking | Request full PDF of arXiv 2602.20564 or await journal publication |
| 2 | Thermal power conversion cycle type and efficiency | S2, S5 | truly-unknown | blocking | OpenStar BOP disclosure; Rankine assumption usable as analogue with caveat |
| 3 | Auxiliary heating power Paux → recirculating fraction → Qeng | S2, S5 | proprietary | blocking | Required for LCOE closure; only inferred within wide range from net/fusion power pair |
| 4 | Total plant capital cost at any level | S5 | truly-unknown | blocking | No near-term public source; may appear with Maui (2031) pre-conceptual design |
| 5 | LCOE estimate or target | S5 | truly-unknown | blocking | No company or independent analysis; would require plant study |
| 6 | Confinement scaling validation at Lawson-relevant conditions | S2, S3 | truly-unknown | blocking | Tahi (~2028) is designed to demonstrate this; currently unsupported experimentally |
| 7 | Plasma exhaust and fueling subsystem design | S3 | truly-unknown | important | Not addressed in any OpenStar publication; fundamental gap for sustained D-T operation |
| 8 | Capacity factor numerical model and maintenance schedule | S5 | not-yet-sourced | important | >95% stated; detailed maintenance timeline not published |
| 9 | Core magnet stored energy and REBCO tape quantity | S4, S5 | derivable | important | [Derivable once coil geometry published; scales approximately as B²V from Junior] |
| 10 | Sacrificial coil section replacement cost (OPEX) | S3, S5 | truly-unknown | important | Annual scheduled item; no manufacturing specification or cost analogue |
| 11 | Flux pump capital cost | S3, S5 | truly-unknown | important | Patented novel technology; no precedent in any prior analysis |
| 12 | Li₂O blanket module design: cooling scheme, neutron multiplier, and geometry | S3, S5 | not-yet-sourced | important | Paper acknowledges preliminary stage; detailed design may appear with Maui design work |
| 13 | First-wall heat flux profile and replacement schedule | S3, S5 | truly-unknown | important | High-temperature radiated power from >2000 K shield; no materials specification |
| 14 | Commercial plant net electric target and power balance | S5 | not-yet-sourced | important | Only "50–200 MWe" for Tama Nui; no design point or closed power balance |

---

## Section 7: Cross-Concept Notes

Four approved prior analyses were consulted: 01-hts-compact-tokamak (handwritten exemplar), 08-frc-w-direct-conversion, 11-magnetic-mirror, and 21-spherical-tokamak-hts. The levitated dipole shares surface-level technology categories with several approved concepts — HTS REBCO magnets, ICRH heating, ceramic tritium breeding — but the system architecture differs enough that most data transfers only at the supply chain level, not at the component engineering level.

**Shared with 01-hts-compact-tokamak and 21-spherical-tokamak-hts — REBCO supply chain:**

The global REBCO supply chain characterization from the tokamak analyses (thousands of km/year production, $30–100/kA-m current price, scale-up to commercial fusion requires 1–2 orders of magnitude in volume and a factor of 3–10 cost reduction) applies as the baseline constraint. The key departure: the levitated dipole's single-coil architecture is a qualitative supply chain advantage. A tokamak requires >5,000 km of tape per ARC-class plant [01-hts-compact-tokamak handwritten §Key Materials]; the levitated dipole needs one primary coil plus one support magnet. Even accounting for annual sacrificial section replacement, total REBCO demand over a plant lifetime is likely one order of magnitude lower than for a comparable tokamak. This does not eliminate the supply chain challenge — 23 T pushes to the performance frontier — but changes its scale substantially.

**Shared with 01-hts-compact-tokamak — Tritium and Li-6 supply chains:**

Tritium constraints ($35,000/g, ~25–30 kg global inventory, CANDU-produced, 5.5%/yr decay, ~1 kg startup) and Li-6 enrichment geopolitics (Russian/Chinese dominance, mercury-process ban in Western jurisdictions) are identical to all D-T concepts. The characterization from the handwritten analysis is directly reused. The levitated dipole's favorable neutron geometry — 75% of neutrons bypass the core magnet — provides a potential TBR advantage not available to tokamaks with denser magnet coverage.

**Shared with 21-spherical-tokamak-hts — Undisclosed thermal cycle:**

Both OpenStar and Tokamak Energy have published machine parameter sets (OpenStar: 667 MW / 208 MWe; Tokamak Energy: 450–750 MWe net) without specifying thermal power conversion cycle choices. In both cases, the dossiers confirm this is a genuine publication gap — not a research artifact. The modeling approach for both is to assume a thermal efficiency range (35–40% Rankine, 40–45% sCO₂) and propagate uncertainty.

**Diverges from all tokamak and mirror analyses — No disruptions, no ELMs:**

The tokamak analyses (01-hts-compact-tokamak, 21-spherical-tokamak-hts) identify disruptions and ELMs as design constraints that drive first-wall structural specification, reduce effective availability, and add complexity to plasma-facing component replacement. The levitated dipole is inherently MHD stable via interchange mode: no toroidal plasma current means no disruption mechanism, and the peaked pressure profile in good-curvature geometry does not exhibit ELMs. The mirror analysis (11-magnetic-mirror) notes axial end losses as the dominant physics risk — the levitated dipole's closed topology eliminates this. These are genuine engineering advantages, but their magnitude in LCOE terms is unknown without a plant study.

**Diverges from 08-frc-w-direct-conversion — No direct energy conversion path:**

The FRC analysis (08-frc-w-direct-conversion) notes that Helion's direct energy recovery from collapsing plasma inductance can dramatically lower the Q threshold for net electricity. The levitated dipole is a closed-field configuration where ions are confined magnetically and lose energy radiatively or through anomalous transport to the first wall rather than escaping in a directed beam. No DEC mechanism is applicable to the levitated dipole. This removes a potential economic lever; all fusion energy must be recovered thermally.

**Diverges from 11-magnetic-mirror — Single-coil vs. linear solenoid magnet architecture:**

The mirror analysis identifies the center-cell solenoid array as a 50+ m linear magnet system requiring substantial REBCO over its length. The levitated dipole's single floating coil is architecturally opposite — one magnet, not a distributed array. The economic implications run in opposite directions: the mirror's linear geometry enables modular scaling by adding center-cell length, while the dipole must scale by upsizing the single coil or building multiple independent units (the Tama Nui "50–200 MWe" range may reflect this flexibility).

---

## Section 8: Sources

1. **arxiv-2602-20564-dt-dipole-power-plants.md** — T. Simpson, R.A. Badcock, et al. (OpenStar Technologies Limited, 2026), "Deuterium-Tritium Levitated Dipole Fusion Power Plants," arXiv:2602.20564v1. Primary engineering reference: Reactor A design point (667 MW fusion, 208 MWe net), 23 T REBCO CICC coil, Li₂O blanket (TBR 1.1), two-section sacrificial coil, >95% duty cycle, power balance equation (Eq. 9), ICRH baseline (~70% efficiency), neutron management (W/B₄C shield, 25% core intercept), Bohm-like confinement scaling, local β₀ ~ 3 optimal. Phase 1a source: `iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md`.

2. **arxiv-2508-17691-junior-design-results.md** — OpenStar Technologies team (2025), "Design and Initial Results from the 'Junior' Levitated Dipole Experiment," arXiv:2508.17691v1. Junior prototype specifications: 14 NI solder-impregnated HTS coils, 5.63 T design / 2.35 T achieved at 42% design current, 1.44 kA design / 600 A achieved, 550 kg floating mass, 0.095 MJ stored energy (world record for HTS flux pump delivery), ECRH heating, built in under 2 years for <$10M. Phase 1a source: `iter-01/sources/arxiv-2508-17691-junior-design-results.md`.

3. **openstar-prototype-roadmap.md** — Compiled from multiple news sources and OpenStar website. Device naming and roadmap (Junior → Tahi → Maui → Tama Nui), company founding details (2021, Wellington; Ratu Mataira CEO, Darren Garnier CSO from MIT LDX program, Rod Badcock CTO), funding history (NZD 20M pre-2026 + NZD 35M Feb 2026), key milestones (170 kJ flux pump, 10 W continuous maintenance), LDX and RT-1 experimental heritage. Phase 1a source: `iter-01/sources/openstar-prototype-roadmap.md`.

4. **arxiv-2602-20564-plasma-state-clarification.md** — iter-02 research note based on Simpson et al. (2026). Documents evidence that the power plant design is "sustained" not ignited: Paux is an essential term in power balance Eq. 9, alpha heating in good-curvature region entirely balanced by radiation losses (only bad-curvature alpha heating contributes net self-heating), ICRH is described as "required" not supplementary, fixed Qsci design framework. Phase 1a source: `iter-02/sources/arxiv-2602-20564-plasma-state-clarification.md`.

5. **openstar-2026-funding-tahi-timeline.md** — Compiled from Bloomberg, RNZ, World Nuclear News, Energy Connects (February–March 2026). February 2026 milestone: levitated plasma at ~300,000°C for 20 seconds. NZD 35M NZ Regional Development Fund grant. Prototype timeline with Tahi specifications (20 T, Lawson criterion, ~2028), Maui (~2031, neutron production, revenue), Tama Nui (50–200 MWe commercial). Phase 1a source: `iter-02/sources/openstar-2026-funding-tahi-timeline.md`.

6. **01-hts-compact-tokamak handwritten analysis** — Fusion TEA project handwritten exemplar. REBCO supply chain characterization (>5,000 km per ARC-class plant, $30–100/kA-m, commercial target ~$10/kA-m), tritium supply chain ($35,000/g, 25–30 kg global inventory, 5.5%/yr decay, ~1 kg startup per plant), Li-6 enrichment constraints (Russian/Chinese dominance, mercury-process ban) reused in Section 4 with adaptation to single-coil demand profile.

7. **LDX (Levitated Dipole Experiment)** — MIT/Columbia University, DOE-funded, 2004–2011. First levitated dipole experiment: demonstrated quasi-steady high-beta confinement (β ~20%), inward turbulent pinch, ECRH heating at 2.45–28 GHz. Primary physics heritage for OpenStar. Cited via openstar-prototype-roadmap.md §Lab Experiments; no direct source document in Phase 1a materials. Wikipedia: https://en.wikipedia.org/wiki/Levitated_Dipole_Experiment.
