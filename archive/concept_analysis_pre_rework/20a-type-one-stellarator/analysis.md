---
ID: 20a-type-one-stellarator
Concept: QI Modular HTS Stellarator - Infinity Two
Company: Type One Energy
Status: draft
Created: 2026-04-19
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: QI Modular HTS Stellarator – Infinity Two (Type One Energy)

**Concept**: Quasi-isodynamic Modular HTS Stellarator — D-T fuel
**Company**: Type One Energy (Madison, WI)
**Pilot Plant**: Infinity Two
**Confinement Family**: MFE — Stellarator (QI/maximum-J, 4-field-period, modular coils)

---

## Section 1: Availability of Data

**Rating: Moderate**

Type One Energy has published a six-paper Physics Basis in the *Journal of Plasma Physics* (2025), making Infinity Two one of the most thoroughly documented private fusion designs in the current landscape. This level of peer-reviewed disclosure is exceptional for a private company at pre-conceptual design stage and stands in sharp contrast to the opacity of most competitors. However, the Phase 1a extraction contains only secondary sources — press releases and news articles — rather than the underlying peer-reviewed papers. Critical engineering and economic parameters remain unpublished.

**Published technical documentation:**
The dossier characterizes the six JPP papers with high confidence. Key documented results:
- E65: Comprehensive unified baseline physics design — R = 12.5 m, A = 10, Q > 40, 800 MW D-T [dossier.md §Confinement Concept, §Plasma State]
- E86: Breeder blanket and tritium fuel cycle feasibility — TBR = 1.30, confirmed by OpenMC Monte Carlo with 300 million particle histories [dossier.md §Tritium Breeding]
- Baseline plasma physics design paper: ECRH as sole auxiliary source; pellet injection for fueling only [dossier.md §Primary Heating]
- 70,000+ configuration simulations on the DOE Frontier supercomputer underpinning the design selection [dossier.md §Confinement Concept]

**Company transparency:**
Key machine parameters are publicly disclosed: R = 12.5 m, A = 10, 9 T on-axis, 800 MW fusion, 350 MWe net, TBR = 1.30, HCPB blanket, REBCO HTS coils in partnership with CFS, 2-year operating cycle with 30-day maintenance outages [typeoneenergy-type-one-energy-issues-first-realistic.md §Physics Solution]. However, the following remain unpublished: capital cost, overnight construction cost, thermal efficiency, ECRH auxiliary power requirement, recirculating power fraction, capacity factor target, and detailed blanket/divertor geometry.

The press release states:

> "Type One Energy has architected a maintenance solution which supports good power plant Capacity Factors (CF) and associated Levelized Cost of Electricity (LCOE)."
> — typeoneenergy-type-one-energy-issues-first-realistic.md

and

> "[The design achieves] favorable regulatory requirements for component manufacturing and power plant construction methods essential to achieving a reasonable Over-Night Cost (ONC) for Infinity Two."
> — typeoneenergy-type-one-energy-issues-first-realistic.md

These indicate cost-consciousness in the design but provide no quantitative anchor for an LCOE model.

**Independent analyses:**
No independent techno-economic analysis has been published for Infinity Two specifically. The ARIES-CS study (late 1990s–early 2000s) remains the most detailed published stellarator power plant study and is the primary independent reference for stellarator cost structure. Brown (2018, *IEEE Transactions on Plasma Science*) provides a comparative cost decomposition across spherical tokamak, standard tokamak, and stellarator geometries. No system code (PROCESS, HELIOS) results have been published for the Infinity Two design point.

**Phase 1a dossier completeness:**
The Phase 1a dossier achieved high confidence on all primary taxonomy columns (confinement family, topology, fuel, heating, blanket type, TBR, operation mode, magnet type) after two research iterations including the parent concept 20-modular-hts-stellarator. The remaining gap is in engineering details: blanket radial build, island divertor geometry, remote maintenance cycle, and ECRH power requirement. These are confirmed as not-yet-published rather than omissions in research coverage.

**Commercialization posture:** Taken together — six peer-reviewed JPP physics basis papers, a signed TVA Cooperative Agreement (January 2025), and a concrete Infinity One subscale program targeting 2029 — Type One Energy's commercialization posture is more advanced than the typical private fusion developer at TRL 3–4. The staged program (Infinity One → Infinity Two) does not resolve the manufacturing unknowns, but it provides a public, time-bounded validation pathway that can reduce the TRL 2–3 risk identified in Section 3.

**Key data gaps limiting this analysis:**
1. Thermal efficiency — implied ≈47% from published power balance using D-T canonical M_b=1.10 (model uses 0.45 as central estimate); not explicitly stated
2. Capital cost estimate or $/kWe target — not published; "reasonable ONC" is the only reference
3. Auxiliary ECRH power (MW) at the Q > 40 design point
4. Remote maintenance system cycle time and blanket replacement interval
5. 3D HTS coil manufacturing approach, yield, and cost — the dominant manufacturing risk

---

## Section 2: Challenges in Capturing System Function

Infinity Two presents a distinct LCOE modeling challenge: it is the most thoroughly physics-documented private fusion concept, with published TBR, Q, and machine geometry, but lacks any published economic characterization. The physics uncertainties are lower than most competitors; the cost uncertainties are high and stem from the novelty of the 3D HTS manufacturing problem and the large machine scale. Challenges are ranked by LCOE impact.

**1. 3D HTS coil manufacturing cost — the LCOE model has no cost precedent (Impact: Critical)**

The defining cost challenge for Infinity Two is winding REBCO HTS tape onto complex, three-dimensionally curved non-planar modular coil forms. This is categorically harder than manufacturing HTS coils for a tokamak: tokamak TF coils are planar (2D) and can be wound with conventional winding machines. Stellarator coils curve in three dimensions — their cross-section rotates and twists along the coil path, following the 4-field-period QI optimization. W7-X (the scientific predecessor, built with LTS Nb₃Sn/NbTi) took approximately six years of coil manufacturing and cost on the order of €1 billion for magnets alone [ARIES-CS and W7-X construction records, referenced in dossier.md]. REBCO tape is stiffer and more sensitive to bending strain than the LTS multi-strand cables used in W7-X, making the transition to HTS on the same geometry a genuine engineering problem, not just a material substitution. Type One Energy's CFS partnership brings REBCO manufacturing experience from flat-coil tokamak winding; its applicability to 3D stellarator forms is not yet demonstrated. No public cost estimate exists for HTS 3D stellarator coils at any scale. ARIES-CS estimated magnet costs at 20–30% of direct capital cost for a stellarator; at Infinity Two scale, the absolute magnet cost could easily dominate the plant capital budget.

**Corollary risk — error field correction coils:** W7-X required auxiliary external correction coils to suppress low-order error modes (n/m=1) that would otherwise degrade island topology and divertor performance. The Infinity Two design specifically selected the m=5, n=4 island chain (not resonant at the ι=1 surface) to minimize this risk [cambridge-core-services-aop-cambridge-core-content-view.md §2.3], and correction coil control techniques are planned for testing in Infinity One [cambridge-core-services-aop-cambridge-core-content-view.md §7]. If manufacturing-scale field errors at Infinity Two nonetheless require correction coils, this is an unbudgeted capital item — additional coil systems, power supplies, and cryogenic infrastructure — with no published cost estimate. The design intent avoids them, but field-error tolerance at Infinity Two manufacturing scale has not been validated.

**2. Large machine scale — high absolute capital with uncertain learning rate (Impact: High)**

At R = 12.5 m and A = 10, Infinity Two is physically large — major radius nearly twice ITER's 6.2 m. Large machines have better physics performance per unit field (lower required field for ignition) but high absolute capital cost: the vacuum vessel, plasma-facing components, building, and coils all scale with machine volume. The fusion power density is relatively low (800 MW in a large plasma volume), which means capital investment per MW of fusion power is high relative to compact high-field designs like CFS. The key question for TEA is whether the capital per kWe is offset by high availability (steady-state, 2-year cycles) and simplified physics (no disruptions, no current drive). No published analysis quantifies this trade-off for Infinity Two specifically.

**3. Unknown thermal efficiency and recirculating power (Impact: High)**

The press release states 800 MW fusion power and 350 MWe net [typeoneenergy-type-one-energy-issues-first-realistic.md §Physics Solution]. Deriving thermal efficiency requires knowing: (a) blanket energy multiplication factor (with HCPB and Be multiplier, typically 1.10–1.20), (b) recirculating power (ECRH, cryogenics, pumps), and (c) gross electrical output. Working backward:

- With Q > 40, P_ext (ECRH) = 800/Q ≤ 20 MW
- Gyrotron wall-plug efficiency ~50–55% → electrical input ~36–40 MWe
- Cryogenic load for HTS at operating temperature: ~10–20 MWe [analogue from HTS tokamak studies]
- Other auxiliaries (pumps, tritium systems): ~10–15 MWe
- Total recirculating: ~60–75 MWe [inferred]
- Gross electric = 350 + 65 ≈ 415 MWe
- With blanket multiplication M_b = 1.10 (D-T canonical per scoring_framework.md §Blanket energy multiplication): gross thermal = 800 × 1.10 = 880 MW
- Implied thermal efficiency = 415/880 ≈ 47%

A 47% efficiency would require a supercritical steam or sCO₂ cycle; the dossier characterizes the cycle as "Rankine with reheat, thermal efficiency > 30%." The "> 30%" lower bound is consistent with a wide range and the exact value materially affects LCOE. This is a derivable gap, not a fundamental unknown, but the derivation requires one or two unanchored assumptions.

**4. Island divertor design choice — two scenario branches with different TRL and exhaust efficiency (Impact: Moderate–High)**

Stellarators exhaust heat and particles through island divertors. The Infinity Two physics basis paper (E67, Bader et al., *J. Plasma Phys.* 2025) defines two distinct divertor designs under development, representing different risk profiles and TEA implications:

> "adequately sized island divertors to exhaust helium ash"
> — typeoneenergy-type-one-energy-issues-first-realistic.md

**Option A — Classical island divertor (W7-X heritage, TRL 4–5):** An open divertor with 8 plates (2 per field period) following W7-X geometry, "modeled extensively and tested experimentally, in particular in W7-X" [cambridge-core-services-aop-cambridge-core-content-view.md §E67]. This is the low-TRL-risk option. However, particle exhaust efficiency analogous to W7-X is 0.44%–2.9%, which falls at or below the lower end of the required 0.5%–5% range for Infinity Two steady-state helium ash removal [cambridge-core-services-aop-cambridge-core-content-view.md §4]. Under conservative particle-transport assumptions (5% required), the classical design is marginal; under optimistic assumptions (0.5% sufficient), it may be adequate. The core risk is that helium ash accumulation could degrade plasma performance and limit availability over a 2-year operating cycle.

**Option B — Large Island Backside Divertor (LIBD, TRL 2–3):** A novel closed divertor with a dome structure inserted into the island interior, plus active baffles to improve neutral confinement. The LIBD targets 12.6% particle exhaust efficiency — well above the required range under all scenarios [cambridge-core-services-aop-cambridge-core-content-view.md §7]. However, this design "has not been validated experimentally" [E67]; experimental validation is planned for Infinity One [cambridge-core-services-aop-cambridge-core-content-view.md §7]. The dome must be structurally sound and actively cooled inside the island interior — a challenging access geometry. If perpendicular particle transport is large relative to parallel transport, particles may impinge on the dome's front face rather than the backside, "and the particles will intersect the dome on its front as much as – if not more than – the backside" [E67]. A dome and island shape optimization program is planned but not complete.

The design choice between these options is deferred to Infinity One results. This is a **scenario-determining decision**: the classical divertor carries TRL 4–5 but risks marginal helium ash exhaust over 2-year cycles; the LIBD preserves exhaust margin but adds a TRL 2–3 unvalidated system to the critical path, with its cooling-access geometry unresolved.

**TEA cost direction**: Both options represent a **cost penalty** relative to conventional tokamak divertors. Capital (CAS22): neither option has a published unit cost; the only manufacturing reference is W7-X-scale LTS equipment. The LIBD dome adds a novel actively-cooled structure in constrained access geometry, making it more capital-intensive than the classical option. O&M (CAS70): both options face 2-year continuous heat flux endurance before maintenance access. The divertor design selection should be modeled as a scenario branch: classical (lower capital, availability risk from marginal exhaust) vs. LIBD (higher capital, availability protected by 12.6% exhaust efficiency).

**5. HCPB blanket integration and Be multiplier considerations (Impact: Moderate)**

The HCPB (Helium-Cooled Pebble Bed) blanket is EU-DEMO heritage technology and is well-characterized in the breeding physics literature. TBR = 1.30 is confirmed by OpenMC neutronics with 300 million particle histories [dossier.md §Tritium Breeding], providing confidence in the breeding design. However, two integration challenges for LCOE modeling are unresolved: (a) the blanket must conform to a non-symmetric stellarator first wall, which complicates module design relative to the axisymmetric EU-DEMO configuration; and (b) the beryllium neutron multiplier is toxic, has limited global supply, and adds manufacturing complexity. The EU-DEMO HCPB development program provides the most relevant reference but was designed for a tokamak geometry.

**6. Tritium self-sufficiency margin and startup inventory (Impact: Moderate)**

TBR = 1.30 provides good tritium self-sufficiency margin. However, the 2-year continuous operating cycle requires the tritium fuel cycle to operate continuously at full throughput for 24 months between maintenance outages. Any tritium extraction inefficiency or breeding shortfall during this period cannot be corrected until the scheduled maintenance window, a more demanding constraint than a pulsed or periodically-maintained machine. The startup inventory requirement (~1 kg at >$35,000/g) is shared with all D-T concepts.

**O&M placeholder (flagged per process):**
No published O&M cost breakdown exists for Infinity Two. Steady-state stellarator operation eliminates the disruption repair cost present in tokamak O&M models, but adds unique items: island divertor target replacement, HCPB pebble bed replacement at neutron-damage lifetime, and 3D coil inspection and maintenance. ARIES-CS O&M estimates provide the closest public analog but were developed for an LTS machine.

**Top LCOE sensitivity parameters:**
Three model parameters carry the greatest leverage on Infinity Two's LCOE: (1) **3D HTS coil cost** — the highest-sensitivity input (elasticity ≈ +0.99), proxied by coil radius in the current model but representing the uncharacterized manufacturing cost premium for winding REBCO tape on complex 3D stellarator forms; a 2× error in coil cost translates to nearly a 2× error in LCOE, and the baseline is acknowledged as likely too low relative to the W7-X magnet benchmark. (2) **Availability** (elasticity ≈ −0.93) — the 2-year operating cycle supports a theoretical ~96% capacity factor, but actual unplanned outage exposure from ECRH system failures, tritium processing interruptions, and island divertor degradation is unconstrained; each percentage point below 96% directly increases LCOE. (3) **Construction schedule** (elasticity ≈ +0.55) — 3D HTS coil manufacturing complexity makes schedule overrun the dominant financial cost driver during construction, and no Infinity Two-scale coil has been manufactured. These three parameters should be modeled as uncertainty ranges, not point estimates. In particular, an availability scenario sweep (80% pessimistic / 85% canonical base / 93% mid / 96% aspirational) should accompany the coil cost sensitivity sweep — both have near-equal LCOE elasticity and neither is observationally constrained. The central-case availability of 85% is policy-driven per scoring_framework.md §Plant availability (MCF steady-state, D-T canonical), enabling apples-to-apples LCOE comparison across the MFE concept family; no Type One Energy–published availability target qualifies as a Tier-A override. Presenting only the coil cost sweep hides one of the two dominant LCOE uncertainties.

**Modeling approach — 1costingfe with explicit stellarator adjustments:**

The current model uses the 1costingfe framework with standard tokamak-derived cost accounts. This is defensible in the absence of a stellarator-specific commercial cost database, but requires explicit awareness of three divergences from Infinity Two's actual cost structure: (a) C220103 (3D HTS coils) is the primary account where the framework default is a confirmed lower bound — no 3D stellarator HTS coil fabrication cost precedent exists, and the framework does not penalize for non-planar winding complexity; (b) the central solenoid account should be zeroed out — Infinity Two has no plasma current and no central solenoid; (c) the island divertor account is materially different from a tokamak divertor account and has no published unit cost — both the classical and LIBD options require treatment as scenario-dependent upward adjustments to the divertor line item. ARIES-CS and Brown (2018) can anchor free-form stellarator-adapted cost adjustments and should serve as the cross-check for any concept-specific CAS modifications. The 1costingfe result is best interpreted as a lower bound on capital cost; the ARIES-CS stellarator magnet fraction of 20–30% of direct capital provides an independent sanity check on coil cost sensitivity outcomes.

Note on published operating point: the Infinity Two design is 800 MW fusion / 350 MWe net. The power balance derivation in Section 2 implies η_th ≈ 47% at this point (gross electric ~415 MWe / thermal 880 MW at M_b = 1.10 canonical). Central case uses the canonical D-T blanket multiplication factor 1.10 (no dedicated multiplier credit). HCPB+Be designs may yield 1.10–1.20 in EU-DEMO neutronics literature; a Tier-A cite would justify reverting to 1.15 as a central case. The model should be anchored to the 800 MW published fusion power with thermal efficiency adjusted to match; if the framework requires a different fusion power input, the resulting operating point departure from the published design should be documented explicitly in model output.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature to most mature.

---

**3D HTS Modular Stellarator Coils — TRL 2–3**

- **Demonstrated**: W7-X demonstrates that complex 3D non-planar modular coils can be successfully wound with LTS conductors (Nb₃Sn/NbTi) at stellarator scale — a multi-year, billion-euro achievement [dossier.md §Magnet Type]. CFS has demonstrated 20 T REBCO HTS coils in flat tokamak winding configuration. Type One Energy's CFS partnership is explicitly aimed at adapting CFS's HTS manufacturing experience to stellarator geometry.
- **On paper only**: Winding REBCO tape onto 3D non-planar forms for the Infinity Two coil geometry. The critical technical question — whether REBCO tape can be wound onto complex 3D forms without exceeding its bending strain limit — has not been demonstrated at any scale. REBCO tape has a minimum bending radius of approximately 25–30 mm at room temperature (dependent on tape width and thickness) that may be challenged by the complex curvature of QI-optimized stellarator coil cross-sections. CFS partnership scope and technical approach not publicly documented.
- **Missing at scale**: Industrial process for winding HTS tape on 3D stellarator coil forms. Quality assurance methods for internal winding joints and layer-to-layer adhesion on curved geometries. Demonstrated quench protection strategy for 3D HTS coils (non-planar geometry makes quench propagation dynamics different from planar coils). Radiation-hardened insulation system validated for the 3D coil geometry. Complete Infinity Two-scale coil form manufacturing. Irradiation behavior of REBCO tape under stellarator magnetic geometry (different mechanical stress state than tokamak coils during pulsed field excursions).

**Staged validation pathway — Infinity One (2029):** Type One Energy has a concrete TRL mitigation strategy. A subscale stellarator, "Infinity One," is "currently being designed" and targeted for a design verification test program in 2029 [cambridge-core-journals-journal-of-plasma-physics-article.md]. Infinity One is "derived from the essential features of Infinity Two" and is explicitly intended to reduce the stellarator physics uncertainties — including island divertor / core plasma confinement compatibility — that necessitate conservative design margins in Infinity Two. The device will be constructed and operated at TVA's retired Bull Run fossil plant in Tennessee under a Cooperative Agreement signed January 20, 2025. TVA's stated belief is that Infinity Two is deployable "as early as the mid-2030s" [cambridge-core-journals-journal-of-plasma-physics-article.md]. This staged program distinguishes Type One Energy from most private fusion developers, who have no subscale validation pathway at equivalent TRL. However, the Infinity One→Infinity Two timeline gap introduces a schedule risk: successful 2029 Infinity One verification plus typical construction lead times makes a mid-2030s first plasma date highly aggressive — any design iteration driven by Infinity One results would push that date out.

---

**Island Divertor — Option A: Classical (W7-X Heritage) — TRL 4–5**

- **Demonstrated**: W7-X classical island divertor has operated at stellarator research scale — demonstrating detachment, heat flux reduction, and helium ash exhaust. The Infinity Two classical design (8 plates, 2 per field period) is a direct geometric extrapolation [cambridge-core-services-aop-cambridge-core-content-view.md §E67]. This is the world's only operating island divertor at plasma physics scale. Particle exhaust efficiency analogous to W7-X classical divertor: 0.44%–2.9%.
- **On paper only**: Classical divertor performance at burning plasma (Q > 40, 800 MW) heat and particle fluxes. Helium ash exhaust efficiency is at the low end of the required 0.5%–5% range for Infinity Two — marginal under conservative particle-transport assumptions. Detachment control at heat fluxes likely exceeding 10 MW/m² average.
- **Missing at scale**: Confirmation that 0.44%–2.9% exhaust efficiency is sufficient for 2-year steady-state helium ash removal (depends on particle-transport modeling not yet validated at burning plasma scale). Material selection and qualification for targets under fusion-relevant neutron + steady-state heat flux. Remote maintenance for classical target exchange in Infinity Two non-axisymmetric geometry. Divertor capital and O&M cost basis.

---

**Island Divertor — Option B: Large Island Backside Divertor (LIBD) — TRL 2–3**

- **Demonstrated**: LIBD concept is entirely at physics design / 2D-modeling stage — "a concept that has still not been validated experimentally" [cambridge-core-services-aop-cambridge-core-content-view.md §E67]. Two-dimensional neutral model estimates 12.6% particle exhaust efficiency, well above the required range under all scenarios. The LIBD dome geometry (inserted inside the island interior) is defined in the E67 paper. 87.0±0.1% of particles ionize in the divertor volume in the model.
- **On paper only**: LIBD structural design — the dome must be structurally sound and actively cooled inside the island interior, an access-constrained geometry. Validated exhaust efficiency under conditions where perpendicular transport is comparable to parallel transport (risk of particles impinging the dome front rather than backside). Island and dome shape optimization (planned, not yet complete). Compatibility with Infinity Two's specific magnetic island width and field geometry.
- **Missing at scale**: Any experimental demonstration — Infinity One is the planned validation platform [cambridge-core-services-aop-cambridge-core-content-view.md §7]. Cooling duct routing for the active dome inside the island interior. Remote maintenance access for dome replacement inside the island geometry. Validated performance under burning plasma particle loads. LIBD capital cost compared to classical option.

---

**HCPB Breeding Blanket (Non-Symmetric Geometry) — TRL 3–5**

- **Demonstrated**: HCPB blanket engineering is the most mature of EU-DEMO blanket candidates — extensive EU development over 20+ years with component-level testing. Li₄SiO₄ and Li₂TiO₃ pebble beds characterized under neutron irradiation and thermal cycling. TBR = 1.30 confirmed by OpenMC neutronics for Infinity Two with 300 million particle histories [dossier.md §Tritium Breeding, citing J. Plasma Phys. E86]. Helium coolant circuit technology is mature.
- **On paper only**: HCPB blanket modules conforming to a non-axisymmetric stellarator first wall. Module-to-module interfaces in stellarator geometry (blanket coverage gaps at coil penetrations are geometrically complex in a non-planar stellarator). Validated tritium extraction system sized for 2-year continuous operation. Integrated thermal hydraulics with stellarator-specific first wall geometry.
- **Missing at scale**: 14 MeV neutron irradiation of HCPB pebble beds to full fusion-relevant fluences (> 50 dpa). Tritium extraction from helium coolant at kg/day throughput. HCPB module replacement in stellarator geometry with remote handling. Performance demonstration of beryllium neutron multiplier pebbles under combined irradiation + tritium permeation + thermal cycling. Stellarator-adapted HCPB module geometry that achieves TBR = 1.30 with realistic access ports and diagnostic penetrations.

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: HCPB blanket tritium breeding physics is well characterized. JET and TFTR operated gram-scale D-T tritium fuel cycles. Tritium extraction from solid ceramic breeders has been studied in small-scale experiments. Infinity Two TBR = 1.30 provides self-sufficiency margin [dossier.md §Tritium Breeding].
- **On paper only**: Closed-loop tritium fuel cycle at kg/day throughput for a 2-year continuous operating cycle. Continuous tritium extraction from HCPB pebble bed under full neutron + thermal load with no maintenance access. Near-zero tritium permeation losses through 24-month operating period.
- **Missing at scale**: Industrial tritium processing capacity for a steady-state burning plasma. Tritium extraction from HCPB pebbles at fusion plant throughput — the EU-DEMO program is addressing this but not yet at proof-of-concept stage for full throughput. Tritium accountability throughout a 2-year continuous operating cycle. Permeation barriers validated over 2-year continuous helium coolant service.

---

**Remote Maintenance System for Stellarator Geometry — TRL 4–5**

- **Demonstrated**: ITER remote handling prototypes at full scale for blanket/divertor exchange. W7-X has demonstrated manual and semi-remote component exchange for LTS coil and in-vessel components. The Infinity Two press release states a maintenance solution "supporting good capacity factors" [typeoneenergy-type-one-energy-issues-first-realistic.md] but does not detail the approach.
- **On paper only**: Remote maintenance scheme for Infinity Two-specific geometry — HCPB blanket module extraction, island divertor target exchange, and HTS coil inspection in a non-axisymmetric machine. Maintenance cycle time consistent with 30-day target.
- **Missing at scale**: Validated remote tooling for non-axisymmetric stellarator geometry (no standard casks or central solenoid removal pathway as in tokamaks). Radiation-hardened robotics for the full Infinity Two interior geometry. Neutron activation inventory and waste classification for 30-day maintenance cycle duration. HCPB blanket module handling in helium coolant atmosphere.

---

**ECRH Heating System at Pilot Plant Scale — TRL 5–7**

- **Demonstrated**: MW-class CW gyrotrons are routinely operated on stellarators (W7-X uses 10 × 1 MW, 140 GHz gyrotrons). ECRH is the standard heating method for stellarators — no bootstrap current complication means there is no plasma-current-maintenance constraint on heating approach. At Q > 40, ECRH power is modest (≤ 20 MW of microwave) [inferred from dossier.md §Primary Heating: Q > 40 confirmed]. Pellet injection for fueling is demonstrated technology.
- **On paper only**: Multi-MW ECRH installation optimized for Infinity Two plasma parameters. Validated ECCD-free operation (stellarators do not need current drive — ECRH is purely for heating and control). Long-term gyrotron reliability in the neutron and gamma background of a burning plasma stellarator.
- **Missing at scale**: Gyrotron and transmission line design for Infinity Two's specific magnetic field geometry (9 T on-axis, complex field topology). Continuous-wave gyrotron operation at 20 MW total over 2-year cycles without maintenance. High-efficiency (> 55%) gyrotrons at fusion plant scale (needed to limit recirculating power contribution).

---

**HTS Magnet Technology (Flat-Coil Benchmark, Not 3D) — TRL 6–8**

- **Demonstrated**: CFS demonstrated 20 T REBCO HTS coils in flat tokamak winding configuration (SPARC prototype, 2021). 9 T on-axis for Infinity Two implies lower peak field at the coil than CFS designs (peak field on conductor is higher than on-axis but remains within well-demonstrated REBCO operating range). HTS tape production is ramping at major manufacturers (Shanghai Superconductor Technology, Faraday Factory Japan, CFS).
- **On paper only**: Application of CFS flat-coil HTS manufacturing experience to Infinity Two's 3D coil geometry (see Section 3.1 above). Quench protection strategy for the Infinity Two 3D coil architecture.
- **Missing at scale**: Industrial 3D stellarator HTS coil winding at Infinity Two scale. Supply chain for the REBCO tape length required for a complete Infinity Two coil set (estimated several thousand km; see Section 4).

---

**Balance of Plant (Rankine Steam Cycle) — TRL 8–9**

- **Demonstrated**: Conventional Rankine steam cycles are commercially mature at GW scale. The Infinity Two steady-state operating mode delivers constant thermal power to BOP — no thermal buffering required, unlike pulsed concepts. This is a significant cost and simplicity advantage relative to pulsed systems.
- **On paper only**: Tritium-compatible heat exchanger design between HCPB helium primary coolant and secondary steam circuit. Integration with stellarator-specific coolant geometry.
- **Missing at scale**: Tritium permeation barriers for primary helium circuit interfaces. Stellarator-specific coolant manifold routing (non-axisymmetric geometry complicates plumbing layout).

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck, 3D Winding Adds Qualification Requirement**

Global REBCO production capacity is on the order of a few thousand kilometers per year across all manufacturers. A rough estimate of Infinity Two REBCO demand: the machine has 4 field periods × ~10 modular coils per period = ~40 coils [inferred from QI stellarator geometry analogues]. Each coil at R = 12.5 m, A = 10 is physically large — the coil circumference is roughly 2π × (12.5/10) × aspect ratio adjustment ≈ multi-meter. Scaling from W7-X (50 non-planar coils, ~2.5 m average height, LTS) to Infinity Two's larger geometry, total REBCO tape demand is on the order of 5,000–15,000 km [inferred from geometry scaling with W7-X coil dimensions]. At current REBCO pricing of $30–100/kA-m [handwritten exemplar 01-hts-compact-tokamak.md §Key Materials], even at the low end, magnet conductor cost alone could reach $500M–$2B before fabrication costs. The $10/kA-m commercial viability target [handwritten exemplar] is essential and not yet achieved. Additionally, the tape must be qualified for 3D stellarator winding — a separate challenge from raw tape production.

**Beryllium (HCPB Neutron Multiplier) — Constrained Supply Chain**

The HCPB blanket uses beryllium pebbles as a neutron multiplier (typically Be + n → 2n + α reaction amplifies neutron population, enabling TBR > 1 with solid ceramic breeders). Global beryllium production is approximately 300 tonnes/year, dominated by a single US producer (Materion Corp) [handwritten exemplar 01-hts-compact-tokamak.md §Key Materials]. For a 350 MWe stellarator with HCPB blanket, the beryllium pebble inventory is on the order of tonnes per blanket zone, requiring multi-tonne initial load and periodic replacement as beryllium swells under neutron irradiation (helium production from (n,2n) and (n,α) reactions). Unlike FLiBe — which also contains beryllium — HCPB beryllium pebbles are a separate manufactured component with nuclear-grade purity requirements. No commercial HCPB blanket pebble manufacturing infrastructure exists at fusion scale. Beryllium is also toxic, requiring specialized manufacturing and handling facilities.

**Lithium Orthosilicate / Metatitanate Pebbles (HCPB Breeder) — Specialized Ceramic, Not Commercially Produced at Scale**

The HCPB solid breeder uses Li₄SiO₄ or Li₂TiO₃ pebble beds [dossier.md §Tritium Breeding]. These lithium ceramic pebbles require controlled sintering, pebble size distribution, and Li-6 enrichment. EU-DEMO has developed manufacturing processes for these pebbles at kilogram scale, but not at the multi-tonne scale required for a pilot plant blanket. The ceramics are fragile under irradiation-induced cracking and must be replaced on a neutron fluence schedule.

The Li-6 enrichment situation is more severe than a simple supply concentration issue. The historical Western enrichment route — COLEX (mercury amalgam process), which produced 442 tonnes of Li-6 at Y-12/Oak Ridge between 1954–1963 — is **banned under the Minamata Convention** on mercury for new industrial-scale use; this is an outright prohibition, not a policy preference [science-media-fes-pdf-fes-presentations-2022-pearson.md]. As a result, Western commercial Li-6 supply is currently **effectively zero**: "No other stockpile or supply of lithium-6 currently exists in the West" [Pearson 2022]. The primary alternative technology, ICOMAX (a cleaner variant of COLEX), is "under development as a frontrunner" but "could take decades to fully establish and scale up" [Pearson 2022]. This is a **supply creation problem**, not a diversification problem — Li-6 enrichment for an HCPB blanket would require establishing a new industrial process from near-zero Western capacity on the Infinity Two timeline. Russia and China retain legacy Li-6 production capability, making geopolitical dependency the default path absent Western investment. One design alternative that avoids enrichment entirely is a natural lithium blanket, which Pearson characterizes as "technically challenging, but not impossible" and identifies as worth investigating; this path would require higher TBR margins and blanket redesign but could eliminate the enrichment supply dependency.

**Tritium (D-T Fuel) — Shared Constraint Across All D-T Concepts, with Deployment-Timeline Risk**

Global tritium inventory is approximately 25–30 kg, produced primarily as CANDU heavy-water reactor byproduct, decaying at 5.5%/year [handwritten exemplar 01-hts-compact-tokamak.md §Key Materials]. Startup inventory of ~1 kg at >$35,000/g applies equally to Infinity Two. TBR = 1.30 provides a 30% self-sufficiency margin, which is the highest confirmed TBR value among concepts in this analysis pipeline (most HCPB references target TBR ≈ 1.1–1.15). This margin is meaningful for startup flexibility. The 2-year continuous operating cycle, however, means any tritium processing shortfall or HCPB breeding degradation cannot be corrected until the scheduled maintenance outage — a more demanding reliability requirement than periodically-maintained machines.

**Deployment timeline intersection — supply-timing risk:** Pearson (2022) projects that fusion demand is expected to begin depleting the available tritium stockpile "from as early as ~2035," when ITER and domestic programs (STEP, CFETR) come online simultaneously [science-media-fes-pdf-fes-presentations-2022-pearson.md]. TVA characterizes Infinity Two as deployable "as early as the mid-2030s." These two facts create a material timing overlap: Infinity Two's startup tritium procurement would occur precisely when Pearson projects the global stockpile first comes under sustained multi-project demand pressure. The ~$35,000/g startup cost estimate treats tritium as a fixed-cost parameter, but both price and availability may increase substantially if the mid-2030s drawdown scenario materializes. This should be modeled as a scenario-dependent risk range in Section 5, not a point estimate.

**Tungsten (First Wall and Island Divertor) — Supply Adequate, Manufacturing Challenge**

Tungsten for the island divertor targets and first wall is available in adequate global supply. The stellarator geometry creates a potentially more favorable plasma-facing component environment than a tokamak: no disruptions, no ELMs in a properly controlled stellarator plasma, and steady-state heat flux that may enable better thermal management than pulsed loads. However, island divertor targets see high steady-state heat flux and must survive continuous operation for 2 years between replacements. Tungsten manufacturing for the geometrically complex island divertor target design is not yet characterized.

**No Niobium-Based Superconductors Required**

Unlike LTS stellarators (W7-X used Nb₃Sn/NbTi), Infinity Two uses REBCO HTS throughout, removing niobium from the supply chain. Niobium is produced primarily in Brazil (>80% global supply), and niobium-based conductor supply constraints would apply to an LTS approach. The HTS-only approach removes this supply dependency.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Major radius | 12.5 m | dossier.md §Confinement Concept; J. Plasma Phys. E65 | high | 4-field-period QI/maximum-J; A = 10 |
| Aspect ratio | 10 | dossier.md §Confinement Concept | high | Large-aspect-ratio stellarator; high A simplifies coil manufacturing relative to low-A stellarators |
| On-axis toroidal field | 9 T | dossier.md §Magnet Type | high | Lower than CFS (20 T); higher than W7-X (2.5 T); within well-demonstrated REBCO operating range |
| Fusion power | 800 MW | dossier.md §Fuel; modernsciences-type-one-energy-fusion-pilot-plant-design.md | high | D-T; "800 megawatts of power" confirmed in multiple sources |
| Net electrical output | 350 MWe | typeoneenergy-type-one-energy-issues-first-realistic.md §Physics Solution | high | "delivers a nominal 350 MWe to the power grid" |
| Fusion gain (Q) | > 40 | dossier.md §Plasma State; J. Plasma Phys. E65 | high | "access to ignition"; alpha heating dominant; Q > 40 confirmed |
| Tritium breeding ratio | 1.30 | dossier.md §Tritium Breeding; J. Plasma Phys. E86 | high | OpenMC neutronics with 300M particles; HCPB + FLiBe backup zones |
| Blanket type | HCPB (Li₄SiO₄/Li₂TiO₃ pebbles + Be multiplier) | dossier.md §Tritium Breeding | high | EU-DEMO heritage; FLiBe considered for shielding-primary zones |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | No plasma current drive needed; inherent stellarator steady-state advantage |
| Maintenance cycle | 2-year operating + 30-day planned outage | dossier.md §Operation Mode; Type One Energy press release May 2025 | high | "2-year power plant operating cycle separated by 30-day planned maintenance outages" |
| Primary heating | ECRH only | dossier.md §Primary Heating; J. Plasma Phys. baseline paper | high | "only envisioned external sources required for Infinity Two operation are pellet injection and ECRH" |
| HCPB ECRH power (max) | ≤ 20 MW microwave | [inferred: Q = 40 → P_ext = 800/40 = 20 MW; Q likely higher, reducing this further] | medium | Low absolute heating power requirement due to high Q; favorable for recirculating power fraction |
| Implied gyrotron electrical input | ~36–40 MWe | [inferred: 20 MW ECRH / 0.52 gyrotron wall-plug efficiency; analogue from W7-X gyrotron specs] | low | Sets floor for heating system recirculating power; Q > 40 caps ECRH demand |
| Blanket energy multiplication (mn) | 1.10 | scoring_framework.md §Blanket energy multiplication | high | D-T canonical; HCPB+Be designs may yield 1.10–1.20 (EU-DEMO range); 1.15 reserved as sensitivity excursion pending Tier-A cite |
| Thermal efficiency (implied) | ~47% | [inferred: 800 MW fusion × 1.10 blanket multiplier (D-T canonical) = 880 MW thermal; 350 MWe net + ~65 MWe estimated recirculating = ~415 MWe gross; 415/880 ≈ 47%; model uses 0.45 as conservative central estimate; range reflects recirculating uncertainty] | low | Derivable but not published; "Rankine with reheat, thermal efficiency > 30%" is the only public bound [dossier.md] |
| Implied capacity factor from cycle | ~96% | [inferred: 730 operating days / 760 total days per 2-year cycle = 96%] | low | Aspirational target; actual availability depends on unplanned outages, tritium system availability, ECRH system reliability; not confirmed by company |
| Plant availability (canonical) | 0.85 | scoring_framework.md §Plant availability | high | Canonical per project policy (MCF steady-state, D-T); previously 0.87; no Tier-A override applies — no published Type One availability target exists; 2-year cycle gives theoretical ~96% upper bound but is not a stated commitment |
| REBCO tape cost (current market) | $30–100/kA-m | handwritten exemplar 01-hts-compact-tokamak.md §Key Materials | medium | Target ~$10/kA-m for commercial viability |
| REBCO tape demand (estimated) | 5,000–15,000 km | [inferred: scaling from W7-X ~3,000 km of LTS conductor across 50 coils to Infinity Two's 40 coils at larger scale; HTS tape width equivalent] | low | Wide range reflects uncertainty in coil cross-section and number of turns; no published figure |
| Particle exhaust efficiency — required range | 0.5%–5% | cambridge-core-services-aop-cambridge-core-content-view.md §4 (E67) | high | Bracketing conservative and optimistic particle-transport assumptions for steady-state He ash removal |
| Particle exhaust efficiency — classical divertor (W7-X analogue) | 0.44%–2.9% | cambridge-core-services-aop-cambridge-core-content-view.md §E67 | medium | At low end of required range; marginal under conservative assumptions; TRL 4–5 |
| Particle exhaust efficiency — LIBD (modeled) | 12.6% | cambridge-core-services-aop-cambridge-core-content-view.md §7 (E67) | low | 2D neutral model estimate; unvalidated experimentally; Infinity One dependency; TRL 2–3 |
| Tritium startup inventory | ~1 kg | [analogue: standard D-T startup inventory] | medium | At >$35,000/g; applies to all D-T concepts [handwritten exemplar 01-hts-compact-tokamak.md] |
| Regulatory cost scenario (fission-style) | 2.2× building cost | Stewart & Shirvan 2022 [handwritten exemplar 01-hts-compact-tokamak.md §Challenges] | medium | Upper bound; applies equally to all D-T MFE plants; favorable DOE stellarator program involvement may reduce regulatory uncertainty |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost / overnight construction cost | proprietary | blocking | "Reasonable ONC" mentioned in press release but no estimate published; no plant study exists for Infinity Two; ARIES-CS provides only approximate analog |
| Thermal efficiency (confirmed) | not-yet-sourced | blocking | Implied ~38–42% from power balance but "Rankine with reheat > 30%" is the only published bound; cycle type (steam vs. sCO₂) not confirmed |
| Magnet system cost (3D HTS coils) | truly-unknown | blocking | No public estimate; 3D HTS coil fabrication has no cost precedent; will likely dominate capital cost structure |
| ECRH auxiliary power (confirmed value) | not-yet-sourced | important | Upper bound derivable from Q > 40; actual Q value not published so actual ECRH power unknown |
| Remote maintenance cycle time and cost | proprietary | important | "30-day outage" is stated but maintenance scope and remote handling system design not disclosed |
| Blanket replacement interval and cost | not-yet-sourced | important | HCPB pebble bed neutron damage limit determines replacement frequency; EU-DEMO studies suggest ~5 dpa limit for Li₄SiO₄; implies replacement every few years |
| Island divertor target lifetime | truly-unknown | important | No data for island divertor at burning plasma power levels; life-limiting component for availability |
| HCPB beryllium pebble inventory and replacement cost | not-yet-sourced | important | Beryllium pebble quantity per blanket zone; replacement cycle driven by swelling at ~2,630 appm He/year production |
| Plant capital cost breakdown by CAS element | truly-unknown | blocking | No ARIES-CS–equivalent published for Infinity Two; stellarator-specific cost decomposition (magnets, vessel, blanket, divertor) unavailable |
| Capacity factor (confirmed target) | proprietary | blocking | 2-year cycle implies ~96% theoretical maximum; actual availability target accounting for unplanned outages not published |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Capital cost and $/kWe — no published estimate | S1, S5 | proprietary | blocking | ARIES-CS provides the closest stellarator plant study; apply scaling from ARIES-CS to Infinity Two machine parameters with stellarator cost model from Brown (2018) |
| 2 | 3D HTS coil manufacturing cost — no cost precedent exists | S2, S3, S4, S5 | truly-unknown | blocking | Engineering assessment needed from coil winding specialists; W7-X LTS cost ($1B+ magnets) and CFS flat-coil HTS cost provide partial brackets |
| 3 | Thermal efficiency (confirmed) | S1, S2, S5 | not-yet-sourced | blocking | Power balance derivation gives ~38–42% if recirculating power is estimated; flag as medium confidence; watch for plant study publications |
| 4 | Overnight construction cost (ONC) — "reasonable ONC" is only public reference | S1, S2, S5 | proprietary | blocking | ARIES-CS COE estimates (late 1990s dollars) provide order-of-magnitude; direct comparison requires material + labor cost index adjustment |
| 5 | Plant capacity factor target — 2-year cycle only gives theoretical upper bound of ~96% | S2, S5 | proprietary | blocking | Apply conservative 85–90% range from D-T MCF literature [Araiinejad & Shirvan 2025] as central estimate; flag 2-year cycle as favorable structural driver |
| 6 | ECRH auxiliary power confirmed value | S2, S3, S5 | not-yet-sourced | important | Derivable once Q value is confirmed; watch for physics basis papers; upper bound is P_ECRH = 800/40 = 20 MW |
| 7 | 3D HTS coil winding feasibility demonstration | S3 | truly-unknown | blocking | Critical technology risk; watch for Type One Energy / CFS joint publications on stellarator coil manufacturing |
| 8 | Island divertor target lifetime at burning plasma conditions | S3 | truly-unknown | important | No data exists for island divertors at Infinity Two power levels; W7-X results at low power are only reference; dedicated engineering study needed |
| 9 | HCPB blanket module replacement interval and cost for stellarator geometry | S3, S5 | not-yet-sourced | important | EU-DEMO HCPB irradiation data (tokamak geometry) provides partial analog; stellarator non-axisymmetric adaptation not published |
| 10 | Beryllium pebble supply chain and cost at fusion plant scale | S4, S5 | not-yet-sourced | important | Materion Corp. and Heraeus produce Be pebbles for EU-DEMO TBM; scale-up to full plant supply chain not characterized; beryllium supply constraint shared with FLiBe-based designs |
| 11 | REBCO tape total demand for Infinity Two coil set | S4, S5 | derivable | important | Estimate from coil geometry (number × circumference × turns × tape width); W7-X coil geometry provides scaling reference; will require publication of Infinity Two coil detailed design |
| 12 | Remote maintenance system for non-axisymmetric stellarator geometry | S3 | proprietary / not-yet-sourced | important | W7-X remote handling experience provides partial basis; Infinity Two-scale remote system design not published |
| 13 | Li-6 enrichment level and Western supply pathway for HCPB pebbles | S4 | truly-unknown | important | COLEX banned under Minamata Convention; Western commercial Li-6 supply currently near-zero; ICOMAX frontrunner but decades to scale; natural lithium blanket alternative avoids enrichment but requires redesign; path-critical for HCPB deployment on Infinity Two timeline |
| 14 | Tritium extraction efficiency from HCPB over 2-year continuous cycle | S3, S5 | truly-unknown | important | No experimental data for HCPB tritium extraction over multi-year continuous operation; EU-DEMO program addressing this but not yet at demonstration scale |
| 15 | O&M cost breakdown (fixed + variable, scheduled + unplanned) | S2 | proprietary | important | No public data; steady-state operation eliminates disruption repair but adds island divertor target and HCPB pebble bed replacement as distinct O&M categories |
| 16 | Tritium startup cost under mid-2030s stockpile pressure scenario | S4, S5 | scenario-dependent | important | Pearson (2022) projects fusion demand begins depleting stockpile ~2035; Infinity Two mid-2030s target creates timing overlap; current $35,000/g pricing is a point estimate valid only under current supply conditions — should be modeled as a range |
| 17 | Divertor design selection — classical vs. LIBD — scenario branch not yet decided | S2, S3, S6 | truly-unknown | blocking | Design choice deferred to Infinity One results; classical is TRL 4–5 but exhaust efficiency 0.44–2.9% (marginal); LIBD is TRL 2–3 with 12.6% efficiency (unvalidated). Affects availability model (helium ash accumulation risk in classical case) and CAS22 capital (LIBD dome adds active cooling cost in constrained geometry). Model as two LCOE scenarios |
| 18 | Error field correction coil requirement at Infinity Two manufacturing scale | S2 | truly-unknown | important | Design uses m=5, n=4 island chain to avoid ι=1 resonances; correction coil techniques planned for Infinity One testing. If manufacturing-scale field errors require correction coils anyway, this is unbudgeted CAS22 capital with no published cost estimate. W7-X required such coils despite similar design intent |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis in the pipeline is the Spherical Tokamak - HTS (21-spherical-tokamak-hts, Tokamak Energy). This comparison is less direct than a stellarator-to-stellarator comparison would be, but shares the REBCO HTS supply chain and D-T fuel cycle.

**Reused assumptions from 21-spherical-tokamak-hts:**

- **REBCO tape cost and supply chain characterization**: Global production capacity (few thousand km/year), current pricing ($30–100/kA-m), and commercial viability target (~$10/kA-m) are adopted directly [analyses/21-spherical-tokamak-hts/analysis.md §Section 4]. The Infinity Two demand estimate (5,000–15,000 km) is larger than the ST-E1 estimate but uses the same pricing basis.
- **Tritium startup inventory and D-T supply constraints**: CANDU production baseline (~25–30 kg global inventory), 5.5%/year decay, ~1 kg startup requirement at >$35,000/g, and the sequencing constraint for fleet deployment are shared across all D-T concepts [analyses/21-spherical-tokamak-hts/analysis.md §Section 4].
- **Regulatory cost uncertainty**: The Stewart & Shirvan 2.2× building cost factor for fission-style regulation applies equally to Infinity Two as a D-T fusion plant.

**Key divergences from 21-spherical-tokamak-hts:**

- **Topology and physics basis**: Infinity Two is fundamentally different from a spherical tokamak — no plasma current, no disruptions, no ELMs in optimized operation, no current drive system, no central solenoid. These differences remove entire LCOE challenge categories (disruption damage, current drive recirculating power, pulsed thermal stress) while adding others (3D coil manufacturing, island divertor).
- **Blanket chemistry**: Infinity Two uses solid HCPB (Li₄SiO₄ + Be), not liquid lithium (ST-E1). HCPB is better characterized from EU-DEMO but introduces beryllium supply/toxicity concerns absent from the liquid lithium approach. HCPB has a higher TBR (1.30 vs. 1.2 for ST-E1) and a more developed engineering database.
- **Machine scale**: At R = 12.5 m, Infinity Two is physically 2.5× larger in major radius than ST-E1 (R = 5.0 m). This creates higher absolute capital cost but potentially better physics margins and higher thermal output (800 MW fusion vs. 1.5–2.5 GW estimated for ST-E1, but ST-E1's fusion power is unpublished).
- **Data availability**: Infinity Two is more documented than ST-E1 at the physics level (six peer-reviewed papers vs. four machine parameters for ST-E1). However, both lack published capital cost, LCOE estimates, and key engineering design details. The Phase 1a sources for Infinity Two are secondary (press releases, news articles); the JPP papers themselves are not yet extracted.
- **Steady-state vs. pulsed**: Infinity Two is genuinely steady-state; ST-E1 is quasi-pulsed (15+ minute pulses with dwell periods). Infinity Two's thermal output to BOP is constant — no thermal buffering system required — which simplifies BOP cost modeling and eliminates the thermal energy storage capital category present in ST-E1.

**Nearest-neighbor positioning:**
Infinity Two's closest analogs in this analysis pipeline are the in-progress stellarator concepts: 09-qi-stellarator-hts (Proxima Fusion — smaller QI stellarator with HTS, R = ~1.8 m) and 10-large-scale-stellarator (Gauss Fusion — large LTS+HTS stellarator, W7-X heritage, 40 coils). The Brown (2018) IEEE paper provides the best publicly available stellarator vs. tokamak vs. ST cost comparison framework and should be the primary independent reference for Infinity Two capital cost structure once those analyses are completed.

**Shared stellarator advantages for TEA pipeline representation:**
Stellarators as a class share cost structure features that differ systematically from tokamaks and should be captured in the TEA pipeline:
1. No current drive system capital or O&M cost
2. No central solenoid (saves a major capital item)
3. No disruption management system (saves capital; eliminates disruption repair O&M)
4. Island divertor as the distinct heat exhaust system (**cost penalty** relative to tokamak divertor — complex 3D target geometry with no published unit cost, high continuous heat flux over 2-year exposures, and no commercial supply chain; upward pressure on CAS22 capital and CAS70 O&M)
5. Complex 3D first wall and blanket geometry (higher manufacturing cost per unit area than axisymmetric)
6. Availability advantage from steady-state operation (no dwell periods, no pulsed thermal cycling of first wall)

---

## Section 8: Sources

**1. Dossier: QI Modular HTS Stellarator — Infinity Two (D-T)**
- Full citation: Phase 1a dossier, last updated 2026-03-07. Incorporates data from J. Plasma Phys. 2025 paper series (E65, E86, and baseline plasma physics paper).
- Contribution: Primary factual foundation for all high-confidence parameters (R, A, B, Q, fusion power, net electric, TBR, blanket type, heating method, operation mode, magnet type). Documents CFS partnership, DOE Frontier simulations, and W7-X heritage.
- Location: `knowledge/concept_research/20a-type-one-stellarator/dossier.md`

**2. Type One Energy Press Release — First Realistic Unified Fusion Power Plant Design Basis**
- Full citation: Type One Energy, "Type One Energy Issues First Realistic Unified Fusion Power Plant Design Basis." Available at: typeoneenergy.com (April 2025).
- Contribution: Confirms 800 MW fusion / 350 MWe net, Q > 40, steady-state operation, island divertors, HCPB blanket, advanced manufacturing methods, CFS partnership, DOE Frontier simulations. Primary public statement of design intent and economic positioning ("reasonable ONC," "good capacity factors and LCOE").
- Location: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/typeoneenergy-type-one-energy-issues-first-realistic.md`

**3. Modern Sciences — Type One Energy Fusion Pilot Plant Design Summary**
- Contribution: Secondary summary of Infinity Two design basis. Confirms 800 MW, Q = 40, 350 MWe, gas-cooled solid breeder blankets, island divertors. Points to underlying JPP papers for detail.
- Location: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/modernsciences-type-one-energy-fusion-pilot-plant-design.md`

**4. ANS Nuclear Newswire — April 1, 2025 (Article 6903)**
- Contribution: Brief announcement confirming publication of design basis. Notes "realistically considers the relationship between competing requirements for plasma performance, power plant startup, construction logistics, reliability, and economics utilizing actual power plant operating experience." Minimal additional technical content.
- Location: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/ans-news-2025-04-01-article-6903.md`

**5. J. Plasma Phys. 2025, E65 — Comprehensive Unified Baseline Physics Design**
- Full citation: Author(s) not available from extracted sources. "A comprehensive unified baseline physics design for the Type One Energy stellarator fusion pilot power plant Infinity Two." *Journal of Plasma Physics*, 2025, E65. Cambridge University Press. doi: [referenced in dossier.md]
- Contribution: Primary technical reference for machine parameters (R = 12.5 m, A = 10, Q > 40, 800 MW), ECRH-only heating, 4-field-period QI/maximum-J configuration. Not available as extracted text in Phase 1a sources.
- Location: Referenced in dossier; paper at Cambridge University Press DOI listed in dossier §Key Sources

**6. J. Plasma Phys. 2025, E86 — Breeder Blanket and Tritium Fuel Cycle Feasibility**
- Full citation: Clark et al. (assumed; first author not confirmed from available sources). "Breeder blanket and tritium fuel cycle feasibility of the Infinity Two fusion pilot plant." *Journal of Plasma Physics*, 2025, E86. Cambridge University Press.
- Contribution: TBR = 1.30 confirmed by OpenMC Monte Carlo with 300 million particle histories. HCPB blanket with Li₄SiO₄/Li₂TiO₃ pebbles and Be multiplier. FLiBe considered for shielding-primary zones. Not available as extracted text in Phase 1a sources.
- Location: Referenced in dossier §Tritium Breeding and §Key Sources

**7. Brown, T.G. (2018) — Three Confinement Systems Cost Comparison**
- Full citation: Brown, T.G. (2018) "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements." *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148.
- Contribution: Reference framework for stellarator capital cost decomposition by component category. The only published comparative cost analysis covering stellarator configuration. Essential for constructing an Infinity Two cost model in the absence of a plant study.
- Location: Referenced in approved analysis 21-spherical-tokamak-hts and handwritten exemplar 01-hts-compact-tokamak.md

**8. ARIES-CS Study (late 1990s–early 2000s)**
- Full citation: ARIES Team, "ARIES-CS Compact Stellarator Fusion Power Plant" study. University of California San Diego / ARIES Project. Available at: qedfusion.org/DOCS/bib.shtml
- Contribution: Most detailed publicly available stellarator power plant cost study. Plant capital breakdown, magnet system cost fraction, blanket costs, maintenance scheme for a compact stellarator. Design point differs from Infinity Two (compact, lower aspect ratio) but provides the primary independent reference for stellarator cost structure.
- Location: Referenced in handwritten exemplar 01-hts-compact-tokamak.md and cross-concept memory

**9. Araiinejad, L.S. and Shirvan, K. (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants." *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: Capacity factor uncertainty ranges (75–90%), regulatory cost scenarios, and FLiBe cost estimates for D-T MCF plants. Applied here as a proxy for missing Infinity Two availability and cost parameters.
- Location: Referenced in handwritten exemplar 01-hts-compact-tokamak.md

**10. Approved D1+ Analysis: Spherical Tokamak – HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for REBCO tape supply chain characterization (pricing, global capacity, commercial viability target), D-T tritium supply constraints, and regulatory cost scenarios. Used to anchor shared supply chain parameters for Section 4.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`
