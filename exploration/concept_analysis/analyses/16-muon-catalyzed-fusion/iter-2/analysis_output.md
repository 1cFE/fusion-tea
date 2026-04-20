# D1+ Analysis: Muon-Catalyzed Fusion (D-T) — Acceleron Fusion

**Concept**: Muon-Catalyzed Fusion (μCF) — D-T fuel
**Company**: Acceleron Fusion (US; founded 2008, spun off 2022)
**Confinement Family**: Non-Standard (non-plasma, muon catalysis)

---

## Section 1: Availability of Data

**Rating: Limited**

Muon-catalyzed fusion (μCF) has a well-established physics literature going back to Jackson's 1957 theoretical study, but commercially focused engineering data is almost entirely absent. For Acceleron Fusion specifically, only three sources were captured in the Phase 1a research:

- **ARPA-E BETHE presentation (July 2025)**: The primary engineering reference. Discloses the active-target muon source design concept, ML-optimized geometry, the 47% recirculating power claim, the $0.025/kWh LCOE target, and a cost-versus-physics-parameters contour plot. Contains preliminary (explicitly flagged) DT cycling rate data. A single presentation is a thin basis for LCOE modeling.
- **Acceleron company overview** (acceleron-company-overview.md): Marketing-level document. Establishes the 100 MWe target plant size, 500–1000°C operating temperature range, and the PSI experimental campaign (September 2024). No quantitative cost or engineering data.
- **Wikipedia article on muon-catalyzed fusion physics** (muon-catalyzed-fusion-physics.md): Comprehensive coverage of the underlying physics, historical experiments, and the fundamental energy-balance barriers. Cites Jackson (1957), Jones et al. (Los Alamos LAMPF), and Kelly, Hart & Rose (2021). This is the best available public source on the physics constraints.

**Peer-reviewed publications from Acceleron**: None found in Phase 1a research. The company's PSI experimental campaign (September 2024) has not yet produced published results. No plant studies, systems code outputs, or independent techno-economic analyses of the MCF concept exist in the public domain.

**General μCF physics literature**: A moderate body of peer-reviewed work exists on the fundamental physics — particularly from the Los Alamos Meson Physics Facility experiments (Jones et al., achieving 150 fusions/muon), and theoretical studies on alpha-sticking (Jackson 1957; revised estimates 0.3–0.5% sticking probability). However, this literature is primarily physics-focused and does not address commercial cost structure.

**Phase 1a dossier completeness**: High confidence on confinement family, fuel, primary mechanism, plasma state, operation mode, and driver technology. Medium confidence on energy capture cycle (Brayton mentioned but not confirmed), tritium breeding design (shown in diagrams but unspecified). No cost data captured.

**Key data gaps limiting analysis**:
1. No published capital cost estimate for any μCF plant system
2. No published accelerator design specifications or cost for Acceleron's muon source at plant scale
3. No Q value or net energy balance demonstrated at any scale
4. Blanket type, TBR target, and tritium extraction approach undisclosed
5. No capacity factor or maintenance schedule data

---

## Section 2: Challenges in Capturing System Function

Muon-catalyzed fusion presents a unique modeling challenge: the dominant LCOE uncertainty is not capital cost uncertainty but **physics feasibility uncertainty**. The two binding physics parameters — muon production energy cost and fusions per muon — are coupled in a way that makes the LCOE contour extremely steep near the commercial threshold. Challenges are ranked by LCOE impact.

**1. Energy balance: the fundamental viability constraint (Impact: Critical)**

The entire LCOE model for μCF is gated by the ratio of energy produced per muon to energy consumed per muon. The D-T fusion reaction releases 17.6 MeV per event [muon-catalyzed-fusion-physics.md §Deuterium–tritium]. Each muon costs approximately 6 GeV (electrical energy) to produce via conventional accelerators [muon-catalyzed-fusion-physics.md §Problems facing practical exploitation]. To break even purely on fusion energy, a muon must catalyze approximately 340 fusions (6,000 MeV ÷ 17.6 MeV). With realistic accelerator efficiency (18% electrical to deuteron kinetic energy) and heat-to-electric conversion (~60%), the Kelly, Hart & Rose (2021) model finds:

> "Using realistic accelerator efficiency of 18% and heat-to-electric conversion of 60%, only 14% of electrical energy consumed could be produced" [muon-catalyzed-fusion-physics.md §Breakeven alternative estimate]

This means even 150 fusions/muon (the Los Alamos record) does not approach commercial viability at current accelerator efficiency. Acceleron's innovation addresses both sides simultaneously: reducing muon production energy to ~2.5–3 GeV via a novel active-target accelerator design, and targeting ~200–300 fusions per muon via enhanced operational parameters. The ARPA-E cost contour plot shows that the $0.025/kWh commercial target requires approximately 200 fusions/muon at 2.5 GeV muon energy cost [acceleron-arpa-e-presentation-2025.md §Cost of electricity versus physics parameters]. Neither target has been demonstrated. The uncertainty envelope around this operating point is large enough to encompass both commercial viability and commercial impossibility — making energy balance the single most consequential gap in the LCOE model.

**Critical risk framing**: At Acceleron's stated operating point (E_mu = 2.5 GeV, N_fus = 200, η_th = 50%), independent analysis of the energy balance finds Q_sci ≈ 1.41 and a gross-to-driver energy ratio of approximately 0.78 — meaning the fusion chamber produces only ~78% of the energy the accelerator consumes, yielding net-negative electricity at standard conversion efficiency. This is not a marginal shortfall: at these parameters, the plant operates as an energy sink regardless of capital cost structure. The $0.025/kWh ARPA-E contour target therefore cannot be reached at the stated operating point under standard conversion assumptions — it either depends on undisclosed conversion efficiency gains beyond η_th = 50%, on physics parameters more favorable than those stated (e.g., lower E_mu or higher N_fus), or on substantial heat sales revenue offsetting the electrical deficit. The primary risk bifurcation for MCF is not LCOE level but whether net positive electricity generation is physically achievable at the stated operating point. A concept whose self-reported parameters imply an energy sink has a categorically different risk profile than one that achieves positive Q but high LCOE.

**2. Alpha-sticking: the physics ceiling on fusions per muon (Impact: Critical)**

Alpha-sticking — the probability that a muon permanently bonds to the alpha particle from a D-T fusion event — limits the maximum achievable fusions per muon. Two distinct quantities matter here: the *initial* sticking probability (ω_S⁰), the fraction captured immediately at the moment of fusion; and the *effective* sticking probability, the fraction permanently lost after accounting for Auger reactivation, in which muons initially captured on the recoiling alpha are partially recovered as the alpha decelerates in the dense D-T medium and transfers the muon back to the fuel. The effective probability is what sets the fusions/muon ceiling.

> "The α-sticking problem is the approximately 1% probability of the muon 'sticking' to the alpha particle that results from deuteron-triton fusion, thereby effectively removing the muon from the muon-catalysis process altogether." [muon-catalyzed-fusion-physics.md §Problems facing practical exploitation]

This "~1%" figure (Jackson 1957) approximates the initial sticking probability. Kamimura & Kino (2021) calculate ω_S⁰ = 0.857% — "~7% smaller than the literature values (≃0.91–0.93%)" — using a coupled-channels Schrödinger equation for the dtμ molecule [arxiv-2112-08399.md §Abstract]. After Auger reactivation, the effective sticking probability falls to 0.3–0.5%, raising the achievable ceiling from ~100 fusions/muon (Jackson's estimate) to 200–350 fusions/muon [muon-catalyzed-fusion-physics.md §Problems facing practical exploitation]. The analysis cites the 0.3–0.5% figure throughout as the effective post-reactivation value — the quantity that enters the LCOE model. Acceleron's 300 fusions/muon target sits near the top of this revised effective range. The sticking probability is not a freely adjustable engineering parameter — it is a function of quantum mechanical muon transfer dynamics. Any LCOE model must represent fusions/muon as a constrained physics parameter rather than a design variable.

**3. Accelerator cost: novel capital cost category with no fusion analogues (Impact: High)**

The superconducting proton accelerator that produces muons is the likely dominant capital cost item for a commercial μCF plant. Particle physics accelerators are the only available cost analogues (e.g., spallation neutron sources, proton therapy facilities), but these are optimized for very different operating regimes (much higher beam energy, much lower average current). A μCF power plant requires a high-current, moderate-energy (2.5–3 GeV) CW proton accelerator — a class of machine that has not been built at scale. Acceleron claims their active-target muon source with ML-optimized geometry achieves the 3 GeV/muon target [dossier.md §Driver Technology; acceleron-arpa-e-presentation-2025.md §Muon source], but no cost estimate for the accelerator system at any scale is in the public domain. The accelerator represents a recurring capital cost structure analogous to the pulsed power driver in MagLIF or the laser system in IFE — but with no existing plant-scale cost reference.

**4. Fusion chamber (target) at commercial scale: undefined architecture (Impact: High)**

Acceleron's current experimental apparatus uses a diamond anvil cell (DAC) to compress DT fuel to high density [acceleron-arpa-e-presentation-2025.md §Materials and Methods]. A diamond anvil cell is precision laboratory equipment designed for one-off static compression experiments. It bears no architectural relationship to a commercial fusion chamber. What the power plant fusion chamber looks like — how DT fuel is continuously cycled, how fusion neutrons are captured, how product helium is exhausted, and how the chamber survives long-term operation — is entirely unspecified in available sources. The architecture must be reinvented between the experimental and commercial scales.

**5. Operating cost structure: no data, placeholder required (Impact: High)**

No information on O&M cost breakdown, maintenance schedule, component replacement rates, staffing requirements, or unplanned outage rates is available for a μCF power plant. At the subsystem level, a continuous-operation superconducting accelerator has known O&M characteristics from particle physics, but power-plant-scale operation of this class of machine is not documented. The Brayton cycle BOP is mature with well-characterized O&M. The fusion chamber and tritium handling systems have no analogous operational history. LCOE models for this concept require explicit O&M placeholder sections with wide uncertainty bounds. Until the chamber architecture is defined, the distinction between scheduled and unscheduled maintenance cannot be made, and no realistic capacity factor can be established.

**Modeling Approach**

The MCF cost model uses the 1cFE CAS-Structured Free-Form approach rather than 1costingfe's plasma-centric CAS accounts because the dominant capital cost item — the superconducting proton accelerator — has no analog in plasma-fusion account structures (CAS22: magnet system, CAS23: heating systems, CAS26: vacuum systems are all inapplicable). The accelerator is better treated as a single capital block with its own scaling law. Three parameters dominate LCOE sensitivity, in descending order: (1) **E_mu** (muon production energy cost, GeV/muon) — the most uncertain physics parameter, currently 6× above the commercial target; (2) **N_fus** (fusions per muon) — the physics ceiling parameter, bounded above by effective sticking probability; and (3) **accelerator capital cost** ($/kWe) — the cost analogue to the magnet system or driver in other fusion concepts, currently uncharacterized at power-plant scale. The key testable hypothesis the model explores: *Is there any combination of E_mu ≤ 3 GeV and N_fus ≥ 150 that satisfies net electricity output AND LCOE < $0.10/kWh under independently derived capital and O&M assumptions?* The model output (scenario table) shows that at current demonstrated parameters (E_mu = 6 GeV, N_fus = 150), all scenarios produce net-negative electricity, and even at Acceleron's stated targets (E_mu = 2.5 GeV, N_fus = 200), the plant is marginally net-negative. Commercial viability requires simultaneous achievement of both targets beyond currently demonstrated levels.

**6. Tritium breeding: architecture unspecified (Impact: Moderate)**

As a D-T concept, tritium self-sufficiency requires TBR > 1.0. A breeding blanket appears in Acceleron's system diagrams, but the type (FLiBe, LiPb, solid ceramic), geometry, and TBR target are not disclosed [dossier.md §Tritium Breeding]. The blanket design interacts with the muon source and chamber architecture — a DT neutron-transparent chamber must still be surrounded by a breeding medium. The low-temperature, non-plasma nature of μCF (fusion occurs at 500–1000°C in material containment) simplifies some blanket engineering compared to MFE concepts, but the complete tritium cycle remains uncharacterized.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**Fusion Chamber / DT Target System — TRL 1–2**

- **Demonstrated**: Diamond anvil cell compression of DT fuel at laboratory scale (PSI, September 2024) [acceleron-company-overview.md §Testing]. This is a proof-of-concept apparatus, not a scalable power plant component. Muon-catalyzed fusion physics has been experimentally demonstrated (D-T cycling, 150 fusions/muon) at Los Alamos LAMPF [muon-catalyzed-fusion-physics.md §History].
- **On paper only**: A commercial-scale fusion chamber that continuously cycles DT fuel, captures fusion neutrons, and sustains the muon catalysis reaction at plant power density. Acceleron's DT cycling rate data is described as "PRELIMINARY" in the ARPA-E presentation [acceleron-arpa-e-presentation-2025.md §Results]. No engineering design exists for a power plant fusion chamber.
- **Missing at scale**: Continuous DT fuel injection and recovery at kg/day scale. Helium exhaust management without muon loss. Fusion chamber material compatibility with muon beams, DT fuel, and 14.1 MeV neutrons over plant lifetime. Target-equivalent architecture replacing the diamond anvil cell.

---

**Active-Target Muon Source (ML-Optimized) — TRL 2–3**

- **Demonstrated**: Conventional pion/muon production from proton beams is a mature technique at major accelerator facilities (LAMPF, PSI, TRIUMF, RAL). Acceleron claims preliminary results from PSI experiments (2024) [acceleron-company-overview.md §Testing]. The active-target design and ML-optimized geometry represent a novel approach aimed at reducing the energy cost per muon from ~6 GeV (conventional) to ~3 GeV [dossier.md §Driver Technology; acceleron-arpa-e-presentation-2025.md §Muon source].
- **On paper only**: The full active-target accelerator system achieving 3 GeV/muon at power-plant-relevant muon flux. ML-optimized geometry validated at target scale. Muon beam optics and focusing for efficient injection into the DT target.
- **Missing at scale**: Continuous-wave (CW) operation at the beam current required for ~100 MWe output. Accelerator wall-plug efficiency achieving the 47% recirculating power fraction target. The 47% figure appears to be a model output rather than a measured result [acceleron-arpa-e-presentation-2025.md §Muon source; dossier.md §Summary].

---

**Tritium Breeding Blanket — TRL 2 (type unspecified)**

- **Demonstrated**: Blanket shown in Acceleron system diagrams, type not disclosed [dossier.md §Tritium Breeding]. General D-T blanket physics and several blanket concepts (FLiBe, LiPb, solid ceramic) are mature at laboratory scale, as characterized in the HTS Compact Tokamak analysis [01-hts-compact-tokamak.md §Tritium Fuel Cycle].
- **On paper only**: A complete μCF-specific breeding blanket design integrated with the fusion chamber architecture. TBR target not stated. Neutron spectrum from room-temperature D-T catalysis is identical to plasma D-T (14.1 MeV neutrons), so blanket physics is the same — but the chamber geometry differs entirely from toroidal or spherical MFE designs.
- **Missing at scale**: Integration with the non-plasma, material-containment fusion chamber. Tritium extraction from the breeding medium at kg/day throughput. Self-sufficient tritium fuel cycle with TBR > 1.

---

**Superconducting Proton Accelerator — TRL 4–5**

- **Demonstrated**: Superconducting linear proton accelerators exist at particle physics facilities (SNS at ORNL, ESS in Lund, proton therapy systems). These use NbTi or Nb₃Sn cavities optimized for pulsed operation. Continuous-wave superconducting linacs for proton acceleration at relevant energies (~GeV class) exist at several facilities. Acceleron assumes a superconducting accelerator in their LCOE model [acceleron-arpa-e-presentation-2025.md §Cost model].
- **On paper only**: A CW superconducting accelerator optimized for muon production efficiency at 2.5–3 GeV proton energy, operating at the beam current required for ~100 MWe fusion output.
- **Missing at scale**: Commercial-grade, power-plant availability operation of a GeV-class superconducting linac (particle physics machines have availability driven by experimental schedules, not power generation economics). Cost reduction from scientific instrument to industrial product. Accelerator design co-optimized with the active-target muon source geometry.

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: Laboratory-scale tritium handling, gram-level D-T operations at PSI, TRIUMF, and other muon facilities. The μCF tritium cycle shares the same fundamental challenges as all D-T approaches. Historical μCF experiments at LAMPF used D-T mixtures in liquid or gas form [muon-catalyzed-fusion-physics.md §History].
- **On paper only**: Closed-loop kg/day tritium breeding, extraction, and recycling at plant scale. Tritium handling integrated with continuous muon beam operation and DT target cycling.
- **Missing at scale**: Same as all D-T concepts: industrial tritium processing, self-sufficiency demonstration, permeation barrier systems. μCF-specific: tritium management in a material-containment (non-vacuum) chamber environment.

---

**Energy Conversion (Brayton Cycle BOP) — TRL 8–9**

- **Demonstrated**: Brayton cycle (gas turbine) power conversion is commercially mature. Supercritical CO₂ Brayton cycles at 500–1000°C inlet are in commercial demonstration at CSP and fission pilot plants. Acceleron's operating temperature range (500–1000°C) is compatible with high-efficiency Brayton cycles. This is the one fully mature subsystem in the MCF architecture.
- **Missing at scale**: Integration with tritium-compatible heat exchangers and the specific thermal output profile of a μCF chamber. The non-pulsed, continuous nature of μCF simplifies BOP compared to pulsed IFE concepts.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium — Declining External Supply (Shared D-T Constraint)**

The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU heavy-water reactor byproduct, decaying at 5.5%/year. Startup inventory for a D-T plant requires ~1 kg at >$35,000/g [analyses/21-spherical-tokamak-hts §Section 4]. MCF shares this constraint identically with tokamaks, stellarators, and other D-T concepts. No breeding blanket type has been specified for Acceleron, but any commercial MCF plant requires TBR > 1 for fuel self-sufficiency. The external tritium supply is declining as CANDU reactors age — the same sequencing constraint applies: early MCF plants must demonstrate tritium self-sufficiency before fleet scaling.

**Superconducting Accelerator Materials (NbTi / Nb₃Sn or HTS)**

The proposed superconducting accelerator requires large quantities of superconducting RF cavity material. For GeV-class protons, niobium cavities (NbTi or bulk Nb) are the standard. This is a well-characterized supply chain — niobium RF cavities are manufactured by several specialized vendors (e.g., JLAB, DESY partners). The supply chain is much better developed than REBCO HTS for fusion magnets; there is no supply bottleneck analogous to the REBCO shortage facing tokamak programs. If Acceleron's accelerator uses HTS for focusing magnets (rather than the cavities themselves), the REBCO supply chain constraint would partially apply, but at lower tape demand than a full tokamak magnet system.

**No REBCO Confinement Magnets — A Genuine Supply Chain Advantage**

Unlike tokamaks, stellarators, and mirror machines, μCF requires no large HTS confinement magnets. The dominant HTS supply chain bottleneck for the fusion industry (REBCO tape: currently ~$30–100/kA-m; target ~$10/kA-m for commercial tokamaks [analyses/21-spherical-tokamak-hts §Section 4]) simply does not apply to MCF. This is a structural cost advantage over MFE concepts.

**No Beryllium Required**

MCF uses no beryllium in its baseline architecture. The FLiBe blanket supply chain constraint (scarce beryllium from Materion Corp, ~300 tonnes/year global supply) does not apply if a lithium-based blanket is chosen. The blanket material selection remains undefined, but beryllium is not intrinsic to the concept.

**DT Fuel Target / High-Pressure DT Handling**

Current experiments use diamond anvil cells (DAC) to compress DT fuel to high density [acceleron-arpa-e-presentation-2025.md §Materials and Methods]. Diamond anvil cells are precision laboratory instruments manufactured in small quantities for materials science research. No industrial-scale production pathway for DT-compatible DAC-equivalent components exists. The commercial chamber architecture is undefined, so materials requirements cannot be quantified. If a material-containment concept replaces the DAC at scale, the materials challenge shifts to high-temperature, DT-compatible structural materials (Hastelloy-N class, tungsten, or ceramics) compatible with 14 MeV neutron flux.

**Lithium-6 Enrichment (for tritium breeding)**

Natural lithium is ~7.5% Li-6. Depending on blanket design and geometry, Li-6 enrichment may be required to achieve TBR > 1. Li-6 enrichment capacity is limited globally (Russian and Chinese production use legacy mercury amalgam processes; Western alternatives are in development). This constraint is shared with all D-T fusion concepts requiring a lithium breeding blanket.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| LCOE target | $0.025/kWh | acceleron-arpa-e-presentation-2025.md §Cost of electricity versus physics parameters | medium | Company self-reported; single data point on contour plot; assumes superconducting accelerator + Brayton BOP + revenue from heat sales |
| Muon energy cost (target) | 2.5–3 GeV | acceleron-arpa-e-presentation-2025.md §Cost contour; dossier.md §Summary | medium | Conventional accelerators cost ~6 GeV/muon; active-target design targets 3 GeV; cost contour operating point shown at 2.5 GeV |
| Muon energy cost (current state-of-art) | ~6 GeV | muon-catalyzed-fusion-physics.md §Problems facing practical exploitation | high | "Best recent estimates" per Wikipedia source; sets baseline for any MCF LCOE model |
| Fusions per muon (near-term target) | ~200 | acceleron-arpa-e-presentation-2025.md §Cost contour | medium | Operating point on $0.025/kWh iso-cost line; read from contour figure |
| Fusions per muon (stretch target) | ~300 | dossier.md §Summary | medium | Acceleron's stated target; near top of physics ceiling with 0.3–0.5% sticking |
| Fusions per muon (demonstrated maximum) | 150 | muon-catalyzed-fusion-physics.md §Problems facing practical exploitation | high | "Steven E. Jones' team achieved 150 d-t fusions per muon" at Los Alamos LAMPF; "almost enough to reach theoretical break-even" |
| Alpha-sticking probability, initial (ω_S⁰) | 0.857% (literature range: 0.86–0.93%) | arxiv-2112-08399.md §Abstract (Kamimura & Kino 2021); muon-catalyzed-fusion-physics.md §Problems facing practical exploitation | high | Theoretical calculation of dtμ molecule; "~7% smaller than literature values (≃0.91-0.93%)"; Jackson 1957 originally estimated ~1% initial sticking |
| Alpha-sticking probability, effective (post-reactivation) | 0.3–0.5% | muon-catalyzed-fusion-physics.md §Problems facing practical exploitation | high | Reduced from initial by Auger muon reactivation as alpha decelerates; this is the quantity that sets the fusions/muon ceiling at 200–350 |
| Recirculating power fraction (claimed) | 47% | acceleron-arpa-e-presentation-2025.md §Muon source | low | Model output, not measured; assumes active-target design at target muon energy cost; described as "preliminary" in dossier |
| Plant electrical output (target) | ~100 MWe | acceleron-company-overview.md §Advantages | medium | "Small (100 MW) power plants"; no design basis published |
| Operating temperature | 500–1000°C | acceleron-company-overview.md §Advantages | medium | Range stated for material-containment fusion cell; compatible with high-efficiency Brayton cycle |
| D-T fusion energy release | 17.6 MeV | muon-catalyzed-fusion-physics.md §Deuterium–tritium | high | Fundamental physics: 14.1 MeV neutron + 3.5 MeV alpha; an additional 4.8 MeV extractable via Li-6 blanket |
| Muon lifetime | 2.2 μs | muon-catalyzed-fusion-physics.md §Process | high | Rest-frame lifetime; sets fundamental limit on muon cycling rate |
| Energy conversion cycle | Brayton | acceleron-arpa-e-presentation-2025.md §BOP | medium | Stated in LCOE model assumptions; unconfirmed for commercial design |
| Thermal efficiency (estimated) | [inferred] ~45–50% | [inferred: Brayton cycle at 500–1000°C; sCO₂ Brayton commercial demonstration data ~45–50% at these temperatures] | low | Derivable from stated operating temperature and Brayton cycle physics; Acceleron has not published a specific value |
| Net electrical efficiency (Kelly et al. model) | ~14% of electrical input | muon-catalyzed-fusion-physics.md §Breakeven alternative estimate | medium | At 150 fusions/muon + 18% accelerator efficiency + 60% thermal conversion; highlights severity of energy balance challenge |
| Energy breakeven test date | ~2030 (5-year roadmap from 2025) | dossier.md §Summary; acceleron-arpa-e-presentation-2025.md §Roadmap | medium | Planned at Brookhaven National Laboratory; no funding confirmation found |
| LCOE contour iso-cost lines | $0.01, $0.02, $0.03, $0.05, $0.10/kWh | acceleron-arpa-e-presentation-2025.md §Cost contour | medium | Function of fusions/muon (x-axis) and muon energy cost (y-axis); quantitative values from contour plot |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Plant capital cost ($M or $/kWe) | proprietary / truly-unknown | blocking | No estimate at any scale; dominant cost item (accelerator) has no published cost for the power-generation operating regime |
| Accelerator capital cost | truly-unknown | blocking | GeV-class CW superconducting linacs exist in particle physics at ~$500M–$2B scale; power generation scale and MCF-specific active-target variant is completely uncosted |
| Net Q / energy gain at commercial conditions | truly-unknown | blocking | 47% recirculating power fraction is a model output, not a measured Q; no energy gain demonstration at any scale exists |
| Fusion chamber capital cost | truly-unknown | blocking | Architecture undefined beyond diamond anvil cell (laboratory apparatus); no commercial-scale chamber design or cost |
| Operating cost breakdown | truly-unknown | blocking | No maintenance schedule, staffing model, consumable rates, or component replacement cycle for any μCF system |
| Capacity factor | truly-unknown | blocking | Continuous operation mode implies high CF in principle, but no maintenance model exists; accelerator availability in particle physics typically 85–95% but for scientific, not commercial, missions |
| Tritium breeding blanket type, TBR, cost | proprietary | blocking | Shown in system diagrams; not disclosed; blocks tritium fuel cycle analysis |
| Muon production efficiency (demonstrated) | proprietary | important | Active-target improvement over conventional demonstrated at PSI (2024) but result not published; only preliminary data mentioned in ARPA-E presentation |
| Accelerator wall-plug efficiency | truly-unknown | important | Acceleron's superconducting accelerator assumes achievement of the 47% recirculating power; actual accelerator efficiency has not been characterized at target operating conditions |
| DT cycling rate at target density | proprietary | important | "PRELIMINARY data on DT cycling rate to 2.2 LHD (2024)" per ARPA-E presentation; full validated data not available |
| Fusion chamber neutron wall loading | truly-unknown | important | Required for blanket design and neutron shielding calculations; not characterizable until chamber architecture is defined |
| Tritium startup inventory and supply chain plan | not-yet-sourced | important | D-T startup requirement (~1 kg) shared with all D-T concepts but not addressed in Acceleron-specific literature |
| LCOE sensitivity to muon energy cost vs. fusions/muon | derivable | nice-to-have | Contour plot is shown in ARPA-E presentation but not quantitatively extracted; iso-cost slope around the operating point quantifies relative value of improving each parameter |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Plant capital cost (total) unknown — LCOE model has no capital anchor | S1, S5 | truly-unknown | blocking | Publish accelerator system cost study analogous to Z-IFE driver cost estimates; proton therapy facility costs provide rough order-of-magnitude for superconducting linac in the GeV range |
| 2 | Accelerator capital cost — dominant subsystem cost, no public data for MCF-relevant operating regime | S2, S3, S5 | truly-unknown | blocking | SNS (ORNL, $1.4B, 1 GeV, 1.4 MW) and ESS (Sweden, ~€2B, 2 GeV) provide upper-bound analogues; active-target architecture may differ substantially |
| 3 | Net Q or energy gain: 47% recirculating power is modeled, not demonstrated | S2, S3, S5 | truly-unknown | blocking | Depends on achieving both 2.5 GeV/muon AND ~200 fusions/muon simultaneously; Brookhaven breakeven test (~2030) is the planned resolution |
| 4 | Fusion chamber architecture for commercial scale — DAC cannot scale | S2, S3, S5 | truly-unknown | blocking | No published design; must be defined before any subsystem cost modeling is possible |
| 5 | Operating cost structure: no maintenance model, capacity factor, or O&M breakdown | S2, S5 | truly-unknown | blocking | Particle physics accelerator O&M records (SNS, ESS operational data) provide analogues for accelerator portion; chamber O&M is undefined |
| 6 | Tritium breeding blanket type, TBR, and extraction method | S3, S4, S5 | proprietary | blocking | Blanket appears in Acceleron diagrams; ARPA-E progress reports may contain details; all D-T blanket literature (FLiBe, LiPb, solid ceramic) applies once type is known |
| 7 | Fusions per muon at Acceleron's target density conditions — PSI data not yet published | S2, S3, S5 | proprietary | blocking | Resolution requires publication of September 2024 PSI experimental results; impacts whether the 200 fusions/muon target is achievable |
| 8 | Muon production energy cost at Acceleron's active-target geometry — vs. 6 GeV conventional | S2, S3 | proprietary | blocking | Same PSI experimental campaign; whether active-target achieves meaningful improvement over conventional muon production has not been demonstrated publicly |
| 9 | DT cycling rate validation — "preliminary" data mentioned in ARPA-E presentation | S3, S5 | proprietary | important | Full cycling rate characterization needed to establish muon catalysis throughput per unit time and per unit volume |
| 10 | Alpha-sticking probability in Acceleron's high-density DT conditions | S2, S5 | not-yet-sourced | important | Recent measurements at 0.3–0.5% are from conventional μCF facilities; high-density (DAC-compressed) conditions may differ; muon transfer dynamics are density-dependent |
| 11 | Accelerator availability and maintenance model for power generation mission | S3, S5 | not-yet-sourced | important | Particle physics accelerators achieve 85–95% availability in scientific mode; power generation requires different scheduling and higher mean-time-between-failures targets; no published study |
| 12 | Li-6 enrichment requirement and blanket geometry for TBR > 1 | S4 | derivable | important | Requires blanket type to be known; once blanket architecture is disclosed, Li-6 enrichment fraction is calculable from standard neutronics |
| 13 | Commercial-scale diamond anvil cell or equivalent production — scaling the target system | S3, S4 | truly-unknown | important | Current DAC production is laboratory-scale; whether a commercial-scale equivalent exists or what it would cost is completely uncharacterized |
| 14 | Revenue from heat sales as LCOE lever — ARPA-E model includes heat revenue | S5 | derivable | nice-to-have | ARPA-E model explicitly includes "revenue from heat sales" as a contributor to $0.025/kWh target; the sensitivity of LCOE to this revenue stream is not quantified |
| 15 | Muon source muon yield per MW of beam power — fundamental throughput metric | S5 | not-yet-sourced | nice-to-have | Sets the scale relationship between accelerator power and fusion chamber output; derivable from pion production cross-sections and active-target geometry once design is specified |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available for cross-referencing is `21-spherical-tokamak-hts` (Tokamak Energy). Muon-catalyzed fusion is architecturally and physically so different from MFE that most structural assumptions do not transfer. The cross-concept overlap is narrow but real.

**Shared assumptions from 21-spherical-tokamak-hts:**

- **Tritium supply constraint**: Global tritium inventory (~25–30 kg), startup requirement (~1 kg at >$35,000/g), CANDU production decline, and TBR > 1 self-sufficiency requirement are identical for any D-T fusion plant [analyses/21-spherical-tokamak-hts §Section 4]. MCF does not escape the tritium sequencing problem despite its non-plasma architecture.
- **14.1 MeV neutron management**: D-T fusion at any scale produces 14.1 MeV neutrons, requiring full shielding infrastructure and a breeding blanket [dossier.md §Neutron Management]. Neutron wall loading and shielding costs are conceptually shared with all D-T concepts, though chamber geometry differs radically.
- **Regulatory cost uncertainty**: The Stewart & Shirvan 2.2× building cost multiplier for fission-style regulation is applicable to MCF as a D-T nuclear facility, though the regulatory precedent for a non-plasma fusion concept is even less defined than for MCF.

**Key divergences from any approved MFE/IFE analysis:**

- **No plasma confinement subsystem**: MCF eliminates the single largest capital cost category in MFE (HTS magnets, vacuum vessel, heating systems) and the largest capital uncertainty in IFE (driver system, target fabrication). It replaces them with a particle accelerator — a fundamentally different cost structure with different scaling behavior.
- **REBCO tape supply chain constraint does not apply**: The dominant supply chain bottleneck in all HTS tokamak/stellarator analyses is irrelevant to MCF. This is a genuine structural advantage.
- **Energy balance is the primary LCOE driver, not capital cost per se**: In MFE and IFE analyses, capital cost dominates the LCOE corridor (70–85% in most scenarios). In MCF, the recirculating power fraction (47% claimed) is so large that it rivals capital cost as an LCOE driver. A 47% recirculating fraction with a $0.025/kWh gross LCOE leaves only 53% of gross production as net output — fundamentally different from MFE where recirculating power is typically 15–25%.
- **Room-temperature fusion — no plasma physics uncertainties**: MCF eliminates the entire suite of plasma physics uncertainties (confinement time, beta limits, disruptions, ELMs, divertor heat loads, neutron activation of plasma-facing components at extreme heat fluxes). These are replaced by accelerator beam dynamics and μCF quantum mechanical process uncertainties — different, but better-characterized at the fundamental physics level.

**Nearest conceptual neighbors in the broader landscape**:

No concept is a close structural twin to MCF — the particle accelerator driver is unique in the concept landscape. However, three concepts share specific TEA-relevant structural features and are worth positioning against:

1. **Heavy-Ion Beam ICF (`25-heavy-ion-beam-icf`) — most structurally similar**: Both rely on a large particle accelerator as the cost-dominant capital item, and both face the same "driver-cost scales inversely with efficiency" challenge. The difference is physics of energy deposition: heavy-ion ICF compresses a D-T target to ignition via beam heating in a single shot; MCF uses the muon as a quantum catalyst in a continuous process. TEA implication: heavy-ion ICF cost modeling patterns for the driver (linear induction accelerator cost, repetition rate economics) are directionally applicable but use different beam parameters (GeV-class hadrons vs. μA-to-mA proton currents for muon production). Neither concept has a published plant-scale driver cost estimate, so both share the "accelerator cost is a blocking gap" problem.

2. **MagLIF (`07-maglif`) — same dominant LCOE structure**: MagLIF's pulsed power driver is the cost-dominant capital item, and MagLIF faces a conceptually identical energy-sink-at-current-state problem — current Z-machine performance (shot yield, driver energy) does not achieve net electricity. The shared TEA lesson: driver-cost-dominated concepts with net-negative Q at demonstrated parameters require the model to explicitly represent the Q threshold as a viability gate rather than a sensitivity parameter. MagLIF cost modeling (pulsed power capital at $/kJ scale; repetition rate economics) is not directly transferable (MCF uses CW, not pulsed, operation), but the scenario framing — "viable" vs. "sink" scenarios separated by a physics threshold — is directly reusable.

3. **Electrostatic Hybrid (`13-electrostatic-hybrid`) — same "external power input drives fusion" structure**: Avalanche Energy's Orbitron also uses a high-voltage external power input (300 kV electrostatic acceleration) to drive fusion in a non-burning, non-plasma device. Both MCF and the electrostatic hybrid face the fundamental challenge that recirculating power fraction is the primary LCOE lever, not capital cost. Neither achieves plasma burning — both require continuous driver power. TEA implication: the recirculating-power-fraction cost corridor (47% for MCF; ~40–60% estimated for electrostatic) is the dominant modeling challenge in both, replacing the confinement time uncertainty in MFE concepts. Cross-concept note: electrostatic hybrid (13-electrostatic-hybrid) is much lower TRL overall with no path to net gain documented in available sources — MCF's physics literature is significantly more developed.

---

## Section 8: Sources

**1. Seth Newburg, Acceleron Fusion — ARPA-E BETHE Program Presentation (July 2025)**
- Full citation: Newburg, S. (2025) "Muon Catalyzed Fusion," ARPA-E BETHE Program Presentation, July 2025. Acceleron Fusion.
- Contribution: Primary engineering reference for the entire analysis. Source for active-target muon source design, ML-optimized geometry, 47% recirculating power fraction, $0.025/kWh LCOE target, energy-vs-physics cost contour plot (~200 fusions/muon at 2.5 GeV for $0.025/kWh), superconducting accelerator + Brayton BOP assumptions, diamond anvil cell experimental apparatus, "PRELIMINARY" DT cycling rate data, 5-year roadmap to Brookhaven breakeven test. Central source for all Acceleron-specific quantitative claims.
- Location: Phase 1a source [iter-01/sources/acceleron-arpa-e-presentation-2025.md]

**2. Wikipedia — Muon-Catalyzed Fusion (Physics Reference)**
- Contribution: Comprehensive coverage of μCF physics constraints. Source for: Jackson (1957) foundational analysis, alpha-sticking probability (original ~1%, revised 0.3–0.5%), Los Alamos LAMPF 150 fusions/muon record, ~6 GeV current muon production energy cost, Kelly-Hart-Rose (2021) energy balance calculation (14% electrical net output at 150 fusions/muon + 18% accelerator efficiency), muon lifetime (2.2 μs), history of experimental milestones (Alvarez 1956, Jones et al., PSI, TRIUMF, RAL). Provides physics ceiling on commercial viability.
- Location: Phase 1a source [iter-01/sources/muon-catalyzed-fusion-physics.md]

**3. Acceleron Fusion — Company Overview**
- Contribution: Secondary reference for high-level concept positioning. Source for: 100 MWe target plant size, 500–1000°C operating temperature, fossil fuel plant conversion potential as market entry strategy, PSI experimental campaign (September 2024), company history (founded 2008, spun off 2022). No quantitative cost or engineering data beyond those from the ARPA-E presentation.
- Location: Phase 1a source [iter-01/sources/acceleron-company-overview.md]

**4. Phase 1a Dossier — Muon-Catalyzed Fusion (D-T)**
- Contribution: Synthesized Phase 1a research results. Source for: 300 fusions/muon stretch target, 3 GeV/muon energy cost target confirmation, TBD tritium breeding assessment, medium-confidence energy capture classification (Brayton unconfirmed), complete differentiation table with citations.
- Location: knowledge/concept_research/16-muon-catalyzed-fusion/dossier.md

**5. Kamimura, M.; Kino, Y. et al. — arXiv:2112.08399 (2021, rev. 2023)**
- Full citation: Kamimura, M.; Kino, Y. (2021, revised 2023). "Comprehensive study of muon-catalyzed nuclear reaction processes in the dtμ molecule." arXiv:2112.08399.
- Contribution: Theoretical calculation of the initial α-μ sticking probability (ω_S⁰ = 0.857%) using coupled-channels Schrödinger equation for the dtμ molecule. Establishes that ω_S⁰ is "~7% smaller than literature values (≃0.91–0.93%)." Source for the initial sticking value cited in Section 2 Challenge 2 and Section 5 parameter table. Also provides dtμ fusion rate (1.15×10¹² s⁻¹) and muon emission energy spectra.
- Location: Phase 1a source [iter-01/sources/arxiv-2112-08399.md]

**6. Prior Approved Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-reference for D-T tritium supply constraints, REBCO HTS tape supply chain characterization (cited to establish the non-applicability of this constraint to MCF), regulatory cost multiplier. Supply chain figures for tritium (~25–30 kg global inventory, >$35,000/g) and blanket materials cited from this analysis.
- Location: analyses/21-spherical-tokamak-hts/analysis.md
