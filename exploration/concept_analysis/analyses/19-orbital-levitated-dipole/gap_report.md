# Gap Assessment: Orbital Levitated Dipole (D-He3)

## Overall Readiness
**Rating**: Insufficient Data
**Summary**: Zephyr Fusion (YC F25, founded 2025, 2 employees, pre-prototype) has disclosed no plasma performance targets, no energy conversion mechanism, and no reactor design in any public source. The concept's most fundamental parameters — Q value, net power output, heating method, and the fusion-to-beamable-power conversion chain — remain either proprietary or technically undefined. Additionally, the D-He3 fuel cycle requires He-3 at scales orders of magnitude beyond current global production, and no credible supply pathway exists at fusion scale. A qualitative narrative can be structured around dipole physics heritage and the orbital architecture concept; a quantitative LCOE model cannot be responsibly constructed.

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- YC launch page (`iter-01/sources/yc-launch-page.md`): physics basis (τₑ ~ R² scaling, dipole magnetosphere analogy), market positioning (orbital industrial power), hardware approach (meter-scale REBCO coil, Falcon 9 deployable), founder credentials (ORNL, LLNL, W7-X, DIII-D), claimed cost comparisons (ISS solar at ~$1B/MW, ITER at ~$650M/MW)
- Community technical critique (`iter-01/sources/nasaspaceflight-forum-discussion.md`): identifies key gaps — no blanket, no heat output, no power conversion, no tritium breeding
- Levitated dipole heritage (`iter-01/sources/levitated-dipole-technical-background.md`): LDX (MIT, Nature Physics 2010), RT-1 (U. Tokyo), OpenStar 2024 helium ionization demonstration, terrestrial dipole landscape
- OpenStar D-T dipole reactor paper (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`, arxiv 2602.20564): detailed D-T terrestrial levitated dipole engineering study — REBCO coil design, heating options with efficiency figures (ECRH 30-40%, ICRH 70%, NBI), neutron shielding, plant power balance equations, assumed thermal efficiency 40%, cryogenic efficiency 1.25%; D-T reactor designs at 667 MW fusion / 208 MW net electric
- He-3 supply chain (`iter-02/sources/everycrsreport-reports-r41419.md`): CRS congressional report on He-3 shortage — historical prices ($40-85/liter from DOE auctions), production sources (primarily weapons tritium decay at ~15,000 liters/year peak), alternative sources (CANDU byproduct, particle accelerators, atmospheric extraction), quantified shortage context at neutron-detection scale
- Power beaming context (`iter-02/sources/arxiv-2401-15267.md`): Caltech/MAPLE WPT experiment demonstrating flexible coherent WPT array in LEO for 8 months; RF pointing to ground confirmed (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`): WPT microwave theory and SPS transmission efficiency framework
- Web survey (`iter-02/sources/zephyr-fusion-web-sources-2026.md`): confirms no additional technical content beyond YC page across FusionXInvest, Fondo, DCD, LinkedIn sources

**Missing**:
- Any Zephyr-authored technical document (paper, patent, conference presentation)
- D-He3 orbital dipole design study — no peer-reviewed reactor study for this specific configuration exists
- Teller et al. 1992 "Space Propulsion by Fusion in a Magnetic Dipole" — original orbital dipole proposal (referenced in YC page but not extracted)
- Hasegawa & Chen 1987 PPPL-2627 — original D-He3 dipole proposal (referenced throughout but not extracted)
- ARIES-III study — D-He3 advanced fuel tokamak with direct energy conversion analysis

**Gaps**:
- No company technical disclosures — proprietary — **blocking**
- No D-He3 orbital dipole design study — truly-unknown — **blocking**
- Teller 1992 and Hasegawa 1987 original papers not extracted — not-yet-sourced — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Poor

**Available**:
- Dipole confinement physics (LDX/RT-1 heritage): turbulent inward pinch confirmed, peaked pressure profiles, natural stability to interchange modes; τₑ ~ R² scaling motivates large plasma volumes
- D-T dipole engineering analysis (`dipole-reactor-heating-energy-conversion.md`): equilibrium physics (Grad-Shafranov, Eq. 1-6), β limits, plasma edge conditions, energy confinement time framework, power balance model (Equations 9-20 in OpenStar paper); identifies that transport in the "good curvature" region approaching inner first closed flux surface is a key open physics question
- Heating options with efficiency data: ECRH (30-40% wall-plug, high cutoff density, high-field-side launch), ICRH (70% efficiency, complex antenna geometry, ongoing investigation), NBI (mature, geometrically compatible with dipoles)
- Power beaming infrastructure: microwave WPT demonstrated in LEO at small scale; transmission efficiency theory well-developed for SPS concepts

**Missing**:
- D-He3 fusion performance in dipole geometry: D-He3 requires ~60 keV ion temperature vs. ~15 keV for D-T; triple product requirement is ~100× harder; no published analysis asks whether an orbital dipole can reach D-He3 burning conditions
- Energy conversion chain: the full pathway from fusion-product charged particles (85% of D-He3 energy) through direct conversion at the separatrix, to DC power, to RF beam — undesigned and unanalyzed
- Orbital plasma environment effects: LEO atomic oxygen erosion, charged particle belt radiation effects on plasma, microgravity effects on plasma fueling and particle injection
- Fueling system design: D and He-3 injection on orbital platform not addressed

**Gaps**:
- Energy conversion pathway (fusion → beamable power) — proprietary/truly-unknown — **blocking**
- D-He3 burning conditions in dipole geometry not modeled or published — not-yet-sourced — **blocking**
- Orbital plasma environment effects on confinement — truly-unknown — important
- On-orbit fueling system design — proprietary/not-yet-sourced — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **REBCO HTS coil (terrestrial)**: TRL 6-7. OpenStar Junior device validated 14-coil REBCO assembly with levitation and internal low-field shielding region (`dipole-reactor-heating-energy-conversion.md`). Commercial tape available from multiple vendors. Faraday Factory "Mirai" tape at >1000 A/mm² engineering current density.
- **Orbital HTS deployment**: TRL 2-3. No superconducting magnet system has operated in LEO. The OpenStar paper's cryogenic slush strategy (neon slush, 5-minute docking intervals) is designed for terrestrial operation; an orbital equivalent is undesigned.
- **ECRH heating (terrestrial)**: TRL 6-7. Demonstrated on LDX, RT-1, and W7-X. Orbital adaptation TRL 2-3 (no space plasma heating system built).
- **ICRH (terrestrial)**: TRL 4-5 for dipole geometry (demonstrated on RT-1 with "mixed results" per OpenStar paper). Ongoing at OpenStar. Orbital adaptation TRL 2.
- **Power beaming (microwave WPT)**: TRL 4-5. Caltech/MAPLE LEO WPT experiment demonstrated 8-month operation of flexible coherent arrays, RF beam pointing confirmed to ground stations (`arxiv-2401-15267.md`). Efficiency at SPS scale (>85% rectenna) is theoretical.
- **Direct energy conversion**: TRL 2-3. Concept studied for D-He3 tokamak in ARIES-III (not extracted), no experimental demonstration.
- **SpaceX Falcon 9 launch**: TRL 9. Rideshare economics available.

**Missing**:
- TRL for space-rated HTS cryogenic system (the orbital equivalent of neon slush docking strategy)
- TRL for D-He3 direct conversion at dipole separatrix
- TRL for He-3 fuel handling in orbit (pressurized gas management, radiation shielding of inventory)
- System-level TRL integration for the complete orbital fusion platform

**Gaps**:
- Space-hardened HTS cryogenic system: core engineering bet with no existing design — not-yet-sourced — **blocking**
- Direct energy conversion TRL and engineering maturity — not-yet-sourced (ARIES-III not extracted) — important
- He-3 on-orbit fuel handling: no published design — truly-unknown — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial (He-3 supply well-covered by CRS report; system-level supply chain poor)

**Available**:
- **REBCO HTS tape**: Mature commercial supply chain (SuperOx, Fujikura, AMSC, Faraday Factory). Cost declining with demand growth from MRI and fusion programs. No supply chain bottleneck identified for this concept.
- **He-3 fuel supply** (`everycrsreport-reports-r41419.md`): comprehensive CRS data —
  - Historical auction price: $40-85/liter (U.S. DOE; pre-shortage)
  - Primary production: tritium decay from nuclear weapons stockpile (~15,000 liters/year at peak U.S. production)
  - By 2009, neutron-detection demand (thousands of liters/year) alone exceeded supply; federal rationing implemented
  - Alternative sources: CANDU heavy-water reactor byproduct (small quantities), particle accelerator production (expensive), natural gas/atmosphere extraction (trace only), lunar regolith (long-term, speculative)
  - No fusion-scale He-3 demand has ever been analyzed or planned for in any source reviewed
- **Launch vehicle**: SpaceX Falcon 9 rideshare economics available; Falcon 9 fairing constrains coil geometry (YC launch page)

**Missing**:
- He-3 demand estimate for a MW-scale D-He3 fusion device: no calculation in any source; first-principles estimate suggests MW-class D-He3 fusion would consume more He-3 annually than the entire current global He-3 production
- Current He-3 market pricing (post-2010): the CRS report is from 2010; prices rose dramatically after the shortage and current market is opaque
- Radiation-hardened electronics supply chain for orbital plasma systems
- Space-rated cryogenic system supply chain

**Gaps**:
- He-3 supply at fusion scale: no viable production pathway exists — truly-unknown — **blocking**. Global production (~15,000 liters/year) is estimated to be orders of magnitude below what a MW-class D-He3 device would consume.
- He-3 post-2010 market pricing: not captured — not-yet-sourced — important
- Radiation-hardened cryogenic and plasma-system electronics: supply chain unassessed — not-yet-sourced — important

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Note on metric applicability**: The orbital concept does not target terrestrial $/MWh LCOE. The value proposition is orbital power at $/kW to space customers. Standard CAS-based LCOE methodology partially applies (capital cost, O&M, utilization/capacity factor) but the power market is fundamentally different from grid electricity.

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Target power class | MW-scale (unspecified) | YC launch page | l |
| HTS coil technology | REBCO, up to 23 T peak (D-T analog) | OpenStar D-T dipole paper, §2.2.1 | l (analog) |
| Thermal efficiency (D-T analog) | 40% | OpenStar D-T dipole, Table 2 | l (analog) |
| ICRH auxiliary heating efficiency | 70% | OpenStar D-T dipole, Table 2 | l (analog) |
| Cryogenic system efficiency | 1.25% | OpenStar D-T dipole, Table 2 | l (analog only) |
| He-3 historical fuel price | $40–85/liter | CRS He-3 report, p.2 | l (outdated, pre-shortage) |
| Terrestrial modular fusion LCOE analog | $34–54/MWh (~$43/MWh average) | ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | l (analog only) |
| ISS solar power cost reference | ~$1B/MW | YC launch page | m |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion gain Q | proprietary | blocking | No target disclosed; D-He3 requires far higher confinement than D-T; Q<1 likely initially |
| Net power output | proprietary | blocking | MW-class claimed but no specific target; required for all normalization |
| Capital cost by subsystem (CAS) | truly-unknown | blocking | No plant study; orbital concept lacks standard CAS structure (no blanket, no steam cycle, no power block) |
| Energy conversion efficiency | truly-unknown | blocking | Fusion → direct conversion → RF beam → rectenna chain undefined; end-to-end efficiency unknown |
| Capacity factor / availability | truly-unknown | blocking | No plant design basis; orbital ops subject to debris avoidance, orbit decay, docking cycles |
| O&M cost model | truly-unknown | blocking | On-orbit maintenance has no cost analog; resupply logistics undefined |
| He-3 fuel cycle cost | truly-unknown | blocking | No fusion-scale He-3 supply exists; cost would be indeterminate |
| Launch cost contribution | not-yet-sourced | important | Falcon 9 rideshare pricing exists but coil mass unspecified; not integrated |
| Power beaming infrastructure cost | not-yet-sourced | important | Rectenna ground infrastructure, orbital relay costs not addressed |
| Plant lifetime in LEO | truly-unknown | important | REBCO lifetime under LEO radiation environment uncharacterized |

---

## Source Recommendations

**Sources to acquire for qualitative analysis improvement**:
- **Teller et al. 1992** "Space Propulsion by Fusion in a Magnetic Dipole," Fusion Technology: original orbital dipole proposal, physics case for D-He3 burning at large magnetospheric scale. Search OSTI/Fusion Technology journal archives. `not-yet-sourced`
- **Hasegawa & Chen 1987** PPPL-2627: original D-He3 dipole design with direct conversion. Available via INIS or PPPL technical reports. `not-yet-sourced`
- **ARIES-III study** (Najmabadi et al.): D-He3 advanced fuel tokamak with direct conversion of charged particles and synchrotron radiation rectennas — closest analog for energy conversion efficiency data. Search ARIES project publications via OSTI. `not-yet-sourced`
- **Kesner et al. 2003** "Helium catalysed D-D fusion in a levitated dipole": D-D/He-3 fuel cycle analysis for dipole geometry (cited in OpenStar D-T paper). Journal of Plasma Physics. `not-yet-sourced`
- **LDX experimental papers** (Boxer et al. 2010, Nature Physics; Garnier et al. 2006): quantitative achieved plasma parameters (n, T, β, τₑ) from the only levitated dipole demonstrating turbulent inward pinch. `not-yet-sourced`
- **He-3 current pricing**: DOE Office of Isotope R&D and Production annual reports (post-2010). Current price is likely substantially higher than the $40-85/liter in the CRS report. `not-yet-sourced` — confirm existence before searching
- **Wurzel & Hsu 2021** (meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/): Contains levitated dipole LDX data point in their cross-concept physics progress compilation. Already in repo — recommend reading for TRL physics baseline.

**Fleet-wide source disqualifications** (sources read or assessed; not applicable to this concept):

- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Read. Provides terrestrial modular fusion LCOE analog ($34-54/MWh for ~500 MWe). Integrated as order-of-magnitude cost reference in §5. Does not downgrade any blocking gap: the orbital concept's economics differ fundamentally (no grid delivery, no conventional CAS structure, no terrestrial BOP), and the ALPHA concepts were D-T MIF concepts with standard power blocks.

- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Applicable to D-T MFE with blanket, steam cycle, and tritium breeding. The orbital concept has none of these subsystems. The CAS structure provides vocabulary but no transferable cost data. Disqualified for quantitative use.

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Standard CAS framework (accounts 20-27 direct, 90-98 indirect). Inapplicable: no CAS 23 (vacuum vessel/blanket), no CAS 24 (power turbine plant), no CAS 26 (heat rejection), no conventional BOP. An orbital concept requires a space-system cost framework, not CAS. Disqualified for quantitative use.

- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific Monte Carlo LCOE model for pulsed driver-target concepts. Different confinement family, different physics regime, different cost structure. Disqualified.

- **Overview of the Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Planar-coil stellarator, D-T, terrestrial. Different confinement, different fuel, no orbital infrastructure. Disqualified.

- **Economic studies for heavy-ion-fusion**, **Energy from Inertial Fusion**, **Accelerators for IFE**, **AMPS high-yield IFE**, **Commercialization of laser fusion energy**: All IFE-specific, terrestrial, pulsed driver technologies. Disqualified.

- **An Assessment of the Economics of Future Electric Power Generation Options** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Historical terrestrial LCOE benchmarking against coal, nuclear, renewables. The orbital concept targets space power markets, not terrestrial grid competition. Benchmarking framework inapplicable. Disqualified.

- **NSS WPT workshop** (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`) and **arxiv 2401.15267** (`iter-02/sources/arxiv-2401-15267.md`): Read. These cover WPT transmission from orbit (not fusion-to-electricity conversion). The arxiv paper demonstrates LEO WPT array functionality but does not address the upstream conversion of fusion products to RF power. They confirm WPT infrastructure feasibility but do not resolve the energy conversion gap. Integrated as WPT context; do not downgrade any blocking gap.

- **NTRS NASA comparison SPS vs. CSP** (`iter-02/sources/ntrs-api-citations-20140003205-downloads-20140003205.md`): Read. SPS-to-CSP efficiency comparison for 1 GW systems. Context on space power economics but no fusion content. Provides the observation that SPS total infrastructure area remains large regardless of solar cell efficiency — useful framing for orbital power limits but no applicability to fusion LCOE. Disqualified for quantitative use.

---

## Summary

Proceed to qualitative narrative analysis only. The concept can be described in terms of (1) the physics motivation for orbital dipole confinement advantage over terrestrial alternatives, (2) engineering challenges unique to space deployment — HTS cryogenics in LEO, direct conversion, power beaming chain, (3) He-3 supply as a potentially civilization-scale constraint with no current solution, and (4) positioning relative to terrestrial levitated dipole competitors (OpenStar, Deutelio) and other orbital power concepts (space solar). Do not attempt quantitative LCOE modeling without Zephyr or peer-reviewed disclosure of: plasma performance targets, energy conversion mechanism, and an architecture-level plant design. Sourcing Teller 1992, Hasegawa 1987 PPPL-2627, ARIES-III, LDX experimental papers, and Kesner 2003 would substantially enrich the qualitative analysis but would not unlock a quantitative LCOE unless a reactor design study also becomes available.

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 7
important_count: 8
counting_method: "all_sections_deduplicated — blocking: (1) no plasma performance targets/Q, (2) energy conversion mechanism undefined, (3) no plant-level design/capital cost, (4) He-3 supply at fusion scale nonexistent, (5) capacity factor absent, (6) O&M cost model absent, (7) space-hardened HTS cryogenic system undesigned. Important: heating method undisclosed, D-He3 orbital plasma physics, He-3 post-2010 pricing, direct conversion TRL, launch cost not integrated, power beaming infrastructure cost, plant lifetime in LEO, He-3 on-orbit fuel handling."
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Poor"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor"
```