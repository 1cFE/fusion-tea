# D1+ Analysis: Polywell (D-T)

**Concept**: Polywell (D-T)
**Company**: EMC2 (Energy Matter Conversion Corporation)
**Confinement Family**: Electrostatic (magnetic-cusp electron confinement, electrostatic ion acceleration)
**Analysis Date**: 2026-04-20

---

## Section 1: Availability of Data

**Rating: Limited**

The Polywell has a longer experimental history than most non-mainstream fusion concepts (WB-1 through WB-X, 1989–2013), but the public data is thin in ways that matter most for TEA. Key deficits:

**Published peer-reviewed results:**
- One definitive experimental paper: Park et al. (2015), *Phys. Rev. X*, reporting WB-X high-beta electron confinement with order-of-magnitude enhancement in hard X-ray emission at high beta. This is the strongest public evidence that the Wiffle-Ball confinement enhancement is real, but it does not demonstrate fusion.
- WB-6 fusion result (~10⁹ D-D neutrons/s at 12.5 kV) was reported by Bussard in conference talks (2006) but was never independently published in peer-reviewed form [1].

**Theoretical reactor scaling study:**
- Park et al. (2025), arXiv:2508.06761, "Polywell Revisited" — the only reactor-scale design study. This is a physics-scaling paper, not an engineering design. It provides quantitative design parameters (1.6 m cube, 4.5 T, Q~10.5) but explicitly acknowledges key unknowns as free parameters [2].

**No published:**
- Plant engineering design with cost breakdown
- Power balance calculations with specific energy conversion system
- Independent economic analysis
- Any results from WB-8 (2009–2012) or subsequent work in peer-reviewed literature

**Company transparency:** Low. EMC2 has published two peer-reviewed papers since 2015, one reactor scaling preprint (arXiv), and minimal website content. Current activities pivot to the FPNS (Fusion Prototypic Neutron Source) program in partnership with SHINE Technologies [3]. No current device status, experimental parameters, or engineering progress is publicly reported.

**Phase 1a dossier completeness:** Good coverage of differentiation column values based on available sources. Key gaps (tritium breeding design, energy capture specifics, coil type for reactor) reflect genuine EMC2 non-disclosure, not research insufficiency.

**Data gaps limiting this analysis:**
- No energy conversion architecture: the 80% neutron energy fraction has no specified extraction pathway
- No independent critique of the Park 2025 scaling model in the published literature
- No published results from the most recent EMC2 device series (post-WB-8)

---
[1] polywell-technical-details.md §WB-6: "the result was roughly 100,000 times greater than what Farnsworth achieved at similar well depth and drive conditions"
[2] polywell-revisited-2025-park.md §Scaling for Net Energy: "currently, we lack a quantitative model for the reduction in the loss rate. Therefore, we will use a parametric expression"
[3] thefusionreport-p-interview-with-emc2-fusion-a-different.md §Next Steps for EMC2 Fusion: "EMC2 is pursuing the Fusion Prototypic Neutron Source (FPNS) program in partnership with SHINE Technologies"

---

## Section 2: Challenges in Capturing System Function

The Polywell presents unusual LCOE modeling challenges because the critical physics uncertainty (electron confinement at high beta) propagates directly into the Q value, which in turn drives every cost ratio. Unlike a tokamak, where Q is constrained by transport scaling laws benchmarked against decades of data, the Polywell Q in the Park 2025 study is a function of a single unvalidated free parameter.

**LCOE sensitivity ranking**: Three parameters dominate the Polywell LCOE corridor in descending order of leverage: **(1) γ / Q_plasma** — the master parameter; a 2× change in γ changes beam input power by 2× and swings modeled LCOE by ±10+ ¢/kWh; **(2) thermal efficiency** — second-order but blocks net output calculations (±2 ¢/kWh range across plausible 35–45% cycle assumptions); **(3) capital cost of the SC coil and e-beam systems** — reducible through engineering study, minor in comparison (±1 ¢/kWh with aggressive overrides). Bremsstrahlung (item 3) and O&M (item 6) are physically important but have far lower LCOE leverage than these three. Cost model sensitivity analysis should prioritize this ordering.

**1. The loss reduction factor γ — the master parameter (blocking)**

The entire Park 2025 reactor design hinges on γ = 0.1, described as "a parametric expression to represent the reduction in the energy loss rate" from potential-well formation. The authors acknowledge: *"currently, we lack a quantitative model for the reduction in the loss rate"* [1]. Sensitivity: γ = 0.05 requires only 39 MW input; γ = 0.2 requires 156 MW input for the same 980 MW fusion power — a 4× swing in recirculating power fraction. At γ = 0.2, Q_plasma ≈ 6.3 rather than 10.5; engineering Q (accounting for conversion efficiency and electron beam power supply efficiency) could fall below breakeven. The 2019 University of Sydney experiments found *"little or no trace of virtual electrode formation"* at higher plasma densities, and calculated that electron supply rates of 200,000 A would be required to sustain a virtual cathode at commercial plasma densities [2]. EMC2 disputes this but has not published counter-experimental evidence. A cost model cannot be anchored to Park 2025's performance projections without a validated γ.

**2. No energy conversion architecture (blocking)**

D-T fusion deposits ~80% of its energy (14.1 MeV) in neutrons. For a 980 MW fusion reactor, approximately 784 MW flows as neutrons into an unspecified blanket. Park 2025 mentions *"naturally diverging magnetic fields at plasma-facing surfaces"* for thermal management but specifies no blanket type, no thermal cycle (Rankine, sCO2, or other), and no coolant [3]. Gross electric output, recirculating power, and net electrical output are all unknown. Without this, no LCOE estimate can be constructed at any confidence level.

**3. Bremsstrahlung radiation loss balance**

For non-Maxwellian (non-thermal) plasmas, Rider (1995) calculated that bremsstrahlung X-ray losses exceed fusion power output by at least 20%. Bussard argued this doesn't apply to the Polywell's non-equilibrium ion distribution. Park 2025 assumes *"sufficiently fast thermalization time scale for a high-density cusp plasma equilibrium"* [4] — i.e., it assumes the plasma thermalizes, which changes the Rider calculation but also means the ion distribution is Maxwellian at 20 keV, not the monoenergetic beams Bussard envisioned. This theoretical tension (thermalized plasma loses the direct-conversion advantage; non-thermal plasma faces Rider radiation losses) is not resolved in any public source.

**4. Tritium breeding under polyhedral coil geometry (blocking)**

Park 2025 explicitly identifies the coil geometry as a challenge: *"tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures"* [5]. The six coil faces subtend a large solid angle from the plasma center, shadowing neutrons from the blanket in those directions. No TBR calculation, no blanket geometry, and no material selection is provided. A standard liquid-Li or LiPb blanket design from a MFE concept cannot be adapted without a neutronics study specific to the polyhedral geometry.

**5. Physics scaling extrapolation across three orders of magnitude in power**

WB-X (coil diameter ~13.8 cm, sub-microsecond pulses) → FPNS target (~17–20 cm coil diameter, 350 kW fusion, steady-state) → reactor design (coil diameter ~160 cm, 980 MW fusion). The linear scale-up from WB-X to reactor is ~12×; power scale-up is ~10⁶×. The Park 2025 paper derives scaling laws from PIC simulations and WB-X/WB-8 data, but acknowledges the gyroradius scaling exponent is *"preliminary"* and requires *"future experiments and/or simulations"* [6]. Standard fusion concept cost models assume validated physics scaling; here the scaling model itself is speculative.

**6. O&M structure: unknown**

No published source addresses maintenance strategy, plasma-facing component (PFC) lifetime under 14 MeV neutron bombardment, or scheduled vs. unplanned outage costs. The compact polyhedral geometry may simplify modular replacement (Park 2025 emphasizes "easily assembled and disassembled in a modular manner"), but this is a design claim, not a demonstrated maintenance strategy. A placeholder O&M section is required for any LCOE model — no data exists to populate it.

---
[1] polywell-revisited-2025-park.md §Scaling for Net Energy: "currently, we lack a quantitative model for the reduction in the loss rate"
[2] en-wiki-polywell.md §University of Sydney experiments: "it was calculated that new electrons would have to be supplied at an unfeasible rate of 200,000 amps"
[3] polywell-revisited-2025-park.md §Discussion: "naturally diverging magnetic fields at plasma-facing surfaces"
[4] polywell-revisited-2025-park.md §Scaling Assumptions: "sufficiently fast thermalization time scale for a high-density cusp plasma equilibrium"
[5] polywell-revisited-2025-park.md §Discussion: "tritium breeding blankets can operate in regions of low magnetic field strength"
[6] polywell-revisited-2025-park.md §Cusp Loss Scaling: "Note that the r_i² is much larger than r_hybrid² by a factor of 60.6 for deuterium ions, a significant factor that needs to be validated"

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

---

**Tritium Breeding Blanket — TRL 1**

- **Demonstrated**: Nothing. No Polywell-specific neutronics study has been published. No blanket material or geometry has been proposed by EMC2.
- **On paper only**: Park 2025 identifies the problem (coil neutron shadowing) and characterizes it as an opportunity for *"innovative breeding solutions"* — but offers no design.
- **Missing at scale**: Everything. A polyhedral-cusp neutron source creates six "shadowed" sectors aligned with the coil faces. Achieving TBR > 1.1 (standard requirement) in this geometry requires a dedicated neutronics analysis that has not been done. Whichever blanket concept is chosen (liquid-Li flowing, LiPb, FLiBe, solid ceramic), the geometry will require concept-specific engineering. There is no off-the-shelf MFE blanket design that can be dropped in.

---

**Energy Conversion / Balance of Plant — TRL 1–2**

- **Demonstrated**: Nothing specific to Polywell. General steam Rankine and sCO2 thermal cycles are industrially mature (TRL 9), but the Polywell has produced no engineering specification connecting its fusion power output to a thermal circuit.
- **On paper only**: Park 2025 mentions *"effective thermal management of plasma exhaust"* and notes that neutrons will be captured in a blanket. No cycle type, coolant, or thermodynamic parameters are given.
- **Missing at scale**: Any plant-scale specification for the following chain: neutron-to-blanket heating → primary coolant loop → power conversion cycle → generator. For 980 MW fusion at ~40% thermal efficiency (analogue), gross electric output would be ~390 MWe, minus recirculating power for 78 MW electron beam injection (plus beam power supply efficiency losses). Net output is unknown within ~±50%.

---

**High-Beta Cusp Confinement at Reactor-Relevant Parameters — TRL 3**

- **Demonstrated**: WB-X (2013, published Phys. Rev. X 2015) demonstrated that at high beta (β ~ 1), hard X-ray emission increased by approximately an order of magnitude relative to low-beta operation, confirming the Wiffle-Ball confinement enhancement at 13.8 cm coil scale with sub-microsecond pulses [1]. This is a genuine physics result. WB-8 (2010–2012) demonstrated over 500 high-power plasma shots with 0.8 T field.
- **On paper only**: Park 2025 scaling model projects that high-beta confinement at 4.5 T boundary field and 20 keV ion temperature yields Q = 10.5. The scaling laws assume the loss reduction factor observed at low beta generalizes to reactor conditions.
- **Missing at scale**: Sustained (not pulsed) high-beta confinement. All WB experiments ran pulsed (resistive coil heating limited pulses to sub-millisecond to ~100 ms). No high-beta result at D-T fusion temperatures. No fusion yield at high-beta conditions (all WB-X results showed confinement enhancement, but device did not produce fusion during these tests). Crucially: validation of γ = 0.1 at any scale.

> "Experiments conducted at varying cusp magnetic field strengths showed that both too low and too high magnetic fields reduce confinement, indicating the existence of an optimal β value, β ~1"
> — polywell-revisited-2025-park.md §WB-X Results

---

**Superconducting Coil System for 6-Sided Cusp Geometry — TRL 3–4**

- **Demonstrated**: All WB-series devices used resistive copper coils. EMC2 reportedly began SC Polywell development in 2012 but no results were published [2]. The 4.5 T boundary field in Park 2025 implies steady-state superconducting coils — resistive coils would require impractical continuous cooling.
- **On paper only**: The non-interlocking cubic coil geometry has been described as a manufacturing advantage ("compact, non-interlocking coils that can be easily assembled and disassembled in a modular manner" [3]), but no SC coil design with specified wire type, operating temperature, or mechanical support structure has been published.
- **Missing at scale**: SC coil design for 6-sided polyhedral geometry with coil-face independence (no shared load-bearing structure between adjacent coils). Standard HTS tokamak coil knowledge (REBCO, CICC) does not transfer directly. At 4.5 T with REBCO tape, the coil technology is feasible in principle (Nb3Sn handles this comfortably), but the geometry and mechanical loading under high-beta plasma pressure require concept-specific engineering.

---

**MW-Class Electron Beam Injection System — TRL 5–6**

- **Demonstrated**: Commercial electron beam systems at hundreds of kW to MW scale are available for industrial applications (vacuum metallurgy, materials processing, medical). Park 2025 confirms: *"commercial-grade MW-class electron beam injectors are available that can provide sufficient power to produce and sustain a potential well"* [4].
- **On paper only**: The specific requirement (60 keV, 1.3 kA, CW operation, injected into a magnetized cusp geometry) has not been demonstrated as an integrated system. WB-series experiments used plasma guns and emitters; the reactor-scale electron beam injection geometry is different.
- **Missing at scale**: Steady-state reliability of 78 MW total beam injection (multiple beams) into a magnetic cusp, beam-plasma coupling efficiency at reactor plasma densities, and long-term beam component lifetime under neutron and X-ray fluence. The technology is commercially sourced (a cost advantage) but requires integration engineering.

---

**Vacuum Vessel and Basic Structure — TRL 7+**

- **Demonstrated**: A ~1.6 m cube vacuum vessel is straightforward industrial engineering. No novel materials, activation-resistant alloys, or ultra-high-vacuum coatings are required beyond standard fusion practice.
- **Missing at scale**: Integration with blanket modules (once designed), remote maintenance access for coil replacement, and neutron shielding for external systems — but these are design challenges, not technology development.

---

**Tritium Fuel Cycle — TRL 4–5 (analogue)**

The tritium handling, processing, storage, and injection systems for Polywell are conceptually identical to any D-T fusion device. Park 2025 references D-T fuel (50:50 mixture, 20 keV); the FPNS facility design includes *"supporting systems such as tritium handling"* [5]. No Polywell-specific tritium challenges beyond the universal D-T issues (limited global supply, tritium permeation, handling costs) have been identified — except the unresolved breeding blanket geometry.

---
[1] polywell-revisited-2025-park.md §WB-X Results: "hard x-ray emission increased by an order of magnitude"
[2] en-wiki-polywell.md §WB-8: "EMC2 reportedly began superconducting Polywell work in 2012"
[3] polywell-revisited-2025-park.md §Discussion: "compact, non-interlocking coils that can be easily assembled and disassembled"
[4] polywell-revisited-2025-park.md §Discussion: "commercial-grade MW-class electron beam injectors are available"
[5] emc2-fpns-talk-polywell-2023.md §Task 8: "Design FPNS facility, including supporting systems such as tritium handling, shielding, etc."

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium**

Same supply chain constraints as any D-T fusion concept. Current global tritium inventory is ~25 kg, held primarily by CANDU operators. A reactor producing ~980 MW fusion power requires approximately 55 kg/year of tritium fuel (at ~55% burnup fraction and modest wall recycling), which exceeds current global supply by a factor of ~2. This makes on-site tritium breeding from a lithium blanket mandatory — but as noted in Section 3, no blanket design exists for the Polywell. There is no novel Polywell-specific tritium risk beyond the universal D-T supply constraint; the geometry-specific blanket design challenge is the real risk.

**Coil Conductors**

All demonstrated WB-series coils used resistive copper. For a reactor (4.5 T steady-state at 80 cm coil scale), superconducting conductors are essentially required. The coil material type is unspecified by EMC2. Likely candidates:
- REBCO (HTS, ~4.2–77 K): suitable for 4.5 T; emerging supply chain from CFETR/SPARC/tokamak programs; km-scale production ramping but limited
- Nb3Sn (LTS, 4.2 K): mature supply chain; adequate for 4.5 T; commercially produced by multiple vendors

The non-interlocking polyhedral geometry requires six independent coil assemblies. Unlike a tokamak's toroidal field coils (one continuous set of forces in-plane), Polywell coils experience the full magnetic pressure asymmetrically. Custom coil forms will be needed regardless of conductor choice. No dedicated Polywell conductor procurement or manufacturing study exists.

**Blanket and Structural Materials**

No blanket material has been specified. If a liquid-Li or LiPb blanket is eventually adopted (following MFE convention), the material supply chain is standard and not concept-limiting. Li-6 enrichment would be required if a natural lithium blanket is insufficient for TBR > 1.1 — this is a shared constraint with all D-T MFE concepts but is noted here because the Polywell's coil-shadowing geometry may require higher enrichment or thicker blankets to compensate.

**Electron Beam Sources**

Park 2025 confirms commercial availability of MW-class electron beam systems. These sources are manufactured by Leybold, Sciaky, and Ferrotec, among others, for materials processing applications. At 78 MW total injection (multiple beams), beam supply cost and electrical efficiency of the beam power supplies are LCOE-relevant. No costing data for this application is available in public sources.

**Vacuum Pumping**

A 1.6 m cube device running D-T at 20 keV requires turbomolecular and cryogenic vacuum pumping similar to mid-scale MFE experiments. Tritium-compatible pumping (without tritium contamination of pump oil) is mature industrial practice. No supply chain constraint.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion power (theoretical) | ~980 MW | polywell-revisited-2025-park.md §Scaling for Net Energy | low | Depends on γ=0.1; if γ=0.2, Q≈6.3 |
| Electron beam input power | 78 MW (γ=0.1) / 156 MW (γ=0.2) | polywell-revisited-2025-park.md §Scaling for Net Energy | low | Dominant recirculating load |
| Plasma gain Q_plasma | ~10.5 | polywell-revisited-2025-park.md §Scaling for Net Energy | low | Free parameter γ=0.1 assumed |
| Reactor device size | 1.6 m cube side | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | Geometric design point |
| Plasma volume | ~4.1 m³ | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | Inferred from 1.6 m cube |
| Boundary magnetic field | 4.5 T | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | Specified design value |
| Ion temperature | 20 keV | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | D-T design point |
| Electron beam energy | 60 keV | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | Specified injection energy |
| Electron beam current | 1.3 kA | polywell-revisited-2025-park.md §Scaling for Net Energy | medium | Specified injection current |
| D-T fuel mix | 50:50 | polywell-revisited-2025-park.md §Scaling for Net Energy | high | Explicitly specified |
| FPNS fusion power | 350 kW steady-state | emc2-fpns-talk-polywell-2023.md §Specifications | medium | Near-term demonstration milestone |
| FPNS ion beam power | 5–6 MW | emc2-fpns-talk-polywell-2023.md §Specifications | medium | Input power for FPNS |
| FPNS boundary field | 2–3 T | emc2-fpns-talk-polywell-2023.md §Specifications | medium | Lower than reactor design |
| FPNS plasma target | 500 eV | emc2-fpns-talk-polywell-2023.md §Specifications | medium | FPNS not at fusion temps |
| FPNS R&D cost (Phase 1) | $20M / 24 months | emc2-fpns-talk-polywell-2023.md §Cost | medium | Program development budget only |
| WB-6 D-D fusion rate | ~10⁹ n/s | polywell-technical-details.md §WB-6 | medium | At 12.5 kV drive, 5 tests only |
| Net electric output (approx.) | ~310–390 MWe | [inferred: 980 MW × 40% thermal efficiency − 78–156 MW recirculating; thermal efficiency analogue from steam Rankine cycle; beam power from Park 2025] | very low | Blocking uncertainties on every component |
| Engineering Q_eng (approx.) | ~2–4 | [inferred: gross electric ~390 MWe / recirculating ~78–156 MW × beam supply efficiency ~80%; wide range reflects γ uncertainty] | very low | Plausible if physics holds |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Validated Q value (γ experimentally confirmed) | truly-unknown | blocking | Core LCOE lever; no experimental basis |
| Net electrical output | truly-unknown | blocking | No energy conversion system designed |
| Thermal efficiency | truly-unknown | blocking | No thermal cycle specified |
| Recirculating power fraction | derivable | blocking | Requires energy conversion design first |
| Total overnight capital cost | truly-unknown | blocking | No plant study or cost model exists |
| Capital cost by CAS category | truly-unknown | blocking | No engineering design |
| Capacity factor | truly-unknown | blocking | No maintenance or operational design |
| TBR (tritium breeding ratio) | truly-unknown | blocking | No blanket design |
| Fixed O&M costs | truly-unknown | important | No plant design or staffing model |
| Variable O&M costs | truly-unknown | important | PFC lifetime, coil replacement schedule unknown |
| Blanket thermal output fraction | truly-unknown | important | Depends on coil-shadow geometry |
| Power supply efficiency for beams | not-yet-sourced | important | Affects recirculating power; industrial data available |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Loss reduction factor γ — no experimental validation for γ=0.1; entire Q projection depends on this free parameter | S2, S5 | truly-unknown | blocking | Next-generation experiment at FPNS scale or above with high-beta conditions; Park et al. explicitly flag this |
| 2 | Virtual cathode formation at commercial plasma densities — Univ. Sydney 2019 found no evidence; EMC2 disputes but has not published counter-data | S2, S3 | truly-unknown | blocking | Independent experiment at n~10²¹ m⁻³; EMC2 internal data likely exists but not disclosed |
| 3 | Energy conversion architecture — no thermal cycle, blanket coolant, or BOP design; 80% of fusion energy in neutrons with no extraction path specified | S3, S5 | truly-unknown | blocking | EMC2 engineering design study; could not exist publicly yet |
| 4 | Net electrical output and recirculating power fraction | S5 | derivable | blocking | Requires energy conversion design (gap #3) |
| 5 | Tritium breeding blanket design — coil neutron shadowing creates geometry-specific challenge with no proposed solution | S3, S4, S5 | truly-unknown | blocking | Neutronics analysis for polyhedral cusp geometry; no public study identified |
| 6 | Capital cost breakdown by CAS category | S5 | truly-unknown | blocking | No plant engineering study; analogue borrowing from MFE concepts is the only current option |
| 7 | Bremsstrahlung radiation balance for Park 2025's assumed thermalized plasma — Rider 1995 critique partially addressed by thermalization assumption but not fully resolved | S2 | truly-unknown | important | First-principles bremsstrahlung calculation for 20 keV Maxwellian D-T plasma at reactor density |
| 8 | SC coil design for 6-sided cusp geometry — conductor type, operating temperature, mechanical support unspecified | S3, S4 | proprietary | important | EMC2 reportedly began SC work 2012; no published results |
| 9 | Capacity factor and maintenance strategy — modular coil advantage claimed but no quantitative maintenance plan | S5 | truly-unknown | important | Would require plant design; placeholder ~80% from MFE analogue for modeling |
| 10 | Fixed and variable O&M costs | S3, S5 | truly-unknown | important | No plant operational design; placeholder from MFE D-T analogue required |
| 11 | Beam power supply efficiency at 78 MW scale — affects recirculating power fraction | S5 | not-yet-sourced | important | Industrial electron beam supplier data; ~80–90% power supply efficiency is reasonable starting point |
| 12 | Scaling law validation — hybrid gyroradius exponent and cusp loss scaling unverified at mass ratio 3672 (D-T) | S2, S3 | truly-unknown | important | Park 2025 flags explicitly; requires multi-species experiment |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available for cross-referencing is **21-spherical-tokamak-hts** (Tokamak Energy). The Polywell and spherical tokamak share essentially no subsystems, cost structures, or physics mechanisms. The spherical tokamak analysis provides no directly reusable assumptions for Polywell modeling.

**Concept family positioning:**

The Polywell belongs to the Electrostatic confinement family (schema §Column 1: `Electrostatic`). Within the full concept landscape, the nearest conceptual neighbors are:
- **13-electrostatic-hybrid (Avalanche Energy)**: E×B electron confinement with electrostatic ion acceleration — shares the principle of using electron trapping to build an electrostatic well for ions. Avalanche uses resistive wall + electrostatic cathode rather than magnetic cusp; similar Q-prediction uncertainty; not yet approved for full cross-reference.
- **IEC/Fusor concepts**: The Polywell's direct ancestor. Distinguished by replacing the physical grid cathode with a magnetic cusp, eliminating grid losses — but the same fundamental question (can electron confinement time be long enough for net energy?) applies.

**Divergence from MFE mainstream:**

The Polywell is conceptually distant from all MFE tokamak/stellarator concepts in the following ways relevant to TEA:

1. **Magnet sizing**: MFE magnets must confine 20 keV ions at billion-particle densities, requiring >5–20 T fields over large plasma volumes. Polywell magnets only confine electrons at much lower energy densities — in principle, a far smaller and cheaper magnet system. Park 2025 notes *"the magnetic energy density required to confine electrons is far smaller than that required to directly confine ions"* [1]. This is the primary claimed cost advantage.

2. **No divertor**: Unlike tokamaks, which require a complex plasma-exhaust handling system (divertor), the Polywell's cusp geometry naturally provides plasma exhaust outlets at the cusp points. This eliminates a major MFE cost item (divertor design, replacement, remote handling).

3. **No burning plasma**: The Polywell is not designed around a self-sustaining burn. The electrostatic well continuously injects energy (78 MW electron beam) to maintain ion acceleration. Alpha particle heating is incidental, not the primary confinement mechanism. This changes the physics of the self-Q calculation versus a burning-plasma MFE concept. **Cost implication (penalty):** Because the e-beam must run continuously at full power, the recirculating power fraction is structural — approximately 29% at baseline γ=0.1 (78 MW beam / 267 MW gross electric at 40% efficiency × 980 MW fusion) and 40–45%+ at γ=0.2. A burning-plasma MFE concept (tokamak, stellarator) recirculates only 10–20% for heating and housekeeping once ignited. This structural penalty is permanent and compounds the γ uncertainty: doubling γ doubles beam power, directly halving Q_eng, and γ is the primary lever on both net output and LCOE simultaneously.

4. **Modular assembly**: The six non-interlocking coils each face one side of the cube. Park 2025 claims this enables straightforward manufacturing and maintenance — a contrast to the interlocked TF coils of tokamaks that require fully remote maintenance.

**Modeling approach:** CAS-structured (1costingfe) modeling is appropriate for the Polywell, not free-form. The concept shares the standard D-T plant BOP structure (buildings, turbine island, tritium handling, cooling towers) with all MFE concepts — those CAS accounts can be borrowed directly with plausible analogues. Concept-specific cost differences concentrate in two CAS22 line items: the SC coil system (six independent polyhedral coils replacing TF/PF coil set) and the e-beam injection system (replacing H&CD system). Both are handled via direct CAS22 overrides without restructuring the cost model. Free-form modeling would not improve accuracy given the current data availability level and would lose the cross-concept comparability the project requires.

**Shared baseline assumptions for placeholder LCOE modeling:**

Where concept-specific data is absent, the following analogues from MFE D-T concepts are defensible for a first-pass model:
- Thermal cycle efficiency: 40% (steam Rankine) as a baseline; sCO2 at 45% as an optimistic scenario [analogue: MFE D-T standard]
- Fixed O&M: ~2–3% of overnight capital cost per year [analogue: MFE D-T standard]
- Tritium handling cost: standard fusion D-T assumptions
- Capacity factor: 80% [analogue: MFE D-T aspirational; no Polywell-specific reason to diverge]

These are `[analogue]` values and should be flagged as such in any LCOE model built from this analysis.

---
[1] polywell-technical-details.md §Cost vs. Tokamaks: "the magnetic energy density required to confine electrons is far smaller than that required to directly confine ions, as is done in other fusion projects such as ITER"

---

## Section 8: Sources

1. **Park, J. et al., "Polywell Revisited," arXiv:2508.06761 (submitted August 2025)**
   The only reactor scaling study. Provides all quantitative design parameters for the D-T concept: 1.6 m cube, 4.5 T boundary field, 20 keV plasma, ~980 MW fusion power, 78 MW electron beam injection, Q=10.5. Also the primary source for key uncertainties: γ free parameter, scaling law limitations, tritium breeding challenge identification.
   Saved: `knowledge/concept_research/27-polywell/iter-02/sources/polywell-revisited-2025-park.md` (full text, 89 KB); abstract at `iter-03/sources/arxiv-2508-06761.md`

2. **Park, J. et al., "High-Energy Electron Confinement in a Magnetic Cusp Configuration," *Phys. Rev. X* 5, 021024 (2015)**
   Only published peer-reviewed experimental result from EMC2. Demonstrates WB-X high-beta confinement enhancement (order-of-magnitude increase in hard X-ray emission at β~1). The foundational experimental evidence for the Wiffle-Ball confinement mechanism. Referenced throughout via Wikipedia sources.
   Not directly saved as extracted source; referenced in `polywell-technical-details.md` and `polywell-revisited-2025-park.md`

3. **Wikipedia, "Polywell," retrieved 2025–2026 (two extracted versions)**
   Comprehensive technical history of EMC2 experiments (WB-1 through WB-8), operating principle, criticisms (Rider 1995, Nevins), and University of Sydney 2019 negative results. Provides the only public documentation of Fusion One Corporation's negative Phase 2 findings and the virtual cathode formation doubts.
   Saved: `knowledge/concept_research/27-polywell/iter-01/sources/polywell-technical-details.md` (109 KB); `iter-03/sources/en-wiki-polywell.md` (109 KB)

4. **EMC2 / SHINE Technologies, FPNS Program Proposal (FPA 2023 context)**
   Near-term demonstration device parameters: 350 kW fusion, 5–6 MW ion beam input, 2–3 T boundary field, 8.5–10 cm plasma radius. $20M/24-month R&D cost estimate. Key source for current EMC2 development roadmap.
   Saved: `knowledge/concept_research/27-polywell/iter-02/sources/emc2-fpns-talk-polywell-2023.md` (2 KB)

5. **TheFusionReport, "Interview with EMC2 Fusion: A Different Approach," 2025**
   Current company strategy: FPNS neutron source as near-term revenue to fund power reactor development. Compactness and cost advantage narrative. WB formation pulse power threshold (700 MW). ~2 m coil diameter claimed to yield ~100 MW fusion.
   Saved: `knowledge/concept_research/27-polywell/iter-03/sources/thefusionreport-p-interview-with-emc2-fusion-a-different.md` (8 KB)

6. **EMC2 Fusion website summary**
   Minimal corporate overview. Confirms EMC2's position that prior negative academic results are contested. No technical specifications.
   Saved: `knowledge/concept_research/27-polywell/iter-01/sources/emc2-website-summary.md` (1 KB)

7. **Polywell Phase 1a dossier (internal)**
   Research synthesis from two prior iterations. Provides differentiation table values with citations and confidence ratings. Key context: per-column rationale for Fuel=D-T, Operation Mode=Steady-state, Tritium Breeding=TBD.
   Path: `knowledge/concept_research/27-polywell/dossier.md`
