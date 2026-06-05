## Design Point

- Name: Inertia Enterprises commercial plant (1,000-beamline Thunderwall, 1.5 GWe stated)
- Maturity: paper-concept
- P_native: 1500 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/enr-mike-dunne-interview.md
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/inertia-website-technical.md
  - knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/globenewswire-series-a-press-release.md

## 1. Availability of Data

**Rating: Limited**

Inertia Enterprises has released only high-level promotional materials since its founding in 2024 and $450M Series A announcement in February 2026. The available data consists of website descriptions, a press release, and one technical interview with CTO Mike Dunne. No peer-reviewed publications, detailed plant studies, or system code outputs exist from the company itself.

The concept inherits its physics foundation from LLNL's National Ignition Facility, where co-founder Annie Kritcher's Hybrid-E target design achieved ignition in December 2022. NIF's extensive experimental database (2009–present) provides well-documented ignition physics for indirect-drive targets, but **NIF operated at single-shot mode with flashlamp-pumped lasers at ~0.1% wall-plug efficiency**. The translation from single-shot ignition demonstrations to a 10 Hz, 10% efficient, 1,000-beamline power plant represents a massive engineering scale-up with sparse published data.

The LLNL LIFE (Laser Inertial Fusion Energy) program (2008–2013) produced the closest architectural predecessor. LIFE envisioned 384 diode-pumped solid-state laser beamlines delivering 2.2 MJ per target at 16 Hz with ~7% driver efficiency. Key LIFE documents include:
- Dunne et al., "Timely Delivery of Laser Inertial Fusion Energy (LIFE)" (LLNL-JRNL-438170, 2010)
- Abbott et al., "LIFE Plant Conceptual Design" (Fusion Sci. Tech. 60, 2011)
- Moses et al., "A Sustainable Nuclear Fuel Cycle Based on Laser Inertial Fusion-Fission Energy (LIFE)" (Fusion Sci. Tech. 56, 2009)

However, LIFE was terminated in 2013 before any hardware demonstrations. Inertia's Thunderwall design differs substantially in architecture (1,000 beamlines vs. 384, 10 MJ total vs. 2.2 MJ, different pulse-shaping approach), making LIFE cost estimates only loosely applicable.

**Key data gaps:**
- No published reactor design study for the 1.5 GWe plant
- No detailed laser driver cost breakdown or supply-chain analysis
- No chamber design, neutronics analysis, or first-wall lifetime estimates
- No capacity factor analysis or maintenance schedule projections
- No target manufacturing cost validation beyond the "<$1 per target" claim
- No thermal conversion cycle specifications beyond generic "steam turbines" mention

The dossier notes company transparency is "opaque" — Dunne explicitly states in the ENR interview that "specific details of these [supply chain] engagements are currently confidential."

## 2. Challenges in Capturing System Function

The major LCOE modeling challenges for this concept, ranked by impact severity:

### 2.1 Laser Driver Cost Dominance (High uncertainty, concept-unique)

The driver is the largest single capital cost item. Inertia's website claims 1,000 Thunderwall beamlines delivering 10 MJ total laser energy. The ENR interview states each beamline is "20 times more efficient than at NIF" and occupies "1/10th the physical footprint." NIF's 192-beamline system cost approximately $3.5 billion (2009 dollars, construction only), implying ~$18M per beamline.

> "Our modular laser system is the most powerful in the world. It is comprised of a thousand smaller lasers, each twenty times more efficient than at NIF."
> — inertia-website-technical.md

If Inertia's footprint and efficiency claims translate to proportional cost reduction, a naive scaling suggests ~$1.8M per Thunderwall beamline, or $1.8B total for the driver. However, the website also states "1000 Beamlines built in factories and delivered by truck," implying mass-manufacturing cost dynamics not captured in NIF's one-off construction. The handwritten exemplar for concept 26 (Laser ICF Indirect Drive) notes Xcimer's published DPSSL cost target of $60–80/J NOAK, which would imply $600–800M for a 10 MJ driver. Inertia's website states "$700–$1,000/J" but the provenance of this figure is unclear.

**Uncertainty range**: $600M (optimistic mass manufacturing at Xcimer's NOAK target) to $3B+ (conservative NIF-heritage scaling). This 5× spread dominates the LCOE uncertainty envelope.

### 2.2 Target Gain Extrapolation (High uncertainty, shared with all IFE)

Inertia claims "18 times output vs. input energy" for the pilot plant and ">30 times input-output power ratio" for the full-scale plant (ENR interview). These appear to be **capsule gain** (fusion energy / laser energy delivered to target), not **engineering Q** (net electric / total electric consumed).

NIF's December 2022 ignition shot delivered 2.05 MJ of laser energy to the hohlraum and produced 3.15 MJ of fusion energy, for a gain of ~1.5×. Subsequent shots reached up to ~2.4× gain. Inertia's claim of 18× at 10 MJ scale and 30+ at commercial scale requires:
- Target design improvements (Kritcher's Hybrid-E heritage)
- Capsule scale-up from NIF's ~2 MJ laser energy to 10 MJ
- Consistent performance at 10 Hz repetition rate

The gain scaling with laser energy is empirically validated only in the 1–3 MJ range at NIF. The 10 MJ → 30× gain claim is simulation-based, not experimentally demonstrated. The handwritten exemplar for concept 26 notes that NIF-derived architectures typically assume a 2/3-power-law scaling for gain vs. laser energy, which would predict gains of ~5–10× at 10 MJ, not 30×. Inertia's higher projection may reflect Hybrid-E design optimizations, but the claim carries **low confidence** without published simulation validation.

### 2.3 High Repetition Rate Feasibility (High uncertainty, concept-distinctive)

The 10 Hz target and 10 Hz laser operation are both unprecedented for indirect-drive ICF:
- **Chamber clearing**: Each 450 MJ fusion shot (per website: "4.5x higher energy than NIF" × NIF's ~100 MJ yield) vaporizes significant chamber material and debris. The chamber must clear, cool, and prepare for the next shot within 100 ms. No clearing strategy is described in available sources.
- **Target injection**: Delivering cryogenic D-T capsules inside lead hohlraums at 10 Hz with the required positioning precision (tens of microns) is undemonstrated. The ENR interview mentions "fuel target manufacturing plant" prototypes but provides no technical details.
- **Final optics survival**: Laser optics must survive X-ray, debris, and neutron exposure from fusion events occurring 100 ms away. LIFE envisioned grazing-incidence metal mirrors at 10 m standoff distance, but Inertia has not disclosed its optics protection strategy.
- **Thermal management**: 450 MJ × 10 Hz = 4.5 GW thermal power deposited in the chamber and blanket. The liquid lithium blanket (described on website) must circulate, extract tritium, and reject waste heat at this rate. Flow rates, pump power, and thermal cycling stresses are unquantified.

The handwritten exemplar for concept 26 notes that even Xcimer Energy's 0.25–1 Hz target is considered aggressive. Inertia's 10 Hz target is an order of magnitude more demanding.

### 2.4 Capacity Factor and Maintenance (Moderate uncertainty, IFE-shared)

The website claims "assumptions that result in 0s dwell between pulses! Structural replacements every 3-5 years." This implies >95% availability, which is inconsistent with:
- The need for chamber component replacement (first wall degradation under 14.1 MeV neutron bombardment)
- Unplanned laser beamline failures (with 1,000 beamlines, even 99.9% per-unit reliability implies several units offline at any given time)
- Target factory downtime (manufacturing defects, cryogenic system failures)

The ENR interview acknowledges "system integration" as the primary risk: "ensuring each part of the power plant works in harmony together, from the lasers to fuel targets to power production systems." No quantitative reliability or scheduled maintenance analysis has been published.

**Working assumption**: 75–85% capacity factor is more plausible for a first-of-a-kind plant, consistent with tokamak projections and IFE architectural complexity. This represents a 10–15% LCOE penalty vs. the website's implicit 95%+ assumption.

### 2.5 Balance of Plant Efficiency (Moderate uncertainty, archetype-shared)

The website states "steam turbines for electricity" but provides no thermal cycle details. LIFE studies assumed Rankine cycle at ~42% thermal efficiency (consistent with modern coal plants). The handwritten exemplar for concept 26 notes ~45% for combined-cycle approaches.

> "Neutron energy heats liquid lithium, then steam turbine cycle for electricity."
> — inertia-website-technical.md, FAQ section

The 4.5 GW thermal fusion power (450 MJ × 10 Hz) would yield ~1.9–2.0 GW electric at 42–45% efficiency. After recirculating power (10 MJ laser at 10% efficiency = 100 MW average laser wallplug, plus auxiliary systems), the 1.5 GW net electric claim appears plausible **if** the stated gains and efficiencies are achieved. However, all terms in this chain carry significant uncertainty.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first):

### 3.1 High-Repetition-Rate Target Injection and Tracking (TRL ~2)

**On paper only**: Cryogenic D-T layering, hohlraum assembly, target injection at 10 Hz with micron-scale positioning accuracy.

**Demonstrated**: NIF targets are hand-assembled, cryogenically layered over hours, and positioned via robotic inserter at single-shot cadence. General Atomics and LLNL have built NIF target prototypes but not at scale or speed.

**Missing at scale**:
- Automated factory production at 10 targets/second (315 million targets/year for continuous operation)
- Cryogenic D-T ice layer deposition with <1 μm RMS surface roughness at production rates
- Lead hohlraum fabrication at <$1/unit (current NIF gold hohlraums cost ~$50,000+ per target)
- Real-time target tracking and injection into a 10 Hz fusion chamber

The "<$1 per target" website claim is **three orders of magnitude** below current NIF target costs. The handwritten exemplar for concept 26 notes Xcimer's similar claim but flags it as unvalidated. The ENR interview states Inertia is building a "fuel target manufacturing plant prototype" to demonstrate "mass production at the scale and cost required," but no results have been published.

### 3.2 Final Optics Survivability and Beam Alignment (TRL ~2–3)

**On paper only**: Optics system that survives 450 MJ neutron/X-ray/debris environment every 100 ms for years.

**Demonstrated**: NIF final optics (fused silica, KDP frequency-conversion crystals) are damaged by single high-energy shots and require refurbishment. LIFE studied grazing-incidence metal mirrors at 10+ m standoff, but no prototypes were built.

**Missing at scale**: Radiation-hardened optics materials, debris shielding strategies, beam alignment to the required spot size (~500 μm at target) at 10 Hz cadence, replacement logistics for a 1,000-beamline system.

### 3.3 Diode-Pumped Solid-State Laser at 10 Hz, 10% Efficiency (TRL ~3)

**Demonstrated**: The Thunderwall prototype beamline is under construction (GlobeNewsWire press release). Diode-pumped solid-state lasers exist at kJ-class energy (Lawrence Livermore's Mercury laser demonstrated 10 kJ at 10 Hz in the early 2000s, but at ~5% efficiency). NIF uses flashlamp-pumped glass lasers at 1.8 MJ per beamline but <0.5% efficiency and single-shot mode.

> "Thunderwall laser system — targeting 10 MJ total energy from ~1,000 beamlines at 10 Hz and 10% wallplug efficiency"
> — dossier.md summary

**On paper only**: 10 kJ per beamline at 10% wallplug efficiency in a compact, mass-manufacturable package. The "20 times more efficient than at NIF" (ENR interview) comparison refers to wall-plug efficiency (~10% vs. NIF's ~0.5%), not laser architecture.

**Missing at scale**:
- Long-term reliability (millions of shots at rated power)
- Thermal management for continuous 10 Hz operation
- Beam quality and pulse-shaping fidelity at this efficiency
- Diode pump lifetime and replacement cost (current industrial laser diodes operate at 10,000–100,000 hour MTBF; 10 Hz for 30 years = ~10^10 shots, implying diode replacement cycles)

The handwritten exemplar for concept 26 notes laser diode costs of $0.007–0.02/W are required for IFE viability. Inertia's website mentions partnerships with "the semiconductor laser diode industry" but specifics are confidential.

### 3.4 Chamber Clearing and Debris Management (TRL ~3–4)

**On paper only**: Chamber that clears vaporized lithium, ablated wall material, target debris, and fusion ash within 100 ms to allow the next shot.

**Demonstrated**: LIFE studies analyzed liquid lithium flow patterns and FLiBe vapor clearing. Z-machine pulsed-power experiments demonstrate chamber recovery between shots, but at much lower rep rates (~1 shot per 30 minutes) and without liquid metal walls.

**Missing at scale**: Demonstration of 10 Hz clearing with liquid metal first wall. The handwritten exemplar for concept 26 notes that even Xcimer's 0.25 Hz clearing (4-second dwell) is undemonstrated; Inertia's 0.1-second dwell is far more aggressive.

### 3.5 Liquid Lithium Blanket and Tritium Extraction (TRL ~3–4)

**Demonstrated**: Liquid lithium as a plasma-facing component has been tested in tokamaks (NSTX, FTU) at small scale. Lithium blanket concepts for fusion were studied extensively in the 1970s–1980s fission-fusion hybrid programs and in LIFE.

> "Lining the fusion chamber with pipes full of liquid lithium"
> — inertia-website-technical.md, FAQ

**On paper only**: Continuous flow at GW-scale thermal power, integrated tritium extraction, corrosion management, and redox control of lithium at 500–700°C operating temperatures.

**Missing at scale**:
- Tritium extraction from flowing liquid lithium at kg/day rates
- Long-term compatibility of structural materials (steel, refractory alloys) with flowing lithium
- Lithium fire risk mitigation and safety case
- Piping and pump systems for hundreds of tons of liquid lithium circulating at m/s velocities

The website FAQ states "tritium extraction from flowing liquid lithium is still an area of active development."

### 3.6 Hohlraum Target Design and Gain Validation (TRL ~5–6)

**Demonstrated**: Annie Kritcher's Hybrid-E target design achieved ignition at NIF (December 2022, multiple subsequent shots). The design uses a low-gas-fill hohlraum with a high-density carbon ablator, enabling higher implosion velocity and lower mix compared to prior NIF targets.

**On paper only**: Scaling to 10 MJ laser energy, 30× gain, with lead hohlraums instead of gold (cost reduction), at 10 Hz cadence with consistent yield.

**Missing at scale**: The gain-vs-laser-energy scaling beyond 2–3 MJ is simulation-based. NIF's experimental database extends only to ~2 MJ. The shift from gold to lead hohlraums (for cost reasons) changes the X-ray conversion efficiency and wall albedo; this has not been experimentally validated.

### 3.7 Thermal Power Conversion (Steam Rankine Cycle) (TRL ~8)

**Demonstrated**: Conventional steam Rankine cycles at GW scale are mature technology (coal, nuclear fission).

**Missing at scale**: Integration with IFE pulsed thermal source. The 10 Hz pulse rate is slow enough that thermal storage (molten salt, pressurized water) can smooth the power delivery to the turbine, making this a relatively low-risk subsystem. LIFE studies projected 42% net thermal efficiency.

## 4. Key Materials and Supply Chain Considerations

### 4.1 Tritium (Startup Inventory and Breeding) — Shared Constraint with All D-T Concepts

**Current supply**: Global civilian tritium inventory is ~25 kg, produced as a byproduct in CANDU heavy-water reactors. Market price exceeds $30,000/g. CANDU fleet is aging; supply is declining at ~5% per year (tritium half-life 12.3 years).

**Plant requirement**: Inertia's FAQ claims "hundreds of grams" on-site (vs. "20× more for tokamaks," i.e., ~10–20 kg for a D-T tokamak). This is plausible for IFE due to lower circulating inventory, but **startup tritium for the first few plants is supply-constrained**.

**Breeding**: The liquid lithium blanket must achieve tritium breeding ratio (TBR) >1.0 to be self-sufficient. Lithium enrichment (>90% Li-6) is required for adequate breeding. Current Li-6 production is limited (Russia, China use mercury-based COLEX process; US production is minimal). LIFE studies projected Li-6 demand of several hundred kg per plant.

**Extraction**: Tritium must be continuously extracted from circulating liquid lithium to prevent buildup and maintain breeding efficiency. The FAQ explicitly states this is "still an area of active development." No pilot-scale demonstration exists.

### 4.2 Semiconductor Laser Diodes — Novel, High-Volume Demand

**Current production**: Industrial laser diodes are produced at ~100 million units/year globally for fiber optics, lidar, consumer electronics, and industrial lasers. However, the high-power, high-brightness diodes needed for fusion DPSSL drivers are a specialized subset.

**Plant requirement**: Each Thunderwall beamline likely contains thousands of individual laser diodes (based on LIFE architecture, which used diode arrays). For 1,000 beamlines, this implies millions of fusion-grade diodes per plant.

> "Inertia is partnering with a broad cross-section of the semiconductor laser diode industry"
> — enr-mike-dunne-interview.md, §ENR: What makes Inertia's technology best

**Supply-chain challenge**: The ENR interview states Inertia needs "~100× expansion of semiconductor laser diode supply chain" to support commercial deployment. Current diode costs are ~$0.05–0.20/W (industrial lasers); the handwritten exemplar for concept 26 notes fusion requires $0.007–0.02/W for LCOE viability. This implies both volume scale-up **and** unit cost reduction by factors of 3–10×.

**Lifetime**: At 10 Hz for 30 years, diodes must survive ~10^10 shots or be economically replaceable. Current high-power diodes operate at 10,000–100,000 hour MTBF, implying replacement cycles every 1–10 years.

### 4.3 Lead (Hohlraum Material) — Commodity but Novel Application

**Substitution rationale**: Inertia uses lead hohlraums instead of NIF's gold to reduce target cost. Gold costs ~$60,000/kg; lead costs ~$2,000/kg (commodity price). NIF hohlraums contain ~500 mg of gold (~$30 per hohlraum for material alone, though fabrication costs dominate).

**Plant requirement**: At 10 Hz for 1 year of full operation, Inertia consumes 315 million targets. Even at 100 mg lead per target, this is 31,500 kg/year — a negligible fraction of global lead production (~11 million tonnes/year).

**Manufacturing challenge**: Lead hohlraums require precision cylindrical shells (~1 mm wall thickness) with diagnostic holes, support features, and <10 μm dimensional tolerances. Current NIF gold hohlraums are fabricated by electroplating onto mandrels. Lead's lower melting point (327°C vs. gold's 1,064°C) may enable injection molding or die-casting at scale, but this is unproven.

### 4.4 Liquid Lithium (Blanket Coolant/Breeder) — Shared with Select Fusion Concepts

**Chemistry**: Pure liquid lithium metal, enriched to >90% Li-6 for tritium breeding. Melting point 181°C; operating temperature ~500–700°C.

**Plant requirement**: LIFE studies estimated ~500–1,000 tonnes of lithium inventory for a GW-scale plant (chamber blanket + piping + heat exchangers). Inertia's FAQ states "~20 EV battery equivalents per year" for lithium consumption, which translates to ~1,500 kg/year (assuming 75 kg lithium per EV battery × 20). This is for **makeup**, not inventory; the inventory demand is ~1,000× larger.

**Supply**: Global lithium production is ~130,000 tonnes/year (2024), dominated by battery-grade lithium carbonate/hydroxide. Fusion requires metallic lithium enriched in Li-6, which is a niche product. Natural lithium is 7.5% Li-6; enrichment to 90% requires isotope separation (currently done via COLEX or laser isotope separation). The handwritten exemplar for concept 01 notes Li-6 enrichment supply is limited to Russia, China, and small US capacity.

**Corrosion and safety**: Liquid lithium is chemically aggressive (attacks most structural steels, causes intergranular corrosion) and reacts violently with water and air. Inertia has not disclosed structural material choices or corrosion mitigation strategies. LIFE proposed nickel-based superalloys or refractory metals (V-4Cr-4Ti), but long-term compatibility at fusion-relevant conditions is unproven.

### 4.5 Optical Materials (Final Optics) — Specialized, Radiation-Sensitive

**NIF heritage**: Fused silica lenses, potassium dihydrogen phosphate (KDP) frequency-conversion crystals, anti-reflection coatings. These are custom optics manufactured by a few specialized suppliers (Schott, Corning, Cleveland Crystals). NIF's 192 beamlines required ~7,500 large-aperture optics.

**Inertia scaling**: 1,000 beamlines × ~40 optics/beamline (typical for DPSSL) = ~40,000 custom optics. At 10 Hz with debris/radiation exposure, optics lifetime is a critical unknown. If optics must be replaced every 1,000–10,000 shots (conservatively, 100–1,000 seconds of operation), this implies continuous optics refurbishment.

**Supply-chain risk**: Large-aperture (30–40 cm) laser optics are low-volume, high-precision products. Scaling to 40,000 units + continuous replacement supply would require significant industry expansion.

## 5. Design Point Parameters

All parameters below describe the **Inertia Enterprises 1.5 GWe commercial plant** as stated in primary sources (website, ENR interview, press release). Values are at the native 1.5 GWe scale, not scaled to 1 GWe.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Fusion Architecture** |
| fusion_power_MW | ~6,750 MWth | [inferred: 450 MJ/shot × 10 Hz × 1.5 GWe ÷ 0.42 η_th − P_input] | medium | Informational only; `p_fus` is back-solved by 1costingFE from `p_input` + `P_native` |
| net_electric_MWe | 1,500 | inertia-website-technical.md (line 34: "1.5GW"); enr-mike-dunne-interview.md | high | Must equal `P_native`; spec key: drives module count at 1 GWe comparison |
| p_input_MW | ~100 | [inferred: 10 MJ laser at 10% eff = 100 MW avg; no aux heating] | medium | Spec key: `p_input` — laser wallplug power, not fusion power |
| **Driver Specifications** |
| laser_energy_MJ | 10.0 | globenewswire-series-a-press-release.md (line 29: "10 kJ beam"); inertia-website-technical.md (line 30: "10MJ Laser"); confirmed by 1000 beamlines × 10 kJ | high | Total laser energy delivered to target per shot |
| beamline_count | 1,000 | inertia-website-technical.md (line 45: "1000 Beamlines"); enr-mike-dunne-interview.md | high | Modular DPSSL architecture |
| beamline_energy_kJ | 10.0 | globenewswire-series-a-press-release.md (line 29: "10 kJ beam") | high | Thunderwall prototype spec |
| laser_efficiency_wallplug | 0.10 | globenewswire-series-a-press-release.md (line 29: "10% wallplug efficiency"); inertia-website-technical.md | high | Driver efficiency, not coupling efficiency |
| laser_wavelength_nm | 351 | [inferred: DPSSL 3ω UV typical for indirect drive; NIF uses 351 nm] | low | Not explicitly stated; inferred from NIF heritage and indirect-drive requirements |
| repetition_rate_Hz | 10.0 | inertia-website-technical.md (line 45: "10 targets per second"); enr-mike-dunne-interview.md ("10 times per second"); globenewswire-series-a-press-release.md | high | Spec key: `rep_rate` for IFE archetype |
| **Target and Gain** |
| target_gain_capsule | 30 | enr-mike-dunne-interview.md (">30 times input-output power ratio" for grid-scale plant) | medium | Capsule gain (fusion energy / laser energy on target), not engineering Q |
| target_gain_pilot | 18 | enr-mike-dunne-interview.md ("18 times output vs. input energy" for pilot plant) | medium | Lower gain at 50 MWe pilot scale; grid plant requires >30× |
| fusion_yield_per_shot_MJ | 450 | inertia-website-technical.md (line 32: "4.5x higher energy than NIF"); NIF ignition ~100 MJ → 450 MJ | medium | Fusion energy release per target implosion; drives chamber design |
| hohlraum_material | Lead (Pb) | [inferred: cost-reduction substitute for NIF's gold hohlraums] | medium | Not explicitly stated; lead chosen for cost vs. gold ($2k/kg vs. $60k/kg) |
| target_cost_USD | <1.0 | inertia-website-technical.md (line 28: "Less than $1 per target") | low | Company claim; 3 orders of magnitude below current NIF target costs (~$50k+); unvalidated |
| target_type | Hybrid-E indirect drive (D-T capsule in hohlraum) | enr-mike-dunne-interview.md; dossier.md (Kritcher heritage) | high | Annie Kritcher's NIF ignition design; low-gas-fill hohlraum, high-density carbon ablator |
| **Blanket and Breeding** |
| blanket_type | Liquid lithium (flowing, integrated tritium breeding) | inertia-website-technical.md FAQ ("lining the fusion chamber with pipes full of liquid lithium") | high | Spec key: `blanket_config` → `Liquid metal` |
| tritium_inventory_kg | ~0.2–0.5 | [inferred: "hundreds of grams" per FAQ vs. "20× more for tokamaks"] | low | Startup inventory; much lower than tokamak due to minimal plasma-facing tritium |
| Li6_enrichment | >0.90 | [inferred: required for TBR >1 in lithium blanket] | medium | Not stated; standard assumption for liquid Li breeding blankets |
| lithium_inventory_tonnes | ~500–1,000 | [analogue: LIFE blanket studies for GW-scale plant] | low | Chamber + piping + heat exchanger inventory; website mentions "~20 EV battery equivalents per year" (~1.5 tonnes) as makeup, not total inventory |
| **Thermal Conversion** |
| thermal_efficiency | 0.42 | [analogue: LIFE Rankine cycle studies; standard for steam plants] | medium | Website mentions "steam turbines"; no cycle details; LIFE assumed 42%; spec key: `eta_th` |
| thermal_power_MW | ~3,570 | [inferred: 1,500 MWe ÷ 0.42 − 100 MW recirc ≈ 3,570 MWth after accounting for recirc] | medium | Average thermal power delivered to balance of plant |
| cooling_system | Wet cooling towers (assumed) | [inferred: standard for GW-scale thermal plants] | low | Not stated; waste heat ~2,070 MW at 42% efficiency |
| **Performance and Availability** |
| capacity_factor | 0.75 | [estimated: website implies >0.95 with "0s dwell between pulses," but this is implausible for FOAK plant] | low | Conservative estimate accounting for maintenance, beamline failures, target factory downtime |
| plant_lifetime_years | 30 | [assumed: standard for capital-intensive energy projects] | medium | Not stated; industry standard |
| scheduled_replacement_interval_years | 3–5 | inertia-website-technical.md ("Structural replacements every 3-5 years") | medium | Chamber first-wall and structural components; frequency is aggressive for 14.1 MeV neutron environment |
| **Fuel Cycle** |
| fuel | D-T | inertia-website-technical.md FAQ ("D-T at 150 million C") | high | Explicitly chosen over D-D for "3.5× higher energy yield and lower ignition temperature" |
| deuterium_consumption_kg_per_year | ~15 | [inferred: 10 Hz × 315M shots/yr × ~50 μg D per target] | low | Deuterium is cheap (~$1,000/kg); not a cost driver |
| tritium_breeding_ratio_TBR | >1.0 | [required: self-sufficiency for D-T fuel cycle] | medium | Not stated; mandatory for commercial D-T plant; liquid Li blanket must achieve this |
| **Chamber and Neutronics** |
| neutron_wall_loading_MW_m2 | [NOT ENOUGH DATA] | N/A | N/A | Chamber radius and geometry not disclosed; cannot compute NWL without chamber dimensions |
| chamber_clearing_time_ms | 100 | [inferred: 10 Hz = 100 ms cycle time] | low | Not stated; assumes near-instantaneous clearing to achieve 10 Hz; highly aggressive |
| first_wall_material | [NOT ENOUGH DATA] | N/A | N/A | Not disclosed; LIFE used ODS steel or W; liquid Li provides some shielding |
| **Comparison Basis** |
| pilot_plant_net_MWe | 50 | enr-mike-dunne-interview.md ("50 MWe net to the grid") | high | Initial DOE pilot plant; scales to >1 GWe over time |
| commercial_plant_target_year | 2030 | enr-mike-dunne-interview.md ("grid-scale power plant in 2030") | medium | Company projection; aggressive timeline given TRL levels |

### Notes on Missing Parameters

Several canonical spec keys for the IFE archetype cannot be populated from available sources:
- **Chamber geometry** (radius, wall thickness): Not disclosed. LIFE used ~5 m radius chambers; Inertia's design may differ.
- **Neutron wall loading**: Cannot compute without chamber dimensions.
- **First-wall material**: Not stated. Liquid lithium provides partial shielding but structural first wall is still required.
- **Cryogenic target specifications**: D-T ice layer thickness, capsule diameter, hohlraum dimensions not published.
- **Laser pulse shape**: NIF uses complex temporally-shaped pulses (pickets, main drive, coast phases). Inertia has not disclosed pulse-shaping strategy.

## 5b. Override Candidates

The per-account walkthrough was conducted against the canonical 1costingFE schema for the IFE DPSSL archetype. For each account, the question was: does the dossier name a company-grounded quantity, unit cost, or published dollar figure that lets me price this account better than the library default?

**Result**: **Zero enabled overrides**. The archetype-fit grade is High, predicting 0–4 overrides; the count of 0 falls within band.

**Rationale**: Inertia has not published quantitative cost data for any individual account. The available sources provide:
- High-level performance targets (1.5 GWe, 10 Hz, 10 MJ laser)
- Qualitative claims of cost reduction ("$700–$1,000/J" for laser, "<$1 per target")
- System integration philosophy (modular, factory-built, mass-manufactured)

None of these translate to accountable, evidence-backed departures from library defaults. Specifically:

**C220104 (Laser driver)**: The "$700–$1,000/J" figure appears on the website but has no provenance (no citation, no derivation, no link to component costs). It is lower than NIF heritage (~$18M per beamline ÷ 1.8 MJ ≈ $10,000/J) but higher than Xcimer's published NOAK target of $60–80/J. Without a breakdown (diode costs, optics costs, assembly costs, mass-manufacturing learning curve), this cannot be grounded as `direct` provenance. A `derived` override would require stating: diode cost $X/W × Y watts × Z learning rate factor + optics cost... — but the components are not disclosed. **No override proposed**.

**C220108 (Target factory)**: The "<$1 per target" claim is stated but not derived. NIF targets cost ~$50,000+ (mostly labor-intensive cryogenic layering and gold hohlraum fabrication). Inertia claims 3-order-of-magnitude cost reduction via mass manufacturing and lead substitution, but the arithmetic is not shown. A credible `derived` override would require: lead cost per hohlraum ($A) + D-T fill cost ($B) + cryogenic layering cost at scale ($C/target at 10 million units/year throughput, citing industrial cryogenic process analogues) + capsule ablator cost ($D) = $1. None of these are disclosed. **No override proposed**.

**C220107 (Pulsed-power capacitor bank)**: Not applicable to DPSSL laser architectures (capacitors are used in flashlamp-pumped or excimer lasers, not DPSSL). The library correctly assigns zero cost here for DPSSL. **No override proposed**.

**CAS27 (Special materials — lithium inventory)**: The FAQ mentions "~20 EV battery equivalents per year" for lithium consumption, which is **makeup**, not inventory. The initial blanket fill is ~500–1,000 tonnes (inferred from LIFE), worth ~$500M–$1B at commodity lithium prices (~$1,000/kg for battery-grade; fusion-grade metallic Li-6-enriched is higher). But the dossier does not publish this figure, so it is an analogue, not company-grounded. **No override proposed**.

**CAS70 (O&M)**: The website mentions "modular line-replaceable units" and "standard MTBF targets" for lasers but gives no staffing model, scheduled maintenance cost, or unplanned replacement rates. **No override proposed**.

**CAS80 (Fuel cost)**: Tritium breeding is mentioned ("hundreds of grams on-site") but no fuel cycle cost breakdown is given. The library handles D-T fuel via standard archetype defaults (tritium breeding in blanket, deuterium procurement). **No override proposed**.

All other accounts (C220101 blanket, C220102 shield, C220105 structure, C220106 vacuum, C220110 remote handling, C220111 installation, CAS21 buildings, CAS23 turbine, CAS24 electric plant, CAS26 heat rejection) have no company-published data.

**Disabled override for future reference** (if Inertia publishes validation):

```yaml
overrides:
  - account: C220104
    value: 8500.0  # $850/J midpoint of stated $700–1000/J range × 10 MJ = $8.5B
    enabled: false
    provenance: direct
    source: "inertia-website-technical.md (line 28, table); note: provenance currently UNGROUNDED — no component breakdown or derivation provided"
    rationale: |
      Website states "$700–$1,000/J" for laser cost. At 10 MJ total laser energy,
      this implies $7B–$10B driver cost. However, this figure has no stated basis
      (no diode cost, no optics cost, no learning curve citation). It is lower than
      NIF heritage (~$18M/beamline × 1000 = $18B for comparable beamline count, but
      NIF beamlines are 1.8 MJ each, not 10 kJ) and higher than Xcimer's $60–80/J
      NOAK target (which would be $600–800M). Until Inertia publishes a cost
      breakdown or supply-chain validation, this override remains disabled.
      If enabled, use midpoint $850/J → $8.5B.
```

**Summary**: The expected 0–4 override band for High archetype-fit is met with 0 enabled overrides. The concept is well-matched to the IFE DPSSL archetype, and the library's per-archetype defaults are the correct pricing basis until Inertia publishes detailed cost validation.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Laser driver detailed cost breakdown (diode costs, optics costs, assembly costs, learning curve vs. NIF heritage) | S1, S2.1 | proprietary | blocking | Request Inertia technical white paper or await Thunderwall prototype cost data |
| 2 | Target manufacturing cost validation (cryogenic layering at scale, lead hohlraum fabrication cost, production line CAPEX) | S1, S2.1 | proprietary | blocking | Target factory prototype results (Inertia building this per ENR interview but no data published) |
| 3 | Capsule gain scaling validation (10 MJ → 30× gain claim; simulation codes, convergence studies, sensitivity to target tolerances) | S2.2 | proprietary / not-yet-sourced | blocking | LLNL LIFE simulation studies may provide partial validation; Inertia's internal simulations are proprietary |
| 4 | Chamber clearing strategy and demonstration (debris management, FLiBe vapor clearing, 100 ms cycle time feasibility) | S2.3, S3.4 | truly-unknown | blocking | Experimental demonstration or detailed engineering study (does not exist publicly) |
| 5 | Final optics protection and lifetime (radiation damage, debris shielding, replacement schedule) | S2.3, S3.2 | truly-unknown | blocking | LIFE grazing-incidence mirror studies are closest analogue; no Inertia-specific design published |
| 6 | Capacity factor and maintenance schedule (beamline MTBF, target factory uptime, chamber component replacement intervals) | S2.4 | proprietary | important | Plant reliability model (does not exist for this concept) |
| 7 | Liquid lithium blanket detailed design (flow rates, pump power, tritium extraction rate, corrosion mitigation, structural materials) | S3.5, S4.4 | not-yet-sourced | important | LIFE lithium blanket studies (LLNL-TR-505441, 2011) provide partial basis; Inertia-specific design unpublished |
| 8 | Thermal conversion cycle specifications (Rankine vs. sCO2, turbine inlet temperature, condenser design for pulsed source) | S2.5, S5 | derivable | important | LIFE BOP studies assumed Rankine at 42%; can use as analogue with medium confidence |
| 9 | First-wall and chamber structural material (neutron damage tolerance, replacement interval, remote handling approach) | S3.4, S5 | not-yet-sourced | important | LIFE used ODS ferritic steel; Inertia chamber design unpublished |
| 10 | Semiconductor laser diode supply chain validation (volume production capacity, cost scaling to $0.007–0.02/W, MTBF at 10 Hz for 30 years) | S4.2 | proprietary | important | Inertia mentions partnerships with diode industry but specifics confidential; industry roadmaps (TRUMPF, II-VI Incorporated) may provide partial data |
| 11 | Tritium breeding ratio and neutronics (TBR calculation for liquid Li blanket, Li-6 enrichment level, neutron multiplier if needed) | S4.1, S5 | derivable | important | Can compute with MCNP/OpenMC if chamber geometry disclosed; Inertia has not published neutronics |
| 12 | Chamber geometry (radius, wall thickness, neutron wall loading) | S5 | proprietary | nice-to-have | Required for NWL calculation; LIFE used ~5 m radius; Inertia may differ |
| 13 | Laser pulse shaping strategy (temporal profile, picket pulses, energy distribution across hohlraum drive) | S5 | proprietary | nice-to-have | NIF Hybrid-E uses complex pulse shapes; Inertia's DPSSL fidelity to this profile determines gain; proprietary |
| 14 | Hohlraum and capsule dimensions (hohlraum cylinder dimensions, capsule radius, ablator thickness, ice layer specs) | S5 | proprietary | nice-to-have | Required for detailed target physics validation; Kritcher's NIF Hybrid-E published some parameters but Inertia's 10 MJ scaling unpublished |

### Gap Prioritization Summary

**Blocking gaps** (1–5): Without resolution, the LCOE model carries order-of-magnitude uncertainty in driver cost, target cost, gain, and feasibility of 10 Hz operation. These are the primary barriers to model confidence elevation.

**Important gaps** (6–11): These affect LCOE by 20–50% but can be bounded with analogues (LIFE studies, tokamak BOP, industrial supply chain projections). They should be closed for D2+ iteration but do not block D1+ model completion.

**Nice-to-have gaps** (12–14): These improve model fidelity (NWL calculation, pulse-shape optimization, target dimensions) but are not LCOE-critical at D1+ depth. They matter for detailed engineering validation (TRL progression) but not for comparative LCOE ranking.

## 7. Family-Delta vs Comparables

Inertia's design point is compared against the fixed comparables list:
- 17b-laser-icf-fast-ignition (Focused Energy)
- 26-laser-icf-indirect-drive (generic NIF-heritage)
- 31-laser-icf-oec-architecture (Blue Laser Fusion)
- 32-laser-icf-french-national (GenF Systems)
- 17a-laser-icf-hybrid-drive (Xcimer Energy)

### 7.1 vs. 17b Laser ICF Fast Ignition (Focused Energy)

**Confinement concept divergence**: Fast ignition separates compression (long-pulse driver laser) from ignition (short-pulse petawatt laser). Inertia uses **conventional indirect drive** (single DPSSL driver for both compression and ignition via hohlraum X-rays). This is a fundamental physics difference.

**Cost delta**:
- **Advantage (Inertia)**: Eliminates the petawatt short-pulse ignition laser, reducing driver complexity. Fast ignition requires maintaining two separate laser systems (compression + ignition) with independent pulse timing and targeting — higher capital cost and operational complexity.
- **Penalty (Inertia)**: Conventional indirect drive has lower coupling efficiency (~12% laser-to-capsule) vs. fast ignition's direct energy deposition into pre-compressed core (potentially >20% coupling). Lower coupling efficiency means Inertia requires higher laser energy for the same gain, increasing driver cost.
- **Magnitude**: LIFE studies showed fast ignition could reduce required laser energy by ~40% for the same yield. If Inertia's 10 MJ driver is priced at $7–10B (per website claim), a fast-ignition design at equivalent performance might require only 6 MJ → $4–6B driver, a **$3–4B capital cost advantage** for fast ignition. However, the petawatt laser subsystem adds back $500M–$1B, so net delta is ~$2–3B **in favor of fast ignition**.

**Shared**: Both are IFE, both are D-T, both require cryogenic target factories and high-rep-rate chamber clearing. Blanket, BOP, and tritium breeding are identical cost structures.

### 7.2 vs. 26 Laser ICF Indirect Drive (Generic NIF-heritage, e.g., Inertia Thunderwall)

This is **the same confinement concept**. Concept 26 in the handwritten exemplar appears to be a generic placeholder for NIF-derived indirect-drive commercialization. Inertia is a specific implementation of this generic category.

**Design point differences** (if concept 26 refers to a different implementation, e.g., LLNL LIFE):
- **Beamline count**: Inertia 1,000 beamlines vs. LIFE 384 beamlines. Inertia uses more, smaller beamlines for better fault tolerance (single beamline failure = 0.1% capacity loss vs. 0.26% for LIFE).
- **Laser energy**: Inertia 10 MJ total vs. LIFE 2.2 MJ. Inertia targets higher gain at higher energy.
- **Rep rate**: Inertia 10 Hz vs. LIFE 16 Hz. LIFE's faster rep rate implies more aggressive chamber clearing and target injection requirements.

**Cost delta**: Negligible if both use DPSSL at ~10% efficiency and indirect-drive hohlraums. The driver cost scales roughly with total laser energy ($/J × total MJ). The beamline count affects manufacturing economies of scale but not fundamental $/J if both achieve mass production.

### 7.3 vs. 31 Laser ICF OEC Architecture (Blue Laser Fusion)

**Driver divergence**: OEC (Optical Emission Control) architecture uses wavelength-shifted lasers (blue, 450 nm) for improved coupling and reduced laser-plasma instabilities vs. Inertia's UV (351 nm, inferred). The handwritten exemplar for concept 31 should clarify this, but assuming OEC is a driver-level innovation:

**Cost delta**:
- **Neutral or penalty (Inertia)**: UV frequency tripling (1ω → 3ω) via KDP crystals loses ~20% energy vs. direct blue emission. If OEC eliminates frequency conversion, it may achieve 10–15% higher driver efficiency, reducing required laser energy and capital cost.
- **Magnitude**: Unknown without OEC-specific data. If OEC's blue laser provides 15% efficiency vs. Inertia's 10%, Inertia's driver must be 50% larger (15/10 = 1.5×) for the same delivered energy → **~$3–5B penalty** at Inertia's stated $7–10B driver cost.

**Shared**: Indirect drive physics, hohlraum targets, thermal BOP, tritium breeding.

### 7.4 vs. 32 Laser ICF French National (GenF Systems)

Insufficient public data on GenF's specific architecture to quantify delta. Assuming GenF also uses indirect-drive DPSSL (based on concept name "French National" implying CEA/LLNL collaboration heritage):

**Cost delta**: Likely **neutral**. Both are state-backed or well-funded NIF-derivative programs with access to similar technology bases. Differences would be in specific engineering choices (beamline architecture, target factory approach, chamber design) rather than fundamental physics.

**Potential divergence**: If GenF uses LMJ (Laser Mégajoule, France's NIF-equivalent) heritage, it may use flashlamp-pumped lasers instead of DPSSL, which would give Inertia a **large efficiency advantage** (10% vs. <1%), translating to ~10× smaller driver for the same delivered energy → **multi-billion-dollar advantage for Inertia**. However, this assumes GenF has not transitioned to DPSSL, which is speculative.

### 7.5 vs. 17a Laser ICF Hybrid Drive (Xcimer Energy)

**Driver and fuel divergence**: Xcimer uses **KrF excimer lasers** (248 nm deep-UV, gas-based) at ~7% efficiency vs. Inertia's **DPSSL** (solid-state diodes) at 10% efficiency. Xcimer uses **hybrid direct-drive** (brief hohlraum X-ray pulse for plasma formation, then 2-beam direct capsule ablation) vs. Inertia's pure **indirect drive**.

**Cost delta**:
- **Advantage (Inertia, driver efficiency)**: 10% DPSSL vs. 7% excimer means Inertia's recirculating power is 30% lower for the same laser energy delivered. At GW scale, this is ~30 MW less recirculating load → ~$30–50M lower in electric plant equipment (CAS24) and transformer capacity.
- **Penalty (Inertia, laser capital cost)**: Xcimer's published NOAK target is $60–80/J for KrF excimer systems (per handwritten exemplar for concept 26, citing Xcimer/TRUMPF whitepaper). Inertia's website claims $700–$1,000/J. If both figures are credible, **Inertia's driver is 10× more expensive** ($7–10B vs. $600–800M for a 10 MJ system). This is the **dominant delta** in the comparison.
- **Advantage (Xcimer, coupling efficiency)**: Hybrid direct drive achieves >50% laser-to-capsule coupling (per exemplar, citing Xcimer data) vs. Inertia's ~12% indirect-drive coupling. This means Xcimer requires **4× less laser energy** for the same fusion yield. At Xcimer's $60–80/J, a 2.5 MJ Xcimer driver (equivalent to 10 MJ Inertia in delivered energy) costs $150–200M, vs. Inertia's $7–10B → **Xcimer has a $7–10B driver cost advantage**.

**Magnitude of total delta**: Xcimer's combination of lower $/J and higher coupling efficiency creates an **order-of-magnitude capital cost advantage** in the driver account (C220104), which is the single largest LCOE driver for IFE. This advantage is partially offset by:
- Xcimer's slower rep rate (0.25–1 Hz vs. Inertia's 10 Hz) requires 10× higher yield per shot for the same average power, increasing chamber size and structural costs.
- KrF excimer's gas gain medium and large aperture optics may have higher per-shot operating costs than DPSSL's solid-state modularity.

**Verdict**: Xcimer likely has **significantly lower LCOE** than Inertia if both concepts achieve their stated performance. The driver cost gap is too large for Inertia's higher rep rate and modular manufacturing to overcome.

### 7.6 Shared Costs Across All Laser ICF Comparables

The following accounts are **architecturally identical** across all comparables and Inertia:
- **C220101 (Blanket)**: D-T breeding blanket (FLiBe or liquid Li) — shared cost structure.
- **C220102 (Shield)**: 14.1 MeV neutron shielding — scales with chamber size and NWL, but physics is identical.
- **C220108 (Target factory)**: Cryogenic D-T capsule + hohlraum manufacturing — shared challenge, though Inertia claims <$1/target vs. others' unspecified costs.
- **CAS23 (Turbine plant)**: Thermal Rankine cycle — identical for all thermal-conversion IFE.
- **CAS27 (Special materials)**: Tritium startup inventory, Li-6 enrichment — shared constraint.
- **CAS70/80 (O&M and fuel)**: Staffing, scheduled maintenance, D-T fuel cycle — differences are in details (laser maintenance, target QA) but not fundamental structure.

**Key takeaway**: The LCOE spread among laser ICF concepts is driven almost entirely by **driver technology choices** (DPSSL vs. excimer vs. flashlamp; efficiency; $/J) and **target coupling efficiency** (indirect vs. direct vs. hybrid drive). Chamber, blanket, and BOP are second-order differentiators.

## 8. Sources

Listed in order of importance to the analysis:

1. **ENR Mike Dunne Interview** — "Ten Minutes With: Mike Dunne, Co-Founder and CTO of Fusion Power Startup Inertia Enterprises" (Engineering News-Record, date unknown but post-Feb 2026 Series A)
   - Saved: `knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/enr-mike-dunne-interview.md`
   - **Contribution**: Primary source for plant-scale performance targets (1.5 GW, 50 MWe pilot, 10 Hz, 18× and >30× gain claims), supply-chain strategy (diode partnerships), technical risks (system integration), and commercialization timeline (2030 grid-scale plant). Most quantitative LCOE-relevant parameters in Section 5 trace to this interview.
   - **Limitations**: High-level discussion; no cost breakdowns, no detailed subsystem specifications, no chamber or blanket design details.

2. **Inertia Enterprises Website Technical Pages** — https://inertia.com/ (FAQ and technical overview sections)
   - Saved: `knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/inertia-website-technical.md`
   - **Contribution**: Key architectural specifications (1,000 beamlines, 10 MJ laser, 4.5× NIF energy per shot, liquid lithium blanket description, "<$1 per target" claim, zero-emissions branding). Provides the "factory-built, truck-deliverable" modularity framing.
   - **Limitations**: Marketing-focused content; no engineering drawings, no cost derivations, no validation data. The "$700–$1,000/J" laser cost claim has no stated provenance.

3. **GlobeNewsWire Series A Press Release** (February 11, 2026) — "Inertia raises $450 million to commercialize the only proven fusion science"
   - Saved: `knowledge/concept_research/30-laser-icf-nif-commercialization/iter-01/sources/globenewswire-series-a-press-release.md`
   - **Contribution**: Thunderwall prototype laser specifications (10 kJ, 10 Hz, 10% wallplug efficiency), company founding narrative (Kritcher + Dunne + Lawson), and funding scale ($450M Series A). Confirms the "50× more powerful in average power" claim vs. prior DPSSL lasers.
   - **Limitations**: Press release genre; no technical depth beyond single-beamline prototype specs.

4. **LLNL LIFE Program Studies** (2008–2013) — Laser Inertial Fusion Energy conceptual design
   - **Key documents**:
     - Dunne et al., "Timely Delivery of Laser Inertial Fusion Energy (LIFE)" (LLNL-JRNL-438170, 2010)
     - Abbott et al., "LIFE Plant Conceptual Design," Fusion Science and Technology 60 (2011)
     - Moses et al., "A Sustainable Nuclear Fuel Cycle Based on Laser Inertial Fusion-Fission Energy (LIFE)," Fusion Science and Technology 56 (2009)
   - **Contribution**: Architectural heritage for Inertia's design. LIFE defined the DPSSL IFE power plant concept (384 beamlines, 2.2 MJ, 16 Hz, liquid lithium or FLiBe blanket, Rankine cycle BOP). Provides cost structure analogues for accounts where Inertia has not published data (blanket inventory, BOP efficiency, chamber dimensions).
   - **Limitations**: LIFE was terminated before hardware demonstration. Its cost estimates are 2010-era and based on different beamline count and energy. Inertia's architecture has evolved (1,000 beamlines, 10 MJ, 10 Hz), so LIFE is an analogue, not a direct source.
   - **Access**: LLNL technical reports available via OSTI.gov and LLNL publication database.

5. **NIF Ignition Experimental Results** — Annie Kritcher's Hybrid-E target design
   - **Key paper**: Kritcher et al., "Design of an Inertial Fusion Experiment Exceeding the Lawson Criterion for Ignition," Physical Review E 106, 025201 (2022)
   - **Contribution**: Physics validation for the Hybrid-E target design Inertia inherits. Demonstrates ignition at ~2 MJ laser energy with low-gas-fill hohlraum and high-density carbon ablator. Establishes the empirical basis for Inertia's gain claims, though NIF experiments were single-shot, not 10 Hz.
   - **Limitations**: NIF operates at 0.1% efficiency with flashlamp lasers. The translation to DPSSL at 10% efficiency and 10 Hz rep rate is an engineering extrapolation, not a demonstrated capability.

6. **Dossier** — `knowledge/concept_research/30-laser-icf-nif-commercialization/dossier.md`
   - **Contribution**: Structured summary of Inertia's differentiation table values (confinement family IFE, indirect drive, D-T fuel, DPSSL driver, etc.) with confidence ratings. Consolidates the three primary sources above into a single reference.
   - **Limitations**: Dossier is a derivative document; all claims trace back to the website, interview, and press release — it adds no new data.

7. **Handwritten Exemplar: Concept 26 Laser ICF Indirect Drive**
   - **Path**: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\26-laser-icf-indirect-drive.md`
   - **Contribution**: Comparative cost data for laser ICF concepts (Xcimer's $60–80/J NOAK target, target cost constraints per Goodin et al. 2004, LIFE's FLiBe inventory estimates). Provides cross-concept context for Inertia's claims and identifies which cost figures are outliers (e.g., Inertia's "$700–$1,000/J" is 10× higher than Xcimer's published target).
   - **Limitations**: Exemplar is not a primary source for Inertia; it documents other IFE concepts (Xcimer, LIFE) and is used here only for analogy and sanity-checking.

8. **Schema** — `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\phase_1a\schema.md`
   - **Contribution**: Controlled vocabulary for differentiation table columns (confinement family, fuel, blanket config, etc.). Ensures consistent terminology across the corpus.
   - **Limitations**: Definitional document; not a data source for Inertia's design.

**Sources NOT cited but relevant for future iterations**:
- **LLNL GEM (Generalized Economics Model)**: Excel-based LCOE tool for DPSSL laser ICF. May contain cost scaling relationships not available in narrative LIFE reports.
- **Goodin et al. (2004)**: "Developing a commercial production process for 500,000 targets per day..." — target factory cost constraints (<10% of electricity yield per target).
- **Haefner et al. (2023)**: LLNL/TRUMPF study on diode cost requirements ($0.007/W target for IFE viability). Cited in handwritten exemplar; not directly accessed for this iteration.

**Missing sources** (data gaps):
- No peer-reviewed publications from Inertia Enterprises on Thunderwall laser, chamber design, target manufacturing, or plant-level cost estimates.
- No independent techno-economic analysis of Inertia's architecture by third parties (LLNL, DOE, academic groups).
- No neutronics simulations or chamber clearing demonstrations for the 10 Hz architecture.