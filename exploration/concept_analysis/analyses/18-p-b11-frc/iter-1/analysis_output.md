## Design Point

- Name: Da Vinci 50 MWe pilot plant (TAE Technologies, December 2025 merger announcement)
- Maturity: paper-concept
- P_native: 50 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-djt-merger-davinci-specs.md
  - knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-energy-conversion-clarification.md

## 1. Availability of Data

**Rating: Limited**

TAE Technologies has published extensive information on its experimental program (Norman/C-2W device) but minimal detail on the Da Vinci commercial pilot plant. The December 2025 Trump Media (DJT) merger announcement discloses only one specification: 50 MWe net electric output, with construction planned for 2026.

### What exists:
- **Experimental physics foundation**: TAE's Nature Communications 2025 paper (Roche et al.) demonstrates NBI-only FRC formation, achieving total plasma temperatures of ~3 keV and densities of 1-3×10¹⁹ m⁻³ in the Norman device. This represents proof-of-principle for the beam-driven FRC concept but remains far from reactor-relevant temperatures of 100-200 keV required for p-B11 fusion.

> "TAE reporting up to a 50% decrease in reactor size, complexity, and overall construction expenses relative to earlier prototypes and competing designs"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Cost Reductions

- **FRC physics literature**: Reactor-scale FRC modeling exists in peer-reviewed literature (Putvinski et al. Nucl. Fusion 2019, Steinhauer Phys. Plasmas 2011). These studies describe FRC confinement scaling, stability requirements, and geometric constraints for fusion-relevant devices, providing context for extrapolating from Norman to Da Vinci.

- **p-B11 fuel cycle analysis**: Rider (Phys. Plasmas 1997) and Nevins & Swain (Phys. Plasmas 2000) provide foundational physics analysis of proton-boron fusion, including bremsstrahlung losses, optimal density regimes (n_e ~ 5×10²⁰ m⁻³), and temperature requirements (T_i ~ 150-250 keV, T_e ~ 80 keV to minimize radiation losses).

- **Patent disclosures**: TAE's Inverse Cyclotron Converter (ICC) patents (US7459654, US6628740, US6888907) describe direct energy conversion technology targeting >90% efficiency, but these are conceptual designs without demonstrated reactor-scale operation.

### What is missing:
- **No Da Vinci design specification**: Geometry, magnetic field configuration, plasma volume, confinement time, NBI power requirements, and magnetic field strength are unpublished. The analyst-patch source (iter-03/sources/analyst-patch-spec-anchors.md) provides physics-constrained estimates but notes these are "Norman-extrapolated OR physics-constrained... TAE has not published reactor-scale Da Vinci parameters."

- **No cost breakdown**: Capital cost estimates, subsystem costs, or LCOE projections are absent. TAE claims "up to 50% cost reductions relative to tokamak-based plants" but provides no supporting detail.

- **No performance targets**: Q (energy gain), capacity factor, availability, or burn duration are undisclosed. The only confirmed target is achieving Q>1 (net energy gain).

- **No energy conversion pathway detail for Da Vinci**: The tae-energy-conversion-clarification.md FAQ explicitly describes thermal/steam conversion:

> "a network of pipes will spring into action to cool the fusion machine's interior by collecting that heat into a fluid and ushering it to a steam generator. The steam spins a turbine that then drives an electric generator"
> — knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-energy-conversion-clarification.md §How do you produce electricity from fusion?

This contradicts TAE's long-term vision of direct energy conversion via the ICC, which TAE frames as a future upgrade, not the Da Vinci baseline.

## 2. Challenges in Capturing System Function

The primary LCOE modeling challenges for the p-B11 FRC concept stem from fundamental physics uncertainties, the aneutronic fuel cycle's extreme temperature requirements, and the absence of a published reactor-scale design.

### Challenge 1: Net energy gain undemonstrated for p-B11 (Critical - concept-gating)

> "Achieving net energy gain (Q > 1) remains undemonstrated for p-¹¹B, with current experiments yielding fusion products but far below breakeven due to these plasma physics challenges"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Aneutronic Fusion via p-B11 Reaction

The proton-boron reaction cross-section peaks at ~600 keV, requiring plasma temperatures of 100-200 keV for meaningful reactivity — an order of magnitude beyond Norman's ~3 keV. Bremsstrahlung radiation losses scale with Z_eff and dominate at these temperatures unless T_e is held significantly below T_i (~80 keV vs ~150 keV per Rider 1997). No FRC experiment has approached these conditions. The physics extrapolation from Norman to Da Vinci is larger than the gap from ITER parameters to D-T reactor operation.

**LCOE impact**: If Q remains below unity, no commercial operation is possible. If Q is achieved but at the low end of projections (Q ~ 2-3), the recirculating power fraction becomes prohibitive for competitive LCOE. The analyst-patch assumes p_input/P_native = 100/50 = 2.0, implying Q_eng ~ 0.5 — below breakeven. This reflects the high recirculation expected for first-generation p-B11 systems but is inconsistent with net power production.

### Challenge 2: FRC confinement scaling to reactor size (High - affects capital costs)

FRCs are inherently susceptible to global MHD instabilities (tilt mode, rotational kink mode) and anomalous transport that degrades energy confinement. Steinhauer (Phys. Plasmas 2011) notes that kinetic stabilization mechanisms effective in compact FRCs "diminish at larger scales required for fusion ignition."

> "Reactor-relevant FRCs, necessitating major radii of approximately 1-2 meters... face amplified risks of these modes"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §FRC Stability Challenges

Norman operates at separatrix radius r_s ~ 0.4 m. The analyst-patch scales Da Vinci to r_s = 2.0 m (5× linear scaling) to reach ~10 MA plasma current required for reactor-class operation. This scaling is within the Putvinski 2019 reactor design range but has never been experimentally validated. If confinement degrades faster than empirical scaling laws predict, the required plasma volume and magnetic field strength (hence capital costs) increase accordingly.

**LCOE impact**: Capital costs for CAS22 (reactor plant equipment) scale with plasma volume and magnetic field. If confinement scaling is unfavorable, the chamber_length may need to increase from the assumed 8 m to maintain adequate Lawson triple product, directly impacting building costs (CAS21) and magnet costs (C220103).

### Challenge 3: Beam-driven sustainment power requirements (High - affects recirculating power)

TAE's beam-driven FRC concept relies exclusively on neutral beam injection (NBI) for plasma formation, heating, current drive, and stabilization. Norman uses 21 MW of NBI for ~30 ms pulse lengths at sub-fusion temperatures. The analyst-patch estimates 100 MW p_input for Da Vinci at 50 MWe net output.

> "Sustainment poses additional intrinsic hurdles... incurring recirculating power fractions that challenge steady-state viability"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Sustainment challenges

At p_input = 100 MW and P_native = 50 MWe, the implied recirculating fraction is 100/(50 + 100) = 66.7%, leaving Q_eng = 0.5. This is physically inconsistent with net power production — either P_native is higher than 50 MWe at this input power, or p_input must be lower. TAE has not published the intended Q_eng for Da Vinci, making power balance closure impossible without additional assumptions.

**LCOE impact**: NBI systems cost ~$1-2M per MW of injected power (from tokamak ITER costing). At 100 MW, NBI capital costs alone approach $100-200M. If p_input scales higher than 100 MW to achieve adequate plasma heating, both capital costs and recirculating power fraction increase, directly degrading LCOE.

### Challenge 4: Direct energy conversion vs thermal cycle ambiguity (Moderate - affects efficiency and costs)

TAE's long-term vision includes the Inverse Cyclotron Converter (ICC) for direct energy conversion at >90% efficiency, but the tae-energy-conversion-clarification.md FAQ explicitly describes thermal/steam conversion for the near-term plant. The patent literature on ICC shows a conceptual design with "four or more equal, semi-cylindrical electrodes" in a "hollow cylinder with a length of about five meters" converting 5 MHz fusion output power to 60 Hz grid frequency.

No ICC has been built or tested at fusion-relevant power levels. The claimed >90% efficiency is simulation-derived. If Da Vinci defaults to thermal conversion, the thermal efficiency is limited to ~40% (Rankine steam cycle) or ~45-50% (supercritical CO2), reducing net electric output for a given fusion power and increasing LCOE.

**LCOE impact**: Direct conversion at 90% efficiency vs thermal at 40% implies a 2.25× difference in electric output for the same fusion power. If the cost of the ICC (capital cost, development risk, operational complexity) is lower than the cost of scaling up the fusion power by 2.25× to compensate for thermal conversion losses, ICC becomes the economically favored pathway. Without ICC costing or a confirmed Da Vinci energy conversion pathway, LCOE estimates carry large uncertainty.

### Challenge 5: Regulatory and tritium exemptions (Low - affects licensing timeline, not LCOE physics)

p-B11 fusion produces <1% neutron energy from side reactions, enabling hands-on maintenance and eliminating tritium breeding infrastructure. TAE emphasizes this as a cost advantage:

> "avoiding neutron-induced material degradation, allowing for durable, lower-maintenance reactor walls"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Material advantages

However, the U.S. NRC has not yet established a regulatory framework specific to aneutronic fusion. If Da Vinci is regulated under the same framework as D-T reactors (10 CFR Part 50), the claimed cost savings from reduced shielding and simplified blanket design may be offset by regulatory conservatism. The timeline impact (licensing delays) is more significant than the direct LCOE impact.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in **ascending order of maturity** (least mature first):

### p-B11 fusion physics at reactor scale (TRL 2-3)

**Demonstrated**: TAE demonstrated first p-B11 fusion in a magnetically confined plasma (with NIFS Japan, 2023). Norman achieves ~3 keV total plasma temperature and densities of 1-3×10¹⁹ m⁻³.

**On paper only**: Reactor-scale p-B11 FRC achieving T_i ~ 150 keV, T_e ~ 80 keV, n_e ~ 5×10²⁰ m⁻³, and Q>1. These conditions are 50× higher in temperature and 50× higher in density than current Norman performance. Simulation studies (Putvinski 2019, Nevins & Swain 2000) suggest these parameters are theoretically achievable but have no experimental validation.

**Missing at scale**: Sustained burn at Q>1, confinement time scaling validation, bremsstrahlung loss mitigation at Z_eff ~ 3, and demonstration that beam-driven current sustainment can maintain stability at reactor scale.

### Inverse Cyclotron Converter for direct energy conversion (TRL 2-3)

**Demonstrated**: Patent literature describes conceptual design. No prototype has been built or tested.

**On paper only**: ICC converting 5 MHz charged particle exhaust to 60 Hz AC power at >90% efficiency. The patent (US7459654) describes a "hollow cylinder... length of about five meters" with quadrupole electric field structure, but provides no experimental validation.

**Missing at scale**: ICC fabrication, high-voltage electrode survivability in fusion exhaust environment, power conditioning electronics for MW-class output, and efficiency demonstration at any power level.

### FRC formation and sustainment via NBI alone (TRL 4-5)

**Demonstrated**: TAE's 2025 Nature Communications paper (Roche et al.) demonstrates NBI-only FRC formation in Norman, eliminating plasma gun formation hardware. This represents a major technical milestone:

> "reducing hardware requirements by nearly 50%"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §NBI breakthrough

Norman sustains FRC plasmas for ~30 ms with 21 MW NBI input, achieving plasma currents of 300-350 kA.

**On paper only**: Steady-state or quasi-steady-state FRC sustainment at reactor temperatures (100-200 keV) with 100+ MW NBI input. Current pulse lengths (~30 ms) are limited by NBI pulse duration, not FRC physics, but extension to seconds or minutes is undemonstrated.

**Missing at scale**: Reactor-class NBI systems (100-300 keV, 100+ MW total), beam-target coupling efficiency at reactor densities, and current drive efficiency at high temperatures.

### High-power neutral beam injection systems (TRL 5-6)

**Demonstrated**: ITER-class NBI systems deliver 16.5 MW per injector at 1 MeV (D⁻ negative ion sources). TAE's Norman uses eight injectors (four fixed 15 keV, four tunable 15-40 keV) at 13 MW total. NBI technology is mature for tokamaks.

**On paper only**: NBI optimized for FRC geometry (tangential injection, high beam-target coupling) at 100+ MW total power and 100-300 keV energies required for p-B11 fuel heating.

**Missing at scale**: Continuous-wave or long-pulse operation at reactor-class power levels. Current ITER NBI systems are pulsed (3600s burn, 1000s dwell). Da Vinci's steady-state or quasi-steady-state operation requires continuous NBI, which is unprecedented.

### Magnetic field control and plasma diagnostics (TRL 6-7)

**Demonstrated**: Norman has "flexible edge-biasing electrode systems," "active feedback control using Trim and Saddle coils," and "50+ dedicated plasma diagnostics."

> "proprietary power supplies and real-time active feedback controls"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/tae-nbi-breakthrough-2025.md §Technology

Copernicus (Norman's successor) features "750 megawatts of bi-directional electricity on sub-millisecond timescales" for plasma control.

**On paper only**: Scaled-up feedback control for reactor-scale FRC with higher plasma currents (~10 MA vs Norman's 300 kA) and larger plasma volumes.

**Missing at scale**: Sensor and actuator technology surviving reactor neutron/radiation environment for aneutronic but non-zero neutron flux (p-B11 side reactions).

### FRC stability control (TRL 5-6)

**Demonstrated**: Norman uses rotation (via edge biasing), neutral beam-driven flows, and external magnetic field shaping to suppress tilt and kink modes. Roche et al. 2025 shows tilt stability in NBI-sustained FRCs.

**On paper only**: Stability at reactor-scale plasma currents and larger radii where kinetic stabilization mechanisms weaken.

**Missing at scale**: Long-pulse stability demonstration (>1 second). Norman's 30 ms pulse lengths are insufficient to assess slow-growing modes that may become unstable on transport timescales (hundreds of ms to seconds).

### Aneutronic reactor materials and shielding (TRL 4-5)

**Demonstrated**: p-B11 fusion produces <1% neutron energy, enabling thin shielding and hands-on maintenance:

> "little or no radioactivity"
> — knowledge/concept_research/18-p-b11-frc/iter-02/sources/tae-energy-conversion-clarification.md §Fuel cycle

The analyst-patch assumes neutron wall loading of 0.05-0.2 MW/m² vs 2-4 MW/m² for D-T, reducing blanket/shield costs to 30-50% of D-T baseline.

**On paper only**: First-wall materials surviving X-ray and charged particle fluxes from p-B11 fusion. While neutron damage is minimal, surface heat loads and erosion from direct charged particle impact are significant. No experimental test facility replicates p-B11 fusion surface conditions.

**Missing at scale**: Long-term material qualification, activation and decommissioning pathways, and regulatory acceptance of "low-activation" fusion (no established precedent for licensing aneutronic reactors as distinct from D-T).

### Thermal power conversion (steam or sCO2 cycle) (TRL 8-9)

**Demonstrated**: Conventional Rankine steam cycles and supercritical CO2 Brayton cycles are mature commercial technologies deployed at GW scale in fission and fossil plants.

**On paper only**: Integration with aneutronic fusion heat source. The first-wall heat flux profile and thermal transient behavior differ from fission or D-T fusion.

**Missing at scale**: Nothing — this is the most mature subsystem. If Da Vinci uses thermal conversion, this component is low-risk.

## 4. Key Materials and Supply Chain Considerations

### Boron-11 fuel supply

> "Boron-11 constitutes about 80% of natural boron, sourced from minerals like borax, making it economically viable"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Fuel materials

Natural boron is ~20% ¹⁰B and ~80% ¹¹B. Borax (sodium borate) deposits are abundant globally (Turkey, USA, Chile, Argentina), with annual production ~4 million tonnes. For fusion fuel, isotopic enrichment to >99% ¹¹B may be required to minimize neutron production from ¹⁰B(p,α)7Be side reactions. Isotopic separation of boron is industrially practiced (for semiconductor applications) but not at the scale or purity required for fusion fuel.

**Supply chain risk**: Low. Boron availability is not a constraint. Enrichment infrastructure would need to scale, but the technology exists.

**Cost**: Natural boron costs ~$2-5/kg. Enriched ¹¹B is estimated at $50-200/kg (by analogy to lithium isotope separation), but at ~kg/day fuel consumption rates, annual fuel costs are negligible (<$1M/year) compared to capital costs or NBI operating costs.

### Hydrogen fuel supply

Hydrogen (¹H) is the most abundant element in the universe and industrially produced at ~70 million tonnes/year globally. For fusion, ultra-pure hydrogen is required, but this is a commodity product for semiconductor and industrial gas markets.

**Supply chain risk**: None.

### Neutral beam injector components

High-power NBI systems require:
- **Cesium-seeded negative ion sources**: Cesium metal is a specialty material (global production ~20 tonnes/year) but required in small quantities (grams per injector). Supply is adequate.
- **High-voltage accelerator grids**: Molybdenum or copper-alloy grids withstanding 100+ kV. These are precision-machined components with long lead times but no fundamental material constraint.
- **RF drivers and power supplies**: Conventional high-power electronics.

**Supply chain risk**: Low. NBI component fabrication is established for ITER/JT-60SA programs.

**Cost**: ITER NBI injectors cost ~$20-30M per unit (16.5 MW capacity). Scaling to TAE's 100 MW requirement implies ~6 injectors at $120-180M capital cost for the NBI subsystem alone.

### Magnet materials

TAE emphasizes its FRC design uses conventional magnets, not superconducting coils:

> "without the cryogenic superconducting magnets required in tokamaks"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Cost advantages

Norman uses copper coils for equilibrium, mirror, and trim fields. Da Vinci's magnet type is undisclosed but likely resistive based on FRC's near-unity beta (β ~ 0.9-1.0), which minimizes external field requirements.

**If resistive magnets**: Copper or aluminum conductors. Supply chain is well-established. Power consumption for resistive magnets is significant (10s of MW continuous draw), contributing to recirculating power fraction.

**If superconducting magnets** (HTS or LTS): Would enable lower recirculating power but at higher capital cost and added cryogenic infrastructure. No indication TAE plans superconducting magnets for Da Vinci.

### Inverse Cyclotron Converter materials

The ICC patent describes "four or more equal, semi-cylindrical electrodes" in a 5-meter cylinder. High-voltage electrodes in fusion exhaust must withstand:
- Charged particle bombardment (MeV-class protons and alpha particles)
- X-ray flux
- High vacuum and thermal cycling

Materials candidates: Refractory metals (tungsten, molybdenum), graphite, or SiC composites. These are established fusion-facing materials but have never been deployed in direct energy converter geometry.

**Supply chain risk**: Low for materials. Fabrication complexity and electrode survivability are TRL risks, not material availability risks.

### First-wall and structural materials

Aneutronic fusion eliminates the need for advanced reduced-activation materials (RAFM steels, SiC composites) required for D-T reactors. Conventional 304 or 316 stainless steel may be adequate for the pressure vessel and first wall, given neutron wall loading is 10-20× lower than D-T:

> "avoiding neutron-induced material degradation, allowing for durable, lower-maintenance reactor walls"
> — knowledge/concept_research/18-p-b11-frc/iter-01/sources/grokipedia-tae-technologies.md §Material advantages

**Supply chain risk**: None. Stainless steel is a commodity material.

**Cost advantage vs D-T**: The analyst-patch assumes C220101 (blanket) at 0.50× library baseline and C220102 (shield) at 0.30× library baseline, reflecting the reduced neutronics requirements. However, surface heat loads from charged particle impact may require tungsten plasma-facing components similar to D-T divertors, partially offsetting material cost savings.

## 5. Design Point Parameters

The Da Vinci design point is physics-constrained and Norman-extrapolated. TAE has not published reactor-scale specifications. All quantitative values below are derived from the analyst-patch source (iter-03/sources/analyst-patch-spec-anchors.md), which combines Putvinski 2019 reactor-class FRC modeling, Rider/Nevins p-B11 physics analysis, and 5× linear scaling from Norman experimental parameters.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Net electric power** | 50 MWe | tae-djt-merger-davinci-specs.md | high | TAE disclosure, Dec 2025 DJT merger announcement |
| **chamber_length** | 8.0 m | analyst-patch-spec-anchors.md §Verified spec values | medium | PHYSICS-CONSTRAINED: Putvinski 2019, Steinhauer 2011 (L = 6-10 m for net-electric p-B11). Spec key: `chamber_length` |
| **Separatrix radius (r_s)** | 2.0 m | analyst-patch-spec-anchors.md §Verified spec values | medium | Norman × 5 scaling to I_p ~ 10 MA reactor target; Putvinski 2019 (r_s = 1.5-2.5 m). Spec key: `plasma_t` |
| **Plasma volume** | 50 m³ | analyst-patch-spec-anchors.md §Verified spec values | medium | DERIVED: 0.5 × π × r_s² × L = 0.5 × π × 4 × 8 ≈ 50.3 m³ (Steinhauer 2011 FRC mid-plane). Spec key: `plasma_volume` |
| **Internal FRC field (B)** | 5.0 T | analyst-patch-spec-anchors.md §Verified spec values | medium | PHYSICS-CONSTRAINED: MHD pressure balance B² × β / (2 μ₀) ≥ P_plasma. At β=0.9, n_e=5e20, T_i=150 keV: B ≥ 5.2 T. Spec key: `B` |
| **External axial field (B_ext)** | 0.5 T | analyst-patch-spec-anchors.md §Verified spec values | low | Norman × 5 scaling; Norman B_ext = 0.1 T (Gota 2020), Putvinski 2019 reactor ~0.5-1.0 T. Spec key: `b_center` |
| **Electron density (n_e)** | 5.0×10²⁰ m⁻³ | analyst-patch-spec-anchors.md §Verified spec values | medium | PHYSICS-CONSTRAINED: Nevins & Swain 2000, Rider 1997 p-B11 sweet spot. Spec key: `n_e` |
| **Electron temperature (T_e)** | 80 keV | analyst-patch-spec-anchors.md §Verified spec values | medium | PHYSICS-CONSTRAINED: Rider/Nevins: T_e < T_i to avoid bremsstrahlung dominance with Z_eff ~ 3. Spec key: `T_e` |
| **Ion temperature (T_i)** | 150 keV | [inferred: p-B11 cross-section peaks at ~600 keV center-of-mass; T_i ~ 150-250 keV required per Rider 1997] | low | Not explicitly stated in analyst-patch but implied by n_e and p-B11 reactivity requirements |
| **Beta (β)** | 0.9-1.0 | [inferred: FRC inherent property, Steinhauer 2011] | high | Near-unity beta is defining characteristic of FRC confinement |
| **Plasma current (I_p)** | ~10 MA | [inferred: analyst-patch notes "Norman × 5... I_p ~ 10 MA reactor target"] | low | Norman I_p ~ 300-350 kA; 5× scaling yields ~1.5-1.75 MA; 10 MA is reactor-class target from literature |
| **Auxiliary heating power (p_input)** | 100 MW | analyst-patch-spec-anchors.md §Verified spec values | medium | PHYSICS-DERIVED: Reactor-class NBI 100-300 keV; Putvinski 2019 uses 100 MW class. Spec key: `p_input` |
| **Fusion power (P_fus)** | ~594 MW | [inferred: library back-solve from P_native + p_input, see note] | low | Analyst-patch notes library back-solves P_fus from P_native and auxiliary power; not directly specified |
| **Q_plasma** | ~5.9 | [derived: P_fus / p_input = 594 / 100] | low | Assumes library back-solve is self-consistent; TAE has not disclosed Q target |
| **Q_eng** | 0.5 | [derived: P_native / (P_native + p_input) = 50 / 150] | low | Physically inconsistent with net power generation; implies Da Vinci operates at breakeven or slightly below |
| **Energy conversion** | Thermal (steam) | tae-energy-conversion-clarification.md §How do you produce electricity | high | TAE FAQ explicitly describes thermal/steam cycle; ICC direct conversion is future upgrade |
| **Thermal efficiency (η_th)** | 0.40 | [estimated: Rankine steam cycle baseline] | low | sCO2 could reach 0.45-0.50 but not confirmed; ICC at 0.90 is aspirational |
| **Confinement time (τ_E)** | [unknown] | [not specified in sources] | N/A | Critical parameter for Lawson criterion; no value disclosed |
| **Burn duration** | [unknown] | [not specified in sources] | N/A | Steady-state, quasi-steady, or long-pulse operation not clarified |

**Critical parameter inconsistency**: The power balance implied by P_native = 50 MWe and p_input = 100 MW yields Q_eng = 0.5, below breakeven. This is physically inconsistent with net power production unless:
1. P_native is the net output to the grid after recirculating power is subtracted, and the gross electric output is higher, OR
2. p_input is lower than 100 MW, OR
3. The fusion power is significantly higher than the back-solved ~594 MW, implying a higher Q_plasma.

TAE has not disclosed which interpretation is correct. The analyst-patch acknowledges this inconsistency:

> "`p_input/P_native = 100/50 = 2.0` is well above F9's 0.5 cap, reflecting the high recirculation expected for a Q ~ 2-5 p-B11 plant... p-B11 fusion cross-section is ~1000× smaller than D-T at relevant T_i"
> — analyst-patch-spec-anchors.md §High recirculation power

## 5b. Override Candidates

```yaml
overrides:
  - account: C220101
    value: 0.50 * generic.costs.cas22_detail["C220101"]
    enabled: true
    provenance: derived
    source: "analyst-patch-spec-anchors.md §Overrides"
    rationale: |
      Aneutronic fuel cycle eliminates tritium breeding blanket. The library's 1 GWe
      modular-fleet default assumes Li-6 ceramic breeder with Be multiplier and
      tritium extraction system. For p-B11, the "blanket" is solely for energy
      capture (first-wall thermal load management), not breeding. Neutron wall loading
      of 0.05-0.2 MW/m² vs 2-4 MW/m² for D-T reduces material requirements and
      eliminates Li-6 procurement, tritium processing, and beryllium multiplier.
      Analyst-patch cites 0.50× multiplier reflecting reduced functionality and
      neutronics. No TAE-published blanket design exists; this is physics-grounded
      analogue scaling.

  - account: C220102
    value: 0.30 * generic.costs.cas22_detail["C220102"]
    enabled: true
    provenance: derived
    source: "analyst-patch-spec-anchors.md §Overrides"
    rationale: |
      Aneutronic fusion produces <1% neutron energy from side reactions (¹⁰B(p,α)7Be,
      secondary D-D from beam-target reactions). Neutron wall loading is 10-20× lower
      than D-T baseline. Shielding requirements are driven by secondary neutrons
      (2.45 MeV from D-D, ~1 MeV from ¹⁰B side reactions) and X-ray flux from
      bremsstrahlung. The library's shield thickness and material (borated steel,
      tungsten, polyethylene) are sized for 14.1 MeV neutron attenuation. For p-B11,
      shielding mass can be reduced to ~30% of D-T baseline (analyst-patch estimate).
      TAE emphasizes "little or no radioactivity" as cost advantage; 0.30× multiplier
      reflects this structural simplification at the 1 GWe modular-fleet scale.

  - account: C220104
    value: 180.0
    enabled: true
    provenance: derived
    source: "analyst-patch-spec-anchors.md §Overrides; ITER NBI costing analogue"
    rationale: |
      NBI-only plasma formation and sustainment at 100 MW p_input. ITER NBI injectors
      cost ~$20-30M per unit at 16.5 MW capacity. Scaling to 100 MW implies ~6
      injectors at $120-180M total. Analyst-patch uses $180M as upper-bound estimate
      for Da Vinci NBI subsystem. This is a per-unit (Class U) account — each module
      requires its own NBI set. The library default for C220104 (supplementary heating)
      assumes RF (ECRH/ICRH) at lower $/MW than NBI. TAE's beam-driven FRC is
      NBI-intensive by design; $180M per 50 MWe module reflects reactor-class NBI at
      100-300 keV beam energy. At the 1 GWe fleet scale (20 modules × 50 MWe), the
      NBI capital cost is $3.6B — a major LCOE driver.

  - account: CAS27
    value: 0.10 * generic.costs.cas27
    enabled: true
    provenance: derived
    source: "analyst-patch-spec-anchors.md §Overrides"
    rationale: |
      CAS27 (special materials — initial reactor inventory / blanket fill) is sized
      for D-T tritium breeding and coolant chemistry. For p-B11, the inventory is:
      (1) boron-11 fuel (natural boron at $2-5/kg, enriched ¹¹B at $50-200/kg;
      kg/day consumption → negligible annual cost), (2) hydrogen fuel (commodity),
      (3) first-wall coolant (water, helium, or molten salt — not FLiBe/Li-Pb breeder).
      No lithium-6 enrichment, no tritium startup inventory ($30k/g avoided), no
      beryllium pebbles. The library default at the 1 GWe modular-fleet scale includes
      FLiBe or Li-Pb inventory at 100s of tonnes per plant. For p-B11, material
      inventory is reduced to ~10% of D-T baseline. Analyst-patch applies 0.10×
      multiplier (Class P — power-proportional, fleet-wide).

  - account: CAS80
    value: 0.02
    enabled: false
    provenance: derived
    source: "analyst-patch-spec-anchors.md §Overrides"
    rationale: |
      CAS80 (annualized fuel cost) for p-B11 is negligible. Boron-11 at $50-200/kg
      enriched, consumed at ~kg/day, yields <$100k/year fuel cost for a 50 MWe plant.
      Hydrogen fuel is commodity-priced. Compare to D-T tritium at $30,000/g with
      kg-scale inventory requirements. Analyst-patch sets CAS80 = $0.02M/year but
      notes this override is "taught but NOT overridable today" per 1costingfe #106.
      The fleet-scale fuel cost is still trivial relative to LCOE; included here for
      completeness but `enabled: false` reflects current tool limitation.
```

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_plasma and Q_eng targets for Da Vinci | S5 | truly-unknown | blocking | TAE technical publication or investor deck disclosing fusion gain targets, confinement time, and power balance for 50 MWe design point |
| 2 | Energy conversion pathway — thermal vs ICC direct conversion | S2, S5 | truly-unknown | important | TAE engineering design publication clarifying whether Da Vinci baseline is thermal/steam (per FAQ) or ICC (per long-term vision) |
| 3 | Confinement time (τ_E) at reactor scale | S2, S5 | not-yet-sourced | blocking | Putvinski 2019 provides FRC scaling laws; TAE experimental validation of τ_E scaling from Norman to Copernicus would constrain Da Vinci extrapolation |
| 4 | Burn duration / pulse length for Da Vinci | S5 | truly-unknown | important | Steady-state, quasi-steady (minutes), or long-pulse (seconds) operation determines capacity factor and NBI duty cycle |
| 5 | Capital cost breakdown by subsystem | S1, S2 | proprietary | important | TAE has not published LCOE estimates or cost structure. Independent cost model (ARIES-equivalent for FRC) or TAE disclosure needed |
| 6 | NBI system specifications for Da Vinci | S3, S5 | proprietary | important | Number of injectors, beam energy (keV), beam power per injector, duty cycle, and target cost per MW of NBI capacity |
| 7 | ICC fabrication cost and TRL | S3, S5 | truly-unknown | important | Patents exist but no prototype cost or TRL assessment. Direct energy converter cost could dominate CAS22 if ICC is baseline |
| 8 | First-wall material specification | S4, S5 | truly-unknown | nice-to-have | Stainless steel, tungsten plasma-facing components, or novel materials (SiC, graphite) for charged particle impact |
| 9 | Magnet type for Da Vinci (resistive vs superconducting) | S4, S5 | not-yet-sourced | important | TAE emphasizes "no superconducting magnets" but has not explicitly disclosed Da Vinci magnet design. If resistive, power consumption is major recirculating power contributor |
| 10 | Capacity factor and maintenance schedule | S2, S5 | truly-unknown | important | Aneutronic fusion enables hands-on maintenance but first-wall replacement intervals, scheduled downtime, and availability targets are undisclosed |
| 11 | Regulatory pathway for aneutronic fusion | S2 | truly-unknown | nice-to-have | NRC has not established framework for licensing low-activation fusion distinct from D-T reactors. Timeline and cost impact uncertain |
| 12 | Boron-11 enrichment cost at fusion scale | S4, S5 | not-yet-sourced | nice-to-have | Industrial boron isotope separation exists (semiconductor industry) but not at fusion-scale tonnage. Enrichment cost projection from isotope separation industry analogue |

**Priority order for closing gaps**: Gaps #1, #2, and #3 are blocking for credible LCOE estimates. Without Q targets, energy conversion pathway, and confinement time scaling, the Da Vinci design point cannot be fully specified. Gaps #4, #5, and #6 are important for refining cost structure but secondary to fundamental physics closure.

## 7. Family-Delta vs Comparables

(No comparable concept in the corpus for this design point.)

The lack of a comparable concept reflects the unique position of TAE's beam-driven FRC pursuing p-B11 fuel. Within the taxonomy:
- **vs D-T FRCs** (e.g., Helion's pulsed FRC with D-He3/D-D): TAE uses steady-state beam sustainment, not pulsed magnetic compression. The fuel cycle (p-B11 vs D-He3) and confinement approach (beam-driven vs inductive) are fundamentally different.
- **vs D-T magnetic confinement** (tokamaks, stellarators, mirrors): p-B11 eliminates tritium breeding blankets, superconducting magnets (near-unity beta FRC), and heavy neutron shielding. These are structural cost advantages offset by extreme temperature requirements and undemonstrated Q>1.
- **vs other aneutronic concepts** (IEC, Polywell, p-B11 laser ICF): TAE's FRC is the only magnetically confined steady-state aneutronic concept at reactor scale in the corpus. IEC/Polywell are electrostatic (lower TRL, smaller scale). p-B11 laser ICF (HB11 Energy, Marvel Fusion) are pulsed inertial concepts with different cost structures (driver capital vs NBI capital).

The closest structural analogue is **beam-driven D-T magnetic mirror** (Realta Fusion), which shares NBI-intensive heating and linear geometry but uses D-T fuel and direct energy conversion via electrostatic collectors. However, mirrors have open-field-line geometry (axial loss cone) while FRCs are closed-field toroidal plasmas in a linear form factor — the confinement physics diverges.

## 8. Sources

Listed in order of importance:

1. **analyst-patch-spec-anchors.md** (iter-03/sources/analyst-patch-spec-anchors.md)
   - Provides physics-constrained design point parameters for Da Vinci, synthesized from Putvinski 2019, Steinhauer 2011, Rider 1997, Nevins & Swain 2000, and Norman experimental scaling.
   - Contains all quantitative values in Section 5 parameter table and override registry.
   - Acknowledges parameter synthesis is analyst-derived, not TAE-published.

2. **tae-djt-merger-davinci-specs.md** (iter-02/sources/tae-djt-merger-davinci-specs.md)
   - December 2025 Trump Media merger announcement.
   - Single confirmed specification: Da Vinci 50 MWe net electric output.
   - Construction planned for 2026, subject to regulatory approval.

3. **tae-energy-conversion-clarification.md** (iter-02/sources/tae-energy-conversion-clarification.md)
   - TAE FAQ explicitly describing thermal/steam conversion for power generation.
   - Confirms Da Vinci baseline uses conventional Rankine cycle, not ICC direct conversion.
   - Provides fuel cycle comparison (D-T, D-D, D-He3, p-B11) with p-B11 challenges acknowledged: "requires superior confinement and operational conditions to reach the considerably higher temperatures needed."

4. **grokipedia-tae-technologies.md** (iter-01/sources/grokipedia-tae-technologies.md)
   - Comprehensive TAE machine history: C-1, C-2/C-2U, Norman/C-2W, Copernicus, Da Vinci.
   - Norman performance parameters: separatrix radius 0.4 m, plasma current 300-350 kA, 13 MW NBI, total temperature ~3 keV.
   - Technical challenges: "Achieving net energy gain (Q > 1) remains undemonstrated for p-¹¹B" with bremsstrahlung losses and FRC scaling uncertainties explicitly noted.
   - Cost reduction claims: "up to a 50% decrease in reactor size, complexity, and overall construction expenses."

5. **tae-c2w-machine-details.md** (iter-02/sources/tae-c2w-machine-details.md)
   - Norman/C-2W experimental specifications: 21 MW NBI (eight injectors, 15-40 keV), electron temperature ~250-300 eV, electron density 1-3×10¹⁹ m⁻³, 30 ms pulse duration.
   - Subsystems: edge-biasing electrodes, trim/saddle coils for active feedback, 50+ diagnostics, 2000 m³/s pumping capacity.
   - Provides technology baseline for extrapolation to Da Vinci.

6. **tae-nbi-breakthrough-2025.md** (iter-01/sources/tae-nbi-breakthrough-2025.md)
   - 2025 press release on NBI-only FRC formation eliminating plasma gun hardware.
   - Claims "reducing hardware requirements by nearly 50%" and enabling "simpler, linear fusion machine that is much less complicated to construct, less costly to build and run."

7. **Nature Communications 2025** (Roche et al., s41467-025-58849-5) — referenced in grokipedia and other sources
   - Peer-reviewed publication demonstrating NBI-only FRC formation in Norman.
   - Not directly read for this analysis but cited in secondary sources as experimental validation of TAE's beam-driven approach.

8. **Putvinski et al., Nucl. Fusion 2019** — referenced in analyst-patch as "reactor-class FRC"
   - Provides FRC reactor design parameters: r_s = 1.5-2.5 m, L = 6-10 m, B_ext ~ 0.5-1.0 T, I_p ~ 10 MA.
   - Not directly read for this analysis but foundational for analyst-patch parameter derivation.

9. **Rider, Phys. Plasmas 1997** — referenced in analyst-patch
   - Foundational p-B11 physics analysis: bremsstrahlung losses, Z_eff ~ 3, optimal T_e/T_i ratio to minimize radiation.
   - Not directly read for this analysis but cited for T_e = 80 keV, T_i = 150 keV parameter choices.

10. **Nevins & Swain, Phys. Plasmas 2000** — referenced in analyst-patch
    - p-B11 optimal density regime: n_e ~ 5×10²⁰ m⁻³ "sweet spot" balancing reactivity and confinement losses.
    - Not directly read for this analysis but cited for density parameter choice.

11. **Steinhauer, Phys. Plasmas 2011** — referenced in analyst-patch
    - FRC geometry and confinement scaling laws.
    - Section III (mid-plane geometry) and Section IV (axial length for net-electric operation) provide chamber_length and plasma_volume derivations.
    - Not directly read for this analysis but foundational for geometric parameter choices.