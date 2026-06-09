---
ID: 20b-renaissance-stellarator
Concept: Renaissance Stellarator (Renaissance Fusion)
Company: Renaissance Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Editorial Synthesis: Renaissance Stellarator (Renaissance Fusion)

## 1. Executive Summary

- **Most important risk**: The flowing liquid Li-LiH wall with suspended Pb pebbles is entirely on paper — no thermo-fluid or MHD analysis published, no experimental demonstration in *any* magnetic confinement geometry, and no path to validate at sub-reactor scale. This integrated FW/blanket/shield architecture is Renaissance's core cost differentiator, but it's TRL 2-3 with fundamental physics unknowns.
- **Most important advantage**: Laser-patterned HTS film on cylindrical surfaces eliminates traditional stellarator coil winding entirely — potentially bypassing both the REBCO tape supply bottleneck (no need for thousands of km of tape) and the 3D coil fabrication nightmare (cylindrical substrates instead of complex modular coils). If film deposition scales, this could deliver stellarator coils cheaper than any tokamak magnet approach.
- **LCOE ballpark**: 70 $/MWh at 1 GWe NOAK (model output) — this is library-only costing with zero overrides and is nearly meaningless. Renaissance has published zero cost data for any subsystem. The true LCOE is bounded only by plausibility: 50 $/MWh if both innovations work, 150+ $/MWh if either fails.
- **Confidence verdict**: Low — the physics design point is peer-reviewed and quantitatively complete (Prost & Volpe 2024, excellent neutronics and systems analysis), but the two enabling technologies (laser-patterned magnets at TRL 3-4, liquid metal wall at TRL 2-3) are both undemonstrated at scale, and zero economic data exists.

## 2. What Matters Most for LCOE

Ranked by LCOE impact potential:

### 2.1 Laser-Patterned HTS Magnet Cost (C220103: $1,106M library default, 20% of capital)
- **Assumed value**: $1,106M from library defaults scaling with R₀ = 3.8 m, B = 10.2 T, and STELLARATOR archetype parameters
- **Source**: None — Renaissance has published no REBCO film deposition cost, no laser patterning throughput, no conductor area per cylinder, no total system cost. The 6 T Helmholtz demonstrator at 1.2 m validates the physics concept but provides zero manufacturing cost data.
- **Sensitivity**: C220103 is 20% of 1 GWe overnight capital. A ±50% swing ($550M – $1,660M) moves LCOE by ±7 $/MWh. However, the true range is far wider: if cylindrical film deposition proves cheaper per ampere-meter than wound REBCO tape (plausible — eliminates winding labor, uses cylindrical substrates amenable to automated deposition), magnet cost could drop to $500–700M and LCOE to ~60 $/MWh. Conversely, if laser patterning requires custom film quality control that doesn't scale, or if 20–40 T peak fields demand film thickness that makes deposition economically prohibitive, magnet cost could exceed $2B and LCOE rises to 85+ $/MWh.
- **What would flip the conclusion**: A full-scale field-period magnet cylinder (6.3 m length, 10–15 T on-axis capability) delivered at documented cost with validated laser-patterned current paths at reactor-relevant J_c. If Renaissance demonstrates this at <$100M per cylinder and needs 4–8 cylinders for the full reactor, total magnet cost is $400–800M and LCOE drops below 65 $/MWh — stellarators become the cheapest fusion path. If the demonstrator costs >$500M per cylinder, the concept is economically dead regardless of liquid-wall performance.

### 2.2 Liquid Li-LiH Wall System Integration (C220101: $154M library default, but structurally wrong)
- **Assumed value**: $154M for first wall/blanket from library defaults that assume a solid first wall with contained coolant — fundamentally different from a flowing liquid metal wall that *is* the first wall, blanket, and partial shield
- **Source**: None — the blanket paper (Prost et al. 2024, J. Nucl. Mater.) provides material compositions and neutronics but no cost data. No thermo-fluid analysis, no MHD pressure drop calculations, no liquid metal circulation system design, no cost estimate.
- **Sensitivity**: The library default is structurally inapplicable. If the liquid wall eliminates conventional blanket module fabrication (claimed "reduced solid components replacement"), C220101 could drop by 30–50% ($100M savings, -2 $/MWh LCOE). However, if MHD pressure drops require massive circulation pumps, or if Li-LiH corrosion of the V-Cr-Ti vessel necessitates frequent replacement, or if Pb pebble coating (SiC at 700–900°C in flowing Li-LiH) degrades faster than assumed, the liquid metal *system* cost could exceed conventional solid blankets by 2–3× ($300M penalty, +5 $/MWh).
- **What would flip the conclusion**: A successful flowing liquid metal wall demonstration in a stellarator magnetic field geometry at >1 MW/m² wall loading, with measured MHD pressure drops, validated heat extraction uniformity, and demonstrated tritium extraction from Li-LiH at >1 g/day. This is a ~10-year experimental program requiring a dedicated test facility (no existing stellarator can accommodate this). If the demo works and system cost is <$200M, LCOE stays below 75 $/MWh. If the demo reveals insurmountable MHD flow instabilities or corrosion issues, Renaissance must redesign to solid FW/blanket — losing the compactness advantage, increasing radial build from 91 cm to 1.2+ m, and raising total capital cost by the claimed 20% (LCOE from 70 → 85+ $/MWh).

### 2.3 Ignited Operating Point Achievability (p_input: 5 MW vs. 50+ MW if ignition fails)
- **Assumed value**: Q = ∞ (ignition) with 5 MW residual burn-control power, based on dossier claim "design point at 10 keV" and zero steady-state heating
- **Source**: Dossier and design-point paper reference (Prost & Volpe, Nucl. Fusion 2024). No published confinement scaling validation, no beta or density data in extracted sources (data gap #4). Ignition at 10 keV is aggressive for a stellarator — most compact stellarator designs target Q = 5–20, not Q = ∞.
- **Sensitivity**: If ignition is not achieved and Renaissance requires 40–60 MW of NNBI at steady state (at 60% neutralization efficiency = 70–100 MW wallplug), recirculating power rises from ~48 MW to ~120 MW, net output drops from 1000 MWe to ~930 MWe at fixed fusion power, and $/kWe increases 8%. LCOE rises from 70 → 76 $/MWh. Not decisive, but non-trivial — and the NNBI system cost (C220104: $25M library default) would increase 10–15× to $250–400M if sized for steady-state operation.
- **What would flip the conclusion**: Publication of the full design-point paper (Nucl. Fusion 64, 2024, 026007) with plasma beta, density, confinement time, and alpha-heating power balance. If the published τ_E and n·T·τ product demonstrate ignition margin at 10 keV with conservative assumptions, Q = ∞ is credible and 70 $/MWh LCOE holds. If the confinement scaling extrapolation is optimistic and ignition requires 15 keV or higher beta than achievable, auxiliary heating becomes a permanent cost burden.

### 2.4 Compact Radial Build and Structural Cost (CAS21: $598M library default)
- **Assumed value**: $598M for buildings/site structures from library scaling — but the blanket paper explicitly claims "reducing radial build from 1.3 m to 1 m could reduce a 1 GWe reactor's cost by up to 20%." Renaissance's 91 cm build is 30% more compact than the library's default assumptions.
- **Source**: Infoscience-bitstreams output.md §1 Introduction (20% cost reduction claim) — this is a systems-model output from the design-point paper, not a CAS21-specific figure, so it cannot be used as a direct override. However, it signals that the library-default building cost may be overestimated for this compact machine.
- **Sensitivity**: If the 20% systems-level cost reduction is real and half of it comes from smaller buildings (a plausible allocation), CAS21 drops from $598M to ~$450M, saving $148M and reducing LCOE by ~2 $/MWh. However, if the compact geometry introduces unanticipated structural costs — coil stress management at 20–40 T peak field in a 91 cm build, electromagnetic forces on the cylindrical magnet assemblies, liquid metal containment integration — CAS21 and C220105 (primary structure) could rise by 20–30% (+$100M, +2 $/MWh).
- **What would flip the conclusion**: Publication of the design-point paper's cost breakdown showing which CAS accounts benefit from the 20% reduction. If buildings, structure, and magnets all scale down proportionally with radial build (plausible for a cylindrical architecture), LCOE drops to ~65 $/MWh. If the cost reduction is concentrated in non-capital items (construction schedule, materials transport) and capital accounts are unaffected, the library default is correct and LCOE stays at 70 $/MWh.

### 2.5 VH₂ Neutron Shield Cost and Maturity (C220102: $105M library default, but novel material)
- **Assumed value**: $105M from library defaults pricing conventional shielding (concrete, water, steel). Renaissance uses 54 cm of vanadium hydride (VH₂), which the blanket paper notes is "not as cost effective as concrete" but achieves 91 cm total build vs. >1 m with concrete alone.
- **Source**: Infoscience-bitstreams output.md §5 — VH₂ selected for compactness despite higher cost; no dollar figure provided. No long-term irradiation data for VH₂ at reactor fluence. No industrial-scale VH₂ production demonstrated.
- **Sensitivity**: If VH₂ costs 3–5× more per unit volume than concrete (plausible for metal hydride vs. commodity material), and the 54 cm shield volume is ~200–300 m³, C220102 could rise from $105M to $250–400M (+$150–300M, +3–5 $/MWh LCOE). However, if the compactness enables smaller magnets and buildings that offset the shield premium (the 20% cost reduction claim in 2.4), net impact is neutral.
- **What would flip the conclusion**: Demonstration of large-volume VH₂ production at <$50/kg with validated neutron shielding performance and radiation stability to 0.1 dpa (shield damage tolerance). If VH₂ proves manufacturable at <$100M for the full reactor shield, the compact build advantage is real. If VH₂ costs >$500M or suffers hydrogen embrittlement under irradiation requiring frequent replacement, Renaissance must redesign to conventional shielding (thicker build, larger machine, 20% cost penalty).

## 3. Risk Verdicts

### 3.1 Liquid Li-LiH Wall Thermo-Fluid and MHD Behavior (Impact: Critical)
- **Verdict**: Genuinely uncertain
- **Rationale**: No stellarator has ever operated a flowing liquid metal first wall. The 700–900°C Li-LiH must flow uniformly in a non-axisymmetric magnetic field with varying field direction and magnitude — MHD pressure drops, flow stability, turbulence, and heat extraction uniformity are all unknown. The blanket paper provides neutronics (TBR = 1.53–1.60, excellent) but zero thermo-fluid analysis. The liquid metal wall is not a cost optimization — it is the *enabling architecture* for the compact build. If it doesn't work, the entire concept must be redesigned.
- **What would retire this risk**: A flowing liquid metal test loop in a >5 T stellarator-like field with demonstrated stable flow at >10 MW/m² heat flux and <1 MPa MHD pressure drop. This requires a dedicated experimental facility (cannot be tested at component scale in a lab). If the test succeeds, the liquid wall is validated and Renaissance's path forward is credible. If the test reveals fundamental MHD instabilities or unmanageable pressure drops, the concept is unviable in its current form.

### 3.2 Laser-Patterned HTS Film Scalability to 10–15 T Reactor Fields (Impact: Critical)
- **Verdict**: Unlikely resolvable in first generation
- **Rationale**: Film deposition of REBCO on meter-scale cylindrical substrates is demonstrated at 6 T, 1.2 m diameter, 20 K. Reactor operation requires 10–15 T on-axis with 20–40 T peak fields on the conductor. Scaling challenges: (1) Film thickness must increase for higher current density — does deposition rate/quality degrade? (2) Laser patterning must maintain precise current paths over larger areas at higher resolution. (3) Quench protection for a patterned film is fundamentally different from a tape-wound coil — how do you detect and mitigate quenches in a 2D current distribution? (4) Radiation tolerance of the film-on-cylinder architecture at 10¹⁹ n/cm² fluence is undemonstrated.
- **What would retire this risk**: A full-scale reactor field-period cylinder (6.3 m length, 10+ T capability) operated at 20 K with validated quench protection and documented manufacturing cost. This is a 5–10 year magnet R&D program. If Renaissance delivers this by 2030, the approach is validated for Gen-1 deployment. If the demonstrator reveals insurmountable challenges (film quality degradation at required thickness, laser patterning defects, quench propagation failures), Renaissance must fall back to conventional HTS tape winding — losing the manufacturing cost advantage and likely becoming uncompetitive with other stellarator approaches.

### 3.3 Ignition at 10 keV in a Compact Stellarator (Impact: Moderate-High)
- **Verdict**: Likely resolvable
- **Rationale**: The 4-field-period quasi-symmetric design with cylindrical piecewise approximation is published and peer-reviewed. The neutronics are solid (TBR = 1.6 with full coverage). However, the confinement scaling that delivers ignition at 10 keV is not validated in the extracted sources (plasma beta, density, confinement time are missing — data gap #4). Ignition in a compact stellarator is achievable if beta ≥3–4% and confinement is HSX-class or better, but this is unproven at R = 3.8 m scale.
- **What would retire this risk**: Publication of the full design-point paper with equilibrium β, n_e, τ_E, and alpha-heating power balance. If the published ignition margin is >20% at conservative confinement assumptions, Q = ∞ is credible. Alternatively, a successful intermediate-scale demonstration (Thea Energy's Eos, Proxima's STEP-aligned prototype, or Renaissance's own pilot device) achieving H_ISS04 ≥ 1.2 in a compact stellarator would validate the confinement extrapolation.

### 3.4 V-Cr-Ti Vacuum Vessel Fabrication and Li-LiH Corrosion (Impact: Moderate)
- **Verdict**: Likely resolvable
- **Rationale**: V-14.5Cr-5Ti at 5 cm thickness is thin for a vacuum vessel (ITER uses ~10 cm stainless steel). Corrosion resistance to Li-LiH at 700–900°C is the design driver — the blanket paper selects V-Cr-Ti specifically for this. However, no large-scale V-Cr-Ti fabrication exists, and long-term corrosion data in flowing Li-LiH at 900°C is sparse. If corrosion proves worse than expected, vessel lifetime drops below the 32 FPY structural DPA limit (200 DPA / 6.25 DPA/yr = 32 years), requiring mid-life vessel replacement.
- **What would retire this risk**: Corrosion testing of V-14.5Cr-5Ti in flowing Li-LiH at 900°C for >10,000 hours with measured mass loss <10 μm/yr. If corrosion is manageable, the 40-year lifetime is achievable. If corrosion exceeds 50 μm/yr, vessel replacement every 10–15 years is required, dropping capacity factor from 80% to ~70% and raising LCOE by 7–10 $/MWh.

### 3.5 Pb Pebble Coating Durability (SiC or Similar) (Impact: Moderate)
- **Verdict**: Likely resolvable
- **Rationale**: Lead pebbles (0.1–5 mm diameter) require SiC or similar coatings to resist corrosion from Li-LiH and provide electrical insulation at 700–900°C. SiC is well-characterized for high-temperature applications, but durability in a flowing liquid metal environment with neutron irradiation is undemonstrated. If coatings degrade, uncoated Pb dissolves into the Li-LiH, contaminating the coolant and potentially shorting electrical currents.
- **What would retire this risk**: SiC-coated Pb pebbles tested in flowing Li-LiH at 900°C under neutron irradiation (fission test reactor or spallation source) for >1 year with <1% coating failure rate. If coatings prove durable, the Pb pebble concept is viable. If failure rates exceed 5% per year, pebbles require frequent replacement — a maintenance burden that could reduce capacity factor and add O&M cost.

### 3.6 No Published Cost Data Anywhere (Impact: Critical for modeling)
- **Verdict**: Resolvable only by company disclosure
- **Rationale**: Renaissance has published excellent physics and engineering analysis (peer-reviewed systems study, detailed neutronics, optimized power cycle), but zero cost data for any subsystem. The design-point paper performs "economically optimized" parameter selection via a systems model — implying cost estimates exist internally — but these are not publicly available. Without company-grounded overrides, all LCOE modeling is library-only and nearly meaningless.
- **What would retire this risk**: Publication of the design-point paper's cost outputs or a separate techno-economic study with subsystem-level dollar figures (even if rough). If Renaissance discloses that total capital is $3–4B for 1 GWe (vs. $5.5B library default), LCOE drops to 50–55 $/MWh and stellarators become the cheapest fusion path. If they disclose $7–8B (laser-patterned magnets more expensive than assumed), LCOE rises to 90+ $/MWh and competitiveness is lost.

## 4. Structural Advantages and Disadvantages

### Advantages (relative to conventional D-T tokamak baseline)

1. **Eliminates REBCO tape supply bottleneck** by depositing film on cylindrical substrates instead of winding pre-fabricated tape. Global REBCO tape production is thousands of km/year; a single ARC-class reactor requires >5,000 km. Renaissance's approach bypasses this entirely — if film deposition scales, they can build magnets independent of the tape supply chain. Cost direction: potentially eliminates a 2–5 year procurement bottleneck and enables faster deployment, though cost magnitude is unknown.

2. **Integrated liquid wall replaces three subsystems** (first wall + blanket + partial shield) with a single flowing Li-LiH layer. The blanket paper claims this reduces "solid components replacement rates compared with solid first walls." If true, O&M cost drops and capacity factor rises (fewer scheduled outages for blanket segment replacement). Magnitude: plausibly 5–10 percentage points higher CF vs. solid FW designs (80% vs. 75%), worth 3–5 $/MWh LCOE reduction.

3. **Compact geometry (R = 3.8 m, 91 cm radial build)** is 50–70% smaller than conventional stellarators (HELIAS 5-B at R ~ 22 m, W7-X at R = 5.5 m) and 35% smaller than Thea Helios (R = 8 m). The blanket paper explicitly claims up to 20% total cost reduction from the compact build. Even if only half realized (10%), this is worth ~10 $/MWh LCOE advantage.

4. **Cylindrical modular architecture** (4 field periods, 6.3 m cylinders) may simplify maintenance vs. conventional non-planar stellarator coils. No maintenance concept is published, but the geometry suggests overhead crane removal of field-period modules — potentially faster than tokamak sector extraction or classical stellarator coil access. If maintenance downtime is reduced from 20 days/year to 12 days/year, capacity factor rises from 80% to 83% (worth ~2 $/MWh).

5. **No Li-6 enrichment required** (natural lithium in Li-LiH) avoids the geopolitical supply-chain risk and cost premium of 60–90% enriched Li-6. Compared to concepts requiring enrichment (e.g., Thea Helios at 65% Li-6), this saves $50–100M in initial inventory and eliminates a deployment bottleneck. LCOE impact: ~1–2 $/MWh advantage.

6. **sCO₂ Brayton-Rankine at 49–51% gross efficiency** (Famà et al. 2023) is 10–15 points higher than conventional Rankine cycles (35–40%). Higher cycle efficiency means smaller thermal plant for the same net electric output — CAS23 advantage of 15–25% (worth ~3–5 $/MWh LCOE reduction vs. baseline Rankine).

### Disadvantages (cost additions vs. baseline)

1. **Liquid Li-LiH wall is undemonstrated in any fusion device** — if MHD flow proves unmanageable or heat extraction is non-uniform, the entire first wall/blanket must be redesigned to solid structures. This would eliminate the compactness advantage (radial build increases from 91 cm to 1.2+ m), enlarge the machine, and increase capital cost by the claimed 20% (from $5.5B to $6.6B at 1 GWe, +13 $/MWh LCOE).

2. **Laser-patterned HTS film at TRL 3–4** carries manufacturing scale-up risk that conventional tape-wound coils don't. If film deposition doesn't scale or quench protection proves unsolvable, Renaissance must fall back to REBCO tape winding — losing the manufacturing advantage and likely becoming cost-equivalent to Proxima or Type One Energy (both pursuing conventional HTS winding in stellarators).

3. **VH₂ neutron shield is exotic and potentially expensive** — the 54 cm VH₂ layer achieves compactness but at unknown cost and with no industrial production precedent. If VH₂ proves prohibitively expensive (>$500M for the shield), the capital premium offsets the compactness advantage and LCOE rises ~5–8 $/MWh vs. conventional concrete shielding.

4. **V-Cr-Ti vacuum vessel has no industrial supply chain** — same issue as Thea Helios, but more severe because Renaissance needs the vessel to resist Li-LiH corrosion at 900°C. If V-Cr-Ti proves unqualifiable at scale, the fallback is stainless steel with protective coatings — thicker vessel, larger machine, higher cost. Magnitude: plausibly 5–10% capital penalty if redesign is required.

5. **Ignited operation at 10 keV is unvalidated in compact stellarators** — if ignition fails and Renaissance requires 50–80 MW of NNBI at steady state, recirculating power rises and C220104 (heating systems) increases from $25M to $250–400M. LCOE impact: ~5 $/MWh if auxiliary heating is required.

6. **No published cost data** means all modeling is speculative. This is the largest *modeling* disadvantage, not necessarily an actual cost penalty — Renaissance may have internal estimates showing 30% lower cost than the library default, or they may discover costs are 50% higher during detailed design.

## 5. Cross-Concept Positioning

### Within the stellarator family

Renaissance sits at the **cylindrical laser-patterned HTS, liquid-metal wall, ignited compact** corner of the stellarator landscape. Direct comparables:

**05-planar-coil-stellarator (Thea Energy / Helios)**: Both pursue stellarator coil manufacturing disruption via radically different methods. Thea simplifies *geometry* (planar coils, relaxed tolerances) while keeping conventional winding; Renaissance eliminates *winding entirely* (laser-patterned film). Cost direction: genuinely divergent — Thea's approach is TRL 4–5 with Canis prototype and near-term validation path via Eos; Renaissance's is TRL 3–4 lab-only with no announced intermediate-scale demonstrator. Thea has higher near-term deployment probability; Renaissance has higher long-term cost reduction potential if film deposition scales. LCOE: Thea 241 $/MWh (library-only), Renaissance 70 $/MWh (library-only) — but both are unmeasurable without company cost data.

**09-qi-stellarator-hts (Proxima Fusion)**: Proxima pursues quasi-isodynamic geometry with conventional 3D HTS coils (W7-X/HELIAS heritage). Renaissance's compact QS design at R = 3.8 m vs. Proxima's likely R = 5–6 m creates a fundamental size delta. Cost comparison: Renaissance's laser-patterned cylindrical magnets (if successful) should be cheaper per ampere-meter than Proxima's 3D modular coils, but Renaissance carries liquid-wall risk that Proxima avoids with solid blankets. Net direction: Renaissance cheaper *if both innovations work*; Proxima safer bet with lower technical risk.

**10-large-scale-stellarator (Gauss Fusion)**: If Gauss pursues W7-X-class conventional stellarators at R = 10–22 m with LTS or LTS+HTS 3D coils, Renaissance has a structural 3–6× size advantage (smaller major radius, more compact build, lower building volume). This is the most dramatic geometric divergence in the stellarator family. LCOE direction: Renaissance potentially 40–60% cheaper if compactness claim (20% cost reduction) and magnet innovation (film deposition cheaper than 3D winding) both validate. However, Gauss's large-scale approach has better confinement scaling (τ_E ∝ R³ in some regimes) and lower risk of beta limits.

**20a-type-one-stellarator (Type One Energy)**: Type One uses modular stellarator coils with HTS, emphasizing simplified coil shapes optimized for manufacturability. Both Type One and Renaissance target magnet cost reduction, but via different strategies (Type One: simpler modular coils, Renaissance: eliminate winding). Cost comparison depends entirely on unvalidated manufacturing processes for both. Physics: Type One has published less design-point detail than Renaissance; direct comparison is limited.

**36-helical-coil-stellarator (Helical Fusion / HESTIA)**: Helical coils (LHD heritage) vs. cylindrical piecewise coils is a topological choice with different cost structures. Helical coils: fewer discrete components (2–4 continuous windings vs. Renaissance's 4 field-period cylinders), simpler power supplies, but complex 3D bucking structure. Renaissance: more modular (4 cylinders removable independently), potentially easier maintenance, but unproven laser-patterned current distribution. Cost direction: unknown — both approaches are uncosted in the literature.

### The compact stellarator gambit

Renaissance's 3.8 m major radius with 91 cm radial build is the most compact stellarator design point in the surveyed corpus. This compactness is *enabled* by two undemonstrated technologies (liquid metal wall for thin blanket, HTS film for high field), creating a binary outcome:

- **If both work**: Renaissance delivers stellarator electricity at 50–65 $/MWh (cheaper than any tokamak, cheaper than fission, competitive with renewables + storage). The compact geometry reduces capital cost by ~20% vs. conventional stellarators, and the magnet/blanket innovations add another ~20–30% reduction. Total: 35–45% cheaper than library-default stellarators, translating to LCOE of 50–60 $/MWh at 1 GWe NOAK.

- **If either fails**: Renaissance loses the compactness advantage (liquid wall failure forces thicker build, or magnet cost is no better than conventional HTS winding) and becomes cost-equivalent to other advanced stellarators (Thea, Proxima, Type One) at 70–90 $/MWh. Still potentially viable, but no longer a cost leader.

The modeled 70 $/MWh is library-only costing that applies standard stellarator defaults to a non-standard architecture — it's almost certainly wrong in either direction by 20–40 $/MWh. The true LCOE is unknowable without Renaissance disclosing cost data.

## 6. Modeling Confidence

**Rating**: Low

### Data-anchored parameters (9 / 14 major inputs)
- Plasma geometry (R₀ = 3.8 m, a ~ 0.93 m, A = 4.1): high confidence, peer-reviewed design point
- Magnetic field (B₀ = 10.2 T, B_peak = 20–40 T): high confidence for on-axis, medium for peak (range from dossier, not extracted paper)
- Radial build (91 cm plasma-to-coil): high confidence, detailed in blanket paper
- Fusion power (~2000 MW): high confidence, quoted in blanket paper
- Thermal power (~2200 MWth): high confidence
- Net electric (1000 MWe): high confidence, design target
- TBR (1.53–1.60): high confidence, OpenMC neutronics with conservative assumptions
- Cycle efficiency (49–51% gross, 34% net): high confidence, published Famà et al. 2023
- Availability (80% at 40-year lifetime): medium-high confidence, design specification

### Speculative / unknown parameters (5 / 14 major inputs)
- Auxiliary heating (5 MW assumed for ignited operation): **low confidence** — no published NNBI system sizing or burn-control power requirement; 5 MW is analyst estimate for residual ECRH in ignited stellarator. If ignition fails, true value is 50–100 MW wallplug.
- Plasma beta, density, confinement time: **low confidence** — missing from extracted sources (data gap #4); required to validate ignition claim. The design-point paper exists but is not extracted.
- Magnet cost ($1,106M library default): **low confidence** — zero published data on REBCO film deposition cost, laser patterning throughput, conductor area, or total system cost. Plausible range $400M – $2.5B depending on film deposition scalability.
- First wall/blanket cost ($154M library default): **low confidence** — library assumes solid FW with contained coolant; Renaissance's flowing liquid wall is structurally different. True cost depends on unanalyzed MHD, thermo-fluid, and corrosion behavior. Plausible range $100M – $500M.
- VH₂ shield cost ($105M library default): **low-medium confidence** — library prices conventional shielding; VH₂ is exotic and potentially 3–5× more expensive per volume. Plausible range $100M – $400M.

### Dominant source of LCOE uncertainty

**Liquid metal wall viability**, not magnet cost. The magnet uncertainty is large ($700M to $2B plausible range), but it's a manufacturing/economics question with a clear validation path (build a full-scale demonstrator, measure cost). The liquid wall uncertainty is fundamental physics — if MHD pressure drops are unmanageable or flow stability cannot be achieved in stellarator geometry, there is no fix short of complete redesign. A failed liquid wall forces:
- Radial build increase from 91 cm to 1.2+ m (eliminate compactness advantage)
- Redesign to solid first wall + blanket modules (add complexity, increase C220101 cost)
- Potentially thicker neutron shield (more VH₂ or switch to concrete, increase radial build further)
- Larger machine, higher capital cost across CAS21, C220103, C220105

Net impact of liquid wall failure: ~25–35% capital cost increase, LCOE from 70 → 95+ $/MWh. This is worse than the magnet cost upside/downside (~15 $/MWh swing), making the liquid wall the dominant risk.

The second-largest uncertainty is **ignition achievability** — if Renaissance requires steady-state auxiliary heating, recirculating power rises and C220104 balloons from $25M to $250–400M, adding ~5 $/MWh to LCOE. However, this is a physics question that can be resolved via publication of the design-point paper's confinement analysis or experimental validation in a pilot device.

## 7. What Would Change My Mind

### Evidence that would materially lower LCOE estimate (to ~50 $/MWh or below)

1. **Renaissance demonstrates a full-scale field-period cylinder** (6.3 m length, 10+ T on-axis) with laser-patterned REBCO film at documented cost <$100M per cylinder, *and* validates quench protection and field accuracy to <1% RMS error, *and* the total 4-cylinder magnet system costs <$500M. This proves the film deposition revolution is real. Combined with the compact geometry advantage (20% cost reduction claimed), LCOE drops from 70 → 50–55 $/MWh and stellarators become the cheapest fusion path.

2. **A flowing liquid metal wall test loop in stellarator-like field** (>5 T, non-axisymmetric) demonstrates stable flow at 10+ MW/m² heat flux with MHD pressure drop <1 MPa and uniform heat extraction within 10%, *and* tritium extraction from Li-LiH achieves >1 g/day at 900°C. This retires the liquid wall risk and confirms the integrated FW/blanket/shield architecture is viable. If both the magnet and liquid wall validate, LCOE is 45–55 $/MWh.

3. **Renaissance publishes the design-point paper's cost breakdown** showing total overnight capital <$4B for 1 GWe (<$4,000/kW), with documented magnet cost <$700M, liquid wall system <$200M, and buildings/structure savings from compact geometry >$500M vs. conventional stellarators. If the cost claim is third-party reviewed and grounded in supplier quotes or detailed bottom-up estimates, the library-only 70 $/MWh is too pessimistic by 25–35%.

### Evidence that would materially raise LCOE estimate (to >100 $/MWh, rendering concept uncompetitive)

1. **Liquid metal wall MHD test reveals fundamental instabilities** — flow oscillations, hot spots, or pressure drops >5 MPa that cannot be mitigated within the 91 cm radial build constraint. This forces redesign to solid FW/blanket, increasing radial build to 1.2+ m and raising capital cost by ~30% (from $5.5B to $7.2B at 1 GWe). LCOE rises from 70 → 95+ $/MWh, and Renaissance loses its primary differentiator vs. other stellarators.

2. **Laser-patterned film deposition proves unscalable to reactor-relevant J_c at 10–15 T** — film quality degrades at required thickness, laser patterning introduces current-path defects at >1% rate, or quench detection/protection is unsolvable for 2D patterned conductors. Renaissance falls back to conventional REBCO tape winding, magnet cost rises to $2–2.5B (comparable to other HTS stellarators), and LCOE increases to 85+ $/MWh. Without the magnet advantage, Renaissance is cost-equivalent to Proxima or Thea.

3. **Design-point paper reveals ignition is marginal or unachievable** — published confinement time or beta shows ignition requires 15 keV or higher density than achievable, forcing 60–100 MW of steady-state NNBI. C220104 rises from $25M to $400M, recirculating power increases from ~48 MW to ~120 MW, net output drops from 1000 MWe to ~930 MWe, and $/kWe increases 8%. LCOE rises from 70 → 78 $/MWh. Not a concept-killer, but eliminates the "essentially free heating" advantage of ignited operation.

4. **VH₂ shield proves prohibitively expensive or irradiation-unstable** — cost exceeds $500M for 54 cm shield, or hydrogen embrittlement under neutron flux requires replacement every 5–10 years. Renaissance must redesign to conventional shielding (concrete + steel), increasing radial build from 91 cm to 1.3+ m and raising capital cost by 15–25%. LCOE rises from 70 → 85 $/MWh, and the compactness advantage partially evaporates.
