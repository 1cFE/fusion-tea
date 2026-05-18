---
ID: 37-magnetized-target-inertial-fusion-mtif
Concept: Magnetized Target Inertial Fusion - MTIF (D-D)
Company: NearStar Fusion
Status: draft
Created: 2026-05-17
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Magnetized Target Inertial Fusion - MTIF (D-D) (NearStar Fusion)

**Concept**: Magnetized Target Impact Fusion (MTIF) — D-D fuel, plasma-armature railgun driver
**Company**: NearStar Fusion (Huntsville, AL)
**Confinement Family**: MIF — Magnetized Target (projectile compression)

---

## Section 1: Availability of Data

**Rating: Opaque**

NearStar Fusion is an early-stage company with essentially no public technical disclosures beyond its corporate website and a small set of investor-facing materials. After two research iterations, the available source base comprises two locally extracted summaries totaling approximately 3 KB of text. No peer-reviewed publications, preprints, white papers, plant studies, or system-code outputs are available. NearStar has not disclosed any funded DOE or ARPA-E program participation, nor have NearStar-associated researchers appeared in conference abstracts in the sources available.

> "Magnetized Target Impact Fusion (MTIF)…compressing, heating and magnetizing fusion fuel simultaneously"
> — nearstar-website-summary.md, §Concept

> "able to retrofit the heat source in traditional hydrocarbon (e.g., coal) power plants with a fusion power core to leverage existing turbines and power grid infrastructure"
> — nearstar-energy-capture-research.md, §Key finding

The sole published quantitative technical facts are: capsule mass (~50 g), capsule velocity (~10 km/s), minimum kinetic energy delivered per shot (>1 MJ), and repetition rate (1 Hz). No fusion gain target, no net electrical output, no capital cost estimate, no thermal efficiency, and no experimental results are available publicly.

**Company transparency:** NearStar's public profile is at the far low end relative to other concepts in this portfolio. Conceptually adjacent companies — General Fusion (concept 14, pneumatic MTF) and First Light Fusion (concept 22, projectile ICF) — have both published quantitative design parameters, partnership disclosures, and in First Light's case peer-reviewed experimental results. NearStar has published none of these. Investor press releases confirm venture capital investment (Virginia Venture Partners, Ecosphere Ventures) but disclose no funding quantum or technical milestones [dossier.md §Key Sources].

**Independent analyses:** No third-party techno-economic or physics assessment of NearStar's specific approach was found. The generic MIF and inertial confinement literature provides physical context but cannot substitute for concept-specific data.

**Phase 1a dossier completeness:** The dossier achieved high confidence on confinement family, fuel, primary heating mechanism, operation mode, and repetition rate. Medium confidence on blanket configuration (Pb liquid metal classification) and energy capture (steam Rankine inferred from coal retrofit framing). Low confidence or gaps on magnet type / pellet pre-magnetization, driver electrical efficiency, fusion gain, and virtually all quantitative performance parameters.

**Key data gaps limiting this analysis:**
1. Fusion gain (Q) — no target disclosed
2. Net electrical output — no design-point power stated
3. Railgun electrical efficiency — determines actual driver energy cost
4. Lab-scale experimental results — no demonstration of D-D compressed plasma
5. Capital cost of any subsystem
6. Pellet pre-magnetization mechanism details

---

## Section 2: Challenges in Capturing System Function

Five major modeling challenges are identified, ranked by LCOE impact.

**1. D-D ignition physics is the dominant cost and viability uncertainty (Impact: Critical)**

NearStar's primary fuel is D-D, chosen to eliminate tritium handling. The physics consequence is severe: the D-D fusion cross-section is approximately 100× lower than D-T at temperatures in the 10–30 keV range where fusion concepts typically operate, and the minimum self-heating temperature for D-D is substantially higher than for D-T. For magnetized target compression of a D-D plasma, achieving ignition requires either much higher compression ratios, much higher seed magnetic fields, or much higher initial plasma temperatures than the D-T equivalent — all of which are undemonstrated at any scale. NearStar publishes no gain target, no simulation results, and no physical argument for the ignition margin. This is not a LCOE parameter uncertainty; it is an uncertainty about whether the concept can produce net fusion energy at all. Until D-D ignition is demonstrated or credibly modeled for this driver geometry, the LCOE model has no physics anchor.

The D-D reaction produces two roughly equal branches: D+D → T (1.01 MeV) + p (3.02 MeV) and D+D → He-3 (0.82 MeV) + n (2.45 MeV). These secondary products — tritium and He-3 — can undergo further reactions in situ, raising effective energy yield, but simultaneously introducing trace tritium handling and inventory concerns even in a nominally D-D system. No data from NearStar addresses this issue.

**2. Energy balance and required target gain are not established (Impact: Critical)**

At 1 Hz with >1 MJ kinetic energy delivered per shot, achieving 100 MWe net requires fusion yield on the order of several hundred MJ per shot (assuming ~35% thermal-to-electric conversion and non-trivial railgun electrical efficiency). The implied target gain is in the range of 100–300, which far exceeds any demonstrated or credibly projected gain for D-D fuel in any inertial confinement scheme. Published gain projections for D-T magnetized target fusion from analogous concepts target gains of approximately 5–15 (General Fusion) to 30–100 (MagLIF simulations at 60+ MA). No equivalent gain analysis exists for NearStar's configuration. The entire economic case depends on a target gain that is not quantified, not modeled publicly, and not validated experimentally.

Even modest changes in assumed gain (3× vs. 30×) shift the LCOE by an order of magnitude. Without a gain anchor, sensitivity analysis cannot be meaningfully bounded.

**3. Railgun wear and replacement rate at 1 Hz operation (Impact: High)**

Plasma-armature railguns operating at Mach 30 (10 km/s) subject the rail surfaces to extreme electromagnetic erosion, thermal ablation, and mechanical stress. At 1 Hz over a plant lifetime, the railgun fires approximately 28 million shots per year, or roughly 840 million shots over 30 years. Documented rail lifetimes in defense hypervelocity programs range from approximately 12 shots in early systems to a contested milestone of ~400 shots — achieved at unconfirmed full power — in a program that the U.S. Navy cancelled in its FY2022 budget after spending approximately $500M over 17 years without meeting its 3,000-shot, 10-round-per-minute development target [en-wiki-railgun.md §Naval Research]. The characterization of "hundreds to a few thousand shots" as a typical range overstates demonstrated capability; the 400-shot figure is the best-documented upper end, and the 3,000-shot goal was never achieved before program cancellation. The gap between the best documented defense result (~400 shots) and commercial fusion requirements (~840 million shots over 30 years) is approximately eight orders of magnitude, not six. At 1 Hz, rails lasting 400 shots require replacement approximately every 7 minutes — a maintenance cadence incompatible with any conventional power plant operating paradigm. Rail replacement frequency constitutes both a capacity factor constraint and a direct consumable cost that scales with shot count, independent of fusion output.

**Breakeven framing:** Sensitivity analysis identifies availability (elasticity ≈ −1.0) and fusion gain Q_eng (elasticity ≈ −0.33) as the dominant LCOE levers. At nominal assumed availability of 0.40, LCOE is approximately 190 $/MWh. A commercially viable threshold (~80 $/MWh) requires availability in the range of 0.65–0.70 — roughly double the nominal assumption. Converting to a physical rail life requirement: if each replacement event takes 1 hour (shutdown, swap, restart), maintaining 0.70 availability at 1 Hz requires rails lasting ≥ ~12,000 shots per replacement interval — approximately 30× the best documented defense result. This gap must be closed on the O&M dimension alone before fusion gain even enters the viability calculation. No data suggests a credible development path to 12,000-shot rail life in fusion duty-cycle conditions. No data exists from NearStar on expected rail life, replacement schedule, or replacement cost.

**4. Coal-plant retrofit integration: thermal matching and site constraints (Impact: Moderate)**

NearStar frames its commercial product as a heat-source retrofit for existing coal plants, capturing the existing steam turbines, generators, grid interconnects, and civil infrastructure. This is a genuine potential cost advantage if it works as described. However, the strategy depends on thermal output matching the host plant's requirements. Existing coal plants operate at subcritical or supercritical steam conditions (500–600°C, 10–25 MPa for supercritical units), and the thermal output of NearStar's fusion core must drive a Pb primary loop, an intermediate heat exchanger, and a steam generator capable of meeting these conditions. Molten Pb thermal hydraulics at plant scale — including operating temperature, intermediate loop design, and heat exchanger materials — are not disclosed. The retrofit strategy also faces a non-technical constraint: coal plants are being decommissioned rapidly. The window during which a fusion heat source could be retrofit into operating coal-plant infrastructure at scale is probably narrower than the time needed to commercialize the technology.

**5. Absence of experimental validation for any fusion-relevant subsystem (Impact: High)**

Unlike MagLIF, which has over 70 integrated fusion experiments at the Z machine, or General Fusion, which has operated plasma injectors and rotating liquid metal experiments, NearStar provides no evidence of any experiment relevant to MTIF performance — no compressed plasma data, no neutron yield measurements, no rail gun tests at the stated velocity and projectile mass for this application. The university partnerships mentioned (UAH, Texas A&M) are not associated with published MTIF experiments in the available sources [dossier.md §Remaining Gaps]. The LCOE model for this concept cannot be grounded in any empirical validation of the core subsystem chain.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**D-D Magnetized Target Physics (TRL 1–2)**

- **Demonstrated**: D-D fusion in simple devices (Farnsworth-Hirsch, Z-pinches) at negligible yield. Magnetized target fusion experiments at General Fusion and Sandia have targeted D-T fuel; the MIF physics database for D-D is sparse. No published experiment has achieved magnetized D-D compression to ignition-relevant conditions in a geometry analogous to NearStar's.
- **On paper only**: Gain projections for a railgun-driven magnetized D-D target. Minimum target conditions (density, temperature, magnetic field) for net fusion energy with D-D fuel. Secondary tritium and He-3 burn-up fractions and their energy contribution.
- **Missing at scale**: Any integrated D-D magnetized target experiment. Scaling of compression physics from D-T analogues to D-D requirements. Suppression of energy losses (Bremsstrahlung, electron thermal conduction) in a D-D compressed plasma with the Pb-shockwave boundary condition.

---

**Pellet Pre-Magnetization (TRL 2–3)**

- **Demonstrated**: Seed field generation for magnetized target fusion has been demonstrated by General Fusion (magnetized plasma injectors) and in MagLIF (external Helmholtz coils, now being replaced by self-magnetizing targets). Neither approach is directly applicable to a 50 g hypervelocity capsule that must survive Mach 30 launch and maintain its seed field through extreme deceleration in the Pb chamber.
- **On paper only**: Pre-magnetization mechanism for NearStar's capsule design — the method (embedded coil, capacitor-driven θ-pinch, ferromagnetic core, or other) is not disclosed [dossier.md §Remaining Gaps]. Field survivability through the launch and impact sequence.
- **Missing at scale**: Validation that any pre-magnetization approach survives the mechanical and electromagnetic environment of a 10 km/s railgun launch. Compatibility of the magnetization mechanism with the 1 Hz production and insertion cadence.

---

**Plasma-Armature Railgun Driver (TRL 3–4)**

- **Demonstrated**: Plasma-armature railguns achieving hypervelocities in the 10 km/s range are documented in defense research (U.S. Navy, BAE Systems, General Atomics electromagnetic launch programs). These programs have achieved velocities of 5–8 km/s with solid armatures and higher with plasma armatures at smaller scale. The physics of plasma-armature operation, rail erosion, and armature acceleration is reasonably well understood. **However, the U.S. Navy terminated its railgun R&D program in its FY2022 budget — after spending approximately $500M over 17 years — citing barrel durability and rate-of-fire limitations as the disqualifying obstacles [en-wiki-railgun.md §Naval Research].** Documented rail life in the most advanced test systems reached only ~400 shots at unconfirmed full power; the program's 3,000-shot development goal was never achieved. The defense programs therefore represent not a successful proof-of-concept pathway but a terminated effort that ran into exactly the rail erosion challenges NearStar must solve at roughly eight orders of magnitude greater cumulative shot count. TRL 3–4 is appropriate for the underlying physics, but there is no ongoing program establishing a path to higher TRL for fusion-relevant duty cycles.
- **On paper only**: Rail and armature design for 50 g capsule mass at sustained 10 km/s at 1 Hz. Rail erosion lifetime model for fusion application duty cycles. Capsule structural integrity through launch (the 50 g pre-magnetized, cryogenic-or-dense-gas fuel capsule must survive Mach 30 acceleration without disrupting the seed field or the fuel geometry).
- **Missing at scale**: Any railgun demonstration at or near the required duty cycle (1 Hz, 10 km/s, 50 g armature) for fusion plant lifetimes. Rail erosion characterization over millions of shots at these parameters. Automated capsule loading and chambering at 1 Hz cadence. Electromagnetic compatibility between the railgun's current pulse and surrounding plant equipment.

---

**Molten Lead First Wall and Target Chamber (TRL 3–4)**

- **Demonstrated**: Lead-cooled fast reactor (LFR) research has characterized liquid Pb and Pb-Bi eutectic (LBE) thermal hydraulics, corrosion of structural steels, and handling at industrial scale. MYRRHA (Belgium) and BREST-OD-300 (Russia) programs provide the most complete engineering databases for liquid Pb fission systems. Liquid-metal first-wall concepts for fusion have been studied in the context of FLiBe (Z-IFE), Pb-17Li (EU), and Li metal (ST-E1), providing analogous engineering references, though none with the specific Pb chemistry and projectile-impact geometry of NearStar's design.
- **On paper only**: Liquid Pb chamber that absorbs hypervelocity projectile impact (shockwave dynamics in molten Pb from a Mach 30 impactor at 1 Hz), reforms between shots, and maintains thermal steady state. Heat extraction from a turbulent, shock-disturbed Pb pool into a secondary steam circuit.
- **Missing at scale**: Any experiment testing shockwave dynamics in molten Pb from hypervelocity impact at 1 Hz. Lead activation product inventory (particularly Po-210 from Pb-208 neutron capture in an LFR context — less severe for D-D neutrons at 2.45 MeV than for 14.1 MeV D-T neutrons, but still a radiological management concern). Structural materials corrosion lifetime in flowing Pb at fusion thermal loads.

**O&M Considerations**: No O&M cost breakdown is disclosed. For an analogue, MIF pulsed concepts (MagLIF concept 07, General Fusion concept 14) have flagged periodic replacement of consumables (RTL, liner/target) as a dominant operating cost. For NearStar, the closest equivalent is rail replacement — the most plausible O&M cost driver. At 1 Hz, if rails last 400 shots (the best documented defense program result at unconfirmed full power [en-wiki-railgun.md §Naval Research]), replacement is required approximately every 7 minutes — a cadence so extreme it renders sustained operation effectively impossible. Even at a highly aspirational 10,000-shot rail life (25× better than the documented defense result), replacement is required every ~3 hours. Rail replacement must therefore appear in the model as two distinct entries: a capacity factor penalty (encoded in availability) and a direct per-shot consumable cost for rail material and replacement labor. Treating it only as an availability reduction understates the operating cost burden. Target capsule fabrication at 1 Hz (28M/year) constitutes a second consumable cost line: IFE target fabrication benchmarks (National Academies IFE study) require ~$0.25–$0.30/target for power plant viability — a 10,000× reduction from current research-scale costs — and NearStar's capsule (50 g, pre-magnetized, must survive Mach 30 launch) is structurally more complex than conventional ICF pellets, placing it well above that baseline. At 28M shots/year, even $0.50/capsule yields $14M/year in capsule cost alone. Fixed O&M (labor, utilities, cooling water, pumps) follows conventional thermal plant patterns and is the most tractable component.

---

**Tritium Handling (TRL N/A — not required as primary fuel)**

D-D fuel eliminates the tritium startup inventory requirement (~1 kg at >$35,000/g) and the tritium breeding blanket engineering challenge that dominates D-T concept risk. However, D-D reactions generate tritium as a product of the D+D → T + p branch (~50% of reactions). In a high-gain D-D device, this secondary tritium partially burns in situ via D+T → He-4 + n (14.1 MeV), boosting energy yield. Unburned secondary tritium accumulates in the Pb first wall and exhaust, requiring some degree of tritium monitoring and handling even in a nominally D-D plant. At any credible gain, the secondary tritium inventory is small relative to D-T fusion plants, but it is not zero. NearStar's website cites the absence of tritium as a simplification [nearstar-website-summary.md, §Fuel]; the degree of simplification depends on achieved gain and burn-up fraction of secondary T.

---

**Balance of Plant / Steam Energy Conversion (TRL 7–9)**

- **Demonstrated**: Steam Rankine power conversion at 50–1000 MWe scale is commercially mature. Coal plant steam systems (subcritical and supercritical Rankine) are fully industrialized. Molten-Pb-to-steam heat exchangers are being developed for LFR fission applications (ALFRED, BREST) with the key challenge being Pb corrosion of secondary-side surfaces. NearStar's coal-plant retrofit strategy leverages this mature technology explicitly.
- **On paper only**: Intermediate loop design between molten Pb primary (fusion heat source) and steam secondary (coal plant). Temperature matching between Pb outlet temperature and existing coal plant steam conditions. Intermediate loop material selection for Pb compatibility at the coal plant's operating temperatures.
- **Missing at scale**: Thermal integration of a pulsed (1 Hz burst) heat source with a steady-state steam turbine. The 1 Hz shot cycle deposits thermal energy in discrete bursts; the Pb pool must buffer these pulses into a near-steady thermal output. Pb pool sizing for thermal buffering at fusion-relevant power levels is not addressed in available sources.

---

## Section 4: Key Materials and Supply Chain Considerations

**Lead (Molten Pb First Wall and Target Chamber) — Abundant, No Supply Constraint**

Lead is a commodity metal with global annual production exceeding 10 million tonnes, dominated by recycled sources (battery manufacturing). At fusion plant scale, the Pb inventory in the target chamber is on the order of tens of tonnes — a trivial demand fraction of global supply. Pb melting point (327°C) and boiling point (1749°C) define a wide operating window. The principal engineering constraint is not supply but materials compatibility: liquid Pb corrodes common steels (grain boundary attack, dissolution of Fe, Ni, Cr at elevated temperatures) above approximately 450–500°C. The LFR fission program has characterized surface oxide layer management in Pb-Bi eutectic as a mitigation — oxygen control in the Pb melt maintains a protective oxide layer on steel surfaces. These techniques are transferable to NearStar's Pb chamber but require dedicated process control. Pb activation under D-D neutrons (2.45 MeV) is milder than under 14.1 MeV D-T neutrons: Pb-204(n,γ) and Pb-206(n,γ) reactions are subdominant, and the notorious Po-210 pathway (Pb-208 → Bi-209 → Po-210 via neutron capture + β-decay) is activated primarily by slow neutrons in the LFR context and is less severe here. However, Pb activation management remains a radiological engineering consideration.

**No Tritium, No REBCO, No Beryllium, No FLiBe — Supply Chain Advantages**

NearStar's design requires none of the critical materials that constrain other fusion concepts in this portfolio:
- No tritium startup inventory (D-D fuel eliminates the ~1 kg, >$35,000/g startup requirement constraining all D-T concepts)
- No REBCO superconducting tape (no external magnets; global production capacity of a few thousand km/year is not a constraint)
- No beryllium (no FLiBe, no Be-containing neutron multiplier)
- No lithium-6 enrichment

This is a material supply chain advantage relative to all HTS-magnet MFE concepts and all D-T breeding blanket concepts in the portfolio. However, the advantage is conditional on the D-D fuel cycle delivering net energy — which is the central unresolved physics question.

**Railgun Materials — Wear-Dominated, No Established Supply Chain for Fusion Application**

Plasma-armature railguns require high-conductivity rail materials (typically oxygen-free copper or copper alloys) and insulating containment structures capable of withstanding repeated high-voltage, high-current pulses. At 1 Hz operation, rail erosion from ablation and arcing is severe. Defense hypervelocity programs have explored various rail liner materials (copper, molybdenum-copper composites, graphite liners) to extend rail life, but replacement rates at fusion plant cadences have not been characterized. At 28 million shots per year, even if each shot consumes a gram of rail material, the annual rail material throughput is tens of tonnes. The supply chain for precision-formed rail materials at this scale is not an existing industry.

**Deuterium Fuel — No Supply Constraint**

Deuterium is extracted from seawater at approximately $300–600/kg and is effectively inexhaustible. At 50 g capsules and fusion burn fractions of a few percent, the annual deuterium throughput is modest. Fuel cost is negligible in the LCOE — an assumption NearStar implicitly relies on in its clean-energy framing.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fuel capsule mass | ~50 g | nearstar-website-summary.md §Driver | high | Per shot; D-D fuel |
| Projectile velocity | ~10 km/s (Mach 30) | nearstar-website-summary.md §Driver | high | Plasma-armature railgun |
| Kinetic energy delivered per shot | >1 MJ | nearstar-website-summary.md §Driver | high | Minimum; actual depends on target-coupling efficiency |
| Repetition rate | 1 Hz | nearstar-website-summary.md §Concept | high | "once per second" |
| Operation mode | Pulsed | dossier.md §Operation Mode | high | Discrete shots at 1 Hz cadence |
| Fuel | D-D (primary); D-T (backup) | nearstar-website-summary.md §Fuel | high | D-D preferred to avoid tritium |
| Energy capture method | Thermal (steam Rankine) | nearstar-energy-capture-research.md §Key finding | medium | Inferred from coal-plant retrofit framing; specific Rankine parameters (subcritical/supercritical, operating temps) not disclosed |
| Blanket / first wall | Molten Pb | nearstar-website-summary.md §Concept | high | Non-breeding; neutron absorber and heat exchanger |
| Magnet type | None (external confinement) | dossier.md §Magnet Type | medium | Pellet is pre-magnetized; no external confinement coils; seed-field mechanism not disclosed |
| Driver electrical efficiency | [unknown] | No data in available sources | — | Railgun wall-plug-to-kinetic efficiency typically 20–40% for experimental systems; fusion plant optimized version uncharacterized |
| Thermal conversion efficiency | [estimated] ~33–38% | [analogue — subcritical/supercritical coal plant Rankine cycle, consistent with coal-plant retrofit framing; nearstar-energy-capture-research.md §Key finding] | low | Subcritical coal plants operate at 33–36%; supercritical at 36–42%; actual NearStar thermal parameters undisclosed |
| Net electrical output | [unknown] | No data in available sources | — | No design-point power stated |
| Fusion gain (Q) | [unknown] | No data in available sources | — | No target disclosed; physics-based minimum implied by D-D cross-sections is very high |
| Capital cost | [unknown] | No data in available sources | — | No estimate for any subsystem |
| Capacity factor | [unknown] | No data in available sources | — | Rail replacement rate and cadence TBD |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion gain / Q | truly-unknown | blocking | No published target or simulation; this is the concept's core viability question |
| Net fusion power per shot | truly-unknown | blocking | Required to compute LCOE; depends on gain × driver input energy |
| Net electrical output (MWe) | truly-unknown | blocking | Needed for capital cost denominator |
| Railgun wall-plug electrical efficiency | truly-unknown | blocking | Determines actual electrical energy cost per shot; experimental railguns ~20–40% |
| Target gain required for net electricity | derivable | blocking | Derivable from energy balance: yield > driver energy / (thermal efficiency × availability); currently requires gain assumption |
| Capital cost (total or by subsystem) | truly-unknown | blocking | No estimate available for any component |
| Rail lifetime and replacement cost | truly-unknown | blocking | Dominant OPEX unknown; best documented defense result ~400 shots at unconfirmed full power — gap of ~8 orders of magnitude between that and 30-year plant requirement (~840M shots). At 1 Hz, 400-shot rail life = replacement every ~7 min. |
| Capsule fabrication cost per shot | truly-unknown | important | IFE benchmark (nationalacademies-read-18289-chapter-5.md §Cost of Electricity): power plant viability requires ~$0.25–$0.30/target, a 10,000× reduction from current research-scale cost and 100,000× faster than current production rates. NearStar's capsule (50 g, pre-magnetized, must survive Mach 30 launch) is more complex than conventional ICF pellets — $0.25–$0.30 is an absolute lower bound. At 28M shots/year, even $0.50/capsule = $14M/year direct consumable cost. |
| Pellet pre-magnetization mechanism | proprietary | important | Not disclosed; affects per-shot cost, complexity, and failure modes |
| Pb primary loop operating temperature | proprietary | important | Determines compatibility with coal plant steam parameters and intermediate loop materials |
| Plant capacity factor | truly-unknown | important | Depends on rail replacement schedule and chamber maintenance; no basis for estimate |
| Secondary tritium inventory and handling cost | derivable | important | Derivable from gain and burn fraction; small but nonzero for D-D |
| D-D ignition conditions for this geometry | truly-unknown | blocking | No published simulation or experimental data for railgun-driven magnetized D-D target |
| Driver energy storage and recharge power | derivable | important | At 1 Hz, recharge power ≈ stored energy (MJ) × rep rate; stored energy unknown |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Fusion gain (Q) — no target or simulation published; concept's central viability question | S1, S2, S5 | truly-unknown | blocking | Patent search (assignee "NearStar Fusion"); APS DPP / IEEE SOFE abstracts; UAH / Texas A&M collaboration output |
| 2 | Net electrical output — no design-point power stated | S1, S5 | truly-unknown | blocking | Monitor investor disclosures; DOE Milestone program filings if NearStar participates |
| 3 | Railgun driver electrical efficiency and energy storage requirement | S2, S3, S5 | truly-unknown | blocking | Defense hypervelocity railgun literature (Navy, DARPA) provides range estimates; NearStar-specific values not public |
| 4 | Rail lifetime at 1 Hz, 10 km/s, 50 g plasma-armature duty cycle | S2, S3, S5 | truly-unknown | blocking | No published data for fusion application; bounds from defense railgun programs (US Navy, General Atomics EML) |
| 5 | D-D magnetized target ignition conditions for railgun-driven geometry | S2, S3, S5 | truly-unknown | blocking | No published simulation; General Fusion / Sandia MTF literature for D-T provides physical framework for scaling estimate |
| 6 | Pellet pre-magnetization mechanism and cost | S3, S5 | proprietary | important | USPTO patent search; APS DPP abstracts from UAH/TAMU collaborators |
| 7 | Per-shot capsule fabrication cost at 28M shots/year | S3, S5 | truly-unknown | important | National Academies IFE study benchmarks conventional ICF pellets at ~$0.25–$0.30/target for power plant viability (currently thousands of dollars each, requiring 10,000× cost reduction and 100,000× faster production). NearStar's capsule design complexity places it above this lower bound; NearStar-specific design not public. At 28M shots/year, $0.50/capsule = $14M/year. |
| 8 | Molten Pb primary loop operating temperature and pressure | S3, S4, S5 | proprietary | important | LFR fission literature (MYRRHA, BREST) provides Pb thermal-hydraulic engineering context; NearStar conditions undisclosed |
| 9 | Intermediate loop and heat exchanger design for Pb-to-steam coupling | S3, S5 | proprietary | important | LFR fission literature (ALFRED, BREST steam generator designs) provides engineering analog |
| 10 | Target gain required for net electricity (energy balance derivation) | S2, S5 | derivable | blocking | Computable once driver electrical efficiency and output power are estimated; requires gain assumption currently |
| 11 | Plant capacity factor | S5 | truly-unknown | important | Not estimable without rail lifetime and Pb chamber maintenance data |
| 12 | Secondary D-D tritium production and handling requirements | S3, S4 | derivable | important | Derivable from D-D reaction kinematics and gain assumption; small but nonzero |
| 13 | Capital cost for any subsystem | S1, S5 | truly-unknown | blocking | No public data; railgun defense costs provide approximate driver analog |
| 14 | Experimental validation of any MTIF-relevant subsystem | S1, S3 | truly-unknown | blocking | NearStar has not published any experimental results; UAH/TAMU partnership outputs are the most likely near-term source |
| 15 | Coal-plant retrofit compatibility (Pb outlet temp vs. host steam conditions) | S2, S3, S5 | proprietary | important | Subcritical coal plant steam data is public; Pb loop operating temperature is the missing input |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available for cross-referencing is concept 21, Spherical Tokamak - HTS (Tokamak Energy). The analytical overlap with NearStar MTIF is minimal: different confinement family (MFE vs. MIF), different fuel cycle (D-T vs. D-D), different driver physics (magnetic confinement vs. kinetic-impact compression), and no shared subsystems. The only transferable observations are:

- **D-T tritium constraints are absent here.** The ST-HTS analysis identified the global tritium inventory constraint (~25–30 kg, declining as CANDU reactors retire) and startup inventory cost (~1 kg at >$35,000/g) as a shared D-T concept constraint. NearStar's D-D fuel eliminates this constraint entirely — a genuine advantage relative to the ST-HTS and all other D-T concepts in the portfolio.

- **No REBCO supply chain constraint applies.** The ST-HTS analysis characterized the global REBCO production bottleneck and cost trajectory as a shared HTS-magnet concept constraint. NearStar requires no external magnets and no superconducting tape.

**Nearest conceptual neighbors (not yet approved analyses):** The concepts with the most structural relevance for cross-referencing are concept 14 (Magnetized Target Fusion — Pneumatic Compression, General Fusion), concept 22 (Projectile ICF, First Light Fusion), and concept 07 (MagLIF, Pacific Fusion). All three are in-progress analyses. Key comparisons for future iterations:

- *General Fusion (14)* shares the magnetized target compression architecture and liquid-metal first wall, but uses D-T fuel, pneumatic (not railgun) compression at ~150 m/s, and LiPb first wall for tritium breeding. NearStar replaces pneumatics with a hypervelocity railgun and Pb (non-breeding) first wall, and uses D-D fuel. The choice of D-D substantially raises the ignition bar; the choice of railgun substantially raises the driver velocity (enabling higher shock pressures). The driver capital structures are also fundamentally different: pneumatic pistons are a mature industrial technology with established suppliers and cost benchmarks, while plasma-armature railguns at NearStar's specifications require pulsed-power infrastructure (energy storage banks, high-current switches, precision firing circuits) with no commercial fusion precedent. Defense electromagnetic launcher programs provide rough order-of-magnitude capital estimates ($10s–$100s M$ per installation at duty cycles far less demanding than 1 Hz continuous), suggesting railgun driver capital may exceed a pneumatic piston baseline by a factor of several to an order of magnitude. Cost models that calibrate driver capital to pneumatic piston benchmarks likely understate this cost penalty.

- *First Light Fusion (22)* shares the projectile-impact driver concept, using an electromagnetic gun to accelerate a "shock driver" into a D-T target. First Light is D-T, uses projectile velocities in the same Mach 20–30 range, and has published experimental yield data — the most relevant experimental analog for NearStar's driver architecture. First Light's per-shot energy, however, is much lower, and its ICF physics (unmagnetized target) differs from NearStar's magnetized approach.

- *MagLIF (07)* shares the pulsed 1 Hz cadence, the liquid-metal first wall philosophy, and the magnetized target compression concept, but uses electrical (pulsed power) rather than kinetic energy delivery. The MagLIF analysis (handwritten exemplar) provides the most developed TEA framework for magnetized-target pulsed concepts and its pipeline design requirements (rep rate as first-class parameter, per-shot consumable costs, driver capital decomposition) apply directly to NearStar.

Cross-concept note on D-D fuel: Of the 39 concepts in the portfolio, D-D is used by only two: NearStar MTIF (this concept) and Cortex Fusion Laser ICF — Liquid Jet Target (concept 03, also early-stage with low confidence). Both D-D concepts face the same fundamental challenge: D-D cross-sections are approximately 100× lower than D-T at typical fusion temperatures, raising the ignition and gain threshold by a comparable factor. Neither concept has resolved this challenge publicly.

---

## Section 8: Sources

**1. NearStar Website Summary (iter-01)**
- Contribution: Sole source for quantitative technical parameters — capsule mass (~50 g), velocity (~10 km/s), kinetic energy (>1 MJ), repetition rate (1 Hz), fuel (D-D), first wall (molten Pb). Confirms concept name and classification as Magnetized Target Impact Fusion (MTIF). Documents D-D fuel choice rationale (tritium avoidance).
- Location: Phase 1a source — `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-01/sources/nearstar-website-summary.md`

**2. NearStar Energy Capture Research (iter-02)**
- Contribution: Confirms coal-plant retrofit strategy as primary commercial approach ("leverage existing turbines and power grid infrastructure"). Identifies molten Pb as primary heat-sink and intermediate loop fluid. Establishes thermal energy conversion as steam Rankine cycle by inference from retrofit framing. No additional quantitative parameters.
- Location: Phase 1a source — `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/iter-02/sources/nearstar-energy-capture-research.md`

**3. Phase 1a Dossier — Magnetized Target Inertial Fusion - MTIF (D-D)**
- Contribution: Synthesized column-by-column assessment with confidence ratings. Provides classification rationale, identified gaps in pellet pre-magnetization mechanism and energy capture cycle specifics, and key source index. The dossier's medium-high overall confidence rating reflects classification confidence, not physics or economic performance confidence.
- Location: `knowledge/concept_research/37-magnetized-target-inertial-fusion-mtif/dossier.md`

**4. D1+ Analysis: MagLIF (Pacific Fusion) — Handwritten Exemplar**
- Contribution: Provides the TEA framework and pipeline design requirements for pulsed magnetized-target fusion concepts most analogous to NearStar. Key transferable insights: rep rate as first-class economic parameter (not an operational detail), per-shot consumable cost structure, driver capital as a novel cost category, and the challenge of achieving GJ-class yields at ~1 Hz cadence. Referenced for conceptual framework only; no MagLIF-specific quantitative assumptions are transferred.
- Location: `exploration/concept_analysis/handwritten/07-maglif.md`

**5. D1+ Analysis: Spherical Tokamak - HTS (Tokamak Energy) — Approved Prior Analysis**
- Contribution: Limited cross-concept relevance. Provides reference characterization of D-T tritium startup constraints ($35,000/g, global inventory ~25–30 kg) and REBCO supply chain constraints that are absent from NearStar's D-D concept. No analytical assumptions are transferred from this analysis.
- Location: `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

**6. Lead-Cooled Fast Reactor (LFR) Engineering Literature (not directly ingested — background context)**
- Contribution: Provides engineering context for liquid Pb materials compatibility, corrosion management, activation products (Po-210 pathway), and structural materials selection (T91, oxide-dispersion-strengthened steels) used for Pb-facing components. The MYRRHA and BREST-OD-300 programs are the most relevant public references for Pb engineering at power-plant scale. These are well-known landmark programs referenced for context only — no specific claims from this literature are made in the analysis.
- Location: Not ingested; available through standard nuclear engineering references.

---

*No YAML frontmatter included — generated by pipeline.*
