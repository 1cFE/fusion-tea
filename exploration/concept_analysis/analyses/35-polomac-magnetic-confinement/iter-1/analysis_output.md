## Design Point

(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)

## Section 1: Availability of Data

**Rating: Limited**

The Polomac Magnetic Confinement concept developed by Deutelio has a very thin public data footprint. Only three primary sources are available:

1. **2014 FED paper** — "Poloidal magnetic confinement with magnetic tunnels" by F. Elio (Fusion Engineering and Design, 2014). This is the foundational technical paper introducing the concept.
2. **2024 JTSP technical report** — Updated concept description including small prototype specifications and reactor-scale projections.
3. **Deutelio company profile** — High-level promotional materials with minimal technical content.

Both technical papers were authored by F. Elio, a mechanical engineer with extensive fusion device construction experience (RFX, ITER, W7-X). The 2014 paper was explicitly noted as "a personal unfunded voluntary activity of the author not related to his present duty in the JRC of the European Commission nor to the European policy on fusion research," indicating this began as an independent conceptual study.

> "Further analyses on MHD, confinement, stability and an outline engineering design are required to assess the possibilities envisaged"
> — elio-2014-fed-poloidal-confinement.md, §Conclusions

The company, Deutelio, is registered in Luxembourg and is very early-stage. They placed 4th in the 2024 Boldbrain Startup Challenge. No peer-reviewed experimental data, independent analyses, or detailed plant studies exist. The company profile indicates a development roadmap progressing from small prototype → heat generators → electrical generation, with "Energy generation by 2030" as a stated timeline, but no quantitative performance targets or cost estimates are publicly disclosed.

**Key data gaps:**
- No experimental validation of magnetic tunnel concept
- No published cost estimates or LCOE projections
- No blanket, shielding, or balance-of-plant design
- No tritium fuel cycle analysis (if D-T operation)
- No heating system specification for reactor scale
- No plasma confinement data at any scale

The concept remains at TRL 2-3: analytical formulation with small prototype under development, but no experimental demonstration of the core physics claim (that magnetic tunnels enable effective poloidal confinement without support-wire losses).

## Section 2: Challenges in Capturing System Function

Polomac presents several distinctive modeling challenges, ranked by impact on LCOE uncertainty:

### 1. Unvalidated Core Physics (Highest Uncertainty)

The magnetic tunnel concept — the entire basis for this approach — has never been experimentally demonstrated. Previous poloidal confinement experiments "suffered from poor field intensity (0.1–0.3 T) and energy losses against the support wires" (elio-2014-fed-poloidal-confinement.md, §Past dipole experiments). Polomac claims to solve this via shaped field-line "tunnels" that remain plasma-free, but:

> "The particles lost on the symmetry plane of the tunnels and in the weak field regions above/below them affect the energy balance of the plasma to an extent which should be quantified"
> — jtsp-2024-polomac-technical-report.md, §IV.a

Particle loss rates through these tunnels are unknown. Without experimental validation, the concept's claimed confinement advantage over tokamaks (factor of 2-3 lower magnetic field for equivalent conditions) cannot be confirmed.

### 2. D-D vs D-T Fuel Choice Ambiguity

The concept targets D-D fuel to avoid tritium breeding complexity:

> "avoiding the development of the breeding blanket to produce the Tritium"
> — jtsp-2024-polomac-technical-report.md, Abstract

However, D-D operation requires 142× more challenging Lawson criterion than D-T (jtsp-2024-polomac-technical-report.md, §VI). The reactor-scale projections include both:
- **D-T pathway**: 8.1 keV, 10²⁰ m⁻³ density, 4-5 s confinement, 2-3 T field
- **D-D pathway**: 100-200 keV, ~10²¹ m⁻³ density, 20-40 s confinement

Neither pathway has been demonstrated. The D-T path is more near-term achievable but eliminates the claimed economic advantage of avoiding tritium breeding. The D-D path is dramatically more challenging and likely decades away even if the core magnetic tunnel concept works.

For LCOE modeling, this creates a bifurcation: a D-T Polomac would face similar blanket/fuel-cycle costs and neutron damage issues as tokamaks, partially negating the magnet cost advantage. A D-D Polomac would avoid blanket costs but face extreme performance requirements with no clear path to demonstration.

### 3. Heating Method Not Specified

The small prototype uses "electron cyclotron resonance (5-10 kW microwave heating at 4 GHz)" (jtsp-2024-polomac-technical-report.md, §III), but no heating method for reactor-scale operation is disclosed. D-D operation at 100-200 keV requires extreme temperatures with no obvious heating technology pathway. This is flagged in the dossier as a "critical gap — D-D requires very high temperatures so this is a critical technical gap."

### 4. Power Consumption vs Output Unknown

The 2014 paper noted a severe problem with the conceptual design at that stage:

> "The power consumption in 0.1 m thick copper coil layer reaches 700 MW, like in JET but excessive for steady operation"
> — elio-2014-fed-poloidal-confinement.md, §Coil support and supply

This was for a 1300 m³ plasma volume design with copper coils. The 2024 report mentions "superconducting magnets" (deutelio-company-profile.md, §Development Roadmap) as a future transition, but provides no analysis of recirculating power fraction, Q_eng, or net electric output for any design point. Without these, LCOE cannot be estimated.

### 5. Scaling from 100 eV Prototype to keV Reactor

The planned small prototype operates at:
- 100 eV ion temperature
- 0.2-0.3 T magnetic field
- 150 dm³ plasma volume
- Hydrogen (not deuterium) plasma

This must scale to D-T conditions (8.1 keV, 2-3 T) or D-D conditions (100-200 keV). This represents a ~80× temperature increase and ~10× magnetic field increase. Such extrapolations carry enormous physics risk, especially given that the magnetic tunnel particle-loss mechanism is scale-dependent and untested.

### Contradictions with Fixed Design-Point Selection

The upstream design-point selection for this concept is pending. When it arrives, it may contradict the limited available data. The technical papers describe conceptual reactor conditions but no specific "named plant" with a defined net-electric output. Any design-point parameters in Section 5 below will necessarily be inferred or estimated rather than company-stated.

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Magnetic Tunnel Support System — TRL 2

**On paper only**: The magnetic tunnel concept is the core innovation: shaped field-line channels that create plasma-free regions for mechanical support of the internal dipole coil. This solves the historical problem of support-wire plasma contamination in dipole experiments.

**Missing at scale**: No prototype exists. Particle loss rates through tunnels are unquantified. The 2024 JTSP paper notes:

> "Protons moving straight at 100 eV on the symmetry plane of the tunnel cannot be deviated and hit the vault"
> — jtsp-2024-polomac-technical-report.md, Figure 14 caption

And:

> "Protons at lower energy 10 eV can be trapped in the weak field region above/below the tunnel...They could accumulate drifts or get aligned with the field and escape the confinement"
> — jtsp-2024-polomac-technical-report.md, Figure 13 caption

The extent to which these losses degrade confinement is unknown. The entire concept's viability depends on these losses being acceptable. No experimental data exists. A systematic particle path analysis is contracted to Paul Scherrer Institute but not yet complete (jtsp-2024-polomac-technical-report.md, §IV.a).

### Reactor-Scale Heating System — TRL 1-2

**On paper only**: The small prototype uses 5-10 kW ECRH at 4 GHz. No heating system for reactor-scale D-T (8.1 keV) or D-D (100-200 keV) operation has been specified.

**Missing at scale**: D-D at 100-200 keV is far beyond demonstrated auxiliary heating capabilities for any magnetic confinement concept. Even D-T at 8.1 keV in a novel magnetic geometry with untested heating efficiency represents a major development requirement. The absence of any disclosed heating strategy for the reactor is a critical gap.

### Tritium Breeding Blanket (if D-T pathway) — TRL 2-3

**On paper only**: The concept aims to avoid tritium breeding by using D-D fuel. If D-T operation is pursued instead (the more near-term achievable pathway), a blanket would be required. No blanket design has been disclosed.

**Missing at scale**: Standard D-T blanket challenges (tritium breeding ratio >1, neutron damage, coolant chemistry, remote handling) apply. The poloidal geometry may create unique blanket engineering challenges around the magnetic tunnel penetrations. No analysis of TBR, blanket coverage fraction, or neutron streaming through tunnels exists.

### MHD Simulation and Stability Analysis — TRL 3-4

**Demonstrated**: The concept developer has created custom MHD code:

> "Established MHD codes developed for Tokamaks and Stellarators...are not applicable to the Polomac"
> — jtsp-2024-polomac-technical-report.md, §IV.b

**On paper only**: The code "must be validated with benchmarks" (jtsp-2024-polomac-technical-report.md, §IV.b). Stability analysis has not been performed: "Stability analysis will be committed to plasma specialists after completing the verification of the above steps" (jtsp-2024-polomac-technical-report.md, §IV.c).

The author expects positive results "because the poloidal system didn't evidence stability issues in the past experiments," but those past experiments operated at much lower field and temperature (0.1-0.3 T, no fusion-relevant conditions).

### Dipole Coil and External Coil Set — TRL 4-5

**Demonstrated**: Dipole coils (levitated or mechanically supported) have been used in multiple past experiments (LDX at MIT, earlier poloidal experiments). Water-cooled copper coils at modest field (0.2-0.3 T) are well-established technology.

**On paper only**: Superconducting magnets for reactor-scale operation (2-3 T, steady-state) have been mentioned (deutelio-company-profile.md, §Development Roadmap) but not specified (HTS vs LTS, conductor type, current density, structural support under magnetic loads in the tunnel-penetrated geometry).

**Missing at scale**: Integration of superconducting coils with the magnetic tunnel geometry in a neutron environment. The discontinuous azimuthal structure creates unique coil support and stress management requirements.

### Vacuum Vessel and Structural Materials — TRL 6-7

**Demonstrated**: The small prototype uses "304LN stainless steel, 400 kg" vacuum vessel (jtsp-2024-polomac-technical-report.md, Table 1). Conventional vacuum technology.

**Missing at scale**: Reactor-scale vessel must handle neutron activation, magnetic tunnel penetrations, and thermal loads. The 2024 report notes "The first fusion reactor...will need a thick radiation shield" (jtsp-2024-polomac-technical-report.md, §VII). Shielding requirements for 2.45 MeV neutrons (D-D) or 14.1 MeV neutrons (D-T) have not been analyzed.

### Balance of Plant / Power Conversion — TRL 6-8

**Demonstrated**: The development roadmap targets "low temperature 150-200°C heat generation unit for industrial applications" initially, then "higher temperature 350°C" for electricity production (jtsp-2024-polomac-technical-report.md, §VII).

**Missing at scale**: No specific power cycle (Rankine, sCO2, etc.) or thermal efficiency has been disclosed. The low initial temperature target (150-200°C) suggests thermal conversion efficiency would be poor (<20%), requiring very large thermal output to produce meaningful net electric power.

## Section 4: Key Materials and Supply Chain Considerations

### Tritium (if D-T pathway)

If Polomac pursues D-T operation, standard tritium supply constraints apply. The global civilian tritium inventory is ~25 kg, produced primarily as a byproduct of CANDU reactors. A single D-T startup requires ~1 kg. The concept aims to avoid this entirely by using D-D fuel, but that pathway is far more challenging (142× Lawson criterion).

### Copper (Small Prototype)

The small prototype uses "Water-cooled copper conductors, 960 m total length, 2500 A maximum current" (jtsp-2024-polomac-technical-report.md, Table 1). Copper is a commodity material with no supply chain constraints at prototype scale.

### Superconducting Materials (Reactor Scale)

The development roadmap mentions transition to "superconducting magnets" (deutelio-company-profile.md, §Development Roadmap), but no conductor type (HTS REBCO, LTS NbTi/Nb3Sn) is specified. If HTS at 2-3 T, REBCO supply chain would be relevant:

Global REBCO production capacity is currently on the order of thousands of kilometers per year. A tokamak-class reactor requires ~5,000+ km. However, Polomac's lower magnetic field target (2-3 T vs 12-20 T for compact tokamaks) may allow use of less costly LTS technology or smaller quantities of HTS.

### Structural Materials (Reactor Scale)

The 2024 report notes:

> "Plasma physics and technical components are conventional"
> — jtsp-2024-polomac-technical-report.md, §III

This suggests standard materials (stainless steels, RAFM steels if neutron environment requires). No exotic materials are claimed. However, the magnetic tunnel penetrations create non-standard structural loading conditions.

### Beryllium (If Solid Breeder Blanket)

If a D-T blanket with beryllium neutron multiplier is used, beryllium supply constraints apply. Beryllium is toxic, expensive (~$800/kg), and global production is ~300 tonnes/year (dominated by Materion Corp). No blanket design exists for Polomac, so beryllium requirement is unknown.

### Lithium / Lithium-6 Enrichment (If D-T Blanket)

If D-T operation with FLiBe or lithium-based blanket, lithium-6 enrichment is required for tritium breeding. Only a few suppliers produce 90+% Li-6 at small scale (Russia, China, ORNL). This is a shared constraint across all D-T concepts.

The D-D fuel pathway (if achievable) avoids this supply chain entirely, which is one of the concept's claimed advantages.

## Section 5: Design Point Parameters

**(No design-point row for this concept yet — selection is upstream-pending.)**

Because no specific named plant with defined net-electric output has been identified upstream, the parameters below are extracted from the 2024 JTSP technical report's reactor-scale projections. These are conceptual target conditions, not a validated design point.

Two pathways are described in the sources: D-T and D-D. The D-T pathway is presented below as it is nearer-term achievable. The D-D pathway parameters are noted where they diverge.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Confinement Concept** | Poloidal (levitated dipole variant with magnetic tunnel supports) | jtsp-2024-polomac-technical-report.md §Abstract | high | Proprietary name "PoloMac." Magnetic tunnels are shaped field-line channels allowing physical support of internal dipole without plasma contamination. |
| **Fuel** | D-T (baseline) or D-D (aspirational) | jtsp-2024-polomac-technical-report.md §V, §VI | high | D-D is stated goal to avoid tritium breeding; D-T is more achievable near-term pathway. |
| **B (on-axis magnetic field)** | 2-3 T (D-T) | jtsp-2024-polomac-technical-report.md §V | medium | Stated as "half magnetic field" compared to ITER's 5.3 T. Claimed advantage: lower field enables lower-cost magnets. D-D operation field not explicitly stated. |
| **Plasma density** | 10²⁰ m⁻³ (D-T) <br> ~10²¹ m⁻³ (D-D) | jtsp-2024-polomac-technical-report.md §V, §VI | medium | D-T density comparable to tokamaks. D-D requires 10× higher density. |
| **Ion temperature** | 8.1 keV (D-T) <br> 100-200 keV (D-D) | jtsp-2024-polomac-technical-report.md §V, §VI | medium | D-T temperature standard for fusion. D-D requires extreme temperature with no clear heating pathway. |
| **Energy confinement time** | 4-5 s (D-T) <br> 20-40 s (D-D) | jtsp-2024-polomac-technical-report.md §V, §VI | low | Claimed comparable to ITER for D-T. D-D requires 4-8× longer confinement. No experimental basis for either claim. |
| **Beta (plasma pressure / magnetic pressure)** | 20-30% | elio-2014-fed-poloidal-confinement.md §Introduction | medium | Stated as "The best performances of the poloidal configurations with in-vessel rings of any type" from past dipole experiments. High beta is key advantage enabling lower magnetic field. |
| **Plasma volume** | 1300 m³ (2014 design) | elio-2014-fed-poloidal-confinement.md §Coil support and supply | low | From 2014 conceptual study. No updated reactor-scale plasma volume in 2024 report. This is much larger than compact tokamaks (e.g., ARC ~60 m³). |
| **Operation mode** | Steady-state | jtsp-2024-polomac-technical-report.md §Abstract | high | Stated explicitly: "steady state rather than pulsed" |
| **Heating method (reactor scale)** | Unknown | Not disclosed in sources | low | Small prototype uses 5-10 kW ECRH at 4 GHz. Reactor-scale heating method not specified. Critical gap for D-D (100-200 keV). |
| **Net electric output** | Unknown | Not disclosed in sources | low | No P_native stated. Development roadmap mentions "150-200°C heat generation" initially, then "350°C" for electricity, but no power level specified. |
| **Fusion power** | Unknown | Not disclosed in sources | low | Cannot be inferred without plasma volume, confinement time, and validated performance. |
| **Q_eng** | Unknown | Not disclosed in sources | low | Coil power consumption was 700 MW for 1300 m³ plasma in 2014 copper-coil design (excessive for steady operation). Superconducting coils would reduce this dramatically, but recirculating power not analyzed. |
| **Thermal conversion target** | 150-200°C (Phase 1) <br> 350°C (Phase 2) | jtsp-2024-polomac-technical-report.md §VII | medium | Low temperature implies poor thermal efficiency (<20%). Higher temp for electricity generation not tied to specific cycle (Rankine, sCO2, etc.). |

**Key Inferences and Gaps:**

1. **No specific "plant name" or P_native**: The sources describe conceptual reactor conditions but no named design (e.g., "Polomac-1 at 500 MWe"). Section 5 parameters are extrapolated from physics targets, not an engineered design point.

2. **D-T vs D-D bifurcation**: The D-D pathway is stated as the goal but is 142× more challenging than D-T by Lawson criterion. A realistic near-term design point would be D-T, but that eliminates the claimed advantage of avoiding tritium breeding blankets.

3. **Magnet cost advantage claim unvalidated**: Lower magnetic field (2-3 T vs 5.3 T for ITER, or 12-20 T for HTS compact tokamaks) would reduce magnet costs, but only if the claimed "higher confinement efficiency of the poloidal configuration" (jtsp-2024-polomac-technical-report.md §V) is real. This has no experimental validation.

4. **Power balance unknown**: The 2014 design had excessive coil power consumption (700 MW). Transition to superconductors would reduce this, but no Q_eng, recirculating power fraction, or net electric output analysis exists.

5. **Large plasma volume concern**: 1300 m³ plasma volume (2014 design) is very large compared to compact tokamaks. Large volume generally implies large capital cost (vacuum vessel, blanket, shielding, building). The concept's economic advantage over tokamaks is unclear without detailed cost modeling.

## Section 5b: Override Candidates

**(No 1costingFE archetype mapping for this concept — the canonical account schema does not apply. Do not propose account-coded overrides.)**

Because no archetype mapping has been established upstream, the per-account override walkthrough cannot be performed. If an archetype is assigned in the future (likely MFE-mirror or MFE-dipole, depending on how the library classifies poloidal confinement), the following concept-specific features would justify investigation for potential overrides:

1. **Lower magnetic field (2-3 T vs 5+ T tokamaks)**: If validated, this would reduce CAS22 (magnets) costs. However, the larger plasma volume may offset this advantage through increased vessel, blanket, and building costs (CAS21, CAS26).

2. **Magnetic tunnel structural supports**: The discontinuous azimuthal geometry with field-line "breaches" creates non-standard structural loading. CAS21 (structures and site facilities) may differ from standard dipole or mirror assumptions.

3. **D-D fuel cycle (if pursued)**: Eliminates blanket breeding requirements (CAS23 tritium systems, CAS26 blanket module costs), but at the cost of dramatically more challenging plasma performance. The tradeoff is unclear without validated physics.

4. **High beta (20-30%)**: If achievable, high beta enables more compact plasma volume for given power, potentially reducing capital costs across multiple accounts. However, the 2014 design had 1300 m³ plasma volume, which is not compact.

5. **Steady-state operation**: Avoids pulsed magnet stress and cyclic thermal loads, potentially reducing maintenance costs (CAS27) relative to pulsed concepts. However, steady-state heating power requirements may increase CAS24 (heating and current drive) costs.

Without a canonical account schema and without validated performance data, no specific override values can be proposed. The concept is too immature for accountable cost modeling.

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Experimental validation of magnetic tunnel concept (particle loss rates, confinement degradation, stability) | S1, S2, S3 | truly-unknown | blocking | Small prototype construction and operation; publish experimental results. PSI contracted particle-path analysis (in progress) is first step. |
| 2 | Reactor-scale heating method (especially for D-D at 100-200 keV) | S2, S3, S5 | proprietary or truly-unknown | blocking | Company disclosure or future technical publications. D-D heating at 100-200 keV is not demonstrated by any concept. |
| 3 | Net electric power target (P_native) and Q_eng for any design point | S2, S5 | proprietary or not-yet-decided | blocking | Company disclosure or power plant study. Cannot perform LCOE modeling without this. |
| 4 | Blanket design and tritium breeding ratio (if D-T pathway) | S3, S5 | not-yet-sourced or proprietary | important | Future publications. Standard D-T blanket literature may be partially applicable, but poloidal geometry with magnetic tunnel penetrations is unique. |
| 5 | Superconducting magnet specification (HTS vs LTS, conductor type, current density) | S3, S4, S5 | proprietary or not-yet-decided | important | Company disclosure. Magnet cost estimate depends on this. |
| 6 | Validated MHD code benchmarks and stability analysis results | S2, S3 | truly-unknown | important | MHD code validation publication; stability analysis publication. Contracted to plasma specialists per 2024 JTSP report. |
| 7 | Plasma volume, aspect ratio, and geometric parameters for reactor design point | S5 | proprietary or not-yet-decided | important | Engineering design study or company disclosure. 1300 m³ from 2014 paper is preliminary. |
| 8 | Thermal conversion cycle (Rankine, sCO2, efficiency target) | S3, S5 | not-yet-decided or proprietary | nice-to-have | Standard for D-T concepts; can be assumed from literature if not disclosed. Low initial temp (150-200°C) suggests poor efficiency. |
| 9 | Shielding requirements and neutron streaming analysis through magnetic tunnels | S3, S4 | truly-unknown | important | Neutronics analysis of tunnel geometry; shielding design study. Tunnels may create neutron streaming paths not present in closed-field-line MFE. |
| 10 | Capital cost estimate or LCOE projection for any design point | S1, S2 | proprietary or not-yet-sourced | important | Company disclosure, independent TEA study, or detailed engineering design. No cost data exists. |
| 11 | Development timeline and funding to support prototype construction | S1 | proprietary | nice-to-have | Company disclosure. Timeline states "1 year" for small prototype construction, "2-3 years" experimental campaign, but no funding announcement beyond seed round. |

**Summary**: Gaps 1-4 are blocking for any credible LCOE assessment. Until the magnetic tunnel concept is experimentally validated (Gap 1), all downstream analysis is speculative. Gaps 2-3 (heating method, power target) are required inputs for any cost model. Gap 4 (blanket) is critical if D-T pathway is pursued.

## Section 7: Family-Delta vs Comparables

**(No comparable concept in the corpus for this design point.)**

Because no comparables have been identified upstream, the family-delta analysis cannot be performed in the standard format. However, the following observations can be made about Polomac's positioning relative to broader MFE families:

### Versus Standard Tokamaks

**Claimed advantages**:
1. **Lower magnetic field**: "The poloidal confinement can achieve Deuterium-Tritium reactor conditions with a magnetic field 3 times weaker than the Tokamak" (jtsp-2024-polomac-technical-report.md, Abstract). This would reduce magnet capital cost (CAS22) if validated.
2. **Steady-state by design**: No pulsed operation, avoiding disruption risk and cyclic stresses. Most tokamaks require advanced scenarios or external current drive for steady-state.
3. **Simpler than stellarators**: "The PoloMac results from a wish of something simpler than stellarators and with less operation constraints than Tokamaks" (elio-2014-fed-poloidal-confinement.md, §Discussion).
4. **High beta (20-30%)**: Enables higher plasma pressure at lower field, potentially allowing more compact design for given power.

**Penalties**:
1. **Unproven confinement**: Tokamak confinement is validated across dozens of machines. Poloidal confinement with magnetic tunnels has zero experimental demonstration.
2. **Particle losses through tunnels**: Creates a loss channel not present in closed-flux-surface tokamaks. Loss rate is unquantified.
3. **Large plasma volume**: 1300 m³ (2014 design) is much larger than HTS compact tokamaks (ARC ~60 m³). Large volume generally means high capital cost.
4. **No heating strategy**: D-D operation at 100-200 keV has no demonstrated heating pathway. Even D-T at 8.1 keV in a poloidal geometry is untested.

### Versus HTS Compact Tokamaks (e.g., CFS ARC, Tokamak Energy)

**Claimed advantages**:
1. **Lower field**: 2-3 T vs 12-20 T for HTS compact tokamaks. Dramatically reduces magnet cost if performance claims hold.
2. **No disruption risk**: Poloidal geometry may be inherently disruption-free (past experiments showed no stability issues at low parameters).

**Penalties**:
1. **Unproven physics**: HTS compact tokamaks leverage 40 years of tokamak physics validation. Polomac physics is extrapolated from low-field experiments that failed due to support-wire issues.
2. **Technology maturity**: HTS compact tokamaks are building/testing hardware (CFS SPARC prototype magnet tested at 20 T, Jan 2026). Polomac has no prototype yet.
3. **Likely larger size**: Even with high beta, the 1300 m³ plasma volume suggests a large device. HTS compact tokamaks achieve high power density in small volume via high field.

### Versus Magnetic Mirrors (e.g., Realta, Terra Fusion)

**Claimed advantages**:
1. **Closed-flux-surface confinement**: Unlike open-ended mirrors, poloidal dipole has closed field lines except at magnetic tunnel locations. This should reduce axial losses compared to mirror loss cone.
2. **No end-plugging required**: Mirrors require tandem plugs, centrifugal barriers, or ponderomotive barriers to reduce axial losses. Polomac's closed-field geometry avoids this complexity.

**Penalties**:
1. **Magnetic tunnels create intentional openings**: The cost of mechanical support is field-line breaches that may act like loss channels. Mirrors accept axial losses by design and optimize end-plugs; Polomac creates losses via structural necessity.
2. **Modularity**: Mirrors have inherently modular geometry (long cylindrical chambers). Poloidal dipole is a single integrated device with complex 3D geometry, likely harder to manufacture and maintain.

### Versus Levitated Dipole (e.g., LDX at MIT)

**Claimed advantages**:
1. **Mechanical support eliminates levitation system**: LDX required a superconducting levitation coil and cryogenic system to float the internal dipole. Polomac uses direct mechanical support through magnetic tunnels, eliminating levitation complexity and power requirements.

**Penalties**:
1. **Particle losses through support structure**: LDX avoided plasma-support interaction by levitating the coil. Polomac reintroduces physical penetrations (albeit in field-free "tunnels"), which may degrade confinement.

### Cost Implications Summary

**Cost advantages (if physics works)**:
- Lower magnetic field → lower CAS22 (magnets)
- No tritium blanket if D-D succeeds → eliminates CAS26 (blanket) and CAS23 (tritium systems)
- Steady-state → lower CAS27 (maintenance) via reduced cyclic stress

**Cost penalties (or neutral)**:
- Large plasma volume → higher CAS21 (structures), CAS26 (if D-T blanket), CAS28 (building)
- Unknown heating → CAS24 (heating systems) could be higher for D-D extreme temperatures
- First-of-a-kind → high development cost and schedule risk not captured in NOAK LCOE

The net cost position relative to tokamaks is indeterminate without validated performance and engineering design.

## Section 8: Sources

Listed in order of importance:

1. **jtsp-2024-polomac-technical-report.md** — "The PoloMac Magnetic Confinement" by F. Elio et al. (Journal of Technical and Scientific Publications, 2024). Primary technical source. Describes small prototype specifications, reactor-scale projections for D-T and D-D pathways, magnetic tunnel concept, MHD code development status, and stability analysis plans. Provides quantitative parameters for magnetic field, density, temperature, confinement time, and beta. Cites contracted analysis to Paul Scherrer Institute for particle path validation. Most complete source for Polomac concept as of 2024.

2. **elio-2014-fed-poloidal-confinement.md** — "Poloidal magnetic confinement with magnetic tunnels" by F. Elio (Fusion Engineering and Design, 2014). Foundational paper introducing the magnetic tunnel concept. Describes the historical context (past poloidal confinement experiments failed due to support-wire losses), the magnetic tunnel solution, conceptual reactor design with 1300 m³ plasma volume, and power consumption issue (700 MW for copper coils). Notes need for further MHD, confinement, stability, and engineering analysis. Explicitly stated as independent voluntary work unaffiliated with European Commission or official fusion policy.

3. **deutelio-company-profile.md** — High-level company information for Deutelio (Luxembourg). Provides development roadmap (hydrogen plasma prototype → heat generation → electricity generation), timeline aspiration ("Energy generation by 2030"), team background (F. Elio - RFX, ITER, W7-X experience), and business milestones (seed funding, Boldbrain 4th place, 2024). Contains no technical specifications, cost data, or quantitative performance targets. Useful for company maturity assessment but not for LCOE modeling.

4. **jtsp-jtsp-article-download-32-28.md** (0 KB file) — Empty or unavailable source file. Not used in analysis.

**External references cited in sources but not available**:
- Paul Scherrer Institute contracted particle-path analysis (in progress as of 2024 report)
- MHD code benchmarking studies (planned but not yet published)
- Stability analysis by plasma specialists (contracted but not yet completed)

**Recommended additional sources** (not available):
- Independent techno-economic analysis of poloidal confinement
- Experimental results from small prototype (not yet built)
- Blanket and shielding design studies for poloidal geometry
- Comparative cost modeling: Polomac vs tokamak vs mirror