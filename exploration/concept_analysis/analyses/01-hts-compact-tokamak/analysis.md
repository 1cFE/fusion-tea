---
ID: 01-hts-compact-tokamak
Concept: HTS Compact Tokamak
Company: Commonwealth Fusion Systems
Status: approved
Created: 2026-03-20
Approved-Date: 2026-03-20
Reuses: []
---

# D1+ Analysis: HTS Compact Tokamak (Commonwealth Fusion Systems)

---

## Section 1: Availability of Data

**Rating: Rich**

The HTS compact tokamak pursued by Commonwealth Fusion Systems (CFS) is the best-documented private fusion venture and among the most thoroughly analyzed fusion concepts in the public literature. Data availability spans peer-reviewed physics design papers, independent techno-economic analyses, company communications, and third-party engineering studies. This is unusual: most private fusion companies release far less.

**Peer-reviewed physics and engineering design:**
- Sorbom et al. (2015) published the foundational ARC conceptual design paper in *Fusion Engineering and Design*, providing full physics and engineering parameters (plasma dimensions, field strengths, blanket design, energy conversion baseline) for the original ARC configuration [arc-reactor-specifications.md; Sorbom et al. 2015].
- Creely et al. (2020) published the SPARC overview in *Journal of Plasma Physics*, giving detailed physics parameters for the burning plasma experiment under construction [dossier.md].
- Lin & Wright et al. (2020) published the ICRF heating physics basis for SPARC — one of few heating-system-specific design papers for any private fusion concept [sparc-icrf-heating-paper.md].

**Techno-economic analyses (independent):**
- Araiinejad & Shirvan (2025) published the most detailed publicly available TEA for a D-T magnetic confinement fusion power plant in *Applied Energy*, directly applicable to ARC-class compact tokamaks [handwritten exemplar, 01-hts-compact-tokamak.md]. This study quantifies the impact of regulatory scenarios, blanket costs, and capacity factor uncertainties on LCOE.
- Colliva et al. (2024) independently studied three power conversion cycles for ARC-like tokamaks using GE GateCycle software, concluding that supercritical steam Rankine is "the most promising solution" among the options studied [arc-power-conversion-studies.md].
- Segantin et al. (2020) conducted an earlier thermodynamic cycle study for ARC, treating Rankine as the baseline reference [arc-power-conversion-studies.md].

**System codes and modeling frameworks:**
- The PROCESS system code (UKAEA) provides physics-consistent design point calculations for tokamak configurations including compact high-field variants [handwritten exemplar].
- Woodruff Scientific's pyFECONS framework (Woodruff, 2026, arXiv:2601.21724) provides a costing framework applicable to ARC-class plants [handwritten exemplar].
- The ARIES series of studies (late 1990s–early 2000s) established cost accounting baselines for tokamak power plants that are still referenced in current TEA work [handwritten exemplar].

**Company transparency:**
CFS is more transparent than most private fusion companies, though it stops well short of the detail needed for a bottom-up cost model. Published material includes: the ARC conceptual design (Sorbom 2015), SPARC physics papers, blog posts describing SPARC assembly milestones, PPA announcements (Google 200 MW, Eni >$1B covering remaining capacity), a Virginia site announcement, and periodic technology milestone communications [cfs-2025-2026-updates.md]. CFS has not published detailed cost estimates for SPARC or ARC, engineering drawings, or a formal power plant study updated from the 2015 Sorbom paper.

**Phase 1a dossier coverage:**
The Phase 1a dossier achieved high overall confidence across all 13 differentiation columns. The only medium-confidence item is the energy conversion cycle (Rankine vs. Brayton), where CFS has not made a public commitment despite multiple published academic analyses favoring steam Rankine [dossier.md].

**Key data gaps limiting this analysis:**
1. No published NOAK cost estimate for ARC. The most applicable TEA (Araiinejad & Shirvan 2025) is based on a generalized D-T MCF plant, not ARC-specific parameters.
2. No published capacity factor target or availability analysis for ARC from CFS.
3. ARC thermal output has evolved from ~525 MW (Sorbom 2015) to an implied higher figure supporting 400 MWe net [cfs-2025-2026-updates.md], but no updated physics paper documents the current design point.
4. FLiBe system engineering (pump design, tritium extraction, heat exchanger materials) is not detailed in available public sources.

---

## Section 2: Challenges in Capturing System Function

The HTS compact tokamak is among the easier fusion concepts to build an LCOE model for — its steady-state thermal operation fits conventional power plant cost structures, and the plasma physics basis is the most mature in fusion. But several challenges introduce significant modeling uncertainty, ranked by LCOE impact:

**1. CAPEX uncertainty: magnets and the REBCO scaling bet**

The ARC economic thesis rests on the claim that HTS magnets enable compact, high-power-density operation that lowers cost per kWe. But the REBCO tape supply chain is thin, and the current cost of REBCO tape ($30–100/kA-m, depending on source) far exceeds the ~$10/kA-m or better range that would make commercial viability straightforward [handwritten exemplar; Whyte 2024]. A single ARC-class reactor requires >5,000 km of REBCO tape [handwritten exemplar], and no public bottom-up cost estimate for the ARC magnet system has been published by CFS. The magnet system is simultaneously the key enabling technology and one of the largest single capital items. Its cost is highly uncertain — it is a novel product being manufactured at a scale the industry has never attempted.

The Araiinejad & Shirvan (2025) study is the most useful public proxy, but it applies a generalized reactor cost model rather than ARC-specific parameters. The compact high-field design should in principle lower reactor building size and cost relative to a large-aspect-ratio tokamak, but this benefit has not been directly verified against a detailed bottom-up cost account.

**2. Capacity factor: maintenance-driven downtime is the second-largest LCOE lever**

For a D-T tokamak, the breeding blanket, first wall, and divertor are activated and require remote replacement on a timescale of years. The frequency of these outages is the dominant driver of capacity factor [handwritten exemplar]. ARC's liquid FLiBe blanket design partially addresses this: liquid blanket replacement (draining and refilling the FLiBe pool) is likely faster than solid module extraction, but the full maintenance cycle for a FLiBe-immersion blanket at neutron fluences has never been demonstrated or scheduled in detail. The Araiinejad study shows that capacity factor assumptions have among the largest LCOE sensitivities. CFS has not published a capacity factor target for ARC.

**3. FLiBe system engineering: a novel coolant/breeder with high coupling**

The ARC design integrates tritium breeding, neutron shielding, and primary heat removal into a single FLiBe loop [arc-reactor-specifications.md]. This is elegant but creates tight coupling between systems: FLiBe chemistry control, tritium extraction, beryllium toxicity management, heat exchanger material compatibility, and pump reliability are all interdependent. No large-scale FLiBe system has operated at fusion-relevant conditions. Kairos Power (fission) is developing FLiBe technology and could provide supply chain synergies, but their operating conditions differ materially from a fusion first wall [handwritten exemplar].

**4. Regulatory uncertainty**

The 2023 NRC decision to regulate fusion under 10 CFR Part 30 is favorable, but detailed rulemaking remains incomplete. A study by Stewart & Shirvan (2022) demonstrates that applying fission-style nuclear regulation would result in a 2.2× markup on building costs. Araiinejad's scenario analysis combines this building cost factor with higher indirect cost percentages and reduced capacity factor, nearly doubling overnight capital cost and quadrupling the LCOE spread [handwritten exemplar]. The actual regulatory cost burden for an ARC-class plant is unresolved and represents a potentially blocking uncertainty.

**5. Quasi-steady-state operation: plasma control and availability**

ARC targets quasi-steady-state operation with burns of "tens of minutes at a time" [cfs-2025-2026-updates.md], enabled by a combination of LHCD current drive and bootstrap current. The SPARC precursor operates in fully pulsed mode (10-second flat-top), so quasi-steady ARC operation has not been demonstrated. If burns are shorter than expected, plasma restart frequency increases, which increases wear on heating/current-drive components and affects availability. The FLiBe thermal mass absorbs pulse-to-pulse variation, so grid output remains continuous — but plasma availability (fraction of time in burn) affects blanket temperature, tritium production, and electrical output [cfs-2025-2026-updates.md]. This coupling is not well-characterized in public sources.

**6. Tritium startup inventory and self-sufficiency**

The global tritium inventory is ~25–30 kg and is declining as CANDU reactors age [handwritten exemplar]. A single ARC plant requires on the order of 1 kg startup inventory at >$35,000/kg. Fleet scaling requires demonstrated TBR > 1.0 in operating conditions, not just simulated. The ARC FLiBe blanket is designed for TBR ≥ 1.1 (optimized to ~1.22) [arc-reactor-specifications.md], which provides margin, but this has not been validated at relevant neutron fluences.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (most risk to LCOE model) to most mature.

---

**FLiBe Liquid Blanket System — TRL 3–4**

- **Demonstrated**: Small-scale FLiBe flow loops and heat transfer experiments. Kairos Power fission reactor uses FLiBe as primary coolant (ongoing construction). Tritium breeding from FLiBe demonstrated at laboratory scale. ARC blanket design published (Sorbom et al. 2015) with TBR calculations showing ≥1.1 achievable.
- **On paper only**: Full-scale FLiBe immersion blanket integrating tritium breeding, neutron shielding, and primary heat removal under simultaneous neutron + heat + tritium extraction loads. High-temperature FLiBe outlet (900 K baseline, up to 1200 K) heat exchanger designs with Hastelloy-N or equivalent materials.
- **Missing at scale**: Tritium extraction from FLiBe at kg/day rates. FLiBe purification at power plant throughput. Pumping systems for high-temperature, tritium-bearing, beryllium-containing molten salt at fusion-relevant scale. Long-term materials compatibility data for Hastelloy-N under combined fusion neutron + FLiBe corrosion + tritium permeation conditions.

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: Lab-scale tritium handling. JET and TFTR handled gram-level tritium quantities in D-T operation. Tritium extraction from liquid breeders demonstrated at bench scale.
- **On paper only**: Closed-loop kg/day-scale self-sufficient fuel cycle for a commercial plant. Near-zero tritium loss (<1%) from the combined blanket + plasma exhaust + gas processing system.
- **Missing at scale**: Industrial tritium processing plant sized for a commercial fusion plant. Permeation barriers for FLiBe heat exchangers at plant-relevant temperatures and neutron flux. Demonstrated TBR > 1.0 in operating conditions (all current TBR data are from simulation or fission-neutron experiments, not 14 MeV fusion neutrons).

---

**Remote Maintenance System — TRL 5–6**

- **Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for blanket and divertor exchange. Significant investment in radiation-hardened robotics for ITER maintenance operations.
- **On paper only**: ARC-specific remote maintenance scheme for FLiBe drain/refill, tungsten first-wall inspection and replacement, and divertor servicing in a compact high-field configuration. Reliable, high-availability remote maintenance enabling >80% plant capacity factor.
- **Missing at scale**: Radiation-hardened robotics capable of multi-year operation inside the vessel with minimal human intervention. Remote maintenance cycle times needed to achieve the planned capacity factor for ARC.

---

**Divertor — TRL 5–7**

- **Demonstrated**: Tungsten monoblock divertors tested at >10–20 MW/m² in WEST, GLADIS, and DTT test facilities. Detached/radiative divertor operation demonstrated in multiple tokamaks (DIII-D, JET, AUG). ARC uses a high-field-side divertor configuration (scrape-off layer design different from ITER).
- **On paper only**: Advanced ARC divertor geometry at full fusion power and neutron fluence. Long-term divertor performance under simultaneous neutron damage + heat loading + tritium co-deposition in a compact high-field geometry.
- **Missing at scale**: Materials that survive steady-state 10–20 MW/m² plus 14 MeV neutron damage for years. Full-scale remote replacement system for an ARC-class compact divertor. Validated detachment regime in the compact, high-density ARC plasma regime.

---

**HTS Magnets (REBCO TF/PF/CS Coils) — TRL 5–8**

- **Demonstrated**: 20 T large-bore HTS test magnet demonstrated by CFS in September 2021 — the key proof-of-concept milestone [dossier.md]. Tokamak Energy Demo4 achieved 11.8 T in full tokamak configuration (November 2025). SPARC TF coil installation is underway (first of 18 coils installed as of CES 2026) [cfs-2025-2026-updates.md]. Full SPARC magnet ring expected by end of summer 2026. CFS has demonstrated both wound (NINT) and cable-in-conduit (PIT VIPER) HTS coil architectures.
- **On paper only**: Full magnet system for an ARC-class power plant (larger geometry, higher field than SPARC). Demountable joint performance under neutron irradiation over multi-year plant lifetime. Full quench protection system for a complete plant magnet set in a neutron environment.
- **Missing at scale**: REBCO tape production at thousands of km/year with tight Jc specifications (>150 MA/cm² at 20 K, 20 T). Radiation-hardened magnet insulation for fusion-relevant neutron fluence. Long-term fatigue data under combined high-field + cyclic thermal loading for demountable joint interfaces.

---

**ICRF / LHCD Heating and Current Drive — TRL 6–8**

- **Demonstrated**: SPARC will use 25 MW ICRF at 120 MHz via 4-strap antennas in 7 ports [sparc-icrf-heating-paper.md]. ICRF systems have operated routinely on JET, AUG, Alcator C-Mod. Lower hybrid current drive (LHCD) systems have operated on Alcator C-Mod, JT-60SA, and EAST. ARC design uses 25 MW LHCD + 13.6 MW ICRF.
- **On paper only**: Continuous-wave, high-efficiency ICRF + LHCD systems at 25–40 MW total with >50% wall-plug efficiency under ARC operating conditions. Validated current-drive efficiency sufficient to maintain quasi-steady-state operation for tens of minutes.
- **Missing at scale**: Long-term antenna reliability under neutron + gamma background in an ARC geometry with compact wall-to-antenna clearances. Demonstrated quasi-steady-state sustainment in a burning plasma (all existing current drive experience is in non-burning, non-self-heated plasmas).

---

**Vacuum Vessel and In-Vessel Structures — TRL 7–8**

- **Demonstrated**: ITER vacuum vessel sectors (double-walled Inconel/stainless steel) being manufactured and welded at full scale. ARC design uses double-walled Inconel 718 vacuum vessel. Small-scale manufacturing of Inconel 718 structures is well-established.
- **On paper only**: Full-scale ARC vacuum vessel manufacturing with tolerance control adequate for magnet alignment. Integration with FLiBe blanket inlet/outlet ports and ICRF/LHCD antenna feedthroughs.
- **Missing at scale**: Qualification of large-scale Inconel 718 welds for activation and remote maintenance requirements. Full integration challenge with demountable magnets (vessel must accommodate magnet opening for maintenance access, unlike ITER).

---

**Cryogenics and Thermal Management — TRL 7–8**

- **Demonstrated**: Large-scale helium refrigeration plants at ITER scale designed and tested. Smaller-scale 20 K cryoplants for HTS magnet testing (CFS, Tokamak Energy) operational. HTS coil operating temperature (~20 K) is warmer than LTS coils, reducing cryogenic plant size and cost relative to Nb₃Sn-based designs.
- **Missing at scale**: Optimized 20 K cryoplant design for an ARC-class plant accounting for neutron-induced heat loads in the cryogenic structures. Thermal cycle performance under the quasi-pulsed plasma operation schedule.

---

**Balance of Plant (Power Conversion, Turbine, Heat Rejection) — TRL 8–9**

- **Demonstrated**: Conventional Rankine steam cycle at GW scale is mature commercial technology. Supercritical steam Rankine (as recommended by Colliva et al. 2024 for ARC) is standard in modern coal and combined-cycle plants.
- **Missing at scale**: Integration with FLiBe primary loop at ARC operating temperatures (900–1200 K outlet). Tritium-compatible heat exchangers between primary FLiBe and secondary water loops. Qualification of heat exchanger materials for FLiBe chemistry at fusion-relevant temperatures.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck**

Global REBCO production capacity is on the order of a few thousand kilometers per year across all manufacturers. A single ARC-class reactor requires >5,000 km of tape [handwritten exemplar]. Scaling production by one to two orders of magnitude while reducing cost from the current $30–100/kA-m range to the ~$10/kA-m level needed for commercial viability requires massive capital investment in tape manufacturing facilities. Current major producers include Shanghai Superconductor Technology, Faraday Factory Japan, and CFS's own tape manufacturing effort. The supply chain is ramping but not yet at the scale needed for even a single commercial plant, let alone a fleet. There is a shared demand signal from medical MRI, industrial NMR, and other superconducting magnet applications, but fusion applications would dwarf current market volume. Cost and supply risk is the highest of any CFS-specific material.

**Tritium — Declining External Supply**

The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU reactor byproduct, and decays at 5.5%/year [handwritten exemplar]. A single D-T reactor startup requires ~1 kg. As CANDU reactors retire, external tritium supply will shrink, creating a sequencing constraint: early fusion plants must demonstrate tritium self-sufficiency (TBR > 1 in operation) before the fleet can scale. The ARC FLiBe blanket is designed for TBR ≥ 1.1 [arc-reactor-specifications.md], providing margin. Market price is >$35,000/g, making tritium startup inventory a material capital cost item (~$35M per kilogram needed). The tritium fuel cycle — extraction from FLiBe, purification, storage, and accountability — involves handling a radioactive gas with extremely low tolerable release limits, adding regulatory complexity.

**FLiBe Molten Salt (Li₂BeF₄) — Not Produced at Industrial Scale**

FLiBe is not currently produced at industrial scale for any application. Beryllium, one of its components, is toxic and produced in limited global quantities (~300 tonnes/year, dominated by Materion Corp in the US) [handwritten exemplar]. Lithium enrichment for tritium breeding (requiring >90% Li-6, up from the natural 7.5%) has only a few global suppliers, with Russia and China relying on a mercury-based enrichment process banned elsewhere. The Araiinejad study estimates NOAK FLiBe cost at ~$154/kg assuming a 20% learning rate [handwritten exemplar]. FLiBe shares a supply chain with Kairos Power (fission), which could aid economies of scale, but Kairos FLiBe volumes are modest compared to a fusion fleet. The FLiBe inventory for ARC (estimated tens of cubic meters in the blanket cavity) represents a meaningful capital cost that scales with plant size.

**Tungsten — Manufacturing-Limited, Not Supply-Limited**

Tungsten for the first wall (1 cm W layer in ARC design [arc-reactor-specifications.md]) and divertor is available in adequate supply globally. The manufacturing challenge is fabricating large, precisely shaped tungsten components — divertor monoblock tiles, first-wall cladding — that withstand extreme heat loads and thermal cycling without cracking. Tungsten becomes brittle after neutron irradiation, and the combination of high-temperature operation, neutron damage, and pulsed thermal loading creates a challenging materials environment. Tungsten supply is not a bottleneck; tungsten manufacturing and quality control at power plant scale is an open R&D problem.

**Inconel 718 (Vacuum Vessel) — Available but Specialized**

Inconel 718 is used for the ARC vacuum vessel. This is a mature aerospace alloy with established manufacturing infrastructure. Supply at the tonnes scale needed for a single reactor vessel is not a concern, but precision fabrication of complex double-wall vacuum vessel geometries with the tight tolerances required for magnet alignment represents a specialized manufacturing challenge.

**Titanium Hydride (TiH₂) for Neutron Shielding — Limited Data**

ARC uses TiH₂ as a neutron shield to protect the HTS magnets [arc-reactor-specifications.md]. TiH₂ is commercially available, but its behavior under fusion-relevant 14 MeV neutron irradiation (hydrogen gas release, swelling, thermal conductivity changes) at the scale and fluence of an ARC power plant is not characterized. This is a unique ARC design feature not shared with other tokamak designs and represents an R&D gap.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (ARC) | 400 MWe | CFS 2025–2026 announcements; Google/Eni PPAs [cfs-2025-2026-updates.md] | high | Updated from 270 MWe in Sorbom 2015; current commercial design target |
| Net electrical output (ARC, original) | ~270 MWe | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | Original design; superseded by 400 MWe in current plans |
| Fusion thermal power (ARC) | ~525 MW (Sorbom 2015); ~1 GW implied by 400 MWe target | Sorbom et al. 2015; [arc-reactor-specifications.md] | medium | Sorbom 2015 gives 525 MW; 400 MWe output at 30–40% thermal efficiency implies ~1–1.3 GW fusion power unless efficiency improved; no updated physics paper |
| Fusion gain Q (ARC) | ~13.6 | Sorbom et al. 2015 [arc-reactor-specifications.md; dossier.md] | high | Design target in published paper; above burning plasma threshold |
| Fusion gain Q (SPARC) | ~11 | Creely et al. 2020 [dossier.md] | high | Burning plasma experiment; Q=11 is design point |
| SPARC fusion thermal power | 140 MW | Creely et al. 2020 [arc-reactor-specifications.md] | high | Proof-of-concept experiment, not power plant |
| On-axis toroidal field (ARC) | 9.2 T | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| Peak field in coils (ARC) | 23 T | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | Sets REBCO tape operating requirements |
| Major radius (ARC) | 3.3 m | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| Minor radius (ARC) | 1.1 m | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| Plasma current (ARC) | 7.8 MA | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| Thermal-to-electric efficiency | 30–40% | Sorbom et al. 2015 (30% Rankine baseline); Colliva et al. 2024; Segantin et al. 2020 [arc-power-conversion-studies.md] | medium | 30% for baseline Rankine; sCO2 Brayton could reach 40%+; CFS has not committed to a cycle |
| FLiBe blanket operating temperature (outlet) | ~900 K (baseline), scalable to 1200 K | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | Sets thermodynamic cycle efficiency ceiling |
| Tritium breeding ratio (TBR) | ≥1.1 (optimized to ~1.22) | Sorbom et al. 2015 [arc-reactor-specifications.md; dossier.md] | high | Simulated; unvalidated at fusion-neutron fluences |
| Neutron power capture fraction (FLiBe) | ~80% | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | FLiBe captures ~80% of neutron energy; remainder in first wall and shielding |
| ICRF heating power (SPARC) | 25 MW at 120 MHz | Lin & Wright et al. 2020 [sparc-icrf-heating-paper.md] | high | Sole auxiliary heating method on SPARC |
| ARC heating/current drive | 25 MW LHCD + 13.6 MW ICRF | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | LHCD for current drive; ICRF for heating |
| Operation mode | Quasi-steady-state (burns of tens of minutes) | CFS blog; cfs-2025-2026-updates.md | high | FLiBe thermal mass enables continuous steam generation |
| SPARC operation mode | Pulsed: 10 s ramp-up, 10 s flat-top, 10 s ramp-down; 20 min–1 hr cooling gap | cfs-2025-2026-updates.md | high | SPARC is the physics proof step |
| ARC commercial capacity (PPAs) | 400 MWe (200 MW Google PPA + Eni >$1B covers remainder) | cfs-2025-2026-updates.md | high | Fully subscribed; Virginia site (Chesterfield County) |
| Total CFS funding | ~$2B+ (including $863M Series B2, September 2025) | cfs-2025-2026-updates.md | high | Not directly an LCOE parameter but indicates investor confidence in NOAK cost projections |
| SPARC first plasma target | 2027 | cfs-2025-2026-updates.md | medium | Company announced; timeline uncertainty applies |
| ARC grid connection target | Early 2030s | cfs-2025-2026-updates.md | medium | Company announced; contingent on SPARC success and ARC construction start |
| Normalized beta (ARC) | 3.3 | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| Energy confinement time (ARC) | ~0.64 s | Sorbom et al. 2015 [arc-reactor-specifications.md] | high | |
| REBCO tape cost (current market) | $30–100/kA-m | Handwritten exemplar; Whyte 2024 | medium | Wide range reflects supplier variation and quantity |
| REBCO tape required per ARC | >5,000 km | Handwritten exemplar | medium | Order-of-magnitude estimate; exact figure unpublished by CFS |
| REBCO tape cost target (commercial viability) | ~$10/kA-m | Handwritten exemplar; Whyte 2024 | medium | Industry consensus target; not yet achieved at volume |
| FLiBe NOAK cost estimate | ~$154/kg (20% learning rate assumed) | Araiinejad & Shirvan 2025, cited in handwritten exemplar | medium | Model-derived, not measured; depends heavily on learning rate assumption |
| Tritium market price | >$35,000/g | Handwritten exemplar | medium | Rough current market; highly variable |
| Regulatory cost multiplier (fission-style regulation scenario) | 2.2× building cost markup | Stewart & Shirvan 2022, cited in handwritten exemplar | medium | Upper-bound scenario; not expected under 10 CFR Part 30 but not fully resolved |
| Blanket neutron power multiplication | [inferred] ~1.1–1.2 | Analogy to ARC FLiBe blanket design; standard tokamak blanket physics | medium | FLiBe (n,α) reactions on Li-6 produce some energy multiplication; exact value for ARC not published |
| Plant capacity factor | Not published | — | — | See missing parameters below |
| ARC overnight capital cost ($/kWe) | Not published | — | — | See missing parameters below |

---

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Plant capacity factor | proprietary / not-yet-sourced | blocking | CFS has not published a capacity factor target. This is a primary LCOE sensitivity. ARIES-AT used ~85%; Araiinejad study treats 75–90% as the uncertainty range. FLiBe maintenance cycle and plasma restart frequency are the key sub-inputs. |
| Overnight capital cost ($/kWe or $M total) | proprietary | blocking | No public bottom-up cost estimate for ARC. Araiinejad & Shirvan 2025 is the closest proxy (generalized D-T MCF plant). ARC's compact design should reduce building and vessel costs, but no CFS-specific estimate has been published. |
| Updated fusion power / plasma design for 400 MWe ARC | not-yet-sourced | blocking | Sorbom 2015 gives 525 MW fusion power and 270 MWe net. The updated 400 MWe target implies significantly higher fusion power or higher thermal efficiency, but no updated physics paper has been published. The gap between 270 MWe and 400 MWe (~48% increase) represents a substantial design change. |
| Component replacement schedule (first wall, divertor, FLiBe system) | proprietary / not-yet-sourced | important | Replacement frequency directly determines maintenance downtime and capacity factor. ARC's liquid blanket complicates direct analogy to solid-blanket tokamak maintenance studies. |
| Recirculating power fraction | derivable | important | Can be estimated from Q_eng relationship: net electric output = fusion thermal × η_th × (1 – f_recirc). At Q≈13.6 and η_th=30–40%, recirculating power fraction should be modest (<15%), but the exact figure depends on cryogenic load (20 K HTS is lower than LTS but non-negligible), LHCD/ICRF auxiliary power, and balance-of-plant pumping. |
| REBCO tape cost at ARC production volume | not-yet-sourced / proprietary | important | CFS is reportedly investing in tape manufacturing. No public $/kA-m projection for the volume required by a commercial fleet. |
| FLiBe inventory volume and cost for ARC | derivable | important | Blanket cavity volume is determinable from published ARC geometry; FLiBe density is known. FLiBe cost at volume is uncertain (see Araiinejad $154/kg estimate). |
| ARC magnet system cost | proprietary | important | The magnet system (TF + PF + CS coils) is likely the single largest capital cost item. No public estimate from CFS. |
| SPARC D-T performance data | truly-unknown | important | SPARC first plasma is targeted for 2027. No experimental burning plasma data from CFS exists yet. SPARC performance will validate (or revise) the physics basis for ARC. |
| Tritium startup inventory requirements | derivable | important | Derivable from ARC plasma volume and tritium inventory model; not explicitly published for the current ARC design. |
| TiH₂ neutron shield cost and performance | truly-unknown | nice-to-have | Unique ARC design feature; no irradiation data or cost estimate in public literature. |
| Power conversion cycle efficiency (committed) | proprietary | nice-to-have | Multiple studies favor supercritical steam Rankine at ~30–35%. CFS has not committed. The choice affects both thermal efficiency and heat exchanger material requirements. |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Plant capacity factor — CFS has published no target | S1, S5 | proprietary | blocking | Apply Araiinejad & Shirvan (2025) sensitivity range (75–90%) as uncertainty bracket. ARIES-AT (85%) as central estimate pending ARC-specific data. |
| 2 | ARC overnight capital cost ($/kWe) | S1, S5 | proprietary | blocking | Use Araiinejad & Shirvan (2025) generalized D-T MCF study as proxy; apply compact-design adjustment factor for smaller building and vessel. Flag as highly uncertain. |
| 3 | Updated ARC design point for 400 MWe (fusion power, Q, plasma parameters) | S1, S2, S5 | not-yet-sourced | blocking | Watch for CFS publications. Current model must bridge 2015 Sorbom paper and current 400 MWe claim — requires assumption about fusion power increase or efficiency improvement. |
| 4 | Component replacement schedule and maintenance downtime | S3, S5 | proprietary / not-yet-sourced | important | Review ARIES-AT and PROCESS outputs for comparable compact tokamak designs. FLiBe drain/refill cycle needs engineering estimate. |
| 5 | REBCO tape cost at ARC production volume | S4, S5 | not-yet-sourced / proprietary | important | Monitor CFS tape manufacturing announcements. Use $10/kA-m as target assumption in optimistic scenario; $30–50/kA-m as conservative. |
| 6 | ARC magnet system cost | S3, S5 | proprietary | important | Brown (2018) IEEE comparison of MCF cost elements provides a reference framework. Apply to ARC magnet dimensions and REBCO tape cost assumptions. |
| 7 | Recirculating power fraction (Q_eng) | S5 | derivable | important | Derive from Q≈13.6, η_th≈30–35%, cryogenic load (estimate from SPARC-analogous system), and auxiliary heating power. Central estimate: Q_eng ≈ 5–8. |
| 8 | FLiBe inventory volume and cost | S4, S5 | derivable | important | Derive from ARC blanket cavity geometry (Sorbom 2015). Apply Araiinejad $154/kg NOAK estimate. |
| 9 | SPARC experimental validation of physics basis | S3 | truly-unknown | important | SPARC first plasma 2027. Key metrics to watch: achieved Q, confinement scaling, plasma control in burning regime. |
| 10 | TBR validation at fusion-relevant neutron fluence | S3, S4 | truly-unknown | important | No 14 MeV neutron facility can currently test ARC-scale blanket performance. Will remain unvalidated until SPARC D-T operation and early ARC operation. |
| 11 | Tritium startup inventory requirement and cost | S4, S5 | derivable | important | Estimate from ARC plasma volume and tritium inventory models. Apply >$35,000/g market price. |
| 12 | TiH₂ neutron shield irradiation performance | S3, S4 | truly-unknown | nice-to-have | Unique ARC feature. Needs dedicated neutron irradiation campaign. Not expected to be available before ARC construction. |
| 13 | Power conversion cycle commitment (Rankine vs. Brayton) | S1, S3, S5 | proprietary | nice-to-have | Colliva et al. 2024 and Segantin et al. 2020 both favor supercritical steam Rankine. Use as default assumption. |

---

## Section 7: Cross-Concept Notes

No approved prior analyses are available for cross-referencing.

Note for the pipeline: when analyses of other tokamak concepts are approved (e.g., standard aspect-ratio tokamak, spherical tokamak, CFETR-class device), the following cost structure elements should be candidates for reuse or consistent assumption:
- FLiBe blanket cost model and TBR assumptions (likely identical if FLiBe is also used)
- Tritium fuel cycle cost (shared structure across all D-T concepts)
- Balance of plant cost (mature Rankine/Brayton technology, shared across thermal concepts)
- Regulatory cost uncertainty range (applies to all D-T fusion plants)
- REBCO tape cost and supply chain (relevant to all HTS magnet concepts)

The HTS compact tokamak design differs from a standard large-aspect-ratio tokamak (e.g., DEMO, ARIES-AT) primarily in: higher magnetic field enabling compact geometry (lower building and vessel volume costs), demountable magnets enabling in-vessel access without port-based remote handling, FLiBe liquid immersion blanket (vs. solid breeding modules in most DEMO designs), and quasi-steady-state operation (vs. steady-state in some DEMO variants). These distinctions should be captured as adjustments to any shared tokamak cost framework rather than starting from scratch.

---

## Section 8: Sources

**1. Sorbom et al. (2015) — ARC foundational design paper**
- Full citation: Sorbom, B.N. et al. (2015) "ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets," *Fusion Engineering and Design*, 100, pp. 378–405. doi:10.1016/j.fusengdes.2015.06.001.
- Contribution: Core plasma and engineering parameters for ARC (dimensions, field strength, fusion power, Q, blanket design, TBR, heating systems, energy conversion baseline). The primary engineering reference for all ARC-specific parameter claims in this analysis.
- Location: Phase 1a source [arc-reactor-specifications.md]; arXiv:1409.3540

**2. Lin & Wright et al. (2020) — SPARC ICRF heating physics basis**
- Full citation: Lin, Y. and Wright, J.C. et al. (2020) "Physics basis for the ICRF system of the SPARC tokamak," *Journal of Plasma Physics*, 86, 865860506. doi:10.1017/S0022377820001245.
- Contribution: SPARC heating system design: 25 MW ICRF at 120 MHz, antenna configuration, operating scenarios, rationale for ICRF selection.
- Location: Phase 1a source [sparc-icrf-heating-paper.md]

**3. Colliva et al. (2024) — ARC power conversion cycle analysis**
- Full citation: Colliva, A. et al. (2024) "Analysis of Power Conversion System Options for ARC-like Tokamak Fusion Reactor Balance of Plant," *MDPI Sustainability*, 16(17), 7480. doi:10.3390/su16177480.
- Contribution: Independent analysis of three power conversion cycles (supercritical steam Rankine, sCO2 Brayton, He Brayton) for ARC; conclusion favoring supercritical steam Rankine as "most promising solution."
- Location: Phase 1a source [arc-power-conversion-studies.md]

**4. Segantin et al. (2020) — ARC thermodynamic cycle study**
- Full citation: Segantin, S. et al. (2020) "Exploration of power conversion thermodynamic cycles for ARC fusion reactor," *Fusion Engineering and Design*, 2020. doi:10.1016/j.fusengdes.2020.111398.
- Contribution: Earlier study of thermodynamic cycles for ARC; establishes Rankine as baseline reference case; sCO2 Brayton efficiency potential (up to 40%+).
- Location: Phase 1a source [arc-power-conversion-studies.md]

**5. CFS 2025–2026 Updates (various company sources)**
- Sources: Fortune (Jan 2026); MIT News (Dec 2024); CFS press release (Virginia site); CFS blog posts; neutronbytes.com (Series B2 announcement).
- Contribution: Current ARC design target (400 MWe), SPARC assembly milestones (first TF coil installed), PPA details (Google 200 MW, Eni >$1B), Virginia site location, timeline targets (SPARC first plasma 2027, ARC grid connection early 2030s), funding ($863M Series B2, ~$2B+ total), operation mode clarification (quasi-steady plasma, continuous grid output via FLiBe thermal storage).
- Location: Phase 1a source [cfs-2025-2026-updates.md]

**6. Araiinejad & Shirvan (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: Most detailed public TEA for D-T MCF plants; LCOE sensitivity analysis; regulatory cost scenarios; FLiBe cost estimate ($154/kg NOAK); capacity factor uncertainty ranges. Primary proxy for ARC LCOE parameters not directly published by CFS.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**7. Whyte, D. (2024) — Fusion economics presentation**
- Full citation: Whyte, D. (2024) "Fusion economics: power density, materials and maintenance." Presentation, Cassyni event, 12 September 2024.
- Contribution: REBCO tape cost targets and supply chain scaling analysis; power density argument for compact high-field tokamak economics.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]; Cassyni recording

**8. Creely et al. (2020) — SPARC overview**
- Full citation: Creely, A.J. et al. (2020) "Overview of the SPARC tokamak," *Journal of Plasma Physics*, 86. doi:10.1017/S0022377820001257.
- Contribution: SPARC engineering overview, confirmed machine parameters (R=1.85 m, Bt=12.2 T, Q~11, 140 MW fusion power), construction plan.
- Location: Phase 1a dossier [dossier.md]

**9. Stewart & Shirvan (2022) — Regulatory cost analysis**
- Contribution: Quantified fission-style regulatory scenario: 2.2× building cost markup; combined with indirect cost adjustments nearly doubles overnight capital cost.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**10. Brown (2018) — MCF cost element comparison**
- Full citation: Brown, T.G. (2018) "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148.
- Contribution: Reference framework for decomposing tokamak capital cost by component; applicable for ARC magnet and vessel cost estimation.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]
