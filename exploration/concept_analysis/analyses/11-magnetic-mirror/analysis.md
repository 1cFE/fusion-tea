---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (Realta Fusion / CoSMo)
Company: Realta Fusion
Status: draft
Created: 2026-06-09
Approved-Date:
Confinement-Family: MFE
Archetype: MIRROR
Archetype-Fit: High
Comparison-Status: costingfe
Comparables: []
Design-Point-Name: Hammir pilot plant — Frank et al. 2024 conservative operating point (Realta Fusion)
Design-Point-Maturity: paper-concept
P-Native: 50
Grounding-Confidence: medium
---

## Design Point

- Name: Hammir pilot plant — Frank et al. 2024 conservative operating point (Realta Fusion)
- Maturity: paper-concept
- P_native: 50 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md
  - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/aps-dpp-2025-sutherland.md

## 1. Availability of Data

**Rating: Moderate**

The magnetic mirror concept benefits from a substantial historical database — six decades of experiments including Los Alamos FRX, University of Washington LSX, and the Gas Dynamic Trap in Russia — providing empirical grounding for confinement scaling, formation physics, and stability behavior. Realta Fusion has published a detailed confinement modeling study (Frank et al. 2024, arXiv 2411.06644) projecting Q > 5 for their Hammir pilot plant design using a 50-meter central cell with 25 T HTS mirror coils. This modeling work includes POPCON analysis, parametric simulations, and detailed end-plug physics.

However, **critical power plant cost data is sparse**. No plant-level costing studies exist for the modern HTS-enabled tandem mirror. The most detailed historical reactor concept, MARS (Mirror Advanced Reactor Study, 1983-1986), used outdated LTS yin-yang coils and projected 7 ¢/kWh in 1983 dollars for a ~600 MWe plant. Company-provided cost breakdowns are absent — Realta has not published subsystem costs, blanket designs, maintenance schedules, or capacity factor estimates. Public communications emphasize physics validation (WHAM experimental results, end-plug modeling) rather than techno-economic specifics.

**Key sources**:
- Frank et al. (2024): detailed Q > 5 modeling for Hammir — central cell and end-plug parameters, POPCON analysis, design point sensitivity
- Fusion Hub spotlight (2024): qualitative system overview, direct energy conversion, vortex stabilization approach
- The Fusion Report interview (2024): 7 MW/m scaling, tritium breeding confirmation, Q > 10 potential with longer cells
- WHAM experiment: 17 T HTS magnets (CFS-built), first plasma July 2024, ECH+NBI+HHFW heating demonstrated

**Data gaps**:
- No blanket design specifics (lithium chemistry, TBR calculations, thermal cycle choice)
- No first-wall lifetime or neutron damage estimates
- No direct energy conversion efficiency or capital cost estimates
- No capacity factor projections or maintenance schedules
- No tritium system details beyond "thermal blankets breed tritium from lithium"
- No cost data for HTS magnets beyond WHAM++ REBCO tape estimate ($50M for magnets represents "majority of cost")

## 2. Challenges in Capturing System Function

Five challenges dominate LCOE modeling of the tandem magnetic mirror, ranked by economic impact:

### Challenge 1: High Recirculating Power Fraction (Critical — structural cost penalty)

The tandem mirror requires continuous high-power neutral beam injection (15-20 MW per end plug, 30-40 MW total) to sustain end-plug confinement. At the Hammir design point (50 MWe net output, 30 MW NBI), the recirculating fraction is **60%** — an order of magnitude higher than steady-state tokamaks (5-15%). This fundamentally limits net electric output for a given fusion power and drives up overnight capital cost per kWe. The recirculating power does not decrease with longer center cells (which increase fusion power proportionally), creating a structural cost ceiling.

> "The input power does not change, even as the center cell gets longer" — fusion-report-interview-realta.md, §Q Scaling

This is not a modeling artifact but a physical constraint of tandem mirror operation. The library's `p_input/P_native = 0.6` ratio is at the extreme edge of the F9 validation band (0.5%, 50%), but it accurately represents this concept's architecture. For comparison, a tokamak at Q = 10 operates at ~10% recirculating power; Hammir at Q = 5.8 operates at 60%.

**LCOE consequence**: Higher overnight cost per kWe, lower capacity utilization of fusion island components, reduced competitiveness vs. concepts with lower auxiliary power demands.

### Challenge 2: End-Plug Confinement Physics Uncertainty (High — concept-gating risk)

The Frank et al. (2024) Q > 5 projection relies on **unvalidated assumptions about end-plug physics**: classical transport only (no turbulent transport), MHD stability via unspecified actuators, spatial gradients neglected, and tritium-only end-plug fuel reducing fusion rates by orders of magnitude. The authors explicitly state:

> "the question of MHD stabilization of the end plug was ignored... it was assumed that the plasma is MHD stable and whichever actuator used to ensure MHD stability was assumed to not substantially perturb equilibrium transport. This topic will be tackled in more detail in future work." — arxiv-2411-06644-confinement-predictions.md, §4.1

No fully integrated tandem mirror model exists; the published results use a "piece-wise approach" treating the end plug as a standalone simple mirror, which makes electron drag estimates conservative but does not capture coupling effects. Turbulent transport, if present, could degrade confinement by 2-5×. Kinetic instabilities from loss-cone physics are acknowledged but not quantified. The Fusion Hub notes: "this problem doesn't magically go away with the higher mirror ratios that Realta is planning on."

**LCOE consequence**: If end-plug confinement degrades below predictions, Q could fall from 5.8 to 2-3, making net electric output unviable without major design changes (longer central cell, higher NBI power, or alternative end-plug approach).

### Challenge 3: Drift-Cyclotron Loss-Cone (DCLC) Instability (Moderate — requires engineering solution)

The second Frank et al. modeling paper addresses DCLC instability — a known issue in high-beta mirrors that can rapidly dump plasma through the loss cone. While the paper "enables the development of engineering solutions," no specific mitigation approach is disclosed beyond general references to "vortex stabilization." DCLC was a historical problem for the TMX-U tandem mirror experiment. High mirror ratios (Realta targets 10+) partially suppress DCLC, but complete suppression at Q > 5 conditions is undemonstrated.

**LCOE consequence**: If DCLC proves unsuppressed, operating beta may be limited below the βc = 0.6 design target, reducing fusion power density and requiring a larger (more expensive) central cell for equivalent output. Alternatively, active stabilization hardware (RF antennas, beam modulation) would add capital cost and auxiliary power consumption.

### Challenge 4: Negative-Ion NBI Technology at 240-360 keV (Moderate — technology readiness)

Hammir requires continuous 240-360 keV negative-ion neutral beams at 60% wall-plug efficiency. Frank et al. note:

> "RF ion heating found to be ineffective for end plugs" — arxiv-2411-06644-confinement-predictions.md, Appendix B

Negative-ion NBI at this energy and efficiency exists at ITER scale (1 MeV, 50% eff, pulsed duty), but continuous-wave operation at the required parameters is not commercially demonstrated. The technology path is clear but carries execution risk. The beam energy choice (240 vs. 360 keV) significantly affects end-plug density and NBI power requirements — the parametric study shows a 5 MW spread between optimum (240 keV, 15 MW) and alternate (360 keV, 20 MW) cases.

**LCOE consequence**: If wall-plug efficiency falls short (e.g., 50% vs. 60%), recirculating power increases proportionally, reducing net output. If continuous-wave reliability proves poor, capacity factor degrades. The cost of 30-40 MW of continuous negative-ion NBI systems is a major CAS22 capital driver not captured in default mirror pricing.

### Challenge 5: HTS Magnet Feasibility at 25 T Planar Geometry (Moderate — technology scale-up)

The Hammir design requires 25 T HTS (REBCO) mirror throat magnets in planar axisymmetric coils. WHAM has demonstrated 17 T in-bore field with CFS-built HTS coils. The 25 T target is stated as "should be viable" but not yet built. REBCO tape current density, quench protection, and mechanical strain at 25 T in meter-class bores represent an incremental but non-trivial scale-up from WHAM. The longer central cell uses weaker ~3 T solenoid magnets, which are straightforward, but the end-plug magnets are the enabling technology.

**LCOE consequence**: If 25 T proves infeasible or excessively expensive, mirror ratio falls below 10, degrading end-plug confinement and forcing either lower Q (higher recirculating fraction) or larger machine geometry. The $50M REBCO tape cost for WHAM++ (noted as "majority of cost") provides a cost anchor, but scaling to Hammir's full magnet set is uncertain.

## 3. Maturity of Key Subsystems and Components

Subsystems are ranked by ascending maturity (least mature first), following the template requirement.

### Direct Energy Conversion (Venetian Blinds) — TRL 2-3

**On paper only**: Historical MARS study employed venetian blind electrostatic direct energy converters with ~54% efficiency. Realta has discussed implementing "axisymmetric ferromagnetic venetian blinds" to capture escaping charged particles from the central cell. The concept: lost ions emerge as a directed beam, electrodes maintained at high voltage decelerate them and recover kinetic energy as current.

**Missing at scale**: No venetian blind system has operated in a D-T neutron environment. Thin electrodes downstream of the fusion reaction must survive debris, X-rays, and scattered neutrons without cooling. Surface damage and sputter erosion over thousands of operating hours is uncharacterized. The handwritten analysis notes: "survivability of thin uncooled electrodes downstream of a fusion reactor is low."

At the Hammir design point, 20% of transport power (alpha particle exhaust) flows through the loss cone. At 54% conversion efficiency, DEC recovers ~11% of fusion power as electricity, reducing thermal burden but not fundamentally altering the power balance. If DEC is omitted (f_dec = 0), LCOE increases by ~15-20% due to lower net output for the same fusion power.

**Alternative**: Drop venetian blinds, thermalize all exhaust in expander divertors, accept ~10% LCOE penalty. This is the conservative modeling path given survivability concerns.

### Tritium Breeding Blanket — TRL 2-3

**On paper only**: The Fusion Report interview confirms "thermal blankets (which also produce tritium from lithium)," but Realta has not published blanket chemistry, geometry, or TBR calculations. Historical MARS used LiPb eutectic (Li17Pb83) with TBR = 1.15. Modern candidates include FLiBe molten salt, liquid lithium, or helium-cooled solid ceramic breeders.

**Missing at scale**: No blanket design specific to the linear tandem mirror geometry exists. The cylindrical central cell allows simpler blanket coverage than toroidal devices, and the open ends route exhaust to expander divertors (reducing divertor heat flux challenge), but no engineering drawings, thermal-hydraulic analysis, or tritium extraction scheme have been disclosed.

At 175-200 MW fusion power (Hammir target), 14.1 MeV neutron wall loading on the central cell first wall is ~0.5-1.0 MW/m². This is moderate by fusion standards (DEMO targets ~2 MW/m²), easing materials constraints. The blanket must achieve TBR > 1.0 given the tritium supply crisis (global inventory ~25 kg, single plant startup needs ~1 kg).

### End-Plug Physics and NBI Systems — TRL 3-4

**Demonstrated**: Simple mirror physics at high mirror ratios (WHAM targets R_mirror > 10), negative-ion NBI at ITER scale (1 MeV, pulsed), ECH/ECRH at 100+ GHz (gyrotrons), HHFW RF ion acceleration. WHAM achieved first plasma in July 2024 with 17 T HTS magnets, demonstrating high-field simple mirror operation.

**On paper only**: Tandem mirror end-plug operation with Q > 5 central cell, continuous-wave negative-ion NBI at 240-360 keV and 60% wall-plug efficiency, T-only end-plug fuel cycle reducing neutron damage, integrated vortex stabilization, and sloshing-ion kinetic stability.

**Missing at scale**: The Anvil device (Realta's next step, post-WHAM, ~2028) aims to demonstrate "stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant." This is explicitly the de-risking objective. Until Anvil operates, end-plug confinement projections remain simulation-based.

### HTS Magnets (REBCO, 17-25 T) — TRL 5-6

**Demonstrated**: WHAM uses two CFS-built 17 T HTS magnets (REBCO tape), setting a world record for magnetic field strength in magnetically confined plasmas. Tokamak Energy's Demo4 achieved 11.8 T in a full tokamak (Nov 2025). CFS SPARC prototype TF coil tested at 20 T. Large-bore HTS coils under relevant thermal/mechanical loads have been qualified.

**Missing at scale**: Hammir requires 25 T mirror throat field, a 47% increase over WHAM. While REBCO tape performance curves suggest 25 T at 20 K is achievable, no meter-class 25 T magnet has been built. Quench protection, AC losses during field ramps, and mechanical strain in planar pancake geometries at this field strength need demonstration.

Supply chain: CFS is Realta's magnet supplier. REBCO tape global production is scaling (thousands of km/year currently, 10,000+ km needed for a single Hammir-class plant if end-plug magnets dominate). The $50M REBCO cost for WHAM++ (Realta's next simple-mirror experiment) is noted as "majority of cost," suggesting HTS magnets are the single largest capital item.

### Balance of Plant (Thermal Cycle, Turbines, Heat Rejection) — TRL 6-7

**Demonstrated**: Frank et al. assume 50% thermal-to-electric efficiency (Brayton cycle). MARS achieved 36% with 1980s technology. Modern sCO2 Brayton cycles approach 45-50% at high inlet temperatures. Standard Rankine steam cycles are 35-40%. Turbine plant equipment, heat exchangers, and cooling towers are mature commercial technologies.

**Missing at scale**: Integration with a fusion-specific heat source (pulsed vs. steady-state thermal transients, tritium-compatible heat exchangers, FLiBe or LiPb coolant chemistry). The linear mirror geometry simplifies primary coolant loops (no toroidal complexity), but no plant-level thermal balance or component sizing has been published.

### Vacuum Vessel, Remote Handling, Cryogenics — TRL 6-7

**Demonstrated**: Cylindrical vacuum vessels, cryogenic systems for HTS magnets (20 K operation), remote handling for activated components (ITER prototypes). The axisymmetric linear geometry offers a structural advantage: "simpler construction and maintenance" vs. toroidal devices. The central cell is essentially a long cylindrical pressure vessel with radial penetrations for NBI and diagnostics.

**Missing at scale**: Module replacement strategy for the central cell. The Fusion Hub notes mirrors could be "designed for disassembly and replacement, reducing the time the machine needs to be offline," but this "requires working in a hot (radioactive) cell surrounding entire machine, or finding clever ways to isolate the interior, which is in of itself costly." No capacity factor estimate or maintenance schedule has been published.

The open-ended geometry routes power and particle exhaust to large expander regions "far away from the expensive HTS magnets," reducing radiation damage to the highest-value components. Neutron shielding between the central cell and end-plug magnets is critical but not yet designed.

## 4. Key Materials and Supply Chain Considerations

### REBCO Superconducting Tape (Critical — dominant capital cost item)

**Current capacity vs. plant demand**: WHAM++ (Realta's second experiment, targeting scientific breakeven) requires an estimated $50M in REBCO tape, described as "the majority of the cost." Scaling to Hammir (50 MWe) or commercial plants (100-500 MWe) would require multiple km of REBCO tape per plant. Global production capacity is currently thousands of km/year (Shanghai Superconductor Technology, Faraday Factory Japan, CFS Magnetics). A Hammir-class plant likely requires 5,000-10,000 km of tape depending on coil design — within reach of current capacity but representing a significant procurement commitment.

**Cost trajectory**: REBCO tape pricing is ~$50-150/kA-m at commercial volumes today. Learning curve projections target $10-30/kA-m for GW-scale deployment. Realta's partnership with CFS for magnet fabrication provides access to the leading HTS supply chain in fusion, but tape cost remains a dominant capital driver. The simple planar pancake coil geometry (vs. 3D stellarator coils or tokamak TF coils) minimizes tape consumption per tesla-meter of field.

**Sole-source risk**: REBCO production is concentrated in three suppliers globally. CFS is vertically integrating tape production. Any supply disruption or price spike directly impacts capital cost. Shared demand with tokamak/stellarator programs (CFS SPARC, Tokamak Energy ST80, Proxima QI stellarator) could create allocation constraints.

### Tritium (Critical — fuel cycle and licensing)

**Startup inventory**: Hammir at 50 MWe, 175 MW fusion power, requires ~0.5-1 kg tritium startup inventory (estimated from burn rate and residence time). At current market prices (~$30,000-35,000/g), this is $15-35M. Global civilian tritium inventory is ~25-30 kg (declining as CANDU reactors retire), creating a sequencing constraint: the first few fusion plants must demonstrate TBR > 1 before the fleet can scale.

**Breeding requirement**: Realta confirms "thermal blankets breed tritium from lithium" but has not disclosed TBR calculations or blanket chemistry. MARS achieved TBR = 1.15 with LiPb. If Realta uses FLiBe or lithium-ceramic breeders, TBR must still exceed 1.0 with margin for extraction losses and decay. The linear geometry's higher surface-to-volume ratio (vs. compact tokamaks) aids tritium breeding — more blanket area per fusion power — but no quantitative TBR estimate exists.

**Tritium extraction and processing**: At 175 MW fusion power, Hammir burns ~150 g tritium/day (assuming 1% burnup fraction, which is typical for open-ended systems with low confinement time). Extraction from blanket, purification, and recycling require kg/day throughput capacity. The open ends exhaust unburned fuel and alpha ash continuously, mixing with end-plug tritium. Separating tritium from helium, deuterium, and impurities in a continuous exhaust stream is more complex than tokamak pellet fueling, where fuel is batch-injected and ash is pulsed out. No tritium system design has been published.

### Lithium (blanket breeder) and Beryllium (multiplier)

**Li-6 enrichment**: Natural lithium is 7.5% Li-6, 92.5% Li-7. Tritium breeding requires 30-90% Li-6 enrichment depending on blanket design. Li-6 enrichment is commercially available but not at GW-scale fusion fleet production rates. Current suppliers are concentrated in Russia and China (mercury-based processes). The U.S. and EU are rebuilding Li-6 enrichment capacity in response to fusion needs, but scaling to multi-ton annual throughput per plant is 5-10 years out.

**Beryllium neutron multiplier**: If Realta uses a solid-breeder blanket (Li₄SiO₄ + Be pebbles, HCPB-style), beryllium demand is 50-100 t per plant. Global beryllium production is ~300 t/year, dominated by Materion (U.S.). Beryllium is toxic, expensive (~$800/kg), and supply-constrained. If Realta chooses FLiBe (molten Li₂BeF₄ salt), beryllium demand is higher (~200-300 t per plant for both salt and multiplier zones), further straining supply. Historical MARS used LiPb (no beryllium), which is the least supply-constrained option.

**Blanket chemistry choice is LCOE-critical**: FLiBe is expensive but simplifies tritium extraction and corrosion management. LiPb is cheaper but poses corrosion and MHD-interaction challenges. Solid-ceramic breeders (HCPB) require helium coolant loops and pebble-handling systems. Until Realta specifies blanket type, supply-chain risk remains unquantified.

### Structural Materials and First Wall

**Reduced-activation steels (RAFM)**: The central cell first wall sees ~0.5-1.0 MW/m² neutron wall loading. RAFM steels (EUROFER, F82H) or SiC composites are candidate materials. RAFM is not mass-produced; specialty nuclear-grade procurement adds cost. At Hammir scale (50 m × 1 m diameter central cell), first-wall surface area is ~160 m², requiring ~10-20 t of RAFM. This is modest compared to tokamak in-vessel components but still a specialty procurement item with 12-18 month lead times.

**Radiation damage**: At 1 MW/m² wall loading and 80% availability, the first wall accumulates ~10-15 DPA/year. RAFM steels reach end-of-life at ~20-50 DPA depending on operating temperature and microstructure. This implies a 2-5 year first-wall lifetime. Module replacement strategy is critical for capacity factor but undisclosed.

The end-plug proposal to use T-only fuel (rather than D-T) reduces end-plug neutron rates by "many orders of magnitude" and shifts neutron energy from 14.1 MeV to ~3 MeV (T-T fusion products). This dramatically reduces radiation shielding requirements for end-plug magnets and NBI components, a cost advantage unique to the tandem mirror architecture.

### Tungsten (divertor/expander surfaces)

The open ends route escaping plasma to expander divertors where it neutralizes and pumps out. These surfaces experience heat fluxes similar to tokamak divertors (~5-10 MW/m²) but distributed over larger areas. Tungsten monoblock tiles on CuCrZr heat sinks are the baseline technology (ITER heritage). Tungsten supply is adequate (global production ~90,000 t/year), but precision fabrication of plasma-facing components is expensive and time-consuming. No expander divertor design has been published, making cost estimation speculative.

## 5. Design Point Parameters

The following parameters describe the **Hammir pilot plant conservative operating point** from Frank et al. (2024), targeting > 50 MWe net electric output at Q > 5. This is the "optimum case" from Table 3 of arxiv-2411-06644-confinement-predictions.md. All values are at the native 50 MWe scale.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 50 MWe | arxiv-2411-06644 §3.2, aps-dpp-2025 | high | Design target; must equal P_native. Spec key: `P_native` |
| fusion_power_MW | 175 MW (optimum) | arxiv-2411-06644 §3.2 Table 3 | high | Informational only — `p_fus` back-solved by library from `p_input` + `P_native`; do NOT put in spec |
| p_input_MW | 30 MW (2×15 MW NBI) | arxiv-2411-06644 §3.2 Table 3; analyst-patch §Verified central-cell spec | high | Total NBI wallplug power (both end plugs). Spec key: `p_input`. Drives 60% recirculating fraction. |
| chamber_length | 50 m | arxiv-2411-06644 §3.2, fusion-report §Q scaling | high | Central cell length. Spec key: `chamber_length`. Scales at ~7 MW fusion per meter. |
| plasma_t (central cell radius) | 0.54 m | arxiv-2411-06644 Table 3 (a_c); analyst-patch §Verified spec | high | Central cell plasma radius. Spec key: `plasma_t`. Optimum case. Alternate case: 0.78 m. |
| B (central cell on-axis field) | 3.0 T | arxiv-2411-06644 Table 3 (B0c); analyst-patch §Verified spec | high | Central cell magnetic field (weaker than end plugs). Spec key: `B` (canonical name, NOT `B0`). Alternate case: 2.6 T. |
| B_mirror (throat field) | 25 T | arxiv-2411-06644 §3.2, §4.1 | medium | End-plug mirror throat field (HTS REBCO magnets). NOT a spec key (end-plug geometry dropped for single-cell mirror library model). |
| mirror_ratio | ~8.3 | [inferred: 25 T / 3.0 T] | medium | Ratio of mirror throat field to central cell field. Enables high-beta end plugs with reduced loss-cone losses. |
| T_i (ion temp, central cell) | 50 keV | arxiv-2411-06644 Table 3 (T_ic optimum case) | high | Central cell ion temperature. Alternate case: 57 keV. |
| T_e (electron temp, central cell) | 100 keV | arxiv-2411-06644 Table 3 (T_ec optimum case) | high | Central cell electron temperature. Higher than ions (atypical for fusion plasmas). Alternate case: 120 keV. |
| n_c (central cell density) | 7.5×10¹⁹ m⁻³ | arxiv-2411-06644 Table 3 (nc optimum case) | high | Central cell plasma density. Alternate case: 5.8×10¹⁹ m⁻³. |
| beta_c (central cell beta) | 0.6 | arxiv-2411-06644 §3.2 | high | Central cell plasma beta (βc). Informational — not a spec key. |
| Q (fusion gain) | 5.8 (optimum case) | arxiv-2411-06644 §3.2 Table 3 | medium | Fusion power / NBI power. Informational — back-solved by library from p_input and net electric. Alternate case: Q = 5.0. |
| Q_e (electric gain) | > 1.0 | aps-dpp-2025, arxiv-2411-06644 §1 | high | Net electric out / total electric in (NBI + auxiliaries + BOP). Target threshold. |
| eta_th (thermal efficiency) | 0.50 | arxiv-2411-06644 §3.2 Equation 26 | medium | Brayton cycle assumption. Spec key: `eta_th`. MARS achieved 36%; modern sCO2 targets 45-50%. |
| eta_NBI | 0.60 | arxiv-2411-06644 §3.2 Equation 26 | medium | Negative-ion NBI wall-plug efficiency. Spec key: `eta_pin`. ITER-class target but not yet demonstrated in continuous-wave. |
| C_mult (blanket multiplication) | 1.1 | arxiv-2411-06644 §3.2 Equation 26 | high | Neutron energy multiplication in blanket (14.1 MeV → ~15-16 MeV total with (n,2n) and exothermic reactions). Standard D-T value. Spec key: `mn`. |
| NBI_energy_per_plug | 240 keV (optimum) | arxiv-2411-06644 Table 3 (E_NBI optimum case) | high | Negative-ion beam energy for end-plug fueling. Alternate case: 360 keV. NOT a spec key (end-plug parameter). |
| n_p (end-plug density) | 1.66×10²⁰ m⁻³ | arxiv-2411-06644 Table 3 (optimum case) | high | End-plug plasma density (3× higher than central cell). NOT a spec key. |
| beta_p (end-plug beta) | 0.58 | arxiv-2411-06644 Table 3 (optimum case) | high | End-plug plasma beta. NOT a spec key. |
| a_m (mirror throat radius) | 0.15 m | arxiv-2411-06644 Table 3 (optimum case) | high | Mirror throat plasma radius. NOT a spec key. Alternate case: 0.20 m. |
| l_p (end-plug length) | 4.5 m | arxiv-2411-06644 Table 3 | high | End-plug mirror cell length (both ends). NOT a spec key. |
| tau_c (central cell confinement) | ~5-10 s | arxiv-2411-06644 §1 | medium | Central cell particle confinement time. "Very large confinement times" relative to tokamaks (~1 s). Informational. |
| f_dec (DEC energy fraction) | 0.20 | [analogue: alpha particle fraction in D-T, 20% of fusion energy] | low | Fraction of transport power available for direct energy conversion (alpha particles escaping through loss cone). Spec key: `f_dec`. If DEC is dropped (conservatively), set to 0. |
| eta_de (DEC efficiency) | 0.54 | [analogue: MARS historical venetian blind DEC efficiency, 1983 study] | low | Direct energy conversion efficiency if venetian blinds are implemented. Spec key: `eta_de`. MARS achieved ~54%; modern estimate uncertain. |
| blanket_t | 0.60 m | [estimated from MARS study and typical D-T blanket thickness] | low | Blanket thickness (breeder + shield). Spec key: `blanket_t`. MARS used ~0.5-0.6 m LiPb blanket. No Realta-specific value. |
| ht_shield_t | 0.20 m | [estimated from typical magnetic confinement shielding] | low | High-temperature neutron shield thickness. Spec key: `ht_shield_t`. Standard D-T value. |
| structure_t | 0.15 m | [estimated from cylindrical pressure vessel scaling] | low | Structural support thickness (vessel wall, ribs, support frame). Spec key: `structure_t`. |
| vessel_t | 0.10 m | [estimated from vacuum vessel wall thickness at ~1 m diameter] | low | Vacuum vessel wall thickness. Spec key: `vessel_t`. |
| availability | 0.85 | [standard fusion assumption; no Realta-specific estimate] | low | Plant availability factor. Spec key: `availability`. No capacity factor or maintenance schedule published. |
| lifetime_yr | 30 | [standard plant economic lifetime] | medium | Plant operating lifetime. Spec key: `lifetime_yr`. |
| construction_time_yr | 5.0 | [estimated for first-of-a-kind 50 MWe pilot plant] | low | Construction duration. Spec key: `construction_time_yr`. No Realta estimate. FOAK target is early 2030s; NOAK mid-late 2030s. |

**Key inferences and gaps**:

1. **End-plug parameters dropped**: The 1costingfe `MIRROR` model represents a single-cell mirror only. All end-plug geometry (`l_p`, `a_m`, `B_m`, `B_0`) and end-plug plasma parameters (`T_ic`, `beta_p0`, `n_p0`, `E_NBI`) are published by Frank et al. but have no library equivalent. The analyst-patch document confirms these must be DROPPED from the spec to avoid validation errors. The physics consequence (Q > 5) is baked into the central-cell parameters; the library back-solves fusion power from `p_input` + `P_native`.

2. **High recirculating fraction is architectural**: The `p_input/P_native = 30/50 = 0.6` ratio is at the extreme edge of the F9 validation band (0.5%, 50%) but accurately represents tandem mirror operation. This is not a data error; mirrors run 30-50% recirculating power vs. steady-state MFE 5-15%. The analyst-patch confirms this as a "genuinely high-recirculation tandem-mirror design."

3. **Direct energy conversion uncertainty**: `f_dec = 0.20` and `eta_de = 0.54` are analogues from MARS (1983) and tokamak alpha-exhaust fractions. Realta has discussed venetian blind DEC but provided no efficiency estimates or capital cost data. Conservative modeling path: set `f_dec = 0`, drop DEC entirely, accept ~10-15% LCOE penalty. Optimistic path: retain DEC with MARS-level efficiency, but flag survivability risk.

4. **Blanket chemistry unknown**: `blanket_t = 0.6 m` is an engineering estimate from MARS LiPb blanket. Realta has confirmed lithium-based tritium breeding but not specified FLiBe, LiPb, liquid Li, or solid ceramic. This is a critical gap for cost modeling — different chemistries have order-of-magnitude different costs and supply-chain implications.

5. **Capacity factor / maintenance unknown**: `availability = 0.85` is the standard fusion assumption. No Realta-specific capacity factor, first-wall lifetime, or planned replacement interval exists. The modular "CoSMo" branding suggests module replacement as a maintenance strategy, but no schedule or cost estimate is published.

## 5b. Override Candidates

```yaml
overrides: []
```

**Rationale for zero overrides**:

The per-account walkthrough of the canonical 1costingFE schema identified **no company-grounded cost data** that justifies departing from library defaults. The analyst-patch document confirms "lack of company-grounded cost data" as the reason for an empty overrides list. The dossier provides:

- One data point: "$50 million in REBCO tape alone for WHAM++, although that is expected to be the majority of the cost" (Fusion Hub). WHAM++ is a simple-mirror scientific breakeven experiment, **not the Hammir pilot plant**. The magnet geometry, field strength (likely <20 T), and scale differ significantly from Hammir's 25 T mirror coils + 50 m solenoid. Extrapolating WHAM++ tape cost to Hammir requires assumptions about coil geometry, field profile, and conductor performance that are not grounded in published Realta data. This does not meet the "direct" or "derived" provenance threshold.
- Qualitative claims: "simpler magnet geometry → cheaper construction," "fewer magnets than a stellarator," "low capital path to fusion energy." These are positioning statements, not accountable cost figures.
- No published subsystem costs for blanket, first wall, vacuum vessel, NBI systems, tritium processing, direct energy conversion hardware, buildings, or balance of plant.

**Per-account decisions (excerpt)**:

- **C220103 (Confinement magnets)**: The $50M WHAM++ figure is the only magnet cost anchor, but it describes a different device (simple mirror, not tandem; smaller scale; possibly lower field). Scaling factor from WHAM++ to Hammir is ungrounded. **No override.**
- **C220104 (Supplementary heating — NBI)**: 30 MW continuous negative-ion NBI at 240-360 keV and 60% efficiency. No capital cost or unit cost ($/MW installed) provided by Realta. ITER NBI costs are public ($50-100M per 16.5 MW injector, pulsed duty) but Hammir's continuous-wave requirement may differ substantially. **No override.**
- **C220109 (Direct energy converter)**: Venetian blinds mentioned in Fusion Hub, but no efficiency data, capital cost, or hardware description from Realta. MARS achieved ~54% DEC efficiency in 1983, but electrode design, voltage profile, and cost are not transferable to a modern HTS tandem mirror. **No override.**
- **CAS21 (Buildings)**: Qualitative claim of "simpler construction" due to cylindrical geometry vs. toroidal devices. No dollar figure, cost breakdown, or building size estimate. The linear geometry likely simplifies hot cell access and reduces shielding complexity, but the magnitude of the cost advantage is not quantified. **No override.**
- **CAS27 (Special materials — blanket inventory)**: Blanket chemistry unknown (FLiBe vs. LiPb vs. solid ceramic). No tritium breeding ratio, no lithium mass, no beryllium mass, no material cost estimate. **No override.**

**Override count sanity check**: Archetype-Fit is High → expected band is 0-4 enabled overrides. Actual count: 0. This falls within the expected band. The count reflects genuine data sparsity: Realta has prioritized physics validation (WHAM experiment, confinement modeling) over techno-economic disclosure. The LCOE model will rely entirely on library defaults, which are calibrated to historical magnetic confinement concepts (MARS, TMX, MFTF) and modern HTS cost proxies.

**Consequence for model reliability**: The resulting LCOE estimate is a corridor-level projection, not a plant-specific forecast. Uncertainties are large (±50-100%) due to the absence of company-grounded overrides. Key parameters where library defaults may misrepresent Hammir:

1. **C220103 magnet cost**: Library prices HTS magnets by coil geometry and field. The tandem mirror's hybrid architecture (25 T end-plug mirrors + 3 T central-cell solenoid) may be cheaper per tesla-meter than a uniform high-field tokamak, but this is not captured without an override.
2. **C220104 NBI cost**: Continuous-wave negative-ion beams at 240-360 keV are more expensive than pulsed ITER-class injectors, but the magnitude is unknown.
3. **C220109 DEC cost**: If venetian blinds are implemented, they represent a ~$20-50M capital item (estimated from MARS study inflation-adjusted) plus operating cost. If omitted, LCOE increases ~10-15%. The library model does not include DEC by default.
4. **CAS21 building cost**: The linear geometry may reduce building volume and shielding complexity by 20-30% vs. a toroidal device, but this is speculative.

The model will flag these gaps in the Data Quality Warning section and present LCOE as a band (pessimistic / baseline / optimistic) bounded by plausible override ranges.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | **Blanket chemistry and TBR calculation**: Realta confirms lithium-based tritium breeding but has not specified FLiBe, LiPb, liquid Li, or solid ceramic breeder. No TBR calculation, lithium mass, beryllium requirement, or blanket thermal-hydraulic design exists. | S3, S4, S5 | proprietary / not-yet-sourced | blocking | Request Hammir pre-conceptual design paper (expected 2026 per dossier). Alternatively, use MARS LiPb blanket (TBR=1.15) as historical analogue with low confidence flag. |
| 2 | **Direct energy conversion efficiency and cost**: Venetian blind DEC mentioned qualitatively (Fusion Hub). No efficiency estimate, electrode geometry, voltage profile, capital cost, or survivability analysis from Realta. MARS achieved ~54% in 1983, but modern HTS tandem mirror conditions differ. | S3, S5, S5b | proprietary / not-yet-sourced | important | Request DEC system design from Realta or CFS (if subcontracted). If unavailable, model two scenarios: (a) no DEC (f_dec=0, conservative), (b) MARS-level DEC (eta_de=0.54, optimistic). |
| 3 | **Capacity factor and maintenance schedule**: No first-wall lifetime, planned replacement interval, or module changeout duration published. `availability = 0.85` is an ungrounded assumption. | S3, S5 | proprietary / not-yet-sourced | important | Request maintenance strategy and component lifetime estimates. Cross-reference tokamak first-wall replacement schedules (2-5 years at 1 MW/m²). |
| 4 | **HTS magnet cost at Hammir scale**: $50M REBCO tape for WHAM++ is the only cost anchor, but WHAM++ is a different device (simple mirror, smaller scale, likely <20 T). No cost estimate for Hammir's 25 T mirrors + 50 m solenoid. | S4, S5b | proprietary / not-yet-sourced | important | Request CFS magnet cost estimate or REBCO tape procurement quote for Hammir geometry. If unavailable, scale WHAM++ cost by conductor length and field (±50% confidence). |
| 5 | **Negative-ion NBI capital cost**: 30 MW continuous-wave at 240-360 keV and 60% efficiency. No capital cost ($/MW) or unit cost from Realta. ITER NBI costs are $50-100M per 16.5 MW (pulsed). | S3, S5, S5b | not-yet-sourced | important | Request NBI system quote from neutral beam suppliers (e.g., NNBI consortium, JAEA, ORNL). Continuous-wave duty cycle may add 20-50% cost vs. pulsed. |
| 6 | **Turbulent transport in end plugs**: Frank et al. assume classical transport only. Turbulent transport, if present, could degrade confinement by 2-5×, reducing Q from 5.8 to 2-3. Authors note gyrokinetic simulations are "future work." | S2, S5 | truly-unknown | blocking | Await gyrokinetic turbulence simulation results (Frank et al. future publication). No alternative source — this is a fundamental physics uncertainty. |
| 7 | **MHD stabilization actuator and cost**: Frank et al. state "MHD stability was assumed" but not modeled. The actuator (vortex coils, RF antennas, or beam modulation) is unspecified. If active stabilization is required, capital cost and auxiliary power increase. | S2, S5 | proprietary / not-yet-sourced | important | Request MHD stabilization approach from Realta. If unavailable, estimate cost analogy to tokamak error field correction coils (~$10-20M). |
| 8 | **DCLC instability mitigation hardware**: Second Frank et al. paper "enables engineering solutions" but does not specify mitigation approach. If DCLC suppression requires RF heating, rotating magnetic fields, or feedback control, capital cost and auxiliary power increase. | S2 | proprietary / not-yet-sourced | important | Request DCLC mitigation design or wait for second Frank et al. paper publication with engineering details. |
| 9 | **Expander divertor heat flux and design**: Open ends route escaping plasma to expanders. Heat flux distribution, tungsten tile area, cooling requirements, and particle pumping capacity not published. | S3, S4 | proprietary / not-yet-sourced | nice-to-have | Request divertor/expander thermal analysis. If unavailable, estimate heat flux from power balance: ~20% of fusion power exits through end losses (~35 MW per end), distributed over ~1-2 m² expander surface → 15-35 MW/m². This exceeds tokamak divertor limits (10 MW/m²) and may require active cooling or larger surface area. |
| 10 | **Tritium extraction efficiency and system cost**: At 175 MW fusion, Hammir burns ~150 g tritium/day. Extraction from blanket, purification, separation from helium/deuterium in exhaust, and recycling require kg/day throughput. No tritium system design or capital cost estimate. | S4, S5 | derivable | nice-to-have | Estimate tritium processing cost by analogy to ITER tritium plant (~$500M for 2 kg/day capacity, adjust for Hammir's 0.15 kg/day → ~$50-100M). Cross-check with tokamak tritium system costs. |
| 11 | **Building footprint and site requirements**: 50 m central cell + expanders + NBI beamlines + auxiliary systems. Total building length ~80-100 m estimated, but no site layout or building volume from Realta. Linear geometry simplifies construction but requires more land area than compact toroidal devices. | S5, S5b | derivable | nice-to-have | Estimate building volume from MARS study (600 MWe plant, ~40,000 m² reactor building) scaled to Hammir's 50 MWe → ~3,000-5,000 m². Cross-check with tokamak building costs (~$300-500/m²). |
| 12 | **T-only end-plug fuel cycle validation**: Frank et al. propose tritium-only end plugs to suppress neutron rates and reduce radiation damage to magnets. T-T fusion produces ~3 MeV neutrons vs. 14 MeV from D-T. This concept is undemonstrated experimentally — no mirror experiment has operated with T-only fuel. Tritium inventory and licensing implications are uncertain. | S2, S3, S5 | truly-unknown | important | No near-term experimental validation path (WHAM/Anvil use D or H fuel). Await Hammir design paper for T-only fuel cycle analysis. If unavailable, model as D-T end plugs (conservative — higher neutron damage, higher shielding cost). |

## 7. Family-Delta vs Comparables

**(No comparable concept in the corpus for this design point.)**

The comparables list provided by the orchestrator is empty. This indicates no prior analysis in the corpus shares sufficient architectural similarity for a structured delta comparison. However, the dossier and handwritten exemplars provide context for positioning the tandem magnetic mirror within the broader magnetic confinement family and against tokamak/stellarator architectures.

### Structural Positioning (No Quantitative Comparables)

The tandem magnetic mirror occupies a distinct corner of the MFE design space:

**Geometry and field topology**: Linear open-field-line system vs. closed toroidal flux surfaces (tokamaks, stellarators). The cylindrical central cell with axial end plugs eliminates toroidal curvature, simplifying magnet geometry (planar pancake coils vs. 3D helical or toroidal coils) and blanket design (cylindrical annulus vs. complex 3D breeding zones). The open ends route power and particle exhaust to large expander divertors far from the high-field magnets, reducing radiation damage to the highest-cost components.

**Confinement mechanism**: Electrostatic plugging via hot dense end plugs vs. purely magnetic confinement. The end-plug potential creates a barrier to axial ion loss, enabling long confinement times (τ_c ~ 5-10 s) in the central cell despite the loss cone. This is fundamentally different from tokamak current-driven confinement or stellarator rotational transform — the mirror relies on a **continuously sustained auxiliary confinement subsystem** (the end plugs, powered by 30-40 MW NBI). This explains the 60% recirculating power fraction: the end plugs are not startup systems (like tokamak ECRH), they are steady-state operational requirements.

**Disruption immunity**: No internal plasma current → no current-driven instabilities (disruptions, vertical displacement events, sawteeth). This eliminates a major tokamak engineering burden (disruption mitigation hardware, quench-protection for magnets, runaway electron suppression). However, mirrors face different instabilities (DCLC, MHD interchange, kinetic modes from loss-cone and ambipolar potential holes). The *types* of risks differ, but the existence of concept-gating instabilities is shared across all MFE.

**Steady-state operation**: Mirrors are inherently steady-state (no pulsed plasma current, no inductive current drive). Tokamaks require either pulsed operation (lower Q, frequent thermal cycles) or continuous current drive (RF power injection, complex wave-plasma coupling). Stellarators are also steady-state but rely on 3D shaping rather than external potential barriers. The mirror's steady-state claim is not unique but is achieved via a different mechanism (sustained end plugs vs. optimized 3D fields).

**HTS magnet architecture**: The tandem mirror uses simple planar HTS coils (strong at the ends, weaker in the center) rather than complex 3D coils (stellarators) or large-bore toroidal field coils (tokamaks). The Fusion Hub claims "simplest magnet geometry out of any MCF scheme → simpler construction and maintenance." This is directionally correct: planar coils are easier to wind, align, and replace than 3D shapes. However, the 25 T mirror throat field is more aggressive than most tokamak TF coils (12-16 T typical), trading geometric simplicity for higher field strength per coil.

**Direct energy conversion pathway**: The open ends allow charged particles (unburned fuel, alpha ash) to escape axially as a directed beam, enabling electrostatic deceleration and current recovery. No closed-field-line device (tokamak, stellarator) has this option — all charged particle energy must thermalize in the blanket. If venetian blind DEC achieves ~50% efficiency on the 20% alpha-particle energy stream, it reduces the Q threshold for net-electric by ~10% (Q_e > 1 at Q_plasma ~ 4.5 instead of Q ~ 5.5). This is a **unique architectural advantage**, but it is coupled to the end-loss challenge: the same open geometry that enables DEC also requires continuous NBI power to prevent excessive losses.

### Implied Comparables (From Handwritten and Exemplar Context)

The handwritten mirror analysis (11-magnetic-mirror.md) compares mirrors to tokamaks on LCOE saturation: "MARS/MINIMARS projected LCOE of 7 ¢/kWh in 1983 dollars, and that the LCOE saturates around 600 MWe. The saturation is surprising, as it means a mirror becomes competitive at smaller outputs compared to Tokamaks that require large size to be competitive." This suggests mirrors have **better economies of scale at moderate power levels** (50-500 MWe) vs. tokamaks optimized for GW-scale. The linear scaling (7 MW fusion per meter of central cell length) supports this: to double output, extend the central cell length without increasing auxiliary power — a form of modularity that toroidal devices lack.

The handwritten analysis also notes: "LCOE ~ 80 ¢/kWh using 1costingfe with chamber_length = 20 m, eta_th = 0.50, f_dec = 0.30." The automated mirror analysis (from the comparison report) produced LCOE = 135 ¢/kWh with chamber_length = 70 m and more conservative parameters. Both are **non-competitive with current electricity prices** (~5-15 ¢/kWh), but the handwritten analysis's 20 m chamber implied Q ~ 28 (physically unrealistic for mirrors), and the automated analysis's 70 m chamber is closer to the Frank et al. design basis (50 m for Q > 5). The delta is driven by parameter optimism, not architectural differences.

The tokamak exemplar (01-hts-compact-tokamak.md) describes CFS ARC projecting LCOE ~ 60-80 ¢/kWh at 270 MWe with Q ~ 13 and ~10% recirculating power. Comparing to Hammir (LCOE TBD, 50 MWe, Q = 5.8, 60% recirculating power): the mirror's **higher recirculating fraction** is the dominant structural penalty. A tokamak at Q = 6 would operate at ~15% recirculating power; Hammir at Q = 6 operates at 60% because the end-plug NBI is independent of fusion gain. This is the price of the open-field-line geometry.

The stellarator architectural challenge (large 3D coils, complex assembly) is avoided by the mirror, but the mirror faces a different assembly challenge: the continuous 50+ meter central cell must be constructed as a single vacuum vessel or assembled from modules with high-integrity joints. The handwritten analysis notes: "Module replacement and hot-cell operations as a practical concern" — replacing a 10-meter central-cell module in a radioactive environment is conceptually simpler than replacing a tokamak blanket sector (toroidal disassembly) but still requires overhead cranes, shielded transporters, and precision alignment. No maintenance time estimate exists, making capacity factor comparison speculative.

### What Would Change the Family-Delta Assessment

1. **If end-plug confinement exceeds predictions** (turbulent transport less than classical, DCLC fully suppressed): Q could reach 8-10 with the same NBI power, reducing recirculating fraction to 30-40%. This would close the gap with tokamaks on net electric efficiency and shift the mirror from "high-recirculation penalty" to "competitive recirculation with simpler geometry."

2. **If direct energy conversion achieves >60% efficiency**: At 60% DEC efficiency on 20% of fusion power, net output increases by ~12%, equivalent to reducing overnight capital cost by 10-12% for the same LCOE. This would offset part of the high-recirculation penalty. However, DEC survivability in a D-T neutron environment is unproven.

3. **If 25 T HTS magnets prove cheaper per tesla-meter than tokamak TF coils**: The planar pancake geometry uses less conductor per unit field volume than toroidal coils (no large-bore constraint). If magnet cost scales as conductor length rather than field strength, the mirror could achieve 20-30% lower magnet cost than a tokamak with the same on-axis field. This is unverified but plausible.

4. **If capacity factor exceeds 85% due to modular maintenance**: The CoSMo branding emphasizes modularity. If central-cell modules can be replaced in <2 weeks (vs. tokamak blanket sectors requiring 6-12 months), capacity factor could reach 90-95%, improving LCOE by 10-15%. This requires demonstrated hot-cell module-handling capability, which does not exist.

The mirror's economic case rests on **cumulative advantages outweighing the high-recirculation penalty**: simpler magnets, modular construction, steady-state operation without disruptions, and potential DEC efficiency. None of these is individually decisive, but together they define a distinct architectural trade-space. The absence of comparable analyses in the corpus reflects the mirror's 40-year hiatus (1980s shutdown of U.S. mirror program) — the concept is re-emerging with HTS magnets as the enabling technology, but the TEA database has not yet caught up.

## 8. Sources

Listed in order of importance for LCOE modeling and concept assessment.

1. **Frank, I. et al. (2024).** "Physics predictions for the tandem mirror pilot plant." *arXiv preprint arXiv:2411.06644*. Available: `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md`. **What it contributes**: Detailed Q > 5 modeling for Hammir pilot plant — central cell and end-plug parameters (Table 3), POPCON analysis, design point sensitivity (optimum vs. alternate cases), T-only end-plug fuel cycle proposal, fusion power density (~3.5 MW/m³), NBI requirements (15-20 MW per plug, 240-360 keV), thermal efficiency assumptions (50% Brayton, 60% NBI, 1.1 blanket multiplication). This is the **primary quantitative source** for design point parameters. The authors acknowledge critical modeling gaps: classical transport only (turbulent transport neglected), MHD stability assumed but not modeled, end-plug treated as standalone simple mirror (not fully integrated tandem), and alpha particle removal mechanism (drift pumping) assumed but not validated. Published online November 2024.

2. **The Fusion Report (2024).** "Interview with Realta Fusion — Derek Sutherland." Available: `knowledge/concept_research/11-magnetic-mirror/iter-02/sources/fusion-report-interview-realta.md`. **What it contributes**: Confirms Q > 5 modeling from Frank et al., provides **7 MW per meter central-cell scaling** ("the longer the center cell is, the more power the system will put out (this increases by roughly 7 MW per meter)"), notes Q > 10 possible with longer cells, confirms Q = 20 scenario produces 500 MW, confirms input power does NOT scale with central-cell length, confirms **thermal blankets breed tritium from lithium**, confirms **direct energy conversion for charged particle (helium ash) capture**, and clarifies target market (50-500 MW "medium-sized" machines, early 2030s FOAK, mid-late 2030s NOAK). This source provides **architectural insights and scaling laws** critical for understanding the concept's economic value proposition. Published as interview, date not specified (dossier dated 2024).

3. **Fusion Hub (2024).** "Fusion Startup Spotlight: Realta Fusion." Available: `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/realta-fusion-hub-spotlight.md`. **What it contributes**: Qualitative system overview with emphasis on **cost advantages** ("simplest magnet geometry out of any MCF scheme → simpler construction and maintenance," "cheaper construction, cheaper operations and maintenance, and cheaper energy"), describes **direct energy conversion via axisymmetric ferromagnetic venetian blinds**, describes **vortex stabilization** for MHD (unspecified actuators), describes **sloshing ions** from skewed NBI for kinetic stability, confirms HTS REBCO magnets with "mirror ratios of 10 or more" enable breakeven and beyond, provides **$50 million REBCO tape cost for WHAM++** (noted as "majority of cost" for that device), confirms **CFS partnership for magnet manufacturing**, notes impurity accumulation challenge in tandem mirrors, and provides historical context (MARS/MINIMARS studies). This source is **qualitative but valuable for subsystem descriptions and cost positioning**. Published online, date not specified (dossier iter-01, March 2024 context).

4. **APS Division of Plasma Physics (2025).** "Hammir Facility Overview." Available: `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/aps-dpp-2025-sutherland.md`. **What it contributes**: Confirms Hammir targets **P_e > 50 MWe, Q_e > 1, 3+ hours continuous operation**, confirms tandem mirror configuration (two end plugs + central cell), confirms meets National Academies pilot plant standards, describes **Anvil device as end-plug demonstrator** (primary objective: "demonstrate stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant"), and provides WHAM context (17 T HTS magnets from CFS, simple mirror experiment). This is a **brief conference abstract** — limited quantitative detail but confirms program milestones and phasing (WHAM → Anvil → Hammir). Presented at APS DPP annual meeting, 2025.

5. **WHAM Experiment Website (2024).** Available: `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/wham-experiment-details.md`. **What it contributes**: Confirms **17 T HTS magnets (REBCO, CFS-built)**, confirms **first plasma July 15, 2024**, describes heating systems (110 GHz ECH gyrotron, NBI for fueling, HHFW RF for in-situ ion acceleration), confirms performance targets (1 keV electron temperature, 20 keV average ion energy, "approach plasma pressure limit"), describes quasi-stationary operation (duration >> confinement times), and notes "world record in magnetic field strength for magnetically confined plasmas" at 17 T. This source provides **experimental validation context** for HTS mirror operation and confirms CFS as magnet supplier. Retrieved from wham.physics.wisc.edu, 2024.

6. **Realta Fusion Press Release (2026).** "Realta Fusion Secures $9.5M Growth Capital Facility from Silicon Valley Bank." Available: `knowledge/concept_research/11-magnetic-mirror/iter-02/sources/realta-svb-funding-feb2026.md`. **What it contributes**: Confirms $9.5M debt financing (February 2026), provides CEO quote on "lower capital path to fusion energy than some other concepts" (qualitative cost claim), confirms compact/scalable/modular branding (CoSMo fusion™), confirms HTS magnet use (17 T WHAM record), and notes funding will "enable Realta to continue derisking the physics." This is a **funding announcement** — minimal technical detail but confirms company is active, funded, and targeting industrial heat/datacenter markets. Published February 2026.

7. **Analyst Patch: Specification Anchors (2026).** Available: `knowledge/concept_research/11-magnetic-mirror/iter-03/sources/analyst-patch-spec-anchors.md`. **What it contributes**: Documents **architectural mismatch between tandem mirror and 1costingFE single-cell mirror library model** — confirms end-plug parameters (l_p, a_m, B_m, B_0, T_ic, beta_p0, n_p0, E_NBI) cannot be represented in the library and must be DROPPED from spec. Confirms **high recirculating power fraction (60%) is architectural, not a data error** (p_input/P_native = 0.6 at edge of F9 validation band). Clarifies **parameter semantic mismatches** (Realta's "eta_p = 0.6" is central-cell beta β_c, NOT efficiency; Realta's "T_ec = 100 keV" is end-plug electron temperature, library's T_e is central-cell only). Documents **zero enabled overrides** due to "lack of company-grounded cost data." This is an **internal analyst guide** — not a primary source but critical for model validation and parameter mapping. Created 2026 for this analysis iteration.

8. **Historical MARS Study (1983-1986).** Logan, B. G. et al. "The Mirror Advanced Reactor Study (MARS)." LLNL/Sandia National Laboratories. Available: Semantic Scholar / OSTI. **What it contributes**: Historical baseline for mirror economics — **7 ¢/kWh in 1983 dollars** (inflation-adjusted ~25-30 ¢/kWh in 2024 dollars), ~600 MWe plant, **LCOE saturates at 600 MWe**, LiPb blanket (TBR = 1.15), **venetian blind DEC efficiency ~54%**, 36% plant thermal efficiency, yin-yang coil geometry (obsolete), and demonstrates that mirror economics are fundamentally different from tokamaks (smaller optimal scale, linear fusion-power scaling, modular construction). This study predates HTS magnets and modern NBI but provides **cost structure analogues** and validates mirror-specific phenomena (end-loss-dominated power balance, DEC contribution, linear scaling). Referenced in multiple dossier sources as the most complete mirror costing study. Published 1983-1986; not directly available in dossier but extensively cited.