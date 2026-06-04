# D1+ Analysis: Spherical Tokamak - HTS (Tokamak Energy)

**Concept**: Spherical Tokamak with HTS magnets — D-T fuel
**Company**: Tokamak Energy (Oxford, UK; US and Japan subsidiaries)
**Pilot Plant**: ST-E1 Revision D (final pre-conceptual design point, DPP 2025)
**Confinement Family**: MFE — Spherical Tokamak

---

## Section 1: Availability of Data

**Rating: Limited**

Tokamak Energy is materially less transparent than Commonwealth Fusion Systems. After three research iterations, the ST-E1 Revision D design is characterized by four published machine parameters (R = 5.0 m, A = 2.3, B = 5.25 T on-axis, TBR = 1.2) and one output range (450–750 MWe net), but fusion power, Q value, plasma current, heating power, thermal efficiency, and capital cost remain unpublished. The "Limited" rating reflects that Tokamak Energy publishes enough to confirm the concept and machine geometry, but not enough to anchor a closed LCOE model without extensive analogue assumptions.

**Published machine design documentation:**
The ST-E1 Revision D parameters were disclosed at APS DPP 2025 by Erik Maartensson in an overview talk [tokamak-energy-st-e1-dpp2025-abstract.md]. This abstract is the primary engineering reference: it confirms the final pre-conceptual design point, documents design evolution methodology (two-week cycles → two-month iterations → one six-month iteration), and notes that maintenance scheme implications were addressed early in the design process. The DPP 2024 talk disclosed an earlier design with A=2.0, R=4.25 m, 85 MWe net — substantially different from the current point, indicating the concept is still in active development [tokamak-energy-st-e1-design-evolution.md].

**Component-level publications:**
- Alieva et al. (EPJ Web of Conferences 2026) provides the most technically detailed ST-E1 subsystem paper in the public domain: ray-tracing simulation results for EC current drive efficiency across three plasma scenarios, confirming that O-mode ECRH can serve as the sole auxiliary source during flat-top operation [tokamak-energy-ec-heating-pilot-plant.md]. This is a peer-reviewed publication from Tokamak Energy's internal RF physics team.
- Demo4 HTS magnet system (November 2025 press release): validated complete 14 TF + 2 PF coil set at 11.8 T, 30 K, with 7 million ampere-turns through the center column. This is a world-first for a complete HTS coil set in tokamak configuration, going beyond single-coil demonstrations [tokamak-energy-demo4-magnets.md].
- Humphry-Baker & Smith (2019), *Philosophical Transactions of the Royal Society A*, provides the only detailed published analysis of center-stack neutron shielding for a compact spherical tokamak. The co-author (G.D.W. Smith) was affiliated with Tokamak Energy, making this a semi-authoritative source for shielding design [spherical-tokamak-center-stack-shielding.md].
- Gryaznevich et al. (MDPI 2023) establishes the physics case for pulsed spherical tokamak reactors and documents the advantages of quasi-steady operation for ST geometry [pulsed-spherical-tokamak-paper.md].

**Independent analyses of the spherical tokamak concept family:**
The UKAEA has conducted the most quantitative independent work. Foster et al. (2024) developed a framework for extrapolating costs to commercial fusion power plants including spherical tokamak variants [referenced in handwritten exemplar 01-hts-compact-tokamak.md]. Hidalgo-Salaverri et al. (2025) published a full techno-economic analysis and cost-driver sensitivity study for spherical tokamaks for hybrid hydrogen-electricity production in *Nuclear Fusion* [referenced in handwritten exemplar]. Brown (2018, *IEEE Transactions on Plasma Science*) provides a comparative cost decomposition across spherical tokamak, standard tokamak, and stellarator geometries — a direct reference framework for the ST-E1 capital cost structure [referenced in handwritten exemplar]. The PROCESS system code (UKAEA) includes a spherical tokamak physics model that can generate self-consistent design points for LCOE estimation [referenced in handwritten exemplar].

**Company transparency:**
Tokamak Energy publishes roadmap milestones, machine photos, press releases, and experimental results from ST40, but stops well short of the detail needed for an LCOE model. Published items: $335M funding ($275M private, $60M government UK+US), ~280-person staff, DOE Milestone-Based Fusion Development Program participation (May 2023 selection), ST80-HTS build completion target of 2026, ST-E1 grid connection target of "early 2030s" (now realistically mid-2030s) [tokamak-energy-overview.md, tokamak-energy-roadmap.md]. Not published: cost estimates, capacity factor targets, detailed blanket design, Q value, or any form of plant study.

**Phase 1a dossier completeness:**
The Phase 1a dossier achieved high confidence on confinement family, confinement concept, fuel, magnet type, tritium breeding, neutron management, and operation mode. Medium confidence remains on energy capture (thermal cycle undisclosed) and plasma state (burning plasma inferred but Q unpublished). After three research iterations, these medium-confidence items are confirmed as proprietary or unpublished — further iterations will not resolve them without direct company disclosure.

**Key data gaps limiting this analysis:**
1. Q value and fusion power — fundamental inputs to any LCOE model — are not publicly available
2. Thermal efficiency and power conversion cycle choice undisclosed
3. Auxiliary heating power for ST-E1 not stated
4. No published capital cost estimate or capacity factor target
5. Liquid lithium blanket engineering details not documented beyond TBR=1.2 and "outboard-only"

---

## Section 2: Challenges in Capturing System Function

The Spherical Tokamak - HTS shares several LCOE modeling challenges with conventional D-T tokamaks, but adds a set of geometry-specific constraints that are harder to address with published data. Challenges are ranked by LCOE impact.

**1. Unknown fusion power and Q — the model has no physics anchor (Impact: Critical)**

Net electric output of 450–750 MWe is published, but fusion power is not. To derive fusion power, one must assume: (a) thermal-to-electric conversion efficiency (undisclosed; STEP-related ST research evaluates steam Rankine, hybrid steam-ORC, and sCO2 Brayton, none committed for ST-E1 [ste1-pilot-plant-specs.md]), (b) recirculating power fraction (depends on auxiliary heating power, which is undisclosed), and (c) cryogenic and pumping loads. With a 30–40% thermal efficiency assumption and central estimate of ~600 MWe net, gross electric is roughly 800–900 MWe, implying fusion power of ~1.5–2.5 GW depending on recirculating fraction. The Q value, if burning plasma (Q >> 1), implies heating power of tens of MW. This full chain involves at least three unanchored assumptions and produces very wide uncertainty. The gap is more constraining than for CFS, where Sorbom et al. (2015) published the complete plasma parameter set.

**2. Outboard-only blanket: incomplete coverage and unusual tritium extraction (Impact: High)**

The ST-E1 outboard-only liquid lithium blanket is a direct consequence of spherical tokamak geometry: the compact center stack (~32 cm of available radial space [spherical-tokamak-center-stack-shielding.md]) cannot accommodate a breeding blanket. Only the outboard hemisphere is available for neutron capture and tritium breeding. Achieving TBR = 1.2 with ~50% solid-angle coverage requires either high Li-6 enrichment (to maximize breeding per unit area) or thick outboard blanket geometry. The 1.2 TBR target is published, but the engineering design that achieves it is not. The use of liquid lithium (Li metal, not FLiBe) as the breeder creates distinct engineering challenges: Li metal is chemically reactive with water and oxygen, requiring inert atmosphere operations; tritium extraction from liquid metal differs mechanically from FLiBe vacuum degassing; and Li metal has different tritium permeation behavior through structural materials. The Pb-17Li blanket program (ITER, EU-DEMO) provides partial analogs, but pure Li metal is more reactive and the relevant operational database at fusion scale is sparse.

**3. ECRH-only flat-top heating: high recirculating power and efficiency limits (Impact: High)**

The ST-E1 flat-top is designed to use EC waves exclusively as the auxiliary source [tokamak-energy-ec-heating-pilot-plant.md]. Gyrotrons achieve ~50–55% wall-plug efficiency at current generation. For a pilot plant needing tens of MW of ECRH, the recirculating power from the heating system alone is a significant fraction of gross electric. This contrasts with NBI (~60–70% wall-plug efficiency) or with the bootstrap-current-dominated, low-auxiliary-power design of some high-Q concepts. The ECRH-only choice simplifies the plasma physics (no beam-driven rotation, no NBI-first-wall interactions) but creates a higher recirculating power cost. Without published auxiliary heating power, the recirculating fraction cannot be calculated, and Q_engineering remains unknown. This is a material LCOE uncertainty specific to the Tokamak Energy approach.

**4. Pulsed operation: thermal energy storage and plasma restart costs (Impact: Moderate)**

Pulse lengths of 15+ minutes are described as "more desirable than steady-state" for spherical tokamaks due to limited CS flux [pulsed-spherical-tokamak-paper.md]. Each pulse cycle includes: ramp-up (inductive current drive from CS), flat-top (ECRH current drive), and ramp-down; followed by a dwell period for CS re-magnetization. The dwell period represents downtime and wear on heating/current-drive systems. Pulsed operation requires thermal energy storage (e.g., molten salt buffer) between pulses to maintain steady grid output [ste1-pilot-plant-specs.md]. This buffer system is a capital cost without equivalent in steady-state designs and is not dimensioned or costed in any public ST-E1 document. Plasma restart stress on divertor targets and first wall (due to disruption risk during ramp-up) also reduces effective availability. The DPP 2025 abstract explicitly notes that "demonstrated compatibility with reactor-level performance and availability factor" was achieved in design, but no numerical target is given. The central-case LCOE model therefore adopts the canonical 0.85 availability for MCF quasi-steady D-T concepts (scoring_framework.md §Plant availability); pulsed-operation downside risk is captured via sensitivity sweeps rather than a concept-specific override.

**5. Center stack durability under neutron irradiation (Impact: Moderate)**

The center stack must protect HTS tape from radiation damage within ~32 cm of shielding radial depth. Humphry-Baker & Smith (2019) studied this for a smaller device (R = 1.35 m) and identified WC-FeCr cermet as the optimal shielding material, projecting fast neutron flux of ~1.4 × 10¹⁷ m⁻² s⁻¹ into the superconducting core after 32 cm of shielding [spherical-tokamak-center-stack-shielding.md]. However, irradiation damage behavior of WC cermets under fusion-relevant 14 MeV neutrons is not well characterized — this gap was explicitly flagged in the original paper. REBCO tape critical current degrades under neutron irradiation; the allowable flux threshold and its implications for center stack shielding design at ST-E1 scale have not been published. This introduces uncertainty in both magnet performance lifetime and center stack replacement schedule.

**6. Capital cost structure: compact vs. large-machine trade-off (Impact: Moderate)**

The spherical tokamak's economic case relative to a conventional aspect-ratio tokamak (and to the CFS compact high-field approach) rests on the claim that higher beta compensates for lower field, enabling adequate fusion power at moderate magnetic stress. Brown (2018) provides quantitative cost comparisons across ST, conventional tokamak, and stellarator configurations for several major cost elements. However, no published cost study has been done for the specific ST-E1 Revision D geometry with REBCO HTS magnets. The capital cost of the ST-E1 outboard blanket, center stack, and divertor — which differ substantially in design from either ITER-class or ARC-class devices — is entirely uncharacterized in the public literature.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk to LCOE model) to most mature.

---

**Outboard-Only Liquid Lithium Breeder Blanket — TRL 2–3**

- **Demonstrated**: Small-scale liquid lithium flow experiments. The EU-DEMO Pb-17Li blanket program provides partial analogy for liquid-metal tritium breeding. ITER Test Blanket Module (TBM) program includes Li-containing concepts. ARIES studies have modeled liquid-Li blanket configurations. Tokamak Energy confirms outboard-only liquid Li with TBR = 1.2 but has not published engineering details [tokamak-energy-st-e1-dpp2025-abstract.md].
- **On paper only**: Complete outboard-only liquid Li blanket achieving TBR = 1.2 with the outboard coverage constraint of spherical tokamak geometry. Tritium extraction system for liquid Li at kg/day throughput. Li metal handling systems (inert atmosphere, chemical compatibility with structural materials) at fusion plant scale. Thermal hydraulics of Li metal blanket under fusion neutron + gamma heating.
- **Missing at scale**: 14 MeV neutron irradiation of liquid Li blanket structural materials at fusion-relevant fluences. Tritium permeation characterization from Li metal through structural alloys at blanket operating temperatures. Li metal/structural alloy compatibility under long-term thermal and radiation exposure. Full TBR validation with realistic neutron spectrum including blanket penetrations, supports, and diagnostics reducing effective coverage below 50% solid angle.

---

**Center Stack Neutron Shielding (WC Cermet) — TRL 3–4**

- **Demonstrated**: WC-based cermets manufactured and mechanically characterized under non-radiation conditions. Humphry-Baker & Smith (2019) experimentally validated WC-FeCr properties (10× higher flexural strength than pure W, 3–4× better thermal shock resistance) and performed neutron transport modeling for a small spherical tokamak geometry [spherical-tokamak-center-stack-shielding.md]. Concept is well-developed in the literature.
- **On paper only**: Irradiation performance of WC cermet under 14 MeV fusion neutrons at relevant dose rates. Hydrogen (tritium) trapping in WC cermet and its implications for tritium inventory and permeation. Thermal-mechanical performance of the five-layer concentric annular shield design during pulsed operation (thermal cycling + neutron heating).
- **Missing at scale**: WC cermet production at nuclear-grade purity and scale for a complete center stack shield. Long-term irradiation database under fusion neutron spectrum. Validated neutron transport model for ST-E1 geometry specifically (Humphry-Baker & Smith studied R = 1.35 m; ST-E1 is R = 5.0 m with a larger center stack, but similar radial shielding constraint of ~32 cm for HTS coil protection). Tritium accountability in the center stack shielding volume.

---

**Tritium Fuel Cycle (Liquid Li Circuit) — TRL 3–4**

- **Demonstrated**: Lab-scale tritium handling loops. JET and TFTR operated gram-level tritium inventories. The EU Pb-17Li program has demonstrated tritium extraction from lead-lithium at lab and semi-industrial scale, providing a partial analogy. Tritium breeding from Li-6 is well-understood physics. ST-E1 TBR = 1.2 is consistent with a self-sufficient fuel cycle with margin [dossier.md; tokamak-energy-st-e1-dpp2025-abstract.md].
- **On paper only**: Closed-loop liquid Li tritium breeding and extraction at kg/day rates for a commercial plant. Continuous tritium extraction from circulating Li metal at elevated temperatures. Near-zero permeation of tritium through Li metal heat exchanger surfaces (tritium permeation through steel from liquid Li is a documented concern in fission breeder reactor research).
- **Missing at scale**: Industrial-scale tritium processing for a liquid Li-based fusion plant. Tritium accountability in a Li metal primary circuit. Tritium permeation barriers for Li metal-facing heat exchangers (different challenge than FLiBe-facing materials). Demonstrated TBR > 1.0 in operating conditions for an outboard-only blanket with realistic penetrations and access ports.

---

**Remote Maintenance System — TRL 5–6**

- **Demonstrated**: ITER remote handling prototypes at full scale. Spherical tokamak geometry creates different (and in some ways more challenging) access requirements than a conventional tokamak — the compact center stack and limited inboard clearance constrain maintenance approach. The DPP 2025 abstract explicitly states that "maintenance scheme and its implications on other systems was an early-stage priority" in the ST-E1 design methodology, indicating early integration of maintenance constraints [tokamak-energy-st-e1-dpp2025-abstract.md].
- **On paper only**: ST-E1-specific remote maintenance scheme for outboard blanket module extraction, center stack assembly maintenance, divertor replacement, and ECRH antenna servicing. Full maintenance cycle time needed to achieve target availability.
- **Missing at scale**: Validated remote maintenance cycle for activated outboard blanket modules in ST-E1 geometry. Center stack maintenance tooling that can access the compact inboard region. Radiation-hardened robotics for the specific geometric constraints of a spherical tokamak. Neutron activation inventory and waste volume estimates for the remote maintenance cycle.

---

**ECRH Heating and Current Drive at Pilot Plant Scale — TRL 5–7**

- **Demonstrated**: ST40 operating with 1 MW Kyoto Fusioneering gyrotron at 104/137 GHz (installed 2025) alongside NBI [st40-heating-systems.md, tokamak-energy-heating-systems.md]. ITER uses 170 GHz, 1 MW CW gyrotrons (multiple installed or in final testing). Alieva et al. (EPJ 2026) performed ray-tracing simulations across three plasma scenarios for ST-E1, optimizing ECCD efficiency ζ_ECCD in O-mode polarization [tokamak-energy-ec-heating-pilot-plant.md]. ECRH current drive is well-understood in conventional aspect-ratio tokamaks; application to spherical tokamak geometry (lower field, higher beta, different accessibility windows) has been studied theoretically.
- **On paper only**: Multi-tens-of-MW ECRH installation on ST-E1. Demonstrated ECCD efficiency sufficient to maintain quasi-steady-state operation for 15+ minute flat-tops in a burning plasma. Validated that O-mode ECCD drives sufficient current to maintain plasma current at flat-top without CS contribution.
- **Missing at scale**: Long-term, continuous-wave gyrotron reliability at plant-relevant power levels and cycle times. ECRH antenna/launcher designs surviving the neutron and gamma environment in a burning plasma ST. Validated ECCD current drive efficiency in a fusion-power-density plasma (all existing ECCD data is from non-burning plasmas). Recirculating power fraction quantification once auxiliary heating power target is established.

---

**HTS Magnets (REBCO TF/PF Coil System) — TRL 6–8**

- **Demonstrated**: Demo4 completed November 2025 — complete 14 TF + 2 PF HTS coil set achieved 11.8 T at 30 K, with 7 million ampere-turns through the center column [tokamak-energy-demo4-magnets.md]. This is a world-first for a complete HTS coil system in tokamak configuration (CFS had demonstrated a single 20 T coil in 2021; Tokamak Energy's Demo4 validated the complete magnet architecture). REBCO HTS delivers ~200× the current density of copper. The 11.8 T at-coil field is consistent with the 5.25 T on-axis target for ST-E1 (field falls as 1/R from the coil winding to the plasma axis at R = 5.0 m). ST-E1 operates at a lower field than CFS designs, reducing mechanical stress and reducing REBCO tape performance requirements.
- **On paper only**: Full ST-E1 TF coil system at the larger scale (R = 5.0 m, 14 TF coils of plant scale vs. Demo4 scale). Quench protection system for the complete magnet set in a neutron environment. Long-term magnet performance under combined radiation + cyclic thermal loads over a multi-year plant lifetime.
- **Missing at scale**: REBCO tape performance under cumulative 14 MeV neutron + gamma irradiation at the ST-E1 center stack neutron flux levels. Quench detection and energy extraction for a complete HTS system in fusion environment. Insulation systems for radiation resistance in the HTS coil package. Supply chain scale-up for the REBCO tape length required for a full ST-E1 coil set.

---

**Divertor — TRL 5–7**

- **Demonstrated**: Tungsten monoblock divertors tested at >10–20 MW/m² in WEST, GLADIS, and DTT facilities. Spherical tokamak divertor physics is particularly relevant to MAST-U's Super-X divertor program (UKAEA/Culham), which has demonstrated dramatically reduced divertor heat loads via extended divertor leg geometry. MAST-U and NSTX-U provide the most directly relevant ST divertor physics databases [tokamak-energy-roadmap.md; dossier.md].
- **On paper only**: Advanced ST divertor design at pilot plant heat flux levels (~5–20 MW/m² depending on radiation fraction). Detachment control in a burning plasma ST with high-recycling divertor conditions.
- **Missing at scale**: Validated detachment regime for ST-E1 plasma parameters (high current, high density, high heating power). Remote replacement system for a compact ST divertor geometry. Tungsten divertor lifetime under combined neutron damage + heat load for multi-year replacement intervals.

---

**Balance of Plant (Power Conversion, Thermal Buffering) — TRL 7–9 (BOP) / TRL 4–5 (Thermal Buffer)**

- **Demonstrated**: Conventional steam Rankine and sCO2 Brayton cycles at GW scale are commercially mature. STEP (Spherical Tokamak for Energy Production, UKAEA) has evaluated steam Rankine, hybrid steam-ORC, and sCO2 for spherical tokamak applications — providing indirect relevance [ste1-pilot-plant-specs.md]. Molten salt thermal energy storage (the leading candidate for pulsed tokamak buffering) is commercially deployed in concentrated solar power plants.
- **On paper only**: Integration of a thermal buffer with a pulsed (~15 min on/~5 min off) fusion heat source at 450–750 MWe scale. Sizing and cost of the thermal buffer system for ST-E1 pulse characteristics.
- **Missing at scale**: Integration with tritium-compatible heat exchangers between liquid Li primary loop and secondary working fluid. Confirmed power conversion cycle selection for ST-E1 (not yet committed). Thermal buffer sizing for actual ST-E1 pulse length and dwell time (not yet published). Capital cost of thermal buffering system — a cost category absent from steady-state concept LCOE models.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck, Shared with HTS Compact Tokamak**

Global REBCO production capacity is on the order of a few thousand kilometers per year across all manufacturers. The Tokamak Energy Demo4 system (14 TF + 2 PF coils) is a magnet set, not a full ST-E1 plant; the complete pilot plant magnet system will require substantially more tape. The ST-E1 design operates at lower on-axis field (5.25 T) than CFS ARC (9.2 T), meaning lower required critical current density per unit tape length, but the larger machine geometry (5.0 m major radius vs. ARC's 3.3 m) partly offsets this — total tape demand for ST-E1 is on the order of thousands to tens of thousands of km, comparable in scale to other HTS tokamak designs. Tape cost at the current $30–100/kA-m range [handwritten exemplar 01-hts-compact-tokamak.md] needs to fall toward ~$10/kA-m or lower for commercial viability. Key REBCO producers include Shanghai Superconductor Technology, Faraday Factory Japan, and CFS's own tape manufacturing effort. Supply chain is ramping but has not yet demonstrated the volume needed for even a first commercial plant, let alone a fleet.

**Liquid Lithium (Li Metal) — Different Chemistry from FLiBe, Commercially Available but Fusion-Scale Unproven**

Liquid lithium (as opposed to FLiBe molten salt used in ARC) is the ST-E1 blanket and tritium breeding medium. Lithium metal is commercially available at scale (driven primarily by battery demand), making raw material supply less constrained than FLiBe. However, liquid lithium breeding at fusion plant scale introduces distinct challenges:
- **Chemical reactivity**: Li metal reacts exothermically with water and air, requiring fully inert atmosphere operations throughout the primary circuit. This creates different structural and operational requirements than FLiBe.
- **Li-6 enrichment**: Natural lithium is ~7.5% Li-6. Breeding TBR ≥ 1.2 with outboard-only coverage likely requires moderate-to-high Li-6 enrichment. Li-6 enrichment capacity is limited globally (primary producers in Russia and China use legacy mercury amalgam processes; Western alternatives are being developed but are not at commercial scale for fusion demand).
- **Tritium extraction**: Different from FLiBe extraction — tritium solubility in liquid Li varies strongly with temperature; extraction requires vacuum degassing or selective permeation membrane systems, neither demonstrated at fusion-plant throughput for pure Li metal systems.
- **Supply chain for fusion**: Unlike FLiBe (which requires scarce beryllium), liquid Li does not require beryllium, removing one supply constraint. But the specific Li-6-enriched liquid Li metal circuit represents a novel industrial system with no prior deployment at this scale.

**Tungsten Carbide Cermet (Center Stack Shielding) — Specialized Material, Thin Irradiation Database**

WC-FeCr cermet is identified as the optimal center stack shielding material based on its mechanical and thermal shock properties [spherical-tokamak-center-stack-shielding.md]. It is not currently produced at nuclear-grade purity or in the quantities needed for a pilot plant center stack. More critically, the irradiation damage behavior of WC cermets under fusion-relevant 14 MeV neutron spectra is explicitly characterized as "not well characterized" in the source paper. This represents both a supply chain gap (no industrial process for nuclear-grade WC cermet production) and a materials qualification gap (no irradiation database at fusion neutron energies). Unlike tungsten for divertor tiles (where extensive fission reactor and 14 MeV-source irradiation data exist), WC cermet has not been studied in a fusion-relevant environment.

**Tritium — Declining External Supply (Shared D-T Constraint)**

The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU heavy-water reactor byproduct, and decays at 5.5%/year [handwritten exemplar 01-hts-compact-tokamak.md]. A single D-T reactor startup requires ~1 kg at >$35,000/g. The outboard-only blanket design with TBR = 1.2 provides adequate breeding margin if the outboard design performs as modeled, but the asymmetric blanket geometry creates more sensitivity to local coverage gaps (maintenance ports, diagnostics, divertor openings) than a 4π blanket design. As CANDU reactors retire, the external tritium supply will shrink, creating the same sequencing constraint as for all D-T concepts: early plants must demonstrate self-sufficiency before fleet scaling is feasible.

**Tungsten (First Wall and Divertor) — Supply Adequate, Manufacturing Challenges Remain**

Tungsten for the first wall and divertor is available in adequate global supply. The manufacturing challenges (large-area tungsten tiles, thermal fatigue resistance, remote-weldable attachment systems) are shared with other D-T tokamak designs and are actively being addressed in the ITER divertor program. Not a supply bottleneck; a manufacturing quality challenge.

**No Beryllium Required (Unlike FLiBe-Based Designs)**

Unlike ARC (which uses FLiBe containing beryllium), the Tokamak Energy liquid Li blanket uses no beryllium as a primary material. This removes one supply chain constraint [handwritten exemplar 01-hts-compact-tokamak.md notes beryllium is produced in limited quantities globally, ~300 tonnes/year, dominated by Materion Corp.]. The center stack WC cermet also uses no beryllium. This is a modest but real supply chain advantage over FLiBe-based blanket designs.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output | 450–750 MWe | APS DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | Revision D final pre-conceptual design point; range reflects physics and technology assumptions |
| Major radius | 5.0 m | DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | Revision D; up from 4.25 m in Oct 2024 design |
| Aspect ratio | 2.3 | DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | At upper boundary of "spherical tokamak"; less compact than initial A=2.0 design |
| On-axis toroidal field | 5.25 T | DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | Lower than CFS ARC (9.2 T) and SPARC (12.2 T); consistent with lower-B ST physics regime |
| Tritium breeding ratio | 1.2 | DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | Outboard-only liquid Li blanket; provides self-sufficiency margin |
| Blanket type | Outboard-only liquid lithium | DPP 2025 abstract [tokamak-energy-st-e1-dpp2025-abstract.md] | high | Inboard side limited to WC cermet shielding for center stack protection |
| Operation mode | Quasi-steady (15+ min pulses) | Gryaznevich et al. MDPI 2023 [pulsed-spherical-tokamak-paper.md]; ST80-HTS roadmap [tokamak-energy-roadmap.md] | high | Pulsed operation described as "more desirable than steady-state" for ST geometry |
| Plant availability (central case) | 0.85 | Canonical per scoring_framework.md §Plant availability (MCF quasi-steady, D-T); previously 0.80 | medium | Policy-driven canonical value — no concept-specific published target; pulsed-operation downside captured in sensitivity sweeps; cross-concept MCF LCOE comparisons are apples-to-apples on this dimension |
| Center stack shielding radial depth | ~32 cm | Humphry-Baker & Smith 2019 [spherical-tokamak-center-stack-shielding.md] | medium | Studied for smaller device (R=1.35 m); ST-E1 at R=5.0 m has more space but same architectural constraint |
| Fast neutron flux into SC core (after shielding) | ~1.4 × 10¹⁷ m⁻² s⁻¹ | Humphry-Baker & Smith 2019 [spherical-tokamak-center-stack-shielding.md] | medium | Through 32 cm WC shield; for smaller device; ST-E1 values not published |
| Demo4 magnet system field | 11.8 T at 30 K | Demo4 press release Nov 2025 [tokamak-energy-demo4-magnets.md] | high | Complete 14 TF + 2 PF coil set; 7 million ampere-turns through center column |
| Plasma current (pre-RevD disruption paper) | 13.6 MA | arxiv:2512.16604 cited in [tokamak-energy-st-e1-dpp2025-abstract.md] | medium | Pre-Revision D parameters (R=4.25 m, A=2.15); may not match Revision D |
| Primary heating method (flat-top) | ECRH only (O-mode) | Alieva et al. EPJ Web of Conferences 2026 [tokamak-energy-ec-heating-pilot-plant.md] | high | Ray-tracing simulations across 3 scenarios; paper confirms EC as sole flat-top source |
| ST40 operational ECRH | 1 MW gyrotron (104/137 GHz) | Kyoto Fusioneering delivery Jan 2025 [st40-heating-systems.md] | high | Tunable-frequency; NBI + ECRH combined on ST40 |
| Total company funding | $335M ($275M private, $60M government) | Tokamak Energy overview [tokamak-energy-overview.md] | high | As of 2024 data |
| Thermal efficiency | [inferred] ~30–38% | [analogue — STEP programme ST thermal cycle studies; steam Rankine basis] | low | CPS has not committed to a cycle; STEP evaluates steam Rankine, hybrid ORC, and sCO₂ for ST; ST-E1 likely in same range |
| Fusion power (derived estimate) | [estimated] ~1.5–2.5 GW | [estimated from 450–750 MWe net, assumed 30–38% thermal efficiency, assumed recirculating fraction ~15–20%] | low | Requires three unanchored assumptions; very wide uncertainty band |
| Q value | [inferred] burning plasma | [inferred from power output targets] | low | Q deliberately unpublished; 450–750 MWe net implies high Q; burning plasma state probable |
| Gyrotron wall-plug efficiency | ~50–55% | [analogue — ITER-class gyrotron performance data] | medium | Standard CW gyrotron efficiency; sets floor for ECRH recirculating power fraction |
| REBCO tape cost (current market) | $30–100/kA-m | Whyte 2024; handwritten exemplar [01-hts-compact-tokamak.md] | medium | Wide range reflects supplier variation; target is ~$10/kA-m for commercial viability |
| Tritium market price | >$35,000/g | Handwritten exemplar [01-hts-compact-tokamak.md] | medium | Approximate current market |
| Regulatory cost multiplier (fission-style scenario) | 2.2× building cost | Stewart & Shirvan 2022; cited in [01-hts-compact-tokamak.md] | medium | Upper-bound scenario for all D-T fusion concepts |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value / fusion gain | proprietary | blocking | Not disclosed after 3 research iterations; burning plasma inferred from power targets; needed to derive auxiliary heating power and recirculating fraction |
| Fusion power (gross thermal) | proprietary | blocking | Net electric given but fusion power derivation requires thermal efficiency and recirculating power, both unknown; estimated range ~1.5–2.5 GW has very wide uncertainty |
| Power conversion cycle type and thermal efficiency | proprietary | blocking | Steam Rankine vs. sCO₂ Brayton not committed by Tokamak Energy; STEP-related research explores both; cycle choice affects both efficiency and heat exchanger materials |
| Auxiliary heating power for ST-E1 | proprietary | blocking | ECRH total MW for flat-top not disclosed; determines recirculating power fraction and Q_engineering |
| Plant capacity factor | proprietary | important | Not published; central case adopts canonical 0.85 per scoring_framework.md §Plant availability (MCF quasi-steady, D-T); pulsed operation (dwell periods for CS re-magnetization) creates downside risk relative to steady-state designs, tested in sensitivity sweeps |
| Overnight capital cost ($/kWe or total $M) | proprietary | blocking | No public cost estimate for ST-E1; no plant study analogous to ARIES-ST or PROCESS-based design for the specific ST-E1 Rev D parameters |
| Component replacement schedule | proprietary / not-yet-sourced | important | Outboard blanket, center stack, and divertor replacement intervals needed for availability and maintenance cost estimates |
| ECRH recirculating power fraction (Q_engineering) | derivable | important | Derivable once auxiliary heating power is known; formula: Q_eng = (P_fusion × η_blanket × η_thermal) / (P_fusion × η_blanket × η_thermal − P_aux / η_gyrotron); currently not calculable |
| Plasma current (Revision D) | not-yet-sourced | important | Disruption paper value of 13.6 MA uses pre-Revision D parameters; Revision D Ip not yet published |
| Liquid Li tritium extraction rate and efficiency | truly-unknown | important | No published design or experimental data for Li metal tritium extraction at plant scale for a fusion application; Pb-17Li analogy is partial |
| Center stack neutron flux and shielding performance at ST-E1 scale | not-yet-sourced | important | Humphry-Baker & Smith (2019) studied R=1.35 m device; ST-E1 at R=5.0 m has different neutron source term and center stack geometry; scaling not published |
| WC cermet irradiation database under fusion neutrons | truly-unknown | important | Explicitly identified as a gap in Humphry-Baker & Smith (2019); no 14 MeV irradiation data for WC-FeCr cermet in public domain |
| REBCO tape quantity required for ST-E1 magnet system | proprietary / derivable | important | Can be estimated from coil geometry; not published by Tokamak Energy; Demo4 coil dimensions not detailed enough to scale to ST-E1 |
| Thermal energy storage sizing and cost | truly-unknown | important | Required for pulsed operation grid output smoothing; no design or cost estimate for ST-E1 pulse characteristics |
| Li-6 enrichment level for TBR=1.2 with outboard-only geometry | derivable | nice-to-have | Can be estimated from neutronics if blanket thickness and geometry are known; sets Li supply chain requirements |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q value not published — blocks derivation of auxiliary heating power and Q_engineering | S1, S2, S5 | proprietary | blocking | Watch for ST-E1 plasma performance publications at DPP 2026 or future peer-reviewed paper; PROCESS model run with published machine parameters could provide estimate |
| 2 | Fusion power (gross) unknown — requires three unanchored assumptions to estimate | S1, S2, S5 | proprietary | blocking | Derivable from published parameters using PROCESS or similar code once plasma current or Q is known |
| 3 | Power conversion cycle type and efficiency not committed | S1, S2, S5 | proprietary | blocking | Use steam Rankine ~32–35% as default assumption based on STEP-related ST research; flag as unconfirmed |
| 4 | Auxiliary ECRH power for ST-E1 not disclosed — recirculating power unknown | S2, S3, S5 | proprietary | blocking | Apply ECCD scaling from Alieva et al. (2026) to estimate minimum ECRH needed for current drive; treat as estimate with high uncertainty |
| 5 | Plant capacity factor not published | S1, S5 | proprietary | important | Central case adopts canonical 0.85 per scoring_framework.md §Plant availability (MCF quasi-steady, D-T); sensitivity sweeps should test lower values (e.g., 0.65–0.75) to capture pulsed-operation downside risk from CS re-magnetization dwell periods |
| 6 | No published capital cost estimate for ST-E1 | S1, S5 | proprietary | blocking | Brown (2018) IEEE ST cost decomposition and PROCESS-based ST cost studies provide reference framework; apply compact-ST geometric adjustment |
| 7 | Component replacement schedule (blanket, divertor, center stack) not disclosed | S3, S5 | proprietary / not-yet-sourced | important | ITER blanket program and ARIES-ST maintenance studies provide analogies; liquid Li blanket replacement likely faster than solid module exchange but no ST-E1 specific data |
| 8 | Liquid Li tritium extraction system design and cost | S3, S4, S5 | truly-unknown | important | Review EU-DEMO Pb-17Li TBM extraction literature as closest published analog; flag as less well-characterized than FLiBe extraction |
| 9 | WC cermet irradiation performance under 14 MeV neutrons | S3, S4 | truly-unknown | important | Dedicated irradiation campaign needed; no public data exists; could be partially addressed by existing fission-spectrum irradiation data with spectrum unfolding |
| 10 | REBCO tape total demand for ST-E1 magnet system | S4, S5 | derivable | important | Estimate from Demo4 coil scale + scaling to ST-E1 geometry; Tokamak Energy may publish with ST80-HTS results |
| 11 | Thermal energy storage system sizing and cost for quasi-steady pulsed operation | S3, S5 | truly-unknown | important | No ST-E1 specific data; molten salt TES from CSP industry provides cost analog (~$15–30/kWh_th); needs sizing input from pulse length and dwell time |
| 12 | Plasma current for Revision D design | S5 | not-yet-sourced | important | Disruption paper uses pre-Rev D value (13.6 MA at R=4.25 m); Rev D value for R=5.0 m should scale roughly as Ip ∝ aB/q; estimated ~15–18 MA but unconfirmed |
| 13 | Center stack neutron shielding performance at ST-E1 scale | S3, S5 | not-yet-sourced | important | Scale Humphry-Baker & Smith (2019) neutron transport results to ST-E1 geometry; publish via PROCESS or MCNP model |
| 14 | Li-6 enrichment level required for TBR=1.2 with outboard-only blanket | S4 | derivable | nice-to-have | Neutronics calculation with blanket geometry; sets Li supply chain requirement; analogous calculations exist for Pb-17Li TBM designs |
| 15 | Demo4 coil detailed dimensions and REBCO tape length | S3 | not-yet-sourced | nice-to-have | Would enable scaling estimate for ST-E1 tape demand; Tokamak Energy has not disclosed; may follow in a technical paper |

---

## Section 7: Cross-Concept Notes

The approved analysis for the HTS Compact Tokamak (CFS, `01-hts-compact-tokamak`) is the most directly applicable prior analysis for cross-referencing. Both concepts use REBCO HTS magnets and D-T fuel with a liquid breeding blanket, but they diverge significantly in geometry, blanket chemistry, field strength, and heating approach. The following elements from the CFS analysis are reused or adapted here.

**Reused assumptions and structures:**

- **REBCO tape cost and supply chain**: The CFS analysis characterizes the global REBCO production bottleneck (~thousands km/year capacity vs. >5,000 km needed per ARC reactor), current pricing ($30–100/kA-m), and commercial viability target (~$10/kA-m) [01-hts-compact-tokamak.md, Section 4]. These figures apply equally to ST-E1's REBCO requirement, with the caveat that ST-E1's lower field reduces tape performance requirements per unit length but the larger machine geometry partially offsets total tape demand.
- **Tritium fuel cycle (D-T)**: Global inventory constraint (~25–30 kg), startup inventory (~1 kg at >$35,000/g), CANDU production decline, and self-sufficiency sequencing constraint are identical across all D-T concepts [01-hts-compact-tokamak.md, Section 4].
- **Regulatory cost uncertainty**: The Stewart & Shirvan 2.2× building cost factor for fission-style regulation applies to ST-E1 as a D-T fusion plant, exactly as it applies to ARC [01-hts-compact-tokamak.md, Section 2].
- **Capacity factor sensitivity**: Availability is the highest-elasticity lever in the model sensitivity output (−0.85 %LCOE/%param). The central-case value of 0.85 follows the project-wide canonical value for MCF quasi-steady D-T concepts (scoring_framework.md §Plant availability); ST-E1's pulsed operation creates downside risk relative to steady-state designs, which is captured in sensitivity sweeps rather than the central case. This canonical alignment makes cross-concept LCOE comparisons within the MCF family apples-to-apples on this dimension.

**Key divergences from CFS analysis:**

- **Blanket: Liquid Li vs. FLiBe**: ST-E1 uses liquid lithium metal (outboard-only), not FLiBe immersion. This removes beryllium from the supply chain but introduces distinct Li metal handling challenges (chemical reactivity, tritium extraction chemistry). FLiBe NOAK cost estimates from Araiinejad & Shirvan (~$154/kg) do not apply to Li metal. Li metal is commercially available and less supply-constrained than FLiBe, but Li-6 enrichment is still required. The blanket TRL is similar (both ~TRL 2–3) but the engineering challenges are different.
- **Magnetic field and geometry**: ST-E1 at A=2.3, B=5.25 T is a categorically different operating regime from ARC at A=3.0, B=9.2 T. Higher beta in the ST plasma compensates for lower field. Lower field means lower mechanical stress on coils and lower REBCO tape performance requirements per unit length. The magnet system is in principle less technically demanding than CFS's, but the compact center stack with WC cermet shielding is a unique challenge with no ARC equivalent.
- **Heating approach**: ARC uses ICRF + LHCD; ST-E1 uses ECRH-only for flat-top. ECRH has lower wall-plug efficiency (~50–55%) than NBI, creating higher recirculating power per unit of current drive. ICRF (for ARC) also has moderate wall-plug efficiency (~70%), but LHCD may have similar issues. The specific recirculating power fraction comparison cannot be made without knowing the auxiliary heating power of either concept at their respective design points.
- **Pulsed vs. quasi-steady**: ARC targets quasi-steady operation (tens of minutes burns via bootstrap + LHCD current drive) that approaches continuous operation. ST-E1 explicitly embraces pulsed operation (15+ min pulses with dwell periods) as "more desirable" for ST geometry. This means ST-E1 requires a thermal energy storage buffer between pulses, a capital cost category absent from ARC's cost structure.
- **Data availability**: ARC has the published Sorbom et al. (2015) full plasma parameter set; ST-E1 has only the four machine parameters from DPP 2025. The CFS analysis can anchor an LCOE model to a specific physics design point; the ST-E1 analysis cannot without substantial analogues.

**Spherical tokamak-specific considerations for the TEA pipeline:**

The ST geometry creates several cost structure features that differentiate it from conventional aspect-ratio tokamaks (ARC, DEMO) and that the TEA pipeline should represent:
1. Outboard-only blanket coverage — blanket cost scales differently from 4π designs; TBR sensitivity to port fractions and shielding penetrations is higher.
2. Center stack shielding as a separate capital and O&M cost item — no equivalent in ARC or conventional tokamak designs.
3. Thermal energy storage buffer — required for pulsed operation; sized by pulse energy and dwell duration; absent from steady-state designs.
4. Higher beta → potentially higher normalized performance per unit magnetic energy stored → different CAPEX driver mix than high-field designs (less magnet cost per unit fusion power, but smaller building size trade-off is less pronounced at lower field).

---

## Section 8: Sources

**1. APS DPP 2025 Abstract — ST-E1 Revision D overview (Maartensson et al., November 2025)**
- Contribution: Authoritative source for all ST-E1 Revision D machine parameters (R=5.0 m, A=2.3, B=5.25 T, 450–750 MWe net, TBR=1.2, outboard-only Li blanket). Confirms "final pre-conceptual design point" designation and maintenance-first design methodology.
- Location: Phase 1a source [iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md]

**2. Alieva et al. (2026) — EC heating and current drive for Tokamak Energy FPP**
- Full citation: Alieva, A. et al. (2026) "Progress in the pre-conceptual design of the auxiliary heating and current drive system for the Tokamak Energy Fusion Pilot Plant," *EPJ Web of Conferences*, 2026.
- Contribution: Peer-reviewed confirmation that ST-E1 flat-top phase relies exclusively on EC waves in O-mode polarization for auxiliary heating and current drive. Ray-tracing optimization across three plasma scenarios. Primary source for heating strategy characterization.
- Location: Phase 1a source [iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md]

**3. Tokamak Energy Demo4 press release (November 19, 2025)**
- Contribution: Complete 14 TF + 2 PF HTS coil set at 11.8 T, 30 K — world-first for complete HTS tokamak magnet system. 7 million ampere-turns through center column. Confirms REBCO magnet technical approach is validated at tokamak coil-set scale.
- Location: Phase 1a source [iter-03/sources/tokamak-energy-demo4-magnets.md]

**4. Humphry-Baker, S.A. and Smith, G.D.W. (2019) — Center stack shielding in compact spherical tokamak**
- Full citation: Humphry-Baker, S.A. and Smith, G.D.W. (2019) "Shielding materials in the compact spherical tokamak," *Philosophical Transactions of the Royal Society A*, 377(2141). doi:10.1098/rsta.2018.0233. PMC6365859.
- Contribution: Quantitative analysis of center stack neutron shielding for a compact ST (R=1.35 m). WC-FeCr cermet identified as optimal; 32 cm radial depth; ~1.4 × 10¹⁷ m⁻² s⁻¹ fast neutron flux into SC core. Explicitly identifies irradiation database gap for WC cermets under fusion neutrons.
- Location: Phase 1a source [iter-02/sources/spherical-tokamak-center-stack-shielding.md]

**5. Tokamak Energy ST-E1 design evolution documentation (compiled from DPP 2024 and DPP 2025)**
- Contribution: Documents progression from initial design (A=2.0, R=4.25 m, 85 MWe net) to Revision D (A=2.3, R=5.0 m, 450–750 MWe net). Key metric: the dramatic increase in power output from initial to Rev D indicates significant design philosophy change and indicates the design has not stabilized.
- Location: Phase 1a source [iter-02/sources/tokamak-energy-st-e1-design-evolution.md]

**6. Gryaznevich, M. et al. (MDPI 2023) — Pulsed spherical tokamak reactors**
- Full citation: Gryaznevich, M. et al. (2023) "Pulsed Spherical Tokamak — A New Approach to Fusion Reactors," *Plasma*, 5(2), 19. doi:10.3390/plasma5020019. (Authors include Tokamak Energy researchers.)
- Contribution: Establishes physics case for pulsed ST reactors. Key findings: pulsed STs "more desirable than steady-state"; starting point for reactor-relevant pulses is tens of minutes; HTS central solenoid provides order-of-magnitude higher flux for inductive current drive. Foundational reference for operation mode characterization.
- Location: Phase 1a source [iter-01/sources/pulsed-spherical-tokamak-paper.md]

**7. Tokamak Energy company overview and roadmap documentation**
- Contribution: Company background ($335M funding, ~280 staff, DOE Milestone program selection May 2023), machine roadmap (ST40 → ST80-HTS → ST-E1), commercial plant timeline. ST80-HTS completion target ~2026; ST-E1 grid connection "early 2030s."
- Location: Phase 1a sources [iter-01/sources/tokamak-energy-overview.md; iter-02/sources/tokamak-energy-roadmap.md]

**8. ST40 and ST80-HTS heating systems documentation**
- Contribution: ST40 operational heating: NBI + 1 MW Kyoto Fusioneering gyrotron (104/137 GHz, delivered Jan 2025). Combined NBI + ECRH approach on ST40 informing pilot plant design. Gyrotron technology described as "crucial for future power plants."
- Location: Phase 1a sources [iter-01/sources/st40-heating-systems.md; iter-02/sources/tokamak-energy-heating-systems.md]

**9. Brown, T.G. (2018) — Three confinement systems cost comparison**
- Full citation: Brown, T.G. (2018) "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148.
- Contribution: Reference framework for decomposing ST capital cost by component category relative to conventional tokamak and stellarator. Provides the primary publicly available cost comparison basis for an ST power plant.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**10. Araiinejad, L.S. and Shirvan, K. (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: Most detailed public LCOE sensitivity analysis for D-T MCF plants; capacity factor uncertainty ranges (75–90%); regulatory cost scenarios; FLiBe cost estimate ($154/kg NOAK). Used here as proxy for ST-E1 missing LCOE parameters.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**11. Hidalgo-Salaverri et al. (2025) — Spherical tokamak TEA**
- Full citation: Hidalgo-Salaverri, J. et al. (2025) "Hybrid hydrogen-electricity production using spherical tokamaks: a cost-driver sensitivity study and techno-economic analysis," *Nuclear Fusion*, 65, 036027. doi:10.1088/1741-4326/adaa01.
- Contribution: ST-specific TEA with cost-driver sensitivity analysis. Provides the most directly applicable independent economic analysis for a spherical tokamak configuration.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**12. Foster, J. et al. (2024) — Extrapolating costs to commercial fusion power plants**
- Full citation: Foster, J. et al. (2024) "Extrapolating costs to commercial fusion power plants," *IEEE Transactions on Plasma Science*, 52(9), pp. 3772–3777. doi:10.1109/TPS.2024.3362428. UKAEA publication.
- Contribution: UKAEA cost extrapolation framework for fusion plants including ST variants; useful for ST-E1 capital cost estimation in absence of plant study.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**13. Approved D1+ Analysis: HTS Compact Tokamak (01-hts-compact-tokamak)**
- Contribution: Cross-concept reference for shared HTS magnet supply chain characterization (REBCO tape costs, production capacity), D-T tritium supply constraints, FLiBe cost estimates (not applicable to ST-E1 Li metal blanket but referenced for comparison), regulatory cost scenarios, and CFS company transparency benchmarking.
- Location: `analyses/01-hts-compact-tokamak/analysis.md`
