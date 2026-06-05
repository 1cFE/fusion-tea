## Design Point

- Name: MANTA NT Fusion Pilot Plant (Rutherford et al. 2024)
- Maturity: paper-concept
- P_native: 90 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/manta-reference-design.md
  - knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/greyb-firefly-interview.md

## 1. Availability of Data

**Rating: Moderate**

The negative-triangularity tokamak concept benefits from two distinct data streams: academic reactor design studies and limited early-stage commercial disclosure. The academic literature provides detailed physics and engineering parameters for reactor-scale NT machines, while commercial sources (Firefly Fusion) offer minimal technical detail beyond high-level targets.

**Academic Design Studies (Rich):**
The MANTA reference design (Rutherford et al. 2024) provides comprehensive reactor-level parameters, cost breakdowns, and engineering specifications for a 90 MWe NT pilot plant. The study includes plasma physics parameters, magnet specifications, blanket configuration, divertor design, operational cycle, overnight cost assessment ($3.4B), and LCOE projections ($396/MWh for a scaled 550 MW version). This represents one of the most detailed publicly available tokamak cost studies published in recent years, comparable in depth to ARC or SPARC conceptual designs.

Supporting academic work includes:
- Ball, Balestri, and Coda (2024) on ohmic-only NT operation, demonstrating that high-field NT tokamaks could potentially eliminate auxiliary heating systems entirely at Q > 10
- Experimental validation data from DIII-D (General Atomics) and TCV (EPFL/SPC) demonstrating NT plasma stability, ELM-free operation, and improved heat exhaust at laboratory scale

**Commercial Sources (Opaque):**
Firefly Fusion (founded 2024) has disclosed only high-level parameters through a GreyB interview with CEO Rustem Ospanov: major radius 2-2.5 m, magnetic field 10-12 T, target Q > 5, fusion power 50-100 MW with 20-30 MW heating input. No cost data, detailed engineering specifications, blanket choice, or plant-scale performance targets have been released. The company website (as of March 2026) provides team bios and advisor affiliations but no technical documentation.

**Data Gaps:**
- No published Firefly-specific reactor design or cost estimate
- Limited NT experimental database at reactor-relevant parameters (high beta_N, high density, radiative divertor operation)
- Uncertainty in NT confinement scaling laws — H_NA = 2.0 for ohmic NT plasmas is extrapolated from small experiments (TCV, DIII-D)
- No disclosed blanket choice or tritium breeding strategy from Firefly
- Manufacturing cost estimates for NT-specific coil geometry and divertor configuration are preliminary

The MANTA design provides a credible reference point for NT tokamak economics, but it is an academic study, not a commercial plant design. The analysis below uses MANTA as the design-point proxy given the absence of Firefly technical publications.

## 2. Challenges in Capturing System Function

**Ranked LCOE Modeling Challenges (Highest Impact First):**

### 1. HTS Magnet Cost and Lifetime (High Impact, Medium-High Uncertainty)

> "turbine efficiency, magnet cost and replacement time are the most critical upfront and lifetime cost drivers, respectively."
> — manta-reference-design.md, §1 Abstract

The MANTA design has TF coil costs of $1,500M — 44% of the $3.4B overnight cost. REBCO tape cost assumptions ($40/kA·m) and fabrication factors (5× material cost for superconducting components) carry large uncertainty ranges. A ±50% sensitivity sweep on REBCO cost keeps overnight cost below $5B, but the learning curve for large-scale REBCO production is unproven at fusion plant demand levels (>5,000 km per reactor).

Magnet lifetime sets the replacement cycle: PF2 requires replacement every ~2 full-power years due to neutron damage, driving an 88% availability assumption. TF coil lifetime is projected at >1,000 megawatt-years but lacks experimental validation under 14 MeV neutron flux at high fluence (>50 dpa).

**Modeling Challenge:** Magnet cost scales with REBCO tape performance (J_c at high field), structural material choices (Inconel 718 vs. alternatives), and manufacturing learning curves. Lifetime depends on neutron damage accumulation in tape, insulation radiation hardening, and quench protection system reliability — all TRL 5-6 at best for fusion conditions.

### 2. NT Confinement Scaling Uncertainty (High Impact, High Uncertainty)

> "Compared to positive triangularity, negative triangularity is far less understood. While MANTA's success in meeting the NASEM targets together with previous work show the plausibility of NT pilot/power plants, further experimental data, especially with regards to radiative ELM-free plasmas, is required to provide greater confidence that NT can scale to a reactor-class tokamak."
> — manta-reference-design.md, §8 Conclusion

The MANTA design assumes H_98y2 = 1.44 based on DIII-D NT campaign data, but the scaling database is thin. Ball et al. use H_NA = 2.0 for ohmic NT plasmas, extrapolated from TCV experiments. The confinement advantage claimed for NT — enabling ohmic-only operation at Q = 500 in MANTA parameters — is entirely dependent on these extrapolations holding at reactor scale.

> "These three confinement factors [H_NA, H_98, H_89] represent the biggest uncertainty in predicting how a NT plasma will behave... Since no existing scaling law incorporates NT with sufficiently broad applicability, one is forced to account for NT by choosing representative confinement enhancement factors."
> — ball-balestri-ohmic-nt-paper.md, §Appendix B

**Modeling Challenge:** If NT confinement does not scale as predicted, the design point may require larger size (higher R0), higher magnetic field (higher magnet cost), or external heating systems (negating the cost advantage). The confinement uncertainty propagates into fusion power, Q, and therefore LCOE.

### 3. Tritium Breeding Ratio and FLiBe Blanket Integration (Medium-High Impact, Medium Uncertainty)

The MANTA design uses a liquid immersion FLiBe blanket with TBR = 1.15. This is an unconventional blanket architecture for tokamaks — the FLiBe flows toroidally around the entire vacuum vessel in a continuous tank, serving dual purpose as breeder, coolant, and shield.

> "A liquid immersion blanket, consisting of molten 2LiF·BeF₂ (FLiBe) flowing down and around the vacuum vessel in a toroidally continuous tank, was selected due to the improved reactor serviceability and enhanced TBR relative to traditional blanket designs that rely on tritium breeding modules inside the vacuum vessel containing significant amounts of non-breeding structural material."
> — manta-reference-design.md, §5.1

This architecture trades high TBR for integration complexity:
- V-4Cr-4Ti vacuum vessel must be compatible with FLiBe at operating temperature (assumed compatible if MoF₆ dissolved for self-healing Mo barrier)
- 169 metric tonnes of FLiBe at $169/kg = $29M material cost, but supply chain readiness is TRL 3-4
- Tritium extraction from flowing molten salt at kg/day rates is unproven at scale
- Liquid blanket access and maintenance procedures differ from modular solid breeder schemes (ITER TBM baseline)

**Modeling Challenge:** Blanket cost ($380M in MANTA) depends on V-4Cr-4Ti fabrication at scale, FLiBe procurement and enrichment (Li-6), and tritium processing system complexity. TBR = 1.15 provides margin, but real-world breeding performance under neutron flux with impurities, temperature gradients, and tritium burnup has not been demonstrated.

### 4. Divertor Heat Load and Replacement Cycle (Medium Impact, Low-Medium Uncertainty for NT specifically)

NT offers a significant advantage here:

> "MANTA's divertor already operates in a far less challenging environment than that of other reactor-class tokamaks. This is a direct result of MANTA's ability to maintain a low P_SOL and high n_sep."
> — manta-reference-design.md, §3.2

MANTA's P_SOL = 23.5 MW vs. 83 MW for ARC V1 (positive triangularity). The divertor target metrics M₁ = 57.3 MW·T/m and M₂ = 70.7 are far below conventional tokamaks (ARC V1: M₁ = 263, M₂ = 707; EU-DEMO: M₁ = 98.9, M₂ = 1580).

**Modeling Challenge:** Despite NT's physics advantage, the divertor still requires tungsten monoblock cassettes on CuCrZr heat sinks, remote replacement infrastructure, and scheduled downtime. MANTA assumes a $150M divertor capital cost. The replacement frequency is less critical than for PT tokamaks but still contributes to capacity factor limits (79% effective availability including thermal storage duty cycle and maintenance).

### 5. Ohmic-Only Operation Feasibility (Low-Medium Impact, High Uncertainty)

Ball et al. demonstrate that high-Q NT tokamaks could eliminate auxiliary heating entirely:

> "In the limit of devices that can ignite, there is clearly no need for any external heating systems... Both cases reach the same fusion power P_fus ≃ 1.0 GW. However, the Ohmic scenario has a fusion gain of Q ≃ 500, while the case heated with external power of P_ext = 40MW has Q ≃ 30."
> — ball-balestri-ohmic-nt-paper.md, §Analytic results

If validated, this eliminates $370M of ICRF heating capital cost and tens of MW of recirculating power. However, MANTA's reference design retains 40 MW of ICRF heating, suggesting the community has not yet converged on ohmic-only as a baseline strategy.

**Modeling Challenge:** Ohmic-only operation is attractive but unproven at reactor scale. If it works, LCOE drops significantly (higher Q, lower capex, lower opex). If it doesn't, the design defaults to MANTA's auxiliary-heated configuration. This is a binary fork in the design space.

### 6. Capacity Factor and Remote Maintenance (Medium Impact, Medium Uncertainty)

MANTA's environmental cycle is set by PF2 replacement every ~2 full-power years, with 2-month maintenance downtime per replacement. Combined with thermal storage duty cycle (90%) and maintenance schedule (88%), effective availability is ~79%.

> "MANTA's environmental cycle is therefore set by PF2, which will require replacement every ~2 full-power years."
> — manta-reference-design.md, §4.3

The demountable TF coil design allows vertical access to PF coils and vacuum vessel, but the remote handling system is "very uncertain" per the study.

**Modeling Challenge:** Capacity factor drives revenue and amortization. The 79% assumption is aggressive for a first-of-a-kind plant with undemonstrated remote handling at full neutron activation levels. Downside risk to 60-70% would increase LCOE proportionally.

## 3. Maturity of Key Subsystems and Components

**Listed in ascending order of maturity (least mature first):**

### Integrated FLiBe Liquid Immersion Blanket (TRL 2-3)

- **On paper only**: Toroidally continuous liquid blanket with FLiBe flowing around vacuum vessel in external tank
- **Demonstrated**: Small-scale molten salt experiments (MSRE), FLiBe material property measurements, compatibility tests with vanadium alloys under non-neutron conditions
- **Missing at scale**: Full-scale liquid blanket with 14 MeV neutron flux, tritium extraction from flowing FLiBe at kg/day rates, thermal-structural-fluid-tritium coupled integration under tokamak pulsed operation, V-4Cr-4Ti vacuum vessel fabrication at multi-hundred-tonne scale

The FLiBe blanket is architecturally distinct from ITER's modular solid breeder test blanket modules. No tokamak has operated with a liquid immersion blanket at any scale.

### NT Plasma Confinement Scaling at Reactor Parameters (TRL 3-4)

- **Demonstrated**: ELM-free NT plasmas at DIII-D and TCV with improved heat exhaust, L-mode-like edge stability at high normalized pressure (β_N ~ 3.5 on DIII-D), H_98y2 ~ 1.0-1.5 in diverted NT configurations
- **On paper only**: H_98y2 = 1.44 at reactor density, temperature, and power; sustained radiative divertor operation in NT at high Greenwald fraction (f_GW = 0.88); H_NA = 2.0 for ohmic-only NT operation enabling Q = 500
- **Missing at scale**: High-power NT plasma operation (P_fus > 10 MW), long-pulse NT burn (>100 s), validation of confinement scaling laws with reactor-relevant heating, current drive, and impurity seeding

> "The most essential area of future work will be continuing NT studies on existing devices."
> — manta-reference-design.md, §8 Conclusion

### Tritium Fuel Cycle for FLiBe Blanket (TRL 3-4)

- **Demonstrated**: Lab-scale tritium extraction from molten salts (LIBRA experiments in Japan), tritium handling loops at gram-per-day rates (TFTR, JET legacy)
- **On paper only**: Closed-loop tritium processing at kg/day scale from FLiBe with <1% losses, integration with tokamak pulsed burn cycle (15-min pulses with 2-min inter-pulse), inventory management in flowing liquid breeder with thermal gradients
- **Missing at scale**: Industrial-scale tritium extraction from FLiBe (TBD technology — bubbling, permeation, molten salt distillation?), low-inventory storage compatible with liquid breeder chemistry, permeation barriers for V-4Cr-4Ti vacuum vessel, accountability and loss detection in liquid breeder systems

The MANTA design produces 1.8 kg tritium/year net. The extraction efficiency, inventory control, and permeation loss rates are critical unknowns.

### Demountable REBCO HTS TF Coils (TRL 5-6)

- **Demonstrated**: Full-scale non-demountable REBCO TF coils at 20 T (CFS SPARC magnet, tested and delivered Jan 2026), demountable joints for REBCO tape demonstrated at small scale (MIT PSFC), large-bore HTS coils under mechanical and thermal loads (Tokamak Energy Demo4 at 11.8 T)
- **On paper only**: 18-coil demountable TF coil set with joints at each coil for maintenance access, non-insulated winding at J_c = 1000 A/mm² at 25 K and 25 T, quench protection and resistive lead design for demountable operation
- **Missing at scale**: Reliable joint resistance at fusion-relevant current density over thousands of thermal and mechanical cycles, radiation-hardened REBCO tape and insulation at >50 dpa neutron fluence, long-term fatigue and delamination resistance in window-pane geometry, manufacturing at >5,000 km REBCO tape per reactor

> "While a detailed quench resilience analysis is outside the scope of this paper, given the evolving nature of the field, quench resilience needs are..."
> — manta-reference-design.md, §4.1

### Remote Handling and Maintenance (TRL 4-5)

- **Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for blanket and divertor cassette exchange, radiation-hardened robotics at TRL 6-7 for fission hot cells
- **On paper only**: Integrated remote maintenance scheme for demountable NT tokamak with vertical TF coil removal, PF coil replacement inside TF bore, and liquid blanket drain/fill procedures under activation
- **Missing at scale**: Radiation-hardened remote handling at fusion activation levels (14 MeV neutrons produce higher activation than fission), demonstrated 2-month PF coil replacement turnaround time, remote seal/joint assembly for demountable TF coils under tritium contamination

> "The design of a such a system for a fusion power plant is very uncertain; this would be a valuable area for future research."
> — manta-reference-design.md, Table C1 notes

### Tungsten Monoblock Divertor (TRL 6-7)

- **Demonstrated**: ITER-style tungsten monoblock divertors tested at 10-20 MW/m² heat flux in facilities (WEST, GLADIS, DTT prototypes), detached/radiative divertor operation demonstrated on multiple tokamaks (DIII-D, JET, ASDEX Upgrade)
- **On paper only**: NT-specific double-null divertor geometry with reduced M₁ and M₂ metrics, sustained operation at P_SOL = 23.5 MW with radiative detachment
- **Missing at scale**: Long-duration operation at NT-relevant heat fluxes under neutron damage (10-20 MW/m² for thousands of hours), large-area W-monoblock manufacturing with consistent quality, remote replacement cassette design for NT divertor geometry

The divertor is a relative strength for NT tokamaks due to low P_SOL, but the component maturity is comparable to conventional tokamaks.

### ICRF Heating System (TRL 7-8)

- **Demonstrated**: MW-class ICRF systems routinely operated on existing tokamaks (JET, ASDEX Upgrade), ITER ICRF system under construction (20 MW coupled power per launcher)
- **On paper only**: 40 MW coupled ICRF power at 110 MHz with He-3 minority heating in NT plasma (MANTA specification)
- **Missing at scale**: Continuous-wave ICRF operation at 40 MW total power in NT plasma geometry (if auxiliary heating retained), long-term reliability under neutron background, integration with NT divertor and first wall

If ohmic-only operation is validated, this subsystem can be eliminated entirely.

### PF Coils and Central Solenoid (TRL 6-7)

- **Demonstrated**: Large-scale PF coils with REBCO HTS (CFS SPARC CS prototype), insulated PIT-VIPER-like cables for low AC losses in pulsed operation
- **On paper only**: PF coils inside demountable TF coils (enabled by TF demountability), PF2 replacement cycle every ~2 full-power years
- **Missing at scale**: Demonstrated PF coil neutron lifetime under 14 MeV flux, in-bore replacement procedures for activated PF coils, AC loss management for 15-min pulse / 2-min inter-pulse cycle over decades

### Vacuum Vessel and In-Vessel Structures (TRL 6-7)

- **Demonstrated**: V-4Cr-4Ti alloy fabricated at small scale for fusion materials testing programs, welding and joining techniques developed
- **On paper only**: Multi-hundred-tonne V-4Cr-4Ti vacuum vessel with FLiBe compatibility (MoF₆ barrier formation), integration with liquid immersion blanket tank, port extensions for divertor and heating
- **Missing at scale**: V-4Cr-4Ti production at reactor-vessel scale (hundreds of tonnes), large-structure welding with fusion-grade quality control, long-term FLiBe corrosion resistance at operating temperature and neutron flux, activation and waste stream management for vanadium

V-4Cr-4Ti is chosen for low activation and FLiBe compatibility, but global production capacity is limited (vanadium is a byproduct of steel/titanium processing, and the V-4Cr-4Ti alloy grade has never been produced at multi-hundred-tonne scale).

### Balance of Plant (Thermal Cycle, Turbine, Heat Rejection) (TRL 8-9)

- **Demonstrated**: Conventional Rankine cycle at GW scale in fission and fossil plants, turbine-generator sets at 36% thermal efficiency (MANTA assumption), heat rejection systems (cooling towers, circulating water)
- **Missing at scale**: Integration with pulsed fusion heat source (15-min pulses with thermal storage to smooth output), tritium-compatible heat exchangers in primary loop, materials qualified for FLiBe primary coolant chemistry

The thermal cycle is mature technology but requires fusion-specific adaptation for pulsed operation and tritium containment.

## 4. Key Materials and Supply Chain Considerations

### REBCO Superconducting Tape (High Criticality, Emerging Supply Chain)

**Demand**: MANTA requires >5,000 km of REBCO tape for 18 TF coils plus PF and CS coils. Assumed cost: $40/kA·m.

**Supply**: Global REBCO production capacity is currently thousands of km/year (Shanghai Superconductor Technology, Faraday Factory Japan, CFS internal production). Scaling to tens of thousands of km/year for a multi-reactor fleet requires massive capital investment in tape manufacturing facilities.

**Performance requirement**: J_c = 1000 A/mm² at 25 K and 25 T with magnetic field perpendicular to tape plane. Commercial superOx tapes meet this target per MANTA study, but yield consistency, radiation hardening, and long-term degradation under neutron flux remain validation gaps.

**Cost trajectory**: CFS and Tokamak Energy target $10/kA·m for commercial viability (vs. $40/kA·m MANTA assumption). Learning curve depends on tape production volume and manufacturing process optimization.

**Supply chain risk**: REBCO supply is shared across all HTS tokamak concepts (CFS, Tokamak Energy, ENN, Neo Fusion, Firefly). First-to-market concepts will drive tape production scale-up; late entrants benefit from learning curve.

### FLiBe Molten Salt (Medium Criticality, Limited Current Supply)

**Demand**: MANTA requires 169 metric tonnes of 2LiF·BeF₂ at $169/kg = $29M material cost.

**Supply**: FLiBe is not produced at industrial scale. Beryllium global production is ~300 tonnes/year (Materion Corp dominates US production). Beryllium is toxic and requires specialized handling. Lithium fluoride is commodity-scale, but Li-6 enrichment for tritium breeding adds cost and supply constraints (only a few facilities produce 90+% Li-6, primarily in Russia and China using mercury amalgamation).

**Cost trajectory**: Araiinejad & Shirvan (2025) estimate NOAK FLiBe cost of $154/kg assuming 20% learning rate. MANTA uses $169/kg, consistent with near-term pricing.

**Supply chain risk**: FLiBe supply is shared with molten-salt fission reactors (Kairos Power, Terrestrial Energy) and other fusion concepts (potentially). Beryllium supply is the bottleneck — 300 t/year global production vs. 169 t for a single MANTA plant suggests fleet-scale supply constraints.

**Alternative**: Some tokamak designs use LiPb eutectic or solid ceramic breeders (Li₄SiO₄ pebbles) to avoid beryllium supply constraints. MANTA's choice of FLiBe is driven by TBR and serviceability, not supply chain robustness.

### Tritium (Existential Criticality, Severe Supply Constraint)

**Demand**: MANTA requires 900 g startup inventory (at $30k/g = $27M) and must breed 1.8 kg/year net to sustain operations plus fuel the next plant.

**Supply**: Global civilian tritium inventory is ~25-30 kg, produced as a byproduct of CANDU heavy-water reactors. Tritium decays at 5.5%/year. As CANDU reactors age and retire, external tritium supply will shrink.

**Sequencing constraint**: The first few D-T fusion plants must demonstrate tritium self-sufficiency (TBR > 1 with margin) before the fleet can scale. There is no margin for breeding shortfalls. MANTA's TBR = 1.15 provides 15% margin, but real-world breeding performance with impurities, temperature gradients, and extraction losses is unvalidated.

**Supply chain risk**: Shared across all D-T fusion concepts. This is not a competition for external supply (which is finite and shrinking) — it is a requirement that every D-T concept breed its own tritium successfully.

### V-4Cr-4Ti Vanadium Alloy (Medium-High Criticality, Limited Production)

**Demand**: MANTA vacuum vessel requires several hundred tonnes of V-4Cr-4Ti alloy. Assumed cost: $43/kg (India pricing), potentially 50% higher in US.

**Supply**: Vanadium is produced at ~100,000 t/year globally as a byproduct of steel and titanium processing. However, V-4Cr-4Ti alloy with controlled impurities (Ti ~4%, Cr ~4%, controlled O/C/N/H) has never been produced at multi-hundred-tonne scale. Small heats (kg to tonne-scale) have been produced for fusion materials testing.

**Alternative**: ODS (oxide-dispersion-strengthened) ferritic steels or SiC/SiC composites are alternative low-activation structural materials. MANTA notes these as future upgrade paths if TRL matures:

> "Given MANTA's modularity, these materials [ODS ferritic steels, SiC/SiC composites] could be explored later in MANTA's life cycle based on material technological readiness levels."
> — manta-reference-design.md, §5.1

**Supply chain risk**: V-4Cr-4Ti is not a commodity material. Scaling to reactor-vessel production requires dedicated supply chain development. Alternative materials (ODS, SiC/SiC) face similar challenges.

### Tungsten (Low-Medium Criticality, Adequate Supply with Manufacturing Challenges)

**Demand**: MANTA divertor requires tungsten monoblock tiles (exact tonnage not disclosed, but likely tens of tonnes based on divertor area).

**Supply**: Tungsten global production is ~85,000 t/year, adequate for fusion fleet demand. Tungsten is available but expensive ($30-50/kg for tungsten powder, significantly higher for formed monoblocks).

**Manufacturing challenge**: Fabricating large-area tungsten monoblock cassettes with CuCrZr heat sinks, consistent quality, and resistance to thermal cycling and neutron embrittlement is TRL 6-7. This is a manufacturing maturity issue, not a supply constraint.

**Supply chain risk**: Shared with fission and materials science applications. Supply is adequate, but specialized fusion-grade manufacturing capacity is limited.

### Summary: Supply Chain Bottlenecks in Rank Order

1. **Tritium** — existential constraint, TBR > 1 mandatory, no external supply at scale
2. **REBCO tape** — capacity scaling required, shared across HTS tokamak fleet, learning curve underway
3. **FLiBe / Beryllium** — limited beryllium supply (300 t/year global), toxic handling, Li-6 enrichment geopolitical risk
4. **V-4Cr-4Ti** — no reactor-scale production demonstrated, alternative materials at similar TRL
5. **Tungsten** — adequate supply, manufacturing scale-up required

## 5. Design Point Parameters

The quantitative description below is for the **MANTA NT Fusion Pilot Plant** (Rutherford et al. 2024), which serves as the design-point proxy for negative-triangularity tokamaks in the absence of published Firefly specifications.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Geometry** | | | | |
| R0 (major radius) | 4.55 m | manta-reference-design.md §2, Table 1 | high | spec key: `R0` |
| a (minor radius) | 1.2 m | manta-reference-design.md §2, Table 1 | high | spec key: `plasma_t` |
| elongation κ | 1.8 | manta-reference-design.md §2, Table 1 | high | spec key: `elon` |
| triangularity δ | -0.5 | manta-reference-design.md §2, Table 1 | high | spec key: `tria` (negative sign is defining feature) |
| plasma volume V_p | 155 m³ | manta-reference-design.md §2, Table 1 | high | informational |
| plasma surface area A_p | 258 m² | manta-reference-design.md §2, Table 1 | high | informational |
| aspect ratio A | 3.79 | [inferred: R0/a = 4.55/1.2] | high | informational |
| **Magnetic Field** | | | | |
| B (on-axis field) | 11 T | manta-reference-design.md §2, Table 1 | high | spec key: `B` |
| I_p (plasma current) | 10 MA | manta-reference-design.md §2, Table 1 | high | spec key: `ip` |
| q_95 (safety factor) | 2.3 | manta-reference-design.md §2, Table 1 | high | informational |
| q_min | 0.905 | manta-reference-design.md §2, Table 1 | high | informational |
| **Power Performance** | | | | |
| P_fus (fusion power) | 450 MW | manta-reference-design.md §2, Table 1 | high | informational — library back-solves from P_native + p_input |
| P_net (net electric) | 90 MWe | manta-reference-design.md §2, Table 1 | high | must equal Design Point `P_native` |
| P_input (auxiliary heating) | 40 MW | manta-reference-design.md §2, Table 1 (ICRF coupled power) | medium | spec key: `p_input` — note: Ball et al. claim ohmic-only (0 MW) viable at these parameters |
| P_SOL (scrape-off layer) | 23.5 MW | manta-reference-design.md §2, Table 1 | high | informational (divertor heat load) |
| P_th (total thermal) | 530 MW | manta-reference-design.md §2, Table 1 | high | informational |
| **Performance Metrics** | | | | |
| Q (plasma gain) | 11.5 | manta-reference-design.md §2, Table 1 | high | informational |
| Q_E (electricity gain) | 2.4 | manta-reference-design.md §2, Table 1 | high | informational |
| H_98y2 (confinement factor) | 1.44 | manta-reference-design.md §2, Table 1 | medium | extrapolated from DIII-D NT campaign data |
| τ_E (energy confinement time) | 0.94 s | manta-reference-design.md §2, Table 1 | medium | follows from H_98y2 |
| β_N (normalized beta) | 1.45 | manta-reference-design.md §2, Table 1 | high | spec key: `betan` |
| f_BS (bootstrap fraction) | 18% | manta-reference-design.md §2, Table 1 | medium | spec key: `fbs` |
| **Plasma State** | | | | |
| ⟨T_i⟩ (avg ion temp) | 7.3 keV | manta-reference-design.md §2, Table 1 | high | informational |
| ⟨T_e⟩ (avg electron temp) | 7.1 keV | manta-reference-design.md §2, Table 1 | high | informational |
| ⟨n⟩ (avg density) | 1.95 × 10²⁰ m⁻³ | manta-reference-design.md §2, Table 1 | high | spec key: `dens` |
| T_i0 (on-axis ion temp) | 19 keV | manta-reference-design.md §2, Table 1 | high | informational |
| n_0 (on-axis density) | 2.76 × 10²⁰ m⁻³ | manta-reference-design.md §2, Table 1 | high | informational |
| f_GW (Greenwald fraction) | 0.88 | manta-reference-design.md §2, Table 1 | medium | high density — risk for disruption |
| **Operational** | | | | |
| τ_pulse (pulse length) | 15 min | manta-reference-design.md §2, Table 1 | high | spec key: `burn_time` or informational |
| τ_inter (inter-pulse) | 2 min | manta-reference-design.md §2, Table 1 | high | informational |
| TBR (tritium breeding ratio) | 1.15 | manta-reference-design.md §2, Table 1 | medium | FLiBe blanket prediction — unvalidated |
| T production (net/year) | 1.8 kg | manta-reference-design.md §7.2, Table C5 | medium | TBR × burn time × availability |
| Availability (effective) | 79% | [inferred: 90% thermal storage duty × 88% maintenance] manta-reference-design.md §7.2 | medium | spec key: `availability` |
| T startup inventory | 900 g | manta-reference-design.md Table C4 | high | informational |
| **Cost Metrics** | | | | |
| Overnight cost | $3.4B | manta-reference-design.md §7.1 | medium | academic study, NOAK assumptions |
| Overnight $/kWe | $38M/MWe | [inferred: $3.4B / 90 MWe] | medium | informational |
| LCOE (550 MW scaled) | $396/MWh | manta-reference-design.md §7.2 | low | 30-year plant, not 90 MWe pilot |
| TF coil cost | $1.5B | manta-reference-design.md Table C1 | medium | 44% of overnight cost |
| **Magnet Specs** | | | | |
| TF coils (number) | 18 | manta-reference-design.md §4.1 | high | demountable REBCO HTS |
| TF coil type | REBCO HTS, non-insulated | manta-reference-design.md §4.1 | high | window-pane geometry |
| J_c (critical current density) | 1000 A/mm² at 25 K, 25 T | manta-reference-design.md §4.1 | medium | commercial superOx tape performance target |
| REBCO cost | $40/kA·m | manta-reference-design.md §7.1 | low | industry target, high uncertainty |
| PF coil replacement cycle | ~2 full-power years | manta-reference-design.md §4.3 | medium | PF2 sets environmental cycle |
| **Blanket / First Wall** | | | | |
| Blanket type | FLiBe liquid immersion | manta-reference-design.md §5.1 | medium | toroidally continuous tank around VV |
| FLiBe mass | 169 t | manta-reference-design.md Table C4 | medium | 2LiF·BeF₂ |
| FLiBe cost | $169/kg | manta-reference-design.md Table C4 | low | NOAK estimate, supply chain TRL 3-4 |
| Vacuum vessel material | V-4Cr-4Ti | manta-reference-design.md §5.1, Table 6 | medium | low activation, FLiBe-compatible |
| VV cost | $43/kg | manta-reference-design.md Table 6 | low | India pricing, 50% higher in US |
| Divertor type | Double-null tungsten monoblock | manta-reference-design.md §3 | high | CuCrZr heat sinks |
| Divertor cost | $150M | manta-reference-design.md Table C1 | medium | capital cost estimate |

### Notes on Design Point Selection

The MANTA design is an **academic community study**, not a Firefly company specification. Firefly has disclosed only high-level parameters (R = 2-2.5 m, B = 10-12 T, Q > 5, P_fus = 50-100 MW) through a GreyB interview. MANTA represents the closest published NT tokamak reference design at pilot-plant scale and is used as the design-point proxy.

**Key uncertainties for the named design point:**
- **Confinement**: H_98y2 = 1.44 is extrapolated from small NT experiments (DIII-D, TCV); reactor-scale validation pending
- **Auxiliary heating**: MANTA assumes 40 MW ICRF; Ball et al. claim ohmic-only viable at Q = 500 for same parameters — heating requirement is genuinely uncertain
- **Blanket**: FLiBe liquid immersion blanket is unconventional for tokamaks; TBR = 1.15 is predictive, not demonstrated
- **Availability**: 79% effective availability assumes 88% maintenance availability with PF2 replacement every ~2 FPY — remote handling capability unproven

## 5b. Override Candidates

The per-account walkthrough below identifies company-grounded departures from 1costingFE library defaults for the MANTA NT design point. The MANTA study provides component-level cost breakdowns, enabling accountable overrides where the design departs from tokamak library assumptions.

```yaml
overrides:
  - account: C220103
    value: 1500.0
    enabled: true
    provenance: direct
    source: "manta-reference-design.md §7.1, Table C1"
    rationale: |
      MANTA publishes TF coil cost at $1,500M for 18 demountable REBCO HTS coils.
      Breakdown: REBCO tape at $40/kA·m, Inconel 718 structure, 5× fabrication
      factor for superconducting components. Library default is geometry-based
      and may not capture demountable joint costs or window-pane coil geometry.

  - account: C220104
    value: 370.0
    enabled: false
    provenance: direct
    source: "manta-reference-design.md §7.1, Table C1"
    rationale: |
      MANTA specifies $370M for 40 MW ICRF heating at 110 MHz (He-3 minority).
      However, Ball et al. demonstrate ohmic-only operation viable at Q=500
      for same device parameters (ball-balestri-ohmic-nt-paper.md). Heating
      requirement is genuinely uncertain. Override disabled to preserve library
      default heating cost; enable if auxiliary heating is validated as required.

  - account: C220108
    value: 150.0
    enabled: true
    provenance: direct
    source: "manta-reference-design.md §7.1, Table C1"
    rationale: |
      MANTA publishes divertor cost at $150M for double-null tungsten monoblock
      design. NT-specific geometry and reduced heat load (P_SOL = 23.5 MW vs.
      ~80 MW for conventional tokamaks) may reduce replacement frequency, but
      capital cost is explicitly stated.

  - account: CAS27
    value: 28.6
    enabled: true
    provenance: direct
    source: "manta-reference-design.md §7.1, Table C4, Table 6"
    rationale: |
      MANTA FLiBe blanket: 169 t × $169/kg = $28.6M (rounded from $28.561M).
      Library default uses solid breeder unit costs inappropriate for liquid
      immersion blanket. This is material-only cost; fabrication/structure
      in C220101.

  - account: CAS70
    value: 0.70 * generic.costs.cas70
    enabled: true
    provenance: derived
    source: "manta-reference-design.md §7.2, Table C5"
    rationale: |
      MANTA assumes ~1 person/MWe staffing at $150k/employee-year = ~$15M/yr
      for 90 MWe plant. This is ~30% lower than library default staffing
      assumptions for tokamaks. Relative override: 70% of library CAS70.
```

**Override Count Sanity Check:**
Expected band for Archetype-Fit = High is 0-4 enabled overrides. Actual enabled count: 4 (C220103, C220108, CAS27, CAS70). Within expected range.

**Accounts Considered but Not Overridden:**

- **C220101** (blanket structure): MANTA reports $380M blanket cost, but this includes FLiBe tank, vacuum vessel integration, and first wall — not directly comparable to library's breeding blanket account without detailed decomposition. Library default retained.
- **C220102** (shield): MANTA uses B₄C and WC shielding layers (Table 6), but no standalone shield cost is broken out — included in blanket and VV accounts. Library default retained.
- **C220105** (primary structure): MANTA includes inter-coil structure and machine base, but no standalone cost figure. Library default retained.
- **C220106** (vacuum vessel): V-4Cr-4Ti vessel at $43/kg, but total vessel cost not isolated in Table C1. Library default retained.
- **C220107** (power supplies): TF power supplies at $0.5M each (18 coils = $9M) and resistive leads at $2M each ($36M total) reported, but library default likely covers this. No override without full electrical plant breakdown.
- **C220110** (remote handling): MANTA reports $55M but notes "very uncertain" — library default likely equally uncertain. No override.
- **C220111** (installation): MANTA applies 10% contingency and includes assembly in indirect costs, but no direct installation cost breakdown. Library default retained.
- **CAS21** (buildings): MANTA assumes brownfield site saving ~$400M vs. greenfield, but this is not a design-point feature — it's a siting assumption. Library default retained.
- **CAS23** (turbine): MANTA assumes 36% thermal efficiency for Rankine cycle — library default thermal cycle efficiency is appropriate. No override.
- **CAS24** (electric plant): No MANTA-specific cost figure. Library default retained.
- **CAS26** (heat rejection): No MANTA-specific cost figure. Library default retained.
- **CAS80** (fuel cost): Tritium at $30k/g with 900 g startup inventory = $27M one-time; library handles consumables. No recurring fuel cost override justified.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | NT confinement scaling validation at reactor parameters (H_98y2 = 1.44 for MANTA, H_NA = 2.0 for ohmic-only at Q > 100) | S3, S2 | truly-unknown | blocking | High-power long-pulse NT experiments on DIII-D/KSTAR/EAST with reactor-relevant heating, density, and impurity seeding. Academic publications from ongoing NT campaigns. |
| 2 | Ohmic-only operation feasibility — can high-Q NT tokamaks eliminate auxiliary heating entirely? | S2, S5b | truly-unknown | important | Experimental validation of ohmic-heated NT plasmas at high normalized pressure and density. If validated, eliminates $370M heating capex. |
| 3 | FLiBe liquid immersion blanket TBR and tritium extraction at kg/day rates | S3, S4 | truly-unknown | blocking | Neutronics validation for toroidally continuous FLiBe tank with V-4Cr-4Ti VV; tritium extraction technology demonstration at fusion-relevant throughput. |
| 4 | REBCO HTS tape neutron lifetime and quench resilience in demountable TF coil geometry | S3, S4 | truly-unknown | blocking | Neutron irradiation testing of REBCO tape, insulation, and joints at >50 dpa; quench detection and protection validation for non-insulated windings. |
| 5 | V-4Cr-4Ti vacuum vessel fabrication and FLiBe compatibility at scale | S3, S4 | truly-unknown | important | Multi-hundred-tonne V-4Cr-4Ti heat production and welding qualification; long-term FLiBe corrosion testing under neutron flux and thermal cycling. |
| 6 | Remote handling turnaround time for PF2 replacement under full neutron activation | S3, S2 | truly-unknown | important | Integrated remote handling demonstration for activated tokamak components; 2-month turnaround validation for PF coil replacement inside TF bore. |
| 7 | Magnet replacement cycle cost and schedule for REBCO HTS under neutron damage | S2, S5 | truly-unknown | important | Accelerated neutron damage testing for REBCO tape; validated replacement procedures for demountable TF coils. Library default PF replacement cost may not capture NT-specific geometry. |
| 8 | NT divertor power split (inner vs. outer strike point) and radiative detachment stability | S2 | truly-unknown | nice-to-have | UEDGE and SOLPS modeling validated against NT divertor experiments; long-pulse radiative divertor operation on DIII-D or TCV. |
| 9 | REBCO tape supply chain scaling to multi-GW fleet demand (tens of thousands of km/year) | S4 | not-yet-sourced | important | REBCO manufacturer roadmaps (Shanghai Superconductor, Faraday Factory Japan, CFS); tape production capital investment plans and learning curve data. |
| 10 | FLiBe / beryllium supply chain capacity for fusion fleet (hundreds of tonnes per plant) | S4 | not-yet-sourced | important | Beryllium production forecasts from Materion and other suppliers; FLiBe cost and availability projections from molten salt reactor community (Kairos, Terrestrial Energy). |
| 11 | Firefly-specific reactor design, blanket choice, heating approach, and cost estimate | S1, all | proprietary | important | Firefly technical publications, FIA member profile updates, or conference presentations. Company is early-stage (founded 2024) with minimal public disclosure as of March 2026. |

## 7. Family-Delta vs Comparables

The negative-triangularity tokamak differs from conventional positive-triangularity (PT) HTS tokamaks in plasma shape optimization, divertor heat load management, and potentially auxiliary heating requirements. The deltas below are articulated against the four fixed comparables: 01-hts-compact-tokamak (CFS ARC), 21-spherical-tokamak-hts (Tokamak Energy), 28-hts-tokamak-full-hts (Energy Singularity), and 33-state-backed-tokamak-best (Neo Fusion BEST).

### vs. 01-hts-compact-tokamak (CFS ARC V1) — Divertor Heat Load Advantage

**Delta**: NT plasma shaping inverts the D-shaped cross-section (δ = -0.5 vs. δ = +0.4 for ARC), which stabilizes the plasma edge and eliminates ELMs without ELM suppression coils. This reduces scrape-off-layer power (P_SOL) by ~3.6×:

> "MANTA's M₁ = 57.3 MW·T/m vs. ARC V1 (PT) = 263, CFETR = 82.2, EU-DEMO = 98.9"
> — manta-reference-design.md §3, Table 2

MANTA: P_SOL = 23.5 MW
ARC V1: P_SOL ~ 83 MW (estimated from published P_fus = 525 MW, Sorbom 2015)

**TEA Implication**: Lower P_SOL reduces divertor material stress, potentially extending component lifetime and reducing replacement frequency. MANTA's divertor capital cost is $150M — comparable to PT tokamaks despite lower heat load, suggesting the cost advantage is in operational lifetime, not upfront cost. **Cost effect: neutral to small advantage** (lower replacement frequency, but capital cost similar). **Magnitude uncertain** — replacement cycle not quantified in MANTA study.

### vs. 01-hts-compact-tokamak (CFS ARC) — Auxiliary Heating Uncertainty

**Delta**: Ball et al. demonstrate that ohmic-only NT operation at MANTA parameters achieves Q = 500 vs. Q = 30 with 40 MW auxiliary heating:

> "Both cases reach the same fusion power P_fus ≃ 1.0 GW. However, the Ohmic scenario has a fusion gain of Q ≃ 500, while the case heated with external power of P_ext = 40MW has Q ≃ 30."
> — ball-balestri-ohmic-nt-paper.md §Numerical results

If validated, this eliminates $370M ICRF heating capital cost and tens of MW recirculating power. ARC uses 25-35 MW of ICRF heating per Sorbom 2015.

**TEA Implication**: **Potential cost advantage of $370M capex + reduced opex** if ohmic-only operation is validated. However, MANTA's reference design retains 40 MW ICRF, indicating the community has not converged on ohmic-only as baseline. **Cost effect: large potential advantage, but unvalidated.** Magnitude: ~11% of overnight cost ($370M / $3.4B) if heating eliminated.

### vs. 01-hts-compact-tokamak (CFS ARC) — Demountable TF Coils vs. Non-Demountable

**Delta**: MANTA uses demountable REBCO TF coils to enable vertical maintenance access for PF coils and vacuum vessel. ARC's design (Sorbom 2015) did not specify demountability in the original publication, though CFS's SPARC prototype uses demountable joints.

**TEA Implication**: Demountable joints add resistive losses and require power supplies/resistive leads ($0.5M + $2M per coil = $45M for 18 coils), but enable faster maintenance turnaround and reduced downtime. MANTA assumes 2-month PF coil replacement cycle inside TF bore. **Cost effect: small penalty in capital cost, potential advantage in availability.** Net effect depends on whether maintenance time reduction justifies joint cost.

### vs. 21-spherical-tokamak-hts (Tokamak Energy ST40) — Aspect Ratio and Geometry

**Delta**: NT tokamaks use conventional aspect ratio (A ~ 3-4) rather than spherical geometry (A < 2). MANTA: A = 3.79. Spherical tokamaks achieve higher β and smaller size but require complex center-post engineering and have limited space for blanket/shield inboard.

**TEA Implication**: Conventional aspect ratio allows thicker inboard blanket and shield, improving TBR and magnet protection. MANTA achieves TBR = 1.15 with liquid immersion blanket; spherical tokamaks struggle to exceed TBR > 1 due to inboard space constraints. **Cost effect: advantage in tritium self-sufficiency, penalty in size.** Magnitude: MANTA at 90 MWe has R0 = 4.55 m; a spherical tokamak at similar power might achieve R0 ~ 2-3 m, but with lower TBR and higher magnet replacement frequency (tighter inboard neutron shielding).

### vs. 28-hts-tokamak-full-hts (Energy Singularity HH70) — Shared HTS Magnet Technology, Different Plasma Shape

**Delta**: Both concepts use REBCO HTS magnets at 10-12 T, but NT vs. PT plasma shaping is the key difference. Energy Singularity's HH70 uses positive triangularity (conventional H-mode) with active ELM suppression (RMP coils or pellet pacing). NT eliminates ELMs passively through plasma shaping.

**TEA Implication**: NT avoids RMP coil capital cost and pellet injection system complexity. However, PT H-mode has a larger experimental database and higher confinement at similar parameters (H_98y2 ~ 1.0-1.1 for PT H-mode vs. H_98y2 ~ 1.44 claimed for NT — but the NT value is extrapolated). **Cost effect: small advantage if NT eliminates ELM control systems; large penalty if NT confinement scaling does not hold.** Magnitude: RMP coils are small fraction of overnight cost (likely <$50M), but confinement uncertainty dominates.

### vs. 33-state-backed-tokamak-best (Neo Fusion BEST) — Conventional PT Tokamak Baseline

**Delta**: Neo Fusion's BEST is a conventional PT tokamak at larger scale (R0 likely 5-8 m based on 1 GWe target). NT at compact scale (R0 = 4.55 m for 90 MWe) represents a different point in the tokamak design space: smaller, higher-field, potentially lower auxiliary heating.

**TEA Implication**: Compact high-field enables smaller size and potentially lower capital cost per unit power, but requires higher magnetic field (higher REBCO cost, higher structural loads). BEST likely operates at lower field (6-8 T) with larger size and conventional auxiliary heating. **Cost effect: NT advantage in compactness if ohmic-only validated; PT advantage in technology maturity and larger experimental database.** Magnitude: cannot quantify without BEST cost data.

### Shared Subsystems (No Delta)

The following subsystems are shared across all HTS tokamak concepts and provide **no differentiation**:
- REBCO HTS magnet supply chain (same tape, same suppliers, same learning curve)
- Tritium breeding requirement (all D-T concepts require TBR > 1)
- Vacuum vessel and first wall materials (low-activation steels or vanadium alloys)
- Balance of plant (thermal cycle, turbine, heat rejection)
- Remote handling and maintenance complexity (14 MeV neutron activation)

### Summary: NT Tokamak Unique Deltas

| Delta | Direction | Magnitude | Confidence |
|-------|-----------|-----------|------------|
| Divertor P_SOL reduction (3.6× vs. PT) | Advantage | Small to medium (longer component life, lower replacement frequency) | Medium |
| Ohmic-only heating (if validated) | Advantage | Large ($370M capex, reduced opex) | Low (unvalidated at reactor scale) |
| NT confinement scaling (H_98y2 = 1.44) | Advantage or Penalty | Large (determines size, field, Q) | Low (thin experimental database) |
| ELM elimination (passive, no RMP coils) | Advantage | Small (<$50M capex for RMP coils avoided) | Medium |
| Demountable TF coils | Small penalty (joints) + potential advantage (availability) | Small (net ~$45M penalty, but faster maintenance) | Medium |
| Conventional aspect ratio vs. spherical | Advantage (TBR, blanket space) + Penalty (size) | Medium (TBR = 1.15 vs. <1.05 for ST; but larger R0) | Medium |

The **largest uncertainties** are confinement scaling and ohmic-only heating feasibility. If both validate, NT offers significant cost advantages over PT tokamaks. If either fails, NT falls back to a conventional HTS tokamak with slightly different plasma shaping.

## 8. Sources

### Primary Sources (Critical for Design Point Parameters)

1. **Rutherford, E.J. et al. (2024)** "MANTA: A negative-triangularity NASEM-compliant fusion pilot plant." arXiv:2405.20243. Available at: https://arxiv.org/abs/2405.20243. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/manta-reference-design.md (164 KB).
   - **Contribution**: Complete reactor design (R0, B, I_p, Q, P_fus, P_net, pulse length, TBR), cost breakdown ($3.4B overnight, $1.5B TF coils, $370M heating, $150M divertor, $380M blanket), FLiBe liquid immersion blanket specification, demountable REBCO HTS coil design, divertor metrics (P_SOL = 23.5 MW, M₁ = 57.3), LCOE projection ($396/MWh for 550 MW scaled plant), magnet replacement cycle, materials specifications (V-4Cr-4Ti VV, REBCO at $40/kA·m, FLiBe at $169/kg).

2. **Ball, J., Balestri, M., Coda, S. (2024)** "On the feasibility of Ohmically heated negative triangularity tokamak power plants." Available at: https://arxiv.org/html/2407.06439v2. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/ball-balestri-ohmic-nt-paper.md (55 KB).
   - **Contribution**: Demonstration that ohmic-only NT operation at MANTA parameters achieves Q = 500 vs. Q = 30 with auxiliary heating; H_NA = 2.0 confinement enhancement factor for ohmic NT plasmas; analysis showing auxiliary heating systems unnecessary for high-Q NT tokamaks; uncertainty quantification for NT confinement scaling laws.

### Secondary Sources (Company Context and Validation)

3. **GreyB / Scouted Interview with Firefly Fusion CEO Rustem Ospanov** (2024). "Scouted: Firefly Fusion." Available at: https://greyb.com/blog/firefly-fusion-scouted-interview. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/greyb-firefly-interview.md (9 KB).
   - **Contribution**: Firefly high-level parameters (R = 2-2.5 m, B = 10-12 T, Q > 5, P_fus = 50-100 MW, P_input = 20-30 MW), HTS magnet choice rationale, compact design philosophy ("compactness brings affordability"), NT physics risk acknowledgment.

4. **DIII-D National Fusion Facility Collaboration Page** — Firefly Fusion. Available at: https://d3dfusion.org/fireflyfusion/. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/firefly-fusion-diii-d-collaboration.md (3 KB).
   - **Contribution**: Confirmation of Firefly-DIII-D collaboration for NT plasma experiments, LUCIOLE prototype device specification (actively-cooled copper magnets for rapid iteration), validation that NT plasmas have been experimentally demonstrated.

5. **Firefly Fusion Website** (March 2026). Available at: https://fireflyfusion.energy/. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-02/sources/firefly-website-2026.md (2 KB).
   - **Contribution**: Team and advisor biographies (Justin Ball, Yves Martin, Pascale Hennequin, Jérémie Bucalossi), company location (Cadarache, France), founding date (2024), but no technical parameters disclosed.

6. **Venture Kick Profile** — Firefly Fusion. Available at: https://www.venturekick.ch/firefly-fusion. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/venture-kick-profile.md (1 KB).
   - **Contribution**: CHF 50k funding, "microwaves to create and control hot plasma" (suggests ECRH, but weakly sourced).

7. **Fusion Energy Base Profile** — Firefly Fusion. Available at: https://www.fusionenergybase.com/organizations/firefly-fusion. Saved: knowledge/concept_research/29-negative-triangularity-tokamak/iter-01/sources/fusion-energy-base-profile.md (1 KB).
   - **Contribution**: Phased magnet strategy (copper for LUCIOLE prototype, HTS for commercial plants), location, founding date.

### Supporting Academic Literature (Not Directly Cited but Contextual)

8. **Sorbom, B.N. et al. (2015)** "ARC: a compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets." Fusion Engineering and Design, 100, pp. 378–405. doi:10.1016/j.fusengdes.2015.06.001.
   - **Context**: ARC design provides PT tokamak comparison baseline (R0 = 3.3 m, B0 = 9.2 T, P_fus = 525 MW, P_SOL ~ 83 MW).

9. **Araiinejad, L.S. and Shirvan, K. (2025)** "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants." Applied Energy, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
   - **Context**: FLiBe cost projections ($154/kg NOAK with 20% learning rate), tokamak LCOE drivers (capacity factor, magnet cost, regulatory markup), HTS cost targets ($10/kA·m for commercial viability).

### Data Gaps and Unavailable Sources

- **Firefly Fusion technical design publication**: Does not exist as of March 2026. Company is early-stage (founded 2024) with minimal public disclosure beyond high-level parameters.
- **NT tokamak experimental database at reactor-relevant parameters**: Limited to DIII-D and TCV campaigns, with highest plasma current ~2 MA and highest normalized pressure β_N ~ 3.5. No reactor-scale (I_p = 10 MA, β_N = 1.5, high density) NT plasmas demonstrated.
- **REBCO HTS neutron lifetime data**: Neutron irradiation testing at >50 dpa for REBCO tape, insulation, and joints is ongoing but not published at full fusion-relevant fluence.
- **FLiBe blanket tritium extraction at kg/day rates**: Technology demonstration does not exist at scale. LIBRA experiments in Japan are gram/day scale.