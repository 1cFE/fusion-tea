---
ID: 18-p-b11-frc
Concept: PB11 FRC (TAE Technologies)
Company: TAE Technologies
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Synthesis: PB11 FRC (TAE Technologies)

## 1. Executive Summary

- **Single most important risk**: Net energy gain (Q>1) is undemonstrated for p-B11 fusion. TAE's Norman device operates at ~3 keV; reactor requires 100-200 keV — a 50× temperature leap and ~10⁶× increase in nT pressure. No FRC experiment has approached these conditions. The physics extrapolation is larger than ITER-to-D-T-reactor.

- **Single most important advantage**: Aneutronic fuel cycle eliminates ~$150M tritium infrastructure, 70% of neutron shielding costs, and enables hands-on maintenance. The blanket costs 50% of D-T baseline, shield costs 30%. This structural simplification is genuine — but only matters if the concept achieves Q>1.

- **LCOE ballpark**: $359/MWh (1 GWe NOAK projection). Native-scale 50 MWe plant shows $438/MWh. Both figures are 3-4× higher than D-T tokamak targets (~$100-120/MWh) and uncompetitive with fission or renewables. The model assumes thermal conversion at 40% efficiency; direct energy conversion at 90% (if ICC works) would halve these numbers but remains TRL 2-3.

- **Confidence verdict**: **Low**. TAE has published exactly one reactor specification: 50 MWe net output. Every other parameter (plasma volume, magnetic field, confinement time, NBI power, Q target) is analyst-extrapolated from experimental scaling laws or physics constraints. The power balance is suspect: spec implies p_input/P_native = 100/50 = 2.0, yielding Q_eng = 0.5 — physically inconsistent with net power production. Until TAE discloses Q targets and confinement scaling data, LCOE estimates are speculative.

## 2. What Matters Most for LCOE

### 1. Auxiliary heating power (p_input) — Dominates recirculating power fraction
- **Assumed value**: 100 MW (model_setup.py:114-124)
- **Source**: Physics-derived from reactor-class NBI requirements (100-300 keV beam energy, Putvinski 2019)
- **Sensitivity**: At p_input = 100 MW and P_native = 50 MWe, the recirculating fraction is 67%, leaving Q_eng = 0.5. This is below breakeven. If p_input must rise to 150 MW to sustain the plasma, Q_eng drops to 0.33 — no net power. Conversely, if TAE achieves higher Q_plasma (Q ~ 10 instead of the back-solved ~6) and p_input drops to 50 MW, Q_eng rises to 1.0 and LCOE improves proportionally.
- **What would flip the conclusion**: If p_input ≤ 25 MW at Q_plasma ≥ 20, LCOE drops below $200/MWh and the concept becomes competitive with advanced D-T designs. This requires beam-target coupling efficiency at 90%+ and far better confinement than current FRC scaling laws predict.

### 2. Q_plasma (fusion gain) — Sets capital cost per MW and all downstream economics
- **Assumed value**: ~5.9 (library back-solved from P_fus ≈ 594 MW / p_input = 100 MW)
- **Source**: Derived, not published by TAE. Nevins & Swain (2000) suggest Q ~ 2-5 is achievable for p-B11 at T_i = 150 keV if confinement is excellent.
- **Sensitivity**: Q_plasma is the square root of LCOE for any fusion concept. At Q = 3, the plant requires 2× the capital cost per net MW (more fusion power to overcome losses). At Q = 10, capital cost per MW halves. The model output shows CAS22 (reactor plant equipment) at $21B for the 1 GWe fleet — 58% of overnight capital. If Q drops from 6 to 3, CAS22 doubles to $42B and LCOE rises to ~$600/MWh.
- **What would flip the conclusion**: Q ≥ 15 brings LCOE below $250/MWh even with thermal conversion. This requires confinement time τ_E ≥ 0.5s at reactor densities (5×10²⁰ m⁻³) — far beyond current FRC record (30 ms at 2×10¹⁹ m⁻³).

### 3. Energy conversion efficiency (η_th or η_DEC) — 2.25× LCOE multiplier
- **Assumed value**: 40% (Rankine steam cycle, model_setup.py thermal conversion assumption)
- **Source**: tae-energy-conversion-clarification.md §How do you produce electricity — TAE FAQ explicitly describes steam/turbine pathway
- **Sensitivity**: Thermal at 40% vs. supercritical CO2 at 48% is a 20% LCOE swing. Thermal at 40% vs. ICC direct conversion at 90% is a 2.25× difference in electric output for the same fusion power. If ICC works and adds <$500M to capital (reasonable for a 5-meter cylindrical electrode structure), LCOE drops from $359/MWh to ~$180-200/MWh.
- **What would flip the conclusion**: ICC demonstration at MW scale with >80% measured efficiency. This retires the largest single uncertainty in the cost structure. If ICC fails and TAE is locked into thermal conversion, LCOE remains >$300/MWh indefinitely and the concept is non-competitive.

### 4. Confinement scaling (τ_E at reactor scale) — Gates capital cost and Q_plasma
- **Assumed value**: Unknown (not disclosed by TAE, not modeled explicitly)
- **Source**: Steinhauer (Phys. Plasmas 2011) provides FRC scaling laws; Putvinski (2019) assumes τ_E ~ 0.1-0.5s for reactor-class FRCs
- **Sensitivity**: FRC τ_E scales empirically as τ_E ∝ r_s^1.5 / T_i^0.5. Norman's τ_E ~ 5 ms at r_s = 0.4 m, T_i ~ 1 keV. Da Vinci at r_s = 2 m, T_i ~ 150 keV requires τ_E ≥ 0.3s to close Lawson criterion for p-B11. If scaling degrades faster than r_s^1.5 (e.g., due to anomalous transport at large radius), τ_E may saturate at 0.05-0.1s, forcing a 3-5× increase in plasma volume (chamber_length from 8 m to 20-30 m). This directly scales CAS21 (structures/site) and CAS22 (reactor equipment) costs.
- **What would flip the conclusion**: Experimental validation of τ_E ≥ 0.5s at r_s ≥ 1 m and T_i ≥ 50 keV in Copernicus or a follow-on device. If achieved, the 8-meter chamber length is adequate and capital costs hold. If τ_E plateaus at 0.05s, the concept is dead — no economically feasible chamber size can achieve net power.

### 5. NBI capital cost — $3.6B at 1 GWe scale dominates CAS22
- **Assumed value**: $180M per 50 MWe module (disabled in model_setup.py:186-206 but noted as critical)
- **Source**: ITER NBI analogue ($20-30M per 16.5 MW injector → $120-180M for 100 MW at 6 injectors)
- **Sensitivity**: Model output shows C220104 (supplementary heating) at $706M for the native-scale plant. This is library-default RF heating cost, not NBI-specific. If the NBI override is enabled at $180M per module, the 1 GWe fleet (20 modules) adds $3.6B to CAS22, raising overnight capital from $36B to $39B and LCOE from $359/MWh to ~$380/MWh. If NBI scales unfavorably (e.g., 10 injectors at $30M each per module due to 100-300 keV beam energy complexity), NBI costs hit $6B and LCOE exceeds $400/MWh.
- **What would flip the conclusion**: Volume production NBI at <$10/W (vs. ITER's $17/W). Semiconductor-style learning curves from pulsed power component mass manufacturing could drive costs down by 50%. If TAE achieves $5/W NBI at 100 MW (via integration, supply chain optimization, and NOAK economies), NBI cost drops to $500M total fleet-wide and LCOE improves by ~$20/MWh.

## 3. Risk Verdicts

### Net energy gain undemonstrated for p-B11 (Q>1 at 100-200 keV)
- **Verdict**: **Genuinely uncertain** — leans toward unlikely but not impossible
- **Rationale**: The physics literature (Rider 1997, Nevins & Swain 2000) does not prove p-B11 Q>1 is unachievable; it shows bremsstrahlung losses are severe and confinement requirements are extreme. TAE's experimental program is methodical (Norman → Copernicus with 2.5× NBI power). If Copernicus reaches 10-15 keV and validates confinement scaling, extrapolation to 150 keV becomes defensible. But the temperature leap is unprecedented — no magnetic confinement device has sustained 100+ keV plasmas at fusion-relevant densities.
- **What would retire this risk**: Copernicus demonstration of T_i ≥ 30 keV at n_e ≥ 5×10¹⁹ m⁻³ with τ_E ≥ 50 ms and Q_plasma ≥ 0.1 (even for D-D side reactions). This would validate the scaling trajectory. Without it, Da Vinci is a >10× physics extrapolation from experimental basis.

### FRC confinement scaling to reactor size (τ_E and stability at r_s = 2 m, I_p ~ 10 MA)
- **Verdict**: **Unlikely resolvable** without a dedicated intermediate-scale device
- **Rationale**: Norman's r_s = 0.4 m → Da Vinci's r_s = 2 m is a 5× linear scale jump. FRC instabilities (tilt mode, kink mode) grow with system size, and kinetic stabilization mechanisms effective at small scale weaken at large radius (Steinhauer 2011). No FRC experiment has exceeded r_s ~ 0.6 m. The C-2/C-2U devices demonstrated stability at 0.3-0.4 m via neutral beam-driven rotation and edge biasing, but this is 5-7× smaller than reactor needs. TAE's roadmap shows Copernicus (upgraded Norman) then Da Vinci — no intermediate-scale confinement test.
- **What would retire this risk**: A 1-2 meter radius FRC test facility operating at 10-30 keV with sustained stability for ≥1 second. This is a $500M-1B machine (comparable to NSTX-U or C-Mod scale). Without it, Da Vinci is betting reactor-scale stability on 5× extrapolation from sub-scale experiments — historically a poor bet in fusion.

### Beam-driven sustainment power requirements (p_input vs. P_native power balance closure)
- **Verdict**: **Likely resolvable** if Q_plasma ≥ 10 is achieved, otherwise blocking
- **Rationale**: The spec inconsistency (p_input/P_native = 2.0 → Q_eng = 0.5) is likely a disclosure ambiguity, not a fundamental physics error. TAE has not clarified whether "50 MWe" is gross electric (before recirculation) or net to grid. If gross, the power balance closes: P_fus ~ 600 MW → P_electric ~ 240 MW at 40% thermal efficiency → 50 MWe net after 190 MW recirculation (100 MW NBI + 50 MW balance-of-plant + 40 MW magnet losses). This is plausible but awful economics (Q_eng ~ 0.26). Alternatively, if Q_plasma is higher (Q ~ 15-20) and p_input is overstated, the power balance closes at reasonable recirculation (<50%).
- **What would retire this risk**: TAE disclosure of Q_eng target and NBI power scaling vs. reactor thermal power. If TAE states "Da Vinci operates at Q_eng = 0.8-1.0 as a pilot demonstrator, not a commercial power plant," the spec is honest and LCOE is moot (it's a physics validation machine). If TAE claims "50 MWe net commercial power," the current spec is inconsistent and requires revision.

### Direct energy conversion (ICC) TRL and cost
- **Verdict**: **Unlikely resolvable** on Da Vinci timescale (2026 construction → 2028-2030 operation)
- **Rationale**: The ICC is TRL 2-3 (patent concepts, no prototype). Da Vinci uses thermal conversion per TAE's FAQ. ICC at >80% efficiency is critical for economic viability but deferred to future plants. The 5-meter cylindrical electrode structure described in patents is not obviously infeasible (simpler than stellarator coils), but high-voltage electrode survivability in fusion exhaust is unproven. Developing ICC to TRL 7-8 requires 5-10 years and $100-300M investment.
- **What would retire this risk**: ICC prototype test at 1-10 MW scale on Norman or Copernicus, demonstrating >70% conversion efficiency and electrode survivability over 100+ shots. If successful by 2028, ICC could be retrofitted to Da Vinci or incorporated in follow-on plants. If ICC never works, p-B11 FRC is locked into 40-48% thermal efficiency and LCOE >$300/MWh — non-competitive.

### Regulatory pathway for aneutronic fusion
- **Verdict**: **Likely resolvable** — NRC will establish framework, timeline uncertain
- **Rationale**: p-B11 produces <1% neutron energy, enabling hands-on maintenance and eliminating tritium licensing burdens. This is a genuine safety advantage, but the NRC has not yet created a licensing category for "low-activation fusion" distinct from D-T reactors (10 CFR Part 50). If Da Vinci is regulated as a Class I fission reactor equivalent, licensing costs and timelines are similar to D-T fusion (~$50-100M, 3-5 years). If NRC creates a streamlined pathway (analogous to Part 53 for advanced reactors), licensing could be faster and cheaper ($20-50M, 2-3 years).
- **What would retire this risk**: NRC rulemaking establishing aneutronic fusion licensing framework by 2026-2027. Precedent exists: NRC issued policy statement on fusion regulation in 2020 and launched Advanced Reactor licensing rulemaking in 2018-2020. TAE's Da Vinci application could drive NRC to clarify aneutronic fusion treatment. Worst case: NRC treats it as novel Class I fission reactor and requires full EIS — adds 2-3 years and $100M. Best case: NRC treats it as a non-power particle accelerator (existing framework) — adds 1 year and $10-20M.

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T tokamak baseline

1. **Eliminated subsystems** (quantified from model output):
   - **C220101 (blanket)**: 50% cost reduction → saves ~$1.5M per 50 MWe module (generic $3.0M → native $1.5M). At 1 GWe scale (20 modules), this is ~$30M savings. The blanket is no longer a tritium breeder — just thermal capture.
   - **C220102 (shield)**: 70% cost reduction → saves ~$1.5M per module ($2.1M → $0.6M), or ~$30M at fleet scale. Neutron wall loading is 10-20× lower than D-T (0.05-0.2 MW/m² vs. 2-4 MW/m²).
   - **C220108 (divertor)**: Eliminated entirely → saves $47.8M per module (generic value), or ~$950M at fleet scale. FRC has axial exhaust, not toroidal divertor. This is the single largest capital savings.
   - **C220109 (direct energy conversion)**: Not used in Da Vinci baseline ($23.3M generic → $0 native). However, this is a *missed opportunity* cost, not a savings — thermal conversion at 40% vs. DEC at 90% is a 2.25× penalty on electric output.
   - **CAS27 (special materials / fuel inventory)**: Reduced from $3.3M to $5.0M in model (small increase reflects beryllium in thermal blanket, if used). More importantly, no tritium inventory (~$30-150M avoided at D-T scale) and no lithium-6 enrichment (~$50-100M avoided). For p-B11, fuel is commodity boron and hydrogen at <$100k/year.

   **Total structural capital savings**: ~$1.0-1.5B at 1 GWe scale vs. D-T tokamak baseline. This is 3-4% of overnight capital ($36B). Meaningful but not transformative.

2. **Simplified magnets**: FRC beta ~ 0.9-1.0 eliminates high-field superconducting TF coils. Model override sets C220103 (magnets) at $80M absolute (vs. $21.4M library default — actually an *increase* due to resistive coil power consumption trade-off). The "simplification" is geometric (axisymmetric solenoids vs. toroidal coils) but not necessarily cost-reducing unless HTS is avoided. If resistive copper coils are used, capital drops to ~$50M but operating costs rise by $10-20M/year (magnet resistive losses at 10-20 MW continuous draw).

3. **Hands-on maintenance**: Aneutronic fusion enables contact maintenance (no remote handling manipulators, no hot cell infrastructure). This reduces CAS23 (turbine plant equipment installation and maintenance tooling) and CAS26 (instrumentation & control for remote ops). The model does not explicitly override these — estimated savings are ~$50-100M at fleet scale. More importantly, maintenance *downtime* drops from weeks (remote operations) to days (hands-on), improving capacity factor by 5-10 percentage points. This is worth ~$20-40/MWh in LCOE.

4. **No tritium fuel cycle**: Eliminates CAS24 subsystems (fuel handling, tritium processing, isotope separation, inventory management). Model does not override CAS24 ($24.4M native = generic), suggesting library does not yet model tritium-specific fuel handling separately. Real D-T plant tritium systems cost $100-300M (ITER's tritium plant is €500M, ~$550M). p-B11 saves this entirely.

**Net structural advantage**: ~$1.5-2.0B capital savings at 1 GWe scale, plus $20-40/MWh LCOE improvement from capacity factor gains. This is significant but insufficient to overcome the Q penalty. D-T tokamak at Q = 30 with $37B capital beats p-B11 FRC at Q = 6 with $35B capital — the fusion gain dominates.

### Disadvantages vs. D-T tokamak baseline

1. **NBI capital cost dominance**: Model shows C220104 (supplementary heating) at $706M native (library default, likely RF heating analogue). If the NBI override is enabled at $180M per 50 MWe module, the 1 GWe fleet NBI capital is $3.6B. This is 10% of total overnight capital. For comparison, ITER's NBI is $550M for 33 MW (~2% of ITER capital). TAE's beam-driven concept is NBI-intensive by design — the capital cost scales with reactor count, not shared infrastructure.

2. **Extreme temperature requirements**: p-B11 requires T_i ~ 150-250 keV vs. D-T's 10-20 keV. Auxiliary heating power scales with temperature gap and energy confinement time. At p_input = 100 MW for 50 MWe net, the heating power is 2× the electric output — unprecedented recirculating fraction for a commercial power plant. D-T tokamaks target p_input/P_net ~ 0.2-0.3 (Q_eng ~ 3-5). p-B11's Q_eng ~ 0.5-1.0 is structurally worse.

3. **Undemonstrated confinement scaling**: D-T tokamak confinement is empirically validated across 5 decades of experiments (ITER → JT-60SA → JET → DIII-D → Alcator C-Mod) spanning 5× in major radius and 50× in plasma current. FRC confinement scaling is validated only over 2× in radius (C-1 to Norman, 0.2 m → 0.4 m) and 10× in temperature (0.3 keV → 3 keV). The Da Vinci extrapolation is 5× in radius and 50× in temperature beyond experimental basis — equivalent to building ITER in 1990 without JET, TFTR, or JT-60 data.

4. **Low Q_plasma ceiling**: p-B11 fusion cross-section is ~1000× smaller than D-T at 10 keV, and ~100× smaller even at optimal p-B11 temperatures (150 keV). This fundamentally limits achievable Q_plasma. Nevins & Swain (2000) estimate p-B11 Q ~ 5-10 at best, even with perfect confinement. D-T routinely targets Q = 20-40 in reactor designs (ARC, SPARC, Commonwealth Fusion). The Q ceiling translates directly to higher capital cost per net MW for p-B11.

5. **Thermal conversion lock-in**: Da Vinci baseline uses 40% efficient steam cycle, sacrificing 2.25× in electric output vs. the aspirational 90% ICC. If ICC development fails, p-B11 is permanently locked into thermal conversion while D-T advanced concepts pursue direct conversion (magnetic expander, cusp divertors with electrostatic collectors). The efficiency gap becomes structural, not transitional.

**Net structural disadvantage**: Q_plasma ceiling and recirculating power fraction are the killers. The capital savings from eliminated subsystems (~$2B) are overwhelmed by the Q penalty. At Q = 6 vs. Q = 30, the p-B11 plant requires 5× the fusion power per net MW, scaling CAS22 and CAS30 proportionally. This adds ~$10-15B to overnight capital at 1 GWe scale, outweighing all aneutronic advantages.

## 5. Cross-Concept Positioning

**TAE's p-B11 FRC occupies a unique position**: it is the only magnetically confined steady-state aneutronic concept at reactor scale in the fusion landscape.

### vs. other aneutronic concepts
- **IEC / Polywell (electrostatic confinement)**: Smaller scale (~kW-MW prototypes), lower TRL (3-4), but avoiding magnetic field complexity. IEC capital costs are low ($10-50M for a 10 MW device) but Q<1 is structural due to beam-background collisions. TAE's FRC has plausible path to Q>1 (if confinement scaling holds) but at $1-2B capital per 50 MWe.
- **p-B11 laser ICF (HB11 Energy, Marvel Fusion)**: Pulsed inertial confinement with entirely different cost structure. Driver (petawatt lasers or heavy-ion beams) costs $1-5B, but blanket/shield is minimal and direct conversion via ballistic collection may reach 60-80% efficiency. Repetition rate (1-10 Hz) and target fabrication costs (~$0.10-1.00 per shot) are the economic challenges. TAE's steady-state FRC avoids target costs but inherits magnetic confinement complexity.

### vs. other FRCs
- **Helion (D-D/D-He³ pulsed FRC with magnetic compression)**: Helion's Polaris targets 50 MWe from D-D/D-He³ at T_i ~ 50-100 keV (lower than p-B11's 150-250 keV). Helion uses pulsed magnetic compression (inductive) rather than beam sustainment, avoiding TAE's NBI capital costs (~$3-5B saved at fleet scale) but requiring pulsed power infrastructure ($500M-1B). Helion's D-He³ fuel produces ~5% neutron energy vs. p-B11's <1%, so shielding costs are intermediate. Critically, Helion targets direct energy conversion at 95% efficiency as the baseline, not a future upgrade — this is the key architectural difference. If Helion's DEC works, their LCOE could be 2× better than TAE's thermal-conversion baseline.

### vs. D-T magnetic confinement (tokamaks, stellarators, mirrors)
- **Tokamaks (Commonwealth SPARC, Tokamak Energy, Type One Energy)**: D-T tokamaks at Q = 20-40 target LCOE ~$80-150/MWh with NOAK capital $20-30B per GWe. TAE's $36B per GWe at Q ~ 6 yields $359/MWh — 3× worse. The aneutronic advantages (~$2B capital savings, +$20-40/MWh capacity factor) are insufficient to close the Q gap. D-T tokamaks win on LCOE by 2-3× even after accounting for tritium breeding costs and remote maintenance penalties.
- **Stellarators (Type One Energy, Proxima Fusion)**: Stellarators target Q = 10-20 at $30-50B per GWe NOAK. TAE's simpler FRC geometry ($36B) is competitive on capital, but Q ~ 6 yields worse LCOE. If TAE achieves Q = 15 (upper end of p-B11 physics estimates), the concepts are comparable on economics ($250/MWh stellarator vs. $280/MWh FRC).
- **Magnetic mirrors (Realta Fusion, Type One mirror variants)**: Mirrors share linear geometry and axial loss channels with FRCs but use open-field-line confinement with electrostatic end plugs. Realta's D-T mirror with direct conversion targets 70-80% thermal-to-electric efficiency at Q ~ 20-30. TAE's FRC at Q ~ 6 with 40% thermal efficiency is structurally worse by 4-5× on electric output per fusion MW. If TAE's ICC works (90% efficiency), the gap narrows to 2× — FRC still loses but becomes defensible as a tritium-free alternative.

**Positioning verdict**: TAE's p-B11 FRC is a high-risk, high-reward bet on aneutronic physics. It occupies the "harder fusion physics, simpler engineering" quadrant — opposite to D-T tokamaks ("solved fusion physics, complex engineering"). If Q>1 is achieved and ICC direct conversion works, p-B11 FRC could reach LCOE ~$150-200/MWh and compete with advanced fission. If Q remains <5 or ICC fails, the concept is non-competitive at any capital cost. There is no middle ground.

## 6. Modeling Confidence

**Rating: Low**

### Data anchoring
- **Data-anchored parameters (5 of 12)**: chamber_length (Putvinski 2019, Steinhauer 2011), n_e (Rider 1997, Nevins & Swain 2000), T_e (Rider 1997 bremsstrahlung analysis), P_native (TAE disclosure Dec 2025), energy conversion pathway (TAE FAQ thermal/steam).
- **Physics-constrained but unvalidated (4 of 12)**: plasma_t (r_s = 2 m from Norman × 5 scaling, within Putvinski 2019 range but not experimentally tested), B (5 T from MHD pressure balance at β ~ 0.9, not directly measured), plasma_volume (derived from r_s and L via FRC geometry conventions), b_center (0.5 T from Norman × 5 scaling, consistent with Putvinski reactor designs).
- **Speculative (3 of 12)**: p_input (100 MW is reactor-class NBI power order-of-magnitude, not Da Vinci-specific), Q_plasma (back-solved from library power balance at ~5.9, not published by TAE), τ_E (unspecified, inferred from Lawson criterion closure).

**Dominant source of LCOE uncertainty**: Q_plasma and the coupling to p_input. The model back-solves P_fus ~ 594 MW from P_native = 50 MWe and spec inputs, implying Q ~ 6 at p_input = 100 MW. If TAE's actual Q target is 3 (achievable but marginal for p-B11), P_fus must double to ~1200 MW and capital costs scale accordingly, raising LCOE to ~$600/MWh. If Q target is 15 (optimistic but within physics bounds), P_fus drops to ~400 MW and LCOE improves to ~$250/MWh. The 2.4× spread in LCOE is driven by 5× uncertainty in Q.

### Model limitations
1. **NBI cost not overridden in baseline**: The C220104 override ($180M) is *disabled* in model_setup.py:186 due to Q uncertainty. Library default ($706M) likely reflects RF heating analogue, not NBI-specific costs. Enabling the NBI override adds ~$20-30/MWh to LCOE, worsening the competitive position.

2. **No confinement time modeling**: The library's power balance solver does not expose τ_E as an input or output. Lawson criterion closure (n × T × τ_E ≥ threshold) is implicit in the fusion power calculation but not validated against FRC empirical scaling laws (Steinhauer 2011 τ_E ∝ r_s^1.5 / T_i^0.5). If FRC scaling degrades at reactor size, the spec's 50 m³ plasma volume is undersized and LCOE increases proportionally with required chamber volume.

3. **Capacity factor not adjusted for aneutronic maintenance advantage**: Model uses library-default capacity factor (~85-90% implied from LCOE). p-B11's hands-on maintenance should improve CF by 5-10 percentage points vs. D-T remote ops (CF → 90-95%), worth $20-40/MWh. This improvement is not captured — actual LCOE could be $340-380/MWh rather than $359/MWh if maintenance advantage is real.

4. **No sensitivity analysis on energy conversion efficiency**: The model assumes 40% thermal efficiency (steam cycle). Switching to supercritical CO2 (48%) or ICC direct conversion (90%) requires rerunning the model with adjusted η_th, but this is not parameterized in the current setup. The 40% → 90% efficiency improvement would reduce LCOE from $359/MWh to ~$180/MWh (2× improvement) — the single largest sensitivity, but not explored in model output.

**What would improve confidence**:
- TAE disclosure of Q_plasma target, confinement time, and NBI power scaling for Da Vinci → enables validation of spec power balance
- Copernicus experimental results demonstrating T_i ≥ 30 keV at n_e ≥ 5×10¹⁹ m⁻³ with τ_E ≥ 50 ms → validates FRC confinement scaling trajectory
- Independent cost model for NBI at 100-300 keV, 100 MW scale → anchors C220104 override
- ICC prototype test at 1-10 MW scale with measured efficiency → retires energy conversion uncertainty

## 7. What Would Change My Mind

### Evidence that would *improve* the LCOE estimate (make the concept more viable):

1. **Copernicus demonstration of T_i = 30-50 keV at n_e ≥ 1×10²⁰ m⁻³ with Q_D-D ≥ 0.01** (even from D-D side reactions in the plasma): This would validate the confinement scaling trajectory from Norman's 3 keV to Da Vinci's 150 keV as physically plausible, not fantasy. If Copernicus hits 50 keV at relevant density, the remaining 3× temperature jump to 150 keV is within beam heating capability (300 keV NBI energy is ITER-class technology). LCOE estimate would tighten to ~$300-400/MWh with "Medium" confidence, and I would believe TAE has a path to Q>1.

2. **TAE disclosure that "50 MWe" is a pilot demonstrator operating at Q_eng ~ 0.5-0.8, with commercial follow-on plants targeting Q_eng ≥ 1.5 at 200-500 MWe scale**: This would resolve the power balance inconsistency as an honest staging strategy rather than a physics error. Da Vinci LCOE would be moot (it's a demo plant, not commercial), and the economic analysis would shift to the unspecified follow-on plant. If TAE projects Q_plasma = 15-20 for the commercial plant with ICC at 90% efficiency, LCOE could reach $150-200/MWh — competitive with advanced fission.

3. **ICC demonstration at 1-10 MW scale on Norman/Copernicus with ≥70% measured efficiency over 100+ pulses**: This would retire the energy conversion uncertainty and halve the LCOE estimate to ~$180-200/MWh. Combined with Q = 10 at reactor scale, p-B11 FRC becomes a defensible alternative to D-T tokamaks on the basis of tritium-free operation and hands-on maintenance. I would upgrade confidence to "Medium" and recommend continued R&D investment.

### Evidence that would *worsen* the LCOE estimate (kill the concept):

1. **Copernicus fails to exceed T_i = 10 keV at n_e ≥ 5×10¹⁹ m⁻³ despite 50+ MW NBI input**: This would indicate beam heating efficiency or confinement physics is fundamentally worse than expected. If $500M+ invested in Copernicus cannot reach 10 keV (1/15 of reactor target), the extrapolation to 150 keV is untenable. I would conclude Q>1 is unachievable within economically feasible plasma volumes and retire the concept as non-viable. LCOE estimate becomes irrelevant — the physics does not close.

2. **Independent FRC scaling analysis shows τ_E saturates at 0.05-0.1s due to anomalous transport at r_s > 1 m**: This would force plasma volume to increase 3-5× (chamber_length from 8 m to 20-30 m) to maintain Lawson criterion closure, scaling CAS21/CAS22 proportionally. Overnight capital would rise from $36B to $50-70B per GWe, pushing LCOE to $500-700/MWh — non-competitive with any alternative. The concept survives as a physics research platform but is economically dead.

3. **TAE confirms Da Vinci baseline is thermal conversion and ICC development is deferred beyond 2035**: This would lock p-B11 FRC into 40-48% thermal efficiency for the next decade, guaranteeing LCOE >$300/MWh even at Q = 10. Combined with D-T tokamaks reaching LCOE ~$100-150/MWh in the same timeframe (Commonwealth SPARC, Type One Energy), p-B11 FRC loses the economic race by 2-3×. I would downgrade the concept to "non-competitive but scientifically interesting" and recommend stopping investment at pilot scale.
