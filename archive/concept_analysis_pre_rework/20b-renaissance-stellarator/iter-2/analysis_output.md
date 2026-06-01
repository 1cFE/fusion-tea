# D1+ Analysis: Compact Liquid-Wall HTS Stellarator (Renaissance Fusion)

**Concept**: Compact Liquid-Wall HTS Stellarator — D-T fuel
**Company**: Renaissance Fusion (Grenoble, France)
**Confinement Family**: MFE — Stellarator (modular)

---

## Section 1: Availability of Data

**Rating: Moderate**

Renaissance Fusion has published three peer-reviewed papers in high-quality journals that collectively define the physics design point, the integrated blanket/neutron management system, and the power conversion cycle. This is unusually rigorous public disclosure for a private fusion startup at this stage, and it provides a solid technical foundation. However, no economic analysis, capital cost estimate, system code study (PROCESS, ARIES-equivalent), or plant costing breakdown has been published. The "Moderate" rating reflects strong technical data on subsystem performance, but zero published economic data and no complete plant-level system model.

**Published primary sources:**

*Nuclear Fusion 64 (2024) 026007* is the core design paper: it establishes the machine geometry (R ≤ 4 m, A ≈ 4), the laser-patterned HTS REBCO magnet approach (B = 10 T nominal, up to 15 T at coil), the plasma design point (D-T at 10 keV, Q = ∞), and the startup heating system (NNBI with 60% neutralization efficiency). The paper explicitly performs an economic optimization of the design point — the cost-optimal major radius and machine scale are derived — but does not disclose the absolute cost result. This is the most directly useful single source for TEA and distinguishes Renaissance Fusion from private companies that have released no technical documentation at all.

> "The design point has been economically optimized for 1 GWe output at major radius ≤4 m with aspect ratio ~4"
> — paraphrased from dossier.md, §Summary (citing Nuclear Fusion 64 (2024) 026007)

*Journal of Nuclear Materials 599 (2024) 155239* characterizes the integrated liquid Li-LiH first wall and blanket: radial build (15 cm Pb + 18 cm Li-LiH), maximum wall loading capability (25 MW/m²), neutron energy multiplication factor (fm = 1.24), neutron energy absorption (99.99%), and outer shielding structure (50 cm VH₂ + 1.3 m concrete bioshield). This paper defines the first-wall architecture that is central to the concept's TEA distinctiveness.

*Energy Conversion and Management 276 (2023) 116572* (Fama et al.) documents the sCO₂ Brayton-Rankine combined cycle optimized via genetic algorithm for this design: 49–51% thermal cycle efficiency, yielding 34% net plant efficiency at the 1 GWe design point. This is the source for all power conversion parameters.

**Additional public materials:**

The Renaissance Fusion technology page (renfusion.eu/technology) confirms the laser-patterning approach, liquid metal wall, steady-state operation with "near-100% duty cycle," and ignited design target. A UC Berkeley seminar ("High-field HTS stellarators with liquid metal walls") and an MT29 abstract (2024) provide additional context on the magnet fabrication approach and the hardware demonstration milestone: a 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K. The MT29 milestone is the only hardware result in the public record.

**Independent analyses:**

No independent third-party assessment of the Renaissance Fusion design exists in the public literature. There is no ARIES-equivalent study, no PROCESS run for this geometry, and no academic group has published a techno-economic analysis of the laser-patterned stellarator concept. The ARIES-CS study (quasi-isodynamic compact stellarator) provides a partial geometry analogy but does not address the laser-patterning approach or liquid metal wall architecture.

**Phase 1a dossier completeness:**

The dossier achieved high confidence across all differentiation taxonomy columns. The full JNM blanket paper (J. Nuclear Materials 599 (2024) 155239) confirms TBR = 1.60 for the optimized blanket configuration (10 cm Pb pebbles + 22 cm non-enriched Li-LiH), against a design requirement of TBR ≥ 1.15. This margin of ~39% above the design threshold is intended to cover port coverage losses and fuel cycle inefficiencies in the 3D geometry. The original dossier correctly cited TBR ≈ 1.60, but had a secondary inconsistency: a "neutron energy multiplication factor (fm) = 1.24" that the full paper does not verify — the JNM paper reports the blanket energy multiplication factor as 1.07. The 1.24 figure is not reproducible from the available source and should not be carried into the TEA parameter set. The TBR gap is now resolved; the fm labeling has been corrected (see Section 5).

**Key data gaps limiting this analysis:**

1. No capital cost estimate, LCOE model, or CAS-level cost breakdown has been published
2. TBR = 1.60 is confirmed (JNM 599 §Case study); blanket energy multiplication factor = 1.07 (corrected from dossier's unverified 1.24 figure)
3. No plasma confinement time, density, or bootstrap fraction published
4. Liquid metal circulation pump power not disclosed — drives unexplained gap between cycle efficiency (50%) and net efficiency (34%)
5. No divertor design or plasma exhaust solution has been addressed in any source
6. The demonstrated magnet (6 T, Helmholtz) is at 60% of nominal design field and does not characterize manufacturing cost or throughput

---

## Section 2: Challenges in Capturing System Function

Challenges are ranked by LCOE impact.

**1. Entirely unanchored economics — no cost model starting point (Impact: Critical)**

Unlike CFS (Sorbom et al. 2015 plant study), ARIES-CS (complete cost breakdown), or any other stellarator concept with an analogue study, Renaissance Fusion has published zero economic data. The Nuclear Fusion design paper notes the design point was "economically optimized" but reports only relative results (cost-optimal radius), not the absolute cost. Every CAS account — from laser-patterned magnets through liquid metal wall through sCO₂ balance of plant — must be constructed from first principles with no company anchor point. This is the broadest costing uncertainty in the MFE stellarator family.

**2. Laser-patterned HTS film: no manufacturing cost analogue exists (Impact: Critical)**

The laser-patterning approach — REBCO film deposited on ~1 m diameter cylindrical surfaces, current paths defined by laser ablation — eliminates traditional coil winding but substitutes a cost structure with no published industrial analogue. For a wound-tape design, the coil cost is approximable as tape length × $/kA-m. For laser-patterned film, the cost drivers are:
- REBCO thin-film deposition throughput and uniformity at 1 m cylinder scale
- Laser patterning throughput, kerf/waste rates, and re-work protocols
- Substrate (cylinder) fabrication and qualification
- Quench detection and protection for distributed thin-film superconductor (very different from wound tape, where quench propagation and protection are well-characterized)

None of these cost drivers has a published analogue at relevant scale. The 6 T Helmholtz demonstration validates that the physics concept works, but does not characterize production economics. This is the single largest manufacturing cost uncertainty in this survey.

**3. Ignited stellarator plasma (Q = ∞): extrapolation with no intermediate steps (Impact: High)**

No stellarator has operated near burning plasma conditions. The gap between the best demonstrated stellarator performance (W7-X: plasma temperatures of a few keV at low density, no significant fusion reactions) and the Renaissance Fusion target (ignited 10 keV D-T plasma in a compact A ≈ 4 geometry at 10 T) is enormous. Unlike tokamaks, where TFTR, JET, and JT-60SA provide stepping stones and ITER is a validated pathway to burning plasma, there is no experimental stellarator program that provides an intermediate data point for Q >> 1. The compact aspect ratio (A ≈ 4) puts this design in a parameter space with no stellarator experimental precedent — the confinement quality of a compact QI geometry at 10 T has not been tested. This physics extrapolation propagates into large uncertainty in the capital cost model: if confinement underperforms, the machine must grow, driving cost upward nonlinearly.

**4. Liquid Li-LiH wall at 25 MW/m²: unprecedented engineering regime (Impact: High)**

The flowing liquid metal wall is the most radical first-wall concept in this survey. At 25 MW/m² continuous wall loading, the Li-LiH system must simultaneously:
- Present a stable plasma-facing free surface without disrupting confinement via MHD interactions
- Circulate at sufficient velocity to limit tritium holdup (tritium solubility in Li is very high — a favorable breeding property but a permeation risk)
- Deliver heat to the sCO₂ heat exchanger at the high temperatures needed to achieve 49–51% cycle efficiency
- Manage the Pb pebble neutron multiplication layer within the flowing liquid system

> "The liquid metal wall serves as integrated first wall, breeder, shield, and coolant — a fundamentally different architecture from contained blanket approaches. Capable of 25 MW/m² wall loading."
> — dossier.md, §Tritium Breeding (citing J. Nuclear Materials 599 (2024) 155239)

No flowing liquid metal wall has been demonstrated at 25 MW/m² in any experimental facility. The MHD behavior of a Li-LiH mixture (as opposed to pure Li or Pb-17Li) in the complex 3D magnetic geometry of a compact stellarator is uncharacterized. For LCOE modeling, the liquid metal circulation system (pumps, heat exchangers, tritium extraction, MHD conditioning piping) is a major capital cost account with essentially no published cost analogue.

**5. The net efficiency gap: unexplained recirculating power (Impact: High)**

The published numbers — 49–51% sCO₂ cycle efficiency and 34% net plant efficiency [ECM 276 (2023) 116572] — imply that roughly 32% of gross electric output is consumed by parasitic loads. For a design targeting Q = ∞ (zero heating power at steady state), this large recirculating fraction requires explanation. The likely contributors are:
- Cryogenic refrigeration for HTS at 20 K (significant at large magnet volume)
- Liquid metal circulation pumps for 25 MW/m² continuous wall loading (likely the dominant load)
- sCO₂ cycle compressors
- Auxiliary systems

None of these loads are itemized in any published source. Without knowing the pump power specifically, the Q_engineering calculation cannot be closed from first principles. This gap makes it impossible to verify the 34% net efficiency number or to perform a recirculating power sensitivity analysis — a key LCOE lever.

**6. sCO₂ combined cycle at 49–51%: not yet demonstrated at GW scale (Impact: Moderate)**

The genetic-algorithm-optimized Brayton-Rankine combined cycle [ECM 276 (2023) 116572] achieves its efficiency by operating at high turbine inlet temperatures enabled by the liquid metal heat source. sCO₂ cycles have been demonstrated at MW scale (Sandia, Echogen) but not at GW scale, and not with the specific inlet temperature profile from a liquid metal fusion heat source. The 49–51% target represents a 15-percentage-point premium over steam Rankine (~34–36%) — a very significant LCOE lever — and should be treated as high-reward/medium-confidence until demonstrated at larger scale.

**7. O&M and maintenance: zero published data (Impact: Moderate)**

No published source addresses maintenance intervals, component replacement schedules, remote handling requirements, or O&M costs. The flowing liquid wall concept may eliminate the discrete solid first-wall replacement cycle that dominates maintenance downtime in solid-blanket designs, but introduces its own maintenance requirements (pump overhauls, heat exchanger fouling, Pb pebble bed management, tritium extraction system maintenance). These are entirely uncharacterized. Per cross-concept memory, O&M absence is a guaranteed finding in first-pass analyses — a placeholder subsection is included here as recommended.

**O&M placeholder**: In the absence of any published data, O&M cost for this concept should be modeled using a two-component framework: (a) fixed O&M ($/year) from scaling to plant size and staffing analogy with ARIES-CS or similar stellarator plant studies; (b) a liquid metal system maintenance adder calibrated against industrial liquid metal handling experience (nuclear Na-cooled fast reactors, fusion breeder blanket R&D). Both components carry very high uncertainty (factor of 2–3×) at this stage.

**Top LCOE sensitivity parameters (from model sensitivity analysis):**

The three engineering parameters with the highest LCOE elasticity for this concept are, in order: (1) **plant availability** (elasticity ≈ −0.94) — a 10% reduction in availability increases LCOE by ~9.4%; (2) **coil cost multiplier** (elasticity ≈ +0.77) — the laser-patterned magnet cost uncertainty dominates capital cost sensitivity, and a 10× spread in coil cost produces an LCOE range spanning hundreds of $/MWh; (3) **construction time** (elasticity ≈ +0.54) — schedule overruns have a larger LCOE impact than thermal efficiency. The sCO₂ cycle efficiency premium (Sections 2.6, 7) is a favorable architectural feature, but thermal efficiency elasticity is only ~0.11 — it is not the dominant LCOE lever. The cost model should be specifically designed to test the coil cost uncertainty range and the achievable capacity factor under liquid-wall maintenance conditions.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**Ignited Stellarator Plasma — TRL 2–3**

- **Demonstrated**: Wendelstein 7-X achieved record stellarator energy confinement times and validated quasi-isodynamic field optimization at A = 10. W7-X plasma temperatures reached a few keV at low density — far from fusion conditions. No stellarator has operated in a burning or even significantly fusion-producing plasma regime. The compact A ≈ 4 geometry is roughly 2.5× lower aspect ratio than W7-X, entering territory without experimental stellarator precedent.
- **On paper only**: QI-optimized equilibrium at R ≤ 4 m, A ≈ 4, B = 10 T with 10 keV D-T design point. Alpha particle confinement at ignition conditions in this compact QI geometry. Stellarator confinement scaling validation at the Renaissance Fusion operating point. Plasma exhaust and divertor solution (not addressed in any published source).
- **Missing at scale**: Any experimental demonstration of Q >> 1 in any stellarator configuration. Confinement quality validation at A ≈ 4 (much less shape freedom for QI optimization than W7-X at A = 10). Stability of plasma-liquid metal interface (the free-surface or confined-film liquid wall must interact with the plasma edge without degrading confinement). Alpha heating dominance in a compact stellarator — depends on alpha confinement quality that has never been experimentally tested.

---

**Laser-Patterned HTS Film on Cylinders (Magnet System) — TRL 3–4**

- **Demonstrated**: A 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K has been built and operated, validating that laser-ablated current paths on REBCO film deposited on a cylindrical substrate can carry superconducting current at useful fields [MT29 Abstract, 2024; dossier.md §Magnet Type]. This is the sole hardware milestone for the magnet program.
- **On paper only**: Scaling the laser-patterning approach to 10–15 T design field (and to the 20–40 T peak coil fields referenced in the Nuclear Fusion design paper [NF 64 (2024) 026007]) across the full toroidal array of cylinders producing a 3D QI stellarator field. Current path optimization for QI confinement quality. Quench detection and protection for distributed thin-film HTS (quench propagation in patterned film is fundamentally different from wound tape — detection and energy extraction strategies are undemonstrated).
- **Missing at scale**: REBCO film deposition uniformity and critical current density (Jc) on 1 m diameter curved substrates at production throughput. Laser patterning precision, repeatability, and repair protocols at nuclear-grade quality. Long-term performance of laser-patterned film under combined cryogenic thermal cycling and 14 MeV neutron irradiation. Manufacturing cost characterization at any scale relevant to a commercial plant. Behavior at peak coil fields of 20–40 T — REBCO Jc degrades sharply above ~20 T at 20 K; achieving 40 T would require either much lower operating temperature or accepting greatly reduced current density, neither of which is addressed in available sources.

---

**Liquid Li-LiH Integrated Wall System — TRL 2–3**

- **Demonstrated**: Liquid metal first-wall concepts (pure Li, Pb-17Li) have been tested at small scale in tokamak environments — the LiMIT limiter on DIII-D, small-scale Li wall experiments on NSTX, and extensive Pb-17Li loop experiments for EU-DEMO. The specific Li-LiH mixture is non-standard (LiH is solid at room temperature, melts at 680°C; the operating mixture must be managed as a high-temperature fluid). The JNM blanket paper [J. Nuclear Materials 599 (2024) 155239] characterizes neutron performance analytically, validating the shielding and breeding geometry.
- **On paper only**: Stable Li-LiH flow at 25 MW/m² plasma-facing wall loading. Tritium extraction from the flowing Li-LiH circuit (tritium solubility in Li is very high — extraction system design is crucial for tritium accountability). Pb pebble integration with flowing liquid metal (pebble retention and fluidization in the flow field). Heat exchanger transferring heat from Li-LiH to sCO₂ without tritium permeation through exchanger walls.
- **Missing at scale**: Any demonstration of a Li-LiH wall at fusion-relevant neutron flux and heat load. MHD flow stability of Li-LiH in complex 3D stellarator geometry under large magnetic field gradients. Tritium permeation rate from liquid Li through structural walls at operating temperature (relevant data exists for pure Li but not Li-LiH mixture). Long-term compatibility of Li-LiH with RAFM structural steels under combined chemical attack, neutron activation, and thermal cycling. Industrial-scale tritium extraction from the liquid Li-LiH circuit at the kg/day rates needed for a 1 GWe plant.

---

**Tritium Fuel Cycle — TRL 3–4**

- **Demonstrated**: Lab-scale tritium handling loops. JET and TFTR operated gram quantities of tritium. The EU Pb-17Li blanket program has demonstrated tritium extraction from lead-lithium in semi-industrial experiments, providing a partial liquid-metal analogy. Tritium's very high solubility in liquid lithium is physically well-understood from fission breeder reactor research.
- **On paper only**: Closed-loop breeding and extraction from Li-LiH at kg/day scale for a 1 GWe plant. Low-permeation heat exchanger design between Li-LiH primary circuit and sCO₂ secondary (tritium permeation through steel heat exchangers from liquid Li is a documented concern). Tritium accounting in a large-volume flowing liquid metal primary circuit. TBR > 1 for the specific Li-LiH + Pb pebble geometry with realistic penetrations (the confirmed quantity is fm = 1.24, not TBR directly).
- **Missing at scale**: Plant-scale tritium processing plant for a liquid Li-based fusion system. Validated demonstration that the JNM blanket design achieves TBR > 1 in prototypical operating conditions. Li-6 enrichment requirements to achieve sufficient TBR with the Li-LiH blanket composition.

---

**sCO₂ Brayton-Rankine Combined Cycle — TRL 4–5**

- **Demonstrated**: sCO₂ Brayton cycles have been demonstrated at 10 MW scale (Sandia National Laboratory, Echogen Power Systems, Southwest Research Institute). Combined Brayton-Rankine architectures are commercially deployed in gas turbine combined cycles. Genetic-algorithm optimization of sCO₂ cycle parameters is published for the Renaissance Fusion design [ECM 276 (2023) 116572].
- **On paper only**: sCO₂ Brayton-Rankine combined cycle at GWe scale from a liquid metal fusion heat source. Tritium-compatible heat exchangers between the primary Li-LiH circuit and sCO₂ secondary working fluid. Operating temperatures enabling 49–51% cycle efficiency (very high turbine inlet temperature required; not specified in available sources).
- **Missing at scale**: Commercial-scale sCO₂ turbomachinery at ~1.5–2 GWe gross output. Integration with tritium-compatible heat exchangers (no demonstrated design). Lifetimes and maintenance intervals for sCO₂ turbomachinery at these temperatures and cycle counts over plant lifetime. Detailed cost data for sCO₂ BOP at GW scale (emerging technology; cost projections vary widely).

---

**NNBI Heating System (Startup Only) — TRL 5–6**

- **Demonstrated**: Negative NBI (NNBI) has been developed extensively for ITER (where 1 MeV negative ion neutral beams are the target). ITER NNBI systems are in late engineering. The 60% neutralization efficiency cited in the design paper [NF 64 (2024) 026007] is within the expected range for ITER-class NNBI based on published experimental data. Positive NBI has been operated at MW scale on many tokamaks and some stellarators.
- **On paper only**: NNBI system geometry for a compact stellarator with A ≈ 4 (beam port access and shine-through fraction in compact geometry). Startup-only operation profile — full NNBI power for ramp-up, then complete shutdown at steady state (unusual duty cycle for NBI systems designed for continuous operation).
- **Missing at scale**: Validated NNBI design for compact stellarator beam access geometry. Long-term reliability of an NNBI system used only for intermittent startups (vs. continuous operation) over plant lifetime. Capital cost characterization for a startup-only NBI system — likely less expensive than a continuous heating system but not dimensioned in available sources.

---

**Cryogenics (HTS at 20 K) — TRL 6–7**

- **Demonstrated**: Large-scale helium refrigeration plants are commercially mature (ITER-scale systems built and tested). Operating at 20 K (as opposed to 4 K for LTS) halves the Carnot penalty relative to LTS refrigeration, reducing the cryogenic parasitic power per unit heat load. Renaissance Fusion's magnet operating temperature (20 K) has been confirmed in the Helmholtz demonstration [MT29 Abstract].
- **On paper only**: Full cryogenic system design for the laser-patterned cylinder stellarator (thermal shield geometry, cooldown procedures for a large distributed superconductor array). Cryogenic heat load from neutron/gamma irradiation of HTS cylinders — a key input to recirculating power estimation.
- **Missing at scale**: Refrigeration system sizing for the full magnet set (not yet characterized). Cryogenic load from the neutron irradiation environment in the blanket gap — REBCO film irradiation generates localized heat that must be removed without compromising Jc. Demonstrated long-term cryogenic reliability for the laser-patterned cylinder geometry.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Film Deposition at Commercial Scale — Novel Industrial Process with No Cost Data**

Renaissance Fusion's magnet approach replaces REBCO tape winding with thin-film deposition and laser patterning on cylindrical substrates. This removes the primary REBCO tape supply chain bottleneck (km-scale wound tape, ~$30–100/kA-m [cited per 21-spherical-tokamak-hts analysis, Section 4]) but substitutes a fundamentally different manufacturing challenge: industrial REBCO film deposition at 1 m diameter scale with nuclear-grade uniformity and the throughput needed for a full stellarator magnet set.

REBCO thin-film deposition (MOCVD, PLD, sputtering) is routinely done in research at wafer scale (centimeters to tens of centimeters). Scaling to 1 m diameter cylindrical substrates introduces:
- Chamber size and geometry requirements for uniform deposition
- Substrate handling and rotation for coating uniformity
- Quality control on curved non-planar surfaces
- Laser patterning precision at stellarator winding surface dimensions

No industrial process for this manufacturing approach exists at relevant scale. The Helmholtz demonstration validates the physics concept but does not reveal production economics. For TEA purposes, the magnet CAS account is entirely uncharacterized from a cost basis, and must be modeled with very wide uncertainty bounds. This is the single largest manufacturing unknown in the concept.

**Liquid Li-LiH System — Supply Available, Engineering Novel**

Raw lithium supply is not a bottleneck. Global lithium production has scaled dramatically with battery demand (~100,000 tonnes/year in 2024, primarily from Australia, Chile, and China). This is a meaningful supply chain advantage over beryllium-containing FLiBe (limited to ~300 tonnes/year Be globally, from a handful of suppliers). However, the Li-LiH mixture introduces:

- **Li-6 enrichment**: The baseline optimized design uses **non-enriched natural Li-LiH** (7.5% Li-6) and achieves TBR = 1.60 — well above the 1.15 design requirement. Li-6 enrichment to 90% is explored in the JNM paper as an optional trade-off that reduces the required breeding layer thickness by ~2 cm but adds enrichment cost; the paper notes this requires "a detailed cost analysis" to justify and does not recommend it as a baseline. Enrichment is therefore a cost optimization lever, not a physics necessity. Global Li-6 enrichment capacity (limited legacy production in Russia and China, early-stage Western alternatives) is not a supply-chain risk for this baseline design.
- **LiH component**: Lithium hydride is commercially produced but is a solid at room temperature. Operating the Li-LiH mixture as a high-temperature fluid introduces handling and compatibility challenges (LiH reacts with moisture; handling in inert atmosphere required). The specific Li-LiH operating mixture composition is not published, adding uncertainty to both supply chain requirements and tritium chemistry behavior.
- **Pb pebbles**: Lead is globally abundant and not supply-constrained. The Pb pebble layer [JNM 599 (2024) 155239] adds neutron multiplication without introducing a scarce material.
- **Tritium inventory in liquid Li**: Tritium has very high solubility in liquid lithium (~100× higher per unit volume than in FLiBe). This creates a large in-circuit tritium inventory that must be managed for safety and tritium accounting, and requires an effective extraction system before the primary circuit reaches steady state.

**Structural Materials (RAFM Steels for Liquid Metal Compatibility) — Qualification Gap**

Structural components in contact with flowing Li-LiH at elevated temperatures and under 14 MeV neutron irradiation require:
- Resistance to liquid lithium corrosion (austenitic steels are attacked by Li; RAFM steels — EUROFER97, F82H — are preferred)
- Radiation swelling and embrittlement resistance under 14 MeV neutron spectrum
- Thermal cycling resistance at the wall loading of 25 MW/m²

RAFM steels have extensive irradiation databases from fission reactors, and partial 14 MeV neutron data from fusion-neutron sources. However, simultaneous liquid Li-LiH chemical exposure + fusion neutron irradiation at fusion-relevant fluences has not been demonstrated for any structural alloy. This is a shared qualification gap with all D-T liquid metal blanket concepts but is more acute here because of the higher wall loading (25 MW/m² vs. ~5–10 MW/m² in most liquid metal blanket designs).

**sCO₂ Turbomachinery — Emerging at GW Scale**

sCO₂ turbines and compressors are approaching commercial readiness at MW scale but have not been demonstrated at GW output. The 49–51% efficiency target requires high turbine inlet temperatures enabled by the liquid metal heat source — specific temperature not published, but substantially above current sCO₂ demonstration conditions. Cost projections for GW-scale sCO₂ turbomachinery vary widely; the best analogues are natural gas combined cycle turbines, adjusted for sCO₂ working fluid properties. This technology is shared with other sCO₂-adopting concepts in this survey (Helical Fusion, concept 36), and cost data will improve as the sCO₂ industry matures.

**Tritium (Shared D-T Constraint)**

The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU reactor byproduct and decaying at 5.5%/year. A single D-T reactor startup requires ~1 kg at >$35,000/g [per 21-spherical-tokamak-hts analysis, Section 4]. Renaissance Fusion's TBR is unconfirmed in available sources (fm = 1.24 is confirmed; TBR is a distinct quantity). If the blanket achieves TBR > 1, this provides the breeding self-sufficiency required for fleet deployment, but the sequencing constraint is universal for D-T: early plants must demonstrate self-sufficiency before the fleet can scale beyond the available external tritium inventory.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output | 1 GWe | Nuclear Fusion 64 (2024) 026007 — cost-optimized design point | high | Target output at the economically optimized machine scale |
| Major radius | ≤4 m | Nuclear Fusion 64 (2024) 026007 | high | Upper bound at cost-optimal design point |
| Aspect ratio | ~4 | Nuclear Fusion 64 (2024) 026007; dossier.md §Summary | high | Much more compact than W7-X (A=10); approaching tokamak geometry |
| Nominal on-axis magnetic field | 10 T | Nuclear Fusion 64 (2024) 026007 | high | Nominal design field; exceeds W7-X (3 T) and Proxima Fusion targets |
| Peak coil field | 15 T (design); up to 20–40 T (paper envelope) | Nuclear Fusion 64 (2024) 026007; dossier.md §Magnet Type | medium | Wide range; 15 T is the primary design target; 40 T upper bound approaches REBCO Jc limit |
| D-T plasma temperature design point | 10 keV | Nuclear Fusion 64 (2024) 026007 | high | Equivalent to ~116 million K; standard D-T burn temperature |
| Q target | ∞ (ignited — zero external heating at steady state) | Nuclear Fusion 64 (2024) 026007; dossier.md §Plasma State | high | Most aggressive plasma state target among all stellarators in this survey |
| Primary heating method | NNBI (startup/ramp-up only; 60% neutralization efficiency) | Nuclear Fusion 64 (2024) 026007 | high | NNBI not needed at operating point; eliminates continuous heating capital/operating cost |
| sCO₂ Brayton-Rankine cycle efficiency | 49–51% | Energy Conversion and Management 276 (2023) 116572 | high | Genetic algorithm optimized; highest thermal cycle efficiency in this survey |
| Net plant efficiency | 34% | Energy Conversion and Management 276 (2023) 116572 | high | After all parasitic loads; significantly below cycle efficiency, implying large parasitic load |
| Implied fusion thermal power | ~2.9 GW_th | [inferred: 1 GWe / 0.34 net efficiency] | medium | Not directly published; derived from net output and efficiency |
| Implied gross electric output | ~1.47 GWe | [inferred: ~2.9 GW_th × 0.50 cycle efficiency; approximate] | low | Requires assumption that all thermal power goes through sCO₂ cycle |
| Implied recirculating power fraction | ~32% of gross electric | [inferred: (0.50 − 0.34) / 0.50; cycle eff 50%, net 34%] | low | Large fraction for a Q=∞ design; dominant contributors unidentified in sources |
| Liquid metal wall loading | 25 MW/m² | J. Nuclear Materials 599 (2024) 155239 | high | Claimed design capability; no demonstration at this loading |
| Neutron energy absorption | 99.99% | J. Nuclear Materials 599 (2024) 155239 | high | First wall + blanket combined performance |
| Blanket energy multiplication factor | 1.07 | J. Nuclear Materials 599 (2024) 155239 §Case study | high | Ratio of total blanket thermal energy to incident neutron energy; meets design requirement ≥1.0. Note: a value of 1.24 appears in the original dossier but is not confirmed in the full JNM paper and should not be used |
| Tritium breeding ratio (TBR) | 1.60 | J. Nuclear Materials 599 (2024) 155239 §Case study | high | Optimized configuration: 10 cm Pb + 22 cm non-enriched Li-LiH; design requirement TBR ≥ 1.15; margin ~39% above threshold to cover port losses and fuel cycle inefficiencies |
| Blanket inner radial build | 10 cm Pb + 22 cm Li-LiH | J. Nuclear Materials 599 (2024) 155239 §Case study | high | Optimized case study configuration; Li-LiH layer extended from 17 cm to 22 cm to meet ≥90% nuclear heat extraction in liquid metal layer |
| Outer shielding and bioshield | 50 cm VH₂ + 1.3 m concrete | J. Nuclear Materials 599 (2024) 155239 | high | Beyond liquid metal blanket |
| Operation mode | Steady-state, near-100% duty cycle | Company website; Nuclear Fusion 64 (2024) 026007 | high | Stellarator inherent advantage — no disruptions, no CS or current drive requirement |
| Demonstrated magnet field | 6 T peak (Helmholtz, 1.2 m diameter, 20 K) | MT29 Abstract (2024); dossier.md §Magnet Type | high | Only hardware milestone; 60% of nominal design field; 1.2 m diameter prototype |
| REBCO tape cost (wound analogue — not applicable) | $30–100/kA-m | [analogue — 21-spherical-tokamak-hts analysis Section 4] | low | Cited for reference only; patterned film cost structure is completely different from wound tape |
| Tritium startup cost | >$35,000/g (~1 kg per plant) | [analogue — 21-spherical-tokamak-hts analysis Section 4] | medium | Standard D-T constraint; applies regardless of blanket approach |
| Capacity factor (estimated) | ~90–95% | [estimated — stellarator steady-state advantage; no disruptions or pulse cycling; maintenance intervals unknown] | low | Upper bound assumption; actual maintenance schedule completely uncharacterized |
| Regulatory cost multiplier (fission-style scenario) | 2.2× building costs | Stewart & Shirvan 2022, cited in 01-hts-compact-tokamak analysis | medium | Applies to all D-T fusion concepts as upper-bound regulatory scenario |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost (total plant $/kWe, or major subsystem costs) | truly-unknown | blocking | No cost estimate published in any source; Nuclear Fusion paper reports relative optimization but not absolute cost |
| LCOE estimate | truly-unknown | blocking | No public LCOE or costing model of any kind |
| Magnet system cost | truly-unknown | blocking | Laser-patterned film has no manufacturing cost analogue; REBCO tape pricing not applicable |
| Liquid metal circulation pump power | proprietary / truly-unknown | blocking | Key driver of the ~32% implied recirculating fraction; not disclosed in any source |
| Plasma energy confinement time target (τ_E) | not-yet-sourced | important | Needed to close Lawson criterion at design point; not published separately |
| Plasma density design point | not-yet-sourced | important | Required for Q = ∞ feasibility assessment; not stated in available summaries |
| Bootstrap fraction | not-yet-sourced | important | Key stellarator parameter; theoretically high for QI geometry but not quantified for this design |
| Divertor design and exhaust solution | truly-unknown | important | Not addressed in any published source; critical for plasma-facing component cost and availability |
| Annual O&M cost | truly-unknown | important | No O&M data in any source; flowing wall introduces different maintenance philosophy than solid PFC |
| Component replacement schedule | truly-unknown | important | Flowing wall may not require discrete module replacement; pump/exchanger maintenance uncharacterized |
| Peak Li-LiH outlet temperature | not-yet-sourced | important | Determines achievable sCO₂ turbine inlet temperature and therefore cycle efficiency |
| HTS cylinder count and scale for full plant | not-yet-sourced | important | Needed to estimate magnet system cost and REBCO film demand; not published |
| Cryogenic refrigeration power at 20 K for full magnet set | not-yet-sourced | important | Key contributor to recirculating power; not characterized in available sources |
| Li-6 enrichment cost optimization | derivable | nice-to-have | Baseline design achieves TBR = 1.60 without enrichment; enrichment is an optional cost optimization (reduces blanket thickness ~2 cm) requiring detailed cost analysis to evaluate |
| sCO₂ turbomachinery capital cost at GW scale | not-yet-sourced | important | Emerging technology; cost data improving but not specific to this concept |
| NNBI system cost (startup-only) | derivable | nice-to-have | Less critical since startup-only; ITER NNBI program provides cost analogue |
| REBCO film Jc vs. field at 20 K | not-yet-sourced | nice-to-have | Needed to confirm 20–40 T peak coil fields are achievable with realistic Jc values |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No capital cost estimate or LCOE model of any kind — LCOE analysis entirely unanchored | S1, S2, S5 | truly-unknown | blocking | No near-term public disclosure expected; use ARIES-CS as closest stellarator plant cost analogue with full magnet and blanket cost override |
| 2 | Laser-patterned HTS film manufacturing cost — no industrial analogue at any scale | S2, S3, S4, S5 | truly-unknown | blocking | Monitor MT29/MT30 program publications; engineering estimate from thin-film deposition industry (semiconductor, photovoltaics CVD) with appropriate scaling. **LCOE impact**: With r_coil elasticity ≈ +0.77, a 10× coil cost vs. the tape-winding analogue produces an LCOE roughly 7× above the tape-winding-based estimate (≫200 $/MWh swing); a 0.3× scenario (if film deposition is cheaper than winding) reduces LCOE substantially. The cost model must test this range explicitly via scenario branches — a single stub value obscures the dominant structural uncertainty |
| 3 | Liquid metal circulation pump power — drives the unexplained gap between cycle efficiency (50%) and net efficiency (34%) | S2, S5 | proprietary / truly-unknown | blocking | Derive from first principles: estimate Li-LiH flow rate needed for 25 MW/m² wall loading at acceptable temperature rise, then apply liquid metal pump power scaling; treat as ±50% estimate |
| 4 | ~~Tritium breeding ratio (TBR)~~ — **RESOLVED**: JNM 599 §Case study explicitly reports TBR = 1.60 for the optimized 10 cm Pb + 22 cm Li-LiH configuration; design requirement TBR ≥ 1.15 met with 39% margin | S1, S5 | resolved | — | No further action required; TBR is now in Available Parameters table |
| 5 | Liquid metal wall system cost — no cost analogue for Li-LiH circulation at plant scale | S2, S3, S4, S5 | truly-unknown | blocking | Use Na-cooled fast reactor primary circuit costs as structural analogue; apply significant uncertainty premium for first-of-kind fusion application |
| 6 | Divertor design and exhaust solution — not addressed in any source | S3, S5 | truly-unknown | important | Critical for plasma-facing component cost and availability model; need company disclosure or stellarator divertor analogue (W7-X island divertor adapted to compact geometry) |
| 7 | Plasma parameters at ignition — confinement time, density, bootstrap fraction not published | S2, S3, S5 | not-yet-sourced | important | Apply ISS04 stellarator energy confinement time scaling to design point (R, A, B, n, T); treat as engineering estimate |
| 8 | Annual O&M cost — zero data | S2, S5 | truly-unknown | important | Apply ARIES-CS stellarator O&M baseline (~2–4% of capital/year); add liquid metal system maintenance adder from Na-cooled fast reactor experience |
| 9 | Peak Li-LiH outlet temperature | S3, S5 | not-yet-sourced | important | Should be in ECM paper (Fama et al. 2023); read original paper; determines confidence in 49–51% efficiency target |
| 10 | Li-6 enrichment cost optimization | S4 | derivable | nice-to-have | JNM baseline achieves TBR = 1.60 with non-enriched natural Li-LiH — enrichment is NOT a physics requirement. Enrichment to 90% Li-6 reduces blanket thickness by ~2 cm but adds enrichment cost; trade-off requires detailed cost analysis. Downgraded from important to nice-to-have |
| 11 | REBCO film Jc at peak coil fields (20–40 T) at 20 K | S3 | not-yet-sourced | important | REBCO Jc vs. field data at 20 K is available in literature; check against design point to confirm feasibility at upper end of coil field range |
| 12 | HTS cylinder count, dimensions, and total REBCO film area for full plant | S3, S5 | not-yet-sourced | important | Required to estimate magnet system scale and film deposition demand; not published |
| 13 | Cryogenic refrigeration power for full magnet system at 20 K | S3, S5 | not-yet-sourced | important | Estimate from magnet volume and neutron/gamma heating at design fluence; 20 K is more efficient than 4 K LTS — quantify the advantage |
| 14 | Component replacement schedule and maintenance intervals | S2, S3, S5 | truly-unknown | important | Flowing wall concept may lack discrete replacement cycles; pump MTBF and heat exchanger fouling analogy from liquid metal industrial systems |
| 15 | sCO₂ heat exchanger tritium permeation and compatibility with Li-LiH | S3, S4 | truly-unknown | nice-to-have | Safety-relevant and could require design mitigations (permeation barriers); no published data for Li-LiH / sCO₂ interface |

---

## Section 7: Cross-Concept Notes

**Approved prior analyses referenced:**

The only approved prior analysis in the pool for cross-referencing is the Spherical Tokamak - HTS (`21-spherical-tokamak-hts`, Tokamak Energy). While the confinement topology is entirely different, three elements are reused:

- **D-T tritium supply constraints**: Global inventory (~25–30 kg), startup requirement (~1 kg at >$35,000/g), CANDU production decline, and fleet sequencing constraint apply identically to this concept. Characterization from [21-spherical-tokamak-hts, Section 4] is adopted without modification.
- **REBCO tape market reference (wound)**: The $30–100/kA-m wound tape pricing from [21-spherical-tokamak-hts, Section 4] is cited explicitly as a reference point that does *not* apply to the laser-patterned film approach. The distinction is noted: the global tape supply bottleneck is not the relevant constraint here; the REBCO film deposition process cost is the relevant constraint, and it has no published analogue.
- **Regulatory cost scenario**: Stewart & Shirvan 2.2× building cost multiplier for fission-style regulation applies as a D-T fusion upper-bound scenario, identical to all D-T concepts.

**Divergences from peer stellarators (in-progress, not formally cross-referenceable):**

Three in-progress stellarator analyses (09-qi-stellarator-hts/Proxima Fusion, 20a-type-one-stellarator/Type One Energy, 10-large-scale-stellarator/Gauss Fusion) have not reached approved status and cannot be formally cited. However, the following conceptual distinctions are important for the TEA pipeline:

- **Magnet manufacturing — unique cost structure**: All other HTS stellarators in this survey use wound REBCO tape in complex 3D non-planar coils. The laser-patterned cylinder approach cannot share cost modeling assumptions with any other concept. The coil cost model must be built independently with wide uncertainty bounds.

- **Blanket architecture — consolidated vs. separate CAS accounts**: Proxima Fusion (09) uses LiPb blanket; Type One Energy (20a) uses solid HCPB with helium cooling; Gauss Fusion (10) uses Li blanket (unspecified form). All of these are contained blanket concepts where the first wall, breeder, and shield are distinct sub-elements. Renaissance Fusion's flowing liquid metal wall consolidates what would be three or four separate CAS accounts into a single pumped-fluid system. This is an architecturally different cost model, not just a parameter variation.

- **Q target — capital cost implications**: All other stellarators in this survey target burning plasma state (Q >> 5) but not ignition. The Q = ∞ target eliminates the steady-state heating/current-drive system as a capital cost account (ECRH gyrotrons, power supplies, antennas are absent at operating point). This is a genuine cost advantage if achieved, potentially reducing the recirculating power account by 10–20% compared to ECRH-heated stellarators. However, it is also the most uncertain physics assumption in the concept.

- **Power conversion efficiency — 15-percentage-point premium**: Type One Energy (20a) uses conventional steam Rankine (estimated ~35%). Renaissance Fusion's sCO₂ combined cycle (49–51%) represents a 15-point efficiency premium. At 1 GWe net output, this implies ~30% less thermal power required — which scales down blanket/BOP capital cost relative to what steam Rankine would require. This is a favorable architectural feature, but it is **not** the dominant LCOE lever: thermal efficiency elasticity is ~0.11 in the sensitivity model, compared to ~0.77 for coil cost and ~0.94 for plant availability. The efficiency premium reduces required thermal capacity but does not make or break the LCOE case; coil cost uncertainty and plant availability do.

- **Aspect ratio compactness — building and civil cost**: A ≈ 4 is much more compact than W7-X (A = 10), Type One Energy (A estimated ~7), or any large-scale QI stellarator. A compact machine fits in a smaller building footprint, reducing civil and structural cost. However, compactness also reduces the geometric flexibility available for QI optimization — the confinement quality of a compact QI at A ≈ 4 has not been demonstrated, while W7-X at A = 10 has proven QI benefits.

**Cost model architecture recommendation for TEA pipeline:**

**Modeling approach: 1costingfe with explicit scenario branches for two highest-uncertainty accounts.** Despite the architectural novelties, a completely free-form model is not warranted — the plant-level cost structure (civil, balance of plant, fuel cycle, O&M) follows standard CAS conventions and can be populated from ARIES-CS analogues with appropriate adjustments. The correct approach is to use the 1costingfe framework with explicit overrides and scenario branches on the two accounts where tape-winding analogues are inapplicable:

1. **C220103 (coil cost)**: Three scenarios — 0.3× (film cheaper than winding), 1.0× (tape-winding analogue), and 10× (novel process cost premium) — must be implemented as explicit branches to characterize the dominant LCOE uncertainty. A single stub value produces false precision.
2. **C220101 (first wall / liquid metal wall system)**: Override the standard solid-blanket cost with a liquid-metal-system analogue (Na-cooled fast reactor primary circuit as lower bound) plus a first-of-kind adder; apply ±50% uncertainty bounds.

The remaining CAS accounts requiring non-standard treatment but not scenario branches:
3. **Heating/CD**: Startup-only NNBI (one-time capital, no steady-state recirculating load) — size from ITER NNBI programme cost analogue, apply discount for startup-only duty cycle.
4. **Power conversion (C240000)**: sCO₂ combined cycle (TRL 4–5) — use emerging sCO₂ cost projections rather than steam Rankine rates; 49–51% efficiency assumption should be flagged as medium-confidence pending GW-scale demonstration.

---

## Section 8: Sources

**1. Nuclear Fusion 64 (2024) 026007 — Primary design paper**
- Full citation: Samulski, C. et al. (2024) "Economically optimized design point for a compact liquid-metal-wall stellarator," *Nuclear Fusion*, 64, 026007. doi:10.1088/1741-4326/ad142e
- Contribution: Definitive source for machine geometry (R ≤ 4 m, A ≈ 4), magnetic field (10 T nominal, 15 T at coil, 20–40 T peak envelope), D-T plasma design point (10 keV), Q = ∞ target, NNBI startup heating (60% neutralization efficiency), and the economic optimization rationale for the design point. Most directly useful source for TEA.
- Location: dossier.md §Key Sources; available at iopscience.iop.org

**2. Journal of Nuclear Materials 599 (2024) 155239 — Blanket and neutron management paper**
- Full citation: (Authors not given in dossier) (2024) "Compact fusion blanket with liquid metal wall," *Journal of Nuclear Materials*, 599, 155239. doi:10.1016/j.jnucmat.2024.155239
- Contribution: Defines the integrated first-wall/blanket/shield system: 15 cm Pb + 18 cm Li-LiH radial build, 25 MW/m² wall loading capability, fm = 1.24 neutron multiplication, 99.99% neutron absorption, 50 cm VH₂ + 1.3 m concrete bioshield. Primary source for all blanket, neutron management, and wall loading parameters.
- Location: dossier.md §Key Sources; available at doi.org

**3. Energy Conversion and Management 276 (2023) 116572 — Power conversion system paper**
- Full citation: Fama et al. (2023) "Optimized power conversion system for compact fusion reactor," *Energy Conversion and Management*, 276, 116572. doi:10.1016/j.enconman.2022.116572
- Contribution: Genetic algorithm-optimized sCO₂ Brayton-Rankine combined cycle for Renaissance Fusion's design. Key results: 49–51% thermal cycle efficiency, 34% net plant efficiency at 1 GWe target. Primary source for all power conversion parameters.
- Location: dossier.md §Key Sources; available at doi.org

**4. MT29 Abstract (2024) — Magnet program**
- Full citation: Renaissance Fusion magnet program abstract, Applied Superconductivity Conference MT29 (2024). Indico.cern.ch event 1431972, contribution 6420099.
- Contribution: Documents the primary hardware milestone: 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K. Validates that laser-patterned REBCO film on cylindrical substrates can carry superconducting current at useful fields. Primary source for TRL assessment of magnet system.
- Location: dossier.md §Key Sources; available at indico.cern.ch

**5. Renaissance Fusion technology page (renfusion.eu/technology)**
- Contribution: Company-authored confirmation of laser-patterning approach, liquid metal wall, steady-state operation with "near-100% duty cycle," and ignited design target. Consistent with peer-reviewed papers.
- Location: dossier.md §Key Sources

**6. UC Berkeley seminar — "High-field HTS stellarators with liquid metal walls"**
- Contribution: Additional context on magnet fabrication philosophy and the combined HTS + liquid wall design rationale. Provides qualitative support for the synthesis of these two innovations.
- Location: dossier.md §Key Sources; nuc.berkeley.edu

**7. Innovation News Network (2024) — "Simplifying stellarator technology"**
- Contribution: Accessible company description of the laser-patterning concept and its motivation (eliminating coil winding complexity). Secondary/popular press; used for context only.
- Location: dossier.md §Key Sources; innovationnewsnetwork.com

**8. D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts, Tokamak Energy) [Cross-reference]**
- Contribution: D-T tritium supply constraint characterization (startup cost, CANDU decline, sequencing requirement); REBCO wound tape pricing reference ($30–100/kA-m, noted as not applicable to patterned film); regulatory cost scenario (Stewart & Shirvan 2.2×).
- Location: analyses/21-spherical-tokamak-hts/analysis.md

**9. Stewart, M. and Shirvan, K. (2022) — Regulatory cost study [Referenced via prior analyses]**
- Contribution: Fission-style nuclear regulation cost multiplier (2.2× building cost). Applied as upper-bound regulatory scenario for this D-T concept, consistent with application to all D-T fusion concepts.
- Location: Referenced in handwritten exemplar 01-hts-compact-tokamak.md and in 21-spherical-tokamak-hts analysis
