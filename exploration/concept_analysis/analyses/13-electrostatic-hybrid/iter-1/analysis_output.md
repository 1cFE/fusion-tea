# D1+ Analysis: Electrostatic Hybrid (D-T) — Avalanche Energy Orbitron

**Concept**: Orbitron — crossed-field magneto-electrostatic fusion device
**Company**: Avalanche Energy (Seattle, WA)
**Confinement Family**: Electrostatic (Non-Standard)
**Fuel**: D-T (primary); p-B11 (future aspiration)

---

## Section 1: Availability of Data

**Rating: Limited**

Avalanche Energy is a small, early-stage private company. Public technical disclosure is fragmentary and dominated by marketing materials. After one research iteration, the available corpus consists of: two peer-reviewed journal publications (accessible as abstracts only), one extended technical blog post from a 2023 conference, two funding/milestone press releases, a $10M state grant announcement, a product page, and a single forum thread. No plant study, techno-economic analysis, independent assessment, or detailed engineering design has been published.

**Peer-reviewed publications (abstracts only):**
Two papers confirm the experimental program is real:

> "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" — *AIP Advances* 14(8), 085025 (August 2024)

> "Mode-enhanced ion loading in a 100 kV orbitrap" — *Physics of Plasmas* 32(9), 092105 (September 2025)

Only abstracts were accessible; neither paper's full text, experimental data, or measured parameters are available in the Phase 1a source corpus. This is the most significant data gap: the quantitative experimental record is behind a paywall.

**Technical blog post — primary engineering source:**
The CWFest 2023 blog post (`avalanche-cwfest2023-blog.md`) is the most substantive public technical document. It describes the device architecture, operating point targets, the two major physics critiques leveled at electrostatic fusion, Avalanche's claimed responses to those critiques, and preliminary subsystem layout. All operating targets cited in this analysis derive from this source.

**Press releases and grant documentation:**
The $29M Series A announcement (`avalanche-29m-raise-2026.md`) confirms the Q>1 D-T test program intent and FusionWERX facility plans. The 300 kV milestone release (`avalanche-300kv-press-release.md`) provides the most specific technical milestone: steady-state 300 kV sustained for hours at 3 W power draw. The FusionWERX grant release (`avalanche-fusionwerx-grant.md`) confirms $10M in state funding and tritium handling capability at the Richland, WA facility.

**Independent analysis:**
None found. No university groups, national labs, or fusion TEA frameworks have published analyses of the Orbitron concept. The electrostatic fusion family more broadly (IEC fusors, Polywell) has an academic literature, but the Orbitron's specific crossed-field architecture is not addressed in that body of work.

**Phase 1a dossier completeness:**
High confidence on confinement mechanism, operating voltage, fuel, heating method, and operation mode. Medium confidence on energy capture (thermal cycle with turbines stated but impractical at current device scale), plasma state (non-burning sub-Q=1 near-term), and neutron management. Tritium breeding is TBD — no design exists. The overall confidence rating of medium-low reflects the concept's early stage and thin technical disclosure.

**Key data gaps limiting this analysis:**
1. Full text of both peer-reviewed papers — measured device parameters, plasma density, confinement time, neutron yield per operating condition
2. Q value achieved in any configuration — all targets are stated goals, not reported measurements
3. Coulomb collision loss rate — the dominant physics risk — not experimentally characterized
4. Any plant-scale architecture or cost model
5. Energy conversion pathway for commercial scale (turbines are impractical below ~1 MWe)

---

## Section 2: Challenges in Capturing System Function

The Orbitron concept presents LCOE modeling challenges that differ fundamentally from those of mainstream fusion concepts. The central difficulty is not missing engineering parameters but unresolved physics: the two barriers to Q>1 operation have not been experimentally retired. Challenges are ranked by LCOE impact.

**1. Q>1 not demonstrated — the entire cost model hangs on an unproven physics result (Impact: Critical)**

The CWFest 2023 blog states the operating point target: 600 W cathode + 400 W ion guns = 1,000 W total input, targeting "mid to high 10^11 neutrons per second" corresponding to approximately 1 kW fusion power [avalanche-cwfest2023-blog.md §Fusion rate scaling]. This implies Q ≈ 1 as the near-term ceiling — barely break-even before any conversion losses. For electricity production, Q_engineering (which includes thermal efficiency and recirculating power) must substantially exceed Q ≈ 1. Achieving Q_engineering > 2 would require a fusion Q of perhaps 5–10+, depending on conversion efficiency. No experimental data supporting Q>1 has been published. The entire economic case for the Orbitron — mass-manufactured modules at low capital cost — is conditional on a physics result that has not been demonstrated in any electrostatic confinement device.

**2. Coulomb collision losses — an unresolved fundamental barrier (Impact: Critical)**

The CWFest 2023 blog explicitly acknowledges this as the dominant physics challenge:

> "The coulomb collision one is going to be a longer term thing...demonstrating this experimentally with deuterium tritium fusion is ultimately how we intend to develop a queue greater than one small fusion reactor." — avalanche-cwfest2023-blog.md §Critical controversies

The 1998 Lampe-Mannheimer analysis is cited as claiming "Coulomb collision rate 25–37× faster than fusion" for this class of device [avalanche-cwfest2023-blog.md §Coulomb collision problem]. Avalanche's response — that thermalization rates in simulations use density scaling that makes the problem appear worse than it is — is a theoretical argument, not an experimental refutation. Until Coulomb collision losses are measured in an operating Orbitron at fusion-relevant parameters, this is an open physics risk that propagates into unbounded cost uncertainty. An LCOE model built before this is resolved is effectively speculative.

**3. Energy conversion at module scale — thermal turbines are impractical below ~1 MWe (Impact: High)**

The Orbitron product page states energy will be "converted to electrical energy with a thermal cycle, utilizing turbines" [avalanche-orbitron-page.md §Energy Capture]. At the target module output of 1–100 kWe, conventional steam or sCO₂ turbines are not economically viable — minimum commercial turbine sizes are in the hundreds of kWe to MWe range, and thermodynamic efficiency falls sharply at small scale. For a 1 kWe module, no practical thermal conversion pathway exists at reasonable efficiency. This is not acknowledged in any Avalanche source. The company may be describing the conversion system for a stacked multi-module plant (megawatt scale), but no plant-scale architecture is described. The energy conversion method, efficiency, and cost are entirely uncharacterized for any commercially relevant configuration.

**4. No breeding blanket design — tritium must be purchased indefinitely (Impact: High)**

The Orbitron at current device scale (desktop, 10s of cm diameter) has no tritium breeding blanket and no path to one. All tritium for D-T operation must be purchased from external suppliers at >$35,000/g [01-hts-compact-tokamak.md §Materials]. The dossier confirms no breeding approach has been disclosed [dossier.md §Tritium Breeding]. For the near-term FusionWERX neutron source application, purchased tritium is acceptable — neutron production is the revenue product. For a power reactor, the tritium cost at scale would be prohibitive without self-breeding. The company acknowledges the FusionWERX facility has "advanced tritium handling capabilities" [avalanche-fusionwerx-grant.md] but not breeding capability. Any LCOE model must account for purchased tritium as a permanent fuel cost unless and until a breeding design is disclosed.

**5. Modular scaling from kWe to MWe — the plant architecture is entirely undefined (Impact: High)**

The Orbitron value proposition rests on stacking many small modules: "modular design can be stacked for near-endless power applications" [avalanche-orbitron-page.md]. But the CWFest blog targets "under six years" to commercial operation and "less than a billion dollars" [avalanche-cwfest2023-blog.md] without describing how many modules constitute a commercial plant, what the balance of plant looks like for a modular fusion array, how neutron shielding is handled for each module in a dense array, or how tritium supply and handling scale across hundreds or thousands of modules. The modular claim is economically attractive but entirely unengineered. LCOE modeling requires a plant-scale reference design that does not exist.

**6. O&M cost structure — neutron bombardment and component replacement rates uncharacterized (Impact: Moderate)**

The desktop device produces 14.1 MeV neutrons from D-T fusion. The cathode and vacuum chamber components will experience neutron activation and radiation damage. At 1–100 kWe scale, the activation inventory per module is small, but with hundreds or thousands of modules, cumulative activation and maintenance becomes a plant-level concern. No data on cathode lifetime under neutron bombardment, HV feedthrough reliability at operating voltage over commercial timescales, or planned component replacement schedules has been published. The CWFest blog notes a "concrete castle" for shielding the prototype [avalanche-cwfest2023-blog.md], indicating non-trivial radiation management even at small scale. Fixed and variable O&M costs are entirely unknown. A placeholder assumption of 2–5% of capital cost per year (the conventional rule of thumb for novel fusion concepts) is the only option in the absence of data.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest LCOE modeling risk) to most mature.

---

**Q>1 Physics Validation — TRL 1–2**

- **Demonstrated**: Neutron production confirmed at sub-breakeven conditions (implied by FusionWERX design intent and neutron output targets). The device confines ions and produces D-T neutrons — this much is credible from the AIP Advances publication. The 10^11 n/s neutron rate target at 1 kW input corresponds to sub-Q=1 operation.
- **On paper only**: Q>1 in any electrostatic confinement configuration. Avalanche's claimed path to Q>1 relies on suppressing Coulomb collision thermalization through electron co-confinement geometry and density regimes not yet demonstrated. The theoretical argument is described but not validated.
- **Missing at scale**: Experimental measurement of Coulomb collision loss rate in an operating Orbitron at fusion-relevant ion densities. Demonstration of net energy gain (Q>1) in any test device. Scaling law from current 100 kV operation to 300 kV operating point. Confinement time measurement. These are not engineering gaps — they are open physics questions that determine whether the concept is viable.

---

**Tritium Fuel Cycle and Breeding — TRL 1–2**

- **Demonstrated**: Avalanche has a tritium-licensed facility (FusionWERX in Richland, WA) and confirmed tritium handling capability. The facility was built in the former location of Kurion's detritiation prototype facility, which was previously licensed for tritium operations [avalanche-fusionwerx-grant.md §Strategic Public-Sector Partnerships]. D-T neutron production at sub-commercial rates is the facility's stated purpose.
- **On paper only**: Any breeding blanket design. Tritium self-sufficiency roadmap. Closed fuel cycle for a commercial Orbitron plant.
- **Missing at scale**: Tritium breeding blanket engineering for a desktop-scale or module-scale device (geometrically challenging given the device's compact form factor). Tritium inventory management for a multi-module plant. At sub-breakeven operation, tritium consumed per kWh of neutron production is a cost driver with no published analysis.

---

**Energy Conversion System — TRL 1–2 (at module scale)**

- **Demonstrated**: Conventional steam turbines and sCO₂ cycles are mature at GW scale (TRL 9) [01-hts-compact-tokamak.md §BOP]. Thermoelectric conversion exists at small scales (TRL 6–7). Neither is designed or demonstrated for the Orbitron's thermal output range.
- **On paper only**: Any energy conversion pathway for the 1–100 kWe module range. Thermal management of neutron heating in the Orbitron chamber. Heat extraction geometry from a compact cylindrical device.
- **Missing at scale**: Conversion system that achieves reasonable efficiency (>20%) at 1–100 kWe per module. Integration with tritium-compatible primary circuit. Any cost model for the power conversion subsystem. The company states turbines but this is almost certainly describing a multi-module plant scenario at megawatt aggregate scale, not the per-module energy conversion.

---

**Plasma Confinement and Ion Orbiting — TRL 3–4**

- **Demonstrated**: High-voltage electrostatic ion orbiting in an Orbitron geometry has been demonstrated experimentally. The AIP Advances paper (2024) reports the co-confinement of high-energy ions and electrons [dossier.md §Key Sources]. The "mode-enhanced ion loading" paper (2025) reports operation at 100 kV in the orbitrap geometry [dossier.md]. These are genuine experimental milestones.
- **On paper only**: Ion confinement at the 300 kV operating point with simultaneous 0.4 T magnetic field. Ion density achievable in the full co-confinement configuration. Confinement time and energy balance at fusion-relevant conditions.
- **Missing at scale**: Stable, sustained ion orbiting at 300 kV under D-T plasma conditions (vs. laboratory beam-into-gas). Orbit stability over commercial operating timescales. Radiation hardening of the cathode structure under 14 MeV neutron bombardment. The Talk-Polywell forum raises a valid structural question: at 300 kV, preventing ions from impacting the cathode at fusion-relevant kinetic energies requires precise orbit stability that must be demonstrated rather than assumed [talk-polywell-orbitron-paper-discussion.md].

---

**High-Voltage Feedthrough and Power Supply — TRL 4–5**

- **Demonstrated**: Steady-state 300 kV sustained for hours at 3 W power draw [avalanche-300kv-press-release.md §"Robin Langtry" quote]. This is the company's most concrete technical milestone — described as achieving 4.7 MV/m field gradient across 2.5 inches, explicitly compared to lightning field gradients. Avalanche characterizes this as the key engineering innovation enabling the concept:

> "This high voltage milestone, the last for Series A, is the result of a novel HV feedthrough design developed by Avalanche's engineering team." — avalanche-300kv-press-release.md

> "Significantly more challenging than pulsed high voltage, which only needs to hold for microseconds or milliseconds." — avalanche-300kv-press-release.md

- **On paper only**: Feedthrough lifetime under sustained neutron bombardment. HV stability under plasma load (D-T plasma vs. vacuum operation). Power supply efficiency at commercial scale.
- **Missing at scale**: Radiation hardening of HV feedthrough insulation under cumulative 14 MeV neutron dose. Commercial power supply design for sustained 300 kV with minimal ohmic losses. The 3 W power draw for the feedthrough itself is remarkable, but total system power balance at fusion-relevant plasma densities is not characterized.

---

**Auxiliary Magnetic System (E×B Electron Confinement) — TRL 4–6**

- **Demonstrated**: Permanent magnets at ~0.05 T are operational in the current prototypes (Neo, Marty generations) [dossier.md §Magnet Type]. Magnetron-geometry electron confinement via E×B drift is well-understood physics from microwave tube technology.
- **On paper only**: Superconducting magnet upgrade to 0.3 T (announced as long-lead equipment in the $29M raise [avalanche-29m-raise-2026.md §subsystems]). Whether 0.3 T is achievable with a small, compact SC magnet system vs. permanent magnets.
- **Missing at scale**: SC magnet design for the Orbitron geometry. Radiation hardening of SC coils in a neutron-producing environment. The transition from 0.05 T (permanent magnets) to 0.3 T (SC) is a technology development step, not a procurement step. The field required is modest by fusion standards — 0.3 T vs. 5–20 T for MFE — but the geometry and radiation environment create specific engineering challenges.

---

**Neutron Shielding — TRL 5–6 (generic) / TRL 2–3 (module-scale integration)**

- **Demonstrated**: Conventional concrete shielding used for the Marty prototype — the "concrete castle" is described in the CWFest blog [avalanche-cwfest2023-blog.md §Marty prototype]. Large-scale neutron shielding is a mature technology (TRL 9 in fission). FusionWERX is explicitly a shielded neutron production facility.
- **On paper only**: Compact neutron shielding integrated with or surrounding individual Orbitron modules in a multi-module plant configuration. Activation management for small-module arrays operating at commercial duty cycles.
- **Missing at scale**: Shielding geometry for stacked modules that does not make each module's surrounding infrastructure dominate the system volume and cost. If each 1–100 kWe module requires a "concrete castle," the modular architecture becomes economically self-defeating. No design has addressed this.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium — Purchased Supply, No Breeding Path**

Unlike D-T concepts with breeding blankets, the Orbitron must purchase all tritium from external suppliers. At >$35,000/g, tritium cost is a significant operating cost driver for a sub-Q=1 neutron source and potentially prohibitive for a power reactor without breeding. The FusionWERX facility's "advanced tritium handling capabilities" [avalanche-fusionwerx-grant.md] confirm the ability to store and use tritium, but not produce it. The global tritium inventory (~25–30 kg, primarily from CANDU reactor byproduct) is the same constrained pool that limits all D-T fusion concepts — but the Orbitron's lack of a breeding plan makes it uniquely dependent on external supply indefinitely at current design maturity.

For the near-term neutron source application, purchased tritium at modest rates is acceptable. For a commercial power reactor without breeding, tritium cost could add $0.01–0.10/kWh depending on consumption rate and device Q — a potentially LCOE-dominating operating cost if Q remains near 1.

**Superconducting Magnets — Modest Field, Conventional Scale**

The planned SC upgrade targets 0.3 T — orders of magnitude below the 5–20 T fields used in MFE tokamaks and stellarators. The SC magnets needed are small and technically undemanding relative to other fusion concepts. No REBCO tape supply chain bottleneck applies here; conventional low-temperature superconductors (NbTi) would suffice at 0.3 T, and even small REBCO coils would be trivially small in the context of global production capacity. This is a genuine supply chain advantage over HTS-dependent concepts.

**High-Voltage Power Electronics — Specialized but Not Scarce**

Sustained 300 kV power supplies are specialized industrial equipment, used in particle accelerators, electron microscopes, and high-voltage testing. The global supply base is limited but not the extreme bottleneck that REBCO tape represents for tokamaks. The critical innovation — the HV feedthrough maintaining 4.7 MV/m steadily — is proprietary to Avalanche. For a multi-module plant, scaling HV supply manufacturing would require investment but is not a fundamental bottleneck.

**Tungsten and Structural Materials — Standard Availability**

At device scale, the cathode and chamber structural materials are standard vacuum and high-voltage engineering materials (stainless steel, tungsten for high-voltage electrode components, ceramic insulators). No exotic material supply chains are required at current development stage. At commercial scale, neutron activation of structural materials would create radioactive waste management requirements, but the small per-module inventory limits absolute activation compared to large-scale D-T plants.

**No FLiBe, No Beryllium, No Large REBCO Requirement**

The Orbitron concept avoids the three most constrained materials in the mainstream D-T tokamak supply chain: FLiBe (not produced at industrial scale, requires scarce beryllium), large REBCO tape quantities (global production insufficient for multiple plants), and large beryllium inventories. This is a genuine advantage if the concept ever reaches plant scale — the materials supply chain is far less constrained than for HTS tokamak approaches.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Module electrical output (target) | 1–100 kWe | avalanche-orbitron-page.md §Power range | medium | Per single Orbitron module; commercial plant requires stacking many modules; upper bound not demonstrated |
| Cathode operating voltage | 300 kV | avalanche-300kv-press-release.md §"300,000 Volts is the ideal energy" | high | Milestone achieved in steady-state; described as "ideal energy for fusing D-T" |
| Electron confinement field | ~0.05 T (current) / 0.3 T (target) | avalanche-cwfest2023-blog.md §Operating point; dossier.md §Magnet Type | medium | Permanent magnets current; SC upgrade planned as "long-lead equipment" |
| Input power (target operating point) | ~1,000 W total (600 W cathode + 400 W ion guns) | avalanche-cwfest2023-blog.md §Fusion rate scaling | medium | Aspirational operating point; no measured power balance at 300 kV reported |
| Target fusion power | ~1 kW (≈Q=1) | avalanche-cwfest2023-blog.md §Fusion rate scaling | low | Implied by "600 W + 400 W → Q≈1"; not measured |
| Target neutron rate | Mid-to-high 10^11 n/s | avalanche-cwfest2023-blog.md §Fusion rate scaling | medium | For D-T at operating point; neutron source goal for FusionWERX |
| Operation mode | Steady-state | avalanche-300kv-press-release.md §"significantly more challenging than pulsed" | high | Explicitly emphasized by company; 300 kV sustained for hours |
| HV feedthrough power draw | ~3 W | avalanche-300kv-press-release.md §"Robin Langtry" quote | high | For feedthrough itself; does not include ion gun or plasma load |
| Electric field gradient | 4.7–6 MV/m | avalanche-300kv-press-release.md; avalanche-fusionwerx-grant.md | high | Across device gap; described as "double lightning" density |
| Time to commercial (aspirational) | <6 years | avalanche-cwfest2023-blog.md §Timeline | low | 2023 statement; aspirational; no milestone-based plan publicly disclosed |
| Capital cost to commercial (aspirational) | <$1B | avalanche-cwfest2023-blog.md §Capital cost | low | Aspirational; no cost model disclosed |
| Total company funding | $29M (Series A) + $10M state grant | avalanche-29m-raise-2026.md; avalanche-fusionwerx-grant.md | high | As of early 2026; modest by fusion standards |
| Thermal efficiency | [estimated] <20% at module scale | [estimated: no practical turbine at 1–100 kWe; thermoelectric conversion ~5–15%] | low | Fundamental engineering problem; company states "thermal cycle with turbines" but this is implausible at current scale |
| Q_engineering (derived) | [inferred] << 1 currently; target ≈ 1 | [inferred from 1 kW input, target 1 kW fusion × thermal efficiency <<1] | low | Even if Q_physics ≈ 1, conversion losses imply Q_engineering << 1 at current scale |
| Plant capacity factor | [analogue] ~85–90% | [analogue: steady-state operation mode; no pulsed downtime; but cathode and HV system lifetime unknown] | low | Steady-state is favorable for capacity factor; component lifetime under neutron bombardment is the limiting unknown |
| Tritium fuel cost (purchased) | [estimated] significant OPEX if Q<5 | [estimated from tritium price >$35,000/g × consumption rate; no consumption data available] | low | Tritium cost dominates OPEX at near-breakeven Q; no breeding blanket compounds this |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value in any experimental configuration | truly-unknown | blocking | No published measurement; all values are targets |
| Coulomb collision loss rate (measured) | truly-unknown | blocking | Core physics risk; not experimentally characterized; determines whether Q>1 is achievable |
| Ion density, confinement time, triple product | truly-unknown | blocking | Fundamental plasma parameters; not published; needed to assess fusion power potential |
| Fusion yield per operating condition (measured) | proprietary / not-yet-sourced | blocking | Full AIP Advances paper likely contains measured neutron rates; accessible only as abstract |
| Commercial plant architecture (module count, BOP) | truly-unknown | blocking | No plant-scale design; stacking concept described qualitatively only |
| Energy conversion system design and efficiency | truly-unknown | blocking | No engineering design for kWe-scale thermal conversion; turbines stated but impractical |
| Overnight capital cost per kWe (any estimate) | truly-unknown | blocking | No cost model; no plant study; aspirational <$1B total with no basis stated |
| Cathode lifetime under neutron irradiation | truly-unknown | important | Determines maintenance cycle and cathode replacement cost; no data |
| HV feedthrough lifetime at operating conditions | proprietary | important | Key reliability metric for steady-state operation; 300 kV demonstrated but not at sustained plasma load |
| Tritium consumption rate at operating Q | derivable | important | Calculable from Q and neutron rate if Q were known |
| Breeding blanket design (any) | truly-unknown | important | No design disclosed; needed for long-term fuel cost estimation |
| O&M cost structure (fixed vs. variable) | truly-unknown | important | No data; standard placeholder (2–5% of CAPEX/yr) required |
| Thermal efficiency at kWe scale | truly-unknown | important | Conversion approach undefined; cannot be borrowed from MFE analogues |
| Scaling law from 100 kV (demonstrated) to 300 kV (target) | proprietary / not-yet-sourced | important | Second Physics of Plasmas paper may contain relevant data; accessible as abstract only |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q>1 not demonstrated in any electrostatic confinement device — entire economic case is conditional | S1, S2, S5 | truly-unknown | blocking | Await AIP Advances + Physics of Plasmas full text; watch for conference presentations with measured fusion yields |
| 2 | Coulomb collision loss rate not measured — dominant physics risk unretired | S2, S3, S5 | truly-unknown | blocking | Requires full text of AIP Advances paper and follow-on experimental publications; cannot be resolved from available sources |
| 3 | Ion density, confinement time, and triple product unpublished — no plasma physics anchor for LCOE model | S1, S5 | truly-unknown | blocking | Full text of both peer-reviewed papers; company technical presentations |
| 4 | Commercial plant architecture undefined — no module count, BOP layout, or plant-scale reference design | S2, S5 | truly-unknown | blocking | Company has not disclosed; watch for roadmap publications post-FusionWERX commissioning |
| 5 | Energy conversion system at kWe scale undefined — turbines impractical; alternative not specified | S2, S3, S5 | truly-unknown | blocking | Technical roadmap document from Avalanche; or independent assessment of small-module thermal conversion options |
| 6 | Overnight capital cost per kWe — no model, no plant study, no component-level breakdown | S2, S5 | truly-unknown | blocking | No resolution path from public sources; requires direct company disclosure or independent cost estimation from plant architecture (which also doesn't exist) |
| 7 | Tritium consumption rate and fuel cost at operating conditions | S4, S5 | derivable | important | Calculable once Q and neutron rate at operating conditions are published; tritium price from market |
| 8 | Cathode and HV feedthrough lifetime under sustained neutron bombardment | S3, S5 | truly-unknown | important | No fission or other analog; requires dedicated irradiation testing at 14 MeV |
| 9 | Tritium breeding blanket design — none disclosed | S3, S4, S5 | truly-unknown | important | Watch for power reactor design publications; likely years from disclosure given current TRL |
| 10 | O&M cost structure (fixed + variable, scheduled + unplanned) | S2, S5 | truly-unknown | important | Standard fusion industry placeholder (~2–5% CAPEX/yr) as lower bound; actual cost unknown |
| 11 | Measured scaling from 100 kV (Physics of Plasmas paper) to 300 kV operating point | S3, S5 | proprietary / not-yet-sourced | important | Full text of Physics of Plasmas 32(9), 092105 (2025); accessible as abstract only |
| 12 | SC magnet design for 0.3 T upgrade — specifications, cost, geometry | S3, S5 | proprietary | nice-to-have | Company confirmed as "long-lead equipment" in $29M raise; no specs disclosed |
| 13 | Neutron shielding integration for stacked multi-module plant | S3, S5 | truly-unknown | nice-to-have | Fundamental design problem; no concept published; needed before modular LCOE model is feasible |

---

## Section 7: Cross-Concept Notes

**Approved prior analysis available: 21-spherical-tokamak-hts**

The Spherical Tokamak - HTS (Tokamak Energy) is the only approved analysis in the pool. The Orbitron and the ST-E1 share D-T fuel and steady-state operation but are otherwise minimally comparable — different confinement family, scale, physics, and maturity. Cross-referencing is limited to shared D-T fuel cycle constraints.

**Reused elements from 21-spherical-tokamak-hts:**

- **Tritium supply constraints**: The global tritium inventory (~25–30 kg), decay rate (5.5%/year), CANDU production origin, and market price (>$35,000/g) [21-spherical-tokamak-hts.md §Section 4] apply identically to the Orbitron's near-term purchased-tritium operation. The sequencing constraint (early plants must demonstrate self-sufficiency before fleet scaling) is even more acute for the Orbitron, which has no breeding blanket design at all.
- **Regulatory cost scenarios**: The Stewart & Shirvan 2.2× building cost factor for fission-style regulation [21-spherical-tokamak-hts.md §Section 2] would apply to the Orbitron as a D-T fusion facility if scaled to power plant operation, though at current scale FusionWERX operates as a research facility under less onerous regulatory frameworks.

**Key divergences from mainstream D-T concepts:**

The Orbitron diverges from all MFE, IFE, and MIF concepts in the landscape in three structural ways relevant to TEA:

1. **No large magnets, no breeding blanket, no plasma heating system**: The three largest capital cost drivers in tokamak LCOE models (magnets, blanket, auxiliary heating) are either absent or radically smaller in the Orbitron. If Q>1 is achieved, the capital cost structure would look nothing like any prior D-T TEA. The modular mass-manufacturing model is the claimed cost mechanism — but it requires a plant architecture design that does not exist.

2. **Sub-commercial scale physics**: All approved and in-progress analyses in the landscape assume concepts that at least have a credible Q>>1 path anchored by published physics. The Orbitron's Q target is Q≈1, which is insufficient for electricity generation after conversion losses. The gap between where the concept is and where it needs to be for LCOE analysis is larger than for any other concept in the portfolio.

3. **Nearest neighbors in the landscape**: The Polywell (27-polywell, gap-checked) is the most similar concept — both are non-standard electrostatic approaches to D-T fusion using combined electric and magnetic fields. The Polywell has a longer experimental history (U.S. Navy program, multiple generations of WB devices) and a more developed physics critique, but also has not demonstrated Q>1. The Dense Plasma Focus (24, gap-checked) shares the "non-standard" family but uses a fundamentally different confinement mechanism. Neither has an approved analysis available for direct parameter reuse.

**TEA pipeline recommendation:**

A conventional LCOE model cannot be built for the Orbitron at current maturity. The appropriate TEA treatment is:
1. Back-solve from commercial viability to identify what Q and what capital cost per kWe the concept needs to achieve
2. Compare those targets against the physics barriers (Coulomb collision problem) and engineering requirements (thermal conversion at kWe scale, tritium breeding)
3. Present as a conditional viability assessment — if physics barriers are resolved, what does the cost structure look like — rather than a central LCOE estimate

This is a fundamentally different modeling posture than for mature MFE or IFE concepts where physics is anchored and cost is the primary uncertainty.

---

## Section 8: Sources

**1. Avalanche Energy CWFest 2023 Blog Post**
- Full reference: Avalanche Energy (2023) "CWFest 2023 presentation blog." Available at: https://www.avalanchefusion.com/blog/cwfest2023
- Contribution: Primary technical source — device architecture, operating point targets (300 kV, 0.4 T, 1 kW fusion power), the two major physics critiques and Avalanche's responses, preliminary subsystem description, capital cost and timeline aspirations, Marty prototype description. Most detailed public technical document.
- Location: `iter-01/sources/avalanche-cwfest2023-blog.md`

**2. AIP Advances Paper (2024) — Orbitron co-confinement**
- Full citation: [Author(s) not in abstract] "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons," *AIP Advances*, 14(8), 085025 (August 2024). doi: not available from abstract.
- Contribution: Peer-reviewed confirmation of the experimental Orbitron concept; co-confinement of high-energy ions and electrons demonstrated. Full experimental parameters unavailable (abstract only).
- Location: Referenced in `dossier.md §Key Sources`

**3. Physics of Plasmas Paper (2025) — Mode-enhanced ion loading**
- Full citation: [Author(s) not in abstract] "Mode-enhanced ion loading in a 100 kV orbitrap," *Physics of Plasmas*, 32(9), 092105 (September 2025). doi: not available from abstract.
- Contribution: Reports 100 kV operation with enhanced ion loading; provides experimental scaling data between Neo and Marty device generations. Full parameters unavailable (abstract only).
- Location: Referenced in `dossier.md §Key Sources`

**4. Avalanche Energy $29M Series A Press Release (2026)**
- Full reference: Avalanche Energy (2026) "Avalanche Energy raises $29 million following plasma physics breakthroughs." Available at: https://www.avalanchefusion.com/news-release/avalanche-energy-raises-29-million-following-plasma-physics-breakthroughs
- Contribution: Confirms Q>1 D-T test program, FusionWERX facility (licensed 2027), superconducting magnets as long-lead equipment, modular stacking architecture. Business context and funding scale.
- Location: `iter-01/sources/avalanche-29m-raise-2026.md`

**5. Avalanche Energy 300 kV Milestone Press Release**
- Full reference: Avalanche Energy (2025) "Avalanche Energy completes final Series A voltage milestone: 300,000 volts in compact high-efficiency prototype fusion machine." Available at: https://www.avalanchefusion.com/news-release/avalanche-energy-completes-final-series-a-voltage-milestone-300-000-volts-in-compact-high-efficiency-prototype-fusion-machine
- Contribution: Most specific technical milestone — 300 kV steady-state for hours at 3 W feedthrough power draw; 4.7 MV/m field gradient; confirms steady-state vs. pulsed operation; HV feedthrough design as proprietary innovation.
- Location: `iter-01/sources/avalanche-300kv-press-release.md`

**6. Avalanche Energy FusionWERX Grant Announcement**
- Full reference: Avalanche Energy (2025) "Avalanche Energy awarded $10 million grant from Washington State to develop FusionWERX neutron factory." Available at: https://www.avalanchefusion.com/news-release/avalanche-energy-awarded-10-million-grant-from-washington-state-to-develop-fusionwerx-neutron-factory
- Contribution: Confirms FusionWERX facility location (Richland, WA), tritium handling capability, cost-per-neutron competitive advantage claim, near-term revenue from neutron production, partnership with PNNL and WSU.
- Location: `iter-01/sources/avalanche-fusionwerx-grant.md`

**7. Avalanche Energy Orbitron Product Page**
- Full reference: Avalanche Energy (n.d.) "Orbitron." Available at: https://www.avalanchefusion.com/orbitron
- Contribution: Module power range (1–100 kWe), energy conversion statement ("thermal cycle, utilizing turbines"), cost advantage claims ("avoids expense of high-powered magnets or lasers"), modular stacking architecture, p-B11 future aspiration, rapid manufacturing concept.
- Location: `iter-01/sources/avalanche-orbitron-page.md`

**8. Talk-Polywell Forum Discussion (August 2024)**
- Full reference: "Djnz" (2024) Thread on Orbitron AIP Advances paper. Talk-Polywell forum, August 22–23, 2024. Available at: https://talk-polywell.org/bb/viewtopic.php?t=6587
- Contribution: External community critique — 300 kV maintenance challenge, ion cathode impact risk, operating mode ambiguity (pulsed vs. steady), "5 kWe pulsed" speculation. Useful for identifying engineering concerns not acknowledged in company materials.
- Location: `iter-01/sources/talk-polywell-orbitron-paper-discussion.md`

**9. Phase 1a Dossier — Electrostatic Hybrid (D-T)**
- Full reference: Internal research product, Fusion TEA project (2026-03-08). `knowledge/concept_research/13-electrostatic-hybrid/dossier.md`
- Contribution: Synthesis of all column values with confidence ratings, citations, and classification rationale; identifies key sources, remaining gaps, and classification decisions (especially the electrostatic vs. hybrid confinement family question, and the steady-state vs. pulsed operation mode question).

**10. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-reference for D-T tritium supply constraints (global inventory, CANDU production decline, >$35,000/g price, sequencing constraint) and regulatory cost uncertainty. Not otherwise applicable — device physics, scale, and cost structure are categorically different.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`
