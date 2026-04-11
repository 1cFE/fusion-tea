---
ID: 06-magnetic-mirror
Concept: Magnetic Mirror (p-B11)
Company: Pale Blue Fusion
Status: draft
Created: 2026-03-22
Approved-Date:
Reuses: [11-magnetic-mirror, 08-frc-w-direct-conversion, 01-hts-compact-tokamak]
Review-Iterations: 1
Last-Review: 2026-03-22
Review-Status: addressed
---

# D1+ Analysis: Magnetic Mirror (p-B11) — Pale Blue Fusion

**Concept**: Multi-chamber centrifugal magnetic mirror (CHARM) — p-B11 fuel, alpha channeling, direct energy conversion
**Company**: Pale Blue Fusion (pre-incorporation; Princeton University spinoff, Nat Fisch group)
**Confinement Family**: MFE — Magnetic mirror (centrifugal)
**Operation Mode**: Steady-state

---

## Section 1: Availability of Data

**Rating: Opaque**

This concept sits at an extreme early stage — a physics research group in the process of incorporating a company, with no dedicated experimental hardware of their own, no plant design, and no engineering cost estimates in the public record. Data availability is opaque for LCOE purposes: rich in plasma physics theory and computation, essentially empty on engineering and economics.

**Peer-reviewed literature:**

The Fisch group at Princeton has produced 29 peer-reviewed publications under ARPA-E support (2022–2025), making this one of the most publication-active private fusion groups relative to its stage of development. [1] However, these publications are exclusively plasma physics — they address the fundamental science of alpha channeling, centrifugal species separation, ponderomotive barriers, nonthermal p-B11 operation, and DEC in axisymmetric fields. The closest to an engineering document is a 2025 PRX Energy paper on direct energy conversion efficiency in axisymmetric fields:

> "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields"
> — Rax, Kolmes & Fisch, PRX Energy 4, 013007 (2025)
> (arpa-e-2025-fisch-presentation-notes.md, §Key Publication List)

This paper analyzes the physics efficiency ceiling of adiabatic DEC but does not provide engineering parameters or cost data. No plant study, no system code output, and no power plant design document for CHARM exists anywhere in the public record.

**Company transparency:**

As of July 2025, Pale Blue Fusion was pre-incorporation — Princeton University approvals were in place, a website mockup was shown at the ARPA-E presentation (palebluefusion.com, "Full website coming soon"), and the team was publicly seeking investors and partners. [2] No FIA listing, no independent funding announcement, no device roadmap, and no reactor concept study have been published. The ARPA-E OPEN 2021 grant ($1.5M) is the only disclosed funding:

> "Fisch receives funding for 'unlikely but fantastic' clean energy technology"
> — princeton-arpa-e-funding-2022.md, §Key Facts: "$1.5 million from ARPA-E OPEN 2021 program"

**Experimental validation:**

The Fisch group does not operate its own experimental hardware. The most relevant validation is CMFX (Centrifugal Mirror Fusion Experiment) at the University of Maryland — a separate group using repurposed MRI LTS superconducting magnets (3 T throat / 0.3 T midplane, mirror ratio 10, 6.7 m length). CMFX achieved first plasma October 2022 and reported fusion yield measurements in 2025 (arXiv:2505.23047). [3] CMFX uses D-D fuel, conventional LTS magnets, and does not implement alpha channeling, the multi-chamber CHARM architecture, ponderomotive barriers, or p-B11 fuel. It validates centrifugal mirror confinement physics but not any of CHARM's distinguishing technical bets.

The 0D power balance code (PB)² and the S5 PIC code (for wave-particle interactions in rotating plasmas) are computational tools developed by the Fisch group, shown in the ARPA-E presentation. These are simulation tools, not experimental data.

**Completeness of Phase 1a dossier:**

The dossier captures the concept accurately and exhausts what is publicly available. The remaining gaps are not resolvable with more search — they reflect the pre-commercialization stage of the effort.

**Key data gaps:**

- No plant design, device concept study, or engineering parameters of any kind
- No fusion power, net electric, Q, or energy balance figures
- No capital cost, operating cost, or LCOE estimate
- No magnet specifications (conductor technology not disclosed)
- No DEC efficiency data or efficiency targets
- No experimental demonstration of CHARM's specific architecture

---
[1] arpa-e-2025-fisch-presentation-notes.md, §Key Publication List: "29 papers under ARPA-E support, 2022–2025."
[2] arpa-e-2025-fisch-presentation-notes.md, §Company Status (slides 8–9).
[3] technical-papers-summary.md, §Related: CMFX.

---

## Section 2: Challenges in Capturing System Function

CHARM combines five distinct technical bets — p-B11 fusion, centrifugal species separation, alpha channeling, ponderomotive barriers, and direct energy conversion — all of which must work simultaneously for the concept to function. This creates LCOE modeling challenges that are qualitatively different from D-T magnetic confinement: the fusion physics itself is undemonstrated at any scale, and the regime required (nonthermal, quasi-relativistic protons in a rotating plasma with wave-mediated energy recycling) has no experimental analog.

### 1. p-B11 Reactivity Deficit: The Fundamental Barrier (Impact: Blocking)

p-B11 fusion requires the highest temperatures and confinement quality of any fusion fuel cycle. The p-B11 cross-section peaks at ~600 keV, versus ~65 keV for D-T — roughly a 9× higher cross-section peak energy, translating to operating temperature requirements of ~150–300 keV vs. ~10–20 keV for D-T thermal plasmas. At the temperatures needed for p-B11 fusion (~150–300 keV), electrons radiate energy as X-rays (bremsstrahlung) at rates that exceed fusion power production in any conventional thermal plasma:

> "At required temperatures (~150–300 keV), electrons produce x-rays (bremsstrahlung) that carry away more energy than fusion produces"
> — princeton-arpa-e-funding-2022.md, §Technical Approach

This is an existential constraint, not merely a challenge. CHARM's response is to make the plasma strongly nonthermal: energetic protons maintained far above the equilibrium temperature, cold electrons and boron to suppress radiation. The alpha channeling mechanism is the energy source for maintaining this nonthermal state — it extracts energy from fusion-born helium ions and redirects it into the proton population. If alpha channeling efficiency is insufficient, or if thermalization causes the proton distribution to relax, bremsstrahlung losses exceed fusion gain and the reactor cannot operate.

For LCOE modeling, this means there is no "baseline Q" to assume. The effective gain depends critically on: (a) alpha channeling efficiency η_α, (b) the ratio of nonthermal proton energy to total stored energy, (c) radiation loss management including bremsstrahlung reabsorption (synchrotron radiation was identified as manageable via reabsorption in slide 19 of the ARPA-E presentation), and (d) the energy cost of maintaining plasma rotation. All four quantities are theoretical estimates; none are experimentally measured. The range of plausible effective gains spans zero (thermalization wins) to economically competitive (all physics bets work) — an uncertainty range that prevents meaningful LCOE bounds. [1]

### 2. Alpha Channeling Efficiency: The Critical Internal Lever (Impact: Critical)

Alpha channeling is the mechanism by which CHARM converts an existentially problematic fuel cycle (p-B11) into a potentially viable one. The mechanism — RF waves in the ion cyclotron frequency range that resonantly interact with fusion-born helium ions, extracting their energy and redirecting it into fuel protons — reduces the required confinement time for p-B11 breakeven by a factor of 2.6 (thermal proton case) to 6.9 (fast proton hybrid scheme):

> "Alpha channeling reduces required energy confinement time for ignition by factor of 2.6 (thermal) to 6.9 (fast proton)"
> — technical-papers-summary.md, §Lowering the reactor breakeven requirements for p-B11 fusion (2024)

The factor-of-6.9 improvement (from the hybrid fast-plus-thermal proton scheme) is the difference between p-B11 being plausibly achievable and clearly infeasible. However, this efficiency factor is derived from analytical and 0D models, not from experiments. The S5 PIC simulation shows XB mode conversion is the relevant wave physics, but has not been validated against CHARM-specific plasma conditions. [2]

For LCOE, α channeling efficiency η_α is the dominant sensitivity parameter — it controls whether the concept achieves net gain at any economically relevant Q. A 2× reduction in η_α relative to the model value could make the concept non-igniting regardless of engineering optimization. No experimental measurement of η_α in a centrifugal mirror with p-B11-like plasma conditions exists anywhere in the literature.

### 3. Helium Ash Management: No Margin for Error (Impact: Critical)

Even if fusion conditions are achieved, helium ash from the three alpha products of each p-B11 reaction (p + B11 → 3 He4) will rapidly accumulate and poison the plasma. The 2025 Ochs, Kolmes, Fisch paper addresses this directly:

> "Preventing ash from poisoning proton-boron 11 fusion plasmas"
> — Ochs, Kolmes, Fisch, Phys. Plasmas 32, 052506 (2025)
> (arpa-e-2025-fisch-presentation-notes.md, §Key Publication List)

The CHARM multi-chamber architecture — fusion chamber where boron is centrifugally confined, heat exchange chamber where helium and hot protons migrate, with ponderomotive barriers controlling ion traffic — is specifically designed to solve this. Boron ions (11 amu) are more strongly centrifugally confined than protons (1 amu); helium ions (4 amu, 2e charge) have an intermediate charge-to-mass ratio that allows them to migrate to the heat exchange chamber where waves remove them. The 2025 Kolmes, Ochs, Fisch paper further shows that adding a third species with a lower charge-to-mass ratio (e.g., Li-7) can "invert" centrifugal confinement to create better end plugs (arXiv:2504.18634, submitted PRL).

For LCOE, this architecture introduces multiple sequential physics requirements that must all work: differential centrifugal confinement, functional ponderomotive barriers, wave-induced ash diffusion in the heat exchange chamber, and continuous helium extraction. Each is an independent risk that compounds the others. The integrated architecture has never been tested. [3]

### 4. Rotation Energy Cost and Recovery: Unknown Recirculating Power (Impact: High)

CHARM requires a rapidly rotating plasma to exploit centrifugal species separation. The rotation is established and maintained by a biased central electrode, with "large voltage drops with minimal dissipation." [4] This requires continuous power input to maintain the radial electric field against resistive losses and particle cross-field transport. The ARPA-E presentation slide 19 identifies that "voltage drops can be minimized near walls" — implying this was a derisking goal, not a demonstrated result.

The fraction of fusion power that must be recirculated to sustain plasma rotation is not characterized. It depends on plasma resistivity, the confinement time of the rotation energy, and the efficiency of the biased electrode system. This recirculating power fraction directly enters the LCOE calculation as a reduction in net electric output, analogous to NBI recirculating power in D-T mirrors. For CHARM, unlike D-T mirrors, there is no published power balance model with numbers — only the 0D (PB)² code framework shown in the ARPA-E presentation. [5]

### 5. Direct Energy Conversion: Efficiency and Capital Cost Unknown (Impact: High)

CHARM's preferred energy conversion strategy appears to be recovering the rotation energy of the plasma directly, rather than using a conventional thermal cycle. The 2025 PRX Energy paper from the core team (Rax, Kolmes, Fisch) specifically analyzes adiabatic DEC in axisymmetric fields — the physics basis for recovering rotation energy as electricity. An earlier SWDEC patent (US20230298771, 2023) covers RF-based DEC for axisymmetric mirrors. The ARPA-E slide 19 notes that "centrifugal drift energy is recoverable."

However, no efficiency number, capital cost estimate, or engineering design for the DEC system has been published by Pale Blue or the Fisch group. The PRX Energy paper addresses physical efficiency limits, not hardware specifications. The interaction between DEC, plasma exhaust management, and the heat exchange chamber architecture is not characterized. This is a different challenge than Realta Fusion's venetian-blind DEC (Section 7) — Pale Blue targets rotation energy recovery, while Realta targets escaping end-loss ion energy — but both lack experimental validation. [6]

### 6. No Plant Design, No Scaling Anchor (Impact: Blocking for LCOE)

There is no published plant design, device concept study, or even a parameterized conceptual reactor point for CHARM. The ARPA-E presentation shows a schematic of the multi-chamber architecture, identifies the key physics questions, and summarizes which questions have been theoretically derisked. It does not specify machine size, plasma density, plasma radius, mirror length, magnetic field strength, fusion power, net electric output, or any engineering cost. This is qualitatively different from concepts like Realta (where Hammir parameters are partially published) or Helion (where Polaris hardware is operational). For CHARM, even a rough order-of-magnitude LCOE estimate would require assuming every major system parameter.

---
[1] princeton-arpa-e-funding-2022.md, §Technical Approach; arpa-e-fisch-2025-presentation.md, §Requirements for pB11 Fusion.
[2] technical-papers-summary.md, §Lowering the reactor breakeven requirements; arpa-e-2025-fisch-presentation-notes.md, §Computational Tools (S5 PIC Code).
[3] arpa-e-fisch-2025-presentation.md, §CHARM Architecture; technical-papers-summary.md, §Ion Mix Can Invert Centrifugal Confinement (2025).
[4] arpa-e-2025-fisch-presentation-notes.md, §Device Details (slide 6): "large voltage drops with minimal dissipation (biased electrode)."
[5] arpa-e-2025-fisch-presentation-notes.md, §Power Balance Code (PB)².
[6] arpa-e-2025-fisch-presentation-notes.md, §Summary of Derisked Questions (slide 19): "Centrifugal drift energy is recoverable."

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**CHARM Multi-Chamber Integrated Architecture — TRL 1**

- **Demonstrated**: Nothing. The multi-chamber architecture (fusion chamber + heat exchange chamber + plug) with ponderomotive barriers, centrifugal species separation, and alpha channeling operating simultaneously has never been built or tested at any scale. The architecture exists only in papers and a schematic on an ARPA-E slide.
- **On paper only**: The full CHARM concept. The spatial separation of boron-trapping, helium-extraction, and proton recycling into distinct physical chambers. The integrated ponderomotive barrier system. Simultaneous centrifugal confinement and alpha channeling in a rotating plasma.
- **Missing at scale**: A proof-of-concept experiment demonstrating even one chamber of the architecture in the relevant plasma regime. An integrated test of centrifugal species separation with p-B11 or analog plasmas. Any data on how the chambers interact dynamically. [1]

---

**p-B11 Nonthermal Reactor Operation — TRL 1–2**

- **Demonstrated**: p-B11 fusion has been observed in beam-target experiments and inertial confinement shots, demonstrating the reaction is physically real. Theory of nonthermal p-B11 fusion is extensively developed by the Fisch group. The Kolmes et al. 2022 papers establish the hybrid fast-thermal proton scheme analytically.
- **On paper only**: Any reactor-relevant plasma regime for p-B11 — high-temperature, nonthermal proton distribution with cold electrons and boron, maintained by wave-mediated energy recycling. The "derisked" questions from slide 19 are all theoretical derisks, not experimental ones.
- **Missing at scale**: A laboratory plasma at p-B11-relevant conditions (>100 keV proton temperature, cold electron distribution, measurable p-B11 fusion yield above bremsstrahlung). This is the concept's fundamental experimental gap. [2]

---

**Ponderomotive Barriers / One-Way RF Walls — TRL 2**

- **Demonstrated**: The theory of ponderomotive barriers using static azimuthal perturbations in rotating mirrors is developed in Rubin & Fisch (Phys. Plasmas 32, 062104, 2025). The fundamental ponderomotive effect of RF waves on plasma is well-established physics. ARPA-E slide 19 identifies selective ponderomotive walls as derisked in principle.
- **On paper only**: Any experimental demonstration of a species-selective ponderomotive barrier in a rotating plasma. The specific geometry and field configuration needed for CHARM's "one-way RF walls." The energy cost of maintaining ponderomotive barriers at steady state.
- **Missing at scale**: Experimental validation at reactor-relevant conditions. ARPA-E slide 19 notes "one-way walls have high energy cost, so use is situational" — indicating that the energy cost issue is recognized but not resolved. [3]

---

**Direct Energy Conversion (Rotation Energy Recovery) — TRL 2–3**

- **Demonstrated**: The physics of adiabatic DEC in axisymmetric fields is analyzed theoretically in Rax, Kolmes, Fisch (PRX Energy 4, 013007, 2025). The general principle of electrostatic deceleration of escaping ions as a DEC mechanism is supported by historical work on gridded converters and venetian-blind collectors. SWDEC (Standing Wave Direct Energy Converter) is covered by patent US20230298771 (2023) as an alternative RF-based approach.
- **On paper only**: Any prototype of the rotation energy recovery DEC design. Efficiency characterization for Pale Blue's specific approach (adiabatic vs. SWDEC). Integration with the multi-chamber plasma flow.
- **Missing at scale**: Hardware of any kind. Experimental efficiency measurement. The conceptual separation between "rotation energy recovery" and "escaping ion energy recovery" (as in Realta's venetian-blind DEC) is physically meaningful but neither approach has been built. [4]

---

**Alpha Channeling in Centrifugal Mirrors — TRL 3–4**

- **Demonstrated**: Alpha channeling in mirror machines is theoretically established since Fisch (PRL 97, 225001, 2006). The wave physics — RF waves resonantly extracting energy from fusion-born alpha particles and cooling them out of the trap — is analytically derived and computationally modeled. The S5 PIC code simulates XB mode conversion in supersonic rotating plasmas, specifically validating the relevant wave-particle interaction physics. The 2022 papers demonstrate analytically that hybrid fast-thermal proton alpha channeling reduces breakeven requirements by 6.9×.
- **On paper only**: Alpha channeling in a centrifugal mirror with fast proton populations and p-B11 reaction products specifically. The coupling between alpha channeling efficiency and plasma rotation dynamics.
- **Missing at scale**: Any experimental demonstration of alpha channeling in a rotating plasma. Alpha channeling has been proposed but not yet demonstrated experimentally even in non-rotating mirrors — the Fisch group's own 2006 paper was a theory proposal. The required wave frequency, power level, antenna geometry, and coupling efficiency at CHARM-relevant conditions are not characterized. [5]

---

**Centrifugal Mirror Confinement (E×B Rotation) — TRL 3–4**

- **Demonstrated**: CMFX at the University of Maryland has demonstrated centrifugal mirror confinement with E×B rotation using LTS superconducting magnets (3 T / 0.3 T, mirror ratio 10, 6.7 m length, biased central electrode up to 100 kV). First plasma October 2022; DC power supply (100 kV, 100 kW) installed May 2024; fusion yield measurements reported in 2025 (arXiv:2505.23047). This is independent physics validation of the centrifugal mirror approach. [6]
- **On paper only**: Species separation at the p vs. B11 mass ratio (1 vs. 11 amu) in a fusion-relevant plasma. Centrifugal mirror confinement at reactor-relevant temperatures (>100 keV). The CMFX results are at low temperature and use D-D fuel, not p-B11.
- **Missing at scale**: Centrifugal species separation in a p-B11-relevant plasma. CMFX validates the confinement geometry but CHARM's distinguishing feature — exploiting the 11× mass disparity of p vs. B11 to separate species centrifugally — has not been demonstrated. The Kolmes et al. 2025 paper (arXiv:2504.18634) shows theoretically that a third species can improve confinement, suggesting continued evolution of the species separation concept. [7]

---

**Magnet System (Conductor Type Unspecified) — TRL Indeterminate**

- **Demonstrated**: The ARPA-E presentation shows solenoidal axisymmetric mirror coils (outer and inner) but does not specify conductor technology. CMFX uses repurposed MRI LTS magnets. WHAM (Realta, separate project) uses REBCO HTS magnets at 17 T as the most relevant state-of-the-art mirror magnet [Realta Hammir: 11-magnetic-mirror analysis §Section 3]. HTS solenoid winding for mirror geometry is demonstrated at WHAM.
- **On paper only**: Pale Blue's magnet specifications. Mirror ratio requirement for CHARM. Field strength at the throat and midplane for a reactor concept. Whether CHARM needs HTS (for high mirror ratio) or could use LTS or normal conducting magnets at the intended operating point.
- **Missing at scale**: Any reactor-engineering specifications from Pale Blue. The magnet architecture will depend entirely on the plasma physics operating point, which is itself undefined. [8]

---

**RF Heating / Wave Launch (Alpha Channeling Antenna) — TRL 4–5 (generic) / TRL 1–2 (CHARM-specific)**

- **Demonstrated**: Ion cyclotron range of frequency (ICRF) heating antennas are deployed routinely on major tokamaks and mirror experiments. High-power RF systems in the 1–100 MHz range are industrial products. The XB mode conversion mechanism is understood theoretically and has been simulated with S5.
- **On paper only**: Alpha channeling antenna geometry for a rotating plasma — the wave must be launched to resonate with alpha particles at specific locations in the rotating multi-chamber geometry. The required power level and frequency for CHARM's operating conditions.
- **Missing at scale**: Any alpha channeling RF system operating in a fusion plasma. The wave-particle interaction that CHARM relies on for its core energy recycling function has not been demonstrated experimentally in any device. [9]

---
[1] arpa-e-fisch-2025-presentation.md, §CHARM Architecture.
[2] technical-papers-summary.md, §Wave-supported hybrid fast-thermal p-B11 fusion (2022); princeton-arpa-e-funding-2022.md, §Technical Approach.
[3] technical-papers-summary.md, §Ponderomotive barriers in rotating mirror devices using static fields (2025); arpa-e-2025-fisch-presentation-notes.md, §Summary of Derisked Questions: "One-way walls have high energy cost, so use is situational."
[4] technical-papers-summary.md, §Related: Direct Energy Conversion.
[5] technical-papers-summary.md, §Alpha Channeling in Mirror Machines (Fisch 2006); arpa-e-2025-fisch-presentation-notes.md, §Computational Tools (S5 PIC Code).
[6] technical-papers-summary.md, §Related: CMFX.
[7] technical-papers-summary.md, §Ion Mix Can Invert Centrifugal Confinement (2025).
[8] dossier.md, §Magnet Type: "no conductor technology specification; no public disclosure from Pale Blue/Fisch group."
[9] arpa-e-2025-fisch-presentation-notes.md, §Computational Tools (S5 PIC Code).

---

## Section 4: Key Materials and Supply Chain Considerations

CHARM's most striking material property from a supply chain perspective is what it does not need. The p-B11 fuel cycle eliminates tritium breeding, lithium, neutron shielding materials, and remote handling infrastructure required by D-T concepts. This represents a potential structural supply chain advantage if the physics can be demonstrated. But it introduces a different set of concerns.

**Boron-11 Fuel**

Natural boron is 19.9% boron-10 and 80.1% boron-11. p-B11 fusion requires boron enriched in B-11 to suppress parasitic reactions on B-10. The B-10(n,α) reaction is a large neutron absorber in nuclear reactors, but for p-B11 which is near-aneutronic, the concern is primarily the reactivity dilution from B-10 occupying centrifugal trapping positions in the fusion chamber. The required B-11 enrichment level for CHARM is not specified in any available source. Industrial B-11 enrichment is established technology — boron isotope separation is used in nuclear plant moderator systems. Crucially, since B-11 is already the major isotope at ~80%, enrichment to fusion-grade purity (e.g., >99%) is a modest isotopic purification task — not a 5× concentration step, but rather a ~5-fold reduction of the minority B-10 component. This is substantially less demanding than enrichment scenarios where the desired isotope starts as the minority species. Natural boron costs approximately $5–10/kg for industrial grades; enriched B-11 at high purity is specialty-chemical territory at higher cost, but the enrichment challenge is accessible by existing industrial methods. Supply chain risk is low (boron is globally abundant and not radioactively controlled), and the reasoning flows directly from B-11 being the naturally dominant isotope. No data on Pale Blue's B-11 requirements is available. [1]

**No Tritium, No Lithium, No Breeding Blanket**

The absence of tritium and lithium from the supply chain is a genuine structural advantage relative to D-T concepts:

> "No tritium breeding and containment... Cheap and non-radioactive reactants"
> — arpa-e-fisch-2025-presentation.md, §Why p-B11?

The D-T mirror (Realta, 11-magnetic-mirror analysis) faces the same tritium startup problem as all D-T concepts — ~$35M in tritium per plant, CANDU reactor dependence, Li-6 enrichment supply chain — all of which disappear for CHARM. This is not a trivial advantage: it removes two of the three most challenging fusion supply chain items (tritium and lithium-6). [2]

**Magnet Conductor (Unknown — Likely HTS)**

The magnet technology is unspecified by Pale Blue. If CHARM adopts HTS (REBCO) magnets as the most likely choice for reactor-scale mirrors (see dossier note and the WHAM/CMFX contrast), the same global REBCO supply chain constraints apply as documented in prior analyses:

- Current global REBCO production: thousands of km/year
- SPARC-class tokamaks require >5,000 km; mirror solenoids have simpler geometry but similar magnetic energy requirements
- REBCO price: $30–100/kA-m; cost reduction of 3–5× needed for commercial fusion economics
- Geographically concentrated: SuperPower (US), Fujikura (Japan), SuNAM (Korea)

However, unlike Realta's Hammir — which has a specific 17 T end-plug magnet requirement established by WHAM — Pale Blue has not specified any field strength, coil geometry, or stored energy for CHARM. The mirror ratio needed for centrifugal confinement at p-B11 temperatures is not published. The magnet supply chain risk cannot be quantified without a design point. [3]

**Proton Source (Hydrogen)**

CHARM requires a proton beam source to establish the fast proton population for the hybrid scheme. Hydrogen is trivially abundant. Proton injectors (either NBI equivalents or RF-ionized sources) are established technology. This is not a supply chain concern. [4]

**No First-Wall Neutron Damage or Activation**

The near-aneutronic p-B11 fuel cycle eliminates the most severe materials development challenge of D-T concepts — first-wall materials that survive 14.1 MeV neutron fluences at the levels needed for commercial operation. Tungsten, ODS steels, and other materials under development for ITER and DEMO first walls are irrelevant for CHARM. There is still wall loading from energetic plasma electrons (bremsstrahlung) and synchrotron radiation — ARPA-E slide 19 identifies synchrotron radiation as "manageable through reabsorption" — but this is a qualitatively different and less severe materials challenge than neutron damage. [5]

**Central Electrode and Wall Materials**

CHARM's biased central electrode must maintain up to ~100 kV (comparable to CMFX's 100 kV design) against plasma erosion and resistive losses. Materials for high-voltage electrodes in plasma environments are a potential concern — arcing, sputtering, and contamination of the plasma with electrode material could degrade confinement and increase radiation losses. No electrode material specification for CHARM has been published.

---
[1] dossier.md, §Fuel: "The entire concept is designed around p-B11's mass disparity."
[2] arpa-e-fisch-2025-presentation.md, §Why p-B11?; 11-magnetic-mirror analysis §Section 4 (tritium supply chain characterization from D-T mirror).
[3] dossier.md, §Magnet Type; 11-magnetic-mirror analysis §Section 4 (REBCO supply chain from Realta analysis, reused by reference).
[4] dossier.md, §Primary Heating (alpha channeling RF mechanism).
[5] arpa-e-2025-fisch-presentation-notes.md, §Summary of Derisked Questions: "Synchrotron radiation is manageable through reabsorption."

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fuel type | p-B11 | arpa-e-fisch-2025-presentation.md §Why p-B11? | high | Aneutronic — no tritium, negligible neutron production |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | Continuous E×B rotation; no pulse required |
| ARPA-E funding | $1.5M (OPEN 2021) | princeton-arpa-e-funding-2022.md §Key Facts | high | Only disclosed funding; company not yet capitalized |
| Required proton temperature | ~150–300 keV | princeton-arpa-e-funding-2022.md §Technical Approach | medium | Range for p-B11 fusion; p-B11 cross-section peaks at ~600 keV |
| Alpha channeling gain factor (thermal) | 2.6× reduction in required τ_E | technical-papers-summary.md §Lowering reactor breakeven (2024) | medium | Analytical result from Ochs & Fisch 2024; not experimentally validated |
| Alpha channeling gain factor (fast proton hybrid) | 6.9× reduction in required τ_E | technical-papers-summary.md §Wave-supported hybrid fast-thermal pB11 fusion (2022) | medium | Hybrid scheme; most optimistic analytical case; key physics bet |
| CMFX mirror ratio | 10 (3 T / 0.3 T) | technical-papers-summary.md §Related: CMFX | high | Separate UMD experiment; validates centrifugal mirror geometry, not CHARM |
| CMFX electrode voltage | up to 100 kV | technical-papers-summary.md §Related: CMFX | high | DC power supply; analogous to Pale Blue's biased electrode concept |
| CMFX device length | 6.7 m | technical-papers-summary.md §Related: CMFX | high | Small experiment, not reactor scale |
| Neutron energy fraction | <1% | arpa-e-fisch-2025-presentation.md §Why p-B11?; p-B11 reaction physics | high | Near-aneutronic: essentially all energy in 3 charged alpha particles |
| Tritium breeding requirement | N/A | dossier.md §Tritium Breeding | high | Aneutronic fuel cycle; no breeding blanket required |
| Peer-reviewed publications | 29 (2022–2025) | arpa-e-2025-fisch-presentation-notes.md §Key Publication List | high | All plasma physics; no engineering design papers |
| Patent applications filed | 4 (March–April 2025) | arpa-e-2025-fisch-presentation-notes.md §Patent Applications | high | Physics and architecture patents; no device specs implied |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net electric output (plant) | truly-unknown | blocking | No plant design exists; no design point published at any scale |
| Plasma Q or fusion gain target | truly-unknown | blocking | Not published; depends on all physics bets working simultaneously |
| Alpha channeling efficiency η_α (experimental) | truly-unknown | blocking | Only analytical estimates; no experimental measurement in any device |
| Effective gain including bremsstrahlung losses | truly-unknown | blocking | Fundamental uncertainty; depends on nonthermal proton fraction and η_α |
| Rotation sustainment power (recirculating fraction) | truly-unknown | blocking | Not characterized; key LCOE input |
| DEC efficiency (rotation energy recovery) | truly-unknown | blocking | PRX Energy paper covers physics limits only; no engineering efficiency target |
| Total plant capital cost | truly-unknown | blocking | No cost study of any kind |
| LCOE estimate or target | truly-unknown | blocking | No company or independent estimate |
| Magnet field strength and conductor type | truly-unknown | blocking | Not disclosed; concept-defining but unanswered |
| Machine size (plasma radius, length) | truly-unknown | blocking | No reactor concept study published |
| Capacity factor / maintenance philosophy | truly-unknown | important | Steady-state operation implies high availability in principle; no analysis |
| Thermal vs. direct conversion energy split | truly-unknown | important | All fusion energy in charged particles; some fraction may be radiative (synchrotron, bremsstrahlung) — split unknown |
| B-11 enrichment requirement and cost | truly-unknown | important | Enrichment level not specified; cost depends on purity target |
| Electrode material and lifetime | truly-unknown | important | No specification; erosion and contamination not characterized |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Any reactor design point: fusion power, plasma parameters, machine geometry | S1, S5 | truly-unknown | blocking | Requires Pale Blue Fusion to publish a conceptual design — no external source can fill this |
| 2 | Alpha channeling efficiency η_α: experimental measurement | S2, S3, S5 | truly-unknown | blocking | First requires a rotating plasma experiment with relevant wave heating; CMFX could be a testbed if upgraded |
| 3 | Effective gain including bremsstrahlung accounting (full power balance) | S2, S5 | truly-unknown | blocking | 0D (PB)² code exists but outputs not published; Pale Blue technical disclosure needed |
| 4 | Rotation sustainment power: steady-state recirculating fraction | S2, S5 | truly-unknown | blocking | Depends on plasma resistivity and rotation energy confinement time; no published measurement |
| 5 | DEC efficiency for rotation energy recovery | S2, S3, S5 | truly-unknown | blocking | PRX Energy 2025 paper provides physics bounds; engineering efficiency target unpublished |
| 6 | Total capital cost at any level | S5 | truly-unknown | blocking | No cost study exists; no component-level estimates |
| 7 | Magnet technology choice and field requirements | S3, S4 | truly-unknown | blocking | Not disclosed; required mirror ratio for CHARM is not published |
| 8 | p-B11 nonthermal plasma demonstration at any scale | S2, S3 | truly-unknown | blocking | Conceptually the most important experimental gap; no existing experiment achieves required conditions |
| 9 | CHARM multi-chamber architecture proof-of-concept | S3 | truly-unknown | blocking | No experiment; required prior to any engineering cost study |
| 10 | Ponderomotive barrier experimental demonstration | S3 | truly-unknown | important | Theory derisked; experimental validation required for concept credibility |
| 11 | B-11 enrichment requirement and cost | S4, S5 | not-yet-sourced | important | Published in enrichment/isotope literature; Pale Blue has not specified purity requirement |
| 12 | Synchrotron radiation: reabsorption efficiency and wall loading | S2, S3 | truly-unknown | important | Identified as manageable in slide 19; no quantification published |
| 13 | Capacity factor and maintenance philosophy for open-end geometry | S5 | truly-unknown | important | Open-ended geometry may enable simpler maintenance than toroids; no study |
| 14 | Company status: incorporation, funding rounds, device roadmap | S1 | not-yet-sourced | nice-to-have | As of July 2025 pre-incorporation; 2026 news may include incorporation/funding |

---

## Section 7: Cross-Concept Notes

Five approved prior analyses were consulted: 11-magnetic-mirror (Realta D-T), 08-frc-w-direct-conversion (Helion D-He3), 01-hts-compact-tokamak (handwritten), 07-maglif (handwritten), and 21-spherical-tokamak-hts.

**Shared mirror confinement basis with 11-magnetic-mirror (Realta D-T)**

CHARM and Realta's Hammir both use magnetic mirror confinement, but the physics of the two concepts diverges substantially. Realta uses a classical tandem mirror with D-T fuel, neutron-producing plasma, and relies on HTS end plugs to create electrostatic plugging potentials. CHARM uses centrifugal confinement from E×B rotation, p-B11 fuel, and relies on mass disparity for species separation rather than electrostatic potentials. The mirror geometry (outer coils, inner coils, solenoidal architecture) is shared at the coil level, and the CMFX experiment (which validates centrifugal mirror physics) uses a mirror ratio of 10 — similar to what Realta uses with HTS at WHAM.

The characterization of REBCO supply chain from the 11-magnetic-mirror analysis is reused here conditionally: if CHARM adopts HTS magnets, the same tape quantity concerns (thousands of km/year current capacity, $30–100/kA-m price) apply. The DEC challenge is superficially shared — both concepts include energy conversion from escaping charged particles — but the mechanisms differ: Realta targets escaping D-T end-loss ions via venetian-blind collectors, while CHARM targets rotational kinetic energy recovery.

The critical divergence is the fuel cycle. The 11-magnetic-mirror analysis is dominated by D-T challenges: tritium breeding, blanket engineering, neutron damage, Li-6 enrichment, CANDU dependence. All of these are absent for CHARM, which instead faces the harder underlying physics challenge of p-B11 breakeven.

**Fuel cycle comparison with 08-frc-w-direct-conversion (Helion D-He3)**

Both CHARM and Helion's FRC target aneutronic or near-aneutronic fuel cycles to eliminate tritium and neutron challenges. Helion targets D-He3, which requires temperatures 3–4× higher than D-T but much lower than p-B11; CHARM targets p-B11, which requires temperatures ~9× higher than D-T. Both rely on direct energy conversion as the primary energy extraction pathway, bypassing the conventional thermal cycle. The handwritten 08-frc-w-direct-conversion exemplar notes that "D-He3 capital cost is extremely cheap, with cheap coils and no tritium breeding" — this structural argument applies even more strongly to p-B11, which has no neutron activation of coils at all. However, Helion is an operational experiment with 7 prototype generations; Pale Blue has no hardware.

The He3 supply constraint identified for Helion (global production ~8 kg/year, cost $2,000–$15,000/NTP-liter) does not apply to CHARM. Boron-11 is abundant and cheap. This is a supply chain advantage for CHARM over Helion, though it is irrelevant until the physics is demonstrated.

**DEC analogues across concepts**

Three approved concepts include DEC: 11-magnetic-mirror (venetian-blind DEC for D-T end-loss ions), 08-frc-w-direct-conversion (inductive energy recovery from compressed FRCs), and CHARM (rotation energy recovery). All three are at low TRL for their specific DEC implementation, and none have published efficiency numbers or capital cost estimates for their production designs. The 1983 MARS study value (~54% for gridless end-loss DEC) is the only empirical DEC efficiency number in the literature; it applies most directly to 11-magnetic-mirror and least directly to CHARM's rotation energy recovery approach.

**REBCO supply chain**

The global REBCO supply chain characterization from 01-hts-compact-tokamak and 11-magnetic-mirror applies to CHARM conditionally (if HTS is adopted). No additional analysis is required here — the constraints are the same.

---

## Section 8: Sources

**Primary Sources (used directly)**

1. **Fisch, N., et al.** "Economical Proton-Boron11 Fusion" — ARPA-E Programs Annual Meeting, July 9, 2025. 20-slide presentation covering CHARM architecture, derisked physics, computational tools, patent portfolio, company pivot. Primary source for this analysis.
   - Phase 1a path: `iter-01/sources/arpa-e-fisch-2025-presentation.md` and `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md`

2. **Princeton University Press Release** (March 10, 2022): "Fisch receives funding for 'unlikely but fantastic' clean energy technology." ARPA-E OPEN 2021 grant announcement; key facts on funding and concept rationale.
   - Phase 1a path: `iter-01/sources/princeton-arpa-e-funding-2022.md`

3. **Fisch Group Publication Summary** — Phase 1a-synthesized summary of 7 key technical papers from the Princeton group (2006–2025), including alpha channeling theory, wave-supported hybrid pB11 fusion, CMFX description, and ponderomotive barriers.
   - Phase 1a path: `iter-01/sources/technical-papers-summary.md`

4. **Phase 1a Dossier** — per-column research summary with confidence ratings and citations for all CHARM differentiation table values.
   - Path: `phase_1a/research/06-magnetic-mirror/dossier.md`

**Peer-Reviewed Literature (cited by dossier and presentation)**

5. **Fisch, N. J.** "Alpha channeling in mirror machines." *Phys. Rev. Lett.* 97, 225001 (2006). Foundational paper establishing the alpha channeling concept in mirrors.

6. **Ochs, I. E., Kolmes, E. J., Mlodik, M. E., Rubin, T., Fisch, N. J.** "Improving the feasibility of economical proton-boron-11 fusion via alpha channeling with a hybrid fast and thermal proton scheme." *Phys. Rev. E* 106, 055215 (2022). Hybrid proton scheme; 6.9× confinement time reduction.

7. **Kolmes, E. J., et al.** "Wave-Supported Hybrid Beam-Thermal pB11 Fusion." *Physics of Plasmas* 29, 110701 (2022). Hybrid fast-thermal scheme mechanism.

8. **Ochs, I. E., Fisch, N. J.** "Lowering the reactor breakeven requirements for p-B11 fusion." *Physics of Plasmas* 31, 012503 (2024). 2.6–6.9× breakeven improvement from alpha channeling.

9. **Ochs, I. E., Kolmes, E. J., Fisch, N. J.** "Preventing ash from poisoning proton-boron 11 fusion plasmas." *Physics of Plasmas* 32, 052506 (2025). Multi-region spatial separation approach for helium ash.

10. **Rax, J. M., Kolmes, E. J., Fisch, N. J.** "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields." *PRX Energy* 4, 013007 (2025). DEC efficiency physics basis for rotation energy recovery.

11. **Rubin, T., Fisch, N. J.** "Ponderomotive barriers in rotating mirror devices using static fields." *Physics of Plasmas* 32, 062104 (2025). One-way RF wall concept for ion traffic control.

12. **Kolmes, E. J., Ochs, I. E., Fisch, N. J.** "Ion Mix Can Invert Centrifugal Confinement." arXiv:2504.18634 (2025, submitted to PRL). Third-species end-plug enhancement.

**Patent Applications (cited by dossier)**

13. US 19/083,790 — "Nonthermal Proton-Boron11 Fusion with Separated Reactant Regions" (March 2025)
14. US 19/084,168 — "Enhanced Particle Confinement with Positive and Negative Ponderomotive Potentials" (March 2025)
15. US 19/175,473 — "Systems and Methods for Producing Ultra-high DC Voltages in Open Field Line Traps" (April 2025)
16. US Provisional 63/794,470 — "Differential Confinement, Mixing, and Demixing of Plasma in a Rotating Trap" (April 2025)
17. US20230298771 — "Direct Energy Converter for Axisymmetric Mirror Fusion Reactor" (SWDEC, 2023)

**Cross-Concept Analyses (consulted)**

18. **11-magnetic-mirror analysis** (Realta D-T): Magnetic mirror supply chain, DEC context, REBCO characterization. `analyses/11-magnetic-mirror/analysis.md`
19. **08-frc-w-direct-conversion analysis** (Helion D-He3): Aneutronic fuel cycle economics, DEC in pulsed context. `analyses/08-frc-w-direct-conversion/analysis.md`
20. **01-hts-compact-tokamak handwritten**: REBCO supply chain baseline. `handwritten/01-hts-compact-tokamak.md`
