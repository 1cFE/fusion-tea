# D1+ Analysis: HTS Tokamak - Full HTS (Energy Singularity)

**Concept**: Compact D-shaped tokamak with full HTS magnet system (all TF + PF + CS coils in REBCO)
**Company**: Energy Singularity (上海能量奇点能源科技有限公司), Shanghai, China
**Prototype**: HH70 (operating), Jingtian test magnet (operating), HH170 (Q > 10 target, ~2027)
**Commercial Demo**: HH380 (post-2030)
**Confinement Family**: MFE — Compact Tokamak

---

## Section 1: Availability of Data

**Rating: Limited**

Energy Singularity is among the least transparent private fusion companies with public documentation. After three research iterations exhausting English and Chinese-language sources, the dossier is characterized by strong milestone data on the HH70 prototype and near-total absence of commercial design parameters. The "Limited" rating (rather than "Opaque") reflects that the HH70 operational record is genuinely well-documented, but every parameter relevant to an LCOE model — net electric output, fusion power, Q for commercial machines, blanket design, thermal conversion efficiency, and capital cost — is undisclosed.

**What is documented:**

- **HH70 prototype operation**: 1,337-second steady-state plasma achieved February 2026 (shot #5,755) [energy-singularity-overview.md §HH70 Performance]. This is the most precise operational milestone in the public record. Toroidal field at plasma center: 0.6 T; maximum field on coils: 2.5 T after cryogenic upgrade [energy-singularity-overview.md §Machine Parameters].
- **Jingtian test magnet**: 21.7 T peak field (some sources: 22.4 T) achieved by a 32-layer stacked REBCO single-pancake coil assembly [energy-singularity-overview.md §Magnet System; dossier.md §Driver Technology]. This was confirmed to surpass the CFS/MIT 20 T SPARC magnet record in 2024.
- **HH170 design intent**: Q > 10 (D-T equivalent energy gain), on-axis field ~14 T (~110% of SPARC), machine volume ~70% of SPARC, D-shaped HTS coils targeting 25 T peak field, expected completion 2027 [dossier.md §Confinement Concept].
- **Company positioning**: Described as building "world's smallest and lowest-cost tokamak device capable of achieving 10-fold energy gain" [energy-singularity-overview.md §HH170 — Next-Generation Device]. Co-founder Dong Ge's stated strategic goal: "reduce the levelized cost of electricity from fusion power to that of thermal power, or even lower" [energy-singularity-technical-summary.md §Strategic Goal].
- **Supply chain localization**: >95% domestic component sourcing for HH70 and HH170 construction [energy-singularity-overview.md §Construction; dossier.md §Driver Technology].
- **HH70 heating**: ICRH (ICRF) confirmed as primary heating method; electron gun used for pre-ionization [dossier.md §Primary Heating].

**What is not documented:**

Three research iterations and 20+ sources found no public disclosure of: blanket design or TBR target, tritium breeding approach, power conversion cycle, net electric output for any commercial machine, Q for the HH380 commercial demo, capital cost estimates, heating configuration for HH170 or HH380, or neutron shielding design beyond physics-inferred requirements. The ScienceDirect commissioning paper for HH70 (Fusion Engineering and Design, 2025) was paywalled and covers an experimental machine with no D-T operation, so it is unlikely to address any of these commercial design parameters.

> "Energy Singularity seeks additional $500M for HH170"
> — energy-singularity-overview.md §Funding

> "the deep integration of HTS and AI control technologies has reached engineering feasibility, paving the way for the low-cost, high-efficiency construction of future fusion power plants"
> — energy-singularity-technical-summary.md §Dong Ge Quote

**Key data gaps limiting this analysis:**
1. No net electric output, fusion power, or Q disclosed for any commercial machine (HH380)
2. No blanket design — structurally unresolvable until HH380 engineering phase (~post-2030)
3. No thermal conversion cycle specified
4. No capital cost estimate or plant study exists
5. HH170 "D-T equivalent" framing suggests D-T may not be burned in that machine, leaving Q commercial path uncertain

---

## Section 2: Challenges in Capturing System Function

Ranked by LCOE impact.

**1. No commercial design point exists — model has no anchor (Impact: Critical)**

Energy Singularity has not published a commercial plant design. The HH380 demo power station is a name and a roadmap entry, not an engineering design. The HH170 Q > 10 machine is a physics demonstration device, not a power plant precursor with a stated electrical output. Without a design point — major radius, plasma current, fusion power, net electric, thermal efficiency — an LCOE model has no starting parameters. The closest analog in the literature is SPARC/ARC (CFS), which shares the compact HTS tokamak architecture but has R = 1.85 m (SPARC), 8 T on-axis, and published ARC design parameters (Sorbom et al. 2015). Energy Singularity's HH380 is likely in a different size class. Any LCOE estimate would require wholesale analogue assumptions from CFS's ARC or from the CFETR cost analysis (Chen et al. 2015). These analogues could easily carry ±50% uncertainty on capital cost alone.

**2. Blanket design is entirely undisclosed — no tritium breeding model possible (Impact: Critical)**

The HH380 commercial demo must breed its own tritium, but no blanket concept has been disclosed. China's CFETR program is developing WCCB (water-cooled ceramic breeder), HCCB (helium-cooled ceramic breeder), and sCO₂-cooled LiPb blankets [dossier.md §Tritium Breeding], but no connection between these programs and Energy Singularity's design exists in the public literature. This is not a data gap that will resolve soon: HH70 is experimental with no neutron production at D-T levels; HH170 may not burn D-T; and HH380 engineering decisions (where blanket design becomes critical) are post-2030. The blanket is the single largest cost uncertainty outside of magnets and the item with the highest TRL risk.

**3. Full HTS coil set at 25 T peak field — validated at 21.7 T, commercial operation unproven (Impact: High)**

The Jingtian test magnet achieved 21.7 T (some sources: 22.4 T), establishing a world record. The HH170 targets 25 T peak field [dossier.md §Driver Technology]. The gap from 21.7 T to 25 T is not trivial — REBCO tape Jc falls rapidly above 20 T at 20 K, and the magnet structural design must handle proportionally higher Lorentz forces. Beyond HH170, the HH380 commercial magnets at scale introduce additional manufacturing consistency requirements. The cost of the full TF+PF+CS HTS coil system at commercial scale is unknown; the Jingtian result proves the physics but does not anchor a commercial coil cost.

A further uncertainty: extending HTS to all coil types (PF and CS) is novel. Most competing designs (CFS, Tokamak Energy) use HTS for TF coils and LTS or conventional conductors for PF/CS. Full HTS CS coils must generate and sustain plasma initiation current, a demanding duty cycle that introduces additional quench and fatigue risks. No published fatigue or reliability data exists for full-HTS CS coils in tokamak operation.

**Primary structure and vacuum vessel sizing — undisclosed, and counterintuitively demanding (Impact: Moderate on CAS22)**

No primary structure thickness or vacuum vessel wall thickness has been disclosed for HH70, HH170, or HH380. The intuition that a compact machine requires thinner structure is incorrect for high-field HTS tokamaks: TF coil out-of-plane loads scale approximately as B² × volume, and at 25 T peak field the Lorentz forces on the TF structure are substantially higher than on a conventional 5–6 T LTS machine of similar size. SPARC and ARC (the closest published analogues) adopt primary structure thicknesses of ~0.20 m — the framework default for tokamaks — despite their compact geometry, specifically to handle the higher EM loads. Until Energy Singularity publishes structural engineering data for HH170 or HH380, the tokamak default (0.20 m / 0.20 m for structure / vessel) is the defensible anchor; any downward deviation requires a published load-path argument. The CAS22 capital cost sensitivity to this parameter is bounded: sweeping structure_t and vessel_t over [0.10, 0.20] m changes CAS22 by approximately 5–8% in absolute terms, translating to roughly 1–2% on total plant LCOE given the distribution across all cost accounts — non-negligible but not dominant.

**4. AI-based plasma control — potentially significant for capacity factor but unquantified (Impact: Moderate)**

Energy Singularity's AI-based plasma control system enabled the 1,337-second steady-state plasma [dossier.md §Operation Mode; energy-singularity-overview.md §HH70 Performance]. This is genuinely novel and may confer capacity factor advantages if it reduces disruption frequency and enables tighter operating margins. However, no published reliability or availability data exists for this system. The LCOE leverage of capacity factor is high: moving from 75% to 85% availability improves LCOE ~12% for capital-dominated plants. Without disruption frequency data, the capacity factor cannot be modeled.

**5. ICRH as primary heating — scale and efficiency for power plant uncertain (Impact: Moderate)**

ICRH is confirmed on HH70, but at very low power levels appropriate for an experimental machine. ICRH at the tens-of-MW scale needed for a burning plasma tokamak has different efficiency, reliability, and antenna engineering challenges. No heating configuration has been disclosed for HH170 or HH380. Wall-plug efficiency of ICRH is ~60–70% — comparable to NBI but inferior to ECRH (~50–55%) in some configurations. Without disclosed heating power, recirculating power fraction cannot be estimated.

**Technical bet scenario structure:**

The two critical technical bets for this concept should be modeled as explicit scenario branches, not absorbed into a single base-case availability:

- **CS coil reliability failure scenario**: Full HTS CS coils at 25 T under cyclic EM loading fail to achieve target availability. Model as availability = 65% plus an additional coil-replacement cost factor. LCOE impact vs. base case (80% availability) is approximately +14% on LCOE from the availability drop alone (elasticity ≈ −0.94), before coil replacement costs.
- **AI plasma control underperforms scenario**: AI control system does not reduce disruption frequency at burning-plasma conditions to levels assumed in base case. Model as availability = 70%, representing disruption-limited operation rather than steady-state. LCOE impact vs. base case approximately +9%.

Bracketing these two failure modes against the base case establishes the LCOE range attributable to the concept's novel elements, distinguishing the "novel technology premium" from the "general fusion capital cost" uncertainty.

**Key LCOE sensitivity parameters for this concept:**

Three parameters dominate the LCOE sensitivity for a capital-intensive concept with no commercial design anchor:

1. **Availability / capacity factor** (highest elasticity, ~−0.94): Determined by AI control reliability and full HTS CS coil duty-cycle endurance. Challenge #3 and #4 above are both proximate causes of availability risk. Moving from 80% to 65% availability increases LCOE by ~14%. This is the primary operability bet.
2. **Cost of capital / interest rate** (second lever): Capital-dominated concepts are highly sensitive to financing terms. Without a commercial design anchor or published cost study, financing terms carry additional uncertainty risk premium. This is the primary financial lever and should be the axis for scenario sweeps.
3. **Major radius / plant scale** (structural uncertainty): With HH380 design point undisclosed, major radius (and by extension fusion power and net electric output) is the dominant structural unknown. It determines capital cost scaling, magnet material demand, and recirculating power. Any LCOE model must bracket this parameter with discrete scenario runs — not marginal sensitivity perturbations around a fixed output — because the uncertainty is about the unknown design point itself (is HH380 a ~250 MWe machine at R ≈ 1.5 m or an ~800 MWe machine at R ≈ 2.5 m?). Recommended scenario structure: **Scenario C** (small machine: R ≈ 1.5 m, net electric ~250 MWe, capital scaled accordingly) and **Scenario D** (large machine: R ≈ 2.5 m, net electric ~800 MWe) reported alongside the technical-bet failure scenarios (Scenarios A and B) in a unified LCOE table so the design-point uncertainty band is visible.

**6. Chinese regulatory and supply chain context (Impact: Moderate)**

Energy Singularity operates under Chinese regulatory framework rather than NRC/IAEA Western frameworks. The 2023 NRC decision to regulate fusion under 10 CFR Part 30 does not apply to Chinese projects; Chinese nuclear regulation for fusion power plants is still being formulated. On the supply chain side, the >95% domestic localization rate [energy-singularity-technical-summary.md §Supply Chain] could be a significant cost advantage given China's scale in manufacturing, but it also concentrates supply chain risk geopolitically and creates barriers to international cost benchmarking.

A 2025 policy paper (pii-s2211467x25003839) proposes a "Global Licensing and Regulation Framework to accelerate the development and deployment of fusion energy," including a proposed "Global Organisation for Fusion Energy" and a 7-point framework treating fusion more like particle accelerators than fission reactors. The paper notes that "most recent timelines agree on the second half of the 2030s for the realisation of a Fusion Energy pilot plant" — placing Energy Singularity's HH380 demo station directly in this regulatory transition window. International harmonization efforts are relevant because they may determine whether China-developed fusion technology can access international markets or grid-connection frameworks. However, the available extract does not confirm whether the paper addresses Chinese regulatory specifics; the China regulatory gap (Gap #12) remains open.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest LCOE risk) to most mature.

---

**Tritium Breeding Blanket — TRL 1–2**

- **Demonstrated**: Nothing specific to Energy Singularity's design. China's CFETR program has conducted small-scale tritium breeding experiments under the WCCB and HCCB blanket programs, but no connection between these and Energy Singularity has been documented. Global TBM programs (ITER, CFETR) are in detailed engineering at TRL 3–4, but these are for different machines and designs.
- **On paper only**: No blanket concept has been publicly disclosed for HH170 or HH380. No TBR target has been stated. No tritium extraction approach has been named.
- **Missing at scale**: The entire blanket concept, engineering, and qualification program. This is the largest maturity gap in the concept. Without a disclosed blanket design, this is effectively TRL 1 (concept not stated) for this company's specific approach.

---

**Tritium Fuel Cycle — TRL 2–3**

- **Demonstrated**: Lab-scale tritium handling (JET, TFTR). The standard D-T fuel cycle physics is well-understood globally. Energy Singularity has no documented tritium handling capability — HH70 operates with non-D-T plasmas.
- **On paper only**: Tritium breeding, extraction, and closed-loop fuel cycle for any Energy Singularity machine. D-T plasma operation is the stated goal for HH170, but the "D-T equivalent" framing suggests D-T may not be burned in HH170 either.
- **Missing at scale**: All tritium-handling infrastructure from primary circuit tritium permeation barriers to secondary purification to accountancy systems. The startup tritium inventory (~1 kg at >$35,000/g [handwritten exemplar 01-hts-compact-tokamak.md]) must be acquired before first D-T burn; no evidence that Energy Singularity has begun planning this.

---

**Full HTS Coil Set at 25 T Peak Field (CS and PF Included) — TRL 4–5**

- **Demonstrated**: Jingtian test magnet achieved 21.7 T peak field using 32 stacked REBCO single-pancake coils [energy-singularity-overview.md §Magnet System]. HH70 26-coil full-HTS system (12 TF + 6 PF + 8 CS) operates at 0.6–1 T on-axis / 2.5 T on coil [energy-singularity-overview.md §Machine Parameters]. Shanghai Superconductor supplies REBCO tape. Construction completed in under 2 years with >95% domestic sourcing.
- **On paper only**: Full 25 T D-shaped HTS coil set for HH170. Full HTS CS coil performing plasma initiation current ramp at plant-relevant fields and current densities. Quench protection system for a 26+-coil full-HTS system in a neutron environment. REBCO tape performance at 25 T / 20 K at the mechanical loads of a compact high-field coil.
- **Missing at scale**: Long-term (multi-year) reliability of REBCO HTS CS coils under combined cyclic EM loading + neutron + gamma irradiation. Demonstrated quench detection and energy extraction for a full TF+PF+CS HTS system. Insulation systems for CS coils that survive plasma initiation transients and radiation damage. Supply chain for REBCO tape at commercial plant scale (thousands of km per plant).

> "Jingtian magnet reached 21.7 T peak field (later sources report 22.4 T), surpassing the CFS/MIT 20 T record"
> — dossier.md §Magnet Type

---

**Steady-State Plasma Control (AI System) — TRL 5–6**

- **Demonstrated**: 1,337-second steady-state plasma in HH70 (February 2026, shot #5,755) [energy-singularity-overview.md §HH70 Performance; energy-singularity-technical-summary.md §Opening paragraph]. AI-based plasma control system credited with enabling long-pulse operation. Multiple pulse durations documented: 120 s, 335 s, 1,337 s over the campaign.
- **On paper only**: AI control system performance at burning-plasma conditions (high neutron flux, high radiation, high plasma power) where feedback latencies and sensor degradation create a fundamentally different control environment than HH70. Control system performance under D-T plasma instabilities and disruption precursors.
- **Missing at scale**: Disruption frequency and disruption mitigation capability in a burning plasma. Validated availability contribution from AI control at commercial duty cycle. Control system redundancy and radiation hardening for HH380-scale operation.

---

**ICRH Heating System — TRL 6–7**

- **Demonstrated**: ICRH confirmed operational on HH70 [dossier.md §Primary Heating]. ICRH at tens-of-MW scale is mature technology globally — JET, ITER, and multiple large tokamaks routinely operate MW-class ICRH systems.
- **On paper only**: ICRH configuration (power, frequency, antenna geometry) for HH170 and HH380 is not disclosed. Heating power allocation for a Q > 10 machine requires specification of plasma temperature and confinement targets, neither of which is published for the commercial design.
- **Missing at scale**: ICRH antenna survival under D-T neutron bombardment at HH380 first-wall flux levels. Continuous-wave ICRH operation at the tens-to-hundreds of MW level needed for a burning plasma commercial machine.

---

**Compact Tokamak Vacuum Vessel and Plasma-Facing Components — TRL 6–7**

- **Demonstrated**: HH70 vacuum vessel built and operating. Compact tokamak vacuum vessel design and construction is proven technology (multiple existing machines globally). Energy Singularity's under-2-year build time from design to plasma is notable [energy-singularity-overview.md §Construction].
- **On paper only**: HH380-scale vacuum vessel with integrated neutron shielding, blanket attachment, remote maintenance access, and D-T compatibility. Divertor design for the target plasma parameters.
- **Missing at scale**: First wall and divertor for sustained D-T operation at HH380 plasma power. Remote maintenance scheme — not disclosed. Tungsten divertor replacement schedule and cost at commercial availability.

---

**Balance of Plant / Power Conversion — TRL 7–9 (generic) / TRL 1–2 (concept-specific)**

- **Demonstrated**: Conventional steam Rankine and sCO₂ Brayton cycles at GW scale are commercially mature. No energy conversion hardware is relevant to HH70 (no net power production).
- **On paper only**: Power conversion cycle for HH380 is not named. The strategic goal of LCOE at or below thermal power costs implies a high efficiency target, but no cycle type, efficiency target, or heat rejection design has been disclosed.
- **Missing at scale**: Coupling of fusion heat source to power conversion in a D-T environment. Tritium-compatible primary coolant heat exchangers. BOP design for the specific heat source temperature and capacity of HH380.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck, Partially Domestic**

Global REBCO production capacity is estimated at a few thousand km/year across all manufacturers. A single compact HTS tokamak plant requires on the order of thousands to tens of thousands of km of tape depending on design field and coil geometry. Energy Singularity uses Shanghai Superconductor Technology as its primary supplier [energy-singularity-overview.md §Magnet System], giving it access to one of the world's leading REBCO producers and a domestic supply chain that bypasses geopolitical risk for China-based deployment. However, Shanghai Superconductor's current capacity is still below what fleet-scale deployment would require, and tape cost at the current ~$30–100/kA-m range needs to fall toward ~$10/kA-m or lower for commercial competitiveness [handwritten exemplar 01-hts-compact-tokamak.md].

The full HTS coil set (TF + PF + CS) likely requires more tape per plant than a TF-only HTS design, since PF and CS coils add significant conductor volume. This is a cost penalty unique to the full-HTS approach relative to partial-HTS competitors. On the other hand, operating all coils at HTS temperatures potentially reduces cryogenic complexity by eliminating the need to maintain separate LTS coils at lower temperatures.

Energy Singularity's >95% domestic localization rate for HH70 and HH170 [energy-singularity-technical-summary.md §Supply Chain] positions it well for China-domestic deployment but creates an opaque cost basis for international comparison.

**Tritium — Declining External Supply (Shared D-T Constraint)**

The global tritium inventory is approximately 25–30 kg, produced primarily as a CANDU heavy-water reactor byproduct, decaying at 5.5%/year [handwritten exemplar 01-hts-compact-tokamak.md]. A D-T reactor startup requires ~1 kg at >$35,000/g. The HH380 commercial demo must breed its own tritium from first D-T ignition or rely on CANDU-derived inventory. China's indigenous tritium production capability (via CANDU-type heavy water reactors or otherwise) is not publicly documented in this context. The blanket design choice (which determines TBR, tritium inventory, and extraction method) is not disclosed, making tritium fuel cycle cost unquantifiable.

**China's REBCO and Domestic Manufacturing Context**

Shanghai Superconductor is one of China's leading HTS tape producers, part of a broader domestic HTS manufacturing ecosystem that includes State Grid Corporation-linked companies. China's national fusion program (CFETR, EAST, J-TEXT) creates substantial institutional demand for HTS tape and associated cryogenic infrastructure, providing potential scale advantages for Energy Singularity's domestic supply chain. This may give Energy Singularity a structural cost advantage for China-domestic deployment that does not translate to international commercial comparisons. The >96% localization rate for HH70 suggests this supply chain is functional at prototype scale; whether it can scale to commercial volume without significant cost increase is unknown.

**Blanket and Coolant Materials — Entirely Undetermined**

Since no blanket design has been disclosed, the critical material choices for the primary breeding zone — FLiBe, solid lithium ceramic, Pb-17Li, or pure Li metal — are unknown. Each carries distinct supply chain implications: FLiBe requires beryllium (limited to ~300 tonnes/year globally, one primary producer); Pb-17Li has extensive ITER TBM heritage; solid ceramic pebbles require qualified manufacturing. Without a blanket material, no supply chain assessment for the breeding zone is possible.

**Tungsten (First Wall and Divertor) — Adequate Supply**

Tungsten for plasma-facing components is available in adequate global supply with the manufacturing challenges (thermal fatigue resistance, precision shaping, remote replacement) shared across all D-T tokamak designs. Not a binding supply constraint. China has significant tungsten reserves (~80% of global known deposits), giving Energy Singularity structural supply security for this material.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| HH70 on-axis toroidal field | 0.6 T (upgraded to >1 T) | energy-singularity-overview.md §Machine Parameters | high | Prototype only; not commercial machine |
| HH70 peak field on coils | 2.5 T | energy-singularity-overview.md §Machine Parameters | high | Post-cryogenic upgrade value |
| HH70 major radius | 0.7 m | sciencedirect-science-article-pii-s092037962500537x.md §Abstract | high | Prototype; peer-reviewed commissioning paper supersedes dossier estimate of 0.75 m |
| HH70 minor radius | 0.25–0.30 m | sciencedirect-science-article-pii-s092037962500537x.md §Abstract | high | Confirmed in commissioning paper abstract (a = 0.25–0.3 m) |
| HH70 steady-state duration (record) | 1,337 seconds | energy-singularity-overview.md §HH70 Performance; energy-singularity-technical-summary.md §Opening | high | Shot #5,755, February 2026 |
| HH70 total shots completed | 5,755 | energy-singularity-technical-summary.md §Opening | high | As of February 2026 announcement |
| Jingtian peak field | 21.7 T (some sources: 22.4 T) | dossier.md §Magnet Type | high | Test magnet; 32-layer stacked REBCO; superceded CFS/MIT record |
| HH170 target Q | > 10 (D-T equivalent) | dossier.md §Plasma State; energy-singularity-overview.md §HH170 | medium | "D-T equivalent" framing may not require actual D-T burn |
| HH170 on-axis field | ~14 T | dossier.md §Confinement Concept | medium | ~110% of SPARC |
| HH170 peak coil field (target) | 25 T | dossier.md §Driver Technology | medium | D-shaped HTS magnets; not yet achieved |
| HH170 volume vs. SPARC | ~70% SPARC volume | dossier.md §Confinement Concept | medium | Approximately 0.9× SPARC diameter |
| HH170 expected completion | ~2027 | dossier.md §Summary | medium | Company roadmap target |
| HH380 status | Post-2030 demo station | dossier.md §Summary | high | No design parameters disclosed |
| Domestic component localization | >95% (HH70/HH170) | energy-singularity-overview.md §Construction | high | China-domestic supply chain |
| Build time (HH70) | < 2 years | energy-singularity-overview.md §Construction | high | First plasma to record milestone |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | Long-pulse confirmed on HH70 |
| Fuel | D-T (target) | dossier.md §Fuel | high | HH70 is pre-D-T |
| Primary heating (HH70) | ICRH (ICRF) | dossier.md §Primary Heating | high | Electron gun for pre-ionization |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net electrical output (HH380) | proprietary | blocking | No commercial machine design exists |
| Fusion power (HH380) | proprietary | blocking | Required to anchor LCOE model |
| Q value (commercial machine) | proprietary | blocking | HH170 Q > 10 is for physics machine, not power plant |
| Thermal conversion efficiency | proprietary | blocking | Cycle type not disclosed |
| Capital cost estimate | proprietary | blocking | No plant study exists |
| Blanket TBR target | proprietary | blocking | No blanket design disclosed |
| Blanket material / design type | truly-unknown | blocking | Structurally unresolvable pre-HH380 engineering |
| Tritium breeding approach | truly-unknown | blocking | Not disclosed; linked to blanket choice |
| Heating power (HH170/HH380) | proprietary | important | Required for recirculating power fraction |
| Capacity factor target | proprietary | important | AI control system may improve; unquantified |
| Magnet cost per coil set | proprietary | important | REBCO tape volume and coil design not published |
| REBCO tape demand per plant | derivable | important | Can estimate from field/coil geometry if design published |
| HTS full-coil cost premium vs. TF-only HTS (`hts_full_coil_premium`) | derivable | important | Ratio of CS+PF+TF tape demand to TF-only demand at same field; placeholder ×1.1–×1.3; drives C220103 in model |
| Major radius (HH380) | truly-unknown | important | No commercial design point |
| Wall-loading / neutron flux | truly-unknown | important | Depends on undisclosed fusion power |
| First wall / divertor lifetime | truly-unknown | important | Depends on undisclosed wall loading |
| Primary structure thickness (structure_t) | truly-unknown | important | No ES disclosure; SPARC/ARC analogue → ~0.20 m (framework tokamak default); compact-geometry downward deviation requires load-path argument not yet available |
| Vacuum vessel wall thickness (vessel_t) | truly-unknown | important | No ES disclosure; SPARC/ARC analogue → ~0.20 m (framework tokamak default); impacts CAS22 via per-m³ vessel cost coefficient (~$0.72M/m³) |
| O&M cost breakdown | truly-unknown | nice-to-have | No plant study available; placeholder needed |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Net electrical output and fusion power for commercial machine (HH380) | S1, S5 | proprietary | blocking | Await HH380 engineering phase publications (post-2030) or CFS ARC as proxy |
| 2 | Q value and plasma parameters for commercial design point | S2, S5 | proprietary | blocking | HH170 physics papers (if published post-2027); SPARC analogy as proxy |
| 3 | Blanket design, material, and TBR target | S1, S2, S3, S5 | truly-unknown | blocking | Structurally unresolvable until HH380 engineering; CFETR blanket programs as possible proxy |
| 4 | Tritium fuel cycle design and T inventory | S3, S4, S5 | truly-unknown | blocking | Linked to gap #3; ITER/CFETR tritium cycle as functional analogue |
| 5 | Power conversion cycle type and thermal efficiency | S2, S5 | proprietary | blocking | Await HH380 engineering; sCO₂ Brayton or steam Rankine as proxy depending on coolant |
| 6 | Capital cost estimate or plant cost study | S5 | truly-unknown | blocking | No source exists; CFETR cost study (Chen et al. 2015) or ARC TEA (Araiinejad & Shirvan 2025) as analogue |
| 7 | Heating system power and configuration for HH170 / HH380 | S2, S5 | proprietary | important | HH170 technical papers if released 2027+ |
| 8 | Full HTS CS coil fatigue and reliability data | S3 | truly-unknown | important | Research gap globally — no published fatigue data for HTS CS in tokamak operation |
| 9 | REBCO tape demand per plant (full HTS design) | S4, S5 | derivable | important | Requires design point (gap #2); derivable once coil geometry known |
| 10 | Capacity factor target and disruption rate with AI control | S2, S5 | proprietary | important | HH70/HH170 operational statistics if published |
| 11 | O&M cost structure (fixed vs. variable, maintenance schedule) | S5 | truly-unknown | important | No plant study; ARC TEA or CFETR as analogue for D-T tokamak O&M |
| 12 | Regulatory framework for fusion power in China and international harmonization | S2 | partially-sourced | important | International framework paper (pii-s2211467x25003839) addresses global proposals but not China-specific rules; Chinese regulatory agency publications needed for domestic framework details |
| 13 | HH70 commissioning paper (ScienceDirect, paywalled) | S1 | not-yet-sourced | nice-to-have | Fusion Engineering and Design 2025; likely covers HH70 coil construction, not commercial design |

---

## Section 7: Cross-Concept Notes

### Differentiators vs. Conventional Large-Aspect-Ratio Tokamak (ITER-like Baseline)

| Differentiator | vs. Conventional Tokamak | Cost Implication | CAS Accounts Affected | Direction |
|----------------|--------------------------|-----------------|----------------------|-----------|
| Full HTS coil set (TF + PF + CS in REBCO) vs. **TF-only HTS competitors** (CFS, Tokamak Energy) | CFS/SPARC and Tokamak Energy Demo4 use HTS for TF coils only; CS and PF use LTS or copper; Energy Singularity extends HTS to all coil types | **Penalty**: higher REBCO tape demand for CS+PF vs. TF-only HTS (tape cost premium); novel CS duty-cycle risk adds CS coil reconditioning / replacement cost in reliability failure scenarios; **Benefit**: uniform 20 K cryoplant potentially simplifies thermal management | **Primary**: C220103 (magnet system — incremental REBCO tape volume for CS+PF); **Secondary**: CAS70 O&M (CS coil reconditioning / replacement events in CS reliability failure scenario) | Net cost penalty vs. TF-only-HTS competitors; magnitude unquantified |
| Compact high-field geometry (~14 T on-axis, ~70% SPARC volume) vs. ITER (5.3 T, R = 6.2 m) | Compact design reduces structural material and building volume for a given Q; higher field enables higher pressure at smaller radius | **Advantage**: smaller machine → lower structural material cost, shorter build time, smaller site; potentially lower absolute capital cost at same Q | C210 (site and structures), C220 (magnets) | Advantage (capital cost) |
| AI-based plasma control enabling long-pulse/steady-state operation | Conventional tokamaks rely on feedback control but not AI-native architectures; steady-state operation requires active current drive | **Advantage** (if it works): higher capacity factor, fewer disruptions → better LCOE; **Risk**: unvalidated at burning plasma conditions | CAS70 O&M (fewer disruption repairs); LCOE via capacity factor | Potential advantage; high uncertainty |
| China-domestic supply chain (>95% domestic localization) | Western designs rely on international supply chains for key components | **Advantage for China-domestic deployment**: lower logistics cost, no export control friction; **Barrier for international comparison**: opaque cost basis | Distributed across all CAS accounts — affects unit prices, not account structure | Geography-dependent |

The most TEA-relevant differentiator is the **full HTS coil scope (TF + PF + CS)** relative to **TF-only HTS competitors (CFS, Tokamak Energy)**— not vs. the LTS baseline, since those are the live commercial competitors operating in the same compact high-field regime. The relevant cost penalty falls primarily in **C220103** (HTS magnet system account): the incremental REBCO tape demand for CS and PF coils beyond the TF-only baseline. A secondary cost impact appears in **CAS70 O&M** under the CS coil reliability failure scenario: if CS coils at 25 T under cyclic EM loading require mid-life reconditioning or replacement, those costs accrue to scheduled and unscheduled O&M rather than capital. The potential benefit (simplified cryoplant with uniform 20 K operating temperature across all coils, eliminating mixed LTS/HTS cryogenic circuits) is real but unquantified in any published source. The model should apply a `hts_full_coil_premium` multiplier to C220103 to represent this incremental tape and fabrication cost; the range ×1.1–×1.3 relative to a TF-only baseline is a placeholder pending an Engineering estimate of CS+PF tape volume.

---

**Prior approved analysis consulted**: [21-spherical-tokamak-hts] (Tokamak Energy ST-E1)

The 21-spherical-tokamak-hts analysis covers Tokamak Energy's ST-E1, which shares the HTS magnet technology and D-T fuel cycle with Energy Singularity's concept. Several supply chain and materials observations from that analysis apply here with minor modification:

**Shared with 21-spherical-tokamak-hts:**
- REBCO superconducting tape supply chain bottleneck: both concepts require thousands of km of HTS tape per plant; current global production capacity is below fleet-scale demand; tape cost must fall from ~$30–100/kA-m to ~$10/kA-m for commercial viability. The REBCO supply assessment from that analysis applies directly [21-spherical-tokamak-hts §Section 4].
- D-T tritium fuel supply constraint: global inventory ~25–30 kg, CANDU production declining, startup requirement ~1 kg at >$35,000/g. This constraint applies identically to any D-T tokamak [21-spherical-tokamak-hts §Section 4].
- Tritium fuel cycle TRL (3–4) and breeding blanket TRL (2–3) as baseline for a D-T tokamak at this stage — Energy Singularity is arguably even earlier (TRL 1–2 for blanket, since no concept has been disclosed).
- Regulatory uncertainty for tokamak power plants (though the Chinese regulatory context differs from the NRC/IAEA context analyzed in 21).

**Key divergences from 21-spherical-tokamak-hts:**

- **Geometry**: Energy Singularity uses a D-shaped (conventional aspect ratio, ~A ≈ 3–4 estimated for HH380) tokamak, not a spherical tokamak (A = 2.3). The center stack geometry, blanket access, and neutron shielding challenges of the spherical tokamak geometry do not apply here. The inboard blanket can potentially be included for a standard aspect ratio machine, allowing 4π (full-coverage) breeding rather than the outboard-only constraint of the ST.
- **Magnet system scope**: Energy Singularity uses HTS for all coils (TF + PF + CS). Tokamak Energy Demo4 validated TF + PF only at 11.8 T; CS coil technology at 25 T in full HTS is a gap with no equivalent in the 21 analysis.
- **Field level**: HH170 targets 25 T peak / ~14 T on-axis — higher than ST-E1 (11.8 T at coil / 5.25 T on-axis). This is closer to the CFS SPARC/ARC regime and implies higher REBCO tape performance requirements at lower temperatures.
- **Domestic supply chain**: Energy Singularity's >95% China-domestic localization (Shanghai Superconductor as primary tape supplier) has no parallel in the Tokamak Energy analysis. This may lower costs for China-domestic deployment but creates a different risk profile.
- **Data availability**: ST-E1 has four published machine parameters and a peer-reviewed ECRH study. Energy Singularity HH380 has no published machine parameters at all. The 21 analysis was rated "Limited"; this analysis is also "Limited" but with substantially less parameter coverage.

**Relationship to 01-hts-compact-tokamak (CFS/SPARC) — not an approved prior, noted for context:**
The most technically relevant analogue for Energy Singularity is not ST-E1 but the CFS SPARC/ARC program: both are compact, high-field, D-shaped HTS tokamaks targeting Q > 10 with subsequent power plant design. The ARC concept (Sorbom et al. 2015), SPARC parameters, and Araiinejad & Shirvan (2025) TEA are the best available proxies for an HH380 LCOE model. Energy Singularity appears to target a similar or slightly higher magnetic field than SPARC, in a similar or slightly smaller machine volume. Key differences from CFS: full HTS (vs. TF-only HTS); Chinese domestic supply chain; AI-based plasma control; less published physics basis.

---

## Section 8: Sources

**Primary sources for this analysis:**

1. **energy-singularity-overview.md** (iter-01/sources/)
   - Synthesized overview of Energy Singularity, HH70, HH170, Jingtian magnet
   - Contains HH70 machine parameters, coil specifications, steady-state records, HH170 targets, funding data
   - Primary factual foundation for Sections 1, 3, 5

2. **energy-singularity-technical-summary.md** (iter-02/sources/)
   - News announcement on the 1,337-second plasma milestone
   - Contains co-founder strategic statement on LCOE target, domestic localization rate
   - Brief (2 KB) — contributes the strategic framing and localization data

3. **Phase 1a dossier** (knowledge/concept_research/28-hts-tokamak-full-hts/dossier.md)
   - Structured research summary across three iterations and 20+ sources
   - High-confidence values: confinement family, fuel, magnet type, operation mode; medium-confidence: heating, energy capture, plasma state; unresolved: tritium breeding, neutron management
   - Foundation for all differentiation table values and gap characterization

**Key external sources supporting analogue reasoning:**

4. **Sorbom, B.N. et al. (2015)**: "ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets," *Fusion Engineering and Design*, 100, 378–405.
   - Best published analogue for commercial design parameters (compact high-field HTS tokamak)
   - Not ingested as a source document — referenced via handwritten exemplar 01-hts-compact-tokamak.md

5. **Araiinejad, L.S. and Shirvan, K. (2025)**: "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567.
   - Best available TEA framework for D-T tokamaks including regulatory cost factors
   - Cited in handwritten exemplar 01-hts-compact-tokamak.md; applicable as proxy for HH380 LCOE model

6. **Chen, H. et al. (2015)**: "Preliminary cost assessment and comparison of China Fusion Engineering Test Reactor," *Journal of Fusion Energy*, 34(1), 1–10.
   - Only published cost study for a Chinese D-T tokamak concept (CFETR)
   - Potentially more relevant to Energy Singularity's actual cost environment than Western studies
   - Referenced in handwritten exemplar 01-hts-compact-tokamak.md

7. **21-spherical-tokamak-hts approved analysis** (exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md)
   - HTS supply chain assessment and D-T tritium supply characterization reused for Sections 4 and 7

**Paywalled sources not incorporated:**

8. **ScienceDirect (2025)**: "Design, commissioning, and first operation of HH70" — *Fusion Engineering and Design*
   - Covers HH70 experimental machine; unlikely to contain commercial design parameters
   - Not incorporated due to paywall and low expected yield for LCOE modeling

9. **Fusion Energy (2025)**: "Global Licensing and Regulation Framework to accelerate the development and deployment of fusion energy" — *Energy* journal (pii-s2211467x25003839)
   - Policy and governance paper proposing a 7-point international regulatory framework for fusion, including a proposed "Global Organisation for Fusion Energy"
   - Relevant to Section 2 Challenge #6: paper cites second-half-2030s as consensus timeline for fusion pilot plants; advocates regulatory treatment of fusion like particle accelerators rather than nuclear fission
   - Abstract extracted; full article behind paywall — China-specific regulatory content not confirmed in available extract
   - Not a magnet construction paper (previously misidentified in this source list)

---

*Footnotes:*

[1] energy-singularity-overview.md §HH70 Performance: "steady-state durations achieved: 120 seconds (January 2026), 335 seconds (January 2026), 1,337 seconds (February 2026)"

[2] energy-singularity-overview.md §HH170 — Next-Generation Device: "world's smallest and lowest-cost tokamak device capable of achieving 10-fold energy gain"

[3] energy-singularity-technical-summary.md §Dong Ge Quote: "the deep integration of HTS and AI control technologies has reached engineering feasibility, paving the way for the low-cost, high-efficiency construction of future fusion power plants"

[4] dossier.md §Tritium Breeding: "Confirmed across 3 iterations and 20+ sources. Structurally unresolvable at current company stage"

[5] energy-singularity-overview.md §Magnet System: conductor is "Two 12mm-wide HTS tapes with 10mm REBCO core sandwiched between copper tapes"; supplier is Shanghai Superconductor
