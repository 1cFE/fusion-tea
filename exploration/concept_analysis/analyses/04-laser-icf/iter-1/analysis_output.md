## Design Point

- Name: HB11 Energy 500 MWe technoeconomic model scenario (McKenzie et al. 2023)
- Maturity: paper-concept
- P_native: 500 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/04-laser-icf/iter-03/sources/link-10-1007-s10894-023-00349-9/output.md
  - knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-patent-reactor-design.md

## Section 1: Availability of Data

**Rating: Limited**

The public information base for HB11 Energy's laser-driven hydrogen-boron fusion concept is narrow in both breadth and depth. The concept has one peer-reviewed technoeconomic paper, one reactor design patent, one experimental physics paper, and a handful of press articles and website pages. No independent third-party cost analysis, no plant-level systems code output, and no detailed subsystem cost breakdown exist in the public domain.

**Peer-reviewed publications:**
- McKenzie et al., "HB11 -- Understanding Hydrogen-Boron Fusion as a New Clean Energy Source," *J. Fusion Energy* 42, 17 (2023). This is the primary and essentially sole source for the 500 MWe technoeconomic model. It provides a high-level power-loop analysis (recirculating power fraction as a function of laser efficiency, target gain, and conversion efficiency) but does not publish a capital cost breakdown, component-level costs, or a full LCOE calculation. The paper is authored by HB11 Energy's managing director and team -- there is no independent validation.
- Margarone et al., "In-Target Proton-Boron Nuclear Fusion Using a PW-Class Laser," *Applied Sciences* 12(3):1444 (2022). Experimental physics paper reporting the best published alpha-particle yield (~10^10/sr) at the Osaka LFEX facility. Contains no cost or engineering data.

**Patent:**
- US10410752B2 / US20170125129A1, Hora et al. (filed 2014, granted 2019). Describes the reactor architecture in detail -- two-laser system, consumable magnetic field device, direct electrostatic energy conversion, stainless steel sphere. Provides the most detailed subsystem enumeration but contains no cost figures and explicitly states that many subsystems are "not described."

**Company communications:**
- HB11 Energy website (hb11.energy/our-technology/) -- multiple extraction attempts captured only marketing boilerplate; the technical content is rendered dynamically and was not successfully extracted. The 2025 version states "conventional steam cycle generator," contradicting the patent's direct electrostatic conversion.
- New Atlas interview (2020) and various press releases provide qualitative claims but no quantitative engineering or cost data.
- Optica OPN profile (June 2025) confirms "hybrid burn target design" terminology.

**Key data gaps:**
1. No published capital cost estimate for any subsystem or for the overall plant.
2. No published LCOE figure -- only boundary conditions ($35/MWh target, $350/MWh upper bound).
3. No published repetition rate demonstration or engineering analysis.
4. No published direct energy conversion efficiency measurement or prototype.
5. No published target manufacturing process or cost estimate.
6. No independent engineering or cost assessment by any third party.

> "While a detailed appraisal and sensitivity analysis of the technoeconomic model is beyond the scope of this paper, the range of the target gain required to achieve such economic viability varies between 100 and 300 when assuming a laser efficiency of 20%."
> -- McKenzie et al. 2023, §Commercialisation: Technoeconomic Model

## Section 2: Challenges in Capturing System Function

The LCOE modeling challenges for HB11 Energy's concept are dominated by the enormous gap between experimental demonstration and design-point assumptions, and by the fundamental uncertainty about whether the physics allows net energy gain at all.

**1. Four-order-of-magnitude physics gap (Critical)**
The single most important challenge. Current best experimental results show a laser-to-alpha energy conversion efficiency of ~0.005% (approximately 0.1 J of alpha energy from ~1 kJ of laser input at Osaka LFEX). The design point requires a target gain G of 100--300, corresponding to a laser-to-fusion efficiency of ~10,000%--30,000%. The gap from current performance to the minimum viable design point is approximately four orders of magnitude. This is not an engineering scale-up problem; it is an open question in fundamental physics.

> "The 'breakeven' threshold corresponds to 2.15 x 10^15 alpha particles per kJ of laser energy, corroborating the four orders of magnitude deficit from breakeven."
> -- McKenzie et al. 2023, §Pathways to Increase Fusion Gain

**2. Bremsstrahlung barrier to thermal ignition (Critical)**
The p-B11 reaction has a boron atomic number of Z=5, producing severe bremsstrahlung radiation losses. Under thermal equilibrium conditions, radiation losses exceed fusion power density. McKenzie et al. cite Wurzel & Hsu (2022): "bremsstrahlung power density always exceed the power density generated by fusion reaction when Te >= Ti/3 suggesting that p-B11 ignition may require a non-equilibrium burn." The entire concept depends on maintaining a strongly non-equilibrium plasma state -- a condition that is theoretically debated and experimentally unverified at relevant scales.

**3. Energy conversion pathway uncertainty (High)**
The concept has undergone a significant design pivot. The 2018 patent describes direct electrostatic conversion at -1.4 MV bias, collecting alpha-particle charge directly as current -- which would eliminate the entire thermal balance-of-plant. The 2025 company website states "conventional steam cycle generator." McKenzie et al. 2023 discusses multiple options: direct electrodynamic conversion (DEC) at ~50%, MHD + Rankine at ~64%, and conventional thermal at 36--40%. The energy conversion pathway is not settled, and the choice has a ~2x effect on LCOE through the conversion efficiency parameter epsilon.

**4. Undefined driver cost (High)**
The laser driver system is the dominant capital cost item for any laser ICF concept. HB11 requires a 30 kJ, 1 ps, 30 PW CPA laser for ignition plus a 3 kJ nanosecond laser for magnetic field generation. No laser of this specification exists as a commercial product. No cost estimate for such a system has been published by HB11 or any independent source. The McKenzie paper assumes 20% wall-plug efficiency, which "can only be achieved using a diode-pumped solid state laser driver" -- but no such system has been demonstrated at the required pulse parameters.

**5. Consumable magnetic field device cost (High)**
The patent describes a consumable assembly (two nickel plates, coil windings, polyethylene foam, quartz fiber fuel support, fuel pellet with silver cover) that is destroyed every shot. At 1 Hz repetition, this is ~31.5 million assemblies per year. The unit cost and manufacturing throughput of this assembly are entirely uncharacterized. McKenzie et al. 2023 states only that "a target cost of several dollars per target is acceptable if a target gain of 200 can be achieved."

**6. Unvalidated avalanche multiplication mechanism (Medium-High)**
One of the most promising gain pathways is the "avalanche" chain reaction, where alpha particles from initial fusions accelerate protons to cause secondary fusions. McKenzie et al. acknowledge this mechanism "has been the subject of debate." If the avalanche does not produce the predicted multiplication, the required laser energy per target increases dramatically, potentially making the concept unviable at any reasonable cost.

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

**Target gain physics -- TRL 1--2**
- **On paper only**: Non-thermal block ignition of p-B11 at energy-positive scales. Avalanche multiplication mechanism. Hybrid burn combining compression with fast ignition. Kilotesla magnetic confinement of the fuel. All pathways to net energy gain remain theoretical.
- **Demonstrated**: Alpha-particle production at ~10^10/sr per PW-class shot (Osaka LFEX, 2022). Approximately 10 experimental demonstrations of laser-driven p-B11 fusion have ever been conducted worldwide.
- **Missing at scale**: Any demonstration of energy gain, even at sub-breakeven levels. Current results are ~4 orders of magnitude below breakeven.

**Direct energy conversion -- TRL 1--2**
- **On paper only**: The patent describes a Faraday cage at -1.4 MV collecting alpha particles directly as current. McKenzie et al. discuss DEC at ~50% and MHD + Rankine at ~64%.
- **Demonstrated**: No prototype or proof-of-concept of direct energy conversion for HB11 alpha spectra exists in the public record.
- **Missing at scale**: Any hardware, efficiency measurement, or engineering design for power-plant-scale direct conversion of alpha-particle kinetic energy.

**Kilotesla magnetic field generation -- TRL 2--3**
- **Demonstrated**: Laser-driven capacitor-coil targets have produced sub-kilotesla fields (~350 T, Fujioka et al.). The patent and McKenzie et al. require 10 kT -- roughly 30x beyond the cited experimental basis.
- **Missing at scale**: Reproducible multi-kilotesla fields at the fuel target, at repetition rate, with adequate spatial uniformity and temporal duration for fusion confinement.

**Petawatt CPA laser driver -- TRL 3--4**
- **Demonstrated**: PW-class CPA lasers exist at national facilities (LFEX at Osaka, ELI in Europe). These are single-shot research instruments, not commercial products. HB11's Adelaide partnership (A$8.2M, 2025) is developing USPL systems targeting >10% wall-plug efficiency.
- **On paper only**: A 30 kJ, 1 ps, 30 PW CPA laser operating at Hz repetition rates with 20% wall-plug efficiency. McKenzie et al. identify this as a key challenge.
- **Missing at scale**: High-repetition-rate operation (>1 Hz), commercial-grade reliability, 20% wall-plug efficiency, cost reduction to power-plant-viable levels. No laser manufacturer has demonstrated these parameters in combination.

**Target/consumable fabrication -- TRL 2--3**
- **On paper only**: Mass production of composite target assemblies (nickel plates, coil windings, micro-scale fuel pellet with silver coating, quartz fiber support) at ~1 Hz throughput and "several dollars per target."
- **Demonstrated**: Laboratory fabrication of boron nitride targets for single-shot experiments. Novel materials (borophene, white graphene) identified as candidates for solution-based manufacturing.
- **Missing at scale**: Automated manufacturing line, quality control at rate, demonstrated unit cost.

**Reactor vessel / chamber -- TRL 3--4**
- **On paper only**: The patent describes a stainless steel sphere (>=1 m diameter, 10 mm wall) at ground potential, with laser apertures and vacuum systems. McKenzie et al. describe "a largely empty metal sphere."
- **Demonstrated**: The aneutronic nature of p-B11 means negligible neutron damage (~0.1% side reactions), potentially allowing conventional structural materials and a 25-year reactor lifetime without neutron-driven replacement. The patent estimates shock per shot at ~5 grams TNT equivalent.
- **Missing at scale**: Any prototype reactor vessel. Vacuum system design, fuel handling airlock, laser window survivability at repetition rate.

**Energy conversion (thermal, if selected) -- TRL 8--9**
- **Demonstrated**: Conventional Rankine and sCO2 Brayton cycles are mature commercial technology.
- **Missing at scale**: Integration with the pulsed thermal source from an IFE reactor.

## Section 4: Key Materials and Supply Chain Considerations

**Boron-11 fuel (No constraint)**
Natural boron is ~80% B-11. The world's largest boron mine contains ~1.2 billion metric tons. McKenzie et al. estimate annual boron consumption for a global fusion fleet would be below 10^6 tons/year, "1000 times less than confirmed global boron reserves." Fuel availability is a genuine structural advantage over tritium-based concepts.

However, natural boron contains ~20% B-10, which produces neutrons via the p-B10 side reaction. If isotopically pure B-11 is required to ensure a truly aneutronic reaction, enrichment costs would add an unquantified fuel cost premium. McKenzie et al. note that "the cost of production of isotopically pure 11B" must be weighed against neutron production from B-10.

**Hydrogen (No constraint)**
Ubiquitous and inexpensive. No supply chain risk.

**Nickel (consumable, potentially significant)**
The patent's magnetic field device uses two nickel plates per shot. At ~31.5M shots/year, this represents a sustained industrial-scale nickel consumption stream. Exact mass per unit is not specified, but even at gram-scale per plate, annual consumption would be tens to hundreds of tonnes -- manageable against global nickel production (~3.3M tonnes/year) but a non-trivial recurring cost.

**Silver (consumable, minor)**
Vapor-deposited silver cover layer (<=5 microns) on each fuel pellet. Small per-unit quantity but aggregates over millions of shots annually.

**CPA laser optics and components (critical, no supply chain)**
No commercial supply chain exists for PW-class CPA laser systems at the parameters required. Large-aperture diffraction gratings, gain media, and pulse compression optics are bespoke scientific components. HB11's Adelaide partnership is attempting to establish sovereign Australian laser manufacturing capability, but this is at a very early stage (A$8.2M investment, 2025).

**Laser diodes (potentially significant)**
McKenzie et al. assume diode replacement cost of $1/W with a lifetime of 2.2 billion shots. This is the primary recurring O&M cost in the technoeconomic model. The assumed cost requires continued learning-curve reduction in high-power laser diode manufacturing.

**No tritium, no lithium blanket, no REBCO (structural advantage)**
The p-B11 fuel cycle eliminates tritium (globally ~25 kg, $30,000+/g), lithium breeding blanket materials (FLiBe, lithium ceramics), and -- since there are no superconducting magnets -- REBCO tape. This removes three of the most constrained supply chains in fusion.

**No reduced-activation steels (potential advantage)**
The aneutronic reaction (~0.1% neutron energy fraction) may allow conventional structural steels rather than RAFM or vanadium alloys. If confirmed, this eliminates the specialty structural materials supply chain.

## Section 5: Design Point Parameters

All parameters describe the HB11 Energy 500 MWe technoeconomic model scenario (McKenzie et al. 2023) at its native 500 MWe scale.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 500 MWe | McKenzie et al. 2023 §Commercialisation | medium | spec key: drives `P_native` |
| Fuel | p-B11 (proton-boron-11) | McKenzie et al. 2023 §Introduction | high | spec key: `fuel` |
| Confinement | IFE (laser-driven, fast ignition) | dossier.md §Confinement Family | high | |
| Ignition laser pulse energy | 30 kJ | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | spec key: `driver_energy` |
| Ignition laser peak power | 30 PW (at ~1 ps) | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Ignition laser pulse duration | ~1 ps | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Ignition laser focal intensity | 10^20 W/cm^2 | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Ignition laser focal spot | 200 um | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Magnetic field laser energy | 3 kJ | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Magnetic field laser pulse duration | nanosecond | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | medium | |
| Magnetic field strength | 10 kT | McKenzie et al. 2023 §Pathways (magnetic fields subsection) | low | 30x beyond experimental basis (~350 T) |
| Target gain (G) | 100--300 (economic viability range) | McKenzie et al. 2023 §Commercialisation | low | 4 orders of magnitude above current demonstration |
| Laser wall-plug efficiency (eta) | 20% | McKenzie et al. 2023 §Commercialisation | low | "can only be achieved using a diode-pumped solid state laser driver" |
| Conversion efficiency (epsilon) | 36--40% (thermal) to 50% (DEC) to 64% (MHD+Rankine) | McKenzie et al. 2023 §Commercialisation | low | Pathway not settled; thermal is most conservative |
| Recirculating power fraction (f) | 0.10 target (0.25 bare minimum) | McKenzie et al. 2023 §Commercialisation | low | f = 1/(epsilon * eta * G) |
| Laser driver power consumption | 50 MW (at f = 0.10) | McKenzie et al. 2023 §Commercialisation | low | [inferred: 10% of 500 MWe] |
| Average laser output power | 10 MW | McKenzie et al. 2023 §Commercialisation | low | [inferred: 50 MW * 20% eta] |
| Fuel pellet geometry | Cylinder, 1 cm length x 2 mm diameter | McKenzie et al. 2023 §Pathways; Patent US10410752B2 | medium | Solid HB11, room-temperature |
| Repetition rate | ~1 Hz | Patent US10410752B2; dossier.md §Repetition Rate | low | Patent states "1 reaction per second"; not experimentally demonstrated |
| Reaction products | 3 alpha particles, 8.7 MeV per reaction | McKenzie et al. 2023 §Introduction | high | Aneutronic primary reaction |
| Neutron fraction | ~0.1% from side reactions | McKenzie et al. 2023 §Commercialisation | medium | |
| Energy per shot | ~1 GJ (at G ~ 30,000 from patent) or variable with G | Patent US10410752B2 (1 GJ claim); McKenzie et al. 2023 (G-dependent) | low | Patent's claimed gain is inconsistent with McKenzie's G=100-300 range |
| Reactor vessel | Stainless steel sphere, >=1 m diameter, 10 mm wall | Patent US10410752B2 | low | Patent design; may differ in current concept |
| Shock per shot | ~5 grams TNT equivalent | Patent US10410752B2 | low | Based on patent's 1 GJ yield scenario |
| Plant lifetime | 25 years | McKenzie et al. 2023 §Commercialisation | medium | Assumed; not limited by neutron irradiation |
| Diode lifetime | 2.2 billion shots | McKenzie et al. 2023 §Commercialisation | low | Assumed; diode replacement at $1/W |
| LCOE target | $35/MWh (upper bound $350/MWh) | McKenzie et al. 2023 §Commercialisation | low | Boundary condition, not calculated result |
| TNSA laser-to-proton conversion | ~10% | McKenzie et al. 2023 §History | medium | Literature value, not HB11-specific |
| p-B11 cross-section at resonance | ~1.2 barn at 675 keV | hb11-osaka-experiment-2022.md §Section 1 | high | Orders of magnitude below DT (~5 barns) |
| Current best alpha yield | ~10^10 /sr (Osaka LFEX, 2022) | hb11-osaka-experiment-2022.md §Section 3; McKenzie et al. 2023 §History | high | Anchor for physics gap assessment |
| Current laser-to-alpha efficiency | ~0.005--0.01% | hb11-osaka-experiment-2022.md §Section 4; McKenzie et al. 2023 §History | high | 4 orders of magnitude below breakeven |

**Consistency notes:**

The patent (2018) and McKenzie et al. (2023) present inconsistent design points in several respects:
- The patent claims ~1 GJ per shot from 30 kJ laser input, implying a gain of ~33,000x. McKenzie et al. state the viable gain range is 100--300. The 500 MWe scenario implicitly requires a gain of ~200 at the stated parameters (30 kJ laser, 20% eta, 10% recirculating fraction), producing ~6 MJ fusion per shot. At 1 Hz, this yields only ~6 MW of fusion power, insufficient for 500 MWe. To reach 500 MWe at G=200 with epsilon=0.40 and eta=0.20, the average laser power must be 10 MW and the average fusion power 2 GW thermal, requiring ~333 Hz repetition rate at 30 kJ or ~1 Hz at ~10 MJ laser energy per shot. The paper does not resolve this arithmetic explicitly.
- The patent describes direct electrostatic conversion at -1.4 MV. The 2025 website states "conventional steam cycle generator." McKenzie et al. (2023) discusses both options without committing. The design point's energy conversion pathway is not fixed.

These inconsistencies are inherent to the paper-concept maturity level and mean that the "500 MWe scenario" is more accurately described as a set of coupled economic boundary conditions (f <= 0.10, LCOE <= $35/MWh, G in [100, 300]) than as a specific engineering design.

### Section 5b: Override Candidates

The per-account walkthrough below applies the canonical 1costingFE account schema for the IFE archetype. For each account, the question is whether the dossier names a company-grounded quantity, unit cost, or published dollar figure that justifies departing from the library default.

**Walkthrough:**

- **C220101** (First wall / blanket / energy-capture): The p-B11 reaction is aneutronic (<0.1% neutron energy). There is no tritium-breeding blanket and minimal neutron shielding. The reactor vessel is described as "a largely empty metal sphere" (New Atlas interview) or a stainless steel sphere >=1 m, 10 mm wall (patent). The library default for this account prices a DT-relevant blanket, which fundamentally misrepresents this design. However, no company-grounded dollar figure exists for what replaces it. **Override proposed**: zero or near-zero, with rationale based on architectural elimination.

- **C220102** (Radiation shield): Neutron wall loading is negligible (~0.1% of energy in side-reaction neutrons). The patent does not discuss shielding. Shield sizing scales to neutron wall loading; at <0.1% neutron fraction, the shield is structurally minimal. **Override proposed**: strong reduction from default.

- **C220104** (Primary pulsed driver -- laser): This is the dominant capital cost item. McKenzie et al. 2023 provide no dollar figure. The paper identifies the laser driver as critical and assumes 20% wall-plug efficiency with $1/W diode replacement cost, but does not publish a system-level cost. No override can be grounded in company-published data. **No override -- data insufficient.**

- **C220105** (Primary structure): The patent describes a stainless steel sphere (>=1 m, 10 mm wall). The shock per shot (~5 g TNT equivalent) is modest. No cost figure published. **No override.**

- **C220106** (Vacuum system): The patent mentions vacuum pumps and airlocks for fuel loading. No cost figure. **No override.**

- **C220107** (Power supplies / pulsed-power capacitor bank): The HB11 concept does not use a capacitor bank for energy delivery -- the driver is a laser. No pulsed-power capacitor bank exists in this design. **Override proposed**: zero.

- **C220108** (Target factory): McKenzie et al. state "a target cost of several dollars per target is acceptable if a target gain of 200 can be achieved." The target is a complex consumable (nickel plates, coils, fuel pellet, silver coating, quartz fiber). At 1 Hz and "several dollars," annual target cost would be ~$100M--$300M. Novel materials (borophene, white graphene) enable "solution-based methods that are amenable to large-scale manufacturing." The "several dollars" figure is an acceptability threshold, not a cost estimate, but it is the only company-grounded number available. **Override proposed** with low confidence.

- **C220110** (Remote handling): With negligible neutron activation, rad-hardening requirements are dramatically reduced relative to DT concepts. No specific cost figure. **Override proposed**: reduction based on minimal activation environment.

- **C220111** (Installation & assembly): No company data. **No override.**

- **CAS21** (Buildings & site): The concept eliminates several building-intensive subsystems (tritium plant, hot cells for activated-component processing, heavy biological shielding). No cost figure. **Override proposed**: reduction based on eliminated facilities.

- **CAS23** (Turbine plant): If direct energy conversion is used (patent design), the thermal cycle is eliminated entirely and CAS23 = 0. If thermal conversion is used (2025 website), CAS23 is a standard steam turbine island. The design point is ambiguous. **Override proposed**: zero for DEC pathway; library default for thermal pathway. Given the 2025 website's statement, the safer assumption is thermal conversion, in which case no override is warranted. **Conditional override.**

- **CAS24** (Electric plant equipment): The patent describes a -1.4 MV HVDC-to-AC conversion system for direct conversion. If thermal conversion is used instead, standard electric plant equipment applies. **No override** under thermal assumption.

- **CAS26** (Heat rejection): If DEC is used, heat rejection is minimal. If thermal conversion is used, standard. **No override** under thermal assumption.

- **CAS27** (Special materials -- initial inventory): The fuel inventory is solid hydrogen-boron pellets at room temperature. No cryogenic handling, no tritium, no lithium compounds. Boron-11 is cheap (~$1--5/kg for industrial boron). **Override proposed**: near-zero relative to DT concepts.

- **CAS70** (O&M + scheduled component replacement): McKenzie et al. state that "significant operational costs of DT systems are primarily associated with the replacement of the activated reactor components exposed to high neutron fluxes. For the HB11 system, these costs are reduced." 25-year lifetime assumed without neutron-driven replacement. Laser diode replacement at $1/W with 2.2 billion shot lifetime is the primary recurring cost. **Override proposed**: reduction from DT default, with laser diode replacement as the dominant O&M item.

- **CAS80** (Fuel cost): p-B11 fuel is earth-abundant. No tritium procurement. Boron-11 is ~80% of natural boron. Annual boron consumption for the fleet estimated at <10^6 tonnes against ~10^9 tonnes reserves. However, target fabrication cost ("several dollars per target") is the real fuel-cycle cost driver, and this is partly captured in C220108. If isotopic enrichment of B-11 is required, this adds an unquantified cost. **Override proposed**: near-zero for raw fuel; target fabrication cost allocated to C220108.

```yaml
overrides:
  - account: C220101
    value: 0.05 * generic.costs.c220101
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation; hb11-patent-reactor-design.md §Energy Conversion"
    rationale: |
      Aneutronic p-B11 reaction eliminates tritium-breeding blanket entirely.
      Neutron energy fraction ~0.1% from side reactions. No lithium blanket,
      no neutron multiplier, no tritium extraction. The "first wall" is a
      stainless steel sphere (>=1m, 10mm wall). Retained at 5% of default
      to account for minimal energy-capture wall structure and alpha-particle
      thermal management. No company-published dollar figure; override is
      based on architectural elimination of the subsystem.

  - account: C220102
    value: 0.05 * generic.costs.c220102
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
    rationale: |
      Neutron wall loading is negligible (~0.1% of fusion energy in side-
      reaction neutrons, 2 orders of magnitude below conventional fission
      per MW). Shield sizing scales to neutron wall loading. Retained at 5%
      to account for residual shielding against side-reaction neutrons and
      alpha-particle-induced activation (which McKenzie notes will need
      materials research).

  - account: C220107
    value: 0.0
    enabled: true
    provenance: direct
    source: "hb11-patent-reactor-design.md §Reactor Architecture; link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
    rationale: |
      HB11 uses a laser driver, not a pulsed-power capacitor bank. No
      capacitor bank exists in this design. The driver cost is captured
      in C220104 (laser). Setting to zero eliminates double-counting.

  - account: C220108
    value: 100.0
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
    rationale: |
      McKenzie et al. 2023 state "a target cost of several dollars per target
      is acceptable if a target gain of 200 can be achieved." The target is a
      complex consumable assembly. Novel materials (borophene, white graphene)
      enable solution-based manufacturing. $100M is a placeholder for the
      target factory capital cost, analogous to other IFE target factory
      estimates. Highly uncertain -- no published factory design or bottom-up
      cost estimate exists.

  - account: C220110
    value: 0.15 * generic.costs.c220110
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
    rationale: |
      Negligible neutron activation eliminates the need for rad-hardened
      remote handling equipment. Maintenance can be performed with
      conventional equipment in a non-activated environment. Retained at
      15% for mechanical handling of consumable target assemblies, laser
      optics maintenance, and general reactor chamber access.

  - account: CAS21
    value: 0.50 * generic.costs.cas21
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation; hb11-patent-reactor-design.md §Reactor Architecture"
    rationale: |
      Eliminated facilities: tritium processing building, hot cell for
      activated-component handling, heavy biological shielding structure,
      cryogenic target preparation facility. Retained: reactor building
      (simplified), turbine building (if thermal conversion), laser building,
      target fabrication facility, electrical building, control building.
      50% reduction reflects elimination of ~half the building scope of a
      DT IFE plant.

  - account: CAS27
    value: 1.0
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Introduction"
    rationale: |
      Initial reactor material inventory is solid hydrogen-boron fuel at
      room temperature. No cryogenic handling, no tritium, no lithium
      compounds, no FLiBe. Boron-11 is industrial commodity (~$1-5/kg).
      $1M placeholder covers initial fuel inventory and target assembly
      materials. Negligible relative to DT concepts requiring tritium
      ($30k+/g startup inventory) and FLiBe.

  - account: CAS70
    value: 0.50 * generic.costs.cas70
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Commercialisation"
    rationale: |
      McKenzie et al.: "significant operational costs of DT systems are
      primarily associated with the replacement of activated reactor
      components... For the HB11 system, these costs are reduced." No
      neutron-driven component replacement (25-year lifetime assumed).
      Primary O&M cost is laser diode replacement ($1/W, 2.2 billion
      shot lifetime). 50% reduction from DT default reflects elimination
      of activated-component replacement program while retaining laser
      maintenance, target factory operations, and general plant O&M.

  - account: CAS80
    value: 0.5
    enabled: true
    provenance: derived
    source: "link-10-1007-s10894-023-00349-9/output.md §Introduction; §Commercialisation"
    rationale: |
      Raw fuel cost is negligible. Boron-11 is 80% of natural boron
      (industrial commodity). Hydrogen is ubiquitous. No tritium
      procurement. Annual boron consumption estimated at <10^6 tons
      against ~10^9 tons global reserves. $0.5M/yr placeholder.
      Target fabrication cost (the real fuel-cycle driver) is allocated
      to C220108.
```

**Override count: 9 enabled.** The override-count rubric for Low archetype-fit expects 6--12 enabled overrides. This count (9) falls within the expected band. The dominant theme is architectural elimination of DT-specific subsystems (tritium blanket, shielding, pulsed power, activated-component maintenance) that the p-B11 aneutronic fuel cycle renders unnecessary. The driver cost (C220104), which is likely the largest single cost account, has **no** override because no company-published cost figure exists.

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Target gain (G) at net-energy-positive levels: current demonstration is ~4 orders of magnitude below breakeven. No experimental or validated simulation basis for G=100--300. | S2, S3, S5 | truly-unknown | blocking | Fundamental physics research; no source can fill this gap without new experimental results. |
| 2 | Laser driver capital cost: no published estimate for a 30 kJ, 1 ps, 30 PW CPA laser system at Hz repetition rate. | S2, S5 | proprietary / truly-unknown | blocking | LLNL or ELI cost studies for PW-class systems; diode-pumped SSL cost curves from laser industry. |
| 3 | Direct energy conversion efficiency and design: no prototype, no efficiency measurement, no engineering design for alpha-particle DEC at power-plant scale. | S2, S3, S5 | truly-unknown | blocking (if DEC pathway is selected) | Literature on charged-particle direct conversion (Venetian blinds, ICC); Prelas 2007 and Johansson 2003 cited in McKenzie. |
| 4 | Consumable target unit cost: "several dollars per target" is an acceptability threshold, not a cost estimate. No manufacturing process, no bill of materials, no volume-production cost analysis. | S2, S4, S5 | truly-unknown | blocking | Target fabrication studies from NIF/IFE community; analogues from semiconductor or ammunition batch production. |
| 5 | Repetition rate engineering: no demonstration of Hz-rate laser firing, target loading, chamber clearing, or vacuum re-establishment for this concept. | S2, S3, S5 | truly-unknown | important | IFE chamber clearing literature (HYLIFE-II, HAPL); laser rep-rate studies from ELI, TRUMPF. |
| 6 | Laser wall-plug efficiency at required pulse parameters: 20% assumed, not demonstrated for 30 kJ ps CPA systems. | S2, S5 | not-yet-sourced | important | Diode-pumped SSL efficiency data from LLNL, HiLASE, ELI. |
| 7 | Alpha-particle damage to reactor materials: McKenzie et al. note "materials research will also be needed." No data exists. | S3, S4 | truly-unknown | important | Materials irradiation studies with alpha-particle beams; analogy to fission alpha-recoil damage. |
| 8 | Isotopic enrichment cost for pure B-11 (if required to eliminate B-10 neutron side reactions). | S4 | not-yet-sourced | nice-to-have | Boron isotope separation literature; enrichment cost data from isotope suppliers. |
| 9 | O&M cost breakdown: no published fixed vs. variable O&M, no scheduled maintenance plan, no staffing estimate. | S5 | proprietary | important | General IFE O&M estimates from GEM, HAPL, LIFE studies; scale from NIF operational costs. |
| 10 | Energy conversion pathway (DEC vs. thermal): design pivot from patent (DEC) to website (steam cycle) is documented but not explained. Choice has ~2x LCOE effect. | S2, S5 | proprietary | important | Company clarification; engineering trade study. |

## Section 7: Family-Delta vs Comparables

### vs. 23-laser-icf-nanostructured-target (Marvel Fusion)

Both concepts share the same fuel (p-B11), the same confinement family (IFE), and many of the same architectural advantages over DT laser ICF (no tritium, no cryogenic targets, no heavy shielding, abundant fuel). The family-delta is in the driver architecture, target physics, energy conversion, and scale.

**Driver architecture: picosecond CPA vs. femtosecond CPA**
- HB11 uses a two-laser system: a ~1 ps, 30 kJ, 30 PW CPA laser for proton fast ignition plus a ~3 kJ nanosecond laser to generate kilotesla magnetic fields via a capacitor-coil target. Marvel Fusion uses femtosecond (~30 fs) DPSSL pulses on nanostructured silicon targets, targeting ~10 Hz repetition rate with ~500 laser systems at commercial scale.
- **Cost direction**: HB11's single-shot energy (30 kJ) is higher but at lower rep rate (~1 Hz); Marvel's per-shot energy is lower but at higher rep rate (~10 Hz). The module-count multiplier (Marvel requires ~500 lasers vs. HB11's 2) is a major capital cost difference. HB11's approach may have lower driver capital cost per unit but the comparison is speculative -- neither concept has a published driver cost.

**Target physics: fast ignition with magnetic confinement vs. nanostructured ablation**
- HB11 relies on proton fast ignition: laser-accelerated protons are both reactants and the ignition mechanism. The fuel is magnetically confined by a laser-generated kilotesla field. This is a non-thermal initiation pathway.
- Marvel relies on femtosecond laser interaction with nanostructured targets to achieve non-thermal proton acceleration and fusion. No external magnetic confinement.
- **Cost direction**: HB11's consumable magnetic field device (destroyed every shot) is a significant per-shot cost item with no analogue in Marvel's approach. Marvel's nanostructured targets may be simpler to manufacture (silicon-based, semiconductor fab analogy) but are uncosted. **Advantage: uncertain, potentially Marvel** due to simpler consumable.

**Energy conversion: unsettled vs. hybrid**
- HB11 has pivoted between direct electrostatic conversion (patent) and conventional steam cycle (2025 website). McKenzie et al. discuss DEC at ~50% and MHD+Rankine at ~64%.
- Marvel proposes a hybrid approach (direct conversion + thermal) at ~70% combined efficiency -- which concept 23's analysis flags as "extraordinary" and TRL 1--2.
- **Cost direction**: If either concept achieves direct conversion, the thermal BOP (~$100--200M for a conventional steam island) is eliminated. Both claims are unvalidated. **Neutral -- neither has demonstrated any energy conversion beyond conventional thermal.**

**Design point scale: 500 MWe vs. 100 MWe**
- HB11's design point is 500 MWe; Marvel's is 100 MWe (pilot).
- **Cost direction**: At 1 GWe NOAK comparison, scale differences wash out. The native-scale difference means HB11's native LCOE benefits from better capital amortization, but this is a parameter choice, not a physics advantage.

**Physics gap: comparable**
Both concepts face the same fundamental challenge: no demonstrated net energy gain from p-B11 fusion. HB11's best result is ~10^10 alpha/sr at Osaka LFEX (~0.005--0.01% laser-to-alpha conversion); Marvel's experimental results are not published. Both are 4+ orders of magnitude from breakeven. Neither has a validated path to the required gain.

**Summary**: The two concepts are structurally similar (same fuel, same confinement family, same architectural advantages over DT). The primary divergences are in driver architecture (HB11's two-laser + kT magnetic field vs. Marvel's femtosecond multi-laser array) and target design (HB11's complex consumable assembly vs. Marvel's nanostructured targets). Neither divergence can be costed with confidence given the data available. The binding constraint for both is identical: the unresolved question of whether p-B11 fusion can achieve net energy gain at all.

## Section 8: Sources

1. **McKenzie, W., Batani, D., Mehlhorn, T.A. et al., "HB11 -- Understanding Hydrogen-Boron Fusion as a New Clean Energy Source," *J. Fusion Energy* 42, 17 (2023). DOI: 10.1007/s10894-023-00349-9.**
   - Contributes: The only peer-reviewed technoeconomic analysis. Provides the power-loop model (f = 1/(epsilon * eta * G)), LCOE boundary conditions ($35--350/MWh), gain requirements (G = 100--300 at eta = 20%), diode replacement cost ($1/W at 2.2B shots), target cost threshold ("several dollars"), boron fuel abundance, and a candid assessment of physics gaps (4 orders of magnitude to breakeven, bremsstrahlung barrier, avalanche debate, simulation limitations).
   - Found: knowledge/concept_research/04-laser-icf/iter-03/sources/link-10-1007-s10894-023-00349-9/output.md

2. **Hora, H. et al., US Patent US10410752B2 / US20170125129A1, "Method for Generating Electrical Energy by Laser-Based Nuclear Fusion and Laser Reactor" (filed 2014, granted 2019).**
   - Contributes: Most detailed reactor architecture description. Specifies: two-laser system (30 kJ ps CPA + 10 kJ ns), consumable magnetic field device (nickel plates, coils, foam, fuel pellet), direct electrostatic conversion at -1.4 MV, stainless steel sphere (>=1 m, 10 mm wall), fuel pellet geometry (1 cm x 0.2 mm cylinder), ~5 g TNT shock per shot, 1 Hz repetition rate. No cost data.
   - Found: knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-patent-reactor-design.md

3. **Margarone, D. et al., "In-Target Proton-Boron Nuclear Fusion Using a PW-Class Laser," *Applied Sciences* 12(3):1444 (2022). DOI: 10.3390/app12031444.**
   - Contributes: Best published experimental result for laser-driven p-B11 fusion. Alpha-particle flux ~1.2 x 10^10/sr (Osaka LFEX, ~1.4 kJ in 2.2 ps). Laser-to-alpha conversion efficiency ~0.005%. Establishes the 4-order-of-magnitude gap to breakeven. In-target geometry shows ~10x improvement over pitcher-catcher.
   - Found: knowledge/concept_research/04-laser-icf/iter-01/sources/hb11-osaka-experiment-2022.md

4. **Dossier: Laser ICF (p-B11) -- HB11 Energy.** Last updated 2026-03-07, 2 iterations, overall confidence medium.
   - Contributes: Structured synthesis of differentiation table values, energy capture design pivot documentation (patent DEC to website steam cycle), driver technology description, experiment history, funding level (~A$12.8M total), remaining gaps.
   - Found: knowledge/concept_research/04-laser-icf/dossier.md

5. **HB11 Energy Technology Page (2025).** https://hb11.energy/our-technology/
   - Contributes: Confirms "conventional steam cycle generator" (energy conversion pivot), "arrays of nanosecond and picosecond lasers," ~1 Hz repetition rate.
   - Found: knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-technology-page-2025.md (extraction incomplete)

6. **New Atlas Article (2020).** Blain, L., "Radical hydrogen-boron reactor leapfrogs current nuclear fusion tech."
   - Contributes: McKenzie quotes on reactor simplicity ("largely empty metal sphere"), no thermal BOP ("no need for a heat exchanger or steam turbine generator"), timeline caution ("I don't want to be a laughing stock").
   - Found: knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-newatlas-article.md

7. **HB11 Recent Developments 2024-2025 Compilation.**
   - Contributes: TINEX membership, Adelaide USPL partnership (A$8.2M), DOE INFUSE grant for innovative H2-boron fuel targets, Optica OPN profile confirming "hybrid burn target design."
   - Found: knowledge/concept_research/04-laser-icf/iter-02/sources/hb11-recent-developments-2024-2025.md

8. **Concept 23 Analysis (Laser ICF Nanostructured Target -- Marvel Fusion).**
   - Contributes: Family-delta comparison. Design point: 100 MWe pilot, 10 Hz, femtosecond DPSSL, hybrid energy conversion at 70%. 1 GWe NOAK LCOE: 793.2 $/MWh. Driver cost $2B (weakly grounded). Same p-B11 fuel, same physics gap.
   - Found: exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/analysis.md
