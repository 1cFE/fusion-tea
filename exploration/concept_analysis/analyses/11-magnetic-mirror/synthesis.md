---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Type: synthesis
Status: draft
Created: 2026-05-13
---

## 1. Executive Summary

- **Single most important risk**: End-plug confinement physics at Q > 5 has never been experimentally validated. The tandem mirror economic case rests entirely on hot, dense end-plug plasmas creating electrostatic barriers deep enough to confine the main cell at commercial Q. DCLC instability management via sloshing ions and vortex flows is computationally modeled but undemonstrated. If end-plug physics underperforms by 50% (Q = 5 degrades to Q = 2.5), recirculating power doubles and net electricity production vanishes at pilot scale.

- **Single most important advantage**: Linear scaling of fusion power with center-cell length at roughly constant input power. If Realta's ~7 MW/m thesis holds, longer machines approach arbitrarily high Q without proportional increases in end-plug heating costs. This is a structural economic advantage no toroidal concept can claim — tokamaks and stellarators face minimum-size ignition thresholds that create diseconomies below ~500 MWe.

- **LCOE ballpark**: 95.4 $/MWh at 500 MWe (67.0 $/MWh scaled to 1 GW). The model uses MARS 1983 analogues for blanket (LiPb, TBR 1.15, η_th = 0.36) and DEC (venetian blinds, η_de = 0.54) because Realta has published no plant-level engineering data. The 95 $/MWh figure is an order-of-magnitude structural estimate with ±40% uncertainty.

- **Confidence verdict**: Low. Physics parameters (Q > 5 at 50 m, end-plug stability) are modeled not demonstrated. Engineering parameters (blanket type, thermal cycle, recirculating power fraction) are undisclosed. Capital costs are framework defaults across all CAS accounts — Realta has published zero subsystem cost estimates. The 40 MW heating power assumption carries 2.5× uncertainty (handwritten model used 40 MW, automated used 100 MW). The LCOE estimate is credible as a first-pass analogue but cannot be validated against Realta data until the 2026 Hammir design paper appears.

---

## 2. What Matters Most for LCOE

### 1. Availability (elasticity: -0.89)
- **Assumed value**: 85%
- **Source**: No published target. Framework default for steady-state D-T MFE. DEC electrode survivability under continuous D-T exhaust bombardment is unknown — thin uncooled electrodes downstream of a 2 GW fusion reactor have never been tested. Electrode replacement frequency drives availability.
- **Sensitivity magnitude**: A 10% increase in availability (85% → 93.5%) cuts LCOE by 8.9%. This is the dominant economic lever.
- **What would flip the conclusion**: If DEC electrodes require replacement every 6 months (forcing 2–3 week outages for hot-cell operations along the full 70 m machine length), availability falls to 75% and LCOE rises to ~110 $/MWh at 500 MWe. Conversely, if electrodes survive 3+ years between replacements, availability reaches 90%+ and LCOE drops toward 85 $/MWh. DEC electrode lifetime is a blocking gap flagged in the analysis with no experimental data.

### 2. Interest rate (elasticity: +0.59)
- **Assumed value**: 7%
- **Source**: Framework default for project finance.
- **Sensitivity magnitude**: A 1 percentage point increase (7% → 8%) raises LCOE by ~6 $/MWh. Standard financial leverage for capital-intensive projects.
- **What would flip the conclusion**: If the linear scaling thesis proves out and Realta achieves capital cost 30% below tokamak baselines (via simplified center-cell geometry and outboard-only DEC), low-cost capital at 4–5% (government-backed loans for clean energy) could push LCOE below 75 $/MWh at 1 GW scale. Conversely, if the concept is perceived as high-risk and debt costs rise to 10%, LCOE exceeds 80 $/MWh at 1 GW even with favorable physics. The WHAM operational track record and Anvil end-plug validation (2028) will determine financing terms.

### 3. Chamber length (elasticity: +0.27)
- **Assumed value**: 70 m (commercial extrapolation from 50 m Hammir pilot)
- **Source**: arXiv 2411.06644 cites Q > 5 at 50 m, Q > 10 "with longer center cell" (length unspecified). The 70 m commercial design is extrapolated to produce ~490 MWt fusion power at ~7 MW/m. This is an engineering choice not a physics constraint.
- **Sensitivity magnitude**: A 10% increase in center-cell length (70 → 77 m) raises LCOE by 2.7%. This is non-intuitive — shouldn't longer cells improve Q and lower LCOE? The +0.27 elasticity reflects that building, blanket, and magnet costs scale with length while fusion power scales linearly. The Q improvement from 70 → 77 m is modest (Q ~ 10 → Q ~ 11 at constant input power) and does not offset the capital cost growth.
- **What would flip the conclusion**: The LCOE-optimal center-cell length depends on the uncosted center-cell cost structure. If solenoid magnets and blanket modules are cheap (factory-manufactured, learning-curve benefits), longer is better and the optimum may be 100+ meters. If per-meter costs are high (stick-built assembly, neutron shielding drives up coil radius), the optimum is shorter and 50–60 m may be preferred. MARS found LCOE saturation near 600 MWe (1983 technology), implying an optimal length exists. Without Realta's cost-per-meter data, the 70 m choice is speculative.

### 4. Thermal efficiency η_th (elasticity: -0.23)
- **Assumed value**: 36% (MARS 1983 steam Rankine analogue). Model updated to 55% per canonical η_th for Hybrid (thermal + direct) per scoring framework.
- **Source**: MARS study. Actual Hammir thermal cycle undisclosed. sCO2 Brayton could reach 40–45% if Realta commits to an advanced cycle. Blanket type (FLiBe, LiPb, liquid Li, HCPB) determines outlet temperature and cycle efficiency.
- **Sensitivity magnitude**: A 3 percentage point improvement (36% → 39%, achievable with sCO2 at 700°C FLiBe outlet) cuts LCOE by ~2%. This is modest but achievable.
- **What would flip the conclusion**: If the undisclosed blanket type forces a low-temperature outlet (LiPb at 350°C → saturated steam at 30% efficiency), LCOE rises by 5–7%. Above 45% is implausible for a D-T thermal cycle without exotic direct energy conversion. The 36% MARS baseline is defensible but carries ±3 percentage point uncertainty tied to the blanket/cycle choice.

### 5. Blanket unit cost (elasticity: +0.18)
- **Assumed value**: Framework default D-T blanket cost (0.60 M$/m³ for LiPb breeding blanket)
- **Source**: No published cost data. The cylindrical axisymmetric center-cell geometry is well-suited to annular blanket modules (conceptually simpler than tokamak saddle-coil-shaped modules). MARS used LiPb, TBR 1.15. Realta's blanket type is undisclosed.
- **Sensitivity magnitude**: Blanket is CAS22 sub-account C220103 at ~$205M. A 10% increase in unit cost raises LCOE by 1.8%.
- **What would flip the conclusion**: If the axisymmetric geometry reduces fabrication complexity by 20–30% vs. tokamak blankets (annular modules are easier to manufacture than 3D-curved modules), blanket cost could fall 20% and LCOE drops ~3.5%. Conversely, if the undisclosed blanket type is FLiBe (requiring BeF₂ chemistry and higher-T materials), costs could exceed framework defaults by 30% and LCOE rises ~5%. The linear geometry is a manufacturing advantage, but material choice drives absolute cost.

---

## 3. Risk Verdicts

### Challenge 1: End-plug confinement at Q > 5 (analysis Section 2, Challenge 1)
- **Verdict**: Genuinely uncertain
- **Rationale**: The arXiv paper models Q = 5.8 at 50 m using machine learning optimization for end-plug stability, explicitly acknowledging "stabilization against MHD and trapped particle modes" is required. DCLC and AIC modes must be suppressed via sloshing ions and vortex flows — techniques demonstrated in 1980s TMX at sub-commercial conditions but never at the density, temperature, and field strength required for Q > 5. The Anvil device (2028) is the first dedicated end-plug confinement demonstrator. If DCLC management is 50% less effective than modeled, Q = 5 degrades to Q = 2.5 and the recirculating fraction rises from ~35% to >50%, eliminating net electricity at pilot scale.
- **What would retire this risk**: Anvil end-plug validation at 10+ T mirror ratio, demonstrating stable electrostatic plugging potential at densities and temperatures consistent with Q > 5 main-cell confinement. Alternatively, WHAM extending its current operations to achieve sustained end-plug confinement with measured plugging potential > 5 kV would provide strong evidence. The risk cannot be retired by simulation alone — DCLC is a kinetic instability that requires experimental validation.

### Challenge 2: Linear scaling thesis is uncosted (analysis Section 2, Challenge 2)
- **Verdict**: Likely resolvable but economically uncertain
- **Rationale**: The physics claim (~7 MW/m at constant input power) is consistent with the arXiv scaling analysis and plausible on first principles — end-plug power dominates, center-cell transport is classical. However, the cost per meter of center cell (magnets, blanket, building, structure) is unestimated in any modern study. MARS costed its full 100 m device but used copper coils, yin-yang geometry, and 1983 construction costs. If center-cell solenoids are factory-manufactured REBCO modules with learning-curve cost reduction, the linear scaling thesis translates to favorable LCOE scaling. If per-meter costs are high (stick-built assembly, neutron shielding expands coil radius), the advantage evaporates.
- **What would retire this risk**: A published cost breakdown for Hammir (expected 2026 design paper) with CAS-level estimates for magnets, blanket, and building scaled per meter. If the 2026 paper provides a cost-per-meter estimate of $5–10M/m (magnet + blanket + structure), the linear scaling thesis becomes economically credible. If cost-per-meter exceeds $15M/m, the concept loses its scaling advantage and LCOE remains flat or rises with machine size.

### Challenge 3: Recirculating power fraction is unknown (analysis Section 2, Challenge 3)
- **Verdict**: Likely resolvable
- **Rationale**: The model assumes 40 MW input power (arXiv-anchored: 30–40 MW for 50 m pilot; commercial extrapolation assumes constant end-plug power). This produces Q_eng = 4.4 and recirculating fraction 22.7% — manageable for net electricity production. However, the handwritten exemplar used 40 MW and the automated pipeline used 100 MW — a 2.5× spread. If the true commercial Hammir requirement is 70–100 MW (end-plug sustainment proves more power-hungry than modeled), Q_eng falls to 3–4 and recirculating fraction rises to 35–40%, cutting net output by 50–100 MWe and raising LCOE by 15–20%.
- **What would retire this risk**: Publication of the NBI + ECH input power requirement for Hammir in the 2026 design paper. Alternatively, Anvil experimental validation of end-plug sustainment power at commercial density/temperature would bound the requirement. If Anvil confirms end-plug heating power scales favorably (30–40 MW for Q > 5), the recirculating power risk retires. If Anvil requires 60–80 MW to maintain plugging potential, the risk materializes and LCOE rises.

### Challenge 4: DEC contribution is real but modest for D-T (analysis Section 2, Challenge 4)
- **Verdict**: Likely resolvable but economically marginal
- **Rationale**: D-T fusion produces 80% neutron energy (14.1 MeV) captured in the thermal blanket and 20% alpha energy (3.5 MeV) potentially capturable by DEC. At 54% DEC efficiency (MARS historical value), the electrical contribution is 0.20 × 0.54 ≈ 11% of thermal output. This is meaningful but not transformative. The model includes DEC (η_de = 0.54, f_dec = 0.20) and shows -0.007 elasticity — excluding DEC entirely would raise LCOE by <1%. The handwritten exemplar's dismissal of DEC as "not worth considering" overstates the case (11% is real), but its concern about thin uncooled electrodes surviving continuous D-T exhaust bombardment is valid and unaddressed in Realta publications.
- **What would retire this risk**: Experimental demonstration of venetian blind DEC at fusion-relevant charged-particle flux (even in a non-D-T environment like deuterium beam testing) would validate electrode survivability. If electrodes survive multi-month continuous operation at kW/m² flux levels, DEC becomes a credible 10% LCOE improvement. If electrodes degrade within weeks, DEC is operationally infeasible and LCOE rises ~1%. This is not a concept-gating risk — the concept works without DEC, just at slightly higher LCOE.

### Challenge 5: Tritium breeding blanket type undisclosed, TBR unverified (analysis Section 2, Challenge 5)
- **Verdict**: Likely resolvable but TBR validation is a mandatory gate
- **Rationale**: Realta confirms a lithium-based blanket but does not disclose the type (FLiBe, LiPb, liquid Li, HCPB). This matters for TBR, thermal efficiency, and cost. MARS achieved TBR 1.15 with LiPb in a yin-yang geometry. Realta's cylindrical center cell with axisymmetric blanket is geometrically favorable for TBR — no complex 3D shaping, full 2π coverage. If the blanket is FLiBe with beryllium multiplication, TBR > 1.2 is plausible. If it's HCPB (solid ceramic), TBR margins are tighter and Li-6 enrichment may be required.
- **What would retire this risk**: Neutronics validation showing TBR > 1.05 for the Hammir geometry with realistic port fractions (15–20% of surface allocated to NBI, diagnostics, access). The 2026 Hammir design paper is expected to include neutronics. If TBR falls below 1.0 with realistic penetrations, the concept requires external tritium supply (economically non-viable) or a blanket redesign that increases R0 and capital cost.

### Challenge 6: Center stack durability under neutron irradiation (implicit in analysis Section 3)
- **Verdict**: Genuinely uncertain
- **Rationale**: The axisymmetric mirror has no center stack (unlike spherical tokamaks) — the open-ended geometry terminates at the DEC electrodes, not a neutron-shielded central column. However, the end-mirror HTS coils face direct neutron exposure from the end-loss cones. The analysis does not quantify neutron flux into the end-mirror magnets or address shielding requirements. If 14 MeV neutron flux into the end-mirror REBCO coils exceeds ~10¹⁸ n/m² integrated over 5–10 FPY, REBCO critical current degrades and the end magnets require replacement. Replacement of the end-mirror magnets (17 T HTS solenoids, $50M in REBCO tape for WHAM scale) is a multi-month maintenance event.
- **What would retire this risk**: Neutronics modeling of the end-mirror neutron flux and published shielding design for the Hammir geometry. If the end-loss cones can be shielded to <10¹⁷ n/m² s⁻¹ with reasonable shield thickness (30–40 cm), the magnets survive 10+ FPY. If shielding is inadequate and flux exceeds 10¹⁸ n/m² s⁻¹, magnet lifetime is 5–7 FPY and replacement frequency becomes a major availability and cost driver. This is a genuine uncertainty unaddressed in available Realta sources.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. conventional D-T tokamak baseline

**Eliminates ~15–20% of direct capital by removing divertor strike-point complexity**
The open-ended mirror geometry creates natural loss cones at the ends — escaping plasma flows directly to the DEC electrodes and end vacuum pumps. There is no divertor strike point with 50–100 MW/m² parallel heat flux requiring detachment control, seeded impurities, and tungsten monoblock engineering. The DEC electrodes face lower heat flux (alphas are magnetically expanded before collection) and operate at ~1–5 MW/m² — manageable without active cooling. The model shows divertor base cost (C220104) at $282M in CAS22, but this is a framework default for D-T tokamaks. The mirror divertor is fundamentally simpler. If the true mirror "divertor" (end structures + DEC) costs 50% less than a tokamak divertor, total capital falls $140M and LCOE drops ~3–4%.

**Linear geometry enables factory-manufactured center-cell modules**
The cylindrical solenoid coils and annular blanket modules are geometrically simpler than tokamak saddle coils or stellarator 3D non-planar coils. The center cell can be segmented into 10–20 m modules (solenoid + blanket + structure) that are factory-assembled, shipped, and site-integrated. This is not full modularization (the modules are not drop-in replaceable like a laser IFE target factory), but it's a manufacturing advantage over stick-built toroidal coils. C1 modularization score is 2.3 — worse than laser IFE (3.5–4.0) but better than large stellarators (1.5–2.0). If factory learning curves reduce per-module cost by 20–30% over the first 10 plants (analogous to wind turbine nacelle learning), LCOE drops 5–10%.

**No disruptions eliminates a major tokamak risk category**
Magnetic mirrors have no plasma current and therefore no disruptions. This removes: (a) disruption-induced halo currents and electromagnetic loads on structure, (b) thermal quench heat spikes on first wall, (c) runaway electron damage risk, (d) disruption prediction and mitigation systems (shattered pellet injection, massive gas injection). The tokamak must budget for disruption-hardened first walls, real-time disruption avoidance, and conservative operational limits to stay away from disruption boundaries. The mirror operates without these constraints. This is a qualitative safety and operational advantage that reduces R&D cost and accelerates licensing, but it is not directly quantified in the LCOE model.

### Disadvantages vs. conventional D-T tokamak baseline

**End-plug physics is undemonstrated at commercial Q — adds ~30% uncertainty to Q_eng**
Tokamaks benefit from 70+ years of confinement physics validation across 100+ machines (JET, TFTR, JT-60U, DIII-D, EAST, WEST, ASDEX-U, etc.). Burning plasma physics is validated at JET (16 MW D-T, 1997) and will be validated at ITER (2030s). The magnetic mirror has TMX (1980s, decommissioned), MFTF-B (canceled before operation), and WHAM (first plasma July 2024, sub-commercial). The tandem mirror end-plug physics required for Q > 5 has never been demonstrated. The arXiv paper models Q = 5.8 but explicitly flags stability as a development requirement. If end-plug physics proves 30–50% less effective than modeled (a plausible outcome given the lack of experimental validation), Q degrades from ~10 to ~5–7 and LCOE rises 10–15%.

**DEC adds operational complexity and uncharacterized maintenance cost**
The venetian blind DEC is a novel subsystem not present in tokamaks. It requires: (a) thin electrodes with large surface area exposed to the end-loss plasma, (b) high-voltage biasing (10s of kV) to separate ions by energy, (c) vacuum compatibility and neutron/gamma survivability, (d) remote handling for electrode replacement in an activated environment. DEC electrode lifetime under continuous D-T exhaust bombardment is unknown — this is flagged as a blocking gap in the analysis. If electrodes require replacement every 6–12 months, the maintenance burden is substantial and availability falls. The model assumes 85% availability but provides no electrode replacement schedule. If DEC maintenance drives availability to 75%, LCOE rises ~12%.

**Recirculating power fraction is higher than advanced tokamaks due to steady-state heating**
The mirror requires continuous NBI + ECH to sustain the end plugs. The model assumes 40 MW input power, producing Q_eng = 4.4 and recirculating fraction 22.7%. Advanced tokamaks like ARC target Q_eng ~ 6–8 with pulsed heating (NBI during ramp-up only, self-heated burn phase). The steady-state mirror cannot self-heat — it requires external heating at all times. If commercial Hammir requires 60–80 MW (end-plug sustainment proves more demanding), Q_eng falls to 3.5–4.0 and recirculating fraction rises to 30–35%. This is still net-positive but worse than self-heated tokamaks. The model shows p_input elasticity of +0.05 — a 50% increase in heating power (40 → 60 MW) raises LCOE by ~2.5%.

**Gyrotron capital and operating costs are substantial and scale with machine size**
The 40 MW ECRH requirement (model assumption) requires 30–40× 1 MW CW gyrotrons at ~$1M/MW capital cost. This is $30–40M in gyrotrons alone, not including power supplies, waveguides, and launchers. NBI adds another $40M (heating_nbi_per_mw scaling). Total heating system cost is ~$80M in the model (C220200). If commercial Hammir requires 80 MW (2× the model assumption), heating system cost doubles to ~$160M and LCOE rises ~2%. Tokamaks with self-heated burn phases avoid this scaling penalty — heating systems are sized for ramp-up only, not steady-state operation.

**Unknown fusion power and Q leave LCOE validation impossible until Hammir data is published**
This is the overriding disadvantage. The model produces 95.4 $/MWh from MARS analogues and arXiv pilot physics, but Realta has published no cost data, no recirculating power fraction, no blanket specification, and no capital cost breakdown. The 40 MW heating power assumption carries 2.5× uncertainty. The Q_eng = 4.4 is a back-solved consistency check, not a physics anchor. Until Realta publishes the 2026 Hammir design paper with engineering parameters and performance targets, the LCOE estimate is a placeholder with ±40% error bars.

---

## 5. Cross-Concept Positioning

**Shares linear scaling economics with laser IFE — but mirror has unproven physics where IFE has proven ignition**
Both concepts scale output by replicating modular units: laser IFE adds target chambers and driver beamlines; magnetic mirror adds center-cell meters. Both claim to avoid the minimum-size ignition threshold that constrains tokamaks. However, laser IFE demonstrated ignition at NIF (3.15 MJ, December 2022) and the target physics is validated. Magnetic mirror end-plug physics at Q > 5 has never been demonstrated. The mirror's physics risk is higher; its operational risk is lower (steady-state plasma vs. 10 Hz target implosions with debris clearing). LCOE comparison depends on whether end-plug physics validates — if it does, the mirror's steady-state operation is an advantage; if it doesn't, the concept fails where IFE has succeeded.

**Shares HTS magnet supply chain with compact tokamaks (CFS, Tokamak Energy) — creates bottleneck competition**
All HTS fusion concepts depend on REBCO tape from the same thin global supply chain (CFS, Shanghai Superconductor, Faraday Factory Japan). Realta's WHAM required $50M in REBCO tape from CFS for two 17 T end-mirror magnets. A 70 m commercial Hammir with 10–15 center-cell solenoid modules plus two end mirrors requires tens of thousands of km of tape — similar scale to CFS ARC or Tokamak Energy ST-E1. The $30–100/kA-m current tape cost must reach $10/kA-m for commercial viability. All three concepts share this bottleneck and the associated supply-chain learning requirements (C3 = 3.1). The mirror's axisymmetric solenoids are easier to wind than tokamak D-coils or stellarator saddle coils, providing a manufacturing cost advantage, but the total tape quantity is comparable.

**Shares tritium breeding challenge with all D-T concepts — but cylindrical blanket geometry is favorable**
The global tritium supply (25–30 kg from CANDU reactors), Li-6 enrichment bottleneck (Russia/China dominance), and TBR > 1 requirement are identical across all D-T fusion concepts. The mirror's cylindrical axisymmetric center cell is geometrically favorable for breeding — full 2π coverage with no complex 3D shaping or inboard space constraints (unlike tokamaks). MARS achieved TBR 1.15 with LiPb in a yin-yang geometry; Realta's simpler geometry should exceed this. If the 2026 Hammir neutronics confirms TBR > 1.2, the mirror has a structural breeding advantage over compact tokamaks (which struggle to fit breeding blankets in the inboard space). If TBR falls below 1.0 with realistic port fractions, the advantage evaporates.

**Diverges from FRC w/ direct conversion (Helion) on fuel choice — D-He3 vs. D-T economics are incomparable**
Helion's D-He3 FRC pursues aneutronic fusion with ~40% of energy in charged particles, making DEC the dominant power pathway. Realta's D-T mirror captures 80% of energy thermally and only 20% via DEC. The Helion DEC is design-defining (η_plant ~ 35–40% with DEC vs. ~15% without); the Realta DEC is a 10% enhancement (η_plant ~ 40% with DEC vs. ~36% without). The economic cases are categorically different. Helion eliminates tritium breeding, Li-6 enrichment, and 14 MeV neutron shielding but inherits He-3 supply bootstrapping (no terrestrial source). Realta inherits all D-T challenges but benefits from mature fuel-cycle technology. From a TEA perspective, Realta is more analogous to D-T tokamaks than to Helion.

**Most similar to pre-ITER magnetic confinement concepts — 1980s technology with modern magnets**
MARS/MINIMARS (1983–1985) are the closest historical analogues. Both used tandem mirror geometry, LiPb blankets (TBR 1.15), direct energy conversion (~54% efficiency), and linear scaling arguments to justify economic viability. MARS projected ~7 ¢/kWh (1983 dollars, ~25 ¢/kWh in 2025 dollars inflation-adjusted) and found LCOE saturation near 600 MWe. Realta's CoSMo is MARS with HTS magnets (17 T vs. ~5 T copper) and modern heating systems (110 GHz gyrotrons vs. 1980s NBI). The HTS upgrade reduces coil resistive losses and shrinks magnet radius, but the fundamental concept is unchanged. The 95 $/MWh LCOE estimate is consistent with MARS economics once inflation-adjusted, suggesting the concept has not fundamentally improved its cost structure in 40 years — only its magnet technology.

---

## 6. Modeling Confidence

**Rating**: Low

**How many parameters are data-anchored vs. speculative?**
- **High-confidence data-anchored** (4 parameters): Q > 5 at 50 m (arXiv modeling, medium confidence), ~7 MW/m scaling law (Fusion Report interview, medium confidence), 17 T HTS magnets (WHAM demonstrated, high confidence), D-T fuel with lithium blanket (confirmed, high confidence).
- **Medium-confidence analogue** (3 parameters): η_th = 0.36 (MARS steam Rankine), η_de = 0.54 (MARS gridless DEC), TBR = 1.15 (MARS LiPb blanket). All three are 40-year-old analogues for fundamentally different magnet and blanket technologies.
- **Low-confidence default or speculative** (7 parameters): 40 MW heating power (2.5× uncertainty: 40 vs. 100 MW), 70 m center-cell length (extrapolation from 50 m pilot), 500 MWe net output (commercial scale guess, pilot targets >50 MWe only), 85% availability (no published target, DEC electrode lifetime unknown), all capital costs (framework defaults — zero Realta cost data), blanket type (undisclosed), thermal cycle type (undisclosed).

**Dominant source of LCOE uncertainty**
Three roughly equal contributors:
1. **Capital cost structure** is entirely uncharacterized. Framework defaults produce $6,489/kW overnight capital with no validation against Realta data. The only published cost signal is "$50M REBCO for WHAM++" — a sub-scale magnet cost that cannot be extrapolated to a 70 m commercial Hammir without magnet geometry and field strength specifications.
2. **Physics performance anchor** is weak. Q > 5 at 50 m is modeled not demonstrated. End-plug stability at commercial density/temperature has never been experimentally validated. The arXiv paper uses ML optimization to tune design parameters, indicating the solution is still being discovered computationally. Anvil (2028) will provide the first end-plug validation.
3. **Power balance uncertainty** is large. The 40 MW heating power assumption (producing Q_eng = 4.4, recirculating fraction 22.7%) carries 2.5× spread (40 vs. 100 MW from prior models). If commercial Hammir requires 70–80 MW, Q_eng falls to ~3.5 and LCOE rises 15–20%.

All three uncertainties are ~±30% individually, compounding to ±40% total LCOE uncertainty.

**Data adequacy breakdown (feeds into C8 scoring)**
- **Source diversity** (C8A = 3.0): One peer-reviewed physics paper (arXiv 2411.06644), one APS DPP conference abstract (Sutherland 2025), multiple company communications (Fusion Hub, Fusion Report interview), and one operational experiment (WHAM). No independent cost analysis or system code study exists for a modern HTS magnetic mirror. MARS (1983) is the only plant-level study, but it predates HTS magnets by 30 years. The mix of company and independent sources provides moderate confidence in physics claims but zero confidence in cost estimates.
- **Reactor design specification** (C8B = 3.0): Comprehensive conceptual design with major subsystems identified (magnets, heating, DEC, blanket, geometry) but significant gaps in engineering integration (blanket type undisclosed, thermal cycle unselected, recirculating power uncalculated, capital cost structure unknown). The 2026 Hammir design paper is expected to close many gaps.
- **LCOE parameter coverage** (C8C = 2.0): 6 blocking gaps (input power, recirculating fraction, center-cell length, blanket type/TBR, capital cost breakdown, DEC electrode lifetime). The gap count is worse than CFS ARC (4 blocking gaps) but better than purely speculative concepts with no operational hardware.
- **Commercialization pathway clarity** (C8D = 4.0): Clear three-stage roadmap (WHAM operational July 2024 → Anvil end-plug demonstrator ~2028 → Hammir pilot mid-2030s). Each stage de-risks the next. $9.5M SVB funding (Feb 2026) confirms ongoing operations. Industrial heat delivery as near-term application (data centers, chemical processing) provides a revenue pathway before grid electricity. This is better than most fusion startups (which go directly from lab-scale to pilot plant) but lacks published cost-to-market estimates or LCOE targets.

**Model validation status**
The model output (95.4 $/MWh at 500 MWe, 67.0 $/MWh at 1 GW) cannot be validated against Realta data because the company has published no cost estimates or LCOE targets. The fusion power of 1,052 MW (model output) is derived from 500 MWe net, 55% hybrid efficiency (updated from 36% thermal per canonical η_th), and assumed power balance — all UNCERTAIN. The Q_eng = 4.4 is a consistency check (net output requires Q_eng ~ 4–5 for a D-T hybrid plant), not a physics anchor. The model is internally consistent (power balance closes, CAS accounts sum correctly, sensitivities are plausible) but externally unvalidated. The 67 $/MWh at 1 GW is competitive with advanced tokamaks if — and only if — the end-plug physics validates and the linear scaling thesis proves out economically.

---

## 7. What Would Change My Mind

### 1. Anvil demonstrates stable end-plug confinement at Q > 5 equivalent conditions (by 2028–2030)
If the Anvil end-plug demonstrator achieves sustained electrostatic plugging potential > 5 kV at end-plug densities and temperatures consistent with main-cell Q > 5 operation, the single largest physics risk retires. I would upgrade the plasma performance evidence tier from 3 (subscale) to 4 (near-regime demonstrated). The LCOE confidence rating improves from Low to Medium. I would expect LCOE to remain in the 90–100 $/MWh range at 500 MWe (central estimate unchanged) but with error bars narrowing to ±25% instead of ±40%. Conversely, if Anvil achieves only Q ~ 2–3 equivalent plugging (50% of target), the concept fails its gating physics test and LCOE rises to 120–140 $/MWh as recirculating power dominates.

### 2. 2026 Hammir design paper discloses power balance and cost structure (expected mid-2026)
If Realta's expected 2026 pre-conceptual design paper for Hammir publishes: (a) fusion power and Q for the Rev D commercial design, (b) NBI + ECH input power requirement, (c) blanket type and neutronics (TBR validation), and (d) capital cost breakdown by CAS account, the data adequacy gap collapses from 6 blocking gaps to 1–2. I would update the LCOE model with anchored parameters and re-run. If the paper confirms 40 MW heating, Q ~ 10, and TBR > 1.2, the 95 $/MWh estimate is validated and confidence upgrades to Medium. If the paper reveals 80 MW heating, Q ~ 5, and TBR < 1.05, LCOE rises to 110–120 $/MWh and the concept becomes marginally viable at best.

### 3. Center-cell cost-per-meter is published below $8M/m (magnet + blanket + structure)
If the 2026 Hammir paper or a follow-on study provides a credible bottom-up cost estimate for the center-cell modular units (solenoid coil + annular blanket + support structure) at $5–8M/m, the linear scaling thesis becomes economically credible. At $7M/m for a 70 m center cell (~$500M), the concept gains a structural capital-cost advantage over tokamaks (which face minimum-size thresholds driving 4–6 GW thermal plants). I would lower the overnight capital estimate by 15–20% and LCOE drops to 80–85 $/MWh at 500 MWe. Conversely, if cost-per-meter exceeds $15M/m (total center-cell capital >$1B for 70 m), the scaling advantage evaporates and LCOE rises to 110+ $/MWh. The concept then competes poorly against large tokamaks.

---

## 8. LCOE Downselect Scoring

### C1: Modularization — Score: 2.8

**Sub-factor breakdown by CAS account construction mode:**

| CAS Account | Construction Mode | Mode Score | Cost Share | Weighted |
|-------------|------------------|------------|------------|----------|
| CAS21 (Buildings) | Stick-built (long cylindrical hall, 70+ m) | 1 | 11.3% | 0.11 |
| CAS22.1 (Blanket & first wall) | Factory-manufactured annular modules | 5 | 5.2% | 0.26 |
| CAS22.2 (Magnets — center cell) | Factory sub-assemblies, site-integrated solenoids | 3 | 3.3% | 0.10 |
| CAS22.2 (Magnets — end mirrors) | Factory sub-assemblies, site-integrated | 3 | 5.2% | 0.16 |
| CAS22.3 (Divertor/DEC) | Factory-manufactured DEC electrodes + site assembly | 5 | 1.8% | 0.09 |
| CAS22.4 (Vacuum vessel) | Stick-built cylindrical segments, field-welded | 1 | 3.7% | 0.04 |
| CAS22.5 (Shield) | Stick-built annular shield segments | 1 | 5.1% | 0.05 |
| CAS22.7 (Heat transport) | Site-assembled piping, pumps, HX | 1 | 1.3% | 0.01 |
| CAS22.9 (Heating — gyrotrons) | Factory-manufactured gyrotron units | 5 | 2.0% | 0.10 |
| CAS22.9 (Heating — NBI) | Factory sub-assemblies, site integration | 3 | 1.5% | 0.05 |
| CAS22.11 (Remote handling) | Factory-manufactured tooling (linear geometry) | 5 | 5.0% | 0.25 |
| CAS23 (Turbine plant) | Factory modules (steam Rankine or sCO2) | 3 | 3.8% | 0.11 |
| CAS24 (Electrical) | Factory components, site integration | 3 | 1.7% | 0.05 |

**Cost-weighted average**: 1.4
**Module repetition boost**: +1.0 (10–15 center-cell solenoid modules + 10–15 blanket annular segments + 30–40 gyrotron units = 50–70 repeated factory-manufactured components)
**C1 = 2.4, clamped to [1, 5]**

**Justification**: The magnetic mirror has genuine modularization advantages over tokamaks in specific subsystems: (1) annular blanket modules for the cylindrical center cell are geometrically simpler than tokamak 3D-shaped saddle-coil blanket modules — true factory manufacturing with repetition learning, (2) center-cell solenoid coils are axisymmetric (easier to wind than stellarator non-planar coils or tokamak D-coils), (3) DEC venetian blind electrodes are planar thin structures manufacturable in industrial stamping/coating facilities, (4) gyrotrons are off-the-shelf industrial equipment (1 MW CW units commercially available from Kyoto Fusioneering, Thales), (5) remote handling tools for a linear geometry are simpler than toroidal access (straight-line insertion vs. port-limited radial access). However, large fractions of capital remain stick-built: the 70 m cylindrical building is field-erected, the vacuum vessel is welded on-site, the WC-cermet shield is likely stick-built (concentric annular geometry with complex penetrations), and the heat transport piping is site-assembled. The cost-weighted average of 1.4 reflects this mix: ~30% of capital is genuinely modular (blanket, heating, RH, DEC), ~70% is stick-built or site-assembled (building, vessel, shield, magnets, BOP). The +1.0 repetition boost recognizes 50–70 repeated factory-manufactured units (blanket segments, solenoid modules, gyrotrons) — enough for meaningful learning curves. The final score of 2.4 places the concept between tokamaks (1.5–2.0) and laser IFE (3.5–4.0).

**Deviation from ST-E1 (tokamak) score of 2.0**: The mirror scores 0.4 higher due to: (a) annular blanket modules are simpler than tokamak saddle-coil blankets (+0.2), (b) axisymmetric solenoids are easier to manufacture than D-coils (+0.1), (c) linear remote handling is simpler than toroidal port access (+0.1). The mirror loses modularity vs. compact IFE concepts because the 70 m machine size forces stick-built buildings and large on-site assembly campaigns.

---

### C3: Supply Chain Learning — Score: 3.2

**Sub-factor A: Component learning rates (cost-weighted)** — **3.3**

| Component Category | Learning Rate | Justification | Cost Share | Weighted |
|-------------------|---------------|---------------|------------|----------|
| REBCO HTS tape (end mirrors) | 2 (fusion-specific, no market) | Global REBCO production ~thousands km/yr; commercial Hammir needs tens of thousands km for center-cell solenoids + two end mirrors; current price $30–100/kA-m vs. target $10/kA-m | 5.2% | 0.10 |
| REBCO HTS tape (center solenoids) | 2 (fusion-specific, no market) | Same supply chain as end mirrors; axisymmetric solenoids are simpler to wind (manufacturing advantage) but tape quantity is large | 3.3% | 0.07 |
| Li breeding blanket modules | 2 (fusion-specific) | Blanket type undisclosed (FLiBe/LiPb/liquid-Li/HCPB); no reactor-scale Li breeding blanket ever built; tritium extraction at kg/day untested | 5.2% | 0.10 |
| WC-cermet or steel shielding | 3 (specialty, limited supply) | Neutron shield for end mirrors and center-cell outer radius; industrial WC exists but not at nuclear grade; RAFM steel is TRL 6 (ITER baseline) | 5.1% | 0.15 |
| Vacuum vessel (cylindrical steel) | 4 (industrial component) | Large cylindrical pressure vessels are established industrial products (chemical, nuclear); 70 m length is large but geometry is simple | 3.7% | 0.15 |
| DEC venetian blind electrodes | 2 (fusion-specific) | No fusion-condition DEC hardware exists; thin planar electrodes with coatings are manufacturable but survivability under D-T exhaust is unknown | 1.8% | 0.04 |
| Gyrotrons (ECRH, 1 MW CW) | 3 (specialty, limited production) | 1 MW CW gyrotrons commercially available (Kyoto Fusioneering, Thales, CPI); scaling to 30–40 units for commercial Hammir is within reach but not mass-produced | 2.0% | 0.06 |
| NBI systems | 3 (specialty, growing base) | Modern NBI at 80–120 keV and multi-MW commercially available from ITER suppliers (JAEA, Budker); not yet mass-produced | 1.5% | 0.05 |
| Turbine & BOP (steam or sCO2) | 4 (industrial, growing base) | Steam Rankine is TRL 9 (GW-scale deployment); sCO2 Brayton is TRL 6 (10 MWe demos); fusion-specific integration but commodity cycle equipment | 3.8% | 0.15 |
| Remote handling (linear geometry) | 3 (fusion-specific, simpler than toroidal) | Linear access is geometrically simpler than tokamak/stellarator port-limited radial access; ITER RH prototypes exist but no commercial market | 5.0% | 0.15 |
| Structural steel, concrete, HVAC, electrical | 5 (commodity) | Fully established construction materials with deep supply chains | ~15% | 0.75 |

**Cost-weighted average: 3.3**

**Sub-factor B: Supply chain bottleneck count** — **3.5**

Start at 5.0, subtract penalties:
- **REBCO tape production scaling** (scaling constraint: global capacity must scale 10× from current thousands km/yr to tens of thousands km/yr for pilot + commercial fleet): -0.5
- **Li-6 enrichment capacity** (scaling constraint: current Western capacity insufficient for multi-GW D-T fusion fleet; Russian/Chinese suppliers dominate; Western alternatives under development): -0.5
- **DEC electrode coating/materials** (no hard constraint but untested at fusion conditions): -0.5

**Sub-factor B = 3.5** (higher than tokamak due to absence of hard WC-cermet bottleneck for center stack — no center stack in open-ended mirror geometry)

**Sub-factor C: External demand pull** — **2.5**

Components with >$1B/yr external markets:
- Structural steel, concrete, HVAC, electrical switchgear: ~15% of capital
- Steam turbines / sCO2 power cycle equipment: ~4% of capital (steam Rankine has $10B+/yr external market in nuclear + fossil; sCO2 is emerging but smaller)
- Vacuum pumps, cryogenic systems, control systems: ~2% of capital (industrial markets exist)
- Gyrotrons: ~2% of capital but <$50M/yr external market (materials processing, plasma heating for other fusion concepts)

**Total: ~20–25% of capital cost → Score 2–3 (framework: <20% = 2, 20–40% = 3)**
**C3C = 2.5** (midpoint; gyrotron market is small but growing; sCO2 market is emerging)

**C3 = (3.3 + 3.5 + 2.5) / 3 = 3.1**

**Justification**: The magnetic mirror supply chain is dominated by fusion-specific components (REBCO tape, Li breeding blanket, DEC electrodes, remote handling) with no current commercial markets outside fusion. The REBCO bottleneck is shared with all HTS fusion concepts (CFS, Tokamak Energy, TAE) — current global tape production must scale 10× to meet pilot plant demand. Li-6 enrichment is supply-constrained (legacy Russian/Chinese capacity dominates; Western alternatives are 5–10 years from commercial scale). However, the mirror avoids some tokamak bottlenecks: (a) no center-stack WC-cermet (open-ended geometry eliminates this hard constraint), (b) axisymmetric solenoids are easier to manufacture than 3D stellarator coils or compact tokamak D-coils (lower fabrication cost per meter of tape). The 20–25% commodity component share (steel, concrete, conventional BOP) provides modest external learning pull but does not offset the 75–80% fusion-specific island. The score of 3.1 reflects a supply chain requiring dedicated development, similar to tokamaks (3.0–3.2) but slightly better due to simpler magnet geometry and absence of center-stack cermet bottleneck.

---

### C4: Plant Complexity — Score: 2.5

**Sub-factor A: Operational coupling density** — **3**

The magnetic mirror operates as a steady-state D-T MFE device with moderate operational coupling:

- **Decoupled systems**: Cryogenic cooling (HTS magnets at ~20 K, lower load than 4 K LTS) operates independently of plasma state. Turbine & BOP run on steady thermal output (no pulsed buffering required — steady-state advantage over pulsed tokamaks). Tritium processing is batch-mode (not real-time coupled to plasma). DEC operates passively (no active feedback control — ions self-select by energy in magnetic expansion).

- **Moderate coupling**: NBI + ECH heating systems must sustain end-plug density and temperature continuously — any interruption degrades plugging potential and main-cell confinement decays. Plasma fueling (gas puffing or pellet injection) couples to NBI/ECH power — underfueling starves the plugs, overfueling cools them. Blanket coolant flow must match fusion power output — loss of coolant flow triggers plasma shutdown.

- **Failure cascades**: Loss of NBI or ECH during steady-state operation causes end-plug density/temperature decay, electrostatic plugging potential collapses, main-cell ions escape via loss cones, fusion power drops to zero within seconds (not catastrophic but requires restart). DEC electrode damage (e.g., coating spallation from neutron-induced embrittlement) reduces collection efficiency and increases heat deposition on end structures, potentially forcing shutdown for inspection. Blanket coolant leak requires plasma termination and radioactive-Li cleanup (high consequence but low frequency if engineered properly).

- **Maintenance coupling**: DEC electrode replacement requires hot-cell operations along the full machine length (linear access is simpler than toroidal, but activated electrodes create radiological coupling). End-mirror magnet replacement (if neutron damage exceeds REBCO tolerance after 5–10 FPY) is a multi-month campaign requiring access to both ends. Blanket module replacement is sequential (one annular segment at a time), reducing maintenance coupling vs. tokamaks (where blanket replacement often requires TF coil disassembly).

**Verdict**: Moderate coupling. Steady-state operation creates continuous NBI/ECH coupling (any interruption decays confinement), but the plasma does not require real-time feedback control for detachment, ELMs, or current-profile shaping (advantages over tokamaks). DEC operates passively (no active voltage tuning during plasma operation). The open-ended geometry eliminates divertor strike-point detachment control (major complexity reduction vs. tokamaks). **Score: 3**

**Sub-factor B: Subsystem count (>1% of capital)** — **2**

CAS22 sub-accounts and other major accounts >1% of total capital ($6.5B overnight):
1. Primary structure & support (C220101): $236M (3.6%)
2. Magnets — center solenoids (C220102 allocated): $110M (1.7%)
3. Magnets — end mirrors (C220102 allocated): $170M (2.6%)
4. Blanket & first wall (C220103): $205M (3.2%)
5. Shield & vacuum vessel (C220104 combined): $282M (4.3%)
6. Heat transport & coolant (C220107): $59M (0.9%) — just below 1%
7. DEC structures (C220108 if broken out; combined into C220104 in model): ~$60M (0.9%) — marginal
8. Fueling & vacuum (C220109 + C220105): $82M combined (1.3%)
9. Heating systems — NBI + ECH (C220200 via C220110/C220111): ~$104M (1.6%)
10. Auxiliary systems (C220500): $74M (1.1%)
11. Remote handling (C220111): $164M (2.5%)
12. Buildings (CAS21): $366M (5.6%)
13. Turbine plant (CAS23): $123M (1.9%)
14. Electrical plant (CAS24): $55M (0.8%) — just below 1%
15. Heat rejection (CAS26): $39M (0.6%)

**Count: 11 significant subsystems (>1% threshold) → Score 2** (11–14 range per framework)

**C4 = (3 + 2) / 2 = 2.5**

**Justification**: The magnetic mirror has moderate D-T MFE complexity — simpler than tokamaks in some respects (no disruptions, no divertor detachment control, passive DEC operation, linear remote handling access) but more complex in others (continuous NBI/ECH sustainment, novel DEC hardware, undemonstrated end-plug physics). The subsystem count (11–12) is typical for D-T fusion plants: magnets, blanket, heating, fueling, vacuum, tritium processing, remote handling, power conversion. The steady-state operation reduces control complexity vs. pulsed tokamaks (no CS re-magnetization, no ramp-up/flat-top transition management, no thermal buffering) but increases heating system duty cycle (NBI/ECH operate continuously, not just during ramp-up). The operational coupling is moderate — NBI/ECH interruption decays confinement, but the plasma does not cascade to disruption. The score of 2.5 places the concept between simple pulsed IFE chambers (3.5–4.0) and complex steady-state stellarators with 50+ magnet coils (1.5–2.0). The mirror is operationally simpler than compact tokamaks (no disruption management, no divertor detachment feedback) but has more subsystems than linear IFE concepts.

---

### C5: Customization Needs — Score: 2.0

**Sub-factor A: Thermal rejection** — **2**

Large cooling towers required for standard thermal cycle (updated model uses η_th = 0.55 hybrid efficiency with partial DEC contribution, but 80% of fusion energy is still captured thermally). At 500 MWe net output, ~1,052 MWt fusion power produces ~900 MWt thermal waste heat (after accounting for DEC capture of 20% alpha fraction at 54% efficiency and thermal capture at 55% effective efficiency). This requires conventional cooling towers sized for ~900 MWt rejection. The steady-state operation (no pulsed buffering) simplifies cooling system design vs. pulsed tokamaks but does not change the scale of thermal infrastructure. No air-cooling option (too large). Site selection requires cooling water availability or dry cooling with efficiency penalty. **Score: 2**

**Sub-factor B: Fuel safety profile** — **1**

D-T fuel with full tritium handling and breeding infrastructure. Lithium-based blanket (type undisclosed: FLiBe/LiPb/liquid-Li/HCPB) with TBR 1.15 analogue (MARS). Tritium inventory in blanket, fuel processing, DEC exhaust pumping, and storage. Tritium extraction from Li circuit at ~100–200 g/day throughput (matching fusion consumption). This is the most demanding fuel safety category. **Score: 1**

**Raw C5 = (2 + 1) / 2 = 1.5**
**Scaled to [1, 5]: C5 = 1 + (1.5 - 1) × (4/3) = 1.67 → rounds to 2.0**

**Justification**: The magnetic mirror requires large-scale conventional thermal rejection (cooling towers for ~900 MWt) and the most complex fuel cycle (D-T with tritium breeding, extraction from Li circuit, full fuel handling infrastructure, 14 MeV neutron activation). The cylindrical center-cell geometry does not simplify tritium handling — the blanket is annular (2π coverage, not 4π, but still large-area Li/tritium interface). Site selection must accommodate: (a) cooling water availability (or dry cooling at efficiency penalty), (b) tritium containment licensing (Part 30 NRC, similar to tokamaks), (c) 14 MeV neutron activation and decommissioning planning, (d) D-T fuel transport and storage. The linear geometry offers no site-flexibility advantages vs. toroidal D-T concepts. The score of 2.0 is identical to D-T tokamaks — both require identical thermal rejection and fuel-cycle infrastructure. The mirror gains no customization advantage from its geometry.

---

### C8: Data Adequacy — Score: 2.5

**Sub-factor A: Source diversity & independence** — **3**

- **Company sources**: Realta Fusion peer-reviewed arXiv preprint (2411.06644, Nov 2024), APS DPP 2025 conference abstract (Sutherland), company communications (Fusion Hub Startup Spotlight, The Fusion Report interview), SVB funding announcement (Feb 2026 PR Newswire). These are authoritative for machine parameters (R, L, B, Q targets) but lack independent validation.
- **Independent sources**: WHAM experiment details (UW-Madison public website, operational data), historical MARS/MINIMARS studies (1983–1985, LLNL public documents), Moir & Barr venetian blind DEC paper (Nuclear Fusion 1973, peer-reviewed), Endrizzi et al. WHAM physics basis (Journal of Plasma Physics 2023, peer-reviewed). These validate the concept class (tandem mirrors) and DEC technology but do not validate Realta's specific commercial design.
- **Academic literature**: No independent cost analysis or system code study for a modern HTS magnetic mirror exists. MARS (1983) is the only plant-level TEA, predating HTS by 30 years.

**Verdict**: Mix of company publications and independent sources with limited peer review. The arXiv confinement paper is peer-reviewed and citable, providing strong physics credibility. WHAM operational results (first plasma July 2024, 17 T HTS magnets demonstrated) validate the magnet technology. However, zero independent cost analyses or TEA studies exist for HTS mirrors. **Score: 3** (mix of independent and company sources with some peer review but no independent cost validation).

**Sub-factor B: Reactor design specification** — **3**

- **Complete specification**: Machine geometry (R0 undefined for cylinder, L = 70 m extrapolation, plasma radius 0.75 m), magnet type (REBCO HTS, 17 T demonstrated at WHAM, 10+ mirror ratio), heating method (NBI + ECH + HHFW confirmed), fuel (D-T with Li breeding blanket), DEC type (venetian blinds, axisymmetric ferromagnetic per Fusion Hub), operation mode (steady-state, 3+ hour target for pilot).
- **Partial specification**: Blanket type undisclosed (FLiBe/LiPb/liquid-Li/HCPB), thermal cycle unselected (steam Rankine vs. sCO2 unconfirmed), recirculating power fraction uncalculated (depends on unpublished heating power), fusion power for commercial Hammir derivable but not published (arXiv gives 175 MW for 50 m pilot, commercial extrapolation to 70+ m is inference).
- **Missing**: Capital cost breakdown (no CAS-level estimates for any subsystem), component replacement schedule (DEC electrode lifetime unknown, end-mirror magnet neutron flux uncharacterized), tritium extraction system design (Li circuit chemistry unspecified), remote maintenance scheme (linear access is conceptually simpler but no published strategy).

**Verdict**: Comprehensive conceptual design with major subsystems identified but significant gaps in engineering integration and costing. The 2026 Hammir design paper is expected to close many gaps. **Score: 3** (partial design with key subsystems defined but gaps in integration).

**Sub-factor C: LCOE parameter coverage** — **2**

Gap report blocking gaps (prevent LCOE closure without assumptions):
1. NBI + ECH input power for commercial Hammir — proprietary — **blocking** (2.5× uncertainty: 40 vs. 100 MW)
2. Recirculating power fraction — derivable but requires (1) — **blocking**
3. Center-cell length for commercial Hammir — proprietary — **blocking** (50 m pilot confirmed, commercial length unspecified)
4. End-plug confinement validation at Q > 5 — truly-unknown (Anvil ~2028) — **blocking** (gating physics risk)
5. Blanket type and TBR — proprietary — **blocking** (FLiBe/LiPb/liquid-Li/HCPB drives cost and efficiency)
6. Capital cost breakdown — truly-unknown — **blocking** (zero Realta subsystem cost data)
7. DEC electrode lifetime — truly-unknown — **important** (drives availability assumption)

**Count: 6 blocking gaps → Score 2** (5–7 blocking gaps per framework)

**Sub-factor D: Commercialization pathway clarity** — **4**

- **Clear pathway**: WHAM operational (July 2024, 17 T HTS demonstrated) → Anvil end-plug demonstrator (~2028, validates Q > 5 plugging physics) → Hammir pilot (mid-2030s, Qe > 1, >50 MWe for 3+ hours) → commercial plant (2040s, 500+ MWe). Each stage de-risks the next. This is a coherent three-stage build sequence.
- **Funding**: $9.5M SVB growth capital (Feb 2026) confirms ongoing operations. Total funding not disclosed but WHAM construction ($10M ARPA-E + internal/partner funds) and WHAM++ ($50M REBCO tape signal) suggest $60–80M cumulative. Industrial heat delivery (data centers, chemical processing, metal recycling) as near-term application provides revenue pathway before grid electricity.
- **Timeline**: Hammir mid-2030s grid connection target is realistic (10-year development from 2024 WHAM first plasma). 2026 pre-conceptual design paper publication is committed by company.
- **Gaps**: No published LCOE target or cost-to-market estimate. No fleet deployment plan or unit cost reduction roadmap. No public identification of strategic partners beyond CFS (magnet supplier) and UW-Madison (WHAM host). Funding is growth-stage ($9.5M) not pilot-construction-scale ($500M+).

**Verdict**: Clear roadmap with identified steps and incremental de-risking, but lacking cost specifics and commercialization economics. Better than purely aspirational concepts (which skip intermediate validation steps), worse than programs with published cost targets and fleet plans (e.g., CFS ARC with $0.065/kWh LCOE target). **Score: 4** (clear pathway with steps but gaps in commercial economics).

**C8 = (3 + 3 + 2 + 4) / 4 = 3.0 → rounds to 3.0**

**Justification**: The data adequacy is characteristic of a well-documented concept at the pre-conceptual design stage from a moderately transparent company. Realta publishes more than most fusion startups (peer-reviewed arXiv paper, operational experiment, conference abstracts) but stops short of the detail needed for independent LCOE validation. The 6 blocking gaps (heating power, recirculating fraction, center-cell length, end-plug validation, blanket type, capital cost) force the model to rely on MARS analogues across most of the cost structure. The arXiv physics paper is credible and citable, providing strong confinement physics documentation (better than concepts with no peer-reviewed basis). WHAM operational results validate the HTS magnet technology (a major de-risking vs. paper designs). The commercialization pathway is clear and incremental (WHAM → Anvil → Hammir is a coherent sequence). However, the complete absence of cost data, the 2.5× uncertainty in heating power, and the undemonstrated end-plug physics prevent confident LCOE estimation. The score of 3.0 reflects data sufficient for first-pass LCOE estimation with clearly bounded uncertainties, but insufficient for cross-concept ranking or investment decision-making without the 2026 Hammir design paper.

**Deviation from prior synthesis (ST-E1 C8 = 2.5)**: The mirror scores 0.5 higher due to: (a) peer-reviewed arXiv confinement paper provides stronger physics credibility than Tokamak Energy DPP abstracts alone (+0.3), (b) WHAM operational results (first plasma, 17 T HTS demonstrated) validate magnet technology at scale (+0.2). The mirror loses points vs. ST-E1 on commercialization (Tokamak Energy has $335M funding and DOE Milestone participation; Realta has $9.5M disclosed and no DOE program). The net difference is +0.5 in data adequacy, driven by stronger physics documentation.

---

### C7: Technical Risk Evidence — 14-cell risk matrix

#### Function 1: Plasma Performance

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Main-cell confinement at Q > 5 requires end-plug electrostatic potential barrier ≥ 5 kV to suppress ion escape via loss cones; main-cell density ~10²⁰ m⁻³, Ti ~ 10–15 keV, τE sufficient for fusion power density ~7 MW/m³ at 70 m length → 1,050 MWt fusion |
| Best demonstrated | WHAM achieved first plasma July 2024, targeting 1 keV electron temperature and 20 keV average ion energy (sub-commercial); TMX (1980s, decommissioned) demonstrated tandem mirror end-plug electrostatic plugging at ~1 kV potential (5× below commercial requirement); arXiv 2411.06644 models Q = 5.8 at 50 m, Q > 10 at longer cells but with ML-optimized stability parameters flagged as requiring active stabilization |
| Gap ratio | ~100× in fusion power density (TMX sub-MW/m³ → commercial ~7 MW/m³), 5× in end-plug potential (TMX ~1 kV → commercial ≥5 kV) |
| Closure mechanism | Scaling from WHAM + Anvil to Hammir pilot; arXiv modeling uses sloshing ions for DCLC suppression and vortex flows for AIC stabilization; machine learning optimization of coil currents and plasma profiles; heritage from 1980s tandem mirror physics (TMX, MFTF-B) provides qualitative validation but not quantitative extrapolation to HTS high-field regime |
| Classification | Binary (zero net electricity if end-plug confinement fails to achieve Q ≥ 3; degrading if Q = 3–5 rather than Q > 5 target, as recirculating power rises) |
| Evidence tier | 3 (subscale demonstration: TMX demonstrated tandem mirror physics at 1 kV plugging, WHAM validating high-field end-plug geometry; commercial Q > 5 is 5–10× extrapolation unvalidated by experiment) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | First wall heat flux tolerance ~1–2 MW/m² average (open-ended geometry distributes flux over large cylindrical surface area); end structures and DEC electrodes tolerate escaping-particle heat load ~5–10 MW/m² after magnetic expansion; plasma-facing components survive 30-year lifetime (with periodic replacement) under 14 MeV neutron flux ~0.5–1 MW/m² and continuous plasma bombardment |
| Best demonstrated | WHAM first wall is uncooled tungsten at sub-MW/m² heat flux (operational July 2024–present); DEC venetian blinds demonstrated in laboratory settings at 50–65% efficiency (Moir & Barr 1973) but never in fusion conditions; MARS study (1983) incorporated DEC at ~54% efficiency in plant design but DEC was never built or tested at reactor scale; no first wall tested under combined 14 MeV neutron flux + continuous D-T plasma bombardment in an open-ended geometry |
| Gap ratio | ~1000× in integrated fluence-duration product (WHAM seconds-to-minutes → commercial 30 years continuous), N/A for DEC (laboratory beam tests → D-T fusion exhaust is categorically different environment) |
| Closure mechanism | Magnetic expansion at mirror throats reduces heat flux on DEC electrodes by 5–10× (field expansion from 17 T mirror peak to ~2–3 T at DEC location); tungsten first wall technology from tokamak programs (WEST, ITER); thin uncooled DEC electrodes must survive via radiative cooling + periodic replacement (replacement schedule unknown — flagged as blocking gap); annular blanket modules provide structural support and neutron shielding for first wall |
| Classification | Degrading (DEC electrode failure shortens replacement intervals, reduces availability, increases maintenance cost; inadequate first wall cooling increases erosion rate and replacement frequency; not binary because plant can operate with higher replacement frequency at cost penalty) |
| Evidence tier | 2 (simulation + lab scale: DEC demonstrated in beam tests but never in D-T fusion exhaust; first wall heat flux distribution modeled but open-ended geometry unvalidated; WHAM demonstrates sub-commercial first wall survival but fluence gap is 1000×) |

**Function-level mean: F1 = (3 + 2) / 2 = 2.5**

---

#### Function 2: Driver / Energy Input

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | NBI + ECH heating at 30–40 MW (arXiv-anchored) to 60–100 MW (prior pipeline range) continuous input to sustain end-plug density and temperature; ECH current drive efficiency sufficient to maintain plugging potential ≥5 kV; NBI for fueling and end-plug ion heating; total heating power determines recirculating fraction and Q_eng |
| Best demonstrated | WHAM operates 1 MW ECH (110 GHz gyrotron delivered by Kyoto Fusioneering Jan 2025) + NBI + HHFW for end-plug heating; arXiv 2411.06644 cites 30–40 MW input for 50 m pilot at Q = 5.8 (derived from P_fus = 175 MW); ITER-class gyrotrons at 1 MW CW demonstrated at 170 GHz; NBI at 80–120 keV and multi-MW demonstrated on JT-60SA, DIII-D |
| Gap ratio | 30–100× in total heating power (1 MW demonstrated at WHAM → 30–100 MW required for commercial Hammir, depending on which prior model is correct) |
| Closure mechanism | Scaling gyrotron count from 1 (WHAM) to 30–100 units (commercial Hammir); gyrotron technology is commercially available at 1 MW CW (Kyoto Fusioneering, Thales, CPI); NBI scaling to 10–20 MW total is within demonstrated tokamak range; steady-state operation (continuous heating) is more demanding than tokamak pulsed heating (ramp-up only) but wall-plug efficiency is well-characterized (~50–55% for ECH, ~60–70% for NBI) |
| Classification | Degrading (insufficient heating power reduces Q, increases recirculating fraction, lowers net output; excessive heating power cost raises capital and operating expense; not binary because plant can operate at lower Q with higher recirc fraction, just worse economics) |
| Evidence tier | 4 (near-regime: 1 MW CW gyrotron operational on WHAM, multi-MW NBI demonstrated on tokamaks, 30–100 MW total is scaling not novel physics; continuous operation is extrapolation from pulsed tokamak heating but wall-plug efficiency is known) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | 30–100× 1 MW CW gyrotrons (depending on total heating power requirement) with >50% wall-plug efficiency, reliable over 30-year plant lifetime (with periodic tube replacement every 5–10 years); NBI ion sources and neutralizers at 10–20 MW total with 60–70% efficiency; launcher ports and waveguide transmission with minimal neutron/gamma damage in fusion environment |
| Best demonstrated | Single 1 MW CW gyrotron at 110 GHz operational on WHAM (Jan 2025, Kyoto Fusioneering); ITER procured multiple 1 MW 170 GHz gyrotrons (TRL 7); gyrotron lifetimes >10,000 hours demonstrated in test stands but not in fusion neutron environment; NBI systems at 10+ MW operational on JT-60SA (20 MW NBI), DIII-D (20 MW); NBI ion sources require periodic replacement (cathodes, grids) every 1–2 years |
| Gap ratio | 1× in unit gyrotron/NBI performance (demonstrated at 1 MW/unit), 30–100× in integrated system scale (1 unit → 30–100 units), N/A for neutron environment (no burning plasma D-T mirror exists to test heating hardware under 14 MeV neutron flux) |
| Closure mechanism | Industrial gyrotron production scaling (Kyoto Fusioneering ramping 1 MW CW production; Thales and CPI also produce MW-class tubes); NBI systems commercially available from ITER suppliers (JAEA, Budker); launcher shielding and remote replacement for degraded components; gyrotron tube replacement every 5–10 years is budgeted O&M cost |
| Classification | Degrading (gyrotron or NBI failures reduce heating availability, shorten pulse duration or force plasma termination, increase maintenance cost; not binary because plant can restart after component replacement) |
| Evidence tier | 4 (near-regime: CW gyrotron and multi-MW NBI demonstrated, 30–100 unit integrated system is scaling not R&D; neutron environment for launchers is extrapolation but shielding strategies exist from tokamak ECRH ports) |

**Function-level mean: F2 = (4 + 4) / 2 = 4.0**

---

#### Function 3: Instability Control

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | DCLC (drift cyclotron loss cone) instability suppressed via sloshing ions at end plugs; AIC (Alfvén ion cyclotron) instability suppressed via vortex stabilization (sheared azimuthal flows); classical radial transport dominates (good curvature in expander regions); disruptions impossible (no plasma current, no current-driven kink modes); end-plug stability at reactor-relevant density and temperature for Q > 5 main-cell confinement |
| Best demonstrated | TMX (1980s) demonstrated sloshing-ion stabilization of DCLC at sub-commercial conditions (~1 kV plugging potential, 10¹³ cm⁻³ end-plug density); arXiv 2411.06644 models DCLC/AIC suppression via ML-optimized coil currents and vortex flows but explicitly flags "stabilization against MHD and trapped particle modes" as required; WHAM will test end-plug stability at higher field (17 T) but sub-commercial density/temperature; no operating mirror has achieved commercial Q > 5 end-plug conditions |
| Gap ratio | ~5–10× in end-plug density and temperature (TMX 10¹³ cm⁻³, ~1 keV → commercial 10¹⁴ cm⁻³, ~10 keV required for deep potential well); gap is qualitative: ML-optimized stability is computationally predicted but experimentally unvalidated |
| Closure mechanism | Anvil device (~2028) is dedicated end-plug demonstrator to validate DCLC/AIC suppression at commercial-relevant parameters; arXiv modeling provides computational roadmap; TMX historical results provide qualitative validation that tandem mirror end-plugging works in principle; HTS high-field magnets (17 T at WHAM, 10+ mirror ratio) enable higher end-plug density and deeper potential wells than 1980s copper coils |
| Classification | Binary (failed DCLC stabilization causes excessive ion loss via drift modes, collapsing plugging potential and main-cell confinement; plant produces zero net electricity if Q < 3 due to high recirculating fraction) |
| Evidence tier | 2 (simulation + historical qualitative analogue: TMX demonstrated sloshing-ion stabilization at 1980s conditions; arXiv modeling uses ML optimization to predict commercial stability but "stabilization required" language indicates solution is still computational; Anvil will test but has not yet operated) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | HTS end-mirror magnets at 17 T peak field create 10+ mirror ratio to enable deep electrostatic potential wells; coil current control for vortex stabilization (requires real-time feedback or preprogrammed profiles); plasma-facing components tolerate end-plug heat flux and escaping-particle bombardment; no active MHD control coils required (advantage over tokamaks — mirrors have no current-driven instabilities) |
| Best demonstrated | WHAM operates two 17 T HTS end-mirror magnets (CFS-built REBCO, operational July 2024); >20 T on-conductor achieved (world record for magnetically confined plasma experiments at WHAM scale per analysis.md); coil current control at ms-timescale demonstrated on tokamaks (power supplies, feedback algorithms); no burning-plasma mirror has tested end-mirror magnet performance under 14 MeV neutron flux from end-loss cones |
| Gap ratio | 1× in magnet field performance (17 T demonstrated at WHAM scale), ~100× in neutron flux environment (WHAM is deuterium sub-MW fusion → commercial is 1 GW D-T with 14 MeV neutrons escaping via end-loss cones into end-mirror region) |
| Closure mechanism | HTS REBCO magnets demonstrated at WHAM; neutron shielding for end-mirror coils (thick shield between plasma end region and magnet bore, accepting larger machine radius if needed); REBCO critical current degradation under neutron irradiation is a known risk (flagged in Challenge 6 verdict) — may require end-mirror magnet replacement every 5–10 FPY if shielding is inadequate |
| Classification | Degrading (inadequate end-mirror neutron shielding shortens magnet lifetime, increases replacement frequency and maintenance cost; coil current control failures degrade vortex stabilization and increase DCLC losses, reducing Q; not binary because magnets are replaceable and control can be restored) |
| Evidence tier | 3 (subscale + extrapolation: 17 T HTS demonstrated at WHAM scale in non-burning plasma; neutron shielding for end-mirror magnets is design challenge unaddressed in Realta publications; REBCO irradiation tolerance at 10¹⁸ n/m² is uncertain) |

**Function-level mean: F3 = (2 + 3) / 2 = 2.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Open-ended loss-cone divertor distributes escaping-particle heat load over large end surface area and DEC electrodes; magnetic expansion at mirror throats reduces heat flux from ~50–100 MW/m² (typical tokamak divertor parallel flux) to ~5–10 MW/m² at DEC electrode location; acceptable sputtering rates (tungsten erosion <10 nm/s) for multi-year first-wall lifetime; no detachment control required (major simplification vs. tokamaks) |
| Best demonstrated | WHAM operates open-ended geometry with end-loss plasma flowing to end vacuum pumps (heat flux unmeasured but sub-MW/m² scale at current WHAM power levels); no magnetic mirror has operated at fusion-relevant power levels (1 GW thermal) to validate heat flux distribution in end regions; MARS study (1983) assumed DEC electrode heat flux manageable via radiative cooling + periodic replacement but provided no experimental validation |
| Gap ratio | ~1000× in fusion power (WHAM ~1 MW → commercial Hammir 1,000+ MW) creates proportional increase in end-loss heat flux; gap is qualitative: heat flux distribution in open-ended geometry at fusion power is unvalidated |
| Closure mechanism | Magnetic field expansion at mirror throats (17 T peak → 2–3 T at DEC location) spreads heat flux over larger surface area; DEC electrodes are thin planar structures designed for radiative cooling (no active cooling per MARS analogy); first wall is actively cooled via blanket coolant (Li or other); periodic replacement of DEC electrodes (schedule unknown — flagged as blocking gap in analysis.md) if erosion exceeds tolerance |
| Classification | Degrading (excessive DEC electrode erosion shortens replacement intervals, reduces availability, increases maintenance cost; inadequate first-wall cooling increases erosion and component damage frequency; not binary because plant can operate with higher replacement frequency at cost penalty) |
| Evidence tier | 2 (simulation only: heat flux distribution modeled via magnetic field expansion but never validated experimentally at fusion power; DEC electrode heat flux tolerance is analogy from 1973 lab tests, not fusion-relevant demonstration) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Tungsten first wall survives ~1–2 MW/m² average neutron + plasma heat flux for 5+ FPY; DEC venetian blind electrodes (thin planar structures with specialized coatings) tolerate ~5–10 MW/m² escaping-particle heat load for 1–3 years between replacements; end vacuum pumps and cryopanels handle continuous D-T exhaust at ~10–20 Pa·m³/s throughput; bake-out and conditioning systems maintain low impurity influx |
| Best demonstrated | Tungsten first wall tested on WEST (10+ MW/m² for 50+ seconds in L-mode), ITER divertor monoblocks tested at 20 MW/m² for 1000+ cycles in GLADIS; no tungsten first wall tested under combined 14 MeV neutron flux + continuous plasma bombardment in open-ended geometry for multi-year integrated exposure; DEC venetian blinds demonstrated in 1973 lab tests (Moir & Barr) at 50–65% efficiency for monoenergetic ion beams but never in D-T fusion exhaust; vacuum pumps at 10–20 Pa·m³/s commercially available (Edwards, Pfeiffer, Leybold) but tritium-compatible pumps require specialized design |
| Gap ratio | ~100–1000× in fluence-duration product for first wall (WEST 50 seconds → commercial 30 years), N/A for DEC electrodes (lab beam tests → D-T fusion exhaust is categorically different), 1× in vacuum pump throughput (demonstrated at required scale but tritium compatibility is engineering challenge) |
| Closure mechanism | Tungsten monoblock first wall technology from ITER program; magnetic expansion reduces DEC electrode heat flux below active cooling threshold (radiative cooling only); DEC electrode replacement via remote handling every 1–3 years (schedule TBD pending Anvil/Hammir data); vacuum pump technology from tokamak tritium systems (ITER, JET) with cryopanel regeneration cycles |
| Classification | Degrading (DEC electrode erosion shortens replacement intervals, increases maintenance downtime and cost; first wall erosion increases activated waste volume and replacement frequency; vacuum pump failures reduce availability; not binary because all components are replaceable) |
| Evidence tier | 3 (subscale + extrapolation: tungsten first wall tested at high flux but short duration; DEC electrodes tested in lab but not fusion environment; vacuum pumps demonstrated at throughput scale but tritium systems are specialty engineering; multi-year integrated exposure is unvalidated) |

**Function-level mean: F4 = (2 + 3) / 2 = 2.5**

---

#### Function 5: Neutron/Particle Handling

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | 14 MeV neutron flux ~0.5–1 MW/m² at cylindrical first wall (lower flux density than compact tokamaks due to larger surface area of 70 m cylinder); neutron energy deposition in blanket + shield does not exceed structural material damage limits (~15 dpa/FPY in first-wall steel); helium production in structural materials (via n,α reactions) tolerable for 5+ FPY operation; end-loss neutrons escaping via loss cones into end-mirror regions require shielding to protect HTS magnets |
| Best demonstrated | JET DTE2 (2021) produced 14 MeV neutrons at ~1 MW fusion power for ~5 seconds in tokamak D-T shots; NIF ignition (2022) produced 14 MeV neutrons at 3.15 MJ in single-shot microsecond implosion; no magnetic mirror has operated with D-T fuel; neutron transport physics is well-understood via MCNP/Serpent codes validated on JET and TFTR; cylindrical geometry creates ~170 m² first-wall surface area at 70 m length, 0.75 m radius → ~6 MW/m² at 1,052 MW fusion implies flux distribution is not uniform (peaked at center cell) |
| Gap ratio | ~1000× in fusion power (JET 1 MW → commercial 1,000+ MW), ~10⁶× in integrated neutron fluence (JET 5 seconds → commercial 30 years); gap is quantitative: neutron physics is validated but fluence accumulation at commercial scale is extrapolation |
| Closure mechanism | 14 MeV neutron transport modeling validated on JET, TFTR, NIF data; cylindrical geometry distributes neutrons over large surface area (advantage over compact tokamaks); blanket/shield design uses RAFM steel (TRL 6 from ITER program) or ODS steel for first wall; end-mirror neutron shielding (thick annular shield between end-loss plasma and HTS magnets) required but not yet designed by Realta (flagged in Challenge 6 verdict) |
| Classification | Degrading (excessive neutron damage shortens structural lifetimes, increases blanket/first-wall replacement frequency, raises tritium inventory in activated materials; end-loss neutrons damaging HTS end-mirror magnets shortens magnet lifetime; not binary because damage is gradual and components are replaceable at cost penalty) |
| Evidence tier | 3 (subscale demonstration: JET/TFTR produced 14 MeV neutrons in tokamak geometry; mirror open-ended geometry is different but neutron physics is well-modeled; commercial fluence is 10⁶× extrapolation) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Annular Li breeding blanket (type undisclosed: FLiBe/LiPb/liquid-Li/HCPB) operates at 400–700°C without excessive corrosion, tritium permeation, or structural damage under 14 MeV neutron flux for 5 FPY replacement interval; RAFM or ODS steel first wall survives ~50–100 dpa over 5 FPY; end-mirror neutron shielding (material TBD, likely WC-based or steel) reduces fast neutron flux into HTS coil bore to <10¹⁷ n/m² s⁻¹ to limit REBCO critical current degradation; remote handling for activated blanket/first-wall modules in linear geometry |
| Best demonstrated | FLiBe chemistry studied in Kairos Power fission program (700°C) and MSRE (1960s, 650°C); LiPb blanket tested in fission-neutron test loops (EU TBM program) but not at fusion neutron spectrum; RAFM steels tested to 80 dpa in fission reactors (HFIR) but 14 MeV fusion spectrum creates different He/dpa ratios; REBCO tape irradiation studies show critical current degradation at ~10¹⁸ n/m² fast fluence (data sparse); no full-scale breeding blanket operated under fusion neutron flux for multi-year exposure |
| Gap ratio | 1× in blanket temperature regime (FLiBe/LiPb demonstrated at 400–700°C), ~10× in neutron flux environment (fission test loops ~0.1 MW/m² → fusion first wall ~1 MW/m²), 100× in integrated fluence (fission test campaigns months → fusion commercial years); end-mirror neutron flux into HTS coils is uncharacterized (Realta has not published shielding design) |
| Closure mechanism | Li blanket chemistry from fission breeder programs (Pb-17Li analogue, liquid Li reactors); RAFM steel is ITER baseline structural material (TRL 6); end-mirror shielding design TBD (likely WC-based or thick steel annular shield, accepting larger machine radius if needed); REBCO tape replacement as part of end-mirror magnet maintenance every 5–10 FPY if neutron flux exceeds tolerance; remote handling for activated blanket modules in linear geometry is geometrically simpler than tokamak port access |
| Classification | Degrading (excessive blanket neutron damage shortens replacement intervals, increases maintenance cost and activated waste volume; inadequate end-mirror shielding damages HTS magnets and forces replacement every 5–7 FPY instead of 10+ FPY; not binary because all components are replaceable) |
| Evidence tier | 3 (subscale + fission analogue: Li blanket chemistry demonstrated in fission environments but not fusion neutron spectrum; RAFM steel tested in fission reactors but fusion He/dpa ratios are different; REBCO irradiation data incomplete; end-mirror shielding is design challenge unaddressed in Realta publications) |

**Function-level mean: F5 = (3 + 3) / 2 = 3.0**

---

#### Function 6: Fuel Cycle Closure

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | TBR ≥ 1.05 after accounting for realistic port fractions (NBI, ECH, diagnostics, vacuum access penetrate cylindrical blanket), module gaps, and maintenance access; tritium breeding reaches equilibrium within 2–3 FPY without external supply beyond startup inventory (~1 kg); cylindrical axisymmetric blanket geometry covers 2π solid angle (advantage over tokamak 4π requirement) |
| Best demonstrated | MARS study (1983) achieved TBR = 1.15 with LiPb blanket in yin-yang mirror geometry; neutronics modeling for cylindrical mirrors confirms 2π coverage is favorable for breeding (full 360° azimuthal coverage, no inboard space constraint like tokamaks); no experimental TBR validation in any operating magnetic mirror; ITER TBM program will test breeding modules but at <1% of surface area, not full 2π |
| Gap ratio | N/A (TBR = 1.15 is MARS modeling prediction for different geometry; Realta's commercial TBR is unpublished; gap is qualitative: no TBR validation for cylindrical HTS mirror exists) |
| Closure mechanism | Neutronics calculations (MCNP, Serpent) for Hammir geometry with Li blanket type TBD (FLiBe/LiPb/liquid-Li/HCPB); cylindrical 2π geometry eliminates inboard breeding challenge faced by tokamaks (structural advantage); possible Li-6 enrichment to 30–60% (from 7.5% natural) to boost TBR if needed; 2026 Hammir design paper expected to include neutronics and TBR validation |
| Classification | **Binary** (TBR < 1.0 after realistic penetrations means external tritium supply required indefinitely, economically non-viable for fleet deployment; TBR = 1.0–1.05 is marginal and sensitive to port fraction assumptions) |
| Evidence tier | 2 (simulation only: MARS TBR = 1.15 is for different geometry and 1983 codes; Realta TBR unpublished; cylindrical 2π geometry is theoretically favorable but unvalidated experimentally) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Li blanket tritium extraction at ~150–200 g T/day throughput (matching consumption for ~1 GW fusion power); tritium inventory in blanket <5 kg (regulatory limit); tritium permeation through Li/heat-exchanger interfaces <1 g/day (minimizes inventory loss); closed-loop Li circulation with inert atmosphere (if liquid Li metal) or salt chemistry management (if FLiBe/LiPb); blanket type selection (FLiBe/LiPb/liquid-Li/HCPB) drives extraction chemistry and system design |
| Best demonstrated | Pb-17Li tritium extraction demonstrated at g/day scale in EU TBM test loops; FLiBe vacuum degassing demonstrated in MSRE (1960s) but not for tritium specifically; liquid Li metal tritium extraction is less characterized than Pb-17Li (no fusion-relevant demonstration); tritium permeation barriers (Al₂O₃, Er₂O₃ coatings) tested in lab but not at plant scale; inert atmosphere loops (Ar or He cover gas for liquid Li) demonstrated in sodium-cooled fission reactors (Phenix, Superphenix) but Li is more reactive than Na |
| Gap ratio | ~100× in tritium extraction throughput (1 g/day lab scale → 150–200 g/day plant scale), 1× in permeation barrier materials (demonstrated in lab but not at fusion heat-exchanger scale), 1× in inert atmosphere loop technology (demonstrated for Na in fission, Li is more reactive) |
| Closure mechanism | Li metal tritium extraction via vacuum degassing or selective permeation (technology exists at lab scale, engineering scale-up required); Pb-17Li extraction from EU TBM program provides partial analogue; permeation barriers on heat exchanger surfaces (technology demonstrated in fission programs); blanket type selection in 2026 Hammir design paper will clarify extraction pathway |
| Classification | **Binary** (failed tritium extraction or excessive permeation losses prevent fuel cycle closure, requiring external tritium purchase indefinitely at $35k/g — economically non-viable; tritium inventory exceeding regulatory limits forces operational restrictions or licensing delays) |
| Evidence tier | 2 (lab scale + partial analogue: Pb-17Li extraction demonstrated but pure Li metal or FLiBe extraction at fusion scale is unvalidated; permeation barriers tested in fission environments but fusion heat exchanger chemistry is different; inert atmosphere loop technology from fission Na reactors is analogous but Li is more reactive) |

**Function-level mean: F6 = (2 + 2) / 2 = 2.0**

---

#### Function 7: Power Conversion & BOP

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Hybrid thermal + direct conversion: (1) thermal pathway captures 80% of fusion energy (14.1 MeV neutrons) in Li blanket at 400–700°C (blanket type TBD), feeding steam Rankine (~33–36% efficiency) or sCO2 Brayton (~40–45% efficiency) secondary cycle; (2) DEC pathway captures 20% of fusion energy (3.5 MeV alphas) via venetian blind electrodes at ~54% efficiency (MARS analogue); combined η_plant ~ 40–55% (model uses 55% hybrid) |
| Best demonstrated | Steam Rankine at 33–38% efficiency is commercially mature for nuclear PWRs (300+ GWe installed globally) and CSP plants; sCO2 Brayton demonstrated at 10 MWe scale (Sandia, 2020s) with projected 42–48% efficiency at 600–700°C; DEC venetian blinds demonstrated at 50–65% efficiency in 1973 lab tests (Moir & Barr) for monoenergetic ion beams; MARS study (1983) achieved ~36% overall plant efficiency (thermal + DEC combined) in plant design but DEC was never built |
| Gap ratio | 1× in steam Rankine efficiency (fully mature), ~100× in sCO2 scale (10 MWe demo → 500+ MWe commercial), N/A for DEC (lab ion beams → D-T fusion alpha exhaust is categorically different environment; efficiency may be similar but electrode survivability is untested) |
| Closure mechanism | Steam Rankine is low-risk baseline (TRL 9); sCO2 Brayton offers 5–10 percentage point efficiency gain but requires commercialization (multiple vendors developing: Echogen, Kairos, GE); DEC efficiency at 54% is MARS historical value, venetian blind geometry is conceptually simpler than gridless converters, but no fusion-condition validation exists; steady-state operation (no thermal buffering required) is advantage over pulsed tokamaks |
| Classification | Degrading (low thermal efficiency reduces net output, increases LCOE; DEC failure (electrode erosion, efficiency degradation) forces fallback to thermal-only operation at ~36% efficiency vs. ~40–55% hybrid, raising LCOE by ~10–15%; not binary because plant can operate thermal-only) |
| Evidence tier | 4 for thermal pathway (steam Rankine fully mature; sCO2 demonstrated at 10 MWe, commercial scale is extrapolation), 2 for DEC pathway (lab efficiency demonstrated but fusion-condition electrode survivability unvalidated) → blended tier is 3 (acknowledging DEC is the higher-uncertainty component) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Li-to-secondary-fluid heat exchangers survive 400–700°C liquid Li or molten salt environment with tritium permeation barriers; steam turbine or sCO2 turbomachinery operates on steady heat input with >99% availability; DEC venetian blind electrodes (thin planar structures, ~1–5 mm thick with specialized coatings) tolerate ~5–10 MW/m² escaping-alpha heat load for 1–3 years between replacements (replacement schedule TBD); high-voltage biasing system (10–50 kV) for DEC energy separation |
| Best demonstrated | Na-to-water heat exchangers operated in fission fast reactors (Phenix, Superphenix) at 500–550°C (Li is more reactive but similar temperature regime); steam turbines achieve >99.5% availability in baseload nuclear plants (300+ GWe fleet globally); sCO2 turbomachinery demonstrated at 10 MWe scale (reliability data limited); DEC venetian blinds are planar electrodes manufacturable via stamping/coating but never tested in D-T fusion exhaust; high-voltage biasing systems (10–50 kV DC) are mature technology (electrostatic precipitators, ion implanters) |
| Gap ratio | 1× in heat exchanger temperature regime (Na-to-water is analogue, Li is more reactive), ~100× in sCO2 turbomachinery scale (10 MWe → 500+ MWe), N/A for DEC electrodes (manufacturing is straightforward but survivability under fusion exhaust is unknown), 1× in HV biasing (mature technology but fusion-neutron environment requires radiation-hardened components) |
| Closure mechanism | Li/salt heat exchanger technology from fission programs with tritium permeation barriers (Al₂O₃, Er₂O₃ coatings); steam turbine is off-the-shelf (GE, Siemens, Mitsubishi); sCO2 turbomachinery commercialization underway (Echogen, GE targeting 2025–2030 commercial deployment); DEC electrode replacement via remote handling every 1–3 years (schedule TBD pending Anvil/Hammir data); HV biasing systems from industrial applications |
| Classification | Degrading (heat exchanger leaks reduce availability and create tritium contamination risk; DEC electrode erosion shortens replacement intervals and increases maintenance cost; turbine maintenance increases O&M; not binary because all components are repairable or replaceable) |
| Evidence tier | 4 (near-regime: heat exchangers demonstrated for similar liquid metals, steam turbines fully mature, sCO2 at 10 MWe scale; DEC electrodes are manufacturing extrapolation not R&D, but survivability is unvalidated → hardware tier is 4 acknowledging DEC uncertainty is survivability not manufacturing) |

**Function-level mean: F7 = (3 + 4) / 2 = 3.5**

---

### Heritage Credit (D-T Mirror Lineage)

**Applicable heritage**: Mirror (MFTF, TMX) → **Floor = 2.5** on F1–F7

**Application**:
- F1 (Plasma Performance) = 2.5 → **no change** (exactly at 2.5 floor)
- F2 (Driver / Energy Input) = 4.0 → **no change** (above floor)
- F3 (Instability Control) = 2.5 → **no change** (exactly at floor)
- F4 (Plasma-Wall Interaction) = 2.5 → **no change** (exactly at floor)
- F5 (Neutron/Particle Handling) = 3.0 → **no change** (above floor)
- F6 (Fuel Cycle Closure) = 2.0 → **raised to 2.5** (below floor)
- F7 (Power Conversion & BOP) = 3.5 → **no change** (above floor)

**Justification**: The mirror heritage credit floor of 2.5 (vs. tokamak 4.0) reflects limited D-T burning plasma experience: TMX and MFTF operated in the 1980s but were deuterium-only or decommissioned before D-T campaigns. No magnetic mirror has ever operated with tritium fuel. However, the tandem mirror physics basis (electrostatic plugging, sloshing-ion stabilization, classical transport) was validated at TMX and provides qualitative heritage. The floor applies to F6 (Fuel Cycle Closure), raising it from 2.0 to 2.5 — the Li breeding blanket concept benefits from 1980s MARS/MINIMARS design heritage (LiPb TBR 1.15) even though no operational validation exists. F1, F3, F4 exactly hit the 2.5 floor without adjustment. All other functions exceed the floor.

---

### Binary Risks

1. **TBR < 1.0 after realistic port penetrations** (F6 physics): Cylindrical 2π blanket geometry with 15–20% of surface allocated to NBI, ECH, diagnostics, vacuum access, and module gaps may reduce effective TBR below 1.0, requiring external tritium supply indefinitely (economically non-viable for fleet deployment). MARS achieved TBR 1.15 with LiPb in yin-yang geometry, but Realta's cylindrical geometry with undisclosed blanket type has no experimental TBR validation.

2. **Tritium extraction failure from Li circuit** (F6 hardware): No demonstrated kg/day tritium extraction from FLiBe, LiPb, liquid Li, or HCPB at fusion plant scale; if extraction efficiency is <90% or permeation losses exceed 1 g/day, tritium inventory accumulates in blanket (exceeding regulatory limits) or fuel cycle cannot close without external tritium purchase at $35k/g.

3. **End-plug confinement failure below Q = 3** (F1 physics): If DCLC instability suppression via sloshing ions proves 50% less effective than arXiv modeling predicts, end-plug electrostatic potential collapses from ≥5 kV target to 2–3 kV, main-cell ion losses via drift modes increase, Q degrades from Q > 5 target to Q = 2–3, recirculating fraction rises from ~23% to >50%, and plant produces zero net electricity. Anvil device (~2028) will test this, but no experimental validation exists today.

---

### Function-Level Means (for Python C7 computation)

- **F1**: 2.5 (exactly at heritage floor)
- **F2**: 4.0
- **F3**: 2.5 (exactly at heritage floor)
- **F4**: 2.5 (exactly at heritage floor)
- **F5**: 3.0
- **F6**: 2.5 (raised from 2.0 by heritage floor)
- **F7**: 3.5

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.8
  C3: 3.2
  C4: 2.5
  C5: 2.0
  C8: 3.0
  F1: 2.5
  F2: 4.0
  F3: 2.5
  F4: 2.5
  F5: 3.0
  F6: 2.5
  F7: 3.5
  binary_risks:
    - "TBR < 1.0 after realistic port penetrations in cylindrical 2π blanket geometry"
    - "Tritium extraction failure from Li circuit at kg/day fusion plant scale"
    - "End-plug confinement failure below Q = 3 due to DCLC instability"
---
```
