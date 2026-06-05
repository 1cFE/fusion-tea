## Design Point

- Name: ST-E1 Revision D, technology-conservative case (Maartensson et al., DPP 2025)
- Maturity: paper-concept
- P_native: 450 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md
  - knowledge/concept_research/21-spherical-tokamak-hts/iter-02/sources/tokamak-energy-st-e1-design-evolution.md
  - knowledge/concept_research/21-spherical-tokamak-hts/iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md

## Section 1: Availability of Data

**Rating: Limited**

The publicly available information on the ST-E1 Revision D design point is thin compared to other tokamak concepts. The primary source is a conference abstract from the 67th APS Division of Plasma Physics meeting (Maartensson et al., DPP 2025), which provides only three machine parameters (R0, A, B0), a net electric power range, blanket type, and TBR.[^1] No full journal paper on the ST-E1 Revision D design has been published.

Supporting sources fall into three categories:

1. **Peer-reviewed physics papers**: Gryaznevich, Chuyanov & Takase (2022) present the pulsed spherical tokamak reactor concept with a reference design point "ST280-5T" (R0 = 2.8 m, A = 1.9, Bt = 5 T) that is an earlier, smaller configuration — not ST-E1 Revision D.[^2] Humphry-Baker & Smith (2019) provide a detailed materials study of WC cermet center-stack shielding for a 185 MW pilot plant (R0 = 1.35 m), again a different, smaller machine.[^3]

2. **Conference contributions and journal abstracts**: Alieva et al. (EPJ Web of Conferences, 2026) confirm that EC waves are the sole flat-top auxiliary heating and current drive source, but only the abstract was extracted — no power levels, frequencies, or system sizing are available.[^4]

3. **Company press releases and news articles**: Demo4 HTS magnet milestone (11.8 T, 14 TF + 2 PF, Nov 2025),[^5] ST80-HTS announcement (2022), gyrotron delivery (1 MW, Kyoto Fusioneering, late 2024),[^6] and roadmap statements. These provide milestones but no engineering design data for ST-E1.

> "The final pre-conceptual design point, ST-E1 revision D, is a 5.0m major radius, aspect ratio of 2.3 and on-axis toroidal field of 5.25 T machine with a net power electric output of 450-750MW, depending on technology and physics assumptions."
> — tokamak-energy-st-e1-dpp2025-abstract.md, §Abstract

**Key data gaps**: No published values for plasma current (Ip), elongation (κ), triangularity (δ), beta, Q, fusion power, or auxiliary heating power for the Revision D design point. No cost data, no capital cost breakdown, no LCOE estimate. The energy conversion pathway (steam vs. sCO2) is undisclosed. The design maturity is explicitly labeled "pre-conceptual," and the wide power output range (450–750 MWe) reflects unresolved physics and technology assumptions.

**Independent analyses**: The UKAEA PROCESS code has published spherical tokamak models, and academic papers (Hidalgo-Salaverri et al. 2025, Foster et al. 2024) provide ST TEA frameworks, but none are calibrated to ST-E1 Revision D specifically.

[^1]: tokamak-energy-st-e1-dpp2025-abstract.md §Abstract
[^2]: pulsed-spherical-tokamak-paper.md §2.2, §3
[^3]: spherical-tokamak-center-stack-shielding.md §1(a)
[^4]: tokamak-energy-ec-heating-pilot-plant.md §Abstract
[^5]: tokamak-energy-demo4-magnets.md
[^6]: st40-heating-systems.md

## Section 2: Challenges in Capturing System Function

The following challenges are ranked by their impact on LCOE modeling uncertainty, from most to least severe.

### 1. Missing core plasma performance parameters (blocking)

The DPP 2025 abstract does not state plasma current, elongation, beta, Q, or fusion power for ST-E1 Revision D. Without Q and fusion power, the recirculating power fraction and net electric output cannot be independently verified. The stated net electric range of 450–750 MWe represents a 1.67× spread — larger than many fusion concepts publish — and reflects genuine uncertainty in both physics performance and balance-of-plant assumptions. For the 1costingFE model, we must adopt the lower bound (450 MWe) as P_native and infer or estimate the missing parameters from the published geometry, published physics papers, and ST scaling relationships.

### 2. Center-stack shielding lifetime (high uncertainty)

The spherical tokamak's compact center stack leaves only ~32 cm for neutron shielding in the reference geometry studied by Humphry-Baker & Smith (2019). Their analysis found that with a WC shield, the fast neutron flux reaching the HTS core would be ~1.4 × 10^17 s⁻¹ m⁻², corresponding to an HTS tape degradation threshold of ~40 hours of continuous operation — though the authors explicitly state "the accuracy of this prediction is questionable" because all irradiation data used fission-spectrum neutrons, not 14.1 MeV fusion neutrons.[^7] The ST-E1 Revision D is substantially larger (R0 = 5.0 m vs. 1.35 m), which should provide more radial space for shielding, but no published shielding analysis exists for the Revision D geometry. This is a critical LCOE driver because HTS tape replacement frequency directly affects availability and O&M costs.

> "We note that this neutron fluence would correspond to approximately 40 h of continuous operation for a 32 cm WC shield… However, the accuracy of this prediction is questionable, as all the studies were performed using fission reactor neutron sources."
> — spherical-tokamak-center-stack-shielding.md §1(a)

### 3. Pulsed operation and capacity factor

ST-E1 is designed for quasi-steady operation with 15+ minute burn pulses, with inter-pulse gaps for central solenoid recharging.[^8] This is a deliberate design choice — the pulsed-ST paper argues pulsed operation is "more desirable than steady-state" for spherical tokamaks due to limited CS space.[^9] However, the duty cycle (burn time / total cycle time) is unpublished. With ~20 MW of RF power consumed during CS recharging and an unknown recharging duration, the effective capacity factor could range from 70% to 90%. Thermal energy storage during inter-pulse gaps adds capital cost not present in steady-state concepts.

### 4. Outboard-only blanket coverage

The spherical tokamak geometry forces an outboard-only blanket because the compact center stack cannot accommodate a breeding blanket on the inboard side. The claimed TBR of 1.2 is thin margin for a D-T reactor (most designs target TBR ≥ 1.1 as minimum for self-sufficiency). This constraint is unique to the spherical tokamak and represents both a cost advantage (less blanket material) and a risk (marginal tritium self-sufficiency).

### 5. Energy conversion pathway undisclosed

After three research iterations, the thermal cycle (steam Rankine vs. sCO2 Brayton) has not been specified. This affects thermal efficiency (η_th ~33% for Rankine vs. ~40% for sCO2), which propagates into the required fusion power for a given net electric output.

[^7]: spherical-tokamak-center-stack-shielding.md §1(a)
[^8]: tokamak-energy-roadmap.md (ST80-HTS targets 15-minute pulses)
[^9]: pulsed-spherical-tokamak-paper.md §Introduction

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Center-Stack Neutron Shielding, TRL ~2–3

- **On paper only**: WC-FeCr cermet shielding concept developed by Humphry-Baker & Smith (2019) with detailed materials characterization (thermal conductivity, fracture toughness, oxidation resistance, transmutation products). Shield optimization via simulation (Windsor et al.) for a 185 MW pilot plant. Si-impregnation coating demonstrated to improve oxidation resistance by 1000×.
- **Missing at scale**: No WC-FeCr cermet shield has been fabricated at reactor-relevant dimensions. No irradiation testing of WC-FeCr with 14.1 MeV fusion neutrons. The HTS tape radiation tolerance under fusion-spectrum neutrons at cryogenic operating temperatures is unknown — all existing data uses fission-spectrum neutrons at above-room-temperature conditions.[^10] Carbon control during WC-FeCr manufacturing requires tighter process windows than established WC-Co production.

### Tritium Fuel Cycle & Breeding Blanket, TRL ~3

- **On paper only**: Outboard-only liquid lithium blanket design with TBR = 1.2. Liquid lithium wall testing on ST40 is planned via the DOE/DESNZ $52M collaboration.[^11]
- **Missing at scale**: No prototype liquid lithium blanket tested in a spherical tokamak geometry. Outboard-only coverage is a constraint unique to the ST that has not been validated for tritium self-sufficiency. Tritium extraction from liquid lithium at plant scale is undemonstrated.

### Remote Maintenance System, TRL ~3–4

- **Demonstrated**: The DPP 2025 abstract states that the maintenance scheme "was considered very early on and is shown to be compatible with reactor-level performance and availability factor."[^12] However, no details of the maintenance approach are published.
- **Missing at scale**: The spherical tokamak's tight geometry and compact center stack create unique maintenance challenges. Remote handling in the confined inboard region is more demanding than in conventional tokamaks. No prototype maintenance system exists for any spherical tokamak power plant.

### Divertor, TRL ~4–5

- **Demonstrated**: Conventional and super-X divertor concepts studied on MAST-U (UKAEA). Tungsten monoblock divertor technology demonstrated at relevant heat fluxes on multiple tokamaks.
- **Missing at scale**: Divertor power loading in the ST geometry — with its compact lower divertor region — is a known challenge flagged in the foundational literature.[^13] No ST-specific divertor has been tested at power-plant-relevant heat loads.

### HTS Magnets, TRL ~5–6

- **Demonstrated**: Demo4 (Nov 2025) achieved 11.8 T with a complete 14 TF + 2 PF HTS coil set in tokamak configuration — a world-first for a system-level HTS magnet demonstration.[^14] This goes beyond CFS's single-coil 20 T demonstration (2021) by validating coil-to-coil electromagnetic interactions. The system operated at 30 K with 7 million ampere-turns.
- **Missing at scale**: Demo4 is small-scale compared to ST-E1 (R0 = 5.0 m). Scaling HTS coil production to the km-scale tape quantities needed for a pilot plant, radiation-hardened insulation, quench protection under neutron environments, and long-term fatigue under cyclic mechanical loads are all undemonstrated. No published data on REBCO tape quantity or cost for ST-E1.

### Heating & Current Drive (ECRH), TRL ~5–6

- **Demonstrated**: 1 MW gyrotron (104/137 GHz) from Kyoto Fusioneering delivered to ST40 in late 2024.[^15] ECRH and ECCD demonstrated on multiple tokamaks worldwide. Ray-tracing simulations confirm EC waves in O-mode can drive current throughout the plasma volume for the FPP flat-top phase.[^16]
- **Missing at scale**: Total heating power requirement for ST-E1 is unpublished. Scaling from 1 MW to the likely tens-of-MW requirement for a 450 MWe plant requires multiple gyrotrons in a coordinated system. Wall-plug efficiency of gyrotrons (~30–50%) affects recirculating power.

### Balance of Plant, TRL ~8–9

- **Demonstrated**: Thermal power conversion via steam or sCO2 cycles is mature technology from fission and fossil plants.
- **Missing at scale**: Integration with the pulsed thermal source and inter-pulse thermal buffering requirements. The specific thermal cycle for ST-E1 has not been selected.

[^10]: spherical-tokamak-center-stack-shielding.md §1(a), §1(b)
[^11]: st40-heating-systems.md
[^12]: tokamak-energy-st-e1-dpp2025-abstract.md §Abstract
[^13]: pulsed-spherical-tokamak-paper.md §1
[^14]: tokamak-energy-demo4-magnets.md
[^15]: st40-heating-systems.md
[^16]: tokamak-energy-ec-heating-pilot-plant.md §Abstract

## Section 4: Key Materials and Supply Chain Considerations

### REBCO Superconducting Tape

HTS REBCO tape is the enabling technology for the entire concept. Demo4 demonstrated a complete magnet system but no tape quantities or costs are published for either Demo4 or the planned ST-E1. Global REBCO production capacity is on the order of thousands of km/year, while a single ARC-class reactor (R0 ~ 3.3 m) requires >5,000 km. ST-E1 (R0 = 5.0 m, but lower on-axis field of 5.25 T vs. ARC's ~12 T) would require substantial but unquantified tape. The lower field requirement is a partial relief — lower field means less conductor per coil — but the larger major radius partly offsets this.

Key REBCO suppliers include Shanghai Superconductor Technology, Faraday Factory Japan, SuperOx, and THEVA. CFS is building its own production capability. Tokamak Energy's REBCO supply chain is not publicly disclosed. Current tape prices are in the range of $30–100/kA-m; commercial fusion viability likely requires ~$10/kA-m.

### Tungsten Carbide Cermet Shielding

WC cermet (with FeCr binder, replacing the standard Co binder excluded by neutron activation concerns) is a novel material for fusion applications. The standard WC-Co industry is well-established for machine tools and mining, but WC-FeCr requires tighter carbon control, has slower densification kinetics, and needs additional Si-impregnation for oxidation resistance.[^17] The raw materials (W, C, Fe, Cr, Si) are all industrially abundant and low-activation. The manufacturing process (pressureless sintering at ~1400°C) is less demanding than hot-pressing, but achieving >97% density is critical for neutron attenuation and has only been demonstrated via spark-plasma sintering (a batch process difficult to scale).

No WC-FeCr components have been manufactured at the dimensions required for a tokamak center stack. The supply chain for this material does not exist at fusion-relevant scale.

### Tritium

Standard D-T concern. Global civilian tritium inventory is ~25 kg, decaying at 5.5%/year. Startup inventory of ~1 kg is required. The outboard-only blanket with TBR = 1.2 provides thin margin for self-sufficiency. Tritium cost is >$30,000/g.

### Liquid Lithium (Blanket)

Liquid lithium is the breeder/coolant for the outboard blanket. Lithium is industrially available (shared supply chain with the battery industry), but liquid lithium handling in a fusion reactor environment is challenging — lithium is highly reactive, requiring inert atmosphere handling and fire-safety engineering. Lithium-6 enrichment for breeding enhancement is commercially available but not at fleet-scale volumes.

[^17]: spherical-tokamak-center-stack-shielding.md §3(a), §3(b)

## Section 5: Design Point Parameters

All parameters describe the ST-E1 Revision D at its native scale (450 MWe). Parameters not published for this design point are flagged with confidence tags and derivation chains.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 5.0 m | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract | high | spec key: `R0` |
| a (minor radius) | 2.17 m | [inferred: R0/A = 5.0/2.3] | medium | spec key: `plasma_t` |
| A (aspect ratio) | 2.3 | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract | high | informational — library derives a from R0/A |
| elongation (κ) | 2.8 | [estimated: typical ST value; MAST-U operates at κ~2.5–3.0; pulsed-ST paper cites κ=3 for STEP simulation device] | low | spec key: `elon` |
| B0 (on-axis field) | 5.25 T | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract | high | spec key: `B` |
| B_peak (on conductor) | ~11.8 T | [analogue: Demo4 achieved 11.8 T at coil; ST-E1 field ratio ~2.2× on-axis consistent with low-A geometry] | medium | informational only |
| Ip (plasma current) | ~14 MA | [estimated: from ST scaling; ARIES-ST at A=1.6 has Ip~29 MA; scaling to A=2.3, B=5.25 T suggests 12–16 MA range; no published value] | low | informational — not a spec key |
| fusion_power_MW | ~1500 MW | [estimated: for 450 MWe net at η_th~0.35, η_aux~0.10 recirculating fraction, Pfus~1400–1600 MW; pulsed-ST paper ref design gives 800 MW at R0=2.8 m, scaling as R0³×B⁴/A⁴ gives ~1500 MW at R0=5.0 m; no published value] | low | informational only — library back-solves from P_native + p_input |
| net_electric_MWe | 450 MWe | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract (lower bound of 450–750 MW range) | high | spec key: `P_native` |
| p_input_MW | ~50 MW | [estimated: pulsed-ST paper states ~20 MW RF for CS recharging; additional ECRH for current drive and heating during flat-top; total wallplug auxiliary ~40–60 MW; no published value] | low | spec key: `p_input` |
| TBR | 1.2 | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract | high | informational |
| blanket coverage | outboard-only | tokamak-energy-st-e1-dpp2025-abstract.md §Abstract | high | informational — cost-relevant: reduces blanket mass but limits TBR |
| operation mode | quasi-steady (~15+ min pulses) | tokamak-energy-roadmap.md; pulsed-spherical-tokamak-paper.md §2.2 | high | informational |
| bootstrap fraction | ~90% | pulsed-spherical-tokamak-paper.md §2.2 (for ST280-5T reference) | medium | informational — reduces CD power requirement |

**Note on inferred parameters**: The plasma current, fusion power, and auxiliary heating power are not published for ST-E1 Revision D. The estimates above are derived from published ST scaling relationships and the earlier ST280-5T reference design. These carry low confidence and should be treated as order-of-magnitude placeholders until Tokamak Energy publishes the full design point.

**Sensitivity coverage**: The two lowest-confidence spec inputs — `p_input` (50 MW, low confidence, range 40–60 MW) and `elon` (2.8, low confidence, range 2.5–3.0) — are swept individually in `model_setup.py` to bound the LCOE impact of the acknowledged parameter uncertainty. `plasma_t` (2.17 m, medium confidence) is a deterministic derivation from R0/A and is not independently swept.

## Section 5b: Override Candidates

### Per-Account Walkthrough

Each canonical account is evaluated against the dossier for company-grounded override evidence.

**C220101 — First wall, blanket & neutron multiplier**: The dossier confirms an outboard-only liquid lithium breeder blanket with TBR = 1.2. However, no cost data, mass estimates, or unit prices for the blanket are published. The outboard-only coverage reduces blanket mass relative to full-coverage designs, but no quantitative basis exists to price the difference vs. the library default. **No override proposed.**

**C220102 — Radiation shield**: The Humphry-Baker & Smith (2019) paper provides extensive materials characterization of WC-FeCr cermet shielding, but for a 185 MW pilot plant (R0 = 1.35 m), not for ST-E1 Revision D. No cost data for WC-FeCr fabrication at any scale is published. The asymmetric shielding architecture (WC cermet inboard, integrated blanket/shield outboard) is architecturally distinctive but uncosted. **No override proposed.**

**C220103 — Confinement magnets / coils**: Demo4 demonstrated 11.8 T with a 14 TF + 2 PF system, but no REBCO tape quantities, magnet masses, or cost figures are published for either Demo4 or ST-E1. The lower on-axis field (5.25 T vs. CFS's ~12 T) implies less conductor per coil, but the larger machine (R0 = 5.0 m) and the need for center-stack structural support offset this. Without published magnet cost or mass data, the library default stands. **No override proposed.**

**C220104 — Supplementary plasma heating**: The flat-top phase uses ECRH exclusively (Alieva et al. 2026), replacing the NBI + ECRH combination used on ST40. No heating power requirement (MW), number of gyrotrons, or system cost is published for ST-E1. **No override proposed.**

**C220105 — Primary structure**: No company data on structural mass, support design, or cost. **No override proposed.**

**C220106 — Vacuum system**: No company data. **No override proposed.**

**C220107 — Power supplies**: No company data on magnet power supply sizing or cost. The CS recharging system (~20 MW RF per the pulsed-ST paper) is a concept-specific power supply requirement, but no cost figure is published. **No override proposed.**

**C220108 — Divertor**: No company data on divertor design, heat flux handling, or cost for ST-E1. **No override proposed.**

**C220110 — Remote handling & maintenance**: The DPP 2025 abstract states the maintenance scheme was designed early and is "compatible with reactor-level performance and availability factor," but no specifics or cost data are published. **No override proposed.**

**C220111 — Reactor-equipment installation & assembly**: No company data. **No override proposed.**

**CAS21 — Buildings & site structures**: No company data. **No override proposed.**

**CAS23 — Turbine plant equipment**: D-T thermal cycle; turbine plant applies. No specific data. **No override proposed.**

**CAS24 — Electric plant equipment**: No company data. **No override proposed.**

**CAS26 — Heat rejection system**: No company data. **No override proposed.**

**CAS27 — Special materials**: The outboard-only liquid lithium blanket fill is a concept-specific material inventory. However, no lithium mass, volume, or cost is published for ST-E1. **No override proposed.**

**CAS70 — O&M + scheduled component replacement**: No company data on O&M costs, staffing, or replacement schedules. **No override proposed.**

**CAS80 — Annualized fuel cost**: Standard D-T fuel cycle. No concept-specific data. **No override proposed.**

### Override Count: 0 enabled overrides

The archetype-fit grade is High, with an expected band of 0–4 enabled overrides. The count of 0 falls within this band. This reflects the genuinely data-poor state of the ST-E1 Revision D design point: the dossier provides architectural descriptions and materials science characterization, but publishes no cost figures, mass estimates, or unit prices that would justify departing from library defaults for any account.

```yaml
overrides: []
```

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Plasma current (Ip) for ST-E1 Rev D | S5 | proprietary | blocking | Await Tokamak Energy publication of full design point or PROCESS code model |
| 2 | Fusion power (Pfus) for ST-E1 Rev D | S5 | proprietary | blocking | Same as #1 |
| 3 | Elongation (κ) for ST-E1 Rev D | S5 | proprietary | important | Same as #1; could be estimated from MAST-U/NSTX-U analogue |
| 4 | Plasma Q for ST-E1 Rev D | S5 | proprietary | blocking | Same as #1 |
| 5 | Auxiliary heating power requirement (MW) | S5 | proprietary | important | Await full EC heating paper (Alieva et al. 2026) or direct company disclosure |
| 6 | HTS tape radiation tolerance under fusion-spectrum neutrons at cryogenic temperatures | S3 | truly-unknown | blocking | Requires dedicated irradiation facility with 14.1 MeV neutrons (IFMIF-class) |
| 7 | Center-stack shielding thickness and design for ST-E1 Rev D geometry (R0 = 5.0 m) | S2, S3 | not-yet-sourced | important | Seek Windsor et al. or updated Tokamak Energy shielding publications |
| 8 | Thermal cycle selection (steam vs. sCO2) | S2 | proprietary | important | Await company disclosure |
| 9 | Duty cycle (burn time / total cycle time) for quasi-steady pulsed operation | S2 | proprietary | important | Needed to compute capacity factor; seek ST80-HTS operational data |
| 10 | REBCO tape quantity and cost for ST-E1 magnets | S4 | proprietary | important | Could be estimated from coil geometry if winding pack current density is published |
| 11 | Liquid lithium blanket mass and inventory cost | S4 | not-yet-sourced | nice-to-have | Derivable from blanket geometry and lithium density if coverage area is published |
| 12 | O&M cost breakdown (fixed vs. variable, maintenance schedule) | S1 | not-yet-sourced | important | No company data; use ARIES-ST or PROCESS analogues |

## Section 7: Family-Delta vs Comparables

### vs. 01-hts-compact-tokamak (CFS ARC-class)

The most natural comparison. Both are HTS-REBCO tokamaks targeting D-T operation, but with fundamentally different aspect ratios and field strategies.

**Geometry and field**: ST-E1 operates at A = 2.3 and B0 = 5.25 T; ARC operates at A ~3.3 and B0 ~12 T. The spherical tokamak trades high field for high beta — achieving confinement through plasma pressure rather than magnetic field strength. The pulsed-ST paper quantifies this via the C_MAG proxy (toroidal magnetic field energy per unit fusion power): C_MAG = 14 MJ/MW for the ST reference design vs. 33–37 MJ/MW for pulsed ARC, indicating the ST uses roughly half the magnet energy per unit of fusion power.[^18]

**Cost direction on C220103 (magnets)**: The lower on-axis field (5.25 T vs. ~12 T) reduces REBCO tape requirements per unit of ampere-meters. However, the larger machine (R0 = 5.0 m vs. ~3.3 m) increases total coil circumference. The net effect on magnet cost is uncertain — the C_MAG proxy suggests an advantage, but the proxy does not capture conductor unit cost or manufacturing complexity. **Direction: likely advantage, magnitude unknown.**

**Cost direction on C220102 (radiation shield)**: The compact center stack requires high-performance WC cermet shielding with tight engineering tolerances — a cost category that conventional-aspect-ratio tokamaks largely avoid because they have ample radial space for standard shielding materials. **Direction: penalty (novel, uncosted subsystem).**

**Cost direction on C220104 (heating)**: ST-E1 uses ECRH-only for flat-top, eliminating NBI. ARC uses ICRH and/or LHCD. ECRH gyrotrons are commercially available and can be positioned remotely from the device; NBI requires close proximity and complex high-voltage systems. **Direction: likely advantage (simpler, fewer components), magnitude unknown.**

**Cost direction on C220101 (blanket)**: Outboard-only coverage reduces blanket material relative to ARC's full-coverage design, but with marginal TBR (1.2). **Direction: advantage on material cost, risk on tritium self-sufficiency.**

**Cost direction on capacity factor**: ST-E1's quasi-steady pulsed operation (~15+ min pulses with recharging gaps) inherently reduces capacity factor relative to ARC's targeted steady-state operation. **Direction: penalty (likely 5–15% CF reduction).**

### vs. 28-hts-tokamak-full-hts (Energy Singularity)

Energy Singularity pursues a conventional-aspect-ratio tokamak with full HTS. The delta is essentially the same as vs. CFS ARC: lower field / higher beta / compact center stack for ST-E1, with the same trade-offs on magnets, shielding, and capacity factor.

### vs. 29-negative-triangularity-tokamak (Firefly Fusion)

Negative triangularity operates at conventional aspect ratio with shaped plasma geometry for improved confinement and ELM suppression. The delta vs. ST-E1:

- **Magnets**: Negative-delta uses conventional or moderate-field HTS; ST-E1's lower field but larger machine makes the comparison ambiguous.
- **Plasma-facing components**: Negative triangularity claims reduced divertor heat flux via broader SOL; ST-E1's compact divertor geometry faces higher localized loads. **Direction: penalty for ST-E1.**
- **Center-stack shielding**: Not applicable to negative-triangularity (conventional geometry). **Direction: unique penalty for ST-E1.**

### vs. 33-state-backed-tokamak-best (Neo Fusion / ASIPP-class)

State-backed tokamaks (CFETR-class) operate at conventional aspect ratio (A ~3.5–4) with LTS or hybrid magnets. The delta vs. ST-E1:

- **Magnets**: ST-E1's HTS at 5.25 T is less demanding per coil than CFETR's larger LTS magnets, but HTS conductor costs per kA-m are currently much higher than LTS (NbTi/Nb3Sn). **Direction: uncertain — lower field helps but higher conductor unit cost hurts.**
- **Scale**: State-backed designs target >1 GWe; ST-E1 at 450 MWe is smaller, which reduces absolute capital cost but increases specific cost ($/kWe) through loss of economies of scale. **Direction: penalty on specific capital cost.**
- **Center-stack shielding**: Same unique penalty as above.
- **Technology readiness**: CFETR-class builds on ITER heritage with LTS magnets (TRL 7–8); ST-E1's HTS system-level demonstration (Demo4, TRL 5–6) is less mature. **Direction: risk premium for ST-E1.**

[^18]: pulsed-spherical-tokamak-paper.md §3

## Section 8: Sources

1. **Maartensson, E. et al. (DPP 2025)** — "Overview of Tokamak Energy's Fusion Pilot Plant Program," 67th APS-DPP. Primary source for ST-E1 Revision D design point (R0, A, B0, net electric power, TBR). Found at: tokamak-energy-st-e1-dpp2025-abstract.md. Also duplicated in ste1-pilot-plant-specs.md.

2. **Gryaznevich, M., Chuyanov, V.A., Takase, Y. (2022)** — "Pulsed Spherical Tokamak — A New Approach to Fusion Reactors," Plasma 5, 247–257. Provides the physics case for pulsed ST operation, the C_MAG cost proxy, and the ST280-5T reference design. Found at: pulsed-spherical-tokamak-paper.md.

3. **Humphry-Baker, S.A. and Smith, G.D.W. (2019)** — "Shielding materials in the compact spherical tokamak," Phil. Trans. R. Soc. A. Detailed materials science review of WC cermet center-stack shielding — thermal properties, neutron attenuation, transmutation, manufacturing. Found at: spherical-tokamak-center-stack-shielding.md.

4. **Alieva, A. et al. (2026)** — "Progress in the pre-conceptual design of the auxiliary heating and current drive system for the Tokamak Energy Fusion Pilot Plant," EPJ Web of Conferences 346, 02014. Confirms EC-only flat-top heating/current drive. Only abstract extracted. Found at: tokamak-energy-ec-heating-pilot-plant.md.

5. **Tokamak Energy (2025)** — Demo4 HTS magnet press release. 11.8 T, 14 TF + 2 PF system at 30 K. Found at: tokamak-energy-demo4-magnets.md.

6. **Tokamak Energy (2025)** — ST40 gyrotron press release. 1 MW gyrotron from Kyoto Fusioneering, 104/137 GHz. $52M DOE/DESNZ collaboration for ST40 upgrades including liquid lithium wall testing. Found at: st40-heating-systems.md.

7. **ANS Nuclear News (2022)** — "Tokamak Energy bets its spherical design will deliver fusion energy in the early 2030s." Roadmap: ST40 → ST80-HTS (2026) → ST-E1 (early 2030s). Found at: tokamak-energy-roadmap.md.

8. **World Nuclear News** — "Tokamak Energy gives details of pilot fusion energy plant design." Earlier design snapshot (A=2.0, R0=4.25 m, B0=4.25 T). Found at: tokamak-energy-st-e1-design-evolution.md.

9. **Tokamak Energy heating systems article** — Interesting Engineering coverage of 1 MW gyrotron delivery. Earlier power figures (800 MW fusion, 85 MWe net) from pre-Revision D design. Found at: tokamak-energy-heating-systems.md.

10. **Tokamak Energy overview** — Company homepage. Marketing content only. Found at: tokamak-energy-overview.md.
